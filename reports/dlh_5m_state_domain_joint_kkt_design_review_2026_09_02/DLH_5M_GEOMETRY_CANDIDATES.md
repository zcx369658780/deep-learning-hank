# DLH-5M — Domain-Geometry Candidates (Design R, Design W, W1, W2)

**Issue #39 §4, §5, §6.** Analytical comparison only. No implementation, no grid, no
`W_max` selection.

Accepted accounting (immutable):

```text
mu_a = r_a_eff(a)*a + d
mu_b = r_b*b + labor_income - d - adjustment_cost(d,a) - (consumption - transfer_income)
mu_W = mu_a + mu_b = r_a_eff(a)*a + r_b*b + labor_income - adjustment_cost(d,a)
                     - (consumption - transfer_income)
r_a_eff(a) = r_a*(1 - 0.1*(a/a_max)^9),  a_max = 10
```

---

## 1. Design R — rectangular componentwise state constraints (Issue #39 §4)

**Domain:** the current computational rectangle `{a in [0,a_max], b in [b_min,b_max]}`.

**Tangent-cone conditions on active faces:**

```text
upper-a face (a=a_max):  mu_a <= 0
upper-b face (b=b_max):  mu_b <= 0
joint upper corner:      mu_a <= 0 AND mu_b <= 0
lower-b face:            mu_b >= 0
lower-a face:            mu_a >= 0
```

**Correct state-constraint HJB/KKT statement:** on each active face the household
maximizes the HJB Hamiltonian over controls admissible to the active tangent cone
(no post-hoc clipping, no branch forcing). See `DLH_5M_JOINT_KKT_BOUNDARY_LAWS.md`
for the multiplier structure.

**Which controls enter each drift constraint:**

| Drift | Controls entering | Linear `d` |
|---|---|---|
| `mu_a = r_a_eff(a)*a + d` | `d` (`+1`) | yes |
| `mu_b = ... - d - adjustment_cost(d,a) - (c - transfer_income)` | `d`, `c`, `l` (through `labor_income`), adjustment cost | yes (`-1`) plus nonlinear cost |
| `mu_W = mu_a + mu_b` | `c`, `l`, adjustment cost | **cancels one-for-one** |

**Is the current MATLAB-faithful upper-b/upper-a ordering equivalent to the
constrained problem? No.** The accepted DLH-5K `joint_corner_feasibility` shows the
selected transfer candidate is infeasible for joint rectangular inwardness at all 17
offenders, and the current solver closes the upper-b boundary by one-sided
finite-difference value reconstruction (`vb_boundary_closure` vs `vb_backward`)
rather than a KKT multiplier on `mu_b <= 0`. The current boundary treatment is a
truncation convention, not the tangent-cone constrained problem.

**What must change conceptually if rectangular geometry is retained:** a genuine
state-constraint HJB/KKT boundary-value formulation on every active face and at the
corner, with the same law mirrored in the KFE. This is an implementation task under
separate authority, not authorized in DLH-5M.

---

## 2. Design W — hybrid joint-wealth truncation (Issue #39 §5)

**Candidate domain:**

```text
D_W = { a >= 0,  b >= b_min,  a <= a_max,  a + b <= W_max }
```

**Required normal/tangent conditions:**

```text
W face (a + b = W_max):          mu_W = mu_a + mu_b <= 0
upper-a face (a = a_max):        mu_a <= 0
intersection a=a_max, W=W_max:   mu_a <= 0 AND mu_W <= 0
lower-b face:                    mu_b >= 0
lower-a face:                    mu_a >= 0
```

**Source facts supporting `W = a + b` as an accounting coordinate:** the accepted
accounting gives `mu_W = mu_a + mu_b` with `d` cancelling one-for-one, so the
total-wealth drift is independent of the instantaneous reallocation `d`. This is a
genuine accounting-additivity fact about the drift decomposition.

**Mandatory distinction:** accounting additivity is **not** the economic claim that
`W` must be the production truncation variable. The accepted evidence shows `mu_W < 0`
on the pre-frozen finite high-wealth set, which is consistent with `W` as a good
truncation coordinate but is not an infinite-domain theorem and does not by itself
authorize `W` as the production truncation variable.

**Compatibility with the accepted `a_max`-normalized taper:** the illiquid support
`a <= a_max` is retained as a separate face, so the taper is unchanged on `a`. The `W`
cap adds a slanted (45° in `(a,b)`) face that the `a`-normalized taper does not
stabilize; at the `W` face (away from `a_max`) the illiquid return is taper-unaffected
and `mu_W <= 0` must be enforced by the constraint itself. No conflict, no help.

**Geometry of the slanted W boundary:** `a + b = W_max` is the line of slope `-1`.
Active-constraint intersections: `W` ∩ `{a=0}` at `b = W_max`; `W` ∩ `{a=a_max}` at
`b = W_max - a_max` (joint corner, `mu_a <= 0` and `mu_W <= 0` both active);
`W` ∩ `{b=b_min}` at `a = W_max - b_min`. Two multipliers are active at each
intersection.

**Generic constrained HJB/KKT at the W face:** maximize subject to `mu_W <= 0`. Since
`d` cancels from `mu_W`, the `W`-face constraint binds only consumption, labor and
adjustment cost; the transfer `d` remains free to reallocate `b -> a` at the cap. This
is the key economic contrast with Design R: at the corner, R forbids net `b`
accumulation even when financed by `a` drawdown, while W permits internal rebalancing
as long as total wealth does not grow.

**KFE generator/tangent-flow requirements (design statement only):** a conservative
generator on `D_W` with the flux through the slanted `W` face matched to the
controlled dynamics (normal flux `= mu_W` on the face), and HJB/KFE sharing the exact
same controlled domain and boundary law (controlled-process matching).

---

## 3. Representation options for Design W (Issue #39 §6)

### W1 — masked `(a,b)` tensor grid

Retain the tensor lattice; treat states beyond `a + b <= W_max` as outside the domain.

| Aspect | Assessment |
|---|---|
| Stencil loss near slanted boundary | The 45° cut removes neighbors on the `W` face; asymmetric one-sided stencils appear. |
| Generator conservation | Conservative discretization of the slanted face requires explicit flux bookkeeping; otherwise mass leaks. |
| Boundary-neighbor topology | Neighbor sets change discontinuously across the cut. |
| Exact HJB/KFE process matching | Harder: the discrete process must respect the same slanted face in both operators. |

### W2 — transformed `(a,W)` representation

Set `b = W - a` analytically. Drifts: `mu_a` unchanged; `W`-drift is `mu_W` (the total
drift; `d` absent). Transformed domain:

```text
a in [0, a_max],  W in [W_lower(a), W_max],  W_lower(a) = a + b_min
faces: a=0, a=a_max, W=W_max (flat, coordinate-aligned), W = a + b_min (slanted)
```

| Aspect | Assessment |
|---|---|
| Transformed drift identities | `mu_W = mu_a + mu_b` becomes the coordinate drift; `d` appears only in `mu_a`. |
| Transformed lower-b constraint | `b >= b_min` becomes `W >= a + b_min`, a slanted face in `(a,W)`. |
| Is the transformed domain simpler? | Not unambiguously: the `W` cap becomes flat (good) but the borrowing floor becomes slanted (the difficulty moves, it does not disappear). Domain is a trapezoid with two vertical sides, a flat top, a slanted bottom. |
| Implications for the accepted taper and transfer FOC | Taper is `a`-based and survives unchanged; the transfer FOC couples `a` and `W` (since `d` moves `a` but not `W`). |

Neither W1 nor W2 is selected in DLH-5M; both require additional design work before
implementation authority.

---

## 4. Geometry-consistency rejection test (Issue #39 §7)

Shortcut: keep the rectangle but at the joint upper corner replace `mu_b <= 0` by
`mu_W <= 0`.

- Rectangular corner tangent cone: `C_rect = {(v_a,v_b): v_a <= 0, v_b <= 0}`.
- Shortcut condition (keeping `mu_a <= 0`, replacing `mu_b <= 0`): `C_shortcut =
  {(v_a,v_b): v_a <= 0, v_a + v_b <= 0}`.
- `C_rect ⊊ C_shortcut`: e.g. `(-1, +0.5)` has `v_a <= 0`, `v_a + v_b = -0.5 <= 0` but
  `v_b > 0`.
- Accepted offenders (`mu_a < 0, mu_b > 0, mu_W < 0`) lie in `C_shortcut` but not in
  `C_rect`.

**Verdict: geometry-inconsistent. Reject.** The shortcut is a PASS-seeking relabeling
that enlarges the admissible cone at the corner; it must not be recommended merely
because it makes the accepted offender states pass. A rectangle with a correct corner
law requires componentwise inwardness on each active face.

---

## 5. Summary comparison

| | Design R | Design W |
|---|---|---|
| Upper-b face | constrained face `mu_b <= 0` | removed; replaced by `W` cap |
| Upper-a face | `mu_a <= 0` | `mu_a <= 0` |
| Joint corner | `mu_a <= 0 AND mu_b <= 0` | `mu_a <= 0 AND mu_W <= 0` |
| Transfer at cap | restricted (`mu_b <= 0` binds even a-financed b-accumulation) | free reallocation (`d` cancels in `mu_W`) |
| Economic status of cap | treats truncation as constraint | cap is a truncation; economic status of `W` as production variable unresolved |
| Numerical standardness | standard rectangle lattice | slanted face / transformed coordinates |
| Freezability on accepted evidence | not freezable (truncation-as-constraint) | not freezable (W_max undefined, finite-state evidence only) |
