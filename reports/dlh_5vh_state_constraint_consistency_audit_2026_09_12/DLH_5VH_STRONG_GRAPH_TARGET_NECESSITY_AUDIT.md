# DLH-5V-H — Strong-Graph-Target Necessity Audit (Micro-Rev Rev 1)

**Sequence step C of Issue #56; Micro-Rev tasks C and F.** Question: is the Issue-#55 raw Kuratowski admissible-drift-set graph target *genuinely necessary* for state-constraint HJB scheme convergence, *merely sufficient / over-strong*, or *unanswered and needing a project-specific lemma*? Issue #55's Outcome C remains accepted under the target it was assigned; this audit answers the distinct necessity question. The Micro-Rev restates the operator-level argument in the control/payoff formulation (no geometry-only inference) and corrects the counterexample drift units.

---

## 1. The Issue-#55 raw graph target (recalled exactly, not revised)

For the fixed-aspect refinement family (m = 1, 2, …; da_m = 10/(19m), db_m = 7/(19m); N_m = ⌊19m(W_max + 2)⌋), let A_m(s) ⊆ R² be the set of drifts representable at grid state s by nonnegative rates (physical units), with the sector/cone laws of the frozen process. The Issue-#55 target (as assigned) required, for **every** convergent state sequence s_m → x_* ∈ D_W:

```text
(raw outer / limsup)   limsup_m A_m(s_m)  ⊆  T_D(x_*)          (Kuratowski upper limit)
(raw recovery / liminf)  every μ ∈ T_D(x_*) is a limit of admissible μ_m ∈ A_m(s_m)   (recovery)
```

Issue #55 Outcome C proved (accepted): no per-state buffer rule satisfies both the outer/limsup and recovery/liminf conditions on the counterexample and recovery families.

## 2. The trichotomy — answer

**Answer: option (2) — sufficient but over-strong. The raw graph target is NOT necessary for the operator-consistency components of state-constraint HJB scheme convergence.** Two independent arguments:

**(i) The convergence machinery never uses the raw graph condition.** The Barles–Souganidis half-relaxed-limit framework (provenance in the capsule) requires: monotonicity (order-preservation in the scaled Bellman form — see the frozen-process report §D.1), stability (max-principle bound), operator/test-function consistency, and comparison for the limit problem. The consistency hypothesis is a statement about the *scheme operator applied to smooth test functions* at the states visited by the half-relaxed-limit sequences — not a Kuratowski statement about admissible-drift sets. The state-constraint boundary enters through the one-sided subsolution test on the closure (Soner form, continuous-target report §2), again a test-function/operator object.

**(ii) Toy falsification of necessity.** The 1D toy discriminator (frozen-process report §Part F) is a monotone scheme with interior grid points near the constrained boundary that admit outward drift (raw graph failure) yet satisfies all operator-consistency components — with its elementary boundary inequality verified in both half-relaxed-limit branches. A necessary condition cannot fail on such a scheme; the toy therefore falsifies necessity directly. No project-specific lemma is required for the necessity answer.

## 3. Operator-level restatement (Task C — no geometry-only inference)

The legitimate object is not the geometric jump cone but the **discrete Bellman Hamiltonian** — the max over candidates of {running payoff + drift score}. The boundary consistency test at a boundary point x̂ is:

**For every test function φ touching a candidate subsolution from above at x̂, along the half-relaxed-limit near-maximizer sequences: `limsup S_m(s_m, φ) ≤ 0`** — equivalently `ρφ(x̂) ≤ H_lim(x̂, Dφ(x̂))` where H_lim is the limit of the discrete Hamiltonians at the visited states (derivation in the frozen-process report §D.2).

- If the maximizer sequence visits **interior states**: H_lim = H_proj (unrestricted sup over candidates with their payoffs and drifts) — the inequality is `ρV ≤ H_proj`, which is exactly the Soner-form subsolution on the closure (continuous-target report §2.2) — **holds by the continuous authority**.
- If the maximizer sequence visits **W-contact states**: H_lim = H_R (the limit of the discrete Hamiltonians at the W-contact candidates). The transfer `ρV ≤ H_R` requires the constrained characterization `ρV ≤ H_T` combined with the control-level bridge `liminf H_R ≥ H_T`. The **control-level bridge is proved** (frozen-process report §E.4: every viable control's payoff and drift are represented at the W-contact cells, so `liminf H_R ≥ H_T` as a statement about the discrete operators). The **constrained characterization `ρV ≤ H_T` is the single bounded gap** (Outcome B): it is PLAUSIBLE-BUT-NOT-YET-PROVED under project hypotheses.

**Consequence:** the raw Issue-#55 graph condition is over-strong for the operator-consistency components; the remaining obstruction to the full boundary transfer is the Outcome-B gap (constrained characterization + comparison), which is a *different* object from the raw graph condition and is not what Issue #55 proved.

## 4. Re-test of the Issue-#55 sequences under the operator target (Task F — drift corrected)

1. `s_m = (0, i_t^m(0) − 2), μ = (0, 1)` → corner (0, W_max):
   - The state is interior (non-W-active; `i ≤ i_t − 2`). Its own tangent cone is the a=0 face law {μ_a ≥ 0}; the frozen process represents exactly cone{w_right, w_up, w_down} = {μ_a ≥ 0}.
   - The drift is admitted: μ_a = 0 ≥ 0. **Physical drift units: μ_W = μ_a + μ_b = 0 + 1 = 1** (the jump w_up = (0, 7/(19m)) with rate q_up = 19m/7 gives first moment q_up·w_up = (0, 1); jump size and physical drift are distinct objects — the earlier `7/19` is a unit error, corrected here).
   - Interior operator consistency at s_m: for φ ∈ C², `S_m(s_m, φ) → ρφ(x̂) − H_{μ_a≥0}(x̂, Dφ(x̂))` with O(1/m) remainder (second-moment bound). The state's own cone {μ_a ≥ 0} is the correct a=0-face law at its own position; the raw graph failure (μ_W = 1 > 0 at the corner limit) is immaterial to this operator statement.
   - The boundary subsolution at the corner via *interior* maximizer sequences holds by the Soner authority (ρV ≤ H_proj); via *W-contact* maximizer sequences it is gated by the Outcome-B gap (ρV ≤ H_T, unproved). **The raw graph test is violated; the operator-consistency components are not.**
2. Upper-corner analogue `s_m = (19m, i_t^m(19m) − 2), μ = (−1, 2)` (μ_W = 1): same structure — interior state, own cone {μ_a ≤ 0} (a_max face law); operator-consistent; raw graph test violated; boundary transfer gated by the same gap.
3. Raw graph verdict (accepted #55, unchanged): both sequences violate the raw outer/limsup condition. This confirms the raw target and the operator target are genuinely different objects.

## 5. Relation to the accepted Issue-#55 result (no silent revision)

- Issue #55 remains accepted under its exact raw graph target; nothing here revises it.
- This audit answers the distinct necessity question: the raw target is **over-strong** (sufficient, not necessary) for the operator-consistency components — established by the structural argument and the toy.
- The frozen process's operator-consistency components are verified in the frozen-process report (§E); the boundary subsolution transfer has the single bounded gap declared as Outcome B.

## 6. Conclusion

The raw graph target is sufficient but over-strong (trichotomy option 2). The legitimate target is the operator/test-function consistency target of step D; the frozen process passes its consistency components; the boundary subsolution transfer at the W-corners is gated by the single bounded Outcome-B gap (constrained characterization ρV ≤ H_T + comparison), which the Micro-Rev declares explicitly rather than carrying forward.
