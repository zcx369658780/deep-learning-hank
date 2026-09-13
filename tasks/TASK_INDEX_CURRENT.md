# Deep Learning + HANK Task Index

Status: `ISSUE_64_NEXT_ACTIVE__BUILDER_NOT_YET_OPERATIVE`

Last synchronized: 2026-09-13

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

**Issue #64 / DLH-5V-P is NEXT ACTIVE — BUILDER NOT YET OPERATIVE.** Builder
execution for Issue #64 becomes operative only after all three CURRENT
governance files are synchronized to Issue #64 (this file included), the
initial activation comment ID is recorded, and a final authoritative
activation-refresh comment confirms the post-sync live `main`.

Initial authoritative activation comment:

`5652648524`

Owner / Reviewer route decision:

`APPROVE_FTB_STAGNATION_RESIDUAL_DECOMPOSITION_AND_FROZEN_POLICY_NEWTON_GEOMETRY_AFTER_5VO_TERMINAL_B`

Authority marker:

`DLH_5VP_STAGNATION_NEWTON_GEOMETRY_DIAGNOSTIC_AUTHORIZED`

Task type:

`SCIENTIFIC_NUMERICAL_DIAGNOSTIC__FTB_STAGNATION_RESIDUAL_DECOMPOSITION_AND_FROZEN_POLICY_NEWTON_GEOMETRY`

Dedicated future Builder branch:

`dsh/issue-64-dlh-5vp-stagnation-newton-geometry-2026-09-13`

Issue #63 / DLH-5V-O remains ACCEPTED / CLOSED at Terminal B (controlling
accepted evidence for the FTB-stagnation state reconstructed by Issue #64).

## Next active task — Issue #64 / DLH-5V-P

Title:

`DLH-5V-P: Diagnose Issue #63 stagnation residual decomposition and frozen-policy Newton boundary geometry`

Task type:

`SCIENTIFIC_NUMERICAL_DIAGNOSTIC__FTB_STAGNATION_RESIDUAL_DECOMPOSITION_AND_FROZEN_POLICY_NEWTON_GEOMETRY`

Scientific question: at the accepted Issue #63 FTB-stagnation state, is the
obstruction mainly (1) a boundary-normal geometry problem that also makes a
frozen-policy Newton direction essentially unusable, or (2) a pseudo-time
direction problem, where a Newton-like frozen-policy direction has a
meaningful positive domain-safe step and materially reduces the re-selected
HJB residual? A second required question: why the accepted final-validation
residual (~490.756) is much larger than the iteration-operator residual scale
(~10.43) — decompose by F0 versus boundary rows and by iteration versus
final-validation operator semantics.

### Frozen scientific boundary (binding)

- reconstruct ONLY the accepted Issue #63 stagnation state: deterministic
  reconstruction of the accepted trajectory, STOP immediately after accepted
  FTB step 8, before any new HJB iterate is accepted; reproduce the final step
  statistic ≈ `3.6614352438846254e-08`, final min boundary
  `p_b ≈ 4.8089461301970005e-09`, wall state F3 (13,13), z=1, and the final
  accepted Bellman validation residual ≈ `490.7560425919994`;
- only: iteration-vs-final residual/operator decomposition (`R_iter =
  rho*V_* - [u_iter + Q_iter V_*]` vs `R_final = rho*V_* - [u_final +
  Q_final V_*]`); F0-vs-boundary residual decomposition; ONE frozen-policy
  Newton direction `J_iter d_N = -R_iter` with `J_iter = rho I - Q_iter`;
  ONE boundary-crossing calculation; exactly TWO diagnostic trial fractions
  (`alpha_half`, `alpha_near`); ONE deterministic repeat;
- frozen diagnostic constants: `PB_MARGIN=1e-12`, `EPS_ALPHA=1e-6`,
  `HALF_ALPHA=0.5`, `MATERIAL_REDUCTION_RATIO=0.50`;
- `alpha_near = min(1, (1-EPS_ALPHA)*alpha_cross)` if a finite positive
  crossing exists, otherwise `1`; `alpha_half = 0.5*alpha_near`; NO line
  search, NO alpha tuning, NO material-threshold tuning;
- trial states are diagnostic only — NOT accepted HJB iterates;
- no multi-step Newton / policy-iteration / semismooth / trust-region solver;
- no adaptive line search; no economics / prices / grid / domain / `PB_MARGIN`
  change; no Issue #63 controller change; no clip/floor of `p_b`;
- Stationary KFE remains **NOT AUTHORIZED**.

### Execution design and terminals

Execute exactly: ONE deterministic reconstruction of the accepted Issue #63
stagnation state; ONE residual/operator decomposition at `V_*`; ONE
frozen-policy Newton direction solve; ONE boundary-crossing calculation;
exactly TWO trial fractions; ONE deterministic repeat of the full diagnostic.
A trial is a material nonlinear residual reduction only if BOTH
`||R_reselect||_inf / ||R_iter||_inf <= 0.50` and
`||R_final_trial||_inf / ||R_final||_inf <= 0.50` (frozen ex ante diagnostic
threshold for this Issue, not a convergence criterion).

Exactly ONE terminal:

- A `DLH_5VP_STAGNATION_NEWTON_GEOMETRY__BOUNDARY_SAFE_NEWTON_DIRECTION_MATERIALLY_REDUCES_RESELECTED_RESIDUALS__NEWTON_TRUST_REGION_DESIGN_GATE_READY`
- B `DLH_5VP_STAGNATION_NEWTON_GEOMETRY__POSITIVE_BOUNDARY_SAFE_NEWTON_STEP_BUT_NONLINEAR_RESIDUAL_REDUCTION_INSUFFICIENT__FURTHER_DIRECTION_DESIGN_REQUIRED`
- C `DLH_5VP_STAGNATION_NEWTON_GEOMETRY__NONFINITE_INCONSISTENT_OR_NO_POSITIVE_BOUNDARY_SAFE_NEWTON_GEOMETRY__BOUNDARY_HJB_ROUTE_REVIEW_REQUIRED`
- Blocked `BLOCKED_DLH_5VP_AUTHORITY_OR_DEPENDENCY_CONFLICT`

### Builder allowlist (four new paths only)

1. `src/deep_learning_hank/two_asset/stagnation_newton_geometry.py`
2. `tests/test_dlh_5vp_stagnation_newton_geometry.py`
3. `reports/dlh_5vp_stagnation_newton_geometry_2026_09_13/DLH_5VP_STAGNATION_NEWTON_GEOMETRY_REPORT.md`
4. `reports/dlh_5vp_stagnation_newton_geometry_2026_09_13/DLH_5VP_NEWTON_GEOMETRY_SUMMARY.csv`

## Prior accepted task — Issue #63 / DLH-5V-O (ACCEPTED / CLOSED)

Issue #63 is CLOSED completed at Terminal B and remains the controlling
accepted evidence for the FTB-stagnation state reconstructed by Issue #64.

Accepted candidate / integration:

`a552dc6ebb2c82ad19fe26cd747d362ceecdfdcc`

Reviewer acceptance:

`5652576918`

Acceptance integration:

`5652579072`

Accepted verdict:

`DLH_5VO_ACCEPTED__TERMINAL_B_CONFIRMED__CONTINUOUS_FTB_PRESERVES_EFFECTIVE_DOMAIN_BUT_STAGNATES_AT_BOUNDARY_WITH_MATERIAL_BELLMAN_RESIDUAL__ROUTE_RECONSIDERATION_REQUIRED`

Accepted terminal:

`DLH_5VO_CONTINUOUS_FTB_RESOLVENT__EFFECTIVE_DOMAIN_PRESERVED_BUT_VALIDATED_HJB_CONVERGENCE_NOT_REACHED`

Accepted scientific interpretation (trajectory-bounded):

- the continuous FTB controller successfully preserves the effective domain on
  the frozen central selected-Q case;
- 8 accepted root-controlled FTB steps in total; cap-direct = 0,
  root-controlled = 8;
- the limiting wall state is locked to F3 (13,13), z=1 on the accepted path;
- selected delta and the boundary margin shrink approximately geometrically;
- final min boundary p_b ≈ 4.81e-9, still > `PB_MARGIN=1e-12`;
- the accepted-step trigger fired at iteration 8:
  `max|V_{n+1}-V_n| ≈ 3.66e-8 < 1e-7`;
- but the final re-selection / validation shows Bellman residual
  ≈ 490.756 >> 1e-3;
- the raw fixed-point direction norm stays ≈ 10.43-10.88 on the trajectory and
  does NOT approach 0;
- therefore the accepted interpretation is **FTB_STAGNATION**: a tiny step
  caused by boundary-following geometry, NOT validated HJB convergence;
- Q conservative, 0 artificial bindings, 0 optimizer expansions;
- deterministic repeat identical;
- the Issue #62 positive local safe radius is real but does NOT suffice for
  validated convergence under this frozen FTB controller;
- trajectory-bounded evidence only: does NOT prove that all FTB controllers
  globally fail to converge; does NOT prove the absence of another
  fixed-point-preserving direction/operator; does NOT prove the HJB fixed
  point does not exist; does NOT authorize KFE / stationary KFE.

Non-blocking metadata observation (recorded for CURRENT / roadmap wording):

- the candidate result field `converged=True` means only that the accepted-step
  statistic trigger was reached;
- scientific validated convergence = FALSE, because the final Bellman
  validation failed;
- CURRENT / roadmap must NOT phrase that field as HJB convergence;
- recommended wording:
  `step-size convergence trigger reached; validated HJB convergence failed (FTB_STAGNATION)`.

## Prior accepted task — Issue #62 / DLH-5V-N (ACCEPTED / CLOSED)

Issue #62 is CLOSED completed at Outcome A and remains the controlling
authority for the frozen central case and the local geometry facts.

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
- does NOT prove continuation convergence (and Issue #63 now confirms the FTB
  continuation stagnates at the boundary on the frozen central case).

## Prior accepted task — Issue #61 / DLH-5V-M (ACCEPTED / CLOSED)

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

## Prior accepted task — Issue #60 / DLH-5V-L (ACCEPTED / CLOSED)

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

Accepted selected-Q implementation remains immutable/read-only:

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

Accepted Issue #63 implementation remains read-only evidence:

`src/deep_learning_hank/two_asset/continuous_ftb_resolvent_hjb.py`

Git blob:

`746799509c517746ba6a321e5526c57a8f4698e4`

Binding law remains:

```text
HJB boundary policy <=> KFE boundary transition law
Q backward
future KFE exactly Q^T
Q_ij>=0 for i!=j
Q_ii=-sum of ACTUAL represented outgoing rates
Q1=0 by construction
same selected candidate/rates for HJB and future KFE
```

Stationary KFE remains **NOT AUTHORIZED**.

## Hard ceiling

Issue #64 / DLH-5V-P is the authorized local diagnostic scope only: exactly
ONE frozen-policy Newton direction on the frozen iteration operator and exactly
TWO diagnostic trial fractions (`alpha_half`, `alpha_near`); trial states are
diagnostic only and NOT accepted HJB iterates. A multi-step Newton /
policy-iteration / semismooth / trust-region solver, an adaptive line search,
alpha / material-threshold tuning, further delta-shrinking or `TAU_FTB`
tuning, a continuous continuation variant, an extension of any delta ladder as
an experiment, and any new price / grid / margin experiments remain **NOT
AUTHORIZED** without a further Owner/ChatGPT scientific design and a new
authorized Issue. No KFE/stationary KFE, no SCC/global-Q, no GE/multi-region/
neural/nominal/calibration/policy/welfare/Results work.

## Current governance files

- `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
- `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
- Issue #64 body/comments (next active; initial activation `5652648524`).
- Issue #63 body/comments (accepted/closed).
