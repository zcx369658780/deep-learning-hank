# Deep Learning + HANK Task Index

Status: `ACTIVE_BUILDER_ISSUE__DLH_5M_STATE_DOMAIN_GEOMETRY_AND_JOINT_KKT_DESIGN_REVIEW`

Last synchronized: 2026-09-02

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

Current Issue:

**Issue #39 — OPEN**

Title:

`DLH-5M: Design-review state-domain geometry and joint HJB/KKT boundary law`

Task type:

`SCIENTIFIC_DESIGN_REVIEW__STATE_DOMAIN_GEOMETRY_AND_JOINT_KKT`

Dedicated branch:

`dsh/issue-39-dlh-5m-domain-kkt-design-review-2026-09-02`

Issue #39 becomes the sole DSH Builder authority only after the authoritative activation comment is present and the CURRENT Startup Snapshot is synchronized to the same Issue. If Issue #39 is not open, activation is absent, or Issue / Task Index / Startup identity differs, DSH must fail closed.

## Latest accepted task — Issue #38 / DLH-5L

Accepted candidate:

`3df43fe4da552e19aa7cd3486e06a7e5042d97df`

Integrated to `main` by acceptance merge commit:

`b20e23e28d2f9969df06cb725b3ca23a6fecc2fe`

Accepted reviewer verdict:

`DLH_5L_ISSUE_38_IMPLEMENTATION_ACCEPTED__TOTAL_ASSET_DRIFT_INWARD_ON_PREFROZEN_HIGH_WEALTH_STATE_SET__RECTANGULAR_B_VIOLATION_REINTERPRETED_AS_COMPONENTWISE_REALLOCATION__CROSS_A_TOTAL_DRIFT_SENSITIVITY_REMAINS__DOMAIN_KKT_DESIGN_REVIEW_REQUIRED`

Acceptance level:

`L3_COMMIT_VERIFIED__SCIENTIFIC_ANALYTICAL_DIAGNOSTIC_ACCEPTED`

Accepted interpretation:

- accepted J0–J5 evidence reproduces exactly and the deterministic repeat is exact;
- the pre-frozen DLH-5K/DLH-5L evidence set contains 105 unique states;
- every one of the 44 material positive-`mu_b` states has `mu_W=mu_a+mu_b<=0`;
- all 17 top-layer upper-b offenders violate rectangular `mu_b<=0` while satisfying `mu_a<=0` and `mu_W<=0`;
- the linear transfer control cancels one-for-one in total-asset drift while adjustment cost remains;
- this is finite-state/source-accounting evidence only, not an infinite-domain mean-reversion theorem or stationary-tail proof;
- cross-a absolute total-drift differences are smaller than liquid-drift differences, but `rel_diff_mu_W` still exceeds the pre-registered 1e-2 diagnostic threshold on 16/24 aligned pairs;
- no production-domain replacement, HJB/KFE mutation, taper/FOC/adjustment-cost change, or stationary re-entry is accepted;
- pure larger-b-grid continuation remains CLOSED;
- stationary KFE remains NOT AUTHORIZED under Issue #27.

Reviewer note: the stale DLH-5K stationary marker in the DLH-5L forbidden-operation report is a non-scientific labeling typo only.

## Issue #39 scientific scope

DLH-5M is a **model-design review**, not an implementation task.

It must distinguish structural/economic constraints from computational truncations, and compare two coherent candidate designs:

1. **Design R — rectangular componentwise state constraints** with tangent-cone/KKT conditions on active faces, including `mu_a<=0`, `mu_b<=0`, and both at the upper corner.
2. **Design W — hybrid joint-wealth truncation** `a>=0`, `b>=b_min`, `a<=a_max`, `a+b<=W_max`, with normal-drift condition `mu_W<=0` on the joint-wealth face and joint constraints at active intersections.

The task must also compare W1 masked `(a,b)` and W2 transformed `(a,W)` representations, reject geometry-inconsistent shortcuts, map accepted DLH-5K/5L evidence to both designs, and produce an explicit Owner decision packet.

No Builder recommendation freezes or changes the model. Owner decision is mandatory before any implementation authority exists.

## Exact Builder allowlist

Builder may create only:

1. `docs/design/DLH_5M_STATE_DOMAIN_AND_JOINT_KKT_DESIGN_REVIEW.md`
2. `reports/dlh_5m_state_domain_joint_kkt_design_review_2026_09_02/` with exactly:
   - `DLH_5M_CONSTRAINT_CLASSIFICATION.md`
   - `DLH_5M_GEOMETRY_CANDIDATES.md`
   - `DLH_5M_JOINT_KKT_BOUNDARY_LAWS.md`
   - `DLH_5M_ACCEPTED_EVIDENCE_MAPPING.csv`
   - `DLH_5M_IMPLEMENTATION_IMPACT_MATRIX.csv`
   - `DLH_5M_SCIENTIFIC_RECOMMENDATION.md`
   - `DLH_5M_OWNER_DECISION_PACKET.md`
   - `DLH_5M_FORBIDDEN_OPERATION_CHECK.md`

No existing tracked file may be modified by Builder.

## Scientific ceiling

No source/model/domain mutation; no numerical `W_max`; no new or rerun grid; no HJB/KFE/taper/FOC/adjustment-cost/economic-price mutation; no boundary-KKT implementation; no clipping; no stationary KFE/density/tail/aggregates; no D1-D3, regional GE, multi-province audit, neural training, nominal HANK, calibration, policy/welfare or Results.

No PR / merge / close / successor Issue / self-accept from Builder.

## Current route authority

- Issue #39 full body + authoritative activation comment = exact Builder design-review authority once activation is posted.
- Startup Snapshot: `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
- Roadmap: `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
- Historical handoff remains context only: `docs/governance/DLH_HANDOFF_2026_09_01_UPPER_DOMAIN_STATIONARY_TAIL_ROUTE.md`
