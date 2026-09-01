# DLH-5F — Upper-Domain Adequacy and Stationary-Tail Diagnostic (Issue #29)

Bounded diagnostic on the frozen two-asset household over the exact six pre-frozen numerical domains. The accepted MATLAB-faithful HJB source is immutable and reused read-only; the accepted DLH-5E diagnostic helper is read-only authority where applicable.

Overall terminal classification: `DLH_5F_UPPER_DOMAIN_DIAGNOSTIC_COMPLETE__NO_PREFROZEN_DOMAIN_REACHES_SAME_PROCESS_STATIONARY_TAIL__SCIENTIFIC_REVIEW_REQUIRED`

Secondary scientific annotations: `LIQUID_ILLIQUID_UPPER_DOMAIN_BEHAVIOR_DIVERGES__SEPARATE_SCIENTIFIC_TREATMENT_REQUIRED`

Frozen economics/prices: `wbar=1.0`, `r_a=0.03`; all non-grid objects exactly the accepted DLH-5B/DLH-5E canonical fixture (`configs/dlh_5b_two_region_symmetric_anchor.toml`, region_index=0).

## Variant status (Phase A)

| variant | b pts | b domain | b max | db | a pts | a domain | a max | da | HJB conv | iters | stat | gate | max requested outward | Phase E | variant terminal |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| V0_BASE | 20 | [-2.0,5.0] | 5.0 | 0.368421052631579 | 20 | [0.0,10.0] | 10.0 | 0.5263157894736842 | True | 11 | 1.674e-08 | VIOLATION | 3.537e-01 | False | NOT_REACHED__HJB_KFE_SAME_PROCESS_BOUNDARY_GATE_FAILED |
| V1_A_WIDE | 20 | [-2.0,5.0] | 5.0 | 0.368421052631579 | 40 | [0.0,20.526315789473685] | 20.526315789473685 | 0.5263157894736842 | True | 11 | 1.487e-08 | VIOLATION | 1.238e+00 | False | NOT_REACHED__HJB_KFE_SAME_PROCESS_BOUNDARY_GATE_FAILED |
| V2_B_WIDE | 40 | [-2.0,12.368421052631579] | 12.368421052631579 | 0.368421052631579 | 20 | [0.0,10.0] | 10.0 | 0.5263157894736842 | True | 11 | 1.028e-08 | VIOLATION | 3.095e-01 | False | NOT_REACHED__HJB_KFE_SAME_PROCESS_BOUNDARY_GATE_FAILED |
| V3_AB_MID | 30 | [-2.0,8.68421052631579] | 8.68421052631579 | 0.368421052631579 | 30 | [0.0,15.263157894736842] | 15.263157894736842 | 0.5263157894736842 | True | 12 | 4.969e-09 | VIOLATION | 3.375e-01 | False | NOT_REACHED__HJB_KFE_SAME_PROCESS_BOUNDARY_GATE_FAILED |
| V4_AB_WIDE | 40 | [-2.0,12.368421052631579] | 12.368421052631579 | 0.368421052631579 | 40 | [0.0,20.526315789473685] | 20.526315789473685 | 0.5263157894736842 | True | 12 | 9.987e-09 | VIOLATION | 4.799e-01 | False | NOT_REACHED__HJB_KFE_SAME_PROCESS_BOUNDARY_GATE_FAILED |
| V5_BASE_FINE | 39 | [-2.0,5.0] | 5.0 | 0.18421052631578938 | 39 | [0.0,10.0] | 10.0 | 0.2631578947368421 | True | 11 | 1.025e-08 | VIOLATION | 1.272e+00 | False | NOT_REACHED__HJB_KFE_SAME_PROCESS_BOUNDARY_GATE_FAILED |

## Boundary requested-rate diagnostics (Phase B)

Requested directional rates are reconstructed from post-convergence `mu_b`/`mu_a` as `max(-mu_b,0)/db`, `max(mu_b,0)/db`, `max(-mu_a,0)/da`, `max(mu_a,0)/da` and are NEVER clipped or mutated. Coordinates are exact `(b_index,a_index,z_index)` plus physical `(b,a,z)` recovered with C-order `np.unravel_index` on the actual 2-D boundary slice shape.

### V0_BASE

| boundary | direction | max | count>1e-10 | share | argmax index | argmax physical | requested at max | q50/q90/q95/q99 |
|---|---|---|---|---|---|---|---|---|
| lower_b | b_backward | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_b | b_forward | 3.537e-01 | 3 | 7.500e-02 | (19, 19, 1) | (5.0, 10.0, 1.3) | 3.537e-01 | 0.27186872359611547/0.33737190793689/0.34555980597948677/0.35211012441356426 |
| lower_a | a_backward | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_a | a_forward | 2.641e-01 | 28 | 7.000e-01 | (14, 19, 1) | (3.1578947368421053, 10.0, 1.3) | 2.641e-01 | 0.20265880202205963/0.25652049957419243/0.2615557792231614/0.26389746757596977 |

Complete offending states (requested outward rate > 1e-10):

| boundary | direction | b_index | a_index | z_index | b | a | z | requested outward rate |
|---|---|---|---|---|---|---|---|---|
| upper_b | b_forward | 19 | 17 | 1 | 5.000000 | 8.947368 | 1.300000 | 1.157606987e-01 |
| upper_b | b_forward | 19 | 18 | 1 | 5.000000 | 9.473684 | 1.300000 | 2.718687236e-01 |
| upper_b | b_forward | 19 | 19 | 1 | 5.000000 | 10.000000 | 1.300000 | 3.537477040e-01 |
| upper_a | a_forward | 5 | 19 | 1 | -0.157895 | 10.000000 | 1.300000 | 3.175106194e-03 |
| upper_a | a_forward | 6 | 19 | 1 | 0.210526 | 10.000000 | 1.300000 | 1.034225218e-01 |
| upper_a | a_forward | 7 | 19 | 0 | 0.578947 | 10.000000 | 0.800000 | 2.940147623e-02 |
| upper_a | a_forward | 7 | 19 | 1 | 0.578947 | 10.000000 | 1.300000 | 1.460640158e-01 |
| upper_a | a_forward | 8 | 19 | 0 | 0.947368 | 10.000000 | 0.800000 | 9.009153816e-02 |
| upper_a | a_forward | 8 | 19 | 1 | 0.947368 | 10.000000 | 1.300000 | 1.763017040e-01 |
| upper_a | a_forward | 9 | 19 | 0 | 1.315789 | 10.000000 | 0.800000 | 1.367105809e-01 |
| upper_a | a_forward | 9 | 19 | 1 | 1.315789 | 10.000000 | 1.300000 | 2.031466324e-01 |
| upper_a | a_forward | 10 | 19 | 0 | 1.684211 | 10.000000 | 0.800000 | 1.732706282e-01 |
| upper_a | a_forward | 10 | 19 | 1 | 1.684211 | 10.000000 | 1.300000 | 2.253730726e-01 |
| upper_a | a_forward | 11 | 19 | 0 | 2.052632 | 10.000000 | 0.800000 | 2.021709716e-01 |
| upper_a | a_forward | 11 | 19 | 1 | 2.052632 | 10.000000 | 1.300000 | 2.429588552e-01 |
| upper_a | a_forward | 12 | 19 | 0 | 2.421053 | 10.000000 | 0.800000 | 2.248302109e-01 |
| upper_a | a_forward | 12 | 19 | 1 | 2.421053 | 10.000000 | 1.300000 | 2.558509867e-01 |
| upper_a | a_forward | 13 | 19 | 0 | 2.789474 | 10.000000 | 0.800000 | 2.419158557e-01 |
| upper_a | a_forward | 13 | 19 | 1 | 2.789474 | 10.000000 | 1.300000 | 2.634259008e-01 |
| upper_a | a_forward | 14 | 19 | 0 | 3.157895 | 10.000000 | 0.800000 | 2.533455404e-01 |
| upper_a | a_forward | 14 | 19 | 1 | 3.157895 | 10.000000 | 1.300000 | 2.640718827e-01 |
| upper_a | a_forward | 15 | 19 | 0 | 3.526316 | 10.000000 | 0.800000 | 2.580826964e-01 |
| upper_a | a_forward | 15 | 19 | 1 | 3.526316 | 10.000000 | 1.300000 | 2.546689128e-01 |
| upper_a | a_forward | 16 | 19 | 0 | 3.894737 | 10.000000 | 0.800000 | 2.537143916e-01 |
| upper_a | a_forward | 16 | 19 | 1 | 3.894737 | 10.000000 | 1.300000 | 2.305539903e-01 |
| upper_a | a_forward | 17 | 19 | 0 | 4.263158 | 10.000000 | 0.800000 | 2.352871698e-01 |
| upper_a | a_forward | 17 | 19 | 1 | 4.263158 | 10.000000 | 1.300000 | 1.867536785e-01 |
| upper_a | a_forward | 18 | 19 | 0 | 4.631579 | 10.000000 | 0.800000 | 1.907037702e-01 |
| upper_a | a_forward | 18 | 19 | 1 | 4.631579 | 10.000000 | 1.300000 | 1.206860239e-01 |
| upper_a | a_forward | 19 | 19 | 0 | 5.000000 | 10.000000 | 0.800000 | 8.783338931e-02 |
| upper_a | a_forward | 19 | 19 | 1 | 5.000000 | 10.000000 | 1.300000 | 3.635781425e-02 |

### V1_A_WIDE

| boundary | direction | max | count>1e-10 | share | argmax index | argmax physical | requested at max | q50/q90/q95/q99 |
|---|---|---|---|---|---|---|---|---|
| lower_b | b_backward | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_b | b_forward | 1.238e+00 | 6 | 7.500e-02 | (19, 39, 1) | (5.0, 20.526315789473685, 1.3) | 1.238e+00 | 0.7748616809049792/1.1728850611885822/1.2052095284144713/1.2310691021951825 |
| lower_a | a_backward | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_a | a_forward | 0.000e+00 | 0 | 0.000e+00 | (0, 39, 0) | (-2.0, 20.526315789473685, 0.8) | 0.000e+00 | NOT_APPLICABLE |

Complete offending states (requested outward rate > 1e-10):

| boundary | direction | b_index | a_index | z_index | b | a | z | requested outward rate |
|---|---|---|---|---|---|---|---|---|
| upper_b | b_forward | 19 | 34 | 1 | 5.000000 | 17.894737 | 1.300000 | 1.724097907e-01 |
| upper_b | b_forward | 19 | 35 | 1 | 5.000000 | 18.421053 | 1.300000 | 4.096713022e-01 |
| upper_b | b_forward | 19 | 36 | 1 | 5.000000 | 18.947368 | 1.300000 | 6.543476500e-01 |
| upper_b | b_forward | 19 | 37 | 1 | 5.000000 | 19.473684 | 1.300000 | 8.953757118e-01 |
| upper_b | b_forward | 19 | 38 | 1 | 5.000000 | 20.000000 | 1.300000 | 1.108236127e+00 |
| upper_b | b_forward | 19 | 39 | 1 | 5.000000 | 20.526316 | 1.300000 | 1.237533996e+00 |

### V2_B_WIDE

| boundary | direction | max | count>1e-10 | share | argmax index | argmax physical | requested at max | q50/q90/q95/q99 |
|---|---|---|---|---|---|---|---|---|
| lower_b | b_backward | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_b | b_forward | 1.020e-02 | 1 | 2.500e-02 | (39, 19, 1) | (12.368421052631579, 10.0, 1.3) | 1.020e-02 | 0.010203356062305411/0.010203356062305411/0.010203356062305411/0.010203356062305411 |
| lower_a | a_backward | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_a | a_forward | 3.095e-01 | 68 | 8.500e-01 | (22, 19, 0) | (6.105263157894736, 10.0, 0.8) | 3.095e-01 | 0.27570549025433355/0.30765703479367806/0.30886034443603066/0.30922430554204733 |

Complete offending states (requested outward rate > 1e-10):

| boundary | direction | b_index | a_index | z_index | b | a | z | requested outward rate |
|---|---|---|---|---|---|---|---|---|
| upper_b | b_forward | 39 | 19 | 1 | 12.368421 | 10.000000 | 1.300000 | 1.020335606e-02 |
| upper_a | a_forward | 5 | 19 | 1 | -0.157895 | 10.000000 | 1.300000 | 3.340559455e-03 |
| upper_a | a_forward | 6 | 19 | 1 | 0.210526 | 10.000000 | 1.300000 | 1.037185052e-01 |
| upper_a | a_forward | 7 | 19 | 0 | 0.578947 | 10.000000 | 0.800000 | 2.961341708e-02 |
| upper_a | a_forward | 7 | 19 | 1 | 0.578947 | 10.000000 | 1.300000 | 1.464849560e-01 |
| upper_a | a_forward | 8 | 19 | 0 | 0.947368 | 10.000000 | 0.800000 | 9.044960205e-02 |
| upper_a | a_forward | 8 | 19 | 1 | 0.947368 | 10.000000 | 1.300000 | 1.770230905e-01 |
| upper_a | a_forward | 9 | 19 | 0 | 1.315789 | 10.000000 | 0.800000 | 1.373124883e-01 |
| upper_a | a_forward | 9 | 19 | 1 | 1.315789 | 10.000000 | 1.300000 | 2.043612125e-01 |
| upper_a | a_forward | 10 | 19 | 0 | 1.684211 | 10.000000 | 0.800000 | 1.742857243e-01 |
| upper_a | a_forward | 10 | 19 | 1 | 1.684211 | 10.000000 | 1.300000 | 2.274316378e-01 |
| upper_a | a_forward | 11 | 19 | 0 | 2.052632 | 10.000000 | 0.800000 | 2.039039604e-01 |
| upper_a | a_forward | 11 | 19 | 1 | 2.052632 | 10.000000 | 1.300000 | 2.465141984e-01 |
| upper_a | a_forward | 12 | 19 | 0 | 2.421053 | 10.000000 | 0.800000 | 2.278442047e-01 |
| upper_a | a_forward | 12 | 19 | 1 | 2.421053 | 10.000000 | 1.300000 | 2.621391198e-01 |
| upper_a | a_forward | 13 | 19 | 0 | 2.789474 | 10.000000 | 0.800000 | 2.472667309e-01 |
| upper_a | a_forward | 13 | 19 | 1 | 2.789474 | 10.000000 | 1.300000 | 2.747991012e-01 |
| upper_a | a_forward | 14 | 19 | 0 | 3.157895 | 10.000000 | 0.800000 | 2.630121070e-01 |
| upper_a | a_forward | 14 | 19 | 1 | 3.157895 | 10.000000 | 1.300000 | 2.849422674e-01 |
| upper_a | a_forward | 15 | 19 | 0 | 3.526316 | 10.000000 | 0.800000 | 2.757081090e-01 |
| upper_a | a_forward | 15 | 19 | 1 | 3.526316 | 10.000000 | 1.300000 | 2.929287953e-01 |
| upper_a | a_forward | 16 | 19 | 0 | 3.894737 | 10.000000 | 0.800000 | 2.858361362e-01 |
| upper_a | a_forward | 16 | 19 | 1 | 3.894737 | 10.000000 | 1.300000 | 2.990498670e-01 |
| upper_a | a_forward | 17 | 19 | 0 | 4.263158 | 10.000000 | 0.800000 | 2.937736161e-01 |
| upper_a | a_forward | 17 | 19 | 1 | 4.263158 | 10.000000 | 1.300000 | 3.035440044e-01 |
| upper_a | a_forward | 18 | 19 | 0 | 4.631579 | 10.000000 | 0.800000 | 2.998223714e-01 |
| upper_a | a_forward | 18 | 19 | 1 | 4.631579 | 10.000000 | 1.300000 | 3.066095975e-01 |
| upper_a | a_forward | 19 | 19 | 0 | 5.000000 | 10.000000 | 0.800000 | 3.042282429e-01 |
| upper_a | a_forward | 19 | 19 | 1 | 5.000000 | 10.000000 | 1.300000 | 3.084142656e-01 |
| upper_a | a_forward | 20 | 19 | 0 | 5.368421 | 10.000000 | 0.800000 | 3.071949835e-01 |
| upper_a | a_forward | 20 | 19 | 1 | 5.368421 | 10.000000 | 1.300000 | 3.091018006e-01 |
| upper_a | a_forward | 21 | 19 | 0 | 5.736842 | 10.000000 | 0.800000 | 3.088942713e-01 |
| upper_a | a_forward | 21 | 19 | 1 | 5.736842 | 10.000000 | 1.300000 | 3.087973373e-01 |
| upper_a | a_forward | 22 | 19 | 0 | 6.105263 | 10.000000 | 0.800000 | 3.094730277e-01 |
| upper_a | a_forward | 22 | 19 | 1 | 6.105263 | 10.000000 | 1.300000 | 3.076112249e-01 |
| upper_a | a_forward | 23 | 19 | 0 | 6.473684 | 10.000000 | 0.800000 | 3.090588270e-01 |
| upper_a | a_forward | 23 | 19 | 1 | 6.473684 | 10.000000 | 1.300000 | 3.056419347e-01 |
| upper_a | a_forward | 24 | 19 | 0 | 6.842105 | 10.000000 | 0.800000 | 3.077639246e-01 |
| upper_a | a_forward | 24 | 19 | 1 | 6.842105 | 10.000000 | 1.300000 | 3.029782303e-01 |
| upper_a | a_forward | 25 | 19 | 0 | 7.210526 | 10.000000 | 0.800000 | 3.056882553e-01 |
| upper_a | a_forward | 25 | 19 | 1 | 7.210526 | 10.000000 | 1.300000 | 2.997007346e-01 |
| upper_a | a_forward | 26 | 19 | 0 | 7.578947 | 10.000000 | 0.800000 | 3.029216260e-01 |
| upper_a | a_forward | 26 | 19 | 1 | 7.578947 | 10.000000 | 1.300000 | 2.958829316e-01 |
| upper_a | a_forward | 27 | 19 | 0 | 7.947368 | 10.000000 | 0.800000 | 2.995452007e-01 |
| upper_a | a_forward | 27 | 19 | 1 | 7.947368 | 10.000000 | 1.300000 | 2.915914887e-01 |
| upper_a | a_forward | 28 | 19 | 0 | 8.315789 | 10.000000 | 0.800000 | 2.956322187e-01 |
| upper_a | a_forward | 28 | 19 | 1 | 8.315789 | 10.000000 | 1.300000 | 2.868854962e-01 |
| upper_a | a_forward | 29 | 19 | 0 | 8.684211 | 10.000000 | 0.800000 | 2.912476007e-01 |
| upper_a | a_forward | 29 | 19 | 1 | 8.684211 | 10.000000 | 1.300000 | 2.818136042e-01 |
| upper_a | a_forward | 30 | 19 | 0 | 9.052632 | 10.000000 | 0.800000 | 2.864455178e-01 |
| upper_a | a_forward | 30 | 19 | 1 | 9.052632 | 10.000000 | 1.300000 | 2.764066887e-01 |
| upper_a | a_forward | 31 | 19 | 0 | 9.421053 | 10.000000 | 0.800000 | 2.812627406e-01 |
| upper_a | a_forward | 31 | 19 | 1 | 9.421053 | 10.000000 | 1.300000 | 2.706607331e-01 |
| upper_a | a_forward | 32 | 19 | 0 | 9.789474 | 10.000000 | 0.800000 | 2.757028715e-01 |
| upper_a | a_forward | 32 | 19 | 1 | 9.789474 | 10.000000 | 1.300000 | 2.644982828e-01 |
| upper_a | a_forward | 33 | 19 | 0 | 10.157895 | 10.000000 | 0.800000 | 2.697006825e-01 |
| upper_a | a_forward | 33 | 19 | 1 | 10.157895 | 10.000000 | 1.300000 | 2.576836919e-01 |
| upper_a | a_forward | 34 | 19 | 0 | 10.526316 | 10.000000 | 0.800000 | 2.630428918e-01 |
| upper_a | a_forward | 34 | 19 | 1 | 10.526316 | 10.000000 | 1.300000 | 2.496421343e-01 |
| upper_a | a_forward | 35 | 19 | 0 | 10.894737 | 10.000000 | 0.800000 | 2.551905443e-01 |
| upper_a | a_forward | 35 | 19 | 1 | 10.894737 | 10.000000 | 1.300000 | 2.390924420e-01 |
| upper_a | a_forward | 36 | 19 | 0 | 11.263158 | 10.000000 | 0.800000 | 2.448504556e-01 |
| upper_a | a_forward | 36 | 19 | 1 | 11.263158 | 10.000000 | 1.300000 | 2.233775713e-01 |
| upper_a | a_forward | 37 | 19 | 0 | 11.631579 | 10.000000 | 0.800000 | 2.287287194e-01 |
| upper_a | a_forward | 37 | 19 | 1 | 11.631579 | 10.000000 | 1.300000 | 1.975216189e-01 |
| upper_a | a_forward | 38 | 19 | 0 | 12.000000 | 10.000000 | 0.800000 | 1.970610811e-01 |
| upper_a | a_forward | 38 | 19 | 1 | 12.000000 | 10.000000 | 1.300000 | 1.538275023e-01 |
| upper_a | a_forward | 39 | 19 | 0 | 12.368421 | 10.000000 | 0.800000 | 1.186582564e-01 |
| upper_a | a_forward | 39 | 19 | 1 | 12.368421 | 10.000000 | 1.300000 | 8.503454305e-02 |

### V3_AB_MID

| boundary | direction | max | count>1e-10 | share | argmax index | argmax physical | requested at max | q50/q90/q95/q99 |
|---|---|---|---|---|---|---|---|---|
| lower_b | b_backward | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_b | b_forward | 2.779e-01 | 3 | 5.000e-02 | (29, 29, 1) | (8.68421052631579, 15.263157894736842, 1.3) | 2.779e-01 | 0.22929673647407903/0.26818927925974667/0.27305084710795513/0.2769401013865219 |
| lower_a | a_backward | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_a | a_forward | 3.375e-01 | 44 | 7.333e-01 | (20, 29, 1) | (5.368421052631579, 15.263157894736842, 1.3) | 3.375e-01 | 0.284990348568805/0.3350192198089379/0.3366384870580093/0.337384060835284 |

Complete offending states (requested outward rate > 1e-10):

| boundary | direction | b_index | a_index | z_index | b | a | z | requested outward rate |
|---|---|---|---|---|---|---|---|---|
| upper_b | b_forward | 29 | 27 | 1 | 8.684211 | 14.210526 | 1.300000 | 8.161843586e-02 |
| upper_b | b_forward | 29 | 28 | 1 | 8.684211 | 14.736842 | 1.300000 | 2.292967365e-01 |
| upper_b | b_forward | 29 | 29 | 1 | 8.684211 | 15.263158 | 1.300000 | 2.779124150e-01 |
| upper_a | a_forward | 7 | 29 | 1 | 0.578947 | 15.263158 | 1.300000 | 6.111379649e-02 |
| upper_a | a_forward | 8 | 29 | 0 | 0.947368 | 15.263158 | 0.800000 | 1.060671461e-04 |
| upper_a | a_forward | 8 | 29 | 1 | 0.947368 | 15.263158 | 1.300000 | 1.171081840e-01 |
| upper_a | a_forward | 9 | 29 | 0 | 1.315789 | 15.263158 | 0.800000 | 6.734632547e-02 |
| upper_a | a_forward | 9 | 29 | 1 | 1.315789 | 15.263158 | 1.300000 | 1.613614411e-01 |
| upper_a | a_forward | 10 | 29 | 0 | 1.684211 | 15.263158 | 0.800000 | 1.210906526e-01 |
| upper_a | a_forward | 10 | 29 | 1 | 1.684211 | 15.263158 | 1.300000 | 1.973970197e-01 |
| upper_a | a_forward | 11 | 29 | 0 | 2.052632 | 15.263158 | 0.800000 | 1.647263404e-01 |
| upper_a | a_forward | 11 | 29 | 1 | 2.052632 | 15.263158 | 1.300000 | 2.271449814e-01 |
| upper_a | a_forward | 12 | 29 | 0 | 2.421053 | 15.263158 | 0.800000 | 2.005460477e-01 |
| upper_a | a_forward | 12 | 29 | 1 | 2.421053 | 15.263158 | 1.300000 | 2.518495274e-01 |
| upper_a | a_forward | 13 | 29 | 0 | 2.789474 | 15.263158 | 0.800000 | 2.301553338e-01 |
| upper_a | a_forward | 13 | 29 | 1 | 2.789474 | 15.263158 | 1.300000 | 2.723866134e-01 |
| upper_a | a_forward | 14 | 29 | 0 | 3.157895 | 15.263158 | 0.800000 | 2.547120385e-01 |
| upper_a | a_forward | 14 | 29 | 1 | 3.157895 | 15.263158 | 1.300000 | 2.894032024e-01 |
| upper_a | a_forward | 15 | 29 | 0 | 3.526316 | 15.263158 | 0.800000 | 2.750715906e-01 |
| upper_a | a_forward | 15 | 29 | 1 | 3.526316 | 15.263158 | 1.300000 | 3.033893568e-01 |
| upper_a | a_forward | 16 | 29 | 0 | 3.894737 | 15.263158 | 0.800000 | 2.918773970e-01 |
| upper_a | a_forward | 16 | 29 | 1 | 3.894737 | 15.263158 | 1.300000 | 3.147183650e-01 |
| upper_a | a_forward | 17 | 29 | 0 | 4.263158 | 15.263158 | 0.800000 | 3.056171314e-01 |
| upper_a | a_forward | 17 | 29 | 1 | 4.263158 | 15.263158 | 1.300000 | 3.236669909e-01 |
| upper_a | a_forward | 18 | 29 | 0 | 4.631579 | 15.263158 | 0.800000 | 3.166554774e-01 |
| upper_a | a_forward | 18 | 29 | 1 | 4.631579 | 15.263158 | 1.300000 | 3.304184639e-01 |
| upper_a | a_forward | 19 | 29 | 0 | 5.000000 | 15.263158 | 0.800000 | 3.252472106e-01 |
| upper_a | a_forward | 19 | 29 | 1 | 5.000000 | 15.263158 | 1.300000 | 3.350443598e-01 |
| upper_a | a_forward | 20 | 29 | 0 | 5.368421 | 15.263158 | 0.800000 | 3.315288315e-01 |
| upper_a | a_forward | 20 | 29 | 1 | 5.368421 | 15.263158 | 1.300000 | 3.374541508e-01 |
| upper_a | a_forward | 21 | 29 | 0 | 5.736842 | 15.263158 | 0.800000 | 3.354806075e-01 |
| upper_a | a_forward | 21 | 29 | 1 | 5.736842 | 15.263158 | 1.300000 | 3.372911509e-01 |
| upper_a | a_forward | 22 | 29 | 0 | 6.105263 | 15.263158 | 0.800000 | 3.368428187e-01 |
| upper_a | a_forward | 22 | 29 | 1 | 6.105263 | 15.263158 | 1.300000 | 3.337418054e-01 |
| upper_a | a_forward | 23 | 29 | 0 | 6.473684 | 15.263158 | 0.800000 | 3.349605599e-01 |
| upper_a | a_forward | 23 | 29 | 1 | 6.473684 | 15.263158 | 1.300000 | 3.252223872e-01 |
| upper_a | a_forward | 24 | 29 | 0 | 6.842105 | 15.263158 | 0.800000 | 3.285224184e-01 |
| upper_a | a_forward | 24 | 29 | 1 | 6.842105 | 15.263158 | 1.300000 | 3.089505435e-01 |
| upper_a | a_forward | 25 | 29 | 0 | 7.210526 | 15.263158 | 0.800000 | 3.151433847e-01 |
| upper_a | a_forward | 25 | 29 | 1 | 7.210526 | 15.263158 | 1.300000 | 2.805774948e-01 |
| upper_a | a_forward | 26 | 29 | 0 | 7.578947 | 15.263158 | 0.800000 | 2.906621552e-01 |
| upper_a | a_forward | 26 | 29 | 1 | 7.578947 | 15.263158 | 1.300000 | 2.343960956e-01 |
| upper_a | a_forward | 27 | 29 | 0 | 7.947368 | 15.263158 | 0.800000 | 2.477055470e-01 |
| upper_a | a_forward | 27 | 29 | 1 | 7.947368 | 15.263158 | 1.300000 | 1.648734290e-01 |
| upper_a | a_forward | 28 | 29 | 0 | 8.315789 | 15.263158 | 0.800000 | 1.725977564e-01 |
| upper_a | a_forward | 28 | 29 | 1 | 8.315789 | 15.263158 | 1.300000 | 6.975014594e-02 |
| upper_a | a_forward | 29 | 29 | 0 | 8.684211 | 15.263158 | 0.800000 | 4.134907367e-02 |

### V4_AB_WIDE

| boundary | direction | max | count>1e-10 | share | argmax index | argmax physical | requested at max | q50/q90/q95/q99 |
|---|---|---|---|---|---|---|---|---|
| lower_b | b_backward | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_b | b_forward | 4.799e-01 | 4 | 5.000e-02 | (39, 39, 1) | (12.368421052631579, 20.526315789473685, 1.3) | 4.799e-01 | 0.32395269406033483/0.4587853114738466/0.46932483087829013/0.47775644640184506 |
| lower_a | a_backward | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_a | a_forward | 3.335e-01 | 57 | 7.125e-01 | (24, 39, 0) | (6.842105263157894, 20.526315789473685, 0.8) | 3.335e-01 | 0.28353184419199645/0.33079759392221303/0.33263509078687153/0.33312141029652403 |

Complete offending states (requested outward rate > 1e-10):

| boundary | direction | b_index | a_index | z_index | b | a | z | requested outward rate |
|---|---|---|---|---|---|---|---|---|
| upper_b | b_forward | 39 | 36 | 1 | 12.368421 | 18.947368 | 1.300000 | 2.507635271e-02 |
| upper_b | b_forward | 39 | 37 | 1 | 12.368421 | 19.473684 | 1.300000 | 2.383045005e-01 |
| upper_b | b_forward | 39 | 38 | 1 | 12.368421 | 20.000000 | 1.300000 | 4.096008876e-01 |
| upper_b | b_forward | 39 | 39 | 1 | 12.368421 | 20.526316 | 1.300000 | 4.798643503e-01 |
| upper_a | a_forward | 8 | 39 | 1 | 0.947368 | 20.526316 | 1.300000 | 3.946620262e-02 |
| upper_a | a_forward | 9 | 39 | 1 | 1.315789 | 20.526316 | 1.300000 | 9.676660806e-02 |
| upper_a | a_forward | 10 | 39 | 0 | 1.684211 | 20.526316 | 0.800000 | 5.004774499e-02 |
| upper_a | a_forward | 10 | 39 | 1 | 1.684211 | 20.526316 | 1.300000 | 1.431159675e-01 |
| upper_a | a_forward | 11 | 39 | 0 | 2.052632 | 20.526316 | 0.800000 | 1.048366062e-01 |
| upper_a | a_forward | 11 | 39 | 1 | 2.052632 | 20.526316 | 1.300000 | 1.812699562e-01 |
| upper_a | a_forward | 12 | 39 | 0 | 2.421053 | 20.526316 | 0.800000 | 1.499016139e-01 |
| upper_a | a_forward | 12 | 39 | 1 | 2.421053 | 20.526316 | 1.300000 | 2.129641907e-01 |
| upper_a | a_forward | 13 | 39 | 0 | 2.789474 | 20.526316 | 0.800000 | 1.872549067e-01 |
| upper_a | a_forward | 13 | 39 | 1 | 2.789474 | 20.526316 | 1.300000 | 2.393843856e-01 |
| upper_a | a_forward | 14 | 39 | 0 | 3.157895 | 20.526316 | 0.800000 | 2.183464428e-01 |
| upper_a | a_forward | 14 | 39 | 1 | 3.157895 | 20.526316 | 1.300000 | 2.613869587e-01 |
| upper_a | a_forward | 15 | 39 | 0 | 3.526316 | 20.526316 | 0.800000 | 2.442477575e-01 |
| upper_a | a_forward | 15 | 39 | 1 | 3.526316 | 20.526316 | 1.300000 | 2.796149832e-01 |
| upper_a | a_forward | 16 | 39 | 0 | 3.894737 | 20.526316 | 0.800000 | 2.657683854e-01 |
| upper_a | a_forward | 16 | 39 | 1 | 3.894737 | 20.526316 | 1.300000 | 2.945651324e-01 |
| upper_a | a_forward | 17 | 39 | 0 | 4.263158 | 20.526316 | 0.800000 | 2.835318442e-01 |
| upper_a | a_forward | 17 | 39 | 1 | 4.263158 | 20.526316 | 1.300000 | 3.066292320e-01 |
| upper_a | a_forward | 18 | 39 | 0 | 4.631579 | 20.526316 | 0.800000 | 2.980265255e-01 |
| upper_a | a_forward | 18 | 39 | 1 | 4.631579 | 20.526316 | 1.300000 | 3.161214058e-01 |
| upper_a | a_forward | 19 | 39 | 0 | 5.000000 | 20.526316 | 0.800000 | 3.096404996e-01 |
| upper_a | a_forward | 19 | 39 | 1 | 5.000000 | 20.526316 | 1.300000 | 3.232963272e-01 |
| upper_a | a_forward | 20 | 39 | 0 | 5.368421 | 20.526316 | 0.800000 | 3.186856298e-01 |
| upper_a | a_forward | 20 | 39 | 1 | 5.368421 | 20.526316 | 1.300000 | 3.283614661e-01 |
| upper_a | a_forward | 21 | 39 | 0 | 5.736842 | 20.526316 | 0.800000 | 3.254142422e-01 |
| upper_a | a_forward | 21 | 39 | 1 | 5.736842 | 20.526316 | 1.300000 | 3.314847961e-01 |
| upper_a | a_forward | 22 | 39 | 0 | 6.105263 | 20.526316 | 0.800000 | 3.300302360e-01 |
| upper_a | a_forward | 22 | 39 | 1 | 6.105263 | 20.526316 | 1.300000 | 3.327985174e-01 |
| upper_a | a_forward | 23 | 39 | 0 | 6.473684 | 20.526316 | 0.800000 | 3.326955770e-01 |
| upper_a | a_forward | 23 | 39 | 1 | 6.473684 | 20.526316 | 1.300000 | 3.323986265e-01 |
| upper_a | a_forward | 24 | 39 | 0 | 6.842105 | 20.526316 | 0.800000 | 3.335323649e-01 |
| upper_a | a_forward | 24 | 39 | 1 | 6.842105 | 20.526316 | 1.300000 | 3.303394591e-01 |
| upper_a | a_forward | 25 | 39 | 0 | 7.210526 | 20.526316 | 0.800000 | 3.326199692e-01 |
| upper_a | a_forward | 25 | 39 | 1 | 7.210526 | 20.526316 | 1.300000 | 3.266215482e-01 |
| upper_a | a_forward | 26 | 39 | 0 | 7.578947 | 20.526316 | 0.800000 | 3.299860105e-01 |
| upper_a | a_forward | 26 | 39 | 1 | 7.578947 | 20.526316 | 1.300000 | 3.211702642e-01 |
| upper_a | a_forward | 27 | 39 | 0 | 7.947368 | 20.526316 | 0.800000 | 3.255892112e-01 |
| upper_a | a_forward | 27 | 39 | 1 | 7.947368 | 20.526316 | 1.300000 | 3.138018805e-01 |
| upper_a | a_forward | 28 | 39 | 0 | 8.315789 | 20.526316 | 0.800000 | 3.192914751e-01 |
| upper_a | a_forward | 28 | 39 | 1 | 8.315789 | 20.526316 | 1.300000 | 3.041733897e-01 |
| upper_a | a_forward | 29 | 39 | 0 | 8.684211 | 20.526316 | 0.800000 | 3.108163058e-01 |
| upper_a | a_forward | 29 | 39 | 1 | 8.684211 | 20.526316 | 1.300000 | 2.917136901e-01 |
| upper_a | a_forward | 30 | 39 | 0 | 9.052632 | 20.526316 | 0.800000 | 2.996915204e-01 |
| upper_a | a_forward | 30 | 39 | 1 | 9.052632 | 20.526316 | 1.300000 | 2.755387563e-01 |
| upper_a | a_forward | 31 | 39 | 0 | 9.421053 | 20.526316 | 0.800000 | 2.851771082e-01 |
| upper_a | a_forward | 31 | 39 | 1 | 9.421053 | 20.526316 | 1.300000 | 2.543652280e-01 |
| upper_a | a_forward | 32 | 39 | 0 | 9.789474 | 20.526316 | 0.800000 | 2.661845883e-01 |
| upper_a | a_forward | 32 | 39 | 1 | 9.789474 | 20.526316 | 1.300000 | 2.264577719e-01 |
| upper_a | a_forward | 33 | 39 | 0 | 10.157895 | 20.526316 | 0.800000 | 2.412004046e-01 |
| upper_a | a_forward | 33 | 39 | 1 | 10.157895 | 20.526316 | 1.300000 | 1.896713093e-01 |
| upper_a | a_forward | 34 | 39 | 0 | 10.526316 | 20.526316 | 0.800000 | 2.082246075e-01 |
| upper_a | a_forward | 34 | 39 | 1 | 10.526316 | 20.526316 | 1.300000 | 1.416596428e-01 |
| upper_a | a_forward | 35 | 39 | 0 | 10.894737 | 20.526316 | 0.800000 | 1.647111146e-01 |
| upper_a | a_forward | 35 | 39 | 1 | 10.894737 | 20.526316 | 1.300000 | 8.028264303e-02 |
| upper_a | a_forward | 36 | 39 | 0 | 11.263158 | 20.526316 | 0.800000 | 1.074346361e-01 |
| upper_a | a_forward | 36 | 39 | 1 | 11.263158 | 20.526316 | 1.300000 | 4.145505619e-03 |
| upper_a | a_forward | 37 | 39 | 0 | 11.631579 | 20.526316 | 0.800000 | 3.214549950e-02 |

### V5_BASE_FINE

| boundary | direction | max | count>1e-10 | share | argmax index | argmax physical | requested at max | q50/q90/q95/q99 |
|---|---|---|---|---|---|---|---|---|
| lower_b | b_backward | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_b | b_forward | 1.272e+00 | 7 | 8.974e-02 | (38, 38, 1) | (5.0, 10.0, 1.3) | 1.272e+00 | 0.6917378344753425/1.1908588680949566/1.2311871654701507/1.263449803370306 |
| lower_a | a_backward | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_a | a_forward | 0.000e+00 | 0 | 0.000e+00 | (0, 38, 0) | (-2.0, 10.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |

Complete offending states (requested outward rate > 1e-10):

| boundary | direction | b_index | a_index | z_index | b | a | z | requested outward rate |
|---|---|---|---|---|---|---|---|---|
| upper_b | b_forward | 38 | 32 | 1 | 5.000000 | 8.421053 | 1.300000 | 9.147081014e-04 |
| upper_b | b_forward | 38 | 33 | 1 | 5.000000 | 8.684211 | 1.300000 | 2.209018943e-01 |
| upper_b | b_forward | 38 | 34 | 1 | 5.000000 | 8.947368 | 1.300000 | 4.527795569e-01 |
| upper_b | b_forward | 38 | 35 | 1 | 5.000000 | 9.210526 | 1.300000 | 6.917378345e-01 |
| upper_b | b_forward | 38 | 36 | 1 | 5.000000 | 9.473684 | 1.300000 | 9.273456077e-01 |
| upper_b | b_forward | 38 | 37 | 1 | 5.000000 | 9.736842 | 1.300000 | 1.137087805e+00 |
| upper_b | b_forward | 38 | 38 | 1 | 5.000000 | 10.000000 | 1.300000 | 1.271515463e+00 |

## Shared-interior policy stability (Phase C)

Frozen V0-based shared-interior mask: `b_index <= 17`, `a_index <= 17`, all z. Comparisons are at exact common nodes without interpolation. `rel_diff = max_abs / max(1, max|V0 reference|)` is a scale-aware relative difference. Strict-interior submetrics exclude the first asset layer and do not replace the frozen primary mask.

### V0_vs_V1_A_WIDE

| field | max_abs_diff | rel_diff | strict-interior max_abs | strict-interior rel | label mismatch |
|---|---|---|---|---|---|
| value | 2.087e+00 | 3.053e-02 | 2.087e+00 | 3.162e-02 | — |
| consumption | 6.093e-02 | 5.149e-02 | 6.093e-02 | 5.149e-02 | — |
| labor | 2.504e-02 | 2.246e-02 | 2.504e-02 | 2.266e-02 | — |
| transfer | 2.793e-01 | 2.793e-01 | 2.793e-01 | 2.793e-01 | — |
| mu_a | 2.892e-01 | 2.892e-01 | 2.892e-01 | 2.892e-01 | — |
| mu_b | 2.163e-01 | 2.163e-01 | 2.163e-01 | 2.163e-01 | — |
| liquid_label | — | — | — | — | 29 |
| transfer_label | — | — | — | — | 205 |

### V0_vs_V2_B_WIDE

| field | max_abs_diff | rel_diff | strict-interior max_abs | strict-interior rel | label mismatch |
|---|---|---|---|---|---|
| value | 2.214e-02 | 3.239e-04 | 4.686e-03 | 7.102e-05 | — |
| consumption | 1.587e-02 | 1.341e-02 | 8.510e-03 | 7.191e-03 | — |
| labor | 6.094e-03 | 5.466e-03 | 3.414e-03 | 3.090e-03 | — |
| transfer | 2.624e-02 | 2.624e-02 | 2.624e-02 | 2.624e-02 | — |
| mu_a | 2.624e-02 | 2.624e-02 | 2.624e-02 | 2.624e-02 | — |
| mu_b | 2.783e-02 | 2.783e-02 | 2.783e-02 | 2.783e-02 | — |
| liquid_label | — | — | — | — | 0 |
| transfer_label | — | — | — | — | 0 |

### V0_vs_V3_AB_MID

| field | max_abs_diff | rel_diff | strict-interior max_abs | strict-interior rel | label mismatch |
|---|---|---|---|---|---|
| value | 1.283e+00 | 1.877e-02 | 1.283e+00 | 1.945e-02 | — |
| consumption | 4.032e-02 | 3.407e-02 | 4.032e-02 | 3.407e-02 | — |
| labor | 1.623e-02 | 1.456e-02 | 1.623e-02 | 1.469e-02 | — |
| transfer | 2.208e-01 | 2.208e-01 | 2.208e-01 | 2.208e-01 | — |
| mu_a | 2.305e-01 | 2.305e-01 | 2.305e-01 | 2.305e-01 | — |
| mu_b | 1.623e-01 | 1.623e-01 | 1.623e-01 | 1.623e-01 | — |
| liquid_label | — | — | — | — | 22 |
| transfer_label | — | — | — | — | 143 |

### V0_vs_V4_AB_WIDE

| field | max_abs_diff | rel_diff | strict-interior max_abs | strict-interior rel | label mismatch |
|---|---|---|---|---|---|
| value | 2.071e+00 | 3.030e-02 | 2.071e+00 | 3.139e-02 | — |
| consumption | 6.059e-02 | 5.120e-02 | 6.059e-02 | 5.120e-02 | — |
| labor | 2.488e-02 | 2.232e-02 | 2.488e-02 | 2.252e-02 | — |
| transfer | 2.779e-01 | 2.779e-01 | 2.779e-01 | 2.779e-01 | — |
| mu_a | 2.878e-01 | 2.878e-01 | 2.878e-01 | 2.878e-01 | — |
| mu_b | 2.131e-01 | 2.131e-01 | 2.131e-01 | 2.131e-01 | — |
| liquid_label | — | — | — | — | 29 |
| transfer_label | — | — | — | — | 204 |

### V0_vs_V5_BASE_FINE

| field | max_abs_diff | rel_diff | strict-interior max_abs | strict-interior rel | label mismatch |
|---|---|---|---|---|---|
| value | 3.762e-01 | 5.504e-03 | 3.607e-01 | 5.467e-03 | — |
| consumption | 4.107e-02 | 3.471e-02 | 4.107e-02 | 3.471e-02 | — |
| labor | 1.783e-02 | 1.599e-02 | 1.783e-02 | 1.614e-02 | — |
| transfer | 9.381e-02 | 9.381e-02 | 9.381e-02 | 9.381e-02 | — |
| mu_a | 9.381e-02 | 9.381e-02 | 9.381e-02 | 9.381e-02 | — |
| mu_b | 9.088e-02 | 9.088e-02 | 9.088e-02 | 9.088e-02 | — |
| liquid_label | — | — | — | — | 21 |
| transfer_label | — | — | — | — | 41 |

## Mechanical generator diagnostics (Phase D)

The candidate generator `Q_c` admits only represented in-grid transitions, omits out-of-grid transitions, sets the diagonal to the negative sum of ACTUALLY ADMITTED off-diagonal rates, and includes the accepted z-switch block. Passing the mechanical thresholds does NOT authorize stationary density while the HJB requests material outward boundary policy.

| variant | row-sum max abs | neg offdiag max mag | neg offdiag count | nnz |
|---|---|---|---|---|
| V0_BASE | 6.106e-16 | 0.000e+00 | 0 | 3114 |
| V1_A_WIDE | 1.776e-15 | 0.000e+00 | 0 | 6334 |
| V2_B_WIDE | 6.661e-16 | 0.000e+00 | 0 | 6235 |
| V3_AB_MID | 8.882e-16 | 0.000e+00 | 0 | 7075 |
| V4_AB_WIDE | 1.332e-15 | 0.000e+00 | 0 | 12638 |
| V5_BASE_FINE | 1.332e-15 | 0.000e+00 | 0 | 12059 |

Required mechanical thresholds: `row_sum max abs <= 1e-12`, `negative off-diagonal magnitude <= 1e-12`.

## Stationary / tail / aggregate reachability (Phases E-F-G)

No pre-frozen variant reaches the same-process stationary gate: every converged variant retains material upper-boundary requested policy under the frozen `max requested outward <= 1e-10` criterion. All stationary/tail/aggregate fields are therefore `NOT_REACHED__HJB_KFE_SAME_PROCESS_BOUNDARY_GATE_FAILED`. No clipped density is accepted.

Scientific reading: boundary influence does NOT converge away within the exact pre-frozen domains; the evidence points to persistent high-wealth mean-reversion / finite-domain HJB/KFE closure behavior. This is a bounded diagnostic observation, not a claim of stationary-tail existence/non-existence.

## Reproducibility

- randomness: `NOT_APPLICABLE`; repeat pass: `True`; terminal run1/run2: `DLH_5F_UPPER_DOMAIN_DIAGNOSTIC_COMPLETE__NO_PREFROZEN_DOMAIN_REACHES_SAME_PROCESS_STATIONARY_TAIL__SCIENTIFIC_REVIEW_REQUIRED` / `DLH_5F_UPPER_DOMAIN_DIAGNOSTIC_COMPLETE__NO_PREFROZEN_DOMAIN_REACHES_SAME_PROCESS_STATIONARY_TAIL__SCIENTIFIC_REVIEW_REQUIRED`.
- V0_BASE: structural identical True, max numeric diff 0.000e+00, aligned non-finite 1, mismatched 0, pass True.
- V1_A_WIDE: structural identical True, max numeric diff 0.000e+00, aligned non-finite 1, mismatched 0, pass True.
- V2_B_WIDE: structural identical True, max numeric diff 0.000e+00, aligned non-finite 1, mismatched 0, pass True.
- V3_AB_MID: structural identical True, max numeric diff 0.000e+00, aligned non-finite 1, mismatched 0, pass True.
- V4_AB_WIDE: structural identical True, max numeric diff 0.000e+00, aligned non-finite 1, mismatched 0, pass True.
- V5_BASE_FINE: structural identical True, max numeric diff 0.000e+00, aligned non-finite 1, mismatched 0, pass True.

## Liquid-vs-illiquid upper-domain behavior

Material-request indicators for the liquid (upper-b) and illiquid (upper-a) dimensions diverge across variants, supporting the secondary annotation `LIQUID_ILLIQUID_UPPER_DOMAIN_BEHAVIOR_DIVERGES__SEPARATE_SCIENTIFIC_TREATMENT_REQUIRED`.

## Artifact integrity

- accepted MATLAB-faithful oracle blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`, SHA-256 `1795718C469FC3B427CAB8E3D5957C133BEAD6EACC9EF0A25A3EDB7211D1A024` re-verified read-only (unchanged from the accepted Issue #23/#26 state).
- no existing tracked file modified; dedicated branch `dsh/issue-29-dlh-5f-upper-domain-stationary-tail-2026-09-01`; allowlist-only additions (3 artifacts + 8 evidence files).

DLH-5F implements NO repair: the accepted HJB/local-policy/KFE/regional source is immutable; no conservative density is accepted for economic interpretation when the HJB/KFE process differs; no regularization/jitter/pseudoinverse; no parameter/price/tolerance retuning; no D1-D3; no regional or multi-province GE; no learned network; no nominal HANK.