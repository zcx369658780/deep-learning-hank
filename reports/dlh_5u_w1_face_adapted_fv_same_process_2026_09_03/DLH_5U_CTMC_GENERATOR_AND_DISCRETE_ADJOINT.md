# DLH-5U Rev 1 — CTMC Generator and Discrete Adjoint (Issue #47, Phase 9 + 10)

**Rev 1 status:** DOCUMENTATION / ANALYTIC CORRECTION ONLY. Aligns the frozen
generator/adjoint with the Rev-1 tessellation, the discrete Hamiltonian, and the
candidate status of the tangential representation (reviewer comment `5521119160`). No
generator assembly, no execution, no `W_max` selection.

---

## 1. One discrete process (frozen)

Route F represents the controlled wealth/portfolio process on the W1 masked lattice as
a conservative CTMC over the represented states, with generator `Q` built from the
Phase-8 face-flux rule over the Rev-1 restricted-Voronoi control volumes
(`omega_s = area(C_s)`):

```text
q_{s->r} = |F_{s,r}| * max( mu_s(c,l,d) . n_{s,r} , 0 ) / omega_s     (s != r)
Q[s,s]   = - sum_{r != s} q_{s->r}
```

The control `(c,l,d)` at cell `s` maximizes the DISCRETE Hamiltonian `H_h`
(Phase-8 report) subject to the cell tangent cone; the control enters the rates
through the drift `mu_s(c,l,d)`.

Property set (frozen): off-diagonal `>= 0`; row sums `= 0`; physical W segments and
axial economic faces carry no flux (`max(mu_W,0)=0` on the W segment by the KKT);
masked destinations not assembled and not in the diagonal; z-switch is a separate
conservative finite-state Markov generator combined additively (Kronecker):

```text
Q_total = Q_wealth (x) I_z + I_w (x) Q_switch
Q_switch = la_mat   (rows sum to 0, accepted frozen rates)
```

Negative-b effective liquid return / borrowing-rate-gap preserved exactly (lives in
`mu_b` accounting; untouched).

**Candidate status (Rev 1):** the tangential representation at W-adjacent cells is
NOT frozen as a viable same-process resolution — the two-step cascade is downgraded
to a diagnostic/candidate construction, and tangential same-process consistency is
the bounded unresolved object (see `DLH_5U_TANGENTIAL_REALLOCATION_AND_CONSISTENCY.md`).

## 2. Same-process adjoint pair (frozen)

With ONE generator `Q`:

```text
backward (HJB action):   (Q V)_s = sum_r q_{s->r}(c,l,d) (V_r - V_s)
forward  (mass KFE):     p_dot = Q^T p,    p = probability mass on cell s
```

- HJB is `rho V = sup H_h(c,l,d)` with `H_h` the discrete Hamiltonian; the control
  and the rates are the same object used by the forward process.
- No independently constructed HJB matrix and KFE matrix: the transition law is
  derived once, and the forward generator is the exact transpose of the backward
  generator.
- Mass conservation: `(Q 1)_s = 0` implies `d/dt sum p = 1^T Q^T p = (Q 1)^T p = 0`.
- Stationary mass: `Q^T p = 0`, `sum p = 1` (mass form is the generator's natural
  forward variable; see the mass/density report).

## 3. Junction with the interior operator (frozen)

The accepted source-faithful interior operator (standard axial upwind on interior
cells) and the Route-F cut-cell layer use the identical face-flux formula. An interior
cell is the full-adjacency special case (`C_s` = base rectangle); a frontier cell is
the Voronoi-polygon case with a physical W segment. The interface rates use the same
rule and sign convention, so no separate junction stencil is required.

## 4. Boundary / same-process guarantee (Rev 1)

- The cell control (discrete-Hamiltonian maximizer under the cell tangent cone)
  determines the drift that yields the W-segment no-flux and axial no-flux — the
  controlled process selected by the boundary HJB and the process represented by the
  KFE generator use the SAME `Q` (same-process law at the discrete level).
- No `BOUNDARY_POLICY_VIOLATION` is possible by construction on the W segment
  (`max(mu_W,0)=0`); a future implementation reporting one must fail closed per
  DLH-5D.
- The tangential *drift* consistency at W-adjacent cells is NOT claimed in this
  report; it is the bounded unresolved object (tangential report §6). This does not
  affect the frozen conservation/monotonicity/no-flux/same-`Q` properties.

## 5. Compliance

No generator assembled, no HJB/KFE solved, no execution. Frozen contract only.
