# DLH-5O Phase C — CRRA-2 `p = 2` Coefficient System

**Issue #41 Phase C.** Derives (conditionally) the coefficient system for the
candidate `V_b ~ K(a,z)/b^2` from the source-faithful interior HJB balance (Phase A
A5), integrating the derivative carefully, auditing `V_inf`, the leading `1/b`
equation for `K`, the `a`- and `z`-independence of `K`, and the implied consumption
ratio, and comparing with the frozen `r_b = 0.015` without importing any
representative-agent formula.

All steps are conditional on the analytic assumptions that the accepted finite-grid
source does not itself establish (continuum/regularity, the ansatz, tail boundary /
transversality specification, uniformity, uniqueness) — see Phase E.

---

## C1. Integrate the candidate derivative

Candidate: `V_b ~ K(a,z)/b^2` with `V_b > 0` and `K(a,z) > 0`. Integrating in `b`:

```text
V(b,a,z) ~ V_inf(a,z) - K(a,z)/b + o(1/b),
```

where `V_inf(a,z)` is the constant of integration (the limit of `V` as `b -> +inf`,
a-priori possibly depending on `(a,z)`).

Derivatives:
- `V_b ~ K/b^2`;
- `V_a ~ dV_inf/da - (dK/da)/b`.

---

## C2. What the HJB implies for `V_inf` (including the switch block)

**Transfer self-consistency first.** If `dV_inf/da != 0`, then
`V_a/V_b ~ (dV_inf/da) b^2/K -> +inf`; the transfer FOC gives `d ~ a*T(q)/chi_1` with
`q -> +inf`, i.e. `d ~ O(b^2)`; then `chi ~ O(b^4)`, `mu_b ~ -O(b^4)`, and
`mu_b V_b ~ -O(b^2)`, an unbalanced `O(b^2)` term (no other `O(b^2)` object exists in
the balance). Hence a self-consistent candidate **must** have `V_inf` a-independent:
`V_inf = V_inf(z)`.

**O(1) balance (with the switch block).** With `V_inf` a-independent, the O(1) part of
the interior HJB is

```text
rho*V_inf(z) = mu_a * (dV_inf/da) + (S*V_inf)(z) = (S*V_inf)(z),
```

because `dV_inf/da = 0` and the `mu_b V_b` term is `O(1/b)` (no O(1) part), `u` is
`O(1/b)` (no O(1) part), and `mu_a V_a` is `O(1/b)` (next-order `V_a`). Here
`(S*V_inf)(z) = sum_z' lambda (V_inf(z')-V_inf(z))` with `lambda = 1/3`.

`(rho*I - S)V_inf = 0`. The generator `S = [[-1/3,1/3],[1/3,-1/3]]` has spectrum
`{0, -2/3}`; `rho = 0.02` is not in the spectrum, so the only bounded solution is

```text
V_inf = 0.
```

So the candidate reduces to `V ~ -K(a,z)/b`.

---

## C3. `a`-dependence of `K`: forced to vanish

With `V ~ -K(a,z)/b`:

- `V_b ~ K/b^2`, `V_a ~ -(dK/da)/b`;
- `V_a/V_b ~ -(dK/da) b / K ~ O(b)` if `dK/da != 0`.

An `O(b)` transfer ratio gives `q ~ O(b)`, `d ~ a*T(q)/chi_1 ~ O(b)`,
`chi ~ O(b^2)` (from `d^2/max(a,a_bar)`), `mu_b ~ -O(b^2)`, and
`mu_b V_b ~ -O(1)` — an unbalanced `O(1)` residual (all other terms are `O(1/b)`).
Hence a self-consistent candidate **must** have `dK/da = 0`:

```text
K = K(z)   (a-independent),   V_a = 0 (leading),   V_a/V_b = 0.
```

Then `q = -1`, `T(-1) = min(-0.9,0) + max(-1.1,0) = -0.9`, and
`d = a*(-0.9)/chi_1 = -0.45a` (bounded, `O(1)`, negative = outflow from `a` to `b` at
interior `a`), `chi = 0.1|d| + d^2/max(a,a_bar)`:
for `a > a_bar`, `chi = 0.045a + 0.2025a = 0.2475a` (bounded `O(1)`);
`labor = (0.85z*V_b)^(1/5) ~ O(b^{-2/5})`, `labor_income = o(1)`.

---

## C4. Leading `1/b` coefficient equation for `K(z)` (all same-order terms)

Substitute `V ~ -K(z)/b` into the interior HJB and collect `O(1/b)` terms:

| Term | `O(1/b)` coefficient |
|---|---|
| `rho*V` | `-rho*K` |
| `u = -1/c - l^6/6` | `-sqrt(K)` (`-l^6/6 ~ O(b^{-12/5})` is lower order) |
| `mu_b*V_b` | `(r_b - 1/sqrt(K))*K` (`mu_b ~ (r_b - 1/sqrt(K))b + 0.2025a + o(1)`; the `0.2025a` part gives `O(1/b^2)`) |
| `mu_a*V_a` | `0` (`V_a = 0`) |
| `S*V` | `-S*K` |

Summing (multiply by `b`):

```text
-rho*K = -sqrt(K) + (r_b - 1/sqrt(K))*K - S*K
```

i.e.

```text
(rho + r_b)*K - 2*sqrt(K) = S*K.          (*)
```

No same-order term is omitted: transfer (`d = -0.45a`, `O(1)`), adjustment cost
(`chi = 0.2475a`, `O(1)`), labor (`labor_income = o(1)`), productivity switch
(`-S*K`), and the `a`-axis term (`mu_a*V_a = 0`) are all audited. The `O(1)` part of
`mu_b` (`0.2025a`) enters only at `O(1/b^2)` and is subleading.

---

## C5. z-dependence of `K` and the value of `K`

For `S = [[-1/3,1/3],[1/3,-1/3]]`, write `(S*K)[z1] = (K2-K1)/3`,
`(S*K)[z2] = (K1-K2)/3`, and `f(K) = (rho+r_b)K - 2sqrt(K)`. The system (*) is

```text
f(K1) = (K2-K1)/3,   f(K2) = (K1-K2)/3 = -f(K1).
```

`f` is strictly convex, `f(K*) = 0` at `K* = 4/(rho+r_b)^2`, `f < 0` below `K*`,
`f > 0` above. A non-constant pair (`K1 != K2`) would require, say `K1 > K2`,
`f(K1) < 0` (so `K1 < K*`) and `f(K2) > 0` (so `K2 > K*`), forcing `K1 < K* < K2 < K1`
— contradiction (symmetric for `K2 > K1`). Hence the only solution is

```text
K1 = K2 = K* = 4/(rho+r_b)^2,   i.e. K is z-constant.
```

With `rho = 0.02`, `r_b = 0.015`: `rho + r_b = 0.035`, `K* = 4/0.001225 = 3265.3`.

---

## C6. Implied asymptotic consumption ratio (derived, not imported)

`c = V_b^(-1/2)`, `V_b ~ K*/b^2`:

```text
c/b ~ 1/sqrt(K*) = (rho + r_b)/2 = 0.0175.
```

This is **not** imported from textbook or representative-agent knowledge; it follows
from the audited `O(1/b)` balance after all same-order terms are retained (C4-C5).

**Comparison with frozen `r_b = 0.015`:**

```text
c/b - r_b = (rho + r_b)/2 - r_b = (rho - r_b)/2 = (0.02 - 0.015)/2 = 0.0025 > 0.
```

Consequently, within the candidate, `mu_b ~ (r_b - c/b)b ~ -0.0025 b < 0` and, since
`mu_a = O(1)`, `mu_W = mu_a + mu_b ~ -0.0025 b < 0` — a **fixed-`a` liquid-tail inward
(mean-reverting)** sign, conditionally on the candidate.

---

## C7. Status of the coefficient system

- Derivable: YES, conditionally (from the source-faithful interior identity + FOCs,
  under the ansatz and the analytic assumptions of Phase A).
- Unconditional from accepted authority: NO (the source does not specify the
  unbounded-tail problem, regularity, or uniqueness of the balance).
- The coefficient `(rho+r_b)/2` is reported because it follows from the audited
  balance; it is not an assumption.
