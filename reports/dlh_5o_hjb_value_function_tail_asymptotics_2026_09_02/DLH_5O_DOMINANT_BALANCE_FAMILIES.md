# DLH-5O Phase B — Candidate HJB Dominant-Balance Families

**Issue #41 Phase B.** Compares candidate liquid-tail scalings `V_b ~ b^{-p}` (with
`p<2`, `p=2`, `p>2`) jointly with the orders of `V_a/V_b`, `d`, `chi(d,a)`, `labor`,
and `V(b,a,z')-V(b,a,z)`, substituted into the source-faithful interior HJB identity
to the extent Phase A authorizes it (i.e., using the derivable interior identity and
the accepted FOCs, conditionally on the continuum/regularity assumption).

Interior HJB identity (Phase A, A5):

```text
rho*V = u + mu_b*V_b + mu_a*V_a + S*V
u = -1/c - l^6/6,   c = V_b^(-1/2),   l = (0.85z*V_b)^(1/5)
mu_a = r_a_eff(a)*a + d,   d = a*T(V_a/V_b-1)/chi_1,   chi = chi_0|d| + 0.5 chi_1 d^2/max(a,a_bar)
mu_b = r_b*b + 0.85z*l - d - chi - c      (transfer_income = 0)
(S*V)[z] = sum_z' lambda (V(z')-V(z)),   lambda = 1/3
```

## General ansatz

`V_b ~ K(a,z) b^{-p}`, `p > 0` (candidate). Then, with `V_inf(a,z)` the constant of
integration:

| p | V | c | u | labor_income | mu_b (leading) |
|---|---|---|---|---|---|
| `0<p<1` | `V_inf + K b^{1-p}/(1-p)` | `b^{p/2}` | `-b^{-p/2}` | `b^{-p/5}` | `r_b b` |
| `p=1` | `V_inf + K log b` | `b^{1/2}` | `-b^{-1/2}` | `b^{-1/5}` | `r_b b` |
| `1<p<2` | `V_inf - K b^{1-p}/(p-1)` | `b^{p/2}` | `-b^{-p/2}` | `b^{-p/5}` | `r_b b` |
| `p=2` | `V_inf - K/b` | `b` | `-b^{-1}` | `b^{-2/5}` | `(r_b - 1/sqrt(K))b` |
| `p>2` | `V_inf - K b^{1-p}/(p-1)` | `b^{p/2}` | `-b^{-p/2}` | `b^{-p/5}` | `-b^{p/2}` (superlinear) |

`V_a/V_b` orders (candidate): if `V_inf` is a-dependent, `V_a ~ dV_inf/da = O(1)`, so
`V_a/V_b ~ O(b^p)`. If `V_inf` is a-independent but `K` is a-dependent,
`V_a ~ O(b^{1-p})` (or `O(log b)` for `p=1`), so `V_a/V_b ~ O(b)`. Transfer orders:
`d = O(T(V_a/V_b-1))`; `chi = O(|d| + d^2/max(a,a_bar))`.

---

## B1. p < 2 families (slow decay): ASYMPTOTICALLY INCONSISTENT

**p in (0,1).** `mu_b ~ r_b b`, `mu_b V_b ~ r_b K b^{1-p}`; `rho*V ~ rho K b^{1-p}/(1-p)`;
`u ~ -b^{-p/2}` (lower order since `1-p > p/2` iff `p < 2/3`; for `p >= 2/3` compare:
`1-p` vs `p/2`: `1-p > p/2` iff `p < 2/3`). For `p < 2/3` the balance at `O(b^{1-p})` is
`rho K/(1-p) = r_b K + (S*K)/(1-p)`, i.e. `(rho - (1-p)r_b)K = S*K`. With
`rho = 0.02`, `r_b = 0.015`, the coefficient `rho - (1-p)r_b = 0.005 + 0.015p` is
**not** an eigenvalue of the switch generator `S` (spectrum `{0, -2/3}`) for `p>0`, so
`K = 0` — only the trivial solution. For `p >= 2/3` the `u`-term (`O(b^{-p/2})`) or the
`mu_b V_b` term cannot be matched either (the `rho*V` term `O(b^{1-p})` is then at most
equal order and no positive-`K` balance exists). **Inconsistent.**

**p = 1 (logarithmic).** `V ~ V_inf + K log b`. O(1) balance forces `V_inf = 0` (see
B3); then `rho*V ~ rho K log b` while `mu_b V_b ~ r_b K` and `u ~ -b^{-1/2}`: a `log b`
vs `O(1)` mismatch — no balance. **Inconsistent.**

**p in (1,2).** `V ~ V_inf - K b^{1-p}/(p-1)`. O(1) balance forces `V_inf = 0` (see
B3); then `rho*V ~ -rho K b^{1-p}/(p-1)`, `mu_b V_b ~ r_b K b^{1-p}` (since `c = o(b)`),
`u ~ -b^{-p/2}` (lower order for `p<2`). Balance at `O(b^{1-p})`:
`-rho K/(p-1) = r_b K - (S*K)/(p-1)`, i.e. `S*K = [rho + (p-1)r_b]K`. The coefficient
`rho + (p-1)r_b = 0.005 + 0.015p > 0` is not in `{0,-2/3}` for `p>0`; only `K = 0`.
**Inconsistent.**

In all `p<2` cases the productivity-switch spectrum argument (`rho`-perturbed
coefficient not in `{0,-2/3}`) forces the trivial solution, so **no slow-decay
power-law tail is self-consistent**.

---

## B2. p > 2 family (fast decay): ASYMPTOTICALLY INCONSISTENT

**p > 2.** `c ~ b^{p/2}` superlinear; `mu_b ~ -c ~ -b^{p/2}`; `mu_b V_b ~ -b^{-p/2}`;
`u ~ -b^{-p/2}`; `rho*V` with `V_inf` a-independent and `V ~ -K b^{1-p}/(p-1)` gives
`O(b^{1-p})`, and for `p>2` we have `p/2 < p-1`, so `b^{-p/2} >> b^{1-p}`. The leading
order is `u + mu_b V_b ~ -2 sqrt(K) b^{-p/2}`, which has **no counterpart** (`rho*V`
and `S*V` are strictly lower order). No positive `K` can balance `-2sqrt(K) = 0`.
**Inconsistent.** (With an a-dependent `V_inf`, `V_a/V_b ~ b^p` drives `d ~ b^p`,
`chi ~ b^{2p}`, `mu_b ~ -b^{2p}`, `mu_b V_b ~ -b^p` — an even worse unbalanced `O(b^p)`
term. Also inconsistent.)

---

## B3. p = 2 family (the candidate): SELF-CONSISTENT (conditional)

**p = 2.** `V ~ V_inf(a,z) - K(a,z)/b`, `V_b ~ K/b^2`, `c ~ b/sqrt(K)`,
`c/b -> 1/sqrt(K)`.

**Self-consistency of the transfer ratio.** If `V_inf` is a-dependent,
`V_a/V_b ~ (dV_inf/da) b^2/K ~ O(b^2)`; then `d ~ O(b^2)`, `chi ~ O(b^4)`,
`mu_b ~ -O(b^4)`, `mu_b V_b ~ -O(b^2)` — an unbalanced `O(b^2)` term. Inconsistent.
If `V_inf` is a-independent but `K` is a-dependent, `V_a/V_b ~ -(dK/da) b/K ~ O(b)`;
then `d ~ O(b)`, `chi ~ O(b^2)`, `mu_b ~ -O(b^2)`, `mu_b V_b ~ -O(1)` — an unbalanced
`O(1)` residual. Inconsistent. **Therefore the self-consistent candidate has `V_inf`
and `K` a-independent** (`V_a = 0`, `V_a/V_b = 0`, `q = -1`, `d = a*T(-1)/chi_1 =
-0.45a`, `chi = O(1)`, all bounded).

**O(1) balance.** `rho*V_inf(z) = mu_a*(dV_inf/da) + (S*V_inf)(z) = (S*V_inf)(z)` (the
`mu_a*V_a` term vanishes since `V_inf` is a-independent). `(rho I - S)V_inf = 0`;
`rho = 0.02` is not in the spectrum `{0,-2/3}` of `S`, so **`V_inf = 0`**.

**O(1/b) balance.** With `V ~ -K(z)/b`, `V_inf = 0`:
- `rho*V ~ -rho K/b`;
- `u ~ -sqrt(K)/b` (labor disutility `-l^6/6 ~ O(b^{-12/5})` is lower order);
- `mu_b V_b`: `mu_b ~ (r_b - 1/sqrt(K))b + 0.2025a + o(1)` (using `d = -0.45a`,
  `chi = 0.2475a`, `labor_income = o(1)`), so
  `mu_b V_b ~ (r_b - 1/sqrt(K))K/b + 0.2025a K/b^2`;
- `mu_a V_a = 0` (`V_a = 0`);
- `S*V ~ -S*K/b`.

Multiplying by `b` and matching `O(1)`:

```text
(rho + r_b)K - 2*sqrt(K) = S*K.
```

**z-consistency.** For the symmetric switch `S = [[-1/3,1/3],[1/3,-1/3]]`,
`(S*K)[z1] = (K2-K1)/3 = - (S*K)[z2]`, and the scalar map
`f(K) = (rho+r_b)K - 2sqrt(K)` is convex with a single zero at
`K* = 4/(rho+r_b)^2`. The system `f(K1) = (K2-K1)/3`, `f(K2) = (K1-K2)/3` has only the
symmetric solution `K1 = K2 = K*` (a non-constant pair would force `K1 < K*` and
`K2 > K*` simultaneously, a contradiction). Hence **`K` is z-constant** and the
cross-`z` switch contribution vanishes at `O(1/b)` (derived, not assumed).

**Coefficient.** `K = 4/(rho+r_b)^2`, `c/b = 1/sqrt(K) = (rho+r_b)/2 = 0.0175`.
This follows from the audited balance (no textbook import). Detailed derivation in
`DLH_5O_P2_COEFFICIENT_SYSTEM.md`.

**Classification: asymptotically self-consistent (conditional on the ansatz and the
analytic assumptions of Phase A; uniqueness of this balance among all conceivable
regimes is NOT established — see B4).**

---

## B4. Transfer-dominated / exotic alternatives

- **`V_a/V_b ~ b^m` with `m > 1/2`:** `chi ~ O(b^{2m})` superlinear, `mu_b ~ -O(b^{2m})`,
  `mu_b V_b ~ -O(b^{2m-p})`, while `rho*V ~ O(b^{1-p})`; since `2m > 1`, the
  `mu_b V_b` term is more divergent than `rho*V` and cannot be balanced.
  **Inconsistent.**
- **`V_a/V_b ~ b^m` with `0 < m <= 1/2`:** `chi = O(b^{2m}) = O(b)` or `O(1)`; such
  sub-superlinear transfer regimes either reduce to the analyzed power-law classes
  (e.g. an a-dependent `b^{-1/2}` term collapses to `p = 3/2`, which is in the
  inconsistent `1<p<2` class) or require a fully specified unbounded-tail problem to
  classify. **Not fully analyzable from accepted authority.**
- **Non-power, oscillatory, or boundary-layer tails:** **not analyzable from accepted
  authority** (the source does not define the unbounded-tail problem).

## Family matrix (summary)

| Family | Joint orders | Classification |
|---|---|---|
| `0<p<1` | `V_a/V_b` any; `c=o(b)` | INCONSISTENT (switch-spectrum forces `K=0`) |
| `p=1` | `c~b^{1/2}` | INCONSISTENT (log vs O(1) mismatch) |
| `1<p<2` | `c=o(b)` | INCONSISTENT (switch-spectrum forces `K=0`) |
| `p=2`, bounded transfer | `V_a/V_b=0`, `d=O(1)`, `chi=O(1)`, `c~b` | SELF-CONSISTENT (conditional); `K=4/(rho+r_b)^2`, `c/b=(rho+r_b)/2` |
| `p>2` | `c` superlinear | INCONSISTENT (flow utility unbalanced) |
| transfer-dominated `m>1/2` | `chi` superlinear | INCONSISTENT |
| transfer-dominated `m<=1/2`; non-power tails | — | NOT ANALYZABLE FROM ACCEPTED AUTHORITY |
