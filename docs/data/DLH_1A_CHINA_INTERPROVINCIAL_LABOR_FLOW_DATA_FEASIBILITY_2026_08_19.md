# DLH-1A-R1 — China Interprovincial Labor-Flow Data Feasibility (Corrected)

- Date: 2026-08-19 (R1 correction)
- Author: DSH (bounded Builder)
- Authority: GitHub Issue #3 — DLH-1A; authoritative R1 correction comment (2026-08-19 08:12:28).
- Status: EVIDENCE ONLY. No data purchase, download, scraping, or ingestion performed. All entries E0/E1.

## 1. Labor-data taxonomy (R1 three tiers — mandatory)

| Tier | Definition | Relation to `W^L_ij,t` supervision |
|---|---|---|
| **TRUE_ANNUAL_OD_FLOW** | newly realized i→j labor moves within a single year, both origin and destination observed | the ideal direct label for `W^L_ij,t` |
| **ANNUAL_OD_STOCK_OR_SAMPLE_CROSSTAB** | current migrant stock / sample cross-tab (origin × destination) in a given year | a stock/snapshot, not a flow; usable only with transition/cohort assumptions |
| **MULTIYEAR_TRANSITION_OR_DERIVED_PROXY** | 5-year transitions (census/1% survey), or model-derived aggregate components (growth-balance / cohort-retention estimates) | timing- and model-dependent; NOT a direct annual flow label |

## 2. Candidate sources — corrected classification

| # | Source | Tier (corrected) | O-D both observed | Years | Coverage | Access | Notes |
|---|---|---|---|---|---|---|---|
| 1 | Population Census long-form 2000/2010/2020 (NBS) | MULTIYEAR_TRANSITION (5-yr-ago residence) | yes (transition) | decennial | full enumeration sample | public tabulations; microdata restricted | 5-year transition matrices, not annual flows |
| 2 | 1% National Population Sample Survey 2005/2015 (NBS) | MULTIYEAR_TRANSITION | yes | intercensal | 1% sample | public tabulations | 5-year transitions |
| 3 | China Migrants Dynamic Survey (CMDS) 2009–2018 | ANNUAL_OD_STOCK_OR_SAMPLE_CROSSTAB (if origin×destination schema constructible) | yes (residence × hukou origin) | annual | migrant-only national cross-section | restricted | **annual repeated migrant cross-section**, not true flow; schema/weight verification required |
| 4 | Estimation Dataset of Inter-provincial Migration Sub-flows (2010–2020) (geodoi Id=3621) | MULTIYEAR_TRANSITION_OR_DERIVED_PROXY (provincial aggregate / model-derived) | **not established** | 2010–2020 | 31 provinces | published | official docs: provincial growth-balance equilibrium table + log inflow/outflow-rate data; **no proven bilateral (i,j,t) matrix** |
| 5 | Origin-destination (OD) of interprovincial floating population (J. Maps 2016) | ANNUAL_OD_STOCK_OR_SAMPLE_CROSSTAB (single-year stock, 2010 census) | yes (stock) | single matrix | 31 provinces | published | migrant stock OD matrix, not flow |
| 6 | Population Research methodological studies | MULTIYEAR_TRANSITION (documentation) | varies | varies | national | journal | statistical-standard semantics |

URLs: [OD floating population (J. Maps)](https://www.tandfonline.com/doi/pdf/10.1080/17445647.2016.1239556); [Sub-flows dataset (geodoi)](https://geodoi.ac.cn/weben/geodoi.aspx?Id=3621); [CMDS retrospective](https://link.springer.com/article/10.1007/s42379-021-00091-9); [Statistical standard (Population Research 2025)](https://rkyj.ruc.edu.cn/EN/Y2025/V49/I1/3).

## 3. geodoi Id=3621 — R1 reclassification (mandatory)

- Official dataset description supports only: (1) an **all-increment equilibrium table of provincial population growth**; and (2) **logarithmic provincial inflow-rate and outflow-rate** data. The associated Acta Geographica Sinica paper describes a **cohort/retention-based simulation/identification model** using census and employment statistics to estimate migration sub-flow components.
- **Reclassified: `PROVINCIAL_AGGREGATE_DERIVED_FLOW_COMPONENTS / PROXY`** — NOT a ready bilateral O-D-year source.
- **It does not currently establish a bilateral `(i,j,t)` 31×31 O-D matrix, and cannot by itself identify destination shares `W^L_ij,t`.** Its use as `W^L` labels is blocked unless direct schema/documentation later proves pair-level origin-destination fields.

## 4. CMDS — R1 reclassification (mandatory)

- CMDS = **annual repeated cross-sectional survey of migrants** (2009–2018). If microdata contain both current destination and hukou/origin province, it yields annual **migrant-stock/sample O-D cross-tabs**, NOT true annual migration flows.
- Classification: `ANNUAL_OD_STOCK_OR_SAMPLE_CROSSTAB`; pair-level annual O-D construction = `LIKELY_AVAILABLE_NEEDS_SCHEMA_VERIFICATION`.
- Additional identification risks: **cross-year survey-weight harmonization, sample-design changes, and questionnaire harmonization** would be required before using those cross-tabs as flow labels.

## 5. Direct answer to the supervision question

> **"Do credible bilateral destination-share labels that can directly supervise `W^L_ij,t` currently exist?"**

**No — not currently proven.** The bounded search found no published **true annual bilateral O-D flow matrix** for Chinese provinces. What exists is (a) decennial/intercensal 5-year **transition** matrices (census/1% survey), (b) annual **migrant-stock cross-tabs** (CMDS, subject to schema/weight verification), and (c) **provincial-aggregate derived components** (geodoi Id=3621, no proven pair-level fields). A direct, credible `(i,j,t)` destination-share label set is therefore **`UNRESOLVED`** and is the single most important remaining data blocker for supervised `W^L`.

## 6. Feature feasibility map (unchanged from R0, re-stated)

| Feature | Class | Verdict |
|---|---|---|
| distance / adjacency / terrain (`Z_static_ij`) | time-invariant pair | `AVAILABLE` (public GIS) |
| GDP pc, wage, population, urbanization, capital stock, fiscal (`Z_node_i,t`) | time-varying node | `LIKELY_AVAILABLE_NEEDS_VERIFICATION` |
| returns, industrial structure/upgrading (`Z_node_i,t`) | time-varying node | `DIFFICULT` |
| wage/GDP/return gaps (`Z_pair_ij,t`) | time-varying pair | `LIKELY_AVAILABLE_NEEDS_VERIFICATION` |
| accessibility change (`Z_pair_ij,t`) | time-varying pair | `DIFFICULT` |
| bilateral migration history (`Z_pair_ij,t`) | time-varying pair | `LIKELY_AVAILABLE_NEEDS_VERIFICATION` (subject to §5 blockers) |
| policy links / institutional state | time-varying | `UNRESOLVED` |

## 7. Measurement / selection issues (unchanged, re-stated)

- Migrant stock vs flow; hukou vs residence semantics; informal/unregistered migration undercoverage; CMDS migrant-only sampling vs full census; home-region identity convention must be reconciled with data residence/hukou semantics.
- No purchase/scrape/download/ingestion authorized or performed in DLH-1A / DLH-1A-R1.
