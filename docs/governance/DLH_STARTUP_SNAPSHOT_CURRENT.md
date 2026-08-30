# Deep Learning + HANK Startup Snapshot — CURRENT

Date: 2026-08-30

Repository: `zcx369658780/deep-learning-hank`

Local Owner-designated workspace: `D:\deep-learning-hank`

## Governance state

- live GitHub `main` = synchronized repository/governance authority;
- active GitHub Issue pointed to by `tasks/TASK_INDEX_CURRENT.md` = sole Builder authority;
- DSH = bounded Builder/executor;
- ChatGPT = independent fresh-GitHub reviewer / scientific-route authority / task issuer / GitHub governance operator;
- Owner = final scientific-direction authority;
- Builder completion is not acceptance.

Priority:

`Scientific correctness > Experiment reproducibility > Research iteration speed > Git auditability > Documentation completeness`

## Active Builder task

`ACTIVE_GITHUB_ISSUE_20__DLH_4D_TWO_ASSET_SINGLE_REGION_GE_STEADY_STATE`

Issue #20:

`DLH-4D: Implement and validate minimal single-region two-asset GE steady state`

Task type:

`SCIENTIFIC_IMPLEMENTATION__TWO_ASSET_SINGLE_REGION_GE_STEADY_STATE`

Builder:

DSH bounded executor.

## Accepted immutable household foundation

Canonical household implementation:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`57e32076f0e11c9a047e1f90f8c2446d4148e457`

SHA-256:

`276D2244B389D6EDE140DAF8B1F9B0BE1F4AA859368941CED1A12BA8A5831AB8`

This household oracle is frozen for the active route. Issue #20 authorizes zero changes to `src/deep_learning_hank/two_asset/**`.

## Accepted DLH-4C GE contract

Issue #19 is accepted/closed at contract commit:

`7fcfd6412c580f888d2ef8175335c3909f146e59`

Classification:

`DLH_4C_OPTION_A_GE_CLOSURE_CONTRACT_ACCEPTED`

Owner-frozen Option A:

- `K=A_hh`;
- `B_hh=B_gov` with constant exogenous real government-bond supply;
- competitive firms, `mu=1`;
- `Y=Z*K^alpha*L^(1-alpha)`;
- `w=F_L`;
- `r_a=F_K-delta`;
- balanced transfer `T=tau*w*L-r_b*B_gov`;
- ordered unknowns `x=(r_a,r_b,L)`;
- ordered root residuals `(A_hh-K, B_hh-B_gov, L_hh-L)`.

Resource/accounting distinction:

- structural resource gap `R_resource_structural=Y-C-delta*K-AC`;
- numerical taper wedge `W_taper` from the immutable faithful oracle;
- faithful gated residual `R_resource_faithful=R_resource_structural-W_taper`.

`W_taper` is numerical regularization, not economic resource use.

## Current scientific objective — DLH-4D

Implement and validate the minimal single-region two-asset real GE steady-state fixture around the immutable household oracle.

Frozen validation fixture and deterministic solver architecture are specified in Issue #20. DSH must fail closed rather than alter economics, fixture values, solver domains, or the household oracle to seek PASS.

## Current scientific ceiling

Accepted before DLH-4D:

`TWO_ASSET_HA_HOUSEHOLD_HJB_KFE_AGGREGATE_FOUNDATION`

and

`TWO_ASSET_SINGLE_REGION_GE_STEADY_STATE_DESIGN_CONTRACT`

Possible ceiling after independent DLH-4D acceptance:

`MINIMAL_SINGLE_REGION_TWO_ASSET_REAL_GE_STEADY_STATE_VALIDATED`

Not authorized or validated:

- household redesign;
- transition dynamics / IRFs;
- NKPC/Taylor/Fisher/monetary shocks;
- regional/multi-province HANK;
- learned `W^L` / `W^K`;
- Deep Learning training;
- empirical calibration;
- policy/welfare/paper Results.

## Required Builder startup

1. fresh fetch live `origin/main`;
2. read CURRENT project rules;
3. read `tasks/TASK_INDEX_CURRENT.md`;
4. read this Startup Snapshot;
5. fresh-read Issue #20 body + all comments;
6. verify immutable household blob/SHA;
7. read accepted DLH-4C contract/validation plan;
8. fail closed on authority or household-identity mismatch.
