# Deep Learning + HANK Task Index

Status: `ACTIVE_GITHUB_ISSUE_12__DLH_3C_TIME_DEPENDENT_HOUSEHOLD_KFE`

## Canonical session handoff

`docs/governance/DLH_SESSION_HANDOFF_AFTER_TIER0_NUMERICAL_ROBUSTNESS_COMPLETE_2026_08_19.md`

A Builder invocation must fresh-fetch live `main` before using this pointer.

## Accepted provenance

- Issue #1 bootstrap: accepted/closed, commit `bcded9b9137f3c10f71a7a6ecb929f78b40bdc11`.
- Issue #2 DLH-0 scientific constitution: `DLH_0_R1_NSR_HANK_SCIENTIFIC_CONSTITUTION_ACCEPTED_AND_CLOSED`, commit `73e1ae5db9d7e362781a77fa2a204c80238fad3e`.
- Issue #3 DLH-1A literature/data feasibility: accepted/closed, commit `e9aa7dc8a3f5a198b1655c917659f519239eb67b`.
- Issue #4 DLH-1B Python kernel audit: accepted/closed, commit `8dce318af5ca704a747e67932ec3caa35f9168ad`.
- Issue #5 DLH-2A fixed-price HJB/KFE: accepted/closed, commit `76b5882a63d8ade18d50098373b7c735eb2c4ca4`, D2 only.
- Issue #6 DLH-2B single-region real HA steady-state GE: accepted/closed, commit `c562ce3a2743ac779123918e9aab5f37044b564a`, D2 only.
- Issue #7 DLH-2C robustness: `DLH_2C_BOUNDARY_SENSITIVITY_BLOCKED_ACCEPTED_AND_CLOSED`, commit `583e352b3ba37d25ebb7d8f468b5fd9f4f5eb5d3`.
- Issue #8 DLH-2C-B1 asset-domain adequacy: `DLH_2C_B1_WIDE_DOMAIN_GRID_CONVERGENCE_BLOCKED_ACCEPTED_AND_CLOSED`, commit `249c9dcaf3c16b4b308e9d83daf232a23dce79cb`.
- Issue #9 DLH-2C-B2 fixed-domain grid convergence: `DLH_2C_B2_FIXED_DOMAIN_GRID_CONVERGENCE_ACCEPTED_AND_CLOSED`, commit `5632ee1cbc781d67daf305f315f556506da0f6df`, D2 only.
- Issue #10 DLH-3A architecture/equation freeze: corrected R1 `f56a7c4058a32cc0a7bdc903cada98602a3706b1` accepted/closed as `DLH_3A_R1_EQUATION_CONSISTENCY_ACCEPTED`.
- Issue #11 DLH-3B HANK steady-state structural kernel: commit `267fef0386098796c06f4b7bf331121af9061a43` accepted/closed as `DLH_3B_HANK_STEADY_STATE_STRUCTURAL_KERNEL_ACCEPTED_WITH_OBSERVATIONS`; evidence ceiling `D2_MACHINE_DIAGNOSTIC__HANK_STEADY_STATE_STRUCTURAL_ONLY`.

Issue #7 and #8 remain accepted fail-closed provenance, not retroactive PASS.

## Accepted Tier-0 numerical reference

The accepted Tier-0 object remains a small one-region real HA/Aiyagari benchmark, not genuine HANK.

- `VALIDATION_FIXTURE_NOT_CALIBRATION`;
- canonical Tier-0 asset domain `[0,200]`;
- C200/F200/Q200 = 317/633/1265 points;
- `K_C=28.218969081766193`;
- `K_F=28.079912014017818`;
- `K_Q=28.010252116571742`;
- `d_C_F=0.00495219029457629`;
- `d_F_Q=0.00248694289348661`;
- Issue #9 full suite `54 passed / 0 failed`.

Tier-0 domain adequacy is not inherited by HANK.

## Accepted DLH-3A / DLH-3B boundary

Accepted DLH-3A R1 single-region validation architecture:

- one liquid/risk-free real financial asset, distinct from Tier-0 productive capital;
- two-state idiosyncratic CTMC;
- CRRA + endogenous static labor;
- continuous-time HJB / forward KFE semantics with stationary reduction;
- labor-only production `Y=Z*N` for the minimal validation route;
- Rotemberg pricing, Fisher relation and unambiguous Taylor rule;
- constant real bond supply `B` through 3B–3D;
- explicit household/distribution/market/accounting/nominal residuals.

Accepted DLH-3B steady-state kernel commit:

`267fef0386098796c06f4b7bf331121af9061a43`

Central accepted D2 steady-state provenance:

- `r*=i*=0.007370613883670197`;
- `N*=1.0656334480169984`;
- `Y*=1.0656334480169984`;
- `A_hh=10.000000002223675` against `B=10`;
- clearing/accounting/nominal/KFE/KKT gates passed;
- full repository suite reported `77 passed / 0 failed`;
- deterministic repeat differences reported exactly `0.0`;
- `[0,100]` / 401 points passed only gross truncation sanity, not HANK domain adequacy.

Owner deferral remains binding: this validation architecture does not irreversibly freeze the later regional steady-state NSR-HANK asset/production structure.

## Sole active Builder authority

**GitHub Issue #12 — OPEN**

Title:

`DLH-3C: Time-dependent household HJB/KFE response under prescribed small paths`

Issue URL:

`https://github.com/zcx369658780/deep-learning-hank/issues/12`

Task nature:

`TIME_DEPENDENT_HOUSEHOLD_HJB_KFE_UNDER_PRESCRIBED_SMALL_PATHS_ONLY`

Evidence ceiling if successful:

`D2_MACHINE_DIAGNOSTIC__HANK_TIME_DEPENDENT_HOUSEHOLD_KFE_ONLY`

Issue #12 is the sole DSH Builder authority. Builder must fresh-read its body/comments from GitHub.

Dedicated branch:

`dsh/issue-12-dlh-3c-time-dependent-household-kfe-2026-08-20`

Expected success classification:

`DLH_3C_TIME_DEPENDENT_HOUSEHOLD_KFE_RESPONSE_READY_FOR_GPT_REVIEW`

### Scientific boundary

DLH-3C validates only:

- backward time-dependent household HJB;
- forward KFE under the resulting policy generators;
- prescribed non-structural wage-only and real-return-only small paths;
- zero-path invariance;
- amplitude-to-zero / local-scaling diagnostics;
- mass/non-negativity/boundary/KKT/HJB diagnostics;
- horizon/terminal robustness at fixed `dt`;
- deterministic reproducibility and full predecessor regression.

No dynamic asset/labor/goods market clearing is required because the real paths are prescribed and full aggregate GE is intentionally open.

No authority for:

- structural monetary/TFP/fiscal shocks;
- `epsilon_i != 0`;
- endogenous NKPC/inflation feedback or full NK GE;
- IRF terminology or policy interpretation;
- time-step robustness claims;
- regional / `W^L` / `W^K` / `W^G`;
- neural/RL/training/GPU;
- empirical calibration/data/regression;
- legacy Matlab / old Python reference repository / private Zotero access;
- Results/policy/welfare/novelty claims;
- Builder PR/merge/Issue close/successor/self-accept.

Future DLH-3D/3E remain `NO_BUILDER_AUTHORITY` until separate open Issues are created.

## Governance numbering note

The older `DLH-*` sequence in the generic diagnostic-gates rule is provenance only. Current project-stage identity comes from the Master Roadmap + this Task Index + the active Issue.
