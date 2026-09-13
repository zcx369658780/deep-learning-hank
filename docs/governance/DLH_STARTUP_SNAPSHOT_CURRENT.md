# Deep Learning + HANK Startup Snapshot — CURRENT

Date: 2026-09-13

Repository: `zcx369658780/deep-learning-hank`

Local Owner-designated workspace: `D:\deep-learning-hank`

## Governance state

- live GitHub `main` = synchronized repository/code/governance authority;
- open GitHub Issue = sole DSH Builder task authority only after publication + CURRENT synchronization + authoritative activation comments;
- DSH = bounded Builder/scientific analyst only under an active Issue;
- ChatGPT = independent reviewer / scientific-route advisor / task issuer / governance operator;
- Owner = final scientific authority;
- Builder completion is not acceptance.

Priority:

`Scientific correctness > Experiment reproducibility > Research iteration speed > Git auditability > Documentation completeness`

## Current Builder state

**Issue #63 / DLH-5V-O is NEXT ACTIVE — BUILDER NOT YET OPERATIVE.** Builder
execution for Issue #63 becomes operative only after all three CURRENT
governance files are synchronized to Issue #63 (this file included) and a final
authoritative activation-refresh comment confirms the post-sync live `main`.

Initial authoritative activation comment:

`5652277509`

Route decision:

`APPROVE_CONTINUOUS_FRACTION_TO_BOUNDARY_RESOLVENT_CONTINUATION_AFTER_5VN_OUTCOME_A`

Dedicated future Builder branch:

`dsh/issue-63-dlh-5vo-continuous-ftb-resolvent-2026-09-13`

## Next active gate — Issue #63 / DLH-5V-O

Title:

`DLH-5V-O: Test continuous fraction-to-boundary pseudo-transient continuation on the frozen central selected-Q HJB case`

Task type:

`SCIENTIFIC_NUMERICAL_DIAGNOSTIC__CONTINUOUS_FRACTION_TO_BOUNDARY_RESOLVENT_CONTINUATION`

Scientific question: can a fixed-point-preserving pseudo-transient resolvent
iteration converge on the single frozen central selected-Q HJB case when each
accepted step is chosen by a continuous fraction-to-boundary rule rather than
by a pre-truncated discrete delta ladder? First authorized multi-step
continuation test after Issue #62 established a positive local safe radius.

### Frozen scientific boundary

- single frozen central selected-Q case, exactly the accepted Issue #61/#62
  configuration and initialization (unchanged parameters/prices/grid/domain/
  tolerances/`PB_MARGIN=1e-12`);
- continuous fraction-to-boundary pseudo-transient controller ONLY per Issue
  #63 frozen rules;
- at every accepted iterate `V_n`, `Q_n,u_n` built exactly once and reused for
  ALL delta/controller evaluations within that iterate (no policy re-selection
  as delta varies); trial solves only
  `[I + delta*(rho I - Q_n)] V_n(delta) = V_n + delta*u_n`;
- controller constants frozen: `DELTA_CAP=1000`, `TAU_FTB=0.90`,
  `RETAIN=0.10`, `EPS_FTB=1e-6`, `MAX_BRACKET_HALVINGS=60`;
- `m0 = min_required_boundary p_b(V_n) - PB_MARGIN` (require finite `m0 > 0`);
  `m_target = RETAIN*m0`; `h_n(delta) = min_required_boundary p_b(V_n(delta))
  - PB_MARGIN - m_target`; cap accepted directly when finite `h_n(DELTA_CAP)
  >= 0`; otherwise deterministic halving `1000, 500, 250, ...` is BRACKET
  CONSTRUCTION ONLY (not an accepted ladder; no probe accepted merely because
  feasible) until the first sign-changing bracket, then deterministic `brentq`
  on `h_n = 0`; `delta_selected = (1 - EPS_FTB)*delta_ftb`; directly verify
  finite `p_b`, `min p_b > PB_MARGIN`, retained margin `>= m_target`; accept
  `V_{n+1} = V_n(delta_selected)` directly — NO value damping;
- Bellman residual never used for step selection;
- no controller-parameter tuning after seeing results;
- no economics/prices/grid/domain/`PB_MARGIN` change; no value damping; no
  clip/floor of `p_b`;
- Stationary KFE remains **NOT AUTHORIZED**.

### Execution design and terminals

Exactly ONE continuation run + ONE deterministic repeat. Convergence trigger
`max|V_{n+1}-V_n| < 1e-7`; final validation requires all required boundary
`p_b > 1e-12`, `||rho V - [u_selected(V)+Q_selected(V)V]||_inf <= 1e-3`,
conservative Q, no artificial bracket binding, deterministic repeat. Step
criterion without final Bellman PASS = `FTB_STAGNATION` (not convergence);
1000 accepted iterations without validated convergence = bounded
non-convergence; no finite feasible bracket within 60 halvings or non-finite
required evidence = `FTB_STEP_CONSTRUCTION_FAILURE` and STOP (fail closed).

Exactly ONE terminal:

- A `DLH_5VO_CONTINUOUS_FTB_RESOLVENT__CENTRAL_HJB_CONVERGES_WITH_FINAL_BELLMAN_PASS__ROBUSTNESS_GATE_READY`
- B `DLH_5VO_CONTINUOUS_FTB_RESOLVENT__EFFECTIVE_DOMAIN_PRESERVED_BUT_VALIDATED_HJB_CONVERGENCE_NOT_REACHED`
- C `DLH_5VO_CONTINUOUS_FTB_RESOLVENT__NO_VIABLE_FRACTION_TO_BOUNDARY_STEP__BOUNDARY_HJB_ROUTE_REVIEW_REQUIRED`
- Blocked `BLOCKED_DLH_5VO_AUTHORITY_OR_DEPENDENCY_CONFLICT`

### Builder allowlist (four new paths only)

1. `src/deep_learning_hank/two_asset/continuous_ftb_resolvent_hjb.py`
2. `tests/test_dlh_5vo_continuous_ftb_resolvent.py`
3. `reports/dlh_5vo_continuous_ftb_resolvent_2026_09_13/DLH_5VO_CONTINUOUS_FTB_RESOLVENT_REPORT.md`
4. `reports/dlh_5vo_continuous_ftb_resolvent_2026_09_13/DLH_5VO_CONTINUATION_TRACE.csv`

## Prior accepted gate — Issue #62 / DLH-5V-N (ACCEPTED / CLOSED)

Issue #62 is CLOSED completed at Outcome A and remains the controlling
authority for the frozen central case and local geometry facts.

Accepted candidate / integration:

`7ba2d75978033064c588230b15d760b60bec9e00`

Reviewer acceptance:

`5652208157`

Acceptance integration:

`5652209372`

Accepted verdict:

`DLH_5VN_ACCEPTED__OUTCOME_A_CONFIRMED__POSITIVE_SUBFLOOR_LOCAL_SAFE_STEP_AND_REPRODUCIBLE_MARGIN_CROSSING__CONTINUATION_DESIGN_GATE_READY`

Accepted terminal:

`DLH_5VN_LOCAL_RESOLVENT_GEOMETRY__POSITIVE_SUBFLOOR_SAFE_STEP_AND_REPRODUCIBLE_MARGIN_CROSSING__CONTINUATION_DESIGN_GATE_READY`

Accepted local facts (trajectory-bounded / local evidence only):

- Issue #61 terminal event is authorized ladder-floor exhaustion;
- frozen Issue #61 terminal operator has a strictly positive sub-floor safe delta;
- continuous margin crossing reproducible in `[0, 1000*2^-20]`;
- `delta_cross ≈ 7.8246e-4` (~0.8205 of the old floor);
- first-order prediction `delta_margin_linear ≈ 7.5943e-4` (ratio ≈ 1.0303);
- root/below/above limiting state is F3 (13,13), z=1;
- corrected directional accounting: 186 required boundary states, 105
  negative-direction, 40 `i == 0` V-independent states with exact zero
  directional derivative;
- R1 true fail-closed non-finite handling is part of the accepted
  implementation;
- does NOT prove continuation convergence.

## Prior accepted gate — Issue #61 / DLH-5V-M (ACCEPTED / CLOSED)

Issue #61 is CLOSED completed at Terminal C.

Accepted candidate / integration:

`2721dadbfd0ad49813f12c8424f6be77fcaf3f85`

Reviewer acceptance:

`5651495744`

Acceptance integration:

`5651496951`

Accepted verdict:

`DLH_5VM_ACCEPTED__TERMINAL_C_CONFIRMED__ADAPTIVE_RESOLVENT_LADDER_EXHAUSTED_ON_FROZEN_CENTRAL_TRAJECTORY__ROUTE_RECONSIDERATION_REQUIRED`

Accepted terminal:

`DLH_5VM_ADAPTIVE_RESOLVENT__NO_VIABLE_EFFECTIVE_DOMAIN_RESOLVENT_STEP__ROUTE_RECONSIDERATION_REQUIRED`

## Prior accepted gate — Issue #60 / DLH-5V-L (ACCEPTED / CLOSED)

Issue #60 is CLOSED completed at Terminal C.

Accepted candidate / integration:

`9b1538feabe2cc4634653721e725ee3e46d449bb`

Reviewer acceptance:

`5650057012`

Acceptance integration:

`5650059195`

Accepted verdict:

`DLH_5VL_ACCEPTED__TERMINAL_C_CONFIRMED__VALUE_UPDATE_ONLY_INVARIANT_SAFEGUARD_FAILS_ON_FROZEN_CENTRAL_TRAJECTORY__RAW_OPERATOR_ROUTE_RECONSIDERATION_REQUIRED`

## Frozen household / same-process authority

Accepted household oracle remains immutable/read-only:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Accepted selected-Q source remains immutable/read-only:

`src/deep_learning_hank/two_asset/boundary_hjb_selected_q.py`

Git blob:

`7ea342ccbe15d852b90743b14bb4b02977c2d78b`

Accepted Issue #61 implementation remains read-only evidence:

`src/deep_learning_hank/two_asset/adaptive_resolvent_hjb.py`

Git blob:

`043e146ef499e985a49d256c4cec2f397f93e4e1`

Accepted Issue #62 local-geometry implementation remains read-only evidence:

`src/deep_learning_hank/two_asset/local_resolvent_domain_geometry.py`

Git blob:

`cb6533475d0ba115e6f52bd73e61aeb85c9b6ea7`

```text
HJB boundary policy <=> KFE boundary transition law
Q backward
future KFE exactly Q^T
Q_ij>=0 for i!=j
Q_ii=-sum of ACTUAL represented outgoing rates
Q1=0 by construction
same selected candidate/rates for HJB and future KFE
```

Pinning/normalization may never repair leakage.

Stationary KFE remains **NOT AUTHORIZED**.

## Interpretation ceiling

Until Issue #63 is operative (final activation-refresh confirms post-sync
`main`): no Builder scientific branch creation, no Issue #63 continuation
execution, no successor, no PR / merge / Issue close / self-accept. Beyond the
Issue #63 allowlist, nothing may start before Owner/ChatGPT scientific design
and a new authorized Issue.

## Current authoritative files

- `tasks/TASK_INDEX_CURRENT.md`
- `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
- Issue #63 body/comments (authoritative).
