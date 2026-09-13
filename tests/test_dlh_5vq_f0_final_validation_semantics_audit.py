"""DLH-5V-Q test suite — F0 final-validation operator consistency audit
(Issue #65)."""

import ast
import inspect
import types

import numpy as np
import pytest

import deep_learning_hank.two_asset.f0_final_validation_semantics_audit as g
from deep_learning_hank.two_asset.f0_final_validation_semantics_audit import (
    DECOMPOSITION_TOL,
    RECONSTRUCT_STEPS,
    TERMINAL_A,
    TERMINAL_B,
    TERMINAL_C,
    F0ValidationSemanticsFailure,
    build_three_operators,
    finalize_outcome,
    f0_operator_differences,
    f0_provenance_controls,
    run_issue65_audit_twice,
)
from deep_learning_hank.two_asset.stagnation_newton_geometry import (
    reconstruct_issue63_stagnation_state,
)


# ---------------------------------------------------------------------------
# Module-scoped real-run fixture (one audit + one deterministic repeat)
# ---------------------------------------------------------------------------
@pytest.fixture(scope="module")
def audit():
    result, identical = run_issue65_audit_twice()
    return result, identical


# ---------------------------------------------------------------------------
# 1. Exact accepted Issue #63 stagnation-state reconstruction
# ---------------------------------------------------------------------------
def test_exact_stagnation_reconstruction(audit):
    r, _ = audit
    assert r.iterations == RECONSTRUCT_STEPS
    assert len(r.trace) == RECONSTRUCT_STEPS
    assert all(t["path"] == "root" and t["cap_direct"] is False for t in r.trace)
    assert r.final_statistic == pytest.approx(3.6614352438846254e-08, rel=1e-12)
    assert r.min_boundary_pb_star == pytest.approx(4.8089461301970005e-09, rel=1e-9)
    assert r.wall_state is not None
    assert r.wall_state["node"] == 332
    assert r.wall_state["family"] == "F3"
    assert r.wall_state["j"] == 13 and r.wall_state["i"] == 13 and r.wall_state["z"] == 1
    assert r.trace[-1]["delta_selected"] == pytest.approx(
        3.5087694086826935e-09, rel=1e-12)


# ---------------------------------------------------------------------------
# 2/3. R_iter and R_final_stale exact reproduction
# ---------------------------------------------------------------------------
def test_r_iter_exact_reproduction(audit):
    r, _ = audit
    assert r.r_iter_inf == pytest.approx(10.435094313164921, rel=1e-12)
    assert r.r_iter_argmax is not None and r.r_iter_argmax["family"] == "F0"
    assert r.r_iter_f0_max == pytest.approx(r.r_iter_inf, rel=1e-12)
    assert r.r_iter_boundary_max == pytest.approx(9.742068328671465, rel=1e-12)


def test_r_final_stale_exact_reproduction(audit):
    r, _ = audit
    assert r.r_final_stale_inf == pytest.approx(490.7560425919994, rel=1e-12)
    assert r.r_final_stale_argmax is not None
    assert r.r_final_stale_argmax["node"] == 272
    assert r.r_final_stale_argmax["family"] == "F0"
    assert r.r_final_stale_f0_max == pytest.approx(r.r_final_stale_inf, rel=1e-12)


# ---------------------------------------------------------------------------
# 4. records provenance explicit and not swapped
# ---------------------------------------------------------------------------
def test_records_provenance_not_swapped():
    rec = reconstruct_issue63_stagnation_state()
    solver, V_star, labor0, records_pre = (
        rec["solver"], rec["V_star"], rec["labor0"], rec["records_pre_step8"])
    rho = rec["rho"]
    calls = []
    orig = solver.build_operator_and_u

    def spy(*args, **kwargs):
        calls.append(kwargs)
        return orig(*args, **kwargs)

    solver.build_operator_and_u = spy
    three = build_three_operators(solver, V_star, labor0, records_pre, rho)
    # exactly three builds at V_*: final=False, stale final=True, current final=True
    assert len(calls) == 3
    assert [c["final"] for c in calls] == [False, True, True]
    # build 1 (iteration) returns records_current; builds 2/3 use it correctly
    records_current = three["records_current"]
    assert records_current is not records_pre
    assert calls[1]["f0_policies"] is records_pre         # stale build: pre-step-8
    assert calls[2]["f0_policies"] is records_current     # current build: current
    # F0 records exist in both sets (no provenance ambiguity on the real case)
    _, f0_rows = g.f0_rows_of(solver)
    for rrow in f0_rows:
        assert records_pre[rrow] is not None
        assert records_current[rrow] is not None


# ---------------------------------------------------------------------------
# 5. Exactly three authorized operator/residual builds at V_*
# ---------------------------------------------------------------------------
def test_exactly_three_builds_at_v_star(audit):
    r, _ = audit
    # operator diagnostics are present and finite for all three builds
    assert r.max_abs_q1_iter is not None
    assert r.max_abs_q1_final_stale is not None
    assert r.max_abs_q1_final_current is not None
    assert np.isfinite(r.max_abs_q1_iter)
    assert r.max_abs_q1_iter == pytest.approx(
        r.max_abs_q1_final_stale, rel=1e-6)
    assert r.max_abs_q1_iter == pytest.approx(
        r.max_abs_q1_final_current, rel=1e-6)


# ---------------------------------------------------------------------------
# 6. D_total = D_stale + D_rate within declared tolerance
# ---------------------------------------------------------------------------
def test_additive_decomposition_holds(audit):
    r, _ = audit
    assert r.add_err_inf is not None
    assert r.add_err_inf <= DECOMPOSITION_TOL
    # algebraic consistency of the recorded norms' sources
    assert r.d_total_inf == pytest.approx(
        488.0988429898615, rel=1e-9)
    assert r.d_stale_inf < r.d_rate_inf


# ---------------------------------------------------------------------------
# 7. total / F0 / boundary decomposition deterministic
# ---------------------------------------------------------------------------
def test_total_f0_boundary_decomposition_deterministic(audit):
    r, identical = audit
    assert identical is True
    assert r.deterministic_repeat_identical is True
    for inf, f0, bnd in ((r.r_iter_inf, r.r_iter_f0_max, r.r_iter_boundary_max),
                         (r.r_final_stale_inf, r.r_final_stale_f0_max,
                          r.r_final_stale_boundary_max),
                         (r.r_final_current_inf, r.r_final_current_f0_max,
                          r.r_final_current_boundary_max),
                         (r.d_total_inf, r.d_total_f0_max,
                          r.d_total_boundary_max),
                         (r.d_stale_inf, r.d_stale_f0_max,
                          r.d_stale_boundary_max),
                         (r.d_rate_inf, r.d_rate_f0_max,
                          r.d_rate_boundary_max)):
        assert f0 is not None and bnd is not None
        assert inf >= f0 and inf >= bnd
        assert np.isfinite(inf)


# ---------------------------------------------------------------------------
# 8. Boundary-only differences consistent with accepted Issue #64 evidence
# ---------------------------------------------------------------------------
def test_boundary_only_differences_exactly_zero():
    # boundary rows are built identically in both semantics (Issue #64
    # accepted evidence: R_final - R_iter boundary diff == 0). The same must
    # hold for every Issue #65 difference.
    rec = reconstruct_issue63_stagnation_state()
    solver, V_star, labor0, records_pre = (
        rec["solver"], rec["V_star"], rec["labor0"], rec["records_pre_step8"])
    rho = rec["rho"]
    three = build_three_operators(solver, V_star, labor0, records_pre, rho)
    keymap = {"D_total": "stats_d_total", "D_stale": "stats_d_stale",
              "D_rate": "stats_d_rate"}
    for key in ("D_total", "D_stale", "D_rate"):
        stats = three[keymap[key]]
        assert stats["boundary"]["max_abs"] == 0.0, key
    # boundary-only residual values are identical across the three operators
    assert three["stats_iter"]["boundary"]["max_abs"] == pytest.approx(
        three["stats_final_stale"]["boundary"]["max_abs"], rel=1e-12)
    assert three["stats_final_stale"]["boundary"]["max_abs"] == pytest.approx(
        three["stats_final_current"]["boundary"]["max_abs"], rel=1e-12)


# ---------------------------------------------------------------------------
# 9. Continuous-control provenance does not rely only on sector labels
# ---------------------------------------------------------------------------
def test_provenance_reports_continuous_controls(audit):
    r, _ = audit
    assert r.f0_row_count == 596
    assert r.changed_label_count == 0          # frozen case: labels unchanged
    # BUT continuous controls differ slightly: sector-label equality is NOT
    # treated as continuous-control equality (Issue #65 required audit).
    deltas = (r.max_abs_delta_consumption, r.max_abs_delta_labor,
              r.max_abs_delta_transfer, r.max_abs_delta_mu_a,
              r.max_abs_delta_mu_b, r.max_abs_delta_utility)
    assert all(d is not None and np.isfinite(d) for d in deltas)
    assert r.max_abs_delta_transfer > 0.0
    assert r.max_abs_delta_mu_b > 0.0
    # the F0 provenance function is a standalone continuous-control audit
    rec = reconstruct_issue63_stagnation_state()
    solver = rec["solver"]
    three = build_three_operators(solver, rec["V_star"], rec["labor0"],
                                  rec["records_pre_step8"], rec["rho"])
    prov = f0_provenance_controls(solver, rec["records_pre_step8"],
                                  three["records_current"])
    assert set(prov) >= {
        "f0_row_count", "changed_sector_transfer_label_count",
        "max_abs_delta_consumption", "max_abs_delta_labor",
        "max_abs_delta_transfer", "max_abs_delta_mu_a", "max_abs_delta_mu_b",
        "max_abs_delta_utility"}
    assert prov["max_abs_delta_utility"] > 0.0


def test_operator_differences_are_f0_only(audit):
    r, _ = audit
    # Q_final_stale - Q_final_current is tiny (nearly identical records);
    # Q_final_current - Q_iter is the dominating final-semantics operator gap
    assert r.q_stale_minus_current_rowwise_max is not None
    assert np.isfinite(r.q_stale_minus_current_rowwise_max)
    assert r.q_stale_minus_current_rowwise_max < 1e-3
    assert r.q_current_minus_iter_rowwise_max > 1.0
    # u_final_current - u_iter is exactly 0 (same selected utilities on F0 rows)
    assert r.u_current_minus_iter_max == 0.0
    assert r.u_current_minus_iter_argmax is None
    assert np.isfinite(r.u_stale_minus_current_max)


# ---------------------------------------------------------------------------
# 10. Non-finite / inconsistent evidence fails closed
# ---------------------------------------------------------------------------
class _FakeSolver:
    def __init__(self, nan=True):
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
        self._nan = nan

    def compute_derivatives(self, V, labor0, ti, gap):
        V = np.asarray(V, float).reshape(self.n, self.nz)
        out = np.full(V.shape, np.nan) if self._nan else np.zeros(V.shape)
        return (np.zeros_like(V), out, np.zeros_like(V), np.zeros_like(V))

    def build_operator_and_u(self, V, labor0, ti, gap, final=False,
                             f0_policies=None):
        V = np.asarray(V, float).reshape(self.n, self.nz)
        Q = np.zeros((self.state_size, self.state_size))
        u = np.full(self.state_size, np.nan if self._nan else 0.0)
        diag = {"total_expansions": 0, "artificial_binding": 0}
        return Q, u, diag, [None] * self.state_size


def test_nonfinite_residual_fails_closed():
    # R_iter / R_final_stale / R_final_current non-finite -> failure -> C
    import deep_learning_hank.two_asset.f0_final_validation_semantics_audit as gg

    def fake_reconstruct():
        n, nz = 3, 1
        solver = _FakeSolver(nan=True)
        V = np.zeros((n, nz))
        recs = [None] * (n * nz)
        return {"solver": solver, "labor0": np.zeros((n, nz)),
                "V_star": V, "records_pre_step8": recs, "rho": 0.02,
                "trace": [], "v0_min_boundary_pb": 1.0,
                "min_accepted_boundary_pb": 1.0}

    orig = gg.reconstruct_issue63_stagnation_state
    gg.reconstruct_issue63_stagnation_state = fake_reconstruct
    try:
        rr = gg.run_issue65_audit()
        assert rr.outcome == TERMINAL_C
        assert rr.failure_detail is not None
    finally:
        gg.reconstruct_issue63_stagnation_state = orig


def test_provenance_ambiguity_fails_closed():
    # missing F0 record -> provenance ambiguity -> F0ValidationSemanticsFailure
    n, nz = 3, 1
    solver = _FakeSolver(nan=False)
    # make row 0 an F0 row so the audit actually visits an F0 row with no record
    solver.grid.families = ["F0", "F1", "F1"]
    recs_pre = [None] * (n * nz)
    recs_cur = [None] * (n * nz)
    with pytest.raises(F0ValidationSemanticsFailure):
        f0_provenance_controls(solver, recs_pre, recs_cur)


# ---------------------------------------------------------------------------
# 11. Deterministic repeat identical
# ---------------------------------------------------------------------------
def test_deterministic_full_repeat(audit):
    r, identical = audit
    assert identical is True
    assert r.deterministic_repeat_identical is True


# ---------------------------------------------------------------------------
# 12. Exactly one terminal; no forbidden machinery (static AST)
# ---------------------------------------------------------------------------
def test_exactly_one_terminal_returned(audit):
    r, _ = audit
    assert r.outcome in (TERMINAL_A, TERMINAL_B, TERMINAL_C)


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
    # no Newton / continuation / line search / damping / p_b clip-floor
    for banned in ("newton", "continuation", "linesearch", "armijo",
                   "damp", "clip", "floor", "maximum", "minimum",
                   "trust_region", "semismooth", "policy_iteration",
                   "spsolve", "construct_ftb_step", "trial"):
        assert banned not in low, banned
    # no KFE / stationary / steady-state machinery
    for banned in ("kfe", "stationary", "steady_state",
                   "solve_household_steady_state"):
        assert banned not in low, banned
    # exactly the three authorized builds appear in the module source
    call_names = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                call_names.append(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                call_names.append(node.func.attr)
    assert call_names.count("build_operator_and_u") == 3
    assert call_names.count("f0_provenance_controls") == 1
    assert call_names.count("f0_operator_differences") == 1
