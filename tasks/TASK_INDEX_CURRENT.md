# Deep Learning + HANK Task Index

Status: `NO_ACTIVE_BUILDER_ISSUE__DLH_5C_ACCEPTED__OWNER_KFE_REDESIGN_DECISION_REQUIRED`

Last synchronized: 2026-09-01

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

There is currently **NO ACTIVE BUILDER ISSUE**.

DSH must not mutate the repository until a new GitHub Issue is explicitly published, Task Index / Startup Snapshot are synchronized, and an authoritative activation comment is present.

## Latest accepted task

**Issue #26 — DLH-5C — ACCEPTED / COMPLETED**

Title:

`DLH-5C: Diagnose stationary KFE contaminated-row singularity on the preserved two-region perturbed path`

Accepted candidate integrated to `main`:

`c6b773323fa4d7fe480f4ae8a1523bcb97d8113c`

Accepted reviewer classification:

`DLH_5C_KFE_SINGULARITY_DIAGNOSTIC_ACCEPTED__FIXED_ROW_SELECTION_ARTIFACT_PRIMARY__OWNER_KFE_REDESIGN_DECISION_REQUIRED`

Acceptance level:

`L3_COMMIT_OR_PR_VERIFIED`

Scientific numerical evidence level:

`D2_MACHINE_NUMERICAL_DIAGNOSTIC__NO_STRONG_ECONOMIC_RESULTS_CLAIM`

Accepted evidence roots:

- `reports/dlh_5c_kfe_singularity_diagnostic_2026_08_31/`
- `reports/dlh_5c_kfe_singularity_diagnostic_r1_2026_08_31/`
- `reports/dlh_5c_kfe_singularity_diagnostic_r2_2026_09_01/`

## Accepted DLH-5C findings

1. Accepted KFE construction currently uses a fixed contaminated row:

```text
transpose = operator.T
row = floor(0.37*N)-1
contaminated[row,:] = 0
contaminated[row,row] = 1
rhs[row] = 0.007
raw = spsolve(contaminated,rhs)
```

2. Correct transition orientation is `Q[row,col]>0 : row -> col`, with `Q V` as backward/HJB action and `Q.T g` as forward/KFE action.

3. Corrected graph diagnostics give two closed sinks on the frozen fixture:

- size 40: `a=0` borrowing-constrained class, conservative;
- size 546: contains accepted row 295, but is leaky at 29-30 upper-boundary rows.

4. Pins 0 and 400 recover the same normalized density and satisfy the ORIGINAL stationary equation to machine precision.

5. The accepted fixed pin 295 can return finite contaminated-system solutions at D0/D1/D3, but those densities do **not** satisfy the original stationary equation; original residual is about `0.126 / 0.123 / 0.127`, with the maximum residual exactly at the dropped row.

6. At D2 the same fixed pin becomes exactly singular/non-finite. The frozen 9-point scan only establishes endpoint-only failure at the sampled resolution; it does not exclude an unsampled narrower failure interval near D2.

7. Bounded sparse singular diagnostics support one near-null direction concentrated essentially entirely on the conservative `a=0` class. `MULTIPLE_OR_NONUNIQUE_STATIONARY_CLASS_CANDIDATE` is not accepted as primary.

Primary diagnostic classification:

`FIXED_ROW_SELECTION_ARTIFACT_CANDIDATE`

Supporting layers:

- numerical conditioning / exact-pivot mechanism at D2;
- post-convergence boundary / conservation problem in the leaky 546-state sink.

## Consequence for accepted DLH-5B

Issue #25 remains accepted for **architecture / wiring / Jacobi / accounting / trace semantics**.

However, household aggregates and firm-anchor objects derived from the current row-295 KFE density are **not validated stationary-equilibrium economic quantities**. In particular, the D0 row-295 density has original KFE residual around `0.126`.

Therefore downstream use of `A*, L*, C*, B*`, derived `Z*, delta*`, perturbed outer-equilibrium claims, calibration, learned networks, larger-region scaling and Results is scientifically blocked until a new stationary-KFE / boundary contract is frozen and validated.

## Current scientific route / Owner decision gate

The next task is **not yet authorized**.

Owner scientific decision is required before any KFE repair/redesign Issue is published. The decision must freeze at least:

- stationary KFE mathematical definition and normalization;
- finite-grid boundary treatment / generator conservation law;
- whether MATLAB-faithful contaminated-row pinning is superseded;
- acceptance conditions for nonnegative normalized density and original-equation residual;
- how the repaired KFE invalidates/requires revalidation of prior household aggregates and the exploratory `K_i=M_i*A_i` two-region anchor.

Until that Owner decision is made, DSH must remain stopped.

## Earlier accepted foundation

- Issue #25 / DLH-5B: two-region synchronous/Jacobi architecture accepted, stationary-KFE-dependent economic quantities now scientifically qualified as above.
- Issue #24 / DLH-5A: network-ready two-region real structural contract accepted.
- Issue #23: MATLAB-faithful two-asset household/HJB parity repair accepted; current stationary KFE implementation remains code authority only until superseded by a new scientific contract.
