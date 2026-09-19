# DLH-WL-P2A — first offline synthetic prototype (Issue #76) — GATE FAIL evidence

## 0. Gate status (read first)

```
terminal: DLH_WL_P2A_OFFLINE_SYNTHETIC_PROTOTYPE__GATE_FAIL__NO_TUNING_AUTHORIZED
```

The run **completed**, but the pre-registered execution gate was **breached**: the
frozen `<= 13` absolute fit-attempt ceiling was exceeded by repeated `--execute`
invocations. The previously recorded PASS terminal is **struck** and no accepted P2
PASS is claimed anywhere in this artifact set.

This is a **reproducibility / protocol gate failure**. It is **not** evidence that
the neural model failed, and it is **not** a scientific rejection of the method
hypothesis.

Everything in sections 4-6 is **observational output from a protocol-gate-failed
run**. The values are preserved exactly as observed and must not be cited as a
confirmatory P2 result.

## 1. Frozen design (not chosen here)

This execution used the Issue #75 / P1B frozen design verbatim: the 5-region x
4-period synthetic universe, the frozen support, the S0/S1 generators, exactly three
baseline families (fixed support-normalized prior, six-parameter contrast-identifiable
gravity/logit MLE, small MLP pair scorer with 16/8 hidden widths), the 9/3/2/6 split,
TRAIN-only preprocessing, three neural seeds, frozen metrics and tolerances, and the
8 / 12 / <=13 / <=1800 s budget. No value was selected by the Builder after seeing
outcomes.

## 2. Execution accounting and gate breach (the decisive finding)

### 2.1 What was authorized

- 8 primary fit configurations;
- 12 planned fit executions;
- **at most 13 absolute fit attempts**;
- one engineering retry, and only for a pure infrastructure failure;
- after the first scientific fit, any code-design defect must be reported and the run
  stops unless the frozen contract permits continuation.

### 2.2 What actually happened

| `--execute` invocation | fits completed | fits retained | outcome |
|---|---|---|---|
| 1 | 12 | 0 | failed at report rendering (`KeyError: terminal`) |
| 2 | 12 | 0 | failed at manifest hash self-consistency |
| 3 | 12 | 0 | failed at raw CRLF-sensitive artifact hashing |
| 4 (published) | 12 | 12 | published |

- **Builder-reported total: 4 invocations / 48 completed fits** (builder session
  record and completion comment `5739969155`).
- **Minimum proven from durable artifacts: 36 completed fits** — the manifest
  addendum written during the final invocation records two earlier failed invocations
  with `fits_completed = 12` each, and the published `RESULTS.json` ledger contains
  the final 12.
- **Unresolved discrepancy (recorded, not guessed):** durable repository evidence
  proves 1 published invocation plus 2 earlier failed invocations (36 fits). The
  builder session record and the completion comment report 4 invocations (48 fits).
  No durable per-invocation log exists for the earlier invocations, so the 3-vs-4
  statement is preserved as an **unresolved discrepancy** rather than silently
  reconciled. The earlier `MANIFEST` text contained both numbers internally (two
  earlier failed attempts listed, plus a note naming three total executions), which
  is one of the defects this remediation corrects.

**The breach does not depend on resolving that discrepancy**: even the minimum
proven reading is 36 completed fits against a ceiling of 13, and
`within_attempt_ceiling = false`.

A completed fit remains a fit attempt even when its output is discarded. "Not
retained", "not used", "byte-identical" and "scientific outcome not consulted" do
**not** remove a fit from the pre-registered attempt ledger.

### 2.3 Retry classification (corrected)

The repeated executions were **not** the authorized infrastructure retry:

- classification: `UNAUTHORIZED_REPEATED_EXECUTION`;
- authorized infrastructure retry consumed: **0**, and it was **not applicable**;
- reason: the failures were deterministic reporting / artifact-writing / hashing code
  defects, not a pure infrastructure failure (crash/NaN) as the frozen retry clause
  requires. They must not be described as free or authorized retries.

### 2.4 Wall clock

- published run only: **1.034439 s** (ceiling 1800 s);
- **all four invocations: approximately 8.7 s, explicitly approximate** (sum of the
  four outer wall-clock measurements taken during the builder session: ~3.2 s,
  ~1.4 s, ~1.4 s, ~1.4 s). No durable per-invocation timing log exists.
- the wall-clock ceiling was never approached; the **attempt-ceiling breach is
  decisive regardless of wall clock**.

## 3. Code and baseline provenance (corrected)

| Item | Value |
|---|---|
| Issue #76 operative baseline | `fa00cdddf10f14bb55d651ff610668d1ac748234` |
| operative baseline declared inside the frozen #75 config | `4b4dc8c39d6a18b8928407308248f4020c10602c` — the P1B-era publication baseline, **not** the Issue #76 operative baseline |
| scientific run commit recorded by the manifest | `fab19a3686778eac437b12c62216f1153edc247c` (best-effort HEAD at artifact-write time) |
| final candidate | `9e4765c57bae385316e9492b11d9310de76ce185` |
| scientific module blob | `b1f2cd043605c511e4965254657d12306170609b` — **identical** at the run commit and at the final candidate |
| focused tests blob | `a6bb7a9facd5a482234b16ca5235a832d4a61f7b` — identical at both commits |
| runner blob during the published run | `8d13c150d503e34b6e4c964ee710fb15af02b32a` |
| runner blob at the final candidate | `b10939fbbc7ffa76c27f4134c59a0acbb5a16455` — **changed after the run** |

Identity evidence: `MANIFEST.json` recorded runner LF SHA-256
`8B993480CBCF245F2929DCEA52A33FC08F61A925848383AAC331D2FF8B8CE5D6` and scientific
module LF SHA-256
`C0AD7B4141C5C4DC29E03047DBD5B743874D4C076B62854577BDE57FEDD4437B` when the
published artifacts were written. The runner LF SHA-256 of the pre-remediation
committed blob `8d13c150` is exactly `8B993480CBCF…`, which confirms that the runner
used for the published run is the runner committed at `fab19a36`, while the final
candidate carries runner blob `b10939fb`. The runner change is scoped to artifact
hashing and accounting/reporting only — no scientific code path was modified and no
fit was re-run afterwards.

**The scientific execution itself happened with the working tree uncommitted**, so no
commit is independent proof that the candidate code was the executed code. The
blob-level agreement above is the strongest available evidence.

## 4. Observational metrics (preserved exactly; gate-failed run)

| regime | family | seed | TEST weighted CE | TEST mean abs share error | TEST row-norm max | neg | support | top-1 | best step |
|---|---|---|---|---|---|---|---|---|---|
| S0 | fixed | — | 1.098612 | 0.193032 | 0.0 | 0 | 0 | 0.0 | — |
| S0 | parametric | — | 0.912172 | 0.000007 | 0.0 | 0 | 0 | 1.0 | — |
| S0 | neural | 0 | 0.913219 | 0.011270 | 0.0 | 0 | 0 | 1.0 | 350 |
| S0 | neural | 1 | 0.921067 | 0.042086 | 0.0 | 0 | 0 | 1.0 | 300 |
| S0 | neural | 2 | 0.915075 | 0.020500 | 0.0 | 0 | 0 | 1.0 | 400 |
| S1 | fixed | — | 1.098612 | 0.195050 | 0.0 | 0 | 0 | 0.0 | — |
| S1 | parametric | — | 0.908159 | 0.001667 | 0.0 | 0 | 0 | 1.0 | — |
| S1 | neural | 0 | 0.909354 | 0.012946 | 0.0 | 0 | 0 | 1.0 | 350 |
| S1 | neural | 1 | 0.917621 | 0.042955 | 0.0 | 0 | 0 | 1.0 | 300 |
| S1 | neural | 2 | 0.912259 | 0.023373 | 0.0 | 0 | 0 | 1.0 | 400 |

VALIDATION weighted CE per configuration: parametric `1.293232` (S0) / `1.293358`
(S1); neural seed 0/1/2 `1.293320 / 1.293274 / 1.293303` (S0) and
`1.293449 / 1.293397 / 1.293429` (S1). TRAIN and `EXCLUDED_REFERENCE_ONLY` metrics
are recorded per configuration in `RESULTS.json`; the six excluded blocks were never
used for fitting, early stopping or final metrics.

Parametric fitted coefficients (six contrast-identifiable columns, frozen order):

```
S0: [1.394641287, 0.786802152, -1.200001084, 0.299999124, -0.399800023, -1.2585e-05]
S1: [1.949170908, 1.097838037, -1.191325891, 0.312346934, -0.410780273, 0.058408132]
```

## 5. Determinism and constraint diagnostics (observational)

```
parametric_S0      deviation = 0.0   (repeat objective identical, coefficient deviation 0.0)
parametric_S1      deviation = 0.0   (repeat objective identical, coefficient deviation 0.0)
neural_S0_seed0    deviation = 0.0   (repeat best step 350, validation loss identical)
neural_S1_seed0    deviation = 0.0   (repeat best step 350, validation loss identical)
row_normalization_violation_max = 2.220446049250313e-16   (tolerance 1e-10)
negativity_violation_count      = 0
support_violation_count         = 0
split_counts                    = {TRAIN 9, VALIDATION 3, TEST 2, EXCLUDED_REFERENCE_ONLY 6}, sum 20
excluded_block_count            = 6 (expected 6)
determinism tolerance           = 1e-12
```

P1A accounting closes on the generated targets at every time slice
(origin/national/destination deviations `<= 1.5e-14`, 5 active rows, 5 valid rows,
`conditional_choice_identified = true` for both regimes).

These diagnostics describe **the published invocation**, which is only 12 of the
minimum-proven 36 completed fits; they do not cure the attempt-ceiling breach.

## 6. Negative result (observation only)

```
S0: parametric 0.912172  vs best neural (seed 0) 0.913219  -> neural_beats_parametric = false
S1: parametric 0.908159  vs best neural (seed 0) 0.909354  -> neural_beats_parametric = false
```

The neural mapping did not beat the parametric baseline on either regime under the
frozen configuration. This remains a **valid negative observation**, and there is
still **no** neural-beats-parametric acceptance gate. However, because the execution
gate failed, **no confirmatory P2 PASS inference may be drawn** from this execution,
and the non-gain must not be cited as a confirmatory method result.

## 7. Interpretation ceiling

Allowed: method/pipeline observations for the frozen synthetic controls from a
gate-failed run; comparison of the three baseline families on S0/S1; held-out-time and
held-out-origin-role observations.

Forbidden and not claimed: empirical China claim; annual OD data availability claim;
unseen-region claim (`R03`/`R04` occur as TRAIN destinations); causal or
economic-mechanism claim; HANK policy or welfare claim; household or GE coupling
claim; **citing this execution as an accepted P2 PASS**; **citing the neural non-gain
as a confirmatory method result**.

## 8. Limitations

- the synthetic control is deliberately small (20 allocation blocks, 18 evaluable
  share cells per time slice, 72 total, 9 training blocks) and carries no economic
  content;
- the split holds out time and the **origin role** only: `R03`/`R04` occur as TRAIN
  destinations, so this is not an unseen-region test;
- the neural backend is NumPy because PyTorch is not installed; the frozen
  architecture and protocol were unchanged;
- real annual bilateral OD label availability remains `UNRESOLVED`; nothing here
  speaks to Chinese interprovincial flows and no HJB/KFE/GE/household coupling was
  attempted;
- the earlier `--execute` invocations left no durable per-invocation log, which is why
  the fits total is reported as a minimum-proven figure plus a builder-reported figure
  with the discrepancy explicitly preserved;
- no checkpoint artifact is produced: identity is code blob + frozen config +
  environment + seeds + manifest + metrics.

## 9. Remediation statement (evidence only)

This revision modifies **only** the runner script and the three Issue #76 report
artifacts. It performed **zero** `--execute` invocations, **zero** optimizer steps,
**zero** new fits/repeats/seeds, **zero** tuning, **zero** new scientific metrics, and
made no real-data, HJB, KFE, GE or MATLAB call. All observed metric values are
preserved exactly as published; only the accounting, provenance and terminal
classification changed.

## 10. Terminal

```
DLH_WL_P2A_OFFLINE_SYNTHETIC_PROTOTYPE__GATE_FAIL__NO_TUNING_AUTHORIZED
```
