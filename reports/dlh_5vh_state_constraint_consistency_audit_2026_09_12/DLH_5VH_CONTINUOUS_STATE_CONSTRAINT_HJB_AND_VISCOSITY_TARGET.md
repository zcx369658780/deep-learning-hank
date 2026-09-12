# DLH-5V-H — Continuous State-Constraint HJB and Viscosity Target (Micro-Rev Rev 6)

**Sequence step A of Issue #56; Micro-Rev tasks A and B.** This report fixes the continuous state-constraint HJB object and its viscosity semantics BEFORE any numerical target is defined, records Soner's actual sign convention and derives the project transform explicitly (Task A), and demotes the tangent-cone-restricted Hamiltonian to an auxiliary object (Task B). Rev 5/6 keep the TRUE full interior control domain (c > 0, l ≥ 0, d ∈ R — no static budget, no installed hard bounds, τ corrected to its source role as a wage wedge), the **parameter-generic** Hamiltonian effective-domain audit for every frozen γ_c > 0, φ > 0 (γ_c = 2 / φ = 5 are the canonical `VALIDATION_FIXTURE_NOT_CALIBRATION`, not theory authority), the LOCAL effective-compactness/coercivity lemma on compact gradient sets with p_b ≥ η > 0 without any numeric γ_c / φ value, and the pointwise/local-vs-global η distinction. **Rev 6 adds the discrete-layer status:** the finite-m discrete Bellman consistency passage is justified by the DISCRETE smooth-test coercivity / optimizer-localization lemma (monotone-scheme report §D.5, route A — the continuous optimizer set is NOT the discrete-max candidate set); scheme-level stability/strict-contraction are DEMOTED to the single bounded Outcome-B block (renamed the UNBOUNDED-CONTROL NUMERICAL-SCHEME / STATE-CONSTRAINT CONVERGENCE-APPLICATION BLOCK), together with the constant-test/operator-finiteness diagnostic. No grid, aspect or stencil redesign is performed; the frozen geometry is consumed as given.

---

## 1. Frozen continuous object (consume, do not reopen)

Production domain and laws (accepted):

```text
D_W(W_max) = { 0 <= a <= a_max, b >= b_min, a + b <= W_max }
a_max = 10, b_min = -2, no numerical W_max selected
```

Household dynamics: states (a, b) with drifts μ_a, μ_b from the household controls (c, l, d); running payoff u(c) − v_l·l. All economics frozen; this audit only fixes the mathematical target used to judge discrete schemes.

## 2. Sign mapping (Task A — derived, not by analogy)

### 2.1 Soner Part I actual convention (PRIMARY THEOREM)

Soner Part I (SIAM JCO 24(3):552–561, 1986; Definition 2.1 / Theorem 2.1 locations verified by the Reviewer's primary-source check, comment `5641997550`) is written for a **minimization** optimal-control problem:

```text
v(x) = inf over admissible controls of ∫_0^∞ e^{−ρt} f(x_t, α_t) dt,   ẋ = b(x, α),
H_S(x, p) = sup_α { −f(x, α) − b(x, α)·p },
G_S(x, r, p) = ρ r + H_S(x, p),   equation G_S(x, v(x), Dv(x)) = 0.
```

The state-constrained value is characterized as the unique viscosity solution with:

- **viscosity subsolution in the OPEN domain** (φ touching v from above at x ∈ D°: `G_S ≤ 0`, i.e. `ρv + H_S(x, Dφ) ≤ 0`);
- **viscosity supersolution on the CLOSED domain** (φ touching v from below at x̂ ∈ D̄: `G_S ≥ 0`, i.e. `ρv + H_S(x̂, Dφ) ≥ 0`).

### 2.2 Project transform (PROJECT-SPECIFIC DERIVATION, fully explicit)

The project is a maximization problem with running payoff g = u(c) − v_l·l and drift b = μ = (μ_a, μ_b):

```text
V(x) = sup over viable controls of ∫_0^∞ e^{−ρt} g(x_t, α_t) dt.
```

Define v := −V. Then v = inf ∫ e^{−ρt} [−g] dt — a minimization problem with running cost f := −g and dynamics b = μ. Substituting into Soner's objects:

```text
H_S(x, p) = sup_α { −f(x,α) − b(x,α)·p } = sup_α { g(x,α) − μ(x,α)·p } = H_proj(x, −p),
G_S(x, v, p) = ρv + H_S(x, p) = −ρV + H_proj(x, −p) = −[ ρV − H_proj(x, −p) ] = −F_proj(x, V, −p),
F_proj(x, r, p) := ρr − H_proj(x, p),   H_proj(x, p) := sup_α { g(x,α) + p·μ(x,α) }.
```

**Residual relation:** `G_S(x, −V, −p) = −F_proj(x, V, p)` for every (x, p).

**Viscosity inequality transform.** Take a test function φ_v for v and set φ = −φ_v (so φ touches V from below/above exactly when φ_v touches v from above/below, and Dφ = −Dφ_v):

- Soner **subsolution in the open domain**: `G_S(x, v, Dφ_v) ≤ 0` ⟺ `−F_proj(x, V, Dφ) ≤ 0` ⟺ `F_proj(x, V, Dφ) ≥ 0` ⟺ **V is a viscosity SUPERSOLUTION (project convention) in the open domain**.
- Soner **supersolution on the closed domain**: `G_S(x̂, v, Dφ_v) ≥ 0` ⟺ `F_proj(x̂, V, Dφ) ≤ 0` ⟺ **V is a viscosity SUBSOLUTION (project convention) on the closure**.

**Conclusion of the transform:** the project orientation "viscosity subsolution on the closure / viscosity supersolution in the interior" (with F_proj = ρV − H_proj, subsolution meaning F_proj ≤ 0 at touching-from-above test functions) is the exact transform of Soner's "subsolution in the open domain / supersolution on the closed domain" under V = −v, f = −g. No sign-by-analogy shortcut is used; every step is displayed above.

### 2.3 Project convention fixed for the whole package

```text
F(x, r, p) = ρ r − H(x, p),   H(x, p) = sup_α { u(c) − v_l·l + p_a μ_a(x,α) + p_b μ_b(x,α) }.
Subsolution   (φ touching V from above at x̂):   F(x̂, V(x̂), Dφ(x̂)) ≤ 0,  i.e. ρV(x̂) ≤ H(x̂, Dφ(x̂)).
Supersolution (φ touching V from below at x̂):  F(x̂, V(x̂), Dφ(x̂)) ≥ 0,  i.e. ρV(x̂) ≥ H(x̂, Dφ(x̂)).
Continuous state-constraint authority (Soner form, transformed):
  V viscosity subsolution on D̄_W; V viscosity supersolution in D_W°.
```

## 3. The state-constraint semantics (distinctions requested by Issue step A)

### 3.1 Equation in the open domain

In `D_W°` both inequalities hold: V is a viscosity subsolution AND supersolution of `F = 0` at every interior point, with the unrestricted (interior) Hamiltonian H_proj and the full reachable drift set.

### 3.2 Boundary semantics — the continuous authority and the auxiliary object

**(a) Soner state-constraint (viscosity) boundary inequality — THE continuous authority.** V is a viscosity **subsolution on the closed domain D̄_W**: at every x̂ ∈ ∂D_W and every φ touching V from above at x̂, `ρV(x̂) ≤ H_proj(x̂, Dφ(x̂))` with the *unrestricted* Hamiltonian H_proj; the supersolution is required only in the interior. The boundary condition is **one-sided** (upper inequality only). This is the transform of Soner Part I's closed-domain supersolution (Section 2.2) and is the object the numerical target is defined against. **The operator-consistency transfer at the boundary targets exactly this object**: the half-relaxed-limit subsolution is established w.r.t. H_proj on the closure (monotone-scheme report §D.2), so no constrained characterization is needed for the transfer.

**(b) Tangent-cone-restricted Hamiltonian H_T — AUXILIARY object (DOWNGRADED, Task B).** Define, as a geometric/control object:

```text
T_D(x) = tangent cone of D_W at x (Bouligand/contingent cone);
H_T(x, p) = sup_{α : μ(x,α) ∈ T_D(x)} { g(x,α) + p·μ(x,α) }.
```

This package does **NOT** assert the equivalence "Soner state-constraint form ⟺ equation with H_T on the closure". The equivalence would require the constrained characterization `ρV ≤ H_T` at boundary points, which is **PLAUSIBLE BUT NOT YET PROVED** for the project's problem (the Outcome-B gap, §3.4). H_T is used only in two separately justified roles:

1. **As the geometric label of the viable drift set at the W-corners:** the accepted active-face laws are exactly the tangent-cone restrictions (a=0: μ_a ≥ 0; b=b_min: μ_b ≥ 0; a=a_max: μ_a ≤ 0; W: μ_W ≤ 0; corners: intersections). These are frozen continuous facts, independent of any equivalence claim.
2. **As the recovery target of the discrete operators:** the local-state same-candidate recovery lemma (monotone-scheme report §E.4) establishes `liminf H_R ≥ H_T` (the tangent-cone values are attained at the discrete level, rates from the local drifts μ(s_m, α_m)) and the restriction gives `limsup H_R ≤ H_proj`; the composite `H_T ≤ liminf H_R ≤ limsup H_R ≤ H_proj` at the corners/faces is the geometric/control content of the boundary operators. This is a statement about the discrete operators, not an equivalence claim about the continuous formulations.

**(c) Relaxed boundary operator.** Any operator built from a cone R(x̂) ⊇ T_D(x̂) at the limit point and consistent with the reachable-drift structure. Interior-state limits produce such operators. Under the Soner authority alone, the one-sided inequality is available with the unrestricted H_proj (ρV ≤ H_proj); operators built from smaller cones (R ⊊ full reachable set) do not need to be compared with V at the level of the transfer (the transfer closes via the restriction H_lim ≤ H_proj), but identifying the boundary limit as the H_T-constrained solution would require the constrained characterization — part of the Outcome-B block.

### 3.3 Active-face laws (frozen, consumed)

```text
a = 0        :  μ_a >= 0          (face cone {μ_a >= 0})
b = b_min    :  μ_b >= 0          (face cone {μ_b >= 0})
a = a_max    :  μ_a <= 0          (face cone {μ_a <= 0})
W face       :  μ_W = μ_a + μ_b <= 0   (face cone {μ_W <= 0})
corners      :  intersection of the active-face cones
```

Accepted corner semantics (Issue #55 Rev 1, consumed): (0, W_max): {μ_a ≥ 0, μ_W ≤ 0}; (a_max, W_max − a_max): {μ_a ≤ 0, μ_W ≤ 0}; (a_max, b_min) for W_max > 8: {μ_a ≤ 0, μ_b ≥ 0} (W inactive); W_max = 8: triple {μ_a ≤ 0, μ_b ≥ 0, μ_W ≤ 0}; (0, b_min): {μ_a ≥ 0, μ_b ≥ 0}.

### 3.4 Viability / tangent controls and the single bounded gap

The supersolution side at boundary points (when the comparison class requires it) is sustained by *tangent* controls: drifts in T_D(x̂) keep the state inside D_W for small times. The constraint's content lives in the one-sided subsolution side. The following are **NOT established in this audit and form the single bounded Outcome-B block** (Rev-6 packaging: the UNBOUNDED-CONTROL NUMERICAL-SCHEME / STATE-CONSTRAINT CONVERGENCE-APPLICATION BLOCK; the finite-m smooth-test consistency passage itself IS proved via the discrete localization lemma of the monotone-scheme report §D.5 — see item 0):

0. **Scheme-level stability / strict contraction under the raw unbounded controls** (Rev-6 addition): the raw-domain `‖g‖∞` is infinite (g unbounded below in l for every φ > 0, unbounded above in c for 0 < γ_c ≤ 1), so the max-principle bound and any GLOBAL strict-contraction claim are invalid on the true control domain; per-candidate weight sum < 1 does not imply a uniform contraction modulus (λ unbounded on raw controls). Monotonicity/order preservation is PROVED at the candidate level; scheme-level existence/stability/unique fixed point is DEMOTED to the block. (The discrete smooth-test consistency passage IS PROVED: the discrete coercivity / optimizer-localization lemma — monotone-scheme report §D.5 — localizes the finite-m maximizers into a common compact set and carries the O(1/m) Taylor remainder through the actual max for p_b > 0 smooth tests.)
1. **Relevant-viscosity-gradient restriction (preferred unresolved question).** Whether all viscosity gradients actually used by the state-constraint consistency/comparison argument remain inside the finite effective Hamiltonian domain, and where needed away from p_b = 0. No universal η is demanded a priori: at a fixed test gradient with p_b > 0 a local η < p_b exists and the local results of §3.5 apply (LOCAL OPERATOR CONSISTENCY); a GLOBAL uniform η over all gradients is required only if the selected comparison theorem actually requires it. Candidate routes: (A) value-function monotonicity in liquid wealth b (the standard lemma: every viscosity supergradient of a b-nondecreasing function has p_b ≥ 0 — holds in general; whether the project's value/limit halves inherit b-monotonicity is a project-specific verification NOT established here); (B) a strict lower bound from the Inada/marginal-utility structure; (C) a comparison theorem formulated on the effective Hamiltonian domain. **The classical FOC c = V_b^(−1/γ_c) presumes V_b > 0 and is NOT a proof of the gradient restriction.**
2. **Project-specific state-constraint comparison/unique-continuation theorem** for the project's continuous limit problem (subsolution on the closure w.r.t. H_proj vs supersolution in the interior w.r.t. H_proj — the Soner II / Capuzzo-Dolcetta–Lions maximal-subsolution form): needed to pass from the halves ū, u̲ to u_m → V. This includes the **Soner-assumption mapping**: Soner Part I assumes a COMPACT control metric space and bounded controlled drift/running cost; the project's raw controls (c > 0, l ≥ 0, d ∈ R) are not compact and the drift/running payoff are not bounded — whether the local effective compactification on {p_b > 0} (§3.5) suffices to map the whole problem into the theorem, or an extension/generalization is required, must be resolved. **Do not cite Soner as directly applicable until this is resolved.**
3. **Constrained characterization `ρV ≤ H_T` at the boundary** (the Soner⟷H_T equivalence content): a coupled sublemma of the same block — NOT needed for the transfer (the transfer closes via the discrete localization + the restriction H_lim ≤ H_proj plus USC on the effective region, monotone-scheme report §D.3/§D.5), but needed to identify the boundary limit as the H_T-constrained solution.

The audit does not assume any of these; the W-contact-state branch of the boundary subsolution transfer is closed for every effective-domain smooth-test gradient (p_b > 0) via the discrete localization lemma + restriction + USC (§D.3/§D.5), and is otherwise CONDITIONAL_ON_EFFECTIVE_DOMAIN_REGULARITY.

### 3.5 TRUE control domain and Hamiltonian effective-domain audit (Rev-4 controlling correction)

**True full interior control domain (from accepted authority).** The frozen interior HJB is `ρV = sup_{c>0, l≥0, d∈R} { u(c) − v(l) + V_a·μ_a + V_b·μ_b }` with the source-exact drift (blob `76ae5b1499…`):

```text
μ_a = r_a_eff(a)·a + d,          r_a_eff(a) = r_a·(1 − 0.1·(a/a_max)^9) ≥ 0.9·r_a ≥ 0
μ_b = r_b·b + labor_income − d − χ(d,a) − c,        labor_income = Σ_j w_j(1 − τ − mig_j)·z·l_j
χ(d,a) = χ_0·|d| + ½·χ_1·d²/max(a, a_bar),   u(c) = log(c) if γ_c = 1, else c^{1−γ_c}/(1−γ_c),  γ_c > 0 (source-freezed: positivity only),   v(l) = Σ_j ω_j l_j^{1+φ}/(1+φ),  φ > 0
```

- **NO global static inequality `c + χ + d ≤ …`:** rearranged it is μ_b ≥ 0, a tangent law ONLY on the actual lower-liquid face b = b_min. The accepted W-boundary sectors explicitly contain R_reverse and R_deplete candidates with μ_b < 0. Imposing it globally converts the liquid drift into a static resource constraint and mutates the economics. **Removed.**
- **τ correction:** τ is the tax wedge inside effective wages w_j(1 − τ − mig_j); it is NOT an additive term in μ_b. Any transfer-income object in a continuous design must be named separately (this audit introduces none).
- **No installed hard bounds l ∈ [0,l_max], d ∈ [d_min,d_max]:** optimizer boundedness, when established, is derived EFFECTIVELY from coercivity on the relevant gradient region; the Hamiltonian is written with **sup** (not max) until attainment/effective compactness is proved.
- **Parameter authority:** the source freezes only γ_c > 0 and φ > 0; the repository instances with γ_c = 2, φ = 5 (`EconomicParams(0.02, 2.0, 5.0, 0.1, 2.0, 1e-6, 0.0, 0.0)` in `tests/test_dlh_4b_transfer.py`, `tests/test_dlh_4d_r3_transfer_foc_parity.py`, `tests/test_dlh_5k_high_wealth_corner_closure_diagnostic.py`, `tests/test_dlh_5l_total_wealth_domain_geometry_diagnostic.py`) are explicitly `VALIDATION_FIXTURE_NOT_CALIBRATION` and are NOT promoted to theory authority. All statements below are parameter-generic in γ_c > 0, φ > 0.
- State constraints (μ_a ≥ 0, μ_b ≥ 0, μ_a ≤ 0, μ_W ≤ 0) apply only on their actual active faces/intersections.

**D.4.1/3.5.1 Hamiltonian effective domain by gradient region (PARAMETER-GENERIC).** H_proj(x, p) = sup_{c>0, l≥0, d∈R} {u(c) − v(l) + p_a·μ_a + p_b·μ_b}. Load-bearing terms: consumption `u(c) − p_b·c`; labor `−v(l) + p_b·y(l)`; transfer `(p_a − p_b)·d − p_b·χ(d,a)`.

- **p_b > 0 (finite, attained for EVERY γ_c > 0, φ > 0 — the effective region):** u(c) − p_b·c is strictly concave (u″ = −γ_c c^{−γ_c−1} < 0 for all γ_c > 0, log branch included) and → −∞ as c → ∞ (for γ_c ≥ 1 directly; for γ_c < 1 the sublinear power gives u(c) − p_b·c = c(c^{−γ_c}/(1−γ_c) − p_b) → −∞); attained at c* = p_b^{−1/γ_c} (value (γ_c/(1−γ_c))·p_b^{(γ_c−1)/γ_c} for γ_c ≠ 1; −1 − log p_b for γ_c = 1). l-term (1+φ)-coercive for φ > 0, attained at l_j* = (p_b·net_wage_j·z/ω_j)^{1/φ}. d-term quadratically coercive via −p_b·χ_1 d²/(2s) (χ_1 > 0, p_b > 0), attained at the transfer FOC d* = (s/χ_1)((p_a−p_b)/p_b − χ_0·sign(d*)) (d* = 0 for |(p_a−p_b)/p_b| ≤ χ_0). H_proj finite (sup = max).
- **p_b = 0, p_a ≠ 0:** d-term reduces to p_a·d — sup = +∞.
- **p_b = 0, p_a = 0:** γ_c > 1 ⟹ sup_c u(c) = 0 (finite, NOT attained, c → ∞); γ_c = 1 ⟹ sup log(c) = +∞; 0 < γ_c < 1 ⟹ sup c^{1−γ_c}/(1−γ_c) = +∞.
- **p_b < 0:** d-term becomes (p_a+|p_b|)·d + |p_b|·χ(d,a) with the +|p_b|·χ_1 d²/(2s) quadratic POSITIVE — sup = **+∞** for every (x, p), independent of the CRRA branch.

**Parameter-generic effective domain (the theorem):** `0 < γ_c ≤ 1 ⟹ H_proj finite ⟺ p_b > 0;  γ_c > 1 ⟹ H_proj finite ⟺ p_b > 0 or (p_b = 0, p_a = 0)`; +∞ on {p_b < 0} ∪ {p_b = 0, p_a ≠ 0} (and, for 0 < γ_c ≤ 1, also at p_b = p_a = 0). The γ_c > 1 branch is conditional on the parameter regime, not unconditional current authority. H_proj is NOT finite for all p.

**3.5.2 Local effective compactness / coercivity lemma (PROVED — parameter-generic).** Fix a compact gradient set `K_p ⊂ {p : p_b ≥ η > 0}` (|p_a| ≤ P, η ≤ p_b ≤ P < ∞) and a compact state neighborhood N. From the frozen objective alone, for every γ_c > 0, φ > 0: **P^{−1/γ_c} ≤ c* = p_b^{−1/γ_c} ≤ η^{−1/γ_c}** (a positive lower c-bound and a finite upper c-bound); l_j* ≤ (P·max_j w_j·z/ω_min)^{1/φ}; |d*| ≤ (s/χ_1)(|p_a−p_b|/η + χ_0) ≤ (s/χ_1)(2P/η + χ_0); and by strict concavity / (1+φ)-coercivity / quadratic coercivity each term strictly dominates outside the corresponding box — hence there is a COMMON compact effective optimizer set `K_alpha(K_p)` such that **sup over the full domain = max over K_alpha(K_p)** on N × K_p; attainment holds; |μ(x, α)| ≤ M < ∞ on N × K_alpha(K_p). PROVED from the frozen objective — no hard bounds installed a priori, no static budget, no numeric γ_c / φ value.

**3.5.3 Hamiltonian regularity on the effective region (PROVED).** On N × K_p (p_b ≥ η > 0): H_proj(x, p) = max_{α ∈ K_alpha(K_p)} Φ(x, α, p) with Φ continuous on the compact N × K_alpha × K_p ⟹ H_proj **jointly continuous in (x, p)** there (maximum over a fixed compact control set / compact-maximum (Berge) argument — K_alpha is generally a continuum, not a finite set; in particular USC); **Lipschitz in p** with M = sup|μ| on the compact set. Uniform max second-moment bound: |μ| ≤ M ⟹ sector rates q = O(m·M) uniformly ⟹ sup_{α ∈ K_alpha} Σ_r q_α |w_r|² = O(1/m) uniformly through the max — **uniform for each compact K_p ⊂ {p_b > 0}** (no global candidate-uniform bound over gradients outside the finite/effective region). Details: monotone-scheme report §D.4.

## 4. What the continuous target requires of a scheme (Rev 6)

A monotone scheme S_m for this problem is judged against the operator/test-function object:

1. Interior consistency at interior states (both inequalities, via test functions).
2. One-sided boundary consistency at boundary-contact states: the half-relaxed-limit subsolution `ρφ(x̂) ≤ H_lim(x̂, Dφ(x̂))` with H_lim ≤ H_proj at the visited states (restriction — trivial subset inclusion on the TRUE full control set; the discrete-to-continuous Taylor passage through the Bellman max is justified by the DISCRETE smooth-test coercivity / optimizer-localization lemma of the monotone-scheme report §D.5; the limsup passage via H_proj USC on the effective region {p_b > 0} — for a fixed test gradient with p_b > 0 a local η < p_b exists, §3.5), and the recovery side liminf H_R ≥ H_T at the corners/faces (local-state same-candidate recovery — monotone-scheme report §E.4). The overall boundary transfer is CONDITIONAL_ON_EFFECTIVE_DOMAIN_REGULARITY (the relevant-viscosity-gradient / comparison block is the Outcome-B gap).
3. No requirement that interior states approaching a boundary have admissible sets equal to the boundary tangent cone (the raw Issue-#55 graph condition is not part of this target — necessity audit report).
4. A comparison hypothesis for the limit problem (the Outcome-B block: scheme-level stability/contraction + relevant-gradient restriction + Soner-assumption mapping + theorem application; the H_proj regularity on the effective region is established in §3.5 parameter-generically and the discrete smooth-test consistency passage in monotone-scheme report §D.5).

The next report (strong-graph-target necessity audit) shows the raw graph condition is over-strong; the monotone-scheme report shows the consistency components, the local-state recovery bridge with the true χ algebra, the discrete smooth-test coercivity/localization, and isolates the Outcome-B unbounded-control numerical-scheme / state-constraint convergence-application block.
