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

### Bootstrap

Issue #1 accepted and closed.

Accepted commit:

`bcded9b9137f3c10f71a7a6ecb929f78b40bdc11`

### DLH-0 / NSR-HANK scientific constitution

Issue #2 accepted and closed after R1 correction.

Acceptance classification:

`DLH_0_R1_NSR_HANK_SCIENTIFIC_CONSTITUTION_ACCEPTED`

Accepted R1 commit:

`73e1ae5db9d7e362781a77fa2a204c80238fad3e`

Authoritative roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_INITIAL_2026_08_19.md`

Accepted working scientific direction:

- working label `Network-Structured Regional HANK (NSR-HANK)`;
- province-local household / firm / HJB / KFE / accounting / clearing remain structural hard modules;
- first learned object = interpretable interregional labor-flow network `W^L`;
- `W^K` later; fiscal transfers remain a separate central-government allocation layer;
- household home-region identity fixed; labor services may move across provinces;
- Python is the main implementation language;
- existing single-province Python HJB/firm code is candidate reusable infrastructure subject to DLH-1B audit;
- Tier 0 one-region real HA/Aiyagari = computational benchmark only, not genuine HANK;
- Tier 1 = minimal genuine single-region HANK with NK nominal layer;
- Tier 2 = small multi-region NSR-HANK;
- cross-year model separates `Z_static`, time-varying node features, and time-varying pair features;
- network structural parameters are shared across years while `W^L_t` is year-varying;
- each year solves a separate conditional equilibrium `X*_t = T(X*_t; theta, Z_t)`;
- hold-out-year + hold-out-pair validation mandatory;
- learning sequence = flow-supervised pretraining -> GE embedding -> bounded equilibrium-constrained fine-tuning;
- GNN/message passing deferred.

Novelty remains unverified; E3 literature evidence is currently zero.

## Current active task

Issue #3 — `DLH-1A: Literature evidence and interprovincial labor-flow data feasibility`

Expected branch:

`dsh/issue-3-dlh-1a-literature-data-feasibility-2026-08-19`

DLH-1A goals:

1. establish the current literature boundary for NSR-HANK;
2. map Structural RL / DeepHAM / neural HJB / differentiable-equilibrium / spatial HA-HANK / learned-flow-network precedents;
3. assess Chinese interprovincial O-D-year labor-flow data feasibility;
4. assess static/time-varying feature feasibility;
5. build E0/E1/E2 evidence plus an E3 human-verification queue.

## Current scientific / implementation state

- master roadmap: `INITIAL_V0_1_PUBLISHED`；
- scientific constitution: `DLH_0_R1_ACCEPTED`；
- primary learned object: `W^L_FIRST_ACCEPTED_AT_SPEC_LEVEL`；
- model implementation: `NOT_STARTED`；
- code migration authority: `NONE`；
- Matlab execution authority: `NONE`；
- Python model execution authority: `NONE`；
- neural training authority: `NONE`；
- numerical Results authority: `NONE`；
- Results/manuscript claim authority: `NONE`；
- final novelty claim authority: `NONE`。

## Permanent read-only local reference roots

1. `D:\MatlabProgram\2023年12月2日 多省份神经网络HANK`
2. `D:\Zotero-Analytical-Workflow`

Issue #3 permits bounded read-only local Zotero-workflow text reconnaissance only as explicitly defined in the Issue. It authorizes zero legacy Matlab reads and zero source-root writes/copy-outs.

## Queued next gate — NOT ACTIVE

`DLH-1B — read-only audit of existing single-province Python HJB + firm kernel`.

It requires a separate GitHub Issue after DLH-1A review. No code migration is authorized yet.
