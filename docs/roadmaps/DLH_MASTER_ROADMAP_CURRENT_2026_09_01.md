# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.34  
**Date:** 2026-09-11  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** POST-DLH-5V-D — REGULAR `T_realloc` CONTROL-DEPENDENT RATE / CONSERVATIVE GENERATOR CONTRACT ACCEPTED / REMAINING REGULAR SECTOR NEXT

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

Binding law:

```text
HJB boundary policy <=> KFE boundary transition law
```

Stationary KFE remains **NOT AUTHORIZED**.

Accepted finite production-domain family:

```text
D_W(W_max) = {0<=a<=a_max, b>=b_min, a+b<=W_max}
```

Restricted-Voronoi cells remain the state partition / mass-volume geometry. The same controlled backward generator `Q` must define the discrete HJB transition term and forward mass dynamics `p_dot=Q^T p`.

---

## 2. Accepted regular-frontier geometry and shared-face obstruction

DLH-5V-A / Issue #49 accepted the period-7 regular W-frontier geometry and actual restricted-Voronoi adjacency. DLH-5V-B / Issue #50 then proved that the local shared-face transition cone is insufficient on recurring top cells:

```text
A^F: K = {7 mu_a + 10 mu_b <= 0}
A^L: K = {mu_a <= 0, 7 mu_a + 10 mu_b <= 0}
B^W: K = R^2
```

Exact sliding `(-u,+u)` is outside the recurring top-cell shared-face cones. This rejected shared-face-only transition geometry but did not invalidate the W-domain or W1/native coordinates.

---

## 3. Accepted W1 wide-stencil regular feasibility — DLH-5V-C / Issue #51

Accepted candidate:

`2134a4b249eb0a79dc20d60ba1fdee830304f261`

Reviewer acceptance:

`5630191586`

Acceptance integration:

`cdbf1906963a9bf06cf117ba63072d2f1542d501`

Accepted exact tangent:

```text
10 Delta j + 7 Delta i = 0
(Delta j,Delta i)=(-7,+10)
w_T=(-70/19,+70/19)
```

Together with

```text
w_in=(-10/19,0)
```

it spans exactly

```text
T_realloc={mu_a<=0,mu_b>=0,mu_W=mu_a+mu_b<=0}.
```

For regular W-active states with `j>=7`, the wide destination `(j-7,i+10)` is represented, the straight segment remains in `D_W`, and the period-7 class/top-subtop offset is preserved. The finite lower-a endpoint band `j in {0,...,6}` remains deferred.

---

## 4. Accepted control-dependent rate / conservative generator contract — DLH-5V-D / Issue #52

Issue #52 is CLOSED completed.

Accepted candidate:

`81705b0c1671a8ee09ee5c2f05953f3e4f9f1e8b`

Reviewer acceptance:

`5631523081`

Acceptance integration:

`d58bd962be3acc8b6f646b66643bbc96f121be57`

Accepted verdict:

`DLH_5VD_ACCEPTED__OUTCOME_A_CONFIRMED__REGULAR_REALLOCATION_CONTROL_DEPENDENT_RATE_AND_CONSERVATIVE_GENERATOR_CONTRACT_FROZEN__READY_FOR_REMAINING_REGULAR_SECTOR_GATE`

Accepted terminal:

`DLH_5VD_REGULAR_REALLOCATION_CONTROL_DEPENDENT_RATE_AND_CONSERVATIVE_GENERATOR_CONTRACT_FROZEN__READY_FOR_REMAINING_REGULAR_SECTOR_GATE`

### 4.1 Accepted rate map on `T_realloc`

For every continuously admissible candidate control whose drift lies in `T_realloc`, define

```text
q_T  = 19*mu_b/70
q_in = 19*(-mu_W)/10
```

and divide by `h` in the fixed-aspect refinement family.

The two-ray decomposition is exact, nonnegative and unique on the sector. Equality cases `mu_b=0`, `mu_W=0`, and zero drift are continuous zero-rate boundary values, not tie-breaks.

### 4.2 Accepted discrete-Hamiltonian scope

DLH-5V-D freezes a **sector-candidate scoring rule**, not a global regular-boundary argmax.

For each admissible candidate with drift in `T_realloc`, its discrete score uses the already-defined control-dependent rates before maximization. Outside-`T_realloc` but continuously admissible candidates remain in the future global HJB choice set.

A global regular-W-boundary discrete-Hamiltonian argmax is deferred until all admissible regular sectors have accepted transition/rate contracts. Then:

```text
all admissible candidates
 -> sector-specific discrete H_h scores
 -> ONE global discrete H_h argmax
 -> selected control + its already-defined rates
 -> ONE backward Q
 -> future KFE consumes exactly Q^T
```

### 4.3 Accepted conservative generator / KFE handoff

Within the accepted sector:

```text
off-diagonal asset rates >= 0
Q_ss(asset) = -(q_in+q_T)
Q_ss = -sum(all actual represented outgoing rates)
Q1=0 by construction
```

No outside/off-grid destination may be omitted while retaining its negative diagonal escape rate. No later row-sum repair is allowed.

KFE may not independently reconstruct boundary transitions from drift. After full regular-sector closure, the selected/converged backward `Q` is the sole forward-process input and KFE uses exactly `Q^T`.

Downstream mass semantics remain:

```text
p = M g
p_dot = Q^T p
stationary source-free equation: Q^T p = 0
```

Issue #27 component-pin authority remains unchanged; pin/normalization fixes scale only and may never repair leakage.

---

## 5. Independent KFE methodology cross-check

The independently stabilized Chapter-5 clean/source-free KFE implementation is supporting methodology only, not foreign model authority. It reinforces the accepted requirements:

```text
Q backward; Q^T forward
off-diagonal >= 0
diagonal = -sum of actual outgoing rates
Q1=0
same Q for HJB and KFE
mass p as forward stationary object
pin/normalization = scale fixing only
original source-free residual required
SCC / closed recurrent classes before uniqueness claims
```

MATLAB-faithful contaminated-row reproduction logic is not imported as production logic.

---

## 6. Immediate next bounded gate

The full regular W-face tangent cone is

```text
{mu_W<=0}.
```

The accepted DLH-5V-D contract covers only `T_realloc`. The remaining admissible regular sector is

```text
{mu_W<=0} \ T_realloc
= {mu_b<0, mu_W<=0}.
```

It has two scientific sub-sectors:

1. **reverse reallocation:** `mu_a>0, mu_b<0, mu_W<=0`;
2. **both-inward depletion:** `mu_a<=0, mu_b<0`.

Recommended next gate: **remaining regular W-boundary sector transition / rate feasibility and contract design**.

No specific remedy is pre-authorized. A mirror tangent `(+7,-10)` may be an object to audit for reverse reallocation, but is not yet accepted or active. Both-inward depletion may admit a different local representation and must be classified rather than forced into the mirror-tangent route.

---

## 7. Current roadmap position

```text
MATLAB-faithful two-asset household economics                 ACCEPTED
finite W-domain + continuous tangent/KKT law                 ACCEPTED
same-process HJB <=> KFE principle                           ACCEPTED
restricted-Voronoi state partition                           ACCEPTED
regular W-frontier phase / adjacency                         ACCEPTED
local shared-face moment cone                                OBSTRUCTION ACCEPTED
W1 exact-tangent wide-stencil regular feasibility            ACCEPTED
T_realloc control-dependent rates + conservative Q contract  ACCEPTED (DLH-5V-D)
remaining regular sector {mu_b<0, mu_W<=0}                  NEXT BOUNDED GATE
endpoint / joint-boundary closure                            PENDING
boundary-HJB / finite-process implementation                 PENDING
KKT + same-process generator validation                      PENDING
nested Wmax / resolution robustness                          PENDING
conservative stationary-generator validation                 PENDING
Issue #27 stationary KFE                                     NOT AUTHORIZED
stationary C,L,A,B                                           PENDING
two-region structural anchor rebuild                         PENDING
3–5 province integration                                     PENDING
learned regional W^L                                         PENDING
```

The project remains in the final household-foundation / finite-boundary discrete-process design sequence before stationary KFE can safely resume.

---

## 8. Planned downstream sequence

If the remaining regular-sector gate closes successfully:

```text
full regular-sector transition/rate coverage
-> endpoint/joint-boundary closure
-> boundary-HJB / finite-process implementation
-> global discrete-Hamiltonian selection + same-process Q validation
-> SCC/closed-class diagnostics
-> Wmax/resolution robustness
-> conservative stationary-generator validation
-> Issue #27 stationary KFE
-> stationary aggregates C,L,A,B
-> two-region structural anchor rebuild
-> 3–5 province integration
-> learned W^L
```

If the remaining regular sector exposes a recurring obstruction, return to Owner route decision rather than forcing a KFE-only repair.

---

## 9. Downstream generator/KFE acceptance contract

When implementation is eventually authorized, acceptance must include at minimum:

- finite generator entries;
- nonnegative off-diagonal rates;
- `||Q1||_inf` / row-sum conservation;
- frozen orientation/flattening contract;
- exact same `Q` passed from HJB to KFE;
- SCC and closed recurrent-class diagnostics before uniqueness claims;
- original source-free stationary residual;
- mass normalization/nonnegativity;
- density conversion through cell weights;
- existing Issue #27 pin semantics without using pinning as leakage repair.

---

## 10. Regional / Deep Learning architecture remains downstream

The first learned object remains `W^L`. Two-region structural/unit anchor -> 3–5 province integration -> 31-province benchmark remains the scaling hierarchy. `W^K`, nominal HANK, automated calibration, policy and welfare remain later roadmap objects.

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.
