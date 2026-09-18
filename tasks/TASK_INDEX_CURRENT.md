# 当前任务指针

更新：2026-09-18。路线：`DLH-WL-V1-20260918`。
状态：`P0_SYNC_ACCEPTED__ISSUE_74_P1A_ACTIVE_OPERATIVE`。

P0 三端同步已经完成并经 Reviewer fresh GitHub 核对：
- 项目源：Owner 已确认上传；
- DSH SYNC_ONLY：`SYNC_ONLY_COMPLETE__AWAITING_SCIENTIFIC_ISSUE`，零科学调用；
- post-sync baseline：`4d194f688cc330a71a6eda692827a4cc75b25a3c`；
- Owner 路线锁未漂移。

当前唯一科学 Builder Issue：
- #74 / `DLH-WL-P1A: frozen-household registry + offline conditional labor-destination accounting`
- 状态：**OPEN / ACTIVE / OPERATIVE**
- exact Builder branch：`dsh/issue-74-dlh-wl-p1a-offline-labor-destination-2026-09-18`
- operative baseline：以 #74 最终 activation comment 指定的 live-main SHA 为准。

#74 P1A 仅包含：现有家庭依赖证据登记 + 条件目的地份额/完整流量离线接口 + 非对称 tiny accounting tests。昂贵科学调用预算=0；无 HJB/KFE/GE、无训练、无 MATLAB、无历史 full suite。

Builder 必须 fresh-fetch，读取 #74 full body + comments，确认最终 activation 后，从指定 operative baseline 创建专用分支执行；完成后 commit/push branch、留一次 completion comment，然后 STOP，等待 Reviewer 独立验收。

当前权威：
- `docs/decisions/DLH_OWNER_ROUTE_FREEZE_WL_V1_2026_09_18.md`
- `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
- `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
- GitHub Issue #74 full body + final activation comment

旧 Task Index/Issue NEXT 仅作历史查询，不覆盖 live authority。
