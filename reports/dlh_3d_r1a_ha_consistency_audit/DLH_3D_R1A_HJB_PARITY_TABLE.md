# DLH-3D-R1A — HJB Parity Table (Python vs Matlab)

- Date: 2026-08-20
- Authority: GitHub Issue #14 (OPEN), activation comment `5355380189`; canonical spec `tasks/DLH_3B_R1_HA_ALGORITHM_PARITY_AUDIT_2026_08_20.md`
- Type: `SCIENTIFIC_AUDIT_ONLY`; no modification; no numerical execution.

## 1. HJB specification comparison

| Aspect | Python (current) | Matlab (legacy `HANK_2ASSETS_HJB.m`) | Match |
|---|---|---|---|
| State variables | `V(a, z)`, one asset `a` | `V(b, ah, z)`, two assets `b`, `ah` | **DIFFERENT** |
| Control variables | consumption `c`; static labor `n` | consumption `c`; static labor `l`; illiquid-asset transfer `d` | **DIFFERENT** (extra `d`) |
| Utility | `u(c)=c^(1-γ)/(1-γ)`, `γ=2` (`economics/preferences.py`) | `alphac*C.^(1-ga)/(1-ga)`, `ga=2`, `alphac=1` (HJB line ~110) | SAME family |
| Labor disutility | `v(n)=χ n^(1+1/φ)/(1+1/φ)`, `χ=0.70`, `φ=1.0` (`solvers/hank_household_steady_state.py`) | `alphal*l.^(1+1/frisch_l)/(1+1/frisch_l)`, `frisch_l=0.2`, `alphal=1` (HJB line ~112; `multi_prov_HANK_12sts.m`) | SAME family, different fixture params |
| Labor FOC | `v'(n) = (1-τ_l) w z V_a`, KKT-clipped to `[0, n_max=5]` (`labor_policy`) | `lab_solve2.m`: `l = (alphac/alphal (1-tau) w z)^frisch_l * (l(1-tau)w z + tempMat)^(-ga*frisch_l)` (static FOC, `fzero` per node) | SAME family |
| Cash-flow / drift | `ȧ = (1-τ_l) w z n + r a + tr + Π − c` | `s = (1-tau)w z l + Rb b + Tt − Cmin − dh − cost(dh,ah) − C` (HJB line ~263) | DIFFERENT: Matlab adds adjustment transfer `dh` and cost; Python none |
| Marginal values | forward/backward differences of `V` along `a`, boundary via constrained-consumption marginal (`_policy_from_value`) | `VbF/VbB` along `b`, `VahF/VahB` along `ah`; boundaries `VbF(I,:)=u'(c0)`, `VbB(1,:)=u'(c0)`, `VahF(:,J)=0`, `VahB(:,1)=0` | SAME upwind family; boundary details differ |
| Consumption FOC | `c = u'^{-1}(V_a)` (3 candidates) | `C_B/C_F/C_0` with upwind indicators `Ic_B/Ic_F/Ic_0` | SAME |
| **Adjustment cost `chi(d,a)`** | **absent** (grep: no `chi0/chi1/adjust/illiquid` code in `src/`) | **present**: `HANK3_FOC.m` inaction band `d = (min(pa/pb−1+chi0,0)+max(pa/pb−1−chi0,0))*a/chi1`; `HANK3_cost.m` cost `chi0*|d| + chi1*d^2/2 * max(a,a_bar)^(-1)`; `CHI.chi0=0.1`, `chi1=2`, `a_bar=1e-6` | **DIFFERENT** (key finding) |
| Asset transfer choice | none (single asset) | `dh` between `b` and `ah` from `HANK3_FOC` evaluated at `(V_ah,V_b)` combinations (`dhBB/dhBF/dhFB/dhFF`) | **DIFFERENT** |
| Borrowing premium | none (`a_min=0.0`) | `rb_neg = rb + rb_gap` for `b<0` | **DIFFERENT** |
| Illiquid return curvature | none | `raah = rah*(1 − 0.1*(ahmax/ah)^(-9))` | **DIFFERENT** |
| Upwind scheme | 3-candidate (zero-drift / forward / backward) Hamiltonian selection | forward/backward differences with feasibility indicators; zero-drift branch `C_0`, `l_0` | SAME family |
| Boundary treatment | state-constraint / no-outward-drift: `drift[:,0] = max(drift[:,0],0)`, `drift[:,-1] = min(drift[:,-1],0)` | `b` boundaries via constrained marginal; `ah` boundaries `VahF(:,J)=0`, `VahB(:,1)=0`; forced `Idh_B(I,:,:)=1` at `b` upper | DIFFERENT conventions |
| Value iteration | `(ρ+1/Δ)I − G` pseudo-time, `Δ=1000` (`hank_household_steady_state.py`) | `(1/Delta+rho)*speye − A`, `Delta=1000`, `crit=1e-7` (`multi_prov_HANK_12sts.m`) | SAME |

## 2. Key confirmations requested by the Issue

### 2.1 Does `chi(d,a)` exist?

- **In Matlab: YES.** `HANK3_FOC.m` + `HANK3_cost.m`, parameters `CHI.chi0=0.1`, `CHI.chi1=2`, `CHI.a_bar=1e-6` (`multi_prov_HANK_12sts.m`). Mechanism: household transfers amount `d` between liquid `b` and illiquid `ah` only when the marginal-value ratio leaves the inaction band `[1−chi0, 1+chi0]`; the transfer is proportional to `a/chi1`; the resource cost is `chi0*|d| + chi1*d^2/2 * max(a,a_bar)^(-1)`.
- **In Python: NO.** No adjustment cost, no second asset, no inaction band. The only "chi" in Python is the labor-disutility scale `χ = 0.70` (`configs/dlh_3b_hank_steady_state_validation.toml` `[fixture] chi`), a **different object** with a colliding name.

### 2.2 If it exists, what are `d` and `a`?

(Matlab only, for the record) `d` = illiquid-asset purchase/transfer amount (choice), `a` = illiquid asset holdings `ah`; the two assets are coupled through the adjustment cost and the budget flow `s` (each household's liquid drift is reduced by `dh` and its cost, and the illiquid position moves by `dh`).

## 3. Conclusion

The HJB **numerical methodology** (continuous-time upwind HJB, pseudo-time value iteration, endogenous static labor, CRRA) is the same HACT family in both codebases; the **economic problem** differs: Python solves the one-asset HJB, Matlab solves the two-asset HJB with adjustment cost, borrowing premium, and illiquid-return curvature. → structural parity mismatch (contributes to `BLOCKED_DLH_3D_R1A_HA_ALGORITHM_PARITY_MISMATCH`).
