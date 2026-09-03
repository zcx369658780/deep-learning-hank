# DLH-5U Rev 1 — Tangential Reallocation and Consistency (Issue #47, Phase 9 + 14)

**Rev 1 status:** DOCUMENTATION / ANALYTIC CORRECTION ONLY. Repairs BLOCKER 2 per
reviewer comment `5521119160`. Withdraws the Rev-0 first-order consistency claims for
the tangential cascade, derives the exact-tangent benchmark, downgrades the cascade
to a diagnostic/candidate construction, and identifies the bounded unresolved object.
No numerical experiment.

---

## 1. Test object (unchanged)

At the physical W frontier the accepted continuous law admits the tangential drift

```text
mu_a < 0,  mu_b > 0,  mu_W = mu_a + mu_b <= 0
```

with the W1 masked lattice `da = 10/19 != db = 7/19` (face tangent off-axis).
DLH-5T Outcome B: pure axial node-to-node transitions do not uniquely preserve the
local process. Rev 1 keeps the face-flux primitive (Phase-8 rule) over the corrected
Rev-1 tessellation (restricted Voronoi cells).

## 2. Local geometry (Rev 1)

Per geometry report: `C_s` is the restricted-Voronoi cell of the represented node
`(i,j)`; `omega_s = area(C_s)`; shared faces `F_{s,r}`, physical W segment `F_s^W`.
For the benchmark the only structural facts used are: the available axial moves in the
needed quadrant from a W-frontier cell are `(i,j-1)` (displacement `(-da, 0)`) and,
via the inward cell, `(0, +db)`; and `da/db = 10/7` fixed.

## 3. Frozen conservative monotone construction (what IS frozen and viable)

The face-flux CTMC (Phase-8 rule) is frozen:

```text
q_{s->r} = |F_{s,r}| * max( mu_s(c,l,d) . n_{s,r} , 0 ) / omega_s
Q[s,s]   = - sum_{r != s} q_{s->r}
```

Properties (frozen, all verified): off-diagonal `>= 0` (monotonicity); row sums
exactly `0` (conservation); no outward W-normal flux (KKT `mu_W <= 0`); masked
destinations not assembled and not in the diagonal; same `Q` for `Q V` and `Q^T p`;
cell control maximizes the discrete Hamiltonian `H_h` (Phase-8 report); z-switch and
negative-b borrowing-rate-gap preserved.

**What is NOT frozen:** the tangential drift representation at W-adjacent cells. The
Rev-0 claim that the two-step cascade is first-order sequence-consistent is withdrawn
(Section 4).

## 4. Exact-tangent benchmark (BLOCKER 2) — derivation

**Benchmark:** `mu_a = -u`, `mu_b = +u`, `mu_W = 0` (exact sliding along the W face),
fixed accepted aspect ratio `da/db = 10/7`, `u > 0`.

**Stated two-step cascade:** `s --(rate r_a, a-down by da)--> (i,j-1) --(rate r_b,
b-up by db)--> (i+1,j-1)`, with `r_a, r_b > 0`.

**Mean waiting time per cycle:**

```text
tau = 1/r_a + 1/r_b        (exp. waiting times add; both O(h) as h -> 0)
```

**Mean displacement per cycle:** `(Delta a, Delta b) = (-da, +db)`.

**Effective continuous-time drift** (law-of-large-numbers rate for the cycle):

```text
( dE[a]/dt , dE[b]/dt ) = ( -da/tau , +db/tau )
effective W-drift:  dE[W]/dt = (db - da)/tau
```

**Consistency condition:** the discrete effective drift must equal the target
`(-u, +u)`:

```text
-da/tau = -u   and   +db/tau = +u   ==>   tau = da/u = db/u   ==>   da = db
```

On the accepted grid `da/db = 10/7 != 1` this is **impossible for any positive
`r_a, r_b`**. Hence the two-step axial cascade cannot reproduce the tangent benchmark.

**Concrete rates (face-flux):**

- Half-cell normalization (Rev-0 base-clipped): `r_a = 2u/da`, `r_b = u/db`:

  ```text
  tau = da/(2u) + db/u
  dE[a]/dt = -u*(da/db)/(da/(2db)+1) = -(5/6)u
  dE[b]/dt =  u/(da/(2db)+1)          = +(7/12)u
  dE[W]/dt = -(5/6)u + (7/12)u        = -(1/4)u   != 0
  ```

- Full-cell normalization (as if `omega_s = da*db`): `r_a = u/da`, `r_b = u/db`:

  ```text
  tau = da/u + db/u
  dE[a]/dt = -u/(1+db/da) = -(10/17)u
  dE[b]/dt =  u/(1+da/db) =  +(7/17)u
  dE[W]/dt = -(10/17)u + (7/17)u = -(3/17)u   != 0
  ```

Both effective drifts are **O(1), independent of `h` at fixed aspect ratio**, and
both carry a spurious inward W-drift (`mu_W^eff < 0`). Because the per-cycle waiting
time is also `O(h)`, the `O(h)` per-cycle wealth displacement `db - da` does NOT yield
`O(h)` normal drift — it yields `O(1)`. This is exactly the reviewer's point.

**Pointwise generator at the cut cell:** `(Q V)_s = r_a(V_{(i,j-1)} - V_s) ~ r_a(-da V_a)`.
With `r_a = 2u/da`: `(Q V)_s ~ -2u V_a` (a-coefficient doubled, `u V_b` term absent).
With `r_a = u/da`: `(Q V)_s ~ -u V_a` (a-coefficient correct, `u V_b` term absent).

**Withdrawn claims (Rev-0), not replaced by a valid derivation:**
- "cascade is first-order sequence-consistent";
- "tangential composition OK in the limit";
- "global first-order cut-cell consistency" (as a statement about the tangential
  representation at fixed aspect ratio).

## 5. Oblique one-step construction (diagnostic only)

A one-step oblique move `s -> (i+1,j-1)` (displacement `(-da, +db)`) at rate `r_diag`,
plus a-down `r_a`, gives

```text
(Q V)_s ~ r_a(-da V_a) + r_diag(-da V_a + db V_b)
```

Matching `(-u, +u)`: `r_diag = u/db`; `r_a = u/da - u/db = u(db-da)/(da db)`.
On the accepted grid `db < da`, so `r_a < 0` — **not monotone**. Withdraw as a frozen
viable scheme; retain only as a diagnostic of why one-step tangential transport is
obstructed on the `da != db` lattice (the one-step achievable generator cone has slope
bounded by `db/da = 7/10`, below the physical tangent ratio 1).

## 6. The bounded unresolved object (reviewer's path B)

Route F's face-flux framework is scientifically viable (monotone, conservative,
same-process, no outward W flux — Section 3), but **no frozen construction reproduces
the admissible tangential cone at W-adjacent cells**:

- the two-step axial cascade has an `O(1)` spurious normal drift at fixed aspect
  ratio (Section 4);
- the oblique one-step exact-moment construction is not monotone on the accepted grid
  (Section 5);
- no alternative monotone, conservative, pointwise-consistent discrete boundary
  process is established in this gate.

Therefore the cascade is **downgraded to a diagnostic/candidate construction**, and
the following is retained as **THE bounded unresolved object (frozen statement)**:

```text
A conservative, monotone, same-process discrete boundary process whose effective
generator reproduces the full admissible tangential cone at the W face
( mu_b >= 0, mu_a <= 0, mu_W <= 0, including the mu_W = 0 sliding benchmark )
on the accepted da/db = 10/7 W1 grid.
```

No impossibility is proven (only the failure of the two frozen candidates), so Route F
remains scientifically viable in the framework sense and Outcome C is NOT triggered;
this is the precisely bounded design object that keeps the gate at Outcome B.

## 7. Consistency audit (Issue #47 §14, Rev 1)

| # | Requirement | Rev-1 status |
|---|---|---|
| 14.1 | Markov monotonicity | OK (frozen face-flux construction; oblique not monotone → diagnostic only) |
| 14.2 | Conservation (row sums 0) | OK |
| 14.3 | Adjoint mass conservation | OK |
| 14.4 | Local first-moment / drift consistency toward `(mu_a,mu_b)` | **UNRESOLVED at W-adjacent cells** (tangent benchmark fails, Section 4); interior cells OK |
| 14.5 | Physical W-normal boundary consistency | OK (KKT `mu_W <= 0`; W segment zero flux; no KFE clipping) |
| 14.6 | Tangential asset-composition consistency | **UNRESOLVED** (same object as 14.4; no arbitrary b-to-a transfer is introduced, but the tangential representation itself is not established) |
| 14.7 | Refinement consistency `h -> 0` | **NOT established for the tangential representation at fixed aspect ratio** (O(1) error, Section 4); the Rev-0 first-order claim is withdrawn |
| 14.8 | Interior-operator junction | OK (identical face-flux formula) |
| 14.9 | z-switch preservation | OK |
| 14.10 | Negative-b borrowing-rate-gap | OK (lives in `mu_b` accounting; untouched) |

## 8. Compliance

No generator assembled, no HJB/KFE solved, no execution. Symbolic/local analytic
derivations only (mean-waiting-time and effective-drift algebra; generator-action
truncation).
