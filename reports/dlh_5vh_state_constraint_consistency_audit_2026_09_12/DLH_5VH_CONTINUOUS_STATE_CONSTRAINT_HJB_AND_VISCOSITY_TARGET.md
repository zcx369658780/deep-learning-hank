# DLH-5V-H — Continuous State-Constraint HJB and Viscosity Target (Micro-Rev Rev 2)

**Sequence step A of Issue #56; Micro-Rev tasks A and B.** This report fixes the continuous state-constraint HJB object and its viscosity semantics BEFORE any numerical target is defined, records Soner's actual sign convention and derives the project transform explicitly (Task A), and demotes the tangent-cone-restricted Hamiltonian to an auxiliary object (Task B). Rev 2 adds the corrected boundary-transfer statement (the subsolution on the closure is obtained via the restriction H_lim ≤ H_proj, not via any constrained characterization) and updates the auxiliary-role list of H_T accordingly. No grid, aspect or stencil redesign is performed; the frozen geometry is consumed as given.

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

The supersolution side at boundary points (when the comparison class requires it) is sustained by *tangent* controls: drifts in T_D(x̂) keep the state inside D_W for small times. The constraint's content lives in the one-sided subsolution side. The following are **NOT established in this audit and form the single bounded Outcome-B block**:

1. **Project-specific state-constraint comparison/unique-continuation theorem** for the project's continuous limit problem (subsolution on the closure w.r.t. H_proj vs supersolution in the interior w.r.t. H_proj — the Soner II / Capuzzo-Dolcetta–Lions maximal-subsolution form): needed to pass from the halves ū, u̲ to u_m → V. Its applicability under project hypotheses (bounded continuous V, H_proj continuous in (x,p) and Lipschitz in p, compact D_W, ρ > 0) is plausible but requires the primary-text theorem application.
2. **Constrained characterization `ρV ≤ H_T` at the boundary** (the Soner⟷H_T equivalence content): a coupled sublemma of the same block — NOT needed for the transfer (the transfer closes via the restriction H_lim ≤ H_proj, monotone-scheme report §D.2), but needed to identify the boundary limit as the H_T-constrained solution.

The audit does not assume either; the W-contact-state branch of the boundary subsolution transfer is closed without them (§D.2).

## 4. What the continuous target requires of a scheme (Rev 2)

A monotone scheme S_m for this problem is judged against the operator/test-function object:

1. Interior consistency at interior states (both inequalities, via test functions).
2. One-sided boundary consistency at boundary-contact states: the half-relaxed-limit subsolution `ρφ(x̂) ≤ H_lim(x̂, Dφ(x̂))` with H_lim ≤ H_proj at the visited states (restriction argument) — i.e., the discrete Hamiltonian at the W-contact states must not exceed the full Hamiltonian's limit (buffered candidate sets ⊆ full candidate sets), and the recovery side liminf H_R ≥ H_T holds at the corners/faces (local-state same-candidate recovery — the exact statement and its control-level content are in the monotone-scheme report §D.2, §E.4).
3. No requirement that interior states approaching a boundary have admissible sets equal to the boundary tangent cone (the raw Issue-#55 graph condition is not part of this target — necessity audit report).
4. A comparison hypothesis for the limit problem (the Outcome-B block).

The next report (strong-graph-target necessity audit) shows the raw graph condition is over-strong; the monotone-scheme report shows the consistency components, the local-state recovery bridge, and isolates the Outcome-B comparison block.
