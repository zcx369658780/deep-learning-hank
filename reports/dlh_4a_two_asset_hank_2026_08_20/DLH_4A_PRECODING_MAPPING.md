# DLH-4A — Pre-Coding Documentation: State-Space / HJB / Generator / Asset-Accounting Mapping

- Date: 2026-08-20
- Authority: GitHub Issue #17 — `DLH-4A: Python Reconstruction of Two-Asset HANK Household HJB and KFE Kernel`（OPEN），activation comment id `IC_kwDOT9FOGc8AAAABP6r2jg`
- Task type: `SCIENTIFIC_IMPLEMENTATION__TWO_ASSET_HANK_HJB_KFE_RECONSTRUCTION`
- 科学参考（只读 legacy）：`D:\MatlabProgram\2023年12月2日 多省份神经网络HANK\HANK_2ASSETS_HJB.m`（SHA-256 `049136B769560040BC678F828F5D3EC5338DDCAA2090D6BED4E40732F56C3EAE`）、`HANK3_FOC.m`、`HANK3_cost.m`、`lab_solve2.m`、`multi_prov_HANK_12sts.m`（哈希见 R1A 审计 manifest）。
- 本文件满足 Issue #17 "Required Pre-coding Documentation" 四项：state-space mapping、HJB equation mapping、generator mapping、asset accounting mapping。
- 全部数值为 `VALIDATION_FIXTURE_NOT_CALIBRATION`；本任务是**家户内核重建**（给定聚合价格），不含厂商/货币/财政/区域/神经模块。

## 0. 重建目标

忠实重建 Matlab 双资产家户 HJB + KFE 内核的**经济结构**与**数值算法家族**（upwind HJB、无穷小生成元 G = G_b + G_a + G_z、转置 KFE、密度归一化），不 collapse 为单资产、不以简单储蓄漂移替代调整成本。

## 1. State-space mapping（状态空间映射）

| 对象 | Matlab（legacy） | Python（reconstruction） |
|---|---|---|
| 液态资产 | `b`，网格 `[bmin,bmax]=[-2,5]`，I=20，`db` | `b`，同网格（20 点，[-2,5]），可为负（借贷） |
| 非液态资产 | `ah`，网格 `[amin,amax]=[0,10]`，J=20，`dah` | `a`，同网格（20 点，[0,10]），`a ≥ 0` |
| 生产率 | `z`，`[zmin,zmax]=[0.8,1.3]`，Nz=2；`la_mat`（2×2，非对角 1/3） | `z`，两状态 CTMC（强度 1/3/1/3） |
| 分布 | 密度 `g(b,ah,z)`，`∫g db dah dz = 1` | 密度 `g(b,a,z)`，同归一化 |
| 家户控制 | `c` 消费、`l` 劳动、`d` 资产转移（illiquid 购买量） | 同 |
| 聚合对象 | `Bt=∫b g`、`Aht=∫ah g`、`Lt=∫z l g`、`Ct=∫C g` | `B_hh=∫b g`、`A_hh=∫a g`、`L_hh=∫z l g`、`C_hh=∫c g` |
| 区域维度 | 31 省（本内核之外） | 无（单区域内核） |

**禁止**：合并两资产（`A_hh ≠ B_hh`，必须分别报告）；collapse 为 `(a,z)`。

## 2. HJB equation mapping（HJB 方程映射）

### 2.1 连续时间 HJB（经济结构）
`ρ V(b,a,z) = max_{c,l,d} { u(c) − v(l) + V_b·ḃ + V_a·ȧ + (Q V)(b,a,z) }`

- 液态漂移：`ḃ = (1−τ) w z l + Rb(b)·b + Tt − c − d − χ(d,a)`
  - `Rb(b) = rb`（b ≥ 0），`Rb(b) = rb + rb_gap`（b < 0，借贷溢价）
- 非液态漂移：`ȧ = d + raah(a)·a`，`raah(a) = ra·(1 − 0.1·(amax/a)^(−9))`（曲率收益；`a=0` 时 `raah=ra`）
- 调整成本：`χ(d,a) = chi0·|d| + chi1·d²/2·max(a, a_bar)^(−1)`
- 效用：`u(c) = alphac·c^(1−ga)/(1−ga)`；`v(l) = alphal·l^(1+1/frisch_l)/(1+1/frisch_l)`
- 消费 FOC：`u'(c) = V_b`
- 劳动 FOC（静态）：`v'(l) = (1−τ) w z V_b`
- 转移 FOC（`HANK3_FOC` 等价，inaction band）：
  `d = ( min(V_a/V_b − 1 + chi0, 0) + max(V_a/V_b − 1 − chi0, 0) ) · a / chi1`
  （`V_a/V_b ∈ [1−chi0, 1+chi0]` 时 `d=0`；高于上带买入 illiquid，低于下带卖出）

### 2.2 数值算法家族（upwind HJB，镜像 Matlab `HANK_2ASSETS_HJB.m`）

| 步骤 | Matlab | Python（reconstruction） |
|---|---|---|
| b 方向导数 | `VbF`（前向，上界用 `u'(c0)`）、`VbB`（后向，下界用 `u'(c0)`） | 同 |
| a 方向导数 | `VahF`（前向，上界 `0`）、`VahB`（后向，下界 `0`） | 同 |
| 消费候选 | `C_F/C_B/C_0`，upwind 选择 `Ic_F/Ic_B/Ic_0`（液态储蓄方向） | 同 |
| 劳动候选 | `l_F/l_B`（用 `VbF/VbB`）+ `l0`（零漂移静态解，`lab_solve2` 等价） | 同 |
| 调整候选 | `dhBB/dhBF/dhFB/dhFF`（四组合），`dh_B/dh_F` 选择 + 边界强制 | 同 |
| 哈密顿量选择 | 消费：`Ic_*`；调整：`Idh_*`（`sdh_B/sdh_F` 符号） | 同 |
| 值迭代 | `(1/Delta + rho)I − A`，`Delta=1000`；收敛 `max|ΔV| < crit=1e-7` | 同 |
| 边界 | b 上下界 `u'(c0)`；a 上下界 `V_a=0`；`Idh_B(I,:,:)=1`、`Idh_F(I,:,:)=0` 等强制 | 同 |

### 2.3 Legacy 代码观察（忠实重建中显式处理的点）

1. **`tempMat = Rah.*raah + Rb.*bbb + Tt`**（HJB 行 84）：`Rah` 为逐节点 `raah` 值数组，`Rah.*raah` = `raah²`，与经济学不符（illiquid 收益并不进入液态现金流）；而零漂移消费 `C_0 = (1−tau)w z l0 + Tt + Rb·b`（行 96）不含该 term。重建采用**自洽版本**：零漂移劳动问题 `c0 = (1−τ) w z l0 + Tt + Rb·b`（与 `C_0` 一致），illiquid 收益仅经 `ȧ = d + raah·a` 与 HJB 包络（`V_a·raah·a`）进入。此为**有文档的 legacy 不一致修正**，非静默简化。
2. **illiquid 收益不入液态预算**：`ḃ` 中无 `ra·a` 项（与 Matlab 一致）。
3. **密度归一化**：`g` 为密度，`∫g db da dz = 1`（Matlab `g_sum = g'·ones·db·dah`），聚合用 `·db·da` 权重。

## 3. Generator mapping（生成元映射）

- 分解：`G = G_b + G_a + G_z`（液态漂移块 + 非液态漂移块 + z 转移块）。
- 布局：`M = I·J·Nz`；`z` 块序（`nz`），块内 b 最快（`row = nz·I·J + j·I + i`）。
- `G_b`：每 `(j,nz)` 列的三对角链——右流 `Z = (Ic_F·sc_F + Idh_F·sdh_F)/db`（行→行+1），左流 `X = −(Ic_B·sc_B + Idh_B·sdh_B)/db`（行→行−1），对角 `Y = −(X+Z)`；行和 0。
- `G_a`：每 `(i,nz)` 列的 a 链——上流 `zetah = MhF/da`（行→行+I），下流 `chih = −MhB/da`（行→行−I），对角 `yyh = −(chih+zetah)`；`MhB = min(dhB,0)`、`MhF = max(dhF,0) + raah·a`（上界 `MhF(:,J−1)=0`，`MhB(:,J−1)=dhB+ra·amax`）。
- `G_z`：`Bswitch`（`la_mat` 块对角，作用于相同资产节点）。
- **同一生成元同时用于 HJB**（`(1/Δ+ρ)I − G`）**与 KFE**（`G^T g = 0`）——HJB/KFE 一致性由单一算子保证。
- 行和诊断：`max|ΣG(row)| ≈ 0`（Matlab `homecrit=1e-2`；Python 用更严格门限）。

## 4. Asset accounting mapping（资产核算映射）

| 对象 | 定义 | 说明 |
|---|---|---|
| `B_hh` | `∫ b g db da dz` | 液态资产聚合（需求侧；可含 `B_hh_pos/B_hh_neg`） |
| `A_hh` | `∫ a g db da dz` | 非液态资产聚合（需求侧） |
| 禁止 | 合并资产、假设 `A_hh = B_hh` | 二者分别报告 |
| 清算诊断 | 本内核为家户块（聚合价格给定），**无供给侧**；`A_hh`/`B_hh` 作为独立聚合诊断报告 | 完整两资产 GE 清算（厂商/货币/财政闭合）不在本 Issue 授权范围 |

## 5. 验证夹具（`VALIDATION_FIXTURE_NOT_CALIBRATION`）

| 参数 | 值 | 来源 |
|---|---|---|
| `rho=0.05`、`ga=2`、`alphac=1`、`alphal=1`、`frisch_l=0.2` | Matlab `multi_prov_HANK_12sts.m` | 参考夹具 |
| `chi0=0.1`、`chi1=2`、`a_bar=1e-6`、`fixcost=0` | Matlab `CHI` | 参考夹具 |
| `b∈[-2,5]` I=20；`a∈[0,10]` J=20；`z∈{0.8,1.3}` Nz=2 | Matlab grid | 参考夹具 |
| `w=1.0`、`rb=0.02`、`rb_gap=0.01`、`ra=0.04`、`tau=0.15`、`Tt=0.0` | 家户块输入（validation fixture） | 本任务设定（Matlab 对应为均衡对象 `wjt/ra/rb` 的合理区间内） |
| `Delta=1000`、`crit=1e-7`、`maxiter=1000` | Matlab num | 参考夹具 |

**限制**：无法运行 MATLAB（未获授权），故 "MATLAB intermediate comparison" 在本任务中为**结构级对照**（方程↔代码逐项映射），并采用与 Matlab 一致的网格/参数以支持未来数值对照；Python 侧数值诊断（HJB 收敛、行和、质量、聚合）在本任务内完成。

## 6. 数值验证结果附记（ADDENDUM，2026-08-20）

本映射文档为 coding 前的目标契约；实际数值验证结果见 `DLH_4A_EXECUTION_REPORT.md` 与 `DLH_4A_DIAGNOSTICS.csv`：

- 结构重建完整（state `(b,a,z)`、`chi(d,a)`、生成元 `G=G_b+G_a+G_z`、KFE、分离核算），机制测试 15/15 通过；
- 参考镜像夹具（`rho=0.05, rb=0.02, ra=0.04` 等）上：生成元性质 PASS（行和 `1.2e-13`、非对角 ≥ 0）；但 HJB 迭代未收敛到单调值函数、`G^T` 零空间 nullity=7（平稳分布非唯一）→ Issue #17 数值验证 gates FAIL；
- 根因（evidence-based）：exogenous-return 双资产家户块在参考参数区域本质退化（liquid 全域支取至借贷下限、illiquid 调整顶格），参考算法家族本身数值脆弱（legacy `homecrit=1e-2`、`raah²`/transfer-scale 不一致）——详见 execution report §4。
- 终分类：**`BLOCKED_DLH_4A_ENGINEERING_FAILURE`**（fail-closed，非 PASS）。
