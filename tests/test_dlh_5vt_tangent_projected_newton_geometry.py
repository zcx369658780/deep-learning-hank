"""DLH-5V-T — focused test suite for the single-wall tangent-projected
frozen-policy Newton geometry diagnostic (Issue #68).

Authority: Issue #68 OPEN; initial authoritative activation ``5674754187``;
final authoritative activation-refresh ``5675003122`` (post-sync live ``main``
``e569271904eacbd3b2721b0b0f1ebb8e9a559e3f``). Route decision
``APPROVE_SINGLE_WALL_TANGENT_PROJECTED_NEWTON_GEOMETRY_AFTER_5VS_TERMINAL_A``;
authority marker ``DLH_5VT_TANGENT_PROJECTED_NEWTON_GEOMETRY_AUTHORIZED``.

Scope ceiling: this is a local direction-geometry DIAGNOSTIC. No trial state is
an accepted HJB iterate; no multi-step Newton, no policy iteration, no
semismooth / trust-region / continuation, no adaptive line search or alpha
tuning, no multiple active constraints, no projection-metric optimization, no
``p_b`` clip/floor, no economics/prices/grid/domain/initialization/controls/
tolerances/``PB_MARGIN``/Bellman-tolerance change, no convergence-criterion
change, no KFE / stationary KFE / steady state.
"""

from __future__ import annotations

import ast
import dataclasses
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pytest
from scipy import sparse

import deep_learning_hank.two_asset.tangent_projected_newton_geometry as m
from deep_learning_hank.two_asset.local_resolvent_domain_geometry import (
    boundary_direction_matrix,
)
from deep_learning_hank.two_asset.stagnation_newton_geometry import (
    PB_MARGIN,
    reconstruct_issue63_stagnation_state,
)

ALPHA_CROSS_N_HISTORICAL = 1.8667384893e-4
CORRECTED_ALPHA_CROSS_T_EXPECTED = 0.16170699931086815
SUPERSEDED_SINGLE_ENTRY_ALPHA_CROSS_T = 0.009436421907523617

MODULE_PATH = Path(m.__file__)
MODULE_SOURCE = MODULE_PATH.read_text(encoding="utf-8")

SELECTED_Q_RELPATH = "src/deep_learning_hank/two_asset/boundary_hjb_selected_q.py"

BANNED_TOKENS = (
    "newton_loop", "policy_iteration", "semismooth", "trust_region",
    "continuation", "linesearch", "line_search", "armijo", "backtrack",
    "adaptive_alpha", "tune_alpha", "active_set", "clip", "floor",
    "spsolve_loop", "kfe", "stationary", "steady_state",
    "solve_household_steady_state", "sweep", "wmax", "results",
)


# ---------------------------------------------------------------------------
# fixtures
# ---------------------------------------------------------------------------
@pytest.fixture(scope="module")
def diag():
    """ONE full diagnostic plus its ONE deterministic repeat."""
    r, ident = m.run_issue68_diagnostic_twice()
    return r, ident


@pytest.fixture(scope="module")
def recon():
    """ONE independent accepted-state reconstruction for guard tests."""
    return reconstruct_issue63_stagnation_state()


# ---------------------------------------------------------------------------
# 1. exact post-repair V_* reconstruction
# ---------------------------------------------------------------------------
def test_reconstruction_exact(diag):
    r, _ = diag
    assert r.failure_detail is None
    assert r.iterations == m.RECONSTRUCT_STEPS == 8
    assert r.final_statistic == pytest.approx(m.FINAL_STATISTIC_EXPECTED, abs=1e-12)
    assert r.min_boundary_pb_star == pytest.approx(m.MIN_BOUNDARY_PB_EXPECTED,
                                                   abs=1e-12)
    assert r.wall_state["family"] == "F3"
    assert r.wall_state["j"] == 13 and r.wall_state["i"] == 13
    assert r.wall_state["z"] == 1
    assert r.wall_state["node"] == m.WALL_NODE


def test_selected_q_repaired_blob_exact():
    """The repaired selected-Q source must be byte-identical to the accepted blob."""
    import subprocess

    repo_root = Path(__file__).resolve().parents[1]
    out = subprocess.run(
        ["git", "rev-parse", f"HEAD:{SELECTED_Q_RELPATH}"],
        cwd=repo_root, capture_output=True, text=True, check=True)
    assert out.stdout.strip() == m.SELECTED_Q_REPAIRED_BLOB


# ---------------------------------------------------------------------------
# 2. exact R reproduction and ONE base operator build
# ---------------------------------------------------------------------------
def test_exact_r_reproduction(diag):
    r, _ = diag
    assert r.r_inf == pytest.approx(m.REPAIRED_R_INF, abs=1e-12)
    assert r.r_argmax is not None and r.r_argmax["family"] == "F0"
    assert r.r_inf > 0.0


def test_exactly_one_operator_build_and_one_newton_solve(recon):
    """Exactly ONE base final=False build and ONE Newton solve at V_*."""
    solver = recon["solver"]
    with patch.object(solver, "build_operator_and_u",
                      wraps=solver.build_operator_and_u) as spy:
        r = m._run_from_reconstruction(recon)
    finals = [c.kwargs.get("final") for c in spy.call_args_list]
    # 1 base build + 1 re-selection per trial (final=False) + 1 final=True per trial
    assert finals.count(False) == 3
    assert finals.count(True) == 2
    assert r.newton_solve_count == 1
    assert r.projection_count == 1
    assert r.crossing_computation_count == 1
    assert r.trial_count == 2


def test_newton_equation_residual(diag):
    r, _ = diag
    assert r.newton_lin_res_ok is True
    assert r.newton_lin_res_inf <= 1e-9
    assert r.newton_lin_res_inf > 0.0
    assert r.j_d_n_plus_r_inf == r.newton_lin_res_inf
    assert np.isfinite(r.d_n_inf) and r.d_n_inf > 0.0


# ---------------------------------------------------------------------------
# 3. accepted Issue #62 boundary derivative semantics
# ---------------------------------------------------------------------------
def test_official_gradient_is_two_entry_full_chain_rule(recon):
    """Issue #68 §4 frozen contract: g is the FULL-state gradient of the wall p_b.

    ``p_b = (V_wall - V_down)/db`` so the gradient has exactly two non-zero
    entries: ``+1/db`` at the wall state and ``-1/db`` at its backward
    neighbour. The single-entry ``+1/db`` variant is NOT the official
    construction.
    """
    solver = recon["solver"]
    n, db = solver.n, float(solver.db)
    gvec = m.limiting_wall_gradient(solver, m.WALL_NODE, m.WALL_NZ)
    wall_idx = m.WALL_NZ * n + m.WALL_NODE
    down_node = int(solver.grid.node_of[
        (int(solver.grid.j_arr[m.WALL_NODE]),
         int(solver.grid.i_arr[m.WALL_NODE]) - 1)])
    down_idx = m.WALL_NZ * n + down_node

    # exactly two non-zero entries, with the right signs and magnitudes
    support = np.nonzero(gvec)[0]
    assert support.size == 2
    assert set(int(s) for s in support) == {wall_idx, down_idx}
    assert float(gvec[wall_idx]) == 1.0 / db
    assert float(gvec[down_idx]) == -1.0 / db
    assert int(np.count_nonzero(gvec)) == 2
    # no other support anywhere in the state vector
    assert float(np.max(np.abs(np.delete(gvec, [wall_idx, down_idx])))) == 0.0
    assert np.isfinite(gvec).all()
    assert float(np.linalg.norm(gvec)) > 0.0


def test_official_gradient_basis_and_finite_difference_identity(recon):
    """The two-entry gradient must reproduce the accepted derivative map exactly.

    Basis check: mapping each ``e[j,z]`` through the accepted
    ``boundary_direction_matrix`` must give exactly ``g[j,z]`` at the wall
    coordinate. Finite-difference check: perturbing the wall coordinate must
    move ``p_b`` by ``eps/db`` and perturbing the backward neighbour by
    ``-eps/db``.
    """
    solver = recon["solver"]
    n, nz = solver.n, solver.nz
    db = float(solver.db)
    V_star, labor0 = recon["V_star"], recon["labor0"]
    gvec = m.limiting_wall_gradient(solver, m.WALL_NODE, m.WALL_NZ)

    # --- basis identity over the whole state space (exact)
    for j in (m.WALL_NODE, m.WALL_NODE - 1, m.WALL_NODE - 2, 97, 0):
        for z in range(nz):
            e = np.zeros((n, nz))
            e[j, z] = 1.0
            dp = boundary_direction_matrix(solver, e)
            assert float(dp[m.WALL_NODE, m.WALL_NZ]) == float(gvec[z * n + j])
    ok, err = m._gradient_basis_check(solver, m.WALL_NODE, m.WALL_NZ, gvec)
    assert ok is True
    assert err == 0.0

    # --- directional finite-difference identity on the wall coordinate
    _, pb, _, _ = solver.compute_derivatives(V_star, labor0, 0.0, 0.0)
    p0 = float(pb[m.WALL_NODE, m.WALL_NZ])
    eps = 1.0e-6
    down_node = int(solver.grid.node_of[
        (int(solver.grid.j_arr[m.WALL_NODE]),
         int(solver.grid.i_arr[m.WALL_NODE]) - 1)])
    for j, expected in ((m.WALL_NODE, 1.0 / db), (down_node, -1.0 / db)):
        Vp = V_star.copy()
        Vp[j, m.WALL_NZ] += eps
        _, pbp, _, _ = solver.compute_derivatives(Vp, labor0, 0.0, 0.0)
        fd = (float(pbp[m.WALL_NODE, m.WALL_NZ]) - p0) / eps
        assert fd == pytest.approx(expected, rel=1e-6)


def test_single_entry_gradient_rejected_as_official(recon):
    """The superseded single-entry variant must NOT satisfy the official contract."""
    solver = recon["solver"]
    n = solver.n
    db = float(solver.db)
    g1 = m.single_entry_debug_gradient(solver, m.WALL_NODE, m.WALL_NZ)
    g2 = m.limiting_wall_gradient(solver, m.WALL_NODE, m.WALL_NZ)
    # it has only one non-zero entry ...
    assert int(np.count_nonzero(g1)) == 1
    # ... and it FAILS the basis identity at the backward neighbour
    ok1, err1 = m._gradient_basis_check(solver, m.WALL_NODE, m.WALL_NZ, g1)
    ok2, err2 = m._gradient_basis_check(solver, m.WALL_NODE, m.WALL_NZ, g2)
    assert ok1 is False
    assert err1 == pytest.approx(1.0 / db, rel=1e-12)
    assert ok2 is True and err2 == 0.0
    # documented as debug-only in the module
    src = MODULE_SOURCE.lower()
    assert "historical/debug only" in src
    assert "debug_gradient" in src


def test_i0_boundary_derivative_exactly_zero(recon):
    """Accepted semantics: i==0 boundary states are V-independent -> exactly 0."""
    solver = recon["solver"]
    g = solver.grid
    i0_nodes = [node for node in range(solver.n)
                if int(g.i_arr[node]) == 0
                and str(g.families[node]) != "F0"]
    assert i0_nodes, "expected i==0 boundary states in the frozen case"
    for node in i0_nodes:
        gvec = m.limiting_wall_gradient(solver, node, 0)
        assert np.all(gvec == 0.0)
    # and the directional matrix agrees for a non-trivial direction
    d = np.linspace(0.5, 1.5, solver.state_size)
    dp = boundary_direction_matrix(
        solver, d.reshape((solver.n, solver.nz), order="F"))
    for node in i0_nodes:
        for z in range(solver.nz):
            assert float(dp[node, z]) == 0.0


def test_zero_derivative_count_matches_i0_rule(diag, recon):
    """Every i==0 boundary state has exactly zero directional derivative."""
    r, _ = diag
    solver = recon["solver"]
    g = solver.grid
    i0_count = sum(
        1 for node in range(solver.n) if str(g.families[node]) != "F0"
        for _ in range(solver.nz) if int(g.i_arr[node]) == 0)
    assert i0_count == 40
    assert r.required_boundary_count == 186
    # the i==0 states are a subset of the exactly-zero-derivative states (the
    # corrected projection may also produce an exact zero on a regular state)
    assert r.zero_derivative_count >= i0_count
    assert r.zero_derivative_count == 41


# ---------------------------------------------------------------------------
# 4. limiting-wall gradient requirements
# ---------------------------------------------------------------------------
def test_gradient_finite_nonzero_and_points_through_wall(diag):
    r, _ = diag
    assert r.gradient_finite is True
    assert r.gradient_nonzero is True
    assert r.gradient_norm2 > 0.0
    assert np.isfinite(r.gradient_norm2)
    assert r.g_dot_d_n < 0.0
    assert r.g_dot_d_n_negative is True


def test_gradient_diagnostics_recorded(diag):
    r, _ = diag
    assert r.gradient_kind == "full_state_chain_rule_two_entry"
    assert r.gradient_nonzero_count == 2
    assert r.gradient_wall_state_index == m.WALL_NZ * 391 + m.WALL_NODE
    assert r.gradient_down_state_index == m.WALL_NZ * 391 + (m.WALL_NODE - 1)
    assert r.gradient_wall_entry == pytest.approx(2.7142857142857144, rel=1e-15)
    assert r.gradient_down_entry == pytest.approx(-2.7142857142857144, rel=1e-15)
    assert r.gradient_wall_entry == -r.gradient_down_entry
    assert set(r.gradient_support) == {r.gradient_wall_state_index,
                                       r.gradient_down_state_index}
    assert r.gradient_basis_check_ok is True
    assert r.gradient_basis_check_max_abs_err == 0.0
    assert r.gradient_finite is True
    assert r.gradient_nonzero is True
    assert np.isfinite(r.gradient_norm2) and r.gradient_norm2 > 0.0


def test_official_trials_use_corrected_full_gradient_direction(diag, recon):
    """The official trial residuals must come from the TWO-ENTRY projection.

    The corrected projection removes only the tiny two-entry normal component
    ``g@d_N = -2.58e-05``, so the official direction stays within ~4.7e-06 of the
    plain Newton direction. This test therefore verifies the direction
    identity directly (recomputing the official trial state and residual from
    the frozen closed form) plus the gradient support, rather than trying to
    separate two nearly identical directions by residual magnitude.
    """
    r, _ = diag
    solver = recon["solver"]
    n, nz, S = solver.n, solver.nz, solver.state_size
    V_star, labor0, rho = recon["V_star"], recon["labor0"], recon["rho"]
    V_flat = V_star.ravel(order="F")
    Q, u, _d, _recs = solver.build_operator_and_u(
        V_star, labor0, 0.0, 0.0, final=False)
    R = rho * V_flat - (u + Q.dot(V_flat))
    J = rho * sparse.eye(S, format="csr") - Q
    from scipy.sparse import linalg
    d_n = linalg.spsolve(J, -R)

    g2 = m.limiting_wall_gradient(solver, m.WALL_NODE, m.WALL_NZ)
    g1 = m.single_entry_debug_gradient(solver, m.WALL_NODE, m.WALL_NZ)
    proj = m.single_wall_tangent_projection(d_n, g2)
    d_t2 = proj["d_T"]
    d_t1 = m.single_wall_tangent_projection(d_n, g1)["d_T"]

    # the corrected projection only removes the (tiny) two-entry normal part
    assert float(np.max(np.abs(d_t2 - d_n))) < 1.0e-4
    assert float(np.max(np.abs(d_t1 - d_n))) > 1.0
    assert float(np.max(np.abs(d_t2 - d_t1))) > 1.0
    assert proj["g_dot_d_t"] == 0.0

    # the official projected direction reproduces the reported d_T metrics
    assert float(np.max(np.abs(d_t2))) == pytest.approx(r.d_t_inf, rel=1e-12)
    assert float(np.max(np.abs(d_t2 - d_n))) == pytest.approx(
        r.d_t_minus_d_n_inf, rel=1e-12)
    assert float(g2 @ d_n) == pytest.approx(r.g_dot_d_n, rel=1e-12)

    # recomputing each official trial residual from the frozen closed form
    # reproduces the reported official ratios exactly
    for t in r.trials:
        assert t.alpha in (r.alpha_half, r.alpha_near)
        Vt = V_star + t.alpha * d_t2.reshape((n, nz), order="F")
        Vtf = Vt.ravel(order="F")
        Qr, ur, _dr, _rs = solver.build_operator_and_u(
            Vt, labor0, 0.0, 0.0, final=False)
        Rr = rho * Vtf - (ur + Qr.dot(Vtf))
        ratio = float(np.max(np.abs(Rr))) / r.r_inf
        assert ratio == pytest.approx(t.reselect_ratio, rel=1e-12)


def test_superseded_single_entry_result_does_not_feed_classification(diag):
    """The stale single-entry diagnostic must not influence the terminal."""
    r, _ = diag
    # the official crossing is the corrected value, not the stale one
    assert r.alpha_cross_t == pytest.approx(
        CORRECTED_ALPHA_CROSS_T_EXPECTED, rel=1e-12)
    assert abs(r.alpha_cross_t
               - SUPERSEDED_SINGLE_ENTRY_ALPHA_CROSS_T) > 0.1
    # the official alpha fractions follow from the corrected crossing
    assert r.alpha_near == pytest.approx(
        min(1.0, (1.0 - m.EPS_ALPHA) * CORRECTED_ALPHA_CROSS_T_EXPECTED),
        rel=1e-12)
    # official trial alphas are the corrected ones
    assert sorted(t.alpha for t in r.trials) == sorted(
        [r.alpha_half, r.alpha_near])
    assert r.alpha_half == pytest.approx(0.08085341880193442, rel=1e-12)
    assert r.alpha_near == pytest.approx(0.16170683760386884, rel=1e-12)
    # the official geometry ratio is the corrected one
    assert r.geometry_improvement_ratio == pytest.approx(
        866.2532997045214, rel=1e-9)
    # and the terminal classification is deterministic
    assert r.terminal == m.TERMINAL_C
    assert r.deterministic_repeat_identical is True


def test_plain_newton_historical_baseline_reproduced(diag):
    r, _ = diag
    assert r.alpha_cross_n is not None
    assert r.alpha_cross_n == pytest.approx(
        m.ALPHA_CROSS_N_HISTORICAL, rel=1e-9)
    assert r.alpha_cross_n_reproduced is True
    assert r.alpha_cross_n_state["family"] == "F3"
    assert r.alpha_cross_n_state["node"] == m.WALL_NODE
    assert r.alpha_cross_n_state["z"] == 1


# ---------------------------------------------------------------------------
# 5. tangent projection
# ---------------------------------------------------------------------------
def test_tangent_identity_holds(diag):
    r, _ = diag
    assert r.tangent_identity_ok is True
    assert abs(r.g_dot_d_t) <= m.TANGENT_TOL
    assert abs(r.g_dot_d_t) == 0.0
    assert np.isfinite(r.d_t_inf)
    assert np.isfinite(r.d_t_minus_d_n_inf)
    assert r.d_t_inf > 0.0
    assert r.d_t_minus_d_n_inf > 0.0


def test_projection_formula_exact(diag, recon):
    """d_T must equal the frozen closed-form projection of d_N."""
    r, _ = diag
    solver = recon["solver"]
    Q, u, _d, _recs = solver.build_operator_and_u(
        recon["V_star"], recon["labor0"], 0.0, 0.0, final=False)
    V_flat = recon["V_star"].ravel(order="F")
    R = recon["rho"] * V_flat - (u + Q.dot(V_flat))
    S = solver.state_size
    J = recon["rho"] * sparse.eye(S, format="csr") - Q
    from scipy.sparse import linalg
    d_n = linalg.spsolve(J, -R)
    gvec = m.limiting_wall_gradient(solver, m.WALL_NODE, m.WALL_NZ)
    d_t = d_n - gvec * (float(gvec @ d_n) / float(gvec @ gvec))
    assert float(np.max(np.abs(d_t))) == pytest.approx(r.d_t_inf, rel=1e-12)
    assert float(np.max(np.abs(d_t - d_n))) == pytest.approx(
        r.d_t_minus_d_n_inf, rel=1e-12)
    # the projection reduces the normal component to exactly zero
    assert float(gvec @ d_t) == r.g_dot_d_t
    # linear residual effect: projection strictly enlarges ||J d + R||
    assert r.j_d_t_plus_r_inf > r.j_d_n_plus_r_inf


def test_no_multiple_constraints_or_metric_optimization():
    """Static scan: exactly ONE projection, no active-set / QP machinery."""
    tree = ast.parse(MODULE_SOURCE)
    calls = [n for n in ast.walk(tree)
             if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
             and n.func.id == "single_wall_tangent_projection"]
    assert len(calls) == 1
    for banned in ("minimize", "linprog", "quadprog", "solve_qp", "cvxopt"):
        assert banned not in MODULE_SOURCE.lower()


# ---------------------------------------------------------------------------
# 6. all-boundary crossing geometry
# ---------------------------------------------------------------------------
def test_all_boundary_crossing_deterministic_and_positive(diag):
    r, _ = diag
    assert r.crossing_computation_count == 1
    assert r.has_positive_safe_fraction is True
    assert r.alpha_cross_t is not None
    assert np.isfinite(r.alpha_cross_t) and r.alpha_cross_t > 0.0
    assert r.alpha_cross_t_state is not None
    assert r.alpha_cross_t_state["family"] == "F3"
    assert r.alpha_cross_t_state["z"] == 1
    assert r.negative_derivative_count > 0
    # OFFICIAL corrected full-gradient crossing (freshly recomputed)
    assert r.alpha_cross_t == pytest.approx(
        CORRECTED_ALPHA_CROSS_T_EXPECTED, rel=1e-12)
    # the superseded single-entry value must NOT be reused
    assert r.alpha_cross_t != pytest.approx(
        SUPERSEDED_SINGLE_ENTRY_ALPHA_CROSS_T, rel=1e-3)


def test_exact_alpha_formulas(diag):
    r, _ = diag
    expected_near = min(1.0, (1.0 - m.EPS_ALPHA) * r.alpha_cross_t)
    assert r.alpha_near == pytest.approx(expected_near, rel=1e-15)
    assert r.alpha_half == pytest.approx(m.HALF_ALPHA * r.alpha_near, rel=1e-15)
    assert r.alpha_half < r.alpha_near
    assert r.alpha_near <= 1.0


def test_no_adaptive_alpha_search(diag):
    """Only the two frozen fractions may appear; no tuning / line search."""
    r, _ = diag
    alphas = sorted(t.alpha for t in r.trials)
    assert alphas == sorted([r.alpha_half, r.alpha_near])
    assert len(set(alphas)) == 2
    # the fractions are the exact frozen formulas, not searched values
    assert r.alpha_half == m.HALF_ALPHA * r.alpha_near
    assert r.trial_count == 2
    for banned in ("minimize_scalar", "brentq", "golden", "fmin"):
        assert banned not in MODULE_SOURCE


def test_exactly_two_trial_states_with_frozen_labels(diag):
    r, _ = diag
    assert r.trial_count == 2
    assert [t.label for t in r.trials] == list(m.TRIAL_ORDER)
    assert {t.label for t in r.trials} == {"alpha_half", "alpha_near"}
    for t in r.trials:
        assert t.accepted_as_hjb_iterate is False
    assert r.accepted_new_hjb_iterate is False


def test_geometry_improving_criterion(diag):
    r, _ = diag
    assert r.geometry_improvement_ratio is not None
    expected = r.alpha_near / min(1.0, r.alpha_cross_n)
    assert r.geometry_improvement_ratio == pytest.approx(expected, rel=1e-12)
    assert r.geometry_improving is (
        r.geometry_improvement_ratio >= m.GEOMETRY_IMPROVEMENT_FACTOR)
    assert r.geometry_improvement_ratio >= 10.0
    assert r.geometry_improving is True


# ---------------------------------------------------------------------------
# 7. the two trials: strict safety, one re-selection, one final build each
# ---------------------------------------------------------------------------
def test_strict_boundary_safety_at_both_trials(diag):
    r, _ = diag
    assert r.all_trials_domain_safe is True
    for t in r.trials:
        assert t.domain_safe is True
        assert np.isfinite(t.min_boundary_pb)
        assert t.min_boundary_pb > PB_MARGIN
        assert t.min_boundary_pb_state is not None


def test_final_vs_iteration_equivalence_at_each_trial(diag):
    """CORRECTED-PROJECTION FINDING: the two operators are NOT equivalent.

    At the corrected full-gradient trial states the re-selected ``final=False``
    and corrected ``final=True`` operators disagree on a small number of F0
    rows (the re-selection path uses the accepted policy's ``iteration_*`` rates
    while the corrected final path recomputes raw drifts). This is asserted as
    the recorded factual outcome, and is the frozen Outcome C condition.
    """
    r, _ = diag
    for t in r.trials:
        assert t.final_vs_iter_equivalent is False
        assert t.final_vs_iter_f0_rowwise_gap > m.EQUIVALENCE_TOL
        assert t.final_vs_iter_inconsistent_row_count > 0
        assert len(t.final_vs_iter_inconsistent_rows) == (
            t.final_vs_iter_inconsistent_row_count)
        # every affected row is an F0 row in the z=1 block
        for row in t.final_vs_iter_inconsistent_rows:
            assert 391 <= row < 782
        # the corrected final and reselected residuals still coincide
        assert t.r_final_trial_inf == pytest.approx(t.r_reselect_inf, rel=1e-12)
    assert r.all_trials_operator_equivalent is False


def test_one_reselection_and_one_final_build_per_trial(recon):
    """Each trial must perform exactly ONE final=False and ONE final=True build."""
    solver = recon["solver"]
    seen: list[dict] = []
    real = solver.build_operator_and_u

    def counting(V, labor0v, ti, brg, final=False, f0_policies=None):
        seen.append({"final": final})
        return real(V, labor0v, ti, brg, final=final, f0_policies=f0_policies)

    with patch.object(solver, "build_operator_and_u", side_effect=counting):
        r = m._run_from_reconstruction(recon)
    assert len(seen) == 5                     # 1 base + 2 per trial
    assert sum(1 for c in seen if c["final"] is False) == 3
    assert sum(1 for c in seen if c["final"] is True) == 2
    assert r.trial_count == 2


def test_trial_diagnostics_recorded(diag):
    r, _ = diag
    for t in r.trials:
        assert np.isfinite(t.r_frozen_inf)
        assert np.isfinite(t.r_reselect_inf)
        assert np.isfinite(t.r_final_trial_inf)
        assert np.isfinite(t.reselect_ratio) and t.reselect_ratio > 0.0
        assert np.isfinite(t.final_ratio) and t.final_ratio > 0.0
        assert t.reselect_ratio == pytest.approx(
            t.r_reselect_inf / r.r_inf, rel=1e-15)
        assert t.final_ratio == pytest.approx(
            t.r_final_trial_inf / r.r_inf, rel=1e-15)
        assert np.isfinite(t.max_abs_q1_reselect)
        assert np.isfinite(t.max_abs_q1_final)
        assert t.label_change_count >= 0
        for nm in ("max_abs_delta_consumption", "max_abs_delta_labor",
                   "max_abs_delta_transfer", "max_abs_delta_mu_a",
                   "max_abs_delta_mu_b", "max_abs_delta_utility"):
            assert np.isfinite(getattr(t, nm))
            assert getattr(t, nm) > 0.0


def test_material_reduction_flag_matches_frozen_rule(diag):
    r, _ = diag
    for t in r.trials:
        expected = bool(t.reselect_ratio <= m.MATERIAL_REDUCTION_RATIO
                        and t.final_ratio <= m.MATERIAL_REDUCTION_RATIO)
        assert t.material_residual_reducing is expected
    assert r.any_trial_materially_reducing is any(
        t.material_residual_reducing for t in r.trials)


def test_conservativity_preserved_at_trials(diag):
    r, _ = diag
    for t in r.trials:
        assert t.max_abs_q1_reselect <= 1e-9
        assert t.max_abs_q1_final <= 1e-9
        assert t.max_abs_q1_reselect == pytest.approx(t.max_abs_q1_final,
                                                      abs=1e-15)


def test_sector_label_switching_recorded(diag):
    """Recorded diagnostic: label switches grow with the corrected fraction.

    Zero label changes at ``alpha_half`` and two at ``alpha_near``. A zero
    label-switch count must NOT be read as unchanged continuous controls — the
    continuous-control maxima below are non-zero at both trials.
    """
    r, _ = diag
    by_label = {t.label: t for t in r.trials}
    assert by_label["alpha_half"].label_change_count == 0
    assert by_label["alpha_near"].label_change_count == 2
    for t in r.trials:
        assert t.max_abs_delta_consumption > 0.0
        assert t.max_abs_delta_labor > 0.0
        assert t.max_abs_delta_mu_b > 0.0


# ---------------------------------------------------------------------------
# 8. deterministic repeat / terminal / fail-closed
# ---------------------------------------------------------------------------
def test_deterministic_repeat_identical(diag):
    r, ident = diag
    assert ident is True
    assert r.deterministic_repeat_identical is True


def test_exactly_one_terminal_returned(diag):
    r, _ = diag
    assert r.terminal == m.TERMINAL_C
    assert r.terminal != m.TERMINAL_A
    assert r.terminal != m.TERMINAL_B
    assert r.terminal != m.TERMINAL_BLOCKED
    assert [r.terminal == t for t in (m.TERMINAL_A, m.TERMINAL_B,
                                      m.TERMINAL_C)].count(True) == 1


def test_terminal_rule_is_the_frozen_rule(diag):
    """Outcome C must follow from the frozen consistency criteria.

    The corrected full-gradient geometry is finite, has an exact tangent
    identity and both trials are domain-safe, but the corrected ``final=True``
    and re-selected ``final=False`` operators are NOT equivalent at the trial
    states, which is the frozen Outcome C condition
    ("corrected-final vs iteration inconsistency").
    """
    r, _ = diag
    assert r.failure_detail is None
    assert r.tangent_identity_ok is True
    assert r.has_positive_safe_fraction is True
    assert r.all_trials_domain_safe is True
    assert r.geometry_improving is True
    # the disqualifying condition
    assert r.all_trials_operator_equivalent is False
    for t in r.trials:
        assert t.final_vs_iter_equivalent is False
        assert t.final_vs_iter_f0_rowwise_gap > m.EQUIVALENCE_TOL
    assert [r.terminal == t for t in (m.TERMINAL_A, m.TERMINAL_B,
                                      m.TERMINAL_C)].count(True) == 1
    assert r.terminal == m.TERMINAL_C


def test_trial_operator_inconsistency_recorded_precisely(diag):
    r, _ = diag
    assert r.all_trials_operator_equivalent is False
    assert r.trials[0].final_vs_iter_inconsistent_row_count == 2
    assert r.trials[0].final_vs_iter_inconsistent_rows == (452, 453)
    assert r.trials[0].final_vs_iter_f0_rowwise_gap == pytest.approx(
        0.6718037653783657, rel=1e-9)
    assert r.trials[1].final_vs_iter_inconsistent_row_count == 4
    assert r.trials[1].final_vs_iter_inconsistent_rows == (452, 453, 482, 483)
    assert r.trials[1].final_vs_iter_f0_rowwise_gap == pytest.approx(
        1.3379411925537439, rel=1e-9)


def test_no_hjb_convergence_claimed(diag):
    """The diagnostic never claims convergence or accepts an iterate."""
    r, _ = diag
    assert r.accepted_new_hjb_iterate is False
    for t in r.trials:
        assert t.accepted_as_hjb_iterate is False
        # no trial ratio approaches a convergence threshold
        assert t.reselect_ratio > m.MATERIAL_REDUCTION_RATIO
        assert t.final_ratio > m.MATERIAL_REDUCTION_RATIO


def test_fail_closed_on_nonfinite_direction(recon):
    solver = recon["solver"]
    bad = np.full(solver.state_size, np.nan)
    gvec = m.limiting_wall_gradient(solver, m.WALL_NODE, m.WALL_NZ)
    with pytest.raises(m.TangentProjectedNewtonFailure):
        m.single_wall_tangent_projection(bad, gvec)


def test_fail_closed_on_degenerate_gradient():
    d_n = np.ones(10)
    with pytest.raises(m.TangentProjectedNewtonFailure):
        m.single_wall_tangent_projection(d_n, np.zeros(10))


def test_fail_closed_on_boundary_safety_violation(recon):
    """A trial that would cross the margin must fail closed, not pass."""
    solver = recon["solver"]
    n, nz = solver.n, solver.nz
    V_star, labor0, rho = recon["V_star"], recon["labor0"], recon["rho"]
    Q, u, _d, recs = solver.build_operator_and_u(
        V_star, labor0, 0.0, 0.0, final=False)
    V_flat = V_star.ravel(order="F")
    R = rho * V_flat - (u + Q.dot(V_flat))
    S = solver.state_size
    J = rho * sparse.eye(S, format="csr") - Q
    from scipy.sparse import linalg
    d_n = linalg.spsolve(J, -R)
    with pytest.raises(m.TangentProjectedNewtonFailure):
        # an enormous fraction along d_N must leave the effective domain
        m.evaluate_tangent_trial(solver, V_star, labor0, rho, d_n, Q, u, recs,
                                 10.435094313164921, "forced_violation", 5.0)


# ---------------------------------------------------------------------------
# 9. forbidden machinery
# ---------------------------------------------------------------------------
def test_no_forbidden_iteration_machinery_static():
    tree = ast.parse(MODULE_SOURCE)
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            tok = node.id.lower()
            if any(b in tok for b in BANNED_TOKENS):
                found.append((tok, getattr(node, "lineno", -1)))
        elif isinstance(node, ast.Attribute):
            tok = node.attr.lower()
            if any(b in tok for b in BANNED_TOKENS):
                found.append((tok, getattr(node, "lineno", -1)))
    assert found == [], f"forbidden tokens found: {found}"
    # exactly ONE linalg.spsolve call (the ONE Newton solve)
    solves = [n for n in ast.walk(tree)
              if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
              and n.func.attr == "spsolve"]
    assert len(solves) == 1
    # exactly THREE operator builds in the module (1 base + 2 re-selections)
    builds = [n for n in ast.walk(tree)
              if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
              and n.func.attr == "build_operator_and_u"]
    assert len(builds) == 3
    assert (MODULE_SOURCE.count("final=True") >= 1)
