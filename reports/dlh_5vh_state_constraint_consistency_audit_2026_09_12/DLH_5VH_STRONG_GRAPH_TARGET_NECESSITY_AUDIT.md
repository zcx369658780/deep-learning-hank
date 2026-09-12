# DLH-5V-H — Strong-Graph-Target Necessity Audit (Micro-Rev Rev 2)

**Sequence step C of Issue #56; Micro-Rev tasks C and F.** Question: is the Issue-#55 raw Kuratowski admissible-drift-set graph target *genuinely necessary* for state-constraint HJB scheme convergence, *merely sufficient / over-strong*, or *unanswered and needing a project-specific lemma*? Issue #55's Outcome C remains accepted under the target it was assigned; this audit answers the distinct necessity question. Rev 2 incorporates the quantifier-corrected half-relaxed-limit algebra (monotone-scheme report §D.2) and the local-state same-candidate recovery lemma (§E.4), and re-scopes the raw-graph claim to exactly the level those support.

---

## 1. The Issue-#55 raw graph target (recalled exactly, not revised)

For the fixed-aspect refinement family (m = 1, 2, …; da_m = 10/(19m), db_m = 7/(19m); N_m = ⌊19m(W_max + 2)⌋), let A_m(s) ⊆ R² be the set of drifts representable at grid state s by nonnegative rates (physical units), with the sector/cone laws of the frozen process. The Issue-#55 target (as assigned) required, for **every** convergent state sequence s_m → x_* ∈ D_W:

```text
(raw outer / limsup)   limsup_m A_m(s_m)  ⊆  T_D(x_*)          (Kuratowski upper limit)
(raw recovery / liminf)  every μ ∈ T_D(x_*) is a limit of admissible μ_m ∈ A_m(s_m)   (recovery)
```

Issue #55 Outcome C proved (accepted): no per-state buffer rule satisfies both the outer/limsup and recovery/liminf conditions on the counterexample and recovery families.

## 2. The trichotomy — answer

**Answer: option (2) — sufficient but over-strong. The raw graph target is NOT necessary for the operator-consistency components of state-constraint HJB scheme convergence.** Two independent arguments, both at the operator level:

**(i) The convergence machinery never uses the raw graph condition.** The Barles–Souganidis half-relaxed-limit framework (provenance in the capsule) requires: monotonicity (order-preservation of the scaled Bellman map — monotone-scheme report §D.1), stability (max-principle), operator/test-function consistency, and comparison for the limit problem. The consistency hypothesis is a statement about the *scheme operator applied to smooth test functions* at the states visited by the half-relaxed-limit sequences — not a Kuratowski statement about admissible-drift sets. The state-constraint boundary enters through the one-sided subsolution test on the closure (Soner form, continuous-target report §2) — again a test-function/operator object.

**(ii) Toy falsification of necessity.** The 1D toy discriminator (monotone-scheme report §Part F) is a monotone scheme with interior grid points near the constrained boundary that admit outward drift (raw graph failure) yet satisfies all operator-consistency components and converges (quantifier-corrected proof; boundary treatment at the boundary node with the exact constrained operator). A necessary condition cannot fail on such a scheme; the toy therefore falsifies necessity directly. No project-specific lemma is required for the necessity answer.

## 3. Operator-level restatement (Rev 2 — corrected transfer chain)

The legitimate object is not the geometric jump cone but the **discrete Bellman Hamiltonian** — the max over candidates of {running payoff + drift score} — and the boundary consistency test is the one-sided subsolution inequality derived in the monotone-scheme report §D.2:

**For every test function φ touching a candidate subsolution from above at x̂, along the half-relaxed-limit near-maximizer sequences: `ρφ(x̂) ≤ H_lim(x̂, Dφ(x̂))`**, where H_lim is the limsup of the discrete Hamiltonians at the visited states. The quantifier-corrected derivation retains the outer max throughout (no per-candidate inference).

**Boundary transfer (both branches, closed without a constrained characterization):**

- **Interior-state branch:** H_lim = H_proj (interior recovery + restriction), so ρφ(x̂) ≤ H_proj(x̂, Dφ) — the Soner-form subsolution on the closure.
- **W-contact-state branch:** H_m(s_m, p) ≤ H_proj(s_m, p) → H_proj(x̂, p) (buffered candidate sets ⊆ full candidate sets; Hausdorff convergence of the feasibility bounds), so ρφ(x̂) ≤ H_lim(x̂, Dφ) ≤ H_proj(x̂, Dφ) — again the Soner-form subsolution.

The recovery-side statement liminf H_R ≥ H_T (the tangent-cone values are attained at the discrete level) is established by the local-state same-candidate recovery lemma (monotone-scheme report §E.4: α_m at the actual states s_m, rates from μ(s_m, α_m), exact first moment, O(1/m) second moment — source-verified drift continuity) and identifies the geometric content of the boundary operators: H_T ≤ liminf H_R ≤ limsup H_R ≤ H_proj at the corners/faces. It is not the load-bearing piece of the transfer.

**Remaining for convergence:** passing from the halves ū (subsolution on the closure w.r.t. H_proj) and u̲ (supersolution in the interior) to u_m → V requires a **comparison/unique-continuation theorem for the project's continuous state-constrained problem** — the single bounded Outcome-B gap (§E.6 of the monotone-scheme report). The constrained characterization ρV ≤ H_T at the boundary is a coupled sublemma of the same block (not established; not needed for the transfer).

**Consequence:** the raw Issue-#55 graph condition is over-strong for the operator-consistency components; the remaining obstruction is the comparison block — a *different* object from the raw graph condition and not what Issue #55 proved.

## 4. Re-test of the Issue-#55 sequences under the operator target (Rev 1 fix retained)

1. `s_m = (0, i_t^m(0) − 2), μ = (0, 1)` → corner (0, W_max):
   - The state is interior (non-W-active; `i ≤ i_t − 2`). Its own tangent cone is the a=0 face law {μ_a ≥ 0}; the frozen process represents exactly cone{w_right, w_up, w_down} = {μ_a ≥ 0}.
   - The drift is admitted: μ_a = 0 ≥ 0. **Physical drift units: μ_W = μ_a + μ_b = 0 + 1 = 1** (the jump w_up = (0, 7/(19m)) with rate q_up = 19m/7 gives first moment q_up·w_up = (0, 1); jump size and physical drift are distinct objects — corrected in Rev 1).
   - Interior operator consistency at s_m: for φ ∈ C², `S_m(s_m, φ) → ρφ(x̂) − H_{μ_a≥0}(x̂, Dφ(x̂))` with O(1/m) remainder. The state's own cone {μ_a ≥ 0} is the correct a=0-face law at its own position; the raw graph failure (μ_W = 1 > 0 at the corner limit) is immaterial to this operator statement.
   - The boundary subsolution at the corner is closed by the §D.2 transfer in both branches (restriction H_lim ≤ H_proj) — no constrained characterization invoked. **The raw graph test is violated; the operator-consistency components are not.**
2. Upper-corner analogue `s_m = (19m, i_t^m(19m) − 2), μ = (−1, 2)` (μ_W = 1): same structure — interior state, own cone {μ_a ≤ 0} (a_max face law); operator-consistent; raw graph test violated; boundary transfer closed by the same argument.
3. Raw graph verdict (accepted #55, unchanged): both sequences violate the raw outer/limsup condition. This confirms the raw target and the operator target are genuinely different objects.

## 5. Relation to the accepted Issue-#55 result (no silent revision)

- Issue #55 remains accepted under its exact raw graph target; nothing here revises it.
- This audit answers the distinct necessity question: the raw target is **over-strong** (sufficient, not necessary) for the operator-consistency components — established by the structural argument (i) and the toy (ii), both at the operator level.
- The frozen process's operator-consistency components are verified in the monotone-scheme report (§E); the boundary subsolution transfer on the closure is closed via the restriction H_lim ≤ H_proj; the single bounded comparison block is declared as Outcome B (§E.6).

## 6. Scope discipline for the raw-graph claim (Rev 2)

The conclusion "the raw graph target is stronger than the operator-consistency object" is asserted **only to the level supported by**: (i) the Barles–Souganidis operator/test-function consistency structure; (ii) the corrected toy discriminator (quantifier-corrected proof, §Part F); (iii) the corrected half-relaxed-limit algebra (§D.2). The unresolved 2D project boundary comparison is NOT used as evidence for the raw-graph claim — the two are independent objects (the raw-graph claim is established; the comparison block is the separate Outcome-B gap).

## 7. Conclusion

The raw graph target is sufficient but over-strong (trichotomy option 2). The legitimate target is the operator/test-function consistency target of step D; the frozen process passes its consistency components (including the local-state same-candidate recovery bridge); the boundary subsolution transfer on the closure is closed via the restriction argument; the single bounded Outcome-B gap is the project-specific state-constraint comparison/unique-continuation application (with the constrained characterization as a coupled sublemma), declared explicitly rather than carried forward.
