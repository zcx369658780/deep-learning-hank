# DLH-5Q Phase D — p=2 Coefficient and Drift Audit

**Issue #43 Phase D (steps 29-31).** Conditional on the `p=2` balance being realized
within the stated theorem assumptions (Phase C), derives/verifies:

```text
(rho+r_b)*K - 2*sqrt(K) = S*K,
K = 4/(rho+r_b)^2,
c/b -> 0.0175,
mu_W/b -> -0.0025,
```

and audits z-switching, labor, transfer, adjustment cost, and fixed-`a` terms at every
same order. States theorem-level vs conditional vs unsupported.

---

## D0. Gate precondition

Phase D is entered **only if** Phase C justifies the `p=2` branch within the stated
theorem assumptions. Since Phase C concludes that `p=2` realization is **conditional**
(not established), everything in this file is a **conditional dominant-balance
derivation**, not a theorem. The coefficient system below is exactly the DLH-5O
Phase C system, restated and audited under S3.

---

## D1. The O(1/b) coefficient system

Assume the `p=2` tail is realized with remainder control (RD) and uniformity:

```text
V ~ -K/b - M(a,z) b^(-3/2) + ...,   V_b ~ K/b^2,   R = V_a/V_b = O(1),   K a-independent.
```

**Same-order audit at O(1/b)** (all terms are the `1/b` coefficients of the combined
HJB):

| Term | O(1/b) coefficient | Note |
|---|---|---|
| `rho*V` | `-rho*K` | from `-K/b` |
| `u = -1/c` | `-sqrt(K)` | `u = -V_b^(1/2)`, `V_b ~ K/b^2` |
| `(r_b*b - c)*V_b` | `r_b*K - sqrt(K)` | `r_b b V_b ~ r_b K/b`; `-c V_b = -V_b^(1/2) ~ -sqrt(K)/b` |
| `labor*V_b` | `0` | `labor ~ (0.85 z V_b)^(1/5) = O(b^(-2/5))`; `labor*V_b = O(b^(-12/5))`, subleading |
| `r_a_eff(a)*a*V_a` | `0` | `V_a = R V_b = O(K/b^2)`; term `= O(1/b^2)` |
| `H_tr = V_b*[d(R-1)-chi]` | `0` | under S3, `d=O(1)`, `chi=O(1)`, `d(R-1)-chi=O(1)`; `H_tr = O(1/b^2)` |
| `S*V` | `-(S*K)` | `S` acts on `z`; `S(-K/b) = -(S K)/b`; zero if `K` z-constant |

The O(1/b) balance is therefore

```text
-rho*K = -sqrt(K) + r_b*K - sqrt(K) - S*K
-rho*K = r_b*K - 2 sqrt(K) - S*K
(rho + r_b)*K - 2 sqrt(K) = S*K.      (D*)
```

**Same-order audit conclusion (step 31):** at O(1/b) the only same-order terms are
`rho*V`, `u - c V_b` (the `-2 sqrt(K)` combination), `r_b*b*V_b`, and `S*V`. Labor,
transfer, adjustment cost, and the fixed-`a` illiquid-return terms are all strictly
subleading (`O(b^(-2/5) b^(-2))`, `O(1/b^2)`, `O(1/b^2)`, `O(1/b^2)` respectively).
The z-switching term is `O(1/b)` and enters through `S*K`.

---

## D2. Solving (D*) for z-constant K

For a z-constant `K` (the symmetric/decoupled candidate), `S*K = 0` and (D*) becomes

```text
(rho + r_b)*K - 2 sqrt(K) = 0
=> sqrt(K) = 2/(rho + r_b)
=> K = 4/(rho+r_b)^2 = 4/(0.035)^2 = 3265.3.
```

**z-constancy of K:** the acceptance note (Issue #42 item 2) controls: if `K` varied
across `z`, the scalar formula would not apply and the coupled `z`-system (D*) must be
solved. The linearized z-stability (Phase E search 4) shows no first-order
z-deformation exists (the required spectral value `(rho+r_b)/2 = 0.0175` is not in the
switch spectrum `{0,-2/3}`), so `K` is (locally) uniquely z-constant; global realized
uniqueness is a theorem gate.

**Consumption ratio:**

```text
c/b = 1/sqrt(K) = (rho+r_b)/2 = 0.0175 > r_b = 0.015.
```

---

## D3. Total-wealth drift

Total wealth `W = b + a`; total-wealth drift

```text
mu_W = mu_b + mu_a = r_b*b + r_a_eff(a)*a + labor - c - chi   (transfer d cancels).
```

Under S3 and the `p=2` tail:

```text
mu_W/b = r_b + (r_a_eff(a)*a)/b + labor/b - c/b - chi/b
       = r_b - c/b + o(1)          (labor/b -> 0, chi/b -> 0 since chi = O(1), (r_a_eff a)/b -> 0)
       = 0.015 - 0.0175 = -0.0025 < 0.
```

The fixed-`a` liquid-tail total-wealth drift is **inward** (mean-reverting), matching
DLH-5O Phase E/F and DLH-5N.

---

## D4. Theorem-level vs conditional vs unsupported (step 31)

| Statement | Status |
|---|---|
| `(rho+r_b)K - 2 sqrt(K) = S*K` with `K = 4/(rho+r_b)^2`, `c/b -> 0.0175`, `mu_W/b -> -0.0025` | **CONDITIONAL** (valid if the `p=2` tail is realized with remainder control, no exotic regime, and uniformity) |
| The actual HJB solution realizes these values | **UNSUPPORTED** (needs existence + comparison + asymptotic realization) |
| `mu_W/b < 0` in the fixed-`a` liquid tail under S3 | **CONDITIONAL** (inward under the `p=2` balance; the out-of-class critical family is also inward) |
| Any `mu_W/b >= 0` branch under S3 | **NOT FOUND** (see falsification search; would require `c/b <= r_b`, i.e. `K >= 1/r_b^2`, outside the S3 balance) |
| Full `[0,10]` uniform version | **UNSUPPORTED** (endpoint authority missing; Phase F) |

---

## D5. Bottom line (Phase D)

Conditional on Phase C realization, the coefficient and drift system is derived from
the audited O(1/b) balance: `K = 4/(rho+r_b)^2`, `c/b -> 0.0175`,
`mu_W/b -> -0.0025 < 0`. The same-order audit is clean (only rho/r_b/consumption/S
at O(1/b); labor/transfer/cost/fixed-`a` subleading). No theorem-level statement is
claimed; no `mu_W/b >= 0` branch is found.
