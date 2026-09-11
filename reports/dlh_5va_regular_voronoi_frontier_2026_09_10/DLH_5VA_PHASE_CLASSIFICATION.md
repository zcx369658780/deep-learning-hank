# DLH-5V-A — Checkpoint B: Regular Frontier Phase Classification

**Issue:** deep-learning-hank #49 (DLH-5V-A) — `SCIENTIFIC_DESIGN__REGULAR_VORONOI_FRONTIER_PHASE_AND_ADJACENCY_CLASSIFICATION`
**Status:** CHECKPOINT B DERIVATION COMPLETE — `CHECKPOINT_ONLY__NOT_SCIENTIFIC_ACCEPTANCE` (explicit-stage commit; not a scientific-acceptance claim)
**Branch:** `dsh/issue-49-dlh-5va-voronoi-frontier-phase-adjacency-2026-09-10`
**Date:** 2026-09-10 (recovery run; recovery authority comment `5615451130`, original activation `5612995339`)
**Scope:** regular (non-endpoint, non-corner) W-frontier cells only. Endpoints/corners, moment cones, transition rates, face-flux moment maps, HJB/KFE, stationary objects, and numerical `W_max` are NOT analyzed here (forbidden or deferred — see §14).

---

## 0. Results at a glance

Let `kappa = 19·(W_max − b_min)`, `N = floor(kappa)`, `theta = kappa − N ∈ [0,1)`, and write the exact grid in
(j,i)-units with `a = (10/19)·x`, `b = b_min + (7/19)·y` (node `(j,i)` sits at `(x,y) = (j,i)`; metric
`d² ∝ 100·Δx² + 49·Δy²`). The represented-node set is `S = {(j,i) : j,i ≥ 0, 10j+7i ≤ N}` and the physical
W-frontier is the line `10x + 7y = N + theta` inside the domain triangle `{x ≥ 0, y ≥ 0, 10x+7y ≤ N+theta}`.

1. **Node set is θ-independent.** Because `10j+7i` is an integer, `10j+7i ≤ N+theta ⇔ 10j+7i ≤ N` for all
   `theta ∈ [0,1)`. θ moves only the frontier *line*; it never adds or removes represented nodes.
2. **Staircase.** The top node of column `j` is `(j, i_t(j))`, `i_t(j) = floor((N−10j)/7)`, with weight
   `w_j = 10j + 7·i_t(j) = N − r_j`, `r_j = (N − 10j) mod 7 = (N − 3j) mod 7 ∈ {0,…,6}`.
   Recurrence `r_{j+1} = (r_j − 3) mod 7`; **period 7**: `r_{j+7} = r_j`.
   Staircase drop `i_t(j) − i_t(j+1) = 2` iff `r_j ∈ {0,1,2}`, and `= 1` iff `r_j ∈ {3,4,5,6}`.
   Seven consecutive drops sum to 10 (exactly three 2-drops and four 1-drops per period).
3. **Regular W-active set (main theorem).** For a regular cell (top node with `j ≥ 1`, `i_t(j) ≥ 1`, plus cells
   below it in the same column, `i ≤ i_t(j)`):
   * (Type A) the staircase top node `(j, i_t(j))` is **always** W-active: `|F^W| > 0`;
   * (Type B) the node directly below the top, `(j, i_t(j) − 1)`, is W-active **iff `r_j ∈ {0,1,2}`**
     (equivalently iff the staircase drops by 2 to column `j+1`); the B-cell is *regular* iff additionally
     `i_t(j) ≥ 2` (for `i_t(j) = 1` the B-cell is the endpoint cell `(j,0)`, excluded);
   * every cell with `i ≤ i_t(j) − 2` has `|F^W| = 0`: its whole cell lies at weight
     `≤ N − r_j − 5.5 ≤ N − 5.5 < N + theta`, strictly below the frontier.
4. **Exact W-face endpoints** (j-units; `y` from `10x+7y = N+theta`), for a top cell with defect `r = r_j`:
   * left endpoint `L_A = j + (14r + 14θ − 149)/340` (intersection of the frontier with the always-binding
     NW-1 bisector, from node `(j−1, i_t+1)`);
   * right endpoint `R_A = j + (r + θ + 7/2)/10` at `y = i_t − 1/2` if `r ∈ {0,1,2}` (corner shared with the B-cell),
     or `R_A = j + (14r + 149 + 14θ)/340` (vertex shared with the next column's top cell) if `r ∈ {3,4,5,6}`;
   * B-cell (only `r ∈ {0,1,2}`): `L_B = R_A`, `R_B = j + (14r + 14θ + 247)/340` (vertex shared with the next
     column's top cell).
5. **Tiling.** The W-segments tile the regular frontier arc continuously: consecutive segments share exact
   vertices, proved by the identities `R_B ≡ L_{A,j+1}` (r ∈ {0,1,2}) and `R_A ≡ L_{A,j+1}` (r ∈ {3,4,5,6}).
   The regular W-segment count per full interior period is **7 A-segments + 3 B-segments = 10**.
6. **Periodic invariant & sufficiency.** The complete regular frontier phase structure is determined by
   **(N mod 7, θ)**: `N mod 7` fixes the discrete phase (the sequence `r_j`, hence types, order, and W-active set);
   θ enters only affinely in endpoint positions. No further invariant is needed; in particular the node-set is
   θ-independent and the discrete phase has **no structural phase break inside θ ∈ [0,1)**.
7. **Phase-break conditions (θ-thresholds).** For regular cells: none structural. All W-face lengths stay
   strictly positive on `[0,1)` (`B_r` length ≥ 68/340 > 0). The only metric degeneracy is the length tie
   `A_1 = A_{3..6}` at exactly **θ = 1/2** (both `= 149/170` in j-units). At `θ = 0` the frontier additionally
   passes through the weight-`N` top nodes (`r = 0` columns), i.e., it is lattice-carrying; for `θ ∈ (0,1)` it is
   lattice-free — this changes no cell's W-active status.
8. **Verification.** Every formula above was confirmed by exact-Fraction restricted-Voronoi computation on small
   instances: all seven `N mod 7` classes at `θ = 0` (`N = 70,…,76`), phases at `θ = 1/2` and `θ = 3/4`
   (`N = 70,71,73,76`), the endpoint-boundary case `N = 77`, and a two-period case `N = 105` (§13). Zero mismatches.

---

## 1. Setup, exact grid, and scaling

Accepted context (DLH-5U Rev 1, Route F): domain `D_W = {0 ≤ a ≤ a_max, b ≥ b_min, a+b ≤ W_max}`; represented
nodes `S = {s = (a_j, b_i) : a_j + b_i ≤ W_max}`; cells `C_s = {x ∈ D_W : ‖x−s‖ ≤ ‖x−r‖ ∀ r ∈ S}` partition `D_W`
a.e.; physical W-activity of a cell is `F^W_s = ∂C_s ∩ {a+b = W_max}` and counts only if `|F^W_s| > 0`.

Exact grid (frozen in DLH-5U Rev 1):

```
a_j = j·(10/19),   b_i = b_min + i·(7/19),   da = 10/19,   db = 7/19,   da/db = 10/7 .
kappa := 19·(W_max − b_min),   N := floor(kappa),   theta := kappa − N ∈ [0,1).
```

Change variables to (j,i)-units: `x := 19·(a − 0)/10 = 19a/10` (so node j sits at x = j) and
`y := 19·(b − b_min)/7`. Then:

```
node (j,i)  ⟺  (x,y) = (j,i);
domain     ⟺  x ≥ 0,  y ≥ 0,  10x + 7y ≤ N + theta;      (frontier line: 10x+7y = N+theta)
represented ⟺  10j + 7i ≤ kappa;                          (see §2 for the reduction)
metric     ⟺  d² = (10/19)²·Δx² + (7/19)²·Δy² ∝ 100·Δx² + 49·Δy² .
```

All geometry below is scale-equivalent to the physical one (uniform scaling by 19), so positivity of lengths and
the incidence structure are preserved exactly; conversions to physical units are given in §8.

## 2. Reduction of the represented-node inequality

`a_j + b_i ≤ W_max ⇔ 10j + 7i ≤ 19·(W_max − b_min) = kappa = N + theta`. Since `10j + 7i` is an integer and
`0 ≤ theta < 1`:

```
10j + 7i ≤ N + theta   ⇔   10j + 7i ≤ N .
```

**Consequence 1 (node-set invariance).** `S = {(j,i) : j,i ≥ 0, 10j+7i ≤ N}` depends only on `N`, not on θ.
**Consequence 2 (frontier position).** The frontier line `10x+7y = N+theta` moves continuously with θ inside
the slab `(N, N+1)` of constant-weight lines; it carries lattice nodes only when `theta = 0` (the weight-`N`
nodes), and carries no node for `theta ∈ (0,1)`.

This is the first reason (N mod 7, θ) can be the complete phase data: the *set* of cells is fixed by N, θ only
slides the frontier across them.

## 3. Bisector half-planes and the dual-cell structure

For nodes `s = (j,i)`, `r = (p,q)`, `d(x,s)² − d(x,r)² = 100[(x−j)²−(x−p)²] + 49[(y−i)²−(y−q)²]`, so the
half-plane of points closer to `s` than `r` is

```
H_{sr}:  200·(p−j)·x + 98·(q−i)·y  ≤  100·(p²−j²) + 49·(q²−i²) .        (bisector inequality)
```

Special cases used throughout (for `s = (j, i_t)`, weight `w = 10j + 7i_t = N − r`):

| neighbor node r | displacement (Δj,Δi) | binding half-plane (s-side) | represented? |
|---|---|---|---|
| (j−1, i_t)    | (−1, 0) | x ≥ j − 1/2                                   | always (weight w−10) |
| (j, i_t−1)    | (0, −1) | y ≥ i_t − 1/2                                  | always (weight w−7) |
| (j, i_t+1)    | (0, +1) | y ≤ i_t + 1/2                                  | **masked** (weight w+7 > N) |
| (j+1, i_t)    | (+1, 0) | x ≤ j + 1/2                                    | **masked** (weight w+10 > N) |
| (j−1, i_t+1)  | (−1, +1)| y ≤ (200x − 200j + 98·i_t + 149)/98   [NW-1]   | always (weight w−3) |
| (j+1, i_t−1)  | (+1, −1)| 200x − 98y ≤ 200j − 98·i_t + 149        [SE-1]   | iff r ∈ {3,4,5,6} (weight w+3) |
| (j+1, i_t−2)  | (+1, −2)| 200x − 196y ≤ 200j − 196·i_t + 296      [SE-2]   | always (weight w−4) |

The interior (non-frontier, non-axis) cells of the exact lattice are `da×db` rectangles bounded by the four
axis-aligned bisectors (diagonal bisectors are tangent at rectangle corners — zero-length faces). All
frontier-structure content of this checkpoint comes from the *masked* right/upper neighbors and from the
always-present NW-1 / SE-2 cuts above.

## 4. Staircase structure and periodicity

Define the staircase top of column j:

```
i_t(j) := floor((N − 10j)/7),   valid for 0 ≤ j ≤ floor(N/10);
r_j     := (N − 10j) mod 7 = N − (10j + 7·i_t(j)) = N − w_j ∈ {0,…,6} .
```

**Lemma 1 (recurrence).** `r_{j+1} = (r_j − 3) mod 7`; hence `r_{j+7} = r_j` (period 7). The staircase drop is

```
i_t(j) − i_t(j+1) = 1 + floor((r_j − 3)/7)   =   2 if r_j ∈ {0,1,2},   1 if r_j ∈ {3,4,5,6} .
```

Over any 7 consecutive columns the drops sum to 10 (one period advances the weight by 70 = 7·10), with exactly
three 2-drops and four 1-drops. Because `j ↦ −3j mod 7` is a bijection, every period contains each defect
`r ∈ {0,…,6}` exactly once; which columns carry which r is fixed by `N mod 7` (= r₀).

**Lemma 2 (periodicity of the phase).** `r_{j+7} = r_j` implies the *entire local configuration* of column j
(depending only on `r_j` and θ, see §§6–8) repeats with period 7 in j. The sequence `(r_0,…,r_6)` is the phase,
indexed by `N mod 7`.

## 5. Regular region

A node/cell is **regular** iff its cell is not clipped by the coordinate axes `x = 0` (a = 0) or `y = 0`
(b = b_min). For the staircase this is equivalent to `j ≥ 1` and `i_t(j) ≥ 1`; the B-cell (when it exists) is
regular iff additionally `i_t(j) ≥ 2`. The regular frontier arc is the arc of `10x+7y = N+theta` covered by
W-faces of regular cells; its ends (near the axes) are covered by endpoint cells and are **excluded** from this
checkpoint (see §14). Regularity does not depend on θ.

## 6. Local configuration of a regular staircase cell

Take `s = (j, i_t(j))`, `j ≥ 1`, `i_t(j) ≥ 1`, `r = r_j`. From §3 the competing nodes that can bound the
frontier-facing (NE) part of `C_s` are:

* **Left:** `x ≥ j − 1/2` from `(j−1, i_t)` — always binds (j ≥ 1).
* **Below:** `y ≥ i_t − 1/2` from `(j, i_t−1)` — always binds.
* **Upper-left:** NW-1 cut from `(j−1, i_t+1)` — always present (weight `w−3 ≤ N`). Note `(j−1, i_t+1)` is the
  staircase top of column j−1 when the drop there is 1, and is the B-cell of column j−1 when the drop is 2; in
  both cases it is represented, so **NW-1 always binds the left end of the W-face**.
* **Upper-right:** masked (`(j, i_t+1)`, `(j+1, i_t)`, and everything further NE has weight > N) — no cuts.
* **Lower-right:** `(j+1, i_t−1)` is represented iff `r ∈ {3,4,5,6}` (weight `w+3 ≤ N`), masked iff
  `r ∈ {0,1,2}`. `(j+1, i_t−2)` is always represented but its cut crosses the frontier strictly to the right of
  every possible W-face right endpoint (§8), so it never binds the W-face for regular cells; deeper SE nodes are
  further away still.
* **NW-2** `(j−1, i_t+2)` (represented iff r ∈ {4,5,6}) crosses the frontier at
  `x = j − 98·i_t/340 + (14r+14θ−296)/340 ≤ j − 0.87 < j − 1/2` for `i_t ≥ 1`, i.e., left of the cell — never
  binds for regular cells.

**Result:** for every regular top cell the frontier-facing boundary is determined by exactly three constraints —
the left cut `x = j − 1/2`, the bottom cut `y = i_t − 1/2`, and either NW-1 (left end) plus one right-end
constraint (SE-1 if present, else the bottom cut) — together with the frontier line itself. This is the complete
local census; no other node can cut the regular W-face.

## 7. Main theorem: regular cells with |F^W_s| > 0

**Theorem 1.** Let `j ≥ 1`, `i_t(j) ≥ 1`, `r = r_j`, and `i ≤ i_t(j)`.

1. (Type A) `(j, i_t(j))` is W-active for every `r ∈ {0,…,6}`: `|F^W| > 0` for all `θ ∈ [0,1)`.
2. (Type B) `(j, i_t(j) − 1)` is W-active iff `r ∈ {0,1,2}`; when `i_t(j) = 1` it is the endpoint cell `(j,0)`
   and falls outside the regular analysis.
3. `i ≤ i_t(j) − 2` implies `|F^W| = 0`.

*Proof of (3).* For `i ≤ i_t − 2` the four axial neighbors are all represented, so
`C_{(j,i)} ⊆ [j−1/2, j+1/2] × [i−1/2, i+1/2]`. Every point of the cell therefore has
`10x + 7y ≤ 10(j+1/2) + 7(i+1/2) ≤ 10j + 7(i_t−2) + 8.5 = N − r − 5.5 ≤ N − 5.5 < N + θ`; the cell is strictly
inside the open half-plane below the frontier, so it cannot touch `10x+7y = N+θ`. ∎

*Proof of (2).* The cell of `s' = (j, i_t−1)` is bounded above by `y ≤ i_t − 1/2` (bisector with the top node
`(j, i_t)`), so any frontier point of `C_{s'}` must have `x ≥ (N+θ − 7(i_t−1/2))/10 = j + (r+θ+7/2)/10`.
If `r ∈ {3,4,5,6}` then `(j+1, i_t−1)` is represented and cuts `x ≤ j + 1/2`, while
`j + (r+θ+7/2)/10 ≥ j + 0.65 > j + 1/2` — impossible, so no frontier point: `|F^W| = 0`.
If `r ∈ {0,1,2}` then `(j+1, i_t−1)` is masked; the right bound is the SE-1′ cut from `(j+1, i_t−2)` (always
represented), which meets the frontier at `x = j + (14r+14θ+247)/340` (computed in §8). The frontier arc
`x ∈ [j + (r+θ+7/2)/10, j + (14r+14θ+247)/340]` lies in `C_{s'}` (it satisfies the bottom cut
`y ≥ i_t − 3/2`, the left cut `x ≥ j − 1/2`, the NW-1′ and SE-2′ cuts, checked in §8) and has positive length
`(128 − 20r − 20θ)/340 ≥ 68/340 > 0`. Hence W-active. ∎

*Proof of (1).* For the top cell `s = (j, i_t)`: the NW-1 cut meets the frontier at `x_L = j + (14r+14θ−149)/340`
(§8), and `x_L > j − 1/2` for all `r,θ`; the right endpoint `x_R` (§8) satisfies `x_R − x_L > 0` for all `r,θ`.
The whole open frontier arc `(x_L, x_R)` is on the s-side of every cut of §6 (by convexity, verified at all
binding constraints), so `F^W_s` is a positive-length segment. ∎

**Corollary (count).** Per full interior period (all 7 columns regular): 7 top cells + 3 B-cells = **10 regular
W-active cells**; equivalently 10 W-segments tiling the regular frontier arc.

## 8. Exact W-face endpoints and segment lengths

All intersections are with the frontier `y = (N+θ−10x)/7`; `N = 10j + 7i_t + r` is used throughout.

**Top cell (Type A), left endpoint — NW-1 cut ∩ frontier.**
`y ≤ (200x − 200j + 98i_t + 149)/98` on the frontier gives `14(N+θ−10x) ≤ 200x − 200j + 98i_t + 149`, i.e.
`340x ≥ 340j + 14r + 14θ − 149`:

```
L_A(r,θ) :  x = j + (14r + 14θ − 149)/340 .
```

(`x_L ≥ j − 149/340 > j − 1/2`; the frontier point lies above the bottom cut since
`y = i_t + (20r+20θ+149)/238 > i_t − 1/2`.)

**Top cell, right endpoint.**

* `r ∈ {0,1,2}`: `(j+1, i_t−1)` is masked, so the frontier leaves the cell where it meets the bottom cut
  `y = i_t − 1/2`:

```
R_A(r,θ) :  x = j + (r + θ + 7/2)/10,   y = i_t − 1/2 .        (corner shared with the B-cell)
```

* `r ∈ {3,4,5,6}`: SE-1 cut ∩ frontier, `200x − 98y ≤ 200j − 98i_t + 149` on the frontier gives
  `340x ≤ 340j + 14r + 14θ + 149`:

```
R_A(r,θ) :  x = j + (14r + 149 + 14θ)/340 .                  (vertex shared with the next top cell)
```

**B-cell (Type B; exists iff r ∈ {0,1,2}).** Left endpoint is the shared corner `L_B = R_A` above. Right endpoint:
SE-1′ cut from `(j+1, i_t−2)` (`200x − 98y ≤ 200j − 98i_t + 247`) ∩ frontier:

```
R_B(r,θ) :  x = j + (14r + 14θ + 247)/340 .
```

**W-segment lengths** (j-units, Δx along the frontier; physical factor in §below):

```
A_r, r ∈ {0,1,2}:  Δx = (20r + 20θ + 268)/340   ∈ ((268+20r)/340, (288+20r)/340)
A_r, r ∈ {3,4,5,6}: Δx = 298/340 = 149/170      (constant, θ-independent)
B_r, r ∈ {0,1,2}:  Δx = (128 − 20r − 20θ)/340   ∈ ((108−20r)/340, (128−20r)/340)
```

All lengths are strictly positive for `θ ∈ [0,1)`; the smallest is `B_2` at `θ → 1`: `68/340 = 0.2`.
**Physical length** of a W-segment with j-unit span Δx (frontier direction `(Δx, Δy) = (Δx, −10Δx/7)`):
`|F^W|_phys = (10√2/19)·Δx`. E.g. `A_{3..6}`: `(10√2/19)(149/170) = 149√2/323 ≈ 0.6524`; `B_0` at θ=0:
`(10√2/19)(32/85) ≈ 0.2802` (units of `a`).

## 9. Frontier tiling identities

Let `r' = r_{j+1} = (r−3) mod 7`. Two exact identities make the W-segments tile the frontier continuously.

* If `r ∈ {0,1,2}` (drop 2): `r' = r+4` and
  `R_B = j + (14r+14θ+247)/340 = j + 1 + (14r' + 14θ − 149)/340 = L_{A,j+1}`.
* If `r ∈ {3,4,5,6}` (drop 1): `r' = r−3` and
  `R_A = j + (14r+149+14θ)/340 = j + 1 + (14r' + 14θ − 149)/340 = L_{A,j+1}`.

So along the regular frontier arc the segments appear in column order, each column contributing its A-segment and
(iff `r ∈ {0,1,2}`) its B-segment, with every consecutive pair sharing an exact vertex. Together with the
partition theorem (DLH-5U Rev 1) and Theorem 1(3) (no other regular cell touches the frontier), the regular arc
is covered exactly once. The observed neighbor displacement sets (preview; full classification is Checkpoint C)
are consistent: A-cells of drop-1 columns show `(−1,0), (−1,1), (0,−1), (1,−1)`; A-cells of drop-2 columns show
`(−1,0), (−1,1), (0,−1)`; B-cells show `(−1,0), (0,−1), (0,1), (1,−1)`.

## 10. Phase classification: the seven sectors

The phase is the period-7 sequence `(r_0,…,r_6) = (m, m−3, m−6, …, m−18) mod 7`, `m = N mod 7`. Table:
`B-columns` lists the column offsets within a period whose top cell has `r ∈ {0,1,2}` (i.e., that carry a B-cell
when `i_t ≥ 2`); `drops` is the drop pattern `(i_t(0)−i_t(1), …, i_t(6)−i_t(7))`.

| m = N mod 7 | r sequence (r₀…r₆)          | drops            | B-columns (mod 7) |
|---|---|---|---|
| 0 | (0,4,1,5,2,6,3) | (2,1,2,1,2,1,1) | 0, 2, 4 |
| 1 | (1,5,2,6,3,0,4) | (2,1,2,1,1,2,1) | 0, 2, 5 |
| 2 | (2,6,3,0,4,1,5) | (2,1,1,2,1,2,1) | 0, 3, 5 |
| 3 | (3,0,4,1,5,2,6) | (1,2,1,2,1,2,1) | 1, 3, 5 |
| 4 | (4,1,5,2,6,3,0) | (1,2,1,2,1,1,2) | 1, 3, 6 |
| 5 | (5,2,6,3,0,4,1) | (1,2,1,1,2,1,2) | 1, 4, 6 |
| 6 | (6,3,0,4,1,5,2) | (1,1,2,1,2,1,2) | 2, 4, 6 |

(All seven rows verified against exact computation, §13.) The `B ≡ 0 (mod 7)` columns are adjacent to the
`j = 0` endpoint and are excluded from the regular analysis together with it.

**Sufficiency theorem.** The complete regular frontier phase structure — W-active set, per-column type (A or
A+B), W-face endpoints, segment lengths, and tiling order — is an explicit function of `(r_j, θ)` with
`r_j = (N − 3j) mod 7`; hence it is fully determined by `(N mod 7, θ)`. Conversely, `N mod 7` alone fixes the
discrete phase (the W-active set and the type order), and θ alone fixes the continuous position of the frontier.
No other invariant (e.g. `N mod 10`, `floor(N/7)`, θ's fractional class) enters the regular structure.

## 11. Phase-break conditions (θ-thresholds)

1. **No structural phase break in θ ∈ [0,1).** The W-active set, cell types, binding half-planes (§6), tiling
   order, and length *orderings within each type family* are constant on the whole interval: every W-face length
   is affine in θ with strictly positive minimum (`B_2`: 68/340 > 0), and the B-cell existence condition
   (`r ∈ {0,1,2}`) is θ-free. Hence the discrete phase is constant; the only θ-effect is affine sliding of the
   segment endpoints.
2. **Metric degeneracy at θ = 1/2.** `A_1` length `= (288+20θ)/340` equals the common length `298/340` of
   `A_{3..6}` exactly at `θ = 1/2` (ties, not a phase change; rankings elsewhere: `B_0 > B_1 > B_2`,
   `A_0 < A_{3..6}`, `A_2 > A_{3..6}`, all θ-independent; `A_1 ≷ A_{3..6}` according as `θ ≷ 1/2`).
3. **θ = 0 lattice-carrying.** At θ = 0 the frontier passes through the top nodes of `r = 0` columns (weight
   exactly N); those nodes lie *inside their own W-face* (`x_L < j < x_R`). For θ ∈ (0,1) the frontier is
   lattice-free. No W-active status changes at this boundary (it is already covered by the θ ∈ [0,1) uniformity).
4. **Discrete sector boundaries.** The only "phase breaks" in the discrete sense occur between the seven
   sectors, i.e. at integer shifts of N (change of `N mod 7`), which permute the r-sequence and the B-column
   positions per the table in §10.

## 12. Recurring regular frontier-node types

The finite type system (each regular W-active cell falls into exactly one):

* **Type A^F** (top cell, drop-1 columns, `r ∈ {3,4,5,6}`): W-face = frontier arc between the NW-1 and SE-1
  vertices; constant length 149/170 (j-units); neighbors (preview): left, NW(−1,1), below, SE(1,−1).
* **Type A^L** (top cell, drop-2 columns, `r ∈ {0,1,2}`): W-face = frontier arc between the NW-1 vertex and the
  bottom-edge corner shared with its B-cell; length (20r+20θ+268)/340; neighbors (preview): left, NW(−1,1),
  below (the B-cell); its SE side is open (the SE-1 node is masked).
* **Type B** (sub-top cell, exists iff `r ∈ {0,1,2}`): W-face = frontier arc between the shared corner and the
  next top cell's left vertex; length (128−20r−20θ)/340; neighbors (preview): left, below, above (the A^L
  cell), SE(1,−1) (the node `(j+1, i_t−2)`).

Per period (all columns regular): 4 × A^F + 3 × A^L + 3 × B = 10 cells. Adjacency *classification* (including
displacement vectors, axial/diagonal/oblique/longer neighbors created by masked nodes) is Checkpoint C.

## 13. Verification log (exact arithmetic)

All runs used the exact-Fraction restricted-Voronoi verifier (temp scratch tool; node mask `10j+7i ≤ N`, exact
Sutherland–Hodgman clipping, exact shared-face detection). For every run below, the computed regular W-active
set and the computed W-face endpoints matched the formulas of §§7–8 *exactly* (zero mismatches):

| N | θ | N mod 7 | regular W-active | W-segment endpoints checked |
|---|---|---|---|---|
| 70 | 0, 1/2 | 0 | 6 A + 2 B = 8 | all 16 endpoints |
| 71 | 0, 3/4 | 1 | 6 A + 2 B = 8 | all 16 endpoints |
| 72 | 0 | 2 | 6 A + 2 B = 8 | all 16 endpoints |
| 73 | 0, 1/2 | 3 | 6 A + 3 B = 9 | all 18 endpoints |
| 74 | 0 | 4 | 6 A + 3 B = 9 | all 18 endpoints |
| 75 | 0 | 5 | 6 A + 3 B = 9 | all 18 endpoints |
| 76 | 0, 1/2 | 6 | 6 A + 3 B = 9 | all 18 endpoints |
| 77 | 0 | 0 | 7 A + 2 B = 9 (B at j=7 is endpoint cell (7,0), excluded) | all |
| 105 | 0 | 0 | 9 A + 4 B = 13 (two periods; col 8 = col 1 + 7, col 9 = col 2 + 7) | all |

The `N = 77` row confirms the B-cell regularity boundary `i_t(j) ≥ 2`: at `j = 7` (`r = 0`, `i_t = 1`) the B-cell
is the endpoint cell `(7,0)`, reported by the verifier as endpoint-touching W-active, not regular. The
`N = 105` row confirms period-7 replication across more than one period.

## 14. Out of scope / deferred / forbidden

* **Not analyzed (explicitly out of Checkpoint B scope):** endpoint/corner cells (`j = 0`, `i = 0` boundary
  cells, the two ends of the regular frontier arc), the θ-behavior of endpoint cells, and the full adjacency
  classification (deferred to Checkpoint C: `DLH_5VA_VORONOI_ADJACENCY_AND_DISPLACEMENTS.md`).
* **Forbidden (per Issue #49):** moment cones, (−1,+1) feasibility, transition rates, face-flux moment maps,
  endpoint/corner transitions, HJB/KFE, stationary objects, numerical `W_max` (this document uses only the
  symbolic `kappa = N + θ`), and any mutation of the accepted household source.
* **No source files were modified**; only allowlist report files were created (§15).

## 15. Checkpoint B acceptance checklist

| Item | State |
|---|---|
| Derived the regular frontier structure symbolically from `10j + 7i ≤ N + theta` | DONE (§§2–9) |
| Periodic invariant(s) | DONE: period 7 in j; `r_j ≡ (N−3j) mod 7`; discrete phase = N mod 7 (§4, §10) |
| Sufficiency of (N mod 7, θ) | DONE: proven & explicit (§10) |
| Exact phase-break conditions | DONE: no structural break in θ ∈ [0,1); tie at θ = 1/2; sectors by N mod 7 (§11) |
| Recurring regular frontier-node types | DONE: A^F, A^L, B (§12) |
| Regular cells with \|F^W_s\| > 0 | DONE: Theorem 1 (§7) |
| Endpoints/corners excluded | DONE (not analyzed) |
| Exact spot-check verification | DONE (§13), zero mismatches |
| Allowlist-only writes, no source mutation | DONE |
| Commit marked `CHECKPOINT_ONLY__NOT_SCIENTIFIC_ACCEPTANCE` | DONE (with this report) |

*This is an explicit-stage checkpoint commit, not a scientific-acceptance claim; acceptance remains with the
Issue #49 authority (GitHub Issue = sole DSH Builder authority; ChatGPT = independent reviewer).*
