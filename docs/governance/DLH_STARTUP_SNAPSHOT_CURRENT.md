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
- `main` remains unprotected unless a fresh read proves otherwise;
- DSH may not self-accept, merge main, close Issue, create successor/PR, or widen scientific scope unless explicitly authorized.

## Current task state

`ACTIVE_GITHUB_ISSUE_11__DLH_3B_HANK_STEADY_STATE_STRUCTURAL_KERNEL`

**Active Builder authority: GitHub Issue #11 only.**

Issue title:

`DLH-3B: Minimal HANK steady-state structural kernel and D2 validation`

Issue URL:

`https://github.com/zcx369658780/deep-learning-hank/issues/11`

Task nature:

`STEADY_STATE_IMPLEMENTATION_AND_BOUNDED_CPU_D2_VALIDATION_ONLY`

Dedicated Builder branch:

`dsh/issue-11-dlh-3b-hank-steady-state-2026-08-20`

Expected successful candidate classification:

`DLH_3B_HANK_STEADY_STATE_STRUCTURAL_KERNEL_READY_FOR_GPT_REVIEW`

## Accepted stages through DLH-3A

- Issues #1–#6: accepted/closed under their canonical commits and D1/D2 evidence boundaries.
- Issue #7: `DLH_2C_BOUNDARY_SENSITIVITY_BLOCKED_ACCEPTED_AND_CLOSED`.
- Issue #8: `DLH_2C_B1_WIDE_DOMAIN_GRID_CONVERGENCE_BLOCKED_ACCEPTED_AND_CLOSED`.
- Issue #9: `DLH_2C_B2_FIXED_DOMAIN_GRID_CONVERGENCE_ACCEPTED_AND_CLOSED`, commit `5632ee1cbc781d67daf305f315f556506da0f6df`.
- Issue #10 DLH-3A: R0 candidate `4b17acb...` rejected for equation inconsistencies; R1 candidate `f56a7c4058a32cc0a7bdc903cada98602a3706b1` independently accepted, fast-forwarded to main and Issue closed with classification `DLH_3A_R1_EQUATION_CONSISTENCY_ACCEPTED`.

Issue #7 and #8 remain accepted fail-closed provenance, not retroactive PASS.

## Final Tier-0 reference

Scientific object: small one-region real HA/Aiyagari benchmark, **not genuine HANK**.

- `VALIDATION_FIXTURE_NOT_CALIBRATION`;
- canonical Tier-0 asset domain `[0,200]`;
- C200/F200/Q200 = 317/633/1265 points;
- `K_C=28.218969081766193`;
- `K_F=28.079912014017818`;
- `K_Q=28.010252116571742`;
- `d_C_F=0.00495219029457629`;
- `d_F_Q=0.00248694289348661`;
- F200→Q200 macro differences all `<0.005`;
- Q200 repeat differences all `0.0`;
- Issue #9 full suite `54 passed / 0 failed`.

Tier-0 Q200 remains a real-HA numerical reference only. Its domain adequacy is not inherited by the HANK economy.

## Accepted DLH-3A R1 equation contract

Accepted commit:

`f56a7c4058a32cc0a7bdc903cada98602a3706b1`

The accepted single-region HANK validation route uses:

- one liquid/risk-free real financial asset, not Tier-0 productive capital;
- two-state idiosyncratic CTMC;
- CRRA consumption + endogenous static labor;
- continuous-time HJB/KFE semantics and stationary reduction;
- `Z_t` = aggregate productivity, `A^hh_t` = household liquid assets;
- labor-only production `Y_t=Z_t N_t`;
- Rotemberg pricing with an explicitly derived exact nonlinear price-setting FOC and a frozen local-linear NKPC for the validation route;
- Fisher relation and Taylor rule `i_t = r_bar + pi_bar + phi_pi*(pi_t-pi_bar)+epsilon_i_t`;
- constant real bond supply `B` through 3B–3D;
- fiscal transfer and lump-sum profit/dividend incidence;
- explicit HJB/KFE/asset/labor/goods/fiscal/profit/wealth/NKPC/Fisher/Taylor residuals.

Owner deferral remains binding: this is a single-region validation architecture, not an irreversible final regional steady-state NSR-HANK asset/production structure.

## Issue #11 scientific scope

DLH-3B implements the **zero-inflation / zero-shock steady-state structural kernel** only.

Frozen validation fixture in Issue #11 includes:

- liquid asset grid `[0,100]`, 401 points, explicitly a starting development domain rather than proven HANK domain adequacy;
- states `(0.5,1.5)`, CTMC intensities `0.25/0.25`;
- `rho_hh=0.01`, `gamma=2.0`, `tau_l=0.15`;
- endogenous labor: `frisch=1.0`, `chi=0.70`, `n_max=5.0`;
- `Z=1.0`, `epsilon=6.0`, `phi_p=100.0`;
- `phi_pi=1.5`, `pi_bar=0`, `epsilon_i=0`;
- constant real bond supply `B=10.0`, `G=0`;
- deterministic nested `brentq` steady-state roots in real return and aggregate labor;
- HJB/KKT, KFE, asset/labor clearing, accounting, nominal consistency, reproducibility, gross upper-bound truncation sanity and full Tier-0 regression gates.

Evidence ceiling for a successful Issue #11 result:

`D2_MACHINE_DIAGNOSTIC__HANK_STEADY_STATE_STRUCTURAL_ONLY`

A 3B PASS does **not** establish dynamic HANK monetary transmission.

## Exact authority / forbidden boundary

Issue #11 alone defines its 16-path allowlist and exact equations, fixture, root scans and thresholds. Builder must read the fresh Issue body/comments before mutation.

Explicitly no authority for:

- mutation of accepted Tier-0 modules/tests/configs/evidence;
- mutation of accepted DLH-3A specifications;
- time-dependent HJB/KFE;
- transition paths;
- monetary/TFP/fiscal shock simulation or IRFs;
- regional / `W^L` / `W^K` / `W^G`;
- multi-region code;
- neural/RL/training/GPU;
- empirical calibration/data/regression;
- legacy Matlab / old Python reference repo / private Zotero access;
- HANK domain/grid robustness claims beyond Issue #11's gross-truncation sanity gate;
- Results/policy/welfare/novelty claims;
- Builder PR/merge/Issue close/successor/self-accept.

Future DLH-3C/3D/3E remain `NO_BUILDER_AUTHORITY` until separate open GitHub Issues exist.

## Required Builder startup order

1. fresh fetch live `refs/heads/main`;
2. read `project_rules/PROJECT_RULE_INDEX_CURRENT.md` and all required CURRENT rules;
3. read `tasks/TASK_INDEX_CURRENT.md`;
4. read this Startup Snapshot;
5. read Master Roadmap;
6. read all four accepted DLH-3A R1 contracts;
7. read only the accepted Tier-0 interfaces/provenance explicitly authorized by Issue #11;
8. fresh-read GitHub Issue #11 body + all comments;
9. confirm Issue #11 remains OPEN and Task Index points exactly to it before mutation.