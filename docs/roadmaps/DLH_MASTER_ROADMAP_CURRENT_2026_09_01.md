# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.32  
**Date:** 2026-09-11  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** POST-DLH-5V-C — W1 WIDE-STENCIL EXACT-TANGENT REGULAR FEASIBILITY ACCEPTED / RATE-DESIGN GATE NEXT

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

Accepted state-partition / same-process framework:

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

Physical displacement map is `((10/19)Delta j,(7/19)Delta i)`.

---

## 3. Accepted local shared-face obstruction — DLH-5V-B / Issue #50

Accepted candidate `6bc8612dc10de6d72d27c9c47d1b4d598a70a15d`; reviewer acceptance `5628629099`; integration `ff0afdf6d3fa0d770654613e42109318d638639d`.

Accepted cones:

```text
A^F: K = {7 mu_a + 10 mu_b <= 0}
A^L: K = {mu_a <= 0, 7 mu_a + 10 mu_b <= 0}
B^W: K = R^2
```

Exact sliding `(-u,+u)` is outside the recurring top-cell local shared-face cones because `7(-u)+10u=3u>0`. This proved the shared-face-only transition geometry insufficient, but did not invalidate the W-domain or W1/native coordinates.

---

## 4. Accepted W1 wide-stencil regular remedy — DLH-5V-C / Issue #51

Issue #51 is CLOSED completed.

Accepted candidate:

`2134a4b249eb0a79dc20d60ba1fdee830304f261`

Reviewer acceptance:

`5630191586`

Acceptance integration:

`cdbf1906963a9bf06cf117ba63072d2f1542d501`

Accepted verdict:

`DLH_5VC_ACCEPTED__OUTCOME_A_CONFIRMED__W1_WIDE_STENCIL_EXACT_TANGENT_REGULAR_FEASIBILITY_FROZEN__READY_FOR_WIDE_STENCIL_RATE_GATE`

Accepted terminal:

`DLH_5VC_W1_WIDE_STENCIL_EXACT_TANGENT_REGULAR_FEASIBILITY_FROZEN__READY_FOR_WIDE_STENCIL_RATE_GATE`

### 4.1 Primitive exact tangent

The native tangent equation

```text
10 Delta j + 7 Delta i = 0
```

has primitive reallocation direction

```text
(Delta j,Delta i)=(-7,+10),
Delta x_T=(-70/19,+70/19).
```

This is a **boundary wide-stencil Markov transition**, not a shared-face finite-volume flux.

### 4.2 Accepted regular-region feasibility

For recurring regular W-frontier states with `j>=7`:

- `(j-7,i+10)` is represented because `10(j-7)+7(i+10)=10j+7i`;
- the full straight segment remains inside `D_W` and satisfies `a+b=const`;
- `r_{j-7}=r_j`, hence A^F/A^L/B^W and top/sub-top offset are preserved;
- the finite endpoint band `j in {0,...,6}` is precisely deferred;
- the augmented displacement cone closes exactly:

```text
cone{(-10/19,0),(-70/19,+70/19)} = T_realloc.
```

For generic

```text
mu=(-a-b,+a), a>=0, b>=0,
```

the base-grid analytic feasibility coefficients are

```text
q_T  = 19a/70
q_in = 19b/10.
```

Under fixed-aspect refinement the physical wide jump is `O(h)`, required rates are `O(1/h)`, first-moment consistency is exact, and the smooth-test-function remainder is `O(h)`.

The identical wide edge may enter both the discrete HJB and forward `Q^T p`, preserving the one-process / one-`Q` law.

### 4.3 Acceptance ceiling

DLH-5V-C accepts regular-region **feasibility only**. It does not yet freeze:

- production control-dependent rate functions;
- activation / tie-breaking rules;
- endpoint/corner transition design;
- code implementation;
- numerical production `W_max`;
- stationary KFE.

---

## 5. Current roadmap position

```text
MATLAB-faithful two-asset household economics                 ACCEPTED
finite W-domain + continuous tangent/KKT law                 ACCEPTED
same-process HJB <=> KFE principle                           ACCEPTED
restricted-Voronoi state partition                           ACCEPTED
regular W-frontier phase classification                      ACCEPTED
regular W-frontier adjacency/displacements                   ACCEPTED
local shared-face geometric moment cone                      OBSTRUCTION ACCEPTED
Owner remedy route: W1 wide-stencil exact tangent            SELECTED
regular wide-stencil feasibility                             ACCEPTED (DLH-5V-C)
wide-stencil production rate / control-dependence design     NEXT BOUNDED GATE
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

The project remains in the final household-foundation / finite-boundary discrete-process design sequence before stationary KFE can safely resume.

---

## 6. Recommended next bounded gate

**Wide-stencil production rate / control-dependence design**.

The next gate should freeze, for regular W-active cells:

1. how the HJB-selected admissible boundary drift is decomposed into inward and exact-tangent components;
2. the nonnegative control-dependent CTMC rates on local inward and wide-tangent edges;
3. activation / zero-drift / tie-breaking semantics;
4. diagonal `Q_ss=-sum_{r!=s} q_sr` and no omitted exit rate;
5. exact reuse of the converged same `Q` in forward KFE;
6. consistency with the discrete Hamiltonian and the accepted `O(h)` refinement statement;
7. a strict distinction between this wide Markov transition and shared-face FV fluxes.

This gate should remain design-only. Endpoint/corner closure should stay separate unless the Owner explicitly combines them.

No successor Issue is active yet.

---

## 7. Downstream route after rate design

If the rate/control-dependence gate passes:

```text
wide-stencil rate/control design accepted
-> endpoint/corner closure
-> boundary-HJB / finite-process implementation
-> KKT + same-process generator validation
-> Wmax/resolution robustness
-> conservative stationary-generator validation
-> stationary KFE
-> aggregates C,L,A,B
-> two-region structural anchor rebuild
-> 3–5 province integration
-> learned W^L
```

If the rate gate finds a new regular-region obstruction, return to Owner route decision rather than forcing a KFE-only repair.

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

## 9. Scientific ceiling

Until a successor Owner-authorized Issue is activated, do not mutate accepted household economics/source; implement/freeze production wide-stencil rates; close endpoint/corner behavior; execute HJB/KFE/stationary; select numerical production `W_max`; compute aggregates/GE; enter multi-province/neural/nominal/calibration/policy/welfare/Results.

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.
