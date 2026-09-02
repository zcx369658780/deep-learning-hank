# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.11  
**Date:** 2026-09-02  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** CURRENT OWNER-APPROVED SCIENTIFIC ROUTE

---

## 0. Long-run objective

Build a data-to-structural-model calibration and regional-network HANK platform in which household HJB/KFE, aggregation, firm/accounting blocks and later nominal-HANK equations remain explicit structural economics, while difficult cross-regional mappings become interpretable learned modules only after household and equilibrium foundations pass scientific and numerical validation.

The first learned object remains the regional labor/spatial rule. Capital-network learning and nominal-HANK integration remain later stages.

---

## 1. Accepted household foundation through DLH-5M

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
- pure larger-b-grid PASS seeking is CLOSED.

### High-wealth mechanism — Issues #37–#38

Accepted evidence establishes, narrowly:

- positive high-wealth `mu_b` is largely a transfer/rebalancing phenomenon;
- the pre-frozen accepted high-wealth evidence set contains 105 states;
- all 44 material positive-`mu_b` states satisfy `mu_W=mu_a+mu_b<=0`;
- all 17 top-layer upper-b offenders satisfy `mu_a<=0` and `mu_W<=0` while violating rectangular `mu_b<=0`;
- the linear transfer term cancels one-for-one in `mu_W`, while adjustment cost remains;
- cross-a absolute total-drift differences shrink materially, but relative `mu_W` differences remain above the existing 1e-2 diagnostic threshold on 16/24 aligned pairs;
- this is finite-state/source-accounting evidence, not an infinite-domain theorem or stationary-tail proof.

### State-domain/KKT design review — Issue #39 / DLH-5M

Accepted candidate:

`80cdb7ab2c14bcb7606fc66a0737c28bd3fbb4bb`

Acceptance integration commit:

`69bde2115cdf038e40640ec41d23e0b620167539`

Accepted reviewer verdict:

`DLH_5M_REVISED_CANDIDATE_ACCEPTED__CORE_KKT_AND_W_ACTIVITY_BLOCKERS_RESOLVED__RECOMMENDATION_U_SUPPORTED__OWNER_SCIENTIFIC_DECISION_REQUIRED`

Owner scientific decision:

`ACCEPT_RECOMMENDATION_U__DO_NOT_FREEZE_R_OR_W_YET`

Controlling accepted interpretation:

1. **Design R remains unfrozen.** A rectangular tangent-cone/KKT formulation is mathematically coherent on a finite rectangle, but the upper-b face is a computational truncation and no accepted evidence shows that this numerical closure has vanishing influence as the truncation recedes.
2. **Design W remains unfrozen.** `W=a+b` is an accepted source-accounting coordinate and is more coherent with the finite-state portfolio-reallocation evidence, but finite-state inwardness, undefined `W_max`, cross-a sensitivity, representation choice and HJB↔KFE process matching are insufficient for a production-domain freeze.
3. Maximization upper-constraint KKT convention is `L=H-lambda*g`; effective gradients are `V-lambda`.
4. At a W face, `lambda_W` cancels from the linear transfer contribution but survives through adjustment cost.
5. W-face activity for any accepted finite state is conditional on symbolic `W_max`; no state is declared W-interior or W-boundary without a chosen cap.
6. The geometry-inconsistent shortcut “rectangle but use `mu_W<=0` instead of `mu_b<=0` at the corner” is rejected.
7. Stationary KFE remains NOT AUTHORIZED.

---

## 2. Immediate theory gate — DLH-5N / Issue #40

### Name

**High-Wealth Total-Drift Asymptotics and Domain Viability**

Task type:

`SCIENTIFIC_THEORY_ANALYSIS__HIGH_WEALTH_TOTAL_DRIFT_ASYMPTOTICS_AND_DOMAIN_VIABILITY`

### Purpose

Owner accepted Recommendation U. The next step is not a boundary implementation and not a new grid search. It is a theory-only analysis of whether the accepted household economics themselves imply total-wealth mean reversion in the high-liquid-wealth tail.

The exact asymptotic path is deliberately narrow:

```text
0 <= a <= a_max=10       current accepted finite illiquid support
b -> +infinity
W=a+b -> +infinity
accepted a_max-normalized taper held fixed
```

The controlling total-drift identity is:

```text
mu_W = r_a_eff(a)*a + r_b*b + labor_income - chi(d,a) - consumption
```

The key scientific question is whether accepted authority alone determines the sign of `mu_W` for sufficiently large `b`, or whether the result depends on unestablished asymptotic behavior of `V_b`, consumption, labor, `V_a/V_b`, transfer and adjustment cost.

### Required logic

DLH-5N must:

1. audit exact accepted source objects and frozen D0 inputs relevant to the tail;
2. classify the asymptotic order/sign status of every term in `mu_W`;
3. distinguish source formulas from theorems about endogenous value derivatives/controls;
4. derive the strongest theorem, conditional theorem, counterexample or unresolved condition supported by current authority;
5. use accepted DLH-5L finite-state evidence only as a consistency check, not as proof of a tail theorem;
6. translate the result into narrow R/W domain-viability implications without choosing a domain.

### Critical scope distinction

A result for `b->infinity` with `a in [0,10]` is **not** a full two-asset infinite-domain result. DLH-5N must not extrapolate the accepted taper beyond `a_max=10` or make claims about `a->infinity`.

### Exact terminals

Use exactly one:

- `DLH_5N_FIXED_A_LIQUID_TAIL_TOTAL_WEALTH_INWARDNESS_ESTABLISHED__DOMAIN_DESIGN_REVIEW_MAY_RESUME`
- `DLH_5N_FIXED_A_LIQUID_TAIL_TOTAL_WEALTH_SIGN_CONDITIONAL__MISSING_CONTROL_ASYMPTOTICS_IDENTIFIED`
- `DLH_5N_FIXED_A_LIQUID_TAIL_TOTAL_WEALTH_NONINWARD_COUNTEREXAMPLE_ESTABLISHED__W_DIRECTION_WEAKENED`
- `BLOCKED_DLH_5N_ACCEPTED_SOURCE_OR_ASYMPTOTIC_OBJECT_INCONSISTENCY`

No terminal freezes R/W or authorizes implementation.

---

## 3. Decision tree after DLH-5N

### Route N-A — unconditional fixed-a liquid-tail inwardness established

Do not immediately implement W. Re-open domain design only with the new theorem as additional evidence, then separately resolve:

- whether the finite `a_max=10` support/taper is itself scientifically adequate;
- how any truncation limit is defined;
- W1/W2 representation and exact HJB↔KFE process matching;
- any principled `W_max` criterion.

### Route N-B — asymptotic sign remains conditional

Publish a deeper HJB/value-function asymptotic theory gate targeted at the exact missing growth conditions. Do not choose R or W and do not resume grid PASS seeking.

### Route N-C — source-consistent non-inward counterexample

Treat W-tail mean reversion as unestablished/weak. Reassess the household high-wealth economics before any W-domain design.

### Blocked

Resolve genuine source/theory inconsistency before scientific progression.

No route may bypass a later accepted HJB/KFE same-process validation before stationary re-entry.

---

## 4. Stationary household revalidation remains blocked

Stationary KFE remains NOT AUTHORIZED throughout DLH-5N.

Only after a state-domain/boundary-law process is scientifically selected, implemented and numerically validated may the project re-enter Issue #27:

- conservative generator;
- recurrent-class/nullspace evidence;
- pin admissibility and valid-pin invariance;
- ORIGINAL `Q^T g` residual;
- mass/non-negativity;
- stationary-tail diagnostics;
- recompute `C,L,A,B` and the two-region anchor from scratch.

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

During DLH-5N do not:

- mutate accepted HJB/KFE/regional source;
- mutate taper, transfer FOC, adjustment cost, economics, prices or calibration;
- choose/implement R, W, W1, W2, `W_max`, a new `b_max` or a new `a_max`;
- extrapolate the accepted taper beyond `a_max=10` as authority;
- add/rerun HJB grids, extents or resolutions;
- rerun J0–J5 or prior numerical fixtures;
- implement any boundary KKT law;
- clip policy;
- run stationary KFE/density/tail/aggregates;
- run regional GE, multi-province audit, network training, nominal HANK, calibration, policy/welfare or Results.

---

## 7. Governance status

Issue #40 is the current intended Builder theory-analysis task. Builder authority requires synchronized Task Index / Startup Snapshot plus authoritative activation comment.

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.
