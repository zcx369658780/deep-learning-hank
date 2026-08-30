# Deep Learning + HANK Task Index

Status: `ACTIVE_GITHUB_ISSUE_23__DLH_4D_R3_MATLAB_TRANSFER_FOC_PARITY_REPAIR`

Last synchronized: 2026-08-30

Repository: `zcx369658780/deep-learning-hank`

## Sole active Builder authority

**GitHub Issue #23 — OPEN**

Title:

`DLH-4D-R3: Repair MATLAB-faithful transfer-FOC liquid-derivative semantics and revalidate frozen GE path`

Task type:

`SCIENTIFIC_REPAIR__MATLAB_FAITHFUL_TRANSFER_FOC_PARITY`

Builder:

DSH bounded scientific repair executor.

Issue URL:

`https://github.com/zcx369658780/deep-learning-hank/issues/23`

Builder must fresh-read Issue #23 body and all authoritative comments before execution.

## Accepted Issue #22 diagnosis

Issue #22 accepted commit:

`3e623160796ed175244703bb01ad40baa1b23749`

Accepted classification:

`DLH_4D_R2_NONFINITE_STAGE_MAP_COMPLETE_ACCEPTED`

Accepted stage map:

- 415/452 non-finite points fail in HJB at the Python transfer-FOC positivity guard;
- 37/452 reach a converged HJB and fail in the faithful contaminated-row KFE solve;
- no GE wrapper root cause was found.

## New source-level scientific blocker

Owner re-supplied the designated MATLAB household source after Issue #22.

`HANK_2ASSETS_HJB.m` SHA-256:

`049136B769560040BC678F828F5D3EC5338DDCAA2090D6BED4E40732F56C3EAE`

This exactly matches the designated MATLAB provenance embedded in the canonical Python oracle.

The MATLAB source floors `Vb` only for consumption/labor controls, while its four `HANK3_FOC` calls pass raw `VbB/VbF`; domestic `HANK3_FOC.m` evaluates `pa./pb` directly with no `pb>0` guard or derivative floor.

The canonical Python oracle currently adds a strict-positive raw-`v_b` transfer-FOC guard absent from MATLAB. This is now treated as a narrow MATLAB-faithfulness blocker requiring explicit repair before any fixture revision.

## Prior household immutability — narrow Owner override

Pre-repair canonical path:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Pre-repair Git blob:

`57e32076f0e11c9a047e1f90f8c2446d4148e457`

Pre-repair SHA-256:

`276D2244B389D6EDE140DAF8B1F9B0BE1F4AA859368941CED1A12BA8A5831AB8`

Issue #23 is the sole narrow exception to previous household immutability. It may alter only transfer-FOC handling of non-positive raw liquid derivatives to restore designated MATLAB semantics.

No other household equation, adjustment cost, bare-`a` scaling, taper, boundary/upwind rule, operator construction, KFE method, aggregation, Option A economics, fixture, or domain is authorized to change.

## Scientific ceiling

Issue #23 may establish only:

- repaired MATLAB-faithful transfer-FOC parity;
- updated non-finite-region evidence;
- and, if the unchanged frozen GE path passes all existing gates, the intended minimal single-region real GE validation fixture.

No authority for broader household redesign, KFE redesign, dynamics, NK, regional HANK, Deep Learning, calibration, welfare/policy, or Results.