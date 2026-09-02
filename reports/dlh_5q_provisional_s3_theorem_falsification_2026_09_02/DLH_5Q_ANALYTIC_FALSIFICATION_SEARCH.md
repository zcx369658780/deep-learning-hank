# DLH-5Q Phase E — Analytic Falsification Search (Rev 3)

**Issue #43 Phase E (steps 32-37).** Treats the provisional S3 class
(`R=V_a/V_b=O(1)` uniformly, `V_inf=0`) as falsifiable. Executes **analytic
falsification search only** (no numerical HJB/KFE/grid execution). Searches for
S3-internal alternatives and preserves the accepted critical `m=1/2` family outside S3
as an exclusion-cost benchmark (NOT an in-class counterexample). **Rev 2 corrected the
`1<p<2` dominant-order argument (rho/r_b/S block dominates; switch-spectrum
exclusion), corrected the slow-tail order accounting, and narrowed "no in-class
counterexample" to the correctly analyzed families** (reviewer `5506978886`). **Rev 3
adds the z-dependent `1/log b` switch-spectrum case and narrows the oscillatory-tail
statement to exclude only sign-changing-derivative constructions** (reviewer
`5507222546`).

---

## E0. What would falsify provisional S3 (from inside)

An S3-internal alternative would be a tail with `R=O(1)` and `V_inf=0` that does NOT
realize the `p=2` coefficient balance, i.e. one of:

- a `p != 2` power tail;
- a non-power / log / slowly-varying tail (of a form admitted by the tested ansatze);
- a derivative-remainder construction that changes the `O(1/b)` coefficient;
- a z-coupling or endpoint construction that violates claimed uniformity while
  remaining in S3;
- any formal branch with `mu_W/b >= 0` under S3 (conditional on the realized `p=2`
  balance — E5).

"**No in-class counterexample found**" below means **no counterexample found among the
correctly analyzed families**; it is NOT an exhaustive exclusion of every non-power /
exotic S3 tail (step 22).

---

## E1. Search 1 — an S3-admissible alternative tail with `p != 2`

**Result: NONE FOUND among the power families (formal exclusion, corrected).**

- `1 < p < 2`: the rho/r_b/S block at `b^(-(p-1))` **dominates** (since `p-1 < p/2`);
  the leading equation is `[rho + (p-1) r_b] K = S*K`. For the frozen symmetric `S`
  (spectrum `{0,-2/3}`), `rho + (p-1) r_b > 0` is not an eigenvalue of `S`, so no
  nonzero `K` satisfies it; `1 < p < 2` is excluded by the **switch-spectrum argument**
  (Phase C C1). (Rev 1's "consumption dominates for `p<2`" was the reversed inequality
  and is withdrawn.)
- `p > 2`: `p/2 < p-1`, so the consumption block `-2 sqrt(K)/b^(p/2)` dominates and is
  unbalanced — excluded (Phase C C1).
- `p <= 1`: excluded by S1 boundedness (log tail `V ~ -K ln b`, or `V` unbounded).
- Hence no `p != 2` power tail survives inside S3 at the formal level.

**Caveat:** this is a formal dominant-balance exclusion (Phase C C3), not a theorem;
it cannot rule out an *a priori unanticipated* regime or non-power/exotic families.
It is a negative result for the falsification search, not an in-class counterexample.

---

## E2. Search 2 — an S3-admissible non-power / log tail

**Result: NONE FOUND among the explicitly tested families.**

- **Log tail** (`V_b ~ K/b`): excluded by S1 boundedness (`V ~ -K ln b -> -inf`).
- **Slowly-varying tail** (`V ~ -C(b)`, `C -> 0`, `C'<0`):
  - power-like `C = b^(-alpha)`: the leading balance is the switch-spectrum equation
    `(rho + r_b alpha) C(z) = S C(z)` (z-dependent amplitude); for the spectrum
    `{0,-2/3}` there is **no positive `alpha`** (`alpha = -rho/r_b < 0` for the
    z-constant/eigenvalue-0 case; the `-2/3` case is also negative). `alpha > 1` is
    separately excluded by the unbalanced dominant consumption term. (Rev 1's
    `alpha = rho/r_b = 4/3` had the sign wrong; corrected in Phase C C2.)
  - explicit example `C = 1/log b` (Rev 3 includes the z-dependent case):
    `rho*C = O(1/log b)` dominates (`r_b*b*V_b = O(1/log^2 b)`, consumption
    `O(1/(sqrt(b) log b))`);
    - z-constant amplitude: the dominant `rho*V` has no `O(1/log b)` partner —
      unmatched rho term, excluded;
    - z-dependent amplitude `A(z)`: `S*V = -(S A)/log b` is also `O(1/log b)`, giving
      `S A = rho A`; since `rho = 0.02` is not in `{0,-2/3}`, no nonzero `A(z)`
      survives — switch-spectrum exclusion.
- **Broader non-power/exotic families** (general slowly-varying `C`, oscillatory-
  envelope constructions keeping `V_b>0`, etc.): **NOT claimed excluded**; they remain
  part of the open `ASYMPTOTIC_REALIZATION / NO-EXOTIC-REGIME` gate (step 18).
- **Oscillatory tails (Rev 3 narrowed):** constructions whose derivative changes sign
  infinitely often violate S1 `V_b > 0` and are not coherent S3 candidates; but
  **sufficiently small oscillatory remainders around a monotone leading tail may keep
  `V_b > 0`** and are NOT exhaustively ruled out — they remain in the open
  `ASYMPTOTIC_REALIZATION / NO-EXOTIC-REGIME` gate unless separately shown harmless.

**Caveat:** the tested-family exclusions are formal order-accounting statements
(Phase C C2/C3), not theorems.

---

## E3. Search 3 — an S3-admissible derivative-remainder construction changing the p=2 coefficient

**Result: NONE FOUND.** The `O(1/b)` coefficient `K` is pinned by the balance
`(rho+r_b)K - 2 sqrt(K) = S*K` (Phase D D1). Under S3 (`R=O(1)`), the combined
transfer Hamiltonian `H_tr = V_b[d(R-1)-chi]` is a **bounded multiple of `V_b`**, i.e.
`O(1/b^2)`, so it can never enter the `O(1/b)` equation. A remainder construction
could only shift `K` if it made `H_tr` (or `r_a_eff a V_a`, or labor) same-order at
`O(1/b)`, which would require `d` or `chi` (or `R-1`) to grow like `b`, violating
`R=O(1)`. Hence **inside S3 the p=2 coefficient is stable against remainder
constructions** (conditional on the balance; the derivative-remainder contract (E)
must be satisfied — Phase C C4).

**Contrast (out-of-class):** the critical `m=1/2` branch does change the coefficient —
`(rho+r_b)K - 2 sqrt(K) = S*K - 0.5*C*K/chi_1`, `c/b = (rho+r_b+0.5 C/chi_1)/2` (accepted
DLH-5P Rev 4). That is precisely the out-of-class mechanism that S3 excludes by
admissibility.

---

## E4. Search 4 — z-coupling / endpoint constructions violating uniformity inside S3

**z-coupling (result: no first-order violation found).** Suppose a z-dependent
deformation `K(z) = K_bar + eps k(z)` of the p=2 coefficient, `K_bar = 4/(rho+r_b)^2`,
`eps << 1`. Linearizing (D*) `(rho+r_b)K - 2 sqrt(K) = S K` about `K_bar`:

```text
[(rho+r_b) - 1/sqrt(K_bar)] k = S k.
```

With `sqrt(K_bar) = 2/(rho+r_b)`, the coefficient is `(rho+r_b) - (rho+r_b)/2 =
(rho+r_b)/2 = 0.0175`. So a nontrivial first-order z-deformation would require `k` to
be an eigenvector of `S` with eigenvalue `(rho+r_b)/2 = 0.0175`. The switch spectrum is
`{0, -2/3}`; `0.0175` is not in it. **No first-order z-deformation exists.** This is a
local (linearized) argument; global realized-z-uniqueness remains a theorem gate.

**Endpoint constructions (result: uniformity not violated by any S3-internal endpoint
branch found):** `a=0` is the bare-`a` corner (R vacuous, `d=0`; balance is the P-TR
form, consistent with `p=2`); `a=10` has **no analytic law invented** (endpoint
authority is an Owner decision — see Phase F); `b_lo` law is unresolved and its
influence on the tail is a robustness/falsifiability gate. A *future* Owner-adopted
`a=10` law that forced a different behavior near `a=10` could in principle break full-
`[0,10]` uniformity — that is an endpoint-authority gap, not an S3-internal
counterexample.

---

## E5. Search 5 — an S3-admissible formal branch with `mu_W/b >= 0`

**Result: NONE FOUND — CONDITIONAL on the realized `p=2` coefficient balance.**
Under the S3 `p=2` balance, `mu_W/b -> r_b - c/b = r_b - (rho+r_b)/2 = -0.0025 < 0`
(Phase D D3). A branch with `mu_W/b >= 0` would require `c/b <= r_b`, i.e.
`sqrt(K) >= 1/r_b`, i.e. `K >= 1/r_b^2 = 4444.4`; but the `p=2` balance pins
`K = 4/(rho+r_b)^2 = 3265.3` (no same-order transfer/cost term can shift it, E3).
This is **conditional on the realized `p=2` coefficient balance**; it is NOT a general
theorem covering every unresolved S3 non-power/exotic tail (step 23). (For reference,
the out-of-class critical family is also inward: `mu_W/b = -0.0025 - 3C/(4 chi_1) < 0`,
accepted DLH-5P Rev 4.)

---

## E6. The critical `m=1/2` family — out-of-class exclusion-cost benchmark (step 37)

The accepted critical family (`R ~ L(a,z) sqrt(b)`, `L != 0`) is **outside S3** and is
preserved as a falsification/adversarial benchmark, NOT an in-class counterexample:

- it is realized by the remainder-derivative mechanism
  `V_b = K b^(-p) + M b^(-p-1/2) + ...` (Clairaut-consistent for arbitrary `p`);
- for the `p=2` base it gives `c/b = (rho+r_b + 0.5 C/chi_1)/2` (a continuum),
  `mu_W/b = -0.0025 - 3C/(4 chi_1) < 0` (inward);
- it is `UNRESOLVED/ADMISSIBLE` on compact interior-`a`; no full-`[0,10]` smooth
  realization is established (singular at `a=0`);
- its status demonstrates the **exclusion cost** of S3: adopting `R=O(1)` removes this
  family by admissibility, not by a balance argument, and does NOT by itself prove the
  realized tail is `p=2`.

**Benchmark role in falsification:** numerical evidence of the `m=1/2` signature
(`R ~ sqrt(b)` growing, `c/b > 0.0175` toward the continuum, `chi/b -> positive
constant`) would falsify the *promotion* of S3 to the actual model (i.e. it would
support terminal C-adjacent / Owner redefinition), even though it is not an in-class
counterexample.

---

## E7. Falsification-search bottom line

| Search | Target | Result |
|---|---|---|
| 1 | `p != 2` power tail in S3 | NONE FOUND among power families (`1<p<2` via switch-spectrum argument; `p>2` via unbalanced consumption; `p<=1` via S1 boundedness) |
| 2 | log / non-power / slowly-varying tail in S3 | NONE FOUND among explicitly tested families (log via S1; `C=b^(-alpha)` via switch-spectrum / unbalanced consumption; `C=1/log b` via unmatched rho term (z-constant) or switch-spectrum `S A = rho A` (z-dependent)); broader non-power/exotic classes (incl. monotone-preserving oscillatory remainders) remain OPEN gates |
| 3 | remainder construction changing p=2 coefficient in S3 | NONE FOUND (H_tr subleading; contract (E) required) |
| 4 | z-coupling / endpoint uniformity violation in S3 | NO first-order z-deformation (spectral obstruction `0.0175 notin {0,-2/3}`); endpoint uniformity = authority gap, not in-class |
| 5 | `mu_W/b >= 0` branch in S3 | NONE FOUND — CONDITIONAL on the realized `p=2` balance (would need `K >= 1/r_b^2`, outside the S3 balance); not a general theorem over all S3 non-power tails |
| Benchmark | critical `m=1/2` family | PRESERVED outside S3 as exclusion-cost benchmark |

**Verdict:** no in-class S3 counterexample was found **among the correctly analyzed
families** (powers `p != 2` via the corrected balances, log and the explicitly tested
slow families via correct order accounting). Provisional S3 is therefore NOT
analytically falsified from inside by those families (so terminal C is not selected).
But the exclusion is **not exhaustive** — broader non-power/exotic S3 tails remain part
of the open `ASYMPTOTIC_REALIZATION / NO-EXOTIC-REGIME` gate, and the class is also NOT
verified as a theorem (Phase B/C gaps). Terminal B is selected.
