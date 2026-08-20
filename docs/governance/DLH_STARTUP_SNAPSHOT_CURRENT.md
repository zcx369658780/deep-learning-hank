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

`ACTIVE_GITHUB_ISSUE_13__DLH_3D_MINIMAL_HANK_MONETARY_GE`

**Active Builder authority: GitHub Issue #13 only.**

Issue title:

`DLH-3D: Full single-region NK GE closure with first deterministic monetary-policy innovation`

Issue URL:

`https://github.com/zcx369658780/deep-learning-hank/issues/13`

Task nature:

`FULL_MINIMAL_SINGLE_REGION_NK_GE_PLUS_FIRST_DETERMINISTIC_MONETARY_INNOVATION`

Dedicated Builder branch:

`dsh/issue-13-dlh-3d-monetary-ge-2026-08-20`

Expected successful candidate classification:

`DLH_3D_MINIMAL_GENUINE_SINGLE_REGION_HANK_DYNAMIC_VALIDATION_READY_FOR_GPT_REVIEW`

Potential accepted classification after independent review:

`MINIMAL_GENUINE_SINGLE_REGION_HANK_DYNAMIC_VALIDATED`

Evidence ceiling if successful:

`D2_MACHINE_DIAGNOSTIC__MINIMAL_SINGLE_REGION_HANK_DYNAMIC_VALIDATION_FIXTURE`

This remains validation-fixture evidence only, not empirical calibration, policy effectiveness evidence, regional NSR-HANK validation, or Results.

## Accepted stages through DLH-3C

- Issues #1–#6: accepted/closed under their canonical commits and D1/D2 boundaries.
- Issue #7: `DLH_2C_BOUNDARY_SENSITIVITY_BLOCKED_ACCEPTED_AND_CLOSED`.
- Issue #8: `DLH_2C_B1_WIDE_DOMAIN_GRID_CONVERGENCE_BLOCKED_ACCEPTED_AND_CLOSED`.
- Issue #9: `DLH_2C_B2_FIXED_DOMAIN_GRID_CONVERGENCE_ACCEPTED_AND_CLOSED`, commit `5632ee1cbc781d67daf305f315f556506da0f6df`.
- Issue #10 / DLH-3A: corrected R1 `f56a7c4058a32cc0a7bdc903cada98602a3706b1` accepted/closed as `DLH_3A_R1_EQUATION_CONSISTENCY_ACCEPTED`.
- Issue #11 / DLH-3B: `267fef0386098796c06f4b7bf331121af9061a43` accepted/closed as `DLH_3B_HANK_STEADY_STATE_STRUCTURAL_KERNEL_ACCEPTED_WITH_OBSERVATIONS`; ceiling `D2_MACHINE_DIAGNOSTIC__HANK_STEADY_STATE_STRUCTURAL_ONLY`.
- Issue #12 / DLH-3C: `3b24790e24e7b7d358848f55640b255a3a2b3191` accepted/closed as `DLH_3C_TIME_DEPENDENT_HOUSEHOLD_KFE_RESPONSE_ACCEPTED_WITH_OBSERVATIONS`; ceiling `D2_MACHINE_DIAGNOSTIC__HANK_TIME_DEPENDENT_HOUSEHOLD_KFE_ONLY`.

Issue #7 and #8 remain accepted fail-closed provenance, not retroactive PASS.

## Accepted scientific baseline

### Tier-0

Tier-0 remains a small one-region real HA/Aiyagari validation benchmark, not genuine HANK. Q200 `[0,200]` is the accepted Tier-0 numerical reference only; HANK domain adequacy must be established separately.

### DLH-3A equation architecture

The accepted single-region HANK validation route has:

- one liquid/risk-free real financial asset, not Tier-0 productive capital;
- two-state idiosyncratic CTMC;
- CRRA + endogenous static labor;
- continuous-time HJB/KFE;
- labor-only production `Y=Z*N`;
- Rotemberg pricing with accepted local-linear operational NKPC;
- Fisher relation + Taylor rule;
- constant real bond supply `B` through 3B–3D;
- explicit market/accounting/nominal residuals.

Owner deferral remains binding: this is not an irreversible final regional steady-state NSR-HANK asset/production architecture.

### DLH-3B steady state

Accepted config SHA-256:

`82AB4A02F9D08FBBAED1349BC027FACE5361B1AB24C710C4CEA6958481CD5FC1`

Central accepted D2 provenance:

- `r*=i*=0.007370613883670197`;
- `N*=Y*=1.0656334480169984`;
- `w*=5/6`;
- `tr*=0.05949804216542284`;
- `Pi*=0.17760557466949967`;
- `A_hh*=10.000000002223675` against `B=10`;
- full suite reported `77 passed / 0 failed`;
- deterministic repeat differences `0.0`.

`[0,100]/401` is still only a starting development domain / gross-truncation result.

### DLH-3C dynamic household/KFE engine

Accepted config SHA-256:

`C7AA76DF3758F46FCBA827872FC0FD0078EDD5309CCFAD04E32C42F5CB4D39A2`

Accepted D2 transition-numerics evidence:

- implicit backward HJB with terminal `V(T)=V_ss`;
- implicit forward KFE without mass renormalization;
- zero-path invariance;
- prescribed non-structural W/R response paths and amplitude-to-zero checks;
- horizon/terminal robustness at fixed `dt`;
- deterministic repeat differences reported `0.0`;
- full suite reported `97 passed / 0 failed`.

DLH-3C acceptance observations remain provenance:

- its execution report misstated the path-diagnostics row count; actual evidence structure was correct;
- a common zero path was used for both W/R families, which is mathematically identical and consistent with the explicit primary-validation-set definition;
- the very small discrete HJB residual is not a time-step robustness result.

## Issue #13 scientific scope

DLH-3D is the **first** gate that may close full minimal single-region NK GE and introduce a small deterministic monetary-policy innovation through `epsilon_i(t)`.

Frozen core route:

`epsilon_i -> Taylor/Fisher -> r -> household HJB/KFE -> A_hh/N_hh/C -> asset/labor clearing -> w,N -> firm/mc -> NKPC -> pi -> Taylor/Fisher`.

At candidate `(w_t,N_t)`:

- `Y=Z*N`, `mc=w/Z`;
- solve accepted local-linear NKPC backward with terminal `pi(T)=0`;
- Taylor + Fisher determine `i_t,r_t`;
- constant-`B` fiscal closure determines transfers;
- Rotemberg-cost-adjusted profits enter household income;
- accepted DLH-3C HJB/KFE engine returns household/distribution paths;
- nonlinear root residuals are asset clearing and labor clearing only;
- goods/resource and dynamic wealth-flow residuals are independent diagnostics.

Validation innovation:

- compact-support nominal-rate innovation on `[0,2]`;
- primary peak `eta_i=0.001`;
- full/half/quarter/zero amplitudes;
- primary `T=12`, `dt=0.05`; long `T=16` at same `dt`.

A successful Issue #13 independent review may first support `MINIMAL_GENUINE_SINGLE_REGION_HANK_DYNAMIC_VALIDATED`, but only at D2 validation-fixture level.

## Explicit non-authority during DLH-3D

No authority for:

- mutation of accepted Tier-0 / DLH-3A / DLH-3B / DLH-3C paths;
- productive capital / investment / Tobin-q;
- varying government debt / extra fiscal states;
- TFP/fiscal shocks or shock estimation;
- empirical calibration/data/regression;
- regional / `W^L` / `W^K` / `W^G` or multi-region code;
- neural/RL/training/GPU;
- legacy Matlab / old Python reference repo / private Zotero;
- time-step robustness claims;
- policy effectiveness / welfare / Results / novelty claims;
- Builder PR/merge/Issue close/successor/self-accept.

Future DLH-3E remains `NO_BUILDER_AUTHORITY` until a separate open Issue exists.

## Required Builder startup order

1. fresh fetch live `refs/heads/main`;
2. read `project_rules/PROJECT_RULE_INDEX_CURRENT.md` and all required CURRENT rules;
3. read `tasks/TASK_INDEX_CURRENT.md`;
4. read this Startup Snapshot;
5. read Master Roadmap;
6. read all four accepted DLH-3A R1 contracts;
7. read accepted DLH-3B and DLH-3C config/modules/tests/evidence as authorized by Issue #13;
8. fresh-read GitHub Issue #13 body + all comments;
9. verify accepted DLH-3B and DLH-3C config hashes;
10. confirm Issue #13 remains OPEN and Task Index points exactly to it before mutation.
