# Deep Learning + HANK Task Index

Status: `NO_ACTIVE_BUILDER_ISSUE__DLH_5VA_ACCEPTED__REGULAR_MOMENT_CONE_GATE_REQUIRED`

Last synchronized: 2026-09-11

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

**NONE.**

Issue #49 / DLH-5V-A has been scientifically accepted. DSH must remain stopped until a successor bounded Issue is separately published, CURRENT Task Index / Startup Snapshot are synchronized to it, and an authoritative activation comment is posted.

Chat text alone does not create Builder authority.

## Latest accepted task — Issue #49 / DLH-5V-A

Title:

`DLH-5V-A: Classify regular restricted-Voronoi W-frontier phases and adjacency`

Task type:

`SCIENTIFIC_DESIGN__REGULAR_VORONOI_FRONTIER_PHASE_AND_ADJACENCY_CLASSIFICATION`

Accepted candidate:

`58a0efe2e85b497d8b19c306a831d865ed65136d`

Reviewer acceptance comment:

`5628285587`

Acceptance integration commit:

`46d6961100d1a050e6b313fa2e321180ed255226`

Acceptance level:

`L3_COMMIT_VERIFIED__SCIENTIFIC_DESIGN_ACCEPTED`

Accepted verdict:

`DLH_5VA_ACCEPTED__OUTCOME_A_CONFIRMED__REGULAR_RESTRICTED_VORONOI_FRONTIER_PHASE_AND_ADJACENCY_FROZEN__READY_FOR_MOMENT_CONE_GATE`

Accepted terminal:

`DLH_5VA_REGULAR_VORONOI_FRONTIER_PHASE_AND_ADJACENCY_FROZEN__READY_FOR_MOMENT_CONE_GATE`

## Accepted regular-frontier authority

Accepted household source remains immutable/read-only:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Binding law remains:

```text
HJB boundary policy <=> KFE boundary transition law
```

Stationary KFE remains **NOT AUTHORIZED**.

Accepted finite domain / restricted-Voronoi framework remains:

```text
D_W(W_max) = {0<=a<=a_max, b>=b_min, a+b<=W_max}
S(W_max)   = {s=(a_j,b_i): a_j+b_i<=W_max}
C_s        = {x in D_W: ||x-s||<=||x-r|| for all represented r}
```

Exact grid:

```text
da=10/19, db=7/19, da/db=10/7
```

For regular non-endpoint frontier cells:

- represented-node set is `10j+7i<=N`, independent of `theta in [0,1)`;
- regular discrete phase is period 7 with `r_j=(N-10j) mod 7=(N-3j) mod 7`;
- `N mod 7` fixes the discrete regular-frontier phase; theta moves the W line affinely without a structural break;
- top A cell is W-active for every defect;
- sub-top B cell is W-active iff `r_j in {0,1,2}`;
- deeper regular cells are not W-active;
- accepted regular neighbor families are axial plus NW/SE diagonal only; no oblique/longer regular neighbor is accepted;
- regular types are `INT`, `A^F`, `A^L`, and `B`; `A^L` is the unique regular class with `N_V=3`.

## Next bounded scientific object

The next recommended gate is a **regular-frontier geometric moment-cone analysis** using the now-frozen actual Voronoi neighbor/displacement sets.

It should determine, for every accepted regular phase class, whether the nonnegative displacement cone contains the admissible tangential reallocation directions, especially exact sliding `(-1,+1)`.

This successor is NOT yet active.

Endpoint/corner closure, source-state face-flux moment audit, boundary-local rate construction, implementation, HJB/KFE, stationary KFE, numerical production `W_max`, aggregates, GE, and neural training remain downstream and unauthorized.

## Superseded Issue #48

Issue #48 remains CLOSED `not_planned` for operational context-budget reasons only and carries no scientific verdict.

Current Startup Snapshot:

`docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`

Current Master Roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
