# DSH 零科学同步协议

协议：`DLH-SYNC-WL-V1-20260918`。路线：`DLH-WL-V1-20260918`。
范围：Owner 已批准三端同步后的本地读取/取得已发布文件；无科学 Issue 的狭窄 housekeeping 例外。不是科学任务或运行授权。

## 启动条件

分发模式为 `THIN_INDEX_SINGLE_FILE`；项目源只需 `DLH_PROJECT_SOURCE_ENTRY_CURRENT.md`，完整规则/路线/合同从 GitHub 读取。不再要求上一轮 25 份附件齐全，已删除的操作附件不必恢复。

Owner 确认该单入口已上传后，发送此协议的启动 prompt。若上传失败或是否完成未知，仍可先做 GitHub/local 只读同步，并将项目源确认标为 PENDING，不能宣布三端同步完成；不要求为启动读取补传所有文件。聊天中粘贴恢复句只证明本会话获得入口，不等于文件已上传或项目指令已保存。入口生成不算 Owner 确认。

## 允许操作

1. 在 `D:\deep-learning-hank` 核对 cwd、origin、branch、dirty/staged/untracked/ahead-behind；保留所有工作成果。
2. `git fetch origin`，记录 fresh origin/main。读取其根目录单入口、AGENTS、规则索引/必读规则、Owner decision、锁 manifest、Task Index、Snapshot、Roadmap、两份合同及当前交接。全部按仓库路径读取，不依赖项目源有同名附件。
3. 核验 route ID、adoption 文件与 roadmap 锁区块哈希。存在新 amendment 时要求明确 Owner 授权记录，不能自动接受仅被改过的哈希。
4. 用 `git show origin/main:<path>` 读取；或建立全新 detached worktree 指向该 SHA。原 main 干净、只落后且可快进时可 `git merge --ff-only origin/main`；不允许创建合并提交或接入本地新代码。
5. 不要求重读全部历史/所有科学源码。当前无活动科学 Issue 时确认 NONE；不能因旧 handoff 的 NEXT 自动恢复 #73。

禁止 reset --hard、git clean、强制 checkout、覆盖/删除本地文件、rebase/force push；本地分歧不能安全解决则报告并停在干净新 worktree 或只读状态。

## 零调用边界

不改任何 tracked 文件；不 commit/push/开 PR/创建 Issue。不运行 pytest/full suite、训练、HJB、KFE、GE、MATLAB、checkpoint 重建、数据或权重下载、环境升级。不以验证 hash 为由 import 科学模块。

## 回报（文本即可，不新增治理提交）

报告 pre/post local SHA、fresh origin/main、工作区/分支状态、读取文件、锁/hash 结果、分发模式 THIN_INDEX_SINGLE_FILE、Owner 对单入口的项目源确认状态、实际命令和模型/算子/训练/pytest 调用数（必须为 0）。用自己的简短表述确认：只学条件目的地份额；m/ell 不学；方向行归一；HA 默认不改；selected-Q 暂停；KFE/GE 未授权；新模型不得改 Owner 路线。

完成状态：`SYNC_ONLY_COMPLETE__AWAITING_SCIENTIFIC_ISSUE`；上传未确认则 `LOCAL_GITHUB_SYNC_COMPLETE__PROJECT_SOURCE_CONFIRMATION_PENDING`；实质冲突则 `SYNC_BLOCKED_WITH_EVIDENCE`。

完成后 STOP。此回报不是科学验收，不能自动执行 P1/P2。Reviewer 核对后再发布下一张 bounded Issue。
