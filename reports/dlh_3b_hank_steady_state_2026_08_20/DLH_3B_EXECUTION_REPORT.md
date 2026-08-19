# DLH-3B — Minimal HANK Steady-State Structural Kernel / D2 Validation — Execution Report

- Date: 2026-08-20
- Author: DSH (bounded Builder)
- Authority: GitHub Issue #11 — `DLH-3B: Minimal HANK steady-state structural kernel and D2 validation` (state: OPEN)
- Accepted predecessor: Issue #10 / DLH-3A R1, accepted commit `f56a7c4058a32cc0a7bdc903cada98602a3706b1`
- Status: **CANDIDATE (scientific success)**. All mandatory Issue #11 gates PASS; acceptance requires fresh-GitHub independent review (ChatGPT).
- Evidence class: **D2 machine-diagnostic evidence** — `D2_MACHINE_DIAGNOSTIC__HANK_STEADY_STATE_STRUCTURAL_ONLY`. This is NOT full dynamic genuine-HANK validation; it is the zero-inflation / zero-shock steady-state structural kernel only.

## 1. Terminal classification

`DLH_3B_HANK_STEADY_STATE_STRUCTURAL_KERNEL_READY_FOR_GPT_REVIEW`

## 2. Baseline / Issue / branch / commit

- Fresh baseline `origin/main` SHA: `0afeae0a486ab56b859ed4792f47e9b0cb175b7f`
- Issue #11 title/status: `DLH-3B: Minimal HANK steady-state structural kernel and D2 validation` — OPEN
- Dedicated branch: `dsh/issue-11-dlh-3b-hank-steady-state-2026-08-20` (created from fresh `origin/main`)
- Candidate commit: single coherent commit at branch HEAD (2026-08-20, DSH); hash reported in the completion response. Expected delta: exactly the 16 allowlisted paths, 0 behind / 1 ahead.

## 3. Exact changed paths (16-path allowlist)

1. `configs/dlh_3b_hank_steady_state_validation.toml`
2. `src/deep_learning_hank/hank_config.py`
3. `src/deep_learning_hank/economics/hank_firm.py`
4. `src/deep_learning_hank/economics/hank_fiscal.py`
5. `src/deep_learning_hank/economics/hank_nominal.py`
6. `src/deep_learning_hank/solvers/hank_household_steady_state.py`
7. `src/deep_learning_hank/solvers/hank_steady_state.py`
8. `src/deep_learning_hank/diagnostics/hank_steady_state.py`
9. `tests/test_dlh_3b_household.py`
10. `tests/test_dlh_3b_equilibrium.py`
11. `tests/test_dlh_3b_accounting.py`
12. `tests/test_dlh_3b_reproducibility.py`
13. `reports/dlh_3b_hank_steady_state_2026_08_20/DLH_3B_EXECUTION_REPORT.md`
14. `reports/dlh_3b_hank_steady_state_2026_08_20/DLH_3B_DIAGNOSTICS.csv`
15. `reports/dlh_3b_hank_steady_state_2026_08_20/DLH_3B_ROOT_TRACE.csv`
16. `reports/dlh_3b_hank_steady_state_2026_08_20/DLH_3B_FORBIDDEN_OPERATION_CHECK.md`

**No other tracked path modified** — accepted Tier-0 modules/tests/configs/reports, accepted DLH-3A specifications, governance, README, roadmap, handoff all untouched (byte-identical to fresh `origin/main`). No `__init__.py` modified.

## 4. Environment / packages (zero installs)

- Python `3.11.9` (pre-existing); numpy `2.4.6`; scipy `1.17.1`; pytest `8.2.1` (all pre-existing; zero installs; no environment mutation; no GPU).
- OS: Windows (pwsh) — deterministic single-threaded CPU execution.

## 5. Exact commands

**Command 1 — single-household probe (engineering check):**
```
$env:PYTHONPATH = "D:\deep-learning-hank\src"
python %TEMP%\dlh3b_probe.py
```
(probe script: load `configs/dlh_3b_hank_steady_state_validation.toml`; solve the household HJB + stationary KFE at the fixed test candidate r=0.005, N=1.0; print gates.)

**Command 2 — full steady-state equilibrium solve + gate evaluation:**
```
$env:PYTHONPATH = "D:\deep-learning-hank\src"
python %TEMP%\dlh3b_solve.py
```
(loads the frozen config; `run_hank_steady_state(config)`; prints root objects, residuals, tail observations and all gate flags.)

**Command 3 — DLH-3B test suite:**
```
$env:PYTHONPATH = "D:\deep-learning-hank\src"
python -m pytest tests/test_dlh_3b_household.py tests/test_dlh_3b_accounting.py tests/test_dlh_3b_equilibrium.py tests/test_dlh_3b_reproducibility.py -v
```
Result: **23 passed, 0 failed.**

**Command 4 — full repository regression suite:**
```
$env:PYTHONPATH = "D:\deep-learning-hank\src"
python -m pytest tests -v
```
Result: **77 passed, 0 failed** (accepted Tier-0: 54 incl. Issue #7/#8 blocker-provenance and Issue #9 fixed-domain robustness; new DLH-3B: 23).

**Command 5 — diagnostics/root-trace capture + reproducibility capture:**
```
$env:PYTHONPATH = "D:\deep-learning-hank\src"
python %TEMP%\dlh3b_capture.py
```
Writes `DLH_3B_DIAGNOSTICS.csv` (single comprehensive row) and `DLH_3B_ROOT_TRACE.csv` (127 root-trace rows) and runs the full pipeline twice more for reproducibility evidence.

## 6. Attempt history (all materially distinct executions)

| # | Attempt | Outcome | Note |
|---|---|---|---|
| A | Command 1 probe (initial) | FAILED (IndexError) | Implementation bug in `solvers/hank_household_steady_state.py`: `q`/`b` were not broadcast to the full `(states, assets)` grid before the zero-drift policy call. Fixed by broadcasting (implementation-plumbing fix, §13). No frozen value changed. |
| B | Command 1 probe (re-run) | PASS | Household gates at the fixed candidate all hold; single solve ~0.25 s. |
| C | Command 2 full equilibrium | PASS | All Issue #11 gates PASS; primary brackets used (no scans). |
| D | Command 3 DLH-3B tests (run 1) | 3 FAILED | Test-side bugs only: array-shape misuse in `test_zero_drift_policy_foc`; wrong KKT expectation in `test_labor_policy_interior_and_kkt`; over-broad "shock" token check in the scope test. Test files fixed; no solver/economic/fixture change. |
| E | Command 3 DLH-3B tests (run 2) | PASS (23/23) | |
| F | Command 4 full suite | PASS (77/77) | Tier-0 regression intact. |
| G | Command 5 capture | PASS | CSVs written; reproducibility diffs all exactly 0.0. |

No economic value, asset domain/grid, root bracket/scan, or scientific threshold was altered at any point after the frozen config was created. Correct fail-closed blockers were never tuned away; none occurred at the final equilibrium.

## 7. Fixture and config hash

- Config: `configs/dlh_3b_hank_steady_state_validation.toml`
- Labels present: `VALIDATION_FIXTURE_NOT_CALIBRATION`; `HANK_STEADY_STATE_STRUCTURAL_ONLY`; `STARTING_DLH3B_DEVELOPMENT_DOMAIN_NOT_HANK_DOMAIN_ADEQUACY`.
- Config SHA-256: `82AB4A02F9D08FBBAED1349BC027FACE5361B1AB24C710C4CEA6958481CD5FC1`
- Frozen values (Issue #11 §11): annual; asset grid `[0,100]` 401 points; states `(0.5,1.5)` intensities `0.25/0.25`; `rho_hh=0.01`, `gamma=2.0`, `tau_l=0.15`; `frisch=1.0`, `chi=0.70`, `n_max=5.0`; `Z=1.0`, `epsilon=6.0`, `phi_p=100.0`; `phi_pi=1.5`, `pi_bar=0.0`, `epsilon_i=0.0`; `B=10.0`, `G=0.0`; labor bracket `[0.20,2.00]` scan `[0.05,4.00]` 80 pts; asset bracket `[-0.0200,0.0095]` scan `[-0.0300,0.0099]` 80 pts; root xtol `1e-9`, maxiter 200.

## 8. Nested root / bracket / scan evidence (Issue #11 §7)

- **Inner labor root** at fixed `r`: residual `R_labor(N) = N_hh - N`; primary bracket `[0.20, 2.00]` **sign-changed (finite endpoints)** — used directly, scan NOT needed; `inner_bracket_from_scan = False`.
- **Outer asset root**: residual `R_asset(r) = A_hh(r, N*(r)) - B`; primary bracket `[-0.0200, 0.0095]` **sign-changed (finite endpoints)** — used directly, scan NOT needed; `outer_bracket_from_scan = False`.
- Evaluation counts: outer evaluations = **13** (2 primary endpoints + 11 brentq callbacks); inner evaluations = **113** (across the 13 outer evaluations); total trace rows = **127** (113 inner + 13 outer + 1 final post-root verification).
- Every full `(r, N)` equilibrium evaluation is recorded in `DLH_3B_ROOT_TRACE.csv` (127 rows; stages `inner_primary_lower/upper`, `inner_scan`, `inner_brentq`, `outer_primary_lower/upper`, `outer_scan`, `outer_brentq`, `final`; every row finite at the final equilibrium, `hjb_converged=True`).
- Root tolerances: inner and outer `brentq` with `xtol = 1e-9`, `maxiter = 200`; both converged (`root_converged = True`).

## 9. Household / KKT diagnostics (Issue #11 §5.4, at the final equilibrium)

| Diagnostic | Value | Gate |
|---|---|---|
| HJB converged | True | required |
| True HJB residual | `6.758818837937497e-08` | `<= 1e-7` PASS |
| HJB iterations | 8 | — |
| min consumption | `0.6549011290706134` | `> 0` PASS |
| lower-boundary min drift | `0.0` | `>= -1e-12` PASS |
| upper-boundary max drift | `-0.11422254136378873` | `<= 1e-12` PASS |
| generator row-sum max abs | `4.440892098500626e-16` | `<= 1e-12` PASS |
| generator literal off-diag min | `0.0` | `>= -1e-14` PASS |
| labor KKT max violation | `2.609024107869118e-15` | `<= 1e-7` PASS |
| consumption-FOC max violation | `2.220446049250313e-16` | `<= 1e-7` PASS |
| NaN/Inf count | 0 | `= 0` PASS |

Household block: upwind HJB with **endogenous static labor** (control, not state), three-candidate Hamiltonian selection (zero-drift / forward / backward) with accepted Tier-0 state-constraint / no-outward-drift boundary semantics; zero-drift policy solved once per aggregate evaluation; labor KKT evaluated with the envelope marginal value `u'(c0)` for zero-drift-selected nodes (documented convention). All zero-drift nodes feasible at the equilibrium (`BLOCKED_DLH_3B_HOUSEHOLD_FEASIBILITY` not triggered).

## 10. Stationary KFE diagnostics (Issue #11 §6, at the final equilibrium)

| Diagnostic | Value | Gate |
|---|---|---|
| mass error | `0.0` | `<= 1e-10` PASS |
| stationarity residual | `1.2576745200831851e-15` | `<= 1e-8` PASS |
| minimum mass | `0.0` | `>= -1e-12` PASS |
| negative-mass count | 0 | `= 0` PASS |
| NaN/Inf count | 0 | `= 0` PASS |
| state-marginal error vs CTMC law `[0.5,0.5]` | `2.220446049250313e-16` | `<= 1e-8` PASS |

## 11. Final steady-state objects (Issue #11 §8)

- real liquid return `r* = 0.007370613883670197`;
- nominal rate `i* = r* = 0.007370613883670197` (`pi = 0`);
- aggregate effective labor `N* = 1.0656334480169984`;
- output `Y = Z*N = 1.0656334480169984`;
- real wage `w = Z/mu = 0.8333333333333334` (= 5/6);
- real marginal cost `mc = 1/mu = 0.8333333333333334`; markup `mu = 1.2`;
- profits `Pi = Y - w*N = 0.17760557466949967`;
- tax revenue `T = tau_l*w*N = 0.1332041810021248`;
- lump-sum transfer `tr = T - r*B = 0.05949804216542284`;
- aggregate liquid assets `A_hh = 10.000000002223675`;
- household aggregate labor `N_hh = 1.0656334485672123`;
- aggregate consumption `C = 1.065633448423122`.

## 12. Clearing / accounting / nominal residuals (Issue #11 §8.1–8.3)

| Residual | Value | Gate |
|---|---|---|
| `R_asset = A_hh - B` | `2.2236754659843427e-09` | `<= 1e-7` PASS |
| `R_labor = N_hh - N` | `5.502138744617469e-10` | `<= 1e-7` PASS |
| `R_goods = Y - C` (pi=0, G=0) | `-4.061235792107709e-10` | `<= 1e-7` PASS |
| `R_fiscal = T - r*B - tr` | `0.0` | `<= 1e-12` PASS |
| `R_profits = Pi - (Y - w*N)` | `0.0` | `<= 1e-12` PASS |
| `R_wealth = (1-tau_l)w*N + r*A_hh + tr + Pi - C` | `-3.897338007874396e-10` | `<= 1e-7` PASS |
| `R_nkpc = pi_dot - rho*pi + (eps/phi_p)(mc - 1/mu)` | `0.0` | `<= 1e-12` PASS |
| `R_fisher = i - r - pi` | `0.0` | `<= 1e-12` PASS |
| `R_taylor = i - [r_bar + pi_bar + phi_pi*(pi-pi_bar) + eps_i]` | `0.0` | `<= 1e-12` PASS |

Wealth-flow consistency chain verified: `C = w*N + Pi = Y` (all within `1e-7` absolute).

## 13. Positivity / finiteness (Issue #11 §8.4)

`Y, N, C, w, B, A_hh` all strictly positive and finite; `r` finite; `tr, Pi, i` finite. PASS.

## 14. Boundary / tail observations (Issue #11 §8.5 — gross-truncation sanity only, NOT domain adequacy)

- upper-boundary mass = `0.0` (`<= 1e-3` PASS);
- top-5%-of-grid mass = `0.0` (observation);
- lower-boundary mass = `0.013148618861405796` (observation: 1.31% of mass at the borrowing constraint `a=0`);
- `A_hh / a_max = 0.10000000002223676`.

This is a **provisional gross-truncation sanity gate only**. It does NOT establish final HANK asset-domain/grid adequacy; DLH-3E must re-establish that separately.

## 15. Deterministic reproducibility (Issue #11 §9)

Full pipeline run twice in the same environment; max absolute repeat differences:

| Object | diff |
|---|---|
| `r*`, `i*`, `N`, `Y`, `w`, `tr`, `Pi`, `C`, `A_hh` | all `0.0` |
| value, consumption, labor, drift | all `0.0` |
| distribution mass | `0.0` |
| full scalar diagnostic vector | `0.0` |
| **max over all** | **`0.0`** |

All `<= 1e-12`. `BLOCKED_DLH_3B_REPRODUCIBILITY_THRESHOLD` not triggered.

## 16. Regression (Issue #11 §10)

Full repository suite: **77 passed / 0 failed** (90.7 s). Accepted Tier-0 tests unchanged and passing (54, incl. Issue #7/#8 blocker-provenance and Issue #9 fixed-domain grid tests); new DLH-3B tests passing (23). Accepted Tier-0 modules/configs/reports/tests not modified. `BLOCKED_DLH_3B_REGRESSION` not triggered.

## 17. Forbidden-operation counters (all zero)

See `DLH_3B_FORBIDDEN_OPERATION_CHECK.md`. Summary: accepted Tier-0 mutation 0 · accepted DLH-3A spec mutation 0 · time-dependent HJB/KFE 0 · transition path 0 · monetary/TFP/fiscal shock or IRF 0 · regional/W^L/W^K/W^G 0 · multi-region code 0 · neural/RL/training/GPU 0 · empirical calibration/data/regression 0 · legacy Matlab / old Python reference repo / private Zotero 0 · Results/policy/welfare/novelty claims 0 · governance mutation 0 · PR / merge / Issue close / successor / self-accept 0.

## 18. Evidence boundary

This result supports only **D2 machine diagnostics for the minimal single-region HANK steady-state structural kernel** under the explicit frozen validation fixture (`VALIDATION_FIXTURE_NOT_CALIBRATION`). It does NOT establish: dynamic HANK monetary transmission; time-dependent household/KFE validity; empirical calibration; final HANK domain/grid robustness (DLH-3E); regional NSR-HANK; learned networks; policy/Results/welfare; novelty. DLH-3C remains separately gated even after a successful 3B.

## 19. Recommendation (non-binding)

If this Issue passes independent review, a separate successor Issue may authorize DLH-3C (time-dependent household/KFE response under externally prescribed small paths). DSH does not create or propose 3C authority beyond this non-binding recommendation.
