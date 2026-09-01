# Deep Learning + HANK Task Index

Status: `ACTIVE_BUILDER_ISSUE__DLH_5E_CONSERVATIVE_STATIONARY_KFE_VALIDATION`

Last synchronized: 2026-09-01

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

Current Issue:

**Issue #28 — OPEN**

Title:

`DLH-5E: Implement conservative stationary-KFE validator and test canonical boundary-policy gate`

Task type:

`SCIENTIFIC_IMPLEMENTATION_VALIDATION__CONSERVATIVE_STATIONARY_KFE_CANDIDATE`

Issue #28 is the sole DSH Builder authority only after the authoritative activation comment is present.

DSH must fresh-fetch `origin/main`, read all CURRENT rules, this Task Index, the CURRENT Startup Snapshot, Issue #28 latest body/comments, accepted Issue #27 contract/audit, accepted Issues #23-#26 evidence, and the canonical MATLAB-faithful household/HJB source before any mutation.

If Issue #28 is not open, activation is absent, or Issue/Task Index/Startup identity differs, DSH must fail closed.

Dedicated Builder branch after activation:

`dsh/issue-28-dlh-5e-conservative-kfe-validation-2026-09-01`

## Issue #28 scientific scope

DLH-5E is a bounded **implementation-validation candidate gate**, not production integration.

It must preserve the accepted MATLAB-faithful HJB/parity source and build a conservative stationary-KFE candidate alongside it.

Controlling scientific contract:

`docs/specifications/DLH_5D_CONSERVATIVE_STATIONARY_KFE_BOUNDARY_AND_CONTAMINATION_CONTRACT_2026_09_01.md`

Controlling provenance audit:

`docs/audits/DLH_5D_MATLAB_KFE_CONTAMINATION_AND_BOUNDARY_PROVENANCE_AUDIT_2026_09_01.md`

Binding sequence:

1. run the exact accepted canonical D0 HJB state;
2. reconstruct requested directional rates from accepted post-convergence `mu_b/mu_a`;
3. report requested outward rates at all four asset boundaries;
4. mechanically assemble a conservative no-outflow candidate generator using only admitted in-grid transitions;
5. if requested outward boundary rate exceeds `1e-10`, classify `BOUNDARY_POLICY_VIOLATION`, reproduce it once, persist evidence, and STOP before scientific KFE/aggregate acceptance;
6. only if D0 boundary policy passes, validate generator conservation, unique stationary structure, MATLAB-style contamination with pin admissibility/original residual, then recompute D0 household aggregates and candidate anchor;
7. only after full D0 success, run exact D1-D3 regression and deterministic repeat;
8. no regional outer fixed point is authorized.

## Issue #28 exact allowlist

Builder may create only:

1. `src/deep_learning_hank/two_asset/conservative_stationary_kfe.py`
2. `configs/dlh_5e_conservative_stationary_kfe_validation.toml`
3. `tests/test_dlh_5e_conservative_stationary_kfe.py`
4. `reports/dlh_5e_conservative_stationary_kfe_validation_2026_09_01/` with the exact evidence files listed in Issue #28.

No existing file may be modified by Builder under Issue #28.

In particular, Builder must not modify:

- `src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`;
- any existing HJB/local-policy code;
- regional fixed-point code/config;
- accepted Issue #27 specification/audit;
- prior evidence roots.

## Latest accepted task

Issue #27 — DLH-5D — ACCEPTED / COMPLETED

Accepted candidate integrated to `main`:

`f52b1fbf0cd5c921f73212ea97b494fa102e3de5`

Accepted classification:

`DLH_5D_CONSERVATIVE_STATIONARY_KFE_AND_MATLAB_CONTAMINATION_CONTRACT_ACCEPTED`

Acceptance level:

`L3_COMMIT_OR_PR_VERIFIED__SCIENTIFIC_DESIGN_CONTRACT_ACCEPTED`

Accepted DLH-5D contract:

- singular `Q` is expected and not itself failure;
- scientific stationary equation is ORIGINAL `Q^T g = 0` plus `cell_weight=db*da` mass normalization and non-negativity;
- MATLAB-style contamination remains authorized as a numerical normalization device;
- contaminated residual is insufficient; ORIGINAL residual is binding;
- stationary uniqueness, pin admissibility and pin invariance are distinct;
- component pin `g_n=c>0` is admissible only when stationary support at `n` is nonzero;
- deterministic pins must be classified as valid / zero-support-inadmissible / unresolved numerical failure;
- only valid pins enter invariance comparison; at least two valid pins are required on the canonical fixture;
- default MATLAB parity pin `floor(0.37*N)-1` must itself be valid before future production use;
- conservative generator rows sum to zero and omitted outward transitions cannot retain diagonal exit rates;
- material requested outward policy is `BOUNDARY_POLICY_VIOLATION` and cannot be silently clipped into PASS;
- canonical fixture target is stationary nullspace dimension 1, with nullity 1 explicitly not equivalent to full support;
- exact tolerances and household/anchor revalidation order are frozen.

## Earlier accepted foundation

- Issue #26 / DLH-5C: fixed-row artifact diagnosis accepted; current row-295 KFE-dependent aggregates are not validated stationary-equilibrium quantities.
- Issue #25 / DLH-5B: two-region synchronous/Jacobi architecture accepted for wiring/accounting/trace semantics; KFE-dependent aggregates/anchor require revalidation.
- Issue #24 / DLH-5A: network-ready two-region real structural contract accepted.
- Issue #23: MATLAB-faithful two-asset HJB / transfer-FOC parity repair accepted; the faithful source remains immutable in DLH-5E.

## Current scientific route

1. accepted two-asset HJB/HA foundation;
2. accepted two-region structural contract and architecture;
3. accepted KFE blocker diagnosis;
4. accepted conservative KFE / contamination scientific contract;
5. **current DLH-5E: implement and validate a conservative stationary-KFE candidate, with D0 boundary-policy gate first**;
6. if DLH-5E passes, separately authorize production household integration and two-region S0/S1 revalidation;
7. if DLH-5E blocks on boundary policy, stop for Owner scientific decision on HJB state-constraint/boundary-policy redesign;
8. only after trusted household/KFE + two-region revalidation resume OD / learned `W^L` / larger-region / nominal-HANK tracks.

## Scientific ceiling during Issue #28

No production integration, no HJB/local-policy mutation, no regional outer iteration, no automatic grid expansion, no parameter retuning, no alternative production pin selection, no data/network training, no larger-region scaling, no nominal HANK, no calibration, no policy/welfare/Results.