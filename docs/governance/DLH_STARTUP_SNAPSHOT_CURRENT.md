# Deep Learning + HANK Startup Snapshot — CURRENT

Date: 2026-08-19

Repository: `zcx369658780/deep-learning-hank`

Local Owner-designated workspace: `D:\deep-learning-hank`

## Governance state

- live GitHub `main` = synchronized repository/governance authority；
- open GitHub Issue = sole DSH Builder task authority；
- `tasks/TASK_INDEX_CURRENT.md` = synchronized Issue pointer only；
- DSH = bounded Builder；
- ChatGPT = independent GitHub reviewer / scientific-route authority / task issuer；
- Owner = final scientific-direction authority。

## Accepted stages

- Issue #1 bootstrap: accepted/closed at `bcded9b9137f3c10f71a7a6ecb929f78b40bdc11`.
- Issue #2 DLH-0 scientific constitution: accepted/closed at `73e1ae5db9d7e362781a77fa2a204c80238fad3e`.
- Issue #3 DLH-1A literature/data feasibility: accepted/closed at `e9aa7dc8a3f5a198b1655c917659f519239eb67b`.
- Issue #4 DLH-1B Python kernel audit: accepted/closed at `8dce318af5ca704a747e67932ec3caa35f9168ad`.
- Issue #5 DLH-2A fixed-price HJB/KFE kernel: accepted/closed after R1 at `76b5882a63d8ade18d50098373b7c735eb2c4ca4`, evidence `D2_MACHINE_DIAGNOSTIC_ONLY`.
- Issue #6 DLH-2B single-region steady-state GE: accepted/closed after R1 at `c562ce3a2743ac779123918e9aab5f37044b564a`, evidence `D2_MACHINE_DIAGNOSTIC_ONLY`.
- Issue #7 DLH-2C robustness: fail-closed result independently accepted/closed at `583e352b3ba37d25ebb7d8f468b5fd9f4f5eb5d3` with classification `DLH_2C_BOUNDARY_SENSITIVITY_BLOCKED_ACCEPTED`, evidence `D2_MACHINE_DIAGNOSTIC_ONLY`.

## Accepted Tier-0 computational state

Under `VALIDATION_FIXTURE_NOT_CALIBRATION`:

- one-region real HA/Aiyagari closure remains `K -> (w,r) -> transfer -> HJB -> KFE -> A(K) -> K-A(K)`;
- accepted DLH-2B baseline at 40 points `[0,50]`: `K*=27.367823476711713`;
- HJB/KFE/effective-labor/fiscal/goods/household-budget/mean-drift gates pass;
- DLH-2B deterministic repeat differences are all `0.0`.

Issue #7 robustness evidence adds:

- fixed-bound grid refinement passes: B40_50→G80_50→G160_50 with `d40_80=0.004552056007726381`, `d80_160=0.002201396805130615`;
- all 80→160 reported macro relative differences remain <0.5%;
- state-label permutation invariance passes at machine precision;
- 21-point bounded capital-residual scan on `[0.5,45]` is finite with exactly one sign-changing interval;
- new-variant reproducibility differences are all `0.0`;
- accepted DLH-2A/DLH-2B regression remains 32/32 PASS;
- **upper-bound sensitivity fails** at matched spacing: `K50=27.243808136211925`, `K100=28.206080385009184`, `d50_100=0.03411577346665587 > 0.005`;
- upper-boundary mass falls from `0.012470893430997766` to `8.909775784954998e-05`; top-5% mass falls from `0.0337799583738194` to `0.0005909812829154132`;
- therefore `a_max=50` must not be treated as an adequate canonical numerical domain.

Issue #7 is accepted as a correct scientific fail-closed result, not retroactively converted into a robustness PASS.

## Authoritative scientific direction

Roadmap:
`docs/roadmaps/DLH_MASTER_ROADMAP_INITIAL_2026_08_19.md`.

Direction remains:
- Tier 0 = one-region real HA/Aiyagari computational benchmark;
- Tier 1 = minimal genuine single-region HANK nominal/New-Keynesian layer;
- Tier 2 = small multi-region NSR-HANK;
- structural household/firm/HJB/KFE/accounting/clearing stay hard economic modules;
- learned labor-flow network `W^L` first, `W^K` later;
- household home-region fixed initially, labor services mobile;
- cross-year shared network parameters with year-specific observables/weights/equilibria;
- GNN/message passing deferred.

## Current active task

Issue #8 — `DLH-2C-B1: Tier-0 asset-domain adequacy and upper-tail convergence validation`

Issue URL:
`https://github.com/zcx369658780/deep-learning-hank/issues/8`

Expected branch:
`dsh/issue-8-dlh-2c-b1-asset-domain-2026-08-19`

## DLH-2C-B1 scientific purpose

Issue #8 is a successor to the accepted Issue #7 blocker. It does not relax or rewrite the 50→100 failure. It grants new bounded authority to determine whether the asset domain converges by `a_max=200` while all economics and solver modules remain frozen.

Existing accepted/read-only points:
- C50 = 80 points `[0,50]`, spacing `50/79`;
- C100 = 159 points `[0,100]`, same spacing.

New authorized points:
- C150 = 238 points `[0,150]`, same coarse spacing `50/79`;
- C200 = 317 points `[0,200]`, same coarse spacing;
- F100 = 317 points `[0,100]`, fine spacing `25/79`;
- F200 = 633 points `[0,200]`, same fine spacing.

Mandatory questions:

1. Does the matched-spacing bound sequence 50→100→150→200 show non-worsening convergence with final `d150_200 <= 0.005`?
2. Does the accepted Issue #7 `d50_100` reproduce within `1e-12` as provenance?
3. Are the 100 and 200 upper-bound domains each stable to halving grid spacing, with `d_grid_100 <= 0.005`, `d_grid_200 <= d_grid_100+1e-12`, and `d_grid_200 <=0.005`?
4. Do all new variants pass accepted steady-state numerical/accounting gates and same-environment reproducibility `<=1e-12`?
5. Does the canonical test suite preserve the Issue #7 blocker as a provenance assertion instead of leaving an unexplained permanent red test?

## Current implementation/scientific authority

- DLH-2A fixed-price kernel: `R1_ACCEPTED_D2`；
- DLH-2B steady-state GE: `R1_ACCEPTED_D2`；
- DLH-2C robustness: `BOUNDARY_SENSITIVITY_BLOCKED_ACCEPTED_D2`；
- DLH-2C-B1 asset-domain adequacy: `ACTIVE_NOT_ACCEPTED`；
- genuine-HANK nominal implementation authority: `NONE`；
- regional/W authority: `NONE`；
- shock/transition authority: `NONE`；
- neural training authority: `NONE`；
- empirical calibration authority: `NONE`；
- Results/manuscript authority: `NONE`；
- final novelty claim authority: `NONE`。

## Current boundaries

Issue #8 may only use its exact tracked-path allowlist. Accepted economics/solver modules, accepted DLH-2A/DLH-2B tests, and Issue #7 reports/evidence remain frozen. The only previously accepted test authorized for narrow modification is `tests/test_dlh_2c_grid_boundary.py`, solely to convert the already-accepted boundary failure into a blocker-provenance regression assertion.

No regional/W, SOE/open-economy, nominal/NK, shock/transition, neural/RL, empirical data/calibration, Matlab/legacy Matlab, old-source-repo access or Results/policy/novelty work is authorized.

## Queued next gate — NOT ACTIVE

`DLH-3 — minimal genuine single-region HANK nominal/New-Keynesian layer` remains blocked until fresh independent disposition of Issue #8 establishes an adequate Tier-0 numerical asset domain or returns another accepted fail-closed result for scientific decision.