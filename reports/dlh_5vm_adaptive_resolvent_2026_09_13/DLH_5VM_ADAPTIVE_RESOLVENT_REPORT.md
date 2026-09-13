# DLH-5V-M — Adaptive Pseudo-Time / Resolvent Safeguard Diagnostic — Report

Issue #61 / DLH-5V-M — `SCIENTIFIC_NUMERICAL_DIAGNOSTIC__ADAPTIVE_PSEUDO_TIME_RESOLVENT_EFFECTIVE_DOMAIN`

Branch: `dsh/issue-61-dlh-5vm-adaptive-resolvent-2026-09-13`

Authority: initial activation `5650244803`; final activation refresh `5650488809`; live `main` at activation `3fdc858453766823d25e1b7d5e8ca1485d08744c`.

## 1. Terminal (exactly ONE)

> **C — `DLH_5VM_ADAPTIVE_RESOLVENT__NO_VIABLE_EFFECTIVE_DOMAIN_RESOLVENT_STEP__ROUTE_RECONSIDERATION_REQUIRED`**

**Adaptive-resolvent central run outcome: `RESOLVENT_STEP_FAILURE`** — after 2
accepted in-domain iterations, the third update request has **no allowed delta on
the deterministic ladder {1000·2^-k, k = 0..20}** that keeps every boundary
effective-domain p_b above the 1e-12 acceptance margin.

Interpretation (trajectory-bounded):

- Adapting the resolvent parameter INSIDE the implicit solve does preserve the
  effective domain for the two accepted iterates (2/2 in-domain; min accepted
  boundary p_b = 0.00985) — including one full iteration more than the undamped
  baseline, which exits at iteration 2.
- At the third update request, NO authorized delta on the deterministic ladder is
  feasible (each of the 21 ladder trials leaves the effective domain somewhere).
  At the binding wall state F3 (13,13) z=1 the accepted iterate's p_b is still
  0.00985 (far from the wall), yet even the SMALLEST authorized delta trial
  (1000·2^-20 ≈ 9.54e-4) already drives that state's p_b to −0.00208, below the
  margin; the recorded worst states of larger-delta trials differ (the delta=1000
  reference trial's worst state is F3 (17,7), z=1).
- Direct cross-route comparison (accepted iterations before the terminal event):
  2 accepted iterations on this adaptive-resolvent route vs 17 under the
  Issue #60 value-damping route on the same frozen central case. No cross-route
  per-unit-parameter "steepness" ratio is claimed (delta and lambda are different
  update parameters with different scales).
- Hence the adaptive-pseudo-time/resolvent route does NOT provide a viable
  positive-domain iteration route on the frozen central case; the tested
  deterministic delta ladder is exhausted at the third update request.

Scope of the claim: this diagnostic establishes the behavior along the ONE
authorized adaptive-resolvent trajectory only. It does NOT establish uniqueness of
the HJB fixed point, absence of another positive-domain fixed point, absence of
another basin, absence of a continuation/homotopy path, or global nonexistence of an
admissible fixed point (continuation/homotopy is not authorized by Issue #61).

Outcome A is not claimed (no convergence, no final Bellman validation). Outcome B is
not claimed (the run reaches the gate's own terminal failure `RESOLVENT_STEP_FAILURE`
at the third update request — no viable authorized resolvent step exists; it does not
stall short of convergence, it cannot even take a next in-domain step). Blocked is
not applicable.

> **R1 repair record (Reviewer `5651311810`):** bounded engineering/evidence repair
> on the same branch, no scientific reconfiguration and no change to the Terminal-C
> interpretation. (1) `min_boundary_pb_state` made FAIL-CLOSED: any required (non-F0)
> boundary p_b that is non-finite (NaN/Inf) deterministically fails the domain check
> (returns +inf at that state) instead of being silently ignored by the min
> comparison; regression tests added. (2) Report wording tightened: the evidence
> supports "no ladder delta is feasible" and "the smallest-delta limiting failure is
> at F3 (13,13), z=1"; it does NOT claim all 21 deltas fail at the same state (the
> delta=1000 reference trial's worst state is F3 (17,7), z=1). (3) The cross-route
> "steepness/sensitivity per-unit-delta vs per-unit-lambda" ratio is removed; the
> direct empirical comparison (2 accepted iterations here vs 17 under Issue #60
> value damping) is retained. The frozen central run + deterministic repeat were
> re-executed to confirm the scientific result is unchanged (bit-identical).

## 2. Authority and scope record

- Fresh live `main` before execution: `3fdc858453766823d25e1b7d5e8ca1485d08744c` (unchanged during execution).
- Issue #61 OPEN; initial activation `5650244803`; final activation refresh `5650488809`; governance blocker record `5650249190`.
- Household oracle blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e` — read-only, unchanged.
- Selected-Q blob `7ea342ccbe15d852b90743b14bb4b02977c2d78b` — read-only, unchanged.
- Stationary KFE remains NOT AUTHORIZED.

## 3. Frozen central case and authorized mechanism

Exactly as Issue #61 §3–§4: `m=1`, `W_max=10`, `b_min=-2`, `a_max=10`; `r_a=0.07`,
`r_b=0.02`, `w=1.00`, borrowing gap `0`; `rho=0.02`, `gamma_c=2`, `phi=5`,
`chi_0=0.1`, `chi_1=2`, `a_bar=1e-6`; `tau=0.15`, migration cost `0`, labor weight
`1`; `z=[0.8,1.3]` with the accepted switch matrix; `tolerance_iter=1e-7`,
`tolerance_Bellman=1e-3`, `max_iterations=1000`; `n_c=n_d=9`, bracket expansion x4
max 3; initialization exactly per the accepted Issue #58 central conventions.

Mechanism per accepted iterate `V_old`:

1. build the accepted selected policy, utility and conservative backward `Q` from
   `V_old` **exactly once** (`build_operator_and_u`);
2. deterministic delta sequence `delta_k = 1000·2^-k`, `k = 0..20`, descending;
3. for each candidate delta solve the resolvent system
   `[(1/delta + rho)I - Q] V_delta = u + V_old/delta` (SAME `(Q, u)` for all
   trials — pinned by test);
4. choose the **largest** delta whose `V_trial` keeps all required boundary
   `p_b > 1e-12`;
5. accept that `V_trial` directly — **no additional value damping** (the Issue #60
   line search is NOT layered on top; pinned by static test).

At a fixed point `V_delta = V_old = V` any positive `delta` cancels and the target
remains `rho V = u(V) + Q(V)V`: this diagnostic changes the numerical path only, not
household economics or the target HJB equation.

## 4. Execution and per-iteration trace

Exactly ONE adaptive-resolvent run + ONE deterministic repeat (no other scientific
configuration). Persisted trace: `DLH_5VM_RESOLVENT_TRACE.csv` (header + 2 rows).

| iter | selected delta | k | bt | accepted max\|V−V_old\| | ref1000 max\|V−V_old\| | ref1000 min p_b | min p_b(V_old) | min p_b(V_new) | delta=1000 violates? | max\|Q·1\| | exp | ab | sector chg |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.0305176 (=1000·2^-15) | 15 | 15 | 0.3198 | 19.58 | −0.682 | 0.4808 | 0.06025 | true | 5.9e-15 | 0 | 0 | 0 |
| 2 | 0.00381470 (=1000·2^-18) | 18 | 18 | 0.03986 | 19.16 | −0.731 | 0.06025 | 0.009854 | true | 5.9e-15 | 0 | 0 | 7 |

- Accepted iterations: **2** (both in-domain; min accepted boundary p_b = **0.009853744163134845**).
- Selected delta: min = 1000·2^-18 ≈ **0.0038147**; median ≈ **0.01717**; both accepted iterations used `delta < 1000` (reduced-delta iterations = 2).
- delta=1000 reference violated the domain on **both** accepted iterations (aggressive reference min p_b = −0.682 / −0.731).
- Q is conservative throughout (max\|Q·1\| = 5.94e-15); optimizer expansions 0; artificial bindings 0; policy/family reconfiguration: the family pattern of the iteration-2 selected policy differs from iteration 1 at 7 of the 782 states, then the run terminates (the reconfiguration is the early-policy-adjustment phase before the wall event, consistent with the accepted #59/#60 runs).
- Convergence criterion `max|V_new−V_old| < 1e-7` NOT reached (smallest accepted step was 0.0399 at iteration 2); no final Bellman validation applies (no convergence).

### 4.1 Terminal failure detail (third update request, from accepted iterate 2)

| metric | value |
|---|---|
| outcome | `RESOLVENT_STEP_FAILURE` |
| global old min p_b (accepted iterate) | 0.009853744163134845 |
| global old min state | node 332, family **F3**, (j, i) = (13, 13), z = 1 |
| smallest authorized delta | 1000·2^-20 ≈ 9.5367431640625e-4 |
| min p_b of the smallest-delta trial | **−0.002078969753188379** (< 1e-12 margin) |
| smallest-delta trial worst state | node 332, family **F3**, (13, 13), z = 1 (SAME wall state) |
| delta=1000 trial min p_b (aggressive reference) | −0.7117516766123627 at F3 (17, 7), z = 1 |
| any allowed delta viable? | **NO** — all 21 ladder deltas are infeasible; the recorded worst state differs across ladder points (only the smallest-delta trial's worst state is F3 (13,13) z=1) |

At the binding wall state F3 (13,13) z=1, the accepted iterate's p_b is 0.00985
(far from the 1e-12 margin), yet the smallest authorized delta trial (9.54e-4)
already drives that state's p_b to −0.00208 — the continuous delta-crossing
(where the trial would stay above the margin) lies below 1000·2^-20, i.e.
outside the authorized ladder. This is the recorded limiting failure of the
smallest authorized delta; larger-delta trials have worst states that may differ
(for example the delta=1000 reference trial's worst state is F3 (17,7), z=1).
No authorized delta exists.

## 5. Scientific interpretation (trajectory-bounded)

- **The adaptive resolvent preserves the effective domain for every accepted
  iterate** (2/2 in-domain), and extends the undamped baseline path by one full
  iteration (baseline exits at iteration 2; here iteration 2 is accepted in-domain
  and the failure occurs at the third request).
- **The tested adaptive-pseudo-time route is NOT a viable convergence route on the
  frozen central case**: the accepted delta collapses by a factor 8 per iteration
  (k 15 → 18), and at the third update request every authorized delta is
  infeasible — the smallest-delta limiting failure is at wall state F3 (13,13)
  z=1 (accepted p_b there 0.00985, smallest-delta trial p_b −0.00208).
- **Direct cross-route observation**: this route accepted 2 in-domain iterations
  before the terminal event, vs 17 under the Issue #60 value-damping route on the
  same frozen central case. No per-unit-parameter "steepness/sensitivity" ratio
  between delta and lambda is claimed (they are different update parameters with
  different scales).
- The wall state F3 (13,13) is the same family/position that blocks the undamped
  baseline (iteration-2 exit) — the F3 sector boundary of the frozen triangle is
  the domain constraint, independent of the numerical route.
- The failure is NOT an operator/conservation failure (max\|Q·1\| ≈ 6e-15), NOT an
  optimizer expansion or artificial-binding failure (0/0), and NOT a
  sector-algebra contradiction (F3 algebra is Gate-2-verified).

### 5.1 Comparison with accepted baselines (frozen, not rediscovered)

| route | accepted in-domain iterations | terminal event |
|---|---|---|
| undamped delta=1000 (Issue #58/#59) | 1 | exits domain at iteration 2, F3 (13,13) |
| value-update damping (Issue #60, Terminal C) | 17 | lambda 2^-20 squeezed against the wall, then no dyadic step |
| adaptive pseudo-time/resolvent (THIS diagnostic) | 2 | delta 1000·2^-20 still violates at the wall; `RESOLVENT_STEP_FAILURE` |

### 5.2 Scope of the claim (does NOT establish)

This diagnostic establishes: along the authorized adaptive-resolvent trajectory, the
raw resolvent direction remains materially nonzero and points outside the effective
domain at the wall state; the authorized delta ladder is exhausted at the third
update request; the tested resolvent-only route provides no viable in-domain next
iterate. It does NOT establish: HJB fixed-point uniqueness; absence of another
positive-domain fixed point; absence of another basin of attraction; absence of a
continuation/homotopy path; global nonexistence of an admissible fixed point.

## 6. Accepted baselines honored (not reopened)

Issue #58/#59 accepted facts (initial V0 min boundary p_b = +0.48076562156308306;
undamped exit at iteration 2, F3 (13,13), z=0) and Issue #60 accepted facts
(value-damping preserves the domain for 17 accepted iterations; no authorized dyadic
step at iteration 18) are used only as frozen references.

## 7. Tests (all pass — 14/14, incl. R1 regression tests)

`tests/test_dlh_5vm_adaptive_resolvent.py`:
- frozen central configuration exact (household params, inputs r_a=0.07/r_b=0.02/
  tau/wages/migration/labor, z, switch, m=1, W_max=10, b_min=−2, a_max=10,
  delta=1000, tolerances, max_iterations=1000, n_c=n_d=9, expand x4 max 3,
  row_sum_tolerance=1e-9);
- delta ladder exactly {1000·2^-k, k=0..20}, descending, 21 distinct values;
- largest feasible delta selected deterministically (synthetic case: delta=1000
  violates, delta=500 feasible → k=1 selected, identical on repeat);
- the same `(Q, u)` reused across ALL delta trials of one accepted iterate
  (runtime pin: one operator build per attempted iteration; every trial solve uses
  the Q/u objects handed to the selection call);
- no derivative clipping/flooring (static: no np.clip/maximum/minimum/floor; no
  `pb` reassignment from min/max);
- no value damping / no Issue #60 layering (static: no `safeguard_step`, no
  `invariant_domain_safeguarded_hjb`, no `V_raw`, no `LAMBDA_MIN_EXP`);
- no feasible delta → `RESOLVENT_STEP_FAILURE` (synthetic);
- PASS requires the final Bellman residual criterion (validation semantics: a
  material residual is never a PASS);
- deterministic full repeat (bit-identical outcome/trace/failure detail);
- real frozen central run reproduces Terminal C (RESOLVENT_STEP_FAILURE, 2
  iterations, k=15 then k=18, smallest-delta limiting failure at F3 (13,13) z=1,
  smallest-delta trial p_b < 0);
- R1 fail-closed regression: when earlier required boundary p_b values are finite
  and a later required state is NaN, `min_boundary_pb_state` returns +inf at that
  state and `_domain_ok` returns False (NaN is never silently ignored); the
  all-finite path is unchanged;
- no KFE / stationary KFE / steady-state invocation (AST name scan);
- margin is acceptance-only (PB_MARGIN never enters derivative or Bellman-scoring
  paths).

## 8. Reproducibility / run counts

- Commands:
  - `$env:PYTHONPATH = "D:\deep-learning-hank\src"`
  - `python -m pytest tests/test_dlh_5vm_adaptive_resolvent.py -q` (14/14 pass, ~2.5 s)
  - diagnostic driver: `run_adaptive_resolvent_central()` executed exactly twice;
    the two results and full traces are bit-identical
    (`deterministic_repeat_identical: true`); `DLH_5VM_RESOLVENT_TRACE.csv` written
    from the first run (2 rows). Re-executed once more after the R1 fail-closed
    repair to confirm the scientific result is unchanged (bit-identical outcome,
    trace and failure detail; NaN evidence never occurs on the frozen central
    trajectory).
- Run counts: 2 adaptive-resolvent executions; each = 2 accepted iterations + 1
  failing update request (each iteration: 1 operator build + (k+2) resolvent solves,
  k = 15, 18, then 22+2 on the failing request; ~0.5 s per run). No other
  scientific configuration.

## 9. Forbidden-operation check (all respected)

No oracle/selected-Q mutation (blobs unchanged); no household/price/grid/domain/
tolerance/initialization change; no control-bracket/search-grid change; no hard
control bounds; no p_b clipping/flooring; the 1e-12 margin is acceptance-only; no
Bellman-residual-driven delta selection; no delta outside {1000·2^-k, k=0..20}; no
value damping (Issue #60 line search not layered); no pseudo-time adaptation beyond
the declared ladder; no continuation/homotopy; no KFE / stationary KFE /
`solve_household_steady_state`; no SCC / global-Q; no GE / multi-region / neural /
nominal / calibration / policy / welfare / Results; no PR / merge / close /
successor / self-accept.

## 10. Deliverables (exactly four NEW paths)

1. `src/deep_learning_hank/two_asset/adaptive_resolvent_hjb.py`
2. `tests/test_dlh_5vm_adaptive_resolvent.py`
3. `reports/dlh_5vm_adaptive_resolvent_2026_09_13/DLH_5VM_ADAPTIVE_RESOLVENT_REPORT.md` (this file)
4. `reports/dlh_5vm_adaptive_resolvent_2026_09_13/DLH_5VM_RESOLVENT_TRACE.csv`
