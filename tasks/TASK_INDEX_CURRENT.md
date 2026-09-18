# 当前任务指针

更新：2026-09-18。路线：`DLH-WL-V1-20260918`。
状态：`P1A_ACCEPTED__P1B_NEXT_DESIGN_GATE_PENDING`。

Issue #74 / DLH-WL-P1A：**ACCEPTED / CLOSED / INTEGRATED**。
- accepted candidate / integration: `d34f00a31e8d23dd8134b9e9ba1be0319e7901bc`
- Reviewer acceptance comment: `5731836951`
- acceptance integration comment: `5731840451`
- terminal: `DLH_WL_P1A_OFFLINE_ACCOUNTING_INTERFACE_AND_HOUSEHOLD_REGISTRY__PASS`

P1A 已建立：
- 冻结家庭依赖 evidence registry（无新增 solved-checkpoint claim）；
- 独立离线 `W -> P -> F -> Ldest` 核算接口；
- support mask / 方向 / 守恒 / wage-bill / 退化情形 tiny checks；
- `conditional_choice_identified` 仅在至少一个正劳动 active row 有 >=2 个结构可用外省目的地时为真。

P1 尚未全部完成。下一 gate 是 P1B：数据/标签口径、canonical sample schema 与 P2 离线实验合同设计。现实年度 bilateral OD flow labels 仍未由本项目现有证据证明可用；不得因此伪造标签，也不得回到 selected-Q solver 主线。

当前科学 Builder Issue：**NONE**（待 Reviewer 发布 P1B）。

P2 neural training、HJB/KFE/GE、MATLAB、policy/welfare 仍未授权。
