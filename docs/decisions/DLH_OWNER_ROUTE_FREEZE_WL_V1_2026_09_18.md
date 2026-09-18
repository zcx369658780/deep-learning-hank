# Owner 已批准的科研路线决定

Decision ID：`DLH-WL-V1-20260918`。日期：2026-09-18。
仓库：`zcx369658780/deep-learning-hank`。
记录者：ChatGPT，依据本会话 Owner 明确确认；不是伪造的 GitHub 签名或外部验收。
发布前 live main：`9058be73fc4b4211c8ad49ea0989d4fdc224ed1d`。

## 授权来源

Owner 明确说：
> 可以，我同意你的思路，并且我也接受第一版只学习“给定外流比例下的目的地分配”，暂不同时学习人口外流总量与家庭总劳动供给

Owner 随后要求同步 GitHub 与项目源，并特别要求路线图不得因后续切回其他模型而被轻易修改。此前确定的顺序为：路线确认 → GitHub 文档 → 项目源替换 → DSH 同步 → 新路线任务。

## 已批准决定

1. 项目恢复 Deep Learning + HANK / NSR-HANK 主线；不再以无限完善当前 selected-Q solver 为全局前置。
2. 冻结现有家庭科学定义/实现依赖，按已有证据记录适用范围；不借冻结新增 solved-checkpoint 声明。
3. 第一版仅学习 `W^L`：给定 origin 外流比例后的 foreign conditional destination shares。外流比例、人口/家庭质量与家庭总劳动不是联合学习目标。
4. 沿用本项目 `origin × destination`、行归一方向；`P_ii=1-m_i`，`P_ij=m_i W_ij (j!=i)`；保存完整双边流量与守恒。
5. 先离线合同/基准/小型学习，现实数据口径核实并行；合成/规则标签与现实标签分别命名。两区做核算，至少三区才做非退化条件目的地学习。
6. 比较固定、低维参数化和小型神经映射；不联合学习资本网络、全部地方参数或全模型 end-to-end。
7. selected-Q refinement 暂停；Jacobi probe 不是开工前置。#73 未收敛候选不得充当经济解、真值或下游输入。
8. 经济耦合单独 gate；ONE selected-Q、同过程 HJB/KFE、一致核算不变。stationary KFE、GE、动态及 Results 没有因路线调整自动授权。
9. 测试分层/缓存；docs/test-contract 低风险修复不默认 full suite；预算耗尽不自动续单。
10. 不读取或使用邻近博士论文仓库作为本项目状态。Owner 提供指南仅转移方法，不导入其参数、代码、checkpoint 或 authority。

## 稳定性与可变边界

本 dated decision 保留为原始批准记录，不随着进度滚动改写。更改上述决定需要新 dated amendment 和 Owner 明确批准；旧记录不删除。Reviewer 可在这些边界内制定有限实施任务、选择事前小型 ML 配置并更新已验收进度，无需重复请求 Owner 批准同一路线。

新会话、GPT-5.6/GPT-6/DSH 切换和一般性“继续”均不重置决定。发现真实科学问题可以暂停受影响用途、提交证据和修改提案，不能隐瞒问题，也不能自行改道。

## 本次执行范围

仅同步文档与导出替换包。无 successor 科学 Issue、无代码/测试/配置改动、无模型/训练运行。DSH 的后续零科学同步按专门协议；科学开工仍需新的 active Issue。
