# Deep Learning + HANK Task Index

Status: `ACTIVE_GITHUB_ISSUE_6_DLH_2B`

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
Accepted source repo: `zcx369658780/dissertation-ch5-r5-python-model` @ `3039a145f43d419a08999c476cd0d97fd5f8341f`.

### Issue #5 — DLH-2A Tier-0 fixed-price HJB/KFE validation
Status: `DLH_2A_R1_TIER0_KERNEL_FIXED_PRICE_VALIDATION_ACCEPTED_AND_CLOSED`
Accepted commit: `76b5882a63d8ade18d50098373b7c735eb2c4ca4`
Evidence level: `D2_MACHINE_DIAGNOSTIC_ONLY`.

Accepted numerical conclusions:
- new clean package implements one-asset finite-z CRRA/inelastic-labor fixed-price household HJB + stationary KFE;
- HJB uses state-constraint/no-outward-drift boundaries and CTMC infinitesimal generator/intensity matrix;
- accepted fixture is explicitly `VALIDATION_FIXTURE_NOT_CALIBRATION`;
- R1 full suite: `15 passed / 0 failed / 0 skipped`;
- HJB true residual `8.335084289434747e-08 <= 1e-7`;
- generator row-sum max abs `5.551115123125783e-17`; literal minimum off-diagonal `0.0`;
- KFE mass error `0.0`, stationarity residual `3.69712940817557e-17`, state marginals `[0.5,0.5]`;
- deterministic repeat differences all `0.0 <= 1e-12`;
- no outer GE, regional/W, nominal, shock/transition, neural or empirical-calibration authority was consumed.

Authoritative roadmap:
`docs/roadmaps/DLH_MASTER_ROADMAP_INITIAL_2026_08_19.md`

## Sole active Builder authority

GitHub Issue #6:

`DLH-2B: Single-region Tier-0 HA/Aiyagari steady-state general equilibrium`

Issue URL:
`https://github.com/zcx369658780/deep-learning-hank/issues/6`

Builder: DSH

Expected dedicated branch:
`dsh/issue-6-dlh-2b-tier0-steady-state-ge-2026-08-19`

## Current gate purpose

DLH-2B closes the accepted fixed-price household/KFE kernel with a minimal one-region two-factor firm, balanced fiscal transfer and productive-capital market.

Economic closure:

`K -> (w,r) -> transfer -> HJB -> KFE -> mean assets A(K) -> R_K(K)=K-A(K)`.

The task must independently validate:
- deterministic `brentq` capital clearing;
- HJB/KFE diagnostics at equilibrium;
- effective labor from the CTMC stationary distribution and final KFE consistency;
- goods/resource accounting;
- household aggregate-budget accounting;
- mean asset drift;
- deterministic full-steady-state reproducibility;
- preservation of all accepted DLH-2A regressions.

## Scope boundary

DLH-2B remains a small **real single-region HA/Aiyagari Tier-0 validation fixture**, not genuine HANK.

It does **not** authorize:
- `W^L`, `W^K`, old `W`, spatial/multi-region code;
- SOE third factor or RegionalAccounts;
- nominal/Fisher/NKPC/Taylor-rule block;
- shocks/AR(1) or transition;
- neural/RL work;
- empirical data/calibration/regression;
- legacy Matlab access;
- Results/policy/novelty claims;
- PR/merge/Issue-close/successor/self-accept by Builder.

## Queued next gate — NOT ACTIVE

A post-DLH-2B Tier-0 numerical robustness / limiting-case validation gate may be issued only after independent review of Issue #6. Genuine-HANK implementation remains later and separately authorized.