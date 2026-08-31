# Deep Learning + HANK Startup Snapshot — CURRENT

Date: 2026-08-31

Repository: `zcx369658780/deep-learning-hank`

Local Owner-designated workspace: `D:\deep-learning-hank`

## Governance state

- live GitHub `main` = synchronized repository/governance authority;
- GitHub Issue = sole DSH Builder authority after publication + activation;
- DSH = bounded Builder/executor;
- ChatGPT = independent fresh-GitHub reviewer / scientific-route authority / task issuer / governance operator;
- Owner = final scientific-direction authority;
- Builder completion is not acceptance.

Priority:

`Scientific correctness > Experiment reproducibility > Research iteration speed > Git auditability > Documentation completeness`

## Current Builder state

Current published task:

**Issue #26 — DLH-5C: Diagnose stationary KFE contaminated-row singularity on the preserved two-region perturbed path**

Task type:

`SCIENTIFIC_DIAGNOSTIC__STATIONARY_KFE_SINGULARITY_ON_REGIONAL_PATH`

Builder authority is active only when Issue #26 remains open, Task Index/Startup identity is synchronized, and the authoritative activation comment is present.

Dedicated branch after activation:

`dsh/issue-26-dlh-5c-kfe-singularity-diagnostic-2026-08-31`

DLH-5C is diagnostic only. It may create only the exact new diagnostic script/config/test/report-root paths authorized by Issue #26. It may not modify the accepted household oracle, accepted regional fixed-point implementation/config, prior evidence, roadmap/governance or legacy sources.

## Latest accepted implementation gate

Issue #25 — DLH-5B

Accepted candidate merged to `main`:

`4c97ae30d98c40466af3ff11ce8048e5e5087335`

Accepted reviewer classification:

`DLH_5B_TWO_REGION_ARCHITECTURE_ACCEPTED__PERTURBED_FIXED_POINT_BLOCKED_BY_REPRODUCIBLE_HOUSEHOLD_KFE_SINGULARITY`

Acceptance level:

`L3_COMMIT_OR_PR_VERIFIED`

Scientific numerical evidence level:

`D2_MACHINE_NUMERICAL_EVIDENCE__NO_STRONG_ECONOMIC_RESULTS_CLAIM`

### Accepted positive evidence

- two-region real structural prototype implements the accepted DLH-5A `K_i=M_i*A_i`, hand-specified labor network and synchronous/Jacobi outer map;
- accepted household oracle remains unchanged;
- deterministic anchor derives finite `A*=8.9586992251`, `L*=0.992496736638`, `Z*=0.720420345882`, `delta*=0.0253929042432`;
- S0 anchor one-turn passes at machine precision: `R_w=2.220e-16`, `R_ra=6.939e-18`;
- labor-origin conservation, economy labor conservation, gross wage-bill consistency, network, KFE and firm gates pass at S0;
- S2 region-order invariance is exact (`0.0`);
- R1 adds complete per-turn validity enforcement, full trace `P^L/lambda/Gamma_next`, NaN/Inf-aware numeric comparison, and fail-closed terminal classification;
- R1 scientific results are identical to predecessor evidence on all common fields.

### Preserved negative evidence

S1 starts from:

```text
w_1=0.99, w_2=1.01
r_1^a=0.0295, r_2^a=0.0305
lambda=0.5
```

The first three valid turns reduce residuals:

```text
R_w:  0.00933470495 -> 0.00504853749 -> 0.00270360504
R_ra: 0.00058124990 -> 0.00024618752 -> 0.00010286349
```

Turn 4 region 0 then fail-closes at the accepted household stationary KFE with:

`faithful contaminated-row solve is non-finite`.

Exact failing region-0 conditional state:

```text
wbar = 0.998807521160338
r_a  = 0.029964194758276677
```

This failure is deterministic and repeated exactly. No tuning, retry or grid expansion was used.

S0 also shows `a_max` boundary mass near `0.196`, above the architecture-stage warning threshold `0.10`. This warning is preserved and means the fixture is not substantive distribution-validation evidence.

## Accepted structural contract

Issue #24 / DLH-5A remains controlling for A1/A2 economics:

- two-region real structural HA-GE prototype first;
- `K_i=M_i*A_i` provisional private capital;
- `B_i` liquid-asset diagnostic only;
- hand-specified `m^L/W^L/P^L`, `F^L`, `L^dest`, composite `wbar`;
- synchronous old-state outer mapping;
- common `r_b`, regional tax/transfer exogenous;
- genuine nominal HANK deferred.

Canonical household source:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Accepted blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Current accepted stationary KFE implementation uses:

```text
transpose = operator.T
row = floor(0.37*N)-1
contaminated[row,:] = 0
contaminated[row,row] = 1
rhs[row] = 0.007
raw = spsolve(contaminated,rhs)
```

and fail-closes if `raw` is non-finite.

## DLH-5C exact diagnostic authority

Issue #26 freezes four exact cases:

### D0 anchor control

```text
wbar=1.0
r_a=0.03
```

### D1 last valid region-0 S1 input

```text
wbar=0.9977278388290097
r_a=0.0299127630152404
```

### D2 exact failing region-0 S1 input

```text
wbar=0.998807521160338
r_a=0.029964194758276677
```

### D3 same-turn region-1 valid control

```text
wbar=1.0011941548981047
r_a=0.03003565330704072
```

Issue #26 also freezes one 9-point linear scan D1->D2 for region 0, no adaptive refinement.

Required diagnostic families:

- HJB and accepted KFE success/failure reproduction;
- sparse operator finite/nnz/diagonal/off-diagonal/row-sum/rank diagnostics;
- accepted contaminated-row index and coordinates;
- positive-transition strongly connected / closed-class graph structure;
- deterministic diagnostic row-pin set `{0,floor(N/4),accepted row,floor(N/2),floor(3N/4),N-1}`;
- optional bounded sparse smallest-singular-value diagnostics for D1/D2;
- exact repeat reproducibility.

Alternative row pins are diagnostic only and do not become solver authority.

## DLH-5C explicit non-authority

No:

- household-oracle mutation;
- regional fixed-point mutation;
- solver repair;
- alternative production row pin;
- regularization/jitter/pseudoinverse in production;
- grid/parameter/S1-path tuning;
- retry/adaptive scan;
- `B=1`, `GovInv`, learned `W^L/W^K`, neural training;
- nominal HANK;
- larger-region scaling;
- policy/welfare/Results claims.

## Current scientific route

Working label: `Network-Structured Regional HANK (NSR-HANK)`.

Sequence now:

1. accepted two-asset household foundation;
2. accepted two-region structural contract;
3. accepted deterministic two-region architecture implementation;
4. **current: diagnose the exact reproducible stationary KFE blocker**;
5. after fresh review, decide whether the evidence supports a numerical repair and whether that repair requires new Owner scientific authority;
6. only after the regional fixed-point path is trustworthy proceed to OD-year labor-flow data/baseline and learned `W^L`;
7. later 3–5 regions, genuine nominal HANK, `W^K`, equilibrium-constrained calibration, 31-region panel and policy/welfare.

## Scientific ceiling during Issue #26

DLH-5C may establish a root-cause diagnostic classification only.

It does not establish a repaired KFE, converged perturbed two-region equilibrium, learned network, empirical calibration, nominal regional HANK, 31-region results or paper Results authority.

## DSH startup sequence

1. `Set-Location D:\deep-learning-hank`;
2. verify repo/remote/worktree;
3. `git fetch origin` and record fresh `origin/main`;
4. read all CURRENT rules;
5. read fresh Task Index and this Startup Snapshot;
6. read Issue #26 latest body/comments and verify activation;
7. read accepted Issue #25 implementation/evidence and Issue #24 contract;
8. read the accepted household HJB/KFE source read-only;
9. create the exact Issue #26 dedicated branch from fresh `origin/main`;
10. create/run only the Issue #26 diagnostic allowlist;
11. commit/push and STOP for fresh ChatGPT review.
