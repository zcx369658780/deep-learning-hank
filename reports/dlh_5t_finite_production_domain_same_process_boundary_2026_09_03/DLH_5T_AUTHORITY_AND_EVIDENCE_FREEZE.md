# DLH-5T — Authority and Evidence Freeze (Issue #46)

**Task type:** `SCIENTIFIC_DESIGN__FINITE_PRODUCTION_DOMAIN_AND_SAME_PROCESS_HJB_KFE_BOUNDARY_CONTRACT`
**Date:** 2026-09-03
**Dedicated branch:** `dsh/issue-46-dlh-5t-finite-domain-same-process-boundary-2026-09-03`
**Fresh `origin/main` baseline:** `01865f2a6d6099f47031f5f3a79653dcbdbf2374`

This document freezes the authority, identity and read-only evidence base for the
DLH-5T design gate. It is design/provenance only: no source mutation, no HJB/KFE/grid
execution, no `W_max` selection.

---

## 1. Issue identity (verified against live GitHub)

| Field | Value |
|---|---|
| Issue | #46 — **OPEN** |
| Title | `DLH-5T: Freeze finite production-domain geometry and same-process HJB–KFE boundary contract` |
| Task type | `SCIENTIFIC_DESIGN__FINITE_PRODUCTION_DOMAIN_AND_SAME_PROCESS_HJB_KFE_BOUNDARY_CONTRACT` |
| Created | 2026-09-03T02:31:43Z |
| Authoritative activation comment | `5519463570` (2026-09-03T02:34:48Z) |
| Owner route decision | `APPROVE_ROUTE_D_FINITE_PRODUCTION_DOMAIN_AND_JOINT_HJB_KFE_BOUNDARY_DESIGN` |
| Dedicated branch | `dsh/issue-46-dlh-5t-finite-domain-same-process-boundary-2026-09-03` |
| Live main at Issue publication | `37aeabb805e0c5b490ba47638c0f4d3a622c2199` |
| Fresh live main at this gate | `01865f2a6d6099f47031f5f3a79653dcbdbf2374` |

Three-way identity agreement verified: Issue #46 / `tasks/TASK_INDEX_CURRENT.md`
(`ACTIVE_BUILDER_ISSUE__DLH_5T_FINITE_DOMAIN_SAME_PROCESS_BOUNDARY_DESIGN`) /
`docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md` all name the same Issue, task type,
dedicated branch and Owner route decision. Master Roadmap V0.22 status:
`CURRENT OWNER-APPROVED ROUTE D — DLH-5T FINITE PRODUCTION-DOMAIN / SAME-PROCESS BOUNDARY DESIGN ACTIVE`.

## 2. Fresh baseline verification

Performed at startup (2026-09-03):

- `git fetch origin --prune` → fresh `origin/main` = `01865f2a6d6099f47031f5f3a79653dcbdbf2374`
  (activation commits present: `1dfde9b` Task Index, `a034876` Startup Snapshot,
  `01865f2` Roadmap V0.22).
- Dedicated branch created from fresh `origin/main`; HEAD = `01865f2a6d6099f47031f5f3a79653dcbdbf2374`;
  upstream = `origin/main`; tracked tree clean (only untracked session artifacts).
- Worktree/staging pre-mutation state: no staged paths, no tracked modifications.

## 3. Accepted upstream authority chain (read-only)

| Gate | Issue | Status | Accepted object |
|---|---|---|---|
| DLH-5S (latest accepted) | #45 | CLOSED completed | candidate `160781a89c6e22b5f17b4259500893140fcb9c01`; reviewer acceptance `5519142363`; integration `75bedf6e3bb97d024dc8af3afa30f7398f205846`; terminal `DLH_5S_P2_REALIZATION_NOT_CLOSED__SCALED_TAIL_TIGHTNESS_OR_BRANCH_SELECTION_REMAINS_UNPROVED__OWNER_ROUTE_DECISION_REQUIRED` |
| DLH-5R | #44 | CLOSED completed | candidate `6b79b7b1ff388174b5460a32de547a25ecb8a097`; acceptance `5510368753`; integration `96f0adb855233da06e96b71c6d8b6fe6aa540fc7` |
| DLH-5M (domain/KKT design review) | #39 | CLOSED completed | terminal `DLH_5M_DOMAIN_GEOMETRY_DESIGN_EVIDENCE_INSUFFICIENT__OWNER_SCIENTIFIC_DECISION_REQUIRED`; Owner decision packet produced |
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

Verified identical at `HEAD`, `origin/main` and in the working tree (re-verified at
this gate). The source is **not modified** by DLH-5T.

Accepted accounting (implemented source) frozen for the design:

```text
mu_a = r_a_eff(a)*a + d
mu_b = r_b*b + labor_income - d - adjustment_cost(d,a) - (consumption - transfer_income)
mu_W = mu_a + mu_b
     = r_a_eff(a)*a + r_b*b + labor_income - adjustment_cost(d,a) - (consumption - transfer_income)
adjustment_cost(d,a) = chi_0*|d| + 0.5*chi_1*d^2/max(a,a_bar)      (accepted source)
r_a_eff(a) = r_a*(1 - 0.1*(a/a_max)^9)                              (accepted a_max-normalized taper)
labor_income = sum_k wages[k]*(1 - tau - migration_costs[k])*z*labor[k]   (single-province: (1-tau)*wbar*z*l)
effective_r_b = r_b + (borrowing_rate_gap if b < 0 else 0)          (accepted source)
consumption FOC: c = V_b^(-1/gamma_c)
labor FOC:       l = (V_b*net_wage/labor_weight)^(1/phi)
transfer FOC (interior, nondifferentiable kink): q = V_a/V_b - 1;
   d = max(a,a_bar)*(min(q+chi_0,0) + max(q-chi_0,0))/chi_1
```

Frozen anchors: `rho=0.02, r_b` (liquid rate; borrowing-rate-gap above b<0),
`r_a=0.03, gamma_c=2, phi=5, chi_0=0.1, chi_1=2.0, a_bar=1e-6, a_max=10, b_min=-2.0,
db=7/19, da=10/19, z in {0.8,1.3}`, accepted z-switch
`la_mat = ones(Nz,Nz)*(1/3/(Nz-1)) + eye(Nz,Nz)*(-1/3-1/3/(Nz-1))` (rows sum 0).

## 5. Read-only evidence inventory (all paths read at this gate)

- `docs/design/DLH_5M_STATE_DOMAIN_AND_JOINT_KKT_DESIGN_REVIEW.md`
- `reports/dlh_5m_state_domain_joint_kkt_design_review_2026_09_02/DLH_5M_JOINT_KKT_BOUNDARY_LAWS.md`
- `reports/dlh_5m_state_domain_joint_kkt_design_review_2026_09_02/DLH_5M_GEOMETRY_CANDIDATES.md`
- `reports/dlh_5m_state_domain_joint_kkt_design_review_2026_09_02/DLH_5M_CONSTRAINT_CLASSIFICATION.md`
- `reports/dlh_5m_state_domain_joint_kkt_design_review_2026_09_02/DLH_5M_OWNER_DECISION_PACKET.md`
- `docs/specifications/DLH_5D_CONSERVATIVE_STATIONARY_KFE_BOUNDARY_AND_CONTAMINATION_CONTRACT_2026_09_01.md`
- `docs/audits/DLH_5D_MATLAB_KFE_CONTAMINATION_AND_BOUNDARY_PROVENANCE_AUDIT_2026_09_01.md`
- `reports/dlh_5e_conservative_stationary_kfe_validation_r1_2026_09_01/DLH_5E_EXECUTION_REPORT.md`
- `project_rules/PROJECT_RULE_INDEX_CURRENT.md` and all rules referenced by it
- `tasks/TASK_INDEX_CURRENT.md`, `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`,
  `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md` (Roadmap V0.22)
- `src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py` (read-only)
- Full Issue #46 body and all comments (activation `5519463570`)

Key accepted facts re-entered for the design (all read-only, no new evidence):

1. DLH-5E D0: max requested outward boundary rate `3.537e-01` (upper-b), `2.641e-01`
   (upper-a) on the accepted rectangular fixture — the truncation-response blocker
   that Route D must resolve by a constrained boundary process, not by clipping.
2. DLH-5M: every inspected state (105/105) satisfies `mu_W = mu_a + mu_b <= 0`;
   all 17 top-layer upper-b offenders satisfy `mu_a <= 0` and `mu_W <= 0`; the
   linear transfer `d` cancels one-for-one from `mu_W`; `lambda_W` cancels from the
   linear transfer FOC and survives through the adjustment-cost term.
3. DLH-5M geometry-consistency test: the shortcut "rectangle + replace `mu_b<=0` by
   `mu_W<=0` at the corner" is geometry-inconsistent (`C_rect ⊊ C_shortcut`) and is
   **rejected**; the Owner-selected Route D freezes the genuine `D_W` geometry.
4. DLH-5D contract: conservative generator, `diagonal = -sum(actually admitted
   off-diagonal rates)`, no outward destination omitted with a retained diagonal
   rate, `BOUNDARY_POLICY_VIOLATION` fail-closed semantics, contamination as a
   downstream normalization device (validated by ORIGINAL `Q^T g` residual).

## 6. Binding DLH-5T rules (Issue #46 §13, verbatim scope)

Design-only. No source mutation; no HJB/KFE/grid/stationary-density execution; no
numerical `W_max`; no b160 reopen / b180 / b200; no `a_max`/`b_min`/spacing/taper/
utility/FOC/transfer/labor/price change; no W1-mask/slanted-stencil/KKT-control/
conservative-generator implementation; no contamination sensitivity; no `C,L,A,B`;
no two-region rebuild; no regional GE / multi-province / neural / nominal /
calibration / policy / welfare / Results; no PR / merge / close / successor /
self-accept. Only the eight allowlist paths may be created; no existing tracked file
modified; handoff/`_decision_inputs.json` stay untracked.

## 7. Stop

This report freezes authority only. The design analysis is carried out in the
companion allowlist reports. The Builder stops for fresh ChatGPT review after the
eight-file deliverable is committed and pushed.
