"""DLH-5V-Y — ONE bounded Route-A projected regularized-Newton step at `V_*`.

Issue #73 / DLH-5V-Y
``SCIENTIFIC_NUMERICAL_EXECUTION__ROUTE_A_SINGLE_Q_ONE_STEP_PROJECTED_REGULARIZED_NEWTON``

Authority: Issue #73 OPEN; initial authoritative activation ``5714125203``; final
authoritative activation-refresh ``5714871725`` (post-sync live ``main``
``90e8b2191b50be04dcc1f4b805613247f69bc231``). Reviewer bounded numerical route
selection
``POLICY_FROZEN_REGULARIZED_NEWTON_DIRECTION_WITHIN_ACCEPTED_PROJECTED_CONSTRAINED_OUTER_FRAME``;
authority marker ``DLH_5VY_ROUTE_A_ONE_STEP_PROJECTED_REGULARIZED_NEWTON_AUTHORIZED``.

This is the **first execution Issue since Issue #63**. It takes exactly ONE
bounded outer step from the accepted `V_*`, using the policy-frozen regularized
Newton direction inside the outer frame frozen by the accepted Issue #72 design,
and stops at the first candidate satisfying every acceptance condition.

Execution ceiling (exactly):
1. ONE deterministic reconstruction of `V_*`;
2. ONE baseline Route-A ``final=False`` selected-`Q` build;
3. ONE baseline residual / Jacobian;
4. ONE bounded lexicographic candidate search;
5. at most ONE accepted experimental candidate;
6. immediate STOP at first acceptance, or fail closed on authorized-search
   exhaustion;
7. ONE deterministic repeat.

**No second outer step. No trajectory. No HJB convergence claim.** Any accepted
state is an *experimental one-step candidate only* — it is NOT an accepted HJB
solution and does not authorize downstream use.

Every candidate is evaluated after a **full reassembly** of the same Route-A
selected generator. There is no alternate / raw-drift `Q`, no partial `Q` update
and no dual-`Q` comparison anywhere in this module.

Frozen attempt order (lexicographic, never reordered, never extended):
``for k_lambda in 0..20: for k_Delta in 0..20: for k_alpha in 0..20``.

Projection and trust-radius conventions (frozen in this Issue, stated exactly)
---------------------------------------------------------------------------
* **Active boundary detection.** For every non-`F0` boundary state the accepted
  wall coordinate is ``p_b = vb_b`` (the backward liquid marginal), obtained from
  the accepted derivative machinery. A state is ACTIVE when
  ``p_b <= ACTIVE_BOUNDARY_TOLERANCE`` (the accepted Issue #72 tolerance). States
  with ``i == 0`` have the accepted V-independent ``p_b`` and therefore contribute
  the zero gradient.
* **Gradients are STACKED, never averaged.** Each active state contributes its own
  full-state limiting-wall gradient (the accepted two-entry ``+1/db`` at the state
  and ``-1/db`` at its backward neighbour). The constraint set is the intersection
  of ALL those hyperplanes, i.e. ``G d = 0`` with ``G`` the stacked matrix.
* **Projection.** The projected direction is the orthogonal projection of the raw
  regularized Newton direction onto the null space of ``G``, computed exactly from
  an orthonormal basis of the row space of ``G``:
  ``d_proj = d - V Vᵀ d`` with ``V`` an orthonormal basis of ``span(rows of G)``.
  This makes ``G d_proj = 0`` hold to machine precision. When no state is active
  the projection is the identity.
* **Trust radius.** ``Delta_k = 2^-k_Delta * ||d_proj||inf``, so rung
  ``k_Delta = 0`` admits the full projected direction and each successive rung
  halves the admissible infinity-norm. The direction actually used is ``d_proj``
  clipped to the infinity-norm ball of radius ``Delta_k`` (componentwise sign
  clipping). The clipping rule is frozen and deterministic.
* **Step.** ``V_trial = V + alpha * d_dir`` with ``alpha = 2^-k_alpha``.
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
from deep_learning_hank.two_asset.route_a_bounded_solver_design import (
    ACTIVE_BOUNDARY_TOLERANCE,
    ARMIJO_COEFFICIENT,
    BELLMAN_RESIDUAL_TOL,
    CANDIDATE_PB_MARGIN,
    CONSTRAINT_TOLERANCE,
    REQUIRED_RESIDUAL_REDUCTION_RATIO,
    RESIDUAL_REFERENCE,
    STEP_FRACTION_LADDER,
    TRUST_RADIUS_FRACTION_LADDER,
)
from deep_learning_hank.two_asset.route_a_hjb_residual_decomposition import (
    ACCEPTED_FINAL_STATISTIC,
    ACCEPTED_MIN_BOUNDARY_PB,
    ACCEPTED_RESIDUAL_ARGMAX_FAMILY,
    ACCEPTED_RESIDUAL_ARGMAX_NODE,
    ACCEPTED_RESIDUAL_ARGMAX_ROW,
    ACCEPTED_RESIDUAL_ARGMAX_Z,
    ACCEPTED_RESIDUAL_INF,
    ACCEPTED_STEPS,
    ACCEPTED_WALL_FAMILY,
    ACCEPTED_WALL_I,
    ACCEPTED_WALL_J,
    ACCEPTED_WALL_NODE,
    ACCEPTED_WALL_Z,
    ISSUE69_AUDIT_BLOB,
    ORACLE_BLOB,
    SELECTED_Q_ACCEPTED_BLOB,
)
from deep_learning_hank.two_asset.stagnation_newton_geometry import (
    reconstruct_issue63_stagnation_state,
)
from deep_learning_hank.two_asset.tangent_projected_newton_geometry import (
    limiting_wall_gradient,
)

# ---------------------------------------------------------------------------
# Frozen accepted references
# ---------------------------------------------------------------------------
ACCEPTED_ISSUE71_BLOB = "96dd262a4ae42e26d489a317d9a04a9264b481b1"
ACCEPTED_ISSUE72_BLOB = "f99ff6eb0d0a74cccc400ba83162a8affa9c6924"
GOVERNANCE_BASE = "90e8b2191b50be04dcc1f4b805613247f69bc231"

SELECTED_Q_RELPATH = "src/deep_learning_hank/two_asset/boundary_hjb_selected_q.py"
ORACLE_RELPATH = ("src/deep_learning_hank/two_asset/"
                  "matlab_faithful_two_asset_ha.py")
AUDIT69_RELPATH = ("src/deep_learning_hank/two_asset/"
                   "f0_rate_path_divergence_audit.py")
ISSUE71_RELPATH = ("src/deep_learning_hank/two_asset/"
                   "route_a_hjb_residual_decomposition.py")
ISSUE72_RELPATH = ("src/deep_learning_hank/two_asset/"
                   "route_a_bounded_solver_design.py")

ACCEPTED_BELLMAN_TOLERANCE = BELLMAN_RESIDUAL_TOL          # 1e-3
ACCEPTED_MAX_ABS_Q1 = 2.4253377084448857e-12

# ---------------------------------------------------------------------------
# Frozen numerical constants (all taken from the accepted Issue #72 design)
# ---------------------------------------------------------------------------
REGULARIZATION_LADDER = tuple(2.0 ** (-k) for k in range(0, 21))    # k_lambda
TRUST_RADIUS_LADDER = tuple(2.0 ** (-k) for k in range(0, 21))      # k_Delta
ALPHA_LADDER = tuple(2.0 ** (-k) for k in range(0, 21))             # k_alpha
LADDER_MAX_EXPONENT = 20
LADDER_LENGTH = 21

MERIT_REFERENCE = RESIDUAL_REFERENCE                       # 10.435094313164921
ARMIJO_C1 = ARMIJO_COEFFICIENT                             # 1e-4
DOMAIN_PB_FLOOR = CANDIDATE_PB_MARGIN                      # 1e-12
ACTIVE_PB_TOL = ACTIVE_BOUNDARY_TOLERANCE                  # 1e-12
MIN_ABSOLUTE_RESIDUAL_DECREASE = 1.0e-12
MATERIAL_REDUCTION_RATIO = REQUIRED_RESIDUAL_REDUCTION_RATIO   # 0.5

# Accepted numerical conservativity scale for the candidate operator. The
# baseline accepted `max|Q 1|` is 2.4253377084448857e-12; a candidate must stay
# within this frozen absolute scale. This is a NUMERICAL conservativity check and
# no economics/grid/tolerance is changed by it.
Q_CONSERVATIVITY_TOL = 1.0e-9
LINEAR_SOLVE_RTOL = 1.0e-12
LINEAR_RESIDUAL_TOL = 1.0e-10

# Projection null-space tolerance: a singular value below this is treated as
# numerically zero when building the orthonormal row-space basis.
NULLSPACE_SVD_TOL = 1.0e-12

REPRO_TOL = 1.0e-9

# ---------------------------------------------------------------------------
# Terminals (frozen)
# ---------------------------------------------------------------------------
TERMINAL_A = (
    "DLH_5VY_ROUTE_A_ONE_STEP_PROJECTED_REGULARIZED_NEWTON__DOMAIN_SAFE_SINGLE_Q_"
    "RESIDUAL_REDUCING_CANDIDATE_ACCEPTED__TRAJECTORY_DESIGN_GATE_READY")
TERMINAL_B = (
    "DLH_5VY_ROUTE_A_ONE_STEP_PROJECTED_REGULARIZED_NEWTON__AUTHORIZED_SEARCH_"
    "EXHAUSTED_WITH_NO_ACCEPTABLE_STEP__DIRECTION_RECONSIDERATION_REQUIRED")
TERMINAL_C = (
    "DLH_5VY_ROUTE_A_ONE_STEP_PROJECTED_REGULARIZED_NEWTON__REPRODUCTION_LINEAR_"
    "SOLVE_DOMAIN_OR_SINGLE_Q_CONTRACT_FAILURE__SCIENTIFIC_REVIEW_REQUIRED")
TERMINAL_BLOCKED = "BLOCKED_DLH_5VY_AUTHORITY_OR_DEPENDENCY_CONFLICT"

# reject / failure reasons
REASON_ACCEPTED = "ACCEPTED"
REASON_NONFINITE = "REJECT_NONFINITE_CANDIDATE"
REASON_DOMAIN = "REJECT_MIN_PB_BELOW_FLOOR"
REASON_SINGLE_Q = "REJECT_SINGLE_Q_CONTRACT"
REASON_CONSERVATIVITY = "REJECT_Q_CONSERVATIVITY"
REASON_NOT_REDUCING = "REJECT_NOT_RESIDUAL_REDUCING"
REASON_DECREASE = "REJECT_ABSOLUTE_DECREASE_BELOW_FLOOR"
REASON_ARMIJO = "REJECT_ARMIJO_CONDITION"

FAILURE_RECONSTRUCTION = "ONE_STEP_RECONSTRUCTION_REPRODUCTION_FAILURE"
FAILURE_LINEAR_SOLVE = "ONE_STEP_LINEAR_SOLVE_FAILURE"
FAILURE_NONFINITE_EVIDENCE = "ONE_STEP_NONFINITE_EVIDENCE"
FAILURE_SINGLE_Q = "ONE_STEP_SINGLE_Q_CONTRACT_FAILURE"


class OneStepNewtonFailure(RuntimeError):
    """Fail-closed: a frozen reproduction gate failed, a linear solve was invalid
    or non-finite, the single-`Q` contract was violated, or evidence was
    non-finite."""


# ---------------------------------------------------------------------------
# Result containers
# ---------------------------------------------------------------------------
@dataclass
class AttemptRecord:
    """ONE attempted candidate: full reporting payload."""

    index: int
    k_lambda: int
    k_delta: int
    k_alpha: int
    lam: float
    trust_fraction: float
    trust_radius: float
    alpha: float
    raw_direction_norm_inf: float
    projected_direction_norm_inf: float
    clipped_direction_norm_inf: float
    linear_solve_residual_inf: float
    finite: bool
    active_constraint_count: int
    active_constraint_ids: tuple
    min_pb_trial: float
    min_pb_node: int
    min_pb_nz: int
    r_trial_inf: float
    residual_ratio: float
    absolute_decrease: float
    armijo_rhs: float
    armijo_pass: bool
    material_reduction_flag: bool
    max_abs_q1_trial: float
    single_q_ok: bool
    conservativity_ok: bool
    accepted: bool
    reject_reason: str
    nonfinite_reason: str = ""


@dataclass
class OneStepResult:
    """ONE fully determined Issue #73 one-step outcome."""

    terminal: str
    failure_detail: Optional[dict] = None
    # baseline reproduction
    steps: int = 0
    final_statistic: float = float("nan")
    min_boundary_pb_star: float = float("nan")
    wall_state: dict = field(default_factory=dict)
    r_base_inf: float = float("nan")
    residual_argmax_row: int = -1
    residual_argmax_node: int = -1
    residual_argmax_z: int = -1
    residual_argmax_family: str = ""
    bellman_tolerance: float = ACCEPTED_BELLMAN_TOLERANCE
    max_abs_q1_base: float = float("nan")
    baseline_operator_build_count: int = 0
    # geometry
    active_constraint_ids: tuple = ()
    active_constraint_count: int = 0
    stacked_gradient_count: int = 0
    gradient_stack_rank: int = 0
    # search
    lambda_rung_count: int = 0
    attempted_count: int = 0
    max_candidate_count: int = 0
    first_accepted_tuple: Optional[tuple] = None
    search_exhausted: bool = False
    attempts: list = field(default_factory=list)
    # accepted candidate
    candidate_accepted: bool = False
    accepted_attempt_index: int = -1
    accepted_state_inf_norm: float = float("nan")
    accepted_step_norm_inf: float = float("nan")
    r_trial_inf: float = float("nan")
    residual_ratio: float = float("nan")
    absolute_decrease: float = float("nan")
    min_pb_trial: float = float("nan")
    max_abs_q1_trial: float = float("nan")
    armijo_rhs: float = float("nan")
    armijo_pass: bool = False
    material_reduction_flag: bool = False
    # safety flags
    second_outer_step_taken: bool = False
    trajectory_run: bool = False
    hjb_convergence_claimed: bool = False
    accepted_new_hjb_iterate: bool = False
    deterministic_repeat_identical: bool = False


# ---------------------------------------------------------------------------
# geometry: active constraints + exact projection
# ---------------------------------------------------------------------------
def _active_constraints(solver: BoundaryHJBSolver, V: np.ndarray,
                        labor0: np.ndarray) -> tuple:
    """Every ACTIVE non-F0 boundary state and its full-state wall gradient.

    Active means ``p_b <= ACTIVE_PB_TOL``, with ``p_b`` the accepted backward
    liquid marginal ``vb_b``. Gradients are STACKED (never averaged). States with
    ``i == 0`` carry the accepted V-independent ``p_b`` and therefore contribute
    the zero gradient, which cannot constrain the direction; they are recorded as
    active observations but contribute no row.
    """
    vb_f, vb_b, va_f, va_b = solver.compute_derivatives(V, labor0, 0.0, 0.0)
    g = solver.grid
    found = []
    for node in range(solver.n):
        if g.families[node] == "F0":
            continue
        for nz in range(solver.nz):
            pb = float(vb_b[node, nz])
            if np.isfinite(pb) and pb <= ACTIVE_PB_TOL:
                grad = limiting_wall_gradient(solver, node, nz)
                found.append({
                    "node": int(node), "nz": int(nz), "p_b": pb,
                    "gradient_norm": float(np.linalg.norm(grad)),
                    "gradient_nonzero": bool(np.any(grad != 0.0)),
                    "gradient": grad,
                })
    return tuple(found)


def _row_space_basis(grads: list) -> np.ndarray:
    """Orthonormal basis (columns) of ``span(rows of G)`` via SVD.

    Rows with negligible norm are dropped; singular values below
    ``NULLSPACE_SVD_TOL`` are treated as numerically zero, so a rank-deficient
    active set is handled deterministically.
    """
    rows = [g for g in grads if np.any(g != 0.0)]
    if not rows:
        return np.zeros((len(grads[0]) if grads else 0, 0), dtype=float)
    matrix = np.vstack(rows)
    _u, s, vt = np.linalg.svd(matrix, full_matrices=False)
    keep = int(np.sum(s > NULLSPACE_SVD_TOL))
    basis = vt[:keep].T if keep > 0 else np.zeros((matrix.shape[1], 0))
    return np.ascontiguousarray(basis)


def _project(d_raw: np.ndarray, basis: np.ndarray) -> np.ndarray:
    """Exact orthogonal projection onto the null space of the stacked gradients."""
    if basis.shape[1] == 0:
        return d_raw
    return d_raw - basis @ (basis.T @ d_raw)


# ---------------------------------------------------------------------------
# one candidate evaluation (full Route-A reassembly)
# ---------------------------------------------------------------------------
def _evaluate_candidate(solver: BoundaryHJBSolver, V_trial: np.ndarray,
                        labor0: np.ndarray, rho: float,
                        r_base: float) -> dict:
    """Full reassembly of the SAME Route-A selected generator at ``V_trial``.

    Returns the evaluated residual evidence plus domain / single-`Q` /
    conservativity status. Raises nothing for a bad candidate: badness is
    reported so the deterministic search can record the exact reject reason.
    """
    if not np.isfinite(V_trial).all():
        return {"finite": False, "nonfinite_reason": "NONFINITE_TRIAL_STATE"}
    try:
        Q_t, u_t, _diag, _records = solver.build_operator_and_u(
            V_trial, labor0, 0.0, 0.0, final=False)
    except Exception as exc:
        return {"finite": False,
                "nonfinite_reason": f"REASSEMBLY_RAISED:{type(exc).__name__}"}
    Vf = V_trial.ravel(order="F")
    if not np.isfinite(Q_t.data).all() or not np.isfinite(u_t).all():
        return {"finite": False,
                "nonfinite_reason": "NONFINITE_OPERATOR_OR_UTILITY"}
    R_t = rho * Vf - u_t - np.asarray(Q_t.dot(Vf)).ravel()
    if not np.isfinite(R_t).all():
        return {"finite": False, "nonfinite_reason": "NONFINITE_RESIDUAL"}
    # single-Q contract: the reassembled operator must be a generator whose row
    # sums vanish (conservativity), and it must have come from the ONE accepted
    # selected-generator path (asserted by construction above).
    q1 = np.abs(np.asarray(Q_t.sum(axis=1)).ravel())
    max_abs_q1 = float(np.max(q1))
    single_q_ok = bool(max_abs_q1 <= Q_CONSERVATIVITY_TOL)
    from deep_learning_hank.two_asset.adaptive_resolvent_hjb import (
        min_boundary_pb_state,
    )
    pb, pb_node, pb_nz = min_boundary_pb_state(solver, V_trial, labor0)
    r_trial = float(np.max(np.abs(R_t)))
    return {
        "finite": True,
        "r_trial_inf": r_trial,
        "max_abs_q1": max_abs_q1,
        "single_q_ok": single_q_ok,
        "conservativity_ok": bool(max_abs_q1 <= Q_CONSERVATIVITY_TOL),
        "min_pb": float(pb),
        "min_pb_node": int(pb_node),
        "min_pb_nz": int(pb_nz),
        "absolute_decrease": float(r_base - r_trial),
        "residual_ratio": (float(r_trial / r_base) if r_base > 0 else float("nan")),
    }


# ---------------------------------------------------------------------------
# the ONE full one-step experiment
# ---------------------------------------------------------------------------
def _run_one_step(rec: dict, counter: Optional[dict] = None) -> OneStepResult:
    counter = counter if counter is not None else {"baseline_builds": 0,
                                                   "candidate_builds": 0}
    failure: Optional[dict] = None
    try:
        solver: BoundaryHJBSolver = rec["solver"]
        labor0: np.ndarray = rec["labor0"]
        V_star: np.ndarray = rec["V_star"]
        rho: float = rec["rho"]
        trace: list = rec["trace"]
        n, nz, S = solver.n, solver.nz, solver.state_size
        Vf = V_star.ravel(order="F")

        # ---- 1. baseline reproduction (fail closed on any mismatch)
        if len(trace) != ACCEPTED_STEPS:
            raise OneStepNewtonFailure(
                f"{FAILURE_RECONSTRUCTION}: steps {len(trace)} != {ACCEPTED_STEPS}")
        final_statistic = float(trace[-1]["accepted_max_stat"])
        wall = dict(trace[-1]["worst_after"])
        if abs(final_statistic - ACCEPTED_FINAL_STATISTIC) > REPRO_TOL:
            raise OneStepNewtonFailure(
                f"{FAILURE_RECONSTRUCTION}: statistic {final_statistic!r}")
        if (str(wall.get("family")) != ACCEPTED_WALL_FAMILY
                or int(wall.get("j")) != ACCEPTED_WALL_J
                or int(wall.get("i")) != ACCEPTED_WALL_I
                or int(wall.get("z")) != ACCEPTED_WALL_Z
                or int(wall.get("node")) != ACCEPTED_WALL_NODE):
            raise OneStepNewtonFailure(
                f"{FAILURE_RECONSTRUCTION}: wall {wall!r}")
        from deep_learning_hank.two_asset.adaptive_resolvent_hjb import (
            min_boundary_pb_state,
        )
        pb_star, _pb_node, _pb_nz = min_boundary_pb_state(solver, V_star, labor0)
        if not np.isfinite(pb_star):
            raise OneStepNewtonFailure(
                f"{FAILURE_NONFINITE_EVIDENCE}: non-finite baseline p_b")
        if abs(float(pb_star) - ACCEPTED_MIN_BOUNDARY_PB) > REPRO_TOL:
            raise OneStepNewtonFailure(
                f"{FAILURE_RECONSTRUCTION}: min p_b {pb_star!r}")

        # ---- 2. exactly ONE baseline selected-Q build + residual + Jacobian
        counter["baseline_builds"] += 1
        Q, u, _diag, _records = solver.build_operator_and_u(
            V_star, labor0, 0.0, 0.0, final=False)
        if counter["baseline_builds"] != 1:
            raise OneStepNewtonFailure("more than one baseline build")
        if not np.isfinite(Q.data).all() or not np.isfinite(u).all():
            raise OneStepNewtonFailure(
                f"{FAILURE_NONFINITE_EVIDENCE}: non-finite baseline operator")
        R = rho * Vf - u - np.asarray(Q.dot(Vf)).ravel()
        if not np.isfinite(R).all():
            raise OneStepNewtonFailure(
                f"{FAILURE_NONFINITE_EVIDENCE}: non-finite baseline residual")
        r_base = float(np.max(np.abs(R)))
        if abs(r_base - ACCEPTED_RESIDUAL_INF) > REPRO_TOL:
            raise OneStepNewtonFailure(
                f"{FAILURE_RECONSTRUCTION}: baseline residual {r_base!r} != "
                f"{ACCEPTED_RESIDUAL_INF!r}")
        am = int(np.argmax(np.abs(R)))
        am_z, am_node = am // n, am % n
        am_family = str(solver.grid.families[am_node])
        if (am != ACCEPTED_RESIDUAL_ARGMAX_ROW
                or am_node != ACCEPTED_RESIDUAL_ARGMAX_NODE
                or am_z != ACCEPTED_RESIDUAL_ARGMAX_Z
                or am_family != ACCEPTED_RESIDUAL_ARGMAX_FAMILY):
            raise OneStepNewtonFailure(
                f"{FAILURE_RECONSTRUCTION}: residual argmax mismatch")
        max_abs_q1_base = float(np.max(np.abs(
            np.asarray(Q.sum(axis=1)).ravel())))
        if max_abs_q1_base > Q_CONSERVATIVITY_TOL:
            raise OneStepNewtonFailure(
                f"{FAILURE_SINGLE_Q}: baseline conservativity "
                f"max|Q1| = {max_abs_q1_base!r}")
        J = (rho * sparse.eye(S, format="csr") - Q).tocsr()
        diag = np.asarray(J.diagonal())
        diag_inf = float(np.max(np.abs(diag)))
        if not np.isfinite(diag_inf) or diag_inf <= 0.0:
            raise OneStepNewtonFailure(
                f"{FAILURE_NONFINITE_EVIDENCE}: degenerate Jacobian scale")

        # ---- geometry: stacked active wall constraints (never averaged)
        active = _active_constraints(solver, V_star, labor0)
        active_ids = tuple((a["node"], a["nz"]) for a in active)
        grads = [a["gradient"] for a in active if a["gradient_nonzero"]]
        basis = _row_space_basis(grads)
        rank = int(basis.shape[1])

        # ---- 3. ONE bounded lexicographic candidate search
        attempts: list[AttemptRecord] = []
        first_accepted: Optional[tuple] = None
        accepted_payload: Optional[dict] = None
        index = 0
        linear_solve_failures = 0
        stop = False
        lambda_rungs = 0
        for k_lambda in range(0, LADDER_MAX_EXPONENT + 1):
            if stop:
                break
            lam = REGULARIZATION_LADDER[k_lambda]
            lambda_rungs += 1
            A = (J + lam * diag_inf * sparse.eye(S, format="csr")).tocsc()
            try:
                d_raw = np.asarray(linalg.spsolve(A, -R)).ravel()
            except Exception as exc:  # pragma: no cover - defensive
                linear_solve_failures += 1
                raise OneStepNewtonFailure(
                    f"{FAILURE_LINEAR_SOLVE}: rung k_lambda={k_lambda}: "
                    f"{exc!r}") from exc
            lin_res = float(np.max(np.abs(np.asarray(A.dot(d_raw)).ravel() + R)))
            if not np.isfinite(d_raw).all() or not np.isfinite(lin_res):
                linear_solve_failures += 1
                raise OneStepNewtonFailure(
                    f"{FAILURE_LINEAR_SOLVE}: rung k_lambda={k_lambda} "
                    "non-finite direction or solve residual")
            if lin_res > LINEAR_RESIDUAL_TOL:
                raise OneStepNewtonFailure(
                    f"{FAILURE_LINEAR_SOLVE}: rung k_lambda={k_lambda} "
                    f"linear residual {lin_res!r} > {LINEAR_RESIDUAL_TOL!r}")
            raw_norm = float(np.max(np.abs(d_raw)))
            d_proj = _project(d_raw, basis)
            if not np.isfinite(d_proj).all():
                raise OneStepNewtonFailure(
                    f"{FAILURE_NONFINITE_EVIDENCE}: non-finite projected "
                    f"direction at k_lambda={k_lambda}")
            proj_norm = float(np.max(np.abs(d_proj)))

            for k_delta in range(0, LADDER_MAX_EXPONENT + 1):
                if stop:
                    break
                frac = TRUST_RADIUS_LADDER[k_delta]
                radius = frac * proj_norm
                if proj_norm > radius:
                    d_dir = np.clip(d_proj, -radius, radius)
                else:
                    d_dir = d_proj
                dir_norm = float(np.max(np.abs(d_dir)))

                for k_alpha in range(0, LADDER_MAX_EXPONENT + 1):
                    if stop:
                        break
                    alpha = ALPHA_LADDER[k_alpha]
                    V_trial = V_star + alpha * d_dir.reshape((n, nz), order="F")
                    counter["candidate_builds"] += 1
                    ev = _evaluate_candidate(solver, V_trial, labor0, rho, r_base)
                    index += 1

                    if not ev.get("finite", False):
                        attempts.append(AttemptRecord(
                            index=index, k_lambda=k_lambda, k_delta=k_delta,
                            k_alpha=k_alpha, lam=float(lam),
                            trust_fraction=float(frac), trust_radius=float(radius),
                            alpha=float(alpha), raw_direction_norm_inf=raw_norm,
                            projected_direction_norm_inf=proj_norm,
                            clipped_direction_norm_inf=dir_norm,
                            linear_solve_residual_inf=lin_res, finite=False,
                            active_constraint_count=len(active_ids),
                            active_constraint_ids=active_ids,
                            min_pb_trial=float("nan"), min_pb_node=-1, min_pb_nz=-1,
                            r_trial_inf=float("nan"), residual_ratio=float("nan"),
                            absolute_decrease=float("nan"), armijo_rhs=float("nan"),
                            armijo_pass=False, material_reduction_flag=False,
                            max_abs_q1_trial=float("nan"), single_q_ok=False,
                            conservativity_ok=False, accepted=False,
                            reject_reason=REASON_NONFINITE,
                            nonfinite_reason=str(ev.get("nonfinite_reason", ""))))
                        continue

                    r_trial = ev["r_trial_inf"]
                    ratio = ev["residual_ratio"]
                    decrease = ev["absolute_decrease"]
                    armijo_rhs = r_base - ARMIJO_C1 * alpha * r_base
                    armijo_pass = bool(r_trial <= armijo_rhs)
                    material = bool(ratio <= MATERIAL_REDUCTION_RATIO)

                    reason = ""
                    if not np.isfinite(ev["min_pb"]) or ev["min_pb"] < DOMAIN_PB_FLOOR:
                        reason = REASON_DOMAIN
                    elif not ev["single_q_ok"]:
                        reason = REASON_SINGLE_Q
                    elif not ev["conservativity_ok"]:
                        reason = REASON_CONSERVATIVITY
                    elif not (r_trial < r_base):
                        reason = REASON_NOT_REDUCING
                    elif not (decrease >= MIN_ABSOLUTE_RESIDUAL_DECREASE):
                        reason = REASON_DECREASE
                    elif not armijo_pass:
                        reason = REASON_ARMIJO
                    accepted = (reason == "")

                    attempts.append(AttemptRecord(
                        index=index, k_lambda=k_lambda, k_delta=k_delta,
                        k_alpha=k_alpha, lam=float(lam),
                        trust_fraction=float(frac), trust_radius=float(radius),
                        alpha=float(alpha), raw_direction_norm_inf=raw_norm,
                        projected_direction_norm_inf=proj_norm,
                        clipped_direction_norm_inf=dir_norm,
                        linear_solve_residual_inf=lin_res, finite=True,
                        active_constraint_count=len(active_ids),
                        active_constraint_ids=active_ids,
                        min_pb_trial=float(ev["min_pb"]),
                        min_pb_node=int(ev["min_pb_node"]),
                        min_pb_nz=int(ev["min_pb_nz"]),
                        r_trial_inf=float(r_trial), residual_ratio=float(ratio),
                        absolute_decrease=float(decrease),
                        armijo_rhs=float(armijo_rhs), armijo_pass=armijo_pass,
                        material_reduction_flag=material,
                        max_abs_q1_trial=float(ev["max_abs_q1"]),
                        single_q_ok=bool(ev["single_q_ok"]),
                        conservativity_ok=bool(ev["conservativity_ok"]),
                        accepted=accepted,
                        reject_reason=REASON_ACCEPTED if accepted else reason))

                    if accepted:
                        first_accepted = (k_lambda, k_delta, k_alpha)
                        accepted_payload = {
                            "index": index,
                            "V_trial": V_trial,
                            "step_norm_inf": float(np.max(
                                np.abs(alpha * d_dir))),
                            "r_trial_inf": r_trial,
                            "ratio": ratio,
                            "decrease": decrease,
                            "min_pb": float(ev["min_pb"]),
                            "max_abs_q1": float(ev["max_abs_q1"]),
                            "armijo_rhs": float(armijo_rhs),
                            "material": material,
                        }
                        stop = True
                        break

        # ---- terminal selection
        if first_accepted is not None:
            terminal = TERMINAL_A
        elif index == 0:
            terminal = TERMINAL_C
        else:
            terminal = TERMINAL_B
        if first_accepted is None and index == 0:
            raise OneStepNewtonFailure(
                f"{FAILURE_NONFINITE_EVIDENCE}: no candidate was attempted")

        max_candidate_count = (LADDER_MAX_EXPONENT + 1) ** 3
        out = OneStepResult(
            terminal=terminal,
            failure_detail=None,
            steps=len(trace),
            final_statistic=final_statistic,
            min_boundary_pb_star=float(pb_star),
            wall_state=wall,
            r_base_inf=r_base,
            residual_argmax_row=am,
            residual_argmax_node=am_node,
            residual_argmax_z=am_z,
            residual_argmax_family=am_family,
            bellman_tolerance=ACCEPTED_BELLMAN_TOLERANCE,
            max_abs_q1_base=max_abs_q1_base,
            baseline_operator_build_count=int(counter["baseline_builds"]),
            active_constraint_ids=active_ids,
            active_constraint_count=len(active_ids),
            stacked_gradient_count=len(grads),
            gradient_stack_rank=rank,
            lambda_rung_count=lambda_rungs,
            attempted_count=index,
            max_candidate_count=max_candidate_count,
            first_accepted_tuple=first_accepted,
            search_exhausted=bool(first_accepted is None),
            attempts=attempts,
            candidate_accepted=bool(first_accepted is not None),
            accepted_attempt_index=(accepted_payload["index"]
                                    if accepted_payload else -1),
            accepted_state_inf_norm=(float(np.max(np.abs(
                accepted_payload["V_trial"]))) if accepted_payload
                else float("nan")),
            accepted_step_norm_inf=(accepted_payload["step_norm_inf"]
                                    if accepted_payload else float("nan")),
            r_trial_inf=(accepted_payload["r_trial_inf"] if accepted_payload
                         else float("nan")),
            residual_ratio=(accepted_payload["ratio"] if accepted_payload
                            else float("nan")),
            absolute_decrease=(accepted_payload["decrease"] if accepted_payload
                               else float("nan")),
            min_pb_trial=(accepted_payload["min_pb"] if accepted_payload
                          else float("nan")),
            max_abs_q1_trial=(accepted_payload["max_abs_q1"] if accepted_payload
                              else float("nan")),
            armijo_rhs=(accepted_payload["armijo_rhs"] if accepted_payload
                        else float("nan")),
            armijo_pass=bool(accepted_payload is not None),
            material_reduction_flag=(accepted_payload["material"]
                                     if accepted_payload else False),
            second_outer_step_taken=False,
            trajectory_run=False,
            hjb_convergence_claimed=False,
            accepted_new_hjb_iterate=False,
            deterministic_repeat_identical=False,
        )
        return out
    except OneStepNewtonFailure as exc:
        failure = {"reason": str(exc)}
    except Exception as exc:  # pragma: no cover - defensive
        failure = {"reason": f"unexpected failure: {exc!r}"}

    return OneStepResult(terminal=TERMINAL_C, failure_detail=failure,
                         second_outer_step_taken=False,
                         trajectory_run=False,
                         hjb_convergence_claimed=False,
                         accepted_new_hjb_iterate=False)


# ---------------------------------------------------------------------------
# entry points
# ---------------------------------------------------------------------------
def run_issue73_one_step() -> OneStepResult:
    """Exactly ONE bounded one-step experiment (one baseline reconstruction, one
    baseline selected-`Q` build, one bounded candidate search, at most one
    accepted candidate)."""
    counter = {"baseline_builds": 0, "candidate_builds": 0}
    return _run_one_step(reconstruct_issue63_stagnation_state(), counter)


def _canon(r: OneStepResult) -> dict:
    """Canonical comparison-safe form (NaN-aware)."""
    def norm(value):
        if isinstance(value, float) and np.isnan(value):
            return "__NAN__"
        if isinstance(value, dict):
            return {k: norm(v) for k, v in value.items()}
        if isinstance(value, (list, tuple)):
            return [norm(v) for v in value]
        return value

    payload = dataclasses.asdict(r)
    payload.pop("accepted_state_inf_norm", None)   # derived summary, not evidence
    return {k: norm(v) for k, v in payload.items()}


def run_issue73_one_step_twice() -> tuple[OneStepResult, bool]:
    """The ONE deterministic repeat of the complete one-step experiment."""
    first = run_issue73_one_step()
    second = run_issue73_one_step()
    identical = bool(_canon(first) == _canon(second))
    first.deterministic_repeat_identical = identical
    return first, identical


def accepted_anchor_blobs() -> dict:
    """Read-only verification of the accepted anchors this Issue rests on."""
    import subprocess
    from pathlib import Path
    repo_root = Path(__file__).resolve().parents[3]

    def blob(relpath: str, rev: str = "HEAD") -> str:
        return subprocess.run(
            ["git", "rev-parse", f"{rev}:{relpath}"], cwd=repo_root,
            capture_output=True, text=True, encoding="utf-8",
            errors="replace", check=True).stdout.strip()

    return {
        "selected_q_blob": blob(SELECTED_Q_RELPATH),
        "oracle_blob": blob(ORACLE_RELPATH),
        "issue69_blob": blob(AUDIT69_RELPATH),
        "issue71_blob": blob(ISSUE71_RELPATH),
        "issue72_blob": blob(ISSUE72_RELPATH),
    }


def attempts_csv_lines(r: OneStepResult) -> list[str]:
    """Per-attempt CSV evidence, one row per attempted candidate."""
    fields = [f.name for f in dataclasses.fields(AttemptRecord)]
    lines = [",".join(fields)]
    for a in r.attempts:
        row = []
        for name in fields:
            v = getattr(a, name)
            if isinstance(v, tuple):
                v = ";".join(str(x) for x in v)
            row.append(str(v))
        lines.append(",".join(row))
    return lines


def summary_csv_lines(r: OneStepResult) -> list[str]:
    """Compact CSV evidence for the Issue #73 report."""
    lines = ["metric,value"]
    for f in dataclasses.fields(r):
        if f.name == "attempts":
            continue
        v = getattr(r, f.name)
        if isinstance(v, dict):
            v = "; ".join(f"{k}={v[k]}" for k in sorted(v))
        lines.append(f"{f.name},{v}")
    return lines
