# Deep Learning + HANK Task Index

Status: `ROADMAP_REBASE_COMPLETE__NO_ACTIVE_BUILDER_ISSUE`

Last synchronized: 2026-08-31

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

There is currently **no active Builder Issue**.

DSH must not execute new scientific/model mutations until a separately published and activated GitHub Issue exists.

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
- post-repair two-asset household identity is recorded as SHA-256 `1795718C469FC3B427CAB8E3D5957C133BEAD6EACC9EF0A25A3EDB7211D1A024`;
- focused parity/regression evidence reports 137 passing tests;
- frozen 729-point reclassification improves FULL_FINITE 277→499 with zero previously-finite regressions and exact repeat reproducibility;
- the 8.77h Phase-E nested-Brent run is INCONCLUSIVE runtime evidence only;
- authoritative Owner clarification supersedes the old arbitrary `B_hh=B_gov=1` / nested-Brent closure as the intended project steady-state route.

## Current scientific route authority

Current roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_08_31.md`

Core direction:

- hard structural household/HJB/KFE/firm/equilibrium definitions;
- outer fixed-point HANK equilibrium architecture;
- hand-specified network-ready small-region prototype first;
- learned labor-flow network `W^L` as the first Deep Learning object;
- learned capital network `W^K` later;
- genuine nominal HANK block separately frozen/validated before policy-HANK claims;
- staged equilibrium-constrained calibration and later learned regional parameter mapping;
- long-run target: data + institutional config → automatically calibrated regional HANK model + learned networks + equilibrium diagnostics.

Historical MATLAB multi-province code is provenance/reference for HANK outer-iteration architecture and selected structural equations. Its hand-coded interregional mappings are **not** the new model target.

## Explicitly superseded

Do not resume as current route:

- `B_hh = B_gov = 1` validation target;
- nested cold-start Brent over `(r_a,r_b,L)` as intended HANK steady-state construction;
- treating the HA conditional stationary problem as an analytic/static DSGE steady-state block.

Historical Issues #19–#22 remain evidence, not forward closure authority.

## Recommended next Issue candidate

Tentative task identity:

`DLH-5A — Freeze Network-Ready Two-Region Structural and Outer-Fixed-Point Contract`

Expected task type:

`SCIENTIFIC_DESIGN__NETWORK_READY_TWO_REGION_FIXED_POINT_CONTRACT`

Expected scope:

- design/specification first;
- no neural training yet;
- define two-region structural interfaces and hand-specified `W^L` contract;
- define outer state/update order, convergence/failure trace and conservation gates;
- consume accepted two-asset HA kernel;
- use MATLAB handoff only as provenance for iterative architecture, not as a spatial-replication target.

The next Issue is **not active** until publication + Task Index/Startup synchronization + authoritative activation comment.

## Scientific ceiling until next Issue

Accepted:

- two-asset HA/HJB/KFE/aggregate foundation with Issue #23 FOC repair;
- scientific rejection of the old fixed-bond nested-Brent closure;
- current NSR-HANK / data-to-regional-HANK roadmap.

Not yet validated:

- network-ready regional fixed point;
- learned `W^L`;
- learned `W^K`;
- genuine regional nominal HANK block;
- equilibrium-constrained neural calibration;
- automatic regional parameter generator;
- 31-region learned equilibrium panel;
- policy/welfare/Results claims.
