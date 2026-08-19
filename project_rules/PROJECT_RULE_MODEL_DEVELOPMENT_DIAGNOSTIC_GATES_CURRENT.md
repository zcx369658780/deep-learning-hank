# Deep Learning + HANK 模型开发与诊断门禁

最后更新：2026-08-19

## Gate 顺序

1. `DLH-0` Scientific constitution / scope freeze
2. `DLH-1` Legacy & literature read-only reference inventory
3. `DLH-2` Transparent economic baseline / special cases
4. `DLH-3` Neural method specification
5. `DLH-4` Small neural prototype
6. `DLH-5` Economic + neural validation
7. `DLH-6` Transition / conditional experiment
8. `DLH-7` Scaling / robustness / performance
9. `DLH-8` Results eligibility / manuscript evidence

任何 PASS 不自动授权下一 gate。

## DLH-0

必须冻结：研究问题、HANK 最小结构、深度学习的 exact role、state/control、regional link、market clearing、shock、benchmark、validation、software boundary。

禁止写 solver、训练网络、跑模型。

## DLH-1

只读收集旧代码/论文笔记。所有导入 reference 有 manifest/hash。不得运行旧 Matlab。

## DLH-2

建立可诊断经济基线或 analytic/special-case benchmark。必须能计算至少：

- relevant equation residuals；
- distribution mass/non-negativity（如适用）；
- market/accounting identities；
- deterministic reproducibility。

## DLH-3

冻结 neural inputs/outputs、architecture family、objective、economic constraints、training data provenance、split、OOD test、baseline。

## DLH-4

仅 small problem。训练成功必须同时输出 neural metrics 与 economic diagnostics。

## DLH-5

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

## DLH-6/7

进入 transition/full-region/scaling 前必须单独授权 exact config, command, device, timeout, output root, retry policy。默认 no-overwrite、failure no automatic retry。

## DLH-8 Results

只有 accepted diagnostics + human review 才可提升到 D3/D4 candidate evidence。正式 Results prose、政策结论、省份排名、福利比较必须单独 gate。
