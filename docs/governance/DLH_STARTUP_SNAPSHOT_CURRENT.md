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

**Issue #47 — DLH-5U: Freeze W1 face-adapted finite-volume same-process discretization**

Task type:

`SCIENTIFIC_DESIGN__W1_FACE_ADAPTED_FINITE_VOLUME_SAME_PROCESS_DISCRETIZATION`

Dedicated branch:

`dsh/issue-47-dlh-5u-w1-face-adapted-fv-design-2026-09-03`

Builder authority becomes active only while Issue #47 remains OPEN, Task Index / Startup identity matches, and the authoritative activation comment is present.

Current master roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`

## Latest accepted gate — Issue #46 / DLH-5T

Issue #46 is CLOSED completed.

Accepted candidate:

`fa9d886ea932c2c9001b86228200a162fb1990cd`

Reviewer acceptance comment:

`5519690088`

Acceptance integration commit:

`73efb8b00b6b4884fc966f159b3aa8401cd3df41`

Acceptance level:

`L3_COMMIT_VERIFIED__SCIENTIFIC_DESIGN_ACCEPTED`

Accepted verdict:

`DLH_5T_ACCEPTED__OUTCOME_B_CONFIRMED__W_DOMAIN_AND_CONTINUOUS_SAME_PROCESS_BOUNDARY_CONTRACT_ACCEPTED__W1_TANGENTIAL_DISCRETE_PROCESS_MATCHING_REMAINS_OPEN`

Accepted terminal:

`DLH_5T_W_DOMAIN_SCIENTIFICALLY_SUPPORTED__W1_DISCRETE_PROCESS_MATCHING_REQUIRES_BOUNDED_FOLLOWUP_DESIGN`

## Owner route decision after DLH-5T

Owner selected:

`APPROVE_ROUTE_F_W1_FACE_ADAPTED_FINITE_VOLUME_OBLIQUE_FLUX_DESIGN`

The current gate therefore keeps W1/native `(a,b)` and designs a face-adapted finite-volume / oblique-flux boundary process. W1-TC and W2 are not active routes.

## Controlling household / boundary / KFE authority

Accepted household source remains immutable/read-only:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Accepted finite numerical domain family:

```text
D_W(W_max) = {
  0 <= a <= a_max,
  b >= b_min,
  a+b <= W_max
}
```

No numerical `W_max` is frozen.

Accepted continuous tangent-cone laws:

```text
a=0:          mu_a >= 0
b=b_min:      mu_b >= 0
a=a_max:      mu_a <= 0
a+b=W_max:    mu_W=mu_a+mu_b <= 0
```

Central same-process law:

```text
controlled process selected by boundary HJB
        ==
controlled process represented by KFE generator
```

Stationary KFE remains **NOT AUTHORIZED** until a discrete finite controlled process is separately designed, implemented and validated.

Contamination/pin remains downstream numerical normalization only and is not the active redesign target.

## Current DLH-5U scientific target

Resolve the DLH-5T W1 discrete blocker without moving the oblique boundary to the borrowing floor.

The critical admissible continuous pattern remains:

```text
mu_b > 0
mu_a < 0
mu_W <= 0
```

Route F must specify how a physical face-adapted control-volume process represents this inward/tangential portfolio reallocation while preserving both asset coordinates, conservation and the exact HJB/KFE discrete adjoint.

Required design objects:

1. clipped physical control volumes and actual shared faces/normals/areas;
2. physical slanted W-face semantics distinct from the staircase mask;
3. precise boundary-control/Hamiltonian location and refinement interpretation;
4. monotone conservative face-flux / CTMC transition-rate rule;
5. local symbolic tangential-reallocation consistency argument;
6. exact backward `Q V` / forward probability-mass `Q^T p` semantics;
7. explicit density/mass-matrix mapping for nonuniform clipped-cell weights;
8. downstream contamination compatibility without pin-location redesign;
9. small-cut-cell/sliver treatment or a precise future geometric admissibility rule;
10. first-order/refinement consistency toward the accepted continuous W-constrained process.

Reviewer clarifications from DLH-5T remain binding:

- no positive W-normal flux does not mean every axial component has an in-mask axial neighbor;
- one-dimensional stationary nullspace is only a future canonical uniqueness target conditional on uniqueness;
- `a_bar=1e-6` is the adjustment-cost denominator floor, not the state boundary;
- negative-`b` implementation must preserve state-dependent effective liquid return / borrowing-rate-gap semantics.

## Exact Builder allowlist

Issue #47 may create only the nine exact files named in the Issue body. No existing tracked file may be modified by Builder.

## Scientific ceiling during Issue #47

Do not:

- mutate accepted household/HJB/KFE/regional economics/source;
- implement control-volume geometry/fluxes/KKT/generator/mass matrix in source;
- run HJB, KFE, stationary density or numerical grid/domain experiments;
- choose numerical `W_max`;
- reopen b160 or alter grid/taper/economic primitives;
- run contamination/pin sensitivity;
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
6. read full Issue #47 and ALL comments, including authoritative activation;
7. read Issue #46 acceptance comment `5519690088` and accepted DLH-5T package;
8. read Issue #27 KFE contract and accepted household source read-only as needed;
9. verify Issue / Task Index / Startup identity exactly;
10. create the exact dedicated branch from fresh synchronized main;
11. create only the nine Issue #47 allowlist files;
12. perform design-only work — no implementation or solver/grid execution;
13. explicit-stage only allowlist paths, commit/push, and STOP for fresh ChatGPT review.

Chat text is not Builder authority.
