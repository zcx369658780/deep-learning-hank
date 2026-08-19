# DLH-1A — China Interprovincial Labor-Flow Data Feasibility (Evidence)

- Date: 2026-08-19
- Author: DSH (bounded Builder)
- Authority: GitHub Issue #3 — DLH-1A
- Status: EVIDENCE ONLY. No data purchase, download, scraping, or ingestion performed. All entries are E0/E1 (metadata/official summary) from public web.

## 1. Measurement-type taxonomy (must not conflate)

| Type | Definition | Consequence for `F^L_ij,t` |
|---|---|---|
| **True flow** | number of workers newly moving i→j in year t | the target of `W^L`; NOT directly observed annually in official data |
| **Migration transition** | stock change over a fixed horizon (e.g., residence 5 years ago vs now) | yields 5-year O-D transition matrices, not annual flows |
| **Migrant stock** | current migrants from i resident in j at time t | O-D stock matrix; not a flow; needs transitions to infer flow |
| **Residence/hukou cross-tab** | current residence × hukou-registration place | O-D cross-tab of floating population (stock), no timing |
| **Workplace flow / commuting** | cross-region commuter flow | different object; generally not interprovincial labor migration |
| **Survey transition** | panel/cohort survey of moves between waves | approximates transition probability; O-D available; sample-limited |
| **Proxy / derived** | estimated annual sub-flows from stocks + transitions | O-D-year matrices constructible but model-dependent; needs provenance audit |

## 2. Candidate sources (E0/E1, no access attempted)

| # | Source / provider | Type of measure | Years / frequency | O-D both observed | Coverage | Access / cost (if known) |
|---|---|---|---|---|---|---|
| 1 | **Population Census long-form** 2000/2010/2020 (NBS) | migration transition + residence/hukou cross-tab | decennial (+5-yr-ago question) | yes | full enumeration sample (long form) | public tabulations; microdata restricted |
| 2 | **1% National Population Sample Survey** 2005/2015 (NBS) | migration transition | intercensal 5-yr | yes | 1% sample | public tabulations |
| 3 | **China Migrants Dynamic Survey (CMDS)** 2009–2018 (流动人口动态监测调查) | migrant stock cross-tab + survey transition (annual cross-section) | annual (2009–2018) | yes (current residence × hukou origin) | large national cross-sectional migrant sample | restricted (application via NBS/CPDRC) |
| 4 | **Estimation Dataset of Inter-provincial Migration Sub-flows (2010–2020)** (Global Change Research Data Publishing, geodoi.ac.cn Id=3621) | proxy/derived annual sub-flows | 2010–2020 | yes | 31 provinces | published dataset; license/provenance to verify |
| 5 | **Origin-destination (OD) of the interprovincial floating population of China** (Journal of Maps, 2016) | migrant stock OD matrix (2010 census basis) | single matrix (2010) | yes | 31 provinces | published map/data appendix |
| 6 | **Population Research (人口研究) studies** (e.g., 2025 statistical standard; 2022 migration transition) | methodological + transition statistics | varies | yes | national | journal (abstract E1) |

URLs: [OD floating population (J. Maps)](https://www.tandfonline.com/doi/pdf/10.1080/17445647.2016.1239556); [Sub-flows dataset (geodoi)](https://geodoi.ac.cn/weben/geodoi.aspx?Id=3621); [CMDS retrospective (Springer)](https://link.springer.com/article/10.1007/s42379-021-00091-9); [Statistical standard/intensity (Population Research 2025)](https://rkyj.ruc.edu.cn/EN/Y2025/V49/I1/3); [Migration transition remarks (Population Research 2022)](https://rkyj.ruc.edu.cn/EN/Y2022/V46/I6/41).

## 3. Feasibility verdict for `F^L_ij,t = (i, j, t)` labor flow

- **A clean annual true-flow matrix is NOT directly published.** Official sources give (a) decennial/intercensal 5-year migration-transition matrices, and (b) annual migrant-stock cross-tabs (CMDS), plus (c) a published derived annual sub-flow dataset for 2010–2020.
- **Feasible construction:** anchor on census/1%-survey O-D transition matrices; use CMDS annual cross-sections for year structure; treat the geodoi "sub-flows (2010–2020)" dataset as the closest ready O-D-year candidate **subject to provenance/methodology audit** (must verify it is not fabricated interpolation).
- **Hold-out feasibility:** hold-out-year is feasible (train early years, validate later years); hold-out-pair is feasible (withhold selected `(i,j)` pairs from the flow-supervised objective).
- **Verdict:** `LIKELY_AVAILABLE_NEEDS_VERIFICATION` for O-D-year flow evidence as transitions/derived flows; `UNRESOLVED` for a genuine annual flow measure.

## 4. Feature feasibility map (first pass)

| Feature | Class | Availability verdict | Notes |
|---|---|---|---|
| geographic distance / adjacency / terrain (`Z_static_ij`) | time-invariant pair | `AVAILABLE` | public GIS; must be frozen once, not re-estimated per year |
| GDP per capita, wage, population, urbanization, capital stock, fiscal rev/exp (`Z_node_i,t`) | time-varying node | `LIKELY_AVAILABLE_NEEDS_VERIFICATION` | NBS provincial yearbooks; definitional harmonization needed |
| returns (capital return), industrial structure, industrial upgrading (`Z_node_i,t`) | time-varying node | `DIFFICULT` | return series and "upgrading" indices require construction/audit |
| wage/GDP/return gaps (`Z_pair_ij,t`) | time-varying pair | `LIKELY_AVAILABLE_NEEDS_VERIFICATION` | derivable from node features |
| accessibility change / transport (`Z_pair_ij,t`) | time-varying pair | `DIFFICULT` | requires transport-network time series |
| bilateral migration history (`Z_pair_ij,t`) | time-varying pair | `LIKELY_AVAILABLE_NEEDS_VERIFICATION` | from the O-D sources in §2 |
| policy links / institutional state (`Z_pair_ij,t`, `Z_node_i,t`) | time-varying | `UNRESOLVED` | needs a defined, documented proxy |

## 5. Measurement / selection issues to record (deferred to DLH-1B/5, not resolved here)

- Migrant stock vs flow: census and CMDS measure stocks/cross-tabs; flows must be inferred.
- Hukou vs residence: floating population excludes permanent hukou migrants; home-region identity convention in NSR-HANK must be reconciled with the data's residence/hukou semantics.
- Undercoverage of informal/unregistered migration; rural-to-urban and interprovincial definitional variance across surveys.
- Sample design of CMDS (migrant-only) vs full census (includes non-migrants).
- No purchase/scrape/download/ingestion authorized or performed in DLH-1A.
