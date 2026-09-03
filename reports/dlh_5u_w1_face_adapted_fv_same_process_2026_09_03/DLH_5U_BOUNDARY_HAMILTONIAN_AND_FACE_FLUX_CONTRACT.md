# DLH-5U Rev 1 — Boundary Hamiltonian and Face-Flux Contract (Issue #47, Phase 7 + 8)

**Rev 1 status:** DOCUMENTATION / ANALYTIC CORRECTION ONLY. Repairs BLOCKER 3
(discrete HJB control law from the same discrete `Q`) per reviewer comment
`5521119160`. No implementation, no generator assembly, no execution, no `W_max`
selection.

---

## 1. Discrete Hamiltonian (frozen — BLOCKER 3 repair)

The exact discrete HJB at cell `s` is control-dependent:

```text
rho V_s = sup_{c,l,d in admissible(s)} H_h(c,l,d)

H_h(c,l,d) = u(c) - v_l(l)
           + sum_r q_{s->r}(c,l,d) [V_r - V_s]
           + (Switch V)_s
```

- The rates `q_{s->r}(c,l,d)` are the Phase-8 face-flux rates built from the
  controlled drift `mu_s(c,l,d) = (mu_a, mu_b)_s(c,l,d)` of the control volume `C_s`
  (Rev-1 tessellation).
- `admissible(s)` is the cell tangent cone: `mu_W <= 0` iff `|F_s^W| > 0`;
  `mu_a >= 0` iff the cell touches `a=0`; `mu_b >= 0` iff it touches `b=b_min`;
  `mu_a <= 0` iff it touches `a=a_max` (cell-boundary conditions per the geometry
  report §3).
- **Boundary controls maximize THIS discrete Hamiltonian.** They do NOT
  automatically satisfy the continuous DLH-5T effective-gradient FOCs
  (`u'(c) = V_b^eff`, `l = (V_b^eff * net_wage / labor_weight)^(1/phi)`,
  `d = max(a,a_bar)(min(q+chi_0,0)+max(q-chi_0,0))/chi_1` with
  `q = V_a^eff/V_b^eff - 1`).
- The continuous DLH-5T FOCs are frozen as **consistency targets / refinement
  limits** only: they are the correct discrete FOCs only where an equivalence
  derivation shows the discrete backward action reduces to
  `V_a mu_a + V_b mu_b` to the required order. No such equivalence is claimed at the
  W-adjacent cells in this gate (the tangential report shows the discrete action does
  NOT reduce to `mu·grad V` there for fixed aspect ratio); at strictly interior
  cells the standard upwind discrete action is `mu_a (V_{j+1}-V_{j-1})/(2da)-` style,
  so the continuous FOC is a target, and the exact discrete maximizer is what the
  discrete HJB selects.
- Note the non-smoothness: `q_{s->r}` contains `max(mu_s . n_{s,r}, 0)`, so the
  discrete FOC for `d` (and the switching of `c,l` across rate-activation thresholds)
  is a cell-local, rate-dependent, non-smooth optimization, distinct from the smooth
  continuous FOC. A successor implementation must maximize `H_h` directly (with the
  KKT complementarity on the active cell tangent constraints), not substitute the
  continuous FOC.

## 2. Face-flux evaluation rule (unchanged in form, control enters the drift)

```text
q_{s->r} = |F_{s,r}| * max( mu_s(c,l,d) . n_{s,r} , 0 ) / omega_s       (s != r)
Q[s,s]   = - sum_{r != s} q_{s->r}
```

- Source-state (upwind) drift `mu_s(c,l,d)` evaluated at the cell control.
- Monotonicity: `max(.,0)` makes `Q[s,r] >= 0`.
- Conservation: diagonal `= -sum(actually assembled rates)`; row sums exactly zero.
- Masked destinations are not assembled and not in the diagonal (DLH-5D rule).
- Physical W segments and axial economic faces are not shared faces; they carry no
  flux. On the W segment the outward-normal flux is `max(mu_W, 0)/sqrt(2)`; the KKT
  (`mu_W <= 0`) makes it identically zero — the KKT excludes the outward flux, never
  KFE clipping.
- The rates depend on the control `(c,l,d)` through `mu_s`; HJB and KFE use the same
  `q_{s->r}(c,l,d)` evaluated at the converged policy (same-process law).

## 3. Required generator properties (unchanged)

1. Off-diagonal `>= 0`.
2. Row sums exactly `0`.
3. No positive physical W-normal flux when KKT gives `mu_W <= 0`.
4. No external omitted destination with retained diagonal exit rate.
5. No hidden reflection (no drift redirected into the opposite axial direction).
6. No arbitrary transfer of b-motion into a-motion at a single cell (each rate uses
   only its own face-normal drift component).
7. Same `Q` for backward and forward process.

## 4. Boundary-control location (BLOCKER 3 — coherent object)

Frozen object: **node value + cell-level constrained control** (geometry report §3).
- Value `V_s` at the represented node; control at the cell `C_s`.
- W KKT imposed iff `|F_s^W| > 0` (cell has a physical W segment), with the
  cell-shrinkage convergence argument (node within `O(h)` of the face as `h -> 0`).
- The discrete Hamiltonian maximization (Section 1) is the control-selection object;
  the continuous FOC is the refinement limit.
- HJB and KFE consume the same control/flux object.

## 5. Successor diagnostics (frozen, no execution here)

Per-cell active-face classification; per-cell KKT multipliers (feasibility
`lambda >= 0`, complementarity on the cell tangent cone); per-face admitted rate
`q_{s->r}` and `|F_{s,r}|`, `omega_s`; row-sum residual; W-segment normal-flux
residual; `BOUNDARY_POLICY_VIOLATION` fail-closed semantics per DLH-5D.

## 6. Compliance

No rates assembled, no generator built, no execution. Frozen contract only.
