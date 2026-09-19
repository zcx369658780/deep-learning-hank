# 当前任务指针

更新：2026-09-19。路线：`DLH-WL-V1-20260918`。
状态：`P2C_GATE_FAIL_ACCEPTED__ISSUE_79_P2D_ACTIVE_OPERATIVE`。

Issue #74 / P1A：ACCEPTED / CLOSED / INTEGRATED。
Issue #75 / P1B：ACCEPTED / CLOSED / INTEGRATED。
Issue #76 / P2A：protocol GATE FAIL EVIDENCE ACCEPTED / CLOSED / INTEGRATED。
Issue #77 / P2B：clean-replication GATE FAIL EVIDENCE ACCEPTED / CLOSED / INTEGRATED。
Issue #78 / P2C：scientific-execution GATE FAIL EVIDENCE ACCEPTED / CLOSED / INTEGRATED。
- #78 integration: `0758daccfe5b207e1dfaaae976559e3f2adc7a6e`
- Reviewer acceptance: `5740815958`
- integration comment: `5740817339`
- terminal: `DLH_WL_P2C_DURABLE_OUTPUT_REPLICATION__GATE_FAIL__NO_SCIENCE_RERUN_AUTHORIZED`

下一科学 Builder Issue：
- #79 / `DLH-WL-P2D: minimal preprocessing-corrected durable replication`
- 状态：**OPEN / ACTIVE / OPERATIVE**
- publication baseline：`4ae19abc9e951e2d4803a1239bb411f7a8798009`
- Builder 必须以 final activation comment 指定的 exact operative baseline 与 branch 为准。

#79 保持 #75 scientific design 不变，保留 #78 已验证的 durable per-fit-output protocol。
唯一 science-path 修复：
`universe._design_matrix = design`
必须在 neural fit 前设置，使训练、early stopping 和最终 prediction 使用同一 TRAIN-only z-scored design。

pre-run 必须有 zero-fit prediction-path negative-control test，能够在缺失该 assignment 时失败。
