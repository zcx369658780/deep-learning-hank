# DLH-5N Phase B — Asymptotic Term-Order Table

**Issue #40 Phase B (rev 2).** Decomposes the asymptotic order of every term in
`mu_W` as `b -> +infinity` with `a in [0,10]` fixed and `z in {0.8,1.3}` finite,
under the accepted source identities (read-only). No new state is computed; this is
an order-of-magnitude accounting of the accepted formulas. Rev 2 applies the
asymptotic-order corrections of fresh ChatGPT review comment `5503060588`.

Controlling identity:

```text
mu_W = r_a_eff(a)*a + r_b*b + labor_income + transfer_income - chi(d,a) - consumption
```

## Term-order table

| # | Term in `mu_W` | Accepted formula (frozen values) | Order as `b -> +inf` | Sign | Provable / conditional |
|---|---|---|---|---|---|
| T1 | `r_b*b` | `0.015*b` | `O(b)` | `+` | **PROVABLE** (r_b=0.015>0 frozen; linear) |
| T2 | `r_a_eff(a)*a` | `0.03*a*(1-0.1*(a/10)^9)`, `a in [0,10]` | `O(1)` (`max 0.27`) | `>= 0` | **PROVABLE** (compact a, explicit bound) |
| T3 | `labor_income` | `(0.85*z)^(6/5) * V_b^(1/5)` | `O(V_b^(1/5))`; `o(b)` if `V_b = o(b^5)`; `->0` if `V_b -> 0`; **otherwise b-order UNIDENTIFIED** (e.g. `V_b = O(b^5)` gives `O(b)` labor) | `>= 0` | **CONDITIONAL** (needs `V_b` tail) |
| T4 | `transfer_income` | `0.0` (frozen scalar) | `O(1)` | `0` | **PROVABLE** (fixed, state-independent) |
| T5 | `-consumption` | `-V_b^(-1/2)` | `-O(V_b^(-1/2))`; with `V_b = O(b^{-(2+delta)})` this is `-Omega(b^{1+delta/2})` | `-` | **CONDITIONAL** (key object: `V_b` tail decay) |
| T6 | `-chi(d,a)` | `-(0.1|d| + d^2/max(a,a_bar))` | `-O(|d| + d^2)`; **`chi = o(b)` iff `d = o(sqrt(b))`** (NOT merely `d = o(b)`); `chi = O(1)` iff `d = O(1)` | `-` | **CONDITIONAL** (needs `V_a/V_b` tail) |
| T7 | `mu_W` total | sum of T1-T6 | sign unresolved | ? | **UNRESOLVED** without control asymptotics |

**M1.6 (remainder):** absent explicit tail assumptions, the b-orders of T3, T5, T6
(and hence of the remainder `mu_W - r_b*b`) are **NOT_IDENTIFIED_BY_CURRENT_ACCEPTED_AUTHORITY**;
the unconditional remainder is not known to be `O(1) + o(b)`.

## Dominant-balance observations

1. **T1 (`r_b*b`) is the only guaranteed positive `O(b)` term.** For `mu_W <= -eta*b`
   eventually, the net object `T5 + T6 + labor_income` must dominate
   `T1 + T2 + T4`. The **general** condition (an exact rearrangement of the
   identity, not an assumption) is:

   ```text
   consumption + chi(d,a) - labor_income - transfer_income
       >= (r_b + eta)*b + r_a_eff(a)*a        (eventually, eta > 0).
   ```

   The asymptotic consumption-wealth-ratio criterion `c/b` bounded below by `r_b`
   is a **special case** of this net condition, valid only under separately stated
   `labor_income = o(b)` and `chi = o(b)` assumptions (e.g. bounded transfer ratio);
   it is **not** equivalent in general and **not necessary** (adjustment cost can
   itself provide an `O(b)` or superlinear negative contribution).

2. **The `a`-support enters only through bounded/compact terms** (`T2`, the
   `max(a,a_bar)` in the adjustment cost, and the `a`-multiplier of `d`). For fixed
   `a in [0,10]`, the `a`-dependence is `O(1)`. **Uniformity is not automatic from
   compactness**: any uniform rate/conclusion (as used in the M2 net condition and
   M3 outward condition) must be assumed or proved uniformly, not inferred from
   compactness alone.

3. **`z` enters through `T3` (a positive `O(V_b^(1/5))` term with `z`-dependent
   constant) and through the HJB `z`-jump term.** The finite `z`-support alone does
   **not** bound `V(b,a,z') - V(b,a,z)` as `b` grows; absent a bound on cross-`z`
   value differences, the `z`-jump contribution to the HJB has **UNIDENTIFIED**
   b-order (this matters for the proposed deeper HJB-asymptotic gate, not for the
   `mu_W` accounting, where `z` enters only through `T3` and the value derivatives).

4. **The knife-edge is the exponent of `V_b` (special case, bounded transfer).**
   Writing `V_b ~ b^{-p}` with bounded `V_a/V_b = O(1)` (so `chi = O(1)`) and
   `labor_income = o(b)`, `consumption ~ b^{p/2}`; the balance is inward for
   `p > 2` (via `consumption = Omega(b^{1+delta/2})`), outward for `p < 2`, and
   borderline `(c/b vs r_b)` for `p = 2`. In general (without bounded transfer), the
   net condition of observation 1 governs, and `chi` can be `O(b)` or superlinear.
   Accepted authority does not fix `p`.

## Order summary (special-case rows: bounded `V_a/V_b = O(1)` unless stated)

| Regime for the endogenous tail | Leading-order `mu_W` | Tail classification |
|---|---|---|
| `V_b ~ b^{-p}`, `0 < p < 2`, `V_a/V_b = o(sqrt(b))` (e.g. `O(1)`) | `r_b*b + o(b) -> +inf` | **OUTWARD** (non-mean-reverting) |
| `V_b ~ b^{-2}`, `V_a/V_b = O(1)` | `(r_b - c/b)*b` | **BORDERLINE** (special-case sign = sign(r_b - c/b)) |
| `V_b ~ b^{-p}`, `p > 2`, `V_a/V_b = O(1)` | `r_b*b - Omega(b^{p/2}) -> -inf` | **INWARD** (mean-reverting) |
| general (no transfer bound) | net condition governs; `chi` order unidentified | **UNRESOLVED** |

The middle row is the "natural" mean-reversion conjecture (consumption a constant
fraction of wealth), but it is a conjecture about the HJB solution, **not an accepted
theorem**. See `DLH_5N_THEOREM_AND_COUNTEREXAMPLE_MATRIX.md`.
