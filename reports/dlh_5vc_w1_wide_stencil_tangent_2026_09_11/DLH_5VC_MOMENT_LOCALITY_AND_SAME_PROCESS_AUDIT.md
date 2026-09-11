# DLH-5V-C — Moment, Locality and Same-Process Audit (Cone Closure, CTMC Certificate, Refinement, HJB/KFE)

**Issue:** deep-learning-hank #51 (DLH-5V-C) · **Branch:** `dsh/issue-51-dlh-5vc-w1-wide-stencil-tangent-2026-09-11`
Covers Issue §5.3 (tangential-cone closure), §5.4 (monotone CTMC feasibility certificate — analytic only),
§5.5 (refinement/locality), §5.6 (cell/face-control / same-process consistency), and the §7 failure-condition check.
Exact algebra only; tiny exact Fraction spot-checks in `%TEMP%` (not committed); no sweeps.

---

## 1. Tangential-cone closure (Issue §5.3) — equality proved

Physical generators of the augmented regular transition set:

```
w1 = (-10/19, 0)          [local inward (-1,0)]
w2 = (-70/19, +70/19)     [wide tangent (-7,+10)]
```

**Claim.** `cone{w1, w2} = T_realloc` where `T_realloc = {mu_a<=0, mu_b>=0, mu_a+mu_b<=0}`.

*Containment*: any `mu = c1·w1 + c2·w2`, `c1, c2 >= 0` has `mu_a = -(10 c1 + 70 c2)/19 <= 0`,
`mu_b = 70 c2/19 >= 0`, `mu_a + mu_b = -10 c1/19 <= 0` — hence `mu in T_realloc`.

*Covering*: write `mu in T_realloc` in the Issue parametrization `mu = (-a-b, +a)` with `a, b >= 0`
(extreme-ray representation `mu = a·(-1,1) + b·(-1,0)`; `(-1,0)` and `(-1,1)` are the extreme rays of
`T_realloc`, so every `mu in T_realloc` has `a = mu_b >= 0` and `b = -mu_a - mu_b >= 0`). Then

```
mu = (19 b/10)·w1 + (19 a/70)·w2,
```

because `(19 b/10)·(-10/19, 0) = (-b, 0)` and `(19 a/70)·(-70/19, +70/19) = (-a, +a)`, summing exactly to
`(-a-b, +a) = mu`. Both coefficients are nonnegative:

```
q_T  = 19 a / 70    (on the wide tangent w2; direction (-1,1))
q_in = 19 b / 10    (on the local inward w1; direction (-1,0))
```

**Equality holds exactly.**

The exact sliding ray `(-u, +u)` is recovered by `a = u`, `b = 0`: pure wide tangent, `q_T = 19u/70`,
`q_in = 0`.

## 2. Monotone CTMC feasibility certificate (Issue §5.4) — symbolic only

For a target first moment `mu = (-alpha-beta, +alpha)`, `alpha, beta >= 0`, the nonnegative rates

```
q_T = 19 alpha / 70        (on the wide tangent edge (-7,+10))
q_in = 19 beta / 10        (on the local inward edge (-1,0))
```

satisfy exactly

```
q_T·Delta x_T + q_in·Delta x_in
  = (19 alpha/70)·(-70/19, +70/19) + (19 beta/10)·(-10/19, 0)
  = (-alpha, +alpha) + (-beta, 0) = (-alpha-beta, +alpha) = mu.
```

- Rates are nonnegative and linear in `(alpha, beta)` (symbolic scaling: `q_T = (19/70) alpha`,
  `q_in = (19/10) beta`);
- the certificate covers **every** `mu in T_realloc`, in particular exact sliding;
- this is a **proof object only**: no production rate function, tie-breaking, control dependence, or strict
  face-flux replacement semantics is frozen or designed (deferred to the rate gate).

## 3. Refinement / locality audit (Issue §5.5)

Family `da_h = h·10/19`, `db_h = h·7/19` (fixed aspect `da/db = 10/7`), fixed index jump `(-7,+10)`, `h -> 0`.

1. **Physical jump = O(h).** `Delta x_T(h) = h·(-70/19, +70/19)`; `||Delta x_T(h)|| = h·(70/19)·sqrt(2) = O(h)`.
   (Spot-check: L1 norms `140/19, 70/19, 35/19, 14/19` at `h = 1, 1/2, 1/4, 1/10` — exactly halving.)
2. **Rate scaling for O(1) drift = O(1/h).** `q_T(h) = 19 alpha/(70 h)`, `q_in(h) = 19 beta/(10 h)`; the products
   `q_T(h)·h = 19 alpha/70`, `q_in(h)·h = 19 beta/10` are h-independent, so `q = O(1/h)` as required for a CTMC
   to realize an O(1) drift with an O(h) step.
3. **Smooth-test-function first-moment consistency (exact).** For `phi in C^2`, the generator acting on `phi`:

   ```
   (Q phi)(x) = q_T [phi(x + h·(-70/19,+70/19)) - phi(x)] + q_in [phi(x + h·(-10/19,0)) - phi(x)].
   ```

   Taylor expansion gives first-order terms `q_T h grad phi·u_T + q_in h grad phi·u_in`
   (`u_T = (-70/19,70/19)`, `u_in = (-10/19,0)`) = `grad phi·(q_T h u_T + q_in h u_in) = grad phi·mu` — the
   first moment matches the continuous drift **exactly** (by construction of `q_T, q_in`).
4. **Second-order remainder = O(h).** The second-order terms are `O(q_T h^2 + q_in h^2) = O((1/h)·h^2) = O(h)`.
   The stencil is first-order accurate (the wide jump is asymmetric — no cancellation of the second moment);
   the remainder vanishes as `h -> 0`. This is the standard order for a first-order monotone scheme; stated
   honestly, not claimed as second-order.
5. **Fixed 17-step Manhattan index distance vs physical locality.** `|Delta j| + |Delta i| = 17` is fixed in
   index space, but locality is a **physical** property: `||Delta x_T(h)|| = O(h) -> 0`, so the transition is
   local in the refinement limit. Index-space count is consistent: with `kappa_h = 19(W_max - b_min)/h`,
   `N_h = floor(kappa_h) = O(1/h)` columns, so `17/N_h = O(h) -> 0`; the deferred endpoint band is 7 fixed
   columns with physical width `70h/19 -> 0`. **No scientific inconsistency**: the wide stencil is
   "wide-stencil but local in the refinement limit".

## 4. Cell/face-control and same-process consistency (Issue §5.6)

The wide edge `(j,i) -> (j-7,i+10)` is a direct CTMC edge between two represented W-active states (representation
and W-activity proven in the destination/phase audit; class preserved, so the destination is W-active in the same
class). It enters the discrete framework as a single generator jump with rate `q_T(c,l,d) >= 0`:

```
H_h(c,l,d) = u(c) - v(l) + sum_r q_{s->r}(c,l,d)[V_r - V_s] + switch      (includes the wide term)
p_dot = Q^T p                                                              (same Q, same edge)
```

- **One `Q`, one controlled process**: the wide edge is part of the same Markov generator used backward (HJB)
  and forward (KFE); no different controlled processes are required. This preserves the accepted
  `HJB boundary policy <=> KFE boundary transition law` at the level of the generator.
- **W constraints remain cell-attached**: W-activity is still defined by the accepted restricted-Voronoi
  W-frontier cells; the wide edge connects two W-active represented states (state values remain node/cell
  values; the mass matrix `p = M g` semantics is untouched).
- **Not a shared-face flux**: the two endpoints share **no** Voronoi face, so the wide edge is **not** an
  ordinary finite-volume face flux `q_{s->r} = |F_{s,r}|·max(mu_s·n_{s,r},0)/omega_s`; it is explicitly a
  **boundary wide-stencil Markov transition** — a bounded extension of the accepted discrete Markov framework
  at the artificial W boundary only, keeping restricted-Voronoi cells for state partition and density semantics.
- Abandoning shared-face-only adjacency **at the artificial W boundary** is a legitimate bounded extension:
  interior adjacency is unchanged; the extension is confined to the recurring regular W-frontier classes
  audited here.

## 5. Issue §7 failure-condition check

| failure condition | status |
|---|---|
| wide destination not represented away from endpoints | NOT PROVEN (representation proved for all `j>=7`) |
| class/phase mapping fails structurally | NOT PROVEN (`r_{j-7}=r_j`; classes preserved) |
| augmented cone misses exact sliding or part of `T_realloc` | NOT PROVEN (cone equals `T_realloc` exactly) |
| nonnegative CTMC coefficients cannot match first moment | NOT PROVEN (explicit nonnegative certificate for all `mu in T_realloc`) |
| physical jump fails to become local under fixed-aspect refinement | NOT PROVEN (`||Delta x_T(h)|| = O(h)`; remainder `O(h)`) |
| wide edge necessarily violates finite domain/economic boundary in regular region | NOT PROVEN (violation confined to the deferred 7-column band `j in {0..6}`) |
| HJB and KFE would require different controlled processes | NOT PROVEN (one `Q`, one controlled process) |

All failures are confined to the precisely deferred endpoint band; **no recurring regular-class obstruction is
proven**. Hence Issue §12 Outcome A is the applicable terminal.

## 6. Verification log (tiny exact Fraction checks, `dlh5vc_wide_stencil.py`, `%TEMP%`)

1. `T_realloc` parametrization `mu = (-alpha-beta, +alpha)` reconstructed exactly with
   `q_in = 19 beta/10`, `q_T = 19 alpha/70` for `(alpha,beta) in {(1,0),(0,1),(7,3),(1/2,9/2),(0,0)}` —
   all exact, all nonnegative.
2. Sliding ray `(-3,+3)` = pure wide tangent: `q_T = 57/70`, `q_in = 0` — exact.
3. Refinement: physical jumps at `h = 1, 1/2, 1/4, 1/10` scale exactly as `O(h)`.

Result: **zero mismatches**.
