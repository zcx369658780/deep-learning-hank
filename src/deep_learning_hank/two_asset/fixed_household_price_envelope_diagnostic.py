"""DLH-5V-K fixed-household external-price convergence envelope diagnostic.

Read-only scientific drivers over the two ACCEPTED solvers:

- Diagnostic A (legacy): the accepted MATLAB-faithful household HJB solver
  (``solve_matlab_faithful_hjb``) on the FROZEN rectangle domain
  ``a = linspace(0,10,20)``, ``b = linspace(-2,5,20)`` (``b_max = 5`` FROZEN).
- Diagnostic B (current): the accepted boundary selected-Q solver
  (``BoundaryHJBSolver``) on the FROZEN triangle domain ``m = 1``,
  ``W_max = 10``.

HJB ONLY. No KFE, no stationary KFE, no distribution ``g``, no stationary
aggregates, no ``solve_household_steady_state``, no SCC/global-Q, no GE.
Only the external equilibrium inputs ``(r_a, r_b, w)`` vary across the
predeclared sparse case list; every other household/domain/numerical/
initialization setting is frozen per solver. No stabilization (no damping,
line search, continuation, pseudo-time adaptation, derivative clipping,
hard control bounds). ``b_max`` and ``W_max`` are never varied.

All diagnostics are deterministic (brentq initialization, fixed grids, fixed
case lists, deterministic midpoint rule).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Optional

import numpy as np
from scipy.optimize import brentq

from deep_learning_hank.two_asset.matlab_faithful_two_asset_ha import (
    EconomicParams,
    HouseholdInputs,
    MatlabFaithfulHJBGrid,
    MatlabFaithfulHJBNumerics,
    flow_utility,
    matlab_faithful_illiquid_return,
    solve_matlab_faithful_hjb,
)
from deep_learning_hank.two_asset.boundary_hjb_selected_q import (
    BoundaryHJBConfig,
    BoundaryHJBFailure,
    BoundaryHJBSolver,
)

# ---------------------------------------------------------------------------
# Frozen household / domain / numerical settings (VALIDATION_FIXTURE_NOT_CALIBRATION)
# ---------------------------------------------------------------------------
FROZEN_PARAMS = EconomicParams(0.02, 2.0, 5.0, 0.1, 2.0, 1e-6, 0.0, 0.0)
FROZEN_TAU = 0.15
FROZEN_MIGRATION_COST = 0.0
FROZEN_LABOR_WEIGHT = 1.0
Z = np.asarray([0.8, 1.3])
SWITCH = np.array([[-1.0 / 3.0, 1.0 / 3.0], [1.0 / 3.0, -1.0 / 3.0]])

# -- legacy rectangle domain (b_max = 5 FROZEN) ------------------------------
LEGACY_B = np.linspace(-2.0, 5.0, 20)   # b_min = -2, b_max = 5
LEGACY_A = np.linspace(0.0, 10.0, 20)   # a in [0, 10]
LEGACY_GRID = MatlabFaithfulHJBGrid(LEGACY_B, LEGACY_A, Z, SWITCH)
# -- legacy numerics / initialization conventions (accepted fixture) ---------
LEGACY_NUMERICS = MatlabFaithfulHJBNumerics(
    delta=1000.0, convergence_tolerance=1e-7, max_iterations=1000, drift_tolerance=1e-12
)
LEGACY_TRANSFER_INCOME = 0.0
LEGACY_GAP = 0.01  # frozen borrowing-gap convention for EVERY legacy price case

# -- selected-Q frozen geometry (m = 1, W_max = 10) --------------------------
SELECTED_Q_M = 1
SELECTED_Q_W_MAX = 10.0
SELECTED_Q_B_MIN = -2.0
SELECTED_Q_A_MAX = 10.0
# all other selected-Q settings are the BoundaryHJBConfig defaults exactly as
# frozen in accepted Issue #58 diagnostic conventions
SELECTED_Q_R_B = 0.02
SELECTED_Q_W = 1.0
SELECTED_Q_R_A_SENTINELS = [0.07, 0.10, 0.13]  # exactly three sentinels

# -- predeclared legacy price cases (sparse design, frozen) ------------------
PREDECLARED_LEGACY_CASES: list[tuple[float, float, float]] = [
    # MAIN r_a line (r_b = 0.02, w = 1.00); includes the central anchor
    (0.05, 0.02, 1.00),
    (0.07, 0.02, 1.00),   # Owner historical SAFE-REGION reference label
    (0.09, 0.02, 1.00),
    (0.11, 0.02, 1.00),
    (0.13, 0.02, 1.00),   # Owner historical HIGH-RATE / FAILURE reference label
    # r_b sentinels (r_a = 0.07, w = 1.00)
    (0.07, 0.015, 1.00),
    (0.07, 0.025, 1.00),
    # wage sentinels (r_a = 0.07, r_b = 0.02)
    (0.07, 0.02, 0.80),
    (0.07, 0.02, 1.20),
]
assert len(PREDECLARED_LEGACY_CASES) == 9

CONSUMPTION_FLOOR_AT_NEAR = 990.0  # v_b floor 1e-6 -> FOC c cap 1000; >= 990 counts as "at/near floor"
LABOR_ZERO_EPS = 1.0e-9


def _inputs(r_a: float, r_b: float, w: float) -> HouseholdInputs:
    return HouseholdInputs(
        r_a=r_a, r_b=r_b, tau=FROZEN_TAU, wages=np.asarray([w], dtype=float),
        migration_costs=np.asarray([FROZEN_MIGRATION_COST], dtype=float),
        labor_weights=np.asarray([FROZEN_LABOR_WEIGHT], dtype=float),
    )


def legacy_initial_arrays(inputs: HouseholdInputs, gap: float = LEGACY_GAP):
    """Deterministic fixture initialization (accepted construction): labor0 via
    brentq, V0 = u(c_full, l0)/rho. Shape (b, a, z) = (20, 20, 2)."""
    b = LEGACY_B
    a = LEGACY_A
    z = Z
    params = FROZEN_PARAMS
    shape = (b.size, a.size, z.size)
    labor0 = np.empty(shape)
    initial = np.empty(shape)
    for nz in range(z.size):
        for j in range(a.size):
            for i in range(b.size):
                rb = inputs.r_b + (gap if b[i] < 0 else 0.0)
                base = rb * b[i]
                net = (1.0 - inputs.tau) * inputs.wages[0] * z[nz]

                def f(l):
                    return l ** params.phi - net * (net * l + base) ** (-params.gamma_c)

                labor0[i, j, nz] = brentq(f, 1e-8, 5.0)
                ra = float(matlab_faithful_illiquid_return(a[j], a[-1], inputs.r_a))
                c_full = net * labor0[i, j, nz] + base + ra * a[j]
                initial[i, j, nz] = flow_utility(c_full, np.array([labor0[i, j, nz]]), inputs, params) / params.rho
    return initial, labor0


def vb_evidence(final_value: np.ndarray, labor0: np.ndarray, inputs: HouseholdInputs,
                gap: float = LEGACY_GAP) -> dict:
    """Transparent final-value liquid monotonicity diagnostic (read-only,
    mirrors the accepted derivative conventions): vb_b/vb_f over (b,a,z),
    boundary marginals from labor0 resources. Never mutates the oracle."""
    b, a, z = LEGACY_B, LEGACY_A, Z
    db = float(b[1] - b[0])
    shape = final_value.shape
    vb_f = np.zeros(shape)
    vb_b = np.zeros(shape)
    vb_f[:-1] = (final_value[1:] - final_value[:-1]) / db
    vb_b[1:] = vb_f[:-1]
    for j in range(a.size):
        for nz in range(z.size):
            for i in (0, b.size - 1):
                rb = inputs.r_b + (gap if b[i] < 0 else 0.0)
                resources = ((1 - inputs.tau) * inputs.wages[0] * z[nz] * labor0[i, j, nz]
                             + LEGACY_TRANSFER_INCOME + rb * b[i])
                marginal = resources ** (-FROZEN_PARAMS.gamma_c)
                if i == 0:
                    vb_b[i, j, nz] = marginal
                else:
                    vb_f[i, j, nz] = marginal
    evidence = np.minimum(vb_b, vb_f)  # weaker of the two local liquid slopes
    finite = np.isfinite(evidence)
    worst = int(np.argmin(evidence)) if finite.any() else None
    wi, wj, wnz = np.unravel_index(worst, shape) if worst is not None else (None, None, None)
    return {
        "min_evidence": float(np.min(evidence)) if finite.any() else None,
        "min_vb_b": float(np.min(vb_b[np.isfinite(vb_b)])),
        "min_vb_f": float(np.min(vb_f[np.isfinite(vb_f)])),
        "nonpositive_share": float(np.mean(evidence <= 0.0)),
        "nonpositive_count": int(np.sum(evidence <= 0.0)),
        "worst_b": float(b[wi]) if wi is not None else None,
        "worst_a": float(a[wj]) if wj is not None else None,
        "worst_z": float(z[wnz]) if wnz is not None else None,
        "worst_evidence": float(evidence[wi, wj, wnz]) if wi is not None else None,
    }


def _limit_cycle_probe(value: np.ndarray, labor0: np.ndarray, inputs: HouseholdInputs,
                       gap: float = LEGACY_GAP) -> Optional[float]:
    """Bounded diagnostic probe (max 8 extra iterations from the final value,
    identical frozen grid/numerics) used ONLY to distinguish finite
    nonconvergence from limit-cycle-like behavior in nonconverged cases."""
    grid = LEGACY_GRID
    numerics = MatlabFaithfulHJBNumerics(
        delta=LEGACY_NUMERICS.delta,
        convergence_tolerance=LEGACY_NUMERICS.convergence_tolerance,
        max_iterations=8,
        drift_tolerance=LEGACY_NUMERICS.drift_tolerance,
    )
    try:
        probe = solve_matlab_faithful_hjb(
            grid, FROZEN_PARAMS, inputs, value, labor0,
            LEGACY_TRANSFER_INCOME, gap, numerics,
        )
    except Exception:
        return None
    return float(probe.convergence_statistic)


def _complete_record(rec: dict) -> dict:
    """Ensure every CSV_HEADER key is present (union schema for both solvers)."""
    for key in CSV_HEADER:
        rec.setdefault(key, None)
    return rec


def run_legacy_case(r_a: float, r_b: float, w: float,
                    gap: float = LEGACY_GAP) -> dict:
    """One legacy price case on the frozen rectangle. Returns the full
    diagnostic record (schema is stable for the CSV)."""
    inputs = _inputs(r_a, r_b, w)
    initial, labor0 = legacy_initial_arrays(inputs, gap)
    failure = None
    result = None
    try:
        result = solve_matlab_faithful_hjb(
            LEGACY_GRID, FROZEN_PARAMS, inputs, initial, labor0,
            LEGACY_TRANSFER_INCOME, gap, LEGACY_NUMERICS,
        )
    except Exception as exc:  # explicit solver failure (e.g. non-finite linear solve)
        failure = f"explicit_failure: {type(exc).__name__}"
    v = result.value if result is not None else None
    v_finite = bool(np.isfinite(v).all()) if v is not None else False
    if failure is None and not v_finite:
        failure = "nonfinite_value"
    if failure is None:
        if result.converged:
            failure = "converged"
        else:
            probe_stat = _limit_cycle_probe(v, labor0, inputs, gap)
            if probe_stat is not None and abs(probe_stat - result.convergence_statistic) <= 0.10 * abs(result.convergence_statistic):
                failure = "limit_cycle_like"
            else:
                failure = "finite_nonconvergence"

    def _stats(arr):
        return (float(np.min(arr)), float(np.max(arr))) if arr is not None else (None, None)

    cmin, cmax = _stats(result.consumption if result is not None else None)
    lmin, lmax = _stats(result.labor if result is not None else None)
    dmin, dmax = _stats(result.transfer if result is not None else None)
    amin_, amax_ = _stats(result.mu_a if result is not None else None)
    bmin, bmax = _stats(result.mu_b if result is not None else None)
    c_floor_share = None
    l_zero_share = None
    l_max_share = None
    v_ev = None
    if result is not None and v_finite:
        cons = result.consumption
        lab = result.labor
        c_floor_share = float(np.mean(cons >= CONSUMPTION_FLOOR_AT_NEAR))
        l_zero_share = float(np.mean(lab <= LABOR_ZERO_EPS))
        l_max_share = float(np.mean(np.abs(lab - float(np.max(lab))) <= 1e-6))
        v_ev = vb_evidence(v, labor0, inputs, gap)
    rec = {
        "solver": "legacy_oracle",
        "r_a": r_a, "r_b": r_b, "w": w,
        "domain": "rectangle b_max=5",
        "converged": bool(result.converged) if result is not None else False,
        "iterations": int(result.iterations) if result is not None else None,
        "convergence_statistic": float(result.convergence_statistic) if result is not None else None,
        "failure_class": failure,
        "v_finite": v_finite,
        "v_min": float(np.min(v)) if v is not None and v_finite else None,
        "v_max": float(np.max(v)) if v is not None and v_finite else None,
        "cons_min": cmin, "cons_max": cmax, "cons_at_floor_share": c_floor_share,
        "labor_min": lmin, "labor_max": lmax,
        "labor_zero_share": l_zero_share, "labor_max_share": l_max_share,
        "d_min": dmin, "d_max": dmax,
        "mu_a_min": amin_, "mu_a_max": amax_,
        "mu_b_min": bmin, "mu_b_max": bmax,
        "vb_min_evidence": v_ev["min_evidence"] if v_ev else None,
        "vb_nonpositive_share": v_ev["nonpositive_share"] if v_ev else None,
        "vb_worst_b": v_ev["worst_b"] if v_ev else None,
        "vb_worst_a": v_ev["worst_a"] if v_ev else None,
        "vb_worst_z": v_ev["worst_z"] if v_ev else None,
    }
    return _complete_record(rec)


def _selected_q_config(r_a: float, r_b: float, w: float) -> BoundaryHJBConfig:
    inputs = _inputs(r_a, r_b, w)
    return BoundaryHJBConfig(
        m=SELECTED_Q_M, w_max=SELECTED_Q_W_MAX, b_min=SELECTED_Q_B_MIN,
        a_max=SELECTED_Q_A_MAX, params=FROZEN_PARAMS, inputs=inputs, z=Z,
        switch_matrix=SWITCH, delta=1000.0, tolerance_iter=1e-7,
        tolerance_bellman=1e-3, max_iterations=1000,
    )


def _min_boundary_pb(solver: BoundaryHJBSolver, V: np.ndarray,
                     labor0: np.ndarray) -> float:
    """Minimum effective liquid marginal p_b (= vb_b) over boundary (non-F0)
    nodes of the current value iterate — the effective-domain guard evidence."""
    vb_f, vb_b, va_f, va_b = solver.compute_derivatives(V, labor0, 0.0, 0.0)
    g = solver.grid
    vals = [float(vb_b[node, nz]) for node in range(solver.n)
            if g.families[node] != "F0" for nz in range(solver.nz)]
    return float(np.min(vals)) if vals else float("nan")


def run_selected_q_case(r_a: float, r_b: float = SELECTED_Q_R_B,
                        w: float = SELECTED_Q_W) -> dict:
    """One selected-Q price sentinel on the frozen triangle (m=1, W_max=10)."""
    solver = BoundaryHJBSolver(_selected_q_config(r_a, r_b, w))
    labor0 = solver.build_labor0(0.0, 0.0)
    V0 = solver.build_initial_value(labor0, 0.0, 0.0)
    # iteration-1 operator diagnostics (frozen build, deterministic)
    Q1, _, diag1, _ = solver.build_operator_and_u(V0, labor0, 0.0, 0.0, final=False)
    max_q1 = float(np.max(np.abs(np.asarray(Q1.sum(axis=1)).ravel())))
    pb_iter1 = _min_boundary_pb(solver, V0, labor0)
    outcome = "converged"
    failure = None
    detail = {}
    v = None
    converged = False
    iterations = None
    statistic = None
    try:
        res = solver.solve(V0, labor0, 0.0, 0.0)
        converged = bool(res.converged)
        iterations = int(res.iterations)
        statistic = float(res.convergence_statistic)
        v = res.value
        if not converged:
            outcome = "finite_nonconvergence"
            failure = "finite_nonconvergence"
    except BoundaryHJBFailure as exc:
        outcome = exc.failure_name
        failure = exc.failure_name
        detail = dict(exc.detail or {})
        iterations = detail.get("iteration")
    pb_final = _min_boundary_pb(solver, v, labor0) if v is not None else None
    rec = {
        "solver": "selected_q",
        "r_a": r_a, "r_b": r_b, "w": w,
        "domain": "triangle W_max=10",
        "converged": converged,
        "iterations": iterations,
        "convergence_statistic": statistic,
        "outcome": outcome,
        "first_failure_iteration": detail.get("iteration"),
        "first_failure_family": detail.get("family"),
        "first_failure_j": detail.get("j"),
        "first_failure_i": detail.get("i"),
        "first_failure_z": detail.get("z"),
        "first_failure_p_b": detail.get("p_b"),
        "iter1_max_abs_q1": max_q1,
        "iter1_v_finite": bool(np.isfinite(V0).all()),
        "iter1_min_boundary_p_b": pb_iter1,
        "iter1_expansions": int(diag1["total_expansions"]),
        "iter1_artificial_bindings": int(diag1["artificial_binding"]),
        "p_b_positive_through_iterations": (
            (pb_iter1 > 0.0 and pb_final is not None and pb_final > 0.0)
            if failure is None
            else (False if failure == "DERIVATIVE_EFFECTIVE_DOMAIN_FAILURE"
                  else pb_iter1 > 0.0)
        ),
        "final_min_boundary_p_b": pb_final,
    }
    return _complete_record(rec)


def legacy_r_a_line_bisection(max_midpoints: int = 4,
                              line_results: Optional[dict] = None) -> list[dict]:
    """Conditional r_a transition localization (DIAGNOSTIC BISECTION, not
    calibration): deterministic midpoint rule, at most ``max_midpoints``
    evaluations, r_b = 0.02, w = 1.00, everything else frozen. Authorized ONLY
    if the predeclared r_a line contains at least one clear PASS and one clear
    FAIL; otherwise returns []. ``line_results`` (optional) supplies the
    already-computed predeclared r_a-line records to avoid re-execution."""
    if max_midpoints < 0 or max_midpoints > 4:
        raise ValueError("bisection capped at four midpoint evaluations")
    line = [(r_a,) for r_a, r_b, w in PREDECLARED_LEGACY_CASES if r_b == 0.02 and w == 1.00]
    if line_results is not None:
        results = dict(line_results)
    else:
        results = {r_a: run_legacy_case(r_a, 0.02, 1.00) for r_a, in line}

    def passes(rec):
        return rec["failure_class"] == "converged" and rec["v_finite"]

    if not (any(passes(results[r]) for r, in line) and any(not passes(results[r]) for r, in line)):
        return []  # no PASS/FAIL bracket -> bisection not authorized
    executed: list[dict] = []
    for _ in range(max_midpoints):
        pairs = []
        pts = sorted(r for r, in line)
        for lo, hi in zip(pts, pts[1:]):
            if passes(results[lo]) != passes(results[hi]):
                pairs.append((hi - lo, (lo + hi) / 2.0, passes(results[lo]), passes(results[hi])))
        if not pairs:
            break
        _, mid, lo_pass, hi_pass = max(pairs, key=lambda p: p[0])  # deterministic tie: widest gap
        mid = float(np.round(mid, 6))
        if mid in results:
            break
        rec = run_legacy_case(mid, 0.02, 1.00)
        results[mid] = rec
        executed.append(rec)
        line = [(r,) for r in sorted(results)]
        if not (any(passes(results[r]) for r, in line) and any(not passes(results[r]) for r, in line)):
            break
    return executed


def all_case_rows() -> list[dict]:
    """Complete executed-case records: 9 predeclared legacy + (conditional)
    bisection midpoints + 3 selected-Q sentinels, in deterministic order."""
    rows = [run_legacy_case(r_a, r_b, w) for r_a, r_b, w in PREDECLARED_LEGACY_CASES]
    line_results = {rec["r_a"]: rec for rec in rows if rec["r_b"] == 0.02 and rec["w"] == 1.00}
    rows += legacy_r_a_line_bisection(line_results=line_results)
    rows += [run_selected_q_case(r_a) for r_a in SELECTED_Q_R_A_SENTINELS]
    return rows


CSV_HEADER = [
    "solver", "r_a", "r_b", "w", "domain", "converged", "iterations",
    "convergence_statistic", "failure_class", "v_finite", "v_min", "v_max",
    "cons_min", "cons_max", "cons_at_floor_share", "labor_min", "labor_max",
    "labor_zero_share", "labor_max_share", "d_min", "d_max", "mu_a_min",
    "mu_a_max", "mu_b_min", "mu_b_max", "vb_min_evidence", "vb_nonpositive_share",
    "vb_worst_b", "vb_worst_a", "vb_worst_z",
    "outcome", "first_failure_iteration", "first_failure_family",
    "first_failure_j", "first_failure_i", "first_failure_z", "first_failure_p_b",
    "iter1_max_abs_q1", "iter1_v_finite", "iter1_min_boundary_p_b",
    "iter1_expansions", "iter1_artificial_bindings", "final_min_boundary_p_b",
]


def csv_lines(rows: list[dict]) -> list[str]:
    """Deterministic CSV serialization of the diagnostic records."""
    lines = [",".join(CSV_HEADER)]
    for rec in rows:
        cells = []
        for key in CSV_HEADER:
            val = rec.get(key)
            if isinstance(val, bool):
                cells.append("true" if val else "false")
            elif val is None:
                cells.append("")
            elif isinstance(val, float):
                cells.append(f"{val:.12g}")
            else:
                cells.append(str(val))
        lines.append(",".join(cells))
    return lines


def write_csv(path: str, rows: list[dict]) -> None:
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write("\n".join(csv_lines(rows)) + "\n")


if __name__ == "__main__":
    rows = all_case_rows()
    print(json.dumps(rows, indent=2, default=str))
