# DLH-5V-G — Shrinking Endpoint-Layer Asymptotic Same-Process Approximation (Umbrella Design)

**Issue:** deep-learning-hank #55 (DLH-5V-G) · **Task type:** `SCIENTIFIC_DESIGN__SHRINKING_ENDPOINT_LAYER_ASYMPTOTIC_MARKOV_APPROXIMATION`
**Branch:** `dsh/issue-55-dlh-5vg-asymptotic-endpoint-approximation-2026-09-11` · **Activation:** comments `5634144909` (+ refresh `5634171277`)
(`DLH_5VG_ROUTE_A_SHRINKING_ENDPOINT_LAYER_ASYMPTOTIC_APPROXIMATION_AUTHORIZED`), final CURRENT sync `origin/main` = `c8c5c3f8d3a002a7efcb93682ff42d50c3667602`
**Status:** Route-A numerical candidate-admissibility buffer (A1) constructed and its full consistency theorem proved at the design level — submitted for fresh ChatGPT review, **NOT scientific acceptance**. Owner decision: `APPROVE_DLH_5VG_ROUTE_A_ASYMPTOTIC_ENDPOINT_APPROXIMATION_DESIGN_GATE`.

## 1. Frozen inputs (accepted — consumed, not reopened)

- Accepted DLH-5V-F obstruction (controlling): at exact-frontier `r_j = 0` top states every represented destination has
  `Delta W <= 0`; exact `mu_W = 0` with nonnegative rates requires same-W destinations only; native same-W displacements
  satisfy `10 Delta j + 7 Delta i = 0` and are multiples of `(7,-10)`; lower endpoint bands can miss `(-7,+10)` and upper
  bands can miss `(+7,-10)`. This is a lattice/discretization obstruction, not a household-source failure. Not reopened.
- Accepted household source immutable, blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e` verified.
- Domain `D_W(W_max) = {0 <= a <= a_max, b >= b_min, a+b <= W_max}`, `a_max = 10`, `b_min = -2`, no numerical `W_max`.
- Symbolic fixed-aspect refinement family (`m = 1,2,...`): `da_m = 10/(19m)`, `db_m = 7/(19m)`, `a_j = j*10/(19m)`,
  `b_i = b_min + i*7/(19m)`, `N_m = floor(19m*(W_max-b_min))`, represented nodes `10j + 7i <= N_m`.
- Accepted regular contracts (DLH-5V-A..E) on the common regular region `7 <= j <= 12`, `i >= 10` (level-1 units) remain
  exact and frozen; wide stencils: forward `(j,i)->(j-7,i+10)` iff `j >= 7`; mirror `(j,i)->(j+7,i-10)` iff `j <= 12`
  (`j <= 19m-7` at level `m`) and `i >= 10`; deferred endpoint complement `j in {0..6}`, `j in {19m-6..19m}`,
  `i in {0..9}` (level-`m` units) + W-active endpoint cells.
- Accepted sector formulas (level-`m` instances; physical drifts in `(a,b)` units, displacements in physical units):
  `w_left = (-10/(19m), 0)`, `w_down = (0, -7/(19m))`, `w_T = (-70/(19m), +70/(19m))`, `w_RT = (+70/(19m), -70/(19m))`;
  `R_reverse = {mu_a > 0, mu_b < 0, mu_W <= 0}` with `q_RT = 19m*mu_a/70`, `q_down = 19m*(-mu_W)/7` on `(w_RT, w_down)`;
  `T_realloc = {mu_a <= 0, mu_b >= 0, mu_W <= 0}` with `q_T = 19m*mu_b/70`, `q_in = 19m*(-mu_W)/10` on `(w_T, w_left)`;
  `R_deplete = {mu_a <= 0, mu_b < 0}` with `q_left = 19m*(-mu_a)/10`, `q_down = 19m*(-mu_b)/7` on `(w_left, w_down)`.

## 2. Route-A scientific object (Issue §4–§5)

Issue #55 tests whether the DLH-5V-F obstruction is only a finite-grid endpoint-layer phenomenon that can be handled by a
**shrinking numerical candidate-admissibility buffer** (A1) applied **before** candidate scoring, clearly distinguished
from true economic faces. Only if A1 fails may the successor test an explicit first-moment defect (A2).

**A1 buffer (this contract).** At a level-`m` state `s = (j,i)`, a continuously admissible drift `mu` is an
**A1-admitted candidate** iff:

```text
(BA1) j <= 6            (lower-a stencil layer):      mu_a >= 0   [numerical; == economic law at j = 0]
(BA2) j >= 19m - 6      (upper-a stencil layer):      mu_a <= 0   [numerical; == economic law at j = 19m]
(BA3) i <= 9            (lower-b stencil layer):      mu_b >= 0   [numerical; == economic law at i = 0]
(BA4) s W-active cell   (W-contact):                  mu_W <= 0   [true W-face law at contact cells]
```

No restriction is imposed away from the layers. The buffer is applied in the candidate-admissibility step, **before**
`H_h^m` scoring and before the global argmax. No candidate is selected and then clipped; no destination is omitted with a
retained diagonal; no reflection/ghost/interpolation/KFE-only repair.

**A1 result (this contract).** A1 **passes**: every A1-admitted candidate at every state of the frozen family has an
exact represented native-grid first-moment contract with nonnegative rates, on a physical layer of width
`ell_m = 70/(19m) -> 0`, recovering the accepted exact regular contract away from endpoints, with tangent-cone,
generator/operator, scaling, monotonicity, conservation, one-Q and seam consistency. A2 is therefore **not invoked**
(Issue §5.5: "if A1 succeeds, preserve exact first moments for every admitted candidate and do not invoke A2").

## 3. The A1 contract — case analysis (exact, closed form, `m >= 1`, Regime I `W_max >= 8`)

Layer membership and structural facts (proved in the companion geometry report; spot-verified exactly over
`m in {1..7}`, all residues `N_m = 190m + s`, `s in {0..13}`, `0` violations):

- **(F1)** every W-active cell with `j <= 6` has `i >= 10` (so the lower-a layer has no lower-b intersection);
- **(F2)** every W-active cell with `i <= 9` has `j >= 19m - 7` (lower-b cells live in the upper-a layer or at the
  a-interior boundary `j = 19m - 7`, including the sub-top `(19m-7, 9)` when `N_m mod 7 in {0,1,2}`);
- **(F3)** no W-active cell has `j <= 6` and `i <= 9`;
- **(F4)** sector generators are represented destinations at every layer cell (see per-case availability below).

**Case L — lower-a layer, W-active (`j <= 6`, `i >= 10`; top and sub-top).**
Buffered cone = `{mu_a >= 0, mu_W <= 0}` (BA1 + BA4; `mu_b = mu_W - mu_a <= 0` automatic). Exact equality
`{mu_a >= 0, mu_W <= 0} = cone{w_RT, w_down}` with `det[w_RT w_down] = -490/(19m)^2 != 0` and rates

```text
q_RT = 19m*mu_a/70,   q_down = 19m*(-mu_W)/7,
q_RT*w_RT + q_down*w_down = (mu_a, mu_W - mu_a) = (mu_a, mu_b)  (exact)
```

Destinations `(j+7, i-10)` (mirror; `j+7 <= 13 <= 19m`, `i >= 10`) and `(j, i-1)` (`i >= 1`) are represented (F4).
This includes the exact-frontier `r_j = 0` cells: the DLH-5V-F obstructing forward-sliding ray `(-u, +u)` has
`mu_a = -u < 0` and is **excluded by BA1** (numerical restriction before scoring). The contract is identical to the
accepted closable `j = 0` reverse-sector formula, m-scaled.

**Case U — upper-a layer, W-active (`19m - 6 <= j <= 19m`, `i >= 10`).**
Buffered cone = `{mu_a <= 0, mu_W <= 0}` (BA2 + BA4) = `cone{w_left, w_down, w_T}` with the accepted split:
`mu_b >= 0` -> `(q_T, q_in)` on `(w_T, w_left)`; `mu_b < 0` -> `(q_left, q_down)` on `(w_left, w_down)`. Moments exact
(identical algebra to the accepted regular contracts, m-scaled). Destinations `(j-1, i)`, `(j, i-1)`, `(j-7, i+10)`
(same-W, `j >= 7`, `j - 7 >= 19m - 13 >= 6`) represented (F4). Includes the `r_j = 0` cells: the obstructing
reverse-sliding ray `(+u, -u)` is excluded by BA2.

**Case B — lower-b layer, W-active (`i <= 9`, `j >= 19m - 7`; top and sub-top).**
Buffered cone = `{mu_b >= 0, mu_W <= 0}` (BA3 + BA4). Since `mu_a = mu_W - mu_b <= 0` automatically, this equals
`{mu_a <= 0, mu_b >= 0, mu_W <= 0} = cone{w_left, w_T}` (the accepted T_realloc cone) with rates

```text
q_T = 19m*mu_b/70,   q_in = 19m*(-mu_W)/10,
q_T*w_T + q_in*w_left = (mu_W - mu_b, mu_b) = (mu_a, mu_b)  (exact)
```

Destinations `(j-1, i)` and `(j-7, i+10)` (`j >= 19m - 7 >= 12 >= 7`, `i + 10 in {10..19}`, same-W) represented (F4).
Covers the corner cells `(19m, i)`, `i in {0..9}` (incl. the b-min face cell) and the a-interior sub-top `(19m-7, 9)`.
At `j = 19m` this is the accepted closable `(19,0)`-type T_realloc contract, m-scaled. (For the `U ∩ B` cells the BA2
constraint `mu_a <= 0` is implied by BA3 + BA4, so the buffered cone is the same `cone{w_left, w_T}` — no conflict.)

**Interior layer cells (`i <= i_t(j) - 2`, any `j`).** Buffered cone is a half-plane/full-plane subset of the accepted
3- or 4-neighbor adjacency cone (`w_left, w_right, w_down, w_up`; equality at face-adjacent positions such as `j = 0`
-> `cone{w_right, w_down, w_up} = {mu_a >= 0}` and `i = 0` -> `cone{w_left, w_right, w_up} = {mu_b >= 0}`); representable
by the accepted interior rates, m-scaled. Interior cells in the layers converge to the interior of the corresponding
economic face (not to the corners), where the buffered half-plane equals the true tangent cone at the limit.

**No other W-active endpoint cases exist** in Regime I (F1–F3). Regular W-active cells (`7 <= j <= 19m - 7`, `i >= 10`)
keep the accepted exact DLH-5V-E contract with no buffer (BA4 there is the true W law).

## 4. Consistency theorem (Issue §7) — proved at design level

**T1 (exactness away from endpoints).** Let `K` be a compact set of W-face points at distance `delta > 0` from the
endpoint set `{a = 0} cup {a = a_max} cup {b = b_min}`. For `m >= ceil(70/(19*delta))`, every W-face state in `K` has
`7 <= j <= 19m - 7` and `i >= 10` and uses the accepted exact regular contract (no buffer). Exactness is pointwise, not
approximate, on `K`.

**T2 (shrinking physical layer).** The buffered region is contained in the coordinate bands
`a in [0, 60/(19m)] cup [10 - 60/(19m), 10]` and `b in [b_min, b_min + 63/(19m)]`; uniform bound
`ell_m = 70/(19m) = O(1/m) -> 0`, uniformly in the frontier phase `theta` and in `N_m mod 7` (membership-based
definition). The stencil width in grid columns stays bounded (7 columns / 10 rows), the physical width vanishes.

**T3 (outer/limsup tangent-cone consistency).** For any sequence of states `s_m` in the layers with physical positions
`x_m -> x_*`, the buffered admissible cone at `s_m` equals (at corners) or is contained in (toward face interiors) the
true economic tangent cone at `x_*`:
- lower-a layer states (W-active or interior) satisfy `a_m -> 0`; BA1 -> the law `mu_a >= 0` at `x_* in {a = 0}`;
  W-active lower-a states satisfy additionally `a_m + b_m -> W_max`, so `x_* = (0, W_max)` and BA4 -> `mu_W <= 0`;
  buffered cone `{mu_a >= 0, mu_W <= 0}` **equals** the true joint cone at `(0, W_max)`;
- upper-a states -> `a_m -> a_max`; lower-b states -> `b_m -> b_min`; their buffers equal the true corner cones
  `{mu_a <= 0, mu_W <= 0}` and `{mu_a <= 0, mu_b >= 0, mu_W <= 0} = T_realloc` respectively (equality at the limit);
- interior layer states -> face interiors where the buffered half-plane equals the true tangent cone at the limit.
Hence every bounded admitted drift sequence clusters in the true tangent cone of the limit point (no inward-normal drift
is hidden, no outward drift is admitted in the limit).

**T4 (recovery/liminf tangent-cone consistency).** The buffered cone at every layer state **equals** the true tangent
cone at its limit point (cone equalities in §3), so recovery is exact: every drift in the true tangent cone at a limit
point is A1-admitted and exactly represented by represented native destinations (not merely approximated).

**T5 (jump/rate/second-moment scaling — proved, not assumed).** Every represented displacement is an integer multiple
of `(10/(19m), 7/(19m))`; max jump `|w| = sqrt(2)*70/(19m) = O(1/m)`. For fixed physical drift `mu = O(1)`, the rates
are `q ~ 19m*|mu|/c = O(m)`. Second moments (explicit, all cases):
`L: sum q|w|^2 = (2660*mu_a + 133*(-mu_W))/(361 m)`; `U/B (T_realloc branch)`: `q_T*2*(70/(19m))^2 + q_in*(10/(19m))^2 =
O(1/m)`; `deplete branch`: `O(1/m)`; interior: `O(1/m)` (rates O(m), jumps O(1/m)). All `= O(1/m)` with constants that
are uniform in the frontier phase. Verified exactly: `m * (2nd moment)` is constant across `m in {1..32}`.

**T6 (generator/operator consistency).** For `phi in C^2` with `||D^2 phi|| <= M_2`,
`|L_m phi(s) - mu . grad phi(s)| <= (1/2) (sum q_r |w_r|^2) M_2 + O(m * (1/m)^3) = O(M_2/m)`; the Taylor remainder
vanishes (third-order terms `sum q |w|^3 = O(1/m^2)`). For smooth test functions the discrete generator converges to
`mu . grad phi` at every state, with vanishing numerical diffusion of order `1/m`.

**T7 (monotonicity, conservation, one-Q same-process).** All rates are nonnegative by construction (sector cones with
`q >= 0`); rows are conservative: `Q_ss = -sum_{r != s} q_{sr}` with `Q_m 1 = 0`; off-diagonals nonnegative; the
diagonal equals minus the sum of the ACTUAL represented outgoing rates. The pipeline is the frozen one: continuous
admissibility + A1 buffer -> candidate-specific represented nonnegative rates -> `H_h^m` score BEFORE selection -> ONE
global statewise argmax -> selected rates -> ONE conservative backward `Q_m` -> future KFE consumes exactly `Q_m^T`.

**T8 (seam consistency).** On the overlap with the accepted exact regular contracts (and with the accepted closable
`j = 0`, `j = 19m`, `(19m, 0)` contracts) the rate formulas coincide exactly (m-scaled instances of the same sector
formulas), so candidates common to a layer cell and a neighboring regular cell receive identical rates — no duplicate
sector ownership, no hidden discontinuous process switch. The buffer only shrinks the admitted candidate set on the
shrinking layer, and the restriction at each layer state equals the true tangent cone at its limit point (T3), so no
drift is excluded that is feasible at the limit and none is admitted that is outward at the limit.

## 5. A2 — not invoked

A1 establishes an exact, asymptotically consistent, monotone, conservative same-process contract for the whole frozen
family (T1–T8). Per the Issue's binding preference order, the explicit first-moment defect object `e_m(s,u)` of A2 is
**not** invoked. No pointwise `O(1/m)` moment defect is claimed anywhere; all admitted candidates carry **exact**
first-moment equality.

## 6. Relation to the DLH-5V-F obstruction (consumed, not reopened)

At exact-frontier `r_j = 0` cells the DLH-5V-F obstruction candidates are precisely the drifts with the missing tangent
orientation (`(-u,+u)` in the lower band, `(+u,-u)` in the upper band), i.e. `mu_a < 0` resp. `mu_a > 0`. The A1 buffer
excludes exactly these on the shrinking layer (BA1/BA2) and thereby restores exact representability for every admitted
candidate; at the limit points `(0, W_max)` and `(a_max, W_max - a_max)` the excluded half-planes coincide with the
outward (infeasible) drift half-planes, so the buffer is asymptotically equivalent to the true KKT law. The accepted
obstruction is not argued away: it is consumed as the finite-m reason the buffer is needed.

## 7. Interpretation ceiling (design only)

This gate establishes a **design-level contract and its consistency theorem** for the frozen family. It does NOT
authorize: source/economic mutation; production grid/aspect/domain redesign; state augmentation; coordinate
transformation; numerical production `W_max`; implementation or solver-source mutation; production `Q` assembly/run;
HJB/KFE/stationary solves (stationary KFE remains NOT AUTHORIZED); numerical production experiments; aggregates/GE/
regional/neural/nominal/calibration/policy/welfare/Results; PR/merge/close/successor/self-accept. A finite enumeration
was used only as a supplementary exact spot-check of the closed-form theorem (tiny `%TEMP%` scripts); the theorem is
analytic in `m` and does not rest on enumeration.

## 8. File map (exact six-file allowlist)

1. This umbrella design document.
2. `reports/dlh_5vg_asymptotic_endpoint_approximation_2026_09_11/DLH_5VG_AUTHORITY_CAPSULE.md` — authority digest + evidence.
3. `reports/dlh_5vg_asymptotic_endpoint_approximation_2026_09_11/DLH_5VG_FIXED_ASPECT_REFINEMENT_AND_LAYER_GEOMETRY.md` — family, scaling identities, layer geometry, structural facts F1–F4.
4. `reports/dlh_5vg_asymptotic_endpoint_approximation_2026_09_11/DLH_5VG_BUFFERED_ADMISSIBILITY_AND_MOMENT_CONSISTENCY.md` — A1 buffer, case analysis, cone equalities, exact moments, tangent-cone consistency T1–T4, seam T8.
5. `reports/dlh_5vg_asymptotic_endpoint_approximation_2026_09_11/DLH_5VG_MONOTONICITY_CONSERVATION_SAME_Q_AND_OPERATOR_CONSISTENCY.md` — scaling T5, operator consistency T6, monotonicity/conservation/one-Q T7, interpretation ceiling.
6. `reports/dlh_5vg_asymptotic_endpoint_approximation_2026_09_11/DLH_5VG_TERMINAL_AND_FORBIDDEN_CHECK.md` — single terminal (Outcome A) + forbidden-operation check + fresh state report.
