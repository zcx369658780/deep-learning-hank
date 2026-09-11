# DLH-5V-E — Both-Inward Depletion and Full Regular-Sector Closure

**Issue:** deep-learning-hank #53 (DLH-5V-E) · **Branch:** `dsh/issue-53-dlh-5ve-remaining-regular-sector-2026-09-11`
Covers Issue §6.1–§6.3 (both-inward cone/rates, represented local destinations, scoring), §7 (no-double-counting /
conservative rows), §8 (full regular coverage), §9 (global regular discrete-Hamiltonian composition), §10
(same-process/KFE safeguards). Exact algebra only; tiny exact Fraction spot-checks in `%TEMP%` (not committed).

---

## 1. Both-inward depletion sector — local axial audit (Issue §6)

`R_deplete = {mu_a <= 0, mu_b < 0}` (then automatically `mu_W = mu_a + mu_b < 0`). Local axial basis:

```
w_left = (-10/19, 0)      (j,i) -> (j-1,i)
w_down = (0, -7/19)       (j,i) -> (j,i-1)
```

**Cone equality (proved).**

```
mu = q_left w_left + q_down w_down,  q_left, q_down >= 0
  => mu_a = -(10/19) q_left <= 0,  mu_b = -(7/19) q_down <= 0,
  => cone{w_left, w_down} = {mu_a <= 0, mu_b <= 0} = closure(R_deplete)  (exact).
```

**Candidate rates — proved exact:**

```
q_left = 19 * (-mu_a) / 10
q_down = 19 * (-mu_b) / 7
```

**Exact first moment:**

```
q_left w_left + q_down w_down
  = (19 (-mu_a)/10)(-10/19, 0) + (19 (-mu_b)/7)(0, -7/19)
  = (mu_a, 0) + (0, mu_b) = (mu_a, mu_b).   (exact)
```

**Nonnegativity:** on `R_deplete`, `mu_a <= 0` ⟹ `q_left >= 0`; `mu_b < 0` ⟹ `q_down > 0`.

**Equality boundaries (ownership made explicit):**
- `mu_a = 0` (shared ray with `R_reverse`): `q_left = 0`, `q_down = 19(-mu_b)/7` — identical to the reverse-sector
  rates on that ray (`q_RT = 0`, `q_down = 19(-mu_W)/7 = 19(-mu_b)/7`). Single-valued.
- `mu_b = 0` (shared ray with `T_realloc`): owned by the accepted `T_realloc` (rates `q_in = 19(-mu_W)/10 =
  19(-mu_a)/10`, `q_T = 0`); the `R_deplete` limit (`q_left = 19(-mu_a)/10`, `q_down = 0`) is identical. No conflict.

**Uniqueness:** `det[w_left w_down] = (-10/19)(-7/19) - 0 = 70/361 != 0` — basis of `R^2`; unique nonnegative
decomposition for every `mu in R_deplete`; equality boundaries are boundary values of the same unique map
(continuous, linear, no tie-breaking).

**Refinement scaling:** `q_left^h = 19(-mu_a)/(10 h)`, `q_down^h = 19(-mu_b)/(7 h)`; physical jumps `O(h)`, rates
`O(1/h)`, first moment exact at every `h`.

## 2. Represented local destinations (Issue §6.2) — proved

- `(j,i) -> (j-1,i)`: index `10(j-1)+7i = 10j+7i-10 < N`; available for `j >= 1`.
- `(j,i) -> (j,i-1)`: index `10j+7(i-1) = 10j+7i-7 < N`; available for `i >= 1`.

Both are interior-type (W strictly decreases) and are represented throughout the declared regular region
(`j >= 7`, `i >= 10`). Endpoint faces (`j = 0` or `i = 0`) are joint-boundary objects **not redesigned here**.

## 3. Depletion-sector scoring semantics (Issue §6.3) — frozen (sector-candidate scoring)

For each admissible candidate control with `mu in R_deplete`, with `s_left = (j-1,i)`, `s_down = (j,i-1)`:

```
H_h^deplete(c,l,d)
 = u(c) - v(l)
 + q_left(c,l,d) [V_{s_left} - V_s]
 + q_down(c,l,d)[V_{s_down} - V_s]
 + switch_z.
```

Rates computed **for each candidate before maximization**; sector-candidate scoring only (the single global
regular argmax is composed in §5). No post-hoc clipping.

## 4. No-double-counting and conservative row contract (Issue §7) — frozen

- Each sector uses exactly **one canonical basis / rate decomposition** (its own pair); the accepted `T_realloc`
  uses `{w_in, w_T}`, the reverse sector `{w_RT, w_down}`, the depletion sector `{w_left, w_down}`.
- No redundant shared-face/wide rates are added that reproduce the same drift: each sector's pair is a basis, so
  the nonnegative decomposition of any in-sector drift is unique (per-sector uniqueness + boundary-ray identity
  across sectors).
- All actual off-diagonal rates are nonnegative (proved per sector).
- The diagonal equals the **negative sum of actual represented outgoing rates only**; omitted/off-grid
  destinations may not leave behind a diagonal escape; `Q 1 = 0` holds **by construction** (no later row-sum
  repair). Productivity switching remains separate (`switch_z`).
- No numerical `Q` is assembled in this Issue.

## 5. Full regular-sector closure (Issue §8) — proved

**Partition/coverage theorem.**

```
T_W = {mu_W <= 0} = T_realloc  union  R_reverse  union  R_deplete
```

(disjoint up to shared boundary rays). Proof by sign-casing on `mu_b`: if `mu_b >= 0` then
`mu_a = mu_W - mu_b <= 0` and `mu in T_realloc`; if `mu_b < 0` then `mu_a > 0` gives `mu in R_reverse` (with
`mu_W <= 0`) and `mu_a <= 0` gives `mu in R_deplete` (whose `mu_W < 0` automatically).

**Boundary ownership (single-valued):**
- `B1: mu_b = 0, mu_a < 0` — owned by `T_realloc`; depletion limit identical (`q_left = q_in`, `q_down = q_T = 0`).
- `B2: mu_a = 0, mu_b < 0` — owned by `R_deplete`; reverse limit identical (`q_left = q_RT = 0`, `q_down` equal).
- `B3: mu_W = 0` — sliding ray: `mu_b >= 0` side owned by `T_realloc` (pure wide `q_T = 19 mu_b/70`), `mu_b < 0`
  side owned by `R_reverse` (pure mirror `q_RT = 19 mu_a/70 = 19(-mu_b)/70`); both equal the accepted sliding rate
  `19|mu_b|/70`. Single-valued.
- `mu = (0,0)`: all rates zero (trivial zero-rate case) — consistent.

**Closure statement.** Every continuously admissible **regular** W-face candidate (drift `mu in T_W`, the only
active continuous constraint on the regular W-face away from endpoints) has **exactly one** applicable
sector-specific transition/rate/scoring contract; the shared boundary rays are proven equivalent (identical
rates), so candidate scoring is single-valued, and **no control is omitted or double-counted**. (Tiny exact
spot-checks: partition classifier + boundary-ray identity — zero mismatches.)

## 6. Future global regular-W-boundary discrete-Hamiltonian composition (Issue §9) — frozen (design semantics only)

Freeze the future composition rule (no HJB/KFE solved here):

```
all continuously admissible regular W-boundary candidate controls
 -> apply exactly one accepted sector-specific rate/scoring contract (T_realloc | R_reverse | R_deplete)
 -> compute each candidate's discrete H_h score BEFORE selection
 -> ONE global argmax over all regular candidates
 -> selected control + its already-defined rates
 -> ONE conservative backward row / generator Q
 -> future KFE consumes exactly Q^T.
```

No candidate may be dropped merely because it belongs to a different sector; no sector is optimized independently
and compared via post-hoc continuous objectives.

## 7. Same-process / KFE safeguard (Issue §10) — preserved

```
Q backward; Q^T forward; off-diagonal >= 0; diagonal = -sum actual outgoing; Q1 = 0;
same selected Q for HJB and KFE; p = M g; p_dot = Q^T p.
```

Future stationary acceptance still requires SCC / closed recurrent-class diagnostics, original source-free
`Q^T p` residual, mass normalization/nonnegativity, density via cell weights, unchanged Issue #27 pin semantics —
**recorded only; none run here.**

## 8. Verification log (tiny exact Fraction checks, `dlh5ve_closure.py`, `%TEMP%`)

- Deplete first moment exact + nonnegative for samples `(-1,-2)`, `(-3,-1/2)`, `(-4,0)` (boundary B1), `(0,-2)`
  (boundary B2) — zero mismatches.
- Boundary-ray identity: B1 `T_realloc` = depletion limit; B2 reverse = depletion limit; B3 sliding rate `19 mu_a/70`
  — all exact.
- Partition classifier: samples `mu_W <= 0` land in exactly one sector — zero mismatches.
