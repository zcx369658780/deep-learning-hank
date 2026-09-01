# DLH-5J — Final Bounded Coupled Liquid-Extent Continuation (Issue #36)

Policy-only diagnostic completing the last pre-frozen larger-b grid experiment before asymptotic adjudication. Accepted MATLAB-faithful HJB source is immutable and reused read-only.

Overall terminal classification: `DLH_5J_JOINT_BOUNDARY_COMPATIBILITY_NOT_ROBUST_ACROSS_A_RESOLUTION__SCIENTIFIC_REVIEW_REQUIRED`

Secondary scientific annotations: `DLH_5J_CROSS_A_POLICY_RESOLUTION_SENSITIVITY_REMAINS_MATERIAL__NUMERICAL_REVIEW_REQUIRED`

Binding route rule: `ASYMPTOTIC_OR_FINITE_DOMAIN_CLOSURE_ADJUDICATION` — STOP larger-grid continuation (b160 hard ceiling); no common threshold reached; next gate must adjudicate high-wealth liquid drift / economic mean reversion / finite-domain HJB closure analytically or semi-analytically.

Frozen economics: `wbar=1.0`, `r_a=0.03`; physical illiquid domain `a [0.0,10.0]`, `a_max=10.0`, taper `r_a*(1-0.1*(a/a_max)^9)_MATLAB_FAITHFUL_UNCHANGED`; liquid spacing `db=0.368421052632`; only mature a resolutions a77/a153 and final b extents b120/b140/b160; b160_IS_THE_HARD_ROUTE_CEILING__NO_B180_B200; all non-grid objects the accepted DLH-5B/DLH-5E fixture (`configs/dlh_5b_two_region_symmetric_anchor.toml`, region_index=0). Accepted DLH-5I b100 results are read-only scalar anchors only (b100 NOT rerun).

## Accepted b100 scalar anchors (read-only, Issue #36 section 7)

- I2_A77_B100 (a77): requested upper-b 1.925385153e-01 (4 states, share 2.597402597e-02), argmax (99, 76, 1) physical (34.473684210526315, 10.0, 1.3), raw upper-b 7.093524248e-02, upper-a requested 0.0e+00. Provenance: ACCEPTED_DLH_5I_EVIDENCE__DLH_5I_BOUNDARY_DIAGNOSTICS_CSV__READ_ONLY (rerun in DLH-5J: False).
- I5_A153_B100 (a153): requested upper-b 2.481811687e-01 (8 states, share 2.614379085e-02), argmax (99, 152, 1) physical (34.473684210526315, 10.0, 1.3), raw upper-b 9.143516741e-02, upper-a requested 0.0e+00. Provenance: ACCEPTED_DLH_5I_EVIDENCE__DLH_5I_BOUNDARY_DIAGNOSTICS_CSV__READ_ONLY (rerun in DLH-5J: False).

## Variant status (Phase A)

| variant | a res | b ext | a pts | da | b pts | b_hi | db | HJB conv | iters | stat | raw upper-a | raw lower-a | raw upper-b | raw lower-b | joint marker |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| J0_A77_B120 | a77 | b120 | 77 | 0.13157894736842105 | 120 | 41.84210526315789 | 0.368421052631579 | True | 10 | 6.566e-08 | 0.000e+00 | 0.000e+00 | 4.292e-02 | 0.000e+00 | JOINT_HJB_BOUNDARY_POLICY_NOT_COMPATIBLE |
| J1_A77_B140 | a77 | b140 | 77 | 0.13157894736842105 | 140 | 49.21052631578947 | 0.368421052631579 | True | 10 | 6.566e-08 | 0.000e+00 | 0.000e+00 | 1.759e-02 | 0.000e+00 | JOINT_HJB_BOUNDARY_POLICY_NOT_COMPATIBLE |
| J2_A77_B160 | a77 | b160 | 77 | 0.13157894736842105 | 160 | 56.578947368421055 | 0.368421052631579 | True | 10 | 6.566e-08 | 0.000e+00 | 0.000e+00 | 0.000e+00 | 0.000e+00 | JOINT_HJB_BOUNDARY_POLICY_COMPATIBLE |
| J3_A153_B120 | a153 | b120 | 153 | 0.06578947368421052 | 120 | 41.84210526315789 | 0.368421052631579 | True | 10 | 2.057e-08 | 0.000e+00 | 0.000e+00 | 6.363e-02 | 0.000e+00 | JOINT_HJB_BOUNDARY_POLICY_NOT_COMPATIBLE |
| J4_A153_B140 | a153 | b140 | 153 | 0.06578947368421052 | 140 | 49.21052631578947 | 0.368421052631579 | True | 10 | 2.060e-08 | 0.000e+00 | 0.000e+00 | 3.844e-02 | 0.000e+00 | JOINT_HJB_BOUNDARY_POLICY_NOT_COMPATIBLE |
| J5_A153_B160 | a153 | b160 | 153 | 0.06578947368421052 | 160 | 56.578947368421055 | 0.368421052631579 | True | 10 | 2.060e-08 | 0.000e+00 | 0.000e+00 | 1.492e-02 | 0.000e+00 | JOINT_HJB_BOUNDARY_POLICY_NOT_COMPATIBLE |

## Complete boundary diagnostics (Phase B, all four asset boundaries)

Raw drift (`max(mu,0)` / `max(-mu,0)`) is the primary cross-resolution quantity; requested generator rate (raw/spacing) is the HJB/KFE compatibility quantity. Raw thresholds `1e-10*da`/`1e-10*db` correspond to the accepted requested-rate threshold `1e-10`. Coordinates are exact `(b_index,a_index,z_index)` plus physical `(b,a,z)` via C-order unraveling on the actual 2-D boundary slice.

### J0_A77_B120

| boundary | kind | max | count | share | argmax index | argmax physical | value at argmax | q50/q90/q95/q99 |
|---|---|---|---|---|---|---|---|---|
| upper_a | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 76, 0) | (-2.0, 10.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_a | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 76, 0) | (-2.0, 10.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_a | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_a | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_b | raw | 4.292e-02 | 3 | 1.948e-02 | (119, 76, 1) | (41.84210526315789, 10.0, 1.3) | 4.292e-02 | 0.02841300609810249/0.04001551479806507/0.041465828385560385/0.04262607925555664 |
| upper_b | requested | 1.165e-01 | 3 | 1.948e-02 | (119, 76, 1) | (41.84210526315789, 10.0, 1.3) | 1.165e-01 | 0.07712101655199247/0.1086135401661766/0.1125501056179496/0.11569935797936802 |
| lower_b | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_b | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |

Complete offending states (raw > `1e-10*spacing`; requested > `1e-10`):

| boundary | kind | b_index | a_index | z_index | b | a | z | rate |
|---|---|---|---|---|---|---|---|---|
| upper_b | raw | 119 | 74 | 1 | 41.842105 | 9.736842 | 1.300000 | 7.108521285e-03 |
| upper_b | raw | 119 | 75 | 1 | 41.842105 | 9.868421 | 1.300000 | 2.841300610e-02 |
| upper_b | raw | 119 | 76 | 1 | 41.842105 | 10.000000 | 1.300000 | 4.291614197e-02 |
| upper_b | requested | 119 | 74 | 1 | 41.842105 | 9.736842 | 1.300000 | 1.929455777e-02 |
| upper_b | requested | 119 | 75 | 1 | 41.842105 | 9.868421 | 1.300000 | 7.712101655e-02 |
| upper_b | requested | 119 | 76 | 1 | 41.842105 | 10.000000 | 1.300000 | 1.164866711e-01 |

### J1_A77_B140

| boundary | kind | max | count | share | argmax index | argmax physical | value at argmax | q50/q90/q95/q99 |
|---|---|---|---|---|---|---|---|---|
| upper_a | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 76, 0) | (-2.0, 10.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_a | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 76, 0) | (-2.0, 10.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_a | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_a | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_b | raw | 1.759e-02 | 2 | 1.299e-02 | (139, 76, 1) | (49.21052631578947, 10.0, 1.3) | 1.759e-02 | 0.010351576081463643/0.016138358118541384/0.016861705873176102/0.017440384076883877 |
| upper_b | requested | 4.773e-02 | 2 | 1.299e-02 | (139, 76, 1) | (49.21052631578947, 10.0, 1.3) | 4.773e-02 | 0.028097135078258458/0.043804114893183754/0.04576748737004942/0.047338185351541946 |
| lower_b | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_b | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |

Complete offending states (raw > `1e-10*spacing`; requested > `1e-10`):

| boundary | kind | b_index | a_index | z_index | b | a | z | rate |
|---|---|---|---|---|---|---|---|---|
| upper_b | raw | 139 | 75 | 1 | 49.210526 | 9.868421 | 1.300000 | 3.118098535e-03 |
| upper_b | raw | 139 | 76 | 1 | 49.210526 | 10.000000 | 1.300000 | 1.758505363e-02 |
| upper_b | requested | 139 | 75 | 1 | 49.210526 | 9.868421 | 1.300000 | 8.463410310e-03 |
| upper_b | requested | 139 | 76 | 1 | 49.210526 | 10.000000 | 1.300000 | 4.773085985e-02 |

### J2_A77_B160

| boundary | kind | max | count | share | argmax index | argmax physical | value at argmax | q50/q90/q95/q99 |
|---|---|---|---|---|---|---|---|---|
| upper_a | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 76, 0) | (-2.0, 10.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_a | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 76, 0) | (-2.0, 10.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_a | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_a | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_b | raw | 0.000e+00 | 0 | 0.000e+00 | (159, 0, 0) | (56.578947368421055, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_b | requested | 0.000e+00 | 0 | 0.000e+00 | (159, 0, 0) | (56.578947368421055, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_b | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_b | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |

Complete offending states (raw > `1e-10*spacing`; requested > `1e-10`):

No state exceeds the raw or requested threshold.

### J3_A153_B120

| boundary | kind | max | count | share | argmax index | argmax physical | value at argmax | q50/q90/q95/q99 |
|---|---|---|---|---|---|---|---|---|
| upper_a | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 152, 0) | (-2.0, 10.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_a | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 152, 0) | (-2.0, 10.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_a | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_a | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_b | raw | 6.363e-02 | 6 | 1.961e-02 | (119, 152, 1) | (41.84210526315789, 10.0, 1.3) | 6.363e-02 | 0.038656972493102626/0.05989340027678103/0.06175967326044751/0.0632526916473807 |
| upper_b | requested | 1.727e-01 | 6 | 1.961e-02 | (119, 152, 1) | (41.84210526315789, 10.0, 1.3) | 1.727e-01 | 0.10492606819556427/0.16256780075126276/0.1676333988497861/0.17168587732860474 |
| lower_b | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_b | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |

Complete offending states (raw > `1e-10*spacing`; requested > `1e-10`):

| boundary | kind | b_index | a_index | z_index | b | a | z | rate |
|---|---|---|---|---|---|---|---|---|
| upper_b | raw | 119 | 147 | 1 | 41.842105 | 9.671053 | 1.300000 | 4.353314391e-03 |
| upper_b | raw | 119 | 148 | 1 | 41.842105 | 9.736842 | 1.300000 | 1.847327678e-02 |
| upper_b | raw | 119 | 149 | 1 | 41.842105 | 9.802632 | 1.300000 | 3.221944759e-02 |
| upper_b | raw | 119 | 150 | 1 | 41.842105 | 9.868421 | 1.300000 | 4.509449740e-02 |
| upper_b | raw | 119 | 151 | 1 | 41.842105 | 9.934211 | 1.300000 | 5.616085431e-02 |
| upper_b | raw | 119 | 152 | 1 | 41.842105 | 10.000000 | 1.300000 | 6.362594624e-02 |
| upper_b | requested | 119 | 147 | 1 | 41.842105 | 9.671053 | 1.300000 | 1.181613906e-02 |
| upper_b | requested | 119 | 148 | 1 | 41.842105 | 9.736842 | 1.300000 | 5.014175125e-02 |
| upper_b | requested | 119 | 149 | 1 | 41.842105 | 9.802632 | 1.300000 | 8.745278631e-02 |
| upper_b | requested | 119 | 150 | 1 | 41.842105 | 9.868421 | 1.300000 | 1.223993501e-01 |
| upper_b | requested | 119 | 151 | 1 | 41.842105 | 9.934211 | 1.300000 | 1.524366046e-01 |
| upper_b | requested | 119 | 152 | 1 | 41.842105 | 10.000000 | 1.300000 | 1.726989969e-01 |

### J4_A153_B140

| boundary | kind | max | count | share | argmax index | argmax physical | value at argmax | q50/q90/q95/q99 |
|---|---|---|---|---|---|---|---|---|
| upper_a | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 152, 0) | (-2.0, 10.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_a | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 152, 0) | (-2.0, 10.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_a | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_a | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_b | raw | 3.844e-02 | 4 | 1.307e-02 | (139, 152, 1) | (49.21052631578947, 10.0, 1.3) | 3.844e-02 | 0.02548526461352396/0.03620870356237982/0.03732452178496265/0.03821717636302891 |
| upper_b | requested | 1.043e-01 | 4 | 1.307e-02 | (139, 152, 1) | (49.21052631578947, 10.0, 1.3) | 1.043e-01 | 0.06917428966527932/0.09828076681217378/0.10130941627347004/0.10373233584250705 |
| lower_b | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_b | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |

Complete offending states (raw > `1e-10*spacing`; requested > `1e-10`):

| boundary | kind | b_index | a_index | z_index | b | a | z | rate |
|---|---|---|---|---|---|---|---|---|
| upper_b | raw | 139 | 149 | 1 | 49.210526 | 9.802632 | 1.300000 | 7.126612376e-03 |
| upper_b | raw | 139 | 150 | 1 | 49.210526 | 9.868421 | 1.300000 | 1.996897737e-02 |
| upper_b | raw | 139 | 151 | 1 | 49.210526 | 9.934211 | 1.300000 | 3.100155186e-02 |
| upper_b | raw | 139 | 152 | 1 | 49.210526 | 10.000000 | 1.300000 | 3.844034001e-02 |
| upper_b | requested | 139 | 149 | 1 | 49.210526 | 9.802632 | 1.300000 | 1.934366216e-02 |
| upper_b | requested | 139 | 150 | 1 | 49.210526 | 9.868421 | 1.300000 | 5.420151000e-02 |
| upper_b | requested | 139 | 151 | 1 | 49.210526 | 9.934211 | 1.300000 | 8.414706933e-02 |
| upper_b | requested | 139 | 152 | 1 | 49.210526 | 10.000000 | 1.300000 | 1.043380657e-01 |

### J5_A153_B160

| boundary | kind | max | count | share | argmax index | argmax physical | value at argmax | q50/q90/q95/q99 |
|---|---|---|---|---|---|---|---|---|
| upper_a | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 152, 0) | (-2.0, 10.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_a | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 152, 0) | (-2.0, 10.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_a | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_a | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_b | raw | 1.492e-02 | 2 | 6.536e-03 | (159, 152, 1) | (56.578947368421055, 10.0, 1.3) | 1.492e-02 | 0.011208514026413319/0.014174707984752465/0.014545482229544859/0.014842101625378775 |
| upper_b | requested | 4.049e-02 | 2 | 6.536e-03 | (159, 152, 1) | (56.578947368421055, 10.0, 1.3) | 4.049e-02 | 0.03042310950026472/0.03847420738718526/0.03948059462305033/0.04028570441174238 |
| lower_b | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_b | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |

Complete offending states (raw > `1e-10*spacing`; requested > `1e-10`):

| boundary | kind | b_index | a_index | z_index | b | a | z | rate |
|---|---|---|---|---|---|---|---|---|
| upper_b | raw | 159 | 151 | 1 | 56.578947 | 9.934211 | 1.300000 | 7.500771578e-03 |
| upper_b | raw | 159 | 152 | 1 | 56.578947 | 10.000000 | 1.300000 | 1.491625647e-02 |
| upper_b | requested | 159 | 151 | 1 | 56.578947 | 9.934211 | 1.300000 | 2.035923714e-02 |
| upper_b | requested | 159 | 152 | 1 | 56.578947 | 10.000000 | 1.300000 | 4.048698186e-02 |

## Final same-a continuation trends (Phase C: b100 anchor -> b120 -> b140 -> b160)

### a77

| b extent | variant | kind | raw upper-b max | requested upper-b max | raw count | requested count | argmax physical (a,z) | upper-a compatible |
|---|---|---|---|---|---|---|---|---|
| b100 | I2_A77_B100 | ANCHOR_B100 | 7.094e-02 | 1.925e-01 | 4 | 4 | (10.0, 1.3) | True |
| b120 | J0_A77_B120 | ENTRY | 4.292e-02 | 1.165e-01 | 3 | 3 | (10.0, 1.3) | True |
| b140 | J1_A77_B140 | ENTRY | 1.759e-02 | 4.773e-02 | 2 | 2 | (10.0, 1.3) | True |
| b160 | J2_A77_B160 | ENTRY | 0.000e+00 | 0.000e+00 | 0 | 0 | (0.0, 0.8) | True |

- adjacent raw attenuation ratios (b100/b120, b120/b140, b140/b160): [1.65288, 2.44049, 'inf']
- adjacent requested attenuation ratios: [1.65288, 2.44049, 'inf']
- raw ratios relative to accepted b100: [1.0, 0.605005, 0.247903, 0.0]
- requested ratios relative to accepted b100: [1.0, 0.605005, 0.247903, 0.0]
- strictly decreasing requested upper-b max over the continuation: True
- non-increasing requested flag: True
- plateau flag: False
- monotonic flag: strictly_decreasing
- first final extent with requested upper-b <= 1e-10: b160
- upper-a compatible on every final extent: True

### a153

| b extent | variant | kind | raw upper-b max | requested upper-b max | raw count | requested count | argmax physical (a,z) | upper-a compatible |
|---|---|---|---|---|---|---|---|---|
| b100 | I5_A153_B100 | ANCHOR_B100 | 9.144e-02 | 2.482e-01 | 8 | 8 | (10.0, 1.3) | True |
| b120 | J3_A153_B120 | ENTRY | 6.363e-02 | 1.727e-01 | 6 | 6 | (10.0, 1.3) | True |
| b140 | J4_A153_B140 | ENTRY | 3.844e-02 | 1.043e-01 | 4 | 4 | (10.0, 1.3) | True |
| b160 | J5_A153_B160 | ENTRY | 1.492e-02 | 4.049e-02 | 2 | 2 | (10.0, 1.3) | True |

- adjacent raw attenuation ratios (b100/b120, b120/b140, b140/b160): [1.437074, 1.655187, 2.577077]
- adjacent requested attenuation ratios: [1.437074, 1.655187, 2.577077]
- raw ratios relative to accepted b100: [1.0, 0.695859, 0.420411, 0.163135]
- requested ratios relative to accepted b100: [1.0, 0.695859, 0.420411, 0.163135]
- strictly decreasing requested upper-b max over the continuation: True
- non-increasing requested flag: True
- plateau flag: False
- monotonic flag: strictly_decreasing
- first final extent with requested upper-b <= 1e-10: None
- upper-a compatible on every final extent: True

These are policy-only trends; no post-hoc root is fitted and no adaptive next extent is generated (b160 is the hard route ceiling). Any upper-a reactivation on an extended b extent is preserved as evidence, not clipped.

## Cross-a exact-node policy comparisons (Phase D)

Three required pairs at common final extents (a77 vs every-second a153, all common b nodes, all z, no interpolation). Shared-interior mask excludes the top two coarse layers in EACH asset dimension. `rel_diff = max_abs / max(1, max|coarse|)` is scale-aware.

### J0_A77_B120_vs_J3_A153_B120 (b120)

| field | max_abs_diff | rel_diff | label mismatch |
|---|---|---|---|
| value | 6.512e-02 | 9.528e-04 | — |
| consumption | 1.740e-03 | 9.497e-04 | — |
| labor | 6.281e-04 | 5.611e-04 | — |
| transfer | 2.429e-02 | 2.204e-02 | — |
| mu_a | 2.429e-02 | 2.429e-02 | — |
| mu_b | 1.913e-02 | 1.913e-02 | — |
| liquid_label | — | — | 25 |
| transfer_label | — | — | 72 |

### J1_A77_B140_vs_J4_A153_B140 (b140)

| field | max_abs_diff | rel_diff | label mismatch |
|---|---|---|---|
| value | 6.512e-02 | 9.528e-04 | — |
| consumption | 1.740e-03 | 8.943e-04 | — |
| labor | 6.281e-04 | 5.611e-04 | — |
| transfer | 2.429e-02 | 2.204e-02 | — |
| mu_a | 2.429e-02 | 2.429e-02 | — |
| mu_b | 1.913e-02 | 1.913e-02 | — |
| liquid_label | — | — | 25 |
| transfer_label | — | — | 72 |

### J2_A77_B160_vs_J5_A153_B160 (b160)

| field | max_abs_diff | rel_diff | label mismatch |
|---|---|---|---|
| value | 6.512e-02 | 9.528e-04 | — |
| consumption | 1.740e-03 | 8.450e-04 | — |
| labor | 6.281e-04 | 5.611e-04 | — |
| transfer | 2.429e-02 | 2.204e-02 | — |
| mu_a | 2.429e-02 | 2.429e-02 | — |
| mu_b | 1.913e-02 | 1.913e-02 | — |
| liquid_label | — | — | 25 |
| transfer_label | — | — | 72 |

## Joint HJB upper-boundary policy compatibility frontier (Phase E)

Per-variant prerequisite marker: `requested_upper_b <= 1e-10 AND requested_upper_a <= 1e-10`. `CROSS_A_RESOLUTION_JOINT_COMPATIBLE_AT_B_EXTENT` holds only when BOTH mature a resolutions at the same final extent pass both thresholds. Prerequisite marker only — it does NOT authorize stationary KFE.

- J0_A77_B120: JOINT_HJB_BOUNDARY_POLICY_NOT_COMPATIBLE (ua 0.000e+00, ub 1.165e-01)
- J1_A77_B140: JOINT_HJB_BOUNDARY_POLICY_NOT_COMPATIBLE (ua 0.000e+00, ub 4.773e-02)
- J2_A77_B160: JOINT_HJB_BOUNDARY_POLICY_COMPATIBLE (ua 0.000e+00, ub 0.000e+00)
- J3_A153_B120: JOINT_HJB_BOUNDARY_POLICY_NOT_COMPATIBLE (ua 0.000e+00, ub 1.727e-01)
- J4_A153_B140: JOINT_HJB_BOUNDARY_POLICY_NOT_COMPATIBLE (ua 0.000e+00, ub 1.043e-01)
- J5_A153_B160: JOINT_HJB_BOUNDARY_POLICY_NOT_COMPATIBLE (ua 0.000e+00, ub 4.049e-02)

- b120 cross-a: a77=False, a153=False -> CROSS_A_RESOLUTION_JOINT_NOT_COMPATIBLE_AT_B_EXTENT
- b140 cross-a: a77=False, a153=False -> CROSS_A_RESOLUTION_JOINT_NOT_COMPATIBLE_AT_B_EXTENT
- b160 cross-a: a77=True, a153=False -> CROSS_A_RESOLUTION_JOINT_NOT_COMPATIBLE_AT_B_EXTENT

Stationary KFE / nullspace / pin / density / tail mass / stationary flux / `C,L,A,B` are `NOT_AUTHORIZED__DLH_5J_POLICY_ONLY_FINAL_BOUNDED_EXTENT_DIAGNOSTIC` and were not executed.

## Reproducibility

- randomness: `NOT_APPLICABLE`; repeat pass: `True`; terminal run1/run2: `DLH_5J_JOINT_BOUNDARY_COMPATIBILITY_NOT_ROBUST_ACROSS_A_RESOLUTION__SCIENTIFIC_REVIEW_REQUIRED` / `DLH_5J_JOINT_BOUNDARY_COMPATIBILITY_NOT_ROBUST_ACROSS_A_RESOLUTION__SCIENTIFIC_REVIEW_REQUIRED`; annotations run1/run2: ['DLH_5J_CROSS_A_POLICY_RESOLUTION_SENSITIVITY_REMAINS_MATERIAL__NUMERICAL_REVIEW_REQUIRED'] / ['DLH_5J_CROSS_A_POLICY_RESOLUTION_SENSITIVITY_REMAINS_MATERIAL__NUMERICAL_REVIEW_REQUIRED'].
- J0_A77_B120: structural identical True, max numeric diff 0.000e+00, aligned non-finite 0, mismatched 0, pass True.
- J1_A77_B140: structural identical True, max numeric diff 0.000e+00, aligned non-finite 0, mismatched 0, pass True.
- J2_A77_B160: structural identical True, max numeric diff 0.000e+00, aligned non-finite 0, mismatched 0, pass True.
- J3_A153_B120: structural identical True, max numeric diff 0.000e+00, aligned non-finite 0, mismatched 0, pass True.
- J4_A153_B140: structural identical True, max numeric diff 0.000e+00, aligned non-finite 0, mismatched 0, pass True.
- J5_A153_B160: structural identical True, max numeric diff 0.000e+00, aligned non-finite 0, mismatched 0, pass True.

## Artifact integrity

- accepted MATLAB-faithful oracle blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`, SHA-256 `1795718C469FC3B427CAB8E3D5957C133BEAD6EACC9EF0A25A3EDB7211D1A024` re-verified read-only (unchanged from the accepted Issue #23/#26 state).
- no existing tracked file modified; dedicated branch `dsh/issue-36-dlh-5j-final-coupled-b-extent-2026-09-01`; allowlist-only additions (3 artifacts + 8 evidence files).

DLH-5J implements NO repair and NO stationary acceptance: accepted HJB/KFE/regional source immutable; physical a-domain/a_max/taper/economics/tolerances/initialization frozen; a77/a153 only; db=7/19 only; b120/b140/b160 only (b160 hard ceiling); no b100 rerun; no clipping; no D1-D3; no regional or multi-province GE; no learned network; no nominal HANK.