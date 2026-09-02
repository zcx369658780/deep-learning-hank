# DLH-5P Phase E — Critical `m = 1/2` Transfer Branch Analysis (Rev 2)

**Issue #42 Phase E (Rev 2).** Analyzes the branch

```text
R = V_a/V_b ~ L(a,z) * sqrt(b),   L != 0,
```

using the accepted transfer FOC and the **combined transfer Hamiltonian**
`V_b * [ d*(R-1) - chi(d,a) ]` (never adjustment cost alone). Rev 1's conclusion that
this branch is "ruled out" is **withdrawn** (reviewer `5504929967`, Blocking
corrections 1-2). This revision (a) withdraws the Clairaut `p=1/2` inference,
(b) gives the explicit remainder-derivative mechanism that admits the branch,
(c) derives the general same-order system without the shortcut, (d) audits the
`L ~ a^{-1/2}` interior family and the `max(a,a_bar)` endpoint behavior, and
(e) leaves the branch **unresolved/admissible** on the compact interior per the
reviewer's Option B.

## E0. Rule: no term-by-term differentiation of a leading equivalence

A leading asymptotic equivalence (e.g. `V_b ~ K(z) b^{-p}`) may **not** be
differentiated term-by-term to infer `V_a` or to apply Clairaut to leading terms,
unless an explicit derivative-remainder expansion justifies it. Rev 1 violated this;
Rev 2 does not.

## E1. The remainder-derivative mechanism (Blocking correction 1)

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
```

and the mixed-partial check

```text
partial_a V_b ~ M_a b^{-p-1/2},     partial_b V_a ~ M_a b^{-p-1/2},
```

so **Clairaut is satisfied for arbitrary `p`** (within the expansion's validity), not
only `p=1/2`. Therefore `C^2` smoothness alone does **not** force `p=1/2`; the
`m=1/2` branch can coexist with any `p` (in particular `p=2`) through the
remainder-derivative term `M`. The same missing derivative-remainder control that
mattered in DLH-5O reappears here. **Rev 1's `p=1/2` inference is withdrawn.**

## E2. The `p = 2` base with the `m=1/2` remainder: general same-order system

For the `p=2` base (`K` z-dependent, a-independent) with `M(a,z) != 0`:

```text
V ~ -K(z)/b - (2/3)M(a,z) b^{-3/2} + ...,
V_b ~ K b^{-2} + M b^{-5/2} + ...,
V_a ~ -(2/3)M_a b^{-3/2} + ...,
R ~ -(2/3)(M_a/K) sqrt(b) = L sqrt(b),   L = -(2/3)M_a/K   (a-dependent).
```

Clairaut is satisfied identically: `partial_a V_b ~ M_a b^{-5/2} = partial_b V_a`.
Transfer objects (with `max(a,a_bar)` kept explicit, Blocking correction / step 23):

```text
d = a*T(R-1)/chi_1 ~ a L b^{1/2}/chi_1 = -(2/3) a M_a b^{1/2}/(K chi_1),     (O(sqrt(b)))
chi = chi_0|d| + 0.5 chi_1 d^2/max(a,a_bar)
    ~ 0.5 a^2 L^2 b / (chi_1 max(a,a_bar)),
d q - chi ~ a L^2 b/chi_1 * [1 - 0.5 a/max(a,a_bar)].
  For a >= a_bar:    d q - chi ~ 0.5 a L^2 b / chi_1.
  For 0 < a < a_bar: d q - chi ~ a L^2 b/chi_1 [1 - 0.5 a/a_bar]  (coefficient in (0.5,1) of a L^2 b/chi_1).
```

Combined transfer Hamiltonian term:

```text
V_b * [d q - chi] ~ K b^{-2} * [0.5 a L^2 b/chi_1] = 0.5 a L^2 K/(chi_1 b)   (a>=a_bar),   = O(1/b), a-dependent.
```

Collecting the `O(1/b)` balance of the source-faithful interior HJB (combined form):

| Term | `O(1/b)` coefficient |
|---|---|
| `rho*V` | `-rho*K` (the `M b^{-3/2}` term is lower order) |
| `u = -1/c` | `-sqrt(K)` (c correction is `O(b^{1/2})`, u correction lower order) |
| `(r_b b + labor - c)V_b` | `(r_b - 1/sqrt(K))K` |
| `r_a_eff(a) a V_a` | `0` (this is `O(b^{-3/2})`) |
| combined transfer | `0.5 a L^2 K / chi_1` (a-dependent) |
| `S*V` | `-S*K` |

```text
(rho + r_b)K - 2 sqrt(K) = S*K + 0.5 a L^2 K / chi_1,   L = -(2/3)M_a/K.     (E*)
```

This is the **altered same-order system** for the `m=1/2`/`p=2` branch.

## E3. Audit of the `a`-dependence: `L ~ a^{-1/2}` interior family (Blocking correction 2)

(E*) must hold as a pointwise identity for each `a`. With `K` a-independent, the only
a-dependent term is `0.5 a L^2 K/chi_1`. Rev 1 claimed this "forces `L = 0` globally."
That is too strong: the term is a-independent if

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
  `rho + r_b > 0.5 C/chi_1`, yielding a **continuum** of coefficients
  `c/b = 1/sqrt(K) = (rho + r_b - 0.5 C/chi_1)/2`, which equals `(rho+r_b)/2` only for
  `C = 0` (trivial remainder). So the critical branch is a **coherent altered dominant
  balance on the compact interior**, one-parameter family indexed by the remainder
  amplitude `C(z)`; it is **admissible**, not ruled out. Completing it to a full
  asymptotic series / actual solution (lower orders, z-coupling, transversality,
  endpoints) is **UNRESOLVED**.
- **Full-`[0,10]` uniform smooth realization:** the `L ~ a^{-1/2}` family is singular
  at `a = 0` (`M ~ sqrt(a)` is `C^0` but not `C^1` at `a = 0`; `M_a` diverges). Hence
  no **full-support smooth uniform** critical branch is established by this mechanism.
  This failure at `a=0` does NOT imply global impossibility because the specification
  itself allows an interior-`a` theorem (Phase C).
- **`a -> 0` bare-`a` endpoint:** at `a = 0`, `d = a*T(q)/chi_1 = 0` for any `R`
  (bare-`a` degeneracy), `chi = 0`, `mu_a = 0`; `R` is vacuous at `a=0`, and the
  transfer term `0.5 a L^2 K/chi_1` vanishes. With no transfer term, (E*) reduces to
  the P-TR form `(rho+r_b)K - 2 sqrt(K) = S*K`. The endpoint therefore does not host
  the critical branch; it is the interior-`a` family that matters.

## E4. Status of the critical branch under each candidate (Rev 2)

- **Under S1:** the `m=1/2` branch is **admissible/unresolved** at the dominant-balance
  level on the compact interior (S1 does not restrict `R`); a full-`[0,10]` uniform
  smooth realization is not established. Not ruled out.
- **Under S2:** same — S2's transversality does not control `R` and does not by itself
  exclude the branch (a `V ~ -K/b - (2/3)M b^{-3/2}` value with a bounded-growth
  remainder is consistent with `e^{-rho T} E[V] -> 0` for suitable paths). Not ruled out.
- **Under S3:** the branch is **excluded only by the adopted admissibility class**
  (`R=O(1)` or P-TR), i.e. by Owner-adopted model primitive, **not** by a balance
  argument. This is the only mechanism that removes it.

**Result (Rev 2):** the critical `m=1/2` branch is **not** ruled out; it is a coherent
altered dominant balance on the compact interior (with `L ~ a^{-1/2}` families and a
continuum of coefficients) and is left **UNRESOLVED/ADMISSIBLE** per the reviewer's
Option B. Tail uniqueness (the `p=2` coefficient) holds only under an explicit
S3/P-TR admissibility primitive.

## E5. Consequence for the tail coefficient

The `m=1/2` branch, if realized, yields `c/b = (rho + r_b - 0.5 C(z)/chi_1)/2` — a
family different from the P-TR value `(rho+r_b)/2 = 0.0175` whenever the remainder
amplitude `C != 0`. Therefore the tail coefficient is **not unique** across smooth
dominant balances: the P-TR branch and the `m=1/2` family are distinct admissible
balances on the interior. Only the adopted S3/P-TR primitive selects the `p=2`
coefficient.

## E6. Formal dominant balance vs actual admissible HJB solution

As in Rev 1, this is a statement about **formal dominant balances**. The corrected
conclusion is the opposite of Rev 1: the `m=1/2` branch **cannot be excluded** at the
formal-dominant-balance level (Blocking corrections 1-2). Whether it is realized by an
actual admissible HJB solution (completion of the series, transversality, endpoint
laws) is **UNRESOLVED** and must be treated as an open item in the Phase F contract,
not assumed away.

## E7. Conclusion (Rev 2)

The critical `V_a/V_b ~ Theta(sqrt(b))` branch is **UNRESOLVED/ADMISSIBLE**:
- the Clairaut `p=1/2` inference and the ruling-out are **withdrawn**;
- the remainder-derivative mechanism `V_b = K b^{-p} + M b^{-p-1/2} + ...` satisfies
  Clairaut for arbitrary `p` and realizes `R ~ L sqrt(b)`;
- for the `p=2` base the altered `O(1/b)` system is
  `(rho+r_b)K - 2 sqrt(K) = S*K + 0.5 a L^2 K/chi_1` (`L = -(2/3)M_a/K`), coherent on
  the compact interior with `L ~ a^{-1/2}` families and a continuum of coefficients;
- full-`[0,10]` uniform smooth realizations are not established (singular at `a=0`);
  `a=0` is governed by the bare-`a` degeneracy;
- `max(a,a_bar)` is retained in all transfer coefficients near `a=0`.

Tail uniqueness is therefore **not** available from the balance; it requires the
Owner-adopted S3/P-TR primitive (or a future Phase F resolution).
