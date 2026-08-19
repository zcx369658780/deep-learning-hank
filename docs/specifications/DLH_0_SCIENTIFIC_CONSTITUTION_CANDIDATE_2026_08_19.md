# DLH-0R1 Scientific Constitution — Network-Structured Regional HANK (NSR-HANK) Candidate (NOT FROZEN)

- Date: 2026-08-19 (R1 revision)
- Author: DeepSeek Harness (DSH) — bounded Builder
- Authority: GitHub Issue #2 — `DLH-0: Scientific constitution and model scope freeze`; authoritative revision comment (2026-08-19 07:27:53) + `docs/roadmaps/DLH_MASTER_ROADMAP_INITIAL_2026_08_19.md` on fresh `origin/main`.
- Prior candidate: `b79b0310bffafaf2a9b562aff349f173dec7d5eb` — process-clean provenance only; **not** merged, **not** frozen authority.
- Status: **CANDIDATE — NOT_FROZEN**. Freeze requires fresh-GitHub review (ChatGPT) + Owner scientific-direction confirmation.

> This document is planning/specification only. It authorizes no model code, no migration, no execution, no training, no package installs, no calibration, no Results.

## 0. Terminal classification

`DLH_0_R1_NSR_HANK_CONSTITUTION_CANDIDATE_READY_FOR_GPT_OWNER_REVIEW`

## 1. Working model label and core idea

**Working model: Network-Structured Regional HANK (NSR-HANK).** (Working label; no novelty claim.)

Core idea (roadmap §0): deep learning does **not** replace province-local HJB/KFE/economic equations. The first generation keeps local structural economic modules as **hard modules**, and represents interregional labor, capital, and fiscal links as **interpretable, trainable network weights**, jointly disciplined by real flow data and national general equilibrium.

`Regional structural modules -> learned interregional flow networks -> national market clearing -> regional prices -> regional structural modules`

## 2. Owner-frozen scientific direction (R1) — implementation in this constitution

1. **NSR-HANK** is the working model label (not a novelty claim).
2. **Province-local household / firm / HJB / KFE / accounting / clearing remain structural hard economic modules.** Neural networks do not re-derive local economics.
3. **First learned object = interpretable interregional labor-flow network `W^L`** (not a surrogate HJB solver, not abstract message passing).
4. **`W^K` (capital-flow network) enters later**, only after the labor-flow baseline is stable.
5. **Fiscal transfers are modeled as a separate central-government allocation layer** (`W^G`), not folded into ordinary capital flows.
6. **Household home-region identity is fixed in the first generation; labor services may be allocated across provinces.** Permanent migration / hukou / housing deferred.
7. **Python is the implementation language.** Existing single-province Python HJB + firm iteration code is a **candidate reusable kernel subject to DLH-1B audit** — not automatic model authority.
8. **A one-region real one-asset HA/Aiyagari model is only a computational benchmark**, not the substantive/genuine HANK model.
9. **A minimal genuine single-region HANK (NK nominal layer) is a separate subsequent structural layer** (DLH-3) before learned multi-region HANK claims.
10. **Interregional implementation sequence:** hand-specified `W^L` in a 2-region prototype -> learned `W^L` -> 3–5 region equilibrium integration -> learned `W^K` -> fiscal module -> full provinces.
11. **GNN / message passing / learned regional messages are deferred** until the interpretable flow-weight baseline is stable.
12. **Legacy Matlab outputs remain non-authoritative and are never numerical truth.**

## 3. Neural role decision (R1 correction of the R0 route decision)

- `PRIMARY_NEURAL_ROUTE` = **learned interpretable interregional flow network (labor flows `W^L` first)** — flow-supervised, GE-embedded, equilibrium fine-tuned (Route E in the decision matrix).
- Route D (surrogate/accelerator around a transparent solver) is retained as **benchmark/infrastructure route** — NOT the primary scientific contribution (Comment 1 correction).
- `FALLBACK_NEURAL_ROUTE` = **economics-constrained household HJB/value-policy approximator** (Route A) — remains a candidate first-paper scientific neural target conditional on DLH-1A literature evidence.
- `DEFERRED_ROUTES` = equilibrium/transition solution operator (B), distribution representation/compression (C), and GNN/message passing.

## 4. Minimum economic structure (R1 corrected)

- **Province-local hard modules:** household HJB + KFE/stationary distribution, budget constraint, firm production/FOC, market clearing, accounting identities — all structural, per province.
- **Household:** fixed home-region identity; one-liquid-asset baseline for the single-region computational benchmark; controls consumption/saving; labor services allocatable across provinces through the two-stage labor-flow model (roadmap §3.1).
- **Benchmark vs genuine HANK tiering:**
  - Tier 0: one-region real one-asset **HA/Aiyagari computational benchmark** (not HANK);
  - Tier 1: **minimal genuine single-region HANK** with NK nominal layer (separate structural layer, DLH-3);
  - Tier 2: small multi-region NSR-HANK with learned `W^L` (DLH-4→6).
- **Nominal rigidity:** deferred from the benchmark; enters at the minimal genuine HANK layer (DLH-3).
- **Fiscal:** separate central-government allocation layer (province revenue -> central government -> province transfers); observed transfers as data constraints initially.
- **Shock concept:** aggregate TFP AR(1) as the benchmark shock; genuine-HANK and regional experiments remain open until the nominal/HANK layer and paper question are decided.
- Full contract: `DLH_0_MINIMUM_ECONOMIC_MODEL_CONTRACT_2026_08_19.md`.

## 5. Cross-year structure (mandatory contract)

Explicit separation of feature types:

- **Time-invariant pair features** `Z_static_ij`: geographic distance, adjacency, terrain, stable geography (identical across years; must not be re-estimated as year-varying).
- **Time-varying node features** `Z_node_i,t`: GDP per capita, wage, returns, population, industrial structure, urbanization, capital stock, fiscal revenue/expenditure, industrial upgrading, coastal manufacturing/service structure, observable policy state.
- **Time-varying pair features** `Z_pair_ij,t`: wage/GDP/return gaps, accessibility change, bilateral migration history, bilateral capital exposure, policy links.

**First-generation cross-year contract:**

`W^L_ij,t = f_L(Z_static_ij, Z_node_i,t, Z_node_j,t, Z_pair_ij,t ; theta_L)`

- `theta_L` is **structurally shared across years**; `W^L_t` changes with year-specific observables.
- **Each year solves a separate conditional equilibrium:** `X*_t = T(X*_t ; theta, Z_t)`.
- This preserves year-by-year steady-state logic while enabling pooled cross-year learning.
- **Validation must include hold-out years and hold-out province pairs** (no pooled in-sample fit only).

## 6. Learning / identification contract (staged)

A. **Flow-supervised pretraining:** learn `theta_L` from origin-destination-year labor-flow data `(i, j, t, F^L_ij,t)`; report flow prediction, origin-share error, destination-share error, hold-out year/pair performance, feature sensitivity, interpretable partial effects.
B. **General-equilibrium embedding:** embed trained `W^L(theta_hat_L)` into the regional HA/HANK system; solve `X*_t(theta_hat_L)`; check province output/labor/capital/wage/return/distribution/national clearing.
C. **Bounded equilibrium-constrained fine-tuning** (only after A/B pass): `L = lambda_F * L_flow + lambda_M * L_macro + lambda_E * L_equilibrium + lambda_R * R(theta)`.

**Identification discipline: macro aggregates `Y/K/L` must NOT be the sole identifiers of `W^L`.** Flow-data discipline is preserved so a better GDP fit cannot freely destroy the observed migration network.

## 7. Validation / benchmark strategy (no legacy oracle)

- Tier-0 HA benchmark with analytic limiting cases + deterministic diagnostics (HJB residual, KFE mass=1, non-negativity, clearing, accounting).
- Flow-network validation: hold-out years, hold-out province pairs, origin/destination share errors, OOS generalization.
- GE validation: equilibrium residuals, labor conservation, capital conservation, goods/capital clearing, fiscal accounting, national identities, perturbation re-equilibration stability.
- Neural prediction error separated from economic residual; CPU-small-case before GPU; reproducibility manifests.

## 8. Software / dependency boundary (design level only)

- Package layout concept per roadmap §7 (`src/deep_learning_hank/`: `economics/`, `regional/`, `solvers/`, `learning/`, `diagnostics/`, `data/`, `experiments/`, `provenance/`).
- economics does not depend on learning; learning may call economics/equilibrium; diagnostics independent of trainer.
- Python main language; PyTorch = deep-learning dependency; numpy/scipy for solvers; minimal dependency policy; immutable config; no-overwrite run outputs; source SHA/data manifest/feature schema recorded; CPU small cases first, GPU later.
- Existing single-province Python kernel: audit-only in DLH-1B (equation map, dependency map, reusable/redesign/drop, I/O contract, legacy-state audit, migration allowlist). No migration in DLH-0R1.

## 9. Evidence discipline

- No E3-verified literature exists yet; **novelty is NOT claimed**. DLH-1A must build the literature evidence base (Structural RL, DeepHAM, neural HJB, neural operators, differentiable equilibrium, learned economic networks, flow/gravity neural models, spatial HA/HANK).
- Local Zotero-workflow reconnaissance (DLH-0) found only E0-level process artifacts; zero citation keys; no verified literature notes. See `DLH_0_EVIDENCE_SOURCE_MAP.csv`.

## 10. Scientific state entering R1 -> after this candidate

| Item | Entering R1 | After this candidate |
|---|---|---|
| master roadmap | INITIAL_V0_1_PUBLISHED | unchanged (roadmap untouched) |
| DLH-0 constitution | R1_CORRECTION_ACTIVE_NOT_FROZEN | CANDIDATE (awaiting review) |
| primary learned object | OWNER_DIRECTION_WL_FIRST | CANDIDATE: `W^L` first, `W^K` later |
| model implementation | NOT_STARTED | NOT_STARTED |
| code migration authority | NONE | NONE |
| Matlab/Python execution, training, results, claims | NONE | NONE |

## 11. Major unresolved scientific decisions (Owner/ChatGPT)

1. Final primary research-question wording and contribution framing (structural / empirical-identification / computational layers).
2. Genuine-HANK nominal closure details (DLH-3 layer) and whether the substantive HANK household block stays one-asset/inelastic.
3. AR(1) benchmark shock freeze values vs region-exposure experiments for the substantive model.
4. First-generation flow data source and its O-D-year structure (DLH-1A/5 decision).
5. Whether the 2-region hand-specified `W^L` prototype (DLH-4) precedes literature/kernel audits or runs in parallel with DLH-1.

## 12. Recommended next gate (suggestion only — no successor creation)

`DLH-1` (A: literature evidence; B: existing Python kernel audit) via a separate GitHub Issue; then DLH-2 (single-region HA computational benchmark). Only after DLH-0R1 is independently reviewed and the Owner confirms the corrected constitution.
