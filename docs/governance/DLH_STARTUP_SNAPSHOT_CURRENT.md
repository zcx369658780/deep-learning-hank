# Deep Learning + HANK Startup Snapshot — CURRENT

Date: 2026-09-01

Repository: `zcx369658780/deep-learning-hank`

Local Owner-designated workspace: `D:\deep-learning-hank`

## Governance state

- live GitHub `main` = synchronized repository/governance authority;
- GitHub Issue = sole DSH Builder authority only after publication + Task Index / Startup synchronization + authoritative activation comment;
- DSH = bounded Builder/executor;
- ChatGPT = independent fresh-GitHub reviewer / scientific-route advisor / task issuer / governance operator;
- Owner = final scientific-direction authority;
- Builder completion is not acceptance.

Priority:

`Scientific correctness > Experiment reproducibility > Research iteration speed > Git auditability > Documentation completeness`

## Current Builder state

Current published task:

**Issue #28 — DLH-5E: Implement conservative stationary-KFE validator and test canonical boundary-policy gate**

Task type:

`SCIENTIFIC_IMPLEMENTATION_VALIDATION__CONSERVATIVE_STATIONARY_KFE_CANDIDATE`

Builder authority becomes active only when Issue #28 remains open, Task Index/Startup identity is synchronized, and the authoritative activation comment is present.

Dedicated branch:

`dsh/issue-28-dlh-5e-conservative-kfe-validation-2026-09-01`

DLH-5E is implementation-validation only. It does not authorize production household routing or HJB/local-policy mutation.

## Latest accepted gate — Issue #27 / DLH-5D

Accepted candidate integrated to `main`:

`f52b1fbf0cd5c921f73212ea97b494fa102e3de5`

Accepted classification:

`DLH_5D_CONSERVATIVE_STATIONARY_KFE_AND_MATLAB_CONTAMINATION_CONTRACT_ACCEPTED`

Acceptance level:

`L3_COMMIT_OR_PR_VERIFIED__SCIENTIFIC_DESIGN_CONTRACT_ACCEPTED`

Controlling specification:

`docs/specifications/DLH_5D_CONSERVATIVE_STATIONARY_KFE_BOUNDARY_AND_CONTAMINATION_CONTRACT_2026_09_01.md`

Controlling MATLAB provenance audit:

`docs/audits/DLH_5D_MATLAB_KFE_CONTAMINATION_AND_BOUNDARY_PROVENANCE_AUDIT_2026_09_01.md`

## Frozen stationary-KFE contract

The scientific stationary object is:

```text
Q^T g = 0
sum_s g_s * (db*da) = 1   per discrete z state
g_s >= 0 up to tolerance
```

For the source generator:

```text
Q[row,col] > 0, row != col  =>  row -> col
```

`Q V` is backward/HJB action and `Q^T g` is forward/KFE action.

Singularity of unmodified `Q` / `Q^T` is expected. It is not a failure.

MATLAB-style contamination remains authorized as a numerical normalization device:

```text
T = Q^T
replace T[n,:] by identity row
rhs[n] = c > 0
solve
normalize
```

The MATLAB provenance pin is `floor(0.37*N)-1` in 0-based indexing with `c=0.007`.

Scientific acceptance requires the normalized contaminated solution to satisfy the ORIGINAL unmodified `Q^T g = 0`; contaminated-system residual alone is insufficient.

## Pin admissibility contract

Stationary uniqueness, pin admissibility and pin invariance are distinct.

For a one-dimensional stationary nullspace, component pin `g_n=c>0` is admissible only when the stationary vector has nonzero support at state `n`.

Successor pin classes are:

- `PIN_VALID_STATIONARY_NORMALIZATION`;
- `PIN_INADMISSIBLE_ZERO_STATIONARY_SUPPORT`;
- `PIN_NUMERICAL_FAILURE_UNRESOLVED`.

Only valid pins are compared for invariance. At least two valid pins must agree within tolerance on the canonical fixture.

The default MATLAB parity pin must itself be valid before any future production use. If it is non-valid, do not auto-switch the production pin; stop for scientific review.

## Conservative finite-grid boundary contract

The admitted finite-grid generator must satisfy:

```text
row-sum max abs <= 1e-12
off-diagonal rates >= -1e-12
Q[i,i] = -sum_{j!=i} admitted Q[i,j]
```

An omitted outward destination may not retain its exit rate in the diagonal.

But mechanical conservation is not enough. The implementation must distinguish:

- requested/economic outward boundary rate;
- admitted generator rate.

Frozen canonical threshold:

`max requested outward boundary rate <= 1e-10`.

A larger requested rate is `BOUNDARY_POLICY_VIOLATION` and blocks scientific acceptance even if the candidate generator is mechanically conservative.

## Issue #28 exact execution order

1. Reuse the exact accepted canonical D0 HJB fixture (`wbar=1`, `r_a=0.03`) with no grid/parameter/price change.
2. Use accepted HJB output read-only and reconstruct requested `mu_b/mu_a` directional rates.
3. Report lower/upper b and a outward requested rates with coordinates.
4. Assemble the conservative no-outflow candidate generator alongside the faithful source.
5. If D0 requested outward rate exceeds `1e-10`, reproduce D0 once, persist evidence, classify `BLOCKED_DLH_5E_BOUNDARY_POLICY_VIOLATION__OWNER_BOUNDARY_POLICY_DECISION_REQUIRED`, and STOP before stationary-density/aggregate acceptance.
6. Only if D0 boundary policy passes, validate generator conservation, unique stationary structure, pin admissibility/invariance and ORIGINAL residual.
7. Only if stationary KFE passes, recompute D0 `C,L,A,B`; require finite `A>0`; re-derive candidate `Z*,delta*` with accepted formulas.
8. Only after full D0 success, run exact D1-D3 household/KFE regression and deterministic repeat.
9. No two-region outer iteration in Issue #28.

Exact D1-D3 states if reached:

```text
D1: wbar=0.9977278388290097, r_a=0.0299127630152404
D2: wbar=0.998807521160338,  r_a=0.029964194758276677
D3: wbar=1.0011941548981047, r_a=0.03003565330704072
```

## Frozen numerical tolerances

```text
generator row-sum max abs              <= 1e-12
negative off-diagonal magnitude        <= 1e-12
original stationary residual ||Q^T g|| <= 1e-10
mass normalization error               <= 1e-12
minimum density                        >= -1e-12
valid-pin normalized-density max diff  <= 1e-10
repeat numeric difference              <= 1e-12
boundary requested outward rate        <= 1e-10
```

No tolerance may be loosened to seek PASS.

## Issue #28 allowed paths

Builder may create only:

1. `src/deep_learning_hank/two_asset/conservative_stationary_kfe.py`
2. `configs/dlh_5e_conservative_stationary_kfe_validation.toml`
3. `tests/test_dlh_5e_conservative_stationary_kfe.py`
4. `reports/dlh_5e_conservative_stationary_kfe_validation_2026_09_01/` with the exact evidence files listed in Issue #28.

No existing file may be modified by Builder.

The accepted MATLAB-faithful source remains immutable:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

## Earlier accepted foundation

### Issue #26 / DLH-5C

Accepted fixed-row artifact diagnosis. Current row-295 KFE-dependent household aggregates are not validated stationary-equilibrium quantities.

### Issue #25 / DLH-5B

Two-region synchronous/Jacobi wiring, labor/network accounting, outer-map and trace/reproducibility architecture accepted. KFE-dependent `C/L/A/B`, `Z/delta` and perturbed equilibrium require revalidation.

### Issue #24 / DLH-5A

Network-ready two-region real structural contract accepted.

### Issue #23

MATLAB-faithful two-asset HJB / transfer-FOC parity repair accepted. The faithful source is provenance/parity authority and remains unchanged in DLH-5E.

## Current scientific route

1. accepted HJB/HA foundation;
2. accepted two-region contract and architecture;
3. accepted KFE blocker diagnosis;
4. accepted conservative KFE / contamination scientific contract;
5. **current: DLH-5E conservative stationary-KFE candidate + D0 boundary-policy validation**;
6. if boundary-policy blocker occurs, Owner decides HJB state-constraint/boundary-policy redesign before further implementation;
7. if DLH-5E passes, separately authorize production integration + two-region S0/S1 revalidation;
8. only after trusted household/KFE and two-region path resume OD / learned `W^L` / larger-region / nominal-HANK tracks.

## Scientific ceiling during Issue #28

No modification of accepted HJB/local-policy source, no production KFE integration, no regional outer iteration, no grid expansion, no parameter retuning, no automatic replacement pin, no learned network, no larger-region scaling, no nominal HANK, no calibration, no policy/welfare/Results.

## DSH startup sequence

1. `Set-Location D:\deep-learning-hank`;
2. verify repo/remote/worktree;
3. `git fetch origin` and record fresh `origin/main`;
4. read all CURRENT rules;
5. read fresh Task Index and this Startup Snapshot;
6. read Issue #28 latest body/comments and verify activation;
7. read accepted Issue #27 contract/audit and Issues #23-#26 evidence;
8. read accepted MATLAB-faithful household/HJB source read-only;
9. create exact Issue #28 dedicated branch from fresh `origin/main`;
10. create/run only the Issue #28 allowlist;
11. explicit stage, commit/push branch, STOP for fresh ChatGPT review.