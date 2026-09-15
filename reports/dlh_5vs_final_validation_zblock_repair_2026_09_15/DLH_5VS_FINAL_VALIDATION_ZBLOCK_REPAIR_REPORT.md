# DLH-5V-S — Minimal `final=True` F0 z-block destination repair and corrected validation re-check

**Issue:** #67 / DLH-5V-S
**Task type:** `SCIENTIFIC_CHANGE__MINIMAL_FINAL_VALIDATION_OPERATOR_REPAIR_AND_REVALIDATION`
**Route decision:** `APPROVE_MINIMAL_FINAL_VALIDATION_ZBLOCK_DESTINATION_REPAIR_AFTER_5VR_TERMINAL_A`
**Authority marker:** `DLH_5VS_MINIMAL_FINAL_VALIDATION_ZBLOCK_REPAIR_AUTHORIZED`
**Initial authoritative activation:** `5672573849`
**Final authoritative activation-refresh:** `5672691735`
**Post-sync live `main`:** `496d14404116cbe76a54df3aa595b91256b30c10`
**Dedicated Builder branch:** `dsh/issue-67-dlh-5vs-final-validation-zblock-repair-2026-09-15`
**Date:** 2026-09-15

## TERMINAL (exactly one)

```
DLH_5VS_FINAL_VALIDATION_ZBLOCK_REPAIR__CORRECTED_FINAL_OPERATOR_MATCHES_MATLAB_FAITHFUL_LAYOUT__SPURIOUS_CROSS_Z_VALIDATION_GAP_REMOVED__HJB_RESIDUAL_REASSESSMENT_GATE_READY
```

## 0. Scope ceiling — what this Issue does and does NOT claim

This Issue performs a **repair + corrected validation re-check only**.

- The repaired `final=True` F0 operator is now **bit-for-bit (to machine
  precision) equal to the accepted iteration operator** at the same `V_*` and
  the same current selected controls, so the corrected final-validation
  residual equals the accepted `R_iter` exactly.
- This is a statement about **operator structure**, NOT a convergence claim.
- **HJB convergence is NOT declared.** The corrected residual
  (`10.435094313164921`) is still ~`1.04e4` times larger than the unchanged
  Bellman tolerance `1e-3`. The Bellman tolerance remains the unchanged
  acceptance threshold.
- `R_iter` is **NOT** declared an accepted final convergence residual.
- **No new HJB iterate is accepted.** No Newton / policy iteration / semismooth
  / trust-region / continuation / line search / parameter sweep was run. No KFE
  / stationary KFE / steady state / GE / neural / calibration / policy /
  welfare / Results work was run.

## 1. The authorized scientific change

Only authorized source mutation: exactly one location inside the `final=True` F0
off-diagonal destination assembly of
`src/deep_learning_hank/two_asset/boundary_hjb_selected_q.py`.

```diff
@@ -975,7 +975,7 @@ class BoundaryHJBSolver:
                                 entries.append((dn, float(rate)))
                         diag = -(bb + bf + ab + af)
                         for dn, rate in entries:
-                            rows.append(row); cols.append(dn); data.append(rate)
+                            rows.append(row); cols.append(nz * self.n + dn); data.append(rate)
                         rows.append(row); cols.append(row); data.append(diag)
                         u[row] = rec.utility
```

- Repaired blob: `556ccc214f03a1a22306cc4f5c7e9f7691bbf897`
- Pre-repair blob (frozen comparison authority):
  `7ea342ccbe15d852b90743b14bb4b02977c2d78b`
- Diff size: **1 insertion / 1 deletion**, exactly one line, no other change.

**Scientific meaning.** Only the z-block destination index is repaired, so that
z=1 F0 off-diagonal destinations remain inside the z=1 block, aligned with the
accepted iteration path (`local_interior_row`), the accepted boundary path
(`_boundary_row`) and the MATLAB-faithful state layout (`row = nz*n + node`).

Unchanged (verified): raw drift calculation; `max(±mu)/step` final rate
formulas; continuous controls; policy selection; diagonal construction;
switch-matrix assembly; economics; prices; grid/domain; initialization;
tolerances; `PB_MARGIN`; convergence criterion; accepted `final=False`
iteration semantics.

The repair makes all three assembly sites agree; the file now contains the
same-z-block form at exactly three lines (978 = repaired `final=True` F0 path,
1008 = accepted iteration path, 1029 = accepted boundary path) and **zero**
bare-destination assembly sites.

## 2. Frozen reconstruction (reproduced exactly)

Deterministic reconstruction of the accepted Issue #63 stagnation state `V_*`
using the accepted Issue #64/#65 helper `reconstruct_issue63_stagnation_state()`,
stopping immediately after accepted FTB step 8.

| Required baseline | Required | Reproduced |
|---|---|---|
| iterations | 8 | **8** |
| final statistic | `3.6614352438846254e-08` | **`3.6614352438846254e-08`** |
| min boundary `p_b` | `4.8089461301970005e-09` | **`4.8089461301970005e-09`** |
| wall state | F3 (13,13), z=1 | **F3 (j=13, i=13, z=1), node 332** |
| accepted `\|\|R_iter\|\|_inf` | `10.435094313164921` | **`10.435094313164921`** |

Grid facts: `n = 391` nodes (F0 = 298), `nz = 2`, `state_size = 782`,
F0 rows = **596**, non-F0 boundary rows = 186.

## 3. Corrected final residual and its argmax

At the same `V_*`, the diagnostic performs exactly ONE `final=False`
current-policy build and exactly ONE corrected `final=True` current-policy build
that consumes the **SAME** current selected F0 controls (`same_controls_max_abs_diff
= 0.0`).

```
R_corrected = rho * V_* - (u_corrected + Q_corrected @ V_*)
```

| Quantity | Value |
|---|---|
| corrected final residual `\|\|R_corrected\|\|_inf` | **`10.435094313164921`** |
| corrected residual argmax | **F0, node 97, (j=3, i=2), z=0** |
| corrected residual F0-part max | `10.435094313164921` |
| corrected residual non-F0 boundary max | `9.742068328671465` |

### Comparison against the accepted baselines

| Quantity | Value |
|---|---|
| pre-repair current-record final residual (accepted Issue #65) | `490.7560414005864` |
| pre-repair stale-record final residual (accepted Issue #65) | `490.7560425919994` |
| accepted `\|\|R_iter\|\|_inf` | `10.435094313164921` |
| **corrected residual** | **`10.435094313164921`** |
| residual improvement (pre-repair current − corrected) | `480.3209470874215` |
| corrected residual / pre-repair residual | `0.02126330280801807` |
| corrected residual / `R_iter` | `1.0` |
| corrected residual / accepted final baseline | `0.02126330280801807` |

### Pre-repair reconciliation (derived, structurally validated)

The pre-repair comparison operator is reconstructed exactly in coordinate space:
the repair is a pure destination-column reassignment on F0 off-diagonal entries,
so the defective operator equals the repaired operator with each F0 row's
off-diagonal destinations moved back to the bare node column `dn`. Non-F0 rows,
every diagonal and `u` are identical; duplicate destinations are summed exactly
as the assembly does.

| Reconciliation check | Value | Accepted reference |
|---|---|---|
| derived pre-repair `\|\|R\|\|_inf` | **`490.7560414005864`** | `490.7560414005864` (**exact match**) |
| derived pre-repair argmax | F0, node 272, (j=10, i=5), z=1 | — |
| derived pre-repair vs ITER F0 rowwise max | **`24.601971766296664`** | `24.601971766296664` (**exact match**) |
| structural match flag | `True` | — |

Both independently accepted Issue #65/#66 numbers are reproduced exactly by the
derived model, so the ~`480.32` residual drop is **fully attributed to the
repaired z-block destination index** and to nothing else.

> Note. The accepted pre-repair *current-record* baseline `490.7560414005864`
> is reproduced to the last bit by the derived model; the accepted *stale-record*
> value `490.7560425919994` differs from it by `1.19e-6`, consistent with the
> accepted Issue #65 finding that the stale-record effect is negligible
> (`\|\|D_stale\|\|_inf = 1.8406872158038823e-05`). No stale-record re-run was
> required or performed.

## 4. Exact repair-equivalence checks

| Check | Result |
|---|---|
| z=0 F0 behavior unchanged | **`0.0`** rowwise max diff (298/298 rows bit-identical) |
| z=1 F0 changed by the repair | `24.601971766296664` rowwise max (298 rows) |
| z=1 F0 final off-diagonal destinations use `nz*n + dn` | **all in-block**, 0 misplaced of 1192 checked off-diagonal entries |
| corrected final directional rates unchanged | **`1.4210854715202004e-14`** (machine precision rate-class max diff) |
| corrected final diagonal unchanged | **`1.4210854715202004e-14`** |
| corrected final row layout vs MATLAB-faithful post-convergence layout | **matches**: corrected final vs ITER rowwise max = `1.4210854715202004e-14` ≤ `1e-9` (total, not only F0) |
| pre-repair cross-z operator gap | `24.601971766296664` (argmax F0 node 297, (11,11), z=1 — reproduces Issue #66) |
| corrected cross-z operator gap | **removed**: `1.4210854715202004e-14` at machine precision |
| unintended cross-z contamination beyond the explicit exogenous switch matrix | **`0.0`** (all off-block content equals `B` exactly; 0 contaminating rows) |
| non-F0 boundary `Q` diff | **`0.0`** |
| non-F0 boundary `u` diff | **`0.0`** |
| utility/source diff (F0) | **`0.0`** |
| `max\|Q 1\|` iteration / corrected | `2.4253377084448857e-12` / `2.4253377084448857e-12` (conservativity preserved, identical) |
| optimizer expansions iteration / corrected | `0` / `0` |
| artificial bindings iteration / corrected | `0` / `0` |
| deterministic repeat | **identical** |

## 5. Terminal derivation (frozen ex ante rule)

- The authorized z-block repair is finite and deterministic: **yes**.
- The corrected final `final=True` F0 row assembly matches the
  MATLAB-faithful / accepted-iteration post-convergence layout within
  `1e-9`: **yes** (`1.42e-14`).
- The pre-repair material cross-z operator gap is removed: **yes**
  (`24.60` → `1.42e-14`).
- Derived pre-repair baselines reconcile exactly: **yes**.

→ **Outcome A** (residual reassessment gate ready), exactly one terminal.

## 6. Deterministic repeat

The full diagnostic was executed twice. All compared fields are identical
(`deterministic_repeat_identical = True`), including the corrected residual,
its argmax, the operator gaps, the reconciliation values and the terminal.

## 7. Tests

- Focused suite `tests/test_dlh_5vs_final_validation_zblock_repair.py`:
  **20 passed**.
- Full repository suite `python -m pytest tests/ -q`:
  **11 failed, 521 passed, 6 warnings in 3468.01 s (0:57:48)**.

### 7.1 The 11 failures are STALE PRE-REPAIR ASSERTIONS, not a code regression

The 11 failing tests are accepted Issue #64 / #65 / #66 tests that hard-code the
**pre-repair defective operator's** numerical signature. The authorized repair
necessarily and correctly changes exactly that signature. Every failure is a
pure consequence of the authorized change; none of them indicates a defect in
the repaired implementation.

Corrected values at the same `V_*` (independently measured):

```
r_iter_inf                                   10.435094313164921     (unchanged)
r_final_inf / r_final_stale_inf              10.435094313165099     (was 490.7560425919994)
r_final_f0_max / r_final_stale_f0_max        10.435094313165099     (was 490.7560425919994)
r_final_current_inf / r_final_current_f0_max 10.435094313164921     (was 490.7560414005864)
r_diff_inf / d_total_inf / d_stale_inf       4.654054919228656e-13  (was 488.0988429898615)
d_rate_inf                                   3.410605131648481e-13  (was 488.0988417984485)
q_current_minus_iter_rowwise_max             1.4210854715202004e-14 (was 24.601971766296664)
class_destination_assembly_gap.affected_rows 0                      (was 298)
```

| # | Test | Line | Pinned (pre-repair) | Corrected | Nature |
|---|---|---|---|---|---|
| 1 | `test_dlh_5vp::test_reconstruction_reproduces_accepted_issue63_terminal` | 95 | `490.7560425919994` | `10.435094313165099` | stale numeric baseline |
| 2 | `test_dlh_5vp::test_iteration_and_final_residuals_separated_and_reproduced` | 112, 114, 115 | `490.7560425919994`, `!=`, `488.0988429898615` | `10.435094313165099`, equality, `4.65e-13` | stale numeric baseline + **inverted conclusion** (`r_iter_inf != r_final_inf` is no longer true) |
| 3 | `test_dlh_5vp::test_f0_boundary_decomposition_consistent_and_deterministic` | 131 | `490.7560425919994` | `10.435094313165099` | stale numeric baseline |
| 4 | `test_dlh_5vq::test_r_final_stale_exact_reproduction` | 70 | `490.7560425919994` | `10.435094313165099` | stale numeric baseline |
| 5 | `test_dlh_5vq::test_additive_decomposition_holds` | 133 | `488.0988429898615` | `4.654054919228656e-13` | stale numeric baseline |
| 6 | `test_dlh_5vq::test_operator_differences_are_f0_only` | 222 | `> 1.0` | `1.4210854715202004e-14` | **inverted conclusion**: the final-vs-iteration operator gap is no longer material |
| 7 | `test_dlh_5vr::test_r_final_current_exact` | 130 | `490.7560414005864` | `10.435094313164921` | stale numeric baseline |
| 8 | `test_dlh_5vr::test_f0_gap_exact` | 141 | `24.601971766296664` | `1.4210854715202004e-14` | stale numeric baseline |
| 9 | `test_dlh_5vr::test_directional_extraction_and_gap_decomposition` | 171, 188 | `298` affected rows | `0` | **inverted conclusion**: destination assembly is no longer the discrepancy |
| 10 | `test_dlh_5vr::test_classification_deterministic` | 249, 251, 252 | `both_equivalent is False`, `materially_non_equivalent is True`, terminal A | `both_equivalent is True`, `materially_non_equivalent is False`, outcome `MIXED_OR_UNRESOLVED` | **inverted conclusion** |
| 11 | `test_dlh_5vr::test_runtime_exactly_two_builds_at_vstar` | 382 | `24.601971766296664` | `1.4210854715202004e-14` | stale numeric baseline |

Why items 6, 9 and 10 are qualitative rather than numeric: those assertions
encoded the scientific *conclusions* that the Issue #66 audit was accepted for
(`FINAL_EQ_MATLAB = false`; destination assembly is the material discrepancy;
298 z=1 F0 rows affected; `materially_non_equivalent = true`). Those
conclusions were conclusions **about the defect**. Removing the defect removes
their subject matter, so they cannot be satisfied by re-numbering: the Issue #66
audit's own internal MATLAB-faithful reference still places F0 destinations at
bare column `dn`, while the repaired source (authorized) and the oracle (source
truth) do not. Post-repair the Issue #66 audit classifies as
`MIXED_OR_UNRESOLVED` precisely because its rate check now agrees and its
assembly check no longer does.

### 7.2 Consequence — a governance dependency NOT covered by this allowlist

`tests/test_dlh_5vp_stagnation_newton_geometry.py`,
`tests/test_dlh_5vq_f0_final_validation_semantics_audit.py` and
`tests/test_dlh_5vr_f0_final_rate_provenance.py` are **accepted read-only
artifacts of Issues #64, #65 and #66** and are explicitly **outside** the
Issue #67 four-path allowlist ("All other accepted sources/tests/reports/
governance remain read-only"). They were therefore deliberately **NOT
modified**.

There is a genuine conflict between two Issue #67 requirements:

- §8 requires the full repository suite to pass;
- §7 allows tracked changes to exactly four paths, none of which is a dependent
  test file.

The repair was executed as authorized and the conflict is reported rather than
worked around. Resolving it requires explicit Owner authorization for one of:

1. **supersede / retire** the affected Issue #66 assertions and re-baseline the
   three dependent test modules post-repair (authorizing a ninth path, or a
   successor task), or
2. **declare** those assertions historical accepted evidence for the pre-repair
   operator, frozen under the pre-repair blob and no longer part of the live
   regression gate.

Neither decision is taken here. The repaired source, its focused regression
suite, the corrected validation evidence and the terminal are complete and
self-consistent; only the historical baselines remain outstanding.

### 7.3 Focused coverage

Focused coverage: source repair is exactly the one authorized location; no
bare-destination assembly remains and all three assembly sites agree; z=0
unchanged; z=1 same-z-block placement; final rate formulas unchanged; diagonal
unchanged; utility/source unchanged; corrected final layout equals the
MATLAB-faithful post-convergence layout; exact `V_*` reconstruction; `R_iter`
reproduction; corrected final residual finite and deterministic; non-F0
boundary unchanged; `Q` conservativity; no new artificial binding / optimizer
expansion; deterministic repeat identical; no new accepted HJB iterate; no
Newton / continuation / line search / KFE / stationary KFE / steady-state
invocation; fail-closed on non-finite evidence and on a missing F0 record;
exactly one terminal.

## 8. Authorized files (exact four-path allowlist)

1. `src/deep_learning_hank/two_asset/boundary_hjb_selected_q.py`
2. `tests/test_dlh_5vs_final_validation_zblock_repair.py`
3. `reports/dlh_5vs_final_validation_zblock_repair_2026_09_15/DLH_5VS_FINAL_VALIDATION_ZBLOCK_REPAIR_REPORT.md`
4. `reports/dlh_5vs_final_validation_zblock_repair_2026_09_15/DLH_5VS_FINAL_VALIDATION_ZBLOCK_REPAIR_SUMMARY.csv`

No fifth tracked Builder path. All other accepted sources, tests, reports and
governance files remain read-only and are byte-identical to the accepted blobs
listed in the Issue #67 completion comment.

## 9. Next gates (for the Owner / reviewer — NOT decided here)

**Gate 1 — residual reassessment.** The corrected final-validation operator now
coincides with the accepted iteration operator, so the ~`490.756`
final-validation failure is fully attributed to the repaired assembly defect.
The residual that remains (`10.435094313164921`) is a separate, pre-existing
convergence question that this Issue does **NOT** resolve and does **NOT**
reclassify. Any change to the convergence criterion, any acceptance of `R_iter`
as the final convergence residual, and any new HJB iterate require fresh
explicit Owner authorization.

**Gate 2 — stale dependent baselines.** As documented in §7.2, 11 assertions in
three accepted read-only test modules pin the pre-repair defect's signature and
now fail. Three of them encode conclusions that the repair inverts
qualitatively. This is outside the Issue #67 allowlist and is reported, not
worked around; it needs an explicit Owner decision (supersede/re-baseline the
Issue #64/#65/#66 test evidence, or declare those assertions frozen historical
evidence for the pre-repair operator).

Stationary KFE remains **NOT AUTHORIZED**.
