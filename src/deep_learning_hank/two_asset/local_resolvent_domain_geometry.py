"""DLH-5V-N: local continuous resolvent / domain-margin geometry diagnostic.

Diagnoses the LOCAL geometry of the frozen selected-Q resolvent at the last
accepted Issue #61 state ``V_*`` (immediately before its terminal third update
request), with frozen ``(V_*, Q_*, u_*)``.

Authorized object ONLY (Issue #62):

- reconstruct the accepted Issue #61 trajectory deterministically and STOP at
  its last accepted state after exactly 2 accepted updates;
- at that frozen ``V_*`` build selected policy / utility / conservative
  backward ``Q_*`` EXACTLY ONCE;
- the same frozen ``(V_*, Q_*, u_*)`` is used for every local delta
  evaluation (no policy re-selection as delta varies);
- exactly: ONE local infinitesimal-direction diagnostic, ONE boundary
  ``dp_b/delta|_0`` diagnostic, ONE first-order margin prediction, ONE
  deterministic bracketed continuous crossing solve on the fixed bracket
  ``[0, 1000*2^-20]``, ONE deterministic repeat.

Equivalent continuous resolvent representation (well-defined at delta = 0):

    [I + delta*(rho I - Q_*)] V(delta) = V_* + delta*u_*        V(0) = V_*

For every positive delta this is algebraically identical to the Issue #61 form

    [(1/delta + rho)I - Q_*] V(delta) = u_* + V_*/delta

and does not change the fixed-point target or household economics.

Local diagnostics:

- exact infinitesimal direction
  ``dV/delta|_0 = u_* + Q_* V_* - rho V_*``;
- boundary directional derivatives ``dp_b/delta|_0`` for every required
  non-F0 boundary state (the accepted ``compute_derivatives`` map is linear in
  V; the b_min face p_b is V-independent, hence its directional derivative is
  0);
- for every state with negative directional derivative, the first-order
  margin-crossing prediction
  ``delta_margin_linear = (p_b(V_*) - PB_MARGIN)/(-dp_b/delta|_0)``;
- the minimum positive finite ``delta_margin_linear`` and its state;
- ``g(delta) = min_required_boundary p_b(V(delta)) - PB_MARGIN`` with
  ``g(0) > 0`` and ``g(1000*2^-20) < 0``, then a deterministic bracketed
  continuous root solve (``scipy.optimize.brentq``) on the fixed bracket
  ``[0, 1000*2^-20]``.

FAIL-CLOSED: any non-finite required boundary p_b or non-finite directional
evidence deterministically fails the diagnostic (raises
``LocalGeometryFailure`` and is surfaced explicitly).

The linear prediction is a LOCAL diagnostic only, not a theorem of the
nonlinear continuous-delta path. A bracketed root is a reproducible
sign-changing crossing of the global boundary margin on the frozen local
operator — NOT a claim of global uniqueness or of the first positive crossing.

Integrity: no third HJB iterate is accepted; no multi-step continuation /
homotopy; the Issue #61 discrete ladder is NOT extended as an experiment; no
value damping; no p_b clip/floor; no economics / prices / grid / domain /
PB_MARGIN change; the household oracle, selected-Q source and the accepted
Issue #61 implementation are all read-only imports. No KFE / stationary KFE /
steady state.
"""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field
from typing import Optional

import numpy as np
from scipy import sparse
from scipy.sparse import linalg
from scipy.optimize import brentq

from deep_learning_hank.two_asset.boundary_hjb_selected_q import (
    BoundaryHJBFailure,
    BoundaryHJBSolver,
)
from deep_learning_hank.two_asset.adaptive_resolvent_hjb import (
    CENTRAL_CONFIG,
    PB_MARGIN,
    DELTA_REF,
    DELTA_MIN_EXP,
    _state_info,
    min_boundary_pb,
    min_boundary_pb_state,
    select_largest_feasible_delta,
)

# ---------------------------------------------------------------------------
# Frozen constants (Issue #62) — do NOT change
# ---------------------------------------------------------------------------
DELTA_FLOOR = DELTA_REF * 2.0 ** (-DELTA_MIN_EXP)   # 1000*2^-20 (Issue #61 ladder floor)
EPS_VERIFY = 1.0e-6                                 # fixed below/above-root verification offset
RECONSTRUCT_ITERATIONS = 2                          # accepted Issue #61 iterations to reproduce
BRENTQ_XTOL = 1.0e-15                               # deterministic root tolerances
BRENTQ_RTOL = 4.0 * np.finfo(float).eps


class LocalGeometryFailure(RuntimeError):
    """Non-finite or internally inconsistent local evidence — fails closed."""


@dataclass(frozen=True)
class LocalGeometryResult:
    outcome: str
    # -- reconstruction of the accepted Issue #61 terminal state -------------
    iterations: int
    trace: list[dict]                       # 2 rows, mirrors accepted Issue #61 trace
    v0_min_boundary_pb: float
    min_accepted_boundary_pb: float
    terminal_min_boundary_pb: float
    terminal_state: Optional[dict]
    # -- frozen operator -----------------------------------------------------
    max_abs_q1: float
    expansions: int
    artificial_bindings: int
    # -- infinitesimal direction ---------------------------------------------
    direction_max_abs: float
    dpb_most_negative: float
    dpb_most_negative_state: Optional[dict]
    dpb_negative_count: int
    dpb_required_count: int
    dpb_zero_count: int
    min_delta_margin_linear: Optional[float]
    min_delta_margin_linear_state: Optional[dict]
    delta_margin_linear_count: int
    # -- continuous crossing -------------------------------------------------
    g0: float
    g_hi: float
    bracket_lo: float
    bracket_hi: float
    delta_cross: Optional[float]
    g_cross: Optional[float]
    cross_worst_state: Optional[dict]
    below_delta: Optional[float]
    below_g: Optional[float]
    below_min_pb: Optional[float]
    below_state: Optional[dict]
    above_delta: Optional[float]
    above_g: Optional[float]
    above_min_pb: Optional[float]
    above_state: Optional[dict]
    ratio_cross_over_floor: Optional[float]
    ratio_cross_over_linear: Optional[float]
    # -- determinism ----------------------------------------------------------
    deterministic_repeat_identical: bool = False
    failure_detail: Optional[dict] = None

    def to_summary_csv_lines(self) -> list[str]:
        """Key/value summary CSV (DLH_5VN_LOCAL_GEOMETRY_SUMMARY.csv)."""
        def st(d: Optional[dict]) -> str:
            if d is None:
                return ""
            return (f"node={d.get('node')},j={d.get('j')},i={d.get('i')},"
                    f"z={d.get('z')},family={d.get('family')}")

        rows: list[tuple[str, str]] = [
            ("outcome", self.outcome),
            ("reconstruction.iterations", str(self.iterations)),
            ("reconstruction.v0_min_boundary_pb", f"{self.v0_min_boundary_pb:.12g}"),
            ("reconstruction.min_accepted_boundary_pb", f"{self.min_accepted_boundary_pb:.12g}"),
            ("reconstruction.terminal_min_boundary_pb", f"{self.terminal_min_boundary_pb:.12g}"),
            ("reconstruction.terminal_state", st(self.terminal_state)),
            ("frozen.max_abs_q1", f"{self.max_abs_q1:.6e}"),
            ("frozen.expansions", str(self.expansions)),
            ("frozen.artificial_bindings", str(self.artificial_bindings)),
            ("direction.dV_delta0_max_abs", f"{self.direction_max_abs:.12g}"),
            ("direction.dpb_most_negative", f"{self.dpb_most_negative:.12g}"),
            ("direction.dpb_most_negative_state", st(self.dpb_most_negative_state)),
            ("direction.dpb_negative_count", str(self.dpb_negative_count)),
            ("direction.dpb_required_count", str(self.dpb_required_count)),
            ("direction.dpb_zero_count", str(self.dpb_zero_count)),
            ("direction.min_delta_margin_linear",
             "" if self.min_delta_margin_linear is None else f"{self.min_delta_margin_linear:.12g}"),
            ("direction.min_delta_margin_linear_state", st(self.min_delta_margin_linear_state)),
            ("direction.delta_margin_linear_count", str(self.delta_margin_linear_count)),
            ("crossing.g0", f"{self.g0:.12g}"),
            ("crossing.g_hi", f"{self.g_hi:.12g}"),
            ("crossing.bracket_lo", f"{self.bracket_lo:.12g}"),
            ("crossing.bracket_hi", f"{self.bracket_hi:.12g}"),
            ("crossing.delta_cross",
             "" if self.delta_cross is None else f"{self.delta_cross:.12g}"),
            ("crossing.g_cross",
             "" if self.g_cross is None else f"{self.g_cross:.12g}"),
            ("crossing.cross_worst_state", st(self.cross_worst_state)),
            ("crossing.below_delta",
             "" if self.below_delta is None else f"{self.below_delta:.12g}"),
            ("crossing.below_g",
             "" if self.below_g is None else f"{self.below_g:.12g}"),
            ("crossing.below_min_pb",
             "" if self.below_min_pb is None else f"{self.below_min_pb:.12g}"),
            ("crossing.below_state", st(self.below_state)),
            ("crossing.above_delta",
             "" if self.above_delta is None else f"{self.above_delta:.12g}"),
            ("crossing.above_g",
             "" if self.above_g is None else f"{self.above_g:.12g}"),
            ("crossing.above_min_pb",
             "" if self.above_min_pb is None else f"{self.above_min_pb:.12g}"),
            ("crossing.above_state", st(self.above_state)),
            ("crossing.ratio_cross_over_floor",
             "" if self.ratio_cross_over_floor is None else f"{self.ratio_cross_over_floor:.12g}"),
            ("crossing.ratio_cross_over_linear",
             "" if self.ratio_cross_over_linear is None else f"{self.ratio_cross_over_linear:.12g}"),
            ("deterministic_repeat_identical", str(self.deterministic_repeat_identical).lower()),
        ]
        return ["," .join([k, v]) for (k, v) in rows]


# ---------------------------------------------------------------------------
# Frozen continuous resolvent (scaled form, well-defined at delta = 0)
# ---------------------------------------------------------------------------
def solve_scaled_resolvent(Q: sparse.csr_matrix, u: np.ndarray,
                           V_star: np.ndarray, delta: float,
                           rho: float) -> np.ndarray:
    """Solve [I + delta*(rho I - Q_*)] V(delta) = V_* + delta*u_*.

    Well-defined at delta = 0 (returns V_* within machine tolerance).
    Uses the same state-vector layout as the accepted solver (z-major,
    node-fastest; reshape order='F'). Deterministic (SuperLU).
    """
    n = int(Q.shape[0])
    eye = sparse.eye(n, format="csr")
    matrix = eye + delta * (rho * eye - Q)
    rhs = (V_star.ravel(order="F")
           + delta * np.asarray(u, dtype=float).ravel(order="F"))
    try:
        v = linalg.spsolve(matrix, rhs)
    except Exception as exc:  # pragma: no cover - defensive
        raise BoundaryHJBFailure(
            "HJB_LINEAR_SOLVE_FAILURE",
            f"scaled resolvent solve raised: {exc!r}", {},
        ) from exc
    if v.shape != (V_star.size,) or not np.isfinite(v).all():
        raise BoundaryHJBFailure(
            "HJB_LINEAR_SOLVE_FAILURE",
            "non-finite scaled resolvent solve output", {},
        )
    return v.reshape(V_star.shape, order="F")


def solve_original_resolvent(Q: sparse.csr_matrix, u: np.ndarray,
                             V_star: np.ndarray, delta: float,
                             rho: float) -> np.ndarray:
    """Issue #61 form [(1/delta + rho)I - Q_*] V(delta) = u_* + V_*/delta.

    delta > 0 only; used to verify algebraic agreement with the scaled form.
    """
    n = int(Q.shape[0])
    matrix = (1.0 / delta + rho) * sparse.eye(n, format="csr") - Q
    rhs = (np.asarray(u, dtype=float).ravel(order="F")
           + V_star.ravel(order="F") / delta)
    try:
        v = linalg.spsolve(matrix, rhs)
    except Exception as exc:  # pragma: no cover - defensive
        raise BoundaryHJBFailure(
            "HJB_LINEAR_SOLVE_FAILURE",
            f"original resolvent solve raised: {exc!r}", {},
        ) from exc
    if v.shape != (V_star.size,) or not np.isfinite(v).all():
        raise BoundaryHJBFailure(
            "HJB_LINEAR_SOLVE_FAILURE",
            "non-finite original resolvent solve output", {},
        )
    return v.reshape(V_star.shape, order="F")


def infinitesimal_direction(Q: sparse.csr_matrix, u: np.ndarray,
                            V_star: np.ndarray, rho: float) -> np.ndarray:
    """Exact local resolvent direction at zero:
    dV/delta|_0 = u_* + Q_* V_* - rho V_*."""
    flat = V_star.ravel(order="F")
    dV = (np.asarray(u, dtype=float).ravel(order="F") + Q.dot(flat)
          - rho * flat)
    return dV.reshape(V_star.shape, order="F")


# ---------------------------------------------------------------------------
# Reconstruction of the accepted Issue #61 terminal state (2 accepted updates)
# ---------------------------------------------------------------------------
def _sector_seq(records: list) -> tuple:
    return tuple((r.family, r.sector) if r is not None else ("?", "?")
                 for r in records)


def reconstruct_issue61_terminal_state() -> dict:
    """Deterministically reconstruct the accepted Issue #61 trajectory and STOP
    at its last accepted state after exactly 2 accepted updates."""
    solver = BoundaryHJBSolver(CENTRAL_CONFIG)
    labor0 = solver.build_labor0(0.0, 0.0)
    V0 = solver.build_initial_value(labor0, 0.0, 0.0)
    v0_pb = min_boundary_pb(solver, V0, labor0)
    V = V0.copy()
    trace: list[dict] = []
    prev_sector: Optional[tuple] = None
    records: list = [None] * solver.state_size
    min_accepted_pb = float("inf")
    for iteration in range(1, RECONSTRUCT_ITERATIONS + 1):
        Q, u, diag1, records = solver.build_operator_and_u(
            V, labor0, 0.0, 0.0, final=False)
        sel = select_largest_feasible_delta(solver, V, labor0, Q, u)
        V_new = sel["V_new"]
        pb_new = min_boundary_pb(solver, V_new, labor0)
        min_accepted_pb = min(min_accepted_pb, pb_new)
        max_q1 = float(np.max(np.abs(np.asarray(Q.sum(axis=1)).ravel())))
        sector_now = _sector_seq(records)
        changes = (sum(1 for x, y in zip(prev_sector, sector_now) if x != y)
                   if prev_sector is not None else 0)
        prev_sector = sector_now
        trace.append({
            "iteration": iteration,
            "selected_delta": sel["delta"],
            "delta_index": sel["k"],
            "backtrack_count": sel["k"],
            "accepted_max_stat": sel["stat"],
            "ref1000_max_stat": sel["ref1000_stat"],
            "ref1000_min_pb": sel["ref1000_min_pb"],
            "min_pb_old": sel["min_pb_old"],
            "min_pb_new": pb_new,
            "delta1000_would_violate": sel["delta1000_would_violate"],
            "max_abs_q1": max_q1,
            "expansions": int(diag1["total_expansions"]),
            "artificial_bindings": int(diag1["artificial_binding"]),
            "sector_changes": changes,
        })
        V = V_new
    return {
        "solver": solver, "labor0": labor0, "V_star": V.copy(),
        "trace": trace, "min_accepted_boundary_pb": min_accepted_pb,
        "v0_min_boundary_pb": v0_pb,
    }


# ---------------------------------------------------------------------------
# Local diagnostics on the frozen (V_*, Q_*, u_*)
# ---------------------------------------------------------------------------
def boundary_direction_matrix(solver: BoundaryHJBSolver,
                              dV: np.ndarray) -> np.ndarray:
    """Manual ``dp_b/delta|_0`` over (n_nodes, n_z) per the ACCEPTED boundary
    derivative semantics.

    The accepted ``compute_derivatives`` map is linear in V on the regular
    backward finite-difference states, but at the b_min face (``i == 0``) it
    OVERWRITES ``vb_b`` with the resource-based marginal
    ``resources**(-gamma_c)``, which is INDEPENDENT of V.  Hence the true
    directional derivative there is exactly 0 and must NOT be read from
    ``compute_derivatives(dV, ...).vb_b`` (that would return the positive
    constant resource marginal instead of the directional derivative).

    Construction (accepted selected-Q source is NOT modified):

    - regular backward finite-difference state (i > 0, down exists):
      ``dp_b/delta|_0 = (dV[node] - dV[down]) / db`` — identical to the
      accepted ``vb_b`` linear difference of ``dV``;
    - accepted V-independent boundary rule (i == 0): ``dp_b/delta|_0 = 0``
      exactly.

    FAIL-CLOSED: non-finite input dV at a required state raises
    ``LocalGeometryFailure`` (surfaced explicitly).
    """
    g = solver.grid
    db = float(solver.db)
    dp = np.zeros((solver.n, solver.nz), dtype=float)
    for node in range(solver.n):
        j, i = int(g.j_arr[node]), int(g.i_arr[node])
        if i == 0:
            continue                      # V-independent boundary rule -> 0
        down = g.node_of.get((j, i - 1))
        if down is None:
            raise LocalGeometryFailure(
                f"no backward neighbor for required state node {node} (i={i})")
        for nz in range(solver.nz):
            v = float((dV[node, nz] - dV[down, nz]) / db)
            if not np.isfinite(v):
                raise LocalGeometryFailure(
                    f"non-finite directional evidence at node {node} z {nz}: "
                    f"{v!r}")
            dp[node, nz] = v
    return dp


def boundary_direction_diagnostic(solver: BoundaryHJBSolver,
                                  V_star: np.ndarray, labor0: np.ndarray,
                                  dV: np.ndarray) -> dict:
    """Boundary p_b(V_*) and directional derivatives dp_b/delta|_0.

    FAIL-CLOSED: non-finite required boundary p_b or non-finite directional
    evidence raises LocalGeometryFailure and is surfaced explicitly.
    """
    pb_star, node0, nz0 = min_boundary_pb_state(solver, V_star, labor0)
    if not np.isfinite(pb_star):
        raise LocalGeometryFailure(
            f"non-finite required boundary p_b(V_star): {pb_star!r} at "
            f"node {node0} z {nz0}")
    _, pb_matrix, _, _ = solver.compute_derivatives(V_star, labor0, 0.0, 0.0)
    dp_matrix = boundary_direction_matrix(solver, dV)
    g = solver.grid
    required = 0
    zero_count = 0
    most_neg: Optional[float] = None
    most_neg_node = -1
    most_neg_nz = -1
    linear_items: list[tuple[float, int, int]] = []
    for node in range(solver.n):
        if g.families[node] == "F0":
            continue
        for nz in range(solver.nz):
            required += 1
            p = float(pb_matrix[node, nz])
            if not np.isfinite(p):
                raise LocalGeometryFailure(
                    f"non-finite boundary p_b at node {node} z {nz}: {p!r}")
            dp = float(dp_matrix[node, nz])
            if dp == 0.0:
                zero_count += 1           # V-independent boundary rule (i == 0)
            if dp < 0.0:
                lin = (p - PB_MARGIN) / (-dp)
                linear_items.append((lin, node, nz))
                if most_neg is None or dp < most_neg:
                    most_neg = dp
                    most_neg_node = node
                    most_neg_nz = nz
    finite_positive = [(lin, node, nz) for (lin, node, nz) in linear_items
                       if np.isfinite(lin) and lin > 0.0]
    best_lin: Optional[tuple[float, int, int]] = None
    for item in finite_positive:
        if best_lin is None or item[0] < best_lin[0]:
            best_lin = item
    return {
        "pb_star": float(pb_star),
        "terminal_state": _state_info(solver, node0, nz0),
        "dpb_most_negative": most_neg,
        "dpb_most_negative_state":
            None if most_neg is None
            else _state_info(solver, most_neg_node, most_neg_nz),
        "dpb_negative_count": len(linear_items),
        "dpb_required_count": required,
        "dpb_zero_count": zero_count,      # V-independent (i == 0) required states
        "min_delta_margin_linear": None if best_lin is None else float(best_lin[0]),
        "min_delta_margin_linear_state":
            None if best_lin is None
            else _state_info(solver, best_lin[1], best_lin[2]),
        "delta_margin_linear_count": len(finite_positive),
        "linear_items": linear_items,
    }


def g_delta(solver: BoundaryHJBSolver, Q: sparse.csr_matrix, u: np.ndarray,
            V_star: np.ndarray, labor0: np.ndarray, rho: float,
            delta: float) -> float:
    """g(delta) = min_required_boundary p_b(V(delta)) - PB_MARGIN.

    FAIL-CLOSED: non-finite required boundary evidence RAISES
    ``LocalGeometryFailure`` — it is never returned as ``+inf`` (which would
    be misread as g > 0, i.e. feasible).
    """
    Vd = solve_scaled_resolvent(Q, u, V_star, delta, rho)
    pb = min_boundary_pb(solver, Vd, labor0)
    if not np.isfinite(pb):
        raise LocalGeometryFailure(
            f"non-finite required boundary p_b at delta={delta:.12g}: {pb!r}")
    return float(pb) - PB_MARGIN


def continuous_crossing_diagnostic(solver: BoundaryHJBSolver,
                                   Q: sparse.csr_matrix, u: np.ndarray,
                                   V_star: np.ndarray, labor0: np.ndarray,
                                   rho: float) -> dict:
    """Deterministic bracketed continuous root solve on [0, 1000*2^-20].

    Verifies g(0) > 0 and g(delta_hi) < 0 (reproducing the accepted Issue #61
    smallest-authorized-delta failure), then brentq. Deterministic repeat
    agrees bit-for-bit.
    """
    delta_lo = 0.0
    delta_hi = DELTA_FLOOR

    def _g(delta: float) -> float:
        return g_delta(solver, Q, u, V_star, labor0, rho, delta)

    g0 = _g(delta_lo)
    g_hi = _g(delta_hi)
    if not (g0 > 0.0 and g_hi < 0.0):
        raise LocalGeometryFailure(
            f"bracket sign mismatch: g(0)={g0:.12g} (must be > 0), "
            f"g(delta_hi)={g_hi:.12g} (must be < 0); accepted Issue #61 "
            f"terminal evidence not reproduced")

    root = brentq(_g, delta_lo, delta_hi, xtol=BRENTQ_XTOL, rtol=BRENTQ_RTOL)
    root = float(root)
    g_cross = _g(root)

    Vr = solve_scaled_resolvent(Q, u, V_star, root, rho)
    pr, nr, zr = min_boundary_pb_state(solver, Vr, labor0)
    if not np.isfinite(pr):
        raise LocalGeometryFailure(
            f"non-finite required boundary p_b at delta_cross: {pr!r}")
    cross_worst_state = _state_info(solver, nr, zr)

    below_delta = max(delta_lo, (1.0 - EPS_VERIFY) * root)
    above_delta = min(delta_hi, (1.0 + EPS_VERIFY) * root)

    g_below = _g(below_delta)
    Vb = solve_scaled_resolvent(Q, u, V_star, below_delta, rho)
    pb_below, nb, zb = min_boundary_pb_state(solver, Vb, labor0)
    if not np.isfinite(pb_below):
        raise LocalGeometryFailure(
            f"non-finite required boundary p_b at delta_below: {pb_below!r}")
    below_state = _state_info(solver, nb, zb)

    g_above = _g(above_delta)
    Va = solve_scaled_resolvent(Q, u, V_star, above_delta, rho)
    pb_above, na, za = min_boundary_pb_state(solver, Va, labor0)
    if not np.isfinite(pb_above):
        raise LocalGeometryFailure(
            f"non-finite required boundary p_b at delta_above: {pb_above!r}")
    above_state = _state_info(solver, na, za)

    return {
        "g0": g0, "g_hi": g_hi,
        "bracket_lo": delta_lo, "bracket_hi": delta_hi,
        "delta_cross": root, "g_cross": g_cross,
        "cross_worst_state": cross_worst_state,
        "below_delta": below_delta, "below_g": g_below,
        "below_min_pb": float(pb_below), "below_state": below_state,
        "above_delta": above_delta, "above_g": g_above,
        "above_min_pb": float(pb_above), "above_state": above_state,
        "ratio_cross_over_floor": root / delta_hi,
    }


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------
def finalize_outcome(result: LocalGeometryResult,
                     repeat_identical: bool) -> str:
    """Exactly one Issue #62 terminal from the local evidence."""
    # reconstruction must reproduce the accepted Issue #61 terminal state
    trace = result.trace
    recon_ok = (len(trace) == RECONSTRUCT_ITERATIONS
                and trace[0]["delta_index"] == 15
                and trace[1]["delta_index"] == 18
                and abs(result.min_accepted_boundary_pb
                        - 0.009853744163134845) < 1e-6
                and result.terminal_state is not None
                and result.terminal_state["node"] == 332
                and result.terminal_state["family"] == "F3"
                and result.terminal_state["i"] == 13
                and result.terminal_state["j"] == 13
                and result.terminal_state["z"] == 1)
    if not recon_ok:
        return ("DLH_5VN_LOCAL_RESOLVENT_GEOMETRY__"
                "NONFINITE_OR_INCONSISTENT_LOCAL_DIRECTION_OR_MARGIN_EVIDENCE__"
                "BOUNDARY_HJB_ROUTE_REVIEW_REQUIRED")
    # local direction evidence must be finite and non-trivial
    if (result.dpb_most_negative_state is None
            or result.min_delta_margin_linear is None
            or not np.isfinite(result.dpb_most_negative)):
        return ("DLH_5VN_LOCAL_RESOLVENT_GEOMETRY__"
                "NONFINITE_OR_INCONSISTENT_LOCAL_DIRECTION_OR_MARGIN_EVIDENCE__"
                "BOUNDARY_HJB_ROUTE_REVIEW_REQUIRED")
    root = result.delta_cross
    if root is None:
        return ("DLH_5VN_LOCAL_RESOLVENT_GEOMETRY__"
                "NONFINITE_OR_INCONSISTENT_LOCAL_DIRECTION_OR_MARGIN_EVIDENCE__"
                "BOUNDARY_HJB_ROUTE_REVIEW_REQUIRED")
    below_feasible = result.below_g is not None and result.below_g > 0.0
    above_infeasible = result.above_g is not None and result.above_g < 0.0
    root_inside = (result.bracket_lo < root < result.bracket_hi)
    if not (root_inside and below_feasible and above_infeasible):
        return ("DLH_5VN_LOCAL_RESOLVENT_GEOMETRY__"
                "NONFINITE_OR_INCONSISTENT_LOCAL_DIRECTION_OR_MARGIN_EVIDENCE__"
                "BOUNDARY_HJB_ROUTE_REVIEW_REQUIRED")
    # clean vs stiff: does the same wall state dominate at root / below / above?
    wall = result.terminal_state
    same_state = (
        result.cross_worst_state is not None
        and result.below_state is not None
        and result.above_state is not None
        and result.cross_worst_state["node"] == wall["node"]
        and result.below_state["node"] == wall["node"]
        and result.above_state["node"] == wall["node"])
    # first-order prediction qualitatively reliable: min-linear state == wall
    lin_state = result.min_delta_margin_linear_state
    linear_reliable = (lin_state is not None
                       and lin_state["node"] == wall["node"])
    ratio_linear = result.ratio_cross_over_linear
    linear_scale_ok = (ratio_linear is not None
                       and np.isfinite(ratio_linear)
                       and 0.5 <= ratio_linear <= 2.0)

    if same_state and linear_reliable and linear_scale_ok and repeat_identical:
        return ("DLH_5VN_LOCAL_RESOLVENT_GEOMETRY__"
                "POSITIVE_SUBFLOOR_SAFE_STEP_AND_REPRODUCIBLE_MARGIN_CROSSING__"
                "CONTINUATION_DESIGN_GATE_READY")
    return ("DLH_5VN_LOCAL_RESOLVENT_GEOMETRY__"
            "POSITIVE_LOCAL_FEASIBILITY_WITH_STIFF_OR_NONUNIQUE_MARGIN_GEOMETRY__"
            "FURTHER_DESIGN_REQUIRED")


def run_local_geometry_diagnostic() -> LocalGeometryResult:
    """Exactly one full local diagnostic:
    1) reconstruction, 2) frozen operator (built once), 3) infinitesimal
    direction, 4) boundary direction, 5) continuous crossing."""
    rec = reconstruct_issue61_terminal_state()
    solver: BoundaryHJBSolver = rec["solver"]
    labor0: np.ndarray = rec["labor0"]
    V_star: np.ndarray = rec["V_star"]
    rho = float(solver.config.params.rho)

    # frozen operator built EXACTLY ONCE for every local delta evaluation
    Q, u, diag, _records = solver.build_operator_and_u(
        V_star, labor0, 0.0, 0.0, final=False)
    max_q1 = float(np.max(np.abs(np.asarray(Q.sum(axis=1)).ravel())))

    dV = infinitesimal_direction(Q, u, V_star, rho)
    bd = boundary_direction_diagnostic(solver, V_star, labor0, dV)
    cr = continuous_crossing_diagnostic(solver, Q, u, V_star, labor0, rho)

    terminal_pb, tn, tz = min_boundary_pb_state(solver, V_star, labor0)
    ratio_linear = None
    if bd["min_delta_margin_linear"] and bd["min_delta_margin_linear"] > 0.0:
        ratio_linear = cr["delta_cross"] / bd["min_delta_margin_linear"]

    result = LocalGeometryResult(
        outcome="", iterations=RECONSTRUCT_ITERATIONS, trace=rec["trace"],
        v0_min_boundary_pb=float(rec["v0_min_boundary_pb"]),
        min_accepted_boundary_pb=float(rec["min_accepted_boundary_pb"]),
        terminal_min_boundary_pb=float(terminal_pb),
        terminal_state=_state_info(solver, tn, tz),
        max_abs_q1=max_q1, expansions=int(diag["total_expansions"]),
        artificial_bindings=int(diag["artificial_binding"]),
        direction_max_abs=float(np.max(np.abs(dV))),
        dpb_most_negative=float(bd["dpb_most_negative"]),
        dpb_most_negative_state=bd["dpb_most_negative_state"],
        dpb_negative_count=bd["dpb_negative_count"],
        dpb_required_count=bd["dpb_required_count"],
        dpb_zero_count=bd["dpb_zero_count"],
        min_delta_margin_linear=bd["min_delta_margin_linear"],
        min_delta_margin_linear_state=bd["min_delta_margin_linear_state"],
        delta_margin_linear_count=bd["delta_margin_linear_count"],
        g0=cr["g0"], g_hi=cr["g_hi"],
        bracket_lo=cr["bracket_lo"], bracket_hi=cr["bracket_hi"],
        delta_cross=cr["delta_cross"], g_cross=cr["g_cross"],
        cross_worst_state=cr["cross_worst_state"],
        below_delta=cr["below_delta"], below_g=cr["below_g"],
        below_min_pb=cr["below_min_pb"], below_state=cr["below_state"],
        above_delta=cr["above_delta"], above_g=cr["above_g"],
        above_min_pb=cr["above_min_pb"], above_state=cr["above_state"],
        ratio_cross_over_floor=cr["ratio_cross_over_floor"],
        ratio_cross_over_linear=ratio_linear,
    )
    return result


def run_local_geometry_diagnostic_twice() -> tuple[LocalGeometryResult, bool]:
    """One full local diagnostic + one deterministic repeat (bit-identical);
    returns (finalized result with exactly one terminal, repeat_identical)."""
    r1 = run_local_geometry_diagnostic()
    r2 = run_local_geometry_diagnostic()
    fields = [
        "terminal_min_boundary_pb", "min_accepted_boundary_pb",
        "direction_max_abs", "dpb_most_negative", "min_delta_margin_linear",
        "g0", "g_hi", "delta_cross", "g_cross", "below_g", "above_g",
        "ratio_cross_over_floor", "ratio_cross_over_linear",
        "terminal_state", "cross_worst_state", "below_state", "above_state",
    ]
    identical = all(
        getattr(r1, f) == getattr(r2, f)
        for f in fields)
    identical = identical and r1.trace == r2.trace
    outcome = finalize_outcome(r1, identical)
    return (
        dataclasses.replace(
            r1, outcome=outcome,
            deterministic_repeat_identical=identical),
        identical,
    )
