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

**Issue #34 — DLH-5H: Isolate illiquid upper-boundary resolution on the provisional liquid-safe domain**

Task type:

`SCIENTIFIC_DIAGNOSTIC__ILLIQUID_UPPER_BOUNDARY_RESOLUTION`

Dedicated branch:

`dsh/issue-34-dlh-5h-illiquid-resolution-2026-09-01`

Builder authority becomes active only while Issue #34 remains OPEN, Task Index / Startup identity matches, and the authoritative activation comment is present.

Current master roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`

Historical scientific handoff:

`docs/governance/DLH_HANDOFF_2026_09_01_UPPER_DOMAIN_STATIONARY_TAIL_ROUTE.md`

## Latest accepted gate — Issue #31 / DLH-5G

Accepted candidate:

`edbd6e9d4683118e08edb8041609c9af1579883a`

Integrated to `main` by acceptance merge commit:

`809d18a3459b5b8c4d8b142ea4f282a34c3af49f`

Accepted reviewer verdict:

`DLH_5G_ISSUE_31_IMPLEMENTATION_ACCEPTED__LIQUID_UPPER_DOMAIN_ADEQUACY_EVIDENCE_CONFIRMED__B_RESOLUTION_SENSITIVITY_RETAINED__ILLIQUID_BOUNDARY_REMAINS_BLOCKER`

Acceptance level:

`L3_COMMIT_VERIFIED__SCIENTIFIC_DIAGNOSTIC_ACCEPTED`

Key accepted interpretation:

- the same-spacing liquid sequence gives upper-b raw/requested maxima `0.1303281015/0.3537477040 -> 0.003759131181/0.01020335606 -> 0/0 -> 0/0`;
- the requested upper-b policy is exactly zero by `b_max=19.7368421053` and stays zero at the wider same-spacing extent;
- finer b-resolution reaches zero already at `b_max=12.3684210526`, so liquid-domain adequacy is supported but b-resolution sensitivity remains material;
- no final production grid is frozen;
- `b60 [-2,375/19]`, `db=7/19` is a **provisional liquid-safe diagnostic domain** for isolating the remaining illiquid boundary problem;
- on that state upper-a remains material: requested max about `0.3094730854`, 108 material states / share `0.90`;
- stationary KFE remains NOT AUTHORIZED.

## Controlling HJB/KFE rule

```text
HJB boundary policy <=> KFE boundary transition law
```

Issue #27 stationary-KFE contract remains controlling for any later stationary validation. No stationary re-entry is authorized until a candidate household grid satisfies coherent upper-boundary HJB policy in both asset dimensions.

## DLH-5H exact scientific scope

DLH-5H isolates illiquid-grid resolution without changing the accepted household controlled process.

Frozen economics:

```text
wbar = 1.0
r_a  = 0.03
```

Frozen physical illiquid domain and taper:

```text
a_lo = 0
a_hi = 10
a_max = 10
accepted taper = r_a*(1-0.1*(a/a_max)^9)
```

Core liquid-safe domain:

```text
b: 60 points on [-2,375/19]
b_max = 19.736842105263158
db = 7/19
```

Primary question:

> With physical a-domain, a_max, taper, economics and the provisional liquid-safe domain fixed, does upper-a raw outward drift attenuate to the HJB/KFE compatibility threshold as only a-grid resolution is refined?

DLH-5H is policy-only. It does not authorize stationary KFE, nullspace/pin, density, tail metrics, stationary flux or `C,L,A,B`.

## Exact six pre-frozen variants

1. `H0_A20_BASE`: b60 core domain; a20 `[0,10]`, `da=10/19`.
2. `H1_A39_FINE`: same b60; a39 `[0,10]`, half baseline `da`.
3. `H2_A77_FINER`: same b60; a77 `[0,10]`, quarter baseline `da`.
4. `H3_A153_FINEST`: same b60; a153 `[0,10]`, eighth baseline `da`.
5. `H4_B119_A39`: same physical b-domain, b119 half `db`; a39.
6. `H5_B119_A77`: same physical b-domain, b119 half `db`; a77.

No additional/adaptive grid is authorized.

## DLH-5H required diagnostic order

1. Fresh accepted HJB on all six variants; no warm start.
2. Upper/lower a raw-drift and requested-rate diagnostics with complete offending-state evidence.
3. Upper/lower b raw/requested regression diagnostics on every variant; fail closed if liquid boundary materially reactivates.
4. Primary a-resolution trend `H0 -> H1 -> H2 -> H3`, including attenuation ratios and first threshold-reaching variant if any.
5. Exact aligned policy comparisons `H0/H1`, `H1/H2`, `H2/H3`, `H1/H4`, `H2/H5`.
6. Per-variant joint upper-boundary HJB policy compatibility marker only; do not run stationary KFE.
7. Deterministic repeat and applicable full repository regression suite.

## Exact Builder allowlist

Builder may create only:

1. `src/deep_learning_hank/two_asset/illiquid_upper_boundary_resolution_diagnostic.py`
2. `configs/dlh_5h_illiquid_upper_boundary_resolution_diagnostic.toml`
3. `tests/test_dlh_5h_illiquid_upper_boundary_resolution_diagnostic.py`
4. `reports/dlh_5h_illiquid_upper_boundary_resolution_diagnostic_2026_09_01/` with exactly eight files:
   - `DLH_5H_VARIANT_STATUS.csv`
   - `DLH_5H_ILLIQUID_BOUNDARY_DIAGNOSTICS.csv`
   - `DLH_5H_LIQUID_REGRESSION_DIAGNOSTICS.csv`
   - `DLH_5H_RESOLUTION_TREND.csv`
   - `DLH_5H_POLICY_STABILITY.csv`
   - `DLH_5H_REPRODUCIBILITY.json`
   - `DLH_5H_EXECUTION_REPORT.md`
   - `DLH_5H_FORBIDDEN_OPERATION_CHECK.md`

No existing tracked file may be modified by Builder.

## Scientific ceiling during Issue #34

Do not modify accepted HJB/KFE/regional source or Issues #23–#31 evidence; do not change physical a-domain, `a_max=10`, taper, economics/prices/parameters/tolerances/initialization; no a-domain widening, warm-start, adaptive/seventh grid or clipping; no stationary KFE/density/tail/aggregates; no D1-D3, two-region/multi-province GE, `31_PROVINCE_HOUSEHOLD_UPPER_DOMAIN_AUDIT`, neural training, nominal HANK, calibration, policy/welfare or Results.

No PR / merge / close / successor / self-accept from Builder.

## DSH startup sequence

1. `Set-Location D:\deep-learning-hank`;
2. verify repository / remote / worktree / staging;
3. `git fetch origin` and record fresh `origin/main`;
4. read all CURRENT project rules;
5. read `tasks/TASK_INDEX_CURRENT.md` and this Startup Snapshot;
6. read current Roadmap and historical Handoff;
7. read Issue #34 full body and latest comments, including activation;
8. read accepted Issue #31 review/evidence, Issue #29 evidence, Issue #27 contract, Issue #28 evidence, and accepted MATLAB-faithful HJB source read-only;
9. verify Issue / Task Index / Startup identity exactly;
10. create the exact dedicated branch from fresh `origin/main`;
11. operate only inside the Issue #34 allowlist;
12. run focused and applicable full regression tests;
13. explicit-stage only allowlist paths, commit/push, and STOP for fresh ChatGPT review.

Chat text is not Builder authority.

## Governance tooling audit note

During an earlier reviewer-side governance synchronization, a temporary file named `NONEXISTENT` was accidentally created on `main` and immediately deleted; the delete restored the prior tree before the accepted DLH-5F merge. The no-op audit commits are `84cc3894829881d81e6232bb510e4612700a9bc0` and `cb4bd714771593b435978f9ebfc9fd7eaf0b68a0`.

Issues #30, #32 and #33 were accidental tooling issues and were immediately closed as `not_planned`; they carry no scientific or Builder authority.
