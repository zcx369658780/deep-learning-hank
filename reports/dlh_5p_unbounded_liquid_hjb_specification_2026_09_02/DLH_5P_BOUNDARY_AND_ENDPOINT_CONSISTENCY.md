# DLH-5P Phase C — Boundary and Endpoint Consistency

**Issue #42 Phase C.** Audits whether the desired tail theorem can be uniform over the
finite `a` support `[0,10]`, examining `a=0`, `a=a_max=10`, and `b=b_lo=-2`, and
whether any theorem must be restricted to an interior compact `a` subset. No new
upper-`a` economic law is created by convenience.

## C1. `a = 0` — bare-`a` transfer degeneracy

- Accepted transfer FOC `d = a*T(q)/chi_1` has the **bare-`a` factor**: at `a = 0`,
  `d = 0` for **any** transfer ratio `R = V_a/V_b`. The combined transfer Hamiltonian
  `V_b[d(R-1)-chi] = 0` at `a=0`, and `mu_a(0) = r_a_eff(0)*0 + 0 = 0`.
- Consequences:
  1. **`R` is vacuous at `a=0`**: no transfer-ratio premise (P-TR or `R=O(1)`) is
     needed or violated at `a=0`; but `a=0` also provides **no evidence** for it.
  2. The **`a`-dependent transfer term** that drives the `m=1/2` ruling-out (Phase E,
     `0.5*a*L^2*K/chi_1`) vanishes at `a=0`; the branch is still excluded at `a=0` by
     the switch-spectrum equation `(rho - r_b/2)K = S*K` (no transfer terms at all),
     and on `(0,10]` by the `a`-dependence. So the ruling-out holds on the full `[0,10]`.
  3. The DLH-5N reviewer annotation (`5503274333`) is preserved: the transfer order
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
  uniformity yields the same tail coefficient).

## C3. `b = b_lo = -2` — lower liquid bound and borrowing-rate gap

- The borrowing-rate gap is accepted economics (Phase A A6): effective borrowing rate
  `0.025` for `b < 0` (used in boundary consumption and shadow rates; the drift formula
  uses `r_b*b` with the gap entering through the selected consumption/transfer).
- `b_lo = -2` is the accepted grid lower edge; its marginal-utility closure is
  `INHERITED_FINITE_GRID_NUMERICAL_SEMANTICS_ONLY`.
- For the analytic problem on `(b_lo,+inf)`, the lower-boundary law is
  `NEW_ANALYTIC_MODEL_DEFINITION_REQUIRES_OWNER` (or, minimally, `V` bounded at `b_lo`
  with a fixed data law). It matters for well-posedness/comparison, not for the
  `b -> +inf` tail.
- **Robustness gate:** the tail theorem should be **independent** of the exact `b_lo`
  law (asymptotic separation). If the coefficient depended on the `b_lo` law, that
  would be a falsification signal for the analytic specification.

## C4. Full `[0,10]` uniform theorem vs interior-`a` theorem

- The DLH-5O `p=2` coefficient system (Phase C of DLH-5O) is **`a`-independent**:
  `V_inf = 0`, `K` z-constant `= 4/(rho+r_b)^2`, `c/b = (rho+r_b)/2`, `mu_W/b ->
  (r_b - c/b) = -0.0025`. The `a`-dependent parts of the balance (transfer/adjustment
  cost, `mu_a`) are `O(1)` or `O(1/b^2)` under P-TR/`R=O(1)` and do not enter the
  `O(1/b)` coefficient equation.
- Therefore the coefficient and sign results are uniform over `a in [0,10]` **once the
  endpoint laws are pinned by the chosen candidate** and the rates are uniform. Two
  defensible statements:
  1. **Interior-`a` theorem (robust):** the theorem holds on `(0,a_max)` (or any
     compact `[a_min, a_max - eps]`), requiring only the interior HJB and regularity.
  2. **Full-`[0,10]` theorem (requires endpoints):** the theorem holds on `[0,10]`
     with explicit endpoint conventions: `a=0` is a trivial corner (no transfer, no
     illiquid drift; the result is trivially valid there), and `a_max=10` uses the
     Owner-chosen upper-`a` law (C2), which does not alter the `a`-independent tail
     coefficient.
- Recommendation: state the full-`[0,10]` uniform theorem with explicit endpoint
  conventions, and require the `a_max` law from the Owner; until then the theorem is
  clean on `(0,a_max)`.

## C5. Compatibility of admissibility/transversality with endpoints

- The S2 transversality (`e^{-rho T} E[V] -> 0`) and S3 derivative-control class
  (`R = o(sqrt(b))` or `O(1)`) are tail laws; they do not conflict with the `a=0`
  corner (vacuous there) or `a_max` (which only constrains `d` sign in the finite grid,
  replaced by an Owner law). No endpoint requires a modification of the admissibility
  law.

## C6. Conclusion

The desired tail theorem can be stated uniformly on the full `[0,10]` support provided
(i) the interior HJB holds on `(0,a_max)`, (ii) the `a_max` upper-`a` endpoint law is
chosen by the Owner (new model definition), (iii) the `a=0` corner is treated as
trivial (bare-`a`), and (iv) rates are uniform. A robust interior-`a` theorem on
`(0,a_max)` holds unconditionally given the interior assumptions. No new upper-`a`
economic law is created by this analysis.
