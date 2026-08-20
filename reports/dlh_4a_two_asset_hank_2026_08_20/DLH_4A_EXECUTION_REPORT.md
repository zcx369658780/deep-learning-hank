# DLH-4A — Python Reconstruction of Two-Asset HANK Household HJB and KFE Kernel — Execution Report

- Date: 2026-08-20
- Author: DSH (bounded Builder)
- Authority: GitHub Issue #17 — `DLH-4A: Python Reconstruction of Two-Asset HANK Household HJB and KFE Kernel` (state: OPEN), activation comment id `IC_kwDOT9FOGc8AAAABP6r2jg`
- Task type: `SCIENTIFIC_IMPLEMENTATION__TWO_ASSET_HANK_HJB_KFE_RECONSTRUCTION`
- Status: **FAIL-CLOSED CANDIDATE — structural reconstruction complete; the Issue #17 numerical validation gates (HJB convergence to a monotone value function; unique stationary distribution) are NOT satisfied on the reference-style fixture within the bounded effort. Evidence preserved for independent review; this is NOT a PASS.**

## 1. Terminal classification

**`BLOCKED_DLH_4A_ENGINEERING_FAILURE`** (Issue #17 §"Engineering failure"): the reconstructed household kernel's **structure** is faithful and its **machinery** is validated (generator properties, adjustment-cost economics, KFE machinery, separate accounting, determinism — 15/15 tests pass), but the **numerical validation** required by the Issue (HJB convergence with monotone value function; unique stationary distribution from the KFE) cannot be achieved on the reference-style fixture within the reconstruction's scope.

The root cause is a documented combination of (a) the **fixture regime degeneracy** of the exogenous-return two-asset household block (with the reference returns relative to the discount rate the household's liquid dimension is uniformly dissaving/borrowing-constrained, and the illiquid adjustment is pinned at its bound), and (b) the **numerical fragility of the reference algorithm family** (the legacy itself tolerates loose generator row sums `homecrit = 1e-2` and relies on per-province calibration).

## 2. Structural reconstruction (complete; Issue #17 "Required Economic Structure")

| Component | Delivered | Where |
|---|---|---|
| State space `(b, a, z)` (liquid, illiquid, productivity; no collapse to `(a,z)`) | ✅ | `src/deep_learning_hank/two_asset/household_hjb.py`; `DLH_4A_PRECODING_MAPPING.md` §1 |
| Controls `c`, `l`, `d`; explicit adjustment cost `chi(d,a)` (inaction band) | ✅ | `economics.py` `adjustment_cost` / `adjustment_transfer`; `household_hjb.py` |
| HJB: forward/backward derivatives in both asset dimensions; candidate policies; adjustment decision logic; boundary conditions | ✅ | `household_hjb.py` `_foc_policies` (upwind derivative conventions, state-constraint boundaries) |
| Generator `G = G_b + G_a + G_z` shared by HJB and KFE | ✅ | `household_hjb.py` `build_generator` (net-drift upwind, exact rows-sum-zero) |
| KFE `g(a,b,z)`; stationary condition; mass normalization; non-negativity diagnostics | ✅ | `kfe.py` (null-space solve; uniqueness/nullity diagnostic) |
| Asset accounting `A_hh = ∫a g`, `B_hh = ∫b g` separately (never merged, never assumed equal) | ✅ | `kfe.py` + `test_dlh_4a_accounting.py` |

Pre-coding documentation (Issue #17 requirement): state-space / HJB / generator / asset-accounting mappings in `DLH_4A_PRECODING_MAPPING.md`, including two documented legacy-code corrections (the reference's `raah²` term in the zero-drift labor base; the transfer scale `a` vs the cost's `max(a, a_bar)`, the latter making `a=0` absorbing in the reference).

## 3. Validation findings on the reference-style fixture (Issue #17 "Validation")

Fixture: `configs/dlh_4a_two_asset_household_validation.toml` (SHA-256 in `DLH_4A_DIAGNOSTICS.csv`); reference-mirroring values `rho=0.05, gamma=2, frisch_l=0.2, chi0=0.1, chi1=2, a_bar=1.0` (documented deviation from the reference `a_bar=1e-6`), `b∈[-2,5]` (20), `a∈[0,10]` (20), `z∈{0.8,1.3}` (2), `w=1.0, rb=0.02, ra=0.04, rb_gap=0.01, Tt=0, tau=0.15`.

| Gate | Value | Required | Verdict |
|---|---|---|---|
| Generator row-sum max abs | `1.184e-13` | `≤ 1e-6` | **PASS** (exact mass conservation) |
| Generator min off-diagonal | `0.0` | `≥ -1e-10` | **PASS** (valid rates) |
| Generator finite (NaN count) | `0` | `0` | **PASS** |
| HJB iteration (bounded 1000) | not converged; true residual `2.739e+07` | converge with monotone value | **FAIL** |
| Value monotone in `b` / `a` | `mono_b ≈ 0.5-0.55` | `≈ 1.0` | **FAIL** |
| Labor FOC max / consumption FOC max | `2.3e-12` / `1.1e-3` | small | PASS / (consumption FOC elevated) |
| Adjustment active fraction | `0.9925` | — | observation (band pinned at bound) |
| KFE stationary distribution unique (`nullity(G^T)` = 1) | **nullity = 7** | 1 | **FAIL** |
| `A_hh` / `B_hh` separate aggregates | not defined (non-unique measure) | reported separately | FAIL (dependent on gate above) |
| Determinism (identical solves) | repeat diff `0.0` | `0.0` | **PASS** |

Overall: `all_gates_pass = False` (see `DLH_4A_DIAGNOSTICS.csv`).

## 4. Root-cause analysis (evidence-based)

1. **Fixture-regime degeneracy.** In the exogenous-return household block with `ra, rb < rho`, the household's liquid dimension is uniformly dissaving (borrowing-constrained): the liquid drift is negative everywhere (households consume/buy illiquid faster than income), so the stationary mass collapses onto the borrowing limit and the value function develops boundary layers; with `ra > rho` the illiquid dimension accumulates to the grid top. The reference itself runs only inside a general-equilibrium closure that pins the returns; that closure is out of scope here (Issue #17 forbids NK/monetary/fiscal extension).
2. **Adjustment band pinned at its bound.** Because the illiquid asset is uniformly attractive relative to liquid (`ra > rb`) in the dissaving region, the transfer FOC sits at the inaction-band boundary (adjustment-active fraction ≈ 0.99), and with the ratio cap the transfer is pinned near its bound — the value iteration then cannot settle into an interior regime.
3. **Reference algorithm family fragility.** The legacy `HANK_2ASSETS_HJB.m` tolerates generator row sums of order `homecrit = 1e-2`, has the documented `raah²` and transfer-scale inconsistencies, and its value iteration was only ever run inside the calibrated multi-province GE. A faithful family reconstruction with exact mass conservation does not, by itself, cure the fixture degeneracy.

## 5. Attempt history (all materially distinct schemes; evidence in `DLH_4A_DIAGNOSTICS.csv` and the probe scripts)

| Scheme | Outcome |
|---|---|
| Split-stream generator (legacy X/Y/Z + chih/yyh/zetah bookkeeping) | value iteration diverges (V_b → 0 amplification); negative off-diagonals at the forced top-b boundary |
| Direct net-drift upwind (FOC policies, no selection) | converges to a deterministic fixed point, but the value is non-monotone (upwind inconsistency) |
| Frozen-direction drift-consistent upwind | directions oscillate (~half the grid flips each iteration); no convergence |
| All schemes with: full-income initialization, consumption cap, ratio cap, state-constraint clipping, policy-iteration / pseudo-time / damping variants | none reach a monotone value + unique stationary distribution on the reference fixture |

## 6. Test results

- New machinery suite (`test_dlh_4a_generator.py`, `test_dlh_4a_accounting.py`, `test_dlh_4a_kfe.py`, `test_dlh_4a_determinism.py`): **15 passed / 0 failed** (14.8 s). These verify the reconstructed machinery (generator structure/properties, adjustment-cost and labor FOC formulas, KFE mass conservation on an irreducible generator, separate aggregates, determinism).
- The Issue #17 validation gates are evaluated honestly by `run_two_asset_diagnostics` (`all_gates_pass=False` on the reference fixture) — the failing gates are reported as evidence, not asserted away.

## 7. Baseline / Issue / branch / commit

- Fresh baseline `origin/main` SHA: `d727dda28738bbdad126c784f0366f0e21be3e1d`
- Issue #17 title/status: OPEN; activation comment `IC_kwDOT9FOGc8AAAABP6r2jg`
- Dedicated branch: `dsh/issue-17-dlh-4a-two-asset-hank-2026-08-20` (created from fresh `origin/main`)
- Candidate commit: single coherent commit at branch HEAD (2026-08-20, DSH); SHA in the completion response.

## 8. Exact changed paths (new only; no accepted path modified)

1. `configs/dlh_4a_two_asset_household_validation.toml`
2. `src/deep_learning_hank/two_asset/__init__.py`
3. `src/deep_learning_hank/two_asset/config.py`
4. `src/deep_learning_hank/two_asset/economics.py`
5. `src/deep_learning_hank/two_asset/household_hjb.py`
6. `src/deep_learning_hank/two_asset/kfe.py`
7. `src/deep_learning_hank/two_asset/diagnostics.py`
8. `tests/test_dlh_4a_generator.py`
9. `tests/test_dlh_4a_accounting.py`
10. `tests/test_dlh_4a_kfe.py`
11. `tests/test_dlh_4a_determinism.py`
12. `reports/dlh_4a_two_asset_hank_2026_08_20/DLH_4A_PRECODING_MAPPING.md`
13. `reports/dlh_4a_two_asset_hank_2026_08_20/DLH_4A_EXECUTION_REPORT.md`
14. `reports/dlh_4a_two_asset_hank_2026_08_20/DLH_4A_DIAGNOSTICS.csv`
15. `reports/dlh_4a_two_asset_hank_2026_08_20/DLH_4A_FORBIDDEN_OPERATION_CHECK.md`

**No accepted predecessor path modified** (Tier-0 / DLH-3A / 3B / 3C / 3D / R1A / R2 / R2-DOC untouched; the two-asset package is new).

## 9. Environment / reproducibility

- Python `3.11.9`; numpy `2.4.6`; scipy `1.17.1`; pytest `8.2.1` (pre-existing; zero installs; no GPU).
- Deterministic single-threaded CPU; no random numbers (seed policy: none required); repeat differences `0.0`.

## 10. Evidence boundary

All evidence is D2 machine-diagnostic. The reconstruction faithfully implements the two-asset household structure (state `(b,a,z)`, adjustment cost, generator decomposition, KFE, separate accounting), but the reference-style fixture does not admit the Issue's numerical validation within scope. This is a correct fail-closed blocker; per project rules it may be accepted as blocker evidence but is not a PASS. No two-asset GE, NK, monetary, regional, or neural claims are made.

## 11. Recommendation (non-binding)

- Review the structural reconstruction and the root-cause analysis independently.
- A successor Issue could authorize either (a) a minimal two-asset GE closure (firm/monetary/fiscal blocks pinning `ra, rb, w, Tt`) so the household block is evaluated at interior equilibrium returns, or (b) a numerical-method specification (upwind direction consistency, continuation/damping) as a separate numerical task — neither of which the Builder may implement here.
