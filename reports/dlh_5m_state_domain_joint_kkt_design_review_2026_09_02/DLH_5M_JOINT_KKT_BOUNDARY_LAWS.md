# DLH-5M — Joint HJB/KKT Boundary Laws (Design R and Design W)

**Issue #39 §4, §5.** Generic state-constraint HJB/KKT derivation. No implementation,
no boundary-KKT coding, no `W_max`.

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
constraint `mu·n_j <= 0`, with complementarity `lambda_j * (mu·n_j) = 0`, gives the
constrained Hamiltonian

```text
rho*V = sup_{c,l,d} { u(c) - v_l*l + V_a*mu_a + V_b*mu_b + sum_j lambda_j * (mu·n_j) }.
```

The multiplier changes the *effective value gradients* entering each FOC exactly where
the constrained control interacts with the drift.

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

Constrained Hamiltonian (b-face):

```text
rho*V = sup_{c,l,d} { u(c) - v_l*l + V_a*mu_a + (V_b + lambda_b)*mu_b },  lambda_b*(mu_b) = 0.
```

Only the `b`-gradient is raised. Consequences for the control FOCs:

- consumption: `u'(c) = V_b + lambda_b` (consumption is a b-resource; the constraint
  raises its shadow price);
- transfer FOC (differentiable branch): `V_a - (V_b + lambda_b) = (V_b + lambda_b)*adj'(d)`,
  i.e. the linear reallocation is taxed at `lambda_b` and the adjustment-cost
  resource cost is scaled by `(V_b + lambda_b)`. A `lambda_b > 0` directly taxes net
  `b` accumulation, **including accumulation financed by `a` drawdown**;
- when the unconstrained optimum already satisfies `mu_b <= 0`, `lambda_b = 0` and the
  interior FOCs are recovered (complementarity).

### 2.2 Upper-a face

```text
rho*V = sup_{c,l,d} { u(c) - v_l*l + (V_a + lambda_a)*mu_a + V_b*mu_b },  lambda_a*(mu_a) = 0.
```

Only the `a`-gradient is raised. Transfer FOC:

```text
(V_a + lambda_a) - V_b = V_b*adj'(d)
```

i.e. the `a`-gradient is taxed, tilting the transfer toward `a` accumulation.

### 2.3 Joint upper corner (both active)

```text
rho*V = sup_{c,l,d} { u(c) - v_l*l + (V_a + lambda_a)*mu_a + (V_b + lambda_b)*mu_b },
       lambda_a*(mu_a) = 0,  lambda_b*(mu_b) = 0.
```

Transfer FOC:

```text
(V_a + lambda_a) - (V_b + lambda_b) = (V_b + lambda_b)*adj'(d).
```

Both gradients are raised. The corner law requires **componentwise** inwardness
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

Constrained Hamiltonian (W-face):

```text
rho*V = sup_{c,l,d} { u(c) - v_l*l + V_a*mu_a + V_b*mu_b + lambda_W*(mu_a + mu_b) }
      = sup_{c,l,d} { u(c) - v_l*l + (V_a + lambda_W)*mu_a + (V_b + lambda_W)*mu_b },
       lambda_W*(mu_W) = 0.
```

The multiplier adds **equally** to both value gradients. Consequences:

- **linear transfer cancellation in the FOC:** the linear `d` part of
  `(V_a+lambda_W)*mu_a + (V_b+lambda_W)*mu_b` contributes `(V_a+lambda_W)*d +
  (V_b+lambda_W)*(-d) = (V_a - V_b)*d` — the `lambda_W` cancels one-for-one from the
  linear reallocation, exactly mirroring the drift identity `d` cancels in `mu_W`;
- **transfer FOC (differentiable branch):**

  ```text
  V_a - V_b = (V_b + lambda_W)*adj'(d).
  ```

  `lambda_W` survives **only through the adjustment-cost resource cost**
  `(V_b+lambda_W)*adj'(d)` (the rebalancing cost is paid in b-resources, whose shadow
  price is `V_b+lambda_W`). If adjustment cost were zero, the transfer FOC would be
  exactly the interior FOC at the cap;
- consumption: `u'(c) = V_b + lambda_W` (total wealth is a b-like resource for
  consumption at the cap);
- complementarity: `lambda_W > 0` only when the unconstrained optimum would exit
  `D_W` through the W face.

Economic reading: at the joint-wealth cap the household can still rebalance `b -> a`
free of any direct cap tax on the linear transfer; only the resource cost of
rebalancing (adjustment cost) is affected. This is the formal sense in which W is
consistent with the portfolio-reallocation interpretation accepted in DLH-5L, in
contrast to the R corner law (2.3) which taxes `b` accumulation directly.

### 3.2 Upper-a face (W)

Identical to R upper-a (2.2): `lambda_a` raises the `a`-gradient only.

### 3.3 Intersection a = a_max, W = W_max

```text
rho*V = sup_{c,l,d} { u(c) - v_l*l + (V_a + lambda_a + lambda_W)*mu_a
                      + (V_b + lambda_W)*mu_b },  lambda_a*(mu_a)=0, lambda_W*(mu_W)=0.
```

Transfer FOC:

```text
(V_a - V_b) + lambda_a = (V_b + lambda_W)*adj'(d).
```

`lambda_W` cancels from the linear part; `lambda_a` remains (a-face tax). The joint
law requires `mu_a <= 0 AND mu_W <= 0`.

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
| R upper-b (`mu_b<=0`) | `V_a`, `V_b+lambda_b` | `V_a - (V_b+lambda_b)` | `(V_b+lambda_b)*adj'(d)` | taxes b-accumulation incl. a-financed |
| R upper-a (`mu_a<=0`) | `V_a+lambda_a`, `V_b` | `(V_a+lambda_a) - V_b` | `V_b*adj'(d)` | taxes a-accumulation |
| R corner (`mu_a<=0, mu_b<=0`) | `V_a+lambda_a`, `V_b+lambda_b` | `(V_a+lambda_a)-(V_b+lambda_b)` | `(V_b+lambda_b)*adj'(d)` | componentwise tax on both |
| W face (`mu_W<=0`) | `V_a+lambda_W`, `V_b+lambda_W` | `V_a - V_b` (**lambda_W cancels**) | `(V_b+lambda_W)*adj'(d)` | no direct tax on linear rebalancing |
| W ∩ a-max (`mu_a<=0, mu_W<=0`) | `V_a+lambda_a+lambda_W`, `V_b+lambda_W` | `(V_a - V_b) + lambda_a` | `(V_b+lambda_W)*adj'(d)` | a-face tax; W tax only via adjustment cost |

The distinguishing mathematical fact: at a W face the KKT multiplier enters both
value gradients symmetrically and cancels from the linear transfer FOC; at an R
upper-b/corner the multiplier enters the `b` gradient only, taxing net liquid
accumulation even when financed by illiquid drawdown. This is the precise sense in
which W is more consistent with the accepted reallocation interpretation, and why the
"replace `mu_b<=0` by `mu_W<=0` at the corner" shortcut (which taxes neither) is a
geometry-inconsistent weakening rather than either coherent law.

No boundary law is implemented in DLH-5M.
