# DLH-5P Phase D — P-TR Derivability Audit (Rev 4)

**Issue #42 Phase D (Rev 4).** Determines, separately for each candidate S1/S2/S3,
whether the central derivative-control object

```text
R(b,a,z) = V_a / V_b,   P-TR: R = o(sqrt(b)) uniformly over (a,z),
```

is derivable from the candidate specification, an admissibility assumption, implied
only by a stronger condition such as `R = O(1)`, unsupported/circular, or falsifiable
by an allowed alternative value expansion. Rev 2 removed the "partially derived" claim
based on the withdrawn ruling-out; Rev 3 additionally notes that P-TR, even when
adopted (S3), excludes the `m=1/2` branch by class but does **not** by itself prove the
realized HJB tail is `p=2` (the `p=2` coefficient remains conditional on the full
DLH-5O theorem premise set).

## D0. What P-TR controls

- `R = o(sqrt(b))` uniformly implies `d = o(sqrt(b))`, `chi = o(b)`, `mu_a =
  o(sqrt(b))` (the combined transfer Hamiltonian is then `o(1/b)`, subleading at the
  `O(1/b)` coefficient balance). (DLH-5O annotation A: the stronger `R=O(1)` gives
  `d=O(1)`, `chi=O(1)`, `mu_a=O(1)`.)
- The `O(1/b)` balance `(rho+r_b)K - 2 sqrt(K) = S*K` and the coefficient
  `c/b = (rho+r_b)/2` hold only under P-TR (or a stronger control).
- Conversely, WITHOUT P-TR the `m=1/2` branch (Phase E Rev 4) is admissible on the
  compact interior and alters the coefficient to `(rho+r_b + 0.5 C(z)/chi_1)/2`
  (a continuum; the PLUS sign is the Rev 4 correction of the transfer-Hamiltonian
  sign). P-TR is therefore precisely the restriction that removes that family.

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

## D2. Under S2 (tail-value selection; discounted-value condition is vacuous)

- **Derivable?** NO. S2's proposed **tail-value selection** `V_inf(a,z) = 0`
  (`V -> 0` as `b -> +inf`) controls the value **level** and does not control the
  **ratio** `R = V_a/V_b`. The `m=1/2`/`p=2` remainder family (`V ~ -K/b - (2/3)M
  b^{-3/2}`) has `V_inf = 0` and is NOT excluded by S2.
- **The discounted-value condition is vacuous (correction 1):** the previously
  proposed `e^{-rho T} E[V] -> 0` is automatically satisfied by every S1-admissible V
  (bounded), so it is REDUNDANT under S1 and adds no selection; it is withdrawn as a
  selection law (Phase B S2).
- **Admissibility assumption?** The `V_inf = 0` selection is a proposed assumption
  (new model definition / theorem assumption), not a derived necessity, and it does not
  touch `R`.
- **Implied by a stronger condition?** Only if one adds a derivative-control condition
  (which is exactly S3).
- **Unsupported / circular?** Not circular, but not implied.
- **Falsifiable?** YES: an S2-admissible solution satisfying `V_inf = 0` with `R` not
  `o(sqrt(b))` that is balance-consistent would falsify P-TR as a claim about the S2
  solution set. The `m=1/2` family is a candidate for exactly this.

**Status under S2: NOT DERIVABLE; NOT ASSUMED (as a `V_inf=0` selection it is proposed,
not proved); an extra condition.**

## D3. Under S3 (derivative-controlled admissibility)

- **Derivable?** As a theorem from the S3 class alone: NO. From the withdrawn
  ruling-out: NO (Phase E Rev 3 preserves the `m=1/2` branch as unresolved/admissible
  on the compact interior).
- **Admissibility assumption?** YES — P-TR (preferably `R=O(1)`) is the defining
  restriction of the S3 class, an **explicit Owner-adopted admissibility primitive**
  (new model definition, Phase A A21 elevated by the Owner). It excludes the `m=1/2`
  branch **by class**.
- **Does P-TR prove the realized tail is `p=2`?** **NO.** P-TR/`R=O(1)` only removes
  the critical transfer branch (and the analyzed power branches) from the class. The
  `p=2` coefficient is available only **conditional on the full DLH-5O theorem premise
  set** — `p=2` asymptotic realization, no exotic competing regime (e.g. non-power /
  non-smooth tails), realized-balance/uniqueness, and uniformity (Phase F gates).
- **Implied by a stronger condition?** YES: `R=O(1)` implies P-TR (the preferred,
  cleaner subcase).
- **Unsupported / circular?** The circularity risk is explicit: the class excludes
  exactly the `m=1/2` family that would alter the coefficient, so the `p=2` result is
  **imposed by the primitive**, not derived. Acceptable as an Owner-adopted primitive,
  but not an independent justification.
- **Falsifiable?** YES: (i) a constructed S3-admissible solution with `R=O(1)` and a
  non-`p=2` tail falsifies the coefficient theorem; (ii) evidence that the actual HJB
  solution has `R` not `o(sqrt(b))` (e.g., future finite-grid measurement of `V_a/V_b`
  near `b_max` under the accepted source) falsifies the class; (iii) a
  balance-consistent construction of the `m=1/2` family that also satisfies S2's
  `V_inf = 0` selection demonstrates the exclusionary cost of the primitive.

**Status under S3: OWNER-ADOPTED ADMISSIBILITY PRIMITIVE (explicit); not derived; not
independently justified by a ruling-out; excludes `m=1/2` by class but does NOT prove
the realized tail is `p=2`; implied by the stronger `R=O(1)`; explicit circularity
(exclusion by class); falsifiable.**

## D4. Summary (Rev 3)

| Candidate | P-TR derivable? | P-TR assumed? | implied by stronger? | circular? | falsifiable? |
|---|---|---|---|---|---|
| S1 | NO | NO | NO | no (not selected) | yes (m=1/2 family is a live counterexample class) |
| S2 | NO (`V_inf=0` selection does not control `R`; discounted-value condition is VACUOUS under S1) | NO (proposed selection, not proved) | only via S3 | no | yes |
| S3 | NO | YES — Owner-adopted primitive | YES (`R=O(1)`) | explicit: exclusion by class, not balance | yes |

**Bottom line:** P-TR is an **explicit Owner-adopted admissibility primitive** (S3),
NOT a derived theorem under any candidate and NOT independently justified by any
critical-branch exclusion (withdrawn). It excludes the `m=1/2` branch by class but does
NOT prove the realized HJB tail is `p=2` (conditional on the full DLH-5O premise set,
Phase F). The `m=1/2` family is a live, balance-consistent alternative on the compact
interior (with inward `mu_W/b = -0.0025 - 3C/(4 chi_1) < 0`, Rev 4) that P-TR excludes
by class. The Owner may adopt `R=O(1)` (stronger, cleaner) or P-TR (weaker) as the
primitive; both are falsifiable, and the exclusionary cost is explicit.
