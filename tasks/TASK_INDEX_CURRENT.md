# Deep Learning + HANK Task Index

Status: `ACTIVE_BUILDER_ISSUE__DLH_5T_FINITE_DOMAIN_SAME_PROCESS_BOUNDARY_DESIGN`

Last synchronized: 2026-09-03

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

Current Issue:

**Issue #46 — OPEN**

Title:

`DLH-5T: Freeze finite production-domain geometry and same-process HJB–KFE boundary contract`

Task type:

`SCIENTIFIC_DESIGN__FINITE_PRODUCTION_DOMAIN_AND_SAME_PROCESS_HJB_KFE_BOUNDARY_CONTRACT`

Dedicated branch:

`dsh/issue-46-dlh-5t-finite-domain-same-process-boundary-2026-09-03`

Issue #46 becomes the sole DSH Builder authority only while it remains OPEN, CURRENT Task Index / Startup identity matches, and the authoritative activation comment is present. Chat text alone does not create Builder authority.

## Latest accepted task — Issue #45 / DLH-5S

Accepted candidate:

`160781a89c6e22b5f17b4259500893140fcb9c01`

Reviewer acceptance comment:

`5519142363`

Acceptance integration commit:

`75bedf6e3bb97d024dc8af3afa30f7398f205846`

Accepted verdict:

`DLH_5S_REV3_ACCEPTED__OUTCOME_B_CONFIRMED__SCALED_TAIL_STRUCTURE_ACCEPTED__P2_REALIZATION_REMAINS_OPEN`

Accepted terminal:

`DLH_5S_P2_REALIZATION_NOT_CLOSED__SCALED_TAIL_TIGHTNESS_OR_BRANCH_SELECTION_REMAINS_UNPROVED__OWNER_ROUTE_DECISION_REQUIRED`

## Owner route decision after DLH-5S

Owner selected Route D:

`APPROVE_ROUTE_D_FINITE_PRODUCTION_DOMAIN_AND_JOINT_HJB_KFE_BOUNDARY_DESIGN`

Scientific meaning:

- preserve the unresolved infinite-domain p=2 caveat;
- move to an explicit finite numerical production-domain design;
- prefer hybrid total-wealth truncation `a+b<=W_max` over the old rectangular upper-b cap;
- use native `(a,b)` masked W1 representation as the primary design candidate;
- freeze HJB boundary KKT and KFE transition law as one controlled process;
- preserve MATLAB-style contamination as a downstream numerical normalization device, not a boundary repair;
- do not select a numerical `W_max` or execute HJB/KFE in this design gate.

## Current DLH-5T target

Primary candidate domain:

```text
D_W(W_max) = {0<=a<=a_max, b>=b_min, a+b<=W_max}
```

Primary representation candidate:

`W1 = native (a,b) tensor coordinates + mask a+b<=W_max`.

Boundary tangent conditions to audit/freeze:

```text
a=0:          mu_a >= 0
b=b_min:      mu_b >= 0
a=a_max:      mu_a <= 0
a+b=W_max:    mu_W=mu_a+mu_b <= 0
```

Central same-process law:

```text
controlled process selected by boundary HJB
        ==
controlled process represented by KFE generator
```

Stationary KFE remains NOT AUTHORIZED in Issue #46.

## Exact Builder allowlist

Builder may create only:

1. `docs/design/DLH_5T_FINITE_PRODUCTION_DOMAIN_AND_SAME_PROCESS_BOUNDARY_CONTRACT.md`
2. `reports/dlh_5t_finite_production_domain_same_process_boundary_2026_09_03/DLH_5T_AUTHORITY_AND_EVIDENCE_FREEZE.md`
3. `reports/dlh_5t_finite_production_domain_same_process_boundary_2026_09_03/DLH_5T_W_DOMAIN_AND_W1_REPRESENTATION.md`
4. `reports/dlh_5t_finite_production_domain_same_process_boundary_2026_09_03/DLH_5T_HJB_KKT_BOUNDARY_LAWS.md`
5. `reports/dlh_5t_finite_production_domain_same_process_boundary_2026_09_03/DLH_5T_SAME_PROCESS_KFE_GENERATOR_CONTRACT.md`
6. `reports/dlh_5t_finite_production_domain_same_process_boundary_2026_09_03/DLH_5T_WMAX_ADEQUACY_PROTOCOL.md`
7. `reports/dlh_5t_finite_production_domain_same_process_boundary_2026_09_03/DLH_5T_IMPLEMENTATION_READINESS_AND_TERMINAL.md`
8. `reports/dlh_5t_finite_production_domain_same_process_boundary_2026_09_03/DLH_5T_FORBIDDEN_OPERATION_CHECK.md`

No existing tracked file may be modified by Builder.

## Scientific ceiling

Issue #46 is design-only. No household-source mutation; no HJB/KFE/grid execution; no numerical `W_max`; no b160 reopening; no W1 implementation; no stationary density/aggregates; no two-region GE; no multi-province execution; no neural training; no nominal HANK/calibration/policy/welfare/Results; no PR/merge/close/successor/self-accept.

Current Startup Snapshot:

`docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`

Current Master Roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
