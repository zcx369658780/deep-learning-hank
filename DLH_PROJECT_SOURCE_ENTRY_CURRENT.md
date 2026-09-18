# DeepLearning-HANK 项目源唯一入口

入口版本：THIN-INDEX V1.0，2026-09-18。科研路线保持 `DLH-WL-V1-20260918`，不重新规划。
唯一当前仓库：`zcx369658780/deep-learning-hank`。
项目源只需上传本文件；完整规则、路线图、合同、任务与证据保存在 GitHub，按需读取。

## 1. 仓库接口与权威

仓库：https://github.com/zcx369658780/deep-learning-hank
本入口：https://github.com/zcx369658780/deep-learning-hank/blob/main/DLH_PROJECT_SOURCE_ENTRY_CURRENT.md
live main：https://api.github.com/repos/zcx369658780/deep-learning-hank/git/ref/heads/main

原始路线发布提交：`01daaf10c5854437870039a46435a075c664d9a3`。这是可追溯锚点，不是永久 HEAD；本入口所在后续文档提交不改变原始路线。
Owner 是最终 scientific authority；ChatGPT 是 L3 independent Reviewer / scientific-route advisor；DSH 是 bounded Builder；GitHub live main 是仓库事实来源。单个已提交文本不能替代 Owner 对战略变更的明确批准。
本文件是入口与安全摘要，不是完整文档镜像，不自动反映后续 Issue 状态，也不授予执行权。

## 2. 新会话如何恢复

先使用已连接的 GitHub 读取工具确认 live main SHA，再以该 SHA 读取同一版本的文件，避免混读。
按 `AGENTS.md` 指定顺序读取规则索引及必读规则、Owner 决策、Task Index、Startup Snapshot、主路线图和相关合同；有活动科学 Issue 时，再 fresh-read full body 与权威 comments。不存在活动任务时，不从历史 NEXT 恢复任务。
路线锁核验使用仓库中的 manifest，静态检查即可；不得运行模型或为通过检查改写哈希。
项目源缺少上述附件不构成缺文档：应从本仓库按路径读取，而不是要求 Owner 重传整套文件。GitHub 内容不通过 file_search 搜索。
同一会话恢复后围绕当前任务读取变化和必要证据，不反复读取全部历史或为文档核验执行科学程序。链接存在不等于内容已读；实际读取失败时应报告缺口，不凭记忆声称完成核验。

## 3. GitHub 文档索引

以下路径均相对于唯一仓库根目录。启动必读集合仍以 AGENTS 与规则索引为准；本表只负责定位。

| 要查什么 | 仓库路径 |
|---|---|
| Agent 启动与规则索引 | `AGENTS.md`；`project_rules/PROJECT_RULE_INDEX_CURRENT.md` |
| Owner 原始批准 | `docs/decisions/DLH_OWNER_ROUTE_FREEZE_WL_V1_2026_09_18.md` |
| 路线保护规则与哈希 | `project_rules/PROJECT_RULE_SCIENTIFIC_ROUTE_LOCK_CURRENT.md`；`docs/governance/DLH_ROUTE_LOCK_MANIFEST.json` |
| 完整主路线图 | `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md` |
| 活动任务、当前事实与交接 | `tasks/TASK_INDEX_CURRENT.md`；`docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`；`docs/handoffs/DLH_SESSION_HANDOFF_CURRENT.md` |
| 冻结家庭依赖 | `docs/contracts/DLH_FROZEN_HOUSEHOLD_DEPENDENCY_CONTRACT_CURRENT.md` |
| 第一版劳动份额合同 | `docs/contracts/DLH_WL_CONDITIONAL_DESTINATION_V1_CURRENT.md` |
| 测试成本与缓存 | `project_rules/PROJECT_RULE_TEST_COST_AND_CACHE_CURRENT.md` |
| DSH 同步协议与启动 | `docs/governance/DLH_DSH_SYNC_ONLY_PROTOCOL_CURRENT.md`；`docs/governance/DLH_DSH_INITIALIZATION_PROMPT_CURRENT.md` |
| 上传范围与历史入口 | `PROJECT_SOURCE_MANIFEST.md`；`docs/archive/pre_wl_route_2026_09_18/README.md` |

科学源码、报告与历史 Issue 只在当前任务需要时读取，不因“恢复项目”重跑所有历史实验。

## 4. 必须继承的科研边界

Owner 已批准的第一版仅学习：**给定外流比例下的条件目的地份额 W^L**。不联合学习外流总量、家庭总劳动、资本网络或全部参数。
矩阵统一 `[origin,destination]`，行归一：`W_ii=0`，`sum_(j!=i) W_ij=1`；`P_ii=1-m_i`，`P_ij=m_i W_ij`；`F_ij=ell_i P_ij`，目的地劳动为列和。m 与 ell 是给定输入；缺失/零外流行不编造有效监督标签。两区只测核算，非退化条件目的地学习至少三区。
家庭参考依赖与用途合同默认冻结，不反复重构 HA；冻结代码不等于得到收敛解。当前 selected-Q solver 支线暂停，不是所有独立离线学习的统一前置。Jacobi、Newton、trajectory 不自动续跑。
P0 同步 → P1 依赖登记/离线接口/小型核算 → P2 小型离线基准与学习 → P3 现实数据验证 → P4 受控经济耦合 → P5 完整 HANK/动态/Results。数据口径工作可按主路线图并行，不重排科学依赖。
固定、低维参数化、小型神经使用相同信息集与划分；合成/规则标签不冒充现实数据。首轮离线实验默认计算上限 30 分钟，具体次数与方法由 activated Issue 事前冻结，预算耗尽不自动续单。
经济耦合另需用途适配的家庭解、最终同一 Q、合法分布与核算证据及明确授权。ONE selected-Q 不变；不得用 Dual-Q、未收敛候选或其他项目的 accepted 状态填补证据。ML/HJB/KFE/GE 误差分开。
不要读取或引用邻近博士论文仓库来确定本项目状态。Owner 提供的跨项目指南只转移方法，不导入参数、代码、checkpoint 或验收。

## 5. 防止模型切换后重写路线

**GPT-5.6、GPT-6、DSH 和任何后续 agent 都继承同一 Owner 决策；新会话、额度变化或换模型不是重选路线的理由。**不得将“继续”“修复问题”解释为解除锁定。
Reviewer 可以在锁定边界内制定有限实施任务与更新已验收进度。战略改动必须先有证据与明确差异，再取得 Owner 批准、记录 dated amendment 后同步。发现科学错误可暂停受影响用途，不能隐瞒，也不能自行改道。
原始批准 SHA-256：`4b87eab29d46e8e53d5da77a7c6210cc9dbaee5b12d852379528d36c25ebd38c`。
原始路线锁定区块 SHA-256：`4d2ef5c125bfbf0bbb59bbb416734485ad3df6b4c4b50b17c760d4718b555ce8`。
算法与编码见仓库 manifest。合法后续 amendment 需追溯 Owner 批准，不以新哈希本身证明合法。本入口不改变上述原始哈希。

## 6. 发布时状态与解释上限

以下为 2026-09-18 本入口整理时的快照，不替代未来 fresh-read：P0；科学 Builder Issue NONE；#73 CLOSED / COMPLETED；项目源单入口上传待 Owner 确认，DSH 同步未回报。入口生成或 GitHub 发布不等于上传完成。
#73 残差 `10.435094313164921 -> 10.435094286652339`，仅极微小合法单步下降，HJB convergence FALSE；起点 active constraints=0，投影为 identity。不是 HJB 解，不用于监督真值或下游经济输入。
#73 旧路径计数 guard 仍有已知测试合同债务；本轮没有运行 full suite，不声称全仓全绿。低风险文档/路径问题不触发小时级科学重跑。

## 7. 上传、缺失文档与暂时无法上传

仅上传本文件即可，不需要另外上传 roadmap、规则、合同、manifest 或本文件的压缩包。上一轮 25 份上传集合不再执行。
已删除的操作文档无需补传；尚存的旧 CURRENT/旧快照/启动包可从项目源移除以腾出名额，GitHub 版本与历史证据不删除。无法移除的旧副本只作历史参考，不覆盖本入口指向的合法 live 状态和 Owner 路线。
论文、原始数据、私有文献与唯一研究资料不因精简而删除，也不未经授权上传公共 GitHub；本轮不要求补齐已缺失的资料。后续研究确需其内容时必须明确取得材料并读取，不能用索引代替证据。
若当前连单份文件也无法上传，可先把下面一句粘贴到新会话以从 GitHub 恢复。也可由 Owner 保存到项目指令作为临时入口；必须说明实际采用的方式，不虚报“文件已上传”。DSH 可先完成 GitHub/local 只读同步，项目源确认仍按协议如实报告 PENDING，不为附件不齐重新规划。

> 请接续 zcx369658780/deep-learning-hank，先 fresh-read GitHub live main 和根目录 DLH_PROJECT_SOURCE_ENTRY_CURRENT.md；继承 Owner 锁定路线 DLH-WL-V1-20260918，不重新规划。完整文档从 GitHub 按索引读取，不要求补传旧附件。先核对项目源与 DSH 同步状态；未有新科学 Issue 时只同步，不运行模型或训练。
