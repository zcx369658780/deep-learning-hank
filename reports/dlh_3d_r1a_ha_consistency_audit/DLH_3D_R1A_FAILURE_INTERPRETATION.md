# DLH-3D-R1A — DLH-3D Fail-Closed Goods-Gate Failure: Evidence-Based Interpretation

- Date: 2026-08-20
- Authority: GitHub Issue #14 (OPEN); diagnostic only; no rerun, no PASS seeking.
- Evidence source: `reports/dlh_3d_hank_monetary_ge_2026_08_20/DLH_3D_EXECUTION_REPORT.md`, `DLH_3D_RESIDUAL_AMPLITUDE_SUMMARY.csv`, `DLH_3D_PATH_DIAGNOSTICS.csv` (fail-closed candidate commit `9f767d1`, branch `dsh/issue-13-dlh-3d-monetary-ge-2026-08-20`).

## 1. The failure to classify

Full-amplitude GE (`T=12`, `dt=0.05`, `K=240`): `max_{k<K} |R_goods,k| = 0.22557608337684318 > 1e-5` at `k = 239` (= K−1, the last root-interval step). All other §9 gates PASS:

| Metric (full run) | Value | Gate | Verdict |
|---|---|---|---|
| root residual inf-norm | 5.470e-08 | ≤1e-7 | PASS |
| max_{k<K} \|R_asset\| | 9.058e-09 | ≤1e-6 | PASS |
| max_{k<K} \|R_labor\| | 5.829e-08 | ≤1e-6 | PASS |
| max_{k<K} \|R_nkpc\| | 2.392e-18 | ≤1e-10 | PASS |
| max_{k<K} \|R_fisher\| / \|R_taylor\| | 0.0 | ≤1e-12 | PASS |
| max_{k<K} \|R_wealth\| (g_{k+1} timing) | 7.049e-14 | ≤1e-5 | PASS |
| max_{k<K} \|R_goods\| | **0.2256 @ k=239** | ≤1e-5 | **FAIL** |
| household/KFE gates | PASS | — | PASS |
| zero-innovation invariance | PASS (R_goods_max = 4.36e-07) | — | PASS |

## 2. Why the failure sits exactly at k = K−1 (identity chain)

The frozen discrete identities (all verified in the audited code and evidence) imply:

1. Asset clearing on the root interval: `A_hh,k = B` for `k = 0..K−1` (root-enforced).
2. Wealth-flow identity (KFE-consistent timing, `R_wealth ≈ 7e-14`): `(A_hh,k+1 − A_hh,k)/dt = Σ_{a,z} g_{k+1}(a,z)·s_k(a,z)`.
3. Fiscal: `tr = τ_l w N − r B`; profits: `Π = Y − wN − AC`.
4. Chain (aggregate budget): `Y − C − AC = (A_hh,k+1 − A_hh,k)/dt` at any `k < K` where the other identities hold.

Therefore at `k = K−1`: `R_goods,K−1 = (A_hh,K − A_hh,K−1)/dt = (A_hh,K − B)/dt`.

Measured: `terminal_A_hh_minus_B = −0.011263952656195286`; `R_goods,K−1 = −0.011263952656195286/0.05 = −0.225279…` ≈ reported `0.2256` (the CSV max-abs). **The goods-gate failure is exactly the terminal asset deviation `A_hh,K − B` scaled by `1/dt`.** This is not an accounting error — it is the discrete consequence of the frozen terminal boundary.

## 3. Why `A_hh,K − B ≠ 0` (terminal boundary artifact)

- The frozen terminal aggregate point pins `w_K = w*`, `N_K = N*` (`pi_K = 0`) but **does not pin `A_hh,K`**; per the authoritative numerical-timing clarification (Issue #13 comment `5349487045`), `A_hh,K − B` is a finite-horizon terminal-approximation diagnostic, not a root equation.
- The innovation's asset effect relaxes very slowly: ~10 years after the forcing, the unforced continuation of the clearing path still has `A_hh,K ≈ 9.9887` (deviation −0.0113, i.e. −0.11% of `B`).
- The root therefore must force `A_hh,K−1 = B` against a "natural" terminal value ≈ 9.9887, producing an extreme last-step boundary layer (`w = 0.6548`, `N = 0.8391` at `k=239`, i.e. −24%/−21% from baseline) where forward-looking households keep consuming near baseline and dissave at −0.226/yr.
- A "mild" candidate with baseline `(w,N)` at `k=239` has small `R_goods` (−1.7e-4) but **fails asset clearing** (`R_asset = +1.7e-2`): under this frozen fixture no candidate satisfies both gates at `k = K−1`.
- The zero-innovation run has no boundary layer and passes all gates — the layer is innovation-induced, not an engine defect.

## 4. Classification

| Candidate cause | Verdict | Basis |
|---|---|---|
| A. HA implementation mismatch | **NOT SUPPORTED** | one-asset HJB/KFE internally consistent (audit §3-4); zero-run invariance passes; wealth-flow residual ~7e-14 |
| B. Asset-accounting mismatch | **NOT SUPPORTED** | `R_asset`/`R_labor`/`R_wealth`/fiscal/profit gates all pass on the root interval; the identity `R_goods,K−1 = (A_hh,K − B)/dt` is exact |
| C. **Finite-horizon terminal-boundary issue** | **PRIMARY CAUSE** | terminal point pins `(w_K,N_K,π_K)` but leaves `A_hh,K` free; frozen root interval `k=0..K−1` forces the last-step layer; `R_goods,K−1 = (A_hh,K − B)/dt` exactly |
| D. Parameter/fixture issue | **CONTRIBUTING** | the frozen fixture (T=12, dt=0.05, slow wealth relaxation of the η_i=0.001 innovation; root interval vs terminal point convention) makes the layer inevitable; no parameter was tuned (forbidden) |
| E. Other (HJB/KFE transition mismatch) | NOT SUPPORTED | transition semantics match accepted DLH-3C; mass and wealth-flow gates pass |

**Evidence-based conclusion: the DLH-3D goods-gate failure is a finite-horizon terminal-boundary artifact (C), amplified by the frozen fixture/root-interval interaction (D). It is NOT an HA implementation, asset-accounting, or HJB/KFE mismatch.**

## 5. Notes for the reviewer (diagnostic only, no authority)

- The long-horizon gate (per clarification, the authority for judging whether the terminal approximation contaminates the early window) compares `[0,8]`; the boundary layer sits at `t≈11.95`, outside that window, but the §9.3 goods gate is frozen on `k=0..K−1` and therefore fails regardless.
- Resolution options would be reviewer/Owner decisions (e.g., longer primary horizon, different terminal-boundary treatment, clarified goods-gate evaluation convention) — none of which the Builder may implement here; no gate/terminal/fixture was altered (see `DLH_3D_R1A_FORBIDDEN_OPERATION_CHECK.md`).
- Half-amplitude root stall (~3.1e-07, bounded effort) is a separate, frozen-root-route convergence observation (documented in the DLH-3D execution report §13), also evidence-preserved without tuning.
