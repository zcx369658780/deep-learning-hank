# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.14  
**Date:** 2026-09-02  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** CURRENT OWNER-APPROVED SCIENTIFIC ROUTE — DLH-5P ACTIVE

---

## 0. Long-run objective

Build a data-to-structural-model calibration and regional-network HANK platform in which household HJB/KFE, aggregation, firm/accounting blocks and later nominal-HANK equations remain explicit structural economics, while difficult cross-regional mappings become interpretable learned modules only after household and equilibrium foundations pass scientific and numerical validation.

The first learned object remains the regional labor/spatial rule. Capital-network learning and nominal-HANK integration remain later stages.

---

## 1. Accepted household foundation through DLH-5O

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

Stationary KFE remains NOT AUTHORIZED until the controlled household domain/boundary process is scientifically selected, implemented and numerically validated, then re-enters the Issue #27 recurrent-class/nullspace/pin/original-residual contract.

### Boundary/domain evidence — Issues #28–#39

Controlling accepted facts remain:

- artificial upper asset truncations can receive outward policy requests;
- pure larger-grid PASS seeking is CLOSED;
- high-wealth positive liquid drift is substantially a portfolio-transfer/reallocation phenomenon;
- on the pre-frozen 105-state evidence set, all 44 material positive-`mu_b` states have `mu_W=mu_a+mu_b<=0`;
- all 17 top-layer upper-b offenders violate rectangular `mu_b<=0` while satisfying `mu_a<=0` and `mu_W<=0`;
- `W=a+b` is an accepted source-accounting coordinate, not production-domain authority;
- Design R and Design W remain unfrozen under Owner decision `ACCEPT_RECOMMENDATION_U__DO_NOT_FREEZE_R_OR_W_YET`;
- no numerical `W_max` is authorized.

### Fixed-a liquid-tail drift theory — Issue #40 / DLH-5N

Accepted terminal:

`DLH_5N_FIXED_A_LIQUID_TAIL_TOTAL_WEALTH_SIGN_CONDITIONAL__MISSING_CONTROL_ASYMPTOTICS_IDENTIFIED`

Accepted interpretation: source accounting alone does not determine the sign of `mu_W` as `b->+infinity` with `a in [0,10]`; the missing object is the HJB/value-gradient tail.

### HJB value-function liquid-tail asymptotics — Issue #41 / DLH-5O

Accepted candidate:

`25645d2dd1963e8fc17176a7fadc16d914811221`

Reviewer acceptance comment:

`5504453148`

Acceptance integration commit:

`540b16ebd3a577a55ccd92a8d74ced373798557e`

Accepted terminal:

`DLH_5O_HJB_LIQUID_TAIL_DOMINANT_BALANCE_CONDITIONAL__MISSING_ANALYTIC_ASSUMPTIONS_IDENTIFIED`

Controlling interpretation:

1. The accepted MATLAB-faithful source is finite-grid HJB authority; it does not itself define an unbounded-positive-`b` HJB/transversality problem.
2. Tail analysis must use the combined transfer Hamiltonian

   ```text
   V_b * [d*(V_a/V_b - 1) - chi(d,a)]
   ```

   rather than adjustment cost alone.
3. The conditional p=2 candidate requires explicit derivative control

   `P-TR: V_a/V_b = o(sqrt(b))` uniformly.

4. Under the complete conditional premise set:

   ```text
   (rho+r_b)K - 2*sqrt(K) = S*K,
   K = 4/(rho+r_b)^2,
   c/b = 0.0175,
   mu_W/b -> -0.0025.
   ```

5. This is conditional fixed-a liquid-tail inwardness, not an unconditional theorem, full two-asset infinite-domain theorem, or domain choice.
6. The critical regime `V_a/V_b ~ Theta(sqrt(b))` remains unresolved because its transfer Hamiltonian is same-order at `O(1/b)` and changes the coefficient system.
7. P-TR alone yields sub-root/sublinear transfer-cost orders; bounded `O(1)` transfer/cost requires the stronger `V_a/V_b=O(1)` subcase.

---

## 2. Immediate model-specification gate — DLH-5P / Issue #42

### Name

**Unbounded-Liquid Analytic HJB Specification and Critical-Transfer Admissibility**

Task type:

`SCIENTIFIC_ANALYTIC_MODEL_SPECIFICATION__UNBOUNDED_LIQUID_HJB_ADMISSIBILITY_AND_CRITICAL_TRANSFER`

### Owner authorization

Owner approved:

`APPROVE_UNBOUNDED_B_ANALYTIC_HJB_SPECIFICATION_GATE__THEORY_DESIGN_ONLY`

The gate is model-defining in subject matter but **not self-freezing**: Builder produces candidate specifications and an Owner decision packet; only Owner may accept a new analytic-model authority after fresh review.

### Purpose

DLH-5O identified exactly what is missing: not another numerical grid, but a defensible analytic definition of the unbounded-positive-liquid HJB problem.

DLH-5P therefore asks:

> Which continuous HJB state space, admissibility/transversality class, regularity/uniformity requirements and derivative-control conditions are scientifically defensible as analytic authority for the fixed-`a` liquid tail, and do they rule out, admit or leave unresolved the critical `V_a/V_b ~ Theta(sqrt(b))` transfer branch?

### Required specification comparison

DLH-5P compares at least three packages:

- **S1 minimal growth/admissibility** — no hard-coded p=2 tail law;
- **S2 transversality-selected** — precise economically mapped discounted-value/no-Ponzi/transversality condition;
- **S3 derivative-controlled admissibility** — explicit condition sufficient for P-TR or stronger bounded transfer-ratio control, with circularity risk audited.

Every candidate must state:

- analytic state-space authority;
- exact continuous HJB equation;
- lower-`b` and `a` endpoint treatment;
- admissible value-function class;
- transversality/growth condition;
- regularity/uniformity;
- status of P-TR;
- whether DLH-5O p=2 coefficient theorem follows;
- risk that the specification simply assumes the desired tail;
- falsification criteria;
- mapping back to the finite-grid accepted source without claiming unproved equivalence.

### Critical-transfer branch

The gate must explicitly analyze

```text
R=V_a/V_b ~ L(a,z)*sqrt(b)
```

using the accepted transfer FOC and combined transfer Hamiltonian. It must derive the altered same-order coefficient system if coherent and determine whether the branch is ruled out, admitted or unresolved under S1/S2/S3.

### Endpoint requirement

Any uniform tail theorem must audit:

- `a=0` bare-`a` transfer degeneracy;
- `a=a_max=10` finite-support/taper authority;
- whether upper-`a` state-constraint semantics are analytic authority or finite-grid closure only;
- `b=b_lo=-2` and borrowing-rate-gap semantics;
- whether the theorem may cover the full `[0,10]` support or only an interior compact subset.

No new upper-`a` economic law may be invented for convenience.

### Outcome

The output is an **Owner decision packet**, not implementation. Exact Builder recommendation terminals are frozen in Issue #42:

- `DLH_5P_ANALYTIC_HJB_SPECIFICATION_CANDIDATE_READY__OWNER_MODEL_DEFINITION_DECISION_REQUIRED`
- `DLH_5P_CRITICAL_TRANSFER_BRANCH_REMAINS_ADMISSIBLE__TAIL_SPECIFICATION_NOT_UNIQUE__OWNER_DECISION_REQUIRED`
- `DLH_5P_ANALYTIC_HJB_SPECIFICATION_EVIDENCE_INSUFFICIENT__OWNER_DECISION_REQUIRED`
- `BLOCKED_DLH_5P_ACCEPTED_ECONOMICS_OR_AUTHORITY_INCONSISTENCY`

No recommendation itself creates accepted analytic authority.

---

## 3. Decision tree after DLH-5P

### Route P-A — candidate analytic specification survives review

Owner decides whether to accept one candidate as analytic-model authority. If accepted, publish a separate theorem/verification gate. Do not yet choose R/W or implement a numerical domain.

### Route P-B — critical branch remains admissible / tail not unique

Do not force P-TR. Continue analytic work on the critical transfer branch or revise the admissibility specification before any domain conclusion.

### Route P-C — evidence insufficient

Seek additional theory/economic review or simplify the claim. Do not continue symbolic proof by assumption.

### Blocked

Resolve genuine inconsistency in inherited economics/authority before further progress.

No route bypasses later HJB/KFE same-controlled-process validation.

---

## 4. Household re-entry sequence after analytic authority

Even a successful DLH-5P does NOT authorize stationary KFE. The remaining household route is:

```text
analytic-model authority / theorem gate
-> return to R/W domain-design decision
-> separate boundary-law implementation authority
-> HJB boundary validation
-> resolution / truncation robustness
-> conservative same-process generator
-> Issue #27 stationary KFE validation
-> recurrent-class / nullspace / pin / original Q^T g residual
-> mass / non-negativity / tail diagnostics
-> recompute C,L,A,B
-> rebuild two-region anchor
```

No historical aggregate is grandfathered.

---

## 5. Regional / Deep Learning sequence remains deferred

Permanent hierarchy:

```text
2-region unit fixture
-> 3–5 province integration fixture
-> 31-province empirical/source benchmark
```

Only after the household controlled process and stationary foundation are accepted does the project resume:

- two-region anchor;
- small multi-region integration;
- 31-province source benchmark;
- first learned regional labor/spatial rule;
- later capital-network learning;
- later nominal HANK, calibration, policy and welfare.

No neural training is authorized during DLH-5P.

---

## 6. Scientific ceiling during DLH-5P

Do not:

- mutate accepted HJB/KFE/regional source or household economics;
- freeze or implement a new analytic specification from Builder output alone;
- choose/implement R, W, W1, W2 or `W_max`;
- create new numerical `b_max`/`a_max` or extrapolate taper beyond `a_max=10`;
- run/extend HJB grids or previous numerical fixtures;
- run stationary KFE/density/tail/aggregates;
- implement boundary KKT law;
- run regional GE, multi-province audit, network training, nominal HANK, calibration, policy/welfare or Results.

---

## 7. Governance status

Issue #42 is the current intended Builder theory/design task. Builder authority requires synchronized Task Index / Startup Snapshot plus authoritative activation comment.

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.
