# Deep Learning + HANK Task Index

Status: `NO_ACTIVE_BUILDER_ISSUE__DLH_5U_ACCEPTED__TANGENTIAL_VORONOI_PROCESS_DESIGN_REQUIRED`

Last synchronized: 2026-09-03

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

**NONE.**

Issue #47 / DLH-5U is accepted and CLOSED completed. DSH must remain stopped until a successor bounded design Issue is separately published, CURRENT Task Index / Startup Snapshot are synchronized to it, and an authoritative activation comment is posted.

Chat text alone does not create Builder authority.

## Latest accepted task — Issue #47 / DLH-5U

Title:

`DLH-5U: Freeze W1 face-adapted finite-volume same-process discretization`

Task type:

`SCIENTIFIC_DESIGN__W1_FACE_ADAPTED_FINITE_VOLUME_SAME_PROCESS_DISCRETIZATION`

Accepted Rev-1 candidate:

`81bf9b46f20e6dd96514bb6fad698097c917a948`

Reviewer acceptance comment:

`5521379228`

Acceptance integration commit:

`060c2835825f9efff4f89c84646f04cab6a9c8a4`

Acceptance level:

`L3_COMMIT_VERIFIED__SCIENTIFIC_DESIGN_ACCEPTED`

Accepted reviewer verdict:

`DLH_5U_REV1_ACCEPTED__OUTCOME_B_CONFIRMED__ROUTE_F_FRAMEWORK_ACCEPTED__TANGENTIAL_SAME_PROCESS_CONSISTENCY_REMAINS_THE_SINGLE_BOUNDED_OPEN_OBJECT`

Accepted terminal:

`DLH_5U_ROUTE_F_SCIENTIFICALLY_VIABLE__ONE_BOUNDED_DISCRETE_GEOMETRY_OR_WEIGHTED_ADJOINT_OBJECT_REMAINS_UNRESOLVED`

## Accepted Route-F scientific state

Accepted household source remains immutable/read-only:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Binding law remains:

```text
HJB boundary policy <=> KFE boundary transition law
```

Stationary KFE remains **NOT AUTHORIZED**.

Accepted finite-domain / continuous authority remains:

```text
D_W(W_max) = {0<=a<=a_max, b>=b_min, a+b<=W_max}

a=0:          mu_a >= 0
b=b_min:      mu_b >= 0
a=a_max:      mu_a <= 0
a+b=W_max:    mu_W=mu_a+mu_b <= 0
```

`W_max` remains numerical truncation authority only; no production number is selected.

Accepted DLH-5U design objects:

1. restricted-Voronoi control-volume tessellation induced only by represented W1 nodes, partitioning `D_W` a.e.;
2. node value + cell-level control object, with W KKT only when the actual Voronoi cell has positive physical W-face segment;
3. exact control-dependent discrete Hamiltonian
   `H_h = u-v + sum_r q_{s->r}(c,l,d)(V_r-V_s) + switch`;
4. monotone/conservative face-flux CTMC framework with one `Q` for backward HJB action and forward mass dynamics;
5. mass/density distinction `p=M g`, stationary mass equation `Q^T p=0`, density equation `M^{-1}Q^T M g=0`;
6. MATLAB-style Issue #27 component pin preserved downstream on mass `p`, followed by normalization and ORIGINAL `Q^T p` residual validation.

## Single bounded unresolved object

Tangential same-process consistency at the actual restricted-Voronoi W frontier remains unresolved.

The Rev-0 two-step axial cascade is NOT accepted as first-order consistent: for the exact tangent benchmark `mu_a=-u`, `mu_b=+u`, fixed `da/db=10/7`, it produces an O(1) spurious normal drift. The simple oblique one-step candidate is not monotone on the accepted rectangular lattice.

The next bounded design must analyze the **actual restricted-Voronoi face-adjacency / neighbor-displacement moment cone**, including oblique Voronoi neighbors. The failed axial candidates are not an impossibility theorem for the true Voronoi graph.

Reviewer clarifications controlling the successor:

- determine `F_s^W` from the actual restricted-Voronoi cell intersection with `a+b=W_max`; do not use base-rectangle crossing as an iff shortcut;
- a future sliver rule must either be a pre-registered geometric fail-closed admissibility condition or separately freeze the state/control/value semantics of agglomeration;
- no implementation is authorized until tangential moment/transition consistency is resolved.

## Scientific ceiling

Until successor authority exists, do not:

- mutate accepted household economics/source;
- implement Route F / restricted Voronoi / boundary-HJB / generator code;
- choose numerical `W_max`;
- execute HJB/KFE/stationary/grid/domain experiments;
- run contamination sensitivity;
- compute stationary aggregates `C,L,A,B`;
- rebuild two-region GE;
- enter multi-province execution, neural training, nominal HANK, calibration, policy, welfare or Results.

Current Startup Snapshot:

`docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`

Current Master Roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
