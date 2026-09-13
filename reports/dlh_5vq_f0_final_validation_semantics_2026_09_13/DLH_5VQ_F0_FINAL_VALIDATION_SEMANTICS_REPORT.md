# DLH-5V-Q — F0 Final-Validation Operator Consistency Audit at the Accepted Stagnation State — Report

Issue #65 / DLH-5V-Q — `SCIENTIFIC_NUMERICAL_DIAGNOSTIC__F0_FINAL_VALIDATION_OPERATOR_CONSISTENCY_AUDIT`

Branch: `dsh/issue-65-dlh-5vq-f0-final-validation-audit-2026-09-13`

Authority: Issue #65 OPEN; initial activation `5653199929`; final authoritative
activation-refresh `5653443917` (post-sync live `main`
`3e82970d59a10ecd812f9d39889f145661dcc293`). Route decision
`APPROVE_F0_FINAL_VALIDATION_OPERATOR_CONSISTENCY_AUDIT_AFTER_5VP_TERMINAL_B`;
authority marker `DLH_5VQ_F0_FINAL_VALIDATION_SEMANTICS_AUDIT_AUTHORIZED`.

## 1. Terminal (exactly ONE)

> **B — `DLH_5VQ_F0_FINAL_VALIDATION_SEMANTICS__FINAL_RATE_SEMANTICS_DOMINATE_OR_TIE_ACCEPTED_VALIDATION_GAP__F0_FINAL_OPERATOR_REVIEW_REQUIRED`**

`||D_rate||_inf = 488.0988417984485 >= ||D_stale||_inf = 1.8406872158038823e-05`
→ frozen rule `FINAL_RATE_SEMANTICS_DOMINANT_OR_TIED`. The accepted ~490.756
final-validation gap at `V_*` is **not** caused by stale F0 records: the
`final=True` F0 upwind-rate/discretization semantics themselves dominate it.
Deterministic repeat bit-identical.

## 2. Answer to the scientific question

The accepted Issue #64 finding (the ~490.756 vs ~10.435 residual gap is
entirely an F0 phenomenon) is now attributed locally at the same fixed `V_*`:

1. **stale-record effect: negligible.** `records_pre_step8` and
   `records_current` are nearly identical (accepted step 8 is tiny): 0 of 596
   F0 rows change sector/transfer label; max |Δ consumption| = 1.26e-8, |Δ
   labor| = 3.53e-9, |Δ transfer| = 2.06e-7, |Δ mu_a| = 2.06e-7, |Δ mu_b| =
   4.03e-7, |Δ utility| = 1.09e-8. Consequently
   `||D_stale||_inf = ||R_final_stale - R_final_current||_inf = 1.84e-5`.
2. **final-rate/discretization effect: dominant.** Re-validating at the SAME
   `V_*` with the freshly re-selected current F0 records yields
   `||R_final_current||_inf = 490.7560414005864 ≈ 490.7560425919994` — the gap
   against the iteration residual is essentially unchanged:
   `||D_rate||_inf = ||R_final_current - R_iter||_inf = 488.0988417984485`.
   The F0 operator itself changes massively under `final=True` semantics:
   rowwise max |`Q_final_current` − `Q_iter`| = 24.60 (F0 node 297 (11,11),
   z=1), versus rowwise max |`Q_final_stale` − `Q_final_current`| = 1.48e-6.

**Verdict:** a "final-validation record refresh" (re-validating with fresh
`V_*`-selected F0 records) would NOT close the accepted validation gap. The
gap is intrinsic to the accepted `final=True` F0 upwind-rate construction
evaluated at `V_*` — a state that is not a fixed point of that final operator.
The accepted F0 final operator construction itself requires review
(`F0_FINAL_OPERATOR_REVIEW_REQUIRED`).

## 3. Frozen stagnation-state reconstruction (reproduced exactly)

Accepted Issue #64 reconstruction path, STOP immediately after accepted FTB
step 8, before any new HJB iterate is accepted (8 root-controlled steps;
halvings 15/19/22/25/29/32/35/39):

- final step statistic = `3.6614352438846254e-08`;
- final min boundary `p_b(V_*) = 4.8089461301970005e-09` (> `PB_MARGIN=1e-12`);
- wall state `V_*` = node 332, **F3 (13,13), z=1** (same as every accepted
  step and Issues #61/#62/#63/#64);
- accepted stale-record final residual = `490.7560425919994` — reproduced
  exactly as `||R_final_stale||_inf` (Build B; identical quantity to the
  accepted final-validation Bellman residual);
- `V_0` min boundary p_b = `0.48076562156308306`.

Provenance preserved and kept strictly separate (never swapped):
`records_pre_step8` = the accepted pre-step-8 records used by Issue #63 final
validation (the `final=False` build at the iterate before accepted step 8);
`records_current` = the `final=False` policies re-selected exactly once at
`V_*` (returned by Build A).

## 4. Exactly three operator/residual builds at the same fixed `V_*`

| object | build | formula | `||·||_inf` | argmax (total) |
|---|---|---|---|---|
| A. iteration | `final=False` (once) → `Q_iter, u_iter, records_current` | `R_iter = rho V_* - [u_iter + Q_iter V_*]` | 10.435094313164921 | F0 node 97 (3,2) z=0 |
| B. accepted stale-record final | `final=True`, `f0_policies = records_pre_step8` | `R_final_stale = rho V_* - [u_final_stale + Q_final_stale V_*]` | 490.7560425919994 | F0 node 272 (10,5) z=1 |
| C. diagnostic current-record final | `final=True`, `f0_policies = records_current` | `R_final_current = rho V_* - [u_final_current + Q_final_current V_*]` | 490.7560414005864 | F0 node 272 (10,5) z=1 |

C is a diagnostic counterfactual operator at the same state only — NOT an
accepted replacement validation rule, and never declared the correct
convergence criterion.

Operator diagnostics (all three): `max|Q 1| = 2.4253377084448857e-12`
(conservative), optimizer expansions = 0, artificial bindings = 0.

## 5. Exact decomposition and total / F0 / boundary record

`D_total = R_final_stale - R_iter`; `D_stale = R_final_stale -
R_final_current`; `D_rate = R_final_current - R_iter`; verified
`D_total = D_stale + D_rate` with `max|D_total - (D_stale + D_rate)|_inf =
0.0` (≤ declared `DECOMPOSITION_TOL = 1e-6`).

| vector | total ‖·‖∞ | argmax | F0-only max | boundary-only max |
|---|---|---|---|---|
| R_iter | 10.435094313164921 | F0 node 97 (3,2) z=0 | 10.435094313164921 | 9.742068328671465 (F10 node 0 (0,0) z=0) |
| R_final_stale | 490.7560425919994 | F0 node 272 (10,5) z=1 | 490.7560425919994 | 9.742068328671465 (F10 node 0 (0,0) z=0) |
| R_final_current | 490.7560414005864 | F0 node 272 (10,5) z=1 | 490.7560414005864 | 9.742068328671465 (F10 node 0 (0,0) z=0) |
| D_total | 488.0988429898615 | F0 node 272 (10,5) z=1 | 488.0988429898615 | **0.0** |
| D_stale | 1.8406872158038823e-05 | F0 node 331 (13,12) z=1 | 1.8406872158038823e-05 | **0.0** |
| D_rate | 488.0988417984485 | F0 node 272 (10,5) z=1 | 488.0988417984485 | **0.0** |

Boundary-only difference is **exactly 0.0 for all three differences**, and the
boundary-only residual value (9.742068328671465) is identical across the
three operators — consistent with the accepted Issue #64 evidence that
boundary rows are built identically in both semantics (no boundary reselection
contribution).

## 6. F0 continuous-control provenance audit (F0 rows only, 596 rows)

`records_pre_step8` vs `records_current`:

| diagnostic | value |
|---|---|
| changed sector/transfer-label count | **0** / 596 |
| max |Δ consumption| | 1.2570318563831506e-08 |
| max |Δ labor| | 3.527538039449496e-09 |
| max |Δ transfer| | 2.0576147896633756e-07 |
| max |Δ mu_a| | 2.0576147896633756e-07 |
| max |Δ mu_b| | 4.029644697922663e-07 |
| max |Δ utility| | 1.088601719878568e-08 |

Same sector/transfer label (0 changes) is NOT treated as proof of identical
continuous controls: the continuous deltas above are small but strictly
positive, and the operator audit below shows the semantic change is large.

F0-only operator differences:

| difference | rowwise max abs (argmax F0 row) |
|---|---|
| `Q_final_stale - Q_final_current` | 1.4847075142654376e-06 (node 331 (13,12) z=1) |
| `Q_final_current - Q_iter` | 24.601971766296664 (node 297 (11,11) z=1) |
| `u_final_stale - u_final_current` max abs | 1.088601719878568e-08 (node 226 (8,1) z=1) |
| `u_final_current - u_iter` max abs | 0.0 (identical selected F0 utilities) |

The rowwise `Q_final_current - Q_iter` gap of ~24.6 quantifies how materially
the accepted `final=True` F0 upwind-rate construction differs from the
iteration operator even with identical controls.

## 7. Frozen attribution rule (local contribution only)

- `STALE_RECORD_DOMINANT` (iff `||D_stale||_inf > ||D_rate||_inf`): **false**
  (`1.84e-5 > 488.10` is false);
- `FINAL_RATE_SEMANTICS_DOMINANT_OR_TIED` (iff `||D_rate||_inf >=
  ||D_stale||_inf`): **true**;
- `||R_final_current||_inf < ||R_final_stale||_inf`: **true**
  (490.7560414005864 < 490.7560425919994, by 1.19e-6).

Attribution is local at `V_*` only; it identifies the larger local
contribution to the accepted residual gap and does NOT declare either
diagnostic counterfactual to be the correct HJB convergence criterion.

## 8. Execution design, determinism, and forbidden-operation check

- exactly ONE deterministic reconstruction; ONE iteration-operator build; ONE
  stale-record `final=True` build; ONE current-record `final=True` build; ONE
  compact F0 provenance audit; ONE deterministic repeat — verified by build
  counting (exactly 3 `build_operator_and_u` calls at `V_*`; the stale build
  received `records_pre_step8` and the current build received
  `records_current`, provenance never swapped);
- deterministic repeat **bit-identical** (`deterministic_repeat_identical =
  true`);
- no trial value states; no Newton step; no policy-iteration / semismooth /
  trust-region / continuation; no line search; no accepted new HJB iterate
  (verified statically and by construction);
- no economics / prices / grid / domain / initialization / controls /
  tolerances / `PB_MARGIN` change; no accepted final-validation-semantics
  change in accepted source; no clip/floor of `p_b`;
- the household oracle, selected-Q source and the accepted Issue #61 / #62 /
  #63 / #64 implementations were imported read-only and are unchanged (six
  frozen blobs verified);
- non-finite / inconsistent evidence and provenance ambiguity fail closed
  (`F0ValidationSemanticsFailure` → Terminal C); no such failure occurred;
- builder allowlist respected: exactly the four Issue #65 paths
  (`f0_final_validation_semantics_audit.py`, its test, this report, and the
  summary CSV); no fifth tracked path.

## 9. Interpretation ceiling

This is local attribution at the single accepted Issue #63 stagnation state
with the frozen central selected-Q case. It does NOT prove that the accepted
`final=True` F0 validation operator is wrong as a convergence criterion (its
status is unchanged), does NOT prove that fresh-record re-validation would
fail at other states, does NOT prove the HJB fixed point does not exist, and
does NOT authorize KFE / stationary KFE. Terminal B records that the accepted
validation gap is dominated by the `final=True` F0 rate/discretization
semantics themselves — the accepted F0 final operator construction requires
review before its large residual is used as a design target for a successor
nonlinear solver.
