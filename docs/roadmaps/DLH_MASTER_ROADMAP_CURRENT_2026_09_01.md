# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.41  
**Date:** 2026-09-11  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** POST-DLH-5V-G OUTCOME C ACCEPTED — ROUTE A GRAPH-CONSISTENCY OBSTRUCTION FROZEN / OWNER ROUTE RE-DECISION NEXT

---

## 0. Long-run objective

Build a hybrid structural–learned regional HANK platform in which household HJB/KFE, aggregation, firm/accounting and later nominal-HANK equations remain explicit structural economics, while hard-to-specify cross-regional mappings become learned modules only after household and equilibrium foundations pass scientific and numerical validation.

The first learned object remains regional labor/spatial mapping `W^L`. Neural training remains downstream.

---

## 1. Accepted household / finite-domain foundation

Accepted household source:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Accepted finite production-domain family:

```text
D_W(W_max)={0<=a<=a_max,b>=b_min,a+b<=W_max}
a_max=10
b_min=-2
```

No numerical production `W_max` is selected.

Binding law:

```text
HJB boundary policy <=> KFE boundary transition law
```

Restricted-Voronoi cells remain the state partition / mass-volume geometry. Any future controlled backward generator `Q` must define the forward mass dynamics exactly through `p_dot=Q^T p`.

Stationary KFE remains **NOT AUTHORIZED**.

---

## 2. Accepted regular-frontier chain — DLH-5V-A through DLH-5V-E

Base accepted grid (`m=1`):

```text
da=10/19
db=7/19
10j+7i<=N
```

Accepted recurring regular W-active region:

```text
7<=j<=12
i>=10
```

plus accepted W-active/class conditions.

Accepted regular sector coverage:

```text
T_W={mu_W<=0}=T_realloc union R_reverse union R_deplete
```

with exact tangent moves

```text
w_T=(-70/19,+70/19)
w_RT=(+70/19,-70/19)
```

and local inward moves

```text
w_left=(-10/19,0)
w_down=(0,-7/19).
```

Candidate semantics remain frozen on the accepted regular W-active block:

```text
continuous admissibility
 -> candidate-specific represented nonnegative rates
 -> discrete H_h score BEFORE selection
 -> ONE global statewise argmax
 -> selected rates
 -> ONE conservative backward Q
 -> future KFE consumes exactly Q^T
```

---

## 3. DLH-5V-F / Issue #54 — exact endpoint finite-process obstruction — ACCEPTED

Accepted candidate:

`b9dab7b6cf5d724074765ddb88d6f300175f6c6f`

Reviewer acceptance:

`5633995486`

Acceptance integration:

`4e77d9c753f81eb2517a8b90a0827db6af8faed4`

Accepted verdict:

`DLH_5VF_ACCEPTED__OUTCOME_C_CONFIRMED__EXACT_ENDPOINT_FINITE_PROCESS_REPRESENTABILITY_OBSTRUCTION_FROZEN__OWNER_APPROXIMATION_ROUTE_DECISION_REQUIRED`

At exact-frontier `r_j=0` top states every represented destination has `Delta W<=0`. Exact tangent `mu_W=0` with nonnegative rates therefore requires same-W moves only; native same-W displacements satisfy `10 Delta j+7 Delta i=0` and are multiples of `(7,-10)`. Finite lower/upper endpoint bands can miss one orientation. Hence exact finite-m endpoint closure fails if native states, nonnegative rates, exact pointwise first moments and one-Q semantics are all retained.

---

## 4. DLH-5V-G / Issue #55 — Route A shrinking-layer asymptotic repair — OUTCOME C ACCEPTED

Accepted candidate:

`15f2f81653a847344d2cd647705487cc893af1d7`

Reviewer acceptance:

`5635802416`

Acceptance integration:

`8dd5e9c444d7356736f28a29b9ffe492bbe81caa`

Accepted verdict:

`DLH_5VG_ACCEPTED__OUTCOME_C_CONFIRMED__ROUTE_A_TANGENT_CONE_GRAPH_CONSISTENCY_OBSTRUCTION_FROZEN__OWNER_ROUTE_REDECISION_REQUIRED`

Accepted terminal:

`DLH_5VG_ROUTE_A_ASYMPTOTIC_ENDPOINT_APPROXIMATION_OBSTRUCTION__OWNER_ROUTE_REDECISION_REQUIRED`

### 4.1 Fixed-aspect family tested

```text
m=1,2,...
da_m=10/(19m)
db_m=7/(19m)
a_j=j*10/(19m), j=0,...,19m
b_i=b_min+i*7/(19m)
N_m=floor(19m*(W_max-b_min))
10j+7i<=N_m
```

Route A kept the state/grid family, household economics, nonnegative Markov rates, conservation and one-Q semantics frozen and tried to repair the finite-m endpoint obstruction through a shrinking numerical endpoint layer.

### 4.2 What finite-m algebra still works

For A1-admitted finite-m candidates, the layer sector contracts remain coherent: actual represented destinations, nonnegative rates, exact first moments, jump size `O(1/m)`, rate scale `O(m)`, second moments `O(1/m)`, conservative rows and one-Q semantics.

These finite-m facts are accepted only as bounded algebraic evidence. They do not imply an asymptotically valid global state-constraint scheme.

### 4.3 Controlling graph-consistency counterexample

Take

```text
s_m=(0,i_t^m(0)-2)
mu=(0,1).
```

These states are represented and non-W-active but converge physically to the true corner `(0,W_max)`. The drift is admitted by the finite-m lower-a rule and exactly represented using the native upward transition. The limiting true tangent cone is

```text
{mu_a>=0, mu_W<=0},
```

so the limit drift lies outside it. The required outer/limsup condition therefore fails.

### 4.4 Why no shrinking per-state buffer can repair it

Let `k_m=i_t(0)-i_m` count rows below the W frontier in the lower-a layer. Physical W-distance is asymptotically proportional to `k_m/m`.

For outer consistency at `(0,W_max)`, every sublinear sequence `k_m=o(m)` must eventually exclude an outward b-direction neighborhood. If admitted outward drifts survived at ratios tending to zero on infinitely many levels, those states themselves would form a counterexample sequence. Therefore outer consistency forces an eventual positive lower bound on the physical distance at which such drifts can remain admissible.

But then choose a fixed positive distance below that bound. Those states converge to an `a=0` face-interior point where the true tangent cone is `{mu_a>=0}` and recovery/liminf requires the b-direction freedom that the buffer would suppress. Hence outer/limsup and recovery/liminf cannot both hold under any per-state shrinking-buffer rule on the frozen family.

This diagonal incompatibility is stronger than failure of any particular fixed-row or distance-threshold recipe.

### 4.5 A2 does not rescue the authorized theorem

Issue #55 separately required admissible-set/tangent-cone graph consistency. A first-moment-defect rule changes represented moments but does not remove this admissible-set incompatibility under the authorized Route-A theorem. The controlling counterexample is already exactly representable with zero moment defect.

Thus Route A is rejected under the exact consistency target that Issue #55 was tasked to prove/refute.

---

## 5. Continuous boundary geometry remains frozen

True active-face laws remain

```text
a=0:       mu_a>=0
b=b_min:   mu_b>=0
a=a_max:   mu_a<=0
W:         mu_a+mu_b<=0
```

Regime-I corner semantics:

```text
(0,W_max):                    a=0 x W
(a_max,W_max-a_max):          a_max x W
(a_max,b_min), W_max>8:       a_max x b_min only
(a_max,b_min), W_max=8:       a_max x b_min x W triple corner
(0,b_min):                    a=0 x b_min
```

Reachability bands and numerical buffers are not economic faces.

---

## 6. Current roadmap position

```text
MATLAB-faithful two-asset household economics                 ACCEPTED
finite W-domain + continuous tangent/KKT law                 ACCEPTED
same-process HJB <=> KFE principle                           ACCEPTED
restricted-Voronoi state partition                           ACCEPTED
regular W-frontier phase / adjacency                         ACCEPTED
shared-face-only local process                               OBSTRUCTION ACCEPTED
regular exact-tangent wide-stencil process                   ACCEPTED
regular control-dependent rates / global scoring             ACCEPTED
endpoint exact finite-process closure                         OBSTRUCTION ACCEPTED — ISSUE #54
Route A shrinking endpoint-layer asymptotic repair            OBSTRUCTION ACCEPTED — ISSUE #55
Owner discretization / consistency route re-decision          NEXT — NOT YET AUTHORIZED
boundary-HJB / finite-process implementation                 BLOCKED PENDING NEW ROUTE
same-process Q validation + SCC diagnostics                  PENDING
nested Wmax / resolution robustness                          PENDING
conservative stationary-generator validation                 PENDING
Issue #27 stationary KFE                                     NOT AUTHORIZED
stationary C,L,A,B                                           PENDING
two-region structural anchor rebuild                         PENDING
3–5 province integration                                     PENDING
learned regional W^L                                         PENDING
```

Current Builder authority: **NONE**.

---

## 7. Owner route re-decision — exact next scientific block, NOT YET AUTHORIZED

Route A has failed under its authorized graph-consistency theorem. Remaining route families are now:

### Route B — boundary-state augmentation / boundary fitting

Change the represented state geometry near economic faces/intersections so the discrete state set itself respects the boundary topology. This can restore exact tangent directions but requires a new restricted-cell/mass partition, adjacency and conservation proof.

### Route C — grid/aspect or boundary-fitted lattice redesign

Change lattice geometry so tangent motion and endpoint topology are compatible. This is invasive because accepted phase/stencil results would need controlled re-derivation.

### Route D — coordinate transformation

Move to coordinates such as `(a,W)` and re-derive borrowing-floor, transfer-FOC, state partition, boundary and same-process laws. The W cap becomes coordinate-aligned but other geometry becomes more complex.

### Route E — explicitly re-scope the consistency target

Only if Owner decides the exact Kuratowski-style admissible-set graph requirement in Issue #55 is stronger than necessary for the intended state-constraint HJB convergence theorem, a new design gate may formulate a different consistency target. This would reopen the mathematical convergence requirement, not silently reinterpret Issue #55.

No route is selected by this roadmap. Owner approval is required before publishing a successor Issue.

---

## 8. Same-process safeguards — frozen through route re-decision

```text
Q backward
Q^T forward
Q_ij>=0 for i!=j
Q_ii=-sum of ACTUAL represented outgoing rates
Q1=0 by construction
same selected Q for HJB and KFE
p=M g
p_dot=Q^T p
```

No route may use pinning/normalization to repair leakage or create a KFE-only process.

Stationary KFE remains explicitly blocked.

---

## 9. Interpretation ceiling

DLH-5V-G acceptance establishes a Route-A design obstruction. It does not authorize implementation, production generator assembly/run, HJB/KFE/stationary computation, numerical production `W_max`, state augmentation, grid/aspect/domain redesign, coordinate transformation, aggregates, GE, multi-region, neural, nominal, calibration, policy, welfare or Results prose.

---

## 10. Current governance pointers

- `tasks/TASK_INDEX_CURRENT.md`
- `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
- Issue #55 acceptance history.

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.
