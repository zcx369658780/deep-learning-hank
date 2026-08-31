# DLH-4D-R3 — MATLAB Transfer-FOC Repair Report (Phase B + Phase C)

**Issue:** #23 — DLH-4D-R3
**Branch:** `dsh/issue-23-dlh-4d-r3-matlab-transfer-foc-repair-2026-08-30`
**Date:** 2026-08-30
**Companion reports:** `DLH_4D_R3_SOURCE_PARITY_AUDIT.md`,
`DLH_4D_R3_NONFINITE_RECLASSIFICATION.csv`, `DLH_4D_R3_GE_REEXECUTION_REPORT.md`,
`DLH_4D_R3_FORBIDDEN_OPERATION_CHECK.md`

---

## 1. Oracle identity (pre-repair → post-repair)

| | Pre-repair | Post-repair |
|---|---|---|
| Git blob | `57e32076f0e11c9a047e1f90f8c2446d4148e457` | `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e` |
| SHA-256 | `276D2244B389D6EDE140DAF8B1F9B0BE1F4AA859368941CED1A12BA8A5831AB8` | `1795718C469FC3B427CAB8E3D5957C133BEAD6EACC9EF0A25A3EDB7211D1A024` |

The frozen Issue #20 config retains the pre-repair identity (NOT modified per
Issue #23). The GE identity gate therefore now fail-closes with exactly the
authorized mismatch — expected and verified.

## 2. Narrow repair applied

The repair is confined to `src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`
and implements only the transfer-FOC handling of non-positive RAW liquid
derivatives. Three source edits:

### 2.1 `transfer_candidate` — accept finite negative `v_b`; IEEE zero-denominator
- **Removed** the Python-only guard `if not np.isfinite([v_a, v_b, a]).all() or v_b <= 0: raise ValueError("transfer FOC requires finite derivatives and V_b > 0")`.
- The FOC now evaluates the **literal** MATLAB `HANK3_FOC` formula
  `d = (min(pa./pb - 1 + chi0, 0) + max(pa./pb - 1 - chi0, 0)).*a/chi1` on the
  **raw** `v_b` (no `1e-6` floor — the floor belongs to consumption/labor).
- The `pa./pb` division is performed with `np.float64` so an **exact-zero
  denominator** yields IEEE `±Inf`/`NaN` exactly as MATLAB `pa./pb` (plain Python
  float division would raise `ZeroDivisionError`). No invented epsilon floor.
- Finite negative `v_b` produce finite literal results (MATLAB-faithful).

### 2.2 `select_matlab_faithful_local_policy` — remove the strict-positive guard
- **Removed** the Python-only guard
  `if min(v_b_forward, v_b_backward) <= 0.0: raise ValueError("designated transfer FOCs require positive liquid derivatives")`.
- The selector now accepts finite negative `v_b`; consumption/labor inputs are
  floored `max(v_b, 1e-6)` exactly as MATLAB `HANK_2ASSETS_HJB.m` L124–128, and
  the four transfer candidates use the **raw** `v_b` (MATLAB L137–140).

### 2.3 `dh_B`/`dh_F` assembly — IEEE logical-mask multiply (mechanical, documented)
- Replaced the ternary assemblies (`x if x > t else 0.0`, which clamp `NaN → 0`)
  with the IEEE mask-multiply `x*(x > t)` / `x*(x < -t)` that MATLAB uses
  (`(x>t).*x`). This reproduces MATLAB's `0.*NaN = NaN`, `0.*Inf = NaN` for the
  exact-zero/non-finite denominator path, so an Inf/NaN candidate is absorbed by
  the downstream Idh masks as **zero-transfer (Idh_0) evidence** rather than
  silently clamped or replaced by an epsilon.
- For all-finite candidates the mask-multiply and the former ternary are
  bit-identical (verified by focused parity tests), so the dominant finite case
  is behavior-identical.

### 2.4 Explicitly preserved (frozen contract)
- `max(Vb, 1e-6)` consumption/labor floor.
- Bare-`a` transfer-FOC scaling (`.*a/chi1`).
- `adjustment_cost(..., max(a, a_bar))` denominator floor.
- Illiquid-return taper `r_a*(1-0.1*(a/a_max)^9)`.
- Boundary/upwind selection, source-operator construction, contaminated-row
  stationary KFE, aggregation, cold initialization.
- `lab_solve2` / baseline-labor semantics (out of scope).

## 3. Phase C — focused parity/regression tests

New file: `tests/test_dlh_4d_r3_transfer_foc_parity.py` (9 tests):

| Test | Pins |
|---|---|
| `test_transfer_candidate_matches_literal_matlab_formula_for_finite_vb` | literal `HANK3_FOC` formula for all finite `v_b` (incl. negative) over a grid of `v_a`, `v_b`, `a` — exact equality |
| `test_transfer_candidate_accepts_finite_negative_vb` | negative `v_b` no longer raises; evaluates the literal formula |
| `test_transfer_candidate_uses_raw_vb_not_derivative_floor` | `v_b = 1e-7` (below floor) used raw, not floored to `1e-6` |
| `test_transfer_candidate_exact_zero_denominator_ieee_deterministic` | `v_b = 0` → `+Inf`/`-Inf`/`NaN` by sign of `v_a`; deterministic; no invented epsilon |
| `test_transfer_candidate_bare_a_scaling` | FOC scales by bare `a`; `a = 0 → 0` |
| `test_negative_vb_select_policy_floored_controls_raw_transfer` | **core regression**: selector returns a policy for `v_b = -0.5` (no guard raise); consumption `= (1e-6)^(-1/2)` and labor floored; transfer from raw negative `v_b` via literal formula |
| `test_exact_zero_vb_select_policy_absorbs_as_zero_transfer` | `v_b = 0.0` → all candidates `+Inf` → Idh masks absorb as zero-transfer (`"0"`, `transfer = 0.0`) |
| `test_positive_vb_select_policy_predecessor_contract` | positive-`v_b` behavior unchanged from predecessor |
| `test_adjustment_cost_preserves_max_a_abar_floor` | cost floor `max(a, a_bar)` preserved |

Narrow test updates (their sole purpose was enforcing the now-superseded
pre-repair identity):
- `tests/test_dlh_4b_import_identity.py`: `REQUIRED_SHA256` → post-repair SHA
  `1795718C…` (Issue #23 exception documented in-file).
- `tests/test_dlh_4d_ge_equations.py`: `test_immutable_oracle_identity` →
  `test_immutable_oracle_identity_detects_issue23_repair` (gate fail-closes with
  the exact authorized mismatch; on-disk SHA = post-repair identity).

**Predecessor Issue #18/#20/#21/#22 tests:** no test enforced the now-disproven
positivity guard (verified by grep), so no other test needed a behavioral update.

### Test results (full suite, `PYTHONPATH=src`):
```
137 passed in 190.91s (128 predecessor + 9 new)
```

## 4. Phase D — frozen-grid reclassification

Exact frozen Issue #20 fixture / Issue #21 729-point grid reclassified on the
repaired oracle (read-only, stage-resolved; identical stage map to Issue #22).
Full per-point before/after table: `DLH_4D_R3_NONFINITE_RECLASSIFICATION.csv`.
Reproducibility: **exact second-run equality across all 56 fields × 729 points
(0 diffs)** — satisfies the exact-reproducibility requirement.

### 4.1 Headline before/after (729 points)

| Metric | Before (Issue #21/#22) | After (Issue #23) |
|---|---|---|
| FULL_FINITE | 277 | **499** |
| Non-finite | 452 | **230** |
| Previously-non-finite → now finite (flipped) | — | **222** |
| Previously-finite → now non-finite (regression) | — | **0** |
| Old transfer-FOC guard failures | 415 | **2** (now a different message; see below) |
| KFE contaminated-row singular/non-finite | 37 | 60 |
| HJB non-convergence (1000 iters, stat > 1e-7) | 0 (all guard-failed first) | 168 |
| Aggregate failures | 0 | 0 |

### 4.2 Stage distribution after (729)

| Stage | Count |
|---|---|
| FULL_FINITE | 499 |
| HJB_NO_CONVERGENCE | 168 |
| KFE_CONTAMINATED_ROW_SINGULAR_NONFINITE | 60 |
| HJB_EXCEPTION | 2 |

### 4.3 What the repair changed

- **415 old-guard HJB exceptions** (`designated transfer FOCs require positive
  liquid derivatives`) are gone. Of those 415: **222 are now FULL_FINITE**, and
  the rest now progress to a legitimate later stage (HJB non-convergence or KFE
  singularity) instead of aborting at the Python-only guard.
- The **2 remaining HJB exceptions** carry a **different, new message**
  `ValueError: invalid source axis components` (a genuine downstream fail-closed
  from extreme drift/rates at those two cells), not the removed guard.
- **168 HJB_NO_CONVERGENCE** points (previously guard-aborted mid-iteration now
  run the full 1000 iterations; convergence statistic 5e-4 … 92, all > 1e-7):
  concentrated at `r_a ∈ {0.015, …, 0.12}` × `r_b ∈ {-0.05, …, 0.1}` — the
  repaired HJB honestly reports non-convergence instead of a spurious guard.
- **60 KFE singular/non-finite** (up from 37): more points now reach the KFE
  stage; the operator is genuinely singular at those candidates (concentrated at
  high `r_b = 0.1`, e.g. `(0.0, 0.025, …)`, `(0.12, 0.1, …)`).
- **0 regressions** among the 277 previously-finite points.
- **Exact reproducibility**: run1 vs run2 field-identical (56 fields × 729).

### 4.4 New failure classes (none invented by the repair)

The only new stage class is `HJB_NO_CONVERGENCE` — a direct, expected consequence
of letting the HJB run to completion instead of aborting at the removed guard. No
fixture/domain/GE tuning was performed; this is the honest before/after.


## 5. Phase E — frozen GE re-execution (INCONCLUSIVE)

Full details: `DLH_4D_R3_GE_REEXECUTION_REPORT.md`.

**Status: stopped by Owner instruction before reaching a terminal E1/E2 state.**
Per the Owner-specified bounded execution ceiling (~8 h), the frozen
`solve_ge(config)` re-execution (with the Issue #23-authorized oracle-identity
override only; the frozen config file was never modified) was run for **8.77 h
wall / 508.4 CPU-min** on the repaired oracle and then stopped at Owner request.
It had **not produced a terminal result** (no `phaseE.json`, no E1 root, no
RootBracketError/E2 fail-closed) when stopped. Per the Owner instruction, this
incomplete run is **not interpreted as GE PASS and not interpreted as E2**;
Phase E remains INCONCLUSIVE and is preserved as evidence for a later gate.

Frozen-path integrity during the run: `solve_ge` was invoked with the frozen
`GeConfig` (identity overridden to the post-repair oracle via
`dataclasses.replace`, never by editing the TOML); no solver parameters, domains,
or gates were changed. Runtime evidence (wall, CPU, last-observed warnings,
absence of terminal output) is preserved in `DLH_4D_R3_GE_REEXECUTION_REPORT.md`.

## 6. Caveats / notes for the next gate
1. `src/deep_learning_hank/two_asset/__init__.py` docstring still cites the
   pre-repair export SHA `276D2244…` (describes the accepted pre-repair export
   provenance). No export change was necessary, so per Issue #23 allowed-mutation
   rules it was left untouched; the post-repair identity is recorded here.
2. The frozen Issue #20 config identity gate now fail-closes against the
   authorized oracle change (expected; verified by test). A future Issue that
   re-freezes the repaired oracle should update the config gate.
3. The selector's general input-finiteness guard (`faithful local-policy inputs
   must be finite`) is unchanged: it fail-closes only for non-finite (NaN/Inf)
   inputs, which in MATLAB would yield a NaN ratio and downstream non-convergence;
   the Python fail-closed exception preserves that evidence at a different stage.
4. No fixture/domain/GE-economics tuning was performed; no PASS-seeking.

## 7. Terminal classification

**NOT CLAIMED.** Issue #23's terminal classes E1 (`…__FROZEN_GE_ROOT_READY_…`) and
E2 (`…__FROZEN_GE_STILL_BLOCKED_…`) both require a **terminal** frozen-GE
re-execution (E1: root validated against the Issue #20 gates; E2: fail-closed
with evidence). Phase E was stopped before either state, so **neither E1 nor E2
is claimed** in this report. The repair itself (Phases A–D) is complete and
reproducible; the frozen-GE re-execution is the sole outstanding deliverable,
preserved as an explicit INCONCLUSIVE item for the next gate.
