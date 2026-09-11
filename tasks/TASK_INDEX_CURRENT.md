# Deep Learning + HANK Task Index

Status: `PUBLISHED_BUILDER_ISSUE_55__DLH_5VG_ROUTE_A_ASYMPTOTIC_ENDPOINT_APPROXIMATION__ACTIVATION_PENDING`

Last synchronized: 2026-09-11

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

**Issue #55 / DLH-5V-G is published but activation is pending at this commit.**

Title:

`DLH-5V-G: Prove/refute shrinking endpoint-layer asymptotic same-process approximation`

Task type:

`SCIENTIFIC_DESIGN__SHRINKING_ENDPOINT_LAYER_ASYMPTOTIC_MARKOV_APPROXIMATION`

Owner decision:

`APPROVE_DLH_5VG_ROUTE_A_ASYMPTOTIC_ENDPOINT_APPROXIMATION_DESIGN_GATE`

Dedicated Builder branch:

`dsh/issue-55-dlh-5vg-asymptotic-endpoint-approximation-2026-09-11`

Issue #55 body plus its future authoritative activation comment are the sole Builder task authority. This Task Index cannot expand scope. Builder MUST NOT mutate anything until the activation comment is posted and a fresh startup verifies Issue #55 remains OPEN and all CURRENT governance agrees.

## Latest accepted task — Issue #54 / DLH-5V-F

Issue #54 is CLOSED completed.

Accepted candidate:

`b9dab7b6cf5d724074765ddb88d6f300175f6c6f`

Reviewer acceptance:

`5633995486`

Acceptance integration:

`4e77d9c753f81eb2517a8b90a0827db6af8faed4`

Accepted verdict:

`DLH_5VF_ACCEPTED__OUTCOME_C_CONFIRMED__EXACT_ENDPOINT_FINITE_PROCESS_REPRESENTABILITY_OBSTRUCTION_FROZEN__OWNER_APPROXIMATION_ROUTE_DECISION_REQUIRED`

Accepted terminal:

`DLH_5VF_ENDPOINT_JOINT_BOUNDARY_FINITE_PROCESS_OBSTRUCTION__OWNER_ROUTE_DECISION_REQUIRED`

## Accepted obstruction — controlling science

The accepted exact finite-m obstruction is:

```text
actual native represented states only
+ nonnegative Markov rates
+ exact pointwise first-moment equality for every finite endpoint candidate
+ exact one-Q same-process HJB/KFE law
```

cannot all hold over the full endpoint complement.

At `r_j=0` exact-frontier top states, every represented destination has `Delta W<=0`; exact tangent `mu_W=0` therefore uses same-W moves only. Since `10 Delta j + 7 Delta i=0`, same-W native moves are multiples of `(7,-10)`. Lower endpoint bands can miss `(-7,+10)` and upper endpoint bands can miss `(+7,-10)`. This is a lattice/discretization obstruction, not a household-source error.

The exact recurring regular W-frontier contract through DLH-5V-E remains accepted and is not reopened.

## Active scientific object after activation — Route A

Issue #55 investigates the least-disruptive Route A only. It keeps household economics, `D_W`, native represented-state family, 10:7 aspect, nonnegative/conservative Markov rows and one-Q semantics, while allowing a deliberately numerical shrinking endpoint-layer approximation.

Symbolic fixed-aspect refinement family:

```text
m=1,2,...
da_m=10/(19m)
db_m=7/(19m)
a_j=j*10/(19m), j=0,...,19m
b_i=b_min+i*7/(19m)
N_m=floor(19m*(W_max-b_min))
10j+7i<=N_m
```

Endpoint stencil layers have physical thickness bounded by

```text
ell_m=70/(19m)=O(1/m).
```

Scientific preference order:

1. first test a shrinking **numerical candidate-admissibility buffer** that may preserve exact first moments for all admitted candidates;
2. only if that fails, test an explicit quantified moment-defect approximation.

Required design theorem includes: exactness away from endpoints, shrinking physical layer, tangent-cone/admissible-set graph consistency, generator/operator consistency, vanishing numerical diffusion, monotonicity, conservation, one-Q same-process semantics and seam consistency.

## Same-process / mass authority

Accepted household source remains immutable/read-only:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Binding law:

```text
HJB boundary policy <=> KFE boundary transition law
Q backward
Q^T forward
Q_ij>=0 for i!=j
Q_ii=-sum of ACTUAL represented outgoing rates
Q1=0 by construction
same selected Q for HJB and KFE
p=M g
p_dot=Q^T p
```

Pinning/normalization may fix scale only and may not repair leakage.

Stationary KFE remains **NOT AUTHORIZED**.

## Hard ceiling

Issue #55 is design-only. It does not authorize source implementation, production generator assembly/run, HJB/KFE/stationary execution, numerical production `W_max`, grid/aspect/domain redesign, state augmentation, coordinate transformation, aggregates/GE/multi-region/neural/nominal/calibration/policy/welfare/Results, PR/merge/close/successor/self-accept.

## Current governance files

- `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
- `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
- Issue #55 body/comments.

Issue #54 acceptance history remains controlling provenance for the obstruction.