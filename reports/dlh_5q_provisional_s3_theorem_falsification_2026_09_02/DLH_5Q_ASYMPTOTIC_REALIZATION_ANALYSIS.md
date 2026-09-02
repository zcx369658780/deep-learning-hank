# DLH-5Q Phase C — Asymptotic-Realization Analysis (Rev 3)

**Issue #43 Phase C (steps 24-28).** Within the provisional S3 class
(`R = V_a/V_b = O(1)` uniformly), determines whether the actual admissible tail must
realize `p=2`. Revisits `p<2`, `p=2`, `p>2` and log/non-power possibilities using the
**accepted combined transfer Hamiltonian** `V_b*[d*(R-1)-chi]`, distinguishes formal
dominant-balance exclusion from an actual asymptotic theorem, and states the
derivative-remainder control required. **Rev 2 corrected the `1<p<2` dominant-order
inequality and the slowly-varying/non-power order accounting** (reviewer `5506978886`),
replaced the degenerate (RD) remainder condition with an explicit non-degenerate
uniform expansion, and narrowed the exclusion claims to the correctly analyzed
families. **Rev 3 adds the z-dependent `1/log b` switch-spectrum case, narrows the
oscillatory-tail statement (monotone-preserving oscillatory remainders are not
exhaustively ruled out), and cleans contract (E) so second derivatives appear only as
auxiliary regularity, not as HJB terms** (reviewer `5507222546`).

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
S*V              ~  -S*K/((p-1) b^(p-1))     [0 if K z-constant]
```

so the consumption/utility terms combine exactly as

```text
u - c*V_b = -2 sqrt(V_b) ~ -2 sqrt(K)/b^(p/2),
```

and the two candidate dominant scales are `1/b^(p/2)` (consumption) and `1/b^(p-1)`
(rho / r_b / S). For `1<p<2` we have `p-1 < p/2`, so `b^(-(p-1))` decays **more
slowly** than `b^(-p/2)`; for `p>2` we have `p/2 < p-1`, so the consumption scale
`b^(-p/2)` is larger. The two scales coincide only at `p=2`.

**Case `1 < p < 2` — rho/r_b/S block dominates (switch-spectrum exclusion).**
Here `p-1 < p/2`, so the leading equation is the `b^(-(p-1))` balance among `rho*V`,
`r_b*b*V_b`, and `S*V` (consumption, `H_tr`, `r_a*V_a` are strictly subleading):

```text
-rho*K/(p-1) = r_b*K - S*K/(p-1)        (leading b^(-(p-1)) equation)
<=>  [rho + (p-1) r_b] K = S*K.
```

`K` must therefore be an eigenvector of the switch generator `S` with eigenvalue
`rho + (p-1) r_b`. For the frozen symmetric `S` (spectrum `{0,-2/3}`), the left scalar
`rho + (p-1) r_b` is strictly positive (rho>0, p>1), so it is **not** an eigenvalue of
`S`. Hence **no nonzero `K` satisfies the leading equation: `1 < p < 2` is excluded by
the switch-spectrum argument.** For z-constant `K` the contradiction is immediate
(`S*K=0` forces `rho + (p-1) r_b = 0`, impossible).

**Case `p > 2` — consumption block dominates and is unbalanced.**
Here `p/2 < p-1`, so `-2 sqrt(K)/b^(p/2)` is the **largest** term; it has no same-order
partner (its same-order partner would have to be a `1/b^(p/2)` term, and there is none;
`u` and `-c V_b` cancel only into the combined `-2 sqrt(V_b)`; `rho*V`, `r_b*b*V_b`,
`S*V` are all smaller at `1/b^(p-1)`, and `H_tr`, `r_a*V_a` are smaller still at
`1/b^p`). **Unbalanced -> formally inconsistent.**

**Case `p = 2` — the O(1/b) balance.**
`p/2 = p-1 = 1`; the O(1/b) balance is `-rho*K + r_b*K - 2 sqrt(K) + (S*K) = 0`, i.e.
`(rho+r_b)K - 2 sqrt(K) = S*K` — the DLH-5O Phase C system — **self-consistent**
(conditional).

This reproduces and confirms DLH-5O Phase B within the S3 class, with the `1<p<2`
exclusion now based on the **correct** dominant system (the rho/r_b/S block, resolved
by the switch spectrum) rather than an unbalanced consumption term: `p<2` and `p>2`
power families are formally inconsistent; `p=2` is the unique self-consistent power
balance. **No `p != 2` power family survives inside S3 at the formal level.**

---

## C2. Log and non-power tails (Rev 3 corrected order accounting)

- **Log tail** (`V_b ~ K/b`): excluded by S1 boundedness (C1): `V ~ -K ln b -> -inf`.
- **Slowly-varying / non-power tails:** consider `V ~ -C(b)`, `C(b) -> 0^+`,
  `C'(b) < 0` (so `V_b = -C'(b) > 0`). The relevant scales are
  `rho*V ~ -rho C(b)`, `r_b*b*V_b ~ -r_b b C'(b)`, and
  `u - c V_b = -2 sqrt(V_b) = -2 sqrt(-C'(b))`. In addition `S*V = -S*C` enters if the
  amplitude is z-dependent.
  - **Power-like `C(b) = b^(-alpha)`, `alpha > 0`.** `C'(b) = -alpha b^(-alpha-1)`,
    `V_b = alpha b^(-alpha-1)`. The consumption scale is `sqrt(V_b) ~ b^(-(alpha+1)/2)`;
    the rho/r_b scale is `b^(-alpha)`. Since `(alpha+1)/2 < alpha` for `alpha > 1` and
    `(alpha+1)/2 > alpha` for `0 < alpha < 1`, the consumption term is subleading for
    `alpha < 1` and dominant for `alpha > 1`.
    - **`0 < alpha < 1` (thicker than `1/b`):** consumption is subleading; the leading
      `b^(-alpha)` balance is `rho*V = r_b*b*V_b + S*V`, i.e. `-rho*C = -r_b b C' - S*C`
      (z-constant amplitude: `S*C = 0`). For `C = b^(-alpha) C(z)`:
      `(rho + r_b alpha) C(z) = S C(z)`, i.e. `C(z)` is an eigenvector of `S` with
      eigenvalue `rho + r_b alpha`. For the frozen spectrum `{0,-2/3}`,
      `rho + r_b alpha > 0` cannot equal `-2/3`, and equals `0` only for
      `alpha = -rho/r_b < 0`. **No positive `alpha` solves the switch-spectrum
      equation -> no `0 < alpha < 1` power-like slow tail.** (The Rev 1 statement
      `alpha = rho/r_b = 4/3` had the sign wrong; the correct z-constant balance
      `-rho*C = r_b*b*(-C')` gives `-rho = r_b alpha`, no positive solution.)
    - **`alpha > 1` (thinner than `1/b`):** consumption `b^(-(alpha+1)/2)` is dominant
      and unbalanced (no same-order partner; `rho*V`, `r_b*b*V_b` are smaller at
      `b^(-alpha)`). **Unbalanced -> excluded** (this reproduces the `p>2` obstruction
      in the value-scale form).
  - **Explicit example `C(b) = 1/log b` (Rev 3 includes the z-dependent case).**
    `V_b = 1/(b log^2 b)`, `rho*C = O(1/log b)`, `r_b*b*V_b = O(1/log^2 b)`,
    `sqrt(V_b) = O(1/(sqrt(b) log b))`. Hence `rho*C` **dominates** (not the
    consumption term, which is the smallest of the three).
    - **z-constant amplitude `A`:** `S*V = 0`; the dominant `O(1/log b)` term `rho*V`
      has **no same-order partner** (nothing else is `O(1/log b)`) — an unmatched rho
      term, so `A = 0`. Excluded. (Rev 1's claim that consumption was algebraically
      larger had the order reversed; corrected.)
    - **z-dependent amplitude `A(z)`:** `S*V = -(S A)/log b` is **also** `O(1/log b)`.
      The leading equation is `rho*V = S*V`, i.e. `-rho A = -S A`, equivalently
      `S A = rho A`: `A(z)` would have to be an eigenvector of `S` with eigenvalue
      `rho = 0.02`. Since `rho` is **not** in the frozen spectrum `{0,-2/3}`, no nonzero
      `A(z)` survives. Excluded by the switch-spectrum argument.
  - **Narrowed conclusion (no general claim):** the **explicitly tested** slow/non-power
    families — power-like `C = b^(-alpha)` (`0<alpha<1` excluded by the switch-spectrum
    equation, `alpha>1` excluded by the unbalanced consumption term) and the example
    `C = 1/log b` (z-constant: unmatched rho term; z-dependent: switch-spectrum
    equation `S A = rho A`) — are excluded by correct order accounting.
    **Broader non-power/exotic classes (e.g. general slowly-varying functions not of
    these forms, oscillatory-envelope constructions that keep `V_b>0`) are NOT claimed
    excluded**; they remain part of the open `ASYMPTOTIC_REALIZATION / NO-EXOTIC-REGIME`
    gate (step 18).

- **Oscillatory tails (Rev 3 narrowed statement):**
  - constructions whose derivative `V_b` changes sign infinitely often violate S1
    `V_b > 0` and are therefore not coherent S3 candidates;
  - **sufficiently small oscillatory remainders around a monotone leading tail may
    keep `V_b > 0`** and are **NOT exhaustively ruled out** by this argument;
  - such monotone-preserving oscillatory/exotic remainders remain part of the open
    `ASYMPTOTIC_REALIZATION / NO-EXOTIC-REGIME` gate unless separately shown harmless.

---

## C3. Formal dominant-balance exclusion vs actual asymptotic theorem (step 26)

The results of C1/C2 are **formal dominant-balance statements about the correctly
analyzed families**: they show that, if `V` admits one of the tested power or
explicitly handled log/slow tail forms with `R=O(1)` and a controlled remainder, then
the only self-consistent scale is `p=2`. They are **NOT** an asymptotic theorem,
because an actual theorem additionally needs:

1. **Existence + comparison** (Phase B) so that there is a well-defined actual
   solution to realize the tail.
2. **Derivative-remainder control** (C4): the passage from `V_b` scaling to
   `R = V_a/V_b` and to the coefficient equation requires a justified expansion with
   controlled remainders.
3. **No exotic competing regime:** the formal exclusion of the `p != 2` power/log and
   the explicitly tested slow families does **not** by itself rule out an *a priori
   unanticipated* tail — a non-uniform-in-`a` construction, a boundary-layer-induced
   regime, or a non-power/exotic family outside the tested forms (step 18). This is the
   "asymptotic realization / no exotic competing regime" gate.
4. **Uniformity** over the claimed `(a,z)` support (interior vs full `[0,10]`).

**Therefore:** do NOT infer that the actual HJB solution realizes `p=2` merely because
S3 excludes the known `m=1/2` branch (step 27). S3 membership is an admissibility
class, not an existence/realization theorem.

---

## C4. Derivative-remainder control (step 28) — Rev 3 non-degenerate contract

Passing from "`V_b ~ K/b^2`" to "`R = V_a/V_b = O(1)`" and to the O(1/b) coefficient
equation requires controlling remainders. The accepted DLH-5P/5O rule is explicit:
**do not differentiate leading asymptotic equivalences term-by-term without a
justified remainder-derivative condition.**

Rev 1's condition `(RD)` contained the degenerate term `|b^2 (V_a - R V_b)|`, which is
identically zero because `R = V_a/V_b`; it supplied no remainder information and has
been **removed**. In its place DLH-5Q adopts an explicit, non-degenerate **uniform
derivative expansion** (theorem-assumption item, NOT established):

```text
(E) There exist a-independent K(z) > 0 and bounded H(a,z) with bounded H_a, and
    remainders r0, r_b, r_a with explicit uniform small-o bounds, such that for
    large b and uniformly on the claimed (a,z) support:

      V    = -K(z)/b + H(a,z)/b^2 + r0,          r0 = o(b^(-2))
      V_b  =  K(z)/b^2 - 2 H(a,z)/b^3 + r_b,     r_b = o(b^(-3))
      V_a  =  H_a(a,z)/b^2 + r_a,                r_a = o(b^(-2))
```

If second or mixed partial derivatives are needed at all, they are invoked **only as
auxiliary regularity** to justify differentiating the expansion (E) (e.g., to validate
the derivative formulas above) — they are **NOT** HJB terms: the frozen HJB is
**first-order** in `(a,b)` (Rev 3 cleanup, reviewer `5507222546`).

Under (E), `R = V_a/V_b = (H_a/b^2 + o(b^-2)) / (K/b^2 + o(b^-2)) -> H_a/K = O(1)`,
provided the derivative remainders are controlled uniformly — the concrete S3-compatible
`a`-dependent subleading mechanism. The leading `K` is `a`-independent (forced by
`R=O(1)`, consistent with DLH-5O point 3); the first `a`-dependent contribution enters
at `O(1/b^2)` through `H`.

**On a retained `M(a,z) b^(-3/2)` term (removed as incoherent in Rev 1):** the Rev 1
statement "`M_a = O(K b^(-1/2))`" is incoherent — `M` is a `b`-independent coefficient,
so a `b`-dependent bound on its derivative is meaningless. The correct statement: a
nonzero `b`-independent `M_a` in a `V_a ~ -(2/3) M_a b^(-3/2)` term generates
`R ~ -(2/3)(M_a/K) sqrt(b)`, which is **outside S3** (`R = Theta(sqrt(b))`, not
`O(1)`). Hence **S3 requires `M_a = 0` at that order**: any `b^(-3/2)` coefficient must
be `a`-independent, and `a`-dependence may enter only at `O(1/b^2)` or smaller, exactly
as in (E).

**Status:** the derivative-remainder expansion (E) — including the uniform small-o
bounds on `r0`, `r_b`, `r_a` and the `K`-a-independence / `H` regularity it requires —
is exactly the kind of theorem-assumption content that is not derivable from the
finite-grid accepted source; it is a required theorem gate (Phase A A3.5). Without (E)
(or an equivalent justified expansion), the formal balance is not a rigorous statement
about the actual solution.

---

## C5. Status of `V_b * b^2 -> K` (step 29)

| Claim | Status |
|---|---|
| `V_b * b^2 -> K` with `K = 4/(rho+r_b)^2` follows from current authority alone | **NO** — not derivable (no existence/realization/remainder control). |
| `V_b * b^2 -> K` conditional on the S3 balance being realized | **YES (conditional)** — if the `p=2` tail is realized with the derivative-remainder contract (E) and uniformity, the O(1/b) balance gives `K = 4/(rho+r_b)^2` (z-constant). |
| `V_b * b^2 -> K` is unconditionally false | **NOT CLAIMED** — the formal balance is self-consistent, so the tail is a live candidate, but it is not a theorem. |

---

## C6. Bottom line (Phase C)

- Inside S3, across the **correctly analyzed families**, the only self-consistent
  formal tail scale is `p=2`:
  - `1 < p < 2`: excluded by the **switch-spectrum argument** — the rho/r_b/S block at
    `b^(-(p-1))` dominates (`p-1 < p/2`), and `[rho + (p-1) r_b] K = S*K` has no
    nonzero `K` because `rho + (p-1) r_b > 0` is not in the switch spectrum `{0,-2/3}`;
  - `p > 2`: consumption block `-2 sqrt(K)/b^(p/2)` dominates (`p/2 < p-1`) and is
    unbalanced;
  - `p = 1` log tail: excluded by S1 boundedness;
  - explicitly tested slow families: `C = b^(-alpha)` (`0<alpha<1` via the
    switch-spectrum equation `(rho + r_b alpha) C = S*C`, no positive `alpha`;
    `alpha>1` via the unbalanced consumption term) and `C = 1/log b` (z-constant:
    unmatched dominant `rho*C`; z-dependent: switch-spectrum equation `S A = rho A`,
    no nonzero `A` since `rho=0.02 notin {0,-2/3}`) are excluded by correct order
    accounting.
  - **Broader non-power/exotic S3 tails are NOT claimed excluded** — they remain part
    of the open `ASYMPTOTIC_REALIZATION / NO-EXOTIC-REGIME` gate.
- This is a **formal dominant-balance statement**, not an actual asymptotic theorem
  (C3); it requires existence/comparison, the derivative-remainder contract (E), no
  exotic regime, and uniformity.
- `V_b*b^2 -> K`: **conditional**, not derivable from current authority.
- These are the `MISSING_ASYMPTOTIC_REALIZATION` components of the DLH-5Q terminal.
