# DLH-5Q Phase G — Theorem / Falsification Matrix and Terminal

**Issue #43 Phase G (step 39).** Produces the theorem/falsification matrix and the
exact single terminal.

---

## G0. Status legend

- **NOT ESTABLISHED** = the statement is an open theorem gate from current authority.
- **CONDITIONAL** = follows from the provisional class IF a stated gate closes
  (existence/comparison/realization/remainder/uniformity).
- **FORMAL** = a dominant-balance-level statement (not a theorem).
- **SUPPORTED** = the class/statement is internally coherent and is the best available
  candidate.

---

## G1. Theorem / falsification matrix

| Row | Item | Status under provisional S1+S2+S3 |
|---|---|---|
| 1 | **Existence** of an admissible value solution (continuous unbounded-`b` HJB) | **NOT ESTABLISHED** — needs a solution notion + comparison framework on `(b_lo,+inf) x (0,a_max) x {z}`, endpoint data (`a=10`, `b_lo`), uniform estimates (Phase B B1) |
| 2 | **Comparison / uniqueness** | **NOT ESTABLISHED** — `V_inf=0` is a level/boundary selection, not a uniqueness theorem; a comparison principle + class-consistency of `R=O(1)` is required (Phase B B2) |
| 3 | **S2 necessity status** (`V_inf=0` as the actual tail-value condition) | **PROVISIONAL ASSUMPTION** (not a proved necessity); within the `p=2` formal balance the O(1) equation `(rho I - S)V_inf = 0`, `rho not in spec(S)`, forces `V_inf=0` at the formal level (consistent, but not a theorem) |
| 4 | **S3 status** (`R=O(1)` primary; P-TR sensitivity only) | **PROVISIONAL WORKING CLASS** (Owner-adopted); excludes the `m=1/2` branch by class; does NOT prove realized tail is `p=2` |
| 5 | **p=2 asymptotic realization** | **CONDITIONAL / NOT ESTABLISHED** — p=2 is the unique self-consistent formal balance inside S3 (p<2, p>2, log, slowly-varying formally excluded); actual realization needs existence/comparison/remainder-control/no-exotic-regime (Phase C) |
| 6 | **Coefficient convergence** (`V_b*b^2 -> K`, `c/b -> 0.0175`, `mu_W/b -> -0.0025`) | **CONDITIONAL** on p=2 realization; `K=4/(rho+r_b)^2`, `c/b -> 0.0175`, `mu_W/b -> -0.0025 < 0` derived from the O(1/b) balance (Phase D) |
| 7 | **Full-`[0,10]` vs interior-`a` theorem scope** | **INTERIOR-`a` CONDITIONAL ONLY**; full support needs `a=10` and `b_lo` Owner endpoint decisions (Phase F) |
| 8 | **In-class counterexample search** (`p!=2`, log/non-power, remainder, z-coupling, `mu_W/b>=0` under S3) | **NONE FOUND** (formal exclusions; no first-order z-deformation; no `mu_W/b>=0` branch) — S3 not analytically falsified from inside (Phase E) |
| 9 | **Out-of-class critical-branch benchmark** (`R ~ Theta(sqrt(b))`) | **PRESERVED outside S3** as exclusion-cost/falsification benchmark; `UNRESOLVED/ADMISSIBLE` on compact interior-`a`; not declared impossible (Phase E E6) |
| 10 | **Future numerical falsification readiness** | **READY (design only, NOT executed)** — observables `V_a/V_b`, `b^2 V_b`, `c/b`, `d` order, `chi` order, `mu_W/b`, boundary influence, pass/fail thresholds (Phase P) |

---

## G2. Terminal selection

Candidate terminals and their trigger conditions:

- **A** (`...THEOREM_VERIFIED...`): requires existence/selection/asymptotic
  realization/coefficient convergence actually established. **NOT satisfied** (Phase
  B/C gaps are open).
- **B** (`...NOT_CLOSED__MISSING_EXISTENCE_COMPARISON_OR_ASYMPTOTIC_REALIZATION...`):
  existence/comparison or asymptotic realization is missing. **SATISFIED** — exactly
  the state found.
- **C** (`...ANALYTIC_CLASS_FALSIFIED...`): an S3-internal in-class counterexample is
  found. **NOT satisfied** (none found; formal exclusions only).
- **D** (`...INTERIOR_A_TAIL_THEOREM_SUPPORTED...`): theorem support survives for
  interior-`a` with endpoint authority as the only remaining Owner item. **NOT fully
  satisfied** — even the interior-`a` statement is conditional on the open
  existence/comparison/realization gates, so the theorem is not "supported" yet; B is
  the precise state.
- **Blocked** (`...ACCEPTED_HJB_OR_PROVISIONAL_S3_AUTHORITY_INCONSISTENCY`): no
  authority inconsistency found. **NOT triggered.**

**Exact terminal (exactly one):**

```text
DLH_5Q_PROVISIONAL_S3_THEOREM_NOT_CLOSED__MISSING_EXISTENCE_COMPARISON_OR_ASYMPTOTIC_REALIZATION_IDENTIFIED__FALSIFICATION_PROTOCOL_READY
```

---

## G3. Route reasoning (why B)

1. The provisional S3 class is **internally consistent**: no in-class counterexample
   was found (Phase E), so the class is not falsified from inside (not C).
2. The `p=2` balance is the **unique self-consistent formal branch** inside S3, and the
   coefficient/drift system is derived conditional on realization (Phase C/D).
3. But **existence, comparison, and asymptotic realization are not established**
   (Phase B/C): the accepted finite-grid source does not provide an infinite-domain
   existence/comparison framework, endpoint authority (`a=10`, `b_lo`) is unresolved,
   and remainder-control/uniformity are theorem gates. Hence the theorem is **not
   closed**.
4. The endpoint/full-support issue (Phase F) is real but secondary: even the
   interior-`a` statement awaits the Phase B/C gates, so terminal D would overstate
   current support.
5. The future numerical falsification protocol is designed and ready (not executed),
   matching the `FALSIFICATION_PROTOCOL_READY` suffix.

---

## G4. What this terminal does and does not authorize

- Does authorize: STOP for fresh ChatGPT review of the theorem-verification +
  falsification-design package.
- Does NOT authorize: any domain/R/W implementation, any numerical run, any stationary
  KFE, any theorem promotion, any endpoint law, any model freeze, any successor Issue
  by Builder.

---

## G5. Recommendation note (for the Owner route)

Provisional S3 remains a **working analytic class**: internally consistent, with a
conditional p=2 balance and a ready falsification protocol, but not a closed theorem.
The natural next analytic steps (in a future Issue, if the Owner approves) are: (i)
close existence/comparison via a concrete viscosity/comparison framework on the
unbounded domain with the `R=O(1)` class; (ii) resolve the `a=10`/`b_lo` endpoint
authority; (iii) execute the authorized numerical falsification protocol.
