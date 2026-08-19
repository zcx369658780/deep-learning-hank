# 历史多省份 HANK 程序解析证据索引

本目录的定位是 **reference evidence**，不是新模型的 authority。

## 最值得先读的文件

1. `01_CODEX_CH5_MODEL_EQUATION_READONLY_REPORT_2026_06_22.md`
   - 最直接的四个主 Matlab 文件结构解析。
   - 说明 household HJB/KFE、firm、multi-province one-turn、outer fixed point 的角色。
2. `02_CODEX_MATLAB_READONLY_INSPECTION_NOTES_2026_06_22.md`
   - 关键对象、helper 和算法位置速查。
3. `04_R5_LEGACY_EQUATION_MIGRATION_MATRIX.csv`
   - 旧方程到 Python 模块的历史 RETAIN / REDESIGN 决策。
   - 所有 `old_output_authority=FALSE`。
4. `05_R5_LEGACY_MIGRATION_STATUS_2026_07_22.md`
   - 32 个 `.m` 文件的历史迁移总结。
5. `03_CODEX_PROVINCE_MODEL_OUTPUT_INVENTORY_2026_07_15.md`
   - 解释为何大量旧输出不能直接当作新模型数值真值。
6. `06_R4H_REAL_PARSER_ROUTE_CLOSEOUT_2026_07_22.md`
   - 明确旧 parser 路线已经关闭，没有 accepted runtime output。
7. `07_R5_PYTHON_AR1_REBUILD_ROADMAP_HISTORICAL_2026_07_22.md`
   - 旧 R5 Python 重构路线，只作为设计经验参考。

## 从历史代码中目前可以较安全继承的“问题地图”

- 两资产 household HJB + stationary KFE/KF block。
- 省级 firm / production / nominal / fiscal objects。
- multi-province labor-link 和 asset/return-link 的存在。
- outer fixed-point / convergence controller。
- 旧 `rah` / `inter_prv_ratio` 的语义和方向需要重新明确。
- 旧 shock implementation 与论文中的 AR(1) 表述曾存在冲突。

## 明确禁止的继承方式

- 不逐行翻译 Matlab。
- 不把旧输出当 Python / neural model 的 numerical oracle。
- 不把历史 PASS 解释成新模型的 calibration / transition / Results PASS。
- 不因为旧代码名字里写 HANK 就声称新模型是 full Spatial HANK。
