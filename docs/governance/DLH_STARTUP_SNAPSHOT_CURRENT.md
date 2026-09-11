# Deep Learning + HANK Startup Snapshot — CURRENT

Date: 2026-09-11

Repository: `zcx369658780/deep-learning-hank`

Local Owner-designated workspace: `D:\deep-learning-hank`

## Governance state

- live GitHub `main` = synchronized repository/code/governance authority;
- GitHub Issue = sole DSH Builder authority only after publication + CURRENT Task Index / Startup synchronization + authoritative activation comment;
- DSH = bounded Builder/scientific analyst only under an active Issue;
- ChatGPT = independent reviewer / scientific-route advisor / task issuer / governance operator;
- Owner = final scientific authority;
- Builder completion is not acceptance.

Priority:

`Scientific correctness > Experiment reproducibility > Research iteration speed > Git auditability > Documentation completeness`

## Current Builder state

Current published task:

**Issue #53 — DLH-5V-E: Close remaining regular W-boundary sectors and full regular candidate-scoring contract**

Task type:

`SCIENTIFIC_DESIGN__REMAINING_REGULAR_W_BOUNDARY_SECTORS_AND_FULL_REGULAR_SCORING_CLOSURE`

Dedicated branch:

`dsh/issue-53-dlh-5ve-remaining-regular-sector-2026-09-11`

Owner continuation decision:

`APPROVE_DLH_5VE_REMAINING_REGULAR_W_BOUNDARY_SECTOR_CLOSURE_GATE`

Builder authority becomes active only while Issue #53 remains OPEN, CURRENT Task Index / this Snapshot identity matches, and the authoritative activation comment is present.

## Latest accepted gate — Issue #52 / DLH-5V-D

Accepted candidate:

`81705b0c1671a8ee09ee5c2f05953f3e4f9f1e8b`

Reviewer acceptance:

`5631523081`

Acceptance integration:

`d58bd962be3acc8b6f646b66643bbc96f121be57`

Acceptance verdict:

`DLH_5VD_ACCEPTED__OUTCOME_A_CONFIRMED__REGULAR_REALLOCATION_CONTROL_DEPENDENT_RATE_AND_CONSERVATIVE_GENERATOR_CONTRACT_FROZEN__READY_FOR_REMAINING_REGULAR_SECTOR_GATE`

## Controlling household / finite-domain authority

Accepted household source remains immutable/read-only:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Binding law:

```text
HJB boundary policy <=> KFE boundary transition law
```

Stationary KFE remains **NOT AUTHORIZED**.

Accepted finite domain remains:

```text
D_W(W_max) = {0<=a<=a_max, b>=b_min, a+b<=W_max}.
```

Restricted-Voronoi state partition, weighted mass/density semantics, discrete-Hamiltonian requirement, and one-`Q` HJB/KFE principle remain accepted. No numerical production `W_max` is selected.

## Accepted regular W-frontier authority through DLH-5V-D

Exact grid:

```text
da=10/19
db=7/19.
```

Regular W-face tangent cone:

```text
T_W={mu_W=mu_a+mu_b<=0}.
```

Accepted forward-reallocation sector:

```text
T_realloc={mu_a<=0,mu_b>=0,mu_W<=0}.
```

Accepted physical directions/rates:

```text
w_in=(-10/19,0)
w_T=(-70/19,+70/19)
q_in=19*(-mu_W)/10
q_T=19*mu_b/70.
```

For each admissible candidate in `T_realloc`, these rates are computed before selection and score the candidate in the discrete `H_h`. DLH-5V-D deliberately did not freeze a global regular-boundary argmax because the remaining tangent-admissible sector still lacked a transition/rate contract.

Conservative one-Q semantics remain:

```text
Q_ij>=0 for i!=j
Q_ii=-sum actual represented outgoing rates
Q1=0 by construction
future forward operator = exactly Q^T.
```

KFE may not reconstruct boundary rates independently. Downstream mass semantics remain `p=Mg`, `p_dot=Q^T p`; Issue #27 component pin remains scale fixing only, never leakage repair.

## Active DLH-5V-E scientific target

The remaining regular sector is

```text
T_rem={mu_b<0,mu_W<=0},
```

split into

```text
R_reverse={mu_a>0,mu_b<0,mu_W<=0}
R_deplete={mu_a<=0,mu_b<0}.
```

Candidate reverse-reallocation mirror tangent to audit:

```text
(Delta j,Delta i)=(+7,-10)
w_RT=(+70/19,-70/19).
```

This edge is **not yet accepted**. Builder must prove/refute represented destination/path/class preservation on a precisely declared regular region and identify finite endpoint/joint-boundary exclusions.

Candidate reverse rates to prove/refute:

```text
q_RT=19*mu_a/70
q_down=19*(-mu_W)/7.
```

Both-inward depletion should audit the local axial basis

```text
w_left=(-10/19,0)
w_down=(0,-7/19)
```

with candidate rates

```text
q_left=19*(-mu_a)/10
q_down=19*(-mu_b)/7.
```

If both sub-sectors pass, Builder may prove full regular coverage of every `mu_W<=0` candidate and freeze the future global composition:

```text
all admissible regular candidates
 -> exactly one sector-specific discrete-H_h score
 -> ONE global regular argmax
 -> selected control + already-defined rates
 -> ONE conservative backward Q
 -> future KFE uses exactly Q^T.
```

This remains design semantics only. Endpoint/joint-boundary closure is separately downstream.

## KFE methodology safeguard

The independently stabilized Chapter-5 clean/source-free KFE route is supporting methodology only:

```text
Q backward; Q^T forward
off-diagonal >=0
diagonal = -sum actual outgoing
Q1=0
same Q HJB/KFE
mass-first stationary object
SCC/closed classes before uniqueness
pin/normalization = scale fixing only
original Q^T p residual required downstream.
```

MATLAB-faithful contaminated-row reproduction logic is not imported.

## Context-budget rule

After all CURRENT project rules, current Task Index / this Snapshot / Roadmap, and full Issue #53 + comments, scientific reading is limited to:

1. `docs/design/DLH_5VD_CONTROL_DEPENDENT_WIDE_STENCIL_RATE_AND_CONSERVATIVE_GENERATOR_CONTRACT.md`
2. `reports/dlh_5vd_wide_stencil_rate_contract_2026_09_11/DLH_5VD_CONTROL_DEPENDENT_RATE_DECOMPOSITION.md`
3. `reports/dlh_5vd_wide_stencil_rate_contract_2026_09_11/DLH_5VD_CONSERVATIVE_GENERATOR_AND_KFE_HANDOFF_CONTRACT.md`
4. `docs/design/DLH_5VA_REGULAR_VORONOI_FRONTIER_PHASE_AND_ADJACENCY.md` only if accepted regular adjacency/class formulas are needed.

Verify the accepted household source blob only. Do not reread broad DLH-5T/5U/5V-B/5V-C history without a concrete contradiction.

## Scientific ceiling

Design only. Do not mutate source/economics; change grid/aspect ratio; implement transitions; numerically assemble `Q`; execute HJB/KFE/stationary; redesign endpoint/joint-boundary states; select numerical `W_max`; redesign Issue #27 pinning; import contaminated-row KFE production logic; compute aggregates/GE; or enter multi-province/neural/nominal/calibration/policy/welfare/Results.

## Planned session handoff checkpoint

The chosen handoff point is **after Issue #53 is independently reviewed and, if valid, accepted**. Before handing off, update Task Index, this Startup Snapshot, Master Roadmap, and create a dedicated current session/project-source handoff snapshot with live `main`, accepted SHAs, Issue states, unresolved endpoint/joint-boundary work, KFE safeguards, and the exact next route.

Current Master Roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`

Chat text is not Builder authority.
