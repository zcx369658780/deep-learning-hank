# DLH-3B-R2 — Canonical One-Asset HANK Validation Kernel — Execution Report

- Date: 2026-08-20
- Author: DSH (bounded Builder)
- Authority: GitHub Issue #15 — `DLH-3B-R2: Rebuild Python HA kernel as canonical one-asset HANK validation module` (state: OPEN), activation comment id `IC_kwDOT9FOGc8AAAABPzrXKg`
- Task type: `SCIENTIFIC_IMPLEMENTATION__HA_KERNEL_RECONSTRUCTION`
- Status: **CANDIDATE (scientific success)** — all Issue #15 §7 validation requirements satisfied; acceptance requires fresh-GitHub independent review (ChatGPT).
- Evidence class: D2 machine-diagnostic kernel validation evidence; labels `VALIDATION_FIXTURE_NOT_CALIBRATION`.
- Classification (Issue #15 §8): `DLH_3B_R2_HA_KERNEL_RECONSTRUCTION_READY_FOR_GPT_REVIEW`

## 1. Headline result

The rebuilt canonical one-asset continuous-time HANK validation kernel reproduces the **accepted DLH-3B steady state exactly**:

| Object | Kernel value | Accepted DLH-3B | Abs diff |
|---|---|---|---|
| `r*` | `0.007370613883670197` | `0.007370613883670197` | `0.0` |
| `N*` | `1.0656334480169984` | `1.0656334480169984` | `0.0` |
| `A_hh*` | `10.000000002223675` | `10.000000002223675` | `0.0` |
| `w*` | `0.8333333333333334` (= 5/6) | `5/6` | `0.0` |
| `C*` | `1.065633448423122` | `1.065633448423122` | `0.0` |

This is the strongest evidence that the rebuild preserved scientific meaning (Issue #15 §5: "refactor existing HA code if scientific meaning remains unchanged"): the kernel implements the same economic problem with clean, documented modules.

## 2. Baseline / Issue / branch / commit

- Fresh baseline `origin/main` SHA: `d727dda28738bbdad126c784f0366f0e21be3e1d`
- Issue #15 title/status: `DLH-3B-R2: Rebuild Python HA kernel as canonical one-asset HANK validation module` — OPEN; activation comment `IC_kwDOT9FOGc8AAAABPzrXKg` (2026-08-20T12:19:26Z)
- Dedicated branch: `dsh/issue-15-dlh-3b-r2-ha-kernel-2026-08-20` (created from fresh `origin/main`)
- Candidate commit: single coherent commit at branch HEAD (2026-08-20, DSH); SHA reported in the completion response.
- Note: `tasks/TASK_INDEX_CURRENT.md` on fresh `origin/main` still points to Issue #13 (pointer lag, recorded observation); the Issue #15 activation comment is the activation authority (same mechanism as Issue #14).

## 3. Exact changed paths (Issue #15 allowlist: new kernel modules + tests + diagnostics + documentation; no accepted path modified)

New:
1. `src/deep_learning_hank/ha_kernel/__init__.py`
2. `src/deep_learning_hank/ha_kernel/household.py`
3. `src/deep_learning_hank/ha_kernel/distribution.py`
4. `src/deep_learning_hank/ha_kernel/equilibrium.py`
5. `src/deep_learning_hank/ha_kernel/diagnostics.py`
6. `tests/test_dlh_3b_r2_kernel_household.py`
7. `tests/test_dlh_3b_r2_kernel_equilibrium.py`
8. `tests/test_dlh_3b_r2_kernel_accounting.py`
9. `tests/test_dlh_3b_r2_kernel_reproducibility.py`
10. `reports/dlh_3b_r2_ha_kernel_2026_08_20/DLH_3B_R2_IMPLEMENTATION_REVIEW.md`
11. `reports/dlh_3b_r2_ha_kernel_2026_08_20/DLH_3B_R2_EXECUTION_REPORT.md`
12. `reports/dlh_3b_r2_ha_kernel_2026_08_20/DLH_3B_R2_DIAGNOSTICS.csv`
13. `reports/dlh_3b_r2_ha_kernel_2026_08_20/DLH_3B_R2_REPRODUCIBILITY_SUMMARY.csv`
14. `reports/dlh_3b_r2_ha_kernel_2026_08_20/DLH_3B_R2_FORBIDDEN_OPERATION_CHECK.md`

**No accepted predecessor path modified** — Tier-0 / DLH-3A / DLH-3B / DLH-3C / DLH-3D / DLH-3D-R1A files byte-identical to fresh `origin/main` (the R1A audit branch is a separate branch). Accepted economics helpers (`preferences.py`, `grids.py`) reused read-only; accepted `hank_config.py` config class reused read-only; the accepted DLH-3B config is consumed read-only with SHA-256 verification at load.

## 4. Environment / reproducibility policy

- Python `3.11.9`; numpy `2.4.6`; scipy `1.17.1`; pytest `8.2.1` (all pre-existing; zero installs; no environment mutation; no GPU).
- OS: Windows (pwsh); deterministic single-threaded CPU execution.
- **Seed policy**: the kernel uses no random numbers; no seed is required. Determinism is exact (repeat differences `0.0`, measured).
- Configuration: `configs/dlh_3b_hank_steady_state_validation.toml`, SHA-256 `82AB4A02F9D08FBBAED1349BC027FACE5361B1AB24C710C4CEA6958481CD5FC1` (accepted DLH-3B fixture, verified at load by the kernel diagnostics layer).

## 5. Exact commands (all recorded)

1. `python %TEMP%\dlh3br2_probe.py` — accepted 3B steady-state runtime probe (6.9 s; baseline reproduced: `A_hh*=10.000000002223675`).
2. `python %TEMP%\dlh3br2_kernel_probe.py` — kernel equilibrium + diagnostics smoke test (7.5 s; all gates PASS, cross-check diffs 0.0).
3. `python -m pytest tests/test_dlh_3b_r2_kernel_household.py tests/test_dlh_3b_r2_kernel_equilibrium.py tests/test_dlh_3b_r2_kernel_accounting.py tests/test_dlh_3b_r2_kernel_reproducibility.py -v` — **11 passed / 0 failed** (57.0 s).
4. Accepted predecessor regression (Tier-0 2a/2b/2c + DLH-3B + DLH-3C): **97 passed / 0 failed** (195.9 s) — no regression; matches the accepted DLH-3D report's 97/0.
5. `python %TEMP%\dlh3br2_csv.py` — generated `DLH_3B_R2_DIAGNOSTICS.csv` and `DLH_3B_R2_REPRODUCIBILITY_SUMMARY.csv` (incl. a second full kernel solve pair; max repeat diff `0.0`).

## 6. Model evidence (Issue #15 §7 — Model)

- Equations implemented: see `DLH_3B_R2_IMPLEMENTATION_REVIEW.md` §1 (target equations: HJB, static labor FOC, KFE, production `Y=Z*N`, fiscal `tr=τ_l w N − r B`, clearing, residuals).
- State-space definition: `(a, z)` — one liquid risk-free real bond `a ∈ [0,100]` (401 pts), two-state CTMC `z ∈ {0.5, 1.5}` (rates 0.25/0.25); distribution `g(a,z)`.
- Asset accounting: `A_hh = ∫ a dg`, constant bond supply `B = 10`, single clearing `R_asset = A_hh − B`.

## 7. Numerical evidence (Issue #15 §7 — Numerical)

| Metric | Value | Frozen threshold | Verdict |
|---|---|---|---|
| HJB true residual | `6.758818837937497e-08` | `≤ 1e-7` (hjb_tolerance) | PASS |
| HJB converged | True | — | PASS |
| Labor KKT max | `2.609024107869118e-15` | `≤ 1e-7` | PASS |
| Consumption FOC max | `2.220446049250313e-16` | `≤ 1e-7` | PASS |
| Min consumption | `> 0` | `> 0` | PASS |
| Boundary drifts | lower `≥ -1e-12`; upper `≤ 1e-12` | state-constraint | PASS |
| Generator row-sum max abs | `≤ 1e-12` | `≤ 1e-12` | PASS |
| KFE mass error | `0.0` | `≤ 1e-10` | PASS |
| KFE minimum mass (non-negativity) | `0.0` | `≥ -1e-12` | PASS |
| Negative mass count / NaN count | `0` / `0` | `0` / `0` | PASS |
| Asset clearing residual `R_asset = A_hh − B` | `2.2236754659843427e-09` | `≤ 1e-6` | PASS |
| Labor clearing residual `R_labor = N_hh − N` | `5.502138744617469e-10` | `≤ 1e-6` | PASS |
| Goods residual | `-4.061235792107709e-10` | `≤ 1e-7` | PASS |
| Fiscal residual | `0.0` | `≤ 1e-12` | PASS |
| Profits residual | `0.0` | `≤ 1e-12` | PASS |
| Wealth-flow residual | `-1.1102230246251565e-15` | `≤ 1e-7` | PASS |
| Cross-check vs accepted 3B (`r*`, `N*`, `A_hh*`) | diffs `0.0` | `≤ 1e-6` | PASS |

All gates: **PASS** (`all_gates_pass = True`).

## 8. Reproducibility evidence (Issue #15 §7 — Reproducibility)

- Two identical kernel equilibrium solves: max abs repeat difference **`0.0`** for `r*`, `N*`, `A_hh*`, `N_hh*`, `C*`, value/consumption/labor policies, distribution mass, and root residuals (see `DLH_3B_R2_REPRODUCIBILITY_SUMMARY.csv`).
- Determinism is exact by construction (no RNG; deterministic brentq roots; identical inputs ⇒ identical outputs).

## 9. Test results

| Suite | Result |
|---|---|
| New kernel tests (4 files) | **11 passed / 0 failed** |
| Accepted predecessor regression (Tier-0 + DLH-3B + DLH-3C) | **97 passed / 0 failed** (no regression) |

## 10. Forbidden-operation check

See `DLH_3B_R2_FORBIDDEN_OPERATION_CHECK.md`. Summary: two-asset implementation 0 · Matlab translation claim 0 · China/province calibration 0 · NK block 0 · monetary shock 0 · regional HANK 0 · neural/RL/GPU 0 · Results claims 0 · modification of accepted paths 0 · parameter/fixture/tolerance tuning 0.

## 11. Evidence boundary

All evidence is D2 machine-diagnostic kernel validation evidence for the minimal single-region one-asset HANK validation kernel. Per Issue #15 §9, passing this task means the Python HA kernel is ready as a reproducible validation foundation; it does **not** mean genuine HANK dynamic validation, NK model validation, regional NSR-HANK validation, or empirical calibration. No policy/welfare/Results claims are drawn.

## 12. Recommendation (non-binding)

- The kernel cross-validation test (exact reproduction of the accepted DLH-3B steady state) should be reviewed independently.
- Future tasks may separately authorize extensions (NK dynamics, monetary innovation, regional structure, domain adequacy in DLH-3E) as new Issues.
