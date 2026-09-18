# 冻结家庭依赖与用途合同

版本：V1.0，2026-09-18，`DLH-WL-V1-20260918`。
本文件冻结默认不改的依赖及用途边界，不宣称新实现、适配器或解已经完成。

## 1. 实际被保留的参考对象

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`
Git blob：`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`。
历史 accepted #23 commit：`b038db800da3760cebee484b1c7a76bf7c1529d0`。
参考 SHA-256：`1795718C469FC3B427CAB8E3D5957C133BEAD6EACC9EF0A25A3EDB7211D1A024`。

独立实验 selected-Q blob：`7857cabb4d28af99cb9d59e2d1c3024b05787c11`。不是通过重新命名即可替代的同一数值解。#73 的 accepted candidate 仍未收敛。

## 2. Freeze 分类

A：经济方程/状态域/边界/策略选择/算子与收敛定义冻结；不等于已求解。
B：代码身份、接口/单位/排序/失败与 provenance 登记；不等于任意输入有效。
C：特定用途下已验收的 HJB、最终同一策略/Q、合法终端分布与聚合共同绑定一个 checkpoint；本轮没有新增 C。

当前决定是保护 A/B 与已有证据，不重新全审计、重跑或修改家庭。完整实际 I/O、排序、失败字段与验证配置将在 P1 从本仓库现有证据登记；未核验字段标记 NOT_VERIFIED，而非虚构现有 API。

## 3. 用途登记

| 用途 | 当前边界 |
|---|---|
| 只读查看源码/合同/历史产物身份 | 可按任务范围使用 |
| 用给定人工劳动总量测试 W^L 核算 | 可以独立设计，不调用家庭，不称均衡输出 |
| 用 #73 candidate 作最优策略标签/GE/福利基线 | 禁止 |
| 新价格/网格下调用 reference oracle 作为经济解 | 需相应证据与授权，不能从一个已测点推到连续区间 |
| stationary KFE / GE / learned-HANK coupling | 当前未授权，P4 前单独核对 |

已知有限域家族 `0<=a<=10, b>=-2, a+b<=W_max` 属实验合同；生产 W_max 未选。历史价格抽样通过不构成价格区间定理。无界控制/状态约束适用性与 selected-Q 固定点缺口保留。

## 4. 后续接口登记要求（规范要求，不是现有代码声明）

输入：contract/version、经济参数、grid/domain、工资/回报/税收/转移、numerics、单位/顺序与 provenance。
输出：V/policy/Q 身份、真实 residual、convergence、失败状态；只有合法验收用途才提供 stationary mass/aggregates。

失败要区分未收敛、无合法策略、非法算子、KFE 非唯一/残差失败、超出已验证域。不能返回裸数组让下游忽略失败。没有实际支持的结果写 unavailable，不能为接口齐全新跑 KFE。

同一个 selected-Q 用于 solve/validation；未来 forward 使用同一过程的 Q^T。固定代码不固定对新价格的响应。参考实现与 corrected successor 分层；变化须 Owner 科学授权，不能以适配器名义改变成本/FOC/边界。

## 5. 来源

本仓库 #23、#73、当前主路线图的历史版本、post-5VY 交接与区域接口。Owner 的跨项目指南只提供 A/B/C 分类方法；其参数、checker、checkpoint 和验收不导入本项目。
