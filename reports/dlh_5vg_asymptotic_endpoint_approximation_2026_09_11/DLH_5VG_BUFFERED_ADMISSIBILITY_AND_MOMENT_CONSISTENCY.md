# DLH-5V-G — Buffered Admissibility and Moment Consistency (Rev 1)

**Design only.** Corrected case analysis (finite-m algebra, retained), the reviewer-counterexample section, the
graph-consistency impossibility proof, and the A2 note. All statements analytic in `m` (Regime I, `W_max >= 8`); tiny
exact `%TEMP%` spot-checks supplementary.

## 1. The buffer (before scoring, never select-then-clip)

```text
(BA1) j <= 6        :  mu_a >= 0     (lower-a stencil layer; == economic law at j = 0)
(BA2) j >= 19m - 6  :  mu_a <= 0     (upper-a stencil layer; == economic law at j = 19m)
(BA3) i <= 9        :  mu_b >= 0     (lower-b stencil layer; == economic law at i = 0)
(BA4) W-active cell :  mu_W <= 0     (true W-face law at contact cells)
```

At interior layer nodes BA1–BA3 are numerical shrinking-buffer restrictions, NOT economic-face declarations. The buffer
is applied in the candidate-admissibility step before `H_h^m` scoring and the single global argmax; no clipping after
selection.

## 2. Case analysis (finite-m algebra — retained and corrected)

Structural facts F1–F4 (geometry report): cases L (`j <= 6`, `i >= 10`), U (`19m-6 <= j <= 19m`, `i >= 10`),
B (`i <= 9`, `j >= 19m-7`; includes `U ∩ B`), interior cells; no W-active cell in `j <= 6` with `i <= 9`.

### Case L — lower-a layer, W-active: reverse sector

Buffered cone `{mu_a >= 0, mu_W <= 0} = cone{w_RT, w_down}` (exact equality; `det = -490/(19m)^2 != 0`):

```text
q_RT = 19m*mu_a/70,   q_down = 19m*(-mu_W)/7,
q_RT*w_RT + q_down*w_down = (mu_a, mu_b)   (exact)
```

Destinations `(j+7, i-10)` (mirror) and `(j, i-1)` represented (F4). At exact-frontier `r_j = 0` cells the DLH-5V-F
obstructing ray `(-u,+u)` is excluded by BA1; every admitted drift exactly represented.

### Case U — upper-a layer, W-active, `i >= 10`: T_realloc/deplete

Buffered cone `{mu_a <= 0, mu_W <= 0} = cone{w_left, w_down, w_T}`:

```text
mu_b >= 0:  q_T = 19m*mu_b/70,  q_in = 19m*(-mu_W)/10  ->  (mu_a, mu_b)   (exact)
mu_b < 0:   q_left = 19m*(-mu_a)/10,  q_down = 19m*(-mu_b)/7  ->  (mu_a, mu_b)   (exact)
```

Destinations `(j-1, i)`, `(j, i-1)`, `(j-7, i+10)` represented (F4).

### Case B — lower-b layer, W-active: T_realloc

Buffered cone `{mu_b >= 0, mu_W <= 0} = {mu_a <= 0, mu_b >= 0, mu_W <= 0} = cone{w_left, w_T}`:

```text
q_T = 19m*mu_b/70,  q_in = 19m*(-mu_W)/10  ->  (mu_a, mu_b)   (exact)
```

Destinations `(j-1, i)` and `(j-7, i+10)` represented (F4). **Correction (F5):** for fixed `W_max > 8`, W-active
lower-b cells exist only for `m <= 69/(19(W_max - 8))`; for large `m` the lower-b layer cells are non-W-active interior
cells with buffered cone `{mu_a <= 0, mu_b >= 0}` (BA2 + BA3) = the true `a_max x b_min` corner cone (W inactive) —
graph-consistent. Only at `W_max = 8` does an infinite W-active lower-b sequence converge to the triple corner
`(a_max, b_min)` with cone `{mu_a <= 0, mu_b >= 0, mu_W <= 0}`.

### Interior layer cells (`i <= i_t(j) - 2`)

Buffered cone is a half-plane/full-plane subset of the accepted 3/4-neighbor cone (equality at face-adjacent positions,
e.g. `j = 0`: `cone{w_right, w_down, w_up} = {mu_a >= 0}`). Exactly representable with accepted interior rates
(m-scaled).

## 3. Reviewer counterexample and graph-consistency obstruction (CONTROLLING)

### 3.1 Mandatory counterexample test (confirmed)

`m >= 1`, `s_m = (0, i_t^m(0) - 2)` (represented, interior/non-W-active):

```text
a_m = 0,  W_max - b_{i_m} = (theta_m + r_0^m + 14)/(19m) -> 0   =>   x_m -> (0, W_max)
```

Under A1: BA1 applies (`mu_a >= 0`), BA4 does not. `mu = (0, +1)` is A1-admitted and exactly represented by the native
`w_up = (0, 7/(19m))` to `(0, i_m + 1)` (represented) with `q_up = 19m/7 >= 0`. At the corner the true tangent cone is
`{mu_a >= 0, mu_W <= 0}`, and `mu_W = +1 > 0`. Therefore:

```text
limsup admitted drift graph  NOT subset of  true tangent-cone graph at (0, W_max).   OUTER/LIMSUP FAILS.
```

Verified over `m in {1,2,5,20,100}` (exact rational arithmetic).

### 3.2 Generalization — unbounded family + frozen regular block

For every fixed `j` (and every `j_m = o(m)`), `s_m = (j, i_t^m(j) - 2)` satisfies `a_m -> 0`, `W-dist -> 0`, hence
`x_m -> (0, W_max)`. This includes `j = 7, 8, ..., 12, 30, ...` in the **accepted regular region**, where the frozen
accepted interior process is full-plane and admits `mu = (0, +1)`. Hence the global outer condition is violated by the
frozen regular/interior contract itself; no endpoint-layer-only buffer can repair it without reopening the frozen
regular block (forbidden). Same mechanism at the upper corner: `s_m = (19m, i_t^m(19m) - 2) -> (a_max, W_max - a_max)`,
`mu = (-1, +2)` (exact via `w_left` + `w_up`) has `mu_W = +1 > 0 notin {mu_a <= 0, mu_W <= 0}`.

### 3.3 Impossibility — no per-state admissible-set rule satisfies both graph conditions

Family C (corner/W-face limits): `W-dist -> 0`, i.e. `k_m = i_t - i = o(m)` (growing rows, physical W-distance still
vanishing). Family F (face-interior limits): `W-dist -> c > 0`, i.e. `k_m ~ 7cm/19` (linear rows). Requirements:

- **outer** at `(0, W_max)` and every W-face point: W-constraint `mu_W <= 0` eventually on every Family-C sequence;
- **recovery/liminf** at every face-interior point with `W-dist = c > 0`: no W-constraint eventually on every Family-F
  sequence converging to it (true cone `{mu_a >= 0}` there needs full `b`-freedom).

Candidate per-state rules and their failures:

| rule | outer | liminf |
|---|---|---|
| W-activity only (BA4 on W-active) | fails (misses all non-W-active Family C — the counterexample) | ok |
| fixed row count `k <= K` | fails (`k = sqrt(mK)` escapes) | ok |
| shrinking W-dist `delta_m -> 0` | fails (`k = m/f(m)`, `f -> oo` slow, `W-dist = 7/(19 f(m))`) | ok |
| fixed W-dist `delta > 0` | ok | fails at `W-dist = c < delta` points |
| any per-state rule | Families C and F are indistinguishable per-state; no partition realizes both | |

Hence **no per-state numerical admissible-set rule can satisfy the exact Issue-#55 outer/limsup + recovery/liminf graph
conditions.** The true tangent-cone multifunction is discontinuous at the boundary, and the grid provides dense interior
approximations of every boundary point; the two conditions force Kuratowski convergence of the discrete admissible sets
to it, which the grid geometry cannot realize per-state.

### 3.4 Consequence

A1 as submitted fails (3.1); the strengthened A1 variants fail (3.3); the global condition fails on the frozen regular
block (3.2). **A1 fails the controlling graph-consistency requirement.**

## 4. A2 cannot repair the admissible-set failure

A2 (Issue §5) relaxes the exact-moment requirement via `e_m(s,u)`; it does not change the admissible-set rule. The
counterexample drift `mu = (0, +1)` at `(0, i_t(0) - 2)` is continuously admissible at the node position (strictly
inside `D_W` in the W-direction) and exactly representable (`q_up = 19m/7`, defect exactly zero) — no moment-defect term
can exclude it. The admissible-set outer/limsup failure at the corners is therefore **not** repaired by any permitted A2
construction. (Matches the reviewer's explicit note; here it is proved, not assumed.)

## 5. Supplementary exact spot-checks (tiny `%TEMP%` scripts, never committed)

- Sector-generator availability: 2734 checks, 0 missing; F1–F5 over `m in {1..7}`, `s in {0..13}`: 0 violations.
- Rate-moment equality for rational drifts across all m/sectors: exact (`True`).
- Mandatory counterexample + generalization + escape sequences: verified exactly (see §3).
- Buffered-drift-in-destination-cone exact separation tests: 158 checks, 0 failures (finite-m algebra only).
