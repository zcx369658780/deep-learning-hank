# DLH-5U — Control-Volume Geometry and Boundary-Control Location (Issue #47, Phase 6 + 7)

**Design only.** Freezes the Route-F clipped-control-volume construction and the
location of the constrained HJB control. No implementation, no `W_max` selection.

---

## 1. Primary geometric object (frozen)

Route F audits the physical clipped control-volume construction

```text
C_s = C_s^base ∩ D_W(W_max)
```

where `C_s^base` is the native Cartesian dual (control) cell associated with the
represented state `s = (a_j, b_i, z_n)`.

### 1.1 Node-centered Cartesian dual (frozen construction)

On the accepted tensor lattice `{b_i}_{i=0}^{I-1}` (`b_0 = b_min`, uniform `db`) and
`{a_j}_{j=0}^{J-1}` (`a_0 = 0` at the `a>=0` face, `a_{J-1} = a_max`, uniform `da`),
the base dual cell of node `(i,j)` is the closed rectangle

```text
C_{(i,j)}^base = [a_{j-1/2}, a_{j+1/2}] × [b_{i-1/2}, b_{i+1/2}]
a_{j-1/2} = a_j - da/2, a_{j+1/2} = a_j + da/2   (with a_{-1/2}=0, a_{J-1+1/2}=a_max)
b_{i-1/2} = b_i - db/2, b_{i+1/2} = b_i + db/2    (with b_{0-1/2}=b_min)
```

The `a=0`, `b=b_min`, `a=a_max` faces are physical faces of `D_W` and the adjacent
dual cells are the standard boundary half-cells (e.g. the `j=0` cell is
`[0, da/2] × …`). The base cells tile the full rectangle; clipping by `D_W`
partitions `D_W` exactly:

```text
D_W = ⊔_s C_s,   C_s = C_s^base ∩ D_W  (disjoint union over represented states s)
```

A masked-out node (`a_j + b_i > W_max`) has zero-measure clipped cell and is NOT a
represented state.

### 1.2 Frozen geometric objects per cell (Issue #47 §6)

For every represented state `s=(i,j,n)`:

| Object | Definition |
|---|---|
| represented native state | `s = (a_j, b_i, z_n)`, `a_j + b_i <= W_max` |
| base cell | `C_s^base` (Section 1.1) |
| clipped cell | `C_s = C_s^base ∩ D_W` |
| cell measure | `omega_s = area(C_s)` (in `(a,b)`, per z-state; no `dz` factor) |
| actual shared face | `F_{s,r} = ∂C_s ∩ ∂C_r` (1-D segment, positive length) between adjacent cells |
| face measure | `|F_{s,r}| = length(F_{s,r})` |
| outward normal | `n_{s,r}` = unit normal of `F_{s,r}` pointing from `s` to `r` |
| physical W segment | `F_s^W = ∂C_s ∩ {a+b = W_max}` (possibly empty) |
| W normal | `n_W = (1,1)/sqrt(2)` |
| economic axial faces | the segments of `∂C_s` lying on `a=0`, `b=b_min`, `a=a_max` (boundary, no flux) |
| face intersections | shared-face endpoints and clipped-cell vertices (Section 2) |
| adjacency graph | cells `s~r` iff `|F_{s,r}| > 0` |

### 1.3 Physical W face ≠ staircase of masked nodes (frozen, critical)

The **physical W boundary** is the straight segment family of `{a+b = W_max} ∩ D_W`,
partitioned into the physical W segments `F_s^W` of the cut cells. The **staircase**
(of masked nodes: a state whose `+a` or `+b` neighbor lies outside the mask) is only
a node-mask description and is **not** the physical boundary. In particular:

- a node is a physical W-boundary point iff its clipped cell has a positive-length
  W segment `F_s^W` (i.e. the base cell crosses the line `a+b=W_max`);
- a node whose `+a`/`+b` neighbor is masked may still be geometrically interior (its
  clipped cell equals its base cell) or may be a genuine cut cell; the two notions
  are distinct;
- W-face KKT conditions are attached to **cells with a positive-length `F_s^W`**
  (boundary cells), never to a masked-node staircase by itself.

### 1.4 Cut cells and the W-frontier band

Let `h = max(da, db)`. The cut cells (with `|F_s^W| > 0`) form an `O(h)`-thick band
adjacent to the physical W face. For a cut cell, the base-cell corner
`(a_{j+1/2}, b_{i+1/2})` lies outside `D_W` (`a_{j+1/2}+b_{i+1/2} > W_max`) while the
node itself is in `D_W`. Because `a_{j-1/2}+b_{i-1/2} < a_j+b_i <= W_max`, every cut
cell retains **positive-length** `-a` and `-b` faces (toward interior cells), so the
adjacency graph over `D_W` is connected and no cell is isolated.

## 2. Face intersections and cell-shape classification (symbolic `W_max`)

Regime I (`W_max >= a_max + b_min`, production regime): the domain is the trapezoid
with faces `a=0`, `b=b_min`, `a=a_max`, `W`. Cut cells occur along the W face and at
the two W-face endpoints (`a=0 × W` at `(0,W_max)` and `a=a_max × W` at
`(a_max, W_max-a_max)`).

Regime II (`b_min <= W_max < a_max + b_min`): the `a=a_max` face is outside; cut cells
along the W face and at `a=0 × W`, `b=b_min × W`.

For every cut cell the clipped cell is either:

- a **triangle** (the W line cuts off one corner of the base rectangle), or
- a **pentagon** (the W line cuts off a corner leaving a truncated rectangle), or
- a **quadrilateral** (two corners cut).

The explicit vertex set of `C_s` is obtained by intersecting the base-rectangle edges
with `a+b=W_max`; the physical W segment is the portion of the line inside the base
cell. These are the exact cell objects a successor implementation must construct.

## 3. Boundary-control location (Issue #47 §7) — frozen selection

**Selected: Option A/B — node/cell-based constrained control with the cut-cell
finite-volume boundary correction.** (For the node-centered dual, Options A and B
coincide: the control-volume state is the node; the constrained Hamiltonian lives at
the cell.)

Freeze the following interpretation:

1. The HJB value function and the household controls `(c,l,d)` live at each
   represented cell/state `s` (node-centered, cell-valued control).
2. At a **boundary cell** (a cell with a positive-length physical face `F_s^W`, or
   touching `a=0`, `b=b_min`, `a=a_max`), the control is the **constrained
   Hamiltonian maximizer** over controls admissible to the active tangent cone of the
   cell's physical faces, using the effective-gradient KKT structure of the accepted
   DLH-5T laws (each active physical face contributes its multiplier to the effective
   gradients; lower faces `V+lambda`, upper/W faces `V-lambda`).
3. At a **strictly interior cell** (clipped cell equals base cell, no physical W
   segment, not touching `a=0`/`b=b_min`/`a=a_max`), the control is the
   unconstrained interior FOC (no KKT multiplier).
4. The W-face KKT (`mu_W <= 0`) is imposed **only on cells with a positive-length
   `F_s^W`** (boundary cells), never on a strictly interior cell. Consistency
   argument (h->0): as the grid refines, a cut cell shrinks toward its node; the
   tangent cone of the cell's boundary converges to the tangent cone of `D_W` at the
   boundary point, so imposing the KKT on boundary cells is the standard
   state-constraint boundary-cell interpretation with a clear refinement meaning. If
   `mu_W <= 0` is non-binding at a cut cell (`lambda_W = 0` by complementarity), the
   constrained policy coincides with the interior policy, so the cut-cell/interior
   interface has no artificial discontinuity.
5. The accepted physical boundary law `mu_W <= 0` (and the axial-face laws) is
   preserved exactly; the boundary-cell approximation has the explicit h->0
   refinement interpretation of (4).
6. **HJB and KFE consume the same face/control object**: the control at cell `s`
   determines the drift `(mu_a,mu_b)_s`, which feeds the SAME face-flux formula used
   for both the backward HJB action and the forward KFE generator (Phase 5 report).

Why not the alternatives:

- **Option C (physical-face Hamiltonian/control coupled to interior unknowns):**
  rejected as primary — it introduces an additional set of boundary unknowns and a
  nonstandard coupling closure, whereas Option A/B places the control on the
  represented state, matching the accepted node-based policy object and the value
  function's natural degrees of freedom.
- **Option D (other bounded Route-F construction):** not needed; Option A/B together
  with the clipped-FV flux is coherent and complete.

## 4. Refinement interpretation (frozen)

For `h -> 0` with `da/db` fixed (or `da, db -> 0`), the collection of clipped cells
approximates `D_W` in the Hausdorff sense; the physical W segments converge to the
line `a+b=W_max`; the cell measures `omega_s -> da*db` away from the face and shrink
as `O(h)` for cut cells. The boundary-cell KKT (Section 3.4) converges to the
continuous state-constraint at the W face. First-order local-moment consistency is
established in the tangential-reallocation and consistency report.

## 5. Compliance

No control-volume implementation, no mask implementation, no slanted-stencil
implementation. All objects above are symbolic/analytic definitions to be realized by
a successor implementation authority.
