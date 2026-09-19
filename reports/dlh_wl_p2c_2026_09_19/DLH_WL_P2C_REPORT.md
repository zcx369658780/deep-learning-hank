# DLH-WL-P2C — durable per-fit-output replication of the frozen synthetic prototype

## 0. Status

```
terminal: DLH_WL_P2C_DURABLE_OUTPUT_REPLICATION__PASS__P2_METHOD_GATE_COMPLETE
```

- Issue: **#78** / `DLH_WL_P2C_DURABLE_OUTPUT_REPLICATION`; route `DLH-WL-V1-20260918`
- PRE_RUN_FREEZE SHA (executed science code identity): `ae4115f20bb3bc7f43ab79d9d0ccf65b62fa2c7d`
- scientific module blob: `b1f2cd043605c511e4965254657d12306170609b` (MATCH)
- frozen config blob: `bb5dbbd0746e9d92874f94b03a1d54f3d382c4a8` (MATCH)
- science invocations: **1**; science retries: **0**
- fit attempts started / completed / failed: **12 / 12 / 0**
- science wall clock: **3.094154 s** (source `SCIENCE_SEAL`, ceiling 1800 s)
- render-only invocations so far: **1** (zero fits, zero optimizer steps)

## 1. What changed from #76/#77 (durability boundary only)

The #75 scientific design is unchanged: 5 regions x 4 periods, the frozen support, the S0/S1 generators, three baseline families (fixed support-normalized uniform, six-parameter contrast-identifiable gravity/logit MLE, small MLP pair scorer with 16/8 hidden widths under masked softmax), the 9/3/2/6 split, TRAIN-only preprocessing, neural seeds 0/1/2, the frozen metrics/tolerances, 12 planned fit executions, a 13-attempt ceiling and an 1800 s wall-clock ceiling.

Only the durability boundary changed. #77 was limited to completion metadata, so when it failed after the twelfth fit before writing RAW_RESULTS nothing could be recovered without retraining. P2C persists the complete scientific output of each fit — full 4x5x5 prediction tensor, coefficients, objective, convergence, best step, best validation loss, backend, diagnostics and a canonical payload SHA-256 — and fsyncs the completed record before the next fit may begin.

This render stage performs zero fits and zero optimizer steps. Every number it publishes is recomputed from the persisted FIT_COMPLETED prediction tensors of the durable attempt ledger plus the frozen inputs. No fitter, no optimizer, no training replay and no seed is used, and the ledger and science seal are never modified.

## 2. Acceptance gate checks

| check | value |
|---|---|
| pre_run_freeze_sha_recorded | True |
| exactly_one_science_invocation | True |
| zero_science_retries | True |
| exactly_twelve_started | True |
| exactly_twelve_completed | True |
| zero_failed_fits | True |
| no_unmatched_started_record | True |
| started_indices_exactly_1_to_12 | True |
| completed_indices_exactly_1_to_12 | True |
| started_before_completed_ordering_ok | True |
| ledger_record_count_is_24 | True |
| every_completed_record_has_full_predictions | True |
| every_prediction_shape_is_4x5x5 | True |
| every_payload_sha256_verifies | True |
| every_completed_record_has_metadata | True |
| science_wall_clock_within_ceiling | True |
| determinism_within_tolerance | True |
| row_normalization_ok | True |
| negativity_violations_zero | True |
| support_violations_zero | True |
| split_counts_9_3_2_6 | True |
| excluded_block_count_6 | True |
| p1a_accounting_closes | True |
| all_frozen_metrics_reported | True |
| no_unseen_region_claim | True |
| scientific_module_blob_matches | True |
| frozen_config_blob_matches | True |
| recovered_predictions_are_valid_share_distributions | True |
| published_metric_keys_complete | True |

## 3. Durable attempt ledger

`reports/dlh_wl_p2c_2026_09_19/DLH_WL_P2C_ATTEMPT_LEDGER.jsonl` — 24 records (12 `FIT_ATTEMPT_STARTED`, 12 `FIT_COMPLETED`, 0 `FIT_FAILED`).

| # | fit key | kind | family | regime | seed | repeats | predictions | payload SHA-256 |
|---|---|---|---|---|---|---|---|---|
| 5 | `S0:neural:seed0` | primary | neural | S0 | 0 | — | 4x5x5 | `98B1A0F606D394DC…` |
| 11 | `S0:neural:seed0:repeat` | verification_repeat | neural | S0 | 0 | S0:neural:seed0 | 4x5x5 | `722D730595ECBC11…` |
| 6 | `S0:neural:seed1` | primary | neural | S0 | 1 | — | 4x5x5 | `B9EB5CEB64676B4C…` |
| 7 | `S0:neural:seed2` | primary | neural | S0 | 2 | — | 4x5x5 | `F6C618EFF652833C…` |
| 1 | `S0:parametric` | primary | parametric | S0 | — | — | 4x5x5 | `736EA69E3544E80C…` |
| 3 | `S0:parametric:repeat` | verification_repeat | parametric | S0 | — | S0:parametric | 4x5x5 | `F65E41A8862EE85A…` |
| 8 | `S1:neural:seed0` | primary | neural | S1 | 0 | — | 4x5x5 | `AA00E2343BC7199A…` |
| 12 | `S1:neural:seed0:repeat` | verification_repeat | neural | S1 | 0 | S1:neural:seed0 | 4x5x5 | `EC0F902074E91D42…` |
| 9 | `S1:neural:seed1` | primary | neural | S1 | 1 | — | 4x5x5 | `8B4D30F89AC38A6D…` |
| 10 | `S1:neural:seed2` | primary | neural | S1 | 2 | — | 4x5x5 | `18CEC8F4AC87B92C…` |
| 2 | `S1:parametric` | primary | parametric | S1 | — | — | 4x5x5 | `5FA4211EB6972571…` |
| 4 | `S1:parametric:repeat` | verification_repeat | parametric | S1 | — | S1:parametric | 4x5x5 | `BD8EE7F23D5A99BA…` |

Recovery contract:

```
metrics_store_shape : {fit_key: {'metrics': {split: metrics}}}
fixed_store_shape   : {regime: {'metrics': {split: metrics}}}
producer            : aggregate_metrics / fixed_baseline_metrics
consumer            : constraint_diagnostics
shape asserted      : True
```

## 4. Observed results

| regime | family | seed | TEST weighted CE | TEST mean abs share error | TEST row-norm max | neg | support | top-1 | VALIDATION CE | best step |
|---|---|---|---|---|---|---|---|---|---|---|
| S0 | fixed | — | 1.098612 | 0.193032 | 0 | 0 | 0 | 0.000 | 1.386294 | — |
| S0 | parametric | — | 0.912172 | 0.000007 | 0 | 0 | 0 | 1.000 | 1.293232 | — |
| S0 | neural | 0 | 1.026776 | 0.152050 | 0 | 0 | 0 | 1.000 | 1.320267 | 350 |
| S0 | neural | 1 | 0.960684 | 0.098318 | 0 | 0 | 0 | 1.000 | 1.328222 | 300 |
| S0 | neural | 2 | 1.019407 | 0.147581 | 1.11e-16 | 0 | 0 | 1.000 | 1.323123 | 400 |
| S1 | fixed | — | 1.098612 | 0.195050 | 0 | 0 | 0 | 0.000 | 1.386294 | — |
| S1 | parametric | — | 0.908159 | 0.001667 | 0 | 0 | 0 | 1.000 | 1.293358 | — |
| S1 | neural | 0 | 1.027022 | 0.154902 | 0 | 0 | 0 | 1.000 | 1.321399 | 350 |
| S1 | neural | 1 | 0.957121 | 0.098468 | 1.11e-16 | 0 | 0 | 1.000 | 1.327840 | 300 |
| S1 | neural | 2 | 1.011269 | 0.144927 | 1.11e-16 | 0 | 0 | 1.000 | 1.321144 | 400 |

Parametric fitted coefficients (six contrast-identifiable columns, frozen order):

```
S0: [1.394641287, 0.786802152, -1.200001084, 0.299999124, -0.399800023, -1.2585e-05]
S1: [1.949170908, 1.097838037, -1.191325891, 0.312346934, -0.410780273, 0.058408132]
```

`EXCLUDED_REFERENCE_ONLY` and `TRAIN` metrics are reported in `DLH_WL_P2C_RESULTS.json` under `metrics_by_split` for every fit key.

## 5. Determinism (persisted predictions only)

```
parametric_S0: deviation=0.000e+00, coefficient_deviation=0.000e+00 | primary=S0:parametric repeat=S0:parametric:repeat
parametric_S1: deviation=0.000e+00, coefficient_deviation=0.000e+00 | primary=S1:parametric repeat=S1:parametric:repeat
neural_S0_seed0: deviation=0.000e+00 | primary=S0:neural:seed0 repeat=S0:neural:seed0:repeat
neural_S1_seed0: deviation=0.000e+00 | primary=S1:neural:seed0 repeat=S1:neural:seed0:repeat
determinism_tolerance=1e-12
max_deviation=0.000e+00
all_within_tolerance=True
scope=TWO_PARAMETRIC_REPEATS_AND_NEURAL_SEED0_REPEATS_ONLY; neural seeds 1 and 2 are sensitivity replications, not duplicate determinism checks
```

## 6. Constraint diagnostics

```
evaluated_prediction_sets=14
row_normalization_violation_max=2.220e-16 (tolerance 1e-10)
negativity_violation_count=0
support_violation_count=0
split_counts={'TRAIN': 9, 'VALIDATION': 3, 'TEST': 2, 'EXCLUDED_REFERENCE_ONLY': 6}
excluded_block_count=6 (expected 6)
allocation_blocks=20
```

Independent structural check of the recovery object (every recovered tensor, re-read from the ledger):

```
fits_checked=12
max_row_sum_deviation=2.220e-16 (tolerance 1e-10)
min_allowed_share=1.286482e-01
unavailable_cell_violations=0
all_valid=True
```

P1A accounting closure (accepted P1A interface, read-only):

```
max_abs_deviation=5.684e-14 (tolerance 1e-10)
conditional_choice_identified_all=True
all_rows_valid=True
closes=True
```

## 7. Neural comparison (no win requirement)

- neural-beats-parametric required: **False**
- S0: fixed 1.098612; parametric 0.912172; best neural seed1 (0.960684); neural beats parametric = False
- S1: fixed 1.098612; parametric 0.908159; best neural seed1 (0.957121); neural beats parametric = False
- negative result flag: **True**
- A neural non-gain is a valid negative scientific result under the frozen design; there is no neural-win acceptance gate. No tuning, extra seed or ad-hoc fit was performed during or after the science stage.

## 8. Audit context versus Issue #76 (not a threshold)

Provenance of the #76 observations: `READ_FROM_reports/dlh_wl_p2_2026_09_19/DLH_WL_P2_RESULTS.json`.

| configuration | Issue #76 observational | P2C observed | absolute difference |
|---|---|---|---|
| S0:parametric | 0.9121715995 | 0.9121715995 | 0.000e+00 |
| S1:parametric | 0.9081586774 | 0.9081586774 | 0.000e+00 |
| S0:neural:seed0 | 0.9132187018 | 1.0267760997 | 1.136e-01 |
| S1:neural:seed0 | 0.9093538306 | 1.0270222477 | 1.177e-01 |

- #76 terminal: `DLH_WL_P2A_OFFLINE_SYNTHETIC_PROTOTYPE__GATE_FAIL__NO_TUNING_AUTHORIZED`
- #76 execution accounting: `{"completed_fits_builder_reported_total": 48, "completed_fits_minimum_proven_total": 36, "within_attempt_ceiling": false}`
- the Issue #76 observational metrics are audit context and are NOT an acceptance threshold; P2C was not tuned to match them

## 9. Interpretation ceiling

Allowed:
- method/pipeline replication under the frozen synthetic controls
- fixed / parametric / neural comparison
- held-out-time and held-out-origin-role observations
- audit comparison with the Issue #76 observational output

Forbidden:
- empirical China claim
- annual bilateral OD data availability claim
- unseen-region claim
- causal or economic mechanism claim
- HJB/KFE/GE/household policy or welfare claim
- any tuning based on Issue #76 or P2C outcomes

## 10. Limitations

- the synthetic control is deliberately small (20 allocation blocks, 18 evaluable share cells per time slice, 72 total, 9 training blocks) and carries no economic content;
- the split holds out time and the **origin role** only: `R03`/`R04` occur as TRAIN destinations, so this is not an unseen-region test;
- the neural backend is NumPy because PyTorch is not installed; the frozen architecture and protocol are unchanged;
- neural weights are not persisted because the accepted scientific module does not expose them through `FitOutcome`; the full persisted predictions are the authoritative recovery object and are sufficient for every frozen metric;
- real annual bilateral OD label availability remains `UNRESOLVED`; nothing here speaks to Chinese interprovincial flows and no HJB/KFE/GE/household coupling was attempted;
- identity is PRE_RUN_FREEZE SHA + frozen config + environment + seeds + durable ledger + manifest + rendered metrics; the science runner and the ledger are immutable after the first optimizer step, and this renderer is strictly zero-fit so it may be rerun.

## 11. Terminal

```
DLH_WL_P2C_DURABLE_OUTPUT_REPLICATION__PASS__P2_METHOD_GATE_COMPLETE
```
