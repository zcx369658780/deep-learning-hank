# Deep Learning + HANK Startup Snapshot — CURRENT

Date: 2026-09-12

Repository: `zcx369658780/deep-learning-hank`

Local Owner-designated workspace: `D:\deep-learning-hank`

## Governance state

- live GitHub `main` = synchronized repository/code/governance authority;
- open GitHub Issue = sole DSH Builder task authority only after publication + CURRENT synchronization + authoritative activation comment;
- DSH = bounded Builder/scientific analyst only under an active Issue;
- ChatGPT = independent reviewer / scientific-route advisor / task issuer / governance operator;
- Owner = final scientific authority;
- Builder completion is not acceptance.

Priority:

`Scientific correctness > Experiment reproducibility > Research iteration speed > Git auditability > Documentation completeness`

## Current Builder state

**ACTIVE — Issue #59 / DLH-5V-K.**

Title:

`DLH-5V-K: Diagnose fixed-household external-price convergence envelope before HJB stabilization`

Task type:

`SCIENTIFIC_DIAGNOSTIC__FIXED_HOUSEHOLD_EXTERNAL_PRICE_CONVERGENCE_ENVELOPE`

Owner decision:

`APPROVE_FIXED_HOUSEHOLD_EXTERNAL_PRICE_ENVELOPE_DIAGNOSTIC_BEFORE_STABILIZATION`

Authority marker:

`DLH_5VK_FIXED_HOUSEHOLD_PRICE_ENVELOPE_DIAGNOSTIC_AUTHORIZED`

Dedicated Builder branch:

`dsh/issue-59-dlh-5vk-fixed-household-price-envelope-2026-09-12`

Initial activation comment:

`5646298166`

Builder must wait for the final activation-refresh comment confirming the post-ID-sync live main before beginning execution.

## Latest accepted gate — Issue #58 / DLH-5V-J

Accepted candidate / integration:

`7b564d1b7d7aaf76b808135b192646e0ec1f5f08`

Reviewer acceptance:

`5646205500`

Acceptance integration:

`5646215533`

Accepted verdict:

`DLH_5VJ_ACCEPTED__TERMINAL_B_CONFIRMED__BOUNDARY_HJB_IMPLEMENTATION_PARTIAL__EFFECTIVE_DOMAIN_EXIT_FROZEN__OWNER_STABILIZATION_ROUTE_DECISION_REQUIRED`

Accepted terminal:

`DLH_5VJ_BOUNDARY_HJB_IMPLEMENTATION_PARTIAL__ONE_BOUNDED_NUMERICAL_OR_CONTRACT_GAP_REMAINS`

The accepted implementation evidence remains:

- F0 common-input local regression PASS;
- Route-A family/sector/representability algebra PASS;
- first selected backward Q conservative and deterministic;
- frozen validation HJB leaves the accepted positive-liquid-marginal effective domain at iteration 2;
- first failing state F3 `(13,13)`, `z=0`, `p_b≈-0.365224`;
- `DERIVATIVE_EFFECTIVE_DOMAIN_FAILURE` is raised before candidate/bracket search.

No final Bellman residual exists for that smoke because HJB convergence is not reached.

## Owner diagnostic route now selected

Before introducing numerical stabilization, the Owner directs the project to test a historical modeling hypothesis:

> with household equations/parameters and asset-domain bounds fixed, HJB convergence may exist only over a practical external-input region in `r_a`, `r_b`, and wage `w`; moving GE iterates outside that region can generate boundary behavior or nonconvergence even though the household model itself is unchanged.

The Owner specifically asks that asset bounds not be varied during this test. In particular:

- legacy accepted-oracle rectangle fixes `b_max=5`;
- selected-Q diagnostic fixes `m=1`, `W_max=10`;
- household preference/adjustment parameters remain frozen;
- no damping, line search, continuation or pseudo-time adaptation is introduced.

This is a hypothesis test, not an assumed explanation.

## Active diagnostic scope

Issue #59 maps a bounded sparse external-price design:

- legacy fixed rectangle: `r_a∈{0.05,0.07,0.09,0.11,0.13}` at `r_b=0.02,w=1`, plus two `r_b` and two wage sentinels; conditional maximum-four midpoint evaluations may localize an `r_a` PASS/FAIL transition only if a bracket exists;
- current selected-Q solver: fixed geometry, three `r_a` sentinels `{0.07,0.10,0.13}` at `r_b=0.02,w=1`.

The task is HJB-only. No KFE, stationary distribution `g`, or stationary aggregates are authorized.

## Frozen household / same-process authority

Accepted household oracle remains immutable/read-only:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Accepted selected-Q implementation remains read-only:

`src/deep_learning_hank/two_asset/boundary_hjb_selected_q.py`

```text
HJB boundary policy <=> KFE boundary transition law
Q backward
future KFE consumes exactly Q^T
Q_ij>=0 for i!=j
Q_ii=-sum of ACTUAL represented outgoing rates
Q1=0 by construction
same selected candidate/rates for HJB score and Q
```

Pinning/normalization may never repair leakage.

Stationary KFE remains **NOT AUTHORIZED**.

## Interpretation ceiling

Issue #59 does not authorize household/source mutation, selected-Q mutation, economic hard bounds on controls, changes in `b_max`/`W_max`/resolution during diagnostics, household-parameter tuning, numerical stabilization, KFE/stationary KFE, SCC/global-Q validation, production Wmax work, aggregates, GE, regional/neural/nominal/calibration/policy/welfare/Results, PR/merge/close/successor/self-accept.

## Current authoritative files

- `tasks/TASK_INDEX_CURRENT.md`
- `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
- Issue #59 body/comments.
