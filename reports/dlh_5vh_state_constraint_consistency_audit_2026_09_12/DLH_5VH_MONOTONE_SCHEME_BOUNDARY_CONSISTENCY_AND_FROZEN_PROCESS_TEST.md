# DLH-5V-H — Monotone-Scheme Boundary Consistency and Frozen-Process Test

**Sequence steps D, E, F of Issue #56.** Defines the weakest defensible numerical target (D), tests the frozen finite-process architecture against it (E) with explicit corner operator algebra, and supplies the mandatory analytic toy discriminator (F).

---

## Part D — The weakest defensible numerical target

### D.1 Scheme operator (Bellman level)

Let u_m be the discrete value function on the level-m grid. The scheme is the discounted Bellman fixed point

```text
ρ u_m(s) = max_{α ∈ A_m(s)} { g(s, α) + Σ_r q_α(s, r) (u_m(r) − u_m(s)) }        (S_m(s, u_m) = 0)
```

with A_m(s) the discrete candidate set at state s, q_α(s, r) ≥ 0 off-diagonal transition rates (frozen nonnegative-Markov structure), g the running payoff, and the equivalent scaled form `u_m(s) = max_α { (g(s,α) + Σ_r q_α(s,r) u_m(r)) / (ρ + Σ_r q_α(s,r)) }`.

The target fixes the operator form S_m(ρ, s, u(s), u) := ρu(s) − max_α { g + Σ q (u(r) − u(s)) } and requires:

- **Monotonicity:** in the operator form, the row-sum condition ρ ≥ max_α Σ_r q_α(s, r) at every s; in the scaled discounted form this is automatic (nonnegative transition kernel). The future scheme must be written in a normalization satisfying it; this is a scheme-design choice, recorded as a deliverable of the next gate.
- **Stability:** uniform boundedness of (u_m) (discounted problem with bounded payoffs and the frozen bounded drift/reward structure); standard argument, deliverable of the next gate.
- **Interior consistency:** for every x̂ ∈ D_W° and every φ ∈ C², for every sequence of interior states s_m → x̂:
  `S_m(s_m, φ) → F(x̂, φ(x̂), Dφ(x̂)) = ρφ(x̂) − H(x̂, Dφ(x̂))`, with remainder `|S_m(s_m,φ) − [ρφ(s_m) − H(s_m, Dφ(s_m))]| ≤ ½ ‖D²φ‖ · max_α Σ_r q_α |w|² = O(1/m)` (frozen scaling: rates O(m), steps O(1/m)).
- **Boundary consistency (one-sided, subsolution side):** for every x̂ ∈ ∂D_W and every φ ∈ C² touching a candidate subsolution from above at x̂, along the near-maximizer sequences used by the half-relaxed-limit construction:
  `limsup_m S_m(s_m, φ) ≤ 0`, where the operator limit uses the discrete cone R(s_m) at the states actually visited. The target requires only that the states' cones satisfy R(s_m) ⊇ T_D(x̂) at the limit (cone containment at corners), so that H_R ≥ H_T and the state-constraint subsolution inequality ρV ≤ H_T ≤ H_R transfers. Interior states approaching the boundary are NOT required to shrink their cones to T_D(x̂).
- **Half-relaxed limits / test-function requirements:** ū = limsup* u_m is a viscosity subsolution on D̄_W (near-maximizer sequences + monotonicity + the above consistencies); u̲ = liminf* u_m is a viscosity supersolution in D_W° (near-minimizer sequences + interior consistency). The grid-state/test-function sequences that must be controlled are exactly: (i) interior-state sequences for interior consistency; (ii) near-maximizer/near-minimizer sequences at boundary points (any states realizing them — the one-sided cone-containment makes both interior and boundary-contact realizations safe); (iii) nothing else. In particular, no sequence of interior states approaching a boundary is required to satisfy a drift-set graph condition.
- **Comparison / uniqueness (hypothesis):** a state-constraint comparison principle for the limit problem: ū ≤ u̲ on D̄_W, hence ū = u̲ = V. This is the Soner-II / Capuzzo-Dolcetta–Lions comparison class (subsolution on closure vs supersolution in interior) with hypotheses (convex D_W, Lipschitz Hamiltonian, viability of the constrained dynamics, ρ > 0); project-specific verification is an enumerated deliverable of the next gate.
- **Asymmetry (subsolution/supersolution):** the boundary condition is one-sided — subsolution on the closure, supersolution in the interior. There is no symmetric boundary condition and no symmetric graph condition.

**What is NOT part of the legitimate target:** Kuratowski outer/limsup + recovery/liminf of admissible-drift sets at arbitrary convergent state sequences (the Issue-#55 raw target); equality of interior-state admissible cones with the boundary tangent cone; any invented min/max boundary operator not derived from the tangent-cone/cones-containment structure above (none is introduced anywhere in this audit).

---

## Part E — Frozen-process test against the legitimate target

### E.1 Mandatory question 1: does `s_m = (0, i_t^m(0) − 2), μ = (0, 1)` violate a legitimate viscosity/operator test, or only the raw graph test?

**Only the raw graph test.** The state is interior (non-W-active: i = i_t − 2). Its frozen cone is exactly {μ_a ≥ 0} (three-neighbor {w_right, w_up, w_down} = {μ_a ≥ 0}; BA1 a=0 face law). The drift μ = (0, +1) has μ_a = 0 ≥ 0, so it is admitted and exactly represented (q_up = 19m/7, destination (0, i+1) represented). Under the legitimate target:

- Interior consistency at s_m holds with the a=0-face operator: for φ ∈ C², `S_m(s_m, φ) → ρφ(x̂) − H_{μ_a≥0}(x̂, Dφ(x̂))`, x̂ = (0, W_max), remainder O(1/m) (frozen second moments; the cell is not W-active, so the W-face rates are absent and the pure a=0 face cone is exact).
- Cone containment: {μ_a ≥ 0} ⊇ REV = T_D(0, W_max); hence H_{μ_a≥0} ≥ H_T and the one-sided subsolution inequality ρV ≤ H_T ≤ H_{μ_a≥0} holds for every touching test function. The boundary subsolution at the corner transfers from ANY near-maximizer sequence, whether it visits these interior cells or the W-contact cells.
- The drift μ_W = +1/19·(7) = +7/19 > 0 is outward at the corner limit — this is precisely why the raw outer/limsup condition fails (accepted #55), and precisely why the raw condition is over-strong: the viscosity test is a statement about the Hamiltonian max over the cone, not about membership of individual drifts.

### E.2 Mandatory question 2: upper-corner analogue

`s_m = (19m, i_t^m(19m) − 2), μ = (−1, +2)` → x̂ = (a_max, W_max − a_max). The state is interior; own cone {μ_a ≤ 0} (a_max face law) ⊇ TDEP = T_D(a_max, W_max − a_max). Interior consistency with H_{μ_a≤0}; H_{μ_a≤0} ≥ H_T; subsolution-safe. **No violation of the legitimate test** (raw graph test fails, accepted #55).

### E.3 Mandatory question 3: may interior states approaching a boundary remain interior-consistent without their admissible set equaling the boundary tangent cone?

**YES.** This is the content of cone-monotonicity + the one-sided boundary structure:

- Subsolution side: cones ⊇ T_D(x̂) only enlarge the Hamiltonian, which relaxes the subsolution inequality ρV ≤ H (larger H is easier).
- Supersolution side: interior supersolution is required only in the interior (w.r.t. H_int = full cone); the boundary supersolution (w.r.t. H_T, when the comparison class requires it) is sustained by the W-contact states' own consistency and by H_T ≤ H_int.
- The toy discriminator (Part F) demonstrates the mechanism in minimal form: interior points near the boundary admitting outward drifts, yet the scheme is viscosity-consistent.

### E.4 Mandatory question 4: at the actual discrete W-contact states, does the frozen process satisfy the legitimate one-sided boundary test?

**YES, at the design level, with exact verification.** The discrete cone at a W-contact state s is R(s) = cone of represented drift destinations. The legitimate boundary test at the W-corner x̂ needs R(s) ⊇ T_D(x̂) so that H_R ≥ H_T.

**Lower-a × W corner algebra (explicit).**

- Corner (0, W_max): T_D = REV = {μ_a ≥ 0, μ_W ≤ 0} = cone{w_RT, w_down} with w_RT = (+70/(19m), −70/(19m)) (mirror wide stencil (j,i) → (j+7, i−10), ΔW = 0) and w_down = (0, −7/(19m)) (ΔW < 0).
- At every lower-a W-contact cell (top (j, i_t(j)) and, when present, sub-top (j, i_t(j)−1), j ∈ {0, …, 7m−1}): mirror available iff j ≤ 19m−7 and i ≥ 10; w_down available iff i ≥ 1. In the lower-a band (j < 7m) every W-contact cell has i_t(j) = ⌊(N_m − 10j)/7⌋ ≥ ⌊(19m(W_max+2) − 70m)/7⌋ ≥ ⌊120m/7⌋ ≥ 17 for W_max ≥ 8, so top i ≥ 17 and sub-top i ≥ 16 — both ≥ 10 — and both w_RT and w_down are represented. (The W-active sub-top with i = 9 < 10 — the (19m−7, 9) case of the Issue-#55 micro-revision — lies in the upper-a band and is covered by the upper-corner check below, whose generators do not require the mirror.)
- **Exact check (scratch, `%TEMP%\dlh5vh_corner_cone.py`):** for m = 1..25 and W_max ∈ {8, 10, 12}, every W-contact cell in the lower-a band (j < 7m) has {w_RT, w_down} ⊆ R(s); every W-contact cell in the upper-a band (j > 12m) has {w_left, w_down, w_T} ⊆ R(s). Result: **0 violations**.
- Consequently H_R ≥ H_T at the lower corner, the one-sided subsolution inequality holds, and the boundary consistency of the scheme at the lower-a×W corner is satisfied.

**Upper-a × W corner algebra (explicit).**

- Corner (a_max, W_max − a_max): T_D = TDEP = {μ_a ≤ 0, μ_W ≤ 0} = cone{w_left, w_down, w_T} with w_left = (−10/(19m), 0), w_down = (0, −7/(19m)), w_T = (−70/(19m), +70/(19m)) (forward wide stencil (j,i) → (j−7, i+10), ΔW = 0).
- At every upper-a W-contact cell (j ∈ {12m+1, …, 19m}, i ≥ 10): w_left (j ≥ 1), w_down (i ≥ 1), w_T (j ≥ 7) all represented; containment TDEP ⊆ R(s); exact check 0 violations.
- H_R ≥ H_T at the upper corner; one-sided boundary test satisfied.

**Regular W-band (j ∈ {7m, …, 12m}):** the accepted sector contracts represent the full W-face tangent cone T_W = {μ_W ≤ 0} = T_realloc ∪ R_reverse ∪ R_deplete exactly (5V-A..E algebra), so H_R = H_T exactly on the regular W-band.

**Face laws:** a=0, a=a_max, b=b_min interior-face states carry the exact face-law cones {μ_a ≥ 0}, {μ_a ≤ 0}, {μ_b ≥ 0} (exact three/four-neighbor representations, accepted 5V-G Case B/A algebra). The b_min corner (a_max, b_min) for W_max > 8 has true cone {μ_a ≤ 0, μ_b ≥ 0}; every cell approaching it carries its own-position face-law cone — {μ_a ≤ 0} (a_max face), {μ_b ≥ 0} (b_min face), full plane (interior), or the exact triple {μ_a ≤ 0, μ_b ≥ 0} at the corner cell (19m, 0) — each of which contains the true corner cone, hence H_own ≥ H_true and the one-sided test is satisfied. W-active lower-b cells (buffered cone TREA = {μ_b ≥ 0, μ_W ≤ 0} ⊊ true) exist only for finitely many m when W_max > 8 (Issue-#55 fact F5: they vanish for m > 69/(19(W_max − 8))), and finitely many levels are irrelevant to the m → ∞ half-relaxed limit. For W_max = 8 the corner is the triple (a_max, b_min) with true cone = TREA exactly.

### E.5 Mandatory question 5: does the Issue-54 finite-m obstruction still kill the scheme under the legitimate viscosity target?

**NO.** The Issue-54 obstruction (accepted, consumed) is: at exact-frontier (r_j = 0) endpoint cells, every represented destination has ΔW ≤ 0, and the exact tangent drift can require a same-W lattice orientation unavailable on the native endpoint band — the missing orientation being the forward w_T at lower-band cells (j < 7) and the mirror w_RT at upper-band cells (j > 12m−7).

Under the legitimate viscosity target this obstruction is harmless, because the missing orientations are exactly the directions the corner laws exclude:

- w_T = (−70/(19m), +70/(19m)) has μ_a = −70/19 < 0 ⇒ **w_T ∉ REV** (the lower corner cone requires μ_a ≥ 0).
- w_RT = (+70/(19m), −70/(19m)) has μ_a = +70/19 > 0 ⇒ **w_RT ∉ TDEP** (the upper corner cone requires μ_a ≤ 0).
- The corner cones' generators (w_RT, w_down at the lower corner; w_left, w_down, w_T at the upper corner) are all represented at the exact-frontier cells (mirror has ΔW = 0 and is available; w_T has ΔW = 0 and is available at j ≥ 7), so T_D ⊆ R(s) at both corners and H_R ≥ H_T is preserved.

The Issue-54 obstruction concerns exact pointwise first-moment representability of *every* tangent direction at *every* endpoint cell (a finite-m lattice identity, universal for N ≥ 190) — a genuinely different object from operator consistency. The discrete Hamiltonian at the endpoint cells remains ≥ H_T at the corner limits, so the legitimate boundary test is unaffected.

---

## Part F — Mandatory toy discriminator (analytic; no simulation)

### F.1 The toy

1D state-constrained problem: state x ∈ [0, 1]; control d ∈ [−1, 1] with state constraint x(t) ∈ [0, 1]. Drift μ(x, d) = d; the tangent cones: T(0) = [0, 1] (outward drifts d < 0 infeasible at 0), T(1) = [−1, 0], T(x) = [−1, 1] for x ∈ (0, 1). Running payoff g(d) bounded and concave; discount ρ > 0. Continuous target:

```text
ρ V(x) = max_{d ∈ T(x)} { g(d) + V'(x) d },   V subsolution on [0,1], supersolution in (0,1).
```

Monotone upwind scheme: grid x_i = i/m (i = 0..m); forward difference for d > 0, backward for d < 0; discrete admissible sets A_m(x_i) = T(x_i) (boundary points restricted, interior points full):

```text
ρ u_m(x_i) = max_{d ∈ A_m(x_i)} { g(d) + m·d⁺(u_m(x_{i+1}) − u_m(x_i)) + m·d⁻(u_m(x_i) − u_m(x_{i−1})) }.
```

### F.2 The discriminator question and answer

**Question:** can a monotone scheme with interior points near a constrained boundary that admit outward drift still be viscosity-consistent via the correct test-function/half-relaxed-limit mechanism?

**Answer: YES** (analytic proof, no simulation).

1. **Raw graph failure (by design):** interior points x_i = 1/m → 0 admit d < 0, so limsup A_m(x_i) ⊇ [−1, 1] ⊄ [0, 1] = T(0) — the Issue-55-style raw graph outer condition fails, identically in spirit to `(0, i_t−2), μ = (0, +1)`.
2. **Interior consistency:** at x ∈ (0,1), for φ ∈ C²: `S_m(x_i, φ) → ρφ(x) − H_int(x, φ'(x))` with H_int(x,p) = max_{d ∈ [−1,1]} {g(d) + p d} (Taylor expansion, upwind exactness, O(1/m) remainder). Both inequalities hold at interior test points.
3. **Boundary consistency (one-sided, subsolution side):** at x̂ = 0, φ touching a subsolution candidate from above. The half-relaxed-limit near-maximizer sequence either visits x_0 = 0 (operator limit H_T(0, p) = max_{d ∈ [0,1]} {g + pd}; the subsolution inequality ρV ≤ H_T holds by the continuous target) or interior points x_i → 0 (operator limit H_int(0, p) = max_{d ∈ [−1,1]} {g + pd} ≥ H_T(0, p) by cone containment [0,1] ⊆ [−1,1]; the inequality ρV ≤ H_T ≤ H_int holds a fortiori). Either realization gives limsup S_m ≤ 0. Same argument at x̂ = 1.
4. **Supersolution side:** near-minimizer sequences in the interior give ρφ ≥ H_int (interior supersolution). At the boundary, the (constrained) supersolution ρV ≥ H_T follows from the boundary point's restricted set (sequence visiting x_0 = 0) or is not needed if the Soner comparison class (subsolution on closure vs supersolution in interior) is used.
5. **Comparison:** the 1D state-constrained problem has the Soner-type comparison (provenance capsule); hence ū ≤ u̲, u_m → V locally uniformly.

**Conclusion of the toy:** interior points near a constrained boundary may admit outward drift without any loss of viscosity consistency; the state-constraint boundary is enforced through (i) the boundary points' restricted admissible sets (the discrete tangent cone at the actual boundary states) and (ii) cone-monotonicity of the Hamiltonian, which makes larger interior cones harmless on the subsolution side. The raw graph condition is therefore not necessary — a scheme violating it can still be fully viscosity-consistent. The 2D analogue at the project's W-corners is the same mechanism with REV/TDEP in place of [0,1]: interior (non-W-active) cells carry cones ⊇ the corner cone, W-contact cells carry R ⊇ REV/TDEP, and both are subsolution-safe by the identical cone-monotonicity argument.

---

## Summary of Part D+E+F

- Legitimate target: monotone + stable + interior-consistent + one-sided boundary-consistent (cones ⊇ T_D at the boundary states) + state-constraint comparison.
- Frozen process: satisfies all consistency components at the design level (exact cone laws, O(1/m) moment scaling, exact corner-cone containment REV/TDEP ⊆ R — 0 violations).
- Issue-55 sequence and upper-corner analogue: violate only the raw graph test; legitimate operator test unaffected.
- Issue-54 obstruction: does not kill the scheme under the legitimate target (missing orientations are outside the corner cones).
- Toy: YES, with the analytic mechanism above.
