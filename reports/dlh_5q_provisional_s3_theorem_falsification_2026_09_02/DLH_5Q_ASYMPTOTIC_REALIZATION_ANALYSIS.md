# DLH-5Q Phase C — Asymptotic-Realization Analysis

**Issue #43 Phase C (steps 24-28).** Within the provisional S3 class
(`R = V_a/V_b = O(1)` uniformly), determines whether the actual admissible tail must
realize `p=2`. Revisits `p<2`, `p=2`, `p>2` and log/non-power possibilities using the
**accepted combined transfer Hamiltonian** `V_b*[d*(R-1)-chi]`, distinguishes formal
dominant-balance exclusion from an actual asymptotic theorem, and states the
derivative-remainder control required.

---

## C0. The accepted interior HJB (combined form) and the S3 class

```text
rho*V = u + (r_b*b + labor - c)*V_b + r_a_eff(a)*a*V_a + V_b*[d*(R-1)-chi] + S*V,
```

with `R = V_a/V_b`, `c = V_b^(-1/2)`, `u = -1/c - w l^6/6` (single region, `gamma_c=2`,
`phi=5`), `l = (0.85 z V_b)^(1/5)`, `d = a*T(R-1)/chi_1`,
`chi = chi_0|d| + 0.5 chi_1 d^2/max(a,a_bar)`.

Under S3 (`R=O(1)` uniformly), with `a in [0,10]` compact and `T` bounded:
`d = O(1)`, `chi = O(1)` (order statements only). Consequently the combined transfer
Hamiltonian satisfies

```text
H_tr = V_b*[d*(R-1) - chi] = O(V_b)   (since d(R-1) - chi = O(1) under R=O(1)).
```

This is the key structural fact: **inside S3, the combined transfer term is a bounded
multiple of `V_b`**; it cannot be larger than `O(V_b)`.

---

## C1. Power-law families `V_b ~ K/b^p` (`K>0`)

**S1 boundedness restricts `p`.** With `V_b ~ K/b^p`, `V ~ V_inf - K/((p-1)b^(p-1))`
for `p>1`, `V ~ V_inf - K ln b` for `p=1`. S1 (`V` bounded, `V_b>0`, `V<0`) plus S2
(`V_inf=0`):

- `p = 1`: `V ~ -K ln b -> -inf`, **violates S1 boundedness** (log tail excluded by
  S1, before any balance argument).
- `0 < p < 1`: `V` grows like `b^(1-p)`, violates `V->0`/boundedness.
- `p < 0`: `V_b` grows; `V -> -inf`, violates boundedness.
- Hence **only `p > 1` is admissible** for a power tail under S1+S2.

**Decomposition of the O(1/b^(p-1)) and O(1/b^(p/2)) scales** (for `p>1`):

```text
rho*V            ~ -rho*K/((p-1) b^(p-1))
(r_b*b - c)*V_b  ~  r_b*K/b^(p-1) - sqrt(K)/b^(p/2)
u                ~ -sqrt(K)/b^(p/2)          [u = -1/c = -V_b^(1/2)]
r_a_eff(a)*a*V_a ~  O(1)/b^p                 [V_a = R V_b = O(K/b^p)]
H_tr             ~  O(1)/b^p                 [bounded multiple of V_b]
S*V              ~  O(1)/b^(p-1)             [0 if K z-constant]
```

so the consumption/utility terms combine exactly as

```text
u - c*V_b = -2 sqrt(V_b) ~ -2 sqrt(K)/b^(p/2),
```

and the two candidate dominant scales are `1/b^(p/2)` (consumption) and `1/b^(p-1)`
(rho / r_b / S).

**Dominant-order condition.** For a consistent balance with no unbalanced leading
term, the consumption scale must coincide with the rho/r_b/S scale:

```text
p/2 = p - 1   <=>   p = 2.
```

- `p < 2` (`1 < p < 2`): `p/2 < p-1`, so `-2 sqrt(K)/b^(p/2)` is the **largest** term
  and has no same-order partner among `rho*V`, `r_b*b*V_b`, `S*V` (all `1/b^(p-1)`),
  nor among `H_tr`, `r_a*V_a` (all `1/b^p`). **Unbalanced -> formally inconsistent.**
- `p > 2`: again `p/2 < p-1`, so `-2 sqrt(K)/b^(p/2)` is larger than `1/b^(p-1)` and
  unbalanced (its same-order partner would have to be a `1/b^(p/2)` term, and there is
  none; `u` and `-c V_b` cancel only into the combined `-2 sqrt(V_b)`). **Formally
  inconsistent.**
- `p = 2`: `p/2 = p-1 = 1`; the O(1/b) balance is
  `-rho*K + r_b*K - 2 sqrt(K) + (S*K) = 0`, i.e.
  `(rho+r_b)K - 2 sqrt(K) = S*K` — the DLH-5O Phase C system — **self-consistent**
  (conditional).

This reproduces and confirms DLH-5O Phase B within the S3 class: `p<2` and `p>2` are
formally inconsistent; `p=2` is the unique self-consistent power balance. **No `p != 2`
power family survives inside S3 at the formal level.**

---

## C2. Log and non-power tails

- **Log tail** (`V_b ~ K/b`): excluded by S1 boundedness (C1).
- **Slowly-varying / non-power tails:** consider `V ~ -C(b)`, `C(b) -> 0^+`,
  `C'(b) < 0` (so `V_b = -C'(b) > 0`). The dominant scales are `rho*V ~ -rho C(b)`,
  `r_b*b*V_b ~ -r_b b C'(b)`, and `u - c V_b = -2 sqrt(-C'(b))`.
  - Try `C(b) = b^(-alpha)`, `alpha > 0` (power-like): `sqrt(-C'(b)) ~ b^(-(alpha+1)/2)`.
    Balance requires `(alpha+1)/2 = alpha`, i.e. `alpha = 1` (`p=2`). For `alpha > 1`
    (thinner than `1/b`), the consumption term `b^(-(alpha+1)/2)` is **larger** than
    `b^(-alpha)` and unbalanced. For `0 < alpha < 1` (thicker), the consumption term is
    smaller; the rho/r_b terms give `(r_b*alpha - rho) b^(-alpha)`, which would require
    `alpha = rho/r_b = 0.02/0.015 = 4/3 > 1`, contradicting `alpha < 1`.
  - General slowly-varying `C` (e.g. `1/ln b`): the consumption term
    `-2 sqrt(-C'(b))` is algebraically larger than `rho C(b)` and `r_b b C'(b)` when
    `C` decays slower than `1/b`, leaving it unbalanced; for `C` decaying faster than
    `1/b` it is again unbalanced at its own (higher) order.
  - Conclusion: **no slowly-varying/non-power formal tail survives inside S3**; the
    balance drives the value scale to `~ 1/b` (i.e. `V_b ~ 1/b^2`, `p=2`).

- **Oscillatory tails** (`V` with bounded oscillation times a decaying envelope):
  `V_b` would change sign infinitely often, violating S1 `V_b>0` on any monotone
  interval; an oscillatory tail is incompatible with the monotonicity class. Not a
  coherent S3 candidate.

---

## C3. Formal dominant-balance exclusion vs actual asymptotic theorem (step 26)

The results of C1/C2 are **formal dominant-balance statements**: they show that, if
`V` admits a power (or slowly-varying) tail of the stated leading form with
`R=O(1)` and a controlled remainder, then the only self-consistent scale is `p=2`.
They are **NOT** an asymptotic theorem, because an actual theorem additionally needs:

1. **Existence + comparison** (Phase B) so that there is a well-defined actual
   solution to realize the tail.
2. **Derivative-remainder control** (C4): the passage from `V_b` scaling to
   `R = V_a/V_b` and to the coefficient equation requires a justified expansion with
   controlled remainders.
3. **No exotic competing regime:** the formal exclusion of `p != 2` power/log/
   slowly-varying families does not by itself rule out an *a priori unanticipated*
   tail (e.g. a non-uniform-in-`a` construction, a boundary-layer-induced regime, or a
   family requiring a different leading ansatz). This is the "asymptotic realization /
   no exotic competing regime" gate.
4. **Uniformity** over the claimed `(a,z)` support (interior vs full `[0,10]`).

**Therefore:** do NOT infer that the actual HJB solution realizes `p=2` merely because
S3 excludes the known `m=1/2` branch (step 27). S3 membership is an admissibility
class, not an existence/realization theorem.

---

## C4. Derivative-remainder control (step 28)

Passing from "`V_b ~ K/b^2`" to "`R = V_a/V_b = O(1)`" and to the O(1/b) coefficient
equation requires controlling remainders. The accepted DLH-5P/5O rule is explicit:
**do not differentiate leading asymptotic equivalences term-by-term without a
justified remainder-derivative condition.**

The minimal condition used in DLH-5Q (as a theorem-assumption item, NOT established):

```text
(RD) There exist K(a,z), and a remainder R_b such that, for large b,
     |b^2 V_b - K| + |b^2 (V_a - R V_b)| + b |V_a| <= eps(b)   with eps(b) -> 0,
     R = V_a/V_b = O(1) uniformly, and the second-derivative terms entering
     the (formal) remainder of the HJB are o(1/b).
```

Under (RD): `V ~ V_inf - K/b - M(a,z) b^(-3/2) + ...` (p=2 base with a subleading
`a`-dependent part `M/b^(3/2)`), giving `V_a ~ -(2/3)M_a b^(-3/2)` (the DLH-5O/5P
remainder-derivative mechanism), and `R ~ -(2/3)(M_a/K) b^(1/2)` — which would be
`Theta(sqrt(b))` unless `M_a = O(K b^(-1/2))`, i.e. unless the `a`-dependent subleading
part is arranged so that `R = O(1)`. Under S3 (`R=O(1)`), this forces the leading
coefficients to be `a`-independent: `d_av V_inf = 0` and `d_aa K = 0` (necessary for
`R=O(1)`, consistent with DLH-5O point 3). A nonzero `R=O(1)` limit arises from a
subleading term `H(a,z)/b^2` with `R -> H_a/K = O(1)`.

**Status:** the remainder-derivative condition (RD) is exactly the kind of
theorem-assumption content that is not derivable from the finite-grid accepted source;
it is a required theorem gate (Phase A A3.5). Without (RD), the formal balance is not
a rigorous statement about the actual solution.

---

## C5. Status of `V_b * b^2 -> K` (step 29)

| Claim | Status |
|---|---|
| `V_b * b^2 -> K` with `K = 4/(rho+r_b)^2` follows from current authority alone | **NO** — not derivable (no existence/realization/remainder control). |
| `V_b * b^2 -> K` conditional on the S3 balance being realized | **YES (conditional)** — if the `p=2` tail is realized with remainder control (RD) and uniformity, the O(1/b) balance gives `K = 4/(rho+r_b)^2` (z-constant). |
| `V_b * b^2 -> K` is unconditionally false | **NOT CLAIMED** — the formal balance is self-consistent, so the tail is a live candidate, but it is not a theorem. |

---

## C6. Bottom line (Phase C)

- Inside S3, the only self-consistent formal tail scale is `p=2`; `p<2`, `p>2`, log,
  slowly-varying, and oscillatory tails are formally excluded (C1-C2).
- This is a **formal dominant-balance exclusion**, not an actual asymptotic theorem
  (C3); it requires existence/comparison, remainder control (RD), no exotic regime,
  and uniformity.
- `V_b*b^2 -> K`: **conditional**, not derivable from current authority.
- These are the `MISSING_ASYMPTOTIC_REALIZATION` components of the DLH-5Q terminal.
