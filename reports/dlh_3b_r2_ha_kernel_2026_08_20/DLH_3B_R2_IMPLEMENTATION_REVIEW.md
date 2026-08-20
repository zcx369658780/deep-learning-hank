# DLH-3B-R2 — Canonical One-Asset HANK Validation Kernel: Implementation Review (Issue #15 §4)

- Date: 2026-08-20
- Authority: GitHub Issue #15 — `DLH-3B-R2: Rebuild Python HA kernel as canonical one-asset HANK validation module` (OPEN), activation comment id `IC_kwDOT9FOGc8AAAABPzrXKg`
- Task type: `SCIENTIFIC_IMPLEMENTATION__HA_KERNEL_RECONSTRUCTION`
- Status: implementation-review documentation (Issue #15 §4 requirement, "before coding"); part of the R2 candidate evidence.
- Labels: `VALIDATION_FIXTURE_NOT_CALIBRATION`; `D2_MACHINE_DIAGNOSTIC`-style kernel validation evidence.

> This document states the target contract of the rebuilt kernel explicitly so that no hidden economic assumption is introduced. Every equation below is the accepted DLH-3A R1 equation contract (docs/specifications/DLH_3_*_2026_08_19.md) restricted to the steady state (DLH-3B), re-derived cleanly for the canonical kernel. The kernel solves the **same economic problem** as the accepted DLH-3B kernel; it is a clean, self-contained reimplementation with explicit documentation, not a Matlab translation (Issue #15 §6).

## 1. Target equations (steady-state, zero-inflation, zero-shock)

### 1.1 Household block
- State: `(a, z)`, `a ∈ [0, a_max]` (one liquid, risk-free real bond; `a_min = 0` ⇒ **no borrowing**), `z ∈ {z_l, z_h}` two-state idiosyncratic CTMC with generator `Q` (rows sum 0, off-diagonals ≥ 0).
- Utility (separable): `U(c, n) = u(c) − v(n)`, `u(c) = c^(1−γ)/(1−γ)`, `v(n) = χ n^(1+1/φ)/(1+1/φ)`.
- Cash flow / budget: `ȧ = (1−τ_l) w z n + r a + tr + Π − c`.
- Stationary HJB: `ρ V(a,z) = max_{c,n} { U(c,n) + V_a(a,z)·[cash_flow − c] + (Q V)(a,z) }`.
- Consumption FOC: `u'(c) = V_a`.
- **Endogenous static labor FOC**: `v'(n) = (1−τ_l) w z V_a` ⇒ `n = min( [ (1−τ_l) w z V_a / χ ]^φ , n_max )` with KKT clipping to `[0, n_max]`.
- Boundary: **state-constraint / no-outward-drift** — at `a = a_min`: `ȧ ≥ 0`; at `a = a_max`: `ȧ ≤ 0` (boundary derivative from the constrained-consumption marginal utility; no reflected-process claim).

### 1.2 Stationary distribution (KFE)
- `Gᵀ g = 0`, `g ≥ 0`, `∫ g da dz = 1`, where `G` is the full infinitesimal generator (upwind asset-drift rates + CTMC `Q`; rows sum 0).
- Aggregates: `A_hh = ∫ a g da dz`, `N_hh = ∫ z n g da dz`, `C = ∫ c g da dz`.

### 1.3 Production / price-setting (steady state)
- `Y = Z·N` (labor-only); markup `μ = ε/(ε−1)`; `mc = w/Z`; steady state `mc = 1/μ` ⇒ `w = Z/μ`.
- Profits (zero inflation): `Π = Y − w·N`.

### 1.4 Fiscal
- Constant bond supply `B`; tax revenue `T = τ_l w N`; government budget `r B + tr = T` ⇒ `tr = τ_l w N − r B` (no seigniorage, no issuance, `Ḃ = 0`).

### 1.5 Markets / residuals (computed, never set to zero by labeling)
- Asset: `R_asset = A_hh − B`.
- Labor: `R_labor = N_hh − N` (with technological demand `N^d = Y/Z`).
- Goods: `R_goods = Y − C − AC` (`AC = (φ_p/2)π²Y = 0` at `π = 0`).
- Fiscal: `R_fiscal = τ_l w N − r B − tr`.
- Profits: `R_profits = Π − (Y − w N − AC)`.
- Wealth flow: `R_wealth = 0 − [(1−τ_l) w N + r A_hh + tr + Π − C]` (steady state `Ȧ_hh = 0`).
- HJB: `R_hjb = max|ρ V − (U + V_a ȧ + Q V)|`; KFE/mass: `|∫g − 1|`, `min g`, negative count, NaN count.

## 2. State variables

| Object | Definition |
|---|---|
| `a` | one liquid risk-free real bond holding (household state); grid `[0, a_max]` uniform, 401 points |
| `z` | idiosyncratic productivity, two-state CTMC `{z_l, z_h}` |
| `g(a,z)` | joint stationary distribution |
| Aggregate inputs | `w` (real wage), `r` (real return), `tr` (lump-sum transfer), `Π` (profits) |
| Aggregate unknowns | `r`, `N` (equilibrium fixed point) |

## 3. Asset accounting

- Household side: `A_hh = ∫ a g da dz`.
- Supply side: constant government bond supply `B` (real).
- Clearing: **one asset market** `A_hh = B`; residual `R_asset = A_hh − B`.
- No second asset, no adjustment cost `chi(d,a)`, no borrowing, no productive capital in the kernel (Issue #15 §3/§6).

## 4. HJB formulation (numerical)

- Upwind **three-candidate policy** per node: zero-drift (`c0, n0` from the static problem `c0 = b + q·n0`, FOC `χ n0^(1/φ) = q c0^(−γ)`), forward (saving) and backward (dissaving) from forward/backward value differences; Hamiltonian selection.
- Boundary values from constrained-consumption marginal utility; drift clipped `ȧ ≥ 0` at `a_min`, `ȧ ≤ 0` at `a_max`.
- Pseudo-time value iteration: `[(ρ + 1/Δ) I − G] V = u − v + V_old/Δ`, `Δ = 1000`; convergence on the **true HJB residual** `max|ρV − (U + G V)| ≤ hjb_tolerance`.

## 5. KFE formulation (numerical)

- Same infinitesimal generator `G` as the HJB (single shared operator).
- Stationary solve: `Gᵀ g = 0` with one pinned row (last row → 1, rhs → 1), then renormalize `Σg = 1`; tiny-negative cleanup rule reported.
- Mass conservation emerges from rows-sum-zero; diagnostics: `mass_error`, `minimum_mass`, `negative_mass_count`, `nan_inf_count`.

## 6. Equilibrium conditions

- Fixed point `(r, N)`:
  1. inner labor root: `R_labor(N) = N_hh(r, N) − N = 0`;
  2. outer asset root: `R_asset(r) = A_hh(r, N*(r)) − B = 0`.
- Deterministic nested bracket roots (primary bracket first, else one bounded deterministic scan); no parameter tuning to manufacture a bracket.

## 7. Limiting cases (documented; deterministic kernel modes)

| Case | Expected behavior |
|---|---|
| Zero-innovation steady state (kernel's only mode) | `π = 0`, `i = r = r̄`, `mc = 1/μ`, `w = Z/μ`, `A_hh = B` |
| `χ → 0` (no labor disutility) | labor supply degenerates (labor FOC interiority lost); documented, not a kernel run |
| Borrowing constraint binding | mass accumulates at `a = a_min = 0`; boundary mass reported |
| `φ → ∞` (inelastic labor) | labor supply becomes insensitive to wages; documented limit |
| Deterministic reproducibility | two identical solves ⇒ max repeat difference `0.0` |

## 8. Explicit non-assumptions

- All numerical values are `VALIDATION_FIXTURE_NOT_CALIBRATION` (accepted DLH-3B fixture, config SHA-256 `82AB4A02F9D08FBBAED1349BC027FACE5361B1AB24C710C4CEA6958481CD5FC1`).
- Asset domain `[0,100]/401` is a development domain, **not** proven HANK domain adequacy (DLH-3E business).
- Single region; no NK dynamics; no monetary innovation; no neural/RL; no regional/`W^L/W^K/W^G`; no data calibration.
- The kernel is not a claim of Matlab parity (Issue #15 §1: "The target is not Matlab parity").
