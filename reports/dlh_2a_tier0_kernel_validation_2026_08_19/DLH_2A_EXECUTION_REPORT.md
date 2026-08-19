# DLH-2A — Tier-0 Kernel Fixed-Price Validation — Execution Report

- Date: 2026-08-19
- Author: DSH (bounded Builder)
- Authority: GitHub Issue #5 — `DLH-2A: Tier-0 kernel migration and fixed-price HJB/KFE validation`
- Status: CANDIDATE. Acceptance requires fresh-GitHub independent review (ChatGPT).
- Evidence class: **D2 machine-diagnostic evidence only** (this gate does not imply calibration, genuine-HANK validity, regional NSR-HANK validity, or Results eligibility).

## 1. Terminal classification

`DLH_2A_TIER0_KERNEL_FIXED_PRICE_VALIDATION_READY_FOR_GPT_REVIEW`

## 2. Baselines and branch

- Fresh target `origin/main` SHA: `a928e2780254bdb3fe9c87567228a2c8c0a89f10`
- Fresh source-repo `main` SHA: `3039a145f43d419a08999c476cd0d97fd5f8341f` (matches accepted audit source; no drift)
- Dedicated branch: `dsh/issue-5-dlh-2a-tier0-kernel-validation-2026-08-19`
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

No other path modified (README, roadmap, accepted audit/spec/evidence, governance, Task Index, Startup Snapshot, `.gitignore` untouched).

## 4. Source provenance mapping (bounded adaptation / reimplementation)

Source repo `zcx369658780/dissertation-ch5-r5-python-model` @ `3039a145f43d419a08999c476cd0d97fd5f8341f` (read-only). See `DLH_2A_SOURCE_PROVENANCE.csv` for blob-level mapping. Summary:

- `economics/grids.py` ← audited `grids.py` pattern — **ADAPTED**
- `economics/preferences.py` ← audited `household_hjb.py` utility/marginal helpers — **ADAPTED/REIMPLEMENTED**
- `economics/firm.py` ← audited `regional_structure.production_block` **two-factor core only** (SOE `alpha_g`/`S` factor dropped) — **ADAPTED**
- `economics/fiscal.py` ← audited `aggregate_block.fiscal_closure` **lump-sum/balanced part only** (SOE rent dropped) — **ADAPTED**
- `solvers/household_hjb.py` ← audited `household_hjb.py` — **REIMPLEMENTED** (clean economics/solver separation; same accepted math contract; no wholesale copy)
- `solvers/distribution_kfe.py` ← audited `distribution_kfe.py` — **REIMPLEMENTED** (clean separation; same accepted math contract)

No old module names/architecture migrated for convenience; no wholesale copy of the old package.

## 5. Environment

- Python: `3.11.9` (pre-existing system Python; executable category = pre-existing, not task-local venv)
- numpy `2.4.6`, scipy `1.17.1`, pytest `8.2.1` (all pre-existing; **zero installs performed, zero environment mutation**)
- No GPU required or used.

## 6. Exact commands executed

```
$env:PYTHONPATH = "D:\deep-learning-hank\src"
python -m pytest tests -v
python -c "..."   # diagnostics capture (see DLH_2A_DIAGNOSTICS.csv)
```

- Test attempt count: **1** (full suite passed on the first run; no engineering correction or rerun was needed).

## 7. Test results

- `tests/test_dlh_2a_economics.py` — 7 passed
- `tests/test_dlh_2a_hjb_kfe.py` — 8 passed
- `tests/test_dlh_2a_reproducibility.py` — 1 passed
- **Total: 15 passed, 0 failed, 0 skipped** (`pytest-8.2.1`)

## 8. Fixture — VALIDATION_FIXTURE_NOT_CALIBRATION

The fixture (`configs/dlh_2a_fixed_price_validation.toml`) is a **numerical regression fixture, NOT empirical calibration**: asset grid `[0,50]`/40 pts; productivity states `(0.5,1.5)`; symmetric intensities `0.25/0.25`; `rho_hh=0.01`; `gamma=2.0`; `wage=1.57`; `asset return=0.01`; `transfer=0.50`; `tau_l=0.15`; HJB tolerance `1e-7`; max iterations `2000`; pseudo-time step `1000`; consumption floor `1e-10`. The config header explicitly labels `VALIDATION_FIXTURE_NOT_CALIBRATION`.

## 9. HJB diagnostics (fixed price) and thresholds

| Diagnostic | Observed | Threshold | PASS |
|---|---|---|---|
| converged | True | True | ✓ |
| iterations | 7 | <= 2000 | ✓ |
| true HJB residual | 8.335084289434747e-08 | <= 1e-7 | ✓ |
| min consumption | 1.1672500000000001 | > 0 | ✓ |
| lower-boundary min drift | 0.0 | >= -1e-12 | ✓ |
| upper-boundary max drift | 0.0 | <= 1e-12 | ✓ |
| generator row-sum max abs | 5.551115123125783e-17 | <= 1e-12 | ✓ |
| generator min off-diagonal | 0.19199361231963288 | >= -1e-14 | ✓ |
| NaN/Inf count | 0 | = 0 | ✓ |

Generator contract: continuous-time infinitesimal generator / intensity matrix — off-diagonals >= 0; diagonal = negative total outflow; row sums = 0 (**NOT row-stochastic**; verified by test `generator.sum(axis=1) == 0`). Boundary = state-constraint / no-outward-drift treatment (boundary derivative from constrained-consumption marginal utility; lower drift >= 0; upper drift <= 0); no reflected-process claim.

Residual-history shape (observation only): monotonically decreasing, `0.1479 -> 0.0151 -> 0.0025 -> 1.37e-4 -> 1.03e-5 -> 9.21e-7 -> 8.34e-8` (7 entries).

## 10. KFE diagnostics (stationary, converged HJB generator) and thresholds

| Diagnostic | Observed | Threshold | PASS |
|---|---|---|---|
| mass error | 0.0 | <= 1e-10 | ✓ |
| stationarity residual | 3.69712940817557e-17 | <= 1e-8 | ✓ |
| minimum mass (after cleanup) | 8.256457805979809e-04 | >= -1e-12 | ✓ |
| pre-cleanup minimum mass | 8.256457805979809e-04 | (reported) | — |
| cleanup rule | none (no tiny negatives) | (reported) | — |
| negative mass count | 0 | = 0 | ✓ |
| NaN/Inf count | 0 | = 0 | ✓ |
| state marginals | [0.5, 0.5] (error 0.0) | within 1e-8 of analytic | ✓ |
| mean assets | 29.01671540591199 | within [0, 50] | ✓ |
| mean consumption | 2.1246671540591198 | > 0 | ✓ |

## 11. Deterministic reproducibility

Pipeline run twice in the same environment; max absolute repeat differences (threshold `1e-12`):

| Object | Max abs diff | PASS |
|---|---|---|
| value | 0.0 | ✓ |
| consumption | 0.0 | ✓ |
| drift | 0.0 | ✓ |
| distribution mass | 0.0 | ✓ |
| scalar diagnostics | 0.0 | ✓ |

All diffs are exactly `0.0` (deterministic `spsolve` + `np.linalg.solve`); threshold met. No `BLOCKED_DLH_2A_REPRODUCIBILITY_THRESHOLD`.

## 12. Engineering corrections / reruns

None. The full suite passed on the first attempt; no implementation/tooling/numerical bug was discovered and no threshold was relaxed.

## 13. Forbidden-operation counters (all zero)

- source-repo writes = 0 · legacy Matlab reads = 0 · regional/W code = 0 · outer single-region GE/capital root = 0 · SOE factor / nominal / shocks / transition / neural = 0 · data/calibration/regression = 0 · Results claims = 0 · governance changes = 0 · PR / merge / Issue close / successor / self-accept = 0.

## 14. Evidence boundary

Passing tests here support **D2 machine-diagnostic evidence only**. They do **not** imply final calibration, genuine-HANK validity, regional NSR-HANK validity, or Results eligibility.

## 15. Recommendation for next gate (suggestion only — no successor creation)

`DLH-2B` — single-region firm/fiscal + capital-market clearing + full Tier-0 steady state, building on this validated fixed-price kernel; to be issued as a separate GitHub Issue after independent review.
