# Deep Learning + HANK Task Index

Status: `ACTIVE_BUILDER_ISSUE__DLH_5O_HJB_VALUE_FUNCTION_LIQUID_TAIL_SCALING`

Last synchronized: 2026-09-02

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

Current Issue:

**Issue #41 — OPEN**

Title:

`DLH-5O: Derive fixed-a liquid-tail HJB value-function asymptotics`

Task type:

`SCIENTIFIC_THEORY_ANALYSIS__HJB_VALUE_FUNCTION_LIQUID_TAIL_SCALING`

Dedicated branch:

`dsh/issue-41-dlh-5o-hjb-value-tail-asymptotics-2026-09-02`

Issue #41 becomes the sole DSH Builder authority only after the authoritative activation comment is present and the CURRENT Startup Snapshot is synchronized to the same Issue. If Issue #41 is not open, activation is absent, or Issue / Task Index / Startup identity differs, DSH must fail closed.

## Latest accepted task — Issue #40 / DLH-5N

Accepted candidate:

`bded30a8b8cb579c3f359a62f5b530d7c34b7526`

Integrated to `main` by acceptance integration commit:

`e23b1ada5f5ab1b11c1291d8141d8286884553d4`

Accepted reviewer verdict:

`DLH_5N_REV2_ACCEPTED__OUTCOME_B_SUPPORTED__FIXED_A_LIQUID_TAIL_SIGN_REMAINS_CONDITIONAL__HJB_VALUE_FUNCTION_TAIL_ASYMPTOTICS_NEXT_GATE_REQUIRED`

Acceptance level:

`L3_COMMIT_VERIFIED__SCIENTIFIC_THEORY_ANALYSIS_ACCEPTED`

Accepted terminal:

`DLH_5N_FIXED_A_LIQUID_TAIL_TOTAL_WEALTH_SIGN_CONDITIONAL__MISSING_CONTROL_ASYMPTOTICS_IDENTIFIED`

Controlling accepted interpretation:

- with current accepted authority and fixed `a in [0,10]`, no unconditional theorem establishes `mu_W<0` for all sufficiently large positive `b`;
- `r_b*b` is the only explicit positive linearly growing term whose order/sign is fixed by source authority; the control-dependent remainder is not asymptotically identified;
- conditional inwardness/outwardness statements require their explicit tail assumptions;
- the formula-level outward family is not HJB-verified and does not establish a model-level counterexample;
- the result is fixed-a liquid-tail only, not a full two-asset infinite-domain theorem;
- reviewer acceptance comment `5503274333` supersedes local over-strong biconditional shorthand in Phase A/C: downstream work may rely only on the sufficient transfer-ratio directions actually used by accepted M2/M3;
- R/W remain unfrozen; no `W_max`; stationary KFE remains NOT AUTHORIZED.

## Issue #41 scientific scope

DLH-5O is a **theory/documentation gate only**.

It must determine whether the accepted MATLAB-faithful HJB authority is sufficient to derive the missing liquid-tail value-function scaling, especially:

```text
V_b(b,a,z)
V_a(b,a,z)/V_b(b,a,z)
V(b,a,z') - V(b,a,z)
```

under the current fixed illiquid support `0<=a<=10`, without numerical tail continuation and without importing an unaccepted textbook boundary/transversality condition.

The central candidate `V_b ~ K(a,z)/b^2` is a hypothesis to be derived, rejected or left conditional — not an accepted premise.

The task must:

1. audit exact HJB authority and distinguish finite-grid numerical semantics from derivable continuous interior identities;
2. compare `p<2`, `p=2`, `p>2` dominant-balance families jointly with transfer, adjustment cost, labor and productivity switching;
3. if authorized, derive the CRRA-2 `p=2` coefficient system including `V_inf`, `K(a,z)` and all same-order terms;
4. test transfer and cross-productivity self-consistency rather than assuming bounded `V_a/V_b` or negligible switching;
5. classify theorem / conditional theorem / HJB-consistent alternative / authority insufficiency;
6. translate the result narrowly back to DLH-5N without choosing a domain.

## Exact Builder allowlist

Builder may create only:

1. `docs/theory/DLH_5O_HJB_VALUE_FUNCTION_LIQUID_TAIL_ASYMPTOTICS.md`
2. `reports/dlh_5o_hjb_value_function_tail_asymptotics_2026_09_02/` with exactly:
   - `DLH_5O_HJB_AUTHORITY_AUDIT.md`
   - `DLH_5O_DOMINANT_BALANCE_FAMILIES.md`
   - `DLH_5O_P2_COEFFICIENT_SYSTEM.md`
   - `DLH_5O_TRANSFER_AND_Z_SWITCH_SELF_CONSISTENCY.md`
   - `DLH_5O_THEOREM_STATUS_MATRIX.md`
   - `DLH_5O_DOMAIN_VIABILITY_IMPLICATIONS.md`
   - `DLH_5O_SCIENTIFIC_TERMINAL.md`
   - `DLH_5O_FORBIDDEN_OPERATION_CHECK.md`

No existing tracked file may be modified by Builder.

## Scientific ceiling

No accepted source/model/domain/taper/FOC/adjustment-cost/economic-price/calibration mutation; no R/W/W1/W2 choice; no `W_max`; no new `b_max`/`a_max`; no HJB/KFE/grid/stationary run; no prior-fixture rerun; no KKT implementation; no regional GE/multi-province audit; no neural training; no nominal HANK; no policy/welfare/Results.

No PR / merge / close / successor Issue / self-accept from Builder.

## Current route authority

- Issue #41 full body + authoritative activation comment = exact Builder theory-analysis authority once activation is posted.
- Startup Snapshot: `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
- Roadmap: `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
- Accepted DLH-5N package and Issue #40 acceptance comments are read-only controlling context.
