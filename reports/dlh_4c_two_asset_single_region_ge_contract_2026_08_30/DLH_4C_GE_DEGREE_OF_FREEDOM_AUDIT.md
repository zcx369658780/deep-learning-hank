# DLH-4C — GE Degree-of-Freedom Audit（自由度审计：未知量/方程计数）

- Date: 2026-08-30（revised 2026-08-30 per Owner Decision + GPT targeted revision authority）
- Authority: GitHub Issue #19（OPEN）
- 目标：显式计数各闭合选项的未知量与方程，证明推荐系统（**Option A，已由 Owner 冻结**）既非欠定也非超定；记录 legacy 的隐含自由度；为决策矩阵提供方程计数。
- **冻结状态**：Option A 为活跃路线（Owner binding）；Option B/C 为历史备选（非活跃）。

## 1. 计数基础（通用构件）

对任意选项，以下均为**确定性函数**（不引入未知量）：
- 不可变家户块：`(w, r_a, r_b, Tt, τ, rb_gap) → (A_hh, B_hh, L_hh, C_hh, AC_hh)`（oracle HJB/KFE/聚合；给定网格、家户参数、numerics）。
- 厂商/财政映射：`(r_a, r_b, L) → (w, K, r_k, Π, Tt, Y, R_fiscal)`（各选项的具体形式见下）。

## 2. Option A — "Aiyagari-minimal, constant bonds, competitive"

| 类别 | 数量 | 对象 |
|---|---|---|
| 未知量 | **3** | `x = (r_a, r_b, L)` |
| 均衡方程（残差） | **3** | `R1 = A_hh − K(x)`；`R2 = B_hh − B_gov`；`R3 = L_hh − L` |
| 确定函数 | — | `K = L·(αZ/(r_a+δ))^(1/(1−α))`（由 `r_a = αZ(K/L)^(α−1) − δ` 反解）；`w = Z(1−α)(K/L)^α`；`Tt = τwL − r_b·B_gov`；`Π = 0` |
| 诊断残差（非 root） | — | ① `R_resource_structural = Y − C − δK − AC`；② `W_taper = ∫[r_a − r_a_eff(a)]·a·g`（`NUMERICAL_REGULARIZATION`）；③ **`R_resource_faithful = R_resource_structural − W_taper`（gate 对象）**；另 `R_fiscal`、`R_wealth`、`R_profits` |

**计数：3 = 3 ⇒ 恰好确定（neither under- nor over-determined）。**
- 无隐藏自由度：`B_gov`、`Z`、`α`、`δ`、`τ`、`rb_gap`、家户参数、网格均为外生 fixture（`VALIDATION_FIXTURE_NOT_CALIBRATION`）。
- 家户质量归一化 1 由 oracle 密度归一化固定；numeraire 由实数经济固定（`P=1`）。

## 3. Option B — "Zero-net liquid supply, competitive"

| 类别 | 数量 | 对象 |
|---|---|---|
| 未知量 | **3** | `x = (r_a, r_b, L)` |
| 均衡方程 | **3** | `R1 = A_hh − K(x)`；`R2 = B_hh − 0`；`R3 = L_hh − L` |
| 确定函数 | — | 同 Option A，但 `B_gov = 0`，`Tt = τwL`（无利息支出） |

**计数：3 = 3 ⇒ 恰好确定。** 无外生 `B_gov` 参数（更少 fixture），但聚合 liquid 位置恒为零（借贷者对消储蓄者），`r_b` 完全由家户 Euler 决定。

## 4. Option C — "Markup + dividends (+ optional public capital)"（历史备选）

| 类别 | 数量 | 对象 |
|---|---|---|
| 未知量 | **3** | `x = (r_a, r_b, L)` |
| 均衡方程 | **3** | `R1 = A_hh − (K − K_gov)`（**记号修正（2026-08-30，provenance）**：若 `K = A_hh + K_gov`，私人资本清算残差必须写为 `A_hh − (K − K_gov)`；`K_gov = 0` 时退化为 `A_hh − K`——原写法 `R1 = A_hh − K` 与 `K = A_hh + K_gov` 不能同时成立）；`R2 = B_hh − B_gov`；`R3 = L_hh − L` |
| 确定函数 | — | `K = A_hh + K_gov`（`K_gov ≥ 0` 外生）；`μ = ε/(ε−1)`（`ε` fixture，如 6 ⇒ μ=1.2）；`w = Z·F_L/μ`；`Π = (1 − 1/μ)·Y`；`r_a = r_k − δ + divrate`，`divrate = (1−τ_c)·Π/K`（`τ_c` 公司税 fixture）；`Tt = τ·w·L + τ_c·Π − r_b·B_gov` |

**计数：3 = 3 ⇒ 恰好确定。** 额外 fixture 参数：`ε`、`τ_c`、`K_gov`（`K_gov=0` 时为纯加成选项）。加成使要素价格分解改变（`w` 更低、`Π > 0` 分红进入 `r_a`），资源条件 `Y = C + δK + AC + G` 仍成立（加成在稳态下是消费者→所有者转移，非资源损耗；无 NK 价格调整成本）。

## 5. Legacy 隐含自由度（对照）

| Legacy 对象 | 状态 | 隐含自由度 |
|---|---|---|
| `Tt=0.1`、`tau=0.05`、`rb_gap=0.07` | 固定 primitive，无平衡来源 | 校准自由度隐藏于这些选择 |
| `GovInv`（±10% 启发式） | 无显式方程 | 资本供给自由度 |
| `Bt`（仅诊断 `GovSurplus`） | 无债券市场方程 | `r_b`/`B` 机制缺失 |
| `Ct`（不进入资源条件） | 无资源方程 | 资源一致性未校验 |
| 逐省顺序更新（KNratio/Ytgap） | 手动收敛，无 residual vector | 无显式未知量/方程计数 |

→ 对照结论：新合同（A/B/C 任一）均**显式确定**（3=3），而 legacy 为欠定/非正式；新合同不继承 legacy 的隐含自由度。

## 6. 推荐

**Option A（Owner 已选定并冻结）**：3=3 恰好确定、最少 fixture、与 accepted one-asset 恒定债券惯例一致、`A_hh/K`、`B_hh/B_gov` 语义显式。Option B、C 为历史备选（非活跃路线）；最终选择由 Owner 决定（已于 2026-08-30 完成，见 `DLH_4C_OWNER_DECISION_MATRIX.md`）。修订后本任务终分类：**`DLH_4C_OPTION_A_GE_CLOSURE_CONTRACT_REVISED_READY_FOR_GPT_REVIEW`**。
