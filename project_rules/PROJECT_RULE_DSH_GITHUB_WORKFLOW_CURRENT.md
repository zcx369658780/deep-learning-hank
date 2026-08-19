# DSH + GitHub Governed Workflow

最后更新：2026-08-19

## 1. Authority hierarchy

本项目正式采用 GitHub-governed workflow：

- live GitHub `main` = 唯一 synchronized repository/governance authority；
- **open GitHub Issue = sole Builder task authority**；
- `tasks/TASK_INDEX_CURRENT.md` = active Issue pointer / synchronization aid，不能扩大 Issue authority；
- DSH = bounded Builder；
- ChatGPT = independent GitHub reviewer / scientific-route authority / task issuer；
- Owner = final scientific-direction authority。

聊天中的 prompt 只负责启动 DSH 去读取指定 GitHub Issue；聊天文字本身不得扩大 Issue 中 committed/published 的 authority。

若 Issue、Task Index、`main` 或 prompt 之间出现 scope/identity mismatch，DSH 必须 fail closed。

## 2. 每次 DSH task startup

每个任务开始必须：

1. `Set-Location D:\deep-learning-hank`；
2. 确认当前目录、`.git`、remote 和 worktree 状态；
3. `git fetch origin`；
4. 记录 fresh `origin/main` SHA；
5. 读取 fresh `origin/main` 上：
   - `project_rules/PROJECT_RULE_INDEX_CURRENT.md`；
   - 规则索引要求的全部 CURRENT rules；
   - `tasks/TASK_INDEX_CURRENT.md`；
6. 从 GitHub 读取 Task Index 指向的唯一 active Issue 的**最新 authoritative body/comments**；
7. 确认 Issue number/title/status 与 Task Index 一致；
8. 在任何 mutation 前检查 worktree dirty state 与 branch identity。

不得根据旧聊天记忆、旧本地文件或 Builder 自己保存的 task copy 推断 current authority。

## 3. Builder 禁止事项

未经当前 GitHub Issue 明确授权，DSH 不得：

- 创建、编辑、关闭、reopen successor Issue；
- self-accept / mark Ready / mark scientific PASS；
- merge 到 `main`；
- 创建 PR（除非 Issue 明确授权）；
- release/tag；
- 删除历史 evidence；
- 扩大 model mechanisms / calibration / data scope；
- 运行 full-scale model；
- 进入 Results prose；
- 修改两个只读 legacy source roots；
- 把本地私有 references、PDF、数据库、raw/private data、checkpoints、secrets 提交公共 GitHub。

正确的 fail-closed `BLOCKED` 可以是有效 completion，但仍须 ChatGPT 独立验收。

## 4. Branch / commit discipline

除非 Issue 另有说明：

- 一个 Issue 对应一个 dedicated bounded branch；
- branch name 应含 task/issue identity；
- `main` 不由 DSH 修改；
- 禁止 `git add .` / `git add -A`；
- 只显式 stage Issue allowlist path；
- commit 前后报告 changed paths、status、ahead/behind 和 candidate SHA；
- push 仅推 dedicated branch；
- DSH completion 后 STOP，等待 ChatGPT fresh GitHub review。

## 5. Completion report minimum

DSH completion 必须报告：

- terminal classification；
- GitHub Issue number/title；
- refreshed baseline `origin/main` SHA；
- branch / candidate commit SHA；
- exact changed paths；
- files read / copied / written；
- tests/checks and commands relevant to acceptance；
- source-root readonly check；
- forbidden-operation check；
- known caveats / blockers；
- recommended next gate（仅建议，不自行创建）。

Builder 的 completion summary 不是验收证据。ChatGPT 必须从 fresh live GitHub 独立读取 Issue、candidate commit/diff/evidence 后，才可决定 ACCEPT/BLOCKED_ACCEPTED、merge、close Issue 或发布 successor Issue。
