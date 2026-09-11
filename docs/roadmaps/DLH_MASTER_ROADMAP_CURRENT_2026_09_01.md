# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.30  
**Date:** 2026-09-11  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** POST-DLH-5V-B — REGULAR LOCAL SHARED-FACE MOMENT-CONE OBSTRUCTION ACCEPTED / OWNER ROUTE DECISION REQUIRED

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

Accepted Route-F restricted-Voronoi framework:

```text
S = {s=(a_j,b_i): a_j+b_i<=W_max}
C_s = {x in D_W: ||x-s||<=||x-r|| for all represented r}
```

Accepted discrete control/adjoint semantics remain:

```text
H_h(c,l,d) = u(c)-v(l) + sum_r q_{s->r}(c,l,d)[V_r-V_s] + switch
p_dot = Q^T p
p = M g
```

with MATLAB-style downstream component pin and original-equation residual validation.

---

## 2. Accepted regular-frontier geometry — DLH-5V-A / Issue #49

Accepted candidate `58a0efe2e85b497d8b19c306a831d865ed65136d`; reviewer acceptance `5628285587`; integration `46d6961100d1a050e6b313fa2e321180ed255226`.

Exact grid:

```text
da=10/19, db=7/19, da/db=10/7
```

Regular phase is period 7. Accepted W-active local adjacency classes in index units:

```text
A^F: (-1,0), (0,-1), (-1,+1), (+1,-1)
A^L: (-1,0), (0,-1), (-1,+1)
B^W: (-1,0), (0,-1), (0,+1), (+1,-1)
```

Physical displacement map is `((10/19)Delta j,(7/19)Delta i)`. No oblique or longer **shared-face** regular neighbor is accepted. Endpoints/corners remain deferred.

---

## 3. Accepted geometric obstruction — DLH-5V-B / Issue #50

Issue #50 is CLOSED completed.

Accepted candidate:

`6bc8612dc10de6d72d27c9c47d1b4d598a70a15d`

Reviewer acceptance:

`5628629099`

Acceptance integration:

`ff0afdf6d3fa0d770654613e42109318d638639d`

Accepted verdict:

`DLH_5VB_ACCEPTED__OUTCOME_C_CONFIRMED__REGULAR_LOCAL_SHARED_FACE_MOMENT_CONE_OBSTRUCTION_PROVEN__OWNER_ROUTE_DECISION_REQUIRED`

Exact accepted cones:

```text
A^F: K = {7 mu_a + 10 mu_b <= 0}
A^L: K = {mu_a <= 0, 7 mu_a + 10 mu_b <= 0}
B^W: K = R^2
```

The continuous admissible W-boundary reallocation cone contains exact sliding `(-u,+u)`. For recurring top-cell classes `A^F` and `A^L`, the separating functional gives

```text
7(-u)+10(+u)=3u>0,
```

so exact physical sliding is outside the local nonnegative shared-face cone. Equivalently the available NW physical diagonal has slope `7/10`, below the required tangent slope `1`.

Therefore the current restricted-Voronoi **local shared-face** transition geometry cannot represent the full continuous tangential cone everywhere on the regular W frontier while preserving monotone nonnegative local CTMC coefficients.

This is a bounded obstruction. It does not prove the W-domain invalid and does not prove every Route-F discretization impossible.

---

## 4. Current branch point — Owner route decision

There is no active Builder Issue.

Do **not** proceed to production rate design, strict face-flux audit or boundary-HJB implementation using the rejected local shared-face geometry.

The next bounded scientific task should compare remedy routes before implementation. The leading candidate to audit is:

### Route F-WIDE — W1/native wide-stencil tangent transport

Retain native `(a,b,z)`, the economic borrowing floor alignment, and the artificial high-wealth W boundary. The minimal exact lattice tangent solves

```text
10 Delta j + 7 Delta i = 0,
```

with primitive integer solution such as

```text
Delta j=-7, Delta i=+10,
```

which maps to physical displacement proportional to `(-70/19,+70/19)` and therefore lies exactly on `mu_a+mu_b=0`.

This is **not accepted and not authorized**. A successor design gate would need to prove represented-destination availability across regular phases, monotonicity, conservation, same-process HJB/KFE compatibility, refinement/locality semantics and whether the long jump is scientifically acceptable.

Alternative bounded routes include augmented boundary/face states and reassessment of transformed-coordinate/W2 constructions. Prior design preference remains to keep numerical geometric complexity at the artificial high-wealth boundary rather than move the economic borrowing floor off-axis, unless evidence overturns that preference.

---

## 5. Current roadmap position

```text
MATLAB-faithful two-asset household economics                 ACCEPTED
finite W-domain + continuous tangent/KKT law                 ACCEPTED
same-process HJB <=> KFE principle                           ACCEPTED
restricted-Voronoi finite-volume framework                   ACCEPTED
regular W-frontier phase classification                      ACCEPTED
regular W-frontier adjacency/displacements                   ACCEPTED
local shared-face geometric moment cone                      OBSTRUCTION ACCEPTED
Owner bounded remedy route decision                          CURRENT
remedy geometry / transition design                          PENDING
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

The project is still in the household-foundation / finite-boundary discrete-process stage. The structural economic core and finite-domain law are substantially established, but stationary KFE, regional GE execution and neural training remain downstream.

---

## 6. Downstream route after a remedy is accepted

If a bounded remedy closes the tangential process consistently:

```text
remedy transition geometry accepted
-> endpoint/corner closure
-> boundary-HJB / finite-process implementation
-> KKT + same-process generator validation
-> Wmax/resolution robustness
-> conservative stationary-generator validation
-> Issue #27 stationary KFE
-> stationary aggregates C,L,A,B
-> two-region structural anchor rebuild
-> 3–5 province integration
-> learned W^L
```

If all bounded W1 remedies fail, the Owner should reassess coordinate/domain representation rather than force a KFE-only repair.

---

## 7. Regional / Deep Learning architecture remains downstream

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

## 8. Scientific ceiling

Until a successor Owner-authorized Issue is activated, do not mutate accepted economics/source; design production rates on the rejected local geometry; implement/execute HJB/KFE/stationary; select numerical production `W_max`; compute stationary aggregates/GE; enter multi-province/neural/nominal/calibration/policy/welfare/Results.

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.
