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

The value-update-only dyadic safeguard DOES preserve the effective domain for every
accepted iterate (17 of 17 accepted iterates in-domain; raw-domain violations avoided
by damping every time), and gets materially past the accepted baseline exit (the
undamped run exits the domain at iteration 2). **But** it is not a viable convergence
route: the raw implicit update never decays (raw iterate change stays ≈ 8.3), the raw
update's boundary p_b at the critical state is ≈ −0.34 for every accepted V, lambda
collapses geometrically toward 2^-20, the accepted iterates are squeezed against the
domain wall (min accepted boundary p_b → 1.8e-12), and at iteration 18 no allowed step
exists. The raw iteration's fixed point lies OUTSIDE the positive-p_b effective domain,
so no damped value update can converge to it. Route reconsideration required.

Outcome A is not claimed (no convergence, no final Bellman validation). Outcome B is
not claimed (the safeguard does not merely stall short of convergence — it reaches the
gate's own terminal failure `INVARIANT_STEP_FAILURE`: no scientifically viable allowed
positive-domain update exists). Blocked is not applicable.

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

### 4.2 Failure detail (terminal event)

At the failing update request (iteration 18), built from the last accepted iterate:
- accepted iterate min boundary p_b = **1.8128990372393415e-12** (hugging the wall);
- raw update min boundary p_b = **−0.336924** at the worst state: **(a = 3.158,
  b = 6.842), z = 1, family F2** (hypotenuse boundary of the frozen triangle;
  grid indices (j, i) = (6, 24), node 201);
- the crossing lambda* = p_b_old / (p_b_old − p_b_raw) ≈ 1.8e-12 / 0.337 ≈ 5.4e-12
  is far below 2^-20, so no allowed dyadic step exists → `INVARIANT_STEP_FAILURE`.

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
- **The safeguard is NOT a viable CONVERGENCE route**: the raw implicit update's
  iterate change stays ≈ 8.30 from iteration 5 onward (it does not shrink), and the raw
  update's boundary p_b at the critical state stays ≈ −0.34 for every accepted V. The
  raw iteration's fixed point (T(V*) = V*) therefore lies OUTSIDE the positive-p_b
  effective domain of the frozen triangle.
- Because the fixed point is outside the domain, the damped iterates are driven against
  the domain wall: the min accepted boundary p_b falls monotonically 0.48 → 1.8e-12,
  lambda collapses geometrically 1/4 → 2^-20, and eventually no allowed positive-domain
  update exists → `INVARIANT_STEP_FAILURE` (no 2^-21, no adaptive epsilon, no alternate
  schedule — exactly per Issue #60 §6).
- The critical boundary state migrates during the run (initial exit F3 (13,13), z=0 →
  final wall F2 (6,24), z=1) — the domain wall is a global constraint, not a single
  fixed state.
- The failure is NOT an operator/conservation failure (max|Q·1| tiny throughout), NOT
  an expansion/artificial-binding failure (0/0 throughout), and NOT an F3 sector-algebra
  contradiction (the F3 algebra is Gate-2-verified). It is a property of the raw
  operator's fixed point relative to the effective domain of the frozen geometry.
- Conclusion: **effective-domain preserving value-update-only line search has no
  scientifically viable positive-domain update for this frozen central case — route
  reconsideration is required** (e.g. a future authorized gate would need to modify the
  raw operator/policy selection or the effective-domain treatment; no such modification
  is made or proposed here).

## 6. Accepted baseline (honored, not rediscovered)

Undamped central selected-Q run (Issue #58/#59 accepted fact): exits the boundary
effective domain at iteration 2, F3 (13,13), z = 0. Used only as the frozen baseline
reference; not re-derived by parameter experimentation.

## 7. Tests (all pass — 11/11)

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
- no KFE / stationary KFE / steady-state invocation (AST scan of imports and used
  names).

## 8. Reproducibility / run counts

- Commands:
  - `$env:PYTHONPATH = "D:\deep-learning-hank\src"`
  - `python -m pytest tests/test_dlh_5vl_invariant_domain_safeguard.py -q` (11/11 pass)
  - diagnostic driver (run twice + persist trace): the module's
    `run_safeguarded_central()` executed exactly twice; the two results and full traces
    are bit-identical (`deterministic_repeat_identical: true`); `DLH_5VL_ITERATION_TRACE.csv`
    written from the first run (17 rows).
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
