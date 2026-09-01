# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.5  
**Date:** 2026-09-01  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** CURRENT OWNER-APPROVED SCIENTIFIC ROUTE

---

## 0. Long-run objective

Build a data-to-structural-model calibration and regional-network HANK platform in which household HJB/KFE, aggregation, firm/accounting blocks and later nominal-HANK equations remain explicit structural economics, while difficult cross-regional mappings become interpretable learned modules only after the underlying household and equilibrium processes pass numerical and scientific validation.

The first learned object remains the regional labor/spatial rule. Capital-network learning and nominal-HANK integration remain later stages.

---

## 1. Accepted foundation through DLH-5G

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

DLH-5E established material outward requests at both artificial upper asset bounds on the canonical D0 household. DLH-5F established that:

- b-only domain expansion strongly attenuates the liquid boundary;
- a-domain widening is confounded by the accepted `a_max`-normalized illiquid-return taper;
- fixed-domain refinement materially changes the illiquid upper-boundary policy;
- no full same-process stationary validation had yet been reached.

### Liquid upper-domain diagnostic — Issue #31 / DLH-5G

Accepted candidate:

`edbd6e9d4683118e08edb8041609c9af1579883a`

Integrated to main:

`809d18a3459b5b8c4d8b142ea4f282a34c3af49f`

Accepted verdict:

`DLH_5G_ISSUE_31_IMPLEMENTATION_ACCEPTED__LIQUID_UPPER_DOMAIN_ADEQUACY_EVIDENCE_CONFIRMED__B_RESOLUTION_SENSITIVITY_RETAINED__ILLIQUID_BOUNDARY_REMAINS_BLOCKER`

Accepted scientific interpretation:

1. Holding the complete illiquid side fixed, the same-spacing b sequence gives upper-b raw/requested maxima
   `0.1303281015/0.3537477040 -> 0.003759131181/0.01020335606 -> 0/0 -> 0/0`.
2. Exact zero is reached at `b_max=19.7368421053` and remains zero at a wider same-spacing domain.
3. Finer b-resolution reaches zero already at `b_max=12.3684210526`; therefore liquid-domain adequacy is supported, but resolution sensitivity remains material and no final production grid is frozen.
4. `b60 [-2,375/19]`, `db=7/19` is designated a **provisional liquid-safe diagnostic domain** for isolating the remaining illiquid problem.
5. On that liquid-safe state, upper-a remains material: requested max about `0.3094730854`, 108 material states / 90% of the upper-a boundary.
6. Stationary KFE remains NOT AUTHORIZED.

---

## 2. Immediate scientific gate — DLH-5H / Issue #34

### Name

**Illiquid Upper-Boundary Resolution Diagnostic on the Provisional Liquid-Safe Domain**

Task type:

`SCIENTIFIC_DIAGNOSTIC__ILLIQUID_UPPER_BOUNDARY_RESOLUTION`

### Purpose

Resolve the remaining clean question before any taper or HJB boundary-law redesign:

> With physical illiquid domain `[0,10]`, `a_max=10`, the accepted taper, D0 economics and a liquid-safe b domain held fixed, does upper-a raw outward drift attenuate to the compatibility threshold as only a-grid resolution is refined?

### Frozen design

Core liquid domain:

```text
b60 [-2,375/19]
db=7/19
```

Physical illiquid domain and taper remain:

```text
a in [0,10]
a_max=10
r_a_eff(a)=r_a*(1-0.1*(a/a_max)^9)
```

Primary a-resolution sequence:

```text
H0: a20
H1: a39
H2: a77
H3: a153
```

Independent b-resolution cross-checks:

```text
H4: b119 / a39
H5: b119 / a77
```

No adaptive seventh grid, no domain widening and no PASS-seeking search.

DLH-5H remains policy-only: no stationary KFE, density, tail metrics or aggregates.

---

## 3. Decision tree after DLH-5H

### Route H1 — joint upper-boundary HJB policy compatibility reached

If at least one pre-frozen candidate has both upper-b and upper-a requested outward rates `<=1e-10`, review policy/interior stability and then publish a separate stationary-KFE re-entry gate under the Issue #27 contract.

The candidate grid is not automatically a final production grid; stationary uniqueness/residual/mass/non-negativity and aggregate stability must still be established.

### Route H2 — upper-a cleanly attenuates but threshold not reached

Do not add adaptive grids. Review the pre-frozen trend and decide whether one further bounded resolution/asymptotic diagnostic is justified.

### Route H3 — upper-a remains persistent / plateau / non-monotonic

Escalate to a separate scientific-design gate for the illiquid upper-boundary/taper interpretation. Do not silently modify the `a_max`-normalized taper or HJB boundary law.

### Route H4 — liquid boundary reactivates under a refinement

Treat this as a coupled numerical-resolution blocker. Revisit the provisional liquid-safe grid choice before any stationary re-entry.

---

## 4. Stationary household revalidation

Stationary validation remains blocked until a candidate grid satisfies coherent HJB upper-boundary policy in both asset dimensions.

When that prerequisite is met, re-enter Issue #27:

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

Issue #34 is the current intended Builder task. Builder authority requires synchronized Task Index / Startup Snapshot plus an authoritative activation comment.

Routine bounded scientific-route decisions are delegated by Owner to ChatGPT unless Owner intervenes or raises a new concern.

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.
