# DLH-5O Phase D — Transfer and Cross-State Self-Consistency

**Issue #41 Phase D.** Analyzes the key missing coupling `V_a/V_b` from DLH-5N, tests
the self-consistency of any bounded-transfer candidate rather than assuming it, and
checks whether cross-`z` coefficient differences generate a productivity-switch term
of the same asymptotic order. All results are conditional on the Phase A analytic
assumptions.

Interior transfer/adjustment-cost objects (accepted, read-only):

```text
d  = a * T(V_a/V_b - 1)/chi_1,    T(q) = min(q+chi_0,0) + max(q-chi_0,0)
chi(d,a) = chi_0|d| + 0.5 chi_1 d^2 / max(a, a_bar)
q  = V_a/V_b - 1
```

---

## D1. `V_a/V_b` order under the candidate and its alternatives

| Value-expansion structure | `V_a` | `V_b` | `V_a/V_b` |
|---|---|---|---|
| `V ~ V_inf(a,z) - K/b`, `V_inf` a-dependent | `O(1)` | `O(1/b^2)` | `O(b^2)` |
| `V ~ -K(a,z)/b`, `K` a-dependent | `O(1/b)` | `O(1/b^2)` | `O(b)` |
| `V ~ -K(z)/b` (a-independent) | `0` (leading) | `O(1/b^2)` | `0` |

- `V_a/V_b = O(b^2)` (a-dependent `V_inf`): `d ~ O(b^2)`, `chi ~ O(b^4)` — destroys the
  balance (Phase B B3). **Invalidates the candidate.**
- `V_a/V_b = O(b)` (a-dependent `K`): `d ~ O(b)`, `chi ~ O(b^2)` — destroys the balance
  (Phase B B3). **Invalidates the candidate.**
- `V_a/V_b = 0` (a-independent `K`, `V_inf = 0`): `q = -1`, `d = -0.45a` (`O(1)`),
  `chi = O(1)`. **Self-consistent** (this is the candidate balance of Phase B/C).

**Conclusion:** the bounded-transfer candidate is **not assumed** — it is the unique
`a`-structure that keeps `d` and `chi` bounded; every a-dependent `V_inf` or `K`
feeds back through `d` and `chi` strongly enough to invalidate the balance.

---

## D2. Transfer order in each regime

- Bounded ratio (`V_a/V_b = O(1)`): `q = O(1)`, `d = O(1)`, `chi = O(1)`.
- `V_a/V_b = o(sqrt(b))` (uniform): `d = o(sqrt(b))`, `chi = o(b)` (the sufficient
  direction retained from accepted DLH-5N M2/M3; per reviewer comment `5503274333`,
  the accepted controlling direction is the sufficient one — bounded ratio => bounded
  `d`, and uniform `T(q)=o(sqrt(b))` => `d=o(sqrt(b))`; it is **not** read as a uniform
  biconditional at `a=0` where the bare-`a` transfer vanishes).
- `V_a/V_b ~ b^m`, `m > 0`: `d ~ O(b^m)`, `chi ~ O(b^{2m})`; for `m > 1/2` the
  superlinear adjustment cost breaks the balance (Phase B B4); for `0 < m <= 1/2` the
  regime is sub-superlinear and either collapses into the analyzed power-law classes or
  is not analyzable from accepted authority.

---

## D3. The candidate's transfer and adjustment cost (explicit)

Under the candidate (`V_inf = 0`, `K` a- and z-independent, `V_a = 0`):

```text
q = -1,
T(-1) = min(-1 + 0.1, 0) + max(-1 - 0.1, 0) = -0.9,
d(a) = a*(-0.9)/2 = -0.45 a   (O(1), <= 0 on [0,10]),
chi(a) = 0.1*0.45a + (0.45a)^2/max(a, a_bar)
       = 0.045a + 0.2025a = 0.2475a   for a > a_bar   (O(1), bounded on [0,10]),
mu_a = r_a_eff(a)*a + d = a*(r_a_eff(a) - 0.45) < 0   (O(1); illiquid drift inward).
```

- The transfer is **active** at the interior (`|q| = 1 > chi_0 = 0.1`) and negative
  (flows from `a` to `b`).
- The MATLAB-faithful upper-`a` branch (`at_upper_a` restricts `d < 0`) is consistent
  with `d < 0`; at `a = 0` the bare-`a` transfer is `0` (a corner point; the sufficient
  transfer direction still applies).
- `labor = (0.85 z V_b)^(1/5) ~ O(b^{-2/5})`, `labor_income ~ O(b^{-2/5}) = o(1)` —
  no `O(b)` or superlinear labor in the candidate.

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

## D5. Summary of self-consistency results

| Candidate property | Derived from the balance? | Status |
|---|---|---|
| `V_inf` a-independent | required by transfer consistency (else `chi ~ b^4`) | DERIVED (necessary within candidate) |
| `V_inf = 0` | `(rho I - S)V_inf = 0`, `rho` not in spectrum | DERIVED |
| `K` a-independent | required by transfer consistency (else `chi ~ b^2`) | DERIVED (necessary within candidate) |
| `K` z-constant | coupled `O(1/b)` system, convexity argument | DERIVED |
| `V_a/V_b = 0`, `d = -0.45a`, `chi = 0.2475a` | follows from `V_inf`/`K` a-independence | DERIVED |
| cross-`z` switch term `O(1/b)` = 0 | follows from `K` z-constant | DERIVED |
| bounded-transfer candidate is the only `a`-consistent family | all a-dependent variants invalidate the balance | DERIVED (within the analyzed classes) |
| uniqueness among all conceivable (non-power, transfer-dominated `m<=1/2`) regimes | not established | NOT ANALYZABLE FROM ACCEPTED AUTHORITY (requires the analytic-model gate) |
