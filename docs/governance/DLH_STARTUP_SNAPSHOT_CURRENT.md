# Deep Learning + HANK Startup Snapshot — CURRENT

Date: 2026-09-03

Repository: `zcx369658780/deep-learning-hank`

Local Owner-designated workspace: `D:\deep-learning-hank`

## Governance state

- live GitHub `main` = synchronized repository/code/governance authority;
- GitHub Issue = sole DSH Builder authority only after publication + Task Index / Startup synchronization + authoritative activation comment;
- DSH = bounded Builder/executor or scientific analyst only under an active Issue;
- ChatGPT = independent fresh-GitHub reviewer / scientific-route advisor / task issuer / governance operator;
- Owner = final scientific authority;
- Builder completion is not acceptance.

Priority:

`Scientific correctness > Experiment reproducibility > Research iteration speed > Git auditability > Documentation completeness`

## Current Builder state

Current published task:

**Issue #46 — DLH-5T: Freeze finite production-domain geometry and same-process HJB–KFE boundary contract**

Task type:

`SCIENTIFIC_DESIGN__FINITE_PRODUCTION_DOMAIN_AND_SAME_PROCESS_HJB_KFE_BOUNDARY_CONTRACT`

Dedicated branch:

`dsh/issue-46-dlh-5t-finite-domain-same-process-boundary-2026-09-03`

Builder authority becomes active only while Issue #46 remains OPEN, Task Index / Startup identity matches, and the authoritative activation comment is present.

Current master roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`

## Latest accepted gate — Issue #45 / DLH-5S

Issue #45 is CLOSED completed.

Accepted candidate:

`160781a89c6e22b5f17b4259500893140fcb9c01`

Reviewer acceptance comment:

`5519142363`

Acceptance integration commit:

`75bedf6e3bb97d024dc8af3afa30f7398f205846`

Acceptance level:

`L3_COMMIT_VERIFIED__SCIENTIFIC_THEORY_ANALYSIS_ACCEPTED`

Accepted verdict:

`DLH_5S_REV3_ACCEPTED__OUTCOME_B_CONFIRMED__SCALED_TAIL_STRUCTURE_ACCEPTED__P2_REALIZATION_REMAINS_OPEN`

Accepted terminal:

`DLH_5S_P2_REALIZATION_NOT_CLOSED__SCALED_TAIL_TIGHTNESS_OR_BRANCH_SELECTION_REMAINS_UNPROVED__OWNER_ROUTE_DECISION_REQUIRED`

## Owner decision after DLH-5S

Owner selected Route D:

`APPROVE_ROUTE_D_FINITE_PRODUCTION_DOMAIN_AND_JOINT_HJB_KFE_BOUNDARY_DESIGN`

The current gate is therefore finite-domain scientific design, not additional infinite-domain proof and not stationary KFE execution.

## Controlling household / KFE authority

Accepted household source remains immutable/read-only:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Issue #27 remains binding:

```text
HJB boundary policy <=> KFE boundary transition law
```

Contamination/pin-row interpretation remains accepted:

- singularity of a conservative generator is expected;
- MATLAB-style row contamination is a numerical normalization device in principle;
- later stationary acceptance still requires the ORIGINAL `Q^T g` residual, normalization and admissibility checks;
- contamination is not the active redesign target of Issue #46.

Stationary KFE remains **NOT AUTHORIZED**.

## DLH-5T scientific target

Primary candidate finite production domain:

```text
D_W(W_max) = {
  0 <= a <= a_max,
  b >= b_min,
  a+b <= W_max
}
```

`W_max` is a numerical truncation parameter, not a household primitive. No numerical `W_max` is selected in this Issue.

Primary representation candidate:

`W1 = native (a,b) tensor coordinates with mask a+b<=W_max`.

Boundary conditions to derive/audit/freeze:

```text
a=0:          mu_a >= 0
b=b_min:      mu_b >= 0
a=a_max:      mu_a <= 0
a+b=W_max:    mu_W=mu_a+mu_b <= 0
```

All active constraints apply jointly at feasible face intersections.

Central Route-D law:

```text
controlled process selected by boundary HJB
        ==
controlled process represented by KFE generator
```

The HJB must select boundary controls from the constrained Hamiltonian/KKT problem itself. KFE-only clipping or silent suppression of a materially outward HJB policy is forbidden.

## Wmax adequacy design scope

DLH-5T freezes the later selection protocol, not the number. A successor nested-domain protocol must distinguish:

- HJB shared-interior policy stability;
- artificial-boundary influence localization;
- future stationary-tail influence;
- future aggregate stability `C,L,A,B`;
- future GE/anchor stability.

## Exact Builder allowlist

Issue #46 may create only the eight paths frozen in the Issue body:

- one design document under `docs/design/`;
- seven exact reports under `reports/dlh_5t_finite_production_domain_same_process_boundary_2026_09_03/`.

No existing tracked file may be modified by Builder.

## Scientific ceiling during Issue #46

Do not:

- mutate accepted household/HJB/KFE/regional source;
- run HJB, KFE, stationary density or grid/domain experiments;
- choose a numerical `W_max`;
- reopen b160 or alter grid/taper/economic primitives;
- implement W1 masking/KKT boundary controls/conservative generator;
- run contamination sensitivity;
- compute stationary aggregates;
- rebuild two-region GE;
- run multi-province execution or neural training;
- enter nominal HANK, calibration, policy, welfare or Results;
- PR / merge / Issue close / successor Issue / self-accept from Builder.

## DSH startup sequence

1. `Set-Location D:\deep-learning-hank`;
2. verify repository / remote / worktree / staging;
3. `git fetch origin` and record fresh `origin/main`;
4. read all CURRENT project rules;
5. read CURRENT Task Index, this Startup Snapshot and Roadmap;
6. read full Issue #46 and ALL comments, including authoritative activation;
7. read Issue #45 acceptance and accepted DLH-5M / Issue #27 / DLH-5E design-evidence as required;
8. verify Issue / Task Index / Startup identity exactly;
9. create the exact dedicated branch from fresh synchronized main;
10. create only the eight Issue #46 allowlist files;
11. perform design-only work — no solver/grid execution;
12. explicit-stage only allowlist paths, commit/push, and STOP for fresh ChatGPT review.

Chat text is not Builder authority.
