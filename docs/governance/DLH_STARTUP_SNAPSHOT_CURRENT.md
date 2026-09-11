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

**No active Builder Issue.**

Current status:

`NO_ACTIVE_BUILDER_ISSUE__DLH_5VE_ACCEPTED__ENDPOINT_JOINT_BOUNDARY_GATE_NEXT`

A successor task is not authorized until it is separately published, synchronized, and activated. Chat text alone is not Builder authority.

## Latest accepted gate — Issue #53 / DLH-5V-E

Title:

`DLH-5V-E: Close remaining regular W-boundary sectors and full regular candidate-scoring contract`

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

This closes the recurring **regular W-frontier sector-design block**. Endpoint/joint-boundary states remain separately unresolved.

## Controlling household / finite-domain authority

Accepted household source remains immutable/read-only:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Accepted finite production domain:

```text
D_W(W_max) = {0<=a<=a_max, b>=b_min, a+b<=W_max}
```

with accepted independent upper-a bound:

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

## Accepted restricted-Voronoi / mass semantics

Restricted-Voronoi cells remain the state partition / cell-volume geometry. For cell-volume matrix `M`:

```text
p = M g
p_dot = Q^T p
```

Aggregates use mass weights. The same backward generator `Q` selected by the discrete HJB must define the forward process.

Accepted clean/source-free safeguards, reinforced by the independent Chapter-5 project:

```text
Q backward
Q^T forward
Q_ij >= 0 for i != j
Q_ii = -sum of actual represented outgoing rates
Q1 = 0 by construction
HJB and KFE consume the SAME Q
SCC / closed recurrent classes before uniqueness claims
stationary original-equation Q^T p residual required
mass normalization and nonnegativity required
```

The MATLAB-faithful contaminated-row reproduction method from the Chapter-5 project is not imported as production KFE logic.

Issue #27 component-pin semantics remain unchanged: pin/normalization fixes scale only, never leakage; validate the original source-free equation afterward.

## Accepted recurring regular W-frontier science — Issues #49–#53

### DLH-5V-A / Issue #49 — phase / adjacency

Regular W-frontier phase is period 7 under

```text
da=10/19
db=7/19
10j+7i<=N
```

with accepted formulas

```text
i_t(j)=floor((N-10j)/7)
r_j=(N-10j) mod 7
r_{j+7}=r_j.
```

### DLH-5V-B / Issue #50 — local shared-face obstruction

Shared-face-only local geometry cannot represent the exact W-tangent sliding ray on recurring top-cell classes. This obstruction is accepted and bounded; it does not invalidate the W-domain or W1/native coordinates.

### DLH-5V-C / Issue #51 — forward exact-tangent wide stencil

Accepted wide tangent:

```text
(Delta j,Delta i)=(-7,+10)
w_T=(-70/19,+70/19)
```

Forward destination `(j-7,i+10)` is valid in the recurring regular region with `j>=7`; lower-a band `j in {0,...,6}` is deferred.

### DLH-5V-D / Issue #52 — forward/reallocation rate contract

For

```text
T_realloc={mu_a<=0,mu_b>=0,mu_W<=0}
```

accepted canonical rates are

```text
w_in=(-10/19,0)
w_T=(-70/19,+70/19)
q_in=19*(-mu_W)/10
q_T=19*mu_b/70.
```

They score each admissible in-sector candidate in discrete `H_h` before selection.

### DLH-5V-E / Issue #53 — remaining sectors and full regular closure

Reverse reallocation:

```text
R_reverse={mu_a>0,mu_b<0,mu_W<=0}
w_RT=(+70/19,-70/19)
w_down=(0,-7/19)
q_RT=19*mu_a/70
q_down=19*(-mu_W)/7
```

Mirror transition `(j,i)->(j+7,i-10)` requires the independent conditions

```text
j<=12
i>=10
```

because `j+7<=j_max=19` and `i-10>=0`.

Both-inward depletion:

```text
R_deplete={mu_a<=0,mu_b<0}
w_left=(-10/19,0)
w_down=(0,-7/19)
q_left=19*(-mu_a)/10
q_down=19*(-mu_b)/7.
```

On the declared common regular region

```text
7<=j<=12
i>=10
```

plus accepted regular W-active/class conditions:

```text
T_W={mu_W<=0}
  = T_realloc union R_reverse union R_deplete
```

with coherent boundary ownership and no omission/double counting.

Future regular selection semantics are frozen:

```text
all continuously admissible regular W-boundary candidates
 -> exactly one sector-specific discrete-H_h score BEFORE selection
 -> ONE global regular argmax
 -> selected control + already-defined rates
 -> ONE conservative backward row / generator Q
 -> future KFE consumes exactly Q^T
```

This is design semantics only; no HJB/KFE solve has been authorized.

## Exact unresolved endpoint / joint-boundary objects

The next scientific block is the state-space complement of the common regular region where one or both wide transitions are unavailable:

```text
lower-a forward-wide band: j in {0,...,6}
upper-a mirror-wide band:  j in {13,...,19}
lower-b mirror-wide band:  i in {0,...,9}
```

plus their intersections/corners and W-active endpoint cells.

The next gate must respect the jointly active tangent-cone/KKT restrictions at `a=0`, `a=a_max`, `b=b_min`, and `a+b=W_max`; it must not silently clip unavailable transitions or leave diagonal escape rates for omitted destinations.

## Downstream roadmap

```text
endpoint / joint-boundary closure
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

## Session handoff checkpoint

This conversation is handing off immediately after DLH-5V-E acceptance and governance synchronization.

Dedicated handoff snapshot:

`docs/governance/DLH_SESSION_HANDOFF_CURRENT_2026_09_11_POST_5VE.md`

Current Task Index:

`tasks/TASK_INDEX_CURRENT.md`

Current Master Roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
