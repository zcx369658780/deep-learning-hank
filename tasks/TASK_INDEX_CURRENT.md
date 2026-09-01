# Deep Learning + HANK Task Index

Status: `ACTIVE_BUILDER_ISSUE__DLH_5J_FINAL_BOUNDED_COUPLED_B_EXTENT_CONTINUATION`

Last synchronized: 2026-09-01

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

Current Issue:

**Issue #36 — OPEN**

Title:

`DLH-5J: Complete the final bounded coupled liquid-extent continuation before asymptotic adjudication`

Task type:

`SCIENTIFIC_DIAGNOSTIC__FINAL_BOUNDED_COUPLED_B_EXTENT_CONTINUATION`

Dedicated branch:

`dsh/issue-36-dlh-5j-final-coupled-b-extent-2026-09-01`

Issue #36 becomes the sole DSH Builder authority only after the authoritative activation comment is present and the CURRENT Startup Snapshot is synchronized to the same Issue.

If Issue #36 is not open, activation is absent, or Issue / Task Index / Startup identity differs, DSH must fail closed.

## Latest accepted task — Issue #35 / DLH-5I

Accepted candidate:

`d8837e04db940b1f71b8ff1fe7e181d1bf9644a3`

Integrated to `main` by acceptance merge commit:

`53d0ff7b0fe9bd73cfbd8c6d27c98bbc4b0423d1`

Accepted reviewer verdict:

`DLH_5I_ISSUE_35_IMPLEMENTATION_ACCEPTED__COUPLED_B_EXTENT_ATTENUATION_CONFIRMED__COMMON_THRESHOLD_NOT_REACHED__UPPER_A_COMPATIBILITY_STABLE__FURTHER_BOUNDED_EXTENT_GATE_REQUIRED`

Accepted interpretation:

- upper-a/lower-a/lower-b requested policy is exact zero for all a77/a153 × b60/b80/b100 variants;
- with `db=7/19` fixed, upper-b requested policy strictly attenuates with b extent:
  - a77: `0.3915648627 -> 0.2808185297 -> 0.1925385153`;
  - a153: `0.4449370735 -> 0.3356027946 -> 0.2481811687`;
- offending upper-b states remain localized to the top-liquid/top-illiquid/high-z corner and counts/shares decline with extent;
- no b60/b80/b100 extent is jointly compatible at either mature a resolution;
- cross-a value/consumption/labor differences are small, while transfer/`mu_a`/`mu_b` remain about 1.9–2.4% apart;
- stationary KFE remains NOT AUTHORIZED.

## Issue #36 scientific scope

DLH-5J is the **final bounded grid-extent continuation** before asymptotic/high-wealth or finite-domain-closure adjudication.

Frozen on all variants:

```text
wbar = 1.0
r_a  = 0.03
a in [0,10]
a_max = 10
accepted taper = r_a*(1-0.1*(a/a_max)^9)
db = 7/19
```

Only mature a resolutions are authorized:

```text
a77
a153
```

Final pre-frozen b extents:

```text
b120 [-2,795/19]
b140 [-2,935/19]
b160 [-2,1075/19]
```

Exact six variants:

1. `J0_A77_B120`
2. `J1_A77_B140`
3. `J2_A77_B160`
4. `J3_A153_B120`
5. `J4_A153_B140`
6. `J5_A153_B160`

No seventh/adaptive grid, no b extent beyond b160, no new a resolution, no a-domain widening and no b-resolution change are authorized.

## Required evidence

1. Fresh accepted HJB on all six variants; no warm start.
2. Complete raw + requested diagnostics on all four asset boundaries with full offending-state evidence.
3. Final continuation trends using accepted DLH-5I b100 scalars as read-only anchors:
   - a77: b100 -> b120 -> b140 -> b160;
   - a153: b100 -> b120 -> b140 -> b160.
4. Exact cross-a aligned policy comparisons at b120/b140/b160.
5. Per-variant joint HJB boundary compatibility marker.
6. Per-final-extent cross-a joint-compatibility frontier marker.
7. Deterministic repeat and applicable full repository regression suite.
8. Stop without stationary KFE / density / tail / aggregate execution.

Binding route rule:

- if a common extent reaches cross-a joint compatibility, next gate is bounded **b-resolution confirmation at the smallest compatible extent**;
- if no common extent reaches compatibility by b160, do **not** publish another larger-grid continuation task; next gate must be high-wealth/asymptotic or finite-domain HJB-closure scientific adjudication.

## Exact Builder allowlist

Builder may create only:

1. `src/deep_learning_hank/two_asset/final_coupled_b_extent_diagnostic.py`
2. `configs/dlh_5j_final_coupled_b_extent_diagnostic.toml`
3. `tests/test_dlh_5j_final_coupled_b_extent_diagnostic.py`
4. `reports/dlh_5j_final_coupled_b_extent_diagnostic_2026_09_01/` with exactly:
   - `DLH_5J_VARIANT_STATUS.csv`
   - `DLH_5J_BOUNDARY_DIAGNOSTICS.csv`
   - `DLH_5J_FINAL_EXTENT_TRENDS.csv`
   - `DLH_5J_CROSS_A_POLICY_STABILITY.csv`
   - `DLH_5J_JOINT_COMPATIBILITY_FRONTIER.csv`
   - `DLH_5J_REPRODUCIBILITY.json`
   - `DLH_5J_EXECUTION_REPORT.md`
   - `DLH_5J_FORBIDDEN_OPERATION_CHECK.md`

No existing tracked file may be modified by Builder.

## Scientific ceiling

Do not modify accepted HJB/KFE/regional source or Issues #23–#35 evidence; do not change physical a-domain, `a_max`, taper, economics/prices/parameters/tolerances/initialization; do not use a resolution outside a77/a153 or change `db=7/19`; do not rerun b100 as an extra variant; no b extent beyond b160; no warm-start, adaptive/root-seeking grid or clipping; no stationary KFE/density/tail/aggregates; no D1-D3, regional GE, multi-province audit, neural training, nominal HANK, calibration, policy/welfare or Results.

No PR / merge / close / successor Issue / self-accept from Builder.

## Current route authority

- Issue #36 full body + authoritative activation comment = exact Builder experiment authority once activation is posted.
- Startup Snapshot: `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
- Roadmap: `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
- Earlier handoff remains historical context: `docs/governance/DLH_HANDOFF_2026_09_01_UPPER_DOMAIN_STATIONARY_TAIL_ROUTE.md`
