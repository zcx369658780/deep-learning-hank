# DLH-3C — Time-Dependent Household HJB/KFE Response Under Prescribed Small Paths — Execution Report

- Date: 2026-08-20
- Author: DSH (bounded Builder)
- Authority: GitHub Issue #12 — `DLH-3C: Time-dependent household HJB/KFE response under prescribed small paths` (state: OPEN)
- Accepted predecessor: Issue #11 / DLH-3B, accepted commit `267fef0386098796c06f4b7bf331121af9061a43`, classification `DLH_3B_HANK_STEADY_STATE_STRUCTURAL_KERNEL_ACCEPTED_WITH_OBSERVATIONS`
- Status: **CANDIDATE (scientific success)**. All mandatory Issue #12 gates PASS; acceptance requires fresh-GitHub independent review (ChatGPT).
- Evidence class: **D2 machine-diagnostic evidence** — `D2_MACHINE_DIAGNOSTIC__HANK_TIME_DEPENDENT_HOUSEHOLD_KFE_ONLY`. This is NOT full dynamic genuine-HANK validation; aggregate NK GE remains deliberately open.

## 1. Terminal classification

`DLH_3C_TIME_DEPENDENT_HOUSEHOLD_KFE_RESPONSE_READY_FOR_GPT_REVIEW`

## 2. Baseline / Issue / branch / commit

- Fresh baseline `origin/main` SHA: `371129e7ab4928ab0753eff0d2c74c934a430e0f`
- Issue #12 title/status: `DLH-3C: Time-dependent household HJB/KFE response under prescribed small paths` — OPEN
- Dedicated branch: `dsh/issue-12-dlh-3c-time-dependent-household-kfe-2026-08-20` (created from fresh `origin/main`)
- Candidate commit: single coherent commit at branch HEAD (2026-08-20, DSH); hash reported in the completion response. Expected delta: exactly the 14 allowlisted paths, 0 behind / 1 ahead.

## 3. Exact changed paths (14-path allowlist)

1. `configs/dlh_3c_hank_transition_validation.toml`
2. `src/deep_learning_hank/hank_transition_config.py`
3. `src/deep_learning_hank/solvers/hank_household_transition.py`
4. `src/deep_learning_hank/solvers/hank_kfe_transition.py`
5. `src/deep_learning_hank/diagnostics/hank_transition.py`
6. `tests/test_dlh_3c_zero_path.py`
7. `tests/test_dlh_3c_prescribed_paths.py`
8. `tests/test_dlh_3c_mass_boundary.py`
9. `tests/test_dlh_3c_horizon_reproducibility.py`
10. `reports/dlh_3c_hank_transition_2026_08_20/DLH_3C_EXECUTION_REPORT.md`
11. `reports/dlh_3c_hank_transition_2026_08_20/DLH_3C_PATH_DIAGNOSTICS.csv`
12. `reports/dlh_3c_hank_transition_2026_08_20/DLH_3C_AMPLITUDE_HORIZON_SUMMARY.csv`
13. `reports/dlh_3c_hank_transition_2026_08_20/DLH_3C_REPRODUCIBILITY_SUMMARY.csv`
14. `reports/dlh_3c_hank_transition_2026_08_20/DLH_3C_FORBIDDEN_OPERATION_CHECK.md`

**No other tracked path modified** — accepted Tier-0, DLH-3A and DLH-3B paths (incl. all accepted predecessor tests) are byte-identical to fresh `origin/main`. No `__init__.py` modified.

## 4. Environment / packages (zero installs)

- Python `3.11.9` (pre-existing); numpy `2.4.6`; scipy `1.17.1`; pytest `8.2.1` (all pre-existing; zero installs; no environment mutation; no GPU).
- OS: Windows (pwsh) — deterministic single-threaded CPU execution.

## 5. Accepted DLH-3B baseline identity (Issue #12 §4)

- Fresh-main `configs/dlh_3b_hank_steady_state_validation.toml` SHA-256: `82AB4A02F9D08FBBAED1349BC027FACE5361B1AB24C710C4CEA6958481CD5FC1` — **matches the Issue-specified frozen value exactly** (verified at load and in test `test_baseline_identity_is_frozen`). `BLOCKED_DLH_3C_BASELINE_IDENTITY_MISMATCH` not triggered.
- Baseline recomputed through the accepted DLH-3B interfaces (`run_hank_steady_state_cached`), not hard-coded:
  - `r* = 0.007370613883670197`, `N* = 1.0656334480169984`, `Y* = 1.0656334480169984`;
  - `w* = 5/6`, `tr* = 0.05949804216542284`, `Pi* = 0.17760557466949967`;
  - `A_hh* = 10.000000002223675` vs `B = 10`, `N_hh* = 1.0656334485672123`, `C* = 1.065633448423122`.

## 6. Transition config hash

- Config: `configs/dlh_3c_hank_transition_validation.toml`
- SHA-256: `C7AA76DF3758F46FCBA827872FC0FD0078EDD5309CCFAD04E32C42F5CB4D39A2`
- Labels: `VALIDATION_FIXTURE_NOT_CALIBRATION`; `EXOGENOUS_NUMERICAL_RESPONSE_PATH_NOT_STRUCTURAL_SHOCK`; `D2_MACHINE_DIAGNOSTIC__HANK_TIME_DEPENDENT_HOUSEHOLD_KFE_ONLY`.

## 7. Time grid / horizons / prescribed paths (Issue #12 §5)

- Primary horizon `T = 12.0`; `dt = 0.05`; grid `t_k = k*dt`, `k = 0..240` (both endpoints included); long horizon `T_long = 16.0` with the **same `dt`** (no time-step refinement claim).
- Bump: `h(t) = sin(pi*t/5)^2` on `[0, 5]`, exactly `0` otherwise; zero at `t=0`, zero for `t >= 5` (terminal region back at baseline).
- **Path W** (wage-only): `w_t = w*·(1 + eta_w·amp·h(t))`, `r_t = r*`, `tr_t = tr*`, `Pi_t = Pi*`; `eta_w = 0.002`.
- **Path R** (real-return-only): `r_t = r* + eta_r·amp·h(t)`, `w_t = w*`, `tr_t = tr*`, `Pi_t = Pi*`; `eta_r = 0.001`.
- Amplitude sequence per family: full `1.0`, half `0.5`, quarter `0.25`, zero `0.0`; no other amplitude search.

## 8. Exact commands

**Command 1 — engine probe:**
```
$env:PYTHONPATH = "D:\deep-learning-hank\src"
python %TEMP%\dlh3c_probe.py
```
(baseline load + zero/W/R full-amplitude single-path runs; per-path gates.)

**Command 2 — full transition validation:**
```
$env:PYTHONPATH = "D:\deep-learning-hank\src"
python %TEMP%\dlh3c_solve.py
```
(`run_transition_validation(config)`; prints zero-invariance, amplitude, horizon, HJB/KFE global gates.)

**Command 3 — DLH-3C test suite:**
```
$env:PYTHONPATH = "D:\deep-learning-hank\src"
python -m pytest tests/test_dlh_3c_zero_path.py tests/test_dlh_3c_prescribed_paths.py tests/test_dlh_3c_mass_boundary.py tests/test_dlh_3c_horizon_reproducibility.py -v
```
Result: **20 passed, 0 failed.**

**Command 4 — full repository regression suite:**
```
$env:PYTHONPATH = "D:\deep-learning-hank\src"
python -m pytest tests -v
```
Result: **97 passed, 0 failed** (accepted Tier-0 54 + accepted DLH-3B 23 + new DLH-3C 20).

**Command 5 — CSV capture + reproducibility capture:**
```
$env:PYTHONPATH = "D:\deep-learning-hank\src"
python %TEMP%\dlh3c_capture.py
```
Writes `DLH_3C_PATH_DIAGNOSTICS.csv` (2169 rows = 9 runs x 241 time points), `DLH_3C_AMPLITUDE_HORIZON_SUMMARY.csv`, `DLH_3C_REPRODUCIBILITY_SUMMARY.csv`, and re-runs the complete primary validation set twice for reproducibility evidence.

## 9. Attempt history (all materially distinct executions)

| # | Attempt | Outcome | Note |
|---|---|---|---|
| A | Command 1 probe | PASS | Baseline identity verified; zero/W/R single-path runs pass per-path gates; ~2.3 s per path run. |
| B | Command 2 full validation | PASS | All Issue #12 gates PASS (see §11–§15). |
| C | Command 3 DLH-3C tests | PASS (20/20) | |
| D | Command 4 full suite | PASS (97/97) | Predecessor regression intact. |
| E | Command 5 capture | PASS | CSVs written; reproducibility max diff exactly `0.0`. |

No time-grid/path-amplitude/horizon value or scientific threshold was altered after the frozen config was created; no fail-closed blocker was tuned away; no blockers occurred at the final validation.

## 10. Backward-HJB numerical method (Issue #12 §6)

- Terminal condition `V(T, a, z) = V_ss` (accepted DLH-3B value function); terminal region inputs are baseline because the forcing is exactly zero after year 5.
- Implicit backward step `[(rho + 1/dt) I - G_k] V_k = u_k - v_k + V_{k+1}/dt`; within-step **policy iteration** (value tolerance `1e-8`, max 200 iterations per step) using **the same state-constraint / upwind / zero-drift / endogenous-static-labor semantics as the accepted DLH-3B household kernel** (read-only reuse of its policy/generator/KKT helpers; the accepted module was not modified). The household HJB is not linearized.
- Global HJB diagnostics across all runs: residual max `1.82e-12` (`<= 1e-6`), labor KKT max `3.22e-15` (`<= 1e-6`), consumption-FOC max `2.22e-16` (`<= 1e-6`), min consumption `> 0` everywhere, boundary drifts (lower `>= -1e-12`, upper `<= 1e-12`), generator row-sum max `<= 1e-12`, literal off-diagonal min `>= -1e-14`, NaN/Inf count `0` on every path. Within-step policy iterations: mean ~1.0–1.4, max 2 on the primary paths (the zero-drift-consistent initial guess is close to the fixed point). `BLOCKED_DLH_3C_BACKWARD_HJB_GATE` not triggered.

## 11. Forward-KFE method and diagnostics (Issue #12 §7)

- Initial distribution `g(0) = g_ss` (accepted DLH-3B stationary distribution); implicit forward step `[I - dt*G_k^T] g_{k+1} = g_k` with **no mass renormalization** (mass conservation emerges from the generator/discretization).
- Global KFE diagnostics across all runs: max mass error `1.78e-15` (`<= 1e-10`), min mass `0.0` (`>= -1e-12`), negative-mass count `0`, NaN/Inf count `0`. State marginals reproduce the symmetric CTMC stationary law `[0.5, 0.5]` within `1e-8` at every time point of every run. `BLOCKED_DLH_3C_FORWARD_KFE_GATE` not triggered.

## 12. Zero-path invariance (Issue #12 §8)

Zero-amplitude engine on the primary grid vs accepted steady state (max absolute deviations over all time points):

| Object | observed | gate |
|---|---|---|
| `V_t - V_ss` | `7.56e-07` | `<= 1e-5` PASS |
| `c_t - c_ss` | `5.33e-09` | `<= 1e-4` PASS |
| `n_t - n_ss` | `4.99e-09` | `<= 1e-4` PASS |
| `drift_t - drift_ss` | `9.68e-09` | `<= 1e-4` PASS |
| `g_t - g_ss` (elementwise) | `4.78e-11` | `<= 1e-6` PASS |
| `A_hh(t) - A_hh*` | `2.24e-08` | `<= 1e-5` PASS |
| `N_hh(t) - N_hh*` | `3.42e-09` | `<= 1e-5` PASS |
| `C(t) - C*` | `1.67e-09` | `<= 1e-5` PASS |

`BLOCKED_DLH_3C_ZERO_PATH_INVARIANCE` not triggered.

## 13. Nontrivial response + amplitude-to-zero / local scaling (Issue #12 §9)

Response vector `x_eta = [A_hh-A_zero, N_hh-N_zero, C-C_zero]`, `M(eta) = maxabs(x_eta)`:

| Metric | Path W | Path R | Gate |
|---|---|---|---|
| `M(full)` | `6.43717e-03` | `2.94662e-02` | `> 1e-8` nontrivial PASS |
| `M(half)` | `3.21758e-03` | `1.47223e-02` | `M(full) > M(half)` PASS |
| `M(quarter)` | `1.60854e-03` | `7.35843e-03` | `M(half) > M(quarter) > 0` PASS |
| `M(quarter)/M(full)` | `0.2499` | `0.2497` | `<= 0.40` PASS |
| `E_half` | `1.56338e-04` | `3.70051e-04` | `<= 0.10` PASS |

Local-scaling diagnostic: the half-amplitude response differs from `0.5 x_full` by at most ~`1.6e-4` (W) / `3.7e-4` (R) relative to `M(full)` — a numerical local-response diagnostic only, not an economic linearity theorem. `BLOCKED_DLH_3C_AMPLITUDE_TO_ZERO_GATE` not triggered.

## 14. Horizon / terminal robustness (Issue #12 §10)

Full-amplitude Path W / Path R, `T_long=16` vs `T=12`, same `dt=0.05`, identical forcing on `[0,5]`, common window `0 <= t <= 8` (max absolute aggregate differences):

| Aggregate | Path W | Path R | Gate |
|---|---|---|---|
| `A_hh` | `8.83e-09` | `8.84e-09` | `<= 1e-4` PASS |
| `N_hh` | `9.34e-10` | `9.35e-10` | `<= 1e-4` PASS |
| `C` | `4.44e-10` | `4.44e-10` | `<= 1e-4` PASS |

Long-horizon runs also satisfy all HJB/KFE gates. `BLOCKED_DLH_3C_HORIZON_TERMINAL_ROBUSTNESS` not triggered. No time-step refinement performed or claimed.

## 15. Deterministic reproducibility (Issue #12 §11)

The complete primary validation set (zero path; Path W full/half/quarter; Path R full/half/quarter; both long-horizon full-amplitude runs) was executed twice in the same environment. Max absolute repeat differences for all time grids, prescribed input paths, value/consumption/labor/drift paths, distribution-mass paths, `A_hh/N_hh/C` paths, and all scalar diagnostics/summary metrics: **exactly `0.0`** (`<= 1e-12`). See `DLH_3C_REPRODUCIBILITY_SUMMARY.csv`. `BLOCKED_DLH_3C_REPRODUCIBILITY_THRESHOLD` not triggered.

## 16. Regression (Issue #12 §12)

Full repository suite: **97 passed / 0 failed** (169.8 s). Accepted Tier-0 tests (54, incl. Issue #7/#8 blocker-provenance and Issue #9 fixed-domain), accepted DLH-3B tests (23) and new DLH-3C tests (20) all pass; no accepted predecessor test was edited. `BLOCKED_DLH_3C_REGRESSION` not triggered.

## 17. Forbidden-operation counters (all zero)

See `DLH_3C_FORBIDDEN_OPERATION_CHECK.md`. Summary: accepted Tier-0/DLH-3A/DLH-3B mutation 0 · structural monetary/TFP/fiscal shock 0 · `epsilon_i != 0` 0 · full NK GE closure 0 · NKPC/inflation feedback 0 · IRF terminology/policy interpretation 0 · dynamic market-clearing claims 0 · time-step robustness claims 0 · regional/W^L/W^K/W^G 0 · neural/RL/GPU 0 · empirical calibration/data/regression 0 · legacy Matlab / old Python reference repo / private Zotero 0 · Results/policy/welfare/novelty claims 0 · governance mutation 0 · PR/merge/Issue close/successor/self-accept 0.

## 18. Evidence boundary

This result supports only **D2 machine diagnostics for the time-dependent household backward-HJB + forward-KFE engine under the frozen prescribed non-structural real paths** (`EXOGENOUS_NUMERICAL_RESPONSE_PATH_NOT_STRUCTURAL_SHOCK`). It does NOT establish: dynamic HANK monetary transmission; NK general-equilibrium closure; IRFs or policy implications; empirical calibration; HANK domain/time-grid robustness (DLH-3E); regional NSR-HANK; learned networks; Results/novelty. DLH-3D (full NK GE + first deterministic monetary innovation through `epsilon_i`) remains separately gated.

## 19. Recommendation (non-binding)

If this Issue passes independent review, a separate successor Issue may authorize DLH-3D (NK GE closure + first small deterministic monetary-policy innovation). DSH does not create or propose 3D authority beyond this non-binding recommendation.
