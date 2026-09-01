# Deep Learning + HANK Task Index

Status: `ACTIVE_BUILDER_ISSUE__DLH_5I_COUPLED_BOUNDARY_DOMAIN_RESOLUTION_FRONTIER`

Last synchronized: 2026-09-01

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

Current Issue:

**Issue #35 — OPEN**

Title:

`DLH-5I: Map the coupled liquid-domain frontier across mature illiquid resolutions`

Task type:

`SCIENTIFIC_DIAGNOSTIC__COUPLED_BOUNDARY_DOMAIN_RESOLUTION_FRONTIER`

Dedicated branch:

`dsh/issue-35-dlh-5i-coupled-boundary-frontier-2026-09-01`

Issue #35 becomes the sole DSH Builder authority only after the authoritative activation comment is present and the CURRENT Startup Snapshot is synchronized to the same Issue.

If Issue #35 is not open, activation is absent, or Issue / Task Index / Startup identity differs, DSH must fail closed.

## Latest accepted task — Issue #34 / DLH-5H

Accepted candidate:

`906c98d107c8dadf6e24d841901d7eb6d53fe0d9`

Integrated to `main` by acceptance merge commit:

`f648ca270a751465ac041a4eee05cee094114ed6`

Accepted reviewer verdict:

`DLH_5H_ISSUE_34_IMPLEMENTATION_ACCEPTED__ILLIQUID_A_RESOLUTION_ADEQUACY_CONFIRMED__LIQUID_BOUNDARY_REACTIVATION_CONFIRMED__COUPLED_RESOLUTION_BLOCKER_ESTABLISHED`

Accepted interpretation:

- with physical `a in [0,10]`, `a_max=10` and taper fixed, upper-a is material on a20 but exact zero on a39/a77/a153;
- the former provisional b60 liquid-safe domain is not robust to a refinement: upper-b requested rate reactivates to about `0.2713`, `0.3916`, `0.4449` on a39/a77/a153;
- half-db cross-checks at the same b extent remain material;
- the blocker is therefore coupled domain/resolution behavior rather than an isolated one-asset boundary problem;
- no pre-frozen grid is jointly HJB-boundary compatible; stationary KFE remains NOT AUTHORIZED.

## Issue #35 scientific scope

DLH-5I maps a coupled liquid-extent frontier at two mature illiquid diagnostic resolutions while preserving the accepted household process.

Frozen for all variants:

```text
wbar = 1.0
r_a  = 0.03
a in [0,10]
a_max = 10
accepted taper = r_a*(1-0.1*(a/a_max)^9)
db = 7/19
```

Only two a resolutions are authorized:

```text
a77
a153
```

Exact b extents:

```text
b60  [-2,375/19]
b80  [-2,515/19]
b100 [-2,655/19]
```

Exact variants:

1. `I0_A77_B60`
2. `I1_A77_B80`
3. `I2_A77_B100`
4. `I3_A153_B60`
5. `I4_A153_B80`
6. `I5_A153_B100`

No seventh/adaptive grid, no a-domain widening, no new a resolution and no b-resolution change are authorized.

## Required evidence

1. Fresh accepted HJB on all six variants; no warm start.
2. Raw + requested diagnostics on upper/lower a and b with complete offending-state evidence.
3. Separate same-a b-extent trends `I0->I1->I2` and `I3->I4->I5`.
4. Exact cross-a aligned policy comparisons at b60, b80 and b100.
5. Per-variant joint HJB boundary compatibility marker.
6. Per-b-extent cross-a joint-compatibility frontier marker.
7. Deterministic repeat and applicable full repository regression suite.
8. Stop without stationary KFE / density / tail / aggregate execution.

## Exact Builder allowlist

Builder may create only:

1. `src/deep_learning_hank/two_asset/coupled_boundary_frontier_diagnostic.py`
2. `configs/dlh_5i_coupled_boundary_frontier_diagnostic.toml`
3. `tests/test_dlh_5i_coupled_boundary_frontier_diagnostic.py`
4. `reports/dlh_5i_coupled_boundary_frontier_diagnostic_2026_09_01/` with exactly:
   - `DLH_5I_VARIANT_STATUS.csv`
   - `DLH_5I_BOUNDARY_DIAGNOSTICS.csv`
   - `DLH_5I_EXTENT_TRENDS.csv`
   - `DLH_5I_CROSS_A_POLICY_STABILITY.csv`
   - `DLH_5I_JOINT_COMPATIBILITY_FRONTIER.csv`
   - `DLH_5I_REPRODUCIBILITY.json`
   - `DLH_5I_EXECUTION_REPORT.md`
   - `DLH_5I_FORBIDDEN_OPERATION_CHECK.md`

No existing tracked file may be modified by Builder.

## Scientific ceiling

Do not modify accepted HJB/KFE/regional source or Issues #23–#34 evidence; do not change physical a-domain, `a_max=10`, taper, economics/prices/parameters/tolerances/initialization; do not use a resolution outside a77/a153 or change `db=7/19`; no warm-start, adaptive grid or clipping; no stationary KFE/density/tail/aggregates; no D1-D3, regional GE, multi-province audit, neural training, nominal HANK, calibration, policy/welfare or Results.

No PR / merge / close / successor Issue / self-accept from Builder.

## Current route authority

- Issue #35 full body + authoritative activation comment = exact Builder experiment authority once activation is posted.
- Startup Snapshot: `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
- Roadmap: `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
- Earlier handoff remains historical context: `docs/governance/DLH_HANDOFF_2026_09_01_UPPER_DOMAIN_STATIONARY_TAIL_ROUTE.md`
