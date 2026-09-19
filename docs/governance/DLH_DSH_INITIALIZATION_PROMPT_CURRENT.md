# DSH 短启动入口

当前候选科学任务：Issue #79 / DLH-WL-P2D。
路线：`DLH-WL-V1-20260918`。

在 Reviewer final activation comment 发布前，#79 为 STAGED / NOT OPERATIVE，不得执行。

final activation 后使用：

```text
接续 zcx369658780/deep-learning-hank，执行 GitHub Issue #79。fresh-fetch origin/main，读取 AGENTS.md、Task Index、路线锁、#75 frozen contract/config、#76/#77/#78 accepted Gate Fail evidence，以及 #79 full body/comments。确认 final activation、operative baseline 与 branch。严格按 #79：保留 P2C durable-output protocol，只修复 neural preprocessing state propagation（universe._design_matrix = design）；先用 zero-fit focused tests 证明最终 prediction path 使用 TRAIN-z-scored design，并用 raw-fallback negative control 证明测试能抓住 #78 缺陷；之后 commit+push PRE_RUN_FREEZE，再从 exact SHA clean detached worktree 仅执行一次 science invocation。每个 FIT_COMPLETED 继续持久化 full predictions + metadata；science 后只允许 zero-fit render。不得第二次 science run、不得改 #75 scientific design/accepted scientific module、不调参、不用真实数据/HJB/KFE/GE/MATLAB/full suite。完成后 commit+push final artifacts，留一次 completion comment并 STOP。
```

聊天 prompt 不扩大 Issue authority。
