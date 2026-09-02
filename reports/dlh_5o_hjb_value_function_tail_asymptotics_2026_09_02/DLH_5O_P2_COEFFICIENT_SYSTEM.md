# DLH-5O Phase C — CRRA-2 `p = 2` Coefficient System (rev 2)

**Issue #41 Phase C.** Derives (conditionally) the coefficient system for the
candidate `V_b ~ K(a,z)/b^2` from the source-faithful interior HJB balance (Phase A
A5/A3b), integrating the derivative carefully, auditing `V_inf`, the leading `1/b`
equation for `K`, the `a`- and `z`-independence of `K`, and the implied consumption
ratio, and comparing with the frozen `r_b = 0.015` without importing any
representative-agent formula.

All steps are conditional on the analytic assumptions that the accepted finite-grid
source does not itself establish — in particular the **derivative-control /
transfer-ratio premise** `R = V_a/V_b = o(sqrt(b))` uniformly (preferably `O(1)`),
which the rev 1 package failed to state and which is required to make the combined
transfer term subleading. See Phase E for the full premise list.

---

## C1. Integrate the candidate derivative

Candidate: `V_b ~ K(a,z)/b^2` with `V_b > 0` and `K(a,z) > 0`. Integrating in `b`:

```text
V(b,a,z) ~ V_inf(a,z) - K(a,z)/b + o(1/b),
```

where `V_inf(a,z)` is the constant of integration.

Derivatives:
- `V_b ~ K/b^2`;
- `V_a ~ d_av V_inf - (d_aa K)/b + (a-derivative of the o(1/b) remainder)`.

**Rev 2 correction (reviewer 5504354859, blocking 2):** the leading expansion controls
only the first two coefficients. The `o(1/b)` remainder may itself be a-dependent,
e.g. `H(a,z)/b^2`, giving `V_a ~ H_a/b^2` and `R = V_a/V_b -> H_a/K = O(1)` — nonzero
even though `K_a = 0`. **`K_a = 0` does NOT imply `V_a = 0` or `R = 0`.** The transfer
ratio is therefore an independent object that must be controlled by an explicit
assumption (C2) or separately derived.

---

## C2. The derivative-control / transfer-ratio premise (explicit)

The combined transfer Hamiltonian (Phase A A3b) is `V_b*[d*(R-1) - chi(d,a)]`,
`R = V_a/V_b`. Its order is set by `R`:

```text
R = o(sqrt(b)) uniformly  =>  d = o(sqrt(b)),  chi = o(b),  combined term = o(1/b)   (subleading)
R = O(1) uniformly        =>  d = O(1),        chi = O(1),  combined term = O(1/b^2) (subleading)
R ~ b^m (m > 0)           =>  d ~ b^m,         chi ~ b^{2m}, combined term = O(b^{2m-2})
```

**Premise (P-TR).** The conditional `p=2` coefficient theorem assumes
`R = V_a/V_b = o(sqrt(b))` uniformly over `(a,z)`; the stronger and cleaner
`R = V_a/V_b = O(1)` uniformly is preferred. Under P-TR the combined transfer term is
subleading and does not enter the `O(1/b)` balance. This premise is **not** derived
from the leading ansatz; it is an explicit analytic assumption (or would need a
separate proof from the actual solution).

---

## C3. What the HJB implies for `V_inf` (under P-TR)

**Transfer self-consistency of the leading coefficients.** With `V_a = R*V_b` and
`R = O(1)` (P-TR), `V_a = O(V_b) = O(1/b^2)`. Since `V_a ~ d_av V_inf - (d_aa K)/b + ...`,
having `V_a = O(1/b^2)` requires `d_av V_inf = 0` and `d_aa K = 0`: the **leading
coefficients are a-independent**. This is a necessary condition for P-TR, not a
sufficient condition for `V_a = 0` (subleading `H(a,z)/b^2` may give `R -> H_a/K =
O(1)` nonzero; that is compatible with P-TR and with all transfer terms `O(1)`).

**O(1) balance.** With `d_av V_inf = 0` and `mu_a = r_a_eff(a)*a + d = O(1)` (since
`d = O(1)` under P-TR with `R = O(1)`), the `mu_a*V_a` term is `O(1/b^2)` and does not
enter `O(1)`. The O(1) part of the interior HJB is

```text
rho*V_inf(z) = (S*V_inf)(z),
```

and `(rho*I - S)V_inf = 0` with `rho = 0.02` not in the spectrum `{0,-2/3}` of `S`
gives

```text
V_inf = 0.
```

So the candidate reduces to `V ~ -K(a,z)/b` (leading) with subleading a-dependent
corrections `H(a,z)/b^2 + ...` allowed.

---

## C4. Leading `1/b` coefficient equation for `K(z)` (all same-order terms, under P-TR)

Substitute `V ~ -K(z)/b` (leading; `V_inf = 0`) and use P-TR so that the combined
transfer term is subleading. Collect `O(1/b)` terms:

| Term | `O(1/b)` coefficient |
|---|---|
| `rho*V` | `-rho*K` |
| `u = -1/c - l^6/6` | `-sqrt(K)` (`-l^6/6 ~ O(b^{-12/5})` is lower order) |
| `(r_b*b + labor - c)*V_b` | `(r_b - 1/sqrt(K))*K` (`labor = o(1)`, `c ~ (c/b)b`, `c/b = 1/sqrt(K)`) |
| `r_a_eff(a)*a*V_a` | `0` at `O(1/b)` (with `V_a = O(1/b^2)`, this is `O(1/b^2)`) |
| combined transfer `V_b*[d*q - chi]` | `0` at `O(1/b)` (subleading under P-TR) |
| `S*V` | `-S*K` |

Summing (multiply by `b`):

```text
-rho*K = -sqrt(K) + (r_b - 1/sqrt(K))*K - S*K
```

i.e.

```text
(rho + r_b)*K - 2*sqrt(K) = S*K.          (*)
```

No same-order term is omitted: the combined transfer Hamiltonian (with `d`, `chi`)
is retained and shown subleading under P-TR; labor and the `a`-axis term are audited;
the productivity switch `-S*K` is retained. The subleading `H(a,z)/b^2` corrections
contribute at `O(1/b^2)` and do not enter `(*)`.

> **Conditionality.** `(*)` and the coefficient below hold **only under P-TR**. In the
> `m = 1/2` regime (`R ~ Theta(sqrt(b))`) the combined transfer term is `Theta(1/b)`
> and `(*)` is **altered** by an a-dependent term; then `c/b = (rho+r_b)/2` does not
> follow (Phase B B4, left unresolved).

---

## C5. z-dependence of `K` and the value of `K`

For `S = [[-1/3,1/3],[1/3,-1/3]]`, write `(S*K)[z1] = (K2-K1)/3`,
`(S*K)[z2] = (K1-K2)/3`, and `f(K) = (rho+r_b)K - 2sqrt(K)`. The system (*) is

```text
f(K1) = (K2-K1)/3,   f(K2) = (K1-K2)/3 = -f(K1).
```

`f` is strictly convex, `f(K*) = 0` at `K* = 4/(rho+r_b)^2`, `f < 0` below `K*`,
`f > 0` above. A non-constant pair (`K1 != K2`) would require `K1 < K* < K2 < K1`
(symmetric for `K2 > K1`) — contradiction. Hence the only solution is

```text
K1 = K2 = K* = 4/(rho+r_b)^2,   i.e. K is z-constant.
```

With `rho = 0.02`, `r_b = 0.015`: `rho + r_b = 0.035`, `K* = 4/0.001225 = 3265.3`.

---

## C6. Implied asymptotic consumption ratio (conditional on P-TR)

`c = V_b^(-1/2)`, `V_b ~ K*/b^2`:

```text
c/b ~ 1/sqrt(K*) = (rho + r_b)/2 = 0.0175.
```

This is **not** imported from textbook or representative-agent knowledge; it follows
from the audited `O(1/b)` balance after all same-order terms are retained (C4-C5),
**under the corrected assumption set P-TR**.

**Comparison with frozen `r_b = 0.015`:**

```text
c/b - r_b = (rho + r_b)/2 - r_b = (rho - r_b)/2 = (0.02 - 0.015)/2 = 0.0025 > 0.
```

Consequently, within the candidate under P-TR, `mu_b ~ (r_b - c/b)b ~ -0.0025 b < 0`
and, since `mu_a = O(1)`, `mu_W = mu_a + mu_b ~ -0.0025 b < 0` — a **fixed-`a`
liquid-tail inward (mean-reverting)** sign, conditional on the candidate and P-TR.

---

## C7. Transfer and adjustment-cost order statements (rev 2)

Under P-TR with `R = O(1)` (preferred):

```text
d  = a*T(R-1)/chi_1 = O(1)      (order statement only)
chi = chi_0|d| + 0.5 chi_1 d^2/max(a,a_bar) = O(1)      (order statement only)
mu_a = r_a_eff(a)*a + d = O(1)
labor = (0.85z*V_b)^(1/5) ~ O(b^{-2/5}),   labor_income = o(1)
```

**Exact limiting transfer values are NOT claimed.** The exact `q=-1`, `d=-0.45a`,
`chi=0.2475a`, `mu_a = a*(r_a_eff(a)-0.45)` require the stronger assumption
`R -> 0` (equivalently `V_a/V_b -> 0`), which is **not** derived from the leading
ansatz and **not** implied by P-TR (`R = O(1)` allows `R -> H_a/K != 0`). They are
presented only as an explicitly-labeled special case under the additional assumption
`R -> 0` (Phase D D3); they are order statements `O(1)` in the main theorem.

---

## C8. Status of the coefficient system (rev 2)

- Derivable: YES, conditionally (from the source-faithful interior identity + FOCs,
  under the ansatz, P-TR, and the Phase A analytic assumptions).
- Unconditional from accepted authority: NO (the source does not specify the
  unbounded-tail problem, regularity, the transfer ratio, or uniqueness of the
  balance).
- The coefficient `(rho+r_b)/2` is reported because it follows from the audited
  balance under the corrected assumption set; it is not an assumption, and it is
  **withheld** outside P-TR (in particular for the unresolved `m = 1/2` family).
