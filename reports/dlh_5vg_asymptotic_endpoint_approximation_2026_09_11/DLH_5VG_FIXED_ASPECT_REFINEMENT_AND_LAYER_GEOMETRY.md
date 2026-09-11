# DLH-5V-G — Fixed-Aspect Refinement Family and Layer Geometry

**Design only.** Symbolic family, scaling identities, endpoint-layer geometry and structural facts for Issue #55 /
DLH-5V-G. All statements are analytic in `m`; tiny exact `%TEMP%` spot-checks are reported as supplementary only.

## 1. The refinement family (Issue §4, frozen)

```text
m = 1, 2, 3, ...
da_m = 10/(19m),  db_m = 7/(19m)
a_j^(m) = j*10/(19m),            j = 0, ..., 19m
b_i^(m) = b_min + i*7/(19m),     i >= 0,  b_min = -2
N_m = floor(19m*(W_max - b_min))
represented nodes: 10j + 7i <= N_m
```

`m = 1` is the currently accepted native grid. No numerical production `W_max` is selected; `W_max >= 8` (Regime I,
`N_m >= 190m`) is the controlling accepted regime of the DLH-5V-F certificates.

## 2. Scaling identities

Let `kappa_1 = 19*(W_max - b_min) = N_1 + theta_1`, `N_1 = floor(kappa_1)`, `theta_1 in [0,1)`. Then

```text
kappa_m = 19m*(W_max - b_min) = m*kappa_1 = m*N_1 + m*theta_1
N_m = m*N_1 + floor(m*theta_1),   theta_m = {m*theta_1} in [0,1)
```

The level-1 node `(j,i)` corresponds to the level-`m` node `(mj, mi)`; its representedness at level `m` is
`10(mj) + 7(mi) = m(10j + 7i) <= N_m` iff `10j + 7i <= N_1 + floor(m*theta_1)/m`. As at level 1 (DLH-5V-A), the node
set is fixed by `N_m` while `theta_m` moves only the frontier line — the family is a self-similar refinement of the
continuous domain `D_W`, not a nested refinement of node sets.

Physical displacements (level `m`):

```text
w_left = (-10/(19m), 0),   w_down = (0, -7/(19m))
w_T    = (-70/(19m), +70/(19m)),   w_RT = (+70/(19m), -70/(19m))
w_right = (+10/(19m), 0),  w_up = (0, +7/(19m))
```

Native same-W displacements satisfy `10*Delta j + 7*Delta i = 0`; with gcd(10,7) = 1 the primitive same-W moves are
`(-7, +10)` (forward) and `(+7, -10)` (mirror).

## 3. Phase facts at level `m` (scale-free, accepted DLH-5V-A structure)

```text
i_t(j) = floor((N_m - 10j)/7),   r_j = (N_m - 10j) mod 7 in {0,...,6}
r_{j+7} = r_j (period 7);  i_t(j+7) = i_t(j) - 10
top cell of class j is always W-active; sub-top (i_t(j) - 1) iff r_j in {0,1,2} and i_t(j) >= 2
cells with i <= i_t(j) - 2 are never W-active (interior)
```

## 4. Endpoint stencil layers at level `m`

```text
lower-a layer:  j in {0,...,6}         (a in [0, 60/(19m)])
upper-a layer:  j in {19m-6,...,19m}   (a in [10 - 60/(19m), 10])
lower-b layer:  i in {0,...,9}         (b in [b_min, b_min + 63/(19m)])
```

Uniform physical-width bound:

```text
ell_m = 70/(19m) = O(1/m)  ->  0   (all coordinate bands are <= ell_m)
```

The layer definitions depend only on grid-coordinate membership, hence the width bound is **uniform in the frontier
phase** `theta` and in `N_m mod 7`.

## 5. Structural facts (proved; spot-verified exactly, 0 violations)

For `m in {1..7}`, all residues `N_m = 190m + s`, `s in {0..13}` (covering `W_max in [8, 8 + 14/19)` — the hardest case;
larger `W_max` only increases the relevant `i`-values, relaxing availability):

- **(F1)** every W-active cell with `j <= 6` satisfies `i >= 10`. Proof: `i_t(j) >= (N_m - 60)/7 >= (190m - 61)/7 >= 18`
  for `m >= 1`; the lower-a layer is entirely `b`-interior. Verified 980 cells, 0 violations.
- **(F2)** every W-active cell with `i <= 9` satisfies `j >= 19m - 7`. Proof: `i_t(j) <= 10` iff `j >= (N_m - 77)/10`;
  the largest a-interior class is `j = 19m - 7` with `i_t = 10` and, when `N_m mod 7 in {0,1,2}`, the W-active sub-top
  `(19m - 7, 9)`. All other lower-b W-active cells lie in `j >= 19m - 6`. Verified 931 cells, 0 violations.
- **(F3)** no W-active cell has `j <= 6` and `i <= 9` (F1 + F2). Verified 0 violations.
- **(F4)** sector generators are represented destinations at every layer cell:
  - Case L (`j <= 6`, `i >= 10`): `(j+7, i-10)` has `j + 7 <= 13 <= 19m`, `i - 10 >= 0`, index `10(j+7)+7(i-10) = 10j+7i <= N_m`; `(j, i-1)` index `10j + 7(i-1) = W_idx - 7 <= N_m`.
  - Case U (`j >= 19m-6`, `i >= 10`): `(j-1, i)` (`W_idx - 10`), `(j, i-1)` (`W_idx - 7`), `(j-7, i+10)` (same-W index `W_idx`, `j - 7 >= 19m - 13 >= 6`, `i + 10 >= 20 >= 0`) all represented.
  - Case B (`i <= 9`, `j >= 19m-7`): `(j-1, i)` (`W_idx - 10`), `(j-7, i+10)` (same-W index `W_idx`, `j >= 19m - 7 >= 12 >= 7`, `i + 10 in {10,...,19}`) all represented.
  - Interior cells (`i <= i_t(j) - 2`): `(j+-1, i)` and `(j, i+-1)` indices `W_idx +- 10 <= N_m - 4` and `W_idx +- 7 <= N_m - 7`; face-adjacent positions keep the 3 available neighbors.
  - Verified: 795 + 931 + 980 + 28 = 2734 availability checks, 0 missing.

## 6. Corner limits of the layer states

- Lower-a layer states: `a -> 0`; W-active ones satisfy `a + b -> W_max`, so `x_* = (0, W_max)`.
- Upper-a layer states (`i >= 10`): `a -> a_max`, `a + b -> W_max`, so `x_* = (a_max, W_max - a_max)`.
- Lower-b layer states: `b -> b_min`, `a -> a_max` (they lie in `j >= 19m - 7`), so `x_* = (a_max, b_min)`.
- Interior layer states: limit points are face interiors (`{a = 0}`, `{a = a_max}`, `{b = b_min}`), not corners.

These limits make the numerical buffer coincide with the true economic tangent cone at the limit points (see the
buffered-admissibility report, T3/T4).

## 7. Supplementary exact spot-checks (tiny `%TEMP%` scripts, never committed)

- Layer-membership claims F1–F3 over `m in {1..7}`, `s in {0..13}`: 0 violations.
- Sector-generator availability (F4): 2734 checks, 0 missing.
- Buffered-drift-in-destination-cone exact separation tests: 158 checks, 0 failures.
- Width arithmetic and scaling: `ell_m = 70/(19m)` verified numerically for `m in {1,2,5,10}`; second moment `m * S2`
  constant over `m in {1..32}` (rate `O(m)`, second moment `O(1/m)`).

These checks are supplementary; the controlling results are the closed-form statements above and in the companion
reports, which hold for all `m >= 1` symbolically.
