# Deep Learning + HANK Startup Snapshot — CURRENT

Date: 2026-09-03

Repository: `zcx369658780/deep-learning-hank`

Local Owner-designated workspace: `D:\deep-learning-hank`

## Governance state

- live GitHub `main` = synchronized repository/code/governance authority;
- GitHub Issue = sole DSH Builder authority only after publication + Task Index / Startup synchronization + authoritative activation comment;
- DSH = bounded Builder/executor or scientific analyst only under an active Issue;
- ChatGPT = independent fresh-GitHub reviewer / scientific-route advisor / task issuer / governance operator;
- Owner = final scientific authority;
- Builder completion is not acceptance.

Priority:

`Scientific correctness > Experiment reproducibility > Research iteration speed > Git auditability > Documentation completeness`

## Current Builder state

`NO_ACTIVE_BUILDER_ISSUE__DLH_5U_ACCEPTED__TANGENTIAL_VORONOI_PROCESS_DESIGN_REQUIRED`

There is **no active Builder Issue**. DSH must remain stopped until a successor bounded scientific-design Issue is separately published, Task Index / Startup are synchronized, and an authoritative activation comment is posted.

Current master roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`

## Latest accepted gate — Issue #47 / DLH-5U

Issue #47 is CLOSED completed.

Accepted Rev-1 candidate:

`81bf9b46f20e6dd96514bb6fad698097c917a948`

Reviewer acceptance comment:

`5521379228`

Acceptance integration commit:

`060c2835825f9efff4f89c84646f04cab6a9c8a4`

Acceptance level:

`L3_COMMIT_VERIFIED__SCIENTIFIC_DESIGN_ACCEPTED`

Accepted verdict:

`DLH_5U_REV1_ACCEPTED__OUTCOME_B_CONFIRMED__ROUTE_F_FRAMEWORK_ACCEPTED__TANGENTIAL_SAME_PROCESS_CONSISTENCY_REMAINS_THE_SINGLE_BOUNDED_OPEN_OBJECT`

Accepted terminal:

`DLH_5U_ROUTE_F_SCIENTIFICALLY_VIABLE__ONE_BOUNDED_DISCRETE_GEOMETRY_OR_WEIGHTED_ADJOINT_OBJECT_REMAINS_UNRESOLVED`

## Controlling household / finite-domain / KFE authority

Accepted household source remains immutable/read-only:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Issue #27 remains binding:

```text
HJB boundary policy <=> KFE boundary transition law
```

Stationary KFE remains **NOT AUTHORIZED**.

Accepted finite numerical domain family:

```text
D_W(W_max) = {
  0 <= a <= a_max,
  b >= b_min,
  a+b <= W_max
}
```

No numerical `W_max` is frozen.

Accepted continuous boundary laws:

```text
a=0:          mu_a >= 0
b=b_min:      mu_b >= 0
a=a_max:      mu_a <= 0
a+b=W_max:    mu_W=mu_a+mu_b <= 0
```

Boundary controls ultimately must respect the same finite controlled process in both backward HJB and forward KFE.

## Accepted DLH-5U Route-F framework

The Rev-1 design accepts the following framework objects:

- restricted-Voronoi dual cells induced only by represented W1 nodes, clipped to `D_W`, giving an a.e. partition of the physical domain;
- physical W-face segments defined from actual cell geometry rather than the masked-node staircase;
- node value plus cell-level controlled drift;
- exact discrete control-dependent Hamiltonian

```text
H_h(c,l,d)
  = u(c) - v(l)
  + sum_r q_{s->r}(c,l,d) [V_r - V_s]
  + switch;
```

- source-state face-flux/CTMC framework

```text
q_{s->r} = |F_{s,r}| * max(mu_s·n_{s,r},0) / omega_s,
Q[s,s]   = -sum_{r!=s} q_{s->r};
```

- one discrete matrix `Q` for `(Q V)` backward action and `p_dot=Q^T p` forward mass dynamics;
- nonuniform-cell mass/density semantics

```text
p = M g,
M = diag(omega_s),
Q^T p = 0,
M^{-1}Q^T M g = 0;
```

- downstream MATLAB-style component pin on mass `p`, followed by normalization and validation against the ORIGINAL `Q^T p` stationary equation.

Continuous DLH-5T effective-gradient FOCs are refinement/consistency targets only unless discrete equivalence is separately established.

## Single bounded unresolved scientific object

Tangential same-process consistency at W-adjacent restricted-Voronoi cells is still unresolved.

The exact tangent benchmark

```text
mu_a = -u,
mu_b = +u,
mu_W = 0
```

shows the earlier two-step axial cascade has an O(1) spurious normal drift at fixed accepted aspect ratio `da/db=10/7`; its first-order consistency claim is withdrawn. The simple oblique one-step candidate is not monotone on the accepted rectangular lattice.

This does **not** prove Route F impossible. Under the Rev-1 restricted-Voronoi tessellation, actual frontier cells may have oblique/diagonal Voronoi neighbors, so the next bounded design must analyze the true Voronoi adjacency and the achievable nonnegative transition-moment cone before Route F can be accepted as implementation-ready.

Reviewer clarifications controlling the next gate:

- compute `F_s^W` from `∂C_s ∩ {a+b=W_max}` directly; do not use base-cell crossing as an iff implementation test;
- keep the sliver strategy fail-closed unless either a geometric admissibility condition is pre-registered or agglomerated-cell state/control/value semantics are separately frozen;
- do not start source implementation until the tangential moment/transition object is resolved.

## Contamination interpretation

Contamination/pin remains a downstream normalization device only. Under the accepted Route-F mass convention, the parity component pin is applied to the mass system `Q^T p=0`; after solving the contaminated system, normalize and check the ORIGINAL unmodified residual. No pin-location optimization or sensitivity is authorized here.

## Scientific ceiling

Until successor authority exists, do not:

- mutate accepted household economics;
- implement restricted-Voronoi / Route-F boundary code;
- run boundary HJB/KFE/stationary/grid/domain experiments;
- choose numerical `W_max`;
- run pin sensitivity;
- compute stationary aggregates;
- rebuild two-region GE;
- run multi-province execution or neural training;
- enter nominal HANK, calibration, policy, welfare or Results.

## New-chat startup

A new session must fresh-fetch `main`, read all CURRENT rules, Task Index, this snapshot and the Roadmap, verify Issue #47 acceptance comment `5521379228` and integration `060c2835825f9efff4f89c84646f04cab6a9c8a4`, and then select/publish a bounded successor design authority before any Builder work.

Chat text is not Builder authority.
