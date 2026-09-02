# DLH-5R — Forbidden-Operation / Scope Check (Issue #44 §14)

DLH-5R is an **HJB-only numerical falsification** gate. DSH performed NONE of
the following during DLH-5R; no accepted source, economics, domain, numerical,
or governance object was modified.

| Forbidden operation (Issue #44 §14) | Status |
|---|---|
| Modify the accepted household source `matlab_faithful_two_asset_ha.py` | NOT PERFORMED — imported read-only; runtime blob check `76ae5b149993…` PASS; `git rev-parse` unchanged |
| Modify economics / FOCs / adjustment cost / taper / prices / calibration | NOT PERFORMED — frozen D0 economics used verbatim |
| Run a new b extent beyond b160 (b180/b200) | NOT PERFORMED — only b120/b140/b160, b160 = HARD ROUTE CEILING |
| Change b_lo / a_max / b resolution / taper extrapolation / adaptive seventh grid | NOT PERFORMED — `b_lo=-2`, `db=7/19`, `a in [0,10]`, `a_max=10`, mature DLH-5J grids only |
| Choose / implement R/W/W1/W2/`W_max` | NOT PERFORMED |
| Implement endpoint KKT / production-domain law | NOT PERFORMED |
| Run stationary KFE / nullspace / pin / density / tail mass | NOT PERFORMED — HJB-only (`solve_matlab_faithful_hjb`); KFE functions not called |
| Recompute production aggregates C/L/A/B | NOT PERFORMED |
| Enter regional GE / multi-province audit / network training / nominal HANK / calibration / policy / welfare / Results | NOT PERFORMED |
| Create PR / merge / close Issue #44 / successor Issue / self-accept | NOT PERFORMED — DSH stops for fresh ChatGPT review |
| Modify any existing tracked file | NOT PERFORMED — only the exact 10 Issue #44 allowlist files created |
| Commit large raw full-grid arrays | NOT PERFORMED — aligned subsets only; `_decision_inputs.json` stays outside staging |

**Scientific-input retry policy (Issue #44 §5):** the only re-run was a
post-processing observable-definition correction (upwind raw `R_hat`/`Q_hat`/
slope) executed with **identical** scientific inputs; the solver-level outputs
(values, gradients, controls, iteration counts, statistics) are identical
between the two executions and exactly reproduce the accepted DLH-5J solutions.
No hidden retry, no parameter/tolerance tuning, no clipping, no price change, no
interpolation or initialization change occurred.

**Bounded Rev 2 (per fresh review `5509806834`):** this revision changed
**only the interpretation/decision documents** within the same 10 Issue #44
allowlist files (terminal B → C; falsification directions B/C/D/E re-scored
NOT SATISFIED; trend/language corrections). **No new run was performed and no
scientific input changed**; the CSVs, config, runner, and `_decision_inputs.json`
are unchanged from Rev 1. No numerical authority was expanded (no b180/b200, no
b_lo/db/a-resolution change, no adaptive extent, no root seeking, no stationary
KFE, no R/W/domain/endpoint choice, no GE/aggregates/network training/Results).
A larger-domain experiment would require a new Owner decision and successor
authority; DSH did not create such an Issue.

**Completion:** explicit-stage only the exact Issue #44 allowlist (10 paths),
commit, push the dedicated branch
`dsh/issue-44-dlh-5r-hjb-tail-falsification-2026-09-02`, and **STOP for fresh
ChatGPT review**.
