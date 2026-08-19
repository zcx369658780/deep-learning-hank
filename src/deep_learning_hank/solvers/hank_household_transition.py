"""DLH-3C time-dependent household backward HJB solver (isolated module).

Implements Issue #12 §6: implicit backward stepping of the continuous-time
household HJB

    rho V_t - partial_t V_t = max_{c,n}{ u(c)-v(n) + G(c,n; w_t,r_t,tr_t,Pi_t) V_t }

with terminal condition ``V(T) = V_ss`` from the accepted DLH-3B steady state
and the frozen discrete step

    [(rho + 1/dt) I - G_k] V_k = u_k - v_k + V_{k+1}/dt .

Within each time step the HJB is solved by policy iteration using **the same
state-constraint / upwind / zero-drift / endogenous-static-labor semantics as
the accepted DLH-3B household kernel** (read-only reuse of its helpers; no
modification of the accepted module).  The household HJB itself is not
linearized.

The prescribed real price/income paths are
``EXOGENOUS_NUMERICAL_RESPONSE_PATH_NOT_STRUCTURAL_SHOCK``; they are not
structural shocks and this module implements no monetary policy innovation,
no NKPC/inflation feedback and no aggregate market clearing.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt
from scipy import sparse
from scipy.sparse.linalg import spsolve

from deep_learning_hank.economics.preferences import utility
from deep_learning_hank.solvers.hank_household_steady_state import (
    HankHouseholdFeasibilityError,
    _build_generator,  # accepted kernel generator semantics (read-only reuse)
    _kkt_diagnostics,  # accepted labor-KKT / consumption-FOC semantics (read-only reuse)
    _policy_from_value,  # accepted upwind/zero-drift policy semantics (read-only reuse)
    labor_disutility,
    zero_drift_policy,
)

__all__ = [
    "DynamicHouseholdStep",
    "DynamicHouseholdSolution",
    "solve_dynamic_household",
]

FloatArray = npt.NDArray[np.float64]


@dataclass(frozen=True)
class TransitionInputs:
    """Prescribed real household-relevant inputs at one time point."""

    wage: float
    real_return: float
    transfer: float
    profits: float


@dataclass(frozen=True)
class DynamicHouseholdStep:
    k: int
    t: float
    value: FloatArray
    consumption: FloatArray
    labor: FloatArray
    drift: FloatArray
    policy_choice: FloatArray
    generator: sparse.csr_matrix
    hjb_residual: float
    min_consumption: float
    lower_boundary_min_drift: float
    upper_boundary_max_drift: float
    generator_row_sum_max_abs: float
    generator_min_off_diagonal: float
    labor_kkt_max: float
    consumption_foc_max: float
    nan_inf_count: int
    iterations: int
    converged: bool


@dataclass(frozen=True)
class DynamicHouseholdSolution:
    time_grid: FloatArray
    inputs: tuple[TransitionInputs, ...]
    steps: tuple[DynamicHouseholdStep, ...]
    converged_all: bool
    value_path: FloatArray
    consumption_path: FloatArray
    labor_path: FloatArray
    drift_path: FloatArray
    generator_path: tuple[sparse.csr_matrix, ...]
    hjb_residual_max: float
    labor_kkt_max: float
    consumption_foc_max: float


def _within_step_solve(
    value_next: FloatArray,
    inputs: TransitionInputs,
    *,
    asset_grid: FloatArray,
    efficiency_states: FloatArray,
    state_generator: FloatArray,
    tau_l: float,
    rho_hh: float,
    gamma: float,
    frisch: float,
    chi: float,
    n_max: float,
    consumption_floor: float,
    dt: float,
    value_tolerance: float,
    max_policy_iterations: int,
) -> tuple[FloatArray, DynamicHouseholdStep, int]:
    """Policy-iterate the frozen within-step HJB equation at one time point."""
    state_count = efficiency_states.size
    asset_count = asset_grid.size
    spacing = float(asset_grid[1] - asset_grid[0])
    q = np.broadcast_to(
        (1.0 - tau_l) * inputs.wage * efficiency_states[:, None], (state_count, asset_count)
    ).copy()
    b = np.broadcast_to(
        inputs.real_return * asset_grid[None, :] + inputs.transfer + inputs.profits,
        (state_count, asset_count),
    ).copy()
    c0, n0, zero_feasible = zero_drift_policy(
        q, b, gamma=gamma, frisch=frisch, chi=chi, n_max=n_max, consumption_floor=consumption_floor
    )
    if not np.all(zero_feasible):
        raise HankHouseholdFeasibilityError(
            "BLOCKED_DLH_3C_BACKWARD_HJB_GATE: no feasible positive-consumption "
            "zero-drift policy at a time step for the prescribed inputs."
        )
    identity = sparse.eye(value_next.size, format="csr", dtype=np.float64)
    inverse_dt = 1.0 / dt
    value = np.asarray(value_next, dtype=np.float64).copy()
    converged = False
    iterations = 0
    final_step: DynamicHouseholdStep | None = None
    for iteration in range(1, max_policy_iterations + 1):
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
        matrix = (rho_hh + inverse_dt) * identity - generator
        rhs = (
            utility(consumption, gamma=gamma).ravel()
            - labor_disutility(labor, chi=chi, frisch=frisch).ravel()
            + value_next.ravel() * inverse_dt
        )
        value_new = np.asarray(spsolve(matrix, rhs), dtype=np.float64).reshape(value.shape)
        value_change = float(np.max(np.abs(value_new - value)))
        value = value_new
        iterations = iteration
        if value_change <= value_tolerance:
            converged = True
            break
    # Final policy + diagnostics with the converged value.
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
    hjb_residual = float(
        np.max(
            np.abs(
                (rho_hh + inverse_dt) * value.ravel()
                - generator @ value.ravel()
                - (
                    utility(consumption, gamma=gamma).ravel()
                    - labor_disutility(labor, chi=chi, frisch=frisch).ravel()
                    + value_next.ravel() * inverse_dt
                )
            )
        )
    )
    labor_kkt_max, consumption_foc_max = _kkt_diagnostics(
        q, labor, selected_marginal, consumption, chi=chi, frisch=frisch, n_max=n_max, gamma=gamma
    )
    row_sums = np.asarray(generator.sum(axis=1)).ravel()
    off_diagonal = generator - sparse.diags(generator.diagonal(), format="csr", dtype=np.float64)
    stored_min_off_diagonal = float(np.min(off_diagonal.data)) if off_diagonal.nnz else 0.0
    nan_inf_count = int(
        np.count_nonzero(~np.isfinite(value))
        + np.count_nonzero(~np.isfinite(consumption))
        + np.count_nonzero(~np.isfinite(labor))
        + np.count_nonzero(~np.isfinite(drift))
        + np.count_nonzero(~np.isfinite(generator.data))
    )
    final_step = DynamicHouseholdStep(
        k=-1,
        t=float("nan"),
        value=value,
        consumption=consumption,
        labor=labor,
        drift=drift,
        policy_choice=choice,
        generator=generator,
        hjb_residual=hjb_residual,
        min_consumption=float(np.min(consumption)),
        lower_boundary_min_drift=float(np.min(drift[:, 0])),
        upper_boundary_max_drift=float(np.max(drift[:, -1])),
        generator_row_sum_max_abs=float(np.max(np.abs(row_sums))),
        generator_min_off_diagonal=min(stored_min_off_diagonal, 0.0),
        labor_kkt_max=labor_kkt_max,
        consumption_foc_max=consumption_foc_max,
        nan_inf_count=nan_inf_count,
        iterations=iterations,
        converged=converged,
    )
    return value, final_step, iterations


def solve_dynamic_household(
    *,
    asset_grid: FloatArray,
    efficiency_states: FloatArray,
    state_generator: FloatArray,
    inputs_path: tuple[TransitionInputs, ...],
    terminal_value: FloatArray,
    tau_l: float,
    rho_hh: float,
    gamma: float,
    frisch: float,
    chi: float,
    n_max: float,
    consumption_floor: float,
    dt: float,
    value_tolerance: float,
    max_policy_iterations: int,
) -> DynamicHouseholdSolution:
    """Backward implicit HJB along the prescribed input path.

    ``inputs_path`` has ``N+1`` entries for ``k = 0..N`` (``N = len-1``);
    ``terminal_value`` is ``V(T) = V_ss``.  Returns the value/policy at every
    time point ``k = 0..N`` (the terminal point is stored without a solve).
    """
    if asset_grid.ndim != 1 or efficiency_states.ndim != 1:
        raise ValueError("household state grids must be one-dimensional")
    if state_generator.shape != (efficiency_states.size, efficiency_states.size):
        raise ValueError("idiosyncratic generator dimensions do not match")
    if not np.allclose(state_generator.sum(axis=1), 0.0, atol=1e-12):
        raise ValueError("state_generator must be a CTMC generator / intensity matrix (rows sum 0)")
    n_points = len(inputs_path)
    if n_points < 2:
        raise ValueError("inputs_path must cover at least two time points")
    spacing_values = np.diff(asset_grid)
    if np.any(spacing_values <= 0.0) or not np.allclose(spacing_values, spacing_values[0]):
        raise ValueError("the HJB uses a uniform increasing asset grid")
    time_grid = dt * np.arange(n_points, dtype=np.float64)
    steps: list[DynamicHouseholdStep] = []
    value_next = np.asarray(terminal_value, dtype=np.float64).copy()
    for k in range(n_points - 1, -1, -1):
        if k == n_points - 1:
            # Terminal point: no within-step solve; policy from the terminal value
            # under the terminal inputs is recorded for completeness.
            inputs = inputs_path[k]
            state_count = efficiency_states.size
            asset_count = asset_grid.size
            q = np.broadcast_to(
                (1.0 - tau_l) * inputs.wage * efficiency_states[:, None],
                (state_count, asset_count),
            ).copy()
            b = np.broadcast_to(
                inputs.real_return * asset_grid[None, :] + inputs.transfer + inputs.profits,
                (state_count, asset_count),
            ).copy()
            c0, n0, zero_feasible = zero_drift_policy(
                q, b, gamma=gamma, frisch=frisch, chi=chi, n_max=n_max,
                consumption_floor=consumption_floor,
            )
            if not np.all(zero_feasible):
                raise HankHouseholdFeasibilityError(
                    "BLOCKED_DLH_3C_BACKWARD_HJB_GATE: terminal inputs infeasible."
                )
            consumption, labor, drift, choice, selected_marginal = _policy_from_value(
                value_next, asset_grid=asset_grid, q=q, b=b, c0=c0, n0=n0,
                zero_feasible=zero_feasible, gamma=gamma, frisch=frisch, chi=chi,
                n_max=n_max, consumption_floor=consumption_floor,
            )
            generator = _build_generator(drift, state_generator, float(spacing_values[0]))
            labor_kkt_max, consumption_foc_max = _kkt_diagnostics(
                q, labor, selected_marginal, consumption, chi=chi, frisch=frisch, n_max=n_max,
                gamma=gamma,
            )
            row_sums = np.asarray(generator.sum(axis=1)).ravel()
            off_diagonal = generator - sparse.diags(
                generator.diagonal(), format="csr", dtype=np.float64
            )
            stored_min_off_diagonal = (
                float(np.min(off_diagonal.data)) if off_diagonal.nnz else 0.0
            )
            nan_inf_count = int(
                np.count_nonzero(~np.isfinite(value_next))
                + np.count_nonzero(~np.isfinite(consumption))
                + np.count_nonzero(~np.isfinite(labor))
                + np.count_nonzero(~np.isfinite(drift))
            )
            steps.append(
                DynamicHouseholdStep(
                    k=k, t=float(time_grid[k]), value=value_next, consumption=consumption,
                    labor=labor, drift=drift, policy_choice=choice, generator=generator,
                    hjb_residual=0.0, min_consumption=float(np.min(consumption)),
                    lower_boundary_min_drift=float(np.min(drift[:, 0])),
                    upper_boundary_max_drift=float(np.max(drift[:, -1])),
                    generator_row_sum_max_abs=float(np.max(np.abs(row_sums))),
                    generator_min_off_diagonal=min(stored_min_off_diagonal, 0.0),
                    labor_kkt_max=labor_kkt_max, consumption_foc_max=consumption_foc_max,
                    nan_inf_count=nan_inf_count, iterations=0, converged=True,
                )
            )
        else:
            value_next, step, _iterations = _within_step_solve(
                value_next,
                inputs_path[k],
                asset_grid=asset_grid,
                efficiency_states=efficiency_states,
                state_generator=state_generator,
                tau_l=tau_l,
                rho_hh=rho_hh,
                gamma=gamma,
                frisch=frisch,
                chi=chi,
                n_max=n_max,
                consumption_floor=consumption_floor,
                dt=dt,
                value_tolerance=value_tolerance,
                max_policy_iterations=max_policy_iterations,
            )
            steps.append(
                DynamicHouseholdStep(
                    k=k, t=float(time_grid[k]), value=step.value, consumption=step.consumption,
                    labor=step.labor, drift=step.drift, policy_choice=step.policy_choice,
                    generator=step.generator, hjb_residual=step.hjb_residual,
                    min_consumption=step.min_consumption,
                    lower_boundary_min_drift=step.lower_boundary_min_drift,
                    upper_boundary_max_drift=step.upper_boundary_max_drift,
                    generator_row_sum_max_abs=step.generator_row_sum_max_abs,
                    generator_min_off_diagonal=step.generator_min_off_diagonal,
                    labor_kkt_max=step.labor_kkt_max,
                    consumption_foc_max=step.consumption_foc_max,
                    nan_inf_count=step.nan_inf_count,
                    iterations=step.iterations,
                    converged=step.converged,
                )
            )
    steps_by_k = sorted(steps, key=lambda s: s.k)
    value_path = np.stack([s.value for s in steps_by_k])
    consumption_path = np.stack([s.consumption for s in steps_by_k])
    labor_path = np.stack([s.labor for s in steps_by_k])
    drift_path = np.stack([s.drift for s in steps_by_k])
    generator_path = tuple(s.generator for s in steps_by_k)
    converged_all = bool(all(s.converged for s in steps_by_k))
    hjb_residual_max = float(max(s.hjb_residual for s in steps_by_k))
    labor_kkt_max = float(max(s.labor_kkt_max for s in steps_by_k))
    consumption_foc_max = float(max(s.consumption_foc_max for s in steps_by_k))
    return DynamicHouseholdSolution(
        time_grid=time_grid,
        inputs=tuple(inputs_path),
        steps=tuple(steps_by_k),
        converged_all=converged_all,
        value_path=value_path,
        consumption_path=consumption_path,
        labor_path=labor_path,
        drift_path=drift_path,
        generator_path=generator_path,
        hjb_residual_max=hjb_residual_max,
        labor_kkt_max=labor_kkt_max,
        consumption_foc_max=consumption_foc_max,
    )
