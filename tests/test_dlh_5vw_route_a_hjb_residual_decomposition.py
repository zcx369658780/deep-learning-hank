"""DLH-5V-W — focused test suite for the Route-A single-`Q` HJB residual source
decomposition at `V_*` (Issue #71).

Authority: Issue #71 OPEN; initial authoritative activation ``5691703381``; final
authoritative activation-refresh ``5691863227`` (post-sync live ``main``
``e1a7a9ac5b00ad4407fcc40bdfb67e46c4ccbe86``). Route decision
``APPROVE_ROUTE_A_SINGLE_Q_HJB_RESIDUAL_SOURCE_DECOMPOSITION_AFTER_5VV_TERMINAL_A``;
authority marker ``DLH_5VW_ROUTE_A_HJB_RESIDUAL_DECOMPOSITION_AUTHORIZED``.

Scope ceiling: READ-ONLY scientific numerical diagnostic. Exactly ONE frozen
state (accepted `V_*`), exactly ONE Route-A ``final=False`` operator build, ONE
all-state additive decomposition, ONE deterministic top-20, ONE read-only top-20
F0 policy reproduction audit, ONE deterministic repeat.

This suite does NOT construct a second scientific `Q`, does NOT build a
``final=True`` scientific comparison operator, does NOT run a Newton / tangent /
trial / line-search / continuation step, does NOT accept an HJB iterate, and does
NOT run a new trajectory.
"""

from __future__ import annotations

import ast
import subprocess
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pytest

import deep_learning_hank.two_asset.route_a_hjb_residual_decomposition as m
from deep_learning_hank.two_asset.stagnation_newton_geometry import (
    reconstruct_issue63_stagnation_state,
)

MODULE_PATH = Path(m.__file__)
MODULE_SOURCE = MODULE_PATH.read_text(encoding="utf-8")

SELECTED_Q_RELPATH = "src/deep_learning_hank/two_asset/boundary_hjb_selected_q.py"
ORACLE_RELPATH = ("src/deep_learning_hank/two_asset/"
                  "matlab_faithful_two_asset_ha.py")
AUDIT69_RELPATH = ("src/deep_learning_hank/two_asset/"
                   "f0_rate_path_divergence_audit.py")

# frozen accepted ancestry (history that must not move)
PRE_ROUTE_A_COMMIT = "825e241804c7fb260c807602fc0f1487caf84e56^"
ORIGINAL_ISSUE70_COMMIT = "825e241804c7fb260c807602fc0f1487caf84e56"
CONTRACT_MIGRATION_COMMIT = "0e3a9597cd5550a237452aeaa57ed0a145aa6c83"
FINAL_ISSUE70_COMMIT = "fb5523d55d01d4b64995d94efb786994b5f8326d"

BANNED_TOKENS = (
    "newton_loop", "policy_iteration", "semismooth", "trust_region",
    "continuation", "linesearch", "line_search", "armijo", "backtrack",
    "alpha_tuning", "tune_alpha", "active_set", "minimize", "sweep",
    "kfe", "stationary", "steady_state", "solve_household_steady_state",
    "run_hjb", "iterate_to_convergence",
)


@pytest.fixture(scope="module")
def decomp():
    """ONE full decomposition plus its ONE deterministic repeat."""
    r, ident = m.run_issue71_decomposition_twice()
    return r, ident


@pytest.fixture(scope="module")
def recon():
    return reconstruct_issue63_stagnation_state()


# ---------------------------------------------------------------------------
# 1. accepted-source provenance (read-only contract)
# ---------------------------------------------------------------------------
def test_selected_q_accepted_blob_exact():
    repo_root = Path(__file__).resolve().parents[1]

    def blob(spec: str, relpath: str) -> str:
        return subprocess.run(
            ["git", "rev-parse", f"{spec}:{relpath}"], cwd=repo_root,
            capture_output=True, text=True, encoding="utf-8",
            errors="replace", check=True).stdout.strip()

    assert blob("HEAD", SELECTED_Q_RELPATH) == m.SELECTED_Q_ACCEPTED_BLOB
    assert m.SELECTED_Q_ACCEPTED_BLOB != m.SELECTED_Q_PRE_ISSUE70_BLOB
    # history preserved: pre-Route-A, original, migration and final remediations
    assert blob(PRE_ROUTE_A_COMMIT, SELECTED_Q_RELPATH) == (
        m.SELECTED_Q_PRE_ISSUE70_BLOB)
    assert blob(ORIGINAL_ISSUE70_COMMIT, SELECTED_Q_RELPATH) == (
        "35e7dadfa4fb8f1c2a89db21751f2b541bda3cab")
    assert blob(CONTRACT_MIGRATION_COMMIT, SELECTED_Q_RELPATH) == (
        "35e7dadfa4fb8f1c2a89db21751f2b541bda3cab")
    assert blob(FINAL_ISSUE70_COMMIT, SELECTED_Q_RELPATH) == (
        m.SELECTED_Q_ACCEPTED_BLOB)
    # and the module records them all
    assert m.SELECTED_Q_PRE_ISSUE70_BLOB == (
        "556ccc214f03a1a22306cc4f5c7e9f7691bbf897")


def test_oracle_blob_exact():
    repo_root = Path(__file__).resolve().parents[1]
    out = subprocess.run(
        ["git", "rev-parse", f"HEAD:{ORACLE_RELPATH}"], cwd=repo_root,
        capture_output=True, text=True, encoding="utf-8",
        errors="replace", check=True).stdout.strip()
    assert out == m.ORACLE_BLOB == "76ae5b149993a7edeeb8eb337f1b02b3fe33c51e"


def test_issue69_audit_blob_exact_and_unmodified():
    repo_root = Path(__file__).resolve().parents[1]
    out = subprocess.run(
        ["git", "rev-parse", f"HEAD:{AUDIT69_RELPATH}"], cwd=repo_root,
        capture_output=True, text=True, encoding="utf-8",
        errors="replace", check=True).stdout.strip()
    assert out == m.ISSUE69_AUDIT_BLOB == (
        "83e9be0febcc03eb721265d3558887bd6b1586a4")
    dirty = subprocess.run(
        ["git", "diff", "--name-only", "HEAD", "--", AUDIT69_RELPATH],
        cwd=repo_root, capture_output=True, text=True, encoding="utf-8",
        errors="replace", check=True).stdout.strip()
    assert dirty == ""


def test_this_issue_does_not_mutate_any_accepted_source():
    """Issue #71 adds only its own four paths.

    Accepted Issue #61-#70 sources are untouched, with ONE disclosed exception: a
    single stale ASSERTION in the accepted Issue #70 focused suite claimed that
    live ``origin/main`` still carried the pre-Route-A selected-Q revision. Since
    Issue #70 was accepted and integrated, ``main`` carries the ACCEPTED Route-A
    state instead, so that assertion is factually wrong about the repository and
    was corrected. It is a truthfulness fix about which revision carries which
    blob; no Route-A scientific quantity, threshold or expectation is changed.
    This test permits that one path and nothing else.
    """
    repo_root = Path(__file__).resolve().parents[1]
    out = subprocess.run(
        ["git", "status", "--porcelain"], cwd=repo_root,
        capture_output=True, text=True, encoding="utf-8",
        errors="replace", check=True).stdout
    allowed_fix = "tests/test_dlh_5vv_route_a_single_q_operator_contract.py"
    for line in out.splitlines():
        if not line.strip():
            continue
        path = line[3:].strip()
        assert (line.startswith("??")
                or "route_a_hjb_residual_decomposition" in line
                or "test_dlh_5vw" in line
                or path == allowed_fix), line


def test_the_one_accepted_file_correction_is_assertion_only():
    """GUARD (Reviewer hold `5695153100`): the ONE permitted fifth-path edit must
    be an assertion-only repository-state correction.

    This does not trust a hand-written claim: it derives the ACTUAL base-vs-HEAD
    diff of the permitted Issue #70 file and audits every added and removed line.

    Allowed added lines are exactly:
      * comments,
      * the `ISSUE70_ACCEPTED_SELECTED_Q_BLOB = "<accepted blob>"` constant, and
      * the corrected assertion that compares `origin/main` against that constant.
    Allowed removed lines are exactly the superseded stale assertion lines that
    claimed live `main` carried the pre-Route-A revision.

    Any scientific threshold, expectation, tolerance, terminal or operator marker
    on either side FAILS this test, so a future scientific mutation cannot hide
    inside this file's authorized correction.
    """
    repo_root = Path(__file__).resolve().parents[1]
    base = "e1a7a9ac5b00ad4407fcc40bdfb67e46c4ccbe86"
    relpath = "tests/test_dlh_5vv_route_a_single_q_operator_contract.py"
    diff = subprocess.run(
        ["git", "diff", base, "--", relpath], cwd=repo_root,
        capture_output=True, text=True, encoding="utf-8",
        errors="replace", check=True).stdout
    added = [ln[1:] for ln in diff.splitlines()
             if ln.startswith("+") and not ln.startswith("+++")]
    removed = [ln[1:] for ln in diff.splitlines()
               if ln.startswith("-") and not ln.startswith("---")]

    # --- scientific/tolerance markers may NOT appear on either side
    forbidden = ("ALPHA_HALF =", "ALPHA_NEAR =", "FINAL_STATISTIC_EXPECTED",
                 "MIN_BOUNDARY_PB_EXPECTED", "R_ITER_INF_S0", "MACHINE_TOL",
                 "BELLMAN_TOLERANCE_UNCHANGED", "TOL", "TERMINAL_",
                 "label_changes", "sector=", "row_entries", "PASSED",
                 "convergence")
    for line in added + removed:
        for token in forbidden:
            assert token not in line, (token, line)

    # --- every added line is a comment, the accepted-blob constant, or the guard
    for line in added:
        stripped = line.strip()
        assert (stripped.startswith("#")
                or stripped.startswith("ISSUE70_ACCEPTED_SELECTED_Q_BLOB =")
                or ("blob(" in line
                    and "ISSUE70_ACCEPTED_SELECTED_Q_BLOB" in line)
                or stripped.startswith("assert blob(")
                ), f"unexpected added line: {line!r}"

    # --- the constant carries exactly the accepted Issue #70 blob
    const_lines = [ln for ln in added
                   if ln.strip().startswith("ISSUE70_ACCEPTED_SELECTED_Q_BLOB =")]
    assert len(const_lines) == 1
    assert m.SELECTED_Q_ACCEPTED_BLOB in const_lines[0]
    assert "7857cabb4d28af99cb9d59e2d1c3024b05787c11" in const_lines[0]

    # --- added lines must reference the accepted blob, never the pre-Route-A one
    for line in added:
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        assert "556ccc214f03a1a22306cc4f5c7e9f7691bbf897" not in line, line

    # --- removed lines are only the superseded origin/main assertion + its comment
    assert removed, "the correction must actually replace something"
    for line in removed:
        stripped = line.strip()
        assert (stripped.startswith("#")
                or (stripped.startswith("assert blob(") and "origin/main" in line)
                ), f"unexpected removed line: {line!r}"

    # --- the pre-Route-A anchor is STILL asserted, at an absolute revision
    corrected = (repo_root / relpath).read_text(encoding="utf-8")
    assert "825e241804c7fb260c807602fc0f1487caf84e56^" in corrected
    assert "SELECTED_Q_PRE_ISSUE70_BLOB" in corrected
    assert "556ccc214f03a1a22306cc4f5c7e9f7691bbf897" in corrected
    # ...and the corrected file still pins the accepted blob for origin/main
    assert "origin/main" in corrected
    assert "live main now carries the ACCEPTED post-Route-A state" in corrected
    # exactly ONE line in the file asserts origin/main, and it uses the constant
    main_asserts = [ln for ln in corrected.splitlines()
                    if "origin/main" in ln and ln.strip().startswith("assert")]
    assert len(main_asserts) == 1
    assert "ISSUE70_ACCEPTED_SELECTED_Q_BLOB" in main_asserts[0]

    # --- the implementation under test is STILL the accepted blob
    def blob(spec: str) -> str:
        return subprocess.run(
            ["git", "rev-parse", f"{spec}:{SELECTED_Q_RELPATH}"], cwd=repo_root,
            capture_output=True, text=True, encoding="utf-8",
            errors="replace", check=True).stdout.strip()

    assert blob("origin/main") == m.SELECTED_Q_ACCEPTED_BLOB
    assert blob(PRE_ROUTE_A_COMMIT) == m.SELECTED_Q_PRE_ISSUE70_BLOB


def test_fifth_path_correction_diff_is_bounded_to_two_hunks():
    """The authorized fifth path must be a SMALL, bounded edit (not a rewrite)."""
    repo_root = Path(__file__).resolve().parents[1]
    diff = subprocess.run(
        ["git", "diff", "--numstat", "e1a7a9ac5b00ad4407fcc40bdfb67e46c4ccbe86",
         "--", "tests/test_dlh_5vv_route_a_single_q_operator_contract.py"],
        cwd=repo_root, capture_output=True, text=True, encoding="utf-8",
        errors="replace", check=True).stdout.split()
    added, removed = int(diff[0]), int(diff[1])
    assert added <= 12, added
    assert removed <= 4, removed


def test_authority_marker_present():
    for token in ("Issue #71", "DLH-5V-W",
                  "DLH_5VW_ROUTE_A_HJB_RESIDUAL_DECOMPOSITION_AUTHORIZED",
                  "5691703381", "5691863227",
                  "APPROVE_ROUTE_A_SINGLE_Q_HJB_RESIDUAL_SOURCE_DECOMPOSITION_AFTER_5VV_TERMINAL_A"):
        assert token in MODULE_SOURCE, token


# ---------------------------------------------------------------------------
# 2. exact frozen-state reproduction
# ---------------------------------------------------------------------------
def test_exact_vstar_reconstruction(decomp):
    r, _ = decomp
    assert r.failure_detail is None
    assert r.steps == m.ACCEPTED_STEPS == 8
    assert r.final_statistic == pytest.approx(m.ACCEPTED_FINAL_STATISTIC,
                                              abs=1e-12)
    assert r.min_boundary_pb_star == pytest.approx(m.ACCEPTED_MIN_BOUNDARY_PB,
                                                   abs=1e-12)
    assert r.wall_state["family"] == m.ACCEPTED_WALL_FAMILY
    assert r.wall_state["j"] == m.ACCEPTED_WALL_J
    assert r.wall_state["i"] == m.ACCEPTED_WALL_I
    assert r.wall_state["z"] == m.ACCEPTED_WALL_Z
    assert r.wall_state["node"] == m.ACCEPTED_WALL_NODE


def test_exact_residual_norm(decomp):
    r, _ = decomp
    assert r.residual_inf == pytest.approx(m.ACCEPTED_RESIDUAL_INF, abs=1e-12)
    assert r.residual_inf == 10.435094313164921


def test_exact_residual_argmax(decomp):
    r, _ = decomp
    assert r.residual_argmax_row == 97
    assert r.residual_argmax_node == 97
    assert r.residual_argmax_z == 0
    assert r.residual_argmax_family == "F0"


def test_no_hjb_convergence_claim(decomp):
    """The residual stays ~10435x the UNCHANGED Bellman tolerance."""
    r, _ = decomp
    assert r.bellman_tolerance == m.BELLMAN_TOLERANCE_UNCHANGED == 1e-3
    assert r.residual_over_tolerance == pytest.approx(10435.094313164921,
                                                      rel=1e-9)
    assert r.residual_over_tolerance > 1.0


# ---------------------------------------------------------------------------
# 3. exactly ONE operator build, no second scientific Q
# ---------------------------------------------------------------------------
def test_exactly_one_operator_build(recon):
    """The decomposition performs exactly ONE Route-A final=False build."""
    solver = recon["solver"]
    real = solver.build_operator_and_u
    seen: list[dict] = []

    def counting(V, labor0v, ti, brg, final=False, f0_policies=None):
        seen.append({"final": final})
        return real(V, labor0v, ti, brg, final=final, f0_policies=f0_policies)

    with patch.object(solver, "build_operator_and_u", side_effect=counting):
        r = m._run_from_reconstruction(recon, {"builds": 0, "selector_calls": 0})
    assert len(seen) == 1
    assert seen[0]["final"] is False
    assert r.operator_build_count == 1


def _code_only_text() -> str:
    """Module source with all docstrings removed, so forbidden-machinery scans
    test CODE rather than prose (the docstring legitimately names the machinery
    this Issue is forbidden to use)."""
    tree = ast.parse(MODULE_SOURCE)
    docstrings = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef,
                             ast.ClassDef)):
            body = getattr(node, "body", [])
            if body and isinstance(body[0], ast.Expr) and isinstance(
                    body[0].value, ast.Constant) and isinstance(
                    body[0].value.value, str):
                docstrings.add(id(body[0]))
    lines = MODULE_SOURCE.splitlines()
    drop = set()
    for node in ast.walk(tree):
        if id(node) in docstrings:
            for ln in range(node.lineno, (node.end_lineno or node.lineno) + 1):
                drop.add(ln)
    return "\n".join(ln for i, ln in enumerate(lines, start=1) if i not in drop)


CODE_SOURCE = _code_only_text()


def test_no_second_scientific_q_in_source():
    """No final=True scientific comparison build, no raw-drift alternate Q."""
    tree = ast.parse(MODULE_SOURCE)
    func = None
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "build_operator_and_u":
            func = node
    assert func is None, "the module must not contain its own operator builder"
    # the ONLY operator build is the single accepted final=False call
    builds = [n for n in ast.walk(tree)
              if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
              and n.func.attr == "build_operator_and_u"]
    assert len(builds) == 1
    kwargs = {kw.arg: kw for kw in builds[0].keywords}
    assert "final" in kwargs
    assert isinstance(kwargs["final"].value, ast.Constant)
    assert kwargs["final"].value.value is False
    # no supplied second policy set (the default None is used, never passed)
    assert "f0_policies" not in kwargs
    for token in ("f0_policies", "asset_drifts_matlab_faithful",
                  "max(-mu", "max(mu", "final=True"):
        assert token not in CODE_SOURCE, token


def test_operator_build_uses_only_the_public_accepted_entry_point():
    calls = [n for n in ast.walk(ast.parse(MODULE_SOURCE))
             if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
             and n.func.attr == "build_operator_and_u"]
    assert len(calls) == 1


def test_exactly_twenty_top_rows(decomp):
    r, _ = decomp
    assert len(r.top20) == m.TOP_N == 20
    assert [t.rank for t in r.top20] == list(range(1, 21))


# ---------------------------------------------------------------------------
# 4. additive decomposition and closure
# ---------------------------------------------------------------------------
def test_rowwise_decomposition_closes(decomp):
    """Every one of the 782 rows closes to floating-point ordering accuracy."""
    r, _ = decomp
    assert r.decomposition_closure_max_error <= m.CLOSURE_TOL
    assert r.decomposition_closure_max_error < 1e-9
    for s in r.rows:
        assert s.closure_error <= m.CLOSURE_TOL, s.row


def test_global_decomposition_closure_reported(decomp):
    r, _ = decomp
    assert np.isfinite(r.decomposition_closure_max_error)
    assert r.decomposition_closure_max_error >= 0.0
    assert r.decomposition_closed is True


def test_operator_row_attribution_reproduces_the_assembled_operator(decomp):
    """The record-rebuilt operator row equals the ONE assembled operator row."""
    r, _ = decomp
    assert r.operator_row_closure_max_error <= 1e-9
    assert r.rate_attribution_mismatch_rows == 0


def test_components_sum_to_the_residual(decomp):
    """The nine components are reported so their PLAIN SUM is the residual."""
    r, _ = decomp
    for s in r.rows:
        assert abs(sum(s.component_vector().values()) - s.residual) <= (
            m.CLOSURE_TOL)
    for t in r.top20:
        gross = sum(abs(getattr(t, n)) for n in m.COMPONENT_NAMES)
        assert np.isfinite(gross)


def test_all_nine_components_reported_for_every_row(decomp):
    r, _ = decomp
    assert len(m.COMPONENT_NAMES) == 9
    for s in r.rows:
        assert set(s.component_vector()) == set(m.COMPONENT_NAMES)
        for name in m.COMPONENT_NAMES:
            assert np.isfinite(float(getattr(s, name))), (s.row, name)


def test_f0_slot_rate_attribution_is_exact(decomp):
    """Each F0 destination is attributed to exactly ONE published rate slot."""
    r, _ = decomp
    for s in r.rows:
        if s.family != "F0":
            continue
        assert s.rate_attribution_ok is True
        # slots that are represented carry exactly the record's rate; the
        # truncated mass accounts for any published-but-unrepresented slot
        assert s.f0_slot_rates is not None
        assert len(s.f0_slot_rates) == 4
        assert s.truncated_slot_mass >= 0.0


def test_z_switch_matches_the_accepted_switch_matrix(recon):
    """The z-switch term is sourced only from the accepted switch matrix."""
    r = m._run_from_reconstruction(recon, {"builds": 0, "selector_calls": 0})
    switch = np.asarray(recon["solver"].config.switch_matrix, dtype=float)
    n = recon["solver"].n
    Vf = recon["V_star"].ravel(order="F")
    for s in r.rows[:120]:
        expected = 0.0
        for z2 in range(recon["solver"].nz):
            if z2 != s.z:
                expected += float(switch[s.z, z2]) * Vf[z2 * n + s.node]
        assert s.z_switch_term == pytest.approx(-expected, abs=0.0)


def test_diagonal_term_is_separately_recorded(recon):
    """The diagonal is recorded independently, from the assembled operator."""
    r = m._run_from_reconstruction(recon, {"builds": 0, "selector_calls": 0})
    Vf = recon["V_star"].ravel(order="F")
    switch = np.asarray(recon["solver"].config.switch_matrix, dtype=float)
    checked = 0
    for s in r.rows:
        assert np.isfinite(s.stored_diagonal)
        assert np.isfinite(s.assembled_diagonal)
        assert s.assembled_diagonal == s.stored_diagonal + float(switch[s.z, s.z])
        assert s.diagonal_term == -(s.assembled_diagonal * Vf[s.row])
        checked += 1
    assert checked == r.total_states


# ---------------------------------------------------------------------------
# 5. all-state statistics
# ---------------------------------------------------------------------------
def test_all_state_statistics(decomp):
    r, _ = decomp
    assert r.total_states == m.ACCEPTED_STATE_SIZE == 782
    assert r.f0_state_count == m.ACCEPTED_F0_STATE_COUNT == 596
    assert r.non_f0_state_count == m.ACCEPTED_NON_F0_STATE_COUNT == 186
    assert r.f0_state_count + r.non_f0_state_count == r.total_states
    assert len(r.rows) == r.total_states


def test_f0_and_non_f0_maxima(decomp):
    r, _ = decomp
    assert r.max_abs_R_f0 == pytest.approx(m.ACCEPTED_RESIDUAL_INF, abs=1e-12)
    assert r.argmax_f0_row == 97
    assert np.isfinite(r.max_abs_R_non_f0)
    assert r.max_abs_R_f0 > r.max_abs_R_non_f0


def test_z_block_maxima(decomp):
    r, _ = decomp
    assert np.isfinite(r.max_abs_R_z0)
    assert np.isfinite(r.max_abs_R_z1)
    assert r.max_abs_R_z0 >= r.max_abs_R_z1


def test_residual_sign_counts(decomp):
    r, _ = decomp
    assert (r.positive_residual_count + r.negative_residual_count
            + r.zero_residual_count) == r.total_states
    assert r.positive_residual_count > 0
    assert r.negative_residual_count > 0


def test_q_conservativity(decomp):
    r, _ = decomp
    assert r.max_abs_q1 <= 1e-9
    assert r.max_abs_q1 == pytest.approx(2.4253377084448857e-12, rel=1e-9)


def test_contribution_class_maxima_reported(decomp):
    r, _ = decomp
    assert set(r.contribution_class_totals) == set(m.COMPONENT_NAMES)
    assert set(r.contribution_class_maxima) == set(m.COMPONENT_NAMES)
    for name in m.COMPONENT_NAMES:
        assert r.contribution_class_totals[name] >= (
            r.contribution_class_maxima[name] - 1e-9)


# ---------------------------------------------------------------------------
# 6. deterministic top-20 ordering
# ---------------------------------------------------------------------------
def test_top20_ordering_is_deterministic(decomp):
    r, _ = decomp
    keys = [(-t.abs_residual, t.row) for t in r.top20]
    assert keys == sorted(keys)


def test_top20_is_the_true_global_top20(decomp):
    r, _ = decomp
    ordered = sorted(r.rows, key=lambda s: (-s.abs_residual, s.row))[:20]
    assert [t.row for t in r.top20] == [s.row for s in ordered]
    # strictly: no non-selected row exceeds the smallest selected row
    assert min(t.abs_residual for t in r.top20) >= max(
        s.abs_residual for s in r.rows if s.row not in {t.row for t in r.top20})


def test_top20_row_payload_complete(decomp):
    r, _ = decomp
    need = {"rank", "row", "node", "j", "i", "z", "family", "residual",
            "abs_residual", "residual_sign", "sector", "liquid_label",
            "transfer_label", "consumption", "labor", "transfer", "mu_a",
            "mu_b", "stored_b_backward_rate", "stored_b_forward_rate",
            "stored_a_backward_rate", "stored_a_forward_rate", "neighbours",
            "represented_destinations", "reconstructed_R", "closure_error"}
    need |= set(m.COMPONENT_NAMES)
    for t in r.top20:
        fields = {f for f in vars(t)}
        assert need <= fields, need - fields


def test_top20_has_no_full_sparse_dump(decomp):
    r, _ = decomp
    for t in r.top20:
        # represented destinations are a compact tuple, not a matrix
        assert isinstance(t.represented_destinations, tuple)
        assert len(t.represented_destinations) <= 4
        assert isinstance(t.neighbours, dict)


def test_top20_all_f0_and_reproduced(decomp):
    r, _ = decomp
    assert r.top20_f0_count == 20
    assert r.policy_reproduction_failure_count == 0


# ---------------------------------------------------------------------------
# 7. read-only top-20 F0 policy reproduction
# ---------------------------------------------------------------------------
def test_policy_records_reproduce(decomp):
    r, _ = decomp
    assert r.policy_reproductions
    assert len(r.policy_reproductions) == r.top20_f0_count
    for p in r.policy_reproductions:
        assert p.reproduced is True, (p.row, p.mismatch_detail)
        assert p.controls_match is True
        assert p.utility_match is True
        assert p.drifts_match is True
        assert p.stored_rates_match is True
        assert p.labels_match is True


def test_reproduction_differences_are_exactly_zero(decomp):
    r, _ = decomp
    for p in r.policy_reproductions:
        assert p.max_control_abs_diff == 0.0
        assert p.max_drift_abs_diff == 0.0
        assert p.max_rate_abs_diff == 0.0
        assert p.utility_abs_diff == 0.0


def test_reproduction_covers_exactly_the_top20_f0_rows(decomp):
    r, _ = decomp
    f0_top_rows = [t.row for t in r.top20 if t.is_f0]
    assert sorted(p.row for p in r.policy_reproductions) == sorted(f0_top_rows)


def test_selector_called_once_per_top20_f0_row(decomp):
    r, _ = decomp
    assert r.selector_call_count == r.top20_f0_count == 20


def test_reproduction_uses_the_accepted_selector_only(recon):
    """The audit re-invokes the accepted selector; no other policy search."""
    calls = [n for n in ast.walk(ast.parse(MODULE_SOURCE))
             if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
             and n.func.id == "select_matlab_faithful_local_policy"]
    assert len(calls) == 1
    assert "select_matlab_faithful_local_policy" in MODULE_SOURCE


def test_reproduction_inputs_match_the_assembly(decomp):
    """The re-invocation uses the same local FD inputs as the assembly."""
    src = MODULE_SOURCE
    for token in ("compute_derivatives", "v_a_forward", "v_a_backward",
                  "v_b_forward", "v_b_backward", "baseline_labor",
                  "a_max", "solver.da", "solver.db", "drift_tolerance",
                  "at_lower_a", "at_upper_a", "at_lower_b", "at_upper_b",
                  "cfg.inputs", "cfg.params", "cfg.z"):
        assert token in src, token


def test_branch_inconsistency_flag_uses_observed_label(decomp):
    r, _ = decomp
    for t in r.top20:
        if not t.is_f0:
            continue
        expected = bool(t.liquid_label == "F" and t.mu_b < 0.0
                        and t.stored_b_forward_rate > 0.0)
        assert t.branch_inconsistent is expected


# ---------------------------------------------------------------------------
# 8. classification determinism + frozen criteria
# ---------------------------------------------------------------------------
def test_classification_is_deterministic(decomp):
    r, _ = decomp
    assert r.decomposition_closed is True
    assert r.policy_records_reproduced is True
    assert r.dominant_residual_f0 is True
    assert isinstance(r.flags, tuple)
    assert m.DECOMPOSITION_CLOSED in r.flags
    assert m.POLICY_RECORDS_REPRODUCED in r.flags
    assert m.DOMINANT_RESIDUAL_F0 in r.flags


def test_no_forced_outcome_a(decomp):
    """Outcome A is NOT claimed: the residual is a cancellation imbalance."""
    r, _ = decomp
    assert r.dominant_component_identified is False
    assert r.dominant_component_class == ""
    assert m.DOMINANT_COMPONENT_IDENTIFIED not in r.flags
    assert r.mixed_or_unresolved is True
    assert m.MIXED_OR_UNRESOLVED in r.flags
    # no single component carries the residual: it is a small remainder
    assert r.cancellation_ratio_top20_mean < m.DOMINANCE_MIN_CANCELLATION_RATIO
    assert r.cancellation_ratio_top20_mean < 0.05
    assert r.cancellation_ratio_top20_max < 0.05


def test_leading_components_are_comparable_not_unique(decomp):
    r, _ = decomp
    totals = r.top20_component_totals
    lead = sorted(totals.items(), key=lambda kv: (-kv[1], kv[0]))
    # the two leading classes are close: no unique dominant mechanism
    assert lead[0][1] > 0.0
    gap = (lead[0][1] - lead[1][1]) / lead[0][1]
    assert gap < 0.60


def test_frozen_dominance_criteria_are_explicit():
    assert m.DOMINANCE_TOP20_COVERAGE == 1.0
    assert 0.0 < m.DOMINANCE_MIN_LEADING_GAP < 1.0
    assert 0.0 < m.DOMINANCE_MIN_CANCELLATION_RATIO < 1.0
    for token in ("DOMINANCE_TOP20_COVERAGE", "DOMINANCE_MIN_LEADING_GAP",
                  "DOMINANCE_MIN_CANCELLATION_RATIO"):
        assert token in MODULE_SOURCE


def test_exactly_one_terminal_returned(decomp):
    r, _ = decomp
    assert r.terminal == m.TERMINAL_B
    assert r.terminal != m.TERMINAL_A
    assert r.terminal != m.TERMINAL_C
    assert r.terminal != m.TERMINAL_BLOCKED
    assert [r.terminal == t for t in (m.TERMINAL_A, m.TERMINAL_B,
                                      m.TERMINAL_C)].count(True) == 1


def test_terminal_follows_the_frozen_rule(decomp):
    r, _ = decomp
    # decomposition + reproduction pass, but no unique dominant component
    assert r.decomposition_closed and r.policy_records_reproduced
    assert not r.dominant_component_identified
    assert r.terminal == m.TERMINAL_B


# ---------------------------------------------------------------------------
# 9. determinism, no iterate, no trajectory, forbidden machinery
# ---------------------------------------------------------------------------
def test_deterministic_repeat_identical(decomp):
    r, ident = decomp
    assert ident is True
    assert r.deterministic_repeat_identical is True


def test_no_accepted_iterate_and_no_trajectory(decomp):
    r, _ = decomp
    assert r.accepted_new_hjb_iterate is False
    assert r.new_trajectory_run is False


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


def test_no_newton_or_tangent_or_linesearch_machinery():
    """No Newton / tangent / line-search / continuation MACHINERY in code.

    The accepted module ``stagnation_newton_geometry`` is imported (for the
    read-only reconstruction) and is therefore excluded from the name scan.
    """
    code = CODE_SOURCE.replace("stagnation_newton_geometry", "")
    code = code.replace("reconstruct_issue63_stagnation_state", "")
    for token in ("spsolve", "limiting_wall_gradient",
                  "single_wall_tangent_projection", "tangent",
                  "alpha_tuning", "linesearch", "line_search", "continuation"):
        assert token not in code, token
    # and no linear solve / matrix inversion of any kind
    solves = [n for n in ast.walk(ast.parse(MODULE_SOURCE))
              if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
              and n.func.attr in ("spsolve", "solve", "splu", "inv")]
    assert solves == []


def test_scope_ceiling_documented():
    lower = MODULE_SOURCE.lower()
    for token in ("read-only diagnostic", "exactly one frozen state",
                  "does **not** construct a second scientific"):
        assert token in lower
