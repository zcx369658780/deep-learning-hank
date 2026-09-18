# 当前任务指针

更新：2026-09-18。路线：`DLH-WL-V1-20260918`。
状态：`P0_PROJECT_SOURCE_CONFIRMED__DSH_SYNC_PENDING__ISSUE_74_STAGED_NOT_OPERATIVE`。

Owner 已确认项目源上传完成。Issue #73：CLOSED / COMPLETED。

下一科学 Builder Issue：
- #74 / `DLH-WL-P1A: frozen-household registry + offline conditional labor-destination accounting`
- 状态：**OPEN / STAGED / NOT OPERATIVE**
- 发布 baseline：`149067875aafb55869750b025302eb923fc3dd01`
- 在 DSH 完成 SYNC_ONLY 并由 Reviewer 核对、发布 activation comment 之前，Builder **不得执行 #74**。

当前唯一允许动作仍是 `docs/governance/DLH_DSH_SYNC_ONLY_PROTOCOL_CURRENT.md` 的零科学同步。即使看到 open #74，也不得将“open”解释为 operative authority。

顺序：项目源上传确认（已完成） → DSH SYNC_ONLY 回报 → Reviewer 核对 → #74 activation → DSH 在专用分支执行 P1A → Reviewer 独立验收。

#74 P1A 仅包含：现有家庭依赖证据登记 + 条件目的地份额/完整流量离线接口 + 非对称 tiny accounting tests。无 HJB/KFE/GE、无训练、无历史 full suite。

当前权威：
- `docs/decisions/DLH_OWNER_ROUTE_FREEZE_WL_V1_2026_09_18.md`
- `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
- `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
- GitHub Issue #74 full body + 后续 activation comment（仅在 activation 后成为 operative task authority）

旧 Task Index 完整原文在 archive，仅作历史查询。任何旧 NEXT ACTIVE 不覆盖 live Issue 状态与 Owner 路线。
