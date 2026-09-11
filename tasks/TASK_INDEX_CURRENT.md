# Deep Learning + HANK Task Index

Status: `NO_ACTIVE_BUILDER_ISSUE__DLH_5VE_ACCEPTED__ENDPOINT_JOINT_BOUNDARY_GATE_NEXT`

Last synchronized: 2026-09-11

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

**NONE.**

No GitHub Issue currently grants DSH Builder authority. Chat text alone does not create Builder authority.

A successor task must be separately published, synchronized into CURRENT governance, and activated by an authoritative activation comment before Builder work begins.

## Latest accepted task — Issue #53 / DLH-5V-E

Title:

`DLH-5V-E: Close remaining regular W-boundary sectors and full regular candidate-scoring contract`

Task type:

`SCIENTIFIC_DESIGN__REMAINING_REGULAR_W_BOUNDARY_SECTORS_AND_FULL_REGULAR_SCORING_CLOSURE`

Accepted candidate:

`ff4607ff74ab1e0cea530ba04f17045698f43a62`

Reviewer acceptance:

`5632150936`

Acceptance integration:

`28e42e4c0f65d03aa403cf7aeedb60b83c7837e2`

Accepted verdict:

`DLH_5VE_ACCEPTED__OUTCOME_A_CONFIRMED__FULL_REGULAR_W_BOUNDARY_SECTOR_CONTRACT_FROZEN__READY_FOR_ENDPOINT_JOINT_BOUNDARY_GATE`

Accepted terminal:

`DLH_5VE_FULL_REGULAR_W_BOUNDARY_SECTOR_CONTRACT_FROZEN__READY_FOR_ENDPOINT_JOINT_BOUNDARY_GATE`

Issue #53 is to be CLOSED completed after this post-acceptance governance synchronization. No successor authority is created by acceptance or closure.

## Controlling household / same-process authority

Accepted household source remains immutable/read-only:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Binding law:

```text
HJB boundary policy <=> KFE boundary transition law
```

Stationary KFE remains **NOT AUTHORIZED**.

The downstream clean/source-free generator contract remains:

```text
Q = backward controlled generator
Q^T = forward mass operator
off-diagonal >= 0
diagonal = -sum of actual represented outgoing rates
Q1 = 0 by construction
same selected Q for HJB and KFE
p = M g
p_dot = Q^T p
```

Issue #27 component-pin authority remains downstream scale fixing only; pinning/normalization may not repair leakage, and the original source-free `Q^T p` residual must be validated.

## Accepted recurring regular W-frontier block through DLH-5V-E

Finite production domain:

```text
D_W(W_max) = {0<=a<=a_max, b>=b_min, a+b<=W_max}
```

Frozen grid:

```text
da = 10/19
db = 7/19
a_max = 10
j_max = 19
```

Regular W-face tangent cone:

```text
T_W = {mu_W = mu_a + mu_b <= 0}
```

### Sector 1 — forward reallocation (`T_realloc`)

```text
T_realloc = {mu_a<=0, mu_b>=0, mu_W<=0}
w_in = (-10/19,0)
w_T  = (-70/19,+70/19)
q_in = 19*(-mu_W)/10
q_T  = 19*mu_b/70
```

Forward wide transition:

```text
(j,i) -> (j-7,i+10)
```

requires `j>=7` away from the lower-a endpoint band.

### Sector 2 — reverse reallocation

```text
R_reverse = {mu_a>0, mu_b<0, mu_W<=0}
w_RT   = (+70/19,-70/19)
w_down = (0,-7/19)
q_RT   = 19*mu_a/70
q_down = 19*(-mu_W)/7
```

Mirror wide transition:

```text
(j,i) -> (j+7,i-10)
```

requires independent bounds `j<=12` and `i>=10`.

### Sector 3 — both-inward depletion

```text
R_deplete = {mu_a<=0, mu_b<0}
w_left = (-10/19,0)
w_down = (0,-7/19)
q_left = 19*(-mu_a)/10
q_down = 19*(-mu_b)/7
```

On the declared common regular region

```text
7 <= j <= 12
i >= 10
```

plus the accepted regular W-active/class conditions, the accepted sector contracts cover all `T_W` candidates without omission or double counting. Shared boundary rays are single-valued.

Future regular candidate selection is frozen as design semantics:

```text
all admissible regular candidates
 -> exactly one sector-specific discrete-H_h score before selection
 -> ONE global regular argmax
 -> selected control + already-defined rates
 -> ONE conservative backward Q
 -> future KFE consumes exactly Q^T
```

No HJB/KFE solve has been authorized or performed by these design gates.

## Exact next bounded scientific object — NOT YET AUTHORIZED

The scientifically natural successor is an **endpoint / joint-boundary closure gate**.

Deferred state-space bands are:

```text
lower-a forward-wide band: j in {0,...,6}
upper-a mirror-wide band:  j in {13,...,19}
lower-b mirror-wide band:  i in {0,...,9}
```

plus their intersections/corners and W-active endpoint cells.

The successor must derive tangent-cone-consistent candidate scoring / represented transition contracts for these states without silent clipping, omitted-destination/retained-diagonal leakage, or a second KFE process.

Do **not** create or execute a successor from this Task Index alone.

## Session handoff

Current dedicated handoff snapshot:

`docs/governance/DLH_SESSION_HANDOFF_CURRENT_2026_09_11_POST_5VE.md`

Current Startup Snapshot:

`docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`

Current Master Roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
