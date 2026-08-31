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

Current published task:

**Issue #24 — DLH-5A: Freeze network-ready two-region structural and outer-fixed-point contract**

Task type:

`SCIENTIFIC_DESIGN__NETWORK_READY_TWO_REGION_FIXED_POINT_CONTRACT`

Builder authority is active only when the authoritative Issue #24 activation comment is present and Issue #24 remains open.

Dedicated branch after activation:

`dsh/issue-24-dlh-5a-two-region-structural-contract-2026-08-31`

DLH-5A is design/specification only. DSH may create only the two Issue-authorized Markdown artifacts and must not modify production/model/config/test/governance/roadmap files.

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
- committed evidence reports 137 passing tests;
- 729-point post-repair diagnostic: FULL_FINITE 277→499, zero previously-finite regressions, exact repeat reproducibility;
- remaining HJB non-convergence/KFE singular regions are research diagnostics, not silently tuned away.

## Superseded single-region GE route

Not current authority:

- `B_hh = B_gov = 1` as an intended equilibrium target;
- nested cold-start Brent over `(r_a,r_b,L)` as HANK steady-state architecture;
- resuming the 8.77h Phase-E frozen solve;
- treating HA as an analytic/static DSGE steady-state block.

The Phase-E run is preserved only as `INCONCLUSIVE / SUPERSEDED_CLOSURE_EXECUTION_EVIDENCE`.

## Correct HANK equilibrium concept

Regional HANK steady state is an outer/nested fixed point across structural blocks:

`current regional prices/state`
→ `conditional regional HA stationary HJB/KFE solves`
→ `household aggregates`
→ `interregional flow allocation`
→ `firm/fiscal/monetary updates`
→ `new regional prices/state`
→ repeat until project-defined convergence and validity gates pass.

Historical MATLAB outer iteration is provenance for this computational architecture only. Its hand-coded spatial allocation rules are not automatically new-model authority.

## Current scientific route

Current roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_08_31.md`

Working label:

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

## DLH-5A Owner-frozen scientific decisions

### 1. Prototype role

A1/A2 first build a two-region **real structural HA-GE outer-fixed-point prototype**. Common liquid return `r_b`, regional taxes `tau_i` and transfers `T_i` are exogenous/config inputs. Genuine nominal HANK closure is deferred to Track B.

### 2. Provisional private-capital closure

New exploratory NSR-HANK specification for A1/A2:

`K_i = M_i * A_i`

with real firm block:

`Y_i = Z_i * K_i^alpha_i * (L_i^dest)^(1-alpha_i)`

`w_i = (1-alpha_i) * Y_i / L_i^dest`

`r_i^a = alpha_i * Y_i / K_i - delta_i`.

This is not claimed as the historical MATLAB `N=1` limit.

`B_i` remains a household liquid-asset aggregate/diagnostic; no `B=1` clearing.

Government productive capital / historical `GovInv` is deferred from A1/A2.

### 3. Labor network

Household home-region identity stays fixed. Define origin outflow `m_i^L`, conditional destination network `W^L`, full allocation matrix `P^L`, flows

`F^L_ij = M_i * L_i^home * P^L_ij`,

and destination labor

`L_j^dest = sum_i F^L_ij`.

First-prototype composite gross wage:

`wbar_i = sum_j P^L_ij * w_j`.

No migration/commuting resource cost is introduced in A1/A2.

### 4. Outer semantics

Both regional HA solves consume the same old outer-state snapshot. The mathematical one-turn map is synchronous/Jacobi and must have no region-order dependence.

## DLH-5A required outputs

DSH may create exactly:

1. `docs/specifications/DLH_5A_NETWORK_READY_TWO_REGION_STRUCTURAL_AND_OUTER_FIXED_POINT_CONTRACT_2026_08_31.md`
2. `docs/audits/DLH_5A_HISTORICAL_MATLAB_PROVENANCE_AND_REPLACEMENT_BOUNDARY_2026_08_31.md`

The first must freeze interfaces, notation, equations, one-turn order, conservation/validity diagnostics, residual/trace interface, and A2 handoff checklist.

The second must distinguish historical MATLAB provenance from new NSR-HANK authority, including `At/Bt/GovInv` semantics and the old spatial/controller formulas intentionally replaced or deferred.

## DLH-5A explicit non-authority

Issue #24 does not authorize:

- source/model implementation;
- HJB/KFE/GE numerical execution;
- household redesign;
- neural training or learned `W^L`;
- `W^K`;
- government productive capital / `GovInv` integration;
- Taylor/Fisher/Phillips/nominal structure;
- new fiscal/debt closure;
- 31-region scaling;
- policy/welfare/Results claims.

## Parameter-learning boundary

Do not start by making all economic parameters free neural outputs.

Separate:

- Tier 0: theory/specification parameters;
- Tier 1: observed/institutional inputs;
- Tier 2: low-dimensional calibrated local parameters;
- Tier 3: learned network/parameter mappings.

Only after separate identification gates may the project use a joint equilibrium-constrained loss.

## Scientific ceiling during DLH-5A

Accepted before Issue #24:

- repaired two-asset HA foundation;
- HANK outer-fixed-point interpretation;
- NSR-HANK/data-to-regional-HANK roadmap.

Issue #24 may establish only a reviewed **network-ready two-region structural design contract**.

Not yet established:

- an implemented/converged two-region fixed point;
- learned labor/capital networks;
- genuine nominal regional HANK;
- differentiable/equilibrium-constrained calibration;
- automatic model generator;
- 31-region learned equilibrium;
- policy/welfare/paper Results.

## DSH startup sequence for Issue #24

1. `Set-Location D:\deep-learning-hank`;
2. verify repo/remote/worktree;
3. `git fetch origin` and record fresh `origin/main`;
4. read all CURRENT rules;
5. read `tasks/TASK_INDEX_CURRENT.md` and this Startup Snapshot from fresh `origin/main`;
6. read Issue #24 latest body/comments and verify activation;
7. read the current roadmap/handoff and accepted household source;
8. use the historical MATLAB handoff only under its read-only/provenance boundary;
9. create the exact dedicated branch from fresh `origin/main`;
10. create only the two authorized Markdown design artifacts;
11. commit/push and STOP for ChatGPT independent review.
