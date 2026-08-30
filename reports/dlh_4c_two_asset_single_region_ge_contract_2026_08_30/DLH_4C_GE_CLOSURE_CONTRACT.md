# DLH-4C — GE Closure Contract（通用均衡闭合候选合同）

- Date: 2026-08-30
- Authority: GitHub Issue #19（OPEN），activation comment id `IC_kwDOT9FOGc8AAAABReZw8Q`
- Status: **CANDIDATE CONTRACT for the recommended closure option（Option A）** — 依 Issue #19 decision rule，因存在多个科学上合法的闭合（见 `DLH_4C_OWNER_DECISION_MATRIX.md`），本任务终分类为 **`BLOCKED_DLH_4C_OWNER_CLOSURE_DECISION_REQUIRED`**；本文件将推荐选项（Option A）的合同细节**完整冻结为候选**，供 GPT/Owner 评审后选定。
- 本文件仅设计合同，**不实现任何 GE 代码**（Issue #19 Forbidden）。

## 0. 三层科学分离（Required scientific comparison）

1. **`ACCEPTED_IMMUTABLE_HOUSEHOLD_STRUCTURE`**（不可变）：`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`（blob `57e32076f0e11c9a047e1f90f8c2446d4148e457`，SHA-256 `276D2244B389D6EDE140DAF8B1F9B0BE1F4AA859368941CED1A12BA8A5831AB8`）——状态 `(b,a,z)`、HJB/KFE、调整成本、劳动 FOC、聚合 `C/L/A/B` 为 `ECONOMIC_STRUCTURE`。
2. **`NUMERICAL_REGULARIZATION / MATLAB_FAITHFUL_IMPLEMENTATION`**（oracle 内部）：illiquid-return taper、bare-`a` transfer FOC、spdiags-equivalent 迭代算子（signed off-diagonals）、contaminated-row KFE、derivative floors——**均为数值设备，不解释为新 GE 经济学**。
3. **`NEW_SINGLE_REGION_GE_CLOSURE_DESIGN`**（本任务设计）：厂商、要素价格、税收/转移、资产市场、资源核算的闭合。本层是**新的、显式的、可审计的**设计，不复制 legacy 手动闭合。

## 1. 推荐闭合（Option A）—— "Aiyagari-minimal, constant bonds, competitive"

> 单一封闭经济、实数（以最终品为 numeraire，P=1）、无增长稳态、单区域、无 NK 动态（`μ=1`）、无公共资本、恒定债券供给。这是与 accepted one-asset 路线（DLH-3A/3B 恒定 `B` 惯例）一致的最小扩展。

### A. 资产映射（Asset mapping）

| 问题 | 回答 |
|---|---|
| A1. 聚合 illiquid 家户财富 `A_hh` 代表什么 | 生产性私人资本存量 `K`（单区域企业使用的全部资本） |
| A2. 是否 `K = A_hh`，或另有固定/公共资本 | **`K = A_hh` 精确成立**（无 `K_gov`；公共资本为未来扩展，见决策矩阵 Option C） |
| A3. 聚合 liquid 家户财富 `B_hh` 代表什么 | 家户持有的政府债券（真实、无风险、一年期可再生） |
| A4. liquid 供给 | **政府债务 `B_gov`，外生恒定**（`B_gov = B̄`，`Ḃ_gov = 0`；惯例同 DLH-3B 恒定 `B`）——"零净供给"为合法备选（决策矩阵 Option B） |
| A5. 资产市场清算方程 | ① 资本市场：`A_hh = K`；② 债券市场：`B_hh = B_gov`；③ 劳动市场：`L_hh = L` |

### B. 厂商块（Firm block）

| 项目 | 冻结 |
|---|---|
| 生产函数 | `Y = Z·K^α·L^(1−α)`（Cobb-Douglas；`Z` 外生，`α ∈ (0,1)` fixture） |
| 资本折旧 | `δ > 0` fixture（参考 legacy `δ=0.025`） |
| 工资 | `w = Z·(1−α)·(K/L)^α = F_L`（边际产出；`μ=1`） |
| illiquid 回报 | `r_a = r_k − δ`，`r_k = Z·α·(K/L)^(α−1) = α·Y/K`（资本边际产出） |
| 利润/分红 | `Π = 0`（竞争，无加成）；无分红（`divrate = 0`） |
| 稳态加成/NK 楔子 | **absent（`μ=1`）**；NK 动态（NKPC/Taylor/Fisher/`ε_i`）为未来扩展（J 节），本任务不添加 |

### C. 家户价格映射（Immutable oracle inputs）

| Oracle 输入 | GE 映射 |
|---|---|
| `r_a` | `= r_k − δ`（厂商块；oracle 内部 taper `r_a·(1−0.1(a/a_max)^9)` 为 `NUMERICAL_REGULARIZATION`，保持原样；GE 残差使用 oracle 聚合输出） |
| `r_b` | GE unknown（债券回报；由 `B_hh = B_gov` 清算） |
| `tau` | `= τ`（劳动税率，fiscal fixture） |
| `wages` | `[w]`（单区域向量长度 1 = 厂商工资） |
| `migration_costs` | `[0.0]`（单区域惯例：无迁移成本） |
| `labor_weights` | `[1.0]`（单区域） |
| `transfer_income` | `= Tt = τ·w·L − r_b·B_gov` |
| `borrowing_rate_gap` | `= rb_gap`（外生 fixture，如 0.01） |

### D. 财政/liquid-asset 闭合（Fiscal closure）

| 项目 | 冻结 |
|---|---|
| 政府资产负债表 | 负债：`B_gov`（真实债券）；资产：0（Option A 无公共资本） |
| 劳动税收入 | `τ·w·L` |
| 债务利息 | `r_b·B_gov` |
| 转移规则 | `Tt = τ·w·L − r_b·B_gov`（平衡预算、残差式） |
| 政府支出 | `G = 0` |
| 政府预算地位 | **会计恒等式（诊断）**——转移规则使其恒成立，**非**均衡方程；明确声明，不继承 legacy 的"无预算零条件" |

### E. 资源核算（Resource accounting）

- 稳态资源条件：**`Y = C + δ·K + AC + G`**，其中 `AC = ∫ χ(d,a) dg`（oracle `adjustment_cost` 按密度聚合的调整成本；`G=0`）。
- 推导（诊断残差，非额外 root）：聚合家户预算（wealth-flow）`∫(μ_b+μ_a)dg = 0`（稳态）⇒ `(1−τ)wL + r_b·B_hh + Tt − C − AC + r_a·A_hh = 0`；代入 `Tt = τwL − r_b·B_gov`、清算 `B_hh=B_gov, A_hh=K, L_hh=L`、零加成厂商 `wL + (r_a+δ)K = Y` ⇒ `C = Y − δK − AC` ⇔ `Y = C + δK + AC + G`。**与 legacy 的 goods/resource 缺失不同，本合同的资源残差被显式计算并 gated。**

### F. Unknown vector 与 residual map（推荐 Option A）

- **未知向量 `x = (r_a, r_b, L)`**（有序）：

| # | 未知量 | 经济含义 | 单位/归一化 | 符号约定 | 来源 |
|---|---|---|---|---|---|
| x1 | `r_a` | illiquid 资本回报（净折旧） | 年率（小数） | 可为正/负，稳态通常 >0 | 资本清算 `A_hh=K` |
| x2 | `r_b` | 债券（liquid）回报 | 年率（小数） | 可为正/负 | 债券清算 `B_hh=B_gov` |
| x3 | `L` | 聚合有效劳动（生产侧） | 水平（单位劳动） | >0 | 劳动清算 `L_hh=L` |

- **残差向量 `R(x) = (R1, R2, R3)`**（有序，各与未知量对齐）：

| # | 残差 | 经济含义 | 方程来源 | 预期数值尺度 |
|---|---|---|---|---|
| R1 | `A_hh(x) − K(x)` | 资本市场清算（家户 illiquid 供给 = 厂商资本需求） | `K = L·(αZ/(r_a+δ))^(1/(1−α))`（由 `r_a=αZ(K/L)^(α−1)−δ` 反解） | 与 `K` 同量级（如 ~1-10） |
| R2 | `B_hh(x) − B_gov` | 债券市场清算 | 家户 liquid 聚合 vs 恒定供给 | 与 `B_gov` 同量级 |
| R3 | `L_hh(x) − L` | 劳动市场清算 | 家户有效劳动聚合 vs 生产劳动 | 与 `L` 同量级（~1） |

- 归一化残差（实施建议）：`R1/K_ref`、`R2/B_gov`、`R3/L_ref`（单位化，便于 root 收敛与 gate）。
- **计数**：3 unknowns = 3 residuals ⇒ 无欠定/超定（证明见 `DLH_4C_GE_DEGREE_OF_FREEDOM_AUDIT.md`）。家户块为 `(w,r_a,r_b,Tt,τ,rb_gap) → (A_hh,B_hh,L_hh,C_hh,AC_hh)` 的确定性函数（不可变 oracle），`w`、`Tt` 为 `(K,L,r_b)` 的显式函数，不引入额外自由度。

### G. Numeraire / 归一化（Normalizations）

- 最终品为 numeraire（`P=1`）；全部对象为实数。
- `Z` 外生固定（fixture `Z=1`）。
- 资产价格：债券面值为 1（价格 1），`r_b` 为票面回报。
- 家户质量归一化 1（oracle 密度 `∫g·db·da = 1`）。

### H. Solver architecture（设计，不实现）

- 序列：候选 `(r_a, r_b, L)` → `w=Z·F_L(K,L)`、`K=L·(αZ/(r_a+δ))^(1/(1−α))`、`Tt=τwL−r_b·B_gov` → 不可变家户 HJB/KFE（oracle `solve_household_steady_state`）→ 聚合 → `R(x)`。
- 方法族：确定性嵌套 bracket roots（沿 `r_a → r_b → L`，brentq + 有界扫描，仿 DLH-3B 嵌套 brentq 惯例）**或** 冻结 Jacobian-free 向量 root（`scipy.optimize.root(method='krylov')`，仿 DLH-3D 惯例）——实施任务在合同中冻结其一，不得事后调参。
- 可行域：`r_a ∈ [r_a_low, r_a_high]`（由 `αZ/…` 反解要求 `r_a+δ>0` 与折旧/回报界）、`r_b ∈ [r_b_low, r_b_high]`、`L ∈ [L_low, L_high]`（正劳动，扫描界）。
- Warm-start：先做一次有界确定性扫描（粗网格），取最小残差范数点作初始猜测；无随机。
- 停止容差：root inf-norm ≤ 1e-8（冻结）；家户 HJB/KFE gates 按 oracle 自身收敛标准；资源残差 ≤ 冻结容差。
- Fail-closed：root 不收敛 → `BLOCKED_DLH_4D_GE_ROOT_NONCONVERGENCE`（类）并保留证据；**无 PASS-seeking 参数调整**。

### I. Validation fixture（供后续实现任务；`VALIDATION_FIXTURE_NOT_CALIBRATION`）

- 网格：oracle 参考 `b∈[-2,5]`（20）、`a∈[0,10]`（20）、`z∈{0.8,1.3}`（2）、switch 1/3——单次家户求解 ~1s，GE 迭代可行。
- 家户参数（oracle 输入侧 fixture）：`rho=0.02`（**注意：与 legacy `rho=0.05` 不同——DLH-4B 验证证明该区域家户块非退化**，`A_hh>0, B_hh≠A_hh`；作为 fixture 冻结）、`gamma=2`、`phi=5`（↔ `frisch_l=0.2`）、`chi0=0.1`、`chi1=2`、`a_bar=1e-6`、`rb_gap=0.01`、`τ=0.15`、`Z=1`。
- 厂商/财政 fixture：`α=0.36`（资本份额惯例）、`δ=0.025`（legacy）、`B_gov=1.0`（fixture，量级与家户 bond 需求匹配，非校准）。
- 规划 gates（实施任务须含）：不可变家户 SHA/blob 身份；家户 HJB 收敛；KFE 密度归一化/非负性；`A_hh`、`B_hh` 分别报告；全部 GE 残差 ≤ 冻结容差；资源残差；确定性 repeat；局部扰动/root 稳定性；predecessor regression。
- 明确标签：非中国/省份校准。

### J. Future-interface 保存（未来扩展须保持的接口）

| 未来层 | 需保持的接口 |
|---|---|
| 转移动态 | GE residual map `R(x)` 与单期家户求解为逐期构件；oracle `solve_household_steady_state` 接口（grid/params/inputs/numerics）保持 |
| NK 货币块 | `r_b`、`w` 为 NK 层将来扰动的接口（`ε_i → Taylor/Fisher → r_b`）；本合同冻结的稳态 `r_b` 为基准 |
| 多区域资本/劳动流 | 单区域闭合定义逐区域家户求解；区域扩展在其外包 `W^L/W^K` |
| learned `W^L`，后续 `W^K` | GE 残差 `R1–R3` 为 learned 网络须满足的逐区域纪律 |
| Deep Learning 组件 | 家户求解为确定性子图，DL 组件不得替换之 |

## 2. 决策规则结论

依 Issue #19 decision rule：**存在多个科学上合法的闭合**（债券市场：恒定供给 vs 零净供给；财政：转移残差 vs 债务调整；资本映射：`K=A_hh` vs `+K_gov`；加成：`μ=1` vs `μ>1` 带分红）→ **Builder 不得静默选择** → 终分类 **`BLOCKED_DLH_4C_OWNER_CLOSURE_DECISION_REQUIRED`**；`DLH_4C_OWNER_DECISION_MATRIX.md` 提供 ≤3 个闭合包（A/B/C）、方程计数、优劣与推荐（推荐 Option A）。
