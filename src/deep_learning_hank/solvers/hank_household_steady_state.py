"""DLH-3B HANK household steady-state solver (isolated module).

Implements the Issue #11 §5 contract for the zero-inflation / zero-shock
steady-state household block:

- upwind HJB with **endogenous static labor** (control, not state);
- three candidate policies per node: zero-drift (§5.2), forward (saving) and
  backward (dissaving), with Hamiltonian selection consistent with the
  accepted Tier-0 upwind / state-constraint / no-outward-drift semantics;
- state-constraint boundaries: drift >= 0 at ``a_min``, drift <= 0 at ``a_max``;
- continuous-time infinitesimal generator / intensity matrix conventions
  (off-diagonals >= 0, rows sum 0);
- labor KKT and consumption-FOC diagnostics (§5.3).

The zero-drift policy depends only on aggregate inputs (``r, w, tr, Pi``), so
it is solved once per aggregate evaluation, not per HJB iteration.

This module is new and isolated: accepted Tier-0 ``household_hjb.py`` is not
modified.  Utility helpers come from accepted ``economics/preferences.py``;
generator/grid semantics mirror the accepted conventions.

``VALIDATION_FIXTURE_NOT_CALIBRATION`` / ``HANK_STEADY_STATE_STRUCTURAL_ONLY``.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt
from scipy import sparse
from scipy.optimize import brentq
from scipy.sparse.linalg import spsolve

from deep_learning_hank.economics.preferences import (
    inverse_marginal_utility,
    marginal_utility,
    utility,
)

__all__ = [
    "HankHouseholdFeasibilityError",
    "HankHouseholdSolution",
    "labor_disutility",
    "labor_policy",
    "marginal_labor_disutility",
    "solve_hank_household",
    "zero_drift_policy",
]

FloatArray = npt.NDArray[np.float64]


class HankHouseholdFeasibilityError(RuntimeError):
    """Raised when no feasible positive-consumption zero-drift policy exists
    at some state/node for the given aggregate inputs (Issue #11 §5.2)."""


@dataclass(frozen=True)
class HankHouseholdSolution:
    value: FloatArray
    consumption: FloatArray
    labor: FloatArray
    drift: FloatArray
    policy_choice: FloatArray
    generator: sparse.csr_matrix
    converged: bool
    iterations: int
    true_residual: float
    min_consumption: float
    lower_boundary_min_drift: float
    upper_boundary_max_drift: float
    generator_row_sum_max_abs: float
    generator_min_off_diagonal: float
    generator_min_positive_off_diagonal: float
    labor_kkt_max: float
    consumption_foc_max: float
    nan_inf_count: int
    residual_history: tuple[float, ...]


def labor_disutility(n: FloatArray, *, chi: float, frisch: float) -> FloatArray:
    """``v(n) = chi * n^(1+1/frisch) / (1+1/frisch)``."""
    exponent = 1.0 + 1.0 / frisch
    return chi * np.asarray(n, dtype=np.float64) ** exponent / exponent


def marginal_labor_disutility(n: FloatArray, *, chi: float, frisch: float) -> FloatArray:
    """``v'(n) = chi * n^(1/frisch)``."""
    return chi * np.asarray(n, dtype=np.float64) ** (1.0 / frisch)


def labor_policy(
    effective_wage: FloatArray, marginal_value: FloatArray, *, chi: float, frisch: float, n_max: float
) -> FloatArray:
    """Static labor FOC ``v'(n) = q*V_a`` with KKT clipping to ``[0, n_max]``."""
    raw = (np.asarray(effective_wage, dtype=np.float64) * np.asarray(marginal_value, dtype=np.float64) / chi) ** frisch
    return np.clip(raw, 0.0, n_max)


def _solve_zero_drift_node(
    q: float, b: float, *, gamma: float, frisch: float, chi: float, n_max: float, consumption_floor: float
) -> tuple[float, float, bool]:
    """Solve the static zero-saving problem at one node (Issue #11 §5.2).

    Returns ``(c0, n0, feasible)`` with ``c0 = b + q*n0 > consumption_floor``.
    The scalar FOC ``chi*n0^(1/frisch) = q*c0^(-gamma)`` is monotone in
    ``n0`` on the feasible interval; solved deterministically with ``brentq``.
    """
    if q <= 0.0:
        return (float("nan"), float("nan"), False)
    c_max = b + q * n_max
    if c_max <= consumption_floor:
        # No n in [0, n_max] can deliver positive consumption.
        return (float("nan"), float("nan"), False)

    def f(n: float) -> float:
        c = b + q * n
        if c <= consumption_floor:
            return -np.inf
        return chi * n ** (1.0 / frisch) - q * c ** (-gamma)

    f_max = f(n_max)
    if f_max <= 0.0:
        # Interior solution at or above n_max -> upper-bound KKT solution.
        return (float(c_max), float(n_max), True)
    n_min = max(0.0, (consumption_floor - b) / q)
    f_min = f(n_min)
    if f_min >= 0.0:
        # The constrained optimum would sit at c0 == consumption_floor, which
        # violates the strict positive-consumption requirement.
        return (float("nan"), float("nan"), False)
    root = brentq(f, n_min, n_max, xtol=1e-14)
    c0 = b + q * root
    return (float(c0), float(root), True)


def zero_drift_policy(
    q: FloatArray,
    b: FloatArray,
    *,
    gamma: float,
    frisch: float,
    chi: float,
    n_max: float,
    consumption_floor: float,
) -> tuple[FloatArray, FloatArray, FloatArray]:
    """Vectorized zero-drift policy over the ``(state, asset)`` grid."""
    consumption = np.empty_like(q)
    labor = np.empty_like(q)
    feasible = np.zeros(q.shape, dtype=bool)
    for idx in np.ndindex(q.shape):
        c0, n0, ok = _solve_zero_drift_node(
            float(q[idx]), float(b[idx]), gamma=gamma, frisch=frisch, chi=chi, n_max=n_max,
            consumption_floor=consumption_floor,
        )
        consumption[idx] = c0
        labor[idx] = n0
        feasible[idx] = ok
    return consumption, labor, feasible


def _policy_from_value(
    value: FloatArray,
    *,
    asset_grid: FloatArray,
    q: FloatArray,
    b: FloatArray,
    c0: FloatArray,
    n0: FloatArray,
    zero_feasible: FloatArray,
    gamma: float,
    frisch: float,
    chi: float,
    n_max: float,
    consumption_floor: float,
) -> tuple[FloatArray, FloatArray, FloatArray, FloatArray, FloatArray]:
    """Upwind policy selection with the three candidates (zero/forward/backward)."""
    spacing = float(asset_grid[1] - asset_grid[0])
    derivative_forward = np.empty_like(value)
    derivative_backward = np.empty_like(value)
    derivative_forward[:, :-1] = (value[:, 1:] - value[:, :-1]) / spacing
    derivative_backward[:, 1:] = (value[:, 1:] - value[:, :-1]) / spacing
    # State-constraint / no-outward-drift boundary: boundary derivative from
    # the marginal utility of the zero-drift (constrained) consumption.
    boundary_marginal = marginal_utility(c0, gamma=gamma)
    derivative_backward[:, 0] = boundary_marginal[:, 0]
    derivative_forward[:, -1] = boundary_marginal[:, -1]
    derivative_forward = np.maximum(derivative_forward, 1e-14)
    derivative_backward = np.maximum(derivative_backward, 1e-14)

    c_forward = np.maximum(
        inverse_marginal_utility(derivative_forward, gamma=gamma), consumption_floor
    )
    n_forward = labor_policy(q, derivative_forward, chi=chi, frisch=frisch, n_max=n_max)
    drift_forward = q * n_forward + b - c_forward
    hamiltonian_forward = (
        utility(c_forward, gamma=gamma)
        - labor_disutility(n_forward, chi=chi, frisch=frisch)
        + derivative_forward * drift_forward
    )

    c_backward = np.maximum(
        inverse_marginal_utility(derivative_backward, gamma=gamma), consumption_floor
    )
    n_backward = labor_policy(q, derivative_backward, chi=chi, frisch=frisch, n_max=n_max)
    drift_backward = q * n_backward + b - c_backward
    hamiltonian_backward = (
        utility(c_backward, gamma=gamma)
        - labor_disutility(n_backward, chi=chi, frisch=frisch)
        + derivative_backward * drift_backward
    )

    hamiltonian_zero = utility(c0, gamma=gamma) - labor_disutility(n0, chi=chi, frisch=frisch)
    drift_zero = q * n0 + b - c0

    forward_feasible = drift_forward > 0.0
    forward_feasible[:, -1] = False
    backward_feasible = drift_backward < 0.0
    backward_feasible[:, 0] = False
    zero_feasible_arr = zero_feasible.astype(bool)

    hamiltonian_forward = np.where(forward_feasible, hamiltonian_forward, -np.inf)
    hamiltonian_backward = np.where(backward_feasible, hamiltonian_backward, -np.inf)
    hamiltonian_zero = np.where(zero_feasible_arr, hamiltonian_zero, -np.inf)

    choice = np.argmax(
        np.stack((hamiltonian_zero, hamiltonian_forward, hamiltonian_backward), axis=0),
        axis=0,
    )
    consumption = np.where(choice == 1, c_forward, np.where(choice == 2, c_backward, c0))
    labor = np.where(choice == 1, n_forward, np.where(choice == 2, n_backward, n0))
    drift = np.where(choice == 1, drift_forward, np.where(choice == 2, drift_backward, drift_zero))
    # State-constraint / no-outward-drift boundary treatment.
    drift[:, 0] = np.maximum(drift[:, 0], 0.0)
    drift[:, -1] = np.minimum(drift[:, -1], 0.0)
    # Marginal value associated with the selected policy (KKT evaluation): the
    # forward/backward derivative for saving/dissaving; for the zero-drift
    # policy the envelope marginal value u'(c0) of the static zero-saving
    # problem (documented R1-consistent KKT convention).
    selected_marginal = np.where(
        choice == 1,
        derivative_forward,
        np.where(choice == 2, derivative_backward, marginal_utility(c0, gamma=gamma)),
    )
    return (
        np.asarray(consumption, dtype=np.float64),
        np.asarray(labor, dtype=np.float64),
        np.asarray(drift, dtype=np.float64),
        np.asarray(choice, dtype=np.int64),
        np.asarray(selected_marginal, dtype=np.float64),
    )


def _build_generator(drift: FloatArray, state_generator: FloatArray, spacing: float) -> sparse.csr_matrix:
    """Continuous-time infinitesimal generator (off-diagonals >= 0, rows sum 0).

    Mirrors the accepted Tier-0 generator semantics: upwind asset-drift rates
    plus the idiosyncratic CTMC transitions.  Vectorized construction
    (COO with duplicate-summing) for the DLH-3B grid sizes.
    """
    state_count, asset_count = drift.shape
    size = state_count * asset_count
    row_list: list[npt.NDArray[np.int64]] = []
    col_list: list[npt.NDArray[np.int64]] = []
    val_list: list[npt.NDArray[np.float64]] = []
    for state in range(state_count):
        base = state * asset_count
        for destination in range(state_count):
            rate = float(state_generator[state, destination])
            if rate != 0.0:
                idx = np.arange(asset_count, dtype=np.int64)
                row_list.append(base + idx)
                col_list.append(destination * asset_count + idx)
                val_list.append(np.full(asset_count, rate, dtype=np.float64))
        drift_state = drift[state]
        right = np.flatnonzero((drift_state > 0.0) & (np.arange(asset_count) < asset_count - 1))
        if right.size:
            rate = drift_state[right] / spacing
            row_list.append(base + right)
            col_list.append(base + right + 1)
            val_list.append(rate)
            row_list.append(base + right)
            col_list.append(base + right)
            val_list.append(-rate)
        left = np.flatnonzero((drift_state < 0.0) & (np.arange(asset_count) > 0))
        if left.size:
            rate = -drift_state[left] / spacing
            row_list.append(base + left)
            col_list.append(base + left - 1)
            val_list.append(rate)
            row_list.append(base + left)
            col_list.append(base + left)
            val_list.append(-rate)
    if row_list:
        rows = np.concatenate(row_list)
        cols = np.concatenate(col_list)
        vals = np.concatenate(val_list)
        generator = sparse.coo_matrix((vals, (rows, cols)), shape=(size, size)).tocsr()
    else:
        generator = sparse.csr_matrix((size, size), dtype=np.float64)
    return generator


def _kkt_diagnostics(
    q: FloatArray,
    labor: FloatArray,
    selected_marginal: FloatArray,
    consumption: FloatArray,
    *,
    chi: float,
    frisch: float,
    n_max: float,
    gamma: float,
) -> tuple[float, float]:
    """Labor KKT and consumption-FOC maximum violations (Issue #11 §5.3)."""
    labor_gap = q * selected_marginal - marginal_labor_disutility(labor, chi=chi, frisch=frisch)
    interior = (labor > 0.0) & (labor < n_max)
    kkt = np.where(
        interior,
        np.abs(labor_gap),
        np.where(labor <= 0.0, np.maximum(labor_gap, 0.0), np.maximum(-labor_gap, 0.0)),
    )
    consumption_gap = np.abs(selected_marginal - marginal_utility(consumption, gamma=gamma))
    return float(np.max(kkt)), float(np.max(consumption_gap))


def solve_hank_household(
    *,
    asset_grid: FloatArray,
    efficiency_states: FloatArray,
    state_generator: FloatArray,
    wage: float,
    real_return: float,
    transfer: float,
    profits: float,
    tau_l: float,
    rho_hh: float,
    gamma: float,
    frisch: float,
    chi: float,
    n_max: float,
    tolerance: float,
    max_iterations: int,
    pseudo_time_step: float,
    consumption_floor: float,
) -> HankHouseholdSolution:
    """Solve the stationary household HJB with endogenous static labor."""
    if asset_grid.ndim != 1 or efficiency_states.ndim != 1:
        raise ValueError("household state grids must be one-dimensional")
    if state_generator.shape != (efficiency_states.size, efficiency_states.size):
        raise ValueError("idiosyncratic generator dimensions do not match")
    if not np.allclose(state_generator.sum(axis=1), 0.0, atol=1e-12):
        raise ValueError("state_generator must be a CTMC generator / intensity matrix (rows sum 0)")
    spacing_values = np.diff(asset_grid)
    if np.any(spacing_values <= 0.0) or not np.allclose(spacing_values, spacing_values[0]):
        raise ValueError("the HJB uses a uniform increasing asset grid")
    if rho_hh <= 0.0 or gamma <= 0.0 or chi <= 0.0 or frisch <= 0.0 or n_max <= 0.0:
        raise ValueError("household preference/technology controls must be strictly positive")

    spacing = float(spacing_values[0])
    state_count = efficiency_states.size
    asset_count = asset_grid.size
    q = np.broadcast_to(
        (1.0 - tau_l) * wage * efficiency_states[:, None], (state_count, asset_count)
    ).copy()
    b = np.broadcast_to(
        real_return * asset_grid[None, :] + transfer + profits, (state_count, asset_count)
    ).copy()

    # Zero-drift policy (depends only on aggregate inputs; solved once).
    c0, n0, zero_feasible = zero_drift_policy(
        q, b, gamma=gamma, frisch=frisch, chi=chi, n_max=n_max, consumption_floor=consumption_floor
    )
    if not np.all(zero_feasible):
        raise HankHouseholdFeasibilityError(
            "BLOCKED_DLH_3B_HOUSEHOLD_FEASIBILITY: no feasible positive-consumption "
            "zero-drift policy exists at some state/node for the given aggregate inputs."
        )

    value = (utility(c0, gamma=gamma) - labor_disutility(n0, chi=chi, frisch=frisch)) / rho_hh
    identity = sparse.eye(value.size, format="csr", dtype=np.float64)
    residual_history: list[float] = []
    converged = False
    consumption = c0
    labor = n0
    drift = q * n0 + b - c0
    choice = np.zeros(q.shape, dtype=np.int64)
    selected_marginal = marginal_utility(c0, gamma=gamma)
    generator = _build_generator(drift, state_generator, spacing)
    iteration = 0

    for iteration in range(1, max_iterations + 1):
        consumption, labor, drift, choice, selected_marginal = _policy_from_value(
            value,
            asset_grid=asset_grid,
            q=q,
            b=b,
            c0=c0,
            n0=n0,
            zero_feasible=zero_feasible,
            gamma=gamma,
            frisch=frisch,
            chi=chi,
            n_max=n_max,
            consumption_floor=consumption_floor,
        )
        generator = _build_generator(drift, state_generator, spacing)
        matrix = (rho_hh + 1.0 / pseudo_time_step) * identity - generator
        rhs = (
            utility(consumption, gamma=gamma).ravel()
            - labor_disutility(labor, chi=chi, frisch=frisch).ravel()
            + value.ravel() / pseudo_time_step
        )
        value = np.asarray(spsolve(matrix, rhs), dtype=np.float64).reshape(value.shape)

        consumption, labor, drift, choice, selected_marginal = _policy_from_value(
            value,
            asset_grid=asset_grid,
            q=q,
            b=b,
            c0=c0,
            n0=n0,
            zero_feasible=zero_feasible,
            gamma=gamma,
            frisch=frisch,
            chi=chi,
            n_max=n_max,
            consumption_floor=consumption_floor,
        )
        final_generator = _build_generator(drift, state_generator, spacing)
        residual = rho_hh * value.ravel() - (
            utility(consumption, gamma=gamma).ravel()
            - labor_disutility(labor, chi=chi, frisch=frisch).ravel()
            + final_generator @ value.ravel()
        )
        true_residual = float(np.max(np.abs(residual)))
        residual_history.append(true_residual)
        if true_residual <= tolerance:
            converged = True
            break

    labor_kkt_max, consumption_foc_max = _kkt_diagnostics(
        q, labor, selected_marginal, consumption, chi=chi, frisch=frisch, n_max=n_max, gamma=gamma
    )
    row_sums = np.asarray(final_generator.sum(axis=1)).ravel()
    generator_row_sum_max_abs = float(np.max(np.abs(row_sums)))
    off_diagonal = final_generator - sparse.diags(
        final_generator.diagonal(), format="csr", dtype=np.float64
    )
    stored_min_off_diagonal = float(np.min(off_diagonal.data)) if off_diagonal.nnz else 0.0
    generator_min_off_diagonal = min(stored_min_off_diagonal, 0.0)
    generator_min_positive_off_diagonal = stored_min_off_diagonal
    nan_inf_count = int(
        np.count_nonzero(~np.isfinite(value))
        + np.count_nonzero(~np.isfinite(consumption))
        + np.count_nonzero(~np.isfinite(labor))
        + np.count_nonzero(~np.isfinite(drift))
        + np.count_nonzero(~np.isfinite(final_generator.data))
    )
    return HankHouseholdSolution(
        value=value,
        consumption=consumption,
        labor=labor,
        drift=drift,
        policy_choice=choice,
        generator=final_generator,
        converged=converged,
        iterations=iteration,
        true_residual=true_residual,
        min_consumption=float(np.min(consumption)),
        lower_boundary_min_drift=float(np.min(drift[:, 0])),
        upper_boundary_max_drift=float(np.max(drift[:, -1])),
        generator_row_sum_max_abs=generator_row_sum_max_abs,
        generator_min_off_diagonal=generator_min_off_diagonal,
        generator_min_positive_off_diagonal=generator_min_positive_off_diagonal,
        labor_kkt_max=labor_kkt_max,
        consumption_foc_max=consumption_foc_max,
        nan_inf_count=nan_inf_count,
        residual_history=tuple(residual_history),
    )
