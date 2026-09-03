# DLH-5U — Authority and Evidence Freeze (Issue #47)

**Task type:** `SCIENTIFIC_DESIGN__W1_FACE_ADAPTED_FINITE_VOLUME_SAME_PROCESS_DISCRETIZATION`
**Date:** 2026-09-03
**Dedicated branch:** `dsh/issue-47-dlh-5u-w1-face-adapted-fv-design-2026-09-03`
**Fresh `origin/main` baseline:** `9ba4a530ba5e880d45433cec74d618e9461357b7`

This document freezes the authority, identity and read-only evidence base for the
DLH-5U design gate. It is design/provenance only: no source mutation, no Route-F
implementation, no HJB/KFE/grid execution, no `W_max` selection.

---

## 1. Issue identity (verified against live GitHub)

| Field | Value |
|---|---|
| Issue | #47 — **OPEN** |
| Title | `DLH-5U: Freeze W1 face-adapted finite-volume same-process discretization` |
| Task type | `SCIENTIFIC_DESIGN__W1_FACE_ADAPTED_FINITE_VOLUME_SAME_PROCESS_DISCRETIZATION` |
| Created | 2026-09-03T04:06:40Z |
| Authority marker | `DLH_5U_W1_FACE_ADAPTED_FINITE_VOLUME_SAME_PROCESS_DISCRETIZATION_AUTHORIZED` |
| Authoritative activation comment | `5520198694` (2026-09-03T04:08:28Z) |
| Owner route decision | `APPROVE_ROUTE_F_W1_FACE_ADAPTED_FINITE_VOLUME_OBLIQUE_FLUX_DESIGN` |
| Dedicated branch | `dsh/issue-47-dlh-5u-w1-face-adapted-fv-design-2026-09-03` |
| Live main at Issue publication | `855b8fdcad1e506ce0f23a35875cd23abb3698a0` |
| Fresh live main at this gate | `9ba4a530ba5e880d45433cec74d618e9461357b7` |

Three-way identity agreement verified: Issue #47 / `tasks/TASK_INDEX_CURRENT.md`
(`ACTIVE_BUILDER_ISSUE__DLH_5U_W1_FACE_ADAPTED_FINITE_VOLUME_DESIGN`) /
`docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md` all name the same Issue, task type,
dedicated branch and Owner Route-F decision. Master Roadmap V0.23 status:
`CURRENT OWNER-APPROVED ROUTE F — DLH-5U W1 FACE-ADAPTED FINITE-VOLUME SAME-PROCESS DESIGN ACTIVE`.

## 2. Fresh baseline verification

Performed at startup (2026-09-03):

- `git fetch origin --prune` → fresh `origin/main` = `9ba4a530ba5e880d45433cec74d618e9461357b7`
  (activation commits present: `0212855` Task Index, `cfe0e0b` Startup Snapshot,
  `9ba4a53` Roadmap V0.23).
- Dedicated branch created from fresh `origin/main`; HEAD = `9ba4a53…`; upstream =
  `origin/main`; tracked tree clean (only untracked session artifacts).
- Worktree/staging pre-mutation state: no staged paths, no tracked modifications.

## 3. Accepted upstream authority chain (read-only)

| Gate | Issue | Status | Accepted object |
|---|---|---|---|
| DLH-5U (current) | #47 | **OPEN** | this gate |
| DLH-5T (latest accepted) | #46 | CLOSED completed | candidate `fa9d886ea932c2c9001b86228200a162fb1990cd`; reviewer acceptance `5519690088`; integration `73efb8b00b6b4884fc966f159b3aa8401cd3df41`; verdict `DLH_5T_ACCEPTED__OUTCOME_B_CONFIRMED__W_DOMAIN_AND_CONTINUOUS_SAME_PROCESS_BOUNDARY_CONTRACT_ACCEPTED__W1_TANGENTIAL_DISCRETE_PROCESS_MATCHING_REMAINS_OPEN`; terminal `DLH_5T_W_DOMAIN_SCIENTIFICALLY_SUPPORTED__W1_DISCRETE_PROCESS_MATCHING_REQUIRES_BOUNDED_FOLLOWUP_DESIGN` |
| DLH-5S | #45 | CLOSED completed | candidate `160781a…`; acceptance `5519142363`; integration `75bedf6…` |
| DLH-5M (domain/KKT design review) | #39 | CLOSED completed | Owner decision packet produced |
| DLH-5D (KFE boundary/contamination contract) | #27 | accepted | `docs/specifications/DLH_5D_CONSERVATIVE_STATIONARY_KFE_BOUNDARY_AND_CONTAMINATION_CONTRACT_2026_09_01.md` |
| DLH-5E (conservative-KFE validator / boundary gate) | #28 | accepted (blocked run) | terminal `BLOCKED_DLH_5E_BOUNDARY_POLICY_VIOLATION__OWNER_BOUNDARY_POLICY_DECISION_REQUIRED` |

Binding Issue #27 law preserved:

```text
HJB boundary policy <=> KFE boundary transition law
```

Stationary KFE remains **NOT AUTHORIZED** in this Issue.

## 4. Accepted household source — immutable, read-only

```text
src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py
Git blob:  76ae5b149993a7edeeb8eb337f1b02b3fe33c51e
SHA-256:   1795718C469FC3B427CAB8E3D5957C133BEAD6EACC9EF0A25A3EDB7211D1A024
```

Verified identical at `HEAD`, `origin/main` and in the working tree. Not modified.

Accepted accounting (frozen; not reopened):

```text
mu_a = r_a_eff(a)*a + d
mu_b = r_b*b + labor_income - d - adjustment_cost(d,a) - (consumption - transfer_income)
mu_W = mu_a + mu_b = r_a_eff(a)*a + r_b*b + labor_income - adjustment_cost(d,a)
                     - (consumption - transfer_income)
adjustment_cost(d,a) = chi_0*|d| + 0.5*chi_1*d^2/max(a,a_bar)
r_a_eff(a) = r_a*(1 - 0.1*(a/a_max)^9)
effective_r_b = r_b + (borrowing_rate_gap if b < 0 else 0)
```

Accepted DLH-5T continuous boundary laws (not reopened):

```text
a=0:          mu_a >= 0
b=b_min:      mu_b >= 0
a=a_max:      mu_a <= 0
a+b=W_max:    mu_W <= 0
at intersections: all active constraints jointly
controls selected by the constrained Hamiltonian/KKT; no unconstrained-policy-then-clip
```

Accepted central law:

```text
controlled process selected by boundary HJB
        ==
controlled process represented by KFE generator
```

## 5. Read-only evidence inventory (read at this gate)

- Full Issue #47 body + all comments (activation `5520198694`).
- The accepted DLH-5T package (8 files) on `main`:
  - `docs/design/DLH_5T_FINITE_PRODUCTION_DOMAIN_AND_SAME_PROCESS_BOUNDARY_CONTRACT.md`
  - `reports/dlh_5t_finite_production_domain_same_process_boundary_2026_09_03/…` (all 7 reports)
- `docs/specifications/DLH_5D_CONSERVATIVE_STATIONARY_KFE_BOUNDARY_AND_CONTAMINATION_CONTRACT_2026_09_01.md`
- `docs/audits/DLH_5D_MATLAB_KFE_CONTAMINATION_AND_BOUNDARY_PROVENANCE_AUDIT_2026_09_01.md`
- `reports/dlh_5e_conservative_stationary_kfe_validation_r1_2026_09_01/DLH_5E_EXECUTION_REPORT.md`
- `reports/dlh_5m_state_domain_joint_kkt_design_review_2026_09_02/…` (KKT laws, geometry candidates, constraint classification, owner decision packet)
- `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md` (Roadmap V0.23, §3–§5 Route-F detail)
- `tasks/TASK_INDEX_CURRENT.md`, `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
- `project_rules/PROJECT_RULE_INDEX_CURRENT.md` and all referenced CURRENT rules
- `src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py` (read-only)

Key accepted facts re-entered (no new evidence):

1. DLH-5T Outcome B object: the W1 masked-lattice tangential-drift representation on
   the slanted `W` face (`mu_b > 0, mu_a < 0, mu_W <= 0` admissible at the continuous
   W frontier; the `+b` axial destination may lie outside the W1 mask; pure axial
   node-to-node transitions do not uniquely preserve the local process).
2. Roadmap reviewer clarifications controlling all downstream work: no positive
   W-normal flux does not imply every axial component has an in-mask axial neighbor;
   `a_bar=1e-6` is the adjustment-cost denominator floor, not the state boundary;
   negative-`b` implementation must preserve the accepted effective liquid return /
   borrowing-rate-gap semantics.
3. DLH-5D contract: conservative generator, `diagonal = -sum(actually admitted
   off-diagonal rates)`, no outward destination omitted with a retained diagonal
   rate, `BOUNDARY_POLICY_VIOLATION` fail-closed semantics, contamination as a
   downstream normalization device validated by the ORIGINAL `Q^T g` residual.

## 6. Binding DLH-5U rules (Issue #47 §18, verbatim scope)

Design-only. No source mutation; no Route-F implementation (no control volumes, no
fluxes, no mass matrix, no KKT controls, no generator assembly); no HJB/KFE/
stationary/grid execution; no numerical `W_max`; no b160 reopen / b180 / b200; no
grid/taper/economic-parameter change; no contamination sensitivity; no `C,L,A,B`;
no two-region rebuild; no multi-province / neural / nominal / calibration / policy /
welfare / Results; no PR / merge / close / successor / self-accept. Only the nine
allowlist paths may be created; no existing tracked file modified; handoff /
`_decision_inputs.json` stay untracked. Read-only symbolic/local analytic derivations
are allowed.

## 7. Stop

This report freezes authority only. The design analysis is carried out in the
companion allowlist reports. The Builder stops for fresh ChatGPT review after the
nine-file deliverable is committed and pushed.
