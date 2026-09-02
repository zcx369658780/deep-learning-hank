# DLH-5N — Exact Scientific Terminal

**Issue #40 §10.** Exactly one primary terminal is used.

## Primary terminal

```text
DLH_5N_FIXED_A_LIQUID_TAIL_TOTAL_WEALTH_SIGN_CONDITIONAL__MISSING_CONTROL_ASYMPTOTICS_IDENTIFIED
```

**(Outcome B).**

### Why Outcome B (and not A, C, or Blocked)

**Not Outcome A** (`...TOTAL_WEALTH_INWARDNESS_ESTABLISHED__DOMAIN_DESIGN_REVIEW_MAY_RESUME`):
accepted authority is **not** sufficient to prove `mu_W < 0` for all sufficiently
large `b`, uniformly over the accepted finite `a`-support and productivity states. The
only provably positive `O(b)` term of `mu_W` is `r_b*b`; every negative term
(consumption, adjustment cost) and the offsetting `labor_income` are controlled by the
tail behavior of `V_b` and `V_a/V_b`, which accepted authority does not characterize
(Phases A-C). No unaccepted assumption may be added.

**Not Outcome C** (`...NONINWARD_COUNTEREXAMPLE_ESTABLISHED__W_DIRECTION_WEAKENED`):
a source-**formula**-consistent family with `mu_W -> +inf` exists (Phase D, M4), but it
is not shown to satisfy the full accepted HJB equation, so it does **not** demonstrate
at the model level that total drift need not be inward. Outcome C requires an
established counterexample; only a conditional, formula-level family is available, and
whether an HJB-consistent solution with slow `V_b` decay exists is unidentified.
Calling C would overclaim and would wrongly weaken the W direction on unproven
grounds.

**Not Blocked** (`BLOCKED_DLH_5N_ACCEPTED_SOURCE_OR_ASYMPTOTIC_OBJECT_INCONSISTENCY`):
there is no source/evidence inconsistency. The accepted source identities are
internally consistent and verified to machine precision (accepted DLH-5L Phase A), and
the accepted DLH-5M package is coherent.

**Outcome B** is exactly the situation: the sign of `mu_W` in the fixed-`a` liquid
tail can be characterized **only conditionally** on explicit growth assumptions for
endogenous controls/value derivatives (`V_b` tail decay, equivalently the asymptotic
consumption-wealth ratio `c/b`, and the tail behavior of `V_a/V_b`), and **those
assumptions are not established by current accepted authority**.

## Statement carried by this terminal

Under the currently accepted household equations with `a in [0,10]` fixed, the
accepted taper held fixed, `z in {0.8,1.3}` finite, and `b -> +infinity` (no upper
`b` constraint, no `W_max`):

- `mu_W = r_b*b + O(1) + o(b)`-terms, with `r_b = 0.015 > 0` (provable).
- The tail sign is **conditional**: inward iff
  `consumption - labor_income + chi - transfer_income` eventually exceeds
  `r_b*b + r_a_eff(a)*a` (e.g. `V_b = O(b^{-(2+delta)})` with bounded transfer);
  outward in the slow-decay family (`V_b ~ b^{-p}`, `0 < p < 2`,
  `V_a/V_b = o(b)`).
- The **missing control asymptotics are identified**: (1) tail decay exponent of
  `V_b` (asymptotic `c/b`), (2) tail behavior of `V_a/V_b` (drives `d` and `chi`),
  (3) labor tail (secondary). None is established by accepted authority.

## What this terminal does NOT do

- Does not freeze R or W; does not choose `W_max`; does not imply any new
  `b_max`/`a_max`.
- Does not establish or refute high-wealth mean reversion at the model level.
- Does not authorize stationary KFE, densities, tails, aggregates, or any
  implementation.
- Does not extrapolate the accepted taper beyond `a_max = 10`.
- Is not a claim about `a -> +infinity` (fixed-`a` liquid-tail result only).
