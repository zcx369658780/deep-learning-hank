# DLH-5H — Illiquid Upper-Boundary Resolution Diagnostic (Issue #34)

Policy-only diagnostic isolating illiquid-grid resolution on the provisional liquid-safe domain. Accepted MATLAB-faithful HJB source is immutable and reused read-only.

Overall terminal classification: `BLOCKED_DLH_5H_LIQUID_BOUNDARY_REACTIVATION_ON_ILLIQUID_RESOLUTION_VARIANTS`

Secondary scientific annotations: `DLH_5H_POLICY_RESOLUTION_SENSITIVITY_REMAINS_MATERIAL__NUMERICAL_REVIEW_REQUIRED`

Frozen economics: `wbar=1.0`, `r_a=0.03`; physical illiquid domain `a [0.0,10.0]`, `a_max=10.0`, taper `r_a*(1-0.1*(a/a_max)^9)_MATLAB_FAITHFUL_UNCHANGED`; liquid-safe core `b60 [-2.0,19.736842105263158]`, `db=0.368421052632` (PROVISIONAL_LIQUID_SAFE_DIAGNOSTIC_DOMAIN_NOT_FINAL_PRODUCTION_GRID); all non-grid objects the accepted DLH-5B/DLH-5E fixture (`configs/dlh_5b_two_region_symmetric_anchor.toml`, region_index=0).

## Variant status (Phase A)

| variant | b pts | db | a pts | da | HJB conv | iters | stat | raw upper-a max | raw lower-a max | joint marker |
|---|---|---|---|---|---|---|---|---|---|---|
| H0_A20_BASE | 60 | 0.368421052631579 | 20 | 0.5263157894736842 | True | 11 | 1.172e-08 | 1.629e-01 | 0.000e+00 | JOINT_HJB_BOUNDARY_POLICY_NOT_COMPATIBLE |
| H1_A39_FINE | 60 | 0.368421052631579 | 39 | 0.2631578947368421 | True | 11 | 9.537e-09 | 0.000e+00 | 0.000e+00 | JOINT_HJB_BOUNDARY_POLICY_NOT_COMPATIBLE |
| H2_A77_FINER | 60 | 0.368421052631579 | 77 | 0.13157894736842105 | True | 10 | 6.171e-08 | 0.000e+00 | 0.000e+00 | JOINT_HJB_BOUNDARY_POLICY_NOT_COMPATIBLE |
| H3_A153_FINEST | 60 | 0.368421052631579 | 153 | 0.06578947368421052 | True | 10 | 1.805e-08 | 0.000e+00 | 0.000e+00 | JOINT_HJB_BOUNDARY_POLICY_NOT_COMPATIBLE |
| H4_B119_A39 | 119 | 0.18421052631578938 | 39 | 0.2631578947368421 | True | 11 | 1.268e-08 | 0.000e+00 | 0.000e+00 | JOINT_HJB_BOUNDARY_POLICY_NOT_COMPATIBLE |
| H5_B119_A77 | 119 | 0.18421052631578938 | 77 | 0.13157894736842105 | True | 10 | 7.422e-08 | 0.000e+00 | 0.000e+00 | JOINT_HJB_BOUNDARY_POLICY_NOT_COMPATIBLE |

## Illiquid upper/lower boundary diagnostics (Phase B)

Raw drift (`max(mu_a,0)` / `max(-mu_a,0)`) is the primary cross-resolution quantity; requested generator rate (raw/`da`) is the HJB/KFE compatibility quantity. Raw threshold = `1e-10*da` corresponds to the accepted requested-rate threshold `1e-10`. Coordinates are exact `(b_index,a_index,z_index)` plus physical `(b,a,z)` via C-order unraveling on the actual 2-D boundary slice.

### H0_A20_BASE

| boundary | kind | max | count | share | argmax index | argmax physical | value at argmax | q50/q90/q95/q99 |
|---|---|---|---|---|---|---|---|---|
| upper_a | raw | 1.629e-01 | 108 | 9.000e-01 | (22, 19, 0) | (6.105263157894736, 10.0, 0.8) | 1.629e-01 | 0.12182043836802761/0.16087173036536837/0.16220356008790573/0.1626835931132292 |
| upper_a | requested | 3.095e-01 | 108 | 9.000e-01 | (22, 19, 0) | (6.105263157894736, 10.0, 0.8) | 3.095e-01 | 0.23145883289925248/0.3056562876941999/0.3081867641670209/0.30909882691513546 |
| lower_a | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_a | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |

Complete offending states (raw > `1e-10*da`; requested > `1e-10`):

| boundary | kind | b_index | a_index | z_index | b | a | z | rate |
|---|---|---|---|---|---|---|---|---|
| upper_a | raw | 5 | 19 | 1 | -0.157895 | 10.000000 | 1.300000 | 1.758189188e-03 |
| upper_a | raw | 6 | 19 | 1 | 0.210526 | 10.000000 | 1.300000 | 5.458868695e-02 |
| upper_a | raw | 7 | 19 | 0 | 0.578947 | 10.000000 | 0.800000 | 1.558600899e-02 |
| upper_a | raw | 7 | 19 | 1 | 0.578947 | 10.000000 | 1.300000 | 7.709734529e-02 |
| upper_a | raw | 8 | 19 | 0 | 0.947368 | 10.000000 | 0.800000 | 4.760505371e-02 |
| upper_a | raw | 8 | 19 | 1 | 0.947368 | 10.000000 | 1.300000 | 9.317004762e-02 |
| upper_a | raw | 9 | 19 | 0 | 1.315789 | 10.000000 | 0.800000 | 7.226973068e-02 |
| upper_a | raw | 9 | 19 | 1 | 1.315789 | 10.000000 | 1.300000 | 1.075585329e-01 |
| upper_a | raw | 10 | 19 | 0 | 1.684211 | 10.000000 | 0.800000 | 9.172932859e-02 |
| upper_a | raw | 10 | 19 | 1 | 1.684211 | 10.000000 | 1.300000 | 1.197008620e-01 |
| upper_a | raw | 11 | 19 | 0 | 2.052632 | 10.000000 | 0.800000 | 1.073178739e-01 |
| upper_a | raw | 11 | 19 | 1 | 2.052632 | 10.000000 | 1.300000 | 1.297443150e-01 |
| upper_a | raw | 12 | 19 | 0 | 2.421053 | 10.000000 | 0.800000 | 1.199180025e-01 |
| upper_a | raw | 12 | 19 | 1 | 2.421053 | 10.000000 | 1.300000 | 1.379679578e-01 |
| upper_a | raw | 13 | 19 | 0 | 2.789474 | 10.000000 | 0.800000 | 1.301403847e-01 |
| upper_a | raw | 13 | 19 | 1 | 2.789474 | 10.000000 | 1.300000 | 1.446311060e-01 |
| upper_a | raw | 14 | 19 | 0 | 3.157895 | 10.000000 | 0.800000 | 1.384274248e-01 |
| upper_a | raw | 14 | 19 | 1 | 3.157895 | 10.000000 | 1.300000 | 1.499696146e-01 |
| upper_a | raw | 15 | 19 | 0 | 3.526316 | 10.000000 | 0.800000 | 1.451095312e-01 |
| upper_a | raw | 15 | 19 | 1 | 3.526316 | 10.000000 | 1.300000 | 1.541730505e-01 |
| upper_a | raw | 16 | 19 | 0 | 3.894737 | 10.000000 | 0.800000 | 1.504400719e-01 |
| upper_a | raw | 16 | 19 | 1 | 3.894737 | 10.000000 | 1.300000 | 1.573946675e-01 |
| upper_a | raw | 17 | 19 | 0 | 4.263158 | 10.000000 | 0.800000 | 1.546176933e-01 |
| upper_a | raw | 17 | 19 | 1 | 4.263158 | 10.000000 | 1.300000 | 1.597600036e-01 |
| upper_a | raw | 18 | 19 | 0 | 4.631579 | 10.000000 | 0.800000 | 1.578012493e-01 |
| upper_a | raw | 18 | 19 | 1 | 4.631579 | 10.000000 | 1.300000 | 1.613734752e-01 |
| upper_a | raw | 19 | 19 | 0 | 5.000000 | 10.000000 | 0.800000 | 1.601201304e-01 |
| upper_a | raw | 19 | 19 | 1 | 5.000000 | 10.000000 | 1.300000 | 1.623233039e-01 |
| upper_a | raw | 20 | 19 | 0 | 5.368421 | 10.000000 | 0.800000 | 1.616815761e-01 |
| upper_a | raw | 20 | 19 | 1 | 5.368421 | 10.000000 | 1.300000 | 1.626851724e-01 |
| upper_a | raw | 21 | 19 | 0 | 5.736842 | 10.000000 | 0.800000 | 1.625759455e-01 |
| upper_a | raw | 21 | 19 | 1 | 5.736842 | 10.000000 | 1.300000 | 1.625249469e-01 |
| upper_a | raw | 22 | 19 | 0 | 6.105263 | 10.000000 | 0.800000 | 1.628805713e-01 |
| upper_a | raw | 22 | 19 | 1 | 6.105263 | 10.000000 | 1.300000 | 1.619007201e-01 |
| upper_a | raw | 23 | 19 | 0 | 6.473684 | 10.000000 | 0.800000 | 1.626626112e-01 |
| upper_a | raw | 23 | 19 | 1 | 6.473684 | 10.000000 | 1.300000 | 1.608643524e-01 |
| upper_a | raw | 24 | 19 | 0 | 6.842105 | 10.000000 | 0.800000 | 1.619811786e-01 |
| upper_a | raw | 24 | 19 | 1 | 6.842105 | 10.000000 | 1.300000 | 1.594626407e-01 |
| upper_a | raw | 25 | 19 | 0 | 7.210526 | 10.000000 | 0.800000 | 1.608889455e-01 |
| upper_a | raw | 25 | 19 | 1 | 7.210526 | 10.000000 | 1.300000 | 1.577382049e-01 |
| upper_a | raw | 26 | 19 | 0 | 7.578947 | 10.000000 | 0.800000 | 1.594333550e-01 |
| upper_a | raw | 26 | 19 | 1 | 7.578947 | 10.000000 | 1.300000 | 1.557301607e-01 |
| upper_a | raw | 27 | 19 | 0 | 7.947368 | 10.000000 | 0.800000 | 1.576575395e-01 |
| upper_a | raw | 27 | 19 | 1 | 7.947368 | 10.000000 | 1.300000 | 1.534746270e-01 |
| upper_a | raw | 28 | 19 | 0 | 8.315789 | 10.000000 | 0.800000 | 1.556010163e-01 |
| upper_a | raw | 28 | 19 | 1 | 8.315789 | 10.000000 | 1.300000 | 1.510051055e-01 |
| upper_a | raw | 29 | 19 | 0 | 8.684211 | 10.000000 | 0.800000 | 1.533002119e-01 |
| upper_a | raw | 29 | 19 | 1 | 8.684211 | 10.000000 | 1.300000 | 1.483527626e-01 |
| upper_a | raw | 30 | 19 | 0 | 9.052632 | 10.000000 | 0.800000 | 1.507888541e-01 |
| upper_a | raw | 30 | 19 | 1 | 9.052632 | 10.000000 | 1.300000 | 1.455466345e-01 |
| upper_a | raw | 31 | 19 | 0 | 9.421053 | 10.000000 | 0.800000 | 1.480982641e-01 |
| upper_a | raw | 31 | 19 | 1 | 9.421053 | 10.000000 | 1.300000 | 1.426137762e-01 |
| upper_a | raw | 32 | 19 | 0 | 9.789474 | 10.000000 | 0.800000 | 1.452575704e-01 |
| upper_a | raw | 32 | 19 | 1 | 9.789474 | 10.000000 | 1.300000 | 1.395793663e-01 |
| upper_a | raw | 33 | 19 | 0 | 10.157895 | 10.000000 | 0.800000 | 1.422938636e-01 |
| upper_a | raw | 33 | 19 | 1 | 10.157895 | 10.000000 | 1.300000 | 1.364667825e-01 |
| upper_a | raw | 34 | 19 | 0 | 10.526316 | 10.000000 | 0.800000 | 1.392323091e-01 |
| upper_a | raw | 34 | 19 | 1 | 10.526316 | 10.000000 | 1.300000 | 1.332976556e-01 |
| upper_a | raw | 35 | 19 | 0 | 10.894737 | 10.000000 | 0.800000 | 1.360962275e-01 |
| upper_a | raw | 35 | 19 | 1 | 10.894737 | 10.000000 | 1.300000 | 1.300919110e-01 |
| upper_a | raw | 36 | 19 | 0 | 11.263158 | 10.000000 | 0.800000 | 1.329071546e-01 |
| upper_a | raw | 36 | 19 | 1 | 11.263158 | 10.000000 | 1.300000 | 1.268678031e-01 |
| upper_a | raw | 37 | 19 | 0 | 11.631579 | 10.000000 | 0.800000 | 1.296848881e-01 |
| upper_a | raw | 37 | 19 | 1 | 11.631579 | 10.000000 | 1.300000 | 1.236419489e-01 |
| upper_a | raw | 38 | 19 | 0 | 12.000000 | 10.000000 | 0.800000 | 1.264475280e-01 |
| upper_a | raw | 38 | 19 | 1 | 12.000000 | 10.000000 | 1.300000 | 1.204293627e-01 |
| upper_a | raw | 39 | 19 | 0 | 12.368421 | 10.000000 | 0.800000 | 1.232115140e-01 |
| upper_a | raw | 39 | 19 | 1 | 12.368421 | 10.000000 | 1.300000 | 1.172434954e-01 |
| upper_a | raw | 40 | 19 | 0 | 12.736842 | 10.000000 | 0.800000 | 1.199916655e-01 |
| upper_a | raw | 40 | 19 | 1 | 12.736842 | 10.000000 | 1.300000 | 1.140962788e-01 |
| upper_a | raw | 41 | 19 | 0 | 13.105263 | 10.000000 | 0.800000 | 1.168012238e-01 |
| upper_a | raw | 41 | 19 | 1 | 13.105263 | 10.000000 | 1.300000 | 1.109981743e-01 |
| upper_a | raw | 42 | 19 | 0 | 13.473684 | 10.000000 | 0.800000 | 1.136518988e-01 |
| upper_a | raw | 42 | 19 | 1 | 13.473684 | 10.000000 | 1.300000 | 1.079582240e-01 |
| upper_a | raw | 43 | 19 | 0 | 13.842105 | 10.000000 | 0.800000 | 1.105539168e-01 |
| upper_a | raw | 43 | 19 | 1 | 13.842105 | 10.000000 | 1.300000 | 1.049840964e-01 |
| upper_a | raw | 44 | 19 | 0 | 14.210526 | 10.000000 | 0.800000 | 1.075160648e-01 |
| upper_a | raw | 44 | 19 | 1 | 14.210526 | 10.000000 | 1.300000 | 1.020821146e-01 |
| upper_a | raw | 45 | 19 | 0 | 14.578947 | 10.000000 | 0.800000 | 1.045457183e-01 |
| upper_a | raw | 45 | 19 | 1 | 14.578947 | 10.000000 | 1.300000 | 9.925723812e-02 |
| upper_a | raw | 46 | 19 | 0 | 14.947368 | 10.000000 | 0.800000 | 1.016488278e-01 |
| upper_a | raw | 46 | 19 | 1 | 14.947368 | 10.000000 | 1.300000 | 9.651294171e-02 |
| upper_a | raw | 47 | 19 | 0 | 15.315789 | 10.000000 | 0.800000 | 9.882981022e-02 |
| upper_a | raw | 47 | 19 | 1 | 15.315789 | 10.000000 | 1.300000 | 9.385087515e-02 |
| upper_a | raw | 48 | 19 | 0 | 15.684211 | 10.000000 | 0.800000 | 9.609123756e-02 |
| upper_a | raw | 48 | 19 | 1 | 15.684211 | 10.000000 | 1.300000 | 9.127006231e-02 |
| upper_a | raw | 49 | 19 | 0 | 16.052632 | 10.000000 | 0.800000 | 9.343309730e-02 |
| upper_a | raw | 49 | 19 | 1 | 16.052632 | 10.000000 | 1.300000 | 8.876514429e-02 |
| upper_a | raw | 50 | 19 | 0 | 16.421053 | 10.000000 | 0.800000 | 9.085116200e-02 |
| upper_a | raw | 50 | 19 | 1 | 16.421053 | 10.000000 | 1.300000 | 8.632264468e-02 |
| upper_a | raw | 51 | 19 | 0 | 16.789474 | 10.000000 | 0.800000 | 8.833350832e-02 |
| upper_a | raw | 51 | 19 | 1 | 16.789474 | 10.000000 | 1.300000 | 8.391316131e-02 |
| upper_a | raw | 52 | 19 | 0 | 17.157895 | 10.000000 | 0.800000 | 8.585318947e-02 |
| upper_a | raw | 52 | 19 | 1 | 17.157895 | 10.000000 | 1.300000 | 8.147521605e-02 |
| upper_a | raw | 53 | 19 | 0 | 17.526316 | 10.000000 | 0.800000 | 8.335283702e-02 |
| upper_a | raw | 53 | 19 | 1 | 17.526316 | 10.000000 | 1.300000 | 7.888220280e-02 |
| upper_a | raw | 54 | 19 | 0 | 17.894737 | 10.000000 | 0.800000 | 8.071183691e-02 |
| upper_a | raw | 54 | 19 | 1 | 17.894737 | 10.000000 | 1.300000 | 7.587581376e-02 |
| upper_a | raw | 55 | 19 | 0 | 18.263158 | 10.000000 | 0.800000 | 7.767312774e-02 |
| upper_a | raw | 55 | 19 | 1 | 18.263158 | 10.000000 | 1.300000 | 7.193593798e-02 |
| upper_a | raw | 56 | 19 | 0 | 18.631579 | 10.000000 | 0.800000 | 7.366278308e-02 |
| upper_a | raw | 56 | 19 | 1 | 18.631579 | 10.000000 | 1.300000 | 6.604215771e-02 |
| upper_a | raw | 57 | 19 | 0 | 19.000000 | 10.000000 | 0.800000 | 6.726932196e-02 |
| upper_a | raw | 57 | 19 | 1 | 19.000000 | 10.000000 | 1.300000 | 5.629786821e-02 |
| upper_a | raw | 58 | 19 | 0 | 19.368421 | 10.000000 | 0.800000 | 5.451531336e-02 |
| upper_a | raw | 58 | 19 | 1 | 19.368421 | 10.000000 | 1.300000 | 3.956945031e-02 |
| upper_a | raw | 59 | 19 | 0 | 19.736842 | 10.000000 | 0.800000 | 2.334621007e-02 |
| upper_a | raw | 59 | 19 | 1 | 19.736842 | 10.000000 | 1.300000 | 1.204303628e-02 |
| upper_a | requested | 5 | 19 | 1 | -0.157895 | 10.000000 | 1.300000 | 3.340559457e-03 |
| upper_a | requested | 6 | 19 | 1 | 0.210526 | 10.000000 | 1.300000 | 1.037185052e-01 |
| upper_a | requested | 7 | 19 | 0 | 0.578947 | 10.000000 | 0.800000 | 2.961341708e-02 |
| upper_a | requested | 7 | 19 | 1 | 0.578947 | 10.000000 | 1.300000 | 1.464849560e-01 |
| upper_a | requested | 8 | 19 | 0 | 0.947368 | 10.000000 | 0.800000 | 9.044960205e-02 |
| upper_a | requested | 8 | 19 | 1 | 0.947368 | 10.000000 | 1.300000 | 1.770230905e-01 |
| upper_a | requested | 9 | 19 | 0 | 1.315789 | 10.000000 | 0.800000 | 1.373124883e-01 |
| upper_a | requested | 9 | 19 | 1 | 1.315789 | 10.000000 | 1.300000 | 2.043612125e-01 |
| upper_a | requested | 10 | 19 | 0 | 1.684211 | 10.000000 | 0.800000 | 1.742857243e-01 |
| upper_a | requested | 10 | 19 | 1 | 1.684211 | 10.000000 | 1.300000 | 2.274316379e-01 |
| upper_a | requested | 11 | 19 | 0 | 2.052632 | 10.000000 | 0.800000 | 2.039039604e-01 |
| upper_a | requested | 11 | 19 | 1 | 2.052632 | 10.000000 | 1.300000 | 2.465141985e-01 |
| upper_a | requested | 12 | 19 | 0 | 2.421053 | 10.000000 | 0.800000 | 2.278442048e-01 |
| upper_a | requested | 12 | 19 | 1 | 2.421053 | 10.000000 | 1.300000 | 2.621391199e-01 |
| upper_a | requested | 13 | 19 | 0 | 2.789474 | 10.000000 | 0.800000 | 2.472667309e-01 |
| upper_a | requested | 13 | 19 | 1 | 2.789474 | 10.000000 | 1.300000 | 2.747991013e-01 |
| upper_a | requested | 14 | 19 | 0 | 3.157895 | 10.000000 | 0.800000 | 2.630121071e-01 |
| upper_a | requested | 14 | 19 | 1 | 3.157895 | 10.000000 | 1.300000 | 2.849422677e-01 |
| upper_a | requested | 15 | 19 | 0 | 3.526316 | 10.000000 | 0.800000 | 2.757081093e-01 |
| upper_a | requested | 15 | 19 | 1 | 3.526316 | 10.000000 | 1.300000 | 2.929287959e-01 |
| upper_a | requested | 16 | 19 | 0 | 3.894737 | 10.000000 | 0.800000 | 2.858361367e-01 |
| upper_a | requested | 16 | 19 | 1 | 3.894737 | 10.000000 | 1.300000 | 2.990498682e-01 |
| upper_a | requested | 17 | 19 | 0 | 4.263158 | 10.000000 | 0.800000 | 2.937736172e-01 |
| upper_a | requested | 17 | 19 | 1 | 4.263158 | 10.000000 | 1.300000 | 3.035440069e-01 |
| upper_a | requested | 18 | 19 | 0 | 4.631579 | 10.000000 | 0.800000 | 2.998223737e-01 |
| upper_a | requested | 18 | 19 | 1 | 4.631579 | 10.000000 | 1.300000 | 3.066096029e-01 |
| upper_a | requested | 19 | 19 | 0 | 5.000000 | 10.000000 | 0.800000 | 3.042282478e-01 |
| upper_a | requested | 19 | 19 | 1 | 5.000000 | 10.000000 | 1.300000 | 3.084142775e-01 |
| upper_a | requested | 20 | 19 | 0 | 5.368421 | 10.000000 | 0.800000 | 3.071949946e-01 |
| upper_a | requested | 20 | 19 | 1 | 5.368421 | 10.000000 | 1.300000 | 3.091018276e-01 |
| upper_a | requested | 21 | 19 | 0 | 5.736842 | 10.000000 | 0.800000 | 3.088942964e-01 |
| upper_a | requested | 21 | 19 | 1 | 5.736842 | 10.000000 | 1.300000 | 3.087973991e-01 |
| upper_a | requested | 22 | 19 | 0 | 6.105263 | 10.000000 | 0.800000 | 3.094730854e-01 |
| upper_a | requested | 22 | 19 | 1 | 6.105263 | 10.000000 | 1.300000 | 3.076113682e-01 |
| upper_a | requested | 23 | 19 | 0 | 6.473684 | 10.000000 | 0.800000 | 3.090589613e-01 |
| upper_a | requested | 23 | 19 | 1 | 6.473684 | 10.000000 | 1.300000 | 3.056422696e-01 |
| upper_a | requested | 24 | 19 | 0 | 6.842105 | 10.000000 | 0.800000 | 3.077642394e-01 |
| upper_a | requested | 24 | 19 | 1 | 6.842105 | 10.000000 | 1.300000 | 3.029790173e-01 |
| upper_a | requested | 25 | 19 | 0 | 7.210526 | 10.000000 | 0.800000 | 3.056889965e-01 |
| upper_a | requested | 25 | 19 | 1 | 7.210526 | 10.000000 | 1.300000 | 2.997025893e-01 |
| upper_a | requested | 26 | 19 | 0 | 7.578947 | 10.000000 | 0.800000 | 3.029233744e-01 |
| upper_a | requested | 26 | 19 | 1 | 7.578947 | 10.000000 | 1.300000 | 2.958873054e-01 |
| upper_a | requested | 27 | 19 | 0 | 7.947368 | 10.000000 | 0.800000 | 2.995493250e-01 |
| upper_a | requested | 27 | 19 | 1 | 7.947368 | 10.000000 | 1.300000 | 2.916017913e-01 |
| upper_a | requested | 28 | 19 | 0 | 8.315789 | 10.000000 | 0.800000 | 2.956419311e-01 |
| upper_a | requested | 28 | 19 | 1 | 8.315789 | 10.000000 | 1.300000 | 2.869097005e-01 |
| upper_a | requested | 29 | 19 | 0 | 8.684211 | 10.000000 | 0.800000 | 2.912704026e-01 |
| upper_a | requested | 29 | 19 | 1 | 8.684211 | 10.000000 | 1.300000 | 2.818702489e-01 |
| upper_a | requested | 30 | 19 | 0 | 9.052632 | 10.000000 | 0.800000 | 2.864988227e-01 |
| upper_a | requested | 30 | 19 | 1 | 9.052632 | 10.000000 | 1.300000 | 2.765386056e-01 |
| upper_a | requested | 31 | 19 | 0 | 9.421053 | 10.000000 | 0.800000 | 2.813867019e-01 |
| upper_a | requested | 31 | 19 | 1 | 9.421053 | 10.000000 | 1.300000 | 2.709661747e-01 |
| upper_a | requested | 32 | 19 | 0 | 9.789474 | 10.000000 | 0.800000 | 2.759893837e-01 |
| upper_a | requested | 32 | 19 | 1 | 9.789474 | 10.000000 | 1.300000 | 2.652007959e-01 |
| upper_a | requested | 33 | 19 | 0 | 10.157895 | 10.000000 | 0.800000 | 2.703583409e-01 |
| upper_a | requested | 33 | 19 | 1 | 10.157895 | 10.000000 | 1.300000 | 2.592868867e-01 |
| upper_a | requested | 34 | 19 | 0 | 10.526316 | 10.000000 | 0.800000 | 2.645413874e-01 |
| upper_a | requested | 34 | 19 | 1 | 10.526316 | 10.000000 | 1.300000 | 2.532655457e-01 |
| upper_a | requested | 35 | 19 | 0 | 10.894737 | 10.000000 | 0.800000 | 2.585828323e-01 |
| upper_a | requested | 35 | 19 | 1 | 10.894737 | 10.000000 | 1.300000 | 2.471746309e-01 |
| upper_a | requested | 36 | 19 | 0 | 11.263158 | 10.000000 | 0.800000 | 2.525235937e-01 |
| upper_a | requested | 36 | 19 | 1 | 11.263158 | 10.000000 | 1.300000 | 2.410488259e-01 |
| upper_a | requested | 37 | 19 | 0 | 11.631579 | 10.000000 | 0.800000 | 2.464012874e-01 |
| upper_a | requested | 37 | 19 | 1 | 11.631579 | 10.000000 | 1.300000 | 2.349197029e-01 |
| upper_a | requested | 38 | 19 | 0 | 12.000000 | 10.000000 | 0.800000 | 2.402503032e-01 |
| upper_a | requested | 38 | 19 | 1 | 12.000000 | 10.000000 | 1.300000 | 2.288157892e-01 |
| upper_a | requested | 39 | 19 | 0 | 12.368421 | 10.000000 | 0.800000 | 2.341018766e-01 |
| upper_a | requested | 39 | 19 | 1 | 12.368421 | 10.000000 | 1.300000 | 2.227626413e-01 |
| upper_a | requested | 40 | 19 | 0 | 12.736842 | 10.000000 | 0.800000 | 2.279841644e-01 |
| upper_a | requested | 40 | 19 | 1 | 12.736842 | 10.000000 | 1.300000 | 2.167829297e-01 |
| upper_a | requested | 41 | 19 | 0 | 13.105263 | 10.000000 | 0.800000 | 2.219223252e-01 |
| upper_a | requested | 41 | 19 | 1 | 13.105263 | 10.000000 | 1.300000 | 2.108965312e-01 |
| upper_a | requested | 42 | 19 | 0 | 13.473684 | 10.000000 | 0.800000 | 2.159386077e-01 |
| upper_a | requested | 42 | 19 | 1 | 13.473684 | 10.000000 | 1.300000 | 2.051206256e-01 |
| upper_a | requested | 43 | 19 | 0 | 13.842105 | 10.000000 | 0.800000 | 2.100524420e-01 |
| upper_a | requested | 43 | 19 | 1 | 13.842105 | 10.000000 | 1.300000 | 1.994697832e-01 |
| upper_a | requested | 44 | 19 | 0 | 14.210526 | 10.000000 | 0.800000 | 2.042805231e-01 |
| upper_a | requested | 44 | 19 | 1 | 14.210526 | 10.000000 | 1.300000 | 1.939560178e-01 |
| upper_a | requested | 45 | 19 | 0 | 14.578947 | 10.000000 | 0.800000 | 1.986368647e-01 |
| upper_a | requested | 45 | 19 | 1 | 14.578947 | 10.000000 | 1.300000 | 1.885887524e-01 |
| upper_a | requested | 46 | 19 | 0 | 14.947368 | 10.000000 | 0.800000 | 1.931327727e-01 |
| upper_a | requested | 46 | 19 | 1 | 14.947368 | 10.000000 | 1.300000 | 1.833745893e-01 |
| upper_a | requested | 47 | 19 | 0 | 15.315789 | 10.000000 | 0.800000 | 1.877766394e-01 |
| upper_a | requested | 47 | 19 | 1 | 15.315789 | 10.000000 | 1.300000 | 1.783166628e-01 |
| upper_a | requested | 48 | 19 | 0 | 15.684211 | 10.000000 | 0.800000 | 1.825733514e-01 |
| upper_a | requested | 48 | 19 | 1 | 15.684211 | 10.000000 | 1.300000 | 1.734131184e-01 |
| upper_a | requested | 49 | 19 | 0 | 16.052632 | 10.000000 | 0.800000 | 1.775228849e-01 |
| upper_a | requested | 49 | 19 | 1 | 16.052632 | 10.000000 | 1.300000 | 1.686537742e-01 |
| upper_a | requested | 50 | 19 | 0 | 16.421053 | 10.000000 | 0.800000 | 1.726172078e-01 |
| upper_a | requested | 50 | 19 | 1 | 16.421053 | 10.000000 | 1.300000 | 1.640130249e-01 |
| upper_a | requested | 51 | 19 | 0 | 16.789474 | 10.000000 | 0.800000 | 1.678336658e-01 |
| upper_a | requested | 51 | 19 | 1 | 16.789474 | 10.000000 | 1.300000 | 1.594350065e-01 |
| upper_a | requested | 52 | 19 | 0 | 17.157895 | 10.000000 | 0.800000 | 1.631210600e-01 |
| upper_a | requested | 52 | 19 | 1 | 17.157895 | 10.000000 | 1.300000 | 1.548029105e-01 |
| upper_a | requested | 53 | 19 | 0 | 17.526316 | 10.000000 | 0.800000 | 1.583703903e-01 |
| upper_a | requested | 53 | 19 | 1 | 17.526316 | 10.000000 | 1.300000 | 1.498761853e-01 |
| upper_a | requested | 54 | 19 | 0 | 17.894737 | 10.000000 | 0.800000 | 1.533524901e-01 |
| upper_a | requested | 54 | 19 | 1 | 17.894737 | 10.000000 | 1.300000 | 1.441640461e-01 |
| upper_a | requested | 55 | 19 | 0 | 18.263158 | 10.000000 | 0.800000 | 1.475789427e-01 |
| upper_a | requested | 55 | 19 | 1 | 18.263158 | 10.000000 | 1.300000 | 1.366782822e-01 |
| upper_a | requested | 56 | 19 | 0 | 18.631579 | 10.000000 | 0.800000 | 1.399592878e-01 |
| upper_a | requested | 56 | 19 | 1 | 18.631579 | 10.000000 | 1.300000 | 1.254800996e-01 |
| upper_a | requested | 57 | 19 | 0 | 19.000000 | 10.000000 | 0.800000 | 1.278117117e-01 |
| upper_a | requested | 57 | 19 | 1 | 19.000000 | 10.000000 | 1.300000 | 1.069659496e-01 |
| upper_a | requested | 58 | 19 | 0 | 19.368421 | 10.000000 | 0.800000 | 1.035790954e-01 |
| upper_a | requested | 58 | 19 | 1 | 19.368421 | 10.000000 | 1.300000 | 7.518195558e-02 |
| upper_a | requested | 59 | 19 | 0 | 19.736842 | 10.000000 | 0.800000 | 4.435779913e-02 |
| upper_a | requested | 59 | 19 | 1 | 19.736842 | 10.000000 | 1.300000 | 2.288176893e-02 |

### H1_A39_FINE

| boundary | kind | max | count | share | argmax index | argmax physical | value at argmax | q50/q90/q95/q99 |
|---|---|---|---|---|---|---|---|---|
| upper_a | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 38, 0) | (-2.0, 10.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_a | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 38, 0) | (-2.0, 10.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_a | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_a | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |

Complete offending states (raw > `1e-10*da`; requested > `1e-10`):

No state exceeds the raw or requested threshold.

### H2_A77_FINER

| boundary | kind | max | count | share | argmax index | argmax physical | value at argmax | q50/q90/q95/q99 |
|---|---|---|---|---|---|---|---|---|
| upper_a | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 76, 0) | (-2.0, 10.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_a | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 76, 0) | (-2.0, 10.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_a | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_a | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |

Complete offending states (raw > `1e-10*da`; requested > `1e-10`):

No state exceeds the raw or requested threshold.

### H3_A153_FINEST

| boundary | kind | max | count | share | argmax index | argmax physical | value at argmax | q50/q90/q95/q99 |
|---|---|---|---|---|---|---|---|---|
| upper_a | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 152, 0) | (-2.0, 10.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_a | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 152, 0) | (-2.0, 10.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_a | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_a | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |

Complete offending states (raw > `1e-10*da`; requested > `1e-10`):

No state exceeds the raw or requested threshold.

### H4_B119_A39

| boundary | kind | max | count | share | argmax index | argmax physical | value at argmax | q50/q90/q95/q99 |
|---|---|---|---|---|---|---|---|---|
| upper_a | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 38, 0) | (-2.0, 10.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_a | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 38, 0) | (-2.0, 10.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_a | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_a | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |

Complete offending states (raw > `1e-10*da`; requested > `1e-10`):

No state exceeds the raw or requested threshold.

### H5_B119_A77

| boundary | kind | max | count | share | argmax index | argmax physical | value at argmax | q50/q90/q95/q99 |
|---|---|---|---|---|---|---|---|---|
| upper_a | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 76, 0) | (-2.0, 10.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_a | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 76, 0) | (-2.0, 10.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_a | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_a | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |

Complete offending states (raw > `1e-10*da`; requested > `1e-10`):

No state exceeds the raw or requested threshold.

## Liquid-boundary regression gate (Phase C)

Upper/lower b raw + requested max/count/share on the provisional liquid-safe domain. The preferred interpretation requires the liquid-safe domain to remain non-binding. No silent b enlargement; any material reactivation is recorded.

| variant | upper-b raw | upper-b requested | count | lower-b raw | lower-b requested | count |
|---|---|---|---|---|---|---|
| H0_A20_BASE | 0.000e+00 | 0.000e+00 | 0 | 0.000e+00 | 0.000e+00 | 0 |
| H1_A39_FINE | 9.995e-02 | 2.713e-01 | 3 | 0.000e+00 | 0.000e+00 | 0 |
| H2_A77_FINER | 1.443e-01 | 3.916e-01 | 7 | 0.000e+00 | 0.000e+00 | 0 |
| H3_A153_FINEST | 1.639e-01 | 4.449e-01 | 13 | 0.000e+00 | 0.000e+00 | 0 |
| H4_B119_A39 | 7.264e-02 | 3.943e-01 | 3 | 0.000e+00 | 0.000e+00 | 0 |
| H5_B119_A77 | 1.215e-01 | 6.598e-01 | 6 | 0.000e+00 | 0.000e+00 | 0 |

## Illiquid a-resolution trend (Phase D: H0 -> H1 -> H2 -> H3)

| variant | raw upper-a max | requested upper-a max | raw count | requested count | raw share | requested share | argmax physical (b,z) |
|---|---|---|---|---|---|---|---|
| H0_A20_BASE | 1.629e-01 | 3.095e-01 | 108 | 108 | 9.000e-01 | 9.000e-01 | (6.105263157894736, 0.8) |
| H1_A39_FINE | 0.000e+00 | 0.000e+00 | 0 | 0 | 0.000e+00 | 0.000e+00 | (-2.0, 0.8) |
| H2_A77_FINER | 0.000e+00 | 0.000e+00 | 0 | 0 | 0.000e+00 | 0.000e+00 | (-2.0, 0.8) |
| H3_A153_FINEST | 0.000e+00 | 0.000e+00 | 0 | 0 | 0.000e+00 | 0.000e+00 | (-2.0, 0.8) |

- adjacent raw attenuation ratios (H0/H1, H1/H2, H2/H3): ['inf', None, None] (`inf` = nonzero-to-zero attenuation)
- adjacent requested attenuation ratios: ['inf', None, None]
- raw ratios relative to H0: [0.0, 0.0, 0.0]
- requested ratios relative to H0: [0.0, 0.0, 0.0]
- strictly decreasing raw upper-a max over H0->H3: False
- strictly decreasing requested upper-a max over H0->H3: False
- plateau flag: False
- first variant with requested upper-a <= 1e-10: H1_A39_FINE

This is a policy-only trend; it does not infer stationary-tail existence or non-existence.

## Exact aligned-node policy stability (Phase E)

Five required pairs: a-resolution H0/H1, H1/H2, H2/H3 (identical b grid, every-second a alignment) and b cross-checks H1/H4, H2/H5 (identical a grid, every-second b alignment). Coarse-grid shared-interior mask excludes the top two coarse layers in both asset dimensions, all z. `rel_diff = max_abs / max(1, max|coarse|)` is scale-aware.

### H0_vs_H1 (a-resolution)

| field | max_abs_diff | rel_diff | label mismatch |
|---|---|---|---|
| value | 1.292e-01 | 1.890e-03 | — |
| consumption | 1.126e-02 | 7.617e-03 | — |
| labor | 4.094e-03 | 3.672e-03 | — |
| transfer | 1.177e-01 | 1.177e-01 | — |
| mu_a | 1.177e-01 | 1.177e-01 | — |
| mu_b | 9.772e-02 | 9.772e-02 | — |
| liquid_label | — | — | 42 |
| transfer_label | — | — | 115 |

### H1_vs_H2 (a-resolution)

| field | max_abs_diff | rel_diff | label mismatch |
|---|---|---|---|
| value | 1.009e-01 | 1.477e-03 | — |
| consumption | 3.984e-03 | 2.691e-03 | — |
| labor | 1.462e-03 | 1.308e-03 | — |
| transfer | 5.005e-02 | 4.865e-02 | — |
| mu_a | 5.005e-02 | 5.005e-02 | — |
| mu_b | 3.849e-02 | 3.849e-02 | — |
| liquid_label | — | — | 33 |
| transfer_label | — | — | 34 |

### H2_vs_H3 (a-resolution)

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

### H1_vs_H4 (b-resolution)

| field | max_abs_diff | rel_diff | label mismatch |
|---|---|---|---|
| value | 2.617e-01 | 3.828e-03 | — |
| consumption | 4.037e-02 | 2.727e-02 | — |
| labor | 1.711e-02 | 1.531e-02 | — |
| transfer | 8.031e-02 | 7.807e-02 | — |
| mu_a | 8.031e-02 | 8.031e-02 | — |
| mu_b | 1.127e-01 | 1.127e-01 | — |
| liquid_label | — | — | 83 |
| transfer_label | — | — | 67 |

### H2_vs_H5 (b-resolution)

| field | max_abs_diff | rel_diff | label mismatch |
|---|---|---|---|
| value | 2.653e-01 | 3.881e-03 | — |
| consumption | 4.278e-02 | 2.883e-02 | — |
| labor | 1.789e-02 | 1.598e-02 | — |
| transfer | 8.256e-02 | 7.492e-02 | — |
| mu_a | 8.256e-02 | 8.256e-02 | — |
| mu_b | 1.165e-01 | 1.165e-01 | — |
| liquid_label | — | — | 155 |
| transfer_label | — | — | 171 |

## Joint HJB upper-boundary policy compatibility (Phase F)

Per-variant prerequisite marker only (no stationary solve): `requested_upper_b <= 1e-10 AND requested_upper_a <= 1e-10`.

- H0_A20_BASE: JOINT_HJB_BOUNDARY_POLICY_NOT_COMPATIBLE
- H1_A39_FINE: JOINT_HJB_BOUNDARY_POLICY_NOT_COMPATIBLE
- H2_A77_FINER: JOINT_HJB_BOUNDARY_POLICY_NOT_COMPATIBLE
- H3_A153_FINEST: JOINT_HJB_BOUNDARY_POLICY_NOT_COMPATIBLE
- H4_B119_A39: JOINT_HJB_BOUNDARY_POLICY_NOT_COMPATIBLE
- H5_B119_A77: JOINT_HJB_BOUNDARY_POLICY_NOT_COMPATIBLE

Stationary KFE / nullspace / pin / density / tail mass / stationary flux / `C,L,A,B` are `NOT_AUTHORIZED__DLH_5H_POLICY_ONLY_ILLIQUID_RESOLUTION_DIAGNOSTIC` and were not executed.

## Reproducibility

- randomness: `NOT_APPLICABLE`; repeat pass: `True`; terminal run1/run2: `BLOCKED_DLH_5H_LIQUID_BOUNDARY_REACTIVATION_ON_ILLIQUID_RESOLUTION_VARIANTS` / `BLOCKED_DLH_5H_LIQUID_BOUNDARY_REACTIVATION_ON_ILLIQUID_RESOLUTION_VARIANTS`; annotations run1/run2: ['DLH_5H_POLICY_RESOLUTION_SENSITIVITY_REMAINS_MATERIAL__NUMERICAL_REVIEW_REQUIRED'] / ['DLH_5H_POLICY_RESOLUTION_SENSITIVITY_REMAINS_MATERIAL__NUMERICAL_REVIEW_REQUIRED'].
- H0_A20_BASE: structural identical True, max numeric diff 0.000e+00, aligned non-finite 0, mismatched 0, pass True.
- H1_A39_FINE: structural identical True, max numeric diff 0.000e+00, aligned non-finite 0, mismatched 0, pass True.
- H2_A77_FINER: structural identical True, max numeric diff 0.000e+00, aligned non-finite 0, mismatched 0, pass True.
- H3_A153_FINEST: structural identical True, max numeric diff 0.000e+00, aligned non-finite 0, mismatched 0, pass True.
- H4_B119_A39: structural identical True, max numeric diff 0.000e+00, aligned non-finite 0, mismatched 0, pass True.
- H5_B119_A77: structural identical True, max numeric diff 0.000e+00, aligned non-finite 0, mismatched 0, pass True.

## Artifact integrity

- accepted MATLAB-faithful oracle blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`, SHA-256 `1795718C469FC3B427CAB8E3D5957C133BEAD6EACC9EF0A25A3EDB7211D1A024` re-verified read-only (unchanged from the accepted Issue #23/#26 state).
- no existing tracked file modified; dedicated branch `dsh/issue-34-dlh-5h-illiquid-resolution-2026-09-01`; allowlist-only additions (3 artifacts + 8 evidence files).

DLH-5H implements NO repair and NO stationary acceptance: accepted HJB/KFE/regional source immutable; physical a-domain/a_max/taper/economics/tolerances/initialization frozen; no clipping; no D1-D3; no regional or multi-province GE; no learned network; no nominal HANK.