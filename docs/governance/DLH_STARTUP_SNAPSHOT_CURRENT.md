# Deep Learning + HANK Startup Snapshot — CURRENT

Date: 2026-09-12

Repository: `zcx369658780/deep-learning-hank`

Local Owner-designated workspace: `D:\deep-learning-hank`

## Governance state

- live GitHub `main` = synchronized repository/code/governance authority;
- open GitHub Issue = sole DSH Builder task authority only after publication + CURRENT synchronization + authoritative activation comment;
- DSH = bounded Builder/scientific analyst/theorist only under an active Issue;
- ChatGPT = independent reviewer / scientific-route advisor / task issuer / governance operator;
- Owner = final scientific authority;
- Builder completion is not acceptance.

Priority:

`Scientific correctness > Experiment reproducibility > Research iteration speed > Git auditability > Documentation completeness`

## Current Builder state

**ACTIVE — Issue #57 / DLH-5V-I, pending final post-sync activation comment.**

Title:

`DLH-5V-I: Freeze boundary-HJB production scheme contract under accepted Outcome-B theory ceiling`

Task type:

`SCIENTIFIC_DESIGN__BOUNDARY_HJB_SCHEME_CONTRACT_AND_IMPLEMENTATION_READINESS`

Owner decision:

`APPROVE_ROUTE_B_FREEZE_OUTCOME_B_THEORY_LIMIT_AND_PROCEED_TO_BOUNDARY_HJB_SCHEME_DESIGN`

Authority marker:

`DLH_5VI_BOUNDARY_HJB_SCHEME_DESIGN_AUTHORIZED`

Dedicated Builder branch:

`dsh/issue-57-dlh-5vi-boundary-hjb-scheme-design-2026-09-12`

Authoritative activation comment: **PENDING POST-SYNC**.

Builder must not begin until the final activation comment is posted. After activation, Builder must fresh-fetch live `origin/main`, verify Issue #57 remains OPEN, read all CURRENT rules/governance and full Issue/comments, confirm exact task type/branch/authority, verify the accepted household blob, then work only inside the six new design files authorized by Issue #57.

## Latest accepted gate — Issue #56 / DLH-5V-H

Issue #56 is CLOSED completed at accepted Outcome B.

Accepted candidate / integration:

`55e29523e6f1bfefab270c05113984af003ea44b`

Reviewer acceptance:

`5644186157`

Acceptance-integration / Owner route decision:

`5644340159`

Accepted verdict:

`DLH_5VH_ACCEPTED__OUTCOME_B_CONFIRMED__UNBOUNDED_CONTROL_NUMERICAL_SCHEME_AND_STATE_CONSTRAINT_CONVERGENCE_APPLICATION_BLOCK_FROZEN`

Accepted terminal:

`DLH_5VH_THEORY_AUDIT_PARTIAL__ONE_BOUNDED_BOUNDARY_CONSISTENCY_OR_COMPARISON_GAP_REMAINS`

The remaining unbounded-control numerical-scheme / state-constraint convergence-application block stays explicit. Owner selected Route B: preserve this theory ceiling and proceed to boundary-HJB scheme design rather than making a complete global convergence theorem an implementation prerequisite.

## Numerical-HJB interpretation

The project does **not** require a closed-form value function for the two-asset HA HJB. Kaplan-style heterogeneous-agent HJBs are treated as numerical nonlinear fixed-point/PDE problems whose future implementation evidence is iterative convergence to declared tolerance plus residual, policy, drift, regression and robustness diagnostics.

Owner empirical experience that convergence is often obtainable around `r_b=0.02` and approximately `0.05<r_a<0.12` is non-binding diagnostic guidance only. It is not calibration authority, a theorem assumption or an acceptance window.

## Continuous boundary authority remains intact

Accepted domain:

```text
D_W(W_max)={0<=a<=a_max,b>=b_min,a+b<=W_max}
a_max=10
b_min=-2
```

True active-face laws:

```text
a=0:       mu_a>=0
b=b_min:   mu_b>=0
a=a_max:   mu_a<=0
W:         mu_a+mu_b<=0
```

True household control domain remains `c>0, l>=0, d in R`, with state tangent restrictions only on actual active faces. No false global static budget constraint and no artificial hard household control bounds are authorized.

## Same-process / mass authority

Accepted household source remains immutable/read-only:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob: `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Binding law:

```text
HJB boundary policy <=> KFE boundary transition law
Q backward
Q^T forward
Q_ij>=0 for i!=j
Q_ii=-sum of ACTUAL represented outgoing rates
Q1=0 by construction
HJB and future KFE consume the SAME selected Q
p=M g
p_dot=Q^T p
```

Pinning/normalization may never repair leakage.

Stationary KFE remains **NOT AUTHORIZED**.

## Active design objective

Issue #57 must freeze an implementation-ready contract for:

- exhaustive represented-state family classification;
- true-control versus numerical-search-bracket semantics;
- derivative/effective-domain diagnostics;
- candidate-specific discrete Bellman scoring with rates generated from local drift before selection;
- ONE global statewise selection and deterministic tie handling;
- conservative selected Q-row construction;
- mapping into the accepted implicit/pseudo-time HJB iteration pattern;
- numerical convergence, residual, policy and failure diagnostics;
- a staged validation hierarchy for the next implementation gate.

No source implementation or production solve is authorized in this gate.

## Interpretation ceiling

Issue #57 is design-only. It does not authorize implementation, production-Q assembly/run, HJB/KFE/stationary solves, numerical production `W_max`, new states/ghosts, grid/aspect/domain redesign, coordinate transformation, aggregates, GE, regional/neural/nominal/calibration/policy/welfare/Results, PR/merge/close/successor/self-accept.

## Current authoritative files

- `tasks/TASK_INDEX_CURRENT.md`
- `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
- Issue #57 body/comments.
