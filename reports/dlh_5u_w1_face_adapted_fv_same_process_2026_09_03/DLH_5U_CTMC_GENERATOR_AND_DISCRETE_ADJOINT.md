# DLH-5U — CTMC Generator and Discrete Adjoint (Issue #47, Phase 9 + 10)

**Design only.** Freezes the single discrete controlled process and its backward /
forward adjoint pair. No generator assembly, no execution, no `W_max` selection.

---

## 1. One discrete process (frozen)

Route F represents the household's controlled wealth/portfolio process on the W1
masked lattice as a **conservative continuous-time Markov chain (CTMC)** over the
represented states, with generator `Q` built from the Phase-4 face-flux rule:

```text
q_{s->r} = |F_{s,r}| * max( mu_s . n_{s,r} , 0 ) / omega_s     (s != r)
Q[s,s]   = - sum_{r != s} q_{s->r}
```

Property set (frozen): off-diagonal `>= 0`; row sums `= 0`; boundary faces carry no
flux (physical W segments and axial economic faces excluded from the rate sum;
`max(mu_W,0)=0` on the W segment by the KKT); omitted destinations are not assembled
and carry no diagonal retention; the `z`-switch is a separate conservative finite-state
Markov generator combined additively (Kronecker):

```text
Q_total = Q_wealth (x) I_z + I_w (x) Q_switch
Q_switch = la_mat  (rows sum to 0, frozen accepted rates)
```

The negative-`b` effective liquid return / borrowing-rate-gap semantics are preserved
exactly: they live in `mu_b` (Phase-2 accounting) and are untouched by this Phase.

## 2. Same-process adjoint pair (frozen, Issue #47 §10)

With **one** generator `Q`:

```text
backward (HJB action):   (Q V)_s = sum_r q_{s->r} (V_r - V_s)
forward  (mass KFE):     p_dot = Q^T p,    p_s = probability mass on cell s
```

- The HJB is `rho V = u - v_l*l + Q V + Switch V`, with controls selected by the
  Phase-4 constrained Hamiltonian at boundary cells and interior FOC at interior
  cells, using the SAME rates the forward process uses.
- No independently constructed HJB matrix and KFE matrix: the transition law is
  derived once (the controlled drift -> face flux -> `q_{s->r}`), and the forward
  generator is the exact transpose of the backward generator.
- Mass conservation: `(Q 1)_s = 0` for all `s` implies `d/dt sum_s p_s =
  sum_s (Q^T p)_s = 1^T Q^T p = (Q 1)^T p = 0`, so total mass is exactly preserved.
- Stationary mass: `Q^T p = 0`, `sum_s p_s = 1` (the mass form is the generator's
  natural forward variable; see the mass/density report).

## 3. Junction with the interior operator (frozen, Issue #47 §14.8)

The accepted source-faithful interior operator (standard axial upwind on interior
cells) and the Route-F cut-cell layer use the **identical face-flux formula** (the
`|F|*max(mu·n,0)/omega` rule). An interior cell is exactly the special case where all
four axial shared faces exist and have full length; a cut cell is the case where some
axial faces are replaced by physical W segments (no flux). Because the formula is
common, the interface between the interior operator and the cut-cell layer is
seamless: the rates across the interface faces are computed by the same rule with the
same sign convention, so no separate junction stencil is required.

## 4. Boundary / same-process guarantee (frozen)

- The HJB boundary policy at boundary cells (constrained Hamiltonian with the KKT
  tangent cone) determines the drift that produces the W-segment no-flux and the
  axial-face no-flux — i.e. the controlled process selected by the boundary HJB is
  exactly the process represented by the KFE generator (DLH-5T central law, now at
  the discrete Route-F level).
- No `BOUNDARY_POLICY_VIOLATION` is possible by construction on the W segment:
  `max(mu_W,0)=0`. Any future implementation that reports one must fail closed per
  DLH-5D.

## 5. Compliance

No generator is assembled, no HJB/KFE solved, no execution. Only the frozen contract
is recorded.
