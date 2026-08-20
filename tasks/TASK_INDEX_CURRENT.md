# Deep Learning + HANK Task Index

Status: `ACTIVE_GITHUB_ISSUE_13__DLH_3D_MINIMAL_HANK_MONETARY_GE`

## Canonical session handoff

`docs/governance/DLH_SESSION_HANDOFF_AFTER_TIER0_NUMERICAL_ROBUSTNESS_COMPLETE_2026_08_19.md`

A Builder invocation must fresh-fetch live `main` before using this pointer.

## Accepted provenance

- Issues #1–#6: accepted/closed under their canonical commits and D1/D2 evidence boundaries.
- Issue #7: `DLH_2C_BOUNDARY_SENSITIVITY_BLOCKED_ACCEPTED_AND_CLOSED`, commit `583e352b3ba37d25ebb7d8f468b5fd9f4f5eb5d3`.
- Issue #8: `DLH_2C_B1_WIDE_DOMAIN_GRID_CONVERGENCE_BLOCKED_ACCEPTED_AND_CLOSED`, commit `249c9dcaf3c16b4b308e9d83daf232a23dce79cb`.
- Issue #9: `DLH_2C_B2_FIXED_DOMAIN_GRID_CONVERGENCE_ACCEPTED_AND_CLOSED`, commit `5632ee1cbc781d67daf305f315f556506da0f6df`, Tier-0 D2 numerical robustness complete.
- Issue #10 / DLH-3A: corrected R1 `f56a7c4058a32cc0a7bdc903cada98602a3706b1` accepted/closed as `DLH_3A_R1_EQUATION_CONSISTENCY_ACCEPTED`.
- Issue #11 / DLH-3B: `267fef0386098796c06f4b7bf331121af9061a43` accepted/closed as `DLH_3B_HANK_STEADY_STATE_STRUCTURAL_KERNEL_ACCEPTED_WITH_OBSERVATIONS`; ceiling `D2_MACHINE_DIAGNOSTIC__HANK_STEADY_STATE_STRUCTURAL_ONLY`.
- Issue #12 / DLH-3C: `3b24790e24e7b7d358848f55640b255a3a2b3191` accepted/closed as `DLH_3C_TIME_DEPENDENT_HOUSEHOLD_KFE_RESPONSE_ACCEPTED_WITH_OBSERVATIONS`; ceiling `D2_MACHINE_DIAGNOSTIC__HANK_TIME_DEPENDENT_HOUSEHOLD_KFE_ONLY`.

Issue #7 and #8 remain accepted fail-closed provenance, not retroactive PASS.

## Accepted scientific state before DLH-3D

### Tier-0 reference

The Tier-0 object remains a small one-region real HA/Aiyagari benchmark, not genuine HANK. Q200 `[0,200]` remains the accepted Tier-0 numerical reference; its domain adequacy is not inherited by HANK.

### DLH-3A architecture

The accepted single-region HANK validation route uses:

- one liquid/risk-free real financial asset, distinct from Tier-0 productive capital;
- two-state idiosyncratic CTMC;
- CRRA + endogenous static labor;
- continuous-time HJB/KFE semantics;
- labor-only production `Y=Z*N`;
- Rotemberg pricing with accepted local-linear operational NKPC;
- Fisher relation and Taylor rule;
- constant real bond supply `B` through 3B–3D;
- explicit market/accounting/nominal residuals.

Owner deferral remains binding: this validation structure does not irreversibly freeze the later regional steady-state NSR-HANK asset/production structure.

### Accepted DLH-3B steady state

Accepted config SHA-256:

`82AB4A02F9D08FBBAED1349BC027FACE5361B1AB24C710C4CEA6958481CD5FC1`

Central D2 provenance:

- `r*=i*=0.007370613883670197`;
- `N*=Y*=1.0656334480169984`;
- `w*=5/6`;
- `tr*=0.05949804216542284`;
- `Pi*=0.17760557466949967`;
- `A_hh*=10.000000002223675` against `B=10`;
- full suite reported `77 passed / 0 failed`;
- repeat differences `0.0`.

`[0,100] / 401` is a development-domain/gross-truncation result only, not HANK domain adequacy.

### Accepted DLH-3C dynamic household/KFE engine

Accepted transition config SHA-256:

`C7AA76DF3758F46FCBA827872FC0FD0078EDD5309CCFAD04E32C42F5CB4D39A2`

Accepted D2 evidence includes:

- implicit backward household HJB with terminal `V(T)=V_ss`;
- implicit forward KFE `[I-dt*G_k^T]g_{k+1}=g_k` without mass renormalization;
- zero-path invariance;
- prescribed wage-only and real-return-only numerical response paths with amplitude-to-zero/local-scaling checks;
- fixed-`dt` horizon/terminal robustness;
- deterministic repeat differences reported `0.0`;
- full suite reported `97 passed / 0 failed`.

The prescribed 3C paths were `EXOGENOUS_NUMERICAL_RESPONSE_PATH_NOT_STRUCTURAL_SHOCK`, not IRFs.

Non-blocking acceptance observations remain provenance: the execution report misstated the path-diagnostics row count; and the ~1e-12 dynamic HJB residual is an implicit discrete-equation residual, not a time-step robustness result.

## Sole active Builder authority

**GitHub Issue #13 — OPEN**

Title:

`DLH-3D: Full single-region NK GE closure with first deterministic monetary-policy innovation`

Issue URL:

`https://github.com/zcx369658780/deep-learning-hank/issues/13`

Task nature:

`FULL_MINIMAL_SINGLE_REGION_NK_GE_PLUS_FIRST_DETERMINISTIC_MONETARY_INNOVATION`

Issue #13 is the sole DSH Builder authority. Builder must fresh-read its body/comments from GitHub.

Dedicated branch:

`dsh/issue-13-dlh-3d-monetary-ge-2026-08-20`

Expected success candidate classification:

`DLH_3D_MINIMAL_GENUINE_SINGLE_REGION_HANK_DYNAMIC_VALIDATION_READY_FOR_GPT_REVIEW`

If independently accepted, Issue #13 may first qualify the validation fixture for:

`MINIMAL_GENUINE_SINGLE_REGION_HANK_DYNAMIC_VALIDATED`

with ceiling:

`D2_MACHINE_DIAGNOSTIC__MINIMAL_SINGLE_REGION_HANK_DYNAMIC_VALIDATION_FIXTURE`

This is still not empirical calibration, policy effectiveness evidence, regional NSR-HANK validation, or Results.

## DLH-3D key scientific boundary

Issue #13 authorizes the first small deterministic monetary-policy innovation `epsilon_i(t)` and full minimal single-region NK GE closure.

At candidate aggregate paths `(w_t,N_t)` it closes:

- `Y=Z*N`, `mc=w/Z`;
- backward NKPC recursion with terminal `pi(T)=0`;
- Taylor + Fisher -> `i_t,r_t`;
- constant-`B` fiscal transfer and Rotemberg-cost-adjusted profits;
- accepted DLH-3C household HJB/KFE engine;
- nonlinear path roots only for asset clearing and labor clearing;
- goods/resource and wealth flow remain independent diagnostic residuals.

No authority for productive capital, varying debt, TFP/fiscal shocks, empirical calibration/data, regional/W, neural/RL/GPU, legacy sources, time-step robustness claims, policy/welfare/Results/novelty, or Builder PR/merge/close/successor/self-accept.

Future DLH-3E remains `NO_BUILDER_AUTHORITY` until a separate open Issue is created.

## Governance numbering note

The older `DLH-*` sequence in the generic diagnostic-gates rule is provenance only. Current project-stage identity comes from the Master Roadmap + this Task Index + the active Issue.
