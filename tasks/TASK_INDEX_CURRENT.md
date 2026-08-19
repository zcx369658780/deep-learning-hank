# Deep Learning + HANK Task Index

Status: `ACTIVE_GITHUB_ISSUE_7_DLH_2C`

## Accepted predecessors

### Issue #1 — local/GitHub bootstrap
Status: `ACCEPTED_AND_CLOSED`
Accepted commit: `bcded9b9137f3c10f71a7a6ecb929f78b40bdc11`

### Issue #2 — DLH-0 / NSR-HANK scientific constitution
Status: `DLH_0_R1_NSR_HANK_SCIENTIFIC_CONSTITUTION_ACCEPTED_AND_CLOSED`
Accepted commit: `73e1ae5db9d7e362781a77fa2a204c80238fad3e`

### Issue #3 — DLH-1A literature / labor-flow data feasibility
Status: `DLH_1A_R1_EVIDENCE_AND_DATA_FEASIBILITY_ACCEPTED_AND_CLOSED`
Accepted commit: `e9aa7dc8a3f5a198b1655c917659f519239eb67b`

### Issue #4 — DLH-1B Python kernel read-only audit
Status: `DLH_1B_R2_PYTHON_KERNEL_READONLY_AUDIT_ACCEPTED_AND_CLOSED`
Accepted commit: `8dce318af5ca704a747e67932ec3caa35f9168ad`

### Issue #5 — DLH-2A fixed-price HJB/KFE validation
Status: `DLH_2A_R1_TIER0_KERNEL_FIXED_PRICE_VALIDATION_ACCEPTED_AND_CLOSED`
Accepted commit: `76b5882a63d8ade18d50098373b7c735eb2c4ca4`
Evidence level: `D2_MACHINE_DIAGNOSTIC_ONLY`.

### Issue #6 — DLH-2B single-region Tier-0 steady-state GE
Status: `DLH_2B_R1_TIER0_SINGLE_REGION_STEADY_STATE_GE_ACCEPTED_AND_CLOSED`
Accepted commit: `c562ce3a2743ac779123918e9aab5f37044b564a`
Evidence level: `D2_MACHINE_DIAGNOSTIC_ONLY`.

Accepted numerical facts under `VALIDATION_FIXTURE_NOT_CALIBRATION`:
- `K*=27.367823476711713` with capital residual `1.0466294497746276e-11`;
- equilibrium HJB/KFE, effective-labor, fiscal, goods, household-budget and mean-drift gates pass;
- R1 root evidence: `root_trace_evaluations=11`, `post_root_validation_evaluations=1`, `total_capital_evaluations=12`, `root_trace_finite_ok=True`;
- R1 complete repository suite = `32 passed / 0 failed`, including accepted DLH-2A regression `15/15`;
- deterministic repeat differences all `0.0`;
- this remains a small one-region real HA/Aiyagari D2 benchmark, not calibration or genuine HANK.

Authoritative roadmap:
`docs/roadmaps/DLH_MASTER_ROADMAP_INITIAL_2026_08_19.md`

## Sole active Builder authority

GitHub Issue #7:

`DLH-2C: Tier-0 numerical robustness, grid-boundary and invariance validation`

Issue URL:
`https://github.com/zcx369658780/deep-learning-hank/issues/7`

Builder: DSH

Expected dedicated branch:
`dsh/issue-7-dlh-2c-tier0-robustness-2026-08-19`

## Current gate purpose

DLH-2C is the final planned Tier-0 robustness gate before any genuine-HANK nominal implementation.

It keeps all accepted DLH-2B economics and solver code frozen and tests only numerical/representation robustness through:

- accepted baseline `B40_50`;
- fixed-bound grid refinements `G80_50` and `G160_50`;
- matched-spacing upper-bound expansion `W159_100`;
- pure state-label permutation `P40_50`;
- 21-point bounded capital-residual scan on `[0.5,45.0]`;
- per-variant full steady-state gates and deterministic reproducibility.

Mandatory robustness criteria are defined only by Issue #7 and may not be relaxed by Builder.

## Scope boundary

DLH-2C remains `VALIDATION_FIXTURE_NOT_CALIBRATION` and real single-region Tier-0 only.

It does **not** authorize:
- modification of accepted DLH-2A/DLH-2B solver/economics modules or tests;
- regional / `W^L` / `W^K` / old `W` code;
- SOE / RegionalAccounts;
- nominal/Fisher/NKPC/Taylor-rule mechanisms;
- shocks/transition;
- neural/RL;
- empirical data/calibration/regression;
- Matlab/legacy Matlab or old-source-repo access;
- Results/policy/novelty claims;
- PR/merge/Issue-close/successor/self-accept by Builder.

## Queued next gate — NOT ACTIVE

`DLH-3 — minimal genuine single-region HANK nominal/New-Keynesian layer` may only be issued after independent disposition of Issue #7.
