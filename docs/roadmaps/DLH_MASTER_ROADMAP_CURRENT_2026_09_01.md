# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.16  
**Date:** 2026-09-02  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** CURRENT OWNER-APPROVED SCIENTIFIC ROUTE — DLH-5Q ACTIVE

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
- the accepted finite-state evidence favors inward total-wealth drift even when rectangular upper-b drift is outward;
- `W=a+b` is an accepted source-accounting coordinate, not production-domain authority;
- Design R and Design W remain unfrozen under Owner decision `ACCEPT_RECOMMENDATION_U__DO_NOT_FREEZE_R_OR_W_YET`;
- no numerical `W_max` is authorized.

### Fixed-a liquid-tail drift theory — Issue #40 / DLH-5N

Accepted terminal:

`DLH_5N_FIXED_A_LIQUID_TAIL_TOTAL_WEALTH_SIGN_CONDITIONAL__MISSING_CONTROL_ASYMPTOTICS_IDENTIFIED`

Source accounting alone does not determine the asymptotic sign of `mu_W`; the missing object is the HJB/value-gradient tail.

### HJB value-function tail asymptotics — Issue #41 / DLH-5O

Accepted candidate:

`25645d2dd1963e8fc17176a7fadc16d914811221`

Accepted terminal:

`DLH_5O_HJB_LIQUID_TAIL_DOMINANT_BALANCE_CONDITIONAL__MISSING_ANALYTIC_ASSUMPTIONS_IDENTIFIED`

Under the full conditional p=2/P-TR premise set:

```text
(rho+r_b)K - 2*sqrt(K) = S*K
K = 4/(rho+r_b)^2
c/b = 0.0175
mu_W/b -> -0.0025
```

This is a conditional dominant balance, not a theorem or domain choice.

### Analytic HJB specification review — Issue #42 / DLH-5P

Accepted candidate:

`faa9fd27dec941de72888d2c8db7db6f5393e0f6`

Reviewer acceptance comment:

`5505979616`

Acceptance integration:

`156d8d092839668b18ab52a6a9d0e12023f248bd`

Accepted terminal:

`DLH_5P_CRITICAL_TRANSFER_BRANCH_REMAINS_ADMISSIBLE__TAIL_SPECIFICATION_NOT_UNIQUE__OWNER_DECISION_REQUIRED`

Controlling accepted interpretation:

1. **S1 base:** fixed-a-support unbounded-positive-b analytic extension; with `V_b>0`, `V<0`, finite lower b and compact a/z, admissible V is bounded with finite `V_inf(a,z)<=0`.
2. **S2 selection:** `V_inf(a,z)=0` is a candidate new analytic selection assumption, not a proved necessity or comparison theorem.
3. **S3 derivative control:** `R=V_a/V_b=O(1)` uniformly (preferred) or weaker P-TR `R=o(sqrt(b))`; this excludes the critical branch by class but does not prove actual p=2 realization.
4. Critical `R~Theta(sqrt(b))` remains an unresolved/admissible formal dominant balance on compact interior-a sets outside S3.
5. For the constant-across-z scalar critical subfamily with `C=aL^2>=0`, `a>=a_bar`:

   ```text
   c/b = (rho+r_b+0.5*C/chi_1)/2
   mu_W/b = -0.0025 - 3*C/(4*chi_1) < 0
   ```

   so the tail coefficient is non-unique outside S3 while the demonstrated family remains total-wealth inward.
6. No actual admissible critical HJB solution, full-support smooth realization, existence/comparison theorem or realized-tail uniqueness has been established.

---

## 2. Owner decision — Option C adopted

Owner selected:

`PROVISIONAL_S3_ANALYTIC_CLASS__PARALLEL_FALSIFICATION_ROUTE_APPROVED`

Owner-decision comment:

`5506138177`

### Provisional working analytic authority

For theorem analysis going forward:

- retain S1 as the continuous analytic base;
- provisionally adopt S2 `V_inf=0` as the tail-value selection assumption;
- provisionally adopt **primary S3 `R=O(1)` uniformly** as the working derivative-control class;
- retain P-TR `R=o(sqrt(b))` only as a weaker sensitivity envelope;
- keep the critical `R~Theta(sqrt(b))` family outside S3 as a parallel falsification/exclusion-cost benchmark.

Scientific meaning:

- the project may now pursue a tractable theorem inside S3;
- the exclusion of the critical branch is explicit model-class selection, not a derived theorem;
- the project must simultaneously preserve a route capable of falsifying S3 analytically or, later under separate authority, numerically;
- no R/W/domain/KFE implementation follows from this provisional choice.

---

## 3. Immediate theorem/falsification gate — DLH-5Q / Issue #43

### Name

**Provisional S3 Tail-Theorem Verification and Parallel Falsification**

Task type:

`SCIENTIFIC_THEOREM_VERIFICATION__PROVISIONAL_S3_LIQUID_TAIL_AND_PARALLEL_FALSIFICATION`

### Purpose

DLH-5Q asks:

> Within the provisional S1+S2+S3 class, can the actual admissible HJB tail be shown to realize the p=2 asymptotics and coefficient, while an independent falsification route remains capable of rejecting the provisional class?

### Required logic

DLH-5Q must:

1. freeze the exact provisional class for theorem work;
2. audit existence, comparison/uniqueness and endpoint well-posedness;
3. attempt p=2 asymptotic realization under primary `R=O(1)` rather than assuming it;
4. derive the p=2 coefficient/drift only if realization is justified;
5. search analytically for S3-internal alternative tails, non-power regimes, derivative-remainder counterexamples, z-coupling failures and any inward-sign reversal;
6. preserve the out-of-class critical family as an exclusion-cost benchmark;
7. design but not execute a future numerical falsification protocol using `V_a/V_b`, `b^2V_b`, `c/b`, transfer/cost orders and boundary-influence diagnostics;
8. separate compact-interior theorem scope from `a=0`, `a=10` and lower-liquid endpoint authority.

### Exact terminals

- `DLH_5Q_PROVISIONAL_S3_FIXED_A_LIQUID_TAIL_THEOREM_VERIFIED__PARALLEL_FALSIFICATION_PROTOCOL_READY`
- `DLH_5Q_PROVISIONAL_S3_THEOREM_NOT_CLOSED__MISSING_EXISTENCE_COMPARISON_OR_ASYMPTOTIC_REALIZATION_IDENTIFIED__FALSIFICATION_PROTOCOL_READY`
- `DLH_5Q_PROVISIONAL_S3_ANALYTIC_CLASS_FALSIFIED__OWNER_REDEFINITION_REQUIRED`
- `DLH_5Q_INTERIOR_A_TAIL_THEOREM_SUPPORTED__FULL_SUPPORT_ENDPOINT_AUTHORITY_OWNER_DECISION_REQUIRED`
- `BLOCKED_DLH_5Q_ACCEPTED_HJB_OR_PROVISIONAL_S3_AUTHORITY_INCONSISTENCY`

No terminal authorizes R/W/domain implementation or stationary KFE.

---

## 4. Route after DLH-5Q

### Route Q-A — theorem verified within provisional S3

```text
accepted S3 theorem/falsification package
-> Owner decides whether provisional S3 graduates to accepted analytic authority
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

### Route Q-B — theorem not closed

Continue only the sharply identified missing analytic gate; do not silently promote provisional assumptions to theorem status.

### Route Q-C — S3 analytically falsified

Return immediately to Owner model-definition review; do not continue domain design under S3.

### Route Q-D — interior theorem only

Resolve the model-defining endpoint law before any full-support claim or domain implementation.

No route skips later HJB/KFE same-controlled-process validation.

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

No neural training is authorized during DLH-5Q.

---

## 6. Scientific ceiling during DLH-5Q

Do not:

- mutate accepted HJB/KFE/regional source or household economics;
- choose/implement R/W/W1/W2 or `W_max`;
- create new numerical `b_max`/`a_max` or extrapolate taper beyond `a_max=10`;
- run HJB/KFE/grid/resolution/stationary experiments;
- rerun previous numerical fixtures;
- implement endpoint KKT/state-domain law;
- run regional GE, multi-province audit, network training, nominal HANK, calibration, policy/welfare or Results.

---

## 7. Governance status

Issue #43 / DLH-5Q is the current intended Builder theorem/falsification task. Builder authority requires synchronized Task Index / Startup Snapshot plus authoritative activation comment.

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.
