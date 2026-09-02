# DLH-5O Phase F — Relation to DLH-5N and Domain Viability

**Issue #41 Phase F.** Translates the HJB result narrowly back to the accepted
DLH-5N net-drift condition, states what the accepted HJB implies (conditionally) for
the fixed-`a` liquid-tail sign, and identifies the exact missing analytic assumptions.
No R/W/W1/W2/`W_max` choice, no domain implication.

---

## F1. Relation to the accepted DLH-5N net condition

Accepted DLH-5N general net condition (exact identity):

```text
mu_W <= -eta*b  <==>  consumption + chi - labor_income - transfer_income
                            >= (r_b + eta)*b + r_a_eff(a)*a        (eventually).
```

DLH-5N Outcome B left the orders of `consumption`, `labor_income`, `chi` (through
`V_b`, `V_a/V_b`) unidentified. DLH-5O supplies a **candidate** resolution of exactly
those missing objects from the source-faithful interior HJB balance:

| Missing DLH-5N object | DLH-5O conditional result (under the `p = 2` candidate, R1-R4) |
|---|---|
| `V_b` tail scaling | `V_b ~ K*/b^2`, `K* = 4/(rho+r_b)^2` |
| `V_a/V_b` | `0` (leading) → `q = -1` |
| `consumption` | `c ~ b/sqrt(K*)`, `c/b -> (rho+r_b)/2 = 0.0175` |
| `labor_income` | `O(b^{-2/5}) = o(1)` |
| `d`, `chi` | `d = -0.45a`, `chi = 0.2475a` (`O(1)`) |
| cross-`z` value difference | `O(1/b)` and zero at `O(1/b)` (K z-constant) |
| net condition | `consumption + chi - labor_income - 0 = (0.0175 b + O(1))`, RHS `(r_b+eta)b + O(1)` with `eta = 0.0025` |

**Sign implication (conditional):** with `c/b = 0.0175 > r_b = 0.015`,
`mu_b ~ (r_b - c/b)b = -0.0025b < 0` and `mu_W = mu_a + mu_b ~ -0.0025b < 0`. So **if**
the `p = 2` balance is the realized tail, the accepted HJB (via the derivable interior
identity) implies **fixed-`a` liquid-tail inwardness** with the derived consumption
ratio. This is consistent with (and sharpens) the DLH-5N conditional inwardness
sufficient condition: within the candidate, `labor_income = o(b)` and `chi = O(1) =
o(b)` hold, so the special-case `c/b` criterion is applicable and gives `c/b = 0.0175
> r_b`.

---

## F2. Exact missing analytic assumptions (the gap to an established result)

The conditional result above does **not** become an established/unconditional theorem
because the accepted authority does not supply:

1. **A specified unbounded-`b` HJB problem**: an asymptotic boundary condition /
   transversality condition at `b -> +inf` is NOT in the source (Phase A A9). Any tail
   theorem must choose one (e.g., the candidate itself, or a no-arbitrage /
   transversality condition), which is an analytic-model decision, not source authority.
2. **Regularity / continuum convergence**: the upwind finite-difference solution
   converging to a `C^1` continuum tail is an analytic assumption (Phase A A7, R1).
3. **Uniqueness of the balance**: ruling out HJB-consistent exotic tail regimes is not
   achievable from source authority alone (Phase B B4, R4).
4. **Uniformity**: uniform rates over `(a,z)` must be assumed or proved uniformly
   (R3).

These are the "missing analytic assumptions identified" that the Outcome B terminal
names.

---

## F3. Domain-viability implications (narrow)

- **Design W** requires total-wealth mean reversion in the tail to be a coherent
  truncation hypothesis. DLH-5O provides a **conditional** (not established) inward
  resolution: if the `p = 2` balance is the realized HJB tail, `mu_W < 0` in the
  fixed-`a` liquid tail with `c/b = 0.0175`. Until the analytic-model gate
  establishes the candidate (F2), W remains a plausible hypothesis, not a
  theory-established domain. `W_max` is NOT chosen.
- **Design R** receives no new support: the tail analysis concerns `b -> +inf` without
  an upper-`b` constraint; it does not establish R's componentwise law on a finite
  rectangle. R remains an unestablished candidate.
- **No `W_max`**, no R/W/W1/W2 selection, no new `b_max`/`a_max`, no taper
  extrapolation beyond `a_max = 10`, no stationary implication (stationary KFE remains
  NOT AUTHORIZED under Issue #27).

---

## F4. Bottom line for the Owner

The accepted HJB authority is **sufficient to derive a conditional `p = 2`
dominant balance** with a full coefficient system (`V_inf = 0`, `K = 4/(rho+r_b)^2`,
`c/b = (rho+r_b)/2 = 0.0175 > r_b`, fixed-`a` liquid-tail inward), and **insufficient
to establish it unconditionally** because the unbounded-tail HJB problem (boundary /
transversality), regularity, uniqueness, and uniformity are not specified by the
finite-grid source. The correct next gate is an **analytic-model specification** that
defines those ingredients and then verifies or refutes the candidate — before any
domain/boundary implementation authority.
