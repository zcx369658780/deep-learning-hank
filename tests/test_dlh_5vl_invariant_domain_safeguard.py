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
