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
- direct true annual bilateral O-D labor-flow labels for `W^L_ij,t` remain unresolved;
- CMDS remains a repeated migrant cross-section / possible O-D stock source pending schema/weight harmonization;
- E3 literature evidence remains zero; final novelty claims remain unauthorized.

### Issue #4 — DLH-1B Python kernel read-only audit
Accepted and closed after R2 at `8dce318af5ca704a747e67932ec3caa35f9168ad`.

Accepted source identity:
`zcx369658780/dissertation-ch5-r5-python-model` @ `3039a145f43d419a08999c476cd0d97fd5f8341f`.

Accepted audit conclusions:
- old source top level = frozen two-region capital-exposure scaffold, not clean single-region solver;
- Tier-0 candidate household = one liquid asset, finite-state productivity, CRRA, inelastic labor;
- HJB contract = upwind continuous-time finite differences + state-constraint/no-outward-drift boundary + CTMC infinitesimal generator;
- KFE contract = stationary `G.T g = 0` + mass/non-negativity/diagnostic checks;
- Tier-0 excludes old `W`, open-economy accounts, SOE third factor, nominal placeholder, shocks and transition.

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

Current substage:

`DLH-2A-R1 — evidence/provenance and off-diagonal diagnostic correction`

Prior candidate:
`2a2534d0660e433bbe48b5576dba18c8df83c9c4`.

Independent review classification:

`DLH_2A_CORE_NUMERICAL_GATE_PASS__EVIDENCE_AND_DIAGNOSTIC_R1_REQUIRED`

### What independently passed in the prior candidate

- geometry = one commit / 21 allowlisted paths / no PR;
- source repo remained at audited SHA `3039a145...`;
- one-asset finite-z CRRA/inelastic-labor household implementation stayed inside Tier-0 scope;
- HJB generator/boundary mathematics matched the accepted contract;
- fixed-price HJB residual `8.335084289434747e-08 <= 1e-7`;
- positive consumption and state-constraint boundary gates passed;
- KFE mass error `0`, stationarity residual `3.69712940817557e-17`, non-negative distribution, state marginals `[0.5,0.5]`;
- deterministic repeat differences were all `0.0`;
- fixture was explicitly `VALIDATION_FIXTURE_NOT_CALIBRATION`;
- D2 evidence only; no calibration/HANK/regional/Results authority.

### Why R1 is required before acceptance

1. Original execution report test-file breakdown is inconsistent with the candidate tests: actual original suite = `7 economics + 7 HJB/KFE + 1 reproducibility = 15`, not `7 + 8 + 1`.
2. Source-provenance CSV labels 40-character Git blob OIDs as `source_blob_sha256`; this must be corrected.
3. Exact diagnostics-capture command was replaced by placeholder `python -c "..."`; R1 must record exact reproducible commands and preserve original-run vs R1-rerun history.
4. `generator_min_off_diagonal` currently takes the minimum over stored nonzero sparse off-diagonal entries. Issue #5 requires the literal minimum over all off-diagonal entries, including implicit zero entries. R1 must correct this diagnostic semantics and rerun the full suite without changing thresholds.
5. Remove unsupported byte-level statement `no code copied verbatim`; retain the supportable no-wholesale-copy + ADAPTED/REIMPLEMENTED provenance statement.

Expected R1 branch:
`dsh/issue-5-dlh-2a-r1-evidence-diagnostic-correction-2026-08-19`.

## Current scientific / implementation state

- master roadmap: `INITIAL_V0_1_PUBLISHED`；
- scientific constitution: `DLH_0_R1_ACCEPTED`；
- DLH-1A evidence/data feasibility: `ACCEPTED_WITH_DATA_BLOCKER_RECORDED`；
- DLH-1B source audit: `R2_ACCEPTED`；
- DLH-2A core fixed-price numerical gate: `SUBSTANTIVE_D2_PASS_PENDING_R1_CANONICAL_EVIDENCE_CORRECTION`；
- DLH-2A merge/acceptance: `NOT_YET_AUTHORIZED`；
- outer steady-state GE authority: `NONE`；
- regional/W authority: `NONE`；
- nominal/genuine-HANK implementation authority: `NONE`；
- shock/transition authority: `NONE`；
- neural training authority: `NONE`；
- numerical Results/manuscript authority: `NONE`；
- final novelty claim authority: `NONE`。

## Current boundaries

Issue #5 R1 remains within the original 21-path allowlist and does not authorize DLH-2B or any scientific expansion. The source repository remains read-only. Original numerical thresholds are frozen and may not be relaxed by Builder.

## Queued next gate — NOT ACTIVE

`DLH-2B — single-region Tier-0 HA/Aiyagari steady-state general equilibrium`.

It may only be issued after fresh independent review and acceptance of corrected DLH-2A-R1.