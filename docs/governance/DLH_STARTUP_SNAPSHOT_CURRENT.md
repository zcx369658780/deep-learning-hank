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

Current published task:

**Issue #27 — DLH-5D: Freeze conservative stationary-KFE boundary law and MATLAB-style contamination contract**

Task type:

`SCIENTIFIC_DESIGN__STATIONARY_KFE_BOUNDARY_AND_CONTAMINATION_CONTRACT`

Builder authority becomes active only when Issue #27 remains open, Task Index/Startup identity is synchronized, and the authoritative activation comment is present.

Dedicated branch:

`dsh/issue-27-dlh-5d-kfe-boundary-contamination-contract-2026-09-01`

Issue #27 is design/provenance only. DSH may add only the two explicit Markdown outputs in the Issue body and may not modify existing production/model/config/test/report/governance files.

## Owner scientific clarification now frozen for DLH-5D

The stationary KFE generator `Q` is expected to be singular. This is normal, not a solver failure.

The scientific stationary object is:

```text
Q^T g = 0
sum(g * cell_weight) = 1
g >= 0 up to tolerance
```

MATLAB-style contamination / row replacement remains an authorized numerical normalization approach in principle:

```text
T = Q^T
T_tilde[n,:] = 0
T_tilde[n,n] = 1
rhs[n] = c > 0
raw = solve(T_tilde, rhs)
g = raw / (sum(raw) * cell_weight)
```

The contamination method is not rejected merely because `Q` is singular.

However, a contaminated solution is scientifically valid only if its normalized density also satisfies the ORIGINAL unmodified equation `Q^T g = 0` within the frozen tolerance. Contaminated-system residual alone is insufficient.

For a conservative generator with a unique stationary distribution, future validation must demonstrate bounded pin-row invariance: different deterministic replacement rows recover the same normalized density within tolerance.

## Finite-grid boundary contract to be frozen

DLH-5C established that the current source-axis assembly can omit an outward destination at a finite boundary while retaining the corresponding rate in the diagonal, producing negative row sums / probability leakage.

DLH-5D must freeze:

```text
sum_j Q[i,j] = 0
Q[i,j] >= 0 for i != j
Q[i,i] = -sum_{j != i} Q[i,j]
```

within numerical tolerance.

At finite asset boundaries the represented process must obey no outward probability flux.

The successor implementation must distinguish:

- economically requested outward drift/rate;
- admitted finite-grid generator rate.

A conservative assembler may not silently turn a materially outward policy into a scientific PASS. Requested outward boundary flow above the frozen tolerance must surface as `BOUNDARY_POLICY_VIOLATION` and stop acceptance.

## Future acceptance targets to be frozen by Issue #27

Default successor tolerances unless DLH-5D justifies stricter/scaled alternatives:

```text
generator row-sum max abs              <= 1e-12
negative off-diagonal magnitude        <= 1e-12
original stationary residual ||Q^T g|| <= 1e-10
mass normalization error               <= 1e-12
minimum density                        >= -1e-12
multi-pin normalized-density max diff  <= 1e-10
repeat numeric difference              <= 1e-12
boundary requested outward rate        <= 1e-10
```

For the canonical validation fixture, a unique normalized stationary distribution is required. If a repaired conservative generator supports multiple economically valid stationary measures, stop for Owner decision; do not let the contamination row implicitly choose a mixture.

## MATLAB provenance requirement

Issue #27 must use the authorized read-only MATLAB source root:

`D:\MatlabProgram\2023年12月2日 多省份神经网络HANK`

to audit, where available:

- HJB generator/transition matrix `A`;
- KFE use of `A'`;
- contaminated-row construction;
- chosen row/RHS conventions;
- normalization;
- finite-grid boundary treatment;
- any implicit matrix assumptions relevant to the contamination method.

Missing provenance must be reported as `NOT LOCATED`, not inferred.

## Latest accepted gate — Issue #26 / DLH-5C

Accepted candidate integrated to `main`:

`c6b773323fa4d7fe480f4ae8a1523bcb97d8113c`

Accepted classification:

`DLH_5C_KFE_SINGULARITY_DIAGNOSTIC_ACCEPTED__FIXED_ROW_SELECTION_ARTIFACT_PRIMARY__OWNER_KFE_REDESIGN_DECISION_REQUIRED`

Acceptance level:

`L3_COMMIT_OR_PR_VERIFIED`

Scientific evidence level:

`D2_MACHINE_NUMERICAL_DIAGNOSTIC__NO_STRONG_ECONOMIC_RESULTS_CLAIM`

Accepted key findings:

- correct source-generator orientation is `Q[row,col]>0 : row -> col`;
- current fixed row 295 can yield finite contaminated-system solutions that violate the original stationary equation at D0/D1/D3;
- row-295 original residual is approximately `0.126 / 0.123 / 0.127`, with the maximum at the dropped row;
- at D2 the same pinned system becomes exactly singular/non-finite;
- pins 0/400 recover the same normalized near-null density on the frozen fixture;
- the current operator has a conservative `a=0` class and a leaky 546-state sink containing row 295;
- one near-null direction is concentrated essentially on the conservative `a=0` class;
- fixed-row selection is the primary diagnosed artifact, with boundary conservation and conditioning as supporting layers.

## Consequence for Issue #25

Issue #25 remains accepted for:

- network wiring;
- synchronous/Jacobi semantics;
- labor accounting/wage-bill identities;
- fixed-damping outer-map architecture;
- trace/reproducibility/fail-closed infrastructure.

Its row-295-KFE-dependent `C,L,A,B` aggregates and derived `Z,delta` anchor are not validated stationary-equilibrium economic quantities.

After a successor KFE implementation passes the new contract, household aggregates must be recomputed from scratch and `K_i=M_i*A_i` must be revalidated. If corrected `A <= 0` or the firm block becomes invalid, stop for Owner decision rather than retuning the fixture.

## Issue #27 allowed outputs

Only:

1. `docs/specifications/DLH_5D_CONSERVATIVE_STATIONARY_KFE_BOUNDARY_AND_CONTAMINATION_CONTRACT_2026_09_01.md`
2. `docs/audits/DLH_5D_MATLAB_KFE_CONTAMINATION_AND_BOUNDARY_PROVENANCE_AUDIT_2026_09_01.md`

No implementation or experiment execution is authorized.

## Current scientific route

1. accepted HJB/HA foundation;
2. accepted two-region contract and architecture;
3. accepted KFE blocker diagnosis;
4. **current DLH-5D design freeze**;
5. only after DLH-5D acceptance, publish a bounded KFE/boundary implementation-validation task;
6. recompute household aggregates and revalidate `K=M*A` / firm anchor;
7. only after that resume perturbed two-region equilibrium, OD/network and later model tracks.

## DSH startup sequence

1. `Set-Location D:\deep-learning-hank`;
2. verify repo/remote/worktree;
3. `git fetch origin` and record fresh `origin/main`;
4. read all CURRENT rules;
5. read fresh Task Index and this Startup Snapshot;
6. read Issue #27 latest body/comments and verify activation;
7. read accepted Issues #23-#26 evidence and canonical household HJB/KFE source read-only;
8. inspect authorized MATLAB source root read-only for provenance;
9. create the exact Issue #27 dedicated branch from fresh `origin/main`;
10. add only the two design/audit Markdown files;
11. commit/push and STOP for fresh ChatGPT review.
