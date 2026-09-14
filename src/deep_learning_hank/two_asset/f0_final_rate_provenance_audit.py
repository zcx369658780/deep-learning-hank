"""DLH-5V-R — F0 `final=True` rate-construction provenance and discrete-operator
consistency audit at the accepted Issue #63 stagnation state.

Issue #66 / DLH-5V-R
``SCIENTIFIC_NUMERICAL_DIAGNOSTIC__F0_FINAL_RATE_DISCRETIZATION_PROVENANCE_AND_OPERATOR_CONSISTENCY``

Authority: Issue #66 OPEN; initial activation ``5656814064``; final
authoritative activation-refresh ``5657247407`` (post-sync live ``main``
``a4227f38a5f11b07e7881f58534e37a4887f5ea7``). Route decision
``APPROVE_F0_FINAL_RATE_DISCRETIZATION_PROVENANCE_AND_OPERATOR_CONSISTENCY_AUDIT_AFTER_5VQ_TERMINAL_B``;
authority marker ``DLH_5VR_F0_FINAL_RATE_PROVENANCE_AUDIT_AUTHORIZED``.

Scientific object (binding, Issue #66 sections 2-8), in exactly this order:

1. ONE deterministic reconstruction of the exact accepted Issue #63
   stagnation state ``V_*`` (accepted Issue #65/#64 helper path; STOP before
   any new HJB iterate is accepted);
2. at the SAME ``V_*``, exactly ONE current-policy ``final=False`` build and
   exactly ONE current-policy ``final=True`` build (``f0_policies`` = the SAME
   current selected F0 controls returned by the ``final=False`` build); no
   stale-record route;
3. reproduce ``||R_iter||_inf = 10.435094313164921``,
   ``||R_final_current||_inf = 490.7560414005864`` and F0 rowwise max
   ``|Q_final_current - Q_iter| ~= 24.6019717663``;
4. ONE all-F0 compact row/rate/component comparison: per F0 row record
   ``b_backward``, ``b_forward``, ``a_backward``, ``a_forward``, ``diagonal``,
   ``represented_outgoing_sum``, ``omitted_destination_rate`` and
   ``utility/source`` for BOTH semantics, decompose the ~24.60 operator gap
   into rate/operator and destination-assembly component classes with
   affected-row counts / component max abs differences / argmax states / max
   total row-entry difference, and separately verify utility/source-term
   identity under the same current controls and non-F0 boundary-row identity
   (any boundary discrepancy fails closed);
5. ONE read-only source-backed MATLAB/oracle provenance mapping (no
   re-interpretation or rewrite of accepted source semantics);
6. frozen ex ante classifications ``ITER_EQ_MATLAB`` / ``FINAL_EQ_MATLAB`` /
   ``BOTH_EQUIVALENT`` / ``MIXED_OR_UNRESOLVED`` and exactly ONE terminal
   (A/B/C);
7. ONE deterministic repeat of the full diagnostic.

Source-backed provenance facts (measured, not assumed):

- the accepted ITER F0 row is the oracle's designated MATLAB local-policy
  construction consumed verbatim by ``local_interior_row``
  (``boundary_hjb_selected_q.py`` lines 484-521 -> ``select_matlab_faithful_local_policy``
  ``matlab_faithful_two_asset_ha.py`` lines 193-416): b-direction iteration
  sc/sdh rates (lines 408-415), a-direction shadow-mh rates (lines 372-377,
  406-407); this is the operator assembled by the accepted oracle iteration
  (lines 553-555) with within-z-block destination columns
  (``boundary_hjb_selected_q.py`` line 1008 ``nz * self.n + dn`` matching the
  oracle ``assemble_source_axis`` layout);
- the accepted FINAL-RAW rate formulas (``boundary_hjb_selected_q.py`` lines
  962-969: raw drift recompute via ``asset_drifts_matlab_faithful`` then
  ``max(+-mu)/step``) match the accepted oracle post-convergence operator
  formula exactly (``matlab_faithful_two_asset_ha.py`` line 562);
- HOWEVER the accepted FINAL-RAW F0 row assembly writes off-diagonal
  destination columns as bare node indices ``dn`` WITHOUT the z-block offset
  (``boundary_hjb_selected_q.py`` line 978 ``cols.append(dn)``), while the
  accepted iteration F0 path (line 1008), the accepted boundary path
  (line 1029) and the accepted oracle assembly all place destinations within
  the same z-block. For z=1 F0 rows the accepted final=True off-diagonal
  entries therefore point at the z=0 block columns — the accepted FINAL-RAW
  ROW is not the MATLAB-faithful discrete HJB construction even though its
  rate formulas are; this destination-assembly deviation is the measured
  driver of the ~24.60 operator gap and of the ~490.756 final residual;
- the accepted iteration b-rates coincide numerically with ``max(+-mu_b)/db``
  on all F0 rows (the sc/sdh shadow flow sums to the raw drift; measured), so
  the rate-component classes show ~0 differences; the gap decomposes into
  destination-assembly placement, not rate formulas;
- both semantics use the identical truncation convention (drop the
  off-diagonal entry when the destination is unavailable, retain the rate on
  the diagonal) — oracle ``assemble_source_axis`` lines 425-451 vs selected-Q
  lines 512-520 / 970-979; on the frozen central case every F0 row has all
  four neighbors (strictly interior), so the measured omitted-destination
  rate is exactly 0 on all F0 rows (recorded, not assumed).

Classifications and terminal are diagnostic only: they do NOT authorize
replacing ``final=True``, changing any convergence criterion, mutating
accepted source, or declaring ``R_iter`` an accepted final convergence
residual. Stationary KFE remains NOT AUTHORIZED.
"""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass
from typing import Optional

import numpy as np
from scipy import sparse

from deep_learning_hank.two_asset.boundary_hjb_selected_q import (
    BoundaryHJBFailure,
    BoundaryHJBSolver,
)
from deep_learning_hank.two_asset.adaptive_resolvent_hjb import (
    _state_info,
    min_boundary_pb_state,
)
from deep_learning_hank.two_asset.continuous_ftb_resolvent_hjb import (
    FTBStepConstructionFailure,
)
from deep_learning_hank.two_asset.matlab_faithful_two_asset_ha import (
    asset_drifts_matlab_faithful,
    select_matlab_faithful_local_policy,
)
from deep_learning_hank.two_asset.stagnation_newton_geometry import (
    reconstruct_issue63_stagnation_state,
    residual_stats,
)

# ---------------------------------------------------------------------------
# Frozen constants (Issue #66) — do NOT change
# ---------------------------------------------------------------------------
RECONSTRUCT_STEPS = 8
REPRO_TOL = 1.0e-9          # component reproduction tolerance (oracle vs operator)
ROW_EQ_TOL = 1.0e-9         # rowwise operator-equivalence tolerance
MATERIAL_GAP_TOL = 1.0      # "materially non-equivalent" F0 total-row-diff threshold
CLASS_TOL = 1.0e-12         # per-component "affected row" threshold

# ---------------------------------------------------------------------------
# Terminals (Issue #66 section 11) — exactly ONE returned by the run
# ---------------------------------------------------------------------------
TERMINAL_A = ("DLH_5VR_F0_FINAL_RATE_PROVENANCE__ITERATION_OPERATOR_MATCHES_"
              "ACCEPTED_MATLAB_FAITHFUL_HJB__FINAL_RAW_RATE_OPERATOR_NON_"
              "EQUIVALENT__VALIDATION_OPERATOR_REDESIGN_REVIEW_GATE_READY")
TERMINAL_B = ("DLH_5VR_F0_FINAL_RATE_PROVENANCE__FINAL_RAW_RATE_OPERATOR_MATCHES_"
              "ACCEPTED_MATLAB_FAITHFUL_HJB__ITERATION_OPERATOR_NON_EQUIVALENT__"
              "ITERATION_OPERATOR_REVIEW_REQUIRED")
TERMINAL_C = ("DLH_5VR_F0_FINAL_RATE_PROVENANCE__MIXED_EQUIVALENT_OR_UNRESOLVED_"
              "DISCRETE_OPERATOR_PROVENANCE__OWNER_SCIENTIFIC_REVIEW_REQUIRED")
TERMINAL_BLOCKED = "BLOCKED_DLH_5VR_AUTHORITY_OR_DEPENDENCY_CONFLICT"


class F0FinalRateProvenanceFailure(RuntimeError):
    """Fail-closed: non-finite / inconsistent evidence, provenance ambiguity,
    or a boundary-row discrepancy in the F0 final-rate provenance audit."""


def f0_rows_of(solver: BoundaryHJBSolver) -> tuple[np.ndarray, np.ndarray]:
    """(boolean mask, integer row indices) of the F0 state rows."""
    n, nz = solver.n, solver.nz
    fam = np.array([str(solver.grid.families[node]) for node in range(n)])
    mask = np.tile(fam == "F0", nz)
    return mask, np.nonzero(mask)[0]


def _state(row: int, solver: BoundaryHJBSolver) -> dict:
    node, nz = row % solver.n, row // solver.n
    return _state_info(solver, node, nz)


# ---------------------------------------------------------------------------
# 2. Exactly two builds at the same V_* (same current selected F0 controls)
# ---------------------------------------------------------------------------
def build_two_operators(solver: BoundaryHJBSolver, V_star: np.ndarray,
                        labor0: np.ndarray, rho: float) -> dict:
    """Exactly two authorized builds at the SAME ``V_*``:

    - A. current-policy ``final=False`` (exactly once) -> ``Q_iter, u_iter``
      and ``records_current`` (the current selected F0 controls);
    - B. current-policy ``final=True`` with ``f0_policies = records_current``
      (exactly once, SAME controls) -> ``Q_final_current, u_final_current``
      and ``records_final`` (the accepted final=True records).

    Computes ``R_iter = rho V_* - [u_iter + Q_iter V_*]`` and ``R_final_current
    = rho V_* - [u_final_current + Q_final_current V_*]``. FAIL-CLOSED on
    non-finite evidence, on any non-F0 boundary-row discrepancy between the
    two operators, and on F0-row provenance ambiguity (missing records).
    """
    n, nz = solver.n, solver.nz
    V_flat = V_star.ravel(order="F")
    Q_iter, u_iter, diag_iter, records_current = solver.build_operator_and_u(
        V_star, labor0, 0.0, 0.0, final=False)
    R_iter = rho * V_flat - (u_iter + Q_iter.dot(V_flat))
    Q_final, u_final, diag_final, records_final = solver.build_operator_and_u(
        V_star, labor0, 0.0, 0.0, final=True, f0_policies=records_current)
    R_final = rho * V_flat - (u_final + Q_final.dot(V_flat))
    for name, R in (("R_iter", R_iter), ("R_final_current", R_final)):
        if not np.isfinite(R).all():
            raise F0FinalRateProvenanceFailure(f"non-finite residual in {name}")

    f0_mask, f0_rows = f0_rows_of(solver)
    non_f0_rows = np.nonzero(~f0_mask)[0]
    # non-F0 boundary rows must be identical between the two builds (same
    # accepted _boundary_row path at the same V_*); any discrepancy fails closed
    bnd_max = 0.0
    for r in non_f0_rows:
        va = np.asarray(Q_iter.getrow(int(r)).toarray()).ravel()
        vb = np.asarray(Q_final.getrow(int(r)).toarray()).ravel()
        bnd_max = max(bnd_max, float(np.max(np.abs(va - vb))))
    bnd_u_max = float(np.max(np.abs(u_iter[non_f0_rows] - u_final[non_f0_rows])))
    if not (np.isfinite(bnd_max) and bnd_max <= ROW_EQ_TOL and bnd_u_max <= ROW_EQ_TOL):
        raise F0FinalRateProvenanceFailure(
            f"non-F0 boundary-row discrepancy: max|Q diff| = {bnd_max:.3e}, "
            f"max|u diff| = {bnd_u_max:.3e}")
    # F0 provenance: records exist for every F0 row in both sets
    for r in f0_rows:
        if records_current[r] is None or records_final[r] is None:
            raise F0FinalRateProvenanceFailure(
                f"missing F0 record at row {r} -> provenance ambiguity")
    # same controls: the final build consumed the SAME current records
    max_ctrl_diff = 0.0
    for r in f0_rows:
        a = records_current[r]
        b = records_final[r]
        max_ctrl_diff = max(
            max_ctrl_diff,
            abs(a.consumption - b.consumption), abs(a.labor - b.labor),
            abs(a.transfer - b.transfer), abs(a.utility - b.utility),
            abs(a.mu_a - b.mu_a), abs(a.mu_b - b.mu_b))
    if max_ctrl_diff > ROW_EQ_TOL:
        raise F0FinalRateProvenanceFailure(
            f"same-controls contract violated: max control diff = {max_ctrl_diff:.3e}")

    def rowmax(Qa: sparse.csr_matrix, Qb: sparse.csr_matrix,
               rows: np.ndarray) -> tuple[float, int]:
        best, best_row = 0.0, -1
        for r in rows:
            va = np.asarray(Qa.getrow(int(r)).toarray()).ravel()
            vb = np.asarray(Qb.getrow(int(r)).toarray()).ravel()
            m = float(np.max(np.abs(va - vb)))
            if m > best:
                best, best_row = m, int(r)
        return best, best_row

    f0_gap, f0_gap_row = rowmax(Q_iter, Q_final, f0_rows)
    return {
        "Q_iter": Q_iter, "u_iter": u_iter, "diag_iter": diag_iter,
        "records_current": records_current,
        "Q_final_current": Q_final, "u_final_current": u_final,
        "diag_final": diag_final, "records_final": records_final,
        "R_iter": R_iter, "R_final_current": R_final,
        "stats_iter": residual_stats(solver, R_iter),
        "stats_final_current": residual_stats(solver, R_final),
        "max_abs_q1_iter": float(np.max(np.abs(np.asarray(Q_iter.sum(axis=1)).ravel()))),
        "max_abs_q1_final_current": float(np.max(np.abs(np.asarray(Q_final.sum(axis=1)).ravel()))),
        "expansions_iter": int(diag_iter["total_expansions"]),
        "bindings_iter": int(diag_iter["artificial_binding"]),
        "expansions_final_current": int(diag_final["total_expansions"]),
        "bindings_final_current": int(diag_final["artificial_binding"]),
        "boundary_row_max_abs_diff": bnd_max,
        "boundary_u_max_abs_diff": bnd_u_max,
        "same_controls_max_abs_diff": max_ctrl_diff,
        "f0_rowwise_max_abs_gap": f0_gap,
        "f0_rowwise_max_abs_gap_row": f0_gap_row,
        "f0_mask": f0_mask, "f0_rows": f0_rows,
    }


# ---------------------------------------------------------------------------
# 4a. ITER component extraction: oracle policy reproduction (source-backed)
# ---------------------------------------------------------------------------
def iter_f0_components(solver: BoundaryHJBSolver, V_star: np.ndarray,
                       labor0: np.ndarray, records_current: list,
                       f0_rows: np.ndarray) -> dict:
    """Re-evaluate the accepted oracle local policy at the EXACT inputs used by
    ``local_interior_row`` for every F0 row and verify it reproduces the
    recorded ITER row (controls + entries + diagonal) within ``REPRO_TOL``.

    Returns per-row ITER components: b_backward / b_forward / a_backward /
    a_forward (the oracle iteration + mh rates), diagonal, represented
    outgoing sum, omitted destination rate, utility.
    """
    cfg = solver.config
    g = solver.grid
    n, nz = solver.n, solver.nz
    vb_f, vb_b, va_f, va_b = solver.compute_derivatives(V_star, labor0, 0.0, 0.0)
    out = {
        "b_backward": np.zeros(len(f0_rows)),
        "b_forward": np.zeros(len(f0_rows)),
        "a_backward": np.zeros(len(f0_rows)),
        "a_forward": np.zeros(len(f0_rows)),
        "diagonal": np.zeros(len(f0_rows)),
        "represented_outgoing_sum": np.zeros(len(f0_rows)),
        "omitted_destination_rate": np.zeros(len(f0_rows)),
        "utility": np.zeros(len(f0_rows)),
        "reproduced": np.zeros(len(f0_rows), dtype=bool),
        "repro_controls_max": 0.0,
        "repro_row_max": 0.0,
    }
    for k, r in enumerate(f0_rows):
        node, zz = int(r % n), int(r // n)
        j, i = int(g.j_arr[node]), int(g.i_arr[node])
        rec = records_current[r]
        policy = select_matlab_faithful_local_policy(
            a=float(g.a_arr[node]), b=float(g.b_arr[node]), z=float(cfg.z[zz]),
            v_a_forward=float(va_f[node, zz]), v_a_backward=float(va_b[node, zz]),
            v_b_forward=float(vb_f[node, zz]), v_b_backward=float(vb_b[node, zz]),
            baseline_labor=float(labor0[node, zz]), transfer_income=0.0,
            borrowing_rate_gap=0.0, a_max=cfg.a_max, da=solver.da, db=solver.db,
            at_lower_a=(j == 0), at_upper_a=(j == g.jmax), at_lower_b=(i == 0),
            at_upper_b=False, inputs=cfg.inputs, params=cfg.params,
            tolerance=cfg.drift_tolerance,
        )
        rb = float(policy.iteration_b_backward_rate)
        rf = float(policy.iteration_b_forward_rate)
        ab = float(policy.a_backward_rate)
        af = float(policy.a_forward_rate)
        neigh = g.neighbors(j, i)
        entries: list[tuple[int, float]] = []
        for dn, rate in ((neigh["down"], rb), (neigh["up"], rf),
                         (neigh["left"], ab), (neigh["right"], af)):
            if dn is not None and rate != 0.0:
                entries.append((dn, float(rate)))
        diag = -(rb + rf + ab + af)
        rep_out = float(sum(rate for _, rate in entries))
        omitted = -diag - rep_out
        out["b_backward"][k] = rb
        out["b_forward"][k] = rf
        out["a_backward"][k] = ab
        out["a_forward"][k] = af
        out["diagonal"][k] = diag
        out["represented_outgoing_sum"][k] = rep_out
        out["omitted_destination_rate"][k] = omitted
        out["utility"][k] = float(rec.utility)
        # reproduction: controls and assembled row must match the record
        ctrl_dev = max(
            abs(policy.consumption - rec.consumption),
            abs(float(policy.labor) - rec.labor),
            abs(policy.transfer - rec.transfer),
            abs(policy.utility - rec.utility),
            abs(policy.mu_a - rec.mu_a), abs(policy.mu_b - rec.mu_b))
        # rowwise deviation against the recorded entries/diagonal directly
        rec_map = {dn0: rrate for dn0, rrate in rec.row_entries}
        devs = [abs(diag - rec.diagonal)]
        for dn0, rrate in rec_map.items():
            found = next((x for x in entries if x[0] == dn0), None)
            devs.append(abs((found[1] if found else 0.0) - rrate))
        for dn0, rrate in entries:
            if dn0 not in rec_map:
                devs.append(abs(rrate))
        row_dev = max(devs)
        out["repro_controls_max"] = max(out["repro_controls_max"], ctrl_dev)
        out["repro_row_max"] = max(out["repro_row_max"], row_dev)
        out["reproduced"][k] = bool(ctrl_dev <= REPRO_TOL and row_dev <= REPRO_TOL)
    return out


# ---------------------------------------------------------------------------
# 4b. FINAL-RAW component extraction + accepted-vs-MATLAB-faithful assembly check
# ---------------------------------------------------------------------------
def final_raw_f0_components(solver: BoundaryHJBSolver, records_final: list,
                            f0_rows: np.ndarray) -> dict:
    """Recompute the accepted FINAL-RAW F0 rates exactly as the source does
    (``boundary_hjb_selected_q.py`` lines 962-976: raw drift recompute via
    ``asset_drifts_matlab_faithful`` then ``max(+-mu)/step``) and verify they
    reproduce the accepted ``final=True`` build's recorded row within
    ``REPRO_TOL``.

    Additionally reconstructs the MATLAB-faithful post-convergence row for the
    SAME rates and controls (destinations placed WITHIN the z-block,
    ``col = nz * self.n + dn``, matching ``matlab_faithful_two_asset_ha.py``
    line 562 + ``assemble_source_axis`` lines 425-451) and measures the
    accepted-row vs MATLAB-faithful-row assembly deviation per F0 row.
    """
    cfg = solver.config
    g = solver.grid
    n, nz = solver.n, solver.nz
    out = {
        "b_backward": np.zeros(len(f0_rows)),
        "b_forward": np.zeros(len(f0_rows)),
        "a_backward": np.zeros(len(f0_rows)),
        "a_forward": np.zeros(len(f0_rows)),
        "diagonal": np.zeros(len(f0_rows)),
        "represented_outgoing_sum": np.zeros(len(f0_rows)),
        "omitted_destination_rate": np.zeros(len(f0_rows)),
        "utility": np.zeros(len(f0_rows)),
        "mu_a": np.zeros(len(f0_rows)),
        "mu_b": np.zeros(len(f0_rows)),
        "reproduced": np.zeros(len(f0_rows), dtype=bool),
        "repro_row_max": 0.0,
        "assembly_deviation": np.zeros(len(f0_rows)),
        "assembly_deviation_max": 0.0,
    }
    for k, r in enumerate(f0_rows):
        node, zz = int(r % n), int(r // n)
        j, i = int(g.j_arr[node]), int(g.i_arr[node])
        rec_f = records_final[r]
        mu_a_v, mu_b_v, _ = asset_drifts_matlab_faithful(
            float(g.a_arr[node]), float(g.b_arr[node]), float(cfg.z[zz]),
            rec_f.consumption, np.array([rec_f.labor]), rec_f.transfer,
            cfg.inputs, cfg.params, cfg.a_max,
        )
        ab = max(-mu_a_v, 0.0) / solver.da
        af = max(mu_a_v, 0.0) / solver.da
        bb = max(-mu_b_v, 0.0) / solver.db
        bf = max(mu_b_v, 0.0) / solver.db
        neigh = g.neighbors(j, i)
        entries: list[tuple[int, float]] = []
        for dn, rate in ((neigh["down"], bb), (neigh["up"], bf),
                         (neigh["left"], ab), (neigh["right"], af)):
            if dn is not None and rate != 0.0:
                entries.append((dn, float(rate)))
        diag = -(bb + bf + ab + af)
        rep_out = float(sum(rate for _, rate in entries))
        omitted = -diag - rep_out
        out["b_backward"][k] = bb
        out["b_forward"][k] = bf
        out["a_backward"][k] = ab
        out["a_forward"][k] = af
        out["diagonal"][k] = diag
        out["represented_outgoing_sum"][k] = rep_out
        out["omitted_destination_rate"][k] = omitted
        out["utility"][k] = float(rec_f.utility)
        out["mu_a"][k] = mu_a_v
        out["mu_b"][k] = mu_b_v
        # reproduction vs the accepted final=True record
        rec_map = {dn0: rrate for dn0, rrate in rec_f.row_entries}
        devs = [abs(diag - rec_f.diagonal)]
        for dn0, rrate in rec_map.items():
            found = next((x for x in entries if x[0] == dn0), None)
            devs.append(abs((found[1] if found else 0.0) - rrate))
        for dn0, rrate in entries:
            if dn0 not in rec_map:
                devs.append(abs(rrate))
        row_dev = max(devs)
        out["repro_row_max"] = max(out["repro_row_max"], row_dev)
        out["reproduced"][k] = bool(row_dev <= REPRO_TOL)
        # accepted row (columns as the accepted code writes them: bare dn)
        # vs MATLAB-faithful post row (columns within the z-block: nz*n + dn)
        accepted = {(dn0, rrate) for dn0, rrate in rec_f.row_entries}
        faithful = {(zz * n + dn0, rrate) for dn0, rrate in entries}
        merged = sorted(set(c for c, _ in accepted) | set(c for c, _ in faithful))
        dev_asm = 0.0
        for c in merged:
            av = next((rrate for cc, rrate in accepted if cc == c), 0.0)
            fv = next((rrate for cc, rrate in faithful if cc == c), 0.0)
            dev_asm = max(dev_asm, abs(av - fv))
        out["assembly_deviation"][k] = dev_asm
        out["assembly_deviation_max"] = max(out["assembly_deviation_max"], dev_asm)
    return out


# ---------------------------------------------------------------------------
# 4c. Component-class decomposition of the ~24.60 operator gap
# ---------------------------------------------------------------------------
def f0_component_comparison(solver: BoundaryHJBSolver, two: dict,
                            iter_comp: dict, final_comp: dict) -> dict:
    """Per-F0-row component comparison and class-level decomposition of the
    rowwise operator gap into rate/operator component classes and the
    destination-assembly class."""
    n = solver.n
    f0_rows = two["f0_rows"]
    names = ("b_backward", "b_forward", "a_backward", "a_forward", "diagonal",
             "represented_outgoing_sum", "omitted_destination_rate", "utility")
    classes: dict[str, dict] = {}
    for name in names:
        d = np.abs(iter_comp[name] - final_comp[name])
        aff = int(np.sum(d > CLASS_TOL))
        if aff > 0:
            k = int(np.argmax(d))
        else:
            k = 0
        classes[name] = {
            "affected_row_count": aff,
            "max_abs_diff": float(np.max(d)),
            "argmax_state": (_state(int(f0_rows[k]), solver)
                             if aff > 0 else None),
        }
    # destination-assembly class: per-row rowwise operator gap (the accepted
    # rows differ in WHERE the same rates are placed for z=1 rows)
    d_asm = np.array([
        float(np.max(np.abs(
            np.asarray(two["Q_iter"].getrow(int(r)).toarray()).ravel()
            - np.asarray(two["Q_final_current"].getrow(int(r)).toarray()).ravel())))
        for r in f0_rows])
    aff_asm = int(np.sum(d_asm > CLASS_TOL))
    k_asm = int(np.argmax(d_asm)) if aff_asm > 0 else 0
    classes["destination_assembly_gap"] = {
        "affected_row_count": aff_asm,
        "max_abs_diff": float(np.max(d_asm)),
        "argmax_state": (_state(int(f0_rows[k_asm]), solver)
                         if aff_asm > 0 else None),
    }
    # max total row-entry difference (rowwise) and its column attribution
    r0 = int(two["f0_rowwise_max_abs_gap_row"])
    node, zz = r0 % n, r0 // n
    g = solver.grid
    j, i = int(g.j_arr[node]), int(g.i_arr[node])
    neigh = g.neighbors(j, i)
    va = np.asarray(two["Q_iter"].getrow(r0).toarray()).ravel()
    vb = np.asarray(two["Q_final_current"].getrow(r0).toarray()).ravel()
    d = np.abs(va - vb)
    col = int(np.argmax(d))
    # both placement variants of each destination direction: the accepted
    # MATLAB-faithful within-z-block column (nz*n + dn, used by the ITER path
    # and the oracle) and the accepted final=True bare-node column (dn)
    dir_cols = {
        "b_backward": (zz * n + neigh.get("down"), neigh.get("down")),
        "b_forward": (zz * n + neigh.get("up"), neigh.get("up")),
        "a_backward": (zz * n + neigh.get("left"), neigh.get("left")),
        "a_forward": (zz * n + neigh.get("right"), neigh.get("right")),
    }
    if col == r0:
        comp = "diagonal"
    else:
        comp = next((nm for nm, cols in dir_cols.items() if col in cols),
                    "switch_matrix_or_other")
    row_comps: dict[str, float] = {"b_backward": 0.0, "b_forward": 0.0,
                                   "a_backward": 0.0, "a_forward": 0.0,
                                   "diagonal": 0.0, "switch_matrix_or_other": 0.0}
    for nm, cols in dir_cols.items():
        for c in cols:
            if c is not None:
                row_comps[nm] = max(row_comps[nm], float(d[c]))
    row_comps["diagonal"] = float(d[r0])
    top = max(row_comps.values())
    row_comps["switch_matrix_or_other"] = float(np.max(d)) - top
    # accepted-final-row vs MATLAB-faithful-post-row assembly deviation
    asm_dev = final_comp["assembly_deviation"]
    aff_dev = int(np.sum(asm_dev > CLASS_TOL))
    k_dev = int(np.argmax(asm_dev)) if aff_dev > 0 else 0
    return {
        "f0_row_count": int(len(f0_rows)),
        "classes": classes,
        "destination_assembly_max_abs_diff": float(np.max(asm_dev)),
        "destination_assembly_affected_row_count": aff_dev,
        "destination_assembly_argmax_state": (_state(int(f0_rows[k_dev]), solver)
                                              if aff_dev > 0 else None),
        "max_total_row_entry_diff": float(np.max(d)),
        "max_total_row_entry_diff_state": _state(r0, solver),
        "max_row_argmax_component": comp,
        "max_row_component_contributions": row_comps,
        "max_row_columns_with_diff": int(np.sum(d > CLASS_TOL)),
    }


# ---------------------------------------------------------------------------
# 5. Source-backed MATLAB/oracle provenance mapping (deterministic)
# ---------------------------------------------------------------------------
def provenance_mapping() -> dict:
    """Deterministic read-only source-backed provenance mapping with exact
    source references (never a re-interpretation or rewrite of source
    semantics)."""
    return {
        "iter_f0_row": {
            "selected_q": "boundary_hjb_selected_q.py:484-521 (local_interior_row)",
            "oracle": "matlab_faithful_two_asset_ha.py:193-416 (select_matlab_faithful_local_policy)",
            "b_rates": "iteration_b_backward_rate / iteration_b_forward_rate = -(sc_b*1[B]+sdh_b*1[B_t])/db and (sc_f*1[F]+sdh_f*1[F_t])/db (lines 408-415)",
            "a_rates": "a_backward_rate = -min(shadow_transfer_b,0)/da; a_forward_rate = (max(shadow_transfer_f,0)+effective_return*a)/da (lines 372-377, 406-407)",
            "controls": "consumption/labor from the liquid FOC branch (lines 270-300); transfer from the shadow-transfer FOC (lines 302-370)",
            "mu": "asset_drifts_matlab_faithful at consumption-transfer_income (lines 379-389; transfer_income=0 here)",
            "iteration_operator_assembly": "matlab_faithful_two_asset_ha.py:553-555 + assemble_source_operator 453-464 (iteration sc/sdh + mh rates)",
            "destination_columns": "boundary_hjb_selected_q.py:1008 cols.append(nz*self.n+dn) — within-z-block, matches oracle assemble_source_axis layout",
        },
        "final_raw_f0_row": {
            "selected_q": "boundary_hjb_selected_q.py:957-994 (final=True F0 row)",
            "mu": "asset_drifts_matlab_faithful(a,b,z,rec.consumption,[rec.labor],rec.transfer,...) (lines 962-965)",
            "rates": "max(-mu_b,0)/db, max(mu_b,0)/db, max(-mu_a,0)/da, max(mu_a,0)/da (lines 966-969) — EXACT oracle post-convergence formula (matlab_faithful_two_asset_ha.py:562)",
            "diagonal": "-(bb+bf+ab+af) (line 976)",
            "destination_columns": "boundary_hjb_selected_q.py:978 cols.append(dn) — BARE node index, NO z-block offset; the oracle assembly (assemble_source_axis 425-451) places destinations within the z-block, so for z=1 F0 rows the accepted final=True off-diagonal entries point at z=0-block columns",
            "assembly_consequence": "accepted FINAL-RAW ROW is not the MATLAB-faithful discrete HJB row (destination placement deviates for z=1 rows) even though its rate formulas are the accepted oracle post-convergence formulas",
        },
        "destination_truncation": {
            "convention": "drop off-diagonal entry when destination is unavailable; retain the rate on the diagonal",
            "oracle": "matlab_faithful_two_asset_ha.py:425-451 (assemble_source_axis), 428 'truncating outward entries but not their diagonal'",
            "selected_q_iter": "boundary_hjb_selected_q.py:512-520 (entries only when neighbor exists; diagonal keeps all four rates)",
            "selected_q_final": "boundary_hjb_selected_q.py:970-979 (same convention)",
        },
        "derivatives": {
            "selected_q": "boundary_hjb_selected_q.py:432-481 (compute_derivatives; b_min marginal formula 462-468; i==i_t[j] top-row convention 479-480)",
            "oracle": "matlab_faithful_two_asset_ha.py:532-542",
        },
        "switch_matrix": {
            "selected_q": "boundary_hjb_selected_q.py:1034-1036 (Q + B kron(switch_matrix, I_n))",
            "oracle": "matlab_faithful_two_asset_ha.py:463 (bswitch kron) — identical contribution on both operators",
        },
        "measured_identity": ("On all 596 F0 rows at V_* the accepted iteration "
                              "b-rates coincide with max(+-mu_b)/db (the sc/sdh "
                              "shadow flow sums to the raw drift) and the "
                              "iteration a-rates coincide with max(+-mu_a)/da "
                              "(transfer branch 0 and mu_a = r_eff*a >= 0), so the "
                              "rate-component classes show ~0 differences and the "
                              "~24.60 operator gap decomposes into "
                              "destination-assembly placement (z-block offset "
                              "dropped in the accepted final=True F0 row) — not "
                              "into rate formulas."),
        "note": ("The accepted oracle itself defines TWO distinct MATLAB-faithful "
                 "discrete operators: the iteration operator (sc/sdh + mh rates, "
                 "lines 553-555) and the post-convergence operator (max(+-mu)/step, "
                 "line 562). The selected-Q ITER F0 row is the former (rates AND "
                 "assembly reproduced). The selected-Q final=True F0 row uses the "
                 "latter's RATE formulas but assembles z=1 destinations at z=0-block "
                 "columns, so the accepted FINAL-RAW ROW is not the MATLAB-faithful "
                 "discrete HJB construction."),
    }


# ---------------------------------------------------------------------------
# 6. Frozen classifications and exactly one terminal
# ---------------------------------------------------------------------------
def classify_and_terminal(two: dict, iter_comp: dict, final_comp: dict) -> dict:
    """Frozen ex ante classifications and exactly ONE terminal (Issue #66)."""
    f0_rows = two["f0_rows"]
    # rate/row reproduction
    iter_eq = bool(np.all(iter_comp["reproduced"]))
    final_repro = bool(np.all(final_comp["reproduced"]))
    # source-backed MATLAB-faithful ROW: rates are the oracle post-convergence
    # formula AND the assembled row matches the MATLAB-faithful within-z-block
    # destination layout within tolerance
    final_asm_max = float(np.max(final_comp["assembly_deviation"]))
    final_eq = bool(final_repro and final_asm_max <= REPRO_TOL)
    both_eq = bool(two["f0_rowwise_max_abs_gap"] <= ROW_EQ_TOL)
    if not (np.all(np.isfinite(iter_comp["b_backward"]))
            and np.all(np.isfinite(final_comp["b_backward"]))
            and np.all(np.isfinite(iter_comp["diagonal"]))
            and np.all(np.isfinite(final_comp["diagonal"]))):
        raise F0FinalRateProvenanceFailure("non-finite F0 rate component evidence")
    if not np.isfinite(two["f0_rowwise_max_abs_gap"]) \
            or not np.isfinite(final_asm_max):
        raise F0FinalRateProvenanceFailure("non-finite operator-gap evidence")
    if iter_eq and not final_eq and not both_eq \
            and two["f0_rowwise_max_abs_gap"] > MATERIAL_GAP_TOL:
        outcome = TERMINAL_A
    elif final_eq and not iter_eq:
        outcome = TERMINAL_B
    else:
        # both-eq / dual-provenance / unresolved / neither uniquely established
        outcome = TERMINAL_C
    return {
        "iter_eq_matlab": bool(iter_eq),
        "final_eq_matlab": bool(final_eq),
        "final_eq_rate_formula": bool(final_repro),
        "final_eq_assembly": bool(final_asm_max <= REPRO_TOL),
        "both_equivalent": bool(both_eq),
        "mixed_or_unresolved": False,
        "materially_non_equivalent": bool(
            two["f0_rowwise_max_abs_gap"] > MATERIAL_GAP_TOL),
        "outcome": outcome,
        "f0_row_count": int(len(f0_rows)),
    }


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------
@dataclass
class F0FinalRateProvenanceResult:
    outcome: str
    # reconstruction
    iterations: int
    trace: list[dict]
    v0_min_boundary_pb: float
    min_accepted_boundary_pb: float
    final_statistic: Optional[float]
    min_boundary_pb_star: float
    wall_state: Optional[dict]
    # reproductions
    r_iter_inf: Optional[float]
    r_iter_argmax: Optional[dict]
    r_iter_f0_max: Optional[float]
    r_iter_boundary_max: Optional[float]
    r_final_current_inf: Optional[float]
    r_final_current_argmax: Optional[dict]
    r_final_current_f0_max: Optional[float]
    r_final_current_boundary_max: Optional[float]
    f0_rowwise_max_abs_gap: Optional[float]
    f0_rowwise_max_abs_gap_state: Optional[dict]
    same_controls_max_abs_diff: Optional[float]
    boundary_row_max_abs_diff: Optional[float]
    boundary_u_max_abs_diff: Optional[float]
    utility_f0_max_abs_diff: Optional[float]
    # operator diagnostics
    max_abs_q1_iter: Optional[float]
    max_abs_q1_final_current: Optional[float]
    expansions_iter: Optional[int]
    bindings_iter: Optional[int]
    expansions_final_current: Optional[int]
    bindings_final_current: Optional[int]
    # component comparison
    f0_row_count: Optional[int]
    class_b_backward: Optional[dict]
    class_b_forward: Optional[dict]
    class_a_backward: Optional[dict]
    class_a_forward: Optional[dict]
    class_diagonal: Optional[dict]
    class_represented_outgoing_sum: Optional[dict]
    class_omitted_destination_rate: Optional[dict]
    class_utility: Optional[dict]
    class_destination_assembly_gap: Optional[dict]
    destination_assembly_max_abs_diff: Optional[float]
    destination_assembly_affected_row_count: Optional[int]
    destination_assembly_argmax_state: Optional[dict]
    max_total_row_entry_diff: Optional[float]
    max_total_row_entry_diff_state: Optional[dict]
    max_row_argmax_component: Optional[str]
    max_row_component_contributions: Optional[dict]
    max_row_columns_with_diff: Optional[int]
    iter_repro_controls_max: Optional[float]
    iter_repro_row_max: Optional[float]
    final_repro_row_max: Optional[float]
    # classifications / provenance
    iter_eq_matlab: bool = False
    final_eq_matlab: bool = False
    final_eq_rate_formula: bool = False
    final_eq_assembly: bool = False
    both_equivalent: bool = False
    mixed_or_unresolved: bool = False
    materially_non_equivalent: bool = False
    provenance_note: str = ""
    # per-row arrays (diagnostic tests only; excluded from CSV and canon)
    f0_rows_array: Optional[np.ndarray] = None
    iter_components: Optional[dict] = None
    final_components: Optional[dict] = None
    # determinism
    deterministic_repeat_identical: bool = False
    failure_detail: Optional[dict] = None

    def to_summary_csv_lines(self) -> list[str]:
        def st(d: Optional[dict]) -> str:
            if d is None:
                return ""
            return (f"node={d.get('node')},j={d.get('j')},i={d.get('i')},"
                    f"z={d.get('z')},family={d.get('family')}")

        def f(x) -> str:
            return "" if x is None else f"{x:.12g}"

        def cls(c: Optional[dict]) -> str:
            if c is None:
                return ""
            return (f"affected={c.get('affected_row_count')},"
                    f"max_abs={f(c.get('max_abs_diff'))},"
                    f"argmax={st(c.get('argmax_state'))}")

        rows: list[tuple[str, str]] = [
            ("outcome", self.outcome),
            ("reconstruction.iterations", str(self.iterations)),
            ("reconstruction.v0_min_boundary_pb", f(self.v0_min_boundary_pb)),
            ("reconstruction.min_accepted_boundary_pb", f(self.min_accepted_boundary_pb)),
            ("reconstruction.final_statistic", f(self.final_statistic)),
            ("reconstruction.min_boundary_pb_star", f(self.min_boundary_pb_star)),
            ("reconstruction.wall_state", st(self.wall_state)),
            ("reproduce.r_iter_inf", f(self.r_iter_inf)),
            ("reproduce.r_iter_argmax", st(self.r_iter_argmax)),
            ("reproduce.r_iter_f0_max", f(self.r_iter_f0_max)),
            ("reproduce.r_iter_boundary_max", f(self.r_iter_boundary_max)),
            ("reproduce.r_final_current_inf", f(self.r_final_current_inf)),
            ("reproduce.r_final_current_argmax", st(self.r_final_current_argmax)),
            ("reproduce.r_final_current_f0_max", f(self.r_final_current_f0_max)),
            ("reproduce.r_final_current_boundary_max", f(self.r_final_current_boundary_max)),
            ("reproduce.f0_rowwise_max_abs_gap", f(self.f0_rowwise_max_abs_gap)),
            ("reproduce.f0_rowwise_max_abs_gap_state", st(self.f0_rowwise_max_abs_gap_state)),
            ("reproduce.same_controls_max_abs_diff", f(self.same_controls_max_abs_diff)),
            ("reproduce.boundary_row_max_abs_diff", f(self.boundary_row_max_abs_diff)),
            ("reproduce.boundary_u_max_abs_diff", f(self.boundary_u_max_abs_diff)),
            ("reproduce.utility_f0_max_abs_diff", f(self.utility_f0_max_abs_diff)),
            ("operator.max_abs_q1_iter", f(self.max_abs_q1_iter)),
            ("operator.max_abs_q1_final_current", f(self.max_abs_q1_final_current)),
            ("operator.expansions_iter", str(self.expansions_iter)),
            ("operator.bindings_iter", str(self.bindings_iter)),
            ("operator.expansions_final_current", str(self.expansions_final_current)),
            ("operator.bindings_final_current", str(self.bindings_final_current)),
            ("components.f0_row_count", str(self.f0_row_count)),
            ("components.class_b_backward", cls(self.class_b_backward)),
            ("components.class_b_forward", cls(self.class_b_forward)),
            ("components.class_a_backward", cls(self.class_a_backward)),
            ("components.class_a_forward", cls(self.class_a_forward)),
            ("components.class_diagonal", cls(self.class_diagonal)),
            ("components.class_represented_outgoing_sum", cls(self.class_represented_outgoing_sum)),
            ("components.class_omitted_destination_rate", cls(self.class_omitted_destination_rate)),
            ("components.class_utility", cls(self.class_utility)),
            ("components.class_destination_assembly_gap", cls(self.class_destination_assembly_gap)),
            ("components.destination_assembly_max_abs_diff", f(self.destination_assembly_max_abs_diff)),
            ("components.destination_assembly_affected_row_count", str(self.destination_assembly_affected_row_count)),
            ("components.destination_assembly_argmax_state", st(self.destination_assembly_argmax_state)),
            ("components.max_total_row_entry_diff", f(self.max_total_row_entry_diff)),
            ("components.max_total_row_entry_diff_state", st(self.max_total_row_entry_diff_state)),
            ("components.max_row_argmax_component", str(self.max_row_argmax_component)),
            ("components.max_row_component_contributions",
             ",".join(f"{k}={f(v)}" for k, v in (self.max_row_component_contributions or {}).items())),
            ("components.max_row_columns_with_diff", str(self.max_row_columns_with_diff)),
            ("repro.iter_repro_controls_max", f(self.iter_repro_controls_max)),
            ("repro.iter_repro_row_max", f(self.iter_repro_row_max)),
            ("repro.final_repro_row_max", f(self.final_repro_row_max)),
            ("classification.iter_eq_matlab", str(self.iter_eq_matlab).lower()),
            ("classification.final_eq_matlab", str(self.final_eq_matlab).lower()),
            ("classification.final_eq_rate_formula", str(self.final_eq_rate_formula).lower()),
            ("classification.final_eq_assembly", str(self.final_eq_assembly).lower()),
            ("classification.both_equivalent", str(self.both_equivalent).lower()),
            ("classification.mixed_or_unresolved", str(self.mixed_or_unresolved).lower()),
            ("classification.materially_non_equivalent", str(self.materially_non_equivalent).lower()),
            ("deterministic_repeat_identical", str(self.deterministic_repeat_identical).lower()),
        ]
        return [",".join([k, v]) for (k, v) in rows]


def run_issue66_audit() -> F0FinalRateProvenanceResult:
    """Exactly one full Issue #66 audit: ONE deterministic reconstruction; ONE
    current-policy ``final=False`` build; ONE current-policy ``final=True``
    build at the same ``V_*`` with the same controls; ONE all-F0 compact
    component comparison; ONE read-only source-backed provenance mapping; ONE
    deterministic repeat (in ``run_issue66_audit_twice``)."""
    rec = reconstruct_issue63_stagnation_state()
    return _audit_from_reconstruction(rec)


def _audit_from_reconstruction(rec: dict) -> F0FinalRateProvenanceResult:
    """Analysis half of the audit at an already-reconstructed accepted state."""
    failure_detail: Optional[dict] = None
    try:
        solver: BoundaryHJBSolver = rec["solver"]
        labor0: np.ndarray = rec["labor0"]
        V_star: np.ndarray = rec["V_star"]
        rho: float = rec["rho"]
        trace: list = rec["trace"]
        wall_pb, wall_node, wall_nz = min_boundary_pb_state(solver, V_star, labor0)
        if not np.isfinite(wall_pb):
            raise F0FinalRateProvenanceFailure("non-finite required boundary p_b at V_*")

        two = build_two_operators(solver, V_star, labor0, rho)
        f0_rows = two["f0_rows"]
        iter_comp = iter_f0_components(
            solver, V_star, labor0, two["records_current"], f0_rows)
        final_comp = final_raw_f0_components(
            solver, two["records_final"], f0_rows)
        comp = f0_component_comparison(solver, two, iter_comp, final_comp)
        classif = classify_and_terminal(two, iter_comp, final_comp)

        s_iter = two["stats_iter"]
        s_fin = two["stats_final_current"]
        utility_f0_max = float(np.max(np.abs(
            two["u_iter"][f0_rows] - two["u_final_current"][f0_rows])))
        prov = provenance_mapping()

        return F0FinalRateProvenanceResult(
            outcome=classif["outcome"], iterations=RECONSTRUCT_STEPS, trace=trace,
            v0_min_boundary_pb=float(rec["v0_min_boundary_pb"]),
            min_accepted_boundary_pb=float(rec["min_accepted_boundary_pb"]),
            final_statistic=float(trace[-1]["accepted_max_stat"]),
            min_boundary_pb_star=float(wall_pb),
            wall_state=_state_info(solver, wall_node, wall_nz),
            r_iter_inf=s_iter["total"]["max_abs"],
            r_iter_argmax=s_iter["total"]["argmax_state"],
            r_iter_f0_max=s_iter["f0"]["max_abs"],
            r_iter_boundary_max=s_iter["boundary"]["max_abs"],
            r_final_current_inf=s_fin["total"]["max_abs"],
            r_final_current_argmax=s_fin["total"]["argmax_state"],
            r_final_current_f0_max=s_fin["f0"]["max_abs"],
            r_final_current_boundary_max=s_fin["boundary"]["max_abs"],
            f0_rowwise_max_abs_gap=two["f0_rowwise_max_abs_gap"],
            f0_rowwise_max_abs_gap_state=_state(
                int(two["f0_rowwise_max_abs_gap_row"]), solver),
            same_controls_max_abs_diff=two["same_controls_max_abs_diff"],
            boundary_row_max_abs_diff=two["boundary_row_max_abs_diff"],
            boundary_u_max_abs_diff=two["boundary_u_max_abs_diff"],
            utility_f0_max_abs_diff=utility_f0_max,
            max_abs_q1_iter=two["max_abs_q1_iter"],
            max_abs_q1_final_current=two["max_abs_q1_final_current"],
            expansions_iter=two["expansions_iter"],
            bindings_iter=two["bindings_iter"],
            expansions_final_current=two["expansions_final_current"],
            bindings_final_current=two["bindings_final_current"],
            f0_row_count=comp["f0_row_count"],
            class_b_backward=comp["classes"]["b_backward"],
            class_b_forward=comp["classes"]["b_forward"],
            class_a_backward=comp["classes"]["a_backward"],
            class_a_forward=comp["classes"]["a_forward"],
            class_diagonal=comp["classes"]["diagonal"],
            class_represented_outgoing_sum=comp["classes"]["represented_outgoing_sum"],
            class_omitted_destination_rate=comp["classes"]["omitted_destination_rate"],
            class_utility=comp["classes"]["utility"],
            class_destination_assembly_gap=comp["classes"]["destination_assembly_gap"],
            destination_assembly_max_abs_diff=comp["destination_assembly_max_abs_diff"],
            destination_assembly_affected_row_count=comp["destination_assembly_affected_row_count"],
            destination_assembly_argmax_state=comp["destination_assembly_argmax_state"],
            max_total_row_entry_diff=comp["max_total_row_entry_diff"],
            max_total_row_entry_diff_state=comp["max_total_row_entry_diff_state"],
            max_row_argmax_component=comp["max_row_argmax_component"],
            max_row_component_contributions=comp["max_row_component_contributions"],
            max_row_columns_with_diff=comp["max_row_columns_with_diff"],
            iter_repro_controls_max=float(np.max(iter_comp["repro_controls_max"])),
            iter_repro_row_max=float(np.max(iter_comp["repro_row_max"])),
            final_repro_row_max=float(np.max(final_comp["repro_row_max"])),
            iter_eq_matlab=classif["iter_eq_matlab"],
            final_eq_matlab=classif["final_eq_matlab"],
            final_eq_rate_formula=classif["final_eq_rate_formula"],
            final_eq_assembly=classif["final_eq_assembly"],
            both_equivalent=classif["both_equivalent"],
            mixed_or_unresolved=classif["mixed_or_unresolved"],
            materially_non_equivalent=classif["materially_non_equivalent"],
            provenance_note=prov["note"],
            f0_rows_array=f0_rows.astype(np.int64),
            iter_components={k: v for k, v in iter_comp.items()
                             if isinstance(v, np.ndarray)},
            final_components={k: v for k, v in final_comp.items()
                              if isinstance(v, np.ndarray)},
        )
    except (F0FinalRateProvenanceFailure, FTBStepConstructionFailure,
            BoundaryHJBFailure, ValueError) as exc:
        failure_detail = {"message": str(exc)}
        return F0FinalRateProvenanceResult(
            outcome=TERMINAL_C, iterations=0, trace=[], v0_min_boundary_pb=0.0,
            min_accepted_boundary_pb=0.0, final_statistic=None,
            min_boundary_pb_star=0.0, wall_state=None,
            r_iter_inf=None, r_iter_argmax=None, r_iter_f0_max=None,
            r_iter_boundary_max=None, r_final_current_inf=None,
            r_final_current_argmax=None, r_final_current_f0_max=None,
            r_final_current_boundary_max=None, f0_rowwise_max_abs_gap=None,
            f0_rowwise_max_abs_gap_state=None, same_controls_max_abs_diff=None,
            boundary_row_max_abs_diff=None, boundary_u_max_abs_diff=None,
            utility_f0_max_abs_diff=None, max_abs_q1_iter=None,
            max_abs_q1_final_current=None, expansions_iter=None,
            bindings_iter=None, expansions_final_current=None,
            bindings_final_current=None, f0_row_count=None,
            class_b_backward=None, class_b_forward=None, class_a_backward=None,
            class_a_forward=None, class_diagonal=None,
            class_represented_outgoing_sum=None,
            class_omitted_destination_rate=None, class_utility=None,
            class_destination_assembly_gap=None,
            destination_assembly_max_abs_diff=None,
            destination_assembly_affected_row_count=None,
            destination_assembly_argmax_state=None,
            max_total_row_entry_diff=None, max_total_row_entry_diff_state=None,
            max_row_argmax_component=None, max_row_component_contributions=None,
            max_row_columns_with_diff=None, iter_repro_controls_max=None,
            iter_repro_row_max=None, final_repro_row_max=None,
            failure_detail=failure_detail,
        )


def _canon(r: F0FinalRateProvenanceResult):
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
        c(r.r_iter_boundary_max), c(r.r_final_current_inf),
        c(r.r_final_current_argmax), c(r.r_final_current_f0_max),
        c(r.r_final_current_boundary_max), c(r.f0_rowwise_max_abs_gap),
        c(r.f0_rowwise_max_abs_gap_state), c(r.same_controls_max_abs_diff),
        c(r.boundary_row_max_abs_diff), c(r.boundary_u_max_abs_diff),
        c(r.utility_f0_max_abs_diff), c(r.max_abs_q1_iter),
        c(r.max_abs_q1_final_current), c(r.expansions_iter),
        c(r.bindings_iter), c(r.expansions_final_current),
        c(r.bindings_final_current), c(r.f0_row_count),
        c(r.class_b_backward), c(r.class_b_forward), c(r.class_a_backward),
        c(r.class_a_forward), c(r.class_diagonal),
        c(r.class_represented_outgoing_sum),
        c(r.class_omitted_destination_rate), c(r.class_utility),
        c(r.class_destination_assembly_gap),
        c(r.destination_assembly_max_abs_diff),
        c(r.destination_assembly_affected_row_count),
        c(r.destination_assembly_argmax_state),
        c(r.max_total_row_entry_diff), c(r.max_total_row_entry_diff_state),
        c(r.max_row_argmax_component), c(r.max_row_component_contributions),
        c(r.max_row_columns_with_diff), c(r.iter_repro_controls_max),
        c(r.iter_repro_row_max), c(r.final_repro_row_max),
        c(r.iter_eq_matlab), c(r.final_eq_matlab),
        c(r.final_eq_rate_formula), c(r.final_eq_assembly),
        c(r.both_equivalent), c(r.mixed_or_unresolved),
        c(r.materially_non_equivalent), c(r.provenance_note),
    )


def run_issue66_audit_twice() -> tuple[F0FinalRateProvenanceResult, bool]:
    """One full audit + one deterministic repeat (bit-identical);
    returns (result, repeat_identical)."""
    r1 = run_issue66_audit()
    r2 = run_issue66_audit()
    identical = bool(_canon(r1) == _canon(r2))
    return (
        dataclasses.replace(
            r1, outcome=r1.outcome,
            deterministic_repeat_identical=identical),
        identical,
    )
