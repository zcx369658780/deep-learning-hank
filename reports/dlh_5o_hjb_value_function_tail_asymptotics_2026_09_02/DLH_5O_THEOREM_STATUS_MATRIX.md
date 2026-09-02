# DLH-5O Phase E — Theorem / Conditional-Theorem / Insufficiency Matrix (rev 2)

**Issue #41 Phase E.** Produces the strongest scientifically valid statement about the
HJB-implied tail, distinguishing: an unconditional theorem derivable from accepted
authority; a conditional dominant-balance theorem requiring explicit
regularity/transversality/transfer-ratio assumptions; an HJB-consistent alternative
tail regime; and insufficiency of the accepted finite-grid source. Every proposed
theorem states its regularity, uniformity, and derivative-control requirements
explicitly.

---

## E1. Unconditional theorem from accepted authority

**NONE derivable.** The accepted source is a finite-grid MATLAB-faithful numerical
solver on `[b_lo,b_max] x [0,a_max] x {z}`. It does **not** specify:

- an unbounded-`b` asymptotic boundary condition or transversality condition
  (Phase A A9);
- the tail scaling of the actual HJB solution (Phase A A10);
- regularity / smooth-continuum convergence of the upwind finite-difference solution on
  the tail (Phase A A7);
- the transfer ratio `R = V_a/V_b` or the a-derivative of the `o(1/b)` remainder
  (Phase A A9b).

Therefore no unconditional statement about `V_b`, `V_a/V_b`, `c/b`, or the sign of
`mu_W` at `b -> +inf` is derivable from accepted authority alone.

> **Outcome A is not attainable from current authority.**

---

## E2. Conditional dominant-balance theorem (rev 2)

**Statement (Conditional p=2 Dominant Balance, rev 2):** Under the following explicit
analytic assumptions —

- (R1) smooth-continuum regularity: the upwind finite-difference HJB solution converges
  to a `C^1` continuum solution of the interior HJB identity (Phase A A5) on the
  fixed-`a` liquid tail, with one-sided derivatives coinciding and the shadow
  components recombining to the actual drift (regularity + tail grid resolution);
- (P-TR) **derivative-control / transfer-ratio premise**: `R = V_a/V_b = o(sqrt(b))`
  uniformly over `(a,z)` (preferably the stronger `R = V_a/V_b = O(1)` uniformly), so
  that the combined transfer Hamiltonian `V_b*[d*(R-1)-chi]` is subleading at `O(1/b)`;
  (rev 1's R1-R4 did not include this and were insufficient to derive
  `K = 4/(rho+r_b)^2` — reviewer 5504354859, blocking 3);
- (R2) the tail admits the power-law ansatz `V ~ V_inf(a,z) - K(a,z)/b` with `V_inf`,
  `K` continuous and positive-`K` (the ansatz itself; a tail boundary /
  transversality specification must be posited because the source does not provide one);
- (R3) uniformity of all rates over `a in [0,10]` and `z in {0.8,1.3}` (assumed or
  proved uniformly; compactness alone is not sufficient);
- (R4) the balance is the realized one (no HJB-consistent exotic regime, including the
  unresolved `m = 1/2` family, is realized; not established from accepted authority) —

then the source-faithful interior balance implies:

```text
V_inf = 0,  K = K(z) constant,  K = 4/(rho+r_b)^2,
c/b = (rho + r_b)/2 = 0.0175,  and  mu_W ~ (r_b - c/b)b < 0  (fixed-a liquid-tail inward),
```

and the transfer/adjustment-cost orders `d = O(1)`, `chi = O(1)`, `labor = o(1)`
(order statements only; the exact `q=-1`/`d=-0.45a`/`chi=0.2475a` values require the
additional assumption `R -> 0`, which is not part of this theorem).

Every step is a derived consequence of the balance (Phases B-D); nothing is imported.
The theorem is **conditional** on R1-R4 + P-TR.

> Status: **CONDITIONAL DOMINANT-BALANCE THEOREM** (premises not established by
> accepted authority; each premise, in particular P-TR, is explicit and auditable).

---

## E3. HJB-consistent alternative tail regime

**None established.** Within the transfer class `R = o(sqrt(b))` uniformly, the pure
power-law families `p<2` and `p>2` are shown asymptotically inconsistent (Phase B
B1-B2); transfer-dominated tails with `m > 1/2` are inconsistent (Phase B B4). A
genuinely HJB-consistent non-inward or alternative regime is **not constructed**.
Outside that transfer class, the critical `m = 1/2` family (`R ~ Theta(sqrt(b))`) is
**not resolved** (its combined transfer term is same-order and its coefficient system
is altered) — it is left **open**, neither accepted nor ruled out.

> **Outcome D is not attainable** (no actual HJB-consistent non-inward regime is
> established; the only self-consistent analyzed balance is inward, conditionally).

---

## E4. Insufficiency

The accepted finite-grid source is **sufficient** to:
- fix the economics and the algebraic form of the interior HJB identity including the
  combined transfer Hamiltonian (Phase A);
- support the conditional derivation of the `p = 2` balance and its full coefficient
  system under the explicit premise set R1-R4 + P-TR (Phases B-D).

The accepted finite-grid source is **insufficient** to:
- establish that the actual HJB solution realizes the `p = 2` balance (no unbounded-
  tail problem is specified: no transversality, no regularity, no transfer-ratio
  control, no uniqueness);
- rule out the unresolved `m = 1/2` family, or exotic regimes, from authority alone.

> Status: **INSUFFICIENT FOR AN UNCONDITIONAL (OR ESTABLISHED) TAIL THEOREM**; the
> correct next step is an **analytic-model specification** (define the unbounded-`b`
> HJB problem, state regularity/transversality/uniformity/transfer-ratio hypotheses,
> then verify or refute the candidate and resolve or rule out the `m = 1/2` family).

---

## Matrix summary (rev 2)

| Row | Statement | Status |
|---|---|---|
| E1 | unconditional theorem from accepted authority | **NONE DERIVABLE** (finite-grid source; no unbounded-tail spec) |
| E2 | `p=2` dominant-balance theorem (V_inf=0, K=4/(rho+r_b)^2, c/b=0.0175, inward) | **CONDITIONAL** on R1-R4 **+ P-TR** (`R=o(sqrt(b))` uniformly, preferably `O(1)`) |
| E3 | HJB-consistent alternative (non-inward) regime | **NOT ESTABLISHED** (power families inconsistent within class; `m=1/2` unresolved) |
| E4 | accepted authority | SUFFICIENT for conditional derivation; INSUFFICIENT for unconditional/established theorem → analytic-model specification gate |
| E5 | transfer self-consistency (`R`, `d`, `chi`, cross-`z`) | ORDER STATEMENTS under P-TR (Phase D); exact `d`/`chi` only under extra `R->0` assumption; a-dependence invalidates the balance via the combined Hamiltonian |
| E6 | `m=1/2` (`R ~ Theta(sqrt(b))`) family | **UNRESOLVED / OPEN** (same-order combined term; coefficient equation altered) |
| E7 | uniformity | MUST be assumed/proved uniformly (R3); not inferred from compactness (accepted DLH-5N finding preserved) |

**Conclusion:** the strongest valid statement is a **conditional dominant balance**
(p = 2, `c/b = (rho+r_b)/2`, fixed-`a` liquid-tail inward) derivable from the
source-faithful interior HJB identity under explicit analytic assumptions — including
the derivative-control / transfer-ratio premise P-TR — that the accepted authority
does not establish. The unresolved `m = 1/2` family is left open. This selects
**Outcome B** (preserved).
