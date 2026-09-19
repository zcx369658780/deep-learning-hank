# DLH-WL-P3A — real-data label / provenance evidence gate — report

Issue: **#80 / `DLH-WL-P3A`**. Owner route: `DLH-WL-V1-20260918`.
Authority marker: `DLH_WL_P3A_REAL_DATA_LABEL_PROVENANCE_GATE_AUTHORIZED`.
Reviewer final activation comment: **`5741079748`**.
Operative baseline: `e688a78907b69627800af65970f82d2fd94afae4`.
Dedicated branch: `dsh/issue-80-dlh-wl-p3a-real-data-evidence-gate-2026-09-19`.

---

## 0. Terminal

```
DLH_WL_P3A_REAL_DATA_LABEL_EVIDENCE_GATE__PASS__BRANCH_B
```

**Branch `B` — bridged pair object only.** No direct annual flow source is verified, but
documented bilateral stock / sample / transition objects exist that could support a
separately authorized explicit bridge/sensitivity design.

`Branch D/B/P is a data-evidence classification, not a model-performance ranking.` No model
was run.

## 1. Deliverables

| # | Path | Role |
|---|---|---|
| 1 | `docs/data/DLH_WL_P3A_REAL_DATA_SOURCE_EVIDENCE_2026_09_19.md` | per-source audit, taxonomy mapping, external metadata check log, cross-reference checks, prohibition record |
| 2 | `docs/data/DLH_WL_P3A_REGION_TIME_SUPPORT_MATRIX_2026_09_19.md` | canonical source × dimension support matrix; region, time, support-mask, weights and leakage views; branch-availability table |
| 3 | `docs/specifications/DLH_WL_P3A_EMPIRICAL_LABEL_GATE_2026_09_19.md` | the empirical label gate G1/G2/G3, terminal selection, gate invariants, claim-ceiling ladder |
| 4 | this report | Issue completion report and terminal |

## 2. What was read (fresh, read-only)

Binding hierarchy, all read fresh at the operative baseline:

1. `AGENTS.md` and `tasks/TASK_INDEX_CURRENT.md`;
2. Owner route freeze `docs/decisions/DLH_OWNER_ROUTE_FREEZE_WL_V1_2026_09_18.md`
   (route `DLH-WL-V1-20260918`);
3. evidence discipline rules
   `project_rules/PROJECT_RULE_RESEARCH_EVIDENCE_AND_CITATION_CURRENT.md` (the E0–E3 ladder);
4. `docs/data/DLH_1A_CHINA_INTERPROVINCIAL_LABOR_FLOW_DATA_FEASIBILITY_2026_08_19.md`
   (DLH-1A-R1) and its companions
   `reports/dlh_1a_evidence_and_data_feasibility_2026_08_19/DLH_1A_REVIEW_PACKET.md` and
   `.../DLH_1A_E3_HUMAN_VERIFICATION_QUEUE.md`;
5. accepted P1B schema and taxonomy
   `docs/data/DLH_WL_P1B_LABEL_AND_SAMPLE_SCHEMA_2026_09_18.md` (revision 4);
6. accepted P2D report `reports/dlh_wl_p2d_2026_09_19/DLH_WL_P2D_REPORT.md` and its results
   terminal, **for interface/feature expectations only** — not as empirical evidence;
7. Issue #80 body and activation comment `5741079748`.

No file outside the repository was opened. No dataset, microdata or full text was opened.

## 3. Source classification summary

| Id | Candidate source | P1B class | `direct_W_supervision` | `target_available_without_bridge` | `bridge_required` | Claim ceiling | Evidence level | Verification status |
|---|---|---|---|---|---|---|---|---|
| S1 | Population Census long-form 2000 / 2010 / 2020 (NBS) | `MULTIYEAR_TRANSITION_OR_DERIVED_PROXY` | false | false | `OTHER` (5-year→annual timing model) | multi-year transition object; annual-flow wording forbidden | E1 | `INTERNAL_E1_CONSISTENT` + `NOT_VERIFIED_EXTERNAL` (tabulation schema, cross-round weights, licence) + `E3_PENDING_HUMAN` (queue item 7) |
| S2 | 1% National Population Sample Survey 2005 / 2015 (NBS) | `MULTIYEAR_TRANSITION_OR_DERIVED_PROXY` | false | false | `OTHER` | as S1 | E1 | as S1 |
| S3 | China Migrants Dynamic Survey (CMDS) 2009–2018 | `ANNUAL_OD_STOCK_OR_SAMPLE_CROSSTAB` | false | false | `STOCK_TO_FLOW` | stock/sample shares of a snapshot; must not be reported as annual flows or `W^L` | E1 | `INTERNAL_E1_CONSISTENT` + `NOT_VERIFIED_EXTERNAL` (origin×destination constructibility, weight harmonization, licence/access) + `E3_PENDING_HUMAN` (queue item 2) |
| S4 | Estimation Dataset of Inter-provincial Migration Sub-flows 2010–2020, geodoi Id=3621 | `PROVINCIAL_AGGREGATE_PROXY` | false | false | `SPATIAL_DECOMPOSITION` | marginal / aggregate quantities and model-implied decomposition; must never be labelled bilateral | E1 | `INTERNAL_E1_CONSISTENT` + `NOT_VERIFIED_EXTERNAL` (pair-level fields, licence) + `E3_PENDING_HUMAN` (queue item 1) |
| S5 | OD of the interprovincial floating population of China, *Journal of Maps* 2016 | `ANNUAL_OD_STOCK_OR_SAMPLE_CROSSTAB` | false | false | `STOCK_TO_FLOW` | stock shares of a single snapshot; must not be reported as annual flows or `W^L` | E1 | `INTERNAL_E1_CONSISTENT` + `NOT_VERIFIED_EXTERNAL` (derivation, licence) |
| S6 | Methodological / statistical-standard studies | `MULTIYEAR_TRANSITION_OR_DERIVED_PROXY` (`DOCUMENTATION_ONLY__PRODUCES_NO_SHARE`) | false | false | `null` (produces no share) | methodological reference only | E1 | `INTERNAL_E1_CONSISTENT` + `NOT_VERIFIED_EXTERNAL` |

**Zero sources are `TRUE_ANNUAL_OD_FLOW`. Zero sources carry
`target_available_without_bridge = true`. `E3 = 0` is unchanged.**

Classification changes made by P3A: **none.** Every classification is carried over verbatim
from the accepted E1 repository record. The only declarative change is the **taxonomy
mapping** from the DLH-1A three-tier list onto the P1B six-class taxonomy, which narrows
tier-3 into `MULTIYEAR_TRANSITION_OR_DERIVED_PROXY` and `PROVINCIAL_AGGREGATE_PROXY` and
assigns geodoi Id=3621 to the latter. No source was upgraded and no source was downgraded.

## 4. Support matrix summary

Full matrix: `docs/data/DLH_WL_P3A_REGION_TIME_SUPPORT_MATRIX_2026_09_19.md` §2.

| Dimension | S1 | S2 | S3 | S4 | S5 | S6 |
|---|---|---|---|---|---|---|
| origin observed | `YES_TRANSITION` | `YES_TRANSITION` | `YES_STOCK` | `YES_AGGREGATE` | `YES_STOCK` | `DOC_ONLY` |
| destination observed | `YES_TRANSITION` | `YES_TRANSITION` | `YES_STOCK` | `YES_AGGREGATE` | `YES_STOCK` | `DOC_ONLY` |
| bilateral pair observed | `YES_TRANSITION` | `YES_TRANSITION` | `NOT_VERIFIED_EXTERNAL` | `NOT_ESTABLISHED` | `YES_STOCK` | n/a |
| time semantics | `TRANSITION_WINDOW_K_YEARS` (k=5) | `TRANSITION_WINDOW_K_YEARS` (k=5) | `SNAPSHOT_YEAR` (annual) | derived series 2010–2020 | `SNAPSHOT_YEAR` (single) | n/a |
| same-period move | no | no | no | no | no | n/a |
| local stayer present | yes (not the `W^L` object) | yes | `ABSENT_BY_DESIGN` | `NOT_ESTABLISHED` | `ABSENT_BY_DESIGN` | n/a |
| province coverage | all provincial-level units of the census year | as S1 | national, migrant-only | 31 | 31 | n/a |
| sample / design weight | present, harmonization `NOT_VERIFIED_EXTERNAL` | present, harmonization `NOT_VERIFIED_EXTERNAL` | present, harmonization `NOT_VERIFIED_EXTERNAL` | none (not a survey) | census-derived, `NOT_VERIFIED_EXTERNAL` | n/a |
| direct `m_i` candidate | `NOT_PRODUCED_BY_P3A` | `NOT_PRODUCED_BY_P3A` | `NOT_PRODUCED_BY_P3A` | `NOT_PRODUCED_BY_P3A` | `NOT_PRODUCED_BY_P3A` | n/a |
| direct `ell_i` candidate | `NOT_PRODUCED_BY_P3A` | `NOT_PRODUCED_BY_P3A` | `NOT_PRODUCED_BY_P3A` | `NOT_PRODUCED_BY_P3A` | `NOT_PRODUCED_BY_P3A` | n/a |
| potential `W` numerator | `NOT_PRODUCED_BY_P3A` | `NOT_PRODUCED_BY_P3A` | `NOT_PRODUCED_BY_P3A` | `NOT_PRODUCED_BY_P3A` | `NOT_PRODUCED_BY_P3A` | n/a |
| potential `W` denominator | `NOT_PRODUCED_BY_P3A` | `NOT_PRODUCED_BY_P3A` | `NOT_PRODUCED_BY_P3A` | `NOT_PRODUCED_BY_P3A` | `NOT_PRODUCED_BY_P3A` | n/a |
| support-mask evidence | diagonal only | diagonal only | none | none | none | n/a |
| feature timing / leakage | label complete only at window end; `REQUIRES_DECLARATION_AT_ADAPTER_TIME` | as S1 plus sample density | contemporaneous, but mover-only frame must be declared | revision timing undeclared | single snapshot → no held-out time | n/a |

Additional region/time findings:

- the P1B region dictionary is a **declaration placeholder** and does not exist, so no
  canonical row can be instantiated and no region id is asserted by P3A;
- no real-data source carries `CALENDAR_YEAR` semantics with same-period moves, so no
  real-data evaluation set can currently satisfy P1B's prohibition on mixing
  `CALENDAR_YEAR` with transition or synthetic time;
- no source documents foreign-pair structural exclusions, so no real `STRUCTURAL_ZERO` set
  exists and no source-derived `support_mask` is available.

## 5. Verification status

| Status | Sources | Meaning |
|---|---|---|
| `INTERNAL_E1_CONSISTENT` | S1–S6 | the repository's own E1 record is mutually consistent across the feasibility file, the review packet and the E3 queue |
| `NOT_VERIFIED_EXTERNAL` | S1–S6, for the specific external questions named per source | the external semantic, schema and licence questions could not be independently verified from this environment |
| `E3_PENDING_HUMAN` | S1/S2, S3, S4 (DLH-1A E3 queue items 7, 2, 1) | reserved by the accepted E3 queue for human verification; the Builder may not resolve these and did not |

External metadata checks performed (all read-only, non-ingesting; full log in the source
evidence document §5): four targeted queries covering the geodoi dataset description, the
annual yearbook floating-population table, the CMDS codebook / constructibility question and
the *Journal of Maps* article. Every outcome was `ATTEMPTED_READ_ONLY__INSUFFICIENT`. Two
outcomes returned only secondary academic papers, which Issue #80 §9 forbids using to verify
availability. **No classification changed as a result of any external check.**

## 6. Cross-reference checks (Issue #80 §8)

| Check | Result |
|---|---|
| DLH-1A tier list vs P1B six-class taxonomy | consistent under the declared mapping; tier-3 refined into two P1B classes |
| feasibility file vs review packet classifications (geodoi, CMDS) | consistent |
| E3 queue data-side items vs the open questions P3A could not close | exactly the same three questions |
| P1B §1.2 / §5 residual items vs this audit | consistent; direct annual bilateral availability remains `UNRESOLVED` |
| P2D interpretation ceiling vs this report | consistent; this report makes no availability claim |
| static table consistency (support matrix vs source evidence document) | consistent — every token in the matrix is drawn from the closed vocabularies in the matrix §1 |

No internal or source contradiction was found, so the review terminal

```
DLH_WL_P3A_REAL_DATA_LABEL_EVIDENCE_GATE__REVIEW_REQUIRED
```

was **not** selected. The authorizing evidence was available and was read, and Issue #80 §3
provides the `NOT_VERIFIED_EXTERNAL` disposition for unverifiable external metadata, so

```
BLOCKED_DLH_WL_P3A_SOURCE_AUTHORITY_OR_METADATA
```

was **not** selected either. The selection rationale is recorded in the gate specification
§6. The selected terminal is `DLH_WL_P3A_REAL_DATA_LABEL_EVIDENCE_GATE__PASS__BRANCH_B`.

## 7. Prohibited-action accounting (all zero)

| Item | Count |
|---|---|
| scientific / model / training calls | **0** |
| fits, estimates, optimizations, calibrations | **0** |
| `pytest` runs / full-suite runs | **0** |
| HJB / KFE / GE / MATLAB / household calls | **0** |
| datasets downloaded, scraped, purchased or ingested | **0** |
| data files, microdata or full texts opened | **0** |
| registry / package / environment changes | **0** |
| fabricated `m`, `ell`, `W` numerator or denominator values | **0** |
| stock→flow relabellings | **0** |
| multi-year→annual annualizations | **0** |
| bilateral `W` inferences from marginals | **0** |
| `m`/`ell` inferences from unrelated totals | **0** |
| evidence-level promotions (`E3` promoted by Builder) | **0** |
| secondary-mention-based availability claims | **0** |
| synthetic result used as real-data evidence | **0** |
| successor issues / bridge designs / P3B artifacts created | **0** |
| source code / tests / config / CURRENT governance / P2 artifacts touched | **0** |
| PRs, merges, closes, self-acceptances | **0** |

## 8. Exact changed paths (4 — exactly the Issue #80 allowlist)

```
docs/data/DLH_WL_P3A_REAL_DATA_SOURCE_EVIDENCE_2026_09_19.md
docs/data/DLH_WL_P3A_REGION_TIME_SUPPORT_MATRIX_2026_09_19.md
docs/specifications/DLH_WL_P3A_EMPIRICAL_LABEL_GATE_2026_09_19.md
reports/dlh_wl_p3a_2026_09_19/DLH_WL_P3A_REPORT.md
```

Nothing else was created or modified: no source code, no tests, no config, no CURRENT
governance document, no household/HJB/KFE/GE file, no P1A/P1B/P2/P2D artifact.

## 9. Interpretation ceiling

Allowed by this Issue:

- the data-evidence classification itself (Branch B) and the reasoning that produces it;
- statements about what each candidate source's raw object is, its reference window, its
  population/sample basis and its coverage, **as documented at E1**;
- statements about what bridge class a source would require, and that no such bridge is
  authorized;
- audit comparison with the DLH-1A-R1 record as provenance context.

Explicitly **not** claimed by this Issue:

- any empirical China estimate;
- any annual bilateral OD data **availability** claim — the opposite is recorded;
- any claim that a bridged destination-share label set exists or can be built now;
- any unseen-region claim;
- any causal, welfare, policy, GE, HJB/KFE or household claim;
- any model-performance statement: no model was run, and Branch D/B/P is not a ranking;
- any evidence-level promotion: every source stays at `E1` and `E3 = 0`.

## 10. Terminal

```
DLH_WL_P3A_REAL_DATA_LABEL_EVIDENCE_GATE__PASS__BRANCH_B
```

No successor Issue, no bridge design and no empirical fitting is created or authorized by
this report. The data-evidence branch is classified; the scientific work remains gated.
