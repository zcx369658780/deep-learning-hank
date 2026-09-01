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

**Issue #37 — DLH-5K: Adjudicate high-wealth liquid drift versus joint upper-corner HJB closure**

Task type:

`SCIENTIFIC_ANALYTICAL_DIAGNOSTIC__HIGH_WEALTH_LIQUID_DRIFT_AND_UPPER_CORNER_CLOSURE`

Dedicated branch:

`dsh/issue-37-dlh-5k-high-wealth-corner-closure-2026-09-01`

Builder authority becomes active only while Issue #37 remains OPEN, Task Index / Startup identity matches, and the authoritative activation comment is present.

Current master roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`

Historical scientific handoff:

`docs/governance/DLH_HANDOFF_2026_09_01_UPPER_DOMAIN_STATIONARY_TAIL_ROUTE.md`

## Latest accepted gate — Issue #36 / DLH-5J

Accepted candidate:

`3899e30c7624db08d3588b08b390f8b5bbc5f7c1`

Integrated to `main` by acceptance merge commit:

`09fcdd66f7d33ccf11a6cc9ec52afed73451568e`

Accepted reviewer verdict:

`DLH_5J_ISSUE_36_IMPLEMENTATION_ACCEPTED__A77_B160_COMPATIBILITY_CONFIRMED__A153_B160_REMAINS_OUTWARD__CROSS_A_ROBUSTNESS_FAILED__GRID_CONTINUATION_CLOSED__ASYMPTOTIC_CLOSURE_ADJUDICATION_REQUIRED`

Acceptance level:

`L3_COMMIT_VERIFIED__SCIENTIFIC_DIAGNOSTIC_ACCEPTED`

Key accepted interpretation:

- upper-a, lower-a and lower-b requested outward policy is exact zero on all J0–J5 variants;
- upper-b attenuates monotonically from accepted b100 anchors through b160;
- a77/b160 reaches exact joint upper-boundary compatibility;
- a153/b160 remains materially outward: raw `1.491625647e-02`, requested `4.048698186e-02`, 2 states, concentrated at the top-liquid/top-illiquid/high-z corner;
- no cross-a jointly compatible extent exists through the hard b160 ceiling;
- cross-a value/consumption/labor differences are about `1e-3` or below, but transfer/`mu_a`/`mu_b` remain diagnostically different by about 2.20% / 2.43% / 1.91%;
- pure b-domain continuation is scientifically closed; no b180/b200/root-seeking expansion;
- stationary KFE remains NOT AUTHORIZED.

## Controlling HJB/KFE rule

```text
HJB boundary policy <=> KFE boundary transition law
```

Issue #27 remains the stationary-KFE contract. No stationary validation begins until a scientifically accepted controlled process has coherent upper-boundary treatment and the required numerical robustness evidence.

## Controlling accepted-source ordering for DLH-5K

The accepted MATLAB-faithful source remains immutable:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Relevant accepted source facts to audit, not assumptions of defect:

1. the upper-b derivative closure is constructed from resource-based marginal utility before the endogenous transfer decision is finalized;
2. the liquid branch is selected from resource/consumption conditions;
3. transfer candidates are then built from `V_a/V_b`;
4. upper-a restricts transfer toward the inward-a / negative-transfer side;
5. upper-b disables forward-transfer selection and forces the backward-transfer branch;
6. final `mu_a` and `mu_b` are evaluated only after transfer selection;
7. the local wrapper passes `consumption - transfer_income` into the drift helper.

Therefore the exact implemented decomposition to test is:

```text
mu_b = base_liquid_surplus + transfer_injection
base_liquid_surplus = r_b*b + labor_income - (consumption - transfer_income)
transfer_injection = -transfer - adjustment_cost
```

This ordering is a diagnostic hypothesis for the residual joint-corner behavior; it is not an accepted source defect or redesign authority.

## DLH-5K exact scientific scope

DLH-5K asks whether the remaining a153 upper-b drift is:

- boundary/joint-corner transfer-closure dominated;
- genuine high-wealth interior outward drift / missing economic mean reversion;
- or a mixed mechanism.

Rerun exactly the already accepted J0–J5 grids only, with all economics, bounds, resolutions and spacings unchanged. No new grids or extents.

Required order:

1. reproduce accepted J0–J5 HJB/boundary evidence;
2. audit source ordering and exact drift algebra;
3. decompose every material upper-b offender and aligned J2 states;
4. inspect the same `(a,z)` at b layers `n-1`, `n-2`, `n-3`, `n-5`;
5. evaluate joint-corner feasibility inequalities under the accepted adjustment-cost law;
6. compare a77/a153 high-wealth mechanisms on exact aligned nodes;
7. deterministic repeat and applicable full regression suite;
8. stop without source modification or stationary KFE.

## Exact Builder allowlist

Builder may create only:

1. `src/deep_learning_hank/two_asset/high_wealth_corner_closure_diagnostic.py`
2. `configs/dlh_5k_high_wealth_corner_closure_diagnostic.toml`
3. `tests/test_dlh_5k_high_wealth_corner_closure_diagnostic.py`
4. `reports/dlh_5k_high_wealth_corner_closure_diagnostic_2026_09_01/` with exactly:
   - `DLH_5K_SOURCE_LAW_AUDIT.md`
   - `DLH_5K_OFFENDER_DECOMPOSITION.csv`
   - `DLH_5K_BOUNDARY_INTERIOR_LOCALIZATION.csv`
   - `DLH_5K_JOINT_CORNER_FEASIBILITY.csv`
   - `DLH_5K_CROSS_A_MECHANISM.csv`
   - `DLH_5K_REPRODUCIBILITY.json`
   - `DLH_5K_EXECUTION_REPORT.md`
   - `DLH_5K_FORBIDDEN_OPERATION_CHECK.md`

No existing tracked file may be modified by Builder.

## Scientific ceiling during Issue #37

Do not add any grid/extent/resolution, including anything beyond b160; do not modify accepted HJB/KFE/regional source, taper, transfer FOC, adjustment cost, boundary law, economics/prices/parameters/tolerances/initialization; no clipping; no stationary KFE/density/tail/aggregates; no D1-D3, regional GE, multi-province audit, neural training, nominal HANK, calibration, policy/welfare or Results.

No PR / merge / close / successor / self-accept from Builder.

## DSH startup sequence

1. `Set-Location D:\deep-learning-hank`;
2. verify repository / remote / worktree / staging;
3. `git fetch origin` and record fresh `origin/main`;
4. read all CURRENT project rules;
5. read `tasks/TASK_INDEX_CURRENT.md` and this Startup Snapshot;
6. read current Roadmap and historical Handoff;
7. read Issue #37 full body and latest comments, including activation;
8. read accepted Issue #36 review/evidence and controlling Issue #27–#35 authority; read accepted MATLAB-faithful HJB source read-only;
9. verify Issue / Task Index / Startup identity exactly;
10. create exact dedicated branch from fresh `origin/main`;
11. operate only inside the Issue #37 allowlist;
12. run focused and applicable full regression tests;
13. explicit-stage only allowlist paths, commit/push, and STOP for fresh ChatGPT review.

Chat text is not Builder authority.

## Governance tooling audit note

During an earlier reviewer-side governance synchronization, a temporary file named `NONEXISTENT` was accidentally created on `main` and immediately deleted; the delete restored the prior tree. The no-op audit commits are `84cc3894829881d81e6232bb510e4612700a9bc0` and `cb4bd714771593b435978f9ebfc9fd7eaf0b68a0`.

Issues #30, #32 and #33 were accidental tooling issues and were immediately closed as `not_planned`; they carry no scientific or Builder authority.
