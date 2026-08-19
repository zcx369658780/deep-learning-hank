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

Status: accepted and closed.

Accepted commit:

`bcded9b9137f3c10f71a7a6ecb929f78b40bdc11`

### Issue #2 — DLH-0 / NSR-HANK scientific constitution

Status: accepted and closed after R1 correction.

Accepted R1 commit:

`73e1ae5db9d7e362781a77fa2a204c80238fad3e`

### Issue #3 — DLH-1A literature / labor-flow data feasibility

Status: accepted and closed after R1 evidence correction.

Acceptance classification:

`DLH_1A_R1_EVIDENCE_AND_DATA_FEASIBILITY_ACCEPTED`

Accepted R1 commit:

`e9aa7dc8a3f5a198b1655c917659f519239eb67b`

Accepted evidence conclusions:

- Owner prior dissertation / SSRN `6028234` is project provenance, not external precedent;
- no credible true annual bilateral O-D flow matrix is currently proven for direct `W^L_ij,t` supervision;
- CMDS is an annual repeated migrant cross-section and may support annual origin×destination migrant-stock/sample cross-tabs only after schema/weight/questionnaire harmonization verification;
- geodoi `Id=3621` is a provincial aggregate/model-derived proxy under current documentation, not a proven bilateral O-D-year matrix;
- E3 literature evidence remains 0 and final novelty claims remain unauthorized.

## Authoritative scientific direction

Roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_INITIAL_2026_08_19.md`

Accepted first-generation NSR-HANK direction remains:

- province-local household / firm / HJB / KFE / accounting / clearing = structural hard modules;
- first learned object = interpretable interregional labor-flow network `W^L`;
- `W^K` later; fiscal transfers remain a separate central-government allocation layer;
- household home-region identity fixed; labor services may move across provinces;
- Python main implementation language;
- Tier 0 = one-region real HA/Aiyagari computational benchmark only;
- Tier 1 = minimal genuine single-region HANK with NK nominal layer;
- Tier 2 = small multi-region NSR-HANK;
- shared cross-year network parameters + year-specific observables / `W^L_t` / equilibrium `X*_t`;
- flow-supervised pretraining -> GE embedding -> bounded equilibrium-constrained fine-tuning;
- GNN/message passing deferred.

## Current active task

Issue #4 — `DLH-1B: Read-only audit of existing single-province Python HJB + firm kernel`

Issue URL:

`https://github.com/zcx369658780/deep-learning-hank/issues/4`

Current substage:

`DLH-1B-R1 — audit terminology / evidence-strength correction`

Prior candidate:

`1d2f3b20fb44680afd93e19ff0aba231a7b47467`

Independent review found its branch/output/source-scope contract clean and independently confirmed its major source findings, but the audit terminology/evidence strength requires a bounded correction before acceptance.

Expected R1 branch:

`dsh/issue-4-dlh-1b-r1-audit-terminology-evidence-correction-2026-08-19`

Read-only candidate source repository:

`zcx369658780/dissertation-ch5-r5-python-model`

Fresh source `main` independently confirmed at review time:

`3039a145f43d419a08999c476cd0d97fd5f8341f`

### Independently confirmed source findings

- actual top-level model is frozen two-region symmetric, not a clean single-province solver;
- one liquid asset, two-state idiosyncratic productivity, CRRA, inelastic labor;
- HJB uses an upwind continuous-time finite-difference structure and constructs an **infinitesimal generator with row sums zero**;
- asset boundaries are handled as **state constraints / no outward drift**;
- KFE solves the stationary transpose-generator equation with normalization;
- firm block includes the legacy `alpha_g` / state-owned-services third factor;
- steady state uses two-region capital exposure `W` and symmetric `brentq` capital clearing;
- parameters are frozen by equality validation;
- source package self-identifies as an engineering scaffold without accepted economic solver/results authority.

### R1 correction requirements

1. Replace `row-stochastic generator` wording with `continuous-time infinitesimal generator / intensity matrix (off-diagonals >= 0; diagonal absorbs outflow; row sums = 0)`.
2. Replace `reflecting boundaries` with `state-constraint / no-outward-drift boundary treatment` unless later separately proven otherwise.
3. Weaken any unexecuted-validity language such as `algorithm correct` / `exact Tier-0 kernel` to candidate/source-compatibility language. Numerical convergence and scientific validity remain unaccepted until a later execution gate.

## Current scientific / implementation state

- master roadmap: `INITIAL_V0_1_PUBLISHED`；
- scientific constitution: `DLH_0_R1_ACCEPTED`；
- DLH-1A evidence/data feasibility: `ACCEPTED_WITH_DATA_BLOCKER_RECORDED`；
- DLH-1B audit: `R1_CORRECTION_ACTIVE_NOT_ACCEPTED`；
- primary learned object: `W^L_FIRST_ACCEPTED_AT_SPEC_LEVEL`；
- model implementation: `NOT_STARTED`；
- code migration authority: `NONE`；
- Python model/test execution authority: `NONE`；
- Matlab execution/read authority for current gate: `NONE`；
- neural training authority: `NONE`；
- numerical Results authority: `NONE`；
- Results/manuscript claim authority: `NONE`；
- final novelty claim authority: `NONE`。

## Read-only boundaries for current gate

Source repo `zcx369658780/dissertation-ch5-r5-python-model` must receive zero mutations.

Issue #4 R1 authorizes no code copy/migration, no test execution, no package install, no data operation, and no legacy Matlab reads.

## Queued next gate — NOT ACTIVE

`DLH-2 — Tier-0 single-region HA/Aiyagari computational benchmark`.

DLH-2 can only be issued after corrected DLH-1B is independently accepted and an exact implementation/migration allowlist is authorized.