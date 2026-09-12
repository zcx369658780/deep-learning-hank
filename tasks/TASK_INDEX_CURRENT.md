# Deep Learning + HANK Task Index

Status: `ACTIVE_BUILDER_ISSUE_57__DLH_5VI_BOUNDARY_HJB_SCHEME_DESIGN`

Last synchronized: 2026-09-12

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

**ACTIVE — Issue #57 / DLH-5V-I.**

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

Authoritative activation comment:

`5644365170`

Builder authority exists only while Issue #57 remains OPEN, CURRENT governance agrees with this task type/branch/authority, and the final activation-refresh comment confirms the post-sync live main. Builder must fresh-fetch live `origin/main`, read all CURRENT rules plus full Issue/comments, verify the accepted household blob, and work only inside Issue #57's exact six-file allowlist.

## Latest accepted task — Issue #56 / DLH-5V-H

Issue #56 is CLOSED completed at accepted Outcome B.

Accepted candidate / integration:

`55e29523e6f1bfefab270c05113984af003ea44b`

Reviewer acceptance:

`5644186157`

Acceptance-integration / Owner route-decision comment:

`5644340159`

Accepted verdict:

`DLH_5VH_ACCEPTED__OUTCOME_B_CONFIRMED__UNBOUNDED_CONTROL_NUMERICAL_SCHEME_AND_STATE_CONSTRAINT_CONVERGENCE_APPLICATION_BLOCK_FROZEN`

Accepted terminal:

`DLH_5VH_THEORY_AUDIT_PARTIAL__ONE_BOUNDED_BOUNDARY_CONSISTENCY_OR_COMPARISON_GAP_REMAINS`

The accepted unresolved block remains explicit and frozen. It is not a blocker to the Owner-selected Route B design gate, but it may not be silently relabeled solved.

## Active scientific object — boundary-HJB implementation-ready design

Issue #57 must freeze an unambiguous design chain:

```text
represented state
 -> state-family classifier
 -> true continuously admissible controls
 -> numerical optimizer/search semantics
 -> represented destinations
 -> candidate-specific nonnegative rates from LOCAL drift
 -> candidate discrete H_h score
 -> ONE global statewise selection
 -> selected control + selected rates
 -> ONE conservative backward Q row
 -> implicit/pseudo-time HJB iteration contract
 -> convergence / residual / failure diagnostics
```

The gate is design-only. It must explicitly distinguish true economic control admissibility from any future finite numerical search brackets.

Owner empirical guidance that Kaplan-style HA HJBs are solved numerically to tolerance, with experience often showing convergence near `r_b=0.02` and roughly `0.05<r_a<0.12`, is **diagnostic guidance only**, not calibration authority or an acceptance window. No analytic value-function solution is required.

## Frozen authority

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
same selected Q for HJB and future KFE
p=M g
p_dot=Q^T p
```

Issue #54 finite-m lattice obstruction, Issue #55 strong graph obstruction, and Issue #56 accepted operator-consistency / Outcome-B ceiling remain controlling provenance.

Stationary KFE remains **NOT AUTHORIZED**.

## Hard ceiling

Issue #57 is design-only. It does not authorize solver/source mutation, production HJB execution, production-Q assembly/run, KFE/stationary execution, numerical production `W_max`, grid/domain redesign, state augmentation, coordinate transformation, aggregates/GE/multi-region/neural/nominal/calibration/policy/welfare/Results, PR/merge/close/successor/self-accept.

## Current governance files

- `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
- `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
- Issue #57 body/comments.
