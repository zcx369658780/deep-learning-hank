# DLH-5V-I — State-Family and Candidate Contract (Issue #57, Micro-Rev)

**Report 3 of 6** — `DLH_5VI_STATE_FAMILY_AND_CANDIDATE_CONTRACT.md`

This report freezes the exhaustive, mutually consistent state-family classifier for every
represented state `(a_j, b_i, z)` in `D_W` at the frozen symbolic finite-`m` level, and the
candidate admissibility / representability / destination / rate contract for each family.
Issue §5 (Required design A). All sector contracts are consumed from the accepted chain
(5V-E/F/G and the 5V-H frozen-process ledger); nothing here reopens them.

**Micro-Rev (Reviewer `5644585238`):** the classifier is repaired to **one ownership
convention (Route A)** — F2/F3/F4 own entire endpoint bands with explicit precedence, F8 is
redefined as a genuinely residual disjoint set, and the dispatch contract is one-family /
one-exact-contract per admissible+representable candidate class. A scratch-only classifier
truth-table/enumeration audit (TEMP, not committed) verified `family_count == 1` for every
represented state and `dispatch_contract_count == 1` (or 0 with an explicit exclusion reason)
for every admissible drift-sign class over 74 representative `(m, N_m)` cases
(120,272 represented states; 50,036 admissible classes — see §11 for the reported result).

**Notation.** `s = (j, i)` node; `x_s = (a_j, b_i)`; jumps in physical units
`w_r = (da_m*Delta j, db_m*Delta i)` with `da_m = 10/(19m)`, `db_m = 7/(19m)`; W-index
`10*j + 7*i <= N_m`; `i_t(j) = floor((N_m - 10*j)/7)`; `r_j = (N_m - 10*j) mod 7`;
`j_max = 19m`. A state is **W-active** iff it is a frontier-phase cell: top `i = i_t(j)`
(always W-active), or sub-top `i = i_t(j) - 1` with `i_t(j) >= 2` (accepted DLH-5V-A
condition). A state is on an **economic face** iff `j = 0` (`a = 0`), `j = 19m`
(`a = a_max`), or `i = 0` (`b = b_min`). Reachability bands (`1 <= j <= 6`,
`19m-6 <= j <= 19m-1`, `1 <= i <= 9`) are **labels, not economic faces** (accepted 5V-F
activation binding).

---

## 1. Classifier decision rule — ONE ownership convention (Route A, deterministic, exhaustive, mutually exclusive)

**Chosen convention (Route A):** F2 / F3 / F4 own their **entire endpoint bands**; F8 is the
**genuinely residual disjoint set** of W-active cells inside the regular j-band that fall
below the `i >= 10` regular-band floor. Precedence is explicit: **F9 (triple corner,
`N_m = 190m` exactly) is checked first and owns its cells exclusively; F4 (`i = 0`
W-contact) is checked before F3; corner cells are checked before the face families.**
Every represented state is classified by the following cascade (no overlap, no omission;
`W_max` symbolic, Regime I = `W_max >= 8` i.e. `N_m >= 190m` as the frozen family;
Regime II rows included for classifier completeness):

```text
1. W-active?  (top i = i_t(j), or sub-top i = i_t(j)-1 with i_t(j) >= 2)
     YES -> 2 ;  NO -> 6
2. Triple corner (symbolic W_max = 8, N_m = 190m exactly):
     (j,i) in {(19m-7, 9), (19m, 0)}  -> F9  (exclusive ownership; nothing else owns these cells)
     otherwise -> 3
3. b_min x W W-contact:  i == 0  (W-active; Regime-I instance: (19m, 0) with i_t(19m) = 0,
     N_m in {191m..196m}; at N_m = 190m owned by F9)
     -> F4  (checked before F3: F4 cells are never F3 cells)
     otherwise -> 4
4. Endpoint bands (F2/F3 own their ENTIRE bands):
     j in {0..6}         -> F2  (lower-a endpoint band; j = 0 exact a = 0 face; j in {1..6}
                                 reachability band, a-interior)
     j in {19m-6..19m} (i >= 1, since i = 0 already returned F4)
                         -> F3  (upper-a endpoint band; j = 19m exact a = a_max face;
                                 j in {19m-6..19m-1} reachability band, a-interior)
     otherwise -> 5
5. Regular j-band 7 <= j <= 19m-7:
     i >= 10  -> F1  (regular W-active band)
     1 <= i <= 9  -> F8  (residual W-active cells: sub-tops with i_t(j) = 10; genuinely
                          residual, disjoint from F1 (i < 10) and from F2/F3 (j-band) and
                          F4 (i > 0))
6. W-inactive states (no W face active):
     corner (0, b_min) = (0,0)               -> F10
     corner (a_max, b_min) = (19m, 0)        -> F11   (W-inactive exactly when i_t(19m) >= 1,
                                                       i.e. N_m >= 197m; at N_m in {190m..196m}
                                                       this cell is W-active -> F9 / F4)
     j = 0, i >= 1                           -> F5  (non-W lower-a face)
     j = 19m, i >= 1                         -> F6  (non-W upper-a face)
     i = 0, 1 <= j <= 19m-1                  -> F7  (non-W lower-b face)
     otherwise                               -> F0  (interior / W-inactive; includes
                                                     W-inactive reachability-band states)
```

**Ownership consequences (verified by the scratch truth-table, §11):** the W-active partition
is `F1 ∪ F2 ∪ F3 ∪ F4 ∪ F8 ∪ F9` with pairwise-disjoint memberships (F4 ⊆ {i = 0} is disjoint
from F3 (i ≥ 1), F2 (i ≥ 10 in-band), F1 (i ≥ 10), F8 (i ∈ {1..9}); F9 is exclusive); the
W-inactive partition is `F0 ∪ F5 ∪ F6 ∪ F7 ∪ F10 ∪ F11` with pairwise-disjoint memberships
(corners first, then faces, then interior). One represented state → exactly one family; one
family → exactly one candidate-contract dispatch (report §10).

---

## 2. Family F0 — interior / W-inactive (no active economic face, not W-active)

- **Membership:** W-inactive AND `j not in {0, 19m}` AND `i >= 1`, excluding the corners
  F10/F11 (which are `j = 0`/`j = 19m` rows). Includes the W-inactive reachability-band cells.
- **Active tangent laws:** none (interior of `D_W`). Continuous admissible cone = full plane `R^2`.
- **Accepted path:** **accepted interior source path unchanged** (MATLAB-faithful local FOC
  policy with accepted floors/masks; upwind `max(mu,0)/step` rates on the 4-neighbor stencil).
  The F0 **local row / local policy map is unchanged for the same input value array** (Gate 1A
  common-input regression); the F0 **global value iterate is NOT claimed bit-identical** to the
  old full-domain oracle once boundary rows elsewhere change (Gate 1B boundary-influence
  diagnostic — validation-plan report §5).
- **Sectors / destinations / rates (accepted interior contract):**
  ```text
  mu_a >= 0:  w_right = (+10/(19m), 0),   q_right = 19m*mu_a/10,   dest (j+1, i)   [j+1 <= 19m, 10(j+1)+7i <= N_m]
  mu_a <  0:  w_left  = (-10/(19m), 0),   q_left  = 19m*(-mu_a)/10, dest (j-1, i)  [j >= 1]
  mu_b >= 0:  w_up    = (0, +7/(19m)),    q_up    = 19m*mu_b/7,    dest (j, i+1)   [10j+7(i+1) <= N_m]
  mu_b <  0:  w_down  = (0, -7/(19m)),    q_down  = 19m*(-mu_b)/7, dest (j, i-1)  [i >= 1]
  ```
  Exact first moment `sum_r q_r w_r = (mu_a, mu_b)`; all rates nonnegative; destinations
  represented by the accepted interior availability conditions.
- **Zero-rate ownership:** `mu_a = 0` ⟹ `q_right = q_left = 0`; `mu_b = 0` ⟹ `q_up = q_down = 0`;
  `mu = (0,0)` ⟹ trivial zero row. No sector overlap.
- **Authority:** accepted source interior contract; DLH-5V-A/B stencils; 5V-G §2.

## 3. Family F1 — regular W-active band

- **Membership:** W-active AND `7 <= j <= 19m-7` AND `i >= 10`.
- **Active tangent laws:** W face only: `mu_W <= 0`. Continuous admissible cone `T_W`.
- **Accepted candidate sectors (full coverage `T_W = T_realloc union R_reverse union R_deplete`):**
  ```text
  R_realloc = {mu_a <= 0, mu_b >= 0, mu_W <= 0}:
      w_T  = (-70/(19m), +70/(19m)),  q_T  = 19m*mu_b/70,   dest (j-7, i+10)  [j >= 7 (holds)]
      w_left = (-10/(19m), 0),        q_in = 19m*(-mu_W)/10, dest (j-1, i)
  R_reverse = {mu_a > 0, mu_b < 0, mu_W <= 0}:
      w_RT  = (+70/(19m), -70/(19m)), q_RT = 19m*mu_a/70,   dest (j+7, i-10)  [j+7 <= 19m (holds); i >= 10 (holds)]
      w_down = (0, -7/(19m)),         q_down = 19m*(-mu_W)/7, dest (j, i-1)
  R_deplete = {mu_a <= 0, mu_b < 0}:
      w_left = (-10/(19m), 0),        q_left = 19m*(-mu_a)/10, dest (j-1, i)
      w_down = (0, -7/(19m)),         q_down = 19m*(-mu_b)/7,  dest (j, i-1)
  ```
- **Dispatch (unique, sign-cased):** `mu_b >= 0` → T_realloc (note `mu_b >= 0` with `mu_W <= 0`
  forces `mu_a <= 0` automatically); `mu_b < 0, mu_a > 0` → R_reverse; `mu_b < 0, mu_a <= 0` →
  R_deplete. Exactly one sector per admissible candidate.
- **Exactness:** every sector has exact first moment `sum q_r w_r = (mu_a, mu_b)`; rates
  nonnegative on the sector; `det[w_T w_left] = 70/361`, `det[w_RT w_down] = -490/361`,
  `det[w_left w_down] = 70/361` (all non-zero — unique sector decomposition).
- **Zero-rate / boundary ownership (B1/B2/B3):** `mu_b = 0` → T_realloc with `q_T = 0` (B1);
  `mu_a = 0, mu_b < 0` → R_deplete with `q_left = 0` (B2); `mu_W = 0` → sliding ray owned by
  the sector active at the equality, rate `19m*|mu_b|/70` on `w_T` (mu_b >= 0) or
  `19m*mu_a/70` on `w_RT` (mu_b < 0) (B3); `mu = (0,0)` → trivial zero row.
- **Destination availability:** `w_T` needs `j >= 7` (holds in F1); `w_RT` needs `j+7 <= 19m`
  (holds) and `i >= 10` (holds); `w_left`, `w_down` always represented in F1.
- **Authority:** 5V-E (regular closure, exact contracts, full coverage); 5V-H E.4 ledger
  (regular W-band family PROVED).

## 4. Family F2 — lower-a × W endpoint band (ENTIRE band `j in {0..6}`; Route A)

- **Membership:** W-active AND `j in {0..6}`. Sub-families: **F2a** `j = 0` (exact `a = 0`
  economic face); **F2b** `j in {1..6}` (lower-a reachability band, a-interior — the only
  active economic constraint is the W face). Note: every W-active F2 cell has
  `i = i_t(j)` or `i_t(j) - 1 >= 10` (since `i_t(j) >= 18m >= 10` for `j <= 6`), so the
  mirror `w_RT` destination is always available in this band.
- **Active tangent laws:** F2a: `{mu_a >= 0, mu_W <= 0}`; F2b: `{mu_W <= 0}` (W only).
- **Candidate contracts (dispatch, unique):**
  ```text
  F2a (j = 0):  cone REV = {mu_a >= 0, mu_W <= 0}:
      w_RT  = (+70/(19m), -70/(19m)),  q_RT  = 19m*mu_a/70,   dest (j+7, i-10)  [i >= 10 (holds)]
      w_down = (0, -7/(19m)),          q_down = 19m*(-mu_W)/7, dest (j, i-1)    [i >= 1]
      (single sector; mu_a < 0 candidates are inadmissible by the face law)
  F2b (j in {1..6}):  cone T_W = {mu_W <= 0}, sector dispatch by drift signs:
      mu_b < 0, mu_a > 0 -> R_reverse:  q_RT = 19m*mu_a/70 (mirror (j+7, i-10), i >= 10 holds),
                                        q_down = 19m*(-mu_W)/7
      mu_b < 0, mu_a <= 0 -> R_deplete: q_left = 19m*(-mu_a)/10 (w_left = (-10/(19m), 0),
                                        dest (j-1, i), j >= 1 holds),
                                        q_down = 19m*(-mu_b)/7
      mu_b >= 0 -> EXCLUDED at candidate level (no served contract; see below)
  ```
- **Exclusion content (F2b, `mu_b >= 0`):** serving `mu_b > 0` at these cells would require the
  forward `w_T` (needs `j >= 7`, unavailable) or an upward move that is NOT part of the
  accepted lower-a band sector contracts; this is exactly the 5V-F forward-sliding obstruction
  content (obstruction classes `j in {1..6}` tops with `r_j = 0` and `j = 1, r_1 in {1,2,3}`;
  the same candidate classes are unrepresented at the remaining band cells). Excluded whole at
  the candidate level (report §10.3), never clipped, never a lost-diagonal exit.
- **Zero-rate ownership:** `mu_a = 0` → `q_RT = 0` (F2a face equality `mu_a = d = 0`; F2b
  R_reverse→R_deplete seam B2); `mu_W = 0` → `q_down = 0` (sliding ray on `w_RT`); `mu = (0,0)`
  trivial. Seam-consistent by formula with the regular band (5V-F §8).
- **Second moment (F2a):** `[2660*mu_a + 133*(-mu_W)]/(361m)` (accepted Case-L).
- **Authority:** 5V-F §6/§8 (closable `j = 0` reverse sector; obstruction certificate);
  5V-H E.4 ledger (lower-a × W family, REV, PROVED recovery).

## 5. Family F3 — upper-a × W endpoint band (ENTIRE band `j in {19m-6..19m}`, `i >= 1`; Route A)

- **Membership:** W-active AND `j in {19m-6..19m}` AND `i >= 1` (the `i = 0` W-contact cell
  `(19m, 0)` with `i_t(19m) = 0` is F4, and at `N_m = 190m` it is F9 — F3 never owns `i = 0`
  W-active cells). Sub-families: **F3a** `j = 19m` (exact `a = a_max` face);
  **F3b** `j in {19m-6..19m-1}` (upper-a reachability band, a-interior).
- **Active tangent laws:** F3a: `{mu_a <= 0, mu_W <= 0}`; F3b: `{mu_W <= 0}` (W only).
- **Candidate contracts (dispatch, unique):**
  ```text
  F3a / F3b:  cone per sub-family, sector dispatch by drift signs:
      mu_b >= 0 -> T_realloc:  q_T  = 19m*mu_b/70   (w_T = (-70/(19m), +70/(19m)),
                                    dest (j-7, i+10), j >= 7 holds for j >= 19m-6),
                               q_in = 19m*(-mu_W)/10 (w_left, dest (j-1, i))
      mu_b < 0  -> R_deplete:  q_left = 19m*(-mu_a)/10 (w_left, dest (j-1, i)),
                               q_down = 19m*(-mu_b)/7  (w_down = (0, -7/(19m)), dest (j, i-1))
  ```
- **Exclusion content:** `R_reverse` is unavailable in F3 (`w_RT` needs `j + 7 <= 19m`, which
  fails for `j >= 19m-6`); candidates with `mu_b < 0, mu_a > 0` are excluded at the candidate
  level — this is exactly the 5V-F reverse-sliding obstruction content (obstruction classes
  `j in {13..18}` tops with `r_j = 0` and the no-helper set). Excluded whole, never clipped.
- **i = 0 note (F4 seam):** the cell `(19m, 0)` with `i_t(19m) = 0` (`N_m in {191m..196m}`) is
  owned by F4 (b_min × W W-contact, cone `{mu_b >= 0, mu_W <= 0}` = T_realloc, no deplete) per
  the accepted 5V-F `(19,0)` row; at `N_m = 190m` it is F9 (triple corner). The `i in {1..9}`
  W-active cells with `j = 19m` (`i_t(19m) >= 1`) are F3a and use the TDEP dispatch (forward +
  deplete), per 5V-F "j = 19 top, i_t >= 1" row.
- **Zero-rate ownership:** `mu_b = 0` → T_realloc with `q_T = 0`; `mu_a = 0, mu_b < 0` →
  R_deplete with `q_left = 0`; `mu_W = 0` → sliding ray on `w_T` (mu_b >= 0) / `w_left`-only
  equality (mu_b < 0, mu_a = -mu_b); `mu = (0,0)` trivial.
- **Authority:** 5V-F §6/§8 (closable `j = 19m` T_realloc/deplete; i_t >= 1 row); 5V-H E.4
  ledger (upper-a × W, TDEP, PROVED recovery).

## 6. Family F4 — b_min × W W-contact cells (`i = 0`, W-active; Route A)

- **Membership:** W-active AND `i = 0`. Regime-I instance: `(19m, 0)` with `i_t(19m) = 0`,
  i.e. `N_m in {191m..196m}`; at `N_m = 190m` the cell is owned by F9 (triple corner).
  General membership covers any `(j, 0)` W-active cell with `j >= 7` (the accepted b_min × W
  joint-cell family, 5V-H E.4 ledger; in Regime I only `j = 19m` qualifies since `i_t(j) = 0`
  requires `j > (N_m - 7)/10`).
- **Active tangent laws:** `{mu_b >= 0, mu_W <= 0}` (b_min face + W face, joint; note
  `mu_W <= 0` with `mu_b >= 0` forces `mu_a <= -mu_b <= 0`).
- **Candidate contract (Case B / T_realloc, unique):**
  ```text
  w_T  = (-70/(19m), +70/(19m)),  q_T  = 19m*mu_b/70,    dest (j-7, i+10)  [j >= 7; W-index 10j+7i preserved]
  w_left = (-10/(19m), 0),        q_in = 19m*(-mu_W)/10, dest (j-1, i)      [j >= 1]
  ```
  Exact first moment `q_T*w_T + q_in*w_left = (mu_a, mu_b)`; no deplete branch (mu_b < 0
  candidates are inadmissible by the face law).
- **Destination availability:** `w_T` needs `j >= 7` (holds for the Regime-I instance
  `j = 19m`; a hypothetical W-active `(j, 0)` cell with `j < 7` has no forward destination and
  raises the candidate-level `REPRESENTATION_FAILURE` class — recorded, never clipped).
- **Zero-rate ownership:** `mu_b = 0` → `q_T = 0` (W-slack served by `w_left` only); `mu_W = 0`
  → `q_in = 0` (sliding ray on `w_T`); `mu = (0,0)` trivial.
- **Authority:** 5V-G §2 Case B (buffered cone `{mu_b >= 0, mu_W <= 0} = cone{w_left, w_T}`,
  exact finite-m algebra); 5V-F §8 (`(19,0)` row, T_realloc design cone); 5V-H E.4 ledger
  (b_min × W joint cells, PROVED recovery incl. the double-tangent coupled construction).

## 7. Families F5 / F6 / F7 — non-W economic faces (corner cells excluded; Route A)

### F5 — non-W lower-a face (`j = 0`, W-inactive, `i >= 1`; the cell `(0,0)` is F10)

- **Active law:** `{mu_a >= 0}`; **cone:** `{mu_a >= 0}` = `cone{w_right, w_up, w_down}`.
- **Destinations / rates:** `w_right = (+10/(19m), 0)`, `q_right = 19m*mu_a/10`, dest `(1, i)`
  `[10 + 7i <= N_m]`; `mu_b >= 0`: `w_up`, `q_up = 19m*mu_b/7`, dest `(0, i+1)`
  `[7(i+1) <= N_m]`; `mu_b < 0`: `w_down`, `q_down = 19m*(-mu_b)/7`, dest `(0, i-1)`
  `[i >= 1]`. Exact first moment; `mu_a = 0` ⟹ `q_right = 0` (face law `mu_a = d = 0` at
  `a = 0`); `mu = (0,0)` trivial.
- **Authority:** 5V-H E.4 (non-W a faces: `mu_a(s, alpha) = d` EXACT at every finite `m`);
  accepted source face masks.

### F6 — non-W upper-a face (`j = 19m`, W-inactive, `i >= 1`; the cell `(19m,0)` is F11)

- **Active law:** `{mu_a <= 0}`; **cone:** `{mu_a <= 0}` = `cone{w_left, w_up, w_down}`.
- **Destinations / rates:** `w_left = (-10/(19m), 0)`, `q_left = 19m*(-mu_a)/10`, dest
  `(19m-1, i)`; b-moves as F5. Exact first moment; `mu_a = 0` ⟹ `q_left = 0`; the KKT
  tightening `mu_a = r_a_eff(a_max)*a_max + d <= 0` is enforced by the candidate law
  (`d <= -r_a_eff(a_max)*a_max`), matching 5T §3.4.
- **Authority:** 5T KKT §3.4; 5V-H E.4 (non-W a faces); accepted source upper-a mask
  superseded at the face by the KKT law.

### F7 — non-W lower-b face (`i = 0`, W-inactive, `1 <= j <= 19m-1`; corners F10/F11 excluded)

- **Active law:** `{mu_b >= 0}`; **cone:** `{mu_b >= 0}` = `cone{w_up, w_right, w_left}`.
- **Destinations / rates:** `w_up = (0, +7/(19m))`, `q_up = 19m*mu_b/7`, dest `(j, 1)`
  `[10j + 7 <= N_m]`; `mu_a >= 0`: `w_right`, `q_right = 19m*mu_a/10`, dest `(j+1, 0)`; `mu_a < 0`:
  `w_left`, `q_left = 19m*(-mu_a)/10`, dest `(j-1, 0)` `[j >= 1]`. Exact first moment;
  `mu_b = 0` ⟹ `q_up = 0`; `mu = (0,0)` trivial.
- **Authority:** 5V-H E.4 (non-W b_min face, PROVED recovery); accepted source b_min masks.

## 8. Family F8 — residual W-active cells inside the regular j-band (`7 <= j <= 19m-7`, `1 <= i <= 9`; Route A)

- **Membership (genuinely residual, disjoint):** W-active AND `7 <= j <= 19m-7` AND
  `1 <= i <= 9`. Since `i_t(j) >= 10` throughout `7 <= j <= 19m-7`, these are exactly the
  **sub-top cells with `i_t(j) = 10`** (top `i = 10` and sub-top `i = 9`; the top cell
  `i = 10` is F1, the sub-top `i = 9` is F8). Disjoint from F1 (`i < 10`), F2/F3 (j-bands),
  F4 (`i > 0`), F9 (exclusive).
- **Active tangent laws:** `{mu_W <= 0}` (W only; `7 <= j <= 19m-7` is a-interior,
  `1 <= i <= 9` is b-interior reachability, NOT the economic `b_min` face).
- **Candidate contracts (dispatch, unique):**
  ```text
  mu_b >= 0 -> T_realloc:  q_T  = 19m*mu_b/70   (w_T forward, dest (j-7, i+10), j >= 7 holds),
                           q_in = 19m*(-mu_W)/10 (w_left, dest (j-1, i))
  mu_b < 0, mu_a <= 0 -> R_deplete: q_left = 19m*(-mu_a)/10 (w_left), q_down = 19m*(-mu_b)/7 (w_down)
  mu_b < 0, mu_a > 0 -> EXCLUDED at candidate level (w_RT mirror needs i >= 10, unavailable at
                        i <= 9; no served contract; recorded, never clipped)
  ```
- **Zero-rate ownership:** as F1 (B1 `mu_b = 0` → T_realloc `q_T = 0`; B2 `mu_a = 0, mu_b < 0`
  → R_deplete `q_left = 0`; `mu_W = 0` sliding on `w_T`; `mu = (0,0)` trivial).
- **Obstruction note:** these sub-top cells are NOT in the 5V-F obstruction classes (the
  certificates apply to specific top cells); all served classes are representable
  (5V-F "other top / sub-top → exact-tangent representable (constructive)").
- **Authority:** 5V-F §6/§7 taxonomy; 5V-E §2/§3 sector formulas (seam-consistent).

## 9. Families F9 / F10 / F11 — symbolic corners (precedence explicit; Route A)

Corner classification (accepted 5V-G §6 corrections; 5T §3.6–3.10; 5V-F §3/§8):

| Corner | Continuous cone | Discrete family / contract (exclusive ownership) | Authority |
|---|---|---|---|
| `(0, W_max)` — `a = 0` × `W` (Regime I & II) | `{mu_a >= 0, mu_W <= 0}` | **F2a corner** (REV: `q_RT = 19m*mu_a/70` mirror `(7, i_t(0)-10)` — `i_t(0) >= 10` for `N_m >= 190m`; `q_down = 19m*(-mu_W)/7`) | 5T §3.9; 5V-F §8; 5V-H E.4 (REV PROVED) |
| `(a_max, W_max - a_max)` — `a_max` × `W` (Regime I) | `{mu_a <= 0, mu_W <= 0}` | **F3a corner** (TDEP split: `mu_b >= 0` → `q_T = 19m*mu_b/70` forward `(19m-7, i_t(19m)+10)`; `mu_b < 0` → deplete) | 5T §3.8; 5V-F §8; 5V-H E.4 (TDEP PROVED) |
| `(W_max - b_min, b_min)` — `b_min` × `W` (Regime II only) | `{mu_b >= 0, mu_W <= 0}` | **F4 corner** (Case B: `q_T = 19m*mu_b/70`, `q_in = 19m*(-mu_W)/10`); on-grid node only when `N_m = 10*j` | 5T §3.10; 5V-G §6 |
| `(0, b_min)` — `a = 0` × `b_min` (W not active for `W_max > b_min`; always W-inactive since `i_t(0) >= 10`) | `{mu_a >= 0, mu_b >= 0}` | **F10** (non-W corner; checked before F5/F7): cone `{mu_a >= 0, mu_b >= 0} = cone{w_right, w_up}`; `q_right = 19m*mu_a/10` dest `(1, 0)`; `q_up = 19m*mu_b/7` dest `(0, 1)`; exact first moment | 5T §3.6; 5V-G §6 |
| `(a_max, b_min)` — `a_max` × `b_min` | `{mu_a <= 0, mu_b >= 0}`; +`{W}` iff `W_max = 8` (N_m = 190m) | **F11** (non-W corner, `N_m >= 197m`): cone `{mu_a <= 0, mu_b >= 0} = cone{w_left, w_up}`; `q_left = 19m*(-mu_a)/10` dest `(19m-1, 0)`; `q_up = 19m*mu_b/7` dest `(19m, 1)`; exact first moment. **Ownership ladder:** `N_m = 190m` → **F9** (triple corner, exclusive); `N_m in {191m..196m}` → **F4** (W-contact, T_realloc cone); `N_m >= 197m` → **F11** | 5T §3.7; 5V-F §8; 5V-G §6 |
| `(a_max, b_min)` at `W_max = 8` — **triple corner** (cells `(19m-7, 9)` and `(19m, 0)`, `N_m = 190m` exactly; **exclusive F9 ownership — checked first, before F4/F3**) | `{mu_a <= 0, mu_b >= 0, mu_W <= 0}` (TREA) | **F9**: cell `(19m-7, 9)` — Case-B contract (`i = 9 < 10`, NO mirror): `q_T = 19m*mu_b/70` forward `(19m-14, 19)` (W-index `190m - 7 <= N_m = 190m`), `q_left = 19m*(-mu_W)/10` dest `(19m-8, 9)`; cell `(19m, 0)` — T_realloc contract: `q_T = 19m*mu_b/70` forward `(19m-7, 10)` (W-index `190m`), `q_in = 19m*(-mu_W)/10` dest `(19m-1, 0)` | 5T §3.6/3.7/3.8; 5V-F §8; 5V-H E.4 (TREA PROVED, double-tangent coupled recovery) |

- **Availability at corners:** every listed destination is represented under the stated
  conditions (`i_t(0) >= 10`, `W_max >= a_max + b_min` for Regime I, `N_m = 10j` for the
  Regime-II b_min × W node, `N_m = 190m` at `W_max = 8`).
- **Zero-rate ownership:** at each corner the face-equality rates vanish continuously
  (`mu_a = 0` at `a = 0`, `mu_W = 0` on W, `mu_b = 0` at `b_min`) and match the adjacent family
  seams by formula (5V-F §8).

## 10. Candidate admissibility and representability contract (no silent clipping; one dispatch per class)

For every state `s` and every candidate `alpha = (c, l, d)`:

1. **Economic admissibility (family law):** `alpha` is admissible at `s` iff `c > 0`,
   `l >= 0`, `d in R`, and the resulting drift `mu(s, alpha)` satisfies every ACTIVE tangent
   law of the state's family (§2–§9). Laws on non-active faces are NOT applied (no global
   `mu_b >= 0`; no budget). Violation → candidate excluded as `SCIENTIFIC_ADMISSIBILITY_FAILURE`
   evidence (never clipped into the cone).
2. **One-family dispatch:** the state's family (Route-A classifier, §1) determines the
   candidate-contract dispatch table. For every admissible drift-sign class the family serves,
   **exactly one** sector contract applies (verified by the scratch truth-table, §11); classes
   the family does not serve (documented exclusion content in §4/§5/§8: 5V-F obstruction rays,
   unavailable forward/mirror destinations) receive **no** contract and the candidate is
   excluded at the candidate level (below) — never silently reassigned to another family or
   contract, never dependent on evaluation order.
3. **Representability:** the family's sector contract maps `mu(s, alpha)` to a unique sector
   with exact first moment. The candidate is **representable** iff every destination of its
   sector contract is a **represented node** of the frozen grid (availability conditions
   §2–§9) AND every sector rate is finite and nonnegative. **Unrepresentable candidates are
   excluded from scoring** (their drift is outside the represented moment cone `C_rep(s)`); a
   candidate explicitly requested by the optimizer that is unrepresentable raises
   `REPRESENTATION_FAILURE` (failure taxonomy). **No destination is ever omitted while its
   diagonal escape rate is retained**: if a sector's destination set is not fully available,
   the sector contract does NOT produce a partial row with a lost-diagonal exit — the
   candidate is excluded whole (conservative-Q contract, Bellman report §5).
4. **5V-F obstruction consumption:** at the obstruction classes the continuously admissible
   cone is strictly larger than `C_rep(s)`; the excluded candidates are exactly the certified
   unrepresentable W-tangent sliding rays (forward-sliding at lower-a band tops, reverse-sliding
   at upper-a band tops, and the no-helper classes), plus the destination-unavailable classes
   (T_realloc forward at `j < 7`, mirror at `i < 10`, R_reverse at `j > 19m-7`). This is
   accepted provenance (5V-F §7/§10; 5V-H: the operator-level target does not require raw-graph
   admissibility), recorded per state by the future Gate-2 diagnostics, and is NOT a silent
   clip and NOT a reopened obstruction.
5. **No ghost states, no interpolation, no virtual destinations** — represented native-grid
   destinations only (frozen same-process law).
6. **Z-dimension:** every family row is instantiated per `z`; the exogenous `z`-switch
   transitions are added at the score/Q level (Bellman report §1/§4) and are identical across
   `z`-rows of the same `(j,i)`.

## 11. Classifier completeness, determinism, and scratch truth-table evidence

- **Exhaustiveness:** the cascade of §1 partitions the represented set: W-active cells are
  exactly `F1 ∪ F2 ∪ F3 ∪ F4 ∪ F8 ∪ F9` (pairwise disjoint — F2 j-band {0..6}, F3 j-band
  {19m-6..19m} with i ≥ 1, F4 i = 0, F1 i ≥ 10 in the regular j-band, F8 i ∈ {1..9} in the
  regular j-band, F9 exclusive); W-inactive cells are exactly `F0 ∪ F5 ∪ F6 ∪ F7 ∪ F10 ∪ F11`
  (pairwise disjoint — corners first, then faces with corner-excluded memberships, then
  interior). No cell is left unclassified; the Regime-II corner row is included for classifier
  completeness even though the symbolic Regime-I family (`N_m >= 190m`) is the active one.
- **Determinism:** classification depends only on `(j, i, N_m, m)` through the accepted
  formulas (`i_t`, W-activity, bands, corners); no numerical value, no evaluation-order
  dependence; reproducible.
- **Scratch truth-table (TEMP only, NOT committed — outside the six-file allowlist):**
  `%TEMP%\dlh5vi_rev1_classifier_audit.py`, executed with Python (exact integer arithmetic).
  **Result:** over 74 representative `(m, N_m)` cases (`m in {1,2,3}`; `N_m` residues covering
  `190m + k` for representative `k`, incl. `190m` (triple corner), `191m..196m` (F4 window),
  `197m..203m` (F11 window), and larger values): **120,272 represented states enumerated;
  `family_count == 1` for EVERY state (asserted)**; **50,036 admissible drift-sign classes
  tested; `dispatch_contract_count == 1` (served) or 0 (documented exclusion) for every class —
  never more than one served contract**; F9 exclusive at `N_m = 190m` (cells `(19m-7,9)` and
  `(19m,0)`); `(19m, 0)` → F4 for `N_m in {191m..196m}` and → F11 for `N_m >= 197m`; F8
  nonempty exactly at sub-top cells with `i_t(j) = 10` (e.g. `(12, 9)` at `N_m = 191m, m = 1`)
  and disjoint from all other W-active families.
- **Authority map:** every row cites its accepted source (5T KKT laws, 5V-A..E contracts,
  5V-F taxonomy/certificate, 5V-G corrections, 5V-H recovery ledger) — no new science
  introduced, no frozen contract reopened.
