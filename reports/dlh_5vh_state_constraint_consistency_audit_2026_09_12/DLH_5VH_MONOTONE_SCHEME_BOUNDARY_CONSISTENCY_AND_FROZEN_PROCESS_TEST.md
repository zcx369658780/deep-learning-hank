# DLH-5V-H — Monotone-Scheme Boundary Consistency and Frozen-Process Test (Micro-Rev Rev 2)

**Sequence steps D, E, F of Issue #56; Micro-Rev Rev 2 (Reviewer comment `5642335215`).** Defines the weakest defensible numerical target (D) with the corrected monotonicity and the **quantifier-corrected** half-relaxed-limit derivation; tests the frozen finite-process architecture against it (E) with the **local-state same-candidate recovery lemma** (rates generated from the drift of the SAME candidate at the ACTUAL state s_m, per the binding candidate→rates→score→argmax→Q law) under the frozen finite-m taxonomy; supplies the mandatory analytic toy discriminator with a full component proof and the corrected max quantifier (F).

**Rev-2 scope:** the Rev-1 repairs (A–F of comment `5641997550`) are preserved; this revision fixes (i) the invalid "max ⟹ every candidate" inference in §D.2, (ii) the limit-state rate construction in §E.4 — replaced by genuine local-state recovery, (iii) the toy's boundary argument under the corrected quantifier, and re-states the terminal honestly.

---

## Part D — The weakest defensible numerical target

### D.1 Scheme operator and corrected monotonicity (kept from Rev 1)

Let u_m be the discrete value function. The scheme is the discounted Bellman fixed point:

```text
Residual form:    S_m(s, u) = ρ u(s) − max_α { g(s,α) + Σ_{j≠s} q_α(s,j) (u(j) − u(s)) } = 0.
Scaled form:      u(s) = T_m(u)(s),   T_m(u)(s) = max_α { [ g(s,α) + Σ_{j≠s} q_α(s,j) u(j) ] / [ ρ + Σ_{j≠s} q_α(s,j) ] }.
```

with q_α(s,j) ≥ 0, ρ > 0. For each fixed candidate the residual is `(ρ + Σ q)u(s) − Σ q u(j) − g` with **positive diagonal** ρ + Σ q ≥ ρ > 0 and **nonpositive off-diagonals** −q ≤ 0 (proper M-matrix structure). **No condition ρ ≥ Σ q** (incompatible with q = O(m)). Monotonicity = **order-preservation of the scaled operator**: weights w_α(s,j) = q_α/(ρ + Σ q) ≥ 0 with Σ_j w_α < 1; u ≥ v ⟹ T_m(u) ≥ T_m(v); strict sup-norm contraction ⟹ unique fixed point. Stability: max-principle gives ‖u_m‖∞ ≤ ‖g‖∞/ρ uniformly in m. (Convention: F = ρu − H, subsolution = F ≤ 0; continuous-target report §2.3.)

### D.2 Half-relaxed-limit derivation (Rev 2 — quantifier corrected)

**Setup.** ū := limsup* u_m, u̲ := liminf* u_m. Let x̂ ∈ D̄ and φ ∈ C²(D̄) touch ū from above at x̂; set φ_ε = φ + ε|x − x̂|² so that ū − φ_ε has a strict local maximum at x̂. Let s_m be near-maximizers of u_m − φ_ε in a neighborhood of x̂: s_m → x̂, c_m := (u_m − φ_ε)(s_m) → 0, and u_m ≤ φ_ε + c_m near s_m (so u_m(s_m) = φ_ε(s_m) + c_m).

**Contact step (valid for EVERY candidate).** At a local near-maximum, for every candidate α with local support (all j in the sum near s_m):

```text
u_m(j) − u_m(s_m) ≤ (φ_ε(j) + c_m) − (φ_ε(s_m) + c_m) = φ_ε(j) − φ_ε(s_m).
```

Hence for every α:

```text
g(s_m,α) + Σ_j q_α(s_m,j)[u_m(j) − u_m(s_m)] ≤ g(s_m,α) + Σ_j q_α(s_m,j)[φ_ε(j) − φ_ε(s_m)].
```

**Max step (the outer maximum is RETAINED — no per-α inference).** Taking max over α on both sides is valid because the left inequality holds candidatewise (max is nondecreasing):

```text
ρu_m(s_m) = max_α { g + Σ q [u_m(j) − u_m(s_m)] } ≤ max_α { g(s_m,α) + Σ_j q_α(s_m,j)[φ_ε(j) − φ_ε(s_m)] }.
```

Substituting u_m(s_m) = φ_ε(s_m) + c_m and Taylor-expanding candidatewise **inside the maximum** — for each α the exact first moment is the candidate's drift at s_m, Σ_j q_α(x_j − x_s) = μ_α(s_m), with remainder ≤ ½‖D²φ_ε‖·max_α Σ_j q_α|x_j − x_s|² → 0 uniformly in α (frozen scaling: rates O(m), steps O(1/m), second moments O(1/m); the max is 1-Lipschitz so the uniform remainder passes through it):

```text
ρφ_ε(s_m) ≤ max_α { g(s_m,α) + Dφ_ε(s_m)·μ_α(s_m) } + o(1).
```

**Subsolution conclusion.** Define the discrete Bellman Hamiltonian at the visited states:

```text
H_m(s_m, p) := max_{α ∈ A_m(s_m)} { g(s_m,α) + p·μ_α(s_m) },   H_lim(x̂, p) := limsup_m H_m(s_m, p).
```

Taking limsup along the sequence (Dφ_ε(s_m) → Dφ(x̂), then ε → 0):

```text
ρφ(x̂) ≤ H_lim(x̂, Dφ(x̂)).
```

**ū is a viscosity subsolution w.r.t. H_lim** (project convention). The per-candidate inequality is NOT asserted; only the max form is used.

**Supersolution direction (analogous, quantifier-checked).** Let φ touch u̲ from below at x̂ ∈ D° and let s_m be near-minimizers of u_m − φ_ε (u_m ≥ φ_ε + c_m near s_m). Contact step: u_m(j) − u_m(s_m) ≥ φ_ε(j) − φ_ε(s_m) for every α, so candidatewise L_α ≥ R_α; the max is nondecreasing, so max_α L_α ≥ max_α R_α, and since max_α L_α = ρu_m(s_m):

```text
ρφ_ε(s_m) ≥ max_α { g(s_m,α) + Σ_j q_α[φ_ε(j) − φ_ε(s_m)] } − ρ|c_m|
⟹  ρφ(x̂) ≥ H_lim(x̂, Dφ(x̂))   at x̂ ∈ D°  (supersolution in the interior).
```

**Interior consistency.** At interior states the candidate sets represent the reachable drifts (interior recovery, §E.4 machinery without cone restrictions), so H_lim = H_proj at interior test points and both inequalities hold with H_proj — the standard interior consistency statement.

**Boundary one-sided transfer (Rev 2 — closed by the restriction, not by a constrained characterization).** At x̂ ∈ ∂D the near-maximizer sequence visits either interior states or W-contact states:

- **Interior-state branch:** H_lim = H_proj (recovery + restriction, §E.4), so ρφ(x̂) ≤ H_proj(x̂, Dφ) — the Soner-form subsolution on the closure (continuous-target report §2.2).
- **W-contact-state branch:** H_m(s_m, p) = max over the **buffered candidate set** at s_m ⊆ the full household candidate set, hence the pointwise restriction

```text
H_m(s_m, p) ≤ H_proj(s_m, p) := max_{α ∈ A_full(s_m)} { g(s_m,α) + p·μ(s_m,α) }
```

and H_proj(s_m, p) → H_proj(x̂, p) (the feasibility bounds of the candidate set are continuous — Hausdorff convergence of the compact candidate sets along s_m → x̂). Therefore

```text
ρφ(x̂) ≤ H_lim(x̂, Dφ) ≤ H_proj(x̂, Dφ).
```

The boundary subsolution w.r.t. the FULL Hamiltonian H_proj is thereby established at every boundary point, in both branches, WITHOUT the constrained characterization ρV ≤ H_T. (The recovery-side statement liminf H_R ≥ H_T — the tangent-cone values are attained by the discrete operators — is the content of the control/payoff bridge, §E.4, and serves the geometric identification of the boundary operators; it is not the load-bearing piece of the transfer.)

**What remains for convergence.** The halves ū (subsolution on the closure w.r.t. H_proj) and u̲ (supersolution in the interior w.r.t. H_proj) pass to the limit u_m → V only through a **comparison/unique-continuation theorem for the project's continuous state-constrained problem** (subsolution on the closure vs supersolution in the interior — the Soner II / Capuzzo-Dolcetta–Lions maximal-subsolution form). Its project-specific applicability is **NOT established in this audit — the single bounded Outcome-B gap** (declared in §E.6 and the terminal report). The constrained characterization ρV ≤ H_T at the boundary is NOT established either and is NOT needed for the transfer; it is a coupled sublemma of the same boundary block (it would identify the boundary limit as the H_T-constrained solution — a stronger identification than the convergence needs).

---

## Part E — Frozen-process test against the legitimate target

### E.1 Mandatory question 1: `s_m = (0, i_t^m(0) − 2), μ = (0, 1)`

**Only the raw graph test is violated; the operator-consistency components are not.** The state is interior (non-W-active). Its frozen cone is exactly {μ_a ≥ 0} (three-neighbor {w_right, w_up, w_down}). The drift μ = (0, 1): μ_a = 0 ≥ 0 — admitted; represented by w_up = (0, 7/(19m)) with q_up = 19m/7, first moment (0, 1). **μ_W = μ_a + μ_b = 1** (physical units; the jump size 7/(19m) is a distinct object). Interior consistency at s_m holds with the a=0-face operator (O(1/m) remainder). The raw graph condition fails because μ_W = 1 > 0 at the corner limit — the over-strong content (necessity audit §4). The boundary subsolution at the corner holds via the §D.2 transfer (both branches, restriction H_lim ≤ H_proj); no constrained characterization is invoked.

### E.2 Mandatory question 2: upper-corner analogue

`s_m = (19m, i_t^m(19m) − 2), μ = (−1, 2)` → (a_max, W_max − a_max): interior state, own cone {μ_a ≤ 0} (a_max face law); operator-consistent; raw graph test violated; boundary transfer closed by the same §D.2 restriction argument.

### E.3 Mandatory question 3: interior states approaching a boundary

**YES** — interior grid states approaching a constrained boundary may remain interior-consistent without their admissible set equaling the boundary tangent cone. Mechanism: (i) the subsolution inequality is one-sided and holds with the full Hamiltonian H_proj (restriction argument, §D.2); (ii) the supersolution is required only in the interior; (iii) the boundary constraint is carried by the W-contact states' own operators and by the boundary treatment. The toy (§Part F) demonstrates the mechanism in minimal form.

### E.4 Mandatory question 4: local-state same-candidate recovery and the control/payoff bridge (Rev 2)

**Preliminary (binding law).** The frozen process obeys: candidate at s_m → admissibility at s_m → local candidate drift μ(s_m, α_m) → rates generated from THAT local drift → candidate-specific discrete Hamiltonian → one global argmax → one backward Q. Rev 1 scored candidates at s_m with rates built from μ(x̂, α) — that broke the same-candidate chain; Rev 2 replaces it with the recovery lemma below.

**Drift structure (verified from the immutable household source, blob `76ae5b1499…`).** For the household candidate α = (c, l, d):

```text
μ_a(x, α) = r_a_eff(a)·a + d,        r_a_eff(a) = r_a·(1 − 0.1·(a/a_max)^9) ≥ 0.9·r_a ≥ 0  (continuous, source lines 101–114, 154–157);
μ_b(x, α) = r_b·b + y(a,b,l) − χ(a,d) − d − c + τ,   y linear in l (continuous via the wage/labor-income map), χ(a,d) = χ_0|d| + ½χ_1 d²/max(a, a_bar) (continuous, source lines 80–83, 138–157);
g(x, α) = u(c) − v_l·l  (independent of x and d — source lines 128–136).
```

**Continuity facts (H1):** μ(x, α) is continuous in (x, α) on D̄_W × (compact control space) — r_a_eff is a polynomial taper, y is linear in l with continuous coefficients, χ is continuous with the a_bar floor, r_b and τ are constants; the feasibility bounds of (c, l, d) (budget/borrowing/transfer bounds) are continuous on D̄_W. **State-error fact (H2):** along the corner families below, |a(s_m) − a*| + |b(s_m) − b*| = O(1/m) (fixed-j cells: a_s = 10j/(19m); 19m−k cells: a_s = 10 − 10k/(19m); b_s = b_min + 7i_t/(19m) with i_t from the class formulas). **Perturbation space (H3):** (c, l, d) with c interior (consumption FOC c = v_b^{−1/γ} > 0 — c + δ_m feasible for large m), l bounded (labor FOC), d bounded (transfer bounds); the payoff g depends only on (c, l) and is continuous.

**Recovery Lemma (local-state same-candidate recovery).** For every continuous viable control/candidate α at a corner/face limit point x̂ (μ(x̂,α) ∈ the accepted corner/face cone), there is a finite-m sequence α_m of actual candidates at the actual states s_m of the corresponding frozen family such that:

1. s_m → x̂ (families below);
2. α_m is admissible at s_m under the frozen buffered law (cone/sign restrictions satisfied at every finite m);
3. α_m → α componentwise;
4. g(s_m, α_m) → g(x̂, α) (exact equality when α_m = α; u(c ± δ_m) → u(c) otherwise);
5. μ(s_m, α_m) → μ(x̂, α) (continuity H1 + H2);
6. the finite-m rates are computed from μ(s_m, α_m) only (never from μ(x̂, α));
7. the accepted sector formulas give Σ_r q_m(s_m, r; α_m)·[x_r − x(s_m)] = μ(s_m, α_m) EXACTLY at every finite m (exact-arithmetic verified for all sector cases);
8. the second moment Σ_r q_m |x_r − x_s|² = O(1/m) → 0;
9. the finite-m sign/admissibility restrictions are satisfied (item 2);
10. the SAME household candidate object (c_m, l_m, d_m) with the SAME running payoff runs through scoring → argmax → Q.

**Construction (corner by corner).**

**Lower corner (0, W_max), cone REV = {μ_a ≥ 0, μ_W ≤ 0}.** Families: fixed-j cells j ∈ {0,…,6} (a_s = 10j/(19m) → 0, b_s → W_max; buffered cone REV) and regular W-active cells j(m) = o(m) (cone {μ_W ≤ 0} ⊇ REV). Let α be viable with μ(x̂,α) ∈ REV.

- **a-side (tangent included, no perturbation needed — proved from the formula):** μ_a(x̂,α) = r_a_eff(0)·0 + d = d ≥ 0, and at s_m: μ_a(s_m, α) = r_a_eff(a_s)·a_s + d ≥ d ≥ 0 because r_a_eff(a_s) ≥ 0.9 r_a ≥ 0 and a_s ≥ 0. **The SAME α is admissible for the a-side at every finite m.**
- **W-side, strict case (μ_W(x̂,α) < 0):** μ_W(s_m, α) = μ_W(x̂, α) + O(1/m) by H1+H2, so μ_W(s_m, α) < 0 for all large m — α_m := α (continuity; no perturbation).
- **W-side, tangent case (μ_W(x̂,α) = 0):** perturb consumption inward: α_m := (c + δ_m, l, d) with δ_m = C_m/m → 0, C_m chosen from the uniform drift bound so that μ_W(s_m, α_m) = μ_W(s_m, α) − δ_m ≤ 0 at every finite m. Then g(s_m,α_m) = u(c + δ_m) − v_l·l → g(x̂,α); μ(s_m,α_m) → μ(x̂,α); the perturbation does not touch μ_a (already fine) and keeps (c,l,d) feasible for large m (H3).

At every such s_m the sector Case-L rates from the LOCAL drift give the EXACT first moment:

```text
q_RT = 19m·μ_a(s_m,α_m)/70 ≥ 0  (mirror),   q_down = 19m·(−μ_W(s_m,α_m))/7 ≥ 0  (down),
q_RT·w_RT + q_down·w_down = (μ_a, −μ_a) + (0, μ_W) = (μ_a(s_m,α_m), μ_b(s_m,α_m))   EXACT;
second moment [2660μ_a + 133(−μ_W)]/(361m) = O(1/m)  (local components).
```

Destinations verified available at every lower-a W-contact cell (mirror: j+7 ≤ 19m−7 and i ≥ 10; down: i ≥ 1 — the class formulas give i_t(j) ≥ 17 for j ≤ 6 and W_max ≥ 8; enumeration supplements, never replaces, the recovery).

**Upper W corner (a_max, W_max − a_max), cone TDEP = {μ_a ≤ 0, μ_W ≤ 0}.** Families: fixed-k cells j = 19m − k, k ∈ {0,…,6} (a_s → 10, b_s → W_max − 10; buffered cone TDEP) and regular cells j(m) = 19m − o(m) (cone {μ_W ≤ 0} ⊇ TDEP).

- **W-side:** as above (strict: α_m = α eventually; tangent μ_W(x̂,α) = 0: c → c + δ_m).
- **a-side, strict (μ_a(x̂,α) < 0):** μ_a(s_m, α) = μ_a(x̂, α) + O(1/m) < 0 eventually — α_m := α.
- **a-side, tangent (μ_a(x̂,α) = 0):** perturb transfer inward: α_m := (c, l, d − ε_m) with ε_m = C_m/m → 0 so that μ_a(s_m, α_m) = μ_a(s_m, α) − ε_m ≤ 0 at every finite m; μ_b increases by ε_m; μ_W unchanged; payoff unchanged (g independent of d); feasibility for large m (H3).

Case-U rates from the LOCAL drift (two-case contract), EXACT first moment:

```text
μ_b(s_m,α_m) ≥ 0:  q_T = 19m·μ_b/70 (forward),  q_left = 19m·(−μ_W)/10 (left),  q_down = 0;
μ_b(s_m,α_m) < 0:  q_left = 19m·(−μ_a)/10 (left),  q_down = 19m·(−μ_b)/7 (down),  q_T = 0;
q_T·w_T + q_left·w_left = (−μ_b, μ_b) + (μ_W, 0) = (μ_a, μ_b)   EXACT (and the μ_b < 0 branch, analogously).
```

Destinations available at every upper-a W-contact cell (forward: j ≥ 7 ✓; left: j ≥ 1 ✓; down: i ≥ 1 ✓ — W-contact cells have i ≥ 10 for W_max ≥ 8; see the triple-corner note below for W_max = 8).

**b_min triple corner (a_max, b_min), W_max = 8, cone TREA = {μ_a ≤ 0, μ_b ≥ 0, μ_W ≤ 0}.** The relevant cells are the W-active lower-b sub-top family (19m−7, 9) — here i = 9, **NOT i ≥ 10** (mirror destination unavailable; the mirror-based Case-L rate does NOT apply at these cells) — and the face cell (19m, 0) (cone {μ_a ≤ 0, μ_b ≥ 0} ⊇ TREA).

- **a-side:** perturb d → d − ε_m (μ_a −= ε_m) as in the upper-corner tangent case.
- **b-side, strict (μ_b(x̂,α) > 0):** μ_b(s_m, α) = μ_b(x̂, α) + O(1/m) > 0 eventually — α_m := α.
- **b-side, tangent (μ_b(x̂,α) = 0):** the SAME ε_m perturbation raises μ_b: μ_b(s_m, α_m) = μ_b(s_m, α) + ε_m ≥ 0.
- **W-side:** c → c + δ_m as above.

Case-B rates from the LOCAL drift (the accepted triple-corner contract — forward + left, no mirror):

```text
q_T = 19m·μ_b/70 ≥ 0 (forward),   q_left = 19m·(−μ_W)/10 ≥ 0 (left),
q_T·w_T + q_left·w_left = (−μ_b, μ_b) + (μ_W, 0) = (μ_a, μ_b)   EXACT.
```

Destinations available at (19m−7, 9): forward (19m−7 ≥ 7 ✓), left (j ≥ 1 ✓). For W_max > 8 the W-active lower-b cells vanish for m > 69/(19(W_max − 8)) (accepted fact F5); the remaining face cells carry their own-position face-law cones containing the true corner cone.

**b_min face cells (i = 0, regular j):** cone {μ_b ≥ 0, μ_W ≤ 0}; b-side tangent via d → d − ε_m, W-side via c → c + δ_m; deplete rates (q_left, q_down) from the local drift, exact first moment (accepted Case-B algebra).

**Regular W-band (7 ≤ j ≤ 19m−7, i = i_t(j)):** cone {μ_W ≤ 0}; the accepted sector contracts (T_realloc ∪ R_reverse ∪ R_deplete) with the local-drift rates (q_T, q_RT, q_left, q_down, and the tangent w_T/w_RT parts as accepted) give the exact first moment μ(s_m, α_m) at every finite m; strict controls: α_m = α eventually; tangent μ_W = 0: c → c + δ_m.

**Recovery-side conclusion (liminf H_R ≥ H_T).** For every viable α at a corner/face limit point and every test function φ ∈ C²:

```text
g(s_m,α_m) + Σ_r q_m(s_m,r;α_m)[φ(x_r) − φ(s_m)] = g(s_m,α_m) + Dφ(s_m)·μ(s_m,α_m) + O(1/m)  →  g(x̂,α) + Dφ(x̂)·μ(x̂,α),
so  liminf_m H_m(s_m, Dφ) ≥ H_T(x̂, Dφ) := sup_{α : μ(x̂,α) ∈ T_D(x̂)} { g(x̂,α) + Dφ(x̂)·μ(x̂,α) }.
```

**Restriction-side conclusion (limsup H_R ≤ H_proj).** H_m(s_m, p) ≤ H_proj(s_m, p) → H_proj(x̂, p) (buffered candidate sets ⊆ full candidate sets; Hausdorff convergence of the feasibility bounds). Hence at the corners/faces:

```text
H_T(x̂, Dφ) ≤ liminf_m H_R(s_m, Dφ) ≤ limsup_m H_R(s_m, Dφ) ≤ H_proj(x̂, Dφ),
```

which is the geometric/control content of the boundary operators and — with §D.2 — closes the boundary subsolution transfer at the W-contact states (ρφ ≤ H_lim ≤ H_proj) WITHOUT any constrained characterization.

**Status (honest):** the local-state same-candidate bridge is **PROVED** at the design level: the α_m constructions are explicit (α, or the δ_m/ε_m inward perturbations with explicit O(1/m) bounds), every rate is generated from μ(s_m, α_m), the exact first-moment identities and the O(1/m) second moments are exact-arithmetic-verified, and all continuity/feasibility hypotheses (H1–H3) are verified from the immutable household source. Finite-m destination enumeration supplements (never replaces) the recovery: enumeration proves stencil availability only.

### E.5 Mandatory question 5: the Issue-54 obstruction under the operator target

The finite-m lattice obstruction does not damage the bridge at the W-corners. The missing orientations are exactly the directions the corner laws exclude: w_T has μ_a = −70/19 < 0 ⟹ w_T ∉ REV (lower corner); w_RT has μ_a = +70/19 > 0 ⟹ w_RT ∉ TDEP (upper corner). The corner cones' generators (w_RT, w_down at the lower corner; w_left, w_down, w_T at the upper corner) are represented at the exact-frontier cells (mirror ΔW = 0 at i ≥ 10; forward ΔW = 0 at j ≥ 7) with the local-drift rates, so the §E.4 bridge holds there too. The Issue-54 obstruction concerns exact pointwise first-moment representability of every tangent direction at every endpoint cell — a finite-m lattice identity, different from the operator-level object here (which needs only the recovery of the CORNER-VIABLE controls, and the restriction H_m ≤ H_proj for everything else).

### E.6 Single bounded gap (Outcome B)

The operator-consistency components are established: monotonicity, stability, interior consistency, stencil destination availability, finite-m rate algebra conditional on a locally admissible candidate, the local-state same-candidate recovery lemma, and the boundary subsolution transfer on the closure w.r.t. H_proj (both branches). **The one bounded unresolved block:** the project-specific application of the state-constraint comparison/unique-continuation theorem for the project's continuous limit problem (subsolution on the closure w.r.t. H_proj vs supersolution in the interior — Soner II / Capuzzo-Dolcetta–Lions form), with the constrained characterization ρV ≤ H_T at the boundary as a tightly coupled sublemma of the same boundary block (not established; not load-bearing for the transfer, but needed to identify the boundary limit as the H_T-constrained solution). This is the Outcome-B terminal.

---

## Part F — Mandatory toy discriminator (Rev 2 — quantifier corrected; analytic; no simulation)

### F.1 Toy definition

1D state-constrained problem: x ∈ [0, 1]; control d ∈ [−1, 1]; drift μ(x,d) = d; state constraint x(t) ∈ [0, 1]; tangent cones T(0) = [0, 1], T(1) = [−1, 0], T(x) = [−1, 1] in the interior. Running payoff g(d) bounded, concave; discount ρ > 0. Continuous authority (Soner form): V subsolution on [0,1] / supersolution in (0,1) with the full Hamiltonian H_proj(x, p) = max_{d ∈ [−1,1]}{g(d) + pd}; the constrained boundary value satisfies ρV(0) = max_{d ∈ [0,1]}{g(d) + V'(0)d} = H_T(0, V'(0)) (elementary constrained characterization for the toy — compact control set, viability, dynamic programming).

Scheme: grid x_i = i/m (i = 0..m); upwind differences (forward for d > 0, backward for d < 0); discrete admissible sets A_m(x_i) = T(x_i): [0,1] at the boundary node, [−1,1] at interior nodes (the raw graph failure: limsup A_m(x_i) ⊇ [−1,1] ⊄ [0,1] = T(0)):

```text
u_m(x_i) = max_{d ∈ A_m(x_i)} { [ g(d) + m·d⁺ u_m(x_{i+1}) + m·d⁻ u_m(x_{i−1}) ] / [ ρ + m·|d| ] }   (scaled Bellman form)
```

### F.2 Component proof (Rev 2)

1. **Scheme definition:** as above; the fixed point exists uniquely (order-preserving contraction, §D.1).
2. **Monotonicity:** scaled operator has nonnegative weights m·d⁺/(ρ+m|d|), m·d⁻/(ρ+m|d|) and is nondecreasing; residual form has positive diagonal ρ + m|d| and nonpositive off-diagonals; no row-sum condition.
3. **Stability:** max-principle gives |u_m| ≤ ‖g‖∞/ρ uniformly.
4. **Interior consistency:** at x ∈ (0,1), for φ ∈ C²: S_m(x_i, φ) → ρφ(x) − max_{d ∈ [−1,1]}{g(d) + φ'(x)d} with O(1/m) remainder (upwind Taylor, exact first moment m d⁺h − m d⁻h = d) — both directions at interior test points.
5. **Boundary half-relaxed-limit subsolution at 0 (corrected quantifier).** Let ū = limsup* u_m, φ touching ū from above at 0, φ_ε = φ + εx², s_m near-maximizers of u_m − φ_ε near 0. Contact step: for every d, u_m(x_{i±1}) − u_m(s_m) ≤ φ_ε(x_{i±1}) − φ_ε(s_m); hence candidatewise the residual score is bounded, and taking the max (valid — max is nondecreasing):

```text
ρu_m(s_m) = max_{d ∈ A_m(s_m)} { g(d) + m d⁺[u_m(x_{i+1})−u_m(s_m)] + m d⁻[u_m(x_{i−1})−u_m(s_m)] }
          ≤ max_{d ∈ A_m(s_m)} { g(d) + m d⁺[φ_ε(x_{i+1})−φ_ε(s_m)] + m d⁻[φ_ε(x_{i−1})−φ_ε(s_m)] }.
```

Taylor candidatewise inside the max (upwind: m d⁺[φ(x+h)−φ(x)] → d φ'(x) uniformly for d ∈ [−1,1]; remainder O(1/m) passes through the 1-Lipschitz max):

```text
ρφ(0) ≤ max_{d ∈ A_lim} { g(d) + φ'(0)·d },
```

where A_lim is the limsup of the admissible sets at the visited states. **Two branches:**

- **Boundary-node branch** (near-maximizers at x_0 for a subsequence): A_lim = [0,1], the operator is EXACTLY the constrained operator H_T(0, φ') = max_{d ∈ [0,1]}{g(d) + φ'd} — ρφ(0) ≤ H_T(0, φ') ✓.
- **Interior-node branch** (near-maximizers at interior x_i → 0): A_lim = [−1,1] and ρφ(0) ≤ H_int(0, φ') = max_{d ∈ [−1,1]}{g + φ'd} = H_proj(0, φ'). The constrained inequality ρφ(0) ≤ H_T(0, φ') does NOT follow from cone containment ([0,1] ⊆ [−1,1] gives the wrong direction) — closing this branch is exactly the constrained-characterization structure: for the toy it is elementary (compact control set + viability + DP: the toy's limit value satisfies ρV(0) = H_T(0, V'(0)), and the scheme's boundary node implements exactly that law), while in the project it is the coupled sublemma of the Outcome-B gap. For the toy's convergence the interior branch already suffices via the full-Hamiltonian subsolution form: ρφ(0) ≤ H_proj(0, φ') (the Soner-form subsolution class used by the toy's comparison — see item 7).

6. **Interior supersolution at x ∈ (0,1):** near-minimizer argument (max retained, nondecreasing max): ρφ(x) ≥ max_{d ∈ [−1,1]}{g + φ'd} = H_proj(x, φ') — the supersolution in the interior ✓.
7. **Comparison assumption/theorem:** the 1D discounted state-constrained problem satisfies the Soner-type comparison (subsolution on [0,1] w.r.t. H_proj vs supersolution in (0,1) w.r.t. H_proj; equivalently the maximal-subsolution characterization) — cited to the primary references in the capsule; for the toy this is a classical elementary result. With it, BS-type arguments give ū ≤ u̲, hence u_m → V.
8. **No "max ⟹ every d" inference** appears anywhere in the toy proof: every inequality step either retains the outer max or uses the candidatewise direction only to bound the max by the max (valid).

### F.3 Role and scope

The toy's role is **only** to falsify necessity of the raw Issue-#55 graph condition: interior nodes x_i → 0 admit d < 0 (raw graph failure) yet the scheme satisfies monotonicity, stability, interior consistency, the boundary treatment (exact constrained operator at the boundary node), and converges (items 5–7). The toy does NOT prove the project's 2D scheme converges — the project's convergence has the §E.6 comparison gap, explicitly not claimed here.

---

## Summary of Part D+E+F (Rev 2)

- Legitimate target: order-preserving (monotone) + stable + interior-consistent + one-sided boundary consistency via the restriction H_lim ≤ H_proj + comparison hypothesis — all in the fixed project convention (Rev-1 monotonicity kept; §D.2 quantifier corrected).
- Frozen process: local-state same-candidate recovery lemma PROVED at the design level (rates from μ(s_m, α_m), explicit α_m constructions, source-verified drift continuity H1–H3); control/payoff bridge liminf H_R ≥ H_T and restriction limsup H_R ≤ H_proj both established; the W-contact transfer closes without a constrained characterization; triple corner (W_max = 8) treated with the Case-B forward/left contract (i = 9, no mirror); taxonomy/drift units as in Rev 1.
- Single bounded gap (Outcome B): the project-specific state-constraint comparison/unique-continuation application, with the constrained characterization ρV ≤ H_T as a coupled sublemma of the same boundary block.
- Toy: YES with the full component proof and the corrected max quantifier (Task 8 of the Micro-Rev).
