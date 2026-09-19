# DLH-WL-P2 — first offline prototype contract (method-only, synthetic controls)

Issue: **#75 / `DLH-WL-P1B`** (this contract is produced *by* P1B and is *executed*
only by a later activated P2 Issue).
Owner route: `DLH-WL-V1-20260918`.
Authority marker: `DLH_WL_P1B_DATA_SCHEMA_AND_P2_CONTRACT_AUTHORIZED`.
Reviewer final activation comment: **`5731890746`**.
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
| foreign cells per block | `R - 1 = 4` (diagonal excluded by structural rule) |
| blocked foreign cells | `2` (see support rule) |
| evaluable share cells | `18` foreign cells `× T = 72` |
| uniform share scale | `1 / (R - 1) = 0.25` per allowed foreign cell |
| training horizon | the problem is deliberately small per the Issue instruction |

Accounting frame (identical to the accepted P1A interface):
`P_ii,t = 1 - m_i,t`, `P_ij,t = m_i,t W^L_ij,t`, `F_ij,t = ell_i,t P_ij,t`,
`Ldest_j,t = sum_i F_ij,t`, shares on the diagonal `W_ii,t = 0`, foreign row sums
`= 1` over allowed destinations.

### 1.1 Frozen deterministic inputs

Region index `i = 0..4`, time index `t = 0..3` (reported as `1..4`).

```
DIST[i][j]   = |i - j|
GDP[t][i]    = 10.0 + 0.2*i + 0.05*t
WAGE[t][i]   = 0.90 * GDP[t][i]
URB[t][i]    = 0.55 + 0.05*i + 0.01*t
W_IJ[i][j]   = [0.80, 0.50, 0.30, 0.10, 0.05][j]
ELL[t][i]    = [100, 80, 120, 60, 90][i] * (1 + 0.02*t)
m[t][i]      = [0.10, 0.12, 0.08, 0.14, 0.09][i] + 0.01*t + [0.02, -0.01, 0.03, 0.00, -0.02][i]
ACCESS[t][i] = sum_k GDP[t][k] / (1 + DIST[i][k])
```

Resulting declared ranges (static check, see §11): `m ∈ [0.07, 0.17]`,
`ell ∈ [60.0, 127.2]`, `ACCESS[1][R00] = 23.376667`.

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

Every block has `m_i > 0`, `ell_i > 0`, at least one available foreign
destination and a valid normalized conditional row, so all 20 blocks satisfy
`block_valid_row = true` and `identifiable_conditional_target = true`; every block
also has `available_foreign_destination_count >= 2`, so
`conditional_choice_identified = true`. The blocked cells are
`STRUCTURAL_ZERO` with reason `SYNTHETIC_PAIR_UNAVAILABLE` — they are *not*
observed zeros and must not be deleted or re-added after seeing results.

### 1.3 Frozen feature list (identical for S0 and S1)

Pair features (`X_pair_ij_t`, order fixed):

```
1. log_distance       = log1p(DIST[i][j])
2. adjacency          = 1{DIST[i][j] == 1}
3. log_gdp_pc_gap     = log(GDP[t][j]) - log(GDP[t][i])
4. log_wage_gap       = log(WAGE[t][j]) - log(WAGE[t][i])
5. log_accessibility_dest = log(ACCESS[t][j])
```

Node features (`X_node_i_t`, order fixed): `log_gdp_pc`, `log_wage`,
`log_accessibility`, `urbanization`.
Time features (`X_time_t`): `t_normalized = t / (T - 1)`.
Static weight feature: `W_IJ[i][j]` (declared static, time-invariant).

Availability: every feature is available at prediction time; `feature_availability_time`
is `T0_STATIC` / `T-1` per the schema, `leakage_flags = []`. No feature uses the
label, the same-period realized flow, or the held-out test region.

---

## 2. Regime S0 — parametric negative/control case

Conditional destination logits for `j != i`, restricted to `available(i, j)`:

```
s0_ij,t = SIGMA * ( BETA_D * GDP[t][j] - BETA_O * GDP[t][i] - GAMMA_DIST * DIST[i][j] )
W_ij,t  = softmax_{k available(i,·)} s0_ik,t
```

Frozen coefficients: `SIGMA = 1.0`, `BETA_D = 0.30`, `BETA_O = 0.20`,
`GAMMA_DIST = 0.60`. **No random term**: S0 is deterministic (`noise_sigma = 0.0`).
Realized flows are then computed through the accepted P1A accounting
(`F = ell * P`), so origin and national conservation hold by construction.

Purpose: the low-dimensional parametric baseline is correctly specified, so the
pipeline must not require a neural model to win.

Reference values (static arithmetic, §11):

```
R00 (time_id 1): [0.471644168, 0.274849815, 0.160168249, 0.093337767] on destinations R01 R02 R03 R04
R04 (time_id 1): [0.098255616, 0.190104212, 0.711640172]              on destinations R00 R01 R03
both sum to 1.000000000000
```
## 3. Regime S1 — bounded nonlinear case

Same universe, same support, same feature list, same coefficients for the linear
part, plus exactly two pre-registered nonlinear interactions that are functions of
the same features:

```
D_MEAN[i] = (sum_{k!=i} DIST[i][k]) / (R - 1) = 2.5
U[i][j]   = (DIST[i][j] / D_MEAN[i]) * (GDP[t][j] - mean_k GDP[t][k])
X2[i][j]  = zscore(log1p(DIST[i][j]))^2                (over the 20 ordered i != j pairs)
X3[i][j]  = max(0, DIST[i][j] - D_STAR) * log(GDP[t][j]),  D_STAR = 1.0
s1_ij,t   = s0_ij,t + BETA_SQ * X2[i][j] * U[i][j] + BETA_RELU * X3[i][j] * U[i][j]
```

Frozen nonlinear coefficients: `BETA_SQ = 0.05`, `BETA_RELU = 0.15`, `D_STAR = 1.0`.
`zscore` uses `mean = 1.045045222291799` and `sd = 0.3248658611007377` of
`log1p(DIST)` over the 20 ordered off-diagonal pairs; both are properties of the
frozen generator, not fitted statistics.

Non-nestability is pre-registered and checked statically (§11): regressing `X2`
and `X3` on the span `{1, DIST, GDP_j, GDP_i, DIST*GDP_j, DIST*GDP_i, GDP_i*GDP_j}`
leaves residuals, so neither nonlinear term is representable by the S0 linear score
family, not even with simple feature engineering.

Reference values:

```
R00 (time_id 1): [0.411547386, 0.240956772, 0.168652417, 0.178843425] on R01 R02 R03 R04
R04 (time_id 1): [0.049978191, 0.172580247, 0.777441563]              on R00 R01 R03
both sum to 1.000000000000
```

Because `GDP` growth is uniform across regions, centre differences and the
conditional shares are time-invariant in both regimes (`S1` differs only in the
4th decimal across `t`), so all reference values are quoted at `time_id 1`. The
time variation enters through `m` and `ell`. This is intentional and keeps the
control interpretable.

---

## 4. Frozen baseline family (exactly three)

| # | Family | Definition | Free parameters | Trained |
|---|---|---|---|---|
| 1 | fixed baseline | support-normalized uniform prior: `W_ij,t = 1 / available_count(i)` on allowed foreign cells, `0` on the diagonal and blocked cells | 0 | no |
| 2 | low-dimensional parametric baseline | gravity multinomial logit: `score_ij,t = alpha_d*log_gdp_pc_j + alpha_o*log_gdp_pc_i + alpha_dw*log_wage_gap + alpha_dist*log_distance + alpha_adj*adjacency + alpha_acc*log_accessibility_dest + alpha_w*w_ij + beta_j*1{j}` with destination intercepts, masked softmax over allowed foreign cells; fitted by weighted maximum likelihood | `7 + R = 12` | yes |
| 3 | small neural score mapping | per-pair MLP scoring `score_ij,t = f_theta(X_pair_ij_t, X_node_i_t, X_node_j_t, X_time_t, W_IJ)` followed by masked softmax over allowed foreign cells | see capacity ceiling | yes |

Capacity ceiling (hard, frozen): `input -> Linear(16) -> ReLU -> Linear(8) -> Tanh
-> Linear(1)`, i.e. **two hidden layers**, widths `16` and `8`, both `<= 32`, one
scalar output per pair. No GNN, attention, transformer, embedding bank, recurrent
layer, or end-to-end HANK component is authorized in the first P2 run. No
architecture change is permitted after observing S0/S1 outcomes.

Preprocessing: fixed declaration — neural inputs `log_distance`, `log_gdp_pc_gap`,
`log_wage_gap`, `log_accessibility_dest` are z-scored with mean and standard
deviation fitted **on the training split only**; `adjacency` and `t_normalized` are
used raw; `W_IJ` is used raw. Any other transformation is forbidden.

Loss: weighted cross entropy
`L = - sum_blocks w_block * sum_{j allowed} W_ij,t * log W_hat_ij,t`,
with block weight `w_block = ell_i,t / sum ell` (normalized over training blocks
only), masked to allowed foreign cells.

---

## 5. Split, preprocessing and reproducibility

Frozen single fold (`split_policy_id = DLH_WL_P2_SPLIT_V1`):

| Split | Definition |
|---|---|
| `TRAIN` | `t in {1, 2, 3}` for origins `R00, R01, R02` (9 blocks) |
| `VALIDATION` | `t = 4` for origins `R00, R01, R02` (3 blocks) |
| `TEST` | `t = 4` for origins `R03, R04` (2 blocks, region-blocked, `split_block_id = TEST_REGION_R03_R04`) |

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
- exactly one deterministic repeat of each fit with the identical seed and config
  is required, and repeated diagnostics must match bitwise or to `<= 1e-12`;
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
| `determinism_deviation` | max absolute difference between the two identical-seed repeats |
| `runtime_seconds` | wall-clock seconds of one deterministic fit plus one evaluation; total across the whole run also reported |

Secondary (reported, not gating):

| Metric | Definition |
|---|---|
| `top1_destination_accuracy` | share of blocks whose argmax `W_hat` equals the argmax `W` |
| `share_kl_per_block_mean` | mean KL `sum_j W log(W / W_hat)` over valid blocks |
| `cross_entropy_s0_vs_s1_delta` | per-family difference between regimes, reported without a success threshold |

Reported per family, per regime, per seed, with valid-block counts and the
excluded-block count (expected `0` here). No other metric may be added after
execution.

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
| wall-clock scientific training budget | **1800 s (30 minutes)**, measured across the whole P2 run (sum of both regimes; no per-regime extension) |
| maximum trained fits | **8** = 2 parametric MLE fits (S0, S1) + 6 neural fits (`NEURAL_SEEDS = [0, 1, 2]` × 2 regimes); the fixed baseline is not fitted |
| early stopping | `max_steps = 1500`, `eval_every = 50` steps, `early_stop_patience = 200` steps, `min_delta = 1e-4` on validation weighted cross entropy |
| optimizer | Adam, `lr = 0.01`, full batch, no schedule |
| hyper-parameter search | **none** |
| automatic retries | **none**, except **one** deterministic re-run of the identical config and seed permitted for a pure engineering failure (crash/NaN from infrastructure), with both attempts logged (so at most 9 fits can execute) |
| budget exhaustion | stops the experiment immediately; no successor Issue is created automatically |

Run accounting must be explicit: total fits attempted, fits completed, retries
used, and wall-clock consumed. Any ceiling breach is a Terminal B outcome, not an
invitation to redefine the experiment.


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
(`_tmp` script, deleted before commit; results reproduced in the report):

| Check | Result |
|---|---|
| `m` inside `[0,1]` | `min 0.07`, `max 0.17` |
| `ell` non-negative | `min 60.0`, `max 127.2` |
| support counts | `[4, 4, 4, 3, 3]`, all `>= 2` |
| `1 / (R - 1)` scaled softmax sums to 1 | `1.000000000000` for every reference block |
| S0 reference shares | `R00 [0.471644168, 0.274849815, 0.160168249, 0.093337767]` on `R01 R02 R03 R04`; `R04 [0.098255616, 0.190104212, 0.711640172]` on `R00 R01 R03` |
| S1 reference shares | `R00 [0.411547386, 0.240956772, 0.168652417, 0.178843425]`; `R04 [0.049978191, 0.172580247, 0.777441563]` || S1 shares at `time_id 4` | `R00 [0.411184483, 0.240744295, 0.168674265, 0.179396957]`, `R04 [0.049784019, 0.172467091, 0.777748890]` (time-invariance holds only to ~1e-3) |
| `d_mean` / `zscore` constants | `2.5`; `mean 1.045045222291799`, `sd 0.3248658611007377` |
| blocked-pair accounting | `R04` has 3 allowed destinations, so its reference vector has 3 entries |
| `X2` non-nestability residual | `max abs residual 0.3828362419` |
| `X3` non-nestability residual | `max abs residual 0.0007618439` |
| checks executed | `99` static checks, all applicable ones pass (`_tmp` checker, deleted before commit) |

No training, no optimization, no data access and no scientific solver was invoked
to produce these numbers.
