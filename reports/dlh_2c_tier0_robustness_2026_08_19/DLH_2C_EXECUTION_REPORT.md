# DLH-2C — Tier-0 Numerical Robustness / Grid-Boundary / Invariance — Execution Report

- Date: 2026-08-19
- Author: DSH (bounded Builder)
- Authority: GitHub Issue #7 — `DLH-2C: Tier-0 numerical robustness, grid-boundary and invariance validation`
- Accepted predecessor: Issue #6 / DLH-2B-R1, accepted commit `c562ce3a2743ac779123918e9aab5f37044b564a` (frozen dependency).
- Status: **FAIL-CLOSED candidate**. A robustness gate failed; the actual diagnostics are preserved below and no economics/grid standard/threshold was modified to force a PASS.
- Evidence class: **D2 machine-diagnostic evidence** (small one-region real HA/Aiyagari Tier-0 benchmark).

## 1. Terminal classification

`BLOCKED_DLH_2C_BOUNDARY_SENSITIVITY`

(The asset upper-bound sensitivity gate failed: `d_bound_K = 0.03411577346665587 > 0.005`. All other DLH-2C gates PASS; see below.)

## 2. Baselines and branch

- Fresh target `origin/main` SHA: `e0b443bcf01bdeca438a8779c38995dd2790dcc5`
- Dedicated branch: `dsh/issue-7-dlh-2c-tier0-robustness-2026-08-19`
- Candidate commit: single coherent commit at branch HEAD (2026-08-19, DSH); hash reported in completion response. Expected delta: exactly the 11 allowlisted paths, 0 behind / 1 ahead.

## 3. Exact changed paths (11-path allowlist)

1. `configs/dlh_2c_grid80_bound50_validation.toml`
2. `configs/dlh_2c_grid160_bound50_validation.toml`
3. `configs/dlh_2c_grid159_bound100_validation.toml`
4. `configs/dlh_2c_state_permutation_validation.toml`
5. `src/deep_learning_hank/diagnostics/tier0_robustness.py`
6. `tests/test_dlh_2c_grid_boundary.py`
7. `tests/test_dlh_2c_invariance.py`
8. `reports/dlh_2c_tier0_robustness_2026_08_19/DLH_2C_EXECUTION_REPORT.md`
9. `reports/dlh_2c_tier0_robustness_2026_08_19/DLH_2C_VARIANT_RESULTS.csv`
10. `reports/dlh_2c_tier0_robustness_2026_08_19/DLH_2C_RESIDUAL_SCAN.csv`
11. `reports/dlh_2c_tier0_robustness_2026_08_19/DLH_2C_FORBIDDEN_OPERATION_CHECK.md`

**No accepted DLH-2A/DLH-2B solver, economics, or test was modified** (frozen dependencies, verified byte-identical). No other path changed.

## 4. Environment and exact commands

- Python `3.11.9` (pre-existing); numpy `2.4.6`, scipy `1.17.1`, pytest `8.2.1` (pre-existing; zero installs; no environment mutation; no GPU).

**Command 1 — full repository test suite (exact command):**
```
$env:PYTHONPATH = "D:\deep-learning-hank\src"
python -m pytest tests -v
```
Result: **39 passed, 1 failed**. The single failure is `tests/test_dlh_2c_grid_boundary.py::test_upper_bound_sensitivity_gate` — the documented gate failure (`BLOCKED_DLH_2C_BOUNDARY_SENSITIVITY`, `d_bound_K = 0.03411577 > 0.005`). **DLH-2A + DLH-2B regression fully clean (32/32 PASS); no `BLOCKED_DLH_2C_REGRESSION`.**

**Command 2 — full robustness diagnostics capture (exact self-contained script):**
```
$env:PYTHONPATH = "D:\deep-learning-hank\src"
$script = @'
from pathlib import Path
import numpy as np
from deep_learning_hank.diagnostics.tier0_robustness import (
    VARIANT_CONFIGS, load_variants, grid_convergence_metrics,
    upper_bound_sensitivity_metrics, permutation_invariance_metrics,
    residual_scan, reproducibility_metrics)
v = load_variants()
for name in ("B40_50","G80_50","G160_50","W159_100","P40_50"):
    d = v[name][1]; f = d.result.final
    print(f"{name}: K*={f.capital:.10f} Y={f.output:.8f} w={f.wage:.8f} r={f.net_capital_return:.8e} C={f.mean_consumption:.8f} A={f.mean_assets:.8f} tr={f.transfer:.8f} gates={d.all_gates_pass} Lg={f.effective_labor_g:.10f}")
gc = grid_convergence_metrics(v)
print("GRID_CONVERGENCE", gc)
bs = upper_bound_sensitivity_metrics(v)
print("BOUNDARY_SENSITIVITY", bs)
pi = permutation_invariance_metrics(v)
print("PERMUTATION", pi)
scan = residual_scan(v["B40_50"][0], points=21)
print("RESIDUAL_SCAN intervals", scan["sign_changing_intervals"], "all_finite", scan["all_finite"], "gate", scan["gate"])
print("RESIDUAL_SCAN_POINTS")
for k, r in zip(scan["points"], scan["residuals"]):
    print(f"  {k:.6f},{r:.10e}")
rp = reproducibility_metrics(v)
print("REPRODUCIBILITY gate", rp["gate"])
for n, dd in rp["per_variant_max_abs_diffs"].items():
    print(f"  {n}: max={max(dd.values()):.3e} all={dd}")
'@
Set-Content -Path (Join-Path $env:TEMP "dlh2c_diag.py") -Value $script -Encoding UTF8
python (Join-Path $env:TEMP "dlh2c_diag.py")
```

## 5. Variants (all `VALIDATION_FIXTURE_NOT_CALIBRATION`)

| Variant | Grid | States | Purpose |
|---|---|---|---|
| B40_50 (accepted DLH-2B config, read-only) | 40 pts [0,50] | (0.5,1.5) | baseline |
| G80_50 | 80 pts [0,50] | (0.5,1.5) | refinement |
| G160_50 | 160 pts [0,50] | (0.5,1.5) | refinement |
| W159_100 | 159 pts [0,100] | (0.5,1.5) | spacing 100/158 = 50/79 matched to G80_50; upper-bound isolation |
| P40_50 | 40 pts [0,50] | (1.5,0.5) reversed | state-label permutation |

## 6. Per-variant numerical gates — **ALL PASS**

| Variant | K* | Y | w | r | C | A_hh | transfer | all gates |
|---|---|---|---|---|---|---|---|---|
| B40_50 | 27.3678234767 | 2.6988085539 | 1.8891659878 | 9.58373971e-3 | 2.1514520844 | 27.3678234767 | 0.2833748982 | True |
| G80_50 | 27.2438081362 | 2.6951338802 | 1.8865937166 | 9.67794226e-3 | 2.1502577204 | 27.2438081362 | 0.2829890582 | True |
| G160_50 | 27.1839654415 | 2.6933565143 | 1.8853495621 | 9.72366022e-3 | 2.1496771968 | 27.1839654415 | 0.2828024335 | True |
| W159_100 | 28.2060803850 | 2.7233460013 | 1.9063422017 | 8.96552051e-3 | 2.1592243875 | 28.2060803850 | 0.2859513294 | True |
| P40_50 | 27.3678234767 | 2.6988085539 | 1.8891659878 | 9.58373971e-3 | 2.1514520844 | 27.3678234767 | 0.2833748982 | True |

Every variant: root converged; root trace finite; capital residual ≤ 1e-7; all HJB/KFE/accounting/effective-labor gates pass; `L_g − L_bar = 0`.

## 7. Grid-refinement convergence — **PASS**

- `d40_80 = 0.004552056`; `d80_160 = 0.002201397`.
- `d80_160 (0.002201) <= d40_80 (0.004552) + 1e-12` ✓ (no worsening).
- `d80_160 (0.002201) <= 0.005` ✓.
- Relative differences 80→160 (observations; all < 0.5%, no reviewer flags): output `0.000659`, wage `0.000659`, net return `4.57e-05`, transfer `0.000187`, mean consumption `0.000270`, mean assets `0.002197`.

## 8. Asset upper-bound sensitivity — **FAIL (terminal blocker)**

Comparison `G80_50` vs `W159_100` (matched spacing 50/79 = 100/158):

- **`d_bound_K = |28.2060803850 − 27.2438081362| / max(1, 28.2060803850) = 0.03411577346665587 > 0.005` → `BLOCKED_DLH_2C_BOUNDARY_SENSITIVITY`.**
- Upper-boundary mass: `0.012470893` (bound 50) vs `8.909776e-05` (bound 100).
- Top-5%-of-grid mass: `0.033779958` (50) vs `0.000590981` (100).
- Mean assets / a_max: `0.544876` (50) vs `0.282061` (100).
- Relative differences 50→100 (observations): output `0.010468` (1.05%), wage `0.010468` (1.05%), net return `0.000712`, transfer `0.002962`, mean consumption `0.004170`.

Interpretation (diagnostic, not an excuse): with `a_max` doubled at matched spacing, the household wealth distribution spreads out (mean assets/a_max drops 0.54 → 0.28, upper-boundary/top-5% mass collapse), and equilibrium capital rises ~3.4%. The accepted benchmark is therefore **not robust to the asset upper bound within the required 0.5% criterion** under this `VALIDATION_FIXTURE_NOT_CALIBRATION`. Per Issue #7 this is a fail-closed result: no further `a_max` enlargement and no threshold redefinition were performed.

## 9. State-label permutation invariance — **PASS**

B40_50 vs P40_50 (state axis reversed back for arrays). Max absolute differences (all `<= 1e-10`, in fact ~machine precision): capital `6.04e-14`, output `1.78e-15`, wage `1.33e-15`, net return `4.86e-17`, transfer `2.22e-16`, value `1.63e-13`, consumption `1.18e-13`, drift `1.18e-13`, distribution mass `2.98e-15`, scalar diagnostics `5.65e-13`. **PASS.**

## 10. Bounded residual-shape / root-uniqueness diagnostic — **PASS**

21 equally spaced points on `[0.5, 45.0]` (full scan in `DLH_2C_RESIDUAL_SCAN.csv`): every capital/residual finite; **exactly one** adjacent sign-changing interval (between K=27.2 and K=29.425; no exact-zero samples). `BLOCKED_DLH_2C_MULTIPLE_BOUNDED_ROOT_INTERVALS` not triggered. Bounded numerical uniqueness diagnostic only (not a global proof).

## 11. Deterministic reproducibility — **PASS**

Each of G80_50, G160_50, W159_100, P40_50 run twice: max absolute repeat differences all **exactly 0.0** (≤ 1e-12) for K*, wage, net return, output, transfer, value, consumption, drift, distribution mass, scalar diagnostics.

## 12. Regression — **PASS**

Accepted DLH-2A (15) + DLH-2B (17) tests all continue to pass (32/32). No `BLOCKED_DLH_2C_REGRESSION`.

## 13. Test results (full repository suite)

- **39 passed, 1 failed.** The single failure is the boundary-sensitivity gate test (`d_bound_K = 0.03411577 > 0.005`) — the intended fail-closed evidence for `BLOCKED_DLH_2C_BOUNDARY_SENSITIVITY`. DLH-2A/2B regression: 32/32 PASS.

## 14. Engineering corrections / reruns

- None required beyond the initial run; no test-plumbing fix was needed. No economics, grid standard, bracket, or threshold was changed. One execution attempt (the suite) plus the diagnostics capture.

## 15. Forbidden-operation counters (all zero)

- W^L / W^K / old W / spatial / multi-region = 0 · SOE / RegionalAccounts = 0 · nominal/Fisher/NKPC/Taylor = 0 · shocks/AR(1) / transition = 0 · neural/RL = 0 · empirical data/calibration/regression = 0 · Matlab/Octave/Dynare = 0 · legacy Matlab reads = 0 · old source-repo access/mutation = 0 · Results/policy/novelty claims = 0 · governance changes = 0 · modification of accepted DLH-2A/2B modules or tests = 0 · PR / merge / Issue close / successor / self-accept = 0.

## 16. Evidence boundary

PASS/fail here is D2 machine-diagnostic evidence about the small one-region real HA/Aiyagari Tier-0 benchmark only. The boundary-sensitivity failure does not establish genuine-HANK, regional NSR-HANK, transition, policy, Results, or novelty.

## 17. Recommendation (suggestion only — no successor creation)

The boundary-sensitivity failure should be independently reviewed; possible scientific responses (Owner/ChatGPT decision, not Builder action) include widening the validation fixture's `a_max` rationale, adding a documented asset-holding upper-tail treatment, or re-scoping the robustness criterion. No successor Issue was created.
