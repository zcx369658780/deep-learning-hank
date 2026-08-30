# Deep Learning + HANK Task Index

Status: `ACTIVE_GITHUB_ISSUE_19__DLH_4C_TWO_ASSET_SINGLE_REGION_GE_CLOSURE_CONTRACT`

Last synchronized: 2026-08-30

Repository: `zcx369658780/deep-learning-hank`

## Sole active Builder authority

**GitHub Issue #19 — OPEN**

Title:

`DLH-4C: Freeze minimal single-region two-asset GE steady-state closure contract`

Task type:

`SCIENTIFIC_DESIGN__TWO_ASSET_SINGLE_REGION_GE_CLOSURE_CONTRACT`

Builder:

DSH bounded scientific auditor / contract drafter.

Issue URL:

`https://github.com/zcx369658780/deep-learning-hank/issues/19`

Builder must fresh-read Issue #19 body and all comments before mutation.

## Immutable accepted household foundation

Issue #18 is accepted and closed.

Canonical household path:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Accepted candidate commit:

`24dde6792f6800f1ae872001587c2a1a3503d919`

Canonical Git blob:

`57e32076f0e11c9a047e1f90f8c2446d4148e457`

Required SHA-256 provenance:

`276D2244B389D6EDE140DAF8B1F9B0BE1F4AA859368941CED1A12BA8A5831AB8`

DLH-4C authorizes zero mutation of the accepted household HJB/KFE/economics/numerical implementation.

## Current scientific task

DLH-4C is a design/source-audit gate only.

Its objective is to freeze an explicit, degree-of-freedom-complete minimal single-region two-asset steady-state GE contract around the immutable household block.

The contract must explicitly settle or escalate:

- mapping of `A_hh` to productive capital;
- economic meaning and supply of `B_hh`;
- firm production/wage/illiquid-return equations;
- liquid-rate closure;
- tax/transfer/government balance sheet;
- resource accounting including adjustment costs;
- ordered GE unknown vector and residual map;
- numeraire/normalization;
- solver architecture and validation fixture;
- future interfaces for dynamics, NK, regional flows and learned matrices.

If materially different closures remain legitimate, DSH must stop with `BLOCKED_DLH_4C_OWNER_CLOSURE_DECISION_REQUIRED` rather than silently choosing.

## Authorized mutation boundary

Only:

`reports/dlh_4c_two_asset_single_region_ge_contract_2026_08_30/**`

No source/config/test mutation is authorized.

## Scientific ceiling

Accepted baseline:

`TWO_ASSET_HA_HOUSEHOLD_HJB_KFE_AGGREGATE_FOUNDATION`

DLH-4C may at most establish:

`TWO_ASSET_SINGLE_REGION_GE_STEADY_STATE_DESIGN_CONTRACT`

It does not authorize or validate GE code, transition dynamics, NK monetary closure, regional NSR-HANK, Deep Learning, empirical calibration, policy/welfare, or Results.
