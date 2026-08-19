# DLH-2B — Single-Region Tier-0 HA/Aiyagari Steady-State GE — Execution Report

- Date: 2026-08-19
- Author: DSH (bounded Builder)
- Authority: GitHub Issue #6 — `DLH-2B: Single-region Tier-0 HA/Aiyagari steady-state general equilibrium`
- Accepted predecessor: Issue #5 / DLH-2A-R1, accepted commit `76b5882a63d8ade18d50098373b7c735eb2c4ca4` (frozen regression dependency).
- Status: CANDIDATE. Acceptance requires fresh-GitHub independent review (ChatGPT).
- Evidence class: **D2 machine-diagnostic evidence for a small one-region real HA/Aiyagari steady-state benchmark only.**

## 1. Terminal classification

`DLH_2B_TIER0_SINGLE_REGION_STEADY_STATE_GE_READY_FOR_GPT_REVIEW`

## 2. Baselines and branch

- Fresh target `origin/main` SHA: `65fcfd8cd2812603b11c448391f5e4dcb7c1ea7b`
- Dedicated branch: `dsh/issue-6-dlh-2b-tier0-steady-state-ge-2026-08-19`
- Candidate commit: single coherent commit at branch HEAD (2026-08-19, DSH); hash reported in completion response. Expected delta: exactly the 13 allowlisted paths, 0 behind / 1 ahead.

## 3. Exact changed paths (13-path allowlist)

1. `configs/dlh_2b_tier0_steady_state_validation.toml`
2. `src/deep_learning_hank/config.py` (SteadyStateConfig added; FixedPriceConfig untouched)
3. `src/deep_learning_hank/solvers/__init__.py` (docstring only)
4. `src/deep_learning_hank/solvers/steady_state.py`
5. `src/deep_learning_hank/diagnostics/__init__.py` (docstring only)
6. `src/deep_learning_hank/diagnostics/tier0_steady_state.py`
7. `tests/test_dlh_2b_equilibrium.py`
8. `tests/test_dlh_2b_accounting.py`
9. `tests/test_dlh_2b_reproducibility.py`
10. `reports/dlh_2b_tier0_steady_state_2026_08_19/DLH_2B_EXECUTION_REPORT.md`
11. `reports/dlh_2b_tier0_steady_state_2026_08_19/DLH_2B_DIAGNOSTICS.csv`
12. `reports/dlh_2b_tier0_steady_state_2026_08_19/DLH_2B_ROOT_TRACE.csv`
13. `reports/dlh_2b_tier0_steady_state_2026_08_19/DLH_2B_FORBIDDEN_OPERATION_CHECK.md`

**Accepted DLH-2A frozen modules were NOT modified** (`household_hjb.py`, `distribution_kfe.py`, `economics/firm.py`, `economics/fiscal.py`, `economics/preferences.py`, `economics/grids.py`, `diagnostics/tier0_fixed_price.py`, DLH-2A tests). No other path modified.

## 4. Environment and exact commands

- Python `3.11.9` (pre-existing); numpy `2.4.6`, scipy `1.17.1`, pytest `8.2.1` (pre-existing; zero installs; no environment mutation; no GPU).

Commands executed:
1. Full repository test suite (twice — first run, then after one test-tooling fix):
```
$env:PYTHONPATH = "D:\deep-learning-hank\src"
python -m pytest tests -v
```
   - Attempt 1: 29 passed, 1 failed (test-tooling bug in the new `test_no_regional_w_soe_nominal_objects`: it sub-string-matched the word "regional" against the module docstring's "Single-region"). Fixed the test to check forbidden imports/identifiers instead of prose substrings (engineering correction authority; DLH-2A untouched).
   - Attempt 2 (final): **30 passed, 0 failed** (DLH-2A 15 + DLH-2B 15).
2. Equilibrium diagnostics capture (exact script executed; outputs in `DLH_2B_DIAGNOSTICS.csv`):
```
$env:PYTHONPATH = "D:\deep-learning-hank\src"
python (Join-Path $env:TEMP "dlh2b_diag.py")
```
   (full script text: loads `configs/dlh_2b_tier0_steady_state_validation.toml`, runs `run_tier0_steady_state` twice, prints all scalars/gates/repeat diffs; see diagnostics CSV.)
3. Root-trace dump (exact command):
```
python -c "from pathlib import Path; from deep_learning_hank.config import SteadyStateConfig; from deep_learning_hank.diagnostics.tier0_steady_state import run_tier0_steady_state; d = run_tier0_steady_state(SteadyStateConfig.from_toml(Path('configs/dlh_2b_tier0_steady_state_validation.toml'))); [print(f'{i},{k},{r}') for i,(k,r) in enumerate(d.result.root_trace)]"
```

## 5. Test counts (final)

- DLH-2A regression (accepted suite, unchanged): 15 passed (economics 7 + HJB/KFE 7 + reproducibility 1).
- DLH-2B new tests: 15 passed (accounting 6 + equilibrium 8 + reproducibility 1).
- **Repository total: 30 passed, 0 failed, 0 skipped.**

## 6. Fixture — VALIDATION_FIXTURE_NOT_CALIBRATION

`configs/dlh_2b_tier0_steady_state_validation.toml` (header explicitly labeled): asset grid `[0,50]`/40 pts; states `(0.5,1.5)`; intensities `0.25/0.25`; `rho_hh=0.01`; `gamma=2.0`; `tau_l=0.15`; firm/root `A=1.0`, `alpha_k=0.30`, `delta=0.02`, `G=0.0`; capital bracket `[0.5,45.0]`; scan bounds `[0.1,49.0]`, 98 points; outer capital tolerance `1e-7`; outer max iterations `200`. Numerical validation fixture only — never empirical calibration.

## 7. Effective-labor construction

- `L_bar = sum_z pi_z * z` from the idiosyncratic CTMC stationary law (`pi` solves `pi @ G = 0`, normalized). For the symmetric fixture: `pi = (0.5, 0.5)`, `L_bar = 1.0` — **computed, not hard-coded**.
- At the final equilibrium KFE: `L_g = sum_{z,a} g(z,a) * z = 1.0`; `|L_g - L_bar| = 0.0 <= 1e-8` ✓.

## 8. Root/bracket evidence

- Primary bracket `[0.5, 45.0]`: endpoint residuals `R_K(0.5) = -49.5`, `R_K(45.0) = +35.365079662198205` — finite, opposite signs (sign change present). **No bounded scan was required** (`bracket_from_scan = False`).
- Root method: `scipy.optimize.brentq` (xtol=1e-10, rtol=1e-14, maxiter=200), converged in **11 total evaluations** (2 endpoint pre-checks + 9 solver evaluations). Full trace in `DLH_2B_ROOT_TRACE.csv`.
- `K* = 27.367823476711713`; capital residual `R_K(K*) = 1.0466294497746276e-11 <= 1e-7` ✓; all evaluations finite.

## 9. Equilibrium objects (fixture)

| Object | Value |
|---|---|
| K* | 27.367823476711713 |
| Y (two-factor Cobb-Douglas) | 2.6988085539374342 |
| wage w | 1.889165987756204 |
| net capital return r (= household asset return) | 0.009583739710619838 (positive, finite) |
| transfer (tau_l·w·L_bar − G) | 0.2833748981634306 |
| mean assets A_hh | 27.367823476701247 |
| mean consumption C | 2.1514520844030995 |

## 10. Household/KFE diagnostics at equilibrium (thresholds frozen)

- HJB converged (8 iterations); true residual `1.3058058412340756e-08 <= 1e-7` ✓; min consumption `1.0862704429598173 > 0` ✓; lower boundary drift `0.0 >= -1e-12` ✓; upper boundary drift `0.0 <= 1e-12` ✓; generator row-sum max abs `1.1102230246251565e-16 <= 1e-12` ✓; **literal** off-diagonal minimum `0.0 >= -1e-14` ✓; NaN/Inf `0` ✓.
- KFE: mass error `0.0 <= 1e-10` ✓; stationarity residual `2.905661822261152e-17 <= 1e-8` ✓; minimum mass `1.0123318235136522e-03 >= -1e-12` ✓; negative-mass count `0` ✓; NaN/Inf `0` ✓; state marginals `[0.5, 0.5]` (error `0.0`) ✓.

## 11. Independent accounting diagnostics (computed, never zeroed)

| Residual | Value | Threshold | PASS |
|---|---|---|---|
| R_goods = Y − C − δ·K − G | 1.0047518372857667e-13 | <= 1e-7 | ✓ |
| R_hh_budget = C − [(1−τ_l)·w·L_g + r·A_hh + transfer] | 0.0 | <= 1e-7 | ✓ |
| mean_drift = Σ g·drift | −2.2941717969793274e-16 | <= 1e-7 | ✓ |
| fiscal residual | 0.0 | <= 1e-12 | ✓ |

Positivity: Y, w, C, K* all > 0; r finite and positive. All accounting gates PASS.

## 12. Deterministic reproducibility

Full steady-state pipeline run twice; max absolute repeat differences (threshold `1e-12`) — all exactly `0.0`: K* `0.0`, wage `0.0`, net capital return `0.0`, output `0.0`, transfer `0.0`, value `0.0`, consumption `0.0`, drift `0.0`, distribution mass `0.0`, scalar diagnostics `0.0`. PASS.

## 13. Engineering corrections / reruns

- One test-tooling fix in the new `tests/test_dlh_2b_equilibrium.py::test_no_regional_w_soe_nominal_objects` (prose sub-string match → import/identifier check). No economic/implementation change; no threshold relaxed; DLH-2A code untouched.
- Test attempt history: attempt 1 = 29 passed/1 failed (tooling); attempt 2 (final) = 30 passed.

## 14. Forbidden-operation counters (all zero)

- W^L / W^K / old W / spatial / multi-region = 0 · SOE factor = 0 · RegionalAccounts = 0 · nominal/Fisher/NKPC/Taylor = 0 · shocks/AR(1) = 0 · transition = 0 · neural/RL = 0 · empirical data/calibration/regression = 0 · Matlab/Octave/Dynare = 0 · legacy Matlab reads = 0 · old source-repo mutation = 0 · Results/policy/novelty claims = 0 · governance changes = 0 · PR / merge / Issue close / successor / self-accept = 0.

## 15. Evidence boundary

Passing DLH-2B supports **D2 machine-diagnostic evidence for a small one-region real HA/Aiyagari steady-state benchmark only**. It does NOT establish calibration, genuine-HANK validity, multi-region NSR-HANK validity, transition dynamics, policy/Results eligibility, or novelty.

## 16. Recommendation for next validation subgate (suggestion only — no successor creation)

Next DLH-2 validation step after independent review: extend to the minimal genuine single-region HANK nominal layer (DLH-3) or proceed per the Master Roadmap; no successor Issue created by the Builder.
