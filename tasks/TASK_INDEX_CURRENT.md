# Deep Learning + HANK Task Index

Status: `ACTIVE_BUILDER_ISSUE__DLH_5B_TWO_REGION_FIXED_POINT`

Last synchronized: 2026-08-31

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

Current Issue:

**Issue #25 — OPEN**

Title:

`DLH-5B: Implement and validate deterministic two-region hand-specified-flow outer fixed point`

Task type:

`SCIENTIFIC_IMPLEMENTATION__TWO_REGION_HAND_SPECIFIED_FIXED_POINT_PROTOTYPE`

Issue #25 is the sole DSH Builder authority **only after** the authoritative activation comment is present.

DSH must fresh-fetch `origin/main`, read all CURRENT rules, this Task Index, the CURRENT Startup Snapshot, the accepted DLH-5A contract/audit, and the latest Issue #25 body/comments before mutation.

If Issue #25 is not open, activation is absent, or Issue/Task Index/Startup identity differs, DSH must fail closed.

## Issue #25 scientific scope

DLH-5B implements the accepted DLH-5A two-region real structural HA-GE outer-fixed-point contract on one exact deterministic exploratory fixture.

Frozen core:

- accepted two-asset household oracle remains immutable;
- `K_i=M_i*A_i` provisional private-capital closure;
- `B_i` diagnostic only; no fixed-bond/root closure;
- hand-specified labor network `P^L=[[0.9,0.1],[0.1,0.9]]` from `m_1=m_2=0.10`;
- synchronous/Jacobi old-state semantics;
- common `r_b=0.015`, regional `tau_i=0.15`, `T_i=0`, `rb_gap_i=0.01`;
- both region masses `M_i=1`;
- exact accepted household grid/parameters/numerics from `tests/test_dlh_4b_transfer.py` (`VALIDATION_FIXTURE_NOT_CALIBRATION`);
- deterministic firm anchor at `w*=1`, `r_a*=0.03`, `alpha=1/3`, with `Z*` and `delta*` derived once from accepted anchor household aggregates and then frozen;
- S0 exact-anchor one-turn smoke;
- S1 small asymmetric fixed-point run with `lambda=0.5`, `tol_w=tol_ra=1e-6`, `max_iter=25`;
- S2 explicit region-order invariance;
- no automatic retry, adaptive tuning or grid expansion;
- output no-overwrite and deterministic reproducibility gates.

Issue #25 may create/modify only its explicit implementation/config/test/report allowlist. It does not authorize changes to the accepted household oracle, existing single-region GE code, historical outputs, roadmap/governance, neural training, `W^K`, `GovInv`, nominal HANK, 31-region scaling, policy/welfare or Results.

Dedicated Builder branch after activation:

`dsh/issue-25-dlh-5b-two-region-fixed-point-prototype-2026-08-31`

## Latest accepted task

Issue #24 — ACCEPTED / COMPLETED

Title:

`DLH-5A: Freeze network-ready two-region structural and outer-fixed-point contract`

Accepted candidate merged to `main`:

`820f23375377b21561d261c0850917056dec15c2`

Accepted reviewer classification:

`DLH_5A_NETWORK_READY_TWO_REGION_STRUCTURAL_CONTRACT_ACCEPTED`

Acceptance level:

`L3_COMMIT_VERIFIED__SCIENTIFIC_DESIGN_CONTRACT_ACCEPTED`

Accepted artifacts:

- `docs/specifications/DLH_5A_NETWORK_READY_TWO_REGION_STRUCTURAL_AND_OUTER_FIXED_POINT_CONTRACT_2026_08_31.md`
- `docs/audits/DLH_5A_HISTORICAL_MATLAB_PROVENANCE_AND_REPLACEMENT_BOUNDARY_2026_08_31.md`

## Accepted household foundation

Issue #23 accepted commit:

`b038db800da3760cebee484b1c7a76bf7c1529d0`

Post-repair household identity:

- blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`
- SHA-256 `1795718C469FC3B427CAB8E3D5957C133BEAD6EACC9EF0A25A3EDB7211D1A024`

Old `B_hh=B_gov=1` / nested-Brent Phase-E route remains superseded and must not be resumed.

## Current scientific route

Working label: `Network-Structured Regional HANK (NSR-HANK)`.

Current order:

1. accepted two-asset HA foundation;
2. accepted two-region structural contract;
3. **current DLH-5B deterministic two-region implementation/validation**;
4. OD-year labor-flow schema + transparent baseline;
5. learned `W^L`;
6. 3–5 region equilibrium embedding;
7. separately validated genuine nominal HANK block;
8. learned `W^K` later;
9. equilibrium-constrained calibration / regional parameter mapping;
10. 31-region panel and automated pipeline;
11. policy/welfare only after all gates.

## Scientific ceiling during Issue #25

DLH-5B may establish only a deterministic hand-specified-flow two-region **real structural HA-GE outer-fixed-point prototype**, including positive convergence or preserved deterministic nonconvergence evidence, conservation/accounting validity, reproducibility, and region-order invariance.

It does not establish learned networks, empirical calibration, genuine nominal regional HANK, 31-region results, policy/welfare or paper Results authority.
