# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.15  
**Date:** 2026-09-02  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** CURRENT OWNER-DECISION CHECKPOINT — DLH-5P ACCEPTED / NO ACTIVE BUILDER ISSUE

---

## 0. Long-run objective

Build a data-to-structural-model calibration and regional-network HANK platform in which household HJB/KFE, aggregation, firm/accounting blocks and later nominal-HANK equations remain explicit structural economics, while difficult cross-regional mappings become interpretable learned modules only after household and equilibrium foundations pass scientific and numerical validation.

The first learned object remains the regional labor/spatial rule. Capital-network learning and nominal-HANK integration remain later stages.

---

## 1. Accepted household foundation through DLH-5P

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

Stationary KFE remains NOT AUTHORIZED until a controlled household domain/boundary process is scientifically selected, implemented and numerically validated, then re-enters the Issue #27 recurrent-class/nullspace/pin/original-residual contract.

### Boundary/domain evidence — Issues #28–#39

Controlling accepted facts remain:

- artificial upper asset truncations can receive outward policy requests;
- pure larger-grid PASS seeking is CLOSED;
- high-wealth positive liquid drift is substantially a portfolio-transfer/reallocation phenomenon;
- on the pre-frozen 105-state evidence set, all 44 material positive-`mu_b` states have `mu_W<=0`;
- all 17 top-layer upper-b offenders violate rectangular `mu_b<=0` while satisfying `mu_a<=0` and `mu_W<=0`;
- `W=a+b` is an accepted source-accounting coordinate, not production-domain authority;
- Design R and Design W remain unfrozen under Owner decision `ACCEPT_RECOMMENDATION_U__DO_NOT_FREEZE_R_OR_W_YET`;
- no numerical `W_max` is authorized.

### Fixed-a liquid-tail drift theory — Issue #40 / DLH-5N

Accepted terminal:

`DLH_5N_FIXED_A_LIQUID_TAIL_TOTAL_WEALTH_SIGN_CONDITIONAL__MISSING_CONTROL_ASYMPTOTICS_IDENTIFIED`

Source accounting alone does not determine the asymptotic sign of `mu_W` as `b->+infinity`; the missing object is the HJB/value-gradient tail.

### HJB value-function liquid-tail asymptotics — Issue #41 / DLH-5O

Accepted candidate:

`25645d2dd1963e8fc17176a7fadc16d914811221`

Reviewer acceptance comment:

`5504453148`

Acceptance integration commit:

`540b16ebd3a577a55ccd92a8d74ced373798557e`

Accepted terminal:

`DLH_5O_HJB_LIQUID_TAIL_DOMINANT_BALANCE_CONDITIONAL__MISSING_ANALYTIC_ASSUMPTIONS_IDENTIFIED`

Controlling result under the full conditional p=2/P-TR premise set:

```text
(rho+r_b)K - 2*sqrt(K) = S*K
K = 4/(rho+r_b)^2
c/b = 0.0175
mu_W/b -> -0.0025
```

This is a conditional fixed-a liquid-tail result, not an unconditional theorem or domain choice.

### Analytic HJB specification review — Issue #42 / DLH-5P

Accepted candidate:

`faa9fd27dec941de72888d2c8db7db6f5393e0f6`

Reviewer acceptance comment:

`5505979616`

Acceptance integration commit:

`156d8d092839668b18ab52a6a9d0e12023f248bd`

Accepted verdict:

`DLH_5P_REV4_ACCEPTED__RECOMMENDATION_B_SUPPORTED__CRITICAL_TRANSFER_BRANCH_REMAINS_FORMALLY_ADMISSIBLE__TAIL_COEFFICIENT_NONUNIQUE__DEMONSTRATED_TOTAL_WEALTH_DRIFT_REMAINS_INWARD__OWNER_DECISION_REQUIRED`

Accepted recommendation terminal:

`DLH_5P_CRITICAL_TRANSFER_BRANCH_REMAINS_ADMISSIBLE__TAIL_SPECIFICATION_NOT_UNIQUE__OWNER_DECISION_REQUIRED`

Controlling interpretation:

1. **S1 minimal analytic extension:** with `V_b>0`, `V<0`, finite lower `b`, compact `a in [0,10]`, finite z and continuity, admissible V is bounded and has a finite tail limit `V_inf(a,z)<=0`.
2. **S2 tail-value selection:** `V_inf(a,z)=0` is a proposed new analytic-model definition / theorem assumption. It is not a proved necessity, not an asset no-Ponzi theorem, and not by itself a uniqueness/comparison result.
3. **S3 derivative-control admissibility:** `R=V_a/V_b=O(1)` uniformly (preferred) or P-TR `R=o(sqrt(b))` may be adopted by the Owner as an explicit admissibility primitive. It excludes the critical transfer branch by class but does not prove that the actual HJB tail is `p=2`.
4. The critical branch

   `R~L(a,z)*sqrt(b)`

   remains an **UNRESOLVED/ADMISSIBLE formal dominant balance on compact interior-a sets** through an a-dependent subleading remainder.
5. For `p=2`, `a>=a_bar`, and the scalar symmetric subfamily with constant `C=aL^2>=0` across productivity states:

   ```text
   (rho+r_b)K - 2*sqrt(K) = -0.5*C*K/chi_1
   c/b = (rho+r_b+0.5*C/chi_1)/2
   chi/b = 0.5*C/chi_1
   mu_W/b = -0.0025 - 3*C/(4*chi_1) < 0
   ```

   Thus the demonstrated critical family gives a continuum of consumption/tail coefficients but remains total-wealth inward.
6. If `C(z)` differs across productivity states, the coupled switch system must be solved; the scalar formula is only for the constant-across-z subfamily.
7. No actual admissible critical HJB solution, full asymptotic-series completion, full `[0,10]` smooth realization, endpoint-compatible theorem, existence/comparison result or realized-tail uniqueness is established.
8. Recommendation B therefore concerns **analytic-tail/coefficient non-uniqueness**, not a demonstrated failure of total-wealth mean reversion.
9. R/W remain unfrozen. No `W_max`. Stationary KFE remains NOT AUTHORIZED.

---

## 2. Current checkpoint — Owner analytic-model decision after DLH-5P

There is **no active Builder Issue**.

The scientific question is now explicit:

> Should the project adopt derivative-control S3 as an analytic admissibility primitive, continue working on the critical `m=1/2` remainder branch without imposing S3, or use S3 provisionally while separately testing/falsifying it?

### Owner option A — adopt S3 explicitly

Adopt the analytic specification:

- S1 continuous base;
- S2 `V_inf=0` tail-value selection;
- S3 derivative control `R=O(1)` uniformly (preferred), with P-TR `R=o(sqrt(b))` as weaker fallback.

Scientific meaning:

- the critical `m=1/2` branch is excluded by a transparent Owner-adopted model primitive;
- the p=2 coefficient remains only a theorem candidate;
- a successor theorem/verification gate must still prove existence, comparison/uniqueness, endpoint consistency, asymptotic realization, derivative-remainder regularity and `V_b b^2 -> K` convergence.

### Owner option B — keep S1/S2, resolve critical branch first

Do not impose derivative control yet. Open a research gate to determine whether the formal `m=1/2` remainder family can be completed to an actual admissible HJB solution, including:

- lower-order asymptotic completion;
- z-state coupling;
- `a=0` / `a=10` endpoint consistency;
- S2 `V_inf=0` compatibility;
- existence/comparison and realized coefficient selection.

### Owner option C — provisional S3 + parallel falsification

Provisionally adopt S3 as a tractable theorem class while simultaneously keeping a separate falsification route for the critical branch / actual finite-grid value-gradient behavior. This makes the exclusionary model choice explicit rather than pretending it was derived.

No option is selected automatically by accepted DLH-5P.

---

## 3. Route after Owner decision

### If S3 is adopted

```text
Owner analytic-model definition
-> theorem/verification gate
   (existence, comparison, regularity, endpoint laws, asymptotic realization, coefficient convergence)
-> return to R/W domain-design decision
-> boundary-law implementation authority
-> HJB boundary validation
-> truncation/resolution robustness
-> conservative same-process generator
-> Issue #27 stationary KFE validation
-> recurrent-class / nullspace / pin / original Q^T g residual
-> mass / non-negativity / stationary-tail diagnostics
-> recompute C,L,A,B
-> rebuild two-region anchor
```

### If critical branch is pursued first

```text
critical-branch analytic resolution
-> Owner analytic-model definition
-> theorem/verification gate
-> return to R/W domain design
-> same downstream household re-entry sequence
```

No route skips HJB/KFE same-controlled-process validation.

---

## 4. Regional / Deep Learning sequence remains deferred

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

No neural training is authorized at the current checkpoint.

---

## 5. Scientific ceiling at the current checkpoint

Until Owner decision and successor activation, do not:

- mutate accepted HJB/KFE/regional source or household economics;
- freeze an analytic specification by Builder recommendation alone;
- choose/implement R, W, W1, W2 or `W_max`;
- create new numerical `b_max`/`a_max` or extrapolate taper beyond `a_max=10`;
- run/extend HJB grids or previous numerical fixtures;
- run stationary KFE/density/tail/aggregates;
- implement boundary KKT law;
- run regional GE, multi-province audit, network training, nominal HANK, calibration, policy/welfare or Results.

---

## 6. Governance status

Issue #42 / DLH-5P is accepted and CLOSED completed.

Current governance status:

`NO_ACTIVE_BUILDER_ISSUE__DLH_5P_ACCEPTED__OWNER_MODEL_DEFINITION_DECISION_PENDING`

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.
