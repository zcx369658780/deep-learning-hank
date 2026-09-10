# Deep Learning + HANK Task Index

Status: `ACTIVE_BUILDER_ISSUE__DLH_5VA_REGULAR_VORONOI_FRONTIER_PHASE_ADJACENCY`

Last synchronized: 2026-09-10

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

Current Issue:

**Issue #49 — OPEN**

Title:

`DLH-5V-A: Classify regular restricted-Voronoi W-frontier phases and adjacency`

Task type:

`SCIENTIFIC_DESIGN__REGULAR_VORONOI_FRONTIER_PHASE_AND_ADJACENCY_CLASSIFICATION`

Dedicated branch:

`dsh/issue-49-dlh-5va-voronoi-frontier-phase-adjacency-2026-09-10`

Owner split-gate decision:

`APPROVE_DLH_5VA_SPLIT_GATE__REGULAR_FRONTIER_PHASE_ADJACENCY_ONLY`

Issue #49 is the sole DSH Builder authority only while it remains OPEN, CURRENT Task Index / Startup identity matches, and the authoritative activation comment is present. Chat text alone does not create Builder authority.

## Superseded Issue #48

Issue #48 / the original broad DLH-5V gate is CLOSED `not_planned` because repeated Builder context/output exhaustion prevented completion before any scientific deliverable was created.

No Issue #48 candidate commit exists and its designated remote branch was never created. This is an operational scope failure, **not a scientific outcome**. No accepted DLH-5U authority changed.

## Latest accepted scientific task — Issue #47 / DLH-5U

Accepted Rev-1 candidate:

`81bf9b46f20e6dd96514bb6fad698097c917a948`

Reviewer acceptance:

`5521379228`

Acceptance integration:

`060c2835825f9efff4f89c84646f04cab6a9c8a4`

Accepted verdict:

`DLH_5U_REV1_ACCEPTED__OUTCOME_B_CONFIRMED__ROUTE_F_FRAMEWORK_ACCEPTED__TANGENTIAL_SAME_PROCESS_CONSISTENCY_REMAINS_THE_SINGLE_BOUNDED_OPEN_OBJECT`

Accepted household source remains immutable/read-only:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Binding law:

```text
HJB boundary policy <=> KFE boundary transition law
```

Stationary KFE remains **NOT AUTHORIZED**.

## Current DLH-5V-A target

This is a deliberately smaller replacement gate. It covers only regular nondegenerate W-frontier geometry away from axial endpoints/corners.

Accepted objects:

```text
D_W(W_max) = {0<=a<=a_max, b>=b_min, a+b<=W_max}
S(W_max)   = {s=(a_j,b_i): a_j+b_i<=W_max}
C_s        = {x in D_W: ||x-s||<=||x-r|| for all represented r}
```

Exact grid:

```text
da=10/19, db=7/19, da/db=10/7
```

Builder must classify the finite recurring regular W-line phases and derive actual restricted-Voronoi shared-face neighbor/displacement sets. Moment cones, transition rates, face-flux moment tests, exact sliding rates, endpoints/corners and implementation are deferred.

## Required scientific reading budget

After all CURRENT project rules and current governance files, scientific history is limited to:

1. `docs/design/DLH_5U_W1_FACE_ADAPTED_FINITE_VOLUME_SAME_PROCESS_DISCRETIZATION.md`
2. `reports/dlh_5u_w1_face_adapted_fv_same_process_2026_09_03/DLH_5U_CONTROL_VOLUME_GEOMETRY_AND_BOUNDARY_LOCATION.md`

Verify the accepted household blob without rereading the full source unless a direct contradiction appears. Do not reread superseded Issue #48 or the full historical DLH-5T / Issue #27 packages for this bounded task.

## Exact Builder allowlist

1. `docs/design/DLH_5VA_REGULAR_VORONOI_FRONTIER_PHASE_AND_ADJACENCY.md`
2. `reports/dlh_5va_regular_voronoi_frontier_2026_09_10/DLH_5VA_AUTHORITY_CAPSULE.md`
3. `reports/dlh_5va_regular_voronoi_frontier_2026_09_10/DLH_5VA_PHASE_CLASSIFICATION.md`
4. `reports/dlh_5va_regular_voronoi_frontier_2026_09_10/DLH_5VA_VORONOI_ADJACENCY_AND_DISPLACEMENTS.md`
5. `reports/dlh_5va_regular_voronoi_frontier_2026_09_10/DLH_5VA_TERMINAL_AND_FORBIDDEN_CHECK.md`

No existing tracked file may be modified by Builder.

## Scientific ceiling

Issue #49 is design-only. Do not mutate source; run HJB/KFE/stationary; select numerical `W_max`; change grid/economics; compute moment cones or rates; analyze endpoint/corner transitions beyond marking them deferred; agglomerate cells; compute aggregates/GE; enter multi-province/neural/nominal/calibration/policy/welfare/Results; or PR/merge/close/successor/self-accept.

Current Startup Snapshot:

`docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`

Current Master Roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
