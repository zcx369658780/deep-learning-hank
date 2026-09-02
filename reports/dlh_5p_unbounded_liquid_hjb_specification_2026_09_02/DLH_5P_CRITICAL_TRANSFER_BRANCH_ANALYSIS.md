# DLH-5P Phase E — Critical `m = 1/2` Transfer Branch Analysis (Rev 3)

**Issue #42 Phase E (Rev 3).** Analyzes the branch

```text
R = V_a/V_b ~ L(a,z) * sqrt(b),   L != 0,
```

using the accepted transfer FOC and the **combined transfer Hamiltonian**
`V_b * [ d*(R-1) - chi(d,a) ]` (never adjustment cost alone). Rev 1's "ruled out"
conclusion is withdrawn; Rev 2 established the remainder-derivative mechanism and left
the branch **UNRESOLVED/ADMISSIBLE** (compact interior-`a`); Rev 3 preserves that
status (step 18) and adds the explicit **total-wealth drift accounting** (steps 19-22):
with `C = a L^2` (`a >= a_bar`), `c/b = (rho+r_b - 0.5 C/chi_1)/2`,
`chi/b = 0.5 C/chi_1`, so `mu_W/b = -0.0025 - C/(4 chi_1) < 0` for `C >= 0` — the
critical family changes the consumption ratio but does **not** reverse total-wealth
mean reversion. `max(a,a_bar)` is retained explicitly for `0<a<a_bar`.

## E0. Rule: no term-by-term differentiation of a leading equivalence

A leading asymptotic equivalence (e.g. `V_b ~ K(z) b^{-p}`) may **not** be
differentiated term-by-term to infer `V_a` or to apply Clairaut to leading terms,
unless an explicit derivative-remainder expansion justifies it. Rev 1 violated this;
Rev 2/3 do not.

## E1. The remainder-derivative mechanism

Consider the explicit expansion with a subleading a-dependent remainder

```text
V_b = K(z) b^{-p} + M(a,z) b^{-p-1/2} + o(b^{-p-1/2}),   K_a = 0,
```

valid for `p` in the range where the remainder is subleading to the leading term. This
corresponds to a value function with

```text
V_sub = M(a,z)/(1/2-p) * b^{1/2-p}   (integration of the remainder),
V_a ~ M_a/(1/2-p) * b^{1/2-p},
R = V_a/V_b ~ [M_a/(K(1/2-p))] sqrt(b) =: L(a,z) sqrt(b),
partial_a V_b ~ M_a b^{-p-1/2},     partial_b V_a ~ M_a b^{-p-1/2},
```

so **Clairaut is satisfied for arbitrary `p`** (within the expansion's validity), not
only `p=1/2`. `C^2` smoothness alone does **not** force `p=1/2`; the `m=1/2` branch can
coexist with any `p` through the remainder-derivative term `M`. **Rev 1's `p=1/2`
inference is withdrawn.**

## E2. The `p = 2` base with the `m=1/2` remainder: general same-order system

For the `p=2` base (`K` z-dependent, a-independent) with `M(a,z) != 0`:

```text
V ~ -K(z)/b - (2/3)M(a,z) b^{-3/2} + ...,
V_b ~ K b^{-2} + M b^{-5/2} + ...,
V_a ~ -(2/3)M_a b^{-3/2} + ...,
R ~ -(2/3)(M_a/K) sqrt(b) = L sqrt(b),   L = -(2/3)M_a/K   (a-dependent).
```

This value is monotone in `b` for large `b` (`V_b ~ K b^{-2} > 0`), negative, and
globally bounded (it satisfies the corrected S1 class, Phase B). Clairaut is satisfied
identically: `partial_a V_b ~ M_a b^{-5/2} = partial_b V_a`. Transfer objects (with
`max(a,a_bar)` kept explicit, step 22):

```text
d = a*T(R-1)/chi_1 ~ a L b^{1/2}/chi_1 = -(2/3) a M_a b^{1/2}/(K chi_1),     (O(sqrt(b)))
chi = chi_0|d| + 0.5 chi_1 d^2/max(a,a_bar)
    ~ 0.5 a^2 L^2 b / (chi_1 max(a,a_bar)),
d q - chi ~ a L^2 b/chi_1 * [1 - 0.5 a/max(a,a_bar)].
  For a >= a_bar:    d q - chi ~ 0.5 a L^2 b / chi_1.
  For 0 < a < a_bar: d q - chi ~ a L^2 b/chi_1 [1 - 0.5 a/a_bar]  (max(a,a_bar) explicit; NOT the a>=a_bar formula).
```

Combined transfer Hamiltonian term:

```text
V_b * [d q - chi] ~ K b^{-2} * [0.5 a L^2 b/chi_1] = 0.5 a L^2 K/(chi_1 b)   (a>=a_bar),   = O(1/b), a-dependent.
```

Collecting the `O(1/b)` balance of the source-faithful interior HJB (combined form):

| Term | `O(1/b)` coefficient |
|---|---|
| `rho*V` | `-rho*K` |
| `u = -1/c` | `-sqrt(K)` |
| `(r_b b + labor - c)V_b` | `(r_b - 1/sqrt(K))K` |
| `r_a_eff(a) a V_a` | `0` (this is `O(b^{-3/2})`) |
| combined transfer | `0.5 a L^2 K / chi_1` (a-dependent) |
| `S*V` | `-S*K` |

```text
(rho + r_b)K - 2 sqrt(K) = S*K + 0.5 a L^2 K / chi_1,   L = -(2/3)M_a/K.     (E*)
```

## E3. Audit of the `a`-dependence: `L ~ a^{-1/2}` interior family

(E*) must hold as a pointwise identity for each `a`. With `K` a-independent, the only
a-dependent term is `0.5 a L^2 K/chi_1`, which is a-independent if

```text
a L(a,z)^2 = C(z)  (a-independent),   i.e.   L(a,z) ~ C(z)^{1/2} a^{-1/2}.
```

- **Compact interior-`a` (e.g. `[a_min, a_max - eps]`, `a_min > 0`):** `L ~ a^{-1/2}`
  (equivalently `M ~ -3/2 K sqrt(a)`, smooth away from `a=0`) makes (E*) hold with a
  z-dependent constant, giving the modified coefficient system

  ```text
  (rho + r_b - 0.5 C(z)/chi_1)K - 2 sqrt(K) = S*K.
  ```

  For z-constant `K` this has the positive solution
  `sqrt(K) = 2/(rho + r_b - 0.5 C/chi_1)` whenever
  `rho + r_b > 0.5 C/chi_1`, yielding a **continuum** of consumption ratios
  `c/b = 1/sqrt(K) = (rho + r_b - 0.5 C/chi_1)/2`, which equals `(rho+r_b)/2` only for
  `C = 0` (trivial remainder). So the critical branch is a **coherent altered dominant
  balance on the compact interior**, one-parameter family indexed by `C(z)`; it is
  **admissible**, not ruled out. Completing it to a full asymptotic series / actual
  solution (lower orders, z-coupling, transversality, endpoints) is **UNRESOLVED**.
- **Full-`[0,10]` uniform smooth realization:** the `L ~ a^{-1/2}` family is singular
  at `a = 0` (`M ~ sqrt(a)` is `C^0` but not `C^1` at `a = 0`; `M_a` diverges). Hence
  no **full-support smooth uniform** critical branch is established by this mechanism.
  This failure at `a=0` does NOT imply global impossibility because the specification
  itself allows an interior-`a` theorem (Phase C).
- **`a -> 0` bare-`a` endpoint:** at `a = 0`, `d = 0` for any `R` (bare-`a`), `chi = 0`,
  `mu_a = 0`; `R` is vacuous, and the transfer term `0.5 a L^2 K/chi_1` vanishes. With
  no transfer term, (E*) reduces to the P-TR form `(rho+r_b)K - 2 sqrt(K) = S*K`. The
  endpoint does not host the critical branch; the interior-`a` family matters.

## E4. Total-wealth drift accounting for the critical branch (steps 19-21)

Total wealth is `W = b + a` (liquid + illiquid). The total-wealth drift is

```text
mu_W = mu_b + mu_a = r_b*b + r_a_eff(a)*a + labor_income - c - chi
```

(the internal transfer `d` cancels: it moves wealth between `b` and `a` but does not
change `W`). At the tail, `(r_a_eff a)/b -> 0` and `labor_income/b -> 0`, so

```text
mu_W/b = r_b - c/b - chi/b.
```

For the compact-interior critical family with `a >= a_bar` and `C = a L^2`
(a-independent):

```text
c/b   = (rho + r_b - 0.5 C/chi_1)/2,          (from E3)
chi/b = 0.5 C/chi_1,                           (chi ~ 0.5 a L^2 b/(chi_1 a) = 0.5 C b/chi_1)
mu_W/b = r_b - c/b - chi/b
       = r_b - (rho + r_b - 0.5 C/chi_1)/2 - 0.5 C/chi_1
       = (r_b - rho)/2 - C/(4 chi_1)
       = (0.015 - 0.02)/2 - C/(4 chi_1)
       = -0.0025 - C/(4 chi_1) < 0    for C >= 0.
```

**Key consequence (steps 20-21):**
- **Tail-coefficient / consumption-ratio non-uniqueness:** the critical family gives
  `c/b = (rho+r_b - 0.5 C/chi_1)/2`, a continuum different from the P-TR value
  `(rho+r_b)/2 = 0.0175` whenever `C != 0`. So the consumption ratio is non-unique.
- **Total-wealth-drift-sign implications:** `mu_W/b = -0.0025 - C/(4 chi_1) < 0` for
  `C >= 0`. The adjustment cost is `O(b)` (`chi/b = 0.5 C/chi_1`), which makes the
  total drift **even more inward** than the P-TR value `-0.0025`. **DLH-5P does NOT
  claim the critical branch reverses mean reversion** (no branch with `mu_W/b >= 0` is
  demonstrated): the demonstrated compact-interior critical family has inward
  `mu_W/b < 0`.
- The distinction is explicit: coefficient non-uniqueness (yes) vs
  total-drift-sign non-uniqueness (no, in this family).

## E5. Status of the critical branch under each candidate (Rev 3)

- **Under S1:** the `m=1/2` branch is **admissible/unresolved** at the dominant-balance
  level on the compact interior (S1 does not restrict `R`; the family's value satisfies
  the S1 class). A full-`[0,10]` uniform smooth realization is not established. Not
  ruled out.
- **Under S2:** same — S2's tail-value selection `V_inf = 0` does not control `R`, and
  the family's value has `V_inf = 0` (`V ~ -K/b - (2/3)M b^{-3/2}`), so it is NOT
  excluded by S2. Not ruled out.
- **Under S3:** the branch is **excluded only by the adopted admissibility class**
  (`R=O(1)` or P-TR), i.e. by Owner-adopted model primitive, **not** by a balance
  argument. This is the only mechanism that removes it; it does NOT by itself prove the
  realized tail is `p=2` (Phase F gates remain).

**Result (Rev 3):** the critical `m=1/2` branch is **not** ruled out; it is a coherent
altered dominant balance on the compact interior (with `L ~ a^{-1/2}` families and a
continuum of consumption ratios), with inward `mu_W/b = -0.0025 - C/(4 chi_1) < 0`,
and is left **UNRESOLVED/ADMISSIBLE**. Tail uniqueness (the `p=2` coefficient) holds
only under an explicit S3/P-TR admissibility primitive (and remains to be proved as a
realized-tail statement, Phase F).

## E6. Formal dominant balance vs actual admissible HJB solution

As in Rev 2, this is a statement about **formal dominant balances**. The `m=1/2`
branch **cannot be excluded** at the formal-dominant-balance level. Whether it is
realized by an actual admissible HJB solution (completion of the series, comparison,
transversality, endpoint laws) is **UNRESOLVED** and must be treated as an open item in
the Phase F contract, not assumed away.

## E7. Conclusion (Rev 3)

The critical `V_a/V_b ~ Theta(sqrt(b))` branch is **UNRESOLVED/ADMISSIBLE** (compact
interior-`a`, preserved from Rev 2):
- the Clairaut `p=1/2` inference and the ruling-out are **withdrawn**;
- the remainder-derivative mechanism `V_b = K b^{-p} + M b^{-p-1/2} + ...` satisfies
  Clairaut for arbitrary `p` and realizes `R ~ L sqrt(b)`;
- for the `p=2` base the altered `O(1/b)` system is
  `(rho+r_b)K - 2 sqrt(K) = S*K + 0.5 a L^2 K/chi_1` (`L = -(2/3)M_a/K`), coherent on
  the compact interior with `L ~ a^{-1/2}` families and a continuum of consumption
  ratios;
- **total-wealth drift (a >= a_bar, C = aL^2):** `c/b = (rho+r_b - 0.5 C/chi_1)/2`,
  `chi/b = 0.5 C/chi_1`, `mu_W/b = -0.0025 - C/(4 chi_1) < 0` — the family changes the
  consumption ratio but does **NOT** reverse mean reversion (no `mu_W/b >= 0` branch is
  demonstrated; step 21);
- `max(a,a_bar)` is retained for `0 < a < a_bar`; the `a>=a_bar` formulas are not
  extended through that layer (step 22);
- full-`[0,10]` uniform smooth realizations are not established (singular at `a=0`);
  `a=0` is governed by the bare-`a` degeneracy.

Tail uniqueness is therefore **not** available from the balance; it requires the
Owner-adopted S3/P-TR primitive (or a future Phase F resolution), and even then the
realized-tail statement remains to be proved.
