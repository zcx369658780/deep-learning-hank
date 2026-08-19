# Deep Learning + HANK Task Index

Status: `ACTIVE_GITHUB_ISSUE_9_DLH_2C_B2`

## Accepted predecessors

- Issue #1 bootstrap: `ACCEPTED_AND_CLOSED`, commit `bcded9b9137f3c10f71a7a6ecb929f78b40bdc11`.
- Issue #2 DLH-0 scientific constitution: `ACCEPTED_AND_CLOSED`, commit `73e1ae5db9d7e362781a77fa2a204c80238fad3e`.
- Issue #3 DLH-1A literature/data feasibility: `ACCEPTED_AND_CLOSED`, commit `e9aa7dc8a3f5a198b1655c917659f519239eb67b`.
- Issue #4 DLH-1B Python kernel audit: `ACCEPTED_AND_CLOSED`, commit `8dce318af5ca704a747e67932ec3caa35f9168ad`.
- Issue #5 DLH-2A fixed-price HJB/KFE: `R1_ACCEPTED_AND_CLOSED`, commit `76b5882a63d8ade18d50098373b7c735eb2c4ca4`, evidence `D2_MACHINE_DIAGNOSTIC_ONLY`.
- Issue #6 DLH-2B single-region steady-state GE: `R1_ACCEPTED_AND_CLOSED`, commit `c562ce3a2743ac779123918e9aab5f37044b564a`, evidence `D2_MACHINE_DIAGNOSTIC_ONLY`.
- Issue #7 DLH-2C robustness: `DLH_2C_BOUNDARY_SENSITIVITY_BLOCKED_ACCEPTED_AND_CLOSED`, commit `583e352b3ba37d25ebb7d8f468b5fd9f4f5eb5d3`.
- Issue #8 DLH-2C-B1 asset-domain adequacy: `DLH_2C_B1_WIDE_DOMAIN_GRID_CONVERGENCE_BLOCKED_ACCEPTED_AND_CLOSED`, commit `249c9dcaf3c16b4b308e9d83daf232a23dce79cb`.

## Accepted Issue #8 scientific findings

Issue #8 is a correct fail-closed result, not a scientific PASS.

Accepted D2 facts:

- coarse matched-spacing asset-bound sequence strongly converges:
  - `d50_100 = 0.03411577346665587`;
  - `d100_150 = 0.000453983596378`;
  - `d150_200 = 2.756408258e-06`;
- C200 upper-boundary mass = `5.50488358e-10`; top-5% mass = `1.36530748e-08`;
- fine-spacing F100→F200 bound observation = `0.000445042795539 < 0.005`;
- therefore the material `a_max=50` upper-bound problem is resolved by the wide-domain evidence up to `a_max=200`;
- fixed-bound grid refinement remains unresolved:
  - C100→F100 `d_grid_100 = 0.004940431182927`;
  - C200→F200 `d_grid_200 = 0.004952190294576`;
  - both individually satisfy 0.5%, but Issue #8's frozen cross-domain non-worsening condition fails because `d_grid_200 > d_grid_100 + 1e-12`;
- all new variants pass accepted HJB/KFE/equilibrium/accounting gates and deterministic reproducibility;
- Issue #7 blocker provenance remains preserved rather than rewritten as PASS.

## Sole active Builder authority

GitHub Issue #9:

`DLH-2C-B2: Fixed-domain third-level grid convergence and canonical Tier-0 numerical standard`

Issue URL:
`https://github.com/zcx369658780/deep-learning-hank/issues/9`

Builder: DSH

Expected branch:
`dsh/issue-9-dlh-2c-b2-fixed-domain-grid-2026-08-19`

## Current gate purpose

Hold the now-wide asset domain fixed at `[0,200]` and perform the scientifically cleaner successive grid-refinement sequence:

- C200 = 317 points, spacing `50/79`;
- F200 = 633 points, spacing `25/79`;
- Q200 = 1265 points, spacing `12.5/79`.

Issue #9 must determine whether the same-domain F200→Q200 difference is non-worsening relative to accepted C200→F200 and remains within 0.5%, while all macro objects, numerical gates, reproducibility and regressions remain valid.

Issue #8's red grid test must be converted only into accepted blocker-provenance regression evidence. Issue #8 remains BLOCKED_ACCEPTED, not PASS.

## Scope boundary

Issue #9 remains `VALIDATION_FIXTURE_NOT_CALIBRATION`, real single-region Tier-0 only.

It does **not** authorize:
- changing asset domain away from `[0,200]` or adding grids beyond Q200;
- modifying accepted household/KFE/firm/fiscal/steady-state solver/economics modules;
- modifying accepted DLH-2A/DLH-2B tests;
- rewriting Issue #7/#8 reports/evidence;
- regional / `W^L` / `W^K` / old W;
- SOE / RegionalAccounts;
- nominal/Fisher/NKPC/Taylor;
- shocks/transition;
- neural/RL;
- empirical data/calibration/regression;
- Matlab/legacy Matlab or old-source-repo access;
- Results/policy/novelty claims;
- PR/merge/Issue-close/successor/self-accept by Builder.

## Queued next gate — NOT ACTIVE

`DLH-3 — minimal genuine single-region HANK nominal/New-Keynesian layer` remains blocked until Issue #9 receives fresh independent disposition. If Issue #9 passes, the planned Tier-0 numerical-robustness block may be closed and DLH-3 may be issued separately.
