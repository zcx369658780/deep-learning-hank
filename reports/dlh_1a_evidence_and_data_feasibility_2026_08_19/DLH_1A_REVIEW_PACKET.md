# DLH-1A-R1 Review Packet — Evidence Correction (Corrected Evidence + Data Feasibility)

- Date: 2026-08-19 (R1)
- Author: DSH (bounded Builder)
- Authority: GitHub Issue #3 — DLH-1A; authoritative R1 correction comment (2026-08-19 08:12:28).
- Prior candidate: `2a04a737bd6aa62b00e8c39a9e2a2d7e3b22b021` — process PASS / evidence packet NOT ACCEPTED; R1 is authored fresh on current `origin/main` (no cherry-pick).
- Status: CANDIDATE evidence. Acceptance requires fresh-GitHub independent review (ChatGPT) + Owner direction.

## 1. Terminal classification

`DLH_1A_R1_EVIDENCE_CORRECTION_READY_FOR_GPT_REVIEW`

## 2. Baseline and branch

- Fresh baseline `origin/main` SHA: `4d7efa20c34daf2fc21bfc576899c4c77532eee9`
- Dedicated R1 branch: `dsh/issue-3-dlh-1a-r1-evidence-correction-2026-08-19`
- Candidate commit: single evidence commit at branch HEAD (2026-08-19, DSH); hash reported in the completion response. Expected delta: exactly the seven paths below, 0 behind / 1 ahead of baseline.
- `main` not modified.

## 3. Exact changed paths (same seven DLH-1A outputs, corrected)

1. `docs/literature/DLH_1A_NSR_HANK_LITERATURE_MAP_2026_08_19.md`
2. `docs/literature/DLH_1A_METHOD_AND_NOVELTY_BOUNDARY_MATRIX_2026_08_19.csv`
3. `docs/data/DLH_1A_CHINA_INTERPROVINCIAL_LABOR_FLOW_DATA_FEASIBILITY_2026_08_19.md`
4. `reports/dlh_1a_evidence_and_data_feasibility_2026_08_19/DLH_1A_EVIDENCE_REGISTER.csv`
5. `reports/dlh_1a_evidence_and_data_feasibility_2026_08_19/DLH_1A_E3_HUMAN_VERIFICATION_QUEUE.md`
6. `reports/dlh_1a_evidence_and_data_feasibility_2026_08_19/DLH_1A_REVIEW_PACKET.md`
7. `reports/dlh_1a_evidence_and_data_feasibility_2026_08_19/DLH_1A_FORBIDDEN_OPERATION_CHECK.md`

No roadmap, constitution, rule, Task Index, Startup Snapshot, README, source code, or historical evidence modified.

## 4. Literature candidates by evidence level (R1)

- E0: 8 · E1: 13 · E2: 0 (no full-text machine read newly performed) · E3: 0 · OWNER_PRIOR_WORK: 1 (SSRN 6028234, excluded from external counts)
- Total records: 22 (see evidence register)

## 5. Top material papers (evidence level in parens)

1. Structural RL for HA macro — Yang, Wang, Schaab, Moll, arXiv:2512.18892 (E1, description corrected)
2. DeepHAM — Han, Yang, E, QE 2026 / arXiv:2112.14377 (E1, distribution ≈ optimal generalized moments)
3. Master equation — Gu, Laurière, Merkel, Payne, arXiv:2406.13726 (E1, PRIMARY; added in R1)
4. Deep-MacroFin — arXiv:2408.10368 (E1)
5. PINN for HA models — arXiv:2511.20283 (E1)
6. SSJ + Deep Learning for HANK — Kase (E0)
7. Economics-Inspired NN — arXiv:2303.14802 (E1)
8. DL for solving/estimating dynamic models (survey) — arXiv:2605.14493 (E1)
9. **Owner prior multi-provincial HANK — SSRN 6028234 (OWNER_PRIOR_WORK; NOT external)**
10. Deep learning four decades of human migration — Gaskin et al. (E1)
11. Closed-form gravity-like learned mobility — Simini et al. (E1)
12. OD of interprovincial floating population (J. Maps 2016) (E1)
13. Inter-provincial Migration Sub-flows dataset — geodoi Id=3621 (E1, reclassified PROXY)
14. CMDS annual migrant survey (E1, reclassified cross-section)

## 6. Direct comparison (R1 corrected)

- **Structural RL** learns low-dimensional prices as state + learned equilibrium price dynamics (single-region HA, HANK app with forward-looking Phillips curve); no interregional flow network.
- **DeepHAM** learns value/policy with distribution ≈ optimal generalized moments (single-region; replaces solver; no flow data).
- **Master-equation / EMINN** (Gu et al. 2406.13726) represents value function with a NN after finite-dim distribution approximation (macro + spatial examples; not a learned interregional flow network).
- **Neural HJB/PINN** solve single-region continuous-time problems; no spatial links.
- **Learned flow/gravity networks** (Gaskin, Simini) learn bilateral flows from real data but are NOT embedded in HA/HANK (no clearing).
- **Multi-region HA/HANK external precedent: UNRESOLVED** — the only candidate found (SSRN 6028234) is Owner prior work, excluded.

## 7. Novelty-boundary verdicts (R1 recomputed after removing Owner prior work)

| Claim | Verdict |
|---|---|
| Learned interpretable `W^L` inside regional HA/HANK (hard local modules) | PARTIAL_PRECEDENT (external learned-flow component exists; external multi-region HA/HANK precedent UNRESOLVED) |
| Cross-year shared network parameters + year-specific equilibria | NO_PRECEDENT_FOUND_IN_BOUNDED_SEARCH |
| Flow-supervised identification before GE embedding | NO_PRECEDENT_FOUND_IN_BOUNDED_SEARCH |
| Hold-out-year + hold-out-pair validation in structural regional HANK | NO_PRECEDENT_FOUND_IN_BOUNDED_SEARCH |
| Separation of observable flow identification from macro-equilibrium fitting | PARTIAL_PRECEDENT |

`NO_PRECEDENT_FOUND_IN_BOUNDED_SEARCH` is **not** a novelty claim.

## 8. Labor-flow data — corrected classification and recommendation

Three tiers applied: `TRUE_ANNUAL_OD_FLOW`, `ANNUAL_OD_STOCK_OR_SAMPLE_CROSSTAB`, `MULTIYEAR_TRANSITION_OR_DERIVED_PROXY`.

- Census/1% survey → `MULTIYEAR_TRANSITION` (5-year O-D matrices; anchor truth).
- CMDS → `ANNUAL_OD_STOCK_OR_SAMPLE_CROSSTAB` (annual migrant cross-section; schema/weight verification required).
- geodoi Id=3621 → `MULTIYEAR_TRANSITION_OR_DERIVED_PROXY` (provincial aggregate / model-derived; **no proven pair-level fields**).

**Direct answer:** no published **true annual bilateral O-D flow matrix** is currently proven; credible bilateral destination-share labels for `W^L_ij,t` are `UNRESOLVED` and are the single most important remaining data blocker.

## 9. Feature feasibility summary (unchanged)

`Z_static` AVAILABLE; `Z_node` mostly LIKELY_AVAILABLE_NEEDS_VERIFICATION; returns/upgrading DIFFICULT; `Z_pair` gaps/bilateral-history LIKELY_NEEDS_VERIFICATION; accessibility DIFFICULT; policy links UNRESOLVED.

## 10. Unresolved evidence/data blockers

1. No credible bilateral `(i,j,t)` destination-share labels proven → supervised `W^L` blocked pending schema/data verification.
2. geodoi Id=3621 pair-level fields unproven (currently aggregate/proxy only).
3. CMDS O-D cross-tab + cross-year weight/sample/questionnaire harmonization unverified.
4. External multi-region HA/HANK literature boundary UNRESOLVED (Owner work excluded).
5. E3 = 0; novelty framing blocked until E3 queue worked.

## 11. Local Zotero paths/queries read (bounded, read-only)

- Read-only keyword scan over allowed text types for DLH-1A concepts (see R0 packet). Relevant local pointers (E0, no citation keys): `docs/kb_stage_reports/2026_06_15_current_papers_research_direction_scan/current_kb_paper_inventory_2026_06_15.csv`; `reports/stage3b/stage3b_research_radar_report.md` + `stage3b_priority_reading_queue.md`; `reports/stage2j/stage2j_batch_*.txt`. No PDF/SQLite; no writes; no copy-out.

## 12. Forbidden-operation counters (all zero)

- legacy Matlab reads = 0; model/code writes = 0; model executions = 0; neural training = 0; data downloads/purchases/scraping = 0; package installs = 0; GPU = 0; calibration/regression = 0; PDF/full-text bulk commit = 0; source-root writes/copy-outs = 0; Results claims = 0; final novelty claims = 0; governance changes = 0.

## 13. Recommended next steps (suggestion only — no successor creation)

- Work the E3 queue (especially geodoi schema + CMDS codebook verification).
- `DLH-1B` (read-only audit of existing single-province Python kernel) — separate GitHub Issue.
