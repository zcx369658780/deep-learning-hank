# DLH-5V-F — Endpoint-Band and Joint-Boundary Finite-Process Closure (Issue #54)

**Issue #54 — OPEN.** `SCIENTIFIC_DESIGN__ENDPOINT_BAND_AND_JOINT_BOUNDARY_FINITE_PROCESS_CLOSURE`
**Branch:** `dsh/issue-54-dlh-5vf-endpoint-joint-boundary-2026-09-11`
**Activation comments:** `5632596303` (authoritative activation) + `5632615142` (final CURRENT sync; fresh main `cff55e7a75a7bb76d3186bc218233dff0c672d95`)
**Owner decision:** `APPROVE_DLH_5VF_ENDPOINT_BAND_AND_JOINT_BOUNDARY_FINITE_PROCESS_CLOSURE_GATE`

**Status: DESIGN / PROVENANCE ONLY.** No source mutation, no implementation, no
HJB/KFE/stationary execution, no numerical `W_max`, no PR/merge/close/successor/
self-accept.

---

## 1. Controlling accepted authority

- Fresh live `main` at this gate: `cff55e7a75a7bb76d3186bc218233dff0c672d95`
  (verified by DSH fresh-fetch before any mutation; Issue #54 already activated in the
  three CURRENT governance files at this commit).
- Immediately prior accepted gate: Issue #53 / DLH-5V-E (candidate `98872fe…`,
  acceptance `5632150936`, integration `28e42e4c…`, terminal
  `DLH_5VE_FULL_REGULAR_W_BOUNDARY_SECTOR_CONTRACT_FROZEN__READY_FOR_ENDPOINT_JOINT_BOUNDARY_GATE`).
- Accepted household source (immutable/read-only):
  `src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`, blob
  `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e` (re-verified at this gate).
- Binding Issue #27 law: `HJB boundary policy <=> KFE boundary transition law`.
- Stationary KFE remains **NOT AUTHORIZED** in this Issue.

## 2. Frozen finite production domain and grid (from DLH-5T / DLH-5V-A)

```text
D_W(W_max) = { (a,b,z) : 0 <= a <= a_max, b >= b_min, a + b <= W_max, z in {z0,z1} }
b_min = -2,  a_max = 10
grid: a_j = j*(10/19), j = 0..19 (j_max = 19);  b_i = b_min + i*(7/19), i >= 0
nodes: 10*j + 7*i <= N,   N = floor(19*(W_max - b_min)) = floor(kappa), kappa = N + theta
displacement: Delta x_sr = ((10/19)*Delta j, (7/19)*Delta i)
```

Independent upper-a authority `a_max = 10`, `j_max = 19` (DLH-5V-E micro-rev). No
numerical `W_max` is selected; the family is symbolic.

## 3. Frozen economic boundary laws (from DLH-5T)

Active-face tangent cones, applied jointly at feasible intersections:

```text
a = 0:          mu_a >= 0
b = b_min:      mu_b >= 0
a = a_max:      mu_a <= 0
a + b = W_max:  mu_W = mu_a + mu_b <= 0
```

Existence conditions (DLH-5T):
- `a=0 x W` corner `(0, W_max)` exists for every `W_max >= b_min`;
- `a=a_max x W` corner `(a_max, W_max - a_max)` exists iff Regime I
  (`W_max >= a_max + b_min = 8`, i.e. `N >= 190`);
- `b=b_min x W` corner `(W_max - b_min, b_min)` exists iff Regime II
  (`b_min <= W_max < 8`, i.e. `N < 190`); on the grid it is a node only when
  `N = 10 j` for some `j`.
The symbolic family studied here (regular W-region nonempty, `N >= 190`) is Regime I;
the `b=b_min`-face W-cells are then confined to `(j, 0)` with `10 j = N` (i.e.
`N in {190, 191, ..., 199}` gives the single triple-corner cell `(19, 0)`).

## 4. Deferred complement (from DLH-5V-E) and the critical distinction

Deferred W-active states = W-active cells with `j in {0..6}`, `j in {13..19}`, or
`i <= 9`. Regular region: `7 <= j <= 12` and `i >= 10` (accepted DLH-5V-E).

**Reachability bands are not economic faces** (activation comment, binding):

```text
j = 0 only      => actual a = 0 face
j = 1..6        => lower-a reachability band but a-interior
j = 19 only     => actual a = a_max face
j = 13..18      => upper-a reachability band but a-interior
i = 0 only      => actual b = b_min face
i = 1..9        => lower-b reachability band but b-interior
```

For a W-active cell in an a-interior or b-interior band, the only active economic
constraint is the `W` face, so the continuous admissible drift cone is exactly
`T_W = { mu_W <= 0 }` (the full accepted W tangent cone). This is what makes the
endpoint bands hard: an economic face (which would cut off the missing direction)
is **not** active there.

## 5. Exact W-tangent lattice identity and same-W generation

```text
10 Delta j + 7 Delta i = 0   (gcd(10,7) = 1)
```

Primitive same-W native-grid displacements are `(-7, +10)` (forward) and `(+7, -10)`
(mirror); all same-W displacements are integer multiples `k*(+7, -10)` (and their
negatives). Availability conditions (destination must be a represented node):

```text
forward  (j - 7, i + 10):  j >= 7                      (else a_dest < 0)
mirror   (j + 7, i - 10):  j <= 12 AND i >= 10         (else a_dest > a_max or b_dest < b_min)
```

Consequently in the a-interior endpoint bands the **same-W transition in the outward
direction of the missing stencil is off-grid**: forward-wide unavailable at
`j in {1..6}`; mirror-wide unavailable at `j in {13..18}` (and at `i <= 9`).

## 6. State-class / active-cone taxonomy (summary; full table in the taxonomy report)

Every deferred W-active cell is classified by (i) economic active set, (ii)
reachability band, (iii) `r_j = (N - 10 j) mod 7` (W residual), (iv) top vs sub-top
(`i_t(j) = floor((N - 10 j)/7)`; top always W-active; sub-top W-active iff
`r_j in {0,1,2}`). An **exact-frontier top cell** has `r_j = 0`, i.e. its W-index
`10 j + 7 i_t(j) = N` exactly.

Deferred classes and their outcome:

| Class | Active set | Continuous admissible cone | Result |
|---|---|---|---|
| `j = 0` (top, sub-top) | `{a=0, W}` | `{mu_a >= 0, mu_W <= 0}` | **Closable** (reverse sector) |
| `j in {1..6}` top, `r_j = 0` | `{W}` | `T_W` | **Obstruction** (forward-sliding) |
| `j in {1..6}` top, `j=1 & r_1 in {1,2,3}` | `{W}` | `T_W` | **Obstruction** (forward-sliding) |
| `j in {1..6}` other top / sub-top | `{W}` | `T_W` | Exact-tangent representable (constructive) |
| `j = 19` (top, sub-top) | `{a=a_max, W}` | `{mu_a <= 0, mu_W <= 0}` | **Closable** (forward + deplete) |
| `j in {13..18}` top, `r_j = 0` | `{W}` | `T_W` | **Obstruction** (reverse-sliding) |
| `j in {13..18}` top, no-helper `r_j in {1,2}` | `{W}` | `T_W` | **Obstruction** (reverse-sliding) |
| `j in {13..18}` other top / sub-top | `{W}` | `T_W` | Exact-tangent representable (constructive) |
| `(19,0)` b-min triple corner (`N in {190..199}`) | `{a=a_max, b=b_min, W}` | `{mu_a<=0, mu_b>=0}` | **Closable** (T_realloc) |

## 7. Moment-cone audit and obstruction certificate (summary; full proof in the audit report)

Let `C_rep(s)` be the nonnegative first-moment cone generated by **all** represented
native-grid destinations of state `s` (every actual in-domain node; accepted
local/wide transitions and any alternative native-grid displacement — no ghosts, no
interpolation). The continuous admissible cone at a `{W}`-only state is `T_W`.

**Certificate (exact-frontier top cells, `r_j = 0`).** From a cell with index exactly
`N`, every represented destination has `10 Delta j + 7 Delta i <= 0`, and `= 0` only
for same-W lattice displacements. Therefore any nonnegative combination with
`mu_W = 0` may use **only** same-W destinations. At `j in {1..6}` the only available
same-W rays are mirror rays (all with `Delta b < 0`), so `mu_b <= 0`: the
continuously admissible exact W-tangent **forward-sliding ray**
`{(-u, +u), u > 0}` (`mu_W = 0`, `mu_b = +u > 0`, admissible since only `W` is
active) is **not** in `C_rep`. Symmetrically at `j in {13..18}` the only available
same-W rays are forward rays (all with `Delta a < 0`), so the **reverse-sliding ray**
`{(+u, -u), u > 0}` is **not** in `C_rep`. This is a finite-process representability
**obstruction**.

**Universality.** An exact-frontier top cell exists in a deferred a-interior band for
every symbolic `N`:
- residues `N mod 7 in {1,2,3,4,5,6}`: lower band, `j = (5 N) mod 7 in {1..6}` has
  `r_j = 0`; its forward-sliding ray is unrepresentable;
- residue `N mod 7 = 0`: upper band `j = 14` has `r_14 = 0`; its reverse-sliding ray
  is unrepresentable.
Exact enumeration over `N in [190, 260]` (all seven residues, both bands) confirms
the certificate property cell-by-cell (see audit report §7).

**Additional exact obstruction classes** (same certificate, dominance argument):
lower-band top cells `j = 1` with `r_1 in {1,2,3}`; upper-band top cells with
`r_j in {1,2}` in the no-helper subset (exact cells per residue in the audit report).
These are reported for completeness; the `r_j = 0` classes already force the
terminal.

**Smallest responsible class and frozen assumption.** The smallest exact class is a
single exact-frontier W-active top cell `(j, i_t(j))` with `j in {1..6}` or
`j in {13..18}` (each exists for a generic symbolic `N`), with admissible drift the
exact W-tangent sliding ray of the unavailable orientation. The obstruction is caused
by the frozen grid/domain placing the corresponding primitive same-W destination
off-grid (forward needs `j >= 7`, mirror needs `j <= 12` and `i >= 10`), while the
frozen exact same-process contract (i) admits only actual represented native-grid
destinations (no ghost/interpolation), and (ii) requires exact first-moment equality
(`mu_W = 0` for tangent motion, no inward-normal injection). Every non-tangent
represented destination strictly decreases `W` at an exact-frontier cell, so no
nonnegative combination can cancel back to `mu_W = 0` in the missing orientation.

## 8. Closable endpoint classes and their exact contracts (summary; full in scoring report)

For every closable deferred class the continuous admissible cone equals the
nonnegative cone of accepted sector transitions, with rates identical to the regular
region (seam-consistent by formula):

```text
reverse sector   (j = 0, a=0 x W):   q_RT = 19*mu_a/70,   q_down = 19*(-mu_W)/7      on (w_RT, w_down)
T_realloc sector (i=0 b-min face, (19,0)): q_in = 19*(-mu_W)/10, q_T = 19*mu_b/70    on (w_left, w_T)
j = 19 (a_max x W):  mu_b >= 0 -> T_realloc rates;  mu_b < 0 -> deplete rates
                     (q_left = 19*(-mu_a)/10, q_down = 19*(-mu_b)/7) on (w_left, w_down, w_T)
```

At these classes the joint KKT multiplier on the economic face cuts off exactly the
drift region that the missing wide stencil would otherwise be needed for
(`mu_a <= 0` at `a = a_max`, `mu_a >= 0` at `a = 0`, `mu_b >= 0` at `b = b_min`), so
the closure is exact and the regular-to-endpoint seams (j=0<->7, j=12<->19, b-min
face) are continuous by formula.

## 9. Same-process / one-Q law at the design level

Where a deferred class is closable, candidate controls are scored by the discrete
`H_h` with **candidate-specific** represented nonnegative rates **before** one global
statewise argmax (accepted DLH-5V-E semantics); each row is conservative by
construction (actual destinations only, outgoing rates only), and there is **one**
selected backward generator `Q` whose rows are those rows; the future exact KFE
handoff consumes exactly `Q^T`. No second boundary process, no KFE-only repair.

For the unclosable classes, no coherent nonnegative represented rate/scoring
contract exists (certificate §7), so the global argmax / one-Q law is **not
well-defined there**: this is the content of the obstruction and is exactly why a
route decision is required. **No clipping, no hidden leakage, no ghost/virtual state,
no inward-normal first-moment injection** is applied in this Issue.

## 10. Decision

The deferred complement is **not** closable under the frozen grid/domain/exact
same-process contract: at least one continuously admissible deferred-state drift
class (the exact W-tangent sliding rays at exact-frontier a-interior top cells, which
exist for every symbolic `N`) cannot be represented by any nonnegative combination of
actual allowed native-grid destinations. The scientific result is a sharply bounded
representability obstruction certificate, not a repair. The terminal is therefore:

```text
DLH_5VF_ENDPOINT_JOINT_BOUNDARY_FINITE_PROCESS_OBSTRUCTION__OWNER_ROUTE_DECISION_REQUIRED
```

Route options (grid/domain extension, explicit approximation-contract change, or
Owner-accepted boundary-law modification) are deliberately **not designed in this
Issue**; the Issue requires the Builder to stop at the certificate for Owner route
decision.

## 11. Interpretation ceiling

This result does NOT establish: implemented boundary-HJB correctness; global
discrete-HJB correctness; numerical `W_max` adequacy; SCC / closed recurrent-class
structure; stationary existence/uniqueness; stationary KFE authorization; stationary
aggregates; GE / regional / neural / nominal / calibration / policy / welfare /
Results. The closable-class contracts are design-level only.

## 12. Context budget

Scientific reading was limited to the Issue #54 budget:
1. `docs/design/DLH_5VE_REMAINING_REGULAR_W_BOUNDARY_SECTOR_CLOSURE.md` (in context);
2. `docs/design/DLH_5T_FINITE_PRODUCTION_DOMAIN_AND_SAME_PROCESS_BOUNDARY_CONTRACT.md`;
3. `reports/dlh_5t_finite_production_domain_same_process_boundary_2026_09_03/DLH_5T_HJB_KKT_BOUNDARY_LAWS.md`;
4. `docs/design/DLH_5VA_REGULAR_VORONOI_FRONTIER_PHASE_AND_ADJACENCY.md` only as
   needed for W-active phase/class identity (accepted formulas in context).
Household blob re-verified only. Tiny exact rational/enumeration spot-checks only
(`%TEMP%`, never committed).

## 13. Completion

Six allowlist files only, staged explicitly, committed and pushed on the dedicated
branch, remote SHA verified equal to local SHA, single terminal posted, STOP for
fresh ChatGPT review. See `DLH_5VF_TERMINAL_AND_FORBIDDEN_CHECK.md`.
