# DLH-5L — Componentwise Liquid Outward Drift vs Total-Wealth Mean Reversion and Boundary Geometry (Issue #38)

Analytical/source-preserving adjudication. Reran exactly the six accepted J0-J5 grids solely to evaluate the total-wealth drift and the local W=a+b normal-drift geometry. Accepted MATLAB-faithful HJB source is immutable and reused read-only; the accepted DLH-5K diagnostic is the read-only reference.

Overall terminal classification: `DLH_5L_COMPONENTWISE_LIQUID_OUTWARD_DRIFT_WITH_TOTAL_WEALTH_MEAN_REVERSION_CONFIRMED__DOMAIN_GEOMETRY_DESIGN_REVIEW_REQUIRED`

Recommended next gate: Next gate must be a scientific design freeze comparing rectangular componentwise state constraints against an economically justified joint-domain / joint-KKT alternative (not an implementation patch). Stationary KFE remains NOT AUTHORIZED.

Frozen economics: `wbar=1.0`, `r_a=0.03`; a [0.0,10.0], `a_max=10.0`, taper `r_a*(1-0.1*(a/a_max)^9)_MATLAB_FAITHFUL_UNCHANGED`; `db=0.368421052632`; a resolutions a77/a153; b extents b120/b140/b160; b160_IS_THE_HARD_ROUTE_CEILING__NO_B180_B200__NO_NEW_GRID. No new grid / extent / resolution / warm start; no b100 rerun; no clipping.

## Accepted J0-J5 reproduction (fail-closed gate)

| variant | HJB stat diff | raw ub diff | req ub diff | count | pass |
|---|---|---|---|---|---|
| J0_A77_B120 | 0.00e+00 | 0.00e+00 | 0.00e+00 | 3/3 | True |
| J1_A77_B140 | 0.00e+00 | 0.00e+00 | 0.00e+00 | 2/2 | True |
| J2_A77_B160 | 0.00e+00 | 0.00e+00 | 0.00e+00 | 0/0 | True |
| J3_A153_B120 | 0.00e+00 | 0.00e+00 | 0.00e+00 | 6/6 | True |
| J4_A153_B140 | 0.00e+00 | 0.00e+00 | 0.00e+00 | 4/4 | True |
| J5_A153_B160 | 0.00e+00 | 0.00e+00 | 0.00e+00 | 2/2 | True |

Overall accepted-J reproduction pass: `True`. Any failure would classify BLOCKED_DLH_5L_ACCEPTED_HJB_REPRODUCTION.

## Inherited state set (pre-frozen, exact union, no post-hoc states)

- 105 unique `(variant,b_index,a_index,z_index)` states from the accepted DLH-5K localization (68 rows) and cross-a (24 rows -> 48 states) evidence, deduplicated only by exact identity.
- per variant: J0_A77_B120=17, J1_A77_B140=14, J2_A77_B160=8, J3_A153_B120=29, J4_A153_B140=22, J5_A153_B160=15

## Phase A — exact total-wealth drift accounting

Full audit persisted in `DLH_5L_SOURCE_ACCOUNTING_AUDIT.md`. `mu_W = mu_a + mu_b = r_a_eff(a)*a + r_b*b + labor_income - adjustment_cost - (consumption - transfer_income)`; the linear transfer term cancels one-for-one between mu_a and mu_b. Verified numerically at every inherited state in `DLH_5L_STATE_DRIFT_DECOMPOSITION.csv`.
- max |mu_W - transfer-cancelled reconstruction| residual = 4.16e-16
- max |linear d + linear (-d)| cancellation = 0.00e+00

## Phase B — four-way coordinate/total classification

Full table persisted in `DLH_5L_COORDINATE_TOTAL_CLASSIFICATION.csv` (105 states). Classification rule (accepted boundary threshold only): B_OUTWARD iff mu_b > 1e-10*db; TOTAL_OUTWARD iff mu_W > 0; TOTAL_INWARD iff mu_W <= 0.

### Counts by variant / layer / a-resolution / z
**by_variant**
- ('J0_A77_B120',): {'B_NONOUTWARD__TOTAL_INWARD': 9, 'B_OUTWARD__TOTAL_INWARD': 8}
- ('J1_A77_B140',): {'B_NONOUTWARD__TOTAL_INWARD': 11, 'B_OUTWARD__TOTAL_INWARD': 3}
- ('J2_A77_B160',): {'B_NONOUTWARD__TOTAL_INWARD': 8}
- ('J3_A153_B120',): {'B_NONOUTWARD__TOTAL_INWARD': 10, 'B_OUTWARD__TOTAL_INWARD': 19}
- ('J4_A153_B140',): {'B_NONOUTWARD__TOTAL_INWARD': 11, 'B_OUTWARD__TOTAL_INWARD': 11}
- ('J5_A153_B160',): {'B_NONOUTWARD__TOTAL_INWARD': 12, 'B_OUTWARD__TOTAL_INWARD': 3}
**by_variant_layer**
- ('J0_A77_B120', 'INTERIOR'): {'B_NONOUTWARD__TOTAL_INWARD': 4, 'B_OUTWARD__TOTAL_INWARD': 5}
- ('J0_A77_B120', 'TOP'): {'B_NONOUTWARD__TOTAL_INWARD': 5, 'B_OUTWARD__TOTAL_INWARD': 3}
- ('J1_A77_B140', 'INTERIOR'): {'B_NONOUTWARD__TOTAL_INWARD': 5, 'B_OUTWARD__TOTAL_INWARD': 1}
- ('J1_A77_B140', 'TOP'): {'B_NONOUTWARD__TOTAL_INWARD': 6, 'B_OUTWARD__TOTAL_INWARD': 2}
- ('J2_A77_B160', 'TOP'): {'B_NONOUTWARD__TOTAL_INWARD': 8}
- ('J3_A153_B120', 'INTERIOR'): {'B_NONOUTWARD__TOTAL_INWARD': 5, 'B_OUTWARD__TOTAL_INWARD': 13}
- ('J3_A153_B120', 'TOP'): {'B_NONOUTWARD__TOTAL_INWARD': 5, 'B_OUTWARD__TOTAL_INWARD': 6}
- ('J4_A153_B140', 'INTERIOR'): {'B_NONOUTWARD__TOTAL_INWARD': 5, 'B_OUTWARD__TOTAL_INWARD': 7}
- ('J4_A153_B140', 'TOP'): {'B_NONOUTWARD__TOTAL_INWARD': 6, 'B_OUTWARD__TOTAL_INWARD': 4}
- ('J5_A153_B160', 'INTERIOR'): {'B_NONOUTWARD__TOTAL_INWARD': 5, 'B_OUTWARD__TOTAL_INWARD': 1}
- ('J5_A153_B160', 'TOP'): {'B_NONOUTWARD__TOTAL_INWARD': 7, 'B_OUTWARD__TOTAL_INWARD': 2}
**by_variant_a_res**
- ('J0_A77_B120', 'a77'): {'B_NONOUTWARD__TOTAL_INWARD': 9, 'B_OUTWARD__TOTAL_INWARD': 8}
- ('J1_A77_B140', 'a77'): {'B_NONOUTWARD__TOTAL_INWARD': 11, 'B_OUTWARD__TOTAL_INWARD': 3}
- ('J2_A77_B160', 'a77'): {'B_NONOUTWARD__TOTAL_INWARD': 8}
- ('J3_A153_B120', 'a153'): {'B_NONOUTWARD__TOTAL_INWARD': 10, 'B_OUTWARD__TOTAL_INWARD': 19}
- ('J4_A153_B140', 'a153'): {'B_NONOUTWARD__TOTAL_INWARD': 11, 'B_OUTWARD__TOTAL_INWARD': 11}
- ('J5_A153_B160', 'a153'): {'B_NONOUTWARD__TOTAL_INWARD': 12, 'B_OUTWARD__TOTAL_INWARD': 3}
**by_variant_z**
- ('J0_A77_B120', 0): {'B_NONOUTWARD__TOTAL_INWARD': 4}
- ('J0_A77_B120', 1): {'B_NONOUTWARD__TOTAL_INWARD': 5, 'B_OUTWARD__TOTAL_INWARD': 8}
- ('J1_A77_B140', 0): {'B_NONOUTWARD__TOTAL_INWARD': 4}
- ('J1_A77_B140', 1): {'B_NONOUTWARD__TOTAL_INWARD': 7, 'B_OUTWARD__TOTAL_INWARD': 3}
- ('J2_A77_B160', 0): {'B_NONOUTWARD__TOTAL_INWARD': 4}
- ('J2_A77_B160', 1): {'B_NONOUTWARD__TOTAL_INWARD': 4}
- ('J3_A153_B120', 0): {'B_NONOUTWARD__TOTAL_INWARD': 4}
- ('J3_A153_B120', 1): {'B_NONOUTWARD__TOTAL_INWARD': 6, 'B_OUTWARD__TOTAL_INWARD': 19}
- ('J4_A153_B140', 0): {'B_NONOUTWARD__TOTAL_INWARD': 4}
- ('J4_A153_B140', 1): {'B_NONOUTWARD__TOTAL_INWARD': 7, 'B_OUTWARD__TOTAL_INWARD': 11}
- ('J5_A153_B160', 0): {'B_NONOUTWARD__TOTAL_INWARD': 4}
- ('J5_A153_B160', 1): {'B_NONOUTWARD__TOTAL_INWARD': 8, 'B_OUTWARD__TOTAL_INWARD': 3}
**by_layer**
- ('INTERIOR',): {'B_NONOUTWARD__TOTAL_INWARD': 24, 'B_OUTWARD__TOTAL_INWARD': 27}
- ('TOP',): {'B_NONOUTWARD__TOTAL_INWARD': 37, 'B_OUTWARD__TOTAL_INWARD': 17}
**by_a_res**
- ('a153',): {'B_NONOUTWARD__TOTAL_INWARD': 33, 'B_OUTWARD__TOTAL_INWARD': 33}
- ('a77',): {'B_NONOUTWARD__TOTAL_INWARD': 28, 'B_OUTWARD__TOTAL_INWARD': 11}
**by_z**
- (0,): {'B_NONOUTWARD__TOTAL_INWARD': 24}
- (1,): {'B_NONOUTWARD__TOTAL_INWARD': 37, 'B_OUTWARD__TOTAL_INWARD': 44}

### Explicit coverage of every accepted DLH-5K INTERIOR_POSITIVE_PERSISTS state

48 inherited states belong to the accepted DLH-5K INTERIOR_POSITIVE_PERSISTS trajectories (recomputed from the accepted localization evidence: top-layer material AND at least one inspected interior layer material). For each, positive mu_b coexists with:
- TOTAL_INWARD: 48; TOTAL_OUTWARD: 0
- J0_A77_B120 (b=115, a=75, z=1, INTERIOR): mu_b=-2.028e-03, mu_W=-1.158e-01 -> TOTAL_INWARD
- J0_A77_B120 (b=117, a=75, z=1, INTERIOR): mu_b=4.240e-03, mu_W=-1.169e-01 -> TOTAL_INWARD
- J0_A77_B120 (b=118, a=75, z=1, INTERIOR): mu_b=1.301e-02, mu_W=-1.169e-01 -> TOTAL_INWARD
- J0_A77_B120 (b=119, a=75, z=1, TOP): mu_b=2.841e-02, mu_W=-1.163e-01 -> TOTAL_INWARD
- J0_A77_B120 (b=115, a=76, z=1, INTERIOR): mu_b=1.013e-02, mu_W=-1.201e-01 -> TOTAL_INWARD
- J0_A77_B120 (b=117, a=76, z=1, INTERIOR): mu_b=1.762e-02, mu_W=-1.212e-01 -> TOTAL_INWARD
- J0_A77_B120 (b=118, a=76, z=1, INTERIOR): mu_b=2.711e-02, mu_W=-1.212e-01 -> TOTAL_INWARD
- J0_A77_B120 (b=119, a=76, z=1, TOP): mu_b=4.292e-02, mu_W=-1.205e-01 -> TOTAL_INWARD
- J1_A77_B140 (b=135, a=76, z=1, INTERIOR): mu_b=-1.352e-02, mu_W=-1.439e-01 -> TOTAL_INWARD
- J1_A77_B140 (b=137, a=76, z=1, INTERIOR): mu_b=-6.795e-03, mu_W=-1.450e-01 -> TOTAL_INWARD
- J1_A77_B140 (b=138, a=76, z=1, INTERIOR): mu_b=2.169e-03, mu_W=-1.450e-01 -> TOTAL_INWARD
- J1_A77_B140 (b=139, a=76, z=1, TOP): mu_b=1.759e-02, mu_W=-1.444e-01 -> TOTAL_INWARD
- J3_A153_B120 (b=115, a=148, z=1, INTERIOR): mu_b=-7.759e-03, mu_W=-1.148e-01 -> TOTAL_INWARD
- J3_A153_B120 (b=117, a=148, z=1, INTERIOR): mu_b=-3.231e-03, mu_W=-1.158e-01 -> TOTAL_INWARD
- J3_A153_B120 (b=118, a=148, z=1, INTERIOR): mu_b=4.296e-03, mu_W=-1.156e-01 -> TOTAL_INWARD
- J3_A153_B120 (b=119, a=148, z=1, TOP): mu_b=1.847e-02, mu_W=-1.149e-01 -> TOTAL_INWARD
- J3_A153_B120 (b=115, a=149, z=1, INTERIOR): mu_b=5.255e-03, mu_W=-1.182e-01 -> TOTAL_INWARD
- J3_A153_B120 (b=117, a=149, z=1, INTERIOR): mu_b=1.022e-02, mu_W=-1.191e-01 -> TOTAL_INWARD
- J3_A153_B120 (b=118, a=149, z=1, INTERIOR): mu_b=1.800e-02, mu_W=-1.189e-01 -> TOTAL_INWARD
- J3_A153_B120 (b=119, a=149, z=1, TOP): mu_b=3.222e-02, mu_W=-1.181e-01 -> TOTAL_INWARD
- J3_A153_B120 (b=115, a=150, z=1, INTERIOR): mu_b=1.725e-02, mu_W=-1.215e-01 -> TOTAL_INWARD
- J3_A153_B120 (b=117, a=150, z=1, INTERIOR): mu_b=2.271e-02, mu_W=-1.224e-01 -> TOTAL_INWARD
- J3_A153_B120 (b=118, a=150, z=1, INTERIOR): mu_b=3.078e-02, mu_W=-1.222e-01 -> TOTAL_INWARD
- J3_A153_B120 (b=119, a=150, z=1, TOP): mu_b=4.509e-02, mu_W=-1.213e-01 -> TOTAL_INWARD
- J3_A153_B120 (b=115, a=151, z=1, INTERIOR): mu_b=2.725e-02, mu_W=-1.245e-01 -> TOTAL_INWARD
- J3_A153_B120 (b=117, a=151, z=1, INTERIOR): mu_b=3.327e-02, mu_W=-1.254e-01 -> TOTAL_INWARD
- J3_A153_B120 (b=118, a=151, z=1, INTERIOR): mu_b=4.168e-02, mu_W=-1.251e-01 -> TOTAL_INWARD
- J3_A153_B120 (b=119, a=151, z=1, TOP): mu_b=5.616e-02, mu_W=-1.242e-01 -> TOTAL_INWARD
- J3_A153_B120 (b=115, a=152, z=1, INTERIOR): mu_b=3.344e-02, mu_W=-1.268e-01 -> TOTAL_INWARD
- J3_A153_B120 (b=117, a=152, z=1, INTERIOR): mu_b=4.013e-02, mu_W=-1.276e-01 -> TOTAL_INWARD
- J3_A153_B120 (b=118, a=152, z=1, INTERIOR): mu_b=4.892e-02, mu_W=-1.273e-01 -> TOTAL_INWARD
- J3_A153_B120 (b=119, a=152, z=1, TOP): mu_b=6.363e-02, mu_W=-1.264e-01 -> TOTAL_INWARD
- J4_A153_B140 (b=135, a=150, z=1, INTERIOR): mu_b=-6.627e-03, mu_W=-1.452e-01 -> TOTAL_INWARD
- J4_A153_B140 (b=137, a=150, z=1, INTERIOR): mu_b=-1.697e-03, mu_W=-1.461e-01 -> TOTAL_INWARD
- J4_A153_B140 (b=138, a=150, z=1, INTERIOR): mu_b=5.957e-03, mu_W=-1.459e-01 -> TOTAL_INWARD
- J4_A153_B140 (b=139, a=150, z=1, TOP): mu_b=1.997e-02, mu_W=-1.451e-01 -> TOTAL_INWARD
- J4_A153_B140 (b=135, a=151, z=1, INTERIOR): mu_b=3.384e-03, mu_W=-1.482e-01 -> TOTAL_INWARD
- J4_A153_B140 (b=137, a=151, z=1, INTERIOR): mu_b=8.841e-03, mu_W=-1.491e-01 -> TOTAL_INWARD
- J4_A153_B140 (b=138, a=151, z=1, INTERIOR): mu_b=1.682e-02, mu_W=-1.489e-01 -> TOTAL_INWARD
- J4_A153_B140 (b=139, a=151, z=1, TOP): mu_b=3.100e-02, mu_W=-1.480e-01 -> TOTAL_INWARD
- J4_A153_B140 (b=135, a=152, z=1, INTERIOR): mu_b=9.617e-03, mu_W=-1.505e-01 -> TOTAL_INWARD
- J4_A153_B140 (b=137, a=152, z=1, INTERIOR): mu_b=1.569e-02, mu_W=-1.514e-01 -> TOTAL_INWARD
- J4_A153_B140 (b=138, a=152, z=1, INTERIOR): mu_b=2.404e-02, mu_W=-1.511e-01 -> TOTAL_INWARD
- J4_A153_B140 (b=139, a=152, z=1, TOP): mu_b=3.844e-02, mu_W=-1.503e-01 -> TOTAL_INWARD
- J5_A153_B160 (b=155, a=152, z=1, INTERIOR): mu_b=-1.265e-02, mu_W=-1.727e-01 -> TOTAL_INWARD
- J5_A153_B160 (b=157, a=152, z=1, INTERIOR): mu_b=-7.133e-03, mu_W=-1.736e-01 -> TOTAL_INWARD
- J5_A153_B160 (b=158, a=152, z=1, INTERIOR): mu_b=8.136e-04, mu_W=-1.734e-01 -> TOTAL_INWARD
- J5_A153_B160 (b=159, a=152, z=1, TOP): mu_b=1.492e-02, mu_W=-1.726e-01 -> TOTAL_INWARD

## Phase C — transfer cancellation / portfolio-reallocation mechanism

For every positive-mu_b state (44 states) the linear d / -d transfer cancellation is verified separately from adjustment cost (max |cancellation sum| persisted). Full table in `DLH_5L_STATE_DRIFT_DECOMPOSITION.csv` and the positive-mu_b subset summary below.

- J0_A77_B120 (b=115, a=76, z=1): mu_a=-1.302e-01, mu_b=1.013e-02, mu_W=-1.201e-01, -transfer=4.002e-01, cost=5.604e-02, bls=-3.341e-01, ti=3.442e-01, linear cancel=0.0e+00
- J0_A77_B120 (b=117, a=75, z=1): mu_a=-1.211e-01, mu_b=4.240e-03, mu_W=-1.169e-01, -transfer=3.909e-01, cost=5.458e-02, bls=-3.321e-01, ti=3.363e-01, linear cancel=0.0e+00
- J0_A77_B120 (b=117, a=76, z=1): mu_a=-1.388e-01, mu_b=1.762e-02, mu_W=-1.212e-01, -transfer=4.088e-01, cost=5.760e-02, bls=-3.336e-01, ti=3.512e-01, linear cancel=0.0e+00
- J0_A77_B120 (b=118, a=75, z=1): mu_a=-1.299e-01, mu_b=1.301e-02, mu_W=-1.169e-01, -transfer=3.997e-01, cost=5.615e-02, bls=-3.305e-01, ti=3.435e-01, linear cancel=0.0e+00
- J0_A77_B120 (b=118, a=76, z=1): mu_a=-1.483e-01, mu_b=2.711e-02, mu_W=-1.212e-01, -transfer=4.183e-01, cost=5.932e-02, bls=-3.318e-01, ti=3.590e-01, linear cancel=0.0e+00
- J0_A77_B120 (b=119, a=74, z=1): mu_a=-1.181e-01, mu_b=7.109e-03, mu_W=-1.110e-01, -transfer=3.872e-01, cost=5.413e-02, bls=-3.260e-01, ti=3.331e-01, linear cancel=0.0e+00
- J0_A77_B120 (b=119, a=75, z=1): mu_a=-1.447e-01, mu_b=2.841e-02, mu_W=-1.163e-01, -transfer=4.144e-01, cost=5.885e-02, bls=-3.272e-01, ti=3.556e-01, linear cancel=0.0e+00
- J0_A77_B120 (b=119, a=76, z=1): mu_a=-1.634e-01, mu_b=4.292e-02, mu_W=-1.205e-01, -transfer=4.334e-01, cost=6.212e-02, bls=-3.284e-01, ti=3.713e-01, linear cancel=0.0e+00
- J1_A77_B140 (b=138, a=76, z=1): mu_a=-1.472e-01, mu_b=2.169e-03, mu_W=-1.450e-01, -transfer=4.172e-01, cost=5.912e-02, bls=-3.559e-01, ti=3.580e-01, linear cancel=0.0e+00
- J1_A77_B140 (b=139, a=75, z=1): mu_a=-1.432e-01, mu_b=3.118e-03, mu_W=-1.401e-01, -transfer=4.130e-01, cost=5.859e-02, bls=-3.513e-01, ti=3.544e-01, linear cancel=0.0e+00
- J1_A77_B140 (b=139, a=76, z=1): mu_a=-1.620e-01, mu_b=1.759e-02, mu_W=-1.444e-01, -transfer=4.320e-01, cost=6.185e-02, bls=-3.525e-01, ti=3.701e-01, linear cancel=0.0e+00
- J3_A153_B120 (b=115, a=149, z=1): mu_a=-1.235e-01, mu_b=5.255e-03, mu_W=-1.182e-01, -transfer=3.930e-01, cost=5.505e-02, bls=-3.327e-01, ti=3.379e-01, linear cancel=0.0e+00
- ... (32 more rows in evidence)

Do not call componentwise outward drift harmless: at a rectangular b upper bound, positive mu_b still violates componentwise inwardness.

## Phase D — rectangular vs W-normal boundary geometry (analytical only)

```text
rectangular upper-corner constraint:  mu_a <= 0  AND  mu_b <= 0
source accounting coordinate:        W = a + b
local constant-W outward normal ~ (1,1):  mu_W = mu_a + mu_b <= 0
```

Persisted in `DLH_5L_BOUNDARY_GEOMETRY.csv` for every inherited top-layer offender (17 rows): rectangular b-inwardness, rectangular a-inwardness, and total-wealth inwardness.

This is an analytical geometry comparison only. It does NOT authorize replacing the production domain by a W-domain or changing the boundary law.

## Phase E — exact aligned a77/a153 total-wealth comparison

Persisted in `DLH_5L_CROSS_A_TOTAL_WEALTH.csv` (24 aligned pairs from the accepted DLH-5K cross-a evidence). Scale-aware relative differences use the pre-registered policy_rel_materiality = 0.01.

- mu_b cross-a material on at least one aligned state: True
- mu_W below the diagnostic threshold on ALL aligned states: False
- portfolio-reallocation annotation fires: False

Summary (24 aligned pairs): mu_b cross-a material on 24/24; mu_W below the diagnostic threshold on 8/24.
- |delta_mu_b| range = [-2.179e-02, -7.352e-03]
- |delta_mu_W| range = [2.924e-03, 6.157e-03]
- rel_diff_mu_b range = [1.906e-02, 1.405e+00]
- rel_diff_mu_W range = [5.773e-03, 4.683e-02]

Determination: mu_b is cross-a material on every aligned state; after the one-for-one transfer cancellation, delta_mu_W (abs ~1e-3..6e-3) is substantially smaller than delta_mu_b (abs ~8e-3..2.3e-2), i.e. the cross-a liquid divergence is portfolio-reallocation-dominated. However, relative to mu_W's own (small) magnitude, rel_diff_mu_W exceeds the diagnostic threshold on most z=1 aligned states, so the total-wealth cross-a difference does not fully vanish and the pre-registered portfolio-reallocation annotation does not fire.

## Deterministic repeat

- randomness `NOT_APPLICABLE`; repeat pass `True`; per-variant max numeric diff and count identity in `DLH_5L_REPRODUCIBILITY.json`. All phase outputs are deterministic functions of the accepted HJB results.

## Forbidden operations

Persisted in `DLH_5L_FORBIDDEN_OPERATION_CHECK.md`. No source/model/domain equation changed; no new grid; no b extent beyond b160; no adaptive/root-seeking; no clipping; no stationary KFE / nullspace / pin / density / tail / aggregates; no D1-D3; no regional / multi-province GE; no province audit; no network training; no nominal HANK.