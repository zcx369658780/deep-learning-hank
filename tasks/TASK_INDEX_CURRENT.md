# Deep Learning + HANK Task Index

Status: `ACTIVE_BUILDER_ISSUE__DLH_5A_SCIENTIFIC_DESIGN`

Last synchronized: 2026-08-31

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

Current Issue:

**Issue #24 — OPEN**

Title:

`DLH-5A: Freeze network-ready two-region structural and outer-fixed-point contract`

Task type:

`SCIENTIFIC_DESIGN__NETWORK_READY_TWO_REGION_FIXED_POINT_CONTRACT`

Issue #24 is the sole DSH Builder authority **after** the authoritative activation comment is present on the Issue.

DSH must fresh-fetch `origin/main`, read this Task Index, the CURRENT Startup Snapshot, all CURRENT rules, and the latest authoritative Issue #24 body/comments before any mutation.

If Issue #24 is not open, the activation comment is absent, or Issue/Task Index/Startup Snapshot identity is inconsistent, DSH must fail closed.

## Issue #24 scientific scope

DLH-5A is design/specification only.

The Owner has frozen four decisions for the A1/A2 prototype:

1. two-region **real structural HA-GE outer-fixed-point prototype** first; common `r_b`, regional `tau_i/T_i` exogenous; genuine nominal HANK deferred to Track B;
2. provisional new NSR-HANK private-capital closure `K_i = M_i * A_i`; `B_i` is household liquid-asset aggregate/diagnostic and is not a productive-capital or arbitrary root target;
3. fixed home-region household identity plus hand-specified labor network `m_i^L / W^L / P^L`, labor-service flows `F^L`, destination labor `L^dest`, and gross composite wage `wbar_i = sum_j P^L_ij w_j`;
4. synchronous/Jacobi outer-turn semantics: both regional HA blocks read the same old-state snapshot; no same-turn region-order contamination.

Issue #24 must produce only:

- `docs/specifications/DLH_5A_NETWORK_READY_TWO_REGION_STRUCTURAL_AND_OUTER_FIXED_POINT_CONTRACT_2026_08_31.md`
- `docs/audits/DLH_5A_HISTORICAL_MATLAB_PROVENANCE_AND_REPLACEMENT_BOUNDARY_2026_08_31.md`

No production code, tests, neural training, GE execution, nominal block, `W^K`, `GovInv`, 31-region scaling, policy/welfare or Results are authorized.

Dedicated Builder branch after activation:

`dsh/issue-24-dlh-5a-two-region-structural-contract-2026-08-31`

## Latest accepted task

Issue #23 — CLOSED / COMPLETED

Title:

`DLH-4D-R3: Repair MATLAB-faithful transfer-FOC liquid-derivative semantics and revalidate frozen GE path`

Accepted candidate commit merged to `main`:

`b038db800da3760cebee484b1c7a76bf7c1529d0`

Accepted reviewer classification:

`DLH_4D_R3_MATLAB_TRANSFER_FOC_PARITY_REPAIR_ACCEPTED__OLD_FIXED_BOND_GE_CLOSURE_SUPERSEDED`

Accepted scientific meaning:

- MATLAB-faithful raw-liquid-derivative transfer-FOC handling is repaired;
- post-repair two-asset household identity is SHA-256 `1795718C469FC3B427CAB8E3D5957C133BEAD6EACC9EF0A25A3EDB7211D1A024`;
- focused evidence reports 137 passing tests;
- frozen 729-point reclassification improves FULL_FINITE 277→499 with zero previously-finite regressions and exact repeat reproducibility;
- old `B_hh=B_gov=1` / nested-Brent Phase-E route is superseded and must not be resumed.

## Current scientific route authority

Current roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_08_31.md`

Core direction:

- hard structural household/HJB/KFE/firm/equilibrium definitions;
- outer fixed-point HANK equilibrium architecture;
- network-ready small-region prototype first;
- learned labor-flow network `W^L` as the first Deep Learning object;
- learned capital network `W^K` later;
- genuine nominal HANK block separately frozen/validated before policy-HANK claims;
- staged equilibrium-constrained calibration and later learned regional parameter mapping;
- long-run target: data + institutional config → automatically calibrated regional HANK model + learned networks + equilibrium diagnostics.

Historical MATLAB multi-province code remains provenance/reference for iterative architecture and selected structural semantics. Its hand-coded interregional mappings are not the new model target.

## Scientific ceiling during Issue #24

Accepted before DLH-5A:

- repaired two-asset HA/HJB/KFE/aggregate foundation;
- rejection of the arbitrary fixed-bond nested-Brent closure;
- NSR-HANK/data-to-regional-HANK roadmap.

DLH-5A may establish only a reviewed two-region structural **design contract**.

Not yet validated:

- implemented network-ready regional fixed point;
- converged two-region equilibrium;
- learned `W^L`;
- learned `W^K`;
- genuine regional nominal HANK;
- equilibrium-constrained neural calibration;
- automatic regional parameter generator;
- 31-region learned equilibrium panel;
- policy/welfare/Results claims.
