# Deep Learning + HANK Startup Snapshot — CURRENT

Date: 2026-09-01

Repository: `zcx369658780/deep-learning-hank`

Local Owner-designated workspace: `D:\deep-learning-hank`

## Governance state

- live GitHub `main` = synchronized repository/code/governance authority;
- GitHub Issue = sole DSH Builder authority only after publication + Task Index / Startup synchronization + authoritative activation comment;
- DSH = bounded Builder/executor;
- ChatGPT = independent fresh-GitHub reviewer / scientific-route advisor / task issuer / governance operator;
- Owner = final scientific-direction authority; routine bounded route decisions are delegated to ChatGPT unless Owner intervenes;
- Builder completion is not acceptance.

Priority:

`Scientific correctness > Experiment reproducibility > Research iteration speed > Git auditability > Documentation completeness`

## Current Builder state

Current published task:

**Issue #35 — DLH-5I: Map the coupled liquid-domain frontier across mature illiquid resolutions**

Task type:

`SCIENTIFIC_DIAGNOSTIC__COUPLED_BOUNDARY_DOMAIN_RESOLUTION_FRONTIER`

Dedicated branch:

`dsh/issue-35-dlh-5i-coupled-boundary-frontier-2026-09-01`

Builder authority becomes active only while Issue #35 remains OPEN, Task Index / Startup identity matches, and the authoritative activation comment is present.

Current master roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`

Historical scientific handoff:

`docs/governance/DLH_HANDOFF_2026_09_01_UPPER_DOMAIN_STATIONARY_TAIL_ROUTE.md`

## Latest accepted gate — Issue #34 / DLH-5H

Accepted candidate:

`906c98d107c8dadf6e24d841901d7eb6d53fe0d9`

Integrated to `main` by acceptance merge commit:

`f648ca270a751465ac041a4eee05cee094114ed6`

Accepted reviewer verdict:

`DLH_5H_ISSUE_34_IMPLEMENTATION_ACCEPTED__ILLIQUID_A_RESOLUTION_ADEQUACY_CONFIRMED__LIQUID_BOUNDARY_REACTIVATION_CONFIRMED__COUPLED_RESOLUTION_BLOCKER_ESTABLISHED`

Acceptance level:

`L3_COMMIT_VERIFIED__SCIENTIFIC_DIAGNOSTIC_ACCEPTED`

Key accepted interpretation:

- upper-a raw/requested outward policy is material on a20 but exact zero on a39, a77 and a153 when physical `a in [0,10]`, `a_max=10` and taper are fixed;
- therefore illiquid upper-boundary resolution adequacy is supported on the fixed physical a-domain without changing the economic/taper law;
- the former provisional liquid-safe b60 domain is not robust to a refinement: upper-b requested policy is `0` on a20 but about `0.2713`, `0.3916`, `0.4449` on a39/a77/a153;
- half-db cross-checks at the same b extent remain materially outward;
- a-resolution aligned-policy differences decline as resolution is refined but transfer/mu objects remain materially resolution-sensitive;
- no Issue #34 variant reaches joint HJB upper-boundary policy compatibility;
- stationary KFE remains NOT AUTHORIZED.

## Controlling HJB/KFE rule

```text
HJB boundary policy <=> KFE boundary transition law
```

Issue #27 stationary-KFE contract remains controlling for any later stationary validation. No stationary re-entry is authorized until a candidate grid has coherent upper-boundary HJB policy in both asset dimensions and survives the required resolution-robustness checks.

## DLH-5I exact scientific scope

DLH-5I treats the remaining household issue as a coupled domain-resolution frontier.

Frozen economics and household law:

```text
wbar = 1.0
r_a  = 0.03
a_lo = 0
a_hi = 10
a_max = 10
accepted taper = r_a*(1-0.1*(a/a_max)^9)
db = 7/19
```

Only mature diagnostic a resolutions are used:

```text
a77  = quarter baseline da
a153 = eighth baseline da
```

Liquid extents are pre-frozen at:

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

No extra/adaptive grid, no new a resolution, no b-resolution change and no a-domain widening are authorized.

## DLH-5I required diagnostic order

1. Fresh accepted HJB on all six variants; no warm start.
2. Raw + requested upper/lower a and b boundary diagnostics with complete offending-state evidence.
3. Same-a b-extent sequences `I0 -> I1 -> I2` and `I3 -> I4 -> I5`.
4. Exact aligned cross-a policy comparisons at b60, b80 and b100.
5. Per-variant joint HJB upper-boundary compatibility marker.
6. Per-b-extent cross-a joint-compatibility frontier marker.
7. Deterministic repeat and applicable full repository regression suite.
8. Stop without stationary KFE / density / tail / `C,L,A,B` execution.

If a common b extent is jointly compatible at both a77 and a153, the next scientific gate is a bounded b-resolution confirmation at the smallest compatible extent. Stationary KFE still does not begin inside DLH-5I.

## Exact Builder allowlist

Builder may create only:

1. `src/deep_learning_hank/two_asset/coupled_boundary_frontier_diagnostic.py`
2. `configs/dlh_5i_coupled_boundary_frontier_diagnostic.toml`
3. `tests/test_dlh_5i_coupled_boundary_frontier_diagnostic.py`
4. `reports/dlh_5i_coupled_boundary_frontier_diagnostic_2026_09_01/` with exactly eight files:
   - `DLH_5I_VARIANT_STATUS.csv`
   - `DLH_5I_BOUNDARY_DIAGNOSTICS.csv`
   - `DLH_5I_EXTENT_TRENDS.csv`
   - `DLH_5I_CROSS_A_POLICY_STABILITY.csv`
   - `DLH_5I_JOINT_COMPATIBILITY_FRONTIER.csv`
   - `DLH_5I_REPRODUCIBILITY.json`
   - `DLH_5I_EXECUTION_REPORT.md`
   - `DLH_5I_FORBIDDEN_OPERATION_CHECK.md`

No existing tracked file may be modified by Builder.

## Scientific ceiling during Issue #35

Do not modify accepted HJB/KFE/regional source or Issues #23–#34 evidence; do not change physical a-domain, `a_max=10`, taper, economics/prices/parameters/tolerances/initialization; do not use a resolution outside a77/a153 or change `db=7/19`; no warm-start, adaptive/seventh grid or clipping; no stationary KFE/density/tail/aggregates; no D1-D3, two-region/multi-province GE, `31_PROVINCE_HOUSEHOLD_UPPER_DOMAIN_AUDIT`, neural training, nominal HANK, calibration, policy/welfare or Results.

No PR / merge / close / successor / self-accept from Builder.

## DSH startup sequence

1. `Set-Location D:\deep-learning-hank`;
2. verify repository / remote / worktree / staging;
3. `git fetch origin` and record fresh `origin/main`;
4. read all CURRENT project rules;
5. read `tasks/TASK_INDEX_CURRENT.md` and this Startup Snapshot;
6. read current Roadmap and historical Handoff;
7. read Issue #35 full body and latest comments, including activation;
8. read accepted Issue #34 review/evidence, Issue #31 evidence, Issue #29 evidence, Issue #27 contract, Issue #28 evidence, and accepted MATLAB-faithful HJB source read-only;
9. verify Issue / Task Index / Startup identity exactly;
10. create the exact dedicated branch from fresh `origin/main`;
11. operate only inside the Issue #35 allowlist;
12. run focused and applicable full regression tests;
13. explicit-stage only allowlist paths, commit/push, and STOP for fresh ChatGPT review.

Chat text is not Builder authority.

## Governance tooling audit note

During an earlier reviewer-side governance synchronization, a temporary file named `NONEXISTENT` was accidentally created on `main` and immediately deleted; the delete restored the prior tree before the accepted DLH-5F merge. The no-op audit commits are `84cc3894829881d81e6232bb510e4612700a9bc0` and `cb4bd714771593b435978f9ebfc9fd7eaf0b68a0`.

Issues #30, #32 and #33 were accidental tooling issues and were immediately closed as `not_planned`; they carry no scientific or Builder authority.
