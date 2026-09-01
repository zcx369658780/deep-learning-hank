# Deep Learning + HANK Startup Snapshot — CURRENT

Date: 2026-09-01

Repository: `zcx369658780/deep-learning-hank`

Local Owner-designated workspace: `D:\deep-learning-hank`

## Governance state

- live GitHub `main` = synchronized repository/code/governance authority;
- GitHub Issue = sole DSH Builder authority only after publication + Task Index / Startup synchronization + authoritative activation comment;
- DSH = bounded Builder/executor;
- ChatGPT = independent fresh-GitHub reviewer / scientific-route advisor / task issuer / governance operator;
- Owner = final scientific-direction authority; routine route decisions are delegated to ChatGPT unless Owner intervenes;
- Builder completion is not acceptance.

Priority:

`Scientific correctness > Experiment reproducibility > Research iteration speed > Git auditability > Documentation completeness`

## Current Builder state

Current published task:

**Issue #31 — DLH-5G: Isolate liquid upper-domain asymptotics under fixed illiquid domain and taper**

Task type:

`SCIENTIFIC_DIAGNOSTIC__LIQUID_UPPER_DOMAIN_ASYMPTOTIC_AND_RESOLUTION`

Dedicated branch:

`dsh/issue-31-dlh-5g-liquid-upper-domain-asymptotic-2026-09-01`

Builder authority is active only while Issue #31 remains OPEN, Task Index / Startup identity matches, and the authoritative activation comment is present.

Current master roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`

Historical scientific handoff:

`docs/governance/DLH_HANDOFF_2026_09_01_UPPER_DOMAIN_STATIONARY_TAIL_ROUTE.md`

## Latest accepted gate — Issue #29 / DLH-5F

Accepted candidate:

`7f4e489154115c9c91cf8c3fccbb3a1d114fbc3f`

Integrated to `main` by acceptance merge commit:

`8eaac27472e3f902d0ff3e8044027f95913155ba`

Accepted reviewer verdict:

`DLH_5F_ISSUE_29_IMPLEMENTATION_ACCEPTED__OUTCOME_B_CONFIRMED__OUTCOME_D_SUPPORTED_WITH_INTERPRETATION_CORRECTION__STATIONARY_TAIL_NOT_REACHED`

Accepted reviewer annotation:

`B_EXTENT_EVIDENCE_SHOWS_STRONG_ATTENUATION_NOT_GROWTH__A_EXTENT_CONFOUNDED_BY_AMAX_NORMALIZED_RETURN_TAPER__RESOLUTION_NOT_YET_STABLE`

Key accepted interpretation:

- clean b-only `V0_BASE -> V2_B_WIDE`, with a20 `[0,10]`, `a_max=10`, taper and `db` fixed, reduces upper-b requested rate from about `0.353747704` to about `0.010203356`;
- shared-interior policy on that comparison is highly stable;
- changing `a_max` changes the accepted MATLAB-faithful effective illiquid return `r_a*(1-0.1*(a/a_max)^9)`, so a-extent comparisons from DLH-5F are confounded;
- V5 keeps `a_max=10` and removes upper-a requested motion, showing strong resolution/local-discretization sensitivity in the illiquid dimension;
- no DLH-5F variant reached full HJB/KFE same-process stationary validation, so stationary-tail existence/non-existence and new `C,L,A,B` remain NOT REACHED.

## Controlling HJB/KFE rule

```text
HJB boundary policy <=> KFE boundary transition law
```

A mechanically conservative KFE cannot be treated as the stationary process of an HJB that requests a different material boundary policy.

Issue #27 stationary-KFE contract remains controlling for any later stationary validation, but DLH-5G does not execute stationary KFE.

## DLH-5G exact scientific scope

DLH-5G isolates the liquid upper boundary while freezing the entire illiquid side and all economics:

```text
wbar = 1.0
r_a  = 0.03
a: 20 points on [0,10]
a_max = 10
da = 10/19
accepted illiquid-return taper unchanged
```

Primary question:

> With fixed illiquid domain/taper and fixed economics, does raw upper-b outward drift `max(mu_b,0)` attenuate toward zero as `b_max` is extended, and is the conclusion robust to independent b-resolution refinement?

Raw `mu_b` is the primary cross-resolution asymptotic quantity. Requested generator rate `max(mu_b,0)/db` remains the boundary-compatibility quantity.

DLH-5G is policy-only. It does not authorize stationary KFE, nullspace/pin, density, tail mass, stationary flux, `C,L,A,B`, HJB redesign or a-taper redesign.

## Exact six pre-frozen variants

All six use identical a20 `[0,10]`, `a_max=10`, `da=10/19`, taper and non-grid economics.

1. `G0_BASE`: b20 `[-2,5]`, `db=7/19`.
2. `G1_B_WIDE_1`: b40 `[-2,235/19]`, same `db`.
3. `G2_B_WIDE_2`: b60 `[-2,375/19]`, same `db`.
4. `G3_B_WIDE_3`: b80 `[-2,515/19]`, same `db`.
5. `G4_BASE_B_FINE`: b39 `[-2,5]`, half `db`.
6. `G5_WIDE1_B_FINE`: b79 `[-2,235/19]`, half `db`.

No additional/adaptive grid is authorized.

## DLH-5G required diagnostic order

1. Fresh accepted HJB on all six variants; no warm start.
2. Upper/lower b raw-drift diagnostics and requested-rate diagnostics with complete offending-state evidence.
3. Upper/lower a requested-rate regression diagnostics only, with a-grid/taper frozen.
4. Same-spacing extent trend `G0 -> G1 -> G2 -> G3` including attenuation ratios.
5. Exact aligned resolution comparisons `G0 vs G4` and `G1 vs G5` for value, consumption, labor, transfer, `mu_a`, `mu_b`, and policy labels.
6. Deterministic repeat and applicable full repository regression suite.
7. Stop without stationary/KFE/aggregate execution.

## Exact Builder allowlist

Builder may create only:

1. `src/deep_learning_hank/two_asset/liquid_upper_domain_asymptotic_diagnostic.py`
2. `configs/dlh_5g_liquid_upper_domain_asymptotic_diagnostic.toml`
3. `tests/test_dlh_5g_liquid_upper_domain_asymptotic_diagnostic.py`
4. `reports/dlh_5g_liquid_upper_domain_asymptotic_diagnostic_2026_09_01/` with exactly eight files:
   - `DLH_5G_VARIANT_STATUS.csv`
   - `DLH_5G_LIQUID_BOUNDARY_DIAGNOSTICS.csv`
   - `DLH_5G_ILLIQUID_REGRESSION_DIAGNOSTICS.csv`
   - `DLH_5G_EXTENT_TREND.csv`
   - `DLH_5G_RESOLUTION_STABILITY.csv`
   - `DLH_5G_REPRODUCIBILITY.json`
   - `DLH_5G_EXECUTION_REPORT.md`
   - `DLH_5G_FORBIDDEN_OPERATION_CHECK.md`

No existing tracked file may be modified by Builder.

## Scientific ceiling during Issue #31

Do not modify accepted HJB/KFE/regional source or Issues #23–#29 evidence; do not change `a_max`, a-grid, taper, economics/prices/parameters/tolerances/initialization; no warm-start, adaptive/seventh grid or clipping; no stationary KFE/density/tail/aggregates; no D1-D3, two-region/multi-province GE, `31_PROVINCE_HOUSEHOLD_UPPER_DOMAIN_AUDIT`, neural training, nominal HANK, calibration, policy/welfare or Results.

No PR / merge / close / successor / self-accept from Builder.

## DSH startup sequence

1. `Set-Location D:\deep-learning-hank`;
2. verify repository / remote / worktree / staging;
3. `git fetch origin` and record fresh `origin/main`;
4. read all CURRENT project rules;
5. read `tasks/TASK_INDEX_CURRENT.md` and this Startup Snapshot;
6. read current Roadmap and historical Handoff;
7. read Issue #31 full body and latest comments, including activation;
8. read accepted Issue #29 review/outputs, Issue #27 contract, Issue #28 evidence, and accepted MATLAB-faithful HJB source read-only;
9. verify Issue / Task Index / Startup identity exactly;
10. create the exact dedicated branch from fresh `origin/main`;
11. operate only inside the Issue #31 allowlist;
12. run focused and applicable full regression tests;
13. explicit-stage only allowlist paths, commit/push, and STOP for fresh ChatGPT review.

Chat text is not Builder authority.

## Governance tooling audit note

During reviewer-side governance synchronization, a temporary file named `NONEXISTENT` was accidentally created on `main` and immediately deleted; the delete restored the prior tree before the accepted DLH-5F merge. The no-op audit commits are `84cc3894829881d81e6232bb510e4612700a9bc0` and `cb4bd714771593b435978f9ebfc9fd7eaf0b68a0`.

Issues #30, #32 and #33 were accidental tooling issues and were immediately closed as `not_planned`; they carry no scientific or Builder authority. Issue #31 is the intended DLH-5G task.
