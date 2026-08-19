# DLH-1B-R1 — Existing Python Kernel Provenance and Scope Audit (Terminology/Evidence Corrected)

- Date: 2026-08-19 (R1 correction)
- Author: DSH (bounded Builder)
- Authority: GitHub Issue #4 — `DLH-1B: Read-only audit of existing single-province Python HJB + firm kernel`; authoritative R1 correction comment (2026-08-19 09:11:31).
- Prior candidate: `1d2f3b20fb44680afd93e19ff0aba231a7b47467` — process-clean provenance only; NOT merged, NOT accepted.
- Source repository (READ-ONLY candidate): `zcx369658780/dissertation-ch5-r5-python-model`
- Status: AUDIT ONLY. No migration, no execution, no Results.

> R1 note: this revision corrects (a) generator terminology to **continuous-time infinitesimal generator / intensity matrix**, (b) boundary wording to **state-constraint / no-outward-drift**, and (c) evidence strength so that no unexecuted code is asserted "correct"/"valid". Reuse classifications remain candidate/reference-only and execution-gated.

## 1. Source identity / provenance

- **Fresh source-repo `main` SHA:** `3039a145f43d419a08999c476cd0d97fd5f8341f` (unchanged from Issue #4 publication; re-verified read-only via `git ls-remote` + shallow clone).
- Canonical remote verified: `https://github.com/zcx369658780/dissertation-ch5-r5-python-model.git`.
- Read method: shallow read-only clone to a temp directory (outside `deep-learning-hank`); **zero writes to the source worktree**.
- Package metadata (`pyproject.toml`): name `dissertation-ch5-r5-model`, version `0.0.0`, `requires-python >=3.11,<3.12`, deps `numpy`, `scipy`, `pandas`; dev `pytest`, `ruff`, `mypy`; self-describes as **"Engineering scaffold only; no accepted economic solver or numerical results."**

## 2. Implementation-status signals (as declared in source)

| Module | IMPLEMENTATION_STATUS |
|---|---|
| household_hjb / distribution_kfe / aggregate_block / steady_state / grids / regional_structure / spatial_links | `R5_3_SMALL_GRID_IMPLEMENTED` |
| parameters | `R5_3_STEADY_STATE_CONFIGURATION_IMPLEMENTED` |
| io_contracts | `R5_3_NO_OVERWRITE_RUN_CONTRACT_IMPLEMENTED` |
| diagnostics | `R5_3_STEADY_STATE_DIAGNOSTICS_IMPLEMENTED` |
| shocks | `R5_4_AR1_ENGINE_IMPLEMENTED` |
| transition | `R5_5I_SMALL_TRANSITION_SOLVER_IMPLEMENTED` |

Evidence status is D2 (machine diagnostics) throughout; nothing asserts Results authority.

## 3. Material scope finding (top-level)

> **The candidate is NOT actually single-province.** The implemented steady-state configuration is a **frozen two-region symmetric capital-exposure model** (`region_count = 2`; `W = [[0.8,0.2],[0.2,0.8]]`; `spatial_links.portfolio_returns = W @ issuer_returns`; `issuer_capital_supply = W.T @ household_assets`). The per-region household/KFE/firm kernels are **structurally separable and candidate-reusable in isolation** (execution-gated), but the top-level `steady_state` and `aggregate`/`spatial_links` layers are 2-region legacy, not a clean single-province HA kernel.

## 4. Exact files read (source)

`src/chapter5_model/`: `household_hjb.py`, `distribution_kfe.py`, `aggregate_block.py`, `steady_state.py`, `diagnostics.py`, `grids.py`, `parameters.py`, `io_contracts.py`, `regional_structure.py`, `spatial_links.py`, `shocks.py`, `transition.py`, `__init__.py`; `pyproject.toml`; `configs/steady_state_small_grid.toml`; 9 representative `tests/`. Full per-file manifest in `DLH_1B_SOURCE_FILE_MANIFEST.csv`.

## 5. Generated / transitional / placeholder / implemented?

- **Implemented (functional source, D2 status):** household_hjb, distribution_kfe, grids, regional_structure, aggregate_block, steady_state, spatial_links, parameters, io_contracts, diagnostics, shocks, transition.
- **Placeholder/no-op:** `nominal_steady_state` is identity-only (Fisher identity; no dynamic NK — matches the frozen "no dynamic NK authority" contract).
- **Transitional markers:** many `codex/r37..r79` branches exist on the source repo (out of Issue #4 source scope; not read).

## 6. Explicit non-actions

- No source-repo mutation (0 writes); no code copy/migration (0); no test/model/Python execution (0); no package install (0); no Matlab/Dynare/Octave read/execution (0).
- Test presence recorded here is D0/D1 source evidence; tests were NOT executed.
