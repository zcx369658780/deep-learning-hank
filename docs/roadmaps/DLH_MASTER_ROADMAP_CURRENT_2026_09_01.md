# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.23  
**Date:** 2026-09-03  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** CURRENT OWNER-DECISION CHECKPOINT — DLH-5T ACCEPTED / W1 DISCRETE W-FRONTIER PROCESS UNRESOLVED

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

Stationary KFE remains **NOT AUTHORIZED** until one finite controlled household process is selected, implemented and validated.

The accepted DLH-5O–5S asymptotic work remains conditional guidance only: the reduced p=2 attractor structure is accepted, but full-HJB p=2 realization remains unproved. Route D preserves that caveat rather than treating it as theorem closure.

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

### 2.1 Finite production-domain family accepted

```text
D_W(W_max) = {
    0 <= a <= a_max,
    b >= b_min,
    a+b <= W_max
}
```

Interpretation:

- `a>=0` is the structural non-negativity boundary;
- `b>=b_min` is the liquid borrowing floor;
- `a<=a_max` retains the accepted illiquid-support/taper anchor and requires a boundary state-constraint law;
- `a+b<=W_max` is a numerical production-domain truncation, not a household primitive or calibrated wealth ceiling;
- no numerical production `W_max` is selected yet.

### 2.2 Continuous boundary process accepted

Accepted tangent-cone laws:

```text
a=0:          mu_a >= 0
b=b_min:      mu_b >= 0
a=a_max:      mu_a <= 0
a+b=W_max:    mu_W=mu_a+mu_b <= 0
```

At all feasible intersections, active inequalities apply jointly. Boundary controls must be selected from the constrained Hamiltonian/KKT problem itself; unconstrained-policy-then-clip is not accepted.

The W multiplier acts symmetrically on the two asset shadow gradients; the linear portfolio-transfer component cancels from total-wealth drift and from the linear part of the W-face transfer FOC, while adjustment cost preserves `d` dependence.

### 2.3 Same-process HJB–KFE law accepted

```text
controlled process selected by boundary HJB
        ==
controlled process represented by KFE generator
```

Future discrete generator requirements:

- every represented transition corresponds to the HJB-admitted discrete process;
- no KFE-only clipping of an HJB-selected boundary policy;
- diagonal = negative sum of actually admitted represented off-diagonal rates;
- no omitted masked destination can leave a retained diagonal exit rate;
- row conservation and non-negative off-diagonals remain mandatory;
- contamination/pin is downstream normalization only and cannot repair boundary economics.

The future stationary KFE still requires recurrent-class/nullspace diagnostics, original `Q^T g` residual, normalization, non-negativity and admissible-pin checks.

### 2.4 `W_max` adequacy method accepted

Production-domain extent will be selected later from pre-registered nested candidates using staged evidence:

```text
HJB shared-interior policy stability
-> artificial-boundary influence localization
-> stationary-tail influence after KFE authorization
-> aggregate stability C,L,A,B
-> GE/two-region price-state stability
```

The eventual production cap is the smallest candidate satisfying all applicable accepted gates. No PASS-seeking tolerance relaxation is allowed.

---

## 3. Current unresolved object — W1 discrete W-frontier process

W1 keeps native `(a,b)` coordinates and masks states with `a+b>W_max`. This preserves the economically important borrowing floor as a coordinate-aligned boundary and keeps the accepted a-based taper native.

However, on the slanted W frontier the continuous constrained HJB may admit portfolio-reallocation drift:

```text
mu_b > 0
mu_a < 0
mu_W = mu_a + mu_b <= 0
```

The continuous normal flux is admissible/inward, but the axial `+b` destination may lie outside the W1 mask. Pure coordinate-split axial transitions therefore do not uniquely preserve the local HJB-controlled process. Dropping the `+b` component changes the process; retaining its diagonal rate leaks mass; rerouting it to `-a` distorts asset composition.

This is a **discrete numerical-process design problem**, not a rejection of the W-domain economics.

Reviewer clarifications controlling downstream work:

- “no outward W flux” means no positive continuous normal flux; it does not imply every axial component has an in-mask axial destination;
- one-dimensional stationary nullspace is a future canonical uniqueness target conditional on uniqueness, not a consequence of conservativity alone;
- `a_bar=1e-6` is the adjustment-cost denominator floor, not the state lower bound;
- negative-`b` implementation must preserve the accepted effective liquid return / borrowing-rate-gap semantics.

---

## 4. Owner decision checkpoint — bounded discrete-process routes

There is currently **NO ACTIVE BUILDER ISSUE**.

### Route F — W1 face-adapted finite-volume / oblique-flux design

Keep W1 native `(a,b)` representation and design an explicit conservative face-based scheme on the artificial W frontier. Required objects include control-volume geometry, normal/tangential flux decomposition, HJB backward action, adjoint KFE forward action, monotonicity/conservation and grid-refinement consistency.

**Scientific advantage:** numerical complexity stays on the artificial high-wealth truncation boundary, while the economic borrowing floor remains coordinate-aligned.

### Route C — W1 tangent/corner-transport transition design

Keep the masked W1 lattice but introduce carefully specified off-axis / diagonal / corner transport transitions that approximate tangential W-face motion. Requires an explicit grid-spacing consistency argument and same-process HJB/KFE construction.

**Scientific risk:** transition geometry may become nonlocal or grid-ratio dependent if not carefully designed.

### Route W2 — transformed `(a,W)` representation

Use `b=W-a`, making `W=W_max` coordinate-aligned. The lower borrowing constraint becomes the oblique boundary `W=a+b_min` and requires its own same-process treatment.

**Scientific tradeoff:** simplifies the artificial upper boundary but moves geometric complexity to the economically important borrowing floor.

### Current scientific recommendation

Prefer **Route F (W1 face-adapted finite-volume / oblique-flux design)** for the next bounded gate. It retains native household states and places the difficult geometry on the artificial upper truncation rather than on the borrowing constraint. The next gate should remain design/specification-first and should not yet run HJB/KFE.

Owner must approve the route before a successor Issue is published.

---

## 5. Intended household sequence after discrete-process design

```text
accepted DLH-5T continuous W-domain / same-process authority
-> bounded W-frontier discrete-process design
-> separate boundary-HJB implementation authority
-> KKT/complementarity and discrete-process validation
-> nested Wmax / resolution robustness
-> conservative same-process generator validation
-> Issue #27 stationary KFE
-> recurrent-class / nullspace / admissible-pin / original Q^T g residual
-> stationary-tail diagnostics
-> recompute C,L,A,B
-> rebuild two-region structural anchor
```

No historical stationary aggregate is grandfathered.

---

## 6. Regional / Deep Learning architecture remains downstream

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

## 7. Scientific ceiling at current checkpoint

Until the Owner selects a bounded discrete-process route and successor authority exists, do not:

- mutate accepted household economics;
- implement W1/W2 or choose numerical `W_max`;
- execute a new boundary-HJB/KFE process;
- solve stationary density or aggregates;
- rebuild two-region GE;
- enter multi-province execution, neural training, nominal HANK, calibration, policy, welfare or Results.

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.
