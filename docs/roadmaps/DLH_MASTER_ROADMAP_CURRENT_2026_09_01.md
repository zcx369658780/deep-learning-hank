# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.38  
**Date:** 2026-09-11  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** DLH-5V-F / ISSUE #54 ACTIVE — ENDPOINT-BAND / JOINT-BOUNDARY FINITE-PROCESS CLOSURE

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
D_W(W_max) = {0<=a<=a_max, b>=b_min, a+b<=W_max}
```

Independent upper-a grid authority:

```text
a_max = 10
a_j = j*(10/19)
j_max = 19
```

No numerical production `W_max` is selected.

Binding law:

```text
HJB boundary policy <=> KFE boundary transition law
```

Restricted-Voronoi cells remain the state partition / mass-volume geometry. The same controlled backward generator `Q` must define both the discrete HJB transition term and the forward mass dynamics `p_dot=Q^T p`.

Stationary KFE remains **NOT AUTHORIZED**.

---

## 2. Accepted regular-frontier design chain — DLH-5V-A through DLH-5V-E

### DLH-5V-A / Issue #49 — phase / adjacency — ACCEPTED

Frozen grid:

```text
da=10/19
db=7/19
10j+7i<=N
```

Regular W-frontier phase is period 7:

```text
i_t(j)=floor((N-10j)/7)
r_j=(N-10j) mod 7
r_{j+7}=r_j
```

### DLH-5V-B / Issue #50 — local shared-face moment cone — OBSTRUCTION ACCEPTED

Shared-face-only local geometry cannot represent exact W-tangent sliding on recurring top-cell classes. This bounded obstruction rejected the shared-face-only route, not the W-domain or native coordinates.

### DLH-5V-C / Issue #51 — forward exact-tangent wide stencil — ACCEPTED

```text
(Delta j,Delta i)=(-7,+10)
w_T=(-70/19,+70/19)
(j,i)->(j-7,i+10)
```

valid on the recurring regular W-active region with `j>=7`.

### DLH-5V-D / Issue #52 — forward/reallocation rate contract — ACCEPTED

For

```text
T_realloc={mu_a<=0,mu_b>=0,mu_W<=0}
```

accepted rates are

```text
w_in=(-10/19,0)
w_T=(-70/19,+70/19)
q_in=19*(-mu_W)/10
q_T=19*mu_b/70
```

with candidate-specific rates entering discrete `H_h` before selection.

### DLH-5V-E / Issue #53 — full recurring regular W-frontier closure — ACCEPTED / CLOSED

Accepted candidate:

`ff4607ff74ab1e0cea530ba04f17045698f43a62`

Reviewer acceptance:

`5632150936`

Acceptance integration:

`28e42e4c0f65d03aa403cf7aeedb60b83c7837e2`

Accepted verdict:

`DLH_5VE_ACCEPTED__OUTCOME_A_CONFIRMED__FULL_REGULAR_W_BOUNDARY_SECTOR_CONTRACT_FROZEN__READY_FOR_ENDPOINT_JOINT_BOUNDARY_GATE`

Reverse reallocation:

```text
R_reverse={mu_a>0,mu_b<0,mu_W<=0}
w_RT=(+70/19,-70/19)
w_down=(0,-7/19)
q_RT=19*mu_a/70
q_down=19*(-mu_W)/7
(j,i)->(j+7,i-10)
```

with independent availability conditions `j<=12`, `i>=10`.

Both-inward depletion:

```text
R_deplete={mu_a<=0,mu_b<0}
w_left=(-10/19,0)
w_down=(0,-7/19)
q_left=19*(-mu_a)/10
q_down=19*(-mu_b)/7
```

On the common regular region

```text
7<=j<=12
i>=10
```

plus accepted regular W-active/class conditions:

```text
T_W={mu_W<=0}
 = T_realloc union R_reverse union R_deplete
```

Every regular candidate receives exactly one sector-specific discrete-Hamiltonian score before ONE global argmax. The selected rates define ONE conservative backward `Q`; future KFE must consume exactly `Q^T`.

---

## 3. Current active scientific gate — DLH-5V-F / Issue #54

Title:

`DLH-5V-F: Close endpoint bands and joint-boundary finite-process contract`

Task type:

`SCIENTIFIC_DESIGN__ENDPOINT_BAND_AND_JOINT_BOUNDARY_FINITE_PROCESS_CLOSURE`

Owner decision:

`APPROVE_DLH_5VF_ENDPOINT_BAND_AND_JOINT_BOUNDARY_FINITE_PROCESS_CLOSURE_GATE`

Authoritative activation comment:

`5632596303`

Authority marker:

`DLH_5VF_ENDPOINT_BAND_AND_JOINT_BOUNDARY_FINITE_PROCESS_CLOSURE_AUTHORIZED`

Dedicated Builder branch:

`dsh/issue-54-dlh-5vf-endpoint-joint-boundary-2026-09-11`

Issue #54 is the active Builder authority while OPEN and while fresh CURRENT governance remains synchronized to this identity. DSH must fresh-fetch before any mutation.

### 3.1 Exact state-space complement

```text
lower-a forward-wide band: j in {0,...,6}
upper-a mirror-wide band:  j in {13,...,19}
lower-b mirror-wide band:  i in {0,...,9}
```

plus their intersections, W-active endpoint cells and true economic corners/joint faces.

### 3.2 Critical distinction: numerical reachability versus economic faces

A reachability band is not an economic boundary face:

```text
actual a=0 face:       j=0 only
actual a=a_max face:   j=19 only
actual b=b_min face:   i=0 only
```

Thus `j=1,...,6`, `j=13,...,18`, and `i=1,...,9` remain interior in the corresponding asset coordinate unless another economic face is active.

Continuous tangent/KKT restrictions apply only on actually active faces, jointly at intersections:

```text
a=0:       mu_a>=0
b=b_min:   mu_b>=0
a=a_max:   mu_a<=0
W:         mu_a+mu_b<=0
```

### 3.3 Exact scientific sequence

Issue #54 proceeds in this order:

```text
state taxonomy
 -> economic active-set cone + transition-reachability flags
 -> actual represented native-grid destination set
 -> nonnegative represented first-moment cone
 -> compare with continuous admissible cone
 -> derive exact candidate rates/scoring where feasible
 -> prove regular/endpoint seam consistency
 -> freeze conservative row law using actual destinations only
 -> either full design closure or a bounded obstruction certificate
```

Exact W-tangent native-grid identity:

```text
10 Delta j + 7 Delta i = 0
```

Primitive same-W lattice displacement is generated by `(-7,+10)` / `(+7,-10)`. The gate must determine rather than assume whether exact tangent coverage survives when these regular destinations are unavailable.

### 3.4 Scientific fail-closed requirements

Do not:

- silently clamp an unavailable wide transition;
- omit an off-grid destination while retaining diagonal escape;
- introduce ghost/interpolation/virtual states or reflected KFE mass;
- let KFE independently rebuild the HJB boundary process;
- change grid/domain/household economics to manufacture closure;
- weaken exact process matching inside this gate.

A proof that a continuously admissible deferred-state drift cannot lie in the nonnegative cone of actual represented native-grid displacements is a legitimate scientific obstruction and requires an Owner route decision.

---

## 4. Same-process generator safeguards — frozen

```text
Q = backward controlled generator
Q^T = forward mass operator
Q_ij >= 0 for i != j
Q_ii = -sum of ACTUAL represented outgoing rates
Q1 = 0 by construction
same selected Q for HJB and KFE
p=Mg
p_dot=Q^T p
```

Issue #27 component-pin semantics remain unchanged: pin/normalization fixes scale only, never leakage; validate the original source-free equation downstream.

Stationary KFE remains explicitly blocked until the global finite controlled process has been implemented and validated.

---

## 5. Current roadmap position

```text
MATLAB-faithful two-asset household economics                 ACCEPTED
finite W-domain + continuous tangent/KKT law                 ACCEPTED
same-process HJB <=> KFE principle                           ACCEPTED
restricted-Voronoi state partition                           ACCEPTED
regular W-frontier phase / adjacency                         ACCEPTED
local shared-face-only process                               OBSTRUCTION ACCEPTED
forward exact-tangent wide stencil                           ACCEPTED
T_realloc control-dependent rates + conservative-Q semantics ACCEPTED
remaining regular W-boundary sectors                         ACCEPTED
full recurring regular W-frontier scoring                    ACCEPTED
endpoint-band / joint-boundary finite-process closure         ACTIVE — ISSUE #54
boundary-HJB / finite-process implementation                 PENDING
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

---

## 6. Issue #54 terminal decision structure

Full design closure:

`DLH_5VF_ENDPOINT_JOINT_BOUNDARY_FINITE_PROCESS_CONTRACT_FROZEN__READY_FOR_BOUNDARY_HJB_IMPLEMENTATION_GATE`

Sharply bounded unresolved class:

`DLH_5VF_ENDPOINT_JOINT_BOUNDARY_PARTIAL__ONE_BOUNDED_CLASS_REMAINS_UNRESOLVED`

Finite-process representability obstruction:

`DLH_5VF_ENDPOINT_JOINT_BOUNDARY_FINITE_PROCESS_OBSTRUCTION__OWNER_ROUTE_DECISION_REQUIRED`

Authority inconsistency:

`BLOCKED_DLH_5VF_ACCEPTED_SOURCE_OR_PRIOR_AUTHORITY_INCONSISTENCY`

This is deliberately not a PASS-seeking gate.

---

## 7. Downstream route after DLH-5V-F

If and only if the endpoint/joint process is scientifically closable and accepted:

```text
boundary-HJB / finite-process implementation
 -> global discrete-HJB implementation
 -> same-process Q validation + SCC/closed-class diagnostics
 -> nested Wmax / resolution robustness
 -> conservative stationary-generator validation
 -> Issue #27 stationary KFE
 -> stationary aggregates C,L,A,B
 -> two-region structural anchor rebuild
 -> 3–5 province integration
 -> learned regional W^L
```

If Issue #54 returns a structural representability obstruction, Owner chooses the next grid/discretization/domain route before implementation.

---

## 8. Interpretation ceiling

DLH-5V-F is design-only. It does not authorize implementation, HJB/KFE execution, stationary computation, numerical `W_max`, aggregates, GE, multi-region, neural, nominal, calibration, policy, welfare, or Results prose.

---

## 9. Current governance pointers

- `tasks/TASK_INDEX_CURRENT.md`
- `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
- Issue #54 body/comments.

`docs/governance/DLH_SESSION_HANDOFF_CURRENT_2026_09_11_POST_5VE.md` is retained as the historical post-DLH-5V-E conversation checkpoint; it does not override later synchronized CURRENT governance.

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.
