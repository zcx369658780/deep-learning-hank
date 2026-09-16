# DLH-5V-V — Route-A single-`Q` F0 operator-contract consolidation and final Bellman revalidation

**Issue:** #70 / DLH-5V-V
**Task type:** `OWNER_AUTHORIZED_SCIENTIFIC_CHANGE__MATLAB_FAITHFUL_SINGLE_Q_F0_OPERATOR_CONTRACT_CONSOLIDATION_AND_REVALIDATION`
**Route decision:** `APPROVE_ROUTE_A_MATLAB_FAITHFUL_SINGLE_Q_F0_OPERATOR_CONTRACT`
**Authority marker:** `DLH_5VV_ROUTE_A_SINGLE_Q_OPERATOR_CONTRACT_AUTHORIZED`
**Initial authoritative activation:** `5681294485`
**Final authoritative activation-refresh:** `5682174361`
**Reviewer hold (contract migration):** `5690304999`
**Reviewer final hold (policy-label identity):** `5691015137`
**Post-sync live `main`:** `0bca3b4552a76331302670bf59bddfa4cd4f06f7`
**Dedicated Builder branch:** `dsh/issue-70-dlh-5vv-route-a-single-q-operator-contract-2026-09-15`
**Date:** 2026-09-15

## TERMINAL (exactly one)

```
DLH_5VV_ROUTE_A_SINGLE_Q_OPERATOR_CONTRACT__FINAL_VALIDATION_REUSES_MATLAB_FAITHFUL_SELECTED_ITERATION_GENERATOR_AT_ALL_FROZEN_STATES__DUAL_RATE_GAP_REMOVED__HJB_RESIDUAL_REASSESSMENT_READY
```

**Outcome A.** At all three frozen states the Route-A final-validation operator
is **bit-identical** to the iteration operator, and the historical Issue #68
dual-rate gaps collapse to exactly `0.0`.

## 0. Owner authority implemented

The Owner explicitly selected **Route A** on 2026-09-15: MATLAB-faithful
iteration-rate semantics remain authoritative for the HJB operator. The binding
single-`Q` contract implemented here is:

1. the HJB solve uses the accepted MATLAB-faithful selected stored rates;
2. final Bellman validation uses the SAME selected stored rates / SAME backward
   generator `Q` semantics as the solve;
3. final validation does **not** recompute a second F0 generator from realized
   drift via `max(±mu)/step`;
4. future forward mass dynamics, once separately authorized, must use this same
   selected backward generator through `Q^T`;
5. dual-`Q` HJB/validation/KFE semantics are not authorized.

## 1. The minimal authorized source change

Only `src/deep_learning_hank/two_asset/boundary_hjb_selected_q.py` was mutated,
and only inside the F0 `final=True` validation assembly of
`build_operator_and_u`.

**Before** — the `final=True` F0 row rebuilt a *second* generator from raw drift:

```python
rec = f0_policies[row]
mu_a_v, mu_b_v, _ = asset_drifts_matlab_faithful(
    a_v, b_v, z_v, rec.consumption, np.array([rec.labor]), rec.transfer, ...)
ab = max(-mu_a_v, 0.0) / self.da
af = max(mu_a_v, 0.0) / self.da
bb = max(-mu_b_v, 0.0) / self.db
bf = max(mu_b_v, 0.0) / self.db
neigh = g.neighbors(j, i)
entries = []
for dn, rate in ((neigh["down"], bb), (neigh["up"], bf),
                 (neigh["left"], ab), (neigh["right"], af)):
    if dn is not None and rate != 0.0:
        entries.append((dn, float(rate)))
diag = -(bb + bf + ab + af)
```

**After** — the final-validation row reuses the SAME selected record:

```python
rec = f0_policies[row]
entries = [(int(dn), float(rate)) for dn, rate in rec.row_entries]
diag = float(rec.diagonal)
for dn, rate in entries:
    rows.append(row); cols.append(nz * self.n + dn); data.append(rate)
rows.append(row); cols.append(row); data.append(diag)
u[row] = rec.utility
```

and the associated metadata (`mu_a_arr` / `mu_b_arr` / `utility` / `sector_arr` /
`_PolicyRecord`) now carries `rec.mu_a`, `rec.mu_b`, `rec.utility` directly
rather than recomputed drifts.

Diff size: **17 insertions / 21 deletions**, one branch, no other line of the
file changed.

| Item | Value |
|---|---|
| pre-Issue-70 selected-Q blob | `556ccc214f03a1a22306cc4f5c7e9f7691bbf897` |
| post-Issue-70 selected-Q blob | `35e7dadfa4fb8f1c2a89db21751f2b541bda3cab` |
| oracle blob (unchanged) | `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e` |

Route-A properties realised: stored `row_entries` reused verbatim; stored
iteration-rate semantics reused; stored `diagonal` reused; stored `utility`
carried to `u`; same-z-block destination indexing preserved
(`cols.append(nz * self.n + dn)`); controls and realized `mu_a` / `mu_b` carried
as metadata only. `asset_drifts_matlab_faithful` is **no longer called** and the
`max(±mu)/step` mapping is **no longer present** anywhere in the assembly
(asserted by AST source tests).

### 1.1a Note on the now-unused import (conscious, not an oversight)

After the change, `asset_drifts_matlab_faithful` is no longer referenced in
`boundary_hjb_selected_q.py`; its import line (line 56) is therefore unused. It
was deliberately **left in place** because removing it would add a second,
non-behavioural hunk to the diff and is not required by the Authorized Change or
the frozen non-change boundary. It is dead-import-only and has no runtime effect.

### 1.1 Frozen non-change boundary (verified)

`select_matlab_faithful_local_policy`; `final=False` iteration semantics; the
accepted oracle; boundary families F1–F11; the switch matrix; grid/domain/state
variables; economics/prices/calibration; controls/policy selection;
initialization; tolerances; `PB_MARGIN`; Bellman tolerance; and the convergence
criterion were **not** altered. The `final=False` path still calls
`local_interior_row` exactly once.

## 2. Frozen-state reconstruction (reproduced exactly)

| Required | Required value | Reproduced |
|---|---|---|
| iterations | 8 | **8** |
| final statistic | `3.6614352438846254e-08` | **`3.6614352438846254e-08`** |
| min boundary `p_b` | `4.8089461301970005e-09` | **`4.8089461301970005e-09`** |
| wall | F3 (13,13), z=1 | **F3 (j=13, i=13, z=1), node 332** |
| S0 iteration residual | `10.435094313164921` | **`10.435094313164921`** |
| tangent identity `g @ d_T` | `0` | **`0.0`** |

Exactly three frozen states, no search and no alpha tuning:
**S0** = accepted Issue #63 `V_*`; **S1** = `alpha_half = 0.08085341880193442`;
**S2** = `alpha_near = 0.16170683760386884`, both reconstructed from the accepted
Issue #68 full-gradient tangent direction.

## 3. S0 / S1 / S2 single-`Q` identity (exactly one build pair per state)

| Quantity | S0 | S1 (`alpha_half`) | S2 (`alpha_near`) |
|---|---|---|---|
| F0 rowwise max `\|Q_final - Q_iter\|` | **`0.0`** | **`0.0`** | **`0.0`** |
| non-F0 rowwise max difference | **`0.0`** | **`0.0`** | **`0.0`** |
| global max difference | **`0.0`** | **`0.0`** | **`0.0`** |
| max `\|u_final - u_iter\|` | **`0.0`** | **`0.0`** | **`0.0`** |
| diagonal max difference | **`0.0`** | **`0.0`** | **`0.0`** |
| destination-set symmetric-difference rows | `0` | `0` | `0` |
| represented-rate mismatch rows | `0` | `0` | `0` |
| `max\|Q 1\|` iteration / final | `2.4253377084448857e-12` / `2.4253377084448857e-12` | same | same |
| controls max abs difference | **`0.0`** | **`0.0`** | **`0.0`** |
| **F0 policy/sector label mismatch rows** | **`0`** | **`0`** | **`0`** |
| all-row (F0 + non-F0) label mismatch rows | **`0`** | **`0`** | **`0`** |

Every operator, diagonal, destination, rate, utility **and policy-label** identity
is **exactly `0.0`** / zero rows, i.e. bit-identical rather than merely within
tolerance. `Q` conservativity is preserved and identical across both
constructions. No alternate F0 rate path exists after the change.

**Policy labels (frozen contract requirement — enforced under Reviewer final hold
`5691015137`).** The Route-A final-validation F0 row preserves the supplied
selected record's policy label VERBATIM:

```python
rec2 = _PolicyRecord(family="F0", sector=rec.sector, ...)
...
sector_arr[node, nz] = rec.sector
```

`sector_arr` therefore carries exactly the labels the solve selected (the observed
F0 label set is `{'0', 'B'}`), not an assembly tag. The frozen Issue #70
requirement — *selected controls **and** selected policy labels are unchanged by
final validation* — is now satisfied on **every** F0 row at S0, S1 and S2
(mismatch row count `0`), and it is checked by
`test_f0_policy_label_identity_all_rows` plus a source-level AST test that forbids
any string-literal `sector=` in the assembly. The intermediate revision
`0e3a959…` tagged these rows `INTERIOR_FINAL`; that tag is **removed**, and no
`INTERIOR_FINAL` token remains anywhere in the module.

This label-only change does not touch `row_entries`, `diagonal`, `utility`,
controls, realized drifts, `final=False` semantics, the oracle, F1–F11, the switch
matrix, economics/prices/grid/domain, initialization, tolerances, `PB_MARGIN`,
the Bellman tolerance or the convergence criterion. Concretely, the entire
remediation diff inside that branch is two value expressions (a `sector=`
keyword argument and a `sector_arr` assignment) plus an explanatory comment — the
generator, diagonal, utility, destination indexing and controls are byte-for-byte
the same code as revision `0e3a959…`, and the S0/S1/S2 identity table above
(including `R_final - R_iter` and the conservativity numbers) is unchanged by it.

## 4. Bellman residual identity

`R_iter = rho V - (u_iter + Q_iter V)`, `R_final = rho V - (u_final + Q_final V)`:

| Quantity | S0 | S1 | S2 |
|---|---|---|---|
| `\|\|R_iter\|\|inf` | **`10.435094313164921`** | `9.593278055493213` | `8.755529626006652` |
| `\|\|R_final\|\|inf` | **`10.435094313164921`** | `9.593278055493213` | `8.755529626006652` |
| `\|\|R_final - R_iter\|\|inf` | **`0.0`** | **`0.0`** | **`0.0`** |
| argmax state (both) | row 97, node 97, z=0, family F0 | same | same |

The final residual is now measured against the **same operator actually used by
the solve**.

## 5. Historical dual-rate gap collapse

| State | Historical Issue #68 gap | Route-A gap |
|---|---|---|
| S1 (`alpha_half`) | `0.6718037653783657` | **`0.0`** |
| S2 (`alpha_near`) | `1.3379411925537439` | **`0.0`** |

Both gaps collapse to machine precision — in fact to exactly zero — under the
Owner-authorized single-`Q` contract. The Issue #68/#69 dual-rate validation
inconsistency is removed by operator-contract consolidation, not by re-tuning any
rate.

### 5.1 A/B control proving the collapse is caused by this change

Rather than merely asserting collapse, the pre-Issue-70 module was loaded from
`origin/main` **outside the working tree** (read-only `git show` into a temp file,
imported under a separate module name) and used to build `final=True` on the
identical frozen states with the identical selected records:

| State | pre-change (dual-`Q`) gap | rows | post-change (Route A) gap |
|---|---|---|---|
| S1 | **`0.6718037653783657`** (exact match to the accepted Issue #68 value) | `[452, 453]` (exact match) | **`0.0`** |
| S2 | **`1.3379411925537439`** (exact match to the accepted Issue #68 value) | `[452, 453, 482, 483]` (exact match) | **`0.0`** |

The control reproduces the accepted Issue #68 magnitudes **and** row sets exactly,
so the collapse is unambiguously attributable to the Route-A consolidation
implemented here. The working tree was not mutated by the control.

### 5.2 Bounded post-Route-A contract migration (completed under Reviewer hold `5690304999`)

The first submission of this Issue disclosed — rather than worked around — a
governance/allowlist conflict: five dependent historical audit suites still
asserted the pre-Route-A dual-`Q` behaviour that Route A was authorized to
remove, so the repository suite was **not** green (22 failed / 13 errors), and
resolving it required touching paths outside the four-path allowlist.

The Reviewer withheld acceptance and authorized a **bounded post-Route-A
contract migration** with an exact **six-path** addition (hold `5690304999`).
The original Issue #70 commit `825e241804c7fb260c807602fc0f1487caf84e56` remains
the parent of this migration; the candidate reported here is its successor on
the same branch, with the Route-A scientific implementation untouched.

Migration branch used: **B — preserve and re-assert**. Every affected historical
expected value is retained as an explicitly labelled historical constant and the
tests are re-pointed at the true current runtime behaviour. Nothing was silently
replaced.

#### 5.2.1 The six added paths and their migration result

| Path | Migration |
|---|---|
| `tests/test_dlh_5vu_f0_rate_path_divergence.py` | **full re-migration** (see §5.2.2) |
| `tests/test_dlh_5vt_tangent_projected_newton_geometry.py` | historical Issue #68 trial gaps/rows and terminal C preserved as `HISTORICAL_*`; current trial gap `0.0`, current terminal = Issue #68 `TERMINAL_B` |
| `tests/test_dlh_5vr_f0_final_rate_provenance.py` | historical pre-Route-A F0 operator gap `1.4210854715202004e-14` preserved as `HISTORICAL_PRE_ROUTE_A_F0_OPERATOR_GAP`; current gap `0.0` |
| `tests/test_dlh_5vq_f0_final_validation_semantics_audit.py` | historical `d_rate_inf = 3.410605131648481e-13` and `q_current_minus_iter = 1.4210854715202004e-14` preserved as `HISTORICAL_PRE_ROUTE_A_*`; current values `0.0` |
| `tests/test_dlh_5vs_final_validation_zblock_repair.py` | pre-Route-A z-block repair evidence preserved as `PRE_ROUTE_A_FINAL_ZBLOCK_*` and re-verified read-only at the parent commit (`git show HEAD~1:…`) |
| `src/deep_learning_hank/two_asset/f0_final_rate_provenance_audit.py` | explicit **zero-gap** handling in `f0_component_comparison` (see §5.2.3) |

#### 5.2.2 The Issue #69 audit module is deliberately NOT modified

`src/deep_learning_hank/two_asset/f0_rate_path_divergence_audit.py` is **not** in
the authorized path set and was **not** touched. It remains byte-identical to its
accepted Issue #69 blob `83e9be0febcc03eb721265d3558887bd6b1586a4` (asserted by
`test_module_is_unmodified_by_route_a`).

Consequence, which is scientifically correct: the audit's frozen rule is that it
attests a divergence *mechanism* only when the accepted Issue #68 rowwise operator
gap and row set are **reproduced**. Route A removes that operator gap, so the
audit now legitimately **fails closed**:

| Field | Current value | Historical (accepted Issue #68/#69) |
|---|---|---|
| live terminal | `TERMINAL_C` (`…MIXED_OR_UNRESOLVED_SOURCE_PROVENANCE__OWNER_SCIENTIFIC_REVIEW_REQUIRED`) | `TERMINAL_A` (unique sign/branch mechanism established) |
| failure reason | `alpha_half: accepted Issue #68 gap/rows not reproduced (gap=0.0 vs 0.6718037653783657; rows=[] vs [452, 453])` | gap `0.6718037653783657`, rows `[452, 453]` |
| trials / mechanism flags | `0` / all un-established | 2 trials, full attribution |
| accepted iterate | `False` | `False` |

The module therefore reports the failure instead of attesting a mechanism from
non-reproducible data — the intended fail-closed behaviour, left as-is by design
("leave candidate science unchanged").

#### 5.2.3 Issue #66 audit module: explicit zero-gap handling

Under Route A the F0 rowwise gap is exactly `0.0`, so the accepted Issue #66 audit
never updated its gap-argmax row from the `-1` sentinel and then indexed a grid
corner where `neigh.get("up") is None`, previously raising
`TypeError: unsupported operand type(s) for +: 'int' and 'NoneType'` at line 491
(and cascading into 13 setup errors). `f0_component_comparison` now returns an
explicit, documented **zero-gap** result — `current_gap_zero=True`,
`current_gap_not_applicable=True`, `max_total_row_entry_diff=0.0`,
`max_total_row_entry_diff_state=None`, all component contributions `0.0`,
`max_row_columns_with_diff=0` — and `f0_rowwise_max_abs_gap_state` is guarded to
`None` when the argmax row is the `-1` sentinel. Verified: `run_issue66_audit()`
returns `failure_detail=None`, gap `0.0`, gap state `None`, and an identical
deterministic repeat. **No threshold, criterion or scientific quantity was
changed** — only the degenerate case that Route A makes reachable.

#### 5.2.4 Measured current behaviour, with the latent mechanism re-verified

The migration did not merely relax assertions: the latent stored-vs-raw b-rate
divergence that Issue #69 attributed is **independently re-measured** from the
current accepted sources. It persists with unchanged magnitudes, while the
operator gap it used to cause is gone:

| Quantity | `alpha_half` (S1) | `alpha_near` (S2) | Historical |
|---|---|---|---|
| b-rate-divergent F0 rows | `[452, 453]` | `[452, 453, 482, 483]` | **identical** |
| max stored-vs-raw b-rate difference | `0.3359018826891829` | `0.6689705962768726` | **identical** |
| rows carrying an opposing-direction component | `2` | `4` | **identical** |
| liquid branch / realized drift on those rows | `liquid_label='F'`, `mu_b < 0` | same | same |
| **operator** rowwise gap | **`0.0`** | **`0.0`** | `0.6718…` / `1.3379…` |
| a-axis rate difference, net active b-direction | `0.0`, agrees | `0.0`, agrees | agrees |

Two measurement facts are recorded in the migrated suite because they correct the
historical Issue #69 prose, and the assertions follow the measurement:

* the iteration and raw paths agree exactly on the **net** active b-direction and
  on the a-axis; the divergence is confined to the per-side stored rate values
  (the iteration stores a positive b-forward rate of `0.335901883` / `0.668971`
  where the raw path stores exactly `0.0`, with a correspondingly inflated
  b-backward rate);
* the divergence is therefore invisible to the net upwind direction and is
  removed from the operator only because Route A reuses the stored record
  verbatim — which is exactly why it no longer reaches `Q`.

#### 5.2.5 An unauthorized change was attempted and reverted (disclosed)

While re-migrating, a remediation of `f0_rate_path_divergence_audit.py` (an
"all()-over-zero-rows" classification guard) was briefly drafted. It is **not**
in the authorized path set, so it was **reverted** with `git checkout --` and the
working tree was restored to the accepted blob
`83e9be0febcc03eb721265d3558887bd6b1586a4`. This is disclosed here rather than
omitted: the committed candidate contains **no** change to that module, and the
final candidate diff is exactly the authorized ten paths.

### 5.3 Final bounded remediation — policy-label preservation (Reviewer final hold `5691015137`)

The Reviewer reviewed candidate `0e3a959…` and confirmed the migration was
otherwise well-formed (base/merge-base `0bca3b4…`, exactly ten authorized paths,
Route-A blob unchanged, Issue #66 zero-gap handling explicit, historical evidence
separated from current assertions, suites green) but withheld acceptance on ONE
remaining contract point: the frozen Issue #70 §6 / activation `5682174361`
requirement is that **selected controls AND selected policy labels are unchanged
by final validation**, and the `final=True` F0 branch was still building
`_PolicyRecord(sector="INTERIOR_FINAL", …)` and writing
`sector_arr[node, nz] = "INTERIOR_FINAL"`. The generator, `u`, controls and drifts
were identical, but the *policy-label* half of the frozen contract was not met.
The Reviewer was explicit that the previous report's own disclosure — "all 596 F0
sector labels differ" — could not be accepted as a mere assembly tag.

**Remediation (one commit, `boundary_hjb_selected_q.py` only).** The entire
inside-branch diff is two value expressions plus an explanatory comment:

```python
# before (revision 0e3a959…)
rec2 = _PolicyRecord(family="F0", sector="INTERIOR_FINAL", ...)
sector_arr[node, nz] = "INTERIOR_FINAL"
# after
rec2 = _PolicyRecord(family="F0", sector=rec.sector, ...)
sector_arr[node, nz] = rec.sector
```

`row_entries`, `diagonal`, `utility`, consumption, labor, transfer, `mu_a`,
`mu_b`, `final=False` semantics, policy selection, the oracle, F1–F11, the switch
matrix, economics/prices/grid/domain, initialization, tolerances, `PB_MARGIN`, the
Bellman tolerance and the convergence criterion are **untouched**; no
`INTERIOR_FINAL` token remains anywhere in the module.

**Verified result at the frozen states** (`label mismatch row count = 0`
required):

| Quantity | S0 | S1 | S2 |
|---|---|---|---|
| F0 policy/sector label mismatch rows | **`0`** | **`0`** | **`0`** |
| all-row (F0 + non-F0) label mismatch rows | **`0`** | **`0`** | **`0`** |
| observed F0 label set (iteration == final) | `{'0', 'B'}` | `{'0', 'B'}` | `{'0', 'B'}` |
| `Q_final == Q_iter` (max abs) | **`0.0`** | **`0.0`** | **`0.0`** |
| `u_final == u_iter` (max abs) | **`0.0`** | **`0.0`** | **`0.0`** |
| controls / `mu` metadata max abs diff | **`0.0`** | **`0.0`** | **`0.0`** |
| diagonal max diff / destination sym-diff rows | `0.0` / `0` | `0.0` / `0` | `0.0` / `0` |
| represented-rate mismatch rows | `0` | `0` | `0` |
| residual vector max abs diff | **`0.0`** | **`0.0`** | **`0.0`** |
| `\|\|R_iter\|\|inf` (unchanged by this fix) | `10.435094313164921` | `9.593278055493213` | `8.755529626006652` |

Because the change is label-only, every identity and residual number above is
identical to revision `0e3a959…`. New tests lock the contract: a runtime all-F0
label-identity check at S0/S1/S2, an aggregate mismatch-count check, and a
source-level AST test asserting that `_PolicyRecord(... sector=rec.sector ...)`
and `sector_arr[node, nz] = rec.sector` are present, that `sector=` is never a
string literal in the assembly, and that `INTERIOR_FINAL` does not exist.

Historical anchors were also made **revision-independent** (absolute SHAs instead
of moving `HEAD~n`) so that adding this commit could not shift the pre-Route-A
evidence: `825e241…^` for the pre-Route-A source, `825e241…` for the original
scientific commit and `0e3a959…` for the migration commit. Historical Issue
#65/#66/#67/#68/#69 evidence is preserved unchanged; current Route-A S1/S2 gaps
remain `0.0` while the historical gaps remain `0.6718037653783657` /
`1.3379411925537439`, distinctly labelled.

## 6. Interpretation ceiling — HJB convergence remains FALSE

Passing this Issue means only that:

- one coherent MATLAB-faithful F0 generator now governs solve and final
  validation;
- the Issue #68/69 dual-rate validation inconsistency is removed by
  Owner-authorized operator-contract consolidation;
- the final Bellman residual is now measured against the same operator actually
  used by the solve.

It does **NOT** mean:

- HJB convergence — the S0 final residual is still **`10.435094313164921`**,
  i.e. `10435.09`× the **unchanged** Bellman tolerance `1e-3`, so S0 remains
  **NOT converged**;
- acceptance of any new HJB iterate (none exists; no new trajectory was run);
- permission to change the Bellman tolerance or the convergence criterion;
- permission to run KFE / stationary KFE;
- proof that the fixed point exists globally.

Single-`Q` consistency must not be read as convergence.

## 7. Deterministic repeat

The full three-state validation was repeated from a fresh independent
reconstruction; the tangent direction, both operators, both `u` vectors and all
identity data are bit-identical (`deterministic_repeat_identical = True`).

## 8. Tests

Focused suite `tests/test_dlh_5vv_route_a_single_q_operator_contract.py`:
**42 passed**.

Coverage: Owner Route-A authority marker present in the implementation; the
pre-Issue-70 selected-Q blob recorded as
`556ccc214f03a1a22306cc4f5c7e9f7691bbf897` and the oracle blob unchanged at
`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`; the `final=True` F0 branch no longer
constructs a raw-drift `Q` (AST: no `asset_drifts_matlab_faithful` call and no
`max(±mu)/step` token in the assembly); the branch reuses the supplied selected
row, diagonal and utility and keeps same-z indexing; `final=False` still calls
`local_interior_row` exactly once; exact S0 reconstruction; exact S1/S2
fractions; exactly three frozen states; exactly one `final=False` and one Route-A
`final=True` build per state (runtime spy: 4 iteration + 3 Route-A builds);
S0/S1/S2 F0, non-F0, global `Q` identity; `u` identity; diagonal and destination
identity; represented-rate identity per row; controls unchanged with documented
label retagging; `Q` conservativity; historical S1/S2 gap collapse; Bellman
residual identity and argmax identity; S0 residual unchanged and not converged;
no tolerance/convergence-rule change; no accepted iterate; deterministic repeat
identical; static scan for forbidden machinery.

Full repository suite `python -m pytest tests/ -q`:

**`641 passed, 6 warnings in 3402.38 s (0:56:42)`** — `EXIT=0`, i.e. **0 failed,
0 errors, GREEN**.

The 6 warnings are the pre-existing `MatrixRankWarning` entries from the accepted
oracle tests (`test_dlh_5b`, `test_dlh_5c`) at
`matlab_faithful_two_asset_ha.py:597`; they are unchanged by this Issue.

Consequence for the completion contract: Issue #70 §10/§13 requires the full
suite to pass while the original §9 allowlist permitted only four tracked paths.
Those two requirements could not both hold once the mandated Route-A semantics
change was applied. The first submission disclosed that conflict (§5.2 of the
previous revision) rather than widening the allowlist unilaterally; the Reviewer
then authorized the bounded six-path addition, and after the migration both
requirements hold simultaneously: the suite is green **and** the cumulative diff
is exactly the ten authorized paths (§9).

### 8.1 Migrated-suite results (six added paths)

| Suite | Result | Historical evidence preserved as |
|---|---|---|
| `tests/test_dlh_5vu_f0_rate_path_divergence.py` | **24 passed** | `PRE_ROUTE_A_SELECTED_Q_BLOB`, `HISTORICAL_ISSUE68_GAP_HALF/NEAR`, `HISTORICAL_ISSUE68_ROWS_HALF/NEAR`, `HISTORICAL_ISSUE68_B_RATE_DIFF_HALF/NEAR`, `HISTORICAL_ISSUE68_ROW_COUNTS`, `HISTORICAL_ISSUE69_TERMINAL_A`, `PRE_ROUTE_A_SELECTED_Q_COMMIT` |
| `tests/test_dlh_5vt_tangent_projected_newton_geometry.py` | **40 passed** | `HISTORICAL_ISSUE68_TRIAL_GAP_HALF/NEAR`, `HISTORICAL_ISSUE68_TRIAL_ROWS_HALF/NEAR`, `HISTORICAL_ISSUE68_TERMINAL_C` |
| `tests/test_dlh_5vr_f0_final_rate_provenance.py` | **18 passed** | `HISTORICAL_PRE_ROUTE_A_F0_OPERATOR_GAP = 1.4210854715202004e-14` |
| `tests/test_dlh_5vq_f0_final_validation_semantics_audit.py` | **15 passed** | `HISTORICAL_PRE_ROUTE_A_D_RATE_INF = 3.410605131648481e-13`, `HISTORICAL_PRE_ROUTE_A_Q_CURRENT_MINUS_ITER = 1.4210854715202004e-14` |
| `tests/test_dlh_5vs_final_validation_zblock_repair.py` | **21 passed** | `PRE_ROUTE_A_FINAL_ZBLOCK_*` plus a dedicated preservation test reading the parent commit read-only at the absolute revision `825e241…^` |
| `src/deep_learning_hank/two_asset/f0_final_rate_provenance_audit.py` | exercised by the above | — (authorized zero-gap handling only, §5.2.3) |

Combined six-target focused run: **160 passed in 77.67 s**.
Issue #70 focused suite alone: **42 passed** (`test_dlh_5vv_route_a_single_q_operator_contract.py`).

Per-file focused counts after the final remediation: `test_dlh_5vv…` 42,
`test_dlh_5vt…` 40, `test_dlh_5vu…` 24, `test_dlh_5vs…` 21, `test_dlh_5vr…` 18,
`test_dlh_5vq…` 15 — total **160**, `0 failed`.

Every historical expected value is retained as an explicitly named historical
constant and asserted as history. Nothing was silently replaced, and no
historical number is asserted as a current runtime expectation:
`490.756…` / `24.6019…` / `0.6718037653783657` / `1.3379411925537439` appear only
in historical-labelled constants and in the fail-closed Issue #69 message that
quotes them as the unreproducible baseline. The current Route-A expectations
(`0.0` gaps, `TERMINAL_B` for the Issue #68 suite, `f0_rowwise_max_abs_gap_state
is None`) are asserted separately.

## 9. Authorized files (exact ten-path cumulative diff)

Issue #70 original four-path allowlist:

1. `src/deep_learning_hank/two_asset/boundary_hjb_selected_q.py`
2. `tests/test_dlh_5vv_route_a_single_q_operator_contract.py`
3. `reports/dlh_5vv_route_a_single_q_operator_contract_2026_09_15/DLH_5VV_ROUTE_A_SINGLE_Q_OPERATOR_CONTRACT_REPORT.md`
4. `reports/dlh_5vv_route_a_single_q_operator_contract_2026_09_15/DLH_5VV_ROUTE_A_SINGLE_Q_OPERATOR_CONTRACT_SUMMARY.csv`

Reviewer hold `5690304999` adds exactly these six existing paths:

5. `tests/test_dlh_5vu_f0_rate_path_divergence.py`
6. `tests/test_dlh_5vt_tangent_projected_newton_geometry.py`
7. `tests/test_dlh_5vr_f0_final_rate_provenance.py`
8. `tests/test_dlh_5vq_f0_final_validation_semantics_audit.py`
9. `tests/test_dlh_5vs_final_validation_zblock_repair.py`
10. `src/deep_learning_hank/two_asset/f0_final_rate_provenance_audit.py`

`git diff --name-only origin/main...HEAD` returns **exactly these ten paths**, and
is asserted during the completion evidence run. No eleventh path. No accepted
source outside the single authorized F0 `final=True` assembly and the Issue #66
zero-gap handling above was modified; the oracle and all accepted Issue #61–#69
blobs are byte-identical to their accepted values.

### 9.1 Frozen scientific implementation (unchanged by this migration)

The Route-A F0 `final=True` assembly is byte-identical to the originally
submitted candidate: the selected-Q blob remains
`35e7dadfa4fb8f1c2a89db21751f2b541bda3cab` and the unchanged oracle blob remains
`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`. The migration changes **test
contracts and one explicitly authorized audit module only**; no Route-A
scientific quantity, threshold or criterion was altered.

## 10. Terminal derivation (frozen rule)

- Route-A F0 `final=True` consolidation implemented: **yes**, one branch only;
- `Q_final == Q_iter` and `u_final == u_iter` at **all three** frozen states:
  **yes**, exactly `0.0`;
- historical S1/S2 gaps collapsed to machine precision: **yes**, exactly `0.0`
  (with A/B control proof in §5.1);
- non-F0 identity, diagonal identity, destination/rate identity, controls
  identity, conservativity: **yes**;
- evidence finite and consistent: **yes**;
- deterministic repeat identical: **yes**.

→ **Outcome A**, exactly one terminal. Outcome B does not apply (no material
final-vs-iteration discrepancy remains: it is exactly zero). Outcome C does not
apply (no nonfinite evidence, no regression in the Route-A implementation, and no
contract failure).

The §5.2 migration does **not** change this derivation. In particular it does not
re-open Outcome B and does not introduce a discrepancy: the failing Issue #69
audit is a *read-only diagnostic* whose frozen rule refuses to attest a mechanism
from data that no longer contains the accepted gap, and the migrated suite
asserts that refusal plus the preserved historical evidence. The latent
stored-vs-raw rate-object divergence is unchanged in magnitude and remains
disclosed (§5.2.4) — it is simply no longer reachable by the operator.

## 11. Next gate (for the Owner / reviewer — NOT decided here)

Two separate matters:

1. **Contract migration (§5.2) and final policy-label remediation (§5.3) —
   CLOSED.** The bounded post-Route-A migration authorized by Reviewer hold
   `5690304999` is complete (six added paths, every historical expected value
   preserved as an explicitly labelled historical constant, the Issue #69 audit
   module deliberately untouched and asserted byte-identical, the Issue #66
   module's degenerate zero-gap case handled explicitly). The policy-label
   contract point raised by Reviewer final hold `5691015137` is also closed:
   selected policy labels are now preserved verbatim on every F0 row
   (`mismatch row count = 0` at S0/S1/S2). The repository suite is green and the
   cumulative diff remains exactly the ten authorized paths.
2. **Residual reassessment.** The solve and final validation now share one
   coherent selected generator, so the final Bellman residual at `V_*`
   (`10.435094313164921`) is the genuine single-operator residual. It remains
   ~`10435`× the unchanged Bellman tolerance `1e-3`, so **validated HJB
   convergence is still FALSE**. Any reassessment of the residual's origin, any
   convergence-rule change, any new HJB iterate, and any authorized `Q^T`
   mass-dynamics work require fresh explicit authorization.

Stationary KFE remains **NOT AUTHORIZED**.
