# DLH-WL-P1B — Label semantics and canonical observation/sample schema for conditional labor-destination shares

Issue: **#75 / `DLH-WL-P1B`** — design / specification only.
Owner route: `DLH-WL-V1-20260918`.
Authority marker: `DLH_WL_P1B_DATA_SCHEMA_AND_P2_CONTRACT_AUTHORIZED`.
Reviewer final activation comment: **`5731890746`**.
Operative baseline: **`4b4dc8c39d6a18b8928407308248f4020c10602c`**.
Status: **frozen design**. No data was downloaded, scraped, purchased or ingested;
no model was trained; no E0/E1 evidence was upgraded.

This document is one of the four Issue #75 deliverables. Its machine-readable
counterpart is `configs/dlh_wl_p2_offline_prototype.toml`; the experiment contract
is `docs/specifications/DLH_WL_P2_OFFLINE_PROTOTYPE_CONTRACT_2026_09_18.md`.

---

## 1. Scope, non-goals and inherited boundaries

Frozen here:

1. the semantic object that labels are supposed to measure;
2. a six-class label-semantic taxonomy with per-class claim ceilings;
3. the canonical observation/sample schema that any later P2/P3 adapter must
   produce;
4. the explicit mapping of that schema onto the **accepted P1A offline interface**
   (`src/deep_learning_hank/regional/labor_destination.py`, integrated at
   `d34f00a31e8d23dd8134b9e9ba1be0319e7901bc`).

Explicitly **not** done here and not authorized by this Issue:

- any download, scrape, purchase, ingestion or licence negotiation;
- any training, fitting, hyper-parameter search or data-driven tuning;
- any improvement of an evidence level (E0/E1 stay E0/E1);
- any claim that a real annual bilateral province-level OD flow label set exists;
- any change to the P1A interface, the household code, the Owner route or the
  CURRENT governance documents.

Inherited scientific boundary (unchanged): the first version learns **only** the
conditional foreign destination shares `W^L` given exogenous outflow shares `m`
and given origin labor totals `ell`. `m`, `ell`, population quality, household
total labor, capital networks and local parameters are **given inputs, never
learning targets**.

### 1.1 Frozen semantic object

For `i = origin`, `j = destination`, `t = time`, with arrays indexed
`[origin, destination]`:

```
W^L_ii,t = 0
W^L_ij,t >= 0
sum_{j != i} W^L_ij,t = 1        over allowed foreign destinations
P_ii,t   = 1 - m_i,t
P_ij,t   = m_i,t * W^L_ij,t      (j != i)
F_ij,t   = ell_i,t * P_ij,t
Ldest_j,t = sum_i F_ij,t
```

`W^L_ij,t` is a **share of a flow realized inside period `t`**, conditional on
origin `i` having already sent `m_i,t` of its labor abroad. It is not a stock, not
a multi-year transition probability and not a provincial aggregate ratio.

### 1.2 Inherited evidence status (must be preserved verbatim)

`docs/data/DLH_1A_CHINA_INTERPROVINCIAL_LABOR_FLOW_DATA_FEASIBILITY_2026_08_19.md`
(DLH-1A-R1, all entries E0/E1) concludes that a direct, credible `(i,j,t)`
destination-share label set is **`UNRESOLVED`**, and that the bounded search found
no published **true annual bilateral OD flow matrix** for Chinese provinces.

**P1B does not change that status.** Nothing in this document may be read as
proving, implying or preparing to claim such a label set. The taxonomy below adds
no new source, no new evidence level and no new empirical claim.

---

## 2. Label-semantic taxonomy (frozen)

Six classes are frozen. Every canonical sample row must carry exactly one
`label_semantics` value from this closed set.

| Class | Raw object actually measured |
|---|---|
| `TRUE_ANNUAL_OD_FLOW` | newly realized `i -> j` labor moves that occur inside a single year, with both origin and destination observed for the same move |
| `ANNUAL_OD_STOCK_OR_SAMPLE_CROSSTAB` | a snapshot: migrant **stock** or a survey **sample** cross-tabulated by origin × destination in a given year |
| `MULTIYEAR_TRANSITION_OR_DERIVED_PROXY` | residence-`k`-years-ago transition matrices, cohort/retention estimates, or other model-derived components whose timing is multi-year |
| `PROVINCIAL_AGGREGATE_PROXY` | origin-level and/or destination-level **totals** (inflow, outflow, growth-balance, rates) with no observed pair dimension |
| `RULE_GENERATED` | values produced by a deterministic, documented spatial/interaction rule implemented by this project |
| `SYNTHETIC` | values produced by a pre-registered synthetic generative process with fixed coefficients, used for method validation only |

### 2.1 Per-class contract

| Class | Direct supervision of `W^L_ij,t`? | Required bridge / assumptions | Claim ceiling | Required provenance |
|---|---|---|---|---|
| `TRUE_ANNUAL_OD_FLOW` | **YES** (the intended direct label) | none for the share itself; still requires a declared `m`/`ell` source and the same-period accounting identity to hold | the strongest available: a conditional-share relationship may be estimated for the covered `(i,j,t)` support, subject to separate identification review | source, provider, version/edition, licence, period definition, coverage, `m` and `ell` sources, unit and efficiency-labor basis, sample/coverage weights, region dictionary version |
| `ANNUAL_OD_STOCK_OR_SAMPLE_CROSSTAB` | **NO** | a stock→flow bridge (e.g. a stated transition/cohort or steady-state assumption) plus a declaration of the survey design; without it only a stock-share object is identifiable | stock/sample shares of a snapshot; may not be reported as annual flows or as `W^L_ij,t` | as above plus survey weights, sample design, questionnaire semantics (residence vs `hukou`), cross-year weight harmonization status |
| `MULTIYEAR_TRANSITION_OR_DERIVED_PROXY` | **NO** | conversion of a `k`-year transition into an annual share requires an explicit timing model (constant-hazard / annualization assumption) that must be pre-registered and sensitivity-tested | multi-year transition or proxy object; annual-flow wording is forbidden | transition window definition, reference year pair, model/estimator identity, version, licence, coverage |
| `PROVINCIAL_AGGREGATE_PROXY` | **NO** — cannot identify pair shares by itself | a spatial interaction model plus an assumption that pins down the pair distribution; marginals alone never identify `W^L` | marginal/aggregate quantities and model-implied decomposition; must never be labelled bilateral | series identity, provider, version, definitions of inflow/outflow/rate, unit, revision status |
| `RULE_GENERATED` | **NO** | none is needed for pipeline use, but the rule must be deterministic, versioned and reported with its parameters | method/pipeline evidence only; explicitly **not** empirical identification | rule name and version, exact parameters, features used, code path, seed (if any), the statement that the labels are rule-generated |
| `SYNTHETIC` | **NO** | none is needed for method validation; the generative process and coefficients are frozen before execution | method-only evidence; explicitly **not** an empirical China estimate and not a data-availability claim | generator id/version, exact equations and coefficients, support pattern, dimensions, seed policy, regeneration command, statement that the labels are synthetic |

### 2.2 Hard prohibitions (normative)

1. `ANNUAL_OD_STOCK_OR_SAMPLE_CROSSTAB`, `MULTIYEAR_TRANSITION_OR_DERIVED_PROXY`
   and `PROVINCIAL_AGGREGATE_PROXY` rows **must not** be relabelled, aggregated or
   rescaled into `TRUE_ANNUAL_OD_FLOW`, and must not be described as annual
   bilateral flows in any report, table or comment.
2. Normalization never repairs semantic mismatch: a row-normalized stock
   cross-tab is still a stock cross-tab.
3. `RULE_GENERATED` and `SYNTHETIC` rows must be labelled as such in every output
   artifact and must never be presented as real province evidence or as causal
   evidence.
4. Only marginals (`sum_j`, `sum_i`) are **not** a label: no class may be assigned
   from marginals; such data enters the schema as a provincial aggregate
   (`PROVINCIAL_AGGREGATE_PROXY`) or not at all.
5. A row with `m_i,t = 0` or `ell_i,t = 0` carries **no** identifiable conditional
   target regardless of class; it must not be given a fabricated uniform label.
6. Evidence level is a property of the row: a P1B/P2/P3 artifact must state the
   evidence level and may not silently promote E0/E1 material.

---

## 3. Canonical sample schema (frozen)

One canonical **observation row** = one `(origin_id, destination_id, time_id)`
triple. Rows are grouped by `(origin_id, time_id)` into an **allocation block**
whose foreign members must satisfy the row-normalization contract. Long format is
canonical; wide matrices are a lossless view of a block.

### 3.1 Key and identity fields

| Field | Type | Required | Semantics |
|---|---|---|---|
| `origin_id` | string | yes | region identifier, must exist in `region_dictionary_version` |
| `destination_id` | string | yes | region identifier from the same dictionary |
| `time_id` | integer or ISO period label | yes | period identifier; the period definition is declared in `time_semantics` |
| `time_semantics` | enum | yes | `CALENDAR_YEAR` saturated to annual, or a declared alternative (`TRANSITION_WINDOW_K_YEARS`, `SNAPSHOT_YEAR`, `SYNTHETIC_STEP`) |
| `same_region` | bool | yes | `origin_id == destination_id` |
| `region_dictionary_version` | string | yes | region set + code/version, required for any cross-year or cross-source join |

### 3.2 Label-semantic and label-value fields

| Field | Type | Required | Semantics |
|---|---|---|---|
| `label_semantics` | enum | yes | exactly one of the six frozen classes |
| `label_evidence_level` | enum | yes | `E0`, `E1`, `E2`, `E3` (per the project evidence rule) |
| `label_is_direct_target` | bool | yes | derivation-free predicate: `true` iff the row may be used as a supervision target for `W^L_ij,t` |
| `label_bridge_assumption` | string or null | required unless `label_is_direct_target` | the declared bridge used to reach a share, or `null` |
| `share_numerator` | float or null | required unless `label_is_direct_target` | raw pair quantity before normalization |
| `share_denominator` | float or null | required unless `label_is_direct_target` | raw origin-level denominator before normalization |
| `raw_unit` | enum | yes | `PERSONS`, `HOUSEHOLDS`, `EFFICIENCY_LABOR`, `NORMALIZED_SHARE`, or a declared alternative |
| `target_W_ij_t` | float or null | yes (nullable) | the conditional share, present **only** when a target is identifiable |
| `target_available` | bool | yes | `true` iff `target_W_ij_t` is not null |

Derivation rule (frozen): `label_is_direct_target = true` **iff**
`label_semantics == TRUE_ANNUAL_OD_FLOW` **and** `time_semantics == CALENDAR_YEAR`
**and** both origin and destination are observed for the same move. For every other
combination it is `false`, and `label_bridge_assumption` must name the bridge or
state `NONE_REQUIRED_RULE_OR_SYNTHETIC`.

### 3.3 Given accounting inputs (never learning targets)

| Field | Type | Required | Semantics |
|---|---|---|---|
| `m_i` | float in `[0,1]` | yes | given origin outflow share |
| `m_provenance_id` | string | yes | source/estimator identity for `m` |
| `ell_i` | float >= 0 | yes | given origin labor total |
| `ell_unit` | enum | yes | must be an explicit efficiency-labor basis; population counts may not be silently treated as efficiency labor |
| `ell_provenance_id` | string | yes | source/estimator identity for `ell` |
| `accounting_period_alignment` | bool | yes | whether `m`, `ell` and the label refer to the same `time_id` window |
| `calendar_lag_definition` | string or null | yes (nullable) | declared calendar-time lag, if any |
| `outer_iteration_lag_definition` | string or null | yes (nullable) | declared outer-iteration lag, if any, kept separate from calendar lag |

`m` and `ell` are **inputs**: the schema forbids them from appearing in the
feature set of any learned mapping and forbids treating them as targets.

### 3.4 Support, zero and missing semantics

| Field | Type | Required | Semantics |
|---|---|---|---|
| `support_mask_ij` | bool | yes | `true` = destination structurally available to this origin (including the own region where relevant) |
| `zero_kind` | enum | yes | `STRUCTURAL_ZERO`, `OBSERVED_ZERO`, `MISSING`, `NOT_APPLICABLE` |
| `structural_zero_reason` | string or null | required iff `zero_kind == STRUCTURAL_ZERO` | declared reason |
| `missing_pattern_id` | string or null | required iff `zero_kind == MISSING` | declared missingness mechanism |
| `observed_value_present` | bool | yes | whether a realized non-zero value was actually observed |

Normative rules:

- `STRUCTURAL_ZERO`: the realization is impossible or excluded by design; it must
  receive zero conditional mass and is excluded from the row sum;
- `OBSERVED_ZERO`: a realized zero inside the support. It is **not** structural
  impossibility, and it must not be deleted after seeing evaluation results;
- `MISSING`: unobserved, which is neither a zero nor an impossibility. Missing rows
  may be predicted but never supervised;
- the support set is part of the experiment design: changing it is a design change
  and may not be done after evaluating outcomes.

### 3.5 Feature fields

| Field | Type | Required | Semantics |
|---|---|---|---|
| `pair_feature_names` | list[string] | yes | frozen ordered list of pair-level feature names |
| `node_feature_names` | list[string] | yes | frozen ordered list of node-level feature names |
| `X_pair_ij_t` | list[float] | yes | frozen-order pair features for `(i,j,t)` |
| `X_node_i_t`, `X_node_j_t` | list[float] | yes | frozen-order node features for origin and destination |
| `X_time_t` | list[float] | yes | frozen-order time features |
| `feature_availability_time` | list[string] | yes | for each feature, the period at which its value would have been known |
| `feature_available_at_prediction_time` | bool | yes | `false` iff any used feature becomes known only after `time_id` |
| `leakage_flags` | list[string] | yes | `USES_LABEL`, `USES_FUTURE_INFORMATION`, `USES_TEST_REGION_INFORMATION`, or empty |
| `transformation_log` | list[string] | yes | exact deterministic transformation applied to each feature (for example `log`, `zscore_fit_on_train_only`) |

Normative rules: features must not encode the label, the same-period realized flow,
or any future information; any normalization statistics are fitted on training data
only; `m` and `ell` are never features.

### 3.6 Provenance, weights and split fields

| Field | Type | Required | Semantics |
|---|---|---|---|
| `source_id` | string | yes | source identity; for synthetic rows the generator id |
| `provider` | string | yes | provider/originator |
| `source_version` | string | yes | version/edition/vintage |
| `license` | string | yes | licence or access condition; `SYNTHETIC_INTERNAL` for synthetic rows |
| `coverage_note` | string | yes | coverage and known undercoverage |
| `sample_weight` | float or null | required for survey-derived rows, else null | survey/design weight |
| `sample_weight_source` | string or null | paired with `sample_weight` | weight variable identity and harmonization status |
| `split_assignment` | enum | yes | `TRAIN`, `VALIDATION`, `TEST` |
| `split_block_id` | string | yes | the block (time and/or region) that defines the split unit |
| `split_policy_id` | string | yes | the frozen split policy applied |
| `identifiable_conditional_target` | bool | yes | whether this allocation block supplies an identifiable conditional target at all |
| `available_foreign_destination_count` | integer | yes | count of allowed foreign destinations in the block |
| `block_valid_row` | bool | yes | whether the block is an allocation-required, fully valid conditional row |
| `notes` | string or null | yes (nullable) | free-text caveat |

Derivation rules (frozen):

```
block_valid_row                = (m_i > 0) and (available_foreign_destination_count >= 1)
                                 and (block foreign shares are non-negative, zero on the diagonal,
                                      and sum to 1 over allowed foreign destinations)
identifiable_conditional_target = (m_i > 0) and (ell_i > 0) and (block_valid_row)
conditional_choice_identified  = exists a block with identifiable_conditional_target
                                 and available_foreign_destination_count >= 2
```

The last two rules are exactly the accepted P1A semantics
(`rows_without_identifiable_target`, `rows_with_conditional_choice`,
`conditional_choice_identified`); the schema may not redefine them.

### 3.7 Canonical record (normative example shape)

```yaml
record:
  origin_id: "R00"
  destination_id: "R02"
  time_id: 1
  time_semantics: "SYNTHETIC_STEP"
  same_region: false
  region_dictionary_version: "DLH_WL_REGION_DICT_V1_2026_09_18"
  label_semantics: "SYNTHETIC"
  label_evidence_level: "NOT_APPLICABLE_SYNTHETIC"
  label_is_direct_target: false
  label_bridge_assumption: "NONE_REQUIRED_RULE_OR_SYNTHETIC"
  share_numerator: null
  share_denominator: null
  raw_unit: "NORMALIZED_SHARE"
  target_W_ij_t: null
  target_available: false
  m_i: 0.12
  m_provenance_id: "P2_SYNTHETIC_M_V1"
  ell_i: 100.0
  ell_unit: "EFFICIENCY_LABOR"
  ell_provenance_id: "P2_SYNTHETIC_ELL_V1"
  accounting_period_alignment: true
  calendar_lag_definition: null
  outer_iteration_lag_definition: null
  support_mask_ij: true
  zero_kind: "OBSERVED_ZERO"
  structural_zero_reason: null
  missing_pattern_id: null
  observed_value_present: true
  pair_feature_names: ["log_distance", "adjacency", "log_gdp_pc_gap"]
  node_feature_names: ["log_gdp_pc", "log_wage", "log_accessibility", "urbanization"]
  X_pair_ij_t: [-0.35667494393873245, 0.0, 0.1823215567939546]
  X_node_i_t: [10.0, 9.9, 8.2, 0.55]
  X_node_j_t: [10.2, 10.1, 8.4, 0.6]
  X_time_t: [1.0]
  feature_availability_time: ["T0_STATIC", "T0_STATIC", "T-1"]
  feature_available_at_prediction_time: true
  leakage_flags: []
  transformation_log: ["log", "log", "difference_of_logs"]
  source_id: "P2_SYNTHETIC_GRAVITY_S0"
  provider: "DLH_PROJECT_INTERNAL"
  source_version: "V1_2026_09_18"
  license: "SYNTHETIC_INTERNAL"
  coverage_note: "pre-registered synthetic control; method-only evidence"
  sample_weight: null
  sample_weight_source: null
  split_assignment: "TRAIN"
  split_block_id: "TIME_1:REGIONS_R00_R01_R02"
  split_policy_id: "DLH_WL_P2_SPLIT_V1"
  identifiable_conditional_target: true
  available_foreign_destination_count: 4
  block_valid_row: true
  notes: null
```

The example above is illustrative of shape only; the frozen numeric content for P2
is in `configs/dlh_wl_p2_offline_prototype.toml`.

---

## 4. Mapping onto the accepted P1A interface

The schema maps one-to-one onto the accepted offline interface
`build_labor_destination_accounting(m, ell, W, *, support_mask, destination_wages,
contract_version, units)`:

| Schema field | P1A parameter / result field |
|---|---|
| `m_i` per block | `m` (vector over regions) |
| `ell_i` per block | `ell` (vector over regions) |
| `target_W_ij_t` per block | `W` (square `[origin, destination]` matrix; diagonal must be `0`) |
| `support_mask_ij` | `support_mask` |
| `ell_unit`, `region_dictionary_version`, `source_id`/`source_version` | `units`, `contract_version`, provenance echo |
| declared destination wage vector (optional, out of V1 scope) | `destination_wages` |
| `block_valid_row`, `identifiable_conditional_target` | `active_row_mask`, `valid_row_mask`, `rows_without_identifiable_target` |
| `available_foreign_destination_count >= 2` blocks | `rows_with_conditional_choice`, `conditional_choice_identified` |
| — (derived) | `P`, `F`, `destination_labor`, `destination_wage_bill`, `wbar`, `total_labor`, `diagnostics` |

Adapter obligations:

1. build `m`/`ell` vectors and the `W` matrix in `[origin, destination]` order;
2. pass `support_mask` derived from `STRUCTURAL_ZERO` only — never from
   `OBSERVED_ZERO` or `MISSING`;
3. never pass a fabricated `W` row for a block with `m_i = 0` or `ell_i = 0`; such
   blocks carry `target_available = false`;
4. rows with fewer than two available foreign destinations must not be reported as
   identified conditional choices;
5. an adapter must not import or trigger HJB/KFE/GE code; offline algebra only.

---

## 5. Frozen declarations, units and residual open items

- Region dictionary id/version: `DLH_WL_REGION_DICT_V1_2026_09_18` (declaration
  placeholder; the concrete regional dictionary is a later deliverable and is not
  created here).
- `time_semantics` is per-row and must be declared; mixing `CALENDAR_YEAR` with
  transition or synthetic time inside one evaluation set is forbidden.
- Annual frequency is the default target frequency; any other frequency must be
  declared and may not be silently annualized.

**Residual open items (recorded, not resolved here):**

1. real annual bilateral OD label availability remains `UNRESOLVED` (DLH-1A-R1);
2. no source in the repository is currently classified `TRUE_ANNUAL_OD_FLOW` for
   China provinces;
3. `m` and `ell` provenance for real data is unresolved; no real efficiency-labor
   conversion exists in this repository;
4. survey-weight harmonization for the CMDS-type stock cross-tabs is unverified;
5. the bridge from any stock/transition/proxy class to an annual share is a
   scientific decision that needs its own dated authority.

None of these open items blocks P2 method validation, because P2 runs on
pre-registered synthetic data only and makes no empirical claim.
