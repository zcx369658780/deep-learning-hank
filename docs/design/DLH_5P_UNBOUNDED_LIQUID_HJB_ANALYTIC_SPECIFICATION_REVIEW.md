# DLH-5P / Issue #42 — Unbounded-Liquid Analytic HJB Specification and Critical-Transfer Admissibility (Rev 2)

**Task type:** `SCIENTIFIC_ANALYTIC_MODEL_SPECIFICATION__UNBOUNDED_LIQUID_HJB_ADMISSIBILITY_AND_CRITICAL_TRANSFER`
**Date:** 2026-09-02
**Branch:** `dsh/issue-42-dlh-5p-unbounded-liquid-hjb-specification-2026-09-02`
**Fresh `origin/main` baseline:** `20b4688ef6a77bf5b3e789abf5ec15a80fe188ea`
**Rev 1 candidate reviewed:** `3fde31a51cf5703f1a4c3c8e1dc8dadc33e1c156`
**Reviewer status (fresh, `5504929967`):**
`DLH_5P_CANDIDATE_REVIEW_BLOCKED__CRITICAL_TRANSFER_CLAIRAUT_ARGUMENT_NOT_VALID_WITH_UNCONTROLLED_REMAINDER__S1_S2_SPECIFICATION_INTERNAL_CONTRADICTIONS__BOUNDED_SAME_ISSUE_REVISION_REQUIRED`

This is a **theory/design specification gate only** (bounded same-Issue revision of the
9 Issue #42 allowlist-created files). It does NOT freeze or implement any analytic
specification, does NOT select R/W/W1/W2/`W_max`, does NOT run any numerical
experiment, and creates no production HJB/domain authority. Builder recommendation is
not model freeze; the Owner remains final authority.

**Rev 2 summary of changes from Rev 1:** the Clairaut `p=1/2` inference and the
associated "critical-branch ruled out" claim are **withdrawn** (Blocking corrections 1-3
of `5504929967`); the critical `m=1/2` branch is preserved as **unresolved/admissible**
(compact interior-`a`) per the reviewer's Option B; S1 and S2 are corrected (S1 no
longer implicitly forces `V -> 0`; S2's transversality is stated as a proposed
verification/selection condition, not a proved necessity, and not mechanically equated
with an asset no-Ponzi law); S3/P-TR are re-stated as an explicit Owner-adopted
admissibility primitive (not "independently justified by a ruling-out"); the endpoint
audit separates full `[0,10]` uniform, compact interior-`a`, and `a -> 0` bare-`a`
behavior; `max(a,a_bar)` is retained explicitly in critical-transfer coefficients; the
borrowing-gap economics is kept distinct from adopting `b_lo=-2` as analytic state-space
authority; and the recommendation terminal moves from A to **B**.

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

## 2. Executive summary of the DLH-5P Rev 2 review

### Phase A — Authority-extension map (inherited vs new)

The accepted finite-grid solver inherits the economics and the algebraic form of the
interior HJB identity (including the combined transfer Hamiltonian), but every
ingredient needed for an unbounded-`b` problem is `NEW_ANALYTIC_MODEL_DEFINITION_REQUIRES_OWNER`:
the state-space extension, the asymptotic boundary/transversality law, the
upper-`a`/lower-`b` endpoint laws, and the selection (comparison/uniqueness) argument.
P-TR and regularity/uniformity are `THEOREM_ASSUMPTION_ONLY__NOT_MODEL_PRIMITIVE` unless
the Owner elevates them. **The borrowing-rate-gap economics is inherited and distinct
from adopting `b_lo = -2` as continuous analytic state-space authority** (the latter is
new model definition). The critical `m=1/2` branch is `UNRESOLVED/ADMISSIBLE` (Rev 1's
Phase E ruling-out is withdrawn).

### Phase B — Three candidate specifications (S1/S2/S3)

- **S1 (minimal growth/admissibility, corrected):** state space
  `(b_lo,+inf) x (0,a_max) x {z}`, the interior HJB, a **coherent** growth class
  (`V in C(D̄) cap C^1(D)`, `V_b > 0`, `V < 0`, polynomial growth `|V| <= C(1+|b|)^N`;
  **no forced `V -> 0`**). S1 explicitly acknowledges that `V -> 0` is a tail-selection
  feature, not an S1 property. Necessary base; insufficient for uniqueness or the
  `p=2` coefficient.
- **S2 (transversality / no-Ponzi, corrected):** proposes the discounted-value
  verification/selection condition `lim_{T->inf} e^{-rho*T} E[V(b_T,a_T,z_T)] = 0`
  **as a proposed analytic selection condition, NOT a proved necessity, and NOT
  mechanically equated with an asset-level no-Ponzi law**. Admissible-path and
  integrability requirements are stated. S2 selects the tail integration constant but
  does not control `R = V_a/V_b`; its incremental selection over corrected S1 is
  **partial** (it excludes exploding values but not, by itself, the `m=1/2` branch).
- **S3 (derivative-controlled admissibility):** an explicit **Owner-adopted
  admissibility primitive** `R = V_a/V_b = O(1)` uniformly (preferred) or at least
  `P-TR: R = o(sqrt(b))` uniformly. Under S3 the DLH-5O `p=2` coefficient follows.
  It is NOT claimed to be independently justified by a critical-branch ruling-out
  (that ruling-out is withdrawn); its justification is that it is an explicit,
  economically motivated (bounded-transfer rationale is motivation, not derivation),
  falsifiable admissibility primitive the Owner may adopt.

### Phase C — Boundary/endpoint audit

- `a = 0`: bare-`a` degeneracy (`d = a*T(q)/chi_1 = 0` for any `R`); `R` is vacuous at
  `a = 0`, `mu_a = 0`. The `m=1/2` branch's interior realizations (`L ~ a^{-1/2}`) are
  singular at `a = 0`, so a **full-`[0,10]` uniform smooth** critical branch is not
  established; the **compact interior-`a`** branch is admissible (Rev 2 Phase E).
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
  transversality controls the value level, not `R`). It is an additional assumption.
- Under **S3**: P-TR is an **Owner-adopted admissibility primitive**; it is implied by
  the stronger `R=O(1)`; it is **not** derived and **not** justified by a
  critical-branch exclusion (the exclusion is withdrawn). It is falsifiable.
- P-TR is **never** labeled "proved" or "independently justified."

### Phase E — Critical `m = 1/2` branch: WITHDRAWN ruling-out; UNRESOLVED/ADMISSIBLE

Rev 1's Clairaut argument (`R ~ L sqrt(b)` + `C^2` ⇒ `p = 1/2`) is **withdrawn**
(Blocking correction 1). The reason: differentiating the leading equivalence
term-by-term is unjustified. With an explicit remainder-derivative expansion

```text
V_b = K(z) b^{-p} + M(a,z) b^{-p-1/2} + o(b^{-p-1/2}),   K_a = 0,
V_sub = M(a,z)/(1/2-p) b^{1/2-p},   R ~ [M_a/(K(1/2-p))] sqrt(b),
partial_a V_b ~ M_a b^{-p-1/2} = partial_b V_a,
```

Clairaut is satisfied for **arbitrary `p`** (within the expansion's validity), so
`C^2` smoothness alone does not force `p=1/2`; the same missing remainder-derivative
control that mattered in DLH-5O reappears. Per the reviewer's Option B, DLH-5P does
NOT add a branch-excluding regularity assumption (that would be circular); instead the
critical branch is left **unresolved/admissible** and its general same-order system is
derived without the shortcut:

- For the `p = 2` base, `V ~ -K(z)/b - (2/3)M(a,z) b^{-3/2}` (arbitrary a-dependent
  remainder) gives `R ~ L sqrt(b)` with `L = -(2/3)M_a/K`, Clairaut-consistent, and the
  altered `O(1/b)` system

  ```text
  (rho + r_b)K - 2 sqrt(K) = S*K + 0.5 a L^2 K / chi_1,   L = -(2/3)M_a/K.
  ```

- On a **compact interior-`a`** domain, `a L(a,z)^2` can be constant with
  `L ~ a^{-1/2}` (`M ~ sqrt(a)`, smooth away from `a=0`), giving a coherent altered
  balance with a **continuum of coefficients** `c/b != (rho+r_b)/2` (a one-parameter
  family indexed by the remainder amplitude). This branch is **admissible at the
  dominant-balance level**; completing it to a full solution is **UNRESOLVED**.
- At **`a = 0`**, the bare-`a` degeneracy (`d = 0`, `mu_a = 0`) makes the transfer
  ratio vacuous; the `L ~ a^{-1/2}` family is singular there, so a full-`[0,10]`
  uniform smooth realization of this branch is **not established**.

**Consequence:** the critical branch does NOT admit the Rev 1 exclusion; the `p=2`
tail is **not unique** among smooth dominant balances (P-TR selects it only as an
Owner-adopted primitive). Recommendation moves to **B**.

### Phase F — Theorem/falsification contract

For each candidate, future theorem gates: existence, uniqueness/comparison, tail
regularity (with explicit derivative-remainder control), uniformity over `(a,z)`,
derivation or justified adoption of P-TR, **resolution (not assumption) of the `m=1/2`
branch**, `V_b*b^2 -> K` convergence, `c/b -> 0.0175`, `mu_W/b -> -0.0025`, and
explicit falsification conditions. No theorem is claimed in this task.

### Phase G — Owner decision packet and recommendation

**Recommendation (B):**
`DLH_5P_CRITICAL_TRANSFER_BRANCH_REMAINS_ADMISSIBLE__TAIL_SPECIFICATION_NOT_UNIQUE__OWNER_DECISION_REQUIRED`

Because the critical `m=1/2` branch is **admissible/unresolved** (compact interior-`a`)
and yields a different tail coefficient, the tail specification is **not unique** under
S1/S2, and under S3 it is unique only via an **explicit Owner-adopted admissibility
primitive** (P-TR / `R=O(1)`). Recommendation B is the honest terminal: the Owner must
decide whether to (i) adopt S3 with the P-TR/`R=O(1)` primitive as model authority
(uniqueness then conditional on that primitive, not on Phase E), or (ii) keep the
branch open and pursue the Phase F resolution. The recommendation is not a freeze.

---

## 3. The corrected central scientific statement

The Rev 1 claim "the critical branch is ruled out as a smooth dominant balance" is
**withdrawn**. The corrected statement is: the critical `R ~ L(a,z) sqrt(b)` branch can
be realized by a remainder-derivative mechanism (`V_b = K b^{-p} + M b^{-p-1/2} + ...`)
that satisfies Clairaut for any `p`, so smoothness alone does not exclude it. For the
`p=2` base this produces the altered `O(1/b)` system
`(rho+r_b)K - 2 sqrt(K) = S*K + 0.5 a L^2 K/chi_1` with `L = -(2/3)M_a/K`, which is
coherent on a compact interior-`a` domain (`L ~ a^{-1/2}` families) and yields
non-`(rho+r_b)/2` coefficients. The branch is therefore **admissible/unresolved** at
the dominant-balance level (full-`[0,10]` uniform smooth realizations not established;
`a=0` governed by the bare-`a` degeneracy). Tail uniqueness holds only under an
explicitly adopted S3/P-TR primitive, not by exclusion.

---

## 4. What is NOT claimed

- NOT claimed: any candidate is frozen, implemented, or model-defining.
- NOT claimed: P-TR is "proved" or "independently justified"; it is an Owner-adopted
  admissibility primitive (S3).
- NOT claimed: the `m=1/2` branch is ruled out; it is unresolved/admissible (compact
  interior-`a`) per the reviewer's Option B.
- NOT claimed: any theorem is proved; the `p=2` result remains a conditional dominant
  balance under an adopted P-TR primitive, pending the Phase F theorem gates.
- NOT claimed: R/W/W1/W2/`W_max`, new `b_max`/`a_max`, taper extrapolation, or
  stationary authority.

## 5. Next step

Owner decides among S1/S2/S3 (recommendation: Recommendation B — decide whether to
adopt S3 with the P-TR/`R=O(1)` primitive, or to fund the Phase F resolution of the
critical branch) after fresh ChatGPT review. Stationary KFE remains NOT AUTHORIZED
under Issue #27.
