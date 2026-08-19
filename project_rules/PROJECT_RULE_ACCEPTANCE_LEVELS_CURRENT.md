# GitHub / Local 验收等级规则（DSH 项目）

最后更新：2026-08-19

## L0 — CHAT_ONLY

只有 DSH/用户文字回复。允许说“Builder 声称完成”；不得声称 repo/commit/test 已独立核验。

## L1 — LOCAL_ARTIFACT_ONLY

有本地 artifact、日志或截图，但未从 GitHub 独立读取。

## L2 — REPO_FILE_VERIFIED

ChatGPT 从 live GitHub 独立读取了相关文件，文件内容支持 verdict。

## L3 — COMMIT_OR_PR_VERIFIED

ChatGPT 独立核验 candidate commit/PR、changed paths、baseline/merge-base/scope，确认变化落在 task authority 内。

## L4 — CI_OR_TEST_VERIFIED

在 L3 基础上，独立读取可信 CI/test artifact，且检查与 task acceptance criteria 相关。

## 科研结论额外边界

L4 也不等于模型经济学有效。工程验收必须与科研 evidence level 分离。

- source mapping / static diagnostics 可以是 D1；
- machine numerical diagnostics 可以是 D2；
- 人工审阅并确认可解释结果才可能进入 D3；
- 投稿级复现、稳健性和 provenance 才可能进入 D4。

Builder 不得 self-promote acceptance level。最终 acceptance level 由独立 reviewer 根据实际读取证据给出。
