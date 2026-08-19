# Chapter 5 Model Equation Memo Read-Only Plan

Date: 2026-06-22

## Provenance

Historical Codex report recovered from `zcx369658780/Zotero-Analytical-Workflow-Skills`.
Commit: `b63d152ca2e6185c6c444b3eb336860928eaa349`.
Original path: `docs/dissertation_submission_reports/2026_06_22_ch5_model_equation_memo_readonly_plan/CH5_MODEL_EQUATION_MEMO_READONLY_PLAN_REPORT_2026_06_22.md`.

## Verdict

`CH5_MODEL_EQUATION_MEMO_READONLY_PLAN_PASS_COMMITTED_TO_GITHUB_READY_FOR_LIMITED_EQUATION_MEMO_GATE`

This package is a read-only model-equation memo plan. It inspects the four user-named Matlab files only to map file roles and identify equation/algorithm blocks for a later memo. It does not translate the model into a final paper model section, does not execute Matlab, and does not create model outputs.

## Matlab Files Inspected Read-Only

- `C:\MatlabProgram\2023年12月2日 多省份神经网络HANK\HANK_2ASSETS_HJB.m`
- `C:\MatlabProgram\2023年12月2日 多省份神经网络HANK\HANK_firm.m`
- `C:\MatlabProgram\2023年12月2日 多省份神经网络HANK\HANK_mp_1eq.m`
- `C:\MatlabProgram\2023年12月2日 多省份神经网络HANK\HANK_mp_1turn.m`

The files were read as text only. No Matlab process was started and no `.m` file was run.

## File-Role Summary

- `HANK_2ASSETS_HJB.m` is the household block. It constructs grids for liquid assets `b`, illiquid/productive assets `ah`, and idiosyncratic state `z`; solves a continuous-time HJB using forward/backward finite differences; constructs a transition generator; solves for the stationary distribution using the transpose generator; and stores aggregates such as consumption, labor, bonds, assets, borrowing measures, utility, marginal utility, and inequality statistics.
- `HANK_firm.m` is the province-level firm/static production and pricing block. It computes Cobb-Douglas output, an NKPC-style marginal-cost object, wages, capital rental return, investment, price adjustment cost, profits, taxes, dividends, and the bounded asset return/wage passed back to households.
- `HANK_mp_1turn.m` is a one-round multi-province update. It builds a cross-province labor-disutility matrix, calls the household solver for each province, updates labor allocation through `Lt_seperate`, updates cross-province capital supply/returns through `inter_prv_ratio`, calls the firm block, updates household wages, collects GDP, and updates common nominal/bond-rate objects.
- `HANK_mp_1eq.m` is the outer multi-province convergence controller. It repeatedly calls `HANK_mp_1turn`, checks capital-labor ratio gaps, output gaps, household HJB convergence, and boundary values for `ra` and `wjt`, then stops or adjusts selected steady-state objects.

## Equation / Algorithm Extraction Summary

A future limited model-equation memo can safely extract:

- Household HJB and utility/FOC structure.
- Two-asset state space with liquid asset `b` and illiquid/productive asset `ah`.
- Idiosyncratic state transition through `la_mat` / `Bswitch`.
- Consumption, labor, saving, and illiquid-asset adjustment policies.
- Stationary distribution / Kolmogorov-forward style equation from `A' g = 0` with normalization.
- Firm production, marginal cost/NKPC-style pricing, wage, return, profit, tax, and dividend objects.
- Province-level labor allocation and cross-province capital-return updating.
- Outer convergence criteria for multi-province equilibrium.

The memo should not yet claim:

- a full housing/hukou/endogenous migration Spatial HANK;
- a completed sequence-space solution method;
- completed calibration, validated results, or submission readiness;
- a final spatial-weight/distance-matrix equation unless later code/data files are read.

## Method-Source Decision Summary

- `Kaplan et al., Monetary Policy According to HANK` was treated as the user-specified primary method source for the historical Matlab route.
- The household solver clearly uses continuous-time HJB-style finite differences and a stationary distribution / generator-transpose solve.
- Sequence-space / Auclert-type references should not be used as a core algorithm description for the historical Matlab route based on the four inspected files alone.

## New-project disposition

This report is **historical reference evidence only**. It does not define the new Deep Learning + HANK model, does not authorize Matlab execution, and does not make old numerical outputs authoritative.
