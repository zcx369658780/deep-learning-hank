"""DLH-5V-N tests: local continuous resolvent / domain-margin geometry.

Pins the Issue #62 contract: frozen config, accepted Issue #61 terminal-state
reconstruction, frozen (V_*, Q_*, u_*) built once and reused, scaled/original
resolvent agreement, infinitesimal direction + finite-difference check,
fail-closed non-finite evidence, g(0)>0 / g(floor)<0 reproduction, bracketed
deterministic root inside the fixed bracket, below/above-root verification,
no policy re-selection across root evaluations, no accepted next iterate /
continuation loop, no KFE / stationary KFE / steady state, margin
acceptance-only, deterministic repeat, and the exact one-terminal decision.
"""

import ast
import types

import numpy as np
import pytest
from scipy import sparse

from deep_learning_hank.two_asset.local_resolvent_domain_geometry import (
    BRENTQ_RTOL,
    BRENTQ_XTOL,
    DELTA_FLOOR,
    EPS_VERIFY,
    RECONSTRUCT_ITERATIONS,
    LocalGeometryFailure,
    LocalGeometryResult,
    boundary_direction_diagnostic,
    continuous_crossing_diagnostic,
    finalize_outcome,
    g_delta,
    infinitesimal_direction,
    reconstruct_issue61_terminal_state,
    run_local_geometry_diagnostic,
    run_local_geometry_diagnostic_twice,
    solve_original_resolvent,
    solve_scaled_resolvent,
)
from deep_learning_hank.two_asset.adaptive_resolvent_hjb import (
    CENTRAL_CONFIG,
    CENTRAL_INPUTS,
    CENTRAL_PARAMS,
    CENTRAL_SWITCH,
    CENTRAL_Z,
    DELTA_MIN_EXP,
    DELTA_REF,
    PB_MARGIN,
)

# accepted Issue #61 evidence (frozen references — do NOT reopen)
ACCEPTED_MIN_ACCEPTED_PB = 0.009853744163134845
ACCEPTED_TERMINAL_NODE = 332          # F3 (13,13), z=1
ACCEPTED_TERMINAL_FAMILY = "F3"
ACCEPTED_TERMINAL_J = 13
ACCEPTED_TERMINAL_I = 13
ACCEPTED_TERMINAL_Z = 1
ACCEPTED_V0_MIN_PB = 0.48076562156308306
ACCEPTED_G_HI_MIN_PB = -0.002078969753188379   # smallest authorized-delta trial p_b


# ---------------------------------------------------------------------------
# Small linear fake solver (p_b = V elementwise; all states required)
# ---------------------------------------------------------------------------
class _FakeSolver:
    """3-node line: (j=0, i=0/1/2). p_b = V elementwise; db = 1.0."""

    def __init__(self, n=3, nz=1):
        self.n, self.nz, self.state_size = n, nz, n * nz
        self.db = 1.0
        self.grid = types.SimpleNamespace(
            families=["F1"] * n,
            j_arr=np.zeros(n, dtype=int),
            i_arr=np.arange(n, dtype=int),
            node_of={(0, 0): 0, (0, 1): 1, (0, 2): 2},
        )
        self.config = types.SimpleNamespace(
            params=types.SimpleNamespace(rho=0.02),
            row_sum_tolerance=1e-9)

    def compute_derivatives(self, V, labor0, ti, gap):
        V = np.asarray(V, float).reshape(self.n, self.nz)
        return (np.zeros_like(V), V.copy(), np.zeros_like(V), np.zeros_like(V))


def _synthetic_case():
    """Q = 0, u = [0, -11, 0], V_star = 0.01 everywhere. The b_min-face node 0
    (i=0) is V-independent (dp = 0); node 1 (i=1) value
    V1(delta) = (0.01 - 11*delta)/(1 + 0.02*delta) crosses the margin inside
    [0, DELTA_FLOOR] (root ~9.09e-4, i.e. ~95% of the floor)."""
    n, nz = 3, 1
    rho = 0.02
    solver = _FakeSolver(n, nz)
    V_star = np.full((n, nz), 0.01)
    u = np.zeros((n, nz))
    u[1, 0] = -11.0
    Q = sparse.csr_matrix((n, n))
    return solver, Q, u, V_star, rho


# ---------------------------------------------------------------------------
# 1. Frozen central configuration exact
# ---------------------------------------------------------------------------
def test_frozen_central_configuration_exact():
    assert CENTRAL_PARAMS.rho == 0.02
    assert CENTRAL_PARAMS.gamma_c == 2.0
    assert CENTRAL_PARAMS.phi == 5.0
    assert CENTRAL_PARAMS.chi_0 == 0.1
    assert CENTRAL_PARAMS.chi_1 == 2.0
    assert CENTRAL_PARAMS.a_bar == 1e-6
    assert CENTRAL_INPUTS.r_a == 0.07
    assert CENTRAL_INPUTS.r_b == 0.02
    assert CENTRAL_INPUTS.tau == 0.15
    assert CENTRAL_INPUTS.wages[0] == 1.0
    assert CENTRAL_INPUTS.migration_costs[0] == 0.0
    assert CENTRAL_INPUTS.labor_weights[0] == 1.0
    assert np.allclose(CENTRAL_Z, [0.8, 1.3])
    assert CENTRAL_CONFIG.m == 1 and CENTRAL_CONFIG.w_max == 10.0
    assert CENTRAL_CONFIG.b_min == -2.0 and CENTRAL_CONFIG.a_max == 10.0
    assert CENTRAL_CONFIG.delta == 1000.0
    assert CENTRAL_CONFIG.tolerance_iter == 1e-7
    assert CENTRAL_CONFIG.tolerance_bellman == 1e-3
    assert CENTRAL_CONFIG.max_iterations == 1000
    assert CENTRAL_CONFIG.n_c_grid == 9 and CENTRAL_CONFIG.n_d_grid == 9
    assert PB_MARGIN == 1e-12
    assert DELTA_REF == 1000.0 and DELTA_MIN_EXP == 20
    assert DELTA_FLOOR == pytest.approx(1000.0 * 2.0 ** (-20))


# ---------------------------------------------------------------------------
# 2/3. Terminal-state reconstruction reproduces the accepted Issue #61 trace
# ---------------------------------------------------------------------------
def test_reconstruction_reproduces_accepted_issue61_trace():
    rec = reconstruct_issue61_terminal_state()
    trace = rec["trace"]
    assert len(trace) == RECONSTRUCT_ITERATIONS == 2
    t1, t2 = trace[0], trace[1]
    # iteration 1: k=15, delta=1000*2^-15
    assert t1["iteration"] == 1 and t1["delta_index"] == 15
    assert t1["selected_delta"] == pytest.approx(1000.0 * 2.0 ** (-15), rel=1e-12)
    assert t1["accepted_max_stat"] == pytest.approx(0.319783912291, rel=1e-4)
    assert t1["ref1000_max_stat"] == pytest.approx(19.5762533642, rel=1e-4)
    assert t1["ref1000_min_pb"] == pytest.approx(-0.682001580079, rel=1e-4)
    assert t1["min_pb_old"] == pytest.approx(ACCEPTED_V0_MIN_PB, rel=1e-9)
    assert t1["min_pb_new"] == pytest.approx(0.0602545352311, rel=1e-4)
    assert t1["delta1000_would_violate"] is True
    assert t1["max_abs_q1"] < 1e-12
    assert t1["expansions"] == 0 and t1["artificial_bindings"] == 0
    assert t1["sector_changes"] == 0
    # iteration 2: k=18, delta=1000*2^-18
    assert t2["iteration"] == 2 and t2["delta_index"] == 18
    assert t2["selected_delta"] == pytest.approx(1000.0 * 2.0 ** (-18), rel=1e-12)
    assert t2["accepted_max_stat"] == pytest.approx(0.039855624229, rel=1e-4)
    assert t2["ref1000_max_stat"] == pytest.approx(19.1615653124, rel=1e-4)
    assert t2["ref1000_min_pb"] == pytest.approx(-0.731193069681, rel=1e-4)
    assert t2["min_pb_old"] == pytest.approx(0.0602545352311, rel=1e-4)
    assert t2["min_pb_new"] == pytest.approx(ACCEPTED_MIN_ACCEPTED_PB, rel=1e-9)
    assert t2["delta1000_would_violate"] is True
    assert t2["max_abs_q1"] < 1e-12
    assert t2["expansions"] == 0 and t2["artificial_bindings"] == 0
    assert t2["sector_changes"] == 7
    assert rec["v0_min_boundary_pb"] == pytest.approx(ACCEPTED_V0_MIN_PB, rel=1e-9)
    assert rec["min_accepted_boundary_pb"] == pytest.approx(
        ACCEPTED_MIN_ACCEPTED_PB, rel=1e-9)


def test_full_diagnostic_reproduces_terminal_state_and_evidence():
    r, _ = run_local_geometry_diagnostic_twice()
    assert r.iterations == 2
    assert r.terminal_min_boundary_pb == pytest.approx(
        ACCEPTED_MIN_ACCEPTED_PB, rel=1e-9)
    assert r.terminal_state["node"] == ACCEPTED_TERMINAL_NODE
    assert r.terminal_state["family"] == ACCEPTED_TERMINAL_FAMILY
    assert r.terminal_state["j"] == ACCEPTED_TERMINAL_J
    assert r.terminal_state["i"] == ACCEPTED_TERMINAL_I
    assert r.terminal_state["z"] == ACCEPTED_TERMINAL_Z
    assert r.g0 == pytest.approx(ACCEPTED_MIN_ACCEPTED_PB - PB_MARGIN, rel=1e-9)
    assert r.g_hi == pytest.approx(ACCEPTED_G_HI_MIN_PB - PB_MARGIN, rel=1e-6)


# ---------------------------------------------------------------------------
# 4. Frozen (Q_*, u_*) built exactly once and reused for every delta evaluation
# ---------------------------------------------------------------------------
def test_operator_built_once_and_reused_across_delta_evaluations(monkeypatch):
    import deep_learning_hank.two_asset.boundary_hjb_selected_q as bq
    counter = {"n": 0}
    original = bq.BoundaryHJBSolver.build_operator_and_u

    def counting(self, *args, **kwargs):
        counter["n"] += 1
        return original(self, *args, **kwargs)

    monkeypatch.setattr(bq.BoundaryHJBSolver, "build_operator_and_u", counting)

    rec = reconstruct_issue61_terminal_state()
    assert counter["n"] == RECONSTRUCT_ITERATIONS  # 2 builds (reconstruction only)
    solver, labor0, V_star = rec["solver"], rec["labor0"], rec["V_star"]
    Q, u, _, _ = solver.build_operator_and_u(V_star, labor0, 0.0, 0.0, final=False)
    assert counter["n"] == RECONSTRUCT_ITERATIONS + 1  # exactly ONE frozen build
    n_before_crossing = counter["n"]
    rho = float(solver.config.params.rho)
    _ = continuous_crossing_diagnostic(solver, Q, u, V_star, labor0, rho)
    assert counter["n"] == n_before_crossing  # NO rebuild during root evaluations


# ---------------------------------------------------------------------------
# 5/6. Scaled resolvent: V(0) = V_*; agreement with the original form
# ---------------------------------------------------------------------------
def test_scaled_resolvent_at_zero_returns_v_star():
    rec = reconstruct_issue61_terminal_state()
    solver, labor0, V_star = rec["solver"], rec["labor0"], rec["V_star"]
    Q, u, _, _ = solver.build_operator_and_u(V_star, labor0, 0.0, 0.0, final=False)
    rho = float(solver.config.params.rho)
    V0 = solve_scaled_resolvent(Q, u, V_star, 0.0, rho)
    assert np.max(np.abs(V0 - V_star)) < 1e-12


def test_scaled_and_original_resolvent_agree_at_positive_deltas():
    rec = reconstruct_issue61_terminal_state()
    solver, labor0, V_star = rec["solver"], rec["labor0"], rec["V_star"]
    Q, u, _, _ = solver.build_operator_and_u(V_star, labor0, 0.0, 0.0, final=False)
    rho = float(solver.config.params.rho)
    for delta in (1e-4, DELTA_FLOOR / 2.0, DELTA_FLOOR):
        Vs = solve_scaled_resolvent(Q, u, V_star, delta, rho)
        Vo = solve_original_resolvent(Q, u, V_star, delta, rho)
        assert np.max(np.abs(Vs - Vo)) < 1e-10


# ---------------------------------------------------------------------------
# 7. Infinitesimal direction formula + finite-difference check
# ---------------------------------------------------------------------------
def test_infinitesimal_direction_formula_and_finite_difference():
    rec = reconstruct_issue61_terminal_state()
    solver, labor0, V_star = rec["solver"], rec["labor0"], rec["V_star"]
    Q, u, _, _ = solver.build_operator_and_u(V_star, labor0, 0.0, 0.0, final=False)
    rho = float(solver.config.params.rho)
    dV = infinitesimal_direction(Q, u, V_star, rho)
    flat = V_star.ravel(order="F")
    expected = (np.asarray(u, dtype=float) + Q.dot(flat)
                - rho * flat).reshape(V_star.shape, order="F")
    assert np.max(np.abs(dV - expected)) < 1e-14
    h = 1e-6
    Vh = solve_scaled_resolvent(Q, u, V_star, h, rho)
    fd = (Vh - V_star) / h
    denom = np.max(np.abs(dV))
    assert np.max(np.abs(fd - dV)) < 1e-4 * max(denom, 1.0)


# ---------------------------------------------------------------------------
# 8. Fail-closed non-finite boundary / directional evidence
# ---------------------------------------------------------------------------
class _AlwaysNaNSolver(_FakeSolver):
    def compute_derivatives(self, V, labor0, ti, gap):
        V = np.asarray(V, float).reshape(self.n, self.nz)
        out = np.full(V.shape, np.nan)
        return (np.zeros_like(V), out, np.zeros_like(V), np.zeros_like(V))


def test_nonfinite_directional_evidence_fails_closed():
    solver = _FakeSolver()
    V_star = np.full((solver.n, solver.nz), 0.01)
    dV = np.full((solver.n, solver.nz), -0.5)
    dV[1, 0] = np.nan          # node 1 (i=1): backward difference of dV -> NaN
    with pytest.raises(LocalGeometryFailure):
        boundary_direction_diagnostic(solver, V_star, np.zeros_like(V_star), dV)


def test_nonfinite_boundary_pb_evidence_fails_closed_in_g():
    # R1: non-finite required boundary p_b must RAISE in g_delta — never be
    # returned as +inf (which would be misread as g > 0, i.e. feasible).
    solver = _AlwaysNaNSolver()
    _, Q, u, V_star, rho = _synthetic_case()
    with pytest.raises(LocalGeometryFailure):
        g_delta(solver, Q, u, V_star, np.zeros_like(V_star), rho, 1e-4)


def test_nonfinite_crossing_evidence_rejected_not_feasible():
    # R1 regression: a non-finite trial in the crossing path must be explicitly
    # rejected — it can never be classified as below-root feasible / Outcome A.
    solver = _AlwaysNaNSolver()
    _, Q, u, V_star, rho = _synthetic_case()
    labor0 = np.zeros_like(V_star)
    with pytest.raises(LocalGeometryFailure):
        continuous_crossing_diagnostic(solver, Q, u, V_star, labor0, rho)


# ---------------------------------------------------------------------------
# R1 fix 1: real b=b_min face directional derivative is exactly zero
# (accepted V-independent boundary rule), while the regular finite-difference
# path is unchanged.
# ---------------------------------------------------------------------------
def test_real_bmin_face_pb_is_v_independent_and_dp_is_zero():
    from deep_learning_hank.two_asset.local_resolvent_domain_geometry import (
        boundary_direction_matrix,
    )
    from deep_learning_hank.two_asset.adaptive_resolvent_hjb import (
        CENTRAL_CONFIG,
    )
    from deep_learning_hank.two_asset.boundary_hjb_selected_q import (
        BoundaryHJBSolver,
    )
    solver = BoundaryHJBSolver(CENTRAL_CONFIG)
    labor0 = solver.build_labor0(0.0, 0.0)
    V_star = solver.build_initial_value(labor0, 0.0, 0.0)
    # find a required (non-F0) b_min-face state (i == 0)
    bmin_nodes = [node for node in range(solver.n)
                  if solver.grid.families[node] != "F0"
                  and int(solver.grid.i_arr[node]) == 0]
    assert len(bmin_nodes) > 0
    node = bmin_nodes[0]
    pb_ref = solver.compute_derivatives(V_star, labor0, 0.0, 0.0)[1]
    # 1) p_b on the b_min face is V-independent: a perturbation changes it not
    perturb = np.zeros_like(V_star)
    perturb[:] = 0.5
    pb_pert = solver.compute_derivatives(V_star + perturb, labor0, 0.0, 0.0)[1]
    for nz in range(solver.nz):
        assert float(pb_ref[node, nz]) == float(pb_pert[node, nz])  # exact
    # 2) the corrected directional matrix gives exactly 0 there
    dV = np.full_like(V_star, -1.0)
    dp = boundary_direction_matrix(solver, dV)
    for nz in range(solver.nz):
        assert float(dp[node, nz]) == 0.0                      # exact zero
    # 3) regular (non i==0) backward finite-difference path unchanged: equals
    #    compute_derivatives(dV).vb_b at a non-b_min required state
    g = solver.grid
    reg = [nd for nd in range(solver.n)
           if g.families[nd] != "F0" and int(g.i_arr[nd]) > 0][0]
    j, i = int(g.j_arr[reg]), int(g.i_arr[reg])
    down = g.node_of.get((j, i - 1))
    assert down is not None
    vb_b_dir = solver.compute_derivatives(dV, labor0, 0.0, 0.0)[1]
    for nz in range(solver.nz):
        manual = float((dV[reg, nz] - dV[down, nz]) / solver.db)
        assert manual == pytest.approx(float(vb_b_dir[reg, nz]), abs=1e-15)


def test_direction_diagnostic_zero_count_matches_v_independent_states():
    from deep_learning_hank.two_asset.adaptive_resolvent_hjb import (
        CENTRAL_CONFIG,
    )
    from deep_learning_hank.two_asset.boundary_hjb_selected_q import (
        BoundaryHJBSolver,
    )
    solver = BoundaryHJBSolver(CENTRAL_CONFIG)
    labor0 = solver.build_labor0(0.0, 0.0)
    V_star = solver.build_initial_value(labor0, 0.0, 0.0)
    required_bmin = sum(
        1 for nd in range(solver.n)
        if solver.grid.families[nd] != "F0" and int(solver.grid.i_arr[nd]) == 0)
    assert required_bmin > 0
    # non-constant dV so regular states have non-zero backward differences
    bd = boundary_direction_diagnostic(
        solver, V_star, labor0, V_star.copy())
    assert bd["dpb_zero_count"] >= required_bmin
    assert bd["dpb_required_count"] > bd["dpb_zero_count"]


# ---------------------------------------------------------------------------
# 9/10/11. Bracketed continuous root: g(0)>0, g(floor)<0, root inside,
# below-root feasible / above-root infeasible, deterministic
# ---------------------------------------------------------------------------
def test_g0_positive_and_gfloor_negative_reproduce_accepted_evidence():
    rec = reconstruct_issue61_terminal_state()
    solver, labor0, V_star = rec["solver"], rec["labor0"], rec["V_star"]
    Q, u, _, _ = solver.build_operator_and_u(V_star, labor0, 0.0, 0.0, final=False)
    rho = float(solver.config.params.rho)
    g0 = g_delta(solver, Q, u, V_star, labor0, rho, 0.0)
    g_hi = g_delta(solver, Q, u, V_star, labor0, rho, DELTA_FLOOR)
    assert g0 > 0.0 and g0 == pytest.approx(ACCEPTED_MIN_ACCEPTED_PB - PB_MARGIN,
                                            rel=1e-9)
    assert g_hi < 0.0 and g_hi == pytest.approx(ACCEPTED_G_HI_MIN_PB - PB_MARGIN,
                                                rel=1e-6)


def test_synthetic_crossing_root_inside_bracket_and_verification():
    solver, Q, u, V_star, rho = _synthetic_case()
    labor0 = np.zeros_like(V_star)
    cr = continuous_crossing_diagnostic(solver, Q, u, V_star, labor0, rho)
    assert cr["g0"] > 0.0 and cr["g_hi"] < 0.0
    root = cr["delta_cross"]
    assert cr["bracket_lo"] < root < cr["bracket_hi"]
    assert abs(cr["g_cross"]) < 1e-9
    # analytic root of (0.01 - 11*delta)/(1 + 0.02*delta) = 1e-12 at node 1
    analytic = (0.01 - 1e-12 * (1.0 + 2e-14)) / 11.0
    assert root == pytest.approx(analytic, rel=1e-4)
    assert cr["below_delta"] == pytest.approx((1.0 - EPS_VERIFY) * root, rel=1e-12)
    assert cr["above_delta"] == pytest.approx((1.0 + EPS_VERIFY) * root, rel=1e-12)
    assert cr["below_g"] > 0.0 and cr["above_g"] < 0.0
    # crossing state is node 1 (i=1); the b_min-face node 0 stays V-independent
    assert cr["below_state"]["node"] == 1 and cr["above_state"]["node"] == 1
    assert cr["cross_worst_state"]["node"] == 1
    # boundary direction: node 0 (i=0) has exactly zero directional derivative;
    # node 1 has the steepest negative dp and the min first-order prediction
    dV = infinitesimal_direction(Q, u, V_star, rho)
    bd = boundary_direction_diagnostic(solver, V_star, labor0, dV)
    assert bd["dpb_zero_count"] >= 1           # the V-independent b_min state
    assert bd["dpb_most_negative_state"]["node"] == 1
    assert bd["min_delta_margin_linear_state"]["node"] == 1
    assert bd["min_delta_margin_linear"] == pytest.approx(analytic, rel=1e-4)


def test_real_crossing_root_deterministic_and_subfloor():
    r1 = run_local_geometry_diagnostic()
    r2 = run_local_geometry_diagnostic()
    assert r1.delta_cross == r2.delta_cross
    assert r1.bracket_lo == 0.0 and r1.bracket_hi == DELTA_FLOOR
    assert 0.0 < r1.delta_cross < DELTA_FLOOR
    assert r1.g0 > 0.0 and r1.g_hi < 0.0
    assert abs(r1.g_cross) < 1e-9
    assert r1.below_g > 0.0 and r1.above_g < 0.0          # feasible/infeasible
    assert r1.below_min_pb > PB_MARGIN
    assert r1.above_min_pb < PB_MARGIN
    # strictly positive sub-floor delta directly verified feasible:
    assert 0.0 < r1.below_delta < DELTA_FLOOR and r1.below_g > 0.0
    assert r1.delta_cross < DELTA_FLOOR
    assert r1.ratio_cross_over_floor == pytest.approx(
        r1.delta_cross / DELTA_FLOOR, rel=1e-12)
    # worst state at root / below / above = the same wall state F3 (13,13) z=1
    for st in (r1.cross_worst_state, r1.below_state, r1.above_state):
        assert st["node"] == ACCEPTED_TERMINAL_NODE
        assert st["family"] == ACCEPTED_TERMINAL_FAMILY
        assert st["j"] == ACCEPTED_TERMINAL_J and st["i"] == ACCEPTED_TERMINAL_I
        assert st["z"] == ACCEPTED_TERMINAL_Z
    # first-order prediction state == wall state; ratio ~1 (reliable)
    assert r1.min_delta_margin_linear_state["node"] == ACCEPTED_TERMINAL_NODE
    assert 0.0 < r1.min_delta_margin_linear < DELTA_FLOOR
    assert r1.ratio_cross_over_linear == pytest.approx(
        r1.delta_cross / r1.min_delta_margin_linear, rel=1e-9)


# ---------------------------------------------------------------------------
# 12. No policy re-selection across root evaluations (pinned above);
#     direction diagnostic records distinct quantities without overloading
# ---------------------------------------------------------------------------
def test_direction_diagnostic_records_separate_quantities():
    rec = reconstruct_issue61_terminal_state()
    solver, labor0, V_star = rec["solver"], rec["labor0"], rec["V_star"]
    Q, u, _, _ = solver.build_operator_and_u(V_star, labor0, 0.0, 0.0, final=False)
    rho = float(solver.config.params.rho)
    dV = infinitesimal_direction(Q, u, V_star, rho)
    bd = boundary_direction_diagnostic(solver, V_star, labor0, dV)
    assert bd["pb_star"] == pytest.approx(ACCEPTED_MIN_ACCEPTED_PB, rel=1e-9)
    assert bd["terminal_state"]["node"] == ACCEPTED_TERMINAL_NODE
    assert bd["dpb_negative_count"] > 0
    assert bd["dpb_required_count"] > bd["dpb_negative_count"]
    assert bd["dpb_zero_count"] > 0            # V-independent b_min-face states
    assert bd["dpb_most_negative"] < 0.0
    assert bd["min_delta_margin_linear"] > 0.0
    # most-negative slope may be at a different z than the crossing state;
    # the min first-order prediction must be at the wall state
    assert bd["min_delta_margin_linear_state"]["node"] == ACCEPTED_TERMINAL_NODE
    assert bd["delta_margin_linear_count"] == bd["dpb_negative_count"]


# ---------------------------------------------------------------------------
# 13/14. Static integrity: no accepted next iterate / continuation loop,
# no KFE / stationary KFE / steady state, margin acceptance-only
# ---------------------------------------------------------------------------
def _module_src():
    import deep_learning_hank.two_asset.local_resolvent_domain_geometry as mod
    return ast.parse(open(mod.__file__, encoding="utf-8").read())


def test_no_continuation_loop_or_next_iterate():
    tree = _module_src()
    for node in ast.walk(tree):
        assert not isinstance(node, ast.While), "no unbounded iteration loop"
    names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
    for banned in ("run_adaptive_resolvent_central", "ResolventStepFailure",
                   "final_bellman_validation", "continuation", "homotopy"):
        assert banned not in names
    assert RECONSTRUCT_ITERATIONS == 2


def test_no_kfe_or_steady_state():
    tree = _module_src()
    names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
    for banned in ("solve_household_steady_state", "stationary",
                   "kfe", "KFE", "steady_state"):
        assert banned not in names


def test_no_derivative_clipping_or_flooring_and_margin_acceptance_only():
    tree = _module_src()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            fname = (node.func.id if isinstance(node.func, ast.Name) else "")
            assert fname not in ("clip", "maximum", "minimum", "floor")
    src = open(
        ast.parse("").__class__ and
        __import__("deep_learning_hank.two_asset.local_resolvent_domain_geometry",
                   fromlist=["x"]).__file__, encoding="utf-8").read()
    # PB_MARGIN is subtracted in acceptance predicates only; never added to V
    assert "PB_MARGIN" in src
    assert "np.clip" not in src and "np.floor" not in src


# ---------------------------------------------------------------------------
# 15/16. Outcome decision: exactly one terminal; A on the real evidence
# ---------------------------------------------------------------------------
def _result_for_outcome(outcome=None, **overrides) -> LocalGeometryResult:
    base = dict(
        outcome="", iterations=2,
        trace=[
            {"iteration": 1, "delta_index": 15, "selected_delta": 0.0305,
             "min_pb_new": 0.06025},
            {"iteration": 2, "delta_index": 18, "selected_delta": 0.00381,
             "min_pb_new": ACCEPTED_MIN_ACCEPTED_PB},
        ],
        v0_min_boundary_pb=ACCEPTED_V0_MIN_PB,
        min_accepted_boundary_pb=ACCEPTED_MIN_ACCEPTED_PB,
        terminal_min_boundary_pb=ACCEPTED_MIN_ACCEPTED_PB,
        terminal_state={"node": 332, "j": 13, "i": 13, "z": 1, "family": "F3"},
        max_abs_q1=5.9e-15, expansions=0, artificial_bindings=0,
        direction_max_abs=10.4, dpb_most_negative=-22.5,
        dpb_most_negative_state={"node": 332, "j": 13, "i": 13, "z": 0,
                                 "family": "F3"},
        dpb_negative_count=105, dpb_required_count=186, dpb_zero_count=24,
        min_delta_margin_linear=0.000759, min_delta_margin_linear_state={
            "node": 332, "j": 13, "i": 13, "z": 1, "family": "F3"},
        delta_margin_linear_count=105,
        g0=0.00985, g_hi=-0.00208, bracket_lo=0.0, bracket_hi=DELTA_FLOOR,
        delta_cross=7.82e-4, g_cross=-1.6e-14,
        cross_worst_state={"node": 332, "j": 13, "i": 13, "z": 1, "family": "F3"},
        below_delta=7.819e-4, below_g=9.5e-9, below_min_pb=9.5e-9,
        below_state={"node": 332, "j": 13, "i": 13, "z": 1, "family": "F3"},
        above_delta=7.821e-4, above_g=-9.5e-9, above_min_pb=-9.5e-9,
        above_state={"node": 332, "j": 13, "i": 13, "z": 1, "family": "F3"},
        ratio_cross_over_floor=0.82, ratio_cross_over_linear=1.03,
        deterministic_repeat_identical=True,
    )
    base.update(overrides)
    return LocalGeometryResult(**base)


def test_outcome_a_on_clean_subfloor_crossing():
    r = _result_for_outcome()
    assert finalize_outcome(r, True) == (
        "DLH_5VN_LOCAL_RESOLVENT_GEOMETRY__"
        "POSITIVE_SUBFLOOR_SAFE_STEP_AND_REPRODUCIBLE_MARGIN_CROSSING__"
        "CONTINUATION_DESIGN_GATE_READY")


def test_outcome_b_on_state_switching():
    r = _result_for_outcome(cross_worst_state={
        "node": 200, "j": 9, "i": 10, "z": 0, "family": "F3"})
    assert finalize_outcome(r, True) == (
        "DLH_5VN_LOCAL_RESOLVENT_GEOMETRY__"
        "POSITIVE_LOCAL_FEASIBILITY_WITH_STIFF_OR_NONUNIQUE_MARGIN_GEOMETRY__"
        "FURTHER_DESIGN_REQUIRED")


def test_outcome_c_on_unreliable_linear_prediction_or_failure():
    r = _result_for_outcome(min_delta_margin_linear_state={
        "node": 100, "j": 5, "i": 8, "z": 0, "family": "F3"})
    assert finalize_outcome(r, True) == (
        "DLH_5VN_LOCAL_RESOLVENT_GEOMETRY__"
        "POSITIVE_LOCAL_FEASIBILITY_WITH_STIFF_OR_NONUNIQUE_MARGIN_GEOMETRY__"
        "FURTHER_DESIGN_REQUIRED")
    r2 = _result_for_outcome(trace=[
        {"iteration": 1, "delta_index": 15, "min_pb_new": 0.06},
        {"iteration": 2, "delta_index": 17, "min_pb_new": 0.01}])
    assert finalize_outcome(r2, True) == (
        "DLH_5VN_LOCAL_RESOLVENT_GEOMETRY__"
        "NONFINITE_OR_INCONSISTENT_LOCAL_DIRECTION_OR_MARGIN_EVIDENCE__"
        "BOUNDARY_HJB_ROUTE_REVIEW_REQUIRED")


def test_real_run_terminal_is_a_with_deterministic_repeat():
    r, identical = run_local_geometry_diagnostic_twice()
    assert identical is True
    assert r.deterministic_repeat_identical is True
    assert r.outcome == (
        "DLH_5VN_LOCAL_RESOLVENT_GEOMETRY__"
        "POSITIVE_SUBFLOOR_SAFE_STEP_AND_REPRODUCIBLE_MARGIN_CROSSING__"
        "CONTINUATION_DESIGN_GATE_READY")


# ---------------------------------------------------------------------------
# 17. Summary CSV well-formed and deterministic
# ---------------------------------------------------------------------------
def test_summary_csv_lines_well_formed_and_deterministic():
    r1, _ = run_local_geometry_diagnostic_twice()
    lines1 = r1.to_summary_csv_lines()
    assert lines1[0].startswith("outcome,")
    assert len(lines1) > 30
    for line in lines1:
        assert "," in line and len(line.split(",", 1)) == 2
    r2, _ = run_local_geometry_diagnostic_twice()
    assert lines1 == r2.to_summary_csv_lines()
