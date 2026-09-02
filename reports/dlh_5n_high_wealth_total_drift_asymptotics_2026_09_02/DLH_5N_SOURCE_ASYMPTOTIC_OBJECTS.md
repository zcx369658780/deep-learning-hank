# DLH-5N Phase A — Source Asymptotic-Object Audit

**Issue #40 Phase A (rev 2).** Audits the exact accepted source asymptotic objects
and the frozen D0 inputs that enter `mu_W`, separating provable source facts from
endogenous objects whose asymptotic behavior is not characterized by accepted
authority. Rev 2 applies the asymptotic-order corrections of fresh ChatGPT review
comment `5503060588`.

Source (read-only, immutable): `src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`
(blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`,
SHA-256 `1795718C469FC3B427CAB8E3D5957C133BEAD6EACC9EF0A25A3EDB7211D1A024`).

---

## 1. Frozen D0 inputs (accepted configuration)

From `configs/dlh_5b_two_region_symmetric_anchor.toml` (region index 0) and the
DLH-5L frozen fixture:

| Object | Accepted value | Sign / nature |
|---|---|---|
| `rho` (discount) | 0.02 | > 0 |
| `gamma_c` (CRRA) | 2.0 | > 1; `u(c) = -1/c` |
| `phi` (inverse Frisch) | 5.0 | > 0 |
| `chi_0` (linear adj. cost) | 0.1 | >= 0 |
| `chi_1` (quadratic adj. cost) | 2.0 | > 0 |
| `a_bar` (illiquid floor) | 1e-6 | > 0 |
| `r_b` (liquid return) | 0.015 | **> 0 (sign matters)** |
| `r_a` (illiquid return) | 0.03 | > 0 |
| `a_max` | 10.0 | finite, fixed |
| `a` support | `[0, 10]` | compact |
| `b_lo` | -2.0 | lower bound (not part of the `b -> +inf` tail) |
| `tau` | 0.15 | tax |
| `wages` | [1.0] | positive |
| `migration_costs` | [0.0] | non-negative |
| `labor_weights` | [1.0] | positive |
| `transfer_income` | 0.0 | state-independent scalar (region 0) |
| `z` support | {0.8, 1.3} | finite; Poisson switch rate 1/3 |
| `mu_z`, `sigma_z` | 0.0, 0.0 | deterministic in fixture |
| taper | `r_a*(1 - 0.1*(a/a_max)^9)` | MATLAB-faithful, frozen |
| `rb_gap` | 0.01 | only for `b < 0`; irrelevant to `b -> +inf` |

---

## 2. Exact accepted formulas (implemented source, read-only)

```text
adjustment_cost(d, a) = chi_0*|d| + 0.5*chi_1*d^2 / max(a, a_bar)
transfer_candidate(V_a, V_b, a) = a * T(q) / chi_1,
    q = V_a/V_b - 1,  T(q) = min(q + chi_0, 0) + max(q - chi_0, 0)   (bare a)
matlab_faithful_illiquid_return(a) = r_a*(1 - 0.1*(a/a_max)^9),  0 <= a <= a_max
consumption_from_vb(V_b) = V_b^(-1/gamma_c),  V_b > 0
labor_from_vb(V_b, z) = (V_b * net_wage / labor_weight)^(1/phi)
    net_wage = wages*(1 - tau - migration_costs)*z = 0.85*z
flow_utility(c, l) = c^(1-gamma_c)/(1-gamma_c) - sum(labor_weights * l^(1+phi)/(1+phi))
asset drifts:
    cost = adjustment_cost(d, a)
    labor_income = sum(wages*(1 - tau - migration_costs)*z*labor)
    mu_b = r_b*b + labor_income - d - cost - (consumption - transfer_income)
    mu_a = r_a_eff(a)*a + d
    mu_W = mu_a + mu_b
```

In the frozen fixture `transfer_income = 0.0`, so numerically
`mu_W = r_a_eff(a)*a + r_b*b + labor_income - chi(d,a) - consumption`.

**Source-asymptotic audit points (each object classified):**

| # | Object | Source fact (accepted) | Asymptotic status for `b -> +inf`, `a in [0,10]` fixed, `z in {0.8,1.3}` |
|---|---|---|---|
| A1 | `r_b*b` | `r_b = 0.015 > 0` frozen; linear in `b` | **PROVABLE**: `O(b)`, strictly positive, `-> +inf` |
| A2 | `r_a_eff(a)*a` | `0.03*a*(1 - 0.1*(a/10)^9)`, `a in [0,10]` | **PROVABLE**: `O(1)`, non-negative, `max = 0.27` at `a=10` |
| A3 | `labor_income` | `0.85*z*(0.85*z)^(1/5)*V_b^(1/5)` | **CONDITIONAL**: non-negative; `= O(V_b^(1/5))`; `o(b)` iff `V_b = o(b^5)`; `-> 0` if `V_b -> 0`; **otherwise b-order UNIDENTIFIED** (e.g. `V_b = O(b^5)` gives `O(b)` labor income) |
| A4 | `transfer_income` | frozen scalar `0.0` (region 0) | **PROVABLE**: `O(1)`, state-independent, `0.0` in fixture |
| A5 | `consumption` | `V_b^(-1/gamma_c) = V_b^(-1/2)` | **CONDITIONAL**: positive; growth set by `V_b` tail (key object); with `V_b = O(b^{-(2+delta)})` and `V_b > 0`, `c = Omega(b^{1+delta/2})` |
| A6 | `d = transfer_candidate` | `a*T(V_a/V_b - 1)/chi_1`, bare `a` | **CONDITIONAL**: `d = O(1)` iff `V_a/V_b = O(1)`; `d = o(sqrt(b))` iff `T(q) = o(sqrt(b))` (sufficient for `chi = o(b)`); otherwise order UNIDENTIFIED (`d = o(b)` alone does NOT give `chi = o(b)`) |
| A7 | `chi(d,a)` | `0.1|d| + d^2/max(a,a_bar)` | **CONDITIONAL**: non-negative; **`o(b)` requires `d = o(sqrt(b))`** (NOT merely `d = o(b)`, because of the quadratic term); `O(1)` iff `d = O(1)` |
| A8 | `V_b` | positive; no accepted tail bound | **NOT IDENTIFIED BY ACCEPTED AUTHORITY** (the decisive missing object) |
| A9 | `V_a/V_b` | no accepted tail bound | **NOT IDENTIFIED BY ACCEPTED AUTHORITY** (drives A6/A7) |
| A10 | `z` process | finite Markov, jump rate 1/3 | finite support alone does **NOT** bound `V(b,a,z')-V(b,a,z)` as `b` grows; HJB `z`-jump contribution has **UNIDENTIFIED** b-order absent a bound on cross-`z` value differences |

---

## 3. Boundary/branch conventions that do NOT enter the asymptotic argument

- The grid boundary branches (`at_upper_b`, `at_lower_b`, `at_upper_a`, `at_lower_a`)
  in `select_matlab_faithful_local_policy` are **finite-grid numerical closure
  conventions**, not analytic conditions for the `b -> +inf` tail at fixed interior
  `a`. They do not appear in the asymptotic balance.
- The `V_b > 0` requirement is accepted (consumption FOC); `consumption_from_vb`
  raises on `V_b <= 0`. In the tail, only `V_b > 0` with the decay question matters.
- The MATLAB-faithful transfer uses **bare `a`** (`a` not `max(a,a_bar)`); for
  `a in [0,10]` fixed this keeps `|d| <= 10*|T(q)|/chi_1`.

---

## 4. Conclusion of Phase A

The only object of `mu_W` that is provably positive and linearly growing in `b` is
`r_b*b` (A1). The `a`-term (A2) is bounded and non-negative. `transfer_income` (A4) is
a fixed scalar (0.0 in the frozen fixture). **Every other object (A3, A5-A9) is
conditional on the tail behavior of the endogenous value derivatives `V_b` and
`V_a/V_b`**, which accepted authority does not characterize; their b-orders (and
hence the remainder `mu_W - r_b*b`) are **NOT_IDENTIFIED_BY_CURRENT_ACCEPTED_AUTHORITY**
absent explicit tail assumptions. There is no accepted theorem about the HJB
solution's behavior as `b -> +infinity`.
