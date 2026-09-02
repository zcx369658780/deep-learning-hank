# Deep Learning + HANK Startup Snapshot — CURRENT

Date: 2026-09-02

Repository: `zcx369658780/deep-learning-hank`

Local Owner-designated workspace: `D:\deep-learning-hank`

## Governance state

- live GitHub `main` = synchronized repository/code/governance authority;
- GitHub Issue = sole DSH Builder authority only after publication + Task Index / Startup synchronization + authoritative activation comment;
- DSH = bounded Builder/executor or bounded scientific analyst only under an active Issue;
- ChatGPT = independent fresh-GitHub reviewer / scientific-route advisor / task issuer / governance operator;
- Owner = final scientific authority for model-defining choices;
- Builder completion is not acceptance and Builder recommendation is not model freeze.

Priority:

`Scientific correctness > Experiment reproducibility > Research iteration speed > Git auditability > Documentation completeness`

## Current Builder state

Current published task:

**Issue #42 — DLH-5P: Specify unbounded-liquid analytic HJB authority and critical-transfer admissibility**

Task type:

`SCIENTIFIC_ANALYTIC_MODEL_SPECIFICATION__UNBOUNDED_LIQUID_HJB_ADMISSIBILITY_AND_CRITICAL_TRANSFER`

Dedicated branch:

`dsh/issue-42-dlh-5p-unbounded-liquid-hjb-specification-2026-09-02`

Builder authority becomes active only while Issue #42 remains OPEN, Task Index / Startup identity matches, and the authoritative activation comment is present.

Current master roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`

## Latest accepted gate — Issue #41 / DLH-5O

Accepted candidate:

`25645d2dd1963e8fc17176a7fadc16d914811221`

Reviewer acceptance comment:

`5504453148`

Acceptance integration commit:

`540b16ebd3a577a55ccd92a8d74ced373798557e`

Accepted verdict:

`DLH_5O_REV2_ACCEPTED__OUTCOME_B_SUPPORTED__P2_COEFFICIENT_AND_INWARD_SIGN_VALID_ONLY_UNDER_EXPLICIT_DERIVATIVE_CONTROL__ANALYTIC_MODEL_SPECIFICATION_OWNER_DECISION_REQUIRED`

Accepted terminal:

`DLH_5O_HJB_LIQUID_TAIL_DOMINANT_BALANCE_CONDITIONAL__MISSING_ANALYTIC_ASSUMPTIONS_IDENTIFIED`

## Owner decision after DLH-5O

Owner approved:

`APPROVE_UNBOUNDED_B_ANALYTIC_HJB_SPECIFICATION_GATE__THEORY_DESIGN_ONLY`

This authorizes Issue #42 as a specification-review gate only. It does not itself accept a continuous/unbounded HJB model, a transversality condition, P-TR as a model primitive, R/W, or any numerical domain.

## Controlling scientific interpretation

Accepted household source remains immutable/read-only:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

The accepted source is finite-grid MATLAB-faithful HJB authority. It fixes the household economics and finite-grid numerical semantics but does not itself specify an unbounded-positive-`b` HJB/transversality problem.

For fixed `a in [0,10]`, DLH-5O established only a conditional p=2 dominant-balance result. Under the complete conditional assumptions including

`P-TR: V_a/V_b = o(sqrt(b))` uniformly,

we have

```text
V_b ~ K/b^2
(rho+r_b)K - 2*sqrt(K) = S*K
K = 4/(rho+r_b)^2
c/b = (rho+r_b)/2 = 0.0175
mu_W/b -> -0.0025
```

This is conditional fixed-a liquid-tail inwardness, not an unconditional theorem and not full two-asset infinite-domain authority.

The controlling transfer HJB object is

```text
V_b * [d*(V_a/V_b - 1) - chi(d,a)]
```

and the unresolved critical regime is

`V_a/V_b ~ Theta(sqrt(b))`,

for which the transfer Hamiltonian is same-order at `O(1/b)` and changes the coefficient equation.

Reviewer comment `5504453148` controls two local clarifications:

- P-TR alone gives `d=o(sqrt(b))`, `chi=o(b)`, `mu_a=o(sqrt(b))`; bounded `O(1)` transfer/cost requires the stronger `V_a/V_b=O(1)` subcase.
- local p<1 exponent shorthand in DLH-5O is not controlling; downstream work uses the reviewer-corrected order comparison.

## DLH-5P scientific rationale

The next obstacle is no longer a numerical grid question. It is a model-definition question:

> Which continuous unbounded-liquid HJB problem and admissibility/transversality class is scientifically defensible, and does it derive or merely assume the derivative-control needed for the p=2 tail candidate?

Issue #42 therefore requires three candidate analytic specification packages:

- S1 minimal growth/admissibility;
- S2 economically mapped transversality/no-Ponzi style;
- S3 derivative-controlled admissibility.

The Builder must stress-test all three against endpoint consistency, P-TR circularity risk, the critical `R~Theta(sqrt(b))` branch, theorem existence/uniqueness/regularity requirements and falsification criteria. The output is an Owner decision packet, not accepted model authority.

## Controlling HJB/KFE rule

```text
HJB boundary policy <=> KFE boundary transition law
```

Issue #27 remains binding. Stationary KFE remains **NOT AUTHORIZED**.

R and W remain unfrozen. No `W_max`, new `b_max`, or new `a_max` is authorized.

## Exact Builder allowlist

Builder may create only:

1. `docs/design/DLH_5P_UNBOUNDED_LIQUID_HJB_ANALYTIC_SPECIFICATION_REVIEW.md`
2. `reports/dlh_5p_unbounded_liquid_hjb_specification_2026_09_02/` with exactly the eight report files frozen in Issue #42.

No existing tracked file may be modified by Builder.

## Scientific ceiling during Issue #42

- no accepted-source/economics mutation;
- no analytic-specification freeze or implementation;
- no R/W/W1/W2 selection;
- no `W_max` / new grid / new extent / new `a_max`;
- no HJB/KFE/grid/stationary run;
- no KKT implementation;
- no D1-D3 / regional GE / multi-province audit;
- no network training / nominal HANK;
- no calibration / policy / welfare / Results.

## DSH startup sequence

1. `Set-Location D:\deep-learning-hank`;
2. verify repository / remote / worktree / staging;
3. `git fetch origin` and record fresh `origin/main`;
4. read all CURRENT rules;
5. read Task Index, this Startup Snapshot and current Roadmap;
6. read Issue #42 full body and latest comments, including authoritative activation;
7. read Issue #41 acceptance/reviewer authority and accepted DLH-5O package read-only;
8. read accepted household source and relevant DLH-5M/5N context read-only;
9. verify Issue / Task Index / Startup identity exactly;
10. create the exact dedicated branch from fresh `origin/main`;
11. create only the Issue #42 allowlist files;
12. do not run HJB/KFE/grid/stationary experiments;
13. explicit-stage only allowlist paths, commit/push, and STOP for fresh ChatGPT review.

Chat text is not Builder authority.
