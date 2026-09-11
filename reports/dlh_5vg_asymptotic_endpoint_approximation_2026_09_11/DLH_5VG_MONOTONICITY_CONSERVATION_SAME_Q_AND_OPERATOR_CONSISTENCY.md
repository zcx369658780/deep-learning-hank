# DLH-5V-G — Monotonicity, Conservation, Same-Q and Operator Consistency

**Design only.** Proves the jump/rate/second-moment scaling (not assumed), the generator/operator consistency for
smooth test functions, monotonicity/conservation and the one-Q same-process semantics of the A1 contract (T5–T7 of the
umbrella). Tiny exact `%TEMP%` spot-checks are supplementary.

## 1. Jump / rate / second-moment scaling — proved

All represented displacements are integer multiples of `(10/(19m), 7/(19m))`:

```text
max jump |w| = |w_T| = sqrt(2)*70/(19m) = O(1/m)
```

**Rate scale O(m).** For fixed physical drift `mu = O(1)` (in `(a,b)` units), every sector rate is `q = 19m * (linear
combination of mu components) / (integer)`, hence `q = O(m)`:

```text
Case L:  q_RT = 19m*mu_a/70,     q_down = 19m*(-mu_W)/7
Case U:  q_T = 19m*mu_b/70,      q_in = 19m*(-mu_W)/10;  or q_left = 19m*(-mu_a)/10, q_down = 19m*(-mu_b)/7
Case B:  q_T = 19m*mu_b/70,      q_in = 19m*(-mu_W)/10
```

**Second-moment scale O(1/m) — explicit constants.** For `mu` bounded by `|mu_a|, |mu_b|, |mu_W| <= M`:

```text
Case L:  sum q |w|^2 = (2660*mu_a + 133*(-mu_W)) / (361 m)          = O(M/m)
Case U/B (T_realloc): q_T*2*(70/(19m))^2 + q_in*(10/(19m))^2        = O(M/m)
Case U (deplete):     q_left*(10/(19m))^2 + q_down*(7/(19m))^2      = O(M/m)
Interior: 4-neighbor rates O(m) with jumps O(1/m)                   = O(M/m)
```

Spot-verified: for fixed `mu`, `m * (second moment)` is exactly constant over `m in {1..32}` (value
`(2660*mu_a + 133*(-mu_W))/361` in Case L). All constants are uniform in the frontier phase `theta` and `N_m mod 7`
(the rates and displacements depend only on the sector cone, not on `r_j`).

## 2. Generator / operator consistency for smooth test functions (T6)

For `phi in C^2` with `||D^2 phi||_inf <= M_2`, the discrete generator at any state `s` is
`L_m phi(s) = sum_r q_{sr} (phi(r) - phi(s))`. Taylor expansion gives

```text
L_m phi(s) = mu . grad phi(s) + (1/2) sum_r q_{sr} w_{sr}^T D^2 phi w_{sr} + R_3,
|R_3| <= (1/6) M_3 sum_r q_{sr} |w_{sr}|^3 = O(m * (1/m)^3) = O(1/m^2)
```

with `sum_r q_{sr} |w_{sr}|^2 = O(1/m)` from §1, so

```text
|L_m phi(s) - mu . grad phi(s)| <= (1/2) M_2 * (second moment) + O(1/m^2) = O(M_2 / m) -> 0.
```

Thus for smooth test functions the discrete generator converges to `mu . grad phi` at every state, with numerical
diffusion vanishing at rate `1/m`. This holds for every admitted candidate at every state (layer and regular alike);
the regular region inherits the accepted m-scaled consistency of the exact contracts.

## 3. Monotonicity and conservation (T7, part 1)

By construction of the sector cones:

- All off-diagonal rates are nonnegative: `q_RT, q_down, q_T, q_in, q_left >= 0` on their cones (nonnegativity follows
  from the cone inequalities `mu_a >= 0`/`mu_a <= 0`/`mu_b >= 0`/`mu_W <= 0` combined with the defining signs of each
  sector); interior rates `>= 0`.
- Rows are conservative: the diagonal is `Q_ss = - sum_{r != s} q_{sr}` — the negative of the sum of the ACTUAL
  represented outgoing rates — hence `Q_m 1 = 0` exactly.
- The rate/decomposition is unique per candidate (bases with `det != 0` in every sector; the T_realloc/deplete split
  is pinned by the sign of `mu_b`, matching the accepted DLH-5V-E boundary identities B1/B2/B3).

## 4. One-Q same-process semantics (T7, part 2)

The frozen candidate pipeline (DLH-5V-E §5, unchanged) is:

```text
continuous admissibility + A1 buffer
  -> candidate-specific represented nonnegative rates (exact first moments)
  -> discrete H_h^m score BEFORE selection
  -> ONE global statewise argmax over admitted candidates
  -> selected control + its already-defined rates
  -> ONE conservative backward row / generator Q_m
  -> future KFE consumes exactly Q_m^T
```

The A1 buffer is applied at the first step (candidate admissibility), before scoring — never select-then-clip. There is
exactly ONE selected backward `Q_m` for the whole family; the future KFE uses exactly `Q_m^T`. No second boundary
process, no ghost/interpolation/reflection, no omitted-destination-with-retained-diagonal, no KFE-only repair.
Pinning/normalization may fix scale only and may not repair leakage. Stationary KFE remains NOT AUTHORIZED.

## 5. Interpretation ceiling (Issue §11)

Outcome A establishes a **design-level** asymptotic same-process contract: for the frozen family there exists a
shrinking numerical candidate-admissibility buffer (A1) under which every admitted endpoint candidate has an exact
native-grid first-moment contract, the physical layer width `ell_m = 70/(19m)` vanishes, the exact regular contract is
recovered away from endpoints, the discrete generator is operator-consistent with `O(1/m)` numerical diffusion, and
monotonicity/conservation/one-Q semantics hold. It does NOT establish: implementation correctness; production `Q`
assembly/run; numerical `W_max` adequacy; HJB/KFE/stationary existence/uniqueness or stationary KFE authorization;
economic validity of the household model; aggregates/GE/regional/neural/nominal/calibration/policy/welfare/Results.

The next gate is a **boundary-HJB implementation gate** (per the terminal name); this gate does not authorize or
perform it.

## 6. Supplementary exact spot-checks (tiny `%TEMP%` scripts, never committed)

- Second-moment scaling: `m * S2` constant over `m in {1,2,4,8,16,32}` (rate `O(m)`, second moment `O(1/m)`).
- Rate-moment equality for rational drifts across all sectors and all `m in {1,2,3,7}`: exact (`True`).
- Cone membership exact separation tests (buffered drift in destination cone): 158 checks, 0 failures.
