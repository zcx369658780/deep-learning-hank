# DLH-5P Phase E — Critical `m = 1/2` Transfer Branch Analysis

**Issue #42 Phase E.** Analyzes the unresolved branch

```text
R = V_a/V_b ~ L(a,z) * sqrt(b),   L != 0,
```

using the accepted transfer FOC and the **combined transfer Hamiltonian**
`V_b * [ d*(R-1) - chi(d,a) ]` (never adjustment cost alone). The branch is tested as a
smooth, uniform dominant balance under the source-faithful interior balance shared by
all three candidates (Phase A A12/A13). A formal dominant balance is distinguished
from an actual admissible HJB solution.

## E1. Leading transfer and adjustment-cost coefficients under `R ~ L sqrt(b)`

Interior transfer/cost objects (accepted):

```text
q = R - 1 ~ L sqrt(b),   T(q) = min(q+chi_0,0) + max(q-chi_0,0) ~ q - chi_0  (active branch),
d = a*T(q)/chi_1 ~ (a L/chi_1) sqrt(b) =: d1(a,z) sqrt(b),   d1 = a L/chi_1,
chi = chi_0|d| + 0.5 chi_1 d^2/max(a,a_bar) ~ 0.5 chi_1 d1^2 b/max(a,a_bar)
    = 0.5 a^2 L^2 b / (chi_1 max(a,a_bar)),
```

and for `a > a_bar` (`a_bar = 1e-6`):

```text
chi ~ chi1c(a,z) b,   chi1c = 0.5 a L^2 / chi_1,
d*q ~ d*R ~ (a L^2/chi_1) b,
d*q - chi ~ (a L^2/chi_1 - 0.5 a L^2/chi_1) b = 0.5 a L^2 b / chi_1  (order b, does not cancel).
```

The combined transfer Hamiltonian (with `V_b ~ K b^{-p}` to be determined) is

```text
V_b * [d*q - chi] ~ K b^{-p} * (0.5 a L^2/chi_1) b = 0.5 a L^2 K b^{1-p} / chi_1.
```

## E2. Mixed-partial (Clairaut) consistency forces `p = 1/2`

Suppose the value function is smooth (`C^2`) on the tail and `V_b ~ K(a,z) b^{-p}`,
`R ~ L(a,z) b^{1/2}` with `L != 0`. Then

```text
V_a = R*V_b ~ L K b^{1/2-p}.
```

Clairaut's theorem (`partial_a V_b = partial_b V_a`) gives, at leading order,

```text
partial_a V_b ~ (d_a K) b^{-p},        partial_b V_a ~ (1/2 - p) L K b^{-1/2-p}.
```

- If `d_a K != 0`: the two orders differ by `b^{-1/2}` (never equal) — not `C^2`.
- Therefore `d_a K = 0` (`K` a-independent) and `(1/2 - p) L K = 0`; with `L != 0`,
  `K != 0`, this forces **`p = 1/2`**.

**Conclusion (E2):** a nonzero critical branch `R ~ L sqrt(b)` with a smooth value
function is a `p = 1/2` tail, `V_b ~ K(z) b^{-1/2}` (so `V ~ 2 K(z) sqrt(b) + C(a,z) + ...`
with `C_a = L K`), **not** a `p = 2` tail. In particular, the `p = 2` value base
(`V_b ~ K/b^2`) is **incompatible** with `R ~ sqrt(b)`: it would force `L = 0` (the
mixed-partial orders `b^{-2}` vs `b^{-5/2}` cannot match).

## E3. The altered `O(b^{1/2})` balance for the `p = 1/2` tail

Value structure: `V ~ 2 K(z) sqrt(b) + C(a,z) + o(1)`, `C_a = L K`, `K` a-independent.
Substitute into the source-faithful interior balance (combined-Hamiltonian form) and
collect `O(b^{1/2})`:

| Term | `O(b^{1/2})` coefficient |
|---|---|
| `rho*V` | `2 rho K` |
| `(r_b b + labor - c)*V_b` | `r_b K` (`c = V_b^{-1/2} ~ K^{-1/2} b^{1/4}` lower order; `labor = o(1)`) |
| `r_a_eff(a)*a*V_a` | `0` (`V_a ~ C_a = O(1)`, so this is `O(1)`, lower order) |
| combined transfer `V_b*[d*q - chi]` | `0.5 a L^2 K / chi_1` (a-dependent) |
| `S*V` | `2 S*K` |
| `u ~ -K^{1/2} b^{-1/4}` | lower order |

Balance at `O(b^{1/2})`:

```text
2 rho K = r_b K + 0.5 a L^2 K / chi_1 + 2 S*K.        (E*)
```

**Uniformity kills it.** Every `O(b^{1/2})` term except the transfer term is
`a`-independent (`K` a-independent, `S*K` a-independent). The transfer term
`0.5 a L^2 K / chi_1` is `a`-dependent and positive for `a in (0,10]` when `L != 0`.
A single-sided `a`-dependence cannot be matched uniformly over `(0,10]`: the equation
(E*) holds for **one** `a` value at most unless `L = 0`. Hence uniform consistency
forces `L = 0` — contradiction with `L != 0`.

**Switch-spectrum check.** If instead one solves (E*) pointwise for a fixed `a`, the
a-dependent term forces `(2 rho - r_b - 0.5 a L^2/chi_1)K = 2 S*K`. For the symmetric
switch this requires `0.5 a L^2/chi_1 = 2 rho - r_b - 2*lambda` for an eigenvalue
`lambda in {0, -2/3}`, i.e. `L^2 = (2*chi_1/a)(2 rho - r_b - 2 lambda)`. The only
positive options give `L(a) ~ a^{-1/2}` (singular at `a=0`, not smooth, not uniform).
At `a = 0` (where the transfer term vanishes) the equation reduces to
`(rho - r_b/2)K = S*K`; with `rho - r_b/2 = 0.02 - 0.0075 = 0.0125 notin {0,-2/3}`
this has only `K = 0`. Either way, no non-trivial smooth solution exists.

## E4. Status of the critical branch under each candidate

The interior balance and the Clairaut argument are shared by all three candidates
(S1/S2/S3 differ only in tail selection laws; the ruling-out uses only the interior
equation and smoothness/uniformity). Hence:

- **Under S1:** the `m=1/2` branch is **RULED OUT** as a smooth, uniform dominant
  balance (it cannot satisfy the interior balance). It is not ruled out as a
  non-smooth/non-power exotic realization (framework-level gap).
- **Under S2:** same ruling-out (the transversality law is irrelevant to the interior
  `O(b^{1/2})` balance). It is **RULED OUT** as a smooth dominant balance.
- **Under S3:** the branch is additionally **excluded by the admissible class**
  (`R=O(1)` or P-TR), consistent with the balance-level ruling-out.

**Result: the critical `m=1/2` branch is RULED OUT as a smooth, uniform dominant
balance under all three candidates.** This resolves the DLH-5O "unresolved" status
within the dominant-balance framework. The remaining gap is non-smooth/non-power
exotic realizations, which are beyond the framework and beyond accepted authority
(`UNRESOLVED` at that level, and not analyzable from the accepted finite-grid source).

## E5. If the branch were admitted: consequences (for completeness, not realized)

Had the branch been a consistent balance, it would have completely changed the tail:
`V ~ 2 K sqrt(b)` (unbounded value), `c ~ K^{-1/2} b^{1/4}` (sublinear consumption),
`c/b -> 0`, `d ~ sqrt(b)`, `chi ~ b`, `mu_W/b -> r_b - c/b = 0.015` (positive, NOT
inward), and a different (non-`(rho+r_b)/2`) coefficient. Since the branch is ruled
out, none of these apply; the `p=2` result (`c/b = 0.0175`, inward) stands as the
unique smooth dominant balance among the analyzed classes.

## E6. Formal dominant balance vs actual admissible HJB solution

The ruling-out is a statement about **formal dominant balances**: no smooth power-consistent
tail with `R ~ L sqrt(b)` can satisfy the source-faithful interior balance. It is the
strongest analytic statement available from the interior equation and does **not** by
itself constitute a theorem about the actual HJB solution (existence/uniqueness of the
full boundary-value problem, and the realization of the `p=2` balance, require the
Phase F theorem gates). The distinction is explicit: the branch is excluded at the
formal-dominant-balance level; promoting the `p=2` balance to a theorem requires the
full contract of Issue #42 Phase F under an Owner-endorsed candidate.

## E7. Conclusion

The critical `V_a/V_b ~ Theta(sqrt(b))` branch is **ruled out** as a smooth, uniform
dominant balance (Clairaut forces `p=1/2`; the `O(b^{1/2})` balance is then
`a`-dependent and forces `L=0`, equivalently `(rho - r_b/2)K = S*K` has only `K=0`).
Consequently it does **not** obstruct a unique tail specification; the `p=2`
bounded/sub-root-transfer balance remains the unique smooth self-consistent dominant
balance. Non-smooth/non-power exotic realizations remain beyond the dominant-balance
framework (not analyzable from accepted authority).
