# DLH-3 — Asset, Fiscal and Nominal Semantics Contract (DLH-3A)

- Date: 2026-08-19
- Author: DSH (bounded Builder)
- Authority: GitHub Issue #10 — DLH-3A
- Status: **SPECIFICATION ONLY — CANDIDATE for GPT/Owner review.** No implementation, no execution.

> This contract fixes the exact semantics of the liquid financial asset, the fiscal/bond/transfer closure, dividend incidence, and the continuous-time nominal (Fisher/Taylor) conventions for the minimal genuine single-region HANK validation economy. It must be read together with `DLH_3_MINIMAL_GENUINE_HANK_ARCHITECTURE_2026_08_19.md` and `DLH_3_STEADY_STATE_AND_DYNAMIC_EQUATION_CONTRACT_2026_08_19.md`.

## 1. Liquid financial asset `a` — exact semantics

- `a` is the household's holding of a **single liquid, risk-free real financial asset** (a claim on government bonds in the validation economy). In real terms, `a` pays the real return `r_t`.
- **`a` is NOT Tier-0 productive capital.** Tier-0's asset entered a Cobb-Douglas production function with `alpha_k` and depreciation `delta`; in DLH-3 the asset is only a store of value / bond claim and appears in the household budget and asset-market clearing, **not** in production. Do not silently reinterpret accepted Tier-0 code (`economics/firm.py`, `solvers/steady_state.py`) — those remain Tier-0 real-economy objects.
- Asset-domain convention: `a ∈ [ā, a_max]` with borrowing limit `ā ≤ 0` (to be given a fixture value later; no empirical assignment) and numerical upper truncation `a_max` (to be re-established for HANK in DLH-3E; Tier-0 `[0,200]` adequacy is **not** inherited).
- Boundary treatment: **state-constraint / no-outward-drift** — at the lower bound `ā`, `ȧ ≥ 0`; at the upper truncation `a_max`, `ȧ ≤ 0`. No reflected-process claim.

## 2. Asset-supply / asset-market clearing

- Government issues an **exogenous positive real bond supply** `B_t` (constant `B` in the steady-state validation fixture; a path in future DLH-3D dynamics).
- Households hold all bonds: aggregate asset demand `A_t = ∫ a dg_t`.
- **Asset-market clearing:** `A_t − B_t = 0`. Equivalent convention: households' aggregate financial wealth equals outstanding bond supply; no private capital, no equity, no international assets.

## 3. Fiscal block

- **Labor tax:** proportional tax on labor income at constant rate `τ_l ∈ (0,1)` (same convention as Tier-0; fixture value `0.15` is Tier-0 provenance, retained as starting validation-fixture convention, not a new calibration).
- **Government budget identity (constant `B` convention, no seigniorage, no debt-issuance change):**
  `r_t B + tr_t = τ_l w_t N_t`.
- **Lump-sum transfer closure:** `tr_t = τ_l w_t N_t − r_t B`. (If negative, a lump-sum tax; the formula is the identity, and the fiscal **residual** is computed, never set to zero by labeling.)
- **No** sovereign default, maturity structure, capital taxation, heterogeneous portfolios, or learned fiscal rules.

## 4. Firm profits / dividends incidence

- Aggregate firm profits (real): `Π_t = Y_t − w_t N_t − (φ_p/2) π_t² Y_t` (revenue minus wage bill minus Rotemberg adjustment cost).
- **Incidence:** `Π_t` is distributed lump-sum to households **equally per capita** (household mass normalized to 1). Each household receives `Π_t` in its cash flow regardless of `(a, z)`.
- **Profit accounting residual:** `R_profits = Π_t − [Y_t − w_t N_t − (φ_p/2) π_t² Y_t]` must be computed and reported.

## 5. Nominal semantics (continuous-time conventions)

- `π_t = Ṗ_t/P_t`: instantaneous inflation (log price-level derivative). Convention: the price level `P_t` is continuous (no jump) in future dynamic gates; `π_t` is a state-like object with law of motion `π̇_t`.
- `i_t`: nominal policy rate (per unit time, continuously compounded convention).
- **Fisher relation:** `i_t = r_t + π_t` (exact continuous-time convention; no `1 + i = (1+r)(1+π)` second-order term at the validation-fixture level). Fisher residual: `R_fisher = i_t − (r_t + π_t)`.
- **Taylor-type rule:** `i_t = r̄ + π_t + φ_π (π_t − π̄)`, with steady-state inflation target `π̄ = 0` and `φ_π > 1` (Taylor principle) as the baseline validation convention; an output-gap term is a documented optional extension, not part of the minimal contract. Residual: `R_taylor = i_t − [r̄ + π_t + φ_π(π_t − π̄)]`.
- **Steady-state normalization:** `π* = 0`, `i* = r* = r̄` (r̄ = steady-state real return determined in equilibrium, not imposed). Zero-shock consistency: at `π = π̄ = 0`, the Taylor rule returns `i = r̄`, so the Fisher relation holds identically at the steady state.

## 6. Aggregate consistency identities (contract)

- Household income decomposition (aggregate): `∫[(1−τ_l) w_t z n] dg + r_t A_t + tr_t + Π_t = (1−τ_l) w_t N_t + r_t B + tr_t + Π_t = w_t N_t + Π_t` (using asset-market clearing and the fiscal identity). With goods clearing `Y_t = C_t + (φ_p/2)π_t² Y_t`, this equals aggregate consumption `C_t`.
- Labor-market clearing: `N_t = ∫ z n dg` equals firm labor demand at the real wage (via `mc_t = w_t/A_t` and the markup).
- These are identities the implementation must **compute residuals for**, not set to zero.

## 7. No-empirical-value rule

- All nominal/fiscal parameters (`γ, χ, φ, ε, φ_p, φ_π, r̄, τ_l, ā, B, z_l, z_h, λ_lh, λ_hl, A_t`) are **fixture-level unknowns** at DLH-3A. Numeric validation-fixture values belong to a later implementation Issue, and every fixture remains labeled `VALIDATION_FIXTURE_NOT_CALIBRATION`.
