# 当前启动快照

日期：2026-09-18。仓库：`zcx369658780/deep-learning-hank`。
工作区：`D:\deep-learning-hank`。路线：`DLH-WL-V1-20260918`。

## 状态与版本解释

本轮发布前 main：`9058be73fc4b4211c8ad49ea0989d4fdc224ed1d`。
本文件所在文档提交是同步发布锚点；启动时记录实际 fresh main，不把发布前 SHA 当永久 HEAD。导出包外部 manifest 记录确切发布 SHA，避免文件自引用自己的 commit。

Owner 已批准新路线。P0 三端同步已经完成并经 Reviewer fresh GitHub 核对：项目源已上传，DSH SYNC_ONLY 完成且科学/模型/训练/pytest 调用均为 0。Issue #74 / P1A 现为 **ACTIVE / OPERATIVE**；其 exact Builder branch 与 operative baseline 由 final activation comment 指定。学习训练尚未授权，经济耦合未授权.

## 最新科学事实（保留，非本轮重跑）

Issue #73 / DLH-5V-Y CLOSED / COMPLETED。
accepted candidate/integration：`838764a9a489b771de852a684a2d2cc99703c168`。
Reviewer acceptance：`5728591018`；integration：`5728595318`。
Terminal A：`DLH_5VY_ROUTE_A_ONE_STEP_PROJECTED_REGULARIZED_NEWTON__DOMAIN_SAFE_SINGLE_Q_RESIDUAL_REDUCING_CANDIDATE_ACCEPTED__TRAJECTORY_DESIGN_GATE_READY`。

残差 `10.435094313164921 → 10.435094286652339`，绝对下降 `2.6512582351756464e-08`，ratio `0.9999999974592868`。接受第 `1340/9261` 次 `(3,0,16)`，lambda `0.125`、alpha `2^-16`。min p_b `5.41690375095121e-10`，max|Q1| `4.85061990573854e-12`；Armijo PASS，material<=0.5 FALSE；repeat IDENTICAL。起点 active constraints=0，projection=identity。

HJB convergence FALSE；candidate 不是解。不授权第二步、trajectory、stationary KFE、GE 或下游经济用途。solver 支线现在暂停。

## 保留的身份

- oracle blob：`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`
- selected-Q blob：`7857cabb4d28af99cb9d59e2d1c3024b05787c11`
- #69 blob：`83e9be0febcc03eb721265d3558887bd6b1586a4`
- #71 blob：`96dd262a4ae42e26d489a317d9a04a9264b481b1`
- #72 module blob：`f99ff6eb0d0a74cccc400ba83162a8affa9c6924`

ONE MATLAB-faithful selected generator governs solve/validation；Dual-Q 禁止；同过程 HJB/KFE 合同保留。未新增生产 W_max、价格适用区间或 solved checkpoint。

## 测试债务

#72 cumulative-path guard 已 durable 修复。#73 仍有旧四路径上限与授权五路径 remediation 的测试合同缺陷。已获低风险 waiver；不自动 scientific blocker。full suite 未在本轮执行，不声称 repository-wide green。不得为本次文档同步启动修复或重跑。

## 新主线与下一动作

第一版离线学习给定外流比例后的目的地份额；外流比例和家庭总劳动不联合训练。沿用 origin×destination、行归一。当前下一步是执行已激活的 Issue #74 / P1A：家庭已有证据登记、离线 W/P/F 核算接口与非对称 tiny tests；不调用家庭、不训练。

路线与合同见 `README_START_HERE.md`。详细旧实验见 post-5VY 交接；本快照不重复全部历史。
