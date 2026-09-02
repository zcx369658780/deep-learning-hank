# DLH-5P Phase B — Analytic HJB Specification Candidates (S1/S2/S3) (Rev 2)

**Issue #42 Phase B (Rev 2).** Formulates three candidate specification packages for
the unbounded-positive-`b` analytic HJB problem. They share the same inherited interior
economics (Phase A A1-A8, A12-A13) and differ in how they select/admit the tail
solution. Rev 2 corrects S1 (coherent minimal class; `V -> 0` is explicitly a
tail-selection feature, not an S1 property) and S2 (transversality stated as a proposed
verification/selection condition, not a proved necessity, and not mechanically equated
with an asset no-Ponzi law), and restates S3/P-TR as an Owner-adopted admissibility
primitive rather than an independently-justified exclusion.

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

## CANDIDATE S1 — Minimal growth/admissibility specification (corrected)

- **Exact state space:** `D = (b_lo,+inf) x (0,a_max) x {z}`, endpoints as a subset of
  `cl(D)`.
- **Exact HJB:** the shared interior equation above on `D`; no added tail equation.
- **Lower-`b`/`a` endpoints:** `b_lo`: `V` continuous up to `b_lo` with a given lower
  data law (left to Owner; not the finite-grid closure). `a=0`: `V` continuous;
  `d=0` by the bare-`a` factor; `mu_a(0)=0` (corner). `a_max`: `V` continuous; upper-`a`
  law unspecified in S1.
- **Admissible value class (coherent minimal, corrected):** `V in C(D̄) cap C^1(D)`,
  `V_b > 0`, `V < 0` (CRRA-2), with a **polynomial growth bound**
  `|V(b,a,z)| <= C(1+|b|)^N` for some finite `C,N`. **S1 does NOT force `V -> 0`**;
  the class admits bounded, decaying (`o(1)`), or slowly growing (e.g. `-2K sqrt(b)`)
  negative value functions consistent with the bound. **The decay `V -> 0` is
  explicitly acknowledged as a tail-selection feature** (needed for the `p=2` balance),
  not an S1 property; any claim that uses `V -> 0` must state it as an added selection
  assumption.
- **Transversality/growth:** NONE (S1 is the minimal base; no selection law).
- **Regularity:** `V in C^1` on `D` (for `V_b`, `V_a`, FOCs); `C^2` on the tail for any
  dominant-balance statement, **with an explicit derivative-remainder expansion**
  (Rev 2 rule E0: leading equivalences are not differentiated term-by-term).
- **Uniformity:** all rates uniform over `(a,z)` required for any tail statement
  (assumed or to be proved; not automatic). Full-`[0,10]` vs compact interior-`a`
  statements are kept separate (Phase C).
- **P-TR status:** NOT assumed, NOT derived; `R` uncontrolled by S1. The `m=1/2`
  branch is **admissible/unresolved** under S1 (Phase E Rev 2).
- **Does the `p=2` coefficient follow?** NO from S1 alone: without a tail selection
  law there is a family of solutions (constant of integration free, `V->0` not
  guaranteed), so the `O(1/b)` coefficient equation is not a theorem. `p=2` is only a
  candidate balance.
- **Circularity risk:** none (S1 does not select `p=2`).
- **Falsification:** an S1-admissible solution with a different smooth dominant balance
  (e.g. a `p<2`/`p>2` or the `m=1/2` remainder family) satisfying the interior HJB
  falsifies the claim that `p=2` is the unique tail.
- **Relation to the finite-grid solver:** S1 is the continuous extension of the
  accepted interior economics; the solver's finite-grid closure at `b_max` is NOT used
  as a tail law (no equivalence claimed).

---

## CANDIDATE S2 — Transversality / no-Ponzi specification (corrected)

- **Exact state space:** as S1.
- **Exact HJB:** as S1.
- **Lower-`b`/`a` endpoints:** as S1.
- **Admissible value class:** S1 class + the proposed selection condition below.
- **Transversality/growth (corrected; step 20):** DLH-5P proposes the discounted-value
  verification/selection condition

  ```text
  lim_{T->inf} e^{-rho*T} E[ V(b_T, a_T, z_T) | (b_0,a_0,z_0) ] = 0
  ```

  as a **proposed analytic verification/selection condition** for the value solution of
  this problem. It is **NOT asserted as a proved necessity** of the household's
  optimization (no necessity theorem is claimed here), and it is **NOT mechanically
  equated with an asset-level no-Ponzi law** (e.g. `lim E[e^{-rho T} b_T] >= 0`): the
  two are related through the value function's shape but are distinct statements, and a
  direct asset no-Ponzi condition would itself be new model definition.
  **Admissible-path / integrability requirements:** the condition is required only
  along paths in the admissible set of the underlying control problem — controls
  yielding finite discounted utility, `b_t >= b_lo` a.s. (or the Owner-chosen
  lower-bound law), locally integrable drifts, and for which `E[V(b_T,a_T,z_T)]` is
  defined and finite for all `T`; the limit is taken in the usual real sense. Whether
  S2's condition is actually necessary for THIS problem is **UNRESOLVED** and must be
  established by a comparison/verification theorem before it is used as a necessity.
- **Regularity:** as S1.
- **Uniformity:** as S1.
- **P-TR status:** NOT derived: S2's condition controls the value **level** (the tail
  integration constant / exploding-value branches), not the **ratio**
  `R = V_a/V_b`. The `m=1/2`/`p=2` remainder family has a value
  `V ~ -K/b - (2/3)M b^{-3/2}` with bounded growth and, for suitable admissible paths
  (e.g. `b_T` growing no faster than `e^{mu T}` with `mu < 2 rho`), satisfies
  `e^{-rho T} E[V] -> 0`. So S2 does not exclude the branch by itself.
- **Does the `p=2` coefficient follow?** NO from S2 alone: the condition selects the
  tail constant but does not control `R`; the `O(1/b)` coefficient equation still
  requires P-TR. `p=2` remains conditional.
- **Incremental selection beyond corrected S1:** **partial.** S2 excludes value
  solutions that grow too fast for the discounted value to vanish (e.g. `V ~ +b`,
  `V ~ +sqrt(b)` with `mu_b > 2 rho`), i.e. it pins the tail integration constant; it
  does NOT select among interior-`R` branches. The honest statement: S2 adds a level
  selection law, not an `R` selection.
- **Circularity risk:** low (the condition is not `p=2`-specific), but it must be
  verified, not asserted, as a selection law (no necessity proof is claimed).
- **Falsification:** a constructed S2-admissible smooth solution with
  `e^{-rho T} E[V] -> 0` but a tail `p != 2` (e.g. the `m=1/2` family) satisfying the
  interior HJB falsifies `p=2` uniqueness under S2.
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
- **Transversality/growth:** as S2 (proposed verification/selection condition).
- **Regularity:** as S1 plus the class requires the value-gradient ratio to satisfy the
  derivative-control bound (this is the admissibility content).
- **Uniformity:** the derivative-control bound is UNIFORM over `(a,z)` by definition of
  the class; further rate-uniformity as in S1.
- **P-TR status (corrected; step 21):** P-TR / `R=O(1)` is an **explicit
  Owner-adopted admissibility primitive** (model-definition content). It is NOT
  claimed to be independently justified by a critical-branch ruling-out — that
  ruling-out is withdrawn (Phase E Rev 2), so the exclusion of the `m=1/2` branch is a
  **property of the adopted class**, not of the balance. Justification of the class is
  limited to: (i) it is an explicit, auditable, falsifiable restriction; (ii) the
  bounded-transfer economic rationale is **motivation, not derivation** (the
  adjustment cost penalizes large transfer rates, so a bounded marginal-value ratio is
  a plausible hypothesis — it does not by itself prove `R=O(1)`).
- **Does the `p=2` coefficient follow?** YES, conditional on the adopted class + the
  analytic assumptions: the accepted DLH-5O theorem gives `K = 4/(rho+r_b)^2`,
  `c/b = (rho+r_b)/2 = 0.0175`, `mu_W/b -> -0.0025 < 0`. This is a conditional
  theorem of the candidate, not a theorem of the accepted finite-grid source, and it
  holds **only because the class excludes the `m=1/2` family** — i.e. uniqueness is
  imposed by the primitive, not derived.
- **Circularity risk:** explicit and higher than in Rev 1's framing: the class
  excludes exactly the branch that would alter the coefficient. This is acceptable as
  an **Owner-adopted primitive** (the Owner may impose it), but it is NOT an
  independent derivation of `p=2`. The class does not force `R=0` or the exact
  transfer values (`q=-1`/`d=-0.45a`/`chi=0.2475a`); those remain derived only under
  additional `R->0` structure.
- **Falsification:** (i) a constructed S3-admissible smooth solution with `R=O(1)` and
  a tail `p != 2` satisfying the interior HJB falsifies the coefficient theorem;
  (ii) evidence that the actual HJB solution has `R` not `o(sqrt(b))` (e.g. a future
  finite-grid measurement of `V_a/V_b` near `b_max` under the accepted source)
  falsifies the class; (iii) a balance-consistent construction of the `m=1/2` family
  that also satisfies S2's transversality shows the primitive is exclusionary (a
  scientific cost the Owner must weigh).
- **Relation to the finite-grid solver:** as S1; the class is a candidate model
  primitive, not a solver statement.

---

## B1. Comparison table (Rev 2)

| Item | S1 | S2 | S3 |
|---|---|---|---|
| Tail selection law | none (`V->0` NOT forced) | proposed `e^{-rho T} E[V] -> 0` (verification/selection; not proved necessity) | S2 + derivative-control `R=O(1)` (pref.) / `R=o(sqrt(b))` (min.) |
| `V -> 0` status | not an S1 property (added selection) | selected only if the condition kills growing values | selected (within class, `p=2` balance uses it) |
| P-TR | not assumed/derived | not derived | Owner-adopted admissibility primitive (not independently justified) |
| `p=2` coefficient | does not follow | conditional only | **follows** (conditional on adopted primitive) |
| uniqueness of tail | no (family) | partial (level selected; `R` not) | yes, but imposed by the primitive, not derived |
| circularity risk | none | low | explicit (excludes the `m=1/2` branch by class, not balance) |
| critical `m=1/2` branch | admissible/unresolved | admissible/unresolved | excluded only by the adopted class |
| new model authority | state space + class | + verification condition (needs Owner) | + derivative-control class (needs Owner) |
| economic faithfulness | high (interior only) | high (mapped to own discounting; necessity unproved) | high (bounded-transfer rationale is motivation only) |
| mathematical tractability | high (underdetermined) | medium (level uniqueness via TV, if verified) | medium-high (class control) |
