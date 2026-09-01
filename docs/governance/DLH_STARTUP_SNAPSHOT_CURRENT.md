# Deep Learning + HANK Startup Snapshot — CURRENT

Date: 2026-09-01

Repository: `zcx369658780/deep-learning-hank`

Local Owner-designated workspace: `D:\deep-learning-hank`

## Governance state

- live GitHub `main` = synchronized repository/code/governance authority;
- GitHub Issue = sole DSH Builder authority only after publication + Task Index / Startup synchronization + authoritative activation comment;
- DSH = bounded Builder/executor;
- ChatGPT = independent fresh-GitHub reviewer / scientific-route advisor / task issuer / governance operator;
- Owner = final scientific authority; routine bounded route decisions are delegated to ChatGPT unless Owner intervenes;
- Builder completion is not acceptance.

Priority:

`Scientific correctness > Experiment reproducibility > Research iteration speed > Git auditability > Documentation completeness`

## Current Builder state

Current published task:

**Issue #38 — DLH-5L: Adjudicate componentwise liquid outward drift versus total-wealth mean reversion and boundary geometry**

Task type:

`SCIENTIFIC_ANALYTICAL_DIAGNOSTIC__TOTAL_WEALTH_DRIFT_AND_DOMAIN_GEOMETRY`

Dedicated branch:

`dsh/issue-38-dlh-5l-total-wealth-domain-geometry-2026-09-01`

Builder authority becomes active only while Issue #38 remains OPEN, Task Index / Startup identity matches, and the authoritative activation comment is present.

Current master roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`

Historical scientific handoff:

`docs/governance/DLH_HANDOFF_2026_09_01_UPPER_DOMAIN_STATIONARY_TAIL_ROUTE.md`

## Latest accepted gate — Issue #37 / DLH-5K

Accepted candidate:

`aaead4a1368ec061ac1e380c3af33d93c0f31161`

Integrated to `main` by acceptance merge commit:

`d26b2b8c8d69d2afa2cb9806f120d03ebe973752`

Accepted reviewer verdict:

`DLH_5K_ISSUE_37_IMPLEMENTATION_ACCEPTED__MIXED_LOCALIZATION_CONFIRMED__TRANSFER_DERIVATIVE_CHANNEL_DOMINATES_CROSS_A_DIVERGENCE__INTERPRETATION_NARROWED__NEXT_GATE_REQUIRED`

Acceptance level:

`L3_COMMIT_VERIFIED__SCIENTIFIC_ANALYTICAL_DIAGNOSTIC_ACCEPTED`

Controlling accepted interpretation:

- DLH-5K reproduced J0–J5 exactly and preserved accepted source identity;
- 5/17 material top-boundary offenders are `BOUNDARY_ONLY_POSITIVE`, while 12/17 retain material positive `mu_b` in at least one of the inspected `n-2/n-3/n-5` layers;
- this establishes local full-policy liquid-drift persistence only; it does not establish an infinite-domain high-wealth theorem or global failure of mean reversion;
- at material offenders, `base_liquid_surplus<0` and `transfer_injection>0`; positive `mu_b` occurs when transfer injection dominates;
- a77/a153 divergence is primarily transfer/derivative-channel driven;
- the selected transfer-FOC candidate fails joint inwardness at inspected offender states, but the algebra admits much larger transfer-flow roots, so no claim of mathematical joint-corner infeasibility is accepted;
- transfer `d` is a continuous-time flow/rate and must not be interpreted as an asset-stock liquidation amount;
- upper-a candidate sign filtering alone is not a proof of `mu_a<=0`; final `mu_a` was checked and is inward at the inspected offenders;
- no source defect/redesign is accepted; larger-b continuation remains CLOSED;
- stationary KFE remains NOT AUTHORIZED.

## Controlling HJB/KFE rule

```text
HJB boundary policy <=> KFE boundary transition law
```

Issue #27 remains the stationary-KFE contract. No stationary validation begins until a scientifically accepted controlled process has coherent boundary treatment and the required robustness evidence.

## DLH-5L scientific rationale

The accepted source has one-for-one transfer terms across the two asset drifts:

```text
mu_a = r_a_eff(a)*a + d
mu_b = r_b*b + labor_income - d - adjustment_cost(d,a)
       - (consumption - transfer_income)
```

Therefore the linear transfer term cancels from total asset drift:

```text
mu_W = mu_a + mu_b
     = r_a_eff(a)*a + r_b*b + labor_income
       - adjustment_cost(d,a) - (consumption - transfer_income)
```

DLH-5L asks whether the positive **liquid-coordinate** `mu_b` found in DLH-5K coexists with inward total-wealth drift on the exact accepted state set. This distinguishes portfolio reallocation / rectangular-domain geometry from genuine total-wealth outwardness. It does not redesign the domain.

## DLH-5L exact numerical scope

Rerun exactly the accepted J0–J5 grids only:

```text
J0_A77_B120
J1_A77_B140
J2_A77_B160
J3_A153_B120
J4_A153_B140
J5_A153_B160
```

Frozen economics and domain objects remain unchanged:

```text
wbar=1.0
r_a=0.03
a in [0,10]
a_max=10
accepted taper unchanged
a resolution in {a77,a153}
db=7/19
b extent in {b120,b140,b160}
```

No new grid, extent, resolution, b100 rerun, b-resolution change or warm start.

The inspected state set is frozen as the union of exact row coordinates from accepted:

- `reports/dlh_5k_high_wealth_corner_closure_diagnostic_2026_09_01/DLH_5K_BOUNDARY_INTERIOR_LOCALIZATION.csv`
- `reports/dlh_5k_high_wealth_corner_closure_diagnostic_2026_09_01/DLH_5K_CROSS_A_MECHANISM.csv`

Deduplicate exact `(variant,b_index,a_index,z_index)` only. No post-hoc states.

## DLH-5L required diagnostic order

1. reproduce accepted J0–J5 HJB/boundary evidence and accepted source identity;
2. derive and verify `mu_W=mu_a+mu_b` and the transfer-cancelled budget at every inherited state;
3. classify every state into the pre-registered component-liquid / total-wealth sign categories using only the accepted threshold;
4. explicitly report total-wealth sign for every DLH-5K `INTERIOR_POSITIVE_PERSISTS` state;
5. verify linear transfer cancellation separately from adjustment cost;
6. analytically compare rectangular component constraints with local `W=a+b` normal drift, without changing the production domain;
7. compare exact aligned a77/a153 total-wealth behavior;
8. deterministic repeat + applicable full regression suite;
9. STOP without source/domain redesign or stationary KFE.

## Exact Builder allowlist

Builder may create only:

1. `src/deep_learning_hank/two_asset/total_wealth_domain_geometry_diagnostic.py`
2. `configs/dlh_5l_total_wealth_domain_geometry_diagnostic.toml`
3. `tests/test_dlh_5l_total_wealth_domain_geometry_diagnostic.py`
4. `reports/dlh_5l_total_wealth_domain_geometry_diagnostic_2026_09_01/` with exactly:
   - `DLH_5L_SOURCE_ACCOUNTING_AUDIT.md`
   - `DLH_5L_STATE_DRIFT_DECOMPOSITION.csv`
   - `DLH_5L_COORDINATE_TOTAL_CLASSIFICATION.csv`
   - `DLH_5L_BOUNDARY_GEOMETRY.csv`
   - `DLH_5L_CROSS_A_TOTAL_WEALTH.csv`
   - `DLH_5L_REPRODUCIBILITY.json`
   - `DLH_5L_EXECUTION_REPORT.md`
   - `DLH_5L_FORBIDDEN_OPERATION_CHECK.md`

No existing tracked file may be modified by Builder.

## Scientific ceiling during Issue #38

Do not add any grid/extent/resolution or use `b>b160`; do not modify accepted HJB/KFE/regional source, taper, FOC, adjustment cost, boundary law, economics/prices/parameters/tolerances/initialization; no clipping; no stationary KFE/nullspace/pin/density/tail/aggregates; no D1-D3, regional GE, multi-province audit, network training, nominal HANK, calibration, policy/welfare or Results.

No PR / merge / close / successor / self-accept from Builder.

## DSH startup sequence

1. `Set-Location D:\deep-learning-hank`;
2. verify repository / remote / worktree / staging;
3. `git fetch origin` and record fresh `origin/main`;
4. read all CURRENT project rules;
5. read Task Index, this Startup Snapshot, current Roadmap and historical Handoff;
6. read Issue #38 full body and latest comments, including activation;
7. read accepted Issue #37 review/evidence and controlling Issue #27–#36 authority;
8. read accepted household source and DLH-5K diagnostic read-only;
9. verify Issue / Task Index / Startup identity exactly;
10. create exact dedicated branch from fresh `origin/main`;
11. operate only inside the Issue #38 allowlist;
12. run focused and applicable full regression tests;
13. explicit-stage only allowlist paths, commit/push, and STOP for fresh ChatGPT review.

Chat text is not Builder authority.

## Governance tooling audit note

Earlier reviewer-side no-op audit commits `84cc3894829881d81e6232bb510e4612700a9bc0` and `cb4bd714771593b435978f9ebfc9fd7eaf0b68a0` remain historical only. Issues #30, #32 and #33 are accidental tooling issues closed `not_planned` and carry no scientific or Builder authority.
