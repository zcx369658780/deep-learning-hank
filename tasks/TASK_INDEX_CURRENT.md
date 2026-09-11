# Deep Learning + HANK Task Index

Status: `ACTIVE_BUILDER_ISSUE__DLH_5VE_REMAINING_REGULAR_W_BOUNDARY_SECTOR_CLOSURE`

Last synchronized: 2026-09-11

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

Current Issue:

**Issue #53 — OPEN**

Title:

`DLH-5V-E: Close remaining regular W-boundary sectors and full regular candidate-scoring contract`

Task type:

`SCIENTIFIC_DESIGN__REMAINING_REGULAR_W_BOUNDARY_SECTORS_AND_FULL_REGULAR_SCORING_CLOSURE`

Dedicated branch:

`dsh/issue-53-dlh-5ve-remaining-regular-sector-2026-09-11`

Owner continuation decision:

`APPROVE_DLH_5VE_REMAINING_REGULAR_W_BOUNDARY_SECTOR_CLOSURE_GATE`

Issue #53 is the sole DSH Builder authority only while it remains OPEN, CURRENT Task Index / Startup Snapshot identity matches, and the authoritative activation comment is present. Chat text alone does not create Builder authority.

## Latest accepted task — Issue #52 / DLH-5V-D

Accepted candidate:

`81705b0c1671a8ee09ee5c2f05953f3e4f9f1e8b`

Reviewer acceptance:

`5631523081`

Acceptance integration:

`d58bd962be3acc8b6f646b66643bbc96f121be57`

Accepted verdict:

`DLH_5VD_ACCEPTED__OUTCOME_A_CONFIRMED__REGULAR_REALLOCATION_CONTROL_DEPENDENT_RATE_AND_CONSERVATIVE_GENERATOR_CONTRACT_FROZEN__READY_FOR_REMAINING_REGULAR_SECTOR_GATE`

Accepted household source remains immutable/read-only:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Binding law:

```text
HJB boundary policy <=> KFE boundary transition law
```

Stationary KFE remains **NOT AUTHORIZED**.

## Accepted regular-sector authority entering DLH-5V-E

Regular tangent cone:

```text
T_W={mu_W=mu_a+mu_b<=0}.
```

Accepted `T_realloc` sector:

```text
T_realloc={mu_a<=0,mu_b>=0,mu_W<=0}.
```

Accepted candidate-control rates:

```text
q_T  = 19*mu_b/70
q_in = 19*(-mu_W)/10
```

on

```text
w_T=(-70/19,+70/19)
w_in=(-10/19,0).
```

These rates score each in-sector candidate inside the discrete `H_h` before any global regular-boundary maximization. Conservative one-Q semantics remain: actual off-diagonals nonnegative, diagonal = negative sum of actual represented outgoing rates, `Q1=0` by construction, future KFE consumes exactly `Q^T`.

## Active DLH-5V-E target

The remaining regular sector is

```text
T_rem={mu_b<0,mu_W<=0}
```

with two sub-sectors:

```text
R_reverse={mu_a>0,mu_b<0,mu_W<=0}
R_deplete={mu_a<=0,mu_b<0}.
```

DLH-5V-E must audit:

- candidate mirror exact tangent `(+7,-10)` / `(+70/19,-70/19)` for reverse reallocation;
- exact represented-destination/path/class conditions and finite deferred endpoint/joint bands;
- nonnegative reverse-reallocation candidate-control rates and scoring rule;
- local left/down representation of both-inward depletion and exact rates;
- equality/boundary ownership across all sectors;
- whether accepted sector contracts now cover all regular `mu_W<=0` candidates;
- if coverage closes, the future ONE global regular discrete-Hamiltonian argmax composition and one-Q handoff.

Endpoint/joint-boundary closure remains separately deferred. No implementation/HJB/KFE/stationary solve is authorized.

## Planned session handoff checkpoint

The chosen handoff point is **after Issue #53 is independently reviewed and, if valid, accepted**, because that closes the recurring regular W-frontier sector-design block. Before handoff, refresh this Task Index, Startup Snapshot, Master Roadmap, and a dedicated current session/project-source handoff snapshot.

Current Startup Snapshot:

`docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`

Current Master Roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
