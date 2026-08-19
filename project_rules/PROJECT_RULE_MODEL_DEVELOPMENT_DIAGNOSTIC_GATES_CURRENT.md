# Deep Learning + HANK 模型开发与诊断门禁

最后更新：2026-08-19

## 0. CURRENT stage-numbering authority / 编号消歧

本文件最初建立时，下面的 `DLH-0`～`DLH-8` 是一套 **generic diagnostic-gate labels**。项目随后在 accepted DLH-0R1 + `docs/roadmaps/DLH_MASTER_ROADMAP_INITIAL_2026_08_19.md` 中形成了新的 CURRENT project-stage roadmap。

因此从 2026-08-19 起：

- **CURRENT project stage identity 以 fresh live `main` 上的 Master Roadmap + `tasks/TASK_INDEX_CURRENT.md` + 当前 open GitHub Issue 为准；**
- 本文件下面的旧 `DLH-*` 标签只保留为 generic diagnostic-category provenance，不得覆盖 CURRENT roadmap stage identity；
- 特别是 CURRENT roadmap 中 `DLH-3` = **minimal genuine single-region HANK nominal/New-Keynesian layer**，不是下方旧 generic label 中的 “neural method specification”；
- neural-method specification / training 仍必须等待未来 CURRENT roadmap / GitHub Issue 明确授权，不能因本文件的旧编号自动启动；
- 若 generic gate label 与 CURRENT roadmap / Task Index / active Issue 冲突，Builder MUST fail closed，并以 CURRENT roadmap + Task Index + active Issue 的更具体 authority 为准，不得自行扩大 scope。

任何 PASS 不自动授权下一 gate。

## Legacy generic gate sequence — provenance only

1. `DLH-0` Scientific constitution / scope freeze
2. `DLH-1` Legacy & literature read-only reference inventory
3. `DLH-2` Transparent economic baseline / special cases
4. `DLH-3` Neural method specification
5. `DLH-4` Small neural prototype
6. `DLH-5` Economic + neural validation
7. `DLH-6` Transition / conditional experiment
8. `DLH-7` Scaling / robustness / performance
9. `DLH-8` Results eligibility / manuscript evidence

## Generic DLH-0 category

必须冻结：研究问题、HANK 最小结构、深度学习的 exact role、state/control、regional link、market clearing、shock、benchmark、validation、software boundary。

禁止写 solver、训练网络、跑模型。

## Generic DLH-1 category

只读收集旧代码/论文笔记。所有导入 reference 有 manifest/hash。不得运行旧 Matlab。

## Generic DLH-2 category

建立可诊断经济基线或 analytic/special-case benchmark。必须能计算至少：

- relevant equation residuals；
- distribution mass/non-negativity（如适用）；
- market/accounting identities；
- deterministic reproducibility。

## Legacy generic DLH-3 category — neural specification, NOT CURRENT project-stage DLH-3

冻结 neural inputs/outputs、architecture family、objective、economic constraints、training data provenance、split、OOD test、baseline。

本节当前不构成 neural Builder authority。CURRENT project-stage `DLH-3` 的含义由 Master Roadmap / Task Index / active Issue 决定。

## Generic DLH-4 category

仅 small problem。训练成功必须同时输出 neural metrics 与 economic diagnostics。

## Generic DLH-5 category

至少检查：

- train/validation/test error；
- equilibrium residuals；
- boundary feasibility；
- mass/accounting/clearing；
- limiting/special cases；
- reproducibility；
- OOD/sensitivity；
- benchmark comparison。

仅 loss 降低、GPU 成功、pytest PASS、figure produced 均不足以构成 scientific PASS。

## Generic DLH-6/7 categories

进入 transition/full-region/scaling 前必须单独授权 exact config, command, device, timeout, output root, retry policy。默认 no-overwrite、failure no automatic retry。

## Generic DLH-8 Results category

只有 accepted diagnostics + human review 才可提升到 D3/D4 candidate evidence。正式 Results prose、政策结论、省份排名、福利比较必须单独 gate。
