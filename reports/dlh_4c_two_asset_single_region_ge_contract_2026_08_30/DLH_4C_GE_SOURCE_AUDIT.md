# DLH-4C — GE Source Audit（通用均衡闭合源码审计）

- Date: 2026-08-30
- Authority: GitHub Issue #19 — `DLH-4C: Freeze minimal single-region two-asset GE steady-state closure contract`（OPEN），activation comment id `IC_kwDOT9FOGc8AAAABReZw8Q`
- Task type: `SCIENTIFIC_DESIGN__TWO_ASSET_SINGLE_REGION_GE_CLOSURE_CONTRACT`（source-audit / design-contract only；无 GE 实现）
- 参考（read-only）：`zcx369658780/dissertation-ch5-two-asset-hank` `docs/CH5_TWO_ASSET_HANK_MATLAB_FAITHFUL_GE_STEADY_STATE_CLOSURE_SOURCE_AUDIT_AND_CONTRACT_FREEZE_REPORT.md`、`exports/matlab_faithful_two_asset_ha.py`；DeepLearning-HANK fresh `main`（`2b852de9fe3e8f95b80948f77d3cd17a2222e4a6`）。

## 1. 审计范围

本文件审计 legacy multi-province MATLAB GE 闭合（`main.m` → `multi_prov_HANK_12sts.m` → `mpHANK_equilibrium_2000.m` → `HANK_mp_1eq.m`/`HANK_mp_1turn.m` → `HANK_2ASSETS_HJB.m`/`HANK_firm.m`），判定哪些可作为新单区域闭合的 provenance、哪些**不得**被盲目复制。审计内容与 Chapter-5 已接受审计报告一致（该报告终分类为 `MATLAB_FAITHFUL_GE_STEADY_STATE_CLOSURE_OWNER_PROVENANCE_REQUIRED`，即 legacy 闭合本身未被接受为合同）。

## 2. Legacy GE 闭合的关键事实（证据）

### 2.1 不存在唯一 GE residual vector / root solver
- 无 `fsolve`/`fzero`/`lsqnonlin` GE 级调用（`HANK_2ASSETS_HJB.m:106` 的 `fzero` 是家户劳动 FOC 子求解，非 GE root）。
- 收敛由**手动顺序更新**驱动：`NKrationgap(i)=|KNratio/tKNratio−1|`（K/L 资本-劳动固定点 gap）、`Ytgap(i)=|Yt/Yt_1−1|`、`convergent_total==31`、`maxra==0 && minra==0`（`HANK_mp_1eq.m:31-42`）；`tKNratio` 以 `0.6*KNratio+0.4*tKNratio` 阻尼。
- 无 joint unknown vector：状态对象（`Zt,GovInv,w,rb,rah,ra,wjt,Kt,Lt,Yt,Tt,tau,rb_gap,pit,totalpit`）为逐省顺序派生对象，非 residual 排序。

### 2.2 缺失的方程（新合同必须讨论，不得继承遗漏）
- **无 bond-market-clearing 方程**：`Bt` 仅进入 `GovSurplus` 诊断（`HANK_mp_1turn.m:65` `GovSurplus += Govinc−Bt*rb*N`）；无债券供给目标。
- **无 goods/resource 方程**：`Ct` 进入 `Lt_seperate` 与 `Ct_total` 报告，不进入任何资源约束。
- **无政府预算零条件**：`Govinc`/`GovSurplus` 为诊断累加器，不回馈、不以零为靶。
- **无 numeraire 方程**。

### 2.3 显式闭合答案（Chapter-5 audit §"Explicit closure answers"）
1. `rb` 仅由 Taylor 顺序派生（`it=istar+rho_pi*totalpit+epsilon_pi`，`rb=it−totalpit`，`istar=.015`，`rho_pi=1.25`），非 root unknown；
2. `rah` 由跨省 `ra` 与持有权重派生（`HANK_mp_1turn.m:40`），无残差方程闭合；
3. 家户 `w` 由 `wage_caculate` 派生；厂商 `wjt` 为边际产出并裁剪 `[0.8,1.3]`；
4. `Tt=0.1`、`tau=0.05`、`rb_gap=0.07` 为**固定 primitive**，非预算平衡/内生；
5. 生产性私人资本使用 `At*N`（跨省供给）+ `GovInv`；`Bt` 或 `At+Bt` 均不清偿生产性资本；
6. 无液态债券供给/清算目标；
7. 厂商劳动用 `Lt_supply`（迁移派生），非家户聚合 `Lt` 精确值；
8. `Ct` 不进入资源条件；`AtTax` 进入 `Govinc` 但无闭合方程。

### 2.4 可作 provenance 的元素（非自动 authority）
- 厂商块公式：`Y=Zt*Kt^alpha*Lt^(1-alpha)`；`rk=mt*alpha/(Kt/Yt)`；`wt0=mt*(1-alpha)*Zt*(Kt/Lt)^alpha`；`It=Kt−Kt_1+delta*Kt`（`delta=.025`）；`ra0=rk−delta+divrate`，`divrate=PIt*(1−corptau)/Kt`（`HANK_firm.m:30-54`）。
- 家户聚合语义：`Bt=Σb·g·db·dah`、`At=Σa·g·db·dah`、`Lt=Σz·l·g·db·dah`、`Ct=ΣC·g·db·dah`（`HANK_2ASSETS_HJB.m:360-363`）。
- 网格/参数（作为 fixture 参考）：`b∈[-2,5]` I=20、`a∈[0,10]` J=20、`z=[0.8,1.3]`；`chi0=.1, chi1=2, a_bar=1e-6`；`ga=2, phi_l=5, frisch_l=.2, rho=.05, epsilon=10, theta=100, delta=.025`；`ramin=.02, ramax=.09`。
- **不得复制**：跨省加权 return 公式（`inter_prv_ratio`）、手动 `Zt/GovInv` 启发式更新（`HANK_mp_1eq.m:49-56`）、Taylor 派生 `rb`（NK 层属未来扩展）、无残差向量的顺序收敛（新合同须显式 residual map）。

### 2.5 隐含自由度（legacy 欠定/非正式）
- `Tt`、`tau`、`rb_gap`、`GovInv_ratio`、`Ztratio` 等 primitive 无平衡/闭合来源 → 校准自由度隐含存在于这些选择中；
- `GovInv` 与 `ra` 边界触发联动（±10% 启发式）→ 资本存量供给无显式方程；
- 无债券市场 → `r_b`/`B` 的确定机制缺失（仅 Taylor 机械派生）；
- 无资源方程 → `Ct` 与产出/投资/调整成本的资源一致性未校验。
→ 结论：**legacy 闭合不可直接作为新单区域合同的 residual-map 模板**（与 Chapter-5 audit 结论一致）。

## 3. 可复用的接口 provenance（one-asset 路线）

- accepted DLH-3A/3B（one-asset）合同提供了单区域 GE 惯例的先例：恒定债券供给 `B`（`B_t≡B`，`Ḃ≡0`）、平衡预算转移 `tr=τ_l·w·N−r·B`、资产清算 `A_hh=B`、`G=0`、财富流恒等式作为交叉一致性残差。
- 注意：该路线为**单资产**；DLH-4C 需将其惯例扩展到双资产（illiquid → 生产性资本；liquid → 债券），并补上 legacy 缺失的 goods/resource 方程（作为诊断，见合同 E 节推导）。
- 使用边界：one-asset GE 材料仅作 interface/diagnostic provenance，**不**作为 DLH-4C 最终科学 authority。

## 4. 结论

Legacy multi-province GE 闭合**不可直接采用**（无唯一 residual vector、无 bond/resource/numeraire 方程、手动顺序更新、隐含自由度）。新单区域合同必须：显式定义 unknown vector 与 residual map、显式资产映射、显式资源核算（含调整成本）、显式 numeraire，并满足 `ACCEPTED_IMMUTABLE_HOUSEHOLD_STRUCTURE` / `NUMERICAL_REGULARIZATION` / `NEW_SINGLE_REGION_GE_CLOSURE_DESIGN` 三层分离。

## 5. Addendum（2026-08-30，per Owner Decision + GPT targeted revision authority）

1. **Owner 选定 Option A**（`IC_kwDOT9FOGc8AAAABReicYg`）：Aiyagari-minimal、恒定政府债券、竞争厂商；`K=A_hh`、`B_hh=B_gov`、`μ=1`、`x=(r_a,r_b,L)`、`R=(A_hh−K, B_hh−B_gov, L_hh−L)`。B/C 为历史备选。
2. **Taper-wedge 资源核算发现**（GPT review `IC_kwDOT9FOGc8AAAABRegOmw`，Owner 接受）：不可变 oracle 使用状态依赖有效 illiquid 回报 `r_a_eff(a)=r_a·(1−0.1·(a/a_max)^9)`，故精确稳态聚合恒等式含 `∫r_a_eff(a)·a·g` 而非 `r_a·A_hh`；定义 `W_taper=∫[r_a−r_a_eff(a)]·a·g`（`NUMERICAL_REGULARIZATION`）；faithful 资源残差 `R_resource_faithful = Y−C−δK−AC−W_taper = 0` 为 gate 对象（不得强制结构 gap 归零）。
3. **AC 聚合澄清**：`AC = Σ hjb.adjustment_cost·kfe.density·db·da`（oracle 外只读）。
4. **Option C 记号修正**（provenance）：`K=A_hh+K_gov` 时资本清算残差须为 `A_hh−(K−K_gov)`。
5. 修订后终分类：**`DLH_4C_OPTION_A_GE_CLOSURE_CONTRACT_REVISED_READY_FOR_GPT_REVIEW`**。
