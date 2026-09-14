"""Issue #66 / DLH-5V-R — F0 `final=True` rate-construction provenance and
operator-consistency audit test suite.

Mandated verification surface (Issue #66 sections 9-10):

1. exact deterministic reconstruction of the accepted Issue #63 stagnation
   state (final statistic ~3.6614352438846254e-08; required boundary p_b
   ~4.8089461301970005e-09; wall F3 (13,13) z=1);
2. same current selected F0 controls for the ITER and FINAL builds;
3. exact reproduction of ||R_iter||_inf = 10.435094313164921;
4. exact reproduction of the current-record ||R_final_current||_inf =
   490.7560414005864;
5. exact reproduction of the F0 rowwise max |Q_final_current - Q_iter|
   ~= 24.6019717663;
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
R_FINAL_CURRENT_INF_EXPECTED = 490.7560414005864
F0_GAP_EXPECTED = 24.601971766296664

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
    assert r.r_final_current_inf == pytest.approx(R_FINAL_CURRENT_INF_EXPECTED,
                                                  abs=1e-9)
    assert r.r_final_current_argmax["family"] == "F0"
    assert r.r_final_current_f0_max == r.r_final_current_inf


# ---------------------------------------------------------------------------
# 5. exact ~24.60 F0 operator gap
# ---------------------------------------------------------------------------
def test_f0_gap_exact(audit_result):
    r, _ = audit_result
    assert r.f0_rowwise_max_abs_gap == pytest.approx(F0_GAP_EXPECTED, abs=1e-9)
    assert r.f0_rowwise_max_abs_gap_state["family"] == "F0"
    assert r.f0_rowwise_max_abs_gap_state["node"] == 297
    assert r.f0_rowwise_max_abs_gap_state["j"] == 11
    assert r.f0_rowwise_max_abs_gap_state["i"] == 11
    assert r.f0_rowwise_max_abs_gap_state["z"] == 1


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
    # with max(+-mu_b)/db and the a-rates with max(+-mu_a)/da on every F0 row
    for nm in ("b_backward", "b_forward", "a_backward", "a_forward",
               "diagonal", "represented_outgoing_sum",
               "omitted_destination_rate", "utility"):
        assert getattr(r, "class_" + nm)["affected_row_count"] == 0
        assert getattr(r, "class_" + nm)["max_abs_diff"] <= audit.CLASS_TOL
    # the entire operator gap decomposes into the destination-assembly class:
    # the accepted final=True F0 row places z=1 destinations at bare node
    # columns without the z-block offset (affected rows == z=1 F0 rows)
    asm = r.class_destination_assembly_gap
    assert asm["affected_row_count"] == 298
    assert asm["max_abs_diff"] == pytest.approx(F0_GAP_EXPECTED, abs=1e-9)
    assert asm["argmax_state"]["node"] == 297 and asm["argmax_state"]["z"] == 1
    # argmax-row attribution: the differing columns are the same two rates
    # placed at the two distinct destinations (cols_diff = 2 directions x 2
    # placements)
    assert r.max_row_argmax_component == "b_backward"
    contrib = r.max_row_component_contributions
    assert contrib["b_backward"] == pytest.approx(F0_GAP_EXPECTED, abs=1e-9)
    assert contrib["a_forward"] == pytest.approx(9.52637251075067, abs=1e-9)
    assert contrib["diagonal"] == 0.0
    assert contrib["switch_matrix_or_other"] == 0.0
    assert r.max_row_columns_with_diff == 4
    assert r.max_total_row_entry_diff == pytest.approx(F0_GAP_EXPECTED, abs=1e-9)
    # accepted-FINAL vs MATLAB-faithful-post row assembly deviation
    assert r.destination_assembly_max_abs_diff == pytest.approx(
        F0_GAP_EXPECTED, abs=1e-9)
    assert r.destination_assembly_affected_row_count == 298


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
    assert r.iter_eq_matlab is True
    assert r.final_eq_matlab is False
    assert r.final_eq_rate_formula is True   # rates ARE the oracle post formula
    assert r.final_eq_assembly is False      # assembled row is NOT MATLAB-faithful
    assert r.both_equivalent is False
    assert r.mixed_or_unresolved is False
    assert r.materially_non_equivalent is True
    assert r.outcome == audit.TERMINAL_A
    assert r.outcome != audit.TERMINAL_B and r.outcome != audit.TERMINAL_C
    assert r.outcome != audit.TERMINAL_BLOCKED
    # exactly one terminal across the frozen rule set
    assert [r.outcome == t for t in (audit.TERMINAL_A, audit.TERMINAL_B,
                                     audit.TERMINAL_C)].count(True) == 1


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
    assert two["f0_rowwise_max_abs_gap"] == pytest.approx(F0_GAP_EXPECTED,
                                                          abs=1e-9)
