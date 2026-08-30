# Deep Learning + HANK Task Index

Status: `ACTIVE_GITHUB_ISSUE_20__DLH_4D_TWO_ASSET_SINGLE_REGION_GE_STEADY_STATE`

Last synchronized: 2026-08-30

Repository: `zcx369658780/deep-learning-hank`

## Sole active Builder authority

**GitHub Issue #20 — OPEN**

Title:

`DLH-4D: Implement and validate minimal single-region two-asset GE steady state`

Task type:

`SCIENTIFIC_IMPLEMENTATION__TWO_ASSET_SINGLE_REGION_GE_STEADY_STATE`

Builder:

DSH bounded executor.

Issue URL:

`https://github.com/zcx369658780/deep-learning-hank/issues/20`

Builder must fresh-read Issue #20 body and all comments before mutation.

## Accepted predecessors

Issue #18 accepted the immutable two-asset household oracle.

Canonical household path:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`57e32076f0e11c9a047e1f90f8c2446d4148e457`

SHA-256:

`276D2244B389D6EDE140DAF8B1F9B0BE1F4AA859368941CED1A12BA8A5831AB8`

Issue #19 / DLH-4C accepted the Owner-frozen Option A GE contract at:

`7fcfd6412c580f888d2ef8175335c3909f146e59`

Accepted classification:

`DLH_4C_OPTION_A_GE_CLOSURE_CONTRACT_ACCEPTED`

## Frozen Option A

- `K=A_hh`;
- `B_hh=B_gov` with constant exogenous real government bonds;
- competitive firms (`mu=1`);
- `Y=Z*K^alpha*L^(1-alpha)`;
- `w=F_L`;
- `r_a=F_K-delta`;
- `T=tau*w*L-r_b*B_gov`;
- unknowns `x=(r_a,r_b,L)`;
- root residuals `(A_hh-K, B_hh-B_gov, L_hh-L)`.

Faithful accounting reports:

- `R_resource_structural=Y-C-delta*K-AC`;
- numerical `W_taper`;
- gated `R_resource_faithful=R_resource_structural-W_taper`.

## Scientific ceiling

DLH-4D may at most establish a validated minimal **single-region two-asset real steady-state GE fixture**.

No authority for household changes, transition dynamics/IRFs, NK monetary closure, regional HANK, learned flow matrices, Deep Learning, empirical calibration, welfare/policy, or Results.
