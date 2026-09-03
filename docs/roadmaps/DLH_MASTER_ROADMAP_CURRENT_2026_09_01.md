# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.25  
**Date:** 2026-09-03  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** CURRENT POST-DLH-5U CHECKPOINT — ROUTE F FRAMEWORK ACCEPTED / TANGENTIAL VORONOI PROCESS REMAINS OPEN

---

## 0. Long-run objective

Build a data-to-structural-model calibration and regional-network HANK platform in which household HJB/KFE, aggregation, firm/accounting blocks and later nominal-HANK equations remain explicit structural economics, while difficult cross-regional mappings become interpretable learned modules only after household and equilibrium foundations pass scientific and numerical validation.

The first learned object remains the regional labor/spatial rule `W^L`; capital-network learning `W^K`, nominal HANK, calibration, policy and welfare remain downstream.

---

## 1. Accepted household foundation through DLH-5U

Accepted MATLAB-faithful household source:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Binding Issue #27 law:

```text
HJB boundary policy <=> KFE boundary transition law
```

Stationary KFE remains **NOT AUTHORIZED** until one discrete finite controlled household process is fully selected, implemented and validated.

The accepted DLH-5O–5S asymptotic work remains conditional guidance only: the reduced p=2 attractor structure is accepted, but full-HJB p=2 realization remains unproved. Route D/F preserves that caveat rather than treating it as theorem closure.

---

## 2. Accepted finite-domain authority from DLH-5T

Finite numerical production-domain family:

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
- `a<=a_max` retains the accepted illiquid-support/taper anchor;
- `a+b<=W_max` is numerical truncation, not a household primitive or calibrated wealth ceiling;
- no numerical production `W_max` is selected yet.

Accepted continuous tangent-cone laws:

```text
a=0:          mu_a >= 0
b=b_min:      mu_b >= 0
a=a_max:      mu_a <= 0
a+b=W_max:    mu_W=mu_a+mu_b <= 0
```

Boundary controls must come from the constrained household problem itself; unconstrained-policy-then-clip is not accepted.

Accepted same-process law:

```text
controlled process selected by boundary HJB
        ==
controlled process represented by KFE generator
```

Contamination remains downstream normalization only.

---

## 3. Accepted DLH-5U / Issue #47

Issue #47 is CLOSED completed.

Accepted Rev-1 candidate:

`81bf9b46f20e6dd96514bb6fad698097c917a948`

Reviewer acceptance comment:

`5521379228`

Acceptance integration:

`060c2835825f9efff4f89c84646f04cab6a9c8a4`

Acceptance level:

`L3_COMMIT_VERIFIED__SCIENTIFIC_DESIGN_ACCEPTED`

Accepted verdict:

`DLH_5U_REV1_ACCEPTED__OUTCOME_B_CONFIRMED__ROUTE_F_FRAMEWORK_ACCEPTED__TANGENTIAL_SAME_PROCESS_CONSISTENCY_REMAINS_THE_SINGLE_BOUNDED_OPEN_OBJECT`

Accepted terminal:

`DLH_5U_ROUTE_F_SCIENTIFICALLY_VIABLE__ONE_BOUNDED_DISCRETE_GEOMETRY_OR_WEIGHTED_ADJOINT_OBJECT_REMAINS_UNRESOLVED`

### 3.1 Restricted-Voronoi Route-F geometry accepted

The Rev-0 clipped-base-cell partition claim was rejected and repaired. The accepted Route-F control volumes are restricted Voronoi cells induced only by represented W1 nodes:

```text
C_s = {x in D_W : ||x-s|| <= ||x-r|| for all represented r}
```

which partition `D_W` a.e. This gives a coherent basis for:

- cell measures `omega_s`;
- shared faces `F_{s,r}`;
- normals `n_{s,r}`;
- physical W segments `F_s^W`;
- adjacency;
- nonuniform mass matrix `M=diag(omega_s)`.

The physical W face is the actual intersection with `a+b=W_max`, not the masked-node staircase.

### 3.2 Discrete household control object accepted

The exact discrete Hamiltonian is control-dependent:

```text
H_h(c,l,d)
  = u(c) - v(l)
  + sum_r q_{s->r}(c,l,d)[V_r-V_s]
  + switch.
```

Controls maximize this discrete Hamiltonian subject to the active cell tangent constraints. Continuous DLH-5T effective-gradient FOCs remain consistency/refinement targets unless discrete equivalence is separately proved.

### 3.3 Face-flux / CTMC framework accepted in the framework sense

Primary rate form:

```text
q_{s->r}
  = |F_{s,r}| * max(mu_s·n_{s,r},0) / omega_s,

Q[s,s] = -sum_{r!=s} q_{s->r}.
```

Accepted framework properties:

- nonnegative off-diagonals;
- exact row-sum conservation by construction;
- physical W-normal outward flux excluded by the HJB/KKT constraint itself;
- no omitted destination with retained diagonal exit rate;
- one `Q` for backward HJB action and forward mass dynamics.

This is not yet accepted as a fully consistent W-frontier tangential process.

### 3.4 Weighted forward / density semantics accepted

Natural forward variable is probability mass:

```text
p_dot = Q^T p,
stationary: Q^T p = 0,
sum_s p_s = 1.
```

For density `g` with nonuniform Voronoi weights:

```text
p = M g,
M = diag(omega_s),
M^{-1} Q^T M g = 0.
```

Economic aggregates use mass weights. Under Route F, the downstream MATLAB-style component pin is applied to the mass equation, followed by normalization and validation against the ORIGINAL unmodified `Q^T p` residual.

---

## 4. Single bounded unresolved object after DLH-5U

Tangential same-process consistency at the actual restricted-Voronoi W frontier remains unresolved.

The exact sliding benchmark

```text
mu_a = -u,
mu_b = +u,
mu_W = 0
```

shows that the previously proposed two-step axial cascade has an O(1) spurious normal drift at fixed accepted aspect ratio `da/db=10/7`; the Rev-0 first-order consistency claim is withdrawn. A simple oblique one-step transition on the original rectangular-neighbor cone is not monotone.

This is **not** an impossibility theorem for Route F. The accepted restricted-Voronoi frontier may contain oblique/diagonal Voronoi neighbors that were not part of the failed axial-cascade analysis.

Therefore the next bounded scientific object is:

> characterize the actual restricted-Voronoi frontier neighbor-displacement / face-normal cone and determine whether nonnegative CTMC rates can match the admissible continuous tangential drift moments while preserving conservation and the one-`Q` same-process law.

Reviewer clarifications:

- determine W-face activity from actual `F_s^W = ∂C_s ∩ {a+b=W_max}`; no base-rectangle-crossing iff shortcut;
- the next analysis must use actual Voronoi adjacency, not assume only axial W1 moves;
- a sliver policy must be fail-closed unless either a hard pre-registered geometric admissibility rule is used or agglomerated-cell state/control/value semantics are separately frozen.

---

## 5. Recommended next bounded gate

Recommended working name:

**DLH-5V — Restricted-Voronoi W-Frontier Tangential Moment-Cone and Same-Process Transition Design**

Recommended task class:

`SCIENTIFIC_DESIGN__RESTRICTED_VORONOI_TANGENTIAL_MOMENT_CONE_AND_SAME_PROCESS_TRANSITIONS`

Target:

- derive actual local Voronoi frontier adjacency / displacement cones symbolically;
- determine whether the target tangential drift lies in the nonnegative cone generated by available neighbor displacements/rates;
- if yes, freeze a monotone conservative rate construction and its refinement statement;
- if no, establish the precise obstruction and return to Owner for Route-F vs W1-TC/W2 choice;
- resolve the sliver policy only insofar as required for a coherent local transition geometry;
- remain design-only: no source implementation, no HJB/KFE execution, no numerical `W_max`.

No successor Issue is active at this roadmap snapshot.

---

## 6. Intended sequence after tangential discrete-process closure

If the next bounded gate resolves the W-frontier tangential process to implementation-ready level:

```text
accepted DLH-5T continuous W-domain / KKT / same-process authority
-> accepted DLH-5U Route-F restricted-Voronoi framework
-> restricted-Voronoi tangential moment/transition closure
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

## 8. Scientific ceiling at current checkpoint

Until successor authority exists, do not:

- mutate accepted household economics/source;
- implement Route F / Voronoi boundary code;
- execute HJB/KFE/stationary/grid/domain experiments;
- choose numerical `W_max`;
- compute stationary aggregates or rebuild two-region GE;
- enter multi-province execution, neural training, nominal HANK, calibration, policy, welfare or Results.

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.
