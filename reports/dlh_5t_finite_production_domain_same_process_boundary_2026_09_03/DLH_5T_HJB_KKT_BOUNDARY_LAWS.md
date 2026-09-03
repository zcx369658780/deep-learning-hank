# DLH-5T — Continuous HJB/KKT Boundary Laws on `D_W` (Issue #46, Phase C)

**Design only.** Full explicit tangent-cone/KKT statements for every active face and
feasible face intersection of `D_W(W_max)`. No implementation, no `W_max` selection.
Derived from the accepted accounting and the accepted DLH-5M KKT structure (which is
preserved and extended here to all lower faces and all feasible intersections).

---

## 1. Generic state-constraint HJB statement

Interior Hamiltonian (accepted source objects):

```text
rho*V = sup_{c,l,d} { u(c) - v_l*l + V_a*mu_a + V_b*mu_b }      (interior)
```

At a boundary face, controls are restricted to the **active tangent cone**: the
state drift must not exit `D_W`. The correct statement is the constrained
Hamiltonian (Carathéodory / Crandall–Liggett viscosity formulation), **never**
post-hoc clipping and **never** branch forcing:

```text
rho*V = sup_{c,l,d : mu·n <= 0 on each active face} { u(c) - v_l*l + V_a*mu_a + V_b*mu_b }   (constrained)
```

Unified KKT convention (frozen, internally consistent): with the **outward** unit
normal `n` of each active face, write the active drift constraint as
`g = mu·n <= 0`. Because this is a **maximization** with upper-bound constraints, the
consistent Lagrangian **subtracts** each non-negative multiplier:

```text
L = u(c) - v_l*l + V_a*mu_a + V_b*mu_b - sum_j lambda_j * g_j,
   lambda_j >= 0,  lambda_j * g_j = 0   (complementarity)
```

Effective value gradients are therefore `V - lambda_j * n_j` (componentwise); the
multiplier of an upper face **reduces** the shadow price along the outward normal,
and a lower face (whose outward normal points in the `-` coordinate direction)
**increases** the shadow price along the inward (feasible) direction.

Outward normals and constraint functions on `D_W`:

```text
a = 0:          n = (-1, 0),   g = -mu_a <= 0   (mu_a >= 0)
b = b_min:      n = (0, -1),   g = -mu_b <= 0   (mu_b >= 0)
a = a_max:      n = (+1, 0),   g =  mu_a <= 0
a + b = W_max:  n = (1,1)/sqrt2, g = mu_W = mu_a + mu_b <= 0
```

## 2. Control structure entering the constraints

```text
mu_a = r_a_eff(a)*a + d                          (control d, linear +1)
mu_b = r_b*b + labor_income - d - chi(d,a) - (c - transfer_income)
                                                 (controls c, l via labor_income, d via -d - chi)
mu_W = mu_a + mu_b = r_a_eff(a)*a + r_b*b + labor_income - chi(d,a) - (c - transfer_income)
                                                 (d cancels one-for-one; chi(d,a) remains)
chi(d,a) = chi_0*|d| + 0.5*chi_1*d^2/max(a,a_bar)
```

Interior control FOCs (nondifferentiable transfer kink, accepted closed form):

```text
c:            u'(c) = V_b        =>  c = V_b^(-1/gamma_c)
l:            l = (V_b * net_wage / labor_weight)^(1/phi),  net_wage = w(1-tau-mc)*z
d (transfer): q = V_a/V_b - 1;  d = max(a,a_bar)*(min(q+chi_0,0)+max(q-chi_0,0))/chi_1
```

At a boundary face, every `V_a` / `V_b` in the FOCs is replaced by the **effective
gradients** `V_a^eff, V_b^eff` of the active face (Section 3), so the boundary
policy is the constrained optimum — never an interior policy that is clipped or
relabeled.

## 3. Per-face effective gradients and transfer-FOC structure

Let `lambda_a^-` (lower-a), `lambda_b^-` (lower-b), `lambda_a^+` (upper-a),
`lambda_W` (W) be the non-negative KKT multipliers. The effective gradients are
`V^eff = (V_a^eff, V_b^eff)`. The transfer FOC is `V_a^eff - V_b^eff =
V_b^eff * chi'(d)` in the differentiable branch (with the kink closed form of
Section 2), where `chi'(d)` denotes the derivative of `chi(d,a)` w.r.t. `d`
(`chi_0*sign(d) + chi_1*d/max(a,a_bar)`; subgradient `[-chi_0, chi_0]` at `d=0`).

### 3.1 Interior (no active face)

```text
(V_a^eff, V_b^eff) = (V_a, V_b)
transfer FOC: V_a - V_b = V_b * chi'(d)
```

### 3.2 Lower-a face `a = 0` (`mu_a >= 0`)

```text
(V_a^eff, V_b^eff) = (V_a + lambda_a^-, V_b)
transfer FOC: (V_a + lambda_a^-) - V_b = V_b * chi'(d)
```

Note: at `a = 0`, `mu_a = r_a_eff(0)*0 + d = d`, so `mu_a >= 0` is **exactly**
`d >= 0` — the frozen KKT law reproduces the accepted MATLAB lower-a transfer mask
(`d >= 0`), a consistency check.

### 3.3 Lower-b face `b = b_min` (`mu_b >= 0`)

```text
(V_a^eff, V_b^eff) = (V_a, V_b + lambda_b^-)
consumption FOC: u'(c) = V_b + lambda_b^-        (shadow value of b elevated at the floor)
transfer FOC: V_a - (V_b + lambda_b^-) = (V_b + lambda_b^-) * chi'(d)
```

### 3.4 Upper-a face `a = a_max` (`mu_a <= 0`)

```text
(V_a^eff, V_b^eff) = (V_a - lambda_a^+, V_b)
transfer FOC: (V_a - lambda_a^+) - V_b = V_b * chi'(d)
```

Note: `mu_a = r_a_eff(a_max)*a_max + d = 0.9*r_a*a_max + d`; with the accepted
`r_a=0.03, a_max=10` this is `mu_a = 0.27 + d`, so `mu_a <= 0` requires `d <= -0.27`.
This is **materially stricter** than the accepted MATLAB upper-a transfer mask
(`d <= 0`): the taper decays but does not extinguish returns at `a_max`, so the
illiquid face requires an active transfer out of `a` of at least the taper
retained return. This is exactly the "current MATLAB ordering is not KKT-equivalent
to the constrained problem" gap identified in DLH-5M, and the successor boundary-HJB
implementation must impose the KKT law.

### 3.5 W face `a + b = W_max` (`mu_W <= 0`)

```text
(V_a^eff, V_b^eff) = (V_a - lambda_W, V_b - lambda_W)
consumption FOC: u'(c) = V_b - lambda_W
transfer FOC: V_a - V_b = (V_b - lambda_W) * chi'(d)
```

The W multiplier enters both gradients **symmetrically** and **cancels one-for-one
from the linear part of the transfer FOC** (`(V_a-lambda_W)*d + (V_b-lambda_W)*(-d)
= (V_a-V_b)*d`), surviving only through the adjustment-cost resource term
`(V_b - lambda_W)*chi'(d)`. The reallocation is **not fully free**: `d` is pinned by
the transfer FOC through the adjustment-cost term. This mirrors the drift identity
that the linear `d` cancels in `mu_W`.

### 3.6 Lower-a × lower-b corner `(0, b_min)` — Regimes I and II

```text
(V_a^eff, V_b^eff) = (V_a + lambda_a^-, V_b + lambda_b^-)
transfer FOC: (V_a + lambda_a^-) - (V_b + lambda_b^-) = (V_b + lambda_b^-) * chi'(d)
```

Joint cone: `mu_a >= 0 AND mu_b >= 0` (at `a=0`, `mu_a = d >= 0`; at `b=b_min`,
`mu_b >= 0`). Always a vertex of `D_W`.

### 3.7 Upper-a × lower-b corner `(a_max, b_min)` — Regime I only

```text
(V_a^eff, V_b^eff) = (V_a - lambda_a^+, V_b + lambda_b^-)
transfer FOC: (V_a - lambda_a^+) - (V_b + lambda_b^-) = (V_b + lambda_b^-) * chi'(d)
```

Joint cone: `mu_a <= 0 AND mu_b >= 0`. Exists iff `W_max >= a_max + b_min` (Regime I).

### 3.8 Upper-a × W intersection `(a_max, W_max - a_max)` — Regime I only

```text
(V_a^eff, V_b^eff) = (V_a - lambda_a^+ - lambda_W, V_b - lambda_W)
transfer FOC: (V_a - V_b) - lambda_a^+ = (V_b - lambda_W) * chi'(d)
```

Joint cone: `mu_a <= 0 AND mu_W <= 0`. `lambda_W` cancels from the linear part;
`lambda_a^+` remains. Exists iff `W_max >= a_max + b_min`.

### 3.9 Lower-a × W intersection `(0, W_max)` — Regimes I and II

```text
(V_a^eff, V_b^eff) = (V_a + lambda_a^- - lambda_W, V_b - lambda_W)
transfer FOC: (V_a + lambda_a^-) - V_b = (V_b - lambda_W) * chi'(d)
```

Joint cone: `mu_a >= 0 AND mu_W <= 0` (at `a=0`, `mu_a = d >= 0`; `mu_W = d + mu_b
<= 0`). Exists for every `W_max >= b_min`.

### 3.10 Lower-b × W intersection `(W_max - b_min, b_min)` — Regime II only

```text
(V_a^eff, V_b^eff) = (V_a - lambda_W, V_b + lambda_b^- - lambda_W)
transfer FOC: V_a - (V_b + lambda_b^-) = (V_b + lambda_b^- - lambda_W) * chi'(d)
```

Joint cone: `mu_b >= 0 AND mu_W <= 0`. `lambda_W` cancels from the linear part;
`lambda_b^-` remains. Exists iff `b_min <= W_max < a_max + b_min` (Regime II).

## 4. KKT feasibility and complementarity (frozen)

For every active face/intersection the successor boundary-HJB solve must enforce:

- **Primal feasibility**: the selected control's drift satisfies the active tangent
  cone (`mu_a >= 0`, `mu_b >= 0`, `mu_a <= 0`, `mu_W <= 0` as applicable) to the
  frozen tolerance.
- **Multiplier feasibility**: every active `lambda_j >= 0`.
- **Complementarity**: `lambda_j * g_j = 0` for every active constraint; a
  multiplier is positive only when the unconstrained optimum would exit the domain
  through that face; when the unconstrained optimum is already admissible,
  `lambda_j = 0` and the interior FOCs are recovered.
- **Stationarity**: the control FOCs of Section 3 with the effective gradients of
  the active face(s).
- **Boundary branch/candidate semantics**: the selected policy on a face is the
  constrained Hamiltonian maximizer, not an interior policy that is clipped or
  relabeled. If the constrained problem itself admits no admissible policy at a
  boundary state, that is a **boundary-HJB scientific failure** (not a KFE repair
  opportunity).

## 5. Consistent facts re-verified (read-only)

- `d` cancels one-for-one from `mu_W`; `chi(d,a)` keeps `mu_W` (and the W KKT law)
  dependent on `d`.
- The `a_max` taper depends only on `a`; it does not stabilize the W face; the
  `a_max` face law (`mu_a <= 0`) is enforced by the constraint itself, with the
  quantitative tightening `d <= -0.27` at `a_max` under the accepted anchors.
- The KKT sign convention is internally consistent: `L = H - sum lambda_j g_j` with
  outward-normal `g_j = mu·n_j <= 0`, lower faces give `V + lambda`, upper/W faces
  give `V - lambda`.

## 6. Boundary policy diagnostics required of a successor

Freeze the successor diagnostic set (no execution here):

- active-face/active-intersection classification per state;
- selected `c, l, d` and resulting `mu_a, mu_b, mu_W` on every active face and
  intersection;
- KKT multipliers (feasibility `lambda >= 0`, complementarity slack);
- primal tangent-cone residual per active constraint;
- `BOUNDARY_POLICY_VIOLATION` semantics per the accepted DLH-5D contract (a
  materially outward requested normal drift is a fail-closed blocker, not a
  clipping opportunity).
