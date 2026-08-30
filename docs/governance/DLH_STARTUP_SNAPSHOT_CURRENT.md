# Deep Learning + HANK Startup Snapshot — CURRENT

Date: 2026-08-30

Repository: `zcx369658780/deep-learning-hank`

Local Owner-designated workspace: `D:\deep-learning-hank`

## Governance state

- live GitHub `main` = synchronized repository/governance authority;
- active GitHub Issue pointed to by `tasks/TASK_INDEX_CURRENT.md` = sole Builder authority;
- DSH = bounded Builder/executor;
- ChatGPT = independent fresh-GitHub reviewer / scientific-route authority / task issuer / GitHub governance operator;
- Owner = final scientific-direction authority;
- Builder completion is not acceptance.

Priority:

`Scientific correctness > Experiment reproducibility > Research iteration speed > Git auditability > Documentation completeness`

## Active Builder task

`ACTIVE_GITHUB_ISSUE_23__DLH_4D_R3_MATLAB_TRANSFER_FOC_PARITY_REPAIR`

Issue #23:

`DLH-4D-R3: Repair MATLAB-faithful transfer-FOC liquid-derivative semantics and revalidate frozen GE path`

Task type:

`SCIENTIFIC_REPAIR__MATLAB_FAITHFUL_TRANSFER_FOC_PARITY`

Builder:

DSH bounded scientific repair executor.

## Accepted two-asset household foundation — pre-repair identity

Canonical implementation:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Pre-repair Git blob:

`57e32076f0e11c9a047e1f90f8c2446d4148e457`

Pre-repair SHA-256:

`276D2244B389D6EDE140DAF8B1F9B0BE1F4AA859368941CED1A12BA8A5831AB8`

This remains the accepted household foundation except for the single narrow MATLAB-faithfulness repair explicitly authorized by Issue #23.

## Accepted Option A GE contract

Issue #19 contract commit:

`7fcfd6412c580f888d2ef8175335c3909f146e59`

Option A economics remain unchanged.

## Accepted GE blocker evidence

Issue #20 implementation commit:

`40ec7ee3d676fc03863a3d2c2b1722b7ad53b2a5`

Accepted classification:

`DLH_4D_ROOT_BRACKET_FAILURE_ACCEPTED_AS_BLOCKER_EVIDENCE__GE_NONEXISTENCE_NOT_YET_CERTIFIED`

Issue #21 diagnostic commit:

`a6187c31d7a1f008e94718778030c3117b6edae7`

Accepted classification:

`DLH_4D_R1_DIAGNOSTIC_INCONCLUSIVE_ACCEPTED__NONFINITE_REGION_REQUIRES_DIAGNOSTIC`

Issue #22 diagnostic commit:

`3e623160796ed175244703bb01ad40baa1b23749`

Accepted classification:

`DLH_4D_R2_NONFINITE_STAGE_MAP_COMPLETE_ACCEPTED`

Accepted Issue #22 stage map:

- 415/452 non-finite points fail at the Python transfer-FOC positivity guard;
- 37/452 reach converged HJB and fail at faithful contaminated-row KFE;
- Phase A classification is exactly reproducible.

## New source-level finding after Issue #22

Owner re-supplied the designated MATLAB household files.

Designated `HANK_2ASSETS_HJB.m` SHA-256:

`049136B769560040BC678F828F5D3EC5338DDCAA2090D6BED4E40732F56C3EAE`

This exactly matches the MATLAB provenance embedded in the canonical Python oracle.

The MATLAB source uses `max(Vb,1e-6)` for consumption and labor but passes raw `VbB/VbF` into all four transfer FOC calls. Domestic `HANK3_FOC.m` computes `pa./pb` directly and has no strict-positive `pb` guard or derivative floor.

The current Python canonical oracle has extra `v_b>0` transfer-FOC guards. These guards are now a narrow scientific/fidelity blocker rather than an accepted numerical-regularization feature.

## Explicit narrow household-repair authority

Issue #23 overrides prior household immutability only for this exact source-proven transfer-FOC mismatch.

Authorized scientific change:

- remove the Python-only strict-positive raw-liquid-derivative requirement from the transfer FOC;
- preserve raw `v_a/v_b` MATLAB semantics for the transfer candidate;
- retain the `1e-6` derivative floor only for consumption/labor as MATLAB does.

Still frozen:

- economic structure;
- `max(a,a_bar)` adjustment-cost floor;
- bare-`a` FOC scaling;
- illiquid-return taper;
- boundary/upwind policy selection except purely mechanical compatibility needed by the narrow repair;
- source-operator construction;
- contaminated-row KFE;
- aggregation;
- Option A GE economics;
- Issue #20 fixture and solver domains.

## Current scientific objective

1. establish source-to-source parity evidence;
2. implement the narrow faithful transfer-FOC repair;
3. run focused parity/regression tests;
4. reclassify the prior 452 non-finite candidates on the unchanged frozen grid;
5. rerun the existing frozen Issue #20 GE solve unchanged.

No PASS-seeking parameter or fixture changes are permitted.

## Current scientific ceiling

Not yet established:

`MINIMAL_SINGLE_REGION_TWO_ASSET_REAL_GE_STEADY_STATE_VALIDATED`

Issue #23 may establish only repaired transfer-FOC MATLAB fidelity, updated non-finite evidence, and—only if all unchanged gates pass—the minimal single-region real GE fixture.

Not authorized:

- broader household redesign;
- KFE redesign;
- transition dynamics / IRFs;
- NK monetary closure;
- regional HANK;
- learned `W^L` / `W^K`;
- Deep Learning training;
- empirical calibration;
- policy/welfare/paper Results.

## Required Builder startup

1. fresh fetch live `origin/main`;
2. read CURRENT project rules;
3. read `tasks/TASK_INDEX_CURRENT.md`;
4. read this Startup Snapshot;
5. read accepted Issues #20-#22 evidence;
6. verify pre-repair oracle identity;
7. fresh-read Issue #23 body + all comments;
8. fail closed on authority/source-parity mismatch.