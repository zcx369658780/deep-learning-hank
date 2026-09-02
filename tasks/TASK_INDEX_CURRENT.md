# Deep Learning + HANK Task Index

Status: `ACTIVE_BUILDER_ISSUE__DLH_5N_HIGH_WEALTH_TOTAL_DRIFT_ASYMPTOTICS_AND_DOMAIN_VIABILITY`

Last synchronized: 2026-09-02

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

Current Issue:

**Issue #40 — OPEN**

Title:

`DLH-5N: Analyze high-wealth total-drift asymptotics and domain viability`

Task type:

`SCIENTIFIC_THEORY_ANALYSIS__HIGH_WEALTH_TOTAL_DRIFT_ASYMPTOTICS_AND_DOMAIN_VIABILITY`

Dedicated branch:

`dsh/issue-40-dlh-5n-high-wealth-total-drift-asymptotics-2026-09-02`

Issue #40 becomes the sole DSH Builder authority only after the authoritative activation comment is present and the CURRENT Startup Snapshot is synchronized to the same Issue. If Issue #40 is not open, activation is absent, or Issue / Task Index / Startup identity differs, DSH must fail closed.

## Latest accepted task — Issue #39 / DLH-5M

Accepted candidate:

`80cdb7ab2c14bcb7606fc66a0737c28bd3fbb4bb`

Integrated to `main` by acceptance merge commit:

`69bde2115cdf038e40640ec41d23e0b620167539`

Accepted reviewer verdict:

`DLH_5M_REVISED_CANDIDATE_ACCEPTED__CORE_KKT_AND_W_ACTIVITY_BLOCKERS_RESOLVED__RECOMMENDATION_U_SUPPORTED__OWNER_SCIENTIFIC_DECISION_REQUIRED`

Owner scientific decision:

`ACCEPT_RECOMMENDATION_U__DO_NOT_FREEZE_R_OR_W_YET`

Accepted interpretation:

- Design R is not frozen;
- Design W is not frozen;
- no numerical `W_max` is authorized;
- `W=a+b` remains a source-accounting coordinate and a plausible truncation hypothesis, not a production-domain authority;
- maximization KKT convention for upper constraints is `L=H-lambda*g`, effective gradients `V-lambda`;
- at a W face `lambda_W` cancels from the linear transfer term but survives through adjustment cost;
- W-face activity for accepted finite states is conditional on symbolic `W_max` and cannot be inferred without choosing it;
- a finite rectangular state constraint may be a numerical closure rather than an economic cap, but no truncation-vanishing argument is accepted;
- stationary KFE remains NOT AUTHORIZED.

## Issue #40 scientific scope

DLH-5N is a **theory/documentation gate only**.

It asks whether, under the currently accepted household equations and with the current finite illiquid support `0<=a<=10` and accepted taper held fixed, the model itself implies total-wealth mean reversion as `b->+infinity` / `W=a+b->+infinity`, without imposing an upper `b` constraint or choosing `W_max`.

The Builder must:

1. audit exact source asymptotic objects and frozen D0 inputs;
2. decompose the asymptotic order of every term in `mu_W`;
3. determine which control/value-derivative growth rates are provable vs conditional vs unidentified;
4. build a theorem / conditional theorem / counterexample matrix;
5. use DLH-5L finite-state evidence only as a read-only consistency check;
6. state narrow implications for unresolved R/W domain viability;
7. use exactly one Issue #40 terminal.

The task must explicitly distinguish a fixed-`a` liquid-tail result from a full two-asset infinite-domain theorem.

## Exact Builder allowlist

Builder may create only:

1. `docs/theory/DLH_5N_HIGH_WEALTH_TOTAL_DRIFT_ASYMPTOTICS_AND_DOMAIN_VIABILITY.md`
2. `reports/dlh_5n_high_wealth_total_drift_asymptotics_2026_09_02/` with exactly:
   - `DLH_5N_SOURCE_ASYMPTOTIC_OBJECTS.md`
   - `DLH_5N_ASYMPTOTIC_TERM_ORDER_TABLE.md`
   - `DLH_5N_CONTROL_GROWTH_ASSUMPTION_AUDIT.md`
   - `DLH_5N_THEOREM_AND_COUNTEREXAMPLE_MATRIX.md`
   - `DLH_5N_DOMAIN_VIABILITY_IMPLICATIONS.md`
   - `DLH_5N_SCIENTIFIC_TERMINAL.md`
   - `DLH_5N_EXECUTION_REPORT.md`
   - `DLH_5N_FORBIDDEN_OPERATION_CHECK.md`

No existing tracked file may be modified by Builder.

## Scientific ceiling

No source/model/domain/taper/FOC/adjustment-cost/economic-price/calibration mutation; no R/W/W1/W2 choice; no numerical `W_max`; no new `b_max` or `a_max`; no grid/HJB/KFE run; no J0–J5 rerun; no stationary density/aggregates; no regional GE or multi-province audit; no neural training; no nominal HANK; no policy/welfare/Results.

No PR / merge / close / successor Issue / self-accept from Builder.

## Current route authority

- Issue #40 full body + authoritative activation comment = exact Builder theory-analysis authority once activation is posted.
- Startup Snapshot: `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
- Roadmap: `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
- Accepted DLH-5M design package is read-only context.
