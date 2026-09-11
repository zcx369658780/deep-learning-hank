# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.39  
**Date:** 2026-09-11  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** POST-DLH-5V-F OUTCOME C ACCEPTED — ENDPOINT EXACT FINITE-PROCESS OBSTRUCTION FROZEN / OWNER ROUTE DECISION NEXT

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
a_j=j*(10/19), j=0,...,19
```

No numerical production `W_max` is selected.

Binding law:

```text
HJB boundary policy <=> KFE boundary transition law
```

Restricted-Voronoi cells remain the state partition / mass-volume geometry. The same controlled backward generator `Q` must define both discrete-HJB transitions and forward mass dynamics `p_dot=Q^T p`.

Stationary KFE remains **NOT AUTHORIZED**.

---

## 2. Accepted regular-frontier chain — DLH-5V-A through DLH-5V-E

The accepted native grid is

```text
da=10/19
db=7/19
10j+7i<=N
```

with regular W-frontier phase

```text
i_t(j)=floor((N-10j)/7)
r_j=(N-10j) mod 7
r_{j+7}=r_j
```

DLH-5V-B accepted that shared-face-only local geometry cannot represent recurring exact W-tangent sliding. DLH-5V-C/D/E then established the regular wide-stencil remedy and exact control-dependent rate/scoring contract.

Accepted common regular W-active region:

```text
7<=j<=12
i>=10
```

Accepted regular sector decomposition:

```text
T_W={mu_W=mu_a+mu_b<=0}
 = T_realloc union R_reverse union R_deplete
```

Forward tangent:

```text
(Delta j,Delta i)=(-7,+10)
w_T=(-70/19,+70/19)
```

Mirror tangent:

```text
(Delta j,Delta i)=(+7,-10)
w_RT=(+70/19,-70/19)
```

Local inward directions:

```text
w_left=(-10/19,0)
w_down=(0,-7/19)
```

Regular selection semantics remain frozen:

```text
continuous admissibility
 -> candidate-specific represented nonnegative rates
 -> discrete H_h score BEFORE selection
 -> ONE global statewise argmax
 -> selected rates
 -> ONE conservative backward Q
 -> future KFE consumes exactly Q^T
```

Latest regular acceptance, Issue #53 / DLH-5V-E:

- accepted candidate `ff4607ff74ab1e0cea530ba04f17045698f43a62`;
- reviewer acceptance `5632150936`;
- integration `28e42e4c0f65d03aa403cf7aeedb60b83c7837e2`.

The regular block is not reopened by the endpoint obstruction.

---

## 3. DLH-5V-F / Issue #54 — endpoint-band / joint-boundary finite-process closure — OUTCOME C ACCEPTED

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

### 3.1 Deferred endpoint object

```text
lower-a forward-wide band: j in {0,...,6}
upper-a mirror-wide band:  j in {13,...,19}
lower-b mirror-wide band:  i in {0,...,9}
```

Reachability bands are distinct from economic boundary faces:

```text
j=0 only      -> actual a=0 face
j=1,...,6     -> a-interior reachability band
j=19 only     -> actual a=a_max face
j=13,...,18   -> a-interior reachability band
i=0 only      -> actual b=b_min face
i=1,...,9     -> b-interior reachability band
```

Continuous active-face laws remain

```text
a=0:       mu_a>=0
b=b_min:   mu_b>=0
a=a_max:   mu_a<=0
W:         mu_a+mu_b<=0
```

### 3.2 Controlling exact obstruction

At an exact-frontier top state `r_j=0`, source W-index equals `N`. Every represented destination therefore satisfies

```text
Delta W<=0.
```

For a nonnegative Markov-rate representation of exact tangent motion `mu_W=0`, only same-W destinations may receive positive rate. Native same-W moves satisfy

```text
10 Delta j + 7 Delta i=0
```

and hence are integer multiples of `(7,-10)`.

Therefore:

- lower a-interior band `j in {1,...,6}` lacks the forward same-W orientation `(-7,+10)` and cannot represent the admissible tangent ray `(-u,+u)`;
- upper a-interior band `j in {13,...,18}` lacks the reverse same-W orientation `(+7,-10)` and cannot represent `(+u,-u)`.

The period-7 residue structure proves that for every `N>=190` in the current regular-Regime-I symbolic family at least one obstructed a-interior exact-frontier column exists.

Thus the following four requirements cannot all hold over the full endpoint complement:

```text
actual native represented states only
+ nonnegative Markov rates
+ exact pointwise first-moment equality
+ exact same-process HJB/KFE law
```

This is a structural finite-process/lattice obstruction, not an accepted-household source error and not a KFE-side repair opportunity.

### 3.3 Boundary semantics preserved

The obstruction does not invalidate the finite W-domain or the continuous state-constraint law. In Regime I the continuous W face does not intersect `b=b_min`; the continuous triple intersection `a=a_max x b=b_min x W` occurs only at `W_max=8`. Discrete restricted-Voronoi W-contact is a separate cell-level boundary representation object.

---

## 4. Current roadmap position

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
Owner approximation/discretization route choice              NEXT — NOT YET AUTHORIZED
boundary-HJB / finite-process implementation                 BLOCKED PENDING ROUTE
global discrete-HJB implementation                           PENDING
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

## 5. Owner route decision — exact next scientific block, NOT YET AUTHORIZED

Outcome C requires choosing which discretization assumption may be relaxed before any implementation. Four bounded route families are now visible.

### Route A — asymptotically consistent endpoint approximation

Keep the accepted household economics, finite W-domain, native represented states, nonnegative/conservative Markov rows and one-Q HJB/KFE semantics, but relax **exact pointwise first-moment equality at the finite endpoint layer** to an explicitly quantified monotone/conservative approximation whose physical endpoint-layer error vanishes under fixed-aspect grid refinement.

A successor design would need to prove/refute:

- actual represented destinations only;
- nonnegative rates and `Q1=0` by construction;
- identical selected `Q` for HJB and future KFE;
- a pre-declared first-moment consistency error and its refinement order;
- endpoint-layer physical width tends to zero;
- no hidden normal leakage / no KFE repair;
- seam consistency with the accepted exact regular contract.

### Route B — boundary-state augmentation / boundary fitting

Add explicit represented boundary states or a boundary-fitted state geometry so both tangent orientations are exactly representable. This preserves exact moment matching but changes state geometry / mass cells and requires a new partition, adjacency, conservation and refinement proof.

### Route C — grid/aspect redesign

Change the lattice so the W tangent is grid-aligned or otherwise exactly representable at endpoints. This is more invasive because phase structure, regular wide stencils, accepted MATLAB/native-grid mapping and downstream evidence may need re-derivation.

### Route D — coordinate transformation

Move to a transformed representation such as `(a,W)` and re-derive the borrowing-floor, transfer-FOC, state partition and same-process boundary laws. This may flatten the W cap but relocates geometric complexity elsewhere.

No route is selected or authorized by this roadmap. Owner approval is required before publishing a successor Issue.

---

## 6. Scientific route recommendation for Owner consideration

The lowest-disruption route to investigate first is **Route A**, because it preserves the accepted household economics, W-domain, regular-region exact contracts, state partition family, conservation and one-Q semantics while relaxing only the requirement that caused the proven finite endpoint impossibility: exact pointwise first-moment equality at a finite number of near-endpoint lattice classes.

This is only a route recommendation. It is **not Builder authority** and does not pre-accept the approximation. A bounded successor should first prove consistency/convergence and fail closed if the approximation error does not vanish cleanly under refinement.

---

## 7. Same-process safeguards — frozen through the route decision

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

No candidate route may use pinning/normalization to repair leakage or create a KFE-only boundary process.

Stationary KFE remains explicitly blocked.

---

## 8. Interpretation ceiling

DLH-5V-F acceptance establishes a design-level structural obstruction and preserves the valid regular contracts. It does not authorize implementation, production generator assembly, HJB/KFE/stationary execution, numerical `W_max`, stationary existence/uniqueness, aggregates, GE, multi-region, neural, nominal, calibration, policy, welfare or Results prose.

---

## 9. Current governance pointers

- `tasks/TASK_INDEX_CURRENT.md`
- `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
- Issue #54 acceptance history.

The post-DLH-5V-E session handoff remains a historical checkpoint only.

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.
