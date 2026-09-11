# DLH-5V-H — Authority and Primary-Theory Capsule

**Issue:** #56 / DLH-5V-H
**Task type:** `SCIENTIFIC_THEORY_AUDIT__STATE_CONSTRAINT_HJB_BOUNDARY_CONSISTENCY_TARGET`
**Branch:** `dsh/issue-56-dlh-5vh-state-constraint-consistency-audit-2026-09-12`
**Date:** 2026-09-12

---

## Digest (≤ 12 lines)

1. DLH-5V-H audits whether the accepted Issue-#55 raw admissible-drift-set graph target (Kuratowski limsup/liminf of the finite-m drift sets at every convergent state sequence) is mathematically necessary for state-constraint HJB scheme convergence.
2. The legitimate convergence object is the viscosity/operator consistency target: monotone, stable, interior-consistent, one-sided boundary-consistent scheme whose half-relaxed limits are compared by a state-constraint comparison principle.
3. The Issue-#55 graph target is sufficient but **over-strong**: it is not required by any primary viscosity/operator consistency condition; interior grid states approaching a constrained boundary may legitimately keep their own (larger) admissible cones.
4. Cone-monotonicity of the Hamiltonian (H increasing in the admissible cone) makes interior-state cones ⊇ the boundary tangent cone harmless for the one-sided subsolution inequality, and dominated on the supersolution side.
5. At the actual discrete W-contact states, the true corner tangent cones REV = {μ_a ≥ 0, μ_W ≤ 0} (lower corner) and TDEP = {μ_a ≤ 0, μ_W ≤ 0} (upper corner) are fully representable (exact check: 0 violations, m ≤ 25, W_max ∈ {8,10,12}).
6. The Issue-#54 missing endpoint orientations (w_T at lower exact-frontier cells, w_RT at upper exact-frontier cells) are exactly the directions OUTSIDE the respective corner tangent cones, so the finite-m lattice obstruction does not damage the viscosity boundary consistency.
7. The Issue-#55 counterexample sequence `s_m = (0, i_t^m(0) − 2), μ = (0, 1)` is an interior (non-W-active) state whose own cone is the a=0 face law {μ_a ≥ 0}; its drift violates only the raw graph test, not the legitimate operator test.
8. A minimal 1D state-constraint toy discriminator answers YES: a monotone scheme with interior points near a constrained boundary admitting outward drift is still viscosity-consistent (analytic proof; no simulation).
9. The frozen finite-process architecture satisfies the consistency components of the legitimate target at the design level; monotonicity normalization, stability and the project-specific comparison hypotheses are enumerated deliverables of the next boundary-HJB scheme-design gate (not gaps of this audit).
10. Conclusion: the Issue-#55 raw graph target is over-strong; the viscosity/operator consistency target is frozen; the frozen process is consistent with it at the design level.

**Terminal:**

`DLH_5VH_STATE_CONSTRAINT_VISCOSITY_CONSISTENCY_TARGET_FROZEN__ISSUE55_GRAPH_TARGET_OVERSTRONG__READY_FOR_BOUNDARY_HJB_SCHEME_DESIGN_GATE`

---

## Authority

- Live `main` at activation-refresh: `5d38c644ec1a06359241f9c3418dcd815c938ec6` (verified by fresh fetch; Issue #56 remains OPEN).
- Activation comments: `5641527846` (initial activation), `5641534701` (activation refresh, final CURRENT sync).
- Owner route decision: `APPROVE_DLH_5VH_ROUTE_E_STATE_CONSTRAINT_HJB_CONSISTENCY_TARGET_AUDIT`.
- Accepted household source (read-only, blob verified): `src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py` = `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`.
- Consumed, not reopened: Issue #54 (`b9dab7b6cf5d724074765ddb88d6f300175f6c6f` / acceptance `5633995486` / integration `4e77d9c753f81eb2517a8b90a0827db6af8faed4`), Issue #55 Outcome C (`15f2f81653a847344d2cd647705487cc893af1d7` / acceptance `5635802416` / integration `8dd5e9c444d7356736f28a29b9ffe492bbe81caa`).

---

## Primary-theory provenance

Cited with metadata only (no copyrighted PDFs, no long quotations). Standard theorem content is stated at concise level; exact hypotheses must be confirmed against the primary texts. Per project evidence rules this is machine-verified metadata + standard-content level (E2-class), explicitly marked where project-specific verification remains open.

| Reference | DOI / metadata | Role in this audit | Sign / domain / boundary mapping | Proved vs unproved |
|---|---|---|---|---|
| H. M. Soner (1986), "Optimal Control with State-Space Constraint I" | SIAM J. Control Optim. 24(3):552–561, DOI `10.1137/0324032` | State-constrained optimal control; value function characterized via HJB with the state-constraint boundary condition; dynamic-programming approximation convergence | Maximization convention maps to project's `ρV = sup{u − vl + V_a μ_a + V_b μ_b}`; state constraint = viscosity subsolution on the closed domain (test functions touching from above at any point of the closure), supersolution in the open domain | Proved in source under its hypotheses (Lipschitz dynamics, convex compact state set, discounting). Project-specific hypothesis check (project D_W, drift set, regularity) = open deliverable of the next gate |
| H. M. Soner (1986), "Optimal Control with State-Space Constraint II" | SIAM J. Control Optim. 24(6):1110–1122, DOI `10.1137/0324067` | Comparison / uniqueness for the state-constrained HJB; the state-constraint boundary condition inside the comparison class | One-sided boundary: subsolution on closure vs supersolution in the interior; the boundary inequality is a subsolution inequality only | Proved in source under hypotheses (Lipschitz value, convex domain, viability of the constrained dynamics). Project-specific viability check (tangent cones T_D with the household drift reachability) = open deliverable |
| G. Barles, P. E. Souganidis (1991), "Convergence of approximation schemes for fully nonlinear second order equations" | Asymptotic Analysis 4(3):271–283, DOI `10.3233/ASY-1991-4305` | Framework: monotone + stable + consistent ⟹ locally uniform convergence (with comparison for the limit problem). Consistency is operator/test-function based, NOT drift-set-graph based | Scheme consistency: `S(ρ, x, φ(x), φ) → F(x, φ(x), Dφ, D²φ)` for smooth test functions; stability and monotonicity are explicit hypotheses | The generic theorem as stated is for equations on the whole space / with comparison; the state-constraint boundary extension is the project-specific mapping supplied in this audit (one-sided boundary consistency + state-constraint comparison) |
| I. Capuzzo-Dolcetta, P.-L. Lions (1990), "Hamilton–Jacobi equations with state constraints" | Trans. Amer. Math. Soc. 318(2):643–683, DOI `10.1090/S0002-9947-1990-0951880-0` | Viscosity theory for HJ equations with state constraints; the state-constraint boundary condition and comparison | The boundary condition is a one-sided inequality at the constraint; interior equation in the open domain | Standard; project mapping as above |
| M. Bardi, I. Capuzzo-Dolcetta (1997), "Optimal Control and Viscosity Solutions of Hamilton–Jacobi–Bellman Equations", Birkhäuser, Ch. IV | Book; Ch. IV treats state-constrained problems and the constrained Hamiltonian `H_T(x,p) = sup_{u : μ(x,u) ∈ T_D(x)} {…}` | Constrained (tangent-cone-restricted) Hamiltonian; equivalence of the tangent-cone and subsolution-on-closure formulations; state-constraint comparison | Project's active-face laws (a=0: μ_a ≥ 0; b=b_min: μ_b ≥ 0; a=a_max: μ_a ≤ 0; W: μ_a + μ_b ≤ 0) are exactly the tangent-cone restrictions of the constrained Hamiltonian | Standard equivalence theorem; project-specific verification enumerated |

### What is proved in this audit (at design level, with exact algebra)

1. **Trichotomy answer (Issue C):** the raw Kuratowski admissible-set graph target is sufficient but **over-strong** — not necessary for viscosity/operator consistency. Supporting argument: (i) the half-relaxed-limit machinery requires only operator/test-function consistency at the states used by the near-maximizer/near-minimizer sequences; (ii) cone-monotonicity of the Hamiltonian (Lemma, Section 3 of the necessity audit); (iii) the 1D toy discriminator falsifies necessity by construction (a monotone scheme violating the raw graph condition at interior points near the boundary that is still viscosity-consistent).
2. **Corner-cone representability:** at every lower-a W-contact cell, REV = cone{w_RT, w_down} ⊆ represented cone R(s); at every upper-a W-contact cell, TDEP = cone{w_left, w_down, w_T} ⊆ R(s). Exact enumeration: 0 violations for m = 1..25, W_max ∈ {8, 10, 12} (scratch `%TEMP%\dlh5vh_corner_cone.py`).
3. **Issue-54 orientations:** the missing endpoint orientations are outside the corner tangent cones (w_T ∉ REV since μ_a < 0; w_RT ∉ TDEP since μ_a > 0), hence H_R ≥ H_T at both W-corners and the viscosity boundary consistency survives the finite-m lattice obstruction.
4. **Issue-55 sequence re-test:** `s_m = (0, i_t^m(0) − 2), μ = (0, 1)` violates only the raw graph test; under the legitimate operator test it is interior-consistent (its own cone {μ_a ≥ 0} is the a=0 face law) and the boundary subsolution at (0, W_max) is safe by cone containment.
5. **Toy discriminator:** YES (analytic proof, Section 5 of the monotone-scheme report).

### What remains unproved (explicitly enumerated, scope of the next boundary-HJB scheme-design gate)

1. Monotonicity normalization of the future scheme (row-sum/discount condition ρ ≥ max_α Σ_r q_α in operator form; automatically satisfied in the scaled discounted representation) — a scheme-design choice.
2. Stability of the discrete value functions in the project's rate normalization (standard discounted argument, needs the payoff bounds) — scheme-gate deliverable.
3. Project-specific verification of the state-constraint comparison hypotheses (convexity of D_W, Lipschitz Hamiltonian, viability of the reachable drift set against the tangent cones, ρ > 0) — theory deliverable of the next gate.
4. The full convergence theorem u_m → V (composition of the above with the consistency components verified here) — next gate.

No copyrighted material is committed; all primary references appear as metadata/DOI + concise standard-content statements.
