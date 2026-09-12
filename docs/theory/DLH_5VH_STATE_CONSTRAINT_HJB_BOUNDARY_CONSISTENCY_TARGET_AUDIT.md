# DLH-5V-H — State-Constraint HJB Boundary-Consistency Target Audit (Micro-Rev Rev 4)

**Issue #56** — `SCIENTIFIC_THEORY_AUDIT__STATE_CONSTRAINT_HJB_BOUNDARY_CONSISTENCY_TARGET`
**Owner route:** `APPROVE_DLH_5VH_ROUTE_E_STATE_CONSTRAINT_HJB_CONSISTENCY_TARGET_AUDIT`
**Branch:** `dsh/issue-56-dlh-5vh-state-constraint-consistency-audit-2026-09-12`
**Micro-Rev Rev 4:** Reviewer comment `5642868947` (Rev 3 Outcome B NOT accepted — false global budget feasibility and Hamiltonian effective domain fix required). Revision commits on top of `bc281a693b2d9281b6e180bc62996d503dfab7fe` (Rev 0) → `5d1e4822dcc94aa16d30837e9c524baaefe5fa3d` (Rev 1) → `52cfbf4cb4a1bcdb36bd77211869e8ac0f51b317` (Rev 2) → `dd3aa425a869a2d5a09835efc667c4ff1c2bb5b3` (Rev 3) → Rev 4.
**Date:** 2026-09-12

This is the umbrella record of the DLH-5V-H audit after the bounded Rev-4 Micro-Rev. It summarizes the theory-first sequence (A → B → C → D → E → F) with the Rev-4 corrections and states the terminal. Detailed arguments live in the five companion reports (links below).

---

## 1. Scope and authority

The audit reopens only the mathematical consistency/convergence target used to judge the discrete scheme; the Rev-4 Micro-Rev removes a false compactification and re-audits the true Hamiltonian without rewriting the gate. Consumed, not revised: household economics (χ/μ formulas re-verified from the immutable source), finite-domain geometry, Issue-#54 lattice obstruction, Issue-#55 Outcome C. Fresh main `5d38c644ec1a06359241f9c3418dcd815c938ec6`; Issue #56 OPEN; activation comments `5641527846` / `5641534701`; Reviewer comments `5641997550` / `5642335215` / `5642677284` / `5642868947`; household blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`. Theory/design only; stationary KFE NOT AUTHORIZED.

## 2. Sequence results (Rev-4 level)

### A. Continuous state-constraint HJB target (report 3)

Frozen continuous object: `ρV = sup_{c>0,l≥0,d∈R}{u(c) − v(l) + V_a μ_a + V_b μ_b}` on `D_W`, `F(x,r,p) = ρr − H(x,p)`.

- **Sign mapping (kept):** Soner Part I minimization convention, transform `V = −v`, `f = −g`, `G_S(x,−V,−p) = −F_proj(x,V,p)` ⟹ project orientation "subsolution on closure / supersolution in interior" (derived, Reviewer-verified locations).
- **Boundary semantics:** (a) Soner one-sided form = THE continuous authority (subsolution on the closure w.r.t. the full H_proj); (b) `H_T` = DOWNGRADED auxiliary object (geometric labels + recovery target of the discrete operators); (c) the boundary transfer closes via USC(H_proj on the effective region) + trivial restriction H_lim ≤ H_proj (§D.3 of report 5).
- **TRUE control domain (Rev 4):** c > 0, l ≥ 0, d ∈ R with source-exact μ_b = r_b·b + labor_income − d − χ(d,a) − c; the Rev-3 static budget `c + χ + d ≤ …` is REMOVED (it is μ_b ≥ 0, a tangent law only at b = b_min; the accepted R_reverse/R_deplete sectors have μ_b < 0); τ is the wage wedge inside effective wages, not additive resources; no hard l/d bounds installed; sup (not max) until attainment is proved.
- **Hamiltonian effective domain (Rev 4, exact, frozen γ_c = 2):** finite ⟺ p_b > 0 or (p_b = 0, p_a = 0); +∞ on {p_b < 0} ∪ {p_b = 0, p_a ≠ 0} (term-by-term: u(c) − p_b·c coercive for p_b > 0; −p_b·χ quadratic for p_b > 0; +|p_b|·χ quadratic-positive for p_b < 0; p_a·d unbounded at p_b = 0, p_a ≠ 0).
- **Local effective compactness (PROVED):** on compact K_p ⊂ {p_b ≥ η > 0}: common compact effective optimizer set K_alpha(K_p) from FOC-derived bounds (c* = p_b^{−1/2}, l_j* = (p_b·net_wage_j·z/ω_j)^{1/φ}, |d*| ≤ (s/χ_1)(|p_a−p_b|/η + χ_0)); sup = max there; |μ| ≤ M.
- **Hamiltonian regularity (PROVED on the effective region):** H_proj jointly continuous/USC in (x,p), Lipschitz in p; uniform O(1/m) max second-moment bound with the SAME domain restriction.

### B. Primary-theory provenance (report 1)

Soner (1986) I/II, Barles–Souganidis (1991), Capuzzo-Dolcetta–Lions (1990), Bardi–Capuzzo-Dolcetta (1997, Ch. IV), Berge (1963, maximum theorem) — metadata/DOI + concise standard-content statements; every load-bearing statement labeled PRIMARY THEOREM / PROJECT-SPECIFIC DERIVATION / PLAUSIBLE-BUT-NOT-YET-PROVED. Soner Part I's compact-control-space / bounded-drift / bounded-running-cost hypotheses are explicitly NOT assumed to hold for the raw project controls; the mapping question is open (Outcome-B block).

### C. Necessity audit of the Issue-#55 raw graph target (report 4)

**Trichotomy answer: option (2) — sufficient but over-strong.** Not necessary for the operator-consistency components: (i) the convergence machinery operates on operator/test-function consistency, never on drift-set graph limits; (ii) the 1D toy falsifies necessity by construction. The raw-graph claim is scoped strictly to the BS operator structure + corrected toy + corrected half-relaxed-limit algebra — never via the unresolved effective-domain/comparison block.

### D. Weakest defensible numerical target (report 5)

Discrete Bellman in residual and scaled forms; corrected monotonicity; max-principle stability; interior consistency; quantifier-corrected half-relaxed-limit (max retained; H_lim = limsup of the discrete Bellman Hamiltonians); boundary subsolution on the closure w.r.t. H_proj on the effective gradient region via trivial restriction + USC; uniform O(1/m) max second-moment bound on the effective region.

### E. Frozen-process test (report 5)

1. `s_m = (0, i_t^m(0) − 2), μ = (0, 1)` with **μ_W = 1**: violates only the raw graph test; operator-consistent; boundary transfer closed on the effective region.
2. Upper-corner analogue `(19m, i_t^m(19m) − 2), μ = (−1, 2)`: same conclusion.
3. Interior states approaching a boundary may remain interior-consistent without admissible set = boundary tangent cone: YES.
4. **Local-state same-candidate recovery with the exact χ algebra (PROVED for ALL families on the TRUE control domain):** Δμ_a = −ε, Δμ_b = +ε − Δχ, Δμ_W = −Δχ under d → d − ε; strict controls by continuity; tangent controls by explicit constructions — lower-a μ_a-tangent by r_a_eff(a) ≥ 0; μ_W/μ_b tangents by c → c ± δ (exact linear algebra); upper/triple μ_a-tangents by d → d − ε (d < 0 always there — Δχ > 0 creates W-slack); double tangents at the triple corner (W_max=8, cells (19m−7,9) and (19m,0), Case-B forward/left contract — no mirror at i=9) and b_min×W by the coupled α_m = (c − δ_m, l, d − ε_m) with ε_m > 2C/m and δ_m in an explicit nonempty interval — strict margins, exact-arithmetic verified; feasibility checked only against c > 0, l ≥ 0, d ∈ R and the genuine face laws (no global μ_b ≥ 0, no budget). Rates from μ(s_m, α_m) only; exact first moment; O(1/m) second moment. Composite H_T ≤ liminf H_R ≤ limsup H_R ≤ H_proj on the effective region. Mirror wording: (j,i) → (j+7, i−10) requiring j+7 ≤ 19m (j ≤ 19m−7) and i ≥ 10.
5. Issue-54 obstruction does not damage the recovery bridge (w_T ∉ REV, w_RT ∉ TDEP).

### F. Toy discriminator (report 5)

1D toy with the full quantifier-corrected component proof; the toy's control set [−1,1] is explicitly compact (its Hamiltonian needs no regularity block — deliberately a bounded-control model; the 2D household Hamiltonian's effective domain is the §D.4 project block); boundary subsolution at 0 in both branches; comparison via the classical 1D state-constraint theorem. **YES** — fails the raw graph condition yet satisfies all operator-consistency components; role limited to falsifying raw-graph necessity.

## 3. Terminal (exactly one, Rev 4)

`DLH_5VH_THEORY_AUDIT_PARTIAL__ONE_BOUNDED_BOUNDARY_CONSISTENCY_OR_COMPARISON_GAP_REMAINS`

**The single bounded block:** the Hamiltonian-effective-domain / state-constraint-comparison application block — (i) the relevant-viscosity-gradient restriction (test functions used by the state-constraint consistency/comparison arguments having p_b ≥ η > 0; routes: value-monotonicity-in-b, Inada lower bound, effective-domain-formulated comparison — none established in scope; the classical FOC c = V_b^{−1/γ_c} presumes V_b > 0 and is not a proof); (ii) the project-specific state-constraint comparison/unique-continuation theorem application, including the Soner compact-control assumption mapping (the project's raw controls are not compact; whether the local effective compactification on {p_b ≥ η > 0} suffices to map the project into the theorem, or an extension/generalization is required — do not cite Soner as directly applicable until resolved); (iii) the constrained characterization `ρV ≤ H_T` at the boundary (coupled sublemma — NOT load-bearing for the transfer, which closes via the trivial restriction + USC on the effective region). The boundary transfer itself is PROVED on {p_b ≥ η > 0} and overall CONDITIONAL_ON_EFFECTIVE_DOMAIN_REGULARITY; the full convergence u_m → V is CONDITIONAL on this block. Per the Reviewer's instruction, returned as Outcome B rather than carried into the next gate; Outcome A is not authorized by the current evidence.

## 4. Companion reports

1. `reports/dlh_5vh_state_constraint_consistency_audit_2026_09_12/DLH_5VH_AUTHORITY_AND_PRIMARY_THEORY_CAPSULE.md`
2. `reports/dlh_5vh_state_constraint_consistency_audit_2026_09_12/DLH_5VH_CONTINUOUS_STATE_CONSTRAINT_HJB_AND_VISCOSITY_TARGET.md`
3. `reports/dlh_5vh_state_constraint_consistency_audit_2026_09_12/DLH_5VH_STRONG_GRAPH_TARGET_NECESSITY_AUDIT.md`
4. `reports/dlh_5vh_state_constraint_consistency_audit_2026_09_12/DLH_5VH_MONOTONE_SCHEME_BOUNDARY_CONSISTENCY_AND_FROZEN_PROCESS_TEST.md`
5. `reports/dlh_5vh_state_constraint_consistency_audit_2026_09_12/DLH_5VH_TERMINAL_AND_FORBIDDEN_CHECK.md`

## 5. Stop condition

Rev 4 committed on top of `dd3aa42` and pushed on the same dedicated branch; remote SHA = local SHA verified; fresh-main/Issue/activation/comments/branch/previous-candidates/new-candidate/ahead-behind/cumulative-diff/household-blob/true-control-domain/false-μ_b≥0-removal/τ-correction/H_proj-domain-by-p_b/effective-compactness/USC-continuity/viscosity-gradient/moment-bound/tangent-ledger/boundary-transfer/comparison-status/single-gap/forbidden-check evidence reported; exactly one terminal posted. STOP for fresh ChatGPT review — no merge, no close, no successor, no self-accept.
