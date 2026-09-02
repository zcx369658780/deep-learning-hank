# DLH-5O / Issue #41 — Fixed-`a` Liquid-Tail HJB Value-Function Asymptotics

**Task type:** `SCIENTIFIC_THEORY_ANALYSIS__HJB_VALUE_FUNCTION_LIQUID_TAIL_SCALING`
**Date:** 2026-09-02 (rev 2)
**Branch:** `dsh/issue-41-dlh-5o-hjb-value-tail-asymptotics-2026-09-02`
**Fresh `origin/main` baseline:** `1646d9c3636b87372eaa28425360d022ff510eab`
**Previous candidate:** `348e0b00f56e32655a85fabdaa74514af0ae718b`
**Fresh ChatGPT review (rev 1):** `5504354859` — blocked pending bounded revision.

This is a **theory/documentation gate only**. No source mutation, no HJB/KFE/grid run,
no stationary operation, no domain choice, no imported textbook tail condition.

DLH-5O asks whether the **accepted HJB authority** (the MATLAB-faithful finite-grid
household solver, immutable) is sufficient to derive the large-positive-`b` scaling of
the value function and its derivatives — `V_b`, `V_a/V_b`, and the cross-productivity
difference `V(b,a,z') - V(b,a,z)` — and thereby resolve the asymptotic consumption
ratio `c/b` and the sign of `mu_W` on the fixed illiquid support `0 <= a <= a_max = 10`.

---

## 0. Controlling accepted authority

- Issue #40 / DLH-5N **accepted** and closed. Accepted candidate
  `bded30a8b8cb579c3f359a62f5b530d7c34b7526`; reviewer acceptance
  `5503274333`; integration commit `e23b1ada5f5ab1b11c1291d8141d8286884553d4`.
- Accepted DLH-5N terminal:
  `DLH_5N_FIXED_A_LIQUID_TAIL_TOTAL_WEALTH_SIGN_CONDITIONAL__MISSING_CONTROL_ASYMPTOTICS_IDENTIFIED`.
- Accepted household source (immutable, read-only):
  `src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`
  (blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`).
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

## 2. Result of the analysis (executive summary, rev 2)

1. **Phase A (authority):** the accepted source is a MATLAB-faithful **finite-grid**
   HJB solver on `[b_lo,b_max] x [0,a_max] x {z}`. Its converged fixed point yields a
   continuous interior HJB identity `rho*V = u + mu_b*V_b + mu_a*V_a + S*V` (a
   **derivable interior identity**, subject to the upwind finite-difference semantics
   and smooth-continuum regularity), but it specifies **no unbounded-`b` asymptotic
   boundary / transversality condition**. The `b_max` marginal-utility boundary closure
   is **finite-grid numerical semantics only** and must not be promoted to an
   infinite-domain condition.
2. **Transfer Hamiltonian (rev 2).** The transfer-dependent part of the HJB is the
   **combined** object
   `d*V_a + (-d-chi)*V_b = V_b*[ d*(V_a/V_b - 1) - chi(d,a) ]`.
   It must be analyzed as one object; `d*V_a` is generally the **same order** as
   `-d*V_b - chi*V_b`. Under the `p=2` ansatz with `R = V_a/V_b`:
   `V_b*[d(R-1)-chi] ~ O(b^{2m-2})` when `R ~ b^m`, so it is subleading iff `m < 1/2`,
   same-order at `m = 1/2`, and dominant (inconsistent) for `m > 1/2`.
3. **Leading a-independence is not `V_a = 0` (rev 2).** From the leading expansion
   `V ~ V_inf - K/b` one may conclude the **leading coefficients** are a-independent
   (`d_av V_inf = 0`, `d_aa K = 0`) — this is necessary for `R = O(1)` — but one may
   **not** conclude `V_a = 0` or `R = 0`: a subleading term `H(a,z)/b^2` gives
   `V_a ~ H_a/b^2` and `R -> H_a/K = O(1)`, nonzero. Consequently the exact transfer
   values `q=-1`, `d=-0.45a`, `chi=0.2475a` are **not** derived from the leading ansatz;
   they are a special case that requires the additional assumption `R -> 0` (separately
   imposed, not derived).
4. **Phase B (dominant balances, narrowed):** within the transfer class
   `R = o(sqrt(b))` uniformly (so `d = o(sqrt(b))`, `chi = o(b)`, combined term
   subleading), the pure power-law families `p<2` and `p>2` are **asymptotically
   inconsistent**; the `p=2` bounded/sub-root-transfer balance is **self-consistent**
   (conditional). Outside that transfer class (e.g. `R ~ Theta(sqrt(b))`, `m=1/2`) the
   combined term is **same-order**, the coefficient system changes, and the family is
   **left unresolved** — it is neither accepted nor ruled out.
5. **Phase C (p=2 coefficient system, corrected):** under the explicit derivative-
   control premise `R = V_a/V_b = o(sqrt(b))` uniformly (preferably `O(1)`), the
   combined transfer term is subleading, the O(1) balance forces `V_inf = 0`, and the
   O(1/b) balance is `(rho+r_b)K - 2sqrt(K) = S*K`, forcing `K` z-constant,
   `K = 4/(rho+r_b)^2`, and `c/b = (rho+r_b)/2 = 0.0175` — derived from the audited
   balance (not imported), **conditional on the corrected assumption set**.
6. **Phase D (self-consistency, corrected):** with `R = O(1)` uniformly, `d = O(1)`
   and `chi = O(1)` (order statements only), `labor = o(1)`; the cross-`z` switch term
   is `O(1/b)` and vanishes (K z-constant). The a-dependent-`V_inf` and a-dependent-`K`
   inconsistency is established from the **combined** transfer Hamiltonian, not from
   `chi` in isolation; the exact `d`, `chi`, `mu_a` values are order statements unless
   `R -> 0` is additionally imposed.
7. **Phase E/F (sign and DLH-5N):** if the `p = 2` balance is the realized HJB tail
   under the corrected transfer-ratio premise, then `c/b = 0.0175 > r_b = 0.015`, so
   `mu_b ~ (r_b - c/b)b = -0.0025b < 0` and `mu_W < 0` for large `b` — a **fixed-`a`
   liquid-tail inward (mean-reverting)** resolution, **conditional** on the candidate
   and the derivative-control assumption. The unconditional/established version is
   **not** obtainable from the accepted finite-grid authority alone.
8. **Terminal: Outcome B** (preserved)
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

## 3. The core derivation in one paragraph (rev 2)

On the interior (continuum limit of the accepted converged fixed point),
`rho*V = u + mu_b*V_b + mu_a*V_a + S*V` with `c = V_b^{-1/2}`, `u = -1/c - l^6/6`,
`l = (0.85z*V_b)^{1/5}`, `d = a*T(R-1)/chi_1`, `R = V_a/V_b`,
`chi = 0.1|d|+d^2/max(a,a_bar)`. Grouping the transfer/adjustment terms as the single
Hamiltonian `V_b*[d*(R-1)-chi]` (the accepted transfer FOC maximizes exactly this
object, up to the bare-`a`/cost-floor caveat), we see: under the explicit
derivative-control premise `R = o(sqrt(b))` uniformly (preferably `R = O(1)`), `d =
o(sqrt(b))`, `chi = o(b)`, and the combined transfer term is subleading. The O(1)
balance then forces `V_inf = 0` (since `rho > 0` is not an eigenvalue of the
productivity-switch generator `S`), and the O(1/b) balance yields
`(rho+r_b)K - 2sqrt(K) = S*K`, forcing `K` z-constant and `c/b = (rho+r_b)/2 = 0.0175`.
Since `0.0175 > r_b = 0.015`, `mu_b ~ -0.0025b < 0` and `mu_W < 0` in the fixed-`a`
liquid tail. **All of this is conditional** on the analytic assumptions that the
accepted finite-grid source does not itself establish (smooth-continuum regularity,
the ansatz, the transfer-ratio/derivative-control condition, a tail
boundary/transversality specification, uniformity, and uniqueness of the balance).
The `m = 1/2` transfer regime (`R ~ Theta(sqrt(b))`) is **not resolved** — there the
combined term is same-order and the coefficient equation is altered.

---

## 4. Finite-grid vs continuous authority (the central distinction)

The accepted source authorizes:

- the exact drift/utility/FOC objects (`DIRECTLY_ACCEPTED_SOURCE_AUTHORITY`);
- the algebraic form of the converged fixed point `rho*V = u + A*V` and hence the
  interior HJB identity, including the combined transfer Hamiltonian
  `V_b*[d*(R-1)-chi]` (`DERIVABLE_INTERIOR_IDENTITY`, subject to the upwind
  finite-difference semantics and smooth-continuum regularity);
- the finite-grid boundary closures at `b_lo`/`b_max`/`a = 0`/`a_max`
  (`FINITE_GRID_NUMERICAL_SEMANTICS_ONLY`).

The accepted source does **NOT** authorize:

- an unbounded-`b` asymptotic boundary condition or transversality condition
  (`NOT_SPECIFIED_BY_ACCEPTED_AUTHORITY`);
- the tail scaling of the actual HJB solution (`NOT_SPECIFIED_BY_ACCEPTED_AUTHORITY`);
- convergence of the finite-difference solution to any continuum tail object
  (`REQUIRES_ADDITIONAL_ANALYTIC_ASSUMPTION`);
- the derivative of the `o(1/b)` remainder of the value expansion — i.e., the
  transfer ratio `R = V_a/V_b` — (`NOT_SPECIFIED_BY_ACCEPTED_AUTHORITY`; it must be
  imposed as an explicit derivative-control premise).

Consequently every result below is a **conditional dominant-balance derivation**, not
an unconditional theorem from accepted authority.

---

## 5. What is explicitly NOT claimed (rev 2)

- NOT claimed: the accepted source alone proves `p = 2` or `c/b = 0.0175` (Outcome A).
- NOT claimed: a HJB-consistent non-inward regime is established (Outcome D).
- NOT claimed: `K_a = 0` implies `V_a = 0` or `V_a/V_b = 0`; the leading a-independence
  of the first two coefficients does not control the a-derivative of the remainder.
- NOT claimed: the exact transfer `q=-1`, `d=-0.45a`, `chi=0.2475a` follows from the
  leading ansatz; these are a special case under the additional (unproved) assumption
  `R -> 0` (equivalently `V_a/V_b -> 0`).
- NOT claimed: `p < 2`/`p > 2` families are inconsistent for **all** transfer regimes;
  they are inconsistent only within the transfer class `R = o(sqrt(b))` uniformly. The
  critical `m = 1/2` family (`R ~ Theta(sqrt(b))`) is left **unresolved**.
- NOT claimed: the coefficient `(rho+r_b)/2` is imported from textbook/representative-
  agent knowledge; it follows (conditionally, under the corrected assumption set) from
  the audited O(1/b) balance.
- NOT claimed: `a -> +infinity`, taper extrapolation, stationary/density/tail/
  aggregate statements, or any R/W/W1/W2/`W_max` implication.
- NOT claimed: `V_inf = 0`, `K` a- and z-independence are assumptions — they are
  **derived consequences** of the candidate balance under the explicit transfer-ratio
  premise (with the caveat that the candidate itself is conditional).

---

## 6. Recommended next gate (not created by Builder)

If ChatGPT/Owner accept the conditional candidate, the next gate is an
**analytic-model specification** (and, if authorized later, a regularity/verification
theory) that: (i) defines the unbounded-`b` HJB problem (asymptotic boundary /
transversality); (ii) states smooth-continuum regularity and uniformity hypotheses;
(iii) proves or imposes the derivative-control / transfer-ratio condition
(`V_a/V_b = o(sqrt(b))` uniformly, or the stronger `V_a/V_b = O(1)`); (iv) establishes
(or refutes) that the actual solution realizes the `p = 2` balance and resolves or
rules out the `m = 1/2` family; (v) only then elevates the conditional sign resolution
to an established fixed-`a` liquid-tail statement. Stationary KFE remains NOT
AUTHORIZED under Issue #27.

No implementation or domain choice is authorized by this Issue.
