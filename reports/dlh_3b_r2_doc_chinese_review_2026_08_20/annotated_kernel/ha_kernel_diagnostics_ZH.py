# -*- coding: utf-8 -*-
"""
DLH-3B-R2-DOC — 中文注释评审副本（REVIEW COPY / 仅供人工审阅，不参与导入执行）
================================================================================

本文件是 Issue #15 内核模块 `src/deep_learning_hank/ha_kernel/diagnostics.py`
（commit 750e5a2f508f3d3ebfcaa517271c29d3093d90f4）的**逐字行为等价评审副本**：

- 所有可执行语句与原模块完全一致（行为不变，Issue #16 §3）；
- 仅新增中文注释；
- 本文件位于 `reports/` 下，**不会被导入、不会被 pytest 收集**，仅作文档。

对应经济学契约：`DLH_3B_R2_IMPLEMENTATION_REVIEW.md` §1.5 / §7；
诊断 ↔ 数学条件映射见 `DLH_3B_R2_DOC_SCIENTIFIC_MAPPING_ZH.md`。
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

from deep_learning_hank.hank_config import HankSteadyStateConfig
from deep_learning_hank.ha_kernel.equilibrium import (
    KernelEquilibriumResult,
    solve_kernel_equilibrium,
)

__all__ = ["KernelDiagnostics", "KernelDiagnosticsError", "run_kernel_diagnostics"]


class KernelDiagnosticsError(RuntimeError):
    """accepted 基线身份不匹配时抛出（load 时校验 DLH-3B config SHA-256）。"""


# Accepted DLH-3B 稳态（冻结的 accepted provenance；Task Index / Startup Snapshot /
# DLH-3B 执行报告）。canonical kernel 必须复现该均衡（同一经济问题，Issue #15 §5）。
ACCEPTED_3B_CONFIG_SHA256 = "82AB4A02F9D08FBBAED1349BC027FACE5361B1AB24C710C4CEA6958481CD5FC1"
ACCEPTED_3B_R_STAR = 0.007370613883670197
ACCEPTED_3B_N_STAR = 1.0656334480169984
ACCEPTED_3B_A_HH_STAR = 10.000000002223675
ACCEPTED_3B_W_STAR = 5.0 / 6.0
ACCEPTED_3B_C_STAR = 1.065633448423122


@dataclass(frozen=True)
class KernelDiagnostics:
    """内核诊断结果：一切残差与门限判定。"""

    config_sha256: str
    result: KernelEquilibriumResult
    hjb_residual: float
    hjb_converged: bool
    labor_kkt_max: float
    consumption_foc_max: float
    kfe_mass_error: float
    kfe_minimum_mass: float
    kfe_negative_mass_count: int
    kfe_nan_inf_count: int
    asset_clearing_residual: float
    labor_clearing_residual: float
    goods_residual: float
    fiscal_residual: float
    profits_residual: float
    wealth_flow_residual: float
    cross_check_r_diff: float
    cross_check_N_diff: float
    cross_check_A_hh_diff: float
    all_gates_pass: bool


def run_kernel_diagnostics(config_path: Path) -> KernelDiagnostics:
    """验证基线身份 → 求解内核均衡 → 报告全部门限。

    诊断 ↔ 数学条件（Issue #16 §4"Scientific mapping"）：
    - hjb_residual            ↔ max|ρV - (U(c,n) + G V)| ≤ hjb_tolerance (1e-7)
    - labor_kkt_max           ↔ 劳动 FOC v'(n) = (1-τ_l)w z V_a 的最大 KKT 违例 ≤ kkt_tolerance
    - consumption_foc_max     ↔ 消费 FOC u'(c) = V_a 的最大违例 ≤ consumption_foc_tolerance
    - kfe_mass_error          ↔ |Σg - 1| ≤ kfe_mass_tolerance (1e-10)
    - kfe_minimum_mass        ↔ min g ≥ negative_mass_threshold (-1e-12)（非负性）
    - asset_clearing_residual ↔ A_hh - B = 0（≤ clearing_tolerance 1e-6）
    - labor_clearing_residual ↔ N_hh - N = 0（≤ clearing_tolerance 1e-6）
    - goods/fiscal/profits/wealth ↔ 独立核算残差（≤ 各自冻结门限）
    - cross_check_*           ↔ 与 accepted DLH-3B 稳态差 ≤ 1e-6（科学意义未变）
    """
    config = HankSteadyStateConfig.from_toml(config_path)
    observed = hashlib.sha256(config_path.read_bytes()).hexdigest().upper()
    if observed != ACCEPTED_3B_CONFIG_SHA256:
        raise KernelDiagnosticsError(
            f"accepted DLH-3B baseline identity mismatch: {observed} != {ACCEPTED_3B_CONFIG_SHA256}"
        )

    result = solve_kernel_equilibrium(config)
    final = result.final
    if final.household is None or final.distribution is None:
        raise KernelDiagnosticsError("kernel equilibrium final evaluation is not finite")

    # 门限检查（冻结的 accepted DLH-3B 阈值）。
    hjb_ok = final.hjb_converged and final.hjb_true_residual <= config.numerical.hjb_tolerance
    household_ok = (
        hjb_ok
        and final.household.labor_kkt_max <= config.numerical.kkt_tolerance
        and final.household.consumption_foc_max <= config.numerical.consumption_foc_tolerance
        and final.household.min_consumption > 0.0
        and final.household.lower_boundary_min_drift >= -1e-12
        and final.household.upper_boundary_max_drift <= 1e-12
        and final.household.generator_row_sum_max_abs <= config.numerical.generator_row_sum_tolerance
        and final.household.generator_min_off_diagonal >= config.numerical.generator_min_off_diagonal_tolerance
        and final.household.nan_inf_count == 0
    )
    kfe_ok = (
        final.distribution.mass_error <= config.numerical.kfe_mass_tolerance
        and final.distribution.minimum_mass >= config.numerical.negative_mass_threshold
        and final.distribution.negative_mass_count == 0
        and final.distribution.nan_inf_count == 0
    )
    clearing_ok = (
        abs(final.R_asset) <= config.numerical.clearing_tolerance
        and abs(final.R_labor) <= config.numerical.clearing_tolerance
    )
    accounting_ok = (
        abs(final.R_goods) <= config.numerical.goods_tolerance
        and abs(final.R_fiscal) <= config.numerical.fiscal_tolerance
        and abs(final.R_profits) <= config.numerical.profits_tolerance
        and abs(final.R_wealth) <= config.numerical.wealth_tolerance
    )

    cross_check_r_diff = abs(result.root_r - ACCEPTED_3B_R_STAR)
    cross_check_N_diff = abs(result.root_N - ACCEPTED_3B_N_STAR)
    cross_check_A_hh_diff = abs(final.A_hh - ACCEPTED_3B_A_HH_STAR)

    all_gates_pass = bool(
        household_ok and kfe_ok and clearing_ok and accounting_ok
        and cross_check_r_diff <= 1e-6
        and cross_check_N_diff <= 1e-6
        and cross_check_A_hh_diff <= 1e-6
    )
    return KernelDiagnostics(
        config_sha256=observed,
        result=result,
        hjb_residual=final.hjb_true_residual,
        hjb_converged=final.hjb_converged,
        labor_kkt_max=final.household.labor_kkt_max,
        consumption_foc_max=final.household.consumption_foc_max,
        kfe_mass_error=final.distribution.mass_error,
        kfe_minimum_mass=final.distribution.minimum_mass,
        kfe_negative_mass_count=final.distribution.negative_mass_count,
        kfe_nan_inf_count=final.distribution.nan_inf_count,
        asset_clearing_residual=final.R_asset,
        labor_clearing_residual=final.R_labor,
        goods_residual=final.R_goods,
        fiscal_residual=final.R_fiscal,
        profits_residual=final.R_profits,
        wealth_flow_residual=final.R_wealth,
        cross_check_r_diff=cross_check_r_diff,
        cross_check_N_diff=cross_check_N_diff,
        cross_check_A_hh_diff=cross_check_A_hh_diff,
        all_gates_pass=all_gates_pass,
    )
