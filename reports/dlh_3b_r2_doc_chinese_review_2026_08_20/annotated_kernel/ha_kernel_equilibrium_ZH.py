# -*- coding: utf-8 -*-
"""
DLH-3B-R2-DOC — 中文注释评审副本（REVIEW COPY / 仅供人工审阅，不参与导入执行）
================================================================================

本文件是 Issue #15 内核模块 `src/deep_learning_hank/ha_kernel/equilibrium.py`
（commit 750e5a2f508f3d3ebfcaa517271c29d3093d90f4）的**逐字行为等价评审副本**：

- 所有可执行语句与原模块完全一致（行为不变，Issue #16 §3）；
- 仅新增中文注释；
- 本文件位于 `reports/` 下，**不会被导入、不会被 pytest 收集**，仅作文档。

对应经济学契约：`DLH_3B_R2_IMPLEMENTATION_REVIEW.md` §1.3-§1.5 / §6。
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
    """找不到有限异号 bracket 时抛出（确定性根求解，不允许调参制造 bracket）。"""


@dataclass(frozen=True)
class KernelEquilibriumEvaluation:
    """一次完整均衡评估（候选 (r, N) 下的一切对象与残差）。

    - r: 实际利率候选；N: 聚合有效劳动候选
    - output Y = Z*N; wage w = Z/μ; marginal_cost mc = 1/μ; markup μ = ε/(ε-1)
    - profits Π = Y - w*N（零通胀）; tax_revenue T = τ_l*w*N; transfer tr = T - r*B
    - A_hh = ∫a dg（聚合资产需求）; N_hh = ∫z n dg（聚合劳动供给）; C = ∫c dg
    - R_asset = A_hh - B（资产市场清算残差）
    - R_labor = N_hh - N（劳动市场清算残差）
    - R_goods / R_fiscal / R_profits / R_wealth：独立核算残差（计算而非标签归零）
    """

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
    """稳态均衡求解结果：根 r*, N* 与最终评估。"""

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
    """候选 (r, N) 处评估失败（家户不可行/异常）时的非有限记录（不参与 bracket 逻辑）。"""
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
    """在候选 (r, N) 处做完整确定性均衡评估。

    链条：生产/价格块 → 财政块 → 家户 HJB → 稳态 KFE → 聚合 → 清算残差。
    """
    try:
        # 生产/价格块（零通胀稳态）：Y = Z*N；μ = ε/(ε-1)；mc = 1/μ；w = Z*mc = Z/μ；Π = Y - w*N。
        z = config.productivity
        output = z * N
        markup = config.epsilon / (config.epsilon - 1.0)
        marginal_cost = 1.0 / markup
        wage = z * marginal_cost
        profits = output - wage * N
        # 财政块（恒定债券供给 B）：T = τ_l*w*N；tr = T - r*B - G（G=0）。
        tax_revenue = config.tau_l * wage * N
        transfer = tax_revenue - r * config.bond_supply - config.public_outlay

        asset_grid = build_asset_grid(config.a_min, config.a_max, config.asset_grid_count)
        efficiency_states = np.asarray(config.idiosyncratic_states, dtype=np.float64)
        state_generator = build_idiosyncratic_generator(config.q_low_to_high, config.q_high_to_low)
        # 家户块：以 (w, r, tr, Π) 为输入求解 HJB + KFE。
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
        # 聚合与清算残差。
        A_hh = distribution.mean_assets
        C = distribution.mean_consumption
        N_hh = float(np.sum(distribution.mass * efficiency_states[:, None] * household.labor))
        R_asset = float(A_hh - config.bond_supply)
        R_labor = float(N_hh - N)
        R_goods = float(output - C - 0.0)  # AC = (φ_p/2)π²Y = 0（π=0）
        R_fiscal = float(tax_revenue - r * config.bond_supply - config.public_outlay - transfer)
        R_profits = float(profits - (output - wage * N - 0.0))
        # 聚合财富流恒等式（稳态 Ȧ_hh = 0）：R_wealth = 0 - [(1-τ_l)wN_hh + rA_hh + tr + Π - C]。
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
    """有限两点是否异号（含零点）；非有限值不算异号。"""
    if not (np.isfinite(a) and np.isfinite(b)):
        return False
    if a == 0.0 or b == 0.0:
        return True
    return np.sign(a) != np.sign(b)


def _inner_labor_root(
    config: HankSteadyStateConfig, r: float
) -> tuple[float, tuple[float, float], bool]:
    """内层劳动根：固定 r，求 R_labor(N) = N_hh - N = 0（确定性 brentq）。

    bracket 选择：先用夹具主 bracket（labor_bracket=[0.20, 2.00]）；
    若主 bracket 无有限异号，做一次有界确定性扫描（labor_scan_bounds=[0.05, 4.00]）。
    """

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
    """外层资产残差：R_asset(r) = A_hh(r, N*(r)) - B（内层劳动根已解出）。"""
    try:
        n_star, _b, _f = _inner_labor_root(config, r)
    except NoKernelBracketError:
        return float("nan")
    evaluation = evaluate_kernel_equilibrium(config, r, n_star)
    return evaluation.R_asset if evaluation.finite else float("nan")


def solve_kernel_equilibrium(config: HankSteadyStateConfig) -> KernelEquilibriumResult:
    """求解稳态均衡：R_asset(r*) = 0（内层劳动根 N*(r)），确定性嵌套 brentq。

    均衡条件（Issue #16 要求文档化）：
    - 资产市场：A_hh = B（R_asset = A_hh - B = 0）；
    - 劳动市场：N_hh = N（R_labor = N_hh - N = 0）。
    """
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
