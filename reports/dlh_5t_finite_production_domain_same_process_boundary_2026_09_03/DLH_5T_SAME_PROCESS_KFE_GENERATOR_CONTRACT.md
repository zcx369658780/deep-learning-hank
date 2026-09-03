# DLH-5T — Same-Process HJB–KFE Generator Contract on `D_W` (Issue #46, Phase E)

**Design only.** Freezes the scientific law that the boundary HJB process and the
future KFE generator describe **exactly the same controlled process**. No KFE
execution, no generator assembly, no `W_max` selection.

---

## 1. Central Route-D law (frozen)

```text
controlled process selected by boundary HJB
        ==
controlled process represented by KFE generator
```

This is the discrete/continuous form of the binding Issue #27 law:

```text
HJB boundary policy <=> KFE boundary transition law
```

## 2. Frozen `Q` conventions (preserves the accepted DLH-5D orientation)

```text
Q[row,col] > 0, row != col   =>   row -> col
Q V    = backward / HJB action
Q^T g  = forward / KFE action
```

The stationary KFE is the forward/adjoint equation `Q^T g = 0` with normalization
`sum_s g_s * cell_weight(s) = 1` and admissibility `g_s >= 0` (up to frozen
tolerances). Stationary KFE remains **NOT AUTHORIZED** in this Issue; this section
freezes the generator contract a successor must satisfy.

## 3. Same-process requirements (frozen)

1. **No KFE-only clipping**: the KFE cannot suppress a materially outward HJB policy
   after the fact. If the boundary HJB/KKT itself produces an inadmissible requested
   outward policy, that is a **boundary-HJB scientific failure**, never a KFE repair.
2. **Every KFE transition corresponds to an HJB-admitted controlled transition**: the
   off-diagonal transition set of the generator is a subset of the controlled
   transitions the boundary HJB admits.
3. **No KFE-only clipping of tangential flow**: on the W face the HJB-admitted policy
   may select a tangential drift (`mu_b > 0, mu_a < 0, mu_W <= 0`); the generator
   must represent that admitted tangential transition, not silently suppress it
   (this is the W1 discrete matching point of the W-domain report, §3.4).
4. **Diagonal rule**: `Q[i,i] = -sum_{j != i, j admitted} Q[i,j]` — the diagonal
   equals minus the sum of the ACTUALLY admitted represented off-diagonal rates.
5. **No omitted outward destination with retained diagonal rate**: no boundary rate
   may be kept in the diagonal if its destination transition is omitted (accepted
   DLH-5D §4.1; forbids the MATLAB-faithful leaky construction).
6. **Future conservative generator invariants** (within the frozen DLH-5D
   tolerances): row sums = 0, off-diagonals nonnegative. The same stencil and
   admitted-transition set are used for `Q V` (backward/HJB) and `Q^T g`
   (forward/KFE).
7. **Reported, not hidden**: any requested outward boundary drift above the frozen
   tolerance is reported as `BOUNDARY_POLICY_VIOLATION` (fail-closed), per the
   accepted DLH-5D contract — never silenced by clipping.

## 4. Mapping onto the W1 masked lattice

The generator on `S = {(i,j,n): a_j + b_i <= W_max}`:

- Interior states: standard split upwind over admitted axial neighbors and the
  `z`-switch.
- Axial faces (`a=0`, `b=b_min`, `a=a_max`): one-sided upwind over admitted
  destinations; the KKT law makes the outward-normal drift non-positive, so no
  outward rate is requested.
- W-frontier states: the outward-normal drift is non-positive by the KKT law
  (`mu_W <= 0`), so no outward normal flux is requested; the **tangential** drift
  representation is the open point of the W-domain report §3.4. Until that
  off-axis construction is resolved (bounded follow-up design), the exact discrete
  generator stencil on the W face is **not uniquely defined** — any chosen stencil
  must preserve requirements 2, 4, 5, 6, but the choice is not determined by the
  accepted science and cannot be validated in this design-only gate.

Consequence (frozen): the W1 discrete process-matching ambiguity is precisely the
point at which an implementation-ready generator contract cannot be completed in
DLH-5T; this is the basis of the Outcome B terminal (Phase H).

## 5. Contamination / pin-row placement (preserve, do not redesign)

Preserve the accepted Issue #27 interpretation, unchanged:

- singularity of a conservative KFE generator is expected (1-dimensional nullspace),
  not a failure;
- MATLAB-style contaminated-row / component-pin normalization remains an authorized
  numerical normalization device in principle;
- the pin fixes scale only; later stationary acceptance requires the ORIGINAL
  unmodified residual `||Q^T g||_inf`, mass/non-negativity and admissibility
  diagnostics, and admissible-pin invariance (DLH-5D §3-§7);
- the `0.37*N` parity convention and the contamination index are NOT re-optimized or
  changed in DLH-5T.

The only DLH-5T requirement: place contamination **downstream**, strictly after a
scientifically accepted same-process conservative generator exists:

```text
accepted same-process conservative Q
        -> stationary normalization device (pin) later
```

Contamination plays **no role** in boundary-policy selection or repair.

## 6. No-execution statement

No stationary KFE, no density solve, no generator assembly, no contamination run, no
pin sensitivity, no `C,L,A,B`, no aggregates, no two-region rebuild. This report is a
contract freeze only.
