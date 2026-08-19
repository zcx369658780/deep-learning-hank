"""Diagnostics layer: single-region Tier-0 steady-state GE validation pipeline.

Assembles the full K -> firm -> fiscal -> HJB -> KFE -> capital-clearing
pipeline, evaluates every Issue #6 gate against the accepted thresholds, and
exposes the scalar diagnostics for reproducibility comparison.

R1: adds the explicit root-trace finiteness machine gate
``root_trace_finite_ok`` (all trace capital/residual entries finite), required
by Issue #6 ("all root evaluations finite") and folded into the root gate and
the overall all-gates verdict.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from deep_learning_hank.config import SteadyStateConfig
from deep_learning_hank.economics.grids import (
    build_asset_grid,
    build_idiosyncratic_generator,
)
from deep_learning_hank.solvers.steady_state import (
    SteadyStateResult,
    effective_labor_from_ctmc,
    solve_steady_state,
)

__all__ = ["SteadyStateDiagnostics", "run_tier0_steady_state"]

FloatArray = npt.NDArray[np.float64]


@dataclass(frozen=True)
class SteadyStateDiagnostics:
    config_sha256: str
    result: SteadyStateResult
    l_bar: float
    effective_labor_error: float
    root_trace_finite_ok: bool
    root_gate_ok: bool
    capital_clearing_ok: bool
    hjb_ok: bool
    kfe_ok: bool
    effective_labor_ok: bool
    fiscal_ok: bool
    goods_ok: bool
    budget_ok: bool
    mean_drift_ok: bool
    positivity_ok: bool
    all_gates_pass: bool

    def scalar_vector(self) -> FloatArray:
        return self.result.final.scalar_vector()

    def scalar_names(self) -> tuple[str, ...]:
        return self.result.final.scalar_names()


def run_tier0_steady_state(config: SteadyStateConfig) -> SteadyStateDiagnostics:
    """Run the single-region Tier-0 steady-state pipeline and evaluate gates."""
    config.validate()
    asset_grid = build_asset_grid(config.a_min, config.a_max, config.asset_grid_count)
    efficiency_states = np.asarray(config.idiosyncratic_states, dtype=np.float64)
    state_generator = build_idiosyncratic_generator(config.q_low_to_high, config.q_high_to_low)
    l_bar = effective_labor_from_ctmc(state_generator, efficiency_states)
    result = solve_steady_state(config)
    final = result.final
    tol = config.numerical

    # R1 machine gate: every root-trace entry (capital and residual) finite.
    root_trace_finite_ok = bool(
        all(
            np.isfinite(k) and np.isfinite(r)
            for k, r in result.root_trace
        )
    )
    root_gate_ok = bool(
        result.root_converged
        and final.capital > 0.0
        and result.bracket_used[0] <= final.capital <= result.bracket_used[1]
        and abs(final.capital_residual) <= tol.outer_capital_tolerance
        and np.isfinite(final.capital_residual)
        and root_trace_finite_ok
    )
    capital_clearing_ok = bool(
        abs(final.capital_residual) <= tol.outer_capital_tolerance
    )
    hjb_ok = bool(
        final.hjb_converged
        and final.hjb_true_residual <= tol.hjb_tolerance
        and final.hjb_min_consumption > 0.0
        and final.hjb_lower_boundary_min_drift >= -1e-12
        and final.hjb_upper_boundary_max_drift <= 1e-12
        and final.hjb_generator_row_sum_max_abs <= tol.generator_row_sum_tolerance
        and final.hjb_generator_min_off_diagonal >= tol.generator_min_off_diagonal_tolerance
        and final.hjb_nan_inf_count == 0
    )
    kfe_ok = bool(
        final.kfe_mass_error <= tol.kfe_mass_tolerance
        and final.kfe_stationarity_residual <= tol.kfe_stationarity_tolerance
        and final.kfe_minimum_mass >= tol.negative_mass_threshold
        and final.kfe_negative_mass_count == 0
        and final.kfe_nan_inf_count == 0
    )
    effective_labor_error = abs(final.effective_labor_g - l_bar)
    effective_labor_ok = bool(
        np.isfinite(l_bar) and l_bar > 0.0 and effective_labor_error <= 1e-8
    )
    fiscal_residual = abs(
        final.transfer - (config.tau_l * final.wage * l_bar - config.public_outlay)
    )
    fiscal_ok = bool(fiscal_residual <= 1e-12)
    goods_ok = bool(abs(final.goods_residual) <= 1e-7)
    budget_ok = bool(abs(final.household_budget_residual) <= 1e-7)
    mean_drift_ok = bool(abs(final.mean_drift) <= 1e-7)
    positivity_ok = bool(
        final.output > 0.0
        and final.wage > 0.0
        and final.mean_consumption > 0.0
        and final.capital > 0.0
        and np.isfinite(final.net_capital_return)
    )
    all_gates_pass = bool(
        all(
            (
                root_gate_ok,
                hjb_ok,
                kfe_ok,
                effective_labor_ok,
                fiscal_ok,
                goods_ok,
                budget_ok,
                mean_drift_ok,
                positivity_ok,
            )
        )
    )
    return SteadyStateDiagnostics(
        config_sha256=config.sha256(),
        result=result,
        l_bar=l_bar,
        effective_labor_error=effective_labor_error,
        root_trace_finite_ok=root_trace_finite_ok,
        root_gate_ok=root_gate_ok,
        capital_clearing_ok=capital_clearing_ok,
        hjb_ok=hjb_ok,
        kfe_ok=kfe_ok,
        effective_labor_ok=effective_labor_ok,
        fiscal_ok=fiscal_ok,
        goods_ok=goods_ok,
        budget_ok=budget_ok,
        mean_drift_ok=mean_drift_ok,
        positivity_ok=positivity_ok,
        all_gates_pass=all_gates_pass,
    )
