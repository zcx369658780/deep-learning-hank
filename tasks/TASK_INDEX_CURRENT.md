# Deep Learning + HANK Task Index

Status: `ISSUE_67_DLH_5VS_NEXT_ACTIVE__BUILDER_NOT_YET_OPERATIVE`

Last synchronized: 2026-09-15

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

Issue #67 / DLH-5V-S is **NEXT ACTIVE — BUILDER NOT YET OPERATIVE**.

Title:

`DLH-5V-S: Minimal repair of final=True F0 z-block destination assembly and corrected validation re-check`

Task type:

`SCIENTIFIC_CHANGE__MINIMAL_FINAL_VALIDATION_OPERATOR_REPAIR_AND_REVALIDATION`

Owner / Reviewer route decision:

`APPROVE_MINIMAL_FINAL_VALIDATION_ZBLOCK_DESTINATION_REPAIR_AFTER_5VR_TERMINAL_A`

Authority marker:

`DLH_5VS_MINIMAL_FINAL_VALIDATION_ZBLOCK_REPAIR_AUTHORIZED`

Initial authoritative activation:

`5672573849`

Final authoritative activation-refresh: **NOT YET PUBLISHED**. Until that
refresh confirms the post-sync live `main`, Builder execution is
**NOT YET OPERATIVE**.

Dedicated future Builder branch:

`dsh/issue-67-dlh-5vs-final-validation-zblock-repair-2026-09-15`

Owner explicit authorization (2026-09-15, recorded in Issue #67):

> `同意 Issue #67 按最小 validation-operator repair 路线执行。`

## Owner-authorized exact scientific change (Issue #67)

Only authorized source modification:

`src/deep_learning_hank/two_asset/boundary_hjb_selected_q.py`

Within the `final=True` F0 off-diagonal destination assembly, from:

`cols.append(dn)`

to:

`cols.append(nz * self.n + dn)`

Scientific meaning: repair **only** the z-block destination index, so that z=1
F0 off-diagonal destinations stay inside the z=1 block, aligned with the
accepted iteration path / boundary path / MATLAB-faithful state layout.

Never changed by this Issue:

- raw drift calculation;
- `max(±mu)/step` final rate formulas;
- continuous controls;
- policy selection;
- diagonal construction;
- switch-matrix assembly;
- economics, prices, grid/domain, initialization;
- tolerances, `PB_MARGIN`;
- convergence criterion;
- accepted iteration semantics.

Boundary of the authorized work: repair + corrected validation re-check only.
The Bellman tolerance remains the unchanged acceptance threshold, and a
materially lower corrected residual must **NOT** be interpreted as HJB
convergence.

Issue #67 exact four-path Builder allowlist:

1. `src/deep_learning_hank/two_asset/boundary_hjb_selected_q.py`;
2. `tests/test_dlh_5vs_final_validation_zblock_repair.py`;
3. `reports/dlh_5vs_final_validation_zblock_repair_2026_09_15/DLH_5VS_FINAL_VALIDATION_ZBLOCK_REPAIR_REPORT.md`;
4. `reports/dlh_5vs_final_validation_zblock_repair_2026_09_15/DLH_5VS_FINAL_VALIDATION_ZBLOCK_REPAIR_SUMMARY.csv`.

No fifth tracked Builder path. No PR / merge / Issue close / successor /
self-accept.

Issue #67 terminal set (exactly ONE to be reported):

- A `DLH_5VS_FINAL_VALIDATION_ZBLOCK_REPAIR__CORRECTED_FINAL_OPERATOR_MATCHES_MATLAB_FAITHFUL_LAYOUT__SPURIOUS_CROSS_Z_VALIDATION_GAP_REMOVED__HJB_RESIDUAL_REASSESSMENT_GATE_READY`
- B `DLH_5VS_FINAL_VALIDATION_ZBLOCK_REPAIR__ZBLOCK_ASSEMBLY_REPAIRED_BUT_MATERIAL_HJB_VALIDATION_DISCREPANCY_REMAINS__FURTHER_VALIDATION_REVIEW_REQUIRED`
- C `DLH_5VS_FINAL_VALIDATION_ZBLOCK_REPAIR__NONFINITE_INCONSISTENT_OR_REGRESSION_FAILURE__SCIENTIFIC_REPAIR_REVIEW_REQUIRED`
- Blocked `BLOCKED_DLH_5VS_AUTHORITY_OR_DEPENDENCY_CONFLICT`

Explicitly NOT authorized in this Issue:

- convergence-criterion replacement;
- `R_iter` becoming an accepted final convergence residual;
- accepting any new HJB iterate;
- Newton / policy iteration / semismooth / trust-region / continuation / line
  search;
- price / Wmax / resolution sweeps;
- KFE / stationary KFE / steady state;
- SCC/global-Q; GE / multi-region / neural / nominal / calibration / policy /
  welfare / Results;
- successor Issue activation;
- any Builder scientific branch beyond the dedicated Issue #67 branch named
  above (not yet created).

Issue #65 / DLH-5V-Q is ACCEPTED / CLOSED at Terminal B and remains the
controlling accepted evidence for the F0 `final=True` rate/discretization
operator dominance audited by Issue #66. Issue #66 / DLH-5V-R is ACCEPTED /
CLOSED at Terminal A (see below) and establishes the concrete accepted
validation-operator assembly defect / provenance mismatch that Issue #67 is
now explicitly authorized by the Owner to repair minimally.

## Superseded accepted task — Issue #66 / DLH-5V-R (ACCEPTED / CLOSED)

Issue #66 is CLOSED completed at Terminal A and establishes the concrete
accepted validation-operator assembly defect / provenance mismatch that
requires an Owner decision before any source repair.

Accepted candidate / integration:

`a31f17e6d965ddfe8214cd1b83d4074833310625`

Reviewer acceptance:

`5666168154`

Acceptance integration:

`5666172248`

Accepted verdict:

`DLH_5VR_ACCEPTED__TERMINAL_A_CONFIRMED__ITERATION_OPERATOR_IS_MATLAB_FAITHFUL__FINAL_TRUE_F0_ROW_ASSEMBLY_DROPS_Z_BLOCK_OFFSET_FOR_Z1__VALIDATION_OPERATOR_SCIENTIFIC_REPAIR_OWNER_GATE_REQUIRED`

Accepted terminal:

`DLH_5VR_F0_FINAL_RATE_PROVENANCE__ITERATION_OPERATOR_MATCHES_ACCEPTED_MATLAB_FAITHFUL_HJB__FINAL_RAW_RATE_OPERATOR_NON_EQUIVALENT__VALIDATION_OPERATOR_REDESIGN_REVIEW_GATE_READY`

Accepted facts (at the same frozen stagnation state `V_*`):

- `ITER_EQ_MATLAB = true`;
- `FINAL_EQ_MATLAB = false`;
- `BOTH_EQUIVALENT = false`;
- `MIXED_OR_UNRESOLVED = false`;
- F0 directional rate formulas coincide within machine tolerance;
- utility/source terms identical;
- non-F0 boundary rows identical;
- destination assembly is the material discrepancy;
- 298 z=1 F0 rows affected;
- rowwise max operator gap = `24.601971766296664`;
- accepted `final=True` F0 off-diagonal path uses bare `dn`;
- accepted iteration and boundary paths use `nz*n + dn`;
- therefore z=1 `final=True` F0 destinations are incorrectly placed in the
  z=0 block.

Accepted scientific interpretation (trajectory-bounded / local attribution
only):

- the accepted iteration operator is the MATLAB-faithful iteration operator;
- the accepted FINAL-RAW row's rate formulas equal the accepted oracle
  post-convergence formula, but its assembled row is not the MATLAB-faithful
  discrete HJB row because the z-block destination offset is dropped for z=1
  rows;
- no conclusion yet that the convergence criterion itself should change;
- correction of accepted `final=True` source semantics required explicit Owner
  authorization — the Owner granted exactly that authorization on 2026-09-15
  through Issue #67 / DLH-5V-S, limited to the minimal z-block destination
  repair described above;
- `R_iter` is NOT declared an accepted final convergence residual;
- does NOT prove the HJB fixed point does not exist;
- the next route is `OWNER SCIENTIFIC DECISION REQUIRED — MINIMAL
  FINAL-VALIDATION OPERATOR REPAIR` — subsequently granted by the Owner on
  2026-09-15 through Issue #67 / DLH-5V-S;
- Stationary KFE remains **NOT AUTHORIZED**.

## Prior accepted task — Issue #65 / DLH-5V-Q (ACCEPTED / CLOSED)

Issue #65 is CLOSED completed at Terminal B and remains the controlling
accepted evidence for the F0 `final=True` rate/discretization operator
dominance audited by Issue #66.

Accepted candidate / integration:

`44cb7bda1a040cacfc94fa45cda689755daa5a4e`

Reviewer acceptance:

`5656806015`

Acceptance integration:

`5656807180`

Accepted verdict:

`DLH_5VQ_ACCEPTED__TERMINAL_B_CONFIRMED__FINAL_TRUE_F0_RATE_SEMANTICS_DOMINATE_ACCEPTED_VALIDATION_GAP__STALE_RECORD_EFFECT_NEGLIGIBLE__F0_FINAL_OPERATOR_PROVENANCE_REVIEW_REQUIRED`

Accepted terminal:

`DLH_5VQ_F0_FINAL_VALIDATION_SEMANTICS__FINAL_RATE_SEMANTICS_DOMINATE_OR_TIE_ACCEPTED_VALIDATION_GAP__F0_FINAL_OPERATOR_REVIEW_REQUIRED`

Accepted facts (at the same frozen stagnation state `V_*`):

- `||R_iter||_inf = 10.435094313164921`;
- `||R_final_stale||_inf = 490.7560425919994`;
- `||R_final_current||_inf = 490.7560414005864`;
- `||D_total||_inf = 488.0988429898615`;
- `||D_stale||_inf = 1.8406872158038823e-05`;
- `||D_rate||_inf = 488.0988417984485`;
- `D_total = D_stale + D_rate` with additive error `0.0`;
- `D_total` / `D_stale` / `D_rate` non-F0 boundary contribution is exactly
  `0` for all three;
- 596 F0 rows: changed sector/transfer label = 0, but continuous controls are
  NOT identical;
- max |Δ consumption| = `1.2570318563831506e-08`;
- max |Δ labor| = `3.527538039449496e-09`;
- max |Δ transfer| = `2.0576147896633756e-07`;
- max |Δ mu_a| = `2.0576147896633756e-07`;
- max |Δ mu_b| = `4.029644697922663e-07`;
- max |Δ utility| = `1.088601719878568e-08`;
- rowwise max |`Q_final_stale` - `Q_final_current`| ≈ `1.4847075143e-06`;
- rowwise max |`Q_final_current` - `Q_iter`| ≈ `24.6019717663`.

Accepted scientific interpretation (trajectory-bounded / local attribution
only):

- stale F0 records contribute negligibly to the ~490.756 accepted
  final-validation gap;
- a record refresh cannot eliminate that gap;
- the accepted `final=True` F0 rate/discretization semantics are the dominant
  source of the gap;
- the conclusion is local attribution at the fixed `V_*` only;
- neither `R_iter`, `R_final_current`, nor any other counterfactual is
  declared to already be the correct convergence criterion;
- does NOT prove the HJB fixed point does not exist;
- the next step must audit the provenance/equivalence of the `final=True` F0
  rate construction against the MATLAB-faithful iteration / discrete HJB
  operator;
- Stationary KFE remains **NOT AUTHORIZED**.

## Prior accepted task — Issue #64 / DLH-5V-P (ACCEPTED / CLOSED)

Issue #64 is CLOSED completed at Terminal B and remains the controlling
accepted evidence for the F0 final-validation semantic gap audited by Issue
#65.

Accepted candidate / integration:

`5db144a65796ff6a7e0f59d2d2a75a0446c13b83`

Reviewer acceptance:

`5653190792`

Acceptance integration:

`5653192646`

Accepted verdict:

`DLH_5VP_ACCEPTED__TERMINAL_B_CONFIRMED__F0_FINAL_SEMANTICS_DOMINATE_VALIDATION_GAP__FROZEN_POLICY_NEWTON_IS_BOUNDARY_SAFE_BUT_GEOMETRICALLY_CAPPED_AND_NONLINEAR_RESIDUAL_REDUCTION_INSUFFICIENT__FURTHER_DIRECTION_DESIGN_REQUIRED`

Accepted terminal:

`DLH_5VP_STAGNATION_NEWTON_GEOMETRY__POSITIVE_BOUNDARY_SAFE_NEWTON_STEP_BUT_NONLINEAR_RESIDUAL_REDUCTION_INSUFFICIENT__FURTHER_DIRECTION_DESIGN_REQUIRED`

Accepted scientific interpretation (trajectory-bounded / local evidence only):

- the accepted Issue #63 stagnation state is reconstructed exactly (8
  root-controlled FTB steps; final step statistic ≈
  `3.6614352438846254e-08`; final min boundary `p_b ≈
  4.8089461301970005e-09`; wall state F3 (13,13), z=1; accepted
  final-validation residual ≈ `490.7560425919994`);
- `||R_iter||_inf = 10.435094313164921`;
- accepted `||R_final_stale||_inf = 490.7560425919994`;
- `||R_final_stale - R_iter||_inf = 488.0988429898615`;
- the residual difference is entirely on F0 rows; non-F0 boundary-row
  difference is exactly zero;
- frozen-policy Newton solve is finite/correct
  (`||J_iter d_N + R_iter||_inf ≈ 6.96e-11`);
- `alpha_cross ≈ 1.8667384893e-4`; limiting state remains F3 (13,13), z=1;
- `alpha_half` / `alpha_near` both strictly domain-safe;
- authorized trials yield iteration/final residual ratios ≈ 0.9998–0.9999;
- dual material-reduction threshold 0.50 not met;
- plain frozen-policy Newton direction therefore not a viable local
  residual-reducing route under this wall geometry;
- does NOT prove HJB fixed point nonexistence or failure of future
  constrained/tangent directions;
- sector-switch count 0 must not be interpreted as proof continuous controls
  unchanged;
- Stationary KFE remains **NOT AUTHORIZED**.

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

Accepted selected-Q implementation — the ONLY accepted scientific source that
Issue #67 / DLH-5V-S is authorized to modify, and then only at the single
`final=True` F0 off-diagonal destination-index location:

`src/deep_learning_hank/two_asset/boundary_hjb_selected_q.py`

Pre-repair accepted Git blob (frozen authority for Issue #67):

`7ea342ccbe15d852b90743b14bb4b02977c2d78b`

The pre-repair blob above is the frozen comparison authority; Issue #67 must
record the repaired blob and demonstrate that the source diff is exactly the
authorized destination-column repair.

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

Accepted Issue #64 implementation remains read-only evidence:

`src/deep_learning_hank/two_asset/stagnation_newton_geometry.py`

Git blob:

`3ca2371c7da1939d1fed55df5728baefb27d8aa7`

Accepted Issue #65 implementation remains read-only evidence:

`src/deep_learning_hank/two_asset/f0_final_validation_semantics_audit.py`

Git blob:

`bb4045378bf19607f68d7d4a7628b3431afcd676`

Accepted Issue #66 implementation remains read-only evidence:

`src/deep_learning_hank/two_asset/f0_final_rate_provenance_audit.py`

Git blob:

`44d47c7545f279dfe9189736f5cdcdfa30c3b84b`

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

**ISSUE #67 / DLH-5V-S IS NEXT ACTIVE — BUILDER NOT YET OPERATIVE.** Issue #66 /
DLH-5V-R is ACCEPTED / CLOSED at Terminal A. The Owner has authorized the
minimal final-validation z-block destination repair through Issue #67 (initial
authoritative activation `5672573849`; authority marker
`DLH_5VS_MINIMAL_FINAL_VALIDATION_ZBLOCK_REPAIR_AUTHORIZED`), but Builder
execution remains NOT YET OPERATIVE until the final authoritative
activation-refresh confirms the post-sync live `main`.

The authorized scientific-change ceiling is exactly one destination-index
repair in `src/deep_learning_hank/two_asset/boundary_hjb_selected_q.py`
(`cols.append(dn)` → `cols.append(nz * self.n + dn)` in the `final=True` F0
off-diagonal path), plus the corrected validation re-check, within the exact
four-path allowlist above. Explicitly NOT authorized: any second source line
change; final rate formula / controls / policy selection / diagonal / switch
matrix / economics / prices / grid / domain / initialization / tolerances /
`PB_MARGIN` / convergence-criterion change; `R_iter` becoming an accepted final
convergence residual; accepting any new HJB iterate; declaring HJB convergence
because the corrected residual drops (the Bellman tolerance is unchanged);
Newton / continuation / line search / parameter sweep; KFE / stationary KFE /
steady state; SCC/global-Q; GE/multi-region/neural/nominal/calibration/policy/
welfare/Results; successor Issue activation; any Builder scientific branch
beyond the dedicated Issue #67 branch (not yet created); PR / merge / Issue
close / self-accept. Stationary KFE remains **NOT AUTHORIZED**.

## Current governance files

- `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
- `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
- Issue #67 body/comments (OPEN; initial authoritative activation `5672573849`;
  final authoritative activation-refresh not yet published).
- Issue #66 body/comments (accepted/closed; reviewer acceptance `5666168154`,
  acceptance integration `5666172248`).
- Issue #65 body/comments (accepted/closed).
- Issue #64 body/comments (accepted/closed).
- Issue #63 body/comments (accepted/closed).
