# Deep Learning + HANK Task Index

Status: `ACTIVE_BUILDER_ISSUE__DLH_5G_LIQUID_UPPER_DOMAIN_ASYMPTOTIC_AND_RESOLUTION`

Last synchronized: 2026-09-01

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

Current Issue:

**Issue #31 — OPEN**

Title:

`DLH-5G: Isolate liquid upper-domain asymptotics under fixed illiquid domain and taper`

Task type:

`SCIENTIFIC_DIAGNOSTIC__LIQUID_UPPER_DOMAIN_ASYMPTOTIC_AND_RESOLUTION`

Dedicated branch:

`dsh/issue-31-dlh-5g-liquid-upper-domain-asymptotic-2026-09-01`

Issue #31 becomes the sole DSH Builder authority only after the authoritative activation comment is present and the CURRENT Startup Snapshot is synchronized to the same Issue.

If Issue #31 is not open, activation is absent, or Issue / Task Index / Startup identity differs, DSH must fail closed.

## Latest accepted task — Issue #29 / DLH-5F

Accepted candidate:

`7f4e489154115c9c91cf8c3fccbb3a1d114fbc3f`

Integrated to `main` by acceptance merge commit:

`8eaac27472e3f902d0ff3e8044027f95913155ba`

Accepted reviewer verdict:

`DLH_5F_ISSUE_29_IMPLEMENTATION_ACCEPTED__OUTCOME_B_CONFIRMED__OUTCOME_D_SUPPORTED_WITH_INTERPRETATION_CORRECTION__STATIONARY_TAIL_NOT_REACHED`

Accepted reviewer annotation:

`B_EXTENT_EVIDENCE_SHOWS_STRONG_ATTENUATION_NOT_GROWTH__A_EXTENT_CONFOUNDED_BY_AMAX_NORMALIZED_RETURN_TAPER__RESOLUTION_NOT_YET_STABLE`

Controlling scientific interpretation:

- clean b-only `V0 -> V2` holds `a_max=10`, a-grid/taper and `db` fixed; upper-b requested rate falls from about `0.353747704` to `0.010203356` with highly stable shared-interior policy;
- changing `a_max` changes the accepted MATLAB-faithful effective illiquid return `r_a*(1-0.1*(a/a_max)^9)`, so V1/V3/V4 are not pure a-domain extent experiments;
- V5 keeps `a_max=10` and removes upper-a outward requests, showing strong upper-a resolution/local-discretization sensitivity;
- no DLH-5F variant reached full HJB/KFE same-process stationary validation, so stationary-tail existence/non-existence and new `C,L,A,B` remain NOT REACHED.

## Issue #31 scientific scope

DLH-5G isolates the liquid upper boundary only. It preserves the accepted household HJB and freezes the entire illiquid side:

```text
wbar = 1.0
r_a  = 0.03
a = 20 points on [0,10]
a_max = 10
da = 10/19
accepted illiquid-return taper unchanged
```

Primary question:

> With fixed illiquid domain/taper and fixed economics, does raw upper-b outward drift `max(mu_b,0)` attenuate toward zero as `b_max` is extended, and how sensitive is that conclusion to an independent b-resolution refinement?

Raw `mu_b` is the primary cross-resolution quantity. Requested generator rate `max(mu_b,0)/db` remains the HJB/KFE boundary-compatibility quantity.

DLH-5G is policy-only. It does **not** authorize stationary KFE, nullspace/pin, density, tail mass, stationary flux, `C,L,A,B`, HJB boundary redesign or a-taper redesign.

## Exact six pre-frozen variants

All use the same a20 `[0,10]` grid and `a_max=10` taper.

1. `G0_BASE`: b20 `[-2,5]`, `db=7/19`.
2. `G1_B_WIDE_1`: b40 `[-2,235/19]`, same `db`.
3. `G2_B_WIDE_2`: b60 `[-2,375/19]`, same `db`.
4. `G3_B_WIDE_3`: b80 `[-2,515/19]`, same `db`.
5. `G4_BASE_B_FINE`: b39 `[-2,5]`, `db=(7/19)/2`.
6. `G5_WIDE1_B_FINE`: b79 `[-2,235/19]`, `db=(7/19)/2`.

No seventh/adaptive grid or PASS-seeking search is authorized.

## Required evidence

1. Fresh accepted HJB on all six variants; no warm start.
2. Upper/lower b raw-drift diagnostics and requested-rate diagnostics, with max, quantiles, counts/shares, argmax and complete offending states.
3. Upper/lower a requested-rate regression evidence with a-grid/taper identity frozen.
4. Same-spacing extent trend `G0 -> G1 -> G2 -> G3`, including raw/requested maxima and attenuation ratios.
5. Exact aligned resolution comparisons `G0 vs G4` and `G1 vs G5` for value, consumption, labor, transfer, `mu_a`, `mu_b`, and direction-label mismatches.
6. Deterministic repeat and applicable full repository regression suite.
7. No stationary/KFE/aggregate execution path.

## Exact Builder allowlist

Builder may create only:

1. `src/deep_learning_hank/two_asset/liquid_upper_domain_asymptotic_diagnostic.py`
2. `configs/dlh_5g_liquid_upper_domain_asymptotic_diagnostic.toml`
3. `tests/test_dlh_5g_liquid_upper_domain_asymptotic_diagnostic.py`
4. `reports/dlh_5g_liquid_upper_domain_asymptotic_diagnostic_2026_09_01/` with exactly:
   - `DLH_5G_VARIANT_STATUS.csv`
   - `DLH_5G_LIQUID_BOUNDARY_DIAGNOSTICS.csv`
   - `DLH_5G_ILLIQUID_REGRESSION_DIAGNOSTICS.csv`
   - `DLH_5G_EXTENT_TREND.csv`
   - `DLH_5G_RESOLUTION_STABILITY.csv`
   - `DLH_5G_REPRODUCIBILITY.json`
   - `DLH_5G_EXECUTION_REPORT.md`
   - `DLH_5G_FORBIDDEN_OPERATION_CHECK.md`

No existing tracked file may be modified by Builder.

## Scientific ceiling

Do not modify accepted source/evidence, `a_max`, a-grid, taper, economics/prices/parameters/tolerances/initialization; do not warm-start, adapt grids, clip policy, run stationary KFE/density/tail/aggregates, D1-D3, regional GE, multi-province audit, neural training, nominal HANK, calibration, policy/welfare or Results.

No PR / merge / close / successor Issue / self-accept from Builder.

## Current route authority

- Issue #31 full body + authoritative activation comment = exact Builder experiment authority.
- Startup Snapshot: `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
- Roadmap: `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
- Earlier handoff remains historical scientific context: `docs/governance/DLH_HANDOFF_2026_09_01_UPPER_DOMAIN_STATIONARY_TAIL_ROUTE.md`
