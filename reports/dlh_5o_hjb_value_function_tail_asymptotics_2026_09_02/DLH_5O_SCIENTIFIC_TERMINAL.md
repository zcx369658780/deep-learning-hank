# DLH-5O — Exact Scientific Terminal

**Issue #41 §9.** Exactly one primary terminal is used.

## Primary terminal

```text
DLH_5O_HJB_LIQUID_TAIL_DOMINANT_BALANCE_CONDITIONAL__MISSING_ANALYTIC_ASSUMPTIONS_IDENTIFIED
```

**(Outcome B).**

### Why Outcome B (and not A, C, D, or Blocked)

**Not Outcome A** (`...TOTAL_DRIFT_SIGN_RESOLVED`): the accepted finite-grid
MATLAB-faithful source does **not** define an unbounded-`b` HJB problem — there is no
asymptotic boundary / transversality condition, no regularity or continuum-convergence
statement, and no tail-scaling statement (Phase A A9-A11). Therefore the HJB tail
scaling and a uniform fixed-`a` liquid-tail sign cannot be derived **unconditionally**
from accepted authority.

**Not Outcome C** (`...ANALYTIC_MODEL_SPECIFICATION_REQUIRED`): the accepted source
**is** sufficient to support a genuine **conditional derivation** of the `p = 2`
dominant balance and its full coefficient system (`V_inf = 0`, `K = 4/(rho+r_b)^2`,
`c/b = (rho+r_b)/2 = 0.0175`, transfer/z-switch self-consistency) from the derivable
interior HJB identity and the accepted FOCs. Outcome C is for when the source cannot
justify the desired theorem **even conditionally**; here the conditional candidate is
derived and audited, so the precise match is Outcome B (the missing analytic
assumptions are identified, but the candidate is not established).

**Not Outcome D** (`...NONINWARD_LIQUID_TAIL_REGIME_ESTABLISHED__W_DIRECTION_WEAKENED`):
no actual HJB-consistent non-inward regime is established; in fact the only
self-consistent analyzed balance (`p = 2`) is **inward** (Phase B-E). Outcome D is
not justified.

**Not Blocked** (`BLOCKED_DLH_5O_ACCEPTED_HJB_SOURCE_OR_EQUATION_AUTHORITY_INCONSISTENCY`):
there is no source/equation inconsistency; the accepted identities are internally
consistent and verified to machine precision (accepted DLH-5L Phase A).

**Outcome B** is exactly the situation: a candidate scaling and coefficient system
(`p = 2`, `c/b = (rho+r_b)/2`, fixed-`a` liquid-tail inward) **can be derived only
conditionally on explicit analytic assumptions** (regularity/continuum convergence,
the power-law ansatz + a posited tail boundary/transversality, uniformity, uniqueness)
**that current accepted authority does not establish**.

## Statement carried by this terminal

Under the accepted household economics (`a in [0,10]` fixed, `z in {0.8,1.3}`, the
accepted taper held fixed, `b -> +inf`):

- The accepted source authorizes the exact economics and the algebraic form of the
  interior HJB identity `rho*V = u + mu_b*V_b + mu_a*V_a + S*V` (derivable interior
  identity), but **not** an unbounded-`b` asymptotic boundary / transversality
  condition, nor any tail-scaling statement.
- Among the analyzed source-faithful dominant balances, the pure power-law families
  `p < 2` and `p > 2` and transfer-dominated tails with superlinear adjustment cost
  are **asymptotically inconsistent**; the **`p = 2` bounded-transfer balance** is
  **asymptotically self-consistent** (conditional on the ansatz and analytic
  assumptions R1-R4).
- The `p = 2` balance forces `V_inf = 0`, `K` a-independent and z-constant,
  `K = 4/(rho+r_b)^2 = 3265.3`, and the asymptotic consumption ratio
  `c/b = (rho+r_b)/2 = 0.0175` (derived from the audited O(1/b) balance, not imported).
- Since `c/b = 0.0175 > r_b = 0.015`, the candidate implies `mu_W ~ (r_b - c/b)b =
  -0.0025b < 0` — a **fixed-`a` liquid-tail inward (mean-reverting)** resolution,
  **conditional** on the candidate being the realized HJB tail.
- The **missing analytic assumptions are identified**: (1) a specified unbounded-`b`
  HJB problem (asymptotic boundary / transversality); (2) regularity / continuum
  convergence of the finite-difference solution on the tail; (3) uniformity over
  `(a,z)`; (4) uniqueness of the `p = 2` balance (no HJB-consistent exotic regime).
  None is established by accepted authority.

## What this terminal does NOT do

- Does not freeze R or W; does not choose `W_max`; does not imply any new
  `b_max`/`a_max`.
- Does not establish or refute high-wealth mean reversion at the model level (it is a
  conditional dominant balance).
- Does not authorize stationary KFE, densities, tails, aggregates, or any
  implementation.
- Does not extrapolate the accepted taper beyond `a_max = 10`.
- Is not a claim about `a -> +infinity` (fixed-`a` liquid-tail result only).
