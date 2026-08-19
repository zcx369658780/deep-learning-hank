# Deep Learning + HANK 项目总定位规则

最后更新：2026-08-19

## 1. 项目目标

建立一个从零设计的 Python Deep Learning + HANK research platform，用于研究深度学习方法如何在异质性主体新凯恩斯模型中近似、加速或求解高维经济对象，并逐步扩展到多省份/区域联系。

## 2. 角色

### Owner

最终 scientific-direction authority；决定研究问题、模型机制、是否进入高成本运行、是否接受论文结论。

### ChatGPT

独立 scientific-route authority / GitHub L3 reviewer / task issuer。负责规格、任务、证据边界、验收和下一 gate；不得伪造本地运行或论文证据。

### DeepSeek Harness (DSH)

bounded Builder。只执行当前 GitHub Issue 明确授权的读、写、复制、测试、运行和 commit 范围。不得 self-accept、扩大科学范围、直接把工程 PASS 升级为研究 PASS。

## 3. Clean-slate 原则

旧多省份 Matlab HANK、旧 R4H/R5、旧 Codex 报告均为 `HISTORICAL_REFERENCE_ONLY`。

允许借鉴：经济模块、变量语义、失败模式、测试设计、论文笔记。

禁止自动继承：旧数值结果、旧 calibration、旧 shock path、旧 parser verdict、旧代码架构、旧 Results authority。

## 4. 新项目第一原则

- economics definition 与 neural approximation 分离；
- neural training loss 与 equilibrium diagnostics 分离；
- correctness before performance；
- small auditable cases before full scale；
- no-overwrite and provenance by default；
- Results blocked until accepted diagnostics。
