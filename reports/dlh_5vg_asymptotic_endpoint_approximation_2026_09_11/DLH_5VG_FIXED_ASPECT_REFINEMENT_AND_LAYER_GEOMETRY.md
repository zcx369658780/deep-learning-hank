# DLH-5V-G — Fixed-Aspect Refinement Family and Layer Geometry (Rev 1)

**Design only.** Symbolic family, scaling identities, endpoint-layer geometry, structural facts (with exact
floor/ceiling proofs), corrected interior-layer/corner taxonomy, and the W-active lower-b disappearance fact for
`W_max > 8`. All statements analytic in `m`; tiny exact `%TEMP%` spot-checks reported as supplementary only.

## 1. The refinement family (Issue §4, frozen)

```text
m = 1, 2, 3, ...
da_m = 10/(19m),  db_m = 7/(19m)
a_j^(m) = j*10/(19m),            j = 0, ..., 19m
b_i^(m) = b_min + i*7/(19m),     i >= 0,  b_min = -2
N_m = floor(19m*(W_max - b_min))
represented nodes: 10j + 7i <= N_m
```

`m = 1` is the accepted native grid. Regime I: `W_max >= 8` (`kappa_1 = 19(W_max+2) >= 190`, `N_m >= 190m`).

## 2. Scaling identities

`kappa_m = 19m(W_max - b_min) = m*kappa_1 = N_m + theta_m`, `N_m = m*N_1 + floor(m*theta_1)`, `theta_m = {m theta_1}`.
Level-1 node `(j,i)` corresponds to level-`m` node `(mj, mi)`. Native same-W displacements satisfy `10 Delta j + 7 Delta i
= 0`; primitive same-W moves are `(-7,+10)` (forward) and `(+7,-10)` (mirror).

Physical displacements (level `m`):

```text
w_left = (-10/(19m), 0),   w_down = (0, -7/(19m))
w_T    = (-70/(19m), +70/(19m)),   w_RT = (+70/(19m), -70/(19m))
w_right = (+10/(19m), 0),  w_up = (0, +7/(19m))
```

## 3. Phase facts at level `m` (scale-free, accepted DLH-5V-A structure)

```text
i_t(j) = floor((N_m - 10j)/7),   r_j = (N_m - 10j) mod 7 in {0,...,6}
r_{j+7} = r_j (period 7);  i_t(j+7) = i_t(j) - 10
top cell of class j is always W-active; sub-top (i_t(j) - 1) iff r_j in {0,1,2} and i_t(j) >= 2
cells with i <= i_t(j) - 2 are never W-active (interior)
```

## 4. Endpoint stencil layers at level `m` and physical width

```text
lower-a layer:  j in {0,...,6}         (a in [0, 60/(19m)])
upper-a layer:  j in {19m-6,...,19m}   (a in [10 - 60/(19m), 10])
lower-b layer:  i in {0,...,9}         (b in [b_min, b_min + 63/(19m)])
```

Uniform physical-width bound: `ell_m = 70/(19m) = O(1/m) -> 0`, uniform in `theta` and `N_m mod 7` (membership-based).

## 5. Structural facts (exact proofs; supplementary spot-checks, 0 violations)

- **(F1)** every W-active cell with `j <= 6` satisfies `i >= 10`.
  Exact proof: `i >= i_t(j) - 1` (W-active cells are top or sub-top); `i_t(j) = floor((N_m - 10j)/7) >= (N_m - 10j - 6)/7
  >= (N_m - 66)/7`; `N_m >= 190m >= 190`, so `(N_m - 66)/7 >= 124/7 > 10`; hence `i >= i_t(j) - 1 >= 10`.
  Spot-check: 980 cells over `m in {1..7}`, `N_m = 190m + s`, `s in {0..13}` — 0 violations.
- **(F2)** every W-active cell with `i <= 9` satisfies `j >= 19m - 7`.
  Exact proof: `i <= 9` and W-active imply `i in {i_t(j), i_t(j) - 1}`, so `i_t(j) <= 10`, i.e.
  `floor((N_m - 10j)/7) <= 10`, i.e. `(N_m - 10j)/7 < 11`, i.e. `10j > N_m - 77`, i.e. `j >= floor((N_m - 77)/10) + 1`
  (j integer). Since `(N_m - 77)/10 >= (190m - 77)/10 = 19m - 7.7`, `floor((N_m - 77)/10) >= 19m - 8`, so
  `j >= 19m - 7`. The largest a-interior class is `j = 19m - 7` with `i_t = 10` and, when `N_m mod 7 in {0,1,2}`, the
  W-active sub-top `(19m - 7, 9)`.
  Spot-check: 931 cells — 0 violations.
- **(F3)** no W-active cell has `j <= 6` and `i <= 9` (F1 + F2). Spot-check: 0 violations.
- **(F4)** sector generators are represented destinations at every layer cell (as in Rev 0): 2734 availability checks, 0 missing.
- **(F5, new)** for fixed `W_max > 8`, W-active lower-b-layer cells disappear for `m > 69/(19*(W_max - 8))`.
  Exact proof: a W-active cell with `b <= b_min + 63/(19m)` satisfies `a = (a + b) - b >= W_max - (r + theta + 63)/(19m)
  >= (W_max + 2) - 69/(19m)` (using `a + b >= W_max - (r+theta)/(19m)` for W-active cells); for
  `m > 69/(19(W_max - 8))` this exceeds `a_max = 10`, contradicting `a <= a_max`. Only at `W_max = 8` can an infinite
  W-active lower-b sequence converge to the triple corner `(a_max, b_min)`. For `W_max > 8`, lower-b layer cells are
  non-W-active interior cells for large `m`.

## 6. Interior-layer / corner taxonomy (CORRECTED — reviewer item 6)

- W-active layer cells: `a + b -> W_max`; at fixed `j` (or `j = o(m)`) with `W-dist -> 0` they converge to the corners
  `(0, W_max)` (lower-a) / `(a_max, W_max - a_max)` (upper-a); at `j ~ alpha m`, `alpha in (0, 19)` they converge to
  interior W-face points.
- **Non-W-active cells with bounded `k = i_t(j) - i`** (including `(0, i_t(0) - 2)`): `W-dist = (7k + r_j + theta_m)/(19m)
  -> 0` — they converge to **corners**, NOT to face interiors (the Rev-0 statement was false and is corrected here).
- **Non-W-active cells with `k ~ alpha m`, `alpha > 0`**: `W-dist -> 7 alpha/19 > 0` — face-interior limits; the true
  tangent cone there has full `b`-freedom (e.g. `{mu_a >= 0}` at `(0, b_*)`).
- **Non-W-active cells with `k = o(m)` but `k -> oo`**: corner limits with `W-dist -> 0` (Family C — the obstruction
  class of reviewer comment `5634957294`).

## 7. Corner limits of the layer states (corrected true cones, DLH-5T semantics)

```text
(0, W_max):                       a = 0 x W:            {mu_a >= 0, mu_W <= 0}
(a_max, W_max - a_max):           a_max x W:            {mu_a <= 0, mu_W <= 0}
(a_max, b_min), W_max > 8:        a_max x b_min only:   {mu_a <= 0, mu_b >= 0}   (W NOT active: a_max + b_min = 8 < W_max)
(a_max, b_min), W_max = 8:        triple corner:        {mu_a <= 0, mu_b >= 0, mu_W <= 0}
(0, b_min):                       a = 0 x b_min:        {mu_a >= 0, mu_b >= 0}   (W NOT active: b_min < W_max)
```

## 8. Supplementary exact spot-checks (tiny `%TEMP%` scripts, never committed)

- F1–F3 over `m in {1..7}`, `s in {0..13}`: 0 violations; F4: 2734 checks, 0 missing.
- Mandatory counterexample `(0, i_t(0) - 2)`, `mu = (0,1)`: `W-dist = (r_0^m + theta_m + 14)/(19m)` verified from
  `0.789` (`m=1`) to `0.008` (`m=100`); `q_up = 19m/7`; destination `(0, i+1)` represented at every level.
- Corner-convergent generalization: `j in {0,3,7,12,30}`, `i = i_t - 2` all give `a -> 0`, `W-dist -> 0`.
- Escape sequences: `k = sqrt(mK)` beats any fixed `K`; `k = m/f(m)`, `f -> oo` beats any shrinking `delta_m`.

These checks are supplementary; the controlling statements are the closed-form proofs above, valid symbolically for all
`m >= 1`.
