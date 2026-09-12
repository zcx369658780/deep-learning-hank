# DLH-5V-H — State-Constraint HJB Boundary-Consistency Target Audit (Micro-Rev Rev 2)

**Issue #56** — `SCIENTIFIC_THEORY_AUDIT__STATE_CONSTRAINT_HJB_BOUNDARY_CONSISTENCY_TARGET`
**Owner route:** `APPROVE_DLH_5VH_ROUTE_E_STATE_CONSTRAINT_HJB_CONSISTENCY_TARGET_AUDIT`
**Branch:** `dsh/issue-56-dlh-5vh-state-constraint-consistency-audit-2026-09-12`
**Micro-Rev Rev 2:** Reviewer comment `5642335215` (Rev 1 Outcome B NOT accepted — local-state candidate bridge and half-relaxed quantifier fix required). Revision commits on top of `bc281a693b2d9281b6e180bc62996d503dfab7fe` (Rev 0) → `5d1e4822dcc94aa16d30837e9c524baaefe5fa3d` (Rev 1) → Rev 2.
**Date:** 2026-09-12

This is the umbrella record of the DLH-5V-H audit after the bounded Rev-2 Micro-Rev. It summarizes the theory-first sequence (A → B → C → D → E → F) with the Rev-2 repairs and states the terminal. Detailed arguments live in the five companion reports (links below).

---

## 1. Scope and authority

The audit reopens only the mathematical consistency/convergence target used to judge the discrete scheme; the Rev-2 Micro-Rev repairs two bounded proof defects without rewriting the gate. Consumed, not revised: household economics (drift formulas re-verified from the immutable source for the recovery lemma), finite-domain geometry, Issue-#54 lattice obstruction, Issue-#55 Outcome C. Fresh main `5d38c644ec1a06359241f9c3418dcd815c938ec6`; Issue #56 OPEN; activation comments `5641527846` / `5641534701`; Reviewer comments `5641997550` / `5642335215`; household blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`. Theory/design only; stationary KFE NOT AUTHORIZED.

## 2. Sequence results (Rev-2 level)

### A. Continuous state-constraint HJB target (report 3)

Frozen continuous object: `ρV = sup{u(c) − v_l·l + V_a μ_a + V_b μ_b}` on `D_W`, `F(x,r,p) = ρr − H(x,p)`.

- **Sign mapping (Task A, kept from Rev 1):** Soner Part I minimization convention (`H_S(x,p) = sup{−b·p − f}`, constrained solution = subsolution in the OPEN domain / supersolution on the CLOSED domain, Definition 2.1/Theorem 2.1, Reviewer-verified locations). Transform `V = −v`, `f = −g`: `G_S(x,−V,−p) = −F_proj(x,V,p)` ⟹ project orientation "subsolution on closure / supersolution in interior" — derived, no sign-by-analogy.
- **Boundary semantics:** (a) Soner one-sided form = THE continuous authority (subsolution on the closure w.r.t. the full H_proj); (b) `H_T` = DOWNGRADED auxiliary object (geometric labels of the frozen face laws; recovery target of the discrete operators); (c) the boundary transfer closes via the restriction H_lim ≤ H_proj (§D.2 of report 5) — no constrained characterization needed for the transfer.

### B. Primary-theory provenance (report 1)

Soner (1986) I/II, Barles–Souganidis (1991), supporting Capuzzo-Dolcetta–Lions (1990) and Bardi–Capuzzo-Dolcetta (1997, Ch. IV) — metadata/DOI + concise standard-content statements; every load-bearing statement labeled PRIMARY THEOREM / PROJECT-SPECIFIC DERIVATION / PLAUSIBLE-BUT-NOT-YET-PROVED.

### C. Necessity audit of the Issue-#55 raw graph target (report 4)

**Trichotomy answer: option (2) — sufficient but over-strong.** Not necessary for the operator-consistency components: (i) the convergence machinery operates on operator/test-function consistency, never on drift-set graph limits; (ii) the 1D toy falsifies necessity by construction. The raw-graph claim is scoped strictly to the BS operator structure + corrected toy + corrected half-relaxed-limit algebra — never via the unresolved 2D comparison block.

### D. Weakest defensible numerical target (report 5)

Discrete Bellman in residual and scaled forms; corrected monotonicity (order-preserving scaled operator with nonnegative weights; M-matrix residual; no ρ ≥ Σq); stability via max-principle; interior consistency (C² test functions, O(1/m) remainder); **quantifier-corrected half-relaxed-limit derivation (§D.2)**: contact step candidatewise, outer max retained, Taylor inside the max, H_lim = limsup of the discrete Bellman Hamiltonians; ū subsolution w.r.t. H_lim, u̲ supersolution in the interior; boundary subsolution on the closure w.r.t. H_proj in both branches via the restriction H_m ≤ H_proj.

### E. Frozen-process test (report 5)

1. `s_m = (0, i_t^m(0) − 2), μ = (0, 1)` with **μ_W = 1**: violates only the raw graph test; operator-consistent at the interior state; boundary transfer closed by the restriction argument.
2. Upper-corner analogue `(19m, i_t^m(19m) − 2), μ = (−1, 2)`: same conclusion.
3. Interior states approaching a boundary may remain interior-consistent without admissible set = boundary tangent cone: YES (one-sided structure + toy).
4. **Local-state same-candidate recovery lemma (§E.4, PROVED at the design level):** for every viable control at a corner/face limit point, explicit α_m at the ACTUAL states s_m — strict controls: α_m = α eventually (source-verified drift continuity); tangent controls: explicit inward perturbations (c → c + δ_m for μ_W = 0; d → d − ε_m for μ_a = 0 / μ_b = 0; the lower-corner a-side tangent handled by r_a_eff(a) ≥ 0 without perturbation); ALL rates from μ(s_m, α_m) with EXACT first moment and O(1/m) second moment (exact-arithmetic verified); the binding law candidate → admissibility → local drift → rates → score → ONE argmax → ONE Q is respected. Composite at the corners/faces: H_T ≤ liminf H_R ≤ limsup H_R ≤ H_proj. Triple corner (W_max = 8) distinct: Case-B forward/left contract at the (19m−7, 9) sub-top cells (i = 9, no mirror).
5. Issue-54 obstruction does not damage the recovery bridge (w_T ∉ REV, w_RT ∉ TDEP — the missing orientations are outside the corner laws; enumeration supplements destination availability only).

### F. Toy discriminator (report 5)

1D state-constraint toy with the full quantifier-corrected component proof (definition, order-preserving monotonicity, max-principle stability, interior consistency, boundary half-relaxed-limit subsolution at 0 in both branches — boundary-node branch exact H_T operator, interior-node branch ρφ(0) ≤ H_proj(0, φ') with the toy's elementary constrained characterization; interior supersolution; comparison assumption/theorem): **YES** — the scheme fails the raw graph condition at interior points near 0 yet satisfies all operator-consistency components and converges. Role limited to falsifying raw-graph necessity; no 2D convergence claim.

## 3. Terminal (exactly one, Rev 2)

`DLH_5VH_THEORY_AUDIT_PARTIAL__ONE_BOUNDED_BOUNDARY_CONSISTENCY_OR_COMPARISON_GAP_REMAINS`

**The single bounded block:** the project-specific application of the state-constraint comparison/unique-continuation theorem for the project's continuous limit problem (subsolution on the closure w.r.t. H_proj vs supersolution in the interior — Soner II / Capuzzo-Dolcetta–Lions form), with the constrained characterization `ρV ≤ H_T` at the boundary as a tightly coupled sublemma of the same block (not established; NOT load-bearing for the transfer, which closes via the restriction H_lim ≤ H_proj; needed only to identify the boundary limit as the H_T-constrained solution). Per the Reviewer's instruction, returned as Outcome B rather than carried into the next gate; Outcome A is not authorized by the current evidence.

## 4. Companion reports

1. `reports/dlh_5vh_state_constraint_consistency_audit_2026_09_12/DLH_5VH_AUTHORITY_AND_PRIMARY_THEORY_CAPSULE.md`
2. `reports/dlh_5vh_state_constraint_consistency_audit_2026_09_12/DLH_5VH_CONTINUOUS_STATE_CONSTRAINT_HJB_AND_VISCOSITY_TARGET.md`
3. `reports/dlh_5vh_state_constraint_consistency_audit_2026_09_12/DLH_5VH_STRONG_GRAPH_TARGET_NECESSITY_AUDIT.md`
4. `reports/dlh_5vh_state_constraint_consistency_audit_2026_09_12/DLH_5VH_MONOTONE_SCHEME_BOUNDARY_CONSISTENCY_AND_FROZEN_PROCESS_TEST.md`
5. `reports/dlh_5vh_state_constraint_consistency_audit_2026_09_12/DLH_5VH_TERMINAL_AND_FORBIDDEN_CHECK.md`

## 5. Stop condition

Rev 2 committed on top of `5d1e482` and pushed on the same dedicated branch; remote SHA = local SHA verified; fresh-main/Issue/activation/comments/branch/previous-candidates/new-candidate/ahead-behind/cumulative-diff/household-blob/provenance/quantifier-fix/recovery-status/strict-tangent-results/H_T-status/comparison-status/single-gap/forbidden-check evidence reported; exactly one terminal posted. STOP for fresh ChatGPT review — no merge, no close, no successor, no self-accept.
