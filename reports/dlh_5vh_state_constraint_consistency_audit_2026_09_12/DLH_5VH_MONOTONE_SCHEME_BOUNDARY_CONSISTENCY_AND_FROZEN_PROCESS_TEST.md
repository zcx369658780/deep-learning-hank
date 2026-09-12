# DLH-5V-H — Monotone-Scheme Boundary Consistency and Frozen-Process Test (Micro-Rev Rev 5)

**Sequence steps D, E, F of Issue #56; Micro-Rev Rev 5 (Reviewer comment `5643574257`).** Defines the weakest defensible numerical target (D) with the corrected monotonicity and the quantifier-corrected half-relaxed-limit derivation; tests the frozen finite-process architecture against it (E) with the **local-state same-candidate recovery lemma** written with the TRUE adjustment-cost algebra and an explicit **strict/tangent recovery ledger**; supplies the mandatory analytic toy discriminator (F).

**Rev-5 scope:** Rev-1/2/3/4 repairs are preserved (Soner sign transform; project convention; H_T downgraded; corrected monotonicity; max-principle stability; frozen finite-m taxonomy; μ_W = 1; quantifier-corrected half-relaxed-limit; the exact-χ perturbation algebra Δμ_a = −ε, Δμ_b = +ε − Δχ, Δμ_W = −Δχ; family-by-family tangent recovery; mirror availability j+7 ≤ 19m, i ≥ 10; the trivial restriction H_m ≤ H_proj; the true control domain c > 0, l ≥ 0, d ∈ R with no static budget and no installed hard bounds; τ as wage wedge). This revision (i) REMOVES every claim that γ_c = 2 / φ = 5 is frozen scientific authority (the source freezes only γ_c > 0, φ > 0; the numeric instances `EconomicParams(0.02, 2.0, 5.0, …)` are the canonical `VALIDATION_FIXTURE_NOT_CALIBRATION` in the test fixtures, not theory authority), (ii) replaces the Hamiltonian effective-domain theorem with the PARAMETER-GENERIC classification for all γ_c > 0, φ > 0 (log-branch included), (iii) keeps the local effective-compactness/coercivity lemma parameter-generic (c* = p_b^{−1/γ_c} with BOTH a positive lower bound P^{−1/γ_c} and a finite upper bound η^{−1/γ_c} on K_p ⊂ {p_b ≥ η > 0}), (iv) distinguishes POINTWISE/LOCAL p_b > 0 (a local η < p_b exists at any fixed test gradient with p_b > 0) from a GLOBAL uniform η (demanded only if the selected comparison theorem requires it), (v) fixes the wording "max of finitely many continuous functions" → "maximum over a fixed compact control set / compact-maximum (Berge) argument" (K_alpha is generally a continuum), and (vi) re-states the Outcome-B ledger accordingly.

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

Taylor candidatewise INSIDE the max (exact first moment Σ_j q_α(x_j − x_s) = μ_α(s_m); remainder ≤ ½‖D²φ_ε‖·max_α Σ_j q_α|x_j − x_s|² — the max is 1-Lipschitz, so a UNIFORM-in-α remainder passes through; the uniform bound on the candidate set relevant to the Bellman max is established in §D.4 with the effective-domain restriction):

```text
ρφ_ε(s_m) ≤ max_α { g(s_m,α) + Dφ_ε(s_m)·μ_α(s_m) } + o(1).
```

**Subsolution conclusion.** With H_m(s_m, p) := max_{α ∈ A_m(s_m)} { g(s_m,α) + p·μ_α(s_m) } and H_lim(x̂, p) := limsup_m H_m(s_m, p):

```text
ρφ(x̂) ≤ H_lim(x̂, Dφ(x̂))   — ū is a viscosity subsolution w.r.t. H_lim.
```

**Supersolution direction (quantifier-checked).** Near-minimizer sequence (u_m ≥ φ_ε + c_m): candidatewise u_m(j) − u_m(s_m) ≥ φ_ε(j) − φ_ε(s_m) ⟹ candidatewise L_α ≥ R_α ⟹ max_α L_α ≥ max_α R_α (max nondecreasing); with max_α L_α = ρu_m(s_m): `ρφ(x̂) ≥ H_lim(x̂, Dφ(x̂))` at x̂ ∈ D° — supersolution in the interior. **Domain caveat (Rev 4):** the supersolution inequality is meaningful only where the relevant H_lim/H_proj values are finite; the effective-domain restriction of the test gradients is the §E.6 block (see §D.4 and §E.5).

### D.3 Boundary one-sided transfer (kept from Rev 2/3 — status re-stated in Rev 5)

At x̂ ∈ ∂D the near-maximizer sequence visits interior or W-contact states:

- **Interior-state branch:** H_lim = H_proj (interior recovery + restriction).
- **W-contact-state branch:** H_m(s_m, p) ≤ H_proj(s_m, p) (buffered candidate set ⊆ TRUE full household control set — see §D.4 — this is now trivial: the discrete candidates are actual household controls; no budget or compactness is used for the restriction). The limiting step limsup_m H_proj(s_m, p_m) ≤ H_proj(x̂, p) requires USC of the TRUE Hamiltonian on the relevant gradient region — established in §D.4 on compact K_p ⊂ {p_b ≥ η > 0} for EVERY γ_c > 0, φ > 0, and at any FIXED test gradient with p_b > 0 one may choose a local η with 0 < η < p_b, so the USC applies there (LOCAL OPERATOR CONSISTENCY). The remaining condition is whether all relevant viscosity test gradients lie in the finite effective domain (and away from p_b = 0 as the chosen comparison theorem requires) — the §E.6 block.

**Boundary-transfer status (Rev-5 honest):** the one-sided operator inequality at the boundary is **PROVED for every effective-domain test gradient (p_b > 0)** (USC of the true H_proj there + trivial restriction + recovery; parameter-generic in γ_c > 0, φ > 0); the overall transfer is **CONDITIONAL_ON_EFFECTIVE_DOMAIN_REGULARITY** — the condition being that the viscosity gradients actually used by the state-constraint comparison/consistency argument stay in the finite effective domain (and away from p_b = 0 where needed), which is not established in scope and belongs to the Outcome-B block. NO global uniform η is demanded a priori. The false global budget-restricted Γ of Rev 3 is NOT used anywhere in this step.

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

**Uniform max second-moment bound (PROVED with the same domain restriction).** On N × K_p: |μ(x, α)| ≤ M ⟹ the sector rates satisfy q(s, r; α) = O(m·|component|) ≤ C·m uniformly over K_alpha, hence

```text
sup_{α ∈ K_alpha(K_p)} Σ_r q_α(s_m, r) |w_r|² = O(1/m)   uniformly over the candidate set relevant to the Bellman max,
```

so the Taylor remainder in §D.2 is uniform through the max on the effective region. **The bound is uniform for each compact K_p ⊂ {p_b > 0}; no global candidate-uniform bound is claimed over gradients outside the finite/effective Hamiltonian region.** Candidatewise bounds are not used.

**Pointwise/local vs global η (Rev-5 distinction).** At a FIXED test gradient p with p_b > 0, one may choose a local neighborhood and an η with 0 < η < p_b, so the local results above apply. A GLOBAL uniform η over all possible viscosity test gradients is NOT a necessary theorem condition unless the selected comparison theorem actually requires it (see §E.6). Thus: **LOCAL OPERATOR CONSISTENCY** needs only the particular test gradient to lie in {p_b > 0} (a local η then exists); **GLOBAL COMPARISON / UNIQUENESS** may require stronger control of all gradients, and that must come from the actual theorem/application.

**Boundary-transfer consequence (§D.3):** for any boundary test gradient with p_b > 0, the local effective compactness/USC applies (local η < p_b), so ρφ ≤ H_lim ≤ H_proj is **PROVED for such effective-domain test gradients**; the overall transfer remains **CONDITIONAL_ON_EFFECTIVE_DOMAIN_REGULARITY** until the project-specific gradient/comparison block (§E.6) is resolved.

---

## Part E — Frozen-process test against the legitimate target

### E.1 Mandatory question 1: `s_m = (0, i_t^m(0) − 2), μ = (0, 1)`

**Only the raw graph test is violated; the operator-consistency components are not.** The state is interior (non-W-active), own cone {μ_a ≥ 0}; μ_a = 0 ≥ 0 admitted; represented by w_up = (0, 7/(19m)) with q_up = 19m/7, first moment (0, 1). **μ_W = 1** (physical units). Interior consistency holds with the a=0-face operator; the raw graph fails (μ_W = 1 > 0 at the corner limit) — the over-strong content (necessity audit §4); the boundary subsolution at the corner holds via the §D.3 transfer (restriction + USC on the effective region + recovery).

### E.2 Mandatory question 2: upper-corner analogue

`s_m = (19m, i_t^m(19m) − 2), μ = (−1, 2)` → (a_max, W_max − a_max): interior state, own cone {μ_a ≤ 0}; operator-consistent; raw graph violated; boundary transfer closed by §D.3.

### E.3 Mandatory question 3: interior states approaching a boundary

**YES** — one-sided subsolution structure + §D.3 transfer + toy.

### E.4 Mandatory question 4: local-state same-candidate recovery with the TRUE χ algebra (Rev 3 kept; feasibility re-audited in Rev 4)

**Binding law.** candidate at s_m → admissibility at s_m → local candidate drift μ(s_m, α_m) → rates generated from THAT local drift → candidate-specific discrete Hamiltonian → ONE global argmax → ONE backward Q. All rates below are computed from μ(s_m, α_m) only.

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

### E.6 Single bounded gap (Outcome B — Rev-5 packaging)

**PROVED (Rev 3 + Rev 4 + Rev 5):** Soner sign mapping (explicit transform); raw-graph non-necessity mechanism (BS operator structure + corrected toy + corrected half-relaxed-limit algebra); monotonicity; stability; interior consistency; stencil destination availability; finite-m rate algebra conditional on a locally admissible candidate; local-state same-candidate recovery (all strict and tangent controls, exact χ algebra, true control domain, parameter-independent); TRUE Hamiltonian effective domain — parameter-generic for every frozen γ_c > 0, φ > 0 (finite ⟺ p_b > 0 for 0 < γ_c ≤ 1; finite ⟺ p_b > 0 or (p_b = 0, p_a = 0) for γ_c > 1; +∞ on {p_b < 0} ∪ {p_b = 0, p_a ≠ 0} and, for 0 < γ_c ≤ 1, also at p_b = p_a = 0); LOCAL effective compactness/coercivity on compact K_p ⊂ {p_b ≥ η > 0} (c/l/d bounds derived from the FOCs + coercivity for every γ_c > 0, φ > 0; no hard bounds installed, no static budget); H_proj joint continuity/USC and Lipschitz in p on the effective region (maximum over a fixed compact control set / compact-maximum (Berge) argument); uniform O(1/m) max second-moment bound uniform per compact K_p ⊂ {p_b > 0}; boundary subsolution transfer on the closure w.r.t. H_proj for every effective-domain test gradient (p_b > 0; trivial restriction + local USC + recovery); interior supersolution; composite H_T ≤ liminf H_R ≤ limsup H_R ≤ H_proj on the effective region.

**UNRESOLVED (the single bounded Outcome-B block — Rev-5 formulation):** the project-specific **Hamiltonian-effective-domain / state-constraint-comparison application** block, with the preferred unresolved question:

> Do all viscosity gradients actually used by the state-constraint comparison/consistency argument remain inside the finite effective Hamiltonian domain, and where needed away from p_b = 0?

No universal η is demanded a priori: for a fixed test gradient with p_b > 0 a local η < p_b exists (LOCAL OPERATOR CONSISTENCY is then PROVED); a GLOBAL uniform η over all gradients is required only if the selected comparison theorem actually requires it. The block contains only genuinely coupled items: (i) the relevant-viscosity-gradient restriction (routes: value-function monotonicity in b — the standard supergradient lemma holds, but the project-specific b-monotonicity of the value/limit halves is NOT established here; the classical FOC c = V_b^{−1/γ} presumes V_b > 0 and is not a proof; a strict Inada-based lower bound; or a comparison theorem formulated on the effective Hamiltonian domain); (ii) whether the local effective compactification on {p_b > 0} is sufficient for the chosen state-constraint comparison theorem, or an extension/generalization is required (Soner Part I assumes a COMPACT control metric space and bounded drift/running cost; the project's raw controls are unbounded — do not cite Soner as directly applicable until this is settled); (iii) the exact Soner-II / Capuzzo-Dolcetta–Lions application; (iv) the optional constrained characterization ρV ≤ H_T at the boundary (coupled sublemma — NOT load-bearing for the transfer). The full convergence u_m → V and the unconditional boundary transfer are CONDITIONAL on this block.

---

## Part F — Mandatory toy discriminator (Rev 4 — consistency language)

### F.1 Toy definition

1D: x ∈ [0,1], d ∈ [−1,1], ẋ = d, x(t) ∈ [0,1]; T(0) = [0,1], T(1) = [−1,0], T(x) = [−1,1] interior. Running payoff g(d) bounded, concave; ρ > 0. Continuous authority: V subsolution on [0,1] / supersolution in (0,1) with H_proj(x,p) = max_{d ∈ [−1,1]}{g(d) + pd}; constrained boundary value ρV(0) = max_{d ∈ [0,1]}{g(d) + V'(0)d} (elementary constrained characterization — the toy's control set is EXPLICITLY compact [−1,1], so the toy's Hamiltonian is finite and continuous for all p with NO regularity block — the toy is deliberately a bounded-control model and makes no claim about the 2D household Hamiltonian's effective domain, which is the §D.4 project block).

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

The toy demonstrates ONLY that the Issue-55 raw drift-set graph condition is not the natural operator/test-function consistency object: interior nodes x_i → 0 carry [−1,1] ⊄ [0,1] (raw graph failure) yet the scheme satisfies monotonicity, stability, interior consistency, the constrained boundary treatment, and converges. It does NOT prove the 2D household Hamiltonian satisfies Soner-II hypotheses or that the project's 2D scheme converges (the §E.6 comparison/effective-domain block is the project gap).

---

## Summary of Part D+E+F (Rev 5)

- Legitimate target: order-preserving + stable + interior-consistent + one-sided boundary consistency via USC(H_proj on the effective region) + restriction + recovery + comparison hypothesis (comparison = the bounded block).
- TRUE control domain: c > 0, l ≥ 0, d ∈ R — the false global static budget (μ_b ≥ 0 everywhere) is REMOVED; τ corrected (wedge inside effective wages, not additive resources); no hard l/d bounds; sup until attainment is proved.
- Parameter authority: γ_c > 0, φ > 0 generic (source-freezed positivity only; γ_c = 2 / φ = 5 are VALIDATION_FIXTURE_NOT_CALIBRATION, not theory authority).
- Hamiltonian effective domain (parameter-generic, every frozen γ_c > 0, φ > 0): 0 < γ_c ≤ 1 ⟹ finite ⟺ p_b > 0; γ_c > 1 ⟹ finite ⟺ p_b > 0 or (p_b = 0, p_a = 0); +∞ on {p_b < 0} ∪ {p_b = 0, p_a ≠ 0} (and at p_b = p_a = 0 for 0 < γ_c ≤ 1). The γ_c > 1 branch is conditional on the parameter regime, not unconditional authority.
- Local effective compactness on compact K_p ⊂ {p_b ≥ η > 0}: PROVED parameter-generically (c* with BOTH bounds P^{−1/γ_c} ≤ c* ≤ η^{−1/γ_c}; l/d bounds from the FOCs + coercivity; no installed bounds); H_proj joint continuity/USC and Lipschitz in p there: PROVED (maximum over a fixed compact control set / compact-maximum (Berge) argument); uniform O(1/m) max second moment: PROVED uniformly per compact K_p ⊂ {p_b > 0}.
- Local vs global η: at a fixed test gradient with p_b > 0 a local η < p_b exists — LOCAL OPERATOR CONSISTENCY PROVED there; a global uniform η is demanded only if the selected comparison theorem requires it (not assumed).
- Boundary transfer: PROVED for every effective-domain test gradient (p_b > 0); overall CONDITIONAL_ON_EFFECTIVE_DOMAIN_REGULARITY (the viscosity-gradient/comparison block is the Outcome-B gap).
- Frozen process: local-state same-candidate recovery PROVED for all strict and tangent controls with the true χ algebra against the true control domain, parameter-independent (exact-arithmetic verified); mirror wording j+7 ≤ 19m; toy language aligned.
- Single bounded gap (Outcome B): the Hamiltonian-effective-domain / state-constraint-comparison application block — (i) whether all relevant viscosity gradients stay in the finite effective domain and away from p_b = 0 as needed, (ii) whether the local effective compactification suffices for the chosen state-constraint comparison theorem or an extension is required (Soner compact-control mapping), (iii) exact Soner-II/CDL application, (iv) constrained characterization ρV ≤ H_T (coupled optional sublemma).
