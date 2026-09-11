# DLH-5V-H — State-Constraint HJB Boundary-Consistency Target Audit

**Issue #56** — `SCIENTIFIC_THEORY_AUDIT__STATE_CONSTRAINT_HJB_BOUNDARY_CONSISTENCY_TARGET`
**Owner route:** `APPROVE_DLH_5VH_ROUTE_E_STATE_CONSTRAINT_HJB_CONSISTENCY_TARGET_AUDIT`
**Branch:** `dsh/issue-56-dlh-5vh-state-constraint-consistency-audit-2026-09-12`
**Date:** 2026-09-12

This is the umbrella record of the DLH-5V-H audit. It summarizes the theory-first sequence (A → B → C → D → E → F) and states the terminal. Detailed arguments live in the five companion reports (links below).

---

## 1. Scope and authority

The audit reopens only the mathematical consistency/convergence target used to judge the discrete scheme. It consumes — without revising — the accepted household economics, the finite-domain geometry, the Issue-#54 finite-m lattice obstruction, and the Issue-#55 Outcome C result that the exact Kuratowski-style admissible-set graph target fails on the frozen state family. Fresh main `5d38c644ec1a06359241f9c3418dcd815c938ec6`; Issue #56 OPEN; activation comments `5641527846` / `5641534701`; household blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`. Theory/design only: no implementation, no production Q, no HJB/KFE/stationary solve, no numerical W_max, stationary KFE NOT AUTHORIZED.

## 2. Sequence results

### A. Continuous state-constraint HJB target (report 2)

Frozen continuous object: `ρV = sup{u(c) − v_l·l + V_a μ_a + V_b μ_b}` on `D_W = {0 ≤ a ≤ a_max, b ≥ b_min, a + b ≤ W_max}`, `F(x,r,p) = ρr − H(x,p)`.

- Equation in the open domain: viscosity sub- AND supersolution at interior points with the unrestricted Hamiltonian.
- Boundary semantics: (a) Soner state-constraint form — viscosity **subsolution on the closed domain** (one-sided upper inequality at boundary test points), supersolution in the interior; (b) tangent-cone-restricted Hamiltonian `H_T(x,p) = sup_{μ ∈ T_D(x)} {u − vl + p·μ}` on the closure; (c) relaxed operators from any cone ⊇ T_D(x̂). (a) and (b) are the two faces of the standard state-constraint characterization; (c) is the class that interior-state limits produce.
- The accepted active-face laws are exactly the tangent-cone restrictions (a=0: μ_a ≥ 0; b=b_min: μ_b ≥ 0; a=a_max: μ_a ≤ 0; W: μ_W ≤ 0; corners: intersections).
- Load-bearing lemma: the Hamiltonian is monotone in the admissible cone (H_C ≤ H_{C′} for C ⊆ C′); hence cones ⊇ T_D(x̂) are subsolution-safe and dominated on the supersolution side.

### B. Primary-theory provenance (report 1)

Soner (1986) I (`SIAM JCO 24(3):552–561`, DOI `10.1137/0324032`); Soner (1986) II (`24(6):1110–1122`, DOI `10.1137/0324067`); Barles–Souganidis (1991) (`Asymptotic Analysis 4(3):271–283`, DOI `10.3233/ASY-1991-4305`); plus Capuzzo-Dolcetta–Lions (1990) and Bardi–Capuzzo-Dolcetta (1997, Ch. IV) as supporting references. Sign convention, domain/boundary hypotheses, comparison assumptions and proved-vs-unproved items are mapped in the capsule table; no memory-only theorem-name invocation; no copyrighted material.

### C. Necessity audit of the Issue-#55 raw graph target (report 3)

**Trichotomy answer: option (2) — sufficient but over-strong.** The raw Kuratowski drift-set graph condition is not necessary: (i) the convergence machinery (monotone + stable + consistent + comparison) operates on operator/test-function consistency, never on drift-set graph limits; (ii) cone-monotonicity makes the Issue-55 counterexample cells (interior states with own-position face-law cones ⊇ the corner cone) harmless under the operator test; (iii) the 1D toy discriminator (report 5) falsifies necessity by construction. The raw target remains sufficient (a strong form of operator consistency) and Issue-#55's Outcome C remains accepted under its own target.

### D. Weakest defensible numerical target (report 5)

Discrete Bellman `S_m(s,u) = ρu(s) − max_α {g + Σ q (u(r) − u(s))} = 0`; monotonicity (row-sum/discount condition, automatic in the scaled discounted form); stability; interior consistency (C² test functions at interior states, O(1/m) remainder); one-sided boundary consistency at boundary-contact states with discrete cones R(s) ⊇ T_D(x̂) at corner limits; half-relaxed limits ū = limsup* (subsolution on D̄), u̲ = liminf* (supersolution in D°); state-constraint comparison hypothesis; explicit one-sided asymmetry. No invented boundary operator; no requirement on interior-state admissible sets approaching the boundary.

### E. Frozen-process test (report 5)

1. `s_m = (0, i_t^m(0) − 2), μ = (0, +1)`: violates ONLY the raw graph test; interior-consistent under the operator test (own cone {μ_a ≥ 0} ⊇ REV; H_{μ_a≥0} ≥ H_T; subsolution-safe). No legitimate-test violation.
2. Upper-corner analogue `(19m, i_t^m(19m) − 2), μ = (−1, +2)`: same conclusion.
3. Interior states approaching a boundary may remain interior-consistent without admissible set = boundary tangent cone: YES (cone-monotonicity + toy).
4. Actual W-contact states satisfy the legitimate one-sided boundary test: YES at design level — corner cones REV = cone{w_RT, w_down} (lower) and TDEP = cone{w_left, w_down, w_T} (upper) are contained in the represented cones at all W-contact band cells (exact enumeration: 0 violations, m ≤ 25, W_max ∈ {8, 10, 12}); regular W-band exact (H_R = H_T); face laws exact.
5. Issue-54 obstruction does NOT kill the scheme under the legitimate target: the missing endpoint orientations are exactly the directions outside the corner tangent cones (w_T ∉ REV since μ_a < 0; w_RT ∉ TDEP since μ_a > 0), so H_R ≥ H_T survives at both W-corners; the obstruction concerns only exact pointwise drift representability (a different object from operator consistency).

### F. Toy discriminator (report 5)

1D state-constraint toy (x ∈ [0,1], drifts [−1,1] interior / [0,1] at 0 / [−1,0] at 1; monotone upwind scheme): **YES** — the scheme fails the raw graph condition at interior points near 0 (outward drifts admitted) yet is viscosity-consistent, by the boundary points' restricted sets + cone-monotonicity + Soner comparison. The project 2D corners use the identical mechanism with REV/TDEP in place of [0,1]. Analytic proof only; no simulation.

## 3. Terminal (exactly one)

`DLH_5VH_STATE_CONSTRAINT_VISCOSITY_CONSISTENCY_TARGET_FROZEN__ISSUE55_GRAPH_TARGET_OVERSTRONG__READY_FOR_BOUNDARY_HJB_SCHEME_DESIGN_GATE`

## 4. Companion reports

1. `reports/dlh_5vh_state_constraint_consistency_audit_2026_09_12/DLH_5VH_AUTHORITY_AND_PRIMARY_THEORY_CAPSULE.md`
2. `reports/dlh_5vh_state_constraint_consistency_audit_2026_09_12/DLH_5VH_CONTINUOUS_STATE_CONSTRAINT_HJB_AND_VISCOSITY_TARGET.md`
3. `reports/dlh_5vh_state_constraint_consistency_audit_2026_09_12/DLH_5VH_STRONG_GRAPH_TARGET_NECESSITY_AUDIT.md`
4. `reports/dlh_5vh_state_constraint_consistency_audit_2026_09_12/DLH_5VH_MONOTONE_SCHEME_BOUNDARY_CONSISTENCY_AND_FROZEN_PROCESS_TEST.md`
5. `reports/dlh_5vh_state_constraint_consistency_audit_2026_09_12/DLH_5VH_TERMINAL_AND_FORBIDDEN_CHECK.md`

## 5. Stop condition

Candidate committed and pushed on the dedicated branch; remote SHA = local SHA verified; fresh-main/Issue/activation/branch/candidate/ahead-behind/cumulative-diff/household-blob/provenance/forbidden-check evidence reported; exactly one terminal posted. STOP for fresh ChatGPT review — no merge, no close, no successor, no self-accept.
