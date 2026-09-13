# Deep Learning + HANK Startup Snapshot — CURRENT

Date: 2026-09-13

Repository: `zcx369658780/deep-learning-hank`

Local Owner-designated workspace: `D:\deep-learning-hank`

## Governance state

- live GitHub `main` = synchronized repository/code/governance authority;
- open GitHub Issue = sole DSH Builder task authority only after publication + CURRENT synchronization + authoritative activation comments;
- DSH = bounded Builder/scientific analyst only under an active Issue;
- ChatGPT = independent reviewer / scientific-route advisor / task issuer / governance operator;
- Owner = final scientific authority;
- Builder completion is not acceptance.

Priority:

`Scientific correctness > Experiment reproducibility > Research iteration speed > Git auditability > Documentation completeness`

## Current Builder state

**NEXT ACTIVE — Issue #61 / DLH-5V-M**, NOT YET OPERATIVE.

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

Builder must not begin until CURRENT records this activation ID and a final authoritative activation-refresh comment confirms the post-sync live `main`. Builder execution remains **NOT OPERATIVE** until then.

Reference handoff:

`docs/handoffs/DLH_SESSION_HANDOFF_POST_5VL_2026_09_13.md`

## Latest accepted gate — Issue #60 / DLH-5V-L

Issue #60 is CLOSED completed at Terminal C.

Accepted candidate / integration:

`9b1538feabe2cc4634653721e725ee3e46d449bb`

Reviewer acceptance:

`5650057012`

Acceptance integration:

`5650059195`

Accepted verdict:

`DLH_5VL_ACCEPTED__TERMINAL_C_CONFIRMED__VALUE_UPDATE_ONLY_INVARIANT_SAFEGUARD_FAILS_ON_FROZEN_CENTRAL_TRAJECTORY__RAW_OPERATOR_ROUTE_RECONSIDERATION_REQUIRED`

Accepted interpretation:

- pure value-update damping preserves the positive-`p_b` domain for a short path but is not a viable convergence route on the frozen central trajectory;
- 17 accepted iterations remain in-domain, then no authorized dyadic value-damping step exists;
- this is trajectory-bounded evidence only and does NOT prove global nonexistence of a positive-domain HJB fixed point;
- external-price sensitivity from Issue #59 remains real but does not resolve the selected-Q invariant-domain problem.

## Next active diagnostic route

Issue #61 tests whether adapting the pseudo-time/resolvent parameter `delta` INSIDE the implicit solve preserves the accepted boundary effective domain, instead of damping an already-computed `delta=1000` value update.

Frozen central case:

```text
m=1
W_max=10
r_a=0.07
r_b=0.02
w=1.00
borrowing_rate_gap=0
rho=0.02
gamma_c=2
phi=5
chi_0=0.1
chi_1=2
a_bar=1e-6
tau=0.15
z=[0.8,1.3]
delta=1000
tolerance_iter=1e-7
tolerance_Bellman=1e-3
max_iterations=1000
n_c=n_d=9
```

Authorized adaptive resolvent only:

```text
[(1/delta + rho)I - Q(V_old)] V_delta = u(V_old) + V_old/delta
delta_k = 1000*2^-k, k = 0..20, descending
choose the largest delta whose V_trial satisfies all required boundary p_b > 1e-12
accept V_trial directly — NO additional value damping
```

The `1e-12` margin is an iterate-acceptance tolerance only; no derivative clipping/flooring is allowed and the margin never enters FOCs or Bellman scoring.

Exactly one adaptive-resolvent run and one deterministic repeat are authorized. Final PASS requires the accepted final Bellman residual criterion, not merely a tiny delta-induced update.

## Frozen household / same-process authority

Accepted household oracle remains immutable/read-only:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Accepted selected-Q source remains immutable/read-only:

`src/deep_learning_hank/two_asset/boundary_hjb_selected_q.py`

Git blob:

`7ea342ccbe15d852b90743b14bb4b02977c2d78b`

```text
HJB boundary policy <=> KFE boundary transition law
Q backward
future KFE exactly Q^T
Q_ij>=0 for i!=j
Q_ii=-sum of ACTUAL represented outgoing rates
Q1=0 by construction
same selected candidate/rates for HJB and future KFE
```

Pinning/normalization may never repair leakage.

Stationary KFE remains **NOT AUTHORIZED**.

## Interpretation ceiling

No price sweep, no alternative delta ladder/margin, no value damping, no Bellman-residual-driven delta selection, no continuation/homotopy, no hard economic bounds, no KFE/stationary KFE, no SCC/global-Q, no production Wmax/resolution, no GE/multi-region/neural/nominal/calibration/policy/welfare/Results.

## Current authoritative files

- `tasks/TASK_INDEX_CURRENT.md`
- `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
- Issue #61 body/comments.
