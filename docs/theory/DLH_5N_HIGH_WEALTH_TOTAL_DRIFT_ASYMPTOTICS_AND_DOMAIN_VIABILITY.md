# DLH-5N / Issue #40 — High-Wealth Total-Drift Asymptotics and Domain Viability

**Task type:** `SCIENTIFIC_THEORY_ANALYSIS__HIGH_WEALTH_TOTAL_DRIFT_ASYMPTOTICS_AND_DOMAIN_VIABILITY`
**Date:** 2026-09-02
**Branch:** `dsh/issue-40-dlh-5n-high-wealth-total-drift-asymptotics-2026-09-02`
**Fresh `origin/main` baseline:** `630df87fef18aa7597a2eedccc2adaba82ec19ff`

This is a **theory/documentation gate only**. No source mutation, no HJB/KFE/grid
run, no stationary operation, no domain choice. It asks whether, under the **currently
accepted household equations** with the illiquid support held at the current finite
range `0 <= a <= a_max = 10` and the accepted `a_max`-normalized taper held fixed,
the model itself implies total-wealth mean reversion (`mu_W < 0`) as
`b -> +infinity` / `W = a + b -> +infinity`, **without** imposing an upper `b`
constraint and **without** choosing `W_max`.

The analysis is intentionally narrower than a full two-asset infinite-domain theorem.
**No claim is made about `a -> infinity`**; `a_max = 10` and the accepted taper remain
an unresolved truncation/modeling boundary (Owner decision U, Issue #39).

---

## 0. Controlling accepted authority and identities

- Issue #39 / DLH-5M accepted at candidate `80cdb7ab2c14bcb7606fc66a0737c28bd3fbb4bb`,
  integrated by merge `69bde2115cdf038e40640ec41d23e0b620167539`; Owner decision
  `ACCEPT_RECOMMENDATION_U__DO_NOT_FREEZE_R_OR_W_YET` (comment `5502482918`).
- Accepted household source (immutable, read-only):
  `src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`
  - blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`
  - SHA-256 `1795718C469FC3B427CAB8E3D5957C133BEAD6EACC9EF0A25A3EDB7211D1A024`
- Frozen D0 configuration (read-only):
  `configs/dlh_5b_two_region_symmetric_anchor.toml` (region index 0),
  `configs/dlh_5l_total_wealth_domain_geometry_diagnostic.toml`.
- Accepted finite-state evidence (read-only, consistency check only):
  `reports/dlh_5l_total_wealth_domain_geometry_diagnostic_2026_09_01/` (105-state set).
- Accepted DLH-5M design package (read-only context):
  `docs/design/DLH_5M_STATE_DOMAIN_AND_JOINT_KKT_DESIGN_REVIEW.md` and
  `reports/dlh_5m_state_domain_joint_kkt_design_review_2026_09_02/`.
- Issue #27 HJB<->KFE same-controlled-process contract remains binding; stationary KFE
  remains NOT AUTHORIZED.

Accepted source accounting identity (implemented source, verified to machine
precision in accepted DLH-5L Phase A):

```text
mu_a = r_a_eff(a)*a + d
mu_b = r_b*b + labor_income - d - chi(d,a) - (consumption - transfer_income)
mu_W = mu_a + mu_b
     = r_a_eff(a)*a + r_b*b + labor_income - chi(d,a) - (consumption - transfer_income)
```

Accepted control objects (frozen D0 values in parentheses):

```text
consumption = V_b^(-1/gamma_c)                      (gamma_c = 2.0)
labor       = (V_b * net_wage / labor_weight)^(1/phi)   (phi = 5.0, labor_weight = 1.0)
net_wage    = wages*(1 - tau - migration_costs)*z   (wages=1.0, tau=0.15, migration_costs=0.0)
labor_income = wages*(1 - tau - migration_costs)*z*labor
d           = transfer_candidate(V_a,V_b,a) = a * T(q) / chi_1,
              T(q) = min(q + chi_0, 0) + max(q - chi_0, 0),  q = V_a/V_b - 1
              (chi_0 = 0.1, chi_1 = 2.0; bare `a` per MATLAB-faithful formula)
chi(d,a)    = chi_0*|d| + 0.5*chi_1*d^2 / max(a, a_bar)    (a_bar = 1e-6)
r_a_eff(a)  = r_a*(1 - 0.1*(a/a_max)^9)             (r_a = 0.03, a_max = 10)
r_b         = 0.015
transfer_income = 0.0   (frozen fixture, region index 0; state-independent scalar)
z           in {0.8, 1.3}, Poisson switch rate 1/3 (deterministic mu_z=sigma_z=0)
```

The fixed `transfer_income` term is preserved in the identity and identified
separately; in the frozen fixture it is exactly `0.0`, so
`mu_W = r_a_eff(a)*a + r_b*b + labor_income - chi(d,a) - consumption` numerically.

---

## 1. Scientific question (restated narrowly)

> Does the accepted household structure itself imply total-wealth mean reversion
> (`mu_W < 0`) in the fixed-`a` liquid tail `b -> +infinity`, or is the sign of
> `mu_W` asymptotically conditional/undetermined because the growth of optimal
> consumption, labor, transfer, or value derivatives has not been established?

Fixed scope: `a in [0, 10]` (finite, compact), `z in {0.8, 1.3}` (finite Markov),
`b -> +infinity`, `W = a + b -> +infinity`. No upper `b` constraint, no `W_max`.

---

## 2. Result of the analysis (executive summary)

1. **One and only one term of `mu_W` is an unconditional, provably positive and
   linearly growing source object:** `r_b*b` with `r_b = 0.015 > 0` (frozen).
2. **`r_a_eff(a)*a` is provably bounded and non-negative** on `[0,10]` (maximum
   `0.27` at `a = 10`), so it can never offset a positive `r_b*b` tail.
3. **Every other term is conditional on the asymptotic behavior of endogenous
   objects** (at least `V_b`, and through it consumption and labor, and `V_a/V_b`,
   through it the transfer and adjustment cost). Accepted authority does not
   determine these asymptotics; no HJB tail theorem is accepted.
4. **Hence no unconditional inwardness theorem is provable** (Outcome A fails). The
   sign of `mu_W` in the fixed-`a` liquid tail is **conditional**: inward iff the
   consumption channel (net of labor income and adjustment cost) dominates `r_b*b`
   eventually; outward in a source-formula-consistent family with slowly decaying
   `V_b`.
5. **The single most important missing object is the tail decay rate of `V_b`
   (equivalently the asymptotic consumption-wealth ratio `c/b`)**, together with the
   tail behavior of `V_a/V_b` (which drives the transfer and adjustment cost).
6. **The terminal is Outcome B:**
   `DLH_5N_FIXED_A_LIQUID_TAIL_TOTAL_WEALTH_SIGN_CONDITIONAL__MISSING_CONTROL_ASYMPTOTICS_IDENTIFIED`.

Detailed derivations are in the report files:

- `DLH_5N_SOURCE_ASYMPTOTIC_OBJECTS.md` — Phase A source-object audit.
- `DLH_5N_ASYMPTOTIC_TERM_ORDER_TABLE.md` — Phase B term-order table.
- `DLH_5N_CONTROL_GROWTH_ASSUMPTION_AUDIT.md` — Phase C control/value-derivative audit.
- `DLH_5N_THEOREM_AND_COUNTEREXAMPLE_MATRIX.md` — Phase D theorem/conditional/
  counterexample matrix.
- `DLH_5N_DOMAIN_VIABILITY_IMPLICATIONS.md` — Phase F domain-viability implications.
- `DLH_5N_SCIENTIFIC_TERMINAL.md` — exact pre-registered terminal.

---

## 3. Why the sign is conditional (the argument in one paragraph)

`mu_W = r_b*b + [r_a_eff(a)*a + labor_income + transfer_income] - [chi(d,a) + consumption]`.
The bracketed first group is `O(1)` or `o(b)` (bounded `a`-term, bounded
`transfer_income`, and `labor_income = O(V_b^{1/phi})` which decays if `V_b -> 0`);
the second group is controlled by `consumption = V_b^{-1/gamma_c}` and
`chi = O(|d| + d^2/max(a,a_bar))` with `d = O(a*T(V_a/V_b - 1))`. For `mu_W < 0` in
the tail, the household must consume (net of labor income and adjustment cost) at a
rate that eventually exceeds `r_b*b + O(1)`, i.e. the asymptotic consumption-wealth
ratio must be bounded below by `r_b`. Whether this holds is a property of the HJB
solution's tail — the decay exponent of `V_b` — which the accepted source does not
characterize. A slowly decaying `V_b` (faster than `b^{-2}` decay is required for
inwardness; slower gives outwardness under bounded transfer). No such rate is
established by accepted authority.

---

## 4. Fixed-`a` liquid tail vs full two-asset infinite-domain theorem

The analysis here concerns `b -> +infinity` with `a` held in the accepted finite
range `[0,10]`. It is a **liquid-tail** result in the sense of a one-dimensional
liquid-wealth tail on a bounded illiquid support. It is **not** a full two-asset
infinite-domain theorem:

- `a_max = 10` is a finite computational support with the accepted taper
  `r_a_eff(a) = r_a*(1 - 0.1*(a/a_max)^9)`; no `a -> +infinity` authority exists.
- The taper is normalized by `a_max` and is NOT extrapolated beyond `a_max = 10` as
  scientific authority anywhere in this analysis.
- A full two-asset infinite-domain theorem would require characterizing `V_a`, `V_b`
  and their cross-effects as both coordinates tend to infinity — strictly harder and
  explicitly outside DLH-5N scope.

Consequently even a future positive conditional result here (e.g. the sufficient
condition in Phase D) would justify at most a "liquid-tail mean-reversion" statement,
not a two-asset theorem, and would still not authorize `W_max` or a domain change.

---

## 5. Finite-state consistency (read-only; not evidence of the tail)

Accepted DLH-5L evidence (105-state pre-frozen set, `b` up to the `b160` ceiling
`~56.58`): all 105 inspected states have `mu_W <= 0`; the 44 material positive-`mu_b`
states are all `B_OUTWARD__TOTAL_INWARD`; the 17 top-layer offenders satisfy
`mu_a <= 0` and `mu_W <= 0`; cross-`a` `rel_diff_mu_W` exceeds the pre-registered
`1e-2` threshold on 16/24 aligned pairs.

Consistency reading for this theory gate:

- At the highest inspected `b` (`b ~ 56.58`), `r_b*b ~ 0.849` while `|mu_W| ~ 0.10-0.17`,
  so on the sampled states the negative term
  `(consumption - labor_income + chi - transfer_income)` already dominates
  `r_b*b + r_a_eff(a)*a`. This is **consistent with** the mean-reversion scenario
  `c/b > r_b` at moderate `b`, but:
- it does **not** prove the asymptotic rate; the inspected range is far short of the
  asymptotic regime, the states are concentrated at high `a` and `z = 1`/`1.3`, and
  the cross-`a` total-drift sensitivity indicates the total drift is not even
  numerically stable across mature `a`-lattices.
- The finite-state evidence is used **only** as a consistency check, exactly as
  Issue #40 §5 requires; no J0-J5 rerun and no new numerical states are made.

---

## 6. Narrow implications for unresolved R/W domain viability

See `DLH_5N_DOMAIN_VIABILITY_IMPLICATIONS.md` for the full table. Summary:

- **Design W** requires total-wealth mean reversion in the tail to be a coherent
  truncation hypothesis. Current theory authority **does not establish** the
  fixed-`a` liquid-tail sign (Outcome B). W therefore remains a plausible hypothesis,
  not a theory-established domain; the missing object is the `V_b` tail decay /
  `V_a/V_b` tail behavior (Route N-B deeper HJB/value-function asymptotic gate).
- **Design R** receives no new support: the analysis does not establish R's
  componentwise law, and the truncation-vanishing argument remains absent.
- **No `W_max`, no `R`/`W`/`W1`/`W2` choice, no new `b_max`/`a_max`** is authorized
  or made.

---

## 7. What is explicitly NOT claimed

- NOT claimed: `mu_W < 0` for all large `b` (Outcome A is not provable).
- NOT claimed: a counterexample is established at the model level (the formula-level
  non-inward family is conditional and not shown to solve the HJB; see Phase D).
- NOT claimed: any statement about `a -> +infinity`, or any taper behavior beyond
  `a_max = 10`.
- NOT claimed: stationary, density, tail, or aggregate implications (all blocked).
- NOT claimed: R or W is viable or non-viable; the Owner decision U remains
  controlling.

---

## 8. Recommended next gate (not created by Builder)

After fresh ChatGPT review of this candidate: a deeper HJB/value-function asymptotic
theory gate (Route N-B) characterizing the tail decay of `V_b` (equivalently the
asymptotic consumption-wealth ratio `c/b`) and the tail behavior of `V_a/V_b` on the
fixed `a`-support, before any domain/boundary implementation authority. Stationary
KFE remains NOT AUTHORIZED under Issue #27.

No implementation or domain choice is authorized by this Issue.
