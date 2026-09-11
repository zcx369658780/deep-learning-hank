# Deep Learning + HANK Startup Snapshot — CURRENT

Date: 2026-09-11

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

**ACTIVE — Issue #55 / DLH-5V-G.**

Title:

`DLH-5V-G: Prove/refute shrinking endpoint-layer asymptotic same-process approximation`

Task type:

`SCIENTIFIC_DESIGN__SHRINKING_ENDPOINT_LAYER_ASYMPTOTIC_MARKOV_APPROXIMATION`

Owner decision:

`APPROVE_DLH_5VG_ROUTE_A_ASYMPTOTIC_ENDPOINT_APPROXIMATION_DESIGN_GATE`

Authoritative activation comment:

`5634144909`

Authority marker:

`DLH_5VG_ROUTE_A_SHRINKING_ENDPOINT_LAYER_ASYMPTOTIC_APPROXIMATION_AUTHORIZED`

Dedicated Builder branch:

`dsh/issue-55-dlh-5vg-asymptotic-endpoint-approximation-2026-09-11`

Builder must fresh-fetch live `origin/main`, verify Issue #55 remains OPEN, read all CURRENT rules/governance and the full Issue/comments, confirm the exact task type/branch and activation comment, verify the accepted household blob, then work only inside the Issue allowlist.

## Latest accepted gate — Issue #54 / DLH-5V-F

Accepted candidate:

`b9dab7b6cf5d724074765ddb88d6f300175f6c6f`

Reviewer acceptance:

`5633995486`

Acceptance integration:

`4e77d9c753f81eb2517a8b90a0827db6af8faed4`

Acceptance level:

`L3_COMMIT_VERIFIED__SCIENTIFIC_DESIGN_ACCEPTED`

Accepted verdict:

`DLH_5VF_ACCEPTED__OUTCOME_C_CONFIRMED__EXACT_ENDPOINT_FINITE_PROCESS_REPRESENTABILITY_OBSTRUCTION_FROZEN__OWNER_APPROXIMATION_ROUTE_DECISION_REQUIRED`

Accepted terminal:

`DLH_5VF_ENDPOINT_JOINT_BOUNDARY_FINITE_PROCESS_OBSTRUCTION__OWNER_ROUTE_DECISION_REQUIRED`

## Accepted obstruction — exact core

The accepted finite-m endpoint obstruction remains controlling:

- exact-frontier `r_j=0` source has every represented destination with `Delta W<=0`;
- exact `mu_W=0` with nonnegative Markov rates therefore requires same-W transitions only;
- `10 Delta j + 7 Delta i=0` implies same-W native displacements are multiples of `(7,-10)`;
- lower a-interior endpoint bands can lack `(-7,+10)` and upper a-interior bands can lack `(+7,-10)`.

Thus finite exact pointwise process closure fails on the full endpoint complement under the previously frozen exact contract. This does not invalidate the household economics, finite W-domain, continuous KKT law or accepted recurring regular W-frontier formulas.

## Owner-selected Route A — active scientific object

Issue #55 tests whether the obstruction is only a finite-grid endpoint-layer phenomenon that can be handled by a **shrinking numerical approximation layer** while preserving conservation, monotonicity and one-Q semantics.

Fixed-aspect symbolic refinement family:

```text
m=1,2,...
da_m=10/(19m)
db_m=7/(19m)
a_j=j*10/(19m), j=0,...,19m
b_i=b_min+i*7/(19m)
N_m=floor(19m*(W_max-b_min))
10j+7i<=N_m
```

Primitive exact tangent jumps scale as

```text
w_T^m=(-70/(19m),+70/(19m))
w_RT^m=(+70/(19m),-70/(19m))
```

and endpoint reachability layers have physical thickness

```text
ell_m=70/(19m)=O(1/m).
```

### Route-A preference order

First test **A1**: a numerical candidate-admissibility buffer on the finite stencil-width layer, applied before scoring/selection and clearly distinguished from true economic faces. If A1 is asymptotically consistent, it may retain exact first moments for all admitted candidates.

Only if A1 fails, test **A2**: an explicit first-moment defect with a declared error object and a proved vanishing operator/boundary-layer consistency statement.

The gate must prove/refute: exactness away from endpoints, shrinking layer, tangent-cone graph consistency, generator/operator consistency, jump/rate/second-moment scaling, monotonicity, conservation, one-Q same-process semantics and seam consistency with the accepted exact regular contract.

A finite enumeration is supplementary only; the controlling consistency result must be analytic or parameterized symbolically.

## Continuous boundary law remains intact

Accepted domain:

```text
D_W(W_max)={0<=a<=a_max,b>=b_min,a+b<=W_max}
a_max=10
b_min=-2
```

True active-face laws remain:

```text
a=0:       mu_a>=0
b=b_min:   mu_b>=0
a=a_max:   mu_a<=0
W:         mu_a+mu_b<=0
```

A numerical buffer at interior stencil-layer nodes is NOT an economic-face declaration. Its only authority is as a candidate asymptotically vanishing numerical restriction under Issue #55.

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
HJB and KFE consume the SAME Q
p=M g
p_dot=Q^T p
```

Pinning/normalization may never repair leakage.

Stationary KFE remains **NOT AUTHORIZED**.

## Interpretation ceiling

Issue #55 is analytic/design only. It does not authorize implementation, production-Q execution, HJB/KFE/stationary solves, numerical `W_max`, new states/ghosts, grid/aspect/domain redesign, coordinate transformation, aggregates, GE, regional/neural/nominal/calibration/policy/welfare/Results, PR/merge/close/successor/self-accept.

## Current authoritative files

- `tasks/TASK_INDEX_CURRENT.md`
- `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
- `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
- Issue #55 body/comments.

Issue #54 acceptance history remains the controlling provenance for why Route A is necessary.