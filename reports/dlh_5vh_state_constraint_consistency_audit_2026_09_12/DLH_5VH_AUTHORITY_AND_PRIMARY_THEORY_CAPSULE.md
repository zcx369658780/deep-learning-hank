# DLH-5V-H — Authority and Primary-Theory Capsule

**Issue:** #56 / DLH-5V-H
**Task type:** `SCIENTIFIC_THEORY_AUDIT__STATE_CONSTRAINT_HJB_BOUNDARY_CONSISTENCY_TARGET`
**Branch:** `dsh/issue-56-dlh-5vh-state-constraint-consistency-audit-2026-09-12`
**Date:** 2026-09-12 — **Micro-Rev revision (Rev 1)** on top of candidate `bc281a693b2d9281b6e180bc62996d503dfab7fe`
**Reviewer:** comment `5641997550` — `DLH_5VH_OUTCOME_A_NOT_ACCEPTED__BOUNDARY_OPERATOR_EQUIVALENCE_AND_SCHEME_CONSISTENCY_MICRO_REV_REQUIRED`

---

## Digest (≤ 12 lines)

1. DLH-5V-H audits whether the accepted Issue-#55 raw admissible-drift-set graph target is mathematically necessary for state-constraint HJB scheme convergence; the Reviewer's Micro-Rev required six bounded repairs (sign mapping, H_T status, control-level consistency, monotonicity, taxonomy, drift typo).
2. Soner Part I's actual convention (minimization value v, `H_S(x,p) = sup{−b·p − f}`, residual `G_S = ρv + H_S`; constrained solution = subsolution in the OPEN domain / supersolution on the CLOSED domain) is mapped to the project by the explicit transform `V = −v`, `f = −g`, `G_S(x,−V,−p) = −F_proj(x,V,p)`; hence the project's "subsolution on closure / supersolution in interior" is the transformed Soner orientation (derivation in the continuous-target report, §2.2).
3. The claimed equivalence "Soner state-constraint form ⟺ tangent-cone-restricted Hamiltonian H_T on the closure" is **DOWNGRADED**: not asserted as an equivalence; Soner's one-sided viscosity condition is the continuous authority; H_T is used only as an auxiliary geometric/control object where separately justified (control-level bridge below).
4. The geometric statement "R(s_m) ⊇ T_D(x*)" is replaced by the control/payoff-level bridge: for every viable control α at a W-corner, the frozen W-contact candidates represent the SAME payoff g(α) with exact first moment μ(x̂,α) and second moment O(1/m); hence `liminf H_R ≥ H_T` at the discrete-operator level (derivation in the frozen-process report, §E.4).
5. The monotonicity condition is corrected: the residual has the proper M-matrix structure (diagonal ρ + Σq > 0, off-diagonals −q ≤ 0); the required order-preservation holds in the scaled discounted Bellman form with nonnegative weights; the condition `ρ ≥ Σq` is NOT imposed (incompatible with q = O(m)); stability via the max-principle `|u_m| ≤ ‖g‖∞/ρ`.
6. The level-m taxonomy is corrected: frozen finite-m endpoint layers `j ∈ {0,…,6}` and `j ∈ {19m−6,…,19m}`, regular stencil region `7 ≤ j ≤ 19m−7`, accepted W-active/class conditions, lower-b layer `i ≤ 9`; proportional regions (`j < 7m`, `j > 12m`) are labeled PHYSICAL LIMIT-REGION partitions only.
7. Counterexample drift corrected: `μ = (0,1)` has `μ_W = 1` (physical units); the jump `w_up = (0, 7/(19m))` with rate `q_up = 19m/7` gives first moment `(0,1)`; jump and physical drift are kept distinct.
8. The corner-cone containment is re-verified under the frozen taxonomy with per-cell limit-corner logic: REV ⊆ R at lower-a W-contact cells, TDEP ⊆ R at upper-a W-contact cells, TREA ⊆ R at the b_min-corner sub-top family, sector generators present in the regular region — 0 violations (m ≤ 25, W_max ∈ {8, 10, 12}).
9. The 1D toy is retained with a strengthened proof (explicit scheme, monotonicity, max-principle stability, interior consistency, boundary half-relaxed-limit inequality with both boundary-node and interior-node branches, comparison assumption); its role is only to falsify necessity of the raw graph condition.
10. **One bounded gap remains:** the state-constraint constrained characterization `ρV ≤ H_T` at boundary points (the H_T-equivalence content) and the comparison principle for the project's continuous limit problem are not established from primary sources with project hypotheses within this audit — this blocks the W-contact-state branch of the boundary subsolution half-relaxed-limit transfer, not the operator-consistency components themselves.

**Terminal (exactly one, Micro-Rev):**

`DLH_5VH_THEORY_AUDIT_PARTIAL__ONE_BOUNDED_BOUNDARY_CONSISTENCY_OR_COMPARISON_GAP_REMAINS`

---

## Authority

- Live `main` at activation-refresh and at Reviewer check: `5d38c644ec1a06359241f9c3418dcd815c938ec6` (re-verified by fresh fetch; unchanged; Issue #56 remains OPEN).
- Activation comments: `5641527846` (initial activation), `5641534701` (activation refresh). Reviewer Micro-Rev comment: `5641997550`.
- Owner route decision: `APPROVE_DLH_5VH_ROUTE_E_STATE_CONSTRAINT_HJB_CONSISTENCY_TARGET_AUDIT`.
- Accepted household source (read-only, blob verified): `src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py` = `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`.
- Consumed, not reopened: Issue #54 (acceptance `5633995486`, integration `4e77d9c7…`), Issue #55 Outcome C (acceptance `5635802416`, integration `8dd5e9c4…`).
- Previous candidate: `bc281a693b2d9281b6e180bc62996d503dfab7fe` (Outcome A proposed, NOT accepted). This Rev 1 amends it on the same branch, same six-file allowlist.

---

## Primary-theory provenance

Cited with metadata only (no copyrighted PDFs, no long quotations). Statements are labeled PRIMARY THEOREM / PROJECT-SPECIFIC DERIVATION / PLAUSIBLE-BUT-NOT-YET-PROVED.

| Reference | DOI / metadata | Role in this audit | Status label |
|---|---|---|---|
| H. M. Soner (1986), "Optimal Control with State-Space Constraint I" | SIAM J. Control Optim. 24(3):552–561, DOI `10.1137/0324032` | State-constrained optimal control; minimization convention `H_S(x,p) = sup{−b·p − f}`, residual `G_S = ρv + H_S`; constrained viscosity solution = **subsolution in the open domain / supersolution on the closed domain** (Definition 2.1 / Theorem 2.1 locations verified by the Reviewer's primary-source check, comment `5641997550`) | PRIMARY THEOREM (convention and orientation as verified by Reviewer); the project transform is a PROJECT-SPECIFIC DERIVATION (§2.2 of the continuous-target report) |
| H. M. Soner (1986), "Optimal Control with State-Space Constraint II" | SIAM J. Control Optim. 24(6):1110–1122, DOI `10.1137/0324067` | Comparison/uniqueness for state-constrained HJB; the state-constraint boundary condition inside the comparison class | PRIMARY THEOREM at reference level; project-specific hypothesis verification = PLAUSIBLE-BUT-NOT-YET-PROVED (the comparison gap, Outcome B) |
| G. Barles, P. E. Souganidis (1991), "Convergence of approximation schemes for fully nonlinear second order equations" | Asymptotic Analysis 4(3):271–283, DOI `10.3233/ASY-1991-4305` | Monotone + stable + consistent (+ comparison) ⟹ locally uniform convergence; consistency is operator/test-function based | PRIMARY THEOREM at reference level (Theorem 2.1); the state-constraint boundary extension is PROJECT-SPECIFIC (this audit's mapping) |
| I. Capuzzo-Dolcetta, P.-L. Lions (1990), "Hamilton–Jacobi equations with state constraints" | Trans. Amer. Math. Soc. 318(2):643–683, DOI `10.1090/S0002-9947-1990-0951880-0` | Viscosity theory for HJ equations with state constraints; one-sided boundary condition and comparison | PRIMARY reference; exact theorem locations to be confirmed against the primary text |
| M. Bardi, I. Capuzzo-Dolcetta (1997), "Optimal Control and Viscosity Solutions of Hamilton–Jacobi–Bellman Equations", Birkhäuser, Ch. IV | Book; Ch. IV: state-constrained problems, constrained Hamiltonian | Background for the constrained Hamiltonian as an auxiliary object | PRIMARY reference at chapter level; conventions to be confirmed against the primary text |

### Load-bearing status labels (Micro-Rev discipline)

- **PRIMARY THEOREM SAYS THIS:** Soner Part I uses the minimization value v with `H_S(x,p) = sup{−b·p − f}` and characterizes the state-constrained value as viscosity subsolution in the open domain / supersolution on the closed domain (Definition 2.1 / Theorem 2.1, locations as verified by Reviewer `5641997550`).
- **PROJECT-SPECIFIC DERIVATION SAYS THIS:** the transform `V = −v` (f = −g, b = μ) gives `G_S(x,−V,−p) = −F_proj(x,V,p)`, so Soner's open-domain subsolution becomes the project's open-domain supersolution and Soner's closed-domain supersolution becomes the project's closed-domain subsolution — the project orientation "subsolution on closure / supersolution in interior" (continuous-target report §2.2, fully derived).
- **PLAUSIBLE BUT NOT YET PROVED (the single bounded gap):** (i) the constrained characterization `ρV ≤ H_T` at boundary points (the H_T-equivalence content under project hypotheses: Lipschitz regularity of V, viability of the constrained dynamics, control compactness) and (ii) the comparison principle for the project's continuous state-constrained limit problem. These are exactly the Outcome-B gap; they are NOT carried forward as established.

### What is proved in this audit (Micro-Rev level)

1. **Trichotomy answer (Issue step C):** the raw Kuratowski admissible-set graph target is sufficient but **over-strong** — not necessary for the operator-consistency components of state-constraint HJB scheme convergence. Arguments: (i) the half-relaxed-limit machinery requires operator/test-function consistency, never drift-set graph convergence; (ii) the 1D toy discriminator falsifies necessity by construction (a monotone scheme failing the raw graph condition at interior points near the boundary that satisfies all operator-consistency components).
2. **Control/payoff-level bridge (Task C):** at the W-corners, every viable control α (μ(x̂,α) ∈ REV at the lower corner, ∈ TDEP at the upper corner) is represented at the relevant W-contact cells by the frozen sector rates with the SAME payoff g(α), EXACT first moment μ(x̂,α), and second moment O(1/m) — hence `liminf H_R ≥ H_T` at the discrete-operator level (frozen-process report §E.4).
3. **Corner-cone containment under the frozen taxonomy (Task E):** REV ⊆ R (lower-a W-contact cells), TDEP ⊆ R (upper-a W-contact cells), TREA ⊆ R (b_min-corner sub-top family), sector generators in the regular region — 0 violations, m ≤ 25, W_max ∈ {8, 10, 12} (scratch `%TEMP%\dlh5vh_frozen_taxonomy2.py`).
4. **Issue-54 orientations (consumed, re-applied):** the missing endpoint orientations (w_T at lower exact-frontier cells, w_RT at upper exact-frontier cells) are outside the corner tangent cones (w_T ∉ REV since μ_a < 0; w_RT ∉ TDEP since μ_a > 0); the finite-m lattice obstruction does not damage the control-level bridge at the W-corners.
5. **Issue-55 sequence re-test (Task F):** `s_m = (0, i_t^m(0) − 2), μ = (0, 1)` with μ_W = 1: interior state, own cone {μ_a ≥ 0} (a=0 face law); it violates only the raw graph test; the operator-level interior consistency at such states is unaffected; the boundary transfer at the corner via W-contact sequences is gated by the Outcome-B gap.
6. **Toy discriminator:** YES with full component proof (frozen-process report §Part F).

### What remains unproved (explicitly, Micro-Rev)

1. **The Outcome-B gap:** the constrained characterization `ρV ≤ H_T` at ∂D (equivalently the Soner⟷H_T equivalence) and the comparison principle for the project's continuous state-constrained limit problem, under project hypotheses (V-regularity, viability, control compactness). Not established within this audit; the W-contact-state branch of the boundary subsolution half-relaxed-limit transfer depends on it.
2. Monotonicity normalization/stability details of the future scheme (order-preservation holds by construction in the scaled form; the final scheme-design choices belong to the next gate).
3. The full convergence theorem u_m → V (composition of the above).

No copyrighted material is committed; all primary references appear as metadata/DOI + concise standard-content statements.
