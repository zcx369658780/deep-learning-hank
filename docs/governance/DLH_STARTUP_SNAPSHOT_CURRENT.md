# Deep Learning + HANK Startup Snapshot — CURRENT

Date: 2026-09-01

Repository: `zcx369658780/deep-learning-hank`

Local Owner-designated workspace: `D:\deep-learning-hank`

## Governance state

- live GitHub `main` = synchronized repository/governance authority;
- GitHub Issue = sole DSH Builder authority only after publication + synchronization + authoritative activation;
- DSH = bounded Builder/executor;
- ChatGPT = independent fresh-GitHub reviewer / scientific-route advisor / task issuer / governance operator;
- Owner = final scientific-direction authority;
- Builder completion is not acceptance.

Priority:

`Scientific correctness > Experiment reproducibility > Research iteration speed > Git auditability > Documentation completeness`

## Current Builder state

`NO_ACTIVE_BUILDER_ISSUE__DLH_5C_ACCEPTED__OWNER_KFE_REDESIGN_DECISION_REQUIRED`

There is currently **no active Builder Issue**. DSH must remain stopped until a new Issue is published, Task Index / Startup Snapshot are synchronized, and an activation comment is present.

## Latest accepted gate — Issue #26 / DLH-5C

Accepted candidate integrated to `main`:

`c6b773323fa4d7fe480f4ae8a1523bcb97d8113c`

Accepted classification:

`DLH_5C_KFE_SINGULARITY_DIAGNOSTIC_ACCEPTED__FIXED_ROW_SELECTION_ARTIFACT_PRIMARY__OWNER_KFE_REDESIGN_DECISION_REQUIRED`

Acceptance level:

`L3_COMMIT_OR_PR_VERIFIED`

Scientific numerical evidence level:

`D2_MACHINE_NUMERICAL_DIAGNOSTIC__NO_STRONG_ECONOMIC_RESULTS_CLAIM`

Accepted evidence roots:

- `reports/dlh_5c_kfe_singularity_diagnostic_2026_08_31/`
- `reports/dlh_5c_kfe_singularity_diagnostic_r1_2026_08_31/`
- `reports/dlh_5c_kfe_singularity_diagnostic_r2_2026_09_01/`

## Accepted stationary-KFE diagnosis

Canonical household source remains:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Current stationary KFE code authority uses:

```text
transpose = operator.T
row = floor(0.37*N)-1
contaminated[row,:] = 0
contaminated[row,row] = 1
rhs[row] = 0.007
raw = spsolve(contaminated,rhs)
```

This implementation is now scientifically qualified by DLH-5C.

### Correct operator orientation

For a positive off-diagonal source-operator entry:

`Q[row,col] > 0`

the accepted operator assembly means:

`row -> col`

where row is the current/source state and column is the destination state. `Q V` is the backward/HJB action; `Q.T g` is the forward/KFE action.

### Corrected graph structure on frozen D0-D3 fixture

Two closed sinks:

1. size 40, `a=0` borrowing-constrained class — conservative / non-leaky;
2. size 546, contains accepted row 295 — leaky at 29-30 upper-boundary states.

The D1/D2 graph structure is unchanged. D2 failure is not caused by an SCC topology change.

### Decisive original-equation residual evidence

Diagnostic pins are `{0,200,295,400,600,799}`.

- Pins 0 and 400 recover the same normalized density and satisfy `Q.T @ g = 0` to machine precision across D0-D3.
- The accepted pin 295 and other pins inside the leaky 546-state sink can produce finite contaminated-system solutions at D0/D1/D3, but those normalized densities are not solutions of the ORIGINAL stationary equation.
- Accepted pin 295 original residuals are approximately:
  - D0: `0.1261148952`
  - D1: `0.1233636144`
  - D3: `0.1272057472`
- In each case the maximum residual occurs exactly at the dropped/pinned equation.
- At D2 pin 295 becomes exactly singular/non-finite; pins 0/400 remain finite and agree.

### Nullspace / stationary-support evidence

Bounded sparse singular diagnostics at D1/D2 show one near-zero singular direction, with essentially all L1 support on the conservative `a=0` size-40 class and negligible support on the leaky 546-state sink.

Accepted bounded interpretation:

- PRIMARY: `FIXED_ROW_SELECTION_ARTIFACT_CANDIDATE`;
- direct D2 mechanism: exact sparse-pivot/singularity of the inconsistent fixed-pinned system;
- structural supporting blocker: upper-boundary non-conservation / leakage in the post-convergence operator;
- `MULTIPLE_OR_NONUNIQUE_STATIONARY_CLASS_CANDIDATE` is not accepted as primary.

The frozen 9-point D1->D2 scan only establishes that D2 is the failed sampled endpoint at that resolution; it does not rule out an unsampled narrower failure interval between `t=7/8` and `t=1`.

## Consequence for DLH-5B / two-region prototype

Issue #25 remains accepted for:

- two-region network wiring;
- synchronous/Jacobi old-state semantics;
- labor-flow accounting and wage-bill identities;
- fixed-damping outer-map implementation;
- trace/reproducibility/fail-closed architecture.

However, the current row-295 KFE density is not a validated stationary distribution even at the D0 anchor. Therefore the previously reported household aggregates:

`A*, L*, C*, B*`

and firm-anchor quantities derived from them:

`Z*, delta*`

must not be treated as validated stationary-equilibrium economic quantities.

This also means the exploratory closure `K_i=M_i*A_i` has not yet been revalidated against a scientifically accepted stationary KFE.

## Current scientific blocker

The project must not proceed to:

- perturbed two-region equilibrium acceptance;
- OD/network training execution;
- learned `W^L`;
- 3–5 region equilibrium embedding;
- `W^K`;
- nominal HANK integration;
- calibration / 31-region runs;
- policy/welfare / Results;

until the stationary-KFE / finite-grid boundary problem is scientifically redesigned and revalidated.

## Owner scientific decision required before next Issue

The next Builder task is intentionally **not published**.

Owner must freeze the scientific redesign contract for at least:

1. stationary KFE equation and normalization condition;
2. finite-grid boundary law and generator conservation requirement;
3. whether the MATLAB-faithful fixed contaminated-row pin is superseded;
4. numerical solver class allowed for the stationary equation;
5. acceptance tolerances for original-equation residual, mass normalization, non-negativity and boundary mass;
6. required revalidation of household aggregates and the two-region `K_i=M_i*A_i` anchor after the KFE repair.

Until that decision is made, no active Builder authority exists.

## Earlier accepted foundation

### Issue #25 / DLH-5B

Accepted candidate:

`4c97ae30d98c40466af3ff11ce8048e5e5087335`

Architecture accepted, stationary-KFE-dependent economic quantities scientifically qualified by DLH-5C.

### Issue #24 / DLH-5A

Network-ready two-region real structural HA-GE contract accepted.

### Issue #23

MATLAB-faithful two-asset HJB / transfer-FOC parity repair accepted. The household/HJB source remains code authority; the stationary KFE portion now requires a new scientific redesign gate before downstream economic use.
