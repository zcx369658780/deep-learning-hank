"""DLH-3B deterministic HANK steady-state equilibrium solver (isolated module).

Implements Issue #11 §7: deterministic nested ``scipy.optimize.brentq`` roots in
the real liquid return ``r`` (outer) and aggregate effective labor ``N``
(inner), with the frozen primary brackets and bounded deterministic scans from
the config.  Every full ``(r, N)`` equilibrium evaluation is recorded in the
root trace.

Non-finite evaluations (e.g., a candidate where the household zero-drift
policy is infeasible) are recorded in the trace but excluded from bracket
logic; the first finite sign-changing adjacent pair is used.  Economic
parameters are never modified to manufacture a bracket or root.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt
from scipy.optimize import brentq

from deep_learning_hank.economics.hank_firm import hank_production
from deep_learning_hank.economics.hank_fiscal import hank_fiscal
from deep_learning_hank.economics.grids import build_asset_grid, build_idiosyncratic_generator
from deep_learning_hank.hank_config import HankSteadyStateConfig
from deep_learning_hank.solvers.distribution_kfe import (
    DistributionSolution,
    solve_stationary_distribution,
)
from deep_learning_hank.solvers.hank_household_steady_state import (
    HankHouseholdFeasibilityError,
    HankHouseholdSolution,
    solve_hank_household,
)

__all__ = [
    "EquilibriumEvaluation",
    "HankSteadyStateResult",
    "NoBracketError",
    "RootTraceRow",
    "evaluate_equilibrium",
    "solve_hank_steady_state",
]

FloatArray = npt.NDArray[np.float64]


class NoBracketError(RuntimeError):
    """Raised when no finite sign-changing bracket is found for a root."""


@dataclass(frozen=True)
class RootTraceRow:
    stage: str
    r: float
    N: float
    A_hh: float
    N_hh: float
    C: float
    R_asset: float
    R_labor: float
    finite: bool
    hjb_converged: bool


@dataclass(frozen=True)
class EquilibriumEvaluation:
    r: float
    N: float
    finite: bool
    output: float
    wage: float
    marginal_cost: float
    markup: float
    profits: float
    tax_revenue: float
    transfer: float
    A_hh: float
    N_hh: float
    C: float
    R_asset: float
    R_labor: float
    hjb_converged: bool
    hjb_true_residual: float
    household: HankHouseholdSolution | None
    distribution: DistributionSolution | None


@dataclass(frozen=True)
class HankSteadyStateResult:
    config_sha256: str
    root_r: float
    root_N: float
    root_converged: bool
    outer_bracket_used: tuple[float, float]
    outer_bracket_from_scan: bool
    inner_bracket_used: tuple[float, float]
    inner_bracket_from_scan: bool
    outer_evaluations: int
    inner_evaluations: int
    root_trace: tuple[RootTraceRow, ...]
    final: EquilibriumEvaluation


def _nonfinite_evaluation(config: HankSteadyStateConfig, r: float, N: float) -> EquilibriumEvaluation:
    return EquilibriumEvaluation(
        r=float(r),
        N=float(N),
        finite=False,
        output=float("nan"),
        wage=float("nan"),
        marginal_cost=float("nan"),
        markup=float("nan"),
        profits=float("nan"),
        tax_revenue=float("nan"),
        transfer=float("nan"),
        A_hh=float("nan"),
        N_hh=float("nan"),
        C=float("nan"),
        R_asset=float("nan"),
        R_labor=float("nan"),
        hjb_converged=False,
        hjb_true_residual=float("nan"),
        household=None,
        distribution=None,
    )


def evaluate_equilibrium(
    config: HankSteadyStateConfig,
    r: float,
    N: float,
    trace: list[RootTraceRow] | None = None,
    stage: str = "eval",
) -> EquilibriumEvaluation:
    """Full deterministic equilibrium evaluation at candidate ``(r, N)``.

    Computes production/fiscal objects, solves the household HJB + stationary
    KFE, aggregates, and the asset/labor residuals.  Optionally records the
    evaluation in the root trace.
    """
    try:
        production = hank_production(productivity=config.productivity, labor=N, epsilon=config.epsilon)
        fiscal = hank_fiscal(
            wage=production.wage,
            labor=N,
            real_return=r,
            bond_supply=config.bond_supply,
            tau_l=config.tau_l,
            public_outlay=config.public_outlay,
        )
        asset_grid = build_asset_grid(config.a_min, config.a_max, config.asset_grid_count)
        efficiency_states = np.asarray(config.idiosyncratic_states, dtype=np.float64)
        state_generator = build_idiosyncratic_generator(config.q_low_to_high, config.q_high_to_low)
        household = solve_hank_household(
            asset_grid=asset_grid,
            efficiency_states=efficiency_states,
            state_generator=state_generator,
            wage=production.wage,
            real_return=r,
            transfer=fiscal.transfer,
            profits=production.profits,
            tau_l=config.tau_l,
            rho_hh=config.rho_hh,
            gamma=config.gamma,
            frisch=config.frisch,
            chi=config.chi,
            n_max=config.n_max,
            tolerance=config.numerical.hjb_tolerance,
            max_iterations=config.numerical.hjb_max_iterations,
            pseudo_time_step=config.numerical.hjb_pseudo_time_step,
            consumption_floor=config.numerical.consumption_floor,
        )
        distribution = solve_stationary_distribution(
            generator=household.generator,
            asset_grid=asset_grid,
            consumption=household.consumption,
            stationarity_tolerance=config.numerical.kfe_stationarity_tolerance,
            mass_tolerance=config.numerical.kfe_mass_tolerance,
            negative_mass_threshold=config.numerical.negative_mass_threshold,
        )
        A_hh = distribution.mean_assets
        C = distribution.mean_consumption
        N_hh = float(np.sum(distribution.mass * efficiency_states[:, None] * household.labor))
        R_asset = float(A_hh - config.bond_supply)
        R_labor = float(N_hh - N)
        evaluation = EquilibriumEvaluation(
            r=float(r),
            N=float(N),
            finite=True,
            output=production.output,
            wage=production.wage,
            marginal_cost=production.marginal_cost,
            markup=production.markup,
            profits=production.profits,
            tax_revenue=fiscal.tax_revenue,
            transfer=fiscal.transfer,
            A_hh=A_hh,
            N_hh=N_hh,
            C=C,
            R_asset=R_asset,
            R_labor=R_labor,
            hjb_converged=household.converged,
            hjb_true_residual=household.true_residual,
            household=household,
            distribution=distribution,
        )
    except (HankHouseholdFeasibilityError, ValueError, RuntimeError):
        evaluation = _nonfinite_evaluation(config, r, N)
    if trace is not None:
        trace.append(
            RootTraceRow(
                stage=stage,
                r=float(r),
                N=float(N),
                A_hh=float(evaluation.A_hh),
                N_hh=float(evaluation.N_hh),
                C=float(evaluation.C),
                R_asset=float(evaluation.R_asset),
                R_labor=float(evaluation.R_labor),
                finite=evaluation.finite,
                hjb_converged=evaluation.hjb_converged,
            )
        )
    return evaluation


def _sign_change(a: float, b: float) -> bool:
    if not (np.isfinite(a) and np.isfinite(b)):
        return False
    if a == 0.0 or b == 0.0:
        return True
    return np.sign(a) != np.sign(b)


def _find_sign_changing_bracket(
    residual,
    primary: tuple[float, float],
    scan_bounds: tuple[float, float],
    scan_points: int,
) -> tuple[tuple[float, float], bool, tuple[float, float]]:
    """Primary bracket first; else one bounded deterministic scan."""
    lo, hi = primary
    r_lo = residual(lo)
    r_hi = residual(hi)
    if _sign_change(r_lo, r_hi):
        return (lo, hi), False, (float(r_lo), float(r_hi))
    previous_x = None
    previous_r = None
    for x in np.linspace(scan_bounds[0], scan_bounds[1], scan_points):
        rx = residual(float(x))
        if previous_x is not None and _sign_change(previous_r, rx):
            return (float(previous_x), float(x)), True, (float(previous_r), float(rx))
        previous_x = float(x)
        previous_r = float(rx)
    raise NoBracketError(
        "no finite sign-changing bracket found in the primary bracket or the "
        "bounded deterministic scan; economic parameters were not modified."
    )


def _inner_labor_root(
    config: HankSteadyStateConfig, r: float, trace: list[RootTraceRow]
) -> tuple[float, tuple[float, float], bool]:
    """Inner labor root at fixed ``r``: ``R_labor(N) = N_hh - N = 0``."""
    def residual(N: float) -> float:
        evaluation = evaluate_equilibrium(config, r, N, trace=trace, stage="inner_brentq")
        return evaluation.R_labor if evaluation.finite else float("nan")

    def bracket_residual(N: float, stage: str) -> float:
        evaluation = evaluate_equilibrium(config, r, N, trace=trace, stage=stage)
        return evaluation.R_labor if evaluation.finite else float("nan")

    primary = config.labor_bracket
    lo, hi = primary
    r_lo = bracket_residual(lo, "inner_primary_lower")
    r_hi = bracket_residual(hi, "inner_primary_upper")
    if _sign_change(r_lo, r_hi):
        bracket = (lo, hi)
        from_scan = False
    else:
        previous_x = None
        previous_r = None
        bracket = None
        from_scan = True
        for x in np.linspace(config.labor_scan_bounds[0], config.labor_scan_bounds[1], config.labor_scan_points):
            rx = bracket_residual(float(x), "inner_scan")
            if previous_x is not None and _sign_change(previous_r, rx):
                bracket = (float(previous_x), float(x))
                break
            previous_x = float(x)
            previous_r = float(rx)
        if bracket is None:
            raise NoBracketError(
                "BLOCKED_DLH_3B_NO_LABOR_BRACKET: no finite sign-changing labor "
                "bracket found at r={r!r} in the primary bracket or the scan."
            )
    root, info = brentq(
        residual,
        bracket[0],
        bracket[1],
        xtol=config.numerical.root_xtol,
        rtol=config.numerical.root_xtol,
        maxiter=config.numerical.root_max_iterations,
        full_output=True,
        disp=False,
    )
    if not info.converged:
        raise NoBracketError("BLOCKED_DLH_3B_NO_LABOR_BRACKET: inner brentq did not converge.")
    return float(root), bracket, from_scan


def _outer_residual(
    config: HankSteadyStateConfig, r: float, trace: list[RootTraceRow], stage: str
) -> float:
    """Outer residual ``R_asset(r) = A_hh(r, N*(r)) - B``."""
    try:
        n_star, _bracket, _from_scan = _inner_labor_root(config, r, trace)
    except NoBracketError:
        trace.append(
            RootTraceRow(
                stage=stage, r=float(r), N=float("nan"), A_hh=float("nan"), N_hh=float("nan"),
                C=float("nan"), R_asset=float("nan"), R_labor=float("nan"),
                finite=False, hjb_converged=False,
            )
        )
        return float("nan")
    evaluation = evaluate_equilibrium(config, r, n_star, trace=trace, stage=stage)
    return evaluation.R_asset if evaluation.finite else float("nan")


def solve_hank_steady_state(config: HankSteadyStateConfig) -> HankSteadyStateResult:
    """Solve ``R_asset(r*) = 0`` with the nested inner labor root ``N*(r)``."""
    config.validate()
    trace: list[RootTraceRow] = []

    def outer_residual(r: float, stage: str) -> float:
        return _outer_residual(config, r, trace, stage)

    primary = config.asset_bracket
    lo, hi = primary
    r_lo = outer_residual(lo, "outer_primary_lower")
    r_hi = outer_residual(hi, "outer_primary_upper")
    if _sign_change(r_lo, r_hi):
        outer_bracket = (lo, hi)
        outer_from_scan = False
    else:
        previous_x = None
        previous_r = None
        outer_bracket = None
        outer_from_scan = True
        for x in np.linspace(config.asset_scan_bounds[0], config.asset_scan_bounds[1], config.asset_scan_points):
            rx = outer_residual(float(x), "outer_scan")
            if previous_x is not None and _sign_change(previous_r, rx):
                outer_bracket = (float(previous_x), float(x))
                break
            previous_x = float(x)
            previous_r = float(rx)
        if outer_bracket is None:
            raise NoBracketError(
                "BLOCKED_DLH_3B_NO_ASSET_BRACKET: no finite sign-changing asset "
                "bracket found in the primary bracket or the scan."
            )

    def brentq_residual(r: float) -> float:
        return outer_residual(r, "outer_brentq")

    root_r, info = brentq(
        brentq_residual,
        outer_bracket[0],
        outer_bracket[1],
        xtol=config.numerical.root_xtol,
        rtol=config.numerical.root_xtol,
        maxiter=config.numerical.root_max_iterations,
        full_output=True,
        disp=False,
    )
    inner_root, inner_bracket, inner_from_scan = _inner_labor_root(config, float(root_r), trace)
    final = evaluate_equilibrium(config, float(root_r), inner_root, trace=trace, stage="final")
    stages = [row.stage for row in trace]
    inner_evaluations = sum(1 for s in stages if s.startswith("inner_"))
    outer_evaluations = sum(1 for s in stages if s.startswith("outer_"))
    return HankSteadyStateResult(
        config_sha256=config.sha256(),
        root_r=float(root_r),
        root_N=inner_root,
        root_converged=bool(info.converged),
        outer_bracket_used=outer_bracket,
        outer_bracket_from_scan=outer_from_scan,
        inner_bracket_used=inner_bracket,
        inner_bracket_from_scan=inner_from_scan,
        outer_evaluations=outer_evaluations,
        inner_evaluations=inner_evaluations,
        root_trace=tuple(trace),
        final=final,
    )
