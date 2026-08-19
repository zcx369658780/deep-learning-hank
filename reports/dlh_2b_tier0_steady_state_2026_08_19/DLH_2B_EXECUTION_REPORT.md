# DLH-2B-R1 — Single-Region Tier-0 HA/Aiyagari Steady-State GE — Execution Report (Corrected)

- Date: 2026-08-19 (R1 evidence/root-trace correction)
- Author: DSH (bounded Builder)
- Authority: GitHub Issue #6 — `DLH-2B`; authoritative R1 correction comment (2026-08-19 11:20:22).
- Prior candidate: `2b4316f699720f0d8ad278c98110e8c1128532c4` — core steady-state D2 gate PASS; candidate NOT accepted/merged; R1 applies bounded evidence/root-trace corrections only.
- Status: CANDIDATE. Acceptance requires fresh-GitHub independent review (ChatGPT).
- Evidence class: **D2 machine-diagnostic evidence for a small one-region real HA/Aiyagari steady-state benchmark only.**

## 1. Terminal classification

`DLH_2B_R1_EVIDENCE_AND_ROOT_TRACE_CORRECTION_READY_FOR_GPT_REVIEW`

## 2. Baselines and branch

- Fresh target `origin/main` SHA: `2b038ae9b9ef3c69209629b14a2515f1d176accf`
- Dedicated R1 branch: `dsh/issue-6-dlh-2b-r1-evidence-root-trace-correction-2026-08-19`
- Candidate commit: single coherent commit at branch HEAD (2026-08-19, DSH); hash reported in completion response. Expected delta: exactly the 13 allowlisted paths, 0 behind / 1 ahead.

## 3. Exact changed paths (13-path allowlist, same as Issue #6)

1. `configs/dlh_2b_tier0_steady_state_validation.toml`
2. `src/deep_learning_hank/config.py`
3. `src/deep_learning_hank/solvers/__init__.py`
4. `src/deep_learning_hank/solvers/steady_state.py`
5. `src/deep_learning_hank/diagnostics/__init__.py`
6. `src/deep_learning_hank/diagnostics/tier0_steady_state.py`
7. `tests/test_dlh_2b_equilibrium.py`
8. `tests/test_dlh_2b_accounting.py`
9. `tests/test_dlh_2b_reproducibility.py`
10. `reports/dlh_2b_tier0_steady_state_2026_08_19/DLH_2B_EXECUTION_REPORT.md`
11. `reports/dlh_2b_tier0_steady_state_2026_08_19/DLH_2B_DIAGNOSTICS.csv`
12. `reports/dlh_2b_tier0_steady_state_2026_08_19/DLH_2B_ROOT_TRACE.csv`
13. `reports/dlh_2b_tier0_steady_state_2026_08_19/DLH_2B_FORBIDDEN_OPERATION_CHECK.md`

**Accepted DLH-2A frozen modules/tests and all other paths: untouched.** R1 changes confined to `steady_state.py` (precise evaluation-count fields), `tier0_steady_state.py` (root-trace finiteness gate), `tests/test_dlh_2b_equilibrium.py` (new assertions), and the four reports.

## 4. Environment and exact commands

- Python `3.11.9` (pre-existing); numpy `2.4.6`, scipy `1.17.1`, pytest `8.2.1` (pre-existing; zero installs; no environment mutation; no GPU).

**Command 1 — full repository test suite (R1 rerun; exact command):**
```
$env:PYTHONPATH = "D:\deep-learning-hank\src"
python -m pytest tests -v
```
R1 rerun result: **32 passed, 0 failed** (DLH-2A regression 15 + DLH-2B 17).

**Command 2 — corrected equilibrium diagnostics (R1 rerun; fully self-contained exact script — full text below):**
```
$env:PYTHONPATH = "D:\deep-learning-hank\src"
$script = @'
from pathlib import Path
import numpy as np
from deep_learning_hank.config import SteadyStateConfig
from deep_learning_hank.diagnostics.tier0_steady_state import run_tier0_steady_state
cfg = SteadyStateConfig.from_toml(Path("configs/dlh_2b_tier0_steady_state_validation.toml"))
d = run_tier0_steady_state(cfg)
r = d.result
f = r.final
print("config_sha256", d.config_sha256)
print("l_bar", repr(d.l_bar))
print("root_capital", repr(r.root_capital))
print("root_converged", r.root_converged)
print("root_trace_evaluations", r.root_trace_evaluations)
print("post_root_validation_evaluations", r.post_root_validation_evaluations)
print("total_capital_evaluations", r.total_capital_evaluations)
print("root_trace_finite_ok", d.root_trace_finite_ok)
print("bracket_used", r.bracket_used, "bracket_from_scan", r.bracket_from_scan)
print("K*", repr(f.capital))
print("output_Y", repr(f.output))
print("wage", repr(f.wage))
print("net_capital_return_r", repr(f.net_capital_return))
print("transfer", repr(f.transfer))
print("mean_assets_A_hh", repr(f.mean_assets))
print("mean_consumption_C", repr(f.mean_consumption))
print("effective_labor_g_L_g", repr(f.effective_labor_g))
print("capital_residual_R_K", repr(f.capital_residual))
print("goods_residual_R_goods", repr(f.goods_residual))
print("household_budget_residual_R_hh", repr(f.household_budget_residual))
print("mean_drift", repr(f.mean_drift))
print("hjb_converged", f.hjb_converged, "hjb_resid", repr(f.hjb_true_residual), "hjb_iters", f.hjb_iterations)
print("hjb_min_consumption", repr(f.hjb_min_consumption))
print("hjb_lower_boundary_min_drift", repr(f.hjb_lower_boundary_min_drift))
print("hjb_upper_boundary_max_drift", repr(f.hjb_upper_boundary_max_drift))
print("hjb_row_sum_max_abs", repr(f.hjb_generator_row_sum_max_abs))
print("hjb_min_off_diag_literal", repr(f.hjb_generator_min_off_diagonal))
print("hjb_nan_inf", f.hjb_nan_inf_count)
print("kfe_mass_error", repr(f.kfe_mass_error))
print("kfe_stationarity", repr(f.kfe_stationarity_residual))
print("kfe_min_mass", repr(f.kfe_minimum_mass))
print("kfe_neg_count", f.kfe_negative_mass_count, "kfe_nan_inf", f.kfe_nan_inf_count)
print("effective_labor_error", repr(d.effective_labor_error))
print("state_marginals", [float(x) for x in f.state_marginals])
print("gates", dict(root_trace_finite=d.root_trace_finite_ok, root=d.root_gate_ok, clearing=d.capital_clearing_ok,
                    hjb=d.hjb_ok, kfe=d.kfe_ok, labor=d.effective_labor_ok, fiscal=d.fiscal_ok,
                    goods=d.goods_ok, budget=d.budget_ok, drift=d.mean_drift_ok, pos=d.positivity_ok))
print("all_gates_pass", d.all_gates_pass)
d2 = run_tier0_steady_state(cfg)
a, b = d.result.final, d2.result.final
diffs = {
 "capital_star": abs(a.capital - b.capital),
 "wage": abs(a.wage - b.wage),
 "net_capital_return": abs(a.net_capital_return - b.net_capital_return),
 "output": abs(a.output - b.output),
 "transfer": abs(a.transfer - b.transfer),
 "value": float(np.max(np.abs(a.household.value - b.household.value))),
 "consumption": float(np.max(np.abs(a.household.consumption - b.household.consumption))),
 "drift": float(np.max(np.abs(a.household.drift - b.household.drift))),
 "distribution_mass": float(np.max(np.abs(a.distribution.mass - b.distribution.mass))),
 "scalars": float(np.max(np.abs(a.scalar_vector() - b.scalar_vector()))),
}
print("repeat_diffs", diffs)
print("root_trace_len", len(r.root_trace))
for i, (k, res) in enumerate(r.root_trace):
    print(f"trace_{i}", repr(k), repr(res))
'@
Set-Content -Path (Join-Path $env:TEMP "dlh2b_r1_diag.py") -Value $script -Encoding UTF8
python (Join-Path $env:TEMP "dlh2b_r1_diag.py")
```

## 5. Test-attempt history (preserved)

- **Original DLH-2B run (R0 candidate `2b4316f…`):**
  - attempt 1 = 29 passed / 1 tooling failure (test-tooling fix in `test_no_regional_w_soe_nominal_objects`);
  - attempt 2 = 30 passed.
- **R1 correction rerun (this candidate):** new execution attempt = **32 passed / 0 failed** (two new machine-gate tests added: root-trace finiteness + evaluation-count semantics).
- History is not rewritten: R1 is not the first run.

## 6. Fixture — VALIDATION_FIXTURE_NOT_CALIBRATION

`configs/dlh_2b_tier0_steady_state_validation.toml` (header explicitly labeled): asset grid `[0,50]`/40 pts; states `(0.5,1.5)`; intensities `0.25/0.25`; `rho_hh=0.01`; `gamma=2.0`; `tau_l=0.15`; `A=1.0`, `alpha_k=0.30`, `delta=0.02`, `G=0.0`; capital bracket `[0.5,45.0]`; scan `[0.1,49.0]`/98 pts; outer capital tolerance `1e-7`; outer max iterations `200`. Numerical validation fixture only — never empirical calibration.

## 7. Effective-labor construction

`L_bar = sum_z pi_z * z` from the idiosyncratic CTMC stationary law (computed, not hard-coded) = `1.0`; final `L_g = sum g(z,a)*z = 1.0`; `|L_g − L_bar| = 0.0 <= 1e-8` ✓.

## 8. Root/bracket evidence (R1 precise evaluation-count semantics)

- Primary bracket `[0.5,45.0]`: endpoint residuals `R_K(0.5) = −49.5`, `R_K(45.0) = +35.365079662198205` (finite, opposite signs). No scan required (`bracket_from_scan = False`).
- `brentq` (xtol=1e-10, rtol=1e-14, maxiter=200) root `K* = 27.367823476711713`, converged.
- **Evaluation counts (precise semantics, R1):**
  - `root_trace_evaluations = 11` (2 primary endpoint pre-checks + 9 `brentq` callback evaluations, all recorded in `DLH_2B_ROOT_TRACE.csv`);
  - `post_root_validation_evaluations = 1` (final `evaluate_capital(root)` after `brentq` returns);
  - `total_capital_evaluations = 12` for this execution.
- **Root-trace finiteness machine gate (R1, Issue #6 "all root evaluations finite"):** `root_trace_finite_ok = True` — every trace entry (capital and residual) is finite; folded into `root_gate_ok` and `all_gates_pass`.
- Capital residual `R_K(K*) = 1.0466294497746276e-11 <= 1e-7` ✓.

## 9. Equilibrium objects (fixture)

| Object | Value |
|---|---|
| K* | 27.367823476711713 |
| Y | 2.6988085539374342 |
| wage w | 1.889165987756204 |
| r (household asset return = net capital return) | 0.009583739710619838 |
| transfer | 0.2833748981634306 |
| mean assets A_hh | 27.367823476701247 |
| mean consumption C | 2.1514520844030995 |

## 10. Household/KFE diagnostics at equilibrium (thresholds frozen, unchanged from R0)

- HJB converged (8 iters); residual `1.3058058412340756e-08 <= 1e-7` ✓; min consumption `1.0862704429598173 > 0` ✓; lower drift `0.0 >= -1e-12` ✓; upper drift `0.0 <= 1e-12` ✓; generator row-sum `1.1102230246251565e-16 <= 1e-12` ✓; **literal** off-diagonal minimum `0.0 >= -1e-14` ✓; NaN/Inf `0` ✓.
- KFE: mass error `0.0 <= 1e-10` ✓; stationarity `2.905661822261152e-17 <= 1e-8` ✓; min mass `1.0123318235136522e-03 >= -1e-12` ✓; negative count `0` ✓; NaN/Inf `0` ✓; marginals `[0.5,0.5]` ✓.

## 11. Independent accounting diagnostics (computed, never zeroed)

| Residual | Value | Threshold | PASS |
|---|---|---|---|
| R_goods = Y − C − δ·K − G | 1.0047518372857667e-13 | <= 1e-7 | ✓ |
| R_hh_budget = C − [(1−τ_l)·w·L_g + r·A_hh + transfer] | 0.0 | <= 1e-7 | ✓ |
| mean_drift = Σ g·drift | −2.2941717969793274e-16 | <= 1e-7 | ✓ |
| fiscal residual | 0.0 | <= 1e-12 | ✓ |

Positivity: Y, w, C, K* > 0; r finite and positive. All accounting gates PASS.

## 12. Deterministic reproducibility (R1 rerun)

Full pipeline run twice; max absolute repeat differences (threshold `1e-12`) — all exactly `0.0`: K* `0.0`, wage `0.0`, r `0.0`, output `0.0`, transfer `0.0`, value `0.0`, consumption `0.0`, drift `0.0`, distribution mass `0.0`, scalars `0.0`. PASS.

## 13. Engineering corrections / reruns

- R1: (a) precise evaluation-count semantics in `steady_state.py` (`root_trace_evaluations` / `post_root_validation_evaluations` / `total_capital_evaluations`); (b) `root_trace_finite_ok` machine gate in `tier0_steady_state.py`, included in `root_gate_ok` / `all_gates_pass`; (c) two strengthened/added assertions in `tests/test_dlh_2b_equilibrium.py`; (d) full exact diagnostics script recorded (this report). No economic/closure/root/brentq/fixture/threshold change.

## 14. Forbidden-operation counters (all zero)

- W^L / W^K / old W / spatial / multi-region = 0 · SOE factor = 0 · RegionalAccounts = 0 · nominal/Fisher/NKPC/Taylor = 0 · shocks/AR(1) = 0 · transition = 0 · neural/RL = 0 · empirical data/calibration/regression = 0 · Matlab/Octave/Dynare = 0 · legacy Matlab reads = 0 · old source-repo mutation = 0 · Results/policy/novelty claims = 0 · governance changes = 0 · PR / merge / Issue close / successor / self-accept = 0.

## 15. Evidence boundary

D2 machine-diagnostic evidence for a small one-region real HA/Aiyagari steady-state benchmark only; does not establish calibration, genuine-HANK validity, multi-region NSR-HANK validity, transition dynamics, policy/Results eligibility, or novelty.

## 16. Recommendation for next validation subgate (suggestion only — no successor creation)

After independent review: proceed per the Master Roadmap to the next DLH-2/3 validation step (e.g., minimal genuine single-region HANK nominal layer); no successor Issue created by the Builder.
