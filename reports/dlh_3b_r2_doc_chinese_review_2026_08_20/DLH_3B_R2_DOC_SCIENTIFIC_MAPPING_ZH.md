# DLH-3B-R2-DOC — 中文科学映射文档（equation → code / variable → meaning / diagnostic → condition）

- Date: 2026-08-20
- Authority: GitHub Issue #16 — `DLH-3B-R2-DOC: Chinese annotated HA kernel review package`（OPEN），activation comment id `IC_kwDOT9FOGc8AAAABP0ScXA`
- Task type: `DOCUMENTATION_ONLY__SCIENTIFIC_REVIEW_PACKAGE`
- 被注释对象：Issue #15 kernel（commit `750e5a2f508f3d3ebfcaa517271c29d3093d90f4`，branch `dsh/issue-15-dlh-3b-r2-ha-kernel-2026-08-20`）
- 本文件是评审包的一部分；**不修改任何代码**，仅做映射与说明。

## 1. 变量 → 经济含义（variable → economic meaning）

| 变量 | 经济含义 | 代码位置（live kernel） |
|---|---|---|
| `a` | 单一流动资产（风险中性政府债券索取权；真实值），`a ∈ [0, a_max=100]`，无借贷（`a_min=0`） | `household.py` `asset_grid`；`configs/dlh_3b_...toml` `[fixture] a_min/a_max/asset_grid_count` |
| `z` | 异质生产率（两状态 CTMC：`{0.5, 1.5}`，强度 0.25/0.25） | `household.py` `efficiency_states`/`state_generator`；`economics/grids.py` `build_idiosyncratic_generator` |
| `g(a,z)` | 家户稳态分布（质量归一化 Σg=1） | `distribution.py` `solve_kernel_distribution` |
| `V(a,z)` | 家户值函数 | `household.py` `solve_kernel_household` → `value` |
| `c(a,z)` / `n(a,z)` | 消费 / 内生静态劳动政策 | `household.py` `consumption` / `labor` |
| `ȧ(a,z)` | 资产漂移 = `(1-τ_l)w z n + r a + tr + Π − c` | `household.py` `drift`（= q·n + b − c） |
| `q` | 税后有效工资 `(1-τ_l) w z` | `household.py` `q` |
| `b` | 非劳动收入 `r·a + tr + Π` | `household.py` `b` |
| `w` | 实际工资 = `Z/μ`（稳态） | `equilibrium.py` `wage` |
| `r` | 实际回报率（均衡未知量之一） | `equilibrium.py` root `r` |
| `B` | 政府债券供给（恒定，`B=10`） | `configs/dlh_3b_...toml` `[fiscal] B`；`equilibrium.py` `bond_supply` |
| `N` | 聚合有效劳动（生产侧劳动，均衡未知量之一） | `equilibrium.py` root `N` |
| `N_hh` | 聚合劳动供给 `∫ z n dg` | `equilibrium.py` `N_hh` |
| `A_hh` | 聚合资产需求 `∫ a dg` | `distribution.py` `mean_assets` |
| `C` | 聚合消费 `∫ c dg` | `distribution.py` `mean_consumption` |
| `Y` | 产出 `Z·N`（labor-only 生产） | `equilibrium.py` `output` |
| `μ` | 加成 `ε/(ε−1)` | `equilibrium.py` `markup` |
| `mc` | 实际边际成本 = `1/μ`（稳态） | `equilibrium.py` `marginal_cost` |
| `Π` | 厂商利润 `Y − w·N`（零通胀） | `equilibrium.py` `profits` |
| `tr` | 一次性转移 `τ_l w N − r B` | `equilibrium.py` `transfer` |
| `τ_l, ρ, γ, φ, χ, n_max` | 劳动税率 0.15；折现率 0.01；风险厌恶 2；Frisch 弹性 1；劳动负效用系数 0.70；劳动上限 5 | `configs/dlh_3b_...toml` `[fixture]` |

## 2. 方程 → 代码位置（equation → code location）

| 经济学方程 | 代码位置（live kernel） |
|---|---|
| 效用 `u(c)=c^(1-γ)/(1-γ)` | `household.py` 复用 `economics/preferences.py utility/marginal_utility/inverse_marginal_utility` |
| 劳动负效用 `v(n)=χ n^(1+1/φ)/(1+1/φ)` | `household.py` `labor_disutility` / `marginal_labor_disutility` |
| 消费 FOC `u'(c)=V_a` | `household.py` `_policy_from_value`（`inverse_marginal_utility(derivative)`） |
| 劳动 FOC `v'(n)=(1-τ_l)w z V_a` | `household.py` `labor_policy` |
| 预算约束 `ȧ = (1-τ_l)w z n + r a + tr + Π − c` | `household.py` `q`/`b` 构造 + `drift = q·n + b − c` |
| 稳态 HJB `ρV = max{U + V_a ȧ + QV}` | `household.py` `solve_kernel_household` 伪时间迭代 + 真实残差 |
| 边界（state-constraint / no-outward-drift） | `household.py` `_policy_from_value`：`drift[:,0]=max(...,0)`、`drift[:,-1]=min(...,0)` |
| 生成元（行和 0；upwind + CTMC） | `household.py` `build_generator` |
| 平稳 KFE `G^T g = 0`，Σg=1 | `distribution.py` `solve_kernel_distribution` |
| 生产 `Y=Z·N`；`mc=w/Z`；`μ=ε/(ε-1)` | `equilibrium.py` `evaluate_kernel_equilibrium` |
| 财政 `tr = τ_l w N − r B` | `equilibrium.py` `transfer` |
| 资产清算 `A_hh = B` | `equilibrium.py` `R_asset = A_hh − bond_supply`；外层根 |
| 劳动清算 `N_hh = N` | `equilibrium.py` `R_labor = N_hh − N`；内层根 |

## 3. 诊断 → 数学条件（diagnostic → mathematical condition）

| 诊断（kernel diagnostics） | 数学条件 | 冻结门限 |
|---|---|---|
| `hjb_residual` | `max|ρV − (U(c,n) + G V)|` | ≤ `1e-7` |
| `labor_kkt_max` | 劳动 FOC `v'(n) = q V_a` 的最大 KKT 违例 | ≤ `1e-7` |
| `consumption_foc_max` | 消费 FOC `u'(c) = V_a` 的最大违例 | ≤ `1e-7` |
| `kfe_mass_error` | `\|Σg − 1\|`（质量守恒） | ≤ `1e-10` |
| `kfe_minimum_mass` | `min g`（非负性） | ≥ `-1e-12` |
| `negative_mass_count` / `nan_inf_count` | 负质量 / NaN-Inf 计数 | `0` |
| `asset_clearing_residual` | `A_hh − B` | ≤ `1e-6` |
| `labor_clearing_residual` | `N_hh − N` | ≤ `1e-6` |
| `goods_residual` | `Y − C − AC`（AC=0 于 π=0） | ≤ `1e-7` |
| `fiscal_residual` | `τ_l w N − r B − tr` | ≤ `1e-12` |
| `profits_residual` | `Π − (Y − wN − AC)` | ≤ `1e-12` |
| `wealth_flow_residual` | `0 − [(1-τ_l)wN_hh + rA_hh + tr + Π − C]`（稳态 Ȧ_hh=0） | ≤ `1e-7` |
| `cross_check_r/N/A_hh_diff` | 与 accepted DLH-3B 稳态差（科学意义未变） | ≤ `1e-6` |

## 4. 评审说明

- 中文注释评审副本位于 `annotated_kernel/`（`ha_kernel_household_ZH.py`、`ha_kernel_distribution_ZH.py`、`ha_kernel_equilibrium_ZH.py`、`ha_kernel_diagnostics_ZH.py`），逐字行为等价于 live kernel（仅新增注释）。
- 内核为**单资产**（one liquid risk-free bond）模型：**无**第二资产、**无**调整成本 `chi(d,a)`、**无**借贷溢价、**无**生产性资本（Issue #15/#16 明确禁止 two-asset / NK / regional / neural）。
- 所有数值为 `VALIDATION_FIXTURE_NOT_CALIBRATION`（accepted DLH-3B 夹具）；资产域 `[0,100]/401` 为开发域，不构成 HANK domain adequacy（DLH-3E 事务）。
- 本内核**不是** legacy Matlab `HANK_2ASSETS_HJB.m` 的翻译（其状态空间为 `(b,ah,z)` 双资产），亦不主张 Matlab parity（Issue #15 §1）。
