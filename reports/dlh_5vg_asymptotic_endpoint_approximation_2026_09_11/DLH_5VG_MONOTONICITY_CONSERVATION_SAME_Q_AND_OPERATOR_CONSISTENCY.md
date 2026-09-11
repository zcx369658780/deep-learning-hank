# DLH-5V-G — Monotonicity, Conservation, Same-Q and Operator Consistency (Rev 1)

**Design only.** The finite-m process properties (jump/rate/second-moment scaling, operator consistency with a pure
`C^2` remainder bound, monotonicity, conservation, one-Q semantics) — retained and corrected per reviewer items 7–8.
Scope note: these properties hold for the finite-m A1-admitted process; they do NOT rescue the asymptotic
graph-consistency obstruction (documented in the buffered-admissibility report and the umbrella).

## 1. Jump / rate / second-moment scaling — proved (retained)

All represented displacements are integer multiples of `(10/(19m), 7/(19m))`:

```text
max jump |w| = |w_T| = sqrt(2)*70/(19m) = O(1/m)
```

Rates for fixed physical drift `mu = O(1)` are `q = 19m * (linear combination of mu components) / (integer) = O(m)`:

```text
Case L:  q_RT = 19m*mu_a/70,     q_down = 19m*(-mu_W)/7
Case U:  q_T = 19m*mu_b/70,      q_in = 19m*(-mu_W)/10;  or q_left = 19m*(-mu_a)/10, q_down = 19m*(-mu_b)/7
Case B:  q_T = 19m*mu_b/70,      q_in = 19m*(-mu_W)/10
Interior (accepted): O(m)
```

Second moments (`|mu| <= M`):

```text
Case L:  sum q |w|^2 = (2660*mu_a + 133*(-mu_W)) / (361 m)   = O(M/m)
Case U/B (T_realloc): q_T*2*(70/(19m))^2 + q_in*(10/(19m))^2 = O(M/m)
Case U (deplete):     q_left*(10/(19m))^2 + q_down*(7/(19m))^2 = O(M/m)
Interior: O(M/m)
```

Spot-verified: `m * (second moment)` exactly constant over `m in {1..32}`; all constants uniform in the frontier phase.

## 2. Generator / operator consistency — pure `C^2` bound (reviewer item 7)

For `phi in C^2` with `||D^2 phi||_inf <= M_2`, the discrete generator is `L_m phi(s) = sum_r q_{sr} (phi(r) - phi(s))`.
Using the integral (Taylor-with-remainder) form on each segment `[s, r]`:

```text
phi(r) - phi(s) = grad phi(s) . w_{sr} + (1/2) w_{sr}^T D^2 phi(xi_{sr}) w_{sr},   xi_{sr} in [s, r],
```

so, with `mu = sum_r q_{sr} w_{sr}` (exact first moment for admitted candidates):

```text
L_m phi(s) = mu . grad phi(s) + (1/2) sum_r q_{sr} w_{sr}^T D^2 phi(xi_{sr}) w_{sr},
|L_m phi(s) - mu . grad phi(s)| <= (1/2) M_2 * sum_r q_{sr} |w_{sr}|^2 = O(M_2 / m).
```

No `C^3`/third-derivative assumption is needed (the previous `M_3` remainder phrasing is removed). Numerical diffusion
vanishes at rate `1/m` for smooth test functions at every state of the finite-m process.

## 3. Monotonicity and conservation (retained)

- All off-diagonal rates are nonnegative on their cones (defining inequalities of each sector); interior rates `>= 0`.
- Rows conservative: `Q_ss = - sum_{r != s} q_{sr}` (negative of the sum of ACTUAL represented outgoing rates), hence
  `Q_m 1 = 0` exactly.
- Unique decomposition per candidate (bases with `det != 0`; T_realloc/deplete split pinned by the sign of `mu_b`,
  matching accepted DLH-5V-E boundary identities B1/B2/B3).

## 4. One-Q same-process semantics (retained)

```text
continuous admissibility + A1 buffer
  -> candidate-specific represented nonnegative rates (exact first moments)
  -> discrete H_h^m score BEFORE selection
  -> ONE global statewise argmax over admitted candidates
  -> selected control + its already-defined rates
  -> ONE conservative backward row / generator Q_m
  -> future KFE consumes exactly Q_m^T
```

Buffer applied at the first step, before scoring — never select-then-clip. Exactly ONE selected backward `Q_m`; future
KFE uses exactly `Q_m^T`. No second boundary process, no ghost/interpolation/reflection, no omitted-destination-with-
retained-diagonal, no KFE-only repair. Pinning/normalization may fix scale only. Stationary KFE remains NOT AUTHORIZED.

## 5. Scope note — what this report does and does NOT establish

This report establishes the finite-m process properties above for the A1-admitted candidates (valid, retained from
Rev 0). It does **not** establish the asymptotic tangent-cone graph consistency: that requirement fails (reviewer
counterexample confirmed; impossibility proof in the buffered-admissibility report; global failure on the frozen regular
block in the umbrella §3.2). Scaling/operator/monotonicity/conservation/one-Q are necessary but not sufficient for the
Issue-#55 theorem; the controlling obstruction stands. Design only; no implementation, no production `Q`, no
HJB/KFE/stationary solve, no numerical `W_max`.

## 6. Supplementary exact spot-checks (tiny `%TEMP%` scripts, never committed)

- Second-moment scaling: `m * S2` constant over `m in {1,2,4,8,16,32}`.
- Rate-moment equality for rational drifts across all sectors and `m in {1,2,3,7}`: exact (`True`).
- Cone-membership exact separation tests: 158 checks, 0 failures (finite-m algebra).
