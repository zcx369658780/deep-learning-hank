# DLH-3D-R1A — Asset-Accounting Audit

- Date: 2026-08-20
- Authority: GitHub Issue #14 (OPEN), activation comment `5355380189`; canonical spec `tasks/DLH_3B_R1_HA_ALGORITHM_PARITY_AUDIT_2026_08_20.md`
- Type: `SCIENTIFIC_AUDIT_ONLY`; no modification; no numerical execution.

## 1. Determination from code evidence

**The current Python implementation is ONE-asset.**

- Household holdings: single liquid, risk-free real financial asset `a` (bond claim). No illiquid asset, no second asset.
- Aggregation: `A_hh = ∫ a dg` (`solvers/distribution_kfe.py` `mean_assets = Σ g·a`; `solvers/hank_steady_state.py` `distribution.mean_assets`).
- Clearing: **single asset market** `A_hh − B = 0` with constant government bond supply `B = 10` (`configs/dlh_3b_hank_steady_state_validation.toml` `[fiscal] B`; `R_asset = A_hh − B`).
- No borrowing: `a_min = 0.0`.
- No portfolio choice, no adjustment cost, no separate liquid/illiquid split.

## 2. One-asset accounting (Python, current)

| Object | Equation | Source |
|---|---|---|
| Asset demand | `A_hh = Σ_a Σ_z g(a,z)·a` | `solvers/distribution_kfe.py` L80 |
| Asset supply | constant `B = 10` (bonds) | `configs/.../dlh_3b_hank_steady_state_validation.toml` |
| Asset clearing | `R_asset = A_hh − B = 0` | `solvers/hank_steady_state.py` L186 |
| Labor | `N_hh = Σ g·z·n` (effective labor supply) | `solvers/hank_steady_state.py` L185 |
| Labor clearing | `R_labor = N_hh − N = 0` (`N` = production labor, `Y = Z·N`) | L187 |
| Goods/resource | `R_goods = Y − C − AC` (AC = Rotemberg cost), diagnostic | `solvers/hank_ge_transition.py` L218 |
| Fiscal | `tr = τ_l w N − r B`; `R_fiscal = τ_l w N − r B − tr` | `economics/hank_fiscal.py` |
| Wealth flow | `R_wealth,k = (A_hh,k+1 − A_hh,k)/dt − a^T G_k^T g_{k+1}` (KFE-consistent) | `solvers/hank_ge_transition.py` L225-233 |

## 3. Two-asset accounting (Matlab legacy, for the record — NOT implemented in Python)

| Object | Equation | Source (`HANK_2ASSETS_HJB.m`) |
|---|---|---|
| Liquid holdings | `Bt = Σ b·g·db·dah` | ~L361 |
| Illiquid (capital) holdings | `Aht = Σ ah·g·db·dah` | ~L363 |
| Effective labor | `Lt = Σ z·l·g·db·dah` | ~L360 |
| Household side | both `b` and `ah` held; adjustment transfer `dh` + cost `chi(d,a)` between them | `HANK3_FOC.m`, `HANK3_cost.m` |
| Supply side | liquid: monetary block; illiquid: capital `K` in firm block `Y = Z K^α L^(1-α)`, return `ra0 = rk − δ + divrate` | `HANK_firm.m` |
| Clearing | capital market via firm return; liquid market via monetary/fiscal block; labor `Lt` in production | `HANK_firm.m`, `mpHANK_equilibrium_2000.m` |

**Do not mix the two asset symbols across codebases:**
- Python `A_hh` (liquid bond demand) ≠ Matlab `Aht` (illiquid capital holdings).
- Python `B` (bond **supply**) ≠ Matlab `Bt` (liquid **demand**) ≠ Matlab `B` (HJB matrix).
- Python `chi` (labor disutility) ≠ Matlab `CHI` (adjustment cost).

## 4. Internal accounting consistency of the Python one-asset route (evidence)

- Accepted DLH-3B: `A_hh* = 10.000000002223675` vs `B = 10` — asset clearing holds to ~2e-9 at the accepted steady state.
- Accepted DLH-3B/3C suite: 77/0 and 97/0 passed; repeat differences 0.0.
- DLH-3D zero-innovation run: `max|A_hh − B| ≈ 2.2e-9 ≤ 1e-5`; `R_wealth ≈ 7.9e-14`; mass gates pass — the accounting identities hold along the path.
- DLH-3D full run: `R_asset_max(k<K) = 9.1e-9`, `R_labor_max(k<K) = 5.8e-8`, `R_wealth ≈ 7.0e-14` — root-interval accounting is internally consistent; the ONLY failing gate is `R_goods` at `k=K-1` (see `DLH_3D_R1A_FAILURE_INTERPRETATION.md`).

## 5. Conclusion

- Python implements **one-asset** accounting: single clearing `A_hh = B` (plus labor clearing), internally consistent.
- Matlab implements **two-asset** accounting: `Bt` + `Aht` with adjustment-cost coupling.
- The asset-accounting structures differ across codebases (structural parity mismatch), while each codebase is internally self-consistent.
