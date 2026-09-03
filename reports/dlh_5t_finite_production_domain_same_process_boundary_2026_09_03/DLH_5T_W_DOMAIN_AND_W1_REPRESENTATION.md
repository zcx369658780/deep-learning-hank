# DLH-5T — W-Domain Freeze and W1 Representation Analysis (Issue #46, Phase B + D)

**Design only.** No implementation, no grid, no `W_max` selection.

---

## 1. Frozen finite production domain `D_W`

Primary Owner-selected candidate (freeze the geometry, not a number):

```text
D_W(W_max) = { (a,b,z) : 0 <= a <= a_max, b >= b_min, a + b <= W_max,
               z in {z_0, z_1} }
```

with `W = a + b` and `W_max` a **numerical production-domain truncation parameter**.

`W_max` is NOT a household primitive, NOT a calibrated structural parameter, NOT an
economic wealth ceiling, and is NOT selected in DLH-5T. It is the numerical
truncation that replaces the old rectangular upper-`b` cap `b <= b_max`.

### 1.1 Economic vs numerical classification (extends the accepted DLH-5M classification)

| Boundary | Class | Consequence |
|---|---|---|
| `a >= 0` (floor `a_bar=1e-6`) | **Structural / economic non-negativity** | retained as a genuine face; `mu_a >= 0` on `a=0` |
| `b >= b_min=-2.0` | **Structural / economic borrowing floor** | retained as a genuine face; `mu_b >= 0` on `b=b_min` |
| `a <= a_max=10` | **Computational truncation + modeling normalization anchor (taper)** | retained as a face; `mu_a <= 0` on `a=a_max`; the accepted taper `r_a_eff(a)` depends only on `a` and does not stabilize the `W` face |
| `a + b <= W_max` | **Numerical production-domain truncation (pure)** | the new artificial cap; `mu_W = mu_a + mu_b <= 0` on the slanted `W` face; `W_max` selection deferred to the adequacy protocol (Phase F) |

Explicitly frozen: the finite domain is a numerical approximation object, not
silently reinterpreted as a household primitive. The `W`-face law `mu_W <= 0` is the
state-constraint that makes the truncation's boundary process controlled; its
influence is a `W_max`-adequacy matter (Phase F), not a free pass.

## 2. Geometry of `D_W` (symbolic `W_max`)

In `(a,b)` the `W` face is the line `a + b = W_max`, slope `-1` in the `(a,b)` plane,
with outward unit normal `n = (1,1)/sqrt(2)` and tangent `tau = (1,-1)/sqrt(2)`.
Faces and vertices depend on `W_max` relative to the corner sum `a_max + b_min = 8`.

### 2.1 Regime I (production regime): `W_max >= a_max + b_min = 8`

The domain is a trapezoid/pentagon with four faces and vertices:

```text
faces:   a=0      (b in [b_min, W_max])
         b=b_min  (a in [0, a_max])
         a=a_max  (b in [b_min, W_max - a_max])
         W        (a in [0, a_max], b = W_max - a)
vertices / active intersections:
         (0, b_min)                 a=0  x b=b_min           (mu_a >= 0, mu_b >= 0)
         (a_max, b_min)             a=a_max x b=b_min        (mu_a <= 0, mu_b >= 0)
         (a_max, W_max - a_max)     a=a_max x W              (mu_a <= 0, mu_W <= 0)
         (0, W_max)                 a=0 x W                  (mu_a >= 0, mu_W <= 0)
```

Note: in Regime I the `W` face does NOT intersect `b = b_min` (the W face ends at
`a = a_max` where `b = W_max - a_max >= b_min`). `a=0 x b=b_min` and
`a=a_max x b=b_min` are genuine vertices of `D_W`.

### 2.2 Regime II (small-`W_max` regime): `b_min <= W_max < a_max + b_min = 8`

The `a = a_max` face is entirely outside `D_W` (at `a=a_max`, `b >= b_min` and
`b <= W_max - a_max < b_min` is empty). The domain is a triangle:

```text
faces:   a=0      (b in [b_min, W_max])
         b=b_min  (a in [0, W_max - b_min])
         W        (from (0,W_max) to (W_max - b_min, b_min))
vertices / active intersections:
         (0, b_min)                 a=0 x b=b_min           (mu_a >= 0, mu_b >= 0)
         (0, W_max)                 a=0 x W                 (mu_a >= 0, mu_W <= 0)
         (W_max - b_min, b_min)     b=b_min x W             (mu_b >= 0, mu_W <= 0)
```

In Regime II the `b=b_min x W` intersection exists; the `a=a_max` face and the
`a=a_max x W` intersection do NOT exist. For a production domain `W_max` is expected
to lie in Regime I, but the exact conditions are stated, not assumed (Issue #46 §6:
"do not assume every symbolic face intersection exists for every `W_max`").

### 2.3 Boundary case `W_max = a_max + b_min = 8`

The `W` face, `a=a_max` face and `b=b_min` face meet at the single point
`(a_max, b_min)`; a triple intersection of active faces. This is the degenerate
transition between Regimes I and II.

### 2.4 Tangent-cone laws (frozen, unified convention)

```text
a = 0:            mu_a >= 0
b = b_min:        mu_b >= 0
a = a_max:        mu_a <= 0
a + b = W_max:    mu_W = mu_a + mu_b <= 0
```

At every feasible intersection, ALL active inequalities apply jointly. The
admissible control set on an active face is the **tangent cone** of `D_W` at that
state; the boundary HJB maximizes over controls admissible to the active cone (the
constraint is imposed in the Hamiltonian, never by post-hoc clipping or relabeling —
see the HJB/KKT laws report).

## 3. W1 — masked native `(a,b)` tensor representation

W1 is the Owner-selected primary representation candidate:

```text
W1 = native (a,b) tensor coordinates + mask a+b <= W_max
```

### 3.1 Represented-state mask (design)

On the tensor lattice `{b_i}_{i=0}^{I-1}` (with `b_0 = b_min`, `b_{I-1} >= W_max` so
that the `a=0` row reaches the `W` face) and `{a_j}_{j=0}^{J-1}` (with `a_0=0`,
`a_{J-1}=a_max`), the represented states are:

```text
S = { (i,j,n) : b_i >= b_min, 0 <= a_j <= a_max, a_j + b_i <= W_max, n in {0,1} }
  = { (i,j,n) : a_j + b_i <= W_max }        (b_min, a>=0 automatic on the lattice)
```

States with `a_j + b_i > W_max` are **not represented** and are not part of the
controlled process. The `b`-extent of the lattice is a successor implementation
choice (once `W_max` is selected under separate authority); DLH-5T does not choose
it.

### 3.2 Frontier sets (design)

```text
W-frontier (ceiling):  F_b = { (i,j,n) in S : a_j + b_{i+1} > W_max }   (+b outside)
                       F_a = { (i,j,n) in S : a_{j+1} + b_i > W_max }   (+a outside)
```

A state is on the W face iff it is in `F_b` or `F_a` (or both, at a staircase step).
On the staircase, the face is a piecewise-linear approximation of the line
`a+b=W_max`: for each `a_j`, the maximal represented `b` index is
`i_max(j) = max{i : b_i <= W_max - a_j}`.

Axial faces (always coordinate-aligned and exact):
- `a=0` face: `j=0`; `-a` neighbor absent.
- `b=b_min` face: `i=0`; `-b` neighbor absent.
- `a=a_max` face: `j=J-1`; `+a` neighbor absent, present only for
  `a_max + b_i <= W_max` (Regime I segment).

### 3.3 W1 discrete process audit (Issue #46 §8)

The following discrete semantics are **resolved at the design level** and frozen:

1. **Mask**: states outside `a_j + b_i <= W_max` are not represented; they have no
   transition rates into or out of `S`.
2. **Valid neighbors**: at an interior state the candidate destinations are the
   axial neighbors `(i±1,j,n)`, `(i,j±1,n)` and the `z`-switch; a candidate
   destination is **admitted** only if it lies in `S`.
3. **One-sided/tangent behavior**: on an active face the drift component in the
   outward-normal lattice direction is **non-positive by the KKT law** (e.g.,
   `mu_W <= 0` on the W face), so no outward probability flux through the face is
   requested; the process is one-sided at the face (inward/tangent only).
4. **Transition orientation**: the frozen `Q[row,col] > 0 (row != col)` means
   `row -> col`; `Q V` is the backward/HJB action, `Q^T g` the forward/KFE action.
5. **Boundary-admitted rates**: at every state, each admitted off-diagonal rate is
   the upwind rate of the KKT-admissible drift restricted to admitted destinations.
6. **Diagonal construction**: `Q[i,i] = -sum_{j != i, j admitted} Q[i,j]` (the
   diagonal equals minus the sum of ACTUALLY admitted represented off-diagonal
   rates); **no outward rate whose destination is omitted by the mask is retained
   in the diagonal** (per the DLH-5D contract §4.1).
7. **HJB/KFE same stencil**: the HJB finite-difference action and the future KFE
   generator must use the **identical** represented-state set, admitted-transition
   set and rates (the discrete form of the central same-process law).
8. **Conservation implications**: with the diagonal rule (6), every row sum is zero
   (up to the `z`-switch which itself has zero row sums), so the generator is
   conservative; the `W`-face flux is zero in the normal direction by (3).

### 3.4 The specific unresolved discrete ambiguity (drives the terminal)

The following is **NOT** resolvable on the accepted axial lattice at the design
level, and is the specific masked-grid process-matching ambiguity that prevents an
implementation-ready W1 contract:

**Tangential-drift representation on the slanted W face.** The continuous W-constrained
process allows a **tangential** boundary drift: at a W-frontier state, the KKT law
`mu_W <= 0` admits `mu_b > 0` with `mu_a < 0` (illiquid-financed liquid accumulation)
— this is precisely the portfolio-reallocation behavior accepted in DLH-5L and
materially present in the DLH-5M evidence (17 offenders with `mu_a < 0, mu_b > 0,
mu_W < 0`). On the W face this drift is tangent to `a + b = W_max`. On the W1 axial
lattice the face tangent `(1,-1)` is **not aligned with any lattice direction**
(because the accepted spacings satisfy `da = 10/19 != db = 7/19`), so the tangential
flow cannot be represented by any axial move: the `+b` destination at a `F_b`
frontier state is outside `S`.

Consequences of the three naive axial-only treatments:

| Treatment | Row-sum/conservation | Same-process fidelity |
|---|---|---|
| (i) drop the `+b` rate and do not add it to the diagonal | conservative (diagonal = -admitted), no leak | **changes the process**: the tangential `b`-upward control selected by the HJB is suppressed at the face (reflected-`b`), so KFE transitions do not correspond to HJB-admitted controlled transitions |
| (ii) MATLAB-faithful retain of the `+b` rate in the diagonal | **leaks** (negative row sum) | forbidden by DLH-5D §4.1 |
| (iii) route the `+b` component into the `-a` axial rate | conservative | **changes the process**: the `b`-dynamics is distorted into an `a`-dynamics; not the same controlled process |

A faithful representation requires an **off-axis flux construction** at the W face
(e.g., face-adapted control volumes with the normal flux `mu_W` and a tangential
flux carried along the face, or tangent/corner-transport diagonal transitions). With
`da != db` there is no lattice-aligned tangent, so the off-axis construction is a
genuine free numerical design choice whose exact form — control-volume geometry,
flux quadrature, tangential routing, and its consistency with the continuous
W-constrained process as the grid refines — is **not determined by the accepted
science and cannot be validated in a design-only gate** (no execution is authorized).

### 3.5 What this means for the terminal

- The W-domain `D_W` economic/numerical logic is **scientifically supported**: the
  continuous tangent-cone laws (Section 2.4), the economic/numerical classification
  (Section 1.1), and the same-process principle are all well-defined and coherent.
- The **W1 discrete process near the slanted W face is not implementation-ready**
  because of the specific tangential-drift representation ambiguity of Section 3.4.
- Per Issue #46 §8, since W1 cannot be made implementation-ready at the design
  level, the appropriate terminal is **Outcome B**
  (`DLH_5T_W_DOMAIN_SCIENTIFICALLY_SUPPORTED__W1_DISCRETE_PROCESS_MATCHING_REQUIRES_BOUNDED_FOLLOWUP_DESIGN`).
- The design does **not** silently switch to W2: W2 is recorded only as a bounded
  follow-up candidate (Section 4), consistent with the Issue's explicit instruction.

## 4. W2 comparison (design note only — not selected)

For contrast only: the transformed `(a,W)` representation (`b = W - a`) makes the
`W` cap flat but moves the slanted face to the borrowing floor `W = a + b_min`, and
the transfer FOC then couples the `a` and `W` coordinates. DLH-5T does not switch to
W2. W2 is listed as a bounded follow-up option to be evaluated under a successor
design authority, together with face-adapted finite-volume treatments of W1.

## 5. Design-only compliance

No source mutation, no grid/domain experiment, no `W_max`, no W1-mask/slanted-stencil
implementation, no generator assembly, no execution. All statements are symbolic/
analytic and are derived from the accepted accounting and evidence.
