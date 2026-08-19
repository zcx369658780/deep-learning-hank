# Deep Learning + HANK

> A governed research project for building and validating deep-learning methods for heterogeneous-agent New Keynesian models from first principles.

## 项目定位

本仓库用于从零设计一个 **Deep Learning + HANK** Python research platform。目标不是逐行翻译旧 Matlab，也不是复刻历史数值结果，而是研究深度学习如何在可解释、可诊断的 HANK / HA-NK 经济结构中承担近似、加速或求解任务，并逐步扩展到多省份/区域联系。

当前阶段：**project bootstrap / scientific specification 尚未冻结 / no model code yet**。

## 研究原则

- Economics first; neural approximation second.
- Clean-slate implementation; legacy Matlab is reference only.
- Training loss is not equilibrium validation.
- Small auditable cases before large-scale experiments.
- No old output is a numerical oracle by default.
- Results remain blocked until numerical and economic diagnostics pass.

## 历史参考

旧多省份 Matlab HANK 曾包含：

- continuous-time household HJB block；
- stationary distribution / KFE-style solve；
- two-asset household states；
- province-level production / pricing / fiscal objects；
- cross-province labor and asset-return links；
- outer multi-province fixed-point controller。

这些内容只用于帮助提出新模型的候选模块。旧 calibration、shock path、parser/runtime result 和 model outputs 不具有本仓库的 numerical authority。

## DSH 本地只读参考源

DeepSeek Harness 可在明确 task 下只读访问：

- `D:\MatlabProgram\2023年12月2日 多省份神经网络HANK`
- `D:\Zotero-Analytical-Workflow`

允许目的：收集必要信息，并将必要的程序文件/论文笔记复制到本地 gitignored reference staging。

**严禁对两个 source roots 写入、覆盖、删除、重命名或产生 cache/log。**

## 推荐研究路线

1. DLH-0 — Scientific constitution and scope freeze
2. DLH-1 — Read-only legacy/literature reference inventory
3. DLH-2 — Transparent economic baseline / special cases
4. DLH-3 — Neural method specification
5. DLH-4 — Small neural prototype
6. DLH-5 — Economic + neural validation
7. DLH-6 — Transition / conditional experiment
8. DLH-7 — Scaling / robustness
9. DLH-8 — Results eligibility and manuscript evidence

## Governance

- live GitHub `main` = synchronized governance authority；
- GitHub Issue = sole Builder task authority；
- `tasks/TASK_INDEX_CURRENT.md` = synchronized active-task pointer；
- DSH = bounded Builder；
- ChatGPT = independent reviewer / scientific-route authority / task issuer；
- Owner = final scientific-direction authority；
- each Builder completion is independently reviewed from fresh live GitHub before merge/next scientific gate。

See `project_rules/`, `tasks/`, and `docs/governance/`.

## Data / references / outputs

This is intended to be a public repository. Do **not** commit:

- Zotero PDFs or database files；
- private/full-text research notes；
- purchased/raw/private data；
- legacy Matlab `.mat` / Excel output dumps；
- model checkpoints or large runtime outputs；
- credentials / tokens / `.env`。

Local reference imports and large outputs must remain gitignored and be represented in GitHub only by safe manifests/summaries when needed.

## License

No open-source license is selected at bootstrap. The owner should choose a license deliberately before external reuse is invited.
