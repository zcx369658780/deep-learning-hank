# DLH-5V-A — Checkpoint C: Restricted-Voronoi Shared-Face Adjacency and Displacements

**Issue:** deep-learning-hank #49 (DLH-5V-A) — `SCIENTIFIC_DESIGN__REGULAR_VORONOI_FRONTIER_PHASE_AND_ADJACENCY_CLASSIFICATION`
**Status:** CHECKPOINT C DERIVATION COMPLETE — `CHECKPOINT_ONLY__NOT_SCIENTIFIC_ACCEPTANCE` (explicit-stage commit; not a scientific-acceptance claim)
**Branch:** `dsh/issue-49-dlh-5va-voronoi-frontier-phase-adjacency-2026-09-10`
**Depends on:** Checkpoint B (phase classification, already committed/pushed) — uses the same exact coordinates, cell-type system (A^F, A^L, B), and the defect variable `r_j = (N − 10j) mod 7`.
**Scope:** actual restricted-Voronoi **shared-face adjacency** of regular cells only (j ≥ 1, i ≥ 1, i ≤ i_t(j)). Endpoint/corner cells excluded. No rates, no moment cones, no HJB/KFE — see §9.

---

## 0. Results at a glance

A **neighbor** of cell `s` is a represented node `r ≠ s` such that the bisector half-plane boundary cuts a
**positive-length** shared segment `C_s ∩ C_r` (equivalently, `H_{sr} ∩ ∂C_s` is a non-degenerate segment).
Zero-length corner contacts (full-lattice diagonal tangencies) are NOT neighbors; the W-frontier face is a
domain-boundary face, not a cell neighbor.

For a regular cell the complete neighbor-displacement census is:

| cell type (condition) | N_V(s) | neighbor displacements (Δj, Δi) | kind |
|---|---|---|---|
| INT — `i ≤ i_t(j) − 2` | 4 | (−1,0), (0,−1), (0,1), (1,0) | 4 axial (full-lattice dual rectangle) |
| A^F — top, `r ∈ {3,4,5,6}` | 4 | (−1,0), (0,−1), (−1,1), (1,−1) | 2 axial + 2 diagonal |
| A^L — top, `r ∈ {0,1,2}` | **3** | (−1,0), (0,−1), (−1,1) | 2 axial + 1 diagonal (SE side open) |
| B — `r ∈ {0,1,2}` (W-active sub-top) | 4 | (−1,0), (0,−1), (0,1), (1,−1) | 3 axial + 1 diagonal |
| B — `r ∈ {3,4,5,6}` (plain rectangle) | 4 | (−1,0), (0,−1), (0,1), (1,0) | 4 axial |

Facts established in this checkpoint:

1. **No oblique or longer neighbors exist for regular cells.** Every neighbor displacement satisfies
   `max(|Δj|, |Δi|) = 1`; the only non-axial displacement pairs are the diagonals `(−1,+1)` (NW) and
   `(+1,−1)` (SE). (Full candidate census, §6.)
2. **The only masked-node-created adjacencies are diagonal:** NW `(−1,1)` on A-cells and SE `(1,−1)` on A^F- and
   B-cells. In the full lattice these pairs meet only at rectangle corners (zero length); they acquire positive
   length here precisely because the axial node `(j, i_t+1)` (above) and/or `(j+1, i_t)` (right) are masked and
   the frontier opens the cells. All other adjacencies (axial, and the B↔A^L, B↔(j+1,i_t−2) faces) exist also in
   the full lattice.
3. **θ-independence.** The neighbor sets are identical for all `θ ∈ [0,1)` (verified at θ = 0, 1/2, 3/4). θ
   moves only the exact vertex positions of the diagonal and W-faces.
4. **A^L is the unique low-valence type** (N_V = 3): its SE node `(j+1, i_t−1)` and right node `(j+1, i_t)` are
   both masked, and its below-neighbor is its own B-cell.
5. Displacement vectors in physical units (see §5): axial `(±10/19, 0)`, `(0, ±7/19)`; diagonals
   `(−10/19, +7/19)`, `(+10/19, −7/19)`.

---

## 1. Setup and neighbor criterion

Same exact coordinates as Checkpoint B: node `(j,i)` at `(x,y) = (j,i)`, `a = (10/19)x`, `b = b_min + (7/19)y`,
metric `d² ∝ 100Δx² + 49Δy²`, domain `{x ≥ 0, y ≥ 0, 10x + 7y ≤ N + θ}`, represented nodes `10j + 7i ≤ N`,
frontier `10x + 7y = N + θ`, staircase top `i_t(j) = floor((N−10j)/7)`, defect `r = r_j = (N−10j) mod 7`.

**Neighbor test (exact).** `r` is a neighbor of `s` iff `C_s ∩ H_{s|r}` — the clip of `C_s` by the bisector
half-plane of points closer to `r` — is a non-degenerate segment (positive length). Using the bisector inequality
`200(p−j)x + 98(q−i)y ≤ 100(p²−j²) + 49(q²−i²)`, this is computed exactly (scratch verifier; no numerics).

## 2. Interior regular cells (INT): the full-lattice dual rectangle

For `i ≤ i_t(j) − 2` all four axial nodes `(j±1, i)`, `(j, i±1)` are represented (weights `w±10, w±7 ≤ N`), and
every diagonal node `(j±1, i±1)` is either masked (weight `w ± 17 > N`) or tangent at the rectangle corner
(`Δ = (±1,±1)`: bisector passes exactly through `(j±1/2, i±1/2)`; e.g. `200x + 98y ≤ 200j + 98i + 149` at
`(j+1/2, i+1/2)` gives equality). Hence `C_s = [j−1/2, j+1/2] × [i−1/2, i+1/2]` with exactly the four axial
shared faces — the full-lattice dual. `N_V = 4`, displacements `{(−1,0), (0,−1), (0,1), (1,0)}`.

## 3. Top cells (Type A)

`s = (j, i_t)`, `w = N − r`. Masked nodes: `(j, i_t+1)` (w+7), `(j+1, i_t)` (w+10) — so the right and above
faces of the full lattice are absent (the cell opens toward the frontier). Present cuts and their faces:

* **Left face** with `(j−1, i_t)`: `x = j − 1/2`, `y ∈ [i_t − 1/2, i_t + 1/2]` — axial, positive length.
* **Below face** with `(j, i_t−1)`: `y = i_t − 1/2`.
  * if `r ∈ {0,1,2}` the below node is the W-active **B-cell**: shared face `x ∈ [j − 1/2, j + (r+θ+7/2)/10]`
    (truncated at the W-face corner `P_right`);
  * if `r ∈ {3,4,5,6}` the below node is a plain rectangle: shared face `x ∈ [j − 1/2, j + 1/2]`.
* **NW diagonal face** (masked-node-created) with `(j−1, i_t+1)` — the NW-1 bisector
  `−200x + 98y = −200j + 98i_t + 149`: segment from `(j − 1/2, i_t + 1/2)` to `(x_L, y_L)` on the frontier,
  `x_L = j + (14r + 14θ − 149)/340` (Checkpoint B). Positive length for all `r,θ` since `x_L > j − 1/2`.
  `(j−1, i_t+1)` is represented for every `r` (weight `w−3 ≤ N`), and is the previous column's top cell (drop 1)
  or B-cell (drop 2).
* **SE diagonal face** (masked-node-created) with `(j+1, i_t−1)` — the SE-1 bisector
  `200x − 98y = 200j − 98i_t + 149` — **exists iff `r ∈ {3,4,5,6}`** (that node is represented exactly then):
  segment from `(j + 1/2, i_t − 1/2)` to `(x_R, y_R)`, `x_R = j + (14r + 149 + 14θ)/340`. Positive length.
  For `r ∈ {0,1,2}` the node `(j+1, i_t−1)` is masked (weight `w+3 > N`), so the SE side is **open** (its W-face
  region is covered by the B-cell and the next column); the node `(j+1, i_t−2)` is represented but its bisector
  meets the frontier strictly to the right of the W-face (Checkpoint B §6), so it contributes no face to the top
  cell.

Hence `A^F` (`r ∈ {3,4,5,6}`): N_V = 4 `{(−1,0), (0,−1), (−1,1), (1,−1)}`; `A^L` (`r ∈ {0,1,2}`): N_V = 3
`{(−1,0), (0,−1), (−1,1)}`.

## 4. Sub-top cells (Type B)

`s' = (j, i_t − 1)`, weight `w − 7 = N − r − 7`.

* **`r ∈ {0,1,2}` (W-active B).** `(j+1, i_t−1)` is masked. Faces:
  * left, with `(j−1, i_t−1)`: `x = j − 1/2`, `y ∈ [i_t − 3/2, i_t − 1/2]` (both rectangles) — axial;
  * below, with `(j, i_t−2)`: `y = i_t − 3/2`, `x ∈ [j − 1/2, j + 1/2]` — axial;
  * above, with the top cell `(j, i_t)`: `y = i_t − 1/2`, `x ∈ [j − 1/2, j + (r+θ+7/2)/10]` — axial, the
    A^L↔B shared face (truncated by the frontier at `P_right`);
  * SE diagonal (masked-node-created) with `(j+1, i_t−2)` — the SE-1′ bisector
    `200x − 98y = 200j − 98i_t + 247`: segment from `(j + 1/2, i_t − 3/2)` to `(R_B, y_{R_B})`,
    `R_B = j + (14r + 14θ + 247)/340` (Checkpoint B). Positive length.
  N_V = 4 `{(−1,0), (0,−1), (0,1), (1,−1)}`.
* **`r ∈ {3,4,5,6}` (plain rectangle).** `(j+1, i_t−1)` is represented; all four axial nodes are represented and
  all diagonal contacts are corner-tangent (the SE-1′ node `(j+1, i_t−2)`'s bisector is tangent at
  `(j+1/2, i_t−3/2)`; the NW-1 node `(j−1, i_t)`'s bisector is tangent at `(j−1/2, i_t−1/2)`). Hence the full
  dual rectangle, N_V = 4 `{(−1,0), (0,−1), (0,1), (1,0)}`, not W-active.

## 5. Displacement vectors

Physical displacement from `s` to neighbor `r` is `Δx_{sr} = (a_r − a_s, b_r − b_s) = ((10/19)·Δj, (7/19)·Δi)`:

| family | (Δj, Δi) | Δx_{sr} (physical) | |Δx| (physical) |
|---|---|---|---|---|
| axial left  | (−1, 0) | (−10/19, 0) | 10/19 ≈ 0.5263 |
| axial right | (+1, 0) | (+10/19, 0) | 10/19 |
| axial below | (0, −1) | (0, −7/19) | 7/19 ≈ 0.3684 |
| axial above | (0, +1) | (0, +7/19) | 7/19 |
| diagonal NW | (−1, +1) | (−10/19, +7/19) | √(10²+7²)/19 = √149/19 ≈ 0.6425 |
| diagonal SE | (+1, −1) | (+10/19, −7/19) | √149/19 |

`N_V(s) ∈ {3, 4}` for regular cells (`3` only for A^L; all others 4). These are the exact physical vectors of the
shared-face geometry; they are the input data of any future face-adapted flux assembly (design deferred — §9).

## 6. Why no oblique or longer neighbors exist (candidate census)

Take a regular cell `s = (j, i)`, `i ≤ i_t(j)`, and any represented `r = (j′, i′)` with `max(|j′−j|, |i′−i|) ≥ 2`.
Such a node lies outside the "first ring"; its weight is `w_r ≤ N`. Enumerate the closest such candidates and
their bisector frontier-crossing abscissas (all computed exactly in Checkpoint B §6/§8):

* `(j+2, i_t−2)` (right, two columns over; represented iff `r ≥ 6`): bisector meets the frontier at
  `x = j + (56(r+θ) + 596)/960 ≥ j + 0.62`, strictly right of every A-cell W-face right endpoint
  (`≤ j + 0.75` for `r ≤ 2`; `≤ j + 0.685` for `r ≥ 3`); for the B-cell the relevant node is `(j+2, i_t−2)` with
  crossing at `x = j + (14r + 14θ + 547)/540 ≥ j + 1.01 > R_B`.
* `(j−1, i_t+2)` (NW-2; represented iff `r ∈ {4,5,6}`): frontier crossing at
  `x ≤ j − 0.87 < j − 1/2` (left of the cell), and the bisector passes above the cell; never a face.
* Any node with `i′ ≤ i_t − 3` is at least two rows below: its bisector with `s` meets the frontier strictly
  right of the cell (same computation as SE-2 / SE-2′, shifted by one row), and inside the regular region it is
  separated from the frontier by the represented nodes of rows `i_t−1, i_t−2`.
* Nodes with `i′ ≥ i_t + 2` have weight `≥ w − 10 + 14 = w + 4` (for Δj ≥ 0) and are masked, or (Δj < 0) meet
  the frontier left of the cell (NW-2 family).

Hence every bisector of a node outside the first ring either lies outside the cell or crosses the frontier beyond
the cell's W-face; no positive-length face is formed. All observed regular neighbor displacements are in the
5-element set of §5, with `max(|Δj|, |Δi|) = 1`. (Verified exhaustively by the exact census, §8.)

## 7. Masked-node-created (restricted-only) adjacencies

The full-lattice dual of `(j, i_t)` would be the 4 axial rectangle. In the restricted tessellation:

* **Created (positive-length where full-lattice has corner-tangency or nothing):**
  * NW face `(−1,1)` on A-cells — appears because `(j, i_t+1)` is masked, so the NW bisector no longer
    degenerates at the rectangle corner; it is cut by the frontier into a positive segment.
  * SE face `(1,−1)` on A^F-cells — `(j+1, i_t)` masked; the SE-1 node is represented (r ≥ 3).
  * SE face `(1,−1)` on B-cells — `(j+1, i_t−1)` masked; the SE-1′ node `(j+1, i_t−2)` is represented.
* **Lost vs. full lattice:** the axial right neighbor `(j+1, i_t)` and axial above `(j, i_t+1)` of every top cell
  are masked (not represented), so top cells have no right/above axial neighbor; A^L additionally loses the
  diagonal SE (its SE-1 node is masked) — the unique N_V = 3 cell.
* The B↔A^L and B↔`(j+1, i_t−2)` faces exist in the full lattice as well (their endpoints are truncated by the
  frontier, but the faces are positive in both).

## 8. Verification log (exact arithmetic)

Exact restricted-Voronoi census (scratch verifier: exact clipping, exact shared-face test) of **all** regular
cells — W-active and INT — for the following cases; every cell's neighbor displacement set matched §2–§4
exactly (zero mismatches; the type-pattern table reproduced with the exact predicted displacement sets):

| N | θ | regular cells | observed types and N_V |
|---|---|---|---|
| 70 | 0 | 27 | 16 INT(4) + 4 A^F(4) + 2 A^L(3) + 2 B-active(4) + 3 B-inactive(4) |
| 73 | 0 | 30 | 19 INT + 4 A^F + 3 A^L + 3 B-active + 1 B-inactive |
| 77 | 0 | 34 | 21 INT + 4 A^F + 3 A^L + 2 B-active + 4 B-inactive (+ endpoint neighbor of last A^L, excluded) |
| 105 | 0 | 81 | 49 INT + 5 A^F + 4 A^L + 4 B-active + ... (two periods; col 8 = col 1 + 7) |
| 70,73,76 | 1/2 | — | W-active neighbor sets identical to θ = 0 |
| 71 | 3/4 | — | W-active neighbor sets identical to θ = 0 |

Counts reconcile: A^L count per period = 3 (drop-2 columns), B-active = 3, A^F = 4, B-inactive = 4; the census
rows confirm each. The `N = 77` case also confirms the last regular A^L cell's `(0,−1)` neighbor is the endpoint
cell `(j,0)` (neighbor set still valid; the endpoint cell itself is not classified here).

## 9. Out of scope / deferred / forbidden

* **Deferred:** endpoint/corner cell adjacency (both axes), and the umbrella design doc update (done with this
  checkpoint — see `docs/design/DLH_5VA_REGULAR_VORONOI_FRONTIER_PHASE_AND_ADJACENCY.md`).
* **Forbidden (Issue #49):** moment cones; (−1,+1) feasibility; transition rates; face-flux moment maps;
  endpoint/corner transitions; HJB/KFE; stationary objects; numerical `W_max`; source mutation. This report
  records only the exact shared-face geometry (neighbors, displacements, N_V) and makes no rate/flux design
  choices.
* **Allowlist-only writes** — this report and the umbrella design doc are the only files created in this
  checkpoint commit; no existing tracked file modified.

## 10. Checkpoint C acceptance checklist

| Item | State |
|---|---|
| Actual restricted-Voronoi shared-face adjacency derived from bisector inequalities | DONE (§§2–4,6) |
| N_V(s) recorded per type | DONE (§0, §§2–4) |
| Every Δx_{sr} = (a_r − a_s, b_r − b_s) recorded | DONE (§5) |
| Axial / diagonal / oblique / longer classification | DONE: only axial + diagonal; no oblique/longer (§6) |
| Masked-node-created adjacencies identified | DONE (§7) |
| Exact spot-check verification | DONE (§8), zero mismatches |
| θ-dependence | DONE: sets θ-independent; θ moves only vertices (§0) |
| Endpoints/corners excluded | DONE |
| Umbrella design doc updated | DONE (companion file) |
| Commit marked `CHECKPOINT_ONLY__NOT_SCIENTIFIC_ACCEPTANCE` | DONE (with this report) |

*Explicit-stage checkpoint commit, not scientific acceptance; acceptance remains with the Issue #49 authority.*
