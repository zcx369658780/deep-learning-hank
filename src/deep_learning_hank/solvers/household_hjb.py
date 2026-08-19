"""Continuous-time household HJB solver (Tier-0, single region, fixed prices).

Mathematical contract (accepted DLH-1B / Issue #5):
  * one liquid asset ``a``, finite-state idiosyncratic productivity ``z``;
  * CRRA utility, inelastic labor, controls = consumption + saving/drift;
  * explicit wage / asset-return / transfer / labor-tax inputs; no portfolio
    choice, no region index, no ``W``, no SOE factor, no nominal block;
  * upwind forward/backward first differences with upwind policy selection;
  * boundary = **state-constraint / no-outward-drift treatment**: boundary
    derivative from constrained-consumption marginal utility; lower-boundary
    drift >= 0; upper-boundary drift <= 0 (no reflected-process claim);
  * generator = **continuous-time infinitesimal generator / intensity matrix**:
    off-diagonals >= 0; diagonal = negative total outflow; row sums = 0
    (NOT row-stochastic);
  * true HJB residual ``max|rho*V - (u(c) + G@V)|``.

REIMPLEMENTATION (clean economics/solver separation) based on the audited
source pattern ``household_hjb.py``; no wholesale copy.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt
from scipy import sparse
from scipy.sparse.linalg import spsolve

from deep_learning_hank.economics.preferences import (
    inverse_marginal_utility,
    marginal_utility,
    utility,
)

__all__ = ["HouseholdSolution", "solve_household"]

FloatArray = npt.NDArray[np.float64]


@dataclass(frozen=True)
class HouseholdSolution:
    value: FloatArray
    consumption: FloatArray
    drift: FloatArray
    generator: sparse.csr_matrix
    converged: bool
    iterations: int
    true_residual: float
    min_consumption: float
    lower_boundary_min_drift: float
    upper_boundary_max_drift: float
    generator_row_sum_max_abs: float
    generator_min_off_diagonal: float
    nan_inf_count: int
    residual_history: tuple[float, ...]


def _policy_from_value(
    value: FloatArray,
    *,
    asset_grid: FloatArray,
    cash_on_hand: FloatArray,
    gamma: float,
    consumption_floor: float,
) -> tuple[FloatArray, FloatArray]:
    """Upwind policy from value (state-constraint / no-outward-drift boundary)."""
    spacing = float(asset_grid[1] - asset_grid[0])
    derivative_forward = np.empty_like(value)
    derivative_backward = np.empty_like(value)
    derivative_forward[:, :-1] = (value[:, 1:] - value[:, :-1]) / spacing
    derivative_backward[:, 1:] = (value[:, 1:] - value[:, :-1]) / spacing
    constrained_consumption = np.maximum(cash_on_hand, consumption_floor)
    boundary_marginal = marginal_utility(constrained_consumption, gamma=gamma)
    derivative_backward[:, 0] = boundary_marginal[:, 0]
    derivative_forward[:, -1] = boundary_marginal[:, -1]
    derivative_forward = np.maximum(derivative_forward, 1e-14)
    derivative_backward = np.maximum(derivative_backward, 1e-14)

    consumption_forward = np.maximum(
        inverse_marginal_utility(derivative_forward, gamma=gamma), consumption_floor
    )
    consumption_backward = np.maximum(
        inverse_marginal_utility(derivative_backward, gamma=gamma), consumption_floor
    )
    drift_forward = cash_on_hand - consumption_forward
    drift_backward = cash_on_hand - consumption_backward

    hamiltonian_zero = utility(constrained_consumption, gamma=gamma)
    hamiltonian_forward = utility(consumption_forward, gamma=gamma) + (
        derivative_forward * drift_forward
    )
    hamiltonian_backward = utility(consumption_backward, gamma=gamma) + (
        derivative_backward * drift_backward
    )
    forward_feasible = drift_forward > 0.0
    forward_feasible[:, -1] = False
    backward_feasible = drift_backward < 0.0
    backward_feasible[:, 0] = False
    hamiltonian_forward = np.where(forward_feasible, hamiltonian_forward, -np.inf)
    hamiltonian_backward = np.where(backward_feasible, hamiltonian_backward, -np.inf)

    choice = np.argmax(
        np.stack((hamiltonian_zero, hamiltonian_forward, hamiltonian_backward), axis=0),
        axis=0,
    )
    consumption = np.where(
        choice == 1,
        consumption_forward,
        np.where(choice == 2, consumption_backward, constrained_consumption),
    )
    drift = cash_on_hand - consumption
    # State-constraint / no-outward-drift boundary treatment.
    drift[:, 0] = np.maximum(drift[:, 0], 0.0)
    drift[:, -1] = np.minimum(drift[:, -1], 0.0)
    return np.asarray(consumption, dtype=np.float64), np.asarray(drift, dtype=np.float64)


def _policy_generator(
    drift: FloatArray, state_generator: FloatArray, spacing: float
) -> sparse.csr_matrix:
    """Continuous-time infinitesimal generator (off-diagonals >= 0, rows sum 0)."""
    state_count, asset_count = drift.shape
    size = state_count * asset_count
    generator = sparse.lil_matrix((size, size), dtype=np.float64)
    for state in range(state_count):
        for asset in range(asset_count):
            row = state * asset_count + asset
            for destination in range(state_count):
                if destination != state:
                    generator[row, destination * asset_count + asset] = state_generator[
                        state, destination
                    ]
            generator[row, row] = state_generator[state, state]
            asset_drift = float(drift[state, asset])
            if asset_drift > 0.0 and asset < asset_count - 1:
                rate = asset_drift / spacing
                generator[row, row + 1] += rate
                generator[row, row] -= rate
            elif asset_drift < 0.0 and asset > 0:
                rate = -asset_drift / spacing
                generator[row, row - 1] += rate
                generator[row, row] -= rate
    return generator.tocsr()


def solve_household(
    *,
    asset_grid: FloatArray,
    efficiency_states: FloatArray,
    state_generator: FloatArray,
    wage: float,
    portfolio_return: float,
    transfer: float,
    tau_l: float,
    rho_hh: float,
    gamma: float,
    tolerance: float,
    max_iterations: int,
    pseudo_time_step: float,
    consumption_floor: float,
) -> HouseholdSolution:
    if asset_grid.ndim != 1 or efficiency_states.ndim != 1:
        raise ValueError("household state grids must be one-dimensional")
    if state_generator.shape != (efficiency_states.size, efficiency_states.size):
        raise ValueError("idiosyncratic generator dimensions do not match")
    if not np.allclose(state_generator.sum(axis=1), 0.0, atol=1e-12):
        raise ValueError("state_generator must be a CTMC generator / intensity matrix (rows sum 0)")
    spacing_values = np.diff(asset_grid)
    if np.any(spacing_values <= 0.0) or not np.allclose(spacing_values, spacing_values[0]):
        raise ValueError("the HJB uses a uniform increasing asset grid")

    cash_on_hand = (
        (1.0 - tau_l) * wage * efficiency_states[:, None]
        + portfolio_return * asset_grid[None, :]
        + transfer
    )
    initial_consumption = np.maximum(cash_on_hand, consumption_floor)
    value = utility(initial_consumption, gamma=gamma) / rho_hh
    identity = sparse.eye(value.size, format="csr", dtype=np.float64)
    residual_history: list[float] = []
    converged = False
    consumption = initial_consumption
    drift = cash_on_hand - consumption
    generator = _policy_generator(drift, state_generator, float(spacing_values[0]))
    final_consumption = consumption
    final_drift = drift
    final_generator = generator
    iteration = 0

    for iteration in range(1, max_iterations + 1):
        consumption, drift = _policy_from_value(
            value,
            asset_grid=asset_grid,
            cash_on_hand=cash_on_hand,
            gamma=gamma,
            consumption_floor=consumption_floor,
        )
        generator = _policy_generator(drift, state_generator, float(spacing_values[0]))
        matrix = (rho_hh + 1.0 / pseudo_time_step) * identity - generator
        rhs = utility(consumption, gamma=gamma).ravel() + value.ravel() / pseudo_time_step
        value = np.asarray(spsolve(matrix, rhs), dtype=np.float64).reshape(value.shape)

        final_consumption, final_drift = _policy_from_value(
            value,
            asset_grid=asset_grid,
            cash_on_hand=cash_on_hand,
            gamma=gamma,
            consumption_floor=consumption_floor,
        )
        final_generator = _policy_generator(
            final_drift, state_generator, float(spacing_values[0])
        )
        residual = rho_hh * value.ravel() - (
            utility(final_consumption, gamma=gamma).ravel()
            + final_generator @ value.ravel()
        )
        true_residual = float(np.max(np.abs(residual)))
        residual_history.append(true_residual)
        if true_residual <= tolerance:
            converged = True
            break

    row_sums = np.asarray(final_generator.sum(axis=1)).ravel()
    generator_row_sum_max_abs = float(np.max(np.abs(row_sums)))
    off_diagonal = final_generator - sparse.diags(
        final_generator.diagonal(), format="csr", dtype=np.float64
    )
    min_off_diagonal = float(np.min(off_diagonal.data)) if off_diagonal.nnz else 0.0
    nan_inf_count = int(
        np.count_nonzero(~np.isfinite(value))
        + np.count_nonzero(~np.isfinite(final_consumption))
        + np.count_nonzero(~np.isfinite(final_drift))
        + np.count_nonzero(~np.isfinite(final_generator.data))
    )
    return HouseholdSolution(
        value=value,
        consumption=final_consumption,
        drift=final_drift,
        generator=final_generator,
        converged=converged,
        iterations=iteration,
        true_residual=true_residual,
        min_consumption=float(np.min(final_consumption)),
        lower_boundary_min_drift=float(np.min(final_drift[:, 0])),
        upper_boundary_max_drift=float(np.max(final_drift[:, -1])),
        generator_row_sum_max_abs=generator_row_sum_max_abs,
        generator_min_off_diagonal=min_off_diagonal,
        nan_inf_count=nan_inf_count,
        residual_history=tuple(residual_history),
    )
