# DLH-5V-H — Authority and Primary-Theory Capsule (Micro-Rev Rev 3)

**Issue:** #56 / DLH-5V-H
**Task type:** `SCIENTIFIC_THEORY_AUDIT__STATE_CONSTRAINT_HJB_BOUNDARY_CONSISTENCY_TARGET`
**Branch:** `dsh/issue-56-dlh-5vh-state-constraint-consistency-audit-2026-09-12`
**Date:** 2026-09-12 — **Micro-Rev Rev 3** on top of Rev 2 candidate `52cfbf4cb4a1bcdb36bd77211869e8ac0f51b317` (itself on top of `5d1e4822dcc94aa16d30837e9c524baaefe5fa3d` and `bc281a693b2d9281b6e180bc62996d503dfab7fe`)
**Reviewer (Rev 2 verdict):** comment `5642677284` — `DLH_5VH_OUTCOME_B_NOT_YET_ACCEPTED__ADJUSTMENT_COST_TANGENT_RECOVERY_AND_HAMILTONIAN_REGULARITY_FIX_REQUIRED`

---

## Digest (Rev 3)

1. DLH-5V-H audits whether the accepted Issue-#55 raw admissible-drift-set graph target is mathematically necessary for state-constraint HJB scheme convergence. Rev 3 repairs the two load-bearing claims the Reviewer found stronger than the evidence: the transfer-perturbation algebra (the adjustment-cost term survives in μ_W) and the Hamiltonian regularity/compactness assumed in the limit passage.
2. **Exact transfer-perturbation algebra (Task A):** with χ(d,a) = χ_0|d| + ½χ_1 d²/max(a,a_bar), μ_a = r_a_eff(a)·a + d, μ_b = r_b·b + y − χ − d − c, μ_W = r_a_eff(a)·a + r_b·b + y − χ − c, the exact finite changes under d → d − ε are Δμ_a = −ε, **Δμ_b = +ε − Δχ, Δμ_W = −Δχ** (Δχ := χ(d−ε,a) − χ(d,a) ≠ 0 in general). Statements like "μ_b += ε" or "μ_W unchanged" are corrected; only the linear d cancels from μ_W, χ(d,a) remains.
3. **Tangent recovery re-audited family by family (Task A):** the ledger now splits PROVED STRICT / PROVED TANGENT / UNRESOLVED for every family: lower-a×W (REV), upper-a×W (TDEP), regular W, b_min×W joint cells, W_max=8 triple corner (TREA), non-W b_min face, non-W a faces. All families are PROVED: strict controls by drift continuity (α_m := α eventually); tangent controls by explicit constructions — μ_a-tangent at the lower corner by the formula r_a_eff(a) ≥ 0 (no perturbation); μ_W-tangent by c → c ± δ (exact linear algebra, no χ); μ_a-tangent at upper/TDEP and triple/TREA by d → d − ε (d < 0 always there, so Δχ > 0 — the perturbation creates W-slack Δμ_W = −Δχ < 0 and a-slack); the double-tangent cases at the triple corner and b_min×W by the coupled α_m = (c − δ_m, l, d − ε_m) with ε_m > 2C/m and δ_m interior to an explicit interval (nonempty — width ε_m + err_b − err_W > 0; strict margins at every finite m; exact-arithmetic verified).
4. **Hamiltonian regularity / effective compactness (Task B — Route R1):** the effective feasible control correspondence Γ(x) (budget + labor bounds + transfer bounds, source-verified components) is compact-valued with compact union — the quadratic adjustment cost coerces d, the budget bounds c, the labor disutility (1+φ)-power coerces l. H_proj(x,p) := max_{α ∈ Γ(x)}{u(c) − v(l) + p·μ} is therefore **finite for every (x,p)** (the formal unbounded-c sup would be +∞ for p_b < 0; the authority's sup is over the FEASIBLE controls — explicit clarification, not a revision); **upper semicontinuous in (x,p)** and continuous in p for each x (Berge, upper hemicontinuous compact-valued Γ + continuous Φ); **Lipschitz in p** (M = sup|μ| < ∞). Joint continuity in (x,p) holds on the interior-feasibility region (full Berge); the degenerate corners and the exact Soner-II/CDL theorem-application belong to the comparison block.
5. **Uniform moment bound (Task B):** |μ| ≤ M on the compact D̄_W × Γ ⟹ the sector rates are O(m·M) uniformly ⟹ sup_α Σ_r q_α|w_r|² = O(1/m) uniformly through the max — the Taylor remainder is uniform (the maximizing α may depend on m without breaking the bound).
6. **Boundary transfer status (honest):** the one-sided operator inequality at the boundary (ρφ ≤ H_lim ≤ H_proj, both branches) is **PROVED** (USC + restriction H_m ≤ H_proj + recovery). The full convergence u_m → V is **CONDITIONAL** on the comparison/unique-continuation block (§E.6) — the project-specific application of the state-constraint comparison theorem, with the constrained characterization ρV ≤ H_T as a coupled sublemma (not load-bearing for the transfer; needed only to identify the boundary limit as the H_T-constrained solution).
7. **Minor wording:** mirror availability is written as (j,i) → (j+7, i−10), requiring j+7 ≤ 19m (equivalently j ≤ 19m−7) and i ≥ 10 — not the stronger j+7 ≤ 19m−7.
8. **Toy:** language aligned with the regularity block (the toy's control set [−1,1] is explicitly compact — its Hamiltonian needs no regularity block; the 2D household Hamiltonian's feasibility/coercivity is the §D.4 project block); role limited to falsifying raw-graph necessity.
9. Rev-1/Rev-2 repairs preserved: explicit Soner sign mapping; project convention (subsolution on closure / supersolution in interior); H_T DOWNGRADED; corrected monotonicity; max-principle stability; frozen finite-m taxonomy; μ_W = 1; quantifier-corrected half-relaxed-limit (max retained); the restriction H_m ≤ H_proj as the right boundary direction.
10. **Ledger (matches the evidence):** PROVED — sign mapping; raw-graph non-necessity mechanism (BS structure + toy + corrected algebra, never via the unresolved 2D block); monotonicity; stability; interior consistency; stencil destination availability; finite-m rate algebra; local-state same-candidate recovery (all strict + tangent families, exact χ algebra); effective compactness/coercivity; H_proj finiteness/USC/Lipschitz-in-p; uniform max moment bound; boundary subsolution transfer on the closure (both branches); interior supersolution; composite H_T ≤ liminf H_R ≤ limsup H_R ≤ H_proj. UNRESOLVED — the project-specific comparison/unique-continuation application (continuous-Hamiltonian hypotheses established; exact theorem-application + degenerate-corner cases pending) and the constrained characterization ρV ≤ H_T (coupled sublemma). **Outcome B.**

**Terminal (exactly one, Rev 3):**

`DLH_5VH_THEORY_AUDIT_PARTIAL__ONE_BOUNDED_BOUNDARY_CONSISTENCY_OR_COMPARISON_GAP_REMAINS`

---

## Authority

- Live `main` at activation-refresh and at Reviewer checks: `5d38c644ec1a06359241f9c3418dcd815c938ec6` (re-verified by fresh fetch; unchanged; Issue #56 remains OPEN).
- Activation comments: `5641527846` (initial activation), `5641534701` (activation refresh). Reviewer comments: `5641997550` (Rev-0 verdict), `5642335215` (Rev-1 verdict), `5642677284` (Rev-2 verdict). Prior completion comments: `5642280244` (Rev 1), `5642519208` (Rev 2).
- Owner route decision: `APPROVE_DLH_5VH_ROUTE_E_STATE_CONSTRAINT_HJB_CONSISTENCY_TARGET_AUDIT`.
- Accepted household source (read-only, blob verified): `src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py` = `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`.
- Consumed, not reopened: Issue #54 (acceptance `5633995486`, integration `4e77d9c7…`), Issue #55 Outcome C (acceptance `5635802416`, integration `8dd5e9c4…`).
- Previous candidates: Rev 0 `bc281a693b2d9281b6e180bc62996d503dfab7fe` (Outcome A, NOT accepted); Rev 1 `5d1e4822dcc94aa16d30837e9c524baaefe5fa3d` (Outcome B, NOT accepted); Rev 2 `52cfbf4cb4a1bcdb36bd77211869e8ac0f51b317` (Outcome B, NOT accepted — two bounded defects). This Rev 3 amends on the same branch, same six-file allowlist.

---

## Primary-theory provenance

Cited with metadata only (no copyrighted PDFs, no long quotations). Statements are labeled PRIMARY THEOREM / PROJECT-SPECIFIC DERIVATION / PLAUSIBLE-BUT-NOT-YET-PROVED.

| Reference | DOI / metadata | Role in this audit | Status label |
|---|---|---|---|
| H. M. Soner (1986), "Optimal Control with State-Space Constraint I" | SIAM J. Control Optim. 24(3):552–561, DOI `10.1137/0324032` | State-constrained optimal control; minimization convention `H_S(x,p) = sup{−b·p − f}`, residual `G_S = ρv + H_S`; constrained viscosity solution = **subsolution in the open domain / supersolution on the closed domain** (Definition 2.1 / Theorem 2.1 locations verified by the Reviewer, comments `5641997550`, `5642335215`) | PRIMARY THEOREM (convention and orientation as verified by the Reviewer); the project transform is a PROJECT-SPECIFIC DERIVATION (continuous-target report §2.2) |
| H. M. Soner (1986), "Optimal Control with State-Space Constraint II" | SIAM J. Control Optim. 24(6):1110–1122, DOI `10.1137/0324067` | Comparison/uniqueness for state-constrained HJB; the state-constraint boundary condition inside the comparison class | PRIMARY THEOREM at reference level; project-specific hypothesis verification = PLAUSIBLE-BUT-NOT-YET-PROVED (the comparison block, Outcome B) |
| G. Barles, P. E. Souganidis (1991), "Convergence of approximation schemes for fully nonlinear second order equations" | Asymptotic Analysis 4(3):271–283, DOI `10.3233/ASY-1991-4305` | Monotone + stable + consistent (+ comparison) ⟹ locally uniform convergence; consistency is operator/test-function based | PRIMARY THEOREM at reference level (Theorem 2.1); the state-constraint boundary extension is PROJECT-SPECIFIC (this audit's mapping) |
| I. Capuzzo-Dolcetta, P.-L. Lions (1990), "Hamilton–Jacobi equations with state constraints" | Trans. Amer. Math. Soc. 318(2):643–683, DOI `10.1090/S0002-9947-1990-0951880-0` | Viscosity theory for HJ equations with state constraints; one-sided boundary condition, maximal-subsolution characterization, comparison | PRIMARY reference; exact theorem locations to be confirmed against the primary text |
| C. Berge (1963), "Topological Spaces" (maximum theorem) | Oliver & Boyd; also K. Border, "Fixed Point Theorems with Applications", Ch. 9 | Maximum theorem used for H_proj USC/continuity (effective compactness, Route R1) | STANDARD THEOREM; all hypotheses stated and verified from the source forms (monotone-scheme report §D.4) |
| M. Bardi, I. Capuzzo-Dolcetta (1997), "Optimal Control and Viscosity Solutions of Hamilton–Jacobi–Bellman Equations", Birkhäuser, Ch. IV | Book; Ch. IV: state-constrained problems, constrained Hamiltonian | Background for the constrained Hamiltonian as an auxiliary object | PRIMARY reference at chapter level; conventions to be confirmed against the primary text |

### Load-bearing status labels (Rev-3 discipline)

- **PRIMARY THEOREM SAYS THIS:** Soner Part I uses the minimization value v with `H_S(x,p) = sup{−b·p − f}` and characterizes the state-constrained value as viscosity subsolution in the open domain / supersolution on the closed domain (Definition 2.1 / Theorem 2.1, locations as verified by the Reviewer).
- **PROJECT-SPECIFIC DERIVATION SAYS THIS:** the transform `V = −v` (f = −g, b = μ) gives `G_S(x,−V,−p) = −F_proj(x,V,p)`, so Soner's open-domain subsolution becomes the project's open-domain supersolution and Soner's closed-domain supersolution becomes the project's closed-domain subsolution — the project orientation "subsolution on closure / supersolution in interior"; the effective-compactness/coercivity and the USC/continuity of H_proj (Berge, hypotheses verified from the immutable source); the local-state same-candidate recovery constructions with the exact χ algebra.
- **PLAUSIBLE BUT NOT YET PROVED (the single bounded Outcome-B block):** (i) the project-specific application of the state-constraint comparison/unique-continuation theorem for the project's continuous limit problem (the continuous-Hamiltonian hypotheses are established under Route R1; the exact primary-theorem application and the degenerate-corner continuity cases remain); (ii) the constrained characterization `ρV ≤ H_T` at boundary points (coupled sublemma; not load-bearing for the transfer). These are NOT carried forward as established.

### What is proved in this audit (Rev-3 level)

1. **Trichotomy answer (Issue step C):** the raw Kuratowski admissible-set graph target is sufficient but **over-strong** — not necessary for the operator-consistency components of state-constraint HJB scheme convergence. Arguments: (i) the half-relaxed-limit machinery requires operator/test-function consistency, never drift-set graph convergence; (ii) the 1D toy discriminator falsifies necessity by construction (quantifier-corrected proof).
2. **Half-relaxed-limit algebra (quantifier-corrected):** ū subsolution w.r.t. H_lim (max retained; no per-candidate inference); u̲ supersolution in the interior; boundary subsolution on the closure w.r.t. H_proj in both branches (USC + restriction + recovery).
3. **Local-state same-candidate recovery (PROVED at the design level, exact χ algebra):** strict controls α_m := α eventually; tangent controls by explicit constructions per family (formula-based at the lower-a μ_a-tangent; c → c ± δ for μ_W/μ_b tangents — exact linear algebra; d → d − ε at upper/TDEP and triple/TREA where d < 0 always — Δχ > 0 creates W-slack; coupled (ε, δ) at the double tangents with explicit interval conditions and strict margins; exact-arithmetic verified). Rates from μ(s_m, α_m) only; exact first moment; O(1/m) second moment.
4. **Hamiltonian regularity (Route R1):** effective compactness/coercivity; H_proj finite for all (x,p), USC in (x,p), continuous in p, Lipschitz in p; uniform O(1/m) max second-moment bound.
5. **Composite boundary-operator bounds at the corners/faces:** H_T ≤ liminf H_R ≤ limsup H_R ≤ H_proj.
6. **Corner-cone containment under the frozen taxonomy:** REV ⊆ R, TDEP ⊆ R, TREA ⊆ R, sector generators in the regular region — 0 violations, m ≤ 25, W_max ∈ {8, 10, 12} (scratch `%TEMP%\dlh5vh_frozen_taxonomy2.py`).
7. **Issue-54 orientations (consumed, re-applied):** w_T ∉ REV (μ_a < 0), w_RT ∉ TDEP (μ_a > 0); the finite-m lattice obstruction does not damage the recovery bridge at the W-corners.
8. **Issue-55 sequence re-test:** `s_m = (0, i_t^m(0) − 2), μ = (0, 1)` with μ_W = 1: violates only the raw graph test; operator-consistent; boundary transfer closed by the USC + restriction argument.
9. **Toy discriminator:** YES with the full quantifier-corrected component proof; language aligned with the regularity block.

### What remains unproved (explicitly, Rev 3)

1. **The Outcome-B block:** (i) the project-specific state-constraint comparison/unique-continuation theorem for the project's continuous limit problem (exact Soner-II / Capuzzo-Dolcetta–Lions theorem-application; degenerate-corner continuity cases of H_proj); (ii) the constrained characterization ρV ≤ H_T at the boundary (coupled sublemma; not load-bearing for the transfer). Not established within this audit.
2. Monotonicity normalization/stability details of the future scheme (order-preservation holds by construction in the scaled form; the final scheme-design choices belong to the next gate).
3. The full convergence theorem u_m → V (composition of the above; CONDITIONAL on the Outcome-B block).

No copyrighted material is committed; all primary references appear as metadata/DOI + concise standard-content statements.
