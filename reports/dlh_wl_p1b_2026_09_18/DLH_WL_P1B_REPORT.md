# DLH-WL-P1B — report: data/label semantics, canonical sample schema and first P2 offline prototype contract

Issue: **#75 / `DLH-WL-P1B`** — OPEN / ACTIVE / OPERATIVE (design / specification only).
Owner route: `DLH-WL-V1-20260918`.
Authority marker: `DLH_WL_P1B_DATA_SCHEMA_AND_P2_CONTRACT_AUTHORIZED`.
Reviewer final activation comment: **`5731890746`**.
Operative baseline: **`4b4dc8c39d6a18b8928407308248f4020c10602c`**.
Dedicated branch: `dsh/issue-75-dlh-wl-p1b-data-schema-p2-contract-2026-09-18`.

This report records a bounded **design** deliverable. No model was trained, no data
was downloaded, scraped or purchased, no solver was called, and no empirical
label set is claimed.

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

| # | Path | Status | Lines | Git blob |
|---|---|---|---|---|
| 1 | `docs/data/DLH_WL_P1B_LABEL_AND_SAMPLE_SCHEMA_2026_09_18.md` | created | 365 | `bb9ca93d477e50432d483a957a8d369caa6c2d9f` |
| 2 | `docs/specifications/DLH_WL_P2_OFFLINE_PROTOTYPE_CONTRACT_2026_09_18.md` | created | 342 | `7800ede094032c1c49b1b33412c581d4e865d287` |
| 3 | `configs/dlh_wl_p2_offline_prototype.toml` | created | 270 | `20b45217f5a013fd039cca9b3f37c127851b8dc4` |
| 4 | `reports/dlh_wl_p1b_2026_09_18/DLH_WL_P1B_REPORT.md` | created | this file | — |

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

`label_is_direct_target` is a frozen predicate: `true` iff
`label_semantics == TRUE_ANNUAL_OD_FLOW` **and** `time_semantics == CALENDAR_YEAR`
**and** both origin and destination are observed for the same move.

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

- universe: `R = 5` regions, `T = 4` periods, 20 allocation blocks, 18 evaluable
  foreign share cells per block (`72` in total), support counts `[4, 4, 4, 3, 3]`
  with blocked pairs `(R03,R02)` and `(R04,R02)` marked `STRUCTURAL_ZERO`;
- deterministic inputs `DIST`, `GDP`, `WAGE`, `URB`, `W_IJ`, `ELL`, `m`,
  `ACCESS` with declared ranges `m ∈ [0.07, 0.17]`, `ell ∈ [60.0, 127.2]`;
- identical frozen feature list of five pair features, four node features, one time
  feature and one static feature, all available at prediction time, no label or
  future-information leakage, `m`/`ell` never used as features;
- **S0** (parametric control): `sigma*(beta_d*GDP_j - beta_o*GDP_i - gamma_dist*DIST)`
  masked-softmax shares with `sigma = 1.0`, `beta_d = 0.30`, `beta_o = 0.20`,
  `gamma_dist = 0.60`, deterministic (no noise);
- **S1** (bounded nonlinear): the same linear core plus exactly two pre-registered
  nonlinear interactions, `+0.05*X2*U` and `+0.15*X3*U`, with
  `X2 = zscore(log1p(DIST))^2` and `X3 = max(0, DIST - 1)*log(GDP_j)`, both shown
  **non-nestable** relative to the S0 linear span even with simple feature
  engineering;
- exactly **three** baseline families: support-normalized uniform fixed baseline;
  gravity multinomial logit (12 free parameters, weighted MLE); small neural
  pair-scorer with `2` hidden layers of widths `16` and `8` (both `<= 32`) followed
  by masked row normalization. No GNN/attention/transformer/recurrent/embedding/
  end-to-end HANK component;
- single frozen fold (`DLH_WL_P2_SPLIT_V1`): `TRAIN = t∈{1,2,3} × {R00,R01,R02}`
  (9 blocks), `VALIDATION = t=4 × {R00,R01,R02}` (3 blocks),
  `TEST = t=4 × {R03,R04}` (2 blocks, region-blocked). The test split shares
  neither time nor regions with training; preprocessing statistics are fitted on
  `TRAIN` only; test is used once after the final checkpoint;
- training protocol: weighted cross entropy, Adam `lr = 0.01`, full batch,
  `max_steps = 1500`, `eval_every = 50`, `early_stop_patience = 200`,
  `min_delta = 1e-4`, `NEURAL_SEEDS = [0, 1, 2]`, deterministic algorithms on, one
  deterministic identical-seed repeat required, no hyper-parameter search and no
  architecture change after observing outcomes;
- pre-registered metrics: weighted cross entropy, mean absolute share error, row
  normalization violation, negativity and support violation counts, determinism
  deviation and runtime (primary), plus top-1 destination accuracy, mean per-block
  KL and the S0/S1 cross-entropy delta (secondary);
- acceptance philosophy: P2 PASS means the bounded experiment executed
  reproducibly and the comparisons are interpretable. **There is no rule that the
  neural model must beat the parametric baseline**, and a correctly reported
  negative result is acceptable;
- cost ceiling: `1800 s` (30 minutes) wall-clock across the whole run, at most `8`
  trained fits (2 parametric MLE + 6 neural, i.e. 3 seeds × 2 regimes), no
  hyper-parameter search, at most `1` deterministic engineering retry, and budget
  exhaustion stops the experiment without auto-creating a successor;
- P2/P3 boundary: P2 carries no empirical content and cannot be cited about Chinese
  interprovincial flows or about the existence of any bilateral OD label set; the
  `UNRESOLVED` real-label status does not block P2 because P2 uses no real labels.

## 4. Machine-readable twin

`configs/dlh_wl_p2_offline_prototype.toml` mirrors all frozen choices in 16
sections (`authority`, `scope`, `universe`, `inputs`, `support`, `features`,
`regime_s0`, `regime_s1`, `non_nestability_check`, `baselines`,
`architecture_neural`, `train_protocol`, `split`, `metrics`, `budget`,
`checks_this_issue`) and carries `executed_in_this_issue = false`.
The contract document is the normative text; the TOML is the executable form.

## 5. Static checks performed (no training, no test-suite execution)

| Check | Result |
|---|---|
| TOML parse (`tomllib`) | **parses**, 16 sections, section set exactly as declared |
| internal arithmetic: `m`/`ell` ranges re-derived from the frozen formulas | `m ∈ [0.07, 0.17]`, `ell ∈ [60.0, 127.2]` — match the declarations |
| accessibility reference recomputed | `ACCESS[time_id 1][R00] = 23.376667` |
| support counts recomputed from the blocked-pair rule | `[4, 4, 4, 3, 3]`, minimum `3 ≥ 2` |
| S0/S1 reference shares recomputed from the frozen formulas, masked softmax, blocked pairs excluded | reproduced to `< 5e-7`; every reference block sums to `1.000000000000` |
| block accounting | `18` evaluable cells per block `× 4` periods `= 72` |
| budget accounting | `2` parametric `+ 6` neural `= 8 = max_training_runs`; `6 = 3 seeds × 2 regimes`; wall clock `1800 s`; `0` search runs |
| split accounting | train `9` + validation `3` + test `2` blocks; test disjoint in time **and** region from train |
| architecture ceiling | 2 hidden layers, widths `[16, 8]`, max `16 ≤ 32`, no unauthorized family enabled |
| cross-document consistency | route id, baseline SHA, activation id, authority marker, support counts, and all reference-share values identical across the three deliverables |
| prohibition scan | design documents make no test-execution claim and no undeclared training claim |
| **total** | **99 static checks, 0 failures** (`_tmp_consistency_check.py`, run once, deleted before commit) |

Two authoring defects were caught by these checks and fixed **before** commit:
an inconsistent `D_MEAN` constant (`2.0` → `2.5`), and reference share vectors that
had been generated without applying the blocked-pair support rule (`R04` correctly
has only 3 allowed foreign destinations, so its reference vector has 3 entries).
Neither fix changed a scientific choice; both removed internal inconsistency.

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

Only document authoring, `tomllib` parsing, plain-Python arithmetic checks, `git`
metadata commands and the GitHub reads above were executed. No scientific module
was imported; no household, HJB, KFE or GE code was touched or triggered.

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
- conditional shares are time-invariant by construction in S0 and nearly so in S1
  (uniform cross-region GDP growth); time variation enters only through `m` and
  `ell`. This is deliberate for an interpretable control, not a defect;
- the synthetic control is deliberately small (20 blocks / 72 evaluable share
  cells); it is a method-validation device and carries no economic content;
- inherited repository test-contract debt from Issue #73 is untouched, and no
  repository-wide green is claimed (no suite was run here).

## 8. Terminal

```
DLH_WL_P1B_DATA_SCHEMA_AND_P2_CONTRACT__PASS__P2_IMPLEMENTATION_GATE_READY
```

One terminal only. No PR, merge, close, successor Issue or self-acceptance was
performed. Independent Reviewer verification is required.
