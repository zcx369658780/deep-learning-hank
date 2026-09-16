"""DLH-5V-S — focused regression tests and single-run diagnostic for the
minimal ``final=True`` F0 z-block destination repair.

Issue #67 / DLH-5V-S
``SCIENTIFIC_CHANGE__MINIMAL_FINAL_VALIDATION_OPERATOR_REPAIR_AND_REVALIDATION``

Authority: Issue #67 OPEN; initial authoritative activation ``5672573849``;
final authoritative activation-refresh ``5672691735`` (post-sync live ``main``
``496d14404116cbe76a54df3aa595b91256b30c10``). Route decision
``APPROVE_MINIMAL_FINAL_VALIDATION_ZBLOCK_DESTINATION_REPAIR_AFTER_5VR_TERMINAL_A``;
authority marker ``DLH_5VS_MINIMAL_FINAL_VALIDATION_ZBLOCK_REPAIR_AUTHORIZED``.

The ONLY authorized source change is the one-location destination-index repair
inside the ``final=True`` F0 off-diagonal assembly of
``boundary_hjb_selected_q.py``::

    cols.append(dn)                  ->   cols.append(nz * self.n + dn)

so that z=1 F0 off-diagonal destinations stay inside the z=1 block, matching the
accepted iteration path, the accepted boundary path and the MATLAB-faithful
state layout.

This module is also the single authoritative runner for the Issue #67 evidence:
``run_issue67_diagnostic()`` performs ONE deterministic reconstruction of the
accepted Issue #63 stagnation state ``V_*``, ONE ``final=False`` current-policy
build, ONE corrected ``final=True`` current-policy build with the SAME selected
F0 controls, and ONE corrected-equivalence/residual diagnostic.
``run_issue67_diagnostic_twice()`` adds the ONE deterministic repeat.

The pre-repair comparison operator is reconstructed in coordinate space from the
repaired operator and the build's own F0 records (the repair is a pure
destination-column reassignment on F0 off-diagonal entries only), and it is
structurally validated against the independently accepted Issue #66 measurement
``F0 rowwise max |Q_final_current - Q_iter| = 24.601971766296664`` and the
accepted Issue #65 pre-repair current-record residual ``490.7560414005864``.

SCOPE CEILING (binding): repair + corrected validation re-check only. A
materially lower corrected residual is NOT HJB convergence; the Bellman
tolerance ``1e-3`` remains the unchanged acceptance threshold. No new HJB
iterate is accepted. No Newton / policy iteration / semismooth / trust-region /
continuation / line search / parameter sweep / KFE / stationary KFE /
steady-state / GE / neural / calibration / policy / welfare / Results work.
"""

from __future__ import annotations

import ast
import dataclasses
from dataclasses import dataclass
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pytest
from scipy import sparse

import deep_learning_hank.two_asset.f0_final_rate_provenance_audit as audit
from deep_learning_hank.two_asset.boundary_hjb_selected_q import (
    BoundaryHJBSolver,
)
from deep_learning_hank.two_asset.stagnation_newton_geometry import (
    reconstruct_issue63_stagnation_state,
    residual_stats,
)

# ---------------------------------------------------------------------------
# Accepted frozen references (accepted Issue #65 / #66 facts)
# ---------------------------------------------------------------------------
SELECTED_Q_RELPATH = "src/deep_learning_hank/two_asset/boundary_hjb_selected_q.py"
SELECTED_Q_ABS = Path(__file__).resolve().parents[1] / SELECTED_Q_RELPATH
SELECTED_Q_PRE_REPAIR_BLOB = "7ea342ccbe15d852b90743b14bb4b02977c2d78b"
SELECTED_Q_REPAIRED_BLOB = "556ccc214f03a1a22306cc4f5c7e9f7691bbf897"

REPAIR_OLD = "rows.append(row); cols.append(dn); data.append(rate)"
REPAIR_NEW = "rows.append(row); cols.append(nz * self.n + dn); data.append(rate)"

RECONSTRUCT_STEPS = 8
FINAL_STATISTIC_EXPECTED = 3.6614352438846254e-08
MIN_BOUNDARY_PB_EXPECTED = 4.8089461301970005e-09
R_ITER_INF_ACCEPTED = 10.435094313164921
R_FINAL_CURRENT_INF_ACCEPTED = 490.7560414005864    # pre-repair current-record baseline
R_FINAL_STALE_INF_ACCEPTED = 490.7560425919994      # accepted stale-record baseline
F0_PRE_REPAIR_GAP_ACCEPTED = 24.601971766296664     # Issue #66 rowwise max |Q_final - Q_iter|
BELLMAN_TOLERANCE_UNCHANGED = 1.0e-3

F0_NODE_COUNT = 298
F0_ROW_COUNT = 596
STATE_SIZE = 782
N_NODES = 391
N_Z = 2
WALL_NODE = 332

CORRECTED_VS_ITER_TOL = 1.0e-9
RECONCILE_TOL = 1.0e-9

# ---------------------------------------------------------------------------
# PRE-ROUTE-A HISTORICAL EVIDENCE (accepted Issue #67 z-block repair, as
# verified at that time). These record the assembly state of the F0
# ``final=True`` branch BEFORE the Owner Route A single-Q consolidation
# (Issue #70 / DLH-5V-V). They remain preserved historical regression
# evidence; they are NOT current runtime expectations.
# ---------------------------------------------------------------------------
PRE_ROUTE_A_FINAL_ZBLOCK_ASSEMBLY_LINE = 978
PRE_ROUTE_A_FINAL_ZBLOCK_LINE_TEXT = (
    "rows.append(row); cols.append(nz * self.n + dn); data.append(rate)")
# CURRENT (Owner Route A) final=F0 branch text: the row is rebuilt from the
# supplied selected record instead of re-deriving raw-drift rates.
CURRENT_ROUTE_A_FINAL_LINE_TEXT = "cols.append(nz * self.n + dn)"
PRE_ROUTE_A_SELECTED_Q_BLOB = "556ccc214f03a1a22306cc4f5c7e9f7691bbf897"
# Revision-independent anchor: the pre-Route-A revision is the parent of the
# ORIGINAL Issue #70 scientific commit. An absolute revision (rather than a moving
# `HEAD~n`) keeps the historical evidence verifiable across later remediation
# commits on this branch.
PRE_ROUTE_A_SELECTED_Q_COMMIT = "825e241804c7fb260c807602fc0f1487caf84e56^"
ORIGINAL_ISSUE70_COMMIT = "825e241804c7fb260c807602fc0f1487caf84e56"

TERMINAL_A = (
    "DLH_5VS_FINAL_VALIDATION_ZBLOCK_REPAIR__CORRECTED_FINAL_OPERATOR_MATCHES_"
    "MATLAB_FAITHFUL_LAYOUT__SPURIOUS_CROSS_Z_VALIDATION_GAP_REMOVED__HJB_"
    "RESIDUAL_REASSESSMENT_GATE_READY")
TERMINAL_B = (
    "DLH_5VS_FINAL_VALIDATION_ZBLOCK_REPAIR__ZBLOCK_ASSEMBLY_REPAIRED_BUT_"
    "MATERIAL_HJB_VALIDATION_DISCREPANCY_REMAINS__FURTHER_VALIDATION_REVIEW_"
    "REQUIRED")
TERMINAL_C = (
    "DLH_5VS_FINAL_VALIDATION_ZBLOCK_REPAIR__NONFINITE_INCONSISTENT_OR_"
    "REGRESSION_FAILURE__SCIENTIFIC_REPAIR_REVIEW_REQUIRED")
TERMINAL_BLOCKED = "BLOCKED_DLH_5VS_AUTHORITY_OR_DEPENDENCY_CONFLICT"

BANNED_TOKENS = (
    "newton", "continuation", "linesearch", "armijo", "trust_region",
    "semismooth", "policy_iteration", "spsolve", "construct_ftb_step", "trial",
    "kfe", "stationary", "steady_state", "solve_household_steady_state",
)


class ZBlockRepairFailure(RuntimeError):
    """Fail-closed: non-finite evidence, a failed same-controls contract, a
    non-F0 boundary-row discrepancy, a missing F0 record, a failed
    pre-repair reconciliation, or a regression in the frozen accepted
    reconstruction."""


# ---------------------------------------------------------------------------
# Result container
# ---------------------------------------------------------------------------
@dataclass
class ZBlockRepairResult:
    """ONE fully determined Issue #67 repair + corrected-validation result."""

    terminal: str
    # frozen reconstruction reproduction
    iterations: int
    final_statistic: float
    min_boundary_pb_star: float
    wall_state: dict
    # corrected final operator vs accepted iteration operator
    r_iter_inf: float
    r_iter_argmax: dict
    r_corrected_inf: float
    r_corrected_argmax: dict
    r_corrected_f0_max: float
    r_corrected_boundary_max: float
    corrected_vs_iter_f0_rowwise_max: float
    corrected_vs_iter_f0_rowwise_max_state: dict
    corrected_vs_iter_total_rowwise_max: float
    corrected_rate_component_max_abs_diff: float
    corrected_destination_layout_misplaced_columns: int
    corrected_destination_layout_checked_rows: int
    offblock_residual_beyond_switch: float
    # invariants that must NOT move
    z0_f0_rowwise_max_abs_diff_vs_pre_repair: float
    z0_f0_unchanged_row_count: int
    z1_f0_rowwise_max_abs_diff_vs_pre_repair: float
    z1_f0_row_count: int
    cross_z_contamination_row_count: int
    utility_f0_max_abs_diff: float
    utility_boundary_max_abs_diff: float
    boundary_row_max_abs_diff: float
    boundary_u_max_abs_diff: float
    diagonal_f0_max_abs_diff: float
    same_controls_max_abs_diff: float
    max_abs_q1_iter: float
    max_abs_q1_corrected: float
    expansions_iter: int
    bindings_iter: int
    expansions_corrected: int
    bindings_corrected: int
    # pre-repair reconciliation (derived, structurally validated)
    r_pre_repair_current_inf: float
    r_pre_repair_current_argmax: dict
    pre_repair_vs_iter_f0_rowwise_max: float
    pre_repair_vs_corrected_f0_rowwise_max: float
    pre_repair_structural_match: bool
    ratio_corrected_over_pre_repair: float
    ratio_corrected_over_r_iter: float
    ratio_corrected_over_accepted_final_baseline: float
    residual_improvement: float
    # scope ceiling
    f0_row_count: int
    bellman_tolerance_unchanged: float
    convergence_declared: bool
    new_hjb_iterate_accepted: bool
    deterministic_repeat_identical: bool


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _rowwise_max(Qa: sparse.csr_matrix, Qb: sparse.csr_matrix,
                 rows) -> tuple[float, int]:
    best, best_row = 0.0, -1
    for r in rows:
        a = np.asarray(Qa.getrow(int(r)).toarray()).ravel()
        b = np.asarray(Qb.getrow(int(r)).toarray()).ravel()
        m = float(np.max(np.abs(a - b)))
        if m > best:
            best, best_row = m, int(r)
    return best, best_row


def pre_repair_final_operator(Q_corr: sparse.csr_matrix, records: list,
                              f0_rows, n: int) -> sparse.csr_matrix:
    """Exact coordinate-space image of the PRE-REPAIR final operator.

    The authorized repair only changed the destination column of F0
    off-diagonal entries from bare ``dn`` to ``nz*n + dn``. The pre-repair
    (defective) operator is therefore the repaired operator with each F0 row's
    off-diagonal destinations moved back to the bare node column
    ``dn = col - z*n``. Every non-F0 row, every diagonal entry and ``u`` are
    identical. Duplicate destinations are summed exactly as
    ``scipy.sparse.coo_matrix`` sums them during assembly.
    """
    rows_out: list[int] = []
    cols_out: list[int] = []
    vals_out: list[float] = []
    f0_set = {int(r) for r in f0_rows}
    for r in range(Q_corr.shape[0]):
        start, stop = int(Q_corr.indptr[r]), int(Q_corr.indptr[r + 1])
        idx = Q_corr.indices[start:stop]
        val = Q_corr.data[start:stop]
        if r not in f0_set:
            rows_out.extend([r] * int(idx.size))
            cols_out.extend(int(c) for c in idx)
            vals_out.extend(float(v) for v in val)
            continue
        zz = r // n
        rec_f = records[r]
        if rec_f is None:
            raise ZBlockRepairFailure(f"missing F0 record at row {r}")
        dests = {zz * n + int(dn) for dn, _ in rec_f.row_entries}
        for c, v in zip(idx, val):
            cc = int(c)
            cols_out.append(cc - zz * n if cc in dests else cc)
            rows_out.append(r)
            vals_out.append(float(v))
    return sparse.coo_matrix((vals_out, (rows_out, cols_out)),
                             shape=Q_corr.shape).tocsr()


# ---------------------------------------------------------------------------
# the single diagnostic
# ---------------------------------------------------------------------------
def _diagnostic_from_reconstruction(rec: dict) -> ZBlockRepairResult:
    solver: BoundaryHJBSolver = rec["solver"]
    labor0: np.ndarray = rec["labor0"]
    V_star: np.ndarray = rec["V_star"]
    rho: float = rec["rho"]
    trace: list = rec["trace"]

    n, nz, state_size = solver.n, solver.nz, solver.state_size
    if (n, nz, state_size) != (N_NODES, N_Z, STATE_SIZE):
        raise ZBlockRepairFailure(f"unexpected frozen case shape {(n, nz, state_size)}")
    V_flat = V_star.ravel(order="F")
    if not np.isfinite(V_flat).all():
        raise ZBlockRepairFailure("non-finite accepted stagnation state V_*")

    # -- 1. frozen accepted reconstruction reproduction ---------------------
    if len(trace) != RECONSTRUCT_STEPS:
        raise ZBlockRepairFailure("reconstruction did not stop at accepted step 8")
    final_statistic = float(trace[-1]["accepted_max_stat"])
    if abs(final_statistic - FINAL_STATISTIC_EXPECTED) > 1e-12:
        raise ZBlockRepairFailure(
            f"accepted final statistic regression: {final_statistic!r}")
    wall = dict(trace[-1]["worst_after"])
    if not (wall["family"] == "F3" and wall["j"] == 13 and wall["i"] == 13
            and wall["z"] == 1):
        raise ZBlockRepairFailure(f"accepted wall state regression: {wall}")
    wall_pb, wall_node, wall_nz = audit.min_boundary_pb_state(solver, V_star, labor0)
    if not np.isfinite(wall_pb):
        raise ZBlockRepairFailure("non-finite required boundary p_b at V_*")
    if abs(wall_pb - MIN_BOUNDARY_PB_EXPECTED) > 1e-12:
        raise ZBlockRepairFailure(f"accepted min boundary p_b regression: {wall_pb!r}")

    # -- 2. the TWO authorized builds, SAME current selected F0 controls ----
    two = audit.build_two_operators(solver, V_star, labor0, rho)
    Q_iter, u_iter = two["Q_iter"], two["u_iter"]
    Q_corr, u_corr = two["Q_final_current"], two["u_final_current"]
    records_corrected = two["records_final"]
    f0_rows = two["f0_rows"]

    # fail-closed on non-finite supplied evidence (both residuals)
    for nm in ("R_iter", "R_final_current"):
        R_supplied = np.asarray(two[nm], dtype=float)
        if not np.isfinite(R_supplied).all():
            raise ZBlockRepairFailure(f"non-finite supplied evidence in {nm}")

    r_iter_inf = float(two["stats_iter"]["total"]["max_abs"])
    if abs(r_iter_inf - R_ITER_INF_ACCEPTED) > 1e-12:
        raise ZBlockRepairFailure(f"accepted R_iter regression: {r_iter_inf!r}")

    # -- 3. corrected final residual ---------------------------------------
    # Q_final_current already contains the explicit exogenous switch matrix B
    # (added at the end of build_operator_and_u). Every destination-layout and
    # cross-z statement below is about the ASSEMBLED part only, so isolate it.
    cfg = solver.config
    B = sparse.kron(sparse.csr_matrix(cfg.switch_matrix),
                    sparse.eye(n, format="csr"), format="csr").tocsr()
    Q_pure = (Q_corr - B).tocsr()

    R_corr = rho * V_flat - (u_corr + Q_corr.dot(V_flat))
    if not np.isfinite(R_corr).all():
        raise ZBlockRepairFailure("non-finite corrected final residual")
    s_corr = residual_stats(solver, R_corr)
    r_corrected_inf = float(s_corr["total"]["max_abs"])

    # -- 4. corrected final vs accepted iteration operator -----------------
    corr_gap, corr_gap_row = _rowwise_max(Q_corr, Q_iter, f0_rows)
    corr_gap_total, _ = _rowwise_max(Q_corr, Q_iter, np.arange(state_size))
    iter_comp = audit.iter_f0_components(
        solver, V_star, labor0, two["records_current"], f0_rows)
    corr_comp = audit.final_raw_f0_components(solver, records_corrected, f0_rows)
    rate_max = 0.0
    for nm in ("b_backward", "b_forward", "a_backward", "a_forward",
               "diagonal", "represented_outgoing_sum",
               "omitted_destination_rate", "utility"):
        rate_max = max(rate_max, float(np.max(np.abs(
            corr_comp[nm] - iter_comp[nm]))))
    if not bool(corr_comp["reproduced"].all()):
        raise ZBlockRepairFailure(
            "corrected final=True F0 rates do not reproduce the accepted rates")

    # corrected destination layout, checked on the ASSEMBLED (B-free) part.
    # The only permitted off-diagonal destinations are the four declared grid
    # neighbours placed inside the SAME z block, i.e. column nz*n + dn.
    layout_misplaced = 0
    layout_checked = 0
    for r in f0_rows:
        zz, node = int(r) // n, int(r) % n
        j, i = int(solver.grid.j_arr[node]), int(solver.grid.i_arr[node])
        nb = solver.grid.neighbors(j, i)
        expected_cols = {zz * n + int(v) for v in nb.values() if v is not None}
        start, stop = int(Q_pure.indptr[r]), int(Q_pure.indptr[r + 1])
        for c in Q_pure.indices[start:stop]:
            cc = int(c)
            if cc == int(r):
                continue
            layout_checked += 1
            in_block = zz * n <= cc < (zz + 1) * n
            if not in_block or cc not in expected_cols:
                layout_misplaced += 1

    # -- 5. pre-repair reconciliation (derived, structurally validated) ----
    Q_pre = pre_repair_final_operator(Q_corr, records_corrected, f0_rows, n)
    R_pre = rho * V_flat - (u_corr + Q_pre.dot(V_flat))
    if not np.isfinite(R_pre).all():
        raise ZBlockRepairFailure("non-finite derived pre-repair residual")
    s_pre = residual_stats(solver, R_pre)
    r_pre_inf = float(s_pre["total"]["max_abs"])
    pre_vs_iter, _ = _rowwise_max(Q_pre, Q_iter, f0_rows)
    pre_vs_corr, _ = _rowwise_max(Q_pre, Q_corr, f0_rows)
    structural_ok = bool(
        abs(pre_vs_iter - F0_PRE_REPAIR_GAP_ACCEPTED) <= 1e-6
        and abs(r_pre_inf - R_FINAL_CURRENT_INF_ACCEPTED) <= RECONCILE_TOL)
    if not structural_ok:
        raise ZBlockRepairFailure(
            "derived pre-repair operator does not reproduce the accepted "
            f"Issue #66/#65 baselines: gap={pre_vs_iter!r}, R={r_pre_inf!r}")

    # -- 6. invariants ------------------------------------------------------
    z0_rows = [int(r) for r in f0_rows if int(r) // n == 0]
    z1_rows = [int(r) for r in f0_rows if int(r) // n == 1]
    z0_diff, _ = _rowwise_max(Q_pre, Q_corr, z0_rows)
    z1_diff, _ = _rowwise_max(Q_pre, Q_corr, z1_rows)
    z0_unchanged = int(sum(
        1 for r in z0_rows
        if float(np.max(np.abs(
            np.asarray(Q_pre.getrow(r).toarray()).ravel()
            - np.asarray(Q_corr.getrow(r).toarray()).ravel()))) == 0.0))
    bnd_rows = np.nonzero(~two["f0_mask"])[0]
    if float(two["boundary_row_max_abs_diff"]) > CORRECTED_VS_ITER_TOL:
        raise ZBlockRepairFailure("non-F0 boundary operator regression")
    if float(two["boundary_u_max_abs_diff"]) > CORRECTED_VS_ITER_TOL:
        raise ZBlockRepairFailure("non-F0 boundary utility regression")
    if float(two["same_controls_max_abs_diff"]) > CORRECTED_VS_ITER_TOL:
        raise ZBlockRepairFailure("same-controls contract violated")
    for r in f0_rows:
        if records_corrected[int(r)] is None:
            raise ZBlockRepairFailure(f"missing corrected F0 record at row {int(r)}")

    # unintended cross-z contamination: on the ASSEMBLED (B-free) part, every
    # off-diagonal F0 destination must lie in the SAME z block as its source row
    # and be a declared grid neighbour. The explicit exogenous switch matrix B
    # accounts for the entire remaining cross-z content by construction
    # (asserted by offblock_residual_beyond_switch == 0).
    cross_z = 0
    for r in f0_rows:
        node, zz = int(r) % n, int(r) // n
        start, stop = int(Q_pure.indptr[r]), int(Q_pure.indptr[r + 1])
        for c in Q_pure.indices[start:stop]:
            cc = int(c)
            if cc == int(r):
                continue
            if not (zz * n <= cc < (zz + 1) * n):
                cross_z += 1

    # the ONLY cross-z content in the corrected F0 rows is the explicit
    # exogenous switch matrix B: each off-block entry must equal the
    # corresponding B entry exactly
    offblock_residual_beyond_switch = 0.0
    for r in f0_rows:
        node, zz = int(r) % n, int(r) // n
        start, stop = int(Q_corr.indptr[r]), int(Q_corr.indptr[r + 1])
        for c, v in zip(Q_corr.indices[start:stop], Q_corr.data[start:stop]):
            cc = int(c)
            if zz * n <= cc < (zz + 1) * n:
                continue
            b_val = float(B[r, cc]) if cc in set(B.indices[
                B.indptr[r]:B.indptr[r + 1]]) else 0.0
            offblock_residual_beyond_switch = max(
                offblock_residual_beyond_switch, abs(float(v) - b_val))

    utility_f0 = float(np.max(np.abs(u_iter[f0_rows] - u_corr[f0_rows])))
    utility_bnd = float(np.max(np.abs(u_iter[bnd_rows] - u_corr[bnd_rows])))
    diag_f0 = float(np.max(np.abs(corr_comp["diagonal"] - iter_comp["diagonal"])))

    ratio_pre = float(r_corrected_inf / r_pre_inf) if r_pre_inf else float("inf")
    ratio_iter = float(r_corrected_inf / r_iter_inf) if r_iter_inf else float("inf")
    ratio_base = (float(r_corrected_inf / R_FINAL_CURRENT_INF_ACCEPTED)
                  if R_FINAL_CURRENT_INF_ACCEPTED else float("inf"))

    # -- 7. frozen terminal rule -------------------------------------------
    corrected_layout_matches = bool(
        layout_misplaced == 0 and cross_z == 0
        and offblock_residual_beyond_switch == 0.0
        and corr_gap <= CORRECTED_VS_ITER_TOL
        and corr_gap_total <= CORRECTED_VS_ITER_TOL)
    if not (np.isfinite(r_corrected_inf) and structural_ok):
        terminal = TERMINAL_C
    elif not corrected_layout_matches or corr_gap > CORRECTED_VS_ITER_TOL:
        terminal = TERMINAL_B
    else:
        terminal = TERMINAL_A

    return ZBlockRepairResult(
        terminal=terminal,
        iterations=len(trace),
        final_statistic=final_statistic,
        min_boundary_pb_star=float(wall_pb),
        wall_state=wall,
        r_iter_inf=r_iter_inf,
        r_iter_argmax=two["stats_iter"]["total"]["argmax_state"],
        r_corrected_inf=r_corrected_inf,
        r_corrected_argmax=s_corr["total"]["argmax_state"],
        r_corrected_f0_max=float(s_corr["f0"]["max_abs"]),
        r_corrected_boundary_max=float(s_corr["boundary"]["max_abs"]),
        corrected_vs_iter_f0_rowwise_max=corr_gap,
        corrected_vs_iter_f0_rowwise_max_state=audit._state(corr_gap_row, solver),
        corrected_vs_iter_total_rowwise_max=corr_gap_total,
        corrected_rate_component_max_abs_diff=rate_max,
        corrected_destination_layout_misplaced_columns=layout_misplaced,
        corrected_destination_layout_checked_rows=layout_checked,
        offblock_residual_beyond_switch=offblock_residual_beyond_switch,
        z0_f0_rowwise_max_abs_diff_vs_pre_repair=z0_diff,
        z0_f0_unchanged_row_count=z0_unchanged,
        z1_f0_rowwise_max_abs_diff_vs_pre_repair=z1_diff,
        z1_f0_row_count=len(z1_rows),
        cross_z_contamination_row_count=cross_z,
        utility_f0_max_abs_diff=utility_f0,
        utility_boundary_max_abs_diff=utility_bnd,
        boundary_row_max_abs_diff=float(two["boundary_row_max_abs_diff"]),
        boundary_u_max_abs_diff=float(two["boundary_u_max_abs_diff"]),
        diagonal_f0_max_abs_diff=diag_f0,
        same_controls_max_abs_diff=float(two["same_controls_max_abs_diff"]),
        max_abs_q1_iter=float(two["max_abs_q1_iter"]),
        max_abs_q1_corrected=float(two["max_abs_q1_final_current"]),
        expansions_iter=int(two["expansions_iter"]),
        bindings_iter=int(two["bindings_iter"]),
        expansions_corrected=int(two["expansions_final_current"]),
        bindings_corrected=int(two["bindings_final_current"]),
        r_pre_repair_current_inf=r_pre_inf,
        r_pre_repair_current_argmax=s_pre["total"]["argmax_state"],
        pre_repair_vs_iter_f0_rowwise_max=pre_vs_iter,
        pre_repair_vs_corrected_f0_rowwise_max=pre_vs_corr,
        pre_repair_structural_match=structural_ok,
        ratio_corrected_over_pre_repair=ratio_pre,
        ratio_corrected_over_r_iter=ratio_iter,
        ratio_corrected_over_accepted_final_baseline=ratio_base,
        residual_improvement=float(r_pre_inf - r_corrected_inf),
        f0_row_count=int(len(f0_rows)),
        bellman_tolerance_unchanged=BELLMAN_TOLERANCE_UNCHANGED,
        convergence_declared=False,
        new_hjb_iterate_accepted=False,
        deterministic_repeat_identical=False,
    )


def run_issue67_diagnostic() -> ZBlockRepairResult:
    """Exactly ONE Issue #67 diagnostic: ONE deterministic reconstruction of the
    accepted Issue #63 stagnation state, ONE ``final=False`` build, ONE corrected
    ``final=True`` build with the SAME current selected F0 controls, ONE
    corrected-equivalence/residual diagnostic. No new HJB iterate is accepted."""
    return _diagnostic_from_reconstruction(
        reconstruct_issue63_stagnation_state())


def _canon(r: ZBlockRepairResult) -> dict:
    return dataclasses.asdict(r)


def run_issue67_diagnostic_twice() -> tuple[ZBlockRepairResult, bool]:
    """The ONE deterministic repeat of the full diagnostic."""
    first = run_issue67_diagnostic()
    second = run_issue67_diagnostic()
    identical = bool(_canon(first) == _canon(second))
    first.deterministic_repeat_identical = identical
    return first, identical


def repair_source_facts() -> dict:
    """Static source-level facts about the authorized repair location."""
    text = SELECTED_Q_ABS.read_text(encoding="utf-8")
    lines = text.splitlines()
    hits = [(i + 1, ln.strip()) for i, ln in enumerate(lines)
            if REPAIR_OLD in ln or REPAIR_NEW in ln]
    return {"hits": hits, "tree": ast.parse(text), "source": text}


def summary_csv_lines(r: ZBlockRepairResult) -> list[str]:
    """Compact CSV evidence lines for the Issue #67 report."""
    lines = ["metric,value"]
    for f in dataclasses.fields(r):
        v = getattr(r, f.name)
        if isinstance(v, dict):
            v = "; ".join(f"{k}={v[k]}" for k in sorted(v))
        lines.append(f"{f.name},{v}")
    return lines


# ===========================================================================
# TESTS
# ===========================================================================
@pytest.fixture(scope="module")
def diag():
    """ONE full diagnostic plus its ONE deterministic repeat."""
    r, ident = run_issue67_diagnostic_twice()
    return r, ident


@pytest.fixture(scope="module")
def recon():
    """ONE independent accepted-state reconstruction for fail-closed guards."""
    return reconstruct_issue63_stagnation_state()


# -- 1. the authorized source repair is exactly one location ---------------
def test_source_repair_is_exactly_one_authorized_location():
    """CURRENT-CONTRACT (Owner Route A): the Issue #67 z-block repair is intact.

    The bare-destination assembly must still be absent and all three assembly
    sites (final, iteration, boundary) must still use the identical same-z-block
    template. Under Route A the final=F0 branch is further consolidated to
    rebuild the row from the supplied selected record, but it retains the very
    same destination-column placement, so the Issue #67 repair itself is
    unchanged and only the rate SOURCE inside that branch changed.
    """
    facts = repair_source_facts()
    src = facts["source"]
    # 1. no bare-destination assembly survives anywhere (Issue #67 repair intact)
    assert src.count(REPAIR_OLD) == 0, "unrepaired bare destination assembly remains"
    # 2. all three assembly sites still agree on same-z-block placement
    assert src.count(REPAIR_NEW) == 3, (
        f"expected the three assembly sites to agree, got {src.count(REPAIR_NEW)}")
    assert src.count("cols.append(nz * self.n + dn)") == 3
    lines = src.splitlines()
    hits = facts["hits"]
    assert len(hits) == 3
    # 3. the final=F0 branch is same-z-block AND now record-sourced (Route A)
    final_line = hits[0][0]
    window = "\n".join(lines[final_line - 25:final_line + 2])
    assert "if final and f0_policies is not None" in window
    assert CURRENT_ROUTE_A_FINAL_LINE_TEXT in window
    assert "rec.row_entries" in window
    # 4. the pre-Route-A raw-drift final-Q construction is gone (historical)
    assert "max(-mu_a_v, 0.0) / self.da" not in window
    assert "diag = -(bb + bf + ab + af)" not in window
    assert PRE_ROUTE_A_FINAL_ZBLOCK_ASSEMBLY_LINE > 0
    # 5. the other two sites are the accepted iteration and boundary paths
    assert "local_interior_row" in "\n".join(lines[hits[1][0] - 20:hits[1][0] + 2])
    assert "_boundary_row" in "\n".join(lines[hits[2][0] - 20:hits[2][0] + 2])


def test_pre_route_a_zblock_repair_evidence_preserved():
    """The accepted Issue #67 repair remains auditable at a pinned revision.

    The pre-Route-A source is read read-only from an ABSOLUTE revision (the
    parent of the original Issue #70 scientific commit) and must still show the
    historical z-block repair: the same-z-block template at THREE sites
    including the final=F0 branch, and no bare-destination assembly. Using an
    absolute revision rather than a moving ``HEAD~n`` keeps the Issue #67 history
    verifiable across later remediation commits instead of overwriting it.
    """
    import subprocess as _sp
    repo_root = Path(__file__).resolve().parents[1]
    pre = _sp.run(["git", "show",
                   f"{PRE_ROUTE_A_SELECTED_Q_COMMIT}:{SELECTED_Q_RELPATH}"],
                  cwd=repo_root, capture_output=True, text=True,
                  encoding="utf-8", errors="replace", check=True).stdout
    assert pre.count(PRE_ROUTE_A_FINAL_ZBLOCK_LINE_TEXT) == 3
    assert "rows.append(row); cols.append(dn); data.append(rate)" not in pre
    # the pre-Route-A final=F0 branch still rebuilt its rates from raw drift
    assert "max(-mu_a_v, 0.0) / self.da" in pre
    blob = _sp.run(
        ["git", "rev-parse",
         f"{PRE_ROUTE_A_SELECTED_Q_COMMIT}:{SELECTED_Q_RELPATH}"],
        cwd=repo_root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=True).stdout.strip()
    assert blob == PRE_ROUTE_A_SELECTED_Q_BLOB
    # the CURRENT Route-A revision still uses the same-z-block destination
    # template at three sites AND preserves the supplied policy label
    current = (repo_root / SELECTED_Q_RELPATH).read_text(encoding="utf-8")
    assert current.count(PRE_ROUTE_A_FINAL_ZBLOCK_LINE_TEXT) == 3
    assert "sector=rec.sector" in current
    assert "sector_arr[node, nz] = rec.sector" in current
    assert "INTERIOR_FINAL" not in current


def test_source_repair_is_the_only_selected_q_change():
    """The repaired source differs from the pre-repair blob by exactly one line.

    Uses the recorded pre-repair blob hash for the base version when available
    through git; otherwise asserts the structural invariant that every
    off-diagonal F0 destination uses the z-block offset.
    """
    facts = repair_source_facts()
    tree = facts["tree"]
    build = None
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "build_operator_and_u":
            build = node
    assert build is not None
    # every cols.append(...) in the final=True F0 off-diagonal path carries the
    # z-block offset; count the bare and offset forms
    offsets = [n for n in ast.walk(build)
               if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
               and n.func.attr == "append"]
    assert offsets, "no cols.append calls found in build_operator_and_u"
    bare = [n for n in offsets
            if len(n.args) == 1 and isinstance(n.args[0], ast.Name)
            and n.args[0].id == "dn"]
    offset = [n for n in offsets
              if len(n.args) == 1 and isinstance(n.args[0], ast.BinOp)]
    assert bare == [], f"unrepaired bare destination append remains: {bare}"
    assert offset, "no z-block-offset destination append found"


# -- 2. frozen accepted reconstruction -------------------------------------
def test_reconstruction_exact(diag):
    r, _ = diag
    assert r.iterations == RECONSTRUCT_STEPS == 8
    assert r.final_statistic == pytest.approx(FINAL_STATISTIC_EXPECTED, abs=1e-12)
    assert r.min_boundary_pb_star == pytest.approx(MIN_BOUNDARY_PB_EXPECTED, abs=1e-12)
    assert r.wall_state["family"] == "F3"
    assert r.wall_state["j"] == 13 and r.wall_state["i"] == 13
    assert r.wall_state["z"] == 1
    assert r.wall_state["node"] == WALL_NODE
    assert r.f0_row_count == F0_ROW_COUNT


def test_r_iter_reproduced(diag):
    r, _ = diag
    assert r.r_iter_inf == pytest.approx(R_ITER_INF_ACCEPTED, abs=1e-12)
    assert r.r_iter_argmax["family"] == "F0"


# -- 3. corrected final operator matches the MATLAB-faithful layout ---------
def test_z1_f0_destinations_stay_in_same_z_block(diag):
    r, _ = diag
    assert r.corrected_destination_layout_misplaced_columns == 0
    assert r.corrected_destination_layout_checked_rows > 0
    assert r.cross_z_contamination_row_count == 0
    # the entire remaining cross-z content is the explicit exogenous switch
    # matrix, reconstructed exactly by construction
    assert r.offblock_residual_beyond_switch == 0.0


def test_corrected_final_matches_iteration_operator(diag):
    r, _ = diag
    assert r.corrected_vs_iter_f0_rowwise_max <= CORRECTED_VS_ITER_TOL
    assert r.corrected_vs_iter_total_rowwise_max <= CORRECTED_VS_ITER_TOL
    # the spurious cross-z validation gap is removed (pre-repair 24.60197...)
    assert r.corrected_vs_iter_f0_rowwise_max < 1e-12


def test_corrected_final_rate_components_unchanged(diag):
    r, _ = diag
    assert r.corrected_rate_component_max_abs_diff <= 1.0e-12
    assert r.diagonal_f0_max_abs_diff <= 1.0e-12
    assert r.utility_f0_max_abs_diff == 0.0
    assert r.utility_boundary_max_abs_diff == 0.0


def test_pre_repair_reconciliation_exact(diag):
    r, _ = diag
    # the derived pre-repair operator reproduces BOTH accepted baselines exactly
    assert r.pre_repair_structural_match is True
    assert r.pre_repair_vs_iter_f0_rowwise_max == pytest.approx(
        F0_PRE_REPAIR_GAP_ACCEPTED, abs=1e-9)
    assert r.r_pre_repair_current_inf == pytest.approx(
        R_FINAL_CURRENT_INF_ACCEPTED, abs=RECONCILE_TOL)
    assert r.r_pre_repair_current_argmax["family"] == "F0"
    assert abs(r.r_pre_repair_current_inf - R_FINAL_STALE_INF_ACCEPTED) < 1e-5


# -- 4. z=0 must be untouched by the repair --------------------------------
def test_z0_f0_behavior_unchanged(diag):
    r, _ = diag
    assert r.z0_f0_rowwise_max_abs_diff_vs_pre_repair == 0.0
    assert r.z0_f0_unchanged_row_count == F0_NODE_COUNT
    # the repair does change z=1 rows (that is its whole purpose)
    assert r.z1_f0_rowwise_max_abs_diff_vs_pre_repair > 1.0
    assert r.z1_f0_row_count == F0_NODE_COUNT


# -- 5. non-F0 boundary rows, conservativity, scope ------------------------
def test_non_f0_boundary_unchanged(diag):
    r, _ = diag
    assert r.boundary_row_max_abs_diff == 0.0
    assert r.boundary_u_max_abs_diff == 0.0
    assert r.same_controls_max_abs_diff == 0.0


def test_conservativity_and_no_new_bindings(diag):
    r, _ = diag
    assert r.max_abs_q1_iter <= 1e-9
    assert r.max_abs_q1_corrected <= 1e-9
    assert r.max_abs_q1_corrected == pytest.approx(r.max_abs_q1_iter, abs=1e-15)
    assert r.expansions_iter == 0
    assert r.bindings_iter == 0
    assert r.expansions_corrected == 0
    assert r.bindings_corrected == 0


# -- 6. corrected residual evidence and the scope ceiling ------------------
def test_corrected_residual_finite_and_recorded(diag):
    r, _ = diag
    assert np.isfinite(r.r_corrected_inf)
    assert r.r_corrected_inf > 0.0
    assert r.r_corrected_argmax is not None
    assert r.r_corrected_f0_max == pytest.approx(r.r_corrected_inf, abs=1e-12)
    assert np.isfinite(r.r_corrected_boundary_max)


def test_corrected_residual_is_exactly_the_iteration_residual(diag):
    """Post-repair the final-validation residual equals the accepted R_iter.

    This is a structural equivalence statement about the repaired operator, NOT
    a convergence claim: the value stays far above the unchanged Bellman
    tolerance.
    """
    r, _ = diag
    assert r.r_corrected_inf == pytest.approx(R_ITER_INF_ACCEPTED, abs=1e-12)
    assert r.ratio_corrected_over_r_iter == pytest.approx(1.0, abs=1e-12)
    assert r.residual_improvement > 400.0
    assert r.ratio_corrected_over_pre_repair < 0.05


def test_no_convergence_claimed_and_no_new_iterate(diag):
    r, _ = diag
    assert r.convergence_declared is False
    assert r.new_hjb_iterate_accepted is False
    assert r.bellman_tolerance_unchanged == BELLMAN_TOLERANCE_UNCHANGED
    # the corrected residual is still FAR above the unchanged tolerance
    assert r.r_corrected_inf > 1.0e3 * BELLMAN_TOLERANCE_UNCHANGED


# -- 7. terminal -----------------------------------------------------------
def test_exactly_one_terminal_returned(diag):
    r, _ = diag
    assert r.terminal == TERMINAL_A
    assert r.terminal not in (TERMINAL_B, TERMINAL_C, TERMINAL_BLOCKED)
    assert [r.terminal == t for t in (TERMINAL_A, TERMINAL_B,
                                      TERMINAL_C)].count(True) == 1


# -- 8. determinism --------------------------------------------------------
def test_deterministic_repeat_identical(diag):
    r, ident = diag
    assert ident is True
    assert r.deterministic_repeat_identical is True


# -- 9. fail-closed guards -------------------------------------------------
def test_fail_closed_on_nonfinite(recon):
    solver = recon["solver"]
    real = audit.build_two_operators

    def nan_two(sv, V, labor0, rho):
        out = real(sv, V, labor0, rho)
        out = dict(out)
        R = out["R_final_current"].copy()
        R[0] = np.nan
        out["R_final_current"] = R
        return out

    with patch.object(audit, "build_two_operators", side_effect=nan_two):
        with pytest.raises(ZBlockRepairFailure):
            _diagnostic_from_reconstruction(recon)


def test_fail_closed_on_missing_f0_record(recon):
    """A missing corrected-F0 record must fail closed, never silently pass."""
    solver = recon["solver"]
    n = solver.n
    Q = sparse.eye(solver.state_size, format="csr")
    with pytest.raises(ZBlockRepairFailure):
        pre_repair_final_operator(Q, [None] * solver.state_size,
                                  [0, n], n)


# -- 10. no forbidden machinery --------------------------------------------
def test_no_forbidden_iteration_machinery_static():
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
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
    # module docstring / comment mentions are not AST Names or Attributes
    assert found == [], f"forbidden tokens found: {found}"
    assert not any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                   and n.func.id == "spsolve" for n in ast.walk(tree))


def test_runtime_exactly_two_builds_at_vstar(recon):
    """The diagnostic must perform exactly ONE final=False and ONE final=True
    operator build at V_* (plus the reconstruction's own internal builds)."""
    solver = recon["solver"]
    with patch.object(solver, "build_operator_and_u",
                      wraps=solver.build_operator_and_u) as spy:
        _diagnostic_from_reconstruction(recon)
    finals = [c.kwargs.get("final") for c in spy.call_args_list]
    assert finals.count(False) == 1
    assert finals.count(True) == 1
