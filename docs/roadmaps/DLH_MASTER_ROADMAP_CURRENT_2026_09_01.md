# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.31  
**Date:** 2026-09-11  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** CURRENT DLH-5V-C ACTIVE — W1 WIDE-STENCIL EXACT-TANGENT REGULAR FEASIBILITY AUDIT

---

## 0. Long-run objective

Build a hybrid structural–learned regional HANK platform in which household HJB/KFE, aggregation, firm/accounting and later nominal-HANK equations remain explicit structural economics, while hard-to-specify cross-regional mappings become learned modules only after the household and equilibrium foundations pass scientific and numerical validation.

The first learned object remains the regional labor/spatial rule `W^L`. Neural training remains downstream.

---

## 1. Accepted household / finite-domain foundation

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
D_W(W_max) = {0<=a<=a_max, b>=b_min, a+b<=W_max}
```

Accepted continuous tangent laws:

```text
a=0:          mu_a >= 0
b=b_min:      mu_b >= 0
a=a_max:      mu_a <= 0
a+b=W_max:    mu_a+mu_b <= 0
```

Accepted Route-F restricted-Voronoi state partition and discrete same-process semantics remain:

```text
S = {s=(a_j,b_i): a_j+b_i<=W_max}
C_s = {x in D_W: ||x-s||<=||x-r|| for all represented r}
H_h = u-v + sum_r q_{s->r}[V_r-V_s] + switch
p_dot = Q^T p
p = M g
```

The same `Q` must define backward HJB and forward mass dynamics.

---

## 2. Accepted regular-frontier geometry — DLH-5V-A / Issue #49

Accepted candidate `58a0efe2e85b497d8b19c306a831d865ed65136d`; reviewer acceptance `5628285587`; integration `46d6961100d1a050e6b313fa2e321180ed255226`.

Exact grid:

```text
da=10/19, db=7/19, da/db=10/7
```

Regular W-frontier phase is period 7. Accepted W-active local adjacency classes in index units:

```text
A^F: (-1,0), (0,-1), (-1,+1), (+1,-1)
A^L: (-1,0), (0,-1), (-1,+1)
B^W: (-1,0), (0,-1), (0,+1), (+1,-1)
```

Physical displacement map is `((10/19)Delta j,(7/19)Delta i)`. Endpoints/corners remain deferred.

---

## 3. Accepted local shared-face obstruction — DLH-5V-B / Issue #50

Issue #50 is CLOSED completed.

Accepted candidate:

`6bc8612dc10de6d72d27c9c47d1b4d598a70a15d`

Reviewer acceptance:

`5628629099`

Acceptance integration:

`ff0afdf6d3fa0d770654613e42109318d638639d`

Accepted verdict:

`DLH_5VB_ACCEPTED__OUTCOME_C_CONFIRMED__REGULAR_LOCAL_SHARED_FACE_MOMENT_CONE_OBSTRUCTION_PROVEN__OWNER_ROUTE_DECISION_REQUIRED`

Accepted cones:

```text
A^F: K = {7 mu_a + 10 mu_b <= 0}
A^L: K = {mu_a <= 0, 7 mu_a + 10 mu_b <= 0}
B^W: K = R^2
```

Exact sliding `(-u,+u)` is outside the recurring top-cell local shared-face cones because `7(-u)+10u=3u>0`. The current local shared-face geometry is therefore insufficient, but this bounded obstruction does not invalidate the W-domain or every W1/Route-F discretization.

---

## 4. Owner route decision

Owner approved:

`APPROVE_ROUTE_F_WIDE__W1_NATIVE_EXACT_TANGENT_REGULAR_AUDIT`

The next remedy audit keeps native `(a,b,z)`, the accepted finite W-domain, and the same-process law, but allows a **boundary wide-stencil/non-shared-face Markov transition** rather than requiring every W-boundary transition to follow an actual Voronoi shared face.

Primary exact lattice tangent:

```text
10 Delta j + 7 Delta i = 0
(Delta j,Delta i)=(-7,+10)
Delta x=(-70/19,+70/19)
```

This candidate is not yet accepted. Issue #51 must determine whether it is scientifically viable on recurring regular frontier states.

---

## 5. Immediate active gate — DLH-5V-C / Issue #51

### Name

**W1 Wide-Stencil Exact-Tangent Regular-Frontier Feasibility Audit**

Task type:

`SCIENTIFIC_DESIGN__W1_WIDE_STENCIL_EXACT_TANGENT_REGULAR_FEASIBILITY`

Dedicated branch:

`dsh/issue-51-dlh-5vc-w1-wide-stencil-tangent-2026-09-11`

### 5.1 Required closure

DLH-5V-C must prove or refute, for recurring regular `A^F`, `A^L`, and `B^W` states away from endpoint/joint-boundary regions:

- primitive/minimal exact tangent construction;
- represented destination `(j-7,i+10)` and full segment domain admissibility;
- period-7 phase/class preservation;
- exact closure of `T_realloc` when the wide tangent is combined with the local inward `(-1,0)` direction;
- existence of nonnegative CTMC first-moment coefficients as an analytic feasibility certificate;
- physical locality under the fixed-aspect refinement family `da_h=h*10/19`, `db_h=h*7/19`;
- smooth-test-function consistency and remainder order;
- coherent use of the identical wide transition in HJB and KFE without pretending it is a shared-face finite-volume flux.

### 5.2 Explicit ceiling

This gate does not authorize production rate functions, endpoint/corner closure, code implementation, numerical `W_max`, HJB/KFE/stationary execution, aggregates, GE, or neural work.

A regular-region pass only establishes that the wide-stencil remedy is worth carrying into a later rate/endpoint gate.

---

## 6. Current roadmap position

```text
MATLAB-faithful two-asset household economics                 ACCEPTED
finite W-domain + continuous tangent/KKT law                 ACCEPTED
same-process HJB <=> KFE principle                           ACCEPTED
restricted-Voronoi state partition                           ACCEPTED
regular W-frontier phase classification                      ACCEPTED
regular W-frontier adjacency/displacements                   ACCEPTED
local shared-face geometric moment cone                      OBSTRUCTION ACCEPTED
Owner remedy route: W1 wide-stencil exact tangent            SELECTED FOR AUDIT
regular wide-stencil feasibility                             ACTIVE (DLH-5V-C)
wide-stencil production rate design                          PENDING
endpoint/corner closure                                      PENDING
boundary-HJB / finite-process implementation                 PENDING
KKT + same-process discrete-generator validation             PENDING
nested Wmax / resolution robustness                          PENDING
conservative stationary-generator validation                 PENDING
Issue #27 stationary KFE                                     NOT AUTHORIZED
stationary C,L,A,B                                           PENDING
two-region structural anchor rebuild                         PENDING
3–5 province integration                                     PENDING
learned regional W^L                                         PENDING
```

The project remains in the household-foundation / finite-boundary discrete-process stage. Stationary KFE, regional GE and neural training remain downstream.

---

## 7. Branching after DLH-5V-C

If regular wide-stencil feasibility passes:

```text
DLH-5V-C accepted
-> bounded production rate / control-dependence design
-> endpoint/corner closure
-> boundary-HJB / finite-process implementation
-> KKT + same-process generator validation
-> Wmax/resolution robustness
-> conservative stationary-generator validation
-> stationary KFE
-> aggregates
-> regional GE
```

If a recurring regular-region obstruction is proven:

```text
DLH-5V-C obstruction
-> Owner route decision
   (augmented boundary/face states, transformed coordinates/W2, or another bounded alternative)
```

No fallback remedy is pre-authorized.

---

## 8. Regional / Deep Learning architecture remains downstream

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

## 9. Scientific ceiling during DLH-5V-C

Do not mutate accepted household economics/source; change the production grid; implement wide-stencil code; assemble a production generator; freeze production rate functions; close endpoint/corner transitions; execute HJB/KFE/stationary; select numerical production `W_max`; compute stationary aggregates/GE; enter multi-province/neural/nominal/calibration/policy/welfare/Results.

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.
