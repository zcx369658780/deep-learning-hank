# -*- coding: utf-8 -*-
"""
DLH-3B-R2-DOC — 中文注释评审副本（REVIEW COPY / 仅供人工审阅，不参与导入执行）
================================================================================

本文件是 Issue #15 内核模块 `src/deep_learning_hank/ha_kernel/distribution.py`
（commit 750e5a2f508f3d3ebfcaa517271c29d3093d90f4）的**逐字行为等价评审副本**：

- 所有可执行语句与原模块完全一致（行为不变，Issue #16 §3）；
- 仅新增中文注释；
- 本文件位于 `reports/` 下，**不会被导入、不会被 pytest 收集**，仅作文档。

对应经济学契约：`DLH_3B_R2_IMPLEMENTATION_REVIEW.md` §1.2 / §5。
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt
from scipy import sparse

__all__ = ["KernelDistributionResult", "solve_kernel_distribution"]

FloatArray = npt.NDArray[np.float64]


@dataclass(frozen=True)
class KernelDistributionResult:
    """稳态分布求解结果（不可变 dataclass）。

    - mass: 稳态分布 g(a,z)，形状 (states, assets)，Σg = 1
    - stationarity_residual: max|G^T g|（KFE 平稳性残差）
    - mass_error: |Σg - 1|（质量守恒误差）
    - minimum_mass / pre_cleanup_minimum_mass: 清理前/后的最小质量（非负性检查）
    - cleanup_rule: 微小负质量清理规则（clip_to_zero_and_renormalize / none）
    - negative_mass_count / nan_inf_count: 负质量与 NaN/Inf 计数
    - state_marginals: 生产率状态的边际分布
    - mean_assets: A_hh = Σ g·a（聚合资产）
    - mean_consumption: C = Σ g·c（聚合消费）
    - lower/upper_boundary_mass: 下/上资产边界质量（边界集中诊断）
    """

    mass: FloatArray
    stationarity_residual: float
    mass_error: float
    minimum_mass: float
    pre_cleanup_minimum_mass: float
    cleanup_rule: str
    negative_mass_count: int
    nan_inf_count: int
    state_marginals: FloatArray
    mean_assets: float
    mean_consumption: float
    lower_boundary_mass: float
    upper_boundary_mass: float


def solve_kernel_distribution(
    *,
    generator: sparse.csr_matrix,
    asset_grid: FloatArray,
    consumption: FloatArray,
    mass_tolerance: float,
    negative_mass_threshold: float,
) -> KernelDistributionResult:
    """由转置无穷小生成元求解稳态分布。

    数值算法（accepted 语义，KFE 契约）：
    1. 平稳 KFE：G^T g = 0（G 为家户生成元，行和为 0 ⇒ 1^T G^T = 0，质量守恒在精确算术下成立）；
    2. 归一化：将最后一行的方程替换为 Σg = 1（pin 一行，rhs 最后一位 = 1），求解线性系统；
    3. 再归一化 g = raw/sum(raw)；
    4. 微小负质量清理：仅当 -threshold <= mass < 0 时 clip 到 0 并重归一化（清理规则必须报告）；
    5. 诊断：平稳性残差、质量误差、最小质量、负质量计数、NaN 计数、边界质量。
    """
    state_count, asset_count = consumption.shape
    if generator.shape != (state_count * asset_count, state_count * asset_count):
        raise ValueError("generator and household arrays have incompatible dimensions")
    if not np.allclose(np.asarray(generator.sum(axis=1)).ravel(), 0.0, atol=1e-10):
        raise ValueError("generator must be a CTMC generator (rows sum 0)")

    # G^T g = 0，用最后一行施加 Σg = 1（确定性直接法，np.linalg.solve）。
    matrix = generator.T.toarray()
    matrix[-1, :] = 1.0
    rhs = np.zeros(state_count * asset_count, dtype=np.float64)
    rhs[-1] = 1.0
    raw_mass = np.linalg.solve(matrix, rhs)
    pre_cleanup_minimum_mass = float(np.min(raw_mass))
    if not np.all(np.isfinite(raw_mass)) or abs(float(np.sum(raw_mass))) < mass_tolerance:
        raise ValueError("KFE linear system returned invalid mass")

    mass = raw_mass / float(np.sum(raw_mass))
    tiny_negative = (mass < 0.0) & (mass >= negative_mass_threshold)
    if np.any(tiny_negative):
        mass = mass.copy()
        mass[tiny_negative] = 0.0
        mass /= float(np.sum(mass))
    shaped_mass = np.asarray(mass.reshape((state_count, asset_count)), dtype=np.float64)
    stationarity_residual = float(np.max(np.abs(generator.T @ mass)))
    mass_error = abs(float(np.sum(mass)) - 1.0)
    minimum_mass = float(np.min(mass))
    negative_mass_count = int(np.count_nonzero(mass < negative_mass_threshold))
    nan_inf_count = int(np.count_nonzero(~np.isfinite(mass)))
    state_marginals = np.asarray(shaped_mass.sum(axis=1), dtype=np.float64)
    # 聚合：A_hh = Σ g·a；C = Σ g·c（质量归一化到 1，网格点权重一致）。
    mean_assets = float(np.sum(shaped_mass * asset_grid[None, :]))
    mean_consumption = float(np.sum(shaped_mass * consumption))
    lower_boundary_mass = float(np.sum(shaped_mass[:, 0]))
    upper_boundary_mass = float(np.sum(shaped_mass[:, -1]))
    return KernelDistributionResult(
        mass=shaped_mass,
        stationarity_residual=stationarity_residual,
        mass_error=mass_error,
        minimum_mass=minimum_mass,
        pre_cleanup_minimum_mass=pre_cleanup_minimum_mass,
        cleanup_rule=(
            "clip_to_zero_and_renormalize"
            if bool(np.any((raw_mass < 0.0) & (raw_mass >= negative_mass_threshold)))
            else "none"
        ),
        negative_mass_count=negative_mass_count,
        nan_inf_count=nan_inf_count,
        state_marginals=state_marginals,
        mean_assets=mean_assets,
        mean_consumption=mean_consumption,
        lower_boundary_mass=lower_boundary_mass,
        upper_boundary_mass=upper_boundary_mass,
    )
