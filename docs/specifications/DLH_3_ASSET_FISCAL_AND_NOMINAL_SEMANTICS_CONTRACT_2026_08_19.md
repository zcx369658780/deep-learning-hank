# DLH-3 — Asset, Fiscal and Nominal Semantics Contract (DLH-3A)

- Date: 2026-08-19 (R1 revision 2026-08-20)
- Author: DSH (bounded Builder)
- Authority: GitHub Issue #10 — DLH-3A; R1 correction per authoritative review comment id `5348615886`.
- Status: **SPECIFICATION ONLY — R1 CANDIDATE for GPT/Owner review.** No implementation, no execution.

> This contract fixes the exact semantics of the liquid financial asset, the fiscal/bond/transfer closure, dividend incidence, and the continuous-time nominal (Fisher/Taylor) conventions for the minimal genuine single-region HANK validation economy. It must be read together with `DLH_3_MINIMAL_GENUINE_HANK_ARCHITECTURE_2026_08_19.md` and `DLH_3_STEADY_STATE_AND_DYNAMIC_EQUATION_CONTRACT_2026_08_19.md`.

## 1. Liquid financial asset `a` — exact semantics

- `a` is the household's holding of a **single liquid, risk-free real financial asset** (a claim on government bonds in the validation economy). In real terms, `a` pays the real return `r_t`.
- **`a` is NOT Tier-0 productive capital.** Tier-0's asset entered a Cobb-Douglas production function with `alpha_k` and depreciation `delta`; in DLH-3 the asset is only a store of value / bond claim and appears in the household budget and asset-market clearing, **not** in production. Do not silently reinterpret accepted Tier-0 code (`economics/firm.py`, `solvers/steady_state.py`) — those remain Tier-0 real-economy objects.
- Asset-domain convention: `a ∈ [ā, a_max]` with borrowing limit `ā ≤ 0` (to be given a fixture value later; no empirical assignment) and numerical upper truncation `a_max` (to be re-established for HANK in DLH-3E; Tier-0 `[0,200]` adequacy is **not** inherited).
- Boundary treatment: **state-constraint / no-outward-drift** — at the lower bound `ā`, `ȧ ≥ 0`; at the upper truncation `a_max`, `ȧ ≤ 0`. No reflected-process claim.
- **Notation (R1):** aggregate household liquid assets are `A^hh_t = ∫ a dg_t` (household mass normalized to 1). Aggregate productivity is `Z_t` (used in production `Y_t = Z_t N_t`). The R0 collision in which a single symbol `A_t` denoted both objects is removed by freeze (review finding 1).

## 2. Asset-supply / asset-market clearing

- Government issues an **exogenous positive real bond supply `B`, frozen constant through DLH-3B/3C/3D** (`B_t ≡ B`, `Ḃ ≡ 0`). Any time-varying debt path or debt-accumulation law `Ḃ` is **deferred** to a separately authorized fiscal extension and is NOT part of the minimal validation closure (review finding 5).
- Households hold all bonds: aggregate asset demand `A^hh_t = ∫ a dg_t`.
- **Asset-market clearing:** `A^hh_t − B = 0`. Equivalent convention: households' aggregate financial wealth equals outstanding bond supply; no private capital, no equity, no international assets.
- Asset-market residual: `R_asset = A^hh_t − B` (must be computed, never set to zero by labeling).

## 3. Fiscal block

- **Labor tax:** proportional tax on labor income at constant rate `τ_l ∈ (0,1)` (same convention as Tier-0; fixture value `0.15` is Tier-0 provenance, retained as starting validation-fixture convention, not a new calibration).
- **Government budget identity (constant-`B` convention, no seigniorage, no debt issuance/accumulation):**
  `r_t B + tr_t = T_t`, with tax revenue `T_t = τ_l w_t N_t`.
- **Lump-sum transfer closure:** `tr_t = τ_l w_t N_t − r_t B`. (If negative, a lump-sum tax; the formula is the identity, and the fiscal **residual** is computed, never set to zero by labeling.)
- Fiscal residual: `R_fiscal = τ_l w_t N_t − r_t B − tr_t`.
- **No** sovereign default, maturity structure, capital taxation, heterogeneous portfolios, or learned fiscal rules.

## 4. Firm profits / dividends incidence

- Aggregate firm profits (real): `Π_t = Y_t − w_t N_t − (φ_p/2) π_t² Y_t` (revenue minus wage bill minus Rotemberg adjustment cost).
- **Incidence:** `Π_t` is distributed lump-sum to households **equally per capita** (household mass normalized to 1). Each household receives `Π_t` in its cash flow regardless of `(a, z)`.
- **Profit accounting residual:** `R_profits = Π_t − [Y_t − w_t N_t − (φ_p/2) π_t² Y_t]` must be computed and reported.

## 5. Nominal semantics (continuous-time conventions)

- `π_t = Ṗ_t/P_t`: instantaneous inflation (log price-level derivative). Convention: the price level `P_t` is continuous (no jump) in future dynamic gates; `π_t` is a state-like object with law of motion `π̇_t`.
- `i_t`: nominal policy rate (per unit time, continuously compounded convention).
- **Fisher relation:** `i_t = r_t + π_t` (exact continuous-time convention; no `1 + i = (1+r)(1+π)` second-order term at the validation-fixture level). Fisher residual: `R_fisher = i_t − (r_t + π_t)`.
- **Taylor-type rule (R1 freeze, review finding 4):** `i_t = r̄ + π̄ + φ_π (π_t − π̄) + ε^i_t`, with:
  - steady-state inflation target `π̄ = 0`;
  - `φ_π > 1` (Taylor principle: the **total** nominal-rate response to an inflation deviation `π_t − π̄` is exactly `φ_π`, because the constant terms `r̄ + π̄` do not depend on `π_t`);
  - `ε^i_t = 0` in DLH-3B and DLH-3C (zero-shock consistency); the future DLH-3D monetary-policy innovation enters **only** through `ε^i_t`;
  - an output-gap term is a documented optional extension, not part of the minimal contract.
  - Taylor residual: `R_taylor = i_t − [r̄ + π̄ + φ_π (π_t − π̄) + ε^i_t]`.
- **Steady-state normalization:** `π* = π̄ = 0`, `i* = r* = r̄` (r̄ = steady-state real return determined in equilibrium, not imposed). Zero-shock consistency: at `π_t = π̄ = 0` and `ε^i_t = 0`, the Taylor rule returns `i_t = r̄`, so the Fisher relation holds identically at the steady state.

## 6. Aggregate consistency identities (contract)

### 6.1 Aggregate household wealth-flow identity (R1, review finding 6)

Aggregating the household budget `ȧ = (1−τ_l) w_t z n + r_t a + tr_t + Π_t − c` over the distribution (mass 1) gives the **aggregate wealth-flow identity**:

`Ȧ^hh_t = (1−τ_l) w_t N_t + r_t A^hh_t + tr_t + Π_t − C_t`,

with `N_t = ∫ z n dg` (aggregate effective labor supplied) and `C_t = ∫ c dg`.

### 6.2 Consistency chain (must be verified from computed objects)

1. Constant-`B` asset clearing gives `A^hh_t = B` and hence `Ȧ^hh_t = 0`.
2. The wealth-flow identity then implies `0 = (1−τ_l) w_t N_t + r_t B + tr_t + Π_t − C_t`.
3. The fiscal identity `tr_t = τ_l w_t N_t − r_t B` then gives `C_t = w_t N_t + Π_t`.
4. The profits identity `Π_t = Y_t − w_t N_t − (φ_p/2) π_t² Y_t` and goods/resource clearing `Y_t = C_t + (φ_p/2) π_t² Y_t + G_t` (`G_t = 0` in the minimal validation) imply `C_t = w_t N_t + Π_t = Y_t − (φ_p/2) π_t² Y_t`. All three expressions for `C_t` agree; this is a cross-consistency **residual check**, not an assumption.

The R0 statement `C = wN + Π = ∫cash_flow dg − (rA + tr)` was arithmetically false under the R0 cash-flow definition and is **removed** in R1; it is replaced by the chain above.

### 6.3 Labor market

- Aggregate effective labor supplied: `N^s_t = ∫ z n dg`.
- Firm labor demand is defined by technology: `N^d_t = Y_t / Z_t` (production requires exactly `Y_t/Z_t` units of effective labor; review finding 7).
- Labor-market residual: `R_labor = N^s_t − N^d_t`.
- The markup relation is a **pricing** condition, not a labor-demand curve: real marginal cost `mc_t = w_t / Z_t` (cost minimization), and the price-setting/NKPC block determines `mc_t` (steady state `mc = 1/μ`, hence `w = Z/μ`). Household labor aggregation, the production identity `Y = Z N`, and price-setting must not be conflated.

## 7. No-empirical-value rule

- All nominal/fiscal/structural parameters (`γ, χ, φ, ε, φ_p, φ_π, r̄, τ_l, ā, B, z_l, z_h, λ_lh, λ_hl, Z_t`, Taylor target `π̄ = 0`) are **fixture-level unknowns** at DLH-3A. Numeric validation-fixture values belong to a later implementation Issue, and every fixture remains labeled `VALIDATION_FIXTURE_NOT_CALIBRATION`.

## 8. R1 revision log (semantics contract)

- §1: introduced distinct notation `Z_t` (productivity) and `A^hh_t` (aggregate liquid assets); removed the `A_t` symbol collision (finding 1).
- §2: froze `B_t ≡ B` constant through 3B–3D with `Ḃ ≡ 0`; deferred any varying-debt path (finding 5).
- §3: fiscal identities written against constant `B` only; explicit `Ḃ ≡ 0`, no seigniorage, no issuance (finding 5).
- §5: Taylor rule replaced by `i_t = r̄ + π̄ + φ_π(π_t − π̄) + ε^i_t` with `φ_π > 1` as the total response coefficient and `ε^i_t = 0` in 3B/3C (finding 4).
- §6: replaced the false subtraction identity with the aggregate wealth-flow identity and the full consistency chain (finding 6); labor-market residual defined via technology `N^d = Y/Z` with markup confined to pricing (finding 7).
