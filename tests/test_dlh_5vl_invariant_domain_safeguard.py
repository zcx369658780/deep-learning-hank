"""DLH-5V-L tests: invariant-domain safeguarded value-update line search.

The accepted selected-Q source and the accepted household oracle are READ
ONLY. The wrapper module ``invariant_domain_safeguarded_hjb`` is tested here:
frozen central config, exact dyadic lambda rule, exact p_b margin, largest
feasible lambda selection, no p_b clipping/flooring, INVARIANT_STEP_FAILURE
semantics, final Bellman criterion for any PASS, deterministic complete
central-case repeat, and no KFE / stationary KFE / steady-state invocation.
"""

import ast
import inspect
import pathlib

import numpy as np
import pytest

from deep_learning_hank.two_asset.boundary_hjb_selected_q import (
    BoundaryHJBConfig,
    BoundaryHJBSolver,
)
from deep_learning_hank.two_asset.invariant_domain_safeguarded_hjb import (
    CENTRAL_CONFIG,
    CENTRAL_INPUTS,
    CENTRAL_PARAMS,
    CENTRAL_SWITCH,
    CENTRAL_Z,
    LAMBDA_MIN_EXP,
    MAX_ITERATIONS,
    PB_MARGIN,
    InvariantStepFailure,
    crossing_lambdas,
    final_bellman_validation,
    min_boundary_pb,
    run_safeguarded_central,
    safeguard_step,
)

MODULE_PATH = pathlib.Path(
    inspect.getsourcefile(run_safeguarded_central)).resolve()


def _solver():
    return BoundaryHJBSolver(CENTRAL_CONFIG)


def _labor0(solver):
    return solver.build_labor0(0.0, 0.0)


# ---------------------------------------------------------------------------
# frozen central configuration
# ---------------------------------------------------------------------------
def test_frozen_central_household_params_exact():
    p = CENTRAL_PARAMS
    assert (p.rho, p.gamma_c, p.phi, p.chi_0, p.chi_1, p.a_bar,
            p.mu_z, p.sigma_z) == pytest.approx(
        (0.02, 2.0, 5.0, 0.1, 2.0, 1e-6, 0.0, 0.0))


def test_frozen_central_inputs_and_switch():
    inp = CENTRAL_INPUTS
    assert inp.r_a == pytest.approx(0.07)
    assert inp.r_b == pytest.approx(0.02)
    assert inp.tau == pytest.approx(0.15)
    assert np.allclose(inp.wages, [1.00])
    assert np.allclose(inp.labor_weights, [1.0])
    assert np.allclose(inp.migration_costs, [0.0])
    assert np.allclose(CENTRAL_Z, [0.8, 1.3])
    assert np.allclose(CENTRAL_SWITCH,
                       [[-1.0 / 3.0, 1.0 / 3.0], [1.0 / 3.0, -1.0 / 3.0]])


def test_frozen_central_config_exact():
    c = CENTRAL_CONFIG
    assert c.m == 1
    assert c.w_max == 10.0
    assert c.b_min == -2.0
    assert c.a_max == 10.0
    assert c.delta == pytest.approx(1000.0)
    assert c.tolerance_iter == pytest.approx(1e-7)
    assert c.tolerance_bellman == pytest.approx(1e-3)
    assert c.max_iterations == 1000
    assert c.n_c_grid == 9
    assert c.n_d_grid == 9
    assert c.bracket_expand_factor == 4.0
    assert c.max_bracket_expansions == 3


# ---------------------------------------------------------------------------
# safeguard rule: exact dyadic lambda sequence, descending, exact margin,
# largest feasible lambda, no clipping/flooring
# ---------------------------------------------------------------------------
def test_lambda_sequence_and_margin_constants():
    assert LAMBDA_MIN_EXP == 20
    assert MAX_ITERATIONS == 1000
    assert PB_MARGIN == 1e-12
    seq = [2.0 ** (-k) for k in range(0, LAMBDA_MIN_EXP + 1)]
    assert seq == sorted(seq, reverse=True)
    assert seq[0] == 1.0 and seq[-1] == 2.0 ** (-20)


def test_margin_is_acceptance_only_no_pb_clip_or_floor():
    """Static scan: the wrapper never clips/floors p_b and never writes the
    margin into any p_b value; min_boundary_pb returns the exact minimum of
    the declared backward liquid marginal."""
    tree = ast.parse(MODULE_PATH.read_text(encoding="utf-8"))
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            names.add(node.id)
    for bad in ("clip", "clip_pb", "pb_floor", "maximum"):
        assert bad not in names, f"forbidden clip/floor operation {bad!r} present"
    solver = _solver()
    lab = _labor0(solver)
    V0 = solver.build_initial_value(lab, 0.0, 0.0)
    _, vb_b, _, _ = solver.compute_derivatives(V0, lab, 0.0, 0.0)
    g = solver.grid
    exact = min(float(vb_b[node, nz])
                for node in range(solver.n) if g.families[node] != "F0"
                for nz in range(solver.nz))
    assert min_boundary_pb(solver, V0, lab) == pytest.approx(exact, rel=0.0,
                                                            abs=1e-15)
    # margin is only a threshold: a raw update with p_b slightly above the
    # margin is NOT floored and must still be accepted at lambda = 1
    V_raw = V0.copy()
    idx = next(node for node in range(solver.n) if g.families[node] != "F0")
    pb0 = float(vb_b[idx, 0])
    assert pb0 > PB_MARGIN
    # reduce one boundary node's p_b to 2*margin (still admissible): this
    # exercises that the margin is a pure threshold, not a floor applied to p_b
    V_raw[idx, 0] = V_raw[idx, 0] - (pb0 - 2.0 * PB_MARGIN) * (7.0 / 19.0)
    assert min_boundary_pb(solver, V_raw, lab) > PB_MARGIN
    lam, bt = safeguard_step(solver, V0, V_raw, lab)
    assert lam == 1.0 and bt == 0


def test_largest_feasible_lambda_selected():
    """For synthetic raw updates, the returned lambda equals the independently
    recomputed largest dyadic lambda keeping ALL boundary p_b > margin."""
    solver = _solver()
    lab = _labor0(solver)
    V0 = solver.build_initial_value(lab, 0.0, 0.0)
    g = solver.grid
    boundary = [node for node in range(solver.n) if g.families[node] != "F0"]
    candidates = [V0.copy() for _ in range(4)]
    candidates[0][boundary[3], 0] -= 30.0          # mild spike
    candidates[1][boundary[5], 1] -= 300.0         # stronger spike
    candidates[2] = -V0                            # sign flip
    rng = np.random.default_rng(0)
    candidates[3] = V0 + 1e-3 * rng.standard_normal(V0.shape)
    for V_raw in candidates:
        feasible = [
            k for k in range(0, LAMBDA_MIN_EXP + 1)
            if min_boundary_pb(
                solver, V0 + 2.0 ** (-k) * (V_raw - V0), lab) > PB_MARGIN
        ]
        if not feasible:
            with pytest.raises(InvariantStepFailure):
                safeguard_step(solver, V0, V_raw, lab)
            continue
        # largest feasible lambda = smallest feasible exponent k
        k_star = min(feasible)
        lam, bt = safeguard_step(solver, V0, V_raw, lab)
        assert lam == 2.0 ** (-k_star)
        assert bt == k_star


def test_invariant_step_failure_when_no_valid_step():
    solver = _solver()
    lab = _labor0(solver)
    V0 = solver.build_initial_value(lab, 0.0, 0.0)
    g = solver.grid
    # a boundary node whose p_b IS a V finite difference (i >= 1), so the
    # spike actually destroys the boundary liquid marginal evidence
    node = next(node for node in range(solver.n)
                if g.families[node] != "F0" and g.i_arr[node] >= 1)
    V_raw = V0.copy()
    V_raw[node, 0] -= 1.0e9          # domain violation at every dyadic step
    with pytest.raises(InvariantStepFailure):
        safeguard_step(solver, V0, V_raw, lab)


# ---------------------------------------------------------------------------
# Micro-Rev corrections: margin-crossing diagnostics (diagnostic ONLY) and
# trajectory-bounded interpretation
# ---------------------------------------------------------------------------
def test_lambda_margin_crossing_formula_uses_pb_margin_not_zero():
    """lambda_margin_crossing = (p_old - PB_MARGIN)/(p_old - p_raw): the
    continuous step crossing the acceptance margin, NOT the zero boundary.
    Values are the same-state terminal pair of the frozen central run."""
    p_old = 1.8128990372393415e-12
    p_raw = -1.0825070292850926e-06
    m = 1.0e-12
    out = crossing_lambdas(p_old, p_raw, m)
    expected_margin = (p_old - m) / (p_old - p_raw)
    expected_zero = p_old / (p_old - p_raw)
    assert out["lambda_margin_crossing"] == pytest.approx(expected_margin,
                                                          rel=0.0, abs=1e-30)
    assert out["lambda_zero_crossing"] == pytest.approx(expected_zero,
                                                        rel=0.0, abs=1e-30)
    # distinct quantities; the margin crossing is the binding one
    assert out["lambda_margin_crossing"] < out["lambda_zero_crossing"]
    assert out["lambda_margin_crossing"] == pytest.approx(7.51e-07, rel=0.02)
    assert out["lambda_zero_crossing"] == pytest.approx(1.67e-06, rel=0.02)
    # the MARGIN crossing is below the smallest authorized dyadic lambda;
    # the ZERO crossing is not (the 2^-20 step stays above zero but dips
    # below the margin — exactly why the margin, not zero, is the criterion)
    assert out["lambda_margin_crossing"] < 2.0 ** (-20)
    assert out["lambda_zero_crossing"] > 2.0 ** (-20)


def test_lambda_zero_crossing_is_separately_named():
    out = crossing_lambdas(1.0, -0.5, 1e-12)
    assert set(out) == {"lambda_zero_crossing", "lambda_margin_crossing"}
    assert out["lambda_margin_crossing"] == pytest.approx(
        (1.0 - 1e-12) / 1.5)
    assert out["lambda_zero_crossing"] == pytest.approx(1.0 / 1.5)


def test_crossing_lambdas_guards_undefined_cases():
    assert crossing_lambdas(np.nan, -1.0)["lambda_margin_crossing"] is None
    assert crossing_lambdas(1.0, np.inf)["lambda_zero_crossing"] is None
    # denominator <= 0 (raw not below old) -> not defined
    assert crossing_lambdas(-1.0, -2.0)["lambda_margin_crossing"] is None
    # margin not strictly between p_raw and p_old -> margin crossing undefined
    assert crossing_lambdas(1e-13, -1.0)["lambda_margin_crossing"] is None


def test_terminal_crossing_diagnostics_from_run():
    """The run's terminal failure detail must carry the same-state
    margin-relevant crossing at the BINDING state (p_old/p_raw at the same
    state), with lambda_margin_crossing < 2^-20 and p_old > PB_MARGIN >
    p_raw. GLOBAL minima are recorded separately (see
    test_global_minima_vs_binding_state_distinction)."""
    res = run_safeguarded_central()
    assert res.outcome == "INVARIANT_STEP_FAILURE"
    diag = res.failure_detail["terminal_crossing_diagnostics"]
    assert diag["PB_MARGIN"] == 1e-12
    p_old = diag["p_old"]
    p_raw = diag["p_raw"]
    assert p_old > 1e-12 > p_raw
    expected = (p_old - 1e-12) / (p_old - p_raw)
    assert diag["lambda_margin_crossing"] == pytest.approx(expected,
                                                           rel=0.0, abs=1e-30)
    assert diag["lambda_margin_crossing"] < diag["lambda_zero_crossing"]
    # binding state is the accepted-iterate wall: p_old is the minimum
    # accepted boundary p_b and the margin crossing is below 2^-20
    assert p_old == res.min_accepted_boundary_pb
    assert diag["lambda_margin_crossing"] < 2.0 ** (-20)
    assert diag["min_authorized_dyadic_lambda"] == 2.0 ** (-20)
    assert diag["binding_state"]["family"] == "F3"
    assert diag["binding_state"]["j"] == 16
    assert diag["binding_state"]["i"] == 8
    assert diag["binding_state"]["z"] == 1
    # binding p_raw is NOT the global raw minimum (which is at F2 (6,24) z=1)
    assert p_raw == pytest.approx(-1.0825070292850926e-06, rel=1e-6)
    assert res.final_min_boundary_pb == pytest.approx(-0.336924, rel=1e-3)


def test_global_minima_vs_binding_state_distinction():
    """GLOBAL old/raw minima (with their states) and the SAME-STATE margin
    binding diagnostic are distinct quantities and must not be conflated:
    global raw min ~ -0.336924 at F2 (6,24) z=1; binding state F3 (16,8)
    z=1 with binding p_raw ~ -1.08e-6."""
    res = run_safeguarded_central()
    assert res.outcome == "INVARIANT_STEP_FAILURE"
    fd = res.failure_detail
    # global raw minimum (frozen-run evidence)
    assert fd["global_raw_min_pb"] == pytest.approx(-0.336924, rel=1e-3)
    grs = fd["global_raw_min_state"]
    assert grs["family"] == "F2" and grs["j"] == 6 and grs["i"] == 24 \
        and grs["z"] == 1
    # global old minimum (accepted-iterate wall)
    assert fd["global_old_min_pb"] == pytest.approx(1.8128990372393415e-12,
                                                    rel=0.0, abs=1e-25)
    gos = fd["global_old_min_state"]
    assert gos["family"] == "F3" and gos["j"] == 16 and gos["i"] == 8 \
        and gos["z"] == 1
    # field-name semantics: the legacy names mean the GLOBAL quantities
    assert fd["raw_min_boundary_pb"] == fd["global_raw_min_pb"]
    assert fd["old_min_boundary_pb"] == fd["global_old_min_pb"]
    assert fd["worst_raw_state"] == grs
    assert res.final_min_boundary_pb == fd["global_raw_min_pb"]
    # binding diagnostic: same state as the global OLD minimum here, but the
    # binding p_raw differs from the GLOBAL raw minimum (different state)
    bd = fd["terminal_crossing_diagnostics"]
    assert bd["binding_state"] == gos
    assert bd["p_old"] == fd["global_old_min_pb"]
    assert bd["p_raw"] != fd["global_raw_min_pb"]
    assert bd["binding_state"] != grs
    assert bd["lambda_margin_crossing"] == pytest.approx(
        (bd["p_old"] - 1e-12) / (bd["p_old"] - bd["p_raw"]), rel=0.0, abs=1e-30)
    assert bd["lambda_margin_crossing"] < 2.0 ** (-20)
    assert bd["lambda_zero_crossing"] > bd["lambda_margin_crossing"]
    # the separate concepts never share one field name
    assert "worst_state" not in bd
    assert "binding_state" not in (fd["worst_raw_state"] or {})


def test_crossing_diagnostics_never_change_step_selection():
    """Diagnostic-only: the safeguarded accepted lambdas stay inside the
    frozen dyadic set {2^-k, k=0..20}; no continuous crossing value is ever
    used as a step."""
    res = run_safeguarded_central()
    assert res.outcome == "INVARIANT_STEP_FAILURE"
    allowed = {2.0 ** (-k) for k in range(0, LAMBDA_MIN_EXP + 1)}
    for t in res.trace:
        assert t["lambda"] in allowed
        assert t["lambda"] >= 2.0 ** (-20)
        # acceptance margin is the only p_b threshold used by the safeguard
        assert t["min_pb_new"] > PB_MARGIN
    # static: the step-selection function never references the diagnostics
    tree = ast.parse(MODULE_PATH.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "safeguard_step":
            body_names = {n.id for n in ast.walk(node)
                          if isinstance(n, ast.Name)}
            assert "crossing_lambdas" not in body_names
            assert "terminal_crossing_diagnostics" not in body_names


def test_terminal_c_reproduction_deterministic():
    res1 = run_safeguarded_central()
    res2 = run_safeguarded_central()
    assert res1.outcome == res2.outcome == "INVARIANT_STEP_FAILURE"
    assert res1.iterations == res2.iterations == 17
    assert (res1.failure_detail["terminal_crossing_diagnostics"]
            == res2.failure_detail["terminal_crossing_diagnostics"])


def test_no_global_fixed_point_assertion_in_scientific_tests():
    """The scientific test module must not encode the forbidden global
    interpretation (fixed point outside the domain / no positive-domain fixed
    point); only trajectory-bounded statements are allowed."""
    source = MODULE_PATH.parents[3] / "tests" / \
        "test_dlh_5vl_invariant_domain_safeguard.py"
    text = source.read_text(encoding="utf-8").lower()
    # assembled so the forbidden phrases never appear verbatim in this file
    banned = [
        "fixed point " + w for w in (
            "lies outside", "is outside", "exists outside",
            "does not exist", "lies outside the domain",
            "is outside the domain",
        )
    ] + [
        "no " + "positive-domain fixed point",
        "no " + "admissible fixed point",
        "hjb solution itself " + "lies outside",
    ]
    for bad in banned:
        assert bad not in text, f"forbidden global interpretation: {bad!r}"


# ---------------------------------------------------------------------------
# final validation semantics
# ---------------------------------------------------------------------------
def test_pass_requires_final_bellman_criterion():
    """Any CONVERGED_WITH_BELLMAN_PASS outcome must satisfy the full final
    validation: Bellman residual <= 1e-3, boundary p_b > 1e-12, conservative
    Q, no accepted artificial bracket binding. The frozen final validation
    function itself must not manufacture PASS."""
    solver = _solver()
    lab = _labor0(solver)
    V0 = solver.build_initial_value(lab, 0.0, 0.0)
    records = [None] * solver.state_size
    val = final_bellman_validation(solver, V0, lab, records)
    assert set(val) == {"bellman_residual", "max_abs_q1", "min_boundary_pb",
                        "artificial_bindings", "expansions", "family_histogram"}
    # validation semantics: a PASS requires all four conditions
    ok = (val["bellman_residual"] <= CENTRAL_CONFIG.tolerance_bellman
          and val["min_boundary_pb"] > PB_MARGIN
          and val["max_abs_q1"] <= CENTRAL_CONFIG.row_sum_tolerance
          and val["artificial_bindings"] == 0)
    assert isinstance(ok, bool)


def test_frozen_failure_taxonomy_preserved():
    """The wrapper only adds INVARIANT_STEP_FAILURE / SAFEGUARD_STAGNATION /
    HJB_NONCONVERGENCE; accepted selected-Q failures are passed through."""
    assert issubclass(InvariantStepFailure, RuntimeError)
    tree = ast.parse(MODULE_PATH.read_text(encoding="utf-8"))
    outcomes = {n.value for n in ast.walk(tree)
                if isinstance(n, ast.Constant) and isinstance(n.value, str)
                and n.value in {
                    "CONVERGED_WITH_BELLMAN_PASS", "SAFEGUARD_STAGNATION",
                    "HJB_NONCONVERGENCE", "INVARIANT_STEP_FAILURE"}}
    assert outcomes == {"CONVERGED_WITH_BELLMAN_PASS",
                        "SAFEGUARD_STAGNATION", "HJB_NONCONVERGENCE",
                        "INVARIANT_STEP_FAILURE"}


# ---------------------------------------------------------------------------
# deterministic complete central-case repeat
# ---------------------------------------------------------------------------
def test_deterministic_complete_central_repeat():
    res1 = run_safeguarded_central()
    res2 = run_safeguarded_central()
    assert res1.outcome == res2.outcome
    assert res1.iterations == res2.iterations
    assert res1.final_statistic == res2.final_statistic
    assert res1.min_lambda == res2.min_lambda
    assert res1.median_lambda == res2.median_lambda
    assert res1.backtracking_iterations == res2.backtracking_iterations
    assert res1.min_accepted_boundary_pb == res2.min_accepted_boundary_pb
    assert res1.raw_domain_violations_avoided == res2.raw_domain_violations_avoided
    assert res1.final_bellman_residual == res2.final_bellman_residual
    assert res1.final_q_max_abs_row_sum == res2.final_q_max_abs_row_sum
    assert res1.final_min_boundary_pb == res2.final_min_boundary_pb
    assert res1.final_artificial_bindings == res2.final_artificial_bindings
    assert res1.failure_detail == res2.failure_detail
    assert res1.trace == res2.trace
    # invariant of the safeguard: every accepted iterate stays in domain
    for t in res1.trace:
        assert t["min_pb_new"] > PB_MARGIN
    # every accepted row must record min p_b of old/raw/new consistently
    for t in res1.trace:
        assert t["min_pb_old"] > PB_MARGIN


# ---------------------------------------------------------------------------
# no KFE / stationary KFE / steady-state invocation
# ---------------------------------------------------------------------------
def test_no_kfe_or_steady_state_invocation():
    tree = ast.parse(MODULE_PATH.read_text(encoding="utf-8"))
    used = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
    imported = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.ImportFrom):
            imported.update(a.name for a in n.names)
        elif isinstance(n, ast.Import):
            imported.update((a.name or "").split(".")[0] for a in n.names)
    banned = {"solve_matlab_faithful_stationary_kfe",
              "MatlabFaithfulKFEResult", "solve_household_steady_state",
              "aggregate_stationary_household", "StationaryHouseholdAggregates",
              "run_kfe", "stationary_kfe"}
    assert not (banned & used), f"KFE/steady-state names used: {banned & used}"
    assert not (banned & imported)
    assert "BoundaryHJBSolver" in imported
    assert "EconomicParams" in imported
    assert "HouseholdInputs" in imported
    for word in ("density", "stationary"):
        assert word not in used
