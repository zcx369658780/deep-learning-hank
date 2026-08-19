# DLH-1A-R1 — E3 Human-Verification Queue (Builder does NOT self-promote)

- Date: 2026-08-19 (R1 correction)
- Author: DSH (bounded Builder)
- Status: E3 = 0. This queue is a request for Owner/ChatGPT human verification; DSH may not promote any E0/E1/E2 entry to E3.

## 1. Queue (priority order, R1 corrected)

| Priority | Item | Evidence level now | What to verify | E3 criterion |
|---|---|---|---|---|
| 1 | geodoi Id=3621 dataset documentation/schema | E1 | whether ANY pair-level (i,j,t) O-D field actually exists (vs provincial aggregate inflow/outflow-rate components); licensing | human reads dataset docs/schema; confirms or refutes pair-level O-D fields |
| 2 | CMDS microdata codebook / questionnaire | E1 | whether origin × destination is constructible; cross-year weight/sample-design/questionnaire harmonization feasibility | human reads codebook + design docs |
| 3 | Structural RL (arXiv:2512.18892) | E1 | confirm low-dimensional price state + learned price dynamics + HANK/Phillips-curve application wording | human reads abstract + relevant sections |
| 4 | DeepHAM (QE 2026) | E1 | confirm "optimal generalized moments" distribution approximation + value/policy NN formulation | human reads abstract + method section |
| 5 | Master equation (Gu–Laurière–Merkel–Payne, arXiv:2406.13726) | E1 | confirm NN value function after finite-dim distribution approximation + spatial examples | human reads abstract |
| 6 | Owner prior work (SSRN 6028234) | OWNER_PRIOR_WORK | provenance confirmation only (author/venue/scope) for the historical-baseline record | human confirms authorship/scope; NOT promoted as external precedent |
| 7 | Census/1% survey migration-table documentation | E1 | confirm 5-year transition semantics and interprovincial O-D tabulation availability | human confirms official documentation |
| 8 | Gaskin et al. + Simini et al. (migration/gravity DL) | E1 | confirm flows learned but NOT embedded in structural HA/HANK (no clearing) | human reads abstracts |

## 2. Rules applied

- `PROJECT_RULE_RESEARCH_EVIDENCE_AND_CITATION_CURRENT.md`: E3 requires human reading + confirmed source/section provenance; machine evidence is at most E2 and not self-promotable.
- Owner prior work (SSRN 6028234) is recorded as `OWNER_PRIOR_WORK / PROJECT_PROVENANCE`, never as external literature precedent.
- No novelty claim may reference this queue until items reach E3.

## 3. Non-actions

- DSH did not open local PDFs, did not access SQLite/Zotero DB, did not copy out any file, and did not download/purchase/scrape any data or full text.
