# Deep Learning + HANK Startup Snapshot — CURRENT

Date: 2026-08-19

Repository: `zcx369658780/deep-learning-hank`

Local Owner-designated workspace: `D:\deep-learning-hank`

## Current governance state

- live GitHub `main` = synchronized repository/governance authority；
- open GitHub Issue = sole DSH Builder task authority；
- `tasks/TASK_INDEX_CURRENT.md` = synchronized Issue pointer only；
- DSH = bounded Builder；
- ChatGPT = independent GitHub reviewer / scientific-route authority / task issuer；
- Owner = final scientific-direction authority。

## Accepted stages

### Issue #1 — Bootstrap
Accepted and closed at `bcded9b9137f3c10f71a7a6ecb929f78b40bdc11`.

### Issue #2 — DLH-0 / NSR-HANK scientific constitution
Accepted and closed after R1 at `73e1ae5db9d7e362781a77fa2a204c80238fad3e`.

### Issue #3 — DLH-1A literature / labor-flow data feasibility
Accepted and closed after R1 at `e9aa7dc8a3f5a198b1655c917659f519239eb67b`.

Key evidence state:
- true annual bilateral O-D labor-flow labels for direct `W^L_ij,t` supervision remain unresolved;
- CMDS remains a repeated migrant cross-section / possible O-D stock source pending schema/weight harmonization;
- E3 literature evidence remains zero; final novelty claims remain unauthorized.

### Issue #4 — DLH-1B Python kernel read-only audit
Accepted and closed after R2 at `8dce318af5ca704a747e67932ec3caa35f9168ad`.

Accepted source identity:
`zcx369658780/dissertation-ch5-r5-python-model` @ `3039a145f43d419a08999c476cd0d97fd5f8341f`.

### Issue #5 — DLH-2A fixed-price household/KFE kernel
Accepted and closed after R1 at `76b5882a63d8ade18d50098373b7c735eb2c4ca4`.

Acceptance classification:
`DLH_2A_R1_TIER0_KERNEL_FIXED_PRICE_VALIDATION_ACCEPTED`.

Accepted evidence level:
`D2_MACHINE_DIAGNOSTIC_ONLY`.

Accepted computational facts under `VALIDATION_FIXTURE_NOT_CALIBRATION`:
- one liquid asset, finite-state productivity, CRRA utility, inelastic labor;
- transparent continuous-time upwind HJB;
- state-constraint / no-outward-drift asset boundaries;
- CTMC infinitesimal generator with nonnegative off-diagonals, negative-outflow diagonal and row sums zero;
- stationary KFE solves `G.T @ g = 0` with mass/non-negativity diagnostics;
- R1 suite = `15 passed / 0 failed / 0 skipped`;
- HJB true residual = `8.335084289434747e-08`;
- generator row-sum max abs = `5.551115123125783e-17`;
- literal minimum off-diagonal = `0.0`;
- KFE mass error = `0.0`;
- KFE stationarity residual = `3.69712940817557e-17`;
- KFE state marginals = `[0.5,0.5]`;
- deterministic repeat differences = all `0.0`.

These facts establish only a small fixed-price household/distribution kernel. They do not establish empirical calibration, HANK, regional equilibrium, policy validity or Results eligibility.

## Authoritative scientific direction

Roadmap:
`docs/roadmaps/DLH_MASTER_ROADMAP_INITIAL_2026_08_19.md`.

First-generation NSR-HANK direction remains:
- province-local structural household / firm / HJB / KFE / accounting / clearing;
- learned `W^L` first, `W^K` later;
- household home-region fixed, labor services mobile;
- Python main implementation language;
- Tier 0 = one-region real HA/Aiyagari computational benchmark;
- Tier 1 = minimal genuine single-region HANK;
- Tier 2 = small multi-region NSR-HANK;
- cross-year shared network parameters + year-specific observables/weights/equilibria;
- GNN/message passing deferred.

## Current active task

Issue #6 — `DLH-2B: Single-region Tier-0 HA/Aiyagari steady-state general equilibrium`

Issue URL:
`https://github.com/zcx369658780/deep-learning-hank/issues/6`

Expected branch:
`dsh/issue-6-dlh-2b-tier0-steady-state-ge-2026-08-19`

## DLH-2B economic closure

Build only on accepted `deep-learning-hank/main`:

`K -> two-factor firm -> (w,r) -> balanced fiscal transfer -> accepted HJB -> accepted KFE -> mean assets A(K) -> capital residual K-A(K)`.

Key definitions:
- effective labor `L_bar = sum_z pi_z*z` from CTMC stationary probabilities, not hard-coded;
- firm `Y=A*K^alpha*L_bar^(1-alpha)`;
- household equilibrium asset return `r = MPK-delta`;
- fiscal transfer `tau_l*w*L_bar - G`;
- capital clearing solved deterministically by bracketed `brentq`;
- final independent diagnostics include capital residual, goods/resource residual, household aggregate-budget residual and mean asset drift.

DLH-2B must rerun and preserve the full accepted DLH-2A regression suite.

## Current scientific / implementation state

- master roadmap: `INITIAL_V0_1_PUBLISHED`；
- scientific constitution: `DLH_0_R1_ACCEPTED`；
- DLH-1A evidence/data feasibility: `ACCEPTED_WITH_DATA_BLOCKER_RECORDED`；
- DLH-1B source audit: `R2_ACCEPTED`；
- DLH-2A fixed-price kernel: `R1_ACCEPTED_D2`；
- DLH-2B single-region steady-state GE: `ACTIVE_NOT_ACCEPTED`；
- regional/W authority: `NONE`；
- nominal/genuine-HANK implementation authority: `NONE`；
- shock/transition authority: `NONE`；
- neural training authority: `NONE`；
- empirical calibration authority: `NONE`；
- numerical Results/manuscript authority: `NONE`；
- final novelty claim authority: `NONE`。

## Current boundaries

Issue #6 remains a `VALIDATION_FIXTURE_NOT_CALIBRATION` one-region real HA/Aiyagari steady-state task.

No regional/W, SOE third factor, open-economy accounts, nominal/NK, shocks, transition, neural/RL, empirical data/calibration, legacy Matlab access or Results/policy claims are authorized.

## Queued next gate — NOT ACTIVE

A Tier-0 numerical robustness / limiting-case validation gate may follow only after fresh independent review of DLH-2B. Genuine-HANK implementation remains a later separate gate.