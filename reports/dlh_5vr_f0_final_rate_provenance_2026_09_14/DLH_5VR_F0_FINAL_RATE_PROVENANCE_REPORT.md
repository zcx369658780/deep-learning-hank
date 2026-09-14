# DLH-5V-R — F0 Final-Rate Discretization Provenance and Operator-Consistency Audit

**Issue:** #66 — `SCIENTIFIC_NUMERICAL_DIAGNOSTIC__F0_FINAL_RATE_DISCRETIZATION_PROVENANCE_AND_OPERATOR_CONSISTENCY`

**Route decision:** `APPROVE_F0_FINAL_RATE_DISCRETIZATION_PROVENANCE_AND_OPERATOR_CONSISTENCY_AUDIT_AFTER_5VQ_TERMINAL_B`

**Authority marker:** `DLH_5VR_F0_FINAL_RATE_PROVENANCE_AUDIT_AUTHORIZED`

**Activations:** `5656814064` (initial) · `5657247407` (final authoritative activation-refresh; live `main` = `a4227f38a5f11b07e7881f58534e37a4887f5ea7`)

**Branch:** `dsh/issue-66-dlh-5vr-f0-final-rate-provenance-2026-09-14` (base = merge-base = `a4227f38a5f11b07e7881f58534e37a4887f5ea7`)

**Date:** 2026-09-14

---

## Outcome (exactly one terminal)

```
TERMINAL A — DLH_5VR_F0_FINAL_RATE_PROVENANCE__ITERATION_OPERATOR_MATCHES_ACCEPTED_MATLAB_FAITHFUL_HJB__FINAL_RAW_RATE_OPERATOR_NON_EQUIVALENT__VALIDATION_OPERATOR_REDESIGN_REVIEW_GATE_READY
```

Frozen classifications (Issue #66 §11), measured at the accepted Issue #63 stagnation state `V_*`:

| Flag | Value | Evidence |
|---|---|---|
| `ITER_EQ_MATLAB` | **true** | accepted iteration F0 row (rates **and** within-z-block destination assembly) reproduces the accepted oracle iteration operator on all 596 F0 rows (repro max 0.0) |
| `FINAL_EQ_MATLAB` | **false** | rate formulas equal the accepted oracle post-convergence formula (`final_eq_rate_formula=true`), but the accepted `final=True` F0 **row assembly drops the z-block destination offset** for z=1 rows (`final_eq_assembly=false`) — the accepted FINAL-RAW row is not the MATLAB-faithful discrete HJB row |
| `BOTH_EQUIVALENT` | false | rowwise max `|Q_final_current − Q_iter|` = 24.601971766296664 > 0 |
| `MIXED_OR_UNRESOLVED` | false | provenance fully resolved from the accepted sources (two distinct, precisely-located constructions) |
| materially non-equivalent | true | 24.601971766296664 > MATERIAL_GAP_TOL = 1.0 |

Frozen rule: Terminal A iff `ITER_EQ_MATLAB = true` AND `FINAL_EQ_MATLAB = false` AND materially non-equivalent → fires. Terminal B requires `FINAL_EQ_MATLAB = true` (does not hold). Terminal C requires both-eq / mixed / unresolved (does not hold). Exactly one terminal is returned.

---

## 1. Deterministic reconstruction of the accepted Issue #63 stagnation state

ONE deterministic reconstruction (accepted Issue #65/#64 helper path, 8 steps, STOP before any new HJB iterate is accepted). No new iterate, Newton, continuation, line-search, KFE, or steady-state machinery is executed by this audit (static scan + runtime spy, §8).

| Step | `accepted_max_stat` | `halving_count` | `selected_min_pb` | worst state (after) |
|---|---|---|---|---|
| 1 | 0.33266420034779287 | 15 | 4.807686276815052e-02 | F3 (13,13) z=1 |
| 2 | 0.03462212614034854 | 19 | 4.807726400828066e-03 | F3 (13,13) z=1 |
| 3 | 0.0035992954473869077 | 22 | 4.8077689340431107e-04 | F3 (13,13) z=1 |
| 4 | 0.00036419854994562684 | 25 | 4.807812084704568e-05 | F3 (13,13) z=1 |
| 5 | 3.655373977551335e-05 | 29 | 4.807856211438581e-06 | F3 (13,13) z=1 |
| 6 | 3.659616339746208e-06 | 32 | 4.807908920513781e-07 | F3 (13,13) z=1 |
| 7 | 3.6609790754482674e-07 | 35 | 4.808043537910375e-08 | F3 (13,13) z=1 |
| 8 | **3.6614352438846254e-08** | 39 | **4.8089461301970005e-09** | F3 (13,13) z=1 |

- Final (accepted) statistic ≈ `3.6614352438846254e-08` ✓ (Issue #66 required value)
- Min boundary p_b at `V_*` ≈ `4.8089461301970005e-09` ✓ (required value)
- Wall state: F3, (j=13, i=13), z=1, node 332 ✓
- `v0_min_boundary_pb` = 0.48076562156308306; `min_accepted_boundary_pb` = 4.8089461301970005e-09

## 2. Exactly two authorized builds at the same `V_*`

- Build A (exactly once): current-policy `final=False` → `Q_iter`, `u_iter`, `records_current` (the current selected F0 controls).
- Build B (exactly once): current-policy `final=True` with `f0_policies = records_current` (**same** controls) → `Q_final_current`, `u_final_current`, `records_final`.
- No stale-record route: `records_pre_step8` is accepted baseline fact only, never a scientific object.
- Same-controls contract: max |control diff| between the two builds' records = **0.0** (exact).
- Non-F0 boundary rows: max |Q diff| = **0.0**, max |u diff| = **0.0** (identical accepted `_boundary_row` path at the same `V_*`; any discrepancy fails closed → Terminal C).
- `max |Q·1|` (conservativity): `2.4253377084448857e-12` on both operators; expansions 0 / 0, artificial bindings 0 / 0.
- Runtime counting spy: exactly **2** `build_operator_and_u` calls at `V_*` (the reconstruction's internal builds belong to the ONE reconstruction).

## 3. Reproductions of the accepted statistics

| Quantity | Measured | Accepted | Match |
|---|---|---|---|
| `||R_iter||_inf` | 10.435094313164921 | 10.435094313164921 | exact |
| `||R_iter||_inf` argmax | F0 node 97 (j=3,i=2,z=0) | — | |
| `||R_final_current||_inf` | 490.7560414005864 | 490.7560414005864 | exact |
| `||R_final_current||_inf` argmax | F0 node 272 (j=10,i=5,z=1) | — | |
| boundary `||R||_inf` (both) | 9.742068328671465 | — | identical |
| F0 rowwise max `|Q_final_current − Q_iter|` | 24.601971766296664 | ≈ 24.6019717663 | exact |
| gap argmax state | F0 node 297 (j=11,i=11,z=1) | — | |
| F0 rows / boundary rows | 596 / 186 (state size 782 = 391 nodes × 2 z) | — | |

`R = rho·V_* − (u + Q·V_*)` in both semantics, `V_*` unchanged across both builds.

## 4. All-F0 compact row/rate/component comparison

Per F0 row the diagnostic records, for both semantics, the compact components
`b_backward`, `b_forward`, `a_backward`, `a_forward`, `diagonal`,
`represented_outgoing_sum`, `omitted_destination_rate`, `utility/source`
(per-row arrays held by the audit result; classes summarized below).

### 4a. Rate/operator component classes (ITER vs FINAL-RAW rates)

| Component class | affected rows | max abs diff | argmax |
|---|---|---|---|
| `b_backward` | 0 | 7.105427357601002e-15 | — |
| `b_forward` | 0 | 0.0 | — |
| `a_backward` | 0 | 0.0 | — |
| `a_forward` | 0 | 0.0 | — |
| `diagonal` | 0 | 1.4210854715202004e-14 | — |
| `represented_outgoing_sum` | 0 | 1.4210854715202004e-14 | — |
| `omitted_destination_rate` | 0 | 0.0 | — |
| `utility/source` | 0 | 0.0 | — |

Measured identity (source-backed, Issue #66 §6): on all 596 F0 rows at `V_*`
the accepted iteration b-rates coincide with `max(±mu_b)/db` (the sc/sdh
shadow flow sums to the raw drift) and the iteration a-rates coincide with
`max(±mu_a)/da` (transfer branch 0, `mu_a = r_eff·a ≥ 0`). The rate **formulas**
of the two constructions therefore contribute ~0 to the operator gap.

### 4b. Destination-assembly class — the measured driver of the ~24.60 gap

| Metric | Value |
|---|---|
| affected rows (`destination_assembly_gap`) | **298** (= z=1 F0 rows with non-zero off-diagonal rates) |
| max abs diff | **24.601971766296664** |
| argmax state | F0 node 297 (j=11,i=11,z=1) |
| accepted-FINAL row vs MATLAB-faithful-post row deviation (max / affected) | 24.601971766296664 / 298 |

Argmax-row decomposition (node 297, z=1): the same two rates sit at **different
destinations** in the two operators — `b_backward` 24.601971766296664 and
`a_forward` 9.52637251075067, each at two placement columns
(`max_row_columns_with_diff = 4`); `diagonal` and `switch_matrix_or_other`
contribute 0.0. `max_total_row_entry_diff` = 24.601971766296664 at the same
state.

Accounting identities (both semantics, all 596 rows): `represented_outgoing_sum
+ omitted_destination_rate = −diagonal` (max err ≤ 1e-12); F0 cells are
strictly interior with all four neighbors, so `omitted_destination_rate` =
**0.0 on every F0 row** (measured, not assumed).

### 4c. Independent identity checks

- utility/source terms: max |`u_final_current` − `u_iter`| on F0 rows = **0.0** exactly (same current controls; independent of the rate comparison).
- non-F0 boundary rows: max |Q diff| = **0.0**, max |u diff| = **0.0** exactly.

## 5. Source-backed MATLAB/oracle provenance mapping (read-only)

Deterministic mapping (no re-interpretation or rewrite of accepted semantics):

- **ITER F0 row** = oracle `select_matlab_faithful_local_policy`
  (`matlab_faithful_two_asset_ha.py:193-416`) consumed verbatim by
  `local_interior_row` (`boundary_hjb_selected_q.py:484-521`); b-direction
  iteration sc/sdh rates (`matlab_faithful_two_asset_ha.py:408-415`), a-direction
  shadow-mh rates (lines 372-377, 406-407); iteration operator assembled at
  lines 553-555; destination columns within the z-block
  (`boundary_hjb_selected_q.py:1008` `nz*self.n + dn`), matching the oracle
  `assemble_source_axis` (lines 425-451) layout.
- **FINAL-RAW rate formulas** = `max(-mu_b,0)/db, max(mu_b,0)/db,
  max(-mu_a,0)/da, max(mu_a,0)/da` (`boundary_hjb_selected_q.py:966-969`) over
  raw drifts recomputed via `asset_drifts_matlab_faithful`
  (`boundary_hjb_selected_q.py:962-965`) — **exact** oracle post-convergence
  operator formula (`matlab_faithful_two_asset_ha.py:562`).
- **FINAL-RAW destination assembly deviation (decisive, source-backed):**
  `boundary_hjb_selected_q.py:978` writes off-diagonal columns as bare node
  indices `cols.append(dn)` with **no z-block offset**, whereas the accepted
  iteration path (line 1008), the accepted boundary path (line 1029), and the
  oracle assembly all place destinations within the same z-block. For z=1 F0
  rows the accepted `final=True` off-diagonal entries therefore point at
  z=0-block columns. This is a property of the **accepted** source, reported
  read-only; it is not introduced or fixed here.
- Truncation convention is identical in both semantics (drop off-diagonal
  entry when the destination is unavailable, keep the rate on the diagonal):
  oracle `assemble_source_axis` lines 425-451 (docstring line 428) vs
  selected-Q lines 512-520 / 970-979.
- Switch matrix: `Q + B kron(switch_matrix, I_n)` (`boundary_hjb_selected_q.py:1034-1036`;
  oracle line 463) — identical contribution on both operators.

## 6. Scientific interpretation and Owner decision gate

The ~490.756 `final=True` validation residual and the ~24.60 F0 operator gap
are **not** explained by rate formulas: the accepted iteration rates and the
accepted post-convergence `max(±mu)/step` rates coincide numerically on every
F0 row (measured). The gap is a **destination-assembly** property: the
accepted `final=True` F0 path drops the z-block column offset
(`boundary_hjb_selected_q.py:978`), so on z=1 rows its off-diagonal entries
point at z=0-block states. The iteration operator is the accepted
MATLAB-faithful iteration operator (Terminal A premise holds); the accepted
FINAL-RAW row is not the MATLAB-faithful post-convergence row even though its
rate formulas are.

Per the frozen rule, `ITER_EQ_MATLAB=true` + `FINAL_EQ_MATLAB=false` +
materially non-equivalent → **Terminal A**:
**`VALIDATION_OPERATOR_REDESIGN_REVIEW_GATE_READY`**. The Owner scientific
review gate concerns whether/where the accepted `final=True` F0 assembly
should place z=1 destinations (e.g., within-z-block `nz*n + dn`), before any
validation-operator redesign is authorized. This audit authorizes nothing
beyond the diagnostic: it does not replace `final=True`, change any
convergence criterion, mutate accepted source, or declare `R_iter` an
accepted final convergence residual. Stationary KFE remains NOT AUTHORIZED.

## 7. Deterministic repeat

One deterministic repeat of the full diagnostic (two complete
reconstructions): bit-identical across all measured fields →
`deterministic_repeat_identical = true`.

## 8. Forbidden-machinery check

- Static AST scan of the audit module: none of `newton`, `continuation`,
  `linesearch`, `armijo`, `damp`, `clip`, `floor`, `maximum`, `minimum`,
  `trust_region`, `semismooth`, `policy_iteration`, `spsolve`,
  `construct_ftb_step`, `trial`, `kfe`, `stationary`, `steady_state`,
  `solve_household_steady_state` appear in code; exactly **2**
  `build_operator_and_u` calls in module source.
- Runtime counting spy: exactly **2** builds at `V_*` (one `final=False`, one
  `final=True` with the same controls).
- Fail-closed guards: non-finite residual/component evidence and F0-record
  provenance ambiguity raise `F0FinalRateProvenanceFailure` (→ Terminal C at
  run level); boundary-row discrepancy between the two builds fails closed.

## Companion artifacts

- `src/deep_learning_hank/two_asset/f0_final_rate_provenance_audit.py` — the audit module.
- `tests/test_dlh_5vr_f0_final_rate_provenance.py` — 17 tests covering the full Issue #66 mandated surface (all pass).
- `DLH_5VR_F0_FINAL_RATE_PROVENANCE_SUMMARY.csv` — compact evidence table.
