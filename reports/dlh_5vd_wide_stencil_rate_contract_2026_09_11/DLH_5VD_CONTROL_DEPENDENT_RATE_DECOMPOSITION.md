# DLH-5V-D — Control-Dependent W1 Wide-Stencil Rates and Conservative Same-Process Generator Contract (Rate Decomposition)

**Issue:** deep-learning-hank #52 (DLH-5V-D) · **Branch:** `dsh/issue-52-dlh-5vd-wide-stencil-rate-contract-2026-09-11`
Covers Issue §5 (exact rate map), §6.1 (activation predicate / equality cases), §6.2 (uniqueness), §6.3
(discrete Hamiltonian), §6.4 (no double counting). Exact algebra only; tiny exact Fraction spot-checks in
`%TEMP%` (not committed); no sweeps.

---

## 1. Frozen inputs (accepted DLH-5V-C — not reopened)

`w_in = (-10/19, 0)` (local inward `(-1,0)`), `w_T = (-70/19, +70/19)` (wide tangent `(-7,+10)`), wide transition
`(j,i) -> (j-7,i+10)` on accepted regular W-active states with `j >= 7`; endpoint band `j in {0..6}` deferred;
`T_realloc = {mu_a<=0, mu_b>=0, mu_W=mu_a+mu_b<=0}`; accepted `cone{w_in, w_T} = T_realloc`.

## 2. Candidate-control rate map (Issue §5) — exact

For each candidate control `(c,l,d)` inside the discrete HJB maximization, compute the continuous drift
`mu(c,l,d) = (mu_a, mu_b)`, `mu_W = mu_a + mu_b`. If `mu in T_realloc`, write `mu = (-a-b, +a)` with
`a = mu_b >= 0`, `b = -mu_W >= 0`, and freeze the base-grid rate map

```
q_T(c,l,d)  = 19 * mu_b / 70 = 19 a / 70
q_in(c,l,d) = 19 * (-mu_W) / 10 = 19 b / 10
```

and, for the symbolic fixed-aspect refinement family `da_h = h·10/19`, `db_h = h·7/19`:

```
q_T^h  = 19 * mu_b / (70 h)
q_in^h = 19 * (-mu_W) / (10 h).
```

**Exact first moment (proof).**

```
q_in·w_in + q_T·w_T
  = (19(-mu_W)/10)·(-10/19, 0) + (19 mu_b/70)·(-70/19, +70/19)
  = (mu_W, 0) + (-mu_b, mu_b)
  = (mu_W - mu_b, mu_b) = (mu_a, mu_b) = mu.   (exact, since mu_W - mu_b = mu_a)
```

**Nonnegativity (proof).** `q_T >= 0 <=> mu_b >= 0` and `q_in >= 0 <=> mu_W <= 0`; both hold on `T_realloc`, so
both rates are nonnegative for every candidate control in the sector.

## 3. Activation predicate and equality cases (Issue §6.1) — exact

Freeze the exact predicate (all four must hold):

```
(P1) source is an accepted regular W-active state;
(P2) j >= 7;
(P3) candidate control (c,l,d) is admissible under the accepted W-boundary KKT/tangent law;
(P4) candidate drift satisfies mu_a <= 0, mu_b >= 0, mu_W <= 0   (i.e. mu in T_realloc).
```

**Equality-case audit (exact).**

| case | rates | meaning |
|---|---|---|
| `mu_b = 0` (so `mu_a = mu_W <= 0`) | `q_T = 0`; `q_in = 19(-mu_W)/10 >= 0` | pure inward axial drift (a decreasing, b unchanged) |
| `mu_W = 0` (so `mu_a = -mu_b <= 0`) | `q_in = 0`; `q_T = 19 mu_b/70 >= 0` | pure wide tangent (sliding along the W-line) |
| `mu_b = 0` and `mu_W = 0` | `q_T = 0` and `q_in = 0` | `mu_a = mu_W - mu_b = 0` -> zero drift `mu = (0,0)`; no transition (trivial zero-rate equality case) |

**Continuous vanishing:** `q_T = (19/70) mu_b` and `q_in = (19/10)(-mu_W)` are continuous linear functions of the
drift, so both rates vanish continuously as their argument tends to the boundary — no ambiguity, no discontinuity,
no discrete on/off switch.

**Outside the sector:** a candidate control with `mu not in T_realloc` is marked **outside the frozen DLH-5V-D
contract**; no alternative transition rule is invented for it. (The remaining admissible regular drift sectors are
identified precisely in §6.9 of the generator-contract report / umbrella §4.)

## 4. Uniqueness / no tie-breaking (Issue §6.2) — proved

`det[w_in  w_T] = (-10/19)(70/19) - 0 = -700/361 != 0`, so `w_in` and `w_T` are **linearly independent** and form a
basis of `R^2`. Hence for every `mu in R^2` the representation `mu = q_in w_in + q_T w_T` has **unique** real
coefficients, forced to be

```
q_T  = 19 mu_b / 70,   q_in = -19 mu_W / 10.
```

Nonnegativity of these unique coefficients holds exactly on `T_realloc` (proved in §2). **Therefore:**
the nonnegative decomposition is **unique for every `mu in T_realloc`**, and **no rate tie-breaking is needed
inside this sector** — the only special cases are the trivial zero-rate boundary cases (`mu_b = 0`, `mu_W = 0`,
`mu = (0,0)`), which are boundary values of the same unique map, not tie-breaks.

## 5. Candidate-control discrete Hamiltonian semantics (Issue §6.3) — frozen

For each candidate control in the sector, with accepted destinations `s_in = (j-1, i)` and `s_T = (j-7, i+10)`
(both represented in the regular region; `s_in` needs `j >= 1` — implied by `P2`, and `10(j-1)+7i = 10j+7i-10 < N`
for a represented source; `s_T` representation is the accepted DLH-5V-C result):

```
H_h(c,l,d)
 = u(c) - v(l)
 + q_in(c,l,d) [V_{s_in} - V_s]
 + q_T(c,l,d)  [V_{s_T} - V_s]
 + switch_z.
```

The rates `q_in(c,l,d)`, `q_T(c,l,d)` are computed **for each candidate control before maximization**. The selected
boundary control is

```
selected control = argmax_{admissible (c,l,d)} H_h(c,l,d).
```

Explicitly **not** allowed: continuous maximization followed by clipping/decomposition of the chosen drift.
Candidate controls with `mu not in T_realloc` are excluded from the wide-stencil contract (outside-sector marking,
§3) — the maximization is over the admissible in-sector candidates plus the (separate, unchanged) interior/productivity
transition structure.

## 6. Canonical no-double-counting semantics (Issue §6.4) — frozen

Within `T_realloc`, the asset-drift part of the controlled generator is represented **canonically by exactly the two
rates `q_in` and `q_T`**:

- By §4 the decomposition is unique; any additional nonnegative rates `{q_k}` on other represented asset edges
  `{v_k}` would need `sum_k q_k v_k = 0` to keep the first moment equal to `mu` — achievable only with at least two
  opposing extra edges, injecting redundant transition mass that reproduces the same drift through multiple paths
  (double counting) while changing the generator's higher moments and structure.
- Such an alternative decomposition is therefore **not equivalent** (the generator differs), **not unique**
  (contradicts §4), and is **rejected**; the canonical two-ray basis `{q_in, q_T}` is used.
- **Productivity switching remains separate and unchanged** (`switch_z`); it is not part of the asset-drift
  decomposition and does not double count it.

## 7. Verification log (tiny exact Fraction checks, `dlh5vd_rate_contract.py`, `%TEMP%`)

1. `det[w_in w_T] = -700/361 != 0` (basis, unique decomposition).
2. First-moment identity `q_in w_in + q_T w_T = mu` exact and nonnegativity for samples: sliding `(-3,3)`
   (`q_T=57/70, q_in=0`), pure inward `(-5,0)` (`q_T=0, q_in=19/2`), pure wide `(-2,2)` (`q_T=19/35, q_in=0`),
   interior `(-7,3)`, boundary mix `(-1,1/2)`, zero drift `(0,0)` — all exact, all nonnegative.
3. Equality cases: `mu_b=0` -> `q_T=0`; `mu_W=0` -> `q_in=0`; `mu=(0,0)` -> both 0 (exact).

Result: **zero mismatches**.
