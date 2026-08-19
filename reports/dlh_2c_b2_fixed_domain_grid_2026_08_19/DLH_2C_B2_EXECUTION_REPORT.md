# DLH-2C-B2 — Fixed-Domain Third-Level Grid Convergence / Canonical Tier-0 Numerical Standard — Execution Report

- Date: 2026-08-19
- Author: DSH (bounded Builder)
- Authority: GitHub Issue #9 — `DLH-2C-B2: Fixed-domain third-level grid convergence and canonical Tier-0 numerical standard`
- Accepted predecessor: Issue #8 / DLH-2C-B1 fail-closed, accepted commit `249c9dcaf3c16b4b308e9d83daf232a23dce79cb` (`DLH_2C_B1_WIDE_DOMAIN_GRID_CONVERGENCE_BLOCKED_ACCEPTED`; frozen dependency).
- Status: **CANDIDATE (scientific success)**. All mandatory Issue #9 gates PASS; acceptance requires fresh-GitHub independent review (ChatGPT).
- Evidence class: **D2 machine-diagnostic evidence** (small one-region real HA/Aiyagari Tier-0 benchmark on fixed domain `[0,200]`).

## 1. Terminal classification

`DLH_2C_B2_FIXED_DOMAIN_GRID_CONVERGENCE_READY_FOR_GPT_REVIEW`

## 2. Baselines and branch

- Fresh target `origin/main` SHA: `c6352a5fba975222fd34f2255b44707ed76b46a4`
- Dedicated branch: `dsh/issue-9-dlh-2c-b2-fixed-domain-grid-2026-08-19`
- Candidate commit: single coherent commit at branch HEAD (2026-08-19, DSH); hash reported in completion response. Expected delta: exactly the 7 allowlisted paths, 0 behind / 1 ahead.

## 3. Exact changed paths (7-path allowlist)

1. `configs/dlh_2c_b2_bound200_quarter_spacing_validation.toml` (Q200: 1265 pts [0,200], spacing 200/1264 = 12.5/79)
2. `src/deep_learning_hank/diagnostics/tier0_fixed_domain_grid.py`
3. `tests/test_dlh_2c_b1_asset_domain.py` — narrow Issue #8 blocker-provenance conversion only (`test_wide_domain_grid_refinement_gates` → `test_issue8_blocker_provenance_regression`)
4. `tests/test_dlh_2c_b2_fixed_domain_grid.py`
5. `reports/dlh_2c_b2_fixed_domain_grid_2026_08_19/DLH_2C_B2_EXECUTION_REPORT.md`
6. `reports/dlh_2c_b2_fixed_domain_grid_2026_08_19/DLH_2C_B2_GRID_RESULTS.csv`
7. `reports/dlh_2c_b2_fixed_domain_grid_2026_08_19/DLH_2C_B2_FORBIDDEN_OPERATION_CHECK.md`

**No accepted economics/solver module and no accepted DLH-2A/DLH-2B test was modified. Issue #7/#8 reports/evidence untouched. Asset domain frozen at `[0,200]`; no grid beyond Q200.**

## 4. Environment and exact commands

- Python `3.11.9` (pre-existing); numpy `2.4.6`, scipy `1.17.1`, pytest `8.2.1` (pre-existing; zero installs; no environment mutation; no GPU).

**Command 1 — full repository test suite (exact command):**
```
$env:PYTHONPATH = "D:\deep-learning-hank\src"
python -m pytest tests -v
```
Result: **54 passed, 0 failed** (DLH-2A 15 + DLH-2B 17 + Issue #7 8 + Issue #8 8 + DLH-2C-B2 6). Includes the converted Issue #7 and Issue #8 blocker-provenance assertions (PASS) and all new active DLH-2C-B2 gates (PASS).

**Command 2 — fixed-domain grid diagnostics capture (exact self-contained script):**
```
$env:PYTHONPATH = "D:\deep-learning-hank\src"
$script = @'
from deep_learning_hank.diagnostics.tier0_fixed_domain_grid import (
    load_variants, fixed_domain_grid_convergence_metrics,
    macro_object_convergence_metrics, tail_diagnostics, reproducibility_metrics)
v = load_variants()
for name in ("C200","F200","Q200"):
    d = v[name][1]; f = d.result.final
    print(f"{name}: K*={f.capital:.10f} Y={f.output:.8f} w={f.wage:.8f} r={f.net_capital_return:.8e} C={f.mean_consumption:.8f} tr={f.transfer:.8f} A={f.mean_assets:.8f} gates={d.all_gates_pass}")
gd = fixed_domain_grid_convergence_metrics(v)
print("GRID_CONV", {k: (round(val, 17) if isinstance(val, float) else val) for k, val in gd.items()})
mo = macro_object_convergence_metrics(v)
print("MACRO", mo)
td = tail_diagnostics(v)
print("TAIL")
for name, row in td["rows"].items():
    print(f"  {name}: ub_mass={row['upper_boundary_mass']:.8e} top5={row['top5_mass']:.8e} A/amax={row['mean_assets_over_amax']:.8f}")
rp = reproducibility_metrics(v)
print("REPRO gate", rp["gate"], "max", max(rp["max_abs_diffs"].values()), rp["max_abs_diffs"])
'@
Set-Content -Path (Join-Path $env:TEMP "dlh2cb2_diag.py") -Value $script -Encoding UTF8
python (Join-Path $env:TEMP "dlh2cb2_diag.py")
```

## 5. Fixed domain and grid sequence

Asset domain frozen at `a in [0,200]`. Grid sequence (all `VALIDATION_FIXTURE_NOT_CALIBRATION`, identical economics/thresholds):

| Grid | Points | Spacing | Ratio |
|---|---|---|---|
| C200 (accepted, read-only) | 317 | 200/316 = 50/79 | h |
| F200 (accepted, read-only) | 633 | 200/632 = 25/79 | h/2 |
| Q200 (new) | 1265 | 200/1264 = 12.5/79 | h/4 |

## 6. Q200 per-variant numerical gates — **PASS**

Q200: K\* = 28.0102521166, Y = 2.7176598944, w = 1.9023619261, r = 9.10712709e-3, C = 2.1574548520, transfer = 0.2853542889. Root converged; root trace finite; capital residual ≤ 1e-7; all HJB (residual ≤ 1e-7, min c > 0, boundary drifts, generator row-sum ≤ 1e-12, literal off-diag ≥ −1e-14, NaN/Inf 0), KFE (mass ≤ 1e-10, stationarity ≤ 1e-8, min mass ≥ −1e-12, neg count 0, NaN/Inf 0), effective-labor (error 0 ≤ 1e-8), fiscal (≤ 1e-12), goods (≤ 1e-7), budget (≤ 1e-7), mean drift (≤ 1e-7) gates pass; Y/w/C/K > 0; return finite.

## 7. Fixed-domain successive grid-convergence gate — **PASS**

- `K_C = 28.218969081766193`, `K_F = 28.079912014017818`, `K_Q = 28.010252116571742`.
- `d_C_F = 0.00495219029457629` — **reproduces accepted Issue #8 value `0.004952190294576287` within 1e-12** ✓ (gate_provenance).
- `d_F_Q = 0.00248694289348661 <= d_C_F + 1e-12` ✓ (gate_no_worsen) — successive refinement on the same fixed domain does not worsen.
- `d_F_Q = 0.00248694289348661 <= 0.005` ✓ (gate_final).
- `ratio = d_F_Q / d_C_F = 0.5021904946201973` — reported exactly; **not** ≤ 0.5, so no `STRONG_REFINEMENT_OBSERVATION` mark (observation only; no ex-post criterion imposed).
- `BLOCKED_DLH_2C_B2_FIXED_DOMAIN_GRID_NOT_CONVERGED` not triggered.

## 8. Macro-object fixed-domain convergence (F200 → Q200) — **PASS**

| Object | relative difference | ≤ 0.005 |
|---|---|---|
| output | 0.000744879 | ✓ |
| wage | 0.000744879 | ✓ |
| net capital return | 5.056456e-05 | ✓ |
| transfer | 0.000212713 | ✓ |
| mean consumption | 0.000293148 | ✓ |
| mean assets | 0.002480773 | ✓ |

`BLOCKED_DLH_2C_B2_MACRO_GRID_CONVERGENCE` not triggered.

## 9. Upper-tail diagnostics (observations only)

| Grid | upper-boundary mass | top-5% mass | mean assets / a_max |
|---|---|---|---|
| C200 | 5.504884e-10 | 1.365308e-08 | 0.141095 |
| F200 | 5.805985e-10 | 1.942123e-08 | 0.140400 |
| Q200 | 5.852582e-10 | 2.370891e-08 | 0.140051 |

Upper-tail mass converges stably near the boundary with grid refinement (observations; do not override gates; `a_max=200` unchanged).

## 10. Issue #8 blocker-provenance conversion

`tests/test_dlh_2c_b1_asset_domain.py::test_issue8_blocker_provenance_regression` (converted from `test_wide_domain_grid_refinement_gates`) **PASSES**: verifies `d_grid_100 = 0.0049404311829274825 <= 0.005`, `d_grid_200 = 0.004952190294576287 <= 0.005`, `d_grid_200 > d_grid_100 + 1e-12`, and both accepted values reproduced within 1e-12; Issue #8 remains `BLOCKED_ACCEPTED`, not PASS; Issue #8 reports/evidence untouched.

## 11. Deterministic reproducibility — **PASS**

Q200 run twice: max absolute repeat differences all **exactly 0.0** (≤ 1e-12) for K*, wage, net return, output, transfer, value, consumption, drift, distribution mass, scalar diagnostics.

## 12. Regression — **PASS**

Full repository suite **54/54 PASS**: DLH-2A (15) ✓, DLH-2B (17) ✓, Issue #7 tests/provenance (8) ✓, converted Issue #8 blocker-provenance assertion (part of the 8) ✓, new DLH-2C-B2 tests (6) ✓. No `BLOCKED_DLH_2C_B2_REGRESSION`.

## 13. Engineering corrections / reruns

- None required; no test-plumbing fix was needed; no economics, asset domain, grid standard, or threshold was changed. One execution attempt (suite) plus the diagnostics capture.

## 14. Forbidden-operation counters (all zero)

- W^L / W^K / old W / regional/multi-region = 0 · SOE / RegionalAccounts = 0 · nominal/Fisher/NKPC/Taylor = 0 · shocks/AR(1) / transition = 0 · neural/RL = 0 · empirical data/calibration/regression = 0 · Matlab/Octave/Dynare = 0 · legacy Matlab reads = 0 · old Python source-repo access = 0 · Results/policy/novelty claims = 0 · governance changes = 0 · modification of accepted economics/solver modules or accepted DLH-2A/DLH-2B tests = 0 · modification of Issue #7/#8 reports/evidence = 0 · asset-domain change away from `[0,200]` = 0 · grid beyond Q200 = 0 · PR / merge / Issue close / successor / self-accept = 0.

## 15. Evidence boundary

PASS supports D2 machine-diagnostic evidence that the small one-region real HA/Aiyagari Tier-0 benchmark is numerically adequate on fixed asset domain `[0,200]` under the explicit three-level grid sequence C200→F200→Q200 (h→h/2→h/4), together with the previously accepted asset-bound evidence. It does not establish calibration, genuine HANK, regional NSR-HANK, transition, policy, Results, or novelty.

## 16. Recommendation (suggestion only — no successor creation)

If this Issue passes independent review, the Tier-0 numerical-robustness block may be considered complete and DLH-3 (minimal genuine single-region HANK) may be issued separately by ChatGPT/Owner. No successor Issue was created by the Builder.
