# DLH-5I — Coupled Liquid-Extent Frontier Diagnostic (Issue #35)

Policy-only diagnostic mapping the coupled b-extent x mature-a-resolution frontier. Accepted MATLAB-faithful HJB source is immutable and reused read-only.

Overall terminal classification: `DLH_5I_COUPLED_B_EXTENT_ATTENUATION_CONFIRMED__COMMON_THRESHOLD_NOT_REACHED__GPT_REVIEW_REQUIRED`

Secondary scientific annotations: `DLH_5I_CROSS_A_POLICY_RESOLUTION_SENSITIVITY_REMAINS_MATERIAL__NUMERICAL_REVIEW_REQUIRED`

Frozen economics: `wbar=1.0`, `r_a=0.03`; physical illiquid domain `a [0.0,10.0]`, `a_max=10.0`, taper `r_a*(1-0.1*(a/a_max)^9)_MATLAB_FAITHFUL_UNCHANGED`; liquid spacing `db=0.368421052632`; only mature a resolutions a77/a153 and b extents b60/b80/b100; all non-grid objects the accepted DLH-5B/DLH-5E fixture (`configs/dlh_5b_two_region_symmetric_anchor.toml`, region_index=0).

## Variant status (Phase A)

| variant | a res | b ext | a pts | da | b pts | b_hi | db | HJB conv | iters | stat | raw upper-a | raw lower-a | raw upper-b | raw lower-b | joint marker |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| I0_A77_B60 | a77 | b60 | 77 | 0.13157894736842105 | 60 | 19.736842105263158 | 0.368421052631579 | True | 10 | 6.171e-08 | 0.000e+00 | 0.000e+00 | 1.443e-01 | 0.000e+00 | JOINT_HJB_BOUNDARY_POLICY_NOT_COMPATIBLE |
| I1_A77_B80 | a77 | b80 | 77 | 0.13157894736842105 | 80 | 27.105263157894736 | 0.368421052631579 | True | 10 | 6.450e-08 | 0.000e+00 | 0.000e+00 | 1.035e-01 | 0.000e+00 | JOINT_HJB_BOUNDARY_POLICY_NOT_COMPATIBLE |
| I2_A77_B100 | a77 | b100 | 77 | 0.13157894736842105 | 100 | 34.473684210526315 | 0.368421052631579 | True | 10 | 6.563e-08 | 0.000e+00 | 0.000e+00 | 7.094e-02 | 0.000e+00 | JOINT_HJB_BOUNDARY_POLICY_NOT_COMPATIBLE |
| I3_A153_B60 | a153 | b60 | 153 | 0.06578947368421052 | 60 | 19.736842105263158 | 0.368421052631579 | True | 10 | 1.805e-08 | 0.000e+00 | 0.000e+00 | 1.639e-01 | 0.000e+00 | JOINT_HJB_BOUNDARY_POLICY_NOT_COMPATIBLE |
| I4_A153_B80 | a153 | b80 | 153 | 0.06578947368421052 | 80 | 27.105263157894736 | 0.368421052631579 | True | 10 | 1.936e-08 | 0.000e+00 | 0.000e+00 | 1.236e-01 | 0.000e+00 | JOINT_HJB_BOUNDARY_POLICY_NOT_COMPATIBLE |
| I5_A153_B100 | a153 | b100 | 153 | 0.06578947368421052 | 100 | 34.473684210526315 | 0.368421052631579 | True | 10 | 2.020e-08 | 0.000e+00 | 0.000e+00 | 9.144e-02 | 0.000e+00 | JOINT_HJB_BOUNDARY_POLICY_NOT_COMPATIBLE |

## Complete boundary diagnostics (Phase B, all four asset boundaries)

Raw drift (`max(mu,0)` / `max(-mu,0)`) is the primary cross-resolution quantity; requested generator rate (raw/spacing) is the HJB/KFE compatibility quantity. Raw thresholds `1e-10*da`/`1e-10*db` correspond to the accepted requested-rate threshold `1e-10`. Coordinates are exact `(b_index,a_index,z_index)` plus physical `(b,a,z)` via C-order unraveling on the actual 2-D boundary slice.

### I0_A77_B60

| boundary | kind | max | count | share | argmax index | argmax physical | value at argmax | q50/q90/q95/q99 |
|---|---|---|---|---|---|---|---|---|
| upper_a | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 76, 0) | (-2.0, 10.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_a | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 76, 0) | (-2.0, 10.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_a | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_a | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_b | raw | 1.443e-01 | 7 | 4.545e-02 | (59, 76, 1) | (19.736842105263158, 10.0, 1.3) | 1.443e-01 | 0.08347878204576187/0.13545793879207554/0.13985933884761367/0.1433804588920442 |
| upper_b | requested | 3.916e-01 | 7 | 4.545e-02 | (59, 76, 1) | (19.736842105263158, 10.0, 1.3) | 3.916e-01 | 0.2265852655527822/0.36767154814991926/0.3796182054435228/0.38917553127840565 |
| lower_b | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_b | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |

Complete offending states (raw > `1e-10*spacing`; requested > `1e-10`):

| boundary | kind | b_index | a_index | z_index | b | a | z | rate |
|---|---|---|---|---|---|---|---|---|
| upper_b | raw | 59 | 70 | 1 | 19.736842 | 9.210526 | 1.300000 | 6.375612177e-03 |
| upper_b | raw | 59 | 71 | 1 | 19.736842 | 9.342105 | 1.300000 | 3.192264240e-02 |
| upper_b | raw | 59 | 72 | 1 | 19.736842 | 9.473684 | 1.300000 | 5.778715769e-02 |
| upper_b | raw | 59 | 73 | 1 | 19.736842 | 9.605263 | 1.300000 | 8.347878205e-02 |
| upper_b | raw | 59 | 74 | 1 | 19.736842 | 9.736842 | 1.300000 | 1.080448853e-01 |
| upper_b | raw | 59 | 75 | 1 | 19.736842 | 9.868421 | 1.300000 | 1.295894054e-01 |
| upper_b | raw | 59 | 76 | 1 | 19.736842 | 10.000000 | 1.300000 | 1.442607389e-01 |
| upper_b | requested | 59 | 70 | 1 | 19.736842 | 9.210526 | 1.300000 | 1.730523305e-02 |
| upper_b | requested | 59 | 71 | 1 | 19.736842 | 9.342105 | 1.300000 | 8.664717224e-02 |
| upper_b | requested | 59 | 72 | 1 | 19.736842 | 9.473684 | 1.300000 | 1.568508566e-01 |
| upper_b | requested | 59 | 73 | 1 | 19.736842 | 9.605263 | 1.300000 | 2.265852656e-01 |
| upper_b | requested | 59 | 74 | 1 | 19.736842 | 9.736842 | 1.300000 | 2.932646888e-01 |
| upper_b | requested | 59 | 75 | 1 | 19.736842 | 9.868421 | 1.300000 | 3.517426718e-01 |
| upper_b | requested | 59 | 76 | 1 | 19.736842 | 10.000000 | 1.300000 | 3.915648627e-01 |

### I1_A77_B80

| boundary | kind | max | count | share | argmax index | argmax physical | value at argmax | q50/q90/q95/q99 |
|---|---|---|---|---|---|---|---|---|
| upper_a | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 76, 0) | (-2.0, 10.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_a | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 76, 0) | (-2.0, 10.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_a | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_a | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_b | raw | 1.035e-01 | 5 | 3.247e-02 | (79, 76, 1) | (27.105263157894736, 10.0, 1.3) | 1.035e-01 | 0.06741485067180775/0.097619730463874/0.1005395943879054/0.10287548552713054 |
| upper_b | requested | 2.808e-01 | 5 | 3.247e-02 | (79, 76, 1) | (27.105263157894736, 10.0, 1.3) | 2.808e-01 | 0.18298316610919244/0.26496783983051514/0.2728931847671718/0.27923346071649713 |
| lower_b | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_b | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |

Complete offending states (raw > `1e-10*spacing`; requested > `1e-10`):

| boundary | kind | b_index | a_index | z_index | b | a | z | rate |
|---|---|---|---|---|---|---|---|---|
| upper_b | raw | 79 | 72 | 1 | 27.105263 | 9.473684 | 1.300000 | 1.733256833e-02 |
| upper_b | raw | 79 | 73 | 1 | 27.105263 | 9.605263 | 1.300000 | 4.294284784e-02 |
| upper_b | raw | 79 | 74 | 1 | 27.105263 | 9.736842 | 1.300000 | 6.741485067e-02 |
| upper_b | raw | 79 | 75 | 1 | 27.105263 | 9.868421 | 1.300000 | 8.886013869e-02 |
| upper_b | raw | 79 | 76 | 1 | 27.105263 | 10.000000 | 1.300000 | 1.034594583e-01 |
| upper_b | requested | 79 | 72 | 1 | 27.105263 | 9.473684 | 1.300000 | 4.704554261e-02 |
| upper_b | requested | 79 | 73 | 1 | 27.105263 | 9.605263 | 1.300000 | 1.165591584e-01 |
| upper_b | requested | 79 | 74 | 1 | 27.105263 | 9.736842 | 1.300000 | 1.829831661e-01 |
| upper_b | requested | 79 | 75 | 1 | 27.105263 | 9.868421 | 1.300000 | 2.411918050e-01 |
| upper_b | requested | 79 | 76 | 1 | 27.105263 | 10.000000 | 1.300000 | 2.808185297e-01 |

### I2_A77_B100

| boundary | kind | max | count | share | argmax index | argmax physical | value at argmax | q50/q90/q95/q99 |
|---|---|---|---|---|---|---|---|---|
| upper_a | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 76, 0) | (-2.0, 10.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_a | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 76, 0) | (-2.0, 10.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_a | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_a | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_b | raw | 7.094e-02 | 4 | 2.597e-02 | (99, 76, 1) | (34.473684210526315, 10.0, 1.3) | 7.094e-02 | 0.045704740993929516/0.06657139534890524/0.06875331891593678/0.07049885776956202 |
| upper_b | requested | 1.925e-01 | 4 | 2.597e-02 | (99, 76, 1) | (34.473684210526315, 10.0, 1.3) | 1.925e-01 | 0.12405572555495153/0.1806937873755999/0.18661615134325696/0.1913540425173826 |
| lower_b | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_b | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |

Complete offending states (raw > `1e-10*spacing`; requested > `1e-10`):

| boundary | kind | b_index | a_index | z_index | b | a | z | rate |
|---|---|---|---|---|---|---|---|---|
| upper_b | raw | 99 | 73 | 1 | 34.473684 | 9.605263 | 1.300000 | 1.062376529e-02 |
| upper_b | raw | 99 | 74 | 1 | 34.473684 | 9.736842 | 1.300000 | 3.502039662e-02 |
| upper_b | raw | 99 | 75 | 1 | 34.473684 | 9.868421 | 1.300000 | 5.638908537e-02 |
| upper_b | raw | 99 | 76 | 1 | 34.473684 | 10.000000 | 1.300000 | 7.093524248e-02 |
| upper_b | requested | 99 | 73 | 1 | 34.473684 | 9.605263 | 1.300000 | 2.883593437e-02 |
| upper_b | requested | 99 | 74 | 1 | 34.473684 | 9.736842 | 1.300000 | 9.505536225e-02 |
| upper_b | requested | 99 | 75 | 1 | 34.473684 | 9.868421 | 1.300000 | 1.530560889e-01 |
| upper_b | requested | 99 | 76 | 1 | 34.473684 | 10.000000 | 1.300000 | 1.925385153e-01 |

### I3_A153_B60

| boundary | kind | max | count | share | argmax index | argmax physical | value at argmax | q50/q90/q95/q99 |
|---|---|---|---|---|---|---|---|---|
| upper_a | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 152, 0) | (-2.0, 10.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_a | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 152, 0) | (-2.0, 10.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_a | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_a | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_b | raw | 1.639e-01 | 13 | 4.248e-02 | (59, 152, 1) | (19.736842105263158, 10.0, 1.3) | 1.639e-01 | 0.08977770396901286/0.1541049384436208/0.15937718834151746/0.16301478564611532 |
| upper_b | requested | 4.449e-01 | 13 | 4.248e-02 | (59, 152, 1) | (19.736842105263158, 10.0, 1.3) | 4.449e-01 | 0.24368233934446346/0.41828483291839924/0.43259522549840446/0.4424687038965987 |
| lower_b | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_b | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |

Complete offending states (raw > `1e-10*spacing`; requested > `1e-10`):

| boundary | kind | b_index | a_index | z_index | b | a | z | rate |
|---|---|---|---|---|---|---|---|---|
| upper_b | raw | 59 | 140 | 1 | 19.736842 | 9.210526 | 1.300000 | 7.015659770e-03 |
| upper_b | raw | 59 | 141 | 1 | 19.736842 | 9.276316 | 1.300000 | 2.028249606e-02 |
| upper_b | raw | 59 | 142 | 1 | 19.736842 | 9.342105 | 1.300000 | 3.377984135e-02 |
| upper_b | raw | 59 | 143 | 1 | 19.736842 | 9.407895 | 1.300000 | 4.749935161e-02 |
| upper_b | raw | 59 | 144 | 1 | 19.736842 | 9.473684 | 1.300000 | 6.142613135e-02 |
| upper_b | raw | 59 | 145 | 1 | 19.736842 | 9.539474 | 1.300000 | 7.553411365e-02 |
| upper_b | raw | 59 | 146 | 1 | 19.736842 | 9.605263 | 1.300000 | 8.977770397e-02 |
| upper_b | raw | 59 | 147 | 1 | 19.736842 | 9.671053 | 1.300000 | 1.040763230e-01 |
| upper_b | raw | 59 | 148 | 1 | 19.736842 | 9.736842 | 1.300000 | 1.182851866e-01 |
| upper_b | raw | 59 | 149 | 1 | 19.736842 | 9.802632 | 1.300000 | 1.321389575e-01 |
| upper_b | raw | 59 | 150 | 1 | 19.736842 | 9.868421 | 1.300000 | 1.451412632e-01 |
| upper_b | raw | 59 | 151 | 1 | 19.736842 | 9.934211 | 1.300000 | 1.563458573e-01 |
| upper_b | raw | 59 | 152 | 1 | 19.736842 | 10.000000 | 1.300000 | 1.639241850e-01 |
| upper_b | requested | 59 | 140 | 1 | 19.736842 | 9.210526 | 1.300000 | 1.904250509e-02 |
| upper_b | requested | 59 | 141 | 1 | 19.736842 | 9.276316 | 1.300000 | 5.505248930e-02 |
| upper_b | requested | 59 | 142 | 1 | 19.736842 | 9.342105 | 1.300000 | 9.168814082e-02 |
| upper_b | requested | 59 | 143 | 1 | 19.736842 | 9.407895 | 1.300000 | 1.289268115e-01 |
| upper_b | requested | 59 | 144 | 1 | 19.736842 | 9.473684 | 1.300000 | 1.667280708e-01 |
| upper_b | requested | 59 | 145 | 1 | 19.736842 | 9.539474 | 1.300000 | 2.050211656e-01 |
| upper_b | requested | 59 | 146 | 1 | 19.736842 | 9.605263 | 1.300000 | 2.436823393e-01 |
| upper_b | requested | 59 | 147 | 1 | 19.736842 | 9.671053 | 1.300000 | 2.824928766e-01 |
| upper_b | requested | 59 | 148 | 1 | 19.736842 | 9.736842 | 1.300000 | 3.210597921e-01 |
| upper_b | requested | 59 | 149 | 1 | 19.736842 | 9.802632 | 1.300000 | 3.586628846e-01 |
| upper_b | requested | 59 | 150 | 1 | 19.736842 | 9.868421 | 1.300000 | 3.939548573e-01 |
| upper_b | requested | 59 | 151 | 1 | 19.736842 | 9.934211 | 1.300000 | 4.243673268e-01 |
| upper_b | requested | 59 | 152 | 1 | 19.736842 | 10.000000 | 1.300000 | 4.449370735e-01 |

### I4_A153_B80

| boundary | kind | max | count | share | argmax index | argmax physical | value at argmax | q50/q90/q95/q99 |
|---|---|---|---|---|---|---|---|---|
| upper_a | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 152, 0) | (-2.0, 10.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_a | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 152, 0) | (-2.0, 10.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_a | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_a | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_b | raw | 1.236e-01 | 10 | 3.268e-02 | (79, 152, 1) | (27.105263157894736, 10.0, 1.3) | 1.236e-01 | 0.0711094185332225/0.11686476438863788/0.12025394962080431/0.12296529780653745 |
| upper_b | requested | 3.356e-01 | 10 | 3.268e-02 | (79, 152, 1) | (27.105263157894736, 10.0, 1.3) | 3.356e-01 | 0.19301127887588962/0.3172043604834457/0.3264035775421831/0.33376295118917304 |
| lower_b | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_b | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |

Complete offending states (raw > `1e-10*spacing`; requested > `1e-10`):

| boundary | kind | b_index | a_index | z_index | b | a | z | rate |
|---|---|---|---|---|---|---|---|---|
| upper_b | raw | 79 | 143 | 1 | 27.105263 | 9.407895 | 1.300000 | 7.522070303e-03 |
| upper_b | raw | 79 | 144 | 1 | 27.105263 | 9.473684 | 1.300000 | 2.143427452e-02 |
| upper_b | raw | 79 | 145 | 1 | 27.105263 | 9.539474 | 1.300000 | 3.552522219e-02 |
| upper_b | raw | 79 | 146 | 1 | 27.105263 | 9.605263 | 1.300000 | 4.974819973e-02 |
| upper_b | raw | 79 | 147 | 1 | 27.105263 | 9.671053 | 1.300000 | 6.402118284e-02 |
| upper_b | raw | 79 | 148 | 1 | 27.105263 | 9.736842 | 1.300000 | 7.819765423e-02 |
| upper_b | raw | 79 | 149 | 1 | 27.105263 | 9.802632 | 1.300000 | 9.201055800e-02 |
| upper_b | raw | 79 | 150 | 1 | 27.105263 | 9.868421 | 1.300000 | 1.049628546e-01 |
| upper_b | raw | 79 | 151 | 1 | 27.105263 | 9.934211 | 1.300000 | 1.161116121e-01 |
| upper_b | raw | 79 | 152 | 1 | 27.105263 | 10.000000 | 1.300000 | 1.236431349e-01 |
| upper_b | requested | 79 | 143 | 1 | 27.105263 | 9.407895 | 1.300000 | 2.041704797e-02 |
| upper_b | requested | 79 | 144 | 1 | 27.105263 | 9.473684 | 1.300000 | 5.817874513e-02 |
| upper_b | requested | 79 | 145 | 1 | 27.105263 | 9.539474 | 1.300000 | 9.642560308e-02 |
| upper_b | requested | 79 | 146 | 1 | 27.105263 | 9.605263 | 1.300000 | 1.350308278e-01 |
| upper_b | requested | 79 | 147 | 1 | 27.105263 | 9.671053 | 1.300000 | 1.737717820e-01 |
| upper_b | requested | 79 | 148 | 1 | 27.105263 | 9.736842 | 1.300000 | 2.122507758e-01 |
| upper_b | requested | 79 | 149 | 1 | 27.105263 | 9.802632 | 1.300000 | 2.497429432e-01 |
| upper_b | requested | 79 | 150 | 1 | 27.105263 | 9.868421 | 1.300000 | 2.848991768e-01 |
| upper_b | requested | 79 | 151 | 1 | 27.105263 | 9.934211 | 1.300000 | 3.151600900e-01 |
| upper_b | requested | 79 | 152 | 1 | 27.105263 | 10.000000 | 1.300000 | 3.356027946e-01 |

### I5_A153_B100

| boundary | kind | max | count | share | argmax index | argmax physical | value at argmax | q50/q90/q95/q99 |
|---|---|---|---|---|---|---|---|---|
| upper_a | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 152, 0) | (-2.0, 10.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_a | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 152, 0) | (-2.0, 10.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_a | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_a | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_b | raw | 9.144e-02 | 8 | 2.614e-02 | (99, 152, 1) | (34.473684210526315, 10.0, 1.3) | 9.144e-02 | 0.05303542614249279/0.08618842231058461/0.08881179485803423/0.09091049289599393 |
| upper_b | requested | 2.482e-01 | 8 | 2.614e-02 | (99, 152, 1) | (34.473684210526315, 10.0, 1.3) | 2.482e-01 | 0.14395329952962327/0.23394000341444393/0.24106058604323574/0.2467570521462692 |
| lower_b | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_b | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |

Complete offending states (raw > `1e-10*spacing`; requested > `1e-10`):

| boundary | kind | b_index | a_index | z_index | b | a | z | rate |
|---|---|---|---|---|---|---|---|---|
| upper_b | raw | 99 | 145 | 1 | 34.473684 | 9.539474 | 1.300000 | 3.549058227e-03 |
| upper_b | raw | 99 | 146 | 1 | 34.473684 | 9.605263 | 1.300000 | 1.775095122e-02 |
| upper_b | raw | 99 | 147 | 1 | 34.473684 | 9.671053 | 1.300000 | 3.199934125e-02 |
| upper_b | raw | 99 | 148 | 1 | 34.473684 | 9.736842 | 1.300000 | 4.614652458e-02 |
| upper_b | raw | 99 | 149 | 1 | 34.473684 | 9.802632 | 1.300000 | 5.992432771e-02 |
| upper_b | raw | 99 | 150 | 1 | 34.473684 | 9.868421 | 1.300000 | 7.283546217e-02 |
| upper_b | raw | 99 | 151 | 1 | 34.473684 | 9.934211 | 1.300000 | 8.393981727e-02 |
| upper_b | raw | 99 | 152 | 1 | 34.473684 | 10.000000 | 1.300000 | 9.143516741e-02 |
| upper_b | requested | 99 | 145 | 1 | 34.473684 | 9.539474 | 1.300000 | 9.633158044e-03 |
| upper_b | requested | 99 | 146 | 1 | 34.473684 | 9.605263 | 1.300000 | 4.818115330e-02 |
| upper_b | requested | 99 | 147 | 1 | 34.473684 | 9.671053 | 1.300000 | 8.685535481e-02 |
| upper_b | requested | 99 | 148 | 1 | 34.473684 | 9.736842 | 1.300000 | 1.252548524e-01 |
| upper_b | requested | 99 | 149 | 1 | 34.473684 | 9.802632 | 1.300000 | 1.626517466e-01 |
| upper_b | requested | 99 | 150 | 1 | 34.473684 | 9.868421 | 1.300000 | 1.976962545e-01 |
| upper_b | requested | 99 | 151 | 1 | 34.473684 | 9.934211 | 1.300000 | 2.278366469e-01 |
| upper_b | requested | 99 | 152 | 1 | 34.473684 | 10.000000 | 1.300000 | 2.481811687e-01 |

## Same-a b-extent trends (Phase C: I0->I1->I2 and I3->I4->I5)

### aa77

| b extent | variant | raw upper-b max | requested upper-b max | raw count | requested count | argmax physical (a,z) | upper-a compatible |
|---|---|---|---|---|---|---|---|
| b60 | I0_A77_B60 | 1.443e-01 | 3.916e-01 | 7 | 7 | (10.0, 1.3) | True |
| b80 | I1_A77_B80 | 1.035e-01 | 2.808e-01 | 5 | 5 | (10.0, 1.3) | True |
| b100 | I2_A77_B100 | 7.094e-02 | 1.925e-01 | 4 | 4 | (10.0, 1.3) | True |

- adjacent raw attenuation ratios (b60/b80, b80/b100): [1.39437, 1.458506]
- adjacent requested attenuation ratios: [1.39437, 1.458506]
- raw ratios relative to b60: [1.0, 0.71717, 0.491716]
- requested ratios relative to b60: [1.0, 0.71717, 0.491716]
- strictly decreasing requested upper-b max over extents: True
- non-increasing requested flag: True
- plateau flag: False
- monotonic flag: strictly_decreasing
- first b extent with requested upper-b <= 1e-10: None
- upper-a compatible on every b extent: True

### aa153

| b extent | variant | raw upper-b max | requested upper-b max | raw count | requested count | argmax physical (a,z) | upper-a compatible |
|---|---|---|---|---|---|---|---|
| b60 | I3_A153_B60 | 1.639e-01 | 4.449e-01 | 13 | 13 | (10.0, 1.3) | True |
| b80 | I4_A153_B80 | 1.236e-01 | 3.356e-01 | 10 | 10 | (10.0, 1.3) | True |
| b100 | I5_A153_B100 | 9.144e-02 | 2.482e-01 | 8 | 8 | (10.0, 1.3) | True |

- adjacent raw attenuation ratios (b60/b80, b80/b100): [1.325785, 1.352249]
- adjacent requested attenuation ratios: [1.325785, 1.352249]
- raw ratios relative to b60: [1.0, 0.75427, 0.557789]
- requested ratios relative to b60: [1.0, 0.75427, 0.557789]
- strictly decreasing requested upper-b max over extents: True
- non-increasing requested flag: True
- plateau flag: False
- monotonic flag: strictly_decreasing
- first b extent with requested upper-b <= 1e-10: None
- upper-a compatible on every b extent: True

These are policy-only trends; any upper-a reactivation on an extended b extent is preserved as evidence, not clipped.

## Cross-a exact-node policy comparisons (Phase D)

Three required pairs at common b extents (a77 vs every-second a153, all common b nodes, all z, no interpolation). Shared-interior mask excludes the top two coarse layers in BOTH asset dimensions. `rel_diff = max_abs / max(1, max|coarse|)` is scale-aware.

### I0_A77_B60_vs_I3_A153_B60 (bb60)

| field | max_abs_diff | rel_diff | label mismatch |
|---|---|---|---|
| value | 6.512e-02 | 9.528e-04 | — |
| consumption | 1.545e-03 | 1.041e-03 | — |
| labor | 6.281e-04 | 5.611e-04 | — |
| transfer | 2.429e-02 | 2.204e-02 | — |
| mu_a | 2.429e-02 | 2.429e-02 | — |
| mu_b | 1.913e-02 | 1.913e-02 | — |
| liquid_label | — | — | 24 |
| transfer_label | — | — | 70 |

### I1_A77_B80_vs_I4_A153_B80 (bb80)

| field | max_abs_diff | rel_diff | label mismatch |
|---|---|---|---|
| value | 6.512e-02 | 9.528e-04 | — |
| consumption | 1.740e-03 | 1.085e-03 | — |
| labor | 6.281e-04 | 5.611e-04 | — |
| transfer | 2.429e-02 | 2.204e-02 | — |
| mu_a | 2.429e-02 | 2.429e-02 | — |
| mu_b | 1.913e-02 | 1.913e-02 | — |
| liquid_label | — | — | 25 |
| transfer_label | — | — | 72 |

### I2_A77_B100_vs_I5_A153_B100 (bb100)

| field | max_abs_diff | rel_diff | label mismatch |
|---|---|---|---|
| value | 6.512e-02 | 9.528e-04 | — |
| consumption | 1.740e-03 | 1.013e-03 | — |
| labor | 6.281e-04 | 5.611e-04 | — |
| transfer | 2.429e-02 | 2.204e-02 | — |
| mu_a | 2.429e-02 | 2.429e-02 | — |
| mu_b | 1.913e-02 | 1.913e-02 | — |
| liquid_label | — | — | 25 |
| transfer_label | — | — | 72 |

## Joint HJB upper-boundary policy compatibility frontier (Phase E)

Per-variant prerequisite marker: `requested_upper_b <= 1e-10 AND requested_upper_a <= 1e-10`. `CROSS_A_RESOLUTION_JOINT_COMPATIBLE_AT_B_EXTENT` holds only when BOTH mature a resolutions at the same b extent pass both thresholds. Prerequisite marker only — it does NOT authorize stationary KFE.

- I0_A77_B60: JOINT_HJB_BOUNDARY_POLICY_NOT_COMPATIBLE (ua 0.000e+00, ub 3.916e-01)
- I1_A77_B80: JOINT_HJB_BOUNDARY_POLICY_NOT_COMPATIBLE (ua 0.000e+00, ub 2.808e-01)
- I2_A77_B100: JOINT_HJB_BOUNDARY_POLICY_NOT_COMPATIBLE (ua 0.000e+00, ub 1.925e-01)
- I3_A153_B60: JOINT_HJB_BOUNDARY_POLICY_NOT_COMPATIBLE (ua 0.000e+00, ub 4.449e-01)
- I4_A153_B80: JOINT_HJB_BOUNDARY_POLICY_NOT_COMPATIBLE (ua 0.000e+00, ub 3.356e-01)
- I5_A153_B100: JOINT_HJB_BOUNDARY_POLICY_NOT_COMPATIBLE (ua 0.000e+00, ub 2.482e-01)

- bb60 cross-a: a77=False, a153=False -> CROSS_A_RESOLUTION_JOINT_NOT_COMPATIBLE_AT_B_EXTENT
- bb80 cross-a: a77=False, a153=False -> CROSS_A_RESOLUTION_JOINT_NOT_COMPATIBLE_AT_B_EXTENT
- bb100 cross-a: a77=False, a153=False -> CROSS_A_RESOLUTION_JOINT_NOT_COMPATIBLE_AT_B_EXTENT

Stationary KFE / nullspace / pin / density / tail mass / stationary flux / `C,L,A,B` are `NOT_AUTHORIZED__DLH_5I_POLICY_ONLY_COUPLED_FRONTIER_DIAGNOSTIC` and were not executed.

## Reproducibility

- randomness: `NOT_APPLICABLE`; repeat pass: `True`; terminal run1/run2: `DLH_5I_COUPLED_B_EXTENT_ATTENUATION_CONFIRMED__COMMON_THRESHOLD_NOT_REACHED__GPT_REVIEW_REQUIRED` / `DLH_5I_COUPLED_B_EXTENT_ATTENUATION_CONFIRMED__COMMON_THRESHOLD_NOT_REACHED__GPT_REVIEW_REQUIRED`; annotations run1/run2: ['DLH_5I_CROSS_A_POLICY_RESOLUTION_SENSITIVITY_REMAINS_MATERIAL__NUMERICAL_REVIEW_REQUIRED'] / ['DLH_5I_CROSS_A_POLICY_RESOLUTION_SENSITIVITY_REMAINS_MATERIAL__NUMERICAL_REVIEW_REQUIRED'].
- I0_A77_B60: structural identical True, max numeric diff 0.000e+00, aligned non-finite 0, mismatched 0, pass True.
- I1_A77_B80: structural identical True, max numeric diff 0.000e+00, aligned non-finite 0, mismatched 0, pass True.
- I2_A77_B100: structural identical True, max numeric diff 0.000e+00, aligned non-finite 0, mismatched 0, pass True.
- I3_A153_B60: structural identical True, max numeric diff 0.000e+00, aligned non-finite 0, mismatched 0, pass True.
- I4_A153_B80: structural identical True, max numeric diff 0.000e+00, aligned non-finite 0, mismatched 0, pass True.
- I5_A153_B100: structural identical True, max numeric diff 0.000e+00, aligned non-finite 0, mismatched 0, pass True.

## Artifact integrity

- accepted MATLAB-faithful oracle blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`, SHA-256 `1795718C469FC3B427CAB8E3D5957C133BEAD6EACC9EF0A25A3EDB7211D1A024` re-verified read-only (unchanged from the accepted Issue #23/#26 state).
- no existing tracked file modified; dedicated branch `dsh/issue-35-dlh-5i-coupled-boundary-frontier-2026-09-01`; allowlist-only additions (3 artifacts + 8 evidence files).

DLH-5I implements NO repair and NO stationary acceptance: accepted HJB/KFE/regional source immutable; physical a-domain/a_max/taper/economics/tolerances/initialization frozen; a77/a153 only; db=7/19 only; no clipping; no D1-D3; no regional or multi-province GE; no learned network; no nominal HANK.