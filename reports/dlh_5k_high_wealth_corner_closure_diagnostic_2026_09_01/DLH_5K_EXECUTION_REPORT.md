# DLH-5K — High-Wealth Liquid Drift vs Joint Upper-Corner HJB Closure (Issue #37)

Analytical/source-preserving adjudication. Reran exactly the six accepted DLH-5J grids J0-J5 solely to extract local high-wealth diagnostics. Accepted MATLAB-faithful HJB source is immutable and reused read-only.

Overall terminal classification: `DLH_5K_MIXED_HIGH_WEALTH_AND_BOUNDARY_CLOSURE_MECHANISM__SCIENTIFIC_REVIEW_REQUIRED`

Secondary scientific annotations: `DLH_5K_CROSS_A_DIVERGENCE_PRIMARILY_TRANSFER_DERIVATIVE_CHANNEL__SCIENTIFIC_REVIEW_REQUIRED`

Recommended next gate: Both mechanisms must be separately resolved before any HJB redesign or stationary re-entry. Stationary KFE remains NOT AUTHORIZED.

Frozen economics: `wbar=1.0`, `r_a=0.03`; a [0.0,10.0], `a_max=10.0`, taper `r_a*(1-0.1*(a/a_max)^9)_MATLAB_FAITHFUL_UNCHANGED`; `db=0.368421052632`; a resolutions a77/a153; b extents b120/b140/b160; b160_IS_THE_HARD_ROUTE_CEILING__NO_B180_B200__NO_NEW_GRID. No new grid / extent / resolution / warm start; no b100 rerun; no clipping.

## Accepted J0-J5 reproduction (fail-closed gate)

| variant | HJB stat | accepted stat | |stat diff| | raw ub | req ub | count | pass |
|---|---|---|---|---|---|---|---|
| J0_A77_B120 | 6.566e-08 | 6.566e-08 | 0.000e+00 | 4.292e-02 | 1.165e-01 | 3 | True |
| J1_A77_B140 | 6.566e-08 | 6.566e-08 | 0.000e+00 | 1.759e-02 | 4.773e-02 | 2 | True |
| J2_A77_B160 | 6.566e-08 | 6.566e-08 | 0.000e+00 | 0.000e+00 | 0.000e+00 | 0 | True |
| J3_A153_B120 | 2.057e-08 | 2.057e-08 | 0.000e+00 | 6.363e-02 | 1.727e-01 | 6 | True |
| J4_A153_B140 | 2.060e-08 | 2.060e-08 | 0.000e+00 | 3.844e-02 | 1.043e-01 | 4 | True |
| J5_A153_B160 | 2.060e-08 | 2.060e-08 | 0.000e+00 | 1.492e-02 | 4.049e-02 | 2 | True |

Overall accepted-J reproduction pass: `True`. Any failure would classify BLOCKED_DLH_5K_ACCEPTED_HJB_REPRODUCTION.

## Phase A — source-law audit

Full audit persisted in `DLH_5K_SOURCE_LAW_AUDIT.md` (8 audited objects: upper-b derivative closure; liquid resource/consumption branch; transfer candidate; upper-a transfer-direction restriction; upper-b transfer-direction override; adjustment cost; final mu_a/mu_b; requested-rate conversion). Decomposition verified numerically in Phase B for every offender: `mu_b = base_liquid_surplus + transfer_injection`.

### Implemented-source special-case identity

When the liquid zero-drift (`0`) branch holds, `consumption` equals total liquid resources, so `base_liquid_surplus = 0` and the implemented identity is `mu_b = -transfer - adjustment_cost`. This is an implemented-source identity under the stated branch conditions, **not** an economic theorem.

## Phase B — complete upper-b offender mechanism decomposition

Full table persisted in `DLH_5K_OFFENDER_DECOMPOSITION.csv` (21 rows: every material upper-b offender on J0/J1/J3/J4/J5 plus the corresponding aligned states on J2). Completeness vs the accepted DLH-5J offender sets:

- J0_A77_B120: accepted 3, recomputed 3, match True (missing [], extra [])
- J1_A77_B140: accepted 2, recomputed 2, match True (missing [], extra [])
- J3_A153_B120: accepted 6, recomputed 6, match True (missing [], extra [])
- J4_A153_B140: accepted 4, recomputed 4, match True (missing [], extra [])
- J5_A153_B160: accepted 2, recomputed 2, match True (missing [], extra [])

Per-state persisted: indices + physical (b,a,z); liquid_label; transfer_label; consumption; labor; transfer; adjustment cost; effective illiquid return; mu_a; mu_b; base_liquid_surplus; transfer_injection; reconstruction residual; V_b boundary-closure derivative; backward V_b derivative; available forward/backward V_a derivatives; V_a/V_b-1; selected transfer candidate where finite. Only derivatives recoverable from the accepted finite grid and converged value function are used (no invented derivatives).

## Phase C — boundary-vs-interior high-wealth localization

Full table persisted in `DLH_5K_BOUNDARY_INTERIOR_LOCALIZATION.csv`. Each material offender (a,z) is inspected at n-1/n-2/n-3/n-5 b layers with the same decomposition and labels; no tolerance beyond the accepted boundary threshold is used.

- J0_A77_B120 (a=74, z=1): BOUNDARY_ONLY_POSITIVE (top material True, interior material False)
- J0_A77_B120 (a=75, z=1): INTERIOR_POSITIVE_PERSISTS (top material True, interior material True)
- J0_A77_B120 (a=76, z=1): INTERIOR_POSITIVE_PERSISTS (top material True, interior material True)
- J1_A77_B140 (a=75, z=1): BOUNDARY_ONLY_POSITIVE (top material True, interior material False)
- J1_A77_B140 (a=76, z=1): INTERIOR_POSITIVE_PERSISTS (top material True, interior material True)
- J3_A153_B120 (a=147, z=1): BOUNDARY_ONLY_POSITIVE (top material True, interior material False)
- J3_A153_B120 (a=148, z=1): INTERIOR_POSITIVE_PERSISTS (top material True, interior material True)
- J3_A153_B120 (a=149, z=1): INTERIOR_POSITIVE_PERSISTS (top material True, interior material True)
- J3_A153_B120 (a=150, z=1): INTERIOR_POSITIVE_PERSISTS (top material True, interior material True)
- J3_A153_B120 (a=151, z=1): INTERIOR_POSITIVE_PERSISTS (top material True, interior material True)
- J3_A153_B120 (a=152, z=1): INTERIOR_POSITIVE_PERSISTS (top material True, interior material True)
- J4_A153_B140 (a=149, z=1): BOUNDARY_ONLY_POSITIVE (top material True, interior material False)
- J4_A153_B140 (a=150, z=1): INTERIOR_POSITIVE_PERSISTS (top material True, interior material True)
- J4_A153_B140 (a=151, z=1): INTERIOR_POSITIVE_PERSISTS (top material True, interior material True)
- J4_A153_B140 (a=152, z=1): INTERIOR_POSITIVE_PERSISTS (top material True, interior material True)
- J5_A153_B160 (a=151, z=1): BOUNDARY_ONLY_POSITIVE (top material True, interior material False)
- J5_A153_B160 (a=152, z=1): INTERIOR_POSITIVE_PERSISTS (top material True, interior material True)

## Phase D — joint upper-corner feasibility algebra + numerical evaluation

```text
chi(d,a) = chi_0*|d| + 0.5*chi_1*d^2/max(a,a_bar)
d = -x, x > 0
upper-a inward: mu_a = r_a_eff(a)*a - x <= 0   <=>  x >= r_a_eff(a)*a
upper-b inward (general): mu_b = base_liquid_surplus
                        + x*(1-chi_0) - 0.5*chi_1*x^2/max(a,a_bar) <= 0
upper-b inward (base_liquid_surplus=0 branch only):
                        x >= 2*(1-chi_0)*max(a,a_bar)/chi_1
```

Numerical evaluation persisted in `DLH_5K_JOINT_CORNER_FEASIBILITY.csv` (17 rows) at the actual offender states with the frozen D0 parameters, verifying the algebra against the direct drifts (mu_a/mu_b residuals reported).

## Phase E — cross-a resolution mechanism (b120/b140/b160)

Full table persisted in `DLH_5K_CROSS_A_MECHANISM.csv` (24 aligned a77 vs every-second a153 pairs).

- b120: sum|delta transfer_injection| = 1.241557e-01, sum|delta base_liquid_surplus| = 8.172015e-03
- b140: sum|delta transfer_injection| = 1.245806e-01, sum|delta base_liquid_surplus| = 7.757281e-03
- b160: sum|delta transfer_injection| = 1.248588e-01, sum|delta base_liquid_surplus| = 7.452123e-03

b160 divergence primarily transfer/derivative channel: True.

## Deterministic repeat

- randomness `NOT_APPLICABLE`; repeat pass `True`; per-variant max numeric diff and count identity in `DLH_5K_REPRODUCIBILITY.json`.

## Forbidden operations

Persisted in `DLH_5K_FORBIDDEN_OPERATION_CHECK.md`. Stationary marker: `NOT_AUTHORIZED__DLH_5K_POLICY_ONLY_HIGH_WEALTH_CORNER_CLOSURE_DIAGNOSTIC`. No source/model equation changed; no new grid; no b extent beyond b160; no adaptive/root-seeking; no clipping; no stationary KFE / nullspace / pin / density / tail / C-L-A-B; no D1-D3; no regional / multi-province GE; no province audit; no network training; no nominal HANK.