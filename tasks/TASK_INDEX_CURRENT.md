# Deep Learning + HANK Task Index

Status: `ACTIVE_GITHUB_ISSUE_10__DLH_3A_MINIMAL_HANK_ARCHITECTURE`

## Canonical session handoff

`docs/governance/DLH_SESSION_HANDOFF_AFTER_TIER0_NUMERICAL_ROBUSTNESS_COMPLETE_2026_08_19.md`

A new Builder invocation must fresh-fetch live `main` before using this pointer.

## Accepted provenance

- Issue #1 bootstrap: `ACCEPTED_AND_CLOSED`, commit `bcded9b9137f3c10f71a7a6ecb929f78b40bdc11`.
- Issue #2 DLH-0 scientific constitution: `DLH_0_R1_NSR_HANK_SCIENTIFIC_CONSTITUTION_ACCEPTED_AND_CLOSED`, commit `73e1ae5db9d7e362781a77fa2a204c80238fad3e`.
- Issue #3 DLH-1A literature/data feasibility: `ACCEPTED_AND_CLOSED`, commit `e9aa7dc8a3f5a198b1655c917659f519239eb67b`.
- Issue #4 DLH-1B Python kernel audit: `ACCEPTED_AND_CLOSED`, commit `8dce318af5ca704a747e67932ec3caa35f9168ad`.
- Issue #5 DLH-2A fixed-price HJB/KFE: `DLH_2A_R1_TIER0_KERNEL_FIXED_PRICE_VALIDATION_ACCEPTED_AND_CLOSED`, commit `76b5882a63d8ade18d50098373b7c735eb2c4ca4`, evidence `D2_MACHINE_DIAGNOSTIC_ONLY`.
- Issue #6 DLH-2B single-region steady-state GE: `DLH_2B_R1_TIER0_SINGLE_REGION_STEADY_STATE_GE_ACCEPTED_AND_CLOSED`, commit `c562ce3a2743ac779123918e9aab5f37044b564a`, evidence `D2_MACHINE_DIAGNOSTIC_ONLY`.
- Issue #7 DLH-2C robustness: `DLH_2C_BOUNDARY_SENSITIVITY_BLOCKED_ACCEPTED_AND_CLOSED`, fail-closed commit `583e352b3ba37d25ebb7d8f468b5fd9f4f5eb5d3`.
- Issue #8 DLH-2C-B1 asset-domain adequacy: `DLH_2C_B1_WIDE_DOMAIN_GRID_CONVERGENCE_BLOCKED_ACCEPTED_AND_CLOSED`, fail-closed commit `249c9dcaf3c16b4b308e9d83daf232a23dce79cb`.
- Issue #9 DLH-2C-B2 fixed-domain third-level grid convergence: `DLH_2C_B2_FIXED_DOMAIN_GRID_CONVERGENCE_ACCEPTED_AND_CLOSED`, commit `5632ee1cbc781d67daf305f315f556506da0f6df`, evidence `D2_MACHINE_DIAGNOSTIC_ONLY`.

Issue #7 and Issue #8 remain accepted scientific blockers/provenance, not retroactive PASS results.

## Final Tier-0 numerical disposition

The planned Tier-0 numerical-robustness block is complete at D2 machine-diagnostic level.

Accepted canonical high-accuracy validation/reference standard:

- scientific object: small one-region real HA/Aiyagari benchmark, **not genuine HANK**;
- fixture label: `VALIDATION_FIXTURE_NOT_CALIBRATION`;
- canonical Tier-0 asset domain: `[0,200]`;
- C200 = 317 points, F200 = 633 points, Q200 = 1265 points;
- `K_C = 28.218969081766193`;
- `K_F = 28.079912014017818`;
- `K_Q = 28.010252116571742`;
- `d_C_F = 0.00495219029457629`;
- `d_F_Q = 0.00248694289348661`;
- F200→Q200 macro-object relative differences all `<0.005`;
- Q200 deterministic repeat differences all `0.0`;
- Issue #9 full suite `54 passed / 0 failed`.

Q200 `[0,200]` remains the accepted Tier-0 reference. Its domain adequacy is **not automatically inherited** by a later HANK economy with different asset semantics.

## Sole active Builder authority

**GitHub Issue #10 — OPEN**

Title:

`DLH-3A: Minimal genuine single-region HANK architecture and equation freeze`

Issue URL:

`https://github.com/zcx369658780/deep-learning-hank/issues/10`

This Issue is the sole DSH Builder authority. DSH must read its fresh body/comments from GitHub at startup.

### Task nature

`SPECIFICATION_ONLY__ZERO_MODEL_IMPLEMENTATION__ZERO_NUMERICAL_EXECUTION`

DLH-3A freezes an auditable single-region HANK **validation architecture** around:

- one liquid/risk-free financial asset for the DLH-3 validation economy;
- heterogeneous households + existing two-state idiosyncratic CTMC starting fixture;
- CRRA + endogenous static labor supply;
- time-dependent HJB / forward KFE semantics plus stationary reduction;
- labor-based production for the minimal validation economy;
- Rotemberg price adjustment / NKPC;
- Fisher relation + Taylor-type monetary rule;
- explicit government-bond supply / fiscal / transfer / dividend accounting;
- explicit market/equation residuals;
- separate future 3B/3C/3D/3E validation gates.

### Owner deferral

The DLH-3 single-region validation asset/production choice does **not** permanently freeze the final regional steady-state NSR-HANK architecture. After the regional steady-state program is sufficiently formed, Owner/ChatGPT may decide whether to retain, modify or replace that structure.

### Exact Builder output allowlist

1. `docs/specifications/DLH_3_MINIMAL_GENUINE_HANK_ARCHITECTURE_2026_08_19.md`
2. `docs/specifications/DLH_3_ASSET_FISCAL_AND_NOMINAL_SEMANTICS_CONTRACT_2026_08_19.md`
3. `docs/specifications/DLH_3_STEADY_STATE_AND_DYNAMIC_EQUATION_CONTRACT_2026_08_19.md`
4. `docs/specifications/DLH_3_VALIDATION_LIMITING_CASE_AND_GRID_CONTRACT_2026_08_19.md`
5. `reports/dlh_3a_minimal_hank_architecture_2026_08_19/DLH_3A_REVIEW_PACKET.md`
6. `reports/dlh_3a_minimal_hank_architecture_2026_08_19/DLH_3A_FORBIDDEN_OPERATION_CHECK.md`

No other tracked path may change.

Dedicated branch:

`dsh/issue-10-dlh-3a-minimal-hank-architecture-2026-08-19`

Expected success candidate classification:

`DLH_3A_MINIMAL_HANK_ARCHITECTURE_READY_FOR_GPT_OWNER_REVIEW`

## Current non-authority

Issue #10 does **not** authorize:

- any `src/**`, `configs/**`, `tests/**` mutation;
- numerical model execution or new pytest scientific run;
- HANK steady-state implementation;
- transition or shock simulation;
- monetary IRFs;
- regional / `W^L` / `W^K` / `W^G` implementation;
- neural/RL/training;
- empirical calibration/data regression;
- legacy Matlab or old Python reference-repository access;
- Results/policy/welfare/novelty claims;
- PR / merge / Issue close / successor / self-accept by Builder.

Future DLH-3B/3C/3D/3E are design boundaries only and carry **NO Builder authority** until separate open GitHub Issues are created.

## Governance numbering note

`project_rules/PROJECT_RULE_MODEL_DEVELOPMENT_DIAGNOSTIC_GATES_CURRENT.md` was reviewer-side clarified before Issue #10 publication: its old `DLH-*` sequence is generic diagnostic-category provenance only. CURRENT project-stage identity comes from the Master Roadmap + this Task Index + the active Issue. Thus CURRENT `DLH-3` means the minimal genuine single-region HANK layer.
