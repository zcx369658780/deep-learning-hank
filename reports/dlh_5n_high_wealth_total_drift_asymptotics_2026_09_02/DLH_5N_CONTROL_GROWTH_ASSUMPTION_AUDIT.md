# DLH-5N Phase C — Control-Growth Assumption Audit

**Issue #40 Phase C.** Audits which control/value-derivative growth rates are
provable from accepted authority, which are conditional on explicit (unproven)
assumptions, and which are unidentified. Activation rule 6 is applied: no growth
rate is assumed unless proved from accepted authority; otherwise the minimum
explicit condition is stated or the object is marked unidentified.

---

## Audit table

| # | Object | Provable from accepted authority? | Minimum explicit condition / note |
|---|---|---|---|
| C1 | `r_b*b` | **PROVABLE**: `O(b)`, `+`, `-> +inf` | `r_b = 0.015 > 0` frozen |
| C2 | `r_a_eff(a)*a` | **PROVABLE**: `O(1)`, `>= 0`, `<= 0.27` | `a in [0,10]` compact; taper frozen |
| C3 | `V_b` positivity | **PROVABLE**: `V_b > 0` required (consumption FOC raises on `V_b <= 0`) | no bound on decay |
| C4 | `V_b` tail decay rate | **NOT IDENTIFIED BY ACCEPTED AUTHORITY** | the decisive missing object; a tail rate would require an HJB asymptotic theorem (Route N-B) |
| C5 | `consumption = V_b^(-1/2)` | **CONDITIONAL**: `O(V_b^(-1/2))` | `c = o(b)` iff `V_b^{-1} = o(b^2)` (i.e. `V_b` decays slower than `b^{-2}`); `c ~ O(b)` iff `V_b ~ b^{-2}`; `c` superlinear iff `V_b` decays faster than `b^{-2}` |
| C6 | `labor = (V_b*0.85*z)^(1/5)` | **CONDITIONAL**: `O(V_b^(1/5))` | decays toward 0 if `V_b -> 0`; bounded otherwise |
| C7 | `labor_income` | **CONDITIONAL**: `O(V_b^(1/5))`, `>= 0` | `-> 0` if `V_b -> 0`; `o(b)` under essentially all plausible `V_b` decay; not a source of positive `O(b)` drift |
| C8 | `V_a/V_b` tail behavior | **NOT IDENTIFIED BY ACCEPTED AUTHORITY** | drives the transfer and adjustment cost; no accepted tail statement |
| C9 | `d = a*T(V_a/V_b - 1)/chi_1` | **CONDITIONAL**: `O(a*T(q))`, `|d| <= 10*|T(q)|/chi_1` | bounded iff `V_a/V_b = O(1)`; `o(b)` iff `V_a/V_b = o(b)` |
| C10 | `chi(d,a)` | **CONDITIONAL**: `O(|d| + d^2/max(a,a_bar))`, `>= 0` | `O(1)` iff `d = O(1)`; `o(b)` iff `d = o(sqrt(b))`; the `max(a,a_bar)` denominator is bounded below by `a_bar` |
| C11 | `transfer_income` | **PROVABLE**: `O(1)`, fixed `0.0` in fixture | state-independent scalar |
| C12 | `z` process | **PROVABLE**: finite Markov `{0.8,1.3}`, rate 1/3 | contributes `O(1)` terms in `b`; no tail effect |

---

## What is provable vs conditional vs unidentified (summary)

- **Provable (frozen-source only):** `r_b*b` (`O(b)`, `+`); `r_a_eff(a)*a`
  (`O(1)`, `>= 0`, `<= 0.27`); `transfer_income` (`O(1)`, `0.0`); `V_b > 0`;
  `a in [0,10]` compact; `z` finite.
- **Conditional (explicit unproven assumption required):** `consumption`,
  `labor`/`labor_income`, `d`, `chi` — each has an explicit minimum condition stated
  in terms of `V_b` (decay exponent) and `V_a/V_b`.
- **Unidentified (no accepted authority, no statement possible):** the tail decay of
  `V_b` (equivalently the asymptotic consumption-wealth ratio `c/b`) and the tail
  behavior of `V_a/V_b`.

## Implication for `mu_W`

Because `c`, `l`, `d`, `chi` are all conditional/unidentified, and the only provably
positive `O(b)` term is `r_b*b`, the sign of `mu_W` in the fixed-`a` liquid tail is
**conditional**: it is determined by the (unestablished) tail decay exponent of `V_b`
and the (unestablished) tail behavior of `V_a/V_b`. This is the exact sense in which
Outcome A (unconditional inwardness) is not provable and Outcome B applies.
