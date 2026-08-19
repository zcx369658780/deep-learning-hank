# Deep Learning + HANK Task Index

Status: `ACTIVE_GITHUB_ISSUE_4_DLH_1B_R1`

## Accepted predecessors

### Issue #1 — local/GitHub bootstrap

Status: `ACCEPTED_AND_CLOSED`

Accepted commit:

`bcded9b9137f3c10f71a7a6ecb929f78b40bdc11`

### Issue #2 — DLH-0 / NSR-HANK scientific constitution

Status: `DLH_0_R1_NSR_HANK_SCIENTIFIC_CONSTITUTION_ACCEPTED_AND_CLOSED`

Accepted commit:

`73e1ae5db9d7e362781a77fa2a204c80238fad3e`

### Issue #3 — DLH-1A literature / labor-flow data feasibility

Status: `DLH_1A_R1_EVIDENCE_AND_DATA_FEASIBILITY_ACCEPTED_AND_CLOSED`

Accepted commit:

`e9aa7dc8a3f5a198b1655c917659f519239eb67b`

Accepted evidence conclusion:

- SSRN `6028234` = Owner prior work / project provenance, not external precedent;
- direct true annual bilateral O-D flow labels for `W^L_ij,t` remain `UNRESOLVED`;
- CMDS = annual repeated migrant cross-section / possible O-D stock source pending schema verification;
- geodoi `Id=3621` = provincial aggregate/model-derived proxy, not proven bilateral O-D-year matrix;
- E3 literature evidence remains 0; novelty claims remain blocked.

Authoritative roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_INITIAL_2026_08_19.md`

## Sole active Builder authority

GitHub Issue #4:

`DLH-1B: Read-only audit of existing single-province Python HJB + firm kernel`

Issue URL:

`https://github.com/zcx369658780/deep-learning-hank/issues/4`

Builder: DSH

Current substage:

`DLH-1B-R1 — audit terminology / evidence-strength correction`

Prior candidate:

`1d2f3b20fb44680afd93e19ff0aba231a7b47467`

Process/geometry/source-scope review: PASS. Audit packet: NOT ACCEPTED / bounded R1 correction required.

Expected R1 dedicated branch:

`dsh/issue-4-dlh-1b-r1-audit-terminology-evidence-correction-2026-08-19`

Read-only candidate source repository:

`zcx369658780/dissertation-ch5-r5-python-model`

Fresh source `main` independently confirmed at review time:

`3039a145f43d419a08999c476cd0d97fd5f8341f`

## Material correction requirements entering R1

- household policy matrix must be described as a continuous-time infinitesimal generator / intensity matrix with nonnegative off-diagonals and **row sums = 0**, not a row-stochastic matrix;
- HJB asset-boundary handling must be described as **state-constraint / no-outward-drift** treatment, not reflecting boundaries;
- reuse rationale must remain source-audit/candidate language and must not call an unexecuted algorithm `correct` or scientifically validated;
- prior candidate remains provenance only and must not be merged as-is.

## Scope boundary

DLH-1B-R1 is documentation/audit correction only.

It does **not** authorize:

- source-repository mutation;
- code copy/migration into `deep-learning-hank`;
- Python/model/test execution;
- package/environment mutation;
- Matlab/Octave/Dynare reads or execution;
- neural training/inference;
- data purchase/download/analysis;
- calibration;
- Results/policy claims;
- final novelty claims;
- PR/merge/Issue-close/successor/self-accept by Builder.

## Queued next gate — NOT ACTIVE

`DLH-2 — Tier-0 single-region HA/Aiyagari computational benchmark`.

DLH-2 may only be issued after corrected DLH-1B is independently accepted and an exact migration/implementation allowlist is authorized.