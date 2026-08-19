# DLH-INIT — DSH Local GitHub Bootstrap Evidence Report

- 生成日期：2026-08-19
- 生成者：DeepSeek Harness (DSH) — bounded Builder
- 依据：GitHub Issue #1（本仓库唯一 active Builder task authority）

## 1. Terminal classification

`DLH_INIT_LOCAL_GITHUB_BOOTSTRAP_READY_FOR_GPT_REVIEW`

（最终验收权在 ChatGPT，从 fresh live GitHub 独立核验；本报告不构成 self-accept。）

## 2. Issue identity

- Issue number: **#1**
- Issue title: `DLH-INIT: Bind local DSH workspace to GitHub and verify bootstrap boundaries`
- Issue state at read time: `open`（comments: 0）
- Issue URL: https://github.com/zcx369658780/deep-learning-hank/issues/1

## 3. Local root / baseline

- Local project root: `D:\deep-learning-hank`
- Fresh baseline `origin/main` SHA: `b76b424d922c19df7ef973271e02ad7e5ce404ff`
  - 对应 commit subject: `references: complete curated legacy analysis bootstrap`
  - author: `Chenxin Zhang <112786427+zcx369658780@users.noreply.github.com>`，2026-08-19 13:26:30 +0800
- Dedicated branch: `dsh/issue-1-local-github-bootstrap-2026-08-19`（从 fresh `origin/main` 创建；`main` 未被修改）
- Sanitized canonical origin URL: `https://github.com/zcx369658780/deep-learning-hank.git`
  - `remote.origin.url`（stored）与 canonical 完全一致；
  - push/fetch 传输使用本机既有 SSH key 认证（GitHub `ssh.github.com:443`），报告不含任何 token / credential 内容。

## 4. Local Git binding result

- `.git` 在任务开始时**不存在** → 已在本目录初始化，initial branch = `main`（`git init -b main`）。
- `origin` 在任务开始时不存在 → 按 Issue #1 添加唯一 canonical URL（无替换场景发生）。
- `git fetch origin main` 成功；记录 fresh SHA 如上。
- Bind 方式（Issue #1 允许的 safe mixed-reset/restore style）：
  1. `git reset origin/main`（mixed：ref + index 指向 fresh origin/main，不动 worktree）；
  2. `git checkout -- .`（将 tracked 路径的 worktree 内容恢复为 fresh origin/main；不触碰 untracked 文件）；
  3. 验证：`git diff --exit-code origin/main -- .` 输出为空，即 tracked 路径与 fresh `origin/main` 完全一致。
- **未使用 `git clean`**；未删除、未移动任何 Owner 已解压文件；未修改公共 `.gitignore`。

### 4.1 本任务开始时已解压的顶层内容（Owner 文件，原样保留）

```
design_notes/  github_seed/  historical_model_analysis/  project_rules/  tasks/
PACKAGE_SHA256SUMS.txt  PROJECT_SOURCE_MANIFEST.md  README_START_HERE.md
```

### 4.2 Local-only `.git/info/exclude` additions（精确 pattern 清单）

Issue #1 §8 允许添加本地专属 exclude pattern 以获得可用的干净 status；以下 pattern 已加入 `.git/info/exclude`（仅本地，不提交）：

```
PACKAGE_SHA256SUMS.txt
github_seed/
```

覆盖的未跟踪本地文件（来自启动包、GitHub 未跟踪，原样保留）：

- `PACKAGE_SHA256SUMS.txt`
- `github_seed/.gitignore`
- `github_seed/README.md`
- `github_seed/REPOSITORY_SETUP.md`

### 4.3 确认：tracked paths 已恢复到 fresh origin/main

在创建本证据文件**之前**，tracked 路径已恢复为 fresh `origin/main` 内容（见 §4 验证结果），此后仅新增本报告文件。

## 5. 两个只读 legacy reference roots（存在性 + 元数据 only）

Issue #1 仅授权检查存在性与 basic metadata；未做任何递归遍历、内容读取、执行或写入。

| Root | `Test-Path -PathType Container` | `Get-Item` 元数据 |
|---|---|---|
| `D:\MatlabProgram\2023年12月2日 多省份神经网络HANK` | `True` | Mode=`d----`; Attributes=`Directory`; LastWriteTime=`2026/8/10 6:53:47` |
| `D:\Zotero-Analytical-Workflow` | `True` | Mode=`d----`; Attributes=`Directory`; LastWriteTime=`2026/8/14 10:47:22` |

使用的精确只读命令（仅元数据级）：

```
Test-Path -LiteralPath '<root>' -PathType Container
Get-Item -LiteralPath '<root>' | Select-Object FullName, Mode, Attributes, LastWriteTime, Length
```

## 6. 显式 forbidden-operation 计数

| 项目 | 计数 |
|---|---|
| legacy-root writes | 0 |
| Matlab executions | 0 |
| model / Python executions | 0 |
| neural training | 0 |
| package installs | 0 |
| source / reference copy-outs | 0 |

## 7. Exact changed path list（唯一 tracked mutation）

```
docs/governance/DLH_DSH_LOCAL_GITHUB_BOOTSTRAP_REPORT_2026_08_19.md
```

- 仅显式 stage 该 allowlist 路径；未使用 `git add .` / `git add -A`。
- 仅创建一个 evidence commit；仅 push 该 dedicated branch；未创建 PR、未 merge、未 edit/close Issue、未创建 successor Issue、未 self-accept、未 release/tag。

## 8. Final worktree / staging / untracked summary

提交前状态（在添加 `.git/info/exclude` 之后）：

- worktree：干净（tracked 路径与 fresh `origin/main` 一致，`git status --short` 无输出）；
- staging：仅 `docs/governance/DLH_DSH_LOCAL_GITHUB_BOOTSTRAP_REPORT_2026_08_19.md`；
- untracked：无（本地专属 extras 已由 exclude pattern 覆盖并保留，见 §4.2）。

## 9. Forbidden-operation check

- 未执行 `git clean` 或任何 untracked 删除 / 移动；
- 未修改公共 `.gitignore`；
- 未修改 `main`（`main` 仍指向 `b76b424d922c19df7ef973271e02ad7e5ce404ff`）；
- 未在两个 legacy roots 内执行任何写 / 读内容 / 递归操作；
- 未提交 secrets、tokens、私有笔记、PDF、旧 Matlab 输出或 recursive source inventory。

## 10. Caveats

1. 本地解压包中的 8 个文件是 Issue #1 创建前的旧版 seed 内容，与 fresh `origin/main` 不同
   （例如本地 `tasks/TASK_INDEX_CURRENT.md` 为 `NO_ACTIVE_BUILDER_TASK`，而 fresh main 为 `ACTIVE_GITHUB_ISSUE_1`）。
   按 Issue #1 §7（tracked paths 必须匹配 fresh origin/main），这些路径已恢复为 origin/main 内容；
   其旧本地内容被新治理内容取代，未另存副本（Issue 未要求）。
   涉及路径：
   - `PROJECT_SOURCE_MANIFEST.md`
   - `README_START_HERE.md`
   - `historical_model_analysis/07_R5_PYTHON_AR1_REBUILD_ROADMAP_HISTORICAL_2026_07_22.md`
   - `project_rules/PROJECT_RULE_DSH_GITHUB_WORKFLOW_CURRENT.md`
   - `project_rules/PROJECT_RULE_INDEX_CURRENT.md`
   - `project_rules/PROJECT_RULE_OVERVIEW_CURRENT.md`
   - `project_rules/PROJECT_RULE_RESEARCH_EVIDENCE_AND_CITATION_CURRENT.md`
   - `tasks/TASK_INDEX_CURRENT.md`
2. fresh `origin/main` 中另有 5 个文件在本地解压包中不存在，已随 restore 物化：
   `.gitignore`、`README.md`、`docs/governance/DLH_DSH_INITIALIZATION_PROMPT_CURRENT.md`、
   `docs/governance/DLH_GITHUB_BOOTSTRAP_AUTHORITY_2026_08_19.md`、`docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`。
3. 本任务无 blocker；如 push 阶段出现认证/远程故障，classification 将改为
   `BLOCKED_PUSH_OR_REMOTE_AUTH_FAILURE` 并停止。

## 11. Recommended next gate（仅建议，不自行创建）

独立验收通过后，按 Task Index 建议的 `DLH_0_SCIENTIFIC_CONSTITUTION_AND_MODEL_SCOPE_FREEZE`
以单独 GitHub Issue 形式发布后再执行（planning/specification only）。
