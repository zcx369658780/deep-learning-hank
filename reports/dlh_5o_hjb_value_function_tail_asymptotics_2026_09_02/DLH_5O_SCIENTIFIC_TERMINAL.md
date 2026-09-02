# DLH-5O — Exact Scientific Terminal (rev 2)

**Issue #41 §9.** Exactly one primary terminal is used.

## Primary terminal

```text
DLH_5O_HJB_LIQUID_TAIL_DOMINANT_BALANCE_CONDITIONAL__MISSING_ANALYTIC_ASSUMPTIONS_IDENTIFIED
```

**(Outcome B)** — preserved from rev 1. The corrected algebra (rev 2, per reviewer
comment `5504354859`) does **not** force another pre-registered terminal.

### Why Outcome B (and not A, C, D, or Blocked)

**Not Outcome A** (`...TOTAL_DRIFT_SIGN_RESOLVED`): the accepted finite-grid
MATLAB-faithful source does **not** define an unbounded-`b` HJB problem — there is no
asymptotic boundary / transversality condition, no smooth-continuum regularity or
continuum-convergence statement, no tail-scaling statement, and no derivative-control /
transfer-ratio statement for `R = V_a/V_b` (Phase A A9-A11/A9b). Therefore the HJB tail
scaling and a uniform fixed-`a` liquid-tail sign cannot be derived **unconditionally**
from accepted authority.

**Not Outcome C** (`...ANALYTIC_MODEL_SPECIFICATION_REQUIRED`): the accepted source
**is** sufficient to support a genuine **conditional derivation** of the `p = 2`
dominant balance and its full coefficient system (`V_inf = 0`, `K = 4/(rho+r_b)^2`,
`c/b = (rho+r_b)/2 = 0.0175`) from the derivable interior HJB identity (with the
combined transfer Hamiltonian) and the accepted FOCs, **under the explicit
derivative-control / transfer-ratio premise P-TR** (`R = V_a/V_b = o(sqrt(b))`
uniformly, preferably `O(1)`). Outcome C is for when the source cannot justify the
desired theorem **even conditionally**; here the conditional candidate is derived and
audited, so the precise match is Outcome B.

**Not Outcome D** (`...NONINWARD_LIQUID_TAIL_REGIME_ESTABLISHED__W_DIRECTION_WEAKENED`):
no actual HJB-consistent non-inward regime is established; in fact the only
self-consistent analyzed balance (`p = 2`, within the transfer class `R = o(sqrt(b))`)
is **inward** (Phase B-E). The `m = 1/2` family is **unresolved/open**, not a
non-inward regime that is established. Outcome D is not justified.

**Not Blocked** (`BLOCKED_DLH_5O_ACCEPTED_HJB_SOURCE_OR_EQUATION_AUTHORITY_INCONSISTENCY`):
there is no source/equation inconsistency; the accepted identities are internally
consistent and verified to machine precision (accepted DLH-5L Phase A).

**Outcome B** is exactly the situation: a candidate scaling and coefficient system
(`p = 2`, `c/b = (rho+r_b)/2`, fixed-`a` liquid-tail inward) **can be derived only
conditionally on explicit analytic assumptions** (smooth-continuum regularity, the
power-law ansatz + a posited tail boundary/transversality, the derivative-control /
transfer-ratio premise P-TR, uniformity, uniqueness) **that current accepted authority
does not establish**.

## Statement carried by this terminal (rev 2)

Under the accepted household economics (`a in [0,10]` fixed, `z in {0.8,1.3}`, the
accepted taper held fixed, `b -> +inf`):

- The accepted source authorizes the exact economics and the algebraic form of the
  interior HJB identity `rho*V = u + mu_b*V_b + mu_a*V_a + S*V`, including the
  **combined transfer Hamiltonian** `V_b*[d*(V_a/V_b-1) - chi(d,a)]` (derivable
  interior identity), but **not** an unbounded-`b` asymptotic boundary /
  transversality condition, nor any tail-scaling or transfer-ratio statement.
- Within the transfer class `R = V_a/V_b = o(sqrt(b))` uniformly (preferably `O(1)`),
  the pure power-law families `p < 2` and `p > 2` and transfer-dominated tails with
  `m > 1/2` are **asymptotically inconsistent**; the **`p = 2` balance** is
  **asymptotically self-consistent** (conditional on the ansatz, P-TR, and the
  analytic assumptions R1-R4).
- The `p = 2` balance, under P-TR, forces `V_inf = 0`, `K` z-constant,
  `K = 4/(rho+r_b)^2 = 3265.3`, and the asymptotic consumption ratio
  `c/b = (rho+r_b)/2 = 0.0175` (derived from the audited O(1/b) balance, not imported).
  The leading coefficients are a-independent (`d_av V_inf = 0`, `d_aa K = 0`); the
  transfer ratio need not vanish (`R` may be `O(1)` nonzero from the subleading
  remainder), and `d`, `chi`, `mu_a` are **order statements** `O(1)` — the exact
  `q=-1`/`d=-0.45a`/`chi=0.2475a` values hold only under the additional assumption
  `R -> 0`, which is not part of this theorem.
- Since `c/b = 0.0175 > r_b = 0.015`, the candidate implies `mu_W ~ (r_b - c/b)b =
  -0.0025b < 0` — a **fixed-`a` liquid-tail inward (mean-reverting)** resolution,
  **conditional** on the candidate being the realized HJB tail and on P-TR.
- The **missing analytic assumptions are identified**: (1) a specified unbounded-`b`
  HJB problem (asymptotic boundary / transversality); (2) smooth-continuum regularity /
  continuum convergence of the finite-difference solution on the tail; (3) the
  derivative-control / transfer-ratio premise P-TR; (4) uniformity over `(a,z)`;
  (5) uniqueness of the `p = 2` balance, including resolving or ruling out the
  **unresolved `m = 1/2` family** (`R ~ Theta(sqrt(b))`, where the combined transfer
  term is same-order and the coefficient equation is altered). None is established by
  accepted authority.

## What this terminal does NOT do

- Does not freeze R or W; does not choose `W_max`; does not imply any new
  `b_max`/`a_max`.
- Does not establish or refute high-wealth mean reversion at the model level (it is a
  conditional dominant balance).
- Does not claim `R = 0`, `q = -1`, `d = -0.45a`, or `chi = 0.2475a` in general (those
  require the separate `R -> 0` assumption).
- Does not claim `p < 2`/`p > 2` inconsistency outside the transfer class
  `R = o(sqrt(b))`; the `m = 1/2` family is left **open**.
- Does not authorize stationary KFE, densities, tails, aggregates, or any
  implementation.
- Does not extrapolate the accepted taper beyond `a_max = 10`.
- Is not a claim about `a -> +infinity` (fixed-`a` liquid-tail result only).
