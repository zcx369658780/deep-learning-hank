"""DLH-5V-O test suite — continuous fraction-to-boundary pseudo-transient
continuation on the frozen central selected-Q HJB case (Issue #63)."""

import ast
import types

import numpy as np
import pytest
from scipy import sparse

from deep_learning_hank.two_asset.continuous_ftb_resolvent_hjb import (
    BELLMAN_TOL,
    CENTRAL_CONFIG,
    CONVERGENCE_TOL,
    DELTA_CAP,
    EPS_FTB,
    FTB_RETAIN_TOL,
    FTB_STAGNATION,
    FTBStepConstructionFailure,
    MAX_BRACKET_HALVINGS,
    PB_MARGIN,
    RETAIN,
    TAU_FTB,
    TERMINAL_A,
    TERMINAL_B,
    TERMINAL_C,
    construct_ftb_step,
    ftb_h_value,
    run_ftb_continuation,
    run_ftb_continuation_twice,
    run_ftb_continuation_with,
    single_ftb_iterate,
    solve_resolvent_scaled,
)
from deep_learning_hank.two_asset.adaptive_resolvent_hjb import (
    CENTRAL_INPUTS,
    CENTRAL_PARAMS,
    CENTRAL_SWITCH,
    CENTRAL_Z,
    DELTA_MIN_EXP,
    DELTA_REF,
    MAX_ITERATIONS,
)
import deep_learning_hank.two_asset.continuous_ftb_resolvent_hjb as ftb_mod
import deep_learning_hank.two_asset.adaptive_resolvent_hjb as acc_mod


# ---------------------------------------------------------------------------
# Small linear fake solver (p_b = V elementwise; all states required)
# ---------------------------------------------------------------------------
class _FakeSolver:
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

    def build_operator_and_u(self, V, labor0, ti, gap, final=False,
                             f0_policies=None):
        V = np.asarray(V, float).reshape(self.n, self.nz)
        u = np.zeros(self.state_size)
        Q = sparse.csr_matrix((self.state_size, self.state_size))
        diag = {"total_expansions": 0, "artificial_binding": 0}
        rec = types.SimpleNamespace(family="F1", sector="S1")
        records = [rec] * self.state_size
        return Q, u, diag, records


class _NaNSolver(_FakeSolver):
    def compute_derivatives(self, V, labor0, ti, gap):
        V = np.asarray(V, float).reshape(self.n, self.nz)
        out = np.full(V.shape, np.nan)
        return (np.zeros_like(V), out, np.zeros_like(V), np.zeros_like(V))


def _synthetic_geometric_case():
    """Q=0, u=0, rho=0.02, V0=0.05 everywhere: every FTB step is a root step
    with delta_ftb = 450 (V_{n+1} = 0.1*V_n), geometric decay to zero ->
    validated convergence at ~6 accepted iterations (Outcome A path)."""
    solver = _FakeSolver(3, 1)
    V0 = np.full((solver.n, solver.nz), 0.05)
    labor0 = np.zeros_like(V0)
    return solver, V0, labor0


def _synthetic_subfloor_crossing_case():
    """Consistent with Issue #62 geometry: node 1 (i=1) value
    V1(delta) = (0.01 - 11*delta)/(1 + 0.02*delta) crosses the retained-margin
    target inside (0, DELTA_FLOOR=1000*2^-20): the continuous root-derived step
    lies BELOW the old Issue #61 ladder floor."""
    solver = _FakeSolver(3, 1)
    V0 = np.full((solver.n, solver.nz), 0.01)
    u = np.zeros((solver.n, solver.nz))
    u[1, 0] = -11.0
    Q = sparse.csr_matrix((solver.n, solver.n))
    labor0 = np.zeros_like(V0)
    return solver, Q, u, V0, labor0


# ---------------------------------------------------------------------------
# 1. Frozen central configuration and controller constants
# ---------------------------------------------------------------------------
def test_frozen_central_config_exact():
    # economics live in HouseholdInputs / EconomicParams; grid/domain,
    # tolerances and control-search settings in the solver config
    assert CENTRAL_CONFIG.m == 1
    assert CENTRAL_CONFIG.w_max == 10.0
    assert CENTRAL_CONFIG.b_min == -2.0
    assert CENTRAL_CONFIG.a_max == 10.0
    assert CENTRAL_CONFIG.n_c_grid == 9 and CENTRAL_CONFIG.n_d_grid == 9
    assert CENTRAL_CONFIG.tolerance_iter == 1e-7
    assert CENTRAL_CONFIG.tolerance_bellman == 1e-3
    assert CENTRAL_CONFIG.max_iterations == 1000
    assert CENTRAL_CONFIG.row_sum_tolerance == 1e-9
    assert CENTRAL_INPUTS.r_a == 0.07
    assert CENTRAL_INPUTS.r_b == 0.02
    assert CENTRAL_INPUTS.wages[0] == 1.00
    assert CENTRAL_INPUTS.tau == 0.15
    assert CENTRAL_INPUTS.migration_costs[0] == 0
    assert CENTRAL_INPUTS.labor_weights[0] == 1
    assert CENTRAL_PARAMS.rho == 0.02
    assert CENTRAL_PARAMS.gamma_c == 2
    assert CENTRAL_PARAMS.phi == 5
    assert CENTRAL_PARAMS.chi_0 == 0.1
    assert CENTRAL_PARAMS.chi_1 == 2
    assert CENTRAL_PARAMS.a_bar == 1e-6
    assert CENTRAL_SWITCH is not None
    assert list(CENTRAL_Z) == [0.8, 1.3]
    assert PB_MARGIN == 1e-12
    assert MAX_ITERATIONS == 1000
    assert DELTA_REF == 1000.0 and DELTA_MIN_EXP == 20


def test_frozen_controller_constants_exact():
    assert TAU_FTB == 0.90
    assert RETAIN == pytest.approx(0.10)
    assert DELTA_CAP == 1000.0
    assert EPS_FTB == 1e-6
    assert MAX_BRACKET_HALVINGS == 60
    assert CONVERGENCE_TOL == 1e-7
    assert BELLMAN_TOL == 1e-3


# ---------------------------------------------------------------------------
# 2. (Q_n,u_n) built once and reused across all controller evaluations
# ---------------------------------------------------------------------------
def test_qn_un_built_once_and_reused_within_iterate():
    from deep_learning_hank.two_asset.boundary_hjb_selected_q import (
        BoundaryHJBSolver,
    )
    solver = BoundaryHJBSolver(CENTRAL_CONFIG)
    labor0 = solver.build_labor0(0.0, 0.0)
    V0 = solver.build_initial_value(labor0, 0.0, 0.0)
    counter = {"builds": 0}
    orig = solver.build_operator_and_u

    def counting(*args, **kwargs):
        counter["builds"] += 1
        return orig(*args, **kwargs)

    solver.build_operator_and_u = counting
    it = single_ftb_iterate(solver, V0, labor0)
    assert counter["builds"] == 1          # exactly once for this iterate
    # the whole step construction + verification reused the frozen (Q,u):
    # no further operator build happened during many resolvent evaluations
    assert it["step"]["delta_selected"] > 0.0
    assert it["step"]["selected_min_pb"] > PB_MARGIN


def test_full_run_build_count_is_iterates_plus_final():
    solver, V0, labor0 = _synthetic_geometric_case()
    counter = {"builds": 0}
    orig = solver.build_operator_and_u

    def counting(*args, **kwargs):
        counter["builds"] += 1
        return orig(*args, **kwargs)

    solver.build_operator_and_u = counting
    res = run_ftb_continuation_with(solver, labor0, V0, max_iterations=100)
    assert res.outcome == TERMINAL_A
    # one build per accepted iterate + exactly one final validation build
    assert counter["builds"] == res.accepted_iterations + 1


# ---------------------------------------------------------------------------
# 3. Cap path
# ---------------------------------------------------------------------------
def test_cap_accepted_directly_when_target_retained_margin_passes():
    solver, _, _, V0, labor0 = _synthetic_subfloor_crossing_case()
    u_pos = np.zeros_like(V0) + 0.001       # grows all p_b -> cap feasible
    Q = sparse.csr_matrix((solver.n, solver.n))
    step = construct_ftb_step(solver, V0, labor0, Q, u_pos,
                              float(solver.config.params.rho))
    assert step["cap_direct"] is True
    assert step["path"] == "cap"
    assert step["delta_selected"] == DELTA_CAP
    assert step["halving_count"] == 0
    # direct verification at the selected trial
    assert np.isfinite(step["selected_min_pb"])
    assert step["selected_min_pb"] > PB_MARGIN
    assert step["retained_margin"] >= step["m_target"] - FTB_RETAIN_TOL


# ---------------------------------------------------------------------------
# 4. Halving is bracket construction only (not an accepted ladder)
# ---------------------------------------------------------------------------
def test_halving_only_bracket_construction_not_ladder():
    solver, Q, u, V0, labor0 = _synthetic_subfloor_crossing_case()
    rho = float(solver.config.params.rho)
    step = construct_ftb_step(solver, V0, labor0, Q, u, rho)
    assert step["cap_direct"] is False
    assert step["path"] == "root"
    assert step["halving_count"] >= 1
    assert step["halving_count"] <= MAX_BRACKET_HALVINGS
    lo, hi = step["delta_lo"], step["delta_hi"]
    m_target = step["m_target"]
    h_lo = ftb_h_value(solver, Q, u, V0, labor0, lo, rho, m_target)
    h_hi = ftb_h_value(solver, Q, u, V0, labor0, hi, rho, m_target)
    assert h_lo > 0.0 and h_hi < 0.0       # genuine sign-changing bracket
    # the halving probes are NOT accepted steps: selected delta is the
    # (1-EPS_FTB)-scaled continuous root, not any probe point
    probes = {DELTA_CAP * 0.5 ** k for k in range(0, MAX_BRACKET_HALVINGS + 1)}
    assert step["delta_selected"] not in probes
    assert step["delta_selected"] == pytest.approx(
        (1.0 - EPS_FTB) * step["delta_ftb"], rel=1e-12)
    # direct verification at the selected trial
    assert np.isfinite(step["selected_min_pb"])
    assert step["selected_min_pb"] > PB_MARGIN
    assert step["retained_margin"] >= step["m_target"] - FTB_RETAIN_TOL


def test_bracketed_root_deterministic():
    solver, Q, u, V0, labor0 = _synthetic_subfloor_crossing_case()
    rho = float(solver.config.params.rho)
    s1 = construct_ftb_step(solver, V0, labor0, Q, u, rho)
    s2 = construct_ftb_step(solver, V0, labor0, Q, u, rho)
    assert s1["delta_ftb"] == s2["delta_ftb"]
    assert s1["delta_selected"] == s2["delta_selected"]
    assert s1["halving_count"] == s2["halving_count"]


def test_no_bracket_within_halving_limit_fails_closed():
    # h > 0 only below DELTA_CAP*2^-60 -> no bracket inside 60 halvings
    solver = _FakeSolver(3, 1)
    V0 = np.full((solver.n, solver.nz), 1e-18)
    u = np.zeros_like(V0)
    u[1, 0] = -11.0
    Q = sparse.csr_matrix((solver.n, solver.n))
    labor0 = np.zeros_like(V0)
    with pytest.raises(FTBStepConstructionFailure):
        construct_ftb_step(solver, V0, labor0, Q, u,
                           float(solver.config.params.rho))


# ---------------------------------------------------------------------------
# 5. Sub-floor geometry consistent with Issue #62
# ---------------------------------------------------------------------------
def test_synthetic_subfloor_case_consistent_with_issue62_geometry():
    """The continuous root-derived step must lie BELOW the old Issue #61 ladder
    floor 1000*2^-20, exactly as Issue #62 established locally."""
    solver, Q, u, V0, labor0 = _synthetic_subfloor_crossing_case()
    rho = float(solver.config.params.rho)
    step = construct_ftb_step(solver, V0, labor0, Q, u, rho)
    old_floor = DELTA_REF * 2.0 ** (-DELTA_MIN_EXP)   # 1000*2^-20
    assert step["delta_ftb"] < old_floor
    assert step["delta_selected"] < old_floor
    # analytic: root of (0.01 - 11*d)/(1+0.02*d) = PB_MARGIN + m_target
    m0 = 0.01 - PB_MARGIN
    m_target = RETAIN * m0
    analytic = (0.01 - (PB_MARGIN + m_target)) / 11.0
    assert step["delta_ftb"] == pytest.approx(analytic, rel=1e-4)


# ---------------------------------------------------------------------------
# 6. Fail-closed non-finite evidence
# ---------------------------------------------------------------------------
def test_nonfinite_boundary_evidence_fails_closed():
    solver = _NaNSolver()
    V0 = np.full((solver.n, solver.nz), 0.01)
    Q = sparse.csr_matrix((solver.n, solver.n))
    u = np.zeros_like(V0)
    labor0 = np.zeros_like(V0)
    with pytest.raises(FTBStepConstructionFailure):
        ftb_h_value(solver, Q, u, V0, labor0, 1e-4,
                    float(solver.config.params.rho), 1e-6)
    with pytest.raises(FTBStepConstructionFailure):
        construct_ftb_step(solver, V0, labor0, Q, u,
                           float(solver.config.params.rho))
    # a full run with non-finite evidence terminates at Terminal C (never
    # classified as feasible / convergence)
    res = run_ftb_continuation_with(solver, labor0, V0, max_iterations=10)
    assert res.outcome == TERMINAL_C
    assert res.accepted_iterations == 0


# ---------------------------------------------------------------------------
# 7. Step trigger cannot PASS without the final Bellman criterion
# ---------------------------------------------------------------------------
def test_step_trigger_cannot_pass_without_final_bellman(monkeypatch):
    solver, V0, labor0 = _synthetic_geometric_case()

    def failing_validation(*args, **kwargs):
        return {
            "bellman_residual": 0.5,          # > 1e-3 -> must NOT pass
            "min_boundary_pb": 1e-9,          # <= PB_MARGIN -> must NOT pass
            "max_abs_q1": 0.0,
            "artificial_bindings": 0,
            "expansions": 0,
            "family_histogram": {"F1": solver.state_size},
        }

    monkeypatch.setattr(ftb_mod, "final_bellman_validation",
                        failing_validation)
    res = run_ftb_continuation_with(solver, labor0, V0, max_iterations=100)
    # the step trigger fired (converged step size) but the final Bellman
    # criterion failed -> FTB_STAGNATION / Terminal B, NOT Terminal A
    assert res.converged is True
    assert res.outcome == TERMINAL_B
    assert res.failure_detail.get("message") == FTB_STAGNATION


# ---------------------------------------------------------------------------
# 8. Full deterministic repeat + validated convergence path
# ---------------------------------------------------------------------------
def test_synthetic_validated_convergence_outcome_a():
    solver, V0, labor0 = _synthetic_geometric_case()
    res = run_ftb_continuation_with(solver, labor0, V0, max_iterations=100)
    assert res.outcome == TERMINAL_A
    assert res.converged is True
    assert 5 <= res.accepted_iterations <= 10   # geometric decay to 1e-12
    assert res.final_statistic is not None and res.final_statistic < CONVERGENCE_TOL
    assert res.final_bellman_residual is not None
    assert res.final_bellman_residual <= BELLMAN_TOL
    assert res.final_min_boundary_pb is not None
    assert res.final_min_boundary_pb > PB_MARGIN
    assert res.final_artificial_bindings == 0
    assert len(res.trace) == res.accepted_iterations


def test_deterministic_full_repeat():
    solver, V0, labor0 = _synthetic_geometric_case()
    r1 = run_ftb_continuation_with(solver, labor0, V0, max_iterations=100)
    r2 = run_ftb_continuation_with(solver, labor0, V0, max_iterations=100)
    assert r1.outcome == r2.outcome
    assert r1.accepted_iterations == r2.accepted_iterations
    assert r1.final_statistic == r2.final_statistic
    assert r1.final_bellman_residual == r2.final_bellman_residual
    assert [t["delta_selected"] for t in r1.trace] == \
           [t["delta_selected"] for t in r2.trace]


def test_max_iterations_bounded_nonconvergence_outcome_b():
    # a run cut short before the convergence trigger fires is bounded
    # non-convergence (Terminal B), with the domain preserved on every step
    solver, V0, labor0 = _synthetic_geometric_case()
    res = run_ftb_continuation_with(solver, labor0, V0, max_iterations=3)
    assert res.outcome == TERMINAL_B
    assert res.converged is False
    assert res.accepted_iterations == 3
    assert res.final_bellman_residual is None
    assert all(t["selected_min_pb"] > PB_MARGIN for t in res.trace)


# ---------------------------------------------------------------------------
# 9. Real frozen central case: initial value / single iterate cross-check
# ---------------------------------------------------------------------------
def test_real_initial_value_margin_matches_accepted():
    from deep_learning_hank.two_asset.boundary_hjb_selected_q import (
        BoundaryHJBSolver,
    )
    solver = BoundaryHJBSolver(CENTRAL_CONFIG)
    labor0 = solver.build_labor0(0.0, 0.0)
    V0 = solver.build_initial_value(labor0, 0.0, 0.0)
    from deep_learning_hank.two_asset.adaptive_resolvent_hjb import (
        min_boundary_pb,
    )
    pb0 = min_boundary_pb(solver, V0, labor0)
    assert pb0 == pytest.approx(0.48076562156308306, rel=1e-9)   # accepted V0
    assert pb0 - PB_MARGIN > 0.0


def test_real_single_ftb_iterate_verified():
    from deep_learning_hank.two_asset.boundary_hjb_selected_q import (
        BoundaryHJBSolver,
    )
    solver = BoundaryHJBSolver(CENTRAL_CONFIG)
    labor0 = solver.build_labor0(0.0, 0.0)
    V0 = solver.build_initial_value(labor0, 0.0, 0.0)
    it = single_ftb_iterate(solver, V0, labor0)
    step = it["step"]
    assert step["delta_selected"] > 0.0
    assert np.isfinite(step["selected_min_pb"])
    assert step["selected_min_pb"] > PB_MARGIN
    assert step["retained_margin"] >= step["m_target"] - FTB_RETAIN_TOL
    assert it["max_abs_q1"] <= CENTRAL_CONFIG.row_sum_tolerance
    assert it["direction_norm"] >= 0.0
    assert it["diag"]["total_expansions"] == 0
    assert it["diag"]["artificial_binding"] == 0


# ---------------------------------------------------------------------------
# 10. Static integrity: no damping, no Bellman step selection, no KFE,
#     halving not via the accepted ladder, p_b never clipped/floored
# ---------------------------------------------------------------------------
def _module_ast():
    import inspect
    import deep_learning_hank.two_asset.continuous_ftb_resolvent_hjb as m
    return ast.parse(inspect.getsource(m))


def test_static_integrity_no_forbidden_machinery():
    tree = _module_ast()
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            names.add(node.id)
        if isinstance(node, ast.Attribute):
            names.add(node.attr)
    low = {n.lower() for n in names}
    # no value damping anywhere in the module
    assert not any("damp" in n for n in low), "damping machinery found"
    # no p_b clipping / flooring / max-min replacements
    for banned in ("clip", "floor", "maximum", "minimum"):
        assert banned not in low, banned
    # no KFE / stationary / steady-state machinery
    for banned in ("kfe", "stationary", "steady_state",
                   "solve_household_steady_state"):
        assert banned not in low, banned
    # no Bellman residual anywhere in step selection: only the accepted final
    # validation helper is referenced by the run loop
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name in ("construct_ftb_step", "ftb_h_value",
                             "single_ftb_iterate"):
                fnames = {n.id.lower() for n in ast.walk(node)
                          if isinstance(n, ast.Name)}
                fnames |= {n.attr.lower() for n in ast.walk(node)
                           if isinstance(n, ast.Attribute)}
                assert "bellman" not in fnames, node.name
    # halving is NOT the accepted discrete ladder: no delta_ladder reference
    assert "delta_ladder" not in low
    assert "select_largest_feasible_delta" not in low
    assert "run_adaptive_resolvent_central" not in low


# ---------------------------------------------------------------------------
# 11. Resolvent equivalence with the accepted Issue #61 form (delta > 0)
# ---------------------------------------------------------------------------
def test_scaled_resolvent_equals_accepted_issue61_form():
    from deep_learning_hank.two_asset.boundary_hjb_selected_q import (
        BoundaryHJBSolver,
    )
    from deep_learning_hank.two_asset.adaptive_resolvent_hjb import (
        solve_resolvent,
    )
    solver = BoundaryHJBSolver(CENTRAL_CONFIG)
    labor0 = solver.build_labor0(0.0, 0.0)
    V0 = solver.build_initial_value(labor0, 0.0, 0.0)
    Q, u, _, _ = solver.build_operator_and_u(V0, labor0, 0.0, 0.0)
    rho = float(solver.config.params.rho)
    for delta in (1e-4, 0.5, DELTA_CAP):
        v_scaled = solve_resolvent_scaled(solver, Q, u, V0, delta, rho)
        v_orig = solve_resolvent(solver, Q, u, V0, delta)
        assert np.max(np.abs(v_scaled - v_orig)) < 1e-10
    # well-defined at delta = 0: V(0) = V_n
    v0 = solve_resolvent_scaled(solver, Q, u, V0, 0.0, rho)
    assert np.max(np.abs(v0 - V0)) < 1e-12


# ---------------------------------------------------------------------------
# 12. Public run constructs the real frozen central case
# ---------------------------------------------------------------------------
def test_run_ftb_continuation_public_uses_real_central_case():
    from deep_learning_hank.two_asset.boundary_hjb_selected_q import (
        BoundaryHJBSolver,
    )
    import deep_learning_hank.two_asset.continuous_ftb_resolvent_hjb as m
    captured = {}
    orig_solver = m.BoundaryHJBSolver

    def spy(*args, **kwargs):
        s = orig_solver(*args, **kwargs)
        captured["solver"] = s
        return s

    m.BoundaryHJBSolver = spy
    try:
        res = m.run_ftb_continuation()
    finally:
        m.BoundaryHJBSolver = orig_solver
    assert "solver" in captured
    assert res.outcome in (TERMINAL_A, TERMINAL_B, TERMINAL_C)


# ---------------------------------------------------------------------------
# 13. run_ftb_continuation_twice returns (run, repeat, identical) on the
#     synthetic case via the parameterized core (identical logic)
# ---------------------------------------------------------------------------
def test_twice_helper_identical_logic():
    solver, V0, labor0 = _synthetic_geometric_case()
    r1 = run_ftb_continuation_with(solver, labor0, V0, max_iterations=100)
    r2 = run_ftb_continuation_with(solver, labor0, V0, max_iterations=100)
    from deep_learning_hank.two_asset.continuous_ftb_resolvent_hjb import (
        _results_identical,
    )
    assert _results_identical(r1, r2) is True
