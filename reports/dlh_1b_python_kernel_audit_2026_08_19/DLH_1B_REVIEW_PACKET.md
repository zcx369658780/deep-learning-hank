# DLH-1B Review Packet — Existing Python Kernel Read-only Audit

- Date: 2026-08-19
- Author: DSH (bounded Builder)
- Authority: GitHub Issue #4 — `DLH-1B: Read-only audit of existing single-province Python HJB + firm kernel`
- Target repository: `zcx369658780/deep-learning-hank`
- Source repository (READ-ONLY): `zcx369658780/dissertation-ch5-r5-python-model`
- Status: CANDIDATE audit. Acceptance requires fresh-GitHub independent review (ChatGPT).

## 1. Terminal classification

`DLH_1B_PYTHON_KERNEL_READONLY_AUDIT_READY_FOR_GPT_REVIEW`

## 2. Baselines and branch

- Fresh **target** `origin/main` SHA: `1ddd44c8b4ed4ec36c853532a8546dff58ea6ee3`
- Fresh **source-repo** `main` SHA: `3039a145f43d419a08999c476cd0d97fd5f8341f` (verified read-only via `git ls-remote` + shallow clone; canonical remote confirmed)
- Dedicated branch: `dsh/issue-4-dlh-1b-python-kernel-audit-2026-08-19`
- Candidate commit: single evidence commit at branch HEAD (2026-08-19, DSH); hash reported in completion response. Expected delta: exactly the seven paths below, 0 behind / 1 ahead of target baseline.

## 3. Exact changed paths (seven allowlisted outputs)

1. `docs/audits/DLH_1B_EXISTING_PYTHON_KERNEL_PROVENANCE_AND_SCOPE_AUDIT_2026_08_19.md`
2. `docs/audits/DLH_1B_KERNEL_EQUATION_AND_DEPENDENCY_MAP_2026_08_19.md`
3. `docs/audits/DLH_1B_REUSE_REDESIGN_DROP_MATRIX_2026_08_19.csv`
4. `docs/audits/DLH_1B_KERNEL_IO_AND_DIAGNOSTIC_CONTRACT_2026_08_19.md`
5. `reports/dlh_1b_python_kernel_audit_2026_08_19/DLH_1B_SOURCE_FILE_MANIFEST.csv`
6. `reports/dlh_1b_python_kernel_audit_2026_08_19/DLH_1B_REVIEW_PACKET.md`
7. `reports/dlh_1b_python_kernel_audit_2026_08_19/DLH_1B_FORBIDDEN_OPERATION_CHECK.md`

No roadmap, accepted spec, DLH-1A evidence, rule, Task Index, Startup Snapshot, README, or code modified.

## 4. Source files / tests / configs read

- Full read: all 13 `src/chapter5_model/` files (`transition.py` = structure+header), `pyproject.toml`, `configs/steady_state_small_grid.toml`, and 9 representative test files (household, distribution, steady-state small-grid, reproducibility, no-model-implementation, imports, contracts, aggregate/fiscal, grids). Remaining configs/tests listed only. Full manifest in `DLH_1B_SOURCE_FILE_MANIFEST.csv`.

## 5. Actual household asset / state / control structure found

- **One liquid asset** `a` on uniform grid `[0,50]` (40 pts); **two idiosyncratic productivity states** `{0.5,1.5}` (symmetric intensities 0.25). Controls: consumption `c` + drift `da`; **inelastic labor** (labor=1.0 fixed), **no portfolio choice**. CRRA `γ=2`. Income = `(1-τ_l)·wage·z + r_portfolio·a + transfer`.

## 6. HJB / KFE / firm / steady-state implementation summary

- **HJB:** continuous-time, implicit policy iteration w/ pseudo-time-step; upwind FD; Hamiltonian argmax {constrained, forward, backward}; reflecting boundaries (drift clamped; lower-boundary marginal utility); sparse row-stochastic generator (2-state jumps + upwind asset drift); `true_residual = max|ρV-(u(c)+GV)|`.
- **KFE:** stationary `A'g=0` (row-pin + solve, mass=1, tiny-negative clip, stationarity/mass/non-negativity diagnostics); plus forward implicit one-step KFE for transition.
- **Firm:** **3-factor Cobb-Douglas** with a **state-owned-services factor `S` (`αg=0.10`)** — legacy SOE, not standard HA firm.
- **Steady-state:** 2-region **symmetric** capital clearing via `brentq` on `capital_residual[0]`, with `W` capital-exposure (`portfolio_return=W@r`, `capital_supply=W.T@assets`), plus aggregate goods/NFI/symmetry/W row-sum residuals and identity-only Fisher nominal.

## 7. Hidden / global-state and legacy-coupling findings (most material)

1. **`region_count = 2` hard-coded** — the "single-province" candidate is actually a frozen 2-region symmetric model.
2. **Frozen calibration embedded in code** — `SteadyStateConfig.validate()`/`TransitionConfig.validate()` reject any deviation (calibration not parameterizable).
3. **Legacy SOE third factor `αg`/`S`** in production.
4. **Legacy open-economy accounting** (net_foreign_income, current_account, portfolio-vs-issuer return).
5. **`W` = capital-exposure matrix**, not the NSR-HANK labor-flow `W^L` (different object/stage).
6. **Provenance side effects** — `diagnostics` shells out to `git` (subprocess) and writes a full run package; `io_contracts` no-overwrite.
7. Determinism good (PCG64 seed, brentq); no mutable module-level random state in the math kernels.

## 8. Reuse classification counts

- `REUSE_AS_REFERENCE_IMPLEMENTATION`: 2 (grids, io_contracts)
- `REUSE_WITH_ADAPTER`: 4 (household_hjb, distribution_kfe, regional_structure/production, aggregate_block/fiscal_closure)
- `REDESIGN_FOR_NSR_HANK`: 3 (steady_state, parameters, diagnostics)
- `DROP_FROM_TIER0`: 3 (spatial_links/W, shocks, aggregate_block/RegionalAccounts)
- `UNRESOLVED_NEEDS_EXECUTION_OR_SCIENTIFIC_DECISION`: 2 (aggregate_block/nominal, transition)

Most important REDESIGN: `steady_state` (2-region→single-region clearing), `parameters` (frozen→bounds-validated config). Most important DROP for Tier-0: `spatial_links` capital-exposure `W` and `RegionalAccounts` open-economy accounting.

## 9. Proposed Tier-0 migration allowlist candidate (NOT migration authority)

- **Candidate inputs for Tier-0 HA/Aiyagari benchmark:** `grids.py`, `io_contracts.py` (reference), `household_hjb.py` + `distribution_kfe.py` (with clean adapters), 2-factor `production_block`, `fiscal_closure` (lump-sum only).
- **Must be excluded/redesigned for Tier-0:** `region_count=2`, `W` capital exposure, `αg`/`S` SOE factor, nominal/Fisher block, regional/current-account accounting, AR(1)/transition, frozen calibration.
- A single-region Tier-0 target = one asset, 2-state productivity, CRRA, inelastic labor, 2-factor firm, lump-sum balanced fiscal, capital-market clearing, deterministic diagnostics — matching the accepted DLH-2 spec.

## 10. Proposed clean I/O contracts (design only)

Household solver (explicit params, no config/region/W) → `HouseholdSolution`; KFE (generator/consumption/tolerances) → `DistributionSolution`; firm (2-factor) → `ProductionResult`; steady-state (single-region `R(K)=K-mean_assets(K)`) → `Tier0SteadyState + diagnostics`; diagnostics = residual dataclass + pure reproducibility payload (no subprocess git); config = TOML→dataclass with bounds/schema validation + sha256 + no-overwrite. Full detail in `DLH_1B_KERNEL_IO_AND_DIAGNOSTIC_CONTRACT_2026_08_19.md`.

## 11. Existing tests mapped to claimed properties (NOT executed)

- `test_household_hjb` → CRRA utility/marginal/inverse identity; fixed-price HJB convergence, residual ≤ tol, consumption>0, boundary drift signs, generator row-sums=0.
- `test_distribution_kfe` → mass=1, non-negativity, state marginals [0.5,0.5], moment bounds.
- `test_steady_state_small_grid` → 2-region convergence + full diagnostic PASS + 12-file run package.
- `test_steady_state_reproducibility` → two solves produce identical diagnostic vector + arrays (determinism).
- `test_aggregate_and_fiscal_block` → factor prices, balanced fiscal, W orientation/allocation, zero nominal/current-account residual.
- `test_grids` → grid bounds/dimension; generator row-sums; stationary probs.
- `test_no_model_implementation` / `test_imports` / `test_contracts` → status labels / package version / config & no-overwrite rejection.
- **None executed in DLH-1B.** Test presence is D0/D1 source evidence only; it does not prove current passing or scientific validity.

## 12. Unresolved items (require later execution or scientific decision)

1. Whether the kernels actually converge at the frozen values — requires (later-authorized) execution, not done here.
2. Genuine-HANK nominal layer (DLH-3) — placeholder `nominal_steady_state` today.
3. Transition solver and AR(1) freeze semantics — defer to DLH-6/7 + DLH-3 freeze.
4. `W`-type interregional links — NSR-HANK `W^L` is a different object, designed later.

## 13. Forbidden-operation counters (all zero)

- source-repo writes = 0 · code copy/migration = 0 · Python/model/test executions = 0 · package installs = 0 · legacy Matlab reads = 0 · neural training = 0 · Results claims = 0 · governance changes = 0.

## 14. Recommended next gate (suggestion only — no successor creation)

`DLH-2` — single-region Tier-0 HA/Aiyagari computational benchmark (transparent HJB + KFE + 2-factor firm + deterministic diagnostics), built on the REUSE_WITH_ADAPTER kernels and clean interfaces above, subject to independent review and a separate GitHub Issue.
