# DLH-WL-P3A — real-data source evidence and provenance audit (per-source)

Issue: **#80 / `DLH-WL-P3A`** — real-data label / provenance evidence gate.
Owner route: `DLH-WL-V1-20260918`.
Authority marker: `DLH_WL_P3A_REAL_DATA_LABEL_PROVENANCE_GATE_AUTHORIZED`.
Reviewer final activation comment: **`5741079748`**.
Operative baseline: **`e688a78907b69627800af65970f82d2fd94afae4`**.
Dedicated branch: `dsh/issue-80-dlh-wl-p3a-real-data-evidence-gate-2026-09-19`.
Status: **evidence / schema validation only. No empirical fitting. Zero scientific, model or
training calls.** No dataset was downloaded, scraped, purchased or ingested; no data file was
opened; no full text was bulk-read.

This document is one of the four Issue #80 deliverables:

1. this source-evidence audit;
2. `docs/data/DLH_WL_P3A_REGION_TIME_SUPPORT_MATRIX_2026_09_19.md` — the canonical
   source-by-dimension support matrix;
3. `docs/specifications/DLH_WL_P3A_EMPIRICAL_LABEL_GATE_2026_09_19.md` — the empirical
   label gate and branch definitions;
4. `reports/dlh_wl_p3a_2026_09_19/DLH_WL_P3A_REPORT.md` — the Issue report and terminal.

---

## 1. Authority chain and what this audit may not do

Binding hierarchy (from the activation comment):

1. Owner route `DLH-WL-V1-20260918`;
2. accepted P1B label/schema taxonomy
   (`docs/data/DLH_WL_P1B_LABEL_AND_SAMPLE_SCHEMA_2026_09_18.md`, revision 4);
3. accepted P2D method result and interpretation ceiling
   (`8ae4561ca3b0c78ba1d47045182fa5b4b023ed6d`) — interface/feature expectations only,
   **never** empirical evidence;
4. historical evidence
   `docs/data/DLH_1A_CHINA_INTERPROVINCIAL_LABOR_FLOW_DATA_FEASIBILITY_2026_08_19.md`
   (DLH-1A-R1) and its companion artifacts;
5. Issue #80 body;
6. activation comment `5741079748`.

Normative consequences applied throughout:

- **No evidence upgrade by inference.** A classification may move only when the source's own
  object semantics are directly evidenced. Nothing here does that, so every classification
  is carried over from the accepted E1 repository record, and every question the repository
  left open stays open.
- **E-levels are not self-promoted.** Repository rule
  `project_rules/PROJECT_RULE_RESEARCH_EVIDENCE_AND_CITATION_CURRENT.md` fixes
  `E0` = metadata/search, `E1` = abstract/official summary, `E2` = machine-read substantive
  sections, `E3` = human-verified. `E3` is `0`, and the Builder may not promote any entry.
  A machine read is at most `E2`; a search result is `E0`/`E1`.
- **No fabricated accounting quantities.** This audit produces no `m`, no `ell`, no `W`
  numerator and no `W` denominator, for any source.
- **No stock→flow relabelling, no annualization, no marginal→bilateral inference, no
  synthetic-as-empirical substitution.**

## 2. Taxonomy in force, and the mapping from the DLH-1A three-tier list

P1B froze a **six-class** taxonomy. The DLH-1A-R1 evidence used a **three-tier** list. The
mapping is declarative and exhaustive; it is a refinement, not a reclassification:

| DLH-1A-R1 tier (3) | P1B class (6) | Mapping relation |
|---|---|---|
| `TRUE_ANNUAL_OD_FLOW` | `TRUE_ANNUAL_OD_FLOW` | identity |
| `ANNUAL_OD_STOCK_OR_SAMPLE_CROSSTAB` | `ANNUAL_OD_STOCK_OR_SAMPLE_CROSSTAB` | identity |
| `MULTIYEAR_TRANSITION_OR_DERIVED_PROXY` | `MULTIYEAR_TRANSITION_OR_DERIVED_PROXY` | narrowed: transition / cohort-retention objects only |
| `MULTIYEAR_TRANSITION_OR_DERIVED_PROXY` | `PROVINCIAL_AGGREGATE_PROXY` | narrowed: objects whose only dimension is origin-level and/or destination-level totals, rates or growth-balance, with **no** observed pair dimension |
| — | `RULE_GENERATED` | project-internal only; no real-data candidate in P3A |
| — | `SYNTHETIC` | project-internal only; documented at P2/P2D, **not** a real-data candidate |

Applied consequence: the geodoi Id=3621 object, which DLH-1A-R1 placed in the tier-3 bucket
with the qualifier "provincial aggregate / model-derived", is assigned the P1B class
`PROVINCIAL_AGGREGATE_PROXY` (see §4.4), because its documented dimension set contains no
observed pair dimension. `RULE_GENERATED` and `SYNTHETIC` are `N/A` for every real-data
candidate in this audit; they remain project-internal classes only.

## 3. Candidate source inventory

Every candidate is one already documented by the repository evidence file
(`DLH_1A_CHINA_INTERPROVINCIAL_LABOR_FLOW_DATA_FEASIBILITY_2026_08_19.md` §2) or by its
companion artifacts. No new candidate was introduced: introducing one would require source
evidence that this Issue is not authorized to obtain, and the repository rule forbids
treating an unverified secondary mention as availability.

| Id | Candidate source | Repository citation (verbatim location) | Provider | Access condition as documented |
|---|---|---|---|---|
| S1 | Population Census long-form 2000 / 2010 / 2020 | `DLH_1A_...FEASIBILITY...md` §2 row 1 | NBS (National Bureau of Statistics of China) | public tabulations; microdata restricted |
| S2 | 1% National Population Sample Survey 2005 / 2015 | §2 row 2 | NBS | public tabulations |
| S3 | China Migrants Dynamic Survey (CMDS) 2009–2018 | §2 row 3 | NHFPC/NHC (former National Health and Family Planning Commission, now National Health Commission) | restricted |
| S4 | Estimation Dataset of Inter-provincial Migration Sub-flows in China (2010–2020), geodoi Id=3621 | §2 row 4 and §3 | geodoi / Global Change Data Repository; associated paper in *Acta Geographica Sinica* | published |
| S5 | Origin–destination (OD) of the interprovincial floating population of China, *Journal of Maps* 2016 | §2 row 5 | Taylor & Francis / *Journal of Maps* article + supplementary dataset | published |
| S6 | Population Research methodological / statistical-standard studies | §2 row 6 | journal (documentation only) | journal access |

External locators recorded by the repository (§2 URL line) and re-checked read-only in this
Issue:

- S4: [geodoi Id=3621](https://geodoi.ac.cn/weben/geodoi.aspx?Id=3621)
- S5: [OD of the interprovincial floating population](https://www.tandfonline.com/doi/pdf/10.1080/17445647.2016.1239556)
- S3: [CMDS retrospective](https://link.springer.com/article/10.1007/s42379-021-00091-9)
- S6: [statistical standard](https://rkyj.ruc.edu.cn/EN/Y2025/V49/I1/3)

## 4. Per-source audit

Legend for the audit fields:

- `verification_status` vocabulary:
  - `INTERNAL_E1_CONSISTENT` — the repository's own E1 record is internally consistent
    across the feasibility file, the review packet and the E3 queue;
  - `NOT_VERIFIED_EXTERNAL` — the named external semantic question could not be
    independently verified from this environment;
  - `E3_PENDING_HUMAN` — reserved by the DLH-1A E3 queue for human verification; the Builder
    may not resolve it.
- `external_metadata_check` vocabulary: `ATTEMPTED_READ_ONLY__INSUFFICIENT`,
  `NOT_ATTEMPTED`.
- Every `share_numerator`, `share_denominator`, `m_i`, `ell_i` entry is **absent by
  construction**: `NOT_PRODUCED_BY_P3A`.

### 4.1 S1 — Population Census long-form 2000 / 2010 / 2020

| Dimension | Finding |
|---|---|
| raw object | census long-form migration items: current residence vs residence **five years earlier**, tabulated as interprovincial origin × destination transition matrices |
| year / reference window | decennial census reference moments (2000, 2010, 2020); each object is a **5-year** transition window (`TRANSITION_WINDOW_K_YEARS`, `k = 5`) |
| population / sample definition | full enumeration with a long-form subsample for the migration items; the repository documents "full enumeration sample" |
| origin definition | province of residence **five years before** the census reference moment |
| destination definition | province of residence **at** the census reference moment |
| bilateral pair support | yes — an interprovincial origin × destination transition matrix exists for the census years |
| local-stayer semantics | present within the same matrix as the "same province / same residence" cell family; this cell family is **not** the conditional `W^L` object (P1B §3.4: `support_mask_ii = false` always, home retention is carried only by `P_ii = 1 - m_i`) |
| weights | census long-form sample weights / inflation factors; harmonization across census rounds `NOT_VERIFIED_EXTERNAL` |
| province coverage | all provincial-level units of the census year (`31` mainland provincial-level units, plus the special-region treatment that the concrete region dictionary must resolve) |
| stock / flow / transition / proxy | **multi-year transition** (`MULTIYEAR_TRANSITION_OR_DERIVED_PROXY`) |
| P1B class | `MULTIYEAR_TRANSITION_OR_DERIVED_PROXY` |
| `direct_W_supervision` | **false** |
| `target_available_without_bridge` | **false** |
| `bridge_required` | `OTHER` — a pre-registered and sensitivity-tested timing model that converts a `k`-year transition into an annual share (P1B §2.1). P1B names `OTHER`, not `ANNUALIZATION`, because the object is a residence-transition, not an annual count to be annualized |
| claim ceiling | multi-year transition object; annual-flow wording is **forbidden**; no `W^L_ij,t` claim |
| provider / version / licence / access | NBS; version = census round; public tabulations with restricted microdata; the specific tabulation licence and redistribution terms `NOT_VERIFIED_EXTERNAL` |
| evidence level | `E1` |
| verification status | `INTERNAL_E1_CONSISTENT` + `NOT_VERIFIED_EXTERNAL` (tabulation schema, cross-round weight harmonization, licence) + `E3_PENDING_HUMAN` (DLH-1A E3 queue item 7: confirm 5-year transition semantics and interprovincial O-D tabulation availability) |
| external metadata check | `ATTEMPTED_READ_ONLY__INSUFFICIENT` — no provider variable dictionary was obtained |
| feature timing / leakage compatibility | the label value for the window ending at `t` is only complete at `t`; a prediction exercise at `t` must therefore declare `calendar_lag_definition` and must not use post-`t` revision of the census tabulation. Whether a same-`t` feature set is legitimately available is `REQUIRES_DECLARATION_AT_ADAPTER_TIME`; the DLH-1A feature map places node and pair features at `LIKELY_AVAILABLE_NEEDS_VERIFICATION` |

### 4.2 S2 — 1% National Population Sample Survey 2005 / 2015

| Dimension | Finding |
|---|---|
| raw object | the intercensal 1% sample survey's migration items: current residence vs residence five years earlier, tabulated as interprovincial origin × destination transition matrices |
| year / reference window | 2005 and 2015 survey moments; each object is a **5-year** transition window (`TRANSITION_WINDOW_K_YEARS`, `k = 5`) |
| population / sample definition | ≈1% national population sample |
| origin definition | province of residence five years before the survey moment |
| destination definition | province of residence at the survey moment |
| bilateral pair support | yes — interprovincial transition matrix for the survey years |
| local-stayer semantics | as S1: the same-province cell family is present but is not the conditional `W^L` object |
| weights | 1% sample design weights; cross-round harmonization `NOT_VERIFIED_EXTERNAL` |
| province coverage | all provincial-level units of the survey year |
| stock / flow / transition / proxy | **multi-year transition** |
| P1B class | `MULTIYEAR_TRANSITION_OR_DERIVED_PROXY` |
| `direct_W_supervision` | **false** |
| `target_available_without_bridge` | **false** |
| `bridge_required` | `OTHER` — same pre-registered `k`-year→annual timing model as S1 |
| claim ceiling | multi-year transition object; annual-flow wording forbidden |
| provider / version / licence / access | NBS; public tabulations; specific schema and licensing `NOT_VERIFIED_EXTERNAL` |
| evidence level | `E1` |
| verification status | `INTERNAL_E1_CONSISTENT` + `NOT_VERIFIED_EXTERNAL` + `E3_PENDING_HUMAN` (shared with S1 under E3 queue item 7) |
| external metadata check | `ATTEMPTED_READ_ONLY__INSUFFICIENT` |
| feature timing / leakage compatibility | as S1; additionally the 1% sample has a smaller sample base, so per-pair observation density must be declared at adapter time (`REQUIRES_DECLARATION_AT_ADAPTER_TIME`) |

### 4.3 S3 — China Migrants Dynamic Survey (CMDS) 2009–2018

| Dimension | Finding |
|---|---|
| raw object | annual repeated **cross-sectional survey of migrants**: migrant stock / sample crosstabulated by destination and by hukou-registered origin |
| year / reference window | annual, 2009–2018 (`SNAPSHOT_YEAR`-type reference period; the questionnaire reference wording is `NOT_VERIFIED_EXTERNAL`) |
| population / sample definition | migrant-only national cross-section (migrants are the sampling frame; non-migrants are not sampled) |
| origin definition | hukou-registered province (origin as **registration**, not as previous residence) |
| destination definition | current province of residence / work at the survey moment |
| bilateral pair support | `LIKELY_AVAILABLE_NEEDS_SCHEMA_VERIFICATION` — constructible **only if** the microdata carry both current destination and hukou origin province. Not verified in this Issue |
| local-stayer semantics | **absent by design**: the sampling frame is migrants only, so non-migrants (local stayers) are not represented. Any use must declare this explicitly |
| weights | survey/design weights exist, but cross-year weight harmonization, sample-design changes and questionnaire harmonization are **unverified** (P1B §5 residual open item 4) |
| province coverage | national cross-section, migrant-only; per-province and per-pair cell counts `NOT_VERIFIED_EXTERNAL` |
| stock / flow / transition / proxy | **annual stock / sample crosstab** |
| P1B class | `ANNUAL_OD_STOCK_OR_SAMPLE_CROSSTAB` |
| `direct_W_supervision` | **false** |
| `target_available_without_bridge` | **false** |
| `bridge_required` | `STOCK_TO_FLOW` — a stated transition / cohort or steady-state assumption **plus** a declaration of the survey design (P1B §2.1) |
| claim ceiling | stock/sample shares of a snapshot; **must not** be reported as annual flows or as `W^L_ij,t` |
| provider / version / licence / access | NHFPC/NHC; years 2009–2018; access **restricted**; the concrete licence and application terms `NOT_VERIFIED_EXTERNAL` |
| evidence level | `E1` |
| verification status | `INTERNAL_E1_CONSISTENT` + `NOT_VERIFIED_EXTERNAL` (origin×destination constructibility, weight harmonization, licence/access) + `E3_PENDING_HUMAN` (DLH-1A E3 queue item 2: read the codebook and design documents) |
| external metadata check | `ATTEMPTED_READ_ONLY__INSUFFICIENT` — the read-only queries returned secondary academic papers that *use* CMDS; per Issue #80 §9 a secondary mention may **not** be used to verify access or object semantics, so nothing was upgraded |
| feature timing / leakage compatibility | contemporaneous with the survey year, so it is timing-compatible with a same-year feature set in principle; the migrant-only frame however makes the population basis inconsistent with an `origin × destination` all-population conditional share, which must be declared at adapter time |

### 4.4 S4 — Estimation Dataset of Inter-provincial Migration Sub-flows in China (2010–2020), geodoi Id=3621

| Dimension | Finding |
|---|---|
| raw object | per the repository's R1 reclassification, based on the official dataset description: (a) an all-increment equilibrium table of provincial population growth, and (b) logarithmic provincial **inflow-rate** and **outflow-rate** series. The associated *Acta Geographica Sinica* paper describes a cohort/retention-based simulation/identification model that estimates migration sub-flow **components** |
| year / reference window | 2010–2020 |
| population / sample definition | not a survey; a model-derived estimation dataset built from census and employment statistics. The estimation population and model population basis are `NOT_VERIFIED_EXTERNAL` |
| origin definition | province as the unit of an outflow rate / component; **no** observed pair origin |
| destination definition | province as the unit of an inflow rate / component; **no** observed pair destination |
| bilateral pair support | **not established** — the repository records "no proven bilateral (i,j,t) matrix". Read-only metadata checks in this Issue returned the dataset title and component/rate language consistent with that record, but no provider variable dictionary was obtained, so pair-level fields remain unproven |
| local-stayer semantics | not applicable / not established at pair level |
| weights | not a survey; no sample weights. Model/estimator identity and versioning `NOT_VERIFIED_EXTERNAL` |
| province coverage | 31 provinces as documented |
| stock / flow / transition / proxy | **provincial aggregate / model-derived proxy components and rates** |
| P1B class | `PROVINCIAL_AGGREGATE_PROXY` |
| `direct_W_supervision` | **false** |
| `target_available_without_bridge` | **false** |
| `bridge_required` | `SPATIAL_DECOMPOSITION` — a spatial interaction model plus an assumption that pins down the pair distribution. P1B is explicit that **marginals alone never identify `W^L`**, so this is not a mechanical bridge but a modelling assumption needing its own dated authority |
| claim ceiling | marginal / aggregate quantities and model-implied decomposition; **must never be labelled bilateral** |
| provider / version / licence / access | geodoi / Global Change Data Repository, DOI `10.3974/geodb.2024.07.05.V1` as surfaced by the read-only check (recorded as metadata only); "published"; the concrete licence text was **not** obtained → `NOT_VERIFIED_EXTERNAL` |
| evidence level | `E1` |
| verification status | `INTERNAL_E1_CONSISTENT` + `NOT_VERIFIED_EXTERNAL` (pair-level field existence, licence) + `E3_PENDING_HUMAN` (DLH-1A E3 queue item 1, the highest-priority item: whether ANY pair-level `(i,j,t)` field exists) |
| external metadata check | `ATTEMPTED_READ_ONLY__INSUFFICIENT` |
| feature timing / leakage compatibility | the object is model-derived from census and employment statistics, so it inherits both sources' revision timing; a leakage assessment is impossible until the estimator identity and vintage are declared (`NOT_VERIFIED_EXTERNAL`) |

### 4.5 S5 — Origin–destination (OD) of the interprovincial floating population of China (*Journal of Maps* 2016)

| Dimension | Finding |
|---|---|
| raw object | a **single-year migrant-stock OD matrix**: interprovincial floating population by origin and destination, derived from the 2010 census floating-population information |
| year / reference window | one matrix, 2010 census reference (`SNAPSHOT_YEAR`) |
| population / sample definition | floating population (residence ≠ hukou registration), as captured by the 2010 census |
| origin definition | origin province of the floating population as defined by the source's own construction |
| destination definition | destination province at the census moment |
| bilateral pair support | yes — a published origin × destination matrix for the single reference year |
| local-stayer semantics | absent: the object covers the **floating** population only; non-movers are not in the matrix |
| weights | derived from census tabulations; the derivation weights and any smoothing/estimation step are `NOT_VERIFIED_EXTERNAL` |
| province coverage | 31 provinces as documented |
| stock / flow / transition / proxy | **annual stock / sample crosstab** — a stock snapshot, explicitly "not flow" in the repository record |
| P1B class | `ANNUAL_OD_STOCK_OR_SAMPLE_CROSSTAB` |
| `direct_W_supervision` | **false** |
| `target_available_without_bridge` | **false** |
| `bridge_required` | `STOCK_TO_FLOW` |
| claim ceiling | stock shares of a single snapshot; **must not** be reported as annual flows or as `W^L_ij,t` |
| provider / version / licence / access | *Journal of Maps* article + supplementary dataset; the article's own licence is `NOT_VERIFIED_EXTERNAL`; the object is single-year so it cannot support a time series by itself |
| evidence level | `E1` |
| verification status | `INTERNAL_E1_CONSISTENT` + `NOT_VERIFIED_EXTERNAL` (derivation method, licence) |
| external metadata check | `ATTEMPTED_READ_ONLY__INSUFFICIENT` — the read-only check confirmed the article title and its OD-of-floating-population subject; it did **not** yield the variable dictionary or licence |
| feature timing / leakage compatibility | single-year snapshot; cannot support held-out-**time** evaluation on its own, so a time-split claim would be unavailable. `split_generalization_claim` for any use would be limited to `HELD_OUT_ORIGIN_ROLE` at best, and even that requires ≥2 years across which origin roles can be held out |

### 4.6 S6 — Population Research methodological / statistical-standard studies

| Dimension | Finding |
|---|---|
| raw object | **none** — a methods / statistical-standard article defining migration measurement semantics, not a dataset |
| year / reference window | n/a (documentation) |
| population / sample definition | n/a |
| origin definition | n/a (it *discusses* definitions) |
| destination definition | n/a |
| bilateral pair support | n/a |
| local-stayer semantics | n/a |
| weights | n/a |
| province coverage | n/a |
| stock / flow / transition / proxy | documentation only |
| P1B class | `MULTIYEAR_TRANSITION_OR_DERIVED_PROXY` **as carried over verbatim from the DLH-1A documentation table**, with the explicit qualifier `DOCUMENTATION_ONLY__PRODUCES_NO_SHARE`. Assigning it a data-semantics class is a carry-over of the repository table, not an assertion that it is a data object |
| `direct_W_supervision` | **false** |
| `target_available_without_bridge` | **false** |
| `bridge_required` | `null` — the source produces no share at all (P1B §3.2 reserves `null` for exactly this case) |
| claim ceiling | methodological reference only; contributes no label, no share and no coverage |
| provider / version / licence / access | journal; access via journal subscription; specific licence `NOT_VERIFIED_EXTERNAL` |
| evidence level | `E1` |
| verification status | `INTERNAL_E1_CONSISTENT` + `NOT_VERIFIED_EXTERNAL` |
| external metadata check | `NOT_ATTEMPTED` — it is a documentation source and cannot change a data-object classification |
| feature timing / leakage compatibility | n/a |

## 5. External metadata check log (read-only, non-ingesting)

Issue #80 §3 permits manual/read-only checking of public source metadata if reachable. This
Issue performed a small number of read-only public-web metadata queries. The log is recorded
so a Reviewer can see exactly what was and was not done.

| # | Target | Outcome | Effect on any classification |
|---|---|---|---|
| 1 | geodoi Id=3621 dataset description / component naming (S4) | dataset title and component/rate language observed, consistent with the repository record; **no** provider variable dictionary obtained | **none** — pair-level fields remain unproven; stays `NOT_VERIFIED_EXTERNAL` |
| 2 | Annual Chinese population/employment yearbook interprovincial floating-population table | only commercial reseller and mirror pages returned; no provider documentation obtained | **none** — no new candidate was introduced and no classification changed |
| 3 | CMDS microdata codebook / origin×destination constructibility (S3) | only secondary academic papers that *use* CMDS returned | **none** — Issue #80 §9 forbids verifying availability from a secondary mention; stays `NOT_VERIFIED_EXTERNAL` |
| 4 | *Journal of Maps* 2016 OD floating-population article (S5) | article title and OD-of-floating-population subject confirmed | **none** — consistent with the existing `ANNUAL_OD_STOCK_OR_SAMPLE_CROSSTAB` record; variable dictionary and licence not obtained |

Explicit non-actions:

- no dataset, microdata, supplementary file or full-text PDF was downloaded, opened, copied
  or ingested;
- no page was crawled or bulk-fetched; no purchase or account creation was performed;
- no environment or package change was made;
- one result set surfaced a **local third-party mirror path** on the machine for the S5
  article. That path was **not** opened, read, copied, listed or used in any way, and this
  audit does not rely on its contents;
- no secondary source was used to promote an evidence level, and no classification was
  changed as a result of any external check.

Net effect of the external checks on the audit: **the classification of every source is
unchanged from the accepted E1 repository record.** No source was upgraded, and no source was
downgraded.

## 6. Cross-reference consistency checks (Issue #80 §8)

| Check | Result |
|---|---|
| `DLH_1A_...FEASIBILITY...md` §2 tier list vs P1B §2 six-class taxonomy | consistent under the §2 mapping; the only refinement is tier-3 splitting into `MULTIYEAR_TRANSITION_OR_DERIVED_PROXY` and `PROVINCIAL_AGGREGATE_PROXY` |
| `DLH_1A_...FEASIBILITY...md` §3 geodoi reclassification vs `DLH_1A_REVIEW_PACKET.md` §8 line 81 | consistent: both say no proven pair-level fields |
| `DLH_1A_...FEASIBILITY...md` §4 CMDS reclassification vs `DLH_1A_REVIEW_PACKET.md` §8 line 80 | consistent: annual migrant cross-section, schema/weight verification required |
| `DLH_1A_E3_HUMAN_VERIFICATION_QUEUE.md` items 1, 2, 7 vs the open questions in §4.1–§4.4 above | consistent; the three data-side E3 items are exactly the three questions this audit could not close |
| P1B §1.2 and §5 residual items 1–5 vs this audit | consistent: direct annual bilateral availability remains `UNRESOLVED`; no source is `TRUE_ANNUAL_OD_FLOW`; real `m`/`ell` provenance unresolved; CMDS weight harmonization unverified; the annual-share bridge needs its own dated authority |
| P1B §3.2 derivation rules vs the flags assigned in §4 | consistent: `target_available` is `false` for every real-data source because no dated bridge/assumption record exists, and `label_is_direct_target` is `false` for every source because none is a `CALENDAR_YEAR` `TRUE_ANNUAL_OD_FLOW` row |
| P2D interpretation ceiling ("annual bilateral OD data availability claim" is forbidden) vs this audit | consistent: this audit makes **no** availability claim; it records non-availability |

No internal or source contradiction was found. The terminals
`...__REVIEW_REQUIRED` and `BLOCKED_DLH_WL_P3A_SOURCE_AUTHORITY_OR_METADATA` are therefore not
selected; the reasons are recorded in
`docs/specifications/DLH_WL_P3A_EMPIRICAL_LABEL_GATE_2026_09_19.md` §6.

## 7. Source classification summary

| Id | Source (short) | P1B class | `direct_W_supervision` | `target_available_without_bridge` | `bridge_required` | Evidence level | External status |
|---|---|---|---|---|---|---|---|
| S1 | Census long-form 2000/2010/2020 | `MULTIYEAR_TRANSITION_OR_DERIVED_PROXY` | false | false | `OTHER` (5-year→annual timing model) | E1 | `NOT_VERIFIED_EXTERNAL` |
| S2 | 1% sample survey 2005/2015 | `MULTIYEAR_TRANSITION_OR_DERIVED_PROXY` | false | false | `OTHER` | E1 | `NOT_VERIFIED_EXTERNAL` |
| S3 | CMDS 2009–2018 | `ANNUAL_OD_STOCK_OR_SAMPLE_CROSSTAB` | false | false | `STOCK_TO_FLOW` | E1 | `NOT_VERIFIED_EXTERNAL` |
| S4 | geodoi Id=3621 sub-flows 2010–2020 | `PROVINCIAL_AGGREGATE_PROXY` | false | false | `SPATIAL_DECOMPOSITION` | E1 | `NOT_VERIFIED_EXTERNAL` |
| S5 | *J. Maps* 2016 floating-population OD | `ANNUAL_OD_STOCK_OR_SAMPLE_CROSSTAB` | false | false | `STOCK_TO_FLOW` | E1 | `NOT_VERIFIED_EXTERNAL` |
| S6 | Methodological / statistical-standard studies | `MULTIYEAR_TRANSITION_OR_DERIVED_PROXY` (`DOCUMENTATION_ONLY__PRODUCES_NO_SHARE`) | false | false | `null` (no share) | E1 | `NOT_VERIFIED_EXTERNAL` |

**No source is `TRUE_ANNUAL_OD_FLOW`. No source carries `direct_W_supervision = true`. No
source carries `target_available_without_bridge = true`. `E3 = 0` is unchanged.** The
repository's existing classifications were neither upgraded nor invented, and the DLH-1A-R1
conclusion that a direct credible `(i,j,t)` destination-share label set is `UNRESOLVED`
stands.

## 8. Hard-prohibition compliance record

| Prohibition (Issue #80 §9, activation comment) | Status |
|---|---|
| do not relabel stock as flow | not done — S3, S5 remain `ANNUAL_OD_STOCK_OR_SAMPLE_CROSSTAB` |
| do not annualize multi-year transitions without a separately authorized bridge | not done — S1, S2 remain `MULTIYEAR_TRANSITION_OR_DERIVED_PROXY` with `bridge_required = OTHER` |
| do not infer bilateral `W` from marginals | not done — S4 remains `PROVINCIAL_AGGREGATE_PROXY` |
| do not infer `m` or `ell` from unrelated totals | not done — no `m` or `ell` was produced for any source |
| do not claim availability from a secondary mention alone | honoured — the three secondary-mention results in §5 changed nothing |
| do not use synthetic P2 success as evidence that a real source identifies `W` | honoured — P2D is cited in §1 only for interface/feature expectations |
| do not create P3B automatically | honoured — no successor, no bridge design, no fit |
| no download / scrape / purchase / ingestion | zero |
| no training / fitting / estimation | zero |
| no `m`/`ell`/`W` fabrication | zero such quantities emitted |
| no HJB / KFE / GE / MATLAB / household | zero calls |
| no full suite / no pytest | zero runs |
| no environment or package change | zero |

Scientific / model / training calls in this Issue: **0.**
