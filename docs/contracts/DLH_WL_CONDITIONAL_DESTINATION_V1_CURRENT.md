# 第一版条件劳动目的地分配合同

版本：V1.0；日期：2026-09-18；Owner route：`DLH-WL-V1-20260918`。
状态：Owner 已批准科学对象；实现、数据和训练尚未执行。具体实验配置由后续 bounded Issue 事前冻结。

## 1. 经济对象

i 是 origin，j 是 destination。数组统一 `[origin,destination]`。
`m_i^L in [0,1]`：给定的劳动外流比例，不是学习目标。
`ell_i=M_i L_i^home`：给定的 origin 劳动总量，M 与 L 的人口/家庭质量及效率单位必须声明；不能把人口计数默认为效率劳动。

W 是外流发生后选择 foreign destination 的条件份额：
`W_ii=0, W_ij>=0, sum_(j!=i) W_ij=1`。
完整矩阵：`P_ii=1-m_i^L; P_ij=m_i^L W_ij (j!=i)`。
完整流量：`F_ij=ell_i P_ij`。
目的地劳动：`L_j^dest=sum_i F_ij`，即 `Ldest=P.T @ ell`。
若使用工资核算：`wbar=P @ w`，则 `sum_i ell_i*wbar_i=sum_j Ldest_j*w_j`；必须同一 P、同一单位，不静默增加税/wedge。

本版只学习 W，不学习 m、人口质量、家庭总劳动、资本网络/参数。暂解释为劳动服务配置；不是内生迁居/户籍/福利机制。现实迁移数据与此经济对象的桥接必须明确。

## 2. 特殊情形与识别

两区域 foreign destination 唯一，W 的条件选择退化；两区只做核算，不用于证明网络学习能力。非退化学习至少三区。

m_i=0 或 ell_i=0 时完整流量仍定义良好，但该行没有可识别的条件目的地标签；缺失/无外流行不得伪造均匀真值或当有效监督。可以计算模型预测行，但须标注没有标签支持。

单区域仅允许 m=0、P=[1] 的核算极限；W 为不适用，不声称 foreign shares 行归一可识别。有 m>0 却没有可选目的地时返回输入/支持域失败，不用 fallback 把质量送回 home。

缺失目的地/结构零需显式 mask 与口径；未观察到不是结构不可能。支持集合变化属于实验设计，不能在评价后自动删难例。

## 3. 数据与信息集

分别记录 origin/destination/time、label_semantics、单位、来源/版本/许可、覆盖、调查权重、missing/support mask、输入信息可用时间、m 与 ell 来源。

年度流量、存量交叉表、多年转移、总量代理互不替代。只有总流入/流出不能自动识别双边 W。规则/合成标签显式标记 RULE_GENERATED/SYNTHETIC，不冒充真实省份或因果证据。归一化不修复经济口径错配。

calendar-time lag 与 outer-iteration lag 分别登记。第一版是离线任务，不默认引入同轮工资→份额→企业→工资反馈。特征不得泄漏标签/未来信息。

## 4. 最小实现与测试要求

输出 W、P、完整 F、destination sums、有效行/mask、诊断和数据/配置/代码身份。不只返回聚合量。

非对称矩阵、不等 ell/m、m=0/1、零总量、单区/两区退化、非法输入、行归一/非负/零对角、origin/national conservation、destination 聚合、工资账恒等式、区域重编号一致性须有 tiny tests。

仅实现离线代数时不得调用/import-trigger HJB/KFE/GE。既有区域模块可作公式参考，不能为取一条核算式执行其 outer solve。

## 5. 学习与接受边界

比较固定映射、低维参数化映射、小型神经映射；同数据、信息集和划分。具体架构/损失/随机种子/训练次数、预算与误差阈值事前在 Issue 冻结；本合同不宣称已选网络或已取得指标。

train/validation/test 分开，预处理在训练部分拟合；按数据支持做时间/地区 OOS。记录预测误差、经济约束、扰动、稳定性与运行成本；神经模型未胜基准可为有效负结果。

简单 source-rule/synthetic 原型有预算，不无限复刻旧公式。没有现实标签只阻塞经验结论，不迫使恢复 solver 主线。ML/HJB/KFE/GE 误差分开；P4 前不得经济耦合。
