# Deep Learning + HANK Task Index

Status: `NO_ACTIVE_BUILDER_TASK__DLH_4B_TWO_ASSET_HA_IMPORT_ACCEPTED`

Last synchronized: 2026-08-30

Repository: `zcx369658780/deep-learning-hank`

## Current Builder authority

There is **no active Builder task** after acceptance of Issue #18.

Future scientific or implementation work remains `NO_BUILDER_AUTHORITY` until ChatGPT publishes and activates a separate GitHub Issue.

## Most recent accepted task

GitHub Issue #18:

`DLH-4B: Import accepted MATLAB-faithful two-asset HA oracle as canonical household kernel`

Accepted candidate commit:

`24dde6792f6800f1ae872001587c2a1a3503d919`

Accepted classification:

`DLH_4B_ACCEPTED_TWO_ASSET_HA_IMPORT_ACCEPTED`

The accepted canonical household file is:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Its Git blob identity matches the source-repository export exactly:

`57e32076f0e11c9a047e1f90f8c2446d4148e457`

Required SHA-256 provenance:

`276D2244B389D6EDE140DAF8B1F9B0BE1F4AA859368941CED1A12BA8A5831AB8`

## Current scientific state

The canonical household foundation is now the accepted MATLAB-faithful two-asset HA block with state `(b,a,z)`, separate liquid/illiquid assets, HJB, stationary KFE, and household aggregates.

Maintain the distinction between:

- `ECONOMIC_STRUCTURE`; and
- `NUMERICAL_REGULARIZATION / MATLAB_FAITHFUL_IMPLEMENTATION`.

The bare-`a` production transfer FOC pairing, the `max(a,a_bar)` adjustment-cost floor, the illiquid-return taper, exact MATLAB-spdiags-equivalent boundary behavior, and contaminated-row KFE are preserved for faithful numerical parity. They must not all be reinterpreted as primitive economic equations.

The earlier one-asset HA/HANK route remains benchmark provenance only, not the canonical future HANK household foundation.

## Historical provenance

- Issues #1–#12: retained under their accepted evidence ceilings.
- Issue #13: closed `not_planned` after scientific-route reassessment.
- Issue #14: completed identity/parity audit.
- Issue #15: completed one-asset validation kernel; benchmark provenance only.
- Issue #16: completed one-asset review package; documentation provenance only.
- Issue #17: closed/superseded failed local two-asset reconstruction; not scientific authority.
- Issue #18: accepted canonical two-asset HA import.

## Scientific ceiling after Issue #18

Accepted now:

`TWO_ASSET_HA_HOUSEHOLD_HJB_KFE_AGGREGATE_FOUNDATION`

Not yet accepted or authorized:

- two-asset GE closure;
- transition dynamics / IRFs;
- NK monetary closure;
- regional NSR-HANK;
- Deep Learning architecture/training;
- empirical calibration;
- welfare/policy/Results claims.
