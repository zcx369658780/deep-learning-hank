# Deep Learning + HANK Startup Snapshot — CURRENT

Date: 2026-08-19

Repository: `zcx369658780/deep-learning-hank`

Local Owner-designated workspace: `D:\deep-learning-hank`

## Governance state

- live GitHub `main` = synchronized repository/governance authority；
- open GitHub Issue = sole DSH Builder task authority；
- `tasks/TASK_INDEX_CURRENT.md` = synchronized Issue pointer only；
- DSH = bounded Builder；
- ChatGPT = independent GitHub reviewer / scientific-route authority / task issuer；
- Owner = final scientific-direction authority。

## Accepted stages

- Issue #1 bootstrap: accepted/closed at `bcded9b9137f3c10f71a7a6ecb929f78b40bdc11`.
- Issue #2 DLH-0 scientific constitution: accepted/closed at `73e1ae5db9d7e362781a77fa2a204c80238fad3e`.
- Issue #3 DLH-1A literature/data feasibility: accepted/closed at `e9aa7dc8a3f5a198b1655c917659f519239eb67b`.
- Issue #4 DLH-1B Python kernel audit: accepted/closed at `8dce318af5ca704a747e67932ec3caa35f9168ad`.
- Issue #5 DLH-2A fixed-price HJB/KFE: accepted/closed after R1 at `76b5882a63d8ade18d50098373b7c735eb2c4ca4`, D2 only.
- Issue #6 DLH-2B steady-state GE: accepted/closed after R1 at `c562ce3a2743ac779123918e9aab5f37044b564a`, D2 only.
- Issue #7 DLH-2C robustness: `DLH_2C_BOUNDARY_SENSITIVITY_BLOCKED_ACCEPTED`, accepted/closed at `583e352b3ba37d25ebb7d8f468b5fd9f4f5eb5d3`.
- Issue #8 DLH-2C-B1 asset-domain adequacy: `DLH_2C_B1_WIDE_DOMAIN_GRID_CONVERGENCE_BLOCKED_ACCEPTED`, accepted/closed at `249c9dcaf3c16b4b308e9d83daf232a23dce79cb`.

## Accepted Tier-0 computational state

The accepted scientific object remains a small one-region real HA/Aiyagari benchmark under `VALIDATION_FIXTURE_NOT_CALIBRATION`:

`K -> (w,r) -> balanced transfer -> HJB -> stationary KFE -> A(K) -> K-A(K)`.

Accepted numerical/economic modules remain frozen.

### Issue #7 accepted blocker

`a_max=50` is not adequate:
- matched-spacing `K50=27.2438081362`, `K100=28.2060803850`;
- `d50_100=0.03411577346665587 > 0.005`;
- upper-boundary and upper-tail mass fall sharply when the bound is widened.

### Issue #8 accepted blocker and new information

Asset-bound convergence itself is now strongly supported on the wider domain:

- C50→C100: `0.03411577346665587`;
- C100→C150: `0.000453983596378`;
- C150→C200: `2.756408258e-06`;
- C200 upper-boundary mass `5.50488358e-10`;
- C200 top-5% mass `1.36530748e-08`;
- F100→F200 fine-spacing bound observation `0.000445042795539 < 0.005`.

Thus the material upper-bound problem exposed by Issue #7 is resolved by the evidence up to `a_max=200`.

However grid convergence is not yet independently established:

- C100→F100 `d_grid_100=0.004940431182927`;
- C200→F200 `d_grid_200=0.004952190294576`;
- both individually satisfy 0.5%, but Issue #8's frozen cross-domain non-worsening condition fails by about `1.18e-05`.

Issue #8 is therefore correctly BLOCKED_ACCEPTED, not PASS.

## Current active task

Issue #9 — `DLH-2C-B2: Fixed-domain third-level grid convergence and canonical Tier-0 numerical standard`

Issue URL:
`https://github.com/zcx369658780/deep-learning-hank/issues/9`

Expected branch:
`dsh/issue-9-dlh-2c-b2-fixed-domain-grid-2026-08-19`

## DLH-2C-B2 authority

Hold asset domain fixed at `[0,200]` and test a true same-domain refinement sequence:

- C200: 317 points, spacing `50/79`;
- F200: 633 points, spacing `25/79`;
- Q200: 1265 points, spacing `12.5/79`.

Mandatory scientific questions:

1. Does accepted C200→F200 difference `0.004952190294576287` reproduce within `1e-12`?
2. Is F200→Q200 non-worsening on the same domain and `<=0.005`?
3. Are F200→Q200 differences in Y, wage, net return, transfer, mean consumption and mean assets each `<=0.005`?
4. Does Q200 pass all accepted HJB/KFE/equilibrium/accounting gates and deterministic reproducibility?
5. Do all accepted regressions remain green after Issue #8's known red gate is converted to blocker-provenance regression evidence?

If Issue #9 passes independent review, the planned Tier-0 numerical-robustness block may be considered complete and DLH-3 may be issued separately.

## Current implementation/scientific authority

- DLH-2A fixed-price kernel: `R1_ACCEPTED_D2`；
- DLH-2B steady-state GE: `R1_ACCEPTED_D2`；
- DLH-2C: `BOUNDARY_SENSITIVITY_BLOCKED_ACCEPTED_D2`；
- DLH-2C-B1: `WIDE_DOMAIN_GRID_CONVERGENCE_BLOCKED_ACCEPTED_D2`；
- DLH-2C-B2 fixed-domain grid convergence: `ACTIVE_NOT_ACCEPTED`；
- genuine-HANK nominal implementation authority: `NONE`；
- regional/W authority: `NONE`；
- shock/transition authority: `NONE`；
- neural training authority: `NONE`；
- empirical calibration authority: `NONE`；
- Results/manuscript authority: `NONE`；
- final novelty claim authority: `NONE`。

## Current boundaries

Issue #9 may only use its exact 7-path allowlist. It may not alter accepted economics/solver modules, accepted DLH-2A/DLH-2B tests, the `[0,200]` asset domain, Issue #7/#8 evidence, or add grid levels beyond Q200.

No regional/W, SOE/open-economy, nominal/NK, shock/transition, neural/RL, empirical data/calibration, Matlab/legacy Matlab, old-source-repo access or Results/policy/novelty work is authorized.

## Reviewer tooling provenance note

During the Issue #8 reviewer-side GitHub transition, ChatGPT accidentally created a one-byte `__dummy__` file through a connector call and immediately removed it in the next reviewer maintenance commit. The current tree contains no such file and no Builder authority was consumed. This is reviewer tooling provenance only and must not be interpreted as project/scientific evidence.
