# DLH_4A_TWO_ASSET_HANK_RECONSTRUCTION_FORENSIC_AUDIT_GATE

Date: 2026-08-21

Repository: zcx369658780/deep-learning-hank

## Objective

Audit the current DLH-4A two-asset HANK reconstruction handoff before any further implementation.

This is a scientific forensic audit task, not a repair task.

The purpose is to determine whether the current Python reconstruction should be:

- fully redesigned from equations;
- critically inherited and stabilized;
- partially retained with solver corrections;
- or rejected for scientific identity mismatch.

## Local Evidence Location

Audit source directory:

C:\Users\zcxve\Downloads\DLH-4A-handoff

Relevant paths:

- tests/
- src/deep_learning_hank/two_asset/
- reports/dlh_4a_two_asset_hank_2026_08_20/

## Required Reading

Read:

1. DLH-4A handoff report.
2. Python tests.
3. MATLAB decomposition files under two_asset.
4. All reports under dlh_4a_two_asset_hank_2026_08_20.

## Audit Questions

Determine:

1. Whether the Python implementation preserves the economic object:

(a,b,z)

with:

- illiquid asset a;
- liquid asset b;
- productivity z.

2. Whether HJB implementation matches the intended economics:

- controls c/l/d;
- adjustment cost chi(d,a);
- forward/backward derivatives;
- policy selection;
- boundary treatment.

3. Whether generator construction is consistent:

G = G_a + G_b + G_z

and whether the same operator supports HJB and KFE.

4. Whether KFE validity is established:

- G^T g = 0;
- unique stationary distribution;
- mass conservation;
- non-negativity.

5. Whether current failures are:

- implementation bugs;
- numerical instability;
- calibration/parameter-region issues;
- economic object mismatch.

## Required Comparison Framework

Explicitly distinguish:

- structural parity;
- algorithmic parity;
- numerical parity.

Do not assume MATLAB similarity from file names or module names.

## Forbidden Operations

Do not:

- rewrite code;
- change solver;
- change calibration;
- run full model experiments;
- claim model validation;
- create Results claims.

## Output Report

Create an audit report containing:

- files inspected;
- architecture assessment;
- retained components;
- rejected components;
- scientific blockers;
- numerical blockers;
- recommended route:
  A. full derivation;
  B. critical inheritance;
  C. hybrid reconstruction.

## Terminal Classification

Use one:

- DLH_4A_AUDIT_COMPLETE_READY_FOR_SCIENTIFIC_DECISION
- DLH_4A_AUDIT_BLOCKED_MISSING_EVIDENCE
- DLH_4A_AUDIT_SCOPE_FAILURE
