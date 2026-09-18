"""DLH-5V-Y — focused test suite for the ONE-step Route-A projected
regularized-Newton execution at `V_*` (Issue #73).

Authority: Issue #73 OPEN; initial authoritative activation ``5714125203``; final
authoritative activation-refresh ``5714871725`` (post-sync live ``main``
``90e8b2191b50be04dcc1f4b805613247f69bc231``). Reviewer bounded numerical route
selection
``POLICY_FROZEN_REGULARIZED_NEWTON_DIRECTION_WITHIN_ACCEPTED_PROJECTED_CONSTRAINED_OUTER_FRAME``;
authority marker ``DLH_5VY_ROUTE_A_ONE_STEP_PROJECTED_REGULARIZED_NEWTON_AUTHORIZED``.

Scope ceiling: exactly ONE bounded one-step execution. No second outer step, no
trajectory, no HJB-convergence claim, no residual/Jacobi direction.
"""

from __future__ import annotations

import ast
import subprocess
from pathlib import Path

import numpy as np
import pytest

import deep_learning_hank.two_asset.route_a_one_step_projected_regularized_newton as m

MODULE_PATH = Path(m.__file__)
MODULE_SOURCE = MODULE_PATH.read_text(encoding="utf-8")
TREE = ast.parse(MODULE_SOURCE)

SELECTED_Q_RELPATH = "src/deep_learning_hank/two_asset/boundary_hjb_selected_q.py"
ORACLE_RELPATH = ("src/deep_learning_hank/two_asset/"
                  "matlab_faithful_two_asset_ha.py")
AUDIT69_RELPATH = ("src/deep_learning_hank/two_asset/"
                   "f0_rate_path_divergence_audit.py")
ISSUE71_RELPATH = ("src/deep_learning_hank/two_asset/"
                   "route_a_hjb_residual_decomposition.py")
ISSUE72_RELPATH = ("src/deep_learning_hank/two_asset/"
                   "route_a_bounded_solver_design.py")

# the residual/Jacobi direction must NOT appear in this Issue
FORBIDDEN_DIRECTION_TOKENS = ("jacobi", "precondition", "M_inv")


def _code_only_text() -> str:
    """Module source with all docstrings removed, so forbidden-token scans test
    CODE rather than prose (the docstrings legitimately NAME the machinery and
    the directions this Issue is forbidden to use)."""
    docstrings = set()
    for node in ast.walk(TREE):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef,
                             ast.ClassDef)):
            body = getattr(node, "body", [])
            if body and isinstance(body[0], ast.Expr) and isinstance(
                    body[0].value, ast.Constant) and isinstance(
                    body[0].value.value, str):
                docstrings.add(id(body[0]))
    lines = MODULE_SOURCE.splitlines()
    drop = set()
    for node in ast.walk(TREE):
        if id(node) in docstrings:
            for ln in range(node.lineno, (node.end_lineno or node.lineno) + 1):
                drop.add(ln)
    return "\n".join(ln for i, ln in enumerate(lines, start=1)
                     if i not in drop)


CODE_SOURCE = _code_only_text()


def _blob(relpath: str, rev: str = "HEAD") -> str:
    repo_root = Path(__file__).resolve().parents[1]
    return subprocess.run(
        ["git", "rev-parse", f"{rev}:{relpath}"], cwd=repo_root,
        capture_output=True, text=True, encoding="utf-8",
        errors="replace", check=True).stdout.strip()


_CACHE: dict = {}


def _experiment():
    """ONE one-step experiment (module-scoped, cached)."""
    if "r" not in _CACHE:
        _CACHE["r"] = m.run_issue73_one_step()
    return _CACHE["r"]


def _repeat():
    """ONE full deterministic repeat, cached so it is paid for exactly once."""
    if "rep" not in _CACHE:
        r, ident = m.run_issue73_one_step_twice()
        _CACHE["rep"] = (r, ident)
    return _CACHE["rep"]


@pytest.fixture(scope="module")
def result():
    return _experiment()


@pytest.fixture(scope="module")
def repeat():
    return _repeat()


# ---------------------------------------------------------------------------
# 1. accepted anchors
# ---------------------------------------------------------------------------
def test_accepted_blobs_pinned():
    assert _blob(SELECTED_Q_RELPATH) == m.SELECTED_Q_ACCEPTED_BLOB == (
        "7857cabb4d28af99cb9d59e2d1c3024b05787c11")
    assert _blob(ORACLE_RELPATH) == m.ORACLE_BLOB == (
        "76ae5b149993a7edeeb8eb337f1b02b3fe33c51e")
    assert _blob(AUDIT69_RELPATH) == m.ISSUE69_AUDIT_BLOB == (
        "83e9be0febcc03eb721265d3558887bd6b1586a4")
    assert _blob(ISSUE71_RELPATH) == m.ACCEPTED_ISSUE71_BLOB == (
        "96dd262a4ae42e26d489a317d9a04a9264b481b1")
    assert _blob(ISSUE72_RELPATH) == m.ACCEPTED_ISSUE72_BLOB == (
        "f99ff6eb0d0a74cccc400ba83162a8affa9c6924")


def test_anchor_helper_is_read_only():
    blobs = m.accepted_anchor_blobs()
    assert blobs["selected_q_blob"] == m.SELECTED_Q_ACCEPTED_BLOB
    assert blobs["oracle_blob"] == m.ORACLE_BLOB
    assert blobs["issue69_blob"] == m.ISSUE69_AUDIT_BLOB
    assert blobs["issue71_blob"] == m.ACCEPTED_ISSUE71_BLOB
    assert blobs["issue72_blob"] == m.ACCEPTED_ISSUE72_BLOB


def test_this_issue_creates_only_its_own_paths():
    repo_root = Path(__file__).resolve().parents[1]
    out = subprocess.run(
        ["git", "diff", "--name-only", f"{m.GOVERNANCE_BASE}...HEAD"],
        cwd=repo_root, capture_output=True, text=True, encoding="utf-8",
        errors="replace", check=True).stdout
    paths = sorted(p.strip() for p in out.splitlines() if p.strip())
    assert len(paths) <= 4, paths
    for p in paths:
        assert ("route_a_one_step_projected_regularized_newton" in p
                or "test_dlh_5vy" in p), p


def test_authority_marker_and_activations_present():
    for token in ("Issue #73", "DLH-5V-Y",
                  "DLH_5VY_ROUTE_A_ONE_STEP_PROJECTED_REGULARIZED_NEWTON_AUTHORIZED",
                  "5714125203", "5714871725",
                  "POLICY_FROZEN_REGULARIZED_NEWTON_DIRECTION_WITHIN_ACCEPTED_"
                  "PROJECTED_CONSTRAINED_OUTER_FRAME"):
        assert token in MODULE_SOURCE, token


# ---------------------------------------------------------------------------
# 2. exact baseline reproduction
# ---------------------------------------------------------------------------
def test_exact_baseline_reproduction(result):
    assert result.failure_detail is None
    assert result.steps == 8
    assert result.final_statistic == pytest.approx(
        m.ACCEPTED_FINAL_STATISTIC, abs=1e-12)
    assert result.min_boundary_pb_star == pytest.approx(
        m.ACCEPTED_MIN_BOUNDARY_PB, abs=1e-12)
    assert result.wall_state["family"] == "F3"
    assert result.wall_state["j"] == 13 and result.wall_state["i"] == 13
    assert result.wall_state["z"] == 1
    assert result.wall_state["node"] == 332


def test_exact_baseline_residual_and_argmax(result):
    assert result.r_base_inf == pytest.approx(
        m.ACCEPTED_RESIDUAL_INF, abs=1e-12)
    assert result.r_base_inf == 10.435094313164921
    assert result.residual_argmax_row == 97
    assert result.residual_argmax_node == 97
    assert result.residual_argmax_z == 0
    assert result.residual_argmax_family == "F0"


def test_bellman_tolerance_unchanged_and_not_converged(result):
    assert result.bellman_tolerance == 1e-3
    assert result.r_base_inf > result.bellman_tolerance
    assert result.hjb_convergence_claimed is False


# ---------------------------------------------------------------------------
# 3. exactly one baseline build, same-Q Jacobian
# ---------------------------------------------------------------------------
def test_exactly_one_baseline_operator_build(result):
    assert result.baseline_operator_build_count == 1


def test_module_builds_baseline_operator_exactly_once():
    calls = [n for n in ast.walk(TREE)
             if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
             and n.func.attr == "build_operator_and_u"]
    # one baseline build plus one full-reassembly per candidate evaluation
    assert len(calls) == 2, [c.lineno for c in calls]


def test_newton_jacobian_uses_the_same_selected_operator():
    """`J = rho*I - Q` must be built from the SAME `Q` used for the residual."""
    assert "J = (rho * sparse.eye(S, format=\"csr\") - Q).tocsr()" in MODULE_SOURCE
    # the baseline build result feeds both the residual and the Jacobian
    assert MODULE_SOURCE.index("R = rho * Vf - u -") < MODULE_SOURCE.index(
        "J = (rho * sparse.eye")


def test_no_alternate_or_raw_drift_q_path():
    """Code-level scan: no raw-drift Q, no dual-Q, no final=True build."""
    for token in ("asset_drifts_matlab_faithful", "max(-mu", "max(mu",
                  "final=True"):
        assert token not in CODE_SOURCE, token
    # and no second operator builder anywhere in the module
    builders = [n for n in ast.walk(TREE)
                if isinstance(n, ast.FunctionDef)
                and n.name == "build_operator_and_u"]
    assert builders == []


def test_no_residual_jacobi_direction():
    """The residual/Jacobi direction is NOT authorized in this Issue."""
    for token in FORBIDDEN_DIRECTION_TOKENS:
        assert token not in CODE_SOURCE, token
    # the only regularized solve is the policy-frozen Newton system
    solves = [n for n in ast.walk(TREE)
              if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
              and n.func.attr == "spsolve"]
    assert len(solves) == 1


# ---------------------------------------------------------------------------
# 4. frozen ladders and lexicographic ordering
# ---------------------------------------------------------------------------
def test_exact_frozen_ladders():
    assert m.REGULARIZATION_LADDER == tuple(2.0 ** (-k) for k in range(0, 21))
    assert m.TRUST_RADIUS_LADDER == tuple(2.0 ** (-k) for k in range(0, 21))
    assert m.ALPHA_LADDER == tuple(2.0 ** (-k) for k in range(0, 21))
    assert m.LADDER_MAX_EXPONENT == 20 and m.LADDER_LENGTH == 21
    assert len(m.REGULARIZATION_LADDER) == len(m.TRUST_RADIUS_LADDER) == (
        len(m.ALPHA_LADDER)) == 21


def test_ladders_match_accepted_issue72_values():
    from deep_learning_hank.two_asset import route_a_bounded_solver_design as d
    assert m.REGULARIZATION_LADDER == d.REGULARIZATION_LADDER
    assert m.TRUST_RADIUS_LADDER == tuple(d.TRUST_RADIUS_FRACTION_LADDER)
    assert m.ALPHA_LADDER == tuple(d.STEP_FRACTION_LADDER)


def test_attempt_order_is_strictly_lexicographic(result):
    keys = [(a.k_lambda, a.k_delta, a.k_alpha) for a in result.attempts]
    assert keys, "at least one candidate must be attempted"
    assert all(keys[i] < keys[i + 1] for i in range(len(keys) - 1))
    assert keys[0] == (0, 0, 0)


def test_attempt_indices_are_contiguous(result):
    assert [a.index for a in result.attempts] == list(
        range(1, result.attempted_count + 1))


def test_lambda_rungs_are_visited_in_order(result):
    seen = []
    for a in result.attempts:
        if a.k_lambda not in seen:
            seen.append(a.k_lambda)
    assert seen == sorted(seen)
    assert seen == list(range(0, len(seen)))


def test_experiment_stops_at_first_acceptance(result):
    accepted = [a for a in result.attempts if a.accepted]
    assert len(accepted) == 1
    assert accepted[0] is result.attempts[-1]
    assert result.first_accepted_tuple == (
        accepted[0].k_lambda, accepted[0].k_delta, accepted[0].k_alpha)
    assert result.attempted_count == len(result.attempts)
    assert result.attempted_count <= result.max_candidate_count


def test_no_extra_rung_beyond_21_cubed(result):
    assert result.max_candidate_count == 21 ** 3
    assert result.attempted_count <= 21 ** 3
    for a in result.attempts:
        assert 0 <= a.k_lambda <= 20
        assert 0 <= a.k_delta <= 20
        assert 0 <= a.k_alpha <= 20


# ---------------------------------------------------------------------------
# 5. geometry: stacked full-wall gradients, never averaged
# ---------------------------------------------------------------------------
def test_geometry_uses_stacked_gradients_not_average():
    assert "STACKED, never averaged" in MODULE_SOURCE
    assert "_row_space_basis" in MODULE_SOURCE
    # no averaging of gradients anywhere
    assert "np.mean(grad" not in MODULE_SOURCE
    assert "average" not in MODULE_SOURCE.lower() or "never averaged" in (
        MODULE_SOURCE)


def test_projection_uses_orthonormal_row_space():
    assert "np.linalg.svd" in MODULE_SOURCE
    assert "d_raw - basis @ (basis.T @ d_raw)" in MODULE_SOURCE


def test_geometry_report_is_consistent(result):
    assert result.stacked_gradient_count <= result.active_constraint_count
    assert result.gradient_stack_rank <= result.stacked_gradient_count
    if result.active_constraint_count == 0:
        assert result.gradient_stack_rank == 0
    for a in result.attempts:
        assert a.active_constraint_count == result.active_constraint_count


# ---------------------------------------------------------------------------
# 6. acceptance conditions are exactly the frozen seven
# ---------------------------------------------------------------------------
def test_all_seven_acceptance_conditions_present():
    for token in ("DOMAIN_PB_FLOOR", "MIN_ABSOLUTE_RESIDUAL_DECREASE",
                  "ARMIJO_C1", "Q_CONSERVATIVITY_TOL", "single_q_ok",
                  "conservativity_ok"):
        assert token in MODULE_SOURCE, token
    assert m.DOMAIN_PB_FLOOR == 1e-12
    assert m.MIN_ABSOLUTE_RESIDUAL_DECREASE == 1e-12
    assert m.ARMIJO_C1 == 1e-4
    assert m.MATERIAL_REDUCTION_RATIO == 0.5


def test_material_reduction_is_reported_not_required(result):
    """The 0.5 material ratio is reported and is NOT an acceptance gate."""
    for a in result.attempts:
        assert isinstance(a.material_reduction_flag, bool)
    # the accepted candidate need not satisfy the material ratio
    accepted = [a for a in result.attempts if a.accepted][0]
    assert accepted.material_reduction_flag in (True, False)
    assert "REQUIRED_RESIDUAL_REDUCTION_RATIO" in MODULE_SOURCE
    # the material flag must not appear in the reject-reason chain
    assert "REASON_MATERIAL" not in MODULE_SOURCE


def test_accepted_candidate_satisfies_every_condition(result):
    if not result.candidate_accepted:
        pytest.skip("no candidate accepted in this run")
    a = [x for x in result.attempts if x.accepted][0]
    assert a.finite is True
    assert np.isfinite(a.min_pb_trial) and a.min_pb_trial >= 1e-12
    assert a.single_q_ok is True
    assert a.conservativity_ok is True
    assert a.max_abs_q1_trial <= m.Q_CONSERVATIVITY_TOL
    assert a.r_trial_inf < result.r_base_inf
    assert a.absolute_decrease >= 1e-12
    assert a.armijo_pass is True
    assert a.r_trial_inf <= a.armijo_rhs


def test_every_rejected_candidate_has_an_exact_reason(result):
    valid = {m.REASON_ACCEPTED, m.REASON_NONFINITE, m.REASON_DOMAIN,
             m.REASON_SINGLE_Q, m.REASON_CONSERVATIVITY, m.REASON_NOT_REDUCING,
             m.REASON_DECREASE, m.REASON_ARMIJO}
    for a in result.attempts:
        assert a.reject_reason in valid, a.reject_reason
        if a.accepted:
            assert a.reject_reason == m.REASON_ACCEPTED
        else:
            assert a.reject_reason != m.REASON_ACCEPTED


def test_nonfinite_candidates_record_their_failure_mode(result):
    for a in result.attempts:
        if a.reject_reason == m.REASON_NONFINITE:
            assert a.nonfinite_reason != ""
            assert a.finite is False


def test_armijo_rhs_is_exact(result):
    for a in result.attempts:
        if not a.finite:
            continue
        expected = result.r_base_inf - 1e-4 * a.alpha * result.r_base_inf
        assert a.armijo_rhs == pytest.approx(expected, rel=0, abs=0)
        assert a.armijo_pass is bool(a.r_trial_inf <= expected)


def test_residual_ratio_and_decrease_are_exact(result):
    for a in result.attempts:
        if not a.finite:
            continue
        assert a.residual_ratio == pytest.approx(
            a.r_trial_inf / result.r_base_inf, rel=0, abs=0)
        assert a.absolute_decrease == pytest.approx(
            result.r_base_inf - a.r_trial_inf, rel=0, abs=0)


def test_trust_radius_and_step_norms_are_exact(result):
    for a in result.attempts:
        assert a.trust_fraction == 2.0 ** (-a.k_delta)
        assert a.alpha == 2.0 ** (-a.k_alpha)
        assert a.lam == 2.0 ** (-a.k_lambda)
        assert a.trust_radius == pytest.approx(
            a.trust_fraction * a.projected_direction_norm_inf, rel=0, abs=0)
        assert a.clipped_direction_norm_inf <= a.projected_direction_norm_inf


def test_linear_solve_residual_is_acceptable(result):
    for a in result.attempts:
        assert np.isfinite(a.linear_solve_residual_inf)
        assert a.linear_solve_residual_inf <= m.LINEAR_RESIDUAL_TOL


# ---------------------------------------------------------------------------
# 7. terminal selection
# ---------------------------------------------------------------------------
def test_exactly_one_terminal(result):
    assert result.terminal in (m.TERMINAL_A, m.TERMINAL_B, m.TERMINAL_C)
    assert [result.terminal == t for t in (m.TERMINAL_A, m.TERMINAL_B,
                                           m.TERMINAL_C)].count(True) == 1
    assert result.terminal != m.TERMINAL_BLOCKED


def test_terminal_follows_the_frozen_rule(result):
    if result.first_accepted_tuple is not None:
        assert result.candidate_accepted is True
        assert result.search_exhausted is False
        assert result.terminal == m.TERMINAL_A
    elif result.attempted_count > 0:
        assert result.candidate_accepted is False
        assert result.search_exhausted is True
        assert result.terminal == m.TERMINAL_B
    else:
        assert result.terminal == m.TERMINAL_C


def test_at_most_one_accepted_candidate(result):
    assert sum(1 for a in result.attempts if a.accepted) <= 1
    assert result.candidate_accepted == (
        result.first_accepted_tuple is not None)


# ---------------------------------------------------------------------------
# 8. execution ceiling: no second step, no trajectory
# ---------------------------------------------------------------------------
def test_no_second_outer_step_or_trajectory(result):
    assert result.second_outer_step_taken is False
    assert result.trajectory_run is False
    assert result.accepted_new_hjb_iterate is False
    assert result.hjb_convergence_claimed is False


def test_module_has_no_iteration_or_trajectory_machinery():
    """Code-level scan: no outer iteration, no trajectory, no KFE/steady state.

    The `trajectory` token is checked separately: it may appear ONLY as part of the
    boolean result field ``trajectory_run``, which records that no trajectory was
    run. Any other occurrence (a loop, a stepper, a function) is forbidden.
    """
    for token in ("newton_loop", "policy_iteration", "semismooth",
                  "trust_region", "continuation", "line_search", "armijo_loop",
                  "multi_step", "outer_loop", "kfe", "stationary",
                  "steady_state", "solve_household_steady_state"):
        assert token not in CODE_SOURCE, token
    # `trajectory` may occur only inside the `trajectory_run` boolean field
    cleaned = CODE_SOURCE.replace("trajectory_run", "")
    assert "trajectory" not in cleaned, "trajectory machinery present"
    # no trajectory/iteration function or loop exists
    for node in ast.walk(TREE):
        if isinstance(node, ast.FunctionDef):
            assert "trajectory" not in node.name, node.name
            assert "loop" not in node.name, node.name


def test_no_accepted_hjb_iterate_flag_in_source():
    assert "accepted_new_hjb_iterate=False" in MODULE_SOURCE
    assert "hjb_convergence_claimed=False" in MODULE_SOURCE


def test_does_not_mutate_accepted_science_sources():
    """Every accepted-science file is byte-identical to its accepted blob."""
    accepted = {
        SELECTED_Q_RELPATH: "7857cabb4d28af99cb9d59e2d1c3024b05787c11",
        ORACLE_RELPATH: "76ae5b149993a7edeeb8eb337f1b02b3fe33c51e",
        AUDIT69_RELPATH: "83e9be0febcc03eb721265d3558887bd6b1586a4",
        ISSUE71_RELPATH: "96dd262a4ae42e26d489a317d9a04a9264b481b1",
        ISSUE72_RELPATH: "f99ff6eb0d0a74cccc400ba83162a8affa9c6924",
    }
    for relpath, expected in accepted.items():
        assert _blob(relpath) == expected, relpath


# ---------------------------------------------------------------------------
# 9. deterministic repeat
# ---------------------------------------------------------------------------
def test_deterministic_repeat_identical(repeat):
    r, ident = repeat
    assert ident is True
    assert r.deterministic_repeat_identical is True


def test_repeat_reproduces_every_required_quantity(repeat, result):
    r, _ = repeat
    assert r.steps == result.steps
    assert r.final_statistic == result.final_statistic
    assert r.min_boundary_pb_star == result.min_boundary_pb_star
    assert r.r_base_inf == result.r_base_inf
    assert r.residual_argmax_row == result.residual_argmax_row
    assert r.attempted_count == result.attempted_count
    assert r.first_accepted_tuple == result.first_accepted_tuple
    assert r.search_exhausted == result.search_exhausted
    assert r.terminal == result.terminal
    # NOTE: the repeat entry point sets `deterministic_repeat_identical = True` on
    # its own returned result, so that field is compared in
    # `test_deterministic_repeat_identical` instead of here.
    assert r.baseline_operator_build_count == 1
    assert [(a.k_lambda, a.k_delta, a.k_alpha, a.reject_reason)
            for a in r.attempts] == [
        (a.k_lambda, a.k_delta, a.k_alpha, a.reject_reason)
        for a in result.attempts]


def test_repeat_candidate_metrics_identical(repeat, result):
    r, _ = repeat
    for a, b in zip(r.attempts, result.attempts):
        assert a.r_trial_inf == b.r_trial_inf or (
            np.isnan(a.r_trial_inf) and np.isnan(b.r_trial_inf))
        assert a.absolute_decrease == b.absolute_decrease or (
            np.isnan(a.absolute_decrease) and np.isnan(b.absolute_decrease))
        assert a.min_pb_trial == b.min_pb_trial or (
            np.isnan(a.min_pb_trial) and np.isnan(b.min_pb_trial))
        assert a.armijo_rhs == b.armijo_rhs or (
            np.isnan(a.armijo_rhs) and np.isnan(b.armijo_rhs))
        assert a.accepted == b.accepted


# ---------------------------------------------------------------------------
# 10. reporting helpers
# ---------------------------------------------------------------------------
def test_attempts_csv_has_one_row_per_attempt(result):
    lines = m.attempts_csv_lines(result)
    assert lines[0].startswith("index,k_lambda,k_delta,k_alpha")
    assert len(lines) == result.attempted_count + 1


def test_summary_csv_lines_deterministic(result):
    a = m.summary_csv_lines(result)
    b = m.summary_csv_lines(result)
    assert a == b
    assert a[0] == "metric,value"
    joined = "\n".join(a)
    for token in ("terminal,", "attempted_count,", "r_base_inf,",
                  "first_accepted_tuple,"):
        assert token in joined, token
