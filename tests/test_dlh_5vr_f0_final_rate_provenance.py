"""Issue #66 / DLH-5V-R — F0 `final=True` rate-construction provenance and
operator-consistency audit test suite.

--------------------------------------------------------------------------
POST-REPAIR TEST-CONTRACT MIGRATION (Issue #67 / DLH-5V-S remediation)
--------------------------------------------------------------------------
Issue #66 audited and was accepted on the defect itself: the accepted
``final=True`` F0 off-diagonal assembly dropped the z-block destination offset
for z=1 rows (``cols.append(dn)``). Issue #67 then repaired that one
Owner-authorized source location, which necessarily changes the numbers this
suite historically pinned.

Nothing is deleted. The pre-repair numbers are preserved as EXPLICIT
HISTORICAL CONSTANTS representing accepted Issue #66 evidence (including its
historical Terminal A), and the runtime assertions now verify the REPAIRED
semantics. The historical defect is NOT re-created here (no monkeypatch, no
old-blob checkout): its reproducibility is preserved by the accepted Issues,
reports and commits, not by the live regression gate.

Re-running the Issue #66 diagnostic against the repaired current source is NOT
forced to return the historical terminal; the audit's classifications are
asserted on the repaired source, and its historical Terminal A is retained as
historical evidence.

The convergence question is untouched: the corrected final residual
(``10.435094313164921``) is still far above the unchanged Bellman tolerance
(``1e-3``), so validated HJB convergence remains FALSE.

Mandated verification surface (Issue #66 sections 9-10, migrated):

1. exact deterministic reconstruction of the accepted Issue #63 stagnation
   state (final statistic ~3.6614352438846254e-08; required boundary p_b
   ~4.8089461301970005e-09; wall F3 (13,13) z=1);
2. same current selected F0 controls for the ITER and FINAL builds;
3. exact reproduction of ||R_iter||_inf = 10.435094313164921 (UNCHANGED);
4. corrected current-record ||R_final_current||_inf = 10.435094313164921
   (pre-repair historical value preserved as a constant);
5. corrected F0 rowwise max |Q_final_current - Q_iter| = 1.42e-14
   (pre-repair historical value 24.601971766296664 preserved as a constant);
6. b/a directional rate extraction per F0 row (b_backward / b_forward /
   a_backward / a_forward), with the measured rate-coincidence and
   destination-assembly decomposition of the gap;
7. diagonal construction identity;
8. represented/omitted destination accounting (rep_out + omitted == -diag;
   omitted == 0 on every F0 row);
9. source-backed MATLAB/oracle provenance mapping is deterministic;
10. ex ante classifications are deterministic and yield exactly ONE terminal;
11. utility/source terms identical under the same current controls
    (independent of the rate-construction comparison);
12. non-F0 boundary rows identical between the two builds;
13. non-finite evidence / provenance ambiguity fail closed;
14. deterministic repeat is bit-identical;
15. no new iterate / Newton / continuation / line search / KFE /
    steady-state machinery (static AST scan + exactly two
    ``build_operator_and_u`` calls in the module).

Plus a runtime counting spy asserting the audit executes exactly two
operator builds at V_* (the reconstruction's internal builds are part of the
ONE reconstruction; the two builds here are the authorized scientific pair).
"""

from __future__ import annotations

import ast
import dataclasses
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pytest

import deep_learning_hank.two_asset.f0_final_rate_provenance_audit as audit

MODULE_PATH = Path(audit.__file__)
MODULE_SOURCE = MODULE_PATH.read_text(encoding="utf-8")

FINAL_STAT_EXPECTED = 3.6614352438846254e-08
MIN_PB_EXPECTED = 4.8089461301970005e-09
R_ITER_INF_EXPECTED = 10.435094313164921

# ---------------------------------------------------------------------------
# HISTORICAL EVIDENCE — accepted Issue #64/#65/#66 pre-repair numbers.
# Retained as accepted scientific evidence; superseded as runtime expectations
# by the Owner-authorized Issue #67 z-block destination repair.
# ---------------------------------------------------------------------------
PRE_REPAIR_FINAL_RESIDUAL_CURRENT = 490.7560414005864
PRE_REPAIR_FINAL_RESIDUAL_STALE = 490.7560425919994
PRE_REPAIR_F0_OPERATOR_GAP = 24.601971766296664
PRE_REPAIR_AFFECTED_Z1_F0_ROWS = 298
PRE_REPAIR_DESTINATION_ASSEMBLY_MAX_DIFF = 24.601971766296664
PRE_REPAIR_F0_GAP_NODE = 297
PRE_REPAIR_TERMINAL_A = "DLH_5VR_F0_FINAL_RATE_PROVENANCE__ITERATION_OPERATOR_MATCHES_ACCEPTED_MATLAB_FAITHFUL_HJB__FINAL_RAW_RATE_OPERATOR_NON_EQUIVALENT__VALIDATION_OPERATOR_REDESIGN_REVIEW_GATE_READY"

# ---------------------------------------------------------------------------
# REPAIRED SEMANTICS — current runtime expectations at the same accepted V_*.
# ---------------------------------------------------------------------------
REPAIRED_R_FINAL_CURRENT_INF = 10.435094313164921
REPAIRED_F0_OPERATOR_GAP = 1.4210854715202004e-14
REPAIRED_DESTINATION_ASSEMBLY_AFFECTED_ROWS = 0
REPAIRED_AFFECTED_Z1_F0_ROWS = 0
REPAIRED_FINAL_VS_ITER_TOL = 1.0e-9
BELLMAN_TOLERANCE_UNCHANGED = 1.0e-3

BANNED_TOKENS = (
    "newton", "continuation", "linesearch", "armijo", "damp", "clip", "floor",
    "maximum", "minimum", "trust_region", "semismooth", "policy_iteration",
    "spsolve", "construct_ftb_step", "trial", "kfe", "stationary",
    "steady_state", "solve_household_steady_state",
)


# ---------------------------------------------------------------------------
# fixtures
# ---------------------------------------------------------------------------
@pytest.fixture(scope="module")
def audit_result():
    """(result, repeat_identical) from one full audit + one deterministic
    repeat of the full diagnostic (two complete reconstructions)."""
    r, ident = audit.run_issue66_audit_twice()
    return r, ident


@pytest.fixture(scope="module")
def recon():
    """ONE accepted-state reconstruction, shared by the runtime spy and the
    fail-closed guard tests (never a scientific object here — the audit's own
    reconstruction is the one reported)."""
    return audit.reconstruct_issue63_stagnation_state()


# ---------------------------------------------------------------------------
# 1. exact reconstruction
# ---------------------------------------------------------------------------
def test_reconstruction_exact(audit_result):
    r, _ = audit_result
    assert r.failure_detail is None
    assert r.iterations == audit.RECONSTRUCT_STEPS == 8
    assert r.final_statistic is not None
    assert r.final_statistic == pytest.approx(FINAL_STAT_EXPECTED, abs=1e-12)
    assert r.min_boundary_pb_star == pytest.approx(MIN_PB_EXPECTED, abs=1e-12)
    assert r.wall_state["family"] == "F3"
    assert r.wall_state["j"] == 13 and r.wall_state["i"] == 13
    assert r.wall_state["z"] == 1


# ---------------------------------------------------------------------------
# 2. same current controls for ITER and FINAL
# ---------------------------------------------------------------------------
def test_same_current_controls(audit_result):
    r, _ = audit_result
    assert r.same_controls_max_abs_diff == 0.0
    assert r.f0_row_count == 596
    it = r.iter_components
    fn = r.final_components
    # per-row utility and drift controls identical (same selected records)
    assert float(np.max(np.abs(it["utility"] - fn["utility"]))) == 0.0
    assert float(np.max(np.abs(it["omitted_destination_rate"]
                              - fn["omitted_destination_rate"]))) == 0.0


# ---------------------------------------------------------------------------
# 3. exact R_iter
# ---------------------------------------------------------------------------
def test_r_iter_exact(audit_result):
    r, _ = audit_result
    assert r.r_iter_inf == pytest.approx(R_ITER_INF_EXPECTED, abs=1e-12)
    assert r.r_iter_argmax["family"] == "F0"
    assert r.r_iter_f0_max == r.r_iter_inf


# ---------------------------------------------------------------------------
# 4. exact current-record R_final_current
# ---------------------------------------------------------------------------
def test_r_final_current_exact(audit_result):
    r, _ = audit_result
    # PRE-REPAIR this was PRE_REPAIR_FINAL_RESIDUAL_CURRENT == 490.7560414005864.
    # After the Issue #67 z-block destination repair the corrected final
    # operator agrees with the iteration operator to machine precision.
    assert r.r_final_current_inf == pytest.approx(REPAIRED_R_FINAL_CURRENT_INF,
                                                  abs=1e-12)
    assert (r.r_final_current_inf
            != pytest.approx(PRE_REPAIR_FINAL_RESIDUAL_CURRENT, rel=1e-3))
    assert r.r_final_current_inf == pytest.approx(r.r_iter_inf,
                                                  abs=REPAIRED_FINAL_VS_ITER_TOL)
    assert r.r_final_current_argmax["family"] == "F0"
    assert r.r_final_current_f0_max == r.r_final_current_inf


# ---------------------------------------------------------------------------
# 5. corrected F0 operator gap (pre-repair ~24.60 removed by the repair)
# ---------------------------------------------------------------------------
def test_f0_gap_exact(audit_result):
    r, _ = audit_result
    # PRE-REPAIR the F0 rowwise max |Q_final_current - Q_iter| was
    # PRE_REPAIR_F0_OPERATOR_GAP == 24.601971766296664 at F0 node 297 (11,11) z=1.
    # Issue #67's authorized destination repair removed that cross-z gap.
    assert r.f0_rowwise_max_abs_gap == pytest.approx(REPAIRED_F0_OPERATOR_GAP,
                                                     abs=1e-15)
    assert r.f0_rowwise_max_abs_gap <= REPAIRED_FINAL_VS_ITER_TOL
    assert (r.f0_rowwise_max_abs_gap
            != pytest.approx(PRE_REPAIR_F0_OPERATOR_GAP, rel=1e-3))
    assert r.f0_rowwise_max_abs_gap_state is not None
    assert r.f0_rowwise_max_abs_gap_state["family"] == "F0"


# ---------------------------------------------------------------------------
# 6. b/a directional extraction and gap decomposition
# ---------------------------------------------------------------------------
def test_directional_extraction_and_gap_decomposition(audit_result):
    r, _ = audit_result
    for nm in ("b_backward", "b_forward", "a_backward", "a_forward",
               "diagonal", "represented_outgoing_sum",
               "omitted_destination_rate", "utility"):
        cls = getattr(r, "class_" + nm)
        assert cls is not None
        assert np.isfinite(cls["max_abs_diff"])
    # rate/operator component classes: the accepted iteration b-rates coincide
    # with max(+-mu_b)/db and the a-rates with max(+-mu_a)/da on every F0 row;
    # AFTER the repair the destination-assembly class also disappears
    for nm in ("b_backward", "b_forward", "a_backward", "a_forward",
               "diagonal", "represented_outgoing_sum",
               "omitted_destination_rate", "utility"):
        assert getattr(r, "class_" + nm)["affected_row_count"] == 0
        assert getattr(r, "class_" + nm)["max_abs_diff"] <= audit.CLASS_TOL
    # PRE-REPAIR the entire operator gap decomposed into the
    # destination-assembly class: PRE_REPAIR_AFFECTED_Z1_F0_ROWS == 298 z=1 F0
    # rows were affected at the bare-node placement. After the Issue #67
    # repair that class is empty.
    asm = r.class_destination_assembly_gap
    assert asm["affected_row_count"] == REPAIRED_AFFECTED_Z1_F0_ROWS == 0
    assert asm["affected_row_count"] != PRE_REPAIR_AFFECTED_Z1_F0_ROWS
    assert asm["max_abs_diff"] <= audit.CLASS_TOL
    assert asm["argmax_state"] is None
    # the accepted-FINAL vs MATLAB-faithful-post row assembly deviation is
    # measured against the audit's historical bare-dn reference, so it still
    # reports the pre-repair magnitude as HISTORICAL evidence
    assert r.destination_assembly_max_abs_diff == pytest.approx(
        PRE_REPAIR_DESTINATION_ASSEMBLY_MAX_DIFF, abs=1e-9)
    assert r.destination_assembly_affected_row_count == (
        PRE_REPAIR_AFFECTED_Z1_F0_ROWS)


# ---------------------------------------------------------------------------
# 7. diagonal construction identity
# ---------------------------------------------------------------------------
def test_diagonal_identity(audit_result):
    r, _ = audit_result
    it = r.iter_components
    fn = r.final_components
    for comp in (it, fn):
        diag = -comp["diagonal"]
        rate_sum = (comp["b_backward"] + comp["b_forward"]
                    + comp["a_backward"] + comp["a_forward"])
        assert float(np.max(np.abs(diag - rate_sum))) <= 1e-12
    assert r.class_diagonal["max_abs_diff"] <= 1e-12


# ---------------------------------------------------------------------------
# 8. represented / omitted destination accounting
# ---------------------------------------------------------------------------
def test_represented_omitted_accounting(audit_result):
    r, _ = audit_result
    it = r.iter_components
    fn = r.final_components
    for comp in (it, fn):
        # accounting identity: represented_outgoing_sum + omitted == -diagonal
        assert float(np.max(np.abs(
            comp["represented_outgoing_sum"] + comp["omitted_destination_rate"]
            + comp["diagonal"]))) <= 1e-12
        # F0 rows are strictly interior with all four neighbors -> omitted == 0
        assert float(np.max(np.abs(comp["omitted_destination_rate"]))) == 0.0
    assert len(r.f0_rows_array) == 596


# ---------------------------------------------------------------------------
# 9. provenance mapping deterministic
# ---------------------------------------------------------------------------
def test_provenance_mapping_deterministic():
    p1 = audit.provenance_mapping()
    p2 = audit.provenance_mapping()
    assert p1 == p2
    for key in ("iter_f0_row", "final_raw_f0_row", "destination_truncation",
                "derivatives", "switch_matrix"):
        assert key in p1
    # source-backed references (no re-interpretation)
    assert "boundary_hjb_selected_q.py:484-521" in p1["iter_f0_row"]["selected_q"]
    assert "matlab_faithful_two_asset_ha.py:193-416" in p1["iter_f0_row"]["oracle"]
    assert "boundary_hjb_selected_q.py:978" in p1["final_raw_f0_row"]["destination_columns"]
    assert "matlab_faithful_two_asset_ha.py:562" in p1["final_raw_f0_row"]["rates"]


# ---------------------------------------------------------------------------
# 10. classification deterministic, exactly one terminal
# ---------------------------------------------------------------------------
def test_classification_deterministic(audit_result):
    r, _ = audit_result
    # The rates are oracle-faithful in both cases (unchanged by the repair).
    assert r.iter_eq_matlab is True
    assert r.final_eq_rate_formula is True
    # The Issue #66 audit's OWN internal MATLAB-faithful reference still places
    # F0 destinations at bare column `dn` (that is what Issue #66 was auditing).
    # The repaired live source — and the source-true oracle — place them at
    # `nz*n + dn`, so the audit's assembly comparison against its own
    # historical reference still reports a mismatch. This is a statement about
    # the audit's reference, not about the repaired source.
    assert r.final_eq_matlab is False
    assert r.final_eq_assembly is False
    # Under the REPAIRED current source the two operators are equivalent and
    # the material non-equivalence has been removed.
    assert r.both_equivalent is True
    assert r.materially_non_equivalent is False
    assert r.mixed_or_unresolved is False
    # Running the Issue #66 diagnostic against the repaired source is NOT
    # forced to return the historical terminal; its historical Terminal A
    # (PRE_REPAIR_TERMINAL_A) is retained as historical accepted evidence.
    assert r.outcome != PRE_REPAIR_TERMINAL_A
    assert r.outcome in (audit.TERMINAL_A, audit.TERMINAL_B, audit.TERMINAL_C)
    # exactly one terminal across the frozen rule set
    assert [r.outcome == t for t in (audit.TERMINAL_A, audit.TERMINAL_B,
                                     audit.TERMINAL_C)].count(True) == 1


def test_no_hjb_convergence_claimed_after_repair(audit_result):
    """Corrected final == R_iter is an OPERATOR statement, not convergence.

    The corrected residual still exceeds the UNCHANGED Bellman tolerance by
    four orders of magnitude, so validated HJB convergence remains FALSE.
    """
    r, _ = audit_result
    assert r.r_final_current_inf == pytest.approx(REPAIRED_R_FINAL_CURRENT_INF,
                                                  abs=1e-12)
    assert r.r_iter_inf == pytest.approx(R_ITER_INF_EXPECTED, abs=1e-12)
    assert r.r_iter_inf > BELLMAN_TOLERANCE_UNCHANGED
    assert r.r_final_current_inf > BELLMAN_TOLERANCE_UNCHANGED
    assert r.r_iter_inf / BELLMAN_TOLERANCE_UNCHANGED > 1.0e4
    assert not (r.r_final_current_inf <= BELLMAN_TOLERANCE_UNCHANGED)
    assert not (r.r_iter_inf <= BELLMAN_TOLERANCE_UNCHANGED)


# ---------------------------------------------------------------------------
# 11. utility/source equivalence (independent)
# ---------------------------------------------------------------------------
def test_utility_source_equivalent(audit_result):
    r, _ = audit_result
    # F0 utility/source identical under the same current controls
    assert r.utility_f0_max_abs_diff == 0.0
    # boundary u identical
    assert r.boundary_u_max_abs_diff == 0.0
    assert float(np.max(np.abs(
        r.iter_components["utility"] - r.final_components["utility"]))) == 0.0


# ---------------------------------------------------------------------------
# 12. non-F0 boundary rows identical
# ---------------------------------------------------------------------------
def test_non_f0_boundary_rows_identical(audit_result):
    r, _ = audit_result
    assert r.boundary_row_max_abs_diff == 0.0
    assert r.boundary_row_max_abs_diff <= audit.ROW_EQ_TOL


# ---------------------------------------------------------------------------
# 13. non-finite / provenance ambiguity fail closed
# ---------------------------------------------------------------------------
def test_fail_closed_nonfinite(recon):
    solver = recon["solver"]
    V_star, labor0, rho = recon["V_star"], recon["labor0"], recon["rho"]
    real = solver.build_operator_and_u

    def nan_final(V, labor0v, ti, brg, final=False, f0_policies=None):
        Q, u, diag, recs = real(V, labor0v, ti, brg, final=final,
                                f0_policies=f0_policies)
        if final:
            u = np.array(u, dtype=float, copy=True)
            u[0] = np.nan
        return Q, u, diag, recs

    with patch.object(solver, "build_operator_and_u", side_effect=nan_final):
        with pytest.raises(audit.F0FinalRateProvenanceFailure):
            audit.build_two_operators(solver, V_star, labor0, rho)


def test_fail_closed_provenance_ambiguity(recon):
    solver = recon["solver"]
    V_star, labor0, rho = recon["V_star"], recon["labor0"], recon["rho"]
    real = solver.build_operator_and_u
    _, f0_rows = audit.f0_rows_of(solver)
    missing = int(f0_rows[0])

    def missing_record(V, labor0v, ti, brg, final=False, f0_policies=None):
        Q, u, diag, recs = real(V, labor0v, ti, brg, final=final,
                                f0_policies=f0_policies)
        if not final:
            recs = list(recs)
            recs[missing] = None
        return Q, u, diag, recs

    with patch.object(solver, "build_operator_and_u", side_effect=missing_record):
        with pytest.raises(audit.F0FinalRateProvenanceFailure):
            audit.build_two_operators(solver, V_star, labor0, rho)


# ---------------------------------------------------------------------------
# 14. deterministic repeat identical
# ---------------------------------------------------------------------------
def test_deterministic_repeat_identical(audit_result):
    r, ident = audit_result
    assert ident is True
    assert r.deterministic_repeat_identical is True


# ---------------------------------------------------------------------------
# 15. no forbidden iterate / Newton / continuation / line search / KFE /
# steady-state machinery (static scan) + exactly two build calls
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
    # exactly two explicit operator builds in the module source
    calls = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "build_operator_and_u"
    ]
    assert len(calls) == 2
    # the two calls are the ITER build and the FINAL build inside
    # build_two_operators
    func = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                and n.name == "build_two_operators")
    func_calls = [
        node for node in ast.walk(func)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "build_operator_and_u"
    ]
    assert len(func_calls) == 2
    # no spsolve / direct linear solve of the full operator
    assert not any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                   and n.func.id == "spsolve" for n in ast.walk(tree))


def test_runtime_exactly_two_builds_at_vstar(recon):
    solver = recon["solver"]
    V_star, labor0, rho = recon["V_star"], recon["labor0"], recon["rho"]
    with patch.object(solver, "build_operator_and_u",
                      wraps=solver.build_operator_and_u) as spy:
        two = audit.build_two_operators(solver, V_star, labor0, rho)
    assert spy.call_count == 2
    finals = [c.kwargs.get("final") for c in spy.call_args_list]
    assert sorted(finals) == [False, True]
    # PRE-REPAIR this gap was PRE_REPAIR_F0_OPERATOR_GAP == 24.601971766296664;
    # the Issue #67 destination repair reduced it to machine precision
    assert two["f0_rowwise_max_abs_gap"] == pytest.approx(
        REPAIRED_F0_OPERATOR_GAP, abs=1e-15)
