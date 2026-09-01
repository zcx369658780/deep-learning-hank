# Deep Learning + HANK Task Index

Status: `ACTIVE_BUILDER_ISSUE__DLH_5H_ILLIQUID_UPPER_BOUNDARY_RESOLUTION`

Last synchronized: 2026-09-01

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

Current Issue:

**Issue #34 — OPEN**

Title:

`DLH-5H: Isolate illiquid upper-boundary resolution on the provisional liquid-safe domain`

Task type:

`SCIENTIFIC_DIAGNOSTIC__ILLIQUID_UPPER_BOUNDARY_RESOLUTION`

Dedicated branch:

`dsh/issue-34-dlh-5h-illiquid-resolution-2026-09-01`

Issue #34 becomes the sole DSH Builder authority only after the authoritative activation comment is present and the CURRENT Startup Snapshot is synchronized to the same Issue.

If Issue #34 is not open, activation is absent, or Issue / Task Index / Startup identity differs, DSH must fail closed.

## Latest accepted task — Issue #31 / DLH-5G

Accepted candidate:

`edbd6e9d4683118e08edb8041609c9af1579883a`

Integrated to `main` by acceptance merge commit:

`809d18a3459b5b8c4d8b142ea4f282a34c3af49f`

Accepted reviewer verdict:

`DLH_5G_ISSUE_31_IMPLEMENTATION_ACCEPTED__LIQUID_UPPER_DOMAIN_ADEQUACY_EVIDENCE_CONFIRMED__B_RESOLUTION_SENSITIVITY_RETAINED__ILLIQUID_BOUNDARY_REMAINS_BLOCKER`

Accepted interpretation:

- same-spacing liquid sequence drives upper-b raw/requested drift from `0.1303281015/0.3537477040` to `0.003759131181/0.01020335606`, then to exact `0/0` at `b_max=19.7368421053`, remaining zero at the wider same-spacing extent;
- a finer b-grid reaches zero already at `b_max=12.3684210526`, so liquid behavior is resolution-sensitive but consistent with finite-domain adequacy rather than persistent outward liquid drift;
- `b60 [-2,375/19]`, `db=7/19` is designated a **provisional liquid-safe diagnostic domain**, not a final production-grid freeze;
- upper-a remains material on that state: requested max about `0.3094730854`, 108 states, share `0.90`;
- stationary KFE remains NOT AUTHORIZED.

## Issue #34 scientific scope

DLH-5H isolates **illiquid-grid resolution** while preserving the accepted household process.

Frozen for all variants:

```text
wbar = 1.0
r_a = 0.03
a_lo = 0
a_hi = 10
a_max = 10
accepted taper = r_a*(1-0.1*(a/a_max)^9)
```

Core liquid-safe domain:

```text
b: 60 points on [-2,375/19]
db = 7/19
```

Primary question:

> With the physical a-domain, a_max, taper, economics and liquid-safe domain fixed, does upper-a raw outward drift attenuate to the HJB/KFE compatibility threshold when only a-grid resolution is refined?

DLH-5H is policy-only. It does not authorize stationary KFE, nullspace/pin, density, tail metrics or `C,L,A,B`.

## Exact six pre-frozen variants

1. `H0_A20_BASE`: b60 core domain; a20 `[0,10]`, `da=10/19`.
2. `H1_A39_FINE`: same b60; a39 `[0,10]`, half `da`.
3. `H2_A77_FINER`: same b60; a77 `[0,10]`, quarter baseline `da`.
4. `H3_A153_FINEST`: same b60; a153 `[0,10]`, eighth baseline `da`.
5. `H4_B119_A39`: b119 on same b-domain, half `db`; a39.
6. `H5_B119_A77`: b119 on same b-domain, half `db`; a77.

No seventh/adaptive grid or PASS-seeking search is authorized.

## Required evidence

1. Fresh accepted HJB on all six variants; no warm start.
2. Upper/lower a raw-drift and requested-rate diagnostics with max, quantiles, counts/shares, argmax and complete offending states.
3. Upper/lower b regression diagnostics on every variant; fail closed if liquid boundary materially reactivates.
4. Primary a-resolution trend `H0 -> H1 -> H2 -> H3` with raw/requested maxima and attenuation ratios.
5. Exact aligned policy comparisons: `H0/H1`, `H1/H2`, `H2/H3`, `H1/H4`, `H2/H5`.
6. Per-variant joint HJB upper-boundary policy compatibility marker only; no stationary solve.
7. Deterministic repeat and applicable full repository regression suite.

## Exact Builder allowlist

Builder may create only:

1. `src/deep_learning_hank/two_asset/illiquid_upper_boundary_resolution_diagnostic.py`
2. `configs/dlh_5h_illiquid_upper_boundary_resolution_diagnostic.toml`
3. `tests/test_dlh_5h_illiquid_upper_boundary_resolution_diagnostic.py`
4. `reports/dlh_5h_illiquid_upper_boundary_resolution_diagnostic_2026_09_01/` with exactly:
   - `DLH_5H_VARIANT_STATUS.csv`
   - `DLH_5H_ILLIQUID_BOUNDARY_DIAGNOSTICS.csv`
   - `DLH_5H_LIQUID_REGRESSION_DIAGNOSTICS.csv`
   - `DLH_5H_RESOLUTION_TREND.csv`
   - `DLH_5H_POLICY_STABILITY.csv`
   - `DLH_5H_REPRODUCIBILITY.json`
   - `DLH_5H_EXECUTION_REPORT.md`
   - `DLH_5H_FORBIDDEN_OPERATION_CHECK.md`

No existing tracked file may be modified by Builder.

## Scientific ceiling

Do not modify accepted HJB/KFE/regional source or Issues #23–#31 evidence; do not change physical a-domain, `a_max=10`, taper, economics/prices/parameters/tolerances/initialization; no a-domain widening, warm-start, adaptive grid or clipping; no stationary KFE/density/tail/aggregates; no D1-D3, regional GE, multi-province audit, neural training, nominal HANK, calibration, policy/welfare or Results.

No PR / merge / close / successor Issue / self-accept from Builder.

## Current route authority

- Issue #34 full body + authoritative activation comment = exact Builder experiment authority once activation is posted.
- Startup Snapshot: `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
- Roadmap: `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
- Earlier handoff remains historical context: `docs/governance/DLH_HANDOFF_2026_09_01_UPPER_DOMAIN_STATIONARY_TAIL_ROUTE.md`
