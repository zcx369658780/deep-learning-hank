# DLH-1B — Proposed Clean Kernel I/O and Diagnostic Contract (Design Only)

- Date: 2026-08-19
- Author: DSH (bounded Builder)
- Authority: GitHub Issue #4 — DLH-1B
- Status: DESIGN ONLY — no implementation, no code, no migration.

> Goal: define candidate Tier-0 interfaces that (a) remove legacy global/hard-coded state, (b) separate economics from solver from diagnostics per the NSR-HANK roadmap, and (c) preserve deterministic provenance / no-overwrite. These are candidate contracts, not migration authority.

## 1. Guiding principles

1. Pure functions: every kernel takes explicit inputs, returns a frozen result dataclass; no module-level mutable state, no region index, no frozen-equality calibration.
2. Economics (parameters/grids/equations) and solver (HJB/KFE/root) and diagnostics (residuals/provenance) are separate layers.
3. Deterministic reproducibility: config SHA + source identity + array hashes; explicit RNG seed where randomness exists (none in Tier-0 steady state).
4. No-overwrite outputs; provenance recorded, never overwritten.

## 2. Household solver interface (candidate)

```
Inputs:  asset_grid: FloatArray          # 1-D, increasing
         efficiency_states: FloatArray   # z values (>=1 state)
         state_generator: FloatArray     # (nz,nz) row-stochastic generator
         wage: float, portfolio_return: float, transfer: float
         tau_l: float, rho_hh: float, gamma: float
         numerical: {hjb_tolerance, hjb_max_iterations, hjb_pseudo_time_step, consumption_floor}
Outputs: HouseholdSolution{
           value, consumption, drift, generator (csr),
           converged, iterations, true_residual,
           min_consumption, lower_boundary_min_drift, upper_boundary_max_drift,
           residual_history }
```
Notes: identical to the existing kernel's shape, but parameters are passed explicitly (no config object, no region index, no W). This is a **REUSE_WITH_ADAPTER** target.

## 3. Distribution / KFE interface (candidate)

```
Inputs:  generator: csr_matrix, asset_grid, consumption,
         {stationarity_tolerance, mass_tolerance, negative_mass_threshold}
Outputs: DistributionSolution{
           mass, stationarity_residual, mass_error, minimum_mass,
           negative_mass_count, nan_inf_count, state_marginals,
           mean_assets, mean_consumption, lower_boundary_mass, upper_boundary_mass }
```
Notes: unchanged algorithm (A'g=0, mass=1, negative-mass clip); clean explicit inputs.

## 4. Firm block interface (candidate, Tier-0 = 2-factor)

```
Inputs:  capital, labor, productivity, alpha_k, delta
Outputs: ProductionResult{ output, mpk, net_capital_return, wage }
```
Notes: Tier-0 drops the `alpha_g`/`S` SOE third factor. (The 3-factor form may return only at a later NSR-HANK fiscal/regional stage, by explicit decision.)

## 5. Steady-state outer loop (candidate, single-region Tier-0)

```
Residual: R(K) = K - mean_assets(K)         # capital market clearing
Solve:    root R(K)=0 over (K_min, K_max)  # brentq, deterministic
Outputs:  Tier0SteadyState{ capital, production, fiscal, household, distribution,
           diagnostics{ hjb_residual, kfe_residual, mass_error, goods_residual,
           capital_residual, boundary_feasibility, nan_inf_count } }
```
Notes: no `W`, no symmetry residual, no nominal, no regional/current-account accounts (all 2-region legacy excluded).

## 6. Diagnostics / residual interface (candidate)

- Single `SteadyStateDiagnostics` dataclass with scalar residuals + PASS/FAIL against explicit tolerances.
- Residuals: HJB `max|ρV-(u(c)+GV)|`; KFE `max|G.T g|`; mass `|Σg - 1|`; goods clearing; capital clearing; boundary feasibility (drift signs, consumption>0, mass>=threshold); `nan_inf_count == 0`.
- Reproducibility payload (pure, injectable source identity — **no subprocess `git`**): `{config_sha256, source_identity (passed in), diagnostic_schema, diagnostic_values, array_hashes}`.
- No-overwrite run directory from `io_contracts` (REUSE_AS_REFERENCE_IMPLEMENTATION).

## 7. Config / provenance interface (candidate)

- Config: TOML → frozen dataclass via `from_toml`, but validation uses **bounds/schema checks**, NOT frozen-equality against a hard-coded fixture. Any parameter within declared bounds is admissible (Tier-0 will sweep a small grid of calibrations).
- Provenance: config SHA256 + source identity (git SHA passed in, not shelled out) + array hashes + command/timestamps; no-overwrite.
- Explicit separation: `economics/` (params/grids/equations) vs `solvers/` (HJB/KFE/root) vs `diagnostics/` (residuals/provenance).

## 8. Explicitly NOT designed here

- No neural/learning interface (not Tier-0; DLH-3+).
- No regional/`W^L`/`W^K`/fiscal-transfer interface (later NSR-HANK stages).
- No nominal/monetary interface (DLH-3 genuine-HANK layer).
- No shock/transition interface (DLH-6/7).
- No code written; this is interface documentation only.
