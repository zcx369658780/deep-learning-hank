# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.24  
**Date:** 2026-09-03  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** CURRENT OWNER-APPROVED ROUTE F — DLH-5U W1 FACE-ADAPTED FINITE-VOLUME SAME-PROCESS DESIGN ACTIVE

---

## 0. Long-run objective

Build a data-to-structural-model calibration and regional-network HANK platform in which household HJB/KFE, aggregation, firm/accounting blocks and later nominal-HANK equations remain explicit structural economics, while difficult cross-regional mappings become interpretable learned modules only after household and equilibrium foundations pass scientific and numerical validation.

The first learned object remains the regional labor/spatial rule `W^L`; capital-network learning `W^K`, nominal HANK, calibration, policy and welfare remain downstream.

---

## 1. Accepted household foundation through DLH-5T

Accepted MATLAB-faithful household source:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Binding Issue #27 law:

```text
HJB boundary policy <=> KFE boundary transition law
```

Stationary KFE remains **NOT AUTHORIZED** until one discrete finite controlled household process is selected, implemented and validated.

The accepted DLH-5O–5S asymptotic work remains conditional guidance only: the reduced p=2 attractor structure is accepted, but full-HJB p=2 realization remains unproved. Route D/F preserves that caveat rather than treating it as theorem closure.

---

## 2. Accepted DLH-5T / Issue #46

Issue #46 is CLOSED completed.

Accepted candidate:

`fa9d886ea932c2c9001b86228200a162fb1990cd`

Reviewer acceptance comment:

`5519690088`

Acceptance integration:

`73efb8b00b6b4884fc966f159b3aa8401cd3df41`

Acceptance level:

`L3_COMMIT_VERIFIED__SCIENTIFIC_DESIGN_ACCEPTED`

Accepted verdict:

`DLH_5T_ACCEPTED__OUTCOME_B_CONFIRMED__W_DOMAIN_AND_CONTINUOUS_SAME_PROCESS_BOUNDARY_CONTRACT_ACCEPTED__W1_TANGENTIAL_DISCRETE_PROCESS_MATCHING_REMAINS_OPEN`

Accepted terminal:

`DLH_5T_W_DOMAIN_SCIENTIFICALLY_SUPPORTED__W1_DISCRETE_PROCESS_MATCHING_REQUIRES_BOUNDED_FOLLOWUP_DESIGN`

### 2.1 Accepted finite production-domain family

```text
D_W(W_max) = {
    0 <= a <= a_max,
    b >= b_min,
    a+b <= W_max
}
```

Interpretation:

- `a>=0` is the structural non-negativity boundary;
- `b>=b_min` is the economic liquid borrowing floor;
- `a<=a_max` retains the accepted illiquid-support/taper anchor and requires a boundary state-constraint law;
- `a+b<=W_max` is a numerical production-domain truncation, not a household primitive or calibrated wealth ceiling;
- no numerical production `W_max` is selected.

### 2.2 Accepted continuous boundary process

```text
a=0:          mu_a >= 0
b=b_min:      mu_b >= 0
a=a_max:      mu_a <= 0
a+b=W_max:    mu_W=mu_a+mu_b <= 0
```

At all feasible intersections, active inequalities apply jointly. Boundary controls must be selected from the constrained Hamiltonian/KKT problem itself; unconstrained-policy-then-clip is not accepted.

### 2.3 Accepted same-process law

```text
controlled process selected by boundary HJB
        ==
controlled process represented by KFE generator
```

Future discrete generator requirements:

- every represented transition corresponds to the HJB-admitted discrete process;
- no KFE-only clipping of HJB-selected boundary policy;
- diagonal = negative sum of actually admitted represented off-diagonal rates;
- no omitted masked destination can leave a retained diagonal exit rate;
- row conservation and non-negative off-diagonals are mandatory;
- contamination/pin is downstream normalization only and cannot repair boundary economics.

### 2.4 Accepted `W_max` adequacy method

Production-domain extent will be selected later from pre-registered nested candidates using staged HJB shared-interior stability, boundary influence localization, future stationary-tail influence, aggregate stability `C,L,A,B`, and downstream GE stability. The eventual production cap is the smallest candidate satisfying all applicable accepted gates.

---

## 3. DLH-5T unresolved discrete object

W1 keeps native `(a,b)` coordinates and masks states with `a+b>W_max`. This preserves the borrowing floor as a coordinate-aligned economic boundary and keeps the accepted a-based taper native.

At the slanted W frontier the continuous constrained HJB may admit portfolio-reallocation drift:

```text
mu_b > 0
mu_a < 0
mu_W = mu_a + mu_b <= 0
```

Pure axial node-to-node transitions do not uniquely preserve this local process when the `+b` axial destination lies outside the mask. Dropping that component changes the process; retaining its diagonal rate leaks mass; rerouting it distorts asset composition.

Reviewer clarifications controlling all downstream work:

- no positive W-normal flux does not imply every axial component has an in-mask axial neighbor;
- one-dimensional stationary nullspace is only a future canonical uniqueness target conditional on uniqueness;
- `a_bar=1e-6` is the adjustment-cost denominator floor, not the state boundary;
- negative-`b` implementation must preserve the accepted effective liquid return / borrowing-rate-gap semantics.

---

## 4. Owner Route-F decision after DLH-5T

Owner selected:

`APPROVE_ROUTE_F_W1_FACE_ADAPTED_FINITE_VOLUME_OBLIQUE_FLUX_DESIGN`

Scientific rationale:

- keep native household coordinates `(a,b,z)`;
- keep the economic borrowing floor `b=b_min` coordinate-aligned;
- keep the difficult oblique geometry on the artificial high-wealth W boundary;
- resolve W1 process matching through a conservative face-adapted finite-volume / oblique-flux construction rather than moving the slanted geometry to the borrowing floor;
- remain design/specification-first before any implementation or HJB/KFE execution.

W1 tangent/corner transport and W2 transformed `(a,W)` remain fallback comparison routes only, not active authority.

---

## 5. Immediate active gate — DLH-5U / Issue #47

### Name

**W1 Face-Adapted Finite-Volume / Oblique-Flux Same-Process Discretization**

Task type:

`SCIENTIFIC_DESIGN__W1_FACE_ADAPTED_FINITE_VOLUME_SAME_PROCESS_DISCRETIZATION`

Dedicated branch:

`dsh/issue-47-dlh-5u-w1-face-adapted-fv-design-2026-09-03`

DLH-5U is **design-only**. It does not authorize implementation or numerical execution.

### 5.1 Primary geometric object

Route F audits control volumes clipped by the physical W-domain:

```text
C_s = C_s^base ∩ D_W(W_max)
```

with explicit cell measures, actual shared faces, normals, physical W-face segments and adjacency. The physical slanted W face must be distinguished from the staircase of masked nodes.

### 5.2 Boundary-control location

DLH-5U must determine where the constrained HJB control/Hamiltonian lives in a cut-cell representation and give a clear refinement interpretation. It may not impose a W-face KKT condition on a strictly interior physical state without a consistency argument.

### 5.3 Face-flux / CTMC generator

The primary candidate is a monotone conservative source-to-neighbor face-flux generator:

```text
Q[s,r] = q_{s->r} >= 0, s != r
Q[s,s] = -sum_{r != s} q_{s->r}
```

with rates derived from HJB-admitted drift and actual shared control-volume faces. Physical W-boundary outward flux is excluded by the accepted KKT condition itself, not by KFE clipping.

The same `Q` must define backward HJB action and forward probability-mass dynamics.

### 5.4 Central tangential-reallocation test

For local admissible drift `mu_b>0, mu_a<0, mu_W<=0`, the design must show symbolically how face fluxes transport the process along/inward from the physical W frontier while preserving both asset coordinates, conservation and monotonicity. Outcome A is forbidden if this local process cannot be represented consistently.

### 5.5 Mass vs density / weighted adjoint

Because clipped control volumes have nonuniform measures, DLH-5U must distinguish:

```text
p_s = probability mass,
M = diag(omega_s),
p = M g.
```

It must derive the correct forward/stationary equation for the chosen variable, normalization, economic aggregation weights, original-equation residual, and downstream contamination compatibility. Uniform-grid shorthand must not be silently reused if cut-cell weights differ.

### 5.6 Sliver/small-cell and refinement consistency

The gate must audit:

- nonnegative rates / Markov monotonicity;
- row-sum conservation;
- first-order/local moment consistency;
- physical W-boundary normal consistency;
- tangential asset-composition consistency;
- small-cut-cell/sliver rates and conditioning;
- whether deterministic agglomeration, future geometric admissibility, or another bounded remedy is required;
- no PASS-seeking numerical W alignment.

No numerical `W_max` is selected.

---

## 6. Intended sequence after DLH-5U

If DLH-5U reaches an implementation-ready design terminal:

```text
accepted DLH-5T continuous W-domain / KKT / same-process authority
-> DLH-5U face-adapted finite-volume discrete-process design
-> separate boundary-HJB / Route-F implementation authority
-> KKT/complementarity + discrete-generator validation
-> nested Wmax / resolution robustness
-> conservative same-process stationary-generator validation
-> Issue #27 stationary KFE
-> recurrent-class / nullspace / admissible-pin / original stationary residual
-> stationary-tail diagnostics
-> recompute C,L,A,B
-> rebuild two-region structural anchor
```

No historical stationary aggregate is grandfathered.

---

## 7. Regional / Deep Learning architecture remains downstream

Long-run hybrid architecture:

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

Scaling hierarchy remains:

```text
2-region unit fixture
-> 3–5 province integration fixture
-> 31-province empirical/source benchmark
```

Learned `W^L`, later `W^K`, nominal HANK, calibration, policy and welfare remain deferred until the controlled household stationary foundation is accepted.

---

## 8. Scientific ceiling during DLH-5U

Do not:

- mutate accepted household economics/source;
- implement Route F or choose numerical `W_max`;
- execute HJB/KFE/stationary/grid/domain experiments;
- compute stationary aggregates or rebuild two-region GE;
- enter multi-province execution, neural training, nominal HANK, calibration, policy, welfare or Results.

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.
