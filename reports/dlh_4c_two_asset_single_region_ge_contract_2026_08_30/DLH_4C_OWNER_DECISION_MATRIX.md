# DLH-4C — Owner Decision Matrix（闭合方案决策矩阵）

- Date: 2026-08-30（updated 2026-08-30: **Owner 已选定 Option A**；本矩阵保留为历史决策记录）
- Authority: GitHub Issue #19（OPEN），decision rule；Owner Decision comment id `IC_kwDOT9FOGc8AAAABReicYg`
- **Owner 决定（binding）**：**Option A — Aiyagari-minimal, constant government bonds, competitive firms** 为单区域双资产 GE 稳态闭合基线。**Option B、C 为历史备选，非活跃路线，未被授权。**
- 三个闭合包（≤3 选项）；方程计数均为 **3 unknowns = 3 residuals**（见 `DLH_4C_GE_DEGREE_OF_FREEDOM_AUDIT.md`）；家户块（不可变 oracle）三者共用。

## 决策矩阵

| 维度 | **Option A — Aiyagari-minimal, constant bonds, competitive（推荐）** | **Option B — Zero-net liquid, competitive** | **Option C — Markup + dividends (+ public capital)** |
|---|---|---|---|
| 资产映射 | `K = A_hh`；`B_hh = B_gov`（恒定外生债券） | `K = A_hh`；`B_hh = 0`（零净供给，内部货币） | `K = A_hh + K_gov`（可选公共资本）；`B_hh = B_gov` |
| 加成 | `μ = 1`（竞争；`Π=0`，无分红） | `μ = 1`（竞争） | `μ = ε/(ε−1)`（如 ε=6 ⇒ μ=1.2；`Π=(1−1/μ)Y`，`divrate=(1−τ_c)Π/K` 进入 `r_a`） |
| 厂商 | `Y=ZK^αL^(1−α)`；`w=F_L`；`r_a=r_k−δ` | 同 A | `Y=ZK^αL^(1−α)`；`w=F_L/μ`；`r_a=r_k−δ+divrate` |
| 财政 | `Tt=τwL−r_b·B_gov`（平衡预算，转移残差）；`G=0` | `Tt=τwL`（无利息）；`G=0` | `Tt=τwL+τ_cΠ−r_b·B_gov`；`G=0` |
| 未知量/方程 | `x=(r_a,r_b,L)`；`R=(A_hh−K, B_hh−B_gov, L_hh−L)`；**3=3** | `x=(r_a,r_b,L)`；`R=(A_hh−K, B_hh−0, L_hh−L)`；**3=3** | `x=(r_a,r_b,L)`；`R=(A_hh−(K−K_gov), B_hh−B_gov, L_hh−L)`（**记号修正 2026-08-30**：`K=A_hh+K_gov` 时资本清算残差须为 `A_hh−(K−K_gov)`）；**3=3** |
| 资源核算 | `R_resource_faithful = Y−C−δK−AC−W_taper = 0`（gate）；`W_taper=∫[r_a−r_a_eff(a)]·a·g`（`NUMERICAL_REGULARIZATION`）；`AC=Σ hjb.adjustment_cost·kfe.density·db·da`（只读） | 同 A | 同 A（加成在稳态为转移，非资源损耗；无 NK 价格调整成本） |
| 外生 fixture 数 | 中（`Z,α,δ,τ,rb_gap,B_gov`+家户参数） | 少（无 `B_gov`） | 多（另加 `ε,τ_c,K_gov`） |
| 与 accepted one-asset 惯例一致性 | **高**（恒定 `B`、平衡转移，DLH-3A/3B 直接扩展） | 中（零净供给偏离恒定债券惯例） | 中（加成/分红接近 legacy/Chapter-5 结构与未来 NK 稳态） |
| 优点 | 最小、无隐藏自由度、`r_a/r_b` 语义显式、与既有接受路线衔接最顺、最易验证 | 无外生债券参数；liquid 为纯内部货币 | 更接近 legacy 与未来 NK 稳态（稳态加成、分红、可选公共资本）；`r_a` 更丰富 |
| 缺点 | `r_b` 仅由家户 bond 需求钉住（无货币块）；`B_gov` 为外生 fixture 选择 | 聚合 liquid 恒为零（借贷者对消）；`r_b` 为纯家户 Euler 对象，货币扩展衔接稍弱 | fixture 参数更多；加成/分红/公共资本引入更多"科学选择"，验证面更宽 |
| 推荐 | **★ 推荐** | 备选 | 备选（若 Owner 倾向 NK-衔接路线） |

## 建议（2026-08-30 状态更新）

**Owner 已选定 Option A（binding）**。以下为历史记录：
1. 推荐 Option A：最小、与 accepted one-asset 恒定债券/平衡转移惯例一致、`A_hh=K`/`B_hh=B_gov` 语义显式、3=3 恰好确定、验证成本最低。
2. 若未来 Owner 希望为 NK 货币块预置稳态加成/分红结构 → 可另行评估 **Option C**（`K_gov=0` 纯加成子选项）——非活跃路线。
3. 若未来希望消除外生债券参数 → 可另行评估 **Option B**（零净 liquid 供给）——非活跃路线。
4. 组合边界：不得将 A/B/C 维度静默混搭而不重新审计自由度。

Owner 决定后（comment `IC_kwDOT9FOGc8AAAABReicYg`），DLH-4D（或等价实现任务）方可按冻结合同实现 GE solver；本任务冻结的是**合同**，非实现。修订后终分类：**`DLH_4C_OPTION_A_GE_CLOSURE_CONTRACT_REVISED_READY_FOR_GPT_REVIEW`**。
