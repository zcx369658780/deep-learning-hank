# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.7  
**Date:** 2026-09-01  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** CURRENT OWNER-APPROVED SCIENTIFIC ROUTE

---

## 0. Long-run objective

Build a data-to-structural-model calibration and regional-network HANK platform in which household HJB/KFE, aggregation, firm/accounting blocks and later nominal-HANK equations remain explicit structural economics, while difficult cross-regional mappings become interpretable learned modules only after the underlying household and equilibrium processes pass numerical and scientific validation.

The first learned object remains the regional labor/spatial rule. Capital-network learning and nominal-HANK integration remain later stages.

---

## 1. Accepted foundation through DLH-5I

### Household/HJB — Issue #23

Accepted MATLAB-faithful two-asset household/HJB source:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Accepted source identity:

- Git blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`
- SHA-256 `1795718C469FC3B427CAB8E3D5957C133BEAD6EACC9EF0A25A3EDB7211D1A024`

### Regional structural fixture — Issues #24–#25

Accepted two-region synchronous/Jacobi architecture remains the permanent human-auditable regional unit fixture.

### Stationary-KFE scientific contract — Issues #26–#27

Accepted density must satisfy the ORIGINAL stationary equation, mass and non-negativity, with conservative-generator, recurrent-class/nullspace and pin-admissibility evidence.

Binding law:

```text
HJB boundary policy <=> KFE boundary transition law
```

### D0 boundary diagnosis — Issues #28–#29

DLH-5E established material outward requests at both artificial upper asset bounds. DLH-5F showed that b-only extent strongly attenuates liquid-boundary influence, that a-domain widening is confounded by the accepted `a_max`-normalized taper, and that fixed-domain resolution materially changes the illiquid policy.

### Liquid upper-domain diagnostic — Issue #31 / DLH-5G

Accepted candidate:

`edbd6e9d4683118e08edb8041609c9af1579883a`

Integrated to main:

`809d18a3459b5b8c4d8b142ea4f282a34c3af49f`

Accepted verdict:

`DLH_5G_ISSUE_31_IMPLEMENTATION_ACCEPTED__LIQUID_UPPER_DOMAIN_ADEQUACY_EVIDENCE_CONFIRMED__B_RESOLUTION_SENSITIVITY_RETAINED__ILLIQUID_BOUNDARY_REMAINS_BLOCKER`

Key result: with coarse a20 fixed, upper-b requested policy reaches exact zero by `b_max=19.7368421053`, but that domain is not robust to later illiquid-grid refinement.

### Illiquid-resolution diagnostic — Issue #34 / DLH-5H

Accepted candidate:

`906c98d107c8dadf6e24d841901d7eb6d53fe0d9`

Integrated to main:

`f648ca270a751465ac041a4eee05cee094114ed6`

Accepted verdict:

`DLH_5H_ISSUE_34_IMPLEMENTATION_ACCEPTED__ILLIQUID_A_RESOLUTION_ADEQUACY_CONFIRMED__LIQUID_BOUNDARY_REACTIVATION_CONFIRMED__COUPLED_RESOLUTION_BLOCKER_ESTABLISHED`

Accepted interpretation:

- upper-a is material on a20 but exact zero on a39/a77/a153 when physical `a in [0,10]`, `a_max=10` and taper are fixed;
- the former b60 liquid-safe domain is not robust to a refinement because upper-b reactivates;
- the remaining issue is therefore coupled domain/resolution behavior.

### Coupled liquid-extent frontier — Issue #35 / DLH-5I

Accepted candidate:

`d8837e04db940b1f71b8ff1fe7e181d1bf9644a3`

Integrated to main:

`53d0ff7b0fe9bd73cfbd8c6d27c98bbc4b0423d1`

Accepted verdict:

`DLH_5I_ISSUE_35_IMPLEMENTATION_ACCEPTED__COUPLED_B_EXTENT_ATTENUATION_CONFIRMED__COMMON_THRESHOLD_NOT_REACHED__UPPER_A_COMPATIBILITY_STABLE__FURTHER_BOUNDED_EXTENT_GATE_REQUIRED`

Accepted scientific interpretation:

1. At both mature a resolutions a77/a153, upper-a/lower-a/lower-b requested policy is exact zero through b60/b80/b100.
2. With `db=7/19`, upper-b requested policy strictly attenuates with liquid extent:
   - a77: `0.3915648627 -> 0.2808185297 -> 0.1925385153`;
   - a153: `0.4449370735 -> 0.3356027946 -> 0.2481811687`.
3. Offending upper-b states remain localized to the top-liquid/top-illiquid/high-productivity corner and decline in count/share with extent.
4. No b60/b80/b100 extent reaches the `1e-10` joint compatibility threshold at either mature a resolution.
5. Cross-a value/consumption/labor differences are small, while transfer/`mu_a`/`mu_b` remain about 1.9–2.4% apart.
6. The evidence supports continued finite-b-domain attenuation, not a claim of non-existent stationary liquid tails.
7. Stationary KFE remains NOT AUTHORIZED.

---

## 2. Immediate scientific gate — DLH-5J / Issue #36

### Name

**Final Bounded Coupled Liquid-Extent Continuation Before Asymptotic Adjudication**

Task type:

`SCIENTIFIC_DIAGNOSTIC__FINAL_BOUNDED_COUPLED_B_EXTENT_CONTINUATION`

### Purpose

DLH-5I still leaves b100 materially outward at both mature a resolutions, but the attenuation trend is clean. DLH-5J is therefore the **last pre-frozen larger-b grid experiment** before the project must switch to high-wealth/asymptotic or finite-domain-closure analysis if compatibility is still not reached.

Scientific question:

> With the accepted household process, mature a resolutions and `db=7/19` frozen, does one of b120/b140/b160 reach joint upper-boundary compatibility at both a77 and a153? If not, does clean attenuation persist through the final bounded frontier?

### Frozen design

```text
wbar = 1.0
r_a  = 0.03
a in [0,10]
a_max = 10
accepted taper = r_a*(1-0.1*(a/a_max)^9)
a resolutions = {a77,a153}
db = 7/19
```

Final extents:

```text
b120 [-2,795/19]
b140 [-2,935/19]
b160 [-2,1075/19]
```

Exact six variants are `{a77,a153} × {b120,b140,b160}`.

Accepted DLH-5I b100 results are read-only scalar anchors for the continuation trend; b100 is not rerun as a seventh/eighth variant.

No b extent beyond b160 is authorized.

DLH-5J remains policy-only: no stationary KFE, density, tail metrics or aggregates.

---

## 3. Decision tree after DLH-5J

### Route J1 — a common final extent reaches joint compatibility at both a77 and a153

Freeze the **smallest common compatible extent as a provisional coupled-domain candidate only**.

Then publish exactly one bounded **b-resolution confirmation gate** at that same physical extent. Stationary KFE remains blocked until that confirmation passes.

### Route J2 — only one mature a resolution reaches compatibility

Do not promote the domain. Treat this as unresolved cross-a resolution robustness and move to scientific numerical/asymptotic review rather than adaptive extent search.

### Route J3 — clean attenuation persists through b160 but no common threshold is reached

**Stop larger-grid continuation.** Do not publish b180/b200 or root-seeking adaptive extent tasks.

The next scientific gate must adjudicate high-wealth liquid drift / economic mean reversion / finite-domain HJB closure analytically or semi-analytically under the accepted household process.

### Route J4 — behavior becomes persistent, plateaued or non-monotonic

Also escalate immediately to high-wealth/asymptotic or finite-domain HJB-closure adjudication.

No HJB or taper rewrite may occur without a later explicit scientific-design gate.

---

## 4. Stationary household revalidation remains blocked

Stationary validation requires BOTH:

1. joint HJB upper-boundary compatibility in both assets on a candidate grid;
2. b-resolution confirmation of that compatibility at the same physical extent.

Only then may the project re-enter Issue #27:

1. conservative generator;
2. recurrent-class/nullspace evidence;
3. pin admissibility and valid-pin invariance;
4. ORIGINAL `Q^T g` residual;
5. mass/non-negativity;
6. stationary tail diagnostics;
7. then recompute `C,L,A,B` and the two-region anchor from scratch.

No historical row-295 aggregate is grandfathered.

---

## 5. Regional and Deep Learning sequence

Permanent hierarchy:

```text
2-region unit fixture
-> 3–5 province integration fixture
-> 31-province empirical/source benchmark
```

The planned `31_PROVINCE_HOUSEHOLD_UPPER_DOMAIN_AUDIT` remains deferred until household boundary/stationary validation is usable.

No neural training is currently authorized. Later sequence remains:

1. `L0` source spatial-rule surrogate;
2. `L1` constrained structural learned spatial rule;
3. `L2` empirical OD-flow learning with endogeneity/double-counting safeguards;
4. later capital-network learning;
5. separate nominal-HANK integration after its structural block is frozen.

---

## 6. Scientific ceiling

Until household boundary/stationary evidence is resolved, do not:

- modify accepted HJB/taper merely to obtain PASS;
- keep enlarging b adaptively beyond the DLH-5J b160 ceiling;
- accept a KFE density from a different controlled process;
- restore historical aggregates;
- run validated policy/welfare Results;
- train regional networks;
- scale to production 31-region learned equilibrium;
- enter nominal-HANK integration.

---

## 7. Governance status

Issue #36 is the current intended Builder task. Builder authority requires synchronized Task Index / Startup Snapshot plus an authoritative activation comment.

Routine bounded scientific-route decisions are delegated by Owner to ChatGPT unless Owner intervenes or raises a new concern.

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.
