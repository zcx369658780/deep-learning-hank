"""DLH-5V-O — continuous fraction-to-boundary pseudo-transient continuation on
the frozen central selected-Q HJB case.

Issue #63 / DLH-5V-O
``SCIENTIFIC_NUMERICAL_DIAGNOSTIC__CONTINUOUS_FRACTION_TO_BOUNDARY_RESOLVENT_CONTINUATION``

Authority: Issue #63 OPEN; initial activation ``5652277509``; final
authoritative activation-refresh ``5652449297`` (post-sync live ``main``
``9029e66dafa76f02cb2690c7e3152a2691350f61``). Route decision
``APPROVE_CONTINUOUS_FRACTION_TO_BOUNDARY_RESOLVENT_CONTINUATION_AFTER_5VN_OUTCOME_A``;
authority marker
``DLH_5VO_CONTINUOUS_FTB_RESOLVENT_CONTINUATION_AUTHORIZED``.

Scientific boundary (binding): single frozen central selected-Q case exactly the
accepted Issue #61/#62 configuration and initialization; continuous
fraction-to-boundary pseudo-transient controller ONLY per the frozen rules;
``Q_n,u_n`` built exactly once per accepted iterate and reused for ALL
delta/controller evaluations within that iterate (no policy re-selection as
delta varies); halving is bracket construction ONLY (not an accepted ladder);
no controller-parameter tuning after seeing trajectory results; no
economics/prices/grid/domain/``PB_MARGIN`` change; no value damping; no
clip/floor of ``p_b``; no Bellman-residual-based step selection; Stationary KFE
remains NOT AUTHORIZED. Oracle / selected-Q / Issue #61 / Issue #62
implementations are imported read-only and never modified.

Frozen controller constants (Issue #63 section 5):
``DELTA_CAP=1000``, ``TAU_FTB=0.90``, ``RETAIN=1-TAU_FTB=0.10``,
``EPS_FTB=1e-6``, ``MAX_BRACKET_HALVINGS=60``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import numpy as np
from scipy import optimize, sparse
from scipy.sparse import linalg

from deep_learning_hank.two_asset.boundary_hjb_selected_q import (
    BoundaryHJBFailure,
    BoundaryHJBSolver,
)
from deep_learning_hank.two_asset.adaptive_resolvent_hjb import (
    CENTRAL_CONFIG,
    CENTRAL_INPUTS,
    CENTRAL_PARAMS,
    CENTRAL_SWITCH,
    CENTRAL_Z,
    MAX_ITERATIONS,
    PB_MARGIN,
    final_bellman_validation,
    min_boundary_pb,
    min_boundary_pb_state,
)

# ---------------------------------------------------------------------------
# Frozen controller constants (Issue #63 section 5)
# ---------------------------------------------------------------------------
DELTA_CAP = 1000.0
TAU_FTB = 0.90
RETAIN = 1.0 - TAU_FTB               # 0.10 retained-margin fraction
EPS_FTB = 1e-6                       # root-interior factor
MAX_BRACKET_HALVINGS = 60
CONVERGENCE_TOL = 1e-7               # accepted-step trigger max|V_{n+1}-V_n|
BELLMAN_TOL = 1e-3                   # final Bellman inf-norm tolerance
FTB_RETAIN_TOL = 1e-9                # declared numerical root tolerance (margin units)
BRENTQ_XTOL = 1e-15
BRENTQ_RTOL = 4.0 * np.finfo(float).eps

# ---------------------------------------------------------------------------
# Terminals (Issue #63 section 11) — exactly ONE returned by the run
# ---------------------------------------------------------------------------
TERMINAL_A = ("DLH_5VO_CONTINUOUS_FTB_RESOLVENT__CENTRAL_HJB_CONVERGES_WITH_"
              "FINAL_BELLMAN_PASS__ROBUSTNESS_GATE_READY")
TERMINAL_B = ("DLH_5VO_CONTINUOUS_FTB_RESOLVENT__EFFECTIVE_DOMAIN_PRESERVED_"
              "BUT_VALIDATED_HJB_CONVERGENCE_NOT_REACHED")
TERMINAL_C = ("DLH_5VO_CONTINUOUS_FTB_RESOLVENT__NO_VIABLE_FRACTION_TO_BOUNDARY_"
              "STEP__BOUNDARY_HJB_ROUTE_REVIEW_REQUIRED")
TERMINAL_BLOCKED = "BLOCKED_DLH_5VO_AUTHORITY_OR_DEPENDENCY_CONFLICT"

FTB_STEP_CONSTRUCTION_FAILURE = "FTB_STEP_CONSTRUCTION_FAILURE"
FTB_STAGNATION = "FTB_STAGNATION"


class FTBStepConstructionFailure(Exception):
    """Fail-closed: the frozen controller cannot construct a viable positive
    FTB step (non-finite required boundary evidence, non-positive margin, or no
    sign-changing bracket within MAX_BRACKET_HALVINGS)."""


def _state_info(solver: BoundaryHJBSolver, node: int, nz: int) -> dict:
    g = solver.grid
    return {
        "node": int(node), "j": int(g.j_arr[node]), "i": int(g.i_arr[node]),
        "z": int(nz), "family": g.families[node],
    }


def _sector_seq(records: list) -> tuple:
    return tuple((r.family, r.sector) if r is not None else ("?", "?")
                 for r in records)


def solve_resolvent_scaled(solver: BoundaryHJBSolver, Q: sparse.csr_matrix,
                           u: np.ndarray, V_n: np.ndarray, delta: float,
                           rho: float) -> np.ndarray:
    """[I + delta*(rho I - Q)] V(delta) = V_n + delta*u  (Issue #63 section 4).

    Well-defined at delta = 0 (V(0) = V_n); algebraically identical to the
    accepted Issue #61 resolvent form for delta > 0. State layout z-major,
    node-fastest (row = nz*n + node; reshape order='F')."""
    n = solver.state_size
    matrix = sparse.eye(n, format="csr") + delta * (
        rho * sparse.eye(n, format="csr") - Q)
    rhs = V_n.ravel(order="F") + delta * u.ravel(order="F")
    try:
        v_new = linalg.spsolve(matrix, rhs)
    except Exception as exc:  # pragma: no cover - defensive
        raise BoundaryHJBFailure(
            "HJB_LINEAR_SOLVE_FAILURE",
            f"scaled resolvent solve raised: {exc!r}", {}) from exc
    if v_new.shape != (n,) or not np.isfinite(v_new).all():
        raise BoundaryHJBFailure(
            "HJB_LINEAR_SOLVE_FAILURE", "non-finite scaled resolvent output", {})
    return v_new.reshape((solver.n, solver.nz), order="F")


def ftb_h_value(solver: BoundaryHJBSolver, Q: sparse.csr_matrix, u: np.ndarray,
                V_n: np.ndarray, labor0: np.ndarray, delta: float, rho: float,
                m_target: float) -> float:
    """h_n(delta) = min_required_boundary p_b(V_n(delta)) - PB_MARGIN - m_target.

    FAIL-CLOSED: non-finite required boundary evidence RAISES
    ``FTBStepConstructionFailure`` — it is never returned as +inf (which would
    be misread as feasible)."""
    Vd = solve_resolvent_scaled(solver, Q, u, V_n, delta, rho)
    pb = min_boundary_pb(solver, Vd, labor0)
    if not np.isfinite(pb):
        raise FTBStepConstructionFailure(
            f"non-finite required boundary p_b at delta={delta:.12g}: {pb!r}")
    return float(pb) - PB_MARGIN - m_target


def construct_ftb_step(solver: BoundaryHJBSolver, V_n: np.ndarray,
                       labor0: np.ndarray, Q: sparse.csr_matrix, u: np.ndarray,
                       rho: float) -> dict:
    """Continuous fraction-to-boundary step selection on the FROZEN (Q_n,u_n).

    Rule (Issue #63 section 5):
    - m0 = min_required_boundary p_b(V_n) - PB_MARGIN; require finite m0 > 0;
    - m_target = RETAIN * m0;
    - if finite h_n(DELTA_CAP) >= 0: delta_selected = DELTA_CAP (cap path);
    - else deterministic halving DELTA_CAP/2^k (BRACKET CONSTRUCTION ONLY, not an
      accepted ladder) until the first finite h_n(delta_lo) > 0 with the
      immediately previous point h_n(delta_hi) < 0, then deterministic brentq on
      h_n = 0 with root delta_ftb and delta_selected = (1 - EPS_FTB)*delta_ftb;
    - direct verification at delta_selected: p_b finite, min p_b > PB_MARGIN,
      retained margin >= m_target up to the declared numerical root tolerance.
    Returns the step record with V_new. FAIL-CLOSED on any contract violation.
    """
    m0 = min_boundary_pb(solver, V_n, labor0) - PB_MARGIN
    if not np.isfinite(m0) or m0 <= 0.0:
        raise FTBStepConstructionFailure(
            f"non-finite or non-positive margin before step construction: "
            f"m0={m0!r}")
    m_target = RETAIN * m0
    h_cap = ftb_h_value(solver, Q, u, V_n, labor0, DELTA_CAP, rho, m_target)
    cap_direct = bool(np.isfinite(h_cap) and h_cap >= 0.0)
    path = "cap" if cap_direct else "root"
    delta_lo: Optional[float] = None
    delta_hi: Optional[float] = None
    delta_ftb: Optional[float] = None
    delta_selected = DELTA_CAP
    halving_count = 0
    if not cap_direct:
        # bracket construction ONLY by deterministic halving (not a ladder)
        prev_delta = DELTA_CAP
        prev_h = float(h_cap)
        found = False
        for k in range(1, MAX_BRACKET_HALVINGS + 1):
            delta_k = DELTA_CAP * 0.5 ** k
            h_k = ftb_h_value(solver, Q, u, V_n, labor0, delta_k, rho, m_target)
            halving_count = k
            if h_k > 0.0:
                if not (prev_h < 0.0):
                    raise FTBStepConstructionFailure(
                        "halving found a positive probe but the immediately "
                        "previous point is not negative (inconsistent bracket)")
                delta_lo = float(delta_k)
                delta_hi = float(prev_delta)
                found = True
                break
            prev_delta = delta_k
            prev_h = h_k
        if not found:
            raise FTBStepConstructionFailure(
                f"no sign-changing bracket within {MAX_BRACKET_HALVINGS} "
                f"halvings (h(cap)={h_cap:.6e}, all smaller halving probes "
                f"non-positive)")
        root = optimize.brentq(
            lambda d: ftb_h_value(solver, Q, u, V_n, labor0, d, rho, m_target),
            delta_lo, delta_hi, xtol=BRENTQ_XTOL, rtol=BRENTQ_RTOL)
        delta_ftb = float(root)
        delta_selected = (1.0 - EPS_FTB) * delta_ftb
    # direct verification at delta_selected (Issue #63 section 5 item 7)
    V_new = solve_resolvent_scaled(solver, Q, u, V_n, delta_selected, rho)
    pb_sel = min_boundary_pb(solver, V_new, labor0)
    if not np.isfinite(pb_sel):
        raise FTBStepConstructionFailure(
            f"non-finite required boundary p_b at delta_selected="
            f"{delta_selected:.12g}: {pb_sel!r}")
    if not (pb_sel > PB_MARGIN):
        raise FTBStepConstructionFailure(
            f"selected delta fails min p_b > PB_MARGIN: pb={pb_sel!r} at "
            f"delta={delta_selected:.12g}")
    retained_margin = float(pb_sel) - PB_MARGIN
    if not (retained_margin >= m_target - FTB_RETAIN_TOL):
        raise FTBStepConstructionFailure(
            f"selected delta fails retained-margin target: retained="
            f"{retained_margin:.12g} < m_target={m_target:.12g} "
            f"(tolerance {FTB_RETAIN_TOL})")
    return {
        "V_new": V_new,
        "m0": float(m0),
        "m_target": float(m_target),
        "h_cap": float(h_cap),
        "cap_direct": cap_direct,
        "path": path,
        "halving_count": halving_count,
        "delta_lo": delta_lo,
        "delta_hi": delta_hi,
        "delta_ftb": delta_ftb,
        "delta_selected": float(delta_selected),
        "selected_min_pb": float(pb_sel),
        "retained_margin": retained_margin,
        "retained_ratio": retained_margin / m_target if m_target > 0 else None,
    }


def single_ftb_iterate(solver: BoundaryHJBSolver, V: np.ndarray,
                       labor0: np.ndarray, rho: Optional[float] = None) -> dict:
    """Build (Q_n,u_n) exactly once and construct/verify one accepted FTB step.

    Used to pin the build-once-and-reuse contract: the step construction and
    verification call no operator build (all controller evaluations reuse the
    same frozen (Q,u))."""
    if rho is None:
        rho = float(solver.config.params.rho)
    Q, u, diag, records = solver.build_operator_and_u(
        V, labor0, 0.0, 0.0, final=False)
    step = construct_ftb_step(solver, V, labor0, Q, u, rho)
    max_q1 = float(np.max(np.abs(np.asarray(Q.sum(axis=1)).ravel())))
    direction = u + Q.dot(V.ravel(order="F")) - rho * V.ravel(order="F")
    return {
        "Q": Q, "u": u, "diag": diag, "records": records,
        "max_abs_q1": max_q1,
        "direction_norm": float(np.max(np.abs(direction))),
        "step": step,
    }


@dataclass
class FTBContinuationResult:
    outcome: str                       # exactly ONE terminal
    converged: bool
    accepted_iterations: int
    final_statistic: Optional[float]
    final_bellman_residual: Optional[float]
    final_max_abs_q1: Optional[float]
    final_min_boundary_pb: Optional[float]
    final_artificial_bindings: Optional[int]
    final_expansions: Optional[int]
    final_family_histogram: Optional[dict]
    min_accepted_boundary_pb: float
    failure_detail: dict
    controller_summary: dict
    trace: list = field(default_factory=list)

    def to_summary_csv_lines(self) -> list:
        rows = [
            ("outcome", self.outcome),
            ("converged", str(self.converged)),
            ("accepted_iterations", str(self.accepted_iterations)),
            ("final_statistic", _fmt(self.final_statistic)),
            ("final_bellman_residual", _fmt(self.final_bellman_residual)),
            ("final_max_abs_q1", _fmt(self.final_max_abs_q1)),
            ("final_min_boundary_pb", _fmt(self.final_min_boundary_pb)),
            ("final_artificial_bindings",
             _fmt(self.final_artificial_bindings)),
            ("final_expansions", _fmt(self.final_expansions)),
            ("min_accepted_boundary_pb", _fmt(self.min_accepted_boundary_pb)),
        ]
        for k, v in sorted(self.controller_summary.items()):
            rows.append((f"controller.{k}", _fmt(v)))
        return rows


def _fmt(x) -> str:
    if x is None:
        return ""
    if isinstance(x, float):
        return repr(x)
    if isinstance(x, dict):
        return str(x)
    return str(x)


def run_ftb_continuation_with(solver: BoundaryHJBSolver, labor0: np.ndarray,
                              V0: np.ndarray,
                              max_iterations: int = MAX_ITERATIONS,
                              rho: Optional[float] = None) -> FTBContinuationResult:
    """Exactly one continuous FTB continuation run on the given frozen case
    (defaults to the frozen central selected-Q case; ``max_iterations`` is an
    execution-length override used only by bounded test runs, never a controller
    parameter)."""
    if rho is None:
        rho = float(solver.config.params.rho)
    V = np.array(V0, dtype=float)
    m0_init = min_boundary_pb(solver, V, labor0) - PB_MARGIN
    if not (np.isfinite(m0_init) and m0_init > 0.0):
        return FTBContinuationResult(
            outcome=TERMINAL_C, converged=False, accepted_iterations=0,
            final_statistic=None, final_bellman_residual=None,
            final_max_abs_q1=None, final_min_boundary_pb=None,
            final_artificial_bindings=None, final_expansions=None,
            final_family_histogram=None, min_accepted_boundary_pb=float("inf"),
            failure_detail={"message": "initial value outside the effective "
                            "domain (m0 not finite and positive)",
                            "m0": _fmt(m0_init)},
            controller_summary={}, trace=[])

    trace: list = []
    prev_sector: Optional[tuple] = None
    records: list = [None] * solver.state_size
    accepted = 0
    statistic = float("inf")
    converged = False
    min_accepted_pb = float("inf")
    outcome: Optional[str] = None
    failure_detail: dict = {}
    cap_count = 0
    root_count = 0
    deltas: list = []
    halving_counts: list = []

    for iteration in range(1, max_iterations + 1):
        # accepted selected policy / utility / conservative backward Q_n,u_n
        # built EXACTLY ONCE; all controller evaluations in this iterate reuse it
        try:
            Q, u, diag, records = solver.build_operator_and_u(
                V, labor0, 0.0, 0.0, final=False)
        except BoundaryHJBFailure as exc:
            outcome = TERMINAL_C
            failure_detail = {
                "message": "accepted selected-Q build failure on an accepted "
                           "iterate", "failure_name": exc.failure_name,
                "iteration": iteration,
                "detail": dict(exc.detail or {}),
            }
            break
        max_q1 = float(np.max(np.abs(np.asarray(Q.sum(axis=1)).ravel())))
        expansions = int(diag["total_expansions"])
        bindings = int(diag["artificial_binding"])
        sector_now = _sector_seq(records)
        changes = (sum(1 for x, y in zip(prev_sector, sector_now) if x != y)
                   if prev_sector is not None else 0)
        prev_sector = sector_now
        direction_norm = float(np.max(np.abs(
            u + Q.dot(V.ravel(order="F")) - rho * V.ravel(order="F"))))
        worst_before = min_boundary_pb_state(solver, V, labor0)
        try:
            step = construct_ftb_step(solver, V, labor0, Q, u, rho)
        except FTBStepConstructionFailure as exc:
            outcome = TERMINAL_C
            failure_detail = {
                "message": str(exc), "iteration": iteration,
                "min_pb_Vn": min_boundary_pb(solver, V, labor0),
                "m0": _fmt(min_boundary_pb(solver, V, labor0) - PB_MARGIN),
            }
            break
        V_new = step["V_new"]
        statistic = float(np.max(np.abs((V_new - V).ravel())))
        pb_new = min_boundary_pb(solver, V_new, labor0)
        min_accepted_pb = min(min_accepted_pb, pb_new)
        worst_after = min_boundary_pb_state(solver, V_new, labor0)
        if step["cap_direct"]:
            cap_count += 1
        else:
            root_count += 1
        deltas.append(step["delta_selected"])
        halving_counts.append(step["halving_count"])
        trace.append({
            "iteration": iteration,
            "path": step["path"],
            "min_pb_Vn": float(min_boundary_pb(solver, V, labor0)),
            "m0": step["m0"],
            "m_target": step["m_target"],
            "h_cap": step["h_cap"],
            "cap_direct": step["cap_direct"],
            "halving_count": step["halving_count"],
            "delta_lo": step["delta_lo"],
            "delta_hi": step["delta_hi"],
            "delta_ftb": step["delta_ftb"],
            "delta_selected": step["delta_selected"],
            "accepted_max_stat": statistic,
            "selected_min_pb": step["selected_min_pb"],
            "retained_margin": step["retained_margin"],
            "retained_ratio": step["retained_ratio"],
            "worst_before": _state_info(solver, worst_before[1], worst_before[2]),
            "worst_after": _state_info(solver, worst_after[1], worst_after[2]),
            "max_abs_q1": max_q1,
            "expansions": expansions,
            "artificial_bindings": bindings,
            "sector_changes": changes,
            "direction_norm": direction_norm,
        })
        V = V_new
        accepted = iteration
        if statistic < CONVERGENCE_TOL:
            converged = True
            break

    controller_summary = {
        "cap_steps": cap_count,
        "root_steps": root_count,
        "min_selected_delta": float(min(deltas)) if deltas else None,
        "median_selected_delta": float(np.median(deltas)) if deltas else None,
        "max_selected_delta": float(max(deltas)) if deltas else None,
        "total_halving_probes": int(sum(halving_counts)),
    }

    if outcome is None and not converged:
        # max-iteration exhaustion without validated convergence -> bounded
        # non-convergence (effective domain preserved by the acceptance contract)
        outcome = TERMINAL_B
        failure_detail = {
            "message": "max_iterations reached without validated convergence",
            "iterations": accepted, "final_statistic": statistic,
        }
    if outcome is None and converged:
        # final re-selection / validation (Issue #63 section 7)
        val = final_bellman_validation(solver, V, labor0, records)
        bellman_ok = (val["bellman_residual"] <= BELLMAN_TOL
                      and val["min_boundary_pb"] > PB_MARGIN
                      and val["max_abs_q1"] <= CENTRAL_CONFIG.row_sum_tolerance
                      and val["artificial_bindings"] == 0)
        if bellman_ok:
            outcome = TERMINAL_A
        else:
            outcome = TERMINAL_B   # FTB_STAGNATION: tiny step, Bellman fails
            failure_detail = {
                "message": FTB_STAGNATION,
                "final_bellman_residual": val["bellman_residual"],
                "final_min_boundary_pb": val["min_boundary_pb"],
                "final_max_abs_q1": val["max_abs_q1"],
                "final_artificial_bindings": val["artificial_bindings"],
            }
        return FTBContinuationResult(
            outcome=outcome, converged=converged,
            accepted_iterations=accepted, final_statistic=statistic,
            final_bellman_residual=val["bellman_residual"],
            final_max_abs_q1=val["max_abs_q1"],
            final_min_boundary_pb=val["min_boundary_pb"],
            final_artificial_bindings=val["artificial_bindings"],
            final_expansions=val["expansions"],
            final_family_histogram=val["family_histogram"],
            min_accepted_boundary_pb=min_accepted_pb,
            failure_detail=failure_detail,
            controller_summary=controller_summary, trace=trace)

    return FTBContinuationResult(
        outcome=outcome, converged=converged,
        accepted_iterations=accepted, final_statistic=statistic,
        final_bellman_residual=None, final_max_abs_q1=None,
        final_min_boundary_pb=None, final_artificial_bindings=None,
        final_expansions=None, final_family_histogram=None,
        min_accepted_boundary_pb=min_accepted_pb,
        failure_detail=failure_detail,
        controller_summary=controller_summary, trace=trace)


def _results_identical(r1: FTBContinuationResult, r2: FTBContinuationResult) -> bool:
    def canon(x):
        if isinstance(x, dict):
            return tuple(sorted((k, canon(v)) for k, v in x.items()))
        if isinstance(x, list):
            return tuple(canon(v) for v in x)
        if isinstance(x, float):
            return ("f", repr(x))
        return (type(x).__name__, str(x))

    return (canon(r1.outcome) == canon(r2.outcome)
            and canon(r1.accepted_iterations) == canon(r2.accepted_iterations)
            and canon(r1.final_statistic) == canon(r2.final_statistic)
            and canon(r1.final_bellman_residual) == canon(r2.final_bellman_residual)
            and canon(r1.final_max_abs_q1) == canon(r2.final_max_abs_q1)
            and canon(r1.final_min_boundary_pb) == canon(r2.final_min_boundary_pb)
            and canon(r1.final_artificial_bindings) == canon(r2.final_artificial_bindings)
            and canon(r1.final_expansions) == canon(r2.final_expansions)
            and canon(r1.controller_summary) == canon(r2.controller_summary)
            and canon(r1.trace) == canon(r2.trace))


def run_ftb_continuation() -> FTBContinuationResult:
    """Exactly ONE continuous FTB continuation run on the frozen central
    selected-Q case (Issue #63 section 8)."""
    solver = BoundaryHJBSolver(CENTRAL_CONFIG)
    labor0 = solver.build_labor0(0.0, 0.0)
    V0 = solver.build_initial_value(labor0, 0.0, 0.0)
    return run_ftb_continuation_with(solver, labor0, V0)


def run_ftb_continuation_twice() -> tuple[FTBContinuationResult,
                                          FTBContinuationResult, bool]:
    """The one authorized run plus ONE deterministic repeat; returns
    (run, repeat, identical)."""
    r1 = run_ftb_continuation()
    r2 = run_ftb_continuation()
    return r1, r2, _results_identical(r1, r2)
