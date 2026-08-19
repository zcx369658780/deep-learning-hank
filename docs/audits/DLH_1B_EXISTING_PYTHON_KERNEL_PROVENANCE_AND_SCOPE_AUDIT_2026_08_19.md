# DLH-1B — Existing Python Kernel Provenance and Scope Audit

- Date: 2026-08-19
- Author: DSH (bounded Builder)
- Authority: GitHub Issue #4 — `DLH-1B: Read-only audit of existing single-province Python HJB + firm kernel`
- Source repository (READ-ONLY candidate): `zcx369658780/dissertation-ch5-r5-python-model`
- Status: AUDIT ONLY. No migration, no execution, no Results.

## 1. Source identity / provenance

- **Fresh source-repo `main` SHA:** `3039a145f43d419a08999c476cd0d97fd5f8341f`
  - (Unchanged from Issue #4 publication-time SHA; recorded independently via `git ls-remote` and re-confirmed after shallow clone.)
- Canonical remote verified: `https://github.com/zcx369658780/dissertation-ch5-r5-python-model.git`.
- Read method: shallow read-only clone to a temp directory (outside `deep-learning-hank`); **zero writes to the source worktree** (no branch, no commit, no formatting, no execution).
- Package metadata (`pyproject.toml`): name `dissertation-ch5-r5-model`, version `0.0.0`, `requires-python >=3.11,<3.12`, runtime deps `numpy`, `scipy`, `pandas`; dev deps `pytest`, `ruff`, `mypy`; package self-describes as **"Engineering scaffold only; no accepted economic solver or numerical results."**
- `pyproject.toml` blob: `2aca077641b384a2eac67361e0ef61ac6b248e45`.

## 2. Implementation-status signals (as declared in source)

| Module | IMPLEMENTATION_STATUS | EVIDENCE_STATUS (where present) |
|---|---|---|
| household_hjb / distribution_kfe / aggregate_block / steady_state / grids / regional_structure / spatial_links | `R5_3_SMALL_GRID_IMPLEMENTED` | D2 (machine diagnostics, no Results authority) |
| parameters | `R5_3_STEADY_STATE_CONFIGURATION_IMPLEMENTED` | `D2_SMALL_GRID_STEADY_STATE_MACHINE_DIAGNOSTICS_NO_RESULTS_AUTHORITY` |
| io_contracts | `R5_3_NO_OVERWRITE_RUN_CONTRACT_IMPLEMENTED` | — |
| diagnostics | `R5_3_STEADY_STATE_DIAGNOSTICS_IMPLEMENTED` | — |
| shocks | `R5_4_AR1_ENGINE_IMPLEMENTED` | `D2_AR1_ENGINE_...NO_TRANSITION_OR_MODEL_RESPONSE_AUTHORITY` |
| transition | `R5_5I_SMALL_TRANSITION_SOLVER_IMPLEMENTED` | `D2_SMALL_TRANSITION_SOLVER_...NO_FORMAL_RESPONSE_AUTHORITY` |

Interpretation: the source is an **R5-3/R5-4/R5-5I engineering scaffold with D2 machine-diagnostics evidence**, explicitly **not** an accepted solver or source of numerical Results. Nothing in the source asserts Results authority.

## 3. Material scope finding (top-level)

> **The candidate is NOT actually single-province.** The implemented steady-state configuration is a **frozen two-region symmetric capital-exposure model** (`region_count = 2`; `W = [[0.8,0.2],[0.2,0.8]]`; `spatial_links.portfolio_returns = W @ issuer_returns`; `issuer_capital_supply = W.T @ household_assets`). The per-region household/KFE/firm kernels are symmetric and reusable in isolation, but the top-level `steady_state` and `aggregate`/`spatial_links` layers are 2-region legacy, not a clean single-province HA kernel.

## 4. Exact files read (source)

`src/chapter5_model/`: `household_hjb.py`, `distribution_kfe.py`, `aggregate_block.py`, `steady_state.py`, `diagnostics.py`, `grids.py`, `parameters.py`, `io_contracts.py`, `regional_structure.py`, `spatial_links.py`, `shocks.py`, `transition.py`, `__init__.py`; `pyproject.toml`; `configs/` (4 TOML files, read `steady_state_small_grid.toml` fully); representative `tests/` (household, distribution, steady-state small-grid, reproducibility, no-model-implementation, imports, contracts, aggregate/fiscal, grids). Full per-file manifest (path/blob/size) in `DLH_1B_SOURCE_FILE_MANIFEST.csv`.

## 5. Generated / transitional / placeholder / implemented?

- **Implemented (functional code, D2):** household_hjb, distribution_kfe, grids, regional_structure (production), aggregate_block, steady_state, spatial_links, parameters, io_contracts, diagnostics, shocks, transition.
- **Placeholder/no-op:** `nominal_steady_state` is a pure identity residual (Fisher identity; no actual NK dynamics — matches the frozen "no dynamic NK authority" contract). `shocks.w_role` enforces that `W` is "not an AR(1) parameter" (legacy separation guard).
- **Transitional markers:** multiple `codex/r37..r79` branches exist on the source repo (HJB/KFE modernization work); `main` is the frozen R5-3/4/5I line. None of the codex branches were read (out of Issue #4 source scope).

## 6. Explicit non-actions

- No source-repo mutation (0 writes).
- No code copied/migrated into `deep-learning-hank` (0).
- No test/model/Python execution; no package install; no environment mutation; no Matlab/Dynare/Octave read or execution.
- Source presence/status recorded here is D0/D1-style evidence; the tests were NOT executed.
