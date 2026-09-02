# DLH-5N — Exact Scientific Terminal

**Issue #40 §10 (rev 2).** Exactly one primary terminal is used. Rev 2 applies the
asymptotic-order corrections of fresh ChatGPT review comment `5503060588`; the
terminal direction is unchanged.

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
(Phases A-C). The unconditional remainder `mu_W - r_b*b` is **not** known to be
`o(b)` (nor `O(1) + o(b)`). No unaccepted assumption may be added.

**Not Outcome C** (`...NONINWARD_COUNTEREXAMPLE_ESTABLISHED__W_DIRECTION_WEAKENED`):
a source-**formula**-consistent family with `mu_W -> +inf` exists (Phase D, M4, built
with a bounded transfer ratio so `d = O(1)`, `chi = O(1)`), but it is not shown to
satisfy the full accepted HJB equation, so it does **not** demonstrate at the model
level that total drift need not be inward. Outcome C requires an established
counterexample; only a conditional, formula-level family is available, and whether an
HJB-consistent solution with slow `V_b` decay exists is unidentified. Calling C would
overclaim and would wrongly weaken the W direction on unproven grounds.

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

- **Unconditional (provable only):** `r_b*b = 0.015 b` is an explicit positive linear
  drift (`O(b)`, `+`); `r_a_eff(a)*a` is uniformly bounded on `[0,10]`
  (`0 <= ... <= 0.27`); `transfer_income` is a fixed `O(1)` scalar (`0.0` in the
  frozen fixture); `V_b > 0` where the consumption FOC applies. The b-orders of
  `labor_income`, `consumption`, `d`, `chi` (and hence of the remainder
  `mu_W - r_b*b`) are **NOT_IDENTIFIED_BY_CURRENT_ACCEPTED_AUTHORITY** absent
  explicit tail assumptions.
- **General net condition (exact identity, not an assumption):** `mu_W <= -eta*b`
  eventually iff the net object
  `consumption + chi - labor_income - transfer_income >= (r_b + eta)*b + r_a_eff(a)*a`
  eventually (`eta > 0`). This is the general condition; the asymptotic `c/b`
  criterion is a **special case** valid only under separately stated
  `labor_income = o(b)` and `chi = o(b)` assumptions.
- **Conditional inwardness (sufficient):** uniformly over `(a,z)`,
  `V_b = O(b^{-(2+delta)})` (upper bound) with bounded `V_a/V_b = O(1)` (so
  `d = O(1)`, `chi = O(1)`) and implied labor decay gives
  `consumption = Omega(b^{1+delta/2})` and `mu_W <= -eta*b` eventually. This is
  sufficient, **not necessary**.
- **Conditional outwardness (sufficient):** uniformly over `(a,z)`,
  `V_b ~ K(a,z) b^{-p}`, `0 < p < 2` with uniform coefficient bounds, and
  `d = o(sqrt(b))` (e.g. `V_a/V_b = O(1)` or `o(sqrt(b))`) so `chi = o(b)`, gives
  `mu_W/b -> r_b > 0`.
- The **missing control asymptotics are identified**: (1) tail decay exponent of
  `V_b` (asymptotic `c/b`), (2) tail behavior of `V_a/V_b` (drives `d` and `chi`;
  `chi = o(b)` needs `d = o(sqrt(b))`), (3) labor tail (`labor_income = C_z V_b^(1/5)`,
  `o(b)` iff `V_b = o(b^5)`), and (4) a uniformity argument for any uniform tail
  conclusion. None is established by accepted authority.

## What this terminal does NOT do

- Does not freeze R or W; does not choose `W_max`; does not imply any new
  `b_max`/`a_max`.
- Does not establish or refute high-wealth mean reversion at the model level.
- Does not authorize stationary KFE, densities, tails, aggregates, or any
  implementation.
- Does not extrapolate the accepted taper beyond `a_max = 10`.
- Is not a claim about `a -> +infinity` (fixed-`a` liquid-tail result only).
