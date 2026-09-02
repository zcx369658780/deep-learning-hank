# DLH-5O Phase D — Transfer and Cross-State Self-Consistency (rev 2)

**Issue #41 Phase D.** Analyzes the key missing coupling `R = V_a/V_b` from DLH-5N,
tests the self-consistency of the candidate balance using the **combined transfer
Hamiltonian** `V_b*[d*q - chi]` (Phase A A3b) rather than `chi` in isolation, and
checks whether cross-`z` coefficient differences generate a productivity-switch term
of the same asymptotic order. All results are conditional on the Phase A analytic
assumptions and the derivative-control premise P-TR (`R = o(sqrt(b))` uniformly,
preferably `R = O(1)`).

Interior objects (accepted, read-only):

```text
R = V_a/V_b,   q = R - 1,
d  = a * T(q)/chi_1,   T(q) = min(q+chi_0,0) + max(q-chi_0,0)
chi(d,a) = chi_0|d| + 0.5 chi_1 d^2 / max(a, a_bar)
combined transfer Hamiltonian = d*V_a + (-d-chi)*V_b = V_b * [ d*q - chi ].
```

---

## D1. `R = V_a/V_b` order under the candidate and its alternatives

| Value-expansion structure | `V_a` | `V_b` | `R = V_a/V_b` |
|---|---|---|---|
| `V ~ V_inf(a,z) - K/b`, `V_inf` a-dependent | `O(1)` | `O(1/b^2)` | `O(b^2)` |
| `V ~ -K(a,z)/b`, `K` a-dependent | `O(1/b)` | `O(1/b^2)` | `O(b)` |
| `V ~ -K(z)/b + H(a,z)/b^2` (leading a-independent) | `O(1/b^2)` | `O(1/b^2)` | `-> H_a/K = O(1)` (nonzero in general) |
| `V ~ -K(z)/b + U(a,z)/b^{3/2}` | `O(b^{-3/2})` | `O(1/b^2)` | `~ Theta(sqrt(b))` (m = 1/2) |

- `R = O(b^2)` (a-dependent `V_inf`): `d ~ O(b^2)`, `chi ~ O(b^4)`, combined term
  `V_b*[d*q - chi] ~ O(b^2)` — unbalanced (the `d*V_a = O(b^2)` part is **inside** the
  combined term, so there is no separate counterpart). **Invalidates the candidate.**
- `R = O(b)` (a-dependent `K`): `d ~ O(b)`, `chi ~ O(b^2)`, combined term `O(1)` —
  unbalanced. **Invalidates the candidate.**
- `R -> H_a/K = O(1)` (leading a-independent, subleading a-derivative): `d = O(1)`,
  `chi = O(1)`, combined term `O(1/b^2)` — **self-consistent** and compatible with the
  candidate balance. This is the case P-TR (with `R = O(1)`) controls; note `R = 0` is
  **not** forced — the exact `q=-1`/`d=-0.45a` values do not follow here.
- `R ~ Theta(sqrt(b))` (m = 1/2): `d ~ Theta(sqrt(b))`, `chi ~ Theta(b)`, combined
  term `Theta(1/b)` — **same order** as the `O(1/b)` coefficient balance; this family
  is **UNRESOLVED / OPEN** and explicitly excluded from the theorem by P-TR.

**Conclusion (rev 2):** the bounded-transfer candidate is **not assumed** — it is the
`a`-structure consistent with the combined-Hamiltonian balance under P-TR; and the
claim that bounded transfer is "the unique a-structure" is **withdrawn** (the leading
a-independence `d_av V_inf = 0`, `d_aa K = 0` is necessary for `R = O(1)`, but the
remainder a-derivative may give `R = O(1)` nonzero; and `R ~ Theta(sqrt(b))` is a
distinct unresolved regime).

---

## D2. Transfer order in each regime (combined-Hamiltonian accounting)

- `R = O(1)` (uniform): `q = O(1)`, `d = O(1)`, `chi = O(1)`, combined term `O(1/b^2)`.
- `R = o(sqrt(b))` (uniform): `d = o(sqrt(b))`, `chi = o(b)`, combined term `o(1/b)`
  (sufficient direction retained from accepted DLH-5N M2/M3; per reviewer comment
  `5503274333`, the accepted controlling direction is the sufficient one — bounded
  ratio => bounded `d`, and uniform `T(q)=o(sqrt(b))` => `d=o(sqrt(b))`; it is **not**
  read as a uniform biconditional at `a=0` where the bare-`a` transfer vanishes).
- `R ~ b^m`, `m > 0`: `d ~ O(b^m)`, `chi ~ O(b^{2m})`, combined term `O(b^{2m-2})`.
  - `m > 1/2`: combined term more divergent than `O(1/b)` — inconsistent.
  - `m = 1/2`: same-order `Theta(1/b)` — **unresolved** (Phase B B4).
  - `0 < m < 1/2`: `o(1/b)` subleading — reduces to the analyzed class.

---

## D3. The candidate's transfer and adjustment cost (order statements; exact values only as a special case)

Under the candidate with P-TR and `R = O(1)`:

```text
q = O(1),   d = a*T(q)/chi_1 = O(1),   chi = O(1),   mu_a = r_a_eff(a)*a + d = O(1).
labor = (0.85 z V_b)^(1/5) ~ O(b^{-2/5}),   labor_income = o(1).
```

- The transfer is active or inactive depending on `|q|`; the **order** `d = O(1)`,
  `chi = O(1)` holds in either case under `R = O(1)`.
- **Exact limiting values are a separate special case.** If (and only if) the
  additional assumption `R -> 0` (i.e. `V_a/V_b -> 0`) is imposed/proved, then
  `q -> -1`, `T(-1) = -0.9`, `d -> -0.45a`, `chi -> 0.2475a` (for `a > a_bar`), and
  `mu_a -> a*(r_a_eff(a)-0.45) < 0`. These exact values are **not** derived from the
  leading ansatz and **not** implied by P-TR; they are labeled as the `R -> 0` special
  case only.
- The MATLAB-faithful upper-`a` branch (`at_upper_a` restricts `d < 0`) and lower-`a`
  corner (`d = 0` at `a = 0`) are finite-grid selection details; they do not change the
  interior order accounting.

---

## D4. Cross-`z` coefficient differences and the switch term

If `K` were z-dependent, `V(b,a,z') - V(b,a,z) ~ (K(z)-K(z'))/b`, so the switch term
`S*V ~ -S*K/b` is of the **same asymptotic order** (`O(1/b)`) as the other balance
terms. This is exactly why the `O(1/b)` equation retains `S*K` (Phase C C4):

```text
(rho + r_b)K - 2 sqrt(K) = S*K.
```

The coupled two-`z` system forces `K1 = K2 = K*` (Phase C C5), so within the
self-consistent candidate the cross-`z` value difference vanishes at `O(1/b)`:

```text
V(b,a,z') - V(b,a,z) ~ (K(z)-K(z'))/b = 0 + o(1/b).
```

This is a **derived** property of the candidate, not an assumption. (For `V_inf`
a-dependent the same switch argument applies to `V_inf` and forces `V_inf = 0` via
`(rho I - S)V_inf = 0` with `rho` not in the spectrum of `S`.)

---

## D5. Summary of self-consistency results (rev 2)

| Candidate property | Derived / premise | Status |
|---|---|---|
| `d_av V_inf = 0`, `d_aa K = 0` (leading a-independence) | necessary for `R = O(1)`; derived within candidate under P-TR | DERIVED (under P-TR) |
| `V_inf = 0` | `(rho I - S)V_inf = 0`, `rho` not in spectrum | DERIVED |
| `K` z-constant | coupled `O(1/b)` system, convexity argument | DERIVED |
| `R = O(1)` (or `o(sqrt(b))`) uniformly | derivative-control / transfer-ratio premise | PREMISE P-TR (not derived from leading ansatz) |
| `d = O(1)`, `chi = O(1)`, `mu_a = O(1)`, `labor = o(1)` | order statements under P-TR | ORDER STATEMENTS |
| `q = -1`, `d = -0.45a`, `chi = 0.2475a`, `mu_a = a*(r_a_eff-0.45)` | requires additional `R -> 0` assumption | SPECIAL CASE ONLY (not derived; not implied by P-TR) |
| cross-`z` switch term `O(1/b)` = 0 | follows from `K` z-constant | DERIVED |
| a-dependent `V_inf` / `K` invalidate the balance | combined-Hamiltonian accounting (`O(b^2)` / `O(1)` residual) | DERIVED |
| `R ~ Theta(sqrt(b))` (m=1/2) family | same-order combined term | **UNRESOLVED / OPEN** (excluded from theorem by P-TR) |
| uniqueness among all conceivable regimes | not established | NOT ANALYZABLE FROM ACCEPTED AUTHORITY |
