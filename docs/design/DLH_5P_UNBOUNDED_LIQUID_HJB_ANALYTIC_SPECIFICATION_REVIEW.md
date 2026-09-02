# DLH-5P / Issue #42 — Unbounded-Liquid Analytic HJB Specification and Critical-Transfer Admissibility

**Task type:** `SCIENTIFIC_ANALYTIC_MODEL_SPECIFICATION__UNBOUNDED_LIQUID_HJB_ADMISSIBILITY_AND_CRITICAL_TRANSFER`
**Date:** 2026-09-02
**Branch:** `dsh/issue-42-dlh-5p-unbounded-liquid-hjb-specification-2026-09-02`
**Fresh `origin/main` baseline:** `20b4688ef6a77bf5b3e789abf5ec15a80fe188ea`

This is a **theory/design specification gate only**. It does NOT freeze or implement any
analytic specification, does NOT select R/W/W1/W2/`W_max`, does NOT run any numerical
experiment, and creates no production HJB/domain authority. Builder recommendation is
not model freeze; the Owner remains final authority for any model-defining analytic
specification.

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

## 2. Executive summary of the DLH-5P review

### Phase A — Authority-extension map (inherited vs new)

The accepted finite-grid solver inherits the economics and the algebraic form of the
interior HJB identity (including the combined transfer Hamiltonian), but every
ingredient needed for an unbounded-`b` problem is `NEW_ANALYTIC_MODEL_DEFINITION_REQUIRES_OWNER`:
the state-space extension, the asymptotic boundary/transversality law, the
upper-`a`/lower-`b` endpoint laws, and the selection (comparison/uniqueness) argument.
P-TR and regularity/uniformity are `THEOREM_ASSUMPTION_ONLY__NOT_MODEL_PRIMITIVE` unless
the Owner elevates them. The critical `m = 1/2` branch is `UNRESOLVED` at the level of
the accepted DLH-5O package; DLH-5P analyzes it (Phase E).

### Phase B — Three candidate specifications (S1/S2/S3)

- **S1 (minimal growth/admissibility):** state space `(b_lo,+inf) x (0,a_max) x {z}`,
  the interior HJB, a broad growth class, **no** tail boundary condition. Necessary
  base; insufficient for uniqueness or the `p=2` coefficient.
- **S2 (economically mapped transversality/no-Ponzi):** adds
  `lim_{T->inf} e^{-rho*T} E[V(b_T,a_T,z_T)] = 0` (and no-Ponzi), mapped to the
  household's own discounted objective. Selects the tail constant of integration but
  does not control `R = V_a/V_b`; `p=2` coefficient still conditional.
- **S3 (derivative-controlled admissibility):** adds an explicit admissible class
  `R = V_a/V_b = O(1)` uniformly (preferred) or at least `P-TR: R = o(sqrt(b))`
  uniformly. Under S3 the DLH-5O `p=2` coefficient theorem follows. Justification:
  the DLH-5P ruling-out of the critical branch (Phase E) plus a bounded-transfer
  economic argument; it is an explicit, falsifiable class.

### Phase C — Boundary/endpoint audit

- `a = 0`: bare-`a` degeneracy (`d = a*T(q)/chi_1 = 0` for any `R`); `R` is vacuous at
  `a = 0`, `mu_a = 0`; the `a = 0` corner is trivial for the coefficient/sign theorem.
- `a = a_max = 10`: `r_a_eff(10) = 0.027 > 0`; the finite-grid `at_upper_a` branch
  (restricts `d < 0`) is `INHERITED_FINITE_GRID_NUMERICAL_SEMANTICS_ONLY`; the analytic
  upper-`a` endpoint law is `NEW_ANALYTIC_MODEL_DEFINITION_REQUIRES_OWNER`.
- `b = b_lo = -2`: borrowing-rate gap (0.025 for `b<0`) is accepted economics; the
  `b_lo` marginal-utility closure is numerical semantics only; the analytic lower-bound
  law is new model definition. The tail result should be independent of the `b_lo` law
  (robustness/falsifiability gate).
- **Full `[0,10]` uniform theorem:** the coefficient and sign results are
  `a`-independent, so they are uniform on `[0,10]` once the `a=0` and `a_max` endpoint
  conventions are pinned by the chosen candidate; otherwise a clean interior-`a`
  theorem on `(0,a_max)` plus an explicit endpoint audit. The `m=1/2` ruling-out holds
  on `(0,10]` and is trivial at `a=0`.

### Phase D — P-TR derivability audit

- Under **S1** and **S2**: P-TR is **not** derived (S1 has no tail law; S2's
  transversality controls the value level, not `R`). It is an additional assumption.
- Under **S3**: P-TR is an **admissibility assumption**; it is implied by the stronger
  `R=O(1)`; and it is **partially derived** at the dominant-balance level — DLH-5P
  shows (Phase E) that all smooth, self-consistent dominant balances with the `p=2`
  base have `R = O(1)` or lower, and the critical/sub-root power branches are
  inconsistent. It is **not circular** in the harmful sense (the class admits any
  `R=O(1)` subleading a-dependence; the coefficient is derived, not assumed) and it is
  **falsifiable**.
- P-TR is **never** labeled "proved" merely because it was assumed in DLH-5O.

### Phase E — Critical `m = 1/2` branch: RULED OUT (as a smooth dominant balance)

The central new DLH-5P result. With `R = V_a/V_b ~ L(a,z) sqrt(b)`, `L != 0`, and a
smooth (`C^2`) value function, the mixed-partial (Clairaut) consistency forces
`V_b ~ K(z) b^{-1/2}` with `a`-independent `K` — i.e. the critical branch is a
`p = 1/2` tail, **not** a `p = 2` tail. Substituting into the source-faithful interior
balance (with the combined transfer Hamiltonian) gives an `O(b^{1/2})` equation with a
single `a`-dependent transfer term `0.5*a*L^2*K/chi_1` that cannot be matched
uniformly over `(0,10]` (all other `O(b^{1/2})` terms are `a`-independent), forcing
`L = 0` — contradiction. Equivalently, the balance reduces to
`(rho - r_b/2)K = S*K` with `rho - r_b/2 = 0.0125` not in the switch spectrum
`{0, -2/3}`, forcing `K = 0`. Hence the critical branch is **not** an admissible
smooth dominant balance. This resolves the DLH-5O "unresolved" status within the
dominant-balance framework; non-smooth/non-power exotic realizations remain beyond the
framework (not analyzable from accepted authority). The `p=2` tail is thereby the
**unique** self-consistent smooth dominant balance among the analyzed classes.

### Phase F — Theorem/falsification contract

For each candidate, future theorem gates: existence, uniqueness/comparison, tail
regularity, uniformity over `(a,z)`, derivation or justified admissibility of P-TR,
exclusion of the `m=1/2` branch (Phase E argument formalized), `V_b*b^2 -> K`
convergence, `c/b -> 0.0175`, `mu_W/b -> -0.0025`, and explicit falsification
conditions. No theorem is claimed in this task.

### Phase G — Owner decision packet and recommendation

**Recommendation (A):**
`DLH_5P_ANALYTIC_HJB_SPECIFICATION_CANDIDATE_READY__OWNER_MODEL_DEFINITION_DECISION_REQUIRED`

The recommended package is **S3** (derivative-controlled admissibility with the
preferred `R = O(1)` subcase), with **S2's** economically mapped transversality as the
selection law and **S1** as the minimal base. Because the critical `m=1/2` branch is
ruled out (Phase E), the tail specification is **unique** among smooth dominant
balances, so Recommendation B is not triggered, and the evidence is sufficient for a
defensible candidate (Recommendation A), not C. The recommendation is not a freeze.

---

## 3. The core new scientific finding in one paragraph

Suppose `R = V_a/V_b ~ L(a,z) sqrt(b)` with `L != 0` and a smooth value function.
Clairaut's theorem on mixed partials (`partial_a V_b = partial_b V_a`) forces
`V_b ~ K(z) b^{-1/2}` (a `p=1/2` tail) with `a`-independent `K`; the `p=2` base is
incompatible with `R ~ sqrt(b)` (it would force `L = 0`). Substituting the `p=1/2`
tail into the interior HJB with the combined transfer Hamiltonian, the `O(b^{1/2})`
balance acquires a single `a`-dependent transfer term `0.5*a*L^2*K/chi_1`. Because
every other `O(b^{1/2})` term is `a`-independent, uniform consistency over `(0,10]`
forces `L = 0` (contradiction); the same conclusion follows from the switch-spectrum
equation `(rho - r_b/2)K = S*K` with `rho - r_b/2 = 0.0125 notin {0,-2/3}`, which has
only `K = 0`. Therefore the critical `m=1/2` transfer branch is **ruled out** as a
smooth, uniform dominant balance under the source-faithful interior balance shared by
all three candidates — it cannot be a realized HJB tail within the smooth
dominant-balance framework.

---

## 4. What is NOT claimed

- NOT claimed: any candidate is frozen, implemented, or model-defining.
- NOT claimed: P-TR is "proved"; it is an admissibility premise (S3), partially
  justified at the dominant-balance level, not a theorem.
- NOT claimed: the `m=1/2` branch is ruled out as a non-smooth/non-power exotic
  realization (that is beyond the dominant-balance framework and beyond accepted
  authority).
- NOT claimed: any theorem is proved; the `p=2` result remains a conditional dominant
  balance until the Phase F theorem gates are met under an Owner-endorsed candidate.
- NOT claimed: R/W/W1/W2/`W_max`, new `b_max`/`a_max`, taper extrapolation, or
  stationary authority.

## 5. Next step

Owner decides among S1/S2/S3 (recommendation: S3 with S2 selection law and S1 base)
after fresh ChatGPT review. The chosen candidate then defines the analytic HJB problem
and the Phase F theorem contract becomes the route to promoting the conditional `p=2`
result. Stationary KFE remains NOT AUTHORIZED under Issue #27.
