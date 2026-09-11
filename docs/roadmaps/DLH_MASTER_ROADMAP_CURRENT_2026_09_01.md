# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.37  
**Date:** 2026-09-11  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** POST-DLH-5V-E ACCEPTED — FULL RECURRING REGULAR W-FRONTIER CONTRACT CLOSED / ENDPOINT-JOINT BOUNDARY NEXT

---

## 0. Long-run objective

Build a hybrid structural–learned regional HANK platform in which household HJB/KFE, aggregation, firm/accounting and later nominal-HANK equations remain explicit structural economics, while hard-to-specify cross-regional mappings become learned modules only after the household and equilibrium foundations pass scientific and numerical validation.

The first learned object remains regional labor/spatial mapping `W^L`. Neural training remains downstream.

---

## 1. Accepted household / finite-domain foundation

Accepted household source:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Accepted finite production-domain family:

```text
D_W(W_max) = {0<=a<=a_max, b>=b_min, a+b<=W_max}
```

Independent upper-a grid authority:

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

Restricted-Voronoi cells remain the state partition / mass-volume geometry. The same controlled backward generator `Q` must define both the discrete HJB transition term and the forward mass dynamics `p_dot=Q^T p`.

Stationary KFE remains **NOT AUTHORIZED**.

---

## 2. Accepted regular-frontier phase / adjacency — DLH-5V-A / Issue #49

Accepted candidate:

`58a0efe2e85b497d8b19c306a831d865ed65136d`

Reviewer acceptance:

`5628285587`

Integration:

`46d6961100d1a050e6b313fa2e321180ed255226`

Frozen grid:

```text
da=10/19
db=7/19
da/db=10/7
```

Regular W-frontier phase is period 7:

```text
i_t(j)=floor((N-10j)/7)
r_j=(N-10j) mod 7
r_{j+7}=r_j.
```

Endpoints/corners were explicitly deferred.

---

## 3. Accepted local shared-face obstruction — DLH-5V-B / Issue #50

Accepted candidate:

`6bc8612dc10de6d72d27c9c47d1b4d598a70a15d`

Reviewer acceptance:

`5628629099`

Integration:

`ff0afdf6d3fa0d770654613e42109318d638639d`

Accepted local shared-face cones:

```text
A^F: K = {7 mu_a + 10 mu_b <= 0}
A^L: K = {mu_a <= 0, 7 mu_a + 10 mu_b <= 0}
B^W: K = R^2
```

Exact sliding `(-u,+u)` is outside recurring top-cell shared-face cones. This rejects shared-face-only transition geometry but does not invalidate the W-domain or W1/native coordinates.

---

## 4. Accepted forward exact-tangent wide stencil — DLH-5V-C / Issue #51

Accepted candidate:

`2134a4b249eb0a79dc20d60ba1fdee830304f261`

Reviewer acceptance:

`5630191586`

Integration:

`cdbf1906963a9bf06cf117ba63072d2f1542d501`

Accepted primitive exact tangent:

```text
(Delta j,Delta i)=(-7,+10)
w_T=(-70/19,+70/19)
```

For recurring regular W-active states with `j>=7`, destination `(j-7,i+10)` is represented, its straight path stays in `D_W`, `a+b` is constant, and period-7 class/top-subtop offset are preserved. Lower-a band `j in {0,...,6}` is deferred.

Together with local inward `w_in=(-10/19,0)`, the wide edge closes

```text
T_realloc={mu_a<=0,mu_b>=0,mu_W<=0}.
```

The wide edge is a **boundary wide-stencil Markov transition**, not an ordinary shared-face finite-volume flux.

---

## 5. Accepted `T_realloc` rate / conservative generator contract — DLH-5V-D / Issue #52

Issue #52 is CLOSED completed.

Accepted candidate:

`81705b0c1671a8ee09ee5c2f05953f3e4f9f1e8b`

Reviewer acceptance:

`5631523081`

Acceptance integration:

`d58bd962be3acc8b6f646b66643bbc96f121be57`

Accepted verdict:

`DLH_5VD_ACCEPTED__OUTCOME_A_CONFIRMED__REGULAR_REALLOCATION_CONTROL_DEPENDENT_RATE_AND_CONSERVATIVE_GENERATOR_CONTRACT_FROZEN__READY_FOR_REMAINING_REGULAR_SECTOR_GATE`

For each admissible candidate in

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

Rates enter the candidate's discrete `H_h` before selection. The gate deliberately did not freeze a global regular-boundary argmax until the remaining sectors were closed.

Conservative generator semantics:

```text
Q_ij>=0 for i!=j
Q_ii=-sum actual represented outgoing rates
Q1=0 by construction
```

---

## 6. Accepted full recurring regular W-frontier closure — DLH-5V-E / Issue #53

Issue #53 accepted candidate:

`ff4607ff74ab1e0cea530ba04f17045698f43a62`

Reviewer acceptance:

`5632150936`

Acceptance integration:

`28e42e4c0f65d03aa403cf7aeedb60b83c7837e2`

Accepted verdict:

`DLH_5VE_ACCEPTED__OUTCOME_A_CONFIRMED__FULL_REGULAR_W_BOUNDARY_SECTOR_CONTRACT_FROZEN__READY_FOR_ENDPOINT_JOINT_BOUNDARY_GATE`

Accepted terminal:

`DLH_5VE_FULL_REGULAR_W_BOUNDARY_SECTOR_CONTRACT_FROZEN__READY_FOR_ENDPOINT_JOINT_BOUNDARY_GATE`

### 6.1 Reverse reallocation

```text
R_reverse={mu_a>0,mu_b<0,mu_W<=0}
```

Accepted mirror exact tangent:

```text
(Delta j,Delta i)=(+7,-10)
w_RT=(+70/19,-70/19)
```

Canonical rates:

```text
q_RT=19*mu_a/70
q_down=19*(-mu_W)/7
```

on `w_RT` and `w_down=(0,-7/19)`.

Mirror destination `(j+7,i-10)` requires both independent state conditions

```text
j<=12
i>=10
```

because `j+7<=j_max=19` and `i-10>=0`.

### 6.2 Both-inward depletion

```text
R_deplete={mu_a<=0,mu_b<0}
```

Canonical local directions/rates:

```text
w_left=(-10/19,0)
w_down=(0,-7/19)
q_left=19*(-mu_a)/10
q_down=19*(-mu_b)/7.
```

### 6.3 Full regular closure

On the accepted common regular W-active region

```text
7<=j<=12
i>=10
```

plus accepted regular class conditions:

```text
T_W={mu_W<=0}
 = T_realloc union R_reverse union R_deplete.
```

Shared boundaries are single-valued:

- `mu_b=0`: `T_realloc` equals the depletion limit;
- `mu_a=0`: depletion equals the reverse limit;
- `mu_W=0`: forward/mirror exact sliding uses the common rate `19|mu_b|/70`;
- zero drift has zero rates.

Every continuously admissible candidate in the common regular region therefore has exactly one coherent sector-specific rate/scoring contract with no omission or double counting.

### 6.4 Future global regular composition

Frozen design semantics:

```text
all admissible regular W-boundary candidates
 -> exactly one sector-specific discrete-H_h score BEFORE selection
 -> ONE global regular argmax
 -> selected control + its already-defined rates
 -> ONE conservative backward row / generator Q
 -> future KFE consumes exactly Q^T
```

No HJB/KFE solve is authorized by this design acceptance.

---

## 7. Independent KFE methodology cross-check

The separately stabilized Chapter-5 clean/source-free KFE implementation reinforces, but does not replace, DeepLearning-HANK authority:

```text
Q backward
Q^T forward
off-diagonal >=0
diagonal = -sum actual outgoing
Q1=0
same Q HJB/KFE
mass-first stationary object p
SCC/closed recurrent classes before uniqueness
original source-free Q^T p residual downstream
pin/normalization != leakage repair
```

The MATLAB-faithful contaminated-row reproduction method is not imported as production logic. DeepLearning-HANK Issue #27 component-pin authority remains unchanged.

---

## 8. Current roadmap position

```text
MATLAB-faithful two-asset household economics                 ACCEPTED
finite W-domain + continuous tangent/KKT law                 ACCEPTED
same-process HJB <=> KFE principle                           ACCEPTED
restricted-Voronoi state partition                           ACCEPTED
regular W-frontier phase / adjacency                         ACCEPTED
local shared-face moment cone                                OBSTRUCTION ACCEPTED
forward exact-tangent wide-stencil feasibility               ACCEPTED
T_realloc control-dependent rates + conservative Q           ACCEPTED
remaining regular W-boundary sectors                         ACCEPTED
full recurring regular W-frontier candidate scoring          ACCEPTED
endpoint / joint-boundary closure                            NEXT — NOT YET AUTHORIZED
boundary-HJB / finite-process implementation                 PENDING
global discrete-HJB implementation                           PENDING
same-process Q validation + SCC diagnostics                  PENDING
nested Wmax / resolution robustness                          PENDING
conservative stationary-generator validation                 PENDING
Issue #27 stationary KFE                                     NOT AUTHORIZED
stationary C,L,A,B                                           PENDING
two-region structural anchor rebuild                         PENDING
3–5 province integration                                     PENDING
learned regional W^L                                         PENDING
```

Current Builder authority: **NONE**.

---

## 9. Exact next bounded scientific block — endpoint / joint-boundary closure

The state-space complement deferred by the regular gates is now explicit:

```text
lower-a forward-wide band: j in {0,...,6}
upper-a mirror-wide band:  j in {13,...,19}
lower-b mirror-wide band:  i in {0,...,9}
```

plus:

- intersections of those bands;
- true corners / joint faces;
- W-active endpoint cells.

The next design gate should derive a finite-process transition/rate/scoring contract that respects all jointly active continuous tangent-cone/KKT constraints:

```text
a=0:       mu_a>=0
b=b_min:   mu_b>=0
a=a_max:   mu_a<=0
W face:    mu_a+mu_b<=0
```

at the appropriate intersections.

It must not:

- silently clamp a regular wide transition that leaves the grid;
- omit an off-grid destination while retaining diagonal escape;
- let KFE independently repair/rebuild the HJB boundary process;
- redesign the economic household equations without new Owner authority.

The likely successor can be named conceptually `DLH-5V-F / endpoint-joint-boundary closure`, but **no successor Issue is authorized or created by this roadmap**.

---

## 10. Downstream route after endpoint / joint-boundary closure

```text
endpoint / joint-boundary closure
 -> boundary-HJB / finite-process implementation
 -> global discrete-HJB implementation
 -> same-process Q validation + SCC/closed-class diagnostics
 -> Wmax / resolution robustness
 -> conservative stationary-generator validation
 -> Issue #27 stationary KFE
 -> stationary aggregates C,L,A,B
 -> two-region structural anchor rebuild
 -> 3–5 province integration
 -> learned regional W^L
```

Stationary KFE remains explicitly blocked until the finite controlled process is fully implemented and validated.

---

## 11. Session handoff

This conversation hands off immediately after DLH-5V-E acceptance and post-acceptance governance synchronization.

Dedicated handoff snapshot:

`docs/governance/DLH_SESSION_HANDOFF_CURRENT_2026_09_11_POST_5VE.md`

Current Task Index:

`tasks/TASK_INDEX_CURRENT.md`

Current Startup Snapshot:

`docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`

No active Builder Issue exists at handoff.

---

## 12. Audit transparency

Immediately before the DLH-5V-E integration, reviewer-side connector housekeeping accidentally created a temporary file `__does_not_exist__` on `main` in commit `51660b9a2c36529ff7e3256b5209b36bc0019716` and immediately deleted it in commit `7db0a4624630dc5cdb18c2de266635faee257ed0`.

The cumulative compare from the pre-housekeeping scientific main `72b0b4d7c0a24d7ebeb2f670f9e26ef25f8ba1ee` to `7db0a4624630dc5cdb18c2de266635faee257ed0` has **zero changed files**. No scientific or governance content changed. History is retained transparently rather than rewritten.

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.
