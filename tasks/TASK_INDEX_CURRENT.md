# Deep Learning + HANK Task Index

Status: `NO_ACTIVE_BUILDER__DLH_5VJ_TERMINAL_B_ACCEPTED__OWNER_STABILIZATION_ROUTE_DECISION_PENDING`

Last synchronized: 2026-09-12

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

**NO ACTIVE BUILDER ISSUE.**

Issue #58 / DLH-5V-J has completed and is accepted at Terminal B. Builder STOP is binding. No successor is authorized until Owner / ChatGPT selects the next scientifically controlled route.

## Latest accepted task — Issue #58 / DLH-5V-J

Title:

`DLH-5V-J: Implement boundary-HJB selected-Q solver and pass local validation gates`

Task type:

`SCIENTIFIC_IMPLEMENTATION__BOUNDARY_HJB_SELECTED_Q_AND_LOCAL_VALIDATION`

Accepted candidate / integration:

`7b564d1b7d7aaf76b808135b192646e0ec1f5f08`

Reviewer acceptance:

`5646205500`

Accepted verdict:

`DLH_5VJ_ACCEPTED__TERMINAL_B_CONFIRMED__BOUNDARY_HJB_IMPLEMENTATION_PARTIAL__EFFECTIVE_DOMAIN_EXIT_FROZEN__OWNER_STABILIZATION_ROUTE_DECISION_REQUIRED`

Accepted terminal:

`DLH_5VJ_BOUNDARY_HJB_IMPLEMENTATION_PARTIAL__ONE_BOUNDED_NUMERICAL_OR_CONTRACT_GAP_REMAINS`

Accepted implementation evidence:

- Gate 1A common-input F0 regression: PASS;
- Gate 2 Route-A family / boundary algebra / representability / first-moment structure: PASS;
- boundary selected-Q implementation is materially accepted;
- conservative iteration-1 backward Q: PASS (`max |Q1| ≈ 7.11e-15` on the frozen smoke);
- deterministic repeat through the first iterate: PASS;
- frozen Gate-3 HJB smoke does **not** converge: at iteration 2, family F3, `(j,i)=(13,13)`, `z=0`, the effective liquid marginal evidence is `p_b≈-0.365224`;
- the corrected implementation raises `DERIVATIVE_EFFECTIVE_DOMAIN_FAILURE` before any raw candidate/bracket search;
- the remaining gap is therefore the production pseudo-time iteration leaving the accepted positive-liquid-marginal effective domain before convergence.

This is inside the already accepted Issue #56 Outcome-B unbounded-control / state-constraint convergence-application ceiling. It is not a household-HJB equation error, geometry contradiction, or sector-algebra contradiction.

## Prior accepted design authority — Issue #57 / DLH-5V-I

Accepted candidate / integration:

`3e450cf8ae177015e68ee7e05ecc5d6be7b2f8ec`

Reviewer acceptance:

`5644767550`

Acceptance integration:

`5644769439`

Accepted verdict:

`DLH_5VI_ACCEPTED__OUTCOME_A_CONFIRMED__BOUNDARY_HJB_SCHEME_CONTRACT_FROZEN__IMPLEMENTATION_GATE_READY_UNDER_ACCEPTED_OUTCOME_B_THEORY_CEILING`

The Route-A F0–F11 classifier, representability dispatch, algorithm-only search-bracket semantics, Bellman ONE-selection contract, conservative selected-Q contract, pseudo-time HJB integration contract, final Bellman-residual criterion and failure taxonomy remain frozen authority.

## Issue #56 theory ceiling — still explicit

The unresolved

`UNBOUNDED-CONTROL NUMERICAL-SCHEME / STATE-CONSTRAINT CONVERGENCE-APPLICATION BLOCK`

remains accepted and unsolved. Issue #58 provides concrete production-iteration evidence for one manifestation of that block: loss of the `p_b>0` effective domain before convergence.

## Current scientific decision point

The next gate must not be SCC/global-Q/KFE yet. The immediate route decision concerns a scientifically controlled **effective-domain-preserving HJB numerical stabilization / invariant-region diagnostic**.

Possible future mechanisms may include damping, pseudo-time-step control, continuation/policy-update stabilization, or another monotonicity/effective-domain-preserving construction, but **none is authorized yet** and no method may be selected by silent tuning.

## Frozen household / same-process authority

Accepted household oracle remains immutable/read-only:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Binding law:

```text
HJB boundary policy <=> KFE boundary transition law
Q backward
future KFE exactly Q^T
Q_ij>=0 for i!=j
Q_ii=-sum of ACTUAL represented outgoing rates
Q1=0 by construction
same selected candidate/rates for HJB score and Q
```

Stationary KFE remains **NOT AUTHORIZED**.

## Hard ceiling while route decision is pending

No Builder work is authorized. Do not run KFE/stationary KFE, SCC/global-Q validation, production `W_max`, Wmax/resolution sweeps, broad parameter sweeps, aggregates/GE/multi-region/neural/nominal/calibration/policy/welfare/Results, or any tuning intended to manufacture HJB convergence.

## Current governance files

- `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
- `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
- Issue #58 body/comments.
