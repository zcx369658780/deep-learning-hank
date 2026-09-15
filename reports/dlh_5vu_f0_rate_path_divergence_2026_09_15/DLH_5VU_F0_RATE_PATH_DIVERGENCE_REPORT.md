# DLH-5V-U — Latent F0 iteration-rate vs raw-drift sign divergence away from `V_*`

**Issue:** #69 / DLH-5V-U
**Task type:** `SCIENTIFIC_NUMERICAL_DIAGNOSTIC__F0_ITERATION_RATE_VS_RAW_DRIFT_SIGN_PROVENANCE_AWAY_FROM_VSTAR`
**Route decision:** `APPROVE_F0_ITERATION_RATE_VS_RAW_DRIFT_SIGN_PROVENANCE_AUDIT_AFTER_5VT_TERMINAL_C`
**Authority marker:** `DLH_5VU_F0_RATE_PATH_DIVERGENCE_AUDIT_AUTHORIZED`
**Initial authoritative activation:** `5676828795`
**Final authoritative activation-refresh:** `5677087565`
**Post-sync live `main`:** `510bde97e60c1fb7f2cb5afb5bee18da18ca561f`
**Dedicated Builder branch:** `dsh/issue-69-dlh-5vu-f0-rate-path-divergence-2026-09-15`
**Date:** 2026-09-15

## TERMINAL (exactly one)

```
DLH_5VU_F0_RATE_PATH_DIVERGENCE__UNIQUE_SIGN_OR_BRANCH_MECHANISM_ESTABLISHED_AND_FULLY_ACCOUNTS_FOR_TRIAL_OPERATOR_GAPS__RATE_SEMANTICS_SCIENTIFIC_REVIEW_GATE_READY
```

**Outcome A.** A unique, source-backed **sign / branch** mechanism is established
and it **fully accounts** for every observed rowwise operator gap at both frozen
Issue #68 trial states, with no unexplained remainder and no truncation,
destination, diagonal-accounting or a-axis contribution.

## 0. Scope ceiling — what this Issue does NOT do

- Read-only **diagnostic / provenance** work only.
- It does **NOT** choose or replace the authoritative rate path. Which path is
  scientifically correct away from `V_*` is **explicitly left open**.
- It does **NOT** accept any HJB iterate, does **NOT** claim HJB convergence,
  and does **NOT** construct any new Newton / tangent / constrained direction.
- It adds **no** third trial, no line search, no alpha tuning, and mutates **no**
  accepted source (selected-Q, oracle, or Issues #61–#68).
- Bellman tolerance remains the unchanged `1e-3`; the accepted residual
  `10.435094313164921` is still ~`10435`× that tolerance.

## 1. Frozen reconstruction and accepted Issue #68 geometry

| Required | Required value | Reproduced |
|---|---|---|
| iterations | 8 | **8** |
| final statistic | `3.6614352438846254e-08` | **`3.6614352438846254e-08`** |
| min boundary `p_b` | `4.8089461301970005e-09` | **`4.8089461301970005e-09`** |
| limiting wall | F3 (13,13), z=1 | **F3 (j=13, i=13, z=1), node 332** |
| `\|\|R\|\|inf` | `10.435094313164921` | **`10.435094313164921`** |
| tangent identity `g @ d_T` | `0` | **`0.0`** |

The accepted Issue #68 full-gradient tangent geometry is rebuilt exactly (two-entry
chain-rule wall gradient, single Euclidean projection). Frozen trial fractions,
unchanged and with no third trial: `alpha_half = 0.08085341880193442`,
`alpha_near = 0.16170683760386884`.

## 2. Exact accepted Issue #68 gap/row reproduction

| Trial | Required gap | Reproduced | Required rows | Reproduced |
|---|---|---|---|---|
| `alpha_half` | `0.6718037653783657` | **`0.6718037653783657`** | `{452, 453}` | **`(452, 453)`** |
| `alpha_near` | `1.3379411925537439` | **`1.3379411925537439`** | `{452, 453, 482, 483}` | **`(452, 453, 482, 483)`** |

Reproduction is enforced fail-closed: a mismatch in either the gap or the row
set raises `F0RatePathDivergenceFailure` rather than passing silently (asserted
by a dedicated test).

## 3. All-F0 accounting (not only the inconsistent rows)

| Quantity | `alpha_half` | `alpha_near` |
|---|---|---|
| total F0 rows | `596` | `596` |
| rate-identical rows | `594` | `592` |
| b-rate divergent rows | `2` | `4` |
| a-rate divergent rows | **`0`** | **`0`** |
| active-direction divergent rows | `0` | `0` |
| **opposite-direction-component rows** | **`2`** | **`4`** |
| diagonal divergent rows | `2` | `4` |
| destination-layout divergent rows | **`0`** | **`0`** |
| omitted-rate divergent rows | **`0`** | **`0`** |
| Q-row divergent rows | `2` | `4` |
| max b-rate difference | `0.3359018826891829` | `0.6689705962768726` |
| max a-rate difference | **`0.0`** | **`0.0`** |
| max diagonal difference | `0.6718037653783657` | `1.3379411925537443` |
| max rowwise Q difference | `0.6718037653783657` | `1.3379411925537439` |
| max decomposition residual | `3.552713678800501e-15` | `3.552713678800501e-15` |
| inconsistent row set | `(452, 453)` | `(452, 453, 482, 483)` |

**Decomposition closure.** For every affected row the summed off-diagonal rate
difference equals the diagonal difference to machine precision:

| Row | `summed_rate_difference` | `diagonal_difference` | residual |
|---|---|---|---|
| 452 (`alpha_half`) | `0.6718037653783653` | `0.6718037653783657` | `4.44e-16` |
| 453 (`alpha_half`) | `0.35345619671126904` | `0.35345619671126904` | `0.0` |
| 452 (`alpha_near`) | `1.3379411925537448` | `1.3379411925537443` | `4.44e-16` |
| 453 / 482 / 483 (`alpha_near`) | equal | equal | `<= 3.55e-15` |

There is **no unexplained remainder**: `max_decomposition_residual <= 3.55e-15`
across all `596` F0 rows at both trials, so the observed Q gaps are **fully
accounted for** by the rate decomposition.

## 4. Per-row evidence (all six affected row-instances)

Each affected row was re-derived by **re-invoking the accepted policy function
read-only** with the exact inputs `local_interior_row` used, and the
re-invocation is verified to reproduce the solver's own re-selection
`row_entries` **exactly** (`all_rows_reproduced = True`) — so the stored
iteration rates are read from the accepted source, not inferred from names.

### 4.1 `alpha_half`, row 452 — node 61, (j=1, i=28), z=1, family F0, sector B

| Quantity | Value |
|---|---|
| consumption / labor / transfer | `1.119920142728147` / `0.9749843243943356` / `0.5384231361639152` |
| utility | `-1.0360850481422097` |
| stored `mu_a` / `mu_b` | `0.5752652414270617` / `-1.0193211243365425` |
| **recomputed raw `mu_a` / `mu_b`** | `0.5752652414270617` / **`-1.0193211243365425`** (bit-identical) |
| iteration `b_backward` / `b_forward` | `3.1026306487455124` / **`0.3359018826891829`** |
| raw `b_backward` / `b_forward` | `2.76672876605633` / **`0.0`** |
| iteration `a_backward` / `a_forward` | `-0.0` / `1.0930039587114173` |
| raw `a_backward` / `a_forward` | `0.0` / `1.0930039587114173` |
| active b direction (iteration / raw) | `B` / `B` |
| active a direction (iteration / raw) | `F` / `F` |
| **opposite-direction component (iteration / raw)** | **`True` / `False`** |
| iteration diagonal / final diagonal | `-4.531536490146113` / `-3.8597327247677473` |
| iteration destinations / final destinations | `(451, 453, 484)` / `(451, 484)` |
| Q-gap non-zero columns / magnitudes | `(451, 452, 453)` / `(0.3359, 0.6718, 0.3359)` |

### 4.2 `alpha_half`, row 453 — node 62, (j=1, i=29), z=1, sector B

| Quantity | Value |
|---|---|
| stored / raw `mu_b` | `-0.9558602919939625` / `-0.9558602919939625` |
| iteration `b_backward` / `b_forward` | `2.7712060337678186` / **`0.17672809835563455`** |
| raw `b_backward` / `b_forward` | `2.594477935412184` / **`0.0`** |
| a-axis (iteration = raw) | `-0.0` / `1.0174459000703193` |
| iteration diagonal / final diagonal | `-3.9653800321937727` / `-3.6119238354825036` |
| destinations iteration / final | `(452, 454, 485)` / `(452, 485)` |

### 4.3 `alpha_near` — rows 452, 453, 482, 483

| Row | node | (j,i,z) | stored/raw `mu_b` | it `b_f` | raw `b_f` | it diagonal | final diagonal |
|---|---|---|---|---|---|---|---|
| 452 | 61 | (1,28,1) | `-0.7784695102701767` | **`0.6689705962768723`** | **`0.0`** | `-4.470887024977735` | `-3.1329458324239905` |
| 453 | 62 | (1,29,1) | `-0.6758516138264798` | **`0.5026579692736282`** | **`0.0`** | `-3.7520629048368934` | `-2.7467469662896367` |
| 482 | 91 | (2,26,1) | `-2.032510279427643` | **`0.08430831528434231`** | **`0.0`** | `-7.734013085816811` | `-7.565396455248126` |
| 483 | 92 | (2,27,1) | `-1.81629254480136` | **`0.26020326300514`** | **`0.0`** | `-7.401734207223617` | `-6.881327681213337` |

On every affected row: `stored_mu_b == raw_mu_b` **bit-identically**, the a-axis
rates agree **exactly**, the realized drift points **backward**, the raw path
therefore stores **no** forward rate, and the iteration path stores a **positive
forward rate** — an opposite-direction component. Controls and utility are
**bit-identical** across the two constructions (`same_controls_and_utility =
True`).

## 5. Source-backed provenance (read-only trace)

Full anchors are persisted in `provenance_mapping()` and asserted by the test
suite against the accepted sources.

### 5.1 Iteration path — `matlab_faithful_two_asset_ha.select_matlab_faithful_local_policy`

```
iteration_b_backward_rate = -(sc_b if use_liquid_b else 0)
                            - (sdh_b if use_transfer_b else 0)) / db      # lines 408-411
iteration_b_forward_rate  = +(sc_f if use_liquid_f else 0)
                            + (sdh_f if use_transfer_f else 0)) / db      # lines 412-415
```

with the branch trees

```
sc_b = liquid_resources_b - consumption_b          # lines 281-284
sc_f = liquid_resources_f - consumption_f
use_liquid_b = sc_b < -tolerance                   # line 285
use_liquid_f = sc_f > tolerance and not use_liquid_b  # line 286

d_b = d_bf*(d_bf > 0) + d_bb*(d_bb < 0)            # line 311
d_f = d_ff*(d_ff > 0) + d_fb*(d_fb < 0)            # line 312
sdh_b = -d_b - adjustment_cost(d_b)                # lines 322-335
sdh_f = -d_f - adjustment_cost(d_f)                # lines 336-348
use_transfer_f = sdh_f > tolerance                 # line 349
use_transfer_b = sdh_b < -tolerance and not use_transfer_f  # line 350

a_backward_rate = -mh_b/da,  mh_b = min(shadow_transfer_b, 0)   # lines 373, 406
a_forward_rate  =  mh_f/da,  mh_f = max(shadow_transfer_f, 0) + effective_return*a  # lines 374, 407
```

**Critical: `sc_b`/`sc_f` are LIQUID first-order-condition residuals and
`sdh_b`/`sdh_f` are TRANSFER branch objects. Neither is the realized drift
`mu_b`.** The b-rates are therefore *branch-gated FOC/shadow objects divided by
`db`*, not upwinded drifts.

These are consumed by `boundary_hjb_selected_q.local_interior_row` (lines
484–521), which builds entries from exactly those four stored rates and sets
`diagonal = -(rb + rf + ab + af)` (line 520).

### 5.2 Corrected `final=True` path — `boundary_hjb_selected_q.build_operator_and_u`

```
mu_a_v, mu_b_v, _ = asset_drifts_matlab_faithful(      # lines 962-965
    a_v, b_v, z_v, rec.consumption, [rec.labor], rec.transfer, ...)
ab = max(-mu_a_v, 0.0) / self.da                       # line 966
af = max( mu_a_v, 0.0) / self.da                       # line 967
bb = max(-mu_b_v, 0.0) / self.db                       # line 968
bf = max( mu_b_v, 0.0) / self.db                       # line 969
diag = -(bb + bf + ab + af)                            # line 976
cols.append(nz * self.n + dn)                          # line 978 (repaired)
```

Same selected controls, raw-drift recompute, `max(±mu)/step` mapping, same-z-block
destination layout, same diagonal construction.

### 5.3 Equivalence and the exact divergence condition

**Globally algebraically equivalent: NO.** The iteration b-rate uses branch-gated
FOC shadow objects; the corrected final b-rate uses the realized drift through
`max(±mu)/db`. They coincide **only** on the subset where the liquid branch is
inactive (`liquid_label == "0"`, i.e. neither `sc_b < -tol` nor `sc_f > tol`),
and they coincide trivially wherever both rates are zero.

**Exact local condition** (identical on all six affected row-instances):

> `liquid_label == "F"` — the liquid branch is **binding at the lower bound**, so
> `use_liquid_f` is true and `sc_f > tolerance` contributes a **positive**
> `iteration_b_forward_rate` — **while the realized `mu_b` is negative**
> (drift backward). The iteration path therefore places a spurious forward
> destination at `nz*n + up` and stores an inflated `iteration_b_backward_rate`;
> the corrected raw path stores `b_forward = 0` and the honest
> `max(-mu_b,0)/db`.

Observed signature on every affected row: `iteration_b_forward_rate > 0` with
`raw_mu_b < 0` and `raw_b_forward_rate == 0`.

**Classification of the mechanism:** **sign / branch**, not truncation. The a-axis
rates are identical everywhere, destination layouts agree, and no omitted
destination rate exists on either path. The extra iteration destination is
simply the **zero-rate forward slot made non-zero** — the same four-slot in-block
upwind template, different rate values.

## 6. Classification flags

| Flag | Value |
|---|---|
| `ITER_RATE_PATH_SOURCE_BACKED` | **True** |
| `FINAL_RAW_PATH_SOURCE_BACKED` | **True** |
| `RATE_FORMULAS_GLOBALLY_EQUIVALENT` | **False** |
| `SIGN_OR_BRANCH_DIVERGENCE_ESTABLISHED` | **True** |
| `TRUNCATION_OR_DESTINATION_DIVERGENCE_ESTABLISHED` | **False** |
| `OTHER_MECHANISM_ESTABLISHED` | **False** |
| `MIXED_OR_UNRESOLVED` | **False** |

These follow directly from the measured evidence; nothing was forced. In
particular `SIGN_OR_BRANCH_DIVERGENCE_ESTABLISHED` requires **all** of: every
affected row diverges on b-rates; every affected row shows an opposite-direction
component on the iteration path; **no** affected row shows one on the raw path;
and the opposite-direction row count equals the divergent-row count at both
trials.

## 7. Terminal derivation (frozen rule)

- unique source-backed sign/branch mechanism established: **yes**;
- it fully accounts for the trial operator gaps: **yes** (decomposition closed
  with `max residual 3.55e-15`, no remainder);
- no truncation/destination mechanism and no other mechanism: **yes**;
- evidence finite and consistent: **yes** (`failure_detail = None`);
- deterministic repeat identical: **yes**.

→ **Outcome A**, exactly one terminal.

## 8. Scientific reading (local, diagnostic only)

The Issue #68 operator inconsistency is now fully explained. It is **not** a
destination-layout or truncation artifact and **not** a drift-recomputation
difference — the stored and recomputed drifts are bit-identical. It is a
**rate-object provenance difference**: the accepted iteration path derives its
liquid-direction b-rates from branch-gated FOC shadow objects (`sc_f`, `sdh_f`)
which, when the liquid branch is binding, inject a positive forward component
even though the realized liquid drift points backward. The corrected `final=True`
path derives its b-rates from the realized drift through `max(±mu)/db`, which
can never store an opposite-direction component.

**This audit does not decide which path is correct away from `V_*`.** Both are
source-backed and each is self-consistent within its own construction; the
question of which is authoritative for the discrete HJB operator off `V_*` is a
scientific-judgment gate that requires an explicit Owner decision. The audit
also does not establish HJB nonexistence or convergence failure, and authorizes
no source mutation.

## 9. Deterministic repeat

The full audit was executed twice; every compared field is identical
(`deterministic_repeat_identical = True`), including the provenance mapping, all
`596`-row accounting statistics, every per-row rate pair, the decomposition
residuals, the classification flags and the terminal.

## 10. Tests

Focused suite `tests/test_dlh_5vu_f0_rate_path_divergence.py`: **28 passed**.

Coverage: exact `V_*` reconstruction; exact accepted Issue #68 `alpha_half` /
`alpha_near`; selected-Q repaired blob exactness via `git rev-parse`;
exact two-trial gap/row reproduction with a fail-closed test; same
controls/utility across the compared paths; stored-vs-raw drift identity;
iteration-rate reproduction from the accepted policy function; the
opposite-direction-component mechanism; a-axis rate identity everywhere;
b-rate divergence magnitudes; all-F0 accounting counts; rowwise Q-gap
decomposition closure; destination-layout non-divergence; Q-gap non-zero column
recording; classification flags; exactly one terminal; terminal-follows-frozen-rule;
no authoritative path selected; provenance mapping determinism with anchors
verified to exist in the accepted sources; exactly two trials with no third;
exactly five runtime operator builds (spy: 3 `final=False` + 2 `final=True`) and
three static call sites; deterministic repeat identical; no accepted iterate;
static AST scan for forbidden machinery (exactly one `spsolve`, no
Newton/loop/line-search/KFE/steady-state tokens).

Full repository suite `python -m pytest tests/ -q`: **601 passed, 0 failed,
6 warnings in 3567.97 s (0:59:27)**. The 6 warnings are the pre-existing
`MatrixRankWarning` entries from the accepted oracle tests (`test_dlh_5b`,
`test_dlh_5c`), not failures.

## 11. Authorized files (exact four-path allowlist)

1. `src/deep_learning_hank/two_asset/f0_rate_path_divergence_audit.py`
2. `tests/test_dlh_5vu_f0_rate_path_divergence.py`
3. `reports/dlh_5vu_f0_rate_path_divergence_2026_09_15/DLH_5VU_F0_RATE_PATH_DIVERGENCE_REPORT.md`
4. `reports/dlh_5vu_f0_rate_path_divergence_2026_09_15/DLH_5VU_F0_RATE_PATH_DIVERGENCE_SUMMARY.csv`

No fifth tracked Builder path. All accepted sources/tests/reports/governance
remain byte-identical to their accepted blobs; the selected-Q repaired blob
`556ccc214f03a1a22306cc4f5c7e9f7691bbf897` is unchanged.

## 12. Next gate (for the Owner / reviewer — NOT decided here)

The divergence is a **rate-object provenance** question, not a numerical defect:
off `V_*`, the accepted iteration path can store an opposite-direction rate
component sourced from a binding-liquid FOC shadow object, while the corrected
`final=True` path cannot. Deciding which construction is authoritative for the
discrete HJB operator away from `V_*` — or defining when each applies — is an
explicit Owner scientific decision. Nothing in this audit authorizes mutating
either path, changing the convergence criterion, or accepting a new iterate.

Stationary KFE remains **NOT AUTHORIZED**.
