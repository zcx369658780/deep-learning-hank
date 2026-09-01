# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.6  
**Date:** 2026-09-01  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** CURRENT OWNER-APPROVED SCIENTIFIC ROUTE

---

## 0. Long-run objective

Build a data-to-structural-model calibration and regional-network HANK platform in which household HJB/KFE, aggregation, firm/accounting blocks and later nominal-HANK equations remain explicit structural economics, while difficult cross-regional mappings become interpretable learned modules only after the underlying household and equilibrium processes pass numerical and scientific validation.

The first learned object remains the regional labor/spatial rule. Capital-network learning and nominal-HANK integration remain later stages.

---

## 1. Accepted foundation through DLH-5H

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

Key result: with coarse a20 fixed, upper-b requested policy reaches exact zero by `b_max=19.7368421053` and remains zero at a wider same-spacing extent. However, b-resolution sensitivity remains material and no production grid is frozen.

### Illiquid-resolution diagnostic — Issue #34 / DLH-5H

Accepted candidate:

`906c98d107c8dadf6e24d841901d7eb6d53fe0d9`

Integrated to main:

`f648ca270a751465ac041a4eee05cee094114ed6`

Accepted verdict:

`DLH_5H_ISSUE_34_IMPLEMENTATION_ACCEPTED__ILLIQUID_A_RESOLUTION_ADEQUACY_CONFIRMED__LIQUID_BOUNDARY_REACTIVATION_CONFIRMED__COUPLED_RESOLUTION_BLOCKER_ESTABLISHED`

Accepted scientific interpretation:

1. With physical `a in [0,10]`, `a_max=10`, taper and D0 economics fixed, upper-a requested outward policy is material on a20 but becomes exact zero on a39 and remains zero on a77/a153.
2. Therefore the illiquid upper-boundary problem is strongly resolution-driven on the fixed physical domain; no taper/HJB rewrite is currently justified by the evidence.
3. The b60 domain previously considered liquid-safe under a20 is **not robust to a refinement**. Upper-b requested policy reactivates to about `0.2713`, `0.3916`, `0.4449` on a39/a77/a153.
4. Half-db b cross-checks at the same extent remain material, confirming that the remaining blocker is a coupled domain-resolution problem.
5. a-resolution aligned policy differences decline across a39/a77/a153, but transfer/mu differences remain material; a77 and a153 are mature diagnostic resolutions, not final production resolutions.
6. No pre-frozen grid reaches joint HJB upper-boundary policy compatibility. Stationary KFE remains NOT AUTHORIZED.

---

## 2. Immediate scientific gate — DLH-5I / Issue #35

### Name

**Coupled Liquid-Extent Frontier Across Mature Illiquid Resolutions**

Task type:

`SCIENTIFIC_DIAGNOSTIC__COUPLED_BOUNDARY_DOMAIN_RESOLUTION_FRONTIER`

### Purpose

Treat the remaining numerical boundary problem jointly rather than sequentially:

> With the physical illiquid domain, `a_max`, taper, economics and accepted HJB frozen, how far must the liquid upper domain be extended at a77 and a153 before joint upper-boundary policy compatibility is reached, and is that result robust across both mature a resolutions?

### Frozen design

Economics and household law remain:

```text
wbar = 1.0
r_a  = 0.03
a in [0,10]
a_max = 10
r_a_eff(a)=r_a*(1-0.1*(a/a_max)^9)
```

Mature diagnostic a resolutions:

```text
a77
a153
```

Liquid spacing remains:

```text
db=7/19
```

Pre-frozen b extents:

```text
b60  [-2,375/19]
b80  [-2,515/19]
b100 [-2,655/19]
```

Exact six variants are the Cartesian 2×3 set of `{a77,a153}` × `{b60,b80,b100}`.

No adaptive seventh grid, no new a resolution and no b-resolution change are allowed in DLH-5I.

DLH-5I remains policy-only: no stationary KFE, density, tail metrics or aggregates.

---

## 3. Decision tree after DLH-5I

### Route I1 — a common b extent is jointly compatible at both a77 and a153

Freeze the **smallest common compatible b extent as a provisional coupled-domain candidate only**. Then run a separate bounded b-resolution confirmation at that extent before any stationary-KFE re-entry.

### Route I2 — only one a resolution reaches joint compatibility

Do not promote the domain. Treat this as lack of resolution robustness and continue bounded numerical-convergence review.

### Route I3 — both a-resolution extent sequences attenuate but common threshold is not reached

Do not adaptively add grids inside the task. Review the frozen trend and decide whether one further bounded extent gate is justified.

### Route I4 — coupled behavior is persistent or non-monotonic

Escalate to analytical/high-wealth or finite-domain HJB-closure review before any taper/boundary-law rewrite.

---

## 4. Stationary household revalidation remains blocked

Stationary validation remains blocked until:

1. a candidate grid is jointly HJB upper-boundary compatible in both assets;
2. that compatibility is robust to the required resolution confirmation.

Only after those prerequisites may the project re-enter Issue #27:

1. conservative generator;
2. recurrent-class/nullspace evidence;
3. pin admissibility and valid-pin invariance;
4. ORIGINAL `Q^T g` residual;
5. mass/non-negativity;
6. tail diagnostics;
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
- accept a KFE density from a different controlled process;
- restore historical aggregates;
- run validated policy/welfare Results;
- train regional networks;
- scale to production 31-region learned equilibrium;
- enter nominal-HANK integration.

---

## 7. Governance status

Issue #35 is the current intended Builder task. Builder authority requires synchronized Task Index / Startup Snapshot plus an authoritative activation comment.

Routine bounded scientific-route decisions are delegated by Owner to ChatGPT unless Owner intervenes or raises a new concern.

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.
