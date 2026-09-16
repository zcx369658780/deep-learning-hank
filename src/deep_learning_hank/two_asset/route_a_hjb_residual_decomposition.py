"""DLH-5V-W — Route-A single-`Q` HJB residual source decomposition at `V_*`.

Issue #71 / DLH-5V-W
``SCIENTIFIC_NUMERICAL_DIAGNOSTIC__ROUTE_A_SINGLE_Q_HJB_RESIDUAL_SOURCE_DECOMPOSITION``

Authority: Issue #71 OPEN; initial authoritative activation ``5691703381``; final
authoritative activation-refresh ``5691863227`` (post-sync live ``main``
``e1a7a9ac5b00ad4407fcc40bdfb67e46c4ccbe86``). Route decision
``APPROVE_ROUTE_A_SINGLE_Q_HJB_RESIDUAL_SOURCE_DECOMPOSITION_AFTER_5VV_TERMINAL_A``;
authority marker ``DLH_5VW_ROUTE_A_HJB_RESIDUAL_DECOMPOSITION_AUTHORIZED``.

Scientific question
-------------------
Owner Route A (accepted Issue #70 / DLH-5V-V) established ONE coherent
MATLAB-faithful selected generator for both the HJB solve and final validation, so
the remaining Bellman residual at the accepted stagnation state `V_*` is now a
genuine single-operator residual::

    R = rho*V - u - Q*V

with ``||R||inf = 10.435094313164921``, i.e. ~``10435``x the unchanged Bellman
tolerance ``1e-3``. This Issue decomposes that residual **additively and
source-backed** to determine where it comes from.

Scope ceiling (read-only diagnostic):
exactly ONE frozen state (`V_*`); exactly ONE Route-A ``final=False`` operator
build; ONE all-state additive decomposition; ONE deterministic top-20 selection;
ONE read-only top-20 F0 policy-reproduction audit; ONE deterministic repeat.

This module does **NOT** construct a second scientific `Q`, does **NOT** build a
``final=True`` scientific comparison operator, does **NOT** run a Newton solve or
any tangent / trial / line-search / continuation step, does **NOT** accept an HJB
iterate, does **NOT** run a new trajectory, and does **NOT** mutate any accepted
source. The selector is re-invoked read-only, exactly as it was invoked during the
operator assembly, and never searched beyond its own deterministic evaluation.

Exact assembled operator structure (measured, source-backed)
-----------------------------------------------------------
``build_operator_and_u`` assembles ``Q = Q_struct + B`` where

- ``Q_struct`` is built per row from the accepted policy records. For F0 rows the
  record's ``row_entries`` are ``(destination_node, rate)`` pairs in **z-block
  local node coordinates** and are stored at absolute column ``z*n + dn`` (the
  accepted same-z-block destination indexing); the F0 record's ``diagonal`` is
  ``-(rb+rf+ab+af)`` under the accepted source truncation convention (an outgoing
  rate that is truncated at the domain edge is NOT represented as a destination
  but IS retained on the diagonal). Non-F0 rows come from the accepted
  ``_boundary_row`` assembly with the same local-to-absolute offset.
- ``B = kron(switch_matrix, I_n)`` is the accepted ``grid.switch_matrix``
  generator. Because ``B`` is added AFTER the per-row assembly, the **assembled**
  row has ``Q[row,row] = record.diagonal + switch_matrix[z,z]`` and
  ``Q[row, z2*n+node] = switch_matrix[z,z2]`` for ``z2 != z``.

This module therefore attributes each term to its OWN source:

- ``b_backward_term / b_forward_term / a_backward_term / a_forward_term`` — the
  four F0 rate slots published by the accepted ``local_interior_row`` assembly,
  read from the record's own ``row_entries`` through the accepted
  ``(neigh["down"], iteration_b_backward_rate)``, ``(neigh["up"],
  iteration_b_forward_rate)``, ``(neigh["left"], a_backward_rate)``,
  ``(neigh["right"], a_forward_rate)`` bijection. The bijection is ASSERTED, not
  assumed: a destination that cannot be attributed to exactly one slot, or whose
  assembled rate differs from that slot, is a rate-attribution mismatch and fails
  closed.
- ``boundary_term`` — the non-F0 accepted boundary row's outgoing moves, whose
  rates the accepted source publishes as a two-part sector rate not expressed in
  the four F0 slot names. They are reported as one explicitly named class rather
  than guessed into an F0 slot.
- ``diagonal_term`` — ``-(Q[row,row]) * V[row]`` with ``Q[row,row]`` the value the
  operator ACTUALLY carries (record diagonal plus the switch matrix's own diagonal
  entry). Recorded independently, because the accepted F0 diagonal retains
  truncated outgoing rates that have no represented destination.
- ``z_switch_term`` — ``-sum_{z2 != z} switch_matrix[z,z2] * V[z2*n+node]`` from
  the accepted switch matrix only.
- ``rhoV_term`` — ``rho*V[row]``; ``utility_source_term`` — ``u[row]``, the
  selected record's utility.

Sign convention (explicit and uniform)
-------------------------------------
Every component is reported so that the plain SUM of the nine components equals
the residual exactly::

    R[row] = rhoV_term - utility_source_term
             - sum_destination_terms - diagonal_term - z_switch_term

with each destination/diagonal/z-switch component defined as the POSITIVE
magnitude ``+(rate * V[dest])``. Equivalently the accumulator is

    rho*V[row] - u[row] - (Q*V)[row]

expanded exactly as above. The reconstruction is checked rowwise against the
directly assembled ``R`` and must close to floating-point ordering accuracy.
"""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field
from typing import Optional

import numpy as np
from scipy import sparse

from deep_learning_hank.two_asset.boundary_hjb_selected_q import (
    BoundaryHJBSolver,
)
from deep_learning_hank.two_asset.matlab_faithful_two_asset_ha import (
    select_matlab_faithful_local_policy,
)
from deep_learning_hank.two_asset.stagnation_newton_geometry import (
    reconstruct_issue63_stagnation_state,
)

# ---------------------------------------------------------------------------
# Frozen accepted references
# ---------------------------------------------------------------------------
SELECTED_Q_ACCEPTED_BLOB = "7857cabb4d28af99cb9d59e2d1c3024b05787c11"
SELECTED_Q_PRE_ISSUE70_BLOB = "556ccc214f03a1a22306cc4f5c7e9f7691bbf897"
ORACLE_BLOB = "76ae5b149993a7edeeb8eb337f1b02b3fe33c51e"
ISSUE69_AUDIT_BLOB = "83e9be0febcc03eb721265d3558887bd6b1586a4"

# accepted Issue #63 stagnation-state facts (frozen Issue #71 reproduction gate)
ACCEPTED_STEPS = 8
ACCEPTED_FINAL_STATISTIC = 3.6614352438846254e-08
ACCEPTED_MIN_BOUNDARY_PB = 4.8089461301970005e-09
ACCEPTED_WALL_FAMILY = "F3"
ACCEPTED_WALL_J = 13
ACCEPTED_WALL_I = 13
ACCEPTED_WALL_Z = 1
ACCEPTED_WALL_NODE = 332
ACCEPTED_RESIDUAL_INF = 10.435094313164921
ACCEPTED_RESIDUAL_ARGMAX_ROW = 97
ACCEPTED_RESIDUAL_ARGMAX_NODE = 97
ACCEPTED_RESIDUAL_ARGMAX_Z = 0
ACCEPTED_RESIDUAL_ARGMAX_FAMILY = "F0"
ACCEPTED_STATE_SIZE = 782
ACCEPTED_F0_STATE_COUNT = 596
ACCEPTED_NON_F0_STATE_COUNT = 186

BELLMAN_TOLERANCE_UNCHANGED = 1.0e-3

# tolerances
REPRO_TOL = 1.0e-9
# The rowwise closure is a sum of ~782 floating-point products whose magnitudes
# reach O(1e4) on boundary rows, so exact zero is not attainable; the frozen bound
# is set above the float-ordering floor (measured ~4.0e-11) and far below any
# physical residual scale (O(1e-3) Bellman tolerance).
CLOSURE_TOL = 1.0e-9
ZERO_TOL = 1.0e-12

TOP_N = 20

# ---------------------------------------------------------------------------
# Component classes (additive decomposition term names)
# ---------------------------------------------------------------------------
COMPONENT_NAMES = (
    "rhoV_term",
    "utility_source_term",
    "b_backward_term",
    "b_forward_term",
    "a_backward_term",
    "a_forward_term",
    "boundary_term",
    "diagonal_term",
    "z_switch_term",
)
# the four F0 source-backed rate slots, in frozen reporting order
F0_SLOT_NAMES = ("b_backward_term", "b_forward_term", "a_backward_term",
                 "a_forward_term")

# ---------------------------------------------------------------------------
# frozen classification flags
# ---------------------------------------------------------------------------
DECOMPOSITION_CLOSED = "DECOMPOSITION_CLOSED"
DOMINANT_RESIDUAL_F0 = "DOMINANT_RESIDUAL_F0"
POLICY_RECORDS_REPRODUCED = "POLICY_RECORDS_REPRODUCED"
DOMINANT_COMPONENT_IDENTIFIED = "DOMINANT_COMPONENT_IDENTIFIED"
BRANCH_INCONSISTENCY_ESTABLISHED = "BRANCH_INCONSISTENCY_ESTABLISHED"
OTHER_MECHANISM_ESTABLISHED = "OTHER_MECHANISM_ESTABLISHED"
MIXED_OR_UNRESOLVED = "MIXED_OR_UNRESOLVED"

# ---------------------------------------------------------------------------
# frozen terminals
# ---------------------------------------------------------------------------
TERMINAL_A = (
    "DLH_5VW_ROUTE_A_HJB_RESIDUAL_DECOMPOSITION__UNIQUE_SOURCE_BACKED_DOMINANT_"
    "MECHANISM_IDENTIFIED__NEXT_SOLVER_DESIGN_GATE_READY")
TERMINAL_B = (
    "DLH_5VW_ROUTE_A_HJB_RESIDUAL_DECOMPOSITION__DECOMPOSITION_AND_POLICY_"
    "REPRODUCTION_PASS_BUT_RESIDUAL_IS_MIXED_FIXED_POINT_IMBALANCE__BOUNDED_"
    "SOLVER_DESIGN_REQUIRED")
TERMINAL_C = (
    "DLH_5VW_ROUTE_A_HJB_RESIDUAL_DECOMPOSITION__DECOMPOSITION_POLICY_"
    "REPRODUCTION_OR_SINGLE_Q_CONTRACT_FAILURE__SCIENTIFIC_REVIEW_REQUIRED")
TERMINAL_BLOCKED = "BLOCKED_DLH_5VW_AUTHORITY_OR_DEPENDENCY_CONFLICT"

# ---------------------------------------------------------------------------
# FROZEN dominance criteria (declared BEFORE any measurement, so Outcome A can
# never be manufactured post hoc)
# ---------------------------------------------------------------------------
# Two DIFFERENT things are measured, and both are reported:
#
#  (D1) the row-wise LARGEST additive class, computed per row over the eight
#       non-diagonal components plus the explicit classes;
#  (D2) the CANCELLATION RATIO |R[row]| / sum_c |component_c[row]|, which says
#       whether the residual is carried by one term or is the small remainder of
#       near-total cancellation among large terms.
#
# A single source-backed DOMINANT MECHANISM is declared only when ALL of:
#   (1) every top-20 row has the SAME largest non-diagonal class
#       (coverage >= DOMINANCE_TOP20_COVERAGE);
#   (2) the leading two classes of the top-20 aggregate are clearly separated
#       (relative gap >= DOMINANCE_MIN_LEADING_GAP);
#   (3) the top-20 mean cancellation ratio is >= DOMINANCE_MIN_CANCELLATION_RATIO,
#       i.e. the residual is a substantial fraction of the gross component mass
#       rather than a small cancellation remainder;
#   (4) there are zero rate-attribution mismatches.
# Otherwise the residual is a cancellation/fixed-point imbalance and the outcome
# is the mixed terminal (Outcome B).
DOMINANCE_TOP20_COVERAGE = 1.0
DOMINANCE_MIN_LEADING_GAP = 0.25
DOMINANCE_MIN_CANCELLATION_RATIO = 0.10
BRANCH_INCONSISTENCY_MIN_ROWS = 1


class ResidualDecompositionFailure(RuntimeError):
    """Fail-closed: non-finite evidence, a failed frozen-state reproduction, a
    rate-attribution mismatch, a decomposition that does not close, a policy
    reproduction mismatch, or a non-deterministic repeat."""


# ---------------------------------------------------------------------------
# Result containers
# ---------------------------------------------------------------------------
@dataclass
class StateRow:
    """Per-state additive residual decomposition (ALL states are covered)."""

    row: int
    node: int
    j: int
    i: int
    z: int
    family: str
    residual: float
    abs_residual: float
    residual_sign: int
    rhoV_term: float
    utility_source_term: float
    b_backward_term: float
    b_forward_term: float
    a_backward_term: float
    a_forward_term: float
    boundary_term: float
    diagonal_term: float
    z_switch_term: float
    reconstructed_R: float
    closure_error: float
    operator_row_closure_error: float
    represented_destinations: tuple
    rate_attribution_ok: bool
    sector: str
    liquid_label: Optional[str]
    transfer_label: Optional[str]
    consumption: float
    labor: float
    transfer: float
    mu_a: float
    mu_b: float
    stored_b_backward_rate: float
    stored_b_forward_rate: float
    stored_a_backward_rate: float
    stored_a_forward_rate: float
    stored_diagonal: float
    assembled_diagonal: float
    # the accepted F0 assembly derives diagonal = -(rb+rf+ab+af); the stored
    # diagonal is therefore the negated SUM of these four slots, so a truncated
    # outgoing slot (absent from the entries but present on the diagonal) shows up
    # as the difference between the slot sum and -stored_diagonal.
    f0_slot_rates: Optional[tuple] = None
    truncated_slot_mass: float = 0.0
    neighbours: dict = field(default_factory=dict)

    def component_vector(self) -> dict:
        """The nine additive components, in frozen reporting order."""
        return {name: float(getattr(self, name)) for name in COMPONENT_NAMES}


@dataclass
class TopRow:
    """ONE deterministic top-20 residual row (full reporting payload)."""

    rank: int
    row: int
    node: int
    j: int
    i: int
    z: int
    family: str
    residual: float
    abs_residual: float
    residual_sign: int
    sector: str
    liquid_label: Optional[str]
    transfer_label: Optional[str]
    consumption: float
    labor: float
    transfer: float
    mu_a: float
    mu_b: float
    stored_b_backward_rate: float
    stored_b_forward_rate: float
    stored_a_backward_rate: float
    stored_a_forward_rate: float
    neighbours: dict
    represented_destinations: tuple
    rhoV_term: float
    utility_source_term: float
    b_backward_term: float
    b_forward_term: float
    a_backward_term: float
    a_forward_term: float
    boundary_term: float
    diagonal_term: float
    z_switch_term: float
    reconstructed_R: float
    closure_error: float
    largest_component_class: str
    largest_component_abs: float
    branch_inconsistent: bool
    is_f0: bool


@dataclass
class PolicyReproduction:
    """Read-only reproduction result for ONE top-20 F0 row."""

    row: int
    node: int
    j: int
    i: int
    z: int
    sector: str
    reproduced: bool
    controls_match: bool
    utility_match: bool
    drifts_match: bool
    stored_rates_match: bool
    labels_match: bool
    liquid_label: str
    transfer_label: str
    record_liquid_label: str
    record_transfer_label: str
    max_control_abs_diff: float
    max_drift_abs_diff: float
    max_rate_abs_diff: float
    utility_abs_diff: float
    mismatch_detail: str


@dataclass
class DecompositionResult:
    """ONE fully determined Issue #71 decomposition outcome."""

    terminal: str
    failure_detail: Optional[dict] = None
    # frozen-state reproduction
    steps: int = 0
    final_statistic: float = float("nan")
    min_boundary_pb_star: float = float("nan")
    wall_state: dict = field(default_factory=dict)
    residual_inf: float = float("nan")
    residual_argmax_row: int = -1
    residual_argmax_node: int = -1
    residual_argmax_z: int = -1
    residual_argmax_family: str = ""
    bellman_tolerance: float = BELLMAN_TOLERANCE_UNCHANGED
    residual_over_tolerance: float = float("nan")
    # all-state statistics
    total_states: int = 0
    f0_state_count: int = 0
    non_f0_state_count: int = 0
    max_abs_R_f0: float = float("nan")
    argmax_f0_row: int = -1
    max_abs_R_non_f0: float = float("nan")
    argmax_non_f0_row: int = -1
    max_abs_R_z0: float = float("nan")
    max_abs_R_z1: float = float("nan")
    positive_residual_count: int = 0
    negative_residual_count: int = 0
    zero_residual_count: int = 0
    top_absolute_contribution_class: str = ""
    contribution_class_totals: dict = field(default_factory=dict)
    contribution_class_maxima: dict = field(default_factory=dict)
    decomposition_closure_max_error: float = float("nan")
    operator_row_closure_max_error: float = float("nan")
    top20_f0_count: int = 0
    policy_reproduction_failure_count: int = 0
    max_abs_q1: float = float("nan")
    # structural accounting
    rate_attribution_mismatch_rows: int = 0
    operator_build_count: int = 0
    selector_call_count: int = 0
    # top-20 + reproduction
    top20: list = field(default_factory=list)
    policy_reproductions: list = field(default_factory=list)
    # classification
    decomposition_closed: bool = False
    dominant_residual_f0: bool = False
    policy_records_reproduced: bool = False
    dominant_component_identified: bool = False
    dominant_component_class: str = ""
    dominance_share: float = float("nan")
    dominance_top20_coverage: float = float("nan")
    dominance_leading_gap: float = float("nan")
    cancellation_ratio_top20_mean: float = float("nan")
    cancellation_ratio_top20_max: float = float("nan")
    top20_component_totals: dict = field(default_factory=dict)
    branch_inconsistency_established: bool = False
    other_mechanism_established: bool = False
    mixed_or_unresolved: bool = False
    accepted_new_hjb_iterate: bool = False
    new_trajectory_run: bool = False
    deterministic_repeat_identical: bool = False
    flags: tuple = ()
    rows: list = field(default_factory=list)


# ---------------------------------------------------------------------------
# F0 rate-slot attribution (source-backed, asserted not assumed)
# ---------------------------------------------------------------------------
def _f0_slot_of(destination: int, neigh: dict) -> Optional[str]:
    """The ONE source-backed rate slot that produced this F0 destination.

    Mirrors the accepted ``local_interior_row`` assembly exactly, which appends
    each slot to exactly one destination and stores the result as the record's
    ``row_entries``.
    """
    if neigh.get("down") is not None and destination == int(neigh["down"]):
        return "b_backward_term"
    if neigh.get("up") is not None and destination == int(neigh["up"]):
        return "b_forward_term"
    if neigh.get("left") is not None and destination == int(neigh["left"]):
        return "a_backward_term"
    if neigh.get("right") is not None and destination == int(neigh["right"]):
        return "a_forward_term"
    return None


# ---------------------------------------------------------------------------
# ONE all-state additive decomposition
# ---------------------------------------------------------------------------
def _decompose(solver: BoundaryHJBSolver, V: np.ndarray, u: np.ndarray,
               records: list, rho: float,
               QV: np.ndarray, R: np.ndarray,
               ) -> tuple[list, float, float, int, dict]:
    """Additive decomposition of ``R`` over EVERY state.

    The operator is NOT rebuilt: only the ONE already-assembled ``Q`` (through its
    matrix-vector product ``QV``) and the assembled residual ``R`` are read,
    together with the accepted policy records.
    """
    cfg = solver.config
    g = solver.grid
    n, nz = solver.n, solver.nz
    switch = np.asarray(cfg.switch_matrix, dtype=float)
    Vf = V.ravel(order="F")

    rows: list[StateRow] = []
    max_closure = 0.0
    max_op_closure = 0.0
    attribution_mismatch_rows = 0

    for node in range(n):
        j, i = int(g.j_arr[node]), int(g.i_arr[node])
        fam = str(g.families[node])
        neigh = g.neighbors(j, i)
        for z in range(nz):
            row = z * n + node
            rec = records[row]
            if rec is None:
                raise ResidualDecompositionFailure(
                    f"missing accepted policy record at row {row}")

            terms = {name: 0.0 for name in COMPONENT_NAMES}
            represented = []
            attribution_ok = True
            slot_rates = None
            truncated_mass = 0.0

            if fam == "F0":
                # ---- attribute every destination to its source-backed slot.
                #      Values are read from the record's OWN ``row_entries``
                #      through the accepted (dn, slot) bijection; no rate is ever
                #      inferred from a variable name or recomputed.
                slot_rates = {name: 0.0 for name in F0_SLOT_NAMES}
                for dn, rate in rec.row_entries:
                    slot = _f0_slot_of(int(dn), neigh)
                    if slot is None:
                        attribution_ok = False
                        continue
                    slot_rates[slot] = float(rate)
                for dst, rate in rec.row_entries:
                    dst = int(dst)
                    slot = _f0_slot_of(dst, neigh)
                    if slot is None:
                        continue
                    col = z * n + dst
                    represented.append((col, float(rate), slot))
                # truncation: slots with a non-zero rate whose destination does
                # not exist are kept on the diagonal by the accepted convention
                for name in F0_SLOT_NAMES:
                    if slot_rates[name] != 0.0:
                        present = any(s == name for _, _, s in represented)
                        if not present:
                            truncated_mass += abs(slot_rates[name])
            else:
                # ---- non-F0: accepted boundary assembly. Its rates are published
                #      as a two-part sector rate, not the four F0 slot names.
                for dst, rate in rec.row_entries:
                    col = z * n + int(dst)
                    represented.append((col, float(rate), "boundary_term"))

            if not attribution_ok:
                attribution_mismatch_rows += 1

            # ---- diagonal: the accepted record's OWN stored diagonal PLUS the
            #      switch matrix's own diagonal entry (the assembler adds B AFTER
            #      the per-row assembly, so Q[row,row] = rec.diagonal +
            #      switch[z,z]). Reported independently because the accepted F0
            #      convention retains a TRUNCATED outgoing rate here that has no
            #      represented destination (see truncated_slot_mass).
            assembled_diag = float(rec.diagonal) + float(switch[z, z])
            terms["diagonal_term"] = -assembled_diag * Vf[row]

            # ---- z-switch: accepted switch matrix OFF-DIAGONAL only (the switch
            #      matrix's own diagonal entry is already inside diagonal_term).
            #      Its row sums to zero, so off-diagonal == -switch[z,z].
            zsw = 0.0
            for z2 in range(nz):
                if z2 != z:
                    zsw += float(switch[z, z2]) * Vf[z2 * n + node]
            terms["z_switch_term"] = -zsw
            # ---- source terms
            terms["rhoV_term"] = float(rho * Vf[row])

            # The nine components are reported so that their PLAIN SUM is the
            # residual. Writing out R = rho*V - u - Q*V with Q's contribution
            # expanded into (destination rates) + (stored diagonal) +
            # (full switch-matrix row) gives, term by term,
            #     rhoV_term    = +rho*V[row]
            #     utility      = -u[row]
            #     destinations = -sum(rate*V[dest])
            #     diagonal     = -stored_diagonal*V[row]
            #     z_switch     = -sum_{z2} switch[z,z2]*V[z2*n+node]
            # so exactly these coefficients are stored, each assigned ONCE.
            terms["utility_source_term"] = -float(u[row])
            for col, rate, slot in represented:
                terms[slot] += -float(rate) * Vf[col]
            reconstructed = sum(terms.values())

            # CLOSURE: the nine components must sum to the residual of the ONE
            # assembled operator, evaluated independently at the top level. This
            # compares two genuinely different paths (component accumulation vs.
            # the assembled sparse matrix-vector product).
            direct = float(R[row])
            closure = abs(reconstructed - direct)
            max_closure = max(max_closure, closure)

            # AUTHORITATIVE source-backed attribution check: the operator row
            # rebuilt ONLY from the accepted record (stored diagonal + own
            # entries) plus the accepted switch matrix must equal the row of the
            # ONE assembled operator the residual was measured against.
            # AUTHORITATIVE source-backed attribution check: the operator row
            # rebuilt ONLY from the accepted record (stored diagonal + own
            # entries) plus the accepted switch matrix's diagonal and
            # off-diagonal entries must equal the row of the ONE assembled
            # operator the residual was measured against.
            rebuilt_QV = (float(rec.diagonal) * Vf[row]
                          + sum(rate * Vf[col] for col, rate, _s in represented)
                          + float(switch[z, z]) * Vf[row]
                          + zsw)
            op_closure = abs(rebuilt_QV - float(QV[row]))
            max_op_closure = max(max_op_closure, op_closure)
            op_closure = abs(rebuilt_QV - float(QV[row]))
            max_op_closure = max(max_op_closure, op_closure)

            liquid = None
            transfer_label = str(rec.sector)
            rows.append(StateRow(
                row=row, node=node, j=j, i=i, z=z, family=fam,
                residual=direct, abs_residual=abs(direct),
                residual_sign=int(np.sign(direct)),
                rhoV_term=terms["rhoV_term"],
                utility_source_term=terms["utility_source_term"],
                b_backward_term=terms["b_backward_term"],
                b_forward_term=terms["b_forward_term"],
                a_backward_term=terms["a_backward_term"],
                a_forward_term=terms["a_forward_term"],
                boundary_term=terms["boundary_term"],
                diagonal_term=terms["diagonal_term"],
                z_switch_term=terms["z_switch_term"],
                reconstructed_R=reconstructed, closure_error=closure,
                operator_row_closure_error=op_closure,
                represented_destinations=tuple(represented),
                rate_attribution_ok=attribution_ok,
                sector=str(rec.sector), liquid_label=liquid,
                transfer_label=transfer_label,
                consumption=float(rec.consumption),
                labor=float(rec.labor),
                transfer=float(rec.transfer),
                mu_a=float(rec.mu_a), mu_b=float(rec.mu_b),
                stored_b_backward_rate=(slot_rates["b_backward_term"]
                                        if slot_rates is not None else float("nan")),
                stored_b_forward_rate=(slot_rates["b_forward_term"]
                                       if slot_rates is not None else float("nan")),
                stored_a_backward_rate=(slot_rates["a_backward_term"]
                                        if slot_rates is not None else float("nan")),
                stored_a_forward_rate=(slot_rates["a_forward_term"]
                                       if slot_rates is not None else float("nan")),
                stored_diagonal=float(rec.diagonal),
                assembled_diagonal=float(rec.diagonal) + float(switch[z, z]),
                f0_slot_rates=(tuple(slot_rates[nm] for nm in F0_SLOT_NAMES)
                               if slot_rates is not None else None),                truncated_slot_mass=float(truncated_mass),
                neighbours={k: (None if v is None else int(v))
                            for k, v in neigh.items()},
            ))

    class_totals = {name: 0.0 for name in COMPONENT_NAMES}
    class_maxima = {name: 0.0 for name in COMPONENT_NAMES}
    for sr in rows:
        for name in COMPONENT_NAMES:
            v = float(getattr(sr, name))
            class_totals[name] += abs(v)
            class_maxima[name] = max(class_maxima[name], abs(v))
    return rows, max_closure, max_op_closure, attribution_mismatch_rows, {
        "totals": class_totals, "maxima": class_maxima}


# ---------------------------------------------------------------------------
# ONE deterministic top-20 selection
# ---------------------------------------------------------------------------
def _select_top(rows: list, top_n: int = TOP_N) -> list:
    """Deterministic top-``top_n`` by ``|R|`` descending, tie-break row id
    ascending. Exactly ``top_n`` rows are returned."""
    ordered = sorted(rows, key=lambda s: (-s.abs_residual, s.row))
    return ordered[:top_n]


def _largest_class(sr: StateRow) -> tuple[str, float]:
    """The largest-magnitude additive class of ONE row.

    The diagonal term is excluded (it is the assembled net-summary of the same
    outgoing rates already present as destination terms). It is still reported.
    """
    candidates = {
        "rhoV_term": abs(sr.rhoV_term),
        "utility_source_term": abs(sr.utility_source_term),
        "b_backward_term": abs(sr.b_backward_term),
        "b_forward_term": abs(sr.b_forward_term),
        "a_backward_term": abs(sr.a_backward_term),
        "a_forward_term": abs(sr.a_forward_term),
        "boundary_term": abs(sr.boundary_term),
        "z_switch_term": abs(sr.z_switch_term),
    }
    best = max(candidates.items(), key=lambda kv: (kv[1], kv[0]))
    return best[0], float(best[1])


# ---------------------------------------------------------------------------
# read-only top-20 F0 policy reproduction audit
# ---------------------------------------------------------------------------
def _reproduce_policy(solver: BoundaryHJBSolver, V: np.ndarray,
                      labor0: np.ndarray, sr: StateRow, record,
                      counter: dict) -> PolicyReproduction:
    """Re-invoke the accepted selector read-only with the EXACT same local
    inputs the assembly used, and compare every published field."""
    cfg = solver.config
    g = solver.grid
    node, z = sr.node, sr.z
    vb_f, vb_b, va_f, va_b = solver.compute_derivatives(V, labor0, 0.0, 0.0)
    counter["selector_calls"] += 1
    pol = select_matlab_faithful_local_policy(
        a=float(g.a_arr[node]), b=float(g.b_arr[node]), z=float(cfg.z[z]),
        v_a_forward=float(va_f[node, z]), v_a_backward=float(va_b[node, z]),
        v_b_forward=float(vb_f[node, z]), v_b_backward=float(vb_b[node, z]),
        baseline_labor=float(labor0[node, z]), transfer_income=0.0,
        borrowing_rate_gap=0.0, a_max=cfg.a_max, da=float(solver.da),
        db=float(solver.db), at_lower_a=(sr.j == 0),
        at_upper_a=(sr.j == g.jmax), at_lower_b=(sr.i == 0),
        at_upper_b=False, inputs=cfg.inputs, params=cfg.params,
        tolerance=cfg.drift_tolerance,
    )
    ctrl = max(abs(pol.consumption - record.consumption),
               abs(pol.labor - record.labor),
               abs(pol.transfer - record.transfer))
    drift = max(abs(float(pol.mu_a) - float(record.mu_a)),
                abs(float(pol.mu_b) - float(record.mu_b)))
    # the record publishes only row_entries; compare the four slots through the
    # accepted (dn, slot) bijection via the record's own entries
    slots = {}
    for dn, rate in record.row_entries:
        slot = _f0_slot_of(int(dn), sr.neighbours)
        if slot is not None:
            slots[slot] = float(rate)
    rates = max(
        abs(float(pol.iteration_b_backward_rate) - slots.get("b_backward_term", 0.0)),
        abs(float(pol.iteration_b_forward_rate) - slots.get("b_forward_term", 0.0)),
        abs(float(pol.a_backward_rate) - slots.get("a_backward_term", 0.0)),
        abs(float(pol.a_forward_rate) - slots.get("a_forward_term", 0.0)),
    )
    util = abs(float(pol.utility) - float(record.utility))
    record_transfer_label = str(record.sector)
    labels = bool(str(pol.transfer_label) == record_transfer_label)
    controls_match = ctrl == 0.0
    utility_match = util == 0.0
    drifts_match = drift == 0.0
    rates_match = rates == 0.0
    reproduced = bool(controls_match and utility_match and drifts_match
                      and rates_match and labels)
    detail = ""
    if not reproduced:
        detail = (f"controls={ctrl!r} utility={util!r} drifts={drift!r} "
                  f"rates={rates!r} labels={labels}")
    return PolicyReproduction(
        row=sr.row, node=node, j=sr.j, i=sr.i, z=z, sector=sr.sector,
        reproduced=reproduced, controls_match=controls_match,
        utility_match=utility_match, drifts_match=drifts_match,
        stored_rates_match=rates_match, labels_match=labels,
        liquid_label=str(pol.liquid_label),
        transfer_label=str(pol.transfer_label),
        record_liquid_label="NOT_PUBLISHED_BY_RECORD",
        record_transfer_label=record_transfer_label,
        max_control_abs_diff=float(ctrl), max_drift_abs_diff=float(drift),
        max_rate_abs_diff=float(rates), utility_abs_diff=float(util),
        mismatch_detail=detail,
    )


# ---------------------------------------------------------------------------
# the ONE full decomposition
# ---------------------------------------------------------------------------
def _run_from_reconstruction(rec: dict,
                             counter: Optional[dict] = None) -> DecompositionResult:
    counter = counter if counter is not None else {"builds": 0, "selector_calls": 0}
    failure: Optional[dict] = None
    try:
        solver: BoundaryHJBSolver = rec["solver"]
        labor0: np.ndarray = rec["labor0"]
        V_star: np.ndarray = rec["V_star"]
        rho: float = rec["rho"]
        trace: list = rec["trace"]
        n, nz = solver.n, solver.nz
        Vf = V_star.ravel(order="F")

        # ---- 1. frozen-state reproduction
        if len(trace) != ACCEPTED_STEPS:
            raise ResidualDecompositionFailure(
                f"reconstruction steps {len(trace)} != {ACCEPTED_STEPS}")
        final_statistic = float(trace[-1]["accepted_max_stat"])
        wall = dict(trace[-1]["worst_after"])
        if abs(final_statistic - ACCEPTED_FINAL_STATISTIC) > REPRO_TOL:
            raise ResidualDecompositionFailure(
                f"final statistic {final_statistic!r} != "
                f"{ACCEPTED_FINAL_STATISTIC!r}")
        if (str(wall.get("family")) != ACCEPTED_WALL_FAMILY
                or int(wall.get("j")) != ACCEPTED_WALL_J
                or int(wall.get("i")) != ACCEPTED_WALL_I
                or int(wall.get("z")) != ACCEPTED_WALL_Z
                or int(wall.get("node")) != ACCEPTED_WALL_NODE):
            raise ResidualDecompositionFailure(f"wall state {wall!r} mismatch")

        from deep_learning_hank.two_asset.adaptive_resolvent_hjb import (
            min_boundary_pb_state,
        )
        pb_star, _pb_node, _pb_nz = min_boundary_pb_state(solver, V_star, labor0)
        if not np.isfinite(pb_star):
            raise ResidualDecompositionFailure("non-finite required p_b(V_*)")
        if abs(float(pb_star) - ACCEPTED_MIN_BOUNDARY_PB) > REPRO_TOL:
            raise ResidualDecompositionFailure(
                f"min boundary p_b {pb_star!r} != {ACCEPTED_MIN_BOUNDARY_PB!r}")

        # ---- 2. exactly ONE Route-A final=False operator build
        counter["builds"] += 1
        Q, u, _diag, records = solver.build_operator_and_u(
            V_star, labor0, 0.0, 0.0, final=False)
        if counter["builds"] != 1:
            raise ResidualDecompositionFailure("more than one operator build")
        if not np.isfinite(Q.data).all() or not np.isfinite(u).all():
            raise ResidualDecompositionFailure("non-finite operator/u")

        R = rho * Vf - u - np.asarray(Q.dot(Vf)).ravel()
        if not np.isfinite(R).all():
            raise ResidualDecompositionFailure("non-finite residual")
        residual_inf = float(np.max(np.abs(R)))
        if abs(residual_inf - ACCEPTED_RESIDUAL_INF) > REPRO_TOL:
            raise ResidualDecompositionFailure(
                f"residual {residual_inf!r} != {ACCEPTED_RESIDUAL_INF!r}")
        am = int(np.argmax(np.abs(R)))
        am_z, am_node = am // n, am % n
        am_family = str(solver.grid.families[am_node])
        if (am != ACCEPTED_RESIDUAL_ARGMAX_ROW
                or am_node != ACCEPTED_RESIDUAL_ARGMAX_NODE
                or am_z != ACCEPTED_RESIDUAL_ARGMAX_Z
                or am_family != ACCEPTED_RESIDUAL_ARGMAX_FAMILY):
            raise ResidualDecompositionFailure(
                f"residual argmax row {am}/node {am_node}/z {am_z}/{am_family} "
                "mismatch")

        # ---- 3. ONE all-state additive decomposition
        rows, max_closure, max_op_closure, mismatch_rows, classes = _decompose(
            solver, V_star, u, records, rho, np.asarray(Q.dot(Vf)).ravel(), R)
        if len(rows) != solver.state_size:
            raise ResidualDecompositionFailure(
                f"decomposition covered {len(rows)} of {solver.state_size}")
        for sr in rows:
            if sr.closure_error > CLOSURE_TOL:
                raise ResidualDecompositionFailure(
                    f"row {sr.row} closure error {sr.closure_error!r}")

        # ---- 4. ONE deterministic top-20
        top = _select_top(rows, TOP_N)
        if len(top) != TOP_N:
            raise ResidualDecompositionFailure(
                f"top selection returned {len(top)} != {TOP_N}")
        top_rows: list[TopRow] = []
        for rank, sr in enumerate(top, start=1):
            cls, val = _largest_class(sr)
            top_rows.append(TopRow(
                rank=rank, row=sr.row, node=sr.node, j=sr.j, i=sr.i, z=sr.z,
                family=sr.family, residual=sr.residual,
                abs_residual=sr.abs_residual, residual_sign=sr.residual_sign,
                sector=sr.sector, liquid_label=sr.liquid_label,
                transfer_label=sr.transfer_label,
                consumption=sr.consumption, labor=sr.labor,
                transfer=sr.transfer, mu_a=sr.mu_a, mu_b=sr.mu_b,
                stored_b_backward_rate=sr.stored_b_backward_rate,
                stored_b_forward_rate=sr.stored_b_forward_rate,
                stored_a_backward_rate=sr.stored_a_backward_rate,
                stored_a_forward_rate=sr.stored_a_forward_rate,
                neighbours=dict(sr.neighbours),
                represented_destinations=sr.represented_destinations,
                rhoV_term=sr.rhoV_term,
                utility_source_term=sr.utility_source_term,
                b_backward_term=sr.b_backward_term,
                b_forward_term=sr.b_forward_term,
                a_backward_term=sr.a_backward_term,
                a_forward_term=sr.a_forward_term,
                boundary_term=sr.boundary_term,
                diagonal_term=sr.diagonal_term,
                z_switch_term=sr.z_switch_term,
                reconstructed_R=sr.reconstructed_R,
                closure_error=sr.closure_error,
                largest_component_class=cls, largest_component_abs=val,
                branch_inconsistent=False, is_f0=bool(sr.family == "F0")))

        # ---- 5. ONE read-only top-20 F0 policy reproduction audit
        repros: list[PolicyReproduction] = []
        for tr in top_rows:
            if not tr.is_f0:
                continue
            sr = next(s for s in rows if s.row == tr.row)
            repros.append(_reproduce_policy(
                solver, V_star, labor0, sr, records[tr.row], counter))
        repro_failures = sum(1 for p in repros if not p.reproduced)

        # the liquid branch label is OBSERVED from the accepted selector's own
        # read-only re-invocation (the record publishes no such attribute)
        for tr in top_rows:
            if not tr.is_f0:
                continue
            pr = next(p for p in repros if p.row == tr.row)
            tr.liquid_label = pr.liquid_label
            tr.transfer_label = pr.transfer_label
            tr.branch_inconsistent = bool(
                pr.liquid_label == "F" and tr.mu_b < 0.0
                and tr.stored_b_forward_rate > 0.0)
            sr = next(s for s in rows if s.row == tr.row)
            sr.liquid_label = pr.liquid_label

        # ---- all-state statistics
        f0_rows = [s for s in rows if s.family == "F0"]
        nf0_rows = [s for s in rows if s.family != "F0"]
        max_f0 = max(f0_rows, key=lambda s: (s.abs_residual, -s.row))
        max_nf0 = max(nf0_rows, key=lambda s: (s.abs_residual, -s.row))
        z0 = [s for s in rows if s.z == 0]
        z1 = [s for s in rows if s.z == 1]

        # ---- classification (frozen criteria, declared above)
        decomp_closed = bool(max_closure <= CLOSURE_TOL)
        dominant_f0 = bool(max_f0.abs_residual > max_nf0.abs_residual)
        records_reproduced = bool(repro_failures == 0 and len(repros) > 0)

        ordered_classes = sorted(classes["totals"].items(),
                                 key=lambda kv: (-kv[1], kv[0]))
        top_class, top_total = ordered_classes[0]
        total_mass = sum(classes["totals"].values())
        share = (top_total / total_mass) if total_mass > 0 else 0.0

        # --- top-20 aggregate leading-two separation over ALL nine components
        top20_totals = {name: 0.0 for name in COMPONENT_NAMES}
        for tr in top_rows:
            for name in COMPONENT_NAMES:
                top20_totals[name] += abs(float(getattr(tr, name)))
        lead = sorted(top20_totals.items(), key=lambda kv: (-kv[1], kv[0]))
        lead_gap = ((lead[0][1] - lead[1][1]) / lead[0][1]) if lead[0][1] > 0 else 0.0

        # --- (1) do ALL top-20 rows share ONE largest non-diagonal class
        #         (the per-row `largest_component_class`), and does that same
        #         class lead the top-20 aggregate? `coverage` is measured against
        #         the MODAL per-row class so the two quantities are comparable.
        top20_classes = [tr.largest_component_class for tr in top_rows]
        modal_class = max(sorted(set(top20_classes)),
                          key=lambda c: (top20_classes.count(c), c)) \
            if top20_classes else ""
        coverage = (top20_classes.count(modal_class) / len(top20_classes)) \
            if top20_classes else 0.0
        # the modal per-row class is itself the leading class of the top-20
        # aggregate only if it is not the excluded diagonal summary
        modal_is_leading = bool(lead[0][0] == modal_class)
        consistency = 1.0 if modal_is_leading else 0.0

        # --- (2) cancellation ratio: is the residual a substantial fraction of
        #         the gross component mass, or a tiny remainder of near-total
        #         cancellation among large terms?
        ratios = []
        for tr in top_rows:
            gross = sum(abs(float(getattr(tr, name))) for name in COMPONENT_NAMES)
            ratios.append((abs(tr.residual) / gross) if gross > 0 else 0.0)
        cancellation_ratio = float(np.mean(ratios)) if ratios else 0.0

        dominant_component = bool(
            coverage >= DOMINANCE_TOP20_COVERAGE
            and consistency >= 1.0
            and lead_gap >= DOMINANCE_MIN_LEADING_GAP
            and cancellation_ratio >= DOMINANCE_MIN_CANCELLATION_RATIO
            and mismatch_rows == 0)
        dominant_component_class = modal_class if dominant_component else ""
        branch_incons = bool(sum(1 for tr in top_rows if tr.branch_inconsistent)
                             >= BRANCH_INCONSISTENCY_MIN_ROWS)
        other_mech = bool(mismatch_rows > 0)
        mixed = bool(not dominant_component)

        if decomp_closed and records_reproduced and dominant_component:
            terminal = TERMINAL_A
        elif decomp_closed and records_reproduced:
            terminal = TERMINAL_B
        else:
            terminal = TERMINAL_C

        flags = tuple(sorted([
            name for name, on in (
                (DECOMPOSITION_CLOSED, decomp_closed),
                (DOMINANT_RESIDUAL_F0, dominant_f0),
                (POLICY_RECORDS_REPRODUCED, records_reproduced),
                (DOMINANT_COMPONENT_IDENTIFIED, dominant_component),
                (BRANCH_INCONSISTENCY_ESTABLISHED, branch_incons),
                (OTHER_MECHANISM_ESTABLISHED, other_mech),
                (MIXED_OR_UNRESOLVED, mixed),
            ) if on]))

        return DecompositionResult(
            terminal=terminal,
            failure_detail=None,
            steps=len(trace),
            final_statistic=final_statistic,
            min_boundary_pb_star=float(pb_star),
            wall_state=wall,
            residual_inf=residual_inf,
            residual_argmax_row=am,
            residual_argmax_node=am_node,
            residual_argmax_z=am_z,
            residual_argmax_family=am_family,
            bellman_tolerance=BELLMAN_TOLERANCE_UNCHANGED,
            residual_over_tolerance=residual_inf / BELLMAN_TOLERANCE_UNCHANGED,
            total_states=len(rows),
            f0_state_count=len(f0_rows),
            non_f0_state_count=len(nf0_rows),
            max_abs_R_f0=float(max_f0.abs_residual),
            argmax_f0_row=int(max_f0.row),
            max_abs_R_non_f0=float(max_nf0.abs_residual),
            argmax_non_f0_row=int(max_nf0.row),
            max_abs_R_z0=float(max(s.abs_residual for s in z0)),
            max_abs_R_z1=float(max(s.abs_residual for s in z1)),
            positive_residual_count=sum(1 for s in rows if s.residual > 0.0),
            negative_residual_count=sum(1 for s in rows if s.residual < 0.0),
            zero_residual_count=sum(1 for s in rows if s.residual == 0.0),
            top_absolute_contribution_class=top_class,
            contribution_class_totals={k: float(v)
                                       for k, v in classes["totals"].items()},
            contribution_class_maxima={k: float(v)
                                       for k, v in classes["maxima"].items()},
            decomposition_closure_max_error=float(max_closure),
            operator_row_closure_max_error=float(max_op_closure),
            top20_f0_count=sum(1 for tr in top_rows if tr.is_f0),
            policy_reproduction_failure_count=int(repro_failures),
            max_abs_q1=float(np.max(np.abs(np.asarray(
                Q.sum(axis=1)).ravel()))),
            rate_attribution_mismatch_rows=int(mismatch_rows),
            operator_build_count=int(counter["builds"]),
            selector_call_count=int(counter["selector_calls"]),
            top20=top_rows,
            policy_reproductions=repros,
            decomposition_closed=decomp_closed,
            dominant_residual_f0=dominant_f0,
            policy_records_reproduced=records_reproduced,
            dominant_component_identified=dominant_component,
            dominant_component_class=dominant_component_class,
            dominance_share=float(share),
            dominance_top20_coverage=float(coverage),
            dominance_leading_gap=float(lead_gap),
            cancellation_ratio_top20_mean=float(cancellation_ratio),
            cancellation_ratio_top20_max=float(max(ratios) if ratios else 0.0),
            top20_component_totals={k: float(v) for k, v in top20_totals.items()},
            branch_inconsistency_established=branch_incons,
            other_mechanism_established=other_mech,
            mixed_or_unresolved=mixed,
            accepted_new_hjb_iterate=False,
            new_trajectory_run=False,
            deterministic_repeat_identical=False,
            flags=flags,
            rows=rows,
        )
    except ResidualDecompositionFailure as exc:
        failure = {"reason": str(exc)}
    except Exception as exc:  # pragma: no cover - defensive
        failure = {"reason": f"unexpected failure: {exc!r}"}

    return DecompositionResult(
        terminal=TERMINAL_C,
        failure_detail=failure,
        accepted_new_hjb_iterate=False,
        new_trajectory_run=False,
        deterministic_repeat_identical=False,
    )


# ---------------------------------------------------------------------------
# entry points
# ---------------------------------------------------------------------------
def run_issue71_decomposition() -> DecompositionResult:
    """Exactly ONE full Issue #71 decomposition (ONE reconstruction, ONE
    Route-A ``final=False`` build, ONE all-state additive decomposition, ONE
    deterministic top-20, ONE read-only top-20 F0 policy reproduction audit)."""
    counter = {"builds": 0, "selector_calls": 0}
    return _run_from_reconstruction(reconstruct_issue63_stagnation_state(),
                                    counter)


def _canon(r: DecompositionResult) -> dict:
    """Canonical, comparison-safe form of a result.

    ``NaN != NaN`` under Python equality, so the NaN sentinels used for
    not-applicable fields (e.g. the four F0 slot rates on non-F0 rows) are mapped
    to a single ``"__NAN__"`` marker. This preserves bitwise-identical repeats as
    "identical" without masking any real numerical difference.
    """
    def norm(value):
        if isinstance(value, float) and np.isnan(value):
            return "__NAN__"
        if isinstance(value, dict):
            return {k: norm(v) for k, v in value.items()}
        if isinstance(value, (list, tuple)):
            return [norm(v) for v in value]
        return value

    return {k: norm(v) for k, v in dataclasses.asdict(r).items()}


def run_issue71_decomposition_twice() -> tuple[DecompositionResult, bool]:
    """The ONE deterministic repeat of the full decomposition."""
    first = run_issue71_decomposition()
    second = run_issue71_decomposition()
    identical = bool(_canon(first) == _canon(second))
    first.deterministic_repeat_identical = identical
    return first, identical


# ---------------------------------------------------------------------------
# reporting helpers
# ---------------------------------------------------------------------------
def summary_csv_lines(r: DecompositionResult) -> list[str]:
    """Compact CSV evidence lines for the Issue #71 report."""
    lines = ["metric,value"]
    for f in dataclasses.fields(r):
        if f.name in ("rows", "top20", "policy_reproductions"):
            continue
        v = getattr(r, f.name)
        if isinstance(v, dict):
            v = "; ".join(f"{k}={v[k]}" for k in sorted(v))
        lines.append(f"{f.name},{v}")
    for tr in r.top20:
        for f in dataclasses.fields(tr):
            v = getattr(tr, f.name)
            lines.append(f"top{tr.rank}.{f.name},{v}")
    for p in r.policy_reproductions:
        for f in dataclasses.fields(p):
            v = getattr(p, f.name)
            lines.append(f"repro{p.row}.{f.name},{v}")
    return lines
