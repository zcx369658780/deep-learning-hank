# DLH-5V-L Invariant-Domain Safeguarded Value-Update Line Search Report

**Issue:** #60 — "DLH-5V-L: Test invariant-domain safeguarded value-update line search on the central selected-Q HJB case"
**Gate type:** `SCIENTIFIC_NUMERICAL_DIAGNOSTIC__EFFECTIVE_DOMAIN_PRESERVING_VALUE_UPDATE`
**Owner / Reviewer route decision:** `APPROVE_CONTROLLED_INVARIANT_DOMAIN_SAFEGUARDED_VALUE_UPDATE_DIAGNOSTIC`
**Authority marker:** `DLH_5VL_INVARIANT_DOMAIN_SAFEGUARD_DIAGNOSTIC_AUTHORIZED`
**Activation comments:** `5649259224` (activation), `5649265447` (FINAL current sync)
**Branch:** `dsh/issue-60-dlh-5vl-invariant-domain-safeguard-2026-09-13`
**Base / merge-base:** fresh `origin/main` `6e493733a845f7847da9d2777a58ae8703901fbb` (fresh-fetched; unchanged)
**Household oracle blob (read-only, unchanged on live main):** `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`
**Selected-Q source (read-only, unchanged):** blob `7ea342ccbe15d852b90743b14bb4b02977c2d78b`
**Date:** 2026-09-13

> Note on the oracle blob string: the activation instruction transcribes the oracle
> blob as `76ae5b149993a7edeeb337f1b02b3fe33c51e` (40 hex chars, missing one digit
> compared with the accepted blob). The blob verified on live `origin/main` is the
> accepted one from Issues #58/#59: `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`.
> That verified blob is byte-identical on the branch and is unchanged by this gate.

---

## 1. Terminal (exactly ONE)

> **C — `DLH_5VL_INVARIANT_DOMAIN_SAFEGUARD__NO_VIABLE_POSITIVE_EFFECTIVE_DOMAIN_UPDATE__ROUTE_RECONSIDERATION_REQUIRED`**

**Safeguarded central run outcome: `INVARIANT_STEP_FAILURE`** — after 17 accepted
in-domain iterations, no allowed dyadic lambda in {2^-k, k = 0..20} keeps all boundary
effective-domain p_b evidence above the 1e-12 acceptance margin.

Interpretation (trajectory-bounded, per Micro-Rev Reviewer `5649480400`):

- Along the authorized safeguarded trajectory, the raw update remains materially
  nonzero and points outside the effective domain as the accepted iterate approaches
  the domain wall.
- The tested value-update-only safeguard route does not provide a viable convergent
  path on the frozen central case.

The value-update-only dyadic safeguard DOES preserve the effective domain for every
accepted iterate (17 of 17 accepted iterates in-domain; raw-domain violations avoided
by damping every time), and gets materially past the accepted baseline exit (the
undamped run exits the domain at iteration 2). **But** on the tested trajectory the raw
update never decays (raw iterate change stays ≈ 8.3), the accepted lambda collapses
geometrically toward 2^-20, the accepted iterates are squeezed against the domain wall
(min accepted boundary p_b → 1.8e-12), and at iteration 18 the continuous step needed
merely to stay above the acceptance margin is λ_margin = 7.51e-7 < 2^-20 — below the
smallest authorized dyadic step, so no authorized safeguard step exists.

**Scope of the claim:** this diagnostic establishes the behavior along the ONE
authorized safeguarded trajectory only. It does NOT establish uniqueness of the raw
fixed point, absence of another positive-domain fixed point, absence of another basin
of attraction, absence of a continuation path, or global nonexistence of an admissible
fixed point (see §5.1).

Outcome A is not claimed (no convergence, no final Bellman validation). Outcome B is
not claimed (the safeguard reaches the gate's own terminal failure
`INVARIANT_STEP_FAILURE`: no scientifically viable allowed positive-domain update
exists on the tested safeguarded trajectory). Blocked is not applicable.

> **Micro-Rev record:** this report incorporates the bounded corrections required by
> Reviewer comment `5649480400` (fixed-point overclaim replaced by the
> trajectory-bounded statement above; same-state margin crossing
> `lambda_margin = (p_old - PB_MARGIN)/(p_old - p_raw)` at the binding state) and
> Reviewer correction `5649693645` (terminal-diagnostic metadata semantics: GLOBAL
> old/raw minima and their states are recorded separately from the margin-binding
> same-state diagnostic; `final_min_boundary_pb` / `raw_min_boundary_pb` /
> `worst_raw_state` mean the GLOBAL raw minimum and its state; the binding-state
> same-state pair lives only inside `terminal_crossing_diagnostics`). No underlying
> economics or solver behavior changed; no accepted numerical evidence was reopened.

---

## 2. Scientific question and frozen design

ONE question: can the accepted selected-Q HJB keep every accepted value iterate inside
the required positive boundary-liquid-marginal effective domain by safeguarding ONLY
the value-update acceptance step?

### Frozen central case (Issue #60 §2 — all unchanged)

| item | value |
|---|---|
| geometry | m = 1, W_max = 10, b_min = −2, a_max = 10 |
| prices | r_a = 0.07, r_b = 0.02, w = 1.00, borrowing_rate_gap = 0.0 |
| household | rho = 0.02, gamma_c = 2.0, phi = 5.0, chi_0 = 0.1, chi_1 = 2.0, a_bar = 1e-6 |
| labor/tax | tau = 0.15, migration_cost = 0, labor_weight = 1 |
| z / switch | z = [0.8, 1.3]; switch = [[−1/3, 1/3], [1/3, −1/3]] |
| numerics | delta = 1000, tolerance_iter = 1e-7, tolerance_Bellman = 1e-3, max_iterations = 1000 |
| search | n_c = 9, n_d = 9, bracket expansion x4, max 3 |

### Safeguard rule (Issue #60 §4–§6, implemented literally)

- raw update: `V_raw = T(V_old)` via the ACCEPTED solver's implicit update (accepted
  operator + utility + `(1/delta + rho)I − Q` solve) — the accepted production step,
  used read-only;
- only the acceptance of the raw update may be damped:
  `V_trial(lambda) = V_old + lambda*(V_raw − V_old)`;
- lambda candidates EXACTLY {2^-k, k = 0..20} (descending); choose the LARGEST lambda
  with ALL boundary effective-domain p_b evidence > 1e-12 (p_b = declared backward
  liquid marginal vb_b over boundary non-F0 nodes; non-finite evidence never accepted);
- the 1e-12 margin is ONLY an iterate-acceptance numerical margin — it never replaces,
  floors or clips p_b and never enters the consumption FOC, labor FOC, transfer choice
  or Bellman score;
- no allowed step → `INVARIANT_STEP_FAILURE` (no 2^-21, no adaptive epsilon, no
  alternate margin/schedule);
- fixed-point integrity: the fixed-point target for every accepted lambda > 0 remains
  `V_raw = V_old`; no candidate/rate/Q/utility/destination/sector modification, no
  policy clipping, no pseudo-time adaptation, no continuation (no theorem claimed).

---

## 3. Execution (Issue #60 §10 — exactly as authorized)

1. ONE safeguarded central-case run — **outcome `INVARIANT_STEP_FAILURE` after 17
   accepted iterations**;
2. ONE deterministic repeat of the SAME safeguarded run — **bit-identical** (same
   outcome, iterations, statistic, full trace equality).

No price sweep, no alternate lambda sequence, no alternate p_b margin, no alternate
delta/tolerance, no alternate W_max or m.

## 4. Safeguarded run results

### 4.1 Summary

| metric | value |
|---|---|
| outcome | `INVARIANT_STEP_FAILURE` |
| total accepted iterations | 17 |
| min lambda (accepted) | 2^-20 = 9.5367431640625e-07 |
| median lambda (accepted) | 2^-10 = 9.765625e-04 |
| iterations requiring backtracking | 17 of 17 (every raw update violated the domain) |
| raw-domain violations avoided | 17 (each time the largest admissible dyadic step was taken) |
| minimum accepted boundary p_b | 1.8128990372393415e-12 (still > 1e-12 margin) |
| max\|Q·1\| over accepted iterates | 5.94e-15 → 7.76e-11 (Q conservative throughout) |
| expansions / artificial bindings | 0 / 0 over all accepted iterations |
| iterate convergence | NOT reached (accepted statistic at exit 7.9e-6, raw statistic 8.30) |
| final Bellman residual | NOT reached (no iterate convergence → no final validation manufactured) |
| failing iteration | 18th update request: no allowed dyadic lambda keeps the domain |

### 4.2 Failure detail (terminal event; corrected per Micro-Rev `5649480400` and
Micro-Rev `5649693645`)

At the failing update request (iteration 18), built from the last accepted iterate
(V_17, min accepted boundary p_b = 1.8128990372393415e-12). Two DISTINCT terminal
diagnostics are recorded (semantics separated after Micro-Rev `5649693645`):

**A. GLOBAL minima (over ALL boundary states, each with its attaining state):**

| metric | value | state |
|---|---|---|
| global old min p_b | 1.8128990372393415e-12 | F3, (j, i) = (16, 8), z = 1, node 367 (the accepted-iterate wall) |
| global raw min p_b | **−0.33692370571864877** | F2, (j, i) = (6, 24), z = 1, node 201 (a = 3.158, b = 6.842) — the most-negative raw boundary p_b anywhere |

**B. MARGIN-BINDING SAME-STATE diagnostic (the state that blocks every authorized
dyadic step — it achieves the minimum continuous margin-crossing lambda):**

| metric | value |
|---|---|
| binding state | node 367, family **F3**, (j, i) = (16, 8), z = 1 → (a = 8.421, b = 0.947) |
| binding p_old (accepted iterate, same state) | 1.8128990372393415e-12 |
| binding p_raw (raw update, same state) | −1.0825070292850926e-06 |
| PB_MARGIN (frozen) | 1e-12 |
| **lambda_margin_crossing** = (p_old − PB_MARGIN)/(p_old − p_raw) | **7.50939858929181e-07** |
| lambda_zero_crossing = p_old/(p_old − p_raw) | 1.674719842086034e-06 |
| minimum authorized dyadic lambda | 2^-20 = 9.5367431640625e-07 |
| margin crossing below smallest authorized step? | **YES** (7.51e-7 < 9.54e-7) |

**The two concepts are different and are never mixed.** The binding state matters
because it yields the smallest allowed continuous margin-crossing lambda (the reason
no authorized step exists). The global raw minimum matters because it is the
most-negative raw boundary derivative anywhere (−0.337 at F2 (6,24) z=1); its state
differs from the binding state. In the result object: `final_min_boundary_pb`,
`raw_min_boundary_pb` and `worst_raw_state` always mean the GLOBAL raw minimum and its
state; `global_old_min_pb`/`global_old_min_state` mean the GLOBAL old minimum and its
state; the binding-state same-state pair lives ONLY inside
`terminal_crossing_diagnostics` (`p_old`, `p_raw`, `binding_state`).

The continuous step needed merely to remain above the acceptance margin is
λ_margin ≈ 7.51e-7, which is below the smallest authorized dyadic step
2^-20 ≈ 9.54e-7: the trial at λ = 2^-20 already dips below the margin at the binding
state (p_trial ≈ 1.81e-12 + 9.54e-7·(−1.08e-6) ≈ 0.78e-12 < 1e-12), so **no authorized
safeguard step exists** → `INVARIANT_STEP_FAILURE`.

> Note on the earlier estimate: the pre-Micro-Rev report cited "λ* ≈ 5.4e-12", computed
> as p_old/(p_old − p_raw) with p_old = 1.81e-12 (min accepted p_b, at F3 (16,8) z=1)
> and p_raw = −0.337 (min raw p_b, at a DIFFERENT state F2 (6,24) z=1). Those two
> minima live at different states, so that number conflated two states and was also the
> zero-crossing rather than the margin-crossing. The corrected SAME-STATE margin
> crossing at the binding state is λ_margin = 7.51e-7, still below 2^-20, so the
> terminal is unchanged. This is exactly why the margin formula (not the zero formula)
> is the relevant criterion: the zero crossing (1.67e-6) lies ABOVE 2^-20, so the
> 2^-20 step stays above zero but dips below the margin — only the margin crossing
> reveals the no-authorized-step condition.

These crossing quantities are DIAGNOSTIC ONLY: they never choose a step, never add
lambda candidates, never authorize lambda below 2^-20, and never alter p_b / candidate
scoring / Q / controls. The actual safeguard remains exactly the authorized dyadic
search {2^-k, k = 0..20} taking the largest feasible lambda.

### 4.3 Iteration trace (persisted in DLH_5VL_ITERATION_TRACE.csv — 17 rows)

Compact per-iteration record (see CSV for full precision): iteration, raw
max|V_raw − V_old|, accepted max|V_new − V_old|, lambda, backtrack count, min
boundary p_b(V_old), min boundary p_b(V_raw), min boundary p_b(V_new),
lambda=1-would-violate flag, max|Q·1|, optimizer expansion count, artificial binding
count, sector/family-change count. Representative rows:

| iter | raw stat | accepted stat | lambda | bt | min p_b(old) | min p_b(raw) | min p_b(new) | Q·1 |
|---|---|---|---|---|---|---|---|---|
| 1 | 19.58 | 4.894 | 1/4 | 2 | 0.4808 | −0.6820 | 0.2358 | 5.9e-15 |
| 2 | 13.98 | 3.494 | 1/4 | 2 | 0.2358 | −0.7017 | 0.01357 | 4.2e-15 |
| 3 | 9.70 | 0.606 | 1/16 | 4 | 0.01357 | −0.5093 | 0.00659 | 3.6e-15 |
| 6 | 8.50 | 0.133 | 1/64 | 6 | 3.0e-4 | −0.3163 | 6.4e-5 | 9.5e-15 |
| 9 | 8.31 | 0.0081 | 1/1024 | 10 | 9.2e-7 | −0.3536 | 1.6e-7 | 1.5e-13 |
| 12 | 8.30 | 2.5e-4 | 1/32768 | 15 | 1.5e-9 | −0.3377 | 5.2e-10 | 4.9e-12 |
| 15 | 8.30 | 6.3e-5 | 2^-17 | 17 | 5.1e-11 | −0.3370 | 7.3e-12 | 1.9e-11 |
| 17 | 8.30 | 7.9e-6 | 2^-20 | 20 | 3.2e-12 | −0.3369 | 1.8e-12 | 7.8e-11 |

Policy/family dynamics: sector changes only in the early iterations (7, 17, 2, 4, 5, 1,
1 then 0) — the policy family pattern reconfigures initially and then freezes while the
value update is damped against the domain wall. Q is conservative (max|Q·1| ≤ 7.8e-11)
and no artificial bracket binding occurs in any accepted iteration.

## 5. Scientific interpretation

- **The safeguard works as a domain PRESERVATION mechanism**: all 17 accepted iterates
  are inside the effective domain (every boundary p_b > 1e-12), and every raw-domain
  violation is avoided by taking the largest admissible dyadic step. This is a strictly
  better domain trajectory than the accepted baseline, whose undamped run exits the
  effective domain at iteration 2 (F3 (13,13), z = 0).
- **The tested value-update-only safeguard is NOT a viable CONVERGENCE route on the
  frozen central case**: along the authorized safeguarded trajectory, the raw implicit
  update's iterate change stays ≈ 8.30 from iteration 5 onward (it does not shrink), and
  the raw update's boundary p_b at the critical state points outside the effective
  domain for every accepted V.
- Along the trajectory the damped iterates are driven against the domain wall: the min
  accepted boundary p_b falls monotonically 0.48 → 1.8e-12, lambda collapses
  geometrically 1/4 → 2^-20, and eventually no allowed positive-domain update exists →
  `INVARIANT_STEP_FAILURE` (no 2^-21, no adaptive epsilon, no alternate schedule —
  exactly per Issue #60 §6). At the terminal request the continuous step needed merely
  to remain above the acceptance margin is λ_margin = 7.51e-7 < 2^-20, so no
  AUTHORIZED safeguard step exists.
- The critical boundary state migrates during the run (initial exit F3 (13,13), z=0 →
  terminal binding state F3 (16,8), z=1; the raw update's most negative p_b at the
  separate hypotenuse state F2 (6,24), z=1) — the domain wall is a global constraint,
  not a single fixed state.
- The failure is NOT an operator/conservation failure (max|Q·1| tiny throughout), NOT
  an expansion/artificial-binding failure (0/0 throughout), and NOT an F3 sector-algebra
  contradiction (the F3 algebra is Gate-2-verified). It is a property of the tested
  trajectory relative to the effective domain of the frozen geometry.

### 5.1 Scope of the claim (corrected per Micro-Rev `5649480400`)

This diagnostic establishes:

- along the authorized safeguarded trajectory;
- as accepted V approaches the effective-domain wall;
- the raw update remains materially nonzero;
- the raw update direction continues to point outside the effective domain;
- the authorized dyadic acceptance step collapses;
- eventually no authorized dyadic step exists.

It does NOT establish:

- uniqueness of the raw fixed point;
- absence of another positive-domain fixed point;
- absence of another basin of attraction;
- absence of a continuation path;
- global nonexistence of an admissible fixed point.

Terminal C is retained because it only requires that the AUTHORIZED deterministic
safeguard route reaches a state with no allowed viable dyadic step — it does not
require proving where every raw fixed point lies. In particular, the claim that "the
raw operator's fixed point lies outside the effective domain", "no positive-domain
fixed point exists", or "the HJB solution itself lies outside the domain" is NOT made
and is NOT supported by this diagnostic.

- Conclusion: **the tested value-update-only invariant-domain safeguard succeeds as a
  short-run DOMAIN-PRESERVATION device but fails as an authorized convergence route on
  the frozen central case** — no scientifically viable allowed positive-domain update
  exists on the tested safeguarded trajectory; route reconsideration is required (e.g.
  a future authorized gate would need to modify the raw operator/policy selection or
  the effective-domain treatment; no such modification is made or proposed here).

## 6. Accepted baseline (honored, not rediscovered)

Undamped central selected-Q run (Issue #58/#59 accepted fact): exits the boundary
effective domain at iteration 2, F3 (13,13), z = 0. Used only as the frozen baseline
reference; not re-derived by parameter experimentation.

## 7. Tests (all pass — 19/19, incl. Micro-Rev additions)

`tests/test_dlh_5vl_invariant_domain_safeguard.py`:
- frozen central configuration exact (household params, inputs r_a=0.07/r_b=0.02/tau,
  wages/labor/migration, z, switch, m=1, W_max=10, b_min=−2, a_max=10, delta=1000,
  tolerance_iter=1e-7, tolerance_bellman=1e-3, max_iterations=1000, n_c=n_d=9, expand
  x4 max 3);
- lambda candidates exactly {2^-k, k = 0..20}, descending; p_b margin exactly 1e-12;
- largest feasible lambda selected (independent recomputation, synthetic raw updates);
- no p_b clipping/flooring (static AST scan + exact-min check on real derivatives);
- synthetic raw update violating the domain is damped when a valid step exists;
- no valid step → `INVARIANT_STEP_FAILURE`;
- any PASS requires the final Bellman residual criterion (validation semantics);
- deterministic complete central-case repeat (full-trace equality);
- Micro-Rev `5649480400` additions: lambda_margin_crossing formula uses PB_MARGIN,
  not zero; lambda_zero_crossing separately named; undefined-case guards; terminal
  diagnostic from the real run satisfies p_old > PB_MARGIN > p_raw at the binding
  state, lambda_margin_crossing recomputed exactly, and lambda_margin_crossing < 2^-20
  (with the zero crossing NOT below 2^-20 — the margin, not zero, is the binding
  criterion); crossing diagnostics never change step selection (trace lambdas all
  inside the authorized dyadic set; `safeguard_step` does not reference the
  diagnostics); PB_MARGIN and the authorized lambda set unchanged; deterministic
  Terminal-C reproduction; no global fixed-point assertion in the scientific tests;
- Micro-Rev `5649693645` additions: GLOBAL raw minimum ≈ −0.336924 pinned at F2
  (6,24) z=1; GLOBAL old minimum 1.8128990372393415e-12 pinned at F3 (16,8) z=1;
  binding-state same-state pair pinned separately (F3 (16,8) z=1, binding p_raw ≈
  −1.08e-6); global raw state ≠ binding state; field-name semantics pinned
  (`final_min_boundary_pb` / `raw_min_boundary_pb` / `worst_raw_state` = GLOBAL raw
  minimum and its state; `old_min_boundary_pb` = GLOBAL old minimum; binding-state
  quantities only inside `terminal_crossing_diagnostics` with `binding_state`, no
  `worst_state` overload);
- no KFE / stationary KFE / steady-state invocation (AST scan of imports and used
  names).

## 8. Reproducibility / run counts

- Commands:
  - `$env:PYTHONPATH = "D:\deep-learning-hank\src"`
  - `python -m pytest tests/test_dlh_5vl_invariant_domain_safeguard.py -q` (19/19 pass)
  - diagnostic driver (run twice + persist trace): the module's
    `run_safeguarded_central()` executed exactly twice; the two results and full traces
    are bit-identical (`deterministic_repeat_identical: true`); `DLH_5VL_ITERATION_TRACE.csv`
    written from the first run (17 rows). Re-executed after each bounded Micro-Rev
    diagnostic/metadata addition; the safeguarded trajectory and trace rows are
    unchanged (the additions are reporting-only metadata), the iteration-trace CSV
    remains byte-identical to the accepted version, and the deterministic repeat
    remains bit-identical.
- Run counts: 2 safeguarded executions; each = 17 accepted iterations + 1 failing
  update request (each iteration: 1 accepted raw update + 1 trace operator build;
  ~6–7 s per run). No other scientific configuration.

## 9. Forbidden-operation check (all respected)

No oracle mutation (blob unchanged); no selected-Q source mutation (blob unchanged); no
household/price/grid/domain change; no W_max/m/resolution/delta/tolerance/
initialization change; no control-bracket/search-grid change; no hard control bounds; no
p_b clipping/flooring; Bellman residual never used to choose lambda; no alternate
damping schedule; no pseudo-time adaptation; no continuation; no policy clipping; no
price sweeps; no KFE; no stationary KFE; no `solve_household_steady_state`; no SCC /
global-Q; no GE / multi-region / neural; no PR / merge / close / successor / self-accept.

## 10. Deliverables (exactly four NEW paths)

1. `src/deep_learning_hank/two_asset/invariant_domain_safeguarded_hjb.py`
2. `tests/test_dlh_5vl_invariant_domain_safeguard.py`
3. `reports/dlh_5vl_invariant_domain_safeguard_2026_09_13/DLH_5VL_INVARIANT_DOMAIN_SAFEGUARD_REPORT.md` (this file)
4. `reports/dlh_5vl_invariant_domain_safeguard_2026_09_13/DLH_5VL_ITERATION_TRACE.csv`

No `__init__.py`, no oracle, no selected-Q source, no Issue #59 diagnostic module, no
accepted existing test, no governance file from the Builder branch, and no fifth tracked
file. Remote verified equal to local after push.
