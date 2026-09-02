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

**Issue #44 — DLH-5R: Execute HJB-only provisional-S3 liquid-tail numerical falsification**

Task type:

`SCIENTIFIC_NUMERICAL_FALSIFICATION__PROVISIONAL_S3_HJB_TAIL_DIAGNOSTIC`

Dedicated branch:

`dsh/issue-44-dlh-5r-hjb-tail-falsification-2026-09-02`

Builder authority becomes active only while Issue #44 remains OPEN, Task Index / Startup identity matches, and the authoritative activation comment is present.

Current master roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`

## Latest accepted gate — Issue #43 / DLH-5Q

Accepted candidate:

`dd39385b6cf4fcf8fed382d69683ab907747cfe3`

Reviewer acceptance comment:

`5507534903`

Acceptance integration commit:

`570d858aea3029e1a30c286b5c683a8efdb836bd`

Accepted verdict:

`DLH_5Q_REV3_ACCEPTED__OUTCOME_B_CONFIRMED__PROVISIONAL_S3_SURVIVES_ANALYZED_FAMILIES__THEOREM_NOT_CLOSED__FALSIFICATION_PROTOCOL_READY`

Accepted terminal:

`DLH_5Q_PROVISIONAL_S3_THEOREM_NOT_CLOSED__MISSING_EXISTENCE_COMPARISON_OR_ASYMPTOTIC_REALIZATION_IDENTIFIED__FALSIFICATION_PROTOCOL_READY`

## Owner decision after DLH-5Q

Owner selected Q-B2:

`APPROVE_Q_B2_HJB_ONLY_NUMERICAL_FALSIFICATION__NO_KFE`

Owner-decision comment on Issue #43:

`5507666206`

This authorizes a bounded HJB-only numerical falsification experiment against provisional S3. It does not authorize S3 promotion, R/W selection, endpoint law adoption, or stationary KFE.

## Controlling source and grids

Accepted household source remains immutable/read-only:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb337f1b02b3fe33c51e`

Read-only mature-grid authority:

`configs/dlh_5j_final_coupled_b_extent_diagnostic.toml`

Exactly six fresh HJB-only variants are authorized:

```text
J0_A77_B120
J1_A77_B140
J2_A77_B160
J3_A153_B120
J4_A153_B140
J5_A153_B160
```

Frozen numerical bounds:

```text
a in [0,10]
a_max = 10
b_lo = -2
db = 7/19
b120 <= 41.84210526315789
b140 <= 49.21052631578947
b160 <= 56.578947368421055
```

No new b extent, b resolution, b_lo, a_hi, or a_max is authorized. b160 remains the hard ceiling.

## Provisional S3 predictions under test

The experiment tests numerical signatures of the provisional working class:

```text
R = V_a/V_b = O(1)
K* = 4/(rho+r_b)^2 = 3265.3061224489797
b^2 V_b -> K*
c/b -> 0.0175
mu_W/b -> -0.0025
chi/b -> 0
```

These are conditional predictions, not theorem facts.

The accepted out-of-S3 exclusion-cost benchmark remains:

```text
R ~ Theta(sqrt(b))
chi/b -> positive constant
c/b can approach a coefficient different from 0.0175
```

A stable benchmark-like signature may falsify promotion of S3 as the realized model. It does not falsify the mathematical definition of S3 itself.

## Raw-gradient provenance rule

Primary numerical observable is:

`R_hat = V_a_raw / V_b_raw`

The raw gradients must be those used in, or algebraically consistent with, the accepted transfer FOC. Do not silently substitute consumption/labor derivative floors into `R_hat`.

If raw transfer-FOC-consistent gradient provenance cannot be established without accepted-source mutation, Issue #44 must stop blocked.

Derivative-floor activation must be recorded separately as a numerical-semantic limitation.

## Primary evidence windows

Aligned physical-b windows are frozen in Issue #44:

```text
W1_COMMON      = [20,35]
W2_COMMON_HIGH = (35,40]
W3_EXTENDED    = [42,48]   # b140/b160
W4_B160_ONLY   = [50,55]   # descriptive only
```

Primary interior-a evidence excludes `a=0` and the top two a77 coarse layers; a77/a153 comparisons use aligned nodes. `a=0` is reported separately; `a=10` is not primary theorem evidence.

## Scientific interpretation ceiling

- numerical support does not prove existence/comparison or close the S3 theorem;
- numerical falsification must be stable across mature b extents and a resolutions and not reducible to boundary/floor/non-convergence artifacts;
- no production-domain choice follows from Issue #44;
- R/W/W1/W2 remain unfrozen; no `W_max`;
- no endpoint-KKT or analytic endpoint law is authorized.

## Controlling HJB/KFE rule

```text
HJB boundary policy <=> KFE boundary transition law
```

Issue #27 remains binding. Stationary KFE remains **NOT AUTHORIZED**.

## Exact Builder allowlist

Builder may create only the 10 files frozen in Issue #44:

- one new DLH-5R config;
- one new DLH-5R diagnostic runner;
- eight exact report/CSV outputs under `reports/dlh_5r_provisional_s3_hjb_tail_falsification_2026_09_02/`.

No existing tracked file may be modified by Builder. Large raw full-grid arrays must not be committed.

## Scientific ceiling during Issue #44

- no accepted-source/economics mutation;
- no new grid extent beyond existing b160 and no new b_lo/a_max;
- no R/W/W1/W2/`W_max`;
- no endpoint-KKT;
- no stationary KFE/nullspace/pin/density/aggregates;
- no regional GE / multi-province audit;
- no network training / nominal HANK;
- no calibration / policy / welfare / Results.

## DSH startup sequence

1. `Set-Location D:\deep-learning-hank`;
2. verify repository / remote / worktree / staging;
3. `git fetch origin` and record fresh `origin/main`;
4. read all CURRENT rules;
5. read Task Index, this Startup Snapshot and current Roadmap;
6. read Issue #44 full body and latest comments, including authoritative activation;
7. read Issue #43 acceptance, reviewer and Owner-decision comments read-only;
8. read accepted DLH-5Q numerical protocol, DLH-5J grid config and household source read-only;
9. verify Issue / Task Index / Startup identity exactly;
10. create the exact dedicated branch from fresh `origin/main`;
11. create only Issue #44 allowlist files;
12. establish raw-gradient provenance before scientific inference;
13. run exactly the six authorized HJB-only mature variants;
14. do not run KFE/stationary/aggregates;
15. explicit-stage only allowlist paths, commit/push, and STOP for fresh ChatGPT review.

Chat text is not Builder authority.
