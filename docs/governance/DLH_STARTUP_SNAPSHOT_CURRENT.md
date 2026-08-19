# Deep Learning + HANK Startup Snapshot — CURRENT

Date: 2026-08-19

Repository: `zcx369658780/deep-learning-hank`

Local Owner-designated workspace: `D:\deep-learning-hank`

## Governance state

- live GitHub `main` = synchronized repository/governance authority；
- open GitHub Issue = sole DSH Builder task authority；
- `tasks/TASK_INDEX_CURRENT.md` = synchronized Issue pointer only；
- DSH = bounded Builder；
- ChatGPT = independent GitHub reviewer / scientific-route authority / task issuer；
- Owner = final scientific-direction authority。

## Accepted stages

- Issue #1 bootstrap: accepted/closed at `bcded9b9137f3c10f71a7a6ecb929f78b40bdc11`.
- Issue #2 DLH-0 scientific constitution: accepted/closed at `73e1ae5db9d7e362781a77fa2a204c80238fad3e`.
- Issue #3 DLH-1A literature/data feasibility: accepted/closed at `e9aa7dc8a3f5a198b1655c917659f519239eb67b`.
- Issue #4 DLH-1B Python kernel audit: accepted/closed at `8dce318af5ca704a747e67932ec3caa35f9168ad`.
- Issue #5 DLH-2A fixed-price HJB/KFE kernel: accepted/closed after R1 at `76b5882a63d8ade18d50098373b7c735eb2c4ca4`, evidence `D2_MACHINE_DIAGNOSTIC_ONLY`.
- Issue #6 DLH-2B single-region steady-state GE: accepted/closed after R1 at `c562ce3a2743ac779123918e9aab5f37044b564a`, evidence `D2_MACHINE_DIAGNOSTIC_ONLY`.

## Accepted DLH-2B-R1 computational state

Under `VALIDATION_FIXTURE_NOT_CALIBRATION`:

- one-region closure = `K -> (w,r) -> balanced transfer -> HJB -> KFE -> A(K) -> K-A(K)`;
- `K*=27.367823476711713`, capital residual `1.0466294497746276e-11`;
- output `2.6988085539374342`, wage `1.889165987756204`, net return `0.009583739710619838`, mean consumption `2.1514520844030995`;
- HJB residual `1.3058058412340756e-08` and all accepted HJB generator/boundary gates pass;
- KFE mass error `0.0`, stationarity residual `2.905661822261152e-17`, state marginals `[0.5,0.5]`;
- effective-labor error `0.0`;
- independent goods residual `1.0047518372857667e-13`, household-budget residual `0.0`, mean drift `-2.2941717969793274e-16`;
- root evidence semantics: 11 trace evaluations + 1 post-root verification = 12 total capital evaluations; all root-trace entries finite;
- full R1 repository suite `32 passed / 0 failed`, including accepted DLH-2A regression `15/15`;
- deterministic repeat differences all `0.0`.

These establish only D2 evidence for a small real one-region HA/Aiyagari benchmark. They do not establish empirical calibration, genuine HANK, regional NSR-HANK, transition dynamics, policy validity, Results eligibility or novelty.

## Authoritative scientific direction

Roadmap:
`docs/roadmaps/DLH_MASTER_ROADMAP_INITIAL_2026_08_19.md`.

Direction remains:
- Tier 0 = one-region real HA/Aiyagari computational benchmark;
- Tier 1 = minimal genuine single-region HANK nominal/New-Keynesian layer;
- Tier 2 = small multi-region NSR-HANK;
- structural household/firm/HJB/KFE/accounting/clearing stay hard economic modules;
- learned labor-flow network `W^L` first, `W^K` later;
- household home-region fixed initially, labor services mobile;
- cross-year shared network parameters with year-specific observables/weights/equilibria;
- GNN/message passing deferred.

## Current active task

Issue #7 — `DLH-2C: Tier-0 numerical robustness, grid-boundary and invariance validation`

Issue URL:
`https://github.com/zcx369658780/deep-learning-hank/issues/7`

Expected branch:
`dsh/issue-7-dlh-2c-tier0-robustness-2026-08-19`

## DLH-2C authority

DLH-2C is the final planned Tier-0 robustness gate before genuine-HANK implementation.

All accepted DLH-2A/DLH-2B solver/economic modules and accepted tests are frozen. Issue #7 permits only its exact 11-path robustness outputs and these numerical/representation variants:

- baseline `B40_50`: accepted 40-point `[0,50]` fixture;
- `G80_50`: 80-point `[0,50]` refinement;
- `G160_50`: 160-point `[0,50]` refinement;
- `W159_100`: 159-point `[0,100]`, exactly matched spacing to `G80_50`;
- `P40_50`: state-label permutation of the baseline;
- a 21-point bounded `R_K(K)` scan over `[0.5,45.0]`.

Issue #7 freezes all economics, solver families and existing acceptance thresholds. Builder may not tune them after observing robustness results.

## Required robustness questions

1. Do successive fixed-bound grid refinements converge rather than worsen, with final 80→160 capital difference <= 0.5%?
2. Does doubling the asset upper bound at matched spacing change equilibrium capital by <= 0.5%?
3. Is the model invariant to pure state-label permutation within `1e-10` after axis realignment?
4. Does the bounded 21-point residual scan show exactly one finite sign-changing root interval?
5. Does every variant pass the accepted steady-state numerical/accounting gates and same-environment reproducibility <= `1e-12`?

A fail-closed robustness result is scientifically useful and must not be hidden by changing economics or thresholds.

## Current implementation/scientific authority

- DLH-2A fixed-price kernel: `R1_ACCEPTED_D2`；
- DLH-2B single-region steady-state GE: `R1_ACCEPTED_D2`；
- DLH-2C numerical robustness: `ACTIVE_NOT_ACCEPTED`；
- genuine-HANK nominal implementation authority: `NONE`；
- regional/W authority: `NONE`；
- shock/transition authority: `NONE`；
- neural training authority: `NONE`；
- empirical calibration authority: `NONE`；
- Results/manuscript authority: `NONE`；
- final novelty claim authority: `NONE`。

## Current boundaries

No accepted solver/economics/test modification, regional/W, SOE/open-economy, nominal/NK, shock/transition, neural/RL, empirical data/calibration, Matlab/legacy Matlab, old-source-repo access, or Results/policy/novelty work is authorized by Issue #7.

## Queued next gate — NOT ACTIVE

`DLH-3 — minimal genuine single-region HANK nominal/New-Keynesian layer` may only be issued after fresh independent review/disposition of DLH-2C.
