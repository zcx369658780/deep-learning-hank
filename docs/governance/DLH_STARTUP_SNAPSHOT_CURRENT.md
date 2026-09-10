# Deep Learning + HANK Startup Snapshot — CURRENT

Date: 2026-09-10

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

**Issue #49 — DLH-5V-A: Classify regular restricted-Voronoi W-frontier phases and adjacency**

Task type:

`SCIENTIFIC_DESIGN__REGULAR_VORONOI_FRONTIER_PHASE_AND_ADJACENCY_CLASSIFICATION`

Dedicated branch:

`dsh/issue-49-dlh-5va-voronoi-frontier-phase-adjacency-2026-09-10`

Owner split-gate decision:

`APPROVE_DLH_5VA_SPLIT_GATE__REGULAR_FRONTIER_PHASE_ADJACENCY_ONLY`

Builder authority is active only while Issue #49 remains OPEN, Task Index / Startup identity matches, and the authoritative activation comment is present.

## Superseded Issue #48

Issue #48 was CLOSED `not_planned` after repeated Builder response/context exhaustion during startup/reference loading. No candidate commit or remote Builder branch was produced. This is operational supersession only; it carries no scientific verdict.

## Latest accepted gate — Issue #47 / DLH-5U

Accepted Rev-1 candidate:

`81bf9b46f20e6dd96514bb6fad698097c917a948`

Reviewer acceptance:

`5521379228`

Acceptance integration:

`060c2835825f9efff4f89c84646f04cab6a9c8a4`

Accepted verdict:

`DLH_5U_REV1_ACCEPTED__OUTCOME_B_CONFIRMED__ROUTE_F_FRAMEWORK_ACCEPTED__TANGENTIAL_SAME_PROCESS_CONSISTENCY_REMAINS_THE_SINGLE_BOUNDED_OPEN_OBJECT`

Accepted household source remains immutable/read-only:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Binding law:

```text
HJB boundary policy <=> KFE boundary transition law
```

Stationary KFE remains **NOT AUTHORIZED**.

## Accepted Route-F framework entering DLH-5V-A

Finite domain:

```text
D_W(W_max) = {0<=a<=a_max, b>=b_min, a+b<=W_max}
```

Represented native nodes and restricted-Voronoi cells:

```text
S(W_max) = {s=(a_j,b_i): a_j+b_i<=W_max}
C_s = {x in D_W : ||x-s||_2 <= ||x-r||_2 for all represented r in S}
```

`{C_s}` partitions `D_W` a.e. Physical W activity is defined only by the actual cell intersection `F_s^W = partial(C_s) intersect {a+b=W_max}` with positive length.

Accepted discrete-Hamiltonian / one-`Q` / weighted mass-density / MATLAB component-pin semantics remain unchanged and are not the active target of Issue #49.

## Exact DLH-5V-A scientific target

Use exact native grid spacing:

```text
da=10/19, db=7/19, da/db=10/7
```

No numerical production `W_max` is selected. Symbolically classify the recurring **regular nondegenerate** W-frontier phases away from `a=0`, `a=a_max`, and `b=b_min`, then derive the actual restricted-Voronoi shared-face neighbors and displacement vectors for every regular class.

Suggested exact phase coordinates:

```text
kappa = 19*(W_max-b_min)
N = floor(kappa)
theta = kappa-N
10*j + 7*i <= kappa
```

The Builder must derive whether `(N mod 7, theta)` is sufficient; do not assume it.

Explicitly deferred: geometric moment cones, transition rates, source-state face-flux moment audit, exact sliding rate construction, endpoints/corners, sliver agglomeration semantics, implementation, HJB/KFE/stationary execution.

## Context-budget startup rule

After reading all CURRENT project rules, current Task Index / this snapshot / Roadmap, full Issue #49 and comments, scientific history is limited to:

1. `docs/design/DLH_5U_W1_FACE_ADAPTED_FINITE_VOLUME_SAME_PROCESS_DISCRETIZATION.md`
2. `reports/dlh_5u_w1_face_adapted_fv_same_process_2026_09_03/DLH_5U_CONTROL_VOLUME_GEOMETRY_AND_BOUNDARY_LOCATION.md`

Verify household blob identity only; do not reread the full source or superseded Issue #48 unless a direct authority contradiction is found. Do not narrate each startup read; after startup use at most a 10-line authority digest and proceed.

## Exact allowlist

Five files only, exactly as listed in Issue #49. No existing tracked file may be modified by Builder.

## Scientific ceiling

Do not mutate source; run HJB/KFE/stationary; choose numerical `W_max`; modify grid/economics; compute moment cones/rates; analyze endpoint/corner transition closure; agglomerate cells; run contamination sensitivity; compute aggregates/GE; enter multi-province/neural/nominal/calibration/policy/welfare/Results; or PR/merge/close/successor/self-accept.

## DSH startup sequence

1. `Set-Location D:\deep-learning-hank`;
2. verify repository / remote / worktree / staging;
3. `git fetch origin` and record fresh `origin/main`;
4. read all CURRENT project rules without narrating them;
5. read CURRENT Task Index, this Startup Snapshot, Roadmap;
6. read full Issue #49 and ALL comments including activation;
7. read only the two scientific files listed above;
8. verify accepted household blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e` without rereading source;
9. verify Issue / Task Index / Startup identity;
10. create exact dedicated branch from fresh synchronized main;
11. create only five allowlist files;
12. perform bounded symbolic design and STOP for fresh ChatGPT review.

Chat text is not Builder authority.
