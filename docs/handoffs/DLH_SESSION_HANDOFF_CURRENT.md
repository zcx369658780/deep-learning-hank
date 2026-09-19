# 当前交接：继承 Owner 锁定路线

日期：2026-09-18。唯一仓库：`zcx369658780/deep-learning-hank`。
路线：`DLH-WL-V1-20260918`。P0 已完成；Issue #74 / P1A 已 ACCEPTED / CLOSED / INTEGRATED。

**不要重新规划。**Owner 已批准给定外流比例下的目的地份额学习，并要求模型切换后保留此路线。所有后续 GPT/DSH 都适用；可以提出有证据的变更，但无 Owner 新批准不改变锁定项。

先 fresh-read main；读 AGENTS/规则/Owner decision/Task Index/Snapshot/Roadmap/两合同。旧项目源 V0.x/旧 NEXT 被新决定替代，不从历史恢复任务。完整原始批准与 hash 在 decisions 和 route-lock manifest。

#73 已 completed；残差仍约 10.435，单步合法微降非 HJB 解，active constraints=0。没有第二步、trajectory、KFE/GE 授权。保留同一 Q，不能引入 Dual-Q。

当前顺序：Issue #75 / P1B 已 ACCEPTED / CLOSED / INTEGRATED。当前顺序：Reviewer 发布并激活 P2 首次 method-only synthetic run → DSH 严格按冻结 config 实现+focused test+执行 → Reviewer 独立验收。P1A 已建立家庭依赖登记及离线 W/P/F 接口；P1B 不重新审计 HA、不训练。

m 与家庭总劳动给定；W origin×destination、foreign 行归一；P 含 home；完整流量保留。两区只测核算，三区以上才有条件选择学习。合成/规则和现实标签分开；真实 OD 可用性尚未证明，不编造数据。

#73 已知 path guard 债务仍在，full suite 未全绿；文档同步不触发历史实验。科学假设失败可以结案，不无限追加预算。

建议恢复句：读取并继承 DLH-WL-V1-20260918，不重选研究路线；先确认项目源与 DSH 同步回报，再在锁定边界内下达下一任务。


## P2A staged
Issue #76 is ACTIVE / OPERATIVE. DSH must fresh-fetch, read the final activation, create the exact dedicated branch from the activation baseline, implement only the P2 harness/focused tests/results paths, then execute the frozen 12-planned-fit synthetic experiment under the 1800s / <=13-attempt ceiling. No outcome-driven tuning.


## P2A gate-fail accepted
Issue #76 is complete as a protocol-gate-failed experiment. Do not reopen or rerun it. Observed S0/S1 metrics are audit evidence only. The next task must preserve the frozen #75 design and obtain a clean replication by separating the one authorized scientific execution from zero-fit artifact rendering.


## P2B clean replication staged
Issue #77 is ACTIVE / OPERATIVE. DSH must read the final activation, then build and commit/push an immutable pre-run replication harness, and execute science exactly once from a clean detached worktree at that SHA. Scientific execution writes only durable attempt ledger + raw results; final reporting uses render-only and may never rerun fits.


## P2B gate-fail accepted
Issue #77 is complete. Do not rerun it. Its ledger proves 12 completed fits but cannot reconstruct predictions or final metrics. The next replication must make FIT_COMPLETED itself the durable scientific artifact: full predictions and sufficient fitted state are persisted/fsynced per fit, so all later aggregation/rendering is zero-fit recoverable.


## P2C staged
Issue #78 is ACTIVE / OPERATIVE. DSH must read the final activation, then first prove with a fake 12-fit ledger that the exact zero-fit aggregation/render path works end-to-end. Then it freezes pre-run code, executes science exactly once, and persists full predictions inside every FIT_COMPLETED record before proceeding to the next fit.


## P2C gate-fail accepted
Issue #78 is complete. Do not rerun it. The next replication must retain the accepted durable per-fit-output protocol and add only the missing neural preprocessing state propagation: the runner must set `universe._design_matrix = design` before any neural fit and prove pre-run, without optimization, that the final prediction path reads that same TRAIN-z-scored design.


## P2D staged
Issue #79 is ACTIVE / OPERATIVE. DSH must read the final activation, then prove pre-run with zero optimizer steps that the accepted final neural prediction path reads the same TRAIN-z-scored design used for training, and that clearing the design state reproduces a materially different raw fallback. Then freeze code and execute science exactly once under the retained P2C durability protocol.


## P2 complete
Issue #79 is accepted and integrated. Do not continue synthetic tuning: the neural non-gain is an accepted negative result. The next bounded task is P3A real-data evidence validation only — establish source object, year/window, population definition, OD-vs-stock-vs-transition semantics, direct/bridged target status, provenance/licence and support coverage before authorizing any empirical model fit.


## P3A staged
Issue #80 is ACTIVE / OPERATIVE. DSH must read the final activation and audit real source semantics/provenance only. It may verify public source metadata read-only if reachable, but must not download/ingest datasets or fit any empirical model. The outcome is Branch D (direct annual OD), B (bridged pair object), or P (pair target not currently supportable).
