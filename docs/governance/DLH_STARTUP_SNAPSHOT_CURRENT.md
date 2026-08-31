# Deep Learning + HANK Startup Snapshot — CURRENT

Date: 2026-08-31

Repository: `zcx369658780/deep-learning-hank`

Local Owner-designated workspace: `D:\deep-learning-hank`

## Governance state

- live GitHub `main` = synchronized repository/governance authority;
- GitHub Issue = sole DSH Builder task authority after publication + activation;
- DSH = bounded Builder/executor;
- ChatGPT = independent fresh-GitHub reviewer / scientific-route authority / task issuer / GitHub governance operator;
- Owner = final scientific-direction authority;
- Builder completion is not acceptance.

Priority:

`Scientific correctness > Experiment reproducibility > Research iteration speed > Git auditability > Documentation completeness`

## Current Builder state

`NO_ACTIVE_BUILDER_ISSUE__DLH_5A_ACCEPTED`

Do not execute a new Builder/model task until a new exact GitHub Issue is published, authority pointers are synchronized, and an authoritative activation comment is added.

## Latest accepted scientific-design gate

Issue #24 — DLH-5A

Accepted commit merged to `main`:

`820f23375377b21561d261c0850917056dec15c2`

Accepted classification:

`DLH_5A_NETWORK_READY_TWO_REGION_STRUCTURAL_CONTRACT_ACCEPTED`

Acceptance level:

`L3_COMMIT_VERIFIED__SCIENTIFIC_DESIGN_CONTRACT_ACCEPTED`

Accepted artifacts:

- `docs/specifications/DLH_5A_NETWORK_READY_TWO_REGION_STRUCTURAL_AND_OUTER_FIXED_POINT_CONTRACT_2026_08_31.md`
- `docs/audits/DLH_5A_HISTORICAL_MATLAB_PROVENANCE_AND_REPLACEMENT_BOUNDARY_2026_08_31.md`

## Accepted A1/A2 structural contract

### Prototype role

A1/A2 is a two-region **real structural HA-GE outer-fixed-point prototype**.

For this stage:

- household block = accepted two-asset HA/HJB/KFE foundation;
- regional production/price feedback = real competitive firm block;
- common liquid return `r_b`, regional taxes `tau_i`, transfers `T_i` are exogenous/config inputs;
- genuine nominal HANK closure is deferred to Track B (B1/B2).

No A1/A2 result may be called a validated genuine regional nominal HANK policy experiment.

### Provisional private-capital closure

Exploratory NSR-HANK authority:

`K_i = M_i * A_i`

with

`Y_i = Z_i * K_i^alpha_i * (L_i^dest)^(1-alpha_i)`

`w_i = (1-alpha_i) * Y_i / L_i^dest`

`r_i^a = alpha_i * Y_i / K_i - delta_i`.

This is explicitly a new prototype closure, not the historical MATLAB `N=1` limit.

`B_i` remains an endogenous household liquid-asset aggregate/diagnostic and is not productive capital or an arbitrary root target.

Government productive capital / historical `GovInv` is deferred.

### Labor-network interface

Household home-region identity stays fixed.

Define hand-specified origin outflow `m_i^L`, conditional destination weights `W^L`, complete allocation matrix `P^L`, labor flows

`F^L_ij = M_i * L_i^home * P^L_ij`,

and destination labor

`L_j^dest = sum_i F^L_ij`.

Composite gross wage seen by origin household `i`:

`wbar_i = sum_j P^L_ij * w_j`.

No migration/commuting resource cost is present in A1/A2.

With two regions, conditional destination choice is mechanically degenerate; A2 validates architecture/conservation/fixed-point behavior, not network identification.

### Synchronous outer semantics

Both regional HA blocks consume the same immutable old outer-state snapshot:

`Gamma^(n) = {w_1, w_2, r_1^a, r_2^a}`.

The one-turn map is Jacobi/synchronous and must be region-order invariant.

## Frozen A1 validity/trace concepts

The accepted contract defines:

- separate per-household vs region-total quantities;
- labor origin conservation;
- economy-wide labor conservation;
- gross wage-bill consistency;
- network row-sum/nonnegativity validity;
- HJB/KFE/mass/boundary diagnostic interfaces;
- positive finite firm-factor states;
- outer residuals `R_w` and `R_ra`;
- deterministic per-turn trace fields and explicit stop reasons;
- no PASS-seeking adaptive retuning.

Reviewer observation for A2:

The currently accepted `solve_household_steady_state` fail-closes on HJB nonconvergence. Historical MATLAB post-loop KFE-after-false semantics remain provenance only and must not be silently reintroduced without separate authority.

## Accepted household foundation

Canonical implementation:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Accepted Issue #23 commit:

`b038db800da3760cebee484b1c7a76bf7c1529d0`

Post-repair identity:

- Git blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`
- SHA-256 `1795718C469FC3B427CAB8E3D5957C133BEAD6EACC9EF0A25A3EDB7211D1A024`

Accepted Issue #23 classification:

`DLH_4D_R3_MATLAB_TRANSFER_FOC_PARITY_REPAIR_ACCEPTED__OLD_FIXED_BOND_GE_CLOSURE_SUPERSEDED`

Old `B_hh=B_gov=1` / nested-Brent Phase-E route remains superseded and must not be resumed.

## Current scientific route

Current roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_08_31.md`

Working label:

`Network-Structured Regional HANK (NSR-HANK)`

Long-run objective:

> regional data + bilateral flows + institutional configuration → structural multi-region HANK with learned interregional networks, selected parameter mappings, year-specific equilibria, and explicit numerical/economic/empirical/generalization diagnostics.

Core order:

1. accepted structural two-asset household foundation;
2. accepted network-ready two-region design contract;
3. deterministic hand-specified-flow two-region implementation/validation;
4. OD-year data schema + transparent baseline;
5. learned `W^L`;
6. 3–5 region equilibrium embedding;
7. minimal genuine nominal HANK block separately frozen/validated;
8. learned `W^K` later;
9. equilibrium-constrained fine-tuning and later regional parameter mapping;
10. 31-region year-specific panel / automated data-to-model pipeline;
11. policy/welfare only after all relevant gates.

## Recommended next Issue candidate — NOT ACTIVE

Tentative:

`DLH-5B / A2 — Implement and validate deterministic two-region hand-specified-flow outer fixed point`

Before publication/execution, freeze an exact small exploratory fixture/config:

- `Gamma^(0)`;
- `m_i^L / W^L`;
- `Z_i, alpha_i, delta_i, M_i, tau_i, T_i, rb_gap_i, r_b`;
- exact accepted household/grid/numerical config;
- outer `lambda`, `tol_w`, `tol_ra`, `max_iter`;
- retry/no-overwrite/output policy;
- validity-gate tolerances;
- deterministic reproducibility and region-order-invariance checks.

No such fixture is active yet.

## Scientific ceiling after DLH-5A

Accepted:

- repaired two-asset HA foundation;
- HANK outer-fixed-point interpretation;
- NSR-HANK/data-to-regional-HANK roadmap;
- reviewed network-ready two-region real structural design contract.

Not yet established:

- implemented/converged two-region fixed point;
- learned labor/capital networks;
- genuine nominal regional HANK;
- differentiable/equilibrium-constrained calibration;
- automatic model generator;
- 31-region learned equilibrium;
- policy/welfare/paper Results.

## Next-session startup

1. fresh fetch live `origin/main`;
2. read all CURRENT project rules;
3. read `tasks/TASK_INDEX_CURRENT.md`;
4. read this Startup Snapshot;
5. read current Master Roadmap and Handoff;
6. read the accepted DLH-5A contract/audit;
7. inspect Issue #24 acceptance comment if needed;
8. do not start A2 implementation until its exact Issue is published and activated.
