# Deep Learning + HANK Task Index

Status: `ACTIVE_GITHUB_ISSUE_8_DLH_2C_B1`

## Accepted predecessors

### Issue #1 — local/GitHub bootstrap
Status: `ACCEPTED_AND_CLOSED`
Accepted commit: `bcded9b9137f3c10f71a7a6ecb929f78b40bdc11`

### Issue #2 — DLH-0 / NSR-HANK scientific constitution
Status: `DLH_0_R1_NSR_HANK_SCIENTIFIC_CONSTITUTION_ACCEPTED_AND_CLOSED`
Accepted commit: `73e1ae5db9d7e362781a77fa2a204c80238fad3e`

### Issue #3 — DLH-1A literature / labor-flow data feasibility
Status: `DLH_1A_R1_EVIDENCE_AND_DATA_FEASIBILITY_ACCEPTED_AND_CLOSED`
Accepted commit: `e9aa7dc8a3f5a198b1655c917659f519239eb67b`

### Issue #4 — DLH-1B Python kernel read-only audit
Status: `DLH_1B_R2_PYTHON_KERNEL_READONLY_AUDIT_ACCEPTED_AND_CLOSED`
Accepted commit: `8dce318af5ca704a747e67932ec3caa35f9168ad`

### Issue #5 — DLH-2A fixed-price HJB/KFE validation
Status: `DLH_2A_R1_TIER0_KERNEL_FIXED_PRICE_VALIDATION_ACCEPTED_AND_CLOSED`
Accepted commit: `76b5882a63d8ade18d50098373b7c735eb2c4ca4`
Evidence: `D2_MACHINE_DIAGNOSTIC_ONLY`.

### Issue #6 — DLH-2B single-region Tier-0 steady-state GE
Status: `DLH_2B_R1_TIER0_SINGLE_REGION_STEADY_STATE_GE_ACCEPTED_AND_CLOSED`
Accepted commit: `c562ce3a2743ac779123918e9aab5f37044b564a`
Evidence: `D2_MACHINE_DIAGNOSTIC_ONLY`.

### Issue #7 — DLH-2C numerical robustness
Status: `DLH_2C_BOUNDARY_SENSITIVITY_BLOCKED_ACCEPTED_AND_CLOSED`
Accepted fail-closed commit: `583e352b3ba37d25ebb7d8f468b5fd9f4f5eb5d3`
Evidence: `D2_MACHINE_DIAGNOSTIC_ONLY`.

Accepted scientific findings from Issue #7:
- all per-variant HJB/KFE/equilibrium/accounting gates pass;
- fixed-bound grid refinement passes: `d40_80=0.004552056`, `d80_160=0.002201397`;
- state-label permutation invariance passes at machine precision;
- 21-point bounded residual scan has exactly one finite sign-changing interval;
- deterministic repeat differences are all `0.0`;
- **asset-upper-bound gate fails materially** at matched spacing: `K50=27.2438081362`, `K100=28.2060803850`, `d50_100=0.03411577346665587 > 0.005`;
- upper-boundary mass falls `0.012470893 -> 8.909776e-05` and top-5% mass falls `0.033779958 -> 0.000590981` when `a_max` doubles;
- therefore `a_max=50` is not an adequate canonical numerical domain.

Authoritative roadmap:
`docs/roadmaps/DLH_MASTER_ROADMAP_INITIAL_2026_08_19.md`

## Sole active Builder authority

GitHub Issue #8:

`DLH-2C-B1: Tier-0 asset-domain adequacy and upper-tail convergence validation`

Issue URL:
`https://github.com/zcx369658780/deep-learning-hank/issues/8`

Builder: DSH

Expected branch:
`dsh/issue-8-dlh-2c-b1-asset-domain-2026-08-19`

## Current gate purpose

Issue #8 grants new authority to resolve the accepted Issue #7 boundary blocker without relaxing it.

All accepted economics and solver modules remain frozen. The task tests asset-domain adequacy using:

- accepted coarse-spacing C50 = 80 points `[0,50]`;
- accepted coarse-spacing C100 = 159 points `[0,100]`;
- new C150 = 238 points `[0,150]`;
- new C200 = 317 points `[0,200]`;
- new F100 = 317 points `[0,100]` with half the coarse spacing;
- new F200 = 633 points `[0,200]` with the same fine spacing as F100.

Mandatory questions:

1. Does matched-spacing bound convergence improve from 50→100→150→200, with final `d150_200 <= 0.005`?
2. Are the `a_max=100` and `a_max=200` domains each stable to halving the grid spacing, with final wide-domain grid difference <= 0.5% and non-worsening?
3. Do all new variants preserve the accepted steady-state numerical/accounting gates and deterministic reproducibility?
4. Does the accepted Issue #7 blocker remain preserved as provenance rather than being rewritten as a PASS?

## Scope boundary

Issue #8 remains `VALIDATION_FIXTURE_NOT_CALIBRATION`, real single-region Tier-0 only.

It does **not** authorize:
- modification of accepted household/KFE/firm/fiscal/steady-state solver/economics modules;
- modification of accepted DLH-2A/DLH-2B tests;
- rewriting accepted Issue #7 reports/evidence;
- expansion beyond `a_max=200`;
- regional / `W^L` / `W^K` / old W;
- SOE / RegionalAccounts;
- nominal/Fisher/NKPC/Taylor mechanisms;
- shocks/transition;
- neural/RL;
- empirical data/calibration/regression;
- Matlab/legacy Matlab or old-source-repo access;
- Results/policy/novelty claims;
- PR/merge/Issue-close/successor/self-accept by Builder.

## Queued next gate — NOT ACTIVE

`DLH-3 — minimal genuine single-region HANK nominal/New-Keynesian layer` remains blocked until Issue #8 receives fresh independent disposition and the Tier-0 asset domain is judged numerically adequate.