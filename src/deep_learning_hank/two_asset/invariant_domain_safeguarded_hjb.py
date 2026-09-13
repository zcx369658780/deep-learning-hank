"""DLH-5V-L invariant-domain safeguarded value-update line search.

Tests ONE question on ONE frozen central selected-Q HJB case:

    Can the accepted selected-Q HJB keep every accepted value iterate inside
    the required positive boundary-liquid-marginal effective domain by
    safeguarding ONLY the value-update acceptance step?

Read-only wrapper/driver over the ACCEPTED boundary selected-Q solver
(``boundary_hjb_selected_q.py`` is NOT modified; the accepted household oracle
is NOT touched).

Mechanism (exactly as authorized):

- at accepted iterate ``V_old`` the accepted solver's raw implicit update is
  ``V_raw = T(V_old)`` (accepted operator + utility + (1/delta + rho) I - Q
  linear solve, i.e. the accepted production iteration step);
- only the ACCEPTANCE of the raw update may be damped:
  ``V_trial(lambda) = V_old + lambda * (V_raw - V_old)``;
- allowed lambda sequence EXACTLY {2^-k, k = 0..20} (descending); choose the
  LARGEST lambda with ALL boundary effective-domain p_b evidence > 1e-12
  (p_b = the declared backward liquid marginal vb_b over boundary, non-F0,
  nodes; non-finite evidence is never accepted);
- the 1e-12 margin is ONLY an iterate-acceptance numerical margin: it never
  replaces, floors or clips p_b and never enters the consumption FOC, labor
  FOC, transfer choice or Bellman score;
- if no dyadic lambda through 2^-20 keeps the domain: INVARIANT_STEP_FAILURE;
- no candidate / rate / Q / utility / destination / sector modification, no
  policy clipping, no pseudo-time adaptation, no continuation;
- the fixed-point target for every accepted lambda > 0 remains
  ``V_raw = V_old`` (no convergence theorem is claimed).

Terminals (exactly one returned):

- A: CONVERGED_WITH_BELLMAN_PASS — iterate change < 1e-7 within 1000 accepted
  iterations, final boundary p_b > 1e-12, final Bellman residual
  ||rho V - [u + Q V]||_inf <= 1e-3, conservative final Q, no accepted
  artificial bracket binding, deterministic repeat;
- B: SAFEGUARD_STAGNATION — iterate convergence reached but the final Bellman
  validation fails (damped step tiny while the residual is materially
  nonzero); or HJB_NONCONVERGENCE — 1000 accepted iterations exhausted;
- preserved accepted selected-Q failures if they occur while constructing an
  operator from an already accepted safeguarded iterate;
- C: INVARIANT_STEP_FAILURE — no allowed positive dyadic step keeps the
  domain.

Exactly one safeguarded central-case run + one deterministic repeat. No other
scientific configuration. No KFE / stationary KFE / steady state / SCC.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import numpy as np

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
# Frozen central case (Issue #60 §2) — do NOT change
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
LAMBDA_MIN_EXP = 20          # lambda in {2^-k, k = 0..20}
MAX_ITERATIONS = 1000


class InvariantStepFailure(RuntimeError):
    """No allowed dyadic lambda in {2^-k, k=0..20} keeps the effective domain."""


@dataclass(frozen=True)
class SafeguardDiagnosticResult:
    outcome: str                       # terminal outcome / failure name
    converged: bool
    iterations: int
    final_statistic: float
    min_lambda: float
    median_lambda: float
    backtracking_iterations: int
    min_accepted_boundary_pb: float
    raw_domain_violations_avoided: int
    final_bellman_residual: Optional[float]
    final_q_max_abs_row_sum: Optional[float]
    final_min_boundary_pb: Optional[float]
    final_artificial_bindings: Optional[int]
    final_family_histogram: Optional[dict]
    failure_detail: Optional[dict] = None
    trace: list[dict] = field(default_factory=list)

    def to_trace_csv_lines(self) -> list[str]:
        header = [
            "iteration", "raw_max_stat", "accepted_max_stat", "lambda",
            "backtrack_count", "min_pb_old", "min_pb_raw", "min_pb_new",
            "lambda1_would_violate", "max_abs_q1", "expansions",
            "artificial_bindings", "sector_changes",
        ]
        lines = [",".join(header)]
        for t in self.trace:
            cells = [
                str(t["iteration"]),
                f"{t['raw_max_stat']:.12g}", f"{t['accepted_max_stat']:.12g}",
                f"{t['lambda']:.12g}", str(t["backtrack_count"]),
                f"{t['min_pb_old']:.12g}", f"{t['min_pb_raw']:.12g}",
                f"{t['min_pb_new']:.12g}",
                "true" if t["lambda1_would_violate"] else "false",
                f"{t['max_abs_q1']:.12g}", str(t["expansions"]),
                str(t["artificial_bindings"]), str(t["sector_changes"]),
            ]
            lines.append(",".join(cells))
        return lines


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


def crossing_lambdas(p_old: float, p_raw: float,
                     margin: float = PB_MARGIN) -> dict:
    """DIAGNOSTIC-ONLY continuous crossing quantities at one boundary state.

    For the affine trial evidence ``p_trial(lambda) = p_old + lambda*(p_raw
    - p_old)``:

    - ``lambda_zero_crossing = p_old/(p_old - p_raw)``: the continuous step
      crossing p_b = 0;
    - ``lambda_margin_crossing = (p_old - margin)/(p_old - p_raw)``: the
      continuous step crossing the acceptance margin p_b = PB_MARGIN.

    These are REPORTING metrics only. They are NEVER used to choose a step,
    never add lambda candidates, never authorize lambda below 2^-20, and never
    alter p_b / candidate scoring / Q / controls. The actual safeguard remains
    exactly the authorized dyadic search {2^-k, k=0..20} taking the largest
    feasible lambda. Quantities that are not mathematically defined (non-finite
    inputs, denominator <= 0, or p_old not above margin above p_raw) are None.
    """
    out = {"lambda_zero_crossing": None, "lambda_margin_crossing": None}
    if not (np.isfinite(p_old) and np.isfinite(p_raw)):
        return out
    denom = p_old - p_raw
    if denom <= 0.0:
        return out
    out["lambda_zero_crossing"] = float(p_old / denom)
    if p_old > margin > p_raw:
        out["lambda_margin_crossing"] = float((p_old - margin) / denom)
    return out


def terminal_crossing_diagnostics(solver: BoundaryHJBSolver, V_old: np.ndarray,
                                  V_raw: np.ndarray, labor0: np.ndarray,
                                  margin: float = PB_MARGIN) -> dict:
    """DIAGNOSTIC-ONLY crossing metrics at the terminal BINDING state.

    The binding state is the boundary state achieving the smallest continuous
    margin-crossing lambda (the state that blocks every authorized dyadic
    step): p_old and p_raw are reported AT THE SAME STATE so that
    lambda_margin_crossing = (p_old - margin)/(p_old - p_raw) is exact.
    Read-only; never changes step selection."""
    g = solver.grid
    _, vb_b_old, _, _ = solver.compute_derivatives(V_old, labor0, 0.0, 0.0)
    _, vb_b_raw, _, _ = solver.compute_derivatives(V_raw, labor0, 0.0, 0.0)
    best: Optional[tuple] = None   # (lambda_margin, p_old, p_raw, node, nz)
    for node in range(solver.n):
        if g.families[node] == "F0":
            continue
        for nz in range(solver.nz):
            po = float(vb_b_old[node, nz])
            pr = float(vb_b_raw[node, nz])
            if not (np.isfinite(po) and np.isfinite(pr)):
                continue
            denom = po - pr
            if denom <= 0.0 or not (po > margin > pr):
                continue
            lm = (po - margin) / denom
            if best is None or lm < best[0]:
                best = (lm, po, pr, node, nz)
    if best is None:
        return {
            "p_old": None, "p_raw": None, "PB_MARGIN": float(margin),
            "lambda_margin_crossing": None, "lambda_zero_crossing": None,
            "min_authorized_dyadic_lambda": 2.0 ** (-LAMBDA_MIN_EXP),
            "worst_state": None,
        }
    lm, po, pr, node, nz = best
    return {
        "p_old": po,
        "p_raw": pr,
        "PB_MARGIN": float(margin),
        "lambda_margin_crossing": lm,
        "lambda_zero_crossing": crossing_lambdas(po, pr, margin)[
            "lambda_zero_crossing"],
        "min_authorized_dyadic_lambda": 2.0 ** (-LAMBDA_MIN_EXP),
        "worst_state": {
            "node": int(node), "j": int(g.j_arr[node]),
            "i": int(g.i_arr[node]), "z": int(nz),
            "family": g.families[node],
        },
    }


def safeguard_step(solver: BoundaryHJBSolver, V_old: np.ndarray,
                   V_raw: np.ndarray, labor0: np.ndarray,
                   margin: float = PB_MARGIN,
                   ) -> tuple[float, int]:
    """Deterministic dyadic backtracking: largest lambda in {2^-k, k=0..20}
    with ALL boundary p_b > margin. Returns (lambda, backtrack_count);
    raises InvariantStepFailure if no allowed step exists."""
    if _domain_ok(solver, V_raw, labor0, margin):
        return 1.0, 0
    for k in range(1, LAMBDA_MIN_EXP + 1):
        lam = 2.0 ** (-k)
        if _domain_ok(solver, V_old + lam * (V_raw - V_old), labor0, margin):
            return lam, k
    raise InvariantStepFailure(
        f"no allowed dyadic lambda in {{2^-k, k=0..{LAMBDA_MIN_EXP}}} keeps "
        f"boundary p_b > {margin:g} (min boundary p_b(V_raw) = "
        f"{min_boundary_pb(solver, V_raw, labor0):.6g})"
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


def run_safeguarded_central() -> SafeguardDiagnosticResult:
    """Exactly one safeguarded run of the frozen central selected-Q case."""
    solver = BoundaryHJBSolver(CENTRAL_CONFIG)
    labor0 = solver.build_labor0(0.0, 0.0)
    V0 = solver.build_initial_value(labor0, 0.0, 0.0)
    if not _domain_ok(solver, V0, labor0):
        raise InvariantStepFailure("initial value is outside the effective domain")
    V = V0.copy()
    trace: list[dict] = []
    prev_sector: Optional[tuple] = None
    converged = False
    statistic = float("inf")
    accepted_iterations = 0
    lambdas: list[float] = []
    raw_violations_avoided = 0
    min_accepted_pb = float("inf")
    failure = None
    records = [None] * solver.state_size
    for iteration in range(1, MAX_ITERATIONS + 1):
        # raw implicit update from the ACCEPTED iterate (accepted solver machinery)
        try:
            V_raw, stat_raw, records = solver._step(
                V, labor0, 0.0, 0.0, iteration)
        except BoundaryHJBFailure as exc:
            # preserved accepted selected-Q failure from an accepted iterate
            failure = exc.failure_name
            return SafeguardDiagnosticResult(
                outcome=failure, converged=False, iterations=iteration - 1,
                final_statistic=statistic,
                min_lambda=min(lambdas) if lambdas else 1.0,
                median_lambda=float(np.median(lambdas)) if lambdas else 1.0,
                backtracking_iterations=sum(1 for l in lambdas if l < 1.0),
                min_accepted_boundary_pb=min_accepted_pb,
                raw_domain_violations_avoided=raw_violations_avoided,
                final_bellman_residual=None, final_q_max_abs_row_sum=None,
                final_min_boundary_pb=None, final_artificial_bindings=None,
                final_family_histogram=None, failure_detail=dict(exc.detail or {}),
                trace=trace,
            )
        pb_old = min_boundary_pb(solver, V, labor0)
        pb_raw = min_boundary_pb(solver, V_raw, labor0)
        try:
            lam, backtracks = safeguard_step(solver, V, V_raw, labor0)
        except InvariantStepFailure as exc:
            crossing = terminal_crossing_diagnostics(solver, V, V_raw, labor0)
            return SafeguardDiagnosticResult(
                outcome="INVARIANT_STEP_FAILURE", converged=False,
                iterations=iteration - 1, final_statistic=statistic,
                min_lambda=min(lambdas) if lambdas else 1.0,
                median_lambda=float(np.median(lambdas)) if lambdas else 1.0,
                backtracking_iterations=sum(1 for l in lambdas if l < 1.0),
                min_accepted_boundary_pb=min_accepted_pb,
                raw_domain_violations_avoided=raw_violations_avoided,
                final_bellman_residual=None, final_q_max_abs_row_sum=None,
                final_min_boundary_pb=crossing["p_raw"],
                final_artificial_bindings=None,
                final_family_histogram=None,
                failure_detail={
                    "message": str(exc),
                    "raw_min_boundary_pb": crossing["p_raw"],
                    "old_min_boundary_pb": crossing["p_old"],
                    "worst_raw_state": crossing["worst_state"],
                    "terminal_crossing_diagnostics": {
                        "p_old": crossing["p_old"],
                        "p_raw": crossing["p_raw"],
                        "PB_MARGIN": crossing["PB_MARGIN"],
                        "lambda_margin_crossing":
                            crossing["lambda_margin_crossing"],
                        "lambda_zero_crossing":
                            crossing["lambda_zero_crossing"],
                        "min_authorized_dyadic_lambda":
                            crossing["min_authorized_dyadic_lambda"],
                        "worst_state": crossing["worst_state"],
                    },
                },
                trace=trace,
            )
        lambda1_violates = not _domain_ok(solver, V_raw, labor0)
        if backtracks > 0:
            raw_violations_avoided += 1
        V_new = V + lam * (V_raw - V)
        statistic = float(np.max(np.abs(V_new - V)))
        pb_new = min_boundary_pb(solver, V_new, labor0)
        min_accepted_pb = min(min_accepted_pb, pb_new)
        lambdas.append(lam)
        # operator diagnostics for the trace (identical deterministic rebuild
        # of the operator built from the accepted V_old inside _step)
        Q1, _, diag1, _ = solver.build_operator_and_u(
            V, labor0, 0.0, 0.0, final=False)
        max_q1 = float(np.max(np.abs(np.asarray(Q1.sum(axis=1)).ravel())))
        sector_now = _sector_seq(records)
        changes = (sum(1 for x, y in zip(prev_sector, sector_now) if x != y)
                   if prev_sector is not None else 0)
        prev_sector = sector_now
        trace.append({
            "iteration": iteration,
            "raw_max_stat": float(stat_raw),
            "accepted_max_stat": statistic,
            "lambda": lam,
            "backtrack_count": backtracks,
            "min_pb_old": pb_old,
            "min_pb_raw": pb_raw,
            "min_pb_new": pb_new,
            "lambda1_would_violate": lambda1_violates,
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
        return SafeguardDiagnosticResult(
            outcome="HJB_NONCONVERGENCE", converged=False,
            iterations=accepted_iterations, final_statistic=statistic,
            min_lambda=min(lambdas) if lambdas else 1.0,
            median_lambda=float(np.median(lambdas)) if lambdas else 1.0,
            backtracking_iterations=sum(1 for l in lambdas if l < 1.0),
            min_accepted_boundary_pb=min_accepted_pb,
            raw_domain_violations_avoided=raw_violations_avoided,
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
        outcome = "SAFEGUARD_STAGNATION"
    return SafeguardDiagnosticResult(
        outcome=outcome, converged=True, iterations=accepted_iterations,
        final_statistic=statistic,
        min_lambda=min(lambdas) if lambdas else 1.0,
        median_lambda=float(np.median(lambdas)) if lambdas else 1.0,
        backtracking_iterations=sum(1 for l in lambdas if l < 1.0),
        min_accepted_boundary_pb=min_accepted_pb,
        raw_domain_violations_avoided=raw_violations_avoided,
        final_bellman_residual=val["bellman_residual"],
        final_q_max_abs_row_sum=val["max_abs_q1"],
        final_min_boundary_pb=val["min_boundary_pb"],
        final_artificial_bindings=val["artificial_bindings"],
        final_family_histogram=val["family_histogram"],
        trace=trace,
    )
