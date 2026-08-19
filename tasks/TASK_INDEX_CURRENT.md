# Deep Learning + HANK Task Index

Status: `ACTIVE_GITHUB_ISSUE_5_DLH_2A`

## Accepted predecessors

### Issue #1 — local/GitHub bootstrap
Status: `ACCEPTED_AND_CLOSED`
Accepted commit: `bcded9b9137f3c10f71a7a6ecb929f78b40bdc11`

### Issue #2 — DLH-0 / NSR-HANK scientific constitution
Status: `DLH_0_R1_NSR_HANK_SCIENTIFIC_CONSTITUTION_ACCEPTED_AND_CLOSED`
Accepted commit: `73e1ae5db9d7e362781a77fa2a204c80238fad3e`

### Issue #3 — DLH-1A literature / labor-flow data feasibility
Status: `DLH_1A_R1_EVIDENCE_AND_DATA_FEASIBILITY_ACCEPTED_AND_CLOSED`
Accepted commit: `e9aa7dc8a3f5a198b1655c917659f519239eb67b`

Accepted evidence conclusion:
- Owner prior work is project provenance, not external novelty evidence;
- true annual bilateral O-D labor-flow labels for direct `W^L_ij,t` supervision remain unresolved;
- CMDS is a repeated migrant cross-section / possible O-D stock source pending schema verification;
- geodoi `Id=3621` is aggregate/model-derived proxy under current evidence;
- E3 literature evidence remains zero and final novelty claims remain blocked.

### Issue #4 — DLH-1B Python kernel read-only audit
Status: `DLH_1B_R2_PYTHON_KERNEL_READONLY_AUDIT_ACCEPTED_AND_CLOSED`
Accepted commit: `8dce318af5ca704a747e67932ec3caa35f9168ad`

Accepted audit conclusions:
- source repo: `zcx369658780/dissertation-ch5-r5-python-model` @ `3039a145f43d419a08999c476cd0d97fd5f8341f`;
- source top-level model is a frozen 2-region capital-exposure scaffold, not a clean single-region model;
- CTMC household generator has nonnegative off-diagonals, diagonal equal to negative outflow, rows sum to zero;
- asset boundary treatment = state-constraint / no-outward-drift;
- Tier-0 candidate inputs: grids/io patterns, household HJB, stationary KFE, two-factor production core, minimal lump-sum fiscal;
- Tier-0 excludes old `W`, RegionalAccounts, SOE third factor, nominal placeholder, shocks and transition;
- numerical convergence/scientific validity remain unverified until execution.

Authoritative roadmap:
`docs/roadmaps/DLH_MASTER_ROADMAP_INITIAL_2026_08_19.md`

## Sole active Builder authority

GitHub Issue #5:

`DLH-2A: Tier-0 kernel migration and fixed-price HJB/KFE validation`

Issue URL:
`https://github.com/zcx369658780/deep-learning-hank/issues/5`

Builder: DSH

Expected dedicated branch:
`dsh/issue-5-dlh-2a-tier0-kernel-validation-2026-08-19`

## Current gate purpose

DLH-2A is the first implementation + numerical-execution subgate inside DLH-2.

It authorizes only:
- clean-slate/adapted Tier-0 package scaffolding within the Issue #5 21-path allowlist;
- one-asset, finite-z, CRRA, inelastic-labor household HJB;
- stationary KFE;
- two-factor firm and minimal fiscal unit-level tests;
- fixed-price validation fixture explicitly labeled `VALIDATION_FIXTURE_NOT_CALIBRATION`;
- HJB/KFE numerical diagnostics and deterministic repeat validation;
- minimal task-local Python environment if needed.

It does **not** authorize:
- single-region outer capital-market root / full steady-state GE (future DLH-2B);
- any regional/W code;
- nominal/NK block;
- shocks/AR(1) or transition;
- neural/RL training;
- data/calibration/Results claims.

## Queued next gate — NOT ACTIVE

`DLH-2B — single-region Tier-0 HA/Aiyagari steady-state general equilibrium`.

DLH-2B may only be issued after DLH-2A is independently reviewed and the fixed-price HJB/KFE kernel passes or receives an explicit reviewer disposition.
