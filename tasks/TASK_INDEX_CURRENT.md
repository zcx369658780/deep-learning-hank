# Deep Learning + HANK Task Index

Status: `ACTIVE_BUILDER_ISSUE__DLH_5VD_CONTROL_DEPENDENT_WIDE_STENCIL_RATE_AND_CONSERVATIVE_GENERATOR_CONTRACT`

Last synchronized: 2026-09-11

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

Current Issue:

**Issue #52 — OPEN**

Title:

`DLH-5V-D: Freeze control-dependent W1 wide-stencil rates and conservative same-process generator contract`

Task type:

`SCIENTIFIC_DESIGN__W1_WIDE_STENCIL_CONTROL_DEPENDENT_RATE_AND_CONSERVATIVE_GENERATOR_CONTRACT`

Dedicated branch:

`dsh/issue-52-dlh-5vd-wide-stencil-rate-contract-2026-09-11`

Owner continuation decision:

`APPROVE_DLH_5VD_CONTROL_DEPENDENT_WIDE_STENCIL_RATE_AND_CONSERVATIVE_GENERATOR_GATE`

Issue #52 is the sole DSH Builder authority only while it remains OPEN, CURRENT Task Index / Startup Snapshot identity matches, and the authoritative activation comment is present. Chat text alone does not create Builder authority.

## Latest accepted task — Issue #51 / DLH-5V-C

Accepted candidate:

`2134a4b249eb0a79dc20d60ba1fdee830304f261`

Reviewer acceptance:

`5630191586`

Acceptance integration:

`cdbf1906963a9bf06cf117ba63072d2f1542d501`

Accepted verdict:

`DLH_5VC_ACCEPTED__OUTCOME_A_CONFIRMED__W1_WIDE_STENCIL_EXACT_TANGENT_REGULAR_FEASIBILITY_FROZEN__READY_FOR_WIDE_STENCIL_RATE_GATE`

Accepted household source remains immutable/read-only:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Binding law:

```text
HJB boundary policy <=> KFE boundary transition law
```

Stationary KFE remains **NOT AUTHORIZED**.

## Accepted wide-stencil regular-region authority entering DLH-5V-D

For accepted regular W-active states with `j>=7`:

```text
w_in = (-10/19, 0)
w_T  = (-70/19, +70/19)
(j,i) -> (j-7,i+10)
```

The wide tangent preserves represented status, `a+b`, period-7 class and top/sub-top offset. The endpoint band `j in {0,...,6}` remains deferred.

Accepted reallocation cone:

```text
T_realloc = {mu_a<=0, mu_b>=0, mu_W=mu_a+mu_b<=0}
cone{w_in,w_T} = T_realloc
```

## Current DLH-5V-D target

For every candidate control `(c,l,d)` inside the discrete boundary-HJB maximization and inside `T_realloc`, freeze the unique control-dependent rate map:

```text
q_T  = 19*mu_b/70
q_in = 19*(-mu_W)/10
```

and the corresponding fixed-aspect refinement scaling divided by `h`.

The gate must freeze:

- exact activation and equality cases;
- uniqueness / no tie-breaking in the two-ray sector;
- candidate-control rates inside discrete `H_h` before maximization;
- canonical no-double-counting semantics;
- nonnegative off-diagonals and diagonal = negative sum of actually represented outgoing rates;
- `Q 1 = 0` by construction;
- same selected backward `Q` handed unchanged to future KFE as `Q^T`;
- mass-first downstream semantics `p=Mg`, `p_dot=Q^T p`;
- future SCC/closed-class/original-residual validation requirements.

This Issue freezes **only** the accepted `T_realloc` regular sector. Any other admissible regular W-boundary drift sector must be identified explicitly as unresolved, not silently claimed solved.

## Cross-project KFE methodological safeguards

The Chapter-5 clean/source-free KFE report is used only as supporting methodology consistent with existing project authority:

```text
Q backward; Q^T forward
Q_ij>=0 off diagonal
Q_ii=-sum outgoing
Q1=0
same Q for HJB/KFE
pin/normalization = scale fixing only, never leakage repair
original source-free residual required downstream
```

MATLAB-faithful contaminated-row logic is not production authority here. Issue #27 component-pin authority remains unchanged.

## Exact Builder allowlist

1. `docs/design/DLH_5VD_CONTROL_DEPENDENT_WIDE_STENCIL_RATE_AND_CONSERVATIVE_GENERATOR_CONTRACT.md`
2. `reports/dlh_5vd_wide_stencil_rate_contract_2026_09_11/DLH_5VD_AUTHORITY_CAPSULE.md`
3. `reports/dlh_5vd_wide_stencil_rate_contract_2026_09_11/DLH_5VD_CONTROL_DEPENDENT_RATE_DECOMPOSITION.md`
4. `reports/dlh_5vd_wide_stencil_rate_contract_2026_09_11/DLH_5VD_CONSERVATIVE_GENERATOR_AND_KFE_HANDOFF_CONTRACT.md`
5. `reports/dlh_5vd_wide_stencil_rate_contract_2026_09_11/DLH_5VD_TERMINAL_AND_FORBIDDEN_CHECK.md`

No existing tracked file may be modified by Builder.

## Scientific ceiling

No source/economics mutation, grid/aspect change, code implementation, production generator execution, HJB/KFE/stationary solve, endpoint/corner design, unaccepted regular-sector remedy, numerical `W_max`, Issue #27 pin redesign, aggregates/GE/neural/nominal/calibration/policy/welfare/Results, PR/merge/close/successor/self-accept.

Current Startup Snapshot:

`docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`

Current Master Roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
