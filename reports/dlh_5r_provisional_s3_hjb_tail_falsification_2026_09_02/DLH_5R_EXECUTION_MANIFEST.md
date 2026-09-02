# DLH-5R — Execution Manifest

**Issue #44 — `DLH_5R_HJB_ONLY_PROVISIONAL_S3_LIQUID_TAIL_NUMERICAL_FALSIFICATION`**

## 1. Authority identity (verified)

- Fresh `origin/main`: `d9d0d1c0b9af062968450200465d3caf50f068ff`
- Dedicated branch created from fresh `origin/main`:
  `dsh/issue-44-dlh-5r-hjb-tail-falsification-2026-09-02`
- Task Index → Issue #44 (`5805a5715131b90cba0f6afe663c94a7da6db37a`);
  Startup Snapshot → Issue #44 (`c6a9e0c797a4dced8f0b77a173600ff9418c0ec8`);
  Roadmap V0.18 → DLH-5R HJB-only falsification (`d9d0d1c0…`).
- Issue #43 accepted and CLOSED; accepted candidate `dd39385…`;
  reviewer acceptance `5507534903`; integration `570d858…`;
  Owner route `APPROVE_Q_B2_HJB_ONLY_NUMERICAL_FALSIFICATION__NO_KFE`
  (`5507666206`).
- Issue #44 OPEN; activation comment `5507725826`.

## 2. Immutable inputs (read-only)

| Object | Value |
|---|---|
| Household HJB source | `src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py` |
| Accepted source blob | `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e` (verified at runtime and via `git rev-parse`) |
| Economics config (D0) | `configs/dlh_5b_two_region_symmetric_anchor.toml` (region 0) |
| Grid authority (DLH-5J) | `configs/dlh_5j_final_coupled_b_extent_diagnostic.toml` (read-only) |
| Falsification protocol | `reports/dlh_5q_provisional_s3_theorem_falsification_2026_09_02/DLH_5Q_NUMERICAL_FALSIFICATION_PROTOCOL.md` (design, executed here under Issue #44) |
| Frozen economics | `rho=0.02, gamma_c=2, phi=5, chi_0=0.1, chi_1=2, a_bar=1e-6, mu_z=0, sigma_z=0, wbar=1.0, r_a=0.03, r_b=0.015, tau=0.15, transfer_income=0, rb_gap=0.01` |
| Grids (exact J0-J5) | `a=linspace(0,10,a_pts)`, `b=linspace(-2,b_hi,b_pts)`, `z=[0.8,1.3]`, `switch=[[-1/3,1/3],[1/3,-1/3]]`; `db=7/19`; b120/b140/b160; **b160 = HARD ROUTE CEILING** |
| Initialization | Accepted fixture: scalar Brent labor root `l^phi = net*(net*l + r_b_eff*b)^(-gamma_c)`, `V0 = u(c_full)/rho`, fresh per variant, no warm-start |
| Numerics | `delta=1000, convergence_tolerance=1e-7, max_iterations=1000, drift_tolerance=1e-12` |

## 3. Executed runs

All six variants executed fresh, HJB-only, via
`scripts/run_dlh_5r_provisional_s3_hjb_tail_falsification.py --workers 6`.
Full per-variant record: `DLH_5R_VARIANT_RUN_SUMMARY.csv` (grid identity,
endpoints, spacings, convergence flag, iterations, statistic, tolerance fields,
runtime, floor activation, non-finite counts, upwind-branch shares).

- All six converged at iteration 10 with `convergence_statistic < 1e-7`,
  reproducing the accepted DLH-5J variant status exactly (iterations and
  statistic identical to all printed digits; J0 upper-b raw boundary
  `4.291614197e-02` matches the accepted DLH-5J boundary CSV).
- `MATLAB_DERIVATIVE_FLOOR = 1e-6` never activated (0 states in every variant).
- No non-finite values in `value`, gradients, controls, or drifts.
- Aligned tail observables persisted: `DLH_5R_ALIGNED_TAIL_OBSERVABLES.csv`
  (64,680 valid aligned states; full Issue #44 §7 field set + audit columns).
- Scaling/plateau diagnostics, cross-b and cross-a tables:
  `DLH_5R_SCALING_AND_PLATEAU_DIAGNOSTICS.csv`.

## 4. Observable-definition correction (documented re-run)

The first execution computed `R_hat`/`Q_hat`/slope from the forward/forward raw
pair. On inspection, all primary tail states are on the dissaving liquid branch
(`mu_b < 0`, since `r_b < rho`), so the economically-active raw `V_b` is the
**backward** gradient (verified: `c = V_b_backward^(-1/gamma_c)` to ~6e-10).
The runner's observable definition was corrected to the raw **upwind** pair
(`V_a = forward raw if mu_a>=0 else backward raw; V_b likewise`), with the
forward/forward pair retained as audit columns (`R_hat_ff`, `Q_hat_ff`). The
run was re-executed with **identical scientific inputs** (same grids, init,
economics, solver, numerics — same iteration counts, statistics, values,
gradients, and controls). This is a post-processing definitional correction, not
a scientific-input retry; both runs are identical at the solver level.

## 5. Exact changed/created paths (Issue #44 allowlist only)

1. `configs/dlh_5r_provisional_s3_hjb_tail_falsification.toml`
2. `scripts/run_dlh_5r_provisional_s3_hjb_tail_falsification.py`
3. `reports/dlh_5r_provisional_s3_hjb_tail_falsification_2026_09_02/DLH_5R_EXECUTION_REPORT.md`
4. `.../DLH_5R_EXECUTION_MANIFEST.md`
5. `.../DLH_5R_RAW_GRADIENT_PROVENANCE.md`
6. `.../DLH_5R_VARIANT_RUN_SUMMARY.csv`
7. `.../DLH_5R_ALIGNED_TAIL_OBSERVABLES.csv`
8. `.../DLH_5R_SCALING_AND_PLATEAU_DIAGNOSTICS.csv`
9. `.../DLH_5R_FALSIFICATION_DECISION.md`
10. `.../DLH_5R_FORBIDDEN_OPERATION_CHECK.md`

No existing tracked file is modified. Large raw full-grid arrays are not
committed; the temporary `_decision_inputs.json` remains outside Git staging.
