# Dissertation Chapter 5 R5 Python + AR(1) Rebuild Roadmap

Date: 2026-07-22  
Project: Codex + Zotero + Obsidian Research Workflow  
Repository for governance: `zcx369658780/Zotero-Analytical-Workflow-Skills`  
Route status: R5 planning approved / implementation not started

## 1. Route objective

Rebuild the Chapter 5 quantitative model in Python rather than continue patching the legacy Matlab architecture.

Scientific decisions already made in that historical R5 route:

- the primary shock law is a genuine AR(1);
- the baseline dynamic experiment is a one-innovation conditional IRF;
- full stochastic simulation is a later extension;
- R4H and the Matlab/parser lineage remain frozen historical evidence;
- no existing Matlab result is accepted as an R5 numerical oracle.

These decisions are historical reference only for the new Deep Learning + HANK project and are not automatically binding.

## 2. Historical target architecture

Recommended package layout in the old R5 planning route:

    chapter5_r5_python_model/
    ├── pyproject.toml
    ├── README.md
    ├── configs/
    ├── src/chapter5_model/
    │   ├── parameters.py
    │   ├── grids.py
    │   ├── regional_structure.py
    │   ├── household_hjb.py
    │   ├── distribution_kfe.py
    │   ├── aggregate_block.py
    │   ├── spatial_links.py
    │   ├── shocks.py
    │   ├── steady_state.py
    │   ├── transition.py
    │   ├── diagnostics.py
    │   └── io_contracts.py
    ├── tests/
    ├── experiments/
    └── outputs/

## 3. Historical stage map

| Stage | Name | Main deliverable | Exit condition | Relative completion |
|---|---|---|---|---:|
| R5-0 | Scientific specification, scope, repository boundary freeze | R5 model constitution | All core choices explicit; no unresolved implementation-critical concept | 8% |
| R5-1 | Legacy equation and dependency migration inventory | retain/redesign/drop map | Every core equation mapped to R5 modules | 18% |
| R5-2 | Python repository and testable scaffold | package + CI + manifests | Import/static/unit scaffold accepted | 27% |
| R5-3 | Steady-state kernel | small-grid steady state | Residual, mass, market-clearing and reproducibility gates pass | 45% |
| R5-4 | AR(1) engine | tested shock module | conditional and stochastic path tests pass | 55% |
| R5-5 | Minimal transition/conditional-IRF solver | one bounded diagnostic run | Short-horizon one-shock diagnostics pass | 70% |
| R5-6 | Numerical/economic validation | accepted diagnostic package | limiting cases, sensitivity and aggregation checks pass | 82% |
| R5-7 | Formal results and manuscript R5 | reviewed figures/tables and Results outline | Output review and claim matrix pass | 94% |
| R5-8 | Submission readiness | reproducibility and submission package | final model/manuscript/citation review pass | 100% |

Percentages described dependency-weighted progress, not calendar time.

## 4. Historical critical path

`R5-0 → R5-1 → R5-2 → R5-3 → R5-4 → R5-5 → R5-6 → R5-7 → R5-8`

The old route required steady-state and shock modules to be independently accepted before transition work.

## 5. Historical R5-0 decisions

The old planning route proposed freezing:

1. exact research question;
2. minimum mechanisms required for the paper;
3. state/control/aggregate variables;
4. state-owned capital stock representation;
5. regional/spatial link definition;
6. market-clearing equations;
7. AR(1) variable, units, mean, `rho`, `sigma`, frequency and innovation timing;
8. conditional IRF normalization;
9. baseline versus extension boundary;
10. legacy mechanisms to defer;
11. Python version and dependency policy;
12. repository name and visibility;
13. local source/test/output roots;
14. evidence and CI policy;
15. first implementation gate.

No code was to be written in R5-0.

## 6. Historical exit-gate ideas worth reusing

### Steady-state correctness

- HJB residual accepted;
- KFE/KF residual accepted;
- mass equals one within tolerance;
- non-negativity checks pass;
- market clearing passes;
- fixed point converges;
- repeated runs are identical;
- small-grid fixture archived.

### Shock correctness

- AR(1) recursion passes analytic tests;
- `rho=0`, `sigma=0`, stationary variance and seed tests pass;
- conditional IRF distinguished from stochastic realization;
- shock path provenance exported.

### Transition boundedness

- one authorized run only;
- no-overwrite output;
- short horizon;
- small grid;
- one shock;
- complete convergence and failure evidence;
- no Results claims.

### Validation

- limiting cases;
- sensitivity;
- regional aggregation;
- reproducibility;
- solver diagnostics;
- human review;
- evidence level sufficient for candidate outputs.

## 7. Main historical risks and controls

| Risk | Historical control |
|---|---|
| Mechanical translation of legacy errors | Equation-first migration inventory |
| Scope explosion | Minimum publishable model frozen before implementation |
| Solver runs without diagnostics | Residual/mass/convergence manifests |
| Confusion between AR(1) and decaying path | Separate law, innovation, conditional path and realization |
| Performance optimization too early | Profiling only after correctness |
| New engineering loop without paper progress | Each gate tied to research contribution |
| Output overclaim | Results blocked until validation review |
| Large/private files committed | Text-first manifests and explicit exclusions |
| Legacy Matlab reactivation | R4 route frozen read-only |

## 8. New-project disposition

This roadmap is **HISTORICAL_REFERENCE_ONLY**.

For the new Deep Learning + HANK project, the reusable lessons are the gate discipline, explicit diagnostics, no-old-output-oracle principle, and separation of economic definition from software/solver work. The new project must independently decide the deep-learning role, shock process, regional mechanisms, benchmark solver, and model scope through DLH-0.
