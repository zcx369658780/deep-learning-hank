# Neural-HANK 当前研究框架与“隐性劳动—测量楔子”后续论文研究备忘录

日期：2026-09-19
项目：zcx369658780/deep-learning-hank
用途：当前 Neural-HANK 论文路线归档 + 后续独立论文研究储备
状态：研究备忘录，不替代 GitHub 已冻结的 operative contract / Issue authority

## 0. 文档定位

本备忘录有两个目的：

1. 归纳当前 Neural-HANK 项目的核心科学构想、模型接口、神经网络设定、数据路线与当前状态。
2. 保存一条后续可独立发展为新论文的研究思路：中国劳动市场中的人口迁移、就业人数、工作时长、劳动效率、社保/单位用工覆盖并非同一个经济对象，真实有效劳动可能是潜在状态，而不同统计体系只是对该潜在状态的不同、有噪声的观测。

若当前 Neural-HANK 论文顺利投稿，可直接从本备忘录恢复下一篇论文，而不必重新恢复本轮讨论。

# 第一部分 当前 Neural-HANK 项目

## 1. 基本定位

当前长期目标是结构化、多区域、可解释的 HANK：

- 家庭异质性、资产、分布、预算约束、企业、价格和核算保持显式经济结构。
- Neural/ML 优先用于难以事先精确指定的区域联系映射。
- 不把 neural network 直接替代 HJB/KFE，也不把 end-to-end GE 作为第一步。
- 当前 selected-Q household fixed point 的历史未解决问题不再阻塞离线区域学习，但后续 HANK coupling 仍需要用途适配的 household/KFE/operator 证据。

核心不是“Deep Learning 解 HANK”，而是“显式经济结构 + 有界可解释的 learned regional mapping”。

## 2. 第一学习对象

第一学习对象是给定 origin outflow rate 之后的 conditional destination share：

W_L(i,j,t)

约束：

- W_L(i,i,t) = 0
- W_L(i,j,t) >= 0
- 对 j != i 行归一

矩阵方向严格为 row = origin, column = destination。

完整 annual allocation：

P_L(i,i,t) = 1 - m_L(i,t)
P_L(i,j,t) = m_L(i,t) * W_L(i,j,t), j != i

劳动流：

F(i,j,t) = ell(i,t) * P_L(i,j,t)

原始 V1 中 m 与 ell 是给定输入，不与 W 同时学习。

两地区只能做 accounting/orientation test；真正的 destination choice 至少需要三个地区。经济集成层级保持 2 -> 3-5 -> 31。

## 3. P2 三类离线基准

### Fixed baseline

在结构允许的 foreign destinations 上 uniform 分配。

### Parametric gravity/logit baseline

冻结六个变量：

- log_gdp_dest
- log_wage_gap
- log_adj_distance
- adjacency
- log_accessibility_dest
- w_ij

不包含 per-origin/block intercept，也不包含 log_gdp_origin。

该模型延续 Owner 过去多省 HANK 的基本直觉：地理摩擦限制人口流动，经济差距提供流动激励。

### Small neural pair scorer

冻结网络：

- pair-level scorer
- raw components 约 16
- hidden widths [16, 8]
- ReLU
- Tanh
- scalar score
- support-masked softmax
- 无 GNN / attention / transformer / RNN / region embedding

训练：

- TRAIN-only z-score
- weighted cross entropy
- ell-normalized TRAIN weights
- Adam, lr=0.01
- full batch
- max steps=1500
- eval interval=50
- patience=200
- min_delta=1e-4
- seeds=[0,1,2]
- deterministic

## 4. P2 负结果

S0 TEST CE：
- fixed 1.098612
- parametric 0.912172
- neural seed0/1/2: 0.913219 / 0.921067 / 0.915075

S1 TEST CE：
- fixed 1.098612
- parametric 0.908159
- neural seed0/1/2: 0.909354 / 0.917621 / 0.912259

结论：在冻结 synthetic design 下，小型 neural pair scorer 没有超过正确设定的低维 parametric gravity/logit baseline。

科学含义：

- 不为了 Deep Learning 而无限扩大神经网络。
- 结构模型的可解释性非常重要。
- distance + economic gap backbone 值得保留。
- 未来 ML 更适合做 residual/nonlinear augmentation，而不是替代整个迁移结构。

## 5. 现实数据桥接

目前现实对象主要包括：

- Census / 1% sample: multi-year residence transition
- floating-population OD: stock snapshot
- CMDS: annual migrant stock/sample candidate
- provincial aggregate inflow/outflow proxies

没有 verified TRUE_ANNUAL_OD_FLOW 可直接当作 W_L 真值。

因此必须区分：

1. multi-year transition -> annual transition
2. stock -> flow
3. population -> labor service

Population-to-labor bridge需要 destination-specific labor intensity lambda(i,j)。person share 只有在适当 share-equivalence 条件下才可作为 labor-service share。

## 6. P3C 数值边界

在任何真实 transition matrix 被程序执行前已冻结：

- pi_max=0.15
- tau_W_abs=0.02
- tau_m_abs=0.02
- unmappable mass max=0.01
- stochastic/support/root/reality/dedup tolerances
- deterministic 64 optimizer starts
- fixed RNG seed
- global uniqueness claim ceiling

严格区分：

- F_all_exact：数学 exact roots
- F_search_tol：有限搜索发现的 numerical epsilon-root candidates

有限搜索不能证明 global uniqueness 或 non-existence。

# 第二部分 Owner 新增路线：Latent Labor Measurement Architecture

## 7. Owner 批准的核心解释

真实人口/就业数据作为 measurement anchors，而不是 W 和 ell 的真值；保留 distance + economic-gap structural flow equation 作为 latent-flow backbone。

未来现实模型使用潜在对象：

- W_star(i,j,t): latent conditional destination share of labor services
- m_star(i,t): latent outflow share
- ell_star(i,t): latent effective origin labor

这些对象不机械等于 Census migration、registered employment、social-insurance enrollment、unit employment 或 total population。

## 8. 有效劳动分解

ell_star(i,t) = N_workers_star(i,t) * h_star(i,t) * e_star(i,t)

其中：

- N_workers_star：真实投入生产的劳动人数
- h_star：工时/劳动强度
- e_star：单位时间或单位劳动者效率

必须区分：

- extensive margin：更多劳动者进入
- intensive margin：同一劳动者工作更久
- measurement margin：真实劳动不变但统计覆盖改变

不能把三者统一写成一个 L 上升。

## 9. Structural latent-flow backbone

代表性 score：

s(i,j,t) = beta_distance * distance(i,j)
         + beta_gap * economic_gap(i,j,t)
         + beta_z * Z(i,j,t)

再经 support-masked normalization 得到 W_star。

候选因素：

- distance
- adjacency
- accessibility
- destination-origin wage/income gap
- output/productivity opportunity gap
- 经后续验证的制度 friction

核心直觉：地理摩擦限制流动，经济差距提供迁移动机。

## 10. Measurement equations

### Migration/residence

Observed census transition = function(latent labor movement, timing, demography, classification) + measurement error

### Employment coverage

L_obs(i,t) = q_cov(i,t) * N_workers_star(i,t) + measurement error

q_cov 可代表某一统计体系对真实 worker quantity 的 coverage。

未来可讨论的 measurement channels 包括单位统计边界、灵活就业、劳务外包、非正规就业和其他 institutional coverage 差异，但当前不假定任何固定 undercoverage 数值。

### Hours

Employment count 不能识别 h_star。

### Efficiency

即使人数和工时都已知，e_star 仍可能变化。

因此 per-worker productivity 与 hourly/effective labor productivity 必须区分。

# 第三部分 后续论文储备：Hidden Labor / Measurement Wedge HANK

## 11. 核心研究动机

就业、人口迁移和社保/单位用工统计，是对潜在有效劳动配置的不同测量体系，而不是同一个经济对象。

直接使用单一统计量可能把：

- worker quantity
- hours
- labor efficiency
- institutional coverage
- TFP

相互混淆。

## 12. 劳动生产率测量

如果真实生产函数是：

Y = A * K^alpha * (N*h*e)^(1-alpha)

但估计只使用 observed employment N_obs，那么未观测的 worker coverage、hours 和 efficiency 会部分进入 estimated productivity / TFP。

更稳妥的研究命题：

当工时和有效劳动强度被遗漏时，per-worker productivity 可能高估 underlying hourly/effective labor productivity。

## 13. 超长工时

不能假定 10 小时劳动等于 8 小时乘 1.25。

可写：

ell_star = N * h * e(h)

并允许高工时区间 e'(h) < 0。

因此更长工时可能同时提高 total labor input、降低 hourly productivity，并增加疲劳、健康与福利成本。

## 14. 社会保障与 HANK 消费机制

保障不足与收入风险可能同时影响：

- cash-income preference
- future income risk
- liquid wealth
- MPC
- precautionary saving

财政刺激消费乘数可写成：

Multiplier_C = f(formal coverage, income risk, hours, liquidity, MPC distribution)

核心问题：劳动保障不足究竟提高还是降低 transfer / consumption-stimulus multiplier？

## 15. 生育扩展

潜在机制：

long hours / insecurity
-> time scarcity + future uncertainty
-> consumption / fertility

但 fertility 内生化会引入生命周期、婚育状态、子女成本、childcare、female labor supply，建议不作为第一篇 hidden-labor HANK 的核心模块。

## 16. 劳动保护与出口竞争力

成本渠道：

labor protection up -> labor cost up -> export competitiveness down

生产率/资本深化渠道：

labor protection up
-> turnover down / effort or human capital up / K-L ratio up
-> productivity up

真正值得研究的是：在 GE/HANK 中，成本渠道与生产率/资本深化/需求渠道哪一个占主导。

## 17. 后续论文优先主题

优先论文：

Hidden Labor, Measurement Wedges and Fiscal Consumption Multipliers

核心链条：

employment coverage + hours + social protection
-> latent effective labor
-> income risk / MPC
-> consumption multiplier

潜在贡献：

1. 区分统计就业与有效劳动。
2. 将 coverage、hours、efficiency 写成 measurement system。
3. 在 HANK 中研究 measurement-adjusted labor 对 MPC distribution 和 fiscal multiplier 的影响。
4. 比较 structural-only、naive-data、latent-measurement-adjusted 三种模型。

第二主题：

Labor Protection and Export Competitiveness

后续加入 tradable/export sector、heterogeneous firms、social-insurance/wage cost、capital substitution、effort/productivity、domestic demand 与 regional labor flows。

# 第四部分 识别纪律

## 18. 不能让所有 wedge 自由变化

未来 empirical model 不能同时无限自由调整：

- migration wedge
- labor coverage wedge
- hours wedge
- efficiency wedge
- TFP wedge
- government-investment/output residual

建议 identification hierarchy：

1. accounting identities
2. low-dimensional structural mobility backbone
3. source-specific measurement equations
4. finite-dimensional measurement wedges
5. productivity residual
6. government residual only with explicit anchor/prior

## 19. 政府投资 residual

过去多省 HANK 中，政府投资补 provincial output gap 是实用 closure。

在 latent-labor architecture 中，它不能再作为无限制 province-by-province residual，否则可能吸收 labor measurement error、TFP error 和 demand gap。

未来必须报告各 residual/wedge 吸收了多少 provincial output discrepancy。

# 第五部分 三模型比较

## S0 STRUCTURAL_ONLY

- distance + economic-gap mobility backbone
- OD data 不当作真值
- 宏观量约束 latent states
- 最接近过去多省 HANK

## S1 NAIVE_DATA_PROXY

- 尽可能直接使用 Census/employment proxy
- benchmark only
- 用于显示“机械使用 observed data 会得到什么”

## S2 LATENT_MEASUREMENT_ADJUSTED

- structural mobility backbone
- population transition anchor
- employment anchor
- wage/GDP/capital anchors
- explicit measurement equations
- constrained coverage/hours/efficiency wedges

这是未来首选核心模型。

# 第六部分 与当前项目的衔接

当前第一篇 Neural-HANK 论文首先完成：

1. learned regional mapping 方法闭环
2. P3 real-data semantics / measurement architecture
3. controlled regional HANK coupling
4. 不夸大 neural superiority 地形成论文

当前论文核心贡献仍然是：

结构化区域 HANK + 可解释的 learned regional labor allocation mapping。

下一篇论文建议在当前 Neural-HANK 论文主体稳定、measurement bridge 有可复用经验、latent W/ell architecture 至少完成一次受控验证后启动。

# 第七部分 Owner 已批准的第一轮 empirical choices

- A：第一轮只做 2010 Census
- B：2000 wave 初期排除
- C：share-equivalence 只能作为 declared benchmark/sensitivity，不是真值
- D：EMPLOYED_PERSONS_DECLARED_AS_PROXY 作为 latent ell_star 的 noisy anchor，而不是 identity
- E：canonical information set 使用 window-start

H1-H4 仍需 primary-source human verification。

# 第八部分 后续论文研究问题

1. 官方就业人数与 latent effective labor 的差距在不同省份是否具有系统模式？
2. 超长工时在多大程度上提高 total labor input，又在多大程度上降低 per-hour efficiency？
3. employment coverage wedge 是否与地区工资、出口暴露、产业结构、城市等级系统相关？
4. 直接使用 Census migration proxy 会如何改变 inferred regional labor allocation？
5. latent measurement adjustment 是否改变省际工资、资本和产出一致性？
6. 传统 TFP 是否部分吸收 hours / coverage / efficiency measurement error？
7. social protection 是否通过降低 income risk 改变 MPC distribution 和 fiscal consumption multiplier？
8. labor protection 提高后的出口效应中，cost channel 与 productivity/capital-deepening channel 哪个占主导？
9. long hours 与 employment insecurity 是否通过 consumption、housing 和 fertility constraints 影响年轻家庭？
10. Census、labor force、unit employment、social insurance 等不同 measurement systems 能否共同识别 coherent latent labor state？

# 第九部分 当前仓库索引

主路线：
docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md
route ID: DLH-WL-V1-20260918

Owner amendment：
docs/decisions/DLH_OWNER_ROUTE_AMENDMENT_LATENT_LABOR_MEASUREMENT_2026_09_19.md

P2：
Issue #79 / P2D
terminal: DLH_WL_P2D_PREPROCESSING_CORRECTED_REPLICATION__PASS__P2_METHOD_GATE_COMPLETE

P3：
- #80 P3A: Branch B
- #81 P3B: bridge candidate available
- #82 P3C: execution readiness frozen
- #83 P3D: Owner human/source verification gate
- #84 P3E: latent labor measurement architecture freeze

# 最终研究定位

当前项目最稳妥的定位：

不是让神经网络替代 HANK，而是在结构化多区域 HANK 中，用可解释的 learned mapping 处理区域劳动配置；现实人口和就业统计不被机械视为真实劳动，而作为潜在有效劳动配置的 measurement anchors。

下一篇论文可进一步发展为：

研究隐性劳动、统计覆盖、工时、社会保障与有效劳动配置的 measurement-error HANK，并研究这些劳动市场 measurement wedges 如何改变消费乘数、区域均衡与出口竞争力。

这条路线将当前 Neural-HANK 项目与 Owner 过去“距离 + 经济差距决定省际流动、劳动供给内生化”的多省 HANK 研究自然连接起来，同时避免把不完备现实数据机械当成结构参数真值。
