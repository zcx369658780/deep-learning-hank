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

**Issue #50 — DLH-5V-B: Regular restricted-Voronoi geometric moment-cone analysis**

Task type:

`SCIENTIFIC_DESIGN__REGULAR_VORONOI_GEOMETRIC_MOMENT_CONE`

Dedicated branch:

`dsh/issue-50-dlh-5vb-regular-voronoi-moment-cone-2026-09-11`

Owner continuation decision:

`APPROVE_DLH_5VB_REGULAR_VORONOI_GEOMETRIC_MOMENT_CONE_GATE`

Builder authority is active only while Issue #50 remains OPEN, CURRENT Task Index / this Snapshot identity matches, and the authoritative activation comment is present.

## Latest accepted gate — Issue #49 / DLH-5V-A

Issue #49 is CLOSED completed.

Accepted candidate:

`58a0efe2e85b497d8b19c306a831d865ed65136d`

Reviewer acceptance:

`5628285587`

Acceptance integration:

`46d6961100d1a050e6b313fa2e321180ed255226`

Accepted verdict:

`DLH_5VA_ACCEPTED__OUTCOME_A_CONFIRMED__REGULAR_RESTRICTED_VORONOI_FRONTIER_PHASE_AND_ADJACENCY_FROZEN__READY_FOR_MOMENT_CONE_GATE`

## Controlling household / finite-domain / KFE authority

Accepted household source remains immutable/read-only:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Binding law:

```text
HJB boundary policy <=> KFE boundary transition law
```

Stationary KFE remains **NOT AUTHORIZED**.

Accepted finite domain:

```text
D_W(W_max) = {0<=a<=a_max, b>=b_min, a+b<=W_max}
```

No numerical production `W_max` is selected.

## Accepted Route-F / regular-frontier geometry

Restricted-Voronoi cells remain the accepted finite-volume geometry:

```text
S = {s=(a_j,b_i): a_j+b_i<=W_max}
C_s = {x in D_W: ||x-s||<=||x-r|| for all represented r}
```

DLH-5V-A froze the regular W-frontier phase/adjacency structure. Exact physical displacement map:

```text
Delta x_sr = ((10/19) Delta j, (7/19) Delta i)
```

W-active regular classes:

```text
A^F: (-1,0), (0,-1), (-1,+1), (+1,-1)
A^L: (-1,0), (0,-1), (-1,+1)
B^W: (-1,0), (0,-1), (0,+1), (+1,-1)
```

The classification is structurally theta-independent over `theta in [0,1)` and repeats with the accepted period-7 phase structure. Endpoints/corners remain deferred.

## Current DLH-5V-B scientific target

For each W-active regular class define

```text
K_s = cone{Delta x_sr}
```

with nonnegative coefficients and compare to

```text
T_realloc = {mu_a<=0, mu_b>=0, mu_a+mu_b<=0}.
```

Mandatory exact sliding benchmark:

```text
mu=(-u,+u), u>0.
```

The gate asks only whether the accepted local shared-face geometry can represent the full continuous tangential cone monotonically. If not, it may establish a bounded geometric obstruction; it may not design a remedy or declare every possible Route-F discretization impossible.

## Context-budget rule

After all CURRENT project rules, current Task Index / this Snapshot / Roadmap, and full Issue #50 + comments, required scientific reading is limited to:

1. `docs/design/DLH_5VA_REGULAR_VORONOI_FRONTIER_PHASE_AND_ADJACENCY.md`
2. `reports/dlh_5va_regular_voronoi_frontier_2026_09_10/DLH_5VA_VORONOI_ADJACENCY_AND_DISPLACEMENTS.md`

Read `DLH_5VA_PHASE_CLASSIFICATION.md` only if one class-condition definition is unclear. Do not reread broad DLH-5T/DLH-5U history without a concrete contradiction.

## Exact allowlist

Four files only, exactly as listed in Issue #50. No existing tracked file may be modified by Builder.

## Scientific ceiling

Do not mutate source/economics; run broad phase/Voronoi enumeration; design production rates; audit strict face-flux moment maps; analyze endpoint/corner transitions; implement/execute HJB/KFE/stationary; select numerical `W_max`; compute aggregates/GE; run multi-province or neural training; or enter nominal HANK, calibration, policy, welfare or Results.

## Intended route after this gate

If the regular geometric cone is feasible:

```text
DLH-5V-B regular moment-cone closure
-> bounded boundary-local rate / strict face-flux audit
-> endpoint/corner closure
-> boundary-HJB / Route-F implementation
-> KKT + same-process generator validation
-> Wmax / resolution robustness
-> conservative stationary-generator validation
-> Issue #27 stationary KFE
-> C,L,A,B
-> two-region structural anchor
-> 3–5 province integration
-> learned W^L
```

If a regular shared-face cone obstruction is proven, the next step is an Owner route decision on a bounded remedy before implementation.

Chat text is not Builder authority.
