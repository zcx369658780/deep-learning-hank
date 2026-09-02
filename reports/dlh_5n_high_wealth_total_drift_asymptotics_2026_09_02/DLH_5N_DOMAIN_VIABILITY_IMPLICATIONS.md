# DLH-5N Phase F — Domain-Viability Implications (R / W, unresolved)

**Issue #40 Phase F.** States the narrow implications of the theory result (Outcome
B) for the unresolved R/W domain question. This section does NOT choose R or W, does
NOT choose `W_max`, and does NOT freeze anything. It only records what the accepted
theory authority does and does not imply.

Controlling facts from this gate:

1. `r_b*b` is the only provably positive, linearly growing term of `mu_W`.
2. The fixed-`a` liquid-tail sign of `mu_W` is **conditional** on the (unestablished)
   tail decay of `V_b` and the tail behavior of `V_a/V_b` (Outcome B).
3. A formula-level source-consistent family with `mu_W -> +inf` (slow `V_b` decay)
   exists but is not HJB-verified, so the mean-reversion hypothesis is neither proven
   nor refuted at the model level.
4. No statement about `a -> +infinity` is made; `a_max = 10` and the accepted taper
   remain an unresolved truncation/modeling boundary.

---

## Implications for Design W (hybrid joint-wealth `a+b <= W_max`)

- W's coherence as a truncation hypothesis requires total-wealth mean reversion
  (`mu_W < 0`) in the tail. Current accepted theory authority **does not establish**
  the fixed-`a` liquid-tail sign (Outcome B). 
- Therefore W remains a **plausible hypothesis**, not a theory-established domain.
  Freezing W is not authorized by this gate and remains subject to the Owner decision
  U (`DO_NOT_FREEZE_R_OR_W_YET`).
- The specific missing object for W: the tail decay exponent of `V_b`
  (equivalently the asymptotic consumption-wealth ratio `c/b`) and the tail behavior
  of `V_a/V_b` on the accepted finite `a`-support.
- Even if a positive (conditional) fixed-`a` liquid-tail inwardness result were
  established, it would justify at most a "liquid-tail mean-reversion" statement,
  **not** a full two-asset infinite-domain theorem, and would still not authorize a
  numerical `W_max`.

## Implications for Design R (rectangular componentwise constraints)

- The analysis provides **no new support** for R. It does not establish R's
  componentwise law (`mu_a <= 0 AND mu_b <= 0`) in the tail, and the
  truncation-vanishing argument for treating `b <= b_max` as a numerical closure
  remains absent (Issue #39 / DLH-5M finding, unchanged).
- The liquid-tail analysis concerns `b -> +infinity` without an upper-`b` constraint,
  which is a different regime from R's finite rectangle; nothing here changes R's
  status as an unestablished candidate.

## What is NOT implied

- No `W_max` is chosen or implied.
- No new `b_max` or `a_max` is implied.
- No R/W/W1/W2 selection is made.
- No boundary law is implemented or recommended for implementation.
- No stationary, density, tail, or aggregate implication is drawn (stationary KFE
  remains NOT AUTHORIZED under Issue #27).
- The accepted taper is not extrapolated beyond `a_max = 10` as scientific authority.

## Bottom line for the Owner

The accepted household economics do **not**, by themselves, prove high-wealth
total-wealth mean reversion in the fixed-`a` liquid tail; the sign is conditional on
endogenous value-function/control asymptotics that are not yet characterized. This
keeps both R and W unresolved, preserves Recommendation U, and points to a deeper
HJB/value-function asymptotic theory gate (Route N-B) as the next scientific step
before any domain implementation authority.
