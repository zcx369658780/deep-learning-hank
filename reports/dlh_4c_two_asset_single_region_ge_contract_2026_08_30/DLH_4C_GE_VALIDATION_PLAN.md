# DLH-4C — GE Validation Plan（后续实现任务的验证夹具与规划 gates）

- Date: 2026-08-30（revised 2026-08-30 per Owner Decision + GPT targeted revision authority）
- Authority: GitHub Issue #19（OPEN）
- 状态：设计计划（不实现）；供后续 DLH-4D（或等价）实现任务使用；**以 Owner 冻结的 Option A 为前提**（`B/C` 为历史备选，非活跃路线）。

## 1. 验证夹具（`VALIDATION_FIXTURE_NOT_CALIBRATION`）

### 1.1 家户侧（不可变 oracle 输入；与 DLH-4B 验证一致的参数区）

| 参数 | 值 | 说明 |
|---|---|---|
| 网格 | `b∈[-2,5]`（20）、`a∈[0,10]`（20）、`z∈{0.8,1.3}`（2）、switch 1/3 | oracle 参考网格；单次家户求解 ~1s |
| `rho` | 0.02 | DLH-4B 验证区域（非退化：`A_hh>0, B_hh≠A_hh`）；legacy 0.05 区域家户块退化，故不用作 GE fixture 起点 |
| `gamma` | 2.0 | 参考 |
| `phi` | 5.0 | ↔ `frisch_l=0.2`（MATLAB 惯例） |
| `chi_0` / `chi_1` / `a_bar` | 0.1 / 2.0 / 1e-6 | 参考（bare-`a` FOC + `max(a,a_bar)` cost floor，保持 oracle 原样） |
| `rb_gap` | 0.01 | 借贷溢价 fixture |
| `tau` | 0.15 | 项目惯例（非校准） |
| `migration_costs` / `labor_weights` | `[0.0]` / `[1.0]` | 单区域惯例 |

### 1.2 厂商/财政侧（GE 外生）

| 参数 | 值 | 说明 |
|---|---|---|
| `Z` | 1.0 | 全要素生产率 fixture |
| `α` | 0.36 | 资本份额惯例（非校准） |
| `δ` | 0.025 | legacy 参考折旧 |
| `B_gov`（Option A/B） | 1.0（A）/ 0.0（B） | 债券供给 fixture（量级与家户 bond 需求匹配；非校准） |
| `K_gov`、`ε`、`τ_c`（仅 Option C） | `K_gov=0.0`、`ε=6.0`、`τ_c=0.0` | Option C 额外 fixture |

### 1.3 GE 数值

| 项目 | 值/方法（冻结于实现任务） |
|---|---|
| root 方法族 | 嵌套确定性 brentq（`r_a → r_b → L`）+ 有界扫描，或冻结的 Jacobian-free 向量 root（`scipy.optimize.root(krylov)`）——二选一，实现任务从合同中冻结 |
| root inf-norm 容差 | ≤ 1e-8 |
| 可行域 | `r_a+δ>0`；`r_b ∈ [r_b_low, r_b_high]`（如 [-0.05, 0.10]）；`L ∈ [L_low, L_high]`（如 [0.2, 3.0]） |
| warm-start | 有界确定性粗扫描取最小残差范数点；无随机 |
| 家户 HJB/KFE | oracle `solve_household_steady_state` 原样（不可变） |

## 2. 规划 gates（实现任务必须通过；均须冻结容差）

| # | Gate | 要求 |
|---|---|---|
| G1 | 不可变家户身份 | canonical 文件 blob `57e32076f0e11c9a047e1f90f8c2446d4148e457`、SHA-256 `276D2244B389D6EDE140DAF8B1F9B0BE1F4AA859368941CED1A12BA8A5831AB8` 逐次验证 |
| G2 | 家户 HJB 收敛 | oracle `hjb.converged`、`convergence_statistic ≤ 1e-7` |
| G3 | KFE 密度 | 归一化 `∫g·db·da = 1`；非负性（min g ≥ −1e-12；negative count 0） |
| G4 | 分离聚合报告 | `A_hh`、`B_hh` 分别报告（`A_hh ≠ B_hh` 恒为真；不合并） |
| G5 | GE 残差 | 归一化 `R1/R2/R3` inf-norm ≤ 1e-8（root）与市场残差 ≤ 1e-6 |
| G6 | **Faithful 资源残差** | **`R_resource_faithful = R_resource_structural − W_taper` ≤ 冻结容差（如 1e-6）**；**必须分别报告** ① `R_resource_structural = Y − C − δK − AC`、② `W_taper = ∫[r_a − r_a_eff(a)]·a·g`（`NUMERICAL_REGULARIZATION`）、③ `R_resource_faithful`。**不得**在保留 taper 的同时强制 `R_resource_structural = 0`（过度约束，与不可变家户块不一致） |
| G7 | 确定性 repeat | 两次完整 GE 求解 max diff = 0.0 |
| G8 | 局部扰动/root 稳定性 | 在 root 附近施加有界扰动（如各未知量 ±1%），root 返回原解（偏差 ≤ 容差）；至少一个方向 |
| G9 | predecessor regression | accepted 家户/one-asset 测试套件不回归 |

## 2b. 聚合对象只读计算（oracle 外；2026-08-30 澄清）

- `AC = Σ hjb.adjustment_cost · kfe.density · db · da`（accepted solver 输出只读聚合；oracle 不修改）。
- `W_taper = Σ [r_a − r_a_eff(a_j)] · a_j · kfe.density · db · da`（`r_a_eff(a) = r_a·(1 − 0.1·(a/a_max)^9)`，oracle taper；`NUMERICAL_REGULARIZATION` 报告项）。

## 3. Fail-closed 约定

- root 不收敛 / 残差超限 / 家户身份不匹配 → `BLOCKED_DLH_4D_GE_…` 类并保留证据；**无 PASS-seeking 调参**。
- 不改变不可变家户模块；不改变 oracle 的 taper/contaminated-row KFE/bare-`a` FOC。

## 4. 范围边界

- 本计划不验证 GE solver（未实现）、不验证 HANK 动力学、NK 货币传导、区域 NSR-HANK、Deep Learning、校准或 Results（Issue #19 scientific ceiling）。
