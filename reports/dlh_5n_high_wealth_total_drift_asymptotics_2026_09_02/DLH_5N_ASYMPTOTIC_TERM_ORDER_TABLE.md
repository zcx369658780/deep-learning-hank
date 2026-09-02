# DLH-5N Phase B — Asymptotic Term-Order Table

**Issue #40 Phase B.** Decomposes the asymptotic order of every term in `mu_W` as
`b -> +infinity` with `a in [0,10]` fixed and `z in {0.8,1.3}` finite, under the
accepted source identities (read-only). No new state is computed; this is an
order-of-magnitude accounting of the accepted formulas.

Controlling identity:

```text
mu_W = r_a_eff(a)*a + r_b*b + labor_income + transfer_income - chi(d,a) - consumption
```

## Term-order table

| # | Term in `mu_W` | Accepted formula (frozen values) | Order as `b -> +inf` | Sign | Provable / conditional |
|---|---|---|---|---|---|
| T1 | `r_b*b` | `0.015*b` | `O(b)` | `+` | **PROVABLE** (r_b=0.015>0 frozen; linear) |
| T2 | `r_a_eff(a)*a` | `0.03*a*(1-0.1*(a/10)^9)`, `a in [0,10]` | `O(1)` (`max 0.27`) | `>= 0` | **PROVABLE** (compact a, explicit bound) |
| T3 | `labor_income` | `(0.85*z)^(6/5) * V_b^(1/5)` | `O(V_b^(1/5))`; `o(b)` if `V_b = o(b^5)`; `->0` if `V_b -> 0` | `>= 0` | **CONDITIONAL** (needs `V_b` tail) |
| T4 | `transfer_income` | `0.0` (frozen scalar) | `O(1)` | `0` | **PROVABLE** (fixed, state-independent) |
| T5 | `-consumption` | `-V_b^(-1/2)` | `-O(V_b^(-1/2))` | `-` | **CONDITIONAL** (key object: `V_b` tail decay) |
| T6 | `-chi(d,a)` | `-(0.1|d| + d^2/max(a,a_bar))` | `-O(|d| + d^2)`; `d = a*T(V_a/V_b-1)/chi_1` | `-` | **CONDITIONAL** (needs `V_a/V_b` tail) |
| T7 | `mu_W` total | sum of T1-T6 | sign unresolved | ? | **UNRESOLVED** without control asymptotics |

## Dominant-balance observations

1. **T1 (`r_b*b`) is the only guaranteed positive `O(b)` term.** For `mu_W < 0`
   eventually, the negative group `T5 + T6` (consumption plus adjustment cost) must
   exceed `T1 + T2 + T3 + T4`; since `T2,T4` are `O(1)` and `T3` is `o(b)` under weak
   conditions, the binding requirement is
   `consumption - labor_income + chi - transfer_income > r_b*b + r_a_eff(a)*a`
   eventually (equivalently: the asymptotic consumption-wealth ratio
   `c/b` must be bounded below by `r_b`).

2. **The `a`-support enters only through bounded/compact terms** (`T2`, the
   `max(a,a_bar)` in the adjustment cost, and the `a`-multiplier of `d`). For fixed
   `a in [0,10]`, the `a`-dependence is `O(1)`; uniformity over `a` is therefore
   a compactness argument once a rate is established pointwise.

3. **`z` enters only through `T3` (a positive `O(V_b^(1/5))` term with `z`-dependent
   constant) and through the HJB jump term (which is `O(1)` in `b`).** The finite
   `z`-support does not change the leading order.

4. **The knife-edge is the exponent of `V_b`.** Writing `V_b ~ b^{-p}` (see Phase D),
   `consumption ~ b^{p/2}`; the balance is inward for `p > 2`, outward for `p < 2`,
   and borderline `(c/b vs r_b)` for `p = 2`. Accepted authority does not fix `p`.

## Order summary

| Regime for the endogenous tail | Leading-order `mu_W` | Tail classification |
|---|---|---|
| `V_b ~ b^{-p}`, `0 < p < 2`, `V_a/V_b = o(b)` | `r_b*b + o(b) + O(1) -> +inf` | **OUTWARD** (non-mean-reverting) |
| `V_b ~ b^{-2}`, `V_a/V_b = O(1)` | `(r_b - c/b)*b` | **BORDERLINE** (sign = sign(r_b - c/b)) |
| `V_b ~ b^{-p}`, `p > 2`, `V_a/V_b = O(1)` | `r_b*b - O(b^{p/2}) -> -inf` | **INWARD** (mean-reverting) |

The middle row is the "natural" mean-reversion conjecture (consumption a constant
fraction of wealth), but it is a conjecture about the HJB solution, **not an accepted
theorem**. See `DLH_5N_THEOREM_AND_COUNTEREXAMPLE_MATRIX.md`.
