"""DLH-3B diagnostics layer: HANK steady-state structural kernel gates.

Assembles the full ``r -> N*(r) -> HJB -> KFE -> asset/labor clearing``
pipeline and evaluates every Issue #11 gate (household HJB/KKT, stationary
KFE, clearing, accounting, nominal consistency, positivity, gross upper-bound
truncation sanity, deterministic reproducibility) against the frozen
thresholds.

Evidence ceiling: ``D2_MACHINE_DIAGNOSTIC__HANK_STEADY_STATE_STRUCTURAL_ONLY``.
A 3B PASS is not full dynamic genuine-HANK validation.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from deep_learning_hank.economics.grids import (
    build_asset_grid,
    build_idiosyncratic_generator,
    stationary_state_probabilities,
)
from deep_learning_hank.economics.hank_nominal import hank_nominal
from deep_learning_hank.hank_config import HankSteadyStateConfig
from deep_learning_hank.solvers.hank_steady_state import (
    EquilibriumEvaluation,
    HankSteadyStateResult,
    solve_hank_steady_state,
)

__all__ = [
    "HankSteadyStateDiagnostics",
    "run_hank_steady_state",
    "run_hank_steady_state_cached",
]

FloatArray = npt.NDArray[np.float64]


@dataclass(frozen=True)
class HankSteadyStateDiagnostics:
    config_sha256: str
    result: HankSteadyStateResult
    root_ok: bool
    household_ok: bool
    kfe_ok: bool
    clearing_ok: bool
    accounting_ok: bool
    nominal_ok: bool
    positivity_ok: bool
    truncation_ok: bool
    state_marginal_error: float
    R_goods: float
    R_fiscal: float
    R_profits: float
    R_wealth: float
    R_nkpc: float
    R_fisher: float
    R_taylor: float
    interest_rate: float
    upper_boundary_mass: float
    top5_mass: float
    lower_boundary_mass: float
    A_hh_over_a_max: float
    all_gates_pass: bool

    def scalar_vector(self) -> FloatArray:
        final = self.result.final
        return np.array(
            [
                self.result.root_r,
                self.interest_rate,
                self.result.root_N,
                final.output,
                final.wage,
                final.transfer,
                final.profits,
                final.C,
                final.A_hh,
                final.R_asset,
                final.R_labor,
                self.R_goods,
                self.R_fiscal,
                self.R_profits,
                self.R_wealth,
                self.R_nkpc,
                self.R_fisher,
                self.R_taylor,
                final.hjb_true_residual,
                final.household.labor_kkt_max,
                final.household.consumption_foc_max,
                final.distribution.mass_error,
                final.distribution.stationarity_residual,
                self.state_marginal_error,
                self.upper_boundary_mass,
                self.top5_mass,
                self.lower_boundary_mass,
                self.A_hh_over_a_max,
            ],
            dtype=np.float64,
        )

    def scalar_names(self) -> tuple[str, ...]:
        return (
            "r_star",
            "i_star",
            "N_star",
            "Y",
            "w",
            "tr",
            "Pi",
            "C",
            "A_hh",
            "R_asset",
            "R_labor",
            "R_goods",
            "R_fiscal",
            "R_profits",
            "R_wealth",
            "R_nkpc",
            "R_fisher",
            "R_taylor",
            "hjb_true_residual",
            "labor_kkt_max",
            "consumption_foc_max",
            "kfe_mass_error",
            "kfe_stationarity_residual",
            "state_marginal_error",
            "upper_boundary_mass",
            "top5_mass",
            "lower_boundary_mass",
            "A_hh_over_a_max",
        )


def _tail_diagnostics(config: HankSteadyStateConfig, final: EquilibriumEvaluation) -> tuple[float, float, float, float]:
    mass = final.distribution.mass
    asset_grid = build_asset_grid(config.a_min, config.a_max, config.asset_grid_count)
    upper_boundary_mass = float(np.sum(mass[:, -1]))
    lower_boundary_mass = float(np.sum(mass[:, 0]))
    top5_count = max(int(np.ceil(0.05 * asset_grid.size)), 1)
    top5_mass = float(np.sum(mass[:, -top5_count:]))
    A_hh_over_a_max = final.A_hh / config.a_max
    return upper_boundary_mass, top5_mass, lower_boundary_mass, A_hh_over_a_max


def run_hank_steady_state(config: HankSteadyStateConfig) -> HankSteadyStateDiagnostics:
    """Run the full DLH-3B steady-state pipeline and evaluate all gates."""
    config.validate()
    result = solve_hank_steady_state(config)
    final = result.final
    tol = config.numerical
    assert final.household is not None and final.distribution is not None

    # --- independent residual objects (computed, never zeroed by labeling) ---
    R_goods = float(final.output - final.C)  # pi=0, G=0
    R_fiscal = float(
        config.tau_l * final.wage * result.root_N - config.bond_supply * result.root_r - final.transfer
    )
    R_profits = float(
        final.profits - (final.output - final.wage * result.root_N)
    )
    R_wealth = float(
        (1.0 - config.tau_l) * final.wage * result.root_N
        + result.root_r * final.A_hh
        + final.transfer
        + final.profits
        - final.C
    )
    nominal = hank_nominal(
        real_return=result.root_r,
        inflation=config.pi_bar,
        inflation_dot=0.0,
        marginal_cost=final.marginal_cost,
        epsilon=config.epsilon,
        phi_p=config.phi_p,
        rho_hh=config.rho_hh,
        phi_pi=config.phi_pi,
        pi_bar=config.pi_bar,
        epsilon_i=config.epsilon_i,
    )
    R_nkpc = nominal.nkpc_residual
    R_fisher = nominal.fisher_residual
    R_taylor = nominal.taylor_residual
    interest_rate = nominal.interest_rate

    # --- state marginal vs symmetric CTMC stationary law ---
    state_generator = build_idiosyncratic_generator(config.q_low_to_high, config.q_high_to_low)
    ctmc_law = stationary_state_probabilities(state_generator)
    state_marginal_error = float(np.max(np.abs(final.distribution.state_marginals - ctmc_law)))

    # --- gates ---
    root_ok = bool(
        result.root_converged
        and final.finite
        and result.outer_bracket_used[0] <= result.root_r <= result.outer_bracket_used[1]
        and abs(final.R_asset) <= tol.clearing_tolerance
        and abs(final.R_labor) <= tol.clearing_tolerance
    )
    household_ok = bool(
        final.household.converged
        and final.household.true_residual <= tol.hjb_tolerance
        and final.household.min_consumption > 0.0
        and final.household.lower_boundary_min_drift >= -1e-12
        and final.household.upper_boundary_max_drift <= 1e-12
        and final.household.generator_row_sum_max_abs <= tol.generator_row_sum_tolerance
        and final.household.generator_min_off_diagonal
        >= tol.generator_min_off_diagonal_tolerance
        and final.household.nan_inf_count == 0
        and final.household.labor_kkt_max <= tol.kkt_tolerance
        and final.household.consumption_foc_max <= tol.consumption_foc_tolerance
    )
    kfe_ok = bool(
        final.distribution.mass_error <= tol.kfe_mass_tolerance
        and final.distribution.stationarity_residual <= tol.kfe_stationarity_tolerance
        and final.distribution.minimum_mass >= tol.negative_mass_threshold
        and final.distribution.negative_mass_count == 0
        and final.distribution.nan_inf_count == 0
        and state_marginal_error <= tol.state_marginal_tolerance
    )
    clearing_ok = bool(
        abs(final.R_asset) <= tol.clearing_tolerance and abs(final.R_labor) <= tol.clearing_tolerance
    )
    accounting_ok = bool(
        abs(R_goods) <= tol.goods_tolerance
        and abs(R_fiscal) <= tol.fiscal_tolerance
        and abs(R_profits) <= tol.profits_tolerance
        and abs(R_wealth) <= tol.wealth_tolerance
    )
    nominal_ok = bool(
        abs(R_nkpc) <= tol.nominal_tolerance
        and abs(R_fisher) <= tol.nominal_tolerance
        and abs(R_taylor) <= tol.nominal_tolerance
    )
    positivity_ok = bool(
        final.output > 0.0
        and result.root_N > 0.0
        and final.C > 0.0
        and final.wage > 0.0
        and config.bond_supply > 0.0
        and final.A_hh > 0.0
        and np.isfinite(result.root_r)
        and np.isfinite(final.transfer)
        and np.isfinite(final.profits)
        and np.isfinite(interest_rate)
    )
    upper_boundary_mass, top5_mass, lower_boundary_mass, A_hh_over_a_max = _tail_diagnostics(
        config, final
    )
    truncation_ok = bool(upper_boundary_mass <= tol.truncation_upper_mass_tolerance)
    all_gates_pass = bool(
        all(
            (
                root_ok,
                household_ok,
                kfe_ok,
                clearing_ok,
                accounting_ok,
                nominal_ok,
                positivity_ok,
                truncation_ok,
            )
        )
    )
    return HankSteadyStateDiagnostics(
        config_sha256=config.sha256(),
        result=result,
        root_ok=root_ok,
        household_ok=household_ok,
        kfe_ok=kfe_ok,
        clearing_ok=clearing_ok,
        accounting_ok=accounting_ok,
        nominal_ok=nominal_ok,
        positivity_ok=positivity_ok,
        truncation_ok=truncation_ok,
        state_marginal_error=state_marginal_error,
        R_goods=R_goods,
        R_fiscal=R_fiscal,
        R_profits=R_profits,
        R_wealth=R_wealth,
        R_nkpc=R_nkpc,
        R_fisher=R_fisher,
        R_taylor=R_taylor,
        interest_rate=interest_rate,
        upper_boundary_mass=upper_boundary_mass,
        top5_mass=top5_mass,
        lower_boundary_mass=lower_boundary_mass,
        A_hh_over_a_max=A_hh_over_a_max,
        all_gates_pass=all_gates_pass,
    )


_CACHE: dict[str, HankSteadyStateDiagnostics] = {}


def run_hank_steady_state_cached(config: HankSteadyStateConfig) -> HankSteadyStateDiagnostics:
    """Test-level cached entry point (single solve shared across gate tests).

    The reproducibility test intentionally bypasses this cache and re-runs the
    pipeline, so the cache never hides non-determinism.
    """
    key = config.sha256()
    if key not in _CACHE:
        _CACHE[key] = run_hank_steady_state(config)
    return _CACHE[key]
