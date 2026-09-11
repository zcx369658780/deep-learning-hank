# DLH-5V-H — Strong-Graph-Target Necessity Audit

**Sequence step C of Issue #56.** Question: is the Issue-#55 raw Kuratowski admissible-drift-set graph target *genuinely necessary* for state-constraint HJB scheme convergence, *merely sufficient / over-strong*, or *unanswered by the literature and needing a project-specific lemma*? Issue #55's Outcome C remains accepted under the target it was assigned; this audit answers the distinct necessity question.

---

## 1. The Issue-#55 raw graph target (recalled exactly, not revised)

For the fixed-aspect refinement family (m = 1, 2, …; da_m = 10/(19m), db_m = 7/(19m); N_m = ⌊19m(W_max + 2)⌋), let A_m(s) ⊆ R² be the set of drifts representable at grid state s by nonnegative rates (scaled to physical units), with the sector/cone laws of the frozen process. The Issue-#55 target (as assigned) required, for **every** convergent state sequence s_m → x_* ∈ D_W:

```text
(raw outer / limsup)   limsup_m A_m(s_m)  ⊆  T_D(x_*)          (Kuratowski upper limit)
(raw recovery / liminf)  every μ ∈ T_D(x_*) is a limit of admissible μ_m ∈ A_m(s_m)   (recovery)
```

Issue #55 Outcome C proved (accepted): no per-state buffer rule satisfies both the outer/limsup condition on the counterexample family and the recovery/liminf condition on the recovery family, because the tangent-cone multifunction x ↦ T_D(x) is discontinuous at the boundary; in particular the counterexample `s_m = (0, i_t^m(0) − 2)` with `μ = (0, +1)` has `x_m → (0, W_max)`, the drift is admitted and exactly represented, and `μ_W = +1 > 0` makes the outer/limsup condition fail.

## 2. The trichotomy — answer

**Answer: option (2) — sufficient but over-strong. The raw graph target is NOT necessary for state-constraint HJB viscosity/operator convergence.**

Three independent arguments:

**(i) The convergence machinery never uses the raw graph condition.** The Barles–Souganidis half-relaxed-limit framework (provenance in the capsule) requires: monotonicity, stability, operator/test-function consistency, and comparison for the limit problem. The consistency hypothesis is a statement about the *scheme operator applied to smooth test functions* at the states used by the near-maximizer/near-minimizer sequences — not a statement about the Kuratowski limit of admissible-drift sets. The state-constraint boundary is carried by the one-sided subsolution test on the closure (Soner), i.e. by the operator inequality at boundary-contact states, again a test-function object.

**(ii) Cone-monotonicity makes the raw condition unnecessary (and its failure harmless).** By the cone-monotonicity lemma (continuous-target report §3), an admissible cone R ⊇ T_D(x̂) produces a Hamiltonian H_R ≥ H_T. The one-sided subsolution inequality ρV ≤ H_T implies ρV ≤ H_R, so any interior state whose cone contains the boundary tangent cone is subsolution-safe. The Issue-#55 counterexample cells are interior (non-W-active) states whose own cones are the correct face laws at their own positions — e.g. (0, i_t−2) has cone {μ_a ≥ 0} ⊇ REV = T_D(0, W_max) — so under the legitimate operator test they are interior-consistent, and their presence does not break the boundary subsolution at the corner. The raw condition fails exactly because it demands A_m(s_m) → T_D(x_*) at sequences whose own-position cones legitimately exceed the boundary cone; that demand is not part of any primary consistency condition.

**(iii) Toy falsification of necessity.** The 1D toy discriminator (frozen-process report §5) constructs a monotone scheme with interior grid points approaching the constrained boundary that admit outward drifts (raw graph failure) yet is viscosity-consistent (all legitimate consistency components verified analytically). A necessary condition cannot fail on a convergent scheme; the toy therefore falsifies necessity directly, without needing a project-specific lemma. (A project-specific *demonstration* is used, but no new theorem is required: the viscosity theory already implies the toy is consistent.)

## 3. Why the raw target is nevertheless sufficient

The raw graph target is a strong form of operator consistency: if A_m(s_m) converges to T_D(x_*) in the Kuratowski sense at every convergent sequence (including interior sequences approaching the boundary) and the moment/scaling structure of the frozen process is retained, then for every smooth test function φ the discrete Hamiltonian at s_m converges to H_T(x_*, Dφ(x_*)) — i.e. the operator consistency holds with the constrained Hamiltonian on the closure. The raw condition is therefore sufficient for the operator target. It is stronger than required: the operator target needs the Hamiltonian convergence only along the states the half-relaxed-limit construction actually visits (near-maximizer/near-minimizer sequences), and it tolerates cones ⊇ T_D at interior states.

## 4. Relation to the accepted Issue-#55 result (no silent revision)

- Issue #55 remains accepted: under the exact raw graph target it was assigned, the frozen state family cannot satisfy outer/limsup + recovery/liminf, and the impossibility is robust to any per-state buffer rule. Nothing here revises that.
- This audit answers the *different* question the Owner explicitly left open: whether that target is mathematically necessary. It is not — it is over-strong relative to the legitimate viscosity/operator target.
- Consequently the Issue-#55 obstruction, as a *graph* obstruction, does not by itself block a state-constraint HJB scheme; the legitimate target (step D) is the one the next boundary-HJB scheme-design gate must meet, and the frozen process's consistency components against it are verified in the frozen-process report (step E).

## 5. Explicit re-test of the Issue-#55 sequences under the legitimate target

For the report's completeness (mandatory Issue step 7):

1. `s_m = (0, i_t^m(0) − 2), μ = (0, +1)` → corner (0, W_max):
   - The state is interior (non-W-active; `i ≤ i_t − 2`). Its own tangent cone is the a=0 face law {μ_a ≥ 0}; the frozen process represents exactly cone{w_right, w_up, w_down} = {μ_a ≥ 0}.
   - Interior operator consistency at s_m: for φ ∈ C², the discrete operator satisfies `S_m(s_m, φ) → ρφ(x̂) − H_{μ_a≥0}(x̂, Dφ(x̂))` with O(1/m) remainder (second-moment bound; rates O(m), steps O(1/m)).
   - Since {μ_a ≥ 0} ⊇ REV = T_D(x̂), H_{μ_a≥0} ≥ H_T and the one-sided subsolution inequality `ρV ≤ H_T ≤ H_{μ_a≥0}` holds; the boundary subsolution at the corner transfers. **No violation of the legitimate operator test.**
2. Upper-corner analogue `s_m = (19m, i_t^m(19m) − 2), μ = (−1, +2)` → corner (a_max, W_max − a_max):
   - Same structure: interior state, own cone the a_max face law {μ_a ≤ 0} ⊇ TDEP = T_D(a_max, W_max − a_max); H_{μ_a≤0} ≥ H_T; subsolution-safe. **No violation.**
3. Raw graph verdict (accepted #55, unchanged): both sequences violate the raw outer/limsup condition because the admitted drifts are outward at the corner limit (μ_W > 0 / μ_a < 0 respectively). This confirms the raw target and the operator target are genuinely different objects.

## 6. Conclusion

The Issue-#55 raw graph target is **sufficient but over-strong** (trichotomy option 2). The legitimate target is the viscosity/operator consistency target of step D; step E verifies the frozen process against it; the toy discriminator (step F) confirms the mechanism analytically.
