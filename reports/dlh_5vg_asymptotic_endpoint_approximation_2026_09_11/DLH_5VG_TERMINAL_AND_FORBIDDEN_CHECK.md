# DLH-5V-G — Terminal and Forbidden Check

**Design only.** Finalize file for Issue #55 / DLH-5V-G.

## 1. Exactly one terminal — Outcome A

```text
DLH_5VG_ROUTE_A_SHRINKING_ENDPOINT_LAYER_ASYMPTOTIC_SAME_PROCESS_CONTRACT_FROZEN__READY_FOR_BOUNDARY_HJB_IMPLEMENTATION_GATE
```

**Rationale (bounded to this gate's evidence).** A1 — the shrinking numerical candidate-admissibility buffer applied
before scoring — passes: the consistency theorem T1–T8 (umbrella §4) is proved at the design level for the whole
frozen fixed-aspect refinement family (`m >= 1`, Regime I):

- every A1-admitted endpoint candidate has an exact represented native-grid first-moment contract (no moment defect);
- endpoint physical width `ell_m = 70/(19m) = O(1/m) -> 0`, uniformly in frontier phase;
- the accepted exact regular contract is recovered pointwise away from the true endpoints;
- outer/limsup and recovery/liminf tangent-cone consistency (with equality of cones at the limit points);
- jump `O(1/m)`, rate `O(m)`, `sum q |jump|^2 = O(1/m)` — proved with explicit constants, not assumed;
- generator/operator consistency for smooth test functions (`O(1/m)` numerical diffusion);
- nonnegative off-diagonals, `Q_ss = -sum of actual outgoing rates`, `Q_m 1 = 0`;
- ONE selected backward `Q_m`; future KFE consumes exactly `Q_m^T`;
- regular/endpoint seam consistency (identical formulas on common candidates; buffer restriction equals the true
  tangent cone at the limit).

A2 (explicit moment defect) is not invoked, per Issue §5.5 ("do not use A2 if A1 already establishes a coherent
asymptotically consistent contract"). No pointwise `O(1/m)` moment defect is claimed anywhere; all admitted candidates
carry exact first moments.

## 2. Forbidden-operation check

| Forbidden | Done? |
|---|---|
| Household/economic source mutation | NO — household blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e` verified unchanged |
| Production grid/aspect/domain redesign | NO — family analyzed as frozen, not redesigned |
| State augmentation / ghost states | NO |
| Coordinate transformation | NO |
| Numerical production `W_max` | NO — `W_max` stays symbolic |
| Implementation / solver-source mutation | NO |
| Production-`Q` assembly/run | NO |
| HJB/KFE/stationary solve | NO — stationary KFE NOT AUTHORIZED |
| Full numerical experiment | NO — only tiny exact `%TEMP%` scripts (never committed) |
| Post-selection clipping | NO — buffer applied before scoring only |
| Omitted destination with retained diagonal escape | NO |
| Reflection / interpolation / KFE-only mass routing | NO |
| Pinning/normalization leakage repair | NO |
| PR / merge / close / successor / self-accept | NO |
| Aggregates / GE / regional / neural / nominal / calibration / policy / welfare / Results | NO |

## 3. Exact changed paths (six-file allowlist, all new files)

1. `docs/design/DLH_5VG_SHRINKING_ENDPOINT_LAYER_ASYMPTOTIC_APPROXIMATION_CONTRACT.md`
2. `reports/dlh_5vg_asymptotic_endpoint_approximation_2026_09_11/DLH_5VG_AUTHORITY_CAPSULE.md`
3. `reports/dlh_5vg_asymptotic_endpoint_approximation_2026_09_11/DLH_5VG_FIXED_ASPECT_REFINEMENT_AND_LAYER_GEOMETRY.md`
4. `reports/dlh_5vg_asymptotic_endpoint_approximation_2026_09_11/DLH_5VG_BUFFERED_ADMISSIBILITY_AND_MOMENT_CONSISTENCY.md`
5. `reports/dlh_5vg_asymptotic_endpoint_approximation_2026_09_11/DLH_5VG_MONOTONICITY_CONSERVATION_SAME_Q_AND_OPERATOR_CONSISTENCY.md`
6. `reports/dlh_5vg_asymptotic_endpoint_approximation_2026_09_11/DLH_5VG_TERMINAL_AND_FORBIDDEN_CHECK.md`

No existing tracked file is modified.

## 4. Fresh state report (recorded at completion)

- Fresh `origin/main` (FINAL CURRENT SYNC, activation refresh `5634171277`): `c8c5c3f8d3a002a7efcb93682ff42d50c3667602`
- Issue #55 state at completion: OPEN (re-verified before push)
- Task type: `SCIENTIFIC_DESIGN__SHRINKING_ENDPOINT_LAYER_ASYMPTOTIC_MARKOV_APPROXIMATION`
- Owner decision: `APPROVE_DLH_5VG_ROUTE_A_ASYMPTOTIC_ENDPOINT_APPROXIMATION_DESIGN_GATE`
- Activation comments: `5634144909` (authoritative) + `5634171277` (refresh)
- Dedicated branch: `dsh/issue-55-dlh-5vg-asymptotic-endpoint-approximation-2026-09-11`
- Candidate commit SHA and ahead/behind: recorded in the completion comment on Issue #55
- Household blob: `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

## 5. Completion

Candidate pushed to the dedicated branch; remote SHA verified equal to local SHA. STOPPED for fresh ChatGPT review.
No merge, no close, no successor, no self-accept.
