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

**Issue #36 — DLH-5J: Complete the final bounded coupled liquid-extent continuation before asymptotic adjudication**

Task type:

`SCIENTIFIC_DIAGNOSTIC__FINAL_BOUNDED_COUPLED_B_EXTENT_CONTINUATION`

Dedicated branch:

`dsh/issue-36-dlh-5j-final-coupled-b-extent-2026-09-01`

Builder authority is active only while Issue #36 remains OPEN, Task Index / Startup identity matches, and the authoritative activation comment is present.

Current master roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`

Historical scientific handoff:

`docs/governance/DLH_HANDOFF_2026_09_01_UPPER_DOMAIN_STATIONARY_TAIL_ROUTE.md`

## Latest accepted gate — Issue #35 / DLH-5I

Accepted candidate:

`d8837e04db940b1f71b8ff1fe7e181d1bf9644a3`

Integrated to `main` by acceptance merge commit:

`53d0ff7b0fe9bd73cfbd8c6d27c98bbc4b0423d1`

Accepted reviewer verdict:

`DLH_5I_ISSUE_35_IMPLEMENTATION_ACCEPTED__COUPLED_B_EXTENT_ATTENUATION_CONFIRMED__COMMON_THRESHOLD_NOT_REACHED__UPPER_A_COMPATIBILITY_STABLE__FURTHER_BOUNDED_EXTENT_GATE_REQUIRED`

Acceptance level:

`L3_COMMIT_VERIFIED__SCIENTIFIC_DIAGNOSTIC_ACCEPTED`

Accepted interpretation:

- a77/a153 both retain exact upper-a/lower-a/lower-b compatibility through b60/b80/b100;
- upper-b requested policy strictly attenuates with b extent at both mature a resolutions:
  - a77: `0.3915648627 -> 0.2808185297 -> 0.1925385153`;
  - a153: `0.4449370735 -> 0.3356027946 -> 0.2481811687`;
- offending states remain localized at `(b=b_max, a near 10, z=1.3)` and counts/shares decline with extent;
- no b60/b80/b100 extent is jointly compatible, so stationary KFE remains blocked;
- cross-a value/consumption/labor differences are small while transfer/`mu_a`/`mu_b` differences remain diagnostically material (~1.9–2.4%);
- current evidence supports finite-domain attenuation, not a claim that the stationary liquid tail fails to exist.

## Controlling HJB/KFE rule

```text
HJB boundary policy <=> KFE boundary transition law
```

Issue #27 remains the stationary-KFE contract for any later re-entry. No stationary validation begins until joint upper-boundary compatibility is established and then survives the required b-resolution confirmation.

## DLH-5J exact scientific scope

DLH-5J is the final pre-frozen larger-b experiment before analytical/asymptotic adjudication.

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

Only mature diagnostic a resolutions:

```text
a77
a153
```

Final b extents:

```text
b120 [-2,795/19]   # b_max 41.84210526315789
b140 [-2,935/19]   # b_max 49.21052631578947
b160 [-2,1075/19]  # b_max 56.578947368421055
```

Exact variants:

1. `J0_A77_B120`
2. `J1_A77_B140`
3. `J2_A77_B160`
4. `J3_A153_B120`
5. `J4_A153_B140`
6. `J5_A153_B160`

Use accepted DLH-5I b100 results only as read-only scalar anchors for continuation trends. Do not rerun b100 as an additional variant.

No b extent beyond b160 is authorized.

## DLH-5J required diagnostic order

1. Fresh accepted HJB on all six variants; no warm start.
2. Complete raw + requested diagnostics on upper/lower a and b with offending-state evidence.
3. Final continuation trends:
   - accepted a77/b100 anchor -> b120 -> b140 -> b160;
   - accepted a153/b100 anchor -> b120 -> b140 -> b160.
4. Exact cross-a policy comparisons at b120/b140/b160.
5. Per-variant joint HJB boundary compatibility marker.
6. Per-final-extent cross-a joint-compatibility frontier marker.
7. Deterministic repeat and applicable full repository regression suite.
8. Stop without stationary KFE / density / tail / `C,L,A,B`.

Binding stopping rule:

- if a common final extent reaches cross-a joint compatibility, next gate is a bounded b-resolution confirmation at the **smallest compatible extent**;
- if no common threshold is reached through b160, no further larger-grid continuation is allowed under the current route; next gate must adjudicate high-wealth asymptotics / mean reversion / finite-domain HJB closure scientifically.

## Exact Builder allowlist

Builder may create only:

1. `src/deep_learning_hank/two_asset/final_coupled_b_extent_diagnostic.py`
2. `configs/dlh_5j_final_coupled_b_extent_diagnostic.toml`
3. `tests/test_dlh_5j_final_coupled_b_extent_diagnostic.py`
4. `reports/dlh_5j_final_coupled_b_extent_diagnostic_2026_09_01/` with exactly eight files:
   - `DLH_5J_VARIANT_STATUS.csv`
   - `DLH_5J_BOUNDARY_DIAGNOSTICS.csv`
   - `DLH_5J_FINAL_EXTENT_TRENDS.csv`
   - `DLH_5J_CROSS_A_POLICY_STABILITY.csv`
   - `DLH_5J_JOINT_COMPATIBILITY_FRONTIER.csv`
   - `DLH_5J_REPRODUCIBILITY.json`
   - `DLH_5J_EXECUTION_REPORT.md`
   - `DLH_5J_FORBIDDEN_OPERATION_CHECK.md`

No existing tracked file may be modified by Builder.

## Scientific ceiling during Issue #36

Do not modify accepted HJB/KFE/regional source or Issues #23–#35 evidence; do not change physical a-domain, `a_max`, taper, economics/prices/parameters/tolerances/initialization; do not use an a resolution outside a77/a153 or change `db=7/19`; do not rerun b100; do not use b extent beyond b160; no warm-start, adaptive/root-seeking grid or clipping; no stationary KFE/density/tail/aggregates; no D1-D3, two-region/multi-province GE, `31_PROVINCE_HOUSEHOLD_UPPER_DOMAIN_AUDIT`, neural training, nominal HANK, calibration, policy/welfare or Results.

No PR / merge / close / successor / self-accept from Builder.

## DSH startup sequence

1. `Set-Location D:\deep-learning-hank`;
2. verify repository / remote / worktree / staging;
3. `git fetch origin` and record fresh `origin/main`;
4. read all CURRENT project rules;
5. read `tasks/TASK_INDEX_CURRENT.md` and this Startup Snapshot;
6. read current Roadmap and historical Handoff;
7. read Issue #36 full body and latest comments, including activation;
8. read accepted Issue #35 review/evidence and controlling Issue #27–#34 authority; read accepted MATLAB-faithful HJB source read-only;
9. verify Issue / Task Index / Startup identity exactly;
10. create exact dedicated branch from fresh `origin/main`;
11. operate only inside the Issue #36 allowlist;
12. run focused and applicable full regression tests;
13. explicit-stage only allowlist paths, commit/push, and STOP for fresh ChatGPT review.

Chat text is not Builder authority.

## Governance tooling audit note

During an earlier reviewer-side governance synchronization, a temporary file named `NONEXISTENT` was accidentally created on `main` and immediately deleted; the delete restored the prior tree before the accepted DLH-5F merge. The no-op audit commits are `84cc3894829881d81e6232bb510e4612700a9bc0` and `cb4bd714771593b435978f9ebfc9fd7eaf0b68a0`.

Issues #30, #32 and #33 were accidental tooling issues and were immediately closed as `not_planned`; they carry no scientific or Builder authority.
