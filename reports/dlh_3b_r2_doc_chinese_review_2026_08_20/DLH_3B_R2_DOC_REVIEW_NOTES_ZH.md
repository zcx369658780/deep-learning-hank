# DLH-3B-R2-DOC — 中文评审笔记（Review Notes）

- Date: 2026-08-20
- Authority: GitHub Issue #16（OPEN），activation comment id `IC_kwDOT9FOGc8AAAABP0ScXA`
- Task type: `DOCUMENTATION_ONLY__SCIENTIFIC_REVIEW_PACKAGE`
- 目的：为 Owner 与外部评审者提供中文审阅要点，对照"经济学方程 ↔ 代码实现 ↔ 数值算法 ↔ 变量含义"；非算法修改。

## 1. 状态空间（Issue #16 §4 "Code annotation: state variables (a,z)"）

- 家户状态：`(a, z)` —— 单一流动资产 `a`（真实、无风险、政府债券索取权，`a ∈ [0,100]` 均匀 401 点，`a_min=0` ⇒ 无借贷）+ 两状态异质生产率 `z ∈ {0.5, 1.5}`（CTMC，强度 0.25/0.25）。
- 分布：`g(a,z)`，形状 `(2, 401)`，质量归一化 `Σg = 1`。
- 聚合状态：无（本内核仅稳态；动态/NK 层由未来独立 Issue 授权）。
- 区域维度：无（single-region validation fixture）。

## 2. 资产含义与核算（Issue #16 §4 "asset meaning"）

- `a` 是家户持有的**唯一**资产（liquid risk-free real bond claim），非生产性资本、非 illiquid 资产。
- 供给侧：政府恒定债券供给 `B = 10`（`Ḃ = 0`，无铸币税、无发债）。
- 聚合：`A_hh = ∫ a dg`；**唯一资产市场清算**：`R_asset = A_hh − B = 0`。
- 注意符号语义（与 legacy Matlab 的碰撞警示）：Python `B` = 债券**供给**；Matlab `Bt` = 流动资产**需求**；Python `chi` = 劳动负效用系数；Matlab `CHI` = 资产调整成本参数。二者不可混用（R1A 审计 findings 之一）。

## 3. HJB 方程映射（Issue #16 §4 "HJB equation mapping"）

- 稳态 HJB：`ρV(a,z) = max_{c,n}{ u(c) − v(n) + V_a[(1−τ_l)w z n + r a + tr + Π − c] + (QV)(a,z) }`。
- 消费 FOC：`u'(c) = V_a`；劳动 FOC（静态）：`v'(n) = (1−τ_l) w z V_a`（KKT 裁剪 `[0, n_max]`）。
- 数值算法：upwind 三候选（零漂移 / 前向储蓄 / 后向支取）哈密顿量选择；边界 = state-constraint / no-outward-drift（下界 `ȧ≥0`，上界 `ȧ≤0`，边界边际值取自约束消费 `u'(c0)`）；伪时间值迭代 `[(ρ+1/Δ)I − G]V = u − v + V_old/Δ`（Δ=1000）；收敛于**真实 HJB 残差** `max|ρV − (U + G V)| ≤ 1e-7`。

## 4. 劳动 FOC（Issue #16 §4 "labor FOC"）

- `n = min( [ (1−τ_l) w z V_a / χ ]^φ , n_max )`；零漂移节点的静态问题 `c0 = b + q·n0`，FOC `χ n0^(1/φ) = q c0^(−γ)` 单调 ⇒ brentq 唯一根。

## 5. 生成元构造（Issue #16 §4 "generator construction"）

- 连续时间**无穷小生成元**（行和为 0，非对角 ≥ 0）：upwind 资产漂移速率（`drift/spacing` 向流动方向）+ 异质生产率 CTMC 转移。
- **HJB 与 KFE 共用同一生成元**（单一算子），保证 HJB/KFE 一致性（accepted 语义；R1A 审计确认该耦合）。

## 6. KFE 逻辑（Issue #16 §4 "KFE logic"）

- 平稳 KFE：`G^T g = 0`；pin 最后一行施加 `Σg = 1`，求解后重归一化。
- 质量守恒：行和为零 ⇒ `1^T G^T = 0`（精确算术）；诊断：`mass_error ≤ 1e-10`、`min g ≥ −1e-12`、负质量/NaN 计数为 0。
- 微小负质量清理规则（仅在冻结阈值内 clip+renormalize）会被报告，不隐藏。

## 7. 均衡清算（Issue #16 §4 "equilibrium clearing"）

- 固定点 `(r, N)`：内层劳动根 `R_labor(N) = N_hh − N = 0`；外层资产根 `R_asset(r) = A_hh(r, N*(r)) − B = 0`。
- 确定性嵌套 brentq（主 bracket 优先，否则一次有界确定性扫描）；禁止为制造根而调参。

## 8. 与 accepted 证据的关系

- 内核复现 accepted DLH-3B 稳态**逐位一致**（`r*=0.007370613883670197`、`N*=1.0656334480169984`、`A_hh*=10.000000002223675`、`w*=5/6`、`C*=1.065633448423122`；cross-check diff = 0.0）——科学意义未变（Issue #15 §5 / Issue #16 §3 验证要求）。
- 与 legacy Matlab `HANK_2ASSETS_HJB.m`（`(b,ah,z)` 双资产 + 调整成本）**不是**同一模型；本内核不作 Matlab parity 主张（Issue #15 §1、Issue #16 §3）。

## 9. 边界与限制

- 本内核仅稳态、无 NK/货币政策/区域/神经组件（Issue #15/#16 明确排除）。
- 资产域 `[0,100]/401` 为开发域，非 HANK domain adequacy（DLH-3E 事务）。
- 所有数值 `VALIDATION_FIXTURE_NOT_CALIBRATION`，非经验校准；无政策/福利/Results 主张。
