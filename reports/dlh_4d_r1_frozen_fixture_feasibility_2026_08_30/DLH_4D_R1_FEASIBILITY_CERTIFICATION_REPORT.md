# DLH-4D-R1 — Frozen Option A Fixture GE Feasibility Certification Report

- Date: 2026-08-30
- Author: DSH (bounded scientific diagnostic executor)
- Authority: GitHub Issue #21 — `DLH-4D-R1: Certify frozen Option A fixture GE feasibility over the full domain`（OPEN），activation comment id `IC_kwDOT9FOGc8AAAABRe5Euw`
- Task type: `SCIENTIFIC_DIAGNOSTIC__FROZEN_FIXTURE_GE_FEASIBILITY_CERTIFICATION`
- Status: **DIAGNOSTIC INCONCLUSIVE（fail-closed）** — 按冻结诊断协议，既未发现满足认证条件的 GE root，也未满足数值不可行认证的全部六项条件（第 6 项不成立）。

## 1. Terminal classification

**`BLOCKED_DLH_4D_R1_DIAGNOSTIC_INCONCLUSIVE`**

诊断结论（协议 D）：
- 729 点全域网格 + 27 个有界 least-squares 起点**均未发现** normalized residual inf-norm ≤ 1e-6 的 root 候选；
- 但数值不可行**认证**未授予：条件 1-5 满足（网格最佳 norm 0.936 ≫ 1e-3；LS 最佳 norm 0.539 ≫ 1e-6；最佳点有限且可分解；双跑精确可复现），**条件 6 不满足**——网格 452/729（62.0%）候选点为非有限（家户 KFE contaminated-row solve 奇异），不能排除结论部分由非有限区域驱动；
- 因此：**既未认证不可行，也未发现备选 root** → `BLOCKED_DLH_4D_R1_DIAGNOSTIC_INCONCLUSIVE`。
- 注意：这不等于"fixture 可行"；它与 Issue #20 的 fail-closed blocker（`DLH_4D_ROOT_BRACKET_FAILURE`）一致地不支持 GE 稳态存在，但按协议不能升级为"已认证不可行"。

## 2. Baseline / Issue / branch / commit

- Fresh baseline `origin/main` SHA: `0f55c583267b69c97c9276abda7d2f8921302561`
- Issue #21 title/status: OPEN；activation comment `IC_kwDOT9FOGc8AAAABRe5Euw`
- Accepted predecessor blocker commit: `40ec7ee3d676fc03863a3d2c2b1722b7ad53b2a5`（Issue #20）
- Immutable household identity（每次诊断前校验）：blob `57e32076f0e11c9a047e1f90f8c2446d4148e457`、SHA-256 `276D2244B389D6EDE140DAF8B1F9B0BE1F4AA859368941CED1A12BA8A5831AB8` —— 精确匹配（`BLOCKED_DLH_4D_R1_IMMUTABLE_HOUSEHOLD_IDENTITY_MISMATCH` 未触发）
- Dedicated branch: `dsh/issue-21-dlh-4d-r1-frozen-fixture-feasibility-2026-08-30`（基于 fresh `origin/main`）
- Candidate commit: single coherent commit（SHA 见 completion response）

## 3. 诊断协议执行（冻结；production `evaluate_ge` 只读复用）

### A. 全域粗网格（9³ = 729 点）
- 网格：`r_a ∈ [0, 0.12]`（9）、`r_b ∈ [−0.05, 0.10]`（9）、`L ∈ [0.2, 3.0]`（9），笛卡尔积 729 点。
- 每点记录：finite/HJB/KFE、raw/normalized `R1,R2,R3`、inf-norm、`A_hh,B_hh,L_hh,K,w,Y,T`、`R_resource_structural,W_taper,R_resource_faithful`、chain/direct wealth-flow。**非有限点不丢弃**（`DLH_4D_R1_FULL_DOMAIN_GRID.csv` 全量 729 行）。
- 结果：**277 有限（38.0%）/ 452 非有限（62.0%）**。

### B. 独立有界残差范数诊断（least_squares）
- `scipy.optimize.least_squares`，bounds = 冻结 domains；恰好 27 个确定性起点（各变量 {low, midpoint, high} 的笛卡尔积）；`max_nfev = 200`（冻结并报告）；非有限候选返回固定大惩罚 `1e6`（文档化，不静默丢弃）。
- 结果：27 个终点中 **12 有限 / 15 非有限**（部分起点直接落在非有限惩罚区，`nfev=1` 终止——恒定惩罚使 Jacobian 为零、`gtol` 立即满足）。

### C. 候选 root 认证
- 无候选满足 raw `R1,R2,R3 ≤ 1e-6` 且 normalized inf-norm ≤ 1e-8 → **未触发** root 认证（无需双冷启动重评估 / 与 `solve_ge` 对照）。

### D. 数值不可行认证规则（六条件逐一）

| # | 条件 | 观测 | 满足？ |
|---|---|---|---|
| 1 | 729 网格无点 norm ≤ 1e-3 | 网格最佳 norm = **0.9364**（(r_a=0.03, r_b=0.00625, L=0.55)） | ✅ |
| 2 | 27 个 LS 起点无一达 ≤ 1e-6 | LS 最佳 norm = **0.5393**（(r_a=0.0489, r_b=0.00796, L=1.595)） | ✅ |
| 3 | 最佳点有限且残差可分解 | 是（LS 最佳：R1=−10.21（资本）、R2=+0.45（债券）、R3=−0.76（劳动）） | ✅ |
| 4 | 最佳残差与零分离 ≥ 2 个数量级（相对 1e-8） | 0.539 ≫ 1e-6 | ✅ |
| 5 | 精确重复运行可复现 | 双跑 grid 与 LS 全部字段精确相等（`reproducible=True`） | ✅ |
| 6 | 结论非由非有限区域单独驱动 | **非有限占比 0.620 > 0.5**；高 r_a 切片（r_a≥0.105）100% 非有限 | ❌ |

→ **认证未授予**（条件 6 不成立）。

### 可复现性（Issue #21 Reproducibility）
- 完整协议双跑：729-grid 有限标志与全部有限标量输出、27 个 LS 终点/状态/残差、best-point 分类——**精确相等**（`grid_reproducible=True`、`ls_reproducible=True`、`reproducible=True`）。
- `BLOCKED_DLH_4D_R1_REPRODUCIBILITY_FAILURE` 未触发。

## 4. 结果解读（Required interpretation — 分离可能原因）

| 可能原因 | 证据 | 判断 |
|---|---|---|
| `B_gov=1` liquid-supply mismatch | 低 r_a（≤0.03）处 `B_hh < 1`（网格最佳点 R2=−0.94，B_hh≈0.064）；高 r_a（≥0.045）处 `B_hh ≥ 1.5-2.4`（R2=+0.45…+2.39）。债券清算的可行 r_a 为窄带（约 0.04 附近穿越 1.0），与资本清算所需 r_a（≈0.05+）不重叠 | **主要候选解释**（与 Issue #20 证据一致） |
| `a_max=10` illiquid-grid capacity/boundary | 有限点 `A_hh ≈ 8.6-9.3`（接近 a-grid 上限 10）；低 r_a 处 `K = 10.4-35.5 > A_hh` → R1 恒负 | **主要候选解释**（资本需求超过家户最大 illiquid 容量） |
| `rho=0.02` saving motive | r_a ≫ rho 时家户过富（A 顶格 + B≥1.7）→ 两资产市场一致性被破坏 | 相关 |
| firm inverse-MPK 资本需求 | `K=L·(αZ/(r_a+δ))^(1/(1−α))` 在 r_a∈[0,0.12] 下 K/L∈[4.2,62.8]；配合 `L_hh≈0.87-0.91` 使 K≈8-58 | 相关（需求侧） |
| 数值非有限 / KFE 奇异候选区域 | 62% 非有限，集中于高 r_a（r_a≥0.105 全非有限）；家户 KFE contaminated-row solve 在这些候选奇异 | **阻碍认证的正式原因**（规则 6 不满足） |
| production nested-bracket 架构 | 独立诊断（网格 + LS）同样未找到 root；与嵌套 brentq 的 fail-closed 一致 | 非独立原因（未发现被 production 漏掉的 root） |

**结论**：诊断证据与 Issue #20 的 fail-closed blocker 一致——冻结 fixture 下三市场残差的最小值仍远离零（0.54-0.94 normalized），且债券/资本市场的可行 r_a 区域不重叠；但按协议（规则 6），62% 非有限区域阻止"数值不可行"认证 → **INCONCLUSIVE**。

## 5. 输出文件

1. `DLH_4D_R1_FEASIBILITY_CERTIFICATION_REPORT.md`（本文件）
2. `DLH_4D_R1_FULL_DOMAIN_GRID.csv`（729 行全量记录，run 1；run 2 精确相等）
3. `DLH_4D_R1_LEAST_SQUARES_STARTS.csv`（27 行，run 1；run 2 精确相等）
4. `DLH_4D_R1_BEST_POINT_DIAGNOSTICS.csv`（grid/LS 最佳点 + summary）
5. `DLH_4D_R1_FORBIDDEN_OPERATION_CHECK.md`
- **`DLH_4D_R1_OWNER_DECISION_MATRIX.md` 未生成**（Issue #21 仅要求"若 fixture infeasibility 被认证"才提供；本诊断为 INCONCLUSIVE，未认证）。

## 6. 建议（非 binding）

- 本诊断**不授权**任何 fixture/route 修改；不提供决策矩阵（未认证不可行）。
- 若需推进，后续动作须由独立 open Issue / Owner 决策（例如：授权专门的非有限区域调查（KFE 奇异候选的分类与成因）、或在澄清非有限结构后重审认证协议）。本报告不自行选择。

## 7. 科学边界

本诊断仅提供**冻结协议下的有界结论**（未找到 root；不可行认证未达成；非有限占比 62%）。不验证 GE 稳态、不授权 fixture 修订、不验证 HANK 动态/NK/区域/DL、不支持校准/Results（Issue #21 scientific ceiling）。
