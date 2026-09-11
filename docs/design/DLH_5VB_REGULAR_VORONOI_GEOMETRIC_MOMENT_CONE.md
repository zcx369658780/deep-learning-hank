# DLH-5V-B — Regular Restricted-Voronoi Geometric Moment-Cone (Umbrella Design)

**Issue:** deep-learning-hank #50 (DLH-5V-B) · **Task type:** `SCIENTIFIC_DESIGN__REGULAR_VORONOI_GEOMETRIC_MOMENT_CONE`
**Branch:** `dsh/issue-50-dlh-5vb-regular-voronoi-moment-cone-2026-09-11` · **Activation:** comment `5628392741`
(`DLH_5VB_REGULAR_VORONOI_GEOMETRIC_MOMENT_CONE_AUTHORIZED`), activation `origin/main` = `3cdcde1284b39b3f426fbb6b3feed1d53884ed0c`
**Status:** geometric feasibility analysis submitted for fresh ChatGPT review — **NOT scientific acceptance**.
Owner continuation decision: `APPROVE_DLH_5VB_REGULAR_VORONOI_GEOMETRIC_MOMENT_CONE_GATE`.

## 1. Frozen inputs (consumed from accepted DLH-5V-A / Issue #49 — not re-derived)

Physical displacement map `Delta x_sr = ((10/19) Delta j, (7/19) Delta i)`; W-active regular classes:

```
A^F: (-1,0), (0,-1), (-1,+1), (+1,-1)
A^L: (-1,0), (0,-1), (-1,+1)
B^W: (-1,0), (0,-1), (0,+1), (+1,-1)
```

No oblique or longer regular shared-face neighbor exists under accepted authority.

## 2. Question of this gate

Can the accepted regular W-frontier shared-face displacement sets generate the continuous admissible
tangential reallocation cone `T_realloc = {mu_a<=0, mu_b>=0, mu_a+mu_b<=0}` with **nonnegative** local
CTMC coefficients, i.e. `T_realloc ⊆ K_s = cone{Delta x_sr}`? Mandatory exact sliding ray `mu = (-u, +u)`.

## 3. Submitted candidate results (exact algebra; analysis report = file 4)

| class | `K_s` | sliding `(-u,+u)` | `T_realloc ⊆ K_s` | `T_realloc ∩ K_s` | obstruction |
|---|---|---|---|---|---|
| A^F (`r∈{3,4,5,6}`) | half-plane `{7 mu_a + 10 mu_b <= 0}` | **NOT in K** (`7(-u)+10u = 3u > 0`) | **NO** | `cone{(-1,0), (-10/19,+7/19)}` | **YES** (slope bound `7/10` < 1) |
| A^L (`r∈{0,1,2}`) | pointed `{mu_a <= 0, 7 mu_a + 10 mu_b <= 0}`; extreme rays `(0,-7/19)`, `(-10/19,+7/19)` | **NOT in K** (`3u > 0`) | **NO** | `cone{(-1,0), (-10/19,+7/19)}` | **YES** (slope bound `7/10` < 1) |
| B^W (`r∈{0,1,2}`) | `R^2` | **in K** (exact `(19u/10)·(-10/19,0) + (19u/7)·(0,+7/19)`) | **YES** | `T_realloc` | none |

Key exact facts: the index diagonal image `(-10/19,+7/19)` **is** in `K^F` and `K^L` (it is a generator /
extreme ray), but the **physical** 45° ray `(-u,+u)` (W-line tangent, slope 1) is not, because top-cell cones
admit at most slope `7/10` (the grid anisotropy `db/da`). The separating form
`ell(mu) = 7 mu_a + 10 mu_b` is the exact Farkas-style certificate for both top-cell classes.

## 4. Bounded meaning and phase-uniformity

The proven obstruction is **bounded**: the accepted restricted-Voronoi **local shared-face** transition
geometry cannot represent the full continuous tangential reallocation cone for the recurring top-cell classes
**A^F and A^L** with nonnegative local coefficients. It does **not** imply Route F is impossible in every
discretization, and no remedy is designed here (Owner-route question). The result is class-uniform over
`theta in [0,1)`, uniform over every period-7 occurrence of each class, and independent of `N mod 7` except
through per-column class assignment.

## 5. Same-process implication (design statement only)

Under `HJB boundary policy <=> KFE boundary transition law`: an HJB policy selecting an admissible drift
outside `K_s` (in particular `(-u,+u)`) cannot be represented by a monotone local CTMC using only the
accepted shared-face neighbors without changing the controlled process. No rates or repairs are constructed.

## 6. Deferred / forbidden in this gate

Deferred: source-state face-flux moment maps; production rates; nonlocal/alternative transitions;
endpoints/corners; sliver/agglomeration semantics; HJB/KFE implementation; stationary KFE; numerical `W_max`;
aggregates/GE/neural objects. Forbidden: source/economics mutation; broad phase/Voronoi enumeration;
PR/merge/close/successor/self-accept.

## 7. File map (exact four-file allowlist)

1. This umbrella design document.
2. `reports/dlh_5vb_regular_moment_cone_2026_09_11/DLH_5VB_AUTHORITY_CAPSULE.md` — authority digest.
3. `reports/dlh_5vb_regular_moment_cone_2026_09_11/DLH_5VB_MOMENT_CONE_ANALYSIS.md` — full exact-algebra analysis.
4. `reports/dlh_5vb_regular_moment_cone_2026_09_11/DLH_5VB_TERMINAL_AND_FORBIDDEN_CHECK.md` — single terminal
   (Outcome C) + forbidden-operation check + fresh state report.
