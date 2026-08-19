# DLH-1B — Kernel Equation and Dependency Map (Actual Implemented Behavior)

- Date: 2026-08-19
- Author: DSH (bounded Builder)
- Authority: GitHub Issue #4 — DLH-1B
- Source: `zcx369658780/dissertation-ch5-r5-python-model` @ `3039a145f43d419a08999c476cd0d97fd5f8341f`
- Scope: ACTUAL code behavior, distinct from comments/docs/old Matlab provenance.

## 1. Household state / control / asset dimension (actual)

- **State:** `(a, z)` where `a` is a **single liquid asset** on a uniform grid `[a_min, a_max]` (frozen `a_min=0.0`, `a_max=50.0`, `count=40`), and `z` is **two-state idiosyncratic productivity** `{0.5, 1.5}` with symmetric transition intensities `q_low_to_high = q_high_to_low = 0.25`.
- **Controls:** consumption `c` and saving/drift `da = cash_on_hand - c`. **No portfolio choice** (single asset); **no labor choice** (`labor = 1.0` fixed in the aggregate block; household supplies labor inelastically via `efficiency_states`).
- **Utility:** CRRA `u(c) = c^(1-γ)/(1-γ)` (log at γ=1), frozen `γ = 2.0`; marginal utility `c^-γ`.
- **Income (cash-on-hand):** `(1-τ_l)·wage·z + r_portfolio·a + transfer` (frozen `τ_l = 0.15`).

## 2. HJB discretization / upwind / boundary / generator (actual)

- Continuous-time HJB: `ρ V = u(c) + V_a·ȧ + Σ_z Q[z,z'] (V(z')-V(z))`, solved by **implicit policy iteration with pseudo-time-step** (`dt` frozen `1000.0`).
- **Upwind policy:** first differences give `V_a` forward/backward; consumption `c = u'^{-1}(V_a)`; Hamiltonian `u(c) + V_a·ȧ` maximized over `{constrained (ȧ=0), forward (ȧ>0), backward (ȧ<0)}`; feasibility via drift sign (upwind selection).
- **Boundary:** lower-boundary `V_a` set to marginal utility of constrained consumption; drift clamped `drift[:,0] >= 0` and `drift[:,-1] <= 0` (reflecting boundaries).
- **Generator:** sparse (CSR), per (z,a) cell: idiosyncratic jumps to the other `z` at same `a`; asset drift upwind (`drift>0 → rate=drift/dx` to `a+1`; `drift<0 → -drift/dx` to `a-1`); diagonal absorbs outflows so rows sum to 0 (row-stochastic).
- **Solve:** `((ρ + 1/dt)·I - G) V = u(c) + V/dt` via `scipy.sparse.linalg.spsolve`; residual `max |ρ V - (u(c) + G·V)|`.
- **Transition variant:** `solve_one_period_backward_hjb` shares the same upwind policy/generator with a discrete-time residual vs `value_next`.

## 3. KFE (actual)

- **Stationary:** solve `A' g = 0` (`A' = G.T`) by pinning the last row to `1` and `np.linalg.solve`; normalize mass to 1; clip tiny negatives; report `stationarity_residual = max |G.T g|`, `mass_error`, `negative_mass_count`, `nan_inf_count`, state marginals, mean assets/consumption, boundary mass.
- **Transition:** forward implicit one-step KFE `(I - dt·G.T) g_{t+1} = g_t` with mass normalization and the same diagnostics.

## 4. Firm / production block (actual)

- `production_block` is **three-factor Cobb-Douglas**: `Y = A·K^αk·L^(1-αk-αg)·S^αg` with a **state-owned-services factor `S`** (frozen `αk=0.30`, `αg=0.10`, `δ=0.02`, `S=1.0`).
- Factor prices: `mpk = αk·Y/K`; `net_capital_return = mpk - δ`; `wage = (1-αk-αg)·Y/L`; `public_service_rent = αg·Y`.
- This `αg`/`S` factor is **legacy SOE coupling**, absent from a standard HA/Aiyagari firm block.

## 5. Fiscal / nominal / clearing / fixed point (actual)

- **Fiscal:** `labor_tax_revenue = τ_l·w·L`; `public_service_rent = αg·Y`; `transfer = revenue + rent - outlay`; balanced budget by construction (`residual = 0`).
- **Nominal:** identity-only (`Fisher`: `portfolio_return - (common_return - inflation)`; `price_index - 1`); **no dynamic NK**.
- **Regional accounts (2-region):** `net_exports = output - consumption - δ·K - outlay`; `net_foreign_income = portfolio_income - issuer_capital_income`; `current_account_residual = net_exports + net_foreign_income`.
- **Spatial link `W`:** row-normalized 2×2 capital-exposure matrix `[[0.8,0.2],[0.2,0.8]]`; `portfolio_return = W @ issuer_returns`; `capital_supply = W.T @ household_assets`.
- **Fixed point:** symmetric capital market — `brentq` on `capital_residual[0] = capital - capital_supply[0]`; extra residuals = aggregate goods, aggregate NFI, symmetry, W row-sum. `SteadyStateResult` reports a 16-vector diagnostic schema (2× per-region residuals + aggregates).

## 6. Shock / transition (actual)

- **AR(1) engine (shocks.py):** `z_t = μ + ρ(z_{t-1}-μ) + σ·ε_t`; frozen `μ=0, ρ=0.90, σ=0.01`, quarterly; path types `CONDITIONAL_ONE_INNOVATION / SEEDED_STOCHASTIC_REALIZATION / EXTERNAL_INNOVATION_REALIZATION / EXPECTED_ZERO_FUTURE_INNOVATIONS`; deterministic PCG64 seed; theoretical moments.
- **Transition (transition.py):** bounded 2-region real transition via backward HJB + forward implicit KFE + timing-bridge accounts; `source_loading = (1.0, 0.0)` (region-0 shock only); explicit "no dynamic NK authority" contract.

## 7. Dependency graph (module → module)

- `steady_state` → `household_hjb`, `distribution_kfe`, `grids`, `aggregate_block`, `regional_structure`, `spatial_links`, `parameters`.
- `transition` → `household_hjb` (one-period), `distribution_kfe` (one-step), `aggregate_block`, `grids`, `regional_structure`, `spatial_links`, `steady_state`, `shocks`, `parameters`.
- `diagnostics` → `parameters`, `steady_state`; shells out to `git` (`subprocess`) and reads environment (`platform`, `sys.executable`, `importlib.metadata`, `site`, `os.environ`).
- External deps: `numpy`, `scipy.sparse`/`scipy.optimize`/`scipy.sparse.linalg`; `pandas` (declared, not observed in the read kernels); `tomllib` (stdlib).

## 8. Hidden state / legacy coupling / hard-coded calibration

1. **Frozen calibration embedded in code:** `SteadyStateConfig.validate()` and `TransitionConfig.validate()` reject ANY deviation from the frozen fixture (region_count=2, W, αg, ρ, σ, grid, tolerances). Calibration is **not** configurable in practice — any parameter change raises `ValueError`.
2. **`region_count = 2` hard-coded** across parameters/steady_state/aggregate/spatial_links/shocks/transition (2-region, not single-province).
3. **Legacy SOE factor `αg`/`S`** in production.
4. **Legacy open-economy accounting** (net_foreign_income, current_account, portfolio-vs-issuer return split) — the old `inter_prv_ratio`/`rah` lineage.
5. **`W` is a capital-exposure matrix**, not the NSR-HANK labor-flow `W^L` (different object, different stage).
6. **Provenance side effects:** `diagnostics` invokes `git` via subprocess and writes a full run package (config copy, source manifest, environment manifest, 8+ CSVs/MDs) to disk; `io_contracts` enforces no-overwrite.
7. **Determinism:** good — no module-level mutable random state; `shocks` uses explicit PCG64 seed; steady-state uses `brentq` (deterministic).
8. **No global mutable module state** in the math kernels (functional + frozen dataclasses), but the frozen-equality validation acts as a global hard constraint.

## 9. Distinguishing actual vs claimed

- Actual behavior is read from code; comments/docs/`IMPLEMENTATION_STATUS` labels and old Matlab provenance are treated as claims only. The source itself declares **D2 (machine diagnostics, no Results authority)** throughout, matching the observed scaffolding (no Results/eligibility/submission authority flags are `False`).
