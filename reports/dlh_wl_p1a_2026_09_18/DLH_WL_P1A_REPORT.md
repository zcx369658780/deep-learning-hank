# DLH-WL-P1A — Frozen-household evidence registry + offline conditional labor-destination accounting

Issue: **#74 / `DLH-WL-P1A`** — OPEN / ACTIVE / OPERATIVE.
Owner route: **`DLH-WL-V1-20260918`**.
Authority marker: `DLH_WL_P1A_OFFLINE_ACCOUNTING_AND_HOUSEHOLD_REGISTRY_AUTHORIZED`.
Final Reviewer activation comment: **`5730955781`** (2026-09-18T13:50:32Z).
Operative baseline (activation-named live `main`): **`e046feccf9f98adad0d7db713eca427e0e7f1e36`**.
Dedicated Builder branch: **`dsh/issue-74-dlh-wl-p1a-offline-labor-destination-2026-09-18`**.

Reading this file is not an economic result. It records a bounded offline
accounting interface plus a read-only evidence registry. **No model was trained,
no
household/HJB/KFE/GE code was executed, and no empirical identification is
claimed.**

---

## 1. Scope, ceilings and declared budgets

Authorized and executed (exactly the Issue #74 allowlist):

1. existing household-dependency evidence registry (read-only);
2. standalone offline conditional labor-destination accounting interface;
3. deterministic asymmetric tiny tests plus focused/static checks.

Binding ceilings, all respected:

| Ceiling | Budget | Actual |
|---|---|---|
| HJB calls | 0 | **0** |
| KFE / stationary KFE calls | 0 | **0** |
| GE / outer fixed-point calls | 0 | **0** |
| MATLAB calls | 0 | **0** |
| neural training runs | 0 | **0** |
| data / weight downloads | 0 | **0** |
| repository-wide (full) suite | NOT AUTHORIZED | **not run** |
| expensive scientific/model calls | 0 | **0** |
| pytest invocations | focused test file only | **focused file only** |

Not done by design: no neural architecture, no optimizer, no dataset loader, no
HJB adapter, no GE adapter, no empirical-label bridge, no P2/P3/P4/P5 entry, no
successor Issue, no PR/merge/close, no self-acceptance.

---

## 2. Exact changed paths

Exactly the four Issue-authorized paths; no CURRENT roadmap/rule/decision/contract
was touched, and no historical scientific result was modified.

| # | Path | Status | LOC |
|---|---|---|---|
| 1 | `src/deep_learning_hank/regional/labor_destination.py` | created | 445 |
| 2 | `tests/test_dlh_wl_p1a_labor_destination.py` | created | 782 |
| 3 | `reports/dlh_wl_p1a_2026_09_18/DLH_WL_P1A_REPORT.md` | created (this file) | 265 |
| 4 | `reports/dlh_wl_p1a_2026_09_18/DLH_WL_P1A_HOUSEHOLD_DEPENDENCY_REGISTRY.md` | created | 182 |

`git status --porcelain` on the dedicated branch shows only these four entries
(plus this report directory). No other tracked file differs from the operative
baseline.

---

## 3. Implemented accounting interface

`build_labor_destination_accounting(m, ell, W, *, support_mask=None,
destination_wages=None, contract_version=..., units=None) ->
LaborDestinationAccounting`

Inputs (all given; **none of them is a learning target in this Issue**):

- `m` — origin labor-outflow shares, shape `(n,)`, values in `[0, 1]`;
- `ell` — origin labor totals, shape `(n,)`, non-negative; the caller declares
  the unit through `units` (population counts are never silently treated as
  efficiency labor);
- `W` — conditional foreign destination shares, shape `(n, n)`, indexed
  `[origin, destination]`, zero diagonal, non-negative, allocation-required rows
  (`m_i > 0`) summing to `1` over allowed foreign destinations;
- `support_mask` — optional boolean `(n, n)` structural availability; `True`
  means destination `j` is structurally available to origin `i`. Defaults to
  "every foreign destination available, own region unavailable";
- `destination_wages` — optional given destination wage vector.

Computed identities (all implemented exactly as contracted):

- `P_ii = 1 - m_i`, `P_ij = m_i * W_ij` for `j != i`;
- `F_ij = ell_i * P_ij` — the **full bilateral flow matrix** is always returned;
- `Ldest_j = sum_i F_ij`;
- `wbar_i = sum_j P_ij w_j` and the wage-bill identity
  `sum_i ell_i wbar_i == sum_j Ldest_j w_j` when wages are supplied.

Returned object (never a bare array): echoed inputs, `P`, `F`,
`destination_labor`, `destination_wage_bill`, `wbar`, `total_labor`,
`support_mask`, `active_row_mask`, `valid_row_mask`,
`rows_without_identifiable_target`, `rows_without_foreign_option`,
`conditional_choice_identified`, provenance strings and a diagnostics mapping.

`P` and `F` are built element by element on purpose. During development a
broadcasting form (`np.eye(n) * (1 - m)[:, None]`) silently scaled the whole
matrix by one scalar; the explicit construction removes that class of
orientation/broadcasting error entirely.

### Fail-closed error reasons

`LaborDestinationAccountingError(reason, message)` (a `ValueError` subclass)
carries one deterministic prefix:

| reason | triggered by |
|---|---|
| `DIMENSION_MISMATCH` | non-1-D `m`/`ell`, non-square or wrong-shaped `W`, `m`/`ell`/wage/support shape mismatch, empty `m` |
| `NON_FINITE` | NaN/inf in `m`, `ell`, `W`, wages or support |
| `NEGATIVE_MASS` | negative `ell` or negative `W` entry |
| `RANGE` | `m` outside `[0, 1]` |
| `ILLEGAL_DIAGONAL` | non-zero `W_ii` |
| `ROW_SUM` | allocation-required row with zero conditional mass, or row sum != 1 over allowed foreign destinations |
| `IMPOSSIBLE_SUPPORT` | support with self available, non-0/1 support encoding, mass on a structurally unavailable destination, or an allocating row with no available destination |
| `SINGLE_REGION_OUTFLOW` | single region with `m > 0` |
| `INCONSISTENT_INPUT` | unreadable array or invalid support encoding |

### Scope guards implemented in code

- **no fabricated supervision labels**: rows with `m_i = 0`, `ell_i = 0` or no
  available foreign option are reported through
  `rows_without_identifiable_target` / `rows_without_foreign_option`; their given
  `W` row is echoed unchanged and is never rewritten into a uniform target;
- **structural vs realised zero**: `support_mask` marks structural
  unavailability; blocked destinations must carry zero conditional mass, while an
  ordinary realised zero flow is not treated as structural impossibility;
- **single region** is accepted only in the `m = 0`, `P = [[1]]` accounting
  limit; `m > 0` fails closed;
- **two regions** are accounting-only for conditional-choice learning because the
  foreign destination is unique there — reported via
  `conditional_choice_identified = False` (non-degenerate learning would need at
  least three regions, and **training is not authorized here**);
- **standalone**: the module imports only `__future__`, `dataclasses`, `typing`
  and `numpy`, contains no dynamic import/eval/exec/compile/`open` call, and
  references no household/HJB/KFE/GE entry point.

---

## 4. Focused checks and results

Command actually used (focused file only, from the dedicated worktree):

```
PYTHONPATH=<worktree>/src python -B -m pytest tests/test_dlh_wl_p1a_labor_destination.py -p no:cacheprovider -q
```

Result: **43 passed** (deterministic; no random seed used, no fixture reuses a
solver).

Coverage mapped onto the Issue-required list:

| Issue #74 §5 requirement | tests |
|---|---|
| 1. asymmetric 3-region case, unequal `m`/`ell` | `test_asymmetric_three_region_accounting_matches_closed_form`, `test_orientation_and_scope_metadata_are_recorded` |
| — orientation guard (transposed reading) | `test_rectangular_case_is_rejected_and_orientation_is_asymmetric` |
| 2. exact origin and national conservation | `test_origin_and_national_conservation_are_exact`, `test_home_and_foreign_mass_decompose_per_origin` |
| 3. destination aggregation | `test_destination_aggregation_equals_column_sums` |
| 4. zero diagonal / non-negativity / required-row normalization | `test_zero_diagonal_non_negativity_and_required_row_normalization` |
| 5. wage-bill identity with unequal wages | `test_wage_bill_identity_closes_with_unequal_wages`, `test_wage_outputs_absent_when_no_wages_supplied` |
| 6. region-permutation equivariance | `test_region_permutation_equivariance` |
| 7. two-region accounting degeneration | `test_two_region_case_is_accounting_only` |
| 8. single-region `m = 0` limit and fail-closed `m > 0` | `test_single_region_m_zero_is_the_accounting_limit`, `test_single_region_outflow_fails_closed` |
| 9. `m = 0` row without fabricated supervision target | `test_m_zero_row_has_no_fabricated_supervision_target`, `test_row_without_foreign_option_is_distinct_from_row_without_labor`, `test_two_region_row_without_foreign_option`, `test_m_zero_row_without_foreign_option_is_reported_not_refused` |
| 10. `m = 1` case | `test_m_one_sends_all_labor_abroad`, `test_m_one_without_any_foreign_option_fails_closed` |
| 11. zero `ell` case | `test_zero_ell_row_produces_zero_flows_and_no_label` |
| 12. structural support mask | `test_structural_support_mask_blocks_unavailable_destination`, `test_support_mask_rejects_mass_on_unavailable_destination`, `test_support_mask_diagonal_must_be_unavailable`, `test_support_mask_shape_and_encoding_fail_closed` |
| 13. invalid / non-finite / negative / dimension mismatch | `test_dimension_mismatch_fails_closed`, `test_matrix_shape_mismatch_fails_closed`, `test_non_1d_input_fails_closed`, `test_m_out_of_range_fails_closed`, `test_negative_ell_fails_closed`, `test_negative_share_fails_closed`, `test_non_finite_input_fails_closed`, `test_illegal_diagonal_fails_closed`, `test_invalid_row_sum_fails_closed`, `test_zero_conditional_mass_on_required_row_fails_closed`, `test_unsupported_destination_without_mass_fails_closed`, `test_wage_vector_dimension_mismatch_fails_closed`, `test_wage_vector_non_finite_fails_closed`, `test_error_messages_carry_reason_prefix` |
| 14. import/static guard, no household/HJB/KFE/GE execution | `test_module_imports_only_offline_safe_names`, `test_module_has_no_dynamic_import_or_file_access_calls`, `test_test_file_does_not_import_forbidden_scientific_modules`, `test_module_never_references_household_or_solver_entrypoints`, `test_subprocess_import_loads_no_household_hjb_kfe_or_ge_modules`, `test_allowlist_paths_and_untouched_scientific_modules` |

Additional static checks run in this Issue (no scientific execution):

- `python -B -m py_compile` on both new Python files — exit 0;
- an AST dead-name scan of the new module — no unused module-level definition
  remains (`_column` was removed after this scan flagged it);
- `git status --porcelain` scope check — only the four authorized paths.

### Orientation and conservation diagnostics (fixture values)

Three-region fixture: `m = (0.25, 0.4, 0.0)`, `ell = (100, 60, 40)`,
`W = [[0, 0.75, 0.25], [0.5, 0, 0.5], [0.5, 0.5, 0]]`.

```
P        = [[0.75, 0.1875, 0.0625], [0.2, 0.6, 0.2], [0.0, 0.0, 1.0]]
F        = [[75.0, 18.75, 6.25], [12.0, 36.0, 12.0], [0.0, 0.0, 40.0]]
Ldest    = [87.0, 54.75, 58.25]        total = 200.0
wbar     = [2.375, 3.2, 5.0]           wage bill = 629.5 (left == right)
```

- origin conservation `F.sum(axis=1) == ell`: max abs deviation exactly `0.0`;
- national conservation `F.sum() == sum(ell)`: max abs deviation exactly `0.0`;
- destination aggregation: max abs deviation exactly `0.0`;
- own-region diagonal `F_ii == (1 - m_i) * ell_i`: max abs deviation `0.0`;
- orientation: the fixture has `W != W.T` and `W.sum(axis=0) != W.sum(axis=1)`; a
  rectangular `W` and its transpose are both rejected with `DIMENSION_MISMATCH`;
  a valid row-normalized transposed reading gives different `F`, `P` and
  destination totals, so a transposed orientation cannot pass accidentally;
- `m = 0` row: `P` row `[0, 0, 1]`, `F` row `[0, 0, 40]`, flagged through
  `rows_without_identifiable_target`.

---

## 5. Explicit zero-call evidence

Per the activation comment, the counts that must be zero are reported as
observed in this Issue:

```
HJB calls                        = 0
KFE / stationary KFE calls       = 0
GE / outer fixed-point calls     = 0
MATLAB calls                     = 0
neural training runs             = 0
data / weight downloads          = 0
expensive scientific/model calls = 0
full repository suite runs       = 0 (not authorized)
```

The only executed code paths were: the new offline pure-algebra module, the new
focused test file, `py_compile`/AST static checks and `git` metadata commands.
The subprocess import guard proves that importing the new module loads neither
any `deep_learning_hank.two_asset` module nor `scipy`/`torch`/`tensorflow`/
`matlab`/`matlabengine`.

---

## 6. Known limitations and boundary of interpretation

- `W` is treated as a **given input object** for the first version. Nothing here
  learns `W`, `m`, `ell`, capital networks, local parameters or an end-to-end
  model; training remains authorized only by a later explicit Issue.
- The interface is offline accounting only. It is not an equilibrium object, not
  a household solution, and not a stationary distribution.
- `support_mask` semantics: an unavailable destination is a **structural zero**
  and must therefore already carry zero conditional mass. A realised zero flow is
  *not* structural unavailability; masking an observed zero would change the
  experimental support set and is a design decision for a later Issue.
- Row sums are validated with tolerance `1e-12` (relative and absolute).
  A `W` row for `m_i = 0` is not required to be normalized, but if non-zero it
  must still be a valid non-negative row; the interface never fabricates a
  uniform target for such rows.
- `rows_without_foreign_option` currently means "no structurally available
  foreign destination at all"; a row whose given `W` row is an all-zero row while
  `m_i > 0` is refused earlier as `ROW_SUM` (malformed conditional matrix).
- No empirical bilateral OD label set is claimed or used. Two-region cases are
  accounting-only; non-degenerate conditional-choice learning would require at
  least three regions and is not authorized here.
- No economic coupling, no HJB/KFE/GE consistency claim, and no policy or welfare
  interpretation is offered. Error accounting remains split: this report contains
  **no** HJB residual, KFE, or GE error statement because none was computed.
- The household registry (`DLH_WL_P1A_HOUSEHOLD_DEPENDENCY_REGISTRY.md`) records
  only existing repository evidence; fields not supported by existing evidence
  are marked `NOT_VERIFIED`. It adds no new solved-checkpoint claim.

---

## 7. Terminal

```
DLH_WL_P1A_OFFLINE_ACCOUNTING_INTERFACE_AND_HOUSEHOLD_REGISTRY__PASS
```

One terminal only. No PR, merge, close, successor Issue or self-acceptance was
performed. Independent Reviewer verification is required.
