# DLH-1B-R2 — Kernel Equation and Dependency Map (Actual Implemented Behavior; R2 Classification-Consistency)

- Date: 2026-08-19 (R2 consistency correction)
- Author: DSH (bounded Builder)
- Authority: GitHub Issue #4 — DLH-1B; R1 correction comment + R2 classification-consistency comment.
- Source: `zcx369658780/dissertation-ch5-r5-python-model` @ `3039a145f43d419a08999c476cd0d97fd5f8341f`
- Scope: ACTUAL code behavior, distinct from comments/docs/old Matlab provenance.

## 1. Household state / control / asset dimension (actual)

- **State:** `(a, z)`; `a` = single liquid asset on uniform grid `[0,50]` (40 pts); `z` = two-state idiosyncratic productivity `{0.5,1.5}` (symmetric intensities 0.25).
- **Controls:** consumption `c` + drift `da`; **inelastic labor** (`labor=1.0`); **no portfolio choice**.
- **Utility:** CRRA `u(c)=c^(1-γ)/(1-γ)`, γ=2; marginal `c^-γ`.
- **Income:** `(1-τ_l)·wage·z + r_portfolio·a + transfer`.

## 2. HJB discretization / upwind / boundary / generator (actual)

- Continuous-time HJB: `ρ V = u(c) + V_a·ȧ + Σ_z Q[z,z'] (V(z')-V(z))`, solved by implicit policy iteration with pseudo-time-step.
- **Upwind policy:** first differences → `V_a` forward/backward; `c = u'^{-1}(V_a)`; Hamiltonian `u(c)+V_a·ȧ` maximized over `{constrained (ȧ=0), forward (ȧ>0), backward (ȧ<0)}`; upwind selection by drift sign.
- **Boundary (state-constraint / no-outward-drift treatment):** the boundary derivative uses **constrained-consumption marginal utility**; drift is clamped so that **lower-boundary drift >= 0** and **upper-boundary drift <= 0**. This is NOT asserted to be a reflected stochastic process; no such mathematical derivation is claimed here.
- **Generator (continuous-time infinitesimal generator / intensity matrix):** sparse (CSR) per (z,a) cell; idiosyncratic jumps to the other `z` at same `a` (off-diagonal rates >= 0); asset drift upwind (drift>0 → rate `drift/dx` to `a+1`; drift<0 → `-drift/dx` to `a-1`); **diagonal = negative total outflow; row sums = 0** (NOT row-stochastic).
- **Solve:** `((ρ + 1/dt)·I - G) V = u(c) + V/dt` via `spsolve`; residual `max |ρ V - (u(c) + G·V)|`.
- **Transition variant:** `solve_one_period_backward_hjb` shares the same upwind policy/generator with a discrete-time residual vs `value_next`.

## 3. KFE (actual)

- **Stationary:** `A'g = 0` (`A' = G.T`) by pinning last row to 1 + `np.linalg.solve`; mass=1; tiny-negative clip; reports `stationarity_residual = max |G.T g|`, `mass_error`, `negative_mass_count`, `nan_inf_count`, state marginals, mean assets/consumption, boundary mass.
- **Transition:** forward implicit one-step KFE `(I - dt·G.T) g_{t+1} = g_t` with mass normalization + same diagnostics.

## 4. Firm / production block (actual)

- **3-factor Cobb-Douglas** `Y = A·K^αk·L^(1-αk-αg)·S^αg` with a **state-owned-services factor `S`** (αk=0.30, αg=0.10, δ=0.02, S=1.0). Factor prices: `mpk=αk·Y/K`; `net_capital_return=mpk-δ`; `wage=(1-αk-αg)·Y/L`; `public_service_rent=αg·Y`. The `αg`/`S` term is legacy SOE coupling (absent from a standard HA/Aiyagari firm).

## 5. Fiscal / nominal / clearing / fixed point (actual)

- **Fiscal:** `labor_tax_revenue=τ_l·w·L`; `public_service_rent=αg·Y`; `transfer=revenue+rent-outlay`; balanced budget by construction.
- **Nominal:** identity-only Fisher residual; no dynamic NK.
- **Regional accounts (2-region):** `net_exports`, `net_foreign_income`, `current_account_residual`.
- **Spatial link `W`:** row-normalized 2×2 **capital-exposure** matrix; `portfolio_return = W @ issuer_returns`; `capital_supply = W.T @ household_assets`.
- **Fixed point:** 2-region symmetric `brentq` on `capital_residual[0]`; extra residuals (aggregate goods/NFI, symmetry, W row-sum); 16-vector diagnostic schema.

## 6. Shock / transition (actual)

- **AR(1):** `z_t = μ + ρ(z_{t-1}-μ) + σ·ε_t`; frozen μ=0, ρ=0.90, σ=0.01, quarterly; path types conditional/stochastic/external/expected; PCG64 deterministic seed.
- **Transition:** bounded 2-region real transition (backward HJB + forward implicit KFE + timing-bridge accounts); `source_loading=(1.0,0.0)`; "no dynamic NK authority".

## 7. Dependency graph (module → module)

- `steady_state` → household_hjb, distribution_kfe, grids, aggregate_block, regional_structure, spatial_links, parameters.
- `transition` → household_hjb (one-period), distribution_kfe (one-step), aggregate_block, grids, regional_structure, spatial_links, steady_state, shocks, parameters.
- `diagnostics` → parameters, steady_state; subprocess `git`, `platform`/`sys.executable`/`importlib.metadata`/`site`/`os.environ`.
- External deps: `numpy`, `scipy`; `pandas` (declared, unobserved in read kernels); `tomllib` (stdlib).

## 8. Hidden state / legacy coupling / hard-coded calibration

1. **Frozen calibration in code** — `SteadyStateConfig.validate()`/`TransitionConfig.validate()` reject any deviation.
2. **`region_count = 2` hard-coded** (2-region, not single-province).
3. **Legacy SOE factor `αg`/`S`**.
4. **Legacy open-economy accounting** (net_foreign_income, current_account, portfolio-vs-issuer return).
5. **`W` = capital-exposure matrix**, not NSR-HANK labor-flow `W^L`.
6. **Provenance side effects** — `diagnostics` subprocess `git` + writes full run package.
7. Determinism good (PCG64, brentq); no mutable module-level random state in the math kernels.

## 9. Distinguishing actual vs claimed

Actual behavior is read from code; comments/docs/status labels and old Matlab provenance are claims only. The source declares D2 (machine diagnostics, no Results authority) throughout. **Numerical convergence and scientific validity remain unverified by this audit** (zero execution performed).
