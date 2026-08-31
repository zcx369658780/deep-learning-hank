# Deep Learning + HANK Task Index

Status: `ACTIVE_BUILDER_ISSUE__DLH_5D_KFE_BOUNDARY_CONTAMINATION_CONTRACT`

Last synchronized: 2026-09-01

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

Current Issue:

**Issue #27 — OPEN**

Title:

`DLH-5D: Freeze conservative stationary-KFE boundary law and MATLAB-style contamination contract`

Task type:

`SCIENTIFIC_DESIGN__STATIONARY_KFE_BOUNDARY_AND_CONTAMINATION_CONTRACT`

Issue #27 is the sole DSH Builder authority only after the authoritative activation comment is present.

DSH must fresh-fetch `origin/main`, read all CURRENT rules, this Task Index, the CURRENT Startup Snapshot, Issue #27 latest body/comments, accepted Issues #23-#26 evidence, the canonical household HJB/KFE source, and the authorized read-only MATLAB source before any mutation.

If Issue #27 is not open, activation is absent, or Issue/Task Index/Startup identity differs, DSH must fail closed.

Dedicated Builder branch after activation:

`dsh/issue-27-dlh-5d-kfe-boundary-contamination-contract-2026-09-01`

## Issue #27 scientific scope

DLH-5D is a **design/provenance-only gate**. It freezes the scientific contract for the stationary KFE before any repair implementation.

Owner clarification now binding:

- the KFE generator `Q` is expected to be singular;
- singularity of `Q` is not a failure;
- MATLAB-style row contamination / equation replacement is a legitimate numerical normalization method in principle;
- the contaminated solution is scientifically accepted only if the normalized density also satisfies the ORIGINAL equation `Q^T g = 0`;
- the future solver must demonstrate bounded pin-row invariance rather than privilege an arbitrary row;
- the finite-grid generator must conserve mass and obey a no-outward-flux boundary law;
- materially requested outward boundary drift/rate must be exposed as a scientific boundary-policy violation, not silently hidden by clipping.

Issue #27 freezes equations, boundary law, contamination semantics, tolerances, MATLAB provenance and future revalidation order. It does **not** authorize source-code changes or experiment execution.

Builder may add only:

1. `docs/specifications/DLH_5D_CONSERVATIVE_STATIONARY_KFE_BOUNDARY_AND_CONTAMINATION_CONTRACT_2026_09_01.md`
2. `docs/audits/DLH_5D_MATLAB_KFE_CONTAMINATION_AND_BOUNDARY_PROVENANCE_AUDIT_2026_09_01.md`

No existing file may be modified by DSH under Issue #27.

## Latest accepted task

Issue #26 — DLH-5C — ACCEPTED / COMPLETED

Accepted candidate integrated to `main`:

`c6b773323fa4d7fe480f4ae8a1523bcb97d8113c`

Accepted classification:

`DLH_5C_KFE_SINGULARITY_DIAGNOSTIC_ACCEPTED__FIXED_ROW_SELECTION_ARTIFACT_PRIMARY__OWNER_KFE_REDESIGN_DECISION_REQUIRED`

Acceptance level:

`L3_COMMIT_OR_PR_VERIFIED`

Scientific evidence level:

`D2_MACHINE_NUMERICAL_DIAGNOSTIC__NO_STRONG_ECONOMIC_RESULTS_CLAIM`

Accepted DLH-5C findings relevant to DLH-5D:

- current fixed row 295 can produce finite contaminated-system solutions that fail the ORIGINAL stationary equation at D0/D1/D3;
- at D2 the same pinned system is exactly singular/non-finite;
- pins 0/400 recover the same normalized near-null density on the frozen fixture;
- corrected transition orientation is `row -> col`;
- the current post-convergence operator has upper-boundary leakage because outward destinations can be omitted while diagonal rates remain;
- one near-null direction is supported mainly on the conservative `a=0` class;
- Issue #25 remains accepted for architecture/wiring/Jacobi/accounting/trace semantics only; its KFE-dependent aggregates/firm anchor are scientifically qualified pending KFE redesign.

## Earlier accepted foundation

- Issue #25 / DLH-5B: two-region synchronous/Jacobi architecture accepted; KFE-dependent aggregates/anchor require revalidation.
- Issue #24 / DLH-5A: network-ready two-region real structural contract accepted.
- Issue #23: MATLAB-faithful two-asset HJB / transfer-FOC parity repair accepted; current stationary KFE code remains authority only until superseded by a new accepted contract/implementation.

## Current scientific route

1. accepted two-asset HJB/HA foundation;
2. accepted two-region structural contract and architecture;
3. accepted KFE blocker diagnosis;
4. **current DLH-5D: freeze conservative stationary-KFE boundary + MATLAB contamination scientific contract**;
5. successor implementation/validation only after DLH-5D acceptance;
6. recompute household aggregates and revalidate `K_i=M_i*A_i` / firm anchor;
7. only then resume perturbed two-region equilibrium and later OD / learned `W^L` / larger-region / nominal-HANK tracks.

## Scientific ceiling during Issue #27

No implementation, no solver repair, no new KFE run, no two-region run, no data/network training, no larger-region scaling, no nominal HANK, no calibration, no policy/welfare/Results.
