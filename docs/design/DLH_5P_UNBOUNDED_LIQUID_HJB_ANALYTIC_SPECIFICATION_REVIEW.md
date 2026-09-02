# DLH-5P / Issue #42 — Unbounded-Liquid Analytic HJB Specification and Critical-Transfer Admissibility (Rev 4)

**Task type:** `SCIENTIFIC_ANALYTIC_MODEL_SPECIFICATION__UNBOUNDED_LIQUID_HJB_ADMISSIBILITY_AND_CRITICAL_TRANSFER`
**Date:** 2026-09-02
**Branch:** `dsh/issue-42-dlh-5p-unbounded-liquid-hjb-specification-2026-09-02`
**Fresh `origin/main` baseline:** `20b4688ef6a77bf5b3e789abf5ec15a80fe188ea`
**Rev 3 candidate reviewed:** `6e1f175dac1838f1378488a61af754ebd35589c0`
**Reviewer status (fresh, `5505516566`):**
`DLH_5P_REV3_CANDIDATE_REVIEW_BLOCKED__CRITICAL_TRANSFER_HJB_SIGN_ERROR__ALTERED_COEFFICIENT_AND_DRIFT_FORMULAS_REQUIRE_BOUNDED_REVISION`

This is a **theory/design specification gate only** (bounded same-Issue revision of the
9 Issue #42 allowlist-created files). It does NOT freeze or implement any analytic
specification, does NOT select R/W/W1/W2/`W_max`, does NOT run any numerical
experiment, and creates no production HJB/domain authority. Builder recommendation is
not model freeze; the Owner remains final authority.

**Rev 4 summary of changes from Rev 3:** the only blocking issue is a **sign error** in
the critical-branch `O(1/b)` coefficient equation (Blocking corrections of
`5505516566`). The optimized transfer Hamiltonian `H_tr = V_b[d(R-1)-chi]` enters the
accepted HJB **positively**, so the altered equation is
`(rho+r_b)K - 2 sqrt(K) = S*K - 0.5*C*K/chi_1` (MINUS on the right; Rev 3 had PLUS).
Consequences corrected everywhere: `c/b = (rho+r_b + 0.5 C/chi_1)/2` (PLUS in the
denominator; positivity automatic for `C>=0`, the Rev 3 restriction
`rho+r_b > 0.5 C/chi_1` removed), and `mu_W/b = -0.0025 - 3C/(4 chi_1) < 0` for
`C>=0` (not `-C/(4 chi_1)`). The `M(a,z)` integration factor is corrected to
`M(a,z) = -3 K sqrt(C a) + const` (up to the sign branch), not `-(3/2)K sqrt(a)`.
Qualitative conclusions are unchanged and, if anything, strengthened: the critical
family changes the consumption ratio (non-unique) but remains total-wealth inward
(`mu_W/b < 0`); no mean-reversion reversal is claimed; the `m=1/2` branch stays
UNRESOLVED/ADMISSIBLE on compact interior-`a`; Recommendation B is preserved.

**Rev 3 summary of changes from Rev 2:** (i) **S1 corrected** — the class
`V_b>0, V<0`, continuity to the finite `b_lo`, compact `a in [0,10]`, finite `z`
implies V is monotone increasing in `b` and **globally bounded**, converging to a
finite `V_inf(a,z) <= 0` as `b -> +inf`; the invalid `-2K sqrt(b)` example (violates
`V_b>0`) is removed and no polynomial growth bound is needed; (ii) **S2 corrected** —
the discounted-value condition `e^{-rho T} E[V] -> 0` is **vacuous/redundant under S1**
(bounded V makes it automatic); it is replaced by an explicit tail-value selection
`V_inf(a,z) = 0` (V vanishes at the tail), clearly marked NEW analytic model
definition / theorem assumption, no necessity claim, distinct from asset no-Ponzi;
(iii) **S3 uniqueness language corrected** — P-TR/`R=O(1)` excludes the `m=1/2` branch
**by class** but does NOT by itself prove the realized HJB tail is `p=2`; the `p=2`
coefficient theorem remains conditional on the full DLH-5O premise set, and actual tail
uniqueness still requires existence/comparison/asymptotic-realization proof;
(iv) **critical-branch total-wealth drift accounted (Rev 4 sign correction)** — with
`C = a L^2` (a>=a_bar): the `O(1/b)` altered equation is
`(rho+r_b)K - 2 sqrt(K) = S*K - 0.5*C*K/chi_1` (the optimized transfer Hamiltonian
enters the HJB positively, so the sign is MINUS on the right; Rev 3 had it wrong),
giving `c/b = (rho+r_b + 0.5 C/chi_1)/2`, `chi/b = 0.5 C/chi_1`, hence
`mu_W/b = r_b - c/b - chi/b = -0.0025 - 3C/(4 chi_1) < 0` for `C >= 0` — the critical
family makes the consumption ratio non-unique but does **not** reverse total-wealth
mean reversion (adjustment cost is O(b), making total drift even more inward);
`max(a,a_bar)` is retained explicitly for `0<a<a_bar` (the `a>=a_bar` formulas are not
extended through that layer); Recommendation B is retained with the clarified meaning
"tail coefficient / analytic specification non-unique", NOT automatically
"mean-reversion sign unresolved".

---

## 0. Controlling accepted authority

- Issue #41 / DLH-5O **accepted and completed**. Accepted candidate:
  `25645d2dd1963e8fc17176a7fadc16d914811221`; reviewer acceptance `5504453148`;
  integration commit `540b16ebd3a577a55ccd92a8d74ced373798557e`.
- Accepted DLH-5O terminal:
  `DLH_5O_HJB_LIQUID_TAIL_DOMINANT_BALANCE_CONDITIONAL__MISSING_ANALYTIC_ASSUMPTIONS_IDENTIFIED`.
- Owner decision after DLH-5O:
  `APPROVE_UNBOUNDED_B_ANALYTIC_HJB_SPECIFICATION_GATE__THEORY_DESIGN_ONLY`.
- Accepted household source (immutable, read-only):
  `src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`
  (blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`).
- Accepted DLH-5N / DLH-5O theory packages are read-only controlling context.
- Stationary KFE remains NOT AUTHORIZED under Issue #27.

---

## 1. Purpose

DLH-5P formulates and stress-tests candidate analytic authority for the fixed-`a`,
unbounded-positive-liquid-wealth HJB problem needed to turn the accepted DLH-5O
conditional dominant balance into a theorem candidate. It answers: what exact
continuous HJB problem, admissibility/transversality class, regularity/uniformity
requirements, and value-gradient/transfer restrictions are scientifically defensible
as analytic authority for `b -> +infinity`, and does that specification rule out,
admit, or leave unresolved the critical `V_a/V_b ~ Theta(sqrt(b))` branch?

This Issue does NOT freeze that specification; it produces candidate specifications,
consequences, falsification conditions, and an Owner decision packet.

---

## 2. Executive summary of the DLH-5P Rev 3 review

### Phase A — Authority-extension map (inherited vs new)

The accepted finite-grid solver inherits the economics and the algebraic form of the
interior HJB identity (including the combined transfer Hamiltonian), but every
ingredient needed for an unbounded-`b` problem is `NEW_ANALYTIC_MODEL_DEFINITION_REQUIRES_OWNER`:
the state-space extension, the asymptotic boundary/transversality law, the
upper-`a`/lower-`b` endpoint laws, and the selection (comparison/uniqueness) argument.
P-TR and regularity/uniformity are `THEOREM_ASSUMPTION_ONLY__NOT_MODEL_PRIMITIVE` unless
the Owner elevates them. **The borrowing-rate-gap economics is inherited and distinct
from adopting `b_lo = -2` as continuous analytic state-space authority** (the latter is
new model definition). The critical `m=1/2` branch is `UNRESOLVED/ADMISSIBLE` (compact
interior-`a`), preserved from Rev 2.

### Phase B — Three candidate specifications (S1/S2/S3)

- **S1 (minimal admissibility, corrected Rev 3):** state space
  `(b_lo,+inf) x (0,a_max) x {z}`, the interior HJB, class
  `V in C(D̄) cap C^1(D)`, `V_b > 0`, `V < 0`, continuity to finite `b_lo`, compact
  `a`, finite `z`. **Derived consequence:** V is monotone increasing in `b` and
  **globally bounded**, so `V -> V_inf(a,z) in [-C, 0]` exists (pointwise) as
  `b -> +inf`. No growth bound is needed (it follows); the invalid `-2K sqrt(b)` example
  is removed (it violates `V_b>0`). `V -> 0` is a tail-selection feature, not an S1
  property. S1 is necessary but insufficient (no uniqueness; `V_inf` free; the `p=2`
  coefficient does not follow).
- **S2 (tail-value selection, corrected Rev 3):** the discounted-value condition
  `e^{-rho T} E[V] -> 0` is **vacuous/redundant under S1** (bounded V makes it
  automatic) and is **replaced** by the explicit tail-value selection
  `V_inf(a,z) = 0` (`V -> 0` uniformly as `b -> +inf`), marked
  `NEW_ANALYTIC_MODEL_DEFINITION_REQUIRES_OWNER` / theorem assumption (no necessity
  claim), distinct from asset no-Ponzi. It excludes `V -> negative-constant` branches
  (genuine selection over S1) but does NOT exclude the `m=1/2` family (which also has
  `V_inf = 0`).
- **S3 (derivative-controlled admissibility):** explicit **Owner-adopted primitive**
  `R = V_a/V_b = O(1)` uniformly (preferred) or `P-TR: R = o(sqrt(b))` uniformly. It
  excludes the `m=1/2` branch **by class**; the `p=2` coefficient is then available
  **conditional on the full DLH-5O theorem premise set** (including `p=2` asymptotic
  realization / no exotic competing regime). Actual tail uniqueness is NOT established
  by the primitive alone.

### Phase C — Boundary/endpoint audit

- `a = 0`: bare-`a` degeneracy (`d = a*T(q)/chi_1 = 0` for any `R`); `R` is vacuous at
  `a = 0`, `mu_a = 0`. The `m=1/2` branch's interior realizations (`L ~ a^{-1/2}`) are
  singular at `a = 0`, so a **full-`[0,10]` uniform smooth** critical branch is not
  established; the **compact interior-`a`** branch is admissible.
- `a = a_max = 10`: `r_a_eff(10) = 0.027 > 0`; the finite-grid `at_upper_a` branch
  (restricts `d < 0`) is `INHERITED_FINITE_GRID_NUMERICAL_SEMANTICS_ONLY`; the analytic
  upper-`a` endpoint law is `NEW_ANALYTIC_MODEL_DEFINITION_REQUIRES_OWNER`.
- `b = b_lo = -2`: borrowing-rate gap (0.025 for `b<0`) is accepted economics; the
  `b_lo` marginal-utility closure is numerical semantics only; **adopting `b_lo = -2`
  as the continuous analytic state-space lower bound is new model definition** (the
  grid chose the value; the analytic adoption is a separate decision). The tail result
  should be independent of the `b_lo` law (robustness/falsifiability gate).

### Phase D — P-TR derivability audit

- Under **S1** and **S2**: P-TR is **not** derived (S1 has no tail law; S2's
  tail-value selection does not control `R`). It is an additional condition.
- Under **S3**: P-TR is an **Owner-adopted admissibility primitive**; implied by the
  stronger `R=O(1)`; **not** derived; **not** justified by any ruling-out; it excludes
  the `m=1/2` branch by class but does NOT prove the realized tail is `p=2`.
- P-TR is **never** labeled "proved" or "independently justified."

### Phase E — Critical `m = 1/2` branch: UNRESOLVED/ADMISSIBLE (preserved), with explicit total-wealth drift (Rev 4 sign correction)

The Rev 2 status is preserved: the branch is realized by the remainder-derivative
mechanism (`V_b = K b^{-p} + M b^{-p-1/2} + ...`, Clairaut-consistent for any `p`), is
a coherent altered dominant balance on the compact interior, and is left
**UNRESOLVED/ADMISSIBLE** (no branch-excluding assumption is added — that would be
circular). Rev 3 added the explicit **total-wealth drift accounting**; **Rev 4 corrects
the sign of the altered `O(1/b)` equation** (the optimized transfer Hamiltonian enters
the HJB positively, so the transfer term is SUBTRACTED when rearranged):

```text
altered O(1/b) system:  (rho + r_b)K - 2 sqrt(K) = S*K - 0.5*C*K/chi_1,   C = a L^2.
for a >= a_bar,  C = a L^2 (a-independent):
  c/b = (rho + r_b + 0.5 C/chi_1)/2,      (PLUS in the denominator)
  chi/b = 0.5 C/chi_1,
  mu_W/b = r_b - c/b - chi/b = (r_b - rho)/2 - 3C/(4 chi_1) = -0.0025 - 3C/(4 chi_1) < 0  for C >= 0.
```

The critical family therefore makes the **consumption ratio non-unique**
(`c/b != (rho+r_b)/2` unless `C=0`; with the corrected sign `c/b` is larger than
`0.0175` for `C>0`) but does **NOT** reverse total-wealth mean reversion on
`a >= a_bar` (adjustment cost is O(b), making `mu_W` even more inward). For
`0 < a < a_bar`, `max(a,a_bar)` is kept explicit and the `a>=a_bar` formulas are not
extended through that layer.

### Phase F — Theorem/falsification contract

For each candidate, future theorem gates: existence, uniqueness/comparison, tail
regularity (with explicit derivative-remainder control), uniformity over `(a,z)`,
derivation or justified adoption of P-TR, **resolution (not assumption) of the `m=1/2`
branch**, `V_b*b^2 -> K` convergence, `c/b -> 0.0175`, `mu_W/b -> -0.0025`, and
explicit falsification conditions (including that the critical family has `mu_W/b =
-0.0025 - 3C/(4 chi_1) < 0`, so drift-sign is inward for both branches). No theorem is
claimed in this task.

### Phase G — Owner decision packet and recommendation

**Recommendation (B):**
`DLH_5P_CRITICAL_TRANSFER_BRANCH_REMAINS_ADMISSIBLE__TAIL_SPECIFICATION_NOT_UNIQUE__OWNER_DECISION_REQUIRED`

The critical `m=1/2` branch is **admissible/unresolved** (compact interior-`a`) and
yields a non-unique consumption ratio `c/b`; under S1/S2 the tail specification is not
unique; under S3 it is unique only via an **explicit Owner-adopted P-TR/`R=O(1)`
primitive**, and even then actual tail uniqueness remains to be proved (Phase F). The
meaning of Recommendation B is clarified: **tail coefficient / analytic specification
non-unique** — NOT automatically "mean-reversion sign unresolved", because the
demonstrated compact-interior critical family still has inward `mu_W/b = -0.0025 -
3C/(4 chi_1) < 0` (adjustment cost is O(b)). The recommendation is not a freeze.

---

## 3. The corrected central scientific statement (Rev 4)

The critical `R ~ L(a,z) sqrt(b)` branch is realized by a remainder-derivative
mechanism (`V_b = K b^{-p} + M b^{-p-1/2} + ...`, Clairaut-consistent for any `p`); for
the `p=2` base it yields the altered `O(1/b)` system
`(rho+r_b)K - 2 sqrt(K) = S*K - 0.5*C*K/chi_1` (`L = -(2/3)M_a/K`, `C = aL^2`,
sign corrected in Rev 4), coherent on the compact interior with `L ~ a^{-1/2}`
families. Its consumption ratio is `c/b = (rho+r_b + 0.5 C/chi_1)/2` and its
total-wealth drift is `mu_W/b = -0.0025 - 3C/(4 chi_1) < 0` for `C = aL^2 >= 0`
(`a >= a_bar`), so it changes the consumption ratio but does NOT reverse mean
reversion. The branch is **UNRESOLVED/ADMISSIBLE**; the `p=2` tail is unique only
under an explicitly adopted S3/P-TR primitive (and even then uniqueness of the realized
tail must be proved via the Phase F gates).

---

## 4. What is NOT claimed

- NOT claimed: any candidate is frozen, implemented, or model-defining.
- NOT claimed: P-TR is "proved" or "independently justified"; it is an Owner-adopted
  admissibility primitive (S3), and it does NOT by itself prove the realized tail is
  `p=2`.
- NOT claimed: the `m=1/2` branch is ruled out; it is unresolved/admissible (compact
  interior-`a`).
- NOT claimed: the critical branch reverses mean reversion; its `mu_W/b =
  -0.0025 - 3C/(4 chi_1) < 0` (inward) on `a >= a_bar`.
- NOT claimed: any theorem is proved; the `p=2` result remains conditional on the full
  DLH-5O premise set plus the adopted P-TR primitive, pending the Phase F theorem gates.
- NOT claimed: R/W/W1/W2/`W_max`, new `b_max`/`a_max`, taper extrapolation, or
  stationary authority.

## 5. Next step

Owner decides among S1/S2/S3 (recommendation: Recommendation B — decide whether to
adopt S3 with the P-TR/`R=O(1)` primitive, or to fund the Phase F resolution of the
critical branch) after fresh ChatGPT review. Stationary KFE remains NOT AUTHORIZED
under Issue #27.
