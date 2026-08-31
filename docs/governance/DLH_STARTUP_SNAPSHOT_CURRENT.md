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

`NO_ACTIVE_BUILDER_ISSUE__ROADMAP_REBASE_COMPLETE`

Do not execute a new Builder/model task until a new GitHub Issue is published, Task Index/Startup Snapshot are synchronized, and an authoritative activation comment is added.

## Latest accepted household foundation

Canonical implementation:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Accepted Issue #23 commit:

`b038db800da3760cebee484b1c7a76bf7c1529d0`

Post-repair identity:

- Git blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`
- SHA-256 `1795718C469FC3B427CAB8E3D5957C133BEAD6EACC9EF0A25A3EDB7211D1A024`

Accepted reviewer classification:

`DLH_4D_R3_MATLAB_TRANSFER_FOC_PARITY_REPAIR_ACCEPTED__OLD_FIXED_BOND_GE_CLOSURE_SUPERSEDED`

Accepted meaning:

- two-asset `(b,a,z)` household/HJB/KFE/aggregate foundation remains the structural household engine;
- MATLAB raw-`V_b` transfer-FOC semantics are repaired;
- consumption/labor derivative floor remains separate from raw transfer-FOC `V_b`;
- bare-`a` FOC scaling, `max(a,a_bar)` cost floor, illiquid-return taper, boundary/upwind construction and contaminated-row KFE were not broadened/redesigned in Issue #23;
- committed test evidence reports 137 passing tests;
- 729-point post-repair diagnostic: FULL_FINITE 277→499, zero previously-finite regressions, exact repeat reproducibility;
- remaining HJB non-convergence/KFE singular regions are research diagnostics, not silently tuned away.

## Superseded single-region GE route

Owner scientific clarification on 2026-08-31 supersedes the prior arbitrary fixed-bond validation architecture as the project route.

Not current authority:

- `B_hh = B_gov = 1` as an intended equilibrium target;
- nested cold-start Brent over `(r_a,r_b,L)` as the HANK steady-state architecture;
- resuming the 8.77h Phase-E frozen `solve_ge` run;
- treating HA as an analytic/static DSGE steady-state block.

The Phase-E run is preserved only as `INCONCLUSIVE / SUPERSEDED_CLOSURE_EXECUTION_EVIDENCE`.

Historical Issues #19–#22 remain useful provenance/negative evidence but do not define the forward equilibrium closure.

## Correct HANK equilibrium concept for this project

Regional HANK steady state is an outer/nested fixed point across structural blocks:

`current regional prices/state`
→ `conditional regional HA stationary HJB/KFE solves`
→ `household aggregates`
→ `interregional flow allocation`
→ `firm/fiscal/monetary updates`
→ `new regional prices/state`
→ repeat until project-defined convergence and validity gates pass.

The historical MATLAB outer iteration is provenance for this computational architecture only. Its hand-coded spatial allocation rules are not automatically new-model authority.

## Current scientific route

Current roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_08_31.md`

Working model label:

`Network-Structured Regional HANK (NSR-HANK)`

Long-run objective:

> Given regional data, bilateral flows and an institutional configuration, generate/calibrate a structural multi-region HANK with learned interregional networks, selected learned parameter mappings, year-specific equilibria, and explicit numerical/economic/empirical/generalization diagnostics.

Core architecture:

1. hard structural regional household/HJB/KFE/firm/accounting definitions;
2. network-ready regional fixed-point engine;
3. learned labor-flow network `W^L` first;
4. learned capital network `W^K` later;
5. minimal genuine nominal HANK block separately specified/validated;
6. equilibrium-constrained fine-tuning only after flow identification;
7. later learned regional parameter mapping `p_{i,t}=g_P(Z_{i,t};theta_P)`;
8. scale to 31-region year-specific equilibrium panel;
9. later country/union model-generator extension.

## Parameter-learning boundary

Do not start by making all economic parameters free neural outputs.

Separate:

- Tier 0: theory/specification parameters;
- Tier 1: observed/institutional inputs;
- Tier 2: low-dimensional calibrated local parameters;
- Tier 3: learned network/parameter mappings.

Only after separate identification gates may the project use a joint equilibrium-constrained loss.

## Immediate next task candidate — not active yet

Tentative:

`DLH-5A — Freeze Network-Ready Two-Region Structural and Outer-Fixed-Point Contract`

Expected design goals:

- two structural regional household modules;
- home-region identity fixed;
- hand-specified `W^L` interface that later becomes learned;
- explicit outer state and one-turn update order;
- deterministic convergence/failure trace;
- labor-flow and accounting conservation gates;
- no old MATLAB spatial-formula replication requirement;
- no neural training yet;
- no arbitrary `B=1` root target.

## Scientific ceiling until next Issue

Accepted:

- repaired two-asset HA foundation;
- HANK outer-fixed-point interpretation;
- current NSR-HANK/data-to-regional-HANK roadmap.

Not yet established:

- regional network-ready fixed-point implementation;
- learned labor/capital networks;
- genuine nominal regional HANK;
- differentiable/equilibrium-constrained calibration;
- automatic model generator;
- 31-region learned equilibrium;
- policy/welfare/paper Results.

## Required next-session startup

1. fresh fetch live `origin/main`;
2. read CURRENT project rules;
3. read `tasks/TASK_INDEX_CURRENT.md`;
4. read this Startup Snapshot;
5. read `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_08_31.md`;
6. read Issue #23 acceptance/supersession comments and commit `b038db8...` as needed;
7. read `DeepLearning_HANK_MATLAB_NATIVE_STEADY_STATE_OUTER_ITERATION_SCIENTIFIC_HANDOFF_2026_08_31.md` from project sources when outer-loop provenance is needed;
8. do not activate a Builder task until the next exact Issue is published and activated.
