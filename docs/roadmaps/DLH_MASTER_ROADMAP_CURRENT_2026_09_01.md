# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.40  
**Date:** 2026-09-11  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** DLH-5V-G / ISSUE #55 PUBLISHED — ROUTE A SHRINKING ENDPOINT-LAYER ASYMPTOTIC APPROXIMATION / ACTIVATION PENDING

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

Restricted-Voronoi cells remain the state partition / mass-volume geometry. The same selected backward generator `Q` must define the future forward mass dynamics `p_dot=Q^T p`.

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

Accepted sector coverage:

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

Candidate semantics remain frozen:

```text
continuous admissibility
 -> candidate-specific represented nonnegative rates
 -> discrete H_h score BEFORE selection
 -> ONE global statewise argmax
 -> selected rates
 -> ONE conservative backward Q
 -> future KFE consumes exactly Q^T
```

The regular block is not reopened by the endpoint approximation gate.

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

At `r_j=0` exact-frontier top states every represented destination has `Delta W<=0`. Exact tangent `mu_W=0` with nonnegative rates therefore needs same-W moves only; native same-W displacements satisfy `10 Delta j+7 Delta i=0` and are multiples of `(7,-10)`. Finite lower/upper endpoint bands can miss one orientation. Hence the exact finite-m endpoint contract cannot cover all continuously admissible finite-m endpoint candidates while simultaneously retaining native states, nonnegative rates, exact first moments and one-Q same-process semantics.

This is a lattice/discretization obstruction, not a household-source failure.

---

## 4. Owner-selected next route — Route A

Owner now explicitly selects:

`APPROVE_DLH_5VG_ROUTE_A_ASYMPTOTIC_ENDPOINT_APPROXIMATION_DESIGN_GATE`

Route A preserves:

- household economics;
- finite W-domain;
- native represented-state family and 10:7 aspect;
- nonnegative Markov rates;
- row conservation;
- one-Q HJB/KFE semantics;
- exact accepted regular-region contracts.

It relaxes only the finite-m requirement that **every endpoint-layer continuously admissible candidate must have exact pointwise native-grid first-moment representation**.

No implementation is authorized yet.

---

## 5. DLH-5V-G / Issue #55 — shrinking endpoint-layer asymptotic same-process approximation

Title:

`DLH-5V-G: Prove/refute shrinking endpoint-layer asymptotic same-process approximation`

Task type:

`SCIENTIFIC_DESIGN__SHRINKING_ENDPOINT_LAYER_ASYMPTOTIC_MARKOV_APPROXIMATION`

Dedicated branch after activation:

`dsh/issue-55-dlh-5vg-asymptotic-endpoint-approximation-2026-09-11`

Issue #55 is published. Builder mutation remains blocked until the authoritative activation comment is posted.

### 5.1 Fixed-aspect symbolic refinement family

```text
m=1,2,...
da_m=10/(19m)
db_m=7/(19m)
a_j^(m)=j*10/(19m), j=0,...,19m
b_i^(m)=b_min+i*7/(19m)
N_m=floor(19m*(W_max-b_min))
10j+7i<=N_m
```

`m=1` is the current accepted production-grid geometry. No numerical production `W_max` is selected in this gate.

Primitive tangent jumps scale as

```text
w_T^m=(-70/(19m),+70/(19m))
w_RT^m=(+70/(19m),-70/(19m)).
```

The common exact regular region at level `m` is

```text
7<=j<=19m-7
i>=10
```

plus accepted W-active/class conditions.

Endpoint stencil-width layers have physical thickness bounded by

```text
ell_m=70/(19m)=O(1/m).
```

### 5.2 Preferred Route-A contract A1

First test a **shrinking numerical candidate-admissibility buffer**:

```text
lower-a stencil layer -> numerical mu_a>=0
upper-a stencil layer -> numerical mu_a<=0
lower-b stencil layer -> numerical mu_b>=0
W-active/contact       -> mu_W<=0
```

At true coordinate faces these are economic constraints; at interior stencil-layer nodes they are numerical restrictions only. They must be applied before candidate scoring/selection, never by clipping a selected control.

A1 is preferred because, if valid, it can preserve exact first moments for every admitted finite-m candidate and relax only the candidate admissible set on a physical layer whose width vanishes.

### 5.3 Fallback A2

Only if A1 fails, test a nonzero first-moment defect with an explicit error object and a proved vanishing consistency statement. No hidden inward-normal bias may be relabeled as exactness.

### 5.4 Required design theorem

Issue #55 must prove/refute all of:

1. exact regular-contract recovery on every physical compact subset away from true endpoints for sufficiently large `m`;
2. `O(1/m)` shrinking endpoint-layer width, uniformly across frontier phases;
3. outer/limsup and recovery/liminf consistency of the numerical admissible drift sets with the true limiting tangent cones at economic faces/intersections;
4. generator consistency for smooth test functions;
5. jump size `O(1/m)`, rate scale `O(m)` and vanishing second-moment / numerical-diffusion term (or the correct rigorously derived orders);
6. nonnegative off-diagonal rates and `Q_m 1=0` by construction;
7. ONE selected backward `Q_m` with future KFE exactly `Q_m^T`;
8. seam consistency with the accepted exact regular process.

Finite enumerations may be supplementary checks only; the asymptotic conclusion requires analytic or parameterized symbolic evidence.

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
Route A shrinking endpoint-layer asymptotic design            PUBLISHED — ISSUE #55 / ACTIVATION PENDING
boundary-HJB / finite-process implementation                 BLOCKED PENDING 5V-G
same-process Q validation + SCC diagnostics                  PENDING
nested Wmax / resolution robustness                          PENDING
conservative stationary-generator validation                 PENDING
Issue #27 stationary KFE                                     NOT AUTHORIZED
stationary C,L,A,B                                           PENDING
two-region structural anchor rebuild                         PENDING
3–5 province integration                                     PENDING
learned regional W^L                                         PENDING
```

---

## 7. Issue #55 terminal structure

Route-A design success:

`DLH_5VG_ROUTE_A_SHRINKING_ENDPOINT_LAYER_ASYMPTOTIC_SAME_PROCESS_CONTRACT_FROZEN__READY_FOR_BOUNDARY_HJB_IMPLEMENTATION_GATE`

Sharply bounded partial:

`DLH_5VG_ROUTE_A_PARTIAL__ONE_BOUNDED_CONSISTENCY_CONDITION_REMAINS_UNPROVED`

Route-A obstruction:

`DLH_5VG_ROUTE_A_ASYMPTOTIC_ENDPOINT_APPROXIMATION_OBSTRUCTION__OWNER_ROUTE_REDECISION_REQUIRED`

Authority/refinement inconsistency:

`BLOCKED_DLH_5VG_ACCEPTED_AUTHORITY_OR_REFINEMENT_FAMILY_INCONSISTENCY`

No terminal self-authorizes implementation; fresh ChatGPT review is required.

---

## 8. Same-process safeguards — frozen

```text
Q_m backward
Q_m^T forward
Q_ij>=0 for i!=j
Q_ii=-sum of ACTUAL represented outgoing rates
Q_m 1=0 by construction
same selected Q_m for HJB and KFE
p=M g
p_dot=Q_m^T p
```

No candidate route may use pinning/normalization to repair leakage or create a KFE-only process.

Stationary KFE remains explicitly blocked.

---

## 9. Interpretation ceiling

DLH-5V-G is analytic/design only. It does not authorize source implementation, production generator assembly/run, HJB/KFE/stationary computation, numerical production `W_max`, state augmentation, grid/aspect/domain redesign, coordinate transformation, aggregates, GE, multi-region, neural, nominal, calibration, policy, welfare or Results prose.

---

## 10. Current governance pointers

- `tasks/TASK_INDEX_CURRENT.md`
- `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
- Issue #55 body/comments.

Issue #54 acceptance history remains the controlling provenance for the finite endpoint obstruction.

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.