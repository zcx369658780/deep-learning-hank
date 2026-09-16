# DLH-5V-X — bounded residual-balanced single-`Q` HJB solver-contract DESIGN

**Issue:** #72 / DLH-5V-X
**Title:** `DLH-5V-X: Design a bounded residual-balanced single-Q HJB solver contract after mixed-imbalance diagnosis`
**Task type:** `SCIENTIFIC_NUMERICAL_DESIGN__ROUTE_A_SINGLE_Q_BOUNDED_RESIDUAL_BALANCED_HJB_SOLVER_CONTRACT`
**Route decision:** `APPROVE_ROUTE_A_BOUNDED_RESIDUAL_BALANCED_SOLVER_CONTRACT_DESIGN_AFTER_5VW_TERMINAL_B`
**Authority marker:** `DLH_5VX_ROUTE_A_BOUNDED_SOLVER_DESIGN_AUTHORIZED`
**Initial authoritative activation:** `5696637965`
**Final authoritative activation-refresh:** `5697299096`
**Live `main` at execution:** `f9bb2b2b2fc889839876185c8fc955200ffb412b`
**Dedicated Builder branch:** `dsh/issue-72-dlh-5vx-route-a-bounded-solver-design-2026-09-16`
**Date:** 2026-09-16

## TERMINAL (exactly one)

```
DLH_5VX_ROUTE_A_BOUNDED_SOLVER_DESIGN__MULTIPLE_PLAUSIBLE_ROUTES_REMAIN__OWNER_OR_REVIEWER_ROUTE_SELECTION_REQUIRED
```

**Outcome B.** The design is frozen and internally consistent, but the accepted
evidence does **not** uniquely prefer one executable contract: **three** candidate
families remain admissible and only **one** is refuted. Per the Issue's own frozen
rule, that is a non-selection outcome.

The **direction-agnostic outer frame IS frozen** (a bounded constrained projected
correction with a residual-based merit and a finite three-ladder attempt budget),
including every ladder, threshold, terminal and pseudocode statement. What remains
open is exactly **one** named sub-choice: which correction direction feeds that
frame.

## 1. Scope discipline (DESIGN ONLY)

This Issue is a specification task. `constructed_new_state`, `accepted_iterate`,
`trajectory_run`, `executed_newton`, `executed_tangent`, `executed_trust_region`,
`executed_line_search`, `executed_continuation`, `executed_pseudo_time` are all
**False**.

Enforced structurally, not merely asserted:

- the module imports **no** solver entry point — only scalar constants from the
  accepted Issue #71 module plus stdlib (AST-asserted);
- the strings `build_operator_and_u`, `select_matlab_faithful_local_policy`,
  `asset_drifts_matlab_faithful`, `spsolve`, `lstsq`, `_step(`,
  `iterate_one_value`, `trust_region_solve`, `line_search(`,
  `pseudo_time_update`, `KFE`/`kfe` do **not** occur anywhere in the module;
- no call in the AST resolves (by name or attribute) to any forbidden entry;
- the result surface contains **no** `ndarray` and no numeric vector of
  `state_size` length, so no state object is produced;
- no `V_new` is produced. (The *contract prose* names `V_new` because it specifies
  a future execution Issue; that is text, not a state.)

## 2. Read-only evidence synthesis (accepted Issues #60–#71)

Nine accepted-evidence entries, five of them **negative** (each recorded with its
accepted published value and its design consequence).

| Issue | Accepted fact | Accepted value | Consequence for design |
|---|---|---|---|
| **#60** | Plain value-update damping exhausted: no viable positive-domain step remained | Terminal C — invariant-domain safeguarded HJB update | **REFUTES** family D standalone: pure value damping cannot reach a viable bounded step |
| **#61** | Adaptive pseudo-time / resolvent ladder ran to its authorized discrete floor; after 2 accepted updates the 3rd request was **not executed** — ladder-floor exhaustion, not operator failure | ladder `{1000·2^-k, k=0..20}`, floor `9.5367431640625e-07` | **REFUTES** family D standalone; bounds it to historical baseline |
| **#62** | A positive sub-floor local safe step exists; limiting F3 wall geometry quantified | Outcome A — local continuous resolvent / domain-margin geometry | **SUPPORTS** domain geometry as a usable design component |
| **#63** | Continuous FTB route can drive the **iterate-change statistic** below `1e-7`, yet the same-`Q` Bellman residual remained large | `CONVERGENCE_TOL=1e-07`, `TAU_FTB=0.9`, Terminal B | **REQUIRES** iterate-change and Bellman convergence to be separate, non-substitutable criteria |
| **#64** | Policy-frozen Newton direction exists but raw safe fraction is tiny (`alpha_near=1.86673662256e-04`) and material residual reduction fails at every safe fraction | `ratio_iter=0.999906663403`, `material_reduction=False` | **REFUTES** raw unconstrained Newton standalone (~0.9999 ratio cannot pass a 0.50 material rule) |
| **#68** | Full wall-gradient tangent projection expands the boundary-safe fraction **866.2532997045214×** vs plain Newton (`50.55026467396071×`), staying within `4.7e-06` of the Newton direction | `geometry_improvement_ratio=866.2532997045214`, Terminal C | **SUPPORTS** a projected/constrained direction as the step geometry; the historical failure was the since-removed dual-`Q` contract |
| **#69** | Owner Route A: MATLAB-faithful selected iteration-rate semantics authoritative | OWNER DECISION — ROUTE A SELECTED | **FIXES** the residual and Jacobian definition; no alternate raw-drift `Q` |
| **#70** | ONE selected generator governs solve and validation; validation reuses the record verbatim | selected-Q blob `7857cabb…`, integration `fb5523d…` | **REQUIRES** single-`Q` consistency across policy reselection |
| **#71** | Residual at `V_*` is a mixed fixed-point **cancellation** imbalance; decomposition closes; top-20 policies reproduce; no unique runaway component | `\|\|R\|\|inf=10.435094313164921`, ratio `0.006665998653866562`, closure `4.036238010485249e-11`, Terminal B | **REQUIRES** a residual-based merit; **forbids** any design assuming one component can be zeroed |

## 3. Candidate-family comparison matrix

Each family is assessed on all eight frozen admissibility axes. **No new numerical
trial was run** to compare them; the comparison is algebraic plus accepted stored
evidence.

| Axis | A. policy-frozen / regularized Newton | B. residual / Jacobi preconditioned correction | C. constrained / projected LSQ / trust-region | D. pseudo-time / resolvent (baseline) |
|---|---|---|---|---|
| residual / Jacobian object | `J_frozen = rho*I - Q_frozen`; solve `J d = -R` | `d = -M⁻¹R`, `M = diag(rho - diag(Q))` | `min \|\|J d + R\|\|₂` s.t. tangents, `\|\|d\|\| <= Δ`, linearized `p_b` | implicit resolvent update `((1/δ+rho)I - Q)V = u + V/δ` |
| domain handling | none intrinsic; tiny safe fraction measured | none intrinsic | **explicit**: active wall gradients + linearized `p_b` + trust ball | acceptance-only via `PB_MARGIN` |
| policy reselection | freeze for the model, reselect once, full reassembly | same | deferred to outer loop; full reassembly | implicit each step |
| single-`Q` consistency | compatible only via full reassembly | compatible (consumes Route-A `R`) | **compatible and enforcing** | compatible in principle |
| expected strength | second-order info; exact linear residual `6.96e-11` | cheap, no solve, directly targets `\|\|R\|\|` | **only family combining residual reduction with geometry** (866× safe-fraction gain) | historically robust at moving `V` without destroying the domain |
| accepted contradiction | Issue #64: positive safe step but insufficient reduction (`0.999906663403`) | none accepted; **also not validated** | Issue #68's failure occurred under the now-removed dual-`Q` contract; not yet validated under Route A | **#60** no viable positive-domain step; **#61** ladder floor exhausted |
| boundedness | only with explicit ladders | bounded by frozen fraction ladder | **bounded by construction** | bounded by finite ladder |
| deterministic reproducibility | yes given fixed solver/ladders | **fully** (no factorization) | yes given fixed ordering/tolerance/solver | yes, already accepted |
| suitability for mixed cancellation | untested; one direction cannot zero a cancellation remainder | plausible; acts on the whole residual | **best as outer frame**; residual merit presumes no dominant component | poor: resolvent direction not tied to cancellation structure |
| **admissible** | **YES** (as direction in the frame) | **YES** | **YES** (outer frame) | **NO — refuted by #60/#61** |

**Result: 3 admissible, 1 refuted.** With three admissible families the frozen
selection rule cannot certify a unique route.

## 4. Frozen route-selection rule (declared before measurement)

A single executable contract (Outcome A) may be selected only when:

1. exactly one candidate family is admissible; **and**
2. that family is admissible on every frozen axis; **and**
3. at least one other family is **refuted** by accepted evidence.

Here (1) fails: three families are admissible. Honest outcome: **Outcome B**.
The rule is declared in the module *before* any assessment is computed, so Outcome
A cannot be manufactured post hoc.

## 5. The frozen contract (outer frame, fully specified)

Frozen and internally consistent, with **19 clauses**:

| # | Clause | Frozen content |
|---|---|---|
| 1 | solver state | **V only**; no new economics state, no auxiliary/dual variable |
| 2 | residual | `R(V) = rho*V - u(V) - Q(V)*V` under Owner Route A; `Q` from ONE `final=False` assembly |
| 3 | policy/operator ordering | build one operator → `R` → Bellman test → direction from frozen-policy model → bounded attempts → on acceptance one full reassembly → statistic test. `Q` refreshed **only** by full reassembly |
| 4 | Jacobian | `J = rho*I - Q_frozen` from the **SAME** `Q` used to evaluate `R`; Newton system `J d = -R` |
| 5 | refresh rule | `J` and `Q` refreshed together, once per outer iteration and whenever the active set changes; **FROZEN** inside one attempt sequence |
| 6 | regularization ladder | `λ ∈ {2^-k, k=0..20}`, solve `(J + λ‖diag J‖∞ I) d = -R` |
| 7 | trust-radius ladder | `Δ = Δ₀·2^-k`, `k=0..20`, `Δ₀ = ‖d_λ‖∞` on the first rung |
| 8 | step-fraction ladder | `α ∈ {2^-k, k=0..20}`, floor `2^-20` |
| 9 | active-boundary detection | active when min required `p_b` is within `ACTIVE_BOUNDARY_TOLERANCE = 1e-12` of the floor; **FULL** wall gradients; **MULTIPLE** gradients **stacked**, never averaged |
| 10 | domain-safety rule | candidate admissible iff min `p_b(V_trial) >= CANDIDATE_PB_MARGIN = 1e-12` and finite; tested on the **CANDIDATE STATE**, not the linearization |
| 11 | projection/constraint rule | intersection of active tangent half-spaces, linearized `p_b` inequality, and trust ball; deterministic active set with `CONSTRAINT_TOLERANCE = 1e-9` |
| 12 | merit function | `merit(V) = ‖R(V)‖∞ / RESIDUAL_REFERENCE` when admissible, else `+inf`; **no component-wise merit permitted** |
| 13 | acceptance rule | accepted iff domain-admissible **and** `merit_trial <= merit - ARMIJO_COEFFICIENT·α·merit` with `ARMIJO_COEFFICIENT = 1e-4` |
| 14 | rejection/backoff | deterministic and exhaustive: advance `α`; on exhaustion advance `Δ` and reset `α`; on exhaustion advance `λ` and reset both |
| 15 | max attempts | 21 / 21 / 21 ladders; `MAX_TOTAL_STEP_ATTEMPTS = 63`; outer ceiling 1000 |
| 16 | iterate convergence | `max\|V_new - V\| <= ITERATE_CHANGE_TOL = 1e-7` — a **separate** criterion that never substitutes for the Bellman test |
| 17 | Bellman convergence | `‖R(V_new)‖∞ <= BELLMAN_RESIDUAL_TOL = 1e-3` with the **same** generator; both must hold |
| 18 | fail-closed terminals | the six named terminals below, all non-retrying |
| 19 | logging fields | per attempt: outer index; `(k_λ, k_Δ, k_α)`; `λ`; `Δ`; `α`; `‖d‖∞`; `‖R(V_trial)‖∞`; merit; candidate min `p_b` (**domain margin**); step norm; active nodes + gradient indices; projection status; linear-solve residual; accept/reject **and its exact reason** |

### 5.1 Frozen numerical constants

**Ladders (exact, finite, strictly descending):**

| Ladder | Definition | Length | Floor |
|---|---|---|---|
| regularization `λ` | `{2^-k, k = 0..20}` | 21 | `9.5367431640625e-07` |
| trust radius fraction | `{2^-k, k = 0..20}` | 21 | `9.5367431640625e-07` |
| step fraction `α` | `{2^-k, k = 0..20}` | 21 | `9.5367431640625e-07` |

**Thresholds (exact):** `ARMIJO_COEFFICIENT = 1e-4`;
`REQUIRED_RESIDUAL_REDUCTION_RATIO = 0.5`; `MIN_RESIDUAL_REDUCTION_ABSOLUTE = 1e-12`;
`CONSTRAINT_TOLERANCE = 1e-9`; `ACTIVE_BOUNDARY_TOLERANCE = 1e-12`;
`PB_SAFETY_MARGIN = 1e-12`; `CANDIDATE_PB_MARGIN = 1e-12`;
`BASELINE_MIN_PB = 4.8089461301970005e-09`; `LINEAR_SOLVE_RTOL = 1e-12`;
`LINEAR_SOLVE_MAXITER = 4`; `LINEAR_RESIDUAL_TOL = 1e-10`;
`ITERATE_CHANGE_TOL = 1e-7`; `BELLMAN_RESIDUAL_TOL = 1e-3`;
`RESIDUAL_REFERENCE = 10.435094313164921`.

**Maximum attempts (finite integers):** `21 / 21 / 21`, total `63`, outer `1000`,
linear `4`.

The module contains **no** hedge language: `choose adaptively`,
`tune if necessary`, `small enough`, `reasonable tolerance`, `as needed`,
`if appropriate` appear nowhere in the contract or the pseudocode (asserted).

### 5.2 Fail-closed terminals (explicit)

```
BOUNDED_SOLVER_NO_DOMAIN_SAFE_STEP          no domain-admissible candidate at any rung
BOUNDED_SOLVER_NO_RESIDUAL_REDUCING_STEP    candidates admissible, none satisfied sufficient decrease
BOUNDED_SOLVER_LINEAR_SOLVE_FAILURE         regularized solve failed / non-finite direction
BOUNDED_SOLVER_NONFINITE_EVIDENCE           non-finite V, Q, u or residual
BOUNDED_SOLVER_SINGLE_Q_CONTRACT_FAILURE    single-Q contract violated
BOUNDED_SOLVER_ATTEMPT_BUDGET_EXHAUSTED     outer iteration ceiling reached
```

### 5.3 Deterministic pseudocode (22 statements)

```
OUTER: given admissible V_0 (accepted V_*)
 1. build (Q, u, records) = ONE final=False assembly at V; require single-Q
    consistency and finite Q, u
 2. R = rho*V - u - Q*V; merit = ||R||inf / RESIDUAL_REFERENCE
 3. if ||R||inf <= BELLMAN_RESIDUAL_TOL: terminal BELLMAN_CONVERGED
 4. J = rho*I - Q   (frozen-policy Jacobian from the SAME Q)
 5. detect active boundary set; stack FULL wall gradients as constraints
 6. FOR k_lambda in 0..20:
      a. solve (J + lambda_k*||diag(J)||inf*I) d = -R
         (LINEAR_SOLVE_RTOL / MAXITER); failure -> FAILURE_LINEAR_SOLVE
      b. project d onto the constraint intersection (CONSTRAINT_TOLERANCE)
      c. FOR k_delta in 0..20:  Delta = Delta_0*2^-k_delta; clip d
           i. FOR k_alpha in 0..20:  alpha = 2^-k_alpha; V_trial = V + alpha*d
              - if not domain-admissible (min p_b < CANDIDATE_PB_MARGIN or
                non-finite) -> log and continue
              - build ONE final=False assembly at V_trial; require finite
              - merit_trial = ||R(V_trial)||inf / RESIDUAL_REFERENCE
              - if merit_trial <= merit - ARMIJO_COEFFICIENT*alpha*merit
                -> ACCEPT, log reason, break out of all three loops
              - else log reject reason and continue
 7. if no candidate accepted after the bounded product -> fail-closed:
    FAILURE_NO_RESIDUAL_REDUCING_STEP if any candidate was domain-admissible,
    else FAILURE_NO_SAFE_STEP
 8. reselect policy by ONE final=False reassembly at the accepted V
    (full Q refresh; never partial)
 9. statistic = max|V_new - V|; if <= ITERATE_CHANGE_TOL record
    ITERATE_STATISTIC_CONVERGED (NOT a Bellman convergence claim)
10. V <- V_new; if outer count > MAX_OUTER_ITERATIONS -> FAILURE_ATTEMPT_BUDGET
11. loop to step 1
TERMINALS: BELLMAN_CONVERGED (both tests), ITERATE_STATISTIC_CONVERGED only,
           or one of the frozen fail-closed failures.
```

## 6. Material distinction from every accepted failure

| Compared to | Why the frozen frame differs |
|---|---|
| **#60 pure value damping** | Never moves `V` without an explicit residual model; every candidate is tested for positive-`p_b` admissibility **before** acceptance. |
| **#61 resolvent ladder** | Does not use pseudo-time as a route. Uses a bounded **correction** of the residual, so exhausting the fraction ladder rejects the **direction**, not the route. |
| **#64 raw/frozen Newton** | Adds a regularization ladder, the active-boundary tangent projection (measured `866.2532997045214×` safe-fraction gain) and a trust radius, so a useful-nowhere-unconstrained direction can still yield an admissible bounded step. |
| **#68 single-wall tangent trial** | Runs under the accepted single-`Q` Route-A contract, stacks **multiple** active gradients instead of one wall, and uses a bounded three-ladder sequence instead of two fixed trials. |

And the five mandated questions:

- **Residual reduction *and* domain geometry together:** the merit is the residual
  inf-norm while admissibility and the constraint set come from boundary geometry —
  a step must satisfy **both**.
- **Mixed cancellation:** never attributes the residual to one component; the merit
  is the full residual vector and acceptance is a sufficient-decrease comparison,
  not a per-component target.
- **Avoiding the tiny raw-Newton safe fraction:** project onto stacked active wall
  tangents and bound with a trust radius scaled from the first regularized
  direction (both measured in Issue #68 to enlarge the safe fraction by orders of
  magnitude).
- **Avoiding iterate-change-only chasing:** `ITERATE_CHANGE_TOL = 1e-7` and
  `BELLMAN_RESIDUAL_TOL = 1e-3` are separate, non-substitutable, and a
  statistic-converged/residual-unconverged terminal is reported distinctly.
- **Single-`Q` consistency across reselection:** `Q` exists only as the result of a
  full `final=False` reassembly; the linear model is always built from that same
  `Q`; no raw-drift alternate generator and no partial `Q` update appears anywhere.

## 7. Internal consistency check (deterministic, 35 checks)

All checks pass (`consistency_ok = True`, zero failures), including:
ladders exact and strictly descending and matching the accepted Issue #61 floor;
all thresholds finite and matching accepted values (`BELLMAN_RESIDUAL_TOL == 1e-3`,
`ITERATE_CHANGE_TOL == 1e-7`, `BASELINE_MIN_PB == 4.8089461301970005e-09`,
`RESIDUAL_REFERENCE == 10.435094313164921`); convergence criteria separated;
attempt budgets finite integers and consistent with ladder lengths; all 19 contract
clauses present and non-empty; **no adaptive hedge language**; evidence covering
Issues #60–#71 with negative evidence present; all four families present and each
assessed on all eight axes; the baseline family refuted **with** a reason;
pseudocode non-empty, hedge-free, and separating the two convergence notions; the
active set provably uses the **full** wall gradient with **multiple** stacked
gradients; the merit is residual-based (no component-wise merit); the fail-closed
clause names **every** frozen failure terminal; single-`Q` is enforced by full
reassembly; and the logging surface carries both the domain margin and the exact
decision reason.

**Deterministic repeat: identical** (`True`).

## 8. What remains open (the single sub-choice)

The frozen frame is **direction-agnostic**: clause 4 fixes the Jacobian definition
but the correction direction may be either

- **A** — policy-frozen / regularized Newton (`J d = -R`), or
- **B** — residual / Jacobi preconditioned correction (`d = -M⁻¹R`).

Both are admissible on all eight axes and neither is refuted by accepted evidence:
Issue #64 refutes **raw unconstrained** Newton as a standalone route, not Newton as
a direction inside a bounded projected frame; family B has never been measured at
all. Selecting between them requires either an Owner/Reviewer decision or fresh
measured evidence — which this design Issue is explicitly forbidden to generate.

## 9. Authorized files (exact four-path allowlist)

1. `src/deep_learning_hank/two_asset/route_a_bounded_solver_design.py`
2. `tests/test_dlh_5vx_route_a_bounded_solver_design.py`
3. `reports/dlh_5vx_route_a_bounded_solver_design_2026_09_16/DLH_5VX_ROUTE_A_BOUNDED_SOLVER_DESIGN_REPORT.md`
4. `reports/dlh_5vx_route_a_bounded_solver_design_2026_09_16/DLH_5VX_ROUTE_A_BOUNDED_SOLVER_DESIGN_SUMMARY.csv`

**No fifth tracked Builder path.** Accepted blobs verified unchanged: selected-Q
`7857cabb4d28af99cb9d59e2d1c3024b05787c11`, oracle
`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`, Issue #69 audit
`83e9be0febcc03eb721265d3558887bd6b1586a4`, Issue #71 module
`96dd262a4ae42e26d489a317d9a04a9264b481b1`.

## 10. Tests

Focused suite `tests/test_dlh_5vx_route_a_bounded_solver_design.py`:
**50 passed**.

Coverage: accepted selected-Q / oracle / Issue #69 / Issue #71 blobs exact;
Issue #70–#71 integration SHAs pinned; evidence matrix complete over #60–#71 with
negative evidence present and no accepted-history distortion; all four candidate
families present, each assessed on all eight axes with its accepted contradiction
stated; baseline family refuted with a reason; constrained family identified as the
outer frame; deterministic, non-forced route selection (Outcome B) with exactly one
terminal and the rule declared; all 19 contract clauses present; solver state is
`V` only; residual is Route-A single-`Q`; policy refresh, active-boundary,
domain-safety, merit, acceptance and backoff rules explicit; iterate/Bellman
convergence separated; reproducibility logging fields complete; every ladder exact;
every threshold exact; no adaptive hedge language; attempt budgets finite integers;
fail-closed terminals explicit and named; pseudocode deterministic and complete;
material distinction answers all four history comparisons and all five mandated
questions; **no** new state constructed; **no** execution flags set; **no** solver
entry point reachable by AST; **no** solver module imported; internal consistency
all-pass; deterministic artifact repeat identical; CSV summary deterministic.

Full repository suite `python -m pytest tests/ -q`: see §11.

## 11. Full repository suite

**`743 passed, 6 warnings in 3460.60 s (0:57:40)`** — `EXIT=0`, i.e. **0 failed,
0 errors, GREEN**.

The 6 warnings are the pre-existing `MatrixRankWarning` entries from the accepted
oracle tests (`test_dlh_5b`, `test_dlh_5c`) at
`matlab_faithful_two_asset_ha.py:597`; they are unchanged by this Issue.

## 12. Terminal derivation (frozen rule)

- design artifacts complete and internally consistent: **yes** (35/35 checks);
- all four families compared on all eight axes without new numerical trials: **yes**;
- admissible families: **3** (A, B, C); refuted: **1** (D, by #60/#61);
- unique admissible family: **NO**;
- therefore Outcome A is **not** available and Outcome C does not apply (a
  justified bounded frame **does** exist).

→ **Outcome B**, exactly one terminal. The direction-agnostic outer frame is frozen
and ready; the direction sub-choice is escalated.

## 13. Interpretation ceiling — no convergence claim

Passing this Issue means only that a bounded solver design is justified by accepted
evidence and that its frame is specified precisely enough for a later execution
gate.

It does **NOT** mean:

- HJB convergence — the accepted residual is still **`10.435094313164921`**, i.e.
  **`10435.09`×** the **unchanged** Bellman tolerance `1e-3`;
- that any new HJB iterate is accepted (none exists; no trajectory was run);
- that the design is validated — **no trial state was constructed or evaluated**;
- that a single route has been chosen (it has **not**);
- that the solver will converge globally;
- that KFE / stationary KFE is authorized;
- that economics / prices / grid / domain / tolerances may change.

## 14. Next gate (for the Owner / Reviewer — NOT decided here)

1. **Direction sub-choice.** Select family **A** (policy-frozen / regularized
   Newton) or family **B** (residual / Jacobi preconditioned correction) for the
   frozen frame, or authorize a bounded measurement that distinguishes them.
2. **Execution authorization.** Any actual execution of the frozen frame at `V_*`
   requires a separate execution Issue; this Issue authorizes none.

Stationary KFE remains **NOT AUTHORIZED**.
