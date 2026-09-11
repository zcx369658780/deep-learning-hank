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

`NO_ACTIVE_BUILDER_ISSUE__DLH_5VA_ACCEPTED__REGULAR_MOMENT_CONE_GATE_REQUIRED`

There is **no active Builder Issue**. DSH must remain stopped until a successor bounded scientific-design Issue is separately published, Task Index / Startup are synchronized, and an authoritative activation comment is posted.

## Latest accepted gate — Issue #49 / DLH-5V-A

Accepted candidate:

`58a0efe2e85b497d8b19c306a831d865ed65136d`

Reviewer acceptance comment:

`5628285587`

Acceptance integration:

`46d6961100d1a050e6b313fa2e321180ed255226`

Acceptance level:

`L3_COMMIT_VERIFIED__SCIENTIFIC_DESIGN_ACCEPTED`

Accepted verdict:

`DLH_5VA_ACCEPTED__OUTCOME_A_CONFIRMED__REGULAR_RESTRICTED_VORONOI_FRONTIER_PHASE_AND_ADJACENCY_FROZEN__READY_FOR_MOMENT_CONE_GATE`

Accepted terminal:

`DLH_5VA_REGULAR_VORONOI_FRONTIER_PHASE_AND_ADJACENCY_FROZEN__READY_FOR_MOMENT_CONE_GATE`

Issue #49 is to be treated as completed after reviewer closure; no successor authority is implied by the terminal.

## Controlling household / finite-domain / KFE authority

Accepted household source remains immutable/read-only:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Binding law remains:

```text
HJB boundary policy <=> KFE boundary transition law
```

Stationary KFE remains **NOT AUTHORIZED**.

Accepted finite domain:

```text
D_W(W_max) = {
  0 <= a <= a_max,
  b >= b_min,
  a+b <= W_max
}
```

No numerical production `W_max` is frozen.

Accepted restricted-Voronoi object:

```text
S(W_max) = {s=(a_j,b_i): a_j+b_i<=W_max}
C_s = {x in D_W : ||x-s||_2 <= ||x-r||_2 for all represented r in S}
```

`{C_s}` partitions `D_W` a.e.; physical W activity is defined only by the actual positive-length intersection `F_s^W = partial(C_s) intersect {a+b=W_max}`.

Accepted discrete-Hamiltonian / one-`Q` / weighted mass-density / MATLAB component-pin semantics from DLH-5U remain unchanged.

## Accepted DLH-5V-A regular-frontier result

Exact native grid:

```text
da=10/19, db=7/19, da/db=10/7
```

Symbolic phase coordinates:

```text
kappa = 19*(W_max-b_min)
N = floor(kappa)
theta = kappa-N
```

Accepted regular-frontier facts:

1. `10j+7i<=N+theta` reduces to the theta-independent represented-node set `10j+7i<=N` for `theta in [0,1)`.
2. `r_j=(N-10j) mod 7=(N-3j) mod 7`, with `r_{j+7}=r_j`; `N mod 7` fixes the regular discrete phase.
3. Theta only shifts the physical W line affinely; no regular structural phase break occurs on `[0,1)`.
4. Regular W-active cells are: staircase-top A always, sub-top B iff `r_j in {0,1,2}`; deeper regular cells are not W-active.
5. Accepted regular Voronoi neighbor displacements are axial plus the diagonal families `(-1,+1)` and `(+1,-1)` in index units; no oblique/longer regular neighbor is accepted.
6. Regular cell classes are `INT`, `A^F`, `A^L`, `B`; `A^L` uniquely has `N_V=3`.

## Still unresolved / unauthorized

- endpoint/corner frontier classes;
- geometric moment cones;
- exact sliding `(-1,+1)` feasibility in the nonnegative CTMC moment cone;
- source-state face-flux moment consistency;
- boundary-local transition-rate construction;
- Route-F implementation;
- HJB/KFE execution;
- stationary KFE;
- numerical production `W_max`;
- stationary aggregates `C,L,A,B`;
- two-region GE rebuild;
- multi-province execution / neural training / nominal HANK / calibration / policy / welfare / Results.

## Recommended next gate

A separate bounded regular-frontier **geometric moment-cone** gate should consume the accepted DLH-5V-A adjacency/displacement table and determine whether every accepted regular phase class can represent the admissible tangential reallocation cone with nonnegative local rates.

No successor Issue is active yet.

Current Master Roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`

Chat text is not Builder authority.
