# DLH-5G — Liquid Upper-Domain Asymptotic and Resolution Diagnostic (Issue #31)

Policy-only diagnostic isolating the liquid (b) upper boundary under a completely frozen illiquid side and frozen economics. Accepted MATLAB-faithful HJB source is immutable and reused read-only.

Overall terminal classification: `DLH_5G_LIQUID_B_PREFROZEN_EXTENT_REACHES_BOUNDARY_THRESHOLD__GPT_REVIEW_REQUIRED`

Secondary scientific annotations: `DLH_5G_B_RESOLUTION_SENSITIVITY_REMAINS_MATERIAL__SEPARATE_NUMERICAL_REVIEW_REQUIRED`

Frozen economics: `wbar=1.0`, `r_a=0.03`; illiquid side frozen at `a20 [0.0,10.0]`, `a_max=10.0`, `da=0.526315789474`, taper `r_a*(1-0.1*(a/a_max)^9)_MATLAB_FAITHFUL_UNCHANGED`; all non-grid objects the accepted DLH-5B/DLH-5E fixture (`configs/dlh_5b_two_region_symmetric_anchor.toml`, region_index=0).

## Variant status (Phase A)

| variant | b pts | b domain | b max | db | a grid | HJB conv | iters | stat | raw upper-b max | raw lower-b max | terminal |
|---|---|---|---|---|---|---|---|---|---|---|---|
| G0_BASE | 20 | [-2.0,5.0] | 5.0 | 0.368421052631579 | a20 [0.0,10.0] | True | 11 | 1.674e-08 | 1.303e-01 | 0.000e+00 | HJB_CONVERGED |
| G1_B_WIDE_1 | 40 | [-2.0,12.368421052631579] | 12.368421052631579 | 0.368421052631579 | a20 [0.0,10.0] | True | 11 | 1.028e-08 | 3.759e-03 | 0.000e+00 | HJB_CONVERGED |
| G2_B_WIDE_2 | 60 | [-2.0,19.736842105263158] | 19.736842105263158 | 0.368421052631579 | a20 [0.0,10.0] | True | 11 | 1.172e-08 | 0.000e+00 | 0.000e+00 | HJB_CONVERGED |
| G3_B_WIDE_3 | 80 | [-2.0,27.105263157894736] | 27.105263157894736 | 0.368421052631579 | a20 [0.0,10.0] | True | 11 | 1.374e-08 | 0.000e+00 | 0.000e+00 | HJB_CONVERGED |
| G4_BASE_B_FINE | 39 | [-2.0,5.0] | 5.0 | 0.18421052631578938 | a20 [0.0,10.0] | True | 11 | 1.183e-08 | 4.508e-03 | 0.000e+00 | HJB_CONVERGED |
| G5_WIDE1_B_FINE | 79 | [-2.0,12.368421052631579] | 12.368421052631579 | 0.18421052631578938 | a20 [0.0,10.0] | True | 11 | 1.089e-08 | 0.000e+00 | 0.000e+00 | HJB_CONVERGED |

## Liquid upper/lower boundary diagnostics (Phase B)

Raw drift (`max(mu_b,0)` / `max(-mu_b,0)`) is the primary cross-resolution asymptotic quantity; requested generator rate (raw/`db`) is the HJB/KFE boundary-compatibility quantity. Raw threshold = `1e-10*db` corresponds to the accepted requested-rate threshold `1e-10`. Coordinates are exact `(b_index,a_index,z_index)` plus physical `(b,a,z)` via C-order unraveling on the actual 2-D boundary slice.

### G0_BASE

| boundary | kind | max | count | share | argmax index | argmax physical | value at argmax | q50/q90/q95/q99 |
|---|---|---|---|---|---|---|---|---|
| upper_b | raw | 1.303e-01 | 3 | 7.500e-02 | (19, 19, 1) | (5.0, 10.0, 1.3) | 1.303e-01 | 0.10016216132488465/0.12429491345043316/0.1273115074661267/0.12972478267868157 |
| upper_b | requested | 3.537e-01 | 3 | 7.500e-02 | (19, 19, 1) | (5.0, 10.0, 1.3) | 3.537e-01 | 0.27186872359611547/0.33737190793689/0.34555980597948677/0.35211012441356426 |
| lower_b | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_b | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |

Complete offending states (raw > `1e-10*db`; requested > `1e-10`):

| boundary | kind | b_index | a_index | z_index | b | a | z | rate |
|---|---|---|---|---|---|---|---|---|
| upper_b | raw | 19 | 17 | 1 | 5.000000 | 8.947368 | 1.300000 | 4.264867848e-02 |
| upper_b | raw | 19 | 18 | 1 | 5.000000 | 9.473684 | 1.300000 | 1.001621613e-01 |
| upper_b | raw | 19 | 19 | 1 | 5.000000 | 10.000000 | 1.300000 | 1.303281015e-01 |
| upper_b | requested | 19 | 17 | 1 | 5.000000 | 8.947368 | 1.300000 | 1.157606987e-01 |
| upper_b | requested | 19 | 18 | 1 | 5.000000 | 9.473684 | 1.300000 | 2.718687236e-01 |
| upper_b | requested | 19 | 19 | 1 | 5.000000 | 10.000000 | 1.300000 | 3.537477040e-01 |

### G1_B_WIDE_1

| boundary | kind | max | count | share | argmax index | argmax physical | value at argmax | q50/q90/q95/q99 |
|---|---|---|---|---|---|---|---|---|
| upper_b | raw | 3.759e-03 | 1 | 2.500e-02 | (39, 19, 1) | (12.368421052631579, 10.0, 1.3) | 3.759e-03 | 0.003759131180849362/0.003759131180849362/0.003759131180849362/0.003759131180849362 |
| upper_b | requested | 1.020e-02 | 1 | 2.500e-02 | (39, 19, 1) | (12.368421052631579, 10.0, 1.3) | 1.020e-02 | 0.010203356062305411/0.010203356062305411/0.010203356062305411/0.010203356062305411 |
| lower_b | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_b | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |

Complete offending states (raw > `1e-10*db`; requested > `1e-10`):

| boundary | kind | b_index | a_index | z_index | b | a | z | rate |
|---|---|---|---|---|---|---|---|---|
| upper_b | raw | 39 | 19 | 1 | 12.368421 | 10.000000 | 1.300000 | 3.759131181e-03 |
| upper_b | requested | 39 | 19 | 1 | 12.368421 | 10.000000 | 1.300000 | 1.020335606e-02 |

### G2_B_WIDE_2

| boundary | kind | max | count | share | argmax index | argmax physical | value at argmax | q50/q90/q95/q99 |
|---|---|---|---|---|---|---|---|---|
| upper_b | raw | 0.000e+00 | 0 | 0.000e+00 | (59, 0, 0) | (19.736842105263158, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_b | requested | 0.000e+00 | 0 | 0.000e+00 | (59, 0, 0) | (19.736842105263158, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_b | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_b | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |

Complete offending states (raw > `1e-10*db`; requested > `1e-10`):

No state exceeds the raw or requested threshold.

### G3_B_WIDE_3

| boundary | kind | max | count | share | argmax index | argmax physical | value at argmax | q50/q90/q95/q99 |
|---|---|---|---|---|---|---|---|---|
| upper_b | raw | 0.000e+00 | 0 | 0.000e+00 | (79, 0, 0) | (27.105263157894736, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_b | requested | 0.000e+00 | 0 | 0.000e+00 | (79, 0, 0) | (27.105263157894736, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_b | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_b | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |

Complete offending states (raw > `1e-10*db`; requested > `1e-10`):

No state exceeds the raw or requested threshold.

### G4_BASE_B_FINE

| boundary | kind | max | count | share | argmax index | argmax physical | value at argmax | q50/q90/q95/q99 |
|---|---|---|---|---|---|---|---|---|
| upper_b | raw | 4.508e-03 | 1 | 2.500e-02 | (38, 19, 1) | (5.0, 10.0, 1.3) | 4.508e-03 | 0.0045079832842120915/0.0045079832842120915/0.0045079832842120915/0.0045079832842120915 |
| upper_b | requested | 2.447e-02 | 1 | 2.500e-02 | (38, 19, 1) | (5.0, 10.0, 1.3) | 2.447e-02 | 0.024471909257151366/0.024471909257151366/0.024471909257151366/0.024471909257151366 |
| lower_b | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_b | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |

Complete offending states (raw > `1e-10*db`; requested > `1e-10`):

| boundary | kind | b_index | a_index | z_index | b | a | z | rate |
|---|---|---|---|---|---|---|---|---|
| upper_b | raw | 38 | 19 | 1 | 5.000000 | 10.000000 | 1.300000 | 4.507983284e-03 |
| upper_b | requested | 38 | 19 | 1 | 5.000000 | 10.000000 | 1.300000 | 2.447190926e-02 |

### G5_WIDE1_B_FINE

| boundary | kind | max | count | share | argmax index | argmax physical | value at argmax | q50/q90/q95/q99 |
|---|---|---|---|---|---|---|---|---|
| upper_b | raw | 0.000e+00 | 0 | 0.000e+00 | (78, 0, 0) | (12.368421052631579, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| upper_b | requested | 0.000e+00 | 0 | 0.000e+00 | (78, 0, 0) | (12.368421052631579, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_b | raw | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |
| lower_b | requested | 0.000e+00 | 0 | 0.000e+00 | (0, 0, 0) | (-2.0, 0.0, 0.8) | 0.000e+00 | NOT_APPLICABLE |

Complete offending states (raw > `1e-10*db`; requested > `1e-10`):

No state exceeds the raw or requested threshold.

## Illiquid-boundary regression evidence (Phase C)

Upper/lower a requested-rate regression diagnostics only. The illiquid domain/taper is frozen but remains scientifically unresolved; DLH-5G does not resolve or redesign the illiquid boundary.

- G0_BASE: lower_a: max=0.000e+00 count=0 share=0.000e+00 argmax=(0, 0, 0); upper_a: max=2.641e-01 count=28 share=7.000e-01 argmax=(14, 19, 1)
- G1_B_WIDE_1: lower_a: max=0.000e+00 count=0 share=0.000e+00 argmax=(0, 0, 0); upper_a: max=3.095e-01 count=68 share=8.500e-01 argmax=(22, 19, 0)
- G2_B_WIDE_2: lower_a: max=0.000e+00 count=0 share=0.000e+00 argmax=(0, 0, 0); upper_a: max=3.095e-01 count=108 share=9.000e-01 argmax=(22, 19, 0)
- G3_B_WIDE_3: lower_a: max=0.000e+00 count=0 share=0.000e+00 argmax=(0, 0, 0); upper_a: max=3.095e-01 count=147 share=9.187e-01 argmax=(22, 19, 0)
- G4_BASE_B_FINE: lower_a: max=0.000e+00 count=0 share=0.000e+00 argmax=(0, 0, 0); upper_a: max=3.564e-01 count=56 share=7.179e-01 argmax=(33, 19, 1)
- G5_WIDE1_B_FINE: lower_a: max=0.000e+00 count=0 share=0.000e+00 argmax=(0, 0, 0); upper_a: max=3.662e-01 count=136 share=8.608e-01 argmax=(44, 19, 0)

## Same-spacing liquid extent trend (Phase D: G0 -> G1 -> G2 -> G3)

| variant | raw upper-b max | requested upper-b max | raw count | requested count | raw share | requested share | argmax physical (a,z) |
|---|---|---|---|---|---|---|---|
| G0_BASE | 1.303e-01 | 3.537e-01 | 3 | 3 | 7.500e-02 | 7.500e-02 | (10.0, 1.3) |
| G1_B_WIDE_1 | 3.759e-03 | 1.020e-02 | 1 | 1 | 2.500e-02 | 2.500e-02 | (10.0, 1.3) |
| G2_B_WIDE_2 | 0.000e+00 | 0.000e+00 | 0 | 0 | 0.000e+00 | 0.000e+00 | (0.0, 0.8) |
| G3_B_WIDE_3 | 0.000e+00 | 0.000e+00 | 0 | 0 | 0.000e+00 | 0.000e+00 | (0.0, 0.8) |

- adjacent raw attenuation ratios (G0/G1, G1/G2, G2/G3): [34.66974, 'inf', None] (`inf` = nonzero-to-zero attenuation)
- adjacent requested attenuation ratios: [34.66974, 'inf', None]
- raw ratios relative to G0 (G1/G0, G2/G0, G3/G0): [0.028844, 0.0, 0.0]
- requested ratios relative to G0: [0.028844, 0.0, 0.0]
- strictly decreasing raw upper-b max over G0->G3: False
- strictly decreasing requested upper-b max over G0->G3: False
- **raw and requested upper-b outward drift reach EXACT ZERO at `G2_B_WIDE_2` (b_max=19.736842) and remain zero at wider extents.** This is full attenuation: the liquid upper-boundary influence converges away within the pre-frozen b extents.

This is a policy-only trend; it does not establish stationary-tail existence or non-existence.

## b-resolution stability (Phase E: G0 vs G4, G1 vs G5)

Exact aligned-node comparisons at the shared-interior mask (`b_index <= coarse_b_pts-3`, `a_index <= 17`, all z). `rel_diff = max_abs / max(1, max|coarse|)` is scale-aware. A supplementary raw `mu_b` comparison at the shared coarse-grid upper-region b nodes is reported separately from each grid's own upper-boundary slice.

### G0_vs_G4

| field | max_abs_diff | rel_diff | label mismatch |
|---|---|---|---|
| value | 2.629e-01 | 3.847e-03 | — |
| consumption | 3.542e-02 | 2.993e-02 | — |
| labor | 1.544e-02 | 1.385e-02 | — |
| transfer | 7.375e-02 | 7.375e-02 | — |
| mu_a | 7.375e-02 | 7.375e-02 | — |
| mu_b | 1.029e-01 | 1.029e-01 | — |
| liquid_label | — | — | 11 |
| transfer_label | — | — | 29 |
| raw_mu_b_upper_shared_nodes | 1.258e-01 | 1.258e-01 | — |

### G1_vs_G5

| field | max_abs_diff | rel_diff | label mismatch |
|---|---|---|---|
| value | 2.631e-01 | 3.849e-03 | — |
| consumption | 3.542e-02 | 2.627e-02 | — |
| labor | 1.544e-02 | 1.385e-02 | — |
| transfer | 7.377e-02 | 7.377e-02 | — |
| mu_a | 7.377e-02 | 7.377e-02 | — |
| mu_b | 1.029e-01 | 1.029e-01 | — |
| liquid_label | — | — | 26 |
| transfer_label | — | — | 43 |
| raw_mu_b_upper_shared_nodes | 3.759e-03 | 3.759e-03 | — |

## Scientific stopping rule (Phase F)

DLH-5G is policy-only. Stationary KFE / nullspace / pin / density / tail mass / stationary flux / `C,L,A,B` are `NOT_AUTHORIZED__DLH_5G_POLICY_ONLY_LIQUID_DOMAIN_DIAGNOSTIC` and were not executed, because the illiquid upper-boundary process remains unresolved and DLH-5G isolates liquid-domain behavior without changing that scientific state.

## Reproducibility

- randomness: `NOT_APPLICABLE`; repeat pass: `True`; terminal run1/run2: `DLH_5G_LIQUID_B_PREFROZEN_EXTENT_REACHES_BOUNDARY_THRESHOLD__GPT_REVIEW_REQUIRED` / `DLH_5G_LIQUID_B_PREFROZEN_EXTENT_REACHES_BOUNDARY_THRESHOLD__GPT_REVIEW_REQUIRED`; annotations run1/run2: ['DLH_5G_B_RESOLUTION_SENSITIVITY_REMAINS_MATERIAL__SEPARATE_NUMERICAL_REVIEW_REQUIRED'] / ['DLH_5G_B_RESOLUTION_SENSITIVITY_REMAINS_MATERIAL__SEPARATE_NUMERICAL_REVIEW_REQUIRED'].
- G0_BASE: structural identical True, max numeric diff 0.000e+00, aligned non-finite 0, mismatched 0, pass True.
- G1_B_WIDE_1: structural identical True, max numeric diff 0.000e+00, aligned non-finite 0, mismatched 0, pass True.
- G2_B_WIDE_2: structural identical True, max numeric diff 0.000e+00, aligned non-finite 0, mismatched 0, pass True.
- G3_B_WIDE_3: structural identical True, max numeric diff 0.000e+00, aligned non-finite 0, mismatched 0, pass True.
- G4_BASE_B_FINE: structural identical True, max numeric diff 0.000e+00, aligned non-finite 0, mismatched 0, pass True.
- G5_WIDE1_B_FINE: structural identical True, max numeric diff 0.000e+00, aligned non-finite 0, mismatched 0, pass True.

## Artifact integrity

- accepted MATLAB-faithful oracle blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`, SHA-256 `1795718C469FC3B427CAB8E3D5957C133BEAD6EACC9EF0A25A3EDB7211D1A024` re-verified read-only (unchanged from the accepted Issue #23/#26 state).
- no existing tracked file modified; dedicated branch `dsh/issue-31-dlh-5g-liquid-upper-domain-asymptotic-2026-09-01`; allowlist-only additions (3 artifacts + 8 evidence files).

DLH-5G implements NO repair and NO stationary acceptance: accepted HJB/KFE/regional source immutable; `a_max`/a-grid/taper/economics/tolerances/initialization frozen; no clipping; no D1-D3; no regional or multi-province GE; no learned network; no nominal HANK.