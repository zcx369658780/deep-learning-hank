# DLH-4B — Import of Accepted MATLAB-Faithful Two-Asset HA Oracle — Integration Report

- Date: 2026-08-30
- Author: DSH (bounded Builder / integrator)
- Authority: GitHub Issue #18 — `DLH-4B: Import accepted MATLAB-faithful two-asset HA oracle as canonical household kernel` (state: OPEN), activation comment id `IC_kwDOT9FOGc8AAAABReMxEg`, scientific clarification id `IC_kwDOT9FOGc8AAAABReN_dA`, executor clarification id `IC_kwDOT9FOGc8AAAABReTgLw`
- Task type: `SCIENTIFIC_INTEGRATION__ACCEPTED_TWO_ASSET_HA_IMPORT`
- Status: **CANDIDATE (scientific success)** — the accepted MATLAB-faithful two-asset HA oracle is established as the canonical household kernel; acceptance requires fresh-GitHub independent review.

## 1. Terminal classification

**`DLH_4B_ACCEPTED_TWO_ASSET_HA_IMPORT_READY_FOR_GPT_REVIEW`**

No stopping condition triggered: source authority recovered and hash-verified (`BLOCKED_DLH_4B_SOURCE_AUTHORITY_MISMATCH` not triggered); byte/behavior preservation verified (`BLOCKED_DLH_4B_ACCEPTED_HA_BEHAVIOR_DRIFT` not triggered); integration tests pass (`BLOCKED_DLH_4B_ENGINEERING_FAILURE` not triggered).

## 2. Phase A — fresh authority recovery

| Item | Result |
|---|---|
| Fresh `origin/main` SHA | `9250304469f6b4480ce7b4eedeb9a2e8b1cba9b6` |
| CURRENT rules / Task Index / Startup Snapshot | read from fresh `origin/main`; Task Index = `ACTIVE_GITHUB_ISSUE_18__DLH_4B_ACCEPTED_TWO_ASSET_HA_IMPORT`; Startup Snapshot synced to Issue #18 |
| Issue #18 body + all comments | read (body + activation `IC_kwDOT9FOGc8AAAABReMxEg` + scientific clarification `IC_kwDOT9FOGc8AAAABReN_dA` + executor clarification `IC_kwDOT9FOGc8AAAABReTgLw`) |
| Source repository | `zcx369658780/dissertation-ch5-two-asset-hank` (public); export file `exports/matlab_faithful_two_asset_ha.py` present on `main` (27,961 bytes) |
| Export-authority commit | `6469e5a87a00366c1b2af38f27efaa3014206936` ("Authorize standalone MATLAB-faithful two-asset HA export and transfer validation") |
| **Source file SHA-256** | fetched raw content → `276D2244B389D6EDE140DAF8B1F9B0BE1F4AA859368941CED1A12BA8A5831AB8` — **exact match to the Issue's required value, verified before mutation** |
| Designated MATLAB authority | `HANK_2ASSETS_HJB.m` SHA-256 `049136B769560040BC678F828F5D3EC5338DDCAA2090D6BED4E40732F56C3EAE` (recorded in the artifact) |

## 3. Phase B — canonical import

- Canonical package path: `src/deep_learning_hank/two_asset/`
- Canonical file: `src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py` — **byte-identical copy** of the accepted export (SHA-256 of the committed copy = `276D2244B389D6EDE140DAF8B1F9B0BE1F4AA859368941CED1A12BA8A5831AB8`; byte count 27,961 = source). No executable statement altered.
- Minimal plumbing only: `src/deep_learning_hank/two_asset/__init__.py` re-exports the module and its public API; no redesign, no boundary normalization, no solver substitution, no contaminated-row KFE replacement.
- Preserved faithful devices (Owner clarification `IC_kwDOT9FOGc8AAAABReN_dA`): bare-`a` transfer FOC pairing; illiquid-return taper `r_a*(1-0.1*(a/a_max)^9)` (labeled `NUMERICAL_REGULARIZATION`); exact spdiags-equivalent HJB iteration operator semantics (signed off-diagonals, nonzero boundary row sums); contaminated-row stationary KFE solve. Labels `ECONOMIC_STRUCTURE` vs `NUMERICAL_REGULARIZATION / MATLAB_FAITHFUL_IMPLEMENTATION` are maintained in the package docstring.

## 4. Phase C — legacy/superseded-code handling

- **Live `main` has no prior two-asset implementation** (no `src/**/two_asset*`, no two-asset configs/tests; the DLH-4A commit on `main` (`f8a8bd7`) is a forensic-audit-gate document only).
- Recorded: **`NO_LIVE_MAIN_TWO_ASSET_IMPLEMENTATION_TO_REPLACE`** — the canonical module is established without removing anything.
- The one-asset HA/Aiyagari validation route (Tier-0 / DLH-3B / DLH-3C) remains untouched as a benchmark; it is not described as the final HANK household foundation.
- The failed Issue #17 branch is **not** merged, copied, or used as scientific authority.

## 5. Phase D — transfer validation (tests and results)

| Test | Result |
|---|---|
| `test_dlh_4b_import_identity.py` — canonical-file SHA-256 integrity; provenance markers; dependency/public-API boundary; faithful-economics markers (bare-`a` FOC, taper, contaminated-row index) | 4 passed |
| `test_dlh_4b_transfer.py` — local-policy and boundary smoke; sparse operator boundary truncation; contaminated-row index; KFE density normalization; household aggregate weighting; end-to-end steady-state smoke; deterministic repeat | 8 passed |
| **New DLH-4B suite total** | **12 passed / 0 failed** (4.2 s) |
| Accepted predecessor regression (Tier-0 + DLH-3B + DLH-3C) + DLH-4B | **109 passed / 0 failed** (180 s) — no regression |

End-to-end evidence (canonical validation fixture, `VALIDATION_FIXTURE_NOT_CALIBRATION`, mirroring the accepted reference grid/parameters):
- HJB converged in 11 iterations, convergence statistic `1.67e-8 ≤ 1e-7`;
- unique stationary distribution (nullity of the post-convergence operator's transpose = 1);
- density normalization `1.0`; contaminated-row KFE solve residual `4.77e-18`;
- household aggregates: `C=1.0583`, `L=0.9925`, **`A=8.9587`** (illiquid), **`B=0.7953`** (liquid) — both assets held, reported separately (`A ≠ B`);
- deterministic repeat: max abs differences `0.0` across value, density, and aggregates.

## 6. Environment / reproducibility

- Python `3.11.9`; numpy `2.4.6`; scipy `1.17.1`; pytest `8.2.1` (pre-existing; zero installs; no GPU).
- Deterministic single-threaded CPU; no random numbers; repeat differences `0.0`.

## 7. Exact changed paths (new only; no accepted path modified)

1. `src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py` (byte-identical canonical import)
2. `src/deep_learning_hank/two_asset/__init__.py` (minimal plumbing)
3. `tests/test_dlh_4b_import_identity.py`
4. `tests/test_dlh_4b_transfer.py`
5. `reports/dlh_4b_accepted_two_asset_ha_import_2026_08_30/DLH_4B_IMPORT_REPORT.md`
6. `reports/dlh_4b_accepted_two_asset_ha_import_2026_08_30/DLH_4B_FORBIDDEN_OPERATION_CHECK.md`

Branch: `dsh/issue-18-dlh-4b-two-asset-ha-import-2026-08-30` (created from fresh `origin/main`); candidate commit SHA reported in the completion response.

## 8. Statement of byte/behavior preservation

The committed canonical file is **byte-identical** to the accepted source export (SHA-256 `276D2244…` verified both before and after the copy). The only added code is the package `__init__.py` (import plumbing) and the tests; no executable semantic change was made to the accepted artifact.

## 9. Limitations

- GE closure and dynamics remain intentionally outside this task (Issue #18 scientific ceiling).
- The canonical validation fixture is `VALIDATION_FIXTURE_NOT_CALIBRATION`; it mirrors the accepted MATLAB reference grid/parameters but is not an empirical calibration.
- The illiquid-return taper and the contaminated-row KFE are preserved as numerical-regularization devices of the MATLAB-faithful oracle (per the Owner clarification); they must not be misdescribed as primitive economic equations.
