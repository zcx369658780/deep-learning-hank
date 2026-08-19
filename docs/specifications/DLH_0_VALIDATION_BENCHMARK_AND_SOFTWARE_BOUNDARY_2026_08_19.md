# DLH-0R1 — Validation, Benchmark and Software Boundary — NSR-HANK (Candidate)

- Date: 2026-08-19 (R1 revision)
- Author: DSH (bounded Builder)
- Status: CANDIDATE for Owner/ChatGPT decision — design-level specification only.

## F. Benchmark / ground-truth strategy (no legacy oracle)

### F.1 Tiering (R1 correction)
- **Tier 0 = one-region real one-asset HA/Aiyagari computational benchmark** (DLH-2). It is a computational benchmark only; **never called the substantive/genuine HANK model**.
- **Tier 1 = minimal genuine single-region HANK** (DLH-3) with an NK nominal layer — separate structural layer.
- **Tier 2 = small multi-region NSR-HANK** (DLH-4→6) with hand-specified then learned `W^L`.

### F.2 Tier-0 benchmark checks (must pass)
- Analytic/limiting special cases (no-idiosyncratic-risk limit, `rho=0`/`sigma=0` AR(1) limits, degenerate grids, boundary/binding cases); small-grid transparent finite-difference HJB+KFE solver (DLH-2) as truth; HJB residual; KFE residual; `mass = 1`; non-negativity; market-clearing/accounting residuals; boundary feasibility; deterministic reproducibility (config hash, source SHA, seed, run manifest, no-overwrite outputs).

### F.3 Flow-network validation (primary route, mandatory)
- Flow-supervised pretraining reports: flow prediction error; **origin-share error**; **destination-share error**; feature sensitivity; interpretable partial effects; explicit gravity-style baseline comparison.
- **Hold-out-year validation** (train early years, validate later years) and **hold-out-province-pair validation** (withhold selected `(i,j)` pairs) — pooled in-sample fit alone is not acceptable (leakage prevention).
- Identification check: macro aggregates `Y/K/L` must NOT be the sole identifiers of `W^L`; a better GDP fit that destroys the observed flow network is a failure.

### F.4 GE embedding / fine-tuning validation
- After embedding trained `W^L(theta_hat_L)`: check province output, labor, capital, wage, return, distribution; national clearing; labor conservation (`sum_j F^L_ij,t = L^home_i,t * m^L_i,t`; inflows consistent); capital conservation (once `W^K`); goods/capital clearing; fiscal accounting (central layer); perturbation re-equilibration stability; parameter sensitivity; OOD on feature combinations; policy-counterfactual stability (later stages).
- Bounded fine-tuning keeps `lambda_F` flow discipline dominant; equilibrium constraints bounded (`lambda_E`, `lambda_M`), regularization `lambda_R`.

### F.5 Neural vs economic error separation
- Report both neural prediction error (vs flow data / vs solver truth) and economic residuals (of the embedded object). Small prediction error does not imply small economic residual. Acceptance requires economic-residual gates + OOS flow gates, not loss curves.

### F.6 Evidence levels
- Machine diagnostics = D2 at most until human review; D3/D4 only after independent review. No Results prose from DLH-0R1.

## G. Software / dependency boundary (design level only)

### G.1 Package layout concept (roadmap §7; no code written)
```
src/deep_learning_hank/
    economics/        # household, distribution, firms, fiscal, prices, market_clearing
    regional/         # regional_module, labor_flows, capital_flows, fiscal_transfers, features
    solvers/          # steady_state, equilibrium, transition
    learning/         # flow_models, objectives, constraints, training
    diagnostics/      # household, distribution, regional, national, learning
    data/             # schemas, transforms
    experiments/
    provenance/
```
- economics 不依赖 learning；learning 可以调用 economics/equilibrium；diagnostics 独立于 trainer。

### G.2 Technology roles
- **Python** = sole main implementation language.
- **PyTorch** = deep-learning dependency (flow networks / neural components only).
- **numpy/scipy** = transparent solvers.
- **Minimal dependency policy**; versions pinned at implementation; no package installation in DLH-0R1.

### G.3 Config / provenance / no-overwrite
- Immutable config per yearly equilibrium; source SHA / data manifest / feature schema recorded; run no-overwrite; failure = no automatic retry, diagnostics first; CPU small case before GPU (GPU later, separately authorized).

### G.4 Gate map (allowed vs forbidden)
| Gate | Allowed | Forbidden until |
|---|---|---|
| DLH-1A | literature evidence build (E1–E3) | model code |
| DLH-1B | read-only audit of existing single-province Python kernel (equation map, dependency map, reusable/redesign/drop, I/O contract, legacy-state audit, migration allowlist) | migration, execution |
| DLH-2 | Tier-0 HA/Aiyagari benchmark + diagnostics (CPU) | neural code, "HANK" labeling of Tier-0 results |
| DLH-3 | minimal genuine single-region HANK (NK nominal layer) | learned multi-region claims |
| DLH-4 | 2-region hand-specified `W^L` prototype | training |
| DLH-5 | learned `W^L` baseline (flow-supervised, OOS year/pair) | GNN/message passing |
| DLH-6 | 3–5 region GE integration | joint `W^L+W^K` training |
| DLH-7 | learned `W^K` after transparent capital baseline | joint training from scratch |
| DLH-8 | fiscal transfer module (observed transfers first) | learned `W^G` until later |
| DLH-9/10 | 31-province panel; policy experiments (after identification/OOS/diagnostics) | Results claims |
| DLH-11 | GNN/message-passing extension (after interpretable baseline stable) | earlier |

### G.5 Explicitly forbidden in DLH-0R1
- Python/model code creation or migration; legacy Matlab source reads; Matlab/Dynare/Octave execution; Python solver/model execution; neural training/inference; package/environment mutation; GPU; calibration/data regression; PDF/full-text extraction; source-root copy-out; Results/policy claims; final novelty claims; governance-rule changes; PR/merge/Issue close/successor/self-accept.
