# DLH-4D-R1 — Forbidden-Operation Check

- Date: 2026-08-30
- Authority: GitHub Issue #21 — `DLH-4D-R1: Certify frozen Option A fixture GE feasibility over the full domain`（OPEN），activation comment id `IC_kwDOT9FOGc8AAAABRe5Euw`
- Task type: `SCIENTIFIC_DIAGNOSTIC__FROZEN_FIXTURE_GE_FEASIBILITY_CERTIFICATION`

## 1. Issue #21 forbidden operations

| Forbidden operation | Performed? | Evidence |
|---|---|---|
| 编辑 `src/deep_learning_hank/two_asset/**` | **0** | oracle 只读；每次运行经 `GeConfig.verify_oracle_identity` 校验（blob `57e32076…`、SHA `276D2244…`） |
| 编辑 `src/deep_learning_hank/ge/**` | **0** | 仅**只读调用** `evaluate_ge`（production residual evaluator）；无任何 GE 源码编辑 |
| fixture/config 变更 | **0** | fixture 与 domains 原样读取（`configs/dlh_4d_two_asset_single_region_ge_validation.toml` 只读） |
| solver-domain 变更 | **0** | domains `r_a∈[0,0.12]`、`r_b∈[−0.05,0.10]`、`L∈[0.2,3.0]` 未变 |
| Option A 经济变更 | **0** | 残差/未知量定义未变 |
| 更改 `B_gov`/`rho`/`a_max`/grid/`alpha`/`delta`/`tau`/`rb_gap` | **0** | 未改 |
| PASS-seeking 调参 | **0** | 诊断协议完全冻结（729-grid、27 起点、`max_nfev=200`、非有限惩罚 `1e6`）；未改生产 solver |
| 生产 solver 修复 | **0** | `solve_ge` 未触碰；本任务为独立诊断 |
| NK/dynamics/IRFs | **0** | 无 |
| 区域/多省份 | **0** | 无 |
| learned matrices / neural / GPU | **0** | 无 |
| 经验校准/数据 | **0** | 无 |
| 福利/政策/Results | **0** | 无 |
| self-accept / merge / close Issue / PR / successor | **0** | 仅 push dedicated branch |

## 2. 不可变家户身份（每次诊断运行前校验）

| 项 | 值 | 结果 |
|---|---|---|
| path | `src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py` | ✅ |
| Git blob | `57e32076f0e11c9a047e1f90f8c2446d4148e457` | ✅ 精确匹配 |
| SHA-256 | `276D2244B389D6EDE140DAF8B1F9B0BE1F4AA859368941CED1A12BA8A5831AB8` | ✅ 精确匹配 |

→ `BLOCKED_DLH_4D_R1_IMMUTABLE_HOUSEHOLD_IDENTITY_MISMATCH` 未触发。

## 3. Allowed mutations（Issue #21）

仅新增 `reports/dlh_4d_r1_frozen_fixture_feasibility_2026_08_30/` 下授权报告文件（FEASIBILITY_CERTIFICATION_REPORT / FULL_DOMAIN_GRID.csv / LEAST_SQUARES_STARTS.csv / BEST_POINT_DIAGNOSTICS.csv / OWNER_DECISION_MATRIX（若 certified infeasible）/ FORBIDDEN_OPERATION_CHECK）。无 src/config/test/fixture/solver mutation。

## 4. 诊断协议（冻结）

- A. 729 点全域笛卡尔网格（9³）——记录全部有限/非有限、HJB/KFE、raw/normalized 残差、聚合、资源/wealth 对象；非有限点不丢弃。
- B. 27 个确定性起点（各变量 {low, midpoint, high} 的笛卡尔积）的 `scipy.optimize.least_squares`（bounds=冻结 domains；`max_nfev=200` 冻结并报告；非有限评估返回固定大惩罚 `1e6`，不静默丢弃）。
- C. 候选 root 认证（raw ≤ 1e-6 且 normalized inf-norm ≤ 1e-8 → 双冷启动重评估 + gates + 与 `solve_ge` 对照）。
- D. 数值不可行认证规则（六条件；非有限占比 < 50% 才允许认证）。
- 可复现性：完整协议双跑，要求精确相等（grid 有限标志与全部有限标量输出、27 起点终点/状态/残差、best-point 分类）。

## 5. Git 纪律

- 专用 branch：`dsh/issue-21-dlh-4d-r1-frozen-fixture-feasibility-2026-08-30`（基于 fresh `origin/main` `0f55c58`）。
- 恰好一个 coherent commit；仅显式 stage 授权报告路径；仅 push 专用 branch。

## 6. 结论

所有禁止操作：**0 执行**。任务为纯诊断（production `evaluate_ge` 只读复用）；家户身份每次校验通过；诊断结论（数值不可行认证 / 备选 root / 不确定）将如实报告。
