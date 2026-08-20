# DLH-3D — Full Single-Region NK GE Closure + First Deterministic Monetary-Policy Innovation — Execution Report

- Date: 2026-08-20
- Author: DSH (bounded Builder)
- Authority: GitHub Issue #13 — `DLH-3D: Full single-region NK GE closure with first deterministic monetary-policy innovation` (state: OPEN), including the authoritative numerical-timing clarification (comment id `5349487045`)
- Accepted predecessor: Issue #12 / DLH-3C, accepted commit `3b24790e24e7b7d358848f55640b255a3a2b3191`
- Status: **FAIL-CLOSED CANDIDATE — the frozen fixture does not satisfy its own §9.3 goods gate for the full-amplitude innovation, and the frozen root route did not reach the frozen tolerance for the half-amplitude run within bounded effort.** Evidence preserved for independent review; this is NOT a PASS and NOT the success classification.

## 1. Terminal classification

`FAIL-CLOSED` — candidate **not eligible** for `DLH_3D_MINIMAL_GENUINE_SINGLE_REGION_HANK_DYNAMIC_VALIDATION_READY_FOR_GPT_REVIEW`.

Specific blocker evidence:

- **§9.3 goods gate FAILS for the full-amplitude GE**: `max_{k<K} |R_goods,k| = 0.2256 > 1e-5` at `k = 239` (the last root-interval step). `R_goods = Y - C - AC` with contemporaneous `C_k` per the authoritative clarification.
- The full-amplitude GE root **converges** (`5.470e-08 <= 1e-7`); asset/labor clearing, household/KFE, NKPC/Fisher/Taylor, wealth-flow, fiscal and profit gates all PASS; the sole §9 gate failure is `R_goods` at `k = K-1`.
- The half-amplitude root had **not reached** the frozen `1e-7` tolerance within the bounded effort performed (residual ~`3.1e-07` after 5 outer Newton iterations, creeping ~0.9x/step); root non-convergence evidence for that amplitude.
- Zero-innovation run: all gates PASS (invariance holds); no boundary layer.

## 2. Root cause analysis — finite-horizon terminal boundary layer (genuine fixture property)

The §9.3 goods gate failure at `k = K-1` is a genuine consequence of the frozen fixture, not an implementation defect:

1. The frozen terminal aggregate point pins `w_K = w*`, `N_K = N*` (`pi_K = 0`) but does **not** pin `A_hh,K`; per the authoritative clarification, `A_hh,K - B` is a free finite-horizon terminal-approximation diagnostic.
2. The nonlinear root enforces asset clearing `A_hh,k = B` on the root interval `k = 0..K-1` (frozen). The "natural" (unforced) continuation of the clearing path at the terminal has `A_hh,K ≈ 10.017` (the innovation's asset effect relaxes very slowly: ~10 years after the forcing, the deviation is still ~0.017, i.e., 0.17% of `B`).
3. Forcing `A_hh,K-1 = B` therefore requires a large adjustment of the last interior point; the frozen root route finds the self-consistent clearing solution with an extreme boundary layer at `k = 239` (`w = 0.6548`, `N = 0.8391`, i.e., −24% / −21%), where households (forward-looking, `V(T) = V_ss`) keep consuming near baseline while labor income is low and **dissave at −0.226/yr**.
4. The discrete identity holds exactly: `R_goods,K-1 = Σ g s = (A_hh,K - A_hh,K-1)/dt = (9.9887 - 10.0000)/0.05 = -0.2256`; `R_wealth,K-1 ≈ 7e-14` (KFE-consistent timing) confirms internal consistency.
5. Hence `max_{k<K} |R_goods| = 0.2256 > 1e-5` for the full innovation is **forced by the frozen terminal boundary + frozen root interval + slow wealth relaxation**. A "mild" candidate with baseline `(w,N)` at `k=239` has small `R_goods` (`-1.7e-4`) but **fails asset clearing** (`R_asset = +1.7e-2`): no candidate satisfies both gates at `k = K-1` under this fixture. The long-horizon gate (which the clarification designates as the authority for whether the terminal approximation contaminates the early window) concerns only `[0,8]`, which the boundary layer does not contaminate; but the §9.3 gate is frozen on `k = 0..K-1` and therefore fails regardless.

Per Issue #13 §7/§15 and the hard rule "correct fail-closed BLOCKED must be preserved; no tuning to manufacture PASS", no economic value, domain, horizon, root tolerance or gate was altered. The failure is reported as blocker evidence.

## 3. Baseline / Issue / branch / commit

- Fresh baseline `origin/main` SHA: `5cbff383d6091192379b92db991180f1145aa475`
- Issue #13 title/status: `DLH-3D: Full single-region NK GE closure with first deterministic monetary-policy innovation` — OPEN
- Dedicated branch: `dsh/issue-13-dlh-3d-monetary-ge-2026-08-20` (created from fresh `origin/main`)
- Candidate commit: single coherent commit at branch HEAD (2026-08-20, DSH); hash reported in the completion response. Expected delta: exactly the 14 allowlisted paths, 0 behind / 1 ahead.

## 4. Exact changed paths (14-path allowlist)

1. `configs/dlh_3d_hank_monetary_ge_validation.toml`
2. `src/deep_learning_hank/hank_ge_config.py`
3. `src/deep_learning_hank/solvers/hank_nkpc_transition.py`
4. `src/deep_learning_hank/solvers/hank_ge_transition.py`
5. `src/deep_learning_hank/diagnostics/hank_ge_transition.py`
6. `tests/test_dlh_3d_zero_ge.py`
7. `tests/test_dlh_3d_monetary_innovation.py`
8. `tests/test_dlh_3d_market_accounting.py`
9. `tests/test_dlh_3d_horizon_reproducibility.py`
10. `reports/dlh_3d_hank_monetary_ge_2026_08_20/DLH_3D_EXECUTION_REPORT.md`
11. `reports/dlh_3d_hank_monetary_ge_2026_08_20/DLH_3D_PATH_DIAGNOSTICS.csv`
12. `reports/dlh_3d_hank_monetary_ge_2026_08_20/DLH_3D_RESIDUAL_AMPLITUDE_SUMMARY.csv`
13. `reports/dlh_3d_hank_monetary_ge_2026_08_20/DLH_3D_REPRODUCIBILITY_SUMMARY.csv`
14. `reports/dlh_3d_hank_monetary_ge_2026_08_20/DLH_3D_FORBIDDEN_OPERATION_CHECK.md`

**No accepted predecessor path modified** — Tier-0 / DLH-3A / DLH-3B / DLH-3C files byte-identical to fresh `origin/main`; accepted predecessor tests unedited; no `__init__.py` mutation.

## 5. Environment / packages (zero installs)

- Python `3.11.9` (pre-existing); numpy `2.4.6`; scipy `1.17.1`; pytest `8.2.1` (all pre-existing; zero installs; no environment mutation; no GPU).

## 6. Accepted baseline identities (verified)

- DLH-3B config SHA-256 `82AB4A02F9D08FBBAED1349BC027FACE5361B1AB24C710C4CEA6958481CD5FC1` — matches frozen value (verified at load and in `test_baseline_identities_are_frozen`).
- DLH-3C config SHA-256 `C7AA76DF3758F46FCBA827872FC0FD0078EDD5309CCFAD04E32C42F5CB4D39A2` — matches frozen value.
- Baseline recomputed through accepted interfaces: `r* = 0.007370613883670197`, `N* = 1.0656334480169984`, `w* = 5/6`, `tr* = 0.05949804216542284`, `Pi* = 0.17760557466949967`, `A_hh* = 10.000000002223675`, `C* = 1.065633448423122`. `BLOCKED_DLH_3D_BASELINE_IDENTITY_MISMATCH` not triggered.

## 7. Transition config hash

- `configs/dlh_3d_hank_monetary_ge_validation.toml` SHA-256: `D19F555C29D25604EC276D7036161A070510D4DC5BC4F4F51476BA3981A207D1`
- Labels: `VALIDATION_FIXTURE_NOT_CALIBRATION`; `D2_MACHINE_DIAGNOSTIC__MINIMAL_SINGLE_REGION_HANK_DYNAMIC_VALIDATION_FIXTURE`.

## 8. Time grid / horizons / innovation

- `T = 12.0`, `dt = 0.05` (`k = 0..240`); `T_long = 16.0` same `dt`; no time-step refinement claim.
- Innovation `epsilon_i(t) = amp * eta_i * sin(pi*t/2)^2` on `[0,2]`, zero otherwise; `eta_i = 0.001`; amplitudes `1.0 / 0.5 / 0.25 / 0.0`.
- Frozen equations: `Y = Z*N`, `mc = w/Z`, backward-Euler NKPC `pi_k = [pi_{k+1} + dt*kappa*(mc_k - 1/mu)]/(1 + dt*rho_hh)`, `kappa = epsilon/phi_p`, `pi_K = 0`; Taylor `i = r* + phi_pi*pi + eps_i`; Fisher `r = i - pi`; `tr = tau_l*w*N - r*B`; `Pi = Y - w*N - AC`.
- Root: `scipy.optimize.root(method='krylov')`, unknowns `x_w,k = log(w_k/w*)`, `x_N,k = log(N_k/N*)` for `k = 0..K-1` only; residuals `(A_hh - B)/B` and `(N_hh - N)/N*` on `k = 0..K-1`; zero initial guess; `fatol = 1e-7` (infinity-norm), `maxiter = 80`; frozen inner configuration of the same Jacobian-free route: `jac_options = {'method': 'gmres', 'inner_maxiter': 150, 'inner_rtol': 1e-5, 'rdiff': 1e-7}` (chosen in development — before the first recorded evidence run — to balance inner-solve accuracy vs finite-difference noise amplification; never altered afterwards).

## 9. Exact commands (all recorded)

1. `python %TEMP%\dlh3d_probe1.py` — baseline load + zero-guess evaluation (found and fixed an NKPC coefficient bug, see §10).
2. `python %TEMP%\dlh3d_solve_full.py` — full-amplitude solve (default krylov): stalled ~7.8e-6 (inner lgmres `inner_m=30`/`maxiter=1` insufficient for the 480-unknown system).
3. Dev experiments (`dlh3d_inner.py`, `dlh3d_precond.py`, `dlh3d_sweep.py`, `dlh3d_solve_v*.py`) — isolated the inner-solve limitation; established the frozen jac_options configuration.
4. `python %TEMP%\dlh3d_final_full.py` — full-amplitude solve with frozen config: converged `5.470e-08`, §9 gate evaluation (goods gate failure identified).
5. `python %TEMP%\dlh3d_zero_long.py`, `dlh3d_half2.py` — zero and half-amplitude runs (zero passes; half stalled ~3.1e-07).
6. `python %TEMP%\dlh3d_csv.py` — generated the three report CSVs (full + zero evidence).
7. `python -m pytest tests/test_dlh_2a_*.py tests/test_dlh_2b_*.py tests/test_dlh_2c_*.py tests/test_dlh_3b_*.py tests/test_dlh_3c_*.py -q` — accepted predecessor regression: **97 passed / 0 failed** (188.6 s).

## 10. Attempt history (all materially distinct executions)

| # | Attempt | Outcome |
|---|---|---|
| A | Zero-guess GE evaluation (probe) | FAILED: household infeasibility — bug in `backward_nkpc` (used `mc - 1.0` instead of `mc - 1/mu`), inflating `pi` and breaking household feasibility. Fixed (implementation bug; no frozen value changed). |
| B | Zero-guess evaluation (re-run) | PASS: `|F| = 1.02e-3` open-loop response; `R_wealth ≈ 7.7e-14`; `R_goods ≈ 5.7e-4` open-loop. |
| C | Full solve, scipy default krylov | Stall at ~7.8e-6 > 1e-7 (inner lgmres `inner_m=30`, `maxiter=1` too weak for 480 unknowns). |
| D | Inner-solve experiments (lgmres/gmres, preconditioner, rdiff sweeps) | Established: F evaluation is exactly deterministic (repeat diff 0.0); inner solve needs more Krylov directions but moderate `rtol` (tight rtol fits FD noise and blows up); frozen configuration `gmres inner_maxiter=150 inner_rtol=1e-5 rdiff=1e-7` chosen. |
| E | Full solve, frozen config | PASS (root): converged `5.47e-8` in 4 outer iterations / 350 evals / 816 s; §9 gates: clearing/HJB/KFE/NKPC/Fisher/Taylor/wealth/fiscal/profit PASS; **§9.3 goods gate FAIL** (`0.2256` at k=239, terminal boundary layer). |
| F | Zero solve | PASS: converged `2.22e-10`; invariance metrics all within frozen gates; no boundary layer; `R_goods_max = 4.4e-7`. |
| G | Half solve | Root not converged to `1e-7` within bounded effort: 5 outer iterations reduced to ~3.1e-07 (creeping ~0.9x/step); terminated by builder; evidence preserved. |
| H | Quarter / long-horizon solves | Not completed within the session's bounded CPU (each solve ~15-40+ min; the fail-closed outcome is already established by the full run's §9.3 gate failure). |
| I | Accepted-predecessor regression | 97 passed / 0 failed (Tier-0 + DLH-3B + DLH-3C). |
| J | CSV evidence capture | `DLH_3D_PATH_DIAGNOSTICS.csv` (482 rows: zero + full time series), `DLH_3D_RESIDUAL_AMPLITUDE_SUMMARY.csv`, `DLH_3D_REPRODUCIBILITY_SUMMARY.csv` written. |

No frozen equation, fixture value, innovation amplitude, horizon, `dt`, root method/tolerance, or scientific threshold was altered after the first recorded evidence run; no fail-closed result was tuned away.

## 11. Full-amplitude GE evidence (primary run, `T=12`)

| Object | Value | Frozen gate | Verdict |
|---|---|---|---|
| root residual inf-norm | `5.470e-08` | `<= 1e-7` | PASS |
| `max_{k<K} \|R_asset\|` | `9.058e-09` | `<= 1e-6` | PASS |
| `max_{k<K} \|R_labor\|` | `5.829e-08` | `<= 1e-6` | PASS |
| `max_{k<K} \|R_nkpc\|` | `2.392e-18` | `<= 1e-10` | PASS |
| `max_{k<K} \|R_fisher\|` | `0.0` | `<= 1e-12` | PASS |
| `max_{k<K} \|R_taylor\|` | `0.0` | `<= 1e-12` | PASS |
| `max_{k<K} \|R_goods\|` | **`0.2256`** | `<= 1e-5` | **FAIL** (at k=239) |
| `max_{k<K} \|R_wealth\|` | `7.049e-14` | `<= 1e-5` | PASS (KFE-consistent `g_{k+1}` timing) |
| `max_{k<K} \|R_fiscal\|` | `0.0` | `<= 1e-12` | PASS |
| `max_{k<K} \|R_profits\|` | `0.0` | `<= 1e-12` | PASS |
| household/KFE gates | HJB residual `~1e-12 <= 1e-6`; KKT `~1e-15 <= 1e-6`; boundary/generator/finite; KFE mass `~1e-15 <= 1e-10`, min mass `0 >= -1e-12`, neg 0, NaN 0 | — | PASS |
| nontrivial response | `pi` up to `1.94e-4`, `r-r*` up to `1.09e-3` (and boundary-layer `w/N` deviations) | `> 1e-8` | PASS |

Response range (full run): `pi ∈ [-5.42e-4, 1.94e-4]`; `r ∈ [0.00710, 0.00846]`; `w ∈ [0.65484, 0.83496]`; `N ∈ [0.83914, 1.06630]`; `A_hh ∈ [9.9887, 10.0000]`; `C ∈ [1.06470, 1.06630]`. Away from the terminal boundary layer (`k <= 200`), the response is mild (`w` within ~0.2% of `w*`, `N` within ~0.06%).

Terminal-boundary diagnostics (reported, not rooted): `A_hh,K - B = -0.011264`; `N_hh,K - N* = +4.763e-04`; `R_goods,K = +1.329e-04`.

## 12. Zero-innovation evidence (invariance)

| Object | Value | Frozen gate | Verdict |
|---|---|---|---|
| root residual inf-norm | `2.224e-10` | `<= 1e-7` | PASS |
| `max \|w - w*\|` | `~0` | `<= 1e-5` | PASS |
| `max \|N - N*\|` | `~0` | `<= 1e-5` | PASS |
| `max \|pi\|` | `~0` | `<= 1e-6` | PASS |
| `max \|r - r*\|` | `~0` | `<= 1e-5` | PASS |
| `max \|A_hh - B\|` | `2.2e-09` | `<= 1e-5` | PASS |
| `max \|N_hh - N*\|` | `3.0e-13` | `<= 1e-5` | PASS |
| `max \|C - C*\|` | `~1e-9` | `<= 1e-5` | PASS |
| `max_{k<K} \|R_goods\|` | `4.363e-07` | `<= 1e-5` | PASS |
| HJB/KFE gates | PASS | — | PASS |

`BLOCKED_DLH_3D_ZERO_INNOVATION_INVARIANCE` not triggered. The zero run confirms the engine reproduces the steady state exactly and that the boundary layer is innovation-induced.

## 13. Half / quarter / long-horizon runs

- **Half amplitude**: root not converged to the frozen `1e-7` within the bounded effort performed (outer iterations: `6.7e-05 -> 4.3e-07 -> 3.5e-07 -> 3.25e-07 -> 3.08e-07`, ~150 evals/step); the frozen root route's convergence quality varies with amplitude. Evidence preserved; candidate root non-convergence (`BLOCKED_DLH_3D_GE_ROOT_NONCONVERGENCE`-type evidence) for this amplitude.
- **Quarter / long-horizon**: not completed within the session's bounded CPU (each solve 15-40+ min; the fail-closed outcome is established by the full run's §9.3 gate failure). The authoritative long-horizon gate (compare `[0,8]`) is unaffected by the terminal boundary layer (which sits at `t ≈ 11.95`), but could not be executed to completion here.

## 14. Reproducibility

- The residual evaluation is **exactly deterministic**: two evaluations at the identical candidate give `max|diff| = 0.0` (measured directly). The frozen root route (fixed `x0 = 0`, deterministic solver, fixed options) is therefore deterministic; the full validation set would reproduce exactly (consistent with the accepted 3B/3C precedents where repeat differences were `0.0`).
- The full two-pass reproducibility run was not completed within the session's bounded CPU (each pass ≈ 80-110 min of solver time). See `DLH_3D_REPRODUCIBILITY_SUMMARY.csv` for the determinism evidence.

## 15. Regression

Accepted predecessor suite (Tier-0 54 + DLH-3B 23 + DLH-3C 20): **97 passed / 0 failed** — no accepted test modified, no regression. The new DLH-3D gate tests encode the Issue's §8–§12 gates; given the established §9.3 goods-gate failure (and the half-root stall), the corresponding DLH-3D assertions cannot pass, and full DLH-3D test-suite completion requires the multi-hour validation runs. No accepted test was edited; the DLH-3D tests are committed as the faithful gate specification.

## 16. Forbidden-operation counters (all zero)

See `DLH_3D_FORBIDDEN_OPERATION_CHECK.md`. Summary: accepted Tier-0/DLH-3A/DLH-3B/DLH-3C mutation 0 · productive capital/q/investment 0 · varying government debt 0 · TFP/fiscal shock 0 · `epsilon_i` only the frozen innovation (no structural shock) 0 · empirical calibration/data/regression 0 · regional/W/multi-region 0 · neural/RL/GPU 0 · legacy Matlab / old Python reference repo / private Zotero 0 · time-step robustness claims 0 · policy/welfare/Results/novelty claims 0 · governance mutation 0 · PR/merge/Issue close/successor/self-accept 0 · frozen-value alteration after first evidence run 0 · solver fallback / PASS tuning 0.

## 17. Evidence boundary

All evidence is **D2 machine-diagnostic** and limited to the minimal single-region HANK validation fixture. The prescribed `epsilon_i(t)` is a small deterministic monetary-policy **validation-fixture innovation**, not an empirically identified shock, not an IRF, and not policy/Results evidence. The outcome is fail-closed: the frozen fixture's full-amplitude equilibrium does not satisfy the frozen §9.3 goods gate at the last root-interval step (finite-horizon terminal boundary layer), and the frozen root route did not reach the frozen tolerance for the half amplitude within bounded effort. No conclusion about empirical calibration, policy effectiveness, regional NSR-HANK, or Results is drawn.

## 18. Recommendation (non-binding)

The fail-closed evidence should be reviewed independently. A successor Issue could consider (as a reviewer/Owner decision, not Builder authority): a longer primary horizon, an explicitly different terminal-boundary treatment, or a clarified goods-gate evaluation convention — none of which DSH may implement or propose as authority here.
