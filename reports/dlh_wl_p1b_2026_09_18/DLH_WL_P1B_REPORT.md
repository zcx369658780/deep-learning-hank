# DLH-WL-P1B — report: data/label semantics, canonical sample schema and first P2 offline prototype contract

Issue: **#75 / `DLH-WL-P1B`** — OPEN / ACTIVE / OPERATIVE (design / specification only).
Owner route: `DLH-WL-V1-20260918`.
Authority marker: `DLH_WL_P1B_DATA_SCHEMA_AND_P2_CONTRACT_AUTHORIZED`.
Reviewer final activation comment: **`5731890746`**.
Reviewer HOLDs remediated by this deliverable: **`5738867875`** (revision 2, seven
items) and **`5739104810`** (revision 3, identifiability/schema closure).
Operative baseline: **`4b4dc8c39d6a18b8928407308248f4020c10602c`**.
Dedicated branch: `dsh/issue-75-dlh-wl-p1b-data-schema-p2-contract-2026-09-18`.

This report records a bounded **design** deliverable. No model was trained, no data
was downloaded, scraped or purchased, no solver was called, and no empirical
label set is claimed. Section 9 records the bounded remediation of the Reviewer
HOLD and supersedes the affected numbers in sections 3-5.

---

## 1. Authority verified before mutation

- fresh-fetch: live `main` = GitHub API live `main` = `4b4dc8c39d6a18b8928407308248f4020c10602c`
  (= the activation-named operative baseline);
- Issue #75 read in full (body + both comments); the single activation comment
  `5731890746` names the baseline and the dedicated branch, and states
  **ACTIVE / OPERATIVE**;
- route lock re-verified **statically** at that baseline: Owner decision blob
  `038aad696dc66eeacabdf25bd7b96a49bd9d9c4c` with SHA-256
  `4b87eab29d46e8e53d5da77a7c6210cc9dbaee5b12d852379528d36c25ebd38c` → **MATCH**;
  roadmap `OWNER_LOCKED_ROUTE` block SHA-256
  `4d2ef5c125bfbf0bbb59bbb416734485ad3df6b4c4b50b17c760d4718b555ce8` → **MATCH**,
  and the block is byte-identical to the original publication
  `01daaf10c5854437870039a46435a075c664d9a3`. No route amendment present;
- dedicated branch created **from that exact baseline**, in an isolated temporary
  worktree, so the primary checkout and its local untracked artefacts were never
  touched.

## 2. Exact changed paths (4/4, allowlist-exact)

| # | Path | Status | Lines (rev 3) |
|---|---|---|---|
| 1 | `docs/data/DLH_WL_P1B_LABEL_AND_SAMPLE_SCHEMA_2026_09_18.md` | created | 437 |
| 2 | `docs/specifications/DLH_WL_P2_OFFLINE_PROTOTYPE_CONTRACT_2026_09_18.md` | created | 465 |
| 3 | `configs/dlh_wl_p2_offline_prototype.toml` | created (config revision 3) | 361 |
| 4 | `reports/dlh_wl_p1b_2026_09_18/DLH_WL_P1B_REPORT.md` | created | this file |

No source code, test, CURRENT governance, Owner decision, route lock, household
file or historical result was modified. Staging is explicit per path (no wide
`git add`).

## 3. What was frozen

### 3.1 Label semantics (`docs/data/...LABEL_AND_SAMPLE_SCHEMA...`)

Six frozen classes: `TRUE_ANNUAL_OD_FLOW`, `ANNUAL_OD_STOCK_OR_SAMPLE_CROSSTAB`,
`MULTIYEAR_TRANSITION_OR_DERIVED_PROXY`, `PROVINCIAL_AGGREGATE_PROXY`,
`RULE_GENERATED`, `SYNTHETIC`. For each class the document specifies the raw
object measured, whether it can **directly** supervise `W^L_ij,t`, the required
bridge/assumptions when it cannot, the claim ceiling, and the required provenance
fields.

Normative prohibitions include: stock, multi-year-transition and provincial-total
rows may not be relabelled, aggregated or rescaled into `TRUE_ANNUAL_OD_FLOW`;
normalization never repairs semantic mismatch; marginals alone are never a label;
a row with `m_i = 0` or `ell_i = 0` has no identifiable conditional target and may
not receive a fabricated uniform label; evidence level is a per-row property and
may not be silently promoted.

`label_is_direct_target` is a frozen **empirical-directness** predicate: `true` iff
`label_semantics == TRUE_ANNUAL_OD_FLOW` **and** `time_semantics == CALENDAR_YEAR`
**and** both origin and destination are observed for the same move.
`target_available` is a **separate usable-target** flag: `true` iff a usable target
exists for the declared purpose. A `SYNTHETIC` row is therefore
`label_is_direct_target = false` **and** `target_available = true`; bridged
stock/transition/proxy classes can only reach `target_available = true` after an
explicit dated bridge record. The evidence-level enum is frozen to
`E0 | E1 | E2 | E3 | NOT_APPLICABLE_NON_EMPIRICAL`, and synthetic/rule-generated
rows are never placed on the empirical ladder.

The inherited evidence status is preserved verbatim: per
`docs/data/DLH_1A_CHINA_INTERPROVINCIAL_LABOR_FLOW_DATA_FEASIBILITY_2026_08_19.md`
(DLH-1A-R1, all entries E0/E1) a direct credible `(i,j,t)` destination-share label
set is **`UNRESOLVED`**. P1B adds no source, no evidence level and no empirical
claim.

### 3.2 Canonical sample schema

One canonical row per `(origin_id, destination_id, time_id)`; rows group into an
allocation block per `(origin_id, time_id)`. Frozen field groups: keys and region
dictionary version; label semantics and value fields (`label_semantics`,
`label_evidence_level`, `label_is_direct_target`, `label_bridge_assumption`,
`share_numerator`/`share_denominator`, `raw_unit`, `target_W_ij_t`,
`target_available`); given accounting inputs (`m_i`, `ell_i` and their provenance
ids, `ell_unit`, period-alignment and the two **separately** declared lag
definitions); support and zero semantics (`support_mask_ij`, `zero_kind` with
`STRUCTURAL_ZERO` / `OBSERVED_ZERO` / `MISSING` / `NOT_APPLICABLE`,
`structural_zero_reason`, `missing_pattern_id`, `observed_value_present`); frozen
ordered feature lists with `feature_availability_time`,
`feature_available_at_prediction_time`, `leakage_flags` and `transformation_log`;
provenance (`source_id`, `provider`, `source_version`, `license`, `coverage_note`),
`sample_weight`/`sample_weight_source`, `split_assignment`, `split_block_id`,
`split_policy_id`, `identifiable_conditional_target`,
`available_foreign_destination_count`, `block_valid_row`, `notes`.

The document also freezes the three derivation rules so the schema cannot redefine
the accepted P1A semantics, and gives a one-to-one mapping table onto
`build_labor_destination_accounting(m, ell, W, *, support_mask, destination_wages,
contract_version, units)` and its result fields, plus five adapter obligations
(orientation, support derived from `STRUCTURAL_ZERO` only, no fabricated `W` row,
no identified choice below two available destinations, offline-only imports).

### 3.3 First P2 offline prototype contract

**Method-only, synthetic, not executed in this Issue.** Frozen:

- universe: `R = 5` regions, `T = 4` periods, 20 allocation blocks, **18 evaluable
  share cells per time slice** across all origins (`18 × 4 = 72` in total; each
  block has 3 or 4 allowed cells), support counts `[4, 4, 4, 3, 3]` with blocked
  pairs `(R03,R02)` and `(R04,R02)` marked `STRUCTURAL_ZERO`, and
  `support_mask_ii = false` always because home retention is carried by
  `P_ii = 1 - m_i` rather than by the W support mask;
- deterministic inputs `DIST`, `GDP`, `WAGE`, `URB`, `W_IJ`, `ELL`, `m`,
  `ACCESS` with declared ranges `m ∈ [0.07, 0.17]`, `ell ∈ [60.0, 127.2]`; the wage
  process is deliberately **not** proportional to GDP so the fitted contrast design
  has full column rank (6/6);
- identical frozen feature list of five pair features, four node features, one time
  feature and one static feature, all available at prediction time, no label or
  future-information leakage, `m`/`ell` never used as features;
- **S0** (parametric control): an exact linear combination of the six fitted
  contrast-identifiable columns — `1.50*log_gdp_dest + 0.60*log_wage_gap −
  1.20*log_adj_distance + 0.30*adjacency − 0.40*log_accessibility_dest +
  0.00*w_ij` (no `log_gdp_origin`, no intercept) — masked-softmax shares,
  deterministic (no noise), **nested by construction** and verified statically in
  the within-block contrast design at numerical precision
  (`1.11e-15` on TRAIN, `1.33e-15` over all blocks, with the frozen coefficients
  recovered exactly);
- **S1** (bounded nonlinear): the same corrected S0 core plus exactly two
  pre-registered within-block-centred interactions, `+0.05*X2` and `+0.15*X3`,
  with `X2 = (centred log1p(DIST))^2` and `X3 = max(0, DIST − 1)*centred log(GDP_j)`,
  both shown **non-nestable against that same fitted contrast design** (TRAIN
  residuals `0.008699` for S1, `0.170586` for `X2`, `0.019806` for `X3` against a
  `1e-12` precision floor);
- exactly **three** baseline families: support-normalized uniform fixed baseline;
  gravity multinomial logit over the **six** fitted contrast-identifiable columns
  (weighted MLE, `parametric_free_parameters = 6`; `log_gdp_origin` and per-origin
  block-additive intercepts are contextual only and cancel in the masked softmax);
  small neural pair-scorer with `2` hidden layers of widths `16` and `8` (both
  `<= 32`) followed by masked row normalization. No
  GNN/attention/transformer/recurrent/embedding/
  end-to-end HANK component;
- single frozen fold (`DLH_WL_P2_SPLIT_V1`) with an explicit excluded/reference
  state so all 20 blocks are accounted for: `TRAIN = t∈{1,2,3} × {R00,R01,R02}`
  (9 blocks), `VALIDATION = t=4 × {R00,R01,R02}` (3 blocks),
  `TEST = t=4 × {R03,R04}` (2 blocks, region-blocked), and
  `EXCLUDED_REFERENCE_ONLY = t∈{1,2,3} × {R03,R04}` (6 blocks) which may be
  generated only for deterministic reference/arithmetic checks and are never used
  for fitting, early stopping or final metrics. Counts satisfy `9+3+2+6 = 20`. The
  test split shares neither time nor regions with training; preprocessing
  statistics are fitted on `TRAIN` only; test is used once after the final
  checkpoint; P2 reports the excluded-block count explicitly (expected `6`);
- training protocol: weighted cross entropy, Adam `lr = 0.01`, full batch,
  `max_steps = 1500`, `eval_every = 50`, `early_stop_patience = 200`,
  `min_delta = 1e-4`, `NEURAL_SEEDS = [0, 1, 2]`, deterministic algorithms on,
  determinism verification on four configurations only (both parametric fits and
  the neural seed-0 fits), no hyper-parameter or seed search, and no architecture
  change after observing outcomes;
- pre-registered metrics: weighted cross entropy, mean absolute share error, row
  normalization violation, negativity and support violation counts, determinism
  deviation, runtime and excluded-block count (primary), plus top-1 destination
  accuracy, mean per-block KL and the S0/S1 cross-entropy delta (secondary);
- acceptance philosophy: P2 PASS means the bounded experiment executed
  reproducibly and the comparisons are interpretable. **There is no rule that the
  neural model must beat the parametric baseline**, and a correctly reported
  negative result is acceptable;
- cost ceiling: `8` primary fit configurations, `12` planned fit executions
  (8 primary + 2 parametric repeats + 2 neural seed-0 repeats), an absolute attempt
  ceiling of `13` after at most one engineering-only retry, all inside a single
  `1800 s` (30 minute) wall-clock ceiling, with `0` search runs and no automatic
  successor on budget exhaustion;
- P2/P3 boundary: P2 carries no empirical content and cannot be cited about Chinese
  interprovincial flows or about the existence of any bilateral OD label set; the
  `UNRESOLVED` real-label status does not block P2 because P2 uses no real labels.

## 4. Machine-readable twin

`configs/dlh_wl_p2_offline_prototype.toml` (configuration revision 3) mirrors all
frozen choices in 17 sections (`authority`, `scope`, `universe`, `inputs`, `support`,
`features`, `regime_s0`, `regime_s1`, `design_space_checks`, `baselines`,
`architecture_neural`, `train_protocol`, `split`, `metrics`, `budget`,
`label_semantics_policy`, `checks_this_issue`) and carries
`executed_in_this_issue = false`.
The contract document is the normative text; the TOML is the executable form.

## 5. Static checks performed (no training, no test-suite execution)

Superseded table: the authoritative, post-remediation results are in sections 9 and
10. The first revision reported 99 static checks with 0 failures, and revision 2
reported 120 checks with 0 failures.

## 6. Zero-call counts

```
neural training runs                 = 0
data download / scrape / purchase    = 0
HJB / KFE / GE / MATLAB calls        = 0
test-suite executions (any scope)    = 0
environment or package changes       = 0
expensive scientific/model calls     = 0
external network reads               = 0 (only GitHub reads of the live main ref and Issue #75)
```

Only document authoring, `tomllib` parsing, plain-Python arithmetic and
linear-algebra checks on frozen synthetic constants, `git` metadata commands and the
GitHub reads above were executed. No scientific module was imported; no household,
HJB, KFE or GE code was touched or triggered.

## 7. Known limitations and open items

- the deliverable is a **design**; nothing here is an experimental result, and the
  frozen P2 contract has not been executed;
- real annual bilateral OD label availability remains `UNRESOLVED`; no source in
  the repository is currently classified `TRUE_ANNUAL_OD_FLOW` for China provinces;
- `m`/`ell` provenance for real data, survey-weight harmonization for
  `ANNUAL_OD_STOCK_OR_SAMPLE_CROSSTAB` sources, and the bridge from stock/transition/
  proxy classes to an annual share all remain unresolved and each needs its own
  dated authority;
- the region dictionary is declared as
  `DLH_WL_REGION_DICT_V1_2026_09_18`; the concrete dictionary is a later
  deliverable and is not created here;
- conditional shares carry only **small deterministic time variation** (S0 `~2.4e-4`,
  S1 `~2.6e-4` absolute between `time_id 1` and `time_id 4`) because the wage process
  grows differently from GDP; neither regime is exactly time-invariant, and both
  `time_id 1` and `time_id 4` reference vectors are frozen in the config.
  Time variation in the *accounting* still enters mainly through `m` and `ell`;
- the synthetic control is deliberately small (20 blocks, 18 evaluable share cells
  per time slice / 72 total, 9 training blocks); it is a method-validation
  device and carries no economic content;
- inherited repository test-contract debt from Issue #73 is untouched, and no
  repository-wide green is claimed (no suite was run here).

---

## 9. Remediation record (Reviewer HOLD `5738867875`, revision 2)

Scope: same Issue #75, same dedicated branch, no successor Issue. Only the original
four allowlist paths were modified. All seven HOLD items were repaired **before
any execution** — P2 has never run, so this is pre-execution design correction, not
outcome-driven tuning.

| HOLD item | Repair |
|---|---|
| **A. synthetic target availability contradictory** | `label_is_direct_target` is now purely the **empirical-directness** flag (`TRUE_ANNUAL_OD_FLOW` + `CALENDAR_YEAR` + both endpoints observed); `target_available` is a separate **usable-target** flag that `SYNTHETIC`/`RULE_GENERATED` rows may set `true` while remaining non-empirical; bridged classes need a dated bridge record; numerator/denominator are required by semantic applicability (`derived from raw counts`) rather than by the old blanket rule; the evidence-level enum is frozen to `E0 \| E1 \| E2 \| E3 \| NOT_APPLICABLE_NON_EMPIRICAL` with no promotion; the canonical example now uses the frozen S0 reference share `0.477725159` with `label_is_direct_target=false`, `target_available=true` |
| **B. support diagonal** | frozen `conditional_support_diagonal_always_false = true` / `support_mask_ii = false` for the `W^L` object, with an explicit statement that home retention is represented only by `P_ii = 1 - m_i`; schema and contract both updated |
| **C. split not exhaustive** | added the stable state `EXCLUDED_REFERENCE_ONLY` for the six blocks `t∈{1,2,3} × {R03,R04}`; counts `9+3+2+6 = 20`; those blocks may be generated only for deterministic reference/arithmetic checks and are never used for fitting, early stopping or final metrics; `excluded_block_count` added to the primary metrics with expected value `6`; the six blocks were **not** moved into `TRAIN` |
| **D. cell counting wording** | corrected everywhere: **18 evaluable share cells per time slice** across all five origins, `18 × 4 = 72` total, each block having 3 or 4 allowed cells; TOML names are now `evaluable_share_cells_per_time = 18`, `evaluable_share_cells_total = 72`, `foreign_cells_per_block_nominal = 4` and `foreign_cells_per_block_actual = [4, 4, 4, 3, 3]` |
| **E. S1 invariance contradiction** | both regimes now declare `conditional_shares_time_invariant = false` with `SMALL_DETERMINISTIC` variation, and both `time_id 1` and `time_id 4` reference vectors are frozen in the TOML and quoted in the normative text |
| **F. repeat vs budget arithmetic** | frozen accounting: **8 primary configurations** (2 parametric + 6 neural = 3 seeds × 2 regimes) → **12 planned executions** (+2 parametric repeats +2 neural seed-0 repeats) → **13 absolute attempts** (+ at most 1 engineering retry) inside **<= 1800 s**; determinism gating covers only the 4 verification configurations; seeds 1 and 2 are sensitivity replications, not duplicate determinism checks; no seed or hyper-parameter search |
| **G. S0 nesting claim** | S0 is now an **exact linear combination of the declared parametric baseline vocabulary** (`log_gdp_dest`, `log_gdp_origin`, `log_wage_gap`, `log_adj_distance`, `adjacency`, `log_accessibility_dest`) with no raw levels; representability is verified against the actual design (6 features + per-origin destination intercepts, block-additive under masked softmax) at numerical precision; the wage process was made independent of GDP to restore full design rank (6/6); S1 is the corrected S0 core plus the two pre-registered within-block-centred interactions, and non-nestability is checked against that **same** design space |

### 9.1 Post-remediation static checks

```
tomllib parse of configs/dlh_wl_p2_offline_prototype.toml : PASS (17 sections)
remediation static/arithmetic/cross-document checker      : 120 checks, 0 failures
```

Included, as required by the HOLD: TOML parses; every universe block has exactly
one split state and counts sum to `20`; the canonical synthetic example is
internally consistent and supplies a usable non-empirical target; the support
diagonal is `false` for conditional `W`; per-time and total cell counts are
`18`/`72`; S0 representability passes at numerical precision against the actual
parametric design; S1 non-nestability is measured against that same design space
plus block-additive constants; S1/S0 `t1`/`t4` machine-readable references agree
with the normative text and are not marked invariant; run-budget arithmetic is
`8 / 12 / <=13 / <=1800 s`; and the cross-document consistency check was updated
and rerun.

### 9.2 Regenerated reference values (revision 2)

```
S0  R00 t1 [0.477725159, 0.221843778, 0.164194930, 0.136236133]   R04 t1 [0.152928167, 0.196744187, 0.650327646]
    R00 t4 [0.477966319, 0.221836852, 0.164104853, 0.136091976]   R04 t4 [0.153106303, 0.196861942, 0.650031755]
S1  R00 t1 [0.479223272, 0.219532182, 0.163400470, 0.137844076]   R04 t1 [0.150941617, 0.194939240, 0.654119143]
    R00 t4 [0.479478444, 0.219535648, 0.163308523, 0.137677385]   R04 t4 [0.151139135, 0.195055970, 0.653804895]
design rank 6/6 | S0 residual <= 1.6e-14 | S1 residual 0.0056595644561093505
X2 residual 0.0907191779 | X3 residual 0.0314502493 | precision floor 1e-12
```

### 9.3 Zero-call counts for this remediation

```
neural training runs              = 0
data download / scrape / purchase = 0
HJB / KFE / GE / MATLAB           = 0
test-suite executions             = 0 (none, any scope)
environment / package changes     = 0
expensive scientific/model calls  = 0
```

Only document/config authoring, `tomllib` parsing, plain-Python arithmetic and
linear-algebra checks (stdlib + numpy on frozen synthetic constants), and `git`
metadata commands were executed. No scientific module, household code, solver or
network access was used.

---

## 10. Remediation record (Reviewer HOLD 2 `5739104810`, revision 3)

Scope: same Issue #75, same dedicated branch, no successor Issue. Only the original
four allowlist paths were modified, and the work was done **before any execution** —
P2 has never run, so this is again pre-execution design correction rather than
outcome-driven tuning. The universe, the neural architecture and the Owner route are
unchanged.

| HOLD 2 item | Repair |
|---|---|
| **H. parametric baseline must be contrast-identifiable** | the fitted parametric score now uses **only the six contrast-identifiable columns** `log_gdp_dest`, `log_wage_gap`, `log_adj_distance`, `adjacency`, `log_accessibility_dest`, `w_ij`; `log_gdp_origin` and the per-origin block-additive intercept are **removed from the fitted parameter vector** and declared as non-fitted context columns that cancel in the masked softmax; `parametric_free_parameters = 6`; the "unique optimum" wording is replaced by a precise claim conditioned on the contrast design being full rank `6 / 6` |
| **H5. rank on the actual TRAIN contrast design** | recomputed from the repository constants: **27 rows × 6 columns, rank `6 / 6`** on TRAIN (and `6 / 6` over the full universe), singular values `[5.418462466, 2.710476939, 0.7452778, 0.256755503, 0.009277778, 0.00042083]` |
| **H6/H7. S0 and S1 re-checked in that exact space** | S0 now excludes the origin term entirely and is an exact linear combination of the six fitted columns; in the contrast representation its residual is `1.1102230246251565e-15` on TRAIN and `1.3322676295501878e-15` over all blocks, recovering the frozen coefficients `[1.5, 0.6, -1.2, 0.3, -0.4, 0.0]`; S1/`X2`/`X3` remain non-nested against the same design with TRAIN residuals `0.008699130793511367` / `0.17058604712292663` / `0.019805631317407806` against a `1e-12` precision floor |
| **I. canonical nonzero target had the wrong zero-kind** | the canonical synthetic example now sets `zero_kind = "NOT_APPLICABLE"` for its nonzero `target_W_ij_t = 0.477725159`, and the schema states explicitly that `OBSERVED_ZERO` is **reserved** for a realized numeric zero inside the support |
| **J. canonical feature schema must encode every frozen input** | added explicit `time_feature_names` and `static_feature_names` plus the `X_static_ij` value vector, and replaced the two flat metadata lists with **per-group** `pair/node/time/static_feature_availability_time` and `pair/node/time/static_feature_transformation_log`, each required to match its own name list in length and order; the example now has name/value lengths `5 / 4 / 1 / 1` with matching grouped metadata; the P2 mapping/adapter obligations were updated; `m`/`ell` remain non-features |
| **K1. report split wording** | the report now states **9 training blocks** (validation `3`, test `2`, excluded `6`) instead of the earlier, incorrect smaller fitting-block count |
| **K2. determinism acceptance scope** | contract §7 acceptance now limits the determinism tolerance to **exactly the four verification configurations** (both parametric fits and the neural seed-0 fits), matching §5/§8, instead of the earlier blanket per-fit-family wording |
| **K3/K4. counts and machine config** | every parametric parameter count/reference was corrected (`6`, not `13`), and the machine-readable config plus the consistency checker were updated accordingly |

### 10.1 Post-remediation static checks (revision 3)

```
tomllib parse of configs/dlh_wl_p2_offline_prototype.toml : PASS (17 sections)
HOLD-2 static/arithmetic/cross-document checker           : 83 checks, 0 failures
```

Coverage required by the HOLD, all verified: TOML parses; the actual TRAIN contrast
design with all six fitted columns has rank `6 / 6`; the S0 contrast residual is at
numerical precision in that exact design and recovers the frozen coefficients;
S1/`X2`/`X3` remain non-nested against that exact design; the canonical example has a
nonzero target with `zero_kind = NOT_APPLICABLE`; every declared pair/node/time/static
feature has an explicit canonical value and unambiguous grouped
availability/transformation metadata; split counts remain `9 / 3 / 2 / 6 = 20`; the
budget remains `8` primary / `12` planned / `<= 13` attempts / `<= 1800 s`; the
determinism acceptance scope is exactly the four verification configurations; and
cross-document consistency passes (route id, baseline SHA, activation id, HOLD ids,
support counts, cell counts, budget arithmetic and every reference-share value).

### 10.2 Reference values after revision 3

The six-column S0 change does not move any reference share (the dropped
`log_gdp_origin` term was block-constant and the added `w_ij` coefficient is `0.00`),
so all values remain as frozen in revision 2 and are re-verified by the checker:

```
S0  R00 t1 [0.477725159, 0.221843778, 0.164194930, 0.136236133]   R04 t1 [0.152928167, 0.196744187, 0.650327646]
    R00 t4 [0.477966319, 0.221836852, 0.164104853, 0.136091976]   R04 t4 [0.153106303, 0.196861942, 0.650031755]
S1  R00 t1 [0.479223272, 0.219532182, 0.163400470, 0.137844076]   R04 t1 [0.150941617, 0.194939240, 0.654119143]
    R00 t4 [0.479478444, 0.219535648, 0.163308523, 0.137677385]   R04 t4 [0.151139135, 0.195055970, 0.653804895]
```

---

## 11. Terminal

```
DLH_WL_P1B_DATA_SCHEMA_AND_P2_CONTRACT__PASS__P2_IMPLEMENTATION_GATE_READY
```

One terminal only. No PR, merge, close, successor Issue or self-acceptance was
performed. Independent Reviewer verification is required.


