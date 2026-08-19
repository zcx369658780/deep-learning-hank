# 深度学习 + HANK：Python 从零重建思路报告

日期：2026-08-19  
状态：THINKING ONLY / 非模型规格冻结 / 非实现授权

## 1. 新项目定位

这是一个从零开始的新研究模型项目，不是旧 Matlab 模型的 Python 翻译，也不是 Dissertation Chapter 5 R5 的继续版本。

旧多省份 HANK 只提供三类参考：

1. 经济模块候选：household HJB/KFE、生产、区域联系、名义/财政闭合；
2. 历史失败经验：隐式全局状态、`rah/inter_prv_ratio` 方向不清、旧 shock path 与 AR(1) 叙述冲突、输出 provenance 不足；
3. 测试灵感：HJB residual、KFE mass、market clearing、矩阵方向、shock limiting cases、reproducibility。

**不得继承旧数值结果作为新模型真值。**

## 2. 核心设计原则

### 2.1 Economics first, neural approximation second

深度学习不能替代经济模型的定义。必须先明确：

- household problem；
- state/control variables；
- production；
- market clearing；
- regional/spatial link；
- shock law；
- aggregate closure；
- equilibrium objects；
- welfare/measurement objects（如后续需要）。

神经网络只能在被明确定义的数学对象上承担近似、压缩、加速或求解作用。

### 2.2 新模型不要求复刻旧 Matlab

对旧机制逐项使用：

- `REUSE_CONCEPT`：经济思想可保留；
- `REDESIGN`：思想可能有用，但数学/软件表达重写；
- `DROP`：不再需要；
- `UNRESOLVED`：必须先研究，不能直接实现。

### 2.3 先小模型、后大规模

第一版只需要证明：

- 方程定义清楚；
- small-grid / small-region special case 可诊断；
- residual、mass、accounting、clearing 可计算；
- neural approximation 有独立基准和误差界面；
- 训练成功不等于经济均衡成立。

## 3. 深度学习可以进入 HANK 的四种候选位置

### 路线 A：家庭块 value/policy function approximator

用神经网络近似价值函数、政策函数或 HJB 解。

优点：

- 直接攻击高维 household block；
- 对连续状态或更多异质性维度有潜在扩展优势。

风险：

- 网络 loss 小不代表 HJB residual 在经济相关区域都小；
- borrowing boundary、monotonicity、concavity、policy feasibility 需要额外约束；
- stationary distribution 仍需严格处理。

### 路线 B：equilibrium / transition solution operator

学习从参数、aggregate state、shock path 到 equilibrium objects / transition responses 的映射。

优点：

- 适合大量反复政策实验；
- 可以与传统小规模 solver 构造训练/验证对照。

风险：

- 需要高质量训练样本；
- OOD 情况可能失真；
- 必须重新计算 equilibrium residual，而不能只看预测误差。

### 路线 C：distribution representation / compression

使用 autoencoder、set/graph representation 或其他 latent representation 压缩高维 distribution state。

优点：

- 有可能降低区域 × household distribution 的维度。

风险：

- latent state 的经济解释弱；
- mass/non-negativity/moments 可能被破坏；
- 应作为后续扩展，不建议第一阶段直接作为唯一状态表示。

### 路线 D：surrogate / accelerator

先有可验证的小规模经典 solver，再让网络近似昂贵步骤、初值或参数到解的映射。

优点：

- 最容易建立可信 benchmark；
- 可以定量证明速度提升与精度损失；
- 风险最低。

**当前推荐：以 D 为安全起点，同时把 A/B 作为真正的研究创新候选。**
最终选哪条必须由 DLH-0 scientific specification gate 冻结。

## 4. 推荐的软件架构（只到思路，不写代码）

建议未来仓库结构：

    src/deep_learning_hank/
        economics/
            parameters
            grids
            household
            distribution
            firms
            regional_links
            market_clearing
            shocks
        solvers/
            steady_state
            transition
        neural/
            architectures
            objectives
            constraints
            datasets
            trainers
        diagnostics/
            economic_residuals
            numerical_checks
            neural_validation
        experiments/
        provenance/

关键原则：

- economics 与 neural 分层；
- neural model 不直接拥有经济定义 authority；
- diagnostics 独立于 trainer；
- 所有 run 使用 immutable config + source identity + no-overwrite output root。

## 5. 冲击过程

旧 R5 选择 genuine AR(1) + one-innovation conditional IRF 是一个较好的历史设计原则，但**新项目尚未冻结该选择**。

建议 DLH-0 至少比较：

- AR(1) aggregate productivity / policy shock；
- common shock + province exposure；
- region-specific shocks；
- conditional IRF 与 stochastic realization 的用途差异。

如果继续使用 AR(1)，必须明确变量、频率、均值、`rho`、`sigma`、innovation normalization 和区域 exposure，而不是只生成一个指数衰减数组。

## 6. 多省份 / spatial link 的重新设计

历史 `rah/inter_prv_ratio` 可以提供“跨省资产收益联系”的思想，但新模型不应复制其隐式实现。

建议在规格阶段显式定义一个或多个矩阵：

- `W_asset`：资产/资本 exposure；
- `W_labor`：劳动力或流动摩擦（如模型确需）；
- `W_trade`：贸易/需求联系（如模型确需）。

每个矩阵必须分别定义：

- row/column economics；
- diagonal；
- normalization；
- non-negativity / sign restrictions；
- data construction；
- whether exogenous/endogenous；
- accounting identity；
- 与 shock exposure 的区别。

不要为了“Spatial HANK”这个名字把所有空间机制一次性塞进去。

## 7. 推荐阶段路线

### DLH-0 — Scientific constitution

只做规格：研究问题、最小模型、DL 的确切角色、变量、方程、区域机制、shock、validation strategy。

### DLH-1 — Read-only legacy/reference extraction

从两个只读参考目录提取：

- 需要阅读的 Matlab source；
- 论文笔记；
- 参数定义或方程说明；
- 只复制到新项目 `references/local_imports/`。

不运行旧模型。

### DLH-2 — Transparent economic baseline

建立最小、可诊断的经济核心和 special cases。此阶段是否需要经典 numerical solver 由 DLH-0 冻结。

### DLH-3 — Neural method specification

冻结：network 输入输出、loss、economic residual、constraints、training-data provenance、train/validation/test split、OOD test。

### DLH-4 — Small neural prototype

只做小规模、可审计实验；不得直接跑 31 省全尺度。

### DLH-5 — Economic consistency validation

必须同时检查预测误差和经济误差：HJB/KFE/clearing/accounting/boundary/mass。

### DLH-6 — Transition / conditional experiment

在 steady-state 与 neural validation 接受后进入动态实验。

### DLH-7 — Scaling and robustness

扩大 grid/region/horizon；profiling；必要时 GPU；sensitivity/OOD。

### DLH-8 — Research results

只有前述 gates 通过后才生成可写论文的 figures/tables/results claims。

## 8. 第一阶段不要做的事

- 不从旧 Matlab 输出制作监督学习标签。
- 不逐行翻译 `.m`。
- 不直接训练 31 省大模型。
- 不先决定“用 Transformer/GNN/PINN”再找经济问题。
- 不把 training loss 当 equilibrium residual。
- 不把 GPU 跑通当科学验证。
- 不写 Results 或政策结论。

## 9. DLH-0 最需要回答的科学问题

1. 新论文的核心问题是什么？
2. 深度学习究竟解决 HANK 的哪个 computational bottleneck？
3. household heterogeneity 最少保留哪些维度？
4. 多省份联系最少需要哪一种？
5. 需要真正动态 distribution transition，还是先做 steady state + conditional response？
6. neural method 的 ground truth / benchmark 从哪里来？
7. 如何在没有旧输出 oracle 的情况下验证？
8. 哪些结果必须满足解析或数值 special cases？
9. 论文创新来自经济机制、数值方法，还是二者结合？

## 10. 当前结论

最值得继承的不是旧代码，而是它暴露出来的经济模块和失败模式。

新项目的目标应是：**建立一个经济方程透明、区域联系显式、神经近似可诊断、训练与均衡验证分离、能够逐阶段扩展的 Deep Learning + HANK research platform。**
