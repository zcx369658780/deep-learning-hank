# Deep Learning + HANK Task Index

Status: `ACTIVE_BUILDER_ISSUE__DLH_5VB_REGULAR_VORONOI_GEOMETRIC_MOMENT_CONE`

Last synchronized: 2026-09-11

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

Current Issue:

**Issue #50 — OPEN**

Title:

`DLH-5V-B: Regular restricted-Voronoi geometric moment-cone analysis`

Task type:

`SCIENTIFIC_DESIGN__REGULAR_VORONOI_GEOMETRIC_MOMENT_CONE`

Dedicated branch:

`dsh/issue-50-dlh-5vb-regular-voronoi-moment-cone-2026-09-11`

Owner continuation decision:

`APPROVE_DLH_5VB_REGULAR_VORONOI_GEOMETRIC_MOMENT_CONE_GATE`

Issue #50 is the sole DSH Builder authority only while it remains OPEN, CURRENT Task Index / Startup identity matches, and the authoritative activation comment is present. Chat text alone does not create Builder authority.

## Latest accepted task — Issue #49 / DLH-5V-A

Accepted candidate:

`58a0efe2e85b497d8b19c306a831d865ed65136d`

Reviewer acceptance:

`5628285587`

Acceptance integration:

`46d6961100d1a050e6b313fa2e321180ed255226`

Accepted verdict:

`DLH_5VA_ACCEPTED__OUTCOME_A_CONFIRMED__REGULAR_RESTRICTED_VORONOI_FRONTIER_PHASE_AND_ADJACENCY_FROZEN__READY_FOR_MOMENT_CONE_GATE`

Accepted household source remains immutable/read-only:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Binding law:

```text
HJB boundary policy <=> KFE boundary transition law
```

Stationary KFE remains **NOT AUTHORIZED**.

## Accepted regular-frontier geometry entering DLH-5V-B

Exact physical displacement map:

```text
Delta x_sr = ((10/19) Delta j, (7/19) Delta i)
```

W-active regular adjacency classes:

```text
A^F: (-1,0), (0,-1), (-1,+1), (+1,-1)
A^L: (-1,0), (0,-1), (-1,+1)
B^W: (-1,0), (0,-1), (0,+1), (+1,-1)
```

No oblique or longer regular shared-face neighbor is available under accepted DLH-5V-A authority.

## Current DLH-5V-B target

For each accepted W-active regular class, derive the nonnegative physical displacement cone

```text
K_s = cone{Delta x_sr}
```

and compare it with the continuous W-boundary reallocation cone

```text
T_realloc = {mu_a<=0, mu_b>=0, mu_a+mu_b<=0}.
```

Mandatory test: exact sliding `mu=(-u,+u)`, `u>0`.

This Issue determines geometric feasibility only. It does not design production rates, audit the strict face-flux moment map, close endpoints/corners, implement HJB/KFE, select `W_max`, or solve stationary KFE.

## Exact Builder allowlist

1. `docs/design/DLH_5VB_REGULAR_VORONOI_GEOMETRIC_MOMENT_CONE.md`
2. `reports/dlh_5vb_regular_moment_cone_2026_09_11/DLH_5VB_AUTHORITY_CAPSULE.md`
3. `reports/dlh_5vb_regular_moment_cone_2026_09_11/DLH_5VB_MOMENT_CONE_ANALYSIS.md`
4. `reports/dlh_5vb_regular_moment_cone_2026_09_11/DLH_5VB_TERMINAL_AND_FORBIDDEN_CHECK.md`

No existing tracked file may be modified by Builder.

## Scientific ceiling

Issue #50 is design-only. Do not mutate source/economics; redo broad phase/Voronoi enumeration; design production transition rates; audit strict face-flux moment maps; analyze endpoint/corner transitions; implement or execute HJB/KFE/stationary; choose numerical `W_max`; compute aggregates/GE; or enter multi-province/neural/nominal/calibration/policy/welfare/Results. No PR/merge/Issue close/successor/self-accept from Builder.

Current Startup Snapshot:

`docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`

Current Master Roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
