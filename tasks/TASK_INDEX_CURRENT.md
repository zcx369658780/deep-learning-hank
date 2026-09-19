# 当前任务指针

更新：2026-09-19。路线：`DLH-WL-V1-20260918`。
状态：`P2B_GATE_FAIL_ACCEPTED__ISSUE_78_P2C_ACTIVE_OPERATIVE`。

Issue #74 / P1A：ACCEPTED / CLOSED / INTEGRATED。
Issue #75 / P1B：ACCEPTED / CLOSED / INTEGRATED。
Issue #76 / P2A：protocol GATE FAIL EVIDENCE ACCEPTED / CLOSED / INTEGRATED。
Issue #77 / P2B：clean-replication GATE FAIL EVIDENCE ACCEPTED / CLOSED / INTEGRATED。
- #77 integration: `e0f3b633e75ef1971e634e34a4a8143193bfe4da`
- Reviewer acceptance: `5740399591`
- integration comment: `5740401009`
- terminal: `DLH_WL_P2B_CLEAN_REPLICATION__GATE_FAIL__NO_SCIENCE_RERUN_AUTHORIZED`

下一科学 Builder Issue：
- #78 / `DLH-WL-P2C: durable per-fit-output replication of frozen synthetic prototype`
- 状态：**OPEN / ACTIVE / OPERATIVE**
- publication baseline：`f6390ccea1eee27fb6528c3ba2572551a7e8dd06`
- Builder 必须以 final activation comment 指定的 exact operative baseline 与 branch 为准。

#78 保持 #75 scientific design 不变，但把每个 FIT_COMPLETED 变成可零-fit恢复的完整科学记录：
- full predictions 持久化 + fsync；
- parametric coefficients / FitOutcome metadata 持久化；
- renderer 只从 durable ledger + frozen inputs 计算 metrics；
- pre-run fake 12-fit ledger 必须端到端通过 exact aggregation/render path；
- science invocation 恰好 1 次，12 started + 12 completed，0 retry；
- report/render 缺陷不得触发第二次 science。
