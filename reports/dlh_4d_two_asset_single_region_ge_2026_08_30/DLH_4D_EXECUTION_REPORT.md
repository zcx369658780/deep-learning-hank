# DLH-4D — Minimal Single-Region Two-Asset GE Steady State — Execution Report

- Date: 2026-08-30
- Author: DSH (bounded Builder)
- Authority: GitHub Issue #20 — `DLH-4D: Implement and validate minimal single-region two-asset GE steady state`（OPEN），activation comment id `IC_kwDOT9FOGc8AAAABRes3RQ`
- Task type: `SCIENTIFIC_IMPLEMENTATION__TWO_ASSET_SINGLE_REGION_GE_STEADY_STATE`
- Status: **FAIL-CLOSED CANDIDATE — 冻结的 Option A validation fixture 不存在 GE 稳态**；冻结 solver 的 bracket 协议在 R1-consistent 区域对 R2 无 bracket（RootBracketError），证据完整保留。这不是 PASS；不修改 fixture/domains 以寻求 PASS。

## 1. Terminal classification

**`BLOCKED_DLH_4D_ROOT_BRACKET_FAILURE`**

根因（evidence-based，见 §4）：冻结 fixture（`B_gov=1.0`、`Z=1`、`α=0.36`、`δ=0.025`、`rho=0.02`、a-grid 上限 10）下，债券市场清算 `R2=B_hh−B_gov=0` 仅在 `r_a ≲ 0.038` 可行，而资本市场清算 `R1=A_hh−K=0` 需 `r_a ≳ 0.050`；两区域无重叠 → 三方程系统（`R1,R2,R3`）无解。冻结 solver 在 R1-consistent 区域调用内层 R2 bracket 时正确 fail-closed。

## 2. Baseline / Issue / branch / commit

- Fresh baseline `origin/main` SHA: `4531d4f329cc3ef721ba2cdbe70587b3c016d882`
- Issue #20 title/status: OPEN；activation comment `IC_kwDOT9FOGc8AAAABRes3RQ`
- Accepted DLH-4C Option A contract commit: `7fcfd6412c580f888d2ef8175335c3909f146e59`
- Immutable household identity（每次 solve 前 `GeConfig.verify_oracle_identity` 校验）：blob `57e32076f0e11c9a047e1f90f8c2446d4148e457`、SHA-256 `276D2244B389D6EDE140DAF8B1F9B0BE1F4AA859368941CED1A12BA8A5831AB8` —— 精确匹配（`BLOCKED_DLH_4D_IMMUTABLE_HOUSEHOLD_IDENTITY_MISMATCH` 未触发）
- Dedicated branch: `dsh/issue-20-dlh-4d-two-asset-single-region-ge-2026-08-30`（基于 fresh `origin/main`）
- Candidate commit: single coherent commit（SHA 见 completion response）

## 3. Frozen Option A implementation（交付完成）

- 厂商：`Y=Z·K^α·L^(1−α)`；`w=(1−α)·Z·(K/L)^α`；`r_a=α·Z·(K/L)^(α−1)−δ`；`K=L·(αZ/(r_a+δ))^(1/(1−α))`（`r_a+δ>0`）
- 财政：`T=τ·w·L−r_b·B_gov`；`G=0`
- 家户（不可变 oracle）输入：`r_a`、`r_b`、`tau`、`wages=[w]`、`migration_costs=[0]`、`labor_weights=[1]`、`transfer_income=T`、`borrowing_rate_gap=rb_gap`
- 未知量 `x=(r_a,r_b,L)`；残差 `R=(A_hh−K, B_hh−B_gov, L_hh−L)`（未静默添加方程）
- Solver：嵌套确定性 brentq（inner `R2`→`r_b`；middle `R3`→`L`；outer `R1`→`r_a`）；domains `r_a∈[0,0.12]`、`r_b∈[−0.05,0.10]`、`L∈[0.2,3.0]`；bracketing 协议（full interval → 9-point scan → 恰一 bracket；0/multiple → fail closed）；`xtol=1e-10`、`maxiter=100`；brentq 内 NaN（家户 KFE 奇异候选）按"non-finite 排除于 bracket 逻辑"处理（不调参）
- 冷初始化（oracle 外）：`r_b_eff=r_b+rb_gap`（b<0）；`net_wage=(1−τ)w·z`；`c0(l)=net_wage·l+T+r_b_eff·b`；静态劳动 FOC `l^φ=net_wage·c0^(−γ)`（brentq）；初始消费含 `r_a_eff(a)·a`；初始值 `flow_utility/ρ`——逐候选点确定性冷启动
- Faithful 资源核算（oracle 外只读）：`AC=Σ hjb.adjustment_cost·kfe.density·db·da`；`W_taper=Σ(r_a−r_a_eff(a))·a·g·db·da`；`R_resource_structural=Y−C−δK−AC`；`R_resource_faithful=R_resource_structural−W_taper`（gate 对象）

## 4. 决定性证据（冻结 fixture 无 GE 稳态）

证据文件：`DLH_4D_FEASIBILITY_DIAGNOSTICS.csv`、`DLH_4D_FORCED_BRACKET_CHECK.csv`。

### 4.1 可行性扫描（r_a ∈ [0.030, 0.060]，每行在 R3 一致的 L*=L_hh≈0.87-0.90 处）

| r_a | L* | B_hh min | B_hh max | R2 跨越 1.0？ | K | A_hh | R1=A_hh−K |
|---|---|---|---|---|---|---|---|
| 0.0300 | 0.900 | 0.025 | 4.660 | **YES** | 16.95 | 8.81 | −8.14 |
| 0.0375 | 0.897 | 0.579 | 4.568 | **YES** | 13.84 | 9.16 | −4.68 |
| 0.0400 | 0.893 | 1.031 | 4.550 | NO | 12.96 | 9.06 | −3.90 |
| 0.0475 | 0.875 | 1.562 | 4.484 | NO | 10.70 | 8.79 | −1.91 |
| 0.0500 | 0.872 | 1.704 | 4.464 | NO | 10.11 | 8.73 | −1.38 |
| 0.0525 | 0.870 | 1.831 | 4.431 | NO | 9.59 | 8.70 | −0.89 |
| 0.0600 | 0.867 | 2.096 | 4.359 | NO | 8.27 | 8.64 | **+0.37** |

（完整 12 行见 CSV；`A_hh≈8.6-9.3` 已接近 a-grid 上限 10。）

### 4.2 无解证明（evidence-based）

1. **R2（债券清算）可行性边界**：`B_hh(r_b)` 在 `[r_b_low, r_b_high]` 上跨越 `B_gov=1.0` 仅当 `r_a ≤ ~0.038`（`r_a=0.0375` 时 min B_hh=0.579；`r_a=0.040` 时 min=1.031 > 1.0）。
2. **R1（资本清算）根位置**：`R1=A_hh−K` 在 R3 一致点随 r_a 单调上升，穿越零约在 `r_a ≈ 0.055-0.06`（`r_a=0.0525` 时 −0.89；`r_a=0.060` 时 +0.37）——因为 `K=L·(αZ/(r_a+δ))^(1/(1−α))` 随 r_a 下降而 `A_hh` 受 a-grid 上限（≤10）约束。
3. **无重叠**：R1=0 所需 `r_a ≥ ~0.05` 处 R2 恒为 `B_hh−1.0 ≥ +0.7`（无根）；R2=0 可行处（`r_a ≤ ~0.038`）R1 恒为负（`K > A_hh`，家户 illiquid 容量不足）。→ **三方程系统无同时解。**
4. **冻结 solver 的 fail-closed 捕获**：在 R1-consistent 区域（`r_a=0.052`）对 R2 执行冻结 bracket 协议 → `RootBracketError`（零 sign-changing bracket），符合合同"zero brackets → fail closed"。
5. 经济直觉：使家户持有 `K=A_hh≈8.7-9.3`（r_a≈0.05 ≫ rho=0.02）时，家户足够富有以致 liquid 持有 `B_hh ≥ 1.7` 在任何债券回报下都超过供给 1.0；压低 r_a 使债券清算可行时，资本需求 `K≈13.8` 又超过家户最大 illiquid 持有 10。

### 4.3 未触发/已通过的 gates

| Gate | 状态 |
|---|---|
| 1. immutable household identity | PASS（每次 solve 前校验；`276D2244…`） |
| 2-9. 单点家户/KFE/资源/财政/wealth/nan（在可行候选处） | 单点评估有限且家户收敛（见测试与诊断）；**GE root gates 因系统无解不适用** |
| 10. deterministic repeat / 11. local stability | 不适用（无 root 可重复/扰动；冻结 solver 已 fail-closed 于 bracket） |
| 12. predecessor regression | PASS：128 passed / 0 failed（109 accepted + 19 new DLH-4D machinery tests） |

## 5. 测试结果

- 新 DLH-4D 机制测试（`test_dlh_4d_ge_{equations,solver,accounting,reproducibility}.py`）：**19 passed / 0 failed**（10.7 s）。
- accepted predecessor regression + DLH-4D：**128 passed / 0 failed**（201 s，无回归）。

## 6. Environment / reproducibility

- Python `3.11.9`；numpy `2.4.6`；scipy `1.17.1`；pytest `8.2.1`（零安装；无 GPU）。
- 确定性单线程 CPU；无随机；单点 GE 残差评估 repeat diff `0.0`（`test_ge_evaluation_deterministic_at_fixed_candidate`）。

## 7. Exact changed paths（仅新增；无 accepted 路径修改）

1. `configs/dlh_4d_two_asset_single_region_ge_validation.toml`
2. `src/deep_learning_hank/ge/__init__.py`
3. `src/deep_learning_hank/ge/two_asset_initialization.py`
4. `src/deep_learning_hank/ge/two_asset_single_region.py`
5. `tests/test_dlh_4d_ge_equations.py`
6. `tests/test_dlh_4d_ge_solver.py`
7. `tests/test_dlh_4d_ge_accounting.py`
8. `tests/test_dlh_4d_ge_reproducibility.py`
9. `reports/dlh_4d_two_asset_single_region_ge_2026_08_30/DLH_4D_EXECUTION_REPORT.md`
10. `reports/dlh_4d_two_asset_single_region_ge_2026_08_30/DLH_4D_FEASIBILITY_DIAGNOSTICS.csv`
11. `reports/dlh_4d_two_asset_single_region_ge_2026_08_30/DLH_4D_FORCED_BRACKET_CHECK.csv`
12. `reports/dlh_4d_two_asset_single_region_ge_2026_08_30/DLH_4D_FORBIDDEN_OPERATION_CHECK.md`

## 8. Evidence boundary / 建议（非 binding）

- 本任务只验证最小单区域双资产实 GE 稳态 fixture（围绕不可变 oracle）；不涉及 HANK 动态/NK/区域/DL/校准/Results。
- 冻结 fixture 无 GE 稳态是 **fixture 参数组合**的属性（`B_gov`、`rho`、a-grid 上限与逆 MPK 映射的相互作用），非 oracle 或 solver 缺陷；**未修改 fixture 以寻求 PASS**（Issue #20 禁令）。
- 后续选项（均须独立 open Issue / Owner 决策）：① 调整 fixture（如更高 `B_gov`、更高 `rho`、更大 a-grid 上限、或非单位 `B_gov` 与均衡匹配）；② 重审 DLH-4C Option A 的 `B_gov` 约定（如令 `B_gov` 为均衡内生成分或零净供给）。本报告不自行选择。
