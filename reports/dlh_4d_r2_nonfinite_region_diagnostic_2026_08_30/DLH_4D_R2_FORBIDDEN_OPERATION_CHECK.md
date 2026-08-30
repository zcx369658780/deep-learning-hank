# DLH-4D-R2 — Forbidden-Operation Check

- Date: 2026-08-30
- Authority: GitHub Issue #22 — `DLH-4D-R2: Classify non-finite household/KFE region before any fixture revision`（OPEN），activation comment `2026-08-30`（authority publication `4a9e7f8a9bb3e3a3a0b8b90dd9e485bf40f50d60`）
- Task type: `SCIENTIFIC_DIAGNOSTIC__NONFINITE_HOUSEHOLD_KFE_REGION_CLASSIFICATION`

## 1. Issue #22 forbidden operations

| Forbidden operation | Performed? | Evidence |
|---|---|---|
| 编辑 `src/deep_learning_hank/two_asset/**` | **0** | oracle 绝对只读；每次诊断运行经 `GeConfig.verify_oracle_identity` 校验（blob `57e32076…`、SHA `276D2244…`）；仅调用 `build_cold_initialization`/`solve_matlab_faithful_hjb`/`solve_matlab_faithful_stationary_kfe`/`aggregate_stationary_household`/`matlab_contaminated_row_index` 等 accepted 函数只读 |
| 编辑 `src/deep_learning_hank/ge/**` | **0** | 仅只读调用 `build_cold_initialization`；**不调用也不修改** `evaluate_ge`/`solve_ge`（旁路顶层 wrapper 仅为保留阶段级异常/warning，未改任何数值/经济方程） |
| config/test 变更 | **0** | `configs/**`、`tests/**` 零修改；fixture 与 domains 原样读取 |
| fixture/domain/parameter 变更 | **0** | `B_gov=1`、`rho=0.02`、`a_max=10`、grid 20×20、`alpha=0.36`、`delta=0.025`、`tau=0.15`、`rb_gap=0.01` 及 domains `r_a∈[0,0.12]`、`r_b∈[−0.05,0.10]`、`L∈[0.2,3.0]` 均未变 |
| Option A 经济变更 | **0** | `K=A_hh`、`B_hh=B_gov`、competitive `mu=1`、`Y=Z·K^α·L^(1−α)`、`w=F_L`、`r_a=F_K−δ`、`T=τ·w·L−r_b·B_gov`、`x=(r_a,r_b,L)`、`R=(A_hh−K, B_hh−B_gov, L_hh−L)` 未变 |
| 生产 solver 修复 | **0** | `solve_ge`/`evaluate_ge` 未触碰；本任务为纯 stage-resolved 诊断 |
| 替代 KFE 方法用于 claim PASS | **0** | Phase C 仅做只读 `splu`/`spsolve` 诊断与图拓扑诊断；**未**构造任何替代 KFE 求解以声称 PASS |
| 加宽 grid/domains | **0** | 未加宽 |
| NK/dynamics/IRFs | **0** | 无 |
| 区域/多省份 | **0** | 无 |
| learned matrices / neural / GPU | **0** | 无 |
| 经验校准/数据 | **0** | 无 |
| 福利/政策/Results | **0** | 无 |
| self-accept / merge / close Issue / PR / successor Issue | **0** | 仅创建 dedicated branch、单 commit、push；STOP for GPT review |

## 2. 不可变家户身份（每次诊断运行前校验）

| 项 | 值 | 结果 |
|---|---|---|
| path | `src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py` | ✅ |
| Git blob | `57e32076f0e11c9a047e1f90f8c2446d4148e457` | ✅ 精确匹配 |
| SHA-256 | `276D2244B389D6EDE140DAF8B1F9B0BE1F4AA859368941CED1A12BA8A5831AB8` | ✅ 精确匹配 |

→ `BLOCKED_DLH_4D_R2_IMMUTABLE_HOUSEHOLD_IDENTITY_MISMATCH` 未触发。

## 3. Allowed mutations（Issue #22）

仅新增 `reports/dlh_4d_r2_nonfinite_region_diagnostic_2026_08_30/` 下授权报告文件:

1. `DLH_4D_R2_NONFINITE_REGION_CLASSIFICATION_REPORT.md`
2. `DLH_4D_R2_ALL_NONFINITE_POINTS.csv`
3. `DLH_4D_R2_FAILURE_STAGE_SUMMARY.csv`
4. `DLH_4D_R2_FINITE_NONFINITE_BOUNDARY_PAIRS.csv`
5. `DLH_4D_R2_KFE_OPERATOR_REPRESENTATIVES.csv`
6. `DLH_4D_R2_FORBIDDEN_OPERATION_CHECK.md`（本文件）

无 src/config/test/fixture/domain/Option-A mutation。诊断脚本为 `%TEMP%` 中 ephemeral untracked 文件，不入仓；阶段数据位于 `%HOME%\dlh4d_r2_stage`（不入仓）。

## 4. 诊断协议（冻结；生产文件只读）

- **Phase A**：读取 #21 full-domain CSV 恰取 `finite=0` 的 **452** 点（计数校验通过）；逐点确定性重放 frozen candidate，直接调用阶段函数（旁路 `evaluate_ge` 仅保留阶段异常/warning），每点记录 56 字段并给出唯一终态阶段分类（10 类 + FULL_FINITE 哨兵，`UNCLASSIFIED` 仅作 fail-closed）；双跑精确复现。
- **Phase B**：冻结 729 网格按 #21 有限标志，取"恰好一个坐标差一个网格步"的有限↔非有限相邻对；每个存在转换的 `r_a` 切片最多字典序最早 2 对 → 14 对；双侧 side-by-side 记录 HJB statistic/iterations、`mu_a`/`mu_b` min/max、post-operator nnz/行和、KFE 结果、contaminated warning/exception。
- **Phase C**：仅对 KFE contaminated-row 失败点，确定性选取 ≤12 代表（按 `r_a` 切片覆盖 + 切片内字典序最早 `(r_b,L)`）→ 7 个；只读复用 post-convergence operator，报告 state count、operator/contaminated nnz 与 data 有限性、行和、`splu` 诊断（只读）、`spsolve` MatrixRankWarning/raw 有限性、正非对角转移图弱/强连通分量与 sink SCC（**仅诊断拓扑证据**）、匹配有限邻居对照。
- 可复现性：Phase A 双跑要求 56 字段 × 452 点精确相等（0 差异，已验证）；Phase B/C 在 Phase A 冻结后运行一次。

## 5. Git 纪律

- 专用 branch：`dsh/issue-22-dlh-4d-r2-nonfinite-region-diagnostic-2026-08-30`（基于 fresh `origin/main` `4a9e7f8a9bb3e3a3a0b8b90dd9e485bf40f50d60`）。
- 恰好一个 coherent commit；仅显式 stage 上述 6 个授权报告路径；仅 push 专用 branch；禁止 `git add .` / `git add -A`。

## 6. 结论

所有禁止操作：**0 执行**。任务为纯阶段分解诊断（production household/GE 代码只读复用，旁路 wrapper 仅为保留异常/warning）；家户身份每次校验通过；452 点全部归类且双跑精确可复现。分类结果与证据严格一致：`DLH_4D_R2_NONFINITE_STAGE_MAP_COMPLETE_READY_FOR_GPT_REVIEW`。
