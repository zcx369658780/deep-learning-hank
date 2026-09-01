# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.4  
**Date:** 2026-09-01  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** CURRENT OWNER-APPROVED SCIENTIFIC ROUTE  

---

## 0. Long-run objective

Build a data-to-structural-model calibration and regional-network HANK platform in which:

- household optimization, HJB/KFE, aggregation, firm/accounting blocks and later nominal-HANK equations remain explicit structural economics;
- difficult cross-regional mappings are the first objects eligible for learning;
- learned mappings remain inside transparent equilibrium/accounting constraints and must pass reproducibility, perturbation and out-of-sample validation.

The first learned object remains the regional labor/spatial rule. Capital-network learning and nominal-HANK integration remain later stages.

---

## 1. Accepted foundation through DLH-5F

### Household/HJB — Issue #23

Accepted MATLAB-faithful two-asset household/HJB source:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Accepted source identity:

- Git blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`
- SHA-256 `1795718C469FC3B427CAB8E3D5957C133BEAD6EACC9EF0A25A3EDB7211D1A024`

### Regional structural fixture — Issues #24–#25

Accepted two-region synchronous/Jacobi architecture with conditional household blocks, labor-flow accounting, destination aggregation, composite wage interface, regional firm block, fixed damping, deterministic trace semantics and region-order invariance.

The two-region fixture remains a permanent human-auditable unit fixture.

### Stationary-KFE scientific contract — Issues #26–#27

Accepted principles:

- singular `Q/Q^T` is expected for a stationary generator;
- accepted density must satisfy ORIGINAL `Q^T g=0`, mass normalization and non-negativity;
- stationary uniqueness, pin admissibility and pin invariance are distinct;
- conservative generator and recurrent-class/nullspace evidence are required;
- HJB and KFE must represent the same controlled process.

Binding law:

```text
HJB boundary policy <=> KFE boundary transition law
```

### D0 boundary blocker — Issue #28 / DLH-5E

Frozen D0:

```text
wbar = 1.0
r_a  = 0.03
```

Accepted HJB converges but requests material outward motion at both artificial upper asset boundaries. Mechanical KFE conservation alone does not repair the HJB/KFE process mismatch.

### Upper-domain diagnostic — Issue #29 / DLH-5F

Accepted candidate:

`7f4e489154115c9c91cf8c3fccbb3a1d114fbc3f`

Integrated to main:

`8eaac27472e3f902d0ff3e8044027f95913155ba`

Accepted verdict:

`DLH_5F_ISSUE_29_IMPLEMENTATION_ACCEPTED__OUTCOME_B_CONFIRMED__OUTCOME_D_SUPPORTED_WITH_INTERPRETATION_CORRECTION__STATIONARY_TAIL_NOT_REACHED`

Accepted interpretation:

1. Clean b-only `V0 -> V2`, with a20 `[0,10]`, `a_max=10`, taper and `db` fixed, reduces upper-b requested rate from about `0.353747704` to about `0.010203356`; shared-interior policy is highly stable. This is evidence of strong liquid-boundary attenuation with b-domain expansion, not growth with extent.
2. Cross-resolution requested rates must be separated from raw `mu_b` because generator rates scale by `1/db`; DLH-5F resolution evidence is not yet policy-converged.
3. a-extent experiments are confounded by the accepted MATLAB-faithful taper
   `r_a_eff(a)=r_a*(1-0.1*(a/a_max)^9)`; changing `a_max` changes effective returns at existing physical nodes.
4. V5 keeps `a_max=10` and removes upper-a outward requests, so the illiquid upper-boundary blocker is strongly resolution/local-discretization sensitive.
5. No variant passes the full HJB/KFE same-process boundary gate. Stationary-tail existence/non-existence and new `C,L,A,B` remain NOT REACHED.

---

## 2. Immediate scientific gate — DLH-5G / Issue #31

### Name

**Liquid Upper-Domain Asymptotic and Resolution Diagnostic under Fixed Illiquid Domain/Taper**

Task type:

`SCIENTIFIC_DIAGNOSTIC__LIQUID_UPPER_DOMAIN_ASYMPTOTIC_AND_RESOLUTION`

### Purpose

Isolate the clean liquid-domain question before any HJB or a-taper redesign:

> With the entire illiquid side fixed at `a in [0,10]`, `a_max=10`, baseline `da` and the accepted taper, does raw upper-b outward drift `max(mu_b,0)` attenuate toward zero as `b_max` is extended, and is that conclusion robust to independent b-resolution refinement?

### Frozen design

All variants preserve canonical D0 economics and exactly the same illiquid grid/taper.

Same-spacing extent sequence:

```text
G0: b20 [-2,5]
G1: b40 [-2,235/19]
G2: b60 [-2,375/19]
G3: b80 [-2,515/19]
```

with `db=7/19`.

Resolution pairs:

```text
G0 vs G4: baseline b-domain, coarse vs half db
G1 vs G5: first wide b-domain, coarse vs half db
```

No adaptive seventh grid.

### Required interpretation discipline

- raw `mu_b` is primary for cross-resolution asymptotic interpretation;
- requested rate `max(mu_b,0)/db` remains the boundary/generator compatibility measure;
- upper/lower a diagnostics are regression evidence only;
- DLH-5G does not execute stationary KFE, density, tail metrics or aggregates because the illiquid boundary remains unresolved.

---

## 3. Decision tree after DLH-5G

### Route B1 — liquid boundary attenuation reaches compatibility threshold

If a pre-frozen b extent reaches the requested-rate threshold with stable interior policy, freeze that as evidence for liquid-domain adequacy only. Do **not** resume stationary KFE until the illiquid boundary is separately resolved.

### Route B2 — clean attenuation continues but threshold is not reached

Do not blindly add adaptive grids. Review the pre-frozen trend and decide between one further bounded asymptotic experiment and analytical/high-wealth liquid-tail interpretation.

### Route B3 — liquid behavior is non-monotonic/persistent

Investigate high-liquid-wealth asymptotics / mean reversion / finite-domain HJB closure before any boundary-law rewrite.

### Route B4 — resolution instability dominates

Resolve liquid HJB discretization sensitivity before promoting a larger b-domain.

---

## 4. Separate illiquid-a route

The illiquid direction is intentionally deferred while DLH-5G runs.

Current facts:

- changing `a_max` also changes the accepted MATLAB-faithful effective return profile, so a-domain extent and return-profile effects are not separable under the current faithful taper;
- fixed-domain refinement can materially change upper-a policy.

Before any new a-domain adequacy claim, a separate scientific-design gate must decide whether the `a_max`-normalized taper is:

1. a MATLAB-parity numerical device retained only for source-faithful reproduction; or
2. part of the intended new DeepLearning-HANK household specification.

Any change to the taper/HJB controlled process is a scientific change and must be explicitly frozen before implementation.

---

## 5. Stationary household revalidation remains blocked

Do not compute or accept new household stationary `C,L,A,B` until both liquid and illiquid boundary treatments are coherent under the same HJB/KFE process.

When boundary coherence is restored, re-enter the Issue #27 stationary contract:

1. conservative generator;
2. recurrent-class/nullspace evidence;
3. pin admissibility and valid-pin invariance;
4. ORIGINAL `Q^T g` residual;
5. mass/non-negativity;
6. then `C,L,A,B` and anchor revalidation.

---

## 6. Regional scale hierarchy

Retain permanently:

```text
2-region unit fixture
-> 3–5 province integration fixture
-> 31-province empirical/source benchmark
```

The planned `31_PROVINCE_HOUSEHOLD_UPPER_DOMAIN_AUDIT` remains deferred until the household boundary/stationary foundation is scientifically usable. When eventually run, prefer frozen household price/input snapshots over repeated full 31-province GE grid sweeps.

Future regional parity must separately inspect continuous-state parity and discrete controller/threshold branch parity.

---

## 7. Deep Learning route

No neural training is authorized while the household stationary foundation is unresolved.

Later sequence remains:

1. `L0` — source spatial-rule surrogate;
2. `L1` — constrained structural learned spatial rule;
3. `L2` — empirical OD-flow learning with endogeneity/double-counting safeguards;
4. later capital-network learning;
5. separate nominal-HANK integration after a minimal nominal block is scientifically frozen.

---

## 8. Current sequencing

Immediate:

1. preserve Issues #23–#29 accepted evidence;
2. execute Issue #31 / DLH-5G exactly as published and activated;
3. review liquid extent/resolution evidence;
4. then decide the next liquid route and the separate illiquid-taper scientific-design route.

After household boundary resolution:

1. stationary KFE / `C,L,A,B` revalidation;
2. `K=M*A` and two-region anchor revalidation;
3. two-region S0/S1 + order invariance;
4. 3–5 province integration fixture;
5. 31-province frozen-price household/source benchmark;
6. only then resume learned spatial-module work.

---

## 9. Scientific ceiling

Until household boundary/stationary evidence is resolved, do not:

- change accepted HJB/taper merely to obtain a PASS;
- accept a clipped KFE density from a different controlled process;
- restore historical row-295 aggregates;
- run validated policy/welfare Results;
- train learned regional networks;
- scale to production 31-region learned equilibrium;
- enter nominal-HANK integration;
- claim the neighboring multi-province reconstruction is already unquestioned full stationary-parity production authority.

---

## 10. Governance status

Issue #31 is the intended next Builder task. Builder authority requires synchronized Task Index / Startup Snapshot plus an authoritative activation comment.

Routine scientific route decisions are delegated by Owner to ChatGPT unless Owner intervenes or raises a new concern.

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.
