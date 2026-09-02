# DLH-5Q / Issue #43 — Provisional S3 Liquid-Tail Theorem Verification and Parallel Falsification (Rev 3)

**Task type:** `SCIENTIFIC_THEOREM_VERIFICATION__PROVISIONAL_S3_LIQUID_TAIL_AND_PARALLEL_FALSIFICATION`
**Date:** 2026-09-02
**Branch:** `dsh/issue-43-dlh-5q-provisional-s3-theorem-falsification-2026-09-02`
**Fresh `origin/main` baseline:** `578263e37c28992b5eed7c11c9d803415e81d688`
**Authoritative activation comment (Issue #43):** `5506167630`
**Owner decision:** `PROVISIONAL_S3_ANALYTIC_CLASS__PARALLEL_FALSIFICATION_ROUTE_APPROVED`
**Owner-decision comment (Issue #42):** `5506138177`
**Review comments (Issue #43):** `5506978886` (Rev 2 corrections), `5507222546` (Rev 3 corrections) — bounded same-Issue revisions.

This is a **theorem-verification + falsification-design gate only**. It does NOT freeze
or implement any analytic specification, does NOT select R/W/W1/W2/`W_max`, does NOT
choose a numerical `b_max`/`a_max`, does NOT run any HJB/KFE/grid/stationary
experiment, and does NOT create production domain or endpoint authority. Builder
completion is not theorem acceptance; provisional S3 is falsifiable working authority,
not a final economic theorem. Stationary KFE remains NOT AUTHORIZED under Issue #27.

---

## 1. Controlling accepted authority

- Issue #42 / DLH-5P **accepted and CLOSED**. Accepted candidate
  `faa9fd27dec941de72888d2c8db7db6f5393e0f6`; reviewer acceptance `5505979616`;
  acceptance integration `156d8d092839668b18ab52a6a9d0e12023f248bd`; accepted
  terminal
  `DLH_5P_CRITICAL_TRANSFER_BRANCH_REMAINS_ADMISSIBLE__TAIL_SPECIFICATION_NOT_UNIQUE__OWNER_DECISION_REQUIRED`.
- Owner decision after DLH-5P (Issue #42 comment `5506138177`):
  `PROVISIONAL_S3_ANALYTIC_CLASS__PARALLEL_FALSIFICATION_ROUTE_APPROVED`.
- Accepted household source (immutable, read-only):
  `src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`
  (blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`).
- Accepted DLH-5O package (read-only):
  `docs/theory/DLH_5O_HJB_VALUE_FUNCTION_LIQUID_TAIL_ASYMPTOTICS.md` +
  `reports/dlh_5o_hjb_value_function_tail_asymptotics_2026_09_02/`.
- Accepted DLH-5P package (read-only):
  `docs/design/DLH_5P_UNBOUNDED_LIQUID_HJB_ANALYTIC_SPECIFICATION_REVIEW.md` +
  `reports/dlh_5p_unbounded_liquid_hjb_specification_2026_09_02/`.
- Frozen D0 configuration (read-only): `configs/dlh_5b_two_region_symmetric_anchor.toml`
  (region 0), `configs/dlh_5l_total_wealth_domain_geometry_diagnostic.toml`.
- Issue #27 HJB<->KFE same-controlled-process contract remains binding; stationary KFE
  remains NOT AUTHORIZED.
- R and W remain unfrozen; no `W_max`; no new `b_max`/`a_max`; the accepted taper is
  not extrapolated beyond `a_max = 10`.

---

## 2. Provisional working analytic authority (this task only)

Per the activation comment `5506167630` and the Owner decision `5506138177`, DLH-5Q
provisionally adopts:

1. **S1 base:** fixed finite illiquid support `a in [0,10]`, accepted z states, an
   unbounded-positive liquid tail, and the accepted continuous interior
   HJB/economics. Concretely: state space `(b_lo,+inf) x (0,a_max) x {z}` with the
   interior HJB identity below; class `V in C(D̄) cap C^1(D)`, `V_b > 0`, `V < 0`,
   continuity to finite `b_lo`, compact `a`, finite `z`. **Derived consequence:**
   V is monotone increasing in `b` and globally bounded, so
   `V_inf(a,z) = lim_{b->+inf} V(b,a,z) in [-C,0]` exists pointwise.
2. **S2 selection:** `V_inf(a,z) = 0`, adopted **provisionally** as a tail-value
   selection assumption. It is NOT a proved necessity and NOT a comparison/uniqueness
   theorem (Issue #42 acceptance item 6 controls). It is distinct from an asset
   no-Ponzi condition.
3. **S3 primary derivative-control class:** `R = V_a/V_b = O(1)` uniformly over the
   claimed `(a,z)` theorem support.
4. **P-TR sensitivity envelope:** `R = o(sqrt(b))` is retained only as a weaker
   sensitivity class, NOT co-equal primary theorem authority.
5. The critical `R ~ Theta(sqrt(b))` family remains **outside** provisional S3 and is
   preserved as an explicit falsification / exclusion-cost benchmark; it is NOT
   declared economically impossible.

The interior HJB identity (accepted source, combined form) is

```text
rho*V = u + (r_b*b + labor - c)*V_b + r_a_eff(a)*a*V_a + V_b*[d*(R-1) - chi] + S*V,
R = V_a/V_b,
```

with the accepted objects (read-only): `u = c^(1-gamma_c)/(1-gamma_c) -
sum_z w_z l_z^(1+phi)/(1+phi)` (gamma_c=2, phi=5), `c = V_b^(-1/2)`,
`l = (V_b * 0.85 z / w)^(1/5)`, `d = a*T(R-1)/chi_1`,
`T(q) = min(q+chi_0,0) + max(q-chi_0,0)`,
`chi = chi_0|d| + 0.5*chi_1*d^2/max(a,a_bar)`,
`r_a_eff(a) = r_a*(1 - 0.1*(a/a_max)^9)`, `r_b_eff = r_b + gap*1_{b<0}`,
`mu_b = r_b*b + labor - d - chi - c`, `mu_a = r_a_eff(a)*a + d`.

Numeric anchors (frozen): `rho=0.02`, `r_b=0.015` (0.025 for `b<0`), `r_a=0.03`,
`chi_0=0.1`, `chi_1=2.0`, `a_bar=1e-6`, `a_max=10`, `b_lo=-2`, `z in {0.8,1.3}`,
switch rate `1/3` (spectrum `{0,-2/3}`).

---

## 3. Executive summary of the DLH-5Q analysis

1. **Phase A — provisional-class freeze.** The provisional class separates inherited
   economics (S1 base) from Owner-adopted provisional assumptions (S2 `V_inf=0`, S3
   `R=O(1)`) from theorem assumptions still to prove (existence, comparison,
   asymptotic realization, remainder control, coefficient convergence, uniformity)
   from unresolved endpoint authority (`a=10` upper law, `b_lo` lower-law adoption,
   `a=0` bare-`a` corner conventions). Full `[0,10]` theorem authority is NOT present.
   See `DLH_5Q_PROVISIONAL_AUTHORITY_FREEZE.md`.
2. **Phase B — existence/comparison.** Existence of an admissible continuous value
   solution of the **continuous unbounded-`b`** problem is NOT established from current
   authority alone: the accepted source is a finite-grid solver; a comparison/
   uniqueness framework on `(b_lo,+inf) x (0,a_max) x {z}` (e.g., viscosity solutions
   with an unbounded-domain comparison theorem), the `a=10` endpoint law, the `b_lo`
   law, and a tail boundary specification are exactly the missing ingredients. `V_inf=0`
   is a level/boundary selection, not a uniqueness theorem. The exact missing
   assumptions are enumerated. See `DLH_5Q_EXISTENCE_COMPARISON_AUDIT.md`.
3. **Phase C — asymptotic realization.** Within S3, across the **correctly analyzed
   families**, `p=2` is the unique self-consistent formal balance. For
   `1 < p < 2`, `p-1 < p/2`, so the rho/r_b/S block at `b^(-(p-1))` **dominates**; the
   leading equation `[rho + (p-1) r_b] K = S*K` has no nonzero `K` because
   `rho + (p-1) r_b > 0` is not in the frozen switch spectrum `{0,-2/3}` (switch-
   spectrum exclusion). For `p > 2`, `p/2 < p-1`, so the consumption block
   `u - c V_b = -2 sqrt(V_b) ~ -2 sqrt(K)/b^(p/2)` dominates and is unbalanced. The
   `p=1` log tail is excluded by S1 boundedness; explicitly tested slow families
   (`C = b^(-alpha)` via the switch-spectrum equation `(rho + r_b alpha) C = S*C`, no
   positive `alpha`; `C = 1/log b` via the unmatched `rho*V` term (z-constant amplitude) or via the switch-spectrum equation `S A = rho A` (z-dependent amplitude `A(z)`; `rho=0.02 notin {0,-2/3}`))`) are excluded by
   corrected order accounting. **Broader non-power/exotic S3 tails are NOT claimed
   excluded** — including monotone-preserving oscillatory remainders (small oscillations around a monotone leading tail may keep `V_b>0`) — they remain part of the open `ASYMPTOTIC_REALIZATION / NO-EXOTIC-REGIME`
   gate. Under `R=O(1)` the combined transfer Hamiltonian `V_b[d(R-1)-chi]` is
   `O(1/b^2)` (subleading). **This is a formal dominant-balance statement, NOT an actual
   asymptotic theorem:** realization of the `p=2` tail by the actual HJB solution
   requires existence + comparison + the explicit derivative-remainder contract (E) +
   no exotic competing regime, none of which is established. See
   `DLH_5Q_ASYMPTOTIC_REALIZATION_ANALYSIS.md`.
4. **Phase D — coefficient/drift.** Conditional on the `p=2` balance being realized
   with the derivative-remainder contract (E), the O(1/b) balance gives
   `(rho+r_b)K - 2 sqrt(K) = S*K` with `K = 4/(rho+r_b)^2` (z-constant),
   `c/b -> 0.0175`, `mu_W/b -> -0.0025 < 0`. Same-order audit: z-switching (`S*V` at
   O(1/b), `S*K=0` for z-constant K), labor (`o(1)`), transfer and adjustment cost
   (`O(1/b^2)` under `R=O(1)`), fixed-`a` illiquid return (`O(1/b^2)`). These are
   **conditional**, not theorem-level. See
   `DLH_5Q_P2_COEFFICIENT_AND_DRIFT_AUDIT.md`.
5. **Phase E — parallel falsification search (analytic only).** No in-class S3
   counterexample was found **among the correctly analyzed families**: no `p != 2`
   power tail (power `1<p<2` via the switch-spectrum argument, `p>2` via the unbalanced
   consumption block), no log tail (S1 boundedness), no explicitly tested slow tail
   (`C = b^(-alpha)`, `C = 1/log b`), no S3-internal remainder construction that changes
   the `O(1/b)` coefficient, no first-order z-deformation of K (the required spectral
   value `(rho+r_b)/2 = 0.0175` is not in `{0,-2/3}`), and no `mu_W/b >= 0` branch
   (**conditional on the realized `p=2` balance**: would need `c/b <= r_b`, i.e.
   `K >= 1/r_b^2`, outside the S3 balance). These are formal exclusions of the analyzed
   families, not theorems and **not an exhaustive exclusion** of every non-power/exotic
   S3 tail. The critical `m=1/2` family is preserved outside S3 as the exclusion-cost
   benchmark. See `DLH_5Q_ANALYTIC_FALSIFICATION_SEARCH.md`.
6. **Phase F — endpoint scope.** Only a compact-interior-`a` theorem statement is
   currently supported (and even that only conditional on Phase B/C gaps being
   closed). Full `[0,10]` authority requires an Owner-adopted `a=10` upper-`a` law and
   an Owner decision on the `b_lo` lower-bound adoption; `a=0` is the bare-`a` corner
   (vacuous R, `d=0`). No analytic `a=10` law is invented. See
   `DLH_5Q_ENDPOINT_SCOPE_AUDIT.md`.
7. **Phase G — matrix and terminal.** The theorem/falsification matrix and the exact
   terminal are in `DLH_5Q_THEOREM_FALSIFICATION_MATRIX_AND_TERMINAL.md`. **Terminal
   (exactly one):**

```text
DLH_5Q_PROVISIONAL_S3_THEOREM_NOT_CLOSED__MISSING_EXISTENCE_COMPARISON_OR_ASYMPTOTIC_REALIZATION_IDENTIFIED__FALSIFICATION_PROTOCOL_READY
```

The provisional S3 class is internally consistent across the correctly analyzed
families (no counterexample found among them), and the `p=2` balance survives as the
unique self-consistent formal branch among those families, but the theorem is NOT
closed because existence, comparison, and asymptotic realization are not established
from current authority, and broader non-power/exotic S3 tails remain part of the open
`ASYMPTOTIC_REALIZATION / NO-EXOTIC-REGIME` gate. The future numerical falsification
protocol is designed but NOT executed
(`DLH_5Q_NUMERICAL_FALSIFICATION_PROTOCOL.md`).

---

## 3b. Rev 2 corrections (reviewer `5506978886`)

1. **`1 < p < 2` dominant order corrected:** for `1<p<2`, `p-1 < p/2`, so the
   rho/r_b/S block at `b^(-(p-1))` dominates (Rev 1's "consumption dominates for
   `p<2`" had the inequality reversed). The leading equation
   `[rho + (p-1) r_b] K = S*K` has no nonzero `K` for the frozen switch spectrum
   `{0,-2/3}` — switch-spectrum exclusion.
2. **`p > 2` preserved separately:** `p/2 < p-1`, consumption block dominant and
   unbalanced.
3. **Slow-tail order/sign corrected:** the z-constant balance `-rho*C = r_b*b*(-C')`
   for `C = b^(-alpha)` gives `-rho = r_b alpha` (no positive `alpha`); z-dependent
   amplitudes give the switch-spectrum equation `(rho + r_b alpha) C = S*C`; the
   example `C = 1/log b` has `rho*C = O(1/log b)` dominant (not the consumption term).
   Rev 1's `alpha = rho/r_b = 4/3` was a sign error and is withdrawn.
4. **No general non-power exclusion claim:** only the power families and the explicitly
   tested log/slow families are excluded; broader non-power/exotic classes remain part
   of the open `ASYMPTOTIC_REALIZATION / NO-EXOTIC-REGIME` gate (step 18).
5. **Derivative-remainder contract (E):** the degenerate `|b^2(V_a - R V_b)|` term
   (identically zero) is removed; replaced by the explicit uniform expansion
   `V = -K/b + H/b^2 + r0`, `V_b = K/b^2 - 2H/b^3 + r_b`, `V_a = H_a/b^2 + r_a` with
   uniform small-o bounds, giving `R -> H_a/K = O(1)`. The incoherent
   `M_a = O(K b^(-1/2))` statement is removed; a nonzero b-independent `M_a` in a
   `b^(-3/2)` term would force `R ~ sqrt(b)` (outside S3), so S3 requires that
   coefficient's `a`-derivative to vanish at that order (Phase C C4).
6. **Existence PDE characterization corrected:** the frozen analytic problem is a
   **first-order** regime-switching HJB (no second-order term in the accepted
   authority); any viscosity/comparison framework must match that structure.
7. **Falsification language narrowed:** "no in-class counterexample found" = none
   found among the correctly analyzed families, not an exhaustive exclusion; the
   `mu_W/b >= 0` search is conditional on the realized `p=2` balance.
8. Terminal **B is retained** (not A); provisional S3 primary `R=O(1)`, P-TR
   sensitivity only, critical `m=1/2` outside S3 as benchmark, no numerical run, no
   endpoint law, stationary KFE NOT AUTHORIZED — all preserved.

---

## 3c. Rev 3 corrections (reviewer `5507222546`)

1. **Phase D made S3-compatible:** D1 no longer reproduces the `a`-dependent
   `M(a,z) b^(-3/2)` value remainder alongside `R=O(1)`; the O(1/b) coefficient audit
   is stated directly under the exact contract (E) (`V=-K/b+H/b^2+r0`,
   `V_b=K/b^2-2H/b^3+r_b`, `V_a=H_a/b^2+r_a`, `R -> H_a/K = O(1)`), with all permitted
   `a`-dependence at `H/b^2` order or smaller. A nonzero b-independent `M_a` would
   force `R ~ sqrt(b)` (outside S3) and is excluded at that order.
2. **z-dependent `1/log b` case corrected:** for `V(b,z) = -A(z)/log b`, `S*V` is also
   `O(1/log b)`; the leading equation is `S A = rho A`, and since `rho=0.02` is not in
   `{0,-2/3}` no nonzero `A(z)` survives (switch-spectrum argument). The z-constant
   case reduces to the unmatched `rho*V` term. This replaces any "simply unmatched"
   phrasing in Phase C/E and the summaries.
3. **Oscillatory-tail statement narrowed:** only constructions whose derivative changes
   sign infinitely often (violating S1 `V_b>0`) are excluded; **monotone-preserving
   oscillatory remainders** (small oscillations around a monotone leading tail keeping
   `V_b>0`) are NOT exhaustively ruled out and remain in the open
   `ASYMPTOTIC_REALIZATION / NO-EXOTIC-REGIME` gate unless separately shown harmless.
4. **Contract (E) matches the first-order HJB:** the second-derivative clause was
   removed from the HJB remainder; if second/mixed partials are needed at all, they are
   invoked only as auxiliary regularity to justify differentiating the expansion, not
   as HJB terms (the frozen HJB is first-order in `(a,b)`).
5. Terminal **B is retained**; the `1<p<2` switch-spectrum exclusion and `p>2`
   unbalanced-consumption argument are preserved unchanged.

---

## 4. What is NOT claimed

- NOT claimed: any candidate is a theorem, frozen, implemented, or model-defining.
- NOT claimed: existence/comparison/uniqueness of the admissible value solution.
- NOT claimed: that the actual HJB solution realizes `p=2` merely because S3 excludes
  the known `m=1/2` branch.
- NOT claimed: that `V_b*b^2 -> K` follows unconditionally; it is conditional on
  Phase B/C gates.
- NOT claimed: that the critical `R ~ Theta(sqrt(b))` family is economically
  impossible; it is outside S3 and preserved as a benchmark.
- NOT claimed: any `mu_W/b >= 0` branch under the realized `p=2` balance; within that
  balance the drift is inward, and the out-of-class critical family is also inward
  (`mu_W/b = -0.0025 - 3C/(4 chi_1) < 0`). The `mu_W/b >= 0` search is conditional, not
  a general theorem over all S3 non-power tails.
- NOT claimed: an **exhaustive** exclusion of every non-power/exotic S3 tail; only the
  power families and the explicitly tested log/slow families are excluded, and broader
  classes — including monotone-preserving oscillatory remainders (small oscillations
  around a monotone leading tail may keep `V_b>0`) — remain part of the open
  `ASYMPTOTIC_REALIZATION / NO-EXOTIC-REGIME` gate.
- NOT claimed: full `[0,10]` uniform theorem authority; endpoint laws are unresolved.
- NOT claimed: any numerical result; the falsification protocol is design only.

---

## 5. Deliverables (Issue #43 allowlist)

- This document.
- `reports/dlh_5q_provisional_s3_theorem_falsification_2026_09_02/` with exactly:
  - `DLH_5Q_PROVISIONAL_AUTHORITY_FREEZE.md` (Phase A)
  - `DLH_5Q_EXISTENCE_COMPARISON_AUDIT.md` (Phase B)
  - `DLH_5Q_ASYMPTOTIC_REALIZATION_ANALYSIS.md` (Phase C)
  - `DLH_5Q_P2_COEFFICIENT_AND_DRIFT_AUDIT.md` (Phase D)
  - `DLH_5Q_ANALYTIC_FALSIFICATION_SEARCH.md` (Phase E)
  - `DLH_5Q_NUMERICAL_FALSIFICATION_PROTOCOL.md` (future protocol, NOT executed)
  - `DLH_5Q_ENDPOINT_SCOPE_AUDIT.md` (Phase F)
  - `DLH_5Q_THEOREM_FALSIFICATION_MATRIX_AND_TERMINAL.md` (Phase G + exact terminal)
  - `DLH_5Q_FORBIDDEN_OPERATION_CHECK.md` (scope/forbidden check)
