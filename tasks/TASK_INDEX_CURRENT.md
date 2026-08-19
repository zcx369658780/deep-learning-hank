# Deep Learning + HANK Task Index

Status: `NO_ACTIVE_GITHUB_ISSUE__DLH_3_NOT_YET_ISSUED`

## Canonical session handoff

`docs/governance/DLH_SESSION_HANDOFF_AFTER_TIER0_NUMERICAL_ROBUSTNESS_COMPLETE_2026_08_19.md`

A new session must fresh-fetch live `main` before using this pointer.

## Accepted provenance

- Issue #1 bootstrap: `ACCEPTED_AND_CLOSED`, commit `bcded9b9137f3c10f71a7a6ecb929f78b40bdc11`.
- Issue #2 DLH-0 scientific constitution: `ACCEPTED_AND_CLOSED`, commit `73e1ae5db9d7e362781a77fa2a204c80238fad3e`.
- Issue #3 DLH-1A literature/data feasibility: `ACCEPTED_AND_CLOSED`, commit `e9aa7dc8a3f5a198b1655c917659f519239eb67b`.
- Issue #4 DLH-1B Python kernel audit: `ACCEPTED_AND_CLOSED`, commit `8dce318af5ca704a747e67932ec3caa35f9168ad`.
- Issue #5 DLH-2A fixed-price HJB/KFE: `DLH_2A_R1_TIER0_KERNEL_FIXED_PRICE_VALIDATION_ACCEPTED_AND_CLOSED`, commit `76b5882a63d8ade18d50098373b7c735eb2c4ca4`, evidence `D2_MACHINE_DIAGNOSTIC_ONLY`.
- Issue #6 DLH-2B single-region steady-state GE: `DLH_2B_R1_TIER0_SINGLE_REGION_STEADY_STATE_GE_ACCEPTED_AND_CLOSED`, commit `c562ce3a2743ac779123918e9aab5f37044b564a`, evidence `D2_MACHINE_DIAGNOSTIC_ONLY`.
- Issue #7 DLH-2C robustness: `DLH_2C_BOUNDARY_SENSITIVITY_BLOCKED_ACCEPTED_AND_CLOSED`, fail-closed commit `583e352b3ba37d25ebb7d8f468b5fd9f4f5eb5d3`.
- Issue #8 DLH-2C-B1 asset-domain adequacy: `DLH_2C_B1_WIDE_DOMAIN_GRID_CONVERGENCE_BLOCKED_ACCEPTED_AND_CLOSED`, fail-closed commit `249c9dcaf3c16b4b308e9d83daf232a23dce79cb`.
- Issue #9 DLH-2C-B2 fixed-domain third-level grid convergence: `DLH_2C_B2_FIXED_DOMAIN_GRID_CONVERGENCE_ACCEPTED_AND_CLOSED`, commit `5632ee1cbc781d67daf305f315f556506da0f6df`, evidence `D2_MACHINE_DIAGNOSTIC_ONLY`.

## Final Tier-0 numerical disposition

The planned Tier-0 numerical-robustness block is complete.

Accepted canonical high-accuracy validation/reference standard:

- scientific object: small one-region real HA/Aiyagari benchmark, **not genuine HANK**;
- fixture label: `VALIDATION_FIXTURE_NOT_CALIBRATION`;
- asset domain: `[0,200]`;
- accepted fixed-domain grids:
  - C200 = 317 points, spacing `50/79`;
  - F200 = 633 points, spacing `25/79`;
  - Q200 = 1265 points, spacing `12.5/79`;
- accepted capital sequence:
  - `K_C = 28.218969081766193`;
  - `K_F = 28.079912014017818`;
  - `K_Q = 28.010252116571742`;
- accepted same-domain differences:
  - `d_C_F = 0.00495219029457629`;
  - `d_F_Q = 0.00248694289348661`;
- F200→Q200 macro-object relative differences all `<0.005`;
- Q200 deterministic repeat differences all `0.0`;
- Issue #9 complete repository suite `54 passed / 0 failed`.

Issue #7 and Issue #8 remain accepted scientific blockers/provenance, not retroactive PASS results.

## Sole active Builder authority

**NONE.**

No open successor Issue is currently authorized for DSH.

DSH must not perform additional implementation, testing, data, legacy-source, nominal, regional or neural work until a new open GitHub Issue is created by ChatGPT/Owner and this Task Index is updated to point to it.

## Queued next scientific route — NOT ACTIVE

`DLH-3 — minimal genuine single-region HANK nominal/New-Keynesian layer`.

DLH-3 has **not** been issued. Its exact nominal equations, dynamics/shock boundary, solver family, development-grid relationship to the accepted Tier-0 standard, path allowlist and acceptance gates remain to be decided in the next session.

Current authority remains:

- genuine-HANK nominal implementation: `NONE` until new Issue;
- shocks/transition: `NONE` until explicitly granted;
- regional / `W^L` / `W^K` / old W: `NONE`;
- neural/RL: `NONE`;
- empirical calibration/data regression: `NONE`;
- Results/policy/novelty claims: `NONE`.
