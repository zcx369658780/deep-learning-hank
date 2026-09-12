# DLH-5V-H — State-Constraint HJB Boundary-Consistency Target Audit (Micro-Rev Rev 1)

**Issue #56** — `SCIENTIFIC_THEORY_AUDIT__STATE_CONSTRAINT_HJB_BOUNDARY_CONSISTENCY_TARGET`
**Owner route:** `APPROVE_DLH_5VH_ROUTE_E_STATE_CONSTRAINT_HJB_CONSISTENCY_TARGET_AUDIT`
**Branch:** `dsh/issue-56-dlh-5vh-state-constraint-consistency-audit-2026-09-12`
**Micro-Rev:** Reviewer comment `5641997550` (Outcome A NOT accepted; bounded same-Issue revision). Revision commit on top of `bc281a693b2d9281b6e180bc62996d503dfab7fe`.
**Date:** 2026-09-12

This is the umbrella record of the DLH-5V-H audit after the bounded Micro-Rev. It summarizes the theory-first sequence (A → B → C → D → E → F) with the Micro-Rev repairs and states the terminal. Detailed arguments live in the five companion reports (links below).

---

## 1. Scope and authority

The audit reopens only the mathematical consistency/convergence target used to judge the discrete scheme; the Micro-Rev repairs six Reviewer findings without rewriting the gate. Consumed, not revised: household economics, finite-domain geometry, Issue-#54 lattice obstruction, Issue-#55 Outcome C. Fresh main `5d38c644ec1a06359241f9c3418dcd815c938ec6`; Issue #56 OPEN; activation comments `5641527846` / `5641534701`; Reviewer `5641997550`; household blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`. Theory/design only; stationary KFE NOT AUTHORIZED.

## 2. Sequence results (Micro-Rev level)

### A. Continuous state-constraint HJB target (report 2)

Frozen continuous object: `ρV = sup{u(c) − v_l·l + V_a μ_a + V_b μ_b}` on `D_W`, `F(x,r,p) = ρr − H(x,p)`.

- **Sign mapping (Task A, fully derived):** Soner Part I uses the minimization value v, `H_S(x,p) = sup{−b·p − f}`, `G_S = ρv + H_S = 0`, constrained solution = subsolution in the OPEN domain / supersolution on the CLOSED domain (Definition 2.1/Theorem 2.1, locations verified by Reviewer `5641997550`). With `V = −v`, `f = −g`, `b = μ`: `G_S(x,−V,−p) = −F_proj(x,V,p)`; Soner's open-domain subsolution becomes the project's open-domain supersolution and Soner's closed-domain supersolution becomes the project's closed-domain subsolution — the project orientation "subsolution on closure / supersolution in interior" is the derived transform, no sign-by-analogy.
- **Boundary semantics:** (a) Soner one-sided form = THE continuous authority (subsolution on the closure with the unrestricted H); (b) `H_T` = DOWNGRADED auxiliary object (no equivalence claim; two separately justified uses: geometric labels of the frozen face laws, and the limit of the control-level bridge for the discrete operators); (c) relaxed operators from cones ⊇ T_D at the limit.
- Load-bearing lemma (retained): the Hamiltonian is monotone in the admissible cone (H_C ≤ H_{C′} for C ⊆ C′) — used only where separately justified.

### B. Primary-theory provenance (report 1)

Soner (1986) I (`24(3):552–561`, DOI `10.1137/0324032`), Soner (1986) II (`24(6):1110–1122`, DOI `10.1137/0324067`), Barles–Souganidis (1991) (`Asymptotic Analysis 4(3):271–283`, DOI `10.3233/ASY-1991-4305`), supporting Capuzzo-Dolcetta–Lions (1990) and Bardi–Capuzzo-Dolcetta (1997, Ch. IV). Every load-bearing statement is labeled PRIMARY THEOREM / PROJECT-SPECIFIC DERIVATION / PLAUSIBLE-BUT-NOT-YET-PROVED; no memory-only theorem-name invocation; no copyrighted material.

### C. Necessity audit of the Issue-#55 raw graph target (report 3)

**Trichotomy answer: option (2) — sufficient but over-strong.** Not necessary for the operator-consistency components: (i) the convergence machinery operates on operator/test-function consistency, never on drift-set graph limits; (ii) the 1D toy falsifies necessity by construction. The boundary transfer at the W-corners via W-contact maximizer sequences additionally needs the constrained characterization `ρV ≤ H_T` — the declared Outcome-B gap (a different object from the raw graph condition).

### D. Weakest defensible numerical target (report 5)

Discrete Bellman in residual and scaled forms; **corrected monotonicity (Task D):** positive diagonal ρ + Σq, nonpositive off-diagonals −q, order-preservation of the scaled operator with nonnegative weights and contraction modulus < 1; NO `ρ ≥ Σq`; stability via max-principle `|u_m| ≤ ‖g‖∞/ρ`; interior consistency (C² test functions, O(1/m) remainder); one-sided boundary consistency via the control/payoff-level bridge `liminf H_R ≥ H_T`; half-relaxed-limit derivation in the fixed convention (ū subsolution w.r.t. H_lim; the near-maximizer argument displayed step by step); comparison hypothesis (Outcome-B gap for the project).

### E. Frozen-process test (report 5)

1. `s_m = (0, i_t^m(0) − 2), μ = (0, 1)` with **μ_W = 1** (Task F): violates only the raw graph test; operator-consistent at the interior state (own cone {μ_a ≥ 0}); boundary transfer gated by the Outcome-B gap.
2. Upper-corner analogue `(19m, i_t^m(19m) − 2), μ = (−1, 2)`: same conclusion.
3. Interior states approaching a boundary may remain interior-consistent without admissible set = boundary tangent cone: YES (one-sided structure + toy).
4. Actual W-contact states: **control/payoff-level bridge (Task C)** — for every viable control at each W-corner, the frozen W-contact candidates represent the SAME payoff with EXACT first moment and O(1/m) second moment (REV at the lower corner: q_RT = 19mμ_a/70, q_down = 19m(−μ_W)/7; TDEP at the upper corner: two-case Case-U contract) — hence `liminf H_R ≥ H_T`. Frozen-taxonomy re-verification (Task E): endpoint layers j ∈ {0,…,6} and j ∈ {19m−6,…,19m}, regular region 7 ≤ j ≤ 19m−7, per-cell limit-corner logic — **0 violations** (m ≤ 25, W_max ∈ {8,10,12}); proportional regions relabeled physical limit-region partitions.
5. Issue-54 obstruction does not damage the bridge at the W-corners: the missing orientations are outside the corner tangent cones (w_T ∉ REV since μ_a < 0; w_RT ∉ TDEP since μ_a > 0).

### F. Toy discriminator (report 5)

1D state-constraint toy with the full component proof (definition, order-preserving monotonicity, max-principle stability, interior consistency, boundary half-relaxed-limit inequality in both branches — boundary node [0,1] and interior nodes [−1,1] — comparison assumption): **YES** — the scheme fails the raw graph condition at interior points near 0 yet satisfies all operator-consistency components. Role limited to falsifying raw-graph necessity; it does not claim the project's 2D convergence.

## 3. Terminal (exactly one, Micro-Rev)

`DLH_5VH_THEORY_AUDIT_PARTIAL__ONE_BOUNDED_BOUNDARY_CONSISTENCY_OR_COMPARISON_GAP_REMAINS`

**The single bounded gap:** the constrained characterization `ρV ≤ H_T` at boundary points (the Soner⟷H_T equivalence content under project hypotheses: V-regularity, viability of the constrained dynamics, control compactness) and the comparison principle for the project's continuous state-constrained limit problem — not established from primary sources within this audit; blocks the W-contact-state branch of the boundary subsolution half-relaxed-limit transfer. Per the Reviewer's instruction, returned as Outcome B rather than carried into the next gate.

## 4. Companion reports

1. `reports/dlh_5vh_state_constraint_consistency_audit_2026_09_12/DLH_5VH_AUTHORITY_AND_PRIMARY_THEORY_CAPSULE.md`
2. `reports/dlh_5vh_state_constraint_consistency_audit_2026_09_12/DLH_5VH_CONTINUOUS_STATE_CONSTRAINT_HJB_AND_VISCOSITY_TARGET.md`
3. `reports/dlh_5vh_state_constraint_consistency_audit_2026_09_12/DLH_5VH_STRONG_GRAPH_TARGET_NECESSITY_AUDIT.md`
4. `reports/dlh_5vh_state_constraint_consistency_audit_2026_09_12/DLH_5VH_MONOTONE_SCHEME_BOUNDARY_CONSISTENCY_AND_FROZEN_PROCESS_TEST.md`
5. `reports/dlh_5vh_state_constraint_consistency_audit_2026_09_12/DLH_5VH_TERMINAL_AND_FORBIDDEN_CHECK.md`

## 5. Stop condition

Micro-Rev committed on top of `bc281a6` and pushed on the same dedicated branch; remote SHA = local SHA verified; fresh-main/Issue/activation/comments/branch/previous-candidate/new-candidate/ahead-behind/cumulative-diff/household-blob/provenance/sign-mapping/H_T-status/bridge/monotonicity/taxonomy/drift/forbidden-check evidence reported; exactly one terminal posted. STOP for fresh ChatGPT review — no merge, no close, no successor, no self-accept.
