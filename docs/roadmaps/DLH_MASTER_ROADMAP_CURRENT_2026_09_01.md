# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.42  
**Date:** 2026-09-12  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** DLH-5V-H / ISSUE #56 ACTIVE — ROUTE E STATE-CONSTRAINT HJB CONSISTENCY-TARGET AUDIT

---

## 0. Long-run objective

Build a hybrid structural–learned regional HANK platform in which household HJB/KFE, aggregation, firm/accounting and later nominal-HANK equations remain explicit structural economics, while hard-to-specify cross-regional mappings become learned modules only after household and equilibrium foundations pass scientific and numerical validation.

The first learned object remains regional labor/spatial mapping `W^L`. Neural training remains downstream.

---

## 1. Accepted household / finite-domain foundation

Accepted household source:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Accepted finite production-domain family:

```text
D_W(W_max)={0<=a<=a_max,b>=b_min,a+b<=W_max}
a_max=10
b_min=-2
```

No numerical production `W_max` is selected.

Binding law:

```text
HJB boundary policy <=> KFE boundary transition law
```

Restricted-Voronoi cells remain the accepted state partition / mass-volume geometry unless a later Owner-authorized route changes them. The same selected backward generator `Q` must define future forward mass dynamics `p_dot=Q^T p`.

Stationary KFE remains **NOT AUTHORIZED**.

---

## 2. Accepted regular finite-process block — DLH-5V-A through DLH-5V-E

Base native grid:

```text
da=10/19
db=7/19
10j+7i<=N
```

Accepted common regular W-active region at m=1:

```text
7<=j<=12
i>=10
```

plus accepted W-active/class conditions.

Accepted sector coverage:

```text
T_W={mu_W<=0}=T_realloc union R_reverse union R_deplete
```

with exact tangent moves

```text
w_T=(-70/19,+70/19)
w_RT=(+70/19,-70/19)
```

and local inward moves

```text
w_left=(-10/19,0)
w_down=(0,-7/19).
```

Candidate semantics remain frozen:

```text
continuous admissibility
 -> candidate-specific represented nonnegative rates
 -> discrete H_h score BEFORE selection
 -> ONE global statewise argmax
 -> selected rates
 -> ONE conservative backward Q
 -> future KFE consumes exactly Q^T
```

---

## 3. Issue #54 / DLH-5V-F — exact endpoint finite-process obstruction — ACCEPTED

Accepted candidate: `b9dab7b6cf5d724074765ddb88d6f300175f6c6f`

Reviewer acceptance: `5633995486`

Acceptance integration: `4e77d9c753f81eb2517a8b90a0827db6af8faed4`

Accepted verdict:

`DLH_5VF_ACCEPTED__OUTCOME_C_CONFIRMED__EXACT_ENDPOINT_FINITE_PROCESS_REPRESENTABILITY_OBSTRUCTION_FROZEN__OWNER_APPROXIMATION_ROUTE_DECISION_REQUIRED`

At exact-frontier `r_j=0` endpoint states, exact tangent drift can require a same-W lattice orientation unavailable on the native endpoint band. Hence native states + nonnegative rates + exact finite-m first moments for every endpoint candidate + exact same-process semantics cannot all be retained globally.

This is a lattice/discretization obstruction, not a household-source or KFE-repair issue.

---

## 4. Issue #55 / DLH-5V-G — Route A shrinking-layer audit — OUTCOME C ACCEPTED

Accepted candidate: `15f2f81653a847344d2cd647705487cc893af1d7`

Reviewer acceptance: `5635802416`

Acceptance integration: `8dd5e9c444d7356736f28a29b9ffe492bbe81caa`

Accepted verdict:

`DLH_5VG_ACCEPTED__OUTCOME_C_CONFIRMED__ROUTE_A_TANGENT_CONE_GRAPH_CONSISTENCY_OBSTRUCTION_FROZEN__OWNER_ROUTE_REDECISION_REQUIRED`

Accepted terminal:

`DLH_5VG_ROUTE_A_ASYMPTOTIC_ENDPOINT_APPROXIMATION_OBSTRUCTION__OWNER_ROUTE_REDECISION_REQUIRED`

Issue #55 proved that its strong raw admitted-drift graph outer/limsup + recovery/liminf convergence target is impossible on the frozen state family. The controlling example is a non-W-active interior sequence such as

```text
s_m=(0,i_t^m(0)-2), mu=(0,1),
```

which converges physically to the true `a=0 x W` corner while still admitting/exactly representing an outward-W drift at finite m.

The strong Issue-#55 result remains accepted. What is not yet established is whether that raw drift-set graph target is itself necessary for state-constraint HJB viscosity convergence.

---

## 5. Owner-selected next route — Route E theory audit

Owner approved:

`APPROVE_DLH_5VH_ROUTE_E_STATE_CONSTRAINT_HJB_CONSISTENCY_TARGET_AUDIT`

Scientific rationale: before paying the much larger cost of boundary-state augmentation, grid redesign or coordinate transformation, audit the actual mathematical boundary-consistency object required by state-constraint HJB / viscosity-solution / monotone-scheme convergence theory.

This route does **not** pre-accept that Issue #55 was over-strong. It must prove/refute that proposition.

---

## 6. DLH-5V-H / Issue #56 — ACTIVE

Title:

`DLH-5V-H: Audit state-constraint HJB boundary consistency target before geometry redesign`

Task type:

`SCIENTIFIC_THEORY_AUDIT__STATE_CONSTRAINT_HJB_BOUNDARY_CONSISTENCY_TARGET`

Authoritative activation comment:

`5641527846`

Authority marker:

`DLH_5VH_ROUTE_E_STATE_CONSTRAINT_HJB_CONSISTENCY_TARGET_AUDIT_AUTHORIZED`

Dedicated Builder branch:

`dsh/issue-56-dlh-5vh-state-constraint-consistency-audit-2026-09-12`

### 6.1 Theory-first sequence

The gate must proceed in this order:

```text
continuous state-constraint HJB / viscosity target
 -> primary-theory sign + hypothesis mapping
 -> necessity audit of Issue-55 raw graph condition
 -> weakest defensible monotone-scheme boundary consistency target
 -> design-level frozen-process test under that legitimate target
```

It may not begin by redesigning stencils or geometry.

### 6.2 Mandatory primary anchors

The Issue requires applicability audits of Soner (1986) state-space constraint Parts I/II and Barles–Souganidis (1991), with additional primary references allowed when required. Generic theorem citation without state-constraint boundary/sign/comparison/stability mapping is not evidence.

### 6.3 Mandatory falsification

The Issue-#55 lower/upper corner counterexamples must be retested under the legitimate viscosity/operator consistency notion. A minimal state-constraint toy scheme must discriminate whether interior nodes approaching a boundary may retain interior/outward controls while a monotone scheme remains viscosity-consistent through the correct boundary test.

### 6.4 Possible outcomes

- freeze a weaker legitimate consistency target and preserve design-level viability of the frozen process;
- isolate one bounded theory/comparison gap;
- show the weaker legitimate target still rejects the frozen process;
- or confirm that the strong graph obstruction (or an equivalent necessary condition) truly requires geometry redesign.

No outcome self-authorizes implementation.

---

## 7. Current roadmap position

```text
MATLAB-faithful two-asset household economics                 ACCEPTED
finite W-domain + continuous tangent/KKT law                 ACCEPTED
same-process HJB <=> KFE principle                           ACCEPTED
restricted-Voronoi state partition                           ACCEPTED
regular W-frontier phase / adjacency                         ACCEPTED
shared-face-only local process                               OBSTRUCTION ACCEPTED
regular exact-tangent wide-stencil process                   ACCEPTED
regular control-dependent rates / global scoring             ACCEPTED
endpoint exact finite-process closure                         OBSTRUCTION ACCEPTED — ISSUE #54
Route A strong graph-consistency target                       OBSTRUCTION ACCEPTED — ISSUE #55
Route E state-constraint HJB consistency-target audit         ACTIVE — ISSUE #56
boundary-HJB scheme design / implementation                  BLOCKED PENDING 5V-H
same-process Q validation + SCC diagnostics                  PENDING
nested Wmax / resolution robustness                          PENDING
conservative stationary-generator validation                 PENDING
Issue #27 stationary KFE                                     NOT AUTHORIZED
stationary C,L,A,B                                           PENDING
two-region structural anchor rebuild                         PENDING
3–5 province integration                                     PENDING
learned regional W^L                                         PENDING
```

---

## 8. Same-process safeguards — frozen

```text
Q backward
Q^T forward
Q_ij>=0 for i!=j
Q_ii=-sum of ACTUAL represented outgoing rates
Q1=0 by construction
same selected Q for HJB and KFE
p=M g
p_dot=Q^T p
```

No route may use pinning/normalization to repair leakage or create a KFE-only process.

Stationary KFE remains explicitly blocked.

---

## 9. Interpretation ceiling

DLH-5V-H is analytic/theory-design only. It does not authorize source implementation, production generator assembly/run, HJB/KFE/stationary computation, numerical production `W_max`, state augmentation, grid/aspect/domain redesign, coordinate transformation, aggregates, GE, multi-region, neural, nominal, calibration, policy, welfare or Results prose.

---

## 10. Current governance pointers

- `tasks/TASK_INDEX_CURRENT.md`
- `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
- Issue #56 body/comments.

Issue #54 and #55 acceptance histories remain controlling provenance for the two distinct obstructions.

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.
