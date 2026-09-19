# DSH 短启动入口

当前候选科学任务：Issue #77 / DLH-WL-P2B。
路线：`DLH-WL-V1-20260918`。

在 Reviewer final activation comment 发布前，#77 为 STAGED / NOT OPERATIVE，不得执行。

final activation 后使用：

```text
接续 zcx369658780/deep-learning-hank，执行 GitHub Issue #77。fresh-fetch origin/main，读取 AGENTS.md、Task Index、路线锁、#75 frozen contract/config、#76 gate-fail evidence，以及 #77 full body/comments。确认 final activation、operative baseline 与 branch。严格按 #77：先实现 science runner / render-only / focused zero-fit tests，commit+push PRE_RUN_FREEZE；再从该 exact SHA 的 clean detached worktree 仅执行一次 --execute-science，写 durable ledger + immutable raw results；之后只用 --render-only 生成结果。不得第二次 science run，不得改 #75/#76 scientific module，不调参、不用真实数据/HJB/KFE/GE/MATLAB/full suite。完成后 commit+push final artifacts，留一次 completion comment并 STOP。
```

聊天 prompt 不扩大 Issue authority。
