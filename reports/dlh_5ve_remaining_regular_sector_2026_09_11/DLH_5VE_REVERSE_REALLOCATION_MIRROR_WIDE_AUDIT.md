# DLH-5V-E — Reverse-Reallocation Mirror-Wide Audit

**Issue:** deep-learning-hank #53 (DLH-5V-E) · **Branch:** `dsh/issue-53-dlh-5ve-remaining-regular-sector-2026-09-11`
Covers Issue §4 (candidate mirror tangent) and §5.1–§5.4 (represented destination/path, phase/class preservation,
cone/rates, reverse-sector scoring). Exact algebra only; tiny exact Fraction spot-checks in `%TEMP%` (not committed);
no sweeps, no new numerical experiment.

---

## 1. Candidate mirror wide tangent (Issue §4) — audited, now accepted on the declared regular region

Native exact tangent: `10 Delta j + 7 Delta i = 0` with primitive lattice direction `(Delta j, Delta i) = (+7, -10)`
(the mirror of the accepted forward `(-7,+10)`), giving

```
w_RT = (+70/19, -70/19),   transition (j,i) -> (j+7, i-10).
```

## 2. Represented destination and path audit (Issue §5.1) — proved

**Index identity (exact):**

```
10(j+7) + 7(i-10) = 10j + 70 + 7i - 70 = 10j + 7i.
```

The mirror destination has the **same W-index** as the source, so on the W-frontier (`10j+7i = N`) the destination
is on the same frontier: W (`a+b`) is preserved **exactly**.

**Conditions (all proved):**

| condition | exact statement | status |
|---|---|---|
| lower-b (`b = b_min` face) | `i - 10 >= 0`, i.e. `i >= 10` | binding constraint |
| upper-a (`a <= a_max` grid range) | on the frontier, `10(j+7) <= N - 7(i-10) <= N` ⟹ `j+7 <= N/10`, so `a_dest <= a_max` follows from `i >= 10` (accepted indexing: a-max corner = `(N/10, 0)`) | automatic given `i >= 10` |
| W-domain membership | `a_dest + b_dest = a_src + b_src <= W_max` (index preserved) | automatic |
| straight segment in `D_W` | a increases monotonically from `a_src` to `a_src + 70/19` (both in `[0, a_max]`), b decreases monotonically to `b_src - 70/19 >= b_min`; W is constant; `D_W` is convex ⟹ whole segment inside | proved |
| other economic boundary crossing | a=0 face not crossed (a increasing); b-min face not crossed (given `i >= 10`); W-frontier not crossed (W constant); a-max corner region excluded by the band below | none in the declared regular region |

**Exact finite deferred band (endpoint/joint-boundary object, NOT a regular failure):**

```
i in {0, ..., 9}   (b-low / a-high end of the W-frontier, including the a-max/b-min joint corner region)
```

Sources in this band cannot take the mirror-wide transition; they are **deferred** to the endpoint/joint-boundary
gate and are **not** silently clamped or treated as regular failures. (The symmetric forward band `j in {0..6}` was
already deferred by accepted DLH-5V-C.)

**Declared regular region for the mirror-wide contract (and for the full closure of Issue §8):**

```
regular W-active states on the W-frontier with  j >= 7  and  i >= 10.
```

## 3. Phase/class preservation (Issue §5.2) — proved

Accepted formulas (DLH-5V-A): `i_t(j) = floor((N - 10j)/7)`, `r_j = (N - 10j) mod 7`, `r_{j+7} = r_j` (period 7).
Exact mirror relations:

```
i_t(j+7) = floor((N - 10(j+7))/7) = floor((N - 10j)/7) - 10 = i_t(j) - 10
r_{j+7}  = (N - 10(j+7)) mod 7 = (N - 10j) mod 7 = r_j.
```

For a represented source with subtop offset `k = i_t(j) - i >= 0`, the destination
`(j+7, i-10)` has `i' = i - 10 = i_t(j) - 10 - k = i_t(j+7) - k`: **same class, same top/sub-top offset**.
- Destination represented: `i' >= 0` (from `i >= 10`) and `i' <= i_t(j+7)` (from `i <= i_t(j)`).
- Destination W-active: top cells are always W-active; sub-top cells are W-active iff `r_{j+7} = r_j in {0,1,2}` —
  preserved by period 7. (Exact spot-checks: `r_{j+7} = r_j`, `i_t(j+7) = i_t(j) - 10`, `i' <= i_t(j+7)` for
  represented sources — zero mismatches.)

## 4. Reverse-reallocation cone and rates (Issue §5.3) — proved

**Cone equality.** `cone{w_RT, w_down}` with `w_down = (0, -7/19)`:

```
mu = q_RT w_RT + q_down w_down,  q_RT, q_down >= 0
  => mu_a = (70/19) q_RT >= 0,  mu_b = -(70/19) q_RT - (7/19) q_down <= 0,
     mu_W = mu_a + mu_b = -(7/19) q_down <= 0.
```

Conversely every `mu in R_reverse = {mu_a > 0, mu_b < 0, mu_W <= 0}` (and its boundary closures) satisfies the
above with `q_RT = 19 mu_a / 70 >= 0` and `q_down = 19 (-mu_W) / 7 >= 0`. Hence

```
cone{w_RT, w_down} = {mu_a >= 0, mu_b <= 0, mu_W <= 0} = closure(R_reverse)  (exact).
```

**Candidate rates — proved exact:**

```
q_RT   = 19 * mu_a / 70
q_down = 19 * (-mu_W) / 7
```

**Exact first moment:**

```
q_RT w_RT + q_down w_down
  = (19 mu_a / 70)(+70/19, -70/19) + (19 (-mu_W)/7)(0, -7/19)
  = (mu_a, -mu_a) + (0, mu_W)
  = (mu_a, mu_W - mu_a) = (mu_a, mu_b).   (exact)
```

**Nonnegativity:** on `R_reverse`, `mu_a > 0` ⟹ `q_RT > 0`; `mu_W <= 0` ⟹ `q_down >= 0`. (Spot-check: any sample
with `mu_W > 0` fails the sector — correctly outside `T_W`, no transition invented.)

**Equality cases (audited, continuous vanishing):**

| case | rates | meaning |
|---|---|---|
| `mu_a = 0` (boundary with `R_deplete`) | `q_RT = 0`, `q_down = 19(-mu_W)/7 = 19(-mu_b)/7` | pure downward — identical to the both-inward rates on that ray |
| `mu_W = 0` (mirror sliding) | `q_down = 0`, `q_RT = 19 mu_a / 70` | pure mirror-wide sliding along the W-frontier (rate `19 mu_a/70`, matching the accepted forward sliding rate `19|mu_b|/70` since `mu_a = -mu_b`) |

Both rates are continuous linear functions of the drift — no ambiguity, no tie-breaking.

**Uniqueness:** `det[w_RT w_down] = (70/19)(-7/19) - (-70/19)(0) = -490/361 != 0`, so `{w_RT, w_down}` is a basis of
`R^2` and the nonnegative decomposition is **unique** for every `mu in R_reverse`; the two equality cases above are
boundary values of the same unique map.

**Refinement scaling (fixed-aspect family `da_h = h·10/19`, `db_h = h·7/19`):** `q_RT^h = 19 mu_a/(70 h)`,
`q_down^h = 19 (-mu_W)/(7 h)`; physical jumps `O(h)`, rates `O(1/h)`, first moment exact at every `h`.

## 5. Reverse-sector scoring semantics (Issue §5.4) — frozen (sector-candidate scoring, not a standalone argmax)

For each admissible candidate control with `mu in R_reverse`, with destinations `s_RT = (j+7, i-10)` and
`s_down = (j, i-1)` (both represented in the declared regular region), freeze the candidate's discrete score

```
H_h^reverse(c,l,d)
 = u(c) - v(l)
 + q_RT(c,l,d) [V_{s_RT} - V_s]
 + q_down(c,l,d)[V_{s_down} - V_s]
 + switch_z.
```

The rates are computed **for each candidate control before maximization**. This is a **sector-candidate scoring
rule** only; the single global regular-W-boundary argmax is composed across all sectors in the closure contract
(Issue §9 / both-inward-and-closure report). No continuous-max -> clip -> remap.

## 6. Verification log (tiny exact Fraction checks, `dlh5ve_closure.py`, `%TEMP%`)

1. `det[w_RT w_down] = -490/361 != 0`; `det[w_left w_down] = 70/361 != 0`.
2. Reverse first moment exact + nonnegative for samples in `R_reverse` (`(3,-1)`@`mu_W=2` correctly rejected as
   outside `T_W`; `(2,-2)` sliding; `(1/2,-3)`; `(0,-2)` boundary) — zero mismatches.
3. Mirror geometry: index preservation `10(j+7)+7(i-10) = 10j+7i`; `i' <= i_t(j+7)`; `r_{j+7} = r_j`;
   `i_t(j+7) = i_t(j) - 10` — zero mismatches (off-frontier source sample correctly flagged).

Result: **zero mismatches**.
