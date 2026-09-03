# DLH-5U Rev 1 — Control-Volume Geometry and Boundary-Control Location (Issue #47, Phase 6 + 7)

**Rev 1 status:** DOCUMENTATION / ANALYTIC CORRECTION ONLY. Repairs BLOCKER 1
(tessellation) and BLOCKER 3 (boundary-control object) per controlling reviewer
comment `5521119160`. No implementation, no execution, no `W_max` selection.

---

## 1. Rev-0 error withdrawn (BLOCKER 1)

Rev 0 asserted that a masked-out native node (`a_j + b_i > W_max`) has zero-measure
intersection of its Cartesian dual cell with `D_W`, and that
`{C_s^base ∩ D_W}` over represented nodes partitions `D_W`. **This is withdrawn.**
A masked node with `a_j + b_i - W_max = delta < (da+db)/2` has a positive-area
lower-left triangular intersection with `D_W`. Therefore the Rev-0 collection of
base-clipped dual cells centered only on represented nodes does **not** generically
partition `D_W`: it leaves uncovered slivers (pieces "owned" by outside-centered
masked nodes). No grid-alignment or `W_max`-alignment assumption is authorized to
avoid this.

## 2. Rev-1 frozen tessellation: restricted Voronoi dual cells (BLOCKER 1 repair)

### 2.1 Definition (frozen, fully deterministic)

Represented state set (W1 mask, unchanged):

```text
S = { s = (i,j,n) : a_j + b_i <= W_max }     (per z-state n)
```

For each represented `s = (i,j)` (any `n`), the control volume is the restricted
Voronoi cell induced ONLY by the represented node set, clipped to `D_W`:

```text
C_s = { x = (a,b) in D_W : ||x - s||_2 <= ||x - r||_2  for all represented r in S }
    = (  ∩_{r in S, r != s} H_{sr} )  ∩  D_W
H_{sr} = { x : ||x - s||_2 <= ||x - r||_2 }   (bisector half-space of the represented pair)
```

### 2.2 Partition theorem (frozen)

```text
D_W =  ⊔_{s in S} C_s   (disjoint union up to measure-zero boundaries)
```

Proof: for every `x in D_W`, the finite set `{||x-r||_2 : r in S}` attains a minimum
at some `s`; `x in C_s` then holds, and distinct `C_s` overlap only on bisectors
(measure zero). Hence the cells tile `D_W` exactly (a.e.). This is the genuine
ownership rule over the ACTUAL represented state set; no masked state is added, no
cell lacks a represented W1 state.

### 2.3 Cell shapes (frozen)

- **Interior cell:** if all four axial neighbors of `s` are represented and the base
  rectangle lies strictly inside `D_W`, the nearest represented nodes are the axial
  neighbors; their mid-line bisectors bound the base rectangle, and all other
  represented nodes are farther, so

  ```text
  C_s = [a_j - da/2, a_j + da/2] x [b_i - db/2, b_i + db/2]   (base dual rectangle)
  ```

- **Frontier cell:** otherwise `C_s` is the convex Voronoi polygon (intersection of
  the bisector half-spaces with `D_W`); it extends into the region of the masked
  neighbors (absorbing the previously uncovered pieces), is bounded, and has a
  positive-length physical W segment `F_s^W = ∂C_s ∩ {a+b = W_max}` iff the base
  rectangle crosses the W line (the cell genuinely touches the W face).
- The exact vertices of frontier cells are computed by a successor implementation
  from the frozen half-plane definition (no additional scientific choice).

### 2.4 Derived objects (frozen, recomputed from the tessellation)

| Object | Definition (Rev 1) |
|---|---|
| cell measure | `omega_s = area(C_s)` (per z-state; no `dz`) |
| shared face | `F_{s,r} = ∂C_s ∩ ∂C_r`, a 1-D segment of positive length |
| face measure | `|F_{s,r}| = length(F_{s,r})` |
| outward normal | `n_{s,r}`, unit normal of `F_{s,r}` pointing `s -> r` |
| physical W segment | `F_s^W = ∂C_s ∩ {a+b=W_max}` (positive length iff the cell touches W) |
| W normal | `n_W = (1,1)/sqrt(2)` |
| axial economic faces | segments of `∂C_s` on `a=0`, `b=b_min`, `a=a_max` (no flux) |
| adjacency graph | `s ~ r` iff `|F_{s,r}| > 0` (connected over `S`; every represented cell has at least one interior shared face because `a_j - da/2 + b_i - db/2 < a_j + b_i <= W_max`) |

### 2.5 Physical W face vs staircase (unchanged, now exact)

The physical W boundary is the straight line `a+b=W_max` partitioned into the
segments `F_s^W` of the frontier cells (a convex partition of the face). The
staircase of masked nodes is only a node-mask description, not the physical
boundary. W-face constraints attach to cells with `|F_s^W| > 0`.

### 2.6 Sliver logic (Rev 1, frozen)

- A cell is a **sliver / small cell** if `omega_s < delta * da * db` for a frozen
  pre-registered threshold `delta in (0,1]` (e.g. candidate value `1/4`, registered
  later in the W_max adequacy protocol, never loosened for a PASS).
- Sliver remedy (frozen): (a) a geometric admissibility condition on future `W_max`
  candidates — every cell must satisfy `omega_s >= delta*da*db`; (b) deterministic
  agglomeration of any sub-threshold cell into the adjacent cell sharing the largest
  shared face, transferring measure, faces and flux identically on HJB and KFE sides;
  (c) no `W_max` selected to avoid cut cells; no threshold loosened for PASS.
- Under the Voronoi tessellation, frontier cells absorb masked pieces so they are
  typically NOT slivers; slivers can still arise only for near-grazing `W_max`
  alignments, handled by the admissibility + agglomeration above.

## 3. Boundary-control object (BLOCKER 3 repair)

Rev 0's ambiguity (imposing a W-face KKT on a node that can be strictly inside the
domain merely because its control volume touches W) is resolved by freezing a
coherent object:

**Frozen object: node value + cell-level constrained control.**

1. The HJB value `V_s` lives at the represented node `s` (source-faithful node-based
   structure).
2. The control at cell `s` is a **cell object**: the controlled drift
   `(mu_a, mu_b)_s(c,l,d)` that enters the face-flux rates `q_{s->r}(c,l,d)` of the
   control volume `C_s`. The control maximizes the DISCRETE Hamiltonian (Phase 8
   report), not the continuous gradient.
3. The W KKT (`mu_W <= 0`) is imposed on cell `s` **iff** `|F_s^W| > 0` (the control
   volume genuinely has a physical W segment). It is a cell-boundary condition, never
   a bare node-point condition, and never applied to a strictly interior cell.
4. **Convergence argument (cell shrinkage):** as `h = max(da,db) -> 0` at fixed
   aspect ratio, `diam(C_s) -> 0` (Voronoi cell shrinks to `s`) and a frontier cell's
   node `s` lies within `O(h)` of the W face, so the node converges to the boundary
   point; the cell tangent-cone condition converges to the continuous state-constraint
   at that point. For a strictly interior node whose cell does not touch W, no W KKT.
5. HJB and KFE consume the same control/flux object: the cell control determines the
   drift, which determines the same face-flux rates used for both `Q V` and `Q^T p`.

## 4. Refinement interpretation (frozen)

For `h -> 0` at fixed `da/db`: the Voronoi cells approximate `D_W` in Hausdorff sense;
the physical W segments converge to the line `a+b=W_max`; `omega_s -> da*db` for
interior cells and `O(h)`-scaled for frontier cells; the cell-tangent-cone condition
converges to the continuous state-constraint (Section 3.4). The tangential *drift*
consistency is NOT claimed here — see the tangential report (the tangent benchmark
fails for fixed aspect ratio; that object is the bounded unresolved design item).

## 5. Compliance

No control-volume implementation, no Voronoi computation, no execution. All objects
are symbolic/analytic definitions to be realized by a successor implementation
authority.
