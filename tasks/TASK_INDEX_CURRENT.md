# Deep Learning + HANK Task Index

Status: `ACTIVE_BUILDER_ISSUE_61__DLH_5VM_ADAPTIVE_PSEUDO_TIME_RESOLVENT_DIAGNOSTIC`

Last synchronized: 2026-09-13

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

**NEXT ACTIVE — Issue #61 / DLH-5V-M**, subject to final authoritative activation-refresh comment.

Initial authoritative activation comment:

`5650244803`

Governance synchronization blocker record:

`5650249190`

Title:

`DLH-5V-M: Adaptive pseudo-time / resolvent safeguard diagnostic on the central selected-Q HJB case`

Task type:

`SCIENTIFIC_NUMERICAL_DIAGNOSTIC__ADAPTIVE_PSEUDO_TIME_RESOLVENT_EFFECTIVE_DOMAIN`

Authority marker:

`DLH_5VM_ADAPTIVE_RESOLVENT_DIAGNOSTIC_AUTHORIZED`

Dedicated future Builder branch:

`dsh/issue-61-dlh-5vm-adaptive-resolvent-2026-09-13`

Builder authority becomes operative ONLY after all three CURRENT governance files are synchronized to Issue #61, this activation ID is recorded here, and a final authoritative activation-refresh comment confirms the post-sync live `main`. Until then Builder execution remains **NOT OPERATIVE**.

Reference handoff:

`docs/handoffs/DLH_SESSION_HANDOFF_POST_5VL_2026_09_13.md`

## Latest accepted task — Issue #60 / DLH-5V-L

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

## Next active scientific object — adaptive pseudo-time / resolvent safeguard

Issue #61 tests exactly one controlled numerical mechanism on the single frozen central selected-Q case: adapt the pseudo-time/resolvent parameter `delta` INSIDE the implicit solve, instead of damping an already-computed `delta=1000` value update.

```text
[(1/delta + rho)I - Q(V_old)] V_delta = u(V_old) + V_old/delta
delta_k = 1000*2^-k, k = 0..20, descending
choose the largest delta whose V_trial satisfies all required boundary p_b > 1e-12
accept V_trial directly — NO additional value damping
```

At a fixed point `V_delta = V_old = V`, any positive `delta` cancels and the target remains `rho V = u(V) + Q(V)V`; this changes the numerical path only, not household economics or the target HJB equation.

Frozen central case includes `m=1`, `W_max=10`, `r_a=0.07`, `r_b=0.02`, `w=1`, `gap=0`, `delta=1000` reference, accepted Issue #58 tolerances/search settings.

Exactly one adaptive-resolvent run + one deterministic repeat are authorized. No price sweep, no alternative delta ladder/margin, no continuation/homotopy, no value damping.

## Frozen household / same-process authority

Accepted household oracle remains immutable/read-only:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Accepted selected-Q implementation remains immutable/read-only:

`src/deep_learning_hank/two_asset/boundary_hjb_selected_q.py`

Git blob:

`7ea342ccbe15d852b90743b14bb4b02977c2d78b`

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

Issue #61 does not authorize mutation of accepted solvers, price sweeps, alternative delta ladders/margins, value damping, Bellman-residual-driven delta selection, continuation/homotopy, hard control bounds, KFE/stationary KFE, SCC/global-Q, production Wmax/resolution, GE, multi-region, neural, nominal, calibration, policy, welfare, or Results work.

## Current governance files

- `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
- `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
- Issue #61 body/comments.
