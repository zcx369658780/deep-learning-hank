# Deep Learning + HANK Task Index

Status: `ACTIVE_GITHUB_ISSUE_6_DLH_2B_R1`

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

Authoritative roadmap:
`docs/roadmaps/DLH_MASTER_ROADMAP_INITIAL_2026_08_19.md`

## Sole active Builder authority

GitHub Issue #6:

`DLH-2B: Single-region Tier-0 HA/Aiyagari steady-state general equilibrium`

Issue URL:
`https://github.com/zcx369658780/deep-learning-hank/issues/6`

Builder: DSH

Current substage:

`DLH-2B-R1 — evidence provenance / root-trace finiteness and evaluation-count correction`

Prior candidate:

`2b4316f699720f0d8ad278c98110e8c1128532c4`

Independent review disposition:

`DLH_2B_CORE_STEADY_STATE_GATE_PASS__EVIDENCE_AND_ROOT_TRACE_R1_REQUIRED`

The prior candidate's economic closure and numerical D2 gates are substantively PASS, but it is NOT accepted/merged until the bounded R1 correction is completed.

Expected R1 dedicated branch:

`dsh/issue-6-dlh-2b-r1-evidence-root-trace-correction-2026-08-19`

## Independently confirmed core PASS

- one-region Tier-0 closure is `K -> (w,r) -> transfer -> HJB -> KFE -> A(K) -> K-A(K)`;
- primary bracket `[0.5,45.0]` has finite opposite-sign endpoint residuals; no scan was used;
- `K*=27.367823476711713`, capital residual `1.0466294497746276e-11 <= 1e-7`;
- equilibrium HJB/KFE thresholds pass;
- effective-labor consistency error is `0.0`;
- goods residual `1.0047518372857667e-13`, household-budget residual `0.0`, mean drift `-2.2941717969793274e-16`;
- full final suite reported `30 passed / 0 failed`, including accepted DLH-2A regression `15/15`;
- deterministic repeat differences are all `0.0`;
- no regional/W/SOE/nominal/shock/transition/neural/data/Matlab/Results scope was consumed.

## R1 correction requirements

1. **Exact diagnostics command provenance**: committed evidence must contain the full exact diagnostics-capture script/command; preserve original-run vs R1-rerun history.
2. **Evaluation-count semantics**: distinguish `root_trace_evaluations = 11`, `post_root_validation_evaluations = 1`, and `total_capital_evaluations = 12` for the accepted fixture (or equivalent precise names). Do not call 11 the complete count of all capital evaluations.
3. **Root-trace finiteness machine gate**: explicitly verify every `(capital, R_K)` entry in the root trace is finite, include this in the root/all-gates logic, strengthen a test, and rerun the complete repository suite and diagnostics.

## Scope boundary

R1 is a bounded evidence/diagnostic correction only. Preserve all Issue #6 economics, fixture values and thresholds and all accepted DLH-2A frozen dependencies.

It does **not** authorize:
- regional / `W^L` / `W^K` / old `W` code;
- SOE or RegionalAccounts;
- nominal/NK mechanisms;
- shocks/transition;
- neural/RL;
- empirical data/calibration;
- Matlab/legacy Matlab access;
- Results/policy/novelty claims;
- PR/merge/Issue-close/successor/self-accept by Builder.

## Queued next gate — NOT ACTIVE

`DLH-2C — Tier-0 numerical robustness / grid-boundary / limiting-case validation` is the recommended next validation gate after corrected DLH-2B is independently accepted.

Genuine-HANK implementation remains later and separately authorized.
