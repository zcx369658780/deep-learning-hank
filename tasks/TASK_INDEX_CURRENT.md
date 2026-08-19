# Deep Learning + HANK Task Index

Status: `ACTIVE_GITHUB_ISSUE_11__DLH_3B_HANK_STEADY_STATE_STRUCTURAL_KERNEL`

## Canonical session handoff

`docs/governance/DLH_SESSION_HANDOFF_AFTER_TIER0_NUMERICAL_ROBUSTNESS_COMPLETE_2026_08_19.md`

A Builder invocation must fresh-fetch live `main` before using this pointer.

## Accepted provenance

- Issue #1 bootstrap: accepted/closed, commit `bcded9b9137f3c10f71a7a6ecb929f78b40bdc11`.
- Issue #2 DLH-0 scientific constitution: `DLH_0_R1_NSR_HANK_SCIENTIFIC_CONSTITUTION_ACCEPTED_AND_CLOSED`, commit `73e1ae5db9d7e362781a77fa2a204c80238fad3e`.
- Issue #3 DLH-1A literature/data feasibility: accepted/closed, commit `e9aa7dc8a3f5a198b1655c917659f519239eb67b`.
- Issue #4 DLH-1B Python kernel audit: accepted/closed, commit `8dce318af5ca704a747e67932ec3caa35f9168ad`.
- Issue #5 DLH-2A fixed-price HJB/KFE: `DLH_2A_R1_TIER0_KERNEL_FIXED_PRICE_VALIDATION_ACCEPTED_AND_CLOSED`, commit `76b5882a63d8ade18d50098373b7c735eb2c4ca4`, D2 only.
- Issue #6 DLH-2B single-region real HA steady-state GE: `DLH_2B_R1_TIER0_SINGLE_REGION_STEADY_STATE_GE_ACCEPTED_AND_CLOSED`, commit `c562ce3a2743ac779123918e9aab5f37044b564a`, D2 only.
- Issue #7 DLH-2C robustness: `DLH_2C_BOUNDARY_SENSITIVITY_BLOCKED_ACCEPTED_AND_CLOSED`, commit `583e352b3ba37d25ebb7d8f468b5fd9f4f5eb5d3`.
- Issue #8 DLH-2C-B1 asset-domain adequacy: `DLH_2C_B1_WIDE_DOMAIN_GRID_CONVERGENCE_BLOCKED_ACCEPTED_AND_CLOSED`, commit `249c9dcaf3c16b4b308e9d83daf232a23dce79cb`.
- Issue #9 DLH-2C-B2 fixed-domain grid convergence: `DLH_2C_B2_FIXED_DOMAIN_GRID_CONVERGENCE_ACCEPTED_AND_CLOSED`, commit `5632ee1cbc781d67daf305f315f556506da0f6df`, D2 only.
- Issue #10 DLH-3A architecture/equation freeze: R0 `4b17acb...` NOT accepted; corrected R1 `f56a7c4058a32cc0a7bdc903cada98602a3706b1` independently accepted and Issue closed with classification `DLH_3A_R1_EQUATION_CONSISTENCY_ACCEPTED`.

Issue #7 and #8 remain accepted fail-closed provenance, not retroactive PASS.

## Final accepted Tier-0 numerical standard

Scientific object: small one-region real HA/Aiyagari benchmark, **not genuine HANK**.

- fixture: `VALIDATION_FIXTURE_NOT_CALIBRATION`;
- canonical Tier-0 asset domain `[0,200]`;
- C200/F200/Q200 = 317/633/1265 points;
- `K_C=28.218969081766193`;
- `K_F=28.079912014017818`;
- `K_Q=28.010252116571742`;
- `d_C_F=0.00495219029457629`;
- `d_F_Q=0.00248694289348661`;
- F200→Q200 macro-object relative differences all `<0.005`;
- Q200 reproducibility differences all `0.0`;
- Issue #9 full suite `54 passed / 0 failed`.

Q200 `[0,200]` remains the accepted Tier-0 reference; its domain adequacy is not inherited by the DLH-3 HANK economy.

## Accepted DLH-3A R1 architecture boundary

Accepted specification commit:

`f56a7c4058a32cc0a7bdc903cada98602a3706b1`

Frozen for the **single-region validation route**:

- one liquid/risk-free real financial asset, distinct from Tier-0 productive capital;
- heterogeneous household + two-state idiosyncratic CTMC;
- CRRA + endogenous static labor;
- continuous-time HJB / forward KFE semantics with stationary reduction;
- labor-only production `Y=Z*N` for the minimal validation economy;
- Rotemberg pricing; accepted exact nonlinear FOC plus operational local-linear NKPC convention;
- Fisher + unambiguous Taylor rule;
- constant real bond supply `B` through 3B–3D, fiscal transfer closure, profits/dividends;
- explicit HJB/KFE/asset/labor/goods/fiscal/profit/wealth/NKPC/Fisher/Taylor residuals.

Owner deferral remains binding: this single-region validation structure does **not** irreversibly freeze the later regional steady-state NSR-HANK asset/production architecture.

## Sole active Builder authority

**GitHub Issue #11 — OPEN**

Title:

`DLH-3B: Minimal HANK steady-state structural kernel and D2 validation`

Issue URL:

`https://github.com/zcx369658780/deep-learning-hank/issues/11`

Task nature:

`STEADY_STATE_IMPLEMENTATION_AND_BOUNDED_CPU_D2_VALIDATION_ONLY`

Issue #11 is the sole DSH Builder authority. Builder must fresh-read its body/comments from GitHub.

Dedicated branch:

`dsh/issue-11-dlh-3b-hank-steady-state-2026-08-20`

Expected success classification:

`DLH_3B_HANK_STEADY_STATE_STRUCTURAL_KERNEL_READY_FOR_GPT_REVIEW`

### Key scientific boundary

DLH-3B may establish only:

`D2_MACHINE_DIAGNOSTIC__HANK_STEADY_STATE_STRUCTURAL_ONLY`

A 3B PASS is **not** full dynamic genuine-HANK validation.

No authority for:

- time-dependent HJB/KFE;
- transition paths;
- monetary/TFP/fiscal shocks or IRFs;
- regional / `W^L` / `W^K` / `W^G`;
- neural/RL/training/GPU;
- empirical calibration/data/regression;
- legacy Matlab or old Python reference-repository access;
- HANK domain/grid robustness claims beyond the Issue #11 gross-truncation sanity gate;
- Results/policy/welfare/novelty claims;
- Builder PR/merge/Issue close/successor/self-accept.

Future DLH-3C/3D/3E remain `NO_BUILDER_AUTHORITY` until separate open Issues are created.

## Governance numbering note

The older `DLH-*` sequence inside `PROJECT_RULE_MODEL_DEVELOPMENT_DIAGNOSTIC_GATES_CURRENT.md` is generic diagnostic-category provenance only. Current project-stage identity comes from the Master Roadmap + this Task Index + the active Issue.