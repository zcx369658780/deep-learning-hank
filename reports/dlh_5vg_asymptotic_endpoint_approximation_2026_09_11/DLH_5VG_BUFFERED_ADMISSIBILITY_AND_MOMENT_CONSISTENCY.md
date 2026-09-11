# DLH-5V-G — Buffered Admissibility and Moment Consistency

**Design only.** Full case analysis of the A1 numerical candidate-admissibility buffer: cone equalities, exact
nonnegative rate contracts, exact first moments, tangent-cone consistency (outer/limsup and recovery/liminf) and seam
consistency. All statements hold symbolically for all `m >= 1` (Regime I, `W_max >= 8`); tiny exact spot-checks are
supplementary.

## 1. The buffer (before scoring, never select-then-clip)

```text
(BA1) j <= 6        :  mu_a >= 0     (lower-a stencil layer; == economic law at j = 0)
(BA2) j >= 19m - 6  :  mu_a <= 0     (upper-a stencil layer; == economic law at j = 19m)
(BA3) i <= 9        :  mu_b >= 0     (lower-b stencil layer; == economic law at i = 0)
(BA4) W-active cell :  mu_W <= 0     (true W-face law at contact cells)
```

At interior layer nodes BA1–BA3 are **numerical shrinking-buffer restrictions** — they are NOT economic-face
declarations (Issue §5 critical interpretation). They coincide with the true KKT laws only at `j = 0`, `j = 19m`,
`i = 0`, and BA4 is the true W law at contact cells. The buffer is applied in the candidate-admissibility step of the
frozen pipeline, before `H_h^m` scoring and before the single global argmax. There is no clipping after selection.

## 2. Case analysis (all W-active endpoint cells + interior layer cells)

Structural facts F1–F4 (geometry report) imply the case list is exhaustive and non-overlapping:
Case L (`j <= 6`, `i >= 10`), Case U (`19m-6 <= j <= 19m`, `i >= 10`), Case B (`i <= 9`, `j >= 19m-7`; includes
`U ∩ B` cells), interior cells (`i <= i_t(j) - 2`). No W-active cell lies in `j <= 6` with `i <= 9` (F3).

### Case L — lower-a layer, W-active: reverse sector (accepted formula, m-scaled)

Buffered cone: `{mu_a >= 0, mu_W <= 0}` (BA1 + BA4). Note `mu_b = mu_W - mu_a <= 0` automatically; the buffer selects
exactly the reverse-reallocation cone.

Cone equality (proved): `{mu_a >= 0, mu_W <= 0} = cone{w_RT, w_down}`:

```text
(=>) q_RT = 19m*mu_a/70 >= 0,  q_down = 19m*(-mu_W)/7 >= 0,
     q_RT*w_RT + q_down*w_down = (mu_a, -mu_a) + (0, mu_W) = (mu_a, mu_b)   (exact)
(<=) cone elements: mu_a = 70*q_RT/(19m) >= 0,  mu_W = -7*q_down/(19m) <= 0.
```

`det[w_RT, w_down] = -490/(19m)^2 != 0`, so the decomposition is unique. Destinations `(j+7, i-10)` (mirror, same-W)
and `(j, i-1)` are represented (F4).

**Resolution of the DLH-5V-F obstruction at lower-band `r_j = 0` cells:** the obstructing forward-sliding ray
`(-u, +u)` has `mu_a = -u < 0`, hence is excluded by BA1 before scoring. Every admitted drift (including the
reverse-sliding ray `(+u, -u)`, `mu_a = u >= 0`) is exactly represented by `(w_RT, w_down)`.

### Case U — upper-a layer, W-active, `i >= 10`: T_realloc/deplete (accepted formulas, m-scaled)

Buffered cone: `{mu_a <= 0, mu_W <= 0}` (BA2 + BA4) = `cone{w_left, w_down, w_T}` (the full accepted `T_W` restricted
to `mu_a <= 0`):

```text
mu_b >= 0:  q_T = 19m*mu_b/70,  q_in = 19m*(-mu_W)/10  on (w_T, w_left):
            q_T*w_T + q_in*w_left = (-mu_b, mu_b) + (mu_W, 0) = (mu_a, mu_b)   (exact)
mu_b < 0:   q_left = 19m*(-mu_a)/10,  q_down = 19m*(-mu_b)/7  on (w_left, w_down):
            q_left*w_left + q_down*w_down = (mu_a, mu_b)   (exact)
```

Destinations `(j-1, i)`, `(j, i-1)`, `(j-7, i+10)` (same-W) are represented (F4). At exact-frontier `r_j = 0` cells the
obstructing reverse-sliding ray `(+u, -u)` has `mu_a = u > 0` and is excluded by BA2; every admitted drift is exactly
represented.

### Case B — lower-b layer, W-active: T_realloc (accepted `(19,0)`-type formula, m-scaled)

Buffered cone: `{mu_b >= 0, mu_W <= 0}` (BA3 + BA4). Since `mu_a = mu_W - mu_b <= 0`, this equals
`{mu_a <= 0, mu_b >= 0, mu_W <= 0} = cone{w_left, w_T}`:

```text
q_T = 19m*mu_b/70,  q_in = 19m*(-mu_W)/10  on (w_T, w_left):
q_T*w_T + q_in*w_left = (mu_W - mu_b, mu_b) = (mu_a, mu_b)   (exact)
```

Destinations `(j-1, i)` and `(j-7, i+10)` (same-W, `i + 10 in {10,...,19}`) are represented (F4). Covers the corner
cells `(19m, i)`, `i in {0,...,9}` (including the `b = b_min` face cell when W-active) and the a-interior sub-top
`(19m-7, 9)` (F2). For `U ∩ B` cells the BA2 constraint is implied by BA3 + BA4, so the same cone applies — no
conflict, no double ownership.

### Interior layer cells (`i <= i_t(j) - 2`)

Buffered cone is a half-plane (or the full plane away from faces) contained in the accepted 3- or 4-neighbor adjacency
cone; equality holds at face-adjacent positions:

```text
j = 0:  cone{w_right, w_down, w_up} = {mu_a >= 0}   (== BA1, == economic law at a = 0)
j = 19m: cone{w_left, w_down, w_up} = {mu_a <= 0}   (== BA2, == economic law at a = a_max)
i = 0:  cone{w_left, w_right, w_up} = {mu_b >= 0}   (== BA3, == economic law at b = b_min)
(0,0):  cone{w_right, w_up} = {mu_a >= 0, mu_b >= 0}
(19m,0): cone{w_left, w_up} = {mu_a <= 0, mu_b >= 0}
```

Representability is exact with the accepted interior rates (m-scaled); e.g. at `j = 0` interior cells,
`q_right = 19m*mu_a/10`, and `q_up/q_down = 19m*max(+-mu_b, 0)/7`.

## 3. Moment-consistency theorem (T1–T4 of the umbrella)

**T1 — Exactness away from endpoints.** For compact `K` of W-face points at distance `delta > 0` from
`{a = 0} cup {a = a_max} cup {b = b_min}`: `j >= 7` iff `a >= 70/(19m)` and `i >= 10` iff
`b - b_min >= 70/(19m)`; hence for `m >= ceil(70/(19*delta))` every W-face state in `K` is regular
(`7 <= j <= 19m - 7`, `i >= 10`) and carries the accepted exact DLH-5V-E contract — pointwise exact, not approximate.

**T2 — Shrinking layer.** Buffered region `subset {a in [0, 60/(19m)] cup [10 - 60/(19m), 10]} cup
{b in [b_min, b_min + 63/(19m)]}`; uniform bound `ell_m = 70/(19m) -> 0`, uniform in `theta` and `N_m mod 7`
(membership-based). The grid-column count in each layer stays bounded (7 columns / 10 rows).

**T3 — Outer/limsup tangent-cone consistency.** For layer states `s_m` with `x_m -> x_*` (corner limits per the
geometry report): the buffered cone at `s_m` equals the true economic tangent cone at `x_*`:
`(0, W_max)`: `{mu_a >= 0, mu_W <= 0}`; `(a_max, W_max - a_max)`: `{mu_a <= 0, mu_W <= 0}`;
`(a_max, b_min)`: `{mu_a <= 0, mu_b >= 0, mu_W <= 0}`; face interiors: the buffered half-plane equals the true tangent
cone at the limit. Hence every bounded admitted drift sequence clusters in the true tangent cone of the limit point;
no outward drift is admitted in the limit and no inward-normal drift is hidden.

**T4 — Recovery/liminf tangent-cone consistency.** Because the buffered cone at every layer state **equals** the true
tangent cone at its limit point (equalities in §2), every drift in the true tangent cone at a limit point is
A1-admitted and exactly represented by represented native destinations (recovery is exact, not merely approximate).

## 4. Seam consistency (T8)

The layer contracts are the accepted sector formulas evaluated at the m-scaled grid. On the overlaps:

- `j = 6` (Case L) vs regular `j = 7` (R_reverse): identical `q_RT = 19m*mu_a/70`, `q_down = 19m*(-mu_W)/7` for common
  candidates (`R_reverse` drifts); T_realloc/R_deplete candidates are admitted only at `j = 7`, which is exactly the
  true-law expansion at the limit point `a -> 0` — no double ownership, no hidden discontinuous rate switch.
- `j = 19m - 7` (Case B sub-top `(19m-7, 9)`) vs regular `(19m-7, 10)`: T_realloc rates identical for common
  candidates; `mu_b < 0` admitted only at `i >= 10`, matching the true law at the limit `b -> b_min`.
- `j = 19m - 6` (Case U) vs regular `(19m - 7, ...)`: T_realloc/deplete identical for common candidates.
- Buffer-vanishing on candidates: at the boundary of each buffered cone (`mu_a = 0`, `mu_b = 0`, `mu_W = 0`) the rates
  vanish continuously and match the adjacent accepted sector boundary identities (B1/B2/B3 of DLH-5V-E, m-scaled).

No admitted drift at any layer state is outside the true tangent cone at its limit point, and every feasible-at-limit
drift is admitted: the buffer is asymptotically equivalent to the true KKT law on a vanishing physical layer.

## 5. Supplementary exact spot-checks (tiny `%TEMP%` scripts, never committed)

- Sector-generator availability at sample layer states (all residues): 795 checks, 0 missing; structural F1–F4 over
  `m in {1..7}`, `s in {0..13}`: 0 violations.
- Rate-moment equality for rational drifts across all m and all three sectors: exact (`True`).
- Buffered-drift-in-destination-cone exact separation tests (2D cone membership via normals of generator rotations):
  158 checks, 0 failures — includes exact-frontier `r_j = 0` cells in all three layer cases.

These checks are supplementary; the controlling statements are the closed-form cone equalities and rate formulas above,
valid symbolically for all `m >= 1`.
