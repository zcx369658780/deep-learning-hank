# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.10  
**Date:** 2026-09-02  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** CURRENT OWNER-APPROVED SCIENTIFIC ROUTE

---

## 0. Long-run objective

Build a data-to-structural-model calibration and regional-network HANK platform in which household HJB/KFE, aggregation, firm/accounting blocks and later nominal-HANK equations remain explicit structural economics, while difficult cross-regional mappings become interpretable learned modules only after household and equilibrium foundations pass scientific and numerical validation.

The first learned object remains the regional labor/spatial rule. Capital-network learning and nominal-HANK integration remain later stages.

---

## 1. Accepted household foundation through DLH-5L

### Household source — Issue #23

Accepted MATLAB-faithful source:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Identity:

- Git blob `76ae5b149993a7edeeb337f1b02b3fe33c51e`
- SHA-256 `1795718C469FC3B427CAB8E3D5957C133BEAD6EACC9EF0A25A3EDB7211D1A024`

### Stationary-KFE contract — Issues #26–#27

Binding law:

```text
HJB boundary policy <=> KFE boundary transition law
```

Any eventual stationary density must satisfy the ORIGINAL `Q^T g=0`, mass/non-negativity, conservative-generator/recurrent-class/nullspace evidence, pin admissibility and valid-pin invariance before aggregates are accepted.

### Boundary/domain diagnostics — Issues #28–#36

Accepted findings:

- canonical D0 HJB converges but artificial upper asset bounds initially receive outward requests;
- b-only extent strongly attenuates liquid-boundary influence;
- widening `a_max` is confounded by the accepted normalized illiquid-return taper;
- refining the fixed physical a domain resolves upper-a but reactivates upper-b, establishing coupled domain/resolution behavior;
- at mature a77/a153, upper-b attenuates monotonically with b extent;
- a77 reaches componentwise joint compatibility at b160 while a153 remains outward at b160;
- no cross-a jointly compatible rectangular extent exists through the hard b160 ceiling;
- the pure larger-b-grid route is CLOSED: no b180/b200/adaptive/root-seeking PASS search.

### High-wealth / upper-corner mechanism — Issue #37 / DLH-5K

Accepted candidate:

`aaead4a1368ec061ac1e380c3af33d93c0f31161`

Integrated to main:

`d26b2b8c8d69d2afa2cb9806f120d03ebe973752`

Accepted verdict:

`DLH_5K_ISSUE_37_IMPLEMENTATION_ACCEPTED__MIXED_LOCALIZATION_CONFIRMED__TRANSFER_DERIVATIVE_CHANNEL_DOMINATES_CROSS_A_DIVERGENCE__INTERPRETATION_NARROWED__NEXT_GATE_REQUIRED`

Accepted interpretation:

1. 5/17 top upper-b offenders are boundary-only within the pre-frozen local window; 12/17 retain positive liquid drift in at least one inspected interior layer.
2. This is local finite-window persistence, not proof of infinite-domain non-mean-reversion.
3. Positive `mu_b` is produced when positive transfer injection dominates a negative base liquid surplus.
4. a77/a153 liquid-drift divergence is primarily transfer/derivative-channel driven.
5. The accepted selected transfer candidate fails joint rectangular inwardness at inspected states, but no no-feasible-transfer theorem is established.
6. Transfer `d` is a continuous-time flow/rate, not an asset stock.

### Total-asset drift / geometry adjudication — Issue #38 / DLH-5L

Accepted candidate:

`3df43fe4da552e19aa7cd3486e06a7e5042d97df`

Integrated to main:

`b20e23e28d2f9969df06cb725b3ca23a6fecc2fe`

Accepted verdict:

`DLH_5L_ISSUE_38_IMPLEMENTATION_ACCEPTED__TOTAL_ASSET_DRIFT_INWARD_ON_PREFROZEN_HIGH_WEALTH_STATE_SET__RECTANGULAR_B_VIOLATION_REINTERPRETED_AS_COMPONENTWISE_REALLOCATION__CROSS_A_TOTAL_DRIFT_SENSITIVITY_REMAINS__DOMAIN_KKT_DESIGN_REVIEW_REQUIRED`

Accepted scientific interpretation:

1. J0–J5 reproduce accepted HJB/boundary evidence exactly and deterministically.
2. The pre-frozen accepted evidence set contains 105 unique high-wealth states.
3. All 44 material positive-`mu_b` states satisfy `mu_W=mu_a+mu_b<=0`; no inspected state has total-asset outward drift.
4. All 17 top-layer upper-b offenders violate rectangular b-inwardness while satisfying a-inwardness and total-asset inwardness.
5. The source accounting identity confirms one-for-one cancellation of the linear transfer term in `mu_W`; adjustment cost remains.
6. This supports a portfolio-reallocation/domain-geometry interpretation on the pre-frozen finite state set. It is not an infinite-domain mean-reversion theorem, stationary-tail proof, or authorization to replace the production domain by `W=a+b`.
7. Absolute cross-a total-drift differences are much smaller than liquid-coordinate differences, but relative total-drift differences still exceed the existing 1e-2 diagnostic threshold on 16/24 aligned pairs.
8. No HJB/KFE/domain/taper/FOC/adjustment-cost mutation is accepted.
9. Stationary KFE remains NOT AUTHORIZED.

---

## 2. Immediate model-design gate — DLH-5M / Issue #39

### Name

**State-Domain Geometry and Joint HJB/KKT Boundary-Law Design Review**

Task type:

`SCIENTIFIC_DESIGN_REVIEW__STATE_DOMAIN_GEOMETRY_AND_JOINT_KKT`

### Purpose

The project has reached a model-defining question. Further grid enlargement is scientifically closed, and accepted evidence alone does not authorize a domain change.

The design review must answer:

> Which state-domain geometry and state-constraint HJB/KKT law best distinguish structural household constraints from computational truncations while preserving the accepted two-asset accounting, transfer technology, taper, and exact HJB/KFE controlled-process matching?

DLH-5M is design-only. It cannot change the model.

### Mandatory boundary classification

Classify at minimum:

```text
a >= 0
b >= b_min
current a <= a_max=10
current b <= b_max
accepted a_max-normalized illiquid-return taper
```

Each must be identified as structural/economic, computational truncation, numerical-stabilization related, or unresolved/Owner decision.

### Candidate R — rectangular componentwise constraints

If the rectangular domain is retained, the state-constraint HJB must use controls admissible to the active tangent cone:

```text
upper-a: mu_a <= 0
upper-b: mu_b <= 0
upper corner: mu_a <= 0 AND mu_b <= 0
```

DLH-5M must derive the generic constrained Hamiltonian/KKT system and determine whether the current MATLAB-faithful branch ordering is equivalent to it. No implementation is authorized.

### Candidate W — hybrid joint-wealth truncation

Analyze only as a candidate:

```text
D_W = {a>=0, b>=b_min, a<=a_max, a+b<=W_max}
W face: mu_W<=0
upper-a: mu_a<=0
intersection: mu_a<=0 AND mu_W<=0
```

`W=a+b` is accepted as a source-accounting coordinate, not yet as the production truncation variable. No numerical `W_max` is selected in DLH-5M.

Compare two representations without coding:

- W1: masked `(a,b)` tensor lattice;
- W2: transformed `(a,W)` coordinates with `b=W-a`.

### Geometry-consistency safeguard

The shortcut “retain a rectangular domain but use `mu_W<=0` only at the rectangular upper corner instead of `mu_b<=0`” must be explicitly tested. A rectangular tangent cone normally requires componentwise inwardness on each active face; a geometry-inconsistent PASS shortcut must be rejected.

### Required recommendation

Builder must recommend exactly one:

- `DLH_5M_RECTANGULAR_COMPONENTWISE_STATE_CONSTRAINT_KKT_RECOMMENDED__OWNER_SCIENTIFIC_DECISION_REQUIRED`
- `DLH_5M_HYBRID_JOINT_WEALTH_DOMAIN_AND_JOINT_KKT_RECOMMENDED__OWNER_SCIENTIFIC_DECISION_REQUIRED`
- `DLH_5M_DOMAIN_GEOMETRY_DESIGN_EVIDENCE_INSUFFICIENT__OWNER_SCIENTIFIC_DECISION_REQUIRED`
- `BLOCKED_DLH_5M_SOURCE_OR_ACCEPTED_EVIDENCE_INCONSISTENCY`

No recommendation freezes or changes the model. Owner decision is mandatory before implementation authority.

---

## 3. Decision tree after DLH-5M

### Route M-R — Owner accepts rectangular KKT design

Publish a separate scientific implementation task that replaces ad hoc upper-boundary branch handling with the accepted rectangular state-constraint/KKT formulation. Then validate boundary behavior and resolution robustness before stationary re-entry.

### Route M-W — Owner accepts hybrid joint-wealth design

First freeze the full domain specification and numerical representation, including how `W_max` is chosen as a computational truncation. Only then publish a separate implementation task. HJB and KFE must share the exact same controlled domain/process.

### Route M-U — evidence insufficient

Do not patch code. Perform the additional theoretical analysis explicitly identified by the Owner decision packet.

No route may bypass post-implementation HJB/KFE process validation.

---

## 4. Stationary household revalidation remains blocked

Stationary KFE remains NOT AUTHORIZED throughout DLH-5M.

Only after:

1. Owner accepts a state-domain/boundary-law design;
2. the design is implemented under separate scientific authority;
3. HJB boundary behavior and resolution robustness are validated;
4. the resulting generator is conservative and represents the same controlled process;

may the project re-enter Issue #27:

- recurrent-class/nullspace evidence;
- pin admissibility and valid-pin invariance;
- ORIGINAL `Q^T g` residual;
- mass/non-negativity;
- stationary-tail diagnostics;
- then recompute `C,L,A,B` and the two-region anchor from scratch.

No historical aggregate is grandfathered.

---

## 5. Regional / Deep Learning sequence remains deferred

Permanent hierarchy:

```text
2-region unit fixture
-> 3–5 province integration fixture
-> 31-province empirical/source benchmark
```

`31_PROVINCE_HOUSEHOLD_UPPER_DOMAIN_AUDIT` remains deferred. No neural training is authorized until household boundary/stationary validation is usable.

---

## 6. Scientific ceiling

During DLH-5M do not:

- mutate accepted HJB/KFE/regional source;
- mutate taper, transfer FOC, adjustment cost, economics or prices;
- choose or implement a production domain or numerical `W_max`;
- add/rerun grids or resolutions;
- implement any boundary KKT law;
- clip policy;
- run stationary KFE/density/tail/aggregates;
- run D1-D3, regional GE, multi-province audit, network training, nominal HANK, calibration, policy/welfare or Results.

---

## 7. Governance status

Issue #39 is the current intended Builder design-review task. Builder authority requires synchronized Task Index / Startup Snapshot plus authoritative activation comment.

Model-defining selection between candidate domain/boundary designs is reserved to Owner after reviewing the DLH-5M Owner decision packet.

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.
