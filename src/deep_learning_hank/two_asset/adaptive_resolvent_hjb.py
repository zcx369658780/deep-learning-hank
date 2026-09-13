"""DLH-5V-M adaptive pseudo-time / resolvent safeguard diagnostic.

Tests ONE question on ONE frozen central selected-Q HJB case:

    Can the accepted selected-Q HJB fixed-point equation be approached while
    preserving the accepted boundary effective domain by adapting the
    pseudo-time/resolvent parameter ``delta`` INSIDE the implicit solve,
    rather than damping an already-computed delta=1000 value update?

Read-only wrapper/driver over the ACCEPTED boundary selected-Q solver
(``boundary_hjb_selected_q.py`` is NOT modified; the accepted household oracle
is NOT touched).

Mechanism (exactly as authorized by Issue #61):

- at accepted iterate ``V_old``, build the accepted selected policy, utility
  and conservative backward ``Q`` from ``V_old`` EXACTLY ONCE:
  ``(Q, u, diag, records) = solver.build_operator_and_u(V_old, ...)``;
- for the deterministic delta sequence ``delta_k = 1000*2^-k``, ``k = 0..20``
  (descending), solve the corresponding resolvent system with the SAME
  ``(Q, u)``:

      [(1/delta + rho) I - Q] V_delta = u + V_old/delta

- choose the LARGEST delta whose ``V_trial`` satisfies ALL boundary
  effective-domain p_b evidence > 1e-12 (p_b = the declared backward liquid
  marginal vb_b over boundary, non-F0, nodes; non-finite evidence is never
  accepted);
- accept that ``V_trial`` DIRECTLY — NO additional value damping (the
  Issue #60 value-update line search is NOT layered on top);
- if no allowed delta keeps the effective domain: ``RESOLVENT_STEP_FAILURE``;
- at a fixed point ``V_delta = V_old = V`` any positive delta cancels and the
  target remains ``rho V = u(V) + Q(V) V``: this diagnostic changes the
  numerical path only, not household economics or the target HJB equation.

Integrity guarantees (per Issue #61 section 5): for a given ``V_old``,
changing delta changes ONLY the resolvent linear system — selected candidate /
controls, utility, local drift, destinations, selected rates, ``Q`` and the
z-switch process are untouched across all delta trials of one accepted iterate
(the same ``Q, u`` are reused; this is pinned by test).

The ``1e-12`` margin is an iterate-acceptance tolerance ONLY: it never
clips/floors/replaces a derivative and never enters household FOCs or Bellman
scoring.

Terminals (exactly one returned):

- A: CONVERGED_WITH_BELLMAN_PASS — iterate change < 1e-7 within 1000 accepted
  iterations, final boundary p_b > 1e-12, final Bellman residual
  ||rho V - [u + Q V]||_inf <= 1e-3, conservative final Q within the accepted
  row-sum tolerance, no accepted artificial bracket binding, deterministic
  repeat;
- B (RESOLVENT_STAGNATION / RESOLVENT_NONCONVERGENCE / preserved accepted
  selected-Q failure): domain preserved materially but validated HJB
  convergence not reached (a tiny delta-induced step with a large residual is
  STAGNATION, not convergence);
- C: RESOLVENT_STEP_FAILURE — no allowed delta on the deterministic ladder
  yields a viable positive-domain next iterate.

Exactly one adaptive-resolvent central-case run + one deterministic repeat. No
other scientific configuration. No KFE / stationary KFE / steady state / SCC.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import numpy as np
from scipy import sparse
from scipy.sparse import linalg

from deep_learning_hank.two_asset.matlab_faithful_two_asset_ha import (
    EconomicParams,
    HouseholdInputs,
)
from deep_learning_hank.two_asset.boundary_hjb_selected_q import (
    BoundaryHJBConfig,
    BoundaryHJBFailure,
    BoundaryHJBSolver,
)

# ---------------------------------------------------------------------------
# Frozen central case (Issue #61 section 3) — do NOT change
# ---------------------------------------------------------------------------
CENTRAL_PARAMS = EconomicParams(0.02, 2.0, 5.0, 0.1, 2.0, 1e-6, 0.0, 0.0)
CENTRAL_INPUTS = HouseholdInputs(
    r_a=0.07, r_b=0.02, tau=0.15, wages=np.asarray([1.00]),
    migration_costs=np.asarray([0.0]), labor_weights=np.asarray([1.0]),
)
CENTRAL_Z = np.asarray([0.8, 1.3])
CENTRAL_SWITCH = np.array([[-1.0 / 3.0, 1.0 / 3.0], [1.0 / 3.0, -1.0 / 3.0]])

# frozen solver settings (Issue #58 / #60 conventions; n_c = n_d = 9 defaults,
# bracket expansion x4 max 3 defaults)
CENTRAL_CONFIG = BoundaryHJBConfig(
    m=1, w_max=10.0, b_min=-2.0, a_max=10.0, params=CENTRAL_PARAMS,
    inputs=CENTRAL_INPUTS, z=CENTRAL_Z, switch_matrix=CENTRAL_SWITCH,
    delta=1000.0, tolerance_iter=1e-7, tolerance_bellman=1e-3,
    max_iterations=1000,
)

PB_MARGIN = 1.0e-12          # iterate-acceptance margin ONLY (never applied inside FOCs/scores)
DELTA_REF = 1000.0           # fixed aggressive reference resolvent (k = 0)
DELTA_MIN_EXP = 20           # delta ladder {1000*2^-k, k = 0..20}
MAX_ITERATIONS = 1000


def delta_ladder() -> list[float]:
    """Deterministic descending delta sequence {1000*2^-k, k = 0..20}."""
    return [DELTA_REF * 2.0 ** (-k) for k in range(DELTA_MIN_EXP + 1)]


class ResolventStepFailure(RuntimeError):
    """No allowed delta on the deterministic ladder keeps the effective domain."""


@dataclass(frozen=True)
class ResolventDiagnosticResult:
    outcome: str                       # terminal outcome / failure name
    converged: bool
    iterations: int
    final_statistic: float
    min_delta: float
    median_delta: float
    reduced_delta_iterations: int      # accepted iterations with delta < 1000
    min_accepted_boundary_pb: float
    delta1000_violation_count: int     # accepted iters where the k=0 reference violated
    final_bellman_residual: Optional[float]
    final_q_max_abs_row_sum: Optional[float]
    final_min_boundary_pb: Optional[float]
    final_artificial_bindings: Optional[int]
    final_family_histogram: Optional[dict]
    failure_detail: Optional[dict] = None
    trace: list[dict] = field(default_factory=list)

    def to_trace_csv_lines(self) -> list[str]:
        header = [
            "iteration", "selected_delta", "delta_index", "backtrack_count",
            "accepted_max_stat", "ref1000_max_stat", "ref1000_min_pb",
            "min_pb_old", "min_pb_new", "delta1000_would_violate",
            "max_abs_q1", "expansions", "artificial_bindings",
            "sector_changes",
        ]
        lines = [",".join(header)]
        for t in self.trace:
            cells = [
                str(t["iteration"]),
                f"{t['selected_delta']:.12g}", str(t["delta_index"]),
                str(t["backtrack_count"]),
                f"{t['accepted_max_stat']:.12g}",
                f"{t['ref1000_max_stat']:.12g}",
                f"{t['ref1000_min_pb']:.12g}",
                f"{t['min_pb_old']:.12g}", f"{t['min_pb_new']:.12g}",
                "true" if t["delta1000_would_violate"] else "false",
                f"{t['max_abs_q1']:.12g}", str(t["expansions"]),
                str(t["artificial_bindings"]), str(t["sector_changes"]),
            ]
            lines.append(",".join(cells))
        return lines


# ---------------------------------------------------------------------------
# Effective-domain helpers (identical semantics to the accepted Issue #60
# wrapper, kept self-contained so this diagnostic has no cross-module coupling)
# ---------------------------------------------------------------------------
def min_boundary_pb(solver: BoundaryHJBSolver, V: np.ndarray,
                    labor0: np.ndarray) -> float:
    """Minimum effective boundary liquid marginal p_b (= vb_b) over all
    boundary (non-F0) nodes of the given iterate. Non-finite evidence is
    returned as +inf so it is never accepted as positive."""
    pb, _, _ = min_boundary_pb_state(solver, V, labor0)
    return pb


def min_boundary_pb_state(solver: BoundaryHJBSolver, V: np.ndarray,
                          labor0: np.ndarray) -> tuple[float, int, int]:
    """Minimum effective boundary liquid marginal p_b plus the worst (node, nz).
    Non-finite evidence is reported as +inf with the first non-finite state."""
    vb_f, vb_b, va_f, va_b = solver.compute_derivatives(V, labor0, 0.0, 0.0)
    g = solver.grid
    best: Optional[tuple[float, int, int]] = None
    for node in range(solver.n):
        if g.families[node] == "F0":
            continue
        for nz in range(solver.nz):
            v = float(vb_b[node, nz])
            if best is None or v < best[0]:
                best = (v, node, nz)
    if best is None:
        return float("inf"), -1, -1
    return best


def _domain_ok(solver: BoundaryHJBSolver, V: np.ndarray,
               labor0: np.ndarray, margin: float = PB_MARGIN) -> bool:
    pb = min_boundary_pb(solver, V, labor0)
    return np.isfinite(pb) and pb > margin


def _state_info(solver: BoundaryHJBSolver, node: int, nz: int) -> dict:
    g = solver.grid
    return {
        "node": int(node), "j": int(g.j_arr[node]), "i": int(g.i_arr[node]),
        "z": int(nz), "family": g.families[node],
    }


# ---------------------------------------------------------------------------
# Resolvent machinery
# ---------------------------------------------------------------------------
def solve_resolvent(solver: BoundaryHJBSolver, Q: sparse.csr_matrix,
                    u: np.ndarray, V_old: np.ndarray, delta: float,
                    ) -> np.ndarray:
    """Solve [(1/delta + rho)I - Q] V_delta = u + V_old/delta with the SAME
    (Q, u). Mirrors the accepted solver's linear algebra (state vector layout
    is z-major, node-fastest: row = nz*n + node; reshape order='F')."""
    cfg = solver.config
    matrix = (1.0 / delta + cfg.params.rho) * sparse.eye(
        solver.state_size, format="csr") - Q
    rhs = u + V_old.ravel(order="F") / delta
    try:
        v_new = linalg.spsolve(matrix, rhs)
    except Exception as exc:  # pragma: no cover - defensive
        raise BoundaryHJBFailure(
            "HJB_LINEAR_SOLVE_FAILURE",
            f"linear solve raised: {exc!r}", {},
        ) from exc
    if v_new.shape != (solver.state_size,) or not np.isfinite(v_new).all():
        raise BoundaryHJBFailure(
            "HJB_LINEAR_SOLVE_FAILURE",
            "non-finite solve output", {},
        )
    return v_new.reshape((solver.n, solver.nz), order="F")


def select_largest_feasible_delta(solver: BoundaryHJBSolver, V_old: np.ndarray,
                                  labor0: np.ndarray, Q: sparse.csr_matrix,
                                  u: np.ndarray,
                                  margin: float = PB_MARGIN) -> dict:
    """Deterministic largest-feasible-delta search over the EXACT authorized
    ladder {1000*2^-k, k=0..20} (descending) using the SAME (Q, u). Returns

        k, delta, V_new, stat, ref1000_stat, ref1000_min_pb,
        delta1000_would_violate, min_pb_old

    raises ``ResolventStepFailure`` when no allowed delta keeps the domain.
    """
    ladder = delta_ladder()
    min_pb_old = min_boundary_pb(solver, V_old, labor0)
    # k = 0 trial is the fixed aggressive reference (delta = 1000)
    V_1000 = solve_resolvent(solver, Q, u, V_old, ladder[0])
    ref1000_stat = float(np.max(np.abs(V_1000 - V_old)))
    ref1000_min_pb = min_boundary_pb(solver, V_1000, labor0)
    delta1000_would_violate = not _domain_ok(solver, V_1000, labor0, margin)
    for k, delta in enumerate(ladder):
        V_delta = solve_resolvent(solver, Q, u, V_old, delta)
        if _domain_ok(solver, V_delta, labor0, margin):
            return {
                "k": k, "delta": delta, "V_new": V_delta,
                "stat": float(np.max(np.abs(V_delta - V_old))),
                "ref1000_stat": ref1000_stat,
                "ref1000_min_pb": ref1000_min_pb,
                "delta1000_would_violate": delta1000_would_violate,
                "min_pb_old": min_pb_old,
            }
    # no allowed delta keeps the domain: report the smallest-delta trial
    V_min = solve_resolvent(solver, Q, u, V_old, ladder[-1])
    raise ResolventStepFailure(
        f"no allowed delta in {{1000*2^-k, k=0..{DELTA_MIN_EXP}}} keeps "
        f"boundary p_b > {margin:g} (min boundary p_b(V_old) = "
        f"{min_pb_old:.6g}; min boundary p_b(V_min_delta) = "
        f"{min_boundary_pb(solver, V_min, labor0):.6g})"
    )


def final_bellman_validation(solver: BoundaryHJBSolver, V: np.ndarray,
                             labor0: np.ndarray,
                             records_f0: list,
                             ) -> dict:
    """Accepted post-convergence validation: final re-selection from V,
    R_Bellman = rho V - [u_selected(V) + Q_selected(V) V] (inf norm),
    Q conservation, boundary p_b, artificial bindings."""
    cfg = solver.config
    final_Q, final_u, diag_final, recs_final = solver.build_operator_and_u(
        V, labor0, 0.0, 0.0, final=True, f0_policies=records_f0,
    )
    R = cfg.params.rho * V.ravel(order="F") - (final_u + final_Q.dot(V.ravel(order="F")))
    bellman_residual = float(np.max(np.abs(R)))
    max_q1 = float(np.max(np.abs(np.asarray(final_Q.sum(axis=1)).ravel())))
    fam_hist: dict = {}
    for r in recs_final:
        if r is not None:
            fam_hist[r.family] = fam_hist.get(r.family, 0) + 1
    return {
        "bellman_residual": bellman_residual,
        "max_abs_q1": max_q1,
        "min_boundary_pb": min_boundary_pb(solver, V, labor0),
        "artificial_bindings": int(diag_final["artificial_binding"]),
        "expansions": int(diag_final["total_expansions"]),
        "family_histogram": fam_hist,
    }


def _sector_seq(records: list) -> tuple:
    return tuple((r.family, r.sector) if r is not None else ("?", "?")
                 for r in records)


def run_adaptive_resolvent_central() -> ResolventDiagnosticResult:
    """Exactly one adaptive-resolvent run of the frozen central selected-Q
    case."""
    solver = BoundaryHJBSolver(CENTRAL_CONFIG)
    labor0 = solver.build_labor0(0.0, 0.0)
    V0 = solver.build_initial_value(labor0, 0.0, 0.0)
    if not _domain_ok(solver, V0, labor0):
        raise ResolventStepFailure("initial value is outside the effective domain")
    V = V0.copy()
    trace: list[dict] = []
    prev_sector: Optional[tuple] = None
    converged = False
    statistic = float("inf")
    accepted_iterations = 0
    deltas: list[float] = []
    reduced_delta_iters = 0
    delta1000_violations = 0
    min_accepted_pb = float("inf")
    failure = None
    records = [None] * solver.state_size
    for iteration in range(1, MAX_ITERATIONS + 1):
        # build the accepted selected policy / utility / conservative Q from
        # the accepted iterate EXACTLY ONCE (all delta trials share it)
        try:
            Q, u, diag1, records = solver.build_operator_and_u(
                V, labor0, 0.0, 0.0, final=False)
        except BoundaryHJBFailure as exc:
            # preserved accepted selected-Q failure from an accepted iterate
            failure = exc.failure_name
            return ResolventDiagnosticResult(
                outcome=failure, converged=False, iterations=iteration - 1,
                final_statistic=statistic,
                min_delta=min(deltas) if deltas else DELTA_REF,
                median_delta=float(np.median(deltas)) if deltas else DELTA_REF,
                reduced_delta_iterations=reduced_delta_iters,
                min_accepted_boundary_pb=min_accepted_pb,
                delta1000_violation_count=delta1000_violations,
                final_bellman_residual=None, final_q_max_abs_row_sum=None,
                final_min_boundary_pb=None, final_artificial_bindings=None,
                final_family_histogram=None,
                failure_detail=dict(exc.detail or {}),
                trace=trace,
            )
        try:
            sel = select_largest_feasible_delta(solver, V, labor0, Q, u)
        except ResolventStepFailure as exc:
            # terminal no-viable-step diagnostics (reporting only)
            go_pb, go_node, go_nz = min_boundary_pb_state(solver, V, labor0)
            V_min = solve_resolvent(solver, Q, u, V, delta_ladder()[-1])
            sm_pb, sm_node, sm_nz = min_boundary_pb_state(solver, V_min, labor0)
            V_1000 = solve_resolvent(solver, Q, u, V, DELTA_REF)
            d1_pb, d1_node, d1_nz = min_boundary_pb_state(solver, V_1000, labor0)
            return ResolventDiagnosticResult(
                outcome="RESOLVENT_STEP_FAILURE", converged=False,
                iterations=iteration - 1, final_statistic=statistic,
                min_delta=min(deltas) if deltas else DELTA_REF,
                median_delta=float(np.median(deltas)) if deltas else DELTA_REF,
                reduced_delta_iterations=reduced_delta_iters,
                min_accepted_boundary_pb=min_accepted_pb,
                delta1000_violation_count=delta1000_violations,
                final_bellman_residual=None, final_q_max_abs_row_sum=None,
                final_min_boundary_pb=None, final_artificial_bindings=None,
                final_family_histogram=None,
                failure_detail={
                    "message": str(exc),
                    "ladder_min_delta": delta_ladder()[-1],
                    "global_old_min_pb": go_pb,
                    "global_old_min_state": _state_info(solver, go_node, go_nz),
                    "smallest_delta_trial_min_pb": sm_pb,
                    "smallest_delta_trial_state": _state_info(solver, sm_node, sm_nz),
                    "delta1000_trial_min_pb": d1_pb,
                    "delta1000_trial_state": _state_info(solver, d1_node, d1_nz),
                },
                trace=trace,
            )
        V_new = sel["V_new"]
        statistic = sel["stat"]
        pb_new = min_boundary_pb(solver, V_new, labor0)
        min_accepted_pb = min(min_accepted_pb, pb_new)
        deltas.append(sel["delta"])
        if sel["delta"] < DELTA_REF:
            reduced_delta_iters += 1
        if sel["delta1000_would_violate"]:
            delta1000_violations += 1
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
            "accepted_max_stat": statistic,
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
        accepted_iterations = iteration
        if statistic < CENTRAL_CONFIG.tolerance_iter:
            converged = True
            break
    if not converged:
        return ResolventDiagnosticResult(
            outcome="RESOLVENT_NONCONVERGENCE", converged=False,
            iterations=accepted_iterations, final_statistic=statistic,
            min_delta=min(deltas) if deltas else DELTA_REF,
            median_delta=float(np.median(deltas)) if deltas else DELTA_REF,
            reduced_delta_iterations=reduced_delta_iters,
            min_accepted_boundary_pb=min_accepted_pb,
            delta1000_violation_count=delta1000_violations,
            final_bellman_residual=None, final_q_max_abs_row_sum=None,
            final_min_boundary_pb=None, final_artificial_bindings=None,
            final_family_histogram=None, trace=trace,
        )
    # iterate convergence reached -> final Bellman validation (never manufactured)
    val = final_bellman_validation(solver, V, labor0, records)
    outcome = "CONVERGED_WITH_BELLMAN_PASS"
    if not (val["bellman_residual"] <= CENTRAL_CONFIG.tolerance_bellman
            and val["min_boundary_pb"] > PB_MARGIN
            and val["max_abs_q1"] <= CENTRAL_CONFIG.row_sum_tolerance
            and val["artificial_bindings"] == 0):
        # small accepted step with a material residual is STAGNATION, not
        # convergence (Issue #61 section 7)
        outcome = "RESOLVENT_STAGNATION"
    return ResolventDiagnosticResult(
        outcome=outcome, converged=True, iterations=accepted_iterations,
        final_statistic=statistic,
        min_delta=min(deltas) if deltas else DELTA_REF,
        median_delta=float(np.median(deltas)) if deltas else DELTA_REF,
        reduced_delta_iterations=reduced_delta_iters,
        min_accepted_boundary_pb=min_accepted_pb,
        delta1000_violation_count=delta1000_violations,
        final_bellman_residual=val["bellman_residual"],
        final_q_max_abs_row_sum=val["max_abs_q1"],
        final_min_boundary_pb=val["min_boundary_pb"],
        final_artificial_bindings=val["artificial_bindings"],
        final_family_histogram=val["family_histogram"],
        trace=trace,
    )
