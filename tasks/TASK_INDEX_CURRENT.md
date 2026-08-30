# Deep Learning + HANK Task Index

Status: `ACTIVE_GITHUB_ISSUE_18__DLH_4B_ACCEPTED_TWO_ASSET_HA_IMPORT`

Last synchronized: 2026-08-30

Repository: `zcx369658780/deep-learning-hank`

## Sole active Builder authority

**GitHub Issue #18 — OPEN**

Title:

`DLH-4B: Import accepted MATLAB-faithful two-asset HA oracle as canonical household kernel`

Issue URL:

`https://github.com/zcx369658780/deep-learning-hank/issues/18`

Task nature:

`SCIENTIFIC_INTEGRATION__ACCEPTED_TWO_ASSET_HA_IMPORT`

Builder:

Codex bounded integrator.

Builder must fresh-read Issue #18 body/comments before mutation.

## Accepted source authority for Issue #18

Source repository:

`zcx369658780/dissertation-ch5-two-asset-hank`

Source file:

`exports/matlab_faithful_two_asset_ha.py`

Export authority recorded by source artifact:

`6469e5a87a00366c1b2af38f27efaa3014206936`

Transferred artifact SHA-256:

`276D2244B389D6EDE140DAF8B1F9B0BE1F4AA859368941CED1A12BA8A5831AB8`

Designated MATLAB source SHA-256:

`049136B769560040BC678F828F5D3EC5338DDCAA2090D6BED4E40732F56C3EAE`

Accepted source authorities include faithful HJB-operator parity, KFE-density parity, end-to-end stationary-distribution parity, and household-aggregate parity.

## Scientific state

The project no longer treats the earlier one-asset HANK validation route as the final household foundation.

Current target household foundation is the externally accepted MATLAB-faithful two-asset HA block with state space `(b,a,z)` and separate liquid/illiquid assets.

Issue #18 is an import/integration gate only. It does not authorize GE closure, dynamics, NK closure, regional NSR-HANK, Deep Learning training, calibration, policy claims, or paper Results.

## Historical provenance

- Issues #1–#6: accepted/closed under canonical evidence boundaries.
- Issue #7: accepted fail-closed boundary-sensitivity provenance.
- Issue #8: accepted fail-closed wide-domain grid-convergence provenance.
- Issue #9: accepted Tier-0 numerical robustness reference.
- Issue #10 / DLH-3A: accepted equation-consistency provenance for the earlier validation route.
- Issue #11 / DLH-3B: accepted one-asset structural-kernel provenance; historical validation only.
- Issue #12 / DLH-3C: accepted one-asset time-dependent household/KFE provenance; historical validation only.
- Issue #13: closed `not_planned` after scientific-route reassessment.
- Issue #14: closed `completed`; audit established one-asset vs MATLAB two-asset identity mismatch.
- Issue #15: closed `completed`; one-asset HA validation kernel retained as benchmark provenance, not final HANK household foundation.
- Issue #16: closed `completed`; Chinese one-asset review package retained as documentation provenance.
- Issue #17: closed `not_planned`; local two-asset reconstruction attempt superseded by the externally accepted MATLAB-faithful implementation.

## Required Builder startup

1. fresh-fetch live `origin/main`;
2. read CURRENT project rules;
3. read this Task Index;
4. read `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`;
5. fresh-read Issue #18 body + comments;
6. verify source repository/path/export authority and transferred file SHA before mutation;
7. fail closed on authority/hash mismatch.

Future successor work remains `NO_BUILDER_AUTHORITY` until separately issued.