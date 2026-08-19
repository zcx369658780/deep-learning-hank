# Deep Learning Regional HANK — 初版 Master Roadmap

**版本**：V0.1  
**日期**：2026-08-19  
**项目**：Deep Learning + HANK / Network-Structured Regional HANK  
**Repository**：`zcx369658780/deep-learning-hank`  
**本地工作区**：`D:\deep-learning-hank`  
**状态**：INITIAL ROADMAP / SCIENTIFIC ROUTE AUTHORITY CANDIDATE FOR IMPLEMENTATION  
**治理**：GitHub Issue = sole DSH Builder task authority；ChatGPT = independent reviewer / scientific-route authority / task issuer；Owner = final scientific-direction authority。

---

## 0. 项目核心目标

本项目不再把“深度学习 + HANK”理解为“用神经网络替代 HJB 求解器”。

第一代模型的核心目标是：

> **保留省内 household / firm / HJB / KFE / market-clearing 等结构经济学方程，把省际劳动力、资本和财政联系表示为可解释、可训练、可验证的网络权重；网络参数通过真实流量数据和全国一般均衡共同约束。**

长期目标是形成一个可扩展的 **Network-Structured Regional HANK（NSR-HANK）**：

\[
\text{Regional structural modules}
\rightarrow
\text{learned interregional flow networks}
\rightarrow
\text{national market clearing}
\rightarrow
\text{regional prices}
\rightarrow
\text{regional structural modules}.
\]

一般均衡写成固定点：

\[
X_t^*(\theta)=T\!\left(X_t^*(\theta);\theta,Z_t\right),
\]

其中：

- \(X_t^*\)：第 \(t\) 年全国各区域的均衡 household / distribution / output / wage / return / labor / capital / fiscal objects；
- \(\theta\)：跨年份共享的 learned-network structural parameters；
- \(Z_t\)：第 \(t\) 年的区域和省际可观测特征；
- 旧 Matlab / 旧模型输出不作为新模型 numerical oracle。

---

# 1. 已冻结的第一代科学设计原则

## 1.1 省内结构经济模块保持“硬结构”

第一代不让神经网络替代以下经济学定义：

- household optimization；
- HJB；
- KFE / stationary distribution；
- household budget constraint；
- firm production / FOC；
- market clearing；
- accounting identities；
- minimal HANK nominal block（进入真正 HANK gate 后）；
- fiscal accounting。

神经网络的第一职责是学习**区域之间的连接机制**，而不是重新发明省内经济学。

## 1.2 第一代 learned object：流量权重，不是抽象 message

第一代优先学习：

- \(W_t^L\)：劳动力跨省配置网络；
- 后续 \(W_t^K\)：资本跨省配置网络；
- 后续财政模块 \(W_t^G\)：中央财政资源分配/转移规则。

Message passing / GNN / attention 保留为高级扩展，不作为 baseline。

## 1.3 第一代人口处理：home region 固定

第一代采用：

> **劳动服务可以跨省配置，但 household 的 home-region identity 暂时固定。**

因此河南 household 可以向广东提供劳动，但 household distribution 仍记在河南。

暂不处理：

- household 永久迁移；
- 户籍改变；
- housing choice；
- household distribution 从一个省直接转移到另一个省。

这些属于后续扩展。

## 1.4 Python 为唯一主实现语言

新模型主程序采用 Python。

既有单省 Python HJB + firm iteration 代码是**候选可复用计算内核**，但必须先经过：

- provenance 审计；
- equation / closure 审计；
- input/output contract；
- deterministic fixture；
- HJB residual；
- KFE mass / non-negativity；
- firm identity；
- removal of legacy global state。

通过后才迁入新项目，不能直接 copy-paste 后视为新模型 authority。

---

# 2. 跨年训练：固定因素与变化因素必须严格分离

这是本项目的核心建模约束之一。

旧多省份模型之所以按年份分别求稳态，是合理的：不同年份的省际结构和宏观状态发生变化，但很多地理结构不变。

第一代 NSR-HANK 将保留这个思路：

> **跨年份共享 learned parameters，但每个年份在自己的 year-specific observables 下单独求稳态。**

暂不把 2010→2011→2012 直接建模成一个完整动态 transition system。

## 2.1 三类输入

### A. 跨年固定的 pair-level structural features

记为 \(Z_{ij}^{static}\)。

候选包括：

- 地理距离；
- 是否相邻；
- 海陆/地形等稳定地理关系；
- 省会间距离；
- 长期地理区位关系。

这些变量在所有年份保持相同，不得人为复制成可自由变化的 year-specific parameter。

### B. 跨年变化的 node-level features

记为 \(Z_{i,t}^{node}\)。

候选包括：

- 人均 GDP；
- 工资；
- 资本回报率；
- 人口；
- 产业结构；
- 城镇化；
- 固定资产/资本存量；
- 财政收入支出；
- 产业升级；
- 沿海制造业/服务业结构变化；
- 可观测政策或制度状态。

### C. 跨年变化的 pair-level features

记为 \(Z_{ij,t}^{pair}\)。

候选包括：

- 工资差；
- 人均 GDP 差；
- 资本回报差；
- 产业互补程度；
- 交通可达性变化；
- bilateral migration history；
- bilateral capital/investment exposure；
- 政策联系。

因此第一代劳动力网络输入写成：

\[
x_{ij,t}=
[
Z_{ij}^{static},
Z_{i,t}^{node},
Z_{j,t}^{node},
Z_{ij,t}^{pair}
].
\]

## 2.2 跨年参数共享

劳动力流量权重：

\[
W_{ij,t}^{L}
=
f_L(x_{ij,t};\theta_L),
\]

其中 \(\theta_L\) **跨年共享**，而 \(W_{ij,t}^{L}\) 因为 \(Z_t\) 的变化而可以逐年改变。

这使模型可以同时解释：

- 地理距离的长期稳定影响；
- 沿海产业升级；
- 中西部工资追赶；
- 省际 GDP 差距变化；
- 交通条件改善；
- 不同年份迁移格局变化。

## 2.3 年度稳态结构

对每一年 \(t\)：

\[
X_t^*
=
T(X_t^*;\theta,Z_t).
\]

因此：

- 2010 年有一个条件稳态；
- 2011 年有一个条件稳态；
- ……
- 每年用该年的动态特征求解；
- learned structural parameters \(\theta\) 在年份之间共享。

这不是“每年训练一套完全独立的网络”。

它是：

> **shared structural mapping + year-specific equilibrium。**

## 2.4 时间验证必须防止信息泄漏

未来训练至少包含两类 OOS：

1. **hold-out years**：用早期年份训练，后期年份验证；
2. **hold-out province pairs**：部分省际 pair 不参加训练，用于检验网络能否根据结构特征泛化。

不得仅报告 pooled in-sample fit。

---

# 3. 第一代劳动力网络 \(W^L\)

## 3.1 两阶段劳动力决策

不建议只用一个 softmax。

第一步：省 \(i\) 有多少劳动服务流向外省：

\[
m_{i,t}^{L}
=
\sigma(g_L(Z_{i,t};\phi_L)).
\]

第二步：已经离开本省的劳动流向哪个目的地：

\[
W_{ij,t}^{L}
=
\frac{\exp(s_{ij,t}^{L})}
{\sum_{j\neq i}\exp(s_{ij,t}^{L})},
\]

其中：

\[
s_{ij,t}^{L}
=
f_L(x_{ij,t};\theta_L).
\]

实际流量：

\[
F_{ij,t}^{L}
=
L_{i,t}^{home}
m_{i,t}^{L}
W_{ij,t}^{L}.
\]

## 3.2 首选训练数据

优先使用可形成 origin-destination-year 结构的真实劳动力流量数据，例如河南→广东、河南→山东等，并保存：

\[
(i,j,t,F_{ij,t}^{L}).
\]

宏观 \(Y/K/L\) 数据只能作为 general-equilibrium discipline，不能替代 flow identification。

---

# 4. 资本与财政网络的分阶段进入

## 4.1 \(W^K\)：第二个 learned network

资本网络与劳动力网络分离。

第一版资本流动可以先用透明、可解释规则：

- distance；
- return gap；
- GDP / industrial structure；
- simple gravity / exposure weights。

劳动力网络稳定后，再将 \(W^K\) 升级为 learned function。

避免第一版同时学习 \(\theta_L,\theta_K,\theta_G\)，从而把 identification 和 equilibrium convergence 混在一起。

## 4.2 \(W^G\)：中央财政节点

财政转移不应默认当作普通 bilateral capital flow。

第一代结构：

\[
\text{Province taxes/revenue}
\rightarrow
\text{Central Government}
\rightarrow
\text{Province transfers}.
\]

初期优先把观测到的财政转移支付作为外生/数据约束对象。

只有在劳动力和资本网络稳定后，再讨论是否学习 \(W^G_{i,t}\)。

---

# 5. 训练策略：Flow Pretraining → Equilibrium Embedding → Fine-tuning

## Stage A — Flow-supervised pretraining

首先只回答：网络能否解释真实省际劳动力流量？

训练：

\[
\theta_L
=
\arg\min
\mathcal L_{flow}.
\]

必须报告：

- flow prediction；
- origin-share error；
- destination-share error；
- hold-out year performance；
- hold-out pair performance；
- feature sensitivity；
- interpretable partial effects。

## Stage B — General-equilibrium embedding

将已训练的 \(W^L_{\hat\theta_L}\) 嵌入 regional HA/HANK system。

求：

\[
X_t^*(\hat\theta_L).
\]

检查：

- province output；
- labor；
- capital；
- wage；
- return；
- distribution；
- national clearing。

## Stage C — Equilibrium-constrained fine-tuning

只有 A/B 均通过后，才允许 \(\theta_L\) 在一般均衡中有限调整：

\[
\mathcal L
=
\lambda_F\mathcal L_{flow}
+
\lambda_M\mathcal L_{macro}
+
\lambda_E\mathcal L_{equilibrium}
+
\lambda_R\mathcal R(\theta).
\]

核心原则：

> 不能为了把 GDP 拟合得更好而破坏真实流量网络。

---

# 6. 模型判据：三重有效性

## 6.1 Empirical fit

解释 bilateral labor flows、province output、labor、capital、wages / returns（如数据允许）。

## 6.2 Economic validity

检查：

- HJB residual；
- KFE residual；
- mass = 1；
- non-negativity；
- household feasibility；
- labor conservation；
- capital conservation；
- goods clearing；
- capital clearing；
- fiscal accounting；
- national identities。

## 6.3 Generalization / policy stability

检查：

- hold-out years；
- hold-out province pairs；
- parameter sensitivity；
- network OOD；
- policy counterfactual stability；
- perturbation 后是否仍能重新达到一般均衡。

---

# 7. 推荐 Python 软件结构

```text
src/deep_learning_hank/
    economics/
        household/
        distribution/
        firms/
        fiscal/
        prices/
        market_clearing/
    regional/
        regional_module/
        labor_flows/
        capital_flows/
        fiscal_transfers/
        features/
    solvers/
        steady_state/
        equilibrium/
        transition/
    learning/
        flow_models/
        objectives/
        constraints/
        training/
    diagnostics/
        household/
        distribution/
        regional/
        national/
        learning/
    data/
        schemas/
        transforms/
    experiments/
    provenance/
```

原则：

- economics 不依赖 learning；
- learning 可以调用 economics/equilibrium；
- diagnostics 独立于 trainer；
- 每个年度 equilibrium 有 immutable config；
- run no-overwrite；
- source SHA / data manifest / feature schema 必须记录；
- CPU small case 优先；
- GPU 后置。

---

# 8. 初版实施路线

## DLH-0R1 — Scientific Constitution Correction

冻结：

- Route D 不再是 primary scientific contribution；
- learned interregional flow network 成为核心研究路线；
- one-region real HA 只作为 computational benchmark；
- minimal genuine HANK 单独作为下一结构层；
- learned \(W^L\) 先于 \(W^K\)；
- household home region 固定；
- yearly steady states + cross-year shared network parameters；
- fixed vs time-varying features 显式分离。

禁止代码。

## DLH-1 — Evidence + Existing Python Kernel Audit

### DLH-1A Literature Route

系统建立 Structural RL、DeepHAM、neural HJB、master-equation neural solvers、neural operator、heterogeneous-agent surrogate methods、learned economic networks、spatial / multi-region HA/HANK、differentiable equilibrium / implicit layers、flow / gravity neural models的文献证据。

### DLH-1B Python Kernel Audit

只读检查现有单省 Python HJB/firm code，输出 equation map、dependency map、reusable/redesign/drop、I/O contract、legacy-state audit、candidate migration allowlist。不直接迁移代码。

## DLH-2 — Single-Region HA Computational Benchmark

建立 one-liquid-asset、idiosyncratic productivity、HJB、KFE、firm、steady-state clearing、deterministic diagnostics。

注意：这一阶段叫 **HA/Aiyagari computational benchmark**，不称为完整 HANK。

## DLH-3 — Minimal Genuine Single-Region HANK

在 DLH-2 上加入最小 New Keynesian closure：nominal rigidity、monetary/fiscal closure、genuine HANK equilibrium objects。

## DLH-4 — Two-Region Hand-Specified Flow Prototype

不训练神经网络。手工给定 \(W^L\)，验证 home-region household identity、cross-region labor service allocation、wage feedback、firm response、conservation、national equilibrium、convergence。

## DLH-5 — Learned Labor Flow Network Baseline

使用真实 origin-destination-year migration / labor-flow data，实现 static features、time-varying node features、time-varying pair features、shared cross-year \(\theta_L\)、year-specific \(W_t^L\)、flow-supervised training、interpretable gravity baseline、constrained neural additive model。

GNN/message passing 禁止进入 baseline。

## DLH-6 — 3–5 Region General-Equilibrium Integration

将 learned \(W^L\) 嵌入 regional structural model，逐年求 \(X_t^*(\theta_L)\)，验证 equilibrium convergence、flow fit、macro fit、OOS year、OOS pair、perturbation stability。

## DLH-7 — Learned Capital Network \(W^K\)

顺序：transparent capital-flow baseline → empirical capital-flow data inventory → supervised \(W^K\) → joint equilibrium → identification test。

不得直接 joint-train \(W^L+W^K\) 从零开始。

## DLH-8 — Fiscal Transfer Module

先以 observed transfers / transparent central allocation 进入，再决定 \(W^G\) 是否需要学习。

## DLH-9 — Full 31-Province Year-by-Year Equilibrium Panel

每一年独立求条件稳态：

\[
X_t^*=T(X_t^*;\theta,Z_t).
\]

但：

- \(\theta_L,\theta_K\) 跨年共享；
- \(Z^{static}\) 固定；
- \(Z_t^{dynamic}\) 逐年变化；
- \(W_t\) 因动态特征而逐年变化。

## DLH-10 — Policy Transmission

进入政策实验前必须先通过 identification、OOS、equilibrium diagnostics、parameter stability、flow-network stability。

候选政策：区域财政倾斜、劳动力流动摩擦变化、交通改善、产业升级、区域生产率 shock、monetary/fiscal shock 的区域异质传导。

## DLH-11 — Learned Message Passing / GNN Extension

Baseline \(W^L/W^K\) 成熟后，再研究 learned messages 是否提供额外解释力，以及是否可以压缩 31 省高维 equilibrium information。

这可能形成独立论文/高级扩展。

---

# 9. 第一代论文的候选贡献结构

现阶段不作 novelty claim，但工作目标可以明确成三层：

1. **Structural**：regional HA/HANK modules + learned interregional flow network + national equilibrium。
2. **Empirical/Identification**：利用真实 origin-destination flow 数据识别网络，而不是仅用宏观总量反推隐藏权重。
3. **Computational**：shared cross-year structural parameters + year-specific equilibrium，并明确区分 time-invariant geography、time-varying regional development、yearly equilibrium、long-run learned mapping。

---

# 10. 当前明确不做

在 baseline 稳定前，不做：

- full 31-province neural training；
- simultaneous \(W^L/W^K/W^G\) learning；
- household permanent migration；
- housing/hukou choice；
- GNN/message passing；
- world trade system；
- tariff / exchange-rate system；
- two-asset regional model；
- GPU-first implementation；
- using old Matlab outputs as truth；
- Results / policy claims before diagnostic gates。

---

# 11. 远期扩展

如果中国省际版本成功，计算架构可扩展为国家网络，但需新增 trade network、tariffs、import/export demand、trade balance、international asset positions、exchange rates、multiple currencies / monetary authorities。

这是远期研究计划，不属于第一代 implementation scope。

---

# 12. 当前立即执行顺序

1. 发布本 Roadmap 到 GitHub `main`。
2. 在 Issue #2 下发布 authoritative `DLH-0R1` correction。
3. DSH 只修订 scientific constitution，不写代码。
4. ChatGPT fresh GitHub review + Owner freeze。
5. Issue #2 关闭。
6. 发布 DLH-1A/1B：文献证据 + existing Python kernel audit。
7. 只有 DLH-1 通过后进入代码迁移/实现。

---

## 当前 working scientific label

**Network-Structured Regional HANK（NSR-HANK）**

第一代核心：

> **Structural local economic modules connected by learned, interpretable interregional flow networks and disciplined by national general equilibrium.**

这是 working label，不构成 novelty claim 或最终论文标题。
