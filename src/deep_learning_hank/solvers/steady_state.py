"""Single-region Tier-0 HA/Aiyagari steady-state general equilibrium.

Closure (accepted DLH-0/1B/2A contract, Issue #6):

    K -> two-factor firm (w, r) -> balanced fiscal transfer -> accepted
        household HJB -> accepted stationary KFE -> mean assets A(K)
        -> capital residual R_K(K) = K - A(K)

The deterministic root is found with ``scipy.optimize.brentq`` on the primary
bracket from config; if the primary bracket does not sign-change, one bounded
deterministic bracket scan (config ``scan_bounds``/``scan_points``) is
performed.  Economic parameters are never modified to manufacture a root.

Effective labor is computed from the idiosyncratic CTMC stationary
distribution: ``L_bar = sum_z pi_z * z`` (never hard-coded to 1).

Firm: two-factor Cobb-Douglas only.  Fiscal: minimal balanced lump-sum.
Household asset return in equilibrium equals the net productive-capital
return ``r``.  No W/regional/SOE/nominal/shock/transition objects.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt
from scipy.optimize import brentq

from deep_learning_hank.config import SteadyStateConfig
from deep_learning_hank.economics.firm import production_block
from deep_learning_hank.economics.fiscal import balanced_fiscal
from deep_learning_hank.economics.grids import (
    build_asset_grid,
    build_idiosyncratic_generator,
    stationary_state_probabilities,
)
from deep_learning_hank.solvers.distribution_kfe import (
    DistributionSolution,
    solve_stationary_distribution,
)
from deep_learning_hank.solvers.household_hjb import (
    HouseholdSolution,
    solve_household,
)

__all__ = [
    "NoCapitalBracketError",
    "CapitalEvaluation",
    "SteadyStateResult",
    "effective_labor_from_ctmc",
    "evaluate_capital",
    "solve_steady_state",
]

FloatArray = npt.NDArray[np.float64]


class NoCapitalBracketError(RuntimeError):
    """Raised when no finite sign-changing capital bracket is found."""


@dataclass(frozen=True)
class CapitalEvaluation:
    capital: float
    output: float
    wage: float
    net_capital_return: float
    transfer: float
    mean_assets: float
    mean_consumption: float
    effective_labor_g: float
    capital_residual: float
    goods_residual: float
    household_budget_residual: float
    mean_drift: float
    hjb_converged: bool
    hjb_true_residual: float
    hjb_iterations: int
    hjb_min_consumption: float
    hjb_lower_boundary_min_drift: float
    hjb_upper_boundary_max_drift: float
    hjb_generator_row_sum_max_abs: float
    hjb_generator_min_off_diagonal: float
    hjb_nan_inf_count: int
    kfe_mass_error: float
    kfe_stationarity_residual: float
    kfe_minimum_mass: float
    kfe_negative_mass_count: int
    kfe_nan_inf_count: int
    state_marginals: FloatArray
    household: HouseholdSolution
    distribution: DistributionSolution

    def scalar_vector(self) -> FloatArray:
        return np.array(
            [
                self.capital,
                self.output,
                self.wage,
                self.net_capital_return,
                self.transfer,
                self.mean_assets,
                self.mean_consumption,
                self.effective_labor_g,
                self.capital_residual,
                self.goods_residual,
                self.household_budget_residual,
                self.mean_drift,
                self.hjb_true_residual,
                self.hjb_generator_row_sum_max_abs,
                self.hjb_generator_min_off_diagonal,
                self.kfe_mass_error,
                self.kfe_stationarity_residual,
                self.kfe_minimum_mass,
            ],
            dtype=np.float64,
        )

    def scalar_names(self) -> tuple[str, ...]:
        return (
            "capital",
            "output",
            "wage",
            "net_capital_return",
            "transfer",
            "mean_assets",
            "mean_consumption",
            "effective_labor_g",
            "capital_residual",
            "goods_residual",
            "household_budget_residual",
            "mean_drift",
            "hjb_true_residual",
            "hjb_generator_row_sum_max_abs",
            "hjb_generator_min_off_diagonal",
            "kfe_mass_error",
            "kfe_stationarity_residual",
            "kfe_minimum_mass",
        )


@dataclass(frozen=True)
class SteadyStateResult:
    config_sha256: str
    root_capital: float
    root_converged: bool
    root_evaluations: int
    root_trace: tuple[tuple[float, float], ...]
    bracket_used: tuple[float, float]
    bracket_from_scan: bool
    final: CapitalEvaluation


def effective_labor_from_ctmc(
    state_generator: FloatArray, efficiency_states: FloatArray
) -> float:
    """Exogenous effective labor from the idiosyncratic CTMC stationary law.

    ``L_bar = sum_z pi_z * z``, where ``pi`` is the stationary distribution of
    the continuous-time generator (``pi @ G = 0``, normalized).
    """
    probabilities = stationary_state_probabilities(state_generator)
    return float(np.dot(probabilities, efficiency_states))


def evaluate_capital(config: SteadyStateConfig, capital: float) -> CapitalEvaluation:
    """Full single-region evaluation at a given capital level (deterministic)."""
    config.validate()
    asset_grid = build_asset_grid(config.a_min, config.a_max, config.asset_grid_count)
    efficiency_states = np.asarray(config.idiosyncratic_states, dtype=np.float64)
    state_generator = build_idiosyncratic_generator(config.q_low_to_high, config.q_high_to_low)
    l_bar = effective_labor_from_ctmc(state_generator, efficiency_states)

    production = production_block(
        capital=capital,
        labor=l_bar,
        productivity=config.productivity,
        alpha_k=config.alpha_k,
        delta=config.delta,
    )
    wage = production.wage
    net_capital_return = production.net_capital_return
    fiscal = balanced_fiscal(
        wage=wage, labor=l_bar, tau_l=config.tau_l, public_outlay=config.public_outlay
    )
    transfer = fiscal.transfer

    household = solve_household(
        asset_grid=asset_grid,
        efficiency_states=efficiency_states,
        state_generator=state_generator,
        wage=wage,
        portfolio_return=net_capital_return,
        transfer=transfer,
        tau_l=config.tau_l,
        rho_hh=config.rho_hh,
        gamma=config.gamma,
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
    mean_assets = distribution.mean_assets
    mean_consumption = distribution.mean_consumption
    effective_labor_g = float(
        np.sum(distribution.mass * efficiency_states[:, None])
    )
    capital_residual = float(capital - mean_assets)
    # Independent accounting diagnostics (computed from aggregated objects,
    # never set to zero by construction).
    goods_residual = float(
        production.output - mean_consumption - config.delta * capital - config.public_outlay
    )
    household_budget_residual = float(
        mean_consumption
        - (
            (1.0 - config.tau_l) * wage * effective_labor_g
            + net_capital_return * mean_assets
            + transfer
        )
    )
    mean_drift = float(np.sum(distribution.mass * household.drift))

    return CapitalEvaluation(
        capital=float(capital),
        output=production.output,
        wage=wage,
        net_capital_return=net_capital_return,
        transfer=transfer,
        mean_assets=mean_assets,
        mean_consumption=mean_consumption,
        effective_labor_g=effective_labor_g,
        capital_residual=capital_residual,
        goods_residual=goods_residual,
        household_budget_residual=household_budget_residual,
        mean_drift=mean_drift,
        hjb_converged=household.converged,
        hjb_true_residual=household.true_residual,
        hjb_iterations=household.iterations,
        hjb_min_consumption=household.min_consumption,
        hjb_lower_boundary_min_drift=household.lower_boundary_min_drift,
        hjb_upper_boundary_max_drift=household.upper_boundary_max_drift,
        hjb_generator_row_sum_max_abs=household.generator_row_sum_max_abs,
        hjb_generator_min_off_diagonal=household.generator_min_off_diagonal,
        hjb_nan_inf_count=household.nan_inf_count,
        kfe_mass_error=distribution.mass_error,
        kfe_stationarity_residual=distribution.stationarity_residual,
        kfe_minimum_mass=distribution.minimum_mass,
        kfe_negative_mass_count=distribution.negative_mass_count,
        kfe_nan_inf_count=distribution.nan_inf_count,
        state_marginals=distribution.state_marginals,
        household=household,
        distribution=distribution,
    )


def _find_sign_changing_bracket(
    config: SteadyStateConfig, trace: list[tuple[float, float]]
) -> tuple[float, float]:
    """Bounded deterministic scan inside ``config.scan_bounds`` (first pair)."""
    lower, upper = config.scan_bounds
    points = np.linspace(lower, upper, config.scan_points)
    previous_residual = None
    previous_point = None
    for point in points:
        residual = evaluate_capital(config, float(point)).capital_residual
        trace.append((float(point), float(residual)))
        if previous_residual is not None:
            if (
                np.isfinite(previous_residual)
                and np.isfinite(residual)
                and previous_residual != 0.0
                and residual != 0.0
                and np.sign(previous_residual) != np.sign(residual)
            ):
                return (float(previous_point), float(point))
        previous_point = point
        previous_residual = residual
    raise NoCapitalBracketError(
        "BLOCKED_DLH_2B_NO_CAPITAL_BRACKET: no finite sign-changing capital "
        "bracket found in the primary bracket or the bounded deterministic scan."
    )


def solve_steady_state(config: SteadyStateConfig) -> SteadyStateResult:
    """Solve ``R_K(K*) = K* - A(K*) = 0`` deterministically."""
    config.validate()
    trace: list[tuple[float, float]] = []
    bracket_from_scan = False

    bracket_lower, bracket_upper = config.capital_bracket
    lower_eval = evaluate_capital(config, bracket_lower)
    upper_eval = evaluate_capital(config, bracket_upper)
    trace.append((bracket_lower, float(lower_eval.capital_residual)))
    trace.append((bracket_upper, float(upper_eval.capital_residual)))

    lower_r = float(lower_eval.capital_residual)
    upper_r = float(upper_eval.capital_residual)
    if np.isfinite(lower_r) and np.isfinite(upper_r):
        if (lower_r == 0.0) or (upper_r == 0.0) or (np.sign(lower_r) != np.sign(upper_r)):
            bracket_lower, bracket_upper = config.capital_bracket
        else:
            bracket_lower, bracket_upper = _find_sign_changing_bracket(config, trace)
            bracket_from_scan = True
    else:
        bracket_lower, bracket_upper = _find_sign_changing_bracket(config, trace)
        bracket_from_scan = True

    def residual_at(capital: float) -> float:
        residual = evaluate_capital(config, capital).capital_residual
        trace.append((float(capital), float(residual)))
        return float(residual)

    root, root_info = brentq(
        residual_at,
        bracket_lower,
        bracket_upper,
        xtol=1e-10,
        rtol=1e-14,
        maxiter=config.numerical.outer_max_iterations,
        full_output=True,
        disp=False,
    )
    final = evaluate_capital(config, float(root))
    root_converged = bool(root_info.converged)
    return SteadyStateResult(
        config_sha256=config.sha256(),
        root_capital=float(root),
        root_converged=root_converged,
        root_evaluations=len(trace),
        root_trace=tuple(trace),
        bracket_used=(bracket_lower, bracket_upper),
        bracket_from_scan=bracket_from_scan,
        final=final,
    )
