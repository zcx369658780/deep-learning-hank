# 当前任务指针

更新：2026-09-19。路线：`DLH-WL-V1-20260918`。
状态：`P2C_GATE_FAIL_ACCEPTED__P2D_MINIMAL_CORRECTED_REPLICATION_NEXT`。

Issue #74 / P1A：ACCEPTED / CLOSED / INTEGRATED。
Issue #75 / P1B：ACCEPTED / CLOSED / INTEGRATED。
Issue #76 / P2A：protocol GATE FAIL EVIDENCE ACCEPTED / CLOSED / INTEGRATED。
Issue #77 / P2B：clean-replication GATE FAIL EVIDENCE ACCEPTED / CLOSED / INTEGRATED。
Issue #78 / P2C：**scientific-execution GATE FAIL EVIDENCE ACCEPTED / CLOSED / INTEGRATED**。
- integration: `0758daccfe5b207e1dfaaae976559e3f2adc7a6e`
- Reviewer acceptance: `5740815958`
- integration comment: `5740817339`
- terminal: `DLH_WL_P2C_DURABLE_OUTPUT_REPLICATION__GATE_FAIL__NO_SCIENCE_RERUN_AUTHORIZED`

#78 established:
- durable-output / single-science-invocation protocol is now accepted as correct;
- 12 completed fits were durably persisted with full prediction tensors;
- neural prediction path violated the frozen TRAIN-only preprocessing contract because the runner omitted `universe._design_matrix = design`;
- neural metrics are audit-only invalid-path evidence; parametric outputs remain frozen-design conformant;
- no confirmatory P2 PASS exists yet.

Current scientific Builder Issue：NONE。
Next gate: one minimal corrected P2 replication under the unchanged #75 design. The only science-path repair is explicit propagation of the TRAIN-z-scored design into `universe.design_matrix` before neural fitting/prediction; #78 durable per-fit-output machinery is retained.
