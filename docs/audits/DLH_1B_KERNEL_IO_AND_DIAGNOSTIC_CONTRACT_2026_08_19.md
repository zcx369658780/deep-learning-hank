# DLH-1B-R1 — Proposed Clean Kernel I/O and Diagnostic Contract (Design Only, Corrected)

- Date: 2026-08-19 (R1 correction)
- Author: DSH (bounded Builder)
- Authority: GitHub Issue #4 — DLH-1B; authoritative R1 correction comment (2026-08-19 09:11:31).
- Status: DESIGN ONLY — no implementation, no code, no migration.

> Goal: define candidate Tier-0 interfaces that remove legacy global/hard-coded state, separate economics/solver/diagnostics, and preserve deterministic provenance/no-overwrite. **Reuse classifications are candidate/reference-only and execution-gated; numerical convergence and scientific validity remain unverified by this audit.**

## 1. Guiding principles

1. Pure functions: explicit inputs → frozen result dataclass; no module-level mutable state, no region index, no frozen-equality calibration.
2. Economics / solver / diagnostics as separate layers.
3. Deterministic reproducibility (config SHA + source identity + array hashes).
4. No-overwrite outputs.

## 2. Household solver interface (candidate)

```
Inputs:  asset_grid: FloatArray          # 1-D, increasing
         efficiency_states: FloatArray   # z values (>=1 state)
         state_generator: FloatArray     # (nz,nz) CTMC generator / intensity matrix
                                         #   off-diagonals >= 0; diagonal = -outflow; rows sum = 0
         wage: float, portfolio_return: float, transfer: float
         tau_l: float, rho_hh: float, gamma: float
         numerical: {hjb_tolerance, hjb_max_iterations, hjb_pseudo_time_step, consumption_floor}
Outputs: HouseholdSolution{
           value, consumption, drift, generator (csr intensity matrix),
           converged, iterations, true_residual,
           min_consumption, lower_boundary_min_drift, upper_boundary_max_drift,
           residual_history }
```
Notes: source-level shape matches the existing kernel; parameters passed explicitly (no config object, no region index, no W). Boundary contract = **state-constraint / no-outward-drift** (boundary derivative from constrained-consumption marginal utility; lower drift >= 0; upper drift <= 0). This is a **candidate REUSE_WITH_ADAPTER** target; validity unverified.

## 3. Distribution / KFE interface (candidate)

```
Inputs:  generator: csr_matrix (CTMC intensity matrix), asset_grid, consumption,
         {stationarity_tolerance, mass_tolerance, negative_mass_threshold}
Outputs: DistributionSolution{
           mass, stationarity_residual, mass_error, minimum_mass,
           negative_mass_count, nan_inf_count, state_marginals,
           mean_assets, mean_consumption, lower_boundary_mass, upper_boundary_mass }
```
Notes: source-level structure matches the desired stationary-KFE form (`A'g=0`, mass=1, negative-mass clip); numerical convergence unverified; clean explicit inputs.

## 4. Firm block interface (candidate, Tier-0 = 2-factor)

```
Inputs:  capital, labor, productivity, alpha_k, delta
Outputs: ProductionResult{ output, mpk, net_capital_return, wage }
```
Notes: Tier-0 drops the `alpha_g`/`S` SOE third factor (scientific decision; the 3-factor form may return only at a later NSR-HANK fiscal/regional stage).

## 5. Steady-state outer loop (candidate, single-region Tier-0)

```
Residual: R(K) = K - mean_assets(K)         # capital market clearing
Solve:    root R(K)=0 over (K_min, K_max)  # brentq, deterministic
Outputs:  Tier0SteadyState{ capital, production, fiscal, household, distribution,
           diagnostics{ hjb_residual, kfe_residual, mass_error, goods_residual,
           capital_residual, boundary_feasibility, nan_inf_count } }
```
Notes: no `W`, no symmetry, no nominal, no regional/current-account accounts (2-region legacy excluded). Candidate reference pattern only.

## 6. Diagnostics / residual interface (candidate)

- Single `SteadyStateDiagnostics` dataclass with scalar residuals + PASS/FAIL vs explicit tolerances.
- Residuals: HJB `max|ρV-(u(c)+GV)|`; KFE `max|G.T g|`; mass `|Σg - 1|`; goods clearing; capital clearing; boundary feasibility (drift signs, consumption>0, mass>=threshold); `nan_inf_count == 0`.
- Reproducibility payload (pure, injectable source identity — **no subprocess `git`**): `{config_sha256, source_identity (passed in), diagnostic_schema, diagnostic_values, array_hashes}`.
- No-overwrite run directory from `io_contracts` (candidate REUSE_AS_REFERENCE_IMPLEMENTATION).

## 7. Config / provenance interface (candidate)

- Config: TOML → frozen dataclass via `from_toml`, but validation uses **bounds/schema checks** (NOT frozen-equality against a hard-coded fixture).
- Provenance: config SHA256 + source identity (git SHA passed in) + array hashes + command/timestamps; no-overwrite.
- Separation: `economics/` vs `solvers/` vs `diagnostics/`.

## 8. Explicitly NOT designed here

- No neural/learning interface (DLH-3+); no regional/`W^L`/`W^K`/fiscal-transfer interface (later NSR-HANK stages); no nominal/monetary interface (DLH-3); no shock/transition interface (DLH-6/7); no code written.
