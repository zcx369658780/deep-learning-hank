# DLH-5Q Phase A — Provisional Authority Freeze

**Issue #43 Phase A (step 20).** Exact freeze of the provisional theorem class for
the theorem-verification gate, separating inherited economics, Owner-adopted
provisional assumptions, theorem assumptions still to prove, unresolved endpoint
authority, and claims explicitly outside authority.

---

## A0. Controlling statements

- Owner decision `5506138177`: adopt S1 base provisionally; adopt S2 `V_inf(a,z)=0`
  provisionally; adopt S3 `R=V_a/V_b=O(1)` as the primary working class; keep P-TR
  `R=o(sqrt(b))` as a weaker sensitivity envelope; keep the critical `m=1/2` branch
  outside S3 as a falsification benchmark.
- Activation `5506167630`: binding rules 1-10 (R=O(1) primary; V_inf=0 provisional
  selection; critical branch out-of-class benchmark; no p=2 inference from S3
  membership; explicit existence/comparison/endpoint/realization/convergence audits;
  analytic in-class falsification search; future numerical protocol design only; no
  domain/KFE execution; exact allowlist; stop for fresh review).

---

## A1. Inherited accepted economics (fixed, read-only)

All from the accepted immutable source (blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`)
and frozen D0 configuration (region 0):

| Object | Exact form (accepted) |
|---|---|
| utility | `u = c^(1-gamma_c)/(1-gamma_c) - sum_z w_z l_z^(1+phi)/(1+phi)`, `gamma_c=2`, `phi=5`; for a single region `u = -1/c - w l^6/6` |
| consumption FOC | `c = V_b^(-1/gamma_c) = V_b^(-1/2)` |
| labor FOC | `l = (V_b * net_wage / w)^(1/phi)`, `net_wage = 0.85 z`, so `l = (0.85 z V_b)^(1/5)`; labor income `= 0.85 z l` |
| transfer FOC | `d = a*T(q)/chi_1`, `q = R-1`, `T(q) = min(q+chi_0,0)+max(q-chi_0,0)` (bare-`a`) |
| adjustment cost | `chi(d,a) = chi_0|d| + 0.5 chi_1 d^2/max(a,a_bar)` |
| illiquid return | `r_a_eff(a) = r_a*(1 - 0.1*(a/a_max)^9)`, `a in [0,a_max]`, `a_max=10`, `r_a=0.03` |
| liquid drift | `mu_b = r_b*b + labor - d - chi - c`; `r_b=0.015`, effective `0.025` for `b<0` (gap `0.01`) |
| illiquid drift | `mu_a = r_a_eff(a)*a + d` |
| interior HJB identity | `rho*V = u + mu_b*V_b + mu_a*V_a + S*V` (combined transfer form below), `rho=0.02` |
| combined transfer Hamiltonian | `V_b*[d*(R-1) - chi(d,a)]` (the transfer FOC maximizes exactly this object, up to the bare-`a`/cost-floor caveat) |
| productivity switch | `S` on `z in {0.8,1.3}`, rate `1/3`, spectrum `{0,-2/3}` |

The interior HJB in combined form is

```text
rho*V = u + (r_b*b + labor - c)*V_b + r_a_eff(a)*a*V_a + V_b*[d*(R-1)-chi] + S*V.
```

Numeric anchors: `rho=0.02`, `r_b=0.015`, `(rho+r_b)/2 = 0.0175`,
`K = 4/(rho+r_b)^2 = 3265.3`, `r_b - c/b -> -0.0025`.

---

## A2. Provisional Owner-adopted analytic assumptions (this task only)

1. **S1 base (adopted):** continuous unbounded-positive-`b` extension of the accepted
   interior economics on state space `(b_lo,+inf) x (0,a_max) x {z}`, class
   `V in C(D̄) cap C^1(D)`, `V_b>0`, `V<0`, continuity to finite `b_lo`, compact
   `a in [0,10]`, finite `z`. **Derived:** V monotone increasing in `b`, globally
   bounded, `V_inf(a,z)=lim_{b->+inf}V in [-C,0]` exists pointwise (no growth bound
   needed). `V->0` is NOT an S1 property.
2. **S2 selection (adopted provisionally):** `V_inf(a,z)=0`. This is a
   level/boundary selection assumption. It is NOT a proved necessity and NOT a
   comparison/uniqueness theorem. It does NOT exclude the `m=1/2` branch (that branch
   also has `V_inf=0`).
3. **S3 derivative control (adopted as the primary working class):**
   `R = V_a/V_b = O(1)` uniformly over the claimed `(a,z)` theorem support.
4. **P-TR (sensitivity only):** `R = o(sqrt(b))` uniformly. It is NOT co-equal
   primary theorem authority. (Under S3, P-TR is automatically satisfied since
   `O(1) = o(sqrt(b))`.)
5. **Critical branch (out-of-class benchmark):** `R ~ Theta(sqrt(b))` remains outside
   S3; it is NOT declared economically impossible.

---

## A3. Theorem assumptions still to prove/verify (NOT adopted)

The following are NOT established by current authority and are exactly the gates that
keep the provisional theorem open:

1. **Existence:** existence of an admissible continuous (viscosity or appropriate)
   value solution of the continuous unbounded-`b` HJB problem on
   `(b_lo,+inf) x (0,a_max) x {z}` with the endpoint/tail conventions.
2. **Comparison / uniqueness:** a comparison principle (or equivalent selection
   argument) for the unbounded domain; uniqueness of the value level under `V_inf=0`;
   realized-tail uniqueness.
3. **S2 necessity:** the claim that `V_inf=0` is the *necessary* tail-value condition
   of the actual solution (currently a provisional assumption).
4. **Asymptotic realization:** that the actual admissible solution realizes the `p=2`
   tail (no non-power/log tail, no exotic competing regime, no slowly-varying tail).
5. **Derivative-remainder control:** a justified condition allowing passage from
   `V_b` scaling to `R=V_a/V_b` statements and to the coefficient equation (no
   term-by-term differentiation of leading equivalences without it).
6. **Coefficient convergence:** `V_b*b^2 -> K` (rate), `c/b -> 0.0175`,
   `mu_W/b -> -0.0025`, with stated scope.
7. **Uniformity:** uniformity of `R=O(1)` and the tail coefficients over the claimed
   `(a,z)` support (full `[0,10]` vs compact interior-`a` stated separately).

---

## A4. Unresolved endpoint authority (NOT invented here)

| Endpoint | Status |
|---|---|
| `a=0` bare-`a` corner | `d = a*T(q)/chi_1 = 0` for any `R`; `R` vacuous; `mu_a=0`; the `p=2` balance at `a=0` is the P-TR form. Corner conventions for a theorem must be stated; no new law invented. |
| `a = a_max = 10` | `r_a_eff(10)=0.027>0`; the finite-grid `at_upper_a` branch (`d<0`) is `INHERITED_FINITE_GRID_NUMERICAL_SEMANTICS_ONLY`; the analytic upper-`a` endpoint law is `NEW_ANALYTIC_MODEL_DEFINITION_REQUIRES_OWNER`. **No analytic `a=10` law is invented in DLH-5Q.** |
| `b = b_lo = -2` | the borrowing-rate gap (`0.025` for `b<0`) is accepted economics; the `b_lo` marginal-utility closure is numerical semantics only; adopting `b_lo=-2` as continuous analytic lower boundary is new model definition. The tail result should be `b_lo`-independent (robustness/falsifiability gate). |
| `b -> +inf` tail | the `V_inf=0` condition (S2) is the adopted tail-value selection; an independent transversality statement is a theorem-assumption item. |

---

## A5. Claims explicitly outside authority

- No R/W/W1/W2/`W_max` selection.
- No new numerical `b_max`/`a_max`.
- No taper extrapolation beyond `a_max=10`.
- No HJB/KFE/grid/resolution/stationary execution; no rerun of J0-J5.
- No endpoint KKT or state-domain law implementation.
- No regional GE / multi-province / network training / nominal HANK / calibration /
  policy / welfare / Results.
- No PR / merge / close / successor Issue / self-accept.
- No model freeze; no theorem promotion by Builder.

---

## A6. Freeze summary (one-line class)

**Provisional theorem class:** S1 (bounded monotone continuous value, accepted
economics, unbounded-positive-`b` interior) + S2 (`V_inf=0` provisional tail-value
selection) + S3 (`R=V_a/V_b=O(1)` uniformly, primary), with P-TR as sensitivity only,
the `m=1/2` branch out-of-class, endpoint laws (`a=10`, `b_lo`) unresolved and
Owner-decision items, and existence/comparison/realization/remainder/uniformity as
open theorem gates.
