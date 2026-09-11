# Deep Learning + HANK Task Index

Status: `NO_ACTIVE_BUILDER_ISSUE__DLH_5VF_OUTCOME_C_ACCEPTED__OWNER_APPROXIMATION_ROUTE_DECISION_REQUIRED`

Last synchronized: 2026-09-11

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

**NONE.**

Issue #54 / DLH-5V-F has been independently reviewed and accepted at Outcome C. No successor Builder Issue is authorized by that acceptance. Chat text, this Task Index, or the roadmap alone cannot create successor authority.

## Latest accepted task — Issue #54 / DLH-5V-F

Title:

`DLH-5V-F: Close endpoint bands and joint-boundary finite-process contract`

Task type:

`SCIENTIFIC_DESIGN__ENDPOINT_BAND_AND_JOINT_BOUNDARY_FINITE_PROCESS_CLOSURE`

Accepted candidate:

`b9dab7b6cf5d724074765ddb88d6f300175f6c6f`

Reviewer acceptance:

`5633995486`

Acceptance level:

`L3_COMMIT_VERIFIED__SCIENTIFIC_DESIGN_ACCEPTED`

Acceptance integration:

`4e77d9c753f81eb2517a8b90a0827db6af8faed4`

Accepted verdict:

`DLH_5VF_ACCEPTED__OUTCOME_C_CONFIRMED__EXACT_ENDPOINT_FINITE_PROCESS_REPRESENTABILITY_OBSTRUCTION_FROZEN__OWNER_APPROXIMATION_ROUTE_DECISION_REQUIRED`

Accepted terminal:

`DLH_5VF_ENDPOINT_JOINT_BOUNDARY_FINITE_PROCESS_OBSTRUCTION__OWNER_ROUTE_DECISION_REQUIRED`

## Accepted scientific result

The recurring regular W-frontier contract from DLH-5V-E remains valid on regular W-active states with

```text
7<=j<=12
i>=10
```

but the full deferred endpoint complement cannot be closed under the simultaneously frozen requirements:

```text
actual represented native-grid states only
+ nonnegative Markov transition rates
+ exact pointwise first-moment matching
+ exact same-process HJB/KFE law
```

The controlling obstruction is closed-form. At an exact-frontier top state with `r_j=0`, source W-index equals `N`, so every represented destination has `Delta W<=0`. Exact tangent motion `mu_W=0` therefore can use only same-W destinations. Since

```text
10 Delta j + 7 Delta i = 0
```

implies native same-W displacements are integer multiples of `(7,-10)`, lower a-interior endpoint-band states `j in {1,...,6}` lack the forward same-W orientation and cannot represent the admissible ray `(-u,+u)`, while upper a-interior states `j in {13,...,18}` lack the reverse orientation and cannot represent `(+u,-u)`.

For every `N>=190` in the current regular-Regime-I symbolic family, the period-7 residue structure supplies at least one such obstructed a-interior exact-frontier column. No numerical production `W_max` was selected.

This is a finite-process/lattice representability obstruction, not an accepted-household source error and not a KFE repair opportunity.

## Continuous versus discrete boundary semantics

Reachability bands are not economic faces:

```text
j=0 only      -> actual a=0 face
j=1,...,6     -> lower-a reachability band but a-interior
j=19 only     -> actual a=a_max face
j=13,...,18   -> upper-a reachability band but a-interior
i=0 only      -> actual b=b_min face
i=1,...,9     -> lower-b reachability band but b-interior
```

Continuous active-face laws remain:

```text
a=0:       mu_a>=0
b=b_min:   mu_b>=0
a=a_max:   mu_a<=0
W:         mu_a+mu_b<=0
```

In Regime I the continuous W face does not intersect `b=b_min`; the continuous `a=a_max x b=b_min x W` triple intersection occurs only at `W_max=8`. Discrete restricted-Voronoi W-contact is a separate cell-level object.

## Controlling household / same-process authority

Accepted household source remains immutable/read-only:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Binding law:

```text
HJB boundary policy <=> KFE boundary transition law
```

The clean/source-free future process contract remains:

```text
Q = backward controlled generator
Q^T = forward mass operator
Q_ij >= 0 for i != j
Q_ii = -sum of ACTUAL represented outgoing rates
Q1 = 0 by construction
same selected Q for HJB and KFE
p = M g
p_dot = Q^T p
```

Issue #27 pin/normalization remains scale fixing only and may never repair leakage.

Stationary KFE remains **NOT AUTHORIZED**.

## Owner route decision — next scientific object, NOT YET AUTHORIZED

Outcome C requires the Owner to choose which frozen discretization assumption may be relaxed before implementation. Bounded route families include:

1. relax exact endpoint first-moment matching to an explicitly controlled monotone/conservative asymptotic approximation while preserving one-Q semantics;
2. augment or boundary-fit the represented state set so the missing tangent orientation becomes representable;
3. change grid/aspect or use a boundary-fitted lattice;
4. transform coordinates (for example a future `(a,W)` representation) and re-derive the affected boundary contract.

No route above is selected by this Task Index. No implementation gate is authorized until the Owner selects a route and a new Issue is separately published, synchronized and activated.

## Current governance files

- `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
- `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
- Issue #54 acceptance history.

The post-DLH-5V-E handoff snapshot is a historical checkpoint and does not override CURRENT governance.
