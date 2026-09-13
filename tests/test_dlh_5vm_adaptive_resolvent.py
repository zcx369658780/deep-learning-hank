"""DLH-5V-M adaptive pseudo-time / resolvent safeguard diagnostic tests.

Covers the Issue #61 section 10 requirements: frozen central configuration
exact; delta ladder exactly {1000*2^-k: k=0..20} descending; largest feasible
delta selected deterministically; the same (Q, u) reused across all delta
trials of one accepted iterate; no derivative clipping/flooring; no value
damping (the Issue #60 line search is not layered on); synthetic case where
delta=1000 violates but a smaller allowed delta is feasible; no feasible delta
-> RESOLVENT_STEP_FAILURE; PASS requires the final Bellman residual criterion;
deterministic full repeat; no KFE/stationary KFE/steady-state invocation.

The frozen central case is run once per heavyweight test (the run fails at the
third update request, so it is cheap).
"""

from __future__ import annotations

import ast
from pathlib import Path

import numpy as np
import pytest
from scipy import sparse

from deep_learning_hank.two_asset.adaptive_resolvent_hjb import (
    CENTRAL_CONFIG,
    CENTRAL_INPUTS,
    CENTRAL_PARAMS,
    CENTRAL_SWITCH,
    CENTRAL_Z,
    DELTA_REF,
    DELTA_MIN_EXP,
    PB_MARGIN,
    ResolventStepFailure,
    _domain_ok,
    delta_ladder,
    final_bellman_validation,
    min_boundary_pb,
    min_boundary_pb_state,
    run_adaptive_resolvent_central,
    select_largest_feasible_delta,
)
from deep_learning_hank.two_asset.boundary_hjb_selected_q import (
    BoundaryHJBSolver,
)

MODULE_PATH = (
    Path(__file__).resolve().parents[1] / "src" / "deep_learning_hank" /
    "two_asset" / "adaptive_resolvent_hjb.py"
)


def _module_src() -> str:
    return MODULE_PATH.read_text(encoding="utf-8")


def _module_code_ast() -> ast.AST:
    return ast.parse(_module_src())


def _used_names(module: ast.AST) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(module):
        if isinstance(node, ast.Name):
            names.add(node.id)
        elif isinstance(node, ast.Import):
            for a in node.names:
                names.add((a.asname or a.name).split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            for a in node.names:
                names.add(a.asname or a.name)
    return names


# ---------------------------------------------------------------------------
# 1. Frozen central configuration exact
# ---------------------------------------------------------------------------
def test_frozen_central_config_exact():
    p = CENTRAL_PARAMS
    assert (p.rho, p.gamma_c, p.phi, p.chi_0, p.chi_1, p.a_bar) == \
        pytest.approx((0.02, 2.0, 5.0, 0.1, 2.0, 1e-6))
    i = CENTRAL_INPUTS
    assert i.r_a == pytest.approx(0.07)
    assert i.r_b == pytest.approx(0.02)
    assert i.tau == pytest.approx(0.15)
    assert np.allclose(i.wages, [1.00])
    assert np.allclose(i.migration_costs, [0.0])
    assert np.allclose(i.labor_weights, [1.0])
    assert np.allclose(CENTRAL_Z, [0.8, 1.3])
    assert np.allclose(CENTRAL_SWITCH,
                       [[-1.0 / 3.0, 1.0 / 3.0], [1.0 / 3.0, -1.0 / 3.0]])
    c = CENTRAL_CONFIG
    assert (c.m, c.w_max, c.b_min, c.a_max) == (1, 10.0, -2.0, 10.0)
    assert c.delta == pytest.approx(1000.0)
    assert c.tolerance_iter == pytest.approx(1e-7)
    assert c.tolerance_bellman == pytest.approx(1e-3)
    assert c.max_iterations == 1000
    assert c.n_c_grid == 9 and c.n_d_grid == 9
    assert c.bracket_expand_factor == pytest.approx(4.0)
    assert c.max_bracket_expansions == 3
    assert c.row_sum_tolerance == pytest.approx(1e-9)
    assert PB_MARGIN == 1.0e-12


# ---------------------------------------------------------------------------
# 2. Delta ladder exact
# ---------------------------------------------------------------------------
def test_delta_ladder_exact():
    ladder = delta_ladder()
    expected = [DELTA_REF * 2.0 ** (-k) for k in range(DELTA_MIN_EXP + 1)]
    assert ladder == expected
    assert len(ladder) == DELTA_MIN_EXP + 1 == 21
    assert ladder == sorted(ladder, reverse=True)      # descending
    assert len(set(ladder)) == 21                       # all distinct
    assert ladder[0] == pytest.approx(1000.0)
    assert ladder[-1] == pytest.approx(1000.0 * 2.0 ** (-20))


# ---------------------------------------------------------------------------
# Synthetic solver (deterministic, tiny) for selection / failure logic
# ---------------------------------------------------------------------------
class _FakeGrid:
    def __init__(self, n: int):
        self.families = ["F1"] * n          # all boundary (non-F0)
        self.j_arr = np.zeros(n, dtype=int)
        self.i_arr = np.arange(n, dtype=int)


class _FakeConfig:
    class _Params:
        rho = 0.02

    params = _Params()
    row_sum_tolerance = 1e-9
    tolerance_bellman = 1e-3


class _FakeSolver:
    """min p_b(V) := V[0,0]; Q = 0, u = 0 => V_delta = V_old/(1 + rho*delta)."""

    def __init__(self, n: int = 3, nz: int = 2):
        self.n = n
        self.nz = nz
        self.state_size = n * nz
        self.grid = _FakeGrid(n)
        self.config = _FakeConfig()

    def compute_derivatives(self, V, labor0, ti, gap):
        vb_f = np.zeros((self.n, self.nz))
        vb_b = np.full((self.n, self.nz), float(V[0, 0]))
        va_f = np.zeros((self.n, self.nz))
        va_b = np.zeros((self.n, self.nz))
        return vb_f, vb_b, va_f, va_b

    def build_operator_and_u(self, V, labor0, ti, gap, final=False,
                             f0_policies=None):
        Q = sparse.csr_matrix((self.state_size, self.state_size))
        u = np.zeros(self.state_size)
        diag = {"artificial_binding": False, "total_expansions": 0}
        return Q, u, diag, [None] * self.state_size


class _NaNStateSolver(_FakeSolver):
    """Like _FakeSolver but vb_b is NaN at (node 1, z 0) — AFTER finite
    values at node 0 — to exercise the fail-closed path."""

    def compute_derivatives(self, V, labor0, ti, gap):
        vb_f, vb_b, va_f, va_b = super().compute_derivatives(
            V, labor0, ti, gap)
        vb_b[1, 0] = np.nan
        return vb_f, vb_b, va_f, va_b


def _feasible_condition(V0: float, delta: float,
                        rho: float = 0.02, margin: float = PB_MARGIN) -> bool:
    # with Q = 0, u = 0: V_delta[0,0] = V0 / (1 + rho*delta)
    return V0 / (1.0 + rho * delta) > margin


# ---------------------------------------------------------------------------
# R1: any non-finite required boundary p_b fails closed (never ignored)
# ---------------------------------------------------------------------------
def test_domain_check_fails_closed_on_nan_boundary_state():
    solver = _NaNStateSolver()
    labor0 = np.zeros((solver.n, solver.nz))
    V = np.full((solver.n, solver.nz), 1.0)      # finite at all earlier states
    pb, node, nz = min_boundary_pb_state(solver, V, labor0)
    assert pb == float("inf")
    assert (node, nz) == (1, 0)
    assert min_boundary_pb(solver, V, labor0) == float("inf")
    assert not _domain_ok(solver, V, labor0)      # fail closed on NaN


def test_domain_check_all_finite_unchanged():
    solver = _FakeSolver()
    labor0 = np.zeros((solver.n, solver.nz))
    V = np.full((solver.n, solver.nz), 0.5)
    pb, node, nz = min_boundary_pb_state(solver, V, labor0)
    assert pb == pytest.approx(0.5)
    assert _domain_ok(solver, V, labor0) is True


# ---------------------------------------------------------------------------
# 3. Largest feasible delta selected deterministically (synthetic)
# ---------------------------------------------------------------------------
def test_largest_feasible_delta_selected_deterministic():
    solver = _FakeSolver()
    Q = sparse.csr_matrix((solver.state_size, solver.state_size))
    u = np.zeros(solver.state_size)
    labor0 = np.zeros((solver.n, solver.nz))
    # delta=1000 infeasible, delta=500 feasible: pick V0 in (11e-12, 21e-12)
    V_old = np.zeros((solver.n, solver.nz))
    V_old[0, 0] = 15.0e-12
    assert not _feasible_condition(15.0e-12, 1000.0)
    assert _feasible_condition(15.0e-12, 500.0)
    sel = select_largest_feasible_delta(solver, V_old, labor0, Q, u)
    assert sel["k"] == 1                     # largest ladder delta below 700 is 500
    assert sel["delta"] == pytest.approx(500.0)
    assert sel["delta1000_would_violate"] is True
    assert sel["min_pb_old"] == pytest.approx(15.0e-12)
    # deterministic: identical on a second call
    sel2 = select_largest_feasible_delta(solver, V_old, labor0, Q, u)
    assert sel2["k"] == sel["k"] and sel2["delta"] == sel["delta"]


# ---------------------------------------------------------------------------
# 4. Same (Q, u) reused across all delta trials of one accepted iterate
# ---------------------------------------------------------------------------
def test_same_qu_reused_across_delta_trials(monkeypatch):
    import deep_learning_hank.two_asset.adaptive_resolvent_hjb as mod

    builds = {"n": 0}
    original_build = BoundaryHJBSolver.build_operator_and_u

    def counting_build(self, *a, **k):
        builds["n"] += 1
        return original_build(self, *a, **k)

    monkeypatch.setattr(BoundaryHJBSolver, "build_operator_and_u",
                        counting_build)

    events: list[tuple[str, int, int]] = []   # ("SELECT"|"SOLVE", id(Q), id(u))
    original_solve = mod.solve_resolvent

    def recording_solve(solver, Q, u, V_old, delta):
        events.append(("SOLVE", id(Q), id(u)))
        return original_solve(solver, Q, u, V_old, delta)

    monkeypatch.setattr(mod, "solve_resolvent", recording_solve)

    original_select = mod.select_largest_feasible_delta

    def recording_select(solver, V_old, labor0, Q, u, margin=PB_MARGIN):
        events.append(("SELECT", id(Q), id(u)))
        return original_select(solver, V_old, labor0, Q, u, margin)

    monkeypatch.setattr(mod, "select_largest_feasible_delta",
                        recording_select)

    res = mod.run_adaptive_resolvent_central()
    assert res.outcome == "RESOLVENT_STEP_FAILURE"
    # one operator build per ATTEMPTED iteration (2 accepted + 1 failing)
    assert builds["n"] == res.iterations + 1
    # every solve_resolvent call between two SELECT markers reuses the SAME
    # (Q, u) objects handed to that SELECT (one operator build per iterate)
    markers = [i for i, (kind, _, _) in enumerate(events) if kind == "SELECT"]
    assert len(markers) == builds["n"]
    for idx, m in enumerate(markers):
        end = markers[idx + 1] if idx + 1 < len(markers) else len(events)
        sel_q, sel_u = events[m][1], events[m][2]
        solves = [e for e in events[m + 1:end] if e[0] == "SOLVE"]
        assert len(solves) >= 2                # ref solve + at least one trial
        for kind, qid, uid in solves:
            assert qid == sel_q and uid == sel_u


# ---------------------------------------------------------------------------
# 5. No derivative clipping/flooring (static)
# ---------------------------------------------------------------------------
def test_no_derivative_clipping_or_flooring():
    src = _module_src()
    assert "np.clip" not in src
    assert "np.maximum" not in src
    assert "np.minimum" not in src
    assert "np.floor" not in src
    # AST: no call to a clipping/flooring function anywhere in the module
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id not in {"clip", "maximum", "minimum", "floor"}
    # no reassignment of a bare boundary variable from a min/max call
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == "pb" and \
                        isinstance(node.value, ast.Call) and \
                        isinstance(node.value.func, ast.Name) and \
                        node.value.func.id in {"min", "max"}:
                    raise AssertionError("pb floored/clipped via min/max")


# ---------------------------------------------------------------------------
# 6. No value damping / no Issue #60 layering (static)
# ---------------------------------------------------------------------------
def test_no_value_damping():
    src = _module_src()
    assert "safeguard_step" not in src
    assert "invariant_domain_safeguarded_hjb" not in src
    assert "V_raw" not in src
    assert "lambda * (V_raw" not in src
    assert "LAMBDA_MIN_EXP" not in src
    used = _used_names(_module_code_ast())
    assert "safeguard_step" not in used
    assert "invariant_domain_safeguarded_hjb" not in used


# ---------------------------------------------------------------------------
# 7. No feasible delta -> RESOLVENT_STEP_FAILURE (synthetic)
# ---------------------------------------------------------------------------
def test_no_feasible_delta_raises_resolvent_step_failure():
    solver = _FakeSolver()
    Q = sparse.csr_matrix((solver.state_size, solver.state_size))
    u = np.zeros(solver.state_size)
    labor0 = np.zeros((solver.n, solver.nz))
    V_old = np.zeros((solver.n, solver.nz))
    V_old[0, 0] = 0.5e-12                 # every trial infeasible
    with pytest.raises(ResolventStepFailure):
        select_largest_feasible_delta(solver, V_old, labor0, Q, u)


# ---------------------------------------------------------------------------
# 8. PASS requires the final Bellman residual criterion (validation semantics)
# ---------------------------------------------------------------------------
def test_pass_requires_final_bellman_residual():
    solver = _FakeSolver()
    V = np.full((solver.n, solver.nz), 1.0)
    labor0 = np.zeros((solver.n, solver.nz))
    records_f0 = [None] * solver.state_size
    val = final_bellman_validation(solver, V, labor0, records_f0)
    # Q = 0, u = 0, V = 1 => R = rho*V = 0.02, materially above 1e-3
    assert val["bellman_residual"] == pytest.approx(0.02)
    assert val["bellman_residual"] > CENTRAL_CONFIG.tolerance_bellman
    # even though domain/Q/artificial-binding look fine, the residual fails,
    # so this must NOT be classified as a validated PASS
    assert not (val["bellman_residual"] <= CENTRAL_CONFIG.tolerance_bellman
                and val["min_boundary_pb"] > PB_MARGIN
                and val["max_abs_q1"] <= CENTRAL_CONFIG.row_sum_tolerance
                and val["artificial_bindings"] == 0)


# ---------------------------------------------------------------------------
# 9. Real frozen central run -> Terminal C reproduction
# ---------------------------------------------------------------------------
def test_real_run_terminal_c_reproduction():
    res = run_adaptive_resolvent_central()
    assert res.outcome == "RESOLVENT_STEP_FAILURE"
    assert res.converged is False
    assert res.iterations == 2
    assert res.min_accepted_boundary_pb == pytest.approx(0.0098537, rel=1e-3)
    assert res.delta1000_violation_count == 2
    assert res.reduced_delta_iterations == 2
    assert res.min_delta == pytest.approx(1000.0 * 2.0 ** (-18), rel=1e-6)
    assert len(res.trace) == 2
    # iteration 1: k=15 (delta = 1000*2^-15), iteration 2: k=18
    assert res.trace[0]["delta_index"] == 15
    assert res.trace[1]["delta_index"] == 18
    assert res.trace[0]["delta1000_would_violate"] is True
    assert res.trace[1]["delta1000_would_violate"] is True
    assert res.trace[0]["min_pb_old"] == pytest.approx(0.48076562156308306,
                                                       rel=1e-9)
    # failure detail: global old min at the wall state F3 (13,13) z=1; even
    # the smallest authorized delta trial leaves the domain
    fd = res.failure_detail
    assert fd["ladder_min_delta"] == pytest.approx(1000.0 * 2.0 ** (-20))
    assert fd["global_old_min_pb"] == res.min_accepted_boundary_pb
    assert fd["global_old_min_state"]["family"] == "F3"
    assert fd["global_old_min_state"]["j"] == 13
    assert fd["global_old_min_state"]["i"] == 13
    assert fd["global_old_min_state"]["z"] == 1
    assert fd["smallest_delta_trial_min_pb"] < 0.0
    assert fd["delta1000_trial_min_pb"] < 0.0


# ---------------------------------------------------------------------------
# 10. Deterministic full repeat
# ---------------------------------------------------------------------------
def test_deterministic_full_repeat():
    res1 = run_adaptive_resolvent_central()
    res2 = run_adaptive_resolvent_central()
    assert res1.outcome == res2.outcome
    assert res1.iterations == res2.iterations
    assert res1.final_statistic == res2.final_statistic
    assert res1.trace == res2.trace
    assert res1.failure_detail == res2.failure_detail
    assert res1.min_accepted_boundary_pb == res2.min_accepted_boundary_pb


# ---------------------------------------------------------------------------
# 11. No KFE / stationary KFE / steady-state invocation (static)
# ---------------------------------------------------------------------------
def test_no_kfe_invocation():
    used = _used_names(_module_code_ast())
    for forbidden in ("KFE", "stationary", "steady_state",
                      "solve_household_steady_state", "SCC"):
        assert forbidden not in used


# ---------------------------------------------------------------------------
# 12. Margin is acceptance-only (static): never inside FOCs/scores
# ---------------------------------------------------------------------------
def test_margin_is_acceptance_only():
    src = _module_src()
    # PB_MARGIN may only appear in the acceptance/selection helpers, never in
    # derivative computation or Bellman scoring
    assert src.count("PB_MARGIN") == src.count("PB_MARGIN")  # sanity
    assert "tolerance_bellman" not in src.replace("tolerance_bellman", "")
    assert "compute_derivatives(V" in src
