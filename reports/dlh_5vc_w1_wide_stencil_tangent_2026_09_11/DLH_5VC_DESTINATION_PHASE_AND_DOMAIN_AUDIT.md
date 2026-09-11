# DLH-5V-C — W1 Wide-Stencil Exact-Tangent Regular-Frontier Feasibility Audit (Destination, Phase, Domain)

**Issue:** deep-learning-hank #51 (DLH-5V-C) · **Branch:** `dsh/issue-51-dlh-5vc-w1-wide-stencil-tangent-2026-09-11`
**Parent authority:** accepted DLH-5V-B (Issue #50, candidate `6bc8612dc10de6d72d27c9c47d1b4d598a70a15d`, acceptance `5628629099`).
This report covers Issue §5.1 (represented destination), §5.2 (phase/class preservation), §5.7 (hidden path), and the
endpoint-band identification. Exact algebra only; tiny exact Fraction spot-checks in `%TEMP%` (not committed); no sweeps.

---

## 1. Primitive/minimal exact tangent (Issue §4 requirement)

The native-lattice tangent condition is `10 Delta j + 7 Delta i = 0`. Because `gcd(10,7) = 1`, every integer
solution satisfies `7 | Delta j` and `10 | Delta i`; writing `Delta j = 7k` gives `10·7k + 7 Delta i = 0`, so
`Delta i = -10k`. Hence the complete integer tangent lattice is

```
(Delta j, Delta i) = k·(7, -10),   k in Z.
```

The reallocation direction (`Delta a < 0`, `Delta b > 0`) requires `k < 0`; the **primitive (minimal)**
solution is `k = -1`:

```
v_T = (-7, +10),   Delta x_T = ((-10/19)·7, (7/19)·10) = (-70/19, +70/19).
```

Minimality: any other integer tangent is an integer multiple `m·(-7,+10)`, `|m| >= 2`, with index Manhattan
distance `17|m| >= 34 > 17`; the minimal nonzero index distance on the tangent lattice is exactly
`|-7| + |+10| = 17`. `Delta a + Delta b = 0` holds exactly, but this alone is not the validity criterion —
the full audits below are the criterion.

## 2. Represented-destination availability (Issue §5.1)

**Represented condition** (accepted DLH-5V-A reduction): node `(j,i)` is represented iff
`10j + 7i <= N` (independent of `theta in [0,1)`).

**Destination identity** (exact):

```
10(j-7) + 7(i+10) = 10j - 70 + 7i + 70 = 10j + 7i.
```

**Theorem (destination representation).** For every represented source `(j,i)` with `j >= 7`, the wide
destination `(j-7, i+10)` is represented:

```
10(j-7) + 7(i+10) = 10j + 7i <= N.
```

(The condition `j >= 7` defines the **declared regular-wide admissibility region** for the domain audit.)

**Domain audits (physical units).**

| audit | computation | result |
|---|---|---|
| `a >= 0` | `a' = (j-7)·10/19 >= 0  <=>  j >= 7` | holds in the admissibility region; **fails for `j < 7`** |
| `b >= b_min` | `b' = b_min + (i+10)·7/19 >= b_min  <=>  i >= -10` | automatic (represented nodes have `i >= 0`; `i+10 >= 10`) |
| `a <= a_max` | `a' = a - 70/19 < a <= a_max` | automatic (a decreases) |
| W-domain membership | `a' + b' = (a - 70/19) + (b + 70/19) = a + b <= W_max` | automatic (W unchanged) |
| full straight segment in `D_W` | `x(t) = (a - t·70/19, b + t·70/19)`, `t in [0,1]`: `a(t)+b(t) = a+b`; `a(t)` decreases to `a - 70/19`; `b(t)` increases | inside `D_W` for all `t` iff `a >= 70/19`, i.e. `j >= 7` |

**Staircase position of the destination.** With `i_t(j) = floor((N - 10j)/7)`,

```
i_t(j-7) = floor((N - 10(j-7))/7) = floor((N - 10j)/7 + 10) = i_t(j) + 10,
```

so `i + 10 <= i_t(j-7)` iff `i <= i_t(j)` — the destination sits at the same vertical offset in its column.

**Finite endpoint band to defer (precise).** The excluded regular-band is the **7-column strip adjacent to the
a-axis**:

```
j in {0, 1, ..., 6},   i.e. physical a < 7·(10/19) = 70/19.
```

In this band the wide destination (and the straight path) would leave `a >= 0`. This band is finite (7 columns,
independent of `N`), its physical width is `70h/19 -> 0` under the refinement family (§ of file 4), and its
relative column measure is `7/N_h = O(h)` — it is an endpoint/corner object, **not** a regular-region failure.
The regular-wide admissibility region is therefore: **regular W-active states with `j >= 7`**.

## 3. Phase/class preservation (Issue §5.2)

Defect (accepted): `r_j = (N - 10j) mod 7 = (N - 3j) mod 7`. Exact computation:

```
r_{j-7} = (N - 3(j-7)) mod 7 = (N - 3j + 21) mod 7 = (N - 3j) mod 7 = r_j,
```

since `21 ≡ 0 (mod 7)`. The map `j -> j-7` is the inverse of the accepted period-7 shift `j -> j+7`; no new
phase content. Hence **class preservation holds for every occurrence**:

```
r_j in {3,4,5,6}  (A^F)  ->  r_{j-7} in {3,4,5,6}  (A^F)
r_j in {0,1,2}    (A^L)  ->  r_{j-7} in {0,1,2}    (A^L)
r_j in {0,1,2}    (B^W)  ->  r_{j-7} in {0,1,2}    (B^W)
```

**Top/sub-top index relation.** If the source is top at column `j` (`i = i_t(j)`), then
`i' = i + 10 = i_t(j) + 10 = i_t(j-7)` — destination is top at column `j-7`. If the source is sub-top B
(`i = i_t(j) - 1`), then `i' = i_t(j-7) - 1` — destination is sub-top B. So both the class (defect) and the
top/sub-top offset are preserved exactly. No broad numerical phase sweep was performed (single exact
periodicity argument).

## 4. No hidden path violation (Issue §5.7)

Straight segment `x(t) = (a - t·70/19, b + t·70/19)`:

```
a(t) + b(t) = a + b   (constant for all t in [0,1])   ->  no artificial W-normal excursion.
```

`a(t)` decreases monotonically from `a` to `a - 70/19`; it crosses `a = 0` iff `a < 70/19`, i.e. `j < 7` —
confined to the deferred endpoint band. In the declared regular-wide region (`j >= 7`), `a(t) >= 0`, `b(t) >= b_min`,
`a(t) <= a_max`, `a(t)+b(t) <= W_max` for all `t`: the segment never leaves the finite domain and never crosses an
economic boundary. **No hidden path violation in the regular region.**

## 5. Verification log (tiny exact Fraction checks, `dlh5vc_wide_stencil.py`, `%TEMP%`)

1. Tangent lattice: solutions `k(7,-10)`, `k=-3..3` listed; `gcd(10,7)=1`; minimal nonzero index Manhattan
   distance = 17 (only `k = ±1`).
2. Destination identity: `10(j-7)+7(i+10) = 10j+7i` for `(j,i) in {(20,5),(13,8),(40,0),(7,0)}` — all equal.
3. `i_t(j-7) = i_t(j) + 10` for `j = 0..14` (N=100) — all exact.
4. `r_{j-7} = r_j` for `j = 0..20` (N=100) — all exact.
5. Path: `a(t)+b(t) = a+b` at `t in {0, 1/3, 1/2, 1}` — constant (exact).

Result: **zero mismatches**.
