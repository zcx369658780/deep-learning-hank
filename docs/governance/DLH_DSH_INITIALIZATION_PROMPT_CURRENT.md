# DSH 短启动入口

当前候选科学任务：Issue #78 / DLH-WL-P2C。
路线：`DLH-WL-V1-20260918`。

在 Reviewer final activation comment 发布前，#78 为 STAGED / NOT OPERATIVE，不得执行。

final activation 后使用：

```text
接续 zcx369658780/deep-learning-hank，执行 GitHub Issue #78。fresh-fetch origin/main，读取 AGENTS.md、Task Index、路线锁、#75 frozen contract/config、#76/#77 accepted gate-fail evidence，以及 #78 full body/comments。确认 final activation、operative baseline 与 branch。严格按 #78：先实现 science runner / zero-fit renderer / focused tests，并用 fake 12-fit completed ledger 端到端跑通 exact aggregation/render path；之后 commit+push PRE_RUN_FREEZE。再从该 exact SHA 的 clean detached worktree 仅执行一次 science invocation。每个 FIT_COMPLETED 必须携带 full predictions + FitOutcome metadata，fsync 后才可开始下一 fit。science 后只允许 zero-fit render；不得第二次 science run，不得改 #75 scientific design 或 accepted scientific module，不调参、不用真实数据/HJB/KFE/GE/MATLAB/full suite。完成后 commit+push final artifacts，留一次 completion comment并 STOP。
```

聊天 prompt 不扩大 Issue authority。
