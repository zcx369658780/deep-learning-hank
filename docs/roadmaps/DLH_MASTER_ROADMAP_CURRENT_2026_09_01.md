# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.26  
**Date:** 2026-09-03  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** CURRENT OWNER-APPROVED DLH-5V — RESTRICTED-VORONOI TANGENTIAL MOMENT-CONE DESIGN ACTIVE

---

## 0. Long-run objective

Build a data-to-structural-model calibration and regional-network HANK platform in which household HJB/KFE, aggregation, firm/accounting blocks and later nominal-HANK equations remain explicit structural economics, while difficult cross-regional mappings become interpretable learned modules only after household and equilibrium foundations pass scientific and numerical validation.

The first learned object remains the regional labor/spatial rule `W^L`; capital-network learning `W^K`, nominal HANK, calibration, policy and welfare remain downstream.

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

Stationary KFE remains **NOT AUTHORIZED** until one discrete finite controlled household process is fully selected, implemented and validated.

Accepted finite production-domain family:

```text
D_W(W_max) = {
    0 <= a <= a_max,
    b >= b_min,
    a+b <= W_max
}
```

No numerical `W_max` is selected.

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

with a.e. partition of `D_W`, actual shared faces `F_{s,r}`, physical W segments `F_s^W`, cell measures `omega_s`, and weighted mass matrix `M=diag(omega_s)`.

Accepted discrete control object:

```text
H_h(c,l,d)
 = u(c)-v(l)
 + sum_r q_{s->r}(c,l,d)[V_r-V_s]
 + switch.
```

Accepted forward semantics:

```text
p_dot = Q^T p,
p = M g,
stationary mass: Q^T p = 0,
stationary density: M^{-1}Q^T M g = 0.
```

MATLAB-style component pin remains downstream on mass `p`, followed by normalization and ORIGINAL unmodified residual validation.

---

## 2. Accepted DLH-5U / Issue #47

Issue #47 is CLOSED completed.

Accepted Rev-1 candidate:

`81bf9b46f20e6dd96514bb6fad698097c917a948`

Reviewer acceptance:

`5521379228`

Acceptance integration:

`060c2835825f9efff4f89c84646f04cab6a9c8a4`

Accepted verdict:

`DLH_5U_REV1_ACCEPTED__OUTCOME_B_CONFIRMED__ROUTE_F_FRAMEWORK_ACCEPTED__TANGENTIAL_SAME_PROCESS_CONSISTENCY_REMAINS_THE_SINGLE_BOUNDED_OPEN_OBJECT`

Accepted terminal:

`DLH_5U_ROUTE_F_SCIENTIFICALLY_VIABLE__ONE_BOUNDED_DISCRETE_GEOMETRY_OR_WEIGHTED_ADJOINT_OBJECT_REMAINS_UNRESOLVED`

DLH-5U established the Route-F framework but did not close W-frontier tangential consistency. The old axial two-step cascade is rejected as first-order same-process evidence because exact sliding `(-u,+u)` at fixed `da/db=10/7` produces O(1) spurious normal drift; a simple rectangular-grid oblique one-step candidate is not monotone.

These failures are not an impossibility theorem for the true restricted-Voronoi adjacency graph.

---

## 3. Owner continuation decision after DLH-5U

Owner approved:

`APPROVE_DLH_5V_RESTRICTED_VORONOI_TANGENTIAL_MOMENT_CONE_DESIGN`

Scientific objective:

> characterize the actual restricted-Voronoi W-frontier neighbor-displacement / face-normal cone and determine whether nonnegative CTMC rates can reproduce the full accepted tangential reallocation cone while preserving conservation, monotonicity and one-`Q` HJB/KFE same-process semantics.

No switch to W1-TC or W2 unless DLH-5V establishes an obstruction and returns an Owner-decision terminal.

---

## 4. Immediate active gate — DLH-5V / Issue #48

### Name

**Restricted-Voronoi W-Frontier Tangential Moment-Cone and Same-Process Transition Design**

Task type:

`SCIENTIFIC_DESIGN__RESTRICTED_VORONOI_TANGENTIAL_MOMENT_CONE_AND_SAME_PROCESS_TRANSITIONS`

Dedicated branch:

`dsh/issue-48-dlh-5v-voronoi-tangential-moment-cone-2026-09-03`

DLH-5V remains **design-only**.

### 4.1 Symbolic frontier classification

Use exact accepted lattice ratio:

```text
da = 10/19,
db = 7/19,
da/db = 10/7.
```

No numerical `W_max`. Introduce a symbolic W-line phase and derive all recurring nondegenerate regular frontier classes, actual restricted-Voronoi shared-face neighbors, displacements and endpoint/joint-boundary classes.

Physical W activity is determined directly from:

```text
F_s^W = partial(C_s) intersect {a+b=W_max}
```

with positive segment length. The node-mask staircase is not the physical face.

### 4.2 Tangential moment cone

For each actual frontier class define:

```text
K_s = cone{Delta x_{sr}: r is an actual shared-face admissible neighbor}.
```

Test whether it contains:

```text
T_realloc = {mu_a<=0, mu_b>=0, mu_a+mu_b<=0}
```

and especially exact sliding `(-1,+1)`.

### 4.3 Strict face-flux vs general nonnegative moment matching

First audit the induced moment map of the accepted primary face-flux candidate:

```text
q^FV_{s->r}(mu)=|F_{s,r}| max(mu·n_{s,r},0)/omega_s,
m_s^FV(mu)=sum_r q^FV_{s->r}(mu) Delta x_{sr}.
```

If strict face-flux does not reproduce tangential drift but the actual Voronoi moment cone is feasible, DLH-5V may freeze a **W-frontier-only nonnegative moment-matching rate rule** on actual shared-face neighbors. Interior source-faithful upwind semantics stay unchanged.

If a recurring geometrically admissible frontier class has no admissible nonnegative same-process moment representation, DLH-5V must establish the precise obstruction and return to Owner.

### 4.4 Mandatory exact sliding benchmark

For every recurring regular frontier class, any successful rate rule must match `mu=(-u,+u)` with nonnegative rates and zero spurious normal velocity at the claimed refinement order. Per-step `O(h)` error is insufficient when CTMC rates scale as `O(1/h)`.

### 4.5 Refinement and phase uniformity

Outcome A requires pointwise/local moment consistency plus a phase-uniform statement across all recurring nondegenerate W-line phases at fixed aspect ratio `10/7`, together with endpoint/joint-boundary compatibility.

### 4.6 Geometric degeneracy / sliver policy

DLH-5V is fail-closed. Define symbolic nondegeneracy conditions on cell measures, relevant shared-face lengths and cone determinants/angles. Do not assign numerical thresholds, agglomerate states, or choose an aligned `W_max` for PASS.

---

## 5. Intended sequence after DLH-5V

If DLH-5V reaches its implementation-ready Outcome A:

```text
accepted continuous W-domain / KKT authority
-> accepted DLH-5U restricted-Voronoi Route-F framework
-> accepted DLH-5V tangential moment/transition closure
-> separate boundary-HJB / Route-F implementation authority
-> KKT + discrete-generator validation
-> nested Wmax / resolution robustness
-> conservative same-process stationary-generator validation
-> Issue #27 stationary KFE
-> recurrent-class / nullspace / admissible-pin / original residual
-> stationary-tail diagnostics
-> recompute C,L,A,B
-> rebuild two-region structural anchor
```

If DLH-5V proves a recurring-class obstruction, return to Owner for Route F vs W1-TC/W2 decision rather than forcing implementation.

---

## 6. Regional / Deep Learning architecture remains downstream

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

Deep Learning does not initially replace HJB/KFE. The HA block remains the structural response operator inside the learned-regional equilibrium environment.

---

## 7. Scientific ceiling during DLH-5V

Do not mutate accepted economics/source; implement Voronoi/rates/HJB/KFE; run programmatic grid/Voronoi/Delaunay experiments; run HJB/KFE/stationary; choose numerical `W_max`; agglomerate states; compute stationary aggregates or GE; enter multi-province/neural/nominal/calibration/policy/welfare/Results.

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.
