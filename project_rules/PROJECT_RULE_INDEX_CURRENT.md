# Deep Learning + HANK 项目规则总入口

最后更新：2026-08-19

读取顺序：

1. `PROJECT_RULE_INDEX_CURRENT.md`
2. `PROJECT_RULE_OVERVIEW_CURRENT.md`
3. `PROJECT_RULE_DSH_GITHUB_WORKFLOW_CURRENT.md`
4. `PROJECT_RULE_DSH_LOCAL_READONLY_REFERENCE_ACCESS_CURRENT.md`
5. `PROJECT_RULE_MODEL_DEVELOPMENT_DIAGNOSTIC_GATES_CURRENT.md`
6. `PROJECT_RULE_RESEARCH_EVIDENCE_AND_CITATION_CURRENT.md`
7. `PROJECT_RULE_ACCEPTANCE_LEVELS_CURRENT.md`
8. 当前 active GitHub Issue。

## 硬边界

- 新项目从零设计，不是 Matlab line-by-line port。
- DSH 对两个 legacy source roots 仅有只读权限。
- legacy source/output 不自动具有新模型 authority。
- GitHub Issue 是 sole Builder task authority；Task Index 只能指向它，不能扩大它。
- planning 不授权 implementation；implementation 不授权 run；run 不授权 Results。
- GitHub public repository 不得提交私有论文笔记、Zotero PDF、raw/private/purchased data、旧 Matlab 大输出、credentials。
- ChatGPT 独立验收后才进入下一科学 gate。
