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

**NO ACTIVE BUILDER ISSUE.**

Issue #58 / DLH-5V-J is accepted at Terminal B and Builder STOP is binding. The project is paused for Owner / ChatGPT route selection before any successor Issue is authorized.

## Latest accepted gate — Issue #58 / DLH-5V-J

Accepted candidate / integration:

`7b564d1b7d7aaf76b808135b192646e0ec1f5f08`

Reviewer acceptance:

`5646205500`

Accepted verdict:

`DLH_5VJ_ACCEPTED__TERMINAL_B_CONFIRMED__BOUNDARY_HJB_IMPLEMENTATION_PARTIAL__EFFECTIVE_DOMAIN_EXIT_FROZEN__OWNER_STABILIZATION_ROUTE_DECISION_REQUIRED`

Accepted terminal:

`DLH_5VJ_BOUNDARY_HJB_IMPLEMENTATION_PARTIAL__ONE_BOUNDED_NUMERICAL_OR_CONTRACT_GAP_REMAINS`

Accepted evidence:

- new boundary-HJB selected-Q implementation is materially accepted;
- Gate 1A F0 common-input local regression passes;
- Gate 2 family / sector / representability / first-moment checks pass;
- iteration-1 backward Q is conservative and deterministic;
- the frozen Gate-3 smoke exits the accepted boundary effective domain at iteration 2;
- first failing state is F3 `(13,13)`, `z=0`, with effective liquid marginal `p_b≈-0.365224`;
- the implementation correctly raises `DERIVATIVE_EFFECTIVE_DOMAIN_FAILURE` **before** candidate/bracket search;
- the prior unbounded `R_DEPLETE` Bellman-score behavior is interpreted as a consequence of the invalid `p_b<=0` iterate, not as a finite-bracket root cause.

No final Bellman residual exists for this smoke because convergence is not reached.

## Scientific interpretation

The evidence does **not** refute the household HJB, the finite-domain geometry, or the accepted F3 sector algebra. It shows that the currently implemented pseudo-time/policy-update iteration can leave the positive-liquid-marginal effective domain before convergence.

This is a concrete manifestation of the already frozen Issue #56 Outcome-B:

`UNBOUNDED-CONTROL NUMERICAL-SCHEME / STATE-CONSTRAINT CONVERGENCE-APPLICATION BLOCK`.

## Next route decision — not yet authorized

The next scientific task should investigate an **effective-domain-preserving / invariant-region numerical stabilization route** before any SCC/global-Q or KFE work.

Potential classes of methods may include:

- controlled damping of value/policy updates;
- pseudo-time-step control;
- continuation or safeguarded policy iteration;
- another monotonicity/effective-domain-preserving construction.

These are candidate research directions only. No method is currently authorized, and no tuning-to-pass is permitted.

## Prior accepted design authority — Issue #57 / DLH-5V-I

Accepted candidate / integration:

`3e450cf8ae177015e68ee7e05ecc5d6be7b2f8ec`

Reviewer acceptance:

`5644767550`

Acceptance integration:

`5644769439`

Issue #57 remains the frozen production-scheme design authority: unique Route-A F0–F11 ownership, candidate representability/dispatch, algorithm-only search brackets, local-drift rates before scoring, ONE deterministic selection, conservative same-candidate Q, pseudo-time HJB integration, final Bellman residual after re-selection, and named failures with no silent fallback.

## Accepted household / same-process authority

Accepted household oracle remains immutable/read-only:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

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

## Current hard ceiling

No active Issue means no Builder work. Do not perform KFE/stationary KFE, SCC/global stationary-generator validation, production `W_max`, Wmax/resolution sweeps, broad parameter sweeps, or aggregates/GE/regional/neural/nominal/calibration/policy/welfare/Results work.

## Current authoritative files

- `tasks/TASK_INDEX_CURRENT.md`
- `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
- Issue #58 body/comments.
