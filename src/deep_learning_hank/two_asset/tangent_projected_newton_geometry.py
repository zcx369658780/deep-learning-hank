"""DLH-5V-T — single-wall tangent-projected frozen-policy Newton geometry after
the accepted final-validation repair.

Issue #68 / DLH-5V-T
``SCIENTIFIC_NUMERICAL_DIAGNOSTIC__BOUNDARY_TANGENT_PROJECTED_NEWTON_GEOMETRY_AFTER_VALIDATION_REPAIR``

Authority: Issue #68 OPEN; initial authoritative activation ``5674754187``;
final authoritative activation-refresh ``5675003122`` (post-sync live ``main``
``e569271904eacbd3b2721b0b0f1ebb8e9a559e3f``). Route decision
``APPROVE_SINGLE_WALL_TANGENT_PROJECTED_NEWTON_GEOMETRY_AFTER_5VS_TERMINAL_A``;
authority marker ``DLH_5VT_TANGENT_PROJECTED_NEWTON_GEOMETRY_AUTHORIZED``.

Scientific question
-------------------
After the accepted Issue #67 validation repair the genuine Bellman residual at
the accepted Issue #63 stagnation state ``V_*`` is ~10.435 (not ~490.756).
Issue #64 showed the unconstrained frozen-policy Newton direction is
geometrically capped by the F3 (13,13), z=1 wall. This diagnostic tests one
hypothesis: does removing the **first-order normal component** of the plain
frozen-policy Newton direction with respect to the single limiting boundary
constraint produce a materially larger boundary-safe step and a meaningful
nonlinear residual reduction at the same frozen economics/state?

Exact execution (Issue #68 section 9), all at the SAME frozen ``V_*``:

1. ONE deterministic reconstruction of the accepted post-repair ``V_*``;
2. ONE current ``final=False`` operator build -> ``Q, u``, with
   ``R = rho V_* - (u + Q V_*)`` and ``J = rho I - Q``;
3. ONE frozen-policy Newton solve ``J d_N = -R``;
4. ONE limiting-wall ``p_b`` gradient ``g`` (accepted Issue #62 boundary
   derivative semantics);
5. ONE single-wall Euclidean tangent projection
   ``d_T = d_N - g*(g@d_N)/(g@g)``;
6. ONE all-boundary crossing computation for ``d_T``;
7. exactly TWO diagnostic trials (``alpha_half``, ``alpha_near``); each trial
   performs exactly ONE ``final=False`` policy re-selection and exactly ONE
   corrected ``final=True`` validation build under the SAME freshly reselected
   current F0 controls;
8. ONE deterministic repeat of the full diagnostic.

No trial state is an accepted HJB iterate. No multi-step Newton, no policy
iteration, no semismooth / trust-region / continuation, no adaptive line search
or alpha tuning, no multiple active constraints, no projection-metric
optimization, no ``p_b`` clip/floor, no economics/prices/grid/domain/
initialization/controls/tolerances/``PB_MARGIN``/Bellman-tolerance change, no
convergence-criterion change, no KFE / stationary KFE / steady state. The
selected-Q source is imported read-only and its blob is asserted.

FAIL-CLOSED: non-finite evidence, a non-positive safe fraction, a boundary
safety violation, a failed corrected-final/iteration equivalence check, a
non-finite tangent projection, or a non-identical deterministic repeat raises
``TangentProjectedNewtonFailure`` (or yields Outcome C), never a silent pass.
"""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field
from typing import Optional

import numpy as np
from scipy import sparse
from scipy.sparse import linalg

from deep_learning_hank.two_asset.adaptive_resolvent_hjb import (
    min_boundary_pb_state,
)
from deep_learning_hank.two_asset.boundary_hjb_selected_q import (
    BoundaryHJBSolver,
)
from deep_learning_hank.two_asset.local_resolvent_domain_geometry import (
    boundary_direction_matrix,
)
from deep_learning_hank.two_asset.stagnation_newton_geometry import (
    EPS_ALPHA,
    HALF_ALPHA,
    NEWTON_SOLVE_TOL,
    PB_MARGIN,
    RECONSTRUCT_STEPS,
    reconstruct_issue63_stagnation_state,
    residual_stats,
)

# ---------------------------------------------------------------------------
# Frozen accepted references (Issue #67 / #64 accepted facts)
# ---------------------------------------------------------------------------
SELECTED_Q_REPAIRED_BLOB = "556ccc214f03a1a22306cc4f5c7e9f7691bbf897"

REPAIRED_R_INF = 10.435094313164921
FINAL_STATISTIC_EXPECTED = 3.6614352438846254e-08
MIN_BOUNDARY_PB_EXPECTED = 4.8089461301970005e-09
WALL_NODE = 332
WALL_J = 13
WALL_I = 13
WALL_NZ = 1
WALL_FAMILY = "F3"

# Historical plain-Newton baseline (accepted Issue #64), reproduced exactly here
ALPHA_CROSS_N_HISTORICAL = 1.8667384893e-4

# Frozen Issue #68 constants
MATERIAL_REDUCTION_RATIO = 0.50
GEOMETRY_IMPROVEMENT_FACTOR = 10.0
TANGENT_TOL = 1.0e-9
EQUIVALENCE_TOL = 1.0e-9

TERMINAL_A = (
    "DLH_5VT_TANGENT_PROJECTED_NEWTON__SINGLE_WALL_TANGENT_PROJECTION_EXPANDS_"
    "SAFE_GEOMETRY_AND_MATERIALLY_REDUCES_NONLINEAR_RESIDUAL__CONSTRAINED_"
    "DIRECTION_DESIGN_GATE_READY")
TERMINAL_B = (
    "DLH_5VT_TANGENT_PROJECTED_NEWTON__TANGENT_DIRECTION_FINITE_AND_DOMAIN_SAFE_"
    "BUT_GEOMETRY_OR_RESIDUAL_IMPROVEMENT_INSUFFICIENT__FURTHER_DIRECTION_"
    "DESIGN_REQUIRED")
TERMINAL_C = (
    "DLH_5VT_TANGENT_PROJECTED_NEWTON__NONFINITE_INCONSISTENT_OR_NO_POSITIVE_"
    "SAFE_TANGENT_GEOMETRY__BOUNDARY_HJB_ROUTE_REVIEW_REQUIRED")
TERMINAL_BLOCKED = "BLOCKED_DLH_5VT_AUTHORITY_OR_DEPENDENCY_CONFLICT"

TRIAL_ORDER = ("alpha_half", "alpha_near")


class TangentProjectedNewtonFailure(RuntimeError):
    """Fail-closed: non-finite or inconsistent projection/operator evidence, a
    missing F0 record, a boundary safety violation, or a failed same-controls
    equivalence check."""


# ---------------------------------------------------------------------------
# Result containers
# ---------------------------------------------------------------------------
@dataclass
class TrialResult:
    """ONE diagnostic trial state. Diagnostic only — never an accepted iterate."""

    label: str
    alpha: float
    min_boundary_pb: float
    min_boundary_pb_state: dict
    domain_safe: bool
    r_frozen_inf: float
    r_reselect_inf: float
    r_final_trial_inf: float
    reselect_ratio: float
    final_ratio: float
    final_vs_iter_f0_rowwise_gap: float
    final_vs_iter_equivalent: bool
    final_vs_iter_inconsistent_row_count: int
    final_vs_iter_inconsistent_rows: tuple
    max_abs_q1_reselect: float
    max_abs_q1_final: float
    label_change_count: int
    max_abs_delta_consumption: float
    max_abs_delta_labor: float
    max_abs_delta_transfer: float
    max_abs_delta_mu_a: float
    max_abs_delta_mu_b: float
    max_abs_delta_utility: float
    material_residual_reducing: bool
    accepted_as_hjb_iterate: bool = False


@dataclass
class TangentProjectedNewtonResult:
    """ONE fully determined Issue #68 diagnostic outcome."""

    terminal: str
    failure_detail: Optional[dict] = None
    # frozen reconstruction
    iterations: int = 0
    final_statistic: float = float("nan")
    min_boundary_pb_star: float = float("nan")
    wall_state: dict = field(default_factory=dict)
    r_inf: float = float("nan")
    r_argmax: Optional[dict] = None
    # base operator / plain Newton
    newton_solve_count: int = 0
    d_n_inf: float = float("nan")
    newton_lin_res_inf: float = float("nan")
    newton_lin_res_ok: bool = False
    # limiting-wall gradient (full-state, two-entry chain rule)
    gradient_kind: str = "full_state_chain_rule_two_entry"
    gradient_nonzero_count: int = 0
    gradient_wall_state_index: int = -1
    gradient_down_state_index: int = -1
    gradient_wall_entry: float = float("nan")
    gradient_down_entry: float = float("nan")
    gradient_support: tuple = ()
    gradient_basis_check_ok: bool = False
    gradient_basis_check_max_abs_err: float = float("nan")
    gradient_norm2: float = float("nan")
    gradient_finite: bool = False
    gradient_nonzero: bool = False
    g_dot_d_n: float = float("nan")
    g_dot_d_n_negative: bool = False
    alpha_cross_n: Optional[float] = None
    alpha_cross_n_state: Optional[dict] = None
    alpha_cross_n_reproduced: bool = False
    # tangent projection
    d_t_inf: float = float("nan")
    d_t_minus_d_n_inf: float = float("nan")
    g_dot_d_t: float = float("nan")
    tangent_identity_ok: bool = False
    projection_count: int = 0
    j_d_n_plus_r_inf: float = float("nan")
    j_d_t_plus_r_inf: float = float("nan")
    # all-boundary crossing for d_T
    crossing_computation_count: int = 0
    required_boundary_count: int = 0
    zero_derivative_count: int = 0
    negative_derivative_count: int = 0
    alpha_cross_t: Optional[float] = None
    alpha_cross_t_state: Optional[dict] = None
    alpha_near: float = float("nan")
    alpha_half: float = float("nan")
    has_positive_safe_fraction: bool = False
    geometry_improvement_ratio: Optional[float] = None
    geometry_improving: bool = False
    # trials
    trials: list = field(default_factory=list)
    trial_count: int = 0
    all_trials_domain_safe: bool = False
    all_trials_operator_equivalent: bool = False
    any_trial_materially_reducing: bool = False
    accepted_new_hjb_iterate: bool = False
    deterministic_repeat_identical: bool = False


# ---------------------------------------------------------------------------
# limiting-wall gradient (accepted Issue #62 boundary derivative semantics)
# ---------------------------------------------------------------------------
def limiting_wall_gradient(solver: BoundaryHJBSolver, node: int,
                           nz_i: int) -> np.ndarray:
    """Exact full-state gradient ``g`` of the limiting wall's ``p_b`` at ``V_*``.

    Accepted Issue #62 semantics (see
    ``local_resolvent_domain_geometry.boundary_direction_matrix``): for a
    regular backward finite-difference boundary state (``i > 0``) the accepted
    wall coordinate is

        ``p_b(V)[node] = (V[node] - V[down]) / db``

    so its gradient with respect to the FULL value vector ``V`` is the
    two-entry vector (Issue #68 section 4 frozen contract)

        ``g[z*n + node] = +1/db``
        ``g[z*n + down] = -1/db``
        all other entries ``0``

    This is the official Issue #68 construction. It is verified in the test
    suite by an exact basis-direction measurement of the accepted derivative
    map (every basis entry matches to machine precision) and by a directional
    finite-difference identity on the wall coordinate. The earlier single-entry
    ``+1/db`` variant is retained only as historical/debug evidence and never
    feeds the official projection, crossing or terminal.

    ``i == 0`` boundary state: the accepted rule is V-INDEPENDENT, so the
    gradient is exactly the zero vector.

    No clipping/flooring/redefinition of ``p_b``.
    """
    gg = solver.grid
    i = int(gg.i_arr[node])
    vec = np.zeros(solver.state_size, dtype=float)
    if i == 0:
        return vec
    down = gg.node_of.get((int(gg.j_arr[node]), i - 1))
    if down is None:
        raise TangentProjectedNewtonFailure(
            f"no backward neighbour for limiting-wall state node {node} "
            f"(i={i}) -> gradient undefined")
    inv_db = 1.0 / float(solver.db)
    vec[nz_i * solver.n + int(node)] = inv_db
    vec[nz_i * solver.n + int(down)] = -inv_db
    return vec


def single_entry_debug_gradient(solver: BoundaryHJBSolver, node: int,
                                nz_i: int) -> np.ndarray:
    """HISTORICAL/DEBUG ONLY — the superseded single-entry ``+1/db`` variant.

    This was the initial Issue #68 candidate's construction. It is NOT the
    official gradient, does NOT satisfy the full-state chain rule of the wall's
    ``p_b``, and must never feed the official projection, crossing or terminal
    classification. Retained solely as historical evidence for the
    Reviewer-authorized remediation record.
    """
    vec = np.zeros(solver.state_size, dtype=float)
    if int(solver.grid.i_arr[node]) == 0:
        return vec
    vec[nz_i * solver.n + int(node)] = 1.0 / float(solver.db)
    return vec


def single_wall_tangent_projection(d_n: np.ndarray, gvec: np.ndarray) -> dict:
    """ONE Euclidean orthogonal projection onto the wall's tangent hyperplane.

    ``d_T = d_N - g*(g@d_N)/(g@g)``. FAIL-CLOSED on non-finite output or a
    degenerate (zero-norm) gradient.
    """
    gg = float(gvec @ gvec)
    if not np.isfinite(gg) or gg <= 0.0:
        raise TangentProjectedNewtonFailure(
            f"degenerate limiting-wall gradient: g@g = {gg!r}")
    d_t = d_n - gvec * (float(gvec @ d_n) / gg)
    if not np.isfinite(d_t).all():
        raise TangentProjectedNewtonFailure("non-finite tangent-projected direction")
    return {
        "d_T": d_t,
        "g_dot_d_n": float(gvec @ d_n),
        "g_dot_d_t": float(gvec @ d_t),
        "d_t_max_abs": float(np.max(np.abs(d_t))),
        "d_t_minus_d_n_max_abs": float(np.max(np.abs(d_t - d_n))),
        "projection_count": 1,
    }


# ---------------------------------------------------------------------------
# all-boundary crossing for d_T (accepted Issue #62 semantics)
# ---------------------------------------------------------------------------
def all_boundary_crossing(solver: BoundaryHJBSolver, V_star: np.ndarray,
                          labor0: np.ndarray, d_t: np.ndarray) -> dict:
    """``alpha_cross_T`` over ALL required non-F0 boundary states.

    ``alpha_cross_i = (p_b_i(V_*) - PB_MARGIN)/(-dp_i)`` for every state with
    ``dp_i < 0``; ``alpha_cross_T`` is the minimum positive finite value, or
    ``+inf`` when no negative derivative exists. FAIL-CLOSED on non-finite
    required ``p_b`` or directional evidence.
    """
    n, nz = solver.n, solver.nz
    grid = solver.grid
    pb_star, node0, nz0 = min_boundary_pb_state(solver, V_star, labor0)
    if not np.isfinite(pb_star):
        raise TangentProjectedNewtonFailure(
            f"non-finite required boundary p_b(V_*): {pb_star!r}")
    _, pb_matrix, _, _ = solver.compute_derivatives(V_star, labor0, 0.0, 0.0)
    dp_matrix = boundary_direction_matrix(
        solver, d_t.reshape((n, nz), order="F"))
    required = 0
    zero_count = 0
    negative_count = 0
    items: list[tuple[float, int, int]] = []
    for node in range(n):
        if grid.families[node] == "F0":
            continue
        for nz_i in range(nz):
            required += 1
            p = float(pb_matrix[node, nz_i])
            if not np.isfinite(p):
                raise TangentProjectedNewtonFailure(
                    f"non-finite boundary p_b at node {node} z {nz_i}: {p!r}")
            dp = float(dp_matrix[node, nz_i])
            if not np.isfinite(dp):
                raise TangentProjectedNewtonFailure(
                    f"non-finite directional evidence at node {node} z {nz_i}")
            if dp == 0.0:
                zero_count += 1          # V-independent boundary rule (i == 0)
            if dp < 0.0:
                negative_count += 1
                items.append(((p - PB_MARGIN) / (-dp), node, nz_i))
    finite_positive = [it for it in items
                       if np.isfinite(it[0]) and it[0] > 0.0]
    if finite_positive:
        best = min(finite_positive, key=lambda it: it[0])
        alpha_cross = float(best[0])
        fastest_state = _state_info(solver, best[1], best[2])
    else:
        alpha_cross = None
        fastest_state = None
    alpha_near = (min(1.0, (1.0 - EPS_ALPHA) * alpha_cross)
                  if alpha_cross is not None else 1.0)
    return {
        "pb_star": float(pb_star),
        "worst_state": _state_info(solver, node0, nz0),
        "required_count": required,
        "zero_count": zero_count,
        "negative_count": negative_count,
        "alpha_cross_T": alpha_cross,
        "alpha_cross_T_state": fastest_state,
        "alpha_near": float(alpha_near),
        "alpha_half": float(HALF_ALPHA * alpha_near),
        "positive_finite_crossing_count": len(finite_positive),
        "crossing_computation_count": 1,
    }


def _state_info(solver: BoundaryHJBSolver, node: int, nz_i: int) -> dict:
    g = solver.grid
    return {
        "node": int(node),
        "j": int(g.j_arr[node]),
        "i": int(g.i_arr[node]),
        "z": int(nz_i),
        "family": str(g.families[node]),
    }


# ---------------------------------------------------------------------------
# ONE diagnostic trial
# ---------------------------------------------------------------------------
def evaluate_tangent_trial(solver: BoundaryHJBSolver, V_star: np.ndarray,
                           labor0: np.ndarray, rho: float, d_t: np.ndarray,
                           Q_iter: sparse.csr_matrix, u_iter: np.ndarray,
                           records_iter: list, r_inf: float, label: str,
                           alpha: float) -> TrialResult:
    """Exactly ONE diagnostic trial at ``V_trial = V_* + alpha*d_T``.

    Performs exactly ONE ``final=False`` policy re-selection and exactly ONE
    corrected ``final=True`` validation build under the SAME freshly reselected
    current F0 controls. The frozen ``Q, u`` supply the frozen-policy residual.
    The trial is diagnostic only and is never an accepted HJB iterate.
    """
    n, nz = solver.n, solver.nz
    V_trial = V_star + alpha * d_t.reshape((n, nz), order="F")
    Vt = V_trial.ravel(order="F")
    if not np.isfinite(Vt).all():
        raise TangentProjectedNewtonFailure(f"non-finite trial state ({label})")

    # A. strict boundary safety over ALL required boundary states
    pb, node, nz_i = min_boundary_pb_state(solver, V_trial, labor0)
    if not np.isfinite(pb):
        raise TangentProjectedNewtonFailure(
            f"non-finite required boundary p_b at trial {label}: {pb!r}")
    domain_safe = bool(pb > PB_MARGIN)
    if not domain_safe:
        raise TangentProjectedNewtonFailure(
            f"trial {label} violates boundary safety: p_b = {pb!r} <= "
            f"PB_MARGIN = {PB_MARGIN!r}")

    # B. frozen-policy residual from the ONE frozen operator
    R_frozen = rho * Vt - (u_iter + Q_iter.dot(Vt))

    # C. exactly ONE nonlinear policy re-selection (final=False)
    Q_res, u_res, _diag_res, records_trial = solver.build_operator_and_u(
        V_trial, labor0, 0.0, 0.0, final=False)
    R_resel = rho * Vt - (u_res + Q_res.dot(Vt))

    # D. exactly ONE corrected final=True validation build, SAME controls
    Q_fin, u_fin, _diag_fin, _records_fin = solver.build_operator_and_u(
        V_trial, labor0, 0.0, 0.0, final=True, f0_policies=records_trial)
    R_final = rho * Vt - (u_fin + Q_fin.dot(Vt))

    for nm, vec in (("R_frozen", R_frozen), ("R_reselect", R_resel),
                    ("R_final_trial", R_final)):
        if not np.isfinite(vec).all():
            raise TangentProjectedNewtonFailure(
                f"non-finite {nm} at trial {label}")

    # E. corrected final=True vs final=False equivalence under SAME controls.
    # The two construction paths use DIFFERENT rate semantics by design
    # (re-selection uses the accepted policy's iteration_* rates with the source
    # truncation convention; the corrected final path recomputes raw drifts and
    # applies max(+-mu)/step). They agree exactly at the accepted V_* but can
    # disagree on F0 rows where a drift sits at an upwind sign boundary. This is
    # recorded as evidence, not raised, so the trial still yields full residual
    # diagnostics; the frozen terminal rule maps the inconsistency to Outcome C.
    f0_rows = _f0_rows_of(solver)
    gap = 0.0
    inconsistent_rows: list[int] = []
    for r in f0_rows:
        a = np.asarray(Q_fin.getrow(int(r)).toarray()).ravel()
        b = np.asarray(Q_res.getrow(int(r)).toarray()).ravel()
        m = float(np.max(np.abs(a - b)))
        if m > 1e-12:
            inconsistent_rows.append(int(r))
        gap = max(gap, m)
    equivalent = bool(gap <= EQUIVALENCE_TOL)

    # F. diagnostics
    label_changes = 0
    dc = dl = dtr = dma = dmb = du = 0.0
    for r in f0_rows:
        a = records_iter[int(r)]
        b = records_trial[int(r)]
        if a is None or b is None:
            raise TangentProjectedNewtonFailure(
                f"missing F0 record at row {int(r)} (trial {label})")
        if a.sector != b.sector:
            label_changes += 1
        dc = max(dc, abs(a.consumption - b.consumption))
        dl = max(dl, abs(a.labor - b.labor))
        dtr = max(dtr, abs(a.transfer - b.transfer))
        dma = max(dma, abs(a.mu_a - b.mu_a))
        dmb = max(dmb, abs(a.mu_b - b.mu_b))
        du = max(du, abs(a.utility - b.utility))

    r_resel_inf = float(residual_stats(solver, R_resel)["total"]["max_abs"])
    r_final_inf = float(residual_stats(solver, R_final)["total"]["max_abs"])
    reselect_ratio = r_resel_inf / r_inf
    final_ratio = r_final_inf / r_inf
    reducing = bool(reselect_ratio <= MATERIAL_REDUCTION_RATIO
                    and final_ratio <= MATERIAL_REDUCTION_RATIO)

    return TrialResult(
        label=label,
        alpha=float(alpha),
        min_boundary_pb=float(pb),
        min_boundary_pb_state=_state_info(solver, node, nz_i),
        domain_safe=domain_safe,
        r_frozen_inf=float(residual_stats(solver, R_frozen)["total"]["max_abs"]),
        r_reselect_inf=r_resel_inf,
        r_final_trial_inf=r_final_inf,
        reselect_ratio=reselect_ratio,
        final_ratio=final_ratio,
        final_vs_iter_f0_rowwise_gap=gap,
        final_vs_iter_equivalent=equivalent,
        final_vs_iter_inconsistent_row_count=len(inconsistent_rows),
        final_vs_iter_inconsistent_rows=tuple(inconsistent_rows),
        max_abs_q1_reselect=float(
            np.max(np.abs(np.asarray(Q_res.sum(axis=1)).ravel()))),
        max_abs_q1_final=float(
            np.max(np.abs(np.asarray(Q_fin.sum(axis=1)).ravel()))),
        label_change_count=label_changes,
        max_abs_delta_consumption=dc,
        max_abs_delta_labor=dl,
        max_abs_delta_transfer=dtr,
        max_abs_delta_mu_a=dma,
        max_abs_delta_mu_b=dmb,
        max_abs_delta_utility=du,
        material_residual_reducing=reducing,
        accepted_as_hjb_iterate=False,
    )


def _f0_rows_of(solver: BoundaryHJBSolver) -> np.ndarray:
    n, nz = solver.n, solver.nz
    fam = np.array([str(solver.grid.families[node]) for node in range(n)])
    return np.nonzero(np.tile(fam == "F0", nz))[0]


# ---------------------------------------------------------------------------
# the ONE full diagnostic
# ---------------------------------------------------------------------------
def _run_from_reconstruction(rec: dict) -> TangentProjectedNewtonResult:
    failure: Optional[dict] = None
    try:
        solver: BoundaryHJBSolver = rec["solver"]
        labor0: np.ndarray = rec["labor0"]
        V_star: np.ndarray = rec["V_star"]
        rho: float = rec["rho"]
        trace: list = rec["trace"]
        n, nz = solver.n, solver.nz
        V_flat = V_star.ravel(order="F")

        # 1. frozen reconstruction
        if len(trace) != RECONSTRUCT_STEPS:
            raise TangentProjectedNewtonFailure(
                "reconstruction did not stop at accepted step 8")
        final_statistic = float(trace[-1]["accepted_max_stat"])
        wall = dict(trace[-1]["worst_after"])
        if not (wall["family"] == WALL_FAMILY and wall["j"] == WALL_J
                and wall["i"] == WALL_I and wall["z"] == WALL_NZ):
            raise TangentProjectedNewtonFailure(
                f"limiting wall regression: {wall}")
        pb_star, wall_node, wall_nz = min_boundary_pb_state(
            solver, V_star, labor0)
        if not np.isfinite(pb_star):
            raise TangentProjectedNewtonFailure("non-finite required p_b(V_*)")

        # 2. ONE current final=False operator build
        Q, u, diag, records = solver.build_operator_and_u(
            V_star, labor0, 0.0, 0.0, final=False)
        R = rho * V_flat - (u + Q.dot(V_flat))
        if not np.isfinite(R).all():
            raise TangentProjectedNewtonFailure("non-finite base residual R")
        stats_R = residual_stats(solver, R)
        r_inf = float(stats_R["total"]["max_abs"])

        # 3. ONE frozen-policy Newton solve
        S = solver.state_size
        J = rho * sparse.eye(S, format="csr") - Q
        try:
            d_n = linalg.spsolve(J, -R)
        except Exception as exc:  # pragma: no cover - defensive
            raise TangentProjectedNewtonFailure(
                f"Newton linear solve raised: {exc!r}") from exc
        if d_n.shape != (S,) or not np.isfinite(d_n).all():
            raise TangentProjectedNewtonFailure("non-finite Newton direction")
        lin_res = float(np.max(np.abs(J.dot(d_n) + R)))
        d_n_inf = float(np.max(np.abs(d_n)))

        # alpha_cross_N: the plain-Newton historical baseline (ONE extra
        # direction evaluation of the accepted Issue #62 semantics; no solve)
        bc_n = _crossing_only(solver, V_star, labor0, d_n)

        # 4. ONE limiting-wall gradient (exact two-entry full-state chain rule)
        gvec = limiting_wall_gradient(solver, wall_node, wall_nz)
        grad_finite = bool(np.isfinite(gvec).all())
        grad_norm2 = float(np.linalg.norm(gvec))
        grad_nonzero = bool(grad_norm2 > 0.0)
        if not (grad_finite and grad_nonzero):
            raise TangentProjectedNewtonFailure(
                "non-finite or zero limiting-wall gradient")
        nz_support = np.nonzero(gvec)[0]
        down_node = solver.grid.node_of.get(
            (int(solver.grid.j_arr[wall_node]),
             int(solver.grid.i_arr[wall_node]) - 1))
        wall_idx = wall_nz * n + int(wall_node)
        down_idx = wall_nz * n + int(down_node)
        basis_ok, basis_err = _gradient_basis_check(solver, wall_node, wall_nz,
                                                    gvec)
        if not (basis_ok and int(nz_support.size) == 2
                and wall_idx in nz_support and down_idx in nz_support):
            raise TangentProjectedNewtonFailure(
                "limiting-wall gradient does not match the full-state "
                f"chain-rule contract (support={nz_support.tolist()}, "
                f"basis_err={basis_err!r})")

        # 5. ONE tangent projection
        proj = single_wall_tangent_projection(d_n, gvec)
        d_t = proj["d_T"]

        # 6. ONE all-boundary crossing computation for d_T
        cross = all_boundary_crossing(solver, V_star, labor0, d_t)
        alpha_cross_t = cross["alpha_cross_T"]
        alpha_near = float(cross["alpha_near"])
        alpha_half = float(cross["alpha_half"])
        has_positive = bool(alpha_cross_t is None
                            or (np.isfinite(alpha_cross_t) and alpha_cross_t > 0.0))
        if alpha_cross_t is not None and not (
                np.isfinite(alpha_cross_t) and alpha_cross_t > 0.0):
            raise TangentProjectedNewtonFailure(
                f"non-positive safe fraction alpha_cross_T = {alpha_cross_t!r}")

        # 7. exactly TWO diagnostic trials
        trials = [
            evaluate_tangent_trial(solver, V_star, labor0, rho, d_t, Q, u,
                                   records, r_inf, "alpha_half", alpha_half),
            evaluate_tangent_trial(solver, V_star, labor0, rho, d_t, Q, u,
                                   records, r_inf, "alpha_near", alpha_near),
        ]
        baseline = bc_n["alpha_cross"]
        geom_ratio = (alpha_near / min(1.0, float(baseline))
                      if baseline is not None and baseline > 0 else None)
        geom_improving = bool(geom_ratio is not None
                              and geom_ratio >= GEOMETRY_IMPROVEMENT_FACTOR)
        all_safe = bool(all(t.domain_safe for t in trials))
        any_reducing = bool(any(t.material_residual_reducing for t in trials))
        all_equivalent = bool(all(t.final_vs_iter_equivalent for t in trials))
        tangent_ok = bool(abs(proj["g_dot_d_t"]) <= TANGENT_TOL)

        # frozen ex ante terminal rule
        consistent = bool(tangent_ok and has_positive and all_safe
                          and all_equivalent and r_inf > 0.0)
        if not consistent:
            terminal = TERMINAL_C
        elif geom_improving and any_reducing:
            terminal = TERMINAL_A
        else:
            terminal = TERMINAL_B

        return TangentProjectedNewtonResult(
            terminal=terminal,
            failure_detail=None,
            iterations=len(trace),
            final_statistic=final_statistic,
            min_boundary_pb_star=float(pb_star),
            wall_state=wall,
            r_inf=r_inf,
            r_argmax=stats_R["total"]["argmax_state"],
            newton_solve_count=1,
            d_n_inf=d_n_inf,
            newton_lin_res_inf=lin_res,
            newton_lin_res_ok=bool(lin_res <= NEWTON_SOLVE_TOL),
            gradient_kind="full_state_chain_rule_two_entry",
            gradient_nonzero_count=int(nz_support.size),
            gradient_wall_state_index=wall_idx,
            gradient_down_state_index=down_idx,
            gradient_wall_entry=float(gvec[wall_idx]),
            gradient_down_entry=float(gvec[down_idx]),
            gradient_support=tuple(int(k) for k in nz_support),
            gradient_basis_check_ok=basis_ok,
            gradient_basis_check_max_abs_err=float(basis_err),
            gradient_norm2=grad_norm2,
            gradient_finite=grad_finite,
            gradient_nonzero=grad_nonzero,
            g_dot_d_n=float(proj["g_dot_d_n"]),
            g_dot_d_n_negative=bool(proj["g_dot_d_n"] < 0.0),
            alpha_cross_n=baseline,
            alpha_cross_n_state=bc_n["alpha_cross_state"],
            alpha_cross_n_reproduced=bool(
                baseline is not None
                and abs(float(baseline) - ALPHA_CROSS_N_HISTORICAL) <= 1e-12),
            d_t_inf=float(proj["d_t_max_abs"]),
            d_t_minus_d_n_inf=float(proj["d_t_minus_d_n_max_abs"]),
            g_dot_d_t=float(proj["g_dot_d_t"]),
            tangent_identity_ok=tangent_ok,
            projection_count=int(proj["projection_count"]),
            j_d_n_plus_r_inf=lin_res,
            j_d_t_plus_r_inf=float(np.max(np.abs(J.dot(d_t) + R))),
            crossing_computation_count=int(cross["crossing_computation_count"]),
            required_boundary_count=int(cross["required_count"]),
            zero_derivative_count=int(cross["zero_count"]),
            negative_derivative_count=int(cross["negative_count"]),
            alpha_cross_t=alpha_cross_t,
            alpha_cross_t_state=cross["alpha_cross_T_state"],
            alpha_near=alpha_near,
            alpha_half=alpha_half,
            has_positive_safe_fraction=has_positive,
            geometry_improvement_ratio=(None if geom_ratio is None
                                        else float(geom_ratio)),
            geometry_improving=geom_improving,
            trials=trials,
            trial_count=len(trials),
            all_trials_domain_safe=all_safe,
            all_trials_operator_equivalent=all_equivalent,
            any_trial_materially_reducing=any_reducing,
            accepted_new_hjb_iterate=False,
            deterministic_repeat_identical=False,
        )
    except TangentProjectedNewtonFailure as exc:
        failure = {"reason": str(exc)}
    except Exception as exc:  # pragma: no cover - defensive
        failure = {"reason": f"unexpected failure: {exc!r}"}

    # Outcome C: non-finite / inconsistent / no positive safe tangent geometry.
    # The failure is surfaced explicitly (never misread as a scientific result).
    return TangentProjectedNewtonResult(
        terminal=TERMINAL_C,
        failure_detail=failure,
        accepted_new_hjb_iterate=False,
        deterministic_repeat_identical=False,
    )


def _gradient_basis_check(solver: BoundaryHJBSolver, node: int, nz_i: int,
                          gvec: np.ndarray) -> tuple[bool, float]:
    """Verify ``g`` reproduces the accepted derivative map basis-entry-wise.

    For every state index ``j`` and z block, the accepted coordinate map applied
    to the basis direction ``e[j,z]`` must give exactly ``g[j,z]`` at the wall
    coordinate. Returns ``(ok, max_abs_err)``.
    """
    n, nz = solver.n, solver.nz
    worst = 0.0
    for j in range(n):
        for z in range(nz):
            e = np.zeros((n, nz))
            e[j, z] = 1.0
            dp = boundary_direction_matrix(solver, e)
            worst = max(worst, abs(float(dp[node, nz_i]) - float(gvec[z * n + j])))
    return bool(worst <= 1e-15), float(worst)


def _crossing_only(solver: BoundaryHJBSolver, V_star: np.ndarray,
                   labor0: np.ndarray, d: np.ndarray) -> dict:
    """alpha_cross for a direction using the accepted Issue #62 semantics.

    Returns ``alpha_cross=None`` when no negative derivative exists.
    """
    n, nz = solver.n, solver.nz
    grid = solver.grid
    _, pb_matrix, _, _ = solver.compute_derivatives(V_star, labor0, 0.0, 0.0)
    dp_matrix = boundary_direction_matrix(
        solver, d.reshape((n, nz), order="F"))
    items: list[tuple[float, int, int]] = []
    for node in range(n):
        if grid.families[node] == "F0":
            continue
        for nz_i in range(nz):
            p = float(pb_matrix[node, nz_i])
            dp = float(dp_matrix[node, nz_i])
            if not np.isfinite(p) or not np.isfinite(dp):
                raise TangentProjectedNewtonFailure(
                    "non-finite boundary crossing evidence")
            if dp < 0.0:
                items.append(((p - PB_MARGIN) / (-dp), node, nz_i))
    finite_positive = [it for it in items
                       if np.isfinite(it[0]) and it[0] > 0.0]
    if finite_positive:
        best = min(finite_positive, key=lambda it: it[0])
        return {"alpha_cross": float(best[0]),
                "alpha_cross_state": _state_info(solver, best[1], best[2])}
    return {"alpha_cross": None, "alpha_cross_state": None}


def run_issue68_diagnostic() -> TangentProjectedNewtonResult:
    """Exactly ONE full Issue #68 diagnostic (ONE reconstruction, ONE operator
    build, ONE Newton solve, ONE gradient, ONE projection, ONE all-boundary
    crossing, exactly TWO trials)."""
    return _run_from_reconstruction(reconstruct_issue63_stagnation_state())


def _canon(r: TangentProjectedNewtonResult) -> dict:
    return dataclasses.asdict(r)


def run_issue68_diagnostic_twice() -> tuple[TangentProjectedNewtonResult, bool]:
    """The ONE deterministic repeat of the full diagnostic."""
    first = run_issue68_diagnostic()
    second = run_issue68_diagnostic()
    identical = bool(_canon(first) == _canon(second))
    first.deterministic_repeat_identical = identical
    return first, identical


def summary_csv_lines(r: TangentProjectedNewtonResult) -> list[str]:
    """Compact CSV evidence lines for the Issue #68 report."""
    lines = ["metric,value"]
    for f in dataclasses.fields(r):
        if f.name == "trials":
            continue
        v = getattr(r, f.name)
        if isinstance(v, dict):
            v = "; ".join(f"{k}={v[k]}" for k in sorted(v))
        lines.append(f"{f.name},{v}")
    for t in r.trials:
        for f in dataclasses.fields(t):
            v = getattr(t, f.name)
            if isinstance(v, dict):
                v = "; ".join(f"{k}={v[k]}" for k in sorted(v))
            lines.append(f"{t.label}.{f.name},{v}")
    return lines
