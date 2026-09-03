# Deep Learning + HANK Task Index

Status: `ACTIVE_BUILDER_ISSUE__DLH_5U_W1_FACE_ADAPTED_FINITE_VOLUME_DESIGN`

Last synchronized: 2026-09-03

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

Current Issue:

**Issue #47 — OPEN**

Title:

`DLH-5U: Freeze W1 face-adapted finite-volume same-process discretization`

Task type:

`SCIENTIFIC_DESIGN__W1_FACE_ADAPTED_FINITE_VOLUME_SAME_PROCESS_DISCRETIZATION`

Dedicated branch:

`dsh/issue-47-dlh-5u-w1-face-adapted-fv-design-2026-09-03`

Issue #47 becomes the sole DSH Builder authority only while it remains OPEN, CURRENT Task Index / Startup identity matches, and the authoritative activation comment is present.

Chat text alone does not create Builder authority.

## Latest accepted task — Issue #46 / DLH-5T

Accepted candidate:

`fa9d886ea932c2c9001b86228200a162fb1990cd`

Reviewer acceptance comment:

`5519690088`

Acceptance integration commit:

`73efb8b00b6b4884fc966f159b3aa8401cd3df41`

Acceptance level:

`L3_COMMIT_VERIFIED__SCIENTIFIC_DESIGN_ACCEPTED`

Accepted verdict:

`DLH_5T_ACCEPTED__OUTCOME_B_CONFIRMED__W_DOMAIN_AND_CONTINUOUS_SAME_PROCESS_BOUNDARY_CONTRACT_ACCEPTED__W1_TANGENTIAL_DISCRETE_PROCESS_MATCHING_REMAINS_OPEN`

Accepted terminal:

`DLH_5T_W_DOMAIN_SCIENTIFICALLY_SUPPORTED__W1_DISCRETE_PROCESS_MATCHING_REQUIRES_BOUNDED_FOLLOWUP_DESIGN`

## Owner route decision after DLH-5T

Owner selected:

`APPROVE_ROUTE_F_W1_FACE_ADAPTED_FINITE_VOLUME_OBLIQUE_FLUX_DESIGN`

Scientific meaning:

- keep native `(a,b,z)` household coordinates;
- keep accepted W-domain family `D_W(W_max)={0<=a<=a_max,b>=b_min,a+b<=W_max}`;
- keep borrowing floor `b=b_min` coordinate-aligned;
- place oblique numerical complexity on the artificial W frontier;
- resolve W1 tangential reallocation through a face-adapted finite-volume / oblique-flux discrete-process design;
- preserve exact HJB/KFE same-process authority;
- remain design-only: no implementation, HJB/KFE execution, or numerical `W_max`.

## Current DLH-5U target

DLH-5U must determine whether Route F can be frozen to implementation-ready level.

Required design objects include:

- physical clipped control-volume geometry distinct from staircase mask semantics;
- boundary-control/Hamiltonian location and its refinement consistency;
- monotone conservative face-flux / CTMC transition rates;
- symbolic proof that admissible `mu_b>0, mu_a<0, mu_W<=0` tangential portfolio reallocation is represented without reflection/leakage/asset distortion;
- exact backward `Q V` / forward mass `Q^T p` adjoint semantics;
- explicit probability-mass vs density / nonuniform cut-cell weight contract;
- compatibility with downstream contamination normalization;
- small-cut-cell/sliver handling or a precise future geometric admissibility rule;
- first-order/refinement consistency toward the accepted continuous constrained process.

Stationary KFE remains **NOT AUTHORIZED**.

Accepted household source remains immutable/read-only:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Binding law:

```text
controlled process selected by boundary HJB
        ==
controlled process represented by KFE generator
```

## Exact Builder allowlist

Issue #47 may create only the nine exact paths frozen in the Issue body:

1. `docs/design/DLH_5U_W1_FACE_ADAPTED_FINITE_VOLUME_SAME_PROCESS_DISCRETIZATION.md`
2. `reports/dlh_5u_w1_face_adapted_fv_same_process_2026_09_03/DLH_5U_AUTHORITY_AND_EVIDENCE_FREEZE.md`
3. `reports/dlh_5u_w1_face_adapted_fv_same_process_2026_09_03/DLH_5U_CONTROL_VOLUME_GEOMETRY_AND_BOUNDARY_LOCATION.md`
4. `reports/dlh_5u_w1_face_adapted_fv_same_process_2026_09_03/DLH_5U_BOUNDARY_HAMILTONIAN_AND_FACE_FLUX_CONTRACT.md`
5. `reports/dlh_5u_w1_face_adapted_fv_same_process_2026_09_03/DLH_5U_CTMC_GENERATOR_AND_DISCRETE_ADJOINT.md`
6. `reports/dlh_5u_w1_face_adapted_fv_same_process_2026_09_03/DLH_5U_TANGENTIAL_REALLOCATION_AND_CONSISTENCY.md`
7. `reports/dlh_5u_w1_face_adapted_fv_same_process_2026_09_03/DLH_5U_MASS_DENSITY_CONTAMINATION_COMPATIBILITY.md`
8. `reports/dlh_5u_w1_face_adapted_fv_same_process_2026_09_03/DLH_5U_IMPLEMENTATION_READINESS_AND_TERMINAL.md`
9. `reports/dlh_5u_w1_face_adapted_fv_same_process_2026_09_03/DLH_5U_FORBIDDEN_OPERATION_CHECK.md`

No existing tracked file may be modified by Builder.

## Scientific ceiling

Issue #47 is design-only. Do not:

- mutate accepted household/HJB/KFE/regional source;
- implement the Route-F scheme;
- run HJB/KFE/stationary/grid/domain experiments;
- choose numerical `W_max`;
- reopen b160 or alter grid/taper/economic primitives;
- run contamination sensitivity;
- compute stationary aggregates;
- rebuild two-region GE;
- enter multi-province execution or neural training;
- enter nominal HANK, calibration, policy, welfare or Results;
- PR / merge / Issue close / successor Issue / self-accept from Builder.

Current Startup Snapshot:

`docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`

Current Master Roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
