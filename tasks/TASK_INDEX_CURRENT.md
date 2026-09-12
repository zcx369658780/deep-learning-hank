# Deep Learning + HANK Task Index

Status: `ACTIVE_BUILDER_ISSUE_59__DLH_5VK_FIXED_HOUSEHOLD_PRICE_ENVELOPE_DIAGNOSTIC`

Last synchronized: 2026-09-12

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

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

Authoritative activation comment:

`5646298166`

Builder authority becomes operative only after the activation-ID synchronization and final activation-refresh comment confirm the post-sync live main.

## Latest accepted task — Issue #58 / DLH-5V-J

Issue #58 is CLOSED completed at accepted Terminal B.

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

Accepted evidence remains frozen: Gate 1A PASS; Gate 2 PASS; first-iteration selected-Q conservative/deterministic; Gate-3 smoke exits `p_b>0` effective domain at iteration 2 (F3 `(13,13)`, `z=0`, `p_b≈-0.365224`) and correctly raises `DERIVATIVE_EFFECTIVE_DOMAIN_FAILURE` before raw candidate/bracket search.

## Active scientific object — fixed household, fixed domain, external-price envelope

Issue #59 tests the Owner's empirical hypothesis that HJB convergence is materially conditioned by the external equilibrium-input region even when the household equations/parameters/domain are held fixed.

The active diagnostic varies only bounded, predeclared cases in `(r_a,r_b,w)` while freezing:

- household preference/adjustment parameters;
- solver tolerances and initialization within each diagnostic solver;
- accepted legacy rectangle `a∈[0,10]`, `b∈[-2,5]` with `b_max=5`;
- selected-Q validation geometry `m=1`, `W_max=10`;
- no stabilization mechanism.

Legacy-oracle HJB and current selected-Q HJB are compared only as separately fixed-geometry diagnostics. Raw convergence differences are not automatically attributed to geometry.

No KFE/distribution `g` is authorized in this gate.

## Frozen household / same-process authority

Accepted household oracle remains immutable/read-only:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Accepted selected-Q implementation also remains read-only:

`src/deep_learning_hank/two_asset/boundary_hjb_selected_q.py`

Binding law remains:

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

## Hard ceiling

Issue #59 is diagnostic only. It does not authorize source/oracle mutation, selected-Q mutation, damping/line-search/continuation/pseudo-time adaptation, variation of `b_max`/`W_max`/resolution, household-parameter tuning, KFE/stationary KFE, distribution `g`, SCC/global-Q validation, aggregates/GE/multi-region/neural/nominal/calibration/policy/welfare/Results, PR/merge/close/successor/self-accept.

## Current governance files

- `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
- `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
- Issue #59 body/comments.
