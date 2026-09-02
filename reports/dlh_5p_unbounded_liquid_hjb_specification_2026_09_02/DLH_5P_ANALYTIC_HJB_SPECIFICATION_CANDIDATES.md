# DLH-5P Phase B — Analytic HJB Specification Candidates (S1/S2/S3) (Rev 4)

**Issue #42 Phase B (Rev 4).** Formulates three candidate specification packages for
the unbounded-positive-`b` analytic HJB problem. They share the same inherited interior
economics (Phase A A1-A8, A12-A13) and differ in how they select/admit the tail
solution. Rev 3 corrected S1 (derived global boundedness from `V_b>0, V<0` + finite
`b_lo` + compact `a,z`; removes the invalid `-2K sqrt(b)` example), corrected S2 (the
discounted-value condition is vacuous under S1 and is replaced by an explicit
tail-value selection `V_inf = 0`, marked as new model definition, no necessity claim),
and corrected S3 (P-TR excludes the `m=1/2` branch by class but does not by itself
prove the realized tail is `p=2`). **Rev 4** carries the S1/S2/S3 logic unchanged and
updates only the critical-branch `O(1/b)` coefficient/`mu_W/b` formulas to the
corrected transfer-Hamiltonian sign (see Phase E Rev 4; B1 table).

## B0. Shared interior problem (all candidates)

State space under review:

```text
D = (b_lo, +infinity) x (0, a_max) x {z},   b_lo = -2, a_max = 10, z in {0.8, 1.3}.
```

Interior HJB (Phase A A12/A13), for `b > 0` and `a in (0, a_max)`:

```text
rho*V = u(c,l) + (r_b*b + labor_income - c)*V_b + r_a_eff(a)*a*V_a
        + V_b*[ d*(R-1) - chi(d,a) ] + S*V
R = V_a/V_b,   q = R-1,
c = V_b^(-1/2),   l = (0.85 z V_b)^(1/5),   labor_income = 0.85 z l,
d = a*T(q)/chi_1,   chi = chi_0|d| + 0.5 chi_1 d^2/max(a,a_bar),
r_a_eff(a) = 0.03*(1 - 0.1*(a/10)^9),   r_b = 0.015,   rho = 0.02,
(S*V)[z] = (1/3)(V(z') - V(z)).
```

For `b < 0` the borrowing-rate gap is applied (effective `0.025`) per the accepted
economics (Phase A A6). All candidates treat the finite-grid closures at `b_lo`, `a=0`,
`a_max` as non-analytic (Phase A A9-A11); `b_lo = -2` as a **continuous analytic
state-space lower bound is new model definition** (step 24), distinct from the
inherited borrowing-gap economics.

---

## CANDIDATE S1 — Minimal admissibility specification (corrected Rev 3)

- **Exact state space:** `D = (b_lo,+inf) x (0,a_max) x {z}`, endpoints as a subset of
  `cl(D)`.
- **Exact HJB:** the shared interior equation above on `D`; no added tail equation.
- **Lower-`b`/`a` endpoints:** `b_lo`: `V` continuous up to `b_lo` with a given lower
  data law (left to Owner; not the finite-grid closure). `a=0`: `V` continuous;
  `d=0` by the bare-`a` factor; `mu_a(0)=0` (corner). `a_max`: `V` continuous; upper-`a`
  law unspecified in S1.
- **Admissible value class (corrected):** `V in C(D̄) cap C^1(D)`, `V_b > 0`,
  `V < 0`, with continuity up to the finite lower bound `b_lo`, compact
  `a in [0,10]`, and finite `z`.
- **Derived boundedness (correction 1):** from these conditions alone:
  - `V_b > 0` and `V < 0` make `V` monotone increasing in `b`, bounded above by `0`;
  - continuity at finite `b_lo` over the compact `(a,z)` domain gives a uniform finite
    lower bound `min_{a,z} V(b_lo,a,z)`;
  - hence **V is globally bounded** on the analytic state space
    (`sup |V| < infinity`), and the pointwise limit `V_inf(a,z) := lim_{b->+inf}
    V(b,a,z) in [-C, 0]` exists for each `(a,z)`.
  - Consequently **no polynomial growth bound is needed** (boundedness follows).
  - The example `V ~ -2K sqrt(b)` is **invalid** under this class (it violates
    `V_b > 0`: `V_b = -K/sqrt(b) < 0`), and is removed. `V ~ +b` / `+sqrt(b)` are
    invalid under `V < 0`.
- **`V -> 0` status:** NOT guaranteed by S1. S1 admits any `V_inf(a,z) in [-C, 0]`;
  the decay `V -> 0` (needed for the `p=2` balance) is a **tail-selection feature**,
  provided by S2 (see below), not an S1 property.
- **Transversality/growth:** NONE (S1 is the minimal base; no selection law).
- **Regularity:** `V in C^1` on `D` (for `V_b`, `V_a`, FOCs); `C^2` on the tail for any
  dominant-balance statement, **with an explicit derivative-remainder expansion**
  (leading equivalences are not differentiated term-by-term).
- **Uniformity:** all rates uniform over `(a,z)` required for any tail statement
  (assumed or to be proved; not automatic). Full-`[0,10]` vs compact interior-`a`
  statements are kept separate (Phase C).
- **P-TR status:** NOT assumed, NOT derived; `R` uncontrolled by S1. The `m=1/2`
  branch is **admissible/unresolved** under S1 (Phase E Rev 3).
- **Does the `p=2` coefficient follow?** NO from S1 alone: without a tail selection law
  (`V_inf` free) there is a family of solutions, so the `O(1/b)` coefficient equation
  is not a theorem. `p=2` is only a candidate balance.
- **Circularity risk:** none (S1 does not select `p=2`).
- **Falsification:** an S1-admissible solution with a different smooth dominant balance
  (e.g. the `m=1/2` remainder family) satisfying the interior HJB falsifies the claim
  that `p=2` is the unique tail.
- **Relation to the finite-grid solver:** S1 is the continuous extension of the
  accepted interior economics; the solver's finite-grid closure at `b_max` is NOT used
  as a tail law (no equivalence claimed).

---

## CANDIDATE S2 — Tail-value selection specification (corrected Rev 3)

- **Exact state space:** as S1.
- **Exact HJB:** as S1.
- **Lower-`b`/`a` endpoints:** as S1.
- **Admissible value class:** S1 class + the explicit tail-value selection below.
- **The discounted-value condition is VACUOUS under S1 (correction 1):** the
  previously proposed `lim_{T->inf} e^{-rho*T} E[V(b_T,a_T,z_T)] = 0` is **redundant**
  under the corrected S1, because V is globally bounded: `|e^{-rho*T} E[V(x_T)]| <=
  e^{-rho*T} sup|V| -> 0` automatically for any admissible path for which the
  expectation is defined. It therefore does **NOT** select the tail integration
  constant and adds **no** effective tail selection beyond S1. This condition is
  classified as **REDUNDANT/VACUOUS under S1** and is **withdrawn** as a selection law.
- **Replacement tail-value selection (correction 1/15):** the genuinely stronger,
  scientifically mapped selection proposed here is the explicit **tail-value
  vanishing** condition

  ```text
  V_inf(a,z) := lim_{b->+inf} V(b,a,z) = 0   (uniformly over the claimed (a,z) support).
  ```

  This selects the decaying-to-zero branch over `V -> negative-constant` branches, and
  is the value-level assumption under which the `p=2` balance (`V ~ -K/b`) can be
  considered. Status: **NEW analytic model definition / theorem assumption**
  (`NEW_ANALYTIC_MODEL_DEFINITION_REQUIRES_OWNER` and `THEOREM_ASSUMPTION_ONLY__NOT_MODEL_PRIMITIVE`).
  **No necessity claim is made** (no proof that every admissible solution must satisfy
  it). It is **distinct from an asset no-Ponzi law**: it is a condition on the value
  function's tail level, not on the wealth process (`b_T`) not running a Ponzi scheme;
  an asset-level no-Ponzi condition would itself be new model definition.
- **What S2 adds over S1:** genuine, if partial: it excludes `V_inf(a,z) < 0`
  (negative-constant tails). What it does NOT add: it does NOT control `R = V_a/V_b`
  and does **NOT** exclude the `m=1/2` family (whose `p=2`-base value
  `V ~ -K/b - (2/3)M b^{-3/2}` also has `V_inf = 0`).
- **Regularity:** as S1.
- **Uniformity:** as S1 (the `V_inf = 0` requirement is uniform over the claimed
  support).
- **P-TR status:** NOT derived: S2's tail-value selection does not control
  `R = V_a/V_b`.
- **Does the `p=2` coefficient follow?** NO from S2 alone: the tail-value selection
  enables the `p=2` balance but does not exclude the `m=1/2` family, so the `O(1/b)`
  coefficient is still non-unique without P-TR.
- **Circularity risk:** low (the selection is not `p=2`-specific in its `R` content),
  but it is an assumption whose scientific admissibility the Owner must endorse.
- **Falsification:** a constructed S2-admissible smooth solution with `V_inf = 0` but
  a tail `p != 2` (e.g. the `m=1/2` family) satisfying the interior HJB falsifies
  `p=2` uniqueness under S2.
- **Relation to the finite-grid solver:** as S1; the solver's `b_max` marginal-utility
  closure is not promoted to this condition.

---

## CANDIDATE S3 — Derivative-controlled admissibility specification (Owner-adopted primitive)

- **Exact state space:** as S1/S2.
- **Exact HJB:** as S1/S2.
- **Lower-`b`/`a` endpoints:** as S1/S2.
- **Admissible value class:** S2 class + the explicit derivative-control restriction

  ```text
  (preferred)  R = V_a/V_b = O(1) uniformly over (a,z);
  (weaker)     P-TR: R = V_a/V_b = o(sqrt(b)) uniformly over (a,z).
  ```

  Under `R = O(1)`: `d = O(1)`, `chi = O(1)`, `mu_a = O(1)` (the stronger, cleaner
  subcase, per DLH-5O annotation A). Under P-TR only: `d = o(sqrt(b))`,
  `chi = o(b)`, `mu_a = o(sqrt(b))`.
- **Transversality/growth:** as S2 (tail-value selection `V_inf = 0`, a proposed
  selection assumption, not proved necessity).
- **Regularity:** as S1 plus the class requires the value-gradient ratio to satisfy the
  derivative-control bound (this is the admissibility content).
- **Uniformity:** the derivative-control bound is UNIFORM over `(a,z)` by definition of
  the class; further rate-uniformity as in S1.
- **P-TR status (corrected Rev 3):** P-TR / `R=O(1)` is an **explicit Owner-adopted
  admissibility primitive** (model-definition content). It excludes the `m=1/2` branch
  **by class**. It is NOT claimed to be independently justified by any ruling-out (the
  ruling-out is withdrawn), and its bounded-transfer rationale is motivation, not
  derivation.
- **Uniqueness language (correction 2/16/17):** P-TR / `R=O(1)` does **NOT** by itself
  prove that the realized HJB tail is `p=2`. It only removes the critical transfer
  branch (and the analyzed power branches) from the admissible class. The `p=2`
  coefficient is available **conditional on the full DLH-5O theorem premise set** —
  including `p=2` asymptotic realization, no exotic competing regime (e.g.
  non-power/non-smooth tails), realized-balance/uniqueness, and uniformity. The phrase
  "unique tail within S3" is **replaced** by: **"the critical `m=1/2` branch is
  excluded by the adopted primitive; actual tail uniqueness remains to be proved"**
  (existence/comparison/asymptotic-realization/coefficient-convergence gates preserved
  in Phase F).
- **Does the `p=2` coefficient follow?** Only conditional on the adopted class AND the
  full DLH-5O premises: `K = 4/(rho+r_b)^2`, `c/b = (rho+r_b)/2 = 0.0175`,
  `mu_W/b -> -0.0025 < 0`. This is a conditional theorem of the candidate, not a
  theorem of the accepted finite-grid source.
- **Circularity risk:** explicit and higher than in Rev 1's framing: the class excludes
  exactly the branch that would alter the coefficient. This is acceptable as an
  **Owner-adopted primitive** (the Owner may impose it), but it is NOT an independent
  derivation of `p=2`.
- **Falsification:** (i) a constructed S3-admissible smooth solution with `R=O(1)` and
  a tail `p != 2` satisfying the interior HJB falsifies the coefficient theorem;
  (ii) evidence that the actual HJB solution has `R` not `o(sqrt(b))` (e.g. a future
  finite-grid measurement of `V_a/V_b` near `b_max` under the accepted source)
  falsifies the class; (iii) a balance-consistent construction of the `m=1/2` family
  that also satisfies S2's tail-value selection shows the primitive is exclusionary (a
  scientific cost the Owner must weigh).
- **Relation to the finite-grid solver:** as S1; the class is a candidate model
  primitive, not a solver statement.

---

## B1. Comparison table (Rev 3)

| Item | S1 | S2 | S3 |
|---|---|---|---|
| Tail selection law | none (`V_inf` free in `[-C,0]`; `V->0` NOT forced) | explicit `V_inf(a,z) = 0` (tail-value vanishing; NEW model definition; no necessity claim); discounted-value condition is VACUOUS under S1 | S2 + derivative-control `R=O(1)` (pref.) / `R=o(sqrt(b))` (min.) |
| `V -> 0` status | not an S1 property (added selection) | selected by `V_inf = 0` (assumption, not necessity) | selected (within class, `p=2` balance uses it) |
| Boundedness of admissible V | **derived** (monotone in b, `V_b>0`, `V<0`, finite `b_lo`, compact `a,z` => globally bounded) | inherited from S1 | inherited from S1 |
| P-TR | not assumed/derived | not derived | Owner-adopted primitive (excludes `m=1/2` by class; does NOT prove realized tail is `p=2`) |
| `p=2` coefficient | does not follow | conditional only (enabled by `V_inf=0`; `m=1/2` still admissible) | **conditional on full DLH-5O premises + adopted primitive** |
| uniqueness of tail | no (family) | no (`m=1/2` admissible; level selected only) | `m=1/2` excluded by primitive; **actual tail uniqueness remains to be proved** |
| circularity risk | none | low (assumption, not necessity) | explicit (excludes the branch by class, not balance) |
| critical `m=1/2` branch | admissible/unresolved | admissible/unresolved | excluded only by the adopted class |
| `mu_W/b` sign for the critical family | n/a (S1 has no tail law) | n/a (level selection only) | n/a (class excludes it); outside the class, `mu_W/b = -0.0025 - 3C/(4 chi_1) < 0` (inward) |
| new model authority | state space + class | + `V_inf = 0` tail-value selection (needs Owner) | + derivative-control class (needs Owner) |
| economic faithfulness | high (interior only) | high (value-level tail selection; necessity unproved) | high (bounded-transfer rationale is motivation only) |
| mathematical tractability | high (underdetermined) | medium (level selection; `R` uncontrolled) | medium-high (class control; still needs Phase F gates) |
