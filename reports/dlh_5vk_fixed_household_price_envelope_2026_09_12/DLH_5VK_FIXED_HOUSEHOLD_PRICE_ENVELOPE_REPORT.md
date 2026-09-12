# DLH-5V-K Fixed-Household External-Price Convergence Envelope Report

**Issue:** #59 — "DLH-5V-K: Diagnose fixed-household external-price convergence envelope before HJB stabilization"
**Gate type:** `SCIENTIFIC_DIAGNOSTIC__FIXED_HOUSEHOLD_EXTERNAL_PRICE_CONVERGENCE_ENVELOPE`
**Owner decision:** `APPROVE_FIXED_HOUSEHOLD_EXTERNAL_PRICE_ENVELOPE_DIAGNOSTIC_BEFORE_STABILIZATION`
**Authority marker:** `DLH_5VK_FIXED_HOUSEHOLD_PRICE_ENVELOPE_DIAGNOSTIC_AUTHORIZED`
**Activation comments:** `5646298166` (activation), `5646305575` (FINAL authoritative refresh)
**Branch:** `dsh/issue-59-dlh-5vk-fixed-household-price-envelope-2026-09-12`
**Base / merge-base:** fresh `origin/main` `8d67855dd3caa362bd0aab16132f90798be0b15c` (fresh-fetched; unchanged)
**Household oracle blob (read-only, unchanged):** `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`
**Selected-Q source (accepted Issue #58, read-only, unchanged):** blob `7ea342ccbe15d852b90743b14bb4b02977c2d78b`
**Date:** 2026-09-12

---

## 1. Terminal (exactly ONE)

> **B — `DLH_5VK_FIXED_HOUSEHOLD_PRICE_ENVELOPE_MAPPED__PRICE_REGION_MATTERS_BUT_SELECTED_Q_EFFECTIVE_DOMAIN_GAP_REMAINS`**

Scientific classification: **H2 — mixed evidence.**

The Owner hypothesis is materially supported in the FIXED LEGACY ORACLE: a reproducible external-price
convergence envelope is mapped on the frozen rectangle (a ∈ [0,10], b ∈ [-2,5], b_max = 5 frozen).
Central price cases converge with finite, bounded values; sufficiently extreme external prices
materially deteriorate or fail (limit-cycle-like behavior / finite nonconvergence), and this is
reproducible and deterministic. **However**, the current accepted selected-Q solver exits its accepted
effective domain at iteration 2 at ALL THREE sentinels, INCLUDING the central/safe-price sentinel
r_a = 0.07. Therefore external-price discipline alone does NOT explain the selected-Q failure; the
selected-Q effective-domain gap is a separate numerical invariant-domain issue. Both external-price
discipline AND numerical invariant-domain issues matter.

Outcome A (H1) is NOT claimed: the selected-Q solver fails at the central safe-price reference, so the
external-price region does not fully explain HJB convergence behavior of the current solver.
Outcome C (H3) is NOT claimed: the legacy oracle's price pattern IS organized (central band
converges, low/high extreme fail), clearly supporting a price envelope within the legacy solver.
Terminal Blocked is not applicable (no authority or dependency conflict).

---

## 2. Scientific question and frozen design

Holding fixed the household HJB equations, preference/adjustment parameters, asset grid/domain,
initialization, and numerical tolerances, the diagnostic tests whether HJB convergence depends
materially on the external equilibrium inputs (r_a, r_b, w). Only bounded predeclared cases vary.

### Frozen household parameters (VALIDATION_FIXTURE_NOT_CALIBRATION — not relabeled as calibration authority)

| parameter | value |
|---|---|
| rho | 0.02 |
| gamma_c | 2.0 |
| phi | 5.0 |
| chi_0 | 0.1 |
| chi_1 | 2.0 |
| a_bar | 1e-6 |
| tau | 0.15 |
| migration_cost | 0.0 |
| labor_weight | 1.0 |
| z | [0.8, 1.3] |
| switch | [[-1/3, 1/3], [1/3, -1/3]] |

### Diagnostic A — legacy accepted oracle (HJB only)

- Solver: `solve_matlab_faithful_hjb` (accepted MATLAB-faithful HJB; read-only).
- FIXED domain for every legacy run: a = linspace(0,10,20), b = linspace(-2,5,20); **b_max = 5 IS FROZEN**.
- Frozen numerics/initialization for every legacy case: delta = 1000.0, convergence_tolerance = 1e-7,
  max_iterations = 1000, drift_tolerance = 1e-12; deterministic brentq labor0 + utility-based V0
  initialization; transfer_income = 0.0; borrowing-gap convention gap = 0.01 (accepted fixture
  convention) held constant for every case.

### Diagnostic B — current selected-Q solver (read-only)

- Solver: `BoundaryHJBSolver` (accepted Issue #58; read-only).
- FIXED geometry: m = 1, W_max = 10.
- FIXED r_b = 0.02, w = 1.00; household params, delta = 1000, tolerances (iter 1e-7, Bellman 1e-3),
  max_iterations = 1000, search resolution (n_c = n_d = 9), bracket semantics (x4, max 3),
  initialization construction EXACTLY as frozen in accepted Issue #58 diagnostic conventions.
- EXACTLY three r_a sentinels: {0.07, 0.10, 0.13}. The effective-domain guard is never weakened.

---

## 3. Diagnostic A results — legacy oracle on the frozen rectangle (b_max = 5)

### 3.1 Predeclared sparse case table (9 cases; complete records in DLH_5VK_PRICE_CASES.csv)

| case (r_a, r_b, w) | classification | iterations | final statistic | V min | V max | min V_b evidence | non-positive V_b share |
|---|---|---|---|---|---|---|---|
| (0.05, 0.02, 1.00) | finite_nonconvergence | 1000 | 3.669 | -68.34 | -47.79 | -1.768 | 0.058 |
| (0.07, 0.02, 1.00) | **converged** | 332 | 1.27e-9 | -68.34 | -35.49 | -0.050 | 0.102 |
| (0.09, 0.02, 1.00) | **converged** | 98 | 4.12e-8 | -68.34 | -15.50 | -0.707 | 0.320 |
| (0.11, 0.02, 1.00) | **converged** | 152 | 2.21e-8 | -68.34 | 0.83 | -0.993 | 0.429 |
| (0.13, 0.02, 1.00) | limit_cycle_like | 1000 | 0.0273 | -68.34 | -16.61 | -0.726 | 0.275 |
| (0.07, 0.015, 1.00) | finite_nonconvergence | 1000 | 9.928 | -68.35 | -35.26 | -5.461 | 0.311 |
| (0.07, 0.025, 1.00) | finite_nonconvergence | 1000 | 1.009 | -68.11 | -36.40 | -0.238 | 0.299 |
| (0.07, 0.02, 0.80) | **converged** | 307 | 4.11e-10 | -83.64 | -35.98 | -0.465 | 0.165 |
| (0.07, 0.02, 1.20) | limit_cycle_like | 1000 | 0.0094 | -58.03 | -31.51 | -0.236 | 0.111 |

Failure-mode distinctions (per case): "finite_nonconvergence" = value stays finite but the iterate
change never falls below 1e-7 in 1000 iterations (with a bounded 8-iteration probe showing the
statistic is NOT reproducing itself — i.e. not a clean cycle); "limit_cycle_like" = nonconverged with
the bounded probe reproducing the same iterate-change statistic (direct oscillation evidence);
"converged" = statistic < 1e-7. No case produced a non-finite value or an explicit solver exception.

Policy diagnostics (complete per-case columns in the CSV): e.g. central anchor (0.07, 0.02, 1.00)
consumption ∈ [0.639, 1000.0] with 6.1% of states at/near the accepted v_b-floor FOC cap
(c >= 990; v_b floor 1e-6 ⇒ c cap 1000), labor ∈ [0.0584, …], d (= transfer) and (mu_a, mu_b)
ranges in the CSV. The convergence verdict is NOT an economic-quality verdict; policy diagnostics are
reported separately (e.g. the converged fixed points still carry 10-43% non-positive V_b evidence).

### 3.2 r_a transition localization (conditional diagnostic bisection; 4 of 4 authorized midpoints)

The predeclared r_a line (r_b = 0.02, w = 1.00) contains clear PASS (0.07, 0.09, 0.11) and clear FAIL
(0.05, 0.13), so bisection was authorized. Deterministic widest-gap midpoint rule; exactly four
evaluations consumed (the cap):

| r_a | classification | iterations | final statistic |
|---|---|---|---|
| 0.060 | limit_cycle_like | 1000 | 2.69 |
| 0.120 | **converged** | 283 | 2.94e-9 |
| 0.065 | limit_cycle_like | 1000 | 28.85 |
| 0.125 | limit_cycle_like | 1000 | 0.0410 |

### 3.3 Legacy convergence envelope (r_b = 0.02, w = 1.00)

- **PASS band:** r_a ∈ [0.07, 0.12] (converged: 0.07, 0.09, 0.11, 0.12).
- **FAIL regions:** r_a ∈ [0.05, 0.065] (low-rate; finite nonconvergence at 0.05, limit cycles at
  0.06/0.065) and r_a ∈ [0.125, 0.13] (high-rate; limit cycles).
- The envelope is **non-monotone** in r_a: both the low-rate and the high-rate extremes fail, with an
  interior convergent band. This is a reproducible deterministic property of the frozen household on
  the frozen rectangle (not a pass/fail tuning artifact).
- r_b sensitivity at r_a = 0.07: r_b = 0.015 and r_b = 0.025 both FAIL (finite nonconvergence) —
  the central (r_a, w) values alone do not guarantee convergence; r_b matters.
- wage sensitivity at r_a = 0.07, r_b = 0.02: w = 0.80 converges, w = 1.20 limit-cycles — w matters.

---

## 4. Diagnostic B results — selected-Q sentinels on the frozen triangle (m=1, W_max=10)

Fixed r_b = 0.02, w = 1.00. Exactly three sentinels. Complete records in DLH_5VK_PRICE_CASES.csv.

| r_a | outcome | first failure iteration | family | (j, i) | z | recorded p_b | iter-1 min boundary p_b | iter-1 max\|Q·1\| | iter-1 expansions | iter-1 artificial bindings |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.07 | DERIVATIVE_EFFECTIVE_DOMAIN_FAILURE | 2 | F3 | (13, 13) | 0 | -0.2840 | +0.4808 | 5.94e-15 | 0 | 0 |
| 0.10 | DERIVATIVE_EFFECTIVE_DOMAIN_FAILURE | 2 | F3 | (13, 13) | 0 | -0.3935 | +0.4199 | 7.11e-15 | 0 | 0 |
| 0.13 | DERIVATIVE_EFFECTIVE_DOMAIN_FAILURE | 2 | F3 | (13, 13) | 0 | -0.4200 | +0.3791 | 1.18e-14 | 0 | 0 |

For every sentinel: iteration 1 is fully inside the effective domain (min boundary p_b > 0;
max|Q·1| ≈ 1e-14; zero expansions; zero artificial bindings; V0 finite), and iteration 2 deterministically
exits the effective domain: the iteration-1 value iterate has non-positive backward liquid marginal
evidence p_b at the same boundary state F3 (13, 13), z = 0, so the accepted effective-domain guard
raises DERIVATIVE_EFFECTIVE_DOMAIN_FAILURE before candidate/bracket search (no bracket expansion
disguises the exit). p_b did NOT remain positive through all executed iterations in any sentinel
(exited at iteration 2). The guard is never weakened or bypassed.

**Decisive fact:** the selected-Q solver fails at the central Owner SAFE-REGION reference
r_a = 0.07 — the very price the legacy oracle handles comfortably (converged in 332 iterations).

---

## 5. Cross-solver interpretation warning (respected)

The two diagnostics use DIFFERENT FIXED geometries: legacy = rectangle (a ∈ [0,10], b ∈ [-2,5],
b_max = 5); selected-Q = triangle (m = 1, W_max = 10). This report does NOT claim "geometry causes
the difference" on the basis of differing convergence. The comparison answers only: does the
external-price region materially matter WITHIN each frozen solver/domain? (Yes for the legacy
rectangle; the selected-Q triangle fails even at the central price, so the price region is not the
binding explanation for the selected-Q exit.) A causal geometry comparison would require a separate
future gate and is NOT performed here.

## 6. H1 / H2 / H3 scientific classification — H2 (mixed evidence)

- H1 (external-price envelope materially supported, GE-envelope route ready) — NOT chosen: the
  legacy envelope is real, but the current selected-Q solver still exits its effective domain at the
  central/safe-price sentinel, so external prices alone do not explain the current solver's
  behavior; the GE-envelope route is NOT ready.
- **H2 (mixed evidence) — CHOSEN:** external prices clearly matter in the fixed legacy oracle
  (reproducible non-monotone envelope: central band r_a ∈ [0.07, 0.12] converges; low/high extremes
  and off-anchor r_b / high-wage fail), AND the current selected-Q solver still exits its accepted
  effective domain at central/safe-price sentinels. Both external-price discipline AND numerical
  invariant-domain issues matter.
- H3 (expected pattern not supported) — NOT chosen: the legacy results DO organize into a
  central-pass / extreme-fail pattern (with the nuance that the pass region is an interior band, not
  a monotone low-rate region).

## 7. Scientific interpretation

- The Owner hypothesis is supported as a LEGACY-solver phenomenon: fixed-household HJB convergence on
  the accepted rectangle is materially conditioned by (r_a, r_b, w); a reproducible convergence
  envelope exists, and its shape is non-monotone in r_a (fail both at low r_a ≈ 0.05-0.065 and at
  high r_a ≈ 0.125-0.13).
- The accepted legacy oracle's own converged fixed points can carry substantial non-positive V_b
  evidence (10-43% of states at the convergent r_a values; e.g. 0.09: 32%, 0.11: 43%, 0.12: 47%)
  with bounded values, and the 0.12 fixed point has V max = +307 (a large positive value at the
  domain corner). V_b positivity is therefore NOT a requirement for legacy rectangle convergence.
  The selected-Q solver's boundary optimizer contract (accepted Issue #57 Rev-2) requires positive
  effective liquid marginal evidence, so the same phenomenon surfaces there as
  DERIVATIVE_EFFECTIVE_DOMAIN_FAILURE on the production iterate — a numerical invariant-domain issue
  of the current scheme, independent of the price region (it occurs at the safe price too).
- The failure does NOT disprove the household HJB or the finite-domain geometry, and it is NOT an
  F3 sector-algebra contradiction (the F3 algebra itself is Gate-2-verified).
- This Issue is BEFORE stabilization: no damping, line search, continuation, pseudo-time adaptation,
  or other stabilization was implemented or used. A controlled effective-domain-preserving
  stabilization route remains a FUTURE decision (not authorized here).

## 8. Reproducibility / determinism / run counts

- Commands:
  - `$env:PYTHONPATH = "D:\deep-learning-hank\src"`
  - targeted tests: `python -m pytest tests/test_dlh_5vk_fixed_household_price_envelope.py -q` (all pass)
  - diagnostic execution: the module's `all_case_rows()` + `write_csv(...)` produced
    `DLH_5VK_PRICE_CASES.csv` (16 rows: 9 predeclared legacy + 4 authorized bisection midpoints + 3
    selected-Q sentinels).
- Run counts: 13 legacy executions (each <= 1000 HJB iterations, plus a bounded <= 8-iteration probe
  for nonconverged cases) and 3 selected-Q executions (each <= 2 iterations before the deterministic
  effective-domain failure). Total legacy compute ~25 minutes.
- Determinism: repeated runs produce bit-identical records (verified by
  `test_deterministic_rerun_central_legacy` and `test_deterministic_rerun_selected_q`; also
  independently re-executed the full 16-case set with identical outcomes).
- Deterministic midpoint rule for bisection: widest-gap adjacent PASS/FAIL pair, ties broken by
  lowest r_a; capped at 4 evaluations.

## 9. Tests (all pass)

`tests/test_dlh_5vk_fixed_household_price_envelope.py`:
- frozen legacy grid: b_max EXACTLY 5, b in [-2, 5], a in [0, 10], 20 points;
- fixed household parameters (VALIDATION_FIXTURE_NOT_CALIBRATION) and fixed numerics;
- exact predeclared 9-case list (r_a line, r_b sentinels, wage sentinels; central anchor present);
- no accidental b_max / W_max / m / resolution variation (run signatures have no such parameters);
- diagnostic output schema (union of the CSV header keys);
- deterministic rerun for the central legacy case and a selected-Q sentinel;
- selected-Q sentinel list exactly {0.07, 0.10, 0.13};
- no KFE / stationary KFE / steady-state invocation (AST scan: no such API references or call sites).

## 10. Forbidden-operation check (all respected)

No oracle mutation; no selected-Q mutation; no HJB-equation change; no change to gamma_c / phi / chi /
rho / tau; no b_max variation (b_max = 5 frozen); no W_max variation (W_max = 10 frozen); no m
variation; no grid-resolution variation; no delta/tolerance/initialization tuning between cases; no
hard economic bounds on c/l/d; no V_b clipping; no damping / line search / continuation / pseudo-time
adaptation; no KFE; no stationary KFE; no `solve_household_steady_state`; no stationary distribution
g; no stationary C/L/A/B used as evidence; no SCC/global-Q; no production Wmax/resolution study; no
GE / regional / neural work; no PR / merge / close / successor / self-accept. The only variation is
the predeclared sparse (r_a, r_b, w) design plus the conditionally authorized four r_a midpoints.

## 11. Deliverables (exactly four NEW paths)

1. `src/deep_learning_hank/two_asset/fixed_household_price_envelope_diagnostic.py`
2. `tests/test_dlh_5vk_fixed_household_price_envelope.py`
3. `reports/dlh_5vk_fixed_household_price_envelope_2026_09_12/DLH_5VK_FIXED_HOUSEHOLD_PRICE_ENVELOPE_REPORT.md` (this file)
4. `reports/dlh_5vk_fixed_household_price_envelope_2026_09_12/DLH_5VK_PRICE_CASES.csv`

No `__init__.py`, no oracle, no selected-Q source, no accepted existing test, no governance file from
the Builder branch, and no fifth tracked file. Remote verified equal to local after push.
