# DLH-WL-P2 — first offline prototype contract (method-only, synthetic controls)

Issue: **#75 / `DLH-WL-P1B`** (this contract is produced *by* P1B and is *executed*
only by a later activated P2 Issue).
Owner route: `DLH-WL-V1-20260918`.
Authority marker: `DLH_WL_P1B_DATA_SCHEMA_AND_P2_CONTRACT_AUTHORIZED`.
Reviewer final activation comment: **`5731890746`**.
Reviewer HOLD remediated by this revision: **`5738867875`**.
Operative baseline: **`4b4dc8c39d6a18b8928407308248f4020c10602c`**.
Machine-readable twin: `configs/dlh_wl_p2_offline_prototype.toml`.
Status: **frozen design; not executed.** No training ran in P1B.

**This experiment is method-only.** It validates that the pipeline, baselines,
masking, normalization, split and reproducibility harness behave correctly on a
known data-generating process. It is **not** an empirical China estimate and makes
**no** data-availability claim.

---

## 1. Frozen universe and accounting frame

| Quantity | Frozen value |
|---|---|
| regions `R` | `5`, ids `R00..R04`, dictionary `DLH_WL_REGION_DICT_V1_2026_09_18` |
| time points `T` | `4`, ids `1..4` |
| allocation blocks | `R × T = 20` |
| nominal foreign cells per block | `R - 1 = 4` |
| actual foreign cells per block | `[4, 4, 4, 3, 3]` (the diagonal is never allowed, and two pairs are blocked) |
| blocked foreign cells | `2` (see support rule) |
| **evaluable share cells per time slice** | **`18`** = `4 + 4 + 4 + 3 + 3` across all five origins in one time slice |
| **evaluable share cells total** | **`18 × 4 time slices = 72`** |
| uniform share scale (nominal) | `1 / (R - 1) = 0.25`; the realised per-block scale is `1 / available_count(i)`, i.e. `1/4` or `1/3` |
| training horizon | the problem is deliberately small per the Issue instruction |

Only **8 of the 20 blocks** are usable for fitting/early stopping/final metrics
(see §5); the remaining blocks are `EXCLUDED_REFERENCE_ONLY` and may still be
generated for deterministic reference and arithmetic checks.

Accounting frame (identical to the accepted P1A interface):
`P_ii,t = 1 - m_i,t`, `P_ij,t = m_i,t W^L_ij,t`, `F_ij,t = ell_i,t P_ij,t`,
`Ldest_j,t = sum_i F_ij,t`, shares on the diagonal `W_ii,t = 0`, foreign row sums
`= 1` over allowed destinations.

### 1.1 Frozen deterministic inputs

Region index `i = 0..4`, time index `t = 0..3` (reported as `1..4`).

```
DIST[i][j]   = |i - j|
GDP[t][i]    = 10.0 + 0.2*i + 0.05*t
WAGE[t][i]   = 9.0 + 0.10*i + 0.08*t          (NOT proportional to GDP)
URB[t][i]    = 0.55 + 0.05*i + 0.01*t
W_IJ[i][j]   = [0.80, 0.50, 0.30, 0.10, 0.05][j]
ELL[t][i]    = [100, 80, 120, 60, 90][i] * (1 + 0.02*t)
m[t][i]      = [0.10, 0.12, 0.08, 0.14, 0.09][i] + 0.01*t + [0.02, -0.01, 0.03, 0.00, -0.02][i]
ACCESS[t][i] = sum_k GDP[t][k] / (1 + DIST[i][k])
```

The wage process is deliberately **not** proportional to GDP: with
`WAGE = 0.90 * GDP` the declared parametric design matrix is rank-deficient
(`log_wage_gap` becomes collinear with the log-GDP features), which would make the
parametric coefficients unidentified and the "correctly specified" claim
unfalsifiable. The independent wage process restores full column rank.

Resulting declared ranges (static check, see §11): `m ∈ [0.07, 0.17]`,
`ell ∈ [60.0, 127.2]`.

`m` and `ell` are **given inputs**. They are never learning targets and never
features.

### 1.2 Frozen support rule

```
available(i, j) = (i != j) and not (i in {3, 4} and j == 2)
```

| Origin | Available foreign destinations | Count |
|---|---|---|
| `R00` | `R01 R02 R03 R04` | 4 |
| `R01` | `R00 R02 R03 R04` | 4 |
| `R02` | `R00 R01 R03 R04` | 4 |
| `R03` | `R00 R01 R04` | 3 |
| `R04` | `R00 R01 R03` | 3 |

**Conditional-support diagonal**: `support_mask_ii = false` always for the `W^L`
object; the own region is never an allowed foreign destination, and home retention
is represented only by `P_ii = 1 - m_i`, never by the W support mask.

Every block has `m_i > 0`, `ell_i > 0`, at least one available foreign
destination and a valid normalized conditional row, so all 20 blocks satisfy
`block_valid_row = true` and `identifiable_conditional_target = true`; every block
also has `available_foreign_destination_count >= 2`, so
`conditional_choice_identified = true`. The blocked cells are
`STRUCTURAL_ZERO` with reason `SYNTHETIC_PAIR_UNAVAILABLE` — they are *not*
observed zeros and must not be deleted or re-added after seeing results.

### 1.3 Frozen feature list (identical for S0 and S1)

Declared parametric baseline vocabulary (the design space that S0 must live in):

```
1. log_gdp_dest           = log(GDP[t][j])
2. log_gdp_origin         = log(GDP[t][i])
3. log_wage_gap           = log(WAGE[t][j]) - log(WAGE[t][i])
4. log_adj_distance       = log1p(DIST[i][j])
5. adjacency              = 1{DIST[i][j] == 1}
6. log_accessibility_dest = log(ACCESS[t][j])
7. w_ij                   = W_IJ[i][j]                      (static)
8. per-origin destination intercept (block-additive in the softmax)
```

Pair features (`X_pair_ij_t`, order fixed) are the first six entries above.
Node features (`X_node_i_t`, order fixed): `log_gdp_pc`, `log_wage`,
`log_accessibility`, `urbanization`.
Time features (`X_time_t`): `t_normalized = t / (T - 1)`.
Static weight feature: `w_ij`.

Availability: every feature is available at prediction time; `feature_availability_time`
is `T0_STATIC` / `T-1` per the schema, `leakage_flags = []`. No feature uses the
label, the same-period realized flow, or the held-out test region.

---

## 2. Regime S0 — parametric control (nested by construction)

S0 uses an **exact linear combination of the declared parametric baseline
vocabulary**, with no raw levels and no non-vocabulary transform:

```
s0_ij,t = 1.50*log_gdp_dest + (-0.80)*log_gdp_origin + 0.60*log_wage_gap
          + (-1.20)*log_adj_distance + 0.30*adjacency + (-0.40)*log_accessibility_dest
W_ij,t  = softmax_{k available(i,·)} s0_ik,t
```

Frozen coefficients: `log_gdp_dest = 1.50`, `log_gdp_origin = -0.80`,
`log_wage_gap = 0.60`, `log_adj_distance = -1.20`, `adjacency = 0.30`,
`log_accessibility_dest = -0.40`. **No random term** (`noise_sigma = 0.0`). Realized
flows are then computed through the accepted P1A accounting (`F = ell * P`), so
origin and national conservation hold by construction.

Purpose: the low-dimensional parametric baseline family is genuinely nested by
construction, so the pipeline must not require a neural model to win. The nesting
is verified statically, not asserted (§11 and G1 below).

Representability (conditional logits up to block-additive constants, i.e. the
softmax invariance of the masked per-origin row):

```
6 declared pair features + per-origin destination intercepts -> 6 x 20 + 20 columns, rank 6 for the feature block
S0 residual, features only                : max abs 2.220446049250313e-15   (numerical precision)
S0 residual, with block intercepts        : max abs 1.554312234475219e-14   (numerical precision)
S0 block-centred residual                 : max abs 1.1102230246251565e-15  (numerical precision)
```

Because S0 is inside the span, the weighted MLE of the parametric family has the
true coefficient vector as its (unique) optimum, so S0 is a correctly specified
control case and must not lose systematically.

Reference values (static arithmetic, §11):

```
R00, time_id 1: [0.477725159, 0.221843778, 0.164194930, 0.136236133] on R01 R02 R03 R04
R00, time_id 4: [0.477966319, 0.221836852, 0.164104853, 0.136091976]
R04, time_id 1: [0.152928167, 0.196744187, 0.650327646]              on R00 R01 R03
R04, time_id 4: [0.153106303, 0.196861942, 0.650031755]
every vector sums to 1.000000000000
```

S0 has **small deterministic time variation** (`conditional_shares_time_invariant =
false`): `~2.4e-4` absolute change between `time_id 1` and `time_id 4`. The shares
are not exactly time-invariant because the wage process grows differently from GDP.

## 3. Regime S1 — bounded nonlinear case

S1 is the **corrected S0 core** plus exactly two pre-registered nonlinear
interactions built from the same declared features:

```
core      = the S0 score above (identical coefficients, no other change)
block_mean_k f(·,k) over allowed foreign destinations k of the origin's block
X2[i][j]  = ( log1p(DIST[i][j]) - block_mean_k log1p(DIST[i][k]) )^2
X3[i][j]  = max(0, DIST[i][j] - D_STAR) * ( log(GDP[t][j]) - block_mean_k log(GDP[t][k]) )
s1_ij,t   = core_ij,t + BETA_SQ * X2[i][j] + BETA_RELU * X3[i][j]
```

Frozen nonlinear coefficients: `BETA_SQ = 0.05`, `BETA_RELU = 0.15`, `D_STAR = 1.0`.
Both terms are within-block centred, so they cannot be absorbed by the
block-additive constants of the softmax.

Non-nestability is pre-registered and checked statically against **that same actual
design space** (§11, G2): regressing `S1`, `X2` and `X3` on
`[6 declared pair features | per-origin intercepts]` leaves residuals far above
numerical precision, so neither S1 nor either interaction is representable by the
parametric baseline.

```
S1 residual, features + block intercepts : max abs 0.0056595644561093505
S1 residual, features only               : max abs 0.010014012922771653
X2 residual, features + block intercepts : max abs 0.0907191779
X3 residual, features + block intercepts : max abs 0.0314502493
residual precision floor                 : 1e-12
```

Reference values:

```
R00, time_id 1: [0.479223272, 0.219532182, 0.163400470, 0.137844076] on R01 R02 R03 R04
R00, time_id 4: [0.479478444, 0.219535648, 0.163308523, 0.137677385]
R04, time_id 1: [0.150941617, 0.194939240, 0.654119143]              on R00 R01 R03
R04, time_id 4: [0.151139135, 0.195055970, 0.653804895]
every vector sums to 1.000000000000
```

S1 likewise has **small deterministic time variation** (`conditional_shares_time_invariant
= false`, `~2.6e-4` absolute change between `time_id 1` and `time_id 4`). Neither
regime may be described as exactly time-invariant, and the machine config records
both `time_id 1` and `time_id 4` references so the normative text and the config
agree.

---

## 4. Frozen baseline family (exactly three)

| # | Family | Definition | Free parameters | Trained |
|---|---|---|---|---|
| 1 | fixed baseline | support-normalized uniform prior: `W_ij,t = 1 / available_count(i)` on allowed foreign cells, `0` on the diagonal and blocked cells | 0 | no |
| 2 | low-dimensional parametric baseline | gravity multinomial logit over the declared vocabulary: `score_ij,t = alpha_d*log_gdp_dest + alpha_o*log_gdp_origin + alpha_dw*log_wage_gap + alpha_dist*log_adj_distance + alpha_adj*adjacency + alpha_acc*log_accessibility_dest + alpha_w*w_ij + per-origin destination intercept`, masked softmax over allowed foreign cells; fitted by weighted maximum likelihood | `6 + 2 + 5 = 13` | yes |
| 3 | small neural score mapping | per-pair MLP scoring `score_ij,t = f_theta(X_pair_ij_t, X_node_i_t, X_node_j_t, X_time_t, w_ij)` followed by masked softmax over allowed foreign cells | see capacity ceiling | yes |

The parametric family's design block has 6 columns (the declared pair features, rank
6) plus 5 per-origin destination intercepts; the intercepts are block-additive and
therefore leave the masked-softmax row probabilities invariant up to a constant, so
all 20 blocks can be represented. S0 lives inside this span by construction (G1).

Capacity ceiling (hard, frozen): `input -> Linear(16) -> ReLU -> Linear(8) -> Tanh
-> Linear(1)`, i.e. **two hidden layers**, widths `16` and `8`, both `<= 32`, one
scalar output per pair. No GNN, attention, transformer, embedding bank, recurrent
layer, or end-to-end HANK component is authorized in the first P2 run. No
architecture change is permitted after observing S0/S1 outcomes.

Preprocessing: fixed declaration — neural inputs `log_gdp_dest`, `log_gdp_origin`,
`log_wage_gap`, `log_adj_distance` and `log_accessibility_dest` are z-scored with
mean and standard deviation fitted **on the training split only**; `adjacency` and
`t_normalized` are used raw; `w_ij` is used raw. Any other transformation is
forbidden.

Loss: weighted cross entropy
`L = - sum_blocks w_block * sum_{j allowed} W_ij,t * log W_hat_ij,t`,
with block weight `w_block = ell_i,t / sum ell` (normalized over training blocks
only), masked to allowed foreign cells.

---

## 5. Split, preprocessing and reproducibility

Frozen single fold (`split_policy_id = DLH_WL_P2_SPLIT_V1`) with an explicit
excluded/reference state, so the 20 universe blocks are exhausted:

| Split state | Definition | Blocks |
|---|---|---|
| `TRAIN` | `t in {1, 2, 3}` for origins `R00, R01, R02` | 9 |
| `VALIDATION` | `t = 4` for origins `R00, R01, R02` | 3 |
| `TEST` | `t = 4` for origins `R03, R04` (`split_block_id = TEST_REGION_R03_R04`) | 2 |
| `EXCLUDED_REFERENCE_ONLY` | `t in {1, 2, 3}` for origins `R03, R04` (`split_block_id = EXCLUDED_REGION_R03_R04_TIMES_1_3`) | 6 |
| **total** | every block carries exactly one state | **20** |

`EXCLUDED_REFERENCE_ONLY` semantics (normative): these six blocks may be generated
for deterministic reference-share checks and arithmetic integrity checks, but they
are **never** used for fitting, for early stopping, or for final test metrics. They
are not moved into `TRAIN`, because that would destroy the intended region holdout;
and they are not test blocks, because they share both time and regions with
training. P2 must report the excluded-block count explicitly (expected `6`).

Blocked structure is deliberate: the test split holds out **both** a later time
point and two entire regions, so no training block shares either its time or its
regions with the test split. Region-based and time-based generalization are
therefore both probed without a hyper-parameter search. Preprocessing statistics
are fitted on `TRAIN` only; validation is used solely for the frozen early-stop
rule; the test split is used **once** after the final checkpoint and may never
inform any choice.

Reproducibility declarations:

- `torch.manual_seed`, `numpy.random.seed` and Python `random` set to each
  declared seed at fit start; `torch.use_deterministic_algorithms(True)`;
  deterministic data order; full-batch optimization (no shuffling);
- seeds: `NEURAL_SEEDS = [0, 1, 2]` (fixed list); the parametric MLE is
  deterministic and uses no seed; the fixed baseline uses no seed;
- determinism verification applies to **four** configurations only: both parametric
  fits (S0, S1) and the neural seed-0 fits in both regimes. Seeds 1 and 2 are
  **sensitivity replications**, not duplicate determinism checks, and are not
  repeated;
- repeated diagnostics for the verification configurations must match bitwise or to
  `<= 1e-12`;
- no hyper-parameter sweep, no seed search, no architecture change after seeing
  outcomes.

---

## 6. Metrics (pre-registered)

Primary (computed on `TEST`, secondary copy on `VALIDATION`):

| Metric | Definition |
|---|---|
| `weighted_cross_entropy` | `- sum_blocks w_block sum_j W log W_hat`, `w_block = ell_i,t` normalized over the reported split using **observed** `ell` |
| `mean_absolute_share_error` | `sum_blocks sum_j abs(W_hat - W) / (number of evaluated foreign cells)` |
| `row_normalization_violation_max` | `max_blocks abs(sum_{j allowed} W_hat - 1)` |
| `negativity_violation_count` | count of `W_hat < 0` entries |
| `support_violation_count` | count of `abs(W_hat) > 0` entries on the diagonal or on `STRUCTURAL_ZERO` cells |
| `determinism_deviation` | max absolute difference between the identical-config repeats of the four determinism verification configurations |
| `runtime_seconds` | wall-clock seconds of one fit plus one evaluation; the total across the whole run is also reported |
| `excluded_block_count` | number of `EXCLUDED_REFERENCE_ONLY` blocks in the universe (expected `6`) |

Secondary (reported, not gating):

| Metric | Definition |
|---|---|
| `top1_destination_accuracy` | share of blocks whose argmax `W_hat` equals the argmax `W` |
| `share_kl_per_block_mean` | mean KL `sum_j W log(W / W_hat)` over valid blocks |
| `cross_entropy_s0_vs_s1_delta` | per-family difference between regimes, reported without a success threshold |

Reported per family, per regime, per seed, with valid-block counts, the
excluded-block count (expected `6`) and the determinism-verification scope. No
other metric may be added after execution.

---

## 7. Acceptance philosophy (normative)

`P2 PASS` means **the bounded experiment executed reproducibly and the comparisons
are interpretable**:

1. all fits ran inside the frozen budget;
2. determinism deviation `<= 1e-12` for each family/seed;
3. row normalization, non-negativity and support diagnostics are at or below
   `1e-10` / `0` / `0` respectively;
4. S0 and S1 results are reported for all three families without post-hoc
   selection.

There is **no rule that the neural model must beat the parametric baseline**. In S0
a correctly specified simple baseline need not lose; in S1 the neural mapping is
tested against a pre-registered nonlinearity. A correctly reported negative result
(a neural model that does not gain) is an acceptable P2 outcome and must not be
retried with new hyper-parameters.

---

## 8. Cost ceiling for P2 (frozen, not executed in P1B)

| Ceiling | Value |
|---|---|
| wall-clock scientific training budget | **1800 s (30 minutes)** for the whole run, covering primary fits **plus** verification repeats **plus** any engineering retry; no per-regime extension |
| **primary fit configurations** | **8** = 2 parametric MLE configurations (S0, S1) + 6 neural configurations (`NEURAL_SEEDS = [0, 1, 2]` × 2 regimes); the fixed baseline is not fitted |
| **planned fit executions** | **12** = the 8 primary configurations + 2 deterministic repeats of the parametric fits + 2 deterministic repeats of the neural seed-0 fits (one per regime) |
| **absolute attempt ceiling** | **13** = 12 planned executions + at most 1 engineering retry |
| determinism verification scope | the 2 parametric repeats and the 2 neural seed-0 repeats only (4 verification executions) |
| sensitivity replications | neural seeds 1 and 2 in each regime are sensitivity replications, **not** duplicate determinism checks, and are not repeated |
| early stopping | `max_steps = 1500`, `eval_every = 50` steps, `early_stop_patience = 200` steps, `min_delta = 1e-4` on validation weighted cross entropy |
| optimizer | Adam, `lr = 0.01`, full batch, no schedule |
| hyper-parameter / seed search | **none** (`0` search executions) |
| automatic retries | **none**, except **one** deterministic re-run of the identical config and seed permitted for a pure engineering failure (crash/NaN from infrastructure), with both attempts logged |
| budget exhaustion | stops the experiment immediately; no successor Issue is created automatically |

Run accounting must be explicit and must satisfy
`8 primary configurations / 12 planned executions / <= 13 absolute attempts / <= 1800 s`.
Any ceiling breach is a Terminal B outcome, not an invitation to redefine the
experiment.


---

## 9. P2 / P3 boundary

| Aspect | P2 (this contract) | P3 |
|---|---|---|
| data | pre-registered synthetic `SYNTHETIC` regimes only | real sources with declared semantics |
| claim ceiling | method/pipeline validation; no empirical content | empirical claim, gated by label class and bridge assumptions |
| label taxonomy | `SYNTHETIC` | `TRUE_ANNUAL_OD_FLOW` or a bridged class with an explicit dated assumption |
| deciding artifact | reproducibility + interpretability of S0/S1 comparison | out-of-sample empirical performance with supported identification |

A successful P2 result may **not** be cited as evidence about Chinese
interprovincial labor flows, about the existence of a bilateral OD label set, or
about any economic mechanism. Conversely, the unresolved real-label status
(`UNRESOLVED` per DLH-1A-R1) does not block P2, because P2 uses no real labels.

---

## 10. Explicit prohibitions for the first P2 run

- no GNN / attention / transformer / recurrent / end-to-end HANK component;
- no architecture or hyper-parameter change after observing outcomes;
- no data download, scraping or purchase;
- no real-data labels, no `m`/`ell` estimation, no joint learning of `m`, `ell`,
  capital networks or local parameters;
- no HJB/KFE/GE/MATLAB execution and no household coupling;
- no `m`/`ell` feature leakage and no future-information features;
- no reporting of P2 numbers as empirical China results;
- no automatic successor Issue, no self-acceptance and no merge to `main`.

---

## 11. Static checks recorded in P1B (no training)

Deterministic arithmetic checks performed while freezing the constants
(`_tmp` scripts, deleted before commit; results reproduced in the report):

| Check | Result |
|---|---|
| `m` inside `[0,1]` | `min 0.07`, `max 0.17` |
| `ell` non-negative | `min 60.0`, `max 127.2` |
| support counts | `[4, 4, 4, 3, 3]`, all `>= 2`; diagonal always `false` |
| parametric design rank / columns | `6 / 6` (full column rank after the independent wage process) |
| **G1 S0 representability** (features only) | `max abs residual 2.220446049250313e-15` → numerical precision |
| **G1 S0 representability** (with block intercepts) | `max abs residual 1.554312234475219e-14` → numerical precision |
| **G1 S0 block-centred residual** | `1.1102230246251565e-15` → numerical precision |
| **G2 S1 non-nestability** (same design space + block constants) | `max abs residual 0.0056595644561093505` |
| **G2 X2 / X3 non-nestability** | `0.0907191779` / `0.0314502493` |
| reference-share sums | `1.000000000000` for every reference block in both regimes and both time slices |
| S0 reference shares | `R00 t1 [0.477725159, 0.221843778, 0.164194930, 0.136236133]`, `R00 t4 [0.477966319, 0.221836852, 0.164104853, 0.136091976]`; `R04 t1 [0.152928167, 0.196744187, 0.650327646]`, `R04 t4 [0.153106303, 0.196861942, 0.650031755]` |
| S1 reference shares | `R00 t1 [0.479223272, 0.219532182, 0.163400470, 0.137844076]`, `R00 t4 [0.479478444, 0.219535648, 0.163308523, 0.137677385]`; `R04 t1 [0.150941617, 0.194939240, 0.654119143]`, `R04 t4 [0.151139135, 0.195055970, 0.653804895]` |
| time variation | S0 `~2.4e-4`, S1 `~2.6e-4` absolute between `time_id 1` and `time_id 4`; **not** invariant |
| blocked-pair accounting | `R04` and `R03` have 3 allowed destinations, so their reference vectors have 3 entries |
| split exhaustiveness | `9 + 3 + 2 + 6 = 20` with every block in exactly one state |
| budget arithmetic | `8` primary configs, `12` planned executions, `13` absolute attempts, `<= 1800 s` |
| checks executed | static consistency + arithmetic checker rerun after remediation (see report) |

No training, no optimization, no data access and no scientific solver was invoked
to produce these numbers.

