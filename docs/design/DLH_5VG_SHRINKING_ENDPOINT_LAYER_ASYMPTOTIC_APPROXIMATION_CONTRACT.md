# DLH-5V-G — Shrinking Endpoint-Layer Asymptotic Same-Process Approximation (Umbrella Design)

**Issue:** deep-learning-hank #55 (DLH-5V-G) · **Task type:** `SCIENTIFIC_DESIGN__SHRINKING_ENDPOINT_LAYER_ASYMPTOTIC_MARKOV_APPROXIMATION`
**Branch:** `dsh/issue-55-dlh-5vg-asymptotic-endpoint-approximation-2026-09-11` · **Activation:** comments `5634144909` (+ refresh `5634171277`)
(`DLH_5VG_ROUTE_A_SHRINKING_ENDPOINT_LAYER_ASYMPTOTIC_APPROXIMATION_AUTHORIZED`), final CURRENT sync `origin/main` = `c8c5c3f8d3a002a7efcb93682ff42d50c3667602`
**Status:** bounded reanalysis of reviewer comment `5634957294` (verdict `DLH_5VG_OUTCOME_A_NOT_ACCEPTED__A1_TANGENT_CONE_GRAPH_CONSISTENCY_COUNTEREXAMPLE__BOUNDED_REANALYSIS_REQUIRED`). The reviewer's counterexample is confirmed and generalized; no permitted Route-A A1 variant and no permitted A2 repair can satisfy the exact Issue-#55 tangent-cone graph-consistency requirements. **Outcome C — bounded Route-A obstruction**, submitted for fresh ChatGPT review, **NOT scientific acceptance**. Owner decision: `APPROVE_DLH_5VG_ROUTE_A_ASYMPTOTIC_ENDPOINT_APPROXIMATION_DESIGN_GATE`.

## 1. Frozen inputs (accepted — consumed, not reopened)

- Accepted DLH-5V-F obstruction (controlling): at exact-frontier `r_j = 0` top states every represented destination has
  `Delta W <= 0`; exact `mu_W = 0` with nonnegative rates requires same-W destinations only; native same-W displacements
  satisfy `10 Delta j + 7 Delta i = 0` and are multiples of `(7,-10)`; lower endpoint bands can miss `(-7,+10)` and upper
  bands can miss `(+7,-10)`. Lattice/discretization obstruction, not a household-source failure. Not reopened.
- Accepted household source immutable, blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e` verified.
- Domain `D_W(W_max) = {0 <= a <= a_max, b >= b_min, a+b <= W_max}`, `a_max = 10`, `b_min = -2`, no numerical `W_max`.
- Symbolic fixed-aspect refinement family (`m = 1,2,...`): `da_m = 10/(19m)`, `db_m = 7/(19m)`, `a_j = j*10/(19m)`,
  `b_i = b_min + i*7/(19m)`, `N_m = floor(19m*(W_max-b_min))`, represented nodes `10j + 7i <= N_m`.
- Accepted regular contracts (DLH-5V-A..E) remain exact and frozen; wide stencils; deferred endpoint complement
  `j in {0..6}`, `j in {19m-6..19m}`, `i in {0..9}` + W-active endpoint cells. The regular block is NOT reopened.
- Accepted sector formulas (level-`m` instances): `w_left = (-10/(19m), 0)`, `w_down = (0, -7/(19m))`,
  `w_T = (-70/(19m), +70/(19m))`, `w_RT = (+70/(19m), -70/(19m))`; `R_reverse` (`q_RT = 19m*mu_a/70`,
  `q_down = 19m*(-mu_W)/7`), `T_realloc` (`q_T = 19m*mu_b/70`, `q_in = 19m*(-mu_W)/10`), `R_deplete`
  (`q_left = 19m*(-mu_a)/10`, `q_down = 19m*(-mu_b)/7`).

## 2. What still passes (finite-m algebra inside A1-admitted cones)

The reviewer confirmed the finite-`m` algebra is coherent. Corrected and retained:

- **A1 buffer (before scoring):** `(BA1) j <= 6 => mu_a >= 0`; `(BA2) j >= 19m-6 => mu_a <= 0`;
  `(BA3) i <= 9 => mu_b >= 0`; `(BA4) W-active => mu_W <= 0`.
- **Case L** (lower-a, W-active, `i >= 10`): `{mu_a >= 0, mu_W <= 0} = cone{w_RT, w_down}` with `q_RT = 19m*mu_a/70`,
  `q_down = 19m*(-mu_W)/7`; exact moment.
- **Case U** (upper-a, W-active, `i >= 10`): `{mu_a <= 0, mu_W <= 0} = cone{w_left, w_down, w_T}`; T_realloc/deplete
  split; exact moment.
- **Case B** (lower-b, W-active, `i <= 9`, `j >= 19m-7`): buffered cone `{mu_b >= 0, mu_W <= 0} =
  {mu_a <= 0, mu_b >= 0, mu_W <= 0} = cone{w_left, w_T}` with `q_T = 19m*mu_b/70`, `q_in = 19m*(-mu_W)/10`; exact moment.
- **Interior layer cells:** buffered cone is a half-plane/full-plane subset of the accepted 3/4-neighbor cone, exactly
  representable (equality at face-adjacent positions).
- **Scaling (proved):** jump `O(1/m)`, rate `O(m)`, `sum q|w|^2 = O(1/m)` with explicit constants; conservative rows,
  `Q_ss = -sum of actual outgoing rates`, `Q_m 1 = 0`; one-Q semantics. All retained.
- **Corner semantics corrected (reviewer item 6):** see §6.

## 3. The controlling failure — tangent-cone graph consistency (T3/T4 as submitted is FALSE)

### 3.1 Reviewer counterexample (confirmed; mandatory test)

Take the non-W-active lower-a state `s_m = (0, i_t^m(0) - 2)` (`i_t(j) = floor((N_m - 10j)/7)`). It is represented,
satisfies `i <= i_t - 2` (interior, not W-active), and

```text
a_m = 0,
W_max - b_{i_m} = (theta_m + r_0^m + 14)/(19m) -> 0,   r_0^m = N_m mod 7,
```

so `x_m -> (0, W_max)` — the true `a = 0 x W` corner. Under A1: BA1 applies (`mu_a >= 0`), BA4 does **not** (not
W-active). The drift `mu = (0, +1)` is A1-admitted and exactly represented by the native `w_up = (0, 7/(19m))` transition
to `(0, i_m + 1)` (represented) with `q_up = 19m/7 >= 0`. But at `(0, W_max)` the true tangent cone is
`{mu_a >= 0, mu_W <= 0}`, and `mu = (0, +1)` has `mu_W = +1 > 0`. Hence the **outer/limsup** statement fails:

```text
limsup admitted discrete drift graph  NOT subset of  true tangent-cone graph at the corner.
```

Verified numerically over `m in {1,2,5,20,100}` (exact rational arithmetic; `W-dist` from 0.789 down to 0.008, `q_up = 19m/7`).

### 3.2 Generalization — unbounded family of corner-convergent non-W-active cells

For **every fixed `j`** (and for every `j_m = o(m)`), `s_m = (j, i_t^m(j) - 2)` satisfies `a_m = 10j/(19m) -> 0` and
`W_max - (a_m + b_{i_m}) = (r_j^m + theta_m + 14)/(19m) -> 0`, so `x_m -> (0, W_max)`. These cells are interior
(non-W-active) for all `m`. In particular `j = 7` (and `j = 8, ..., 12, 30, ...`) lie in the **accepted regular region**
(`7 <= j <= 19m-7`, `i >= 10`), where the frozen accepted interior process is full-plane: `mu = (0, +1)` is admitted
there too. **The frozen accepted regular/interior contract itself therefore violates the global outer/limsup condition at
`(0, W_max)`** — the failure is not caused by the endpoint buffer and cannot be repaired by any endpoint-layer-only
modification without reopening the frozen regular block (forbidden).

The same mechanism occurs at the upper W-corner `(a_max, W_max - a_max)`: `s_m = (19m, i_t^m(19m) - 2)` is non-W-active,
`x_m -> (a_max, W_max - a_max)`, BA2 applies but BA4 does not; `mu = (-1, +2)` (exact via `w_left` + `w_up`) has
`mu_W = +1 > 0 notin {mu_a <= 0, mu_W <= 0}` — outer fails.

### 3.3 Impossibility — no per-state numerical rule can satisfy both graph conditions

Let `A_m(s)` be any per-state admissible-set rule. Partition the convergent non-W-active sequences into:

- **Family C** (corner/W-face limits): `W-dist(s_m) -> 0`, i.e. `k_m := i_t(j_m) - i_m = o(m)` (growing rows below the
  W-active top, physical W-distance still tending to zero);
- **Family F** (face-interior limits): `W-dist(s_m) -> c > 0`, i.e. `k_m ~ 7cm/19` (linearly many rows below the top).

Outer at `(0, W_max)` (and at every W-face point) requires the W-constraint `mu_W <= 0` to hold **eventually on every
Family-C sequence**; liminf at every face-interior point `(0, b_*)` with `W-dist = c > 0` requires **no** W-constraint
eventually on every Family-F sequence converging to it (the true cone there is `{mu_a >= 0}`, full `b`-freedom).

Any per-state rule distinguishes states by level-`m` data only, and Families C and F are indistinguishable per-state:
- a **fixed row-count rule** `k <= K`: escaped by Family-C sequences with `k_m = sqrt(m*K) > K` (still `k_m/m -> 0`,
  `W-dist -> 0`) — outer fails;
- a **shrinking W-distance rule** `W-dist < delta_m`, `delta_m -> 0`: escaped by Family-C sequences with
  `k_m = m/f(m)`, `f(m) -> oo` arbitrarily slowly (`W-dist = 7/(19 f(m)) -> 0` slower than any fixed `delta_m`) — outer fails;
- a **fixed W-distance rule** `W-dist < delta > 0`: catches all Family-C sequences (outer ok), but over-constrains every
  Family-F sequence with `c < delta` — liminf fails at `(0, b_*)` with `W-dist = c < delta`;
- the **W-activity rule** (BA4 on W-active cells only) misses **all** non-W-active Family-C sequences (reviewer's
  counterexample is of this type) — outer fails.

Hence **no per-state admissible-set rule can satisfy the exact Issue-#55 outer/limsup and recovery/liminf graph
conditions simultaneously**. The tangent-cone multifunction `x -> T(x)` is discontinuous at the boundary (full plane at
interior points, half-planes at faces, corners at intersections), and the grid provides dense interior approximations of
every boundary point; the two conditions force the discrete admissible sets to converge to `T` in the Kuratowski sense,
which the grid's geometry cannot realize per-state.

### 3.4 Consequence

The submitted statement "the buffered cone at every layer state equals the true tangent cone at its limit point" cannot
stand: for non-W-active layer states with `W-dist -> 0` the buffered cone (no BA4) is strictly larger than the true cone
at the corner limit, and no correction within Route A's frozen scope fixes this. **A1 fails the controlling graph
consistency requirement.** The DLH-5V-F finite-m obstruction is thus NOT removable by a shrinking numerical
candidate-admissibility buffer of the permitted kind: the buffer either fails the outer condition (as submitted) or,
when strengthened to catch all corner-convergent cells, breaks recovery at face-interior limits (liminf), and the global
condition additionally fails on the frozen regular block (§3.2).

## 4. A2 cannot repair the admissible-set failure (reviewer item 4)

A2 (Issue §5) replaces the exact-moment requirement by an explicit first-moment defect `e_m(s,u)` with a declared error
object and a proved vanishing operator/boundary-layer consistency statement. It does **not** change the admissible-set
rule: the counterexample drift `mu = (0, +1)` at `(0, i_t(0) - 2)` remains continuously admissible at the node position
(the node is strictly inside `D_W` in the W-direction), and remains exactly representable (`q_up = 19m/7`) — the moment
defect is zero for it, so no defect term can exclude it. The admissible-set outer/limsup failure at the corner is
therefore not repaired by any permitted A2 moment-defect construction. (This matches the reviewer's explicit note: a
first-moment defect alone does not automatically repair an admissible-set outer/limsup failure; here it provably cannot.)

## 5. Conclusion — bounded Route-A obstruction (Outcome C)

No permitted Route-A contract (A1 or A2) can meet the exact Issue-#55 tangent-cone graph-consistency requirements under
the frozen state/grid family:

- (O1) the reviewer's counterexample sequence `(0, i_t(0) - 2)`, `mu = (0,1)` violates outer/limsup at `(0, W_max)`;
- (O2) the mechanism is unbounded (all `j = o(m)` cells) and hits the frozen regular block (`j = 7`, ...), so it cannot
  be repaired by endpoint-layer changes without reopening the frozen accepted regular contract;
- (O3) no per-state admissible-set rule can satisfy both outer/limsup and recovery/liminf (§3.3);
- (O4) A2 cannot repair the admissible-set failure (§4).

The finite-m algebra (rates, moments, scaling, monotonicity, conservation, one-Q) remains valid but does not rescue the
asymptotic theorem. The terminal is the exact Outcome-C terminal:

```text
DLH_5VG_ROUTE_A_ASYMPTOTIC_ENDPOINT_APPROXIMATION_OBSTRUCTION__OWNER_ROUTE_REDECISION_REQUIRED
```

## 6. DLH-5T corner semantics correction (reviewer item 6)

Corrected true tangent cones at the Regime-I corners:

```text
(0, W_max):                       a = 0 x W:            {mu_a >= 0, mu_W <= 0}
(a_max, W_max - a_max):           a_max x W:            {mu_a <= 0, mu_W <= 0}
(a_max, b_min), W_max > 8:        a_max x b_min only:   {mu_a <= 0, mu_b >= 0}   (W NOT active: a_max + b_min = 8 < W_max)
(a_max, b_min), W_max = 8:        triple corner:        {mu_a <= 0, mu_b >= 0, mu_W <= 0}
(0, b_min):                       a = 0 x b_min:        {mu_a >= 0, mu_b >= 0}   (W NOT active: b_min < W_max)
```

For **fixed `W_max > 8`**, W-active lower-b-layer cells disappear for sufficiently large `m`: a W-active cell with
`b <= b_min + 63/(19m)` satisfies `a >= W_max - b_min - (r + theta + 63)/(19m) = (W_max + 2) - O(1/m) > a_max = 10` for
`m > 69/(19(W_max - 8))`, contradicting `a <= a_max`. Only at `W_max = 8` can an infinite W-active lower-b sequence
converge to the triple corner. For `W_max > 8`, the lower-b layer cells are non-W-active interior cells for large `m`;
their buffered cone `{mu_a <= 0, mu_b >= 0}` (BA2 + BA3) equals the true `a_max x b_min` corner cone there — that corner
is graph-consistent (no W constraint is needed or claimed). The obstruction is at the **W-corners** `(0, W_max)` and
`(a_max, W_max - a_max)` only.

## 7. Interior-layer / corner taxonomy correction (reviewer item 6)

- W-active layer cells: converge to W-face points; at fixed `j` (or `j = o(m)`) with `W-dist -> 0` they converge to the
  corners `(0, W_max)` / `(a_max, W_max - a_max)`; at `j ~ alpha m`, `alpha in (0, 19)` they converge to interior W-face
  points. (Buffered cone = true cone: consistent.)
- Non-W-active layer cells with bounded `k = i_t - i`: `W-dist = (7k + r + theta)/(19m) -> 0` — they converge to
  **corners**, not face interiors (the previous package statement was false).
- Non-W-active layer cells with `k ~ alpha m`, `alpha > 0`: `W-dist -> 7 alpha/19 > 0` — face-interior limits; the true
  cone there has full `b`-freedom (e.g. `{mu_a >= 0}` at `(0, b_*)`).
- Non-W-active cells with `k = o(m)` but `k -> oo`: corner limits with `W-dist -> 0` — the Family-C obstruction class.

## 8. Interpretation ceiling (design only)

Outcome C is a bounded scientific obstruction: the exact Issue-#55 graph-consistency requirements cannot be met by any
permitted Route-A contract under the frozen state/grid family. It does NOT authorize: source/economic mutation;
production grid/aspect/domain redesign; state augmentation; coordinate transformation; numerical production `W_max`;
implementation or solver-source mutation; production `Q` assembly/run; HJB/KFE/stationary solves (stationary KFE
remains NOT AUTHORIZED); numerical production experiments; aggregates/GE/regional/neural/nominal/calibration/policy/
welfare/Results; PR/merge/close/successor/self-accept. The verification used tiny exact `%TEMP%` scripts only; the
controlling arguments are analytic in `m`.

## 9. File map (exact six-file allowlist, edited on the same dedicated branch)

1. This umbrella design document.
2. `reports/dlh_5vg_asymptotic_endpoint_approximation_2026_09_11/DLH_5VG_AUTHORITY_CAPSULE.md`
3. `reports/dlh_5vg_asymptotic_endpoint_approximation_2026_09_11/DLH_5VG_FIXED_ASPECT_REFINEMENT_AND_LAYER_GEOMETRY.md`
4. `reports/dlh_5vg_asymptotic_endpoint_approximation_2026_09_11/DLH_5VG_BUFFERED_ADMISSIBILITY_AND_MOMENT_CONSISTENCY.md`
5. `reports/dlh_5vg_asymptotic_endpoint_approximation_2026_09_11/DLH_5VG_MONOTONICITY_CONSERVATION_SAME_Q_AND_OPERATOR_CONSISTENCY.md`
6. `reports/dlh_5vg_asymptotic_endpoint_approximation_2026_09_11/DLH_5VG_TERMINAL_AND_FORBIDDEN_CHECK.md`
