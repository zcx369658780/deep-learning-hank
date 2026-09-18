# DSH + GitHub 工作流

更新：2026-09-18。路线：`DLH-WL-V1-20260918`。

## 科学任务

Owner 决定科研方向；ChatGPT 独立审查并发布任务；DSH 有界执行。科学 source/test/config 修改、训练、模型调用均须一个明确 open Issue 及权威 activation。Task Index 是指针，不能扩大 Issue 或 Owner 授权。planning 不等于 implementation，implementation 不等于 run，run 不等于 Results。

启动：核对 `D:\deep-learning-hank`、origin、分支和 dirty 状态；fresh-fetch；读取 fresh main 上 AGENTS/规则/锁定决定/Task Index/Snapshot/Roadmap/相关合同；有活动 Issue 时读取 full body/comments，并确认任务与路线一致。

## 唯一无科学 Issue 的同步例外

Owner 本轮已批准先同步三端再开工。按 `docs/governance/DLH_DSH_SYNC_ONLY_PROTOCOL_CURRENT.md` 做 SYNC_ONLY，可 fetch、读已发布文件、静态 hash、建立新 detached worktree；干净且可快进的本地 main 可仅快进到已发布 origin/main。该例外不允许生成新提交、写 scientific source/test/config、训练、HJB/KFE/GE、pytest 或下载数据/权重，不允许远端写操作。

这是本地取得已发布提交，不是 DSH 集成自己的代码到 main。不存在活动科学 Issue 时，同步完就停止，不从旧 Issue 推导下一任务。

## 执行与验收

每个科学 Issue 有专用分支和明确 allowed paths；只显式 stage，不用 `git add .`/`git add -A`。不覆盖旧产物，不改参考根目录，不提交私有 PDF/raw data/笔记/凭据。

DSH 不得 self-accept、擅自 PR/merge/tag、关闭/重开/创建 successor Issue。完成后报 baseline、candidate、changed paths、预算/实际调用、检查证据、限制并 STOP。Reviewer fresh-read commit/diff/产物后才能验收。

科学 mismatch：暂停受影响科学任务。普通过期指针/路径合同：局部同步或 bounded repair，不升级小时级 scientific blocker。检查范围按测试成本规则，不默认 full suite。

Owner 路线锁优先于过期历史任务中“下一步”的指示；新 Issue 无权暗改锁定内容。
