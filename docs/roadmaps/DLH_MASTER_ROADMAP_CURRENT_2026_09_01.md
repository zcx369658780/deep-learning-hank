# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.27  
**Date:** 2026-09-10  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** CURRENT SPLIT DLH-5V-A — REGULAR RESTRICTED-VORONOI FRONTIER PHASE / ADJACENCY DESIGN ACTIVE

---

## 0. Long-run objective

Build a hybrid structural–learned regional HANK platform in which household HJB/KFE, aggregation, firm/accounting and later nominal-HANK equations remain explicit structural economics, while hard-to-specify cross-regional mappings become learned modules only after the household and equilibrium foundations pass scientific and numerical validation.

The first learned object remains the regional labor/spatial rule `W^L`. Neural training remains downstream.

---

## 1. Accepted household / finite-domain authority through DLH-5U

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

The cells partition `D_W` a.e. Physical W activity is determined from the actual restricted-Voronoi cell intersection with `a+b=W_max`, not the node-mask staircase.

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

The remaining scientific object is W-frontier tangential same-process consistency on the actual restricted-Voronoi adjacency graph. The old axial cascade is not accepted as first-order-consistent evidence.

---

## 3. Superseded broad DLH-5V / Issue #48

Issue #48 attempted to combine regular frontier phase classification, Voronoi adjacency, geometric moment cones, face-flux moment audit, alternative rate construction, endpoints/corners and refinement closure in a single design gate.

The Builder repeatedly exhausted its context/output budget during startup/reference loading before producing any candidate artifact. Issue #48 is therefore CLOSED `not_planned` and superseded for **operational scope reasons only**.

No scientific conclusion was produced by Issue #48. No candidate commit or remote Builder branch existed. Accepted DLH-5U authority remains unchanged.

---

## 4. Owner split-gate decision

Owner approved:

`APPROVE_DLH_5VA_SPLIT_GATE__REGULAR_FRONTIER_PHASE_ADJACENCY_ONLY`

The old DLH-5V objective is now decomposed into bounded gates. The first replacement gate closes only the regular nondegenerate restricted-Voronoi frontier geometry.

---

## 5. Immediate active gate — DLH-5V-A / Issue #49

### Name

**Regular Restricted-Voronoi W-Frontier Phase and Adjacency Classification**

Task type:

`SCIENTIFIC_DESIGN__REGULAR_VORONOI_FRONTIER_PHASE_AND_ADJACENCY_CLASSIFICATION`

Dedicated branch:

`dsh/issue-49-dlh-5va-voronoi-frontier-phase-adjacency-2026-09-10`

### 5.1 Exact scope

Work only on regular nondegenerate W-frontier cells away from `a=0`, `a=a_max`, and `b=b_min` intersections.

Exact grid authority:

```text
a_j = j*(10/19)
b_i = b_min + i*(7/19)
da = 10/19
db = 7/19
da/db = 10/7
```

Symbolic phase variables suggested by the issue:

```text
kappa = 19*(W_max-b_min)
N = floor(kappa)
theta = kappa-N
10*j + 7*i <= kappa
```

The Builder must derive the finite recurring regular phase structure and actual restricted-Voronoi shared-face adjacency/displacements. It may not assume the Voronoi graph is axial-only.

### 5.2 Explicitly deferred

The following do **not** belong to DLH-5V-A:

- geometric moment cones;
- exact sliding `(-1,+1)` containment;
- source-state face-flux moment map;
- nonnegative transition-rate construction;
- endpoint/corner closure;
- sliver agglomeration semantics;
- HJB/KFE implementation;
- stationary KFE;
- numerical `W_max` selection.

### 5.3 Context-budget policy

To avoid the Issue #48 failure, the scientific startup is deliberately minimal. After CURRENT rules/governance and Issue #49, only the accepted DLH-5U umbrella design and the DLH-5U restricted-Voronoi geometry report are required scientific reads. The Builder should not narrate each read and should proceed after a compact authority digest.

---

## 6. Planned split sequence after DLH-5V-A

If DLH-5V-A closes regular frontier geometry successfully, the intended bounded sequence is:

```text
DLH-5V-A regular phase + actual Voronoi adjacency
-> separate regular-frontier geometric moment-cone gate
-> separate boundary-local rate / strict face-flux audit gate if needed
-> separate endpoint/corner closure
-> boundary-HJB / Route-F implementation authority
-> KKT + discrete-generator validation
-> Wmax / resolution robustness
-> conservative same-process stationary-generator validation
-> Issue #27 stationary KFE
-> stationary aggregates C,L,A,B
-> two-region structural anchor
-> regional learned W^L
```

Each scientific layer must be independently reviewed before the next is activated.

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

## 8. Scientific ceiling during DLH-5V-A

Do not mutate accepted economics/source; run HJB/KFE/stationary; choose numerical `W_max`; modify grid/economics; compute moment cones or rates; close endpoint/corner transitions; agglomerate states; compute stationary aggregates/GE; enter multi-province/neural/nominal/calibration/policy/welfare/Results.

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.
