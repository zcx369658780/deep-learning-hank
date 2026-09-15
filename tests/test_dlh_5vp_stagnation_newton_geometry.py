"""DLH-5V-P test suite — FTB stagnation residual decomposition + frozen-policy
Newton boundary geometry (Issue #64).

--------------------------------------------------------------------------
POST-REPAIR TEST-CONTRACT MIGRATION (Issue #67 / DLH-5V-S remediation)
--------------------------------------------------------------------------
Issues #64/#65/#66 were accepted while the accepted ``final=True`` F0
off-diagonal assembly dropped the z-block destination offset for z=1 rows
(``cols.append(dn)`` instead of ``cols.append(nz*self.n + dn)``). Issue #67
repaired that one authorized source location, which necessarily changes the
``final=True``/final-validation numbers these suites historically pinned.

Nothing here is deleted. The pre-repair numbers below are preserved as
EXPLICIT HISTORICAL CONSTANTS representing accepted Issue #64-#66 evidence,
and the runtime assertions now verify the REPAIRED semantics. The historical
defect remains reproducible from the accepted Issues, reports and commits and
is deliberately NOT re-created here (no monkeypatch, no old-blob checkout).

The convergence question is untouched: the corrected final residual
(``10.435094313164921``) is still far above the unchanged Bellman tolerance
(``1e-3``), so validated HJB convergence remains FALSE. See
``test_no_hjb_convergence_claimed_after_repair``.
"""

import ast
import inspect
import types

import numpy as np
import pytest

import deep_learning_hank.two_asset.stagnation_newton_geometry as g
from deep_learning_hank.two_asset.stagnation_newton_geometry import (
    EPS_ALPHA,
    HALF_ALPHA,
    MATERIAL_REDUCTION_RATIO,
    NEWTON_SOLVE_TOL,
    PB_MARGIN,
    RECONSTRUCT_STEPS,
    SCALING_CHECK_TOL,
    TERMINAL_A,
    TERMINAL_B,
    TERMINAL_C,
    NewtonGeometryFailure,
    boundary_crossing,
    boundary_direction_matrix,
    evaluate_trial,
    finalize_outcome,
    frozen_policy_newton_direction,
    reconstruct_issue63_stagnation_state,
    residual_decomposition,
    residual_stats,
    run_issue64_diagnostic_twice,
)
from deep_learning_hank.two_asset.boundary_hjb_selected_q import (
    BoundaryHJBSolver,
)
from deep_learning_hank.two_asset.local_resolvent_domain_geometry import (
    LocalGeometryFailure,
)

# ---------------------------------------------------------------------------
# HISTORICAL EVIDENCE — accepted Issue #64/#65/#66 pre-repair numbers.
#
# These document what the accepted (pre-repair) operator produced. They are
# NOT current runtime expectations: Issue #67's Owner-authorized z-block
# destination repair superseded them. They are retained because the accepted
# Issues, reports and commits cite them as accepted scientific evidence.
# ---------------------------------------------------------------------------
PRE_REPAIR_FINAL_RESIDUAL_CURRENT = 490.7560414005864    # accepted Issue #65
PRE_REPAIR_FINAL_RESIDUAL_STALE = 490.7560425919994      # accepted Issue #65 / #64
PRE_REPAIR_F0_OPERATOR_GAP = 24.601971766296664          # accepted Issue #66
PRE_REPAIR_AFFECTED_Z1_F0_ROWS = 298                     # accepted Issue #66
PRE_REPAIR_FINAL_RESIDUAL_DIFF = 488.0988429898615       # accepted Issue #64/#65
PRE_REPAIR_TERMINAL_64 = "DLH_5VP_STAGNATION_NEWTON_GEOMETRY__POSITIVE_BOUNDARY_SAFE_NEWTON_STEP_BUT_NONLINEAR_RESIDUAL_REDUCTION_INSUFFICIENT__FURTHER_DIRECTION_DESIGN_REQUIRED"

# ---------------------------------------------------------------------------
# REPAIRED SEMANTICS — current runtime expectations at the same accepted V_*.
# ---------------------------------------------------------------------------
REPAIRED_R_ITER_INF = 10.435094313164921
REPAIRED_FINAL_VALIDATION_RESIDUAL = 10.435094313165099
REPAIRED_R_FINAL_INF = 10.435094313165099
REPAIRED_R_FINAL_F0_MAX = 10.435094313165099
REPAIRED_R_DIFF_INF = 4.654054919228656e-13
REPAIRED_FINAL_VS_ITER_TOL = 1.0e-9
BELLMAN_TOLERANCE_UNCHANGED = 1.0e-3


# ---------------------------------------------------------------------------
# Module-scoped real-run fixture (one diagnostic + one deterministic repeat)
# ---------------------------------------------------------------------------
@pytest.fixture(scope="module")
def diag():
    result, identical = run_issue64_diagnostic_twice()
    return result, identical


# ---------------------------------------------------------------------------
# 1. Frozen constants (Issue #64 section 6)
# ---------------------------------------------------------------------------
def test_frozen_issue64_constants_exact():
    assert PB_MARGIN == 1e-12
    assert EPS_ALPHA == 1e-6
    assert HALF_ALPHA == 0.5
    assert MATERIAL_REDUCTION_RATIO == 0.50
    assert RECONSTRUCT_STEPS == 8


# ---------------------------------------------------------------------------
# 2. Exact frozen Issue #63 terminal reconstruction
# ---------------------------------------------------------------------------
def test_reconstruction_reproduces_accepted_issue63_terminal():
    rec = reconstruct_issue63_stagnation_state()
    trace = rec["trace"]
    assert len(trace) == RECONSTRUCT_STEPS
    assert all(t["path"] == "root" and t["cap_direct"] is False for t in trace)
    # accepted step 8 values (DLH_5VO_CONTINUATION_TRACE.csv, bit-level)
    t8 = trace[-1]
    assert t8["accepted_max_stat"] == pytest.approx(
        3.6614352438846254e-08, rel=1e-12)
    assert t8["delta_selected"] == pytest.approx(
        3.5087694086826935e-09, rel=1e-12)
    assert t8["selected_min_pb"] == pytest.approx(
        4.8089461301970005e-09, rel=1e-12)
    assert t8["halving_count"] == 39
    # every accepted step keeps the effective domain
    assert all(t["selected_min_pb"] > PB_MARGIN for t in trace)
    # limiting wall state on every accepted step = F3 (13,13), z=1 (node 332)
    for t in trace:
        w = t["worst_after"]
        assert w["node"] == 332 and w["family"] == "F3"
        assert w["j"] == 13 and w["i"] == 13 and w["z"] == 1
    # accepted trajectory cross-checks (rows 1 and 2 vs accepted CSV)
    assert trace[0]["delta_selected"] == pytest.approx(
        0.031789280949542364, rel=1e-12)
    assert trace[1]["sector_changes"] == 8
    # accepted final validation residual reproduced via preserved pre-step-8
    # F0 records
    solver = rec["solver"]
    val = g.final_bellman_validation(
        solver, rec["V_star"], rec["labor0"], rec["records_pre_step8"])
    # PRE-REPAIR this was PRE_REPAIR_FINAL_RESIDUAL_STALE == 490.7560425919994.
    # After the Owner-authorized Issue #67 z-block destination repair the same
    # accepted V_* / preserved pre-step-8 records give the corrected value.
    assert val["bellman_residual"] == pytest.approx(
        REPAIRED_FINAL_VALIDATION_RESIDUAL, rel=1e-12)
    assert val["bellman_residual"] != pytest.approx(
        PRE_REPAIR_FINAL_RESIDUAL_STALE, rel=1e-3)
    assert val["min_boundary_pb"] == pytest.approx(
        4.8089461301970005e-09, rel=1e-12)
    assert val["artificial_bindings"] == 0
    assert val["expansions"] == 0


# ---------------------------------------------------------------------------
# 3. Iteration and final residuals stored/separated, never conflated
# ---------------------------------------------------------------------------
def test_iteration_and_final_residuals_separated_and_reproduced(diag):
    result, _ = diag
    # iteration operator scale (~10.43, the accepted raw direction norm) --
    # UNCHANGED by the repair
    assert result.r_iter_inf == pytest.approx(REPAIRED_R_ITER_INF, rel=1e-9)
    assert result.r_iter_inf < 11.0
    # PRE-REPAIR the final-validation residual was 490.7560425919994; after the
    # Issue #67 repair the two semantics AGREE to machine precision.
    assert result.r_final_inf == pytest.approx(REPAIRED_R_FINAL_INF, rel=1e-12)
    assert result.r_final_inf == pytest.approx(result.r_iter_inf,
                                               abs=REPAIRED_FINAL_VS_ITER_TOL)
    assert (result.r_final_inf
            != pytest.approx(PRE_REPAIR_FINAL_RESIDUAL_STALE, rel=1e-3))
    # they remain DISTINCT objects with distinct definitions, even though the
    # values now coincide numerically; the difference is machine precision only
    assert result.r_diff_inf == pytest.approx(REPAIRED_R_DIFF_INF, abs=1e-15)
    assert result.r_diff_inf <= REPAIRED_FINAL_VS_ITER_TOL
    assert result.r_diff_inf < result.r_iter_inf
    assert result.r_diff_argmax is not None
    assert result.r_diff_argmax["family"] == "F0"


# ---------------------------------------------------------------------------
# 4. F0-vs-boundary residual decomposition is deterministic and meaningful
# ---------------------------------------------------------------------------
def test_f0_boundary_decomposition_consistent_and_deterministic(diag):
    result, identical = diag
    # boundary rows are built identically under iteration and final-validation
    # semantics: the R_final - R_iter difference is EXACTLY 0 on boundary rows
    assert result.r_diff_boundary_max == 0.0
    assert result.r_iter_boundary_max == result.r_final_boundary_max
    assert result.r_iter_boundary_max > 0.0
    # PRE-REPAIR the 490.756 gap lived entirely in F0 rows; after the Issue #67
    # repair the residual remains F0-dominated but only at machine precision
    assert result.r_final_f0_max == pytest.approx(REPAIRED_R_FINAL_F0_MAX, rel=1e-12)
    assert result.r_final_f0_max == pytest.approx(result.r_final_inf, rel=1e-12)
    assert (result.r_final_f0_max
            != pytest.approx(PRE_REPAIR_FINAL_RESIDUAL_STALE, rel=1e-3))
    assert result.r_final_boundary_max < 11.0
    assert result.r_iter_f0_max == pytest.approx(
        result.r_iter_inf, rel=1e-12)
    # decomposition is deterministic (repeat identical includes all stats)
    assert identical is True


def test_no_hjb_convergence_claimed_after_repair(diag):
    """Corrected final == R_iter is an OPERATOR statement, not convergence.

    The corrected residual still exceeds the UNCHANGED Bellman tolerance by
    four orders of magnitude, so validated HJB convergence remains FALSE.
    """
    result, _ = diag
    assert result.final_validation_residual == pytest.approx(
        REPAIRED_FINAL_VALIDATION_RESIDUAL, rel=1e-12)
    assert result.r_iter_inf == pytest.approx(REPAIRED_R_ITER_INF, rel=1e-12)
    assert result.r_iter_inf > BELLMAN_TOLERANCE_UNCHANGED
    assert result.final_validation_residual > BELLMAN_TOLERANCE_UNCHANGED
    assert result.r_iter_inf / BELLMAN_TOLERANCE_UNCHANGED > 1.0e4
    # validated HJB convergence = FALSE under the accepted tolerance
    assert not (result.final_validation_residual <= BELLMAN_TOLERANCE_UNCHANGED)
    assert not (result.r_iter_inf <= BELLMAN_TOLERANCE_UNCHANGED)


def test_residual_stats_layout_is_z_major_node_fastest():
    # mask sanity: row = z*n + node (state layout of the accepted solver)
    solver = BoundaryHJBSolver(g.CENTRAL_CONFIG)
    n, nz = solver.n, solver.nz
    fam = np.array([str(solver.grid.families[node]) for node in range(n)])
    f0_mask = np.tile(fam == "F0", nz)
    assert f0_mask.shape == (n * nz,)
    # spot check: family of row z*n+node matches families[node]
    node = 97
    for z in range(nz):
        assert fam[node] == "F0"  # accepted argmax node is F0
    assert f0_mask[0 * n + node] and f0_mask[1 * n + node]


# ---------------------------------------------------------------------------
# 5. Q_iter,u_iter built exactly once for the frozen Newton diagnostic
# ---------------------------------------------------------------------------
def test_q_iter_u_iter_built_exactly_once_and_reused():
    rec = reconstruct_issue63_stagnation_state()
    solver, V_star, labor0, records_pre = (
        rec["solver"], rec["V_star"], rec["labor0"], rec["records_pre_step8"])
    rho = rec["rho"]
    counter = {"builds": 0}
    orig = solver.build_operator_and_u

    def counting(*args, **kwargs):
        counter["builds"] += 1
        return orig(*args, **kwargs)

    solver.build_operator_and_u = counting
    dec = residual_decomposition(solver, V_star, labor0, records_pre, rho)
    assert counter["builds"] == 2          # Q_iter once + Q_final once
    # the whole Newton diagnostic + one trial reuse the frozen (Q_iter,u_iter):
    # no further operator build during the solve / crossing / trial
    newt = frozen_policy_newton_direction(
        solver, dec["Q_iter"], dec["u_iter"], V_star, dec["R_iter"], rho)
    bd = boundary_crossing(solver, V_star, labor0, newt["dN"])
    assert counter["builds"] == 2
    evaluate_trial(solver, labor0, rho, V_star, newt["dN"], dec["R_iter"],
                   dec["R_final"], dec["Q_iter"], dec["u_iter"],
                   dec["records_iter"], bd["alpha_half"], "alpha_half")
    # one final=False re-selection + one final=True validation-style build
    assert counter["builds"] == 4


# ---------------------------------------------------------------------------
# 6. J_iter d_N = -R_iter within declared linear-solve tolerance
# ---------------------------------------------------------------------------
def test_newton_linear_residual_within_declared_tolerance(diag):
    result, _ = diag
    assert result.lin_res_ok is True
    assert result.lin_res_max_abs <= NEWTON_SOLVE_TOL
    assert result.dN_max_abs > 0.0
    assert np.isfinite(result.dN_max_abs)


# ---------------------------------------------------------------------------
# 7. Accepted boundary directional semantics (exact zero at i==0)
# ---------------------------------------------------------------------------
def test_boundary_semantics_exact_zero_at_vindependent_i0(diag):
    result, _ = diag
    assert result.dpb_required_count == 186      # accepted required boundary states
    assert result.dpb_zero_count == 40           # accepted i==0 V-independent count
    assert result.dpb_negative_count > 0


def test_boundary_direction_matrix_exact_zero_on_i0():
    # direct pin of the accepted Issue #62 semantics: i == 0 rows are exactly 0
    solver = BoundaryHJBSolver(g.CENTRAL_CONFIG)
    g_ = solver.grid
    dV = np.ones((solver.n, solver.nz), dtype=float)
    dp = boundary_direction_matrix(solver, dV)
    for node in range(solver.n):
        j, i = int(g_.j_arr[node]), int(g_.i_arr[node])
        if i == 0:
            assert np.all(dp[node, :] == 0.0)
    # regular backward finite difference of dV
    node1 = g_.node_of[(1, 1)]
    node0 = g_.node_of[(1, 0)]
    assert dp[node1, 0] == pytest.approx((dV[node1, 0] - dV[node0, 0]) / solver.db)


# ---------------------------------------------------------------------------
# 8. Deterministic alpha_cross / alpha_half / alpha_near
# ---------------------------------------------------------------------------
def test_alpha_fractions_deterministic_and_consistent(diag):
    result, _ = diag
    assert result.alpha_cross is not None and result.alpha_cross > 0.0
    assert np.isfinite(result.alpha_cross)
    assert result.alpha_near == pytest.approx(
        min(1.0, (1.0 - EPS_ALPHA) * result.alpha_cross), rel=1e-12)
    assert result.alpha_half == pytest.approx(
        HALF_ALPHA * result.alpha_near, rel=1e-12)
    # limiting boundary state for the Newton direction = same wall state
    assert result.alpha_cross_state is not None
    assert result.alpha_cross_state["node"] == 332
    assert result.alpha_cross_state["family"] == "F3"
    assert result.alpha_cross_state["j"] == 13
    assert result.alpha_cross_state["i"] == 13
    assert result.alpha_cross_state["z"] == 1


# ---------------------------------------------------------------------------
# 9. Both trial states strictly inside PB_MARGIN, frozen scaling, one
#    re-selection, trial-final semantics use the trial re-selected records
# ---------------------------------------------------------------------------
def test_both_trials_domain_safe_and_frozen_scaling(diag):
    result, _ = diag
    assert len(result.trials) == 2
    names = {t["name"] for t in result.trials}
    assert names == {"alpha_half", "alpha_near"}
    for t in result.trials:
        assert t["domain_safe"] is True
        assert t["trial_min_pb"] > PB_MARGIN
        assert np.isfinite(t["trial_min_pb"])
        # frozen residual scales as (1-alpha) within the declared tolerance
        assert t["frozen_dev_max_abs"] <= SCALING_CHECK_TOL
        expected = (1.0 - t["alpha"]) * result.r_iter_inf
        assert t["r_reselect_inf"] > 0.0
    assert result.trials[0]["alpha"] == result.alpha_half
    assert result.trials[1]["alpha"] == result.alpha_near


def test_trial_exactly_one_reselection_and_uses_trial_records_for_final():
    rec = reconstruct_issue63_stagnation_state()
    solver, V_star, labor0, records_pre = (
        rec["solver"], rec["V_star"], rec["labor0"], rec["records_pre_step8"])
    rho = rec["rho"]
    dec = residual_decomposition(solver, V_star, labor0, records_pre, rho)
    newt = frozen_policy_newton_direction(
        solver, dec["Q_iter"], dec["u_iter"], V_star, dec["R_iter"], rho)
    bd = boundary_crossing(solver, V_star, labor0, newt["dN"])
    calls = []
    orig = solver.build_operator_and_u

    def spy(*args, **kwargs):
        calls.append(kwargs)
        return orig(*args, **kwargs)

    solver.build_operator_and_u = spy
    trial = evaluate_trial(solver, labor0, rho, V_star, newt["dN"],
                           dec["R_iter"], dec["R_final"], dec["Q_iter"],
                           dec["u_iter"], dec["records_iter"],
                           bd["alpha_near"], "alpha_near")
    # exactly one final=False re-selection + one final=True build per trial
    assert len(calls) == 2
    assert calls[0]["final"] is False
    assert calls[1]["final"] is True
    # the final=True call receives the TRIAL re-selected records (same object),
    # not the stale baseline records
    assert calls[1]["f0_policies"] is trial["records_trial"]
    assert calls[1]["f0_policies"] is not dec["records_iter"]
    # trial final residual is computed, finite, and ratio recorded
    assert trial["r_final_trial_inf"] > 0.0
    assert np.isfinite(trial["ratio_final"])
    assert trial["ratio_iter"] > 0.0


# ---------------------------------------------------------------------------
# 10. Non-finite evidence fails closed
# ---------------------------------------------------------------------------
class _FakeSolver:
    def __init__(self, nan_vb=False):
        n, nz = 3, 1
        self.n, self.nz, self.state_size = n, nz, n * nz
        self.db = 1.0
        self.grid = types.SimpleNamespace(
            families=["F1", "F1", "F1"],
            j_arr=np.zeros(n, dtype=int),
            i_arr=np.arange(n, dtype=int),
            node_of={(0, 0): 0, (0, 1): 1, (0, 2): 2},
        )
        self.config = types.SimpleNamespace(
            params=types.SimpleNamespace(rho=0.02),
            row_sum_tolerance=1e-9)
        self._nan = nan_vb

    def compute_derivatives(self, V, labor0, ti, gap):
        V = np.asarray(V, float).reshape(self.n, self.nz)
        out = np.full(V.shape, np.nan) if self._nan else V.copy()
        return (np.zeros_like(V), out, np.zeros_like(V), np.zeros_like(V))


def test_nonfinite_boundary_evidence_fails_closed():
    solver = _FakeSolver(nan_vb=True)
    V_star = np.full((solver.n, solver.nz), 0.01)
    labor0 = np.zeros_like(V_star)
    dN = np.ones(solver.state_size)
    with pytest.raises(NewtonGeometryFailure):
        boundary_crossing(solver, V_star, labor0, dN)


def test_nonfinite_direction_evidence_fails_closed():
    solver = _FakeSolver()
    V_star = np.full((solver.n, solver.nz), 0.01)
    dV = np.full((solver.n, solver.nz), np.nan)
    with pytest.raises(LocalGeometryFailure):
        boundary_direction_matrix(solver, dV)


def test_reconstruction_failure_surfaces_terminal_c(monkeypatch):
    from deep_learning_hank.two_asset.continuous_ftb_resolvent_hjb import (
        FTBStepConstructionFailure,
    )

    def failing_step(*args, **kwargs):
        raise FTBStepConstructionFailure("synthetic fail-closed probe")

    monkeypatch.setattr(g, "construct_ftb_step", failing_step)
    r = g.run_issue64_diagnostic()
    assert r.outcome == TERMINAL_C
    assert r.failure_detail is not None


# ---------------------------------------------------------------------------
# 11. Exactly one terminal, deterministic repeat, no forbidden machinery
# ---------------------------------------------------------------------------
def test_exactly_one_terminal_returned(diag):
    result, _ = diag
    assert result.outcome in (TERMINAL_A, TERMINAL_B, TERMINAL_C)


def test_deterministic_full_repeat(diag):
    result, identical = diag
    assert identical is True
    assert result.deterministic_repeat_identical is True


def _module_ast():
    return ast.parse(inspect.getsource(g))


def test_static_integrity_no_forbidden_machinery():
    tree = _module_ast()
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            names.add(node.id)
        if isinstance(node, ast.Attribute):
            names.add(node.attr)
    low = {n.lower() for n in names}
    # no value damping / line search / adaptive alpha tuning
    assert not any("damp" in n for n in low)
    assert not any("linesearch" in n for n in low)
    assert not any("armijo" in n for n in low)
    # no p_b clip / floor / max-min replacement
    for banned in ("clip", "floor", "maximum", "minimum"):
        assert banned not in low, banned
    # no KFE / stationary / steady-state machinery
    for banned in ("kfe", "stationary", "steady_state",
                   "solve_household_steady_state"):
        assert banned not in low, banned
    # no multi-step Newton / policy-iteration / semismooth / trust-region /
    # resolvent-ladder machinery
    for banned in ("trust_region", "semismooth", "policy_iteration",
                   "delta_ladder", "select_largest_feasible_delta",
                   "run_adaptive_resolvent_central"):
        assert banned not in low, banned
    # exactly TWO trial fractions are evaluated in the run loop: the two
    # evaluate_trial calls appear exactly twice
    call_names = [n.func.id for n in ast.walk(tree)
                  if isinstance(n, ast.Call)
                  and isinstance(n.func, ast.Name)]
    assert call_names.count("evaluate_trial") == 2
    # no accepted-iterate acceptance: the module never writes V_star back as a
    # new iterate (no loop that reuses V_star as the next iterate)
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name in ("run_issue64_diagnostic",
                             "reconstruct_issue63_stagnation_state"):
                fnames = {n.id.lower() for n in ast.walk(node)
                          if isinstance(n, ast.Name)}
                assert "select_largest_feasible_delta" not in fnames
