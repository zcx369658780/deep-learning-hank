# Deep Learning + HANK Startup Snapshot — CURRENT

Date: 2026-08-30

Repository: `zcx369658780/deep-learning-hank`

Local Owner-designated workspace: `D:\deep-learning-hank`

## Governance state

- live GitHub `main` = synchronized repository/governance authority;
- the open GitHub Issue pointed to by `tasks/TASK_INDEX_CURRENT.md` = sole Builder task authority;
- Codex/DSH = bounded Builder according to the active Issue;
- ChatGPT = independent fresh-GitHub reviewer / scientific-route authority / task issuer / GitHub governance operator;
- Owner = final scientific-direction authority;
- Builder completion is not acceptance;
- correct fail-closed results remain scientific evidence;
- metadata mismatch is a governance blocker, not automatically a scientific blocker.

Priority:

`Scientific correctness > Experiment reproducibility > Research iteration speed > Git auditability > Documentation completeness`

## Current active task

`ACTIVE_GITHUB_ISSUE_18__DLH_4B_ACCEPTED_TWO_ASSET_HA_IMPORT`

Active Builder authority:

**GitHub Issue #18 — OPEN**

Title:

`DLH-4B: Import accepted MATLAB-faithful two-asset HA oracle as canonical household kernel`

Task type:

`SCIENTIFIC_INTEGRATION__ACCEPTED_TWO_ASSET_HA_IMPORT`

Builder:

Codex bounded integrator.

## Current scientific stage

Current model stage:

`TWO_ASSET_HA_FOUNDATION__ACCEPTED_EXTERNAL_IMPLEMENTATION_PENDING_REPOSITORY_INTEGRATION`

Current experiment stage:

`TRANSFER_INTEGRATION_VALIDATION`

Current manuscript stage:

`NO_RESULTS_AUTHORITY`

## Accepted two-asset household authority

Source repository:

`zcx369658780/dissertation-ch5-two-asset-hank`

Accepted standalone source:

`exports/matlab_faithful_two_asset_ha.py`

Export authority recorded by source artifact:

`6469e5a87a00366c1b2af38f27efaa3014206936`

Transferred artifact SHA-256:

`276D2244B389D6EDE140DAF8B1F9B0BE1F4AA859368941CED1A12BA8A5831AB8`

Designated MATLAB source:

`HANK_2ASSETS_HJB.m`

MATLAB SHA-256:

`049136B769560040BC678F828F5D3EC5338DDCAA2090D6BED4E40732F56C3EAE`

Accepted household evidence includes:

- MATLAB-faithful HJB propagation/operator parity;
- MATLAB↔Python faithful HJB operator parity;
- MATLAB↔Python faithful KFE density parity;
- end-to-end stationary-distribution parity;
- household aggregate parity.

The accepted standalone implementation is a household numerical baseline/oracle. GE closure and dynamics are excluded.

## Scientific identity of the canonical household foundation

The canonical target is a MATLAB-faithful two-asset HA household block with:

- state space `(b,a,z)`;
- liquid asset `b`;
- illiquid asset `a`;
- deposit/transfer control `d`;
- adjustment cost;
- MATLAB-faithful illiquid-return taper;
- exact MATLAB-spdiags-equivalent iteration-operator boundary semantics;
- separate post-convergence operator;
- contaminated-row stationary KFE;
- aggregate consumption, effective labor, illiquid assets, and liquid assets.

The earlier one-asset route remains useful benchmark provenance but is not the final household foundation for future HANK/NSR-HANK work.

## Historical route correction

- Issue #13: closed after the previous single-region NK GE route was superseded by household-foundation reassessment.
- Issue #14: completed audit; established one-asset vs two-asset identity mismatch.
- Issue #15: completed one-asset validation kernel; benchmark only.
- Issue #16: completed one-asset Chinese review package; documentation only.
- Issue #17: closed/superseded local two-asset reconstruction attempt; not scientific authority.

## Issue #18 scientific boundary

Authorized:

- import the accepted standalone two-asset household artifact;
- establish canonical `src/deep_learning_hank/two_asset/` package;
- add minimal import plumbing and transfer-validation tests;
- deprecate/replace conflicting live-main two-asset code only if such code actually exists.

Not authorized:

- changing accepted household economics/numerics;
- GE closure;
- HANK transition dynamics;
- NK/monetary shocks;
- regional flow networks;
- Deep Learning architecture/training;
- calibration/data work;
- policy/welfare/Results claims.

## Required Builder startup order

1. fresh fetch live `origin/main`;
2. read CURRENT rules;
3. read `tasks/TASK_INDEX_CURRENT.md`;
4. read this snapshot;
5. fresh-read Issue #18 body + comments;
6. inspect the accepted source repository export task and source file;
7. verify source SHA-256 exactly before mutation;
8. stop fail-closed on any authority/hash mismatch.

Future successor tasks remain unauthorized until separately issued.