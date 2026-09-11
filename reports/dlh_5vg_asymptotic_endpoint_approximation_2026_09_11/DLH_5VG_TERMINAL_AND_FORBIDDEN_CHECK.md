# DLH-5V-G — Terminal and Forbidden Check (Rev 1: bounded reanalysis of comment `5634957294`)

**Design only.** Finalize file for Issue #55 / DLH-5V-G after the reviewer-mandated bounded reanalysis.

## 1. Exactly one terminal — Outcome C

```text
DLH_5VG_ROUTE_A_ASYMPTOTIC_ENDPOINT_APPROXIMATION_OBSTRUCTION__OWNER_ROUTE_REDECISION_REQUIRED
```

**Rationale (bounded to this gate's evidence).** Reviewer comment `5634957294` found a genuine tangent-cone
graph-consistency counterexample to the submitted A1 contract. The bounded reanalysis confirms it and establishes that
no permitted Route-A contract can meet the exact Issue-#55 graph-consistency requirements:

1. **Counterexample confirmed (mandatory test):** `s_m = (0, i_t^m(0) - 2)` is non-W-active, `x_m -> (0, W_max)`
   (`W-dist = (r_0^m + theta_m + 14)/(19m) -> 0`), `mu = (0, +1)` is A1-admitted and exactly represented
   (`q_up = 19m/7`), yet `mu_W = +1 > 0` lies outside the true corner cone `{mu_a >= 0, mu_W <= 0}` — outer/limsup fails.
2. **Generalization:** every fixed-`j` cell `(j, i_t(j) - 2)` (including regular-region `j = 7, ...`) converges to
   `(0, W_max)`; the frozen accepted interior contract itself violates the global outer condition — not repairable by
   endpoint-layer-only changes without reopening the frozen regular block (forbidden). Same mechanism at
   `(a_max, W_max - a_max)`.
3. **Impossibility:** no per-state admissible-set rule (W-activity only; fixed row count; shrinking or fixed W-distance
   threshold) can satisfy both outer/limsup (all Family-C sequences, `W-dist -> 0`, `k = o(m)`) and recovery/liminf (all
   Family-F sequences, `W-dist -> c > 0`, `k ~ 7cm/19`) — the two families are indistinguishable per-state; every
   candidate rule fails one side.
4. **A2 cannot repair:** a first-moment defect does not change admissibility; the counterexample drift is exactly
   representable with zero defect, so no permitted A2 construction excludes it.

Hence A1 fails and no permitted Route-A contract meets the stated graph consistency requirements. The terminal is the
exact Outcome-C terminal. The finite-m algebra (rates, moments, scaling, monotonicity, conservation, one-Q) is retained
and remains internally coherent, but does not rescue the asymptotic theorem.

## 2. Reviewer items addressed

| Item | Addressed |
|---|---|
| 1. Mandatory counterexample `(0, i_t-2)`, `mu=(0,1)` | Confirmed exactly; added as controlling test (buffered-admissibility report §3.1) |
| 2. Reassess A1 under exact T3/T4; do not weaken silently | Done: outer/limsup and recovery/liminf both kept at full strength; A1 fails |
| 3. A1 variant + proof for all layer-state sequences (incl. growing rows, `W-dist -> 0`) | Attempted (W-activity, row-count, shrinking/fixed W-distance rules); all fail (impossibility table §3.3) |
| 4. A2 only if it can repair | A2 cannot repair the admissible-set failure (proved, §4); A2 not invoked |
| 5. Outcome-C terminal if no permitted Route-A contract | Returned (this file) |
| 6. DLH-5T corner semantics + interior-layer/corner taxonomy | Corrected (geometry report §6–§7; umbrella §6): `W_max > 8` `(a_max, b_min)` is `a_max x b_min` only (`{mu_a<=0, mu_b>=0}`); W active there only at `W_max = 8`; W-active lower-b cells vanish for `m > 69/(19(W_max-8))`; non-W-active bounded-`k` cells converge to corners, not face interiors |
| 7. Operator proof cleanup | Pure `C^2` integral-remainder bound; `M_3`/`C^3` phrasing removed (monotonicity/operator report §2) |
| 8. Floor-proof cleanup | F1/F2 rewritten with exact floor/ceiling inequalities (geometry report §5) |

## 3. Forbidden-operation check

| Forbidden | Done? |
|---|---|
| Household/economic source mutation | NO — household blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e` verified unchanged |
| Production grid/aspect/domain redesign | NO |
| State augmentation / ghost states | NO |
| Coordinate transformation | NO |
| Numerical production `W_max` | NO |
| Implementation / solver-source mutation | NO |
| Production-`Q` assembly/run | NO |
| HJB/KFE/stationary solve | NO — stationary KFE NOT AUTHORIZED |
| Full numerical experiment | NO — only tiny exact `%TEMP%` scripts (never committed) |
| Post-selection clipping | NO |
| Omitted destination with retained diagonal escape | NO |
| Reflection / interpolation / KFE-only mass routing | NO |
| Pinning/normalization leakage repair | NO |
| PR / merge / close / successor / self-accept | NO |
| Aggregates / GE / regional / neural / nominal / calibration / policy / welfare / Results | NO |

## 4. Exact changed paths (six-file allowlist, edited on the same dedicated branch)

1. `docs/design/DLH_5VG_SHRINKING_ENDPOINT_LAYER_ASYMPTOTIC_APPROXIMATION_CONTRACT.md`
2. `reports/dlh_5vg_asymptotic_endpoint_approximation_2026_09_11/DLH_5VG_AUTHORITY_CAPSULE.md`
3. `reports/dlh_5vg_asymptotic_endpoint_approximation_2026_09_11/DLH_5VG_FIXED_ASPECT_REFINEMENT_AND_LAYER_GEOMETRY.md`
4. `reports/dlh_5vg_asymptotic_endpoint_approximation_2026_09_11/DLH_5VG_BUFFERED_ADMISSIBILITY_AND_MOMENT_CONSISTENCY.md`
5. `reports/dlh_5vg_asymptotic_endpoint_approximation_2026_09_11/DLH_5VG_MONOTONICITY_CONSERVATION_SAME_Q_AND_OPERATOR_CONSISTENCY.md`
6. `reports/dlh_5vg_asymptotic_endpoint_approximation_2026_09_11/DLH_5VG_TERMINAL_AND_FORBIDDEN_CHECK.md`

No existing tracked file outside the allowlist is modified.

## 5. Fresh state report (recorded at completion)

- Fresh `origin/main` (FINAL CURRENT SYNC): `c8c5c3f8d3a002a7efcb93682ff42d50c3667602`
- Issue #55 state at completion: OPEN (re-verified)
- Task type: `SCIENTIFIC_DESIGN__SHRINKING_ENDPOINT_LAYER_ASYMPTOTIC_MARKOV_APPROXIMATION`
- Owner decision: `APPROVE_DLH_5VG_ROUTE_A_ASYMPTOTIC_ENDPOINT_APPROXIMATION_DESIGN_GATE`
- Activation comments: `5634144909` (+ `5634171277`); reviewer comment: `5634957294`
- Dedicated branch: `dsh/issue-55-dlh-5vg-asymptotic-endpoint-approximation-2026-09-11`
- Candidate commit SHA and ahead/behind: recorded in the completion comment on Issue #55
- Household blob: `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

## 6. Completion

Rev-1 candidate pushed to the dedicated branch; remote SHA verified equal to local SHA. STOPPED for fresh ChatGPT
review. No merge, no close, no successor, no self-accept.
