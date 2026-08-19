# Deep Learning + HANK Task Index

Status: `ACTIVE_GITHUB_ISSUE_5_DLH_2A_R1`

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

### Issue #4 — DLH-1B Python kernel read-only audit
Status: `DLH_1B_R2_PYTHON_KERNEL_READONLY_AUDIT_ACCEPTED_AND_CLOSED`
Accepted commit: `8dce318af5ca704a747e67932ec3caa35f9168ad`
Accepted source repo: `zcx369658780/dissertation-ch5-r5-python-model` @ `3039a145f43d419a08999c476cd0d97fd5f8341f`.

Authoritative roadmap:
`docs/roadmaps/DLH_MASTER_ROADMAP_INITIAL_2026_08_19.md`

## Sole active Builder authority

GitHub Issue #5:

`DLH-2A: Tier-0 kernel migration and fixed-price HJB/KFE validation`

Issue URL:
`https://github.com/zcx369658780/deep-learning-hank/issues/5`

Builder: DSH

Current substage:

`DLH-2A-R1 — evidence/provenance and off-diagonal diagnostic correction`

Prior candidate:

`2a2534d0660e433bbe48b5576dba18c8df83c9c4`

Independent review disposition:

`DLH_2A_CORE_NUMERICAL_GATE_PASS__EVIDENCE_AND_DIAGNOSTIC_R1_REQUIRED`

The prior candidate's core fixed-price HJB/KFE numerics and Issue #5 thresholds were independently reviewed as substantively PASS at D2 level, but the candidate is NOT accepted/merged until the bounded R1 correction is completed.

Expected R1 dedicated branch:

`dsh/issue-5-dlh-2a-r1-evidence-diagnostic-correction-2026-08-19`

## R1 correction requirements

Preserve the accepted core implementation/economics and all original Issue #5 thresholds. Correct only the following bounded items under the latest authoritative ChatGPT comment on Issue #5:

1. Test-count evidence: canonical breakdown must reflect the actual candidate files (`7` economics + `7` HJB/KFE + `1` reproducibility = `15` total for the original suite).
2. Source-provenance schema: 40-character Git blob object IDs must not be labeled `sha256`; use an accurate blob-OID field name or add actual SHA-256 separately.
3. Exact command provenance: replace placeholder `python -c "..."` with the full exact R1 execution/diagnostics command(s); preserve history of the original first run and the R1 rerun.
4. Off-diagonal diagnostic semantics: `generator_min_off_diagonal` must represent the literal minimum over all off-diagonal matrix entries, including implicit sparse zeros. Keep threshold `>= -1e-14`; rerun full DLH-2A tests/diagnostics after the bounded correction.
5. Remove unsupported byte-level claim `no code copied verbatim`; retain only the supported statement that no wholesale old-package copy occurred and all adapted/reimplemented logic is provenance-mapped.

## Scope boundary

DLH-2A-R1 remains inside Issue #5 only. It does NOT authorize:
- outer single-region GE/capital root (future DLH-2B);
- regional / `W^L` / `W^K` / old `W` code;
- SOE third factor or RegionalAccounts;
- nominal/NK block;
- shocks/AR(1) or transition;
- neural/RL work;
- data/calibration/Results claims;
- Matlab/legacy Matlab access;
- source-repo mutation;
- PR/merge/Issue-close/successor/self-accept by Builder.

## Queued next gate — NOT ACTIVE

`DLH-2B — single-region Tier-0 HA/Aiyagari steady-state general equilibrium`.

DLH-2B may only be issued after corrected DLH-2A-R1 is independently reviewed and accepted.