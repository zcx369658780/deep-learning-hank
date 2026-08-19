# DLH-3 — Steady-State and Dynamic Equation Contract (DLH-3A)

- Date: 2026-08-19 (R1 revision 2026-08-20)
- Author: DSH (bounded Builder)
- Authority: GitHub Issue #10 — DLH-3A; R1 correction per authoritative review comment id `5348615886`.
- Status: **SPECIFICATION ONLY — R1 CANDIDATE for GPT/Owner review.** No implementation, no execution.

> This is the equation-level contract for the minimal genuine single-region HANK validation economy. Conventions: continuous time, perfect foresight in future dynamic gates, household mass normalized to 1, all variables real unless nominal (i, π) is explicit. `Q` is the 2×2 idiosyncratic CTMC generator / intensity matrix (rows sum 0; off-diagonals ≥ 0; diagonal = negative total outflow); `G` is the full household transition generator including asset drift (rows sum 0). Notation (R1): aggregate productivity `Z_t`; aggregate household liquid assets `A^hh_t = ∫ a dg_t`.

## 1. Household block

### 1.1 State and controls
- State: `(a, z)`, `a ∈ [ā, a_max]`, `z ∈ {z_l, z_h}`.
- Controls: consumption `c ≥ 0`; endogenous static labor `n ∈ [0, n̄]`.
- Utility (separable): `U(c, n) = u(c) − v(n)`, `u(c) = c^(1−γ)/(1−γ)`, `v(n) = χ n^(1+1/φ)/(1+1/φ)`.

### 1.2 Cash-flow decomposition
`cash_flow(a,z;t) = (1−τ_l) w_t z n(a,z,t) + r_t a + tr_t + Π_t`

components:
- labor income `(1−τ_l) w_t z n`;
- liquid-asset return `r_t a`;
- fiscal transfer `tr_t`;
- firm profits/dividends `Π_t` (equal per capita).

Budget constraint: `ȧ = cash_flow − c`.

### 1.3 Time-dependent HJB (perfect foresight)
`ρ V(t,a,z) − ∂_t V(t,a,z) = max_{c,n} { U(c,n) + V_a(t,a,z) [cash_flow(a,z;t) − c] + (Q V)(t,a,z) }`

where `(Q V)(t,a,z) = Σ_{z′} Q[z,z′] V(t,a,z′)`; because the generator rows sum to 0, this equals the expanded form `Σ_{z′} Q[z,z′] (V(t,a,z′) − V(t,a,z))` (the negative diagonal is the outflow, not an additional subtraction).

Boundary (state-constraint / no-outward-drift): lower bound `ȧ ≥ 0` at `a = ā`; upper truncation `ȧ ≤ 0` at `a = a_max`. No reflected-process claim.

### 1.4 FOCs
- Consumption: `u′(c) = V_a` → `c = u′⁻¹(V_a)`.
- **Endogenous static labor:** `v′(n) = (1−τ_l) w_t z V_a` → `n = v′⁻¹((1−τ_l) w_t z V_a)`. (Static; no new state dimension.)

### 1.5 Forward KFE — R1 (two algebraically equivalent forms; review finding 2)

**Compact form (frozen as the primary definition):**
`∂_t g(t,a,z) = −∂_a[ ȧ(t,a,z) g(t,a,z) ] + (Qᵀ g)(t,a,z)`

with `(Qᵀ g)(t,a,z) = Σ_{z′} Q[z′,z] g(t,a,z′)`.

**Expanded form (fully expanded, off-diagonal sums only):**
`∂_t g(t,a,z) = −∂_a[ ȧ(t,a,z) g(t,a,z) ] + Σ_{z′≠z} Q[z′,z] g(t,a,z′) − ( Σ_{z′≠z} Q[z,z′] ) g(t,a,z)`

**Algebraic equivalence:** under the generator convention (rows sum 0, diagonal `Q[z,z] = −Σ_{z′≠z} Q[z,z′]`), `(Qᵀ g)(z) = Q[z,z] g(z) + Σ_{z′≠z} Q[z′,z] g(z′) = Σ_{z′≠z} Q[z′,z] g(z′) − (Σ_{z′≠z} Q[z,z′]) g(z)`. The two forms are therefore identical; the R0 expanded form, which summed over all `z′` in the incoming term and then subtracted off-diagonal outflow again, double-counted the outflow and is **removed** in R1.

Mass conservation: `∫ g da dz = 1`; non-negativity `g ≥ 0`.

### 1.6 Steady-state reduction
At steady state (`∂_t V = 0`, `∂_t g = 0`):
- stationary HJB: `ρ V(a,z) = max_{c,n} { U(c,n) + V_a [cash_flow − c] + Q V }`;
- stationary KFE: `Gᵀ g = 0` (asset drift + idiosyncratic generator), with mass normalization.

This reduces exactly to the accepted Tier-0 stationary HJB/KFE *family* (Issue #5/#6) with the household income terms replaced by the HANK cash flow above — a deliberate, documented re-interpretation, not silent reuse.

## 2. Production / price-setting

### 2.1 Technology
`Y_t = Z_t N_t` with `N_t` = aggregate effective labor used in production (in equilibrium `N_t = N^s_t = N^d_t`, see §5). `Z_t` exogenous (constant `Z` in steady state; path in future DLH-3D). Aggregate productivity `Z_t` is **not** the same symbol as aggregate assets `A^hh_t` (review finding 1).

### 2.2 Markup / marginal cost
`μ = ε/(ε−1)` (markup); real marginal cost `mc_t = w_t / Z_t` (cost minimization: producing one unit of the final good requires `1/Z_t` units of effective labor at wage `w_t`, so `mc_t = w_t/Z_t`). Perfectly substitutable labor ⇒ common real wage `w_t`. The markup relation is a pricing condition: in steady state `mc = 1/μ` and hence `w = Z/μ`.

### 2.3 Rotemberg price adjustment (no Calvo price-age distribution)
Adjustment cost: `(φ_p/2) π_t² Y_t` (real resources, units of final output). Continuum of symmetric infinitesimal firms `j`; firm `j` faces demand `y_{j,t} = Y_t (p_{j,t}/P_t)^(−ε)`, technology `y_{j,t} = Z_t n_{j,t}`, own-price inflation `π_{j,t} = ṗ_{j,t}/p_{j,t}`, and real profits `Π_{j,t} = (p_{j,t}/P_t) y_{j,t} − mc_t y_{j,t} − (φ_p/2) π_{j,t}² Y_t`. Firms discount real profits at the household rate `ρ` (representative-firm valuation convention, frozen at DLH-3A; exact heterogeneous-SDF valuation is a documented extension, not part of the minimal contract).

### 2.4 NKPC — R1 (derived from the stated convention; review finding 3)

**Step 1 — firm price-setting FOC (exact, nonlinear).** The firm maximizes `∫₀^∞ e^{−ρs} Π_{j,s} ds` subject to `ṗ_{j,t} = π_{j,t} p_{j,t}` (state `p_{j,t}`, control `π_{j,t}`). The current-value Hamiltonian is

`H = (p_j/P)^{1−ε} Y − mc Y (p_j/P)^{−ε} − (φ_p/2) π_j² Y + λ π_j p_j`.

Optimality conditions (symmetric equilibrium `p_j = P`, `π_j = π`):

- FOC `π_j`: `−φ_p π_j Y + λ p_j = 0` ⇒ `λ = φ_p π Y/P`;
- costate: `λ̇ = ρλ − H_{p_j} = ρλ − Y(1 − ε + ε mc)/P − λ π`.

Differentiating the FOC (`λ = φ_p π Y/P`) and equating with the costate gives, after canceling the common `−φ_p π² Y/P` term,

`φ_p π̇ + φ_p π Ẏ/Y = ρ φ_p π − (1 − ε + ε mc)`,

i.e. the **exact nonlinear symmetric-equilibrium FOC**

`π̇_t = ρ π_t − (ε/φ_p)(mc_t − 1/μ) − π_t (Ẏ_t/Y_t)`,

using `1/μ = (ε−1)/ε`. This is the equation-level derivation the R0 candidate lacked.

**Step 2 — frozen operational NKPC (explicitly labeled local linearization).** Near the zero-inflation steady state (`π* = 0`, `Ẏ* = 0`) the product term `−π(Ẏ/Y)` is second order. The **frozen operational equation** for DLH-3B/3C/3D is the local linearization:

`π̇_t = ρ π_t − κ (mc_t − 1/μ)`, with `κ ≡ ε/φ_p > 0`.

This is a **linearized** object: it is not an exact nonlinear Phillips curve. The exact nonlinear FOC of Step 1 remains the reference definition from which the linearization is taken; implementation must not silently re-derive either form.

**Step 3 — sign and timing convention (algebraically consistent).** `π_t = Ṗ_t/P_t`; `π̇_t = dπ_t/dt`; `ρ` = household discount rate. At `π_t = 0`, `mc_t > 1/μ` implies `π̇_t = −κ(mc_t − 1/μ) < 0`. This minus sign is the continuous-time expression of forward-looking price-setting: the bounded solution of the linearized law is `π_t = κ ∫_t^∞ e^{−ρ(s−t)} (mc_s − 1/μ) ds`, so a marginal-cost path above the frictionless level `1/μ` implies a **positive inflation level** (`π_t > 0`), matching the standard discrete-time NKPC `π_t = β π_{t+1} + κ (mc_t − 1/μ)`. The R0 prose claim "`mc > 1/μ` implies `π̇ > 0` at `π = 0`" contradicted its own displayed equation and is **corrected** in R1. Steady state: `π = 0` and `mc = 1/μ` (markup `= μ`).

**Step 4 — coefficient convention (no mixing).** `κ = ε/φ_p` is the coefficient on the **level** deviation `mc_t − 1/μ`. If a log-deviation form is ever used, `mc_t − 1/μ ≈ (1/μ) log(mc_t/mc*)` with `mc* = 1/μ` gives the coefficient `(ε−1)/φ_p` on `log(mc_t/mc*)`. R1 freezes the level-deviation convention with `κ = ε/φ_p` and forbids mixing the level object with the log-deviation coefficient.

### 2.5 Profits
`Π_t = Y_t − w_t N_t − (φ_p/2) π_t² Y_t`.

## 3. Monetary block

- Fisher: `i_t = r_t + π_t`; residual `R_fisher = i_t − r_t − π_t`.
- Taylor (R1 freeze, review finding 4): `i_t = r̄ + π̄ + φ_π (π_t − π̄) + ε^i_t`, `π̄ = 0`, `φ_π > 1` (the total nominal-rate response to `π_t − π̄` is exactly `φ_π`), `ε^i_t = 0` in DLH-3B/3C; the future DLH-3D monetary innovation acts through `ε^i_t`. Residual `R_taylor = i_t − [r̄ + π̄ + φ_π (π_t − π̄) + ε^i_t]` (with `π̄ = 0` this is `i_t − r̄ − φ_π π_t − ε^i_t`).
- Steady state: `π* = 0`, `i* = r* = r̄`.

## 4. Fiscal / bond block

- Bonds: exogenous **constant** supply `B` through DLH-3B/3C/3D (`B_t ≡ B`, `Ḃ ≡ 0`; review finding 5); asset-market clearing `A^hh_t = B`. A time-varying debt path / `Ḃ` law is deferred to a separately authorized fiscal extension.
- Tax revenue: `T_t = τ_l w_t N_t`.
- Government budget (no seigniorage, no issuance): `r_t B + tr_t = T_t`; transfer closure `tr_t = T_t − r_t B`.
- Fiscal residual: `R_fiscal = T_t − r_t B − tr_t`.

## 5. Markets / residual objects (every later PASS depends on these, computed)

| Residual | Definition |
|---|---|
| HJB | `R_hjb = ρ V − ∂_t V − [U + V_a ȧ + Q V]` (steady state: `ρ V − [U + V_a ȧ + Q V]`) |
| KFE / mass | `R_kfe = ∂_t g + ∂_a(ȧ g) − Qᵀ g`; mass `|∫ g − 1|`; non-negativity `min g` |
| Asset market | `R_asset = A^hh_t − B` |
| Labor market | `R_labor = N^s_t − N^d_t`, with `N^s_t = ∫ z n dg` (household supply) and `N^d_t = Y_t/Z_t` (technological firm demand; review finding 7) |
| Goods / resource | `R_goods = Y_t − C_t − (φ_p/2) π_t² Y_t − G_t` (`G_t = 0` in minimal validation) |
| Fiscal budget | `R_fiscal = τ_l w_t N_t − r_t B − tr_t` |
| Profits / dividends | `R_profits = Π_t − [Y_t − w_t N_t − (φ_p/2) π_t² Y_t]` |
| Wealth flow (R1) | `R_wealth = Ȧ^hh_t − [(1−τ_l) w_t N_t + r_t A^hh_t + tr_t + Π_t − C_t]` |
| NKPC | `R_nkpc = π̇_t − ρ π_t + κ (mc_t − 1/μ)` (frozen linearized form, §2.4) |
| Fisher | `R_fisher = i_t − r_t − π_t` |
| Taylor | `R_taylor = i_t − [r̄ + π̄ + φ_π (π_t − π̄) + ε^i_t]` |

## 6. Cross-consistency (contract; R1 — review finding 6)

- **Aggregate household wealth-flow identity:** `Ȧ^hh_t = (1−τ_l) w_t N_t + r_t A^hh_t + tr_t + Π_t − C_t` (aggregation of the household budget over the distribution; mass 1).
- **Consistency chain (computed residual check):**
  1. constant-`B` asset clearing ⇒ `A^hh_t = B`, `Ȧ^hh_t = 0`;
  2. wealth-flow identity ⇒ `0 = (1−τ_l) w_t N_t + r_t B + tr_t + Π_t − C_t`;
  3. fiscal identity `tr_t = τ_l w_t N_t − r_t B` ⇒ `C_t = w_t N_t + Π_t`;
  4. profits identity and goods clearing ⇒ `C_t = Y_t − (φ_p/2) π_t² Y_t = w_t N_t + Π_t`.
- The R0 statement `C = wN + Π = ∫cash_flow dg − (rA + tr)` was arithmetically false under the R0 cash-flow definition (it omits `(1−τ_l)wN` and double-counts the tax rebate) and is **removed**; the chain above is the corrected cross-consistency contract.

## 7. Future-gate note (non-authoritative here)

- DLH-3B: zero-inflation/zero-shock steady state — uses §1.6, §2.4 steady state (`π = 0`, `mc = 1/μ`), §3 (`π̄ = 0`, `ε^i = 0`), §4, §5 (static residuals).
- DLH-3C: time-dependent household/KFE response — uses §1.3/§1.5 with externally prescribed small real paths `(w_t, r_t, tr_t, Π_t)`; NK GE not closed; `ε^i_t = 0`; nominal objects `(π_t, i_t)` may be reported consistently via Fisher/Taylor but do not feed the household block.
- DLH-3D: full NK GE + first deterministic monetary innovation — uses the complete §1–§5 dynamic system with the innovation entering through `ε^i_t`.
- DLH-3E: HANK numerical robustness (asset domain, asset-grid refinement, **separate** aggregate-time discretization, horizon/terminal, reproducibility).

## 8. R1 revision log (equation contract)

- §1.5: forward KFE rewritten in compact `Qᵀ` and expanded off-diagonal-only forms with a proof of algebraic equivalence; outflow double-count removed (finding 2).
- §1.3: HJB generator term written compactly with the identity `(QV)(z) = Σ Q[z,z′](V(z′)−V(z))` noted.
- §2.1/§2.2: `Z_t` for productivity (finding 1); `mc_t = w_t/Z_t` derived from cost minimization.
- §2.4: full Rotemberg derivation (demand, technology, profits, Hamiltonian, FOC, costate, symmetric equilibrium) → exact nonlinear FOC; frozen operational equation is the explicitly labeled local linearization `π̇ = ρπ − κ(mc − 1/μ)`, `κ = ε/φ_p`; sign convention made algebraically consistent; coefficient-mixing prohibition stated (finding 3).
- §3: Taylor rule replaced by `i_t = r̄ + π̄ + φ_π(π_t − π̄) + ε^i_t` (finding 4).
- §4: `B_t ≡ B` constant through 3B–3D with `Ḃ ≡ 0` (finding 5).
- §5: labor residual `R_labor = N^s_t − Y_t/Z_t`; wealth-flow residual added (findings 6, 7).
- §6: false subtraction identity replaced by wealth-flow identity + consistency chain (finding 6).
