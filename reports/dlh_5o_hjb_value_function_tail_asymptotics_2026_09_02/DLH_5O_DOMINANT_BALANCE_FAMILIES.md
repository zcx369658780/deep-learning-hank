# DLH-5O Phase B — Candidate HJB Dominant-Balance Families (rev 2)

**Issue #41 Phase B.** Compares candidate liquid-tail scalings `V_b ~ b^{-p}` (with
`p<2`, `p=2`, `p>2`) jointly with the orders of `R = V_a/V_b`, `d`, `chi(d,a)`,
`labor`, and `V(b,a,z')-V(b,a,z)`, substituted into the source-faithful interior HJB
identity **with the transfer/adjustment terms grouped as the combined transfer
Hamiltonian** `V_b*[d*(R-1)-chi(d,a)]` (Phase A A3b/A5). All statements are conditional
on the Phase A analytic assumptions (smooth-continuum regularity, the ansatz,
uniformity, a tail boundary/transversality specification, uniqueness).

Interior HJB identity (Phase A A5, rev 2):

```text
rho*V = u + (r_b*b + labor - c)*V_b + r_a_eff(a)*a*V_a + V_b*[d*(R-1) - chi] + S*V
R = V_a/V_b,   q = R - 1,
u = -1/c - l^6/6,   c = V_b^(-1/2),   l = (0.85z*V_b)^(1/5)
d = a*T(R-1)/chi_1,   chi = chi_0|d| + 0.5 chi_1 d^2/max(a,a_bar)
(S*V)[z] = sum_z' lambda (V(z')-V(z)),   lambda = 1/3
```

The combined transfer Hamiltonian `V_b*[d*q - chi]` is **one same-order object**; it
is never split into `chi` alone. Its order is determined by `R`:

| `R = V_a/V_b` | `d` | `chi` | combined `V_b*[d*q - chi]` |
|---|---|---|---|
| `O(1)` | `O(1)` | `O(1)` | `O(1/b^2)` (subleading for p=2) |
| `o(sqrt(b))` (uniform) | `o(sqrt(b))` | `o(b)` | `o(1/b)` (subleading for p=2) |
| `~ b^m`, `m>0` | `O(b^m)` | `O(b^{2m})` | `O(b^{2m-2})` (p=2 base) |

## General ansatz

`V_b ~ K(a,z) b^{-p}`, `p > 0` (candidate). Then, with `V_inf(a,z)` the constant of
integration, and **within the transfer class `R = o(sqrt(b))` uniformly** (so
`d = o(sqrt(b))`, `chi = o(b)`, combined term subleading):

| p | V | c | u | labor_income | mu_b (leading) |
|---|---|---|---|---|---|
| `0<p<1` | `V_inf + K b^{1-p}/(1-p)` | `b^{p/2}` | `-b^{-p/2}` | `b^{-p/5}` | `r_b b` |
| `p=1` | `V_inf + K log b` | `b^{1/2}` | `-b^{-1/2}` | `b^{-1/5}` | `r_b b` |
| `1<p<2` | `V_inf - K b^{1-p}/(p-1)` | `b^{p/2}` | `-b^{-p/2}` | `b^{-p/5}` | `r_b b` |
| `p=2` | `V_inf - K/b` | `b` | `-b^{-1}` | `b^{-2/5}` | `(r_b - 1/sqrt(K))b` |
| `p>2` | `V_inf - K b^{1-p}/(p-1)` | `b^{p/2}` | `-b^{-p/2}` | `b^{-p/5}` | `-b^{p/2}` (superlinear) |

`V_a/V_b` orders (candidate): if `V_inf` is a-dependent, `V_a ~ d_av V_inf = O(1)`, so
`R ~ O(b^p)` (for the `-K/b` structure, `O(b^2)` at `p=2`). If `V_inf` is a-independent
but `K` is a-dependent, `V_a ~ O(b^{1-p})` (or `O(log b)` for `p=1`), so `R ~ O(b)`.
Leading a-independence of `V_inf` and `K` does **not** imply `R = 0`: a subleading term
`H(a,z)/b^2` gives `V_a ~ H_a/b^2` and `R -> H_a/K = O(1)` (rev 2; see Phase C/D).

---

## B1. p < 2 families — INCONSISTENT only within the transfer class `R = o(sqrt(b))`

**Claim (narrowed).** For the pure power-law families with `p < 2` (including
`p = 1`/logarithmic), **within the transfer class `R = o(sqrt(b))` uniformly** (so
`d = o(sqrt(b))`, `chi = o(b)`, combined transfer term subleading), the interior HJB
balance has **no positive-`K` solution**: the switch-spectrum argument forces the
trivial solution `K = 0`.

- **p in (0,1).** `mu_b ~ r_b b`, `mu_b V_b ~ r_b K b^{1-p}`; `rho*V ~ rho K b^{1-p}/(1-p)`;
  `u ~ -b^{-p/2}` (lower order for `p < 2/3`). Balance at `O(b^{1-p})`:
  `rho K/(1-p) = r_b K + (S*K)/(1-p)`, i.e. `(rho - (1-p)r_b)K = S*K`. With
  `rho = 0.02`, `r_b = 0.015`, the coefficient `rho - (1-p)r_b = 0.005 + 0.015p` is
  **not** an eigenvalue of the switch generator `S` (spectrum `{0, -2/3}`) for `p>0`,
  so `K = 0` — only the trivial solution. For `p >= 2/3` no positive-`K` balance exists
  either. **Inconsistent within the stated transfer class.**
- **p = 1 (logarithmic).** `V ~ V_inf + K log b`; O(1) balance forces `V_inf = 0` (see
  B3); then `rho*V ~ rho K log b` vs `mu_b V_b ~ r_b K`, `u ~ -b^{-1/2}`: a `log b` vs
  `O(1)` mismatch — no balance. **Inconsistent within the stated transfer class.**
- **p in (1,2).** `V ~ V_inf - K b^{1-p}/(p-1)`; O(1) balance forces `V_inf = 0` (B3);
  balance at `O(b^{1-p})` gives `S*K = [rho + (p-1)r_b]K`; the coefficient
  `rho + (p-1)r_b = 0.005 + 0.015p > 0` is not in `{0,-2/3}` for `p>0`; only `K = 0`.
  **Inconsistent within the stated transfer class.**

**Scope of the claim.** These proofs use `mu_b ~ r_b b`, which requires the combined
transfer term to be subleading — i.e., the class `R = o(sqrt(b))` uniformly. They do
**not** rule out `p < 2` HJB regimes outside that class (e.g. `R ~ Theta(sqrt(b))`,
where `d ~ Theta(sqrt(b))`, `chi ~ Theta(b)`, and the combined term contributes at the
same `b^{1-p}` order and changes the coefficient system). The earlier blanket
statements ("in all p<2 cases", "pure p<2 inconsistent") are **withdrawn** in rev 2.

---

## B2. p > 2 family — INCONSISTENT within the transfer class `R = o(sqrt(b))`

**Claim (narrowed).** Within the transfer class `R = o(sqrt(b))` uniformly
(`d = o(sqrt(b))`, `chi = o(b)`), `p > 2` is asymptotically inconsistent:
`c ~ b^{p/2}` superlinear; `mu_b ~ -c ~ -b^{p/2}`; `mu_b V_b ~ -b^{-p/2}`;
`u ~ -b^{-p/2}`; `rho*V ~ O(b^{1-p})` (with `V_inf = 0`), and for `p>2` we have
`p/2 < p-1`, so `b^{-p/2} >> b^{1-p}`. The leading order `u + mu_b V_b ~
-2 sqrt(K) b^{-p/2}` has **no counterpart** — no positive `K` can balance
`-2sqrt(K) = 0`. **Inconsistent within the stated transfer class.**

**Scope of the claim.** Outside the stated transfer class the term ordering differs
(e.g. a transfer-dominated `p>2` variant); the claim here covers only the class where
the combined transfer term is subleading. The earlier blanket "p>2 inconsistent" is
**narrowed** accordingly in rev 2.

---

## B3. p = 2 family (the candidate) — SELF-CONSISTENT under the derivative-control premise

**p = 2.** `V ~ V_inf(a,z) - K(a,z)/b`, `V_b ~ K/b^2`, `c ~ b/sqrt(K)`,
`c/b -> 1/sqrt(K)`.

**Transfer-ratio self-consistency via the combined Hamiltonian (rev 2).**
`R = V_a/V_b ~ (d_av V_inf) b^2/K - (d_aa K) b/K + O(1)`. Therefore:

- If `d_av V_inf != 0`: `R ~ O(b^2)`; then `d ~ O(b^2)`, `chi ~ O(b^4)`, and the
  **combined** term `V_b*[d*q - chi] ~ O(b^{2m-2})` with `m=2` gives `O(b^2)` — an
  unbalanced `O(b^2)` object (the `d*V_a = O(b^2)` part is included in the combined
  term, so there is no missing counterpart). Inconsistent.
- If `d_av V_inf = 0` but `d_aa K != 0`: `R ~ O(b)`; `d ~ O(b)`, `chi ~ O(b^2)`,
  combined term `O(1)` — an unbalanced `O(1)` residual. Inconsistent.
- If `d_av V_inf = 0` and `d_aa K = 0` (leading a-independence) **and** the remainder
  derivative is controlled by the explicit premise `R = o(sqrt(b))` uniformly
  (preferably `R = O(1)`): `d = o(sqrt(b))` (resp. `O(1)`), `chi = o(b)` (resp.
  `O(1)`), combined term `o(1/b)` (resp. `O(1/b^2)`) — **subleading**. This is the
  self-consistent branch, **conditional on the derivative-control premise**.

**O(1) balance.** With `R = o(sqrt(b))`, `V_a = o(1/b^{1/2})... ` — precisely, `V_a` is
at most `o(1/b^{1/2})` relative order, so the `mu_a*V_a` contribution (with
`mu_a = O(1)`) is at most `o(1/b^{1/2})` and certainly `o(1)`; with `d_av V_inf = 0`,
`rho*V_inf(z) = (S*V_inf)(z)`. `(rho I - S)V_inf = 0`; `rho = 0.02` is not in the
spectrum `{0,-2/3}` of `S`, so **`V_inf = 0`**.

**O(1/b) balance (rev 2).** With `V ~ -K(z)/b`, `V_inf = 0`, and the combined transfer
term subleading:

```text
-rho*K = -sqrt(K) + (r_b - 1/sqrt(K))*K - S*K
```

i.e.

```text
(rho + r_b)K - 2*sqrt(K) = S*K.
```

**z-consistency.** For the symmetric switch `S = [[-1/3,1/3],[1/3,-1/3]]`, the map
`f(K) = (rho+r_b)K - 2sqrt(K)` is convex with a single zero at
`K* = 4/(rho+r_b)^2`; the coupled system forces `K1 = K2 = K*` (a non-constant pair
would force `K1 < K*` and `K2 > K*` simultaneously, a contradiction). Hence **`K` is
z-constant** and the cross-`z` switch contribution vanishes at `O(1/b)`.

**Coefficient.** `K = 4/(rho+r_b)^2`, `c/b = 1/sqrt(K) = (rho+r_b)/2 = 0.0175`.
Derived from the audited balance (no textbook import) **under the corrected
derivative-control premise**; detailed derivation in `DLH_5O_P2_COEFFICIENT_SYSTEM.md`.

**Classification: asymptotically self-consistent, conditional on (i) the ansatz, (ii)
the derivative-control premise `R = o(sqrt(b))` uniformly (preferably `O(1)`), and
(iii) the Phase A analytic assumptions. Uniqueness among all conceivable regimes is
NOT established (see B4).**

---

## B4. The critical `m = 1/2` transfer family — UNRESOLVED

- **`R ~ Theta(sqrt(b))` (m = 1/2):** `d ~ Theta(sqrt(b))`, `chi ~ Theta(b)`, and the
  **combined** transfer term `V_b*[d*q - chi]` is `Theta(1/b)` — **exactly the same
  order** as the proposed `O(1/b)` coefficient equation. In this regime
  `(rho+r_b)K - 2sqrt(K) = S*K` is **altered** by an a-dependent term, so
  `c/b = (rho+r_b)/2` does **not** follow, and whether this family is HJB-consistent is
  **NOT RESOLVED** in this package. It is explicitly **excluded from the `p=2`
  conditional theorem** by the premise `R = o(sqrt(b))`, and is left **open** (neither
  accepted nor ruled out).
- **`R ~ b^m` with `m > 1/2`:** `chi ~ O(b^{2m})` superlinear; combined term
  `O(b^{2m-2})`; for `m > 1` this is more divergent than every other term (all `O(1)`
  or `O(1/b)`), and for `1/2 < m <= 1` it is still `O(b^{2m-2})` with `2m-2 > -1`,
  more divergent than the `O(1/b)` balance — **inconsistent** (established from the
  combined Hamiltonian, not from `chi` alone).
- **`R ~ b^m` with `0 < m < 1/2`:** combined term `O(b^{2m-2})` with `2m-2 < -1`
  (`o(1/b)`) — subleading; such regimes reduce to the analyzed subleading-transfer
  classes (the `p=2` balance is unchanged at `O(1/b)`).
- **Non-power, oscillatory, or boundary-layer tails:** **not analyzable from accepted
  authority** (the source does not define the unbounded-tail problem).

## Family matrix (rev 2 summary)

| Family | Transfer class | Combined transfer term | Classification |
|---|---|---|---|
| `0<p<1` | `R=o(sqrt(b))` (uniform) | subleading | INCONSISTENT (switch-spectrum forces `K=0`) |
| `p=1` | `R=o(sqrt(b))` (uniform) | subleading | INCONSISTENT (log vs O(1) mismatch) |
| `1<p<2` | `R=o(sqrt(b))` (uniform) | subleading | INCONSISTENT (switch-spectrum forces `K=0`) |
| `p=2` | `R=o(sqrt(b))` (preferably `O(1)`), uniform | `o(1/b)` (resp. `O(1/b^2)`) | SELF-CONSISTENT (conditional); `K=4/(rho+r_b)^2`, `c/b=(rho+r_b)/2` |
| `p>2` | `R=o(sqrt(b))` (uniform) | subleading | INCONSISTENT (flow utility unbalanced) |
| `p=2`-base, `m>1/2` | `R~b^m` | `O(b^{2m-2})` dominant | INCONSISTENT (combined Hamiltonian) |
| `p=2`-base, `m=1/2` | `R~Theta(sqrt(b))` | `Theta(1/b)` same-order | **UNRESOLVED / OPEN** (coefficient equation altered) |
| `p<2`, `m=1/2` | `R~Theta(sqrt(b))` | same `b^{1-p}` order | NOT RULED OUT by this package (see B1 scope) |
| non-power tails | — | — | NOT ANALYZABLE FROM ACCEPTED AUTHORITY |
