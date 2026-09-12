# DLH-5V-H — Monotone-Scheme Boundary Consistency and Frozen-Process Test (Micro-Rev Rev 6)

**Sequence steps D, E, F of Issue #56; Micro-Rev Rev 6 (Reviewer comment `5643802722`).** Defines the weakest defensible numerical target (D) with the corrected monotonicity and the quantifier-corrected half-relaxed-limit derivation; tests the frozen finite-process architecture against it (E) with the **local-state same-candidate recovery lemma** written with the TRUE adjustment-cost algebra and an explicit **strict/tangent recovery ledger**; supplies the mandatory analytic toy discriminator (F).

**Rev-6 scope (Reviewer `5643802722` — `DLH_5VH_OUTCOME_B_NOT_YET_ACCEPTED__DISCRETE_BELLMAN_COERCIVITY_AND_STABILITY_WITH_UNBOUNDED_CONTROLS_FIX_REQUIRED`).** All Rev-1–5 repairs are preserved and NOT reopened (Soner sign transform; project convention; H_T downgrade; true control domain c > 0, l ≥ 0, d ∈ R; no static budget; τ as wage wedge; no installed hard bounds; parameter authority γ_c > 0, φ > 0 only; parameter-generic continuous H_proj effective-domain theorem; continuous local effective compactness and H_proj regularity on p_b > 0; local-vs-global η; exact-χ tangent-recovery ledger; frozen-process geometry; raw-graph non-necessity at its scoped level). This revision fixes the **discrete-layer coercivity/stability defect** on the raw unbounded control domain:
(i) **New §D.5 — discrete smooth-test coercivity / optimizer-localization lemma (PROVED, route A):** for every compact (N, K_p ⊂ {p_b ≥ η > 0}) and every smooth test φ with locally bounded Hessian, for all m ≥ m₀ the exact/ε-maximizers of the FINITE-m discrete Bellman objective Ψ_m(α) = g + Σ q[φ(x_r)−φ(x_s)] lie in ONE common compact control set K_alpha^disc independent of m; the discrete max is ATTAINED; the uniform second moment O(1/m) and the Taylor remainder pass through the ACTUAL discrete max only after this localization (logical order corrected — the continuous-Hamiltonian K_alpha(K_p) is used only as the uniform lower anchor and for H_proj regularity, NOT as the discrete-max candidate set);
(ii) **§D.1 fixed:** `‖u_m‖∞ ≤ ‖g‖∞/ρ` is INVALID on the raw domain (‖g‖∞ = ∞: g unbounded below in l for every φ > 0, unbounded above in c for 0 < γ_c ≤ 1) — DELETED; per-candidate weight sum < 1 does NOT imply a global strict-contraction modulus (λ unbounded on raw controls) — DEMOTED; monotonicity/order preservation remains PROVED at the candidate level;
(iii) **New §D.6 — constant-function / operator-finiteness diagnostic:** Q·1 = 0 ⟹ the discrete score on a constant test reduces to g; for 0 < γ_c ≤ 1, sup over raw c of g is +∞ ⟹ the Bellman operator is not globally finite on arbitrary bounded functions under the raw control space (economically relevant solutions may live in the p_b > 0 effective region; global bounded-function contraction cannot be assumed; BS/Soner mapping needs an effective-domain/generalized treatment) — recorded inside the Outcome-B block;
(iv) **Outcome-B block renamed** to the UNBOUNDED-CONTROL NUMERICAL-SCHEME / STATE-CONSTRAINT CONVERGENCE-APPLICATION BLOCK (scheme-level stability/existence, strict contraction for production, constant-test finiteness, relevant-viscosity-gradient effective-domain restriction, Soner/CDL mapping and exact theorem application, optional H_T characterization). Outcome C is NOT triggered: the discrete coercivity lemma shows the frozen process CAN define a finite legitimate discrete Bellman score on the p_b > 0 smooth-test class.

---

## Part D — The weakest defensible numerical target

### D.1 Scheme operator, corrected monotonicity, and stability status (Rev-6 honest)

Residual form `S_m(s,u) = ρu(s) − max_α {g + Σ q(u(j) − u(s))} = 0`; scaled form `u = T_m(u)` with weights q/(ρ + Σq) ≥ 0, Σ_j w < 1. For each fixed candidate the residual has positive diagonal ρ + Σ q ≥ ρ > 0 and nonpositive off-diagonals −q ≤ 0 (proper M-matrix structure); **no ρ ≥ Σ q**. (Convention: F = ρu − H, subsolution = F ≤ 0.)

**Monotonicity / order preservation (PROVED, candidate level).** T_m is order-preserving: u ≤ v componentwise ⟹ T_m u ≤ T_m v (nonnegative weights; the max is nondecreasing). This is the only scheme-level property claimed on the raw unbounded control domain.

**Strict contraction / stability status (Rev-6 — the previous claims were invalid; corrected).** The per-candidate weight sum λ_α/(ρ + λ_α) < 1 (λ_α := Σ_r q_α) does NOT imply a GLOBAL strict-contraction modulus: on the raw control set the exit rates λ_α are unbounded, so sup_α λ_α/(ρ + λ_α) can approach 1 — no uniform margin follows from the per-candidate inequality alone. The earlier claim `‖u_m‖∞ ≤ ‖g‖∞/ρ` is **INVALID on the true raw control domain**: g(c,l) = u(c) − v(l) is unbounded below as l → ∞ for every φ > 0 and unbounded above as c → ∞ for 0 < γ_c ≤ 1, so ‖g‖∞ = ∞ on the raw control set. **Both claims are deleted / demoted.** Scheme-level existence/stability of discrete solutions under the raw unbounded controls (e.g., via the §D.5 localization plus valid sub/supersolution barriers or a bounded fixed-point invariant set) is NOT established here and belongs to the Outcome-B block (§E.6). For the smooth-test consistency analysis the relevant operator is the LOCALIZED one: on the discrete optimizer set K_alpha^disc of §D.5, g is bounded and λ ≤ C·m·M < ∞ for each fixed m, so per-m attainment and the consistency passage hold — that is an analysis statement about the consistency passage, NOT a global fixed-point theorem for the production scheme. The toy (Part F) is a separate compact-control model whose stability/contraction claims are valid only within its own scope (explicitly bounded controls and payoff).

### D.2 Half-relaxed-limit derivation (kept from Rev 2 — quantifier corrected)

**Setup.** ū := limsup* u_m; x̂ ∈ D̄; φ ∈ C² touching ū from above; φ_ε = φ + ε|x − x̂|²; s_m near-maximizers of u_m − φ_ε (s_m → x̂, u_m ≤ φ_ε + c_m near s_m, c_m → 0).

**Contact step (candidatewise).** For every candidate α with local support: `u_m(j) − u_m(s_m) ≤ φ_ε(j) − φ_ε(s_m)`.

**Max step (outer max RETAINED — no per-candidate inference).** Since the candidatewise inequality holds, the max is nondecreasing and

```text
ρu_m(s_m) = max_α { g + Σ q [u_m(j) − u_m(s_m)] } ≤ max_α { g(s_m,α) + Σ_j q_α(s_m,j)[φ_ε(j) − φ_ε(s_m)] }.
```

Taylor candidatewise INSIDE the max (exact first moment Σ_j q_α(x_j − x_s) = μ_α(s_m); remainder ≤ ½‖D²φ_ε‖·max_α Σ_j q_α|x_j − x_s|² — the max is 1-Lipschitz, so a UNIFORM-in-α remainder passes through once the near-maximizer sequences are localized: the **discrete smooth-test coercivity / optimizer-localization lemma (§D.5)** gives the common compact set K_alpha^disc containing every ε_m-near-maximizer for all m ≥ m₀, and on K_alpha^disc the uniform second moment is O(1/m) — the logical order is corrected in Rev 6 (continuous-Hamiltonian K_alpha(K_p) is NOT used as the discrete-max candidate set)):

```text
ρφ_ε(s_m) ≤ max_α { g(s_m,α) + Dφ_ε(s_m)·μ_α(s_m) } + o(1).
```

**Subsolution conclusion.** With H_m(s_m, p) := max_{α ∈ A_m(s_m)} { g(s_m,α) + p·μ_α(s_m) } and H_lim(x̂, p) := limsup_m H_m(s_m, p):

```text
ρφ(x̂) ≤ H_lim(x̂, Dφ(x̂))   — ū is a viscosity subsolution w.r.t. H_lim.
```

**Supersolution direction (quantifier-checked).** Near-minimizer sequence (u_m ≥ φ_ε + c_m): candidatewise u_m(j) − u_m(s_m) ≥ φ_ε(j) − φ_ε(s_m) ⟹ candidatewise L_α ≥ R_α ⟹ max_α L_α ≥ max_α R_α (max nondecreasing); with max_α L_α = ρu_m(s_m): `ρφ(x̂) ≥ H_lim(x̂, Dφ(x̂))` at x̂ ∈ D° — supersolution in the interior. **Domain caveat (Rev 4):** the supersolution inequality is meaningful only where the relevant H_lim/H_proj values are finite; the effective-domain restriction of the test gradients is the §E.6 block (see §D.4 and §E.5).

### D.3 Boundary one-sided transfer (kept from Rev 2/3 — status re-stated in Rev 5/6)

At x̂ ∈ ∂D the near-maximizer sequence visits interior or W-contact states:

- **Interior-state branch:** H_lim = H_proj (interior recovery + restriction).
- **W-contact-state branch:** H_m(s_m, p) ≤ H_proj(s_m, p) (buffered candidate set ⊆ TRUE full household control set — see §D.4 — this is now trivial: the discrete candidates are actual household controls; no budget or compactness is used for the restriction). The discrete-to-continuous passage THROUGH THE BELLMAN MAX is justified by the **discrete smooth-test coercivity / optimizer-localization lemma (§D.5)**: for smooth tests with locally bounded Hessian the ε_m-near-maximizer sequences lie in the common compact set K_alpha^disc for all m ≥ m₀, where the Taylor remainder is uniform O(1/m). The limiting step limsup_m H_proj(s_m, p_m) ≤ H_proj(x̂, p) then uses the USC/continuity of the TRUE Hamiltonian on the relevant gradient region — established in §D.4 on compact K_p ⊂ {p_b ≥ η > 0} for EVERY γ_c > 0, φ > 0; at any FIXED test gradient with p_b > 0 one may choose a local η with 0 < η < p_b, so USC + localization apply there (LOCAL OPERATOR CONSISTENCY). The remaining condition is whether all relevant viscosity test gradients lie in the finite effective domain (and away from p_b = 0 as the chosen comparison theorem requires) — the §E.6 block.

**Boundary-transfer status (Rev-5/6 honest):** the one-sided operator inequality at the boundary is **PROVED for every effective-domain smooth-test gradient (p_b > 0, φ with locally bounded Hessian)** (discrete localization §D.5 + USC of the true H_proj there + trivial restriction + recovery; parameter-generic in γ_c > 0, φ > 0); the overall transfer is **CONDITIONAL_ON_EFFECTIVE_DOMAIN_REGULARITY** — the condition being that the viscosity gradients actually used by the state-constraint comparison/consistency argument stay in the finite effective domain (and away from p_b = 0 where needed), which is not established in scope and belongs to the Outcome-B block. NO global uniform η is demanded a priori. The false global budget-restricted Γ of Rev 3 is NOT used anywhere in this step.

### D.4 TRUE control domain and Hamiltonian effective-domain audit (Rev-4 correction kept; Rev-5 parameter-generic)

**True full interior control domain (from accepted authority).** The frozen interior HJB is

```text
ρV = sup_{c>0, l ≥ 0, d ∈ R} { u(c) − v(l) + V_a·μ_a + V_b·μ_b },
```

with the source-exact drift (blob `76ae5b1499…`, lines 80–157):

```text
μ_a = r_a_eff(a)·a + d,          r_a_eff(a) = r_a·(1 − 0.1·(a/a_max)^9) ≥ 0.9·r_a ≥ 0
μ_b = r_b·b + labor_income − d − χ(d,a) − c,        labor_income = Σ_j w_j(1 − τ − mig_j)·z·l_j
χ(d,a) = χ_0·|d| + ½·χ_1·d²/max(a, a_bar)
g(c,l) = u(c) − v(l),            u(c) = log(c) if γ_c = 1, else c^{1−γ_c}/(1−γ_c),  γ_c > 0 (source-freezed: only positivity),   v(l) = Σ_j ω_j l_j^{1+φ}/(1+φ),  φ > 0
```

- **NO global static inequality `c + χ + d ≤ …`:** rearranged, that inequality is μ_b ≥ 0, a tangent law only on the actual lower-liquid face b = b_min; the accepted W-boundary sectors explicitly contain R_reverse and R_deplete candidates with μ_b < 0 (the household can run down liquid wealth). Imposing it globally would silently convert the liquid drift equation into a static resource constraint and mutate the economics. **Removed.**
- **τ correction:** τ is the tax wedge entering effective wages via w_j(1 − τ − mig_j); it is NOT an additive term in μ_b. The source drift is exactly as written above (no +τ). Any transfer-income object in a continuous design must be named separately; this audit introduces none.
- **No hard l_max / d_min / d_max bounds:** optimizer boundedness is derived EFFECTIVELY from coercivity on the relevant gradient region (§D.4.2); the bounds are not installed as frozen feasibility. Until attainment/effective compactness is proved, the Hamiltonian is written with **sup**, not max.
- State constraints (μ_a ≥ 0, μ_b ≥ 0, μ_a ≤ 0, μ_W ≤ 0) apply ONLY on their actual active faces/intersections, as in the frozen taxonomy.

**D.4.1 Hamiltonian effective domain by gradient region (PARAMETER-GENERIC — exact for every frozen γ_c > 0, φ > 0).** Write the true Hamiltonian

```text
H_proj(x, p) = sup_{c>0, l≥0, d∈R} { u(c) − v(l) + p_a·μ_a + p_b·μ_b }
```

and split the load-bearing terms: consumption `u(c) − p_b·c`; labor `−v(l) + p_b·y(l)` (y = labor_income); transfer `(p_a − p_b)·d − p_b·χ(d,a)`. The consumption utility is the source CRRA form: u(c) = log(c) if γ_c = 1, else u(c) = c^{1−γ_c}/(1−γ_c), with γ_c > 0; the labor disutility is v(l) = Σ_j ω_j l_j^{1+φ}/(1+φ), φ > 0. **No numeric γ_c / φ value is frozen theory authority** (the source freezes only positivity; the instances with γ_c = 2, φ = 5 are the canonical `VALIDATION_FIXTURE_NOT_CALIBRATION` in the test fixtures, not scientific authority for the continuous theory).

- **Case p_b > 0 (finite, attained for EVERY γ_c > 0, φ > 0 — the effective region):**
  - c: u(c) − p_b·c is strictly concave (u″(c) = −γ_c·c^{−γ_c−1} < 0 for all γ_c > 0; log branch included) and tends to −∞ as c → ∞ (for γ_c ≥ 1, u(c) − p_b·c → −∞; for γ_c < 1, u(c) = c^{1−γ_c}/(1−γ_c) grows sublinearly, so u(c) − p_b·c = c·(c^{−γ_c}/(1−γ_c) − p_b) → −∞); the sup is attained at the consumption FOC **c* = p_b^{−1/γ_c}**, value (γ_c/(1−γ_c))·p_b^{(γ_c−1)/γ_c} for γ_c ≠ 1, −1 − log(p_b) for γ_c = 1 — finite in both cases.
  - l: −Σω_j l_j^{1+φ}/(1+φ) + p_b·Σ net_wage_j·z·l_j — the (1+φ)-power dominates the linear term for every φ > 0; coercive as l → ∞; attained at the labor FOC **l_j* = (p_b·net_wage_j·z/ω_j)^{1/φ}**.
  - d: (p_a − p_b)·d − p_b·(χ_0|d| + ½χ_1 d²/s) — the −p_b·χ_1 d²/(2s) quadratic term dominates in both directions (χ_1 > 0, p_b > 0); attained at the transfer FOC: **d* = (s/χ_1)((p_a−p_b)/p_b − χ_0·sign(d*))**, and d* = 0 when |(p_a−p_b)/p_b| ≤ χ_0.
  - ⟹ H_proj(x, p) is finite for p_b > 0 for every frozen γ_c > 0, φ > 0 (sup = max, attained).
- **Case p_b < 0 (+∞, regardless of γ_c):** the transfer term becomes (p_a + |p_b|)·d + |p_b|·χ(d,a) — the quadratic term +|p_b|·χ_1 d²/(2s) is POSITIVE — the sup over d ∈ R is **+∞** for every (x, p) with p_b < 0, independent of the CRRA branch.
- **Case p_b = 0, p_a ≠ 0 (+∞):** the transfer term reduces to p_a·d — sup over d ∈ R is +∞ (linear, unbounded in the sign direction of p_a).
- **Case p_b = 0, p_a = 0 (γ_c-dependent):** the c-term sup_c u(c): γ_c > 1 ⟹ u(c) = c^{1−γ_c}/(1−γ_c) → 0 from below, sup = 0 (finite, NOT attained as c → ∞); γ_c = 1 ⟹ sup log(c) = **+∞**; 0 < γ_c < 1 ⟹ sup c^{1−γ_c}/(1−γ_c) = **+∞**. The l-term sup = 0 at l = 0; the d-term = 0 for all d.

**Parameter-generic effective domain (the theorem):**

```text
if γ_c > 1:        H_proj(x,p) < ∞  ⟺  p_b > 0  OR  (p_b = 0 and p_a = 0);   H_proj = +∞ on {p_b < 0} ∪ {p_b = 0, p_a ≠ 0}.
if 0 < γ_c ≤ 1:    H_proj(x,p) < ∞  ⟺  p_b > 0;                             H_proj = +∞ on {p_b ≤ 0} (p_b = 0 including p_a = 0).
```

The γ_c > 1 branch is NOT asserted as unconditional current authority — it is stated conditional on the γ_c > 1 parameter regime, which the source does not freeze. **H_proj is NOT finite for all p.**

**D.4.2 Local effective compactness / coercivity lemma (PROVED — parameter-generic for every γ_c > 0, φ > 0).** Fix a compact gradient set `K_p ⊂ { p : p_b ≥ η > 0 }` (with |p_a| ≤ P, η ≤ p_b ≤ P < ∞) and a compact state neighborhood N of the relevant states. Then:

1. **c-bound (BOTH sides):** c* = p_b^{−1/γ_c} with p_b ∈ [η, P] ⟹ **P^{−1/γ_c} ≤ c* ≤ η^{−1/γ_c}** — a positive lower c-bound and a finite upper c-bound, uniform on K_p; and by strict concavity (u″ < 0 for all γ_c > 0) with the FOC, for any c outside [c̄, c̄] (c̄ ≪ P^{−1/γ_c}, c̄ ≫ η^{−1/γ_c}) the value u(c) − p_b·c is strictly below u(c*) − p_b·c* by a uniform δ > 0 — the maximizer cannot lie outside.
2. **l-bound:** l_j* = (p_b·net_wage_j·z/ω_j)^{1/φ} ≤ (P·max_j w_j·z/ω_min)^{1/φ} uniformly; the (1+φ)-power coercivity gives the same domination for l outside the box (φ > 0).
3. **d-bound:** |d*| ≤ (s/χ_1)(|p_a − p_b|/η + χ_0) ≤ (s/χ_1)((P + P)/η + χ_0) uniformly; the −p_b·χ_1 d²/(2s) quadratic (p_b ≥ η > 0) gives domination outside.

⟹ there is a COMMON compact effective optimizer set `K_alpha(K_p) ⊂ (0,∞) × [0,∞)^J × R` (the bounded box containing all maximizers) such that **sup over the full domain = max over K_alpha(K_p)** on N × K_p; attainment holds; and |μ(x, α)| ≤ M < ∞ on N × K_alpha(K_p) (all drift components continuous and bounded there). **PROVED** from the frozen objective — no hard bounds installed a priori, no static budget used, no numeric γ_c / φ value used.

**D.4.3 Hamiltonian regularity on the effective region (PROVED).** On N × K_p with p_b ≥ η > 0:

- H_proj(x, p) = max_{α ∈ K_alpha(K_p)} Φ(x, α, p) with Φ continuous on the compact N × K_alpha × K_p ⟹ H_proj is **jointly continuous in (x, p)** on that region (the maximum over a fixed compact control set / compact-maximum (Berge) argument — K_alpha is generally a continuum, not a finite set), in particular **USC in (x, p)**;
- **Lipschitz in p:** |H(x,p) − H(x,p′)| ≤ M·|p − p′| (M = sup|μ| on the compact set);
- the same holds on every compact K_p ⊂ {p_b ≥ η > 0} — the needed local statements.

**Uniform max second-moment bound — CONTINUOUS optimizer set only (PROVED).** On N × K_alpha(K_p): |μ(x, α)| ≤ M ⟹ the sector rates satisfy q(s, r; α) = O(m·|component|) ≤ C·m uniformly over K_alpha, hence

```text
sup_{α ∈ K_alpha(K_p)} Σ_r q_α(s_m, r) |w_r|² = O(1/m)   over the CONTINUOUS effective optimizer set K_alpha(K_p),
```

so the Taylor remainder at any α ∈ K_alpha(K_p) is O(1/m). **Rev-5 defect corrected (Rev 6):** this continuous-set bound does NOT by itself localize the finite-m DISCRETE Bellman maximizers — step "continuous K_alpha ⟹ candidate set relevant to the discrete max" was circular. The uniform bound relevant to the ACTUAL discrete max comes only AFTER the discrete smooth-test coercivity / optimizer-localization lemma (§D.5): its set K_alpha^disc ⊇ all ε_m-near-maximizers carries the uniform O(1/m) second moment through the real max. The continuous bound is still needed as (a) the uniform lower anchor (a continuous maximizer α* ∈ K_alpha(K_p) exists, §D.4.2) and (b) the H_proj regularity input. **The bound is uniform for each compact K_p ⊂ {p_b > 0}; no global candidate-uniform bound is claimed over gradients outside the finite/effective Hamiltonian region.** Candidatewise bounds are not used.

**D.5 Discrete smooth-test coercivity / optimizer-localization lemma (PROVED — Rev 6, route A).** Fix a compact state neighborhood N, a compact gradient region `K_p ⊂ {p_b ≥ η > 0}` (|p_a| ≤ P, η ≤ p_b ≤ P), and a smooth test φ ∈ C² on a neighborhood of N with locally bounded Hessian (‖D²φ‖∞ ≤ C_φ < ∞). Use the exact accepted jump/rate contracts (Part E): at a node s_m ∈ N, for every candidate α admissible under the sector/face contract, the local support has jumps w_r of size O(1/m) (the fixed moves w_left, w_down, w_T, w_RT, w_right, w_up), rates q_α(s_m, r) ≥ 0 given by the accepted formulas (each rate a nonnegative multiple of a local drift component with coefficient O(m)), and the **exact first-moment identity**

```text
Σ_r q_α(s_m, r)(x_r − x_s) = μ(s_m, α).
```

**Exact Taylor identity (candidatewise, before compactness).** For φ ∈ C²:

```text
G_m[φ](s_m; α) := Σ_r q_α(s_m, r)[φ(x_r) − φ(s_m)] = Dφ(s_m)·μ(s_m, α) + R_m(α),
|R_m(α)| ≤ ½ C_φ Σ_r q_α |w_r|² ≤ (C_φ·C_geom/m)·|μ(s_m, α)|₁,    |μ|₁ := |μ_a| + |μ_b| + |μ_W|,
```

where C_geom is a universal constant of the frozen geometry (the 19, 70, 7, 10, √2 rate/jump factors). This is the required structure `|R_m(α)| ≤ (C_φ/m)·G(α)` with G(α) = C_geom|μ(α)|₁ of the same growth order as the drift/rate magnitude — **derived globally, before assuming α compact**.

**Drift growth (raw, before compactness).** From the source forms (blob `76ae5b1499…`, lines 80–157): |μ_a| ≤ C₀(1 + |d|); |μ_b|, |μ_W| ≤ C₀(1 + |l|₁ + |d| + d² + c) (χ(d,a) ≤ χ_0|d| + ½χ_1 d²/a_bar with a_bar > 0). Hence

```text
|μ(s_m, α)|₁ ≤ C₀(1 + c + |l|₁ + |d| + d²)   with a universal C₀.
```

**Coercive decomposition.** With p_m := Dφ(s_m) ∈ K_p (so p_b ≥ η along the sequence) and the exact first moment, the discrete smooth-test objective splits as

```text
Ψ_m(α) := g(s_m, α) + G_m[φ](s_m; α)
        = [u(c) − p_b·c] + [−v(l) + p_b·labor_income] + [(p_a − p_b)·d − p_b·χ(d,a)] + [p_a·r_a_eff(a)·a + p_b·r_b·b] + R_m(α).
```

- **(i) Consumption (large c, and c → 0).** For EVERY γ_c > 0: u(c) − p_b·c ≤ u(c) − η·c → −∞ as c → ∞ (γ_c = 1 log branch; 0 < γ_c < 1 sublinear power c^{1−γ_c}/(1−γ_c) with 1−γ_c < 1); the remainder contributes ≤ (C_φ C₀/m)·c, so for m ≥ m₀ with C_φ C₀/m₀ ≤ η/4 the c-coordinate of any bounded-below superlevel set is uniformly bounded above. For c → 0: γ_c ≥ 1 ⟹ u(c) → −∞; for 0 < γ_c < 1 the FOC maximizer c* = p_b^{−1/γ_c} ∈ [P^{−1/γ_c}, η^{−1/γ_c}] (compact in p_b) and strict concavity (u″ = −γ_c c^{−γ_c−1} < 0) give a UNIFORM gap δ > 0 on {c ≤ ½P^{−1/γ_c}} (gap continuous and positive on the compact set), and the remainder is O(1/m) there — so c is uniformly confined to [c_lo, c_hi] with 0 < c_lo ≤ c_hi < ∞, for all m ≥ m₀.
- **(ii) Transfer (large |d|).** (p_a − p_b)·d − p_b·χ(d,a) ≤ |p_a − p_b||d| − ηχ_0|d| − ηχ_1 d²/(2s) ≤ 2P|d| − ηχ_1 d²/(2s̄) (s = max(a,a_bar) ≤ s̄ fixed); remainder ≤ (C_φ C₀/m)·d²; for m ≥ m₀ with C_φ C₀/m₀ ≤ ηχ_1/(4s̄) this is ≤ 2P|d| − (ηχ_1/(4s̄))d² → −∞ as |d| → ∞ uniformly. **χ₁-cancellation:** the d²-coefficient inside the |μ|₁ growth bound is exactly the χ quadratic coefficient χ_1/(2a_bar) (χ enters μ_b, μ_W), so the remainder's d²-coefficient and the leading −ηχ_1d²/(2s̄) coefficient BOTH scale with χ_1 — χ_1 cancels in the dominance ratio and m₀ is finite for every χ_1 > 0 (exact-arithmetic check, scratch `%TEMP%\dlh5vh_rev6_discrete.py`).
- **(iii) Labor (large |l|₁).** −v(l) + p_b·labor_income ≤ −(ω_min/(1+φ))Σ_j l_j^{1+φ} + P·(Σ_j w_j(1−τ−mig_j)z)·|l|₁; remainder ≤ (C_φ C₀/m)·|l|₁; since φ > 0 the (1+φ)-power dominates the linear terms for all m ≥ m₀ → −∞ as |l|₁ → ∞ uniformly.

**Uniform lower anchor.** Let α*(p) ∈ K_alpha(K_p) be any continuous maximizer (§D.4.2, exists for p_b ≥ η > 0). Plugging it in: Ψ_m(α*) = Φ(s_m, α*, p_m) + R_m(α*) ≥ H_proj(x̂, p) − O(1/m) ≥ −K₀, with K₀ := 1 + sup_{N×K_p}|H_proj| < ∞ (§D.4.3), for all m ≥ m₀. Hence sup Ψ_m ≥ −K₀ uniformly.

**Coercivity / localization conclusion (the lemma).** For every m ≥ m₀(N, K_p, C_φ, geometry constants), there is a COMMON compact box

```text
K_alpha^disc := [c_lo, c_hi] × [0, L]^J × [−D, D]   (independent of m ≥ m₀)
```

such that Ψ_m(α) ≤ −K₀ − 1 outside K_alpha^disc; consequently every EXACT maximizer (Ψ_m = sup Ψ_m) and every ε-maximizer (Ψ_m ≥ sup Ψ_m − ε, 0 ≤ ε ≤ 1) lies in K_alpha^disc for all m ≥ m₀. Since Ψ_m is continuous in α (rates depend continuously on μ, itself continuous in α) and its superlevel sets are compact, **the finite-m discrete smooth-test max is ATTAINED for every m ≥ m₀** (sup over the full raw domain = max over K_alpha^disc).

**Uniform second moment through the ACTUAL max (correct logical order).** On K_alpha^disc: |μ(s_m, α)|₁ ≤ M < ∞ (drift continuous on the compact box; N compact) ⟹ q_α = O(m·M) and

```text
sup_{α ∈ K_alpha^disc} Σ_r q_α(s_m, r) |w_r|² ≤ (C_geom·M)/m = O(1/m)   uniformly in m ≥ m₀,
```

so |R_m(α)| ≤ ½C_φ·O(1/m) for all α ∈ K_alpha^disc — the Taylor remainder is uniform THROUGH THE ACTUAL discrete max, justifying the §D.2 half-relaxed-limit step and the §D.3 boundary passage for smooth tests with locally bounded Hessian and p_b > 0 (local η < p_b).

**Logical chain (Rev-6 corrected):** raw unbounded controls → discrete coercivity/localization (D.5) → discrete maximizing controls compact (K_alpha^disc, attainment) → uniform drift/rate bound → uniform second moment O(1/m) → max-level Taylor consistency (§D.2/D.3). The continuous-Hamiltonian K_alpha(K_p) is used ONLY as the uniform lower anchor (α* exists) and for H_proj regularity — NOT as the discrete-max candidate set (the Rev-5 step-3/4 conflation).

**Boundary-face nodes / restricted contracts.** At W-inactive face nodes and the one-move Case-B contract the same structure holds for the admissible (face-law-restricted) candidate classes with the same exact first moment (rates from local drift); the box constants absorb the geometry factors; the localization is uniform over the frozen families (interior, W-active, face cells).

**Scope / status.** PROVED (route A), parameter-generic in γ_c > 0, φ > 0, for every compact (N, K_p ⊂ {p_b ≥ η > 0}) and every smooth test with locally bounded Hessian, for all m ≥ m₀. It does NOT claim: scheme-level (fixed-point) stability, a global strict-contraction modulus, or a uniform-in-m bound — those remain the Outcome-B block items (§D.1, §D.6, §E.6).

**D.6 Constant-function / operator-finiteness diagnostic (Rev-6, recorded in the block).** For every candidate, `Q·1 = 0` (Σ_r q_α(1 − 1) = 0), so on a constant test/value function the discrete Bellman score reduces to g(s, α). Therefore T_m(1)(s) = sup_{α} g(s, α): for 0 < γ_c ≤ 1 this sup over the raw c > 0 controls is **+∞** (sup u(c) = +∞ for γ_c ≤ 1); for γ_c > 1 it is finite (sup u = 0, not attained). Hence **the Bellman operator is NOT globally finite on arbitrary bounded/constant functions under the raw unbounded control space**. This is NOT automatically a scientific contradiction: the economically relevant solution may live in the p_b > 0 effective region, where the discrete smooth-test analysis (§D.5) gives a finite attained max. But it PROVES that (a) a global bounded-function Bellman-map contraction cannot be assumed, and (b) the standard Barles–Souganidis/Soner mapping needs an effective-domain or generalized-theorem treatment — both recorded inside the Outcome-B application block (§E.6).

**Pointwise/local vs global η (Rev-5 distinction).** At a FIXED test gradient p with p_b > 0, one may choose a local neighborhood and an η with 0 < η < p_b, so the local results above apply. A GLOBAL uniform η over all possible viscosity test gradients is NOT a necessary theorem condition unless the selected comparison theorem actually requires it (see §E.6). Thus: **LOCAL OPERATOR CONSISTENCY** needs only the particular test gradient to lie in {p_b > 0} (a local η then exists); **GLOBAL COMPARISON / UNIQUENESS** may require stronger control of all gradients, and that must come from the actual theorem/application.

**Boundary-transfer consequence (§D.3):** for any boundary test gradient with p_b > 0 (smooth test with locally bounded Hessian), the discrete localization lemma (§D.5) localizes the near-maximizers and the local effective compactness/USC applies (local η < p_b), so ρφ ≤ H_lim ≤ H_proj is **PROVED for such effective-domain test gradients**; the overall transfer remains **CONDITIONAL_ON_EFFECTIVE_DOMAIN_REGULARITY** until the project-specific gradient/comparison block (§E.6) is resolved.

---

## Part E — Frozen-process test against the legitimate target

### E.1 Mandatory question 1: `s_m = (0, i_t^m(0) − 2), μ = (0, 1)`

**Only the raw graph test is violated; the operator-consistency components are not.** The state is interior (non-W-active), own cone {μ_a ≥ 0}; μ_a = 0 ≥ 0 admitted; represented by w_up = (0, 7/(19m)) with q_up = 19m/7, first moment (0, 1). **μ_W = 1** (physical units). Interior consistency holds with the a=0-face operator; the raw graph fails (μ_W = 1 > 0 at the corner limit) — the over-strong content (necessity audit §4); the boundary subsolution at the corner holds via the §D.3 transfer (discrete localization §D.5 + restriction + USC on the effective region + recovery).

### E.2 Mandatory question 2: upper-corner analogue

`s_m = (19m, i_t^m(19m) − 2), μ = (−1, 2)` → (a_max, W_max − a_max): interior state, own cone {μ_a ≤ 0}; operator-consistent; raw graph violated; boundary transfer closed by §D.3.

### E.3 Mandatory question 3: interior states approaching a boundary

**YES** — one-sided subsolution structure + §D.3 transfer + toy.

### E.4 Mandatory question 4: local-state same-candidate recovery with the TRUE χ algebra (Rev 3 kept; feasibility re-audited in Rev 4)

**Binding law.** candidate at s_m → admissibility at s_m → local candidate drift μ(s_m, α_m) → rates generated from THAT local drift → candidate-specific discrete Hamiltonian → ONE global argmax → ONE backward Q. All rates below are computed from μ(s_m, α_m) only. **Argmax attainment (Rev-6):** for the smooth-test consistency analysis, existence of the finite-m discrete argmax (nonempty argmax set) is PROVED by the discrete localization lemma §D.5 (attainment on K_alpha^disc for m ≥ m₀); the "ONE" selection is the fixed deterministic tie-break convention — uniqueness of the maximizer is NOT claimed (ties are possible). Outside the smooth-test class (scheme-level fixed point) attainment is NOT claimed and belongs to the Outcome-B block.

**Exact transfer-perturbation algebra (kept from Rev 3 — accepted at that level by the Reviewer).** Under d′ = d − ε (ε > 0 small; no sign flip in the cases used):

```text
Δχ := χ(d−ε, a) − χ(d, a)
Δμ_a = −ε
Δμ_b = +ε − Δχ
Δμ_W = −Δχ
```

with the explicit sign-case formula (s = max(a, a_bar)): d < 0 (no flip): Δχ = ε(χ_0 − χ_1 d/s) + ½χ_1ε²/s > 0 (since −d > 0); d = 0: Δχ = εχ_0 + ½χ_1ε²/s ≥ 0; d > 0 (no flip): Δχ = −ε(χ_0 + χ_1 d/s) + ½χ_1ε²/s < 0 for small ε. The consumption perturbation has exact linear algebra (no χ): c → c ± δ gives Δμ_b = ∓δ, Δμ_W = ∓δ, Δμ_a = 0.

**True control-domain feasibility (Rev-4 re-audit).** The constructions are checked ONLY against: c > 0 (c ± δ_m > 0 for large m — the FOC consumption is interior and δ_m = O(1/m)); l ≥ 0 (unchanged); d ∈ R (d − ε_m or d unchanged — always admissible); and the GENUINE face tangent laws of the frozen taxonomy. **No global μ_b ≥ 0 away from b = b_min; no static budget; no hard l/d bounds.**

**Key structural facts (PROVED from the source forms):** (i) at the upper-a corner and at the triple corner, every viable control has d ≤ −r_a_eff(a_max)·a_max < 0 (from μ_a ≤ 0), so d → d − ε never crosses zero — Δχ = ε(χ_0 − χ_1 d/s) + O(ε²) > 0 — the transfer perturbation CREATES W-slack (Δμ_W = −Δχ < 0) and a-slack (Δμ_a = −ε < 0); (ii) at the b_min×W double-tangent (μ_b = μ_W = 0 ⟹ μ_a = 0 ⟹ d = −r_a_eff(a*)·a* < 0), the same holds.

**Recovery Lemma (Rev 3 kept, Rev-4 feasibility).** For every continuous viable control α at a corner/face limit point x̂, there is a finite-m sequence α_m of actual candidates at the actual states s_m of the corresponding frozen family such that: s_m → x̂; α_m admissible at s_m (against c > 0, l ≥ 0, d ∈ R, and the face laws); α_m → α componentwise; g(s_m, α_m) → g(x̂, α); μ(s_m, α_m) → μ(x̂, α); ALL rates computed from μ(s_m, α_m) with EXACT first moment Σ_r q_m(x_r − x_s) = μ(s_m, α_m) and O(1/m) second moment (the O(1/m) is uniform on the relevant gradient region via the effective compactness of §D.4.2 — the drift is continuous on the compact effective set, so |μ(s_m,α) − μ(x̂,α)| ≤ C/m for the relevant α); the same candidate object runs through scoring → argmax → Q. Constructions, family by family, with the exact Δχ algebra and the explicit interval conditions (all inequalities strict at finite m; exact-arithmetic verified).

**Ledger of tangent recovery by family (kept — status unchanged by the true-domain re-audit).**

| Family (cone) | Strict controls (μ strictly inside) | Tangent controls | Status |
|---|---|---|---|
| Lower-a × W, j ∈ {0..6} (REV = {μ_a ≥ 0, μ_W ≤ 0}) | α_m := α eventually (drift continuity on the effective set) | μ_a tangent (d = 0): μ_a(s_m, α) = r_a_eff(a_s)·a_s + d ≥ 0 by the formula — NO perturbation; μ_W tangent: c → c + δ_m — Δμ_W = −δ_m, Δμ_a = 0, Δμ_b = −δ_m (no μ_b constraint at REV); c + δ_m > 0 for large m | **PROVED** |
| Upper-a × W, j = 19m−k (TDEP = {μ_a ≤ 0, μ_W ≤ 0}) | α_m := α eventually | μ_a tangent (d = −r_a_eff(10)·10 < 0): d → d − ε_m — Δμ_a = −ε_m, Δμ_W = −Δχ_m < 0 (Δχ > 0 for d < 0); μ_b unconstrained at TDEP; μ_W tangent: c → c + δ_m | **PROVED** |
| Regular W-band, 7 ≤ j ≤ 19m−7 ({μ_W ≤ 0}) | α_m := α eventually | μ_W tangent: c → c + δ_m — Δμ_W = −δ_m | **PROVED** |
| b_min × W joint cells, i = 0, 7 ≤ j ≤ 19m−7 ({μ_b ≥ 0, μ_W ≤ 0}) | α_m := α eventually | μ_b tangent only: c → c − δ_m (Δμ_b = +δ_m; Δμ_W = +δ_m ≤ 0 for δ_m ≤ −μ_W(s_m,α), strict W-slack); μ_W tangent only: c → c + δ_m (Δμ_W = −δ_m; Δμ_b = −δ_m ≥ 0 for δ_m ≤ μ_b(s_m,α)); DOUBLE tangent (μ_b=μ_W=0 ⟹ d < 0): coupled α_m = (c − δ_m, l, d − ε_m) — Δμ_a = −ε_m, Δμ_b = ε_m − Δχ_m + δ_m, Δμ_W = δ_m − Δχ_m; ε_m > 2C/m, δ_m interior to [−err_b − ε_m + Δχ_m, −err_W + Δχ_m] (nonempty — width ε_m + err_b − err_W > 0) — all STRICT | **PROVED** |
| W_max = 8 triple corner (TREA = {μ_a ≤ 0, μ_b ≥ 0, μ_W ≤ 0}), cells (19m−7, 9) and (19m, 0) | α_m := α eventually | All viable controls d < 0; FULLY tangent (μ_a=μ_b=μ_W=0): coupled α_m = (c − δ_m, l, d − ε_m) — same interval construction (Δχ_m > 0 always), strict margins | **PROVED** |
| Non-W b_min face, i = 0, W-inactive ({μ_b ≥ 0}) | α_m := α eventually | μ_b tangent: c → c − δ_m (Δμ_b = +δ_m); no other constraint | **PROVED** |
| Non-W a faces (j = 0 / j = 19m, W-inactive: {μ_a ≥ 0} / {μ_a ≤ 0}) | α_m := α eventually | μ_a(s_m, α) = r_a_eff(0)·0 + d = d (j = 0) and = r_a_eff(10)·10 + d (j = 19m) — EXACT at every finite m: tangent controls stay exactly on the face law | **PROVED** |

**Uniform error bounds (the C in the constructions):** along each family |a_s − a*| + |b_s − b*| = O(1/m) (fixed-j and 19m−k cells); for the relevant controls α (the effective optimizer set), μ is continuous on the compact N × K_alpha (§D.4.2), so |μ(s_m,α) − μ(x̂,α)| ≤ C/m with a uniform C on the effective region; ε_m, δ_m = O(1/m) → 0 with explicit choices (e.g., ε_m = 4C/m, δ_m interior to the interval). Payoff: u(c ± δ_m) − v(l) → g(x̂, α) (u, v continuous; c ± δ_m > 0 for large m). Feasibility: c ± δ_m > 0, l ≥ 0, d − ε_m ∈ R — all automatic on the true control domain (no budget needed).

**Rates from the LOCAL drift (exact first moment, O(1/m) second moment — kept):**

```text
REV cells:  q_RT = 19m·μ_a(s_m,α_m)/70 (mirror (j,i)→(j+7,i−10), requiring j+7 ≤ 19m i.e. j ≤ 19m−7, and i ≥ 10), q_down = 19m·(−μ_W(s_m,α_m))/7 (down);
            q_RT·w_RT + q_down·w_down = (μ_a, μ_b)(s_m,α_m)  EXACT;  second moment [2660μ_a + 133(−μ_W)]/(361m).
TDEP cells: μ_b ≥ 0: q_T = 19m·μ_b/70 (forward (j,i)→(j−7,i+10), j ≥ 7), q_left = 19m·(−μ_W)/10 (left);  μ_b < 0: q_left = 19m·(−μ_a)/10, q_down = 19m·(−μ_b)/7;  EXACT first moment in both branches.
TREA cells: q_T = 19m·μ_b/70 (forward), q_left = 19m·(−μ_W)/10 (left) — the Case-B contract at (19m−7, 9) (i = 9 < 10: NO mirror); EXACT.
Regular W: accepted sector contracts with local components; EXACT.
```

**Recovery + restriction composite (kept, with the true-domain restriction):** for every viable α at a corner/face and every φ ∈ C² with Dφ in the effective region (p_b ≥ η > 0):

```text
g(s_m,α_m) + Σ_r q_m(s_m,r;α_m)[φ(x_r) − φ(s_m)] = g(s_m,α_m) + Dφ(s_m)·μ(s_m,α_m) + O(1/m) → g(x̂,α) + Dφ(x̂)·μ(x̂,α),
so  liminf_m H_m(s_m, Dφ) ≥ H_T(x̂, Dφ),
and  H_m(s_m, p) ≤ H_proj(s_m, p) (trivial subset inclusion) with H_proj USC on the effective region ⟹ limsup_m H_m ≤ H_proj(x̂, ·),
hence  H_T(x̂, Dφ) ≤ liminf H_R ≤ limsup H_R ≤ H_proj(x̂, Dφ)   on the effective gradient region.
```

**Status (honest):** the local-state same-candidate recovery is **PROVED for every strict and every tangent control at every family** against the true control domain (c > 0, l ≥ 0, d ∈ R, genuine face laws), with the exact Δχ algebra and the explicit interval constructions (exact-arithmetic verified). Enumeration supplements destination availability only.

### E.5 Mandatory question 5: the Issue-54 obstruction under the operator target

The missing endpoint orientations are outside the corner laws (w_T ∉ REV since μ_a = −70/19 < 0; w_RT ∉ TDEP since μ_a = +70/19 > 0); the corner generators are represented at the exact-frontier cells with local-drift rates; the finite-m lattice identity is distinct from the operator-level recovery (which needs only the corner-viable controls and the restriction for everything else).

### E.6 Single bounded gap (Outcome B — Rev-6 packaging)

**PROVED (Rev 3 + Rev 4 + Rev 5 + Rev 6):** Soner sign mapping (explicit transform); raw-graph non-necessity mechanism (BS operator structure + corrected toy + corrected half-relaxed-limit algebra); monotonicity / order preservation at the candidate level; interior consistency; stencil destination availability; finite-m rate algebra conditional on a locally admissible candidate; local-state same-candidate recovery (all strict and tangent controls, exact χ algebra, true control domain, parameter-independent); TRUE Hamiltonian effective domain — parameter-generic for every frozen γ_c > 0, φ > 0; LOCAL effective compactness/coercivity on compact K_p ⊂ {p_b ≥ η > 0} (parameter-generic); H_proj joint continuity/USC and Lipschitz in p on the effective region; **DISCRETE smooth-test coercivity / optimizer-localization lemma (§D.5, PROVED — route A):** for every compact (N, K_p ⊂ {p_b ≥ η > 0}) and every smooth test φ with locally bounded Hessian, for all m ≥ m₀ all exact/ε-maximizers of the finite-m discrete Bellman objective lie in ONE common compact control set K_alpha^disc; the finite-m discrete max is ATTAINED; uniform O(1/m) second moment through the ACTUAL max (logical order: raw controls → discrete coercivity/localization → compact maximizing controls → uniform drift/rate bound → uniform second moment → max-level Taylor consistency); boundary smooth-test operator consistency on the closure w.r.t. H_proj **PROVED locally for every effective-domain smooth-test gradient (p_b > 0)** (D.5 localization + trivial restriction + USC + recovery); interior supersolution; composite H_T ≤ liminf H_R ≤ limsup H_R ≤ H_proj on the effective region.

**UNRESOLVED (the single bounded Outcome-B block — Rev-6 formulation):** the **UNBOUNDED-CONTROL NUMERICAL-SCHEME / STATE-CONSTRAINT CONVERGENCE-APPLICATION BLOCK**, containing only genuinely coupled items:

1. **Global finite-m stability / existence of discrete solutions** under the raw unbounded controls (the raw ‖g‖∞ is infinite — see §D.1; needs the discrete localization plus valid sub/supersolution barriers or a bounded fixed-point invariant set); the smooth-test consistency passage is PROVED (§D.5) but the scheme's own fixed point is not.
2. **Strict contraction / unique fixed point for production** (per-candidate weight sum < 1 does not give a uniform modulus since λ unbounded on raw controls; a genuine uniform λ bound on the actually localized candidate set, or an effective-domain treatment, is required).
3. **Constant-test / operator-finiteness diagnostic** (§D.6): Q·1 = 0 ⟹ the score on a constant test reduces to g; sup over raw c of g is +∞ for 0 < γ_c ≤ 1 ⟹ the Bellman operator is not globally finite on arbitrary bounded functions under the raw control space — economically relevant solutions may live in the p_b > 0 effective region, and the standard BS/Soner mapping needs an effective-domain or generalized-theorem treatment.
4. **Relevant-viscosity-gradient effective-domain restriction** — the preferred unresolved question: do all viscosity gradients actually used by the state-constraint comparison/consistency argument remain inside the finite effective Hamiltonian domain, and where needed away from p_b = 0? No universal η is demanded a priori: for a fixed test gradient with p_b > 0 a local η < p_b exists (LOCAL OPERATOR CONSISTENCY is then PROVED); a GLOBAL uniform η over all gradients is required only if the selected comparison theorem actually requires it. Routes: value-function monotonicity in b (standard supergradient lemma holds; project-specific b-monotonicity NOT established here; the classical FOC c = V_b^{−1/γ} presumes V_b > 0 and is not a proof); strict Inada-based lower bound; or a comparison theorem formulated on the effective Hamiltonian domain.
5. **Mapping the local effective compactification to the chosen state-constraint comparison theorem** (Soner Part I assumes a COMPACT control metric space and bounded drift/running cost; the project's raw controls are unbounded — whether the local effective compactification on {p_b > 0} suffices, or an extension/generalization is required, must be resolved — do not cite Soner as directly applicable until settled), and the exact Soner-II / Capuzzo-Dolcetta–Lions application.
6. **Optional constrained characterization ρV ≤ H_T** at the boundary (coupled sublemma — NOT load-bearing for the transfer).

The full convergence u_m → V and the unconditional boundary transfer are CONDITIONAL on this block. **Outcome C is NOT triggered:** the discrete coercivity lemma (§D.5) shows the frozen process CAN define a finite legitimate discrete Bellman score on the relevant p_b > 0 smooth-test class (sup attained on the localized set, bounded below uniformly by the continuous anchor) — the frozen process is not inconsistent; the unresolved material is the general unbounded-control scheme/comparison theory, which is not grounds for Outcome C.

---

## Part F — Mandatory toy discriminator (Rev 4 — consistency language)

### F.1 Toy definition

1D: x ∈ [0,1], d ∈ [−1,1], ẋ = d, x(t) ∈ [0,1]; T(0) = [0,1], T(1) = [−1,0], T(x) = [−1,1] interior. Running payoff g(d) bounded, concave; ρ > 0. Continuous authority: V subsolution on [0,1] / supersolution in (0,1) with H_proj(x,p) = max_{d ∈ [−1,1]}{g(d) + pd}; constrained boundary value ρV(0) = max_{d ∈ [0,1]}{g(d) + V'(0)d} (elementary constrained characterization — the toy's control set is EXPLICITLY compact [−1,1], so the toy's Hamiltonian is finite and continuous for all p with NO regularity block — the toy is deliberately a bounded-control model and makes no claim about the 2D household Hamiltonian's effective domain, which is the §D.4 project block). **Scope note (Rev 6):** within the toy's compact-control bounded-payoff model the strict-contraction/unique-fixed-point and max-principle-stability claims are valid; they do NOT extend to the 2D raw unbounded control domain (c > 0, l ≥ 0, d ∈ R), where scheme-level stability/contraction are the Outcome-B block items (§D.1, §E.6).

### F.2 Component proof (Rev 2 kept; language aligned with §D.4)

1. Scheme definition (order-preserving contraction ⟹ unique fixed point — valid within the toy's compact-control scope).
2. Monotonicity: nonnegative weights; residual diagonal ρ + m|d| > 0, off-diagonals ≤ 0; no row-sum condition.
3. Stability: max-principle |u_m| ≤ ‖g‖∞/ρ — valid within the toy's compact-control scope (g bounded on [−1,1]); does NOT extend to the 2D raw unbounded domain (File 5 §D.1).
4. Interior consistency: S_m(x_i, φ) → ρφ(x) − max_{d ∈ [−1,1]}{g(d) + φ'(x)d} + O(1/m) (upwind Taylor, exact first moment) — both directions.
5. Boundary half-relaxed-limit subsolution at 0 (max RETAINED — no "max ⟹ every d"): contact candidatewise ⟹ max ≤ max; Taylor inside the max; ρφ(0) ≤ max_{d ∈ A_lim}{g(d) + φ'(0)d}:
   - Boundary-node branch (near-maximizers at x_0): A_lim = [0,1] — EXACT constrained operator H_T(0, φ') — ρφ(0) ≤ H_T ✓.
   - Interior-node branch (near-maximizers interior): ρφ(0) ≤ H_proj(0, φ') = max_{[−1,1]}{g + φ'd} — the full-Hamiltonian subsolution form used by the toy's comparison; the constrained inequality ρφ(0) ≤ H_T(0, φ') is closed by the toy's elementary constrained characterization (compact control set + viability + DP — no 2D regularity claims).
6. Interior supersolution: near-minimizer argument (max nondecreasing) — ρφ(x) ≥ H_proj(x, φ') in (0,1).
7. Comparison: the toy's Hamiltonian is continuous and Lipschitz in p (explicit compact set) — the classical 1D state-constraint comparison applies; with it, BS-type arguments give u_m → V.
8. No per-candidate inference anywhere.

### F.3 Role and scope

The toy demonstrates ONLY that the Issue-55 raw drift-set graph condition is not the natural operator/test-function consistency object: interior nodes x_i → 0 carry [−1,1] ⊄ [0,1] (raw graph failure) yet the scheme satisfies monotonicity, stability, interior consistency, the constrained boundary treatment, and converges. It does NOT prove the 2D household Hamiltonian satisfies Soner-II hypotheses or that the project's 2D scheme converges (the §E.6 unbounded-control numerical-scheme / state-constraint convergence-application block is the project gap). The toy's own stability/contraction claims hold inside its compact-control scope only (§F.1 scope note).

---

## Summary of Part D+E+F (Rev 6)

- Legitimate target: order-preserving + (scheme-level stability: DEMOTED to the block) + interior-consistent + one-sided boundary consistency via discrete localization (§D.5) + USC(H_proj on the effective region) + restriction + recovery + comparison hypothesis (comparison = the bounded block).
- TRUE control domain: c > 0, l ≥ 0, d ∈ R — the false global static budget (μ_b ≥ 0 everywhere) is REMOVED; τ corrected (wedge inside effective wages, not additive resources); no hard l/d bounds; sup until attainment is proved.
- Parameter authority: γ_c > 0, φ > 0 generic (source-freezed positivity only; γ_c = 2 / φ = 5 are VALIDATION_FIXTURE_NOT_CALIBRATION, not theory authority).
- Hamiltonian effective domain (parameter-generic, every frozen γ_c > 0, φ > 0): 0 < γ_c ≤ 1 ⟹ finite ⟺ p_b > 0; γ_c > 1 ⟹ finite ⟺ p_b > 0 or (p_b = 0, p_a = 0); +∞ on {p_b < 0} ∪ {p_b = 0, p_a ≠ 0} (and at p_b = p_a = 0 for 0 < γ_c ≤ 1). The γ_c > 1 branch is conditional on the parameter regime, not unconditional authority.
- Continuous local effective compactness on compact K_p ⊂ {p_b ≥ η > 0}: PROVED parameter-generically (c* with BOTH bounds P^{−1/γ_c} ≤ c* ≤ η^{−1/γ_c}; l/d bounds from the FOCs + coercivity; no installed bounds); H_proj joint continuity/USC and Lipschitz in p there: PROVED (maximum over a fixed compact control set / compact-maximum (Berge) argument).
- **Discrete smooth-test coercivity / optimizer-localization (§D.5, PROVED — route A):** for every compact (N, K_p ⊂ {p_b ≥ η > 0}) and every smooth test with locally bounded Hessian, all exact/ε-maximizers of the finite-m discrete Bellman objective lie in ONE common compact K_alpha^disc for all m ≥ m₀; finite-m discrete max ATTAINED; uniform O(1/m) second moment through the ACTUAL max; logical order corrected (continuous K_alpha is only the lower anchor, not the discrete-max candidate set).
- Scheme-level stability / strict contraction / unique fixed point: **DEMOTED to the Outcome-B block** (§D.1): ‖g‖∞ = ∞ on the raw domain (the old ‖g‖∞/ρ bound is deleted); per-candidate weight sum < 1 does not imply a global contraction modulus; monotonicity/order preservation remains PROVED at the candidate level.
- Constant-test / operator-finiteness diagnostic (§D.6): Q·1 = 0; sup over raw c of g is +∞ for 0 < γ_c ≤ 1 ⟹ the Bellman operator is not globally finite on arbitrary bounded functions; economically relevant solutions may live in the p_b > 0 effective region; recorded in the block.
- Local vs global η: at a fixed test gradient with p_b > 0 a local η < p_b exists — LOCAL OPERATOR CONSISTENCY PROVED there; a global uniform η is demanded only if the selected comparison theorem requires it (not assumed).
- Boundary transfer: PROVED for every effective-domain smooth-test gradient (p_b > 0, locally bounded Hessian); overall CONDITIONAL_ON_EFFECTIVE_DOMAIN_REGULARITY (the gradient/comparison block is the Outcome-B gap).
- Frozen process: local-state same-candidate recovery PROVED for all strict and tangent controls with the true χ algebra against the true control domain, parameter-independent (exact-arithmetic verified); mirror wording j+7 ≤ 19m; toy language aligned; toy stability/contraction claims scoped to its compact-control model.
- Single bounded gap (Outcome B): the UNBOUNDED-CONTROL NUMERICAL-SCHEME / STATE-CONSTRAINT CONVERGENCE-APPLICATION BLOCK — (i) global finite-m stability/existence of discrete solutions, (ii) strict contraction / unique fixed point for production, (iii) constant-test/operator-finiteness diagnostic, (iv) relevant-viscosity-gradient effective-domain restriction (away from p_b = 0 as needed), (v) local-effective-compactification → Soner/CDL comparison mapping and exact theorem application, (vi) optional constrained characterization ρV ≤ H_T. Outcome C NOT triggered (the frozen process defines a finite legitimate discrete score on the p_b > 0 smooth-test class).
