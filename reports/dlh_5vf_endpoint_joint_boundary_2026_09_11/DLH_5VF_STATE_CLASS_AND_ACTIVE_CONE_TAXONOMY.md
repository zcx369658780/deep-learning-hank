# DLH-5V-F — State-Class and Active-Cone Taxonomy (Issue #54)

Companion report 2 of 5. Classifies **every** deferred W-active state by economic
active-set identity separately from transition reachability, states exact existence
conditions, and records the continuous admissible drift cone per class. No rates are
derived here (see the moment-cone audit and the scoring/one-Q report).

---

## 1. Frozen objects and notation

```text
D_W: 0 <= a <= a_max, b >= b_min, a + b <= W_max;   b_min = -2, a_max = 10
grid: a_j = j*(10/19), j in {0..19};  b_i = b_min + i*(7/19), i >= 0
nodes: 10 j + 7 i <= N;  N = floor(19 (W_max - b_min)), kappa = N + theta, theta in [0,1)
class j:  i_t(j) = floor((N - 10 j)/7),  r_j = (N - 10 j) mod 7,  period 7
W-index of a cell:  W_idx(j,i) = 10 j + 7 i   ( = 19 (a + b - b_min) )
```

Accepted W-active phase facts (DLH-5V-A): the top cell `(j, i_t(j))` of every class
`j in {0..19}` is W-active (its Voronoi cell touches `a + b = W_max`); the sub-top
cell `(j, i_t(j) - 1)` is W-active iff `r_j in {0,1,2}` and `i_t(j) >= 2`.
`i_t(j+7) = i_t(j) - 10`. An **exact-frontier top cell** is a top cell with `r_j = 0`
(`W_idx = N` exactly).

## 2. Economic faces versus reachability bands (binding distinction)

| Grid condition | Economic status | Boundary law |
|---|---|---|
| `j = 0` | actual `a = 0` face | `mu_a >= 0` |
| `j = 19` | actual `a = a_max` face | `mu_a <= 0` |
| `i = 0` | actual `b = b_min` face | `mu_b >= 0` |
| W-active cell | actual `W` face | `mu_W <= 0` |
| `j in {1..6}` | lower-a reachability band, **a-interior** | no a-face law |
| `j in {13..18}` | upper-a reachability band, **a-interior** | no a-face law |
| `i in {1..9}` | lower-b reachability band, **b-interior** | no b-face law |

Consequence (used throughout): a deferred W-active cell whose economic faces are only
`{W}` has continuous admissible cone exactly `T_W = { mu_W <= 0 }` — the full tangent
cone, with **no** economic-face cut that could remove the drift direction belonging to
the missing wide stencil.

## 3. Existence conditions (symbolic family, Regime I: `W_max >= 8`, `N >= 190`)

Regular region nonempty requires `i_t(12) = (N - 120)/7 >= 10`, i.e. `N >= 190`.

- `j = 0` top always exists (`i_t(0) = floor(N/7) >= 27`); sub-top exists iff
  `r_0 = N mod 7 in {0,1,2}`.
- `j = 19` top exists (Regime I) with `i_t(19) = (N - 190)/7 >= 0`; sub-top iff
  `r_19 = (N - 190) mod 7 in {0,1,2}` and `i_t(19) >= 2`.
- `j in {1..6}`: cells exist with `i_t(j) >= 19` (hence b-interior) for `N >= 190`.
- `j in {13..18}`: cells exist with `i_t(j) >= 1` (b-interior) for `N >= 190`
  (`i_t(18) = (N - 180)/7 >= 1`).
- Lower-b band `i <= 9` on the frontier: W-active cells exist iff
  `i_t(19) = (N-190)/7 <= 9`, i.e. `N <= 259`; for `N >= 190` these cells are exactly
  the class-`13..19` top/sub-top cells of rows 7–12 below (the `i <= 9` band is a
  reachability label, not an economic class — the taxonomy rows are mutually
  exclusive and cover all of these cells). The only `b = b_min` W-active cell is
  `(19, 0)`, and it is W-active exactly when it is the class-19 **top** cell:
  `i_t(19) = 0`, i.e. `N in {190..196}`. (For `N in {197..203}` it is the class-19
  sub-top with `i_t(19) = 1 < 2`, which the accepted sub-top W-activity condition
  excludes; for `N >= 204` it is not a frontier-phase cell at all.) Continuously,
  the triple corner `a = a_max, b = b_min, W` exists **only** at the boundary case
  `W_max = 8`, i.e. exactly `N = 190` (`theta = 0`); for `N >= 191` the node
  `(19,0)` lies strictly inside the W face, so the W face is not continuously active
  there — the discrete W-activity of the cell is a separate Voronoi-contact status
  (DLH-5V-A phase facts, `theta`-independent beyond `N = floor(kappa)`).
- Exact-frontier top cells: `r_j = 0` iff `j == (5 N) mod 7`. In the deferred
  a-interior bands:
  - lower band: `(5 N) mod 7 in {1..6}` (i.e. `N mod 7 != 0`) gives `j in {1..6}`;
  - upper band: `(5 N) mod 7 in {6,0,1,2,3,4}` intersected with `{13..18}` gives
    `j = 13` (res 6), `14` (res 0), `15` (res 1), `16` (res 2), `17` (res 3),
    `18` (res 4); residue 5 (`(5 N) mod 7 = 5`) gives no upper-band exact-frontier
    cell (it lands at the regular `j = 12` or the face `j = 19`).

## 4. Joint active-face cones at feasible intersections (from DLH-5T)

```text
a=0 x W           (j = 0 top/sub-top):            { mu_a >= 0, mu_W <= 0 }
a=a_max x W       (j = 19 top/sub-top, i >= 1):   { mu_a <= 0, mu_W <= 0 }
a=0 x b=b_min     (not W-active for N >= 190;     { mu_a >= 0, mu_b >= 0 }
                  exists only in degenerate cases)
a=a_max x b=b_min ((19,0) node, N >= 190):        { mu_a <= 0, mu_b >= 0 }
```

The W face is additionally continuously active at `(19,0)` **only** in the boundary
case `W_max = 8` (exactly `N = 190`, `theta = 0`), giving
`{ mu_a <= 0, mu_b >= 0, mu_W <= 0 }` there. Note that `{ mu_a <= 0, mu_b >= 0 }`
does **not** imply `mu_W <= 0` (e.g. `(mu_a, mu_b) = (-1, +3)`); the
`mu_W <= 0` leg at `(19,0)` for all `N in {190..196}` comes from the **discrete
W-activity** of the cell: the frozen W-boundary design treats every W-active cell
with the cell-level W-contact constraint `mu_W <= 0`, exactly as in the regular
region where W-active cells carry `T_W` even though their node lies inside the W
face. At `(19,0)` the design cone is therefore
`{ mu_a <= 0, mu_b >= 0, mu_W <= 0 } = cone{w_left, w_T} = T_realloc`.

For `{W}`-only cells the cone is `T_W = { mu_W <= 0 }` (full tangent cone).

## 5. Deferred-class taxonomy table

Notation: `O_L` = forward-sliding obstruction (lower band), `O_U` = reverse-sliding
obstruction (upper band); "repr." = exact-tangent representable by actual represented
destinations (constructive decompositions in the audit report); "closable" = full
continuous admissible cone equals the accepted sector cone (exact contracts in the
scoring report). `r_j` is the W residual; `i >= 1` means b-interior.

| # | State class | Exists iff | Active set | Admissible cone | Result |
|---|---|---|---|---|---|
| 1 | `j=0` top | always | `{a=0, W}` | `{mu_a>=0, mu_W<=0}` | **closable** (reverse) |
| 2 | `j=0` sub-top | `r_0 in {0,1,2}` | `{a=0, W}` | same | **closable** (reverse) |
| 3 | `j in {1..6}` top, `r_j=0` | `(5N) mod 7 = j`, `N mod 7 != 0` | `{W}` | `T_W` | **O_L** |
| 4 | `j=1` top, `r_1 in {1,2,3}` | `N mod 7 in {4,5,6}` | `{W}` | `T_W` | **O_L** |
| 5 | `j in {1..6}` other top | always (per class) | `{W}` | `T_W` | repr. |
| 6 | `j in {1..6}` sub-top | `r_j in {0,1,2}`, `i_t>=2` | `{W}` | `T_W` | repr. |
| 7 | `j=19` top, `i_t(19) >= 1` | `N >= 197` | `{a=a_max, W}` | `{mu_a<=0, mu_W<=0}` | **closable** |
| 8 | `j=19` sub-top | `r_19 in {0,1,2}`, `i_t>=2` | `{a=a_max, W}` | same | **closable** |
| 8b | `(19,0)` = class-19 top, `i_t(19)=0` | `N in {190..196}` | continuous `{a_max, b_min}` (+`{W}` iff `N=190`); discrete W-active | design `{mu_a<=0, mu_b>=0, mu_W<=0}` = T_realloc | **closable** (T_realloc) |
| 9 | `j in {13..18}` top, `r_j=0` | `(5N) mod 7` in upper set (above) | `{W}` | `T_W` | **O_U** |
| 10 | `j in {13..18}` top, no-helper set `{j in {15,16}, r_j=1} u {j in {17,18}, r_j in {1,2}}` | closed-form (helper availability, audit §5) | `{W}` | `T_W` | **O_U** (supplementary) |
| 11 | `j in {13..18}` other top | always (per class) | `{W}` | `T_W` | repr. |
| 12 | `j in {13..18}` sub-top | `r_j in {0,1,2}`, `i_t>=2` | `{W}` | `T_W` | repr. |

Rows 3–4 and 9–10 are the obstruction classes; rows 1–2, 7–8, 8b are exactly
closable; rows 5–6, 11–12 are representable for the exact tangent drift (their full
closed-form candidate contracts are not required for the terminal and are only
constructively evidenced in the audit report — the obstruction already determines the
Outcome). Row 10 is marked supplementary because its obstruction status rests on the
closed-form no-helper certificate **plus** exact cell-by-cell verification over
`N in [190, 260]` (audit §5, §8); it is non-controlling — row 9 (`r_j = 0`) is
closed-form, universal over the `N >= 190` family, and alone forces the terminal.

## 6. Reachability inventory per band (destinations actually represented)

Used by the audit report. From a cell `(j,i)`, a destination `(j',i')` is a
represented native-grid node iff `0 <= j' <= 19`, `i' >= 0`, `10 j' + 7 i' <= N`,
`(j',i') != (j,i)`. The available **accepted** transitions are:

```text
w_left = (-10/19, 0)        iff j >= 1
w_down = (0, -7/19)         iff i >= 1
w_T    = (-70/19, +70/19)   iff j >= 7            (forward wide, (j-7, i+10))
w_RT   = (+70/19, -70/19)   iff j <= 12 and i >= 10  (mirror wide, (j+7, i-10))
```

The audit report additionally enumerates **all** represented destinations (any
alternative native-grid displacement), because the endpoint analysis must not assume
that only the accepted four transitions exist.

## 7. Summary of the classification method

1. Classify by economic active set (Section 2) — faces only where actually active.
2. Enumerate actual represented destinations (Section 6) for each class.
3. Compare the nonnegative first-moment cone of those destinations with the
   continuous admissible cone of Section 4 (audit report).
4. Where exact coverage exists, derive rates and discrete-`H_h` scoring (scoring
   report); where it fails, record the smallest obstruction class (audit report §7).
