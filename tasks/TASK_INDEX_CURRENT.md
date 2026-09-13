# Deep Learning + HANK Task Index

Status: `ACTIVE_BUILDER_ISSUE_62__DLH_5VN_LOCAL_RESOLVENT_DOMAIN_GEOMETRY_DIAGNOSTIC`

Last synchronized: 2026-09-13

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

**NEXT ACTIVE — Issue #62 / DLH-5V-N**, subject to final authoritative activation-refresh comment.

Initial authoritative activation comment:

`5651730413`

Title:

`DLH-5V-N: Diagnose local continuous resolvent/domain-margin geometry at the Issue #61 terminal accepted state`

Task type:

`SCIENTIFIC_NUMERICAL_DIAGNOSTIC__LOCAL_CONTINUOUS_RESOLVENT_DOMAIN_GEOMETRY`

Owner / Reviewer route decision:

`APPROVE_LOCAL_CONTINUOUS_RESOLVENT_DOMAIN_GEOMETRY_DIAGNOSTIC_AFTER_5VM_TERMINAL_C`

Authority marker:

`DLH_5VN_LOCAL_RESOLVENT_DOMAIN_GEOMETRY_DIAGNOSTIC_AUTHORIZED`

Dedicated future Builder branch:

`dsh/issue-62-dlh-5vn-local-resolvent-geometry-2026-09-13`

Builder authority becomes operative ONLY after all three CURRENT governance files are synchronized to Issue #62, this activation ID is recorded here, and a final authoritative activation-refresh comment confirms the post-sync live `main`. Until then Builder execution remains **NOT YET OPERATIVE**.

Scientific boundary (binding):

- the ONLY object is the local continuous resolvent/domain-margin geometry at the Issue #61 last accepted state with frozen `Q_*`, `u_*`;
- no third HJB iterate is accepted;
- no multi-step continuation/homotopy;
- no extension of the Issue #61 discrete delta ladder as the experiment;
- no change to economics / prices / grid / domain / `PB_MARGIN`;
- household oracle, selected-Q source, and the accepted Issue #61 implementation are all read-only;
- Stationary KFE remains **NOT AUTHORIZED**.

## Latest accepted task — Issue #61 / DLH-5V-M

Issue #61 is CLOSED completed at Terminal C.

Accepted candidate / integration:

`2721dadbfd0ad49813f12c8424f6be77fcaf3f85`

Reviewer acceptance:

`5651495744`

Acceptance integration:

`5651496951`

Accepted verdict:

`DLH_5VM_ACCEPTED__TERMINAL_C_CONFIRMED__ADAPTIVE_RESOLVENT_LADDER_EXHAUSTED_ON_FROZEN_CENTRAL_TRAJECTORY__ROUTE_RECONSIDERATION_REQUIRED`

Accepted terminal:

`DLH_5VM_ADAPTIVE_RESOLVENT__NO_VIABLE_EFFECTIVE_DOMAIN_RESOLVENT_STEP__ROUTE_RECONSIDERATION_REQUIRED`

Accepted scientific interpretation (trajectory-bounded):

- the adaptive pseudo-time/resolvent route accepted 2 positive-domain iterations on the frozen central trajectory;
- at the third update request every authorized delta on the ladder {1000·2^-k, k=0..20} is infeasible (the smallest-delta limiting failure is at F3 (13,13), z=1);
- this does NOT prove global nonexistence or uniqueness of a positive-domain HJB fixed point;
- it does NOT exclude another basin, a continuation/homotopy path, or another fixed-point-preserving operator;
- the R1 fail-closed non-finite-boundary handling is part of the accepted implementation;
- together with Issue #60 value damping, the two tested stabilization routes are BOTH negative evidence on the frozen central selected-Q case.

## Prior accepted task — Issue #60 / DLH-5V-L

Issue #60 is CLOSED completed at Terminal C.

Accepted candidate / integration:

`9b1538feabe2cc4634653721e725ee3e46d449bb`

Reviewer acceptance:

`5650057012`

Acceptance integration:

`5650059195`

Accepted verdict:

`DLH_5VL_ACCEPTED__TERMINAL_C_CONFIRMED__VALUE_UPDATE_ONLY_INVARIANT_SAFEGUARD_FAILS_ON_FROZEN_CENTRAL_TRAJECTORY__RAW_OPERATOR_ROUTE_RECONSIDERATION_REQUIRED`

Accepted scientific interpretation:

- pure value-update damping preserves the positive-`p_b` domain for a short path but is not a viable convergence route on the frozen central trajectory;
- 17 accepted iterations remain in-domain, then no authorized dyadic value-damping step exists;
- this is trajectory-bounded evidence only and does NOT prove global nonexistence of a positive-domain HJB fixed point;
- external-price sensitivity from Issue #59 remains real but does not resolve the selected-Q invariant-domain problem.

## Frozen household / same-process authority

Accepted household oracle remains immutable/read-only:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Accepted selected-Q implementation remains immutable/read-only:

`src/deep_learning_hank/two_asset/boundary_hjb_selected_q.py`

Git blob:

`7ea342ccbe15d852b90743b14bb4b02977c2d78b`

Accepted Issue #61 implementation remains read-only evidence:

`src/deep_learning_hank/two_asset/adaptive_resolvent_hjb.py`

Binding law remains:

```text
HJB boundary policy <=> KFE boundary transition law
Q backward
future KFE exactly Q^T
Q_ij>=0 for i!=j
Q_ii=-sum of ACTUAL represented outgoing rates
Q1=0 by construction
same selected candidate/rates for HJB and future KFE
```

Stationary KFE remains **NOT AUTHORIZED**.

## Hard ceiling

Issue #62 does not authorize accepting a third HJB iterate, multi-step continuation/homotopy, extension of the Issue #61 discrete delta ladder, mutation of accepted solvers/implementations, price sweeps, alternative margins, hard control bounds, KFE/stationary KFE, SCC/global-Q, production Wmax/resolution, GE, multi-region, neural, nominal, calibration, policy, welfare, or Results work.

## Current governance files

- `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
- `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
- Issue #62 body/comments.
