# 跨项目方法的有限采用说明

日期：2026-09-18。性质：自写方法摘要，不是邻近项目状态报告。

Owner 提供 `CH5_TWO_ASSET_MULTI_PROVINCE_HANK_HJB_FREEZE_AND_POST_FREEZE_GUIDE_20260918.md`。原始文件由 Owner 管理，未整篇提交公共 GitHub；无需访问来源仓库。

采用的方法：科学合同/实现/已解检查点三层 freeze；家庭优化与 stationary mass 分开；同过程 backward/forward；四类误差分账；完整双边矩阵与单位方向；只在有具体 claim 时重开 solver；分层测试、持久化产物和科学依赖缓存。

本项目沿用 origin×destination、行归一，不能照抄指南的 destination×origin 示例。以后若需要 capital layer、signal timing 或其他结构，另行本项目规格与授权，不照搬邻近公式。

不采用为本项目 authority：来源仓库 accepted/frozen 状态、V0/V1/V2、cell 编号、价格/容差/Delta、grid、KKT 修正、资本 K1/GovInv 设定或 Results 状态。没有读取邻近仓库，没有转移代码，没有新增家庭解证明。

这些方法不会放宽 #73 的解释上限，也不授权 KFE/GE；它们支持将独立 W^L 工作从未解决的实验 solver 分支中解耦。
