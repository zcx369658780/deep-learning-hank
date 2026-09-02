# Deep Learning + HANK Startup Snapshot — CURRENT

Date: 2026-09-02

Repository: `zcx369658780/deep-learning-hank`

Local Owner-designated workspace: `D:\deep-learning-hank`

## Governance state

- live GitHub `main` = synchronized repository/code/governance authority;
- GitHub Issue = sole DSH Builder authority only after publication + Task Index / Startup synchronization + authoritative activation comment;
- DSH = bounded Builder/executor or bounded scientific analyst only under an active Issue;
- ChatGPT = independent fresh-GitHub reviewer / scientific-route advisor / task issuer / governance operator;
- Owner = final scientific authority;
- Builder completion is not acceptance.

Priority:

`Scientific correctness > Experiment reproducibility > Research iteration speed > Git auditability > Documentation completeness`

## Current Builder state

Current published task:

**Issue #45 — DLH-5S: Analyze provisional-S3 pre-asymptotic dynamics and p=2 realization**

Task type:

`SCIENTIFIC_THEORY_ANALYSIS__PROVISIONAL_S3_PREASYMPTOTIC_DYNAMICS_AND_P2_REALIZATION`

Dedicated branch:

`dsh/issue-45-dlh-5s-scaled-tail-p2-realization-2026-09-02`

Builder authority becomes active only while Issue #45 remains OPEN, Task Index / Startup identity matches, and the authoritative activation comment is present.

Current master roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`

## Latest accepted gate — Issue #44 / DLH-5R

Accepted candidate:

`6b79b7b1ff388174b5460a32de547a25ecb8a097`

Reviewer acceptance comment:

`5510368753`

Acceptance integration commit:

`96f0adb855233da06e96b71c6d8b6fe6aa540fc7`

Accepted verdict:

`DLH_5R_REV2_ACCEPTED__OUTCOME_C_CONFIRMED__S3_DERIVATIVE_CONTROL_NUMERICALLY_COMPATIBLE_ON_ACCESSIBLE_RANGE__P2_ASYMPTOTIC_REALIZATION_NOT_REACHED__FINITE_TRUNCATION_ASYMPTOTIC_REACH_REMAINS`

Accepted terminal:

`DLH_5R_HJB_TAIL_NUMERICAL_FALSIFICATION_INCONCLUSIVE__BOUNDARY_RESOLUTION_OR_SEMANTIC_SENSITIVITY_REMAINS`

## Owner decision after DLH-5R

Owner selected R-C1:

`APPROVE_R_C1_BOUNDED_ANALYTIC_ASYMPTOTIC_REALIZATION_CLOSURE__NO_NUMERICAL_DOMAIN_EXPANSION`

Owner-decision comment on Issue #44:

`5510675566`

This authorizes bounded analytic/theory work on asymptotic realization and explicitly does NOT reopen b160 or authorize any new numerical HJB/grid experiment.

## Controlling scientific starting point

Accepted household source remains immutable/read-only:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb337f1b02b3fe33c51e`

Provisional working class remains:

- S1 continuous unbounded-positive-b analytic base on fixed finite a-support;
- S2 `V_inf(a,z)=0` provisional tail-selection assumption;
- primary S3 `R=V_a/V_b=O(1)` uniformly on claimed compact interior-a support;
- P-TR `R=o(sqrt(b))` sensitivity only;
- critical `R~Theta(sqrt(b))` retained outside S3 as a benchmark.

Accepted DLH-5Q theory:

- p=2 is the unique self-consistent formal balance among the correctly analyzed power/explicit-slow families inside S3;
- broader exotic/non-power regimes remain open;
- existence/comparison, actual p=2 realization, derivative-remainder control, coefficient convergence and full-support endpoint authority remain unproved.

Accepted DLH-5R numerical evidence:

```text
                 W1       W2       W3       W4 descriptive
slope          -0.559   -0.681   -0.758   -0.832
b^2 V_b         315      485      610      736
c/b            0.0564   0.0454   0.0405   0.0369
|R|/sqrt(b)    0.212    0.182    0.166    0.154
chi/b          0.00079  0.00058  0.00049  0.00040
mu_W/b        -0.0100  -0.0083  -0.0074  -0.0067
```

Controlling interpretation:

1. accessible-range S3 derivative-control signature is numerically compatible;
2. no critical `R~sqrt(b)` / positive-`chi/b` signature is observed;
3. p=2 coefficient/scaling is not yet reached;
4. stable non-p2 asymptotic falsification is not established;
5. principal p2-facing observables continue moving toward their conditional targets;
6. the material numerical limitation is asymptotic reach at the pre-existing b160 hard ceiling.

## DLH-5S exact theory target

DLH-5S must derive and audit scaled-tail variables such as

```text
H=-bV
Q=b^2 V_b
s=log b
```

and exact identities including

```text
dH/ds = H-Q
c/b = Q^(-1/2)
p_eff = 2-dlog(Q)/dlog(b)
```

where regularity permits.

It must derive the exact scaled HJB decomposition, analyze the scalar z-symmetric reduced system, restore the two-state z-switching modes, and determine whether the p=2 candidate

```text
H*=Q*=K*=4/(rho+r_b)^2 = 3265.3061224489797
```

is attracting on an admissibly relevant branch. The key theorem question is whether S1+S2+S3 imply the required branch selection / scaled-tail tightness / remainder smallness, or whether a sharper non-circular assumption remains necessary.

Finite-window DLH-5R evidence is read-only motivation/evidence context only and cannot be promoted into theorem proof.

## Scientific ceiling during Issue #45

- no accepted-source/economics mutation;
- no HJB/grid/resolution execution and no J0-J5 rerun as new evidence;
- no b180/b200 or any reopening of b160;
- no b_lo/db/a_max/a-resolution change;
- no R/W/W1/W2/`W_max` selection;
- no endpoint-KKT or analytic endpoint law invention;
- no stationary KFE/nullspace/pin/density/tail mass/aggregates;
- no regional GE / multi-province audit;
- no network training / nominal HANK;
- no calibration / policy / welfare / Results.

Issue #27 remains binding:

```text
HJB boundary policy <=> KFE boundary transition law
```

Stationary KFE remains NOT AUTHORIZED.

## Exact Builder allowlist

Builder may create only the nine files frozen in Issue #45: one theory document and eight exact theory reports under `reports/dlh_5s_scaled_tail_dynamics_p2_realization_2026_09_02/`.

No existing tracked file may be modified by Builder.

## DSH startup sequence

1. `Set-Location D:\deep-learning-hank`;
2. verify repository / remote / worktree / staging;
3. `git fetch origin` and record fresh `origin/main`;
4. read all CURRENT rules;
5. read Task Index, this Startup Snapshot and current Roadmap;
6. read Issue #45 full body and latest comments, including authoritative activation;
7. read Issue #44 acceptance and Owner route-decision comments read-only;
8. read accepted DLH-5Q theory and DLH-5R evidence packages read-only;
9. verify Issue / Task Index / Startup identity exactly;
10. create the exact dedicated branch from fresh synchronized `origin/main`;
11. create only Issue #45 allowlist files;
12. perform analytic theory work only; no HJB/KFE/grid execution;
13. explicit-stage only allowlist paths, commit/push, and STOP for fresh ChatGPT review.

Chat text is not Builder authority.
