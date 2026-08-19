# DLH-2C-B1 — Tier-0 Asset-Domain Adequacy / Upper-Tail Convergence — Execution Report

- Date: 2026-08-19
- Author: DSH (bounded Builder)
- Authority: GitHub Issue #8 — `DLH-2C-B1: Tier-0 asset-domain adequacy and upper-tail convergence validation`
- Accepted predecessor: Issue #7 / DLH-2C fail-closed, accepted commit `583e352b3ba37d25ebb7d8f468b5fd9f4f5eb5d3` (`DLH_2C_BOUNDARY_SENSITIVITY_BLOCKED_ACCEPTED`; frozen dependency).
- Status: **FAIL-CLOSED candidate**. A robustness gate failed; the actual diagnostics are preserved below and no economics, grid standard, domain criterion, or threshold was modified to force a PASS.
- Evidence class: **D2 machine-diagnostic evidence** (small one-region real HA/Aiyagari Tier-0 benchmark).

## 1. Terminal classification

`BLOCKED_DLH_2C_B1_WIDE_DOMAIN_GRID_CONVERGENCE`

(The wide-domain grid-refinement gate failed: `d_grid_200 = 0.004952190294576287 > d_grid_100 + 1e-12` with `d_grid_100 = 0.0049404311829274825`. All other DLH-2C-B1 gates PASS; see below.)

## 2. Baselines and branch

- Fresh target `origin/main` SHA: `d3e6ae80fe2a004e7a1c175d6a398aa7b9a56021`
- Dedicated branch: `dsh/issue-8-dlh-2c-b1-asset-domain-2026-08-19`
- Candidate commit: single coherent commit at branch HEAD (2026-08-19, DSH); hash reported in completion response. Expected delta: exactly the 10 allowlisted paths, 0 behind / 1 ahead.

## 3. Exact changed paths (10-path allowlist)

1. `configs/dlh_2c_b1_bound150_coarse_validation.toml` (C150: 238 pts [0,150], h=150/237=50/79)
2. `configs/dlh_2c_b1_bound200_coarse_validation.toml` (C200: 317 pts [0,200], h=200/316=50/79)
3. `configs/dlh_2c_b1_bound100_fine_validation.toml` (F100: 317 pts [0,100], h=100/316=25/79)
4. `configs/dlh_2c_b1_bound200_fine_validation.toml` (F200: 633 pts [0,200], h=200/632=25/79)
5. `src/deep_learning_hank/diagnostics/tier0_asset_domain.py`
6. `tests/test_dlh_2c_grid_boundary.py` — narrow Issue #7 blocker-provenance conversion only (`test_upper_bound_sensitivity_gate` → `test_issue7_blocker_provenance_regression`)
7. `tests/test_dlh_2c_b1_asset_domain.py`
8. `reports/dlh_2c_b1_asset_domain_2026_08_19/DLH_2C_B1_EXECUTION_REPORT.md`
9. `reports/dlh_2c_b1_asset_domain_2026_08_19/DLH_2C_B1_DOMAIN_RESULTS.csv`
10. `reports/dlh_2c_b1_asset_domain_2026_08_19/DLH_2C_B1_FORBIDDEN_OPERATION_CHECK.md`

**No accepted economics/solver module and no accepted DLH-2A/DLH-2B test was modified. Issue #7 reports/evidence untouched. `a_max` not enlarged beyond 200.**

## 4. Environment and exact commands

- Python `3.11.9` (pre-existing); numpy `2.4.6`, scipy `1.17.1`, pytest `8.2.1` (pre-existing; zero installs; no environment mutation; no GPU).

**Command 1 — full repository test suite (exact command):**
```
$env:PYTHONPATH = "D:\deep-learning-hank\src"
python -m pytest tests -v
```
Result: **46 passed, 1 failed**. The single failure is `tests/test_dlh_2c_b1_asset_domain.py::test_wide_domain_grid_refinement_gates` — the documented gate failure (`BLOCKED_DLH_2C_B1_WIDE_DOMAIN_GRID_CONVERGENCE`, `d_grid_200 = 0.004952190295 > d_grid_100 + 1e-12`). **DLH-2A (15) + DLH-2B (17) regression clean (32/32 PASS); Issue #7 grid/permutation/residual/reproducibility tests PASS; the converted Issue #7 blocker-provenance assertion PASSES.**

**Command 2 — full domain diagnostics capture (exact self-contained script):**
```
$env:PYTHONPATH = "D:\deep-learning-hank\src"
$script = @'
from deep_learning_hank.diagnostics.tier0_asset_domain import (
    load_variants, coarse_bound_convergence_metrics,
    wide_domain_grid_refinement_metrics, tail_diagnostics, reproducibility_metrics)
v = load_variants()
for name in ("C50","C100","C150","C200","F100","F200"):
    d = v[name][1]; f = d.result.final
    print(f"{name}: K*={f.capital:.10f} Y={f.output:.8f} w={f.wage:.8f} r={f.net_capital_return:.8e} C={f.mean_consumption:.8f} tr={f.transfer:.8f} A={f.mean_assets:.8f} gates={d.all_gates_pass}")
cb = coarse_bound_convergence_metrics(v)
print("COARSE", {k: (round(val, 15) if isinstance(val, float) else val) for k, val in cb.items()})
wg = wide_domain_grid_refinement_metrics(v)
print("WIDE", {k: (round(val, 15) if isinstance(val, float) else val) for k, val in wg.items()})
td = tail_diagnostics(v)
print("TAIL rows")
for name, row in td["rows"].items():
    print(f"  {name}: K={row['capital']:.10f} Y={row['output']:.8f} w={row['wage']:.8f} r={row['net_capital_return']:.8e} C={row['mean_consumption']:.8f} tr={row['transfer']:.8f} ub_mass={row['upper_boundary_mass']:.8e} top5={row['top5_mass']:.8e} A/amax={row['mean_assets_over_amax']:.8f}")
print("TAIL successive", td["successive_relative_changes"])
print("TAIL fine bound", td["k_f100"], td["k_f200"], td["d_fine_bound_100_200"], td["d_fine_bound_flag_gt_half_percent"])
rp = reproducibility_metrics(v)
print("REPRO gate", rp["gate"])
for n, dd in rp["per_variant_max_abs_diffs"].items():
    print(f"  {n}: max={max(dd.values()):.3e}")
'@
Set-Content -Path (Join-Path $env:TEMP "dlh2cb1_diag.py") -Value $script -Encoding UTF8
python (Join-Path $env:TEMP "dlh2cb1_diag.py")
```

## 5. Variants (all `VALIDATION_FIXTURE_NOT_CALIBRATION`)

| Variant | Grid | a_max | Spacing |
|---|---|---|---|
| C50 (accepted G80_50, read-only) | 80 | 50 | 50/79 |
| C100 (accepted W159_100, read-only) | 159 | 100 | 100/158 = 50/79 |
| C150 (new) | 238 | 150 | 150/237 = 50/79 |
| C200 (new) | 317 | 200 | 200/316 = 50/79 |
| F100 (new fine) | 317 | 100 | 100/316 = 25/79 |
| F200 (new fine) | 633 | 200 | 200/632 = 25/79 |

## 6. Per-variant numerical gates — **ALL PASS** (C150, C200, F100, F200)

| Variant | K* | Y | w | r | C | transfer | all gates |
|---|---|---|---|---|---|---|---|
| C150 | 28.2188912988 | 2.7237170238 | 1.9066019157 | 8.95631498e-3 | 2.1593391920 | 0.2859902882 | True |
| C200 | 28.2189690818 | 2.7237192673 | 1.9066034867 | 8.95625911e-3 | 2.1593398913 | 0.2859905159 | True |
| F100 | 28.0674152515 | 2.7193225569 | 1.9035257937 | 9.06561795e-3 | 2.1579742573 | 0.2855288684 | True |
| F200 | 28.0799120140 | 2.7196857286 | 1.9037800112 | 9.05656254e-3 | 2.1580874886 | 0.2855670019 | True |

Every variant: root converged; root trace finite; capital residual ≤ 1e-7; all HJB/KFE/accounting/effective-labor gates pass; `L_g − L_bar = 0`.

## 7. Coarse-spacing asset-bound convergence — **PASS**

- `d50_100 = 0.034115773466656` — reproduces accepted Issue #7 value `0.03411577346665587` within `1e-12` ✓ (gate_provenance).
- `d100_150 = 0.000453983596378 <= d50_100 + 1e-12` ✓ (gate_no_worsen_1).
- `d150_200 = 2.756408258e-06 <= d100_150 + 1e-12` ✓ (gate_no_worsen_2).
- `d150_200 = 2.756408258e-06 <= 0.005` ✓ (gate_final).
- K sequence: 27.244 → 28.206 → 28.219 → 28.219. **The asset domain converges to ≈28.22 by `a_max=100`; the coarse-bound criterion is met at `a_max=200`.** `BLOCKED_DLH_2C_B1_ASSET_DOMAIN_NOT_CONVERGED` not triggered.

## 8. Wide-domain grid-refinement — **FAIL (terminal blocker)**

- At `a_max=100`: `d_grid_100 = 0.004940431182927 <= 0.005` ✓ (K_F100=28.0674 vs K_C100=28.2061).
- At `a_max=200`: `d_grid_200 = 0.004952190294576 <= 0.005` ✓ (individually), **but `d_grid_200 > d_grid_100 + 1e-12`** (0.004952190 vs 0.004940431; difference ≈ 1.18e-5) → `gate_200_no_worsen = False` → **`BLOCKED_DLH_2C_B1_WIDE_DOMAIN_GRID_CONVERGENCE`.**
- Relative differences C100→F100 and C200→F200 (observations; all < 0.5%, no reviewer flags): output 0.001477/0.001481, wage same, net return 1.00e-4, transfer 4.22e-4, mean consumption 5.79e-4, mean assets 0.004916/0.004928.

Interpretation (diagnostic, not an excuse): the asset-domain *bound* sequence converges cleanly (Section 7), but the *fixed-bound grid-refinement* response is marginally non-monotonic: at `a_max=200`, halving the spacing moves K by 0.4952% vs 0.4940% at `a_max=100` — both just under the individual 0.5% criterion, but the "must not worsen" condition fails by ≈1.2e-5 relative. Per Issue #8 this is a fail-closed result; no further `a_max` enlargement and no threshold redefinition were performed.

## 9. Tail diagnostics (evidence; C50/C100/C150/C200)

| Variant | upper-boundary mass | top-5% mass | mean assets / a_max |
|---|---|---|---|
| C50 | 1.24708934e-02 | 3.37799584e-02 | 0.544876 |
| C100 | 8.90977578e-05 | 5.90981283e-04 | 0.282061 |
| C150 | 3.75148759e-07 | 4.94554602e-06 | 0.188126 |
| C200 | 5.50488358e-10 | 1.36530748e-08 | 0.141095 |

- Successive relative changes of K: C50→C100 `0.034116`, C100→C150 `0.000454`, C150→C200 `2.76e-06` (monotone decay; the upper tail empties as the bound grows).
- Fine-spacing bound observation `d_fine_bound_100_200` (F100 vs F200) = `0.00044504279553887104` — **observation, not a mandatory gate; < 0.5%, no flag.**

## 10. Issue #7 blocker provenance conversion

`tests/test_dlh_2c_grid_boundary.py::test_issue7_blocker_provenance_regression` (converted from `test_upper_bound_sensitivity_gate`) **PASSES**: the frozen Issue #7 fixture reproduces `d_bound_K = 0.03411577346665587 > 0.005` within 1e-12 and `metrics["gate"] is False` — the accepted scientific failure is preserved; Issue #7 is NOT written as PASS; its reports/evidence were not modified.

## 11. Deterministic reproducibility — **PASS**

C150, C200, F100, F200 run twice each: max absolute repeat differences all **exactly 0.0** (≤ 1e-12) for K*, wage, net return, output, transfer, value, consumption, drift, distribution mass, scalar diagnostics.

## 12. Regression — **PASS**

Accepted DLH-2A (15) + DLH-2B (17) tests all continue to pass (32/32); Issue #7 other robustness tests (per-variant gates, grid convergence, spacing match, residual scan, reproducibility, permutation invariance, fixture labels) PASS; converted Issue #7 provenance assertion PASSES. No `BLOCKED_DLH_2C_B1_REGRESSION`.

## 13. Test results (full repository suite)

- **46 passed, 1 failed.** The single failure is the wide-domain grid-refinement gate test (`d_grid_200 = 0.004952190295 > d_grid_100 + 1e-12`) — the intended fail-closed evidence for `BLOCKED_DLH_2C_B1_WIDE_DOMAIN_GRID_CONVERGENCE`.

## 14. Engineering corrections / reruns

- None required; no test-plumbing fix was needed. No economics, grid standard, domain criterion, or threshold was changed. One execution attempt (suite) plus the diagnostics capture.

## 15. Forbidden-operation counters (all zero)

- W^L / W^K / old W / regional/multi-region = 0 · SOE / RegionalAccounts = 0 · nominal/Fisher/NKPC/Taylor = 0 · shocks/AR(1) / transition = 0 · neural/RL = 0 · empirical data/calibration/regression = 0 · Matlab/Octave/Dynare = 0 · legacy Matlab reads = 0 · old Python source-repo access = 0 · Results/policy/novelty claims = 0 · governance changes = 0 · modification of accepted economics/solver modules or accepted DLH-2A/DLH-2B tests = 0 · modification of Issue #7 reports/evidence = 0 · `a_max > 200` = 0 · PR / merge / Issue close / successor / self-accept = 0.

## 16. Evidence boundary

PASS/fail here is D2 machine-diagnostic evidence about asset-domain adequacy up to `a_max=200` for the small one-region real HA/Aiyagari Tier-0 validation fixture. It does not establish calibration, genuine HANK, regional NSR-HANK, transition, policy, Results, or novelty.

## 17. Recommendation (suggestion only — no successor creation)

The wide-domain grid-refinement non-monotonicity (0.4952% vs 0.4940%, both under the individual 0.5% criterion) should be independently reviewed; possible scientific responses (Owner/ChatGPT decision, not Builder action) include a documented interpretation of the fixed-bound refinement metric at `a_max=200`, or re-scoping the criterion. No successor Issue was created.
