# DLH-5O / Issue #41 — Fixed-`a` Liquid-Tail HJB Value-Function Asymptotics

**Task type:** `SCIENTIFIC_THEORY_ANALYSIS__HJB_VALUE_FUNCTION_LIQUID_TAIL_SCALING`
**Date:** 2026-09-02
**Branch:** `dsh/issue-41-dlh-5o-hjb-value-tail-asymptotics-2026-09-02`
**Fresh `origin/main` baseline:** `1646d9c3636b87372eaa28425360d022ff510eab`

This is a **theory/documentation gate only**. No source mutation, no HJB/KFE/grid
run, no stationary operation, no domain choice, no imported textbook tail condition.

DLH-5O asks whether the **accepted HJB authority** (the MATLAB-faithful finite-grid
household solver, immutable) is sufficient to derive the large-positive-`b` scaling of
the value function and its derivatives — `V_b`, `V_a/V_b`, and the cross-productivity
difference `V(b,a,z') - V(b,a,z)` — and thereby resolve the asymptotic consumption
ratio `c/b` and the sign of `mu_W` on the fixed illiquid support `0 <= a <= a_max = 10`.

---

## 0. Controlling accepted authority

- Issue #40 / DLH-5N **accepted** and closed. Accepted candidate
  `bded30a8b8cb579c3f359a62f5b530d7c34b7526`; reviewer acceptance
  `DLH_5N_REV2_ACCEPTED__OUTCOME_B_SUPPORTED__FIXED_A_LIQUID_TAIL_SIGN_REMAINS_CONDITIONAL__HJB_VALUE_FUNCTION_TAIL_ASYMPTOTICS_NEXT_GATE_REQUIRED`
  (comment `5503274333`); integration commit `e23b1ada5f5ab1b11c1291d8141d8286884553d4`.
- Accepted DLH-5N terminal:
  `DLH_5N_FIXED_A_LIQUID_TAIL_TOTAL_WEALTH_SIGN_CONDITIONAL__MISSING_CONTROL_ASYMPTOTICS_IDENTIFIED`.
- Accepted household source (immutable, read-only):
  `src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`
  (blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`,
  SHA-256 `1795718C469FC3B427CAB8E3D5957C133BEAD6EACC9EF0A25A3EDB7211D1A024`).
- Frozen D0 configuration (read-only): `configs/dlh_5b_two_region_symmetric_anchor.toml`
  (region index 0), `configs/dlh_5l_total_wealth_domain_geometry_diagnostic.toml`.
- Issue #27 HJB<->KFE same-controlled-process contract remains binding; stationary KFE
  remains NOT AUTHORIZED.
- R and W remain unfrozen; no `W_max`; no new `b_max`/`a_max`; the accepted taper is not
  extrapolated beyond `a_max = 10`.

---

## 1. Scientific question (restated narrowly)

> Under the accepted household economics with `0 <= a <= a_max = 10`, can the accepted
> HJB authority itself determine the large-positive-`b` scaling of `V_b`, `V_a/V_b`,
> and `V(b,a,z')-V(b,a,z)`, and thereby resolve the asymptotic consumption ratio `c/b`
> and the sign of total-wealth drift `mu_W`?

The central candidate from DLH-5N is the CRRA-2 scaling

```text
V_b ~ K(a,z)/b^2,   V ~ V_inf(a,z) - K(a,z)/b,   c ~ b/sqrt(K),
```

but this is a **candidate dominant balance, not accepted authority**. DLH-5O derives,
rejects, or leaves it conditional from the accepted HJB structure.

---

## 2. Result of the analysis (executive summary)

1. **Phase A (authority):** the accepted source is a MATLAB-faithful **finite-grid**
   HJB solver on `[b_lo,b_max] x [0,a_max] x {z}`. Its converged fixed point yields a
   continuous interior HJB identity
   `rho*V = u + mu_b*V_b + mu_a*V_a + Σ_z' λ(V(z')-V(z))` (a **derivable interior
   identity**, subject to the upwind finite-difference semantics), but it specifies
   **no unbounded-`b` asymptotic boundary / transversality condition**. The `b_max`
   marginal-utility boundary closure is **finite-grid numerical semantics only** and
   must not be promoted to an infinite-domain condition.
2. **Phase B (dominant balances):** within the source-faithful interior balance with
   the accepted FOCs, the pure power-law families are classified:
   - `p < 2` (including `p = 1` / logarithmic): **asymptotically inconsistent** (the
     value-flow terms cannot balance; the switch-spectrum argument forces the trivial
     solution).
   - `p > 2`: **asymptotically inconsistent** (flow utility `-1/c` cannot be balanced).
   - `p = 2`: the unique self-consistent pure-power balance, **conditional** on the
     ansatz and analytic assumptions; requires `V_inf` a-independent (hence `V_inf = 0`),
     `K` a-independent and z-independent, and bounded transfer.
   - Transfer-dominated alternatives (`V_a/V_b ~ b^m`, `m > 0`): superlinear adjustment
     cost (`m > 1/2`) is **inconsistent**; sub-superlinear transfer regimes collapse
     into the analyzed power-law classes. A full classification of exotic regimes is
     **not analyzable from accepted authority** (requires an analytic-model gate).
3. **Phase C (p = 2 coefficient system):** under the ansatz `V ~ -K/b` (with the
   audited O(1) balance forcing `V_inf = 0`), the O(1/b) balance is

   ```text
   (rho + r_b)*K - 2*sqrt(K) = (S*K),
   ```

   which forces `K` constant across `z`, `K = 4/(rho+r_b)^2`, and the asymptotic
   consumption ratio

   ```text
   c/b = (rho + r_b)/2 = (0.02 + 0.015)/2 = 0.0175,
   ```

   derived from the audited balance (not imported from textbook knowledge), after all
   same-order terms (transfer, adjustment cost, labor, productivity switch) are
   retained and checked.
4. **Phase D (self-consistency):** within the candidate, `V_a/V_b = 0`, `q = -1`,
   `d = -0.45a` (bounded, `O(1)`), `chi = O(1)`, `labor = o(1)`, and the cross-`z`
   switch contribution vanishes at `O(1/b)` (because the coefficient system forces `K`
   z-constant). Any a-dependent `K` or a-dependent `V_inf` would make `V_a/V_b ~ O(b)`
   or `O(b^2)`, drive `d` and `chi` to grow, and invalidate the balance — so the
   bounded-transfer candidate is the self-consistent one.
5. **Phase E/F (sign and DLH-5N):** if the `p = 2` balance is the realized HJB tail,
   then `c/b = 0.0175 > r_b = 0.015`, so `mu_b ~ (r_b - c/b)b = -0.0025b < 0` and
   `mu_W < 0` for large `b` — a **fixed-`a` liquid-tail inward (mean-reverting)**
   resolution, conditional on the candidate. The unconditional/established version is
   **not** obtainable from the accepted finite-grid authority alone.
6. **Terminal: Outcome B**
   `DLH_5O_HJB_LIQUID_TAIL_DOMINANT_BALANCE_CONDITIONAL__MISSING_ANALYTIC_ASSUMPTIONS_IDENTIFIED`.

Detailed derivations are in:

- `DLH_5O_HJB_AUTHORITY_AUDIT.md` — Phase A.
- `DLH_5O_DOMINANT_BALANCE_FAMILIES.md` — Phase B.
- `DLH_5O_P2_COEFFICIENT_SYSTEM.md` — Phase C.
- `DLH_5O_TRANSFER_AND_Z_SWITCH_SELF_CONSISTENCY.md` — Phase D.
- `DLH_5O_THEOREM_STATUS_MATRIX.md` — Phase E.
- `DLH_5O_DOMAIN_VIABILITY_IMPLICATIONS.md` — Phase F.
- `DLH_5O_SCIENTIFIC_TERMINAL.md` — exact terminal.

---

## 3. The core derivation in one paragraph

On the interior (continuum limit of the accepted converged fixed point),
`rho*V = u + mu_b*V_b + mu_a*V_a + S*V` with `c = V_b^{-1/2}`, `u = -1/c - l^6/6`,
`l = (0.85z*V_b)^{1/5}`, `d = a*T(V_a/V_b-1)/chi_1`, `chi = 0.1|d|+d^2/max(a,a_bar)`.
For `V_b ~ K/b^2` (candidate), the value integrates to `V ~ V_inf - K/b`. An
a-dependent `V_inf` or a-dependent `K` makes `V_a/V_b` grow (`O(b^2)` or `O(b)`),
drives `d` and `chi` to grow, and breaks the balance; therefore the self-consistent
candidate has `V_inf` and `K` a-independent, `V_a = 0`, bounded transfer. The O(1)
balance then forces `V_inf = 0` (since `rho > 0` is not an eigenvalue of the
productivity-switch generator `S`), and the O(1/b) balance yields
`(rho+r_b)K - 2sqrt(K) = S*K`, forcing `K` z-constant and `c/b = (rho+r_b)/2 = 0.0175`.
Since `0.0175 > r_b = 0.015`, `mu_b ~ -0.0025b < 0` and `mu_W < 0` in the fixed-`a`
liquid tail. **All of this is conditional** on the analytic assumptions that the
accepted finite-grid source does not itself establish (continuum/regularity, the
ansatz, a tail boundary/transversality specification, uniformity, and uniqueness of
the balance).

---

## 4. Finite-grid vs continuous authority (the central distinction)

The accepted source authorizes:

- the exact drift/utility/FOC objects (`DIRECTLY_ACCEPTED_SOURCE_AUTHORITY`);
- the algebraic form of the converged fixed point `rho*V = u + A*V` and hence the
  interior HJB identity (`DERIVABLE_INTERIOR_IDENTITY`, subject to the upwind
  finite-difference semantics and regularity);
- the finite-grid boundary closures at `b_lo`/`b_max`/`a = 0`/`a_max`
  (`FINITE_GRID_NUMERICAL_SEMANTICS_ONLY`).

The accepted source does **NOT** authorize:

- an unbounded-`b` asymptotic boundary condition or transversality condition
  (`NOT_SPECIFIED_BY_ACCEPTED_AUTHORITY`);
- the tail scaling of the actual HJB solution (`NOT_SPECIFIED_BY_ACCEPTED_AUTHORITY`);
- convergence of the finite-difference solution to any continuum tail object
  (`REQUIRES_ADDITIONAL_ANALYTIC_ASSUMPTION`).

Consequently every result below is a **conditional dominant-balance derivation**, not
an unconditional theorem from accepted authority.

---

## 5. What is explicitly NOT claimed

- NOT claimed: the accepted source alone proves `p = 2` or `c/b = 0.0175` (Outcome A).
- NOT claimed: a HJB-consistent non-inward regime is established (Outcome D).
- NOT claimed: the coefficient `(rho+r_b)/2` is imported from textbook/representative-agent
  knowledge; it follows (conditionally) from the audited O(1/b) balance.
- NOT claimed: `a -> +infinity`, taper extrapolation, stationary/density/tail/
  aggregate statements, or any R/W/W1/W2/`W_max` implication.
- NOT claimed: `V_inf = 0`, `K` a- and z-independence, bounded transfer, or vanishing
  switch term are assumptions — they are **derived consequences** of the candidate
  balance (with the caveat that the candidate itself is conditional).

---

## 6. Recommended next gate (not created by Builder)

If ChatGPT/Owner accept the conditional candidate, the next gate is an
**analytic-model specification** (and, if authorized later, a regularity/verification
theory) that: (i) defines the unbounded-`b` HJB problem (asymptotic boundary /
transversality); (ii) states regularity and uniformity hypotheses; (iii) establishes
(or refutes) that the actual solution realizes the `p = 2` balance; (iv) rules out
exotic tail regimes. Only then could the conditional sign resolution become an
established fixed-`a` liquid-tail statement. Stationary KFE remains NOT AUTHORIZED
under Issue #27.

No implementation or domain choice is authorized by this Issue.
