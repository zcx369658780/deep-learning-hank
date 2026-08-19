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

Key data/evidence state:
- true annual bilateral O-D labor-flow labels for direct `W^L_ij,t` supervision remain unresolved;
- CMDS is a repeated migrant cross-section / possible annual O-D migrant-stock source pending schema, weights and questionnaire harmonization;
- geodoi `Id=3621` is aggregate/model-derived proxy under current evidence;
- E3 literature evidence remains zero; novelty claims remain unauthorized.

### Issue #4 — DLH-1B Python kernel read-only audit
Accepted and closed after R2 at `8dce318af5ca704a747e67932ec3caa35f9168ad`.

Accepted source identity:
`zcx369658780/dissertation-ch5-r5-python-model` @ `3039a145f43d419a08999c476cd0d97fd5f8341f`.

Accepted audit conclusions:
- old source is a frozen two-region capital-exposure scaffold, not a clean single-region solver;
- household candidate has one liquid asset, finite-state productivity, CRRA utility and inelastic labor;
- HJB source uses upwind finite differences with state-constraint/no-outward-drift boundaries;
- policy matrix is a CTMC infinitesimal generator/intensity matrix with nonnegative off-diagonals and rows summing to zero;
- stationary KFE solves `G.T g = 0` with normalization/diagnostics;
- old `W`, open-economy accounts, SOE third factor, nominal placeholder, shocks and transition are excluded from Tier-0 implementation scope;
- numerical convergence and scientific validity were not established by DLH-1B.

Authoritative 14-row reuse counts:
`2 / 4 / 3 / 3 / 2` = reference / adapter / redesign / drop-from-Tier0 / unresolved.

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

Issue #5 — `DLH-2A: Tier-0 kernel migration and fixed-price HJB/KFE validation`

Issue URL:
`https://github.com/zcx369658780/deep-learning-hank/issues/5`

Expected branch:
`dsh/issue-5-dlh-2a-tier0-kernel-validation-2026-08-19`

## DLH-2A authority

This is the first implementation + numerical-execution gate.

Allowed only under exact Issue #5 scope:
- create the new `src/deep_learning_hank` package within the 21-path allowlist;
- adapt/reimplement accepted HJB/KFE/grid patterns from the read-only source repo;
- implement two-factor firm and minimal fiscal helpers for unit-level tests;
- execute a fixed-price small validation fixture labeled `VALIDATION_FIXTURE_NOT_CALIBRATION`;
- run HJB/KFE diagnostics, new pytest suite and deterministic repeat validation;
- create a task-local environment/install minimal dependencies only if needed.

The HJB/KFE contract must preserve:
- CTMC generator/intensity matrix, not row-stochastic;
- state-constraint/no-outward-drift asset boundaries;
- explicit HJB residual;
- stationary KFE residual/mass/non-negativity diagnostics.

## Current scientific / implementation state

- master roadmap: `INITIAL_V0_1_PUBLISHED`；
- scientific constitution: `DLH_0_R1_ACCEPTED`；
- DLH-1A evidence/data feasibility: `ACCEPTED_WITH_DATA_BLOCKER_RECORDED`；
- DLH-1B source audit: `R2_ACCEPTED`；
- DLH-2A implementation: `ACTIVE_NOT_ACCEPTED`；
- outer steady-state GE authority: `NONE`；
- regional/W authority: `NONE`；
- nominal/genuine-HANK implementation authority: `NONE`；
- shock/transition authority: `NONE`；
- neural training authority: `NONE`；
- numerical Results/manuscript authority: `NONE`；
- final novelty claim authority: `NONE`。

## Current boundaries

Issue #5 does NOT authorize outer GE solving, regional links, nominal/NK blocks, shocks, transition, neural training, empirical data/calibration, legacy Matlab reads, or Results/policy claims.

The old Python source repository remains read-only.

## Queued next gate — NOT ACTIVE

`DLH-2B — single-region Tier-0 HA/Aiyagari steady-state general equilibrium`.

It may only be issued after fresh independent review of DLH-2A.
