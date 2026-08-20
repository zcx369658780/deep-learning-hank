# DLH-3D-R1A — HA State-Space Audit

- Date: 2026-08-20
- Authority: GitHub Issue #14 (OPEN), activation comment `5355380189`; canonical spec `tasks/DLH_3B_R1_HA_ALGORITHM_PARITY_AUDIT_2026_08_20.md`
- Type: `SCIENTIFIC_AUDIT_ONLY`; no code/parameter modification; no numerical execution.

## 1. Headline answer

**The current Python HA/HANK module implements a ONE-asset economy with household state `(a, z)`.**
It is **NOT** a two-asset (`(a,b,z)`) implementation. This is established from source evidence below, not from project naming or history.

The legacy Matlab reference `HANK_2ASSETS_HJB.m` implements a **TWO-asset** economy with household state `(b, ah, z)`.

## 2. Python state-space evidence (source locations)

| Object | Evidence |
|---|---|
| Household state | `(a, z)`: one liquid financial asset `a`, idiosyncratic productivity `z`. `solvers/hank_household_steady_state.py` `solve_hank_household(asset_grid, efficiency_states, state_generator, wage, real_return, transfer, profits, ...)` — exactly one asset grid and one real return. |
| Asset grid | uniform on `[0, 100]`, 401 points; `a_min = 0.0` (no borrowing), `a_max = 100.0`. `configs/dlh_3b_hank_steady_state_validation.toml` `[fixture]`; `economics/grids.py` `build_asset_grid`. |
| Productivity states | `z ∈ {0.5, 1.5}` two-state CTMC with intensities `q_low_to_high = q_high_to_low = 0.25`. Same config; `economics/grids.py` `build_idiosyncratic_generator` (rows sum 0). |
| Distribution | `g(a,z)` shaped `(states=2, assets=401)`; solved from `G^T g = 0` (`solvers/distribution_kfe.py`). |
| Aggregate states | none (steady state); transition solved pathwise in DLH-3C/3D (`solvers/hank_household_transition.py`, `solvers/hank_kfe_transition.py`). |
| Regional dimension | none. Single-region validation fixture (accepted DLH-3A contracts). |

No two-asset code exists anywhere in `src/`:

- grep for `chi0|chi1|adjust|illiquid|borrow|rb_gap|two_asset` across `src/deep_learning_hank/**` returns only Tier-0 comments about "price-adjustment" scope and Rotemberg cost — **no adjustment-cost / second-asset implementation**.
- `solve_hank_household` signature (line 328-347) has exactly one `asset_grid` and one `real_return` argument.

## 3. Matlab state-space evidence (read-only reference)

| Object | Evidence (`HANK_2ASSETS_HJB.m`, `multi_prov_HANK_12sts.m`) |
|---|---|
| Household state | `(b, ah, z)`: liquid asset `b`, illiquid asset `ah`, productivity `z`. State arrays `bbb = zeros(I,J,Nz)`, `aaah = zeros(I,J,Nz)`, `zzz = zeros(I,J,Nz)` (HJB lines ~30-40). |
| Liquid asset | `b ∈ [bmin, bmax] = [-2, 5]`, `I = 20` points (`multi_prov_HANK_12sts.m` `grid.I`, `grid.bmin`, `grid.bmax`). Return `rb` with borrowing premium: `Rb = rb.*(bbb>=0) + rb_neg.*(bbb<0)`, `rb_neg = rb + rb_gap` (HJB lines 70-72). |
| Illiquid asset | `ah ∈ [amin, amax] = [0, 10]`, `J = 20` points. Return with curvature: `raah = rah.*(1 - 0.1*(ahmax./ah).^(-9))` (HJB line 82); `rah` determined by the firm block (`HANK_firm.m`: `ra0 = rk - delta + divrate`). |
| Productivity | `z ∈ [zmin, zmax] = [0.8, 1.3]`, `Nz = 2`; generator `la_mat` (rows sum 0; symmetric rate 1/3), `Bswitch` block (HJB lines 41-47). |
| Distribution | `g(b,ah,z)` density on `(I,J,Nz)`; normalized by grid measure `db*dah`. |
| Regional dimension | 31 provinces (`N_prov = 31`), per-province `Zt`/`alpha` calibrated from data, inter-province spillover matrices (`mpHANK_equilibrium_2000.m`, `main.m`). |

## 4. Grid-dimension comparison table

| Grid | Python (current) | Matlab (legacy) |
|---|---|---|
| Liquid asset points | 401 (`[0,100]`) | 20 (`[-2,5]`) |
| Illiquid asset points | — | 20 (`[0,10]`) |
| Productivity states | 2 (`{0.5,1.5}`) | 2 (`[0.8,1.3]`) |
| Total state grid | 2 × 401 | 20 × 20 × 2 |

## 5. A / B / L / Z meaning table (confirmed semantics)

| Symbol | Python (current) | Matlab (legacy) |
|---|---|---|
| **A** | `A_hh = ∫ a dg` — aggregate household liquid-asset **demand** (`solvers/hank_steady_state.py` `distribution.mean_assets`) | `Aht = ∫ ah dg` — aggregate **illiquid (capital)** holdings (`HANK_2ASSETS_HJB.m` line ~363) |
| **B** | constant real bond **supply**, `B = 10` (`configs/dlh_3b_...toml` `[fiscal] B`; cleared via `R_asset = A_hh - B`) | `Bt = ∫ b dg` — aggregate **liquid holdings**; note Matlab also uses `B` for the HJB iteration matrix `(1/Delta+rho)*speye - A` — symbol overloaded |
| **L** | `N_hh = ∫ z n dg` — aggregate effective labor supply (cleared vs `N`: `R_labor = N_hh - N`) | `Lt = ∫ z·l·g db dah` — aggregate effective labor |
| **Z** | aggregate productivity `Z = 1.0` (`configs/...toml` `[production] Z`; `Y = Z·N`) | province productivity `Zt` (data-calibrated; `Y = Z K^α L^(1-α)`) |

**Prohibition honored:** no symbol mapping is asserted without the codebase qualifier. In particular `B` (Python = supply) must never be conflated with `Bt` (Matlab = demand), and Python `chi` (labor disutility scale, `configs/...toml` `[fixture] chi = 0.70`) must never be conflated with Matlab `CHI` (asset adjustment cost, `multi_prov_HANK_12sts.m` `CHI.chi0=0.1`, `CHI.chi1=2`, `CHI.a_bar=1e-6`).

## 6. Conclusion

- Python: **one-asset `(a,z)`**, consistent with accepted DLH-3A contracts (single liquid risk-free real bond, no second asset, no adjustment cost, no borrowing).
- Matlab: **two-asset `(b,ah,z)`**, with adjustment cost, borrowing premium, illiquid capital return, and 31-province structure.
- Structural state-space mismatch confirmed between the current Python route and the legacy reference → contributes to terminal classification `BLOCKED_DLH_3D_R1A_HA_ALGORITHM_PARITY_MISMATCH` (see `DLH_3D_R1A_MAIN_REPORT.md` §12).
