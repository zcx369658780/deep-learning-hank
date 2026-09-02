# DLH-5P Phase B — Analytic HJB Specification Candidates (S1/S2/S3)

**Issue #42 Phase B.** Formulates three candidate specification packages for the
unbounded-positive-`b` analytic HJB problem. They share the same inherited interior
economics (Phase A A1-A8, A12-A13) and differ in how they select/admit the tail
solution. For each candidate the required template is reported: exact state space,
exact HJB, lower-`b`/`a` endpoint treatment, admissible value class,
transversality/growth, regularity, uniformity, P-TR status, whether the DLH-5O `p=2`
coefficient follows, circularity risk, falsification, and relation to the finite-grid
solver.

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
economics (Phase A A6); this does not affect the `b -> +inf` tail. All candidates
treat the finite-grid closures at `b_lo`, `a=0`, `a_max` as non-analytic (Phase A
A9-A11) and specify endpoint laws explicitly.

---

## CANDIDATE S1 — Minimal growth/admissibility specification

- **Exact state space:** `D = (b_lo,+inf) x (0,a_max) x {z}`, endpoints as a subset of
  `cl(D)`.
- **Exact HJB:** the shared interior equation above on `D`; no added tail equation.
- **Lower-`b`/`a` endpoints:** `b_lo`: `V` continuous up to `b_lo` with a given lower
  data law (left to Owner; not the finite-grid closure). `a=0`: `V` continuous;
  `d=0` by the bare-`a` factor; `mu_a(0)=0` (corner). `a_max`: `V` continuous; upper-`a`
  law unspecified in S1.
- **Admissible value class:** `V in C(D̄)`, `V_b > 0`, `V < 0`, with a growth bound
  `|V(b,a,z)| <= C(1+b)^{-delta}` for some `delta > 0` (so `V -> 0` as `b -> inf` is
  not forced by S1; S1 admits bounded or decaying negative values). Minimal in the
  sense that no tail law is imposed.
- **Transversality/growth:** NONE (S1 is the minimal base; no selection law).
- **Regularity:** `V in C^1` on `D` (for `V_b`, `V_a`, FOCs); `C^2` on the tail for any
  dominant-balance statement (the analytic assumption used by the asymptotics).
- **Uniformity:** all rates uniform over `(a,z)` required for any tail statement
  (assumed or to be proved; not automatic).
- **P-TR status:** NOT assumed, NOT derived; `R` uncontrolled by S1. The `m=1/2`
  branch is excluded only through the smooth dominant-balance argument (Phase E), not
  by S1's class.
- **Does the `p=2` coefficient follow?** NO from S1 alone: without a tail selection
  law there is a family of solutions (constant of integration free), so the `O(1/b)`
  coefficient equation is not a theorem. `p=2` is only a candidate balance.
- **Circularity risk:** none (S1 does not select `p=2`).
- **Falsification:** an S1-admissible solution with a different smooth dominant balance
  (e.g. a `p<2`/`p>2` or non-power tail) satisfying the interior HJB falsifies the
  claim that `p=2` is the unique tail.
- **Relation to the finite-grid solver:** S1 is the continuous extension of the
  accepted interior economics; the solver's finite-grid closure at `b_max` is NOT used
  as a tail law (no equivalence claimed).

---

## CANDIDATE S2 — Economically mapped transversality / no-Ponzi specification

- **Exact state space:** as S1.
- **Exact HJB:** as S1.
- **Lower-`b`/`a` endpoints:** as S1 (endpoint laws specified by Owner; S2 does not
  add endpoint content).
- **Admissible value class:** S1 class + the transversality/no-Ponzi condition below.
- **Transversality/growth (economically mapped, NOT textbook):** the household's
  objective is `E integral_0^inf e^{-rho t} u(c_t,l_t) dt`. The necessary value
  transversality for this discounted objective is

  ```text
  lim_{T->inf} e^{-rho*T} E[ V(b_T, a_T, z_T) | (b_0,a_0,z_0) ] = 0
  ```

  for every admissible path; equivalently the discounted continuation value vanishes at
  infinity. The corresponding no-Ponzi statement is that liquid wealth is not run up
  against a Ponzi scheme: `limsup_T e^{-rho*T} E[V(b_T,...)] >= 0` with the value
  selecting the finite-discounted-value branch. This is mapped to the household's own
  discounting (it is the standard necessary condition of THIS problem, stated
  explicitly, not imported from a representative-agent textbook). Status: a
  `NEW_ANALYTIC_MODEL_DEFINITION_REQUIRES_OWNER` (it selects the value solution's
  integration constant) and simultaneously a `THEOREM_ASSUMPTION_ONLY__NOT_MODEL_PRIMITIVE`
  until the Owner adopts it.
- **Regularity:** as S1.
- **Uniformity:** as S1.
- **P-TR status:** NOT derived from transversality: transversality controls the value
  level/constant, not the ratio `R = V_a/V_b`. P-TR remains an extra condition.
- **Does the `p=2` coefficient follow?** NO from S2 alone: transversality selects the
  tail constant (kills explosive values) but does not control `R`; the `O(1/b)`
  coefficient equation still requires P-TR. `p=2` remains conditional.
- **Circularity risk:** low (transversality is economically mapped and not
  `p=2`-specific).
- **Falsification:** a constructed S2-admissible smooth solution with `e^{-rho T}
  E[V] -> 0` but a tail `p != 2` (satisfying the interior HJB) falsifies `p=2`
  uniqueness; an admissible path with `limsup e^{-rho T} E[V] > 0` violates no-Ponzi
  and is excluded.
- **Relation to the finite-grid solver:** as S1; the solver's `b_max` marginal-utility
  closure is not promoted to this transversality condition.

---

## CANDIDATE S3 — Derivative-controlled admissibility specification

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
- **Transversality/growth:** as S2 (economically mapped no-Ponzi).
- **Regularity:** as S1 plus the class requires the value-gradient ratio to satisfy the
  derivative-control bound (this is the admissibility content).
- **Uniformity:** the derivative-control bound is UNIFORM over `(a,z)` by definition of
  the class; further rate-uniformity as in S1.
- **P-TR status:** ASSUMED as an admissibility premise (part of the class); implied by
  the stronger `R=O(1)`; partially derived at the dominant-balance level — Phase E
  shows all smooth, self-consistent dominant balances with the `p=2` base have
  `R = O(1)` or lower and the critical/sub-root power branches are inconsistent. It is
  NOT "proved" as a theorem.
- **Does the `p=2` coefficient follow?** YES (conditionally on the class + Phase A
  analytic assumptions + the ansatz): the accepted DLH-5O theorem gives
  `K = 4/(rho+r_b)^2`, `c/b = (rho+r_b)/2 = 0.0175`, `mu_W/b -> -0.0025 < 0`. This is
  a conditional theorem of the candidate, not a theorem of the accepted finite-grid
  source.
- **Circularity risk:** MODERATE and made explicit: the class contains the `p=2`
  candidate, so S3 is assumption-driven for the tail family. It is NOT circular in the
  harmful sense because (i) the class admits any `R=O(1)` subleading `a`-dependence
  (it does not force `R=0` or the exact transfer values), (ii) the coefficient is
  derived, not assumed, and (iii) the Phase E ruling-out of the critical branch
  independently justifies excluding `R ~ sqrt(b)`. The bounded-transfer economic
  justification is that adjustment cost penalizes unbounded transfer rates, so a
  bounded consumption-wealth ratio at large `b` corresponds to bounded marginal-value
  ratio.
- **Falsification:** (i) construct an S3-admissible smooth solution with `R=O(1)` and
  a tail `p != 2` satisfying the interior HJB -> falsifies the coefficient theorem;
  (ii) show the actual HJB solution has `R` not `o(sqrt(b))` (e.g. via a future
  finite-grid measurement of `V_a/V_b` near `b_max` under the accepted source) ->
  empirical falsification of the class; (iii) any allowed alternative expansion with
  `R ~ b^m`, `m >= 1/2`, that is balance-consistent falsifies the exclusion.
- **Relation to the finite-grid solver:** as S1; the class is a candidate model
  primitive, not a solver statement.

---

## B1. Comparison table

| Item | S1 | S2 | S3 |
|---|---|---|---|
| Tail selection law | none | `e^{-rho T} E[V] -> 0` (no-Ponzi) | S2 + derivative-control `R=O(1)` (pref.) / `R=o(sqrt(b))` (min.) |
| P-TR | not assumed/derived | not derived | assumed (admissibility); partially derived at dominant-balance level |
| `p=2` coefficient | does not follow | conditional only | **follows** (conditional theorem) |
| uniqueness of tail | no (family) | partial (constant selected) | yes (within class, conditional) |
| circularity risk | none | low | moderate (made explicit) |
| critical `m=1/2` branch | excluded only by Phase E balance | excluded only by Phase E balance | excluded by class + Phase E balance |
| new model authority | state space + class | + transversality | + derivative-control class |
| economic faithfulness | high (interior only) | high (mapped to own discounting) | high (bounded-transfer rationale) |
| mathematical tractability | high (but underdetermined) | medium (uniqueness via TV) | medium-high (class control) |
