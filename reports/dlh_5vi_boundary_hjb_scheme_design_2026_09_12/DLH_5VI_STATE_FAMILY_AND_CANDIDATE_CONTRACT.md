# DLH-5V-I — State-Family and Candidate Contract (Issue #57)

**Report 3 of 6** — `DLH_5VI_STATE_FAMILY_AND_CANDIDATE_CONTRACT.md`

This report freezes the exhaustive, mutually consistent state-family classifier for every
represented state `(a_j, b_i, z)` in `D_W` at the frozen symbolic finite-`m` level, and the
candidate admissibility / representability / destination / rate contract for each family.
Issue §5 (Required design A). All sector contracts are consumed from the accepted chain
(5V-E/F/G and the 5V-H frozen-process ledger); nothing here reopens them.

**Notation.** `s = (j, i)` node; `x_s = (a_j, b_i)`; jumps in physical units
`w_r = (da_m*Delta j, db_m*Delta i)` with `da_m = 10/(19m)`, `db_m = 7/(19m)`; W-index
`10*j + 7*i <= N_m`; `i_t(j) = floor((N_m - 10*j)/7)`; `r_j = (N_m - 10*j) mod 7`;
`j_max = 19m`. A state is **W-active** iff it is a frontier-phase cell: top `i = i_t(j)`
(always W-active), or sub-top `i = i_t(j) - 1` with `i_t(j) >= 2` (accepted DLH-5V-A
condition). A state is on an **economic face** iff `j = 0` (`a = 0`), `j = 19m`
(`a = a_max`), or `i = 0` (`b = b_min`). Reachability bands (`1 <= j <= 6`,
`19m-6 <= j <= 19m-1`, `1 <= i <= 9`) are **labels, not economic faces** (accepted
5V-F activation binding).

---

## 1. Classifier decision rule (deterministic, exhaustive, mutually exclusive)

Every represented state is classified by the following decision cascade (no overlap, no
omission; `W_max` symbolic, Regime I = `W_max >= 8` i.e. `N_m >= 190m` as the frozen
family; Regime II rows included for classifier completeness):

```text
1. W-active?  (top i = i_t(j), or sub-top i = i_t(j)-1 with i_t(j) >= 2)
     YES -> 2 ;  NO -> 4
2. Triple corner (symbolic W_max = 8, N_m = 190m exactly):
     (j,i) in {(19m-7, 9), (19m, 0)}  -> F9 (TREA; exclusive owner of these cells)
     otherwise -> 3
3. Face membership among W-active states:
     j = 0            -> F2 (lower-a x W endpoint band; exact a=0 face at j = 0)
     j = 19m          -> F3 (upper-a x W endpoint band; exact a_max face at j = 19m;
                             incl. the i = 0 W-contact sub-case with i_t(19m) = 0,
                             N_m in {191m..196m}, design cone T_realloc per 5V-F §8)
     i = 0            -> F4 (lower-b x W joint band; exact b_min face at i = 0)
     7 <= j <= 19m-7 AND i >= 10  -> F1 (regular W-active band)
     j in {1..6} or j in {19m-6..19m-1} or 1 <= i <= 9 (and not covered above)
                        -> F8 (W-active endpoint/reachability cells; sector per §5.8)
   Corner W-active cells are the i = i_t(j) members of F2/F3/F4 at the symbolic corners
   (see §6): (0, W_max) -> F2 corner; (a_max, W_max - a_max) -> F3 corner;
   (W_max - b_min, b_min) -> F4 corner (Regime II only); triple corner W_max = 8 -> F9
   (checked first, exclusive).
3. Non-W-active economic faces:
     j = 0 (i <= i_t(0) - 2)  -> F5 (non-W lower-a face)
     j = 19m (i <= i_t(19m) - 2) -> F6 (non-W upper-a face)
     i = 0 (non-W-active)     -> F7 (non-W lower-b face)
     (0, b_min) and (a_max, b_min) corners when non-W-active -> F10/F11 (§6)
4. All remaining states (not W-active, not on an economic face) -> F0 (interior / W-inactive;
   includes reachability-band states `j in {1..6}`, `j in {19m-6..19m-1}`, `i in {1..9}`
   that are W-inactive).
```

Every family row in §2–§9 fixes: active continuous tangent laws; accepted candidate
sector(s); exact destination offsets; destination-availability conditions; rate formulas;
zero-rate / equality ownership; source authority. **No silent clipping** — an unavailable
destination excludes the candidate (candidate contract §10) or raises
`REPRESENTATION_FAILURE` (failure taxonomy); a destination is never omitted while its
diagonal escape rate is retained (conservative-Q contract, Bellman report §5).

---

## 2. Family F0 — interior / W-inactive (no active economic face, not W-active)

- **Membership:** all represented states not captured by F1–F11: `W-inactive` AND `j not in {0, 19m}` AND `i >= 1`. Includes the W-inactive reachability-band cells.
- **Active tangent laws:** none (interior of `D_W`; W-inactive ⟹ the W face is not active at this cell). Continuous admissible cone = full plane `R^2`.
- **Accepted path:** **accepted interior source path unchanged** (MATLAB-faithful local FOC policy with accepted floors/masks; upwind `max(mu,0)/step` rates on the 4-neighbor stencil). This is the Gate-1 regression set (validation plan §2): rows are bit-identical to the accepted oracle by construction.
- **Sectors / destinations / rates (accepted interior contract):**
  ```text
  mu_a >= 0:  w_right = (+10/(19m), 0),   q_right = 19m*mu_a/10,   dest (j+1, i)   [j+1 <= 19m, 10(j+1)+7i <= N_m]
  mu_a <  0:  w_left  = (-10/(19m), 0),   q_left  = 19m*(-mu_a)/10, dest (j-1, i)  [j >= 1]
  mu_b >= 0:  w_up    = (0, +7/(19m)),    q_up    = 19m*mu_b/7,    dest (j, i+1)   [10j+7(i+1) <= N_m]
  mu_b <  0:  w_down  = (0, -7/(19m)),    q_down  = 19m*(-mu_b)/7, dest (j, i-1)  [i >= 1]
  ```
  Exact first moment `sum_r q_r w_r = (mu_a, mu_b)`; all rates nonnegative; destinations represented by the accepted interior availability conditions.
- **Zero-rate ownership:** `mu_a = 0` ⟹ `q_right = q_left = 0` (a-coordinate static); `mu_b = 0` ⟹ `q_up = q_down = 0`; `mu = (0,0)` ⟹ trivial zero row (all rates 0). No sector overlap.
- **Authority:** accepted source interior contract; DLH-5V-A/B stencils; 5V-G §2 (interior layer cells exactly representable).

## 3. Family F1 — regular W-active band

- **Membership:** W-active AND `7 <= j <= 19m-7` AND `i >= 10` (accepted common regular region).
- **Active tangent laws:** W face only: `mu_W = mu_a + mu_b <= 0`. Continuous admissible cone `T_W`.
- **Accepted candidate sectors (full coverage `T_W = T_realloc union R_reverse union R_deplete`):**
  ```text
  R_realloc = {mu_a <= 0, mu_b >= 0, mu_W <= 0}:
      w_T  = (-70/(19m), +70/(19m)),  q_T  = 19m*mu_b/70,   dest (j-7, i+10)  [j >= 7 (holds); 10(j-7)+7(i+10)=10j+7i <= N_m]
      w_left = (-10/(19m), 0),        q_in = 19m*(-mu_W)/10, dest (j-1, i)
  R_reverse = {mu_a > 0, mu_b < 0, mu_W <= 0}:
      w_RT  = (+70/(19m), -70/(19m)), q_RT = 19m*mu_a/70,   dest (j+7, i-10)  [j+7 <= 19m (holds); i >= 10 (holds)]
      w_down = (0, -7/(19m)),         q_down = 19m*(-mu_W)/7, dest (j, i-1)
  R_deplete = {mu_a <= 0, mu_b < 0}:
      w_left = (-10/(19m), 0),        q_left = 19m*(-mu_a)/10, dest (j-1, i)
      w_down = (0, -7/(19m)),         q_down = 19m*(-mu_b)/7,  dest (j, i-1)
  ```
- **Exactness:** every sector has exact first moment `sum q_r w_r = (mu_a, mu_b)`; rates nonnegative on the sector; `det[w_T w_left] = 70/361`, `det[w_RT w_down] = -490/361`, `det[w_left w_down] = 70/361` (all non-zero — unique sector decomposition).
- **Zero-rate / boundary ownership (B1/B2/B3, no double counting):** `mu_b = 0` → candidate in `R_realloc` (depletion limit; `q_T = 0`); `mu_a = 0` → candidate in `R_deplete` (reverse limit; `q_left = 0`); `mu_W = 0` → sliding ray owned by the sector active at the equality, rate consistent with `19m*|mu_b|/70` on `w_T` (mu_b >= 0) or `19m*mu_a/70` on `w_RT` (mu_b < 0); `mu = (0,0)` → trivial zero row. Each continuously admissible candidate has **exactly one** applicable sector contract.
- **Destination availability:** `w_T` needs `j >= 7` (holds in F1) and the W-index identity keeps the destination represented; `w_RT` needs `j + 7 <= 19m` (holds) and `i >= 10` (holds); `w_left`, `w_down` always represented in F1.
- **Authority:** 5V-E (regular closure, exact contracts, full coverage); 5V-H E.4 ledger (regular W-band family PROVED).

## 4. Family F2 — lower-a × W endpoint band (including `a = 0` face)

- **Membership:** W-active AND `j in {0..6}` (top or eligible sub-top). `j = 0` is the exact `a = 0` economic face; `j in {1..6}` are the lower-a reachability band (a-interior — the only active economic constraint is the W face).
- **Active tangent laws:** `j = 0`: `{mu_a >= 0, mu_W <= 0}`; `j in {1..6}`: `{mu_W <= 0}` (W only — reachability band, not an economic face).
- **Accepted candidate sector (REV = `{mu_a >= 0, mu_W <= 0}` for `j = 0`; same sector contract for the band):**
  ```text
  w_RT  = (+70/(19m), -70/(19m)),  q_RT  = 19m*mu_a/70,   dest (j+7, i-10)  [j+7 <= 19m (holds); i >= 10]
  w_down = (0, -7/(19m)),          q_down = 19m*(-mu_W)/7, dest (j, i-1)    [i >= 1]
  ```
  Exact first moment; second moment `[2660*mu_a + 133*(-mu_W)]/(361m)` (accepted Case-L).
- **Destination availability:** mirror `(j+7, i-10)` represented iff `i >= 10` AND `10(j+7) + 7(i-10) = 10j + 7i <= N_m` (W-index preserved). If `i < 10` (lower-b reachability overlap at a W-active `j <= 6` cell — see F8/F9 handling), the mirror is unavailable and the candidate contract of §10 applies (no silent clip; the 5V-F/F8 classification governs).
- **Zero-rate ownership:** `mu_a = 0` → `q_RT = 0` (a-static, matches `j = 0` face equality `mu_a = d = 0`); `mu_W = 0` → `q_down = 0` (sliding ray on `w_RT`); `mu = (0,0)` trivial.
- **Obstruction provenance (5V-F, consumed):** at exact-frontier `r_j = 0` W-active top cells with `j in {1..6}`, the continuously admissible **forward-sliding ray** `{(-u, +u), u > 0}` (`mu_W = 0`, `mu_b = +u > 0`) is not representable by any nonnegative combination of represented destinations (mirror rays all have `mu_b < 0`). Per the classifier this exact-tangent candidate set is **excluded at the candidate-contract level** (§10, representability); the remaining representable candidates of the REV cone are scored normally. No diagonal-escape retention (conservative-Q report). This is accepted provenance, not a new contradiction.
- **Authority:** 5V-F §6/§8 (closable `j = 0` reverse sector; obstruction classes); 5V-H E.4 ledger (lower-a × W family, REV, PROVED recovery).

## 5. Family F3 — upper-a × W endpoint band (including `a = a_max` face)

- **Membership:** W-active AND `j in {19m-6..19m}`. `j = 19m` is the exact `a = a_max` economic face; `j in {19m-6..19m-1}` are the upper-a reachability band (a-interior; W only active).
- **Active tangent laws:** `j = 19m`: `{mu_a <= 0, mu_W <= 0}`; band: `{mu_W <= 0}`.
- **Accepted candidate sectors (TDEP split):**
  ```text
  mu_b >= 0 (T_realloc):  w_T  = (-70/(19m), +70/(19m)), q_T  = 19m*mu_b/70,   dest (j-7, i+10)  [j >= 7]
                          w_left = (-10/(19m), 0),       q_in = 19m*(-mu_W)/10, dest (j-1, i)
  mu_b <  0 (R_deplete):  w_left = (-10/(19m), 0),       q_left = 19m*(-mu_a)/10, dest (j-1, i)
                          w_down = (0, -7/(19m)),        q_down = 19m*(-mu_b)/7,  dest (j, i-1)
  ```
  Exact first moment in both branches.
- **Destination availability:** `w_T` needs `j >= 7` (holds for `j >= 19m-6`, `m >= 1`); `w_left`, `w_down` always represented in F3. **i = 0 W-contact sub-case (`j = 19m`, W-active, `i_t(19m) = 0`, i.e. `N_m in {191m..196m}`):** the accepted design cone is T_realloc `{mu_a <= 0, mu_b >= 0, mu_W <= 0}` (W-contact law, 5V-F §8), served by `q_T = 19m*mu_b/70` on `w_T` (dest `(19m-7, 10)`, W-index `190m <= N_m`) and `q_in = 19m*(-mu_W)/10` on `w_left` (dest `(19m-1, 0)`); the `N_m = 190m` instance of this cell is owned exclusively by F9 (triple corner).
- **Zero-rate ownership:** `mu_b = 0` → T_realloc branch with `q_T = 0`; `mu_a = 0` → R_deplete with `q_left = 0`; `mu_W = 0` → sliding ray on `w_T` (mu_b >= 0) / `w_RT`-type equality not present here (R_deplete has `mu_W < 0` strictly unless `mu = (0,0)`); `mu = (0,0)` trivial.
- **Obstruction provenance (5V-F, consumed):** at exact-frontier `r_j = 0` W-active top cells with `j in {13..18}` (i.e. `19m-6 <= j <= 19m-1`), the **reverse-sliding ray** `{(+u, -u), u > 0}` is not representable (forward rays all have `mu_a < 0`); excluded at the candidate-contract level (§10), matching 5V-F §6 no-helper classes.
- **Authority:** 5V-F §6/§8 (closable `j = 19m` T_realloc/deplete); 5V-H E.4 ledger (upper-a × W, TDEP, PROVED recovery).

## 6. Family F4 — lower-b × W joint band (including `b = b_min` face)

- **Membership:** W-active AND `i in {0..9}` (top or eligible sub-top). `i = 0` is the exact `b = b_min` face; `i in {1..9}` are the lower-b reachability band (b-interior; W only active).
- **Active tangent laws:** `i = 0`: `{mu_b >= 0, mu_W <= 0}`; band: `{mu_W <= 0}` (with the accepted buffered Case-B treatment).
- **Accepted candidate sector (Case B, buffered cone `{mu_b >= 0, mu_W <= 0} = cone{w_left, w_T}` — note `mu_W <= 0` with `mu_b >= 0` implies `mu_a <= -mu_b <= 0`):**
  ```text
  w_T  = (-70/(19m), +70/(19m)),  q_T  = 19m*mu_b/70,    dest (j-7, i+10)  [j >= 7; 10(j-7)+7(i+10) = 10j+7i <= N_m]
  w_left = (-10/(19m), 0),        q_in = 19m*(-mu_W)/10, dest (j-1, i)      [j >= 1]
  ```
  Exact first moment `q_T*w_T + q_in*w_left = (mu_a, mu_b)`.
- **Destination availability:** `w_T` needs `j >= 7`. For the symbolic Regime-I family with `W_max > 8` the W-active lower-b cells lie near the upper-a corner (`j ~ 19m`), where `j >= 7` holds (5V-G §6: for fixed `W_max > 8` these cells vanish for large `m`; at `W_max = 8` they are the triple-corner cells, family F9). For a hypothetical W-active cell with `j < 7` the forward destination is unavailable → candidate contract §10 (`REPRESENTATION_FAILURE` semantics — the buffered cone cannot be served by `w_T` alone; recorded, no silent clip).
- **Zero-rate ownership:** `mu_b = 0` → `q_T = 0` (W-slack served by `w_left` only); `mu_W = 0` → `q_in = 0` (sliding ray on `w_T`); `mu = (0,0)` trivial.
- **Authority:** 5V-G §2 Case B; 5V-F §8 (b-min face cells); 5V-H E.4 ledger (b_min × W joint cells, PROVED recovery incl. the double-tangent coupled construction).

## 7. Families F5 / F6 / F7 — non-W economic faces

### F5 — non-W lower-a face (`j = 0`, W-inactive, `i <= i_t(0) - 2`)

- **Active law:** `{mu_a >= 0}`; **cone:** `{mu_a >= 0}` = `cone{w_right, w_up, w_down}` (full b-freedom).
- **Destinations / rates:** `w_right = (+10/(19m), 0)`, `q_right = 19m*mu_a/10`, dest `(1, i)` `[10 + 7i <= N_m]`; `mu_b >= 0`: `w_up`, `q_up = 19m*mu_b/7`, dest `(0, i+1)` `[7(i+1) <= N_m]`; `mu_b < 0`: `w_down`, `q_down = 19m*(-mu_b)/7`, dest `(0, i-1)` `[i >= 1]`. Exact first moment; `mu_a = 0` ⟹ `q_right = 0` (exact face law `mu_a = d = 0` at `a = 0`); `mu = (0,0)` trivial.
- **Authority:** 5V-H E.4 (non-W a faces: `mu_a(s, alpha) = d` EXACT at every finite `m`); accepted source face masks.

### F6 — non-W upper-a face (`j = 19m`, W-inactive, `i <= i_t(19m) - 2`)

- **Active law:** `{mu_a <= 0}`; **cone:** `{mu_a <= 0}` = `cone{w_left, w_up, w_down}`.
- **Destinations / rates:** `w_left = (-10/(19m), 0)`, `q_left = 19m*(-mu_a)/10`, dest `(19m-1, i)`; b-moves as F5. Exact first moment; `mu_a = 0` ⟹ `q_left = 0`; note the KKT tightening `mu_a = r_a_eff(a_max)*a_max + d <= 0` is enforced by the candidate law (d must satisfy `d <= -r_a_eff(a_max)*a_max`), matching 5T §3.4.
- **Authority:** 5T KKT §3.4; 5V-H E.4 (non-W a faces); accepted source upper-a mask superseded at the face by the KKT law (accepted 5T gap closed by the boundary contract).

### F7 — non-W lower-b face (`i = 0`, W-inactive)

- **Active law:** `{mu_b >= 0}`; **cone:** `{mu_b >= 0}` = `cone{w_up, w_right, w_left}` (full a-freedom).
- **Destinations / rates:** `w_up = (0, +7/(19m))`, `q_up = 19m*mu_b/7`, dest `(j, 1)` `[10j + 7 <= N_m]`; `mu_a >= 0`: `w_right`, `q_right = 19m*mu_a/10`, dest `(j+1, 0)`; `mu_a < 0`: `w_left`, `q_left = 19m*(-mu_a)/10`, dest `(j-1, 0)` `[j >= 1]`. Exact first moment; `mu_b = 0` ⟹ `q_up = 0`; `mu = (0,0)` trivial.
- **Authority:** 5V-H E.4 (non-W b_min face, PROVED recovery); accepted source b_min masks.

## 8. Family F8 — W-active endpoint / reachability cells not in F1–F4 (residual W-active cells)

- **Membership:** W-active cells with `j in {1..6}` OR `j in {19m-6..19m-1}` OR `i in {1..9}` that are NOT already in F2/F3/F4 by face membership. (Per 5V-F §6 these are exactly the classes `{W}`-only endpoint cells: `j in {1..6}` top/sub-top, `j in {13..18}` top/sub-top, and `i <= 9` W-active cells, which for `N_m >= 190m` lie in classes `13..19`; the `(19m, 0)` corner is F9 at `W_max = 8` / F3 otherwise.)
- **Active law:** `{mu_W <= 0}` (W only — endpoint a-interior/b-interior cells).
- **Sector contract:** the REV/TDEP/Case-B sector formulas of F2/F3/F4 apply by band membership with **exact destination-availability conditions**:
  - lower band `j in {1..6}`: REV-style `q_RT = 19m*mu_a/70` (mirror `(j+7, i-10)`, needs `i >= 10`), `q_down = 19m*(-mu_W)/7`; candidates requiring `mu_b > 0` on the exact W-tangent sliding ray are NOT representable (5V-F certificate) → §10 exclusion.
  - upper band `j in {19m-6..19m-1}`: TDEP-style T_realloc/deplete split; mirror-less handling for `i < 10` cells.
  - lower-b overlap `i in {1..9}` W-active: Case-B style `q_T = 19m*mu_b/70` (needs `j >= 7`), `q_in = 19m*(-mu_W)/10`.
- **Zero-rate ownership and availability:** as in F2/F3/F4 with the band-specific conditions; any candidate whose sector requires an unavailable destination is excluded (§10).
- **Authority:** 5V-F §6 taxonomy + §7 certificate (obstruction classes enumerated per `N_m` residue); 5V-G §7 (layer taxonomy corrections).

## 9. Families F9 / F10 / F11 — symbolic corners and the `W_max = 8` triple corner

Corner classification (accepted 5V-G §6 corrections; 5T §3.6–3.10; 5V-F §3):

| Corner | Continuous cone | Discrete family / contract | Authority |
|---|---|---|---|
| `(0, W_max)` — `a = 0` × `W` (Regime I & II) | `{mu_a >= 0, mu_W <= 0}` | **F2 corner** (REV: `q_RT = 19m*mu_a/70` mirror `(7, i_t(0)-10)` — `i_t(0) >= 10` for `N_m >= 190m`; `q_down = 19m*(-mu_W)/7`) | 5T §3.9; 5V-F §8; 5V-H E.4 (REV PROVED) |
| `(a_max, W_max - a_max)` — `a_max` × `W` (Regime I) | `{mu_a <= 0, mu_W <= 0}` | **F3 corner** (TDEP split: `mu_b >= 0` → `q_T = 19m*mu_b/70` forward `(19m-7, i_t(19m)+10)`; `mu_b < 0` → deplete) | 5T §3.8; 5V-F §8; 5V-H E.4 (TDEP PROVED) |
| `(W_max - b_min, b_min)` — `b_min` × `W` (Regime II only) | `{mu_b >= 0, mu_W <= 0}` | **F4 corner** (Case B: `q_T = 19m*mu_b/70`, `q_in = 19m*(-mu_W)/10`); on-grid node only when `N_m = 10*j` | 5T §3.10; 5V-G §6 |
| `(0, b_min)` — `a = 0` × `b_min` (W not active for `W_max > b_min`) | `{mu_a >= 0, mu_b >= 0}` | **F10** (non-W corner): cone `{mu_a >= 0, mu_b >= 0} = cone{w_right, w_up}`; `q_right = 19m*mu_a/10` dest `(1, 0)`; `q_up = 19m*mu_b/7` dest `(0, 1)`; exact first moment | 5T §3.6; 5V-G §6 |
| `(a_max, b_min)` — `a_max` × `b_min` (W not active for `W_max > 8`) | `{mu_a <= 0, mu_b >= 0}` | **F11** (non-W corner): cone `{mu_a <= 0, mu_b >= 0} = cone{w_left, w_up}`; `q_left = 19m*(-mu_a)/10` dest `(19m-1, 0)`; `q_up = 19m*mu_b/7` dest `(19m, 1)`; exact first moment | 5T §3.7; 5V-G §6 |
| `(a_max, b_min)` at `W_max = 8` — **triple corner** (cells `(19m-7, 9)` and `(19m, 0)`, `N_m = 190m` exactly; **exclusive F9 ownership** — the cascade checks F9 before face membership) | `{mu_a <= 0, mu_b >= 0, mu_W <= 0}` (TREA) | **F9**: cell `(19m-7, 9)` — Case-B contract (`i = 9 < 10`, NO mirror): `q_T = 19m*mu_b/70` forward `(19m-14, 19)` (W-index `190m - 7 <= N_m = 190m`), `q_left = 19m*(-mu_W)/10` dest `(19m-8, 9)`; cell `(19m, 0)` — T_realloc contract: `q_T = 19m*mu_b/70` forward `(19m-7, 10)` (W-index `190m`), `q_in = 19m*(-mu_W)/10` dest `(19m-1, 0)` | 5T §3.6/3.7/3.8; 5V-F §8; 5V-H E.4 (TREA PROVED, double-tangent coupled recovery) |

- **Availability at corners:** every listed destination is represented under the stated conditions (`i_t(0) >= 10`, `W_max >= a_max + b_min` for Regime I, `N_m = 10j` for the Regime-II b_min × W node, `N_m = 190m` at `W_max = 8`).
- **Zero-rate ownership:** at each corner the face-equality rates vanish continuously (`mu_a = 0` at `a = 0`, `mu_W = 0` on W, `mu_b = 0` at `b_min`) and match the adjacent family seams by formula (regular-to-endpoint seams `j = 0 <-> 7`, `j = 19m-7 <-> 19m` continuous by formula — accepted 5V-F §8).

## 10. Candidate admissibility and representability contract (Issue §5, §9 — no silent clipping)

For every state `s` and every candidate `alpha = (c, l, d)`:

1. **Economic admissibility (family law):** `alpha` is admissible at `s` iff `c > 0`, `l >= 0`, `d in R`, and the resulting drift `mu(s, alpha)` satisfies every ACTIVE tangent law of the state's family (from §2–§9). Laws on non-active faces are NOT applied (no global `mu_b >= 0`; no budget). Violation → candidate excluded as `SCIENTIFIC_ADMISSIBILITY_FAILURE` evidence (never clipped into the cone).
2. **Representability:** the family's sector contract maps `mu(s, alpha)` to a unique sector with exact first moment. The candidate is **representable** iff every destination of its sector contract is a **represented node** of the frozen grid (availability conditions of §2–§9) AND every sector rate is finite and nonnegative. **Unrepresentable candidates are excluded from scoring** (their drift is outside the represented moment cone `C_rep(s)`); a candidate explicitly requested by the optimizer that is unrepresentable raises `REPRESENTATION_FAILURE` (failure taxonomy). **No destination is ever omitted while its diagonal escape rate is retained**: if a sector's destination set is not fully available, the sector contract does NOT produce a partial row with a lost-diagonal exit — the candidate is excluded whole (conservative-Q contract, Bellman report §5).
3. **5V-F obstruction consumption:** at the obstruction classes (F8 / F2 band / F3 band exact-frontier cells) the continuously admissible cone is strictly larger than `C_rep(s)`; the excluded candidates are exactly the certified unrepresentable W-tangent sliding rays. This is accepted provenance (5V-F §7/§10; 5V-H: the operator-level target does not require raw-graph admissibility), recorded per state by the future Gate-2 diagnostics, and is NOT a silent clip and NOT a reopened obstruction.
4. **No ghost states, no interpolation, no virtual destinations** — represented native-grid destinations only (frozen same-process law).
5. **Z-dimension:** every family row is instantiated per `z`; the exogenous `z`-switch transitions are added at the score/Q level (Bellman report §4) and are identical across `z`-rows of the same `(j,i)`.

## 11. Classifier completeness and determinism

- **Exhaustiveness:** the cascade of §1 partitions the represented set: W-active cells are exactly `F1 ∪ F2 ∪ F3 ∪ F4 ∪ F8 ∪ F9` (F2/F3/F4 face rows, F8 residual endpoint cells, F9 triple corner); W-inactive cells are exactly `F0 ∪ F5 ∪ F6 ∪ F7 ∪ F10 ∪ F11`. No cell is left unclassified; the Regime-II corner row is included for classifier completeness even though the symbolic Regime-I family (`N_m >= 190m`) is the active one.
- **Determinism:** classification depends only on `(j, i, W-activity, face membership, band)` — accepted formulas only; no numerical value; reproducible.
- **Authority map:** every row cites its accepted source (5T KKT laws, 5V-A..E contracts, 5V-F taxonomy/certificate, 5V-G corrections, 5V-H recovery ledger) — no new science introduced, no frozen contract reopened.
