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

POST-ROUTE-A CONTRACT MIGRATION (Issue #70 remediation)
------------------------------------------------------
Owner Route A consolidates HJB rate semantics onto ONE MATLAB-faithful selected
generator. The accepted Issue #69 audit module ``f0_rate_path_divergence_audit``
is a READ-ONLY diagnostic and is deliberately **not** modified by this migration
(it is outside the authorized path set). The audit's frozen rule is that it
attests a divergence MECHANISM only when the accepted Issue #68 rowwise
operator gap/rows are REPRODUCED at the frozen trial states. Route A removes
that operator gap (``Q_final == Q_iter`` exactly), so the audit now correctly
FAILS CLOSED with terminal ``TERMINAL_C`` instead of attesting a mechanism.

This suite therefore asserts the audit's true current behaviour, and keeps the
accepted Issue #68 / #69 magnitudes as explicitly labelled HISTORICAL evidence.
The historical numbers are NEVER asserted as current runtime expectations:

- the current runtime OPERATOR gap is ``0.0`` (asserted as CURRENT);
- the accepted Issue #68 gaps ``0.6718037653783657`` / ``1.3379411925537439``,
  their divergent row sets ``(452, 453)`` / ``(452, 453, 482, 483)`` and the
  latent b-rate differences ``0.3359018826891829`` / ``0.6689705962768723`` are
  preserved as HISTORICAL constants and re-measured independently below.
"""

from __future__ import annotations

import ast
import subprocess
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pytest
from scipy import sparse
from scipy.sparse import linalg

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

# ---------------------------------------------------------------------------
# HISTORICAL (PRE-ROUTE-A) EVIDENCE — accepted Issue #68/#69 magnitudes and the
# pre-Issue-70 selected-Q blob. Retained as regression evidence; NOT current
# runtime expectations.
# ---------------------------------------------------------------------------
PRE_ROUTE_A_SELECTED_Q_BLOB = "556ccc214f03a1a22306cc4f5c7e9f7691bbf897"
HISTORICAL_ISSUE68_GAP_HALF = 0.6718037653783657
HISTORICAL_ISSUE68_ROWS_HALF = (452, 453)
HISTORICAL_ISSUE68_GAP_NEAR = 1.3379411925537439
HISTORICAL_ISSUE68_ROWS_NEAR = (452, 453, 482, 483)
HISTORICAL_ISSUE68_B_RATE_DIFF_HALF = 0.3359018826891829
HISTORICAL_ISSUE68_B_RATE_DIFF_NEAR = 0.6689705962768723
HISTORICAL_ISSUE68_ROW_COUNTS = (2, 4)
HISTORICAL_ISSUE69_TERMINAL_A = (
    "DLH_5VU_F0_RATE_PATH_DIVERGENCE__UNIQUE_SIGN_OR_BRANCH_MECHANISM_"
    "ESTABLISHED_AND_FULLY_ACCOUNTS_FOR_TRIAL_OPERATOR_GAPS__RATE_SEMANTICS_"
    "SCIENTIFIC_REVIEW_GATE_READY")

# ---------------------------------------------------------------------------
# CURRENT (OWNER ROUTE A) EXPECTATIONS — the accepted single-Q consolidation
# makes the final-vs-iteration operator gap exactly zero at every frozen trial,
# so the accepted Issue #68 reproduction gate can no longer be satisfied and the
# read-only audit fails closed.
# ---------------------------------------------------------------------------
CURRENT_ROUTE_A_SELECTED_Q_BLOB = "35e7dadfa4fb8f1c2a89db21751f2b541bda3cab"
CURRENT_ROUTE_A_Q_GAP = 0.0
CURRENT_ROUTE_A_TERMINAL = m.TERMINAL_C
CURRENT_ROUTE_A_TERMINAL_DISCLOSURE = (
    "DLH_5VU_F0_RATE_PATH_DIVERGENCE__CURRENT_ROUTE_A_SINGLE_Q_CONTRACT__"
    "NO_FINAL_VS_ITERATION_RATE_PATH_DIVERGENCE_AT_FROZEN_TRIAL_STATES__"
    "HISTORICAL_ISSUE68_GAP_ATTRIBUTION_PRESERVED")
# The exact current-runtime measurement carried by the fail-closed message.
CURRENT_ROUTE_A_FAILURE_ALPHA_HALF = (
    "alpha_half: accepted Issue #68 gap/rows not reproduced "
    "(gap=0.0 vs 0.6718037653783657; rows=[] vs [452, 453])")

# Frozen trial states (accepted Issue #68 alphas; immutable inputs to the audit).
ALPHA_HALF = m.ALPHA_HALF
ALPHA_NEAR = m.ALPHA_NEAR


@pytest.fixture(scope="module")
def audit():
    """ONE full audit plus its ONE deterministic repeat."""
    r, ident = m.run_issue69_audit_twice()
    return r, ident


@pytest.fixture(scope="module")
def recon():
    return reconstruct_issue63_stagnation_state()


@pytest.fixture(scope="module")
def d_t_direction(recon):
    """The accepted Issue #68 tangent direction, rebuilt exactly as the audit
    module's own ``_run_from_reconstruction`` rebuilds it."""
    solver = recon["solver"]
    V_star, labor0, rho = recon["V_star"], recon["labor0"], recon["rho"]
    V_flat = V_star.ravel(order="F")
    Q0, u0, _d0, _r0 = solver.build_operator_and_u(
        V_star, labor0, 0.0, 0.0, final=False)
    R0 = rho * V_flat - (u0 + Q0.dot(V_flat))
    d_n = linalg.spsolve(
        rho * sparse.eye(solver.state_size, format="csr") - Q0, -R0)
    gvec = limiting_wall_gradient(solver, m.WALL_NODE, m.WALL_NZ)
    return m.single_wall_tangent_projection(d_n, gvec)["d_T"]


@pytest.fixture(scope="module")
def trial_paths(recon, d_t_direction):
    """The frozen trial operators at BOTH accepted Issue #68 alphas.

    Reuses the audit's own construction design (ONE ``final=False``
    re-selection, then ONE corrected ``final=True`` build with the SAME controls)
    without calling the frozen audit entry point, so the current-runtime
    operator identity can be measured independently of the audit's own
    fail-closed gate.
    """
    solver = recon["solver"]
    V_star, labor0 = recon["V_star"], recon["labor0"]
    out = {}
    for label, alpha in (("alpha_half", ALPHA_HALF), ("alpha_near", ALPHA_NEAR)):
        V_trial = V_star + alpha * d_t_direction.reshape(
            (solver.n, solver.nz), order="F")
        Q_i, u_i, _di, rec_i = solver.build_operator_and_u(
            V_trial, labor0, 0.0, 0.0, final=False)
        Q_f, u_f, _df, rec_f = solver.build_operator_and_u(
            V_trial, labor0, 0.0, 0.0, final=True, f0_policies=rec_i)
        out[label] = {
            "alpha": alpha, "V_trial": V_trial,
            "Q_iter": Q_i, "u_iter": u_i, "rec_iter": rec_i,
            "Q_final": Q_f, "u_final": u_f, "rec_final": rec_f,
        }
    return out


@pytest.fixture(scope="module")
def f0_row_evidence(recon, trial_paths):
    """Per-row stored-vs-raw rate evidence on the affected F0 rows.

    The latent rate-object divergence that Issue #69 attributed is measured
    HERE, independently of the audit's fail-closed gate, so the historical
    magnitudes are re-verified against the current accepted sources.
    """
    solver = recon["solver"]
    labor0 = recon["labor0"]
    f0_rows = m._f0_rows_of(solver)
    out = {}
    for label in ("alpha_half", "alpha_near"):
        p = trial_paths[label]
        recs = p["rec_iter"]
        divergent_b: list[int] = []
        opposite: int = 0
        max_b = 0.0
        details = {}
        for r in f0_rows:
            r = int(r)
            info = m._row_rates(solver, p["V_trial"], labor0, r, recs[r])
            bd = max(abs(info["it_bb"] - info["raw_bb"]),
                     abs(info["it_bf"] - info["raw_bf"]))
            max_b = max(max_b, bd)
            if bd > m.ROW_ZERO_TOL:
                divergent_b.append(r)
            if info["iteration_opposite_b_component"]:
                opposite += 1
            if r in (452, 453, 482, 483):
                details[r] = info
        out[label] = {
            "divergent_b_rows": tuple(divergent_b),
            "divergent_b_row_count": len(divergent_b),
            "opposite_component_row_count": opposite,
            "max_b_rate_difference": max_b,
            "details": details,
        }
    return out


# ---------------------------------------------------------------------------
# 1. frozen reconstruction + accepted Issue #68 geometry
# ---------------------------------------------------------------------------
def test_frozen_reconstruction_exact(recon):
    """The accepted Issue #63 base geometry is unchanged by Route A."""
    trace = recon["trace"]
    assert len(trace) == 8
    assert float(trace[-1]["accepted_max_stat"]) == pytest.approx(
        m.FINAL_STATISTIC_EXPECTED, abs=1e-12)
    wall = dict(trace[-1]["worst_after"])
    assert wall["family"] == "F3"
    assert wall["j"] == 13 and wall["i"] == 13
    assert wall["node"] == m.WALL_NODE
    solver = recon["solver"]
    V_star, labor0, rho = recon["V_star"], recon["labor0"], recon["rho"]
    V_flat = V_star.ravel(order="F")
    Q0, u0, _d0, _r0 = solver.build_operator_and_u(
        V_star, labor0, 0.0, 0.0, final=False)
    R0 = rho * V_flat - (u0 + Q0.dot(V_flat))
    assert float(np.max(np.abs(R0))) == pytest.approx(
        m.REPAIRED_R_INF, abs=1e-12)
    gvec = limiting_wall_gradient(solver, m.WALL_NODE, m.WALL_NZ)
    proj = single_wall_tangent_projection(
        linalg.spsolve(rho * sparse.eye(solver.state_size, format="csr") - Q0,
                       -R0), gvec)
    assert proj["g_dot_d_t"] == 0.0


def test_accepted_issue68_alpha_fractions_exact():
    assert m.TRIAL_ORDER == ("alpha_half", "alpha_near")
    assert ALPHA_HALF == 0.08085341880193442
    assert ALPHA_NEAR == 0.16170683760386884


def test_selected_q_repaired_blob_exact():
    """CURRENT: the selected-Q blob is the post-Route-A (Issue #70) candidate.

    The historical pre-Route-A Issue #67 repair blob is preserved as evidence in
    the module constants and remains verifiable at the Issue #70 parent commit.
    """
    repo_root = Path(__file__).resolve().parents[1]
    out = subprocess.run(
        ["git", "rev-parse", f"HEAD:{SELECTED_Q_RELPATH}"],
        cwd=repo_root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=True)
    assert out.stdout.strip() == CURRENT_ROUTE_A_SELECTED_Q_BLOB
    # historical pre-Route-A blob stays recorded and DIFFERENT
    assert m.SELECTED_Q_REPAIRED_BLOB == PRE_ROUTE_A_SELECTED_Q_BLOB
    assert PRE_ROUTE_A_SELECTED_Q_BLOB != CURRENT_ROUTE_A_SELECTED_Q_BLOB
    # and it is verifiable at the Issue #70 parent commit
    pre = subprocess.run(
        ["git", "rev-parse", f"HEAD~1:{SELECTED_Q_RELPATH}"],
        cwd=repo_root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=True)
    assert pre.stdout.strip() == PRE_ROUTE_A_SELECTED_Q_BLOB


# ---------------------------------------------------------------------------
# 2. CURRENT Route-A operator identity at the frozen trial states
# ---------------------------------------------------------------------------
def test_current_route_a_operator_identity_is_exact(trial_paths):
    """CURRENT: at BOTH accepted alphas ``Q_final == Q_iter`` and
    ``u_final == u_iter`` exactly (bit-identical), so the rowwise operator gap
    is exactly ``0.0`` on every one of the 596 F0 rows.

    This is the Route-A property that makes the accepted Issue #68 gap
    unreproducible in the current runtime.
    """
    for label in ("alpha_half", "alpha_near"):
        p = trial_paths[label]
        gap = np.abs(p["Q_final"].toarray() - p["Q_iter"].toarray())
        assert float(gap.max()) == CURRENT_ROUTE_A_Q_GAP
        assert int(np.count_nonzero(gap)) == 0
        assert np.array_equal(p["u_final"], p["u_iter"])
        # the final=True build reuses the SUPPLIED selected records: same number
        # of records, and every record's assembled row entries are EQUAL
        assert len(p["rec_final"]) == len(p["rec_iter"])
        assert all(a.row_entries == b.row_entries
                   and a.diagonal == b.diagonal
                   and a.utility == b.utility
                   for a, b in zip(p["rec_iter"], p["rec_final"])
                   if a is not None and b is not None)


def test_current_route_a_f0_rows_carry_zero_gap(recon, trial_paths):
    """The zero gap holds on every one of the 596 F0 rows, not merely in the
    global maximum, and on both z blocks."""
    solver = recon["solver"]
    f0_rows = m._f0_rows_of(solver)
    assert len(f0_rows) == 596
    for label in ("alpha_half", "alpha_near"):
        p = trial_paths[label]
        q_i, q_f = p["Q_iter"], p["Q_final"]
        for r in f0_rows:
            r = int(r)
            gap = np.abs(
                np.asarray(q_f.getrow(r).toarray()).ravel()
                - np.asarray(q_i.getrow(r).toarray()).ravel())
            assert float(gap.max()) == CURRENT_ROUTE_A_Q_GAP
        # and the per-row record entries are literally the same objects
        for r in f0_rows:
            assert p["rec_iter"][int(r)].row_entries == (
                p["rec_final"][int(r)].row_entries)


def test_current_route_a_controls_are_shared(trial_paths):
    """The compared paths share consumption / labor / transfer / utility / mu /
    diagonal on EVERY record, which is what makes the zero operator gap a
    same-controls result rather than a controls artefact."""
    for label in ("alpha_half", "alpha_near"):
        p = trial_paths[label]
        compared = 0
        for r in range(len(p["rec_iter"])):
            a, b = p["rec_iter"][r], p["rec_final"][r]
            if a is None or b is None:
                continue
            compared += 1
            assert a.consumption == b.consumption
            assert a.labor == b.labor
            assert a.transfer == b.transfer
            assert a.utility == b.utility
            assert a.mu_a == b.mu_a
            assert a.mu_b == b.mu_b
            assert a.diagonal == b.diagonal
            assert a.row_entries == b.row_entries
        assert compared == len(p["rec_iter"]) == 782


# ---------------------------------------------------------------------------
# 3. the latent stored-vs-raw rate mechanism persists (historical magnitudes)
# ---------------------------------------------------------------------------
def test_latent_b_rate_divergence_persists_at_historical_rows(f0_row_evidence):
    """The OPERATOR gap is gone, but the latent rate-object divergence is still
    measurable on exactly the rows Issue #69 identified, and the count of rows
    carrying an opposing-direction component equals the count of b-rate-divergent
    rows (they are the liquid-forward rows)."""
    for label, expected_rows in (("alpha_half", HISTORICAL_ISSUE68_ROWS_HALF),
                                 ("alpha_near", HISTORICAL_ISSUE68_ROWS_NEAR)):
        ev = f0_row_evidence[label]
        assert ev["divergent_b_rows"] == expected_rows
        assert ev["divergent_b_row_count"] == len(expected_rows)
        assert ev["opposite_component_row_count"] == len(expected_rows)
    # the accepted Issue #69 row counts are exactly (2, 4)
    assert tuple(
        f0_row_evidence[k]["divergent_b_row_count"]
        for k in ("alpha_half", "alpha_near")) == HISTORICAL_ISSUE68_ROW_COUNTS
    # Route A leaves the a-axis and the net active b-direction untouched
    for label in ("alpha_half", "alpha_near"):
        for info in f0_row_evidence[label]["details"].values():
            assert info["it_ab"] == info["raw_ab"]
            assert info["it_af"] == info["raw_af"]
            assert info["iteration_active_b"] == info["raw_active_b"]


def test_latent_b_rate_divergence_magnitudes_unchanged(f0_row_evidence):
    """The accepted Issue #69 b-rate magnitudes are reproduced exactly by the
    current sources, even though they no longer reach the operator."""
    assert f0_row_evidence["alpha_half"]["max_b_rate_difference"] == (
        pytest.approx(HISTORICAL_ISSUE68_B_RATE_DIFF_HALF, rel=1e-12))
    assert f0_row_evidence["alpha_near"]["max_b_rate_difference"] == (
        pytest.approx(HISTORICAL_ISSUE68_B_RATE_DIFF_NEAR, rel=1e-12))
    assert HISTORICAL_ISSUE68_ROW_COUNTS == (2, 4)


def test_module_historical_constants_preserved():
    """The module's frozen accepted Issue #68 references are untouched."""
    assert m.EXPECTED_GAP_HALF == HISTORICAL_ISSUE68_GAP_HALF
    assert m.EXPECTED_GAP_NEAR == HISTORICAL_ISSUE68_GAP_NEAR
    assert m.EXPECTED_ROWS_HALF == HISTORICAL_ISSUE68_ROWS_HALF
    assert m.EXPECTED_ROWS_NEAR == HISTORICAL_ISSUE68_ROWS_NEAR
    assert m.ALPHA_HALF == ALPHA_HALF
    assert m.ALPHA_NEAR == ALPHA_NEAR
    assert m.TERMINAL_A == HISTORICAL_ISSUE69_TERMINAL_A
    # and the historical attributions stay DISTINCT from the current terminal
    assert HISTORICAL_ISSUE69_TERMINAL_A != CURRENT_ROUTE_A_TERMINAL


def test_iteration_path_stores_opposite_direction_component(f0_row_evidence):
    """The accepted iteration path stores a NON-ZERO b-forward rate that OPPOSES
    the realized (backward) drift, while the corrected raw upwind path
    structurally cannot and does not.

    MEASURED CURRENT STRUCTURE (differs from the historical Issue #69 prose in
    exactly one respect, and the assertions below follow the measurement):

    * the realized drift is backward (``mu_b < 0``) on all four watched rows;
    * the iteration b-backward rate EXCEEDS the raw backward rate whenever the
      liquid branch is bound forward (``liquid_label == 'F'``) -- rows 452/453 at
      both alphas, plus 482/483 at ``alpha_near``;
    * the iteration b-forward rate is positive exactly there, while the raw
      path stores exactly ``0.0``;
    * the NET active b-direction and the a-axis rates nevertheless AGREE
      exactly, so the divergence is a stored-form divergence confined to the
      per-side rate values -- which is why Route A removes it from the operator
      by reusing the stored record verbatim.
    """
    for label, liquid_f_rows in (("alpha_half", (452, 453)),
                                 ("alpha_near", (452, 453, 482, 483))):
        details = f0_row_evidence[label]["details"]
        assert sorted(details) == [452, 453, 482, 483]
        assert len(details) == 4
        assert f0_row_evidence[label]["divergent_b_rows"] == liquid_f_rows
        for r in sorted(details):
            info = details[r]
            # a-axis rates agree exactly on every watched row
            assert info["it_ab"] == info["raw_ab"]
            assert info["it_af"] == info["raw_af"]
            # the realized drift is backward on every watched row, and the raw
            # path stores exactly one non-zero b side
            assert info["raw_mu_b"] < 0.0
            assert info["raw_active_b"] == "B"
            assert info["raw_bf"] == 0.0
            assert info["raw_bb"] > 0.0
            # only the iteration path can carry the opposing component
            assert info["raw_opposite_b_component"] is False
            # and the stored rates are faithfully reproduced from the accepted
            # policy function (no inference from names)
            assert info["row_reproduction_ok"] is True
            # stored and freshly recomputed drifts coincide exactly: the
            # mechanism is the rate-OBJECT construction, not a recomputation
            assert info["stored_mu_a"] == info["raw_mu_a"]
            assert info["stored_mu_b"] == info["raw_mu_b"]
            # transfer branch is bound backward everywhere here
            assert info["transfer_label"] == "B"
            if r in liquid_f_rows:
                # the source-backed condition: liquid branch bound FORWARD while
                # the realized drift points BACKWARD
                assert info["liquid_label"] == "F"
                assert info["it_bf"] > 0.0
                assert info["it_bb"] > info["raw_bb"]
                assert info["iteration_opposite_b_component"] is True
                # yet the NET direction still agrees -- the divergence lives in
                # the per-side stored rates, not in the net drift direction
                assert info["iteration_active_b"] == info["raw_active_b"] == "B"
            else:
                # not yet liquid-forward: no b-rate divergence at all
                assert info["liquid_label"] == "B"
                assert info["it_bf"] == 0.0
                assert info["it_bb"] == info["raw_bb"]
                assert info["iteration_opposite_b_component"] is False


# ---------------------------------------------------------------------------
# 4. CURRENT: the audit fails closed rather than attesting a vanished gap
# ---------------------------------------------------------------------------
def test_audit_fails_closed_with_terminal_c(audit):
    """CURRENT: the accepted Issue #68 operator gap is not reproducible under
    Route A, so the read-only audit fails closed with ``TERMINAL_C`` (mixed /
    unresolved provenance) and an explicit failure reason rather than
    attesting a mechanism from non-reproducible data."""
    r, _ = audit
    assert r.terminal == CURRENT_ROUTE_A_TERMINAL
    assert r.terminal == m.TERMINAL_C
    assert r.failure_detail is not None
    assert set(r.failure_detail) == {"reason"}
    assert r.failure_detail["reason"] == CURRENT_ROUTE_A_FAILURE_ALPHA_HALF
    # HISTORICAL attribution stays distinct from the current terminal
    assert r.terminal != HISTORICAL_ISSUE69_TERMINAL_A
    assert r.terminal != m.TERMINAL_A
    assert r.terminal != m.TERMINAL_BLOCKED


def test_failure_message_carries_the_current_zero_gap_measurement(audit):
    """The fail-closed message is itself the current-runtime evidence: the
    measured rowwise operator gap is ``0.0`` with NO divergent rows, against the
    preserved historical accepted baseline ``0.6718037653783657`` / ``(452,453)``
    which is quoted verbatim as HISTORY, not as a current expectation."""
    r, _ = audit
    reason = r.failure_detail["reason"]
    assert reason.startswith("alpha_half: accepted Issue #68 gap/rows not "
                            "reproduced")
    assert f"gap={CURRENT_ROUTE_A_Q_GAP!r}" in reason
    assert f"vs {HISTORICAL_ISSUE68_GAP_HALF!r}" in reason
    assert "rows=[]" in reason
    assert f"vs {list(HISTORICAL_ISSUE68_ROWS_HALF)}" in reason


def test_failed_audit_records_no_trial_and_no_mechanism(audit):
    """Every downstream claim is left at its un-established default: no trial
    evidence, no provenance attestation, no established mechanism, and no
    accepted iterate."""
    r, _ = audit
    assert r.iterations == 0
    assert r.trial_count == 0
    assert r.trials == []
    assert r.provenance == {}
    assert r.wall_state == {}
    assert np.isnan(r.final_statistic)
    assert np.isnan(r.min_boundary_pb_star)
    assert np.isnan(r.r_inf)
    assert np.isnan(r.tangent_identity_residual)
    # NO mechanism is established from non-reproducible data
    assert r.iter_rate_path_source_backed is False
    assert r.final_raw_path_source_backed is False
    assert r.rate_formulas_globally_equivalent is False
    assert r.sign_or_branch_divergence_established is False
    assert r.truncation_or_destination_divergence_established is False
    assert r.other_mechanism_established is False
    assert r.mixed_or_unresolved is False
    assert r.a_axis_rates_identical_all_rows is False
    # never an accepted iterate
    assert r.accepted_new_hjb_iterate is False


def test_fail_closed_when_gap_not_reproduced(recon):
    """A measured operator gap that matches NEITHER the current zero-gap runtime
    NOR the supplied accepted baseline must fail closed, never silently pass.

    The current ``final=True`` operator is perturbed only to synthesize a
    genuine non-zero rowwise gap, so the regression guard itself is exercised
    rather than the lawful zero-gap path.
    """
    solver = recon["solver"]
    V_star, labor0, rho = recon["V_star"], recon["labor0"], recon["rho"]
    V_flat = V_star.ravel(order="F")
    Q0, u0, _d0, _r0 = solver.build_operator_and_u(
        V_star, labor0, 0.0, 0.0, final=False)
    R0 = rho * V_flat - (u0 + Q0.dot(V_flat))
    d_n = linalg.spsolve(
        rho * sparse.eye(solver.state_size, format="csr") - Q0, -R0)
    gvec = limiting_wall_gradient(solver, m.WALL_NODE, m.WALL_NZ)
    d_t = m.single_wall_tangent_projection(d_n, gvec)["d_T"]

    real = solver.build_operator_and_u
    f0_rows = m._f0_rows_of(solver)

    def perturbed(V, labor0v, ti, brg, final=False, f0_policies=None):
        Q, u, diag, recs = real(V, labor0v, ti, brg, final=final,
                                f0_policies=f0_policies)
        if final:
            Q = Q.tolil(copy=True)
            r = int(f0_rows[0])
            Q[r, r] = Q[r, r] + 0.5
            Q = Q.tocsr()
        return Q, u, diag, recs

    with patch.object(solver, "build_operator_and_u", side_effect=perturbed):
        # a real non-zero gap matching neither the current zero-gap state nor
        # the supplied historical baseline must fail closed
        with pytest.raises(m.F0RatePathDivergenceFailure) as excinfo:
            m._audit_trial(solver, V_star, labor0, rho, d_t, "alpha_half",
                           ALPHA_HALF, HISTORICAL_ISSUE68_GAP_HALF,
                           HISTORICAL_ISSUE68_ROWS_HALF)
        assert "not reproduced" in str(excinfo.value)

    # the unperturbed zero-gap state is lawful against a zero-gap baseline and
    # must NOT raise (this is the CURRENT Route-A contract)
    trial = m._audit_trial(solver, V_star, labor0, rho, d_t, "alpha_half",
                           ALPHA_HALF, CURRENT_ROUTE_A_Q_GAP, ())
    assert trial.max_rowwise_q_difference == CURRENT_ROUTE_A_Q_GAP
    assert trial.q_row_divergent_row_count == 0
    assert trial.inconsistent_rows == ()
    assert trial.gap_reproduced is True
    assert trial.inconsistent_row_set_match is True
    assert trial.total_f0_rows == 596
    assert trial.rate_identical_row_count == 596
    assert trial.diagonal_divergent_row_count == 0
    assert trial.a_rate_divergent_row_count == 0
    assert trial.omitted_rate_divergent_row_count == 0
    assert trial.destination_layout_divergent_row_count == 0
    assert trial.decomposition_closed is True
    assert trial.same_controls_and_utility is True
    assert trial.all_rows_reproduced is True


def test_audit_with_historical_baseline_fails_closed(recon):
    """The frozen audit entry point is invoked with the HISTORICAL accepted
    baseline, and under Route A that baseline is no longer reproducible; the
    audit therefore reports the failure rather than the historical attribution.
    """
    r = m._run_from_reconstruction(recon)
    assert r.failure_detail is not None
    assert r.terminal == m.TERMINAL_C
    assert r.trials == [] and r.trial_count == 0
    # the HISTORICAL values remain available as module constants
    assert m.EXPECTED_GAP_HALF == HISTORICAL_ISSUE68_GAP_HALF
    assert m.EXPECTED_GAP_NEAR == HISTORICAL_ISSUE68_GAP_NEAR


# ---------------------------------------------------------------------------
# 5. source provenance is still source-backed and read-only
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
    """The cited anchors must really exist in the accepted sources.

    CURRENT-CONTRACT (Owner Route A): the iteration/oracle anchors are
    unchanged, but the final-validation F0 assembly no longer constructs rates
    from raw drift, so the raw-drift rate-mapping tokens are asserted against
    the PRE-ROUTE-A source (verifiable at the Issue #70 parent commit) instead
    of the current one.
    """
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
    # the accepted iteration F0 path still sources the iteration rates
    for token in ("iteration_b_backward_rate", "iteration_b_forward_rate",
                  "a_backward_rate", "a_forward_rate"):
        assert token in selected_q, token
    # CURRENT final-validation assembly is record-sourced and no longer CALLS
    # the raw-drift helper anywhere (it remains imported but is unused)
    assert "rec.row_entries" in selected_q
    assert "float(rec.diagonal)" in selected_q
    tree = ast.parse(selected_q)
    drift_calls = [n for n in ast.walk(tree)
                   if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                   and n.func.id == "asset_drifts_matlab_faithful"]
    assert drift_calls == [], "raw-drift reconstruction must be gone"
    # HISTORICAL pre-Route-A raw-drift assembly, verifiable at the parent commit
    pre = subprocess.run(
        ["git", "show", f"HEAD~1:{SELECTED_Q_RELPATH}"],
        cwd=repo_root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=True).stdout
    for token in ("asset_drifts_matlab_faithful", "max(-mu_a_v, 0.0) / self.da",
                  "max(-mu_b_v, 0.0) / self.db"):
        assert token in pre, token


def test_liquid_branch_gating_is_the_source_backed_condition(f0_row_evidence):
    """The current runtime confirms the source-backed condition: on every
    affected row the liquid branch is bound FORWARD (``liquid_label == 'F'``)
    while the realized ``mu_b`` points BACKWARD, which is exactly the recorded
    ``sign_or_branch`` divergence condition.
    """
    for label in ("alpha_half", "alpha_near"):
        details = f0_row_evidence[label]["details"]
        for r in (452, 453):
            info = details[r]
            assert info["liquid_label"] == "F"
            assert info["raw_mu_b"] < 0.0
            assert info["it_bf"] > 0.0 and info["raw_bf"] == 0.0


# ---------------------------------------------------------------------------
# 6. execution design + determinism + forbidden machinery
# ---------------------------------------------------------------------------
def test_exactly_two_builds_per_trial(recon):
    """The audit design is unchanged: ONE base build, ONE required-``p_b`` build,
    plus TWO builds (ONE ``final=False`` re-selection, ONE corrected
    ``final=True`` build that REUSES the supplied selected records) for the FIRST
    frozen trial, at which the Route-A reproduction gate then fails closed. The
    audit therefore never reaches the second trial."""
    solver = recon["solver"]
    seen: list[dict] = []
    real = solver.build_operator_and_u

    def counting(V, labor0v, ti, brg, final=False, f0_policies=None):
        seen.append({"final": final, "reuses_records": f0_policies is not None})
        return real(V, labor0v, ti, brg, final=final, f0_policies=f0_policies)

    with patch.object(solver, "build_operator_and_u", side_effect=counting):
        r = m._run_from_reconstruction(recon)
    assert len(seen) == 3      # base + p_b probe + trial 1, then fail closed
    assert sum(1 for c in seen if c["final"] is False) == 2
    assert sum(1 for c in seen if c["final"] is True) == 1
    # exactly ONE build reuses the supplied selected records (the Route-A
    # final-validation assembly), and it is the final=True build
    reuse = [c for c in seen if c["reuses_records"]]
    assert len(reuse) == 1 and reuse[0]["final"] is True
    assert r.failure_detail is not None
    assert r.trials == []


def test_exactly_two_builds_per_frozen_trial(recon, d_t_direction):
    """Each frozen trial, taken on its own, performs exactly TWO operator builds:
    ONE ``final=False`` re-selection and ONE corrected ``final=True`` build that
    reuses the supplied selected records. No extra build exists for
    search/tuning, and no third build is ever performed per trial."""
    solver = recon["solver"]
    seen: list[dict] = []
    real = solver.build_operator_and_u

    def counting(V, labor0v, ti, brg, final=False, f0_policies=None):
        seen.append({"final": final, "reuses_records": f0_policies is not None})
        return real(V, labor0v, ti, brg, final=final, f0_policies=f0_policies)

    with patch.object(solver, "build_operator_and_u", side_effect=counting):
        trial = m._audit_trial(solver, recon["V_star"], recon["labor0"],
                               recon["rho"], d_t_direction, "alpha_half",
                               ALPHA_HALF, CURRENT_ROUTE_A_Q_GAP, ())
    assert len(seen) == 2
    assert [c["final"] for c in seen] == [False, True]
    assert [c["reuses_records"] for c in seen] == [False, True]
    assert trial.total_f0_rows == 596


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
    # _audit_trial (invoked once per frozen trial -> FIVE runtime calls before
    # the Route-A reproduction gate fails closed, asserted by the spy above)
    builds = [n for n in ast.walk(tree)
              if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
              and n.func.attr == "build_operator_and_u"]
    assert len(builds) == 3


def test_module_is_unmodified_by_route_a():
    """This migration must NOT touch the read-only Issue #69 audit module: it is
    outside the authorized path set, so its fail-closed behaviour stands."""
    repo_root = Path(__file__).resolve().parents[1]
    relpath = ("src/deep_learning_hank/two_asset/"
               "f0_rate_path_divergence_audit.py")
    out = subprocess.run(
        ["git", "rev-parse", f"HEAD:{relpath}"],
        cwd=repo_root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=True)
    assert out.stdout.strip() == "83e9be0febcc03eb721265d3558887bd6b1586a4"
    # and the working tree matches the committed blob (no uncommitted edit)
    dirty = subprocess.run(
        ["git", "diff", "--name-only", "HEAD", "--", relpath],
        cwd=repo_root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=True)
    assert dirty.stdout.strip() == ""
