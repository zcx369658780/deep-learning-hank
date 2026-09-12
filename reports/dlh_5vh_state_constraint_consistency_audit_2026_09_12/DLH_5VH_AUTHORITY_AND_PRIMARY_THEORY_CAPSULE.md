# DLH-5V-H — Authority and Primary-Theory Capsule (Micro-Rev Rev 2)

**Issue:** #56 / DLH-5V-H
**Task type:** `SCIENTIFIC_THEORY_AUDIT__STATE_CONSTRAINT_HJB_BOUNDARY_CONSISTENCY_TARGET`
**Branch:** `dsh/issue-56-dlh-5vh-state-constraint-consistency-audit-2026-09-12`
**Date:** 2026-09-12 — **Micro-Rev Rev 2** on top of Rev 1 candidate `5d1e4822dcc94aa16d30837e9c524baaefe5fa3d` (which is on top of `bc281a693b2d9281b6e180bc62996d503dfab7fe`)
**Reviewer (Rev 1 verdict):** comment `5642335215` — `DLH_5VH_OUTCOME_B_NOT_YET_ACCEPTED__LOCAL_STATE_CANDIDATE_BRIDGE_AND_HALF_RELAXED_QUANTIFIER_FIX_REQUIRED`

---

## Digest (Rev 2)

1. DLH-5V-H audits whether the accepted Issue-#55 raw admissible-drift-set graph target is mathematically necessary for state-constraint HJB scheme convergence. Rev 1 repaired the Soner sign mapping (explicit transform), downgraded H_T, corrected monotonicity, restored the frozen finite-m taxonomy, and fixed the counterexample drift units. Rev 2 repairs the two load-bearing proof defects the Reviewer found in Rev 1: the half-relaxed-limit candidate quantifier and the limit-state rate construction.
2. **Quantifier fix (§D.2):** the half-relaxed-limit derivation now retains the outer max throughout (contact step candidatewise ⟹ max ≤ max, Taylor candidatewise inside the max, no per-candidate inference); both the subsolution (near-maximizer) and supersolution (near-minimizer) directions are corrected; the limit object is H_lim = limsup of the discrete Bellman Hamiltonians at the visited states.
3. **Boundary transfer closed by the restriction:** at W-contact states H_m(s_m, p) ≤ H_proj(s_m, p) → H_proj(x̂, p) (buffered candidate sets ⊆ full candidate sets; Hausdorff convergence of the feasibility bounds), so ρφ(x̂) ≤ H_lim ≤ H_proj in both branches — the Soner-form subsolution on the closure is obtained WITHOUT the constrained characterization ρV ≤ H_T.
4. **Local-state same-candidate recovery lemma (§E.4, PROVED at the design level):** for every viable control at a corner/face limit point, α_m at the ACTUAL states s_m (strict controls: α_m = α eventually, by the source-verified drift continuity; tangent controls: explicit inward perturbations — c → c + δ_m for μ_W = 0, d → d − ε_m for μ_a = 0 / μ_b = 0, with the a-side tangent at the lower corner handled by the formula itself since r_a_eff(a) ≥ 0); ALL rates are computed from μ(s_m, α_m) with EXACT first moment and O(1/m) second moment (exact-arithmetic verified). The binding law candidate → admissibility → local drift → rates → score → ONE argmax → ONE Q is respected.
5. **Recovery + restriction composite at the corners/faces:** H_T ≤ liminf H_R ≤ limsup H_R ≤ H_proj — the geometric/control content of the boundary operators. The triple corner (W_max = 8) is treated distinctly (Case-B forward/left contract at the (19m−7, 9) sub-top cells, i = 9, NO mirror assertion).
6. **Toy (Rev 2):** full component proof with the corrected max quantifier; the boundary half-relaxed-limit subsolution at 0 is analyzed in both branches (boundary-node branch: exact constrained operator H_T; interior-node branch: ρφ(0) ≤ H_proj(0, φ') suffices for the toy's convergence, with the elementary constrained characterization closing the H_T identification); the toy's role is limited to falsifying the necessity of the raw graph condition.
7. **Raw-graph claim scoping:** "the raw graph target is over-strong" is asserted only to the level supported by the Barles–Souganidis operator structure, the corrected toy, and the corrected half-relaxed-limit algebra — never via the unresolved 2D comparison block.
8. **PROVED (Rev 2):** Soner sign mapping (explicit transform); raw graph non-necessity mechanism; monotonicity (order-preserving scaled operator, M-matrix residual, no ρ ≥ Σq); stability (max-principle); interior consistency; stencil destination availability; finite-m rate algebra conditional on a locally admissible candidate; **local-state same-candidate recovery (strict + tangent, source-verified)**; boundary subsolution transfer on the closure w.r.t. H_proj (both branches, restriction argument); interior supersolution; the composite H_T ≤ liminf H_R ≤ limsup H_R ≤ H_proj at the corners/faces.
9. **UNRESOLVED (the single bounded Outcome-B block):** the project-specific application of the state-constraint comparison/unique-continuation theorem for the project's continuous limit problem (subsolution on the closure w.r.t. H_proj vs supersolution in the interior), with the constrained characterization ρV ≤ H_T at the boundary as a tightly coupled sublemma of the same block (not established; not load-bearing for the transfer; needed only to identify the boundary limit as the H_T-constrained solution).
10. Rev-1 repairs preserved: explicit Soner sign mapping (Task A); H_T DOWNGRADED to an auxiliary object (Task B); corrected monotonicity (Task D); frozen finite-m taxonomy with physical limit-region partitions relabeled (Task E); μ_W = 1 counterexample drift (Task F).

**Terminal (exactly one, Rev 2):**

`DLH_5VH_THEORY_AUDIT_PARTIAL__ONE_BOUNDED_BOUNDARY_CONSISTENCY_OR_COMPARISON_GAP_REMAINS`

---

## Authority

- Live `main` at activation-refresh and at Reviewer checks: `5d38c644ec1a06359241f9c3418dcd815c938ec6` (re-verified by fresh fetch; unchanged; Issue #56 remains OPEN).
- Activation comments: `5641527846` (initial activation), `5641534701` (activation refresh). First Micro-Rev comment: `5641997550`. Latest Reviewer comment (Rev-1 verdict): `5642335215`. Prior completion comment: `5642280244`.
- Owner route decision: `APPROVE_DLH_5VH_ROUTE_E_STATE_CONSTRAINT_HJB_CONSISTENCY_TARGET_AUDIT`.
- Accepted household source (read-only, blob verified): `src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py` = `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`.
- Consumed, not reopened: Issue #54 (acceptance `5633995486`, integration `4e77d9c7…`), Issue #55 Outcome C (acceptance `5635802416`, integration `8dd5e9c4…`).
- Previous candidates: Rev 0 `bc281a693b2d9281b6e180bc62996d503dfab7fe` (Outcome A, NOT accepted); Rev 1 `5d1e4822dcc94aa16d30837e9c524baaefe5fa3d` (Outcome B, NOT accepted — two bounded proof defects). This Rev 2 amends on the same branch, same six-file allowlist.

---

## Primary-theory provenance

Cited with metadata only (no copyrighted PDFs, no long quotations). Statements are labeled PRIMARY THEOREM / PROJECT-SPECIFIC DERIVATION / PLAUSIBLE-BUT-NOT-YET-PROVED.

| Reference | DOI / metadata | Role in this audit | Status label |
|---|---|---|---|
| H. M. Soner (1986), "Optimal Control with State-Space Constraint I" | SIAM J. Control Optim. 24(3):552–561, DOI `10.1137/0324032` | State-constrained optimal control; minimization convention `H_S(x,p) = sup{−b·p − f}`, residual `G_S = ρv + H_S`; constrained viscosity solution = **subsolution in the open domain / supersolution on the closed domain** (Definition 2.1 / Theorem 2.1 locations verified by the Reviewer's primary-source check, comments `5641997550` and `5642335215`) | PRIMARY THEOREM (convention and orientation as verified by the Reviewer); the project transform is a PROJECT-SPECIFIC DERIVATION (§2.2 of the continuous-target report) |
| H. M. Soner (1986), "Optimal Control with State-Space Constraint II" | SIAM J. Control Optim. 24(6):1110–1122, DOI `10.1137/0324067` | Comparison/uniqueness for state-constrained HJB; the state-constraint boundary condition inside the comparison class | PRIMARY THEOREM at reference level; project-specific hypothesis verification = PLAUSIBLE-BUT-NOT-YET-PROVED (the comparison block, Outcome B) |
| G. Barles, P. E. Souganidis (1991), "Convergence of approximation schemes for fully nonlinear second order equations" | Asymptotic Analysis 4(3):271–283, DOI `10.3233/ASY-1991-4305` | Monotone + stable + consistent (+ comparison) ⟹ locally uniform convergence; consistency is operator/test-function based | PRIMARY THEOREM at reference level (Theorem 2.1); the state-constraint boundary extension is PROJECT-SPECIFIC (this audit's mapping) |
| I. Capuzzo-Dolcetta, P.-L. Lions (1990), "Hamilton–Jacobi equations with state constraints" | Trans. Amer. Math. Soc. 318(2):643–683, DOI `10.1090/S0002-9947-1990-0951880-0` | Viscosity theory for HJ equations with state constraints; one-sided boundary condition, maximal-subsolution characterization, comparison | PRIMARY reference; exact theorem locations to be confirmed against the primary text |
| M. Bardi, I. Capuzzo-Dolcetta (1997), "Optimal Control and Viscosity Solutions of Hamilton–Jacobi–Bellman Equations", Birkhäuser, Ch. IV | Book; Ch. IV: state-constrained problems, constrained Hamiltonian | Background for the constrained Hamiltonian as an auxiliary object | PRIMARY reference at chapter level; conventions to be confirmed against the primary text |

### Load-bearing status labels (Rev-2 discipline)

- **PRIMARY THEOREM SAYS THIS:** Soner Part I uses the minimization value v with `H_S(x,p) = sup{−b·p − f}` and characterizes the state-constrained value as viscosity subsolution in the open domain / supersolution on the closed domain (Definition 2.1 / Theorem 2.1, locations as verified by the Reviewer).
- **PROJECT-SPECIFIC DERIVATION SAYS THIS:** the transform `V = −v` (f = −g, b = μ) gives `G_S(x,−V,−p) = −F_proj(x,V,p)`, so Soner's open-domain subsolution becomes the project's open-domain supersolution and Soner's closed-domain supersolution becomes the project's closed-domain subsolution — the project orientation "subsolution on closure / supersolution in interior" (continuous-target report §2.2, fully derived).
- **PLAUSIBLE BUT NOT YET PROVED (the single bounded Outcome-B block):** (i) the project-specific application of the state-constraint comparison/unique-continuation theorem for the project's continuous limit problem (subsolution on the closure w.r.t. H_proj vs supersolution in the interior — the Soner II / Capuzzo-Dolcetta–Lions form); (ii) the constrained characterization `ρV ≤ H_T` at boundary points, as a tightly coupled sublemma of the same block (not needed for the transfer, which closes via the restriction H_lim ≤ H_proj; needed only to identify the boundary limit as the H_T-constrained solution). These are NOT carried forward as established.

### What is proved in this audit (Rev-2 level)

1. **Trichotomy answer (Issue step C):** the raw Kuratowski admissible-set graph target is sufficient but **over-strong** — not necessary for the operator-consistency components of state-constraint HJB scheme convergence. Arguments: (i) the half-relaxed-limit machinery requires operator/test-function consistency, never drift-set graph convergence; (ii) the 1D toy discriminator falsifies necessity by construction (quantifier-corrected proof).
2. **Half-relaxed-limit algebra (Task D, quantifier-corrected):** ū subsolution w.r.t. H_lim (max retained; no per-candidate inference); u̲ supersolution in the interior; boundary transfer on the closure w.r.t. H_proj via the restriction H_m ≤ H_proj (both branches).
3. **Local-state same-candidate recovery (Task C, PROVED at the design level):** explicit α_m constructions (α for strict controls; c → c + δ_m, d → d − ε_m inward perturbations for tangent controls, with explicit O(1/m) bounds), all rates from μ(s_m, α_m), exact first moment, O(1/m) second moment; drift-continuity and feasibility hypotheses verified from the immutable household source (r_a_eff(a) = r_a(1 − 0.1(a/a_max)^9) ≥ 0.9 r_a ≥ 0; μ_b affine in b plus continuous y, χ; g independent of x and d).
4. **Composite boundary-operator bounds at the corners/faces:** H_T ≤ liminf H_R ≤ limsup H_R ≤ H_proj.
5. **Corner-cone containment under the frozen taxonomy (Task E):** REV ⊆ R (lower-a W-contact cells), TDEP ⊆ R (upper-a W-contact cells), TREA ⊆ R (b_min-corner sub-top family), sector generators in the regular region — 0 violations, m ≤ 25, W_max ∈ {8, 10, 12} (scratch `%TEMP%\dlh5vh_frozen_taxonomy2.py`).
6. **Issue-54 orientations (consumed, re-applied):** the missing endpoint orientations (w_T at lower exact-frontier cells, w_RT at upper exact-frontier cells) are outside the corner tangent cones (w_T ∉ REV since μ_a < 0; w_RT ∉ TDEP since μ_a > 0); the finite-m lattice obstruction does not damage the recovery bridge at the W-corners.
7. **Issue-55 sequence re-test (Task F):** `s_m = (0, i_t^m(0) − 2), μ = (0, 1)` with μ_W = 1: interior state, own cone {μ_a ≥ 0} (a=0 face law); it violates only the raw graph test; the operator-level interior consistency at such states is unaffected; the boundary transfer at the corner is closed by the restriction argument.
8. **Toy discriminator:** YES with the full quantifier-corrected component proof (monotone-scheme report §Part F).

### What remains unproved (explicitly, Rev 2)

1. **The Outcome-B block:** (i) the project-specific state-constraint comparison/unique-continuation theorem for the project's continuous limit problem under project hypotheses; (ii) the constrained characterization ρV ≤ H_T at the boundary (coupled sublemma of the same block; not load-bearing for the transfer). Not established within this audit.
2. Monotonicity normalization/stability details of the future scheme (order-preservation holds by construction in the scaled form; the final scheme-design choices belong to the next gate).
3. The full convergence theorem u_m → V (composition of the above).

No copyrighted material is committed; all primary references appear as metadata/DOI + concise standard-content statements.
