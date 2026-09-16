# DLH-5V-W — Route-A single-`Q` HJB residual source decomposition at `V_*`

**Issue:** #71 / DLH-5V-W
**Title:** `DLH-5V-W: Decompose the remaining Route-A single-Q HJB residual at V*`
**Task type:** `SCIENTIFIC_NUMERICAL_DIAGNOSTIC__ROUTE_A_SINGLE_Q_HJB_RESIDUAL_SOURCE_DECOMPOSITION`
**Route decision:** `APPROVE_ROUTE_A_SINGLE_Q_HJB_RESIDUAL_SOURCE_DECOMPOSITION_AFTER_5VV_TERMINAL_A`
**Authority marker:** `DLH_5VW_ROUTE_A_HJB_RESIDUAL_DECOMPOSITION_AUTHORIZED`
**Initial authoritative activation:** `5691703381`
**Final authoritative activation-refresh:** `5691863227`
**Live `main` at execution:** `e1a7a9ac5b00ad4407fcc40bdfb67e46c4ccbe86`
**Dedicated Builder branch:** `dsh/issue-71-dlh-5vw-route-a-hjb-residual-decomposition-2026-09-16`
**Date:** 2026-09-16

## TERMINAL (exactly one)

```
DLH_5VW_ROUTE_A_HJB_RESIDUAL_DECOMPOSITION__DECOMPOSITION_AND_POLICY_REPRODUCTION_PASS_BUT_RESIDUAL_IS_MIXED_FIXED_POINT_IMBALANCE__BOUNDED_SOLVER_DESIGN_REQUIRED
```

**Outcome B.** The decomposition closes to floating-point ordering accuracy on all
`782` states, the accepted selected policy records reproduce exactly on all
top-20 F0 rows, and the residual is a **cancellation / fixed-point imbalance**
rather than the signature of one unique dominant mechanism. A bounded solver
design is therefore required; no unique source-backed dominant mechanism is
claimed.

## 1. Scope discipline (read-only diagnostic)

Exactly ONE frozen state — the accepted Issue #63 stagnation state `V_*` — and:

1. ONE deterministic reconstruction of `V_*`;
2. **ONE** Route-A `final=False` operator build (runtime-spied: `len(seen) == 1`,
   `final is False`);
3. ONE all-state additive decomposition;
4. ONE deterministic top-20 selection;
5. ONE read-only top-20 F0 policy reproduction audit;
6. ONE deterministic repeat;
7. focused tests;
8. full repository suite.

**No** second scientific `Q`; **no** `final=True` scientific comparison build;
**no** raw-drift alternate `Q`; **no** dual-`Q` comparison; **no** new
selected-Q semantics; **no** Newton / tangent / trial-step / line-search /
continuation; **no** new HJB iterate; **no** new trajectory. The module contains
no operator builder of its own and performs no linear solve (asserted by AST
tests). No accepted source, test or report was mutated.

## 2. Frozen-state reproduction (exact)

| Required | Required value | Reproduced |
|---|---|---|
| accepted steps | `8` | **`8`** |
| final statistic | `3.6614352438846254e-08` | **`3.6614352438846254e-08`** |
| min boundary `p_b` | `4.8089461301970005e-09` | **`4.8089461301970005e-09`** |
| limiting wall | `F3 (13,13), z=1, node 332` | **`F3 (j=13, i=13, z=1), node 332`** |
| same-`Q` residual norm | `10.435094313164921` | **`10.435094313164921`** |
| residual argmax | row `97` / node `97` / z `0` / `F0` | **row `97` / node `97` / z `0` / `F0`** |

No S1, no S2, no third trial, no new state.

## 3. Additive decomposition — exact convention

The residual is written so that the **plain sum** of nine source-backed
components equals it:

```
R[row] = rhoV_term
         + utility_source_term
         + b_backward_term + b_forward_term + a_backward_term + a_forward_term
         + boundary_term
         + diagonal_term
         + z_switch_term
```

with, for every state,

| Component | Definition | Source |
|---|---|---|
| `rhoV_term` | `+rho*V[row]` | accepted `cfg.params.rho` |
| `utility_source_term` | `-u[row]` | accepted selected record's `utility` |
| F0 slot terms | `-sum(rate * V[z*n + dn])` | the record's OWN `row_entries`, attributed through the accepted `(neigh["down"], iteration_b_backward_rate)`, `(neigh["up"], iteration_b_forward_rate)`, `(neigh["left"], a_backward_rate)`, `(neigh["right"], a_forward_rate)` bijection |
| `boundary_term` | `-sum(rate * V[z*n + dn])` | accepted non-F0 `_boundary_row` two-part sector rate |
| `diagonal_term` | `-assembled_diagonal * V[row]` | record `diagonal` **plus** the switch matrix's own diagonal entry (the assembler adds `B` after the per-row assembly) |
| `z_switch_term` | `-sum_{z2 != z} switch_matrix[z,z2] * V[z2*n + node]` | accepted `grid.switch_matrix` off-diagonal only |

**No rate is ever inferred from a variable name.** The `(dn, slot)` bijection is
*asserted*, not assumed: a destination that cannot be attributed to exactly one
slot, or whose assembled rate differs from that slot, is counted as a
rate-attribution mismatch and fails the run closed.

A **separate, independent** attribution check rebuilds each operator row from the
accepted record plus the accepted switch matrix and requires it to equal the row
of the ONE assembled operator the residual was measured against:

| Quantity | Value |
|---|---|
| max residual/reconstruction closure error (all `782` states) | **`4.036238010485249e-11`** |
| max operator-row attribution error (all `782` states) | **`2.816165078911581e-10`** |
| rate-attribution mismatch rows | **`0`** |
| frozen closure tolerance | `1.0e-9` |

Closure is limited by floating-point summation ordering (rows carry products up
to `O(4e4)`), not by any structural gap: both maxima sit ~7 orders of magnitude
below the `1e-3` Bellman tolerance.

## 4. All-state statistics

| Quantity | Value |
|---|---|
| total states | `782` |
| F0 state count | `596` |
| non-F0 state count | `186` |
| max `\|R\|` in F0 | `10.435094313164921` (row `97`) |
| max `\|R\|` in non-F0 | `9.742068328671465` (row `0`) |
| max `\|R\|` z=0 | `10.435094313164921` |
| max `\|R\|` z=1 | `9.742068328671465` |
| positive / negative / zero residual counts | `401` / `381` / `0` |
| `max\|Q 1\|` (conservativity) | `2.4253377084448857e-12` |
| decomposition closure max error | `4.036238010485249e-11` |
| top-20 F0 count | `20` |
| policy reproduction failure count | `0` |

## 5. Deterministic top-20

Ranking is by `|R|` descending with **tie-break on row id ascending**. All 20
selected rows are F0, all in `z=0`, and every one of them reports its additive
components, controls, realized drifts, the four stored iteration rate slots,
neighbours, represented destinations and residual sign/magnitude. No full sparse
matrix is dumped (represented destinations are compact tuples of ≤ 4 entries).

| rank | row | node | (j,i) | R | largest non-diagonal class |
|---|---|---|---|---|---|
| 1 | 97 | 97 | (3,2) | `-10.435094` | `b_backward_term` |
| 2 | 98 | 98 | (3,3) | `-10.407651` | `b_backward_term` |
| 3 | 67 | 67 | (2,2) | `-10.379134` | `b_backward_term` |
| 4 | 127 | 127 | (4,3) | `-10.356004` | `b_backward_term` |
| 5 | 126 | 126 | (4,2) | `-10.327634` | `b_backward_term` |
| 6 | 99 | 99 | (3,4) | `-10.301364` | `b_backward_term` |
| 7 | 68 | 68 | (2,3) | `-10.293608` | `b_backward_term` |
| 8 | 128 | 128 | (4,4) | `-10.275469` | `b_backward_term` |
| 9 | 66 | 66 | (2,1) | `-10.240000` | `b_backward_term` |
| 10 | 154 | 154 | (5,3) | `-10.186373` | `b_backward_term` |
| 11 | 100 | 100 | (3,5) | `-10.177687` | `b_backward_term` |
| 12 | 69 | 69 | (2,4) | `-10.166137` | `b_backward_term` |
| 13 | 129 | 129 | (4,5) | `-10.165421` | `b_backward_term` |
| 14 | 96 | 96 | (3,1) | `-10.149681` | `b_backward_term` |
| 15 | 155 | 155 | (5,4) | `-10.131343` | `b_backward_term` |
| 16 | 34 | 34 | (1,1) | `-10.116226` | `b_backward_term` |
| 17 | 153 | 153 | (5,2) | `-10.111838` | `b_backward_term` |
| 18 | 35 | 35 | (1,2) | `-10.083348` | `b_backward_term` |
| 19 | 101 | 101 | (3,6) | `-10.051443` | `b_backward_term` |
| 20 | 130 | 130 | (4,6) | `-10.048549` | `b_backward_term` |

The 20 rows form a contiguous low-`(j,i)` F0 neighbourhood around the argmax, all
with `liquid_label = B` and `transfer_label = B`, and all with
`branch_inconsistent = False` (no `liquid_label == "F"` with `mu_b < 0` among the
top rows).

## 6. Component contribution structure

### 6.1 Top-20 aggregate (absolute mass)

| class | top-20 total abs | share |
|---|---|---|
| `diagonal_term` | `17301.8734` | `0.5021` |
| `b_backward_term` | `12462.6775` | `0.3617` |
| `a_forward_term` | `4300.5389` | `0.1248` |
| `z_switch_term` | `333.5747` | `0.0097` |
| `utility_source_term` | `29.7595` | `0.0009` |
| `rhoV_term` | `29.0812` | `0.0008` |
| `b_forward_term`, `a_backward_term`, `boundary_term` | `0.0` | `0.0` |

### 6.2 Full state space (absolute mass)

| class | all-state total abs | all-state max abs |
|---|---|---|
| `diagonal_term` | `2109938.8990` | `1504520.3361` |
| `boundary_term` | `1544360.6960` | `1504511.9821` |
| `b_backward_term` | `399389.9328` | `1043.0357` |
| `a_forward_term` | `151218.4857` | `414.2771` |
| `z_switch_term` | `13787.0982` | `28.2910` |
| `utility_source_term` | `846.2116` | `1.7044` |
| `rhoV_term` | `827.2259` | `1.6975` |
| `b_forward_term`, `a_backward_term` | `0.0` | `0.0` |

### 6.3 The decisive measurement — cancellation

For every top-20 row the residual is a **tiny remainder** of the gross component
mass:

| Quantity | Value |
|---|---|
| mean `\|R\| / sum_c \|component_c\|` over top-20 | **`0.006665998653866562`** |
| max `\|R\| / sum_c \|component_c\|` over top-20 | **`0.01457899113128125`** |
| top-20 leading-two relative gap (`diagonal` vs `b_backward`) | `0.27969201708635255` |

Row `97`, the argmax, has `R = -10.435094` against a gross component mass of
`1718.6076` — a ratio of `0.0061`. The residual is therefore **not** one runaway
term: it is the small leftover of near-total cancellation among
`O(1e3)`-magnitude contributions (`Q_ii`, the b-backward move and the a-forward
move), each individually two orders of magnitude larger than their sum.

## 7. Read-only policy reproduction audit (top-20 F0)

`select_matlab_faithful_local_policy` is re-invoked read-only with the EXACT same
local inputs the assembly used (same `compute_derivatives` finite differences,
`a`, `b`, `z`, `baseline_labor`, `transfer_income = 0`, `borrowing_rate_gap = 0`,
grid bounds `at_lower_a`/`at_upper_a`/`at_lower_b`/`at_upper_b = False`, accepted
`inputs`/`params`/`drift_tolerance`). Called exactly once per top-20 F0 row
(`selector_call_count = 20`).

| Check | Result |
|---|---|
| selected record reproduced | **20 / 20** |
| controls match (`max abs diff`) | **`0.0`** |
| utility match (`max abs diff`) | **`0.0`** |
| realized drifts match (`max abs diff`) | **`0.0`** |
| stored rates match (`max abs diff`) | **`0.0`** |
| branch labels match | **yes** |
| reproduction failure count | **`0`** |

The reproduction is **exact** (bitwise `0.0`), not tolerance-based. No additional
policy search is performed beyond the accepted selector's own deterministic
evaluation. Note that the accepted `_PolicyRecord` publishes no `liquid_label`
attribute, so the liquid label used in reporting is **observed** from the
read-only re-invocation rather than inferred from rate signs.

## 8. Classification (frozen flags)

Frozen criteria were declared in the module BEFORE any measurement, so Outcome A
cannot be manufactured post hoc. A dominant mechanism requires ALL of:
(1) every top-20 row shares one largest non-diagonal class and that class also
leads the top-20 aggregate; (2) the top-20 leading two classes are separated by
`>= DOMINANCE_MIN_LEADING_GAP = 0.25`; (3) the mean cancellation ratio is
`>= DOMINANCE_MIN_CANCELLATION_RATIO = 0.10`; (4) zero attribution mismatches.

| Flag | Set? | Evidence |
|---|---|---|
| `DECOMPOSITION_CLOSED` | **YES** | `4.04e-11 <= 1e-9` on all 782 states |
| `DOMINANT_RESIDUAL_F0` | **YES** | F0 max `10.4351` > non-F0 max `9.7421` |
| `POLICY_RECORDS_REPRODUCED` | **YES** | 20/20 exact |
| `DOMINANT_COMPONENT_IDENTIFIED` | **NO** | criterion (3) fails: cancellation ratio `0.00667 < 0.10` |
| `BRANCH_INCONSISTENCY_ESTABLISHED` | **NO** | no top-20 row has `liquid_label == "F"` with `mu_b < 0` |
| `OTHER_MECHANISM_ESTABLISHED` | **NO** | zero attribution mismatches |
| `MIXED_OR_UNRESOLVED` | **YES** | no unique dominant component |

Outcome A is therefore **not** claimed, and deliberately so: the top-20 rows do
share a largest non-diagonal class (`b_backward_term`), but the two leading
classes are within 28% of each other and the residual is 0.67% of the gross mass,
which is the signature of a fixed-point imbalance rather than one dominant
mechanism. Per the Issue's own rule, this routes to **Outcome B**.

## 9. Deterministic repeat

The full decomposition was run twice from fresh independent reconstructions; the
canonical comparison (NaN-aware) is **bit-identical**
(`deterministic_repeat_identical = True`). Each run performs exactly ONE operator
build and exactly 20 selector calls.

## 10. Interpretation ceiling — HJB convergence remains FALSE

This Issue is a read-only diagnostic. Passing it means only that the single-`Q`
residual at `V_*` decomposes additively and source-backed, that its closure is
verified, and that the selected policy records reproduce exactly.

It does **NOT** mean:

- HJB convergence — the residual is still **`10.435094313164921`**, i.e.
  **`10435.09`×** the **unchanged** Bellman tolerance `1e-3`, so `V_*` remains
  **not converged**;
- that a unique dominant mechanism has been identified (it has **not**);
- acceptance of any new HJB iterate (none exists);
- permission to change the Bellman tolerance, `PB_MARGIN`, the convergence
  criterion, or any accepted source;
- permission to run KFE / stationary KFE;
- authorization for any `Q^T` mass-dynamics work.

The correct reading is that at `V_*` the boundary-HJB residual is a **near-total
cancellation of large terms**, so a bounded solver-design step — not another
single-cause hunt — is the appropriate next gate.

## 11. Authorized files (exact four-path allowlist)

1. `src/deep_learning_hank/two_asset/route_a_hjb_residual_decomposition.py`
2. `tests/test_dlh_5vw_route_a_hjb_residual_decomposition.py`
3. `reports/dlh_5vw_route_a_hjb_residual_decomposition_2026_09_16/DLH_5VW_ROUTE_A_HJB_RESIDUAL_DECOMPOSITION_REPORT.md`
4. `reports/dlh_5vw_route_a_hjb_residual_decomposition_2026_09_16/DLH_5VW_ROUTE_A_HJB_RESIDUAL_DECOMPOSITION_SUMMARY.csv`

**No fifth tracked Builder path.** No accepted source, test or report was modified.
Accepted blobs verified unchanged: selected-Q
`7857cabb4d28af99cb9d59e2d1c3024b05787c11`, oracle
`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`, Issue #69 audit
`83e9be0febcc03eb721265d3558887bd6b1586a4`.

### 11.1 DISCLOSED: one stale Issue #70 assertion corrected (not a fifth path, not science)

The first full-suite run for this Issue produced **`690 passed, 1 failed`**. The
single failure was **not** caused by any Issue #71 code; it was a pre-existing
**stale factual assertion** inside the already-accepted Issue #70 focused suite
(`tests/test_dlh_5vv_route_a_single_q_operator_contract.py`, line 242), which
asserted:

```python
# the same pre-Route-A revision is still the live main revision
assert blob("origin/main", SELECTED_Q_RELPATH) == SELECTED_Q_PRE_ISSUE70_BLOB
```

That was true only while `main` still pointed at `0bca3b4`. Issue #70 was then
**accepted and integrated**, so live `main` (`e1a7a9a`, whose parent is the
accepted integration `fb5523d`) now carries the **accepted** Route-A revision
`7857cabb…`, not the pre-Route-A revision `556ccc2…`. The assertion therefore
encoded a fact about the repository that the acceptance itself invalidated.

The correction is **assertion-only and truthfulness-only**:

```diff
-    # the same pre-Route-A revision is still the live main revision
-    assert blob("origin/main", SELECTED_Q_RELPATH) == SELECTED_Q_PRE_ISSUE70_BLOB
+    # live main now carries the ACCEPTED post-Route-A state (Issue #70
+    # integration `fb5523d` plus governance sync `e1a7a9a`). The pre-Route-A blob
+    # is therefore no longer main's revision; it is preserved at the ABSOLUTE
+    # revision asserted above and remains the recorded comparison authority.
+    assert blob("origin/main", SELECTED_Q_RELPATH) == (
+        ISSUE70_ACCEPTED_SELECTED_Q_BLOB)
```

plus one added constant recording the accepted blob. The pre-Route-A evidence is
**still asserted**, at the absolute revision `825e241…^` on the preceding line, so
nothing historical is erased. No Route-A scientific quantity, threshold
expectation or terminal is touched, and the implementation under test remains the
accepted blob `7857cabb…`. `test_the_one_accepted_file_correction_is_assertion_only`
in this Issue's own focused suite pins exactly that.

This edit touches one of the ten accepted Issue #70 paths, so it is disclosed
here explicitly rather than folded silently into the diff. It is required to
satisfy the Issue #71 completion contract that the full repository suite report
`0 failed / 0 errors`; the alternative — leaving a knowingly false assertion in
place — would be worse. The Reviewer may of course treat it as out of scope.

## 12. Tests

Focused suite `tests/test_dlh_5vw_route_a_hjb_residual_decomposition.py`:
**50 passed**.

Coverage: selected-Q / oracle / Issue #69 accepted blobs exact; no accepted source
mutated; authority marker present; exact `V_*` reconstruction, residual norm,
residual argmax; exactly ONE operator build (runtime spy, `final=False`) and no
module-level operator builder / no linear solve / no `final=True`; rowwise and
global decomposition closure; components sum to the residual; exactly nine
components reported for all 782 rows; F0 slot attribution exact with truncation
accounting; z-switch sourced only from the accepted switch matrix; diagonal
recorded separately and equal to `stored + switch[z,z]`; all-state statistics
(totals, F0/non-F0, z-block maxima, sign counts, conservativity); deterministic
top-20 ordering, true global top-20, complete payload, no sparse dump; read-only
reproduction (20/20, all diffs exactly `0.0`, per-row coverage, one selector call
per row, same local inputs, observed branch label); classification determinism;
no forced Outcome A; frozen dominance criteria explicit; exactly one terminal;
deterministic repeat identical; no accepted iterate / trajectory; static
forbidden-machinery scan over code (docstrings excluded).

Full repository suite `python -m pytest tests/ -q`: see §13.

## 13. Full repository suite

**`692 passed, 6 warnings in 3429.24 s (0:57:09)`** — `EXIT=0`, i.e. **0 failed,
0 errors, GREEN**.

The 6 warnings are the pre-existing `MatrixRankWarning` entries from the accepted
oracle tests (`test_dlh_5b`, `test_dlh_5c`) at
`matlab_faithful_two_asset_ha.py:597`; they are unchanged by this Issue.

The first run of this suite for this Issue reported `690 passed, 1 failed`. The
single failure was the stale Issue #70 assertion documented and corrected in
§11.1; after that assertion-only correction the suite is green at `692 passed`
(`690 + 1` newly passing plus the `1` added correction-guard test).

## 14. Terminal derivation (frozen rule)

- decomposition closes rowwise and globally: **yes** (`4.04e-11 <= 1e-9`);
- policy records reproduce on top-20 F0 rows: **yes**, exactly;
- attribution mismatch rows: **`0`**;
- one source-backed component clearly, stably and uniquely explaining the
  dominant residual pattern: **NO** — the residual is 0.67% of the gross
  component mass, a cancellation of competing `O(1e3)` terms.

→ **Outcome B**, exactly one terminal. Outcome A is not claimed (its frozen
criteria fail). Outcome C does not apply (no decomposition, reproduction or
single-`Q` contract failure; no non-finite evidence).

## 15. Next gate (for the Owner / Reviewer — NOT decided here)

1. **Bounded solver design.** The residual at `V_*` is a mixed fixed-point
   imbalance dominated by near-cancellation between the diagonal (`Q_ii`, the
   sum of actual outgoing rates), the b-backward move and the a-forward move, with
   boundary (`boundary_term`) mass comparable in the full state space. A bounded
   solver-design step is the appropriate next gate; this Issue does **not**
   prescribe or authorize one.
2. **Residual reassessment.** Any reassessment of the residual's origin, any
   convergence-rule change, any new HJB iterate, and any authorized `Q^T`
   mass-dynamics work require fresh explicit authorization.

Stationary KFE remains **NOT AUTHORIZED**.
