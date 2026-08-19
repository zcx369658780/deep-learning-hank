# DLH-0R1 Review Packet — NSR-HANK Scientific Constitution Correction Candidate

- Date: 2026-08-19 (R1)
- Author: DSH (bounded Builder)
- Authority: GitHub Issue #2 — `DLH-0: Scientific constitution and model scope freeze`; authoritative revision comment (2026-08-19 07:27:53); `docs/roadmaps/DLH_MASTER_ROADMAP_INITIAL_2026_08_19.md` on fresh `origin/main`.
- Prior candidate: `b79b0310bffafaf2a9b562aff349f173dec7d5eb` — process-clean provenance only; **not merged, not frozen, not cherry-picked**. R1 is authored fresh on top of current `origin/main`.
- Status: **CANDIDATE**. This packet is completion evidence, not acceptance. Final acceptance requires fresh-GitHub independent review (ChatGPT) plus Owner scientific-direction confirmation.

## 1. Terminal classification

`DLH_0_R1_NSR_HANK_CONSTITUTION_CANDIDATE_READY_FOR_GPT_OWNER_REVIEW`

## 2. Baseline and branch

- Fresh baseline `origin/main` SHA: `f5733df81b0d2087dc9de6caf355a8bbfd60a22c`
  (tip commit `docs: refresh start-here for NSR-HANK roadmap`; main includes roadmap publish `3be4b43…`, DLH-0R1 activation `ef1d17d…`)
- Dedicated R1 branch: `dsh/issue-2-dlh-0-r1-nsr-hank-roadmap-alignment-2026-08-19`
- Candidate commit: single evidence commit at branch HEAD (2026-08-19, DSH); exact hash reported in the Builder completion response (a packet cannot self-reference its own commit hash). Expected delta: exactly the eight paths below, 0 behind / 1 ahead of the baseline.
- `main` not modified (remote `main` remains at the baseline SHA).

## 3. Exact changed paths (eight DLH-0 paths, corrected)

1. `docs/specifications/DLH_0_SCIENTIFIC_CONSTITUTION_CANDIDATE_2026_08_19.md`
2. `docs/specifications/DLH_0_RESEARCH_QUESTION_AND_CONTRIBUTION_OPTIONS_2026_08_19.md`
3. `docs/specifications/DLH_0_NEURAL_ROUTE_DECISION_MATRIX_2026_08_19.csv`
4. `docs/specifications/DLH_0_MINIMUM_ECONOMIC_MODEL_CONTRACT_2026_08_19.md`
5. `docs/specifications/DLH_0_VALIDATION_BENCHMARK_AND_SOFTWARE_BOUNDARY_2026_08_19.md`
6. `reports/dlh_0_scientific_constitution_2026_08_19/DLH_0_REVIEW_PACKET.md`
7. `reports/dlh_0_scientific_constitution_2026_08_19/DLH_0_EVIDENCE_SOURCE_MAP.csv`
8. `reports/dlh_0_scientific_constitution_2026_08_19/DLH_0_FORBIDDEN_OPERATION_CHECK.md`

No other tracked file modified (rules, Task Index, Startup Snapshot, roadmap, historical evidence, README, `.gitignore` untouched).

## 4. Corrected research question (R1)

Primary (draft): can the interregional **labor-flow network** of a multi-province economy be identified and represented as an interpretable, trainable network `W^L` — parameterized by time-invariant geography, time-varying regional development, and time-varying pair linkages, with parameters shared across years — such that, embedded in structural province-local HA/HANK modules and disciplined by national general equilibrium, it reproduces observed bilateral labor flows and regional equilibrium objects while passing economic-consistency diagnostics and hold-out-year / hold-out-pair validation?

Alternatives: (A1) economics-constrained household value/policy approximator; (A2) regional equilibrium/distribution compression. Details in `DLH_0_RESEARCH_QUESTION_AND_CONTRIBUTION_OPTIONS_2026_08_19.md`.

## 5. `W^L`-first architecture (R1)

- Working label: **Network-Structured Regional HANK (NSR-HANK)**.
- Province-local household/firm/HJB/KFE/accounting/clearing = structural hard modules.
- **First learned object = `W^L`** (two-stage flow model: `m^L_i,t = sigma(g_L(Z_i,t;phi_L))`; `W^L_ij,t = softmax_{j!=i}(s^L_ij,t)`; `F^L_ij,t = L^home_i,t * m^L_i,t * W^L_ij,t`).
- `W^K` later (transparent rules first, learned after labor baseline stable); `W^G` = separate central-government allocation layer (province revenue -> central -> transfers), not folded into `W^K`.
- Household home-region fixed; labor services mobile; permanent migration/hukou/housing deferred.
- GNN/message passing deferred until interpretable flow-weight baseline is stable.
- Route D retained as **benchmark/infrastructure** route only; Route A = fallback; B/C/GNN = deferred.

## 6. Cross-year static/dynamic feature contract

- `Z_static_ij` (time-invariant pair): geographic distance, adjacency, terrain, stable geography — identical across years, not re-estimated as year-varying.
- `Z_node_i,t` (time-varying node): GDP per capita, wage, returns, population, industrial structure, urbanization, capital stock, fiscal revenue/expenditure, industrial upgrading, coastal manufacturing/service structure, observable policy state.
- `Z_pair_ij,t` (time-varying pair): wage/GDP/return gaps, accessibility change, bilateral migration history, bilateral capital exposure, policy links.
- Contract: `W^L_ij,t = f_L(Z_static_ij, Z_node_i,t, Z_node_j,t, Z_pair_ij,t ; theta_L)` — `theta_L` shared across years; `W^L_t` varies with `Z_t`.

## 7. Yearly-equilibrium contract

- Each year solves a separate conditional equilibrium: `X*_t = T(X*_t ; theta, Z_t)`.
- Shared structural parameters + year-specific observables/equilibria; not a full dynamic transition system in the first generation.
- Validation: hold-out years and hold-out province pairs (leakage prevention); no pooled in-sample fit only.

## 8. Staged flow-training / GE logic

A. Flow-supervised pretraining (`theta_L = argmin L_flow`) with origin/destination share errors, hold-out year/pair, feature sensitivity, interpretable partial effects.
B. GE embedding: solve `X*_t(theta_hat_L)`, check province objects + national clearing/conservation.
C. Bounded equilibrium-constrained fine-tuning: `L = lambda_F*L_flow + lambda_M*L_macro + lambda_E*L_equilibrium + lambda_R*R(theta)`.
**Identification discipline: macro aggregates `Y/K/L` are NOT the sole identifiers of `W^L`; flow-data discipline preserved.**

## 9. Benchmark / HA tiering

- Tier 0 = one-region real one-asset **HA/Aiyagari computational benchmark** (not genuine HANK); Tier 1 = minimal genuine single-region HANK (NK nominal layer, DLH-3); Tier 2 = small multi-region NSR-HANK. Legacy Matlab outputs never truth.

## 10. Major unresolved scientific decisions (Owner/ChatGPT)

1. Final question wording / contribution framing (structural / empirical-identification / computational).
2. Genuine-HANK nominal closure (DLH-3) and one-asset/inelastic household persistence.
3. Benchmark shock freeze values vs regional exposure experiments.
4. First-generation O-D-year flow data source (DLH-1A/5).
5. DLH-4 (2-region hand-specified prototype) sequencing vs DLH-1 audits.

## 11. Candidate literature / source count by evidence level

| Evidence level | Count | Notes |
|---|---|---|
| E0 | 480 local matches (478 task-gate records + ~2 non-task) | local Zotero-workflow keyword hits; process artifacts; no citation keys |
| E1 | 0 | — |
| E2 | 0 | — |
| E3 | 0 | — |
| Repository files read | 14 | rules (8) + design (2) + historical (5, incl. CSV) + roadmap (1) — design inputs |
| GitHub sources | 1 | Issue #2 body + 2 comments |

- **Explicit statement: novelty is NOT E3-verified; no literature gap is manufactured; any unverified claim is E0/E1 and caveated.** DLH-1A must build the literature evidence base before any novelty framing.

## 12. Files read (fresh origin/main + GitHub)

- `project_rules/PROJECT_RULE_INDEX_CURRENT.md` + all 7 CURRENT rules (verified unchanged from previous baseline via git diff);
- `tasks/TASK_INDEX_CURRENT.md` (Status `ACTIVE_GITHUB_ISSUE_2_DLH_0_R1`);
- `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`;
- `docs/roadmaps/DLH_MASTER_ROADMAP_INITIAL_2026_08_19.md`;
- 2 design notes + 5 historical analyses (same paths as Issue #2 body; read via `git show origin/main:<path>`);
- GitHub Issue #2 body + all comments in chronological order (comment 1: ChatGPT process PASS / scientific direction pending; comment 2: authoritative Owner/Reviewer R1 revision).

## 13. Bounded Zotero-workflow reconnaissance (performed under Issue #2; results reused)

- Root `D:\Zotero-Analytical-Workflow`, read-only keyword scan over `.md/.txt/.csv/.json/.yaml/.yml` for the Issue's suggested concepts; no PDF/full-text, no SQLite, no writes/cache/index/log inside root, no copy-out. Result: 480 matched files, all classified E0/unverified; only safe metadata recorded in the evidence source map.

## 14. Forbidden-operation counters (all zero)

| Item | Count |
|---|---|
| legacy Matlab source reads | 0 |
| model code writes / migration | 0 |
| Matlab/Dynare/Octave executions | 0 |
| Python model/solver executions | 0 |
| neural training/inference | 0 |
| package installs / environment mutation | 0 |
| GPU experiments | 0 |
| calibration / data regression | 0 |
| PDF/full-text extraction | 0 |
| source-root copy-outs | 0 |
| Results/policy claims | 0 |
| governance/rule changes | 0 |

See `DLH_0_FORBIDDEN_OPERATION_CHECK.md`.

## 15. Recommendation for next gate (suggestion only — no successor creation)

`DLH-1` (A: literature evidence; B: read-only existing Python kernel audit) via a separate GitHub Issue; then DLH-2 (Tier-0 single-region HA computational benchmark). Only after DLH-0R1 is independently reviewed and the Owner confirms the corrected NSR-HANK constitution.
