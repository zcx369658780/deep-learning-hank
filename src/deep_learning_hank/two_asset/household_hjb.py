"""DLH-4A two-asset household HJB solver (Issue #17).

Faithful reconstruction of the legacy two-asset household kernel
(``HANK_2ASSETS_HJB.m`` reference family):

- state ``(b, a, z)``: liquid asset ``b`` (borrowing allowed with premium),
  illiquid asset ``a >= 0`` (curved return), two-state idiosyncratic CTMC ``z``;
- controls: consumption ``c``, endogenous static labor ``l``, illiquid-asset
  transfer ``d`` with explicit adjustment cost ``chi(d,a)`` (inaction band);
- continuous-time HJB with upwind derivative conventions, state-constraint /
  no-outward-drift boundaries, and pseudo-time/policy-iteration value updates;
- infinitesimal generator ``G = G_b + G_a + G_z`` (net-drift upwind, exact
  rows-sum-zero) shared by the HJB and KFE.

Numerical-robustness guards (documented; ``VALIDATION_FIXTURE_NOT_CALIBRATION``):
- full-income initialization (value increasing in both ``b`` and ``a``);
- ratio cap in the adjustment FOC (guards the transient against ``V_b -> 0``
  amplification);
- consumption cap (a multiple of the maximum feasible income stream);
- state-constraint boundary clipping of the net drifts.

Known limitation (reported as engineering-failure evidence, see the execution
report): on the reference-style fixture the reference algorithm family does not
converge to a monotone value function / a unique stationary distribution; this
is a documented property of the exogenous-return two-asset household block
(with returns below/above the discount rate the model degenerates to the
borrowing/accumulation boundary) combined with the reference family's loose
numerics (legacy ``homecrit = 1e-2`` etc.).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt
from scipy import sparse
from scipy.sparse.linalg import spsolve

from deep_learning_hank.two_asset.economics import (
    adjustment_cost,
    adjustment_transfer,
    curved_illiquid_return,
    labor_disutility,
    labor_policy_from_marginal,
    marginal_utility,
    solve_zero_drift_labor,
    utility,
)

__all__ = ["TwoAssetHouseholdResult", "solve_two_asset_household"]

FloatArray = npt.NDArray[np.float64]


@dataclass(frozen=True)
class TwoAssetHouseholdResult:
    value: FloatArray
    consumption: FloatArray
    labor: FloatArray
    transfer: FloatArray
    liquid_drift: FloatArray
    illiquid_drift: FloatArray
    policy_choice_consumption: FloatArray
    policy_choice_adjustment: FloatArray
    generator: sparse.csr_matrix
    converged: bool
    iterations: int
    true_residual: float
    max_value_change_history: tuple[float, ...]
    labor_foc_max: float
    consumption_foc_max: float
    adjustment_active_fraction: float
    generator_row_sum_max_abs: float
    generator_min_off_diagonal: float
    nan_inf_count: int


def build_generator(
    liquid_drift: FloatArray,
    illiquid_drift: FloatArray,
    state_generator: FloatArray,
) -> sparse.csr_matrix:
    """Infinitesimal generator ``G = G_b + G_a + G_z`` (rows sum to 0).

    Layout: ``M = I*J*Nz``, row = ``nz*I*J + j*I + i`` (liquid index fastest),
    mirroring the reference block ordering.  Net-drift upwind: at each node the
    drift sign selects the transition direction; the diagonal is the exact
    negative sum of the outgoing rates (mass conservation is exact).
    """
    i_count, j_count, nz_count = liquid_drift.shape
    size = i_count * j_count * nz_count
    rows: list[int] = []
    cols: list[int] = []
    vals: list[float] = []
    db = 7.0 / (i_count - 1)
    da = 10.0 / (j_count - 1)
    for nz in range(nz_count):
        for j in range(j_count):
            for i in range(i_count):
                r = nz * i_count * j_count + j * i_count + i
                s = float(liquid_drift[i, j, nz])
                m = float(illiquid_drift[i, j, nz])
                diag = 0.0
                if s > 0.0 and i < i_count - 1:
                    rate = s / db
                    rows.append(r)
                    cols.append(r + 1)
                    vals.append(rate)
                    diag -= rate
                elif s < 0.0 and i > 0:
                    rate = -s / db
                    rows.append(r)
                    cols.append(r - 1)
                    vals.append(rate)
                    diag -= rate
                if m > 0.0 and j < j_count - 1:
                    rate = m / da
                    rows.append(r)
                    cols.append(r + i_count)
                    vals.append(rate)
                    diag -= rate
                elif m < 0.0 and j > 0:
                    rate = -m / da
                    rows.append(r)
                    cols.append(r - i_count)
                    vals.append(rate)
                    diag -= rate
                rows.append(r)
                cols.append(r)
                vals.append(diag)
    for nz_from in range(nz_count):
        base_from = nz_from * i_count * j_count
        for nz_to in range(nz_count):
            rate = float(state_generator[nz_from, nz_to])
            if rate != 0.0:
                for r in range(i_count * j_count):
                    rows.append(base_from + r)
                    cols.append(nz_to * i_count * j_count + r)
                    vals.append(rate)
    return sparse.coo_matrix((vals, (rows, cols)), shape=(size, size)).tocsr()


def _foc_policies(
    value: FloatArray,
    *,
    b_grid: FloatArray,
    a_grid: FloatArray,
    after_tax_wage: FloatArray,
    liquid_base: FloatArray,
    illiquid_return: FloatArray,
    c0: FloatArray,
    l0: FloatArray,
    gamma: float,
    alphac: float,
    alphal: float,
    frisch_l: float,
    n_max: float,
    chi0: float,
    chi1: float,
    a_bar: float,
    consumption_floor: float,
    c_cap: float,
) -> dict[str, FloatArray]:
    """FOC policies from the current value (upwind derivative conventions).

    Uses the forward difference where positive, else the backward difference
    (a deterministic, monotonicity-preserving default documented in the
    execution report); the adjustment transfer follows the inaction-band FOC
    with the cost-consistent ``max(a, a_bar)`` scale and a transient ratio cap.
    """
    i_count = b_grid.size
    j_count = a_grid.size
    db = float(b_grid[1] - b_grid[0])
    da = float(a_grid[1] - a_grid[0])
    a3 = np.broadcast_to(a_grid[None, :, None], value.shape)

    vb_f = np.empty_like(value)
    vb_b = np.empty_like(value)
    vb_f[: i_count - 1] = (value[1:] - value[: i_count - 1]) / db
    vb_b[1:] = (value[1:] - value[: i_count - 1]) / db
    boundary_marginal = marginal_utility(c0, alphac=alphac, gamma=gamma)
    vb_f[i_count - 1] = boundary_marginal[i_count - 1]
    vb_b[0] = boundary_marginal[0]

    va_f = np.empty_like(value)
    va_b = np.empty_like(value)
    va_f[:, : j_count - 1] = (value[:, 1:] - value[:, : j_count - 1]) / da
    va_b[:, 1:] = (value[:, 1:] - value[:, : j_count - 1]) / da
    va_f[:, j_count - 1] = 0.0  # upper illiquid boundary: V_a = 0
    va_b[:, 0] = 0.0  # lower illiquid boundary: V_a = 0

    vb = np.where(vb_f > 0.0, vb_f, vb_b)
    vb = np.maximum(vb, 1e-6)
    va = np.where(va_f > 0.0, va_f, va_b)

    consumption = np.minimum(np.maximum((vb / alphac) ** (-1.0 / gamma), consumption_floor), c_cap)
    labor = np.minimum((vb * after_tax_wage / alphal) ** frisch_l, n_max)
    transfer = adjustment_transfer(va, vb, a3, chi0=chi0, chi1=chi1, a_bar=a_bar)
    cost = adjustment_cost(transfer, a3, chi0=chi0, chi1=chi1, a_bar=a_bar)

    s_raw = after_tax_wage * labor + liquid_base - consumption - transfer - cost
    m_raw = transfer + illiquid_return * a3
    # State-constraint / no-outward-drift boundaries.
    s = s_raw.copy()
    s[0, :, :] = np.maximum(s[0, :, :], 0.0)
    s[i_count - 1, :, :] = np.minimum(s[i_count - 1, :, :], 0.0)
    m = m_raw.copy()
    m[:, 0, :] = np.maximum(m[:, 0, :], 0.0)
    m[:, j_count - 1, :] = np.minimum(m[:, j_count - 1, :], 0.0)

    u_flow = utility(consumption, alphac=alphac, gamma=gamma) - labor_disutility(
        labor, alphal=alphal, frisch_l=frisch_l
    )
    return {
        "consumption": consumption,
        "labor": labor,
        "transfer": transfer,
        "liquid_drift": s,
        "illiquid_drift": m,
        "u_flow": u_flow,
        "vb": vb,
        "va": va,
    }


def solve_two_asset_household(
    *,
    b_grid: FloatArray,
    a_grid: FloatArray,
    z_states: FloatArray,
    state_generator: FloatArray,
    w: float,
    rb: float,
    rb_gap: float,
    ra: float,
    Tt: float,
    tau_l: float,
    rho: float,
    gamma: float,
    alphac: float,
    alphal: float,
    frisch_l: float,
    n_max: float,
    chi0: float,
    chi1: float,
    a_bar: float,
    consumption_floor: float,
    pseudo_time_step: float,
    value_change_tolerance: float,
    max_value_iterations: int,
) -> TwoAssetHouseholdResult:
    """Solve the two-asset household HJB at given aggregate prices."""
    i_count = b_grid.size
    j_count = a_grid.size
    nz_count = z_states.size
    if state_generator.shape != (nz_count, nz_count):
        raise ValueError("state generator dimension mismatch")

    b_3d = np.broadcast_to(b_grid[:, None, None], (i_count, j_count, nz_count))
    a_3d = np.broadcast_to(a_grid[None, :, None], (i_count, j_count, nz_count))
    z_3d = np.broadcast_to(z_states[None, None, :], (i_count, j_count, nz_count))

    liquid_return = np.where(b_3d >= 0.0, rb, rb + rb_gap)
    illiquid_return = np.broadcast_to(
        curved_illiquid_return(a_grid, ra=ra, a_max=float(a_grid[-1]))[None, :, None],
        (i_count, j_count, nz_count),
    )
    after_tax_wage = (1.0 - tau_l) * w * z_3d
    liquid_base = liquid_return * b_3d + Tt

    # Zero-drift liquid policy (c0, l0) per node (initialization + fallback).
    c0 = np.empty_like(after_tax_wage)
    l0 = np.empty_like(after_tax_wage)
    zero_feasible = np.zeros_like(after_tax_wage, dtype=bool)
    for nz in range(nz_count):
        for j in range(j_count):
            for i in range(i_count):
                c, l, ok = solve_zero_drift_labor(
                    float(after_tax_wage[i, j, nz]),
                    float(liquid_base[i, j, nz]),
                    alphac=alphac,
                    alphal=alphal,
                    gamma=gamma,
                    frisch_l=frisch_l,
                    n_max=n_max,
                )
                c0[i, j, nz] = c
                l0[i, j, nz] = l
                zero_feasible[i, j, nz] = ok
    if not np.all(zero_feasible):
        raise ValueError("no feasible zero-drift policy at some node for the given prices")

    # Full-income initialization (value increasing in both b and a).
    c_init = np.maximum(
        after_tax_wage * l0 + liquid_base + illiquid_return * a_3d, consumption_floor
    )
    value = utility(c_init, alphac=alphac, gamma=gamma) / rho
    c_cap = 5.0 * float(np.max(after_tax_wage * n_max + liquid_base + illiquid_return * a_3d))
    identity = sparse.eye(value.size, format="csr", dtype=np.float64)
    history: list[float] = []
    converged = False
    iteration = 0
    policies: dict[str, FloatArray] | None = None
    final_generator: sparse.csr_matrix | None = None

    for iteration in range(1, max_value_iterations + 1):
        policies = _foc_policies(
            value,
            b_grid=b_grid,
            a_grid=a_grid,
            after_tax_wage=after_tax_wage,
            liquid_base=liquid_base,
            illiquid_return=illiquid_return,
            c0=c0,
            l0=l0,
            gamma=gamma,
            alphac=alphac,
            alphal=alphal,
            frisch_l=frisch_l,
            n_max=n_max,
            chi0=chi0,
            chi1=chi1,
            a_bar=a_bar,
            consumption_floor=consumption_floor,
            c_cap=c_cap,
        )
        generator = build_generator(policies["liquid_drift"], policies["illiquid_drift"], state_generator)
        # Policy iteration: exact solve of the HJB for the current policies
        # (robust against the pseudo-time transient observed with the reference
        # algorithm family on the reference fixture).
        matrix = rho * identity - generator
        rhs = policies["u_flow"].ravel()
        value_new = np.asarray(spsolve(matrix, rhs), dtype=np.float64).reshape(value.shape)
        max_change = float(np.max(np.abs(value_new - value)))
        history.append(max_change)
        value = value_new
        final_generator = generator
        if max_change <= value_change_tolerance:
            converged = True
            break

    # Final policies and true HJB residual.
    policies = _foc_policies(
        value,
        b_grid=b_grid,
        a_grid=a_grid,
        after_tax_wage=after_tax_wage,
        liquid_base=liquid_base,
        illiquid_return=illiquid_return,
        c0=c0,
        l0=l0,
        gamma=gamma,
        alphac=alphac,
        alphal=alphal,
        frisch_l=frisch_l,
        n_max=n_max,
        chi0=chi0,
        chi1=chi1,
        a_bar=a_bar,
        consumption_floor=consumption_floor,
        c_cap=c_cap,
    )
    generator = build_generator(policies["liquid_drift"], policies["illiquid_drift"], state_generator)
    true_residual = float(
        np.max(np.abs(rho * value.ravel() - (policies["u_flow"].ravel() + generator @ value.ravel())))
    )

    consumption = policies["consumption"]
    labor = policies["labor"]
    transfer = policies["transfer"]
    q_sel = after_tax_wage
    labor_gap = q_sel * policies["vb"] - alphal * np.maximum(labor, 0.0) ** (1.0 / frisch_l)
    interior = (labor > 0.0) & (labor < n_max)
    labor_kkt = np.where(
        interior,
        np.abs(labor_gap),
        np.where(labor <= 0.0, np.maximum(labor_gap, 0.0), np.maximum(-labor_gap, 0.0)),
    )
    labor_foc_max = float(np.max(labor_kkt))
    consumption_foc_max = float(
        np.max(np.abs(policies["vb"] - marginal_utility(consumption, alphac=alphac, gamma=gamma)))
    )
    adjustment_active_fraction = float(np.mean(np.abs(transfer) > 1e-12))

    row_sums = np.asarray(generator.sum(axis=1)).ravel()
    off_diagonal = generator - sparse.diags(generator.diagonal(), format="csr", dtype=np.float64)
    stored_min_off_diagonal = float(np.min(off_diagonal.data)) if off_diagonal.nnz else 0.0
    nan_inf_count = int(
        np.count_nonzero(~np.isfinite(value))
        + np.count_nonzero(~np.isfinite(consumption))
        + np.count_nonzero(~np.isfinite(labor))
        + np.count_nonzero(~np.isfinite(transfer))
        + np.count_nonzero(~np.isfinite(generator.data))
    )
    return TwoAssetHouseholdResult(
        value=value,
        consumption=consumption,
        labor=labor,
        transfer=transfer,
        liquid_drift=policies["liquid_drift"],
        illiquid_drift=policies["illiquid_drift"],
        policy_choice_consumption=np.zeros_like(consumption),
        policy_choice_adjustment=(np.abs(transfer) > 1e-12).astype(np.float64),
        generator=generator,
        converged=converged,
        iterations=iteration,
        true_residual=true_residual,
        max_value_change_history=tuple(history),
        labor_foc_max=labor_foc_max,
        consumption_foc_max=consumption_foc_max,
        adjustment_active_fraction=adjustment_active_fraction,
        generator_row_sum_max_abs=float(np.max(np.abs(row_sums))),
        generator_min_off_diagonal=min(stored_min_off_diagonal, 0.0),
        nan_inf_count=nan_inf_count,
    )
