"""DLH-5V-U — focused test suite for the latent F0 iteration-rate vs raw-drift
sign-divergence audit (Issue #69).

Authority: Issue #69 OPEN; initial authoritative activation ``5676828795``;
final authoritative activation-refresh ``5677087565`` (post-sync live ``main``
``510bde97e60c1fb7f2cb5afb5bee18da18ca561f``). Route decision
``APPROVE_F0_ITERATION_RATE_VS_RAW_DRIFT_SIGN_PROVENANCE_AUDIT_AFTER_5VT_TERMINAL_C``;
authority marker ``DLH_5VU_F0_RATE_PATH_DIVERGENCE_AUDIT_AUTHORIZED``.

Scope ceiling: read-only diagnostic / provenance. This suite does NOT choose or
replace the authoritative rate path, does not accept an HJB iterate, and does
not construct any new Newton / tangent / constrained direction.
"""

from __future__ import annotations

import ast
import subprocess
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pytest

import deep_learning_hank.two_asset.f0_rate_path_divergence_audit as m
from deep_learning_hank.two_asset.stagnation_newton_geometry import (
    reconstruct_issue63_stagnation_state,
)
from deep_learning_hank.two_asset.tangent_projected_newton_geometry import (
    limiting_wall_gradient,
    single_wall_tangent_projection,
)

MODULE_PATH = Path(m.__file__)
MODULE_SOURCE = MODULE_PATH.read_text(encoding="utf-8")

SELECTED_Q_RELPATH = "src/deep_learning_hank/two_asset/boundary_hjb_selected_q.py"

BANNED_TOKENS = (
    "newton_loop", "policy_iteration", "semismooth", "trust_region",
    "continuation", "linesearch", "line_search", "armijo", "backtrack",
    "alpha_tuning", "tune_alpha", "active_set", "minimize", "sweep",
    "kfe", "stationary", "steady_state", "solve_household_steady_state",
)


@pytest.fixture(scope="module")
def audit():
    """ONE full audit plus its ONE deterministic repeat."""
    r, ident = m.run_issue69_audit_twice()
    return r, ident


@pytest.fixture(scope="module")
def recon():
    return reconstruct_issue63_stagnation_state()


# ---------------------------------------------------------------------------
# 1. frozen reconstruction + accepted Issue #68 geometry
# ---------------------------------------------------------------------------
def test_frozen_reconstruction_exact(audit):
    r, _ = audit
    assert r.failure_detail is None
    assert r.iterations == 8
    assert r.final_statistic == pytest.approx(m.FINAL_STATISTIC_EXPECTED, abs=1e-12)
    assert r.min_boundary_pb_star == pytest.approx(
        m.MIN_BOUNDARY_PB_EXPECTED, abs=1e-12)
    assert r.wall_state["family"] == "F3"
    assert r.wall_state["j"] == 13 and r.wall_state["i"] == 13
    assert r.wall_state["z"] == 1 and r.wall_state["node"] == m.WALL_NODE
    assert r.r_inf == pytest.approx(m.REPAIRED_R_INF, abs=1e-12)
    assert r.tangent_identity_residual == 0.0


def test_accepted_issue68_alpha_fractions_exact(audit):
    r, _ = audit
    assert [t.label for t in r.trials] == list(m.TRIAL_ORDER)
    assert [t.alpha for t in r.trials] == [m.ALPHA_HALF, m.ALPHA_NEAR]
    assert m.ALPHA_HALF == 0.08085341880193442
    assert m.ALPHA_NEAR == 0.16170683760386884


def test_selected_q_repaired_blob_exact():
    repo_root = Path(__file__).resolve().parents[1]
    out = subprocess.run(
        ["git", "rev-parse", f"HEAD:{SELECTED_Q_RELPATH}"],
        cwd=repo_root, capture_output=True, text=True, check=True)
    assert out.stdout.strip() == m.SELECTED_Q_REPAIRED_BLOB


# ---------------------------------------------------------------------------
# 2. exact accepted Issue #68 gap/row reproduction
# ---------------------------------------------------------------------------
def test_alpha_half_gap_and_rows_reproduced(audit):
    r, _ = audit
    t = r.trials[0]
    assert t.label == "alpha_half"
    assert t.max_rowwise_q_difference == pytest.approx(
        m.EXPECTED_GAP_HALF, abs=m.REPRO_TOL)
    assert t.inconsistent_rows == m.EXPECTED_ROWS_HALF
    assert t.gap_reproduced is True
    assert t.inconsistent_row_set_match is True
    assert t.expected_rows == m.EXPECTED_ROWS_HALF


def test_alpha_near_gap_and_rows_reproduced(audit):
    r, _ = audit
    t = r.trials[1]
    assert t.label == "alpha_near"
    assert t.max_rowwise_q_difference == pytest.approx(
        m.EXPECTED_GAP_NEAR, abs=m.REPRO_TOL)
    assert t.inconsistent_rows == m.EXPECTED_ROWS_NEAR
    assert t.gap_reproduced is True
    assert t.inconsistent_row_set_match is True
    assert t.expected_rows == m.EXPECTED_ROWS_NEAR


def test_fail_closed_when_gap_not_reproduced(recon):
    """A wrong expected gap must fail closed, never silently pass."""
    solver = recon["solver"]
    V_star, labor0, rho = recon["V_star"], recon["labor0"], recon["rho"]
    V_flat = V_star.ravel(order="F")
    from scipy import sparse
    from scipy.sparse import linalg
    Q0, u0, _d0, _r0 = solver.build_operator_and_u(
        V_star, labor0, 0.0, 0.0, final=False)
    R0 = rho * V_flat - (u0 + Q0.dot(V_flat))
    S = solver.state_size
    d_n = linalg.spsolve(rho * sparse.eye(S, format="csr") - Q0, -R0)
    gvec = limiting_wall_gradient(solver, m.WALL_NODE, m.WALL_NZ)
    d_t = m.single_wall_tangent_projection(d_n, gvec)["d_T"]
    with pytest.raises(m.F0RatePathDivergenceFailure):
        m._audit_trial(solver, V_star, labor0, rho, d_t, "alpha_half",
                       m.ALPHA_HALF, 999.0, m.EXPECTED_ROWS_HALF)


# ---------------------------------------------------------------------------
# 3. same controls / utility across the compared paths
# ---------------------------------------------------------------------------
def test_same_controls_and_utility_across_paths(audit):
    r, _ = audit
    for t in r.trials:
        assert t.same_controls_and_utility is True


def test_stored_and_raw_mu_are_identical(audit):
    """Stored and freshly recomputed drifts must coincide on every affected row.

    This is what rules out a drift-RECOMPUTATION difference and localises the
    mechanism to the rate-object construction.
    """
    r, _ = audit
    for t in r.trials:
        for row in t.rows:
            assert row.stored_mu_a == row.raw_mu_a
            assert row.stored_mu_b == row.raw_mu_b


# ---------------------------------------------------------------------------
# 4. stored-vs-raw rate extraction
# ---------------------------------------------------------------------------
def test_iteration_rates_reproduced_from_accepted_policy(audit):
    r, _ = audit
    for t in r.trials:
        assert t.all_rows_reproduced is True
        for row in t.rows:
            assert row.row_reproduction_ok is True


def test_iteration_path_stores_opposite_direction_component(audit):
    """The mechanism: the accepted iteration path stores a non-zero rate
    OPPOSING the realized drift; the raw upwind path structurally cannot."""
    r, _ = audit
    for t in r.trials:
        assert t.opposite_direction_component_row_count == (
            t.q_row_divergent_row_count)
        for row in t.rows:
            assert row.b_rate_divergent is True
            assert row.iteration_opposite_direction_component is True
            assert row.raw_opposite_direction_component is False
            # realized drift is backward, iteration stores a forward rate
            assert row.raw_mu_b < 0.0
            assert row.raw_b_forward_rate == 0.0
            assert row.iteration_b_forward_rate > 0.0


def test_a_axis_rates_identical_everywhere(audit):
    r, _ = audit
    assert r.a_axis_rates_identical_all_rows is True
    for t in r.trials:
        assert t.a_rate_divergent_row_count == 0
        assert t.max_a_rate_difference == 0.0


def test_b_rate_divergence_magnitudes(audit):
    r, _ = audit
    assert r.trials[0].max_b_rate_difference == pytest.approx(
        0.3359018826891829, rel=1e-12)
    assert r.trials[1].max_b_rate_difference == pytest.approx(
        0.6689705962768723, rel=1e-12)


# ---------------------------------------------------------------------------
# 5. ALL-F0 accounting + decomposition closure
# ---------------------------------------------------------------------------
def test_all_f0_accounting_counts(audit):
    r, _ = audit
    for t in r.trials:
        assert t.total_f0_rows == 596
        assert t.rate_identical_row_count == 596 - t.q_row_divergent_row_count
        assert t.b_rate_divergent_row_count == t.q_row_divergent_row_count
        assert t.diagonal_divergent_row_count == t.q_row_divergent_row_count
        assert t.q_row_divergent_row_count == len(t.inconsistent_rows)
        assert t.omitted_rate_divergent_row_count == 0
        assert t.destination_layout_divergent_row_count == 0


def test_rowwise_q_gap_decomposition_closes(audit):
    """The summed off-diagonal rate difference must equal the diagonal
    difference on every affected row, with no unexplained remainder."""
    r, _ = audit
    for t in r.trials:
        assert t.decomposition_closed is True
        assert t.max_decomposition_residual <= m.DECOMP_TOL
        for row in t.rows:
            assert row.decomposition_residual <= m.DECOMP_TOL
            assert row.summed_rate_difference == pytest.approx(
                row.diagonal_difference, abs=m.DECOMP_TOL)
            # and the reported rowwise operator gap equals that magnitude
            assert row.rowwise_max_gap == pytest.approx(
                row.diagonal_difference, abs=m.DECOMP_TOL)
            # no omitted destination rate on either path
            assert row.omitted_iteration_rate == 0.0
            assert row.omitted_final_rate == 0.0


def test_rowwise_gap_equals_max_diagonal_difference(audit):
    r, _ = audit
    for t in r.trials:
        assert t.max_diagonal_difference == pytest.approx(
            t.max_rowwise_q_difference, abs=m.DECOMP_TOL)


def test_destination_layout_has_no_truncation_divergence(audit):
    """Both paths share the same z-block upwind template; the only difference
    is a zero-valued forward slot on the raw path."""
    r, _ = audit
    for t in r.trials:
        assert t.destination_layout_divergent_row_count == 0
        for row in t.rows:
            assert row.destination_layout_divergent is False
            # the iteration adds exactly one extra in-block destination column
            extra = set(row.iteration_destinations) - set(row.final_destinations)
            assert len(extra) == 1
            assert set(row.final_destinations) < set(row.iteration_destinations)


def test_q_gap_nonzero_columns_recorded(audit):
    r, _ = audit
    for t in r.trials:
        for row in t.rows:
            assert len(row.q_gap_nonzero_columns) == 3
            assert len(row.q_gap_column_magnitudes) == 3
            assert max(row.q_gap_column_magnitudes) <= row.rowwise_max_gap + 1e-15


# ---------------------------------------------------------------------------
# 6. deterministic classification flags + terminal
# ---------------------------------------------------------------------------
def test_classification_flags(audit):
    r, _ = audit
    assert r.iter_rate_path_source_backed is True
    assert r.final_raw_path_source_backed is True
    assert r.rate_formulas_globally_equivalent is False
    assert r.sign_or_branch_divergence_established is True
    assert r.truncation_or_destination_divergence_established is False
    assert r.other_mechanism_established is False
    assert r.mixed_or_unresolved is False


def test_exactly_one_terminal(audit):
    r, _ = audit
    assert r.terminal == m.TERMINAL_A
    assert r.terminal != m.TERMINAL_B
    assert r.terminal != m.TERMINAL_C
    assert r.terminal != m.TERMINAL_BLOCKED
    assert [r.terminal == t for t in (m.TERMINAL_A, m.TERMINAL_B,
                                      m.TERMINAL_C)].count(True) == 1


def test_terminal_follows_the_frozen_rule(audit):
    r, _ = audit
    fully_accounts = all(t.decomposition_closed for t in r.trials)
    assert fully_accounts is True
    assert r.sign_or_branch_divergence_established is True
    assert r.truncation_or_destination_divergence_established is False
    assert r.other_mechanism_established is False
    assert r.mixed_or_unresolved is False
    assert r.terminal == m.TERMINAL_A


def test_no_authoritative_path_selected(audit):
    """The audit must not adjudicate which rate path is correct."""
    r, _ = audit
    src = MODULE_SOURCE.lower()
    for banned in ("authoritative_path =", "chosen_path", "preferred_path",
                   "correct_path =", "replace_rate"):
        assert banned not in src
    assert r.provenance["equivalence"][
        "globally_algebraically_equivalent"] is False


# ---------------------------------------------------------------------------
# 7. source provenance
# ---------------------------------------------------------------------------
def test_provenance_mapping_deterministic_and_source_backed():
    p1 = m.provenance_mapping()
    p2 = m.provenance_mapping()
    assert p1 == p2
    for key in ("iteration_rate_path", "final_raw_rate_path", "equivalence",
                "divergence_condition"):
        assert key in p1
    it = p1["iteration_rate_path"]
    assert "matlab_faithful_two_asset_ha.py" in it["source"]
    assert it["objects_are_foc_shadow_not_drift"] is True
    assert "iteration_b_backward_rate" in it["b_rate_construction"]
    assert "sdh_b" in it["b_rate_construction"]
    fin = p1["final_raw_rate_path"]
    assert "build_operator_and_u" in fin["final_branch"]
    assert "asset_drifts_matlab_faithful" in fin["drift_recompute"]
    assert "max(-mu_b,0)/db" in fin["rate_mapping"]
    dc = p1["divergence_condition"]
    assert dc["kind"] == "sign_or_branch"
    assert dc["a_axis_affected"] is False
    assert dc["destination_layout_affected"] is False
    assert dc["truncation_affected"] is False
    assert p1["read_only"] is True and p1["source_mutation"] is False


def test_provenance_anchors_exist_in_accepted_sources():
    """The cited anchors must really exist in the accepted sources."""
    repo_root = Path(__file__).resolve().parents[1]
    oracle = (repo_root / "src/deep_learning_hank/two_asset"
              / "matlab_faithful_two_asset_ha.py").read_text(encoding="utf-8")
    selected_q = (repo_root / "src/deep_learning_hank/two_asset"
                  / "boundary_hjb_selected_q.py").read_text(encoding="utf-8")
    for token in ("iteration_b_backward_rate", "iteration_b_forward_rate",
                  "sdh_b", "sdh_f", "sc_b", "sc_f", "use_liquid_b",
                  "use_liquid_f", "use_transfer_b", "use_transfer_f",
                  "liquid_resources_b", "liquid_resources_f"):
        assert token in oracle, token
    for token in ("iteration_b_backward_rate", "iteration_b_forward_rate",
                  "a_backward_rate", "a_forward_rate",
                  "asset_drifts_matlab_faithful", "max(-mu_a_v, 0.0) / self.da",
                  "max(-mu_b_v, 0.0) / self.db"):
        assert token in selected_q, token


# ---------------------------------------------------------------------------
# 8. execution design + determinism + forbidden machinery
# ---------------------------------------------------------------------------
def test_exactly_two_trials_and_no_third(audit):
    r, _ = audit
    assert r.trial_count == 2
    assert len(r.trials) == 2
    assert [t.label for t in r.trials] == list(m.TRIAL_ORDER)


def test_exactly_two_builds_per_trial(recon):
    """Each trial: exactly ONE final=False re-selection and ONE corrected
    final=True build; no extra operator build for search/tuning."""
    solver = recon["solver"]
    seen: list[dict] = []
    real = solver.build_operator_and_u

    def counting(V, labor0v, ti, brg, final=False, f0_policies=None):
        seen.append({"final": final})
        return real(V, labor0v, ti, brg, final=final, f0_policies=f0_policies)

    with patch.object(solver, "build_operator_and_u", side_effect=counting):
        r = m._run_from_reconstruction(recon)
    assert len(seen) == 5      # 1 base + 2 per trial
    assert sum(1 for c in seen if c["final"] is False) == 3
    assert sum(1 for c in seen if c["final"] is True) == 2
    assert r.trial_count == 2


def test_deterministic_repeat_identical(audit):
    r, ident = audit
    assert ident is True
    assert r.deterministic_repeat_identical is True


def test_no_accepted_hjb_iterate(audit):
    r, _ = audit
    assert r.accepted_new_hjb_iterate is False


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
    # exactly ONE linalg.spsolve (the base Newton direction, needed only to
    # rebuild the accepted Issue #68 tangent geometry)
    solves = [n for n in ast.walk(tree)
              if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
              and n.func.attr == "spsolve"]
    assert len(solves) == 1
    # exactly THREE operator-build call SITES in the module: ONE base build in
    # _run_from_reconstruction plus ONE final=False and ONE final=True site in
    # _audit_trial (invoked once per frozen trial -> FIVE runtime calls total,
    # asserted by the runtime spy test above)
    builds = [n for n in ast.walk(tree)
              if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
              and n.func.attr == "build_operator_and_u"]
    assert len(builds) == 3
