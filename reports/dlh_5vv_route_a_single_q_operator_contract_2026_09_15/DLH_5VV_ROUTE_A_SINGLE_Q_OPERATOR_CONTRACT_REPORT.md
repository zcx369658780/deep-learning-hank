# DLH-5V-V — Route-A single-`Q` F0 operator-contract consolidation and final Bellman revalidation

**Issue:** #70 / DLH-5V-V
**Task type:** `OWNER_AUTHORIZED_SCIENTIFIC_CHANGE__MATLAB_FAITHFUL_SINGLE_Q_F0_OPERATOR_CONTRACT_CONSOLIDATION_AND_REVALIDATION`
**Route decision:** `APPROVE_ROUTE_A_MATLAB_FAITHFUL_SINGLE_Q_F0_OPERATOR_CONTRACT`
**Authority marker:** `DLH_5VV_ROUTE_A_SINGLE_Q_OPERATOR_CONTRACT_AUTHORIZED`
**Initial authoritative activation:** `5681294485`
**Final authoritative activation-refresh:** `5682174361`
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

Every operator, diagonal, destination, rate and utility identity is **exactly
`0.0`**, i.e. bit-identical rather than merely within tolerance. `Q`
conservativity is preserved and identical across both constructions. No alternate
F0 rate path exists after the change.

**Policy labels.** The Route-A final-validation record is intentionally tagged
`INTERIOR_FINAL` (it records which assembly path produced the row), so all `596`
F0 sector labels differ from the iteration record's label. The mandate's
"controls unchanged" concerns the selected controls and realized drifts, which
are bit-identical (`controls_max_abs_diff = 0.0`); this is documented rather than
suppressed.

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

### 5.2 Dependent-suite consequence (DISCLOSED, not worked around)

Five historical audit test files assert the **pre-Route-A dual-`Q` behaviour**
that this Issue was authorized to remove, and therefore fail:

| File (outside the Issue #70 allowlist) | failed | errors |
|---|---|---|
| `tests/test_dlh_5vu_f0_rate_path_divergence.py` | 13 | 0 |
| `tests/test_dlh_5vt_tangent_projected_newton_geometry.py` | 5 | 0 |
| `tests/test_dlh_5vr_f0_final_rate_provenance.py` | 1 | 13 |
| `tests/test_dlh_5vq_f0_final_validation_semantics_audit.py` | 2 | 0 |
| `tests/test_dlh_5vs_final_validation_zblock_repair.py` | 1 | 0 |

Cause, precisely: under Route A the F0 rowwise operator gap is **exactly `0.0`**,
so the Issue #66 audit module `f0_final_rate_provenance_audit.py` never updates
its gap-argmax row from the `-1` sentinel and then indexes a grid corner where
`neigh.get("up") is None`, raising
`TypeError: unsupported operand type(s) for +: 'int' and 'NoneType'` (line 491);
its 13 setup errors cascade from that. The remaining failures are straightforward
stale assertions (the S1/S2 gaps are no longer `0.6718…` / `1.3379…`, and the
trial operators are now equivalent so the Issue #68 / #69 terminals change).

This is a **governance/allowlist conflict, not a defect in the Route-A
implementation**: Issue #70 requires the full suite to pass (§10/§13) while
allowing only four tracked paths (§9), none of which is a dependent test file.
The conflict is reported rather than worked around, and **no file outside the
allowlist was modified**. Resolving it requires explicit Reviewer/Owner
authorization for a bounded post-Route-A test-contract migration (the precedent
already accepted for Issue #67) and, for the Issue #66 module, authorization to
touch an accepted Issue #66 implementation source.

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
**36 passed**.

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
**22 failed, 602 passed, 6 warnings, 13 errors in 3658.07 s (1:00:58)**.

This is **NOT green**, and the cause is the dependent-suite conflict documented
in §5.2 — five historical audit test files outside the Issue #70 allowlist assert
the pre-Route-A dual-`Q` behaviour that this Issue was authorized to remove. The
profile is reproducible and fully attributed: 13 of the errors cascade from the
single Issue #66 degenerate-gap-argmax `TypeError` at
`f0_final_rate_provenance_audit.py:491`, and the remaining failures are stale
assertions on the now-collapsed S1/S2 gaps and the correspondingly changed
Issue #68 / #69 terminals. **No file outside the four authorized paths was
modified to produce or to hide this result.** The 6 warnings are the pre-existing
`MatrixRankWarning` entries from the accepted oracle tests (`test_dlh_5b`,
`test_dlh_5c`).

Consequence for the completion contract: Issue #70 §10/§13 requires the full
suite to pass while §9 permits only four tracked paths. Those two requirements
cannot both hold once the mandated Route-A semantics change is applied. The
Builder therefore reports the conflict explicitly for Reviewer/Owner resolution
rather than widening the allowlist unilaterally.

## 9. Authorized files (exact four-path allowlist)

1. `src/deep_learning_hank/two_asset/boundary_hjb_selected_q.py`
2. `tests/test_dlh_5vv_route_a_single_q_operator_contract.py`
3. `reports/dlh_5vv_route_a_single_q_operator_contract_2026_09_15/DLH_5VV_ROUTE_A_SINGLE_Q_OPERATOR_CONTRACT_REPORT.md`
4. `reports/dlh_5vv_route_a_single_q_operator_contract_2026_09_15/DLH_5VV_ROUTE_A_SINGLE_Q_OPERATOR_CONTRACT_SUMMARY.csv`

No fifth tracked Builder path. No accepted source outside the single authorized
F0 `final=True` assembly was modified; the oracle and all accepted Issue #61–#69
blobs are byte-identical to their accepted values.

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
apply (no nonfinite evidence, no regression in the Route-A implementation and no
contract failure — the dependent-suite breakage in §5.2 is stale assertions plus
one degenerate-argmax code path in a historical audit module, and is disclosed
separately rather than hidden).

## 11. Next gate (for the Owner / reviewer — NOT decided here)

Two separate matters:

1. **Dependent-suite conflict (§5.2).** Resolving the 22 failed / 13 errored
   historical audit assertions requires a bounded post-Route-A test-contract
   migration authorization (Issue #67 precedent), including, for
   `f0_final_rate_provenance_audit.py`, permission to touch an accepted Issue #66
   implementation source whose degenerate-argmax handling assumes a non-zero gap.
2. **Residual reassessment.** The solve and final validation now share one
   coherent selected generator, so the final Bellman residual at `V_*`
   (`10.435094313164921`) is the genuine single-operator residual. It remains
   ~`10435`× the unchanged Bellman tolerance `1e-3`, so **validated HJB
   convergence is still FALSE**. Any reassessment of the residual's origin, any
   convergence-rule change, any new HJB iterate, and any authorized `Q^T`
   mass-dynamics work require fresh explicit authorization.

Stationary KFE remains **NOT AUTHORIZED**.
