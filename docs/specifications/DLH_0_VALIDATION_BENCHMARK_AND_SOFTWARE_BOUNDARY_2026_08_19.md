# DLH-0 — Validation, Benchmark and Software Boundary (Candidate)

- Date: 2026-08-19
- Author: DSH (bounded Builder)
- Status: CANDIDATE for Owner/ChatGPT decision — design-level specification only.

## F. Benchmark / ground-truth strategy (no legacy oracle)

The neural model is judged **without using legacy Matlab outputs as truth**. Ground truth comes from the project's own transparent reference solver plus analytic special cases.

### F.1 Analytical / limiting special cases (must pass)
- No-idiosyncratic-risk limit (`sigma_z -> 0`): model collapses toward representative-agent-consistent aggregates.
- Stationary-variance tests: `rho = 0`, `sigma = 0` AR(1) limits; ergodic variance formula for the frozen AR(1).
- Degenerate grids / boundary cases: borrowing limit binding region; corner of `a` grid; single-`z`-state case.
- Aggregate consistency: one-region baseline reproduces the textbook Aiyagari steady state within documented tolerance (this is a NEW-model benchmark, not a legacy-output oracle).

### F.2 Small-grid transparent solver benchmark (built in DLH-2)
- A simple, fully documented finite-difference HJB + KFE solver on small grids (candidate ~50 asset points x 2-3 `z` states), implemented in plain Python/numpy.
- Serves as (a) the training-data generator for the neural surrogate, and (b) the validation truth.
- Deterministic reproducibility: same config/seed -> identical outputs; run manifest (config hash, source SHA, timestamps, output root).

### F.3 Residual-based validation (mandatory, independent of neural loss)
- HJB residual; KFE residual; market-clearing residual; budget/accounting identity residual.
- Distribution checks: `mass = 1` within tolerance; non-negativity; moment checks (mean asset, optionally Gini).
- Boundary feasibility: no consumption<=0; borrowing limit respected; policy functions within grid/bounds.

### F.4 Neural prediction error vs economic residual separation (core methodological rule)
- Report BOTH: (i) neural prediction error vs solver truth (interpolation/generalization error), (ii) economic residuals of the neural output inside the equilibrium object. Small prediction error does NOT imply small economic residual. Acceptance requires economic-residual gates, not loss curves.

### F.5 Future OOD / sensitivity tests (deferred to later stages)
- Extrapolation beyond training parameter ranges (`rho`, `sigma`, `gamma`); sensitivity of residuals to grid size, `z` states, region count; documented failure modes.

### F.6 Evidence levels
- Per `PROJECT_RULE_RESEARCH_EVIDENCE_AND_CITATION_CURRENT.md`: machine diagnostics = D2 at most until human review; D3/D4 only after independent review. No Results prose from DLH-0.

## G. Software / dependency boundary (design level only)

### G.1 Package layout concept (from design note; no code written)
```
src/deep_learning_hank/
    economics/       # parameters, grids, household, distribution, firms, regional_links, market_clearing, shocks
    solvers/         # steady_state, transition (transparent reference solver)
    neural/          # architectures, objectives, constraints, datasets, trainers
    diagnostics/     # economic_residuals, numerical_checks, neural_validation
    experiments/     # configs + run drivers
    provenance/      # manifests, no-overwrite output roots
```
- economics 与 neural 分层：neural model 不拥有经济定义 authority；diagnostics 独立于 trainer。

### G.2 Technology roles
- **PyTorch**: the only deep-learning dependency (neural approximation/training only).
- **numpy/scipy**: transparent solvers (HJB finite differences, KFE, fixed point).
- **Minimal dependency policy**: no heavy ecosystem imports at baseline; versions pinned at implementation; no package installation in DLH-0 (and none authorized before DLH-2+).

### G.3 Config / provenance / no-overwrite principles
- Immutable config (candidate: YAML/TOML) bound to source identity (git SHA) at run start.
- Output root: no-overwrite, timestamped run directories; every run writes a manifest (config hash, source SHA, seed, command, environment summary).
- Failure policy: no automatic retry; no overwrite; diagnostics-first.

### G.4 CPU-small-case before GPU
- DLH-2/4 baseline and neural prototype run on **CPU small cases only**. GPU scaling is forbidden until DLH-7 and requires a separate authorization (exact config, command, device, timeout, output root).

### G.5 What may be implemented when (gate discipline)
| Gate | Allowed implementation | Forbidden until |
|---|---|---|
| DLH-2 | transparent economic baseline: parameters/grids/household/firm/clearing + small-grid solver + diagnostics | neural code, training, surrogates |
| DLH-3 | neural method specification (frozen inputs/outputs, loss, constraints, data provenance, splits, OOD test) | any neural implementation |
| DLH-4 | small neural prototype (CPU), neural metrics + economic diagnostics jointly | full-scale training, GPU |
| DLH-5 | economic-consistency validation (residual/mass/clearing/boundary/OOD) | Results claims |
| DLH-6/7 | transition experiments, scaling, GPU (only with separate authorization) | Results prose |

### G.6 Explicitly forbidden in DLH-0
- Creating/editing Python model implementation; Matlab/Dynare/Octave execution; Python model or numerical solver execution; neural training/inference; package installs; GPU; calibration; data analysis/regression; full legacy-root inventory; legacy Matlab source read; PDF/full-text extraction; copy-out from either legacy root; Results prose; final novelty claims; changing governance rules.
