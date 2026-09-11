# Deep Learning + HANK Task Index

Status: `ACTIVE_BUILDER_ISSUE_54__DLH_5VF_ENDPOINT_JOINT_BOUNDARY_FINITE_PROCESS_CLOSURE`

Last synchronized: 2026-09-11

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

**ACTIVE — Issue #54 / DLH-5V-F.**

Authoritative activation comment:

`5632596303`

Authority marker:

`DLH_5VF_ENDPOINT_BAND_AND_JOINT_BOUNDARY_FINITE_PROCESS_CLOSURE_AUTHORIZED`

Task type:

`SCIENTIFIC_DESIGN__ENDPOINT_BAND_AND_JOINT_BOUNDARY_FINITE_PROCESS_CLOSURE`

Owner decision:

`APPROVE_DLH_5VF_ENDPOINT_BAND_AND_JOINT_BOUNDARY_FINITE_PROCESS_CLOSURE_GATE`

Dedicated Builder branch:

`dsh/issue-54-dlh-5vf-endpoint-joint-boundary-2026-09-11`

Issue #54 body plus its authoritative activation comments are the sole Builder task authority. This Task Index only synchronizes identity and cannot expand scope. Builder must fresh-fetch live `origin/main` and verify Issue #54 remains OPEN and all CURRENT governance agrees before mutation.

## Latest accepted task — Issue #53 / DLH-5V-E

Issue #53 is CLOSED completed.

Accepted candidate:

`ff4607ff74ab1e0cea530ba04f17045698f43a62`

Reviewer acceptance:

`5632150936`

Acceptance integration:

`28e42e4c0f65d03aa403cf7aeedb60b83c7837e2`

Accepted verdict:

`DLH_5VE_ACCEPTED__OUTCOME_A_CONFIRMED__FULL_REGULAR_W_BOUNDARY_SECTOR_CONTRACT_FROZEN__READY_FOR_ENDPOINT_JOINT_BOUNDARY_GATE`

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

Finite production domain remains:

```text
D_W(W_max) = {0<=a<=a_max, b>=b_min, a+b<=W_max}
```

Independent upper-a authority:

```text
a_max = 10
a_j = j*(10/19)
j_max = 19
```

No numerical production `W_max` is selected.

The downstream clean/source-free process contract remains:

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

Issue #27 component-pin semantics remain scale fixing only; pinning/normalization may not repair leakage.

## Accepted recurring regular W-frontier block through DLH-5V-E

Frozen grid:

```text
da = 10/19
db = 7/19
```

Common regular W-active region:

```text
7 <= j <= 12
i >= 10
```

plus accepted regular W-active/class conditions.

Accepted drift sectors:

```text
T_W={mu_W=mu_a+mu_b<=0}
 = T_realloc union R_reverse union R_deplete
```

Forward exact tangent:

```text
(j,i)->(j-7,i+10)
w_T=(-70/19,+70/19)
```

Mirror exact tangent:

```text
(j,i)->(j+7,i-10)
w_RT=(+70/19,-70/19)
```

Regular candidate composition is frozen as:

```text
candidate control
 -> continuous admissibility
 -> candidate-specific represented rates
 -> discrete H_h score BEFORE selection
 -> ONE global argmax
 -> selected control + its rates
 -> ONE conservative backward Q
 -> future KFE consumes exactly Q^T
```

No HJB/KFE solve was authorized by these design gates.

## Active scientific object — DLH-5V-F

Deferred reachability bands:

```text
lower-a forward-wide band: j in {0,...,6}
upper-a mirror-wide band:  j in {13,...,19}
lower-b mirror-wide band:  i in {0,...,9}
```

plus their intersections/corners and W-active endpoint cells.

Binding distinction:

- only `j=0` is the actual `a=0` face; `j=1,...,6` are a-interior unless another face is active;
- only `j=19` is the actual `a=a_max` face; `j=13,...,18` are a-interior;
- only `i=0` is the actual `b=b_min` face; `i=1,...,9` are b-interior.

Apply continuous tangent/KKT restrictions only on actually active faces, jointly at intersections:

```text
a=0:       mu_a>=0
b=b_min:   mu_b>=0
a=a_max:   mu_a<=0
W:         mu_a+mu_b<=0
```

Issue #54 must classify economic active sets separately from stencil reachability, enumerate only actual represented native-grid destinations, compare their nonnegative moment cones with the continuous admissible cones, derive exact rates/scoring only where feasible, and return a bounded obstruction if exact representation fails.

Hard safeguards:

- no silent clipping of unavailable transitions;
- no omitted destination with retained diagonal escape;
- no ghost/interpolation/virtual states or reflected KFE mass;
- no second KFE boundary process;
- no grid/domain/economic redesign in this gate;
- stationary KFE remains NOT AUTHORIZED.

## Downstream route

```text
DLH-5V-F endpoint/joint finite-process closure
 -> boundary-HJB / finite-process implementation
 -> global discrete-HJB implementation
 -> same-process Q validation + SCC/closed-class diagnostics
 -> nested Wmax / resolution robustness
 -> conservative stationary-generator validation
 -> Issue #27 stationary KFE
 -> stationary aggregates C,L,A,B
 -> two-region structural anchor rebuild
 -> 3–5 province integration
 -> learned regional W^L
```

## Current governance files

- `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
- `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
- Issue #54 body/comments.

The post-DLH-5V-E session handoff remains a historical checkpoint and does not override later synchronized CURRENT governance:

`docs/governance/DLH_SESSION_HANDOFF_CURRENT_2026_09_11_POST_5VE.md`
