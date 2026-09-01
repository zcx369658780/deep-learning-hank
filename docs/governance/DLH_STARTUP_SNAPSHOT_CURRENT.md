# Deep Learning + HANK Startup Snapshot — CURRENT

Date: 2026-09-02

Repository: `zcx369658780/deep-learning-hank`

Local Owner-designated workspace: `D:\deep-learning-hank`

## Governance state

- live GitHub `main` = synchronized repository/code/governance authority;
- GitHub Issue = sole DSH Builder authority only after publication + Task Index / Startup synchronization + authoritative activation comment;
- DSH = bounded Builder/executor or bounded design analyst as authorized by the active Issue;
- ChatGPT = independent fresh-GitHub reviewer / scientific-route advisor / task issuer / governance operator;
- Owner = final scientific authority; model-defining domain/boundary-law decisions require Owner approval;
- Builder completion is not acceptance.

Priority:

`Scientific correctness > Experiment reproducibility > Research iteration speed > Git auditability > Documentation completeness`

## Current Builder state

Current published task:

**Issue #39 — DLH-5M: Design-review state-domain geometry and joint HJB/KKT boundary law**

Task type:

`SCIENTIFIC_DESIGN_REVIEW__STATE_DOMAIN_GEOMETRY_AND_JOINT_KKT`

Dedicated branch:

`dsh/issue-39-dlh-5m-domain-kkt-design-review-2026-09-02`

Builder authority becomes active only while Issue #39 remains OPEN, Task Index / Startup identity matches, and the authoritative activation comment is present.

Current master roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`

Historical scientific handoff:

`docs/governance/DLH_HANDOFF_2026_09_01_UPPER_DOMAIN_STATIONARY_TAIL_ROUTE.md`

## Latest accepted gate — Issue #38 / DLH-5L

Accepted candidate:

`3df43fe4da552e19aa7cd3486e06a7e5042d97df`

Integrated to `main` by acceptance merge commit:

`b20e23e28d2f9969df06cb725b3ca23a6fecc2fe`

Accepted reviewer verdict:

`DLH_5L_ISSUE_38_IMPLEMENTATION_ACCEPTED__TOTAL_ASSET_DRIFT_INWARD_ON_PREFROZEN_HIGH_WEALTH_STATE_SET__RECTANGULAR_B_VIOLATION_REINTERPRETED_AS_COMPONENTWISE_REALLOCATION__CROSS_A_TOTAL_DRIFT_SENSITIVITY_REMAINS__DOMAIN_KKT_DESIGN_REVIEW_REQUIRED`

Acceptance level:

`L3_COMMIT_VERIFIED__SCIENTIFIC_ANALYTICAL_DIAGNOSTIC_ACCEPTED`

Controlling accepted interpretation:

- J0–J5 reproduce accepted HJB/boundary evidence exactly; deterministic repeat has max numeric diff 0;
- the inspected state set is the pre-frozen 105-state union of accepted DLH-5K localization and cross-a evidence;
- all 44 material positive liquid-drift states are `B_OUTWARD__TOTAL_INWARD`; no inspected state has positive `mu_W`;
- all 17 accepted top-layer upper-b offenders violate rectangular `mu_b<=0` while satisfying `mu_a<=0` and `mu_W<=0`;
- `mu_W=mu_a+mu_b` and the transfer-cancelled budget identity hold to machine precision; linear transfer cancels one-for-one while adjustment cost remains;
- this establishes inward source-accounting total-asset drift only on the pre-frozen finite state set, not an infinite-domain theorem, stationary-tail result, or production-domain choice;
- cross-a total-drift differences shrink substantially in absolute magnitude but remain above the existing 1e-2 diagnostic threshold on 16/24 aligned pairs;
- no source/domain redesign or stationary re-entry is accepted.

Non-blocking documentation note: `DLH_5L_FORBIDDEN_OPERATION_CHECK.md` contains a stale DLH-5K stationary marker; it is a labeling typo and carries no authority.

## Controlling HJB/KFE rule

```text
HJB boundary policy <=> KFE boundary transition law
```

Issue #27 remains the stationary-KFE contract. Stationary validation cannot begin until a scientifically accepted domain/boundary controlled process is implemented and numerically validated.

## DLH-5M scientific rationale

Accepted evidence now separates two facts:

1. under the current rectangular computational truncation, some high-wealth states violate componentwise upper-b inwardness;
2. on the same pre-frozen states, source-accounting total drift `mu_W=mu_a+mu_b` is inward.

This does not justify changing the domain automatically. It requires a model-design review of the state-constraint geometry and HJB/KKT law.

DLH-5M must distinguish economic constraints from computational truncations and compare:

### Design R — rectangular componentwise constraints

```text
upper-a: mu_a <= 0
upper-b: mu_b <= 0
joint upper corner: mu_a <= 0 AND mu_b <= 0
```

The HJB boundary problem must be formulated as optimization over controls admissible to the active tangent cone, with corresponding KKT conditions, not clipping or ad hoc branch forcing.

### Design W — hybrid joint-wealth truncation

```text
D_W = {a>=0, b>=b_min, a<=a_max, a+b<=W_max}
W face: mu_W<=0
upper-a face: mu_a<=0
intersection: mu_a<=0 AND mu_W<=0
```

This is a candidate design only. `W=a+b` is accepted as a source-accounting coordinate, not yet as the production truncation variable. No numerical `W_max` may be chosen in DLH-5M.

DLH-5M must also compare masked `(a,b)` versus transformed `(a,W)` representations, reject geometry-inconsistent shortcuts, map accepted DLH-5K/5L evidence, and provide an explicit Owner decision packet.

## Required Recommendation vocabulary

Use exactly one:

- `DLH_5M_RECTANGULAR_COMPONENTWISE_STATE_CONSTRAINT_KKT_RECOMMENDED__OWNER_SCIENTIFIC_DECISION_REQUIRED`
- `DLH_5M_HYBRID_JOINT_WEALTH_DOMAIN_AND_JOINT_KKT_RECOMMENDED__OWNER_SCIENTIFIC_DECISION_REQUIRED`
- `DLH_5M_DOMAIN_GEOMETRY_DESIGN_EVIDENCE_INSUFFICIENT__OWNER_SCIENTIFIC_DECISION_REQUIRED`
- `BLOCKED_DLH_5M_SOURCE_OR_ACCEPTED_EVIDENCE_INCONSISTENCY`

No recommendation freezes the model. Owner decision is mandatory before implementation.

## Exact Builder allowlist

Builder may create only:

1. `docs/design/DLH_5M_STATE_DOMAIN_AND_JOINT_KKT_DESIGN_REVIEW.md`
2. `reports/dlh_5m_state_domain_joint_kkt_design_review_2026_09_02/` with exactly eight frozen evidence files listed in Issue #39.

No existing tracked file may be modified by Builder.

## Scientific ceiling during Issue #39

No existing-file mutation; no HJB/KFE/regional source mutation; no taper/FOC/adjustment-cost/economic-price change; no production-domain choice or implementation; no `W_max`; no new or rerun grids; no boundary-KKT implementation; no clipping; no stationary KFE/density/tail/aggregates; no D1-D3, regional GE, multi-province audit, network training, nominal HANK, calibration, policy/welfare or Results.

## DSH startup sequence

1. `Set-Location D:\deep-learning-hank`;
2. verify repository / remote / worktree / staging;
3. `git fetch origin` and record fresh `origin/main`;
4. read all CURRENT project rules;
5. read Task Index, this Startup Snapshot, current Roadmap and historical Handoff;
6. read Issue #39 full body and latest comments, including activation;
7. read accepted Issue #38 review/evidence and controlling Issue #27–#37 authority;
8. read accepted household source and DLH-5K/5L evidence read-only;
9. verify Issue / Task Index / Startup identity exactly;
10. create the exact dedicated branch from fresh `origin/main`;
11. create only the Issue #39 allowlist files;
12. do not run any HJB/KFE/grid experiment;
13. explicit-stage only allowlist paths, commit/push, and STOP for fresh ChatGPT review and Owner scientific decision.

Chat text is not Builder authority.
