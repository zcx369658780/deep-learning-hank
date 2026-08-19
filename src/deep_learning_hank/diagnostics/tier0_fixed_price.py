"""Diagnostics layer: Tier-0 fixed-price HJB/KFE validation pipeline.

``diagnostics`` is independent of the trainer/solver internals: it assembles
the fixed-price run, evaluates every gate against the accepted thresholds, and
exposes the scalar diagnostics for reproducibility comparison.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from deep_learning_hank.config import FixedPriceConfig
from deep_learning_hank.economics.grids import (
    build_asset_grid,
    build_idiosyncratic_generator,
)
from deep_learning_hank.solvers.distribution_kfe import (
    DistributionSolution,
    solve_stationary_distribution,
)
from deep_learning_hank.solvers.household_hjb import (
    HouseholdSolution,
    solve_household,
)

__all__ = ["FixedPriceDiagnostics", "run_fixed_price_validation"]

FloatArray = npt.NDArray[np.float64]


@dataclass(frozen=True)
class FixedPriceDiagnostics:
    config_sha256: str
    household: HouseholdSolution
    distribution: DistributionSolution
    state_marginals: FloatArray
    analytic_state_marginals: FloatArray
    state_marginal_error: float
    hjb_residual_ok: bool
    min_consumption_ok: bool
    lower_boundary_drift_ok: bool
    upper_boundary_drift_ok: bool
    generator_row_sum_ok: bool
    generator_off_diagonal_ok: bool
    nan_inf_ok: bool
    kfe_mass_ok: bool
    kfe_stationarity_ok: bool
    kfe_min_mass_ok: bool
    kfe_negative_count_ok: bool
    kfe_marginals_ok: bool
    kfe_mean_assets_ok: bool
    kfe_nan_inf_ok: bool
    all_gates_pass: bool
    hjb_iterations: int

    def scalar_vector(self) -> FloatArray:
        return np.array(
            [
                self.household.true_residual,
                self.household.min_consumption,
                self.household.lower_boundary_min_drift,
                self.household.upper_boundary_max_drift,
                self.household.generator_row_sum_max_abs,
                self.household.generator_min_off_diagonal,
                float(self.household.nan_inf_count),
                self.distribution.mass_error,
                self.distribution.stationarity_residual,
                self.distribution.minimum_mass,
                float(self.distribution.negative_mass_count),
                float(self.distribution.nan_inf_count),
                self.state_marginal_error,
                self.distribution.mean_assets,
                self.distribution.mean_consumption,
            ],
            dtype=np.float64,
        )

    def scalar_names(self) -> tuple[str, ...]:
        return (
            "hjb_true_residual",
            "hjb_min_consumption",
            "hjb_lower_boundary_min_drift",
            "hjb_upper_boundary_max_drift",
            "hjb_generator_row_sum_max_abs",
            "hjb_generator_min_off_diagonal",
            "hjb_nan_inf_count",
            "kfe_mass_error",
            "kfe_stationarity_residual",
            "kfe_minimum_mass",
            "kfe_negative_mass_count",
            "kfe_nan_inf_count",
            "kfe_state_marginal_error",
            "kfe_mean_assets",
            "kfe_mean_consumption",
        )


def run_fixed_price_validation(config: FixedPriceConfig) -> FixedPriceDiagnostics:
    """Run the fixed-price HJB + stationary KFE pipeline for Tier-0A."""
    config.validate()
    asset_grid = build_asset_grid(config.a_min, config.a_max, config.asset_grid_count)
    efficiency_states = np.asarray(config.idiosyncratic_states, dtype=np.float64)
    state_generator = build_idiosyncratic_generator(config.q_low_to_high, config.q_high_to_low)

    household = solve_household(
        asset_grid=asset_grid,
        efficiency_states=efficiency_states,
        state_generator=state_generator,
        wage=config.wage,
        portfolio_return=config.portfolio_return,
        transfer=config.transfer,
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
    state_marginals = distribution.state_marginals
    analytic_state_marginals = np.array([0.5, 0.5], dtype=np.float64)
    state_marginal_error = float(np.max(np.abs(state_marginals - analytic_state_marginals)))

    tol = config.numerical
    hjb_residual_ok = household.true_residual <= tol.hjb_tolerance
    min_consumption_ok = household.min_consumption > 0.0
    lower_boundary_drift_ok = household.lower_boundary_min_drift >= -1e-12
    upper_boundary_drift_ok = household.upper_boundary_max_drift <= 1e-12
    generator_row_sum_ok = household.generator_row_sum_max_abs <= tol.generator_row_sum_tolerance
    generator_off_diagonal_ok = (
        household.generator_min_off_diagonal >= tol.generator_min_off_diagonal_tolerance
    )
    nan_inf_ok = household.nan_inf_count == 0
    kfe_mass_ok = distribution.mass_error <= tol.kfe_mass_tolerance
    kfe_stationarity_ok = (
        distribution.stationarity_residual <= tol.kfe_stationarity_tolerance
    )
    kfe_min_mass_ok = distribution.minimum_mass >= tol.negative_mass_threshold
    kfe_negative_count_ok = distribution.negative_mass_count == 0
    kfe_marginals_ok = state_marginal_error <= 1e-8
    kfe_mean_assets_ok = 0.0 <= distribution.mean_assets <= config.a_max
    kfe_nan_inf_ok = distribution.nan_inf_count == 0

    all_gates_pass = all(
        (
            hjb_residual_ok,
            min_consumption_ok,
            lower_boundary_drift_ok,
            upper_boundary_drift_ok,
            generator_row_sum_ok,
            generator_off_diagonal_ok,
            nan_inf_ok,
            kfe_mass_ok,
            kfe_stationarity_ok,
            kfe_min_mass_ok,
            kfe_negative_count_ok,
            kfe_marginals_ok,
            kfe_mean_assets_ok,
            kfe_nan_inf_ok,
        )
    )
    return FixedPriceDiagnostics(
        config_sha256=config.sha256(),
        household=household,
        distribution=distribution,
        state_marginals=state_marginals,
        analytic_state_marginals=analytic_state_marginals,
        state_marginal_error=state_marginal_error,
        hjb_residual_ok=hjb_residual_ok,
        min_consumption_ok=min_consumption_ok,
        lower_boundary_drift_ok=lower_boundary_drift_ok,
        upper_boundary_drift_ok=upper_boundary_drift_ok,
        generator_row_sum_ok=generator_row_sum_ok,
        generator_off_diagonal_ok=generator_off_diagonal_ok,
        nan_inf_ok=nan_inf_ok,
        kfe_mass_ok=kfe_mass_ok,
        kfe_stationarity_ok=kfe_stationarity_ok,
        kfe_min_mass_ok=kfe_min_mass_ok,
        kfe_negative_count_ok=kfe_negative_count_ok,
        kfe_marginals_ok=kfe_marginals_ok,
        kfe_mean_assets_ok=kfe_mean_assets_ok,
        kfe_nan_inf_ok=kfe_nan_inf_ok,
        all_gates_pass=all_gates_pass,
        hjb_iterations=household.iterations,
    )
