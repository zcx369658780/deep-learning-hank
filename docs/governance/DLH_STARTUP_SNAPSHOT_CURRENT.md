# Deep Learning + HANK Startup Snapshot — CURRENT

Date: 2026-08-20

Repository: `zcx369658780/deep-learning-hank`

Local Owner-designated workspace: `D:\deep-learning-hank`

Canonical handoff:

`docs/governance/DLH_SESSION_HANDOFF_AFTER_TIER0_NUMERICAL_ROBUSTNESS_COMPLETE_2026_08_19.md`

## Governance state

- live GitHub `main` = sole synchronized repository/governance authority;
- an open GitHub Issue explicitly pointed to by `tasks/TASK_INDEX_CURRENT.md` = sole DSH Builder task authority;
- DSH = bounded Builder;
- ChatGPT = independent fresh-GitHub reviewer / scientific-route authority / task issuer;
- Owner = final scientific-direction authority;
- Builder completion summary is not acceptance evidence;
- correct fail-closed scientific BLOCKED results may be accepted without relabeling PASS;
- DSH may not self-accept, merge main, close Issue, create successor/PR, or widen scientific scope unless explicitly authorized.

## Current task state

`ACTIVE_GITHUB_ISSUE_12__DLH_3C_TIME_DEPENDENT_HOUSEHOLD_KFE`

**Active Builder authority: GitHub Issue #12 only.**

Issue title:

`DLH-3C: Time-dependent household HJB/KFE response under prescribed small paths`

Issue URL:

`https://github.com/zcx369658780/deep-learning-hank/issues/12`

Task nature:

`TIME_DEPENDENT_HOUSEHOLD_HJB_KFE_UNDER_PRESCRIBED_SMALL_PATHS_ONLY`

Dedicated Builder branch:

`dsh/issue-12-dlh-3c-time-dependent-household-kfe-2026-08-20`

Expected successful candidate classification:

`DLH_3C_TIME_DEPENDENT_HOUSEHOLD_KFE_RESPONSE_READY_FOR_GPT_REVIEW`

Evidence ceiling if successful:

`D2_MACHINE_DIAGNOSTIC__HANK_TIME_DEPENDENT_HOUSEHOLD_KFE_ONLY`

## Accepted stages through DLH-3B

- Issues #1–#6: accepted/closed under their canonical commits and D1/D2 evidence boundaries.
- Issue #7: `DLH_2C_BOUNDARY_SENSITIVITY_BLOCKED_ACCEPTED_AND_CLOSED`.
- Issue #8: `DLH_2C_B1_WIDE_DOMAIN_GRID_CONVERGENCE_BLOCKED_ACCEPTED_AND_CLOSED`.
- Issue #9: `DLH_2C_B2_FIXED_DOMAIN_GRID_CONVERGENCE_ACCEPTED_AND_CLOSED`, commit `5632ee1cbc781d67daf305f315f556506da0f6df`.
- Issue #10 DLH-3A: corrected R1 candidate `f56a7c4058a32cc0a7bdc903cada98602a3706b1` independently accepted/closed as `DLH_3A_R1_EQUATION_CONSISTENCY_ACCEPTED`.
- Issue #11 DLH-3B: candidate `267fef0386098796c06f4b7bf331121af9061a43` independently accepted/closed as `DLH_3B_HANK_STEADY_STATE_STRUCTURAL_KERNEL_ACCEPTED_WITH_OBSERVATIONS`; evidence ceiling `D2_MACHINE_DIAGNOSTIC__HANK_STEADY_STATE_STRUCTURAL_ONLY`.

Issue #7 and #8 remain accepted fail-closed provenance, not retroactive PASS.

## Final Tier-0 reference

Scientific object: small one-region real HA/Aiyagari benchmark, not genuine HANK.

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

## Accepted DLH-3A architecture / DLH-3B steady state

The accepted single-region validation route uses:

- one liquid/risk-free real financial asset, not Tier-0 productive capital;
- two-state idiosyncratic CTMC;
- CRRA consumption + endogenous static labor;
- continuous-time HJB/KFE semantics and stationary reduction;
- labor-only production `Y=Z*N`;
- Rotemberg price-setting convention;
- Fisher relation and Taylor rule;
- constant real bond supply `B` through 3B–3D;
- fiscal transfer and lump-sum profit/dividend incidence;
- explicit household/distribution/market/accounting/nominal residuals.

Accepted DLH-3B commit:

`267fef0386098796c06f4b7bf331121af9061a43`

Accepted central D2 steady-state provenance:

- accepted DLH-3B config SHA-256 `82AB4A02F9D08FBBAED1349BC027FACE5361B1AB24C710C4CEA6958481CD5FC1`;
- `r*=i*=0.007370613883670197`;
- `N*=1.0656334480169984`;
- `Y*=1.0656334480169984`;
- `w*=5/6`;
- `tr*=0.05949804216542284`;
- `Pi*=0.17760557466949967`;
- `A_hh=10.000000002223675` against `B=10`;
- `R_asset≈2.22e-9`, `R_labor≈5.50e-10`, `R_goods≈-4.06e-10`;
- true HJB residual `≈6.76e-8 <=1e-7`;
- KFE stationarity residual `≈1.26e-15`;
- state-marginal error `≈2.22e-16`;
- full repository suite reported `77 passed / 0 failed`;
- deterministic repeat differences reported exactly `0.0`.

Acceptance observations:

- structural `all_gates_pass` does not itself include reproducibility, but reproducibility is separately mandatory and enforced by the accepted test suite;
- the accepted HJB residual passes but is not a robustness-margin claim;
- `[0,100]` / 401 points passed gross truncation sanity only and is not accepted HANK domain adequacy.

Owner deferral remains binding: this single-region validation structure does not irreversibly freeze the later regional steady-state NSR-HANK asset/production architecture.

## Issue #12 scientific scope

DLH-3C validates the first **time-dependent household/distribution engine** while keeping aggregate GE open.

Frozen transition-validation structure in Issue #12 includes:

- accepted DLH-3B steady state as terminal/initial baseline;
- primary horizon `T=12`, `dt=0.05`;
- long horizon `T_long=16` at the same `dt`;
- compact-support numerical bump `sin(pi*t/5)^2` on `[0,5]`;
- Path W: prescribed wage-only bump, peak relative amplitude `0.002`;
- Path R: prescribed real-return-only bump, peak additive amplitude `0.001`;
- full/half/quarter/zero amplitude sequence;
- implicit backward HJB with within-step policy iteration;
- implicit forward KFE without mass renormalization;
- zero-path invariance;
- nontrivial response + amplitude-to-zero/local-scaling diagnostics;
- mass/non-negativity/boundary/KKT/HJB gates;
- horizon/terminal robustness on `[0,8]`;
- deterministic reproducibility;
- full predecessor regression.

The prescribed paths are explicitly:

`EXOGENOUS_NUMERICAL_RESPONSE_PATH_NOT_STRUCTURAL_SHOCK`.

They are not IRFs and have no policy interpretation.

## Explicit non-authority during DLH-3C

No authority for:

- mutation of accepted Tier-0 / DLH-3A / DLH-3B paths;
- structural monetary/TFP/fiscal shocks;
- `epsilon_i != 0`;
- endogenous NKPC/inflation feedback or full NK GE closure;
- dynamic market-clearing claims;
- IRF terminology/policy interpretation;
- time-step robustness claims;
- regional / `W^L` / `W^K` / `W^G`;
- neural/RL/training/GPU;
- empirical calibration/data/regression;
- legacy Matlab / old Python reference repository / private Zotero access;
- Results/policy/welfare/novelty claims;
- Builder PR/merge/Issue close/successor/self-accept.

Future DLH-3D/3E remain `NO_BUILDER_AUTHORITY` until separate open GitHub Issues exist.

## Required Builder startup order

1. fresh fetch live `refs/heads/main`;
2. read `project_rules/PROJECT_RULE_INDEX_CURRENT.md` and all required CURRENT rules;
3. read `tasks/TASK_INDEX_CURRENT.md`;
4. read this Startup Snapshot;
5. read Master Roadmap;
6. read all four accepted DLH-3A R1 contracts;
7. read accepted DLH-3B config/modules/tests/evidence only as authorized by Issue #12;
8. fresh-read GitHub Issue #12 body + all comments;
9. confirm Issue #12 remains OPEN and Task Index points exactly to it before mutation.
