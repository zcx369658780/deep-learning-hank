# Deep Learning + HANK Task Index

Status: `ACTIVE_BUILDER_ISSUE__DLH_5C_KFE_SINGULARITY_DIAGNOSTIC`

Last synchronized: 2026-08-31

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

Current Issue:

**Issue #26 — OPEN**

Title:

`DLH-5C: Diagnose stationary KFE contaminated-row singularity on the preserved two-region perturbed path`

Task type:

`SCIENTIFIC_DIAGNOSTIC__STATIONARY_KFE_SINGULARITY_ON_REGIONAL_PATH`

Issue #26 is the sole DSH Builder authority only after the authoritative activation comment is present.

DSH must fresh-fetch `origin/main`, read all CURRENT rules, this Task Index, the CURRENT Startup Snapshot, Issue #26 latest body/comments, accepted DLH-5A contract, accepted DLH-5B implementation/evidence, and the canonical household KFE source before any mutation.

If Issue #26 is not open, activation is absent, or Issue/Task Index/Startup identity differs, DSH must fail closed.

## Issue #26 scientific scope

DLH-5C is a diagnostic-only gate for the exact reproducible KFE blocker discovered in accepted Issue #25.

It must diagnose why the accepted MATLAB-faithful stationary KFE contaminated-row solve becomes non-finite at the preserved region-0 S1 turn-4 household state while neighboring/anchor states remain finite.

Frozen cases:

- D0 anchor: `wbar=1.0`, `r_a=0.03`;
- D1 last valid region-0 state: `wbar=0.9977278388290097`, `r_a=0.0299127630152404`;
- D2 exact failing region-0 state: `wbar=0.998807521160338`, `r_a=0.029964194758276677`;
- D3 same-turn valid region-1 control: `wbar=1.0011941548981047`, `r_a=0.03003565330704072`;
- exact 9-point linear scan D1->D2, no adaptive refinement.

Required diagnostics include operator/rank/row-sum structure, positive-transition SCC/closed-class structure, accepted contaminated-row location, deterministic alternative row-pin diagnostics, bounded sparse singular-value diagnostics, and full reproducibility.

Issue #26 is NOT repair authority. No existing production/model/solver/config/test/report file may be modified. Only the new diagnostic script/config/test/report-root allowlist in Issue #26 may be created.

Dedicated Builder branch after activation:

`dsh/issue-26-dlh-5c-kfe-singularity-diagnostic-2026-08-31`

## Latest accepted task

Issue #25 — ACCEPTED / COMPLETED

Title:

`DLH-5B: Implement and validate deterministic two-region hand-specified-flow outer fixed point`

Accepted candidate merged to `main`:

`4c97ae30d98c40466af3ff11ce8048e5e5087335`

Accepted reviewer classification:

`DLH_5B_TWO_REGION_ARCHITECTURE_ACCEPTED__PERTURBED_FIXED_POINT_BLOCKED_BY_REPRODUCIBLE_HOUSEHOLD_KFE_SINGULARITY`

Acceptance level:

`L3_COMMIT_OR_PR_VERIFIED`

Accepted positive scientific meaning:

- deterministic two-region synchronous/Jacobi architecture is implemented and accepted for the frozen prototype;
- S0 anchor map closes at machine precision (`R_w=2.220e-16`, `R_ra=6.939e-18`);
- accounting/network/wage-bill/KFE/firm gates pass at the anchor;
- S2 region-order invariance is exact (`0.0`);
- R1 repaired S1 validity enforcement, trace completeness, non-finite-aware reproducibility comparison and fail-closed terminal classification;
- predecessor vs R1 scientific outputs are unchanged on common fields.

Preserved negative evidence:

- S1 does not establish a converged perturbed two-region fixed point;
- after three valid, residual-reducing turns, region 0 fail-closes deterministically on the accepted stationary KFE contaminated-row solve;
- `a_max` boundary mass near `0.196` remains a non-blocking architecture-stage warning;
- no empirical calibration, learned network, nominal HANK, policy/welfare or paper Results authority is established.

Accepted evidence roots:

- `reports/dlh_5b_two_region_fixed_point_2026_08_31/`
- `reports/dlh_5b_two_region_fixed_point_r1_2026_08_31/`

## Accepted structural foundation

Issue #24 / DLH-5A accepted the network-ready two-region real structural contract.

Canonical household source remains:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Accepted household blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Old `B_hh=B_gov=1` / nested-Brent GE closure remains superseded.

## Current scientific route

Working label: `Network-Structured Regional HANK (NSR-HANK)`.

Current order:

1. accepted two-asset HA foundation;
2. accepted two-region structural contract;
3. accepted two-region architecture implementation with preserved KFE blocker;
4. **current DLH-5C: diagnose the exact stationary KFE singularity before any solver redesign or larger-network stage**;
5. after independent review, decide whether a bounded KFE numerical repair requires Owner scientific authority;
6. only after the regional fixed-point path is numerically trustworthy, proceed to OD-year labor-flow schema / transparent baseline / learned `W^L`;
7. later 3–5 regions, genuine nominal HANK, `W^K`, equilibrium-constrained calibration, 31-region panel and policy/welfare gates.

## Scientific ceiling during Issue #26

DLH-5C may classify the KFE blocker and establish diagnostic evidence only.

It does not authorize a solver repair, household redesign, converged perturbed equilibrium claim, learned network, empirical calibration, nominal regional HANK, 31-region scaling, policy/welfare or Results claims.
