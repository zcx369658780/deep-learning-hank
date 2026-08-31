# DLH-4D-R3 — Forbidden-Operation / Scope Check (Issue #23)

**Issue:** #23 — DLH-4D-R3
**Branch:** `dsh/issue-23-dlh-4d-r3-matlab-transfer-foc-repair-2026-08-30`
**Date:** 2026-08-30

This check records that the Issue #23 execution did **not** widen scope. When a
commit is made it will contain only the authorized narrow repair, its focused
tests, and its reports (explicit staging only). At report time the changes sit in
the working tree on the dedicated branch, uncommitted (commit deferred — see
`DLH_4D_R3_GE_REEXECUTION_REPORT.md` for the Phase E INCONCLUSIVE disposition).

---

## 1. Authorized mutation inventory

| Path | Action | Justification |
|---|---|---|
| `src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py` | Modified (narrow) | Sole Owner-authorized repair: transfer-FOC handling of non-positive RAW liquid derivatives (remove two Python-only strict-`v_b>0` guards; IEEE zero-denominator semantics; `dh_B`/`dh_F` logical-mask multiply mechanical edit, separately documented) |
| `tests/test_dlh_4b_import_identity.py` | Modified (narrow) | `REQUIRED_SHA256` updated to the Issue #23 post-repair identity; test's sole purpose was enforcing the now-superseded pre-repair identity (documented in-file) |
| `tests/test_dlh_4d_ge_equations.py` | Modified (narrow) | `test_immutable_oracle_identity` reframed as `test_immutable_oracle_identity_detects_issue23_repair` (gate fail-closes with the exact authorized mismatch + on-disk post-repair SHA) |
| `tests/test_dlh_4d_r3_transfer_foc_parity.py` | New | Focused Issue #23 parity/regression tests (9 tests) |
| `reports/dlh_4d_r3_matlab_transfer_foc_repair_2026_08_30/` | New | Issue #23 authorized report outputs |

## 2. Forbidden operations — NOT performed

| Item | Status |
|---|---|
| Modify frozen Issue #20 validation config `configs/dlh_4d_two_asset_single_region_ge_validation.toml` | ❌ NOT modified (retains pre-repair SHA `276D2244…`; gate now fail-closes against the authorized change — expected, documented) |
| Modify `src/deep_learning_hank/ge/**` (GE economics, solver, domains, `GeConfig`) | ❌ NOT modified |
| Modify fixture values / economic parameters / household equations other than the authorized transfer-FOC semantics | ❌ NOT modified (`adjustment_cost(max(a,a_bar))`, bare-`a` FOC, taper, consumption/labor floor, boundary/upwind/source-operator, contaminated-row KFE, `lab_solve2`/baseline labor all preserved) |
| Household / KFE redesign, KKT-style correction, or invented epsilon floor | ❌ NOT performed (exact-zero denominator → IEEE `±Inf`/`NaN`, absorbed by MATLAB-faithful Idh masks as zero-transfer evidence) |
| Modify `src/deep_learning_hank/two_asset/__init__.py` | ❌ NOT modified (no export change was necessary; its docstring still cites the pre-repair export SHA — known stale reference, documented in the repair report) |
| Push to `main` / self-accept / self-merge / self-PR / self-close Issue / create successor Issue | ❌ NOT performed (push only the dedicated branch; Issue #23 remains open for GPT independent review) |
| `git add .` / unscoped staging | ❌ NOT performed (explicit file staging only) |

## 3. Changed-file scope at report time (verified via `git status --short`)

- `M src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`
- `M tests/test_dlh_4b_import_identity.py`
- `M tests/test_dlh_4d_ge_equations.py`
- `?? tests/test_dlh_4d_r3_transfer_foc_parity.py`
- `?? reports/dlh_4d_r3_matlab_transfer_foc_repair_2026_08_30/`

No other tracked file is modified and no other untracked file is introduced by
this Issue.

---

## 4. Read-only evidence gates

| Gate | Result |
|---|---|
| Pre-repair oracle identity (blob `57e32076…`, SHA `276D2244…`) verified at startup | ✅ |
| Post-repair oracle identity (blob `76ae5b1…`, SHA `1795718C…`) verified | ✅ |
| All 4 MATLAB source SHA-256 match Issue #23 authority | ✅ |
| Frozen 729-point grid (`DLH_4D_R1_FULL_DOMAIN_GRID.csv`) used read-only for Phase D | ✅ |
| Frozen Issue #20 `solve_ge` executed unchanged (post-repair identity asserted per Issue #23 authorization) | ✅ (executed; **INCONCLUSIVE** — stopped by Owner after 8.77 h before E1/E2; not claimed as PASS or E2) |
| No fixture/domain/GE-economics tuning for PASS-seeking | ✅ |

Terminal guard if this had failed:
`BLOCKED_DLH_4D_R3_FORBIDDEN_OPERATION_CHECK` — **not triggered.**
