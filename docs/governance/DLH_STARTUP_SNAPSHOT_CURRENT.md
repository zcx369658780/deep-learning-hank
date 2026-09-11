# Deep Learning + HANK Startup Snapshot — CURRENT

Date: 2026-09-11

Repository: `zcx369658780/deep-learning-hank`

Local Owner-designated workspace: `D:\deep-learning-hank`

## Governance state

- live GitHub `main` = synchronized repository/code/governance authority;
- GitHub Issue = sole DSH Builder authority only after publication + CURRENT synchronization + authoritative activation comment;
- DSH = bounded Builder/scientific analyst only under an active Issue;
- ChatGPT = independent reviewer / scientific-route advisor / task issuer / governance operator;
- Owner = final scientific authority;
- Builder completion is not acceptance.

Priority:

`Scientific correctness > Experiment reproducibility > Research iteration speed > Git auditability > Documentation completeness`

## Current Builder state

**ACTIVE — Issue #54 / DLH-5V-F.**

Title:

`DLH-5V-F: Close endpoint bands and joint-boundary finite-process contract`

Task type:

`SCIENTIFIC_DESIGN__ENDPOINT_BAND_AND_JOINT_BOUNDARY_FINITE_PROCESS_CLOSURE`

Owner decision:

`APPROVE_DLH_5VF_ENDPOINT_BAND_AND_JOINT_BOUNDARY_FINITE_PROCESS_CLOSURE_GATE`

Authoritative activation comment:

`5632596303`

Authority marker:

`DLH_5VF_ENDPOINT_BAND_AND_JOINT_BOUNDARY_FINITE_PROCESS_CLOSURE_AUTHORIZED`

Dedicated Builder branch:

`dsh/issue-54-dlh-5vf-endpoint-joint-boundary-2026-09-11`

Builder must fresh-fetch live `origin/main`, verify Issue #54 remains OPEN, read all CURRENT rules/governance and the full Issue/comments, confirm the same task type/branch, then work only inside the Issue allowlist. Issue body/comments are the exact task authority; this snapshot cannot expand scope.

## Latest accepted gate — Issue #53 / DLH-5V-E

Issue #53 is CLOSED completed.

Accepted candidate:

`ff4607ff74ab1e0cea530ba04f17045698f43a62`

Reviewer acceptance:

`5632150936`

Acceptance integration:

`28e42e4c0f65d03aa403cf7aeedb60b83c7837e2`

Accepted verdict:

`DLH_5VE_ACCEPTED__OUTCOME_A_CONFIRMED__FULL_REGULAR_W_BOUNDARY_SECTOR_CONTRACT_FROZEN__READY_FOR_ENDPOINT_JOINT_BOUNDARY_GATE`

This closes the recurring regular W-frontier sector-design block. Endpoint-band / joint-boundary finite-process representation is now active under Issue #54.

## Controlling household / finite-domain authority

Accepted household source remains immutable/read-only:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Accepted finite production domain:

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

Binding law:

```text
HJB boundary policy <=> KFE boundary transition law
```

Stationary KFE remains **NOT AUTHORIZED**.

## Same-process / mass semantics

Restricted-Voronoi cells remain the state partition / cell-volume geometry. For cell-volume matrix `M`:

```text
p = M g
p_dot = Q^T p
```

The same backward generator `Q` selected by the discrete HJB must define the forward process:

```text
Q backward
Q^T forward
Q_ij >= 0 for i != j
Q_ii = -sum of ACTUAL represented outgoing rates
Q1 = 0 by construction
HJB and KFE consume the SAME Q
```

Future stationary validation requires SCC / closed recurrent classes before uniqueness claims, original source-free `Q^T p` residual, mass normalization/nonnegativity, and density conversion through cell weights. Issue #27 component-pin semantics remain scale fixing only; pinning/normalization may never repair leakage.

## Accepted recurring regular W-frontier science

Frozen grid:

```text
da=10/19
db=7/19
```

Accepted common regular W-active region:

```text
7<=j<=12
i>=10
```

plus accepted regular W-active/class conditions.

Accepted sectors:

```text
T_W={mu_W=mu_a+mu_b<=0}
 = T_realloc union R_reverse union R_deplete
```

Forward exact tangent wide transition:

```text
(j,i)->(j-7,i+10)
w_T=(-70/19,+70/19)
```

Mirror exact tangent wide transition:

```text
(j,i)->(j+7,i-10)
w_RT=(+70/19,-70/19)
```

Local inward directions:

```text
w_left=(-10/19,0)
w_down=(0,-7/19)
```

Regular selection semantics are frozen:

```text
all continuously admissible regular candidates
 -> exactly one sector-specific discrete-H_h score before selection
 -> ONE global regular argmax
 -> selected control + already-defined rates
 -> ONE conservative backward Q
 -> future KFE consumes exactly Q^T
```

No HJB/KFE solve was authorized by the regular design gates.

## Active scientific object — DLH-5V-F / Issue #54

Deferred reachability bands:

```text
lower-a forward-wide band: j in {0,...,6}
upper-a mirror-wide band:  j in {13,...,19}
lower-b mirror-wide band:  i in {0,...,9}
```

plus their intersections/corners and W-active endpoint cells.

### Critical state classification rule

A stencil-reachability band is **not** an economic boundary face:

- `j=0` is the actual `a=0` face; `j=1,...,6` remain a-interior unless another face is active;
- `j=19` is the actual `a=a_max` face; `j=13,...,18` remain a-interior;
- `i=0` is the actual `b=b_min` face; `i=1,...,9` remain b-interior.

Continuous tangent/KKT laws apply only to actually active faces, jointly at intersections:

```text
a=0:       mu_a>=0
b=b_min:   mu_b>=0
a=a_max:   mu_a<=0
W:         mu_a+mu_b<=0
```

Issue #54 must first classify economic active sets and stencil reachability separately; then enumerate actual represented native-grid destinations, derive their nonnegative first-moment cones, and compare those cones with the continuous admissible drift cones.

Exact W-tangent lattice identity remains:

```text
10 Delta j + 7 Delta i = 0
```

The primitive same-W native-grid displacement is generated by `(-7,+10)` / `(+7,-10)`. If a continuously admissible deferred-state drift cannot be exactly represented by actual allowed destinations with nonnegative rates, the correct scientific result is a bounded obstruction certificate.

Do not silently clip, inject an unacknowledged inward normal component, create ghost/interpolation states, omit an off-grid destination while retaining diagonal escape, or let KFE rebuild another boundary process.

## Current Issue #54 outcome ceiling

Even full Outcome A can establish only a design-level endpoint/joint finite-process contract. It does not authorize:

- boundary-HJB implementation without a separately accepted successor gate;
- global discrete-HJB execution;
- numerical `W_max` selection;
- stationary-generator execution;
- stationary KFE;
- stationary aggregates / GE / regional / neural / nominal / calibration / policy / welfare / Results.

## Downstream roadmap

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

## Current authoritative files

- `tasks/TASK_INDEX_CURRENT.md`
- `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
- `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
- Issue #54 body/comments.

The file `docs/governance/DLH_SESSION_HANDOFF_CURRENT_2026_09_11_POST_5VE.md` is the historical post-5V-E conversation checkpoint. It records the pre-successor state and does not override later synchronized CURRENT governance.
