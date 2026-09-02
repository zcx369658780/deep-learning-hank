# DLH-5O Phase E — Theorem / Conditional-Theorem / Insufficiency Matrix

**Issue #41 Phase E.** Produces the strongest scientifically valid statement about the
HJB-implied tail, distinguishing: an unconditional theorem derivable from accepted
authority; a conditional dominant-balance theorem requiring explicit
regularity/transversality/asymptotic assumptions; an HJB-consistent alternative tail
regime; and insufficiency of the accepted finite-grid source. Every proposed theorem
states its regularity and uniformity requirements explicitly.

---

## E1. Unconditional theorem from accepted authority

**NONE derivable.** The accepted source is a finite-grid MATLAB-faithful numerical
solver on `[b_lo,b_max] x [0,a_max] x {z}`. It does **not** specify:

- an unbounded-`b` asymptotic boundary condition or transversality condition
  (Phase A A9);
- the tail scaling of the actual HJB solution (Phase A A10);
- regularity / continuum convergence of the upwind finite-difference solution on the
  tail (Phase A A7).

Therefore no unconditional statement about `V_b`, `V_a/V_b`, `c/b`, or the sign of
`mu_W` at `b -> +inf` is derivable from accepted authority alone.

> **Outcome A is not attainable from current authority.**

---

## E2. Conditional dominant-balance theorem

**Statement (Conditional p=2 Dominant Balance):** Under the following explicit
analytic assumptions —

- (R1) the upwind finite-difference HJB solution converges to a `C^1` continuum
  solution of the interior HJB identity (Phase A A5) on the fixed-`a` liquid tail
  (regularity + tail grid resolution);
- (R2) the tail admits the power-law ansatz `V ~ V_inf(a,z) - K(a,z)/b` with
  `V_inf`, `K` continuous and positive-`K` (the ansatz itself; a tail boundary /
  transversality specification must be posited because the source does not provide one);
- (R3) uniformity of all rates over `a in [0,10]` and `z in {0.8,1.3}` (assumed or
  proved uniformly; compactness alone is not sufficient);
- (R4) the balance is the realized one (no HJB-consistent exotic regime; not
  established from accepted authority) —

then the source-faithful interior balance implies:

```text
V_inf = 0,  K = K(z) constant,  K = 4/(rho+r_b)^2,
c/b = (rho + r_b)/2 = 0.0175,  and  mu_W ~ (r_b - c/b)b < 0  (fixed-a liquid-tail inward).
```

Every step is a derived consequence of the balance (Phases B-D); nothing is imported.
The theorem is **conditional** on R1-R4.

> Status: **CONDITIONAL DOMINANT-BALANCE THEOREM** (premises not established by
> accepted authority; each premise is explicit and auditable).

---

## E3. HJB-consistent alternative tail regime

**None established.** The pure power-law families `p<2` and `p>2` are shown
asymptotically inconsistent (Phase B B1-B2); transfer-dominated tails with
superlinear adjustment cost (`m > 1/2`) are inconsistent (Phase B B4). A genuinely
HJB-consistent non-inward or alternative regime is **not constructed** — only the
(conditional, inward) `p = 2` balance is self-consistent among the analyzed classes.
Sub-superlinear transfer regimes and non-power tails are **not analyzable from
accepted authority**.

> **Outcome D is not attainable** (no actual HJB-consistent non-inward regime is
> established).

---

## E4. Insufficiency

The accepted finite-grid source is **sufficient** to:
- fix the economics and the algebraic form of the interior HJB identity (Phase A);
- support the conditional derivation of the `p = 2` balance and its full coefficient
  system (Phases B-D).

The accepted finite-grid source is **insufficient** to:
- establish that the actual HJB solution realizes the `p = 2` balance (no unbounded-
  tail problem is specified: no transversality, no regularity, no uniqueness);
- rule out exotic regimes from authority alone.

> Status: **INSUFFICIENT FOR AN UNCONDITIONAL (OR ESTABLISHED) TAIL THEOREM**; the
> correct next step is an **analytic-model specification** (define the unbounded-`b`
> HJB problem, state regularity/transversality/uniformity, then verify or refute the
> candidate).

---

## Matrix summary

| Row | Statement | Status |
|---|---|---|
| E1 | unconditional theorem from accepted authority | **NONE DERIVABLE** (finite-grid source; no unbounded-tail spec) |
| E2 | `p=2` dominant-balance theorem (V_inf=0, K=4/(rho+r_b)^2, c/b=0.0175, inward) | **CONDITIONAL** on explicit R1-R4 (regularity, ansatz+transversality, uniformity, uniqueness) |
| E3 | HJB-consistent alternative (non-inward) regime | **NOT ESTABLISHED** (power families inconsistent; exotic regimes not analyzable) |
| E4 | accepted authority | SUFFICIENT for conditional derivation; INSUFFICIENT for unconditional/established theorem → analytic-model specification gate |
| E5 | transfer self-consistency (`V_a/V_b`, `d`, `chi`, cross-`z`) | DERIVED within candidate (Phase D); a-dependence invalidates the balance |
| E6 | uniformity | MUST be assumed/proved uniformly (R3); not inferred from compactness (accepted DLH-5N finding preserved) |

**Conclusion:** the strongest valid statement is a **conditional dominant balance**
(p = 2, `c/b = (rho+r_b)/2`, fixed-`a` liquid-tail inward) derivable from the
source-faithful interior HJB identity under explicit analytic assumptions that the
accepted authority does not establish. This selects **Outcome B**.
