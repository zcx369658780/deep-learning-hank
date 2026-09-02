# DLH-5P Phase C — Boundary and Endpoint Consistency (Rev 2)

**Issue #42 Phase C (Rev 2).** Audits whether the desired tail theorem can be uniform
over the finite `a` support `[0,10]`, examining `a=0`, `a=a_max=10`, and `b=b_lo=-2`,
and whether any theorem must be restricted to an interior compact `a` subset. Rev 2
separates the three cases the reviewer required (step 17): **full `[0,10]` uniform**,
**compact interior-`a`**, and **`a -> 0` bare-`a` endpoint behavior**, and retains
`max(a,a_bar)` explicitly in all critical-transfer coefficients near `a=0` (step 23).
No new upper-`a` economic law is created by convenience.

## C1. `a = 0` — bare-`a` transfer degeneracy

- Accepted transfer FOC `d = a*T(q)/chi_1` has the **bare-`a` factor**: at `a = 0`,
  `d = 0` for **any** transfer ratio `R = V_a/V_b`. The combined transfer Hamiltonian
  `V_b[d(R-1)-chi] = 0` at `a=0`, and `mu_a(0) = r_a_eff(0)*0 + 0 = 0`.
- Consequences:
  1. **`R` is vacuous at `a=0`**: no transfer-ratio premise (P-TR or `R=O(1)`) is
     needed or violated at `a=0`; but `a=0` also provides **no evidence** for it.
  2. The `a`-dependent transfer term that drives the `m=1/2` altered system (Phase E,
     `0.5 a L^2 K/chi_1`) **vanishes at `a=0`**. At `a=0` the balance reduces to the
     P-TR form `(rho+r_b)K - 2 sqrt(K) = S*K`. The `a=0` endpoint therefore does not
     host the critical branch; the interior-`a` family is the relevant one.
  3. **`max(a,a_bar)` is retained explicitly** in all transfer/cost coefficients near
     `a=0` (step 23): `chi ~ 0.5 a^2 L^2 b/(chi_1 max(a,a_bar))` and
     `d q - chi ~ a L^2 b/chi_1 [1 - 0.5 a/max(a,a_bar)]`, valid for `a in (0,a_max)`
     without taking a limit at `a=0`.
  4. The DLH-5N reviewer annotation (`5503274333`) is preserved: the transfer order
     results are used only in their sufficient direction; `a=0` is not used to infer a
     reverse biconditional.
- Classification: `INHERITED_FINITE_GRID_NUMERICAL_SEMANTICS_ONLY` for the corner
  behavior; the corner is trivial for the coefficient/sign theorem.

## C2. `a = a_max = 10` — finite support and taper authority

- `r_a_eff(10) = 0.03*(1-0.1*(10/10)^9) = 0.027 > 0`: the taper is a finite support
  endpoint with positive effective illiquid return (not an absorbing barrier).
- The finite-grid `at_upper_a` branch restricts `d < 0` (no transfer INTO `a` at the
  upper edge). This is **`INHERITED_FINITE_GRID_NUMERICAL_SEMANTICS_ONLY`** — it is a
  numerical state-constraint-like branch, NOT analytic authority.
- For the analytic extension, the upper-`a` endpoint law is
  **`NEW_ANALYTIC_MODEL_DEFINITION_REQUIRES_OWNER`** (e.g., a reflecting boundary with
  `d <= 0`, a state constraint, or an interior extension on `[0,a_max]` with the taper
  held fixed). It must NOT be invented by convenience.
- The tail theorem's coefficient/sign content is `a`-independent (Phase C4), so it is
  insensitive to the upper-`a` law choice — a desirable robustness/falsifiability
  property (any Owner-chosen endpoint law that preserves the interior balance and
  uniformity yields the same tail coefficient within the adopted class).

## C3. `b = b_lo = -2` — lower liquid bound: inherited economics vs analytic adoption (step 24)

- The **borrowing-rate gap is accepted economics** (Phase A A6): effective borrowing
  rate `0.025` for `b < 0` (used in boundary consumption and shadow rates; the drift
  formula uses `r_b*b` with the gap entering through the selected
  consumption/transfer). This is `INHERITED_ACCEPTED_ECONOMICS`.
- **Adopting `b_lo = -2` as the continuous analytic state-space lower bound is a
  SEPARATE step** (`NEW_ANALYTIC_MODEL_DEFINITION_REQUIRES_OWNER`, Phase A A9/A16): the
  grid chose `-2` (inherited `INHERITED_FINITE_GRID_NUMERICAL_SEMANTICS_ONLY`), but
  making it the analytic lower edge of the unbounded problem is new model authority.
  The inherited borrowing-gap economics does not by itself authorize the analytic
  adoption of the bound.
- For the analytic problem on `(b_lo,+inf)`, the lower-boundary law is
  `NEW_ANALYTIC_MODEL_DEFINITION_REQUIRES_OWNER` (or, minimally, `V` bounded at `b_lo`
  with a fixed data law). It matters for well-posedness/comparison, not for the
  `b -> +inf` tail.
- **Robustness gate:** the tail theorem should be **independent** of the exact `b_lo`
  law (asymptotic separation). If the coefficient depended on the `b_lo` law, that
  would be a falsification signal for the analytic specification.

## C4. Full `[0,10]` uniform vs compact interior-`a` vs `a -> 0` (step 17)

The DLH-5O `p=2` coefficient system (Phase C of DLH-5O) is **`a`-independent**:
`V_inf = 0`, `K` z-constant `= 4/(rho+r_b)^2`, `c/b = (rho+r_b)/2`, `mu_W/b ->
(r_b - c/b) = -0.0025`. The `a`-dependent parts of the balance (transfer/adjustment
cost, `mu_a`) are `O(1)` or `O(1/b^2)` under P-TR/`R=O(1)` and do not enter the
`O(1/b)` coefficient equation. Three separate statements:

1. **Compact interior-`a` theorem (robust):** the P-TR `p=2` result holds on `(0,a_max)`
   (or any compact `[a_min, a_max - eps]`, `a_min > 0`), requiring only the interior
   HJB, the adopted P-TR class, and regularity. This is also the domain on which the
   `m=1/2` alternative family (Phase E, `L ~ a^{-1/2}`) is **admissible** — so on the
   interior the P-TR coefficient is NOT unique without the adopted primitive.
2. **Full `[0,10]` uniform theorem (requires endpoints):** holds with explicit endpoint
   conventions: `a=0` is a trivial corner (no transfer, no illiquid drift; the result
   is trivially valid there), and `a_max=10` uses the Owner-chosen upper-`a` law (C2).
   For the `m=1/2` family, full-`[0,10]` uniform smooth realizations are **not
   established** (the `L ~ a^{-1/2}` form is singular at `a=0`, `M ~ sqrt(a)` is not
   `C^1` at `a=0`). This does NOT imply the branch is globally impossible, because the
   specification itself allows an interior-`a` theorem.
3. **`a -> 0` bare-`a` endpoint:** governed by the bare-`a` degeneracy (C1): `d=0`,
   `R` vacuous, `mu_a=0`, transfer term vanishes; the balance at `a=0` is the P-TR form.
   The critical branch's interior family does not extend smoothly to `a=0`.

Recommendation: state the full-`[0,10]` uniform P-TR theorem with explicit endpoint
conventions; require the `a_max` law from the Owner; and report the `m=1/2` family as
an interior-admissible alternative whose full-support smooth realization is not
established.

## C5. Compatibility of admissibility/transversality with endpoints

- The S2 verification/selection condition (`e^{-rho T} E[V] -> 0`) and S3
  derivative-control class (`R = o(sqrt(b))` or `O(1)`) are tail laws; they do not
  conflict with the `a=0` corner (vacuous there) or `a_max` (which only constrains `d`
  sign in the finite grid, replaced by an Owner law). The `m=1/2` family can satisfy
  the S2 condition for suitable admissible paths (Phase E), so the endpoint laws do
  not by themselves exclude it.

## C6. Conclusion (Rev 2)

The P-TR `p=2` theorem can be stated uniformly on the full `[0,10]` support provided
(i) the interior HJB holds on `(0,a_max)`, (ii) the `a_max` upper-`a` endpoint law is
chosen by the Owner (new model definition), (iii) the `a=0` corner is treated as
trivial (bare-`a`), and (iv) rates are uniform **and the P-TR primitive is adopted**.
The `m=1/2` family is an interior-admissible alternative (full-`[0,10]` uniform smooth
realization not established; `a=0` bare-`a`), so coefficient uniqueness requires the
adopted primitive, not the balance. `max(a,a_bar)` is retained explicitly near `a=0`.
No new upper-`a` economic law is created.
