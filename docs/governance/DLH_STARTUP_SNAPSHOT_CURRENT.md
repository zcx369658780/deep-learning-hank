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

**Issue #29 — DLH-5F: Diagnose upper-domain adequacy and stationary-tail behavior on the frozen two-asset household**

Task type:

`SCIENTIFIC_DIAGNOSTIC__UPPER_DOMAIN_ADEQUACY_AND_STATIONARY_TAIL`

Builder authority is active only while Issue #29 remains open, Task Index/Startup identity matches, and the authoritative activation comment is present.

Dedicated branch:

`dsh/issue-29-dlh-5f-upper-domain-stationary-tail-2026-09-01`

Current master roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`

Current scientific handoff:

`docs/governance/DLH_HANDOFF_2026_09_01_UPPER_DOMAIN_STATIONARY_TAIL_ROUTE.md`

## Latest accepted gate — Issue #28 / DLH-5E

Accepted candidate integrated to `main`:

`a49c19bbc3257f62bebecc26fe7d88ddcc143d9c`

Accepted classification:

`DLH_5E_IMPLEMENTATION_VALIDATION_ACCEPTED__D0_BOUNDARY_POLICY_VIOLATION_CONFIRMED__OWNER_HJB_BOUNDARY_DECISION_REQUIRED`

Acceptance level:

`L3_COMMIT_OR_PR_VERIFIED`

Scientific evidence level:

`D2_MACHINE_NUMERICAL_DIAGNOSTIC__HUMAN_REVIEWED_BOUNDARY_POLICY_BLOCKER`

Accepted D0:

```text
wbar = 1.0
r_a  = 0.03
```

Accepted boundary facts:

- HJB converged in 11 iterations;
- upper-b has 3 states above `1e-10`, max about `0.353747704` at `(19,19,1)`;
- upper-a has 28 states above `1e-10`, max about `0.264071883` at `(14,19,1)`;
- lower boundaries have no material outward request;
- mechanical conservative candidate has row-sum max abs `6.106227e-16`, negative off-diagonal magnitude `0`;
- no clipped stationary density / new `C,L,A,B` / anchor is accepted.

## Controlling stationary-KFE contract

Issue #27 remains binding:

```text
Q^T g = 0
sum_s g_s * (db*da) = 1 per discrete z state
g_s >= 0 up to tolerance
```

Singular `Q/Q^T` is expected.

MATLAB-style component pinning remains allowed only with conservative generator, recurrent-class/nullspace evidence, pin admissibility, ORIGINAL residual, mass/non-negativity and valid-pin invariance. The pin is a scale device followed by separate mass normalization.

## Binding HJB/KFE consistency principle

```text
HJB boundary policy <=> KFE boundary transition law
```

Backward and forward equations must describe the same controlled process.

A mechanically no-outflow `Q_c` is not an accepted economic stationary process if the HJB still requests material outward motion at the same boundary.

## DLH-5F exact frozen experiment

All variants use the exact accepted D0 non-grid economics/prices, HJB numerics and accepted initialization formula independently on each grid. No warm start.

Baseline spacings:

```text
db0 = 7/19
da0 = 10/19
```

Exact variants:

1. `V0_BASE`: b20 `[-2,5]`, a20 `[0,10]`.
2. `V1_A_WIDE`: b20 baseline, a40 `[0,390/19]`.
3. `V2_B_WIDE`: b40 `[-2,235/19]`, a20 baseline.
4. `V3_AB_MID`: b30 `[-2,165/19]`, a30 `[0,290/19]`.
5. `V4_AB_WIDE`: b40 `[-2,235/19]`, a40 `[0,390/19]`.
6. `V5_BASE_FINE`: b39 `[-2,5]`, a39 `[0,10]`, half baseline spacing.

No additional/adaptive grid is authorized.

## DLH-5F required diagnostic order

1. Fresh HJB on all six variants.
2. Full requested-rate diagnostics on all four asset boundaries: max, quantiles, counts/shares, complete index and physical-coordinate sets.
3. Shared-interior comparison at exact aligned nodes with primary mask `b_index<=17`, `a_index<=17`, all z.
4. Mechanical conservative-generator diagnostics.
5. Stationary/nullspace/pin validation only for variants with `max requested outward <=1e-10` so HJB/KFE share the same admissible boundary process.
6. Boundary/near-boundary mass and probability-weighted flux only from a scientifically admissible density.
7. `C,L,A,B` only after stationary validity.
8. Full six-variant deterministic repeat plus applicable full regression suite.

If material boundary requested policy remains, stationary/tail/aggregate fields must be `NOT_REACHED__HJB_KFE_SAME_PROCESS_BOUNDARY_GATE_FAILED`; do not manufacture a density using old leakage or independent clipping.

## Exact Builder allowlist

Builder may create only:

1. `src/deep_learning_hank/two_asset/upper_domain_stationary_tail_diagnostic.py`
2. `configs/dlh_5f_upper_domain_stationary_tail_diagnostic.toml`
3. `tests/test_dlh_5f_upper_domain_stationary_tail_diagnostic.py`
4. `reports/dlh_5f_upper_domain_stationary_tail_diagnostic_2026_09_01/` with exactly eight files:
   - `DLH_5F_VARIANT_STATUS.csv`
   - `DLH_5F_BOUNDARY_POLICY_DIAGNOSTICS.csv`
   - `DLH_5F_INTERIOR_POLICY_STABILITY.csv`
   - `DLH_5F_STATIONARY_TAIL_DIAGNOSTICS.csv`
   - `DLH_5F_AGGREGATE_STABILITY.csv`
   - `DLH_5F_REPRODUCIBILITY.json`
   - `DLH_5F_EXECUTION_REPORT.md`
   - `DLH_5F_FORBIDDEN_OPERATION_CHECK.md`

No existing tracked file may be modified by Builder.

## Scientific ceiling during Issue #29

Do not:

- modify accepted HJB/local-policy/KFE/regional source;
- change economics/prices/tolerances;
- warm-start or adaptively add grids;
- clip HJB policy to seek PASS;
- accept a density from a different controlled process;
- use old row-295 density as economic evidence;
- run D1–D3, two-region outer iteration, 3–5/31-province GE, or the future `31_PROVINCE_HOUSEHOLD_UPPER_DOMAIN_AUDIT`;
- train `W^L` or any neural network;
- enter nominal HANK / calibration / policy / welfare / Results;
- create PR / merge / close / successor / self-accept.

## Multi-province reference status

The neighboring project remains:

> a highly mature source-faithful multi-province reconstruction under active MATLAB–Python stationary parity adjudication

It is a reference/source-contract provider, not yet a fully parity-accepted production oracle.

Permanent regional hierarchy remains:

```text
2-region unit fixture
-> 3–5 province integration fixture
-> 31-province empirical/source benchmark
```

Future regional parity must separately inspect continuous-state parity and discrete-controller branch parity.

## DSH startup sequence

1. `Set-Location D:\deep-learning-hank`;
2. verify repository/remote/worktree;
3. `git fetch origin` and record fresh `origin/main`;
4. read all CURRENT rules;
5. read `tasks/TASK_INDEX_CURRENT.md` and this Startup Snapshot;
6. read current Roadmap and Handoff;
7. read Issue #29 full body and latest comments, verify activation;
8. read accepted Issues #27–#28 controlling evidence and the accepted MATLAB-faithful HJB / DLH-5E diagnostic helper read-only;
9. create exact dedicated branch from fresh main;
10. operate only in the Issue #29 allowlist;
11. explicit-stage, commit/push, STOP for fresh ChatGPT review.

Chat text is not Builder authority.
