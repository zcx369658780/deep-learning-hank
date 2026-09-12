# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.46  
**Date:** 2026-09-12  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** DLH-5V-K / ISSUE #59 ACTIVE — FIXED-HOUSEHOLD EXTERNAL-PRICE ENVELOPE DIAGNOSTIC

---

## 0. Long-run objective

Build a hybrid structural–learned regional HANK platform in which household HJB/KFE, aggregation, firm/accounting and later nominal-HANK equations remain explicit structural economics, while hard-to-specify cross-regional mappings become learned modules only after household and equilibrium foundations pass scientific and numerical validation.

The first learned object remains regional labor/spatial mapping `W^L`. Neural training remains downstream.

---

## 1. Accepted household / finite-domain foundation

Accepted household oracle:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Accepted finite production-domain family:

```text
D_W(W_max)={0<=a<=10,b>=-2,a+b<=W_max}
```

No numerical production `W_max` is selected.

Binding law:

```text
HJB boundary policy <=> KFE boundary transition law
```

Restricted-Voronoi cells remain the accepted state partition / mass-volume geometry unless a later Owner-authorized route changes them. The same selected backward generator `Q` must define future forward mass dynamics `p_dot=Q^T p`.

Stationary KFE remains **NOT AUTHORIZED**.

---

## 2. Accepted finite-process provenance — DLH-5V-A through DLH-5V-E

Accepted grid/refinement family:

```text
da_m=10/(19m)
db_m=7/(19m)
10j+7i<=N_m
```

Accepted W-frontier sector semantics include exact represented wide/local moves and candidate-specific rates generated from local drift before maximization. The frozen composition remains:

```text
continuous admissibility
 -> representability / sector contract
 -> candidate-specific nonnegative rates
 -> candidate H_h score BEFORE selection
 -> ONE global statewise selection
 -> selected control + selected rates
 -> ONE conservative backward Q
 -> future KFE consumes exactly Q^T
```

---

## 3. Issues #54–#56 — accepted boundary theory provenance

### Issue #54 / DLH-5V-F

Endpoint exact finite-process representability obstruction accepted.

Accepted candidate: `b9dab7b6cf5d724074765ddb88d6f300175f6c6f`  
Reviewer acceptance: `5633995486`  
Integration: `4e77d9c753f81eb2517a8b90a0827db6af8faed4`

### Issue #55 / DLH-5V-G

Strong raw admitted-drift-set graph target obstruction accepted.

Accepted candidate: `15f2f81653a847344d2cd647705487cc893af1d7`  
Reviewer acceptance: `5635802416`  
Integration: `8dd5e9c444d7356736f28a29b9ffe492bbe81caa`

### Issue #56 / DLH-5V-H

State-constraint operator-consistency audit accepted at Outcome B.

Accepted candidate / integration: `55e29523e6f1bfefab270c05113984af003ea44b`  
Reviewer acceptance: `5644186157`  
Owner route decision / integration: `5644340159`

Accepted verdict:

`DLH_5VH_ACCEPTED__OUTCOME_B_CONFIRMED__UNBOUNDED_CONTROL_NUMERICAL_SCHEME_AND_STATE_CONSTRAINT_CONVERGENCE_APPLICATION_BLOCK_FROZEN`

One bounded unbounded-control/state-constraint convergence-application block remains explicit and unsolved.

---

## 4. Issue #57 / DLH-5V-I — boundary-HJB production-scheme design — OUTCOME A ACCEPTED

Accepted candidate / integration:

`3e450cf8ae177015e68ee7e05ecc5d6be7b2f8ec`

Reviewer acceptance: `5644767550`  
Acceptance integration: `5644769439`

Accepted verdict:

`DLH_5VI_ACCEPTED__OUTCOME_A_CONFIRMED__BOUNDARY_HJB_SCHEME_CONTRACT_FROZEN__IMPLEMENTATION_GATE_READY_UNDER_ACCEPTED_OUTCOME_B_THEORY_CEILING`

Frozen authority includes unique Route-A F0–F11 ownership, explicit representability exclusions, algorithm-only numerical brackets, rates from local drift before scoring, ONE deterministic global selection, same selected rates in conservative backward Q, accepted `grid.switch_matrix`, pseudo-time HJB integration, separate iterate convergence/final Bellman residual, and named failures with no silent fallback.

---

## 5. Issue #58 / DLH-5V-J — boundary-HJB implementation + local validation — TERMINAL B ACCEPTED

Accepted candidate / integration:

`7b564d1b7d7aaf76b808135b192646e0ec1f5f08`

Reviewer acceptance:

`5646205500`

Acceptance integration:

`5646215533`

Accepted verdict:

`DLH_5VJ_ACCEPTED__TERMINAL_B_CONFIRMED__BOUNDARY_HJB_IMPLEMENTATION_PARTIAL__EFFECTIVE_DOMAIN_EXIT_FROZEN__OWNER_STABILIZATION_ROUTE_DECISION_REQUIRED`

Accepted terminal:

`DLH_5VJ_BOUNDARY_HJB_IMPLEMENTATION_PARTIAL__ONE_BOUNDED_NUMERICAL_OR_CONTRACT_GAP_REMAINS`

Accepted implementation evidence:

- F0 common-input regression PASS;
- Route-A family/sector/representability/first-moment checks PASS;
- first-iteration selected backward Q conservative and deterministic;
- frozen Gate-3 validation exits the `p_b>0` effective domain at iteration 2;
- first failure F3 `(13,13)`, `z=0`, `p_b≈-0.365224`;
- corrected implementation raises `DERIVATIVE_EFFECTIVE_DOMAIN_FAILURE` before candidate/bracket search;
- no final Bellman residual because convergence is not reached.

This is not accepted as a household-equation, geometry, or sector-algebra contradiction.

---

## 6. Owner route decision after Issue #58 — diagnose external-price envelope BEFORE stabilization

Owner scientific experience from prior multi-province HANK work:

- keep the household HJB structure, preference/adjustment parameters, and asset-domain bounds fixed;
- HJB convergence can depend materially on endogenous GE inputs such as `r_a`, `r_b`, and regional wage `w_jt`;
- economically reasonable values (illustratively `r_b≈0.02`, `r_a≈0.07`, `w≈1`) often converge, while sufficiently extreme values (illustratively high `r_a`, e.g. around `0.13`) can drive boundary-like policies or nonconvergence;
- earlier multi-province workflows sometimes constrained GE search iterates for `r_a` and `w_jt`, while final steady states remained interior to those search ranges;
- varying `b_max` or other household-domain bounds while diagnosing prices changes the household fixed-point problem and should therefore be avoided.

Owner decision:

`APPROVE_FIXED_HOUSEHOLD_EXTERNAL_PRICE_ENVELOPE_DIAGNOSTIC_BEFORE_STABILIZATION`

This is a hypothesis to test, not a frozen conclusion.

---

## 7. DLH-5V-K / Issue #59 — ACTIVE DIAGNOSTIC

Title:

`DLH-5V-K: Diagnose fixed-household external-price convergence envelope before HJB stabilization`

Task type:

`SCIENTIFIC_DIAGNOSTIC__FIXED_HOUSEHOLD_EXTERNAL_PRICE_CONVERGENCE_ENVELOPE`

Authority marker:

`DLH_5VK_FIXED_HOUSEHOLD_PRICE_ENVELOPE_DIAGNOSTIC_AUTHORIZED`

Dedicated Builder branch:

`dsh/issue-59-dlh-5vk-fixed-household-price-envelope-2026-09-12`

Initial activation comment:

`5646298166`

### 7.1 Legacy-oracle diagnostic

Hold fixed:

```text
a grid: 0..10, 20 points
b grid: -2..5, 20 points
b_max = 5
household preference/adjustment parameters
solver tolerances
initialization rule
```

Map only the bounded predeclared external-price cases in `(r_a,r_b,w)`, including the Owner safe/high `r_a` anchors. Conditional maximum-four midpoint evaluations may localize an `r_a` PASS/FAIL transition only if the predeclared line contains a clear bracket.

### 7.2 Current selected-Q diagnostic

Hold fixed:

```text
m=1
W_max=10
r_b=0.02
w=1
all household / numerical settings
```

Evaluate only `r_a={0.07,0.10,0.13}` as cross-scheme sentinels.

The rectangle and triangular domain are not the same geometry; convergence differences are diagnostic and must not be attributed causally to geometry without a later dedicated comparison.

### 7.3 Interpretation targets

- **H1:** external-price envelope materially explains fixed-household HJB convergence;
- **H2:** external-price region matters but selected-Q effective-domain instability remains at central/safe prices;
- **H3:** expected external-price convergence pattern is not supported on the frozen fixture.

No stabilization mechanism is authorized in this Issue.

---

## 8. Current roadmap position

```text
MATLAB-faithful two-asset household economics                 ACCEPTED
finite W-domain + continuous tangent/KKT law                 ACCEPTED
same-process HJB <=> KFE principle                           ACCEPTED
restricted-Voronoi state partition                           ACCEPTED
regular W-frontier finite-process block                      ACCEPTED
endpoint exact finite-process closure                         OBSTRUCTION ACCEPTED — ISSUE #54
Route A strong raw graph target                               OBSTRUCTION ACCEPTED — ISSUE #55
state-constraint operator-consistency audit                   OUTCOME B ACCEPTED — ISSUE #56
boundary-HJB production-scheme design                         OUTCOME A ACCEPTED — ISSUE #57
boundary-HJB implementation + local HJB validation            TERMINAL B ACCEPTED — ISSUE #58
fixed-household external-price convergence envelope           ACTIVE — ISSUE #59
effective-domain-preserving HJB stabilization route          PENDING AFTER #59
same-process Q global validation + SCC diagnostics            BLOCKED UNTIL HJB ROUTE RESOLVED
nested Wmax / resolution robustness                          BLOCKED UNTIL HJB ROUTE RESOLVED
conservative stationary-generator validation                 BLOCKED UNTIL HJB ROUTE RESOLVED
Issue #27 stationary KFE                                     NOT AUTHORIZED
stationary C,L,A,B                                           PENDING
two-region structural anchor rebuild                         PENDING
3–5 province integration                                     PENDING
learned regional W^L                                         PENDING
```

---

## 9. Same-process safeguards — frozen

```text
Q backward
Q^T forward
Q_ij>=0 for i!=j
Q_ii=-sum of ACTUAL represented outgoing rates
Q1=0 by construction
same selected candidate/rates for HJB and future KFE
p=M g
p_dot=Q^T p
```

No route may use pinning/normalization to repair leakage or create a KFE-only process.

Stationary KFE remains explicitly blocked.

---

## 10. Current governance position

**ACTIVE BUILDER ISSUE: #59**, but execution begins only after activation-ID CURRENT synchronization + final activation-refresh comment.

Current governance pointers:

- `tasks/TASK_INDEX_CURRENT.md`
- `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
- Issue #59 body/comments.

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.
