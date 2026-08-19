# DLH-3 — Minimal Genuine Single-Region HANK Architecture (DLH-3A Equation/Architecture Freeze)

- Date: 2026-08-19
- Author: DSH (bounded Builder)
- Authority: GitHub Issue #10 — `DLH-3A: Minimal genuine single-region HANK architecture and equation freeze`
- Status: **SPECIFICATION ONLY — CANDIDATE for GPT/Owner review.** Zero model implementation, zero numerical execution. No D2 HANK result is claimed by this document.
- Working label: **minimal genuine single-region HANK validation economy** (continuous time).

> This document is the architecture-level freeze requested by Issue #10. It deliberately avoids the false shortcut of appending Fisher/NKPC/Taylor identities to the Tier-0 productive-capital economy and calling it HANK: dynamic household/distribution response and aggregate NK general equilibrium are separate successor subgates (DLH-3B/3C/3D/3E), none of which is authorized here.

## 1. Scientific purpose and boundary

- Tier-0 (Issues #5–#9) established D2 machine-diagnostic evidence for a small one-region **real HA/Aiyagari** benchmark on canonical domain `[0,200]` with the C200→F200→Q200 grid hierarchy. Tier-0 is **not** genuine HANK.
- DLH-3A fixes the auditable equation/semantics contract for the smallest single-region **heterogeneous-agent New Keynesian** validation economy that can later support monetary/nominal transmission diagnostics.
- This Issue does **not** authorize: model implementation, numerical execution, shock/transition/IRF simulation, calibration, or Results.

## 2. Owner deferral (Issue #10 §2) — final regional architecture remains open

- The single-region validation asset/production structure frozen here is a **DLH-3 validation route**, not an irreversible final NSR-HANK architecture.
- After the regional steady-state program is sufficiently formed, Owner/ChatGPT may retain, modify, or replace this validation structure.
- DSH must not present the DLH-3A choice as the final regional steady-state asset/production architecture.

## 3. Architecture overview

```
                     Aggregate productivity A_t
                                |
                                v
  [Production / price-setting]  Y_t = A_t N_t ; Rotemberg NKPC
            |  real wage w_t, real marginal cost mc_t, dividends Pi_t
            v
  [Household block]  (a, z) state ; controls c, n ; HJB ; forward KFE
            |  labor N_t = integral z n dg ; asset A_t = integral a dg
            v
  [Monetary block]  i_t, pi_t, r_t ; Fisher ; Taylor rule
            |
  [Fiscal / bond supply]  B_t, labor tax, lump-sum transfer, dividends
            |
  [Markets / residuals]  asset, labor, goods (incl. Rotemberg cost),
                         fiscal, profit accounting, NKPC, Fisher, Taylor
```

The loop is the single-region validation economy's NK general equilibrium, to be closed only in DLH-3D; DLH-3A specifies the equations and residuals that later gates must compute.

## 4. State variables, controls, prices, aggregates, residuals (summary table)

| Category | Objects |
|---|---|
| Household state | liquid financial asset `a` (scalar, real); idiosyncratic productivity `z ∈ {z_l, z_h}` (2-state CTMC) |
| Household controls | consumption `c ≥ 0`; **endogenous static labor supply `n ∈ [0, n̄]`** (no new state dimension) |
| Prices (real / nominal) | real wage `w_t`; real liquid return `r_t`; nominal policy rate `i_t`; inflation `π_t`; real marginal cost `mc_t` |
| Policy / fiscal | Taylor rule (φ_π convention); labor tax `τ_l`; government bonds `B_t`; lump-sum transfer `tr_t` |
| Aggregate objects | output `Y_t`, aggregate labor `N_t`, aggregate assets `A_t`, aggregate consumption `C_t`, dividends `Π_t`, markup `μ` |
| Residuals (must be computed, not labeled) | HJB; KFE/mass; asset market; labor market; goods/resource (incl. Rotemberg cost); fiscal budget; profit/dividend accounting; NKPC; Fisher; Taylor |

## 5. Component modules (equation-level contracts)

### 5.1 Household (continuous time)
- State: `(a, z)`; `a` = one **liquid / risk-free financial asset**; `z` = two-state idiosyncratic productivity CTMC (starting validation fixture; kept unless a strict equation-level inconsistency is identified — none is identified in this specification).
- Utility: separable `U(c, n) = u(c) − v(n)` with CRRA `u(c) = c^(1−γ)/(1−γ)` and convex labor disutility `v(n) = χ n^(1+1/φ)/(1+1/φ)` (Frisch elasticity `φ`; `γ, χ, φ` are fixture-level constants, no empirical values assigned here).
- **Endogenous static labor**: `v′(n) = (1−τ_l) w_t z V_a` (labor FOC is static; it adds a control, not a state).
- Budget/cash-flow: `ȧ = (1−τ_l) w_t z n + r_t a + tr_t + Π_t − c`.
- Time-dependent HJB (perfect foresight, state-constraint / no-outward-drift boundary): see `DLH_3_STEADY_STATE_AND_DYNAMIC_EQUATION_CONTRACT_2026_08_19.md`.
- Forward KFE for distribution dynamics; steady-state reduction to stationary HJB/KFE.

### 5.2 Production / price-setting (minimal; no productive capital)
- Labor-based production with aggregate productivity: `Y_t = A_t N_t` (constant returns in effective labor; `A_t` exogenous path in future dynamics).
- Monopolistic competition with markup `μ = ε/(ε−1)`; real marginal cost `mc_t = w_t / A_t`.
- **Rotemberg** nominal price adjustment (not Calvo price-age distribution): adjustment cost `(φ_p/2) π_t² Y_t`; NKPC with explicit continuous-time timing/sign convention (see semantics contract).
- Firm profits/dividends: `Π_t = Y_t − w_t N_t − (φ_p/2) π_t² Y_t`, distributed lump-sum (equal per-capita).
- **No** productive-capital accumulation, investment adjustment, Tobin-q, or capital-arbitrage dynamics in DLH-3A.

### 5.3 Monetary block
- Nominal policy rate `i_t`; inflation `π_t`; real liquid return `r_t`; Fisher relation; Taylor-type rule; steady-state normalization `π* = 0`, `i* = r* = r̄`. No empirical/calibrated values.

### 5.4 Fiscal / asset-supply block
- Exogenous positive government-bond supply `B_t` as the asset-market counterpart; asset-market clearing `A_t − B_t = 0` (or exact equivalent convention justified in the semantics contract).
- Labor tax `τ_l`; government budget identity; lump-sum transfer closure; firm-profit/dividend incidence stated explicitly. No fiscal residual set to zero merely by labeling.

### 5.5 Markets / residuals
Exact residual objects defined in the equation contract for: HJB, KFE, asset market, labor market, goods/resource (incl. Rotemberg cost), fiscal, profits, NKPC, Fisher, Taylor. Every later scientific PASS depends on computed residuals.

## 6. Tier-0 relationship (Issue #10 §6)

- Tier-0 Q200 `[0,200]`, 1265-point result remains the accepted high-accuracy **Tier-0 real HA/Aiyagari reference numerical standard**; the C200/F200/Q200 spacing hierarchy may be used as regression/reference provenance.
- Changing the economic meaning of the asset from **productive capital to liquid financial asset** means Tier-0 domain adequacy is **not automatically inherited** by HANK. A future implementation may use a lower-cost development grid only under an explicit regression contract (see validation/grid contract); final HANK domain/grid adequacy must be re-established in DLH-3E.
- DLH-3A performs no grid run and creates no new numerical result.

## 7. Subgate map (future; non-authoritative here)

| Subgate | Content | Status |
|---|---|---|
| DLH-3B | HANK **steady-state structural kernel**: zero-inflation, zero-shock steady state with household/endogenous-labor/bond-market/nominal-consistency/accounting gates | FUTURE — not authorized here; a 3B PASS alone is NOT full dynamic HANK validation |
| DLH-3C | Time-dependent household/KFE response under externally prescribed small paths (backward HJB + forward KFE), without full NK GE or structural monetary shock | FUTURE — limiting cases specified in the validation contract |
| DLH-3D | NK GE + first small deterministic monetary-policy innovation (full household-distribution-firm-inflation-policy loop) | FUTURE — only an independent 3D review may first qualify for `MINIMAL_GENUINE_SINGLE_REGION_HANK_DYNAMIC_VALIDATED` (validation fixture, not calibration/Results) |
| DLH-3E | HANK numerical robustness freeze: asset-domain adequacy under the new economy, asset-grid refinement, aggregate-time discretization, transition horizon/terminal, reproducibility (never conflate asset-grid and time-discretization convergence) | FUTURE |

## 8. Explicitly NOT included in DLH-3A

- No `src/**`, `configs/**`, or `tests/**` modification; no model run; no pytest for scientific purposes; no transition/shock/IRF; no calibration/regression; no empirical data; no neural/RL; no GPU; no regional/W^L/W^K/W^G; no multi-region code; no Results/policy/welfare/novelty claims; no legacy Matlab / old Python reference / private Zotero access; no governance mutation; no PR/merge/Issue close/successor/self-accept.
