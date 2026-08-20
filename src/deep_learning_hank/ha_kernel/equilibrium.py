"""Canonical one-asset HANK steady-state equilibrium fixed point (DLH-3B-R2).

Implements the deterministic nested fixed point (``DLH_3B_R2_IMPLEMENTATION_
REVIEW.md`` §6):

- inner labor root: ``R_labor(N) = N_hh(r, N) - N = 0`` at fixed ``r``;
- outer asset root: ``R_asset(r) = A_hh(r, N*(r)) - B = 0``;
- each root uses its primary bracket first, else one bounded deterministic
  scan (frozen config brackets/scan); no parameter tuning to manufacture a
  bracket.

Deterministic: no random numbers; identical inputs produce identical outputs.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt
from scipy.optimize import brentq

from deep_learning_hank.economics.grids import (
    build_asset_grid,
    build_idiosyncratic_generator,
)
from deep_learning_hank.hank_config import HankSteadyStateConfig
from deep_learning_hank.ha_kernel.distribution import (
    KernelDistributionResult,
    solve_kernel_distribution,
)
from deep_learning_hank.ha_kernel.household import (
    HouseholdKernelResult,
    solve_kernel_household,
)

__all__ = [
    "KernelEquilibriumEvaluation",
    "KernelEquilibriumResult",
    "NoKernelBracketError",
    "evaluate_kernel_equilibrium",
    "solve_kernel_equilibrium",
]

FloatArray = npt.NDArray[np.float64]


class NoKernelBracketError(RuntimeError):
    """Raised when no finite sign-changing bracket is found for a kernel root."""


@dataclass(frozen=True)
class KernelEquilibriumEvaluation:
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
    R_goods: float
    R_fiscal: float
    R_profits: float
    R_wealth: float
    hjb_converged: bool
    hjb_true_residual: float
    household: HouseholdKernelResult | None
    distribution: KernelDistributionResult | None


@dataclass(frozen=True)
class KernelEquilibriumResult:
    config_sha256: str
    root_r: float
    root_N: float
    root_converged: bool
    outer_bracket_used: tuple[float, float]
    outer_bracket_from_scan: bool
    inner_bracket_used: tuple[float, float]
    inner_bracket_from_scan: bool
    final: KernelEquilibriumEvaluation


def _nonfinite(config: HankSteadyStateConfig, r: float, N: float) -> KernelEquilibriumEvaluation:
    return KernelEquilibriumEvaluation(
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
        R_goods=float("nan"),
        R_fiscal=float("nan"),
        R_profits=float("nan"),
        R_wealth=float("nan"),
        hjb_converged=False,
        hjb_true_residual=float("nan"),
        household=None,
        distribution=None,
    )


def evaluate_kernel_equilibrium(
    config: HankSteadyStateConfig, r: float, N: float
) -> KernelEquilibriumEvaluation:
    """Full deterministic kernel equilibrium evaluation at candidate ``(r, N)``."""
    try:
        z = config.productivity
        output = z * N
        markup = config.epsilon / (config.epsilon - 1.0)
        marginal_cost = 1.0 / markup
        wage = z * marginal_cost
        profits = output - wage * N
        tax_revenue = config.tau_l * wage * N
        transfer = tax_revenue - r * config.bond_supply - config.public_outlay

        asset_grid = build_asset_grid(config.a_min, config.a_max, config.asset_grid_count)
        efficiency_states = np.asarray(config.idiosyncratic_states, dtype=np.float64)
        state_generator = build_idiosyncratic_generator(config.q_low_to_high, config.q_high_to_low)
        household = solve_kernel_household(
            asset_grid=asset_grid,
            efficiency_states=efficiency_states,
            state_generator=state_generator,
            wage=wage,
            real_return=r,
            transfer=transfer,
            profits=profits,
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
        distribution = solve_kernel_distribution(
            generator=household.generator,
            asset_grid=asset_grid,
            consumption=household.consumption,
            mass_tolerance=config.numerical.kfe_mass_tolerance,
            negative_mass_threshold=config.numerical.negative_mass_threshold,
        )
        A_hh = distribution.mean_assets
        C = distribution.mean_consumption
        N_hh = float(np.sum(distribution.mass * efficiency_states[:, None] * household.labor))
        R_asset = float(A_hh - config.bond_supply)
        R_labor = float(N_hh - N)
        R_goods = float(output - C - 0.0)  # AC = 0 at pi = 0
        R_fiscal = float(tax_revenue - r * config.bond_supply - config.public_outlay - transfer)
        R_profits = float(profits - (output - wage * N - 0.0))
        R_wealth = float(
            0.0
            - (
                (1.0 - config.tau_l) * wage * N_hh
                + r * A_hh
                + transfer
                + profits
                - C
            )
        )
        return KernelEquilibriumEvaluation(
            r=float(r),
            N=float(N),
            finite=True,
            output=float(output),
            wage=float(wage),
            marginal_cost=float(marginal_cost),
            markup=float(markup),
            profits=float(profits),
            tax_revenue=float(tax_revenue),
            transfer=float(transfer),
            A_hh=float(A_hh),
            N_hh=float(N_hh),
            C=float(C),
            R_asset=float(R_asset),
            R_labor=float(R_labor),
            R_goods=float(R_goods),
            R_fiscal=float(R_fiscal),
            R_profits=float(R_profits),
            R_wealth=float(R_wealth),
            hjb_converged=household.converged,
            hjb_true_residual=household.true_residual,
            household=household,
            distribution=distribution,
        )
    except (ValueError, RuntimeError):
        return _nonfinite(config, r, N)


def _sign_change(a: float, b: float) -> bool:
    if not (np.isfinite(a) and np.isfinite(b)):
        return False
    if a == 0.0 or b == 0.0:
        return True
    return np.sign(a) != np.sign(b)


def _inner_labor_root(
    config: HankSteadyStateConfig, r: float
) -> tuple[float, tuple[float, float], bool]:
    def residual(N: float) -> float:
        return evaluate_kernel_equilibrium(config, r, N).R_labor

    primary = config.labor_bracket
    lo, hi = primary
    r_lo = residual(lo)
    r_hi = residual(hi)
    if _sign_change(r_lo, r_hi):
        bracket = (lo, hi)
        from_scan = False
    else:
        bracket = None
        from_scan = True
        previous_x = None
        previous_r = None
        for x in np.linspace(config.labor_scan_bounds[0], config.labor_scan_bounds[1], config.labor_scan_points):
            rx = residual(float(x))
            if previous_x is not None and _sign_change(previous_r, rx):
                bracket = (float(previous_x), float(x))
                break
            previous_x = float(x)
            previous_r = float(rx)
        if bracket is None:
            raise NoKernelBracketError(
                f"no finite sign-changing labor bracket at r={r!r} in primary bracket or scan"
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
        raise NoKernelBracketError(f"inner labor brentq did not converge at r={r!r}")
    return float(root), bracket, from_scan


def _outer_residual(config: HankSteadyStateConfig, r: float) -> float:
    try:
        n_star, _b, _f = _inner_labor_root(config, r)
    except NoKernelBracketError:
        return float("nan")
    evaluation = evaluate_kernel_equilibrium(config, r, n_star)
    return evaluation.R_asset if evaluation.finite else float("nan")


def solve_kernel_equilibrium(config: HankSteadyStateConfig) -> KernelEquilibriumResult:
    """Solve ``R_asset(r*) = 0`` with inner labor root ``N*(r)`` (deterministic)."""
    config.validate()

    def outer_residual(r: float) -> float:
        return _outer_residual(config, r)

    primary = config.asset_bracket
    lo, hi = primary
    r_lo = outer_residual(lo)
    r_hi = outer_residual(hi)
    if _sign_change(r_lo, r_hi):
        outer_bracket = (lo, hi)
        outer_from_scan = False
    else:
        outer_bracket = None
        outer_from_scan = True
        previous_x = None
        previous_r = None
        for x in np.linspace(config.asset_scan_bounds[0], config.asset_scan_bounds[1], config.asset_scan_points):
            rx = outer_residual(float(x))
            if previous_x is not None and _sign_change(previous_r, rx):
                outer_bracket = (float(previous_x), float(x))
                break
            previous_x = float(x)
            previous_r = float(rx)
        if outer_bracket is None:
            raise NoKernelBracketError(
                "no finite sign-changing asset bracket in primary bracket or scan"
            )

    root_r, info = brentq(
        outer_residual,
        outer_bracket[0],
        outer_bracket[1],
        xtol=config.numerical.root_xtol,
        rtol=config.numerical.root_xtol,
        maxiter=config.numerical.root_max_iterations,
        full_output=True,
        disp=False,
    )
    inner_root, inner_bracket, inner_from_scan = _inner_labor_root(config, float(root_r))
    final = evaluate_kernel_equilibrium(config, float(root_r), inner_root)
    return KernelEquilibriumResult(
        config_sha256=config.sha256(),
        root_r=float(root_r),
        root_N=inner_root,
        root_converged=bool(info.converged),
        outer_bracket_used=outer_bracket,
        outer_bracket_from_scan=outer_from_scan,
        inner_bracket_used=inner_bracket,
        inner_bracket_from_scan=inner_from_scan,
        final=final,
    )
