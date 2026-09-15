# Deep Learning + HANK Task Index

Status: `ISSUE_69_DLH_5VU_NEXT_ACTIVE__BUILDER_NOT_YET_OPERATIVE`

Last synchronized: 2026-09-15

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

Issue #69 / DLH-5V-U is **NEXT ACTIVE — BUILDER NOT YET OPERATIVE**.

Title:

`DLH-5V-U: Audit latent F0 iteration-rate vs raw-drift sign divergence away from V*`

Task type:

`SCIENTIFIC_NUMERICAL_DIAGNOSTIC__F0_ITERATION_RATE_VS_RAW_DRIFT_SIGN_PROVENANCE_AWAY_FROM_VSTAR`

Owner / Reviewer route decision:

`APPROVE_F0_ITERATION_RATE_VS_RAW_DRIFT_SIGN_PROVENANCE_AUDIT_AFTER_5VT_TERMINAL_C`

Authority marker:

`DLH_5VU_F0_RATE_PATH_DIVERGENCE_AUDIT_AUTHORIZED`

Initial authoritative activation:

`5676828795`

Final authoritative activation-refresh: **NOT YET PUBLISHED**. Until that
refresh confirms the post-sync live `main`, Builder execution is
**NOT YET OPERATIVE**.

Dedicated future Builder branch:

`dsh/issue-69-dlh-5vu-f0-rate-path-divergence-2026-09-15`

## Issue #69 frozen scientific boundary (as activated)

Only the two accepted Issue #68 frozen trial states may be used:

- `alpha_half = 0.08085341880193442`;
- `alpha_near = 0.16170683760386884`.

Must reproduce the accepted Issue #68 operator inconsistencies:

- `alpha_half`: F0 rowwise gap `0.6718037653783657`, inconsistent rows
  `{452, 453}`;
- `alpha_near`: F0 rowwise gap `1.3379411925537439`, inconsistent rows
  `{452, 453, 482, 483}`.

No third trial state.

At each frozen trial, exactly:

1. ONE `final=False` nonlinear policy re-selection;
2. ONE corrected `final=True` same-control build;
3. ONE all-F0 compact rate/row decomposition.

Must persist per inconsistent F0 row: state `(node, j, i, z)`; selected
sector / transfer label; consumption / labor / transfer / utility; stored
`mu_a`, `mu_b`; recomputed raw `mu_a`, `mu_b`; iteration `b_backward`,
`b_forward`, `a_backward`, `a_forward` rates; raw-drift `b_backward`,
`b_forward`, `a_backward`, `a_forward` rates; rate sign / active direction per
axis; diagonal; represented destination columns and rates; omitted destination
rate; rowwise `Q_final - Q_iter` non-zero columns and magnitudes. Plus
counts/maxima over ALL F0 rows. No full sparse matrices persisted.

Read-only source provenance trace required (not inferred from names or
docstrings): iteration b-rate construction; iteration a-rate construction;
finite-difference branch logic; shadow-rate / transfer / truncation semantics;
raw-drift recomputation; `max(±mu)/step` mapping; the exact local condition
causing the upwind sign flip.

Frozen diagnostic flags:

- `ITER_RATE_PATH_SOURCE_BACKED`;
- `FINAL_RAW_PATH_SOURCE_BACKED`;
- `RATE_FORMULAS_GLOBALLY_EQUIVALENT`;
- `SIGN_OR_BRANCH_DIVERGENCE_ESTABLISHED`;
- `TRUNCATION_OR_DESTINATION_DIVERGENCE_ESTABLISHED`;
- `OTHER_MECHANISM_ESTABLISHED`;
- `MIXED_OR_UNRESOLVED`.

Issue #69 exact four-path Builder allowlist:

1. `src/deep_learning_hank/two_asset/f0_rate_path_divergence_audit.py`;
2. `tests/test_dlh_5vu_f0_rate_path_divergence.py`;
3. `reports/dlh_5vu_f0_rate_path_divergence_2026_09_15/DLH_5VU_F0_RATE_PATH_DIVERGENCE_REPORT.md`;
4. `reports/dlh_5vu_f0_rate_path_divergence_2026_09_15/DLH_5VU_F0_RATE_PATH_DIVERGENCE_SUMMARY.csv`.

No fifth tracked Builder path. No PR / merge / Issue close / successor /
self-accept.

Issue #69 terminal set (exactly ONE to be reported):

- A `DLH_5VU_F0_RATE_PATH_DIVERGENCE__UNIQUE_SIGN_OR_BRANCH_MECHANISM_ESTABLISHED_AND_FULLY_ACCOUNTS_FOR_TRIAL_OPERATOR_GAPS__RATE_SEMANTICS_SCIENTIFIC_REVIEW_GATE_READY`
- B `DLH_5VU_F0_RATE_PATH_DIVERGENCE__UNIQUE_TRUNCATION_OR_DESTINATION_MECHANISM_ESTABLISHED_AND_FULLY_ACCOUNTS_FOR_TRIAL_OPERATOR_GAPS__RATE_SEMANTICS_SCIENTIFIC_REVIEW_GATE_READY`
- C `DLH_5VU_F0_RATE_PATH_DIVERGENCE__MIXED_OR_UNRESOLVED_SOURCE_PROVENANCE__OWNER_SCIENTIFIC_REVIEW_REQUIRED`
- Blocked `BLOCKED_DLH_5VU_AUTHORITY_OR_DEPENDENCY_CONFLICT`

Explicitly NOT authorized in this Issue:

- mutating selected-Q, the oracle, or any accepted Issue #61–#68 scientific
  source;
- choosing or replacing the authoritative rate path;
- changing the convergence criterion;
- changing economics / prices / grid / domain / initialization / controls /
  tolerances / `PB_MARGIN` / Bellman tolerance;
- accepting any trial as an HJB iterate;
- constructing a new Newton / tangent / constrained direction;
- multi-step Newton / policy iteration / semismooth / trust-region /
  continuation / line search;
- adding trial states or alpha tuning;
- price / Wmax / resolution sweeps;
- KFE / stationary KFE / `solve_household_steady_state`;
- SCC/global-Q; GE / multi-region / neural / nominal / calibration / policy /
  welfare / Results;
- successor Issue activation;
- any Builder scientific branch beyond the dedicated Issue #69 branch named
  above (not yet created).

## Accepted task — Issue #68 / DLH-5V-T (ACCEPTED / CLOSED)

Issue #68 is CLOSED completed at Terminal C. It diagnosed single-wall
tangent-projected frozen-policy Newton geometry at the accepted post-repair
`V_*`, and its Reviewer-authorized gradient-semantics remediation made the full
two-entry chain-rule wall gradient the controlling construction.

Accepted candidate / integration:

`15083e5c9f089406aa69326bc84dbe2db0e42be8`

Reviewer acceptance:

`5676811925`

Acceptance integration:

`5676816068`

Original scientific candidate / remediation commit:

`b194eb3886af7a5e3d5abe85dad114fdc6ed98eb` /
`15083e5c9f089406aa69326bc84dbe2db0e42be8` (fast-forward, not a merge commit)

Accepted verdict:

`DLH_5VT_ACCEPTED__TERMINAL_C_CONFIRMED__FULL_CHAIN_RULE_TANGENT_GEOMETRY_EXPANDS_SAFE_FRACTION_MATERIALLY__TRIAL_LEVEL_FINAL_VS_ITERATION_RATE_PATH_DIVERGENCE_INVALIDATES_CLEAN_RESIDUAL_CONTRACT__RATE_PATH_PROVENANCE_REVIEW_REQUIRED`

Accepted terminal:

`DLH_5VT_TANGENT_PROJECTED_NEWTON__NONFINITE_INCONSISTENT_OR_NO_POSITIVE_SAFE_TANGENT_GEOMETRY__BOUNDARY_HJB_ROUTE_REVIEW_REQUIRED`

Accepted facts:

- controlling wall gradient = full two-entry chain rule;
- `g[wall] = +1/db`, `g[down] = -1/db`, basis identity error = `0`;
- `alpha_cross_T = 0.16170699931086815`;
- `alpha_near = 0.16170683760386884`, `alpha_half = 0.08085341880193442`;
- geometry ratio = `866.2532997045214`;
- both trials domain-safe;
- indicative residual ratios: `alpha_half = 0.9193283517706523`,
  `alpha_near = 0.8390465254310803`;
- these ratios are **NOT** clean contractual residual evidence because corrected
  `final=True` and `final=False` become inconsistent under the SAME controls;
- `alpha_half`: F0 operator gap `0.6718037653783657`, inconsistent rows
  `{452, 453}`;
- `alpha_near`: F0 operator gap `1.3379411925537439`, inconsistent rows
  `{452, 453, 482, 483}`;
- controls / utility bit-identical across the two operator constructions at the
  affected rows;
- selected-Q repaired blob remains `556ccc214f03a1a22306cc4f5c7e9f7691bbf897`;
- at accepted `V_*` the two rate paths agree to machine precision, so the
  divergence is latent and appears only away from `V_*`.

Accepted scientific interpretation (binding):

- the single-wall full-gradient tangent projection **does** relax the
  first-order wall geometry by ~`866`×;
- the clean nonlinear residual experiment is invalidated at those larger steps
  because the accepted `final=False` iteration-rate path and the corrected
  `final=True` raw-drift rate path diverge under identical controls near an
  upwind sign boundary;
- this does **NOT** establish which rate path is scientifically correct away
  from `V_*`, does **NOT** authorize mutating either path, and does **NOT**
  establish HJB nonexistence or convergence failure;
- **no HJB convergence**; **no accepted new iterate**;
- Stationary KFE remains **NOT AUTHORIZED**.

## Superseded accepted task — Issue #67 / DLH-5V-S (ACCEPTED / CLOSED)

Issue #67 is CLOSED completed at Terminal A. It performed the minimal
Owner-authorized `final=True` F0 z-block destination repair and a corrected
validation re-check, followed by a Reviewer-authorized bounded post-repair
test-contract migration.

Accepted candidate / integration:

`a5753bb9fa329a3d85a5652b03d101fa0be6cd32`

Reviewer acceptance:

`5674741491`

Acceptance integration:

`5674743972`

Original scientific candidate / remediation commit:

`281cfe01b2925364a92308ca172a84a724c6ea58` /
`a5753bb9fa329a3d85a5652b03d101fa0be6cd32` (fast-forward, not a merge commit)

Accepted verdict:

`DLH_5VS_ACCEPTED__TERMINAL_A_CONFIRMED__MINIMAL_ZBLOCK_DESTINATION_REPAIR_EXACT__CORRECTED_FINAL_OPERATOR_MATCHES_MATLAB_FAITHFUL_LAYOUT__FULL_SUITE_GREEN__HJB_RESIDUAL_REASSESSMENT_REQUIRED`

Accepted terminal:

`DLH_5VS_FINAL_VALIDATION_ZBLOCK_REPAIR__CORRECTED_FINAL_OPERATOR_MATCHES_MATLAB_FAITHFUL_LAYOUT__SPURIOUS_CROSS_Z_VALIDATION_GAP_REMOVED__HJB_RESIDUAL_REASSESSMENT_GATE_READY`

Accepted facts (at the frozen stagnation state `V_*`):

- selected-Q repaired blob = `556ccc214f03a1a22306cc4f5c7e9f7691bbf897`;
- the exact scientific source repair remains only
  `cols.append(dn)` → `cols.append(nz * self.n + dn)`;
- corrected final residual = `10.435094313164921`;
- accepted `R_iter` = `10.435094313164921`;
- corrected-final vs ITER rowwise operator gap = `1.4210854715202004e-14`;
- historical pre-repair current final residual = `490.7560414005864`;
- historical pre-repair operator gap = `24.601971766296664`;
- ~`480.32` excess residual attributed to the cross-z destination-index defect;
- z=0 unchanged;
- non-F0 boundary `Q`/`u` diff = `0`;
- utility/source diff = `0`;
- conservativity preserved;
- expansions = `0`;
- artificial bindings = `0`;
- historical Issue #64/#65/#66 test constants preserved;
- post-repair runtime contracts migrated;
- full suite = **534 passed / 0 failed / 6 pre-existing warnings**.

Accepted scientific interpretation (binding):

- **HJB convergence = FALSE**;
- Bellman tolerance remains `1e-3`;
- the corrected residual is ~`10435`× the tolerance;
- `R_iter` is **NOT** declared the accepted final convergence residual;
- the genuine post-repair HJB residual reassessment remains outstanding;
- Stationary KFE remains **NOT AUTHORIZED**.

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

Accepted selected-Q implementation — repaired and accepted under Issue #67 /
DLH-5V-S; now **read-only** for all subsequent Issues (including Issues #68 and
#69):

`src/deep_learning_hank/two_asset/boundary_hjb_selected_q.py`

Accepted (repaired) Git blob:

`556ccc214f03a1a22306cc4f5c7e9f7691bbf897`

Historical pre-repair Git blob (retained as the accepted Issue #64–#66
comparison authority; not a live target):

`7ea342ccbe15d852b90743b14bb4b02977c2d78b`

The accepted scientific source change is and remains exactly the one
Owner-authorized z-block destination-index repair
`cols.append(dn)` → `cols.append(nz * self.n + dn)`. No later Issue is
authorized to mutate this file.

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

Accepted Issue #67 deliverable implementation/test/report paths remain
read-only evidence:

- `src/deep_learning_hank/two_asset/boundary_hjb_selected_q.py` (repaired;
  blob `556ccc214f03a1a22306cc4f5c7e9f7691bbf897`);
- `tests/test_dlh_5vs_final_validation_zblock_repair.py`;
- `tests/test_dlh_5vp_stagnation_newton_geometry.py` (migrated contracts);
- `tests/test_dlh_5vq_f0_final_validation_semantics_audit.py` (migrated
  contracts);
- `tests/test_dlh_5vr_f0_final_rate_provenance.py` (migrated contracts);
- `reports/dlh_5vs_final_validation_zblock_repair_2026_09_15/DLH_5VS_FINAL_VALIDATION_ZBLOCK_REPAIR_REPORT.md`;
- `reports/dlh_5vs_final_validation_zblock_repair_2026_09_15/DLH_5VS_FINAL_VALIDATION_ZBLOCK_REPAIR_SUMMARY.csv`.

Accepted Issue #68 deliverable paths remain read-only evidence:

- `src/deep_learning_hank/two_asset/tangent_projected_newton_geometry.py`;
- `tests/test_dlh_5vt_tangent_projected_newton_geometry.py`;
- `reports/dlh_5vt_tangent_projected_newton_geometry_2026_09_15/DLH_5VT_TANGENT_PROJECTED_NEWTON_GEOMETRY_REPORT.md`;
- `reports/dlh_5vt_tangent_projected_newton_geometry_2026_09_15/DLH_5VT_TANGENT_PROJECTED_NEWTON_GEOMETRY_SUMMARY.csv`.

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

**ISSUE #69 / DLH-5V-U IS NEXT ACTIVE — BUILDER NOT YET OPERATIVE.** Issue #68 /
DLH-5V-T is ACCEPTED / CLOSED at Terminal C and integrated to `main` at
`15083e5c9f089406aa69326bc84dbe2db0e42be8`. Issue #69 is a bounded
diagnostic/provenance audit of the latent F0 divergence between the accepted
`final=False` iteration-rate path and the corrected `final=True` raw-drift rate
path (initial authoritative activation `5676828795`; authority marker
`DLH_5VU_F0_RATE_PATH_DIVERGENCE_AUDIT_AUTHORIZED`), but Builder execution
remains NOT YET OPERATIVE until the final authoritative activation-refresh
confirms the post-sync live `main`.

The Issue #69 ceiling is exactly: ONE deterministic reconstruction of `V_*` plus
the accepted Issue #68 full-gradient tangent geometry; exactly TWO frozen trial
states (`alpha_half`, `alpha_near`) with no third trial; at each trial exactly
ONE `final=False` re-selection and ONE corrected `final=True` same-control
build; ONE all-F0 compact rate/row decomposition per trial; ONE read-only source
provenance mapping; ONE deterministic repeat — within the exact four-path
allowlist above. Explicitly NOT authorized: mutating selected-Q, the oracle, or
any accepted Issue #61–#68 scientific source; choosing or replacing the
authoritative rate path; convergence-criterion change; economics / prices /
grid / domain / initialization / controls / tolerances / `PB_MARGIN` / Bellman
tolerance change; accepting any trial as an HJB iterate; constructing a new
Newton / tangent / constrained direction; multi-step Newton / policy iteration /
semismooth / trust-region / continuation / line search; adding trial states or
alpha tuning; price / Wmax / resolution sweeps; KFE / stationary KFE /
`solve_household_steady_state`; SCC/global-Q; GE/multi-region/neural/nominal/
calibration/policy/welfare/Results; successor Issue activation; any Builder
scientific branch beyond the dedicated Issue #69 branch (not yet created);
PR / merge / Issue close / self-accept. Stationary KFE remains **NOT
AUTHORIZED**.

## Current governance files

- `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
- `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
- Issue #69 body/comments (OPEN; initial authoritative activation `5676828795`;
  final authoritative activation-refresh not yet published).
- Issue #68 body/comments (accepted/closed; reviewer acceptance `5676811925`,
  acceptance integration `5676816068`).
- Issue #67 body/comments (accepted/closed; reviewer acceptance `5674741491`,
  acceptance integration `5674743972`).
- Issue #66 body/comments (accepted/closed; reviewer acceptance `5666168154`,
  acceptance integration `5666172248`).
- Issue #65 body/comments (accepted/closed).
- Issue #64 body/comments (accepted/closed).
- Issue #63 body/comments (accepted/closed).
