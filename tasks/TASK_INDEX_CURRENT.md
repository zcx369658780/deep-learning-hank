# 当前任务指针

更新：2026-09-19。路线：`DLH-WL-V1-20260918`。
状态：`P1_COMPLETE__ISSUE_76_P2A_ACTIVE_OPERATIVE`。

Issue #74 / P1A：ACCEPTED / CLOSED / INTEGRATED。
Issue #75 / P1B：ACCEPTED / CLOSED / INTEGRATED。
- P1B integration: `e1b83b3d5b2c04d7e9052ad614e95631abb03dc6`
- Reviewer acceptance: `5739889010`
- integration comment: `5739889903`

下一科学 Builder Issue：
- #76 / `DLH-WL-P2A: implement and execute frozen offline synthetic prototype`
- 状态：**OPEN / ACTIVE / OPERATIVE**
- publication baseline：`2750bf416b9d3034a5f77792c17e0bc59571aae8`
- Builder 必须以 final activation comment 指定的 exact operative baseline 与 branch 为准。

#76 是第一张真正运行小型训练的 P2 Issue，但只能执行 #75 已冻结的合同：
- synthetic S0/S1；
- fixed / 6-parametric / small-neural 三基准；
- split 9/3/2/6；
- 8 primary configs / 12 planned executions / <=13 attempts / <=1800s；
- no hyperparameter/seed search；
- no real data / HJB / KFE / GE / MATLAB；
- neural 不要求胜过 parametric；负结果可以是 PASS。

split 的唯一允许解释是 held-out time + held-out origin role；不得声称 unseen-region。
