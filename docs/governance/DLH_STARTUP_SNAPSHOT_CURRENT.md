# 当前启动快照

日期：2026-09-18。仓库：`zcx369658780/deep-learning-hank`。
工作区：`D:\deep-learning-hank`。路线：`DLH-WL-V1-20260918`。

## 状态与版本解释

本轮发布前 main：`9058be73fc4b4211c8ad49ea0989d4fdc224ed1d`。
本文件所在文档提交是同步发布锚点；启动时记录实际 fresh main，不把发布前 SHA 当永久 HEAD。导出包外部 manifest 记录确切发布 SHA，避免文件自引用自己的 commit。

Owner 已批准新路线。P0 三端同步已完成。Issue #74 / P1A 已 **ACCEPTED / CLOSED / INTEGRATED** 于 `d34f00a31e8d23dd8134b9e9ba1be0319e7901bc`（Reviewer acceptance `5731836951`；integration `5731840451`）。P1A 只建立离线 W/P/F 核算接口与家庭依赖登记；学习训练尚未授权，经济耦合未授权. Issue #75 / P1B 已 **ACCEPTED / CLOSED / INTEGRATED** 于 `e1b83b3d5b2c04d7e9052ad614e95631abb03dc6`（Reviewer acceptance `5739889010`；integration `5739889903`）。P1 至此完成；下一 gate 是按冻结合同执行 P2 method-only synthetic prototype。

## 最新科学事实（保留，非本轮重跑）

Issue #73 / DLH-5V-Y CLOSED / COMPLETED。
accepted candidate/integration：`838764a9a489b771de852a684a2d2cc99703c168`。
Reviewer acceptance：`5728591018`；integration：`5728595318`。
Terminal A：`DLH_5VY_ROUTE_A_ONE_STEP_PROJECTED_REGULARIZED_NEWTON__DOMAIN_SAFE_SINGLE_Q_RESIDUAL_REDUCING_CANDIDATE_ACCEPTED__TRAJECTORY_DESIGN_GATE_READY`。

残差 `10.435094313164921 → 10.435094286652339`，绝对下降 `2.6512582351756464e-08`，ratio `0.9999999974592868`。接受第 `1340/9261` 次 `(3,0,16)`，lambda `0.125`、alpha `2^-16`。min p_b `5.41690375095121e-10`，max|Q1| `4.85061990573854e-12`；Armijo PASS，material<=0.5 FALSE；repeat IDENTICAL。起点 active constraints=0，projection=identity。

HJB convergence FALSE；candidate 不是解。不授权第二步、trajectory、stationary KFE、GE 或下游经济用途。solver 支线现在暂停。

## 保留的身份

- oracle blob：`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`
- selected-Q blob：`7857cabb4d28af99cb9d59e2d1c3024b05787c11`
- #69 blob：`83e9be0febcc03eb721265d3558887bd6b1586a4`
- #71 blob：`96dd262a4ae42e26d489a317d9a04a9264b481b1`
- #72 module blob：`f99ff6eb0d0a74cccc400ba83162a8affa9c6924`

ONE MATLAB-faithful selected generator governs solve/validation；Dual-Q 禁止；同过程 HJB/KFE 合同保留。未新增生产 W_max、价格适用区间或 solved checkpoint。

## 测试债务

#72 cumulative-path guard 已 durable 修复。#73 仍有旧四路径上限与授权五路径 remediation 的测试合同缺陷。已获低风险 waiver；不自动 scientific blocker。full suite 未在本轮执行，不声称 repository-wide green。不得为本次文档同步启动修复或重跑。

## 新主线与下一动作

第一版离线学习给定外流比例后的目的地份额；外流比例和家庭总劳动不联合训练。沿用 origin×destination、行归一。P1A 已验收；下一步是 P1B 数据/标签口径、canonical sample schema 与 P2 离线实验合同设计，不训练、不调用家庭。

路线与合同见 `README_START_HERE.md`。详细旧实验见 post-5VY 交接；本快照不重复全部历史。


## P2 current gate — 2026-09-19

P1B accepted/integrated at `e1b83b3d5b2c04d7e9052ad614e95631abb03dc6`. Issue #76 / P2A is now **ACTIVE / OPERATIVE** for the first frozen method-only synthetic execution; exact operative baseline and branch are named by the final activation comment. P2A may train only the frozen small neural prototype; it cannot alter the P1B contract/config or use real data/HJB/KFE/GE/MATLAB.


## P2A adjudicated — 2026-09-19

Issue #76 is CLOSED with accepted terminal `DLH_WL_P2A_OFFLINE_SYNTHETIC_PROTOTYPE__GATE_FAIL__NO_TUNING_AUTHORIZED`, integrated at `8c5a9a7f474ce1feac3c63e449e07753141d8984`. The published metrics and neural non-gain are observational only; there is no accepted P2 PASS because the absolute fit-attempt ceiling was breached (minimum proven 36, Builder-reported 48 vs ceiling 13). Next gate is a clean replication with immutable pre-run scientific code and no science rerun on reporting failure.


## P2B clean replication staged — 2026-09-19

Issue #77 is now **ACTIVE / OPERATIVE**. It preserves the #75 frozen scientific design and reuses the #76 scientific module byte-for-byte. The replication requires an immutable PRE_RUN_FREEZE commit, exactly one science invocation, durable per-fit attempt logging, immutable raw results, and zero-fit render-only publication. Exact operative baseline and branch are named by the Reviewer final activation.


## P2B adjudicated — 2026-09-19

Issue #77 is CLOSED with accepted terminal `DLH_WL_P2B_CLEAN_REPLICATION__GATE_FAIL__NO_SCIENCE_RERUN_AUTHORIZED`, integrated at `e0f3b633e75ef1971e634e34a4a8143193bfe4da`. Exactly one immutable science invocation completed all 12 fits with zero retry, but the process failed after the final fit and before RAW_RESULTS serialisation. The durable ledger contains completion metadata only, not predictions/model state, so no zero-fit metric recovery is possible. Next replication must persist full per-fit scientific output inside the durable completion record before proceeding.


## P2C durable-output replication staged — 2026-09-19

Issue #78 is now **ACTIVE / OPERATIVE**. It preserves the #75 frozen scientific design and accepted P2 scientific module. The new durability rule is that every FIT_COMPLETED ledger record must persist the full prediction tensor and sufficient FitOutcome metadata, fsynced before the next fit begins; all later metrics/constraints/rendering must be reconstructible with zero optimizer steps. Exact operative baseline and branch are named by the Reviewer final activation.


## P2C adjudicated — 2026-09-19

Issue #78 is CLOSED with accepted terminal `DLH_WL_P2C_DURABLE_OUTPUT_REPLICATION__GATE_FAIL__NO_SCIENCE_RERUN_AUTHORIZED`, integrated at `0758daccfe5b207e1dfaaae976559e3f2adc7a6e`. Its durability machinery is accepted: one science invocation, 12 durable completed fits, full persisted predictions, zero-fit rendering. The scientific Gate Fail is isolated to a missing `universe._design_matrix = design` assignment: neural optimization used TRAIN-z-scored inputs but final persisted predictions used raw-design fallback. Next replication keeps the #75 design and #78 durability protocol unchanged and repairs only that state propagation.


## P2D minimal corrected replication staged — 2026-09-19

Issue #79 is now **ACTIVE / OPERATIVE**. It preserves the #75 frozen scientific design and #78 accepted durable-output protocol. The only science-path repair is explicit `universe._design_matrix = design` propagation before neural fits, with a zero-fit pre-run prediction-path test that must distinguish the z-scored design from raw fallback. Exact operative baseline and branch are named by the Reviewer final activation.


## P2 method gate complete — 2026-09-19

Issue #79 / P2D is ACCEPTED / CLOSED / INTEGRATED at `8ae4561ca3b0c78ba1d47045182fa5b4b023ed6d` (Reviewer acceptance `5741061720`; integration `5741063251`). The frozen synthetic method experiment is now accepted: all protocol/preprocessing/durability gates pass, and the neural mapping does not beat the correctly specified parametric baseline in S0/S1. This is a valid negative synthetic-method result, not an empirical China result. The next gate is P3A real-data label/provenance/semantics verification before any empirical fitting.


## P3A real-data evidence gate staged — 2026-09-19

Issue #80 is now **ACTIVE / OPERATIVE**. It is evidence/schema validation only: source object, timing, population, bilateral OD support, stock/flow/transition semantics, direct-vs-bridged W status, provenance/licence and feature timing/leakage. Exact operative baseline and branch are named by the Reviewer final activation. No data ingestion or empirical fitting is authorized in P3A.


## P3A Branch B accepted — 2026-09-19

Issue #80 is ACCEPTED / CLOSED / INTEGRATED at `a1505cf0deeaee58c0cde9dc886a16ec502ddae9` (Reviewer acceptance `5741207677`; integration `5741209478`). No direct annual bilateral flow target is verified. Branch B is accepted because bilateral multi-year transition and stock OD objects are sufficiently documented to justify a separately authorized bridge-design gate. E3 remains 0 and no empirical fitting is authorized. Next gate is P3B bridge/source preregistration, not training.


## P3B bridge preregistration staged — 2026-09-19

Issue #81 is now **ACTIVE / OPERATIVE**. It compares and freezes bridge assumptions only: timing annualization, stock-to-flow, population-to-labor-service semantics, region dictionary, m/ell provenance, weights/harmonization, leakage and sensitivity axes. Exact operative baseline and branch are named by the Reviewer final activation. No empirical data ingestion, adapter or fit is authorized in P3B.


## P3B bridge candidate accepted — 2026-09-19

Issue #81 is ACCEPTED / CLOSED / INTEGRATED at `1819b0a5a36b2a8ffde3641c711892df2cdcede7` (Reviewer acceptance `5741469418`; integration `5741471600`). A T-family bridge candidate is preregisterable, but no empirical bridge is executable yet. Before any data-side implementation, P3C must freeze numerical tolerances/search semantics and the claim ceiling for stochastic-root uniqueness, plus the human source/schema verification checklist.


## P3C execution-readiness freeze staged — 2026-09-19

Issue #82 is now **ACTIVE / OPERATIVE**. It freezes Reviewer-side thresholds, numerical root-search semantics, uniqueness/non-existence claim ceilings and the E3 human source-verification packet before any real transition matrix is executed. Exact operative baseline and branch are named by the Reviewer final activation. No real bridge/data/model execution is authorized in P3C.


## P3C execution-readiness accepted — human verification pending — 2026-09-19

Issue #82 is ACCEPTED / CLOSED / INTEGRATED at `3496ba96b78992a579821348ad563e3b67afdf16` (Reviewer acceptance `5741828428`; integration `5741830109`). Numerical/search/claim semantics are frozen before any real matrix execution. H1–H7 remain 7/7 unresolved and E3 promotion is reserved to human/Owner verification. No Builder scientific issue is active and no empirical bridge execution is authorized.
