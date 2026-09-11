# Deep Learning + HANK Task Index

Status: `ACTIVE_BUILDER_ISSUE__DLH_5VC_W1_WIDE_STENCIL_EXACT_TANGENT_REGULAR_FEASIBILITY`

Last synchronized: 2026-09-11

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

Current Issue:

**Issue #51 — OPEN**

Title:

`DLH-5V-C: Audit W1 wide-stencil exact-tangent transport on the regular W frontier`

Task type:

`SCIENTIFIC_DESIGN__W1_WIDE_STENCIL_EXACT_TANGENT_REGULAR_FEASIBILITY`

Dedicated branch:

`dsh/issue-51-dlh-5vc-w1-wide-stencil-tangent-2026-09-11`

Owner route decision:

`APPROVE_ROUTE_F_WIDE__W1_NATIVE_EXACT_TANGENT_REGULAR_AUDIT`

Issue #51 is the sole DSH Builder authority only while it remains OPEN, CURRENT Task Index / Startup identity matches, and the authoritative activation comment is present. Chat text alone does not create Builder authority.

## Latest accepted task — Issue #50 / DLH-5V-B

Accepted candidate:

`6bc8612dc10de6d72d27c9c47d1b4d598a70a15d`

Reviewer acceptance:

`5628629099`

Acceptance integration:

`ff0afdf6d3fa0d770654613e42109318d638639d`

Accepted verdict:

`DLH_5VB_ACCEPTED__OUTCOME_C_CONFIRMED__REGULAR_LOCAL_SHARED_FACE_MOMENT_CONE_OBSTRUCTION_PROVEN__OWNER_ROUTE_DECISION_REQUIRED`

Accepted household source remains immutable/read-only:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Binding law:

```text
HJB boundary policy <=> KFE boundary transition law
```

Stationary KFE remains **NOT AUTHORIZED**.

## Accepted obstruction entering DLH-5V-C

The current restricted-Voronoi **local shared-face** geometry fails on recurring top-cell classes:

```text
A^F: K = {7 mu_a + 10 mu_b <= 0}
A^L: K = {mu_a <= 0, 7 mu_a + 10 mu_b <= 0}
B^W: K = R^2
```

Exact sliding `(-u,+u)` violates the top-cell inequality because `3u>0`. This bounded result does not rule out every W1/Route-F discretization.

## Current DLH-5V-C target

Audit a native-coordinate W1 boundary wide-stencil exact tangent based on the primitive lattice solution

```text
10 Delta j + 7 Delta i = 0,
(Delta j,Delta i)=(-7,+10),
Delta x=(-70/19,+70/19).
```

The gate must prove or refute, on recurring regular W-frontier states away from endpoint/joint-boundary regions:

- represented-destination availability;
- period-7 phase/class preservation;
- full `T_realloc` cone closure when combined with local inward `(-1,0)`;
- nonnegative CTMC first-moment feasibility as an analytic certificate only;
- physical locality under fixed-aspect refinement;
- finite-domain path admissibility;
- compatibility with one-`Q` same-process HJB/KFE semantics as an explicitly non-shared-face boundary Markov transition.

Production rate functions, endpoint/corner closure, implementation, numerical `W_max`, stationary KFE, aggregates, GE and neural work remain unauthorized.

## Exact Builder allowlist

1. `docs/design/DLH_5VC_W1_WIDE_STENCIL_EXACT_TANGENT_REGULAR_FEASIBILITY.md`
2. `reports/dlh_5vc_w1_wide_stencil_tangent_2026_09_11/DLH_5VC_AUTHORITY_CAPSULE.md`
3. `reports/dlh_5vc_w1_wide_stencil_tangent_2026_09_11/DLH_5VC_DESTINATION_PHASE_AND_DOMAIN_AUDIT.md`
4. `reports/dlh_5vc_w1_wide_stencil_tangent_2026_09_11/DLH_5VC_MOMENT_LOCALITY_AND_SAME_PROCESS_AUDIT.md`
5. `reports/dlh_5vc_w1_wide_stencil_tangent_2026_09_11/DLH_5VC_TERMINAL_AND_FORBIDDEN_CHECK.md`

No existing tracked file may be modified by Builder.

Current Startup Snapshot:

`docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`

Current Master Roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
