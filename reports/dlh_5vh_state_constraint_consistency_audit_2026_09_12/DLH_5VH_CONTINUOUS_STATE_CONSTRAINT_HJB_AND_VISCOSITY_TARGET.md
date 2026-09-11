# DLH-5V-H — Continuous State-Constraint HJB and Viscosity Target

**Sequence step A of Issue #56.** This report fixes the continuous state-constraint HJB object and its viscosity semantics BEFORE any numerical target is defined. No grid, aspect or stencil redesign is performed here; the frozen geometry is consumed as given.

---

## 1. Frozen continuous object (consume, do not reopen)

Production domain and laws (accepted; see TASK_INDEX / Roadmap V0.42):

```text
D_W(W_max) = { 0 <= a <= a_max, b >= b_min, a + b <= W_max }
a_max = 10, b_min = -2, no numerical W_max selected
```

Household dynamics: states (a, b) with drifts μ_a, μ_b produced by the household controls (c, l, d); running payoff u(c) − v_l·l. All economics frozen; the audit only fixes the mathematical target used to judge discrete schemes.

Project sign convention (maximization, discounted):

```text
ρ V(x) = sup_{controls} { u(c) − v_l·l + V_a(x)·μ_a + V_b(x)·μ_b }   (x in D_W°)
F(x, r, p) = ρ r − H(x, p),
H(x, p)   = sup_{controls} { u(c) − v_l·l + p_a·μ_a(x,u) + p_b·μ_b(x,u) }.
```

Viscosity conventions with this F (first-order, degenerate-elliptic form):

- **Subsolution** (test function φ ∈ C¹ touching V from above at x̂): `F(x̂, V(x̂), Dφ(x̂)) ≤ 0`, i.e. `ρV(x̂) ≤ H(x̂, Dφ(x̂))`.
- **Supersolution** (test function φ touching V from below at x̂): `F(x̂, V(x̂), Dφ(x̂)) ≥ 0`, i.e. `ρV(x̂) ≥ H(x̂, Dφ(x̂))`.

## 2. The state-constraint semantics (distinctions requested by Issue step A)

The audit fixes the following distinctions; they are the basis of the whole target.

### 2.1 Equation in the open domain

In `D_W°` (interior) both inequalities hold: V is a viscosity subsolution AND a viscosity supersolution of `F = 0` at every interior point. Interior test points use the unrestricted (interior) Hamiltonian H with the full reachable drift set.

### 2.2 Boundary semantics — three candidate objects, one theorem

(a) **Soner state-constraint (viscosity) boundary inequality.** V is a viscosity **subsolution on the closed domain D̄_W**: at every x̂ ∈ ∂D_W and every φ touching V from above at x̂, `ρV(x̂) ≤ H(x̂, Dφ(x̂))` with the *unrestricted* Hamiltonian H. The supersolution is required only in the interior. The boundary condition is therefore **one-sided** (an upper inequality only); there is no boundary supersolution requirement.

(b) **Tangent-cone-restricted (constrained) Hamiltonian.** `H_T(x,p) = sup_{controls : μ(x,u) ∈ T_D(x)} { u(c) − v_l·l + p·μ }` where T_D(x) is the tangent cone of D_W at x (full plane in the interior; on faces the active-face half-plane; at corners the intersection of the active-face half-planes). The constrained equation `ρV − H_T(x, DV) = 0` is then required to hold (in viscosity sense) on D̄_W.

(c) **Relaxed boundary operator.** Any operator built from a cone R(x̂) ⊇ T_D(x̂) (cone containment at the limit point) that is consistent with the reachable-drift structure. Interior-state limits produce exactly such operators (see Section 3).

**Standard equivalence (Soner 1986 I/II; Bardi–Capuzzo-Dolcetta Ch. IV; Capuzzo-Dolcetta–Lions 1990):** under standard hypotheses (convex domain, Lipschitz Hamiltonian, viability of the constrained dynamics, discounting) the value function of the state-constrained problem is characterized equivalently by (a) and by (b); and any operator of class (c) with R ⊇ T_D satisfies the subsolution inequality whenever (a)/(b) hold, because the Hamiltonian is monotone in the admissible cone (Lemma below). The project-specific verification of the hypotheses is an enumerated deliverable (capsule table).

### 2.3 Active-face laws as tangent cones

The accepted continuous laws are exactly the tangent-cone restrictions of the constrained Hamiltonian:

```text
a = 0        :  μ_a >= 0          (face cone {μ_a >= 0})
b = b_min    :  μ_b >= 0          (face cone {μ_b >= 0})
a = a_max    :  μ_a <= 0          (face cone {μ_a <= 0})
W face       :  μ_W = μ_a + μ_b <= 0   (face cone {μ_W <= 0})
corners      :  intersection of the active-face cones
```

Accepted corner semantics (from Issue #55 Rev 1, consumed): (0, W_max): {μ_a ≥ 0, μ_W ≤ 0}; (a_max, W_max − a_max): {μ_a ≤ 0, μ_W ≤ 0}; (a_max, b_min) for W_max > 8: {μ_a ≤ 0, μ_b ≥ 0} (W inactive); W_max = 8: triple {μ_a ≤ 0, μ_b ≥ 0, μ_W ≤ 0}; (0, b_min): {μ_a ≥ 0, μ_b ≥ 0}.

### 2.4 Viability / tangent controls

The supersolution side at boundary points (when needed) is sustained by *tangent* controls: drifts in T_D(x̂) keep the state inside D_W for small times, so the dynamic programming inequality `ρV ≥ g + Dφ·μ` holds for them; the constraint's content lives in the subsolution side. This is why (b) (constrained equation on the closure) and (a) (subsolution on the closure with H) are the two faces of one theorem, and why the one-sided asymmetry (subsolution on D̄, supersolution in D°) is the correct continuous target — not a symmetric graph condition.

## 3. The cone-monotonicity lemma (the load-bearing fact)

**Lemma (cone-monotonicity of the Hamiltonian).** For any two admissible-drift cones C ⊆ C′ (both contained in the reachable-drift set), the corresponding Hamiltonians satisfy `H_C(x,p) ≤ H_{C′}(x,p)` for every (x,p).

*Proof.* H_C is the supremum of the same affine family over a smaller index set. ∎

**Corollaries used throughout the audit.**

1. If V satisfies the state-constraint subsolution inequality with H_T (i.e. ρV ≤ H_T(x̂, p) for touching test functions — true under both (a) and (b)), then it satisfies it with ANY relaxed operator H_R built from a cone R ⊇ T_D(x̂): `ρV ≤ H_T ≤ H_R`.
2. Interior grid states approaching a boundary carry their *own* tangent cones (face laws at their own positions), which contain the boundary tangent cone in the directions relevant to the reachable drift set; the operators they produce are of class (c) and therefore subsolution-safe.
3. Supersolution-side dominance: an interior-state consistency that yields `ρφ ≥ H_int` (full cone) implies the boundary supersolution inequality `ρφ ≥ H_T` whenever H_T ≤ H_int (trivially true by cone containment T ⊆ full plane).

## 4. What the continuous target requires of a scheme (anticipation of step D)

A monotone scheme S_m for this problem must be judged against the operator/test-function object:

1. Interior consistency at interior states (both inequalities, via test functions).
2. One-sided boundary consistency: at boundary-contact states, consistency with an operator of class (c) whose cone contains T_D(x̂) at the limit (the frozen process supplies R ⊇ REV / TDEP at the W-corners — Section 4 of the frozen-process report).
3. No requirement that interior states approaching a boundary have admissible sets equal to the boundary tangent cone.

The next report (strong-graph-target necessity audit) shows that the Issue-#55 raw Kuratowski drift-set graph condition is NOT part of this target.
