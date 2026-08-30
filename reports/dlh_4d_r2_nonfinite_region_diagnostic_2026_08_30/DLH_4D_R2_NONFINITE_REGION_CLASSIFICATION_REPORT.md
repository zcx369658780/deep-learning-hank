# DLH-4D-R2 — Non-Finite Region Stage-Resolved Classification Report

- Date: 2026-08-30
- Author: DSH (bounded scientific diagnostic executor)
- Authority: GitHub Issue #22 — `DLH-4D-R2: Classify non-finite household/KFE region before any fixture revision`（OPEN），activation comment `2026-08-30`（authority publication `4a9e7f8a9bb3e3a3a0b8b90dd9e485bf40f50d60`）
- Task type: `SCIENTIFIC_DIAGNOSTIC__NONFINITE_HOUSEHOLD_KFE_REGION_CLASSIFICATION`
- Status: **stage map complete（fail-closed 证据一致）**

## 1. Terminal classification

**`DLH_4D_R2_NONFINITE_STAGE_MAP_COMPLETE_READY_FOR_GPT_REVIEW`**

- 452 个 Issue #21 非有限候选点**全部**获得精确的单一终态阶段分类（415 × HJB exception + 37 × KFE contaminated-row non-finite）；
- 无 `UNCLASSIFIED`（阶段 10）、无阶段 1/2/4/5/7/8/9/0 出现；
- Phase A 完整双跑逐字段精确相等（56 字段 × 452 点，0 差异）→ `BLOCKED_DLH_4D_R2_REPRODUCIBILITY_FAILURE` 未触发；
- 证据计数 452 与预期严格一致 → `BLOCKED_DLH_4D_R2_EVIDENCE_COUNT_MISMATCH` 未触发；
- 不可变 household oracle 身份逐次校验通过 → `BLOCKED_DLH_4D_R2_IMMUTABLE_HOUSEHOLD_IDENTITY_MISMATCH` 未触发。

## 2. Baseline / Issue / branch / commit

- Fresh baseline `origin/main` SHA: `4a9e7f8a9bb3e3a3a0b8b90dd9e485bf40f50d60`
- Issue #22 title/status: `DLH-4D-R2: Classify non-finite household/KFE region before any fixture revision`（OPEN）
- Accepted predecessor diagnostic commit（#21）: `a6187c31d7a1f008e94718778030c3117b6edae7`
- Accepted predecessor GE implementation（#20）: `40ec7ee3d676fc03863a3d2c2b1722b7ad53b2a5`
- Immutable household identity（每次诊断前校验）: 路径 `src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`、Git blob `57e32076f0e11c9a047e1f90f8c2446d4148e457`、SHA-256 `276D2244B389D6EDE140DAF8B1F9B0BE1F4AA859368941CED1A12BA8A5831AB8` —— 精确匹配
- Dedicated branch: `dsh/issue-22-dlh-4d-r2-nonfinite-region-diagnostic-2026-08-30`（基于 fresh `origin/main`）
- Candidate commit: single coherent commit（仅授权报告文件；SHA 见 completion response）
- 环境: Python 3.11.9, numpy 2.4.6, scipy 1.17.1（`scikits.umfpack` 不可用 → `spsolve` 走 SuperLU）；所有诊断脚本位于 `%TEMP%`（ephemeral, untracked, 不入仓）

## 3. Required startup 清单（fail-closed 逐项）

1. fresh fetch `origin/main` ✅（`0f55c58..4a9e7f8`）
2. 读取 CURRENT rules（`project_rules/PROJECT_RULE_INDEX_CURRENT.md` 及其要求的全部规则）、`tasks/TASK_INDEX_CURRENT.md`、`docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md` ✅
3. 读取 Issue #20 / #21 body + comments + accepted reports（#20 execution / #21 feasibility certification）✅
4. 校验 immutable household blob/SHA ✅（见 §2）
5. fresh-read Issue #22 body + activation comment（chronological）✅
6. 身份/范围无 mismatch ✅（Issue 号/标题/状态与 Task Index 一致）

## 4. 诊断执行规则合规说明

- 生产文件全部只读：`src/deep_learning_hank/two_asset/**`、`src/deep_learning_hank/ge/**`、`configs/**`、`tests/**` **零修改**；
- 仅用 accepted 源函数只读：`build_cold_initialization`、`solve_matlab_faithful_hjb`、`solve_matlab_faithful_stationary_kfe`、`aggregate_stationary_household`、frozen GE candidate→`(K,w,Y,T)` 映射；
- 绕过顶层 `evaluate_ge` 的**唯一目的**是保留阶段级 warnings/exceptions（`evaluate_ge` 的 `try/except (RuntimeError, ValueError, ArithmeticError) → finite=False` 会吞掉阶段信息）；**未改动任何数值/经济方程**；
- 诊断代码全部为 ephemeral untracked script（`%TEMP%\dlh4d_r2_diagnostic.py`、`%TEMP%\dlh4d_r2_finalize.py` 等），不入仓；仅授权报告文件入仓。

## 5. Phase A — 全部 452 个非有限点的阶段分类

### 5.1 输入与计数校验

- 读取 `reports/dlh_4d_r1_frozen_fixture_feasibility_2026_08_30/DLH_4D_R1_FULL_DOMAIN_GRID.csv`，选取**恰好**所有 `finite=0` 行；
- 执行前期望 **452**，实际 **452** —— 严格一致（否则 `BLOCKED_DLH_4D_R2_EVIDENCE_COUNT_MISMATCH`）。

### 5.2 每点记录字段（`DLH_4D_R2_ALL_NONFINITE_POINTS.csv`，56 列）

候选坐标、GE `K,w,Y,T` 有限性、初始化成功/异常类与消息、HJB 成功/异常、HJB `converged`/iterations/statistic、HJB value/consumption/labor/`mu_a`/`mu_b` 有限性、iteration-operator 与 post-convergence-operator shape/nnz/data 有限性与行和 min/max、cold-start `v_b` 诊断（`init_vb_min`）、全部捕获的 SciPy/NumPy warnings（尤其 MatrixRankWarning）、KFE 成功/失败、KFE 异常类/消息、KFE contaminated-row index、contaminated matrix shape/nnz/data 有限性、raw KFE 向量有限性/最小/最大、normalization factor、aggregate 成功/失败、唯一终态阶段标签。

### 5.3 终态阶段分布（452/452 全部归类）

| 阶段 | 标签 | 计数 | 占比 |
|---|---|---|---|
| 3 | `HJB_EXCEPTION` | 415 | 91.81% |
| 6 | `KFE_CONTAMINATED_ROW_SINGULAR_NONFINITE` | 37 | 8.19% |
| 其余（1,2,4,5,7,8,9,10,0） | — | 0 | 0 |

- GE pre-household mapping（阶段 1）: 452/452 全有限（`r_a+delta > 0`，`K,w,Y,T` 均有限）——**无** GE 映射类失败；
- 冷初始化（阶段 2）: 452/452 全部成功且输出有限——**无** 初始化失败；
- HJB non-convergence / non-finite-output（阶段 4/5）: **0**；
- KFE normalization（阶段 7）: **0**；
- aggregate（阶段 8）: **0**；
- 其他显式异常（阶段 9）/ unclassified（阶段 10）: **0**。

### 5.4 HJB_EXCEPTION（415）机制细分

全部 415 个异常均为**同一** `ValueError`，消息逐字一致：

```
designated transfer FOCs require positive liquid derivatives
```

由 immutable oracle 内 `select_matlab_faithful_local_policy` 的忠实守卫
`if min(v_b_forward, v_b_backward) <= 0.0: raise ValueError(...)` 在 HJB 迭代策略循环中触发（`v_b ≤ 0` 时转移 FOC 要求正液态导数）。按 cold-start 液态导数诊断 `init_vb_min`（与 HJB 完全一致的 `v_b` 构造，含边界边际效用）细分：

- **243/415（58.6%）：cold-start `v_b ≤ 0` → 第 1 次迭代立即失败。**
  恰好等于 3 个负 `r_b` 切片（`r_b ∈ {-0.05, -0.03125, -0.0125}`）× 全部 9 个 `r_a` × 全部 9 个 `L` = 81×3 = 243。机制：`r_b < 0` 时（b≥0 区 `r_b_eff = r_b < 0`）冷启动值函数随 b 递减 → `v_b` 在某状态 ≤ 0 → 忠实转移 FOC 守卫第 1 次迭代即抛错。`init_vb_min ∈ [-5.92, 0]`。
- **172/415（41.4%）：cold-start `v_b > 0`，HJB 运行若干次迭代后守卫触发。**
  位于正 `r_b` × 高 `r_a` 带：`r_b=0.00625` 于 `r_a≥0.045`（54）、`r_b=0.025` 于 `r_a≥0.075`（36）、`r_b=0.04375` 于 `r_a≥0.09`（21）、`r_b=0.0625`/`0.08125` 于 `r_a≥0.105`（18+18）、`r_b=0.1` 于 `r_a≥0.09`（25）。`init_vb_min ∈ (0, 0.589]`。

`r_a` 集中度: `0.0:27, 0.015:27, 0.03:27, 0.045:36, 0.06:36, 0.075:45, 0.09:55, 0.105:81, 0.12:81`（`r_a≥0.105` 全切片 81/81 HJB 异常）。`L` 集中度近似均匀（45–47/9 值）。HJB 异常路径未捕获到任何数值 warning（`hjb_warnings` 全部为空）。

### 5.5 KFE_CONTAMINATED_ROW_SINGULAR_NONFINITE（37）机制

全部 37 个：**HJB 正常收敛**（iterations 10–12，`convergence_statistic ∈ [4.75e-9, 9.59e-8]`，全部 < 冻结容差 `1e-7`），post-convergence operator 数据全部有限，contaminated matrix 数据全部有限；随后 faithful 静止 KFE contaminated-row solve 返回非有限 raw 向量，oracle 内 `solve_matlab_faithful_stationary_kfe` 抛出：

```
faithful contaminated-row solve is non-finite
```

（`ValueError`）。**关键 warning 证据**：37/37 点在 KFE 阶段捕获到 `MatrixRankWarning`（scipy SuperLU 报告 contaminated 矩阵奇异）→ `spsolve` 返回 NaN → 忠实函数 fail-closed 抛 ValueError。

- `r_b` 集中度: `0.1:22（59%）`, `0.08125:7`, `0.025:3`, `0.0625:3`, `0.00625:2`, `0.04375:0`（多数位于高 `r_b`，尤其 `r_b=0.1`）；
- `r_a` 集中度: `0.0:5, 0.015:4, 0.03:5, 0.045:5, 0.06:5, 0.075:8, 0.09:5`（`r_a ∈ [0, 0.09]`，`0.105/0.12` 无 KFE 失败——那里全部被 HJB 异常占据）；
- `L` 近似均匀（3–6/9 值）。

## 6. Phase B — 有限/非有限边界配对（`DLH_4D_R2_FINITE_NONFINITE_BOUNDARY_PAIRS.csv`）

- 冻结 729 网格按 #21 CSV 有限标志，确定"恰好相差一个网格步长的一个坐标"的有限↔非有限相邻对；
- 每个存在转换的 `r_a` 切片取字典序最早至多 2 对 → **14 对（28 行）**，覆盖 7 个切片（`r_a=0.0..0.09`）；`r_a=0.105/0.12` 全非有限、无转换。
- 配对性质:
  - 有限侧全部收敛（HJB converged，iterations 10–25，statistic `4.1e-9..9.7e-8` 全部 < `1e-7`），post-operator nnz `3103–3141`，行和 min 负值 `[-1.92, -0.19]`、max ≈ 0（忠实 operator 的边界行和特性）；
  - 非有限侧: 13 对为 `HJB_EXCEPTION`（相邻一步 `r_b` 即翻转），1 对为 `KFE_CONTAMINATED_ROW_SINGULAR_NONFINITE`（`(0.0, 0.00625, 0.2)` 有限 ↔ `(0.0, 0.025, 0.2)` KFE 失败）；
  - **转换在 `r_b` 方向锐利**：有限侧以健康余量收敛，相邻一步的 `r_b` 侧即 HJB 守卫/KFE 奇异翻转；operator nnz 与行和跨边界仅微小变化 → 失败是定性翻转（`v_b` 变号 / KFE 奇异），不是 operator 的平滑退化。

## 7. Phase C — KFE 失败代表点深度算子诊断（`DLH_4D_R2_KFE_OPERATOR_REPRESENTATIVES.csv`）

- 从 37 个 KFE 阶段点，按"尽可能覆盖不同 `r_a` 切片；切片内取字典序最早 `(r_b,L)`"确定性选取 → **7 个代表**（`r_a ∈ {0, 0.015, 0.03, 0.045, 0.06, 0.075, 0.09}`，≤12 上限内）；
- 对每个代表（只读复用已构造的 post-convergence operator）:
  - state count = 800，post-operator nnz `3112–3146`，data 全有限；post row-sum min `[-1.88, -0.29]`、max `≈1e-15`；
  - contaminated matrix（transpose + 污染行置 0、对角置 1）: row index 295（`floor(0.37*800)-1`），nnz `3109–3143`，data 全有限；
  - `scipy.sparse.linalg.splu(contaminated)` 诊断: 2/7 报 **`Factor is exactly singular`**（`r_a=0.045` rep3、`r_a=0.06` rep4），5/7 生成 LU 对象但同矩阵 `spsolve` 仍返回 NaN；
  - `spsolve` 诊断: 7/7 均发出 **`MatrixRankWarning`** 且返回全 NaN raw 向量；
  - 拓扑诊断（post-operator 正非对角转移图的弱/强连通分量与 sink SCC）: weak components ∈ {1,2}，strong components ∈ {1,2}，sink SCC ∈ {1,2} —— 图高度连通，未显示大规模碎裂；**仅作诊断拓扑证据，不解释为新的家户方程、不等同于形式化 KFE 零空间**；
  - 匹配有限邻居（1 个网格步内，确定性最早）: 7/7 均存在，邻居 stage 0 `FULL_FINITE` 且 KFE 成功；邻居 post-operator nnz/行和与代表仅微差（例 rep0: 3138 vs nb 3131；rep6: 3112 vs nb 3110）——再次确认转换锐利、operator 未突变；邻居 contaminated 矩阵 splu 5/7 成功、2/7 `exactly singular`（即使有限邻居的 contaminated 矩阵也可能被 splu 判奇异，但其 `spsolve` 仍返回有限结果——`splu` "exactly singular" 标签不是 `spsolve` NaN 的完备预测器）。

## 8. 可复现性

- Phase A 完整 452 点分类**双跑**（run 1 / run 2），逐字段比较全部 **56 字段 × 452 点**；
- 精确相等: `terminal stage`、异常/警告类别（`MatrixRankWarning` 等）、到达 HJB 点的 `converged`/iterations/statistic、KFE success/failure 与 normalization 状态——**0 差异**；
- Phase B/C 在 Phase A 冻结后各运行一次（确定性选择，可复现）；
- `BLOCKED_DLH_4D_R2_REPRODUCIBILITY_FAILURE` 未触发。

## 9. Required interpretation（7 问逐答）

1. **各阶段失败的比例/计数？**
   452 点中 415（91.81%）为 `HJB_EXCEPTION`，37（8.19%）为 `KFE_CONTAMINATED_ROW_SINGULAR_NONFINITE`；其余阶段 0。

2. **单一机制还是多重机制？**
   多重但**单一主导**：91.8% 由同一个 HJB 忠实转移 FOC 守卫（`v_b ≤ 0` 抛 ValueError）主导，其内部又分两个子机制——243 点 cold-start `v_b ≤ 0`（第 1 次迭代立即失败）、172 点迭代过程中 `v_b` 变号；8.2% 为 faithful KFE contaminated-row 矩阵数值奇异（`MatrixRankWarning` + NaN raw）。

3. **主导机制是否集中于 `r_a`/`r_b`/`L` 或组合？**
   - HJB 冷启动子机制（243）= 严格 `r_b < 0`（三个负 `r_b` 切片）× 任意 `r_a` × 任意 `L`；
   - HJB 迭代子机制（172）= 正 `r_b` × 高 `r_a` 带（随 `r_b` 上升，触发 `r_a` 门槛大致上升：`r_b=0.00625→r_a≥0.045`、`r_b=0.025→r_a≥0.075`、`r_b=0.1→r_a≥0.09`），`L` 均匀；
   - KFE 子机制（37）= 高 `r_b` 集中（`r_b=0.1` 占 59%）× `r_a∈[0,0.09]`，`L` 均匀。
   → 集中度由 `(r_a, r_b)` 组合决定，`L` 基本不参与。

4. **失败前 HJB 是否收敛？**
   - 415 个 HJB 异常点：**否**——HJB 在达到收敛前抛出（243 个第 1 次迭代、172 个后续迭代）；
   - 37 个 KFE 点：**是**——HJB 正常收敛（10–12 次迭代，statistic 4.75e-9–9.59e-8 < 1e-7）后才在 KFE 阶段失败。

5. **若 KFE 主导，post-operator 有限而 contaminated 矩阵奇异/非有限？**
   KFE 非主导（8.2%），但其 37 点证据明确：post-convergence operator 数据**全部有限**、contaminated 矩阵数据**全部有限**，而 `spsolve` 发出 `MatrixRankWarning` 并返回 NaN（7/7 代表；其中 2/7 的 `splu` 直接报 `Factor is exactly singular`）→ **contaminated 矩阵在有限 post-operator 之上数值奇异/退化**。

6. **匹配的有限邻居是否显示 operator/KFE 属性的锐利转换？**
   是（Phase B + Phase C 邻居对照）：有限侧以健康余量收敛（stat 4.1e-9–9.7e-8 < 1e-7），相邻一步 `r_b`/`L` 的侧即 HJB 守卫或 KFE 奇异翻转；operator nnz 与行和跨边界仅微差（例 3138 vs 3131）→ 转换是**定性翻转**而非 operator 平滑退化。

7. **证据指向：frozen fixture 经济/网格交互、faithful KFE 数值奇异、initialization/HJB 失败、production wrapper 行为、还是混合/不明确？**
   **混合，主次明确**：
   - 主导（91.8%）指向 **initialization–HJB 交互**：frozen 冷启动在 `r_b<0` 下产生 `v_b≤0`（243），以及在正 `r_b` × 高 `r_a` 下 HJB 迭代使 `v_b` 变号（172），触发 immutable oracle 的忠实转移 FOC 守卫；
   - 次要（8.2%）指向 **faithful KFE contaminated-row 数值奇异**：有限 post-operator 下 contaminated 矩阵奇异（`MatrixRankWarning` + NaN）；
   - **排除** GE pre-household 映射（452/452 有限，阶段 1 计数 0）；**排除** production wrapper 作为成因——`evaluate_ge` 仅把同一底层异常转为通用 `finite=False`，旁路后逐阶段异常类别与原 `finite=0` 集合一一对应，未发现任何 wrapper 特有的额外失效；
   - 结论未被单一机制完全解释：两个阶段均发生，但 91.8% 集中在 HJB 守卫。

## 10. 输出文件（仅授权路径）

`reports/dlh_4d_r2_nonfinite_region_diagnostic_2026_08_30/`:

1. `DLH_4D_R2_NONFINITE_REGION_CLASSIFICATION_REPORT.md`（本文件）
2. `DLH_4D_R2_ALL_NONFINITE_POINTS.csv`（452 行，全部 56 字段阶段记录，run 1；run 2 精确相等）
3. `DLH_4D_R2_FAILURE_STAGE_SUMMARY.csv`（阶段计数/占比、`r_a`/`r_b`/`L` 集中度、机制行、可复现性行）
4. `DLH_4D_R2_FINITE_NONFINITE_BOUNDARY_PAIRS.csv`（14 对 × 2 侧，共 28 行）
5. `DLH_4D_R2_KFE_OPERATOR_REPRESENTATIVES.csv`（7 代表，含 splu/spsolve/拓扑/邻居对照）
6. `DLH_4D_R2_FORBIDDEN_OPERATION_CHECK.md`

## 11. 科学边界（scientific ceiling）

本诊断**仅**建立冻结非有限候选区域的**阶段分解机制诊断**（stage-resolved classification）。它:

- **不**验证任何 GE 稳态；**不**认证 fixture 不可行；**不**授权 fixture/domain/参数修订；**不**授权 household/KFE 重新设计；**不**修复 production solver；
- **不**提供/建议为 PASS 而改参数的方案；**不**涉及 HANK 动态/NK/区域/Deep Learning/校准/Results；
- 上述 7 项解读中的机制判断为**诊断证据驱动**的机器级别（D2 级）结论，未做人工解释升级；GPT 独立评审（fresh GitHub）后才可进入下一科学 gate。

## 12. 建议（非 binding，仅提示，不自行创建 successor Issue）

- 若需推进冻结 fixture 下的 GE 稳态调查，后续动作必须由独立 open Issue / Owner 决策（例如：在澄清"负 `r_b` 冷启动 `v_b≤0` 与高 `r_a` 迭代 `v_b` 变号"两个 HJB 子机制、以及高 `r_b` 处 KFE contaminated 奇异后，重审认证协议或授权夹具修订）。本报告不自行选择任何 route。
