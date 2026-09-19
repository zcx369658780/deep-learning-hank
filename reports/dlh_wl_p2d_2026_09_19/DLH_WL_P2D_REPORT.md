# DLH-WL-P2D — minimal preprocessing-corrected durable replication of the frozen synthetic prototype

## 0. Status

```
terminal: DLH_WL_P2D_PREPROCESSING_CORRECTED_REPLICATION__PASS__P2_METHOD_GATE_COMPLETE
```

- Issue: **#79** / `DLH_WL_P2D_PREPROCESSING_CORRECTED_REPLICATION`; route `DLH-WL-V1-20260918`
- PRE_RUN_FREEZE SHA (executed science code identity): `c557918e360298dc3ab2906a4c53a1725498481f`
- scientific module blob: `b1f2cd043605c511e4965254657d12306170609b` (MATCH)
- frozen config blob: `bb5dbbd0746e9d92874f94b03a1d54f3d382c4a8` (MATCH)
- science invocations: **1**; science retries: **0**
- fit attempts started / completed / failed: **12 / 12 / 0**
- science wall clock: **1.544039 s** (source `SCIENCE_SEAL`, ceiling 1800 s)
- render-only invocations so far: **2** (zero fits, zero optimizer steps)
- `confirmatory_p2_pass_allowed`: **True**

## 1. What P2D changes — the single authorized science-path repair

The #75 scientific design is unchanged: 5 regions x 4 periods, the frozen support, the S0/S1 generators, three baseline families (fixed support-normalized uniform, six-parameter contrast-identifiable gravity/logit MLE, small MLP pair scorer with 16/8 hidden widths under masked softmax), the 9/3/2/6 split, TRAIN-only preprocessing, neural seeds 0/1/2, the frozen metrics/tolerances, 12 planned fit executions, a 13-attempt ceiling and an 1800 s wall-clock ceiling. No S0/S1, feature, support, split, architecture, optimizer, seed, metric or tolerance changed.

The #78 durable per-fit-output protocol is retained unchanged: every completed fit persists its full 4x5x5 prediction tensor, prediction shape, coefficients when present, objective, convergence, best step, best validation loss, backend, diagnostics, runtime and a canonical scientific-payload SHA-256, with flush + fsync before the next fit may begin.

The **only** scientific execution repair of Issue #79 is:

```python
# after the TRAIN-only z-score design is built, before any neural fit
universe._design_matrix = design
```

Issue #78 omitted that assignment. ``fit_neural(..., design=design)`` optimizes on the supplied design, but the accepted module's final prediction path is ``_neural_predict -> _neural_predict_blocks -> universe.design_matrix``, and ``SyntheticUniverse.design_matrix`` silently falls back to ``raw_design`` when ``_design_matrix`` is None. In #78 the neural parameters were therefore trained on TRAIN-z-scored inputs while the persisted prediction tensors were generated from raw inputs, and the PASS terminal was struck by Reviewer adjudication 5740611528. P2D installs the design, so optimization, early stopping and the final persisted predictions all consume the same TRAIN-only z-scored array.

The runner additionally **fails closed**: it refuses to fit if the installed prediction design is not the TRAIN-only z-scored design, so the #78 defect can no longer happen silently.

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
| every_neural_fit_carries_preprocessing_contract | True |
| every_neural_contract_satisfied | True |
| all_neural_fits_covered | True |
| training_and_prediction_designs_identical_for_all_neural_fits | True |
| zscored_design_matches_frozen_recomputation | True |
| zscored_design_differs_from_raw | True |

- mechanical/durability gate subset: **True**
- overall gate: **True**
- corrected terminal: `DLH_WL_P2D_PREPROCESSING_CORRECTED_REPLICATION__PASS__P2_METHOD_GATE_COMPLETE`

## 2b. Preprocessing-design evidence (Issue #79)

Contract verification recomputes both designs from the frozen inputs — the TRAIN-only statistics are re-derived here directly from the frozen universe (``recomputation = INDEPENDENT_OF_THE_ACCEPTED_MODULE_HELPER``), not by calling the accepted module's preprocessing helper — and requires the durable evidence to match. No fit, no optimizer and no prediction is performed by this stage.

```
required assignment                     : universe._design_matrix = design
training design                         : TRAIN_ONLY_ZSCORED
prediction design                       : TRAIN_ONLY_ZSCORED
prediction path                         : _neural_predict -> _neural_predict_blocks -> universe.design_matrix
zscored design SHA-256 (recomputed)     : EC41B8DC9F55CAD14EC6F05D0C15053E73D009E0EFF9635F70519B8DAE783BDE
raw design SHA-256 (recomputed)         : C6D1AB0EE29801A10E489081D0EC4DC5E5F4D05CCD169395C586A3CBEA00836C
zscored differs from raw                : True
max |zscored - raw|                     : 4.654774451910
design shape / raw shape                : [72, 15] / [72, 15]
TRAIN rows used for the statistics      : 36
neural fits examined                    : 8
all neural fits covered                 : True
every contract present                  : True
every contract satisfied                : True
training == prediction design hash, all : True
zscored hash matches frozen recompute   : True
zscored != raw, all neural fits         : True
```

Per-fit durable evidence (from the ``FIT_COMPLETED`` records; the renderer recomputed the expected hashes independently):

| fit key | training design | prediction design | zscored design SHA-256 | pre-fit universe.design_matrix SHA-256 | equal | raw design SHA-256 | zscored != raw | contract satisfied |
|---|---|---|---|---|---|---|---|---|
| `S0:neural:seed0` | TRAIN_ONLY_ZSCORED | TRAIN_ONLY_ZSCORED | `EC41B8DC9F55CAD14EC6F05D0C15053E73D009E0EFF9635F70519B8DAE783BDE` | `EC41B8DC9F55CAD14EC6F05D0C15053E73D009E0EFF9635F70519B8DAE783BDE` | True | `C6D1AB0EE29801A10E489081D0EC4DC5E5F4D05CCD169395C586A3CBEA00836C` | True | True |
| `S0:neural:seed0:repeat` | TRAIN_ONLY_ZSCORED | TRAIN_ONLY_ZSCORED | `EC41B8DC9F55CAD14EC6F05D0C15053E73D009E0EFF9635F70519B8DAE783BDE` | `EC41B8DC9F55CAD14EC6F05D0C15053E73D009E0EFF9635F70519B8DAE783BDE` | True | `C6D1AB0EE29801A10E489081D0EC4DC5E5F4D05CCD169395C586A3CBEA00836C` | True | True |
| `S0:neural:seed1` | TRAIN_ONLY_ZSCORED | TRAIN_ONLY_ZSCORED | `EC41B8DC9F55CAD14EC6F05D0C15053E73D009E0EFF9635F70519B8DAE783BDE` | `EC41B8DC9F55CAD14EC6F05D0C15053E73D009E0EFF9635F70519B8DAE783BDE` | True | `C6D1AB0EE29801A10E489081D0EC4DC5E5F4D05CCD169395C586A3CBEA00836C` | True | True |
| `S0:neural:seed2` | TRAIN_ONLY_ZSCORED | TRAIN_ONLY_ZSCORED | `EC41B8DC9F55CAD14EC6F05D0C15053E73D009E0EFF9635F70519B8DAE783BDE` | `EC41B8DC9F55CAD14EC6F05D0C15053E73D009E0EFF9635F70519B8DAE783BDE` | True | `C6D1AB0EE29801A10E489081D0EC4DC5E5F4D05CCD169395C586A3CBEA00836C` | True | True |
| `S1:neural:seed0` | TRAIN_ONLY_ZSCORED | TRAIN_ONLY_ZSCORED | `EC41B8DC9F55CAD14EC6F05D0C15053E73D009E0EFF9635F70519B8DAE783BDE` | `EC41B8DC9F55CAD14EC6F05D0C15053E73D009E0EFF9635F70519B8DAE783BDE` | True | `C6D1AB0EE29801A10E489081D0EC4DC5E5F4D05CCD169395C586A3CBEA00836C` | True | True |
| `S1:neural:seed0:repeat` | TRAIN_ONLY_ZSCORED | TRAIN_ONLY_ZSCORED | `EC41B8DC9F55CAD14EC6F05D0C15053E73D009E0EFF9635F70519B8DAE783BDE` | `EC41B8DC9F55CAD14EC6F05D0C15053E73D009E0EFF9635F70519B8DAE783BDE` | True | `C6D1AB0EE29801A10E489081D0EC4DC5E5F4D05CCD169395C586A3CBEA00836C` | True | True |
| `S1:neural:seed1` | TRAIN_ONLY_ZSCORED | TRAIN_ONLY_ZSCORED | `EC41B8DC9F55CAD14EC6F05D0C15053E73D009E0EFF9635F70519B8DAE783BDE` | `EC41B8DC9F55CAD14EC6F05D0C15053E73D009E0EFF9635F70519B8DAE783BDE` | True | `C6D1AB0EE29801A10E489081D0EC4DC5E5F4D05CCD169395C586A3CBEA00836C` | True | True |
| `S1:neural:seed2` | TRAIN_ONLY_ZSCORED | TRAIN_ONLY_ZSCORED | `EC41B8DC9F55CAD14EC6F05D0C15053E73D009E0EFF9635F70519B8DAE783BDE` | `EC41B8DC9F55CAD14EC6F05D0C15053E73D009E0EFF9635F70519B8DAE783BDE` | True | `C6D1AB0EE29801A10E489081D0EC4DC5E5F4D05CCD169395C586A3CBEA00836C` | True | True |

Issue #78 contrast: Issue #78 persisted no preprocessing evidence and generated its prediction tensors from the raw-design fallback because the runner omitted universe._design_matrix = design. That omission is repaired in P2D and this check would fail loudly on any record that cannot prove the corrected path.

## 3. Durable attempt ledger

`reports/dlh_wl_p2d_2026_09_19/DLH_WL_P2D_ATTEMPT_LEDGER.jsonl` — 24 records (12 `FIT_ATTEMPT_STARTED`, 12 `FIT_COMPLETED`, 0 `FIT_FAILED`).

| # | fit key | kind | family | regime | seed | repeats | predictions | payload SHA-256 |
|---|---|---|---|---|---|---|---|---|
| 5 | `S0:neural:seed0` | primary | neural | S0 | 0 | — | 4x5x5 | `806D1370199FFD3D…` |
| 11 | `S0:neural:seed0:repeat` | verification_repeat | neural | S0 | 0 | S0:neural:seed0 | 4x5x5 | `37E40B399FC1EA13…` |
| 6 | `S0:neural:seed1` | primary | neural | S0 | 1 | — | 4x5x5 | `A47DCB9C324BCE21…` |
| 7 | `S0:neural:seed2` | primary | neural | S0 | 2 | — | 4x5x5 | `801EF58F55E3A12F…` |
| 1 | `S0:parametric` | primary | parametric | S0 | — | — | 4x5x5 | `C235AF66ED11CAA9…` |
| 3 | `S0:parametric:repeat` | verification_repeat | parametric | S0 | — | S0:parametric | 4x5x5 | `E7B6BE1195E253F9…` |
| 8 | `S1:neural:seed0` | primary | neural | S1 | 0 | — | 4x5x5 | `07BCF1C83E0765B1…` |
| 12 | `S1:neural:seed0:repeat` | verification_repeat | neural | S1 | 0 | S1:neural:seed0 | 4x5x5 | `5377D176B7002A81…` |
| 9 | `S1:neural:seed1` | primary | neural | S1 | 1 | — | 4x5x5 | `247C3976BAB50392…` |
| 10 | `S1:neural:seed2` | primary | neural | S1 | 2 | — | 4x5x5 | `8B9B1309FC59C1DF…` |
| 2 | `S1:parametric` | primary | parametric | S1 | — | — | 4x5x5 | `5921A920B45C4A24…` |
| 4 | `S1:parametric:repeat` | verification_repeat | parametric | S1 | — | S1:parametric | 4x5x5 | `E7B2B9B9BFC229A2…` |

Recovery contract:

```
metrics_store_shape : {fit_key: {'metrics': {split: metrics}}}
fixed_store_shape   : {regime: {'metrics': {split: metrics}}}
producer            : aggregate_metrics / fixed_baseline_metrics
consumer            : constraint_diagnostics
shape asserted      : True
```

## 4. Observed results

| regime | family | seed | TEST weighted CE | TEST mean abs share error | TEST row-norm max | neg | support | top-1 | VALIDATION CE | best step | provenance |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S0 | fixed | — | 1.098612 | 0.193032 | 0 | 0 | 0 | 0.000 | 1.386294 | — | `FROZEN_DESIGN_CONFORMANT_ZERO_FIT_BASELINE` |
| S0 | parametric | — | 0.912172 | 0.000007 | 0 | 0 | 0 | 1.000 | 1.293232 | — | `FROZEN_DESIGN_CONFORMANT` |
| S0 | neural | 0 | 0.913219 | 0.011270 | 0 | 0 | 0 | 1.000 | 1.293320 | 350 | `FROZEN_DESIGN_CONFORMANT_CORRECTED_PREPROCESSING_PATH` |
| S0 | neural | 1 | 0.921067 | 0.042086 | 0 | 0 | 0 | 1.000 | 1.293274 | 300 | `FROZEN_DESIGN_CONFORMANT_CORRECTED_PREPROCESSING_PATH` |
| S0 | neural | 2 | 0.915075 | 0.020500 | 0 | 0 | 0 | 1.000 | 1.293303 | 400 | `FROZEN_DESIGN_CONFORMANT_CORRECTED_PREPROCESSING_PATH` |
| S1 | fixed | — | 1.098612 | 0.195050 | 0 | 0 | 0 | 0.000 | 1.386294 | — | `FROZEN_DESIGN_CONFORMANT_ZERO_FIT_BASELINE` |
| S1 | parametric | — | 0.908159 | 0.001667 | 0 | 0 | 0 | 1.000 | 1.293358 | — | `FROZEN_DESIGN_CONFORMANT` |
| S1 | neural | 0 | 0.909354 | 0.012946 | 0 | 0 | 0 | 1.000 | 1.293449 | 350 | `FROZEN_DESIGN_CONFORMANT_CORRECTED_PREPROCESSING_PATH` |
| S1 | neural | 1 | 0.917621 | 0.042955 | 0 | 0 | 0 | 1.000 | 1.293397 | 300 | `FROZEN_DESIGN_CONFORMANT_CORRECTED_PREPROCESSING_PATH` |
| S1 | neural | 2 | 0.912259 | 0.023373 | 0 | 0 | 0 | 1.000 | 1.293429 | 400 | `FROZEN_DESIGN_CONFORMANT_CORRECTED_PREPROCESSING_PATH` |

All three families were executed under the frozen #75 design. The neural rows are classified FROZEN_DESIGN_CONFORMANT_CORRECTED_PREPROCESSING_PATH: their prediction tensors were produced through the accepted prediction path with the TRAIN-only z-scored design installed, which the durable FIT_COMPLETED preprocessing evidence proves.

The parametric outputs were produced through the frozen contrast design and the frozen six-column fitted matrix, and reproduce the earlier frozen observations exactly.

The fixed baseline is a zero-fit evaluation of the frozen support-normalized uniform prior.

In Issue #78 the neural rows were classified OBSERVATIONAL_OUTPUT_FROM_INVALID_PREPROCESSING_PREDICTION_PATH because the prediction path used the raw design fallback. P2D installs universe._design_matrix = design before any neural fit, so the persisted tensors come from the frozen path.

Parametric fitted coefficients (six contrast-identifiable columns, frozen order):

```
S0: [1.394641287, 0.786802152, -1.200001084, 0.299999124, -0.399800023, -1.2585e-05]
S1: [1.949170908, 1.097838037, -1.191325891, 0.312346934, -0.410780273, 0.058408132]
```

`EXCLUDED_REFERENCE_ONLY` and `TRAIN` metrics are reported in `DLH_WL_P2D_RESULTS.json` under `metrics_by_split` for every fit key.

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
min_allowed_share=1.241282e-01
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

## 7. Fixed / parametric / neural comparison (no win requirement)

- neural-beats-parametric required: **False**
- neural-vs-parametric comparison permitted: **True**
- S0: fixed 1.098612; parametric 0.912172; neural by seed seed0 0.913219, seed1 0.921067, seed2 0.915075; best neural seed0; neural beats parametric = False
- S1: fixed 1.098612; parametric 0.908159; neural by seed seed0 0.909354, seed1 0.917621, seed2 0.912259; best neural seed0; neural beats parametric = False
- negative result flag: **True**
- A neural non-gain is a valid negative scientific result under the frozen design; there is no neural-win acceptance gate. No tuning, extra seed or ad-hoc fit was performed during or after the science stage. Issue #76 and Issue #78 numbers are audit context only and were never used as thresholds.

## 8. Audit context versus Issues #76 and #78 (provenance only)

- #76 provenance: `READ_FROM_reports/dlh_wl_p2_2026_09_19/DLH_WL_P2_RESULTS.json`
- #78 provenance: `READ_FROM_reports/dlh_wl_p2c_2026_09_19/DLH_WL_P2C_RESULTS.json`

| configuration | P2D observed | #76 observational | |diff| | #78 observational | |diff| | classification |
|---|---|---|---|---|---|---|
| S0:parametric | 0.9121715995 | 0.9121715995 | 0.000e+00 | 0.9121715995 | 0.000e+00 | `FROZEN_DESIGN_CONFORMANT` |
| S1:parametric | 0.9081586774 | 0.9081586774 | 0.000e+00 | 0.9081586774 | 0.000e+00 | `FROZEN_DESIGN_CONFORMANT` |
| S0:neural:seed0 | 0.9132187018 | 0.9132187018 | 0.000e+00 | 1.0267760997 | 1.136e-01 | `FROZEN_DESIGN_CONFORMANT_CORRECTED_PREPROCESSING_PATH` |
| S1:neural:seed0 | 0.9093538306 | 0.9093538306 | 0.000e+00 | 1.0270222477 | 1.177e-01 | `FROZEN_DESIGN_CONFORMANT_CORRECTED_PREPROCESSING_PATH` |

- Issue #78's neural values are GATE FAIL evidence produced through the invalid raw-design prediction path and are recorded here only as provenance; they are not a reference to reproduce and not a threshold.
- the Issue #76 and Issue #78 observations are audit context only and are NOT acceptance thresholds; P2D was not tuned to match either

## 9. Interpretation ceiling

Allowed:
- method/pipeline replication under the frozen synthetic controls
- fixed/parametric/neural comparison with no win requirement
- held-out-time and held-out-origin-role observations
- audit comparison with the Issue #76 and Issue #78 outputs as provenance context only

Forbidden:
- empirical China claim
- annual bilateral OD data availability claim
- unseen-region claim
- causal or economic mechanism claim
- HJB/KFE/GE/household policy or welfare claim
- any tuning based on Issue #76, Issue #78 or P2D outcomes

## 10. Limitations

- the synthetic control is deliberately small (20 allocation blocks, 18 evaluable share cells per time slice, 72 total, 9 training blocks) and carries no economic content;
- the split holds out time and the **origin role** only: `R03`/`R04` occur as TRAIN destinations, so this is not an unseen-region test;
- the neural backend is NumPy because PyTorch is not installed; the frozen architecture and protocol are unchanged;
- neural weights are not persisted because the accepted scientific module does not expose them through `FitOutcome`; the full persisted predictions are the authoritative recovery object, and with the corrected preprocessing path installed they are the frozen neural mapping's own output;
- real annual bilateral OD label availability remains `UNRESOLVED`; nothing here speaks to Chinese interprovincial flows and no HJB/KFE/GE/household coupling was attempted;
- identity is PRE_RUN_FREEZE SHA + frozen config + environment + seeds + durable ledger + manifest + rendered metrics; the science runner and the ledger are immutable after the first optimizer step, and this renderer is strictly zero-fit so it may be rerun.

## 11. Terminal

```
DLH_WL_P2D_PREPROCESSING_CORRECTED_REPLICATION__PASS__P2_METHOD_GATE_COMPLETE
```
