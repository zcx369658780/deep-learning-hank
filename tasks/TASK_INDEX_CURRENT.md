# Deep Learning + HANK Task Index

Status: `ACTIVE_BUILDER_ISSUE__DLH_5L_TOTAL_WEALTH_DRIFT_AND_DOMAIN_GEOMETRY`

Last synchronized: 2026-09-01

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

Current Issue:

**Issue #38 — OPEN**

Title:

`DLH-5L: Adjudicate componentwise liquid outward drift versus total-wealth mean reversion and boundary geometry`

Task type:

`SCIENTIFIC_ANALYTICAL_DIAGNOSTIC__TOTAL_WEALTH_DRIFT_AND_DOMAIN_GEOMETRY`

Dedicated branch:

`dsh/issue-38-dlh-5l-total-wealth-domain-geometry-2026-09-01`

Issue #38 becomes the sole DSH Builder authority only after the authoritative activation comment is present and the CURRENT Startup Snapshot is synchronized to the same Issue. If Issue #38 is not open, activation is absent, or Issue / Task Index / Startup identity differs, DSH must fail closed.

## Latest accepted task — Issue #37 / DLH-5K

Accepted candidate:

`aaead4a1368ec061ac1e380c3af33d93c0f31161`

Integrated to `main` by acceptance merge commit:

`d26b2b8c8d69d2afa2cb9806f120d03ebe973752`

Accepted reviewer verdict:

`DLH_5K_ISSUE_37_IMPLEMENTATION_ACCEPTED__MIXED_LOCALIZATION_CONFIRMED__TRANSFER_DERIVATIVE_CHANNEL_DOMINATES_CROSS_A_DIVERGENCE__INTERPRETATION_NARROWED__NEXT_GATE_REQUIRED`

Acceptance level:

`L3_COMMIT_VERIFIED__SCIENTIFIC_ANALYTICAL_DIAGNOSTIC_ACCEPTED`

Accepted interpretation:

- 5/17 material upper-b offenders are boundary-only within the required `n-1/n-2/n-3/n-5` window; 12/17 retain positive full-policy `mu_b` in at least one inspected interior layer;
- this is local persistence, not proof of infinite-domain/high-wealth non-mean-reversion;
- at inspected offenders, `base_liquid_surplus<0` while `transfer_injection>0`, and the transfer-injection channel dominates enough to make `mu_b>0`;
- a77/a153 divergence is primarily transfer/derivative-channel driven;
- the current selected transfer-FOC candidate fails joint inwardness at the inspected joint-corner states, but the algebra does not prove that no feasible transfer exists;
- transfer `d` is a continuous-time flow/rate, not an asset stock; no liquidation interpretation is accepted;
- no source defect or redesign is accepted; pure larger-b-grid continuation remains CLOSED;
- stationary KFE remains NOT AUTHORIZED.

## Issue #38 scientific scope

DLH-5L distinguishes componentwise liquid outward drift from total-wealth outward drift under the accepted household law.

Accepted accounting identities to test:

```text
mu_a = r_a_eff(a)*a + d
mu_b = r_b*b + labor_income - d - adjustment_cost - (consumption - transfer_income)
mu_W = mu_a + mu_b
     = r_a_eff(a)*a + r_b*b + labor_income
       - adjustment_cost - (consumption - transfer_income)
```

The linear transfer term cancels from `mu_W`.

Rerun exactly accepted J0–J5 only. No new grid, extent, resolution, warm start, b100 rerun, b-resolution change or source mutation.

The inspected state set is frozen as the exact union of row coordinates from accepted:

- `reports/dlh_5k_high_wealth_corner_closure_diagnostic_2026_09_01/DLH_5K_BOUNDARY_INTERIOR_LOCALIZATION.csv`
- `reports/dlh_5k_high_wealth_corner_closure_diagnostic_2026_09_01/DLH_5K_CROSS_A_MECHANISM.csv`

Deduplicate exact `(variant,b_index,a_index,z_index)` only; do not add post-hoc states.

Required evidence:

1. exact accepted J0–J5 reproduction;
2. exact `mu_W=mu_a+mu_b` and transfer-cancelled budget reconstruction;
3. four-way component-liquid / total-wealth drift classification;
4. explicit coverage of every accepted DLH-5K interior-positive state;
5. transfer-cancellation / portfolio-reallocation decomposition;
6. analytical comparison of rectangular component bounds with local `W=a+b` normal drift, without changing the production domain;
7. exact a77/a153 aligned total-wealth comparison;
8. deterministic repeat and applicable full regression suite;
9. stop without source/domain redesign or stationary KFE.

## Exact Builder allowlist

Builder may create only:

1. `src/deep_learning_hank/two_asset/total_wealth_domain_geometry_diagnostic.py`
2. `configs/dlh_5l_total_wealth_domain_geometry_diagnostic.toml`
3. `tests/test_dlh_5l_total_wealth_domain_geometry_diagnostic.py`
4. `reports/dlh_5l_total_wealth_domain_geometry_diagnostic_2026_09_01/` with exactly:
   - `DLH_5L_SOURCE_ACCOUNTING_AUDIT.md`
   - `DLH_5L_STATE_DRIFT_DECOMPOSITION.csv`
   - `DLH_5L_COORDINATE_TOTAL_CLASSIFICATION.csv`
   - `DLH_5L_BOUNDARY_GEOMETRY.csv`
   - `DLH_5L_CROSS_A_TOTAL_WEALTH.csv`
   - `DLH_5L_REPRODUCIBILITY.json`
   - `DLH_5L_EXECUTION_REPORT.md`
   - `DLH_5L_FORBIDDEN_OPERATION_CHECK.md`

No existing tracked file may be modified by Builder.

## Scientific ceiling

Do not add any grid/extent/resolution or use `b>b160`; do not modify accepted HJB/KFE/regional source, taper, transfer FOC, adjustment cost, boundary law, economics/prices/parameters/tolerances/initialization; no clipping; no stationary KFE/density/tail/aggregates; no D1-D3, regional GE, multi-province audit, neural training, nominal HANK, calibration, policy/welfare or Results.

No PR / merge / close / successor Issue / self-accept from Builder.

## Current route authority

- Issue #38 full body + authoritative activation comment = exact Builder experiment authority once activation is posted.
- Startup Snapshot: `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
- Roadmap: `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
- Historical handoff: `docs/governance/DLH_HANDOFF_2026_09_01_UPPER_DOMAIN_STATIONARY_TAIL_ROUTE.md`
