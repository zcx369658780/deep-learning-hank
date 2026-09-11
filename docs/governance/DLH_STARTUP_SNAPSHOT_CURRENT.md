# Deep Learning + HANK Startup Snapshot — CURRENT

Date: 2026-09-11

Repository: `zcx369658780/deep-learning-hank`

Local Owner-designated workspace: `D:\deep-learning-hank`

## Governance state

- live GitHub `main` = synchronized repository/code/governance authority;
- GitHub Issue = sole DSH Builder authority only after publication + CURRENT Task Index / Startup synchronization + authoritative activation comment;
- DSH = bounded Builder/scientific analyst only under an active Issue;
- ChatGPT = independent reviewer / scientific-route advisor / task issuer / governance operator;
- Owner = final scientific authority;
- Builder completion is not acceptance.

Priority:

`Scientific correctness > Experiment reproducibility > Research iteration speed > Git auditability > Documentation completeness`

## Current Builder state

Current published task:

**Issue #52 — DLH-5V-D: Freeze control-dependent W1 wide-stencil rates and conservative same-process generator contract**

Task type:

`SCIENTIFIC_DESIGN__W1_WIDE_STENCIL_CONTROL_DEPENDENT_RATE_AND_CONSERVATIVE_GENERATOR_CONTRACT`

Dedicated branch:

`dsh/issue-52-dlh-5vd-wide-stencil-rate-contract-2026-09-11`

Owner continuation decision:

`APPROVE_DLH_5VD_CONTROL_DEPENDENT_WIDE_STENCIL_RATE_AND_CONSERVATIVE_GENERATOR_GATE`

Builder authority is active only while Issue #52 remains OPEN, CURRENT Task Index / this Snapshot identity matches, and the authoritative activation comment is present.

## Latest accepted gate — Issue #51 / DLH-5V-C

Accepted candidate:

`2134a4b249eb0a79dc20d60ba1fdee830304f261`

Reviewer acceptance:

`5630191586`

Acceptance integration:

`cdbf1906963a9bf06cf117ba63072d2f1542d501`

Accepted verdict:

`DLH_5VC_ACCEPTED__OUTCOME_A_CONFIRMED__W1_WIDE_STENCIL_EXACT_TANGENT_REGULAR_FEASIBILITY_FROZEN__READY_FOR_WIDE_STENCIL_RATE_GATE`

## Controlling household / finite-domain authority

Accepted household source remains immutable/read-only:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Binding law:

```text
HJB boundary policy <=> KFE boundary transition law
```

Stationary KFE remains **NOT AUTHORIZED**.

Accepted finite domain remains:

```text
D_W(W_max) = {0<=a<=a_max, b>=b_min, a+b<=W_max}
```

No numerical production `W_max` is selected.

Restricted-Voronoi state partition, weighted mass/density semantics, discrete-Hamiltonian requirement, and one-`Q` HJB/KFE principle remain accepted.

## Accepted regular wide-stencil route

On recurring regular W-active states with `j>=7`:

```text
w_in = (-10/19,0)
w_T  = (-70/19,+70/19)
wide destination = (j-7,i+10)
```

The wide edge is an explicit **boundary wide-stencil Markov transition**, not a shared-face FV flux. It preserves represented status, `a+b`, period-7 class and top/sub-top offset. The finite lower-a endpoint band `j in {0,...,6}` remains deferred.

Accepted reallocation sector:

```text
T_realloc = {mu_a<=0, mu_b>=0, mu_W=mu_a+mu_b<=0}
cone{w_in,w_T}=T_realloc
```

## Active DLH-5V-D scientific target

For each candidate boundary control `(c,l,d)` considered **inside the discrete Hamiltonian maximization**, compute the continuous drift. When the candidate lies in `T_realloc`, write

```text
mu=(-a-b,+a)
a=mu_b>=0
b=-mu_W>=0
```

and freeze the unique base-grid candidate-control rates

```text
q_T  = 19*mu_b/70
q_in = 19*(-mu_W)/10.
```

Under fixed-aspect symbolic refinement divide both rates by `h`.

Issue #52 must close the exact activation/equality cases, uniqueness, candidate-control `H_h` semantics, no-double-counting rule, conservative diagonal construction, and same selected `Q` handoff to future KFE. It must explicitly identify any other admissible regular W-boundary drift sector that remains outside this contract.

## KFE methodology safeguard transferred from independent Chapter-5 project

The clean/source-free KFE experience is accepted only as a supporting safeguard, not as foreign model authority:

```text
Q = backward controlled generator
forward = Q^T
off-diagonal >= 0
diagonal = -sum of actually represented outgoing rates
Q1=0
same Q for HJB and KFE
stationary downstream object = mass p
pin/normalization fixes scale only and cannot repair leakage
original Q^T p residual must be validated
SCC/closed recurrent classes must be diagnosed before uniqueness claims
```

MATLAB-faithful contaminated-row reproduction logic is not imported. Existing Issue #27 component-pin authority remains unchanged and downstream.

## Context-budget rule

After all CURRENT project rules, current Task Index / this Snapshot / Roadmap, and full Issue #52 + comments, required scientific reading is limited to:

1. `docs/design/DLH_5VC_W1_WIDE_STENCIL_EXACT_TANGENT_REGULAR_FEASIBILITY.md`
2. `reports/dlh_5vc_w1_wide_stencil_tangent_2026_09_11/DLH_5VC_MOMENT_LOCALITY_AND_SAME_PROCESS_AUDIT.md`
3. `reports/dlh_5vc_w1_wide_stencil_tangent_2026_09_11/DLH_5VC_DESTINATION_PHASE_AND_DOMAIN_AUDIT.md`
4. `docs/design/DLH_5U_W1_FACE_ADAPTED_FINITE_VOLUME_SAME_PROCESS_DISCRETIZATION.md` only if the accepted discrete-Hamiltonian / one-Q semantics needs clarification.

Verify the accepted household source blob only. Do not reread broad DLH-5T/5V-A/5V-B history without a concrete contradiction.

## Exact allowlist

Five new files only, exactly as listed in Issue #52. No existing tracked file may be modified by Builder.

## Scientific ceiling

Design only. Do not mutate source/economics; change grid/aspect ratio; implement or numerically assemble the wide-stencil generator; execute HJB/KFE/stationary; redesign endpoint/corner transitions; invent unaccepted regular-sector remedies; select numerical `W_max`; redesign Issue #27 pinning; import contaminated-row KFE production logic; compute aggregates/GE; or enter multi-province/neural/nominal/calibration/policy/welfare/Results.

Current Master Roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`

Chat text is not Builder authority.
