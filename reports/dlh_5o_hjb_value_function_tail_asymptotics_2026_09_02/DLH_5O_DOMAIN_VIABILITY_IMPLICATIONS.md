# DLH-5O Phase F — Relation to DLH-5N and Domain Viability (rev 2)

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
those missing objects from the source-faithful interior HJB balance — **conditional on
the derivative-control / transfer-ratio premise P-TR** (`R = V_a/V_b = o(sqrt(b))`
uniformly, preferably `O(1)`):

| Missing DLH-5N object | DLH-5O conditional result (rev 2, under P-TR) |
|---|---|
| `V_b` tail scaling | `V_b ~ K*/b^2`, `K* = 4/(rho+r_b)^2` |
| `R = V_a/V_b` | `o(sqrt(b))` uniformly (premise); `O(1)` in the preferred version; leading `d_av V_inf = d_aa K = 0`, but `R` need not be `0` (subleading remainder may give `R -> H_a/K = O(1)`) |
| `consumption` | `c ~ b/sqrt(K*)`, `c/b -> (rho+r_b)/2 = 0.0175` |
| `labor_income` | `O(b^{-2/5}) = o(1)` |
| `d`, `chi` | `d = O(1)`, `chi = O(1)` (order statements; exact `-0.45a`/`0.2475a` only under the extra `R -> 0` assumption) |
| cross-`z` value difference | `O(1/b)` and zero at `O(1/b)` (K z-constant) |
| net condition | `consumption + chi - labor_income - 0 = (0.0175 b + O(1))`, RHS `(r_b+eta)b + O(1)` with `eta = 0.0025` |

**Sign implication (conditional).** With `c/b = 0.0175 > r_b = 0.015`,
`mu_b ~ (r_b - c/b)b = -0.0025b < 0` and `mu_W = mu_a + mu_b ~ -0.0025b < 0`. So **if**
the `p = 2` balance is the realized tail **and P-TR holds**, the accepted HJB (via the
derivable interior identity) implies **fixed-`a` liquid-tail inwardness** with the
derived consumption ratio. This is consistent with (and sharpens) the DLH-5N
conditional inwardness sufficient condition: within the candidate, `labor_income = o(b)`
and `chi = O(1) = o(b)` hold, so the special-case `c/b` criterion is applicable and
gives `c/b = 0.0175 > r_b`.

---

## F2. Exact missing analytic assumptions (the gap to an established result)

The conditional result above does **not** become an established/unconditional theorem
because the accepted authority does not supply:

1. **A specified unbounded-`b` HJB problem**: an asymptotic boundary condition /
   transversality condition at `b -> +inf` is NOT in the source (Phase A A9). Any tail
   theorem must choose one (e.g., the candidate itself, or a no-arbitrage /
   transversality condition), which is an analytic-model decision, not source authority.
2. **Derivative-control / transfer-ratio premise (P-TR)**: `R = V_a/V_b = o(sqrt(b))`
   uniformly (preferably `O(1)`) is required to make the combined transfer Hamiltonian
   subleading; it is NOT in the source and NOT implied by leading a-independence of the
   coefficients (Phase A A9b; reviewer 5504354859, blocking 3).
3. **Smooth-continuum regularity / convergence**: the upwind finite-difference solution
   converging to a `C^1` continuum tail is an analytic assumption (Phase A A7, R1).
4. **Uniqueness of the balance**: ruling out HJB-consistent exotic tail regimes — in
   particular the unresolved `m = 1/2` family (`R ~ Theta(sqrt(b))`) — is not
   achievable from source authority alone (Phase B B4, R4).
5. **Uniformity**: uniform rates over `(a,z)` must be assumed or proved uniformly (R3).

These are the "missing analytic assumptions identified" that the Outcome B terminal
names.

---

## F3. Domain-viability implications (narrow)

- **Design W** requires total-wealth mean reversion in the tail to be a coherent
  truncation hypothesis. DLH-5O provides a **conditional** (not established) inward
  resolution: if the `p = 2` balance is the realized HJB tail **and P-TR holds**,
  `mu_W < 0` in the fixed-`a` liquid tail with `c/b = 0.0175`. Until the analytic-model
  gate establishes the candidate and P-TR (F2), W remains a plausible hypothesis, not a
  theory-established domain. `W_max` is NOT chosen.
- **Design R** receives no new support: the tail analysis concerns `b -> +inf` without
  an upper-`b` constraint; it does not establish R's componentwise law on a finite
  rectangle. R remains an unestablished candidate.
- **No `W_max`**, no R/W/W1/W2 selection, no new `b_max`/`a_max`, no taper
  extrapolation beyond `a_max = 10`, no stationary implication (stationary KFE remains
  NOT AUTHORIZED under Issue #27).
- The unresolved `m = 1/2` transfer family does not itself imply a domain statement; it
  only bounds the scope of the conditional theorem (it is excluded by P-TR).

---

## F4. Bottom line for the Owner

The accepted HJB authority is **sufficient to derive a conditional `p = 2`
dominant balance** with a full coefficient system (`V_inf = 0`, `K = 4/(rho+r_b)^2`,
`c/b = (rho+r_b)/2 = 0.0175 > r_b`, fixed-`a` liquid-tail inward) under an explicit
derivative-control / transfer-ratio premise P-TR, and **insufficient to establish it
unconditionally** because the unbounded-tail HJB problem (boundary / transversality),
smooth-continuum regularity, the transfer-ratio condition, uniqueness (including the
unresolved `m = 1/2` family), and uniformity are not specified by the finite-grid
source. The correct next gate is an **analytic-model specification** that defines those
ingredients and then verifies or refutes the candidate — before any domain/boundary
implementation authority.
