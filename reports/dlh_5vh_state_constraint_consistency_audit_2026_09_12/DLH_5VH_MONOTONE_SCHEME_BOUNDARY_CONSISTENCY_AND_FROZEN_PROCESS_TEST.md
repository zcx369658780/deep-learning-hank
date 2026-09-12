# DLH-5V-H — Monotone-Scheme Boundary Consistency and Frozen-Process Test (Micro-Rev Rev 3)

**Sequence steps D, E, F of Issue #56; Micro-Rev Rev 3 (Reviewer comment `5642677284`).** Defines the weakest defensible numerical target (D) with the corrected monotonicity and the quantifier-corrected half-relaxed-limit derivation; tests the frozen finite-process architecture against it (E) with the **local-state same-candidate recovery lemma** written with the TRUE adjustment-cost algebra and an explicit **strict/tangent recovery ledger**; supplies the mandatory analytic toy discriminator (F).

**Rev-3 scope:** the Rev-1 and Rev-2 repairs are preserved (Soner sign transform; project convention; H_T downgraded; corrected monotonicity; max-principle stability; frozen finite-m taxonomy; μ_W = 1; quantifier-corrected half-relaxed-limit; the restriction H_m ≤ H_proj as the right boundary-transfer direction). This revision (i) replaces every transfer-perturbation statement with the exact χ(d,a) algebra (Δμ_a = −ε; Δμ_b = +ε − Δχ; Δμ_W = −Δχ under d → d − ε), (ii) re-audits ALL tangent recovery at the triple corner, the b_min×W joint cells, and every face family, with the PROVED/UNRESOLVED ledger split, (iii) establishes (Route R1) the effective compactness/coercivity of the Hamiltonian and the upper-semicontinuity/continuity of H_proj with a uniform local moment bound, (iv) corrects the mirror-availability wording, (v) rechecks the toy language.

---

## Part D — The weakest defensible numerical target

### D.1 Scheme operator and corrected monotonicity (kept from Rev 1/2)

Residual form `S_m(s,u) = ρu(s) − max_α {g + Σ q(u(j) − u(s))} = 0`; scaled form `u = T_m(u)` with weights q/(ρ + Σq) ≥ 0, Σ_j w < 1. For each fixed candidate the residual has positive diagonal ρ + Σ q ≥ ρ > 0 and nonpositive off-diagonals −q ≤ 0 (proper M-matrix structure); **no ρ ≥ Σ q**. T_m is order-preserving and a strict contraction ⟹ unique fixed point; stability via the max-principle ‖u_m‖∞ ≤ ‖g‖∞/ρ. (Convention: F = ρu − H, subsolution = F ≤ 0.)

### D.2 Half-relaxed-limit derivation (kept from Rev 2 — quantifier corrected)

**Setup.** ū := limsup* u_m; x̂ ∈ D̄; φ ∈ C² touching ū from above; φ_ε = φ + ε|x − x̂|²; s_m near-maximizers of u_m − φ_ε (s_m → x̂, u_m ≤ φ_ε + c_m near s_m, c_m → 0).

**Contact step (candidatewise).** For every candidate α with local support: `u_m(j) − u_m(s_m) ≤ φ_ε(j) − φ_ε(s_m)`.

**Max step (outer max RETAINED — no per-candidate inference).** Since the candidatewise inequality holds, the max is nondecreasing and

```text
ρu_m(s_m) = max_α { g + Σ q [u_m(j) − u_m(s_m)] } ≤ max_α { g(s_m,α) + Σ_j q_α(s_m,j)[φ_ε(j) − φ_ε(s_m)] }.
```

Taylor candidatewise INSIDE the max (exact first moment Σ_j q_α(x_j − x_s) = μ_α(s_m); remainder ≤ ½‖D²φ_ε‖·max_α Σ_j q_α|x_j − x_s|² — the max is 1-Lipschitz, so a UNIFORM-in-α remainder passes through; the uniform bound is established in §D.4):

```text
ρφ_ε(s_m) ≤ max_α { g(s_m,α) + Dφ_ε(s_m)·μ_α(s_m) } + o(1).
```

**Subsolution conclusion.** With H_m(s_m, p) := max_{α ∈ A_m(s_m)} { g(s_m,α) + p·μ_α(s_m) } and H_lim(x̂, p) := limsup_m H_m(s_m, p):

```text
ρφ(x̂) ≤ H_lim(x̂, Dφ(x̂))   — ū is a viscosity subsolution w.r.t. H_lim.
```

**Supersolution direction (quantifier-checked).** Near-minimizer sequence (u_m ≥ φ_ε + c_m): candidatewise u_m(j) − u_m(s_m) ≥ φ_ε(j) − φ_ε(s_m) ⟹ candidatewise L_α ≥ R_α ⟹ max_α L_α ≥ max_α R_α (max nondecreasing); with max_α L_α = ρu_m(s_m): `ρφ(x̂) ≥ H_lim(x̂, Dφ(x̂))` at x̂ ∈ D° — supersolution in the interior.

### D.3 Boundary one-sided transfer (kept from Rev 2 — regularity now established in §D.4)

At x̂ ∈ ∂D the near-maximizer sequence visits interior or W-contact states:

- **Interior-state branch:** H_lim = H_proj (interior recovery + restriction).
- **W-contact-state branch:** H_m(s_m, p) ≤ H_proj(s_m, p) (buffered candidate set ⊆ full household feasible set at s_m — a genuine subset) and H_proj is upper semicontinuous in (x, p) (§D.4), so

```text
ρφ(x̂) ≤ H_lim(x̂, Dφ) ≤ limsup_m H_proj(s_m, Dφ) ≤ H_proj(x̂, Dφ).
```

The Soner-form subsolution on the closure w.r.t. the FULL Hamiltonian H_proj is established WITHOUT the constrained characterization ρV ≤ H_T. (The recovery-side statement liminf H_R ≥ H_T — the tangent-cone values attained at the discrete level — is §E.4; the geometric identification of the boundary operators, not the load-bearing piece of the transfer.)

### D.4 Hamiltonian regularity / effective compactness (Rev-3 Task B — Route R1)

**Effective feasible control correspondence.** The household's feasibility structure (the budget is part of the household problem): at x ∈ D̄_W the feasible controls are

```text
Γ(x) = { (c, l, d) : c ≥ 0, l ∈ Π_j [0, l_j,max], d ∈ [d_min(x), d_max(x)],
          c + χ(a,d) + d ≤ y(a,b,l) + r_b·b + τ }
```

with the source-verified components (r_a_eff(a) = r_a(1 − 0.1(a/a_max)^9) ≥ 0.9 r_a ≥ 0; χ(a,d) = χ_0|d| + ½χ_1 d²/max(a,a_bar) with χ_0 ≥ 0, χ_1 > 0, a_bar > 0; y(a,b,l) = Σ_j net_wage_j·z·l_j linear in l with continuous coefficients; r_b, τ constants; u(c) − v(l) with v(l) = Σ ω_j l_j^{1+φ}/(1+φ), φ > 0).

**Effective compactness / coercivity lemma (PROVED).** Γ(x) is compact-valued for every x and its union over x ∈ D̄_W is compact:

1. **d-coercivity:** from c ≥ 0 and the budget: χ(a,d) + d ≤ y + r_b·b + τ ≤ R_max. For d → +∞: χ + d ≥ ½χ_1 d²/s + χ_0 d + d → +∞ (χ_1 > 0) — bounded above; for d → −∞: χ + d = χ_0|d| + ½χ_1 d²/s + d = (χ_0−1)|d| + ½χ_1 d²/s + O(1) → +∞ — bounded below (the quadratic adjustment cost coerces d in both directions, for every χ_0 ≥ 0).
2. **c-boundedness:** c ≤ y + r_b·b + τ − χ − d ≤ R_max + |d| ≤ bounded.
3. **l-boundedness:** the labor-disutility coercivity: for any p_b bounded, the l-maximizer of −v(l) + p_b·y(a,b,l) satisfies the FOC l_j = (p_b·net_wage_j·z/ω_j)^{1/φ} — finite, locally uniform in p_b; the effective l-range is a fixed compact box for the p-region relevant to the viscosity tests.
4. The bounds y, χ, r_b·b + τ are continuous on the compact D̄_W, so ∪_{x} Γ(x) is compact (locally uniform in p; fixed compact box for l).

**Hamiltonian finiteness and domain issue (PROVED).** With the feasible set, H_proj(x, p) = max_{α ∈ Γ(x)} {u(c) − v(l) + p·μ(x, α)} is **finite for every (x, p) ∈ D̄_W × R²** (compact Γ, continuous integrand). The formal sup over an unbounded consumption would be +∞ for p_b < 0 (u(c) − p_b·c with u → 0, γ > 1); the continuous authority's sup is over the household's FEASIBLE controls (the budget is part of the household problem) — this is the explicit effective-control clarification of the authority, not a revision. No p-region restriction is needed for finiteness.

**Upper semicontinuity (PROVED, Berge).** Γ is upper hemicontinuous and compact-valued (closed graph, locally bounded — the constraint functions are continuous); Φ(x, α, p) = u(c) − v(l) + p·μ(x, α) is continuous on D̄_W × Γ(D̄_W) × R². Berge's maximum theorem (upper-hemicontinuous compact-valued version): H_proj is **upper semicontinuous in (x, p)**; for each fixed x, H_proj(x, ·) is continuous in p (finite max of continuous functions). **Lipschitz in p:** |H(x,p) − H(x,p′)| ≤ M·|p − p′| with M = sup |μ| over the compact D̄_W × Γ (finite).

**Full joint continuity (CONDITIONAL — the comparison block):** Γ is also lower hemicontinuous on the region where the feasible set has nonempty interior (e.g., at budget-slack states: keep α fixed; at budget-binding states with c > 0: scale c down by O(|x_n − x|)), so H_proj is continuous in (x, p) there (full Berge). The degenerate corners (c = 0 with a binding budget) and the exact primary-theorem application (Soner-II / Capuzzo-Dolcetta–Lions hypotheses) belong to the comparison block (§E.6). The transfer only needs USC + the recovery side.

**Uniform local moment bound (PROVED).** |μ(x, α)| ≤ M on the compact D̄_W × Γ (continuous, compact) and the sector rates satisfy q(s, r; α) = O(m·|component|) ≤ C·m uniformly in α; hence

```text
sup_α Σ_r q_α(s_m, r) |w_r|² = O(1/m)   uniformly over the candidate set used by the max,
```

so the Taylor remainder in §D.2 is uniform through the max (the maximizing α may depend on m without breaking the bound).

**Boundary-transfer status (honest):** the one-sided operator inequality at the boundary (ρφ ≤ H_lim ≤ H_proj, both branches) is **PROVED** (USC + restriction + interior/W-contact recovery). The full convergence u_m → V is **CONDITIONAL** on the comparison/unique-continuation block (§E.6) — the project-specific application of the state-constraint comparison theorem to the continuous limit problem, together with the coupled sublemmas (constrained characterization ρV ≤ H_T; the degenerate-corner continuity cases).

---

## Part E — Frozen-process test against the legitimate target

### E.1 Mandatory question 1: `s_m = (0, i_t^m(0) − 2), μ = (0, 1)`

**Only the raw graph test is violated; the operator-consistency components are not.** The state is interior (non-W-active), own cone {μ_a ≥ 0}; μ_a = 0 ≥ 0 admitted; represented by w_up = (0, 7/(19m)) with q_up = 19m/7, first moment (0, 1). **μ_W = 1** (physical units). Interior consistency holds with the a=0-face operator; the raw graph fails (μ_W = 1 > 0 at the corner limit) — the over-strong content (necessity audit §4); the boundary subsolution at the corner holds via the §D.3 transfer (USC + restriction + recovery).

### E.2 Mandatory question 2: upper-corner analogue

`s_m = (19m, i_t^m(19m) − 2), μ = (−1, 2)` → (a_max, W_max − a_max): interior state, own cone {μ_a ≤ 0}; operator-consistent; raw graph violated; boundary transfer closed by §D.3.

### E.3 Mandatory question 3: interior states approaching a boundary

**YES** — one-sided subsolution structure + §D.3 transfer + toy.

### E.4 Mandatory question 4: local-state same-candidate recovery with the TRUE χ algebra (Rev 3)

**Binding law.** candidate at s_m → admissibility at s_m → local candidate drift μ(s_m, α_m) → rates generated from THAT local drift → candidate-specific discrete Hamiltonian → ONE global argmax → ONE backward Q. All rates below are computed from μ(s_m, α_m) only.

**Exact transfer-perturbation algebra (Task A of the Rev-3 review — the correction).** The household equations (immutable source, blob `76ae5b1499…`, lines 80–157):

```text
χ(d, a) = χ_0·|d| + ½·χ_1·d²/max(a, a_bar)
μ_a = r_a_eff(a)·a + d,      r_a_eff(a) = r_a·(1 − 0.1·(a/a_max)^9) ≥ 0.9·r_a ≥ 0
μ_b = r_b·b + y(a,b,l) − χ(d,a) − d − c
μ_W = μ_a + μ_b = r_a_eff(a)·a + r_b·b + y(a,b,l) − χ(d,a) − c   (the linear d cancels; χ(d,a) REMAINS)
```

Under the transfer perturbation d′ = d − ε (ε > 0 small; no sign flip in the cases used below), the EXACT finite changes are:

```text
Δχ := χ(d−ε, a) − χ(d, a)
Δμ_a = −ε
Δμ_b = +ε − Δχ
Δμ_W = −Δχ
```

with the explicit sign-case formula (s = max(a, a_bar)):

```text
d − ε < d < 0  (no flip):   Δχ = ε·(χ_0 − χ_1·d/s) + ½·χ_1·ε²/s  > 0   (since −d > 0)
d = 0:                       Δχ = ε·χ_0 + ½·χ_1·ε²/s              ≥ 0
0 < d − ε (no flip):         Δχ = −ε·(χ_0 + χ_1·d/s) + ½·χ_1·ε²/s  < 0 for small ε
```

**It is NOT true that d → d − ε simply "raises μ_b by ε" or "leaves μ_W unchanged":** Δμ_b = ε − Δχ and Δμ_W = −Δχ with Δχ ≠ 0 in general (Rev-2 statements to that effect are corrected here). The consumption perturbation has exact linear algebra (no χ term): c → c ± δ gives Δμ_b = ∓δ, Δμ_W = ∓δ, Δμ_a = 0.

**Key structural facts used below (PROVED from the source forms):** (i) at the upper-a corner and at the triple corner, every viable control has d ≤ −r_a_eff(a_max)·a_max < 0 (from μ_a ≤ 0: d ≤ −r_a_eff(a)a), so the d → d − ε perturbation never crosses zero — no sign flip, Δχ = ε(χ_0 − χ_1 d/s) + O(ε²) > 0 — the transfer perturbation CREATES W-slack (Δμ_W = −Δχ < 0) and a-slack (Δμ_a = −ε < 0); (ii) at the b_min×W double-tangent (μ_b = μ_W = 0 ⟹ μ_a = 0 ⟹ d = −r_a_eff(a*)·a* < 0), the same holds.

**Recovery Lemma (Rev 3).** For every continuous viable control α at a corner/face limit point x̂, there is a finite-m sequence α_m of actual candidates at the actual states s_m of the corresponding frozen family such that: s_m → x̂; α_m admissible at s_m; α_m → α componentwise; g(s_m, α_m) → g(x̂, α); μ(s_m, α_m) → μ(x̂, α); ALL rates computed from μ(s_m, α_m) with EXACT first moment Σ_r q_m(x_r − x_s) = μ(s_m, α_m) and O(1/m) second moment; the same candidate object runs through scoring → argmax → Q. Proof: constructions below, family by family, with the exact Δχ algebra and the explicit interval conditions (all inequalities strict at finite m; exact-arithmetic verified).

**Ledger of tangent recovery by family (Rev-3 Task A / §4 of the review).**

| Family (cone) | Strict controls (μ strictly inside) | Tangent controls | Status |
|---|---|---|---|
| Lower-a × W, j ∈ {0..6} (REV = {μ_a ≥ 0, μ_W ≤ 0}) | α_m := α eventually (drift continuity H1 + state error O(1/m)) | μ_a tangent (μ_a(x̂,α)=0, i.e., d = 0): μ_a(s_m, α) = r_a_eff(a_s)·a_s + d ≥ d = 0 by the formula (r_a_eff ≥ 0, a_s ≥ 0) — NO perturbation needed; μ_W tangent (μ_W(x̂,α)=0): c → c + δ_m with δ_m = O(1/m) — Δμ_W = −δ_m exact, Δμ_a = 0, Δμ_b = −δ_m (no b constraint at REV) | **PROVED** |
| Upper-a × W, j = 19m−k (TDEP = {μ_a ≤ 0, μ_W ≤ 0}) | α_m := α eventually | μ_a tangent (μ_a(x̂,α)=0 ⟹ d = −r_a_eff(10)·10 < 0): d → d − ε_m — Δμ_a = −ε_m < 0 ✓; Δμ_W = −Δχ_m < 0 ✓ (Δχ > 0 for d < 0); μ_b unconstrained at TDEP — PROVED; μ_W tangent: c → c + δ_m — Δμ_W = −δ_m ✓ | **PROVED** |
| Regular W-band, 7 ≤ j ≤ 19m−7 ({μ_W ≤ 0}) | α_m := α eventually | μ_W tangent: c → c + δ_m — Δμ_W = −δ_m ✓ | **PROVED** |
| b_min × W joint cells, i = 0, 7 ≤ j ≤ 19m−7 ({μ_b ≥ 0, μ_W ≤ 0}) | α_m := α eventually | μ_b tangent only (μ_b=0, μ_W<0): c → c − δ_m — Δμ_b = +δ_m ✓, Δμ_W = +δ_m ≤ 0 for δ_m ≤ −μ_W(s_m,α) (strict W-slack); μ_W tangent only (μ_b>0, μ_W=0): c → c + δ_m — Δμ_W = −δ_m ✓, Δμ_b = −δ_m ≥ 0 for δ_m ≤ μ_b(s_m,α); DOUBLE tangent (μ_b=μ_W=0 ⟹ μ_a=0 ⟹ d = −r_a_eff(a*)·a* < 0): coupled α_m = (c − δ_m, l, d − ε_m) — Δμ_a = −ε_m, Δμ_b = ε_m − Δχ_m + δ_m, Δμ_W = δ_m − Δχ_m; choose ε_m > 2C/m and δ_m interior to [−err_b − ε_m + Δχ_m, −err_W + Δχ_m] (nonempty, width ε_m + err_b − err_W > 0) — all constraints STRICT (exact-arithmetic verified) | **PROVED** |
| W_max = 8 triple corner (TREA = {μ_a ≤ 0, μ_b ≥ 0, μ_W ≤ 0}), cells (19m−7, 9) and (19m, 0) | α_m := α eventually | All viable controls have d < 0 (μ_a ≤ 0 ⟹ d ≤ −r_a_eff(10)·10); FULLY tangent (μ_a = μ_b = μ_W = 0): coupled α_m = (c − δ_m, l, d − ε_m): Δμ_a = −ε_m; Δμ_b = ε_m − Δχ_m + δ_m; Δμ_W = δ_m − Δχ_m; with ε_m > 2C/m and δ_m ∈ [−err_b − ε_m + Δχ_m, −err_W + Δχ_m] (nonempty — width ε_m + err_b − err_W > 0; Δχ_m > 0 always for d < 0): μ_a < 0, μ_b > 0, μ_W < 0 STRICT at every finite m (exact-arithmetic verified) | **PROVED** |
| Non-W b_min face, i = 0, W-inactive ({μ_b ≥ 0}) | α_m := α eventually | μ_b tangent: c → c − δ_m — Δμ_b = +δ_m; no other constraint | **PROVED** |
| Non-W a faces (j = 0 / j = 19m, W-inactive: {μ_a ≥ 0} / {μ_a ≤ 0}) | α_m := α eventually | μ_a(s_m, α) = r_a_eff(0)·0 + d = d (j = 0) and = r_a_eff(10)·10 + d (j = 19m) — EXACT at every finite m: tangent controls stay exactly on the face law — admissible | **PROVED** |

**Uniform error bounds (the C in the constructions):** along each family |a_s − a*| + |b_s − b*| = O(1/m) (fixed-j and 19m−k cells), and μ is continuous on the compact D̄_W × Γ (H1), so |μ_W(s_m,α) − μ_W(x̂,α)| + |μ_b(s_m,α) − μ_b(x̂,α)| + |μ_a(s_m,α) − μ_a(x̂,α)| ≤ C/m for a uniform C; ε_m, δ_m = O(1/m) → 0 with explicit choices (e.g., ε_m = 4C/m, δ_m at the interval midpoint with the strictness margin). Payoff: u(c ± δ_m) − v(l) → g(x̂, α) (u, v continuous; c ± δ_m feasible for large m — consumption FOC interior, budget slack at the W-face; c − δ_m ≥ 0 always). Feasibility of (c ± δ_m, l, d − ε_m) in Γ(s_m) for large m: the budget c + χ + d ≤ y + r_b·b + τ holds with strictness margin at the interior-feasibility states, and the perturbations are O(1/m).

**Rates from the LOCAL drift (exact first moment, O(1/m) second moment — kept from Rev 2, now with local components only):**

```text
REV cells:  q_RT = 19m·μ_a(s_m,α_m)/70 (mirror (j,i)→(j+7,i−10), requiring j+7 ≤ 19m i.e. j ≤ 19m−7, and i ≥ 10), q_down = 19m·(−μ_W(s_m,α_m))/7 (down);
            q_RT·w_RT + q_down·w_down = (μ_a, −μ_a) + (0, μ_W) = (μ_a, μ_b)(s_m,α_m)  EXACT;  second moment [2660μ_a + 133(−μ_W)]/(361m).
TDEP cells: μ_b ≥ 0: q_T = 19m·μ_b/70 (forward (j,i)→(j−7,i+10), j ≥ 7), q_left = 19m·(−μ_W)/10 (left);  μ_b < 0: q_left = 19m·(−μ_a)/10, q_down = 19m·(−μ_b)/7;  EXACT first moment in both branches.
TREA cells: q_T = 19m·μ_b/70 (forward), q_left = 19m·(−μ_W)/10 (left) — the Case-B contract at (19m−7, 9) (i = 9 < 10: NO mirror); EXACT first moment.
Regular W: accepted sector contracts with local components; EXACT.
```

**Recovery + restriction composite (kept from Rev 2, now with the regularity block):** for every viable α at a corner/face and every φ ∈ C²:

```text
g(s_m,α_m) + Σ_r q_m(s_m,r;α_m)[φ(x_r) − φ(s_m)] = g(s_m,α_m) + Dφ(s_m)·μ(s_m,α_m) + O(1/m) → g(x̂,α) + Dφ(x̂)·μ(x̂,α),
so  liminf_m H_m(s_m, Dφ) ≥ H_T(x̂, Dφ),
and  H_m(s_m, p) ≤ H_proj(s_m, p) with H_proj USC ⟹ limsup_m H_m ≤ H_proj(x̂, ·),
hence  H_T(x̂, Dφ) ≤ liminf H_R ≤ limsup H_R ≤ H_proj(x̂, Dφ).
```

**Status (honest):** the local-state same-candidate recovery is **PROVED for every strict and every tangent control at every family**, with the exact Δχ algebra and the explicit interval constructions (exact-arithmetic verified). Enumeration supplements destination availability only.

### E.5 Mandatory question 5: the Issue-54 obstruction under the operator target

The missing endpoint orientations are outside the corner laws (w_T ∉ REV since μ_a = −70/19 < 0; w_RT ∉ TDEP since μ_a = +70/19 > 0); the corner generators are represented at the exact-frontier cells with local-drift rates; the finite-m lattice identity is distinct from the operator-level recovery (which needs only the corner-viable controls and the restriction for everything else).

### E.6 Single bounded gap (Outcome B — Rev-3 packaging)

**PROVED (Rev 3):** Soner sign mapping (explicit transform); raw-graph non-necessity mechanism (BS operator structure + corrected toy + corrected half-relaxed-limit algebra); monotonicity; stability; interior consistency; stencil destination availability; finite-m rate algebra conditional on a locally admissible candidate; local-state same-candidate recovery (all strict and all tangent controls, exact χ algebra); effective compactness/coercivity of the feasible control correspondence; H_proj finite for all (x, p), USC in (x, p), Lipschitz in p (Berge, hypotheses verified); uniform O(1/m) max second-moment bound; boundary subsolution transfer on the closure w.r.t. H_proj (both branches, USC + restriction + recovery); interior supersolution; composite H_T ≤ liminf H_R ≤ limsup H_R ≤ H_proj at the corners/faces.

**UNRESOLVED (the single bounded Outcome-B block):** (i) the project-specific application of the state-constraint comparison/unique-continuation theorem for the project's continuous limit problem (Soner II / Capuzzo-Dolcetta–Lions hypotheses: continuous H_proj — PROVED on the interior-feasibility region, degenerate-corner cases pending — and the exact theorem-application verification); (ii) the constrained characterization ρV ≤ H_T at the boundary (coupled sublemma of the same block; not load-bearing for the transfer; needed only to identify the boundary limit as the H_T-constrained solution). The full convergence u_m → V is CONDITIONAL on this block.

---

## Part F — Mandatory toy discriminator (Rev 3 — consistency language)

### F.1 Toy definition

1D: x ∈ [0,1], d ∈ [−1,1], ẋ = d, x(t) ∈ [0,1]; T(0) = [0,1], T(1) = [−1,0], T(x) = [−1,1] interior. Running payoff g(d) bounded, concave; ρ > 0. Continuous authority: V subsolution on [0,1] / supersolution in (0,1) with H_proj(x,p) = max_{d ∈ [−1,1]}{g(d) + pd}; constrained boundary value ρV(0) = max_{d ∈ [0,1]}{g(d) + V'(0)d} (elementary constrained characterization — the toy's control set is EXPLICITLY compact [−1,1], so the toy's Hamiltonian is finite and continuous for all p with NO regularity block — unlike the 2D household Hamiltonian, whose feasibility/coercivity is the §D.4 project block).

Scheme: grid x_i = i/m; upwind; A_m(x_i) = T(x_i): [0,1] at x_0, [−1,1] at interior nodes (raw graph failure):

```text
u_m(x_i) = max_{d ∈ A_m(x_i)} { [ g(d) + m·d⁺ u_m(x_{i+1}) + m·d⁻ u_m(x_{i−1}) ] / [ ρ + m·|d| ] }
```

### F.2 Component proof (Rev 2 kept; language aligned with §D.4)

1. Scheme definition (order-preserving contraction ⟹ unique fixed point).
2. Monotonicity: nonnegative weights; residual diagonal ρ + m|d| > 0, off-diagonals ≤ 0; no row-sum condition.
3. Stability: max-principle |u_m| ≤ ‖g‖∞/ρ.
4. Interior consistency: S_m(x_i, φ) → ρφ(x) − max_{d ∈ [−1,1]}{g(d) + φ'(x)d} + O(1/m) (upwind Taylor, exact first moment) — both directions.
5. Boundary half-relaxed-limit subsolution at 0 (max RETAINED — no "max ⟹ every d"): contact candidatewise ⟹ max ≤ max; Taylor inside the max; ρφ(0) ≤ max_{d ∈ A_lim}{g(d) + φ'(0)d}:
   - Boundary-node branch (near-maximizers at x_0): A_lim = [0,1] — EXACT constrained operator H_T(0, φ') — ρφ(0) ≤ H_T ✓.
   - Interior-node branch (near-maximizers interior): ρφ(0) ≤ H_proj(0, φ') = max_{[−1,1]}{g + φ'd} — the full-Hamiltonian subsolution form used by the toy's comparison; the constrained inequality ρφ(0) ≤ H_T(0, φ') is closed by the toy's elementary constrained characterization (compact control set + viability + DP — no 2D regularity claims).
6. Interior supersolution: near-minimizer argument (max nondecreasing) — ρφ(x) ≥ H_proj(x, φ') in (0,1).
7. Comparison: the toy's Hamiltonian is continuous and Lipschitz in p (explicit compact set) — the classical 1D state-constraint comparison applies; with it, BS-type arguments give u_m → V.
8. No per-candidate inference anywhere.

### F.3 Role and scope

The toy demonstrates ONLY that the Issue-55 raw drift-set graph condition is not the natural operator/test-function consistency object: interior nodes x_i → 0 carry [−1,1] ⊄ [0,1] (raw graph failure) yet the scheme satisfies monotonicity, stability, interior consistency, the constrained boundary treatment, and converges. It does NOT prove the 2D household Hamiltonian satisfies Soner-II hypotheses or that the project's 2D scheme converges (the §E.6 comparison block is the project gap).

---

## Summary of Part D+E+F (Rev 3)

- Legitimate target: order-preserving + stable + interior-consistent + one-sided boundary consistency via USC(H_proj) + restriction + recovery + comparison hypothesis (comparison = the bounded block).
- Frozen process: local-state same-candidate recovery PROVED for all strict and tangent controls with the TRUE χ algebra (Δμ_a = −ε, Δμ_b = +ε − Δχ, Δμ_W = −Δχ; coupled (ε, δ) constructions with explicit interval conditions and strict margins at the triple corner and b_min×W; exact-arithmetic verified); H_proj regularity established via Route R1 (effective compactness, finiteness, USC, Lipschitz in p, uniform moments); mirror wording corrected (j+7 ≤ 19m); toy language aligned.
- Single bounded gap (Outcome B): the project-specific state-constraint comparison/unique-continuation application (with the constrained characterization as a coupled sublemma); the full convergence is CONDITIONAL on this block.
