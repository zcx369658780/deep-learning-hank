# DLH-4D — Forbidden-Operation Check

- Date: 2026-08-30
- Authority: GitHub Issue #20（OPEN），activation comment id `IC_kwDOT9FOGc8AAAABRes3RQ`
- Task type: `SCIENTIFIC_IMPLEMENTATION__TWO_ASSET_SINGLE_REGION_GE_STEADY_STATE`

## 1. Issue #20 forbidden operations

| Forbidden operation | Performed? | Evidence |
|---|---|---|
| 修改 `src/deep_learning_hank/two_asset/**` | **0** | oracle 只读；blob `57e32076…` / SHA `276D2244…` 在 solve 前经 `GeConfig.verify_oracle_identity` 校验 |
| 家户 redesign / 数值修正 | **0** | 未改家户方程/HJB/KFE/taper/bare-`a` FOC/contaminated-row KFE/聚合/API |
| 改变 Option A 经济学 | **0** | `K=A_hh`、`B_hh=B_gov`、`μ=1`、`Y=ZK^αL^(1−α)`、`w=F_L`、`r_a=F_K−δ`、`T=τwL−r_b·B_gov` 按合同冻结实现 |
| 改变冻结 fixture / solver domains 以取得收敛 | **0** | fixture 与 domains 未改；root 容差/协议未改；brentq NaN 处理仅为"non-finite 排除于 bracket 逻辑"（合同语义），非调参 |
| NKPC/Taylor/Fisher/货币冲击 | **0** | 无 |
| 转移动态 / IRFs | **0** | 无 |
| 区域/多省份流 | **0** | 单区域 |
| `W^L`/`W^K`/神经网络/训练/GPU | **0** | 无 |
| 经验校准/数据/回归 | **0** | `VALIDATION_FIXTURE_NOT_CALIBRATION`；无数据 |
| 福利/政策/论文 Results | **0** | 无 |
| legacy multi-province 手动 GE 迭代作为生产 solver | **0** | 使用冻结的 nested Brent 协议 |
| self-accept / merge / PR / Issue close / successor | **0** | 仅 push dedicated branch |

## 2. 不可变家户身份（每次 solve 前校验）

| 项 | 值 | 结果 |
|---|---|---|
| path | `src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py` | ✅ |
| Git blob | `57e32076f0e11c9a047e1f90f8c2446d4148e457` | ✅ 精确匹配 |
| SHA-256 | `276D2244B389D6EDE140DAF8B1F9B0BE1F4AA859368941CED1A12BA8A5831AB8` | ✅ 精确匹配（`GeConfig.verify_oracle_identity` 每次运行校验） |

→ `BLOCKED_DLH_4D_IMMUTABLE_HOUSEHOLD_IDENTITY_MISMATCH` 未触发。

## 3. 实现边界（Issue #20 Required implementation boundary）

新增仅限：
- `configs/dlh_4d_two_asset_single_region_ge_validation.toml`
- `src/deep_learning_hank/ge/__init__.py`、`two_asset_initialization.py`、`two_asset_single_region.py`（无额外 helper 进入 src；执行驱动脚本位于本地临时目录，不入库）
- `tests/test_dlh_4d_ge_{equations,solver,accounting,reproducibility}.py`
- `reports/dlh_4d_two_asset_single_region_ge_2026_08_30/`（EXECUTION_REPORT / GE_DIAGNOSTICS.csv / REPRODUCIBILITY_SUMMARY.csv / STABILITY_SUMMARY.csv / FORBIDDEN_OPERATION_CHECK）

accepted predecessor src/config/test/report 全部未修改。

## 4. Git 纪律

- 专用 branch：`dsh/issue-20-dlh-4d-two-asset-single-region-ge-2026-08-30`（基于 fresh `origin/main` `4531d4f`）。
- 恰好一个 coherent commit；仅显式 stage 上述新增路径；仅 push 专用 branch。

## 5. 结论

所有禁止操作：**0 执行**。实现严格限于 Issue #20 边界；oracle 身份每次校验通过；gate 失败将如实以 blocker 报告（不调参求 PASS）。
