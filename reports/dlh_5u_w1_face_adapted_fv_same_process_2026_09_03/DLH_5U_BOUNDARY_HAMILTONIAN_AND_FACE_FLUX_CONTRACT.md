# DLH-5U — Boundary Hamiltonian and Face-Flux Contract (Issue #47, Phase 7 + 8)

**Design only.** Freezes the constrained Hamiltonian at boundary/cut cells and the
face-flux evaluation rule for the Route-F monotone conservative generator. No
implementation, no generator assembly, no `W_max` selection.

---

## 1. Constrained Hamiltonian at a cell (frozen, inherits DLH-5T)

At every represented cell `s=(a_j,b_i,z_n)` the HJB is

```text
rho*V_s = sup_{c,l,d} { u(c) - v_l(l) + (Q V)_s + (Switch V)_s }
```

where `(Q V)_s = sum_r q_{s->r}(V_r - V_s)` uses the cell's controlled drift
`mu_s = (mu_a, mu_b)_s` and `(Switch V)_s` is the accepted finite-state `z`-switch
action. At a boundary cell the supremum is over controls admissible to the active
tangent cone of the cell's physical faces (DLH-5T laws):

```text
a=0 (cell touches it):      mu_a >= 0
b=b_min (cell touches it):  mu_b >= 0
a=a_max (cell touches it):  mu_a <= 0
W (|F_s^W| > 0):            mu_W = mu_a + mu_b <= 0
```

Unified KKT convention (frozen, per DLH-5T): with outward normals `n`, the active
constraints are `g = mu·n <= 0`; the Lagrangian subtracts `lambda_j * g_j`,
`lambda_j >= 0`, `lambda_j * g_j = 0`; effective gradients are `V - lambda_j n_j`
(lower faces add, upper/W faces subtract). The control FOCs use the effective
gradients:

```text
c:  u'(c) = V_b^eff                 => c = (V_b^eff)^(-1/gamma_c)
l:  l = (V_b^eff * net_wage / labor_weight)^(1/phi)
d:  q_eff = V_a^eff/V_b^eff - 1;  d = max(a,a_bar)*(min(q_eff+chi_0,0)+max(q_eff-chi_0,0))/chi_1
```

with the `lambda_W` linear-transfer cancellation and the `a=0 => mu_a = d` and
`a=a_max => mu_a = 0.27 + d` facts preserved from DLH-5T. If a boundary cell's
constrained problem admits no admissible policy, that is a boundary-HJB scientific
failure (reported, not repaired by KFE).

## 2. Face-flux evaluation rule (Issue #47 §8) — frozen

The generator off-diagonal rate is the **positive HJB-admitted outward flux through
the actual shared face divided by the cell measure**:

```text
q_{s->r} = |F_{s,r}| * max( mu_s . n_{s,r} , 0 ) / omega_s       (s != r)
Q[s,s]   = - sum_{r != s} q_{s->r}
```

Frozen flux-evaluation choice: **source-state (upwind) drift `mu_s`**, i.e. the
KKT-admissible controlled drift evaluated at the source cell `s`, dotted with the
outward normal of the shared face `F_{s,r}`. Justification:

- Monotonicity: `max( . , 0 )` with source-state drift makes `Q[s,r] >= 0` by
  construction for every `s != r`.
- Conservation: `Q[s,s] = -sum_{r != s} q_{s->r}` gives exactly zero row sums.
- No outward destination omitted by the mask retains a diagonal rate: the diagonal
  is defined as minus the sum of ACTUALLY admitted represented off-diagonal rates
  (a rate whose destination has no represented cell is simply not assembled and not
  in the diagonal) — this is the DLH-5D §4.1 rule.
- The physical W-segment and economic axial faces are NOT shared faces (they are
  domain boundary); they contribute **no** flux. In particular, on the W segment the
  outward-normal flux is `max(mu_W, 0)/sqrt(2)` and the KKT law gives `mu_W <= 0`, so
  the W-segment flux is identically zero — the KKT excludes the outward flux, never
  KFE clipping.

Why not face interpolation / face-local HJB control as the primary rule:

- Face interpolation of the drift would require a face-value construction and, for
  the value/control coupling, would not be monotone in general; the source-state
  upwind rule is the standard monotone conservative choice and the accepted DLH-5D
  diagonal contract.
- Face-local HJB control would place a control on each face, duplicating unknowns and
  breaking the cell-level same-process object (Phase 3 selection of node/cell-based
  control).
- Face interpolation MAY appear only as a documented higher-order variant in a future
  implementation-validation gate; the frozen Route-F primary rule is source-state
  upwind.

## 3. Required generator properties (frozen, Issue #47 §8)

1. Off-diagonal rates `>= 0` — by `max(.,0)`.
2. Row sums exactly zero — by the diagonal definition.
3. No positive physical W-normal flux when KKT gives `mu·n_W <= 0` — W segment is a
   boundary face with zero flux; the normal component is `max(mu_W,0) = 0`.
4. No external omitted destination with retained diagonal exit rate — omitted
   destinations are not assembled and not in the diagonal.
5. No hidden reflection — the scheme never redirects a drift into the opposite axial
   direction (see the tangential report, §3).
6. No arbitrary transfer of b-motion into a-motion — each rate uses only the drift
   component along its own face normal (`mu_a` on a-faces, `mu_b` on b-faces); no
   cross-terms are introduced (see the tangential report).
7. Same `Q` for backward and forward process — one generator object (Phase 5 report).

## 4. Boundary/admitted-rate diagnostics for a successor

Freeze the successor diagnostic set (no execution here): per-cell active-face
classification; per-cell KKT multipliers (feasibility `lambda >= 0`, complementarity);
per-face admitted rate `q_{s->r}` and `|F_{s,r}|`, `omega_s`; row-sum residual;
W-segment normal flux residual; `BOUNDARY_POLICY_VIOLATION` semantics per DLH-5D.

## 5. Compliance

No rates are assembled numerically; no generator is built; no execution. This is the
frozen contract the successor implementation authority will realize.
