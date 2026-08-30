# Deep Learning + HANK Startup Snapshot — CURRENT

Date: 2026-08-30

Repository: `zcx369658780/deep-learning-hank`

Local Owner-designated workspace: `D:\deep-learning-hank`

## Governance state

- live GitHub `main` = synchronized repository/governance authority;
- GitHub Issue = Builder task authority only when separately published and activated;
- DSH = bounded Builder/executor;
- ChatGPT = independent fresh-GitHub reviewer / scientific-route authority / task issuer / GitHub governance operator;
- Owner = final scientific-direction authority;
- Builder completion is not acceptance.

Priority:

`Scientific correctness > Experiment reproducibility > Research iteration speed > Git auditability > Documentation completeness`

## Active Builder task

`ACTIVE_GITHUB_ISSUE_19__DLH_4C_TWO_ASSET_SINGLE_REGION_GE_CLOSURE_CONTRACT`

Issue:

`DLH-4C: Freeze minimal single-region two-asset GE steady-state closure contract`

Task type:

`SCIENTIFIC_DESIGN__TWO_ASSET_SINGLE_REGION_GE_CLOSURE_CONTRACT`

Builder:

DSH bounded scientific auditor / contract drafter.

## Accepted immutable household foundation

Current accepted stage:

`TWO_ASSET_HA_HOUSEHOLD_FOUNDATION_ACCEPTED`

Canonical package:

`src/deep_learning_hank/two_asset/`

Canonical household implementation:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Accepted Issue #18 candidate commit:

`24dde6792f6800f1ae872001587c2a1a3503d919`

Canonical Git blob:

`57e32076f0e11c9a047e1f90f8c2446d4148e457`

Required SHA-256 provenance:

`276D2244B389D6EDE140DAF8B1F9B0BE1F4AA859368941CED1A12BA8A5831AB8`

The household module is immutable in DLH-4C. No changes to household economics, HJB, KFE, policy selection, numerical regularization, boundaries, or aggregation are authorized.

## Household scientific identity

Accepted household object:

- state `(b,a,z)`;
- liquid asset `b`;
- illiquid asset `a`;
- consumption/labor/transfer choice;
- adjustment cost;
- MATLAB-faithful HJB iteration operator;
- post-convergence operator;
- stationary KFE density;
- aggregate `C`, effective labor, `A_hh`, `B_hh`.

Maintain the distinction between:

### `ECONOMIC_STRUCTURE`

and

### `NUMERICAL_REGULARIZATION / MATLAB_FAITHFUL_IMPLEMENTATION`

The accepted numerical baseline preserves the `max(a,a_bar)` cost floor, bare-`a` production transfer-FOC pairing, illiquid-return taper, MATLAB-spdiags-equivalent boundary behavior, and contaminated-row KFE. These must not be silently changed or reinterpreted as new GE equations.

## Current scientific objective — DLH-4C

Freeze the minimal single-region two-asset steady-state GE design contract around the immutable household oracle.

The contract must explicitly close or escalate:

- `A_hh` ↔ productive-capital mapping;
- `B_hh` economic meaning and liquid-asset supply;
- firm production, wage, depreciation and illiquid-return equations;
- household price mappings `r_a`, `r_b`, wage, tax, transfer and borrowing spread;
- fiscal/debt balance sheet;
- steady-state resource accounting including household adjustment costs;
- explicit ordered GE unknown vector and equally sized residual vector;
- degree-of-freedom audit;
- numeraire/normalization;
- deterministic solver architecture;
- compact validation fixture;
- stable interfaces for future dynamics, NK, regional flows and learned matrices.

The Chapter-5 legacy GE route is read-only provenance only. Its manual multi-province iteration, lack of a unique residual map, and missing liquid-bond/resource closures must not be copied blindly.

If materially different scientifically legitimate closures remain, DSH must stop with:

`BLOCKED_DLH_4C_OWNER_CLOSURE_DECISION_REQUIRED`

and return a compact decision matrix instead of choosing silently.

## Mutation boundary

Authorized writes only under:

`reports/dlh_4c_two_asset_single_region_ge_contract_2026_08_30/`

No source/config/test mutation.

## Scientific ceiling

Current accepted ceiling:

`TWO_ASSET_HA_HOUSEHOLD_HJB_KFE_AGGREGATE_FOUNDATION`

Possible DLH-4C design ceiling after independent acceptance:

`TWO_ASSET_SINGLE_REGION_GE_STEADY_STATE_DESIGN_CONTRACT`

Not authorized or validated:

- GE solver implementation;
- transition dynamics / IRFs;
- NK monetary closure;
- regional/multi-province HANK;
- learned `W^L` / `W^K`;
- Deep Learning training;
- empirical calibration;
- policy/welfare/paper Results.

## Required Builder startup

1. fresh fetch live `origin/main`;
2. read CURRENT rules;
3. read `tasks/TASK_INDEX_CURRENT.md`;
4. read this Startup Snapshot;
5. fresh-read Issue #19 body + all comments;
6. verify immutable household blob/SHA identity;
7. read authorized Chapter-5 GE audit/source provenance;
8. fail closed on authority or household-identity mismatch.
