# Deep Learning + HANK Task Index

Status: `ACTIVE_BUILDER_ISSUE__DLH_5F_UPPER_DOMAIN_ADEQUACY_AND_STATIONARY_TAIL`

Last synchronized: 2026-09-01

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

Current Issue:

**Issue #29 — OPEN**

Title:

`DLH-5F: Diagnose upper-domain adequacy and stationary-tail behavior on the frozen two-asset household`

Task type:

`SCIENTIFIC_DIAGNOSTIC__UPPER_DOMAIN_ADEQUACY_AND_STATIONARY_TAIL`

Issue #29 becomes the sole DSH Builder authority only after the authoritative activation comment is present and the CURRENT Startup Snapshot is synchronized to the same Issue.

Dedicated branch:

`dsh/issue-29-dlh-5f-upper-domain-stationary-tail-2026-09-01`

DSH must fresh-fetch `origin/main`, read all CURRENT rules, this Task Index, the CURRENT Startup Snapshot, the current Roadmap/Handoff, Issue #29 full body/latest comments, accepted Issues #27–#28 authority, and the accepted MATLAB-faithful household/HJB source before any mutation.

If Issue #29 is not open, activation is absent, or Issue/Task Index/Startup identity differs, DSH must fail closed.

## Issue #29 scientific scope

DLH-5F is a bounded **diagnostic** task. It does not authorize a new HJB boundary law, a new KFE process, regional GE, calibration, learned networks, or Results.

Frozen D0 economics/prices remain:

```text
wbar = 1.0
r_a  = 0.03
```

All non-grid parameters, prices, taxes/transfers, productivity process, HJB numerics, drift tolerance and initialization logic remain exactly the accepted DLH-5B/DLH-5E fixture.

Binding consistency law:

```text
HJB boundary policy <=> KFE boundary transition law
```

A mechanically clipped conservative KFE is not accepted as the stationary process of an HJB that requests material outward boundary drift.

## Exact six pre-frozen grid variants

No adaptive seventh variant is authorized.

1. `V0_BASE`: b 20 on `[-2,5]`; a 20 on `[0,10]`.
2. `V1_A_WIDE`: b baseline; a 40 on `[0,390/19]`.
3. `V2_B_WIDE`: b 40 on `[-2,235/19]`; a baseline.
4. `V3_AB_MID`: b 30 on `[-2,165/19]`; a 30 on `[0,290/19]`.
5. `V4_AB_WIDE`: b 40 on `[-2,235/19]`; a 40 on `[0,390/19]`.
6. `V5_BASE_FINE`: b 39 on `[-2,5]`; a 39 on `[0,10]`, half baseline spacing.

V0–V4 preserve exact baseline spacing on expanded dimensions; V5 contains every V0 node at every second grid point.

## Required evidence sequence

1. Fresh accepted HJB on all six variants; no warm start.
2. Full upper/lower requested-rate diagnostics: max, positive quantiles, counts/shares, argmax and complete physical/index coordinate sets.
3. Shared-interior policy comparison at exact aligned nodes using the frozen V0 mask `b_index<=17`, `a_index<=17`, all z.
4. Mechanical conservative-generator diagnostics only; row sums/off-diagonals do not self-authorize KFE acceptance.
5. Stationary/nullspace/pin/tail/aggregate validation only for variants with `max requested outward <=1e-10` under the same HJB/KFE controlled process.
6. Boundary/near-boundary mass and probability-weighted flux only from a scientifically admissible density.
7. `C,L,A,B` only after stationary validity; no historical row-295 aggregate.
8. Full six-variant deterministic repeat and applicable repository regression suite.

## Exact Builder allowlist

Builder may create only:

1. `src/deep_learning_hank/two_asset/upper_domain_stationary_tail_diagnostic.py`
2. `configs/dlh_5f_upper_domain_stationary_tail_diagnostic.toml`
3. `tests/test_dlh_5f_upper_domain_stationary_tail_diagnostic.py`
4. `reports/dlh_5f_upper_domain_stationary_tail_diagnostic_2026_09_01/` with exactly:
   - `DLH_5F_VARIANT_STATUS.csv`
   - `DLH_5F_BOUNDARY_POLICY_DIAGNOSTICS.csv`
   - `DLH_5F_INTERIOR_POLICY_STABILITY.csv`
   - `DLH_5F_STATIONARY_TAIL_DIAGNOSTICS.csv`
   - `DLH_5F_AGGREGATE_STABILITY.csv`
   - `DLH_5F_REPRODUCIBILITY.json`
   - `DLH_5F_EXECUTION_REPORT.md`
   - `DLH_5F_FORBIDDEN_OPERATION_CHECK.md`

No existing tracked file may be modified by Builder.

## Explicit scientific ceiling

Do not:

- modify accepted HJB/local-policy/KFE/regional source;
- modify accepted Issues #23–#28 evidence;
- change economic parameters/prices/tolerances;
- warm-start across grids;
- adaptively expand the grid;
- clip HJB policy to seek PASS;
- compute economic stationary density from a different boundary process;
- use old row-295 density as evidence;
- run D1–D3, two-region outer iteration, 3–5/31-province GE, or the future `31_PROVINCE_HOUSEHOLD_UPPER_DOMAIN_AUDIT`;
- train `W^L` or any neural network;
- enter nominal HANK / calibration / policy / welfare / Results;
- create PR / merge / close / successor / self-accept.

## Latest accepted task

Issue #28 — DLH-5E — ACCEPTED / COMPLETED.

Accepted candidate integrated to main:

`a49c19bbc3257f62bebecc26fe7d88ddcc143d9c`

Accepted classification:

`DLH_5E_IMPLEMENTATION_VALIDATION_ACCEPTED__D0_BOUNDARY_POLICY_VIOLATION_CONFIRMED__OWNER_HJB_BOUNDARY_DECISION_REQUIRED`

Accepted D0 facts remain:

- HJB converged in 11 iterations;
- upper-b max about `0.353747704`, 3 material states;
- upper-a max about `0.264071883`, 28 material states;
- mechanical `Q_c` row-sum max abs `6.106227e-16`, negative off-diagonal magnitude `0`;
- no clipped density / new `C,L,A,B` / anchor accepted.

## Current route authority

- Roadmap: `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
- Handoff: `docs/governance/DLH_HANDOFF_2026_09_01_UPPER_DOMAIN_STATIONARY_TAIL_ROUTE.md`
- Issue #29 full body is the exact experiment authority once activation is complete.
