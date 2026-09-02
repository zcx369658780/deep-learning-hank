# DLH-5P Phase D — P-TR Derivability Audit (Rev 2)

**Issue #42 Phase D (Rev 2).** Determines, separately for each candidate S1/S2/S3,
whether the central derivative-control object

```text
R(b,a,z) = V_a / V_b,   P-TR: R = o(sqrt(b)) uniformly over (a,z),
```

is derivable from the candidate specification, an admissibility assumption, implied
only by a stronger condition such as `R = O(1)`, unsupported/circular, or falsifiable
by an allowed alternative value expansion. Rev 2 removes the claim that P-TR is
"partially derived" via the (withdrawn) critical-branch ruling-out: P-TR is an
explicit Owner-adopted admissibility primitive under S3 and an additional condition
under S1/S2.

## D0. What P-TR controls

- `R = o(sqrt(b))` uniformly implies `d = o(sqrt(b))`, `chi = o(b)`, `mu_a =
  o(sqrt(b))` (the combined transfer Hamiltonian is then `o(1/b)`, subleading at the
  `O(1/b)` coefficient balance). (DLH-5O annotation A: the stronger `R=O(1)` gives
  `d=O(1)`, `chi=O(1)`, `mu_a=O(1)`.)
- The `O(1/b)` balance `(rho+r_b)K - 2 sqrt(K) = S*K` and the coefficient
  `c/b = (rho+r_b)/2` hold only under P-TR (or a stronger control).
- Conversely, WITHOUT P-TR the `m=1/2` branch (Phase E Rev 2) is admissible on the
  compact interior and alters the coefficient to `(rho+r_b - 0.5 C(z)/chi_1)/2`
  (a continuum). P-TR is therefore precisely the restriction that removes that family.

## D1. Under S1 (minimal growth/admissibility)

- **Derivable?** NO. S1 imposes only a growth class and no tail selection law; `R` is
  uncontrolled by S1.
- **Admissibility assumption?** Not part of S1's class.
- **Implied by a stronger condition?** No stronger condition is present in S1.
- **Unsupported / circular?** Not circular (S1 does not select `p=2`), but P-TR is
  simply not implied — it is an extra condition needed beyond S1.
- **Falsifiable?** YES: an S1-admissible smooth solution with `R` not `o(sqrt(b))`
  (e.g. the `m=1/2` family of Phase E) that is balance-consistent would be an allowed
  alternative expansion. Phase E shows such a family IS balance-consistent on the
  compact interior, so it is a live counterexample class to P-TR as a claim about S1.

**Status under S1: NOT DERIVABLE; NOT ASSUMED; an additional condition required for the
`p=2` coefficient.**

## D2. Under S2 (transversality / no-Ponzi)

- **Derivable?** NO. S2's proposed verification/selection condition
  `e^{-rho T} E[V] -> 0` controls the value **level** (the tail integration constant /
  exploding-value branches) and does not control the **ratio** `R = V_a/V_b`. The
  `m=1/2`/`p=2` remainder family (`V ~ -K/b - (2/3)M b^{-3/2}`) has bounded growth and
  can satisfy `e^{-rho T} E[V] -> 0` for suitable admissible paths (e.g. `b_T`
  growing at rate `< 2 rho`), so S2 does not exclude it.
- **Admissibility assumption?** Not part of S2's condition.
- **Implied by a stronger condition?** Only if one adds a derivative-control condition
  (which is exactly S3).
- **Unsupported / circular?** Not circular, but not implied.
- **Falsifiable?** YES: an S2-admissible solution satisfying the verification condition
  with `R` not `o(sqrt(b))` that is balance-consistent would falsify P-TR as a claim
  about the S2 solution set. The `m=1/2` family is a candidate for exactly this.

**Status under S2: NOT DERIVABLE; NOT ASSUMED; an extra condition.**

## D3. Under S3 (derivative-controlled admissibility)

- **Derivable?** As a theorem from the S3 class alone: NO. As a consequence of the
  withdrawn ruling-out: **NO** (Phase E Rev 2 removes the only "partial derivation"
  claim; the `m=1/2` branch is not excluded by the balance).
- **Admissibility assumption?** YES — P-TR (preferably `R=O(1)`) is the defining
  restriction of the S3 class, an **explicit Owner-adopted admissibility primitive**
  (new model definition, Phase A A21 elevated by the Owner).
- **Implied by a stronger condition?** YES: `R=O(1)` implies P-TR (the preferred,
  cleaner subcase).
- **Unsupported / circular?** The circularity risk is explicit: the class excludes
  exactly the `m=1/2` family that would alter the coefficient, so the `p=2` result is
  **imposed by the primitive**, not derived. This is acceptable as an Owner-adopted
  primitive but must not be presented as an independent justification. The class does
  not force `R=0` or the exact transfer values; those require further structure.
- **Falsifiable?** YES: (i) a constructed S3-admissible solution with `R=O(1)` and a
  non-`p=2` tail falsifies the coefficient theorem; (ii) evidence that the actual HJB
  solution has `R` not `o(sqrt(b))` (e.g., future finite-grid measurement of `V_a/V_b`
  near `b_max` under the accepted source) falsifies the class; (iii) a
  balance-consistent construction of the `m=1/2` family that also satisfies S2's
  verification condition demonstrates the exclusionary cost of the primitive.

**Status under S3: OWNER-ADOPTED ADMISSIBILITY PRIMITIVE (explicit); not derived; not
independently justified by a ruling-out; implied by the stronger `R=O(1)`; explicit
circularity (exclusion by class); falsifiable.**

## D4. Summary (Rev 2)

| Candidate | P-TR derivable? | P-TR assumed? | implied by stronger? | circular? | falsifiable? |
|---|---|---|---|---|---|
| S1 | NO | NO | NO | no (not selected) | yes (m=1/2 family is a live counterexample class) |
| S2 | NO (verification condition does not control `R`) | NO | only via S3 | no | yes |
| S3 | NO (withdrawn partial-derivation) | YES — Owner-adopted primitive | YES (`R=O(1)`) | explicit: exclusion by class, not balance | yes |

**Bottom line:** P-TR is an **explicit Owner-adopted admissibility primitive** (S3),
NOT a derived theorem under any candidate and NOT independently justified by any
critical-branch exclusion (the exclusion is withdrawn). The `m=1/2` family is a live,
balance-consistent alternative on the compact interior that P-TR excludes by class.
The Owner may adopt `R=O(1)` (stronger, cleaner) or P-TR (weaker) as the primitive;
both are falsifiable, and the exclusionary cost is now explicit.
