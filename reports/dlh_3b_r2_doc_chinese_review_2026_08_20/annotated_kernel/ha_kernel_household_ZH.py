# -*- coding: utf-8 -*-
"""
DLH-3B-R2-DOC — 中文注释评审副本（REVIEW COPY / 仅供人工审阅，不参与导入执行）
================================================================================

本文件是 Issue #15 内核模块 `src/deep_learning_hank/ha_kernel/household.py`
（commit 750e5a2f508f3d3ebfcaa517271c29d3093d90f4）的**逐字行为等价评审副本**：

- 所有可执行语句与原模块完全一致（行为不变，Issue #16 §3）；
- 仅新增中文注释，用于 Owner / 外部评审者对照"经济学方程 ↔ 代码实现 ↔ 数值算法"；
- 本文件位于 `reports/` 下，**不会被导入、不会被 pytest 收集**，仅作文档。

对应经济学契约见：
`reports/dlh_3b_r2_ha_kernel_2026_08_20/DLH_3B_R2_IMPLEMENTATION_REVIEW.md`（§1.1 / §4）
与 `docs/specifications/DLH_3_*_2026_08_19.md`（accepted DLH-3A R1 方程契约）。

证据标签：`VALIDATION_FIXTURE_NOT_CALIBRATION`（数值夹具，非校准）。
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt
from scipy import sparse
from scipy.optimize import brentq
from scipy.sparse.linalg import spsolve

# 只读复用 accepted 工具函数：CRRA 效用 u(c)=c^(1-γ)/(1-γ) 及其导数/逆导数。
from deep_learning_hank.economics.preferences import (
    inverse_marginal_utility,
    marginal_utility,
    utility,
)

__all__ = ["HouseholdKernelResult", "solve_kernel_household"]

FloatArray = npt.NDArray[np.float64]


@dataclass(frozen=True)
class HouseholdKernelResult:
    """家户 HJB 求解结果（不可变 dataclass）。

    - value: 值函数 V(a,z)，形状 (states, assets)
    - consumption: 消费政策 c(a,z)
    - labor: 劳动政策 n(a,z)（内生静态劳动）
    - drift: 资产漂移 ȧ(a,z) = cash_flow - c
    - policy_choice: 每节点选择的政策分支（0=零漂移, 1=前向储蓄, 2=后向支取）
    - generator: 连续时间无穷小生成元 G（行和为 0），HJB 与 KFE 共用
    - converged / iterations / true_residual: 收敛状态与真实 HJB 残差
    - labor_kkt_max / consumption_foc_max: 劳动 KKT 与消费 FOC 最大违例
    """

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
    labor_kkt_max: float
    consumption_foc_max: float
    nan_inf_count: int
    residual_history: tuple[float, ...]


def labor_disutility(n: FloatArray, *, chi: float, frisch: float) -> FloatArray:
    """劳动负效用：v(n) = chi * n^(1+1/frisch) / (1+1/frisch)。

    方程映射：U(c,n) = u(c) - v(n)，可分离效用；frisch 为劳动供给 Frisch 弹性。
    """
    exponent = 1.0 + 1.0 / frisch
    return chi * np.asarray(n, dtype=np.float64) ** exponent / exponent


def marginal_labor_disutility(n: FloatArray, *, chi: float, frisch: float) -> FloatArray:
    """边际劳动负效用：v'(n) = chi * n^(1/frisch)。用于劳动 FOC。"""
    return chi * np.asarray(n, dtype=np.float64) ** (1.0 / frisch)


def labor_policy(
    effective_wage: FloatArray, marginal_value: FloatArray, *, chi: float, frisch: float, n_max: float
) -> FloatArray:
    """内生静态劳动 FOC：v'(n) = q * V_a  ⇒  n = (q * V_a / chi)^frisch。

    其中 q = (1-tau_l) * w * z 为税后有效工资（effective_wage 参数），V_a 为资产边际价值。
    KKT 裁剪到 [0, n_max]：n_max 为劳动供给上限（夹具 n_max=5）。
    方程映射：accepted DLH-3A §1.4 —— v'(n) = (1-τ_l) w z V_a。
    """
    raw = (
        np.asarray(effective_wage, dtype=np.float64)
        * np.asarray(marginal_value, dtype=np.float64)
        / chi
    ) ** frisch
    return np.clip(raw, 0.0, n_max)


def _solve_zero_drift_node(
    q: float, b: float, *, gamma: float, frisch: float, chi: float, n_max: float, consumption_floor: float
) -> tuple[float, float, bool]:
    """单个节点上的"零储蓄"（零漂移）静态问题。

    零漂移意味着 ȧ = 0 ⇒ c0 = b + q*n0，其中 b = r*a + tr + Pi（资产收益+转移+利润），
    q = (1-tau_l)*w*z（税后有效工资）。
    一阶条件：chi*n0^(1/frisch) = q*c0^(-gamma)（劳动 FOC 与消费 FOC 联立，n 单调 ⇒ brentq 唯一根）。
    返回 (c0, n0, feasible)；无可行正消费时返回不可行标志。
    """
    if q <= 0.0:
        return (float("nan"), float("nan"), False)
    c_max = b + q * n_max
    if c_max <= consumption_floor:
        return (float("nan"), float("nan"), False)

    def f(n: float) -> float:
        c = b + q * n
        if c <= consumption_floor:
            return -np.inf
        return chi * n ** (1.0 / frisch) - q * c ** (-gamma)

    f_max = f(n_max)
    if f_max <= 0.0:
        # 内点解落在 n_max 之上 ⇒ 上界 KKT 解（劳动夹在 n_max）。
        return (float(c_max), float(n_max), True)
    n_min = max(0.0, (consumption_floor - b) / q)
    f_min = f(n_min)
    if f_min >= 0.0:
        # 约束最优会落在 c0 == consumption_floor，违反严格正消费要求 ⇒ 不可行。
        return (float("nan"), float("nan"), False)
    root = brentq(f, n_min, n_max, xtol=1e-14)
    return (float(b + q * root), float(root), True)


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
    """在 (state, asset) 网格上向量化求解零漂移政策 (c0, n0, feasible)。"""
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
    """从值函数 V 生成 upwind 三候选政策（零漂移 / 前向储蓄 / 后向支取）。

    数值算法（accepted HACT 语义）：
    1. 资产方向前向/后向差分：V_a^F = (V_{i+1}-V_i)/dh，V_a^B = (V_i-V_{i-1})/dh；
    2. 边界：下界 a_min 处 V_a^B 用约束消费的边际效用 u'(c0)，上界 a_max 处 V_a^F 同理
       （state-constraint / no-outward-drift 边界，非反射过程）；
    3. 由消费 FOC c = u'^{-1}(V_a) 与劳动 FOC n = (q*V_a/chi)^frisch 得到各候选；
    4. 哈密顿量比较：H = u(c) - v(n) + V_a*drift，选择最大者；
    5. 前向候选仅在 drift>0 时可行，后向候选仅在 drift<0 时可行；
    6. 边界处理：drift[:,0]=max(drift[:,0],0)，drift[:,-1]=min(drift[:,-1],0)
       —— 即 a_min 处不允许资产进一步下降，a_max 处不允许资产进一步上升。
    """
    spacing = float(asset_grid[1] - asset_grid[0])
    derivative_forward = np.empty_like(value)
    derivative_backward = np.empty_like(value)
    derivative_forward[:, :-1] = (value[:, 1:] - value[:, :-1]) / spacing
    derivative_backward[:, 1:] = (value[:, 1:] - value[:, :-1]) / spacing
    boundary_marginal = marginal_utility(c0, gamma=gamma)
    derivative_backward[:, 0] = boundary_marginal[:, 0]
    derivative_forward[:, -1] = boundary_marginal[:, -1]
    derivative_forward = np.maximum(derivative_forward, 1e-14)
    derivative_backward = np.maximum(derivative_backward, 1e-14)

    # 前向（储蓄）候选：用前向差分边际值。
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

    # 后向（支取）候选：用后向差分边际值。
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

    # 零漂移候选：静态问题解 (c0, n0)，漂移恒为零。
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

    # 三候选哈密顿量比较（argmax；choice: 0=零漂移, 1=前向, 2=后向）。
    choice = np.argmax(
        np.stack((hamiltonian_zero, hamiltonian_forward, hamiltonian_backward), axis=0),
        axis=0,
    )
    consumption = np.where(choice == 1, c_forward, np.where(choice == 2, c_backward, c0))
    labor = np.where(choice == 1, n_forward, np.where(choice == 2, n_backward, n0))
    drift = np.where(choice == 1, drift_forward, np.where(choice == 2, drift_backward, drift_zero))
    # State-constraint / no-outward-drift 边界处理。
    drift[:, 0] = np.maximum(drift[:, 0], 0.0)
    drift[:, -1] = np.minimum(drift[:, -1], 0.0)
    # 所选政策对应的边际值（KKT 评估用）：前向/后向差分边际；零漂移用包络边际 u'(c0)。
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


def build_generator(
    drift: FloatArray, state_generator: FloatArray, spacing: float
) -> sparse.csr_matrix:
    """构造连续时间无穷小生成元 G（行和为 0，非对角元 ≥ 0）。

    生成元 = 资产漂移的 upwind 速率 + 异质生产率 CTMC 转移速率：
    - 资产向上（drift>0）：以 rate=drift/spacing 向右转移（行内 -rate / +rate）；
    - 资产向下（drift<0）：以 rate=-drift/spacing 向左转移；
    - 生产率状态 z 的转移：state_generator（2×2 CTMC，行和为 0）。
    该生成元同时用于 HJB（(rho+1/Δ)I - G）与 KFE（G^T g = 0），保证 HJB/KFE 一致性。
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
        return sparse.coo_matrix((vals, (rows, cols)), shape=(size, size)).tocsr()
    return sparse.csr_matrix((size, size), dtype=np.float64)


def solve_kernel_household(
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
) -> HouseholdKernelResult:
    """求解稳态单资产家户 HJB（含内生静态劳动）。

    输入（经济含义）：
    - asset_grid: 资产网格 a ∈ [0, a_max]（夹具 [0,100]，401 点，均匀）
    - efficiency_states: 生产率状态 z ∈ {0.5, 1.5}
    - state_generator: 2×2 CTMC 生成元 Q（0.25/0.25）
    - wage w, real_return r, transfer tr, profits Pi（家户收入侧聚合输入）
    - tau_l 劳动税率, rho_hh 折现率, gamma 风险厌恶, frisch Frisch 弹性,
      chi 劳动负效用系数, n_max 劳动上限

    算法（accepted 语义）：
    1. 零漂移政策（只依赖聚合输入，一次求解）；
    2. 伪时间迭代：[(rho + 1/Delta) I - G] V = u - v + V_old/Delta（Delta=1000）；
    3. 每次迭代由当前 V 生成政策 → 构造生成元 → 求解 V_new；
    4. 收敛判据：真实 HJB 残差 max|rho*V - (u - v + G@V)| <= tolerance（1e-7）。
    """
    if asset_grid.ndim != 1 or efficiency_states.ndim != 1:
        raise ValueError("household state grids must be one-dimensional")
    if state_generator.shape != (efficiency_states.size, efficiency_states.size):
        raise ValueError("idiosyncratic generator dimensions do not match")
    if not np.allclose(state_generator.sum(axis=1), 0.0, atol=1e-12):
        raise ValueError("state_generator must be a CTMC generator (rows sum 0)")
    spacing_values = np.diff(asset_grid)
    if np.any(spacing_values <= 0.0) or not np.allclose(spacing_values, spacing_values[0]):
        raise ValueError("the kernel HJB requires a uniform increasing asset grid")
    if rho_hh <= 0.0 or gamma <= 0.0 or chi <= 0.0 or frisch <= 0.0 or n_max <= 0.0:
        raise ValueError("preference/technology controls must be strictly positive")

    spacing = float(spacing_values[0])
    state_count = efficiency_states.size
    asset_count = asset_grid.size
    # 家户现金流：cash_flow(a,z) = (1-tau_l)*w*z*n + r*a + tr + Pi。
    # q = 税后有效工资（劳动收入系数）；b = 非劳动收入（资产收益 + 转移 + 利润）。
    q = np.broadcast_to(
        (1.0 - tau_l) * wage * efficiency_states[:, None], (state_count, asset_count)
    ).copy()
    b = np.broadcast_to(
        real_return * asset_grid[None, :] + transfer + profits, (state_count, asset_count)
    ).copy()

    c0, n0, zero_feasible = zero_drift_policy(
        q, b, gamma=gamma, frisch=frisch, chi=chi, n_max=n_max, consumption_floor=consumption_floor
    )
    if not np.all(zero_feasible):
        raise ValueError("no feasible positive-consumption zero-drift policy at some node")

    # 初值：零漂移政策的即期效用折现（消费正、劳动为正 ⇒ 效用有限）。
    value = (utility(c0, gamma=gamma) - labor_disutility(n0, chi=chi, frisch=frisch)) / rho_hh
    identity = sparse.eye(value.size, format="csr", dtype=np.float64)
    residual_history: list[float] = []
    converged = False
    consumption = c0
    labor = n0
    drift = q * n0 + b - c0
    choice = np.zeros(q.shape, dtype=np.int64)
    selected_marginal = marginal_utility(c0, gamma=gamma)
    generator = build_generator(drift, state_generator, spacing)
    iteration = 0

    for iteration in range(1, max_iterations + 1):
        # 1) 由当前 V 生成政策；2) 构造生成元；3) 伪时间步更新 V。
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
        generator = build_generator(drift, state_generator, spacing)
        matrix = (rho_hh + 1.0 / pseudo_time_step) * identity - generator
        rhs = (
            utility(consumption, gamma=gamma).ravel()
            - labor_disutility(labor, chi=chi, frisch=frisch).ravel()
            + value.ravel() / pseudo_time_step
        )
        value = np.asarray(spsolve(matrix, rhs), dtype=np.float64).reshape(value.shape)

        # 收敛评估：用更新后值函数重新生成政策与生成元，计算真实 HJB 残差。
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
        final_generator = build_generator(drift, state_generator, spacing)
        # 真实 HJB 残差：R_hjb = rho*V - [U(c,n) + G@V]（accepted 定义，绝不仅凭标签归零）。
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

    # 劳动 KKT 与消费 FOC 诊断（Issue #11 §5.3 语义）。
    labor_gap = q * selected_marginal - marginal_labor_disutility(labor, chi=chi, frisch=frisch)
    interior = (labor > 0.0) & (labor < n_max)
    kkt = np.where(
        interior,
        np.abs(labor_gap),
        np.where(labor <= 0.0, np.maximum(labor_gap, 0.0), np.maximum(-labor_gap, 0.0)),
    )
    labor_kkt_max = float(np.max(kkt))
    consumption_foc_max = float(np.max(np.abs(selected_marginal - marginal_utility(consumption, gamma=gamma))))

    # 生成元结构诊断：行和（应为 0）、非对角最小元（应 ≥ 0，含隐式零）。
    row_sums = np.asarray(final_generator.sum(axis=1)).ravel()
    off_diagonal = final_generator - sparse.diags(
        final_generator.diagonal(), format="csr", dtype=np.float64
    )
    stored_min_off_diagonal = float(np.min(off_diagonal.data)) if off_diagonal.nnz else 0.0
    nan_inf_count = int(
        np.count_nonzero(~np.isfinite(value))
        + np.count_nonzero(~np.isfinite(consumption))
        + np.count_nonzero(~np.isfinite(labor))
        + np.count_nonzero(~np.isfinite(drift))
        + np.count_nonzero(~np.isfinite(final_generator.data))
    )
    return HouseholdKernelResult(
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
        generator_row_sum_max_abs=float(np.max(np.abs(row_sums))),
        generator_min_off_diagonal=min(stored_min_off_diagonal, 0.0),
        labor_kkt_max=labor_kkt_max,
        consumption_foc_max=consumption_foc_max,
        nan_inf_count=nan_inf_count,
        residual_history=tuple(residual_history),
    )
