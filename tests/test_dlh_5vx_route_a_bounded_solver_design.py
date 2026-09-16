"""DLH-5V-X — focused test suite for the bounded residual-balanced single-`Q`
HJB solver-contract DESIGN (Issue #72).

Authority: Issue #72 OPEN; initial authoritative activation ``5696637965``; final
authoritative activation-refresh ``5697299096`` (post-sync live ``main``
``f9bb2b2b2fc889839876185c8fc955200ffb412b``). Route decision
``APPROVE_ROUTE_A_BOUNDED_RESIDUAL_BALANCED_SOLVER_CONTRACT_DESIGN_AFTER_5VW_TERMINAL_B``;
authority marker ``DLH_5VX_ROUTE_A_BOUNDED_SOLVER_DESIGN_AUTHORIZED``.

Scope ceiling: DESIGN / SPECIFICATION ONLY. This suite asserts that the design
artifact is complete, deterministic and internally consistent, and that it
constructs no new nonlinear HJB state and executes no numerical step.
"""

from __future__ import annotations

import ast
import dataclasses
import subprocess
from pathlib import Path

import numpy as np
import pytest

import deep_learning_hank.two_asset.route_a_bounded_solver_design as m

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

GOVERNANCE_BASE = "f9bb2b2b2fc889839876185c8fc955200ffb412b"

# machinery that must NOT be reachable from a design-only module
FORBIDDEN_CALL_NAMES = (
    "build_operator_and_u", "select_matlab_faithful_local_policy",
    "asset_drifts_matlab_faithful", "reconstruct_issue63_stagnation_state",
    "run_issue69_audit", "run_issue66_audit", "run_issue71_decomposition",
    "spsolve", "splu", "solve", "inv", "lstsq", "minimize", "linalg",
    "_step", "_iterate_one_value", "run_hjb", "newton", "tangent",
    "line_search", "backtrack", "continuation", "pseudo_time", "resolvent_step",
    "solve_household_steady_state",
)


@pytest.fixture(scope="module")
def design():
    """ONE full design run plus its ONE deterministic repeat."""
    r, ident = m.run_issue72_design_twice()
    return r, ident


def _blob(rev: str, relpath: str) -> str:
    repo_root = Path(__file__).resolve().parents[1]
    return subprocess.run(
        ["git", "rev-parse", f"{rev}:{relpath}"], cwd=repo_root,
        capture_output=True, text=True, encoding="utf-8",
        errors="replace", check=True).stdout.strip()


# ---------------------------------------------------------------------------
# 1. accepted anchors
# ---------------------------------------------------------------------------
def test_selected_q_accepted_blob_exact():
    assert _blob("HEAD", SELECTED_Q_RELPATH) == m.SELECTED_Q_ACCEPTED_BLOB
    assert m.SELECTED_Q_ACCEPTED_BLOB == (
        "7857cabb4d28af99cb9d59e2d1c3024b05787c11")
    assert _blob(GOVERNANCE_BASE, SELECTED_Q_RELPATH) == (
        m.SELECTED_Q_ACCEPTED_BLOB)


def test_oracle_blob_unchanged():
    assert _blob("HEAD", ORACLE_RELPATH) == m.ORACLE_BLOB == (
        "76ae5b149993a7edeeb8eb337f1b02b3fe33c51e")


def test_issue69_audit_blob_unchanged():
    assert _blob("HEAD", AUDIT69_RELPATH) == m.ISSUE69_AUDIT_BLOB == (
        "83e9be0febcc03eb721265d3558887bd6b1586a4")


def test_accepted_issue71_science_reference_pinned():
    assert _blob("HEAD", ISSUE71_RELPATH) == m.ACCEPTED_ISSUE71_BLOB == (
        "96dd262a4ae42e26d489a317d9a04a9264b481b1")
    assert m.ACCEPTED_ISSUE71_INTEGRATION == (
        "e1d79d6aa6677ca262df1699e21007eaf9690c4d")
    assert m.ACCEPTED_ISSUE70_INTEGRATION == (
        "fb5523d55d01d4b64995d94efb786994b5f8326d")


def test_this_issue_creates_only_its_own_paths():
    repo_root = Path(__file__).resolve().parents[1]
    out = subprocess.run(
        ["git", "status", "--porcelain"], cwd=repo_root,
        capture_output=True, text=True, encoding="utf-8",
        errors="replace", check=True).stdout
    for line in out.splitlines():
        if not line.strip():
            continue
        path = line[3:].strip().rstrip("/")
        assert (line.startswith("??")
                or "route_a_bounded_solver_design" in line
                or "test_dlh_5vx" in line
                or path in ("docs/governance", "reports")), line


def test_authority_marker_and_activations_present():
    for token in ("Issue #72", "DLH-5V-X",
                  "DLH_5VX_ROUTE_A_BOUNDED_SOLVER_DESIGN_AUTHORIZED",
                  "5696637965", "5697299096",
                  "APPROVE_ROUTE_A_BOUNDED_RESIDUAL_BALANCED_SOLVER_CONTRACT_"
                  "DESIGN_AFTER_5VW_TERMINAL_B"):
        assert token in MODULE_SOURCE, token


# ---------------------------------------------------------------------------
# 2. evidence synthesis (Issues #60-#71)
# ---------------------------------------------------------------------------
def test_evidence_matrix_covers_60_to_71(design):
    r, _ = design
    assert r.evidence_issue_count == 9
    assert set(r.evidence_issues) == {"60", "61", "62", "63", "64", "68", "69",
                                      "70", "71"}
    for e in r.evidence:
        assert e.fact and e.accepted_value and e.consequence_for_design
        assert isinstance(e.is_negative, bool)


def test_negative_and_positive_evidence_both_present(design):
    r, _ = design
    assert r.negative_evidence_count >= 3
    assert r.negative_evidence_count < r.evidence_issue_count


def test_no_accepted_history_distortion(design):
    """Cited accepted constants must equal the accepted published values."""
    r, _ = design
    by_issue = {e.issue: e for e in r.evidence}
    # Issue #63: iterate tolerance and FTB parameters
    assert str(m.ISSUE63_CONVERGENCE_TOL) in by_issue["63"].accepted_value
    assert str(m.ISSUE63_TAU_FTB) in by_issue["63"].accepted_value
    # Issue #68: the geometry improvement factor is the accepted 866.25...
    assert "866.2532997045214" in by_issue["68"].accepted_value
    # Issue #71: accepted residual norm and cancellation ratio
    assert "10.435094313164921" in by_issue["71"].accepted_value
    assert "0.006665998653866562" in by_issue["71"].accepted_value
    # Issue #70: accepted selected-Q blob
    assert m.SELECTED_Q_ACCEPTED_BLOB in by_issue["70"].accepted_value
    # Issue #64: the accepted failed material-reduction result
    assert "False" in by_issue["64"].accepted_value


def test_accepted_numerics_match_published_values():
    assert m.ACCEPTED_RESIDUAL_INF == 10.435094313164921
    assert m.ACCEPTED_CANCELLATION_RATIO == 0.006665998653866562
    assert m.ACCEPTED_DECOMPOSITION_CLOSURE == 4.036238010485249e-11
    assert m.ACCEPTED_ROW_RECONSTRUCTION == 2.816165078911581e-10
    assert m.ACCEPTED_MAX_ABS_Q1 == 2.4253377084448857e-12
    assert m.ISSUE68_GEOMETRY_IMPROVEMENT == 866.2532997045214
    assert m.ISSUE64_RESIDUAL_RATIO_ITER == 0.999906663403
    assert m.ISSUE64_MATERIAL_REDUCTION is False
    assert m.BELLMAN_TOLERANCE_UNCHANGED == 1.0e-3


# ---------------------------------------------------------------------------
# 3. candidate-family matrix
# ---------------------------------------------------------------------------
def test_all_four_candidate_families_represented(design):
    r, _ = design
    assert r.family_count == 4
    assert tuple(f.family for f in r.families) == m.CANDIDATE_FAMILIES
    assert m.CANDIDATE_FAMILIES == (
        m.FAMILY_POLICY_FROZEN_NEWTON,
        m.FAMILY_RESIDUAL_JACOBI,
        m.FAMILY_CONSTRAINED_TRUST_REGION,
        m.FAMILY_PSEUDO_TIME_BASELINE)


def test_every_family_assessed_on_every_axis(design):
    r, _ = design
    for f in r.families:
        for axis in m.ADMISSIBILITY_AXES:
            value = getattr(f, axis)
            assert isinstance(value, str) and len(value) > 20, (f.family, axis)


def test_every_family_states_its_accepted_contradiction_or_limitation(design):
    r, _ = design
    for f in r.families:
        assert len(f.accepted_historical_contradiction) > 20
        assert len(f.expected_strength) > 20
        assert len(f.boundedness) > 20
        assert len(f.deterministic_reproducibility) > 20
        if not f.admissible:
            assert len(f.refuted_by) > 0


def test_baseline_family_is_refuted_and_labelled_baseline(design):
    r, _ = design
    baseline = next(f for f in r.families
                    if f.family == m.FAMILY_PSEUDO_TIME_BASELINE)
    assert baseline.admissible is False
    assert "baseline" in baseline.role
    assert "60" in baseline.refuted_by and "61" in baseline.refuted_by
    assert m.FAMILY_PSEUDO_TIME_BASELINE in r.refuted_families


def test_constrained_family_is_the_outer_frame(design):
    r, _ = design
    assert r.outer_framework == m.FAMILY_CONSTRAINED_TRUST_REGION
    outer = next(f for f in r.families if f.family == r.outer_framework)
    assert outer.admissible is True
    assert "outer frame" in outer.role


# ---------------------------------------------------------------------------
# 4. route selection rule (no forced Outcome A)
# ---------------------------------------------------------------------------
def test_route_selection_is_deterministic_and_not_forced(design):
    """With 3 admissible families and only 1 refuted, the frozen rule yields B."""
    r, _ = design
    assert r.selection_rule_satisfied is False
    assert r.admissible_family_count == 3
    assert r.refuted_family_count == 1
    assert r.terminal == m.TERMINAL_B
    assert r.selected_contract_name == (
        "ROUTE_A_BOUNDED_CONSTRAINED_OUTER_FRAME__DIRECTION_OPEN")
    assert r.open_sub_choice and "direction sub-choice" in r.open_sub_choice


def test_selection_rule_is_declared_explicitly():
    assert m.SELECTION_REQUIRES_UNIQUE_ADMISSIBLE_FAMILY is True
    assert m.SELECTION_REQUIRES_REFUTED_ALTERNATIVES == 1
    assert len(m.ADMISSIBILITY_AXES) == 8
    for token in ("SELECTION_REQUIRES_UNIQUE_ADMISSIBLE_FAMILY",
                  "SELECTION_REQUIRES_REFUTED_ALTERNATIVES"):
        assert token in MODULE_SOURCE


def test_exactly_one_terminal_returned(design):
    r, _ = design
    assert r.terminal == m.TERMINAL_B
    assert [r.terminal == t for t in (m.TERMINAL_A, m.TERMINAL_B,
                                      m.TERMINAL_C)].count(True) == 1
    assert r.terminal != m.TERMINAL_BLOCKED


def test_terminal_follows_the_frozen_rule(design):
    r, _ = design
    # consistency holds, so not C; >1 admissible family, so not A
    assert r.consistency_ok is True
    assert r.admissible_family_count > 1
    assert r.terminal == m.TERMINAL_B


# ---------------------------------------------------------------------------
# 5. frozen contract completeness
# ---------------------------------------------------------------------------
REQUIRED_CLAUSES = (
    "solver_state", "residual", "policy_operator_ordering",
    "jacobian_definition", "refresh_rule", "regularization_ladder",
    "trust_radius_ladder", "step_fraction_ladder", "active_boundary_detection",
    "domain_safety_rule", "projection_constraint_rule", "merit_function",
    "acceptance_rule", "rejection_backoff_rule", "max_attempts",
    "iterate_convergence_test", "bellman_convergence_test",
    "fail_closed_terminal", "reproducibility_logging_fields",
)


def test_contract_frozen_with_every_required_clause(design):
    r, _ = design
    assert r.contract_frozen is True
    assert set(r.contract) == set(REQUIRED_CLAUSES)
    for clause in REQUIRED_CLAUSES:
        assert isinstance(r.contract[clause], str)
        assert len(r.contract[clause]) > 20, clause


def test_solver_state_is_v_only(design):
    r, _ = design
    state = r.contract["solver_state"]
    assert "V ONLY" in state
    assert "no new economics state" in state.lower()


def test_residual_definition_is_route_a_single_q(design):
    r, _ = design
    residual = r.contract["residual"]
    assert "rho*V - u(V) - Q(V)*V" in residual
    assert "Owner Route A" in residual
    assert "ONE accepted selected generator" in residual


def test_policy_refresh_rule_is_explicit(design):
    r, _ = design
    refresh = r.contract["refresh_rule"]
    assert "full reassembly" in refresh
    assert "never by partial update" in r.contract["policy_operator_ordering"]
    assert "FROZEN" in refresh


def test_active_boundary_rule_is_explicit(design):
    r, _ = design
    active = r.contract["active_boundary_detection"]
    assert "FULL limiting wall gradient" in active
    assert "MULTIPLE active gradients" in active
    assert str(m.ACTIVE_BOUNDARY_TOLERANCE) in active


def test_domain_safety_rule_is_explicit(design):
    r, _ = design
    safety = r.contract["domain_safety_rule"]
    assert "min required p_b(V_trial) >=" in safety
    assert str(m.CANDIDATE_PB_MARGIN) in safety
    assert "CANDIDATE STATE" in safety


def test_merit_function_is_explicit_and_residual_based(design):
    r, _ = design
    merit = r.contract["merit_function"]
    assert "||R(V)||inf" in merit
    assert "RESIDUAL_REFERENCE" in merit
    assert "+inf" in merit
    assert "No component-wise merit is permitted" in merit


def test_acceptance_rule_is_explicit(design):
    r, _ = design
    acc = r.contract["acceptance_rule"]
    assert "ACCEPTED iff" in acc
    assert str(m.ARMIJO_COEFFICIENT) in acc
    assert "domain-admissible" in acc


def test_rejection_backoff_rule_is_explicit_and_deterministic(design):
    r, _ = design
    back = r.contract["rejection_backoff_rule"]
    assert "Deterministic and exhaustive" in back
    assert "advance the step-fraction ladder" in back
    assert "trust-radius ladder" in back
    assert "regularization ladder" in back


def test_iterate_and_bellman_convergence_are_separated(design):
    r, _ = design
    it = r.contract["iterate_convergence_test"]
    bl = r.contract["bellman_convergence_test"]
    assert "SEPARATE criterion" in it
    assert "never substitutes" in it
    assert "SAME single generator" in bl
    assert "Both tests must hold" in bl
    assert m.ITERATE_CHANGE_TOL != m.BELLMAN_RESIDUAL_TOL
    assert m.ITERATE_CHANGE_TOL < m.BELLMAN_RESIDUAL_TOL


def test_reproducibility_logging_fields_complete(design):
    r, _ = design
    fields = r.reproducibility_fields
    assert len(fields) >= 10
    joined = " ".join(fields)
    for token in ("residual", "domain margin", "regularization", "step norm",
                  "active", "merit", "decision"):
        assert token.lower() in joined.lower(), token


# ---------------------------------------------------------------------------
# 6. exact frozen ladders and thresholds
# ---------------------------------------------------------------------------
def test_every_ladder_is_exact_and_frozen(design):
    r, _ = design
    assert r.ladders["regularization_ladder"] == tuple(
        2.0 ** (-k) for k in range(0, 21))
    assert r.ladders["trust_radius_fraction_ladder"] == tuple(
        2.0 ** (-k) for k in range(0, 21))
    assert r.ladders["step_fraction_ladder"] == tuple(
        2.0 ** (-k) for k in range(0, 21))
    assert r.ladders["regularization_ladder_length"] == 21
    assert r.ladders["trust_radius_fraction_ladder_length"] == 21
    assert r.ladders["step_fraction_ladder_length"] == 21
    assert r.ladders["step_fraction_floor"] == 2.0 ** -20


def test_module_ladders_match_issue60_and_issue61_shapes():
    assert m.REGULARIZATION_LADDER_SIZE == 20
    assert m.REGULARIZATION_LADDER[0] == 1.0
    assert m.REGULARIZATION_LADDER[-1] == 2.0 ** -20
    assert m.STEP_FRACTION_FLOOR == 2.0 ** -20
    assert m.ISSUE63_MAX_BRACKET_HALVINGS == 60


def test_every_threshold_is_exact(design):
    r, _ = design
    th = r.thresholds
    assert th["armijo_coefficient"] == m.ARMIJO_COEFFICIENT == 1.0e-4
    assert th["required_residual_reduction_ratio"] == 0.5
    assert th["min_residual_reduction_absolute"] == 1.0e-12
    assert th["constraint_tolerance"] == 1.0e-9
    assert th["active_boundary_tolerance"] == 1.0e-12
    assert th["pb_safety_margin"] == 1.0e-12
    assert th["candidate_pb_margin"] == 1.0e-12
    assert th["baseline_min_pb"] == 4.8089461301970005e-09
    assert th["linear_solve_rtol"] == 1.0e-12
    assert th["linear_residual_tol"] == 1.0e-10
    assert th["iterate_change_tol"] == 1.0e-7
    assert th["bellman_residual_tol"] == 1.0e-3
    assert th["residual_reference"] == 10.435094313164921


def test_no_adaptive_hedge_language_anywhere(design):
    r, _ = design
    blob = " ".join(str(v) for v in r.contract.values()).lower()
    blob += " " + " ".join(r.pseudocode).lower()
    for hedge in ("choose adaptively", "tune if necessary", "small enough",
                  "reasonable tolerance", "as needed", "if appropriate"):
        assert hedge not in blob, hedge


def test_max_attempts_are_finite_integers(design):
    r, _ = design
    for name, value in r.max_attempts.items():
        assert isinstance(value, int) and value > 0, name
    assert r.max_attempts["max_regularization_attempts"] == 21
    assert r.max_attempts["max_trust_radius_attempts"] == 21
    assert r.max_attempts["max_step_fraction_attempts"] == 21
    assert r.max_attempts["max_total_step_attempts"] == 63
    assert r.max_attempts["max_outer_iterations"] == 1000


# ---------------------------------------------------------------------------
# 7. fail-closed terminals and pseudocode
# ---------------------------------------------------------------------------
def test_fail_closed_terminals_explicit(design):
    r, _ = design
    assert len(r.fail_closed_terminals) == 6
    for name in (m.FAILURE_NO_SAFE_STEP, m.FAILURE_NO_RESIDUAL_REDUCING_STEP,
                 m.FAILURE_LINEAR_SOLVE, m.FAILURE_NONFINITE_EVIDENCE,
                 m.FAILURE_OPERATOR_CONTRACT, m.FAILURE_ATTEMPT_BUDGET):
        assert name in r.fail_closed_terminals
        assert name in r.contract["fail_closed_terminal"]


def test_pseudocode_deterministic_and_complete(design):
    r, _ = design
    code = r.pseudocode
    assert len(code) >= 18
    joined = " ".join(code)
    for token in ("final=False assembly", "J = rho*I - Q", "project",
                  "domain-admissible", "ARMIJO_COEFFICIENT", "fail-closed",
                  "BELLMAN_RESIDUAL_TOL", "ITERATE_CHANGE_TOL"):
        assert token in joined, token
    assert "BELLMAN_CONVERGED" in joined
    assert "ITERATE_STATISTIC_CONVERGED" in joined


def test_material_distinction_answers_every_required_question(design):
    r, _ = design
    d = r.material_distinction
    for key in ("vs_issue60_pure_value_damping", "vs_issue61_resolvent_ladder",
                "vs_issue64_raw_frozen_newton",
                "vs_issue68_single_wall_tangent_trial",
                "how_it_uses_residual_reduction_and_domain_geometry_together",
                "how_it_handles_mixed_cancellation",
                "how_it_avoids_the_raw_newton_tiny_safe_fraction",
                "how_it_avoids_chasing_iterate_change_only",
                "how_single_q_consistency_is_kept_across_policy_reselection"):
        assert key in d, key
        assert len(d[key]) > 40, key


# ---------------------------------------------------------------------------
# 8. design-only enforcement (no execution, no new state)
# ---------------------------------------------------------------------------
def test_no_new_nonlinear_state_is_constructed(design):
    r, _ = design
    assert r.constructed_new_state is False
    assert r.accepted_iterate is False
    assert r.trajectory_run is False
    # The contract legitimately NAMES V_new in prose (it specifies a future
    # execution Issue), but this design run must produce no state array and no
    # numerical state payload: every result field must be a scalar/tuple/str/bool
    # or a container of those, never an ndarray.
    for f in dataclasses.fields(r):
        value = getattr(r, f.name)
        assert not isinstance(value, np.ndarray), f.name
        if isinstance(value, dict):
            for v in value.values():
                assert not isinstance(v, np.ndarray), (f.name, v)
        if isinstance(value, (list, tuple)):
            for v in value:
                assert not isinstance(v, np.ndarray), (f.name, v)
    # and no numeric state vector of state_size length is produced anywhere
    def _has_state_sized_numeric(value) -> bool:
        if isinstance(value, (list, tuple)):
            if (len(value) == m.ACCEPTED_STATE_SIZE
                    and all(isinstance(x, (int, float)) for x in value)):
                return True
            return any(_has_state_sized_numeric(x) for x in value)
        return False

    for f in dataclasses.fields(r):
        assert not _has_state_sized_numeric(getattr(r, f.name)), f.name
    for name in ("accepted_new_hjb_iterate", "new_trajectory_run"):
        assert getattr(r, name, False) is False


def test_no_execution_flags_set(design):
    r, _ = design
    for flag in ("executed_newton", "executed_tangent",
                 "executed_trust_region", "executed_line_search",
                 "executed_continuation", "executed_pseudo_time"):
        assert getattr(r, flag) is False, flag


def test_no_solver_entry_point_is_reachable():
    """No call (by name or attribute) may reach an operator build, policy
    selection, linear solve, or any step/iteration entry point."""
    offenders = []
    for node in ast.walk(TREE):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                name = node.func.id
            elif isinstance(node.func, ast.Attribute):
                name = node.func.attr
            else:
                continue
            if name in FORBIDDEN_CALL_NAMES:
                offenders.append((name, getattr(node, "lineno", -1)))
    assert offenders == [], offenders


def test_module_imports_no_solver_module():
    """Only scalar constants may be imported from the accepted science."""
    allowed = {
        "deep_learning_hank.two_asset.route_a_hjb_residual_decomposition",
        "numpy", "dataclasses", "subprocess", "pathlib", "typing",
        "__future__",
    }
    for node in ast.walk(TREE):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".")[0] in ("numpy", "dataclasses",
                                                    "subprocess", "pathlib",
                                                    "typing", "__future__"), (
                    alias.name)
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            assert mod in allowed or mod.startswith("deep_learning_hank"), mod


def test_no_operator_or_policy_symbol_referenced_in_code():
    """The design module must never even reference an operator/policy symbol."""
    code = MODULE_SOURCE
    for token in ("build_operator_and_u", "select_matlab_faithful_local_policy",
                  "asset_drifts_matlab_faithful", "spsolve", "lstsq"):
        assert token not in code, token


def test_no_forbidden_machinery_names_in_code():
    code = MODULE_SOURCE
    for token in ("_step(", "iterate_one_value", "trust_region_solve",
                  "line_search(", "pseudo_time_update", "KFE", "kfe"):
        assert token not in code, token


def test_design_does_not_claim_hjb_convergence(design):
    r, _ = design
    assert r.hjb_convergence_claimed is False
    assert r.bellman_tolerance == 1.0e-3
    assert r.accepted_residual_inf == 10.435094313164921
    assert r.accepted_residual_inf > r.bellman_tolerance


def test_accepted_residual_anchor_echoed(design):
    r, _ = design
    assert r.accepted_residual_argmax == "row 97 / node 97 / z 0 / F0"
    assert r.accepted_cancellation_ratio == 0.006665998653866562


# ---------------------------------------------------------------------------
# 9. internal consistency and determinism
# ---------------------------------------------------------------------------
def test_internal_consistency_checks_all_pass(design):
    r, _ = design
    assert r.consistency_ok is True
    assert r.consistency_check_count == len(r.consistency_checks)
    assert r.consistency_check_count >= 30
    failed = {k: v for k, v in r.consistency_checks.items() if not v}
    assert failed == {}, failed
    assert r.consistency_checks["evidence_covers_60_to_71"] is True
    assert r.consistency_checks["all_four_families_present"] is True
    assert r.consistency_checks["contract_all_clauses_present"] is True
    assert r.consistency_checks["convergence_criteria_separated"] is True
    assert r.consistency_checks["ladder_floor_matches_issue61"] is True
    assert r.consistency_checks["no_adaptive_hedge_language"] is True
    assert r.consistency_checks["active_set_uses_full_wall_gradient"] is True
    assert r.consistency_checks["merit_is_residual_based"] is True
    assert r.consistency_checks[
        "fail_closed_clause_names_every_terminal"] is True
    assert r.consistency_checks[
        "single_q_enforced_by_full_reassembly"] is True
    assert r.consistency_checks[
        "logging_carries_domain_margin_and_reason"] is True


def test_deterministic_design_artifact_repeat_identical(design):
    r, ident = design
    assert ident is True
    assert r.deterministic_repeat_identical is True


def test_csv_summary_lines_are_deterministic(design):
    r, _ = design
    lines_a = m.summary_csv_lines(r)
    lines_b = m.summary_csv_lines(r)
    assert lines_a == lines_b
    assert lines_a[0] == "metric,value"
    joined = "\n".join(lines_a)
    for token in ("ladder.", "threshold.", "max_attempts.", "consistency.",
                  "evidence.issue71", "family.", "pseudocode,"):
        assert token in joined, token


def test_accepted_anchor_blobs_helper_is_read_only():
    blobs = m.accepted_anchor_blobs()
    assert blobs["selected_q_blob"] == m.SELECTED_Q_ACCEPTED_BLOB
    assert blobs["oracle_blob"] == m.ORACLE_BLOB
    assert blobs["issue69_audit_blob"] == m.ISSUE69_AUDIT_BLOB
    assert blobs["issue71_module_blob"] == m.ACCEPTED_ISSUE71_BLOB
    assert blobs["selected_q_blob_at_base"] == m.SELECTED_Q_ACCEPTED_BLOB
