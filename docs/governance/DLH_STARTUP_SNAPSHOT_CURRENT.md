# Deep Learning + HANK Startup Snapshot — CURRENT

Date: 2026-08-19

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
- correct fail-closed scientific BLOCKED results may be accepted as evidence without being relabeled PASS;
- `main` remains unprotected unless a future fresh GitHub read proves otherwise;
- DSH may not self-accept, merge main, close Issue, create successor, create PR, or expand scientific scope unless explicitly authorized.

## Current task state

`ACTIVE_GITHUB_ISSUE_10__DLH_3A_MINIMAL_HANK_ARCHITECTURE`

**Active Builder authority: GitHub Issue #10 only.**

Issue title:

`DLH-3A: Minimal genuine single-region HANK architecture and equation freeze`

Issue URL:

`https://github.com/zcx369658780/deep-learning-hank/issues/10`

Task nature:

`SPECIFICATION_ONLY__ZERO_MODEL_IMPLEMENTATION__ZERO_NUMERICAL_EXECUTION`

Dedicated Builder branch required by Issue #10:

`dsh/issue-10-dlh-3a-minimal-hank-architecture-2026-08-19`

Expected successful Builder candidate classification:

`DLH_3A_MINIMAL_HANK_ARCHITECTURE_READY_FOR_GPT_OWNER_REVIEW`

## Accepted stages

- Issue #1 bootstrap: accepted/closed at `bcded9b9137f3c10f71a7a6ecb929f78b40bdc11`.
- Issue #2 DLH-0 scientific constitution: `DLH_0_R1_NSR_HANK_SCIENTIFIC_CONSTITUTION_ACCEPTED`, accepted/closed at `73e1ae5db9d7e362781a77fa2a204c80238fad3e`.
- Issue #3 DLH-1A literature/data feasibility: accepted/closed at `e9aa7dc8a3f5a198b1655c917659f519239eb67b`.
- Issue #4 DLH-1B Python kernel audit: accepted/closed at `8dce318af5ca704a747e67932ec3caa35f9168ad`.
- Issue #5 DLH-2A fixed-price HJB/KFE: accepted/closed at `76b5882a63d8ade18d50098373b7c735eb2c4ca4`, D2 only.
- Issue #6 DLH-2B steady-state GE: accepted/closed at `c562ce3a2743ac779123918e9aab5f37044b564a`, D2 only.
- Issue #7 DLH-2C robustness: `DLH_2C_BOUNDARY_SENSITIVITY_BLOCKED_ACCEPTED`, accepted/closed at `583e352b3ba37d25ebb7d8f468b5fd9f4f5eb5d3`.
- Issue #8 DLH-2C-B1 asset-domain adequacy: `DLH_2C_B1_WIDE_DOMAIN_GRID_CONVERGENCE_BLOCKED_ACCEPTED`, accepted/closed at `249c9dcaf3c16b4b308e9d83daf232a23dce79cb`.
- Issue #9 DLH-2C-B2 fixed-domain third-level grid convergence: `DLH_2C_B2_FIXED_DOMAIN_GRID_CONVERGENCE_ACCEPTED`, accepted/closed at `5632ee1cbc781d67daf305f315f556506da0f6df`, D2 only.

Issue #7 and #8 remain accepted fail-closed scientific provenance, not retroactive PASS results.

## Final accepted Tier-0 scientific object

The accepted object remains a small **real one-region HA/Aiyagari** benchmark under:

`VALIDATION_FIXTURE_NOT_CALIBRATION`.

It is **not genuine HANK**.

Accepted Tier-0 closure:

`K -> (w,r) -> balanced transfer -> HJB -> stationary KFE -> A(K) -> R_K(K)=K-A(K)`.

Accepted structural core includes:

- one liquid/productive asset in the Tier-0 economy;
- productivity states `(0.5,1.5)`, symmetric CTMC intensities `0.25/0.25`;
- CRRA `gamma=2.0`, `rho_hh=0.01`, inelastic labor;
- labor tax `tau_l=0.15`;
- state-constraint/no-outward-drift HJB;
- continuous-time infinitesimal generator / intensity matrix;
- stationary KFE;
- two-factor Cobb-Douglas validation fixture `A=1.0`, `alpha_k=0.30`, `delta=0.02`;
- `G=0.0` balanced transfer;
- deterministic `brentq` capital clearing.

## Final Tier-0 numerical standard

Canonical Tier-0 asset domain:

`a in [0,200]`.

Accepted grids:

- C200: 317 points;
- F200: 633 points;
- Q200: 1265 points.

Accepted capital sequence:

- `K_C=28.218969081766193`;
- `K_F=28.079912014017818`;
- `K_Q=28.010252116571742`.

Accepted same-domain differences:

- `d_C_F=0.00495219029457629`;
- `d_F_Q=0.00248694289348661`.

Refinement ratio observation:

`0.5021904946201973` — observation only, no strong-refinement claim.

F200→Q200 macro relative differences are all `<0.005`; Q200 required reproducibility differences are all `0.0`; Issue #9 full suite = `54 passed / 0 failed`.

The planned Tier-0 numerical-robustness block is **COMPLETE at D2 machine-diagnostic level**.

Q200 `[0,200]` is the accepted high-accuracy Tier-0 validation/reference standard. Its domain adequacy is not automatically inherited by a later HANK economy with different asset semantics.

## Issue #10 scientific architecture boundary

DLH-3A must specify, not implement, a minimal genuine single-region HANK validation architecture with:

- one liquid/risk-free financial asset for the DLH-3 validation economy, explicitly distinguished from Tier-0 productive capital;
- heterogeneous households and the existing two-state idiosyncratic CTMC starting fixture;
- CRRA consumption utility + endogenous static labor supply;
- time-dependent HJB / forward KFE semantics and stationary reduction;
- minimal labor-based production so productive-capital dynamics are not forced into the first HANK gate;
- monopolistic competition / markup object;
- Rotemberg nominal price adjustment and an explicit NKPC residual;
- nominal policy rate, inflation, real liquid return, Fisher relation and Taylor-type rule;
- positive exogenous liquid government-bond/asset supply, labor-tax treatment, government budget, lump-sum transfer, firm-profit/dividend accounting;
- explicit household, market, fiscal and nominal residual objects.

### Owner deferral — important

The above is a **single-region HANK validation architecture**, not an irreversible final NSR-HANK regional steady-state architecture.

After the future regional steady-state program is sufficiently formed, Owner/ChatGPT may decide whether to retain, modify or replace the DLH-3 validation asset/production structure.

DSH must preserve this caveat in all Issue #10 outputs.

## Future subgate boundaries — NO CURRENT BUILDER AUTHORITY

Issue #10 must specify the boundaries only:

- `DLH-3B`: HANK zero-inflation/zero-shock steady-state structural kernel;
- `DLH-3C`: time-dependent household/KFE response under externally prescribed small aggregate price/income paths;
- `DLH-3D`: full NK GE + first small deterministic monetary-policy innovation;
- `DLH-3E`: HANK-specific asset-domain/grid/time-step/horizon/reproducibility robustness.

No future subgate is active until a separate open GitHub Issue is created.

Only a successful future 3D independent review may first qualify for a classification equivalent to:

`MINIMAL_GENUINE_SINGLE_REGION_HANK_DYNAMIC_VALIDATED`.

Even then, evidence remains validation-fixture evidence, not empirical calibration or Results.

## Issue #10 exact Builder output allowlist

1. `docs/specifications/DLH_3_MINIMAL_GENUINE_HANK_ARCHITECTURE_2026_08_19.md`
2. `docs/specifications/DLH_3_ASSET_FISCAL_AND_NOMINAL_SEMANTICS_CONTRACT_2026_08_19.md`
3. `docs/specifications/DLH_3_STEADY_STATE_AND_DYNAMIC_EQUATION_CONTRACT_2026_08_19.md`
4. `docs/specifications/DLH_3_VALIDATION_LIMITING_CASE_AND_GRID_CONTRACT_2026_08_19.md`
5. `reports/dlh_3a_minimal_hank_architecture_2026_08_19/DLH_3A_REVIEW_PACKET.md`
6. `reports/dlh_3a_minimal_hank_architecture_2026_08_19/DLH_3A_FORBIDDEN_OPERATION_CHECK.md`

No other tracked path may change.

## Explicit non-authority during DLH-3A

No authority for:

- any `src/**`, `configs/**`, `tests/**` mutation;
- model/solver execution;
- HANK steady-state implementation;
- shocks/transition/IRFs;
- productive-capital accumulation/q/investment dynamics;
- regional / `W^L` / `W^K` / `W^G` implementation;
- neural/RL/training;
- empirical calibration/data work;
- legacy Matlab or old Python reference-repository access;
- Results/policy/welfare/novelty claims;
- Builder PR/merge/Issue close/successor/self-accept.

## Governance numbering clarification

Reviewer-side governance commit `689101a9e2d94269bc6bac94358ee3e45182b995` clarified that the older `DLH-*` sequence inside `PROJECT_RULE_MODEL_DEVELOPMENT_DIAGNOSTIC_GATES_CURRENT.md` is generic diagnostic-category provenance only.

CURRENT project-stage identity comes from:

1. fresh Master Roadmap;
2. `tasks/TASK_INDEX_CURRENT.md`;
3. the current open Issue.

Therefore CURRENT project-stage `DLH-3` is the minimal genuine single-region HANK layer, while neural-method specification remains unauthorized until a later explicit roadmap/Issue gate.

## Required Builder startup order

1. fresh fetch live `refs/heads/main`;
2. read canonical handoff;
3. read `project_rules/PROJECT_RULE_INDEX_CURRENT.md` and all required CURRENT rules;
4. read `tasks/TASK_INDEX_CURRENT.md`;
5. read this Startup Snapshot;
6. read Master Roadmap;
7. read accepted DLH-0 constitution materials;
8. read accepted DLH-2A / DLH-2B contracts/code required for interface semantics;
9. read Issue #9 robustness reports/results as numerical-reference provenance;
10. fresh-read GitHub Issue #10 body + all authoritative comments;
11. confirm Issue #10 remains open and Task Index points to it before any mutation.
