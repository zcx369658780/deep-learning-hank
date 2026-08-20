# DLH-3B-R1 — HA Algorithm Parity Audit

Date: 2026-08-20

Status: TASK_SPECIFICATION_CREATED

## Authority

Task type:

`SCIENTIFIC_AUDIT_ONLY`

Roles:

- Builder: DSH / bounded executor
- Reviewer: ChatGPT independent scientific reviewer
- Owner: final scientific-direction authority

This task does not authorize model modification.

---

# 1. Research Question

Determine whether the current Python HA/HANK household kernel is algorithmically consistent with the legacy MATLAB implementation:

`D:\\MatlabProgram\\2023年12月2日 多省份神经网络HANK\\HANK_2ASSETS_HJB.m`

The objective is not to improve the model.

The objective is to determine whether Python is solving the same economic problem with the same numerical semantics.

---

# 2. Scientific Motivation

Before HANK dynamic extension, NK closure, calibration, or regional expansion, the household algorithm must be validated.

The core validation object is:

`HJB + KFE + asset accounting + equilibrium fixed point`

Not RANK-style Euler equation iteration.

---

# 3. Allowed Operations

Allowed:

- Read Python HA/HANK source code.
- Read MATLAB HANK_2ASSETS_HJB.m source.
- Read tests, configs, and reports.
- Produce audit documentation.
- Build comparison tables.
- Identify scientific risks.

---

# 4. Forbidden Operations

Forbidden:

- Modify Python solver.
- Modify MATLAB source.
- Tune parameters.
- Change calibration.
- Change grids.
- Change boundary conditions.
- Add new assets.
- Add NK block.
- Add regional model.
- Run legacy MATLAB execution unless separately authorized.

---

# 5. Required Audit Scope

## 5.1 State Space

Compare:

- asset dimensions;
- productivity states;
- household state ordering;
- regional dimensions if present.

Output a MATLAB vs Python state-space map.

---

## 5.2 Asset Accounting

Audit:

- liquid asset meaning;
- illiquid asset meaning;
- capital/bond interpretation;
- asset accumulation equations;
- market clearing definitions.

Explicitly identify any semantic mismatch.

---

## 5.3 HJB Algorithm

Compare:

- value initialization;
- marginal value calculation;
- FOC implementation;
- consumption policy;
- drift calculation;
- upwind scheme;
- derivative direction;
- boundary treatment;
- convergence logic.

---

## 5.4 Generator / Transition Matrix

Audit whether:

- the same infinitesimal generator is used for HJB and KFE;
- transition matrix orientation is correct;
- mass conservation is preserved.

---

## 5.5 KFE Algorithm

Compare:

- stationary distribution computation;
- normalization;
- non-negativity handling;
- boundary mass behavior;
- convergence criteria.

---

## 5.6 Solver Workflow

Compare the complete loop:

price guess
→ HJB
→ policy functions
→ transition matrix
→ KFE
→ aggregates
→ price update
→ convergence

---

# 6. Required Deliverable

Create audit report containing:

1. MATLAB specification map.
2. Python implementation map.
3. State-space comparison.
4. Asset-accounting comparison.
5. HJB comparison.
6. Generator comparison.
7. KFE comparison.
8. Solver workflow comparison.
9. Confirmed matches.
10. Scientific mismatches.
11. Risk classification.
12. Recommendation for next scientific step.

---

# 7. Completion Evidence

Builder completion report must include:

- terminal classification;
- branch;
- commit SHA;
- changed files;
- files reviewed;
- limitations;
- unresolved scientific questions.

No code modification evidence is expected because this is an audit task.

---

# 8. Stopping Conditions

Stop and report:

`BLOCKED_DLH_3B_R1_SCIENTIFIC_MISMATCH`

if any of the following is found:

- Python solves a different HJB problem;
- asset accounting differs;
- KFE uses inconsistent transition semantics;
- boundary conditions change economic meaning.

Stop and report:

`DLH_3B_R1_AUDIT_COMPLETE`

if the parity review is complete.

---

# 9. Scientific Boundary

This task does not authorize:

- HA calibration;
- HANK steady-state validation;
- NK dynamics;
- monetary policy experiments;
- NSR-HANK regional extension.

Those require future scientific decisions.
