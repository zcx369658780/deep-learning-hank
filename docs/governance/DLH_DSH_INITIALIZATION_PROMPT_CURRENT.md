# DSH 短启动入口

当前阶段只同步，不运行科学任务。详细要求见 `DLH_DSH_SYNC_ONLY_PROTOCOL_CURRENT.md`。

Owner 更新项目源后使用：

```text
接续 zcx369658780/deep-learning-hank，仅做 SYNC_ONLY。fresh-fetch origin/main，先读 AGENTS.md 和 docs/governance/DLH_DSH_SYNC_ONLY_PROTOCOL_CURRENT.md，再按其顺序读取并核验 DLH-WL-V1-20260918 路线锁。保留本地未提交内容；不读邻近项目，不改代码，不跑 pytest/HJB/KFE/GE/训练，不创建任务或提交。回报 SHA、锁/文件同步、项目源确认状态及实际零科学调用，随后 STOP。
```

未来科学任务的 prompt 只负责指定仓库、具体 active Issue、fresh-read、执行与回报。科学细节放 Issue；不使用其他项目的 `/background` 约定。
