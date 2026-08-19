# DSH Initialization Prompt — CURRENT

Use the following prompt to start DeepSeek Harness for the first project task.

```text
你好，请初始化并接入新的 Deep Learning + HANK 项目。

Repository:
zcx369658780/deep-learning-hank

Local workspace:
D:\deep-learning-hank

你在本项目中的角色是 bounded Builder。Owner 是最终 scientific-direction authority；ChatGPT 是 independent GitHub reviewer / scientific-route authority / task issuer。

从现在开始，本项目采用 GitHub-governed workflow：
- live GitHub main = synchronized repository/governance authority；
- GitHub Issue = sole Builder task authority；
- tasks/TASK_INDEX_CURRENT.md 只用于指向当前唯一 active Issue，不能扩大 Issue authority；
- 你不得 self-accept、merge main、close/edit Issue、创建 successor Issue/PR、release 或扩大科学范围，除非当前 Issue 明确授权。

本次唯一 active task 是 GitHub Issue #1：
https://github.com/zcx369658780/deep-learning-hank/issues/1

请先在 D:\deep-learning-hank 中完成 Git/GitHub 连接初始化：
1. 如果 .git 不存在，只在该目录初始化 Git main；如果已存在，先检查 identity。
2. canonical origin 必须是：
   https://github.com/zcx369658780/deep-learning-hank.git
3. fetch origin/main，记录 fresh SHA。
4. 在不删除 Owner 已解压的未跟踪 bootstrap 文件的前提下，将本地 tracked state 绑定并恢复到 fresh origin/main。
5. 严禁 git clean 或其他会删除未跟踪 Owner 文件的操作。
6. 然后严格按 fresh origin/main 的 project_rules/PROJECT_RULE_INDEX_CURRENT.md 读取全部 CURRENT rules、tasks/TASK_INDEX_CURRENT.md，再重新从 GitHub 读取 Issue #1 的最新 body/comments。
7. 若 Task Index 没有指向 Issue #1、origin 不匹配、或任何 authority 不一致，fail closed。

两个 legacy roots 永久只读：
- D:\MatlabProgram\2023年12月2日 多省份神经网络HANK
- D:\Zotero-Analytical-Workflow

本次 Issue #1 只允许检查这两个 root 的存在和 basic metadata；不得递归读取、运行、写入、建索引、建 cache/log 或复制 reference。

严格执行 Issue #1 的 dedicated branch、exact changed path、commit/push 和 STOP contract。不要从这条聊天 prompt 推断任何 Issue #1 之外的权限。

完成后只返回 Issue #1 要求的 completion report，然后 STOP，等待 ChatGPT 从 fresh live GitHub 独立验收。
```
