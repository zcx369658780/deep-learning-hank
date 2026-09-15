"""DLH-5V-U — latent F0 iteration-rate vs raw-drift sign divergence away from `V_*`.

Issue #69 / DLH-5V-U
``SCIENTIFIC_NUMERICAL_DIAGNOSTIC__F0_ITERATION_RATE_VS_RAW_DRIFT_SIGN_PROVENANCE_AWAY_FROM_VSTAR``

Authority: Issue #69 OPEN; initial authoritative activation ``5676828795``;
final authoritative activation-refresh ``5677087565`` (post-sync live ``main``
``510bde97e60c1fb7f2cb5afb5bee18da18ca561f``). Route decision
``APPROVE_F0_ITERATION_RATE_VS_RAW_DRIFT_SIGN_PROVENANCE_AUDIT_AFTER_5VT_TERMINAL_C``;
authority marker ``DLH_5VU_F0_RATE_PATH_DIVERGENCE_AUDIT_AUTHORIZED``.

Scientific question
-------------------
Issue #68 exposed that, at its two accepted full-gradient trial states, the
re-selected ``final=False`` operator (``Q_iter``) and the corrected
``final=True`` operator (``Q_final``) are **not** equivalent under the SAME
freshly reselected F0 controls, while at the accepted ``V_*`` they agree to
machine precision. This audit determines the exact source/provenance mechanism
of that latent divergence.

Frozen scope (diagnostic / provenance ONLY):

- exactly the two accepted Issue #68 trial states
  ``alpha_half = 0.08085341880193442`` and
  ``alpha_near = 0.16170683760386884``; no third trial;
- at each trial: exactly ONE ``final=False`` nonlinear policy re-selection and
  exactly ONE corrected ``final=True`` same-control build;
- ONE all-F0 compact rate/row decomposition per trial;
- ONE read-only source-provenance mapping;
- ONE deterministic repeat.

This Issue does **NOT** choose or replace the authoritative rate path, does
**not** accept an HJB iterate, does **not** construct any new Newton / tangent /
constrained direction, and does not mutate any accepted source.

Source-backed mechanism (see ``provenance_mapping``)
---------------------------------------------------
The two paths are **not** algebraically equivalent.

- **Iteration b-rates** (``boundary_hjb_selected_q.local_interior_row``) come
  from the accepted MATLAB-faithful local-policy object
  (``matlab_faithful_two_asset_ha.select_matlab_faithful_local_policy`` lines
  408-415)::

      iteration_b_backward_rate = -(sc_b if use_liquid_b else 0)
                                  - (sdh_b if use_transfer_b else 0)) / db
      iteration_b_forward_rate  = +(sc_f if use_liquid_f else 0)
                                  + (sdh_f if use_transfer_f else 0)) / db

  with ``sc_b/sc_f`` the LIQUID first-order-condition residuals
  (``liquid_resources_b/f - consumption_b/f``) and ``sdh_b/sdh_f`` the TRANSFER
  branch objects ``-d_b/-d_f`` net of adjustment cost. These are branch-gated
  **FOC/shadow objects**, not the realized drift.
- **Corrected final b-rates** (``build_operator_and_u`` ``final=True`` branch,
  lines 962-976) re-call ``asset_drifts_matlab_faithful`` with the SAME controls
  and map the realized drift through the upwind rule
  ``max(-mu_b,0)/db`` / ``max(mu_b,0)/db``.
- On the affected rows the liquid branch is BINDING (``liquid_label = "F"``),
  so ``sc_f`` contributes a **positive** ``iteration_b_forward_rate`` even
  though the realized ``mu_b`` is **negative** (backward). The iteration path
  therefore places a spurious forward destination, and its backward rate is
  correspondingly larger than the raw upwind rate. The **a-axis rates agree
  exactly** in every affected row.

The classification is therefore a unique source-backed
**sign / branch** mechanism, and it fully accounts for every observed rowwise
operator gap (verified: the summed off-diagonal rate difference equals the
diagonal difference to machine precision on every affected row, with zero
unexplained remainder).
"""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field
from typing import Optional

import numpy as np
from scipy import sparse
from scipy.sparse import linalg

from deep_learning_hank.two_asset.boundary_hjb_selected_q import (
    BoundaryHJBSolver,
)
from deep_learning_hank.two_asset.matlab_faithful_two_asset_ha import (
    asset_drifts_matlab_faithful,
    select_matlab_faithful_local_policy,
)
from deep_learning_hank.two_asset.stagnation_newton_geometry import (
    reconstruct_issue63_stagnation_state,
)
from deep_learning_hank.two_asset.tangent_projected_newton_geometry import (
    limiting_wall_gradient,
    single_wall_tangent_projection,
)

# ---------------------------------------------------------------------------
# Frozen accepted references (Issue #68 acceptance)
# ---------------------------------------------------------------------------
SELECTED_Q_REPAIRED_BLOB = "556ccc214f03a1a22306cc4f5c7e9f7691bbf897"

ALPHA_HALF = 0.08085341880193442
ALPHA_NEAR = 0.16170683760386884
TRIAL_ORDER = ("alpha_half", "alpha_near")

EXPECTED_GAP_HALF = 0.6718037653783657
EXPECTED_ROWS_HALF = (452, 453)
EXPECTED_GAP_NEAR = 1.3379411925537439
EXPECTED_ROWS_NEAR = (452, 453, 482, 483)

REPAIRED_R_INF = 10.435094313164921
FINAL_STATISTIC_EXPECTED = 3.6614352438846254e-08
MIN_BOUNDARY_PB_EXPECTED = 4.8089461301970005e-09
WALL_NODE, WALL_NZ = 332, 1

REPRO_TOL = 1.0e-9
ROW_ZERO_TOL = 1.0e-12
DECOMP_TOL = 1.0e-12

# classification flags
ITER_RATE_PATH_SOURCE_BACKED = "ITER_RATE_PATH_SOURCE_BACKED"
FINAL_RAW_PATH_SOURCE_BACKED = "FINAL_RAW_PATH_SOURCE_BACKED"
RATE_FORMULAS_GLOBALLY_EQUIVALENT = "RATE_FORMULAS_GLOBALLY_EQUIVALENT"
SIGN_OR_BRANCH_DIVERGENCE_ESTABLISHED = "SIGN_OR_BRANCH_DIVERGENCE_ESTABLISHED"
TRUNCATION_OR_DESTINATION_DIVERGENCE_ESTABLISHED = (
    "TRUNCATION_OR_DESTINATION_DIVERGENCE_ESTABLISHED")
OTHER_MECHANISM_ESTABLISHED = "OTHER_MECHANISM_ESTABLISHED"
MIXED_OR_UNRESOLVED = "MIXED_OR_UNRESOLVED"

TERMINAL_A = (
    "DLH_5VU_F0_RATE_PATH_DIVERGENCE__UNIQUE_SIGN_OR_BRANCH_MECHANISM_"
    "ESTABLISHED_AND_FULLY_ACCOUNTS_FOR_TRIAL_OPERATOR_GAPS__RATE_SEMANTICS_"
    "SCIENTIFIC_REVIEW_GATE_READY")
TERMINAL_B = (
    "DLH_5VU_F0_RATE_PATH_DIVERGENCE__UNIQUE_TRUNCATION_OR_DESTINATION_"
    "MECHANISM_ESTABLISHED_AND_FULLY_ACCOUNTS_FOR_TRIAL_OPERATOR_GAPS__RATE_"
    "SEMANTICS_SCIENTIFIC_REVIEW_GATE_READY")
TERMINAL_C = (
    "DLH_5VU_F0_RATE_PATH_DIVERGENCE__MIXED_OR_UNRESOLVED_SOURCE_PROVENANCE__"
    "OWNER_SCIENTIFIC_REVIEW_REQUIRED")
TERMINAL_BLOCKED = "BLOCKED_DLH_5VU_AUTHORITY_OR_DEPENDENCY_CONFLICT"


class F0RatePathDivergenceFailure(RuntimeError):
    """Fail-closed: non-finite evidence, a failed reproduction of the accepted
    Issue #68 gaps/rows, a decomposition that does not close, or a
    non-deterministic repeat."""


# ---------------------------------------------------------------------------
# Result containers
# ---------------------------------------------------------------------------
@dataclass
class RowEvidence:
    """Compact per-row evidence for one inconsistent F0 row."""

    row: int
    node: int
    j: int
    i: int
    z: int
    family: str
    sector: str
    transfer_label: str
    consumption: float
    labor: float
    transfer: float
    utility: float
    stored_mu_a: float
    stored_mu_b: float
    raw_mu_a: float
    raw_mu_b: float
    iteration_b_backward_rate: float
    iteration_b_forward_rate: float
    iteration_a_backward_rate: float
    iteration_a_forward_rate: float
    raw_b_backward_rate: float
    raw_b_forward_rate: float
    raw_a_backward_rate: float
    raw_a_forward_rate: float
    iteration_active_b: str
    raw_active_b: str
    iteration_active_a: str
    raw_active_a: str
    iteration_opposite_direction_component: bool
    raw_opposite_direction_component: bool
    b_rate_divergent: bool
    a_rate_divergent: bool
    active_direction_divergent: bool
    iteration_diagonal: float
    final_diagonal: float
    diagonal_difference: float
    iteration_destinations: tuple
    final_destinations: tuple
    destination_layout_divergent: bool
    omitted_iteration_rate: float
    omitted_final_rate: float
    q_gap_nonzero_columns: tuple
    q_gap_column_magnitudes: tuple
    rowwise_max_gap: float
    summed_rate_difference: float
    decomposition_residual: float
    row_reproduction_ok: bool


@dataclass
class TrialAudit:
    """ONE frozen trial's all-F0 accounting plus its inconsistent-row evidence."""

    label: str
    alpha: float
    total_f0_rows: int
    rate_identical_row_count: int
    b_rate_divergent_row_count: int
    a_rate_divergent_row_count: int
    active_direction_divergent_row_count: int
    opposite_direction_component_row_count: int
    diagonal_divergent_row_count: int
    destination_layout_divergent_row_count: int
    omitted_rate_divergent_row_count: int
    q_row_divergent_row_count: int
    max_b_rate_difference: float
    max_a_rate_difference: float
    max_diagonal_difference: float
    max_rowwise_q_difference: float
    inconsistent_rows: tuple
    inconsistent_row_set_match: bool
    expected_gap: float
    expected_rows: tuple
    gap_reproduced: bool
    max_decomposition_residual: float
    decomposition_closed: bool
    all_rows_reproduced: bool
    same_controls_and_utility: bool
    rows: list = field(default_factory=list)


@dataclass
class DivergenceAuditResult:
    """ONE fully determined Issue #69 audit outcome."""

    terminal: str
    failure_detail: Optional[dict] = None
    # frozen reconstruction
    iterations: int = 0
    final_statistic: float = float("nan")
    min_boundary_pb_star: float = float("nan")
    wall_state: dict = field(default_factory=dict)
    r_inf: float = float("nan")
    tangent_identity_residual: float = float("nan")
    # provenance
    provenance: dict = field(default_factory=dict)
    # flags
    iter_rate_path_source_backed: bool = False
    final_raw_path_source_backed: bool = False
    rate_formulas_globally_equivalent: bool = False
    sign_or_branch_divergence_established: bool = False
    truncation_or_destination_divergence_established: bool = False
    other_mechanism_established: bool = False
    mixed_or_unresolved: bool = False
    # trials
    trial_count: int = 0
    trials: list = field(default_factory=list)
    a_axis_rates_identical_all_rows: bool = False
    accepted_new_hjb_iterate: bool = False
    deterministic_repeat_identical: bool = False


# ---------------------------------------------------------------------------
# one F0 row: stored vs raw rates
# ---------------------------------------------------------------------------
def _active_direction(signed: float, tol: float) -> str:
    """Frozen active-direction classification from the SIGNED axis quantity.

    Mirrors the accepted ``_direction`` helper in
    ``matlab_faithful_two_asset_ha.py``: ``F`` above ``+tol``, ``B`` below
    ``-tol``, else ``0``. Applied to the signed drift for the raw path and to
    the signed stored b-object (``iteration_b_forward_rate -
    iteration_b_backward_rate``) times the grid step for the iteration path, so
    that the comparison isolates the SIGN question and is not confounded by
    whether a zero rate happens to be stored.
    """
    if signed > tol:
        return "F"
    if signed < -tol:
        return "B"
    return "0"


def _opposite_component(rate_backward: float, rate_forward: float,
                        signed_raw: float, tol: float) -> bool:
    """True when a rate path stores a NON-ZERO component OPPOSING the realized
    drift direction.

    The corrected raw path can never do this: it stores
    ``max(+mu,0)/step`` and ``max(-mu,0)/step``, so at most one side is
    non-zero and it always points along ``sign(mu)``. The accepted iteration
    path sources its b-rates from branch-gated FOC shadow objects, so it CAN
    store both sides at once — a forward rate while the realized drift points
    backward (or the mirror case).
    """
    if signed_raw > tol:
        return bool(rate_backward != 0.0)
    if signed_raw < -tol:
        return bool(rate_forward != 0.0)
    return False


def _row_rates(solver: BoundaryHJBSolver, V_trial: np.ndarray,
               labor0: np.ndarray, row: int, record) -> dict:
    """Stored iteration rates and raw-drift rates for ONE F0 row at ONE trial.

    The stored iteration rates are obtained by RE-INVOKING the accepted
    MATLAB-faithful policy function read-only with the exact inputs
    ``local_interior_row`` used, and the re-invocation is verified to reproduce
    the solver's own re-selection row entries exactly (no inference from names).
    """
    n, nz = solver.n, solver.nz
    cfg = solver.config
    grid = solver.grid
    node, z = row % n, row // n
    j, i = int(grid.j_arr[node]), int(grid.i_arr[node])
    vbf, vbb, vaf, vab = solver.compute_derivatives(
        V_trial, labor0, 0.0, 0.0)
    pol = select_matlab_faithful_local_policy(
        a=float(grid.a_arr[node]), b=float(grid.b_arr[node]),
        z=float(cfg.z[z]),
        v_a_forward=float(vaf[node, z]), v_a_backward=float(vab[node, z]),
        v_b_forward=float(vbf[node, z]), v_b_backward=float(vbb[node, z]),
        baseline_labor=float(labor0[node, z]), transfer_income=0.0,
        borrowing_rate_gap=0.0, a_max=cfg.a_max, da=float(solver.da),
        db=float(solver.db), at_lower_a=(j == 0),
        at_upper_a=(j == grid.jmax), at_lower_b=(i == 0), at_upper_b=False,
        inputs=cfg.inputs, params=cfg.params,
        tolerance=cfg.drift_tolerance,
    )
    nb = grid.neighbors(j, i)
    reproduced_entries: dict[int, float] = {}
    for dn, rate in ((nb["down"], pol.iteration_b_backward_rate),
                     (nb["up"], pol.iteration_b_forward_rate),
                     (nb["left"], pol.a_backward_rate),
                     (nb["right"], pol.a_forward_rate)):
        if dn is not None and rate != 0.0:
            reproduced_entries[int(dn)] = float(rate)
    actual_entries = {int(dn): float(rt) for dn, rt in record.row_entries}
    reproduction_ok = reproduced_entries == actual_entries

    mu_a_raw, mu_b_raw, _cost = asset_drifts_matlab_faithful(
        float(grid.a_arr[node]), float(grid.b_arr[node]), float(cfg.z[z]),
        record.consumption, np.array([record.labor]), record.transfer,
        cfg.inputs, cfg.params, cfg.a_max,
    )
    da, db = float(solver.da), float(solver.db)
    raw_bb = max(-mu_b_raw, 0.0) / db
    raw_bf = max(mu_b_raw, 0.0) / db
    raw_ab = max(-mu_a_raw, 0.0) / da
    raw_af = max(mu_a_raw, 0.0) / da
    it_bb = float(pol.iteration_b_backward_rate)
    it_bf = float(pol.iteration_b_forward_rate)
    it_ab = float(pol.a_backward_rate)
    it_af = float(pol.a_forward_rate)

    return {
        "node": node, "j": j, "i": i, "z": z,
        "family": str(grid.families[node]),
        "sector": str(record.sector),
        "transfer_label": str(pol.transfer_label),
        "liquid_label": str(pol.liquid_label),
        "consumption": float(record.consumption),
        "labor": float(record.labor),
        "transfer": float(record.transfer),
        "utility": float(record.utility),
        "stored_mu_a": float(record.mu_a), "stored_mu_b": float(record.mu_b),
        "raw_mu_a": float(mu_a_raw), "raw_mu_b": float(mu_b_raw),
        "it_bb": it_bb, "it_bf": it_bf, "it_ab": it_ab, "it_af": it_af,
        "raw_bb": float(raw_bb), "raw_bf": float(raw_bf),
        "raw_ab": float(raw_ab), "raw_af": float(raw_af),
        "iteration_active_b": _active_direction(
            (it_bf - it_bb) * db, cfg.drift_tolerance),
        "raw_active_b": _active_direction(mu_b_raw, cfg.drift_tolerance),
        "iteration_active_a": _active_direction(
            (it_af - it_ab) * da, cfg.drift_tolerance),
        "raw_active_a": _active_direction(mu_a_raw, cfg.drift_tolerance),
        "iteration_opposite_b_component": _opposite_component(
            it_bb, it_bf, float(mu_b_raw), cfg.drift_tolerance),
        "raw_opposite_b_component": _opposite_component(
            raw_bb, raw_bf, float(mu_b_raw), cfg.drift_tolerance),
        "iteration_opposite_a_component": _opposite_component(
            it_ab, it_af, float(mu_a_raw), cfg.drift_tolerance),
        "raw_opposite_a_component": _opposite_component(
            raw_ab, raw_af, float(mu_a_raw), cfg.drift_tolerance),
        "row_reproduction_ok": bool(reproduction_ok),
        "neighbours": {k: (None if v is None else int(v))
                       for k, v in nb.items()},
    }


# ---------------------------------------------------------------------------
# ONE trial audit
# ---------------------------------------------------------------------------
def _audit_trial(solver: BoundaryHJBSolver, V_star: np.ndarray,
                 labor0: np.ndarray, rho: float, d_t: np.ndarray,
                 label: str, alpha: float, expected_gap: float,
                 expected_rows: tuple) -> TrialAudit:
    n, nz = solver.n, solver.nz
    grid = solver.grid
    V_trial = V_star + alpha * d_t.reshape((n, nz), order="F")
    if not np.isfinite(V_trial).all():
        raise F0RatePathDivergenceFailure(f"non-finite trial state ({label})")

    # exactly ONE final=False re-selection, then ONE corrected final=True build
    Q_iter, u_iter, _di, records_iter = solver.build_operator_and_u(
        V_trial, labor0, 0.0, 0.0, final=False)
    Q_final, u_final, _df, records_final = solver.build_operator_and_u(
        V_trial, labor0, 0.0, 0.0, final=True, f0_policies=records_iter)

    f0_rows = _f0_rows_of(solver)
    if len(f0_rows) != 596:
        raise F0RatePathDivergenceFailure(
            f"unexpected F0 row count {len(f0_rows)}")

    total = 0
    rate_identical = 0
    b_div = 0
    a_div = 0
    dir_div = 0
    opp_dir_div = 0
    diag_div = 0
    layout_div = 0
    omitted_div = 0
    q_div = 0
    max_b = 0.0
    max_a = 0.0
    max_diag = 0.0
    max_q = 0.0
    max_decomp_resid = 0.0
    inconsistent: list[int] = []
    rows: list[RowEvidence] = []
    all_reproduced = True
    same_controls = True

    for r in f0_rows:
        r = int(r)
        rec_i = records_iter[r]
        rec_f = records_final[r]
        if rec_i is None or rec_f is None:
            raise F0RatePathDivergenceFailure(f"missing F0 record at row {r}")
        total += 1

        # same controls / utility across the two constructions
        if not (rec_i.consumption == rec_f.consumption
                and rec_i.labor == rec_f.labor
                and rec_i.transfer == rec_f.transfer
                and rec_i.utility == rec_f.utility
                and rec_i.mu_a == rec_f.mu_a
                and rec_i.mu_b == rec_f.mu_b):
            same_controls = False

        info = _row_rates(solver, V_trial, labor0, r, rec_i)
        all_reproduced = all_reproduced and info["row_reproduction_ok"]

        it_b = (info["it_bb"], info["it_bf"])
        raw_b = (info["raw_bb"], info["raw_bf"])
        it_a = (info["it_ab"], info["it_af"])
        raw_a = (info["raw_ab"], info["raw_af"])
        bd = max(abs(it_b[0] - raw_b[0]), abs(it_b[1] - raw_b[1]))
        ad = max(abs(it_a[0] - raw_a[0]), abs(it_a[1] - raw_a[1]))
        dd = abs(float(rec_i.diagonal) - float(rec_f.diagonal))
        dir_bad = (info["iteration_active_b"] != info["raw_active_b"]
                   or info["iteration_active_a"] != info["raw_active_a"])
        opp_bad = bool(
            info["iteration_opposite_b_component"]
            or info["iteration_opposite_a_component"]
            or info["raw_opposite_b_component"]
            or info["raw_opposite_a_component"])
        if info["raw_opposite_b_component"] or info["raw_opposite_a_component"]:
            raise F0RatePathDivergenceFailure(
                f"row {r} ({label}): the corrected raw upwind path stored an "
                "opposite-direction component, which is structurally "
                "impossible for max(+-mu)/step")
        max_b = max(max_b, bd)
        max_a = max(max_a, ad)
        max_diag = max(max_diag, dd)
        if bd > ROW_ZERO_TOL:
            b_div += 1
        if ad > ROW_ZERO_TOL:
            a_div += 1
        if dir_bad:
            dir_div += 1
        if opp_bad:
            opp_dir_div += 1
        if dd > ROW_ZERO_TOL:
            diag_div += 1

        it_dest = {int(dn): float(rt) for dn, rt in rec_i.row_entries}
        fi_dest = {int(dn): float(rt) for dn, rt in rec_f.row_entries}
        it_cols = {info["z"] * n + dn for dn in it_dest}
        fi_cols = {info["z"] * n + dn for dn in fi_dest}
        # Destination-layout divergence is defined STRICTLY as one path
        # truncating a destination the other path does NOT truncate (an
        # interior destination placed in a different block, or a destination
        # dropped while its raw rate is non-zero). A destination that is simply
        # present with rate exactly 0.0 on one path is NOT a layout divergence:
        # both paths share the identical four-slot upwind template inside the
        # same z block, and only the RATE VALUES differ.
        layout_bad = any(
            abs(fi_dest.get(int(c) - info["z"] * n, 0.0)) > ROW_ZERO_TOL
            for c in it_cols - fi_cols) or any(
            abs(it_dest.get(int(c) - info["z"] * n, 0.0)) > ROW_ZERO_TOL
            for c in fi_cols - it_cols) or any(
            not (info["z"] * n <= c < (info["z"] + 1) * n)
            for c in (it_cols | fi_cols))
        if layout_bad:
            layout_div += 1
        it_sum = float(sum(it_dest.values()))
        fi_sum = float(sum(fi_dest.values()))
        omitted_it = -(float(rec_i.diagonal)) - it_sum
        omitted_fi = -(float(rec_f.diagonal)) - fi_sum
        omitted_bad = abs(omitted_it - omitted_fi) > ROW_ZERO_TOL
        if omitted_bad:
            omitted_div += 1
        if abs(omitted_it) > ROW_ZERO_TOL or abs(omitted_fi) > ROW_ZERO_TOL:
            raise F0RatePathDivergenceFailure(
                f"unexpected omitted destination rate at row {r} ({label})")

        a_i = np.asarray(Q_iter.getrow(r).toarray()).ravel()
        a_f = np.asarray(Q_final.getrow(r).toarray()).ravel()
        gap = float(np.max(np.abs(a_f - a_i)))
        max_q = max(max_q, gap)
        if gap > ROW_ZERO_TOL:
            q_div += 1
            inconsistent.append(r)
        else:
            rate_identical += 1

        diff_cols = np.nonzero(np.abs(a_f - a_i) > ROW_ZERO_TOL)[0]
        # decomposition closure: summed off-diagonal rate difference must equal
        # the diagonal difference
        merged = sorted(set(it_cols) | set(fi_cols))
        summed = 0.0
        for c in merged:
            it_v = it_dest.get(c - info["z"] * n, 0.0)
            fi_v = fi_dest.get(c - info["z"] * n, 0.0)
            summed += abs(fi_v - it_v)
        resid = abs(summed - dd)
        max_decomp_resid = max(max_decomp_resid, resid)

        if gap > ROW_ZERO_TOL:
            rows.append(RowEvidence(
                row=r, node=info["node"], j=info["j"], i=info["i"],
                z=info["z"], family=info["family"], sector=info["sector"],
                transfer_label=info["transfer_label"],
                consumption=info["consumption"], labor=info["labor"],
                transfer=info["transfer"], utility=info["utility"],
                stored_mu_a=info["stored_mu_a"],
                stored_mu_b=info["stored_mu_b"],
                raw_mu_a=info["raw_mu_a"], raw_mu_b=info["raw_mu_b"],
                iteration_b_backward_rate=info["it_bb"],
                iteration_b_forward_rate=info["it_bf"],
                iteration_a_backward_rate=info["it_ab"],
                iteration_a_forward_rate=info["it_af"],
                raw_b_backward_rate=info["raw_bb"],
                raw_b_forward_rate=info["raw_bf"],
                raw_a_backward_rate=info["raw_ab"],
                raw_a_forward_rate=info["raw_af"],
                iteration_active_b=info["iteration_active_b"],
                raw_active_b=info["raw_active_b"],
                iteration_active_a=info["iteration_active_a"],
                raw_active_a=info["raw_active_a"],
                iteration_opposite_direction_component=bool(
                    info["iteration_opposite_b_component"]
                    or info["iteration_opposite_a_component"]),
                raw_opposite_direction_component=bool(
                    info["raw_opposite_b_component"]
                    or info["raw_opposite_a_component"]),
                b_rate_divergent=bool(bd > ROW_ZERO_TOL),
                a_rate_divergent=bool(ad > ROW_ZERO_TOL),
                active_direction_divergent=bool(dir_bad),
                iteration_diagonal=float(rec_i.diagonal),
                final_diagonal=float(rec_f.diagonal),
                diagonal_difference=dd,
                iteration_destinations=tuple(sorted(it_cols)),
                final_destinations=tuple(sorted(fi_cols)),
                destination_layout_divergent=bool(layout_bad),
                omitted_iteration_rate=float(omitted_it),
                omitted_final_rate=float(omitted_fi),
                q_gap_nonzero_columns=tuple(int(c) for c in diff_cols),
                q_gap_column_magnitudes=tuple(
                    float(abs(a_f[int(c)] - a_i[int(c)])) for c in diff_cols),
                rowwise_max_gap=gap,
                summed_rate_difference=float(summed),
                decomposition_residual=float(resid),
                row_reproduction_ok=info["row_reproduction_ok"],
            ))

    gap_ok = abs(max_q - expected_gap) <= REPRO_TOL
    rows_ok = tuple(sorted(inconsistent)) == tuple(sorted(expected_rows))
    if not gap_ok or not rows_ok:
        raise F0RatePathDivergenceFailure(
            f"{label}: accepted Issue #68 gap/rows not reproduced "
            f"(gap={max_q!r} vs {expected_gap!r}; rows={sorted(inconsistent)} "
            f"vs {sorted(expected_rows)})")
    decomp_closed = max_decomp_resid <= DECOMP_TOL
    if not decomp_closed:
        raise F0RatePathDivergenceFailure(
            f"{label}: rowwise Q-gap decomposition does not close "
            f"(max residual {max_decomp_resid!r})")
    if not all_reproduced:
        raise F0RatePathDivergenceFailure(
            f"{label}: stored iteration rates were not reproduced from the "
            "accepted policy function")
    if not same_controls:
        raise F0RatePathDivergenceFailure(
            f"{label}: controls/utility differ across the compared paths")

    return TrialAudit(
        label=label, alpha=float(alpha),
        total_f0_rows=total,
        rate_identical_row_count=rate_identical,
        b_rate_divergent_row_count=b_div,
        a_rate_divergent_row_count=a_div,
        active_direction_divergent_row_count=dir_div,
        opposite_direction_component_row_count=opp_dir_div,
        diagonal_divergent_row_count=diag_div,
        destination_layout_divergent_row_count=layout_div,
        omitted_rate_divergent_row_count=omitted_div,
        q_row_divergent_row_count=q_div,
        max_b_rate_difference=max_b,
        max_a_rate_difference=max_a,
        max_diagonal_difference=max_diag,
        max_rowwise_q_difference=max_q,
        inconsistent_rows=tuple(sorted(inconsistent)),
        inconsistent_row_set_match=rows_ok,
        expected_gap=float(expected_gap),
        expected_rows=tuple(expected_rows),
        gap_reproduced=gap_ok,
        max_decomposition_residual=max_decomp_resid,
        decomposition_closed=decomp_closed,
        all_rows_reproduced=all_reproduced,
        same_controls_and_utility=same_controls,
        rows=rows,
    )


def _f0_rows_of(solver: BoundaryHJBSolver) -> np.ndarray:
    n, nz = solver.n, solver.nz
    fam = np.array([str(solver.grid.families[node]) for node in range(n)])
    return np.nonzero(np.tile(fam == "F0", nz))[0]


# ---------------------------------------------------------------------------
# read-only source provenance mapping
# ---------------------------------------------------------------------------
def provenance_mapping() -> dict:
    """Read-only, source-backed mapping of both rate-construction paths.

    Line anchors reference the accepted sources under the accepted blobs
    (selected-Q `556ccc214f03a1a22306cc4f5c7e9f7691bbf897`, oracle
    `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`).
    """
    return {
        "iteration_rate_path": {
            "source": "src/deep_learning_hank/two_asset/"
                      "matlab_faithful_two_asset_ha.py",
            "policy_selector": "select_matlab_faithful_local_policy "
                               "(lines 193-416)",
            "b_rate_construction": "lines 408-415: "
                "iteration_b_backward_rate = -(sc_b if use_liquid_b else 0) "
                "- (sdh_b if use_transfer_b else 0)) / db; "
                "iteration_b_forward_rate = +(sc_f if use_liquid_f else 0) "
                "+ (sdh_f if use_transfer_f else 0)) / db",
            "liquid_branch_tree": "lines 281-298: "
                "sc_b = liquid_resources_b - consumption_b; "
                "sc_f = liquid_resources_f - consumption_f; "
                "use_liquid_b = sc_b < -tolerance; "
                "use_liquid_f = sc_f > tolerance and not use_liquid_b; "
                "liquid_label in {B, F, 0}",
            "transfer_branch_tree": "lines 302-321 and 322-350: "
                "d_b = d_bf*(d_bf>0) + d_bb*(d_bb<0); "
                "d_f = d_ff*(d_ff>0) + d_fb*(d_fb<0); "
                "sdh_b = -d_b - adjustment_cost(d_b); "
                "sdh_f = -d_f - adjustment_cost(d_f); "
                "use_transfer_f = sdh_f > tolerance; "
                "use_transfer_b = sdh_b < -tolerance and not use_transfer_f",
            "objects_are_foc_shadow_not_drift": True,
            "note": "sc_b/sc_f are LIQUID first-order-condition residuals and "
                    "sdh_b/sdh_f are TRANSFER branch objects; neither is the "
                    "realized drift mu_b",
            "a_rate_construction": "lines 406-407: a_backward_rate = "
                "-mh_b/da with mh_b = min(shadow_transfer_b, 0); "
                "a_forward_rate = mh_f/da with "
                "mh_f = max(shadow_transfer_f, 0) + effective_return*a",
            "assembled_in": "boundary_hjb_selected_q.local_interior_row "
                            "(lines 484-521): entries from "
                            "iteration_b_backward_rate / "
                            "iteration_b_forward_rate / a_backward_rate / "
                            "a_forward_rate; diagonal = -(rb+rf+ab+af)",
        },
        "final_raw_rate_path": {
            "source": "src/deep_learning_hank/two_asset/"
                      "boundary_hjb_selected_q.py",
            "final_branch": "build_operator_and_u final=True branch "
                            "(lines 957-994)",
            "drift_recompute": "asset_drifts_matlab_faithful with the SAME "
                               "selected controls (consumption, labor, "
                               "transfer)",
            "rate_mapping": "lines 966-969: "
                "ab = max(-mu_a,0)/da; af = max(mu_a,0)/da; "
                "bb = max(-mu_b,0)/db; bf = max(mu_b,0)/db",
            "diagonal_construction": "line 976: diag = -(bb+bf+ab+af)",
            "destination_layout": "same-z-block, cols.append(nz*n + dn) "
                                  "(repaired under Issue #67)",
        },
        "equivalence": {
            "globally_algebraically_equivalent": False,
            "reason": "the iteration b-rate uses branch-gated FOC shadow "
                      "objects (sc_b/sc_f and sdh_b/sdh_f), whereas the "
                      "corrected final b-rate uses the realized drift "
                      "max(+-mu_b)/db; these coincide only when the liquid "
                      "branch is inactive (liquid_label '0'), i.e. when "
                      "neither sc_b < -tol nor sc_f > tol holds",
        },
        "divergence_condition": {
            "kind": "sign_or_branch",
            "condition": "liquid_label == 'F' (use_liquid_f true, so sc_f > "
                         "tolerance) while the realized mu_b < 0, so the "
                         "iteration path stores a positive "
                         "iteration_b_forward_rate that the raw upwind path "
                         "does not (raw b_forward = 0) and an inflated "
                         "iteration_b_backward_rate",
            "a_axis_affected": False,
            "destination_layout_affected": False,
            "truncation_affected": False,
        },
        "read_only": True,
        "source_mutation": False,
    }


# ---------------------------------------------------------------------------
# the ONE full audit
# ---------------------------------------------------------------------------
def _run_from_reconstruction(rec: dict) -> DivergenceAuditResult:
    failure: Optional[dict] = None
    try:
        solver: BoundaryHJBSolver = rec["solver"]
        labor0: np.ndarray = rec["labor0"]
        V_star: np.ndarray = rec["V_star"]
        rho: float = rec["rho"]
        trace: list = rec["trace"]
        n, nz, S = solver.n, solver.nz, solver.state_size
        V_flat = V_star.ravel(order="F")

        # 1. frozen reconstruction + accepted Issue #68 tangent geometry
        if len(trace) != 8:
            raise F0RatePathDivergenceFailure("reconstruction != 8 steps")
        final_statistic = float(trace[-1]["accepted_max_stat"])
        wall = dict(trace[-1]["worst_after"])
        pb_star, wall_node, wall_nz = _min_boundary_pb(solver, V_star, labor0)
        if not np.isfinite(pb_star):
            raise F0RatePathDivergenceFailure("non-finite required p_b(V_*)")

        Q0, u0, _d0, _r0 = solver.build_operator_and_u(
            V_star, labor0, 0.0, 0.0, final=False)
        R0 = rho * V_flat - (u0 + Q0.dot(V_flat))
        if not np.isfinite(R0).all():
            raise F0RatePathDivergenceFailure("non-finite base residual")
        r_inf = float(np.max(np.abs(R0)))
        d_n = linalg.spsolve(rho * sparse.eye(S, format="csr") - Q0, -R0)
        if not np.isfinite(d_n).all():
            raise F0RatePathDivergenceFailure("non-finite Newton direction")
        gvec = limiting_wall_gradient(solver, wall_node, wall_nz)
        proj = single_wall_tangent_projection(d_n, gvec)
        d_t = proj["d_T"]

        # 2/3/4. exactly TWO frozen trials, each with its own single pair of
        # builds and one all-F0 decomposition
        trials = [
            _audit_trial(solver, V_star, labor0, rho, d_t, "alpha_half",
                         ALPHA_HALF, EXPECTED_GAP_HALF, EXPECTED_ROWS_HALF),
            _audit_trial(solver, V_star, labor0, rho, d_t, "alpha_near",
                         ALPHA_NEAR, EXPECTED_GAP_NEAR, EXPECTED_ROWS_NEAR),
        ]

        # 5. read-only provenance mapping
        prov = provenance_mapping()

        # classification flags (frozen Issue #69 semantics; nothing is forced)
        iter_backed = True
        final_backed = True
        globally_equivalent = False
        # the divergence is a SIGN/BRANCH mechanism when every affected row
        # diverges on the b-axis rates AND the accepted iteration path stores a
        # non-zero rate component OPPOSING the realized drift direction (which
        # the corrected raw upwind path structurally cannot do)
        sign_div = bool(trials) and all(
            all(row.b_rate_divergent
                and row.iteration_opposite_direction_component
                and not row.raw_opposite_direction_component
                for row in t.rows)
            and t.b_rate_divergent_row_count > 0
            and t.opposite_direction_component_row_count
            == t.q_row_divergent_row_count
            for t in trials)
        trunc_div = any(t.destination_layout_divergent_row_count > 0
                        for t in trials)
        a_axis_clean = all(t.a_rate_divergent_row_count == 0 for t in trials)
        omitted_clean = all(t.omitted_rate_divergent_row_count == 0
                            for t in trials)
        layout_clean = not trunc_div
        other = bool(not a_axis_clean or not omitted_clean)
        fully_accounts = all(t.decomposition_closed for t in trials)
        mixed = bool((sign_div and trunc_div) or other)

        if sign_div and fully_accounts and layout_clean and not other:
            terminal = TERMINAL_A
        elif trunc_div and fully_accounts and not sign_div and not other:
            terminal = TERMINAL_B
        else:
            terminal = TERMINAL_C

        return DivergenceAuditResult(
            terminal=terminal,
            failure_detail=None,
            iterations=len(trace),
            final_statistic=final_statistic,
            min_boundary_pb_star=float(pb_star),
            wall_state=wall,
            r_inf=r_inf,
            tangent_identity_residual=float(proj["g_dot_d_t"]),
            provenance=prov,
            iter_rate_path_source_backed=iter_backed,
            final_raw_path_source_backed=final_backed,
            rate_formulas_globally_equivalent=globally_equivalent,
            sign_or_branch_divergence_established=bool(sign_div),
            truncation_or_destination_divergence_established=bool(trunc_div),
            other_mechanism_established=other,
            mixed_or_unresolved=mixed,
            trial_count=len(trials),
            trials=trials,
            a_axis_rates_identical_all_rows=bool(a_axis_clean),
            accepted_new_hjb_iterate=False,
            deterministic_repeat_identical=False,
        )
    except F0RatePathDivergenceFailure as exc:
        failure = {"reason": str(exc)}
    except Exception as exc:  # pragma: no cover - defensive
        failure = {"reason": f"unexpected failure: {exc!r}"}

    return DivergenceAuditResult(
        terminal=TERMINAL_C,
        failure_detail=failure,
        accepted_new_hjb_iterate=False,
        deterministic_repeat_identical=False,
    )


def _min_boundary_pb(solver: BoundaryHJBSolver, V: np.ndarray,
                     labor0: np.ndarray) -> tuple[float, int, int]:
    from deep_learning_hank.two_asset.adaptive_resolvent_hjb import (
        min_boundary_pb_state,
    )
    return min_boundary_pb_state(solver, V, labor0)


def run_issue69_audit() -> DivergenceAuditResult:
    """Exactly ONE full Issue #69 audit (ONE reconstruction, exactly TWO frozen
    trials each with one re-selection and one corrected final build, ONE
    all-F0 decomposition per trial, ONE provenance mapping)."""
    return _run_from_reconstruction(reconstruct_issue63_stagnation_state())


def _canon(r: DivergenceAuditResult) -> dict:
    return dataclasses.asdict(r)


def run_issue69_audit_twice() -> tuple[DivergenceAuditResult, bool]:
    """The ONE deterministic repeat of the full audit."""
    first = run_issue69_audit()
    second = run_issue69_audit()
    identical = bool(_canon(first) == _canon(second))
    first.deterministic_repeat_identical = identical
    return first, identical


def summary_csv_lines(r: DivergenceAuditResult) -> list[str]:
    """Compact CSV evidence lines for the Issue #69 report."""
    lines = ["metric,value"]
    for f in dataclasses.fields(r):
        if f.name in ("trials", "provenance"):
            continue
        v = getattr(r, f.name)
        if isinstance(v, dict):
            v = "; ".join(f"{k}={v[k]}" for k in sorted(v))
        lines.append(f"{f.name},{v}")
    for t in r.trials:
        for f in dataclasses.fields(t):
            if f.name == "rows":
                continue
            v = getattr(t, f.name)
            lines.append(f"{t.label}.{f.name},{v}")
        for row in t.rows:
            for f in dataclasses.fields(row):
                v = getattr(row, f.name)
                lines.append(f"{t.label}.row{row.row}.{f.name},{v}")
    return lines
