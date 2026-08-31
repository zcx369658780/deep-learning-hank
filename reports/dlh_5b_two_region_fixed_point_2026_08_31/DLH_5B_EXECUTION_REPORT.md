# DLH-5B — Two-Region Fixed-Point Execution Report (Issue #25)

Terminal classification:

`DLH_5B_TWO_REGION_ARCHITECTURE_VALIDATED__PERTURBED_PATH_HOUSEHOLD_BLOCKED_READY_FOR_GPT_REVIEW`

Qualification: `PASS_WITH_OBSERVATIONS` — a boundary-mass warning (threshold 0.10) was observed; surfaced, non-blocking for this architecture-validation stage.

## Fixture identity

- Accepted household oracle: `src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py` (immutable).
- Frozen config: `configs/dlh_5b_two_region_symmetric_anchor.toml` (not modified after seeing results).
- Household fixture: `VALIDATION_FIXTURE_NOT_CALIBRATION` from `tests/test_dlh_4b_transfer.py`.
- Network: `M=[1.0, 1.0]`, `m_L=[0.1, 0.1]`, `P^L=[[0.9, 0.1], [0.1, 0.9]]`.
- Anchor: `w*=[1.0, 1.0]`, `r_a*=[0.03, 0.03]`, `alpha=[0.3333333333333333, 0.3333333333333333]`.

## Derived anchor (derived once, then frozen for all cases)

| object | value |
|---|---|
| `A*` | 8.9586992251 |
| `L*` | 0.992496736638 |
| `C*` | 1.05828286181 |
| `B*` | 0.795287884087 |
| `K*` (=M A*) | 8.9586992251 |
| `Z*` | 0.720420345882 |
| `delta*` | 0.0253929042432 |

Sanity gate: {'A_star_positive': True, 'L_star_positive': True, 'Z_star_positive': True, 'delta_in_unit': True, 'all_finite': True}

Anchor HJB: converged=True, iterations=11, statistic=1.674e-08
Anchor KFE: mass_error=2.220e-16, min_density=-6.654e-20

## S0 — anchor smoke (one-turn from Gamma0={1,1,0.03,0.03})

- gate: `PASS`
- `R_w` = 2.220e-16 (required <= 1e-10)
- `R_ra` = 6.939e-18 (required <= 1e-10)
- accounting: {'origin0_conservation': True, 'origin1_conservation': True, 'economy_labor': True, 'wage_bill': True, 'network_rows_sum': True, 'network_nonneg': True}
- KFE checks: {'kfe_mass_error0': True, 'kfe_min_density0': True, 'kfe_finite0': True, 'kfe_mass_error1': True, 'kfe_min_density1': True, 'kfe_finite1': True}
- firm checks: {'K0_positive': True, 'Ldest0_positive': True, 'Y0_positive': True, 'w_hat0_positive': True, 'r_hat0_finite': True, 'K1_positive': True, 'Ldest1_positive': True, 'Y1_positive': True, 'w_hat1_positive': True, 'r_hat1_finite': True}
- boundary masses: {'region0': {'b_min': 1.970446230087985e-06, 'b_max': 1.5548504529136054e-05, 'a_min': 0.0, 'a_max': 0.1963480310595223, 'warning': True}, 'region1': {'b_min': 1.970446230087985e-06, 'b_max': 1.5548504529136054e-05, 'a_min': 0.0, 'a_max': 0.1963480310595223, 'warning': True}}

## S1 — perturbed outer iteration

- stop reason: `HOUSEHOLD_BLOCK_FAILED:region0:faithful contaminated-row solve is non-finite`
- iteration count: 4 (max_iter=25)
- boundary warning observed: True

## S2 — region-order invariance (S1 initial snapshot)

- max one-turn numeric difference (order [1,2] vs [2,1]): 0.000e+00 (required <= 1e-12)
- pass: True

## Reproducibility (randomness NOT_APPLICABLE)

- S0 repeat: {'pass_bool': True, 'max_numeric_diff': 0.0, 'same_stop_reason': True, 'reason1': 'PASS', 'reason2': 'PASS', 'within_tol': True}
- S1 repeat: {'pass_bool': True, 'stop_reason1': 'HOUSEHOLD_BLOCK_FAILED:region0:faithful contaminated-row solve is non-finite', 'stop_reason2': 'HOUSEHOLD_BLOCK_FAILED:region0:faithful contaminated-row solve is non-finite', 'iterations1': 4, 'iterations2': 4, 'max_trace_numeric_diff': 0.0, 'within_tol': True}

## Artifact identities (SHA-256)

- `DLH_5B_ANCHOR_FIXTURE.json`: `BA8FD41A1594F811F57A12E40366E5E2ED8F770572FEABC9CC9BB0E569CD75B3`
- `DLH_5B_ORDER_INVARIANCE.json`: `F78773BEAE24E3CC3A4099F2E6EAA1C3D68FAD1A9288A27EDA1AAD7E693CEDF0`
- `DLH_5B_REPRODUCIBILITY.json`: `0C1F96B754F9DBFF762EF3A5FA46D2C18B14D2C954A114D5A5CF7EE65A071BDC`
- `DLH_5B_S0_ANCHOR_TRACE.csv`: `0F632DBE58245D22C7E6297A908DAE9FEA4F372D39FF69212C4F8C173BE2221D`
- `DLH_5B_S1_PERTURBED_TRACE.csv`: `572ADC1E4C5C340DAF25B0257FEA930FF8FB3C6EB24E98BA59FC6130AF4CAAEE`

## Notes / caveats

- No automatic retry, adaptive damping, grid expansion or PASS-seeking tuning was used.
- HJB/KFE/boundary failures are preserved as diagnostics; nothing was silently discarded.
- `B_i` is a household liquid-asset diagnostic only; no `B=1` closure was used.
- `K_i = M_i * A_i` is the provisional NSR-HANK exploratory closure; not empirical calibration.
- Outer map uses fixed damping only; no Brent/Newton/fsolve.
