# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.28  
**Date:** 2026-09-11  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** POST-DLH-5V-A CHECKPOINT — REGULAR RESTRICTED-VORONOI FRONTIER GEOMETRY ACCEPTED / MOMENT-CONE GATE NEXT

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

Stationary KFE remains **NOT AUTHORIZED** until one discrete finite controlled household process is fully selected, implemented, and validated.

Accepted finite production-domain family:

```text
D_W(W_max) = {
    0 <= a <= a_max,
    b >= b_min,
    a+b <= W_max
}
```

No numerical production `W_max` is selected.

Accepted continuous tangent laws remain:

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

The cells partition `D_W` a.e. Physical W activity is determined from the actual positive-length restricted-Voronoi cell intersection with `a+b=W_max`, not from the node-mask staircase.

Accepted discrete control / adjoint semantics remain:

```text
H_h(c,l,d) = u(c)-v(l) + sum_r q_{s->r}(c,l,d)[V_r-V_s] + switch
p_dot = Q^T p
p = M g
```

with downstream MATLAB-style component pin on mass `p` and original-residual validation.

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

DLH-5U established the restricted-Voronoi Route-F framework but did not close regular W-frontier tangential moment feasibility.

---

## 3. Operationally superseded broad DLH-5V / Issue #48

Issue #48 is CLOSED `not_planned` because its scope was too broad for the Builder context budget. It produced no accepted scientific result and carries no negative scientific verdict.

Its objective was split into smaller gates beginning with DLH-5V-A.

---

## 4. Accepted DLH-5V-A / Issue #49

Issue #49 result is scientifically accepted.

Accepted candidate:

`58a0efe2e85b497d8b19c306a831d865ed65136d`

Reviewer acceptance:

`5628285587`

Acceptance integration:

`46d6961100d1a050e6b313fa2e321180ed255226`

Accepted verdict:

`DLH_5VA_ACCEPTED__OUTCOME_A_CONFIRMED__REGULAR_RESTRICTED_VORONOI_FRONTIER_PHASE_AND_ADJACENCY_FROZEN__READY_FOR_MOMENT_CONE_GATE`

Accepted terminal:

`DLH_5VA_REGULAR_VORONOI_FRONTIER_PHASE_AND_ADJACENCY_FROZEN__READY_FOR_MOMENT_CONE_GATE`

### 4.1 Accepted regular-frontier phase classification

Exact grid:

```text
a_j = j*(10/19)
b_i = b_min + i*(7/19)
da = 10/19
db = 7/19
da/db = 10/7
```

Symbolic coordinates:

```text
kappa = 19*(W_max-b_min)
N = floor(kappa)
theta = kappa-N
```

Accepted facts:

- represented nodes satisfy `10j+7i<=N`; the node set is independent of `theta in [0,1)`;
- staircase-top defect is `r_j=(N-10j) mod 7=(N-3j) mod 7`;
- `r_{j+7}=r_j`: regular discrete phase is period 7 and fixed by `N mod 7`;
- theta shifts the physical W line affinely and does not create a regular structural phase break on `[0,1)`;
- each regular column contributes an active top A cell;
- the sub-top B cell is W-active iff `r_j in {0,1,2}`;
- deeper regular cells are not W-active;
- per full regular period: 7 A W-segments plus 3 B W-segments.

### 4.2 Accepted regular-frontier adjacency

For regular cells the accepted shared-face displacement families are:

```text
(-1,0), (1,0), (0,-1), (0,1), (-1,+1), (+1,-1)
```

with type-specific subsets:

- `INT`: four axial neighbors;
- `A^F`: left, below, NW diagonal, SE diagonal;
- `A^L`: left, below, NW diagonal only; `N_V=3`;
- W-active `B` (`r in {0,1,2}`): left, below, above, SE diagonal;
- non-W-active sub-top rectangle (`r in {3,4,5,6}`): four axial neighbors.

No oblique or longer regular shared-face neighbor is accepted.

This classification is now the exact geometric input for the next regular-frontier moment-cone gate.

---

## 5. Immediate next scientific object — regular-frontier geometric moment cone

No successor Issue is active yet.

The recommended next bounded gate should consume only the accepted DLH-5V-A regular type/displacement table and answer:

> for each accepted regular W-frontier class, does the nonnegative cone generated by its actual shared-face displacement vectors contain the continuous admissible tangential reallocation directions?

Mandatory test object:

```text
mu_a <= 0
mu_b >= 0
mu_a + mu_b <= 0
```

especially exact sliding:

```text
mu = (-u,+u),  u>0
```

The next gate should remain **geometry / moment-cone only** unless the cone result itself is fully closed. It should not simultaneously design rates, audit strict face-flux moments, close endpoints/corners, or implement HJB/KFE.

This continues the successful split-gate strategy adopted after Issue #48.

---

## 6. Planned sequence after regular moment-cone closure

```text
accepted DLH-5V-A regular phase + adjacency
-> regular-frontier geometric moment-cone gate
-> boundary-local rate / strict face-flux audit gate if geometrically feasible
-> endpoint/corner closure
-> boundary-HJB / Route-F implementation authority
-> KKT + discrete-generator validation
-> Wmax / resolution robustness
-> conservative same-process stationary-generator validation
-> Issue #27 stationary KFE
-> stationary aggregates C,L,A,B
-> two-region structural anchor
-> regional learned W^L
```

If the regular moment-cone gate proves a recurring-class obstruction, return to Owner for Route-F vs fallback route choice rather than forcing implementation.

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

Deep Learning does not initially replace HJB/KFE.

---

## 8. Current scientific ceiling

Until a successor Issue is activated, do not:

- mutate accepted household economics/source;
- compute or implement transition rates;
- audit/replace the face-flux moment map;
- close endpoint/corner transition classes;
- implement Route F / HJB / KFE;
- execute stationary KFE;
- choose numerical production `W_max`;
- compute stationary aggregates or rebuild two-region GE;
- enter multi-province execution, neural training, nominal HANK, calibration, policy, welfare, or Results.

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.
