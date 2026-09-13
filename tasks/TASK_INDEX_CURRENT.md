# Deep Learning + HANK Task Index

Status: `NO_ACTIVE_BUILDER_ISSUE`

Last synchronized: 2026-09-13

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

**NO ACTIVE BUILDER ISSUE.** Issue #62 / DLH-5V-N is ACCEPTED / CLOSED at
Outcome A. The local geometry question is resolved: a strictly positive
sub-floor local safe step exists and the continuous margin crossing is
reproducible on the frozen Issue #61 terminal operator.

Next scientific route: **OWNER / ChatGPT SCIENTIFIC DESIGN REQUIRED**.
A continuation / trust-region / pseudo-transient successor is
**NOT YET AUTHORIZED** (no successor Issue, no Builder scientific branch, no
continuous continuation / trust-region / pseudo-transient iteration, no
accepted new HJB iterate).

## Latest accepted task — Issue #62 / DLH-5V-N

Issue #62 is CLOSED completed at Outcome A.

Accepted candidate / integration:

`7ba2d75978033064c588230b15d760b60bec9e00`

Reviewer acceptance:

`5652208157`

Acceptance integration:

`5652209372`

Accepted verdict:

`DLH_5VN_ACCEPTED__OUTCOME_A_CONFIRMED__POSITIVE_SUBFLOOR_LOCAL_SAFE_STEP_AND_REPRODUCIBLE_MARGIN_CROSSING__CONTINUATION_DESIGN_GATE_READY`

Accepted terminal:

`DLH_5VN_LOCAL_RESOLVENT_GEOMETRY__POSITIVE_SUBFLOOR_SAFE_STEP_AND_REPRODUCIBLE_MARGIN_CROSSING__CONTINUATION_DESIGN_GATE_READY`

Accepted scientific interpretation (trajectory-bounded / local evidence):

- the Issue #61 terminal event is identified as authorized **ladder-floor
  exhaustion**;
- the frozen Issue #61 terminal operator possesses a strictly positive
  sub-floor local safe delta;
- the continuous margin crossing is reproducible inside the fixed bracket
  `[0, 1000·2^-20]`;
- `delta_cross ≈ 7.8246e-4`;
- `delta_cross / old ladder floor ≈ 0.8205`;
- first-order prediction `delta_margin_linear ≈ 7.5943e-4`;
- `delta_cross / delta_margin_linear ≈ 1.0303`;
- the limiting state near root / below / above is F3 (13,13), z=1;
- corrected directional accounting: 186 required boundary states, 105
  negative-direction, and 40 `i == 0` V-independent states with
  `dp_b/delta|_0` exactly 0;
- the R1 true fail-closed non-finite handling is part of the accepted
  implementation;
- this is trajectory-bounded / local evidence only: it does NOT prove global
  uniqueness, does NOT prove the mathematically first positive crossing, does
  NOT prove any actual next HJB iterate is acceptable, does NOT prove
  continuation convergence, and does NOT authorize KFE / stationary KFE.

## Prior accepted task — Issue #61 / DLH-5V-M

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

Git blob:

`043e146ef499e985a49d256c4cec2f397f93e4e1`

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

No successor issue is authorized yet; no continuous continuation / trust-region /
pseudo-transient iteration, no accepted new HJB iterate, no extension of any
delta ladder as an experiment, no new price / grid / margin experiments, no
KFE/stationary KFE, no SCC/global-Q, no GE/multi-region/neural/nominal/
calibration/policy/welfare/Results work may start before an Owner/ChatGPT
scientific design and a new authorized Issue.

## Current governance files

- `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
- `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
- Issue #62 body/comments (accepted/closed).
