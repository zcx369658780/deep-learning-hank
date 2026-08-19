# DSH 本地 Legacy Reference 只读访问规则

最后更新：2026-08-19

## 0. 明确授权的两个只读 source roots

新项目本地 DSH 被允许 **只读访问**：

1. `D:\MatlabProgram\2023年12月2日 多省份神经网络HANK`
2. `D:\Zotero-Analytical-Workflow`

授权目的仅限：收集建立新模型所需的信息，以及复制必要的程序文件、论文笔记或轻量参考材料到新项目的 reference staging area。

## 1. Source root 永久只读

DSH MUST NOT 在上述两个 source roots 内：

- 修改、覆盖、格式化、重命名、移动或删除任何文件；
- 创建新文件、cache、index、log、temporary file、virtual environment；
- 执行会产生 side effect 的脚本；
- git commit/push 或改变其 Git 状态；
- 写回 Zotero/Obsidian 数据；
- 修改 Matlab `.m` 文件或旧输出；
- 运行旧 Matlab main/model 作为默认动作。

若工具会在 source root 自动写 cache/index，必须关闭该行为或停止任务。

## 2. 允许的只读动作

在当前 task 进一步限定后，MAY：

- list/stat/hash；
- bounded text read/search；
- 读取 `.m/.py/.md/.txt/.csv/.json/.yaml/.toml` 等轻量文本；
- 读取论文笔记；
- 识别相关文件；
- 生成 source inventory；
- 从 source root **复制** 明确需要的参考文件到新项目 staging。

对 PDF、SQLite、数据库、binary model outputs、大型 Excel/`.mat` 默认不读取正文/数值，除非 future task 明确授权并说明必要性。

## 3. Copy-out 规则

允许复制不等于允许修改 source。

每次 copy-out 必须：

- 目标只能在新项目目录内；
- 优先目标：`references/local_imports/<task-or-date>/`；
- no-overwrite；
- exact allowlist；
- 记录 `source_path`, `destination_path`, `size`, `SHA256`, `reason`, `evidence_level`；
- 复制后验证 source hash 未变化；
- 不复制 secrets、credentials、Zotero SQLite、private PDFs、copyright-sensitive full-text 到公共 Git 仓库。

复制到本地 reference staging 的文件默认仍为 `REFERENCE_ONLY`，不会自动成为新模型的经济方程、参数或数值 authority。

## 4. Public GitHub 边界

`D:\Zotero-Analytical-Workflow` 中的论文笔记可能包含私有/受版权限制材料。默认：

- 本地可读、可按 task 复制到 gitignored reference staging；
- 不得直接 commit 论文全文、PDF、长摘录、private note；
- GitHub 只提交自写的摘要、source manifest、citation key、必要的短 metadata 和新的研究结论边界。

旧 Matlab 目录同样不得把 `.mat`、Excel 大输出、图表批量提交新公共仓库。

## 5. Fail closed

如果完成任务必须对两个 source roots 之一写入、运行会改变其状态、或无法证明工具是只读的，DSH 必须 STOP 并报告 `BLOCKED_READONLY_SOURCE_BOUNDARY`。
