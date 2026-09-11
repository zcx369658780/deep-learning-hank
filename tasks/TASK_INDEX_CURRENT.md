# Deep Learning + HANK Task Index

Status: `NO_ACTIVE_BUILDER_ISSUE__DLH_5VD_ACCEPTED_OUTCOME_A__REMAINING_REGULAR_SECTOR_GATE_PENDING`

Last synchronized: 2026-09-11

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

**NONE.**

Issue #52 / DLH-5V-D is scientifically accepted and CLOSED completed. DSH must remain stopped until a successor Issue is separately published, CURRENT Task Index / Startup Snapshot are synchronized, and an authoritative activation comment is posted. Chat text alone does not create Builder authority.

## Latest accepted task — Issue #52 / DLH-5V-D

Title:

`DLH-5V-D: Freeze control-dependent W1 wide-stencil rates and conservative same-process generator contract`

Task type:

`SCIENTIFIC_DESIGN__W1_WIDE_STENCIL_CONTROL_DEPENDENT_RATE_AND_CONSERVATIVE_GENERATOR_CONTRACT`

Accepted candidate:

`81705b0c1671a8ee09ee5c2f05953f3e4f9f1e8b`

Reviewer acceptance:

`5631523081`

Acceptance integration:

`d58bd962be3acc8b6f646b66643bbc96f121be57`

Acceptance level:

`L3_COMMIT_VERIFIED__SCIENTIFIC_DESIGN_ACCEPTED`

Accepted verdict:

`DLH_5VD_ACCEPTED__OUTCOME_A_CONFIRMED__REGULAR_REALLOCATION_CONTROL_DEPENDENT_RATE_AND_CONSERVATIVE_GENERATOR_CONTRACT_FROZEN__READY_FOR_REMAINING_REGULAR_SECTOR_GATE`

Accepted terminal:

`DLH_5VD_REGULAR_REALLOCATION_CONTROL_DEPENDENT_RATE_AND_CONSERVATIVE_GENERATOR_CONTRACT_FROZEN__READY_FOR_REMAINING_REGULAR_SECTOR_GATE`

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
D_W(W_max) = {0<=a<=a_max, b>=b_min, a+b<=W_max}
```

No numerical production `W_max` is selected.

## Accepted DLH-5V-D contract — regular `T_realloc` sector

Accepted regular reallocation sector:

```text
T_realloc = {mu_a<=0, mu_b>=0, mu_W=mu_a+mu_b<=0}
```

Accepted regular W1 displacements for `j>=7`:

```text
w_in = (-10/19,0)
w_T  = (-70/19,+70/19)
wide destination = (j-7,i+10)
```

For every continuously admissible candidate control whose drift lies in `T_realloc`, the accepted **sector-candidate scoring** rate map is

```text
q_T  = 19*mu_b/70
q_in = 19*(-mu_W)/10
```

with fixed-aspect refinement rates divided by `h`.

Accepted scientific semantics:

- the two-ray decomposition is exact, nonnegative and unique on `T_realloc`;
- zero-rate equality cases vanish continuously;
- the rates enter the candidate's discrete `H_h` score before any global maximization;
- Issue #52 does **not** freeze the global regular-W-boundary argmax;
- outside-`T_realloc` but continuously admissible candidates remain in the future global HJB choice set;
- canonical asset-drift representation in this sector uses exactly `{q_in,q_T}`, without shared-face double counting;
- actual represented off-diagonals are nonnegative and the diagonal is the negative sum of actual outgoing rates, so `Q1=0` by construction;
- omitted-destination / retained-diagonal leakage is forbidden;
- after all regular sectors are closed, one global discrete-Hamiltonian argmax will select a candidate with already-defined sector-specific rates, producing one backward `Q`;
- future KFE must consume exactly that `Q^T` and may not rebuild boundary transitions independently;
- downstream mass semantics remain `p=Mg`, `p_dot=Q^T p`; pin/normalization is scale fixing only and Issue #27 component-pin authority remains unchanged.

## Next bounded scientific object

The continuous regular W-face tangent cone is `{mu_W<=0}`. The accepted DLH-5V-D contract covers only `T_realloc`. The remaining regular sector is

```text
{mu_W<=0} \ T_realloc
= {mu_b<0, mu_W<=0}.
```

It contains:

1. reverse reallocation: `mu_a>0, mu_b<0, mu_W<=0`;
2. both-inward depletion: `mu_a<=0, mu_b<0`.

Recommended successor gate: **remaining admissible regular W-boundary sector transition/rate design**. No remedy is active or pre-authorized yet.

Endpoint/joint-boundary closure remains separate and downstream. Implementation, numerical `W_max`, stationary-generator validation, stationary KFE, aggregates, GE, multi-province execution and neural training remain unauthorized.

## Downstream KFE safeguards

Future implementation acceptance must include finite generator entries, nonnegative off-diagonals, `||Q1||_inf`, frozen orientation/flattening, exact same `Q` from HJB to KFE, SCC/closed recurrent-class diagnostics, original source-free `Q^T p` residual, mass normalization/nonnegativity and density conversion through cell weights.

Current Startup Snapshot:

`docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`

Current Master Roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
