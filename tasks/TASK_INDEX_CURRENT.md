# Deep Learning + HANK Task Index

Status: `ACTIVE_BUILDER_ISSUE__DLH_5V_RESTRICTED_VORONOI_TANGENTIAL_MOMENT_CONE_DESIGN`

Last synchronized: 2026-09-03

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

Current Issue:

**Issue #48 — OPEN**

Title:

`DLH-5V: Restricted-Voronoi W-frontier tangential moment-cone and same-process transition design`

Task type:

`SCIENTIFIC_DESIGN__RESTRICTED_VORONOI_TANGENTIAL_MOMENT_CONE_AND_SAME_PROCESS_TRANSITIONS`

Dedicated branch:

`dsh/issue-48-dlh-5v-voronoi-tangential-moment-cone-2026-09-03`

Issue #48 becomes the sole DSH Builder authority only while it remains OPEN, CURRENT Task Index / Startup identity matches, and the authoritative activation comment is present. Chat text alone does not create Builder authority.

## Latest accepted task — Issue #47 / DLH-5U

Accepted Rev-1 candidate:

`81bf9b46f20e6dd96514bb6fad698097c917a948`

Reviewer acceptance comment:

`5521379228`

Acceptance integration commit:

`060c2835825f9efff4f89c84646f04cab6a9c8a4`

Accepted verdict:

`DLH_5U_REV1_ACCEPTED__OUTCOME_B_CONFIRMED__ROUTE_F_FRAMEWORK_ACCEPTED__TANGENTIAL_SAME_PROCESS_CONSISTENCY_REMAINS_THE_SINGLE_BOUNDED_OPEN_OBJECT`

Accepted terminal:

`DLH_5U_ROUTE_F_SCIENTIFICALLY_VIABLE__ONE_BOUNDED_DISCRETE_GEOMETRY_OR_WEIGHTED_ADJOINT_OBJECT_REMAINS_UNRESOLVED`

## Owner continuation decision

Owner approved:

`APPROVE_DLH_5V_RESTRICTED_VORONOI_TANGENTIAL_MOMENT_CONE_DESIGN`

Scientific meaning:

- retain W1/native `(a,b,z)` and the accepted finite W-domain;
- retain restricted-Voronoi control volumes induced only by represented W1 nodes;
- analyze the actual W-frontier Voronoi adjacency / neighbor-displacement cone, including oblique neighbors;
- determine whether nonnegative CTMC rates can reproduce the accepted tangential reallocation cone and exact sliding benchmark;
- distinguish strict source-state face-flux consistency from more general boundary-local nonnegative moment matching;
- preserve one-`Q` HJB/KFE same-process semantics;
- use fail-closed geometric admissibility for sliver/degenerate phases in this gate;
- remain design-only: no implementation, solver execution, stationary KFE, or numerical `W_max`.

## Controlling accepted objects

Accepted household source remains immutable/read-only:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Binding law:

```text
HJB boundary policy <=> KFE boundary transition law
```

Stationary KFE remains **NOT AUTHORIZED**.

Accepted finite domain / tangent law:

```text
D_W(W_max) = {0<=a<=a_max, b>=b_min, a+b<=W_max}

a=0:          mu_a >= 0
b=b_min:      mu_b >= 0
a=a_max:      mu_a <= 0
a+b=W_max:    mu_W=mu_a+mu_b <= 0
```

Accepted restricted-Voronoi cell:

```text
C_s = {x in D_W : ||x-s|| <= ||x-r|| for all represented r}
```

Actual W-face activity is determined by `F_s^W = partial(C_s) intersect {a+b=W_max}` with positive length.

## Current DLH-5V target

For every recurring nondegenerate W-frontier phase class under the exact accepted ratio `da/db=10/7`:

1. derive actual restricted-Voronoi shared-face neighbors and displacements;
2. derive the nonnegative displacement/moment cone;
3. test the full reallocation cone `mu_a<=0, mu_b>=0, mu_a+mu_b<=0` and exact sliding ray `(-u,+u)`;
4. audit the induced first moment of the accepted source-state face-flux formula;
5. if needed and geometrically feasible, freeze a boundary-local nonnegative moment-matching rate rule on actual Voronoi neighbors;
6. otherwise establish the precise recurring-class obstruction;
7. audit phase-uniform refinement and W-endpoint/joint-boundary compatibility.

No numerical `W_max` is selected.

## Exact Builder allowlist

Issue #48 may create only the nine exact paths named in the Issue body. No existing tracked file may be modified by Builder.

## Scientific ceiling

Issue #48 is design-only. Do not mutate accepted source; implement Voronoi/rate/HJB/KFE code; run programmatic grid/Voronoi/Delaunay experiments; run HJB/KFE/stationary solves; choose numerical `W_max`; agglomerate cells; run pin sensitivity; compute `C,L,A,B`; rebuild GE; or enter multi-province/neural/nominal/calibration/policy/welfare/Results. No PR/merge/Issue close/successor/self-accept from Builder.

Current Startup Snapshot:

`docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`

Current Master Roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
