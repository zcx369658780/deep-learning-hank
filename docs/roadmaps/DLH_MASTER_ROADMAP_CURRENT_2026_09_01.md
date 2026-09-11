# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.33  
**Date:** 2026-09-11  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** CURRENT DLH-5V-D ACTIVE — CONTROL-DEPENDENT W1 WIDE-STENCIL RATE / CONSERVATIVE GENERATOR CONTRACT

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

Accepted continuous boundary law includes `mu_a+mu_b<=0` on the artificial W face. Restricted-Voronoi cells remain the state partition / mass-volume geometry, and the same controlled backward generator `Q` must define both the discrete HJB transition term and forward mass dynamics `p_dot=Q^T p`.

---

## 2. Accepted regular-frontier geometry — DLH-5V-A / Issue #49

Accepted candidate `58a0efe2e85b497d8b19c306a831d865ed65136d`; reviewer acceptance `5628285587`; integration `46d6961100d1a050e6b313fa2e321180ed255226`.

Exact grid:

```text
da=10/19, db=7/19, da/db=10/7
```

Regular W-frontier phase is period 7. Endpoints/corners remain separately deferred.

---

## 3. Accepted local shared-face obstruction — DLH-5V-B / Issue #50

Accepted candidate `6bc8612dc10de6d72d27c9c47d1b4d598a70a15d`; reviewer acceptance `5628629099`; integration `ff0afdf6d3fa0d770654613e42109318d638639d`.

Accepted local shared-face cones:

```text
A^F: K = {7 mu_a + 10 mu_b <= 0}
A^L: K = {mu_a <= 0, 7 mu_a + 10 mu_b <= 0}
B^W: K = R^2
```

Exact sliding `(-u,+u)` is outside recurring top-cell shared-face cones. This rejected shared-face-only transition geometry but did not invalidate the W-domain or every W1 discretization.

---

## 4. Accepted W1 wide-stencil regular feasibility — DLH-5V-C / Issue #51

Issue #51 is CLOSED completed.

Accepted candidate:

`2134a4b249eb0a79dc20d60ba1fdee830304f261`

Reviewer acceptance:

`5630191586`

Acceptance integration:

`cdbf1906963a9bf06cf117ba63072d2f1542d501`

Accepted verdict:

`DLH_5VC_ACCEPTED__OUTCOME_A_CONFIRMED__W1_WIDE_STENCIL_EXACT_TANGENT_REGULAR_FEASIBILITY_FROZEN__READY_FOR_WIDE_STENCIL_RATE_GATE`

Accepted regular W-boundary wide edge:

```text
10 Delta j + 7 Delta i = 0
(Delta j,Delta i)=(-7,+10)
w_T=(-70/19,+70/19)
```

For regular W-active states with `j>=7`, the destination `(j-7,i+10)` is represented, the straight segment stays in `D_W`, and period-7 class/top-subtop offset are preserved. The finite endpoint band `j in {0,...,6}` remains deferred.

Together with local inward

```text
w_in=(-10/19,0)
```

the accepted cone satisfies

```text
cone{w_in,w_T}=T_realloc
T_realloc={mu_a<=0,mu_b>=0,mu_a+mu_b<=0}.
```

The wide edge is a **boundary wide-stencil Markov transition**, not an ordinary shared-face FV flux. Under fixed-aspect refinement its physical jump is `O(h)` and its drift-matching rate is `O(1/h)`.

---

## 5. Independent KFE methodology cross-check

An independently stabilized clean/source-free KFE implementation from the Chapter-5 two-asset HANK project supplied useful supporting safeguards. They do not replace DeepLearning-HANK authority, but they reinforce the existing same-process route:

```text
Q backward; Q^T forward
off-diagonal >= 0
diagonal = -sum of actually represented outgoing rates
Q1=0
HJB and KFE consume the same Q
mass p is the forward stationary object
pin/normalization is scale fixing only, never leakage repair
original source-free residual and recurrent-class diagnostics are downstream acceptance gates
```

The MATLAB-faithful contaminated-row reproduction method from that project is not imported as production logic. DeepLearning-HANK Issue #27 component-pin authority remains unchanged.

---

## 6. Owner continuation decision

Owner approved:

`APPROVE_DLH_5VD_CONTROL_DEPENDENT_WIDE_STENCIL_RATE_AND_CONSERVATIVE_GENERATOR_GATE`

The next gate freezes the candidate-control rate map and conservative one-`Q` generator contract in the already accepted regular reallocation sector. It does not implement the generator or solve KFE.

---

## 7. Immediate active gate — DLH-5V-D / Issue #52

### Name

**Control-Dependent W1 Wide-Stencil Rates and Conservative Same-Process Generator Contract**

Task type:

`SCIENTIFIC_DESIGN__W1_WIDE_STENCIL_CONTROL_DEPENDENT_RATE_AND_CONSERVATIVE_GENERATOR_CONTRACT`

Dedicated branch:

`dsh/issue-52-dlh-5vd-wide-stencil-rate-contract-2026-09-11`

### Exact regular-sector rate map

For each candidate control `(c,l,d)` considered **inside** the discrete-Hamiltonian maximization, if its drift lies in

```text
T_realloc={mu_a<=0,mu_b>=0,mu_W=mu_a+mu_b<=0},
```

write

```text
mu=(-a-b,+a)
a=mu_b
b=-mu_W
```

and audit/freeze

```text
q_T  = 19*mu_b/70
q_in = 19*(-mu_W)/10.
```

The selected boundary control must maximize the discrete `H_h` containing these candidate-control rates; no unconstrained continuous maximization followed by clipping/remapping is allowed.

### Conservative generator contract

For the selected control:

```text
off-diagonal rates = actually represented selected transitions
Q_ss = -sum_{r!=s} Q_sr
Q1=0 by construction
```

No omitted transition may leave behind a negative diagonal escape rate. The exact selected `Q` is the future KFE input; KFE may not reconstruct boundary transitions independently.

### Scope warning

This gate freezes only `T_realloc`. It must explicitly identify any other admissible regular W-boundary drift sector that remains unresolved. It must not silently claim full regular-boundary closure.

---

## 8. Current roadmap position

```text
MATLAB-faithful two-asset household economics                 ACCEPTED
finite W-domain + continuous tangent/KKT law                 ACCEPTED
same-process HJB <=> KFE principle                           ACCEPTED
restricted-Voronoi state partition                           ACCEPTED
regular W-frontier phase / adjacency                         ACCEPTED
local shared-face moment cone                                OBSTRUCTION ACCEPTED
W1 exact-tangent wide-stencil regular feasibility            ACCEPTED
T_realloc control-dependent wide rates + conservative Q      ACTIVE (DLH-5V-D)
remaining admissible regular W-boundary sector(s)             PENDING
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

---

## 9. Branching after DLH-5V-D

If the `T_realloc` rate/generator contract passes:

```text
DLH-5V-D accepted
-> bounded gate for any remaining admissible regular W-boundary drift sector
-> endpoint/joint-boundary closure
-> boundary-HJB / finite-process implementation
-> same-process Q validation + SCC/closed-class diagnostics
-> Wmax/resolution robustness
-> conservative stationary-generator validation
-> Issue #27 stationary KFE
-> stationary aggregates
-> regional GE
```

If the rate/generator contract is inconsistent even inside `T_realloc`, return to Owner route decision rather than repair KFE downstream.

No remaining-sector remedy is pre-authorized by this roadmap.

---

## 10. Downstream KFE validation contract

When implementation is eventually authorized, acceptance must include at minimum:

- finite generator entries;
- nonnegative off-diagonal rates;
- `||Q1||_inf` / row-sum conservation;
- frozen orientation/flattening contract;
- exact same `Q` passed from HJB to KFE;
- SCC and closed recurrent-class diagnostics before uniqueness claims;
- source-free original stationary residual;
- mass normalization/nonnegativity;
- density conversion through cell weights;
- existing Issue #27 pin semantics without using pinning as leakage repair.

These checks are recorded now but **not executed in Issue #52**.

---

## 11. Regional / Deep Learning architecture remains downstream

The first learned object remains `W^L`. Two-region structural/unit anchor -> 3–5 province integration -> 31-province benchmark remains the scaling hierarchy. `W^K`, nominal HANK, automated calibration, policy and welfare remain later roadmap objects.

---

## 12. Scientific ceiling during DLH-5V-D

Do not mutate accepted economics/source; change the production grid; implement/execute the wide generator, HJB, KFE or stationary solve; close endpoint/corner transitions; invent unaccepted remaining-sector remedies; select numerical `W_max`; redesign Issue #27 pinning; import contaminated-row KFE production logic; compute aggregates/GE; enter multi-province/neural/nominal/calibration/policy/welfare/Results.

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.
