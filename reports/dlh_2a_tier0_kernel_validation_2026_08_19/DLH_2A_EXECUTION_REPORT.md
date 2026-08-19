# DLH-2A-R1 — Tier-0 Kernel Fixed-Price Validation — Execution Report (Corrected)

- Date: 2026-08-19 (R1 evidence/diagnostic correction)
- Author: DSH (bounded Builder)
- Authority: GitHub Issue #5 — `DLH-2A: Tier-0 kernel migration and fixed-price HJB/KFE validation`; authoritative R1 correction comment (2026-08-19 10:19:51).
- Prior candidate: `2a2534d0660e433bbe48b5576dba18c8df83c9c4` — core numerical gate independently PASSED; candidate NOT accepted/merged; R1 applies bounded evidence/diagnostic corrections only.
- Status: CANDIDATE. Acceptance requires fresh-GitHub independent review (ChatGPT).
- Evidence class: **D2 machine-diagnostic evidence only**.

## 1. Terminal classification

`DLH_2A_R1_EVIDENCE_AND_DIAGNOSTIC_CORRECTION_READY_FOR_GPT_REVIEW`

## 2. Baselines and branch

- Fresh target `origin/main` SHA: `ad1ca1096b4e10667a70703d896648b66d0191a0`
- Fresh source-repo `main` SHA: `3039a145f43d419a08999c476cd0d97fd5f8341f` (matches accepted audit source; no drift)
- Dedicated R1 branch: `dsh/issue-5-dlh-2a-r1-evidence-diagnostic-correction-2026-08-19`
- Candidate commit: single coherent commit at branch HEAD (2026-08-19, DSH); hash reported in completion response. Expected delta: exactly the 21 allowlisted paths, 0 behind / 1 ahead.

## 3. Exact changed paths (21-path allowlist)

1. `pyproject.toml`
2. `configs/dlh_2a_fixed_price_validation.toml`
3. `src/deep_learning_hank/__init__.py`
4. `src/deep_learning_hank/config.py`
5. `src/deep_learning_hank/economics/__init__.py`
6. `src/deep_learning_hank/economics/preferences.py`
7. `src/deep_learning_hank/economics/grids.py`
8. `src/deep_learning_hank/economics/firm.py`
9. `src/deep_learning_hank/economics/fiscal.py`
10. `src/deep_learning_hank/solvers/__init__.py`
11. `src/deep_learning_hank/solvers/household_hjb.py`
12. `src/deep_learning_hank/solvers/distribution_kfe.py`
13. `src/deep_learning_hank/diagnostics/__init__.py`
14. `src/deep_learning_hank/diagnostics/tier0_fixed_price.py`
15. `tests/test_dlh_2a_economics.py`
16. `tests/test_dlh_2a_hjb_kfe.py`
17. `tests/test_dlh_2a_reproducibility.py`
18. `reports/dlh_2a_tier0_kernel_validation_2026_08_19/DLH_2A_EXECUTION_REPORT.md`
19. `reports/dlh_2a_tier0_kernel_validation_2026_08_19/DLH_2A_DIAGNOSTICS.csv`
20. `reports/dlh_2a_tier0_kernel_validation_2026_08_19/DLH_2A_SOURCE_PROVENANCE.csv`
21. `reports/dlh_2a_tier0_kernel_validation_2026_08_19/DLH_2A_FORBIDDEN_OPERATION_CHECK.md`

R1 changes were confined to: `household_hjb.py` (diagnostic semantics), `tests/test_dlh_2a_hjb_kfe.py` (literal-min assertion), and the four report/provenance files. No other path modified.

## 4. Source provenance mapping (bounded adaptation / reimplementation)

Source repo `zcx369658780/dissertation-ch5-r5-python-model` @ `3039a145f43d419a08999c476cd0d97fd5f8341f` (read-only). See `DLH_2A_SOURCE_PROVENANCE.csv` (column `source_blob_oid` = 40-char Git/GitHub blob object ID) for the mapping. Summary:

- `economics/grids.py` ← audited `grids.py` — **ADAPTED**
- `economics/preferences.py` ← audited `household_hjb.py` utility helpers — **ADAPTED/REIMPLEMENTED**
- `economics/firm.py` ← audited `production_block` **two-factor core only** — **ADAPTED**
- `economics/fiscal.py` ← audited `fiscal_closure` **lump-sum part only** — **ADAPTED**
- `solvers/household_hjb.py` ← audited `household_hjb.py` — **REIMPLEMENTED**
- `solvers/distribution_kfe.py` ← audited `distribution_kfe.py` — **REIMPLEMENTED**

## 5. Environment

- Python `3.11.9` (pre-existing); numpy `2.4.6`, scipy `1.17.1`, pytest `8.2.1` (pre-existing; zero installs, zero environment mutation); no GPU.

## 6. Exact commands executed (original first run vs R1 rerun — history preserved)

**Original candidate first run (2026-08-19, R0):**
```
$env:PYTHONPATH = "D:\deep-learning-hank\src"
python -m pytest tests -v
```
Result: **15 passed** (7 economics + 7 HJB/KFE + 1 reproducibility). The original diagnostics capture command used a placeholder (`python -c "..."`); this defect is corrected by R1 (below).

**R1 correction rerun (2026-08-19):**
1. Full test suite (exact command):
```
$env:PYTHONPATH = "D:\deep-learning-hank\src"
python -m pytest tests -v
```
Result: **15 passed** (7 + 7 + 1), including the strengthened literal-minimum off-diagonal assertion.

2. Corrected diagnostics capture (exact command — the script was written to a temp file and executed; full script text below):
```
$env:PYTHONPATH = "D:\deep-learning-hank\src"
$script = @'
from pathlib import Path
import numpy as np
from deep_learning_hank.config import FixedPriceConfig
from deep_learning_hank.diagnostics.tier0_fixed_price import run_fixed_price_validation
cfg = FixedPriceConfig.from_toml(Path("configs/dlh_2a_fixed_price_validation.toml"))
d = run_fixed_price_validation(cfg)
hh, dist = d.household, d.distribution
print("config_sha256", d.config_sha256)
print("hjb_converged", hh.converged)
print("hjb_iterations", hh.iterations)
print("hjb_true_residual", repr(hh.true_residual))
print("hjb_min_consumption", repr(hh.min_consumption))
print("hjb_lower_boundary_min_drift", repr(hh.lower_boundary_min_drift))
print("hjb_upper_boundary_max_drift", repr(hh.upper_boundary_max_drift))
print("hjb_generator_row_sum_max_abs", repr(hh.generator_row_sum_max_abs))
print("hjb_generator_min_off_diagonal_literal", repr(hh.generator_min_off_diagonal))
print("hjb_generator_min_positive_off_diagonal_obs", repr(hh.generator_min_positive_off_diagonal))
print("hjb_nan_inf_count", hh.nan_inf_count)
print("kfe_mass_error", repr(dist.mass_error))
print("kfe_stationarity_residual", repr(dist.stationarity_residual))
print("kfe_minimum_mass", repr(dist.minimum_mass))
print("kfe_pre_cleanup_minimum_mass", repr(dist.pre_cleanup_minimum_mass))
print("kfe_cleanup_rule", dist.cleanup_rule)
print("kfe_negative_mass_count", dist.negative_mass_count)
print("kfe_nan_inf_count", dist.nan_inf_count)
print("kfe_state_marginals", [float(x) for x in dist.state_marginals])
print("kfe_state_marginal_error", repr(d.state_marginal_error))
print("kfe_mean_assets", repr(dist.mean_assets))
print("kfe_mean_consumption", repr(dist.mean_consumption))
print("kfe_lower_boundary_mass", repr(dist.lower_boundary_mass))
print("kfe_upper_boundary_mass", repr(dist.upper_boundary_mass))
print("all_gates_pass", d.all_gates_pass)
d2 = run_fixed_price_validation(cfg)
diffs = {
 "value": float(np.max(np.abs(hh.value - d2.household.value))),
 "consumption": float(np.max(np.abs(hh.consumption - d2.household.consumption))),
 "drift": float(np.max(np.abs(hh.drift - d2.household.drift))),
 "distribution_mass": float(np.max(np.abs(dist.mass - d2.distribution.mass))),
 "scalars": float(np.max(np.abs(d.scalar_vector() - d2.scalar_vector()))),
}
print("repeat_diffs", diffs)
'@
Set-Content -Path (Join-Path $env:TEMP "dlh2a_r1_diag.py") -Value $script -Encoding UTF8
python (Join-Path $env:TEMP "dlh2a_r1_diag.py")
```

## 7. Test results

- `tests/test_dlh_2a_economics.py` — **7 passed** (7 test functions)
- `tests/test_dlh_2a_hjb_kfe.py` — **7 passed** (7 test functions)
- `tests/test_dlh_2a_reproducibility.py` — **1 passed** (1 test function)
- **R1 rerun total: 15 passed, 0 failed, 0 skipped.**
- Original candidate first run total: **15 passed** (same 15 tests; the R0 report's incorrect "HJB/KFE = 8" breakdown is corrected here to 7; total 15 preserved as historical fact).

## 8. Fixture — VALIDATION_FIXTURE_NOT_CALIBRATION

Unchanged from R0: asset grid `[0,50]`/40 pts; states `(0.5,1.5)`; intensities `0.25/0.25`; `rho_hh=0.01`; `gamma=2.0`; `wage=1.57`; return `0.01`; transfer `0.50`; `tau_l=0.15`; HJB tol `1e-7`; max iters `2000`; pseudo-time `1000`; floor `1e-10`. Labeled `VALIDATION_FIXTURE_NOT_CALIBRATION`; never described as empirical calibration.

## 9. HJB diagnostics (R1 rerun) and thresholds

| Diagnostic | Observed (R1) | Threshold | PASS |
|---|---|---|---|
| converged | True | True | ✓ |
| iterations | 7 | <= 2000 | ✓ |
| true HJB residual | 8.335084289434747e-08 | <= 1e-7 | ✓ |
| min consumption | 1.1672500000000001 | > 0 | ✓ |
| lower-boundary min drift | 0.0 | >= -1e-12 | ✓ |
| upper-boundary max drift | 0.0 | <= 1e-12 | ✓ |
| generator row-sum max abs | 5.551115123125783e-17 | <= 1e-12 | ✓ |
| **generator min off-diagonal (literal, incl. implicit zeros)** | **0.0** | >= -1e-14 | ✓ |
| generator min off-diagonal (observation: min stored nonzero rate) | 0.19199361231963288 | (observation) | — |
| NaN/Inf count | 0 | = 0 | ✓ |

R1 correction (D): `generator_min_off_diagonal` now reports the **literal minimum over ALL off-diagonal matrix entries**, including implicit sparse zeros (`min(stored_min, 0.0)`). For this generator all stored rates are >= 0, so the literal minimum is `0.0`. Threshold unchanged (>= -1e-14). Generator construction itself is unchanged.

Residual-history shape (observation only): `0.1479 -> 0.0151 -> 0.0025 -> 1.37e-4 -> 1.03e-5 -> 9.21e-7 -> 8.34e-8` (7 entries, monotonically decreasing).

## 10. KFE diagnostics (R1 rerun) and thresholds

| Diagnostic | Observed (R1) | Threshold | PASS |
|---|---|---|---|
| mass error | 0.0 | <= 1e-10 | ✓ |
| stationarity residual | 3.69712940817557e-17 | <= 1e-8 | ✓ |
| minimum mass (after cleanup) | 8.256457805979809e-04 | >= -1e-12 | ✓ |
| pre-cleanup minimum mass | 8.256457805979809e-04 | (reported) | — |
| cleanup rule | none | (reported) | — |
| negative mass count | 0 | = 0 | ✓ |
| NaN/Inf count | 0 | = 0 | ✓ |
| state marginals | [0.5, 0.5] (error 0.0) | within 1e-8 | ✓ |
| mean assets | 29.01671540591199 | within [0, 50] | ✓ |
| mean consumption | 2.1246671540591198 | > 0 | ✓ |

## 11. Deterministic reproducibility (R1 rerun)

Two runs, max absolute repeat differences (threshold `1e-12`): value `0.0`, consumption `0.0`, drift `0.0`, distribution mass `0.0`, scalars `0.0` — all PASS.

## 12. Engineering corrections / reruns

- R1 diagnostics-semantics fix in `household_hjb.py` (literal off-diagonal minimum); strengthened `test_hjb_gate_generator_contract` with a literal-minimum assertion.
- Test attempt count: original first run = 1 (15 passed); R1 rerun = 1 (15 passed). No threshold was relaxed; no scientific scope change.

## 13. Forbidden-operation counters (all zero)

- source-repo writes = 0 · legacy Matlab reads = 0 · regional/W code = 0 · outer GE/capital root = 0 · SOE / nominal / shocks / transition / neural = 0 · data/calibration/regression = 0 · Results claims = 0 · governance changes = 0 · PR / merge / Issue close / successor / self-accept = 0.

## 14. Evidence boundary

D2 machine-diagnostic evidence only; does not imply calibration, genuine-HANK validity, regional NSR-HANK validity, or Results eligibility.

## 15. Recommendation for next gate (suggestion only — no successor creation)

`DLH-2B` — single-region firm/fiscal + capital-market clearing + full Tier-0 steady state, after independent review of this corrected packet.
