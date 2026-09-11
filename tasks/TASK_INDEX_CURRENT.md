# Deep Learning + HANK Task Index

Status: `NO_ACTIVE_BUILDER_ISSUE__DLH_5VC_ACCEPTED_OUTCOME_A__WIDE_STENCIL_RATE_GATE_PENDING`

Last synchronized: 2026-09-11

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

**NONE.**

Issue #51 / DLH-5V-C is scientifically accepted and CLOSED completed. DSH must remain stopped until a successor Issue is separately published, CURRENT Task Index / Startup Snapshot are synchronized, and an authoritative activation comment is posted.

Chat text alone does not create Builder authority.

## Latest accepted task — Issue #51 / DLH-5V-C

Title:

`DLH-5V-C: Audit W1 wide-stencil exact-tangent transport on the regular W frontier`

Task type:

`SCIENTIFIC_DESIGN__W1_WIDE_STENCIL_EXACT_TANGENT_REGULAR_FEASIBILITY`

Accepted candidate:

`2134a4b249eb0a79dc20d60ba1fdee830304f261`

Reviewer acceptance:

`5630191586`

Acceptance integration:

`cdbf1906963a9bf06cf117ba63072d2f1542d501`

Acceptance level:

`L3_COMMIT_VERIFIED__SCIENTIFIC_DESIGN_ACCEPTED`

Accepted verdict:

`DLH_5VC_ACCEPTED__OUTCOME_A_CONFIRMED__W1_WIDE_STENCIL_EXACT_TANGENT_REGULAR_FEASIBILITY_FROZEN__READY_FOR_WIDE_STENCIL_RATE_GATE`

Accepted terminal:

`DLH_5VC_W1_WIDE_STENCIL_EXACT_TANGENT_REGULAR_FEASIBILITY_FROZEN__READY_FOR_WIDE_STENCIL_RATE_GATE`

## Accepted scientific result

Accepted household source remains immutable/read-only:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Binding law:

```text
HJB boundary policy <=> KFE boundary transition law
```

Stationary KFE remains **NOT AUTHORIZED**.

The accepted regular-region remedy is an explicit boundary wide-stencil Markov transition based on the primitive exact lattice tangent

```text
10 Delta j + 7 Delta i = 0,
(Delta j,Delta i)=(-7,+10),
Delta x_T=(-70/19,+70/19).
```

For represented regular W-frontier states with `j>=7`:

- destination `(j-7,i+10)` is represented;
- the full straight segment remains inside `D_W` and satisfies `a+b=const`;
- `r_{j-7}=r_j`, so A^F/A^L/B^W class and top/sub-top offset are preserved;
- the only excluded object is the finite endpoint band `j in {0,...,6}`;
- `cone{(-10/19,0),(-70/19,+70/19)} = T_realloc` exactly;
- for `mu=(-a-b,+a)`, `a,b>=0`, the analytic feasibility coefficients are `q_T=19a/70`, `q_in=19b/10` on the base grid, with `O(1/h)` scaling under refinement;
- the physical wide jump is `O(h)`, first-moment consistency is exact, and the smooth-test-function remainder is `O(h)`;
- the same wide edge may enter backward HJB and forward `Q^T p` as one controlled process.

This acceptance is regular-region feasibility only. It does not freeze production rate/control-dependence semantics, endpoint/corner handling, implementation, numerical `W_max`, or stationary KFE.

## Next bounded scientific object

Recommended next gate: **wide-stencil production rate / control-dependence design**.

It should freeze how the HJB-selected admissible drift is decomposed into nonnegative local-inward and wide-tangent rates, including control dependence, activation/tie-breaking semantics, row-sum conservation, and exact reuse of the converged rates in KFE. It must remain design-only until separately authorized.

Endpoint/corner closure remains a separate downstream gate. HJB/KFE implementation, Wmax robustness, stationary generator validation, stationary KFE, aggregates, GE, multi-province execution and neural training remain unauthorized.

Current Startup Snapshot:

`docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`

Current Master Roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
