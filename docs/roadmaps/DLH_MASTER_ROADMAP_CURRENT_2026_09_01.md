# Deep Learning + HANK — 当前主路线图

版本：**V1.0 / OWNER-APPROVED ROUTE LOCKED**。日期：2026-09-18。
路线 ID：`DLH-WL-V1-20260918`。唯一仓库：`zcx369658780/deep-learning-hank`。
本路径保留历史文件名以保持入口稳定；文件名中的 2026-09-01 不是当前版本日期。

原始 Owner 批准：`docs/decisions/DLH_OWNER_ROUTE_FREEZE_WL_V1_2026_09_18.md`。
本轮只改文档，不授予模型运行权。当前在 P0，项目源替换和 DSH 回报尚待完成。

<!-- OWNER_LOCKED_ROUTE_BEGIN DLH-WL-V1-20260918 -->
## Owner 锁定核心：不得擅自重写

本路线已经 Owner 确认，不是待下一模型重新选择的建议稿。后续 GPT-5.6、GPT-6、DSH 或新会话必须继承；额度或模型切换不是改规划理由。

- 第一学习对象：给定外流比例的条件目的地份额 `W^L`；不同时学习外流总量、家庭总劳动或资本网络。
- 矩阵：`origin × destination`，行归一；`W_ii=0`，`sum_(j!=i) W_ij=1`；`P_ii=1-m_i`，`P_ij=m_i W_ij`。
- 家庭：冻结参考依赖与合同，已有证据分用途登记；不默认重新开发 HA，也不新增“解已验证”的 claim。
- 当前 selected-Q fixed point 仍未解决；该支线暂停，不是独立离线 ML 的统一前置。Jacobi/新 Newton/trajectory 不自动启动。
- 先接口/简单基准/有预算的小型离线原型，现实数据口径核实并行；规则/合成成功不等于经验机制识别。
- 经济耦合需要用途适配的家庭解、最终算子/分布/核算证据与另行授权；ONE selected-Q 不变，Dual-Q 禁止。
- 资本网络、联合估计、neural HJB、全 GE end-to-end 与完整名义/政策/福利 Results 均为后续单独决定，不提前塞进第一版。
- 科学实验与回归分离；不因低风险文档/路径 guard 问题默认运行 full suite 或历史求解实验。
- 两项目状态严格分离。只借鉴 Owner 提供指南的方法，不读取邻近仓库或继承其 accepted/frozen 状态。

战略变更必须遵循 `project_rules/PROJECT_RULE_SCIENTIFIC_ROUTE_LOCK_CURRENT.md`：证据 → 明确差异 → Owner 批准 → dated amendment → 同步。可以因科学错误暂停，不可先改路线后补授权。
<!-- OWNER_LOCKED_ROUTE_END DLH-WL-V1-20260918 -->

## 1. 研究目标与已有基础

长期目标是结构化区域 HANK 与可解释学习网络。家庭优化、资产与分布、企业、核算和后续名义结构保持显式经济定义；学习优先解决区域联系，而不是替代全部 HJB。

Issues #14–#73 留下家庭 provenance/oracle、区域核算接口、有限域/边界合同、单 Q 及真实残差诊断。历史 accepted 不等于所有用途通过。#73 仅有合法且极不 material 的单步下降；HJB convergence=FALSE。详情在 post-5VY 历史交接。

本次明确 supersede V0.55 及更早版本的“先完成当前 solver/全部 GE，才能开展任何 neural training”依赖关系；只对离线学习解耦，不放松经济解或 Results 标准。旧文档中的 NEXT 不再是当前任务。

## 2. P0–P5 执行路线

| 阶段 | 目标/交付 | 验收与前置 | 边界 |
|---|---|---|---|
| P0 | GitHub 文档、项目源、DSH 三端同步 | 同一发布提交/route ID/hash，Owner 上传确认，DSH 零科学回报 | 不训练、不调用模型、不创建科学 successor |
| P1 | 家庭已有证据登记、W^L I/O 与数据口径、离线核算 tiny tests | 方向/非负/归一/完整流量/失败返回明确；不为补登记而重跑家庭 | 不实现或修改 HA；不把预期接口当已存在接口 |
| P2 | 固定/参数化/小型神经三基准离线闭环 | activated Issue；事前冻结输入域、配置、划分、度量和双重预算；必要复现 | 无 HJB/KFE/GE；无漫长 source-rule 重建或超参搜索 |
| P3 | 现实数据独立验证 | schema/口径/识别目标通过，正确样本外比较，数据来源可追溯 | 无合格标签则报告缺口；不伪造年度 OD 标签 |
| P4 | 受控经济耦合 | 用途适配家庭证据；最终同一 Q 与合法 KFE；独立授权 | 初次仅 fixed W^L→learned W^L；保持其他经济块与方法不变 |
| P5 | 完整名义 HANK、扩规模/动态/论文 | 名义/财政/回报结构、识别、数值与 Results 单独验收 | 不是加一条 Taylor rule 即可宣布完整 HANK |

P1 与现实数据口径整理可以并行；P2 不等待没有依赖关系的 selected-Q 修复。P3 的实证训练是否先于/并行 P2，由现有标签是否合格决定，不把数据缺口变成 solver 开发借口。

## 3. 第一学习对象与规模

完整定义见 `docs/contracts/DLH_WL_CONDITIONAL_DESTINATION_V1_CURRENT.md`。
`m_i^L` 为外生给定外流比例，`ell_i=M_i L_i^home` 为明确给定且单位一致的 origin 劳动总量。第一版不训练它们。

`F_ij=ell_i P_ij`；目的地劳动为列和。工资核算如使用 `wbar=P w`，数量与工资必须使用同一 P 与同一劳动单位，不能额外混入未说明的 wedge。

两区域仅做人工可核验核算；条件目的地学习至少三区。经济集成保持 `2 → 3–5 → 31` 层级。早期合成区域不是真实省份校准。

## 4. 标签路线与停损

先检查已有资料，不无限找数据。能独立计算的既有空间规则可用于一次廉价 surrogate；否则用事前说明的合成规则。规则/合成标签只说明方法管线，不获得真实经济识别。

仓库 DLH-1A 已有调查尚未证明合格的年度双边流量标签集；这是历史证据状态，不是本次新的外部数据调查。存量、年度流量、多年转移、总量代理分开，必要时先设计观测桥接再进入经验学习。

固定、低维参数化、小型神经使用相同信息集/划分。预处理仅在训练部分拟合；使用支持的数据频率做时间/地区验证，不凭空声称 OOS。神经基准不胜出时接受负结果，不无限增大网络。

## 5. 预算与重新打开 solver 的条件

P0：昂贵科学调用 0。P1：不调用家庭。首轮 P2 默认计算上限 30 分钟，具体训练次数/epoch/step/复现限额在 activated Issue 前冻结；先触及任一预算即停止。未来更高预算需明确授权，不通过拆分 successor 绕过上限。

selected-Q refinement 当前不排在开工队列。重开须说明它阻塞哪个具体研究 claim，经 Owner 批准后只测试一个假设，设置时间与重组/迭代次数上限；微小下降不自动续期。

## 6. 家庭与经济耦合的真实剩余条件

Freeze-A/B 不等于 Freeze-C。生产 W_max 未选、有限域收敛适用性缺口及 selected-Q fixed point 未解决等历史问题继续记录，但只阻塞依赖其解的用途。既有 oracle 接口、已验收配置与已知失败必须区分。

不得用中间 Q 的 stationary mass 推出 HJB 已解；不得用 #73 candidate 当 optimal policy 标签。代码冻结后价格变化仍需合格的家庭响应，不能重复使用同一个稳态输出假装已更新。

P4/5 分别报告 ML、HJB、KFE/operator、GE/accounting 误差。资本 B/A 定义、数量/回报权重、calendar lag 与 numerical iteration lag 不混用；邻近指南中的参数/方法阈值不自动采用。

## 7. 当前状态与下一交付

已完成：Owner 路线确认、P0 三端同步、Issue #74 / P1A、Issue #75 / P1B。P1B accepted/integrated 于 `e1b83b3d5b2c04d7e9052ad614e95631abb03dc6`；P1 已完成，数据/标签 schema 与首次 P2 method-only synthetic experiment contract 已冻结。

P2A 首次执行已完成但因重复完整执行突破 absolute-attempt ceiling 而以 protocol GATE FAIL 结案；observed neural non-gain 仅保留为观察证据。下一 gate 是在不改变 #75 冻结设计的前提下做一次 clean independent replication：科学代码先冻结成不可变 commit，科学执行只允许一次，报告/哈希修复只能走零-fit render。现实 OD 标签仍按现有证据分级，不因缺口恢复 solver 主线。

每个新任务注明 route ID、具体问题、预算、数据性质、allowed paths、产物与停止条件。Reviewer 可完善这些实施细节，不得改变锁定核心。

## 8. 文档与历史

Task Index 只写任务指针；Snapshot 写当前事实；本文件写路线。不要反复复制长篇历史。更新已验收进度不需要更新 Owner 锁定区块。

历史三份 CURRENT 的原 blob 保存在 `docs/archive/pre_wl_route_2026_09_18/`。#73 科学接受与 waiver 仍见 Issue #73 和 `docs/handoffs/DLH_SESSION_HANDOFF_POST_5VY_2026_09_18.md`。旧失败结果不删除、不重新认证。


P2B clean replication respected the single-invocation rule but ended Gate Fail after all 12 fits because post-fit aggregation crashed before predictions/results were persisted. This validates the need for per-fit durable scientific output. The next P2 replication keeps the #75 design unchanged and persists predictions/state in every FIT_COMPLETED record, making downstream accounting/rendering zero-fit recoverable.


P2C fixed the durability layer but exposed one isolated scientific runner defect: the neural optimizer received the TRAIN-z-scored design while final prediction fell back to raw_design because the runner omitted `universe._design_matrix = design`. The next bounded replication changes no scientific design; it retains the accepted P2C durability machinery and repairs only this preprocessing-state propagation, with a dedicated zero-fit pre-run prediction-path test.
