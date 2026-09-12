# Deep Learning + HANK Task Index

Status: `ACTIVE_BUILDER_ISSUE_58__DLH_5VJ_BOUNDARY_HJB_IMPLEMENTATION_LOCAL_VALIDATION`

Last synchronized: 2026-09-12

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

**ACTIVE — Issue #58 / DLH-5V-J.**

Title:

`DLH-5V-J: Implement boundary-HJB selected-Q solver and pass local validation gates`

Task type:

`SCIENTIFIC_IMPLEMENTATION__BOUNDARY_HJB_SELECTED_Q_AND_LOCAL_VALIDATION`

Owner decision:

`APPROVE_DLH_5VJ_BOUNDARY_HJB_IMPLEMENTATION_AND_LOCAL_VALIDATION_GATE`

Authority marker:

`DLH_5VJ_BOUNDARY_HJB_IMPLEMENTATION_AND_LOCAL_VALIDATION_AUTHORIZED`

Dedicated Builder branch:

`dsh/issue-58-dlh-5vj-boundary-hjb-implementation-2026-09-12`

Authoritative activation comment:

`5644789118`

Builder authority becomes fully operative only after the final activation-refresh comment confirms the post-ID-sync live main. Builder must then fresh-fetch live `origin/main`, verify Issue #58 remains OPEN and all CURRENT governance agrees, read all CURRENT rules plus full Issue/comments, verify the accepted household blob, create/use the exact branch from fresh synchronized main, and work only inside Issue #58's exact six-path allowlist.

## Latest accepted task — Issue #57 / DLH-5V-I

Issue #57 is CLOSED completed at accepted Outcome A.

Accepted candidate / integration:

`3e450cf8ae177015e68ee7e05ecc5d6be7b2f8ec`

Reviewer acceptance:

`5644767550`

Acceptance integration:

`5644769439`

Accepted verdict:

`DLH_5VI_ACCEPTED__OUTCOME_A_CONFIRMED__BOUNDARY_HJB_SCHEME_CONTRACT_FROZEN__IMPLEMENTATION_GATE_READY_UNDER_ACCEPTED_OUTCOME_B_THEORY_CEILING`

Accepted terminal:

`DLH_5VI_BOUNDARY_HJB_SCHEME_CONTRACT_FROZEN__IMPLEMENTATION_GATE_READY_UNDER_ACCEPTED_OUTCOME_B_THEORY_CEILING`

The Issue #57 Route-A F0–F11 family classifier, candidate representability/dispatch, algorithmic-bracket semantics, Bellman ONE-selection contract, conservative selected-Q contract, pseudo-time HJB integration, final Bellman-residual criterion and validation hierarchy are frozen implementation authority.

## Issue #56 theory ceiling — still explicit

Issue #56 remains accepted at Outcome B. The unresolved

`UNBOUNDED-CONTROL NUMERICAL-SCHEME / STATE-CONSTRAINT CONVERGENCE-APPLICATION BLOCK`

is not silently solved by Issue #58. The implementation gate uses numerical convergence/residual/regression evidence under the Owner-selected Route B interpretation.

## Active scientific object — boundary-HJB implementation + bounded local validation

Issue #58 must implement and validate:

```text
finite represented D_W validation grid
 -> exact F0..F11 Route-A classifier
 -> economic admissibility + representability
 -> deterministic algorithmic search brackets
 -> candidate local drift / destinations / rates
 -> candidate Bellman score
 -> ONE deterministic global statewise selection
 -> same selected rates into conservative backward Q
 -> implicit/pseudo-time HJB iteration
 -> final re-selection on final V
 -> final Bellman residual
 -> bounded validation Gates 1A / 2 / 3
```

The accepted household oracle remains immutable/read-only:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Binding same-process law:

```text
HJB boundary policy <=> KFE boundary transition law
Q backward
future KFE exactly Q^T
Q_ij>=0 for i!=j
Q_ii=-sum of ACTUAL represented outgoing rates
Q1=0 by construction
same selected candidate/rates for HJB score and Q
```

Issue #58 may assemble the backward Q needed for the bounded HJB smoke and validate row/generator conservation. It may **not** run KFE/stationary KFE or perform the successor SCC/global stationary-generator gate.

Owner empirical guidance (`r_b≈0.02`, roughly `0.05<r_a<0.12`) remains **DIAGNOSTIC / VALIDATION only**, not calibration/theorem/acceptance authority.

Stationary KFE remains **NOT AUTHORIZED**.

## Hard ceiling

Issue #58 does not authorize stationary KFE, production `W_max`, Wmax/resolution sweeps, broad parameter sweeps, SCC/global stationary-generator validation, aggregates/GE/multi-region/neural/nominal/calibration/policy/welfare/Results, PR/merge/close/successor/self-accept.

## Current governance files

- `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
- `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
- Issue #58 body/comments.
