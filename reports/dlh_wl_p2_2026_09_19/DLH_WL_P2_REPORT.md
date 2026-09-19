# DLH-WL-P2A — first offline synthetic prototype (Issue #76) results

## 1. Frozen design (not chosen here)

This run executes the Issue #75 / P1B frozen design verbatim: the 5-region x 4-period synthetic universe, the frozen support, the S0/S1 generators, exactly three baseline families (fixed support-normalized prior, six-parameter contrast-identifiable gravity/logit MLE, small MLP pair scorer with 16/8 hidden widths), the 9/3/2/6 split, TRAIN-only preprocessing, three neural seeds, frozen metrics and tolerances, and the 8 / 12 / <=13 / <=1800 s budget. No value was selected by the Builder.

## 2. Observed results

- experiment id: `EXP-20260919-DLH-WL-P2A-001`
- branch: `dsh/issue-76-dlh-wl-p2a-offline-synthetic-prototype-2026-09-19`  commit: `fab19a3686778eac437b12c62216f1153edc247c`
- frozen config: `bb5dbbd0746e9d92874f94b03a1d54f3d382c4a8` / `B4728EC1DB71D682D9C0DD96B17B039FCB7BFDCCDFFB0803FABDB216DFA60FD4`
- total P2 scientific wall clock: **1.034 s** (ceiling 1800 s)
- planned executions: 12; attempts logged: 12; engineering retries: 0

| regime | family | seed | TEST weighted cross entropy | TEST mean abs share error | TEST row-norm max | steps | validation checkpoint |
|---|---|---|---|---|---|---|---|
| S0 | neural | 0 | 0.913219 | 0.0112704 | 0 | 350 | 1.29332 |
| S0 | neural | 1 | 0.921067 | 0.0420859 | 0 | 300 | 1.29327 |
| S0 | neural | 2 | 0.915075 | 0.0205 | 0 | 400 | 1.2933 |
| S0 | parametric | — | 0.912172 | 6.90538e-06 | 0 | — | — |
| S1 | neural | 0 | 0.909354 | 0.0129464 | 0 | 350 | 1.29345 |
| S1 | neural | 1 | 0.917621 | 0.0429546 | 0 | 300 | 1.2934 |
| S1 | neural | 2 | 0.912259 | 0.0233732 | 0 | 400 | 1.29343 |
| S1 | parametric | — | 0.908159 | 0.00166657 | 0 | — | — |
| S0 | fixed | — | 1.09861 | 0.193032 | 0 | — | — |
| S1 | fixed | — | 1.09861 | 0.19505 | 0 | — | — |

Parametric fitted coefficients (six contrast-identifiable columns, frozen order):

```
S0:parametric: [1.394641287, 0.786802152, -1.200001084, 0.299999124, -0.399800023, -1.2585e-05]
S1:parametric: [1.949170908, 1.097838037, -1.191325891, 0.312346934, -0.410780273, 0.058408132]
```

## 3. Execution ledger

| # | kind | regime | family | seed |
|---|---|---|---|---|
| 1 | primary | S0 | parametric | None |
| 2 | primary | S1 | parametric | None |
| 3 | verification_repeat | S0 | parametric | None |
| 4 | verification_repeat | S1 | parametric | None |
| 5 | primary | S0 | neural | 0 |
| 6 | primary | S0 | neural | 1 |
| 7 | primary | S0 | neural | 2 |
| 8 | primary | S1 | neural | 0 |
| 9 | primary | S1 | neural | 1 |
| 10 | primary | S1 | neural | 2 |
| 11 | verification_repeat | S0 | neural | 0 |
| 12 | verification_repeat | S1 | neural | 0 |

## 4. Determinism and constraint diagnostics

```
parametric_S0: deviation=0.000e+00 (tolerance 1e-12)
parametric_S1: deviation=0.000e+00 (tolerance 1e-12)
neural_S0_seed0: deviation=0.000e+00 (tolerance 1e-12)
neural_S1_seed0: deviation=0.000e+00 (tolerance 1e-12)
row_normalization_violation_max=2.220e-16 (tolerance 1e-10)
negativity_violation_count=0
support_violation_count=0
split_counts={'TRAIN': 9, 'VALIDATION': 3, 'TEST': 2, 'EXCLUDED_REFERENCE_ONLY': 6}
```

## 5. Negative result (if present)

- neural-beats-parametric required: **False**
- S0: parametric TEST CE = 0.912172; best neural seed = S0:neural:seed0; neural beats parametric = False
- S1: parametric TEST CE = 0.908159; best neural seed = S1:neural:seed0; neural beats parametric = False
- negative result flag: **True**
- A neural non-gain is a valid negative scientific result; the frozen design is unchanged and no tuning, extra seeds or ad-hoc comparison fits were performed.

## 6. Interpretation and claim ceiling

Allowed:
- method and pipeline validation statements for the frozen synthetic controls
- comparison of the three baseline families on S0 and S1
- held-out-time and held-out-origin-role observations

Forbidden:
- empirical claim about China
- annual OD data availability claim
- unseen-region claim
- causal or economic mechanism claim
- HANK policy or welfare claim
- household or GE coupling claim

## 7. Limitations

- the synthetic control is deliberately small (20 allocation blocks, 18 evaluable share cells per time slice, 72 total) and carries no economic content;
- the split holds out time and the **origin role** only: `R03`/`R04` occur as TRAIN destinations, so this is not an unseen-region test;
- the neural backend is NumPy because PyTorch is not installed in this environment; the frozen architecture and protocol are unchanged;
- real annual bilateral OD label availability remains `UNRESOLVED`; nothing here speaks to Chinese interprovincial flows, and no HJB/KFE/GE/household coupling was attempted;
- no checkpoint artifact is produced: identity is code commit + frozen config + environment + seeds + manifest + metrics.

## 8. Terminal

```
DLH_WL_P2A_OFFLINE_SYNTHETIC_PROTOTYPE__PASS__RESULT_INTERPRETABLE
```
