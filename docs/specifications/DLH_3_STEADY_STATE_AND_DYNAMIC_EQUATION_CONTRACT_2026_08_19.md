# DLH-3 — Steady-State and Dynamic Equation Contract (DLH-3A)

- Date: 2026-08-19
- Author: DSH (bounded Builder)
- Authority: GitHub Issue #10 — DLH-3A
- Status: **SPECIFICATION ONLY — CANDIDATE for GPT/Owner review.** No implementation, no execution.

> This is the equation-level contract for the minimal genuine single-region HANK validation economy. Conventions: continuous time, perfect foresight in future dynamic gates, household mass normalized to 1, all variables real unless nominal (i, π) is explicit. `Q` is the 2×2 idiosyncratic CTMC generator / intensity matrix (rows sum 0; off-diagonals ≥ 0); `G` is the full household transition generator including asset drift (rows sum 0).

## 1. Household block

### 1.1 State and controls
- State: `(a, z)`, `a ∈ [ā, a_max]`, `z ∈ {z_l, z_h}`.
- Controls: consumption `c ≥ 0`; endogenous static labor `n ∈ [0, n̄]`.
- Utility (separable): `U(c, n) = u(c) − v(n)`, `u(c) = c^(1−γ)/(1−γ)`, `v(n) = χ n^(1+1/φ)/(1+1/φ)`.

### 1.2 Cash-flow decomposition
`cash_flow(a, z; t) = (1−τ_l) w_t z n(a,z,t) + r_t a + tr_t + Π_t`

components:
- labor income `(1−τ_l) w_t z n`;
- liquid-asset return `r_t a`;
- fiscal transfer `tr_t`;
- firm profits/dividends `Π_t` (equal per capita).

Budget constraint: `ȧ = cash_flow − c`.

### 1.3 Time-dependent HJB (perfect foresight)
`ρ V(t,a,z) − ∂_t V(t,a,z) = max_{c,n} { U(c,n) + V_a(t,a,z) [cash_flow(a,z;t) − c] + Σ_{z′} Q[z,z′] (V(t,a,z′) − V(t,a,z)) }`

Boundary (state-constraint / no-outward-drift): lower bound `ȧ ≥ 0` at `a = ā`; upper truncation `ȧ ≤ 0` at `a = a_max`. No reflected-process claim.

### 1.4 FOCs
- Consumption: `u′(c) = V_a` → `c = u′⁻¹(V_a)`.
- **Endogenous static labor:** `v′(n) = (1−τ_l) w_t z V_a` → `n = v′⁻¹((1−τ_l) w_t z V_a)`. (Static; no new state dimension.)

### 1.5 Forward KFE
`∂_t g(t,a,z) = −∂_a[ ȧ(t,a,z) g(t,a,z) ] + Σ_{z′} Q[z′,z] g(t,a,z′) − Σ_{z′≠z} Q[z,z′] g(t,a,z)`

equivalently `∂_t g = −∂_a(ȧ g) + Qᵀ g` (with the generator convention). Mass conservation: `∫ g da dz = 1`; non-negativity `g ≥ 0`.

### 1.6 Steady-state reduction
At steady state (`∂_t V = 0`, `∂_t g = 0`):
- stationary HJB: `ρ V(a,z) = max_{c,n} { U(c,n) + V_a [cash_flow − c] + Q V }`;
- stationary KFE: `Gᵀ g = 0` (asset drift + idiosyncratic generator), with mass normalization.

This reduces exactly to the accepted Tier-0 stationary HJB/KFE *family* (Issue #5/#6) with the household income terms replaced by the HANK cash flow above — a deliberate, documented re-interpretation, not silent reuse.

## 2. Production / price-setting

### 2.1 Technology
`Y_t = A_t N_t`, `N_t = ∫ z n(a,z,t) g(t,a,z) da dz` (aggregate effective labor). `A_t` exogenous (constant `A` in steady state; path in future DLH-3D).

### 2.2 Markup / marginal cost
`μ = ε/(ε−1)` (markup); real marginal cost `mc_t = w_t / A_t`. (Perfectly substitutable labor ⇒ common real wage `w_t`.)

### 2.3 Rotemberg price adjustment (no Calvo price-age distribution)
Adjustment cost: `(φ_p/2) π_t² Y_t` (real resources, units of final output).

### 2.4 NKPC (continuous-time timing/sign convention, frozen here)
`π̇_t = ρ π_t − κ (mc_t − 1/μ)`, with `κ = (ε−1)/φ_p > 0`.

Timing/sign convention:
- `π_t = Ṗ_t/P_t`; `π̇_t = dπ_t/dt`; `ρ` = household discount parameter;
- sign: when real marginal cost is above the frictionless level `1/μ` (markup below `μ`), inflation is rising (`π̇_t > 0` at `π = 0`);
- steady state: `π = 0` and `mc = 1/μ` (markup `= μ`);
- the exact `κ` convention (`κ = (ε−1)/φ_p`) and the price-level continuity assumption are **frozen** at DLH-3A and must not be re-derived ad hoc at implementation.

### 2.5 Profits
`Π_t = Y_t − w_t N_t − (φ_p/2) π_t² Y_t`.

## 3. Monetary block

- Fisher: `i_t = r_t + π_t`; residual `R_fisher = i_t − r_t − π_t`.
- Taylor: `i_t = r̄ + π_t + φ_π (π_t − π̄)`, `π̄ = 0`, `φ_π > 1`; residual `R_taylor = i_t − r̄ − (1+φ_π) π_t` (with `π̄=0`).
- Steady state: `π* = 0`, `i* = r* = r̄`.

## 4. Fiscal / bond block

- Bonds: exogenous `B_t` (constant `B` in steady state); asset-market clearing `A_t = B_t`.
- Tax revenue: `T_t = τ_l w_t N_t`.
- Government budget: `r_t B_t + tr_t = T_t`; transfer closure `tr_t = T_t − r_t B_t`.
- Fiscal residual: `R_fiscal = T_t − r_t B_t − tr_t`.

## 5. Markets / residual objects (every later PASS depends on these, computed)

| Residual | Definition |
|---|---|
| HJB | `R_hjb = ρ V − ∂_t V − [U + V_a ȧ + Q V]` (steady state: `ρ V − [U + V_a ȧ + Q V]`) |
| KFE / mass | `R_kfe = ∂_t g + ∂_a(ȧ g) − Qᵀ g`; mass `|∫ g − 1|`; non-negativity `min g` |
| Asset market | `R_asset = A_t − B_t` |
| Labor market | `R_labor = N_t − N_t^d` (with `N_t^d` from firm demand via `mc_t = w_t/A_t` and markup) |
| Goods / resource | `R_goods = Y_t − C_t − (φ_p/2) π_t² Y_t − G_t` (`G_t = 0` in minimal validation) |
| Fiscal budget | `R_fiscal = τ_l w_t N_t − r_t B_t − tr_t` |
| Profits / dividends | `R_profits = Π_t − [Y_t − w_t N_t − (φ_p/2) π_t² Y_t]` |
| NKPC | `R_nkpc = π̇_t − ρ π_t + κ (mc_t − 1/μ)` |
| Fisher | `R_fisher = i_t − r_t − π_t` |
| Taylor | `R_taylor = i_t − r̄ − π_t − φ_π (π_t − π̄)` |

## 6. Cross-consistency (contract)

- Aggregate household income identity: `∫ cash_flow dg = (1−τ_l) w_t N_t + r_t A_t + tr_t + Π_t = w_t N_t + Π_t` (using clearing + fiscal identity).
- Goods-market consistency: with `C_t = ∫ c dg`, `R_goods = 0` implies `C_t = w_t N_t + Π_t = ∫ cash_flow dg − (r_t A_t + tr_t)`; the implementation must verify this from computed objects.

## 7. Future-gate note (non-authoritative here)

- DLH-3B: zero-inflation/zero-shock steady state — uses §1.6, §2.4 steady state, §3, §4, §5 (static residuals).
- DLH-3C: time-dependent household/KFE response — uses §1.3/§1.5 with externally prescribed small price/income paths; NK GE not closed.
- DLH-3D: full NK GE + first deterministic monetary innovation — uses the complete §1–§5 dynamic system.
- DLH-3E: HANK numerical robustness (asset domain, asset-grid refinement, **separate** aggregate-time discretization, horizon/terminal, reproducibility).
