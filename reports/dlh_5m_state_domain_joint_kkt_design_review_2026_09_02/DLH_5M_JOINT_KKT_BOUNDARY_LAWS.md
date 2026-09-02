# DLH-5M — Joint HJB/KKT Boundary Laws (Design R and Design W)

**Issue #39 §4, §5.** Generic state-constraint HJB/KKT derivation. No implementation,
no boundary-KKT coding, no `W_max`.

**Revision (2026-09-02, reviewer comment `5501914968`):** upper-face KKT multiplier
sign corrected to the maximization convention `L = H - lambda*g` for each active upper
constraint `g = mu·n <= 0` — effective gradients are `V - lambda`, not `V + lambda`.
The structural result is preserved: `lambda_W` cancels from the linear transfer term
but survives through the adjustment-cost derivative. `d` is not described as fully free
because `chi(d,a)` keeps the W constraint dependent on `d`.

All algebra below is derived from the accepted accounting and the accepted source
objects:

```text
mu_a  = r_a_eff(a)*a + d
mu_b  = r_b*b + labor_income - d - adjustment_cost(d,a) - (consumption - transfer_income)
mu_W  = mu_a + mu_b = r_a_eff(a)*a + r_b*b + labor_income - adjustment_cost(d,a)
                      - (consumption - transfer_income)
adjustment_cost(d,a) = chi_0*|d| + 0.5*chi_1*d^2/max(a,a_bar)     (accepted source)
transfer FOC (interior, differentiable d):  V_a - V_b = V_b * d/d d [adjustment_cost]
   =>  d = max(a,a_bar) * (min(q+chi_0,0) + max(q-chi_0,0)) / chi_1,  q = V_a/V_b - 1
r_a_eff(a) = r_a*(1 - 0.1*(a/a_max)^9),  a_max = 10
```

The accepted `transfer_candidate` is exactly the FOC solution with the inaction
kink `|q| < chi_0` (zero-transfer region), which is why `d` is a genuine control with
a convex, non-smooth adjustment cost.

---

## 1. Generic state-constraint HJB statement

Let `V` solve the household HJB. On an open interior region the Hamiltonian is

```text
rho*V = sup_{c,l,d} { u(c) - v_l*l + V_a*mu_a + V_b*mu_b }   (interior)
```

At a boundary face with a state constraint, the admissibility of controls is
restricted to the **active tangent cone**: the state drift must not exit the domain.
The correct statement is an optimization over controls admissible to that cone
(Carathéodory state-constrained / Crandall–Liggett viscosity formulation), **not**
post-hoc clipping and **not** branch forcing:

```text
rho*V = sup_{c,l,d : mu·n <= 0 on active face} { u(c) - v_l*l + V_a*mu_a + V_b*mu_b }   (constrained)
```

Introducing non-negative KKT multipliers `lambda_j >= 0` for each active drift
constraint `g_j = mu·n_j <= 0`, with complementarity `lambda_j * (mu·n_j) = 0`, gives
the constrained Hamiltonian. Because this is a **maximization** problem and each
active constraint is an upper bound `g_j <= 0`, the consistent KKT Lagrangian
**subtracts** the multiplier times the constraint:

```text
rho*V = sup_{c,l,d} { u(c) - v_l*l + V_a*mu_a + V_b*mu_b - sum_j lambda_j * (mu·n_j) }.
```

Each multiplier therefore enters the *effective value gradients* with a **minus**
sign (`V - lambda_j`), exactly where the constrained control interacts with the drift.
(The same convention `L = H - lambda*g` is applied below to every upper face.)

---

## 2. Design R — rectangular componentwise laws

Active-face tangent cones:

```text
upper-a (a=a_max):  mu_a <= 0      multiplier lambda_a >= 0
upper-b (b=b_max):  mu_b <= 0      multiplier lambda_b >= 0
lower-b (b=b_min):  mu_b >= 0
lower-a (a=0):      mu_a >= 0
joint corner:       mu_a <= 0 AND mu_b <= 0      (both multipliers active)
```

### 2.1 Upper-b face

Constrained Hamiltonian (b-face), maximization KKT convention `L = H - lambda_b*mu_b`:

```text
rho*V = sup_{c,l,d} { u(c) - v_l*l + V_a*mu_a + (V_b - lambda_b)*mu_b },  lambda_b*(mu_b) = 0.
```

Only the `b`-gradient is modified (reduced by `lambda_b`). Consequences for the
control FOCs:

- consumption: `u'(c) = V_b - lambda_b` (at the cap additional liquid wealth cannot
  be accumulated, so its shadow price is reduced);
- transfer FOC (differentiable branch): `V_a - (V_b - lambda_b) = (V_b - lambda_b)*adj'(d)`,
  i.e. the linear reallocation FOC sees `lambda_b` explicitly on the left (a larger
  `a`-vs-`b` value gap is required to reallocate `b -> a`) and the adjustment-cost
  resource term is scaled by `(V_b - lambda_b)`. With `lambda_b > 0` the effective
  `b`-value gradient is reduced, tilting the transfer toward converting `b -> a`:
  net `b` accumulation is **inadmissible** above the cap;
- when the unconstrained optimum already satisfies `mu_b <= 0`, `lambda_b = 0` and the
  interior FOCs are recovered (complementarity).

### 2.2 Upper-a face

```text
rho*V = sup_{c,l,d} { u(c) - v_l*l + (V_a - lambda_a)*mu_a + V_b*mu_b },  lambda_a*(mu_a) = 0.
```

Only the `a`-gradient is modified (reduced by `lambda_a`). Transfer FOC:

```text
(V_a - lambda_a) - V_b = V_b*adj'(d)
```

i.e. the effective `a`-gradient is reduced, tilting the transfer away from `a`
accumulation (net `a` accumulation is inadmissible at the cap).

### 2.3 Joint upper corner (both active)

```text
rho*V = sup_{c,l,d} { u(c) - v_l*l + (V_a - lambda_a)*mu_a + (V_b - lambda_b)*mu_b },
       lambda_a*(mu_a) = 0,  lambda_b*(mu_b) = 0.
```

Transfer FOC:

```text
(V_a - lambda_a) - (V_b - lambda_b) = (V_b - lambda_b)*adj'(d).
```

Both gradients are reduced. The corner law requires **componentwise** inwardness
`mu_a <= 0 AND mu_b <= 0`; this is the rectangular tangent-cone condition (see the
geometry-consistency rejection test in `DLH_5M_GEOMETRY_CANDIDATES.md`).

### 2.4 Equivalence with the current MATLAB-faithful ordering

**Not equivalent.** The current solver closes the upper-b face by a one-sided
finite-difference value reconstruction (`vb_boundary_closure` vs `vb_backward`,
accepted DLH-5K localization evidence) and the accepted DLH-5K
`joint_corner_feasibility` shows the selected transfer candidate fails joint
rectangular inwardness at all 17 offenders. There is no KKT multiplier on `mu_b <= 0`
in the current boundary treatment. Retaining Design R therefore requires a genuine
state-constraint HJB/KKT reformulation of the boundary value problem (implementation
task under separate authority).

---

## 3. Design W — hybrid joint-wealth laws

Active-face tangent cones on `D_W = {a>=0, b>=b_min, a<=a_max, a+b<=W_max}`:

```text
W face (a+b=W_max):   mu_W = mu_a + mu_b <= 0     multiplier lambda_W >= 0
upper-a (a=a_max):    mu_a <= 0                   multiplier lambda_a >= 0
lower-b (b=b_min):    mu_b >= 0
lower-a (a=0):        mu_a >= 0
intersection a=a_max, W=W_max:  mu_a <= 0 AND mu_W <= 0   (lambda_a, lambda_W active)
```

### 3.1 W face

Constrained Hamiltonian (W-face), maximization KKT convention
`L = H - lambda_W*mu_W`:

```text
rho*V = sup_{c,l,d} { u(c) - v_l*l + V_a*mu_a + V_b*mu_b - lambda_W*(mu_a + mu_b) }
      = sup_{c,l,d} { u(c) - v_l*l + (V_a - lambda_W)*mu_a + (V_b - lambda_W)*mu_b },
       lambda_W*(mu_W) = 0.
```

The multiplier enters both value gradients **symmetrically** (as a subtraction).
Consequences:

- **linear transfer cancellation in the FOC:** the linear `d` part of
  `(V_a-lambda_W)*mu_a + (V_b-lambda_W)*mu_b` contributes
  `(V_a-lambda_W)*d + (V_b-lambda_W)*(-d) = (V_a - V_b)*d` — the `lambda_W` cancels
  one-for-one from the linear reallocation, exactly mirroring the drift identity that
  the linear `d` cancels in `mu_W`;
- **transfer FOC (differentiable branch):**

  ```text
  V_a - V_b = (V_b - lambda_W)*adj'(d).
  ```

  `lambda_W` survives **only through the adjustment-cost resource cost**
  `(V_b-lambda_W)*adj'(d)` (the rebalancing cost is paid in b-resources, whose
  effective shadow price at the cap is `V_b-lambda_W`). Because `chi(d,a)` keeps the
  `W` constraint dependent on `d`, the reallocation is **not fully free**: `d` is
  pinned by this FOC through the adjustment-cost term. If adjustment cost were zero,
  the transfer FOC would be exactly the interior FOC at the cap;
- consumption: `u'(c) = V_b - lambda_W` (total wealth is a b-like resource for
  consumption at the cap, with reduced shadow price);
- complementarity: `lambda_W > 0` only when the unconstrained optimum would exit
  `D_W` through the W face.

Economic reading: at the joint-wealth cap the household can still rebalance `b -> a`
free of any **direct cap tax on the linear transfer** — `lambda_W` cancels from the
linear part of the transfer FOC; the rebalancing is governed by the transfer FOC whose
adjustment-cost resource term is scaled by `(V_b - lambda_W)`. This is the formal
sense in which W is consistent with the portfolio-reallocation interpretation accepted
in DLH-5L, in contrast to the R corner law (2.3), whose tangent cone makes net `b`
accumulation inadmissible even when financed by `a` drawdown.

### 3.2 Upper-a face (W)

Identical to R upper-a (2.2): `lambda_a` modifies (reduces) the `a`-gradient only.

### 3.3 Intersection a = a_max, W = W_max

```text
rho*V = sup_{c,l,d} { u(c) - v_l*l + (V_a - lambda_a - lambda_W)*mu_a
                      + (V_b - lambda_W)*mu_b },  lambda_a*(mu_a)=0, lambda_W*(mu_W)=0.
```

Transfer FOC:

```text
(V_a - V_b) - lambda_a = (V_b - lambda_W)*adj'(d).
```

`lambda_W` cancels from the linear part; `lambda_a` remains (a-face multiplier). The
joint law requires `mu_a <= 0 AND mu_W <= 0`. This intersection lies on the boundary
of `D_W` only for parameter ranges implied by the (symbolic) `W_max`; see
`DLH_5M_GEOMETRY_CANDIDATES.md` §2.

### 3.4 KFE generator / tangent-flow requirements (design statement)

If `W` were later selected, the KFE generator on `D_W` must satisfy the
HJB ↔ KFE boundary-transition contract (Issues #26–#27):

- no outward flux through any active face (the tangent cone is the same set of
  admissible drifts used by the HJB);
- on the slanted `W` face the normal flux equals `mu_W` (with unit normal
  `n = (1,1)/sqrt(2)`), so conservativity requires a discrete Gauss theorem across
  the face — the hard part of W1 (masked tensor) and the moved part of W2
  (transformed `(a,W)` where the cap becomes flat but the borrowing floor becomes
  slanted);
- HJB and KFE must share the exact same controlled domain and boundary law.

These are design requirements only; no generator is built in DLH-5M.

---

## 4. Summary of the control-FOC structure

| Active constraint | Effective gradients | Linear `d` in FOC | Adjustment-cost term in FOC | Net economic effect |
|---|---|---|---|---|
| none (interior) | `V_a`, `V_b` | `V_a - V_b` | `V_b * adj'(d)` | rebalancing free up to adjustment cost |
| R upper-b (`mu_b<=0`) | `V_a`, `V_b-lambda_b` | `V_a - (V_b-lambda_b)` | `(V_b-lambda_b)*adj'(d)` | reduced b shadow price; net b accumulation inadmissible |
| R upper-a (`mu_a<=0`) | `V_a-lambda_a`, `V_b` | `(V_a-lambda_a) - V_b` | `V_b*adj'(d)` | reduced a shadow price; net a accumulation inadmissible |
| R corner (`mu_a<=0, mu_b<=0`) | `V_a-lambda_a`, `V_b-lambda_b` | `(V_a-lambda_a)-(V_b-lambda_b)` | `(V_b-lambda_b)*adj'(d)` | componentwise admissibility; net accumulation in either coordinate inadmissible |
| W face (`mu_W<=0`) | `V_a-lambda_W`, `V_b-lambda_W` | `V_a - V_b` (**lambda_W cancels**) | `(V_b-lambda_W)*adj'(d)` | no direct tax on linear rebalancing; adjustment cost keeps `mu_W` dependent on `d` |
| W ∩ a-max (`mu_a<=0, mu_W<=0`) | `V_a-lambda_a-lambda_W`, `V_b-lambda_W` | `(V_a - V_b) - lambda_a` | `(V_b-lambda_W)*adj'(d)` | a-face multiplier; W multiplier only via adjustment cost |

The distinguishing mathematical fact: at a W face the KKT multiplier enters both
value gradients symmetrically and cancels from the linear transfer FOC; at an R
upper-b/corner the multiplier enters the `b` gradient only. Under the maximization KKT
convention each multiplier **subtracts** from the effective gradient (the shadow price
of a coordinate is reduced at its cap), and the R corner tangent cone makes net liquid
accumulation inadmissible even when financed by illiquid drawdown. This is the precise
sense in which W is more consistent with the accepted reallocation interpretation, and
why the "replace `mu_b<=0` by `mu_W<=0` at the corner" shortcut (which imposes neither
coherent law) is a geometry-inconsistent weakening rather than either coherent law.

No boundary law is implemented in DLH-5M.
