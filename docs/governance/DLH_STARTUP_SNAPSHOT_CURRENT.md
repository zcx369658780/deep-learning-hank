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

**NEXT ACTIVE — Issue #62 / DLH-5V-N**, NOT YET OPERATIVE.

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

Builder must not begin until CURRENT records this activation ID and a final authoritative activation-refresh comment confirms the post-sync live `main`. Builder execution remains **NOT YET OPERATIVE** until then.

Scientific boundary (binding):

- the ONLY object is the local continuous resolvent/domain-margin geometry at the Issue #61 last accepted state with frozen `Q_*`, `u_*`;
- no third HJB iterate is accepted;
- no multi-step continuation/homotopy;
- no extension of the Issue #61 discrete delta ladder as the experiment;
- no change to economics / prices / grid / domain / `PB_MARGIN`;
- household oracle, selected-Q source, and the accepted Issue #61 implementation are all read-only;
- Stationary KFE remains **NOT AUTHORIZED**.

## Latest accepted gate — Issue #61 / DLH-5V-M

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

Accepted interpretation (trajectory-bounded):

- the adaptive pseudo-time/resolvent route accepted 2 positive-domain iterations on the frozen central trajectory;
- at the third update request every authorized delta on the ladder {1000·2^-k, k=0..20} is infeasible (the smallest-delta limiting failure is at F3 (13,13), z=1);
- this does NOT prove global nonexistence or uniqueness of a positive-domain HJB fixed point;
- it does NOT exclude another basin, a continuation/homotopy path, or another fixed-point-preserving operator;
- the R1 fail-closed non-finite-boundary handling is part of the accepted implementation;
- together with Issue #60 value damping, the two tested stabilization routes are BOTH negative evidence on the frozen central selected-Q case.

## Prior accepted gate — Issue #60 / DLH-5V-L

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

Issue #62 measures the local continuous resolvent/domain-margin geometry at the frozen Issue #61 last accepted state: does the frozen selected-Q resolvent possess a strictly positive local effective-domain-safe step below the Issue #61 ladder floor, and what is the local domain-margin geometry? This distinguishes ladder-floor exhaustion (smaller positive continuous delta locally feasible) from a deeper local operator/domain pathology (non-finite, inconsistent, or no reproducible positive local step).

Frozen terminal-state provenance (exactly the accepted Issue #61 configuration):

```text
m=1
W_max=10
b_min=-2
a_max=10
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
n_c=n_d=9
bracket expansion x4 max 3
PB_MARGIN=1e-12
```

Reconstruct the accepted Issue #61 trajectory deterministically and STOP at its last accepted state after exactly 2 accepted updates; verify the reconstruction reproduces the accepted Issue #61 trace and terminal-state boundary minimum. At this frozen `V_*`, build selected policy / utility / conservative backward `Q_*` exactly once; the same frozen `(V_*, Q_*, u_*)` is used for every local delta evaluation; no policy re-selection as delta varies.

Equivalent continuous resolvent representation (well-defined at delta=0):

```text
[I + delta*(rho I - Q_*)] V(delta) = V_* + delta*u_*
V(0) = V_*
```

Required local diagnostics: exact infinitesimal direction `dV/delta|_0 = u_* + Q_* V_* - rho V_*`; directional derivatives `dp_b/delta|_0` for every required non-F0 boundary state; first-order margin-crossing predictions `delta_margin_linear = (p_b(V_*) - PB_MARGIN)/(-dp_b/delta|_0)` for all negative-direction states; the minimum positive finite `delta_margin_linear` and its state. Then one deterministic bracketed continuous root solve of `g(delta) = min_required_boundary p_b(V(delta)) - PB_MARGIN` on the fixed bracket `[0, 1000*2^-20]` (scipy.optimize.brentq or equivalent), verifying `g(0) > 0` and `g(1000*2^-20) < 0` first. Record bracket endpoints, reproducible root `delta_cross`, `g(delta_cross)`, worst state at/near the root, direct verification at `(1-eps)*delta_cross` and `(1+eps)*delta_cross` with fixed `eps=1e-6` when inside the bracket, ratio `delta_cross/(1000*2^-20)`, and the ratio to the minimum finite first-order `delta_margin_linear` when both are well-defined.

Non-finite required boundary evidence or non-finite directional evidence must fail closed and be surfaced explicitly. The linear prediction is a local diagnostic only, not a theorem of the nonlinear continuous-delta path. A bracketed root is a reproducible sign-changing crossing of the global boundary margin on the frozen local operator — NOT a claim of global uniqueness or of the first positive crossing unless further evidence proves it.

Execute exactly: ONE deterministic reconstruction of the accepted Issue #61 trajectory; ONE local infinitesimal-direction diagnostic; ONE bracketed continuous crossing solve on `[0, 1000*2^-20]`; ONE deterministic repeat of the full local diagnostic. No additional price case, no Wmax/resolution variation, no alternative margin, no alternative terminal state.

## Frozen household / same-process authority

Accepted household oracle remains immutable/read-only:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Accepted selected-Q source remains immutable/read-only:

`src/deep_learning_hank/two_asset/boundary_hjb_selected_q.py`

Git blob:

`7ea342ccbe15d852b90743b14bb4b02977c2d78b`

Accepted Issue #61 implementation remains read-only evidence:

`src/deep_learning_hank/two_asset/adaptive_resolvent_hjb.py`

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

No accepted third HJB iterate, no multi-step continuation/homotopy, no extension of the Issue #61 discrete ladder as the experiment, no alternative margin / price / grid / domain, no KFE/stationary KFE, no SCC/global-Q, no production Wmax/resolution, no GE/multi-region/neural/nominal/calibration/policy/welfare/Results.

## Current authoritative files

- `tasks/TASK_INDEX_CURRENT.md`
- `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
- Issue #62 body/comments.
