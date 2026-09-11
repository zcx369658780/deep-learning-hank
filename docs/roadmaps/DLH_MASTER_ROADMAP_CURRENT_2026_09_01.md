# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.29  
**Date:** 2026-09-11  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** CURRENT DLH-5V-B ACTIVE — REGULAR RESTRICTED-VORONOI GEOMETRIC MOMENT-CONE GATE

---

## 0. Long-run objective

Build a hybrid structural–learned regional HANK platform in which household HJB/KFE, aggregation, firm/accounting and later nominal-HANK equations remain explicit structural economics, while hard-to-specify cross-regional mappings become learned modules only after the household and equilibrium foundations pass scientific and numerical validation.

The first learned object remains the regional labor/spatial rule `W^L`. Neural training remains downstream.

---

## 1. Accepted household / finite-domain authority

Accepted household source:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Binding law:

```text
HJB boundary policy <=> KFE boundary transition law
```

Stationary KFE remains **NOT AUTHORIZED**.

Accepted finite production-domain family:

```text
D_W(W_max) = {
    0 <= a <= a_max,
    b >= b_min,
    a+b <= W_max
}
```

No numerical production `W_max` is selected.

Accepted continuous tangent laws:

```text
a=0:          mu_a >= 0
b=b_min:      mu_b >= 0
a=a_max:      mu_a <= 0
a+b=W_max:    mu_W=mu_a+mu_b <= 0
```

Accepted Route-F restricted-Voronoi framework:

```text
S = {s=(a_j,b_i): a_j+b_i<=W_max}
C_s = {x in D_W: ||x-s||<=||x-r|| for all represented r}
```

The cells partition `D_W` a.e. Physical W activity is determined by the actual restricted-Voronoi intersection with `a+b=W_max`, not by the node-mask staircase.

Accepted discrete control/adjoint framework remains:

```text
H_h(c,l,d) = u(c)-v(l) + sum_r q_{s->r}(c,l,d)[V_r-V_s] + switch
p_dot = Q^T p
p = M g
```

with downstream MATLAB-style component pin on mass `p` and validation against the original stationary equation.

---

## 2. Accepted DLH-5U / Issue #47

Accepted Rev-1 candidate:

`81bf9b46f20e6dd96514bb6fad698097c917a948`

Reviewer acceptance:

`5521379228`

Integration:

`060c2835825f9efff4f89c84646f04cab6a9c8a4`

Accepted verdict:

`DLH_5U_REV1_ACCEPTED__OUTCOME_B_CONFIRMED__ROUTE_F_FRAMEWORK_ACCEPTED__TANGENTIAL_SAME_PROCESS_CONSISTENCY_REMAINS_THE_SINGLE_BOUNDED_OPEN_OBJECT`

DLH-5U established the finite restricted-Voronoi Route-F framework, weighted mass/density semantics, discrete-Hamiltonian requirement, and one-`Q` HJB/KFE principle. It did not close tangential same-process consistency.

---

## 3. Accepted DLH-5V-A / Issue #49

Issue #49 is CLOSED completed.

Accepted candidate:

`58a0efe2e85b497d8b19c306a831d865ed65136d`

Reviewer acceptance:

`5628285587`

Acceptance integration:

`46d6961100d1a050e6b313fa2e321180ed255226`

Accepted verdict:

`DLH_5VA_ACCEPTED__OUTCOME_A_CONFIRMED__REGULAR_RESTRICTED_VORONOI_FRONTIER_PHASE_AND_ADJACENCY_FROZEN__READY_FOR_MOMENT_CONE_GATE`

Accepted regular-frontier results:

- represented node set is theta-independent inside each `kappa=N+theta`, `theta in [0,1)` slab;
- defect `r_j=(N-10j) mod 7=(N-3j) mod 7` gives period-7 regular phase structure;
- top A cells are always W-active; sub-top B cells are W-active iff `r_j in {0,1,2}`;
- regular restricted-Voronoi adjacency contains only axial and NW/SE diagonal neighbors; no oblique or longer shared-face regular neighbor;
- exact physical displacement map is `((10/19)Delta j,(7/19)Delta i)`.

Accepted W-active regular classes:

```text
A^F: (-1,0), (0,-1), (-1,+1), (+1,-1)
A^L: (-1,0), (0,-1), (-1,+1)
B^W: (-1,0), (0,-1), (0,+1), (+1,-1)
```

Endpoints/corners remain deferred.

---

## 4. Owner continuation decision

Owner approved:

`APPROVE_DLH_5VB_REGULAR_VORONOI_GEOMETRIC_MOMENT_CONE_GATE`

The original broad DLH-5V objective remains decomposed into small independently reviewed scientific gates to avoid context-budget failure and to distinguish geometry, cone feasibility, rate design, endpoints and implementation.

---

## 5. Immediate active gate — DLH-5V-B / Issue #50

### Name

**Regular Restricted-Voronoi Geometric Moment-Cone Analysis**

Task type:

`SCIENTIFIC_DESIGN__REGULAR_VORONOI_GEOMETRIC_MOMENT_CONE`

Dedicated branch:

`dsh/issue-50-dlh-5vb-regular-voronoi-moment-cone-2026-09-11`

DLH-5V-B is design-only.

### 5.1 Exact object

For each accepted W-active regular class define the nonnegative physical displacement cone

```text
K_s = cone{Delta x_sr}
```

and compare it with

```text
T_realloc = {mu_a<=0, mu_b>=0, mu_a+mu_b<=0}.
```

Mandatory exact sliding ray:

```text
mu=(-u,+u), u>0.
```

The gate must determine whether the full continuous tangential cone is representable using nonnegative coefficients on the accepted local shared-face geometry.

### 5.2 Interpretation limit

A failure may establish only that the **current local shared-face restricted-Voronoi transition geometry** is insufficient for a recurring class. It does not by itself prove every possible Route-F discretization impossible.

Possible remedies, if needed, are reserved for a later Owner route decision.

### 5.3 Explicitly deferred

DLH-5V-B does not cover:

- production transition-rate formula;
- strict source-state face-flux moment audit;
- endpoint/corner closure;
- alternative/nonlocal transition construction;
- HJB/KFE implementation;
- stationary KFE;
- numerical `W_max` selection;
- aggregates / GE / learned modules.

---

## 6. Current roadmap position

The household stationary-foundation route is now:

```text
MATLAB-faithful two-asset household economics                 ACCEPTED
finite W-domain + continuous tangent/KKT law                 ACCEPTED
same-process HJB <=> KFE principle                           ACCEPTED
restricted-Voronoi finite-volume framework                   ACCEPTED
regular W-frontier phase classification                      ACCEPTED
regular W-frontier actual adjacency/displacements            ACCEPTED
regular geometric moment-cone feasibility                    ACTIVE (DLH-5V-B)
boundary-local rate / strict face-flux audit                 PENDING
endpoint/corner closure                                      PENDING
boundary-HJB / Route-F implementation                        PENDING
KKT + same-process discrete-generator validation             PENDING
nested Wmax / resolution robustness                          PENDING
conservative stationary-generator validation                 PENDING
Issue #27 stationary KFE                                     NOT AUTHORIZED YET
stationary C,L,A,B                                           PENDING
two-region structural anchor rebuild                         PENDING
3–5 province integration                                     PENDING
learned regional W^L                                         PENDING
```

This means the project is **well inside the household-foundation / finite-boundary discretization stage**. The structural economic core is substantially established, but the project has not yet returned to stationary KFE, regional GE execution or neural training.

---

## 7. Branching after DLH-5V-B

If the full regular tangential cone is geometrically representable:

```text
DLH-5V-B accepted
-> boundary-local rate / strict face-flux audit
-> endpoint/corner closure
-> boundary-HJB / Route-F implementation
-> KKT + same-process generator validation
-> Wmax/resolution robustness
-> conservative stationary-generator validation
-> stationary KFE
-> aggregates
-> regional GE
```

If a recurring regular-class obstruction is proven:

```text
DLH-5V-B obstruction
-> Owner bounded route decision
   (e.g. whether to alter local transition semantics, consider a nonlocal/augmented boundary construction, or reassess coordinate/domain representation)
-> only then resume implementation design
```

No remedy is pre-authorized by this roadmap.

---

## 8. Regional / Deep Learning route remains downstream

Long-run hybrid architecture remains:

```text
learned regional mapping W^L
        ↓
composite regional wage / flow interface
        ↓
structural regional two-asset HA (HJB/KFE)
        ↓
C_i, L_i^home, A_i, B_i
        ↓
labor-flow allocation + structural firm block
        ↓
w_i, r_i^a
        ↓
outer equilibrium fixed point
        ↓
back to HA
```

Scaling hierarchy remains:

```text
2-region structural/unit anchor
-> 3–5 province integration fixture
-> 31-province empirical/source benchmark
```

Learned `W^L`, later `W^K`, nominal HANK, automated calibration, policy and welfare remain deferred until the controlled household stationary foundation is scientifically accepted.

---

## 9. Progress by major research layer

| Layer | Current state |
|---|---|
| Scientific constitution / reproducibility / governance | accepted and operational |
| Tier-0 baseline / early HANK architecture | accepted foundation |
| Two-asset MATLAB-faithful household economics | accepted |
| Finite production-domain economics + continuous boundary law | accepted |
| Restricted-Voronoi discrete geometry framework | accepted |
| Regular W-frontier geometry / adjacency | accepted |
| Regular tangential moment feasibility | active |
| Boundary transition-rate closure | pending |
| Endpoint/corner closure | pending |
| Production boundary HJB / same-process generator implementation | pending |
| Stationary KFE + aggregates | pending |
| Two-region / multi-region structural execution rebuild | pending |
| Learned `W^L` regional network | designed conceptually, not yet implemented/trained |
| `W^K`, nominal HANK, calibration, policy, welfare | later roadmap |

The project should therefore not be described as being near final empirical/neural execution yet. It has moved beyond household-equation correctness and domain selection into the final sequence of **finite-boundary discrete-process design gates** required before stationary KFE can safely resume.

---

## 10. Scientific ceiling during DLH-5V-B

Do not mutate accepted household economics/source; redo broad frontier enumeration; design production rates; audit strict face-flux moments; close endpoints/corners; implement/execute HJB/KFE/stationary; select numerical `W_max`; compute stationary aggregates/GE; enter multi-province/neural/nominal/calibration/policy/welfare/Results.

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.
