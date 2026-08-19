# DLH-1A Review Packet — Literature Evidence + Labor-Flow Data Feasibility

- Date: 2026-08-19
- Author: DSH (bounded Builder)
- Authority: GitHub Issue #3 — `DLH-1A: Literature evidence and interprovincial labor-flow data feasibility`
- Accepted predecessor: Issue #2 / DLH-0R1, accepted commit `73e1ae5db9d7e362781a77fa2a204c80238fad3e`.
- Status: CANDIDATE evidence. Acceptance requires fresh-GitHub independent review (ChatGPT) + Owner direction.

## 1. Terminal classification

`DLH_1A_EVIDENCE_AND_LABOR_FLOW_DATA_FEASIBILITY_READY_FOR_GPT_REVIEW`

## 2. Baseline and branch

- Fresh baseline `origin/main` SHA: `aea6c73f0947a9da246d4775eff10012010d26ec`
- Dedicated branch: `dsh/issue-3-dlh-1a-literature-data-feasibility-2026-08-19`
- Candidate commit: single evidence commit at branch HEAD (2026-08-19, DSH); hash reported in the completion response. Expected delta: exactly the seven paths below, 0 behind / 1 ahead of baseline.
- `main` not modified.

## 3. Exact changed paths (seven allowlisted outputs)

1. `docs/literature/DLH_1A_NSR_HANK_LITERATURE_MAP_2026_08_19.md`
2. `docs/literature/DLH_1A_METHOD_AND_NOVELTY_BOUNDARY_MATRIX_2026_08_19.csv`
3. `docs/data/DLH_1A_CHINA_INTERPROVINCIAL_LABOR_FLOW_DATA_FEASIBILITY_2026_08_19.md`
4. `reports/dlh_1a_evidence_and_data_feasibility_2026_08_19/DLH_1A_EVIDENCE_REGISTER.csv`
5. `reports/dlh_1a_evidence_and_data_feasibility_2026_08_19/DLH_1A_E3_HUMAN_VERIFICATION_QUEUE.md`
6. `reports/dlh_1a_evidence_and_data_feasibility_2026_08_19/DLH_1A_REVIEW_PACKET.md`
7. `reports/dlh_1a_evidence_and_data_feasibility_2026_08_19/DLH_1A_FORBIDDEN_OPERATION_CHECK.md`

No roadmap, constitution, rule, Task Index, Startup Snapshot, README, source code, or historical evidence modified.

## 4. Literature candidates by evidence level

- E0: 9 (title/metadata only)
- E1: 12 (abstract/official-summary read)
- E2: 0 (no full-text machine read performed)
- E3: 0 (no human verification; queue only)
- Total material papers + data sources recorded: 21 (see evidence register)

## 5. Top material papers (evidence level in parens)

1. Structural RL for HA macro — Yang, Wang, Schaab, Moll, arXiv:2512.18892 (E1)
2. DeepHAM — Han, Yang, E, Quantitative Economics 2026 / arXiv:2112.14377 (E1)
3. Deep-MacroFin — arXiv:2408.10368 (E1)
4. Master-equation neural solver — Zhou & Gu draft (E0)
5. PINN for HA models — arXiv:2511.20283 (E1)
6. SSJ + Deep Learning for HANK — Kase (E0)
7. Economics-Inspired NN w/ homotopies — arXiv:2303.14802 (E1)
8. DL for solving/estimating dynamic models (survey) — arXiv:2605.14493 (E1)
9. China regional HANK — SSRN 6028234 (E0)
10. Deep learning four decades of human migration — Gaskin et al., Nature Comms (E1)
11. Closed-form gravity-like learned mobility — Simini et al., Nature Comms 2025 (E1)
12. OD of interprovincial floating population (J. Maps 2016) (E1)
13. Inter-provincial Migration Sub-flows (2010–2020) dataset, geodoi (E1)
14. CMDS annual migrant survey (E1)
15. Census 2000/2010/2020 + 1% surveys 2005/2015 (E1)

## 6. Direct comparison: Structural RL / DeepHAM / neural HJB / learned-flow-network

- **Structural RL** learns a perceived/compressed state and equilibrium policy in **single-region** HA models; does not learn interregional flow networks.
- **DeepHAM** learns global value/policy/distribution, **replacing** the household solver; single-region; no flow data.
- **Neural HJB/master-equation/PINN** methods solve the continuous-time household problem; single-region; no spatial links.
- **Learned flow/gravity networks** (Gaskin, Simini) learn interpretable bilateral migration/mobility flows from **real bilateral data** but are **not embedded in any economic equilibrium** (no market clearing, no HA/HANK).
- **NSR-HANK route** combines hard local structural modules + a learned interpretable interregional flow network `W^L` + real flow data + national general equilibrium. Components have precedent; the combination has **no single direct match** in this bounded search.

## 7. Novelty-boundary verdicts (five candidate claims)

| Claim | Verdict |
|---|---|
| Learned interpretable `W^L` inside regional HA/HANK (hard local modules) | PARTIAL_PRECEDENT |
| Cross-year shared network parameters + year-specific equilibria | NO_PRECEDENT_FOUND_IN_BOUNDED_SEARCH |
| Flow-supervised identification before GE embedding | NO_PRECEDENT_FOUND_IN_BOUNDED_SEARCH |
| Hold-out-year + hold-out-pair validation in structural regional HANK | NO_PRECEDENT_FOUND_IN_BOUNDED_SEARCH |
| Separation of observable flow identification from macro-equilibrium fitting | PARTIAL_PRECEDENT |

`NO_PRECEDENT_FOUND_IN_BOUNDED_SEARCH` is **not** a novelty claim; it is a bounded-search verdict that requires E3 verification before any novelty framing.

## 8. Chinese labor-flow data — candidate sources and recommendation

- **Anchor truth:** census long-form (2000/2010/2020) and 1% sample surveys (2005/2015) provide decennial/intercensal **5-year migration-transition** O-D matrices.
- **Annual structure:** CMDS (2009–2018) provides annual migrant **stock cross-tabs** (current residence × hukou origin); approximates year structure but is not a true annual flow.
- **Ready O-D-year candidate:** "Inter-provincial Migration Sub-flows (2010–2020)" (geodoi.ac.cn Id=3621) — derived annual sub-flows; **requires provenance/methodology audit before any use**.
- **Best current recommendation:** combine census/1%-survey transition matrices (anchor) + CMDS annual cross-sections (year structure), and treat the geodoi sub-flow dataset as a verification target, not an assumption. True multi-year O-D-year flows are `LIKELY_AVAILABLE_NEEDS_VERIFICATION` as transitions/derived flows; a genuine annual true-flow measure is `UNRESOLVED`.

## 9. Static/dynamic feature feasibility summary

- `Z_static_ij` (distance/adjacency/terrain): `AVAILABLE` (public GIS).
- `Z_node_i,t` (GDP pc, wage, population, urbanization, capital stock, fiscal): `LIKELY_AVAILABLE_NEEDS_VERIFICATION` (NBS yearbooks).
- `Z_node_i,t` returns/industrial-upgrading: `DIFFICULT` (needs construction/audit).
- `Z_pair_ij,t` gaps: `LIKELY_AVAILABLE_NEEDS_VERIFICATION` (derivable); accessibility change: `DIFFICULT`; bilateral history: `LIKELY_AVAILABLE_NEEDS_VERIFICATION`; policy links: `UNRESOLVED`.

## 10. Unresolved evidence/data blockers

1. China regional HANK (SSRN 6028234) must be read (E1/E2) to determine whether its links are learned or hand-specified — the single most decision-relevant open item.
2. geodoi sub-flow dataset methodology/provenance unverified (risk of interpolation).
3. True annual flow (vs transition/stock) measurement for `F^L_ij,t` unresolved.
4. Returns / industrial-upgrading / policy-link feature construction unresolved.
5. No E2/E3 literature; novelty framing blocked until DLH-1A E3 queue is worked.

## 11. Local Zotero paths/queries read (bounded, read-only)

- Read-only keyword scan over allowed text types (`.md/.txt/.csv/.json/.yaml/.yml`) for: `DeepHAM`, `structural reinforcement learning`, `neural HJB`, `master equation`, `differentiable`, `implicit layer`, `gravity model`, `migration`, `neural operator`, `equilibrium network`, `flow network`, `spatial HANK`, `regional HANK`, `Aiyagari`, `HANK`.
- Relevant local pointers (E0, process artifacts, no citation keys): `docs/kb_stage_reports/2026_06_15_current_papers_research_direction_scan/current_kb_paper_inventory_2026_06_15.csv`; `reports/stage3b/stage3b_research_radar_report.md` and `stage3b_priority_reading_queue.md`; `reports/stage2j/stage2j_batch_*.txt` (structural RL mentions). No PDF/SQLite access; no writes/cache/index/log; no copy-out.

## 12. Forbidden-operation counters (all zero)

- legacy Matlab reads = 0
- model/code writes (or migration) = 0
- model executions (Matlab/Python solver) = 0
- neural training/inference = 0
- data downloads/purchases/scraping/ingestion = 0
- package installs / environment mutation = 0
- GPU work = 0
- calibration/regression = 0
- PDF/full-text bulk download or commit = 0
- source-root writes/copy-outs = 0
- Results/policy claims = 0
- final novelty claims = 0
- governance changes = 0

## 13. Recommended next steps (suggestion only — no successor creation)

- Work the E3 human-verification queue (§ in `DLH_1A_E3_HUMAN_VERIFICATION_QUEUE.md`).
- `DLH-1B` (read-only audit of existing single-province Python kernel) — separate GitHub Issue.
- Then DLH-2 (Tier-0 HA benchmark) and DLH-5 data-source verification, subject to review.
