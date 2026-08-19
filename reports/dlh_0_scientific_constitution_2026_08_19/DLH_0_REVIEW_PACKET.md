# DLH-0 Review Packet — Deep Learning + HANK Scientific Constitution Candidate

- Date: 2026-08-19
- Author: DSH (bounded Builder)
- Authority: GitHub Issue #2 — `DLH-0: Scientific constitution and model scope freeze`
- Status: **CANDIDATE**. This packet is completion evidence, not acceptance. Final acceptance requires fresh-GitHub independent review (ChatGPT) plus Owner scientific-direction decision.

## 1. Terminal classification

`DLH_0_SCIENTIFIC_CONSTITUTION_CANDIDATE_READY_FOR_GPT_OWNER_REVIEW`

## 2. Baseline and branch

- Fresh baseline `origin/main` SHA: `56c9a72c652bdc75919121f6a5b2622583e397a9`
  (commit `governance: accept Issue #1 and activate DLH-0 Issue #2`)
- Dedicated branch: `dsh/issue-2-dlh-0-scientific-constitution-2026-08-19`
- Candidate commit: the single evidence commit at branch HEAD (2026-08-19, DSH). Exact hash is reported in the Builder completion response; the packet cannot self-reference its own commit hash. Expected delta: exactly the eight allowlisted paths below, 0 behind / 1 ahead of the baseline.
- `main` was not modified (remote `main` remains at the baseline SHA).

## 3. Exact changed paths (eight allowlisted outputs only)

1. `docs/specifications/DLH_0_SCIENTIFIC_CONSTITUTION_CANDIDATE_2026_08_19.md`
2. `docs/specifications/DLH_0_RESEARCH_QUESTION_AND_CONTRIBUTION_OPTIONS_2026_08_19.md`
3. `docs/specifications/DLH_0_NEURAL_ROUTE_DECISION_MATRIX_2026_08_19.csv`
4. `docs/specifications/DLH_0_MINIMUM_ECONOMIC_MODEL_CONTRACT_2026_08_19.md`
5. `docs/specifications/DLH_0_VALIDATION_BENCHMARK_AND_SOFTWARE_BOUNDARY_2026_08_19.md`
6. `reports/dlh_0_scientific_constitution_2026_08_19/DLH_0_REVIEW_PACKET.md`
7. `reports/dlh_0_scientific_constitution_2026_08_19/DLH_0_EVIDENCE_SOURCE_MAP.csv`
8. `reports/dlh_0_scientific_constitution_2026_08_19/DLH_0_FORBIDDEN_OPERATION_CHECK.md`

No other tracked file was modified (rules, Task Index, Startup Snapshot, historical evidence, README, `.gitignore` untouched).

## 4. Primary working research question (draft)

> For a minimal continuous-time heterogeneous-agent model with a small number of regions, can a neural **surrogate/accelerator** trained on a transparent small-grid reference solver approximate the household value/policy block (and later equilibrium objects) such that the neural model passes **economic-residual diagnostics** (HJB/KFE residual, market clearing, mass, boundary) with a measurable, auditable speedup on repeated experiments — i.e., a neural method that is scientifically auditable rather than a black box?

Alternatives (2) and contributions: see `DLH_0_RESEARCH_QUESTION_AND_CONTRIBUTION_OPTIONS_2026_08_19.md`.

## 5. Neural route decisions

- `PRIMARY_NEURAL_ROUTE` = **D — surrogate/accelerator around a transparent solver** (first target: household HJB value/policy block; ground truth = project-owned small-grid solver).
- `FALLBACK_NEURAL_ROUTE` = **A — household value/policy/HJB approximator** (in-loop replacement with economic constraints; higher novelty, harder).
- `DEFERRED_ROUTES` = **B** (equilibrium/transition solution operator) and **C** (distribution representation/compression), with explicit re-entry conditions (see decision matrix CSV).

## 6. Minimum household / economic structure (candidate)

- Single-region, **one-liquid-asset** continuous-time HANK baseline; idiosyncratic productivity `z` (finite-state Markov); consumption + saving controls; CRRA; **inelastic labor** in baseline; exogenous borrowing limit with explicit boundary treatment; KFE stationary distribution (`mass=1`); Cobb-Douglas firm; real model (nominal rigidity deferred); minimal balanced-budget fiscal; explicit market-clearing identities; stationary steady state; conditional perfect-foresight transition.
- Two-asset structure retained as first documented extension (historical reference, not binding).

## 7. Initial regional strategy

- Single-region first; small multi-region (2–3 regions) as documented second stage; full province dimension only after validation.
- Candidate links specified at spec level only: `W_asset` (recommended first link), `W_labor`, `W_trade`, shock-exposure `S` — row/column semantics, diagonal, normalization, accounting role defined; no empirical construction in DLH-0.

## 8. Initial shock concept

- Aggregate log-TFP AR(1), one-innovation conditional (perfect-foresight) transition path; freeze contract for DLH-3: variable, frequency (candidate annual), mean, `rho` (candidate 0.9), innovation normalization, `sigma` (candidate 0.01), exposure semantics, conditional-vs-stochastic interpretation. Second concept: common shock with regional exposure. No simulation in DLH-0.

## 9. Benchmark strategy

- Analytic/limiting special cases; small-grid transparent solver (DLH-2) as truth; residual-based validation (HJB/KFE/clearing/accounting); mass/non-negativity; boundary feasibility; deterministic reproducibility; **neural prediction error vs economic residual separation**; future OOD/sensitivity. No legacy Matlab oracle.

## 10. Major unresolved scientific decisions (Owner/ChatGPT)

1. Question framing: methodology (auditable neural-accelerator contract) vs mechanism vs both.
2. One-asset (recommended) vs two-asset first baseline.
3. Inelastic (recommended) vs elastic labor in baseline.
4. AR(1) freeze parameter values (rho/sigma/frequency).
5. Multi-region stage inside first paper path vs strictly after single-region validation.

## 11. Candidate literature / source count by evidence level

| Evidence level | Count | Notes |
|---|---|---|
| E0 (title/metadata level, unverified) | 2 local matches (non-task) + 478 task-gate records | local Zotero-workflow keyword hits; process artifacts, not literature |
| E1 | 0 | no verified abstract/intro-level sources |
| E2 | 0 | no machine-extracted verified notes |
| E3 | 0 | no human-verified literature |
| Repository design/historical files read | 7 | design inputs (non-authoritative): 2 design notes + 5 historical analyses |

- **Explicit statement: novelty is NOT E3-verified; no literature gap is manufactured. Any unverified claim is E0/E1 and caveated.** The local Zotero-workflow root yielded no verified literature notes for DL-for-HANK in bounded DLH-0 reconnaissance.

## 12. Files read from repository (fresh origin/main)

- `project_rules/PROJECT_RULE_INDEX_CURRENT.md` and all CURRENT rules required by it (7 files);
- `tasks/TASK_INDEX_CURRENT.md`;
- `design_notes/PYTHON_REBUILD_THINKING_FROM_SCRATCH.md`;
- `design_notes/LEGACY_REFERENCE_BOUNDARY.md`;
- `historical_model_analysis/00_HISTORICAL_EVIDENCE_INDEX.md`;
- `historical_model_analysis/01_CODEX_CH5_MODEL_EQUATION_READONLY_REPORT_2026_06_22.md`;
- `historical_model_analysis/04_R5_LEGACY_EQUATION_MIGRATION_MATRIX.csv`;
- `historical_model_analysis/05_R5_LEGACY_MIGRATION_STATUS_2026_07_22.md`;
- `historical_model_analysis/07_R5_PYTHON_AR1_REBUILD_ROADMAP_HISTORICAL_2026_07_22.md`;
- GitHub Issue #2 body + comments (0 comments) via REST API.

## 13. Bounded local Zotero-workflow reconnaissance (paths/queries read)

- Root: `D:\Zotero-Analytical-Workflow` (read-only, no writes/cache/index/log, no PDF/full-text, no SQLite, no copy-out).
- Queries: keyword presence scan (case-insensitive) over allowed text types (`.md`, `.txt`, `.csv`, `.json`, `.yaml`, `.yml`) for: `deep learning`, `neural`, `HJB`, `HANK`, `heterogeneous agent`, `DeepHAM`, `operator`, `surrogate`, `value function`, `policy function`, `distribution`, `spatial`, `multi-region`.
- Result: 480 matched text files; 478 are `tasks\` historical process-gate records (not literature); ~2 other matches (root-level `26_06_23.md`; `tools\dissertation_ch5_r5\formal_transition_package_contract.json`); additional process reports under `reports\stage2*`/`stage3*`, `reports\urhank_*`, `skills\research_workflow\*` also matched keywords but are process/skill artifacts. **No citation keys and no evidence-level markers found in frontmatter; all matches classified E0/unverified.** Safe metadata only is recorded in the evidence source map; no note bodies or quotations were extracted.

## 14. Forbidden-operation counters (all zero)

| Item | Count |
|---|---|
| legacy Matlab source reads | 0 |
| model code writes | 0 |
| Matlab executions | 0 |
| Python model executions | 0 |
| neural training | 0 |
| package installs | 0 |
| Results claims | 0 |
| legacy-root writes | 0 |
| PDF/full-text extraction | 0 |
| copy-outs from either legacy root | 0 |
| governance/rule changes | 0 |

See `DLH_0_FORBIDDEN_OPERATION_CHECK.md` for the command-level check.

## 15. Recommendation for next gate (suggestion only — no successor creation)

`DLH-1` — read-only reference extraction and **E1–E3 literature evidence build-up** (requires a separate GitHub Issue). DLH-2 (transparent economic baseline + small-grid solver) only after DLH-0 is independently reviewed and the Owner decides the scientific direction.
