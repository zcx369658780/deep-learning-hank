# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.9  
**Date:** 2026-09-01  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** CURRENT OWNER-APPROVED SCIENTIFIC ROUTE

---

## 0. Long-run objective

Build a data-to-structural-model calibration and regional-network HANK platform in which household HJB/KFE, aggregation, firm/accounting blocks and later nominal-HANK equations remain explicit structural economics, while difficult cross-regional mappings become interpretable learned modules only after household and equilibrium foundations pass scientific and numerical validation.

The first learned object remains the regional labor/spatial rule. Capital-network learning and nominal-HANK integration remain later stages.

---

## 1. Accepted household foundation through DLH-5K

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

### Boundary/domain sequence — Issues #28–#36

Accepted findings:

- canonical D0 HJB converges but artificial upper asset bounds initially receive outward requests;
- b-only extent strongly attenuates liquid-boundary influence;
- widening `a_max` is confounded by the accepted normalized illiquid-return taper;
- refining the fixed physical a domain resolves upper-a but reactivates upper-b, establishing a coupled domain-resolution problem;
- at mature a77/a153, upper-b attenuates monotonically with b extent;
- a77 reaches joint compatibility at b160, while a153 remains outward at b160;
- no cross-a jointly compatible extent exists through the hard b160 ceiling;
- the pure larger-b-grid route is CLOSED: no b180/b200/adaptive/root-seeking PASS search.

Stationary KFE remains NOT AUTHORIZED.

### High-wealth / upper-corner mechanism adjudication — Issue #37 / DLH-5K

Accepted candidate:

`aaead4a1368ec061ac1e380c3af33d93c0f31161`

Integrated to main:

`d26b2b8c8d69d2afa2cb9806f120d03ebe973752`

Accepted verdict:

`DLH_5K_ISSUE_37_IMPLEMENTATION_ACCEPTED__MIXED_LOCALIZATION_CONFIRMED__TRANSFER_DERIVATIVE_CHANNEL_DOMINATES_CROSS_A_DIVERGENCE__INTERPRETATION_NARROWED__NEXT_GATE_REQUIRED`

Accepted scientific interpretation:

1. 5/17 material upper-b offenders are boundary-only within the required `n-1/n-2/n-3/n-5` window; 12/17 retain positive full-policy `mu_b` in at least one inspected interior layer.
2. The evidence establishes **local** liquid-drift persistence only. It does not establish an infinite-domain high-wealth asymptotic failure.
3. At material offenders, `base_liquid_surplus<0` while `transfer_injection>0`; positive `mu_b` occurs when transfer injection dominates the negative base surplus.
4. a77/a153 divergence is primarily transfer/derivative-channel driven.
5. The accepted selected transfer candidate fails joint inwardness at inspected offender states, but the algebra admits much larger transfer-flow roots; no mathematical no-feasible-transfer theorem is accepted.
6. Transfer `d` is a continuous-time flow/rate, not an asset stock; no liquidation interpretation is accepted.
7. No source defect, HJB redesign, domain redesign or stationary re-entry is authorized by DLH-5K.

---

## 2. Immediate scientific gate — DLH-5L / Issue #38

### Name

**Componentwise Liquid Drift vs Total-Wealth Mean Reversion and Boundary Geometry**

Task type:

`SCIENTIFIC_ANALYTICAL_DIAGNOSTIC__TOTAL_WEALTH_DRIFT_AND_DOMAIN_GEOMETRY`

### Purpose

The accepted household law transfers wealth one-for-one between the two asset coordinates, apart from adjustment cost:

```text
mu_a = r_a_eff(a)*a + d
mu_b = r_b*b + labor_income - d - adjustment_cost
       - (consumption - transfer_income)
```

Therefore:

```text
mu_W = mu_a + mu_b
     = r_a_eff(a)*a + r_b*b + labor_income
       - adjustment_cost - (consumption - transfer_income)
```

The linear transfer `d` cancels from total-wealth drift.

Scientific question:

> When the accepted policy gives positive liquid-coordinate `mu_b` in the high-a/high-b region, does total wealth `W=a+b` nevertheless drift inward because illiquid wealth is falling? If so, the unresolved issue may be componentwise rectangular-domain geometry / portfolio reallocation rather than total-wealth mean-reversion failure. If total wealth is also outward, genuine high-wealth economic asymptotics remain unresolved.

### Frozen numerical evidence set

Rerun exactly accepted J0–J5 only; no new grid, extent or resolution.

The inspected state set is the exact union of coordinates already present in accepted DLH-5K:

- `DLH_5K_BOUNDARY_INTERIOR_LOCALIZATION.csv`
- `DLH_5K_CROSS_A_MECHANISM.csv`

No post-hoc state additions.

### Required evidence

- exact J reproduction and accepted source identity;
- exact `mu_W=mu_a+mu_b` reconstruction and transfer cancellation;
- pre-registered four-way component-liquid / total-wealth classification;
- explicit total-wealth sign for every DLH-5K interior-positive state;
- analytical comparison of rectangular component constraints with local `W=a+b` normal drift;
- exact a77/a153 total-wealth comparison;
- deterministic repeat and applicable full regression suite.

DLH-5L is source-preserving. It does not authorize replacing the production domain with a total-wealth contour.

---

## 3. Decision tree after DLH-5L

### Route L1 — liquid outward, total wealth inward on all accepted positive states

If every inherited material positive-`mu_b` state, including every DLH-5K interior-positive state, has `mu_W<=0`:

- accept only a **pre-frozen-state total-wealth mean-reversion result**, not an infinite-domain theorem;
- next gate = scientific design freeze comparing rectangular componentwise state constraints with economically justified joint-domain / joint-KKT alternatives;
- no implementation patch before design acceptance.

### Route L2 — total wealth outward in accepted high-wealth interior

If material total-wealth outwardness occurs in inherited interior-positive states:

- do not resume larger-grid PASS seeking;
- next gate = genuine high-wealth total-wealth asymptotics / economic mean-reversion analysis under the accepted model.

### Route L3 — mixed total-wealth behavior

Resolve both the portfolio-reallocation/domain-geometry channel and genuine total-wealth outward channel before any boundary redesign or stationary re-entry.

No DLH-5L terminal automatically authorizes source/domain mutation.

---

## 4. Stationary household revalidation remains blocked

Stationary KFE remains NOT AUTHORIZED throughout DLH-5L.

Only after a scientifically coherent controlled process and boundary/domain design has been accepted and numerically validated may the project re-enter Issue #27:

1. conservative generator;
2. recurrent-class/nullspace evidence;
3. pin admissibility and valid-pin invariance;
4. ORIGINAL `Q^T g` residual;
5. mass/non-negativity;
6. stationary tail diagnostics;
7. recompute `C,L,A,B` and the two-region anchor from scratch.

No historical aggregate is grandfathered.

---

## 5. Regional and Deep Learning sequence

Permanent hierarchy:

```text
2-region unit fixture
-> 3–5 province integration fixture
-> 31-province empirical/source benchmark
```

`31_PROVINCE_HOUSEHOLD_UPPER_DOMAIN_AUDIT` remains deferred until household boundary/stationary validation is usable.

No neural training is currently authorized. Later sequence remains:

1. `L0` source spatial-rule surrogate;
2. `L1` constrained structural learned spatial rule;
3. `L2` empirical OD-flow learning with endogeneity/double-counting safeguards;
4. later capital-network learning;
5. separate nominal-HANK integration after its structural block is frozen.

---

## 6. Scientific ceiling

Until DLH-5L is adjudicated, do not:

- enlarge b beyond b160 or add adaptive/root-seeking grids;
- add any new a/b resolution;
- modify accepted HJB/KFE source, taper, transfer FOC, adjustment cost or boundary law;
- replace the rectangular production domain from an analytical geometry diagnostic alone;
- accept a KFE density from a different controlled process;
- run stationary aggregates or policy/welfare Results;
- train regional networks;
- scale to production 31-region learned equilibrium;
- enter nominal-HANK integration.

---

## 7. Governance status

Issue #38 is the current intended Builder task. Builder authority requires synchronized Task Index / Startup Snapshot plus an authoritative activation comment.

Routine bounded scientific-route decisions are delegated by Owner to ChatGPT unless Owner intervenes or raises a new concern.

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.
