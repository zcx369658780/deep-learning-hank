# DLH-5P Phase D — P-TR Derivability Audit

**Issue #42 Phase D.** Determines, separately for each candidate S1/S2/S3, whether the
central derivative-control object

```text
R(b,a,z) = V_a / V_b,   P-TR: R = o(sqrt(b)) uniformly over (a,z),
```

is derivable from the candidate specification, an admissibility assumption, implied
only by a stronger condition such as `R = O(1)`, unsupported/circular, or falsifiable
by an allowed alternative value expansion. DLH-5P does **not** label P-TR "proved"
merely because it was assumed in DLH-5O.

## D0. What P-TR controls

- `R = o(sqrt(b))` uniformly implies `d = o(sqrt(b))`, `chi = o(b)`, `mu_a =
  o(sqrt(b))` (the combined transfer Hamiltonian is then `o(1/b)`, subleading at the
  `O(1/b)` coefficient balance). (DLH-5O annotation A: the stronger `R=O(1)` gives
  `d=O(1)`, `chi=O(1)`, `mu_a=O(1)`.)
- The `O(1/b)` balance `(rho+r_b)K - 2 sqrt(K) = S*K` and the coefficient
  `c/b = (rho+r_b)/2` hold only under P-TR (or a stronger control).

## D1. Under S1 (minimal growth/admissibility)

- **Derivable?** NO. S1 imposes only a growth class and no tail selection law; `R` is
  uncontrolled by S1.
- **Admissibility assumption?** Not part of S1's class.
- **Implied by a stronger condition?** No stronger condition is present in S1.
- **Unsupported / circular?** Not circular (S1 does not select `p=2`), but P-TR is
  simply not implied — it is an extra condition needed beyond S1.
- **Falsifiable?** YES: an S1-admissible smooth solution with `R` not `o(sqrt(b))`
  (e.g., the `m=1/2` branch, or `R ~ b^m`, `m>=1/2`) that is balance-consistent would
  be an allowed alternative expansion; Phase E shows such power branches are
  inconsistent, which is evidence *for* P-TR but not a theorem of S1.

**Status under S1: NOT DERIVABLE; NOT ASSUMED; an additional condition required for the
`p=2` coefficient.**

## D2. Under S2 (economically mapped transversality/no-Ponzi)

- **Derivable?** NO. The transversality condition `lim e^{-rho T} E[V] = 0` controls
  the value **level** (the constant of integration / explosive branches) and does not
  control the **ratio** `R = V_a/V_b`. The `m=1/2`/`p=1/2` tail, for example, satisfies
  `e^{-rho T} V(b_T) -> 0` for suitable drifts, so transversality does not by itself
  exclude it (it is excluded instead by the Phase E balance, which is independent of
  the transversality law).
- **Admissibility assumption?** Not part of S2's transversality.
- **Implied by a stronger condition?** Only if one adds a derivative-control condition
  (which is exactly S3).
- **Unsupported / circular?** Not circular, but not implied.
- **Falsifiable?** YES: an S2-admissible solution (satisfying transversality) with
  `R` not `o(sqrt(b))` that is balance-consistent would falsify P-TR as a claim about
  the S2 solution set. None is constructed; the power branches are inconsistent
  (Phase E).

**Status under S2: NOT DERIVABLE; NOT ASSUMED; an extra condition.**

## D3. Under S3 (derivative-controlled admissibility)

- **Derivable?** As a theorem from the S3 class alone: NO. As a consequence within the
  smooth dominant-balance class: **PARTIALLY DERIVABLE**. Phase E shows that a smooth,
  uniform, self-consistent dominant balance with the `p=2` value base admits only
  `R = O(1)` or lower for its leading transfer ratio (the `R ~ b^m` power branches with
  `0 < m < 1/2` and the critical `m=1/2` branch are inconsistent; `R ~ b` and `R ~ b^2`
  are inconsistent via the balance). Hence every consistent smooth branch satisfies
  P-TR (indeed `R=O(1)` or lower). What remains uncontrolled is non-power/non-smooth
  `R` (e.g., logarithmic), which is a framework-level gap, not a violation of P-TR
  (`log b = o(sqrt(b))` anyway).
- **Admissibility assumption?** YES — P-TR (preferably `R=O(1)`) is the defining
  restriction of the S3 class. It is an explicit, auditable premise.
- **Implied by a stronger condition?** YES: `R=O(1)` implies P-TR (the preferred,
  cleaner subcase).
- **Unsupported / circular?** NOT circular in the harmful sense: the class admits any
  `R=O(1)` subleading `a`-dependence (it does not force `R=0` or the exact transfer
  values `q=-1`/`d=-0.45a`/`chi=0.2475a`), and the `p=2` coefficient is **derived**
  from the balance, not assumed. The circularity risk is the generic one that the class
  contains the `p=2` candidate; it is mitigated by (i) the Phase E independent
  ruling-out of the critical branch, (ii) the bounded-transfer economic rationale, and
  (iii) falsifiability.
- **Falsifiable?** YES: (i) a constructed S3-admissible solution with `R=O(1)` and a
  non-`p=2` tail falsifies the coefficient theorem; (ii) evidence that the actual HJB
  solution has `R` not `o(sqrt(b))` (e.g., future finite-grid measurement of `V_a/V_b`
  near `b_max` under the accepted source) falsifies the class; (iii) any
  balance-consistent allowed expansion with `R ~ b^m`, `m >= 1/2`, falsifies the
  exclusion.

**Status under S3: ADMISSIBILITY ASSUMPTION (made explicit); partially derived at the
dominant-balance level; implied by the stronger `R=O(1)`; not circular in the harmful
sense; falsifiable.**

## D4. Summary

| Candidate | P-TR derivable? | P-TR assumed? | implied by stronger? | circular? | falsifiable? |
|---|---|---|---|---|---|
| S1 | NO | NO | NO | no (not selected) | yes |
| S2 | NO (transversality does not control `R`) | NO | only via S3 | no | yes |
| S3 | partially at the dominant-balance level; not as a theorem | YES (class definition) | YES (`R=O(1)`) | not in the harmful sense (explicit, derived coefficient, independent ruling-out) | yes |

**Bottom line:** P-TR is an **assumption** (S3) with partial dominant-balance-level
justification (Phase E rules out the power branches that would violate it), NOT a
derived theorem under any candidate. The Owner may adopt `R=O(1)` (stronger, cleaner)
or P-TR (weaker) as the admissibility class; both are falsifiable.
