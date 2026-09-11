# DLH-5V-B — Regular Restricted-Voronoi Geometric Moment-Cone Analysis

**Issue:** deep-learning-hank #50 (DLH-5V-B) · **Task type:** `SCIENTIFIC_DESIGN__REGULAR_VORONOI_GEOMETRIC_MOMENT_CONE`
**Branch:** `dsh/issue-50-dlh-5vb-regular-voronoi-moment-cone-2026-09-11` · **Activation:** comment `5628392741` (`DLH_5VB_REGULAR_VORONOI_GEOMETRIC_MOMENT_CONE_AUTHORIZED`), activation `origin/main` = `3cdcde1284b39b3f426fbb6b3feed1d53884ed0c`
**Parent of this analysis:** accepted DLH-5V-A / Issue #49 (candidate `58a0efe2e85b497d8b19c306a831d865ed65136d`, acceptance `5628285587`). Frozen geometry is consumed, **not re-derived**.

---

## 1. Setup and conventions

Frozen physical displacement map (DLH-5V-A, accepted):

```
Delta x_sr = ((10/19) Delta j, (7/19) Delta i)
```

For each W-active regular class `s` the local nonnegative displacement cone is

```
K_s = cone{ Delta x_sr : r in N_V(s) }   (nonnegative linear combinations only)
```

All vectors below are **physical asset-space directions** `mu = (mu_a, mu_b)` in `(a, b)` units. The grid
anisotropy ratio is `db/da = 7/10`. Because a cone is invariant under a common positive scaling of all its
generators, all exact work is done with the integer-scaled generators `(10 Delta j, 7 Delta i)`; inequalities
are stated in physical units (a common factor does not change signs).

Continuous admissible reallocation cone at the W boundary (given by the Issue):

```
T_realloc = { (mu_a, mu_b) : mu_a <= 0, mu_b >= 0, mu_a + mu_b <= 0 }
```

**Do not confuse the two diagonals:**
- index diagonal `(-1,+1)` → physical `(-10/19, +7/19)` (slope `(7/19)/(10/19) = 7/10`);
- physical 45° diagonal `(-u, +u)`, `u > 0` (slope 1; tangent to the W-line `a+b = const`).

---

## 2. Class A^F — W-active top, `r in {3,4,5,6}`

Neighbors (index): `(-1,0), (0,-1), (-1,+1), (+1,-1)`; physical generators:

```
g1 = (-10/19, 0)        [index (-1,0)]
g2 = (0, -7/19)         [index (0,-1)]
g3 = (-10/19, +7/19)    [index (-1,+1)]
g4 = (+10/19, -7/19)    [index (+1,-1)]  = -g3
```

### 2.1 Extreme rays / half-space representation

`g4 = -g3`, so `cone{g3, g4}` is the **full line** `span{(10/19, -7/19)}`. The cone is therefore the closed
**half-plane**

```
K^F = { 7 mu_a + 10 mu_b <= 0 }        (physical units)
```

Proof of containment: the linear form `ell(mu) = 7 mu_a + 10 mu_b` evaluates to `-70/19, -70/19, 0, 0` on
`g1..g4`, hence `ell <= 0` on every nonnegative combination. Proof of covering: for any `mu` with
`ell(mu) <= 0`, `mu = t·(-10,0) + c·(10,-7)` (scaled by 19) with `t = -(7 mu_a + 10 mu_b)/70 >= 0` and
`c = -mu_b/7` any real sign (both `(10,-7)` and `(-10,7)` are generators) — so `mu in K^F`. (Exact Fraction
check §12 confirms all generators satisfy `ell <= 0` with maximum exactly `0`.)

- Extreme rays: **none** (non-pointed); the cone is the half-plane bounded by the line `7 mu_a + 10 mu_b = 0`,
  whose two edge directions are `(10/19, -7/19)` and `(-10/19, +7/19)` (an antipodal pair).
- Minimal nonnegative generating set: the antipodal pair `{(-10/19, +7/19), (+10/19, -7/19)}` plus any
  interior direction, e.g. `(-10/19, 0)` (equivalently `(0, -7/19)`).

### 2.2 The index diagonal image `(-1,+1) -> (-10/19, +7/19)`

`(-10/19, +7/19) = g3` is an **exact generator**, hence `(-10/19, +7/19) in K^F` (on the boundary,
`ell = 0`).

### 2.3 Mandatory sliding test `mu = (-u, +u)`, `u > 0`

```
ell(-u, +u) = 7(-u) + 10(+u) = 3u > 0   for all u > 0
```

while `ell <= 0` on all of `K^F`. Hence `(-u, +u) notin K^F` for every `u > 0` — **the sliding ray is
NOT representable by class A^F**. No nonnegative coefficients `q_k >= 0` solve
`sum q_k Delta a_k = -u`, `sum q_k Delta b_k = +u`.

### 2.4 `T_realloc subseteq K^F`?

`T_realloc = cone{(-1,0), (-1,1)}` (extreme rays proven in §5). The generator `(-1,1)` satisfies
`ell(-1,1) = 3 > 0`, so `(-1,1) notin K^F`. **No**: `T_realloc ⊄ K^F`.

### 2.5 Exact representable subset `T_realloc ∩ K^F`

With `T_realloc ∋ mu = alpha(-1,1) + beta(-1,0) = (-alpha-beta, alpha)`, `alpha, beta >= 0`:

```
ell(mu) = 3 alpha - 7 beta <= 0  <=>  beta >= (3/7) alpha
```

so

```
T_realloc ∩ K^F = { alpha(-1,1) + beta(-1,0) : alpha >= 0, beta >= (3/7) alpha }
                = cone{ (-1, 0), (-10/19, +7/19) }        (physical)
```

Extreme rays: `(-1, 0)` (shared edge) and `(-10/19, +7/19)` (intersection of the interior of `T_realloc`
with the boundary `7 mu_a + 10 mu_b = 0`). Every direction of `T_realloc` with reallocative steepness
`mu_b/(-mu_a) <= 7/10` is representable; every direction with `mu_b/(-mu_a) > 7/10` is not.

### 2.6 Obstruction certificate (exact, Farkas-style)

The separating linear form `ell(mu) = 7 mu_a + 10 mu_b` satisfies `ell <= 0` on `K^F` yet
`ell(-1,1) = 3 > 0`. Equivalently, on `K^F` the physical slope bound is exact:

```
mu_b <= (7/10) (-mu_a)        i.e.   max mu_b/(-mu_a) = 7/10   (attained at the grid diagonal)
```

while the sliding ray `(-u,+u)` requires slope `1 > 7/10`. This is a **genuine geometric obstruction** for
the recurring class A^F under the accepted local shared-face CTMC semantics.

---

## 3. Class A^L — W-active top, `r in {0,1,2}`

Neighbors (index): `(-1,0), (0,-1), (-1,+1)`; physical generators `g1, g2, g3` as in §2. Note
`g1 = g3 + g2` (exact: `(-10/19, 0) = (-10/19, +7/19) + (0, -7/19)`), so `g1` is redundant.

### 3.1 Extreme rays / half-space representation

```
K^L = cone{ g2, g3 } = cone{ (0, -7/19), (-10/19, +7/19) }   (pointed cone)
    = { mu_a <= 0 } ∩ { 7 mu_a + 10 mu_b <= 0 }              (physical units)
```

- Extreme rays: `(0, -7/19)` and `(-10/19, +7/19)`.
- Equivalent inequalities: `mu_a <= 0` and `7 mu_a + 10 mu_b <= 0` (both hold on all generators, maxima 0).

### 3.2 Index diagonal image

`(-10/19, +7/19) = g3` is an **extreme ray** of `K^L`, so `(-10/19, +7/19) in K^L`.

### 3.3 Mandatory sliding test

```
ell(-u, +u) = 3u > 0
```

while `ell <= 0` on `K^L`; also `mu_a = -u <= 0` would be satisfied, so the failure is **exclusively the
slope bound**: `(-u, +u) notin K^L` for all `u > 0`.

### 3.4 `T_realloc subseteq K^L`?

No: `(-1,1) in T_realloc` but `ell(-1,1) = 3 > 0`. (`T_realloc ⊆ {mu_a <= 0}` already, so the extra
half-space of `K^L` adds nothing beyond §2.)

### 3.5 Exact representable subset

```
T_realloc ∩ K^L = cone{ (-1, 0), (-10/19, +7/19) }      (identical to the A^F intersection)
```

### 3.6 Obstruction certificate

Same certificate as §2.6: `ell(mu) = 7 mu_a + 10 mu_b` separates `K^L` (`ell <= 0`) from the sliding ray
(`ell(-1,1) = 3 > 0`); exact slope bound `mu_b/(-mu_a) <= 7/10` on `K^L` vs required slope 1. **Genuine
geometric obstruction** for the recurring class A^L.

---

## 4. Class B^W — W-active sub-top, `r in {0,1,2}`

Neighbors (index): `(-1,0), (0,-1), (0,+1), (+1,-1)`; physical generators:

```
g1 = (-10/19, 0)
g2 = (0, -7/19)
g3 = (0, +7/19)      [index (0,+1)]  = -g2
g4 = (+10/19, -7/19)
```

### 4.1 Extreme rays / half-space representation

`g3 = -g2`, so `cone{g2, g3}` is the **full vertical line** `span{(0,1)}`. Together with
`g1 = (-10/19, 0)` (covers all `x <= 0` with the vertical line) and `g4 = (10/19, -7/19)` (covers all
`x >= 0` with the vertical line):

```
K^B = R^2        (the whole plane; every physical direction is representable)
```

- Extreme rays: **none**; no nontrivial equivalent inequality (unconstrained cone).
- `ell` is **not** a supporting functional: `ell(g3) = +70/19 > 0` (exact check §12).

### 4.2 Index diagonal image

`(-10/19, +7/19) in K^B` — representable as `g1 + g3 = (-10/19, 0) + (0, +7/19)` (note: **not** a direct
neighbor direction of B^W, but an exact nonnegative combination with coefficients `(1, 1)`).

### 4.3 Mandatory sliding test

`(-u, +u) in K^B = R^2` — explicit nonnegative coefficients:

```
q1 = 19u/10 on g1 = (-10/19, 0)   ->  (-u, 0)
q3 = 19u/7  on g3 = (0, +7/19)    ->  (0, +u)
sum = (-u, +u)                    (exact, q1, q3 >= 0)
```

### 4.4 `T_realloc subseteq K^B`?

**Yes** (trivially, since `K^B = R^2`).

### 4.5 Exact representable subset

`T_realloc ∩ K^B = T_realloc = cone{(-1,0), (-1,1)}`.

### 4.6 Obstruction

**None** for B^W.

---

## 5. Structure of `T_realloc` (exact)

```
T_realloc = { mu_a <= 0, mu_b >= 0, mu_a + mu_b <= 0 } = cone{ (-1, 0), (-1, 1) }   (physical)
```

Extreme rays: `(-1, 0)` (from `mu_b = 0`) and `(-1, 1)` (from `mu_a + mu_b = 0`; the corner `mu_a = 0`
degenerates to `(0,0)`). The sliding ray `(-u, +u)` is exactly the interior of the `(-1,1)` extreme ray.

---

## 6. Mandatory sliding test — summary

| class | `(-u,+u) in K_s` ? | exact reason |
|---|---|---|
| A^F | **NO** | `ell(-u,+u) = 3u > 0` vs `ell <= 0` on `K^F` |
| A^L | **NO** | `ell(-u,+u) = 3u > 0` vs `ell <= 0` on `K^L` (the `mu_a <= 0` part would pass) |
| B^W | **YES** | `(-u,+u) = (19u/10)·g1 + (19u/7)·g3` |

The failure of the sliding ray for the two recurring top-cell classes is **not** an index/diagonal
convention artifact: the index diagonal image `(-10/19, +7/19)` *is* in `K^F` and `K^L` (it is a generator /
extreme ray), but the **physical** 45° direction `(-u,+u)` (tangent to the W-line, slope 1) is not, because
`K^F, K^L` admit at most slope `7/10`.

---

## 7. `T_realloc` vs `K_s` — exact summary

| class | `K_s` (equivalent representation) | `(-10/19,+7/19) in K_s` | `(-u,+u) in K_s` | `T_realloc ⊆ K_s` | `T_realloc ∩ K_s` |
|---|---|---|---|---|---|
| A^F | `{7 mu_a + 10 mu_b <= 0}` (half-plane) | YES (generator, boundary) | **NO** | **NO** | `cone{(-1,0), (-10/19,+7/19)}` |
| A^L | `{mu_a <= 0, 7 mu_a + 10 mu_b <= 0}` (pointed) | YES (extreme ray) | **NO** | **NO** | `cone{(-1,0), (-10/19,+7/19)}` |
| B^W | `R^2` | YES (`g1 + g3`) | YES | YES | `T_realloc` |

---

## 8. Obstruction certificates (exact)

For A^F and A^L the single separating linear form `ell(mu) = 7 mu_a + 10 mu_b` is an exact Farkas-style
certificate:

```
ell(K_s) ⊆ (-inf, 0]   and   ell(-1, 1) = 3 > 0   =>   (-1, 1) notin K_s,
equivalently   (-u, +u) notin K_s for all u > 0   (sliding ray).
```

Physical reading: on the accepted geometry, a b-gain of `+Delta b` per a-loss `-Delta a` is bounded by the
grid anisotropy `Delta b / (-Delta a) <= 7/10` for the top-cell classes; the continuous reallocation cone
requires ratios up to `1`.

---

## 9. Phase-uniformity (Issue §9)

The cone `K_s` depends only on (i) the class's neighbor displacement **set** — which DLH-5V-A established to
be structurally `theta`-independent on `theta in [0,1)` and periodic with period 7 — and (ii) the fixed grid
anisotropy `(10/19, 7/19)`. `N mod 7` enters only through **which** class occurs at a given column
(`r in {3,4,5,6}` → A^F; `r in {0,1,2}` → A^L on the top and B^W on the sub-top). Hence the moment-cone
result is:

- **class-uniform over all `theta`** in `[0,1)`;
- **uniform over every occurrence** of each class within the period-7 regular frontier;
- **independent of `N mod 7`** except through per-column class assignment.

No new phase enumeration was performed.

---

## 10. Same-process implication — design statement only (Issue §8)

Under the binding law `HJB boundary policy <=> KFE boundary transition law`: for the recurring top-cell
classes A^F and A^L, an HJB boundary policy selecting an admissible continuous drift outside `K_s` — in
particular the physical sliding ray `(-u, +u)` (pure 1:1 reallocation along the W-line) — **cannot be
represented by a monotone local CTMC** using only the accepted shared-face neighbors with nonnegative
coefficients, without changing the controlled process. This is recorded as a design statement only; no rates
or KFE repairs are constructed in this gate.

---

## 11. Interpretation ceiling (Issue §7)

The conclusion is **bounded**:

> The currently accepted restricted-Voronoi **local shared-face transition geometry** cannot represent the
> full continuous tangential reallocation cone `T_realloc` for the recurring top-cell classes **A^F** and
> **A^L** with nonnegative local coefficients. Class **B^W** (recurring sub-top) has **no** obstruction
> (`K^B = R^2`).

This does **not** imply that the entire finite-domain Route F is impossible in every conceivable
discretization, and no remedy (nonlocal transitions, augmented boundary states, transformed coordinates,
different finite-volume semantics, W2) is designed here — those are Owner-route questions for a later Issue.

---

## 12. Verification log

Exact symbolic spot checks only (tiny scratch script `dlh5vb_moment_cone.py` in `%TEMP%`, **not committed**;
exact `Fraction` arithmetic; no numerical sweeps):

1. Half-space forms: `max(7 mu_a + 10 mu_b)` over the generators of A^F = 0, of A^L = 0 (and `max mu_a = 0`);
   for B^W the max is `+70/19` (on `(0,+7/19)`), confirming B^W has no half-space bound.
2. `(-10/19, +7/19) in K_s` for all three classes with explicit nonnegative coefficients:
   A^F/A^L: `1·(-10/19,+7/19)` (generator); B^W: `1·(-10/19,0) + 1·(0,+7/19)`.
3. Sliding ray: `ell(-1,1) = 3 > 0` (certificate for A^F, A^L); B^W decomposition
   `(19u/10)·(-10/19,0) + (19u/7)·(0,+7/19) = (-u,+u)` exact.
4. `T_realloc = cone{(-1,0), (-1,1)}`: `ell(-1,0) = -7 in K^F/K^L`, `ell(-1,1) = 3 notin`.
5. `T_realloc ∩ K^F = T_realloc ∩ K^L = cone{(-1,0), (-10/19,+7/19)}`: boundary `beta = (3/7)alpha` and
   interior points recovered exactly with `s, t >= 0`.
6. `K^B = R^2`: representative directions (incl. `(-1,1)`, `(1,-1)`, `(-5,2)`, `(3,-4)`, `(-10,7)`) all
   recovered with exact nonnegative coefficients.
7. Slope bound: `(7/19)/(10/19) = 7/10` attained at the grid diagonal; sliding requires 1.

Result: **zero mismatches**. All membership/impossibility statements above are exact algebraic facts.

---

## 13. Checklist against Issue §4 items 1–5

| item | A^F | A^L | B^W |
|---|---|---|---|
| 1. extreme rays / half-space representation | half-plane `{7 mu_a+10 mu_b <= 0}` | pointed cone, extreme rays `(0,-7/19)`, `(-10/19,+7/19)`; `{mu_a <= 0, 7 mu_a+10 mu_b <= 0}` | `K = R^2`; none |
| 2. `(-1,+1)` (physical `(-10/19,+7/19)`) in `K_s` | YES (generator, boundary) | YES (extreme ray) | YES (`g1+g3`) |
| 3. `T_realloc ⊆ K_s` | **NO** | **NO** | YES |
| 4. exact `T_realloc ∩ K_s` | `cone{(-1,0), (-10/19,+7/19)}` | `cone{(-1,0), (-10/19,+7/19)}` | `T_realloc` |
| 5. genuine geometric obstruction | **YES** (slope bound `7/10` < 1) | **YES** (slope bound `7/10` < 1) | no |

Because at least one recurring accepted W-active regular class (A^F and A^L) has a proven nonnegative-cone
obstruction to the full admissible tangential cone, the terminal is **Outcome C** (Issue §14):
`DLH_5VB_REGULAR_VORONOI_LOCAL_SHARED_FACE_MOMENT_CONE_OBSTRUCTION__OWNER_ROUTE_DECISION_REQUIRED`.
