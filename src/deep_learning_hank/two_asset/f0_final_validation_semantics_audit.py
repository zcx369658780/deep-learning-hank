"""DLH-5V-Q — F0 final-validation operator consistency audit at the accepted
Issue #63 stagnation state.

Issue #65 / DLH-5V-Q
``SCIENTIFIC_NUMERICAL_DIAGNOSTIC__F0_FINAL_VALIDATION_OPERATOR_CONSISTENCY_AUDIT``

Authority: Issue #65 OPEN; initial activation ``5653199929``; final
authoritative activation-refresh ``5653443917`` (post-sync live ``main``
``3e82970d59a10ecd812f9d39889f145661dcc293``). Route decision
``APPROVE_F0_FINAL_VALIDATION_OPERATOR_CONSISTENCY_AUDIT_AFTER_5VP_TERMINAL_B``;
authority marker ``DLH_5VQ_F0_FINAL_VALIDATION_SEMANTICS_AUDIT_AUTHORIZED``.

Scientific object (binding, Issue #65 sections 3-8), in exactly this order:

1. ONE deterministic reconstruction of the exact accepted Issue #63
   stagnation state ``V_*`` (accepted Issue #64 reconstruction path; STOP
   before any new HJB iterate is accepted), preserving
   ``records_pre_step8`` (the accepted pre-step-8 records used by Issue #63
   final validation) and ``records_current`` (the ``final=False`` policies
   re-selected exactly once at ``V_*``);
2. at the SAME fixed ``V_*``, exactly THREE operator/residual builds:
   - A. iteration operator: ``final=False`` once -> ``Q_iter, u_iter,
     records_current``; ``R_iter = rho V_* - [u_iter + Q_iter V_*]``;
   - B. accepted stale-record final operator: ``final=True`` with
     ``f0_policies = records_pre_step8`` -> ``Q_final_stale, u_final_stale``;
     ``R_final_stale = rho V_* - [u_final_stale + Q_final_stale V_*]``
     (reproduces the accepted 490.7560425919994);
   - C. diagnostic current-record final operator: ``final=True`` with
     ``f0_policies = records_current`` -> ``Q_final_current,
     u_final_current``; ``R_final_current = rho V_* - [u_final_current +
     Q_final_current V_*]`` (diagnostic counterfactual only, NOT an accepted
     replacement validation rule);
3. exact decomposition ``D_total = R_final_stale - R_iter``,
   ``D_stale = R_final_stale - R_final_current``,
   ``D_rate = R_final_current - R_iter`` with the numerical verification
   ``D_total = D_stale + D_rate`` within the declared tolerance; total /
   F0-only / boundary-only inf norms with argmax state/family/z for each of
   the six residual/difference vectors; ``max|Q 1|``, optimizer expansions
   and artificial bindings for all three operators;
4. ONE compact F0 policy/control provenance audit on F0 rows only:
   changed sector/transfer-label count and max |Delta consumption|, |Delta
   labor|, |Delta transfer|, |Delta mu_a|, |Delta mu_b|, |Delta utility|
   between ``records_pre_step8`` and ``records_current`` (sector-label
   equality is NOT treated as continuous-control equality), plus F0-only
   rowwise max absolute operator differences ``Q_final_stale -
   Q_final_current`` / ``Q_final_current - Q_iter`` and ``u`` differences;
5. frozen attribution rule (ex ante, local contribution only):
   ``STALE_RECORD_DOMINANT`` iff ``||D_stale||_inf > ||D_rate||_inf``;
   ``FINAL_RATE_SEMANTICS_DOMINANT_OR_TIED`` iff ``||D_rate||_inf >=
   ||D_stale||_inf``; separately record whether ``||R_final_current||_inf <
   ||R_final_stale||_inf``;
6. ONE deterministic repeat of the full diagnostic.

Dominance is local attribution at ``V_*`` only: it does NOT declare either
diagnostic counterfactual operator to be the correct HJB convergence
criterion. No trial value states, no Newton step, no continuation, no line
search, no source mutation, no economics/prices/grid/domain/``PB_MARGIN``
change, no accepted final-validation-semantics change. The household oracle,
selected-Q source, the accepted Issue #61 / #62 / #63 / #64 implementations
are imported read-only and never modified. No KFE / stationary KFE / steady
state / ``solve_household_steady_state``.

FAIL-CLOSED: non-finite residual evidence, provenance ambiguity (missing F0
records), or a failed additive decomposition raises
``F0ValidationSemanticsFailure`` (surfaced explicitly, never misread as
attributable). A non-identical deterministic repeat is internally
inconsistent evidence.
"""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field
from typing import Optional

import numpy as np
from scipy import sparse

from deep_learning_hank.two_asset.boundary_hjb_selected_q import (
    BoundaryHJBFailure,
    BoundaryHJBSolver,
)
from deep_learning_hank.two_asset.adaptive_resolvent_hjb import (
    CENTRAL_CONFIG,
    _state_info,
    min_boundary_pb_state,
)
from deep_learning_hank.two_asset.continuous_ftb_resolvent_hjb import (
    FTBStepConstructionFailure,
)
from deep_learning_hank.two_asset.stagnation_newton_geometry import (
    reconstruct_issue63_stagnation_state,
    residual_stats,
)

# ---------------------------------------------------------------------------
# Frozen constants (Issue #65) — do NOT change
# ---------------------------------------------------------------------------
RECONSTRUCT_STEPS = 8               # accepted Issue #63 FTB steps to reproduce
DECOMPOSITION_TOL = 1.0e-6          # declared |D_total - (D_stale + D_rate)|_inf tolerance

# ---------------------------------------------------------------------------
# Terminals (Issue #65 section 11) — exactly ONE returned by the run
# ---------------------------------------------------------------------------
TERMINAL_A = ("DLH_5VQ_F0_FINAL_VALIDATION_SEMANTICS__STALE_F0_RECORDS_DOMINATE_"
              "ACCEPTED_VALIDATION_GAP__FINAL_VALIDATION_RECORD_REFRESH_REVIEW_"
              "GATE_READY")
TERMINAL_B = ("DLH_5VQ_F0_FINAL_VALIDATION_SEMANTICS__FINAL_RATE_SEMANTICS_"
              "DOMINATE_OR_TIE_ACCEPTED_VALIDATION_GAP__F0_FINAL_OPERATOR_"
              "REVIEW_REQUIRED")
TERMINAL_C = ("DLH_5VQ_F0_FINAL_VALIDATION_SEMANTICS__NONFINITE_OR_INCONSISTENT_"
              "DECOMPOSITION__BOUNDARY_HJB_VALIDATION_ROUTE_REVIEW_REQUIRED")
TERMINAL_BLOCKED = "BLOCKED_DLH_5VQ_AUTHORITY_OR_DEPENDENCY_CONFLICT"


class F0ValidationSemanticsFailure(RuntimeError):
    """Fail-closed: non-finite / internally inconsistent decomposition or
    provenance ambiguity in the F0 final-validation semantics audit."""


# ---------------------------------------------------------------------------
# F0 row layout helpers (state layout is z-major, node-fastest: row = z*n + node)
# ---------------------------------------------------------------------------
def f0_rows_of(solver: BoundaryHJBSolver) -> tuple[np.ndarray, np.ndarray]:
    """(boolean mask, integer row indices) of the F0 state rows."""
    n, nz = solver.n, solver.nz
    fam = np.array([str(solver.grid.families[node]) for node in range(n)])
    mask = np.tile(fam == "F0", nz)
    return mask, np.nonzero(mask)[0]


def _max_abs_q1(Q: sparse.csr_matrix) -> float:
    return float(np.max(np.abs(np.asarray(Q.sum(axis=1)).ravel())))


# ---------------------------------------------------------------------------
# 2/3. Exactly three operator/residual builds at the same fixed V_*
# ---------------------------------------------------------------------------
def build_three_operators(solver: BoundaryHJBSolver, V_star: np.ndarray,
                          labor0: np.ndarray, records_pre_step8: list,
                          rho: float) -> dict:
    """Build exactly A / B / C at the SAME ``V_*`` (one build each).

    - A. ``final=False`` exactly once -> ``Q_iter, u_iter`` and
      ``records_current`` (the current records returned by that build);
      ``R_iter = rho V_* - [u_iter + Q_iter V_*]``;
    - B. ``final=True`` with ``f0_policies = records_pre_step8`` ->
      ``Q_final_stale, u_final_stale``; ``R_final_stale`` (must reproduce
      ``||R_final_stale||_inf = 490.7560425919994``);
    - C. ``final=True`` with ``f0_policies = records_current`` ->
      ``Q_final_current, u_final_current``; ``R_final_current`` (diagnostic
      counterfactual only).

    Decomposes ``D_total = R_final_stale - R_iter``, ``D_stale =
    R_final_stale - R_final_current``, ``D_rate = R_final_current -
    R_iter`` and verifies ``D_total = D_stale + D_rate`` within
    ``DECOMPOSITION_TOL``. Records total / F0-only / boundary-only inf norms
    with argmax for all six vectors, plus ``max|Q 1|``, optimizer expansions
    and artificial bindings for the three operators.

    FAIL-CLOSED on any non-finite residual component.
    """
    n, nz = solver.n, solver.nz
    V_flat = V_star.ravel(order="F")
    # A. iteration operator (final=False), exactly once
    Q_iter, u_iter, diag_iter, records_current = solver.build_operator_and_u(
        V_star, labor0, 0.0, 0.0, final=False)
    R_iter = rho * V_flat - (u_iter + Q_iter.dot(V_flat))
    # B. accepted stale-record final operator (final=True)
    Q_final_stale, u_final_stale, diag_stale, _ = solver.build_operator_and_u(
        V_star, labor0, 0.0, 0.0, final=True, f0_policies=records_pre_step8)
    R_final_stale = rho * V_flat - (u_final_stale + Q_final_stale.dot(V_flat))
    # C. diagnostic current-record final operator (final=True)
    Q_final_current, u_final_current, diag_current, _ = \
        solver.build_operator_and_u(
            V_star, labor0, 0.0, 0.0, final=True, f0_policies=records_current)
    R_final_current = rho * V_flat - (u_final_current + Q_final_current.dot(V_flat))
    for name, R in (("R_iter", R_iter), ("R_final_stale", R_final_stale),
                    ("R_final_current", R_final_current)):
        if not np.isfinite(R).all():
            raise F0ValidationSemanticsFailure(
                f"non-finite residual component in {name}")
    D_total = R_final_stale - R_iter
    D_stale = R_final_stale - R_final_current
    D_rate = R_final_current - R_iter
    add_err = D_total - (D_stale + D_rate)
    add_err_inf = float(np.max(np.abs(add_err)))
    if not (np.isfinite(add_err).all() and add_err_inf <= DECOMPOSITION_TOL):
        raise F0ValidationSemanticsFailure(
            f"D_total = D_stale + D_rate fails within tolerance: "
            f"max|err| = {add_err_inf:.6e} > {DECOMPOSITION_TOL:.6e}")
    return {
        # matrices / vectors / records (not persisted)
        "Q_iter": Q_iter, "u_iter": u_iter, "diag_iter": diag_iter,
        "records_current": records_current,
        "Q_final_stale": Q_final_stale, "u_final_stale": u_final_stale,
        "diag_stale": diag_stale,
        "Q_final_current": Q_final_current, "u_final_current": u_final_current,
        "diag_current": diag_current,
        "R_iter": R_iter, "R_final_stale": R_final_stale,
        "R_final_current": R_final_current,
        "D_total": D_total, "D_stale": D_stale, "D_rate": D_rate,
        # stats
        "stats_iter": residual_stats(solver, R_iter),
        "stats_final_stale": residual_stats(solver, R_final_stale),
        "stats_final_current": residual_stats(solver, R_final_current),
        "stats_d_total": residual_stats(solver, D_total),
        "stats_d_stale": residual_stats(solver, D_stale),
        "stats_d_rate": residual_stats(solver, D_rate),
        "add_err_inf": add_err_inf,
        # operator diagnostics
        "max_abs_q1_iter": _max_abs_q1(Q_iter),
        "max_abs_q1_final_stale": _max_abs_q1(Q_final_stale),
        "max_abs_q1_final_current": _max_abs_q1(Q_final_current),
        "expansions_iter": int(diag_iter["total_expansions"]),
        "bindings_iter": int(diag_iter["artificial_binding"]),
        "expansions_final_stale": int(diag_stale["total_expansions"]),
        "bindings_final_stale": int(diag_stale["artificial_binding"]),
        "expansions_final_current": int(diag_current["total_expansions"]),
        "bindings_final_current": int(diag_current["artificial_binding"]),
    }


# ---------------------------------------------------------------------------
# 4. ONE compact F0 policy/control provenance audit (F0 rows only)
# ---------------------------------------------------------------------------
def f0_provenance_controls(solver: BoundaryHJBSolver,
                           records_pre_step8: list,
                           records_current: list) -> dict:
    """F0-row-only continuous-control provenance of the two record sets.

    Compares ``records_pre_step8`` vs ``records_current`` on F0 rows:
    changed sector/transfer-label count and max |Delta consumption|, |Delta
    labor|, |Delta transfer|, |Delta mu_a|, |Delta mu_b|, |Delta utility|.
    A same sector/transfer label is NOT treated as proof of identical
    continuous controls. FAIL-CLOSED on missing F0 records (provenance
    ambiguity).
    """
    _, f0_rows = f0_rows_of(solver)
    changed = 0
    d_c = d_l = d_t = d_mu_a = d_mu_b = d_u = 0.0
    for r in f0_rows:
        p = records_pre_step8[r]
        c = records_current[r]
        if p is None or c is None:
            raise F0ValidationSemanticsFailure(
                f"missing F0 record at row {r} -> provenance ambiguity")
        if p.sector != c.sector:
            changed += 1
        d_c = max(d_c, abs(float(p.consumption) - float(c.consumption)))
        d_l = max(d_l, abs(float(p.labor) - float(c.labor)))
        d_t = max(d_t, abs(float(p.transfer) - float(c.transfer)))
        d_mu_a = max(d_mu_a, abs(float(p.mu_a) - float(c.mu_a)))
        d_mu_b = max(d_mu_b, abs(float(p.mu_b) - float(c.mu_b)))
        d_u = max(d_u, abs(float(p.utility) - float(c.utility)))
    return {
        "f0_row_count": int(len(f0_rows)),
        "changed_sector_transfer_label_count": int(changed),
        "max_abs_delta_consumption": float(d_c),
        "max_abs_delta_labor": float(d_l),
        "max_abs_delta_transfer": float(d_t),
        "max_abs_delta_mu_a": float(d_mu_a),
        "max_abs_delta_mu_b": float(d_mu_b),
        "max_abs_delta_utility": float(d_u),
    }


def _rowwise_max_abs_q_diff(solver: BoundaryHJBSolver,
                            Qa: sparse.csr_matrix, Qb: sparse.csr_matrix,
                            f0_rows: np.ndarray) -> tuple[float, Optional[int]]:
    """Per F0 row: max absolute entry difference; return the max over rows
    with the argmax row."""
    best, best_row = 0.0, None
    for r in f0_rows:
        va = np.asarray(Qa.getrow(int(r)).toarray()).ravel()
        vb = np.asarray(Qb.getrow(int(r)).toarray()).ravel()
        m = float(np.max(np.abs(va - vb)))
        if m > best:
            best, best_row = m, int(r)
    return best, best_row


def _max_abs_u_diff(ua: np.ndarray, ub: np.ndarray,
                    f0_rows: np.ndarray) -> tuple[float, Optional[int]]:
    best, best_row = 0.0, None
    for r in f0_rows:
        m = abs(float(ua[int(r)]) - float(ub[int(r)]))
        if m > best:
            best, best_row = m, int(r)
    return best, best_row


def f0_operator_differences(solver: BoundaryHJBSolver,
                            Q_final_stale: sparse.csr_matrix,
                            Q_final_current: sparse.csr_matrix,
                            Q_iter: sparse.csr_matrix,
                            u_final_stale: np.ndarray,
                            u_final_current: np.ndarray,
                            u_iter: np.ndarray) -> dict:
    """F0-only rowwise max absolute operator / u differences."""
    _, f0_rows = f0_rows_of(solver)

    def st(row: Optional[int]):
        if row is None:
            return None
        node, nz_i = row % solver.n, row // solver.n
        return _state_info(solver, node, nz_i)

    q_sc, row_sc = _rowwise_max_abs_q_diff(
        solver, Q_final_stale, Q_final_current, f0_rows)
    q_ci, row_ci = _rowwise_max_abs_q_diff(
        solver, Q_final_current, Q_iter, f0_rows)
    u_sc, row_us = _max_abs_u_diff(u_final_stale, u_final_current, f0_rows)
    u_ci, row_uc = _max_abs_u_diff(u_final_current, u_iter, f0_rows)
    return {
        "q_final_stale_minus_final_current_rowwise_max": float(q_sc),
        "q_final_stale_minus_final_current_argmax_state": st(row_sc),
        "q_final_current_minus_iter_rowwise_max": float(q_ci),
        "q_final_current_minus_iter_argmax_state": st(row_ci),
        "u_final_stale_minus_final_current_max": float(u_sc),
        "u_final_stale_minus_final_current_argmax_state": st(row_us),
        "u_final_current_minus_iter_max": float(u_ci),
        "u_final_current_minus_iter_argmax_state": st(row_uc),
    }


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------
@dataclass
class F0ValidationSemanticsResult:
    outcome: str
    # -- reconstruction ------------------------------------------------------
    iterations: int
    trace: list[dict]
    v0_min_boundary_pb: float
    min_accepted_boundary_pb: float
    final_statistic: Optional[float]
    min_boundary_pb_star: float
    wall_state: Optional[dict]
    # -- three residuals -----------------------------------------------------
    r_iter_inf: Optional[float]
    r_iter_argmax: Optional[dict]
    r_iter_f0_max: Optional[float]
    r_iter_f0_argmax: Optional[dict]
    r_iter_boundary_max: Optional[float]
    r_iter_boundary_argmax: Optional[dict]
    r_final_stale_inf: Optional[float]
    r_final_stale_argmax: Optional[dict]
    r_final_stale_f0_max: Optional[float]
    r_final_stale_f0_argmax: Optional[dict]
    r_final_stale_boundary_max: Optional[float]
    r_final_stale_boundary_argmax: Optional[dict]
    r_final_current_inf: Optional[float]
    r_final_current_argmax: Optional[dict]
    r_final_current_f0_max: Optional[float]
    r_final_current_f0_argmax: Optional[dict]
    r_final_current_boundary_max: Optional[float]
    r_final_current_boundary_argmax: Optional[dict]
    # -- exact decomposition -------------------------------------------------
    d_total_inf: Optional[float]
    d_total_argmax: Optional[dict]
    d_total_f0_max: Optional[float]
    d_total_boundary_max: Optional[float]
    d_stale_inf: Optional[float]
    d_stale_argmax: Optional[dict]
    d_stale_f0_max: Optional[float]
    d_stale_boundary_max: Optional[float]
    d_rate_inf: Optional[float]
    d_rate_argmax: Optional[dict]
    d_rate_f0_max: Optional[float]
    d_rate_boundary_max: Optional[float]
    add_err_inf: Optional[float]
    # -- operator diagnostics ------------------------------------------------
    max_abs_q1_iter: Optional[float]
    max_abs_q1_final_stale: Optional[float]
    max_abs_q1_final_current: Optional[float]
    expansions_iter: Optional[int]
    bindings_iter: Optional[int]
    expansions_final_stale: Optional[int]
    bindings_final_stale: Optional[int]
    expansions_final_current: Optional[int]
    bindings_final_current: Optional[int]
    # -- F0 provenance -------------------------------------------------------
    f0_row_count: Optional[int]
    changed_label_count: Optional[int]
    max_abs_delta_consumption: Optional[float]
    max_abs_delta_labor: Optional[float]
    max_abs_delta_transfer: Optional[float]
    max_abs_delta_mu_a: Optional[float]
    max_abs_delta_mu_b: Optional[float]
    max_abs_delta_utility: Optional[float]
    q_stale_minus_current_rowwise_max: Optional[float]
    q_stale_minus_current_argmax: Optional[dict]
    q_current_minus_iter_rowwise_max: Optional[float]
    q_current_minus_iter_argmax: Optional[dict]
    u_stale_minus_current_max: Optional[float]
    u_stale_minus_current_argmax: Optional[dict]
    u_current_minus_iter_max: Optional[float]
    u_current_minus_iter_argmax: Optional[dict]
    # -- attribution ---------------------------------------------------------
    staler_record_dominant: bool = False
    final_rate_semantics_dominant_or_tied: bool = False
    r_final_current_lt_stale: bool = False
    # -- determinism ----------------------------------------------------------
    deterministic_repeat_identical: bool = False
    failure_detail: Optional[dict] = None

    def to_summary_csv_lines(self) -> list[str]:
        """Key/value summary CSV (DLH_5VQ_F0_FINAL_VALIDATION_SUMMARY.csv)."""

        def st(d: Optional[dict]) -> str:
            if d is None:
                return ""
            return (f"node={d.get('node')},j={d.get('j')},i={d.get('i')},"
                    f"z={d.get('z')},family={d.get('family')}")

        def f(x) -> str:
            return "" if x is None else f"{x:.12g}"

        rows: list[tuple[str, str]] = [
            ("outcome", self.outcome),
            ("reconstruction.iterations", str(self.iterations)),
            ("reconstruction.v0_min_boundary_pb", f(self.v0_min_boundary_pb)),
            ("reconstruction.min_accepted_boundary_pb", f(self.min_accepted_boundary_pb)),
            ("reconstruction.final_statistic", f(self.final_statistic)),
            ("reconstruction.min_boundary_pb_star", f(self.min_boundary_pb_star)),
            ("reconstruction.wall_state", st(self.wall_state)),
            ("residual_iter.inf_norm", f(self.r_iter_inf)),
            ("residual_iter.argmax", st(self.r_iter_argmax)),
            ("residual_iter.f0_max", f(self.r_iter_f0_max)),
            ("residual_iter.f0_argmax", st(self.r_iter_f0_argmax)),
            ("residual_iter.boundary_max", f(self.r_iter_boundary_max)),
            ("residual_iter.boundary_argmax", st(self.r_iter_boundary_argmax)),
            ("residual_final_stale.inf_norm", f(self.r_final_stale_inf)),
            ("residual_final_stale.argmax", st(self.r_final_stale_argmax)),
            ("residual_final_stale.f0_max", f(self.r_final_stale_f0_max)),
            ("residual_final_stale.f0_argmax", st(self.r_final_stale_f0_argmax)),
            ("residual_final_stale.boundary_max", f(self.r_final_stale_boundary_max)),
            ("residual_final_stale.boundary_argmax", st(self.r_final_stale_boundary_argmax)),
            ("residual_final_current.inf_norm", f(self.r_final_current_inf)),
            ("residual_final_current.argmax", st(self.r_final_current_argmax)),
            ("residual_final_current.f0_max", f(self.r_final_current_f0_max)),
            ("residual_final_current.f0_argmax", st(self.r_final_current_f0_argmax)),
            ("residual_final_current.boundary_max", f(self.r_final_current_boundary_max)),
            ("residual_final_current.boundary_argmax", st(self.r_final_current_boundary_argmax)),
            ("decomposition.d_total_inf", f(self.d_total_inf)),
            ("decomposition.d_total_argmax", st(self.d_total_argmax)),
            ("decomposition.d_total_f0_max", f(self.d_total_f0_max)),
            ("decomposition.d_total_boundary_max", f(self.d_total_boundary_max)),
            ("decomposition.d_stale_inf", f(self.d_stale_inf)),
            ("decomposition.d_stale_argmax", st(self.d_stale_argmax)),
            ("decomposition.d_stale_f0_max", f(self.d_stale_f0_max)),
            ("decomposition.d_stale_boundary_max", f(self.d_stale_boundary_max)),
            ("decomposition.d_rate_inf", f(self.d_rate_inf)),
            ("decomposition.d_rate_argmax", st(self.d_rate_argmax)),
            ("decomposition.d_rate_f0_max", f(self.d_rate_f0_max)),
            ("decomposition.d_rate_boundary_max", f(self.d_rate_boundary_max)),
            ("decomposition.additive_error_inf", f(self.add_err_inf)),
            ("operator.max_abs_q1_iter", f(self.max_abs_q1_iter)),
            ("operator.max_abs_q1_final_stale", f(self.max_abs_q1_final_stale)),
            ("operator.max_abs_q1_final_current", f(self.max_abs_q1_final_current)),
            ("operator.expansions_iter", str(self.expansions_iter)),
            ("operator.bindings_iter", str(self.bindings_iter)),
            ("operator.expansions_final_stale", str(self.expansions_final_stale)),
            ("operator.bindings_final_stale", str(self.bindings_final_stale)),
            ("operator.expansions_final_current", str(self.expansions_final_current)),
            ("operator.bindings_final_current", str(self.bindings_final_current)),
            ("provenance.f0_row_count", str(self.f0_row_count)),
            ("provenance.changed_sector_transfer_label_count", str(self.changed_label_count)),
            ("provenance.max_abs_delta_consumption", f(self.max_abs_delta_consumption)),
            ("provenance.max_abs_delta_labor", f(self.max_abs_delta_labor)),
            ("provenance.max_abs_delta_transfer", f(self.max_abs_delta_transfer)),
            ("provenance.max_abs_delta_mu_a", f(self.max_abs_delta_mu_a)),
            ("provenance.max_abs_delta_mu_b", f(self.max_abs_delta_mu_b)),
            ("provenance.max_abs_delta_utility", f(self.max_abs_delta_utility)),
            ("opdiff.q_final_stale_minus_final_current_rowwise_max", f(self.q_stale_minus_current_rowwise_max)),
            ("opdiff.q_final_stale_minus_final_current_argmax", st(self.q_stale_minus_current_argmax)),
            ("opdiff.q_final_current_minus_iter_rowwise_max", f(self.q_current_minus_iter_rowwise_max)),
            ("opdiff.q_final_current_minus_iter_argmax", st(self.q_current_minus_iter_argmax)),
            ("opdiff.u_final_stale_minus_final_current_max", f(self.u_stale_minus_current_max)),
            ("opdiff.u_final_stale_minus_final_current_argmax", st(self.u_stale_minus_current_argmax)),
            ("opdiff.u_final_current_minus_iter_max", f(self.u_current_minus_iter_max)),
            ("opdiff.u_final_current_minus_iter_argmax", st(self.u_current_minus_iter_argmax)),
            ("attribution.stale_record_dominant", str(self.staler_record_dominant).lower()),
            ("attribution.final_rate_semantics_dominant_or_tied",
             str(self.final_rate_semantics_dominant_or_tied).lower()),
            ("attribution.r_final_current_inf_lt_r_final_stale_inf",
             str(self.r_final_current_lt_stale).lower()),
            ("deterministic_repeat_identical",
             str(self.deterministic_repeat_identical).lower()),
        ]
        return [",".join([k, v]) for (k, v) in rows]


def run_issue65_audit() -> F0ValidationSemanticsResult:
    """Exactly one full Issue #65 audit: 1) ONE deterministic reconstruction;
    2) ONE iteration-operator build; 3) ONE stale-record final=True build;
    4) ONE current-record final=True build; 5) ONE compact F0 provenance
    audit; 6) frozen attribution."""
    failure_detail: Optional[dict] = None
    try:
        rec = reconstruct_issue63_stagnation_state()
        solver: BoundaryHJBSolver = rec["solver"]
        labor0: np.ndarray = rec["labor0"]
        V_star: np.ndarray = rec["V_star"]
        records_pre: list = rec["records_pre_step8"]
        rho: float = rec["rho"]
        trace: list = rec["trace"]
        wall_pb, wall_node, wall_nz = min_boundary_pb_state(
            solver, V_star, labor0)
        if not np.isfinite(wall_pb):
            raise F0ValidationSemanticsFailure(
                "non-finite required boundary p_b at V_*")

        three = build_three_operators(
            solver, V_star, labor0, records_pre, rho)
        prov = f0_provenance_controls(solver, records_pre, three["records_current"])
        opdiff = f0_operator_differences(
            solver, three["Q_final_stale"], three["Q_final_current"],
            three["Q_iter"], three["u_final_stale"], three["u_final_current"],
            three["u_iter"])

        s_iter = three["stats_iter"]
        s_stale = three["stats_final_stale"]
        s_curr = three["stats_final_current"]
        s_dt = three["stats_d_total"]
        s_ds = three["stats_d_stale"]
        s_dr = three["stats_d_rate"]
        d_stale_inf = s_ds["total"]["max_abs"]
        d_rate_inf = s_dr["total"]["max_abs"]
        staler_dominant = bool(d_stale_inf > d_rate_inf)
        r_final_lt = bool(s_curr["total"]["max_abs"] < s_stale["total"]["max_abs"])
        return F0ValidationSemanticsResult(
            outcome="", iterations=RECONSTRUCT_STEPS, trace=trace,
            v0_min_boundary_pb=float(rec["v0_min_boundary_pb"]),
            min_accepted_boundary_pb=float(rec["min_accepted_boundary_pb"]),
            final_statistic=float(trace[-1]["accepted_max_stat"]),
            min_boundary_pb_star=float(wall_pb),
            wall_state=_state_info(solver, wall_node, wall_nz),
            r_iter_inf=s_iter["total"]["max_abs"],
            r_iter_argmax=s_iter["total"]["argmax_state"],
            r_iter_f0_max=s_iter["f0"]["max_abs"],
            r_iter_f0_argmax=s_iter["f0"]["argmax_state"],
            r_iter_boundary_max=s_iter["boundary"]["max_abs"],
            r_iter_boundary_argmax=s_iter["boundary"]["argmax_state"],
            r_final_stale_inf=s_stale["total"]["max_abs"],
            r_final_stale_argmax=s_stale["total"]["argmax_state"],
            r_final_stale_f0_max=s_stale["f0"]["max_abs"],
            r_final_stale_f0_argmax=s_stale["f0"]["argmax_state"],
            r_final_stale_boundary_max=s_stale["boundary"]["max_abs"],
            r_final_stale_boundary_argmax=s_stale["boundary"]["argmax_state"],
            r_final_current_inf=s_curr["total"]["max_abs"],
            r_final_current_argmax=s_curr["total"]["argmax_state"],
            r_final_current_f0_max=s_curr["f0"]["max_abs"],
            r_final_current_f0_argmax=s_curr["f0"]["argmax_state"],
            r_final_current_boundary_max=s_curr["boundary"]["max_abs"],
            r_final_current_boundary_argmax=s_curr["boundary"]["argmax_state"],
            d_total_inf=s_dt["total"]["max_abs"],
            d_total_argmax=s_dt["total"]["argmax_state"],
            d_total_f0_max=s_dt["f0"]["max_abs"],
            d_total_boundary_max=s_dt["boundary"]["max_abs"],
            d_stale_inf=d_stale_inf,
            d_stale_argmax=s_ds["total"]["argmax_state"],
            d_stale_f0_max=s_ds["f0"]["max_abs"],
            d_stale_boundary_max=s_ds["boundary"]["max_abs"],
            d_rate_inf=d_rate_inf,
            d_rate_argmax=s_dr["total"]["argmax_state"],
            d_rate_f0_max=s_dr["f0"]["max_abs"],
            d_rate_boundary_max=s_dr["boundary"]["max_abs"],
            add_err_inf=three["add_err_inf"],
            max_abs_q1_iter=three["max_abs_q1_iter"],
            max_abs_q1_final_stale=three["max_abs_q1_final_stale"],
            max_abs_q1_final_current=three["max_abs_q1_final_current"],
            expansions_iter=three["expansions_iter"],
            bindings_iter=three["bindings_iter"],
            expansions_final_stale=three["expansions_final_stale"],
            bindings_final_stale=three["bindings_final_stale"],
            expansions_final_current=three["expansions_final_current"],
            bindings_final_current=three["bindings_final_current"],
            f0_row_count=prov["f0_row_count"],
            changed_label_count=prov["changed_sector_transfer_label_count"],
            max_abs_delta_consumption=prov["max_abs_delta_consumption"],
            max_abs_delta_labor=prov["max_abs_delta_labor"],
            max_abs_delta_transfer=prov["max_abs_delta_transfer"],
            max_abs_delta_mu_a=prov["max_abs_delta_mu_a"],
            max_abs_delta_mu_b=prov["max_abs_delta_mu_b"],
            max_abs_delta_utility=prov["max_abs_delta_utility"],
            q_stale_minus_current_rowwise_max=opdiff["q_final_stale_minus_final_current_rowwise_max"],
            q_stale_minus_current_argmax=opdiff["q_final_stale_minus_final_current_argmax_state"],
            q_current_minus_iter_rowwise_max=opdiff["q_final_current_minus_iter_rowwise_max"],
            q_current_minus_iter_argmax=opdiff["q_final_current_minus_iter_argmax_state"],
            u_stale_minus_current_max=opdiff["u_final_stale_minus_final_current_max"],
            u_stale_minus_current_argmax=opdiff["u_final_stale_minus_final_current_argmax_state"],
            u_current_minus_iter_max=opdiff["u_final_current_minus_iter_max"],
            u_current_minus_iter_argmax=opdiff["u_final_current_minus_iter_argmax_state"],
            staler_record_dominant=staler_dominant,
            final_rate_semantics_dominant_or_tied=not staler_dominant,
            r_final_current_lt_stale=r_final_lt,
        )
    except (F0ValidationSemanticsFailure, FTBStepConstructionFailure,
            BoundaryHJBFailure) as exc:
        failure_detail = {"message": str(exc)}
        return F0ValidationSemanticsResult(
            outcome=TERMINAL_C, iterations=0, trace=[], v0_min_boundary_pb=0.0,
            min_accepted_boundary_pb=0.0, final_statistic=None,
            min_boundary_pb_star=0.0, wall_state=None,
            r_iter_inf=None, r_iter_argmax=None, r_iter_f0_max=None,
            r_iter_f0_argmax=None, r_iter_boundary_max=None,
            r_iter_boundary_argmax=None, r_final_stale_inf=None,
            r_final_stale_argmax=None, r_final_stale_f0_max=None,
            r_final_stale_f0_argmax=None, r_final_stale_boundary_max=None,
            r_final_stale_boundary_argmax=None, r_final_current_inf=None,
            r_final_current_argmax=None, r_final_current_f0_max=None,
            r_final_current_f0_argmax=None, r_final_current_boundary_max=None,
            r_final_current_boundary_argmax=None, d_total_inf=None,
            d_total_argmax=None, d_total_f0_max=None, d_total_boundary_max=None,
            d_stale_inf=None, d_stale_argmax=None, d_stale_f0_max=None,
            d_stale_boundary_max=None, d_rate_inf=None, d_rate_argmax=None,
            d_rate_f0_max=None, d_rate_boundary_max=None, add_err_inf=None,
            max_abs_q1_iter=None, max_abs_q1_final_stale=None,
            max_abs_q1_final_current=None, expansions_iter=None,
            bindings_iter=None, expansions_final_stale=None,
            bindings_final_stale=None, expansions_final_current=None,
            bindings_final_current=None, f0_row_count=None,
            changed_label_count=None, max_abs_delta_consumption=None,
            max_abs_delta_labor=None, max_abs_delta_transfer=None,
            max_abs_delta_mu_a=None, max_abs_delta_mu_b=None,
            max_abs_delta_utility=None, q_stale_minus_current_rowwise_max=None,
            q_stale_minus_current_argmax=None,
            q_current_minus_iter_rowwise_max=None,
            q_current_minus_iter_argmax=None, u_stale_minus_current_max=None,
            u_stale_minus_current_argmax=None, u_current_minus_iter_max=None,
            u_current_minus_iter_argmax=None, failure_detail=failure_detail,
        )


def _canon(r: F0ValidationSemanticsResult):
    def c(x):
        if isinstance(x, dict):
            return tuple(sorted((k, c(v)) for k, v in x.items()))
        if isinstance(x, list):
            return tuple(c(v) for v in x)
        if isinstance(x, float):
            return ("f", repr(x))
        if isinstance(x, np.ndarray):
            return ("a", repr(x.tolist()))
        return (type(x).__name__, str(x))

    return (
        c(r.trace), c(r.iterations), c(r.final_statistic),
        c(r.min_boundary_pb_star), c(r.wall_state),
        c(r.r_iter_inf), c(r.r_iter_argmax), c(r.r_iter_f0_max),
        c(r.r_iter_f0_argmax), c(r.r_iter_boundary_max),
        c(r.r_iter_boundary_argmax), c(r.r_final_stale_inf),
        c(r.r_final_stale_argmax), c(r.r_final_stale_f0_max),
        c(r.r_final_stale_f0_argmax), c(r.r_final_stale_boundary_max),
        c(r.r_final_stale_boundary_argmax), c(r.r_final_current_inf),
        c(r.r_final_current_argmax), c(r.r_final_current_f0_max),
        c(r.r_final_current_f0_argmax), c(r.r_final_current_boundary_max),
        c(r.r_final_current_boundary_argmax), c(r.d_total_inf),
        c(r.d_total_argmax), c(r.d_total_f0_max), c(r.d_total_boundary_max),
        c(r.d_stale_inf), c(r.d_stale_argmax), c(r.d_stale_f0_max),
        c(r.d_stale_boundary_max), c(r.d_rate_inf), c(r.d_rate_argmax),
        c(r.d_rate_f0_max), c(r.d_rate_boundary_max), c(r.add_err_inf),
        c(r.max_abs_q1_iter), c(r.max_abs_q1_final_stale),
        c(r.max_abs_q1_final_current), c(r.expansions_iter),
        c(r.bindings_iter), c(r.expansions_final_stale),
        c(r.bindings_final_stale), c(r.expansions_final_current),
        c(r.bindings_final_current), c(r.f0_row_count),
        c(r.changed_label_count), c(r.max_abs_delta_consumption),
        c(r.max_abs_delta_labor), c(r.max_abs_delta_transfer),
        c(r.max_abs_delta_mu_a), c(r.max_abs_delta_mu_b),
        c(r.max_abs_delta_utility), c(r.q_stale_minus_current_rowwise_max),
        c(r.q_stale_minus_current_argmax),
        c(r.q_current_minus_iter_rowwise_max), c(r.q_current_minus_iter_argmax),
        c(r.u_stale_minus_current_max), c(r.u_stale_minus_current_argmax),
        c(r.u_current_minus_iter_max), c(r.u_current_minus_iter_argmax),
        c(r.staler_record_dominant),
        c(r.final_rate_semantics_dominant_or_tied),
        c(r.r_final_current_lt_stale),
    )


def finalize_outcome(r1: F0ValidationSemanticsResult,
                     repeat_identical: bool) -> str:
    """Exactly one Issue #65 terminal from the local evidence (fail closed)."""
    if not repeat_identical:
        return TERMINAL_C           # deterministic repeat mismatch = inconsistency
    if r1.failure_detail is not None:
        return TERMINAL_C
    # reconstruction must reproduce the accepted Issue #63 stagnation state
    trace = r1.trace
    recon_ok = (
        len(trace) == RECONSTRUCT_STEPS
        and trace[-1]["path"] == "root"
        and trace[-1]["cap_direct"] is False
        and r1.final_statistic is not None
        and abs(r1.final_statistic - 3.6614352438846254e-08)
        / 3.6614352438846254e-08 <= 1e-6
        and r1.min_boundary_pb_star is not None
        and abs(r1.min_boundary_pb_star - 4.8089461301970005e-09)
        / 4.8089461301970005e-09 <= 1e-6
        and r1.r_final_stale_inf is not None
        and abs(r1.r_final_stale_inf - 490.7560425919994)
        / 490.7560425919994 <= 1e-9
        and r1.wall_state is not None
        and r1.wall_state["node"] == 332
        and r1.wall_state["family"] == "F3"
        and r1.wall_state["i"] == 13
        and r1.wall_state["j"] == 13
        and r1.wall_state["z"] == 1
    )
    if not recon_ok:
        return TERMINAL_C
    # additive decomposition verified within the declared tolerance
    if r1.add_err_inf is None or r1.add_err_inf > DECOMPOSITION_TOL:
        return TERMINAL_C
    if r1.d_stale_inf is None or r1.d_rate_inf is None:
        return TERMINAL_C
    if r1.d_stale_inf > r1.d_rate_inf:
        return TERMINAL_A           # STALE_RECORD_DOMINANT
    return TERMINAL_B               # FINAL_RATE_SEMANTICS_DOMINANT_OR_TIED


def run_issue65_audit_twice() -> tuple[F0ValidationSemanticsResult, bool]:
    """One full audit + one deterministic repeat (bit-identical);
    returns (finalized result with exactly one terminal, repeat_identical)."""
    r1 = run_issue65_audit()
    r2 = run_issue65_audit()
    identical = bool(_canon(r1) == _canon(r2))
    outcome = finalize_outcome(r1, identical)
    return (
        dataclasses.replace(
            r1, outcome=outcome,
            deterministic_repeat_identical=identical),
        identical,
    )
