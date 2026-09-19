# DSH 短启动入口

当前候选科学任务：Issue #76 / DLH-WL-P2A。
路线：`DLH-WL-V1-20260918`。

在 Reviewer final activation comment 发布前，#76 为 STAGED / NOT OPERATIVE，不得执行。

final activation 后使用：

```text
接续 zcx369658780/deep-learning-hank，执行 GitHub Issue #76。fresh-fetch origin/main，读取 AGENTS.md、Task Index、路线锁、#75 frozen P2 contract/config，以及 #76 full body/comments。确认 final activation、operative baseline 与专用分支后，严格按 #76 实现 focused non-training tests，再一次性执行冻结 P2 synthetic run。不得改 #75 contract/config，不调参、不加 seed，不用真实数据/HJB/KFE/GE/MATLAB/full suite。完成后 commit+push 专用 branch，留一次 completion comment并 STOP。
```

聊天 prompt 不扩大 Issue authority。
