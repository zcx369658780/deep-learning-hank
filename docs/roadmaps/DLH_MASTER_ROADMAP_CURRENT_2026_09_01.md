# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.47  
**Date:** 2026-09-13  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** DLH-5V-L / ISSUE #60 ACTIVE — INVARIANT-DOMAIN SAFEGUARDED HJB UPDATE DIAGNOSTIC

---

## 0. Long-run objective

Build a hybrid structural–learned regional HANK platform in which household HJB/KFE, aggregation, firm/accounting and later nominal-HANK equations remain explicit structural economics, while hard-to-specify cross-regional mappings become learned modules only after household and equilibrium foundations pass scientific and numerical validation.

The first learned object remains regional labor/spatial mapping `W^L`. Neural training remains downstream.

---

## 1. Accepted household / finite-domain foundation

Accepted household oracle:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb337f1b02b3fe33c51e`

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

## 2. Accepted finite-process provenance — Issues #54–#56

- Issue #54 / DLH-5V-F: endpoint exact finite-process representability obstruction ACCEPTED.
- Issue #55 / DLH-5V-G: strong raw admitted-drift-set graph target obstruction ACCEPTED.
- Issue #56 / DLH-5V-H: state-constraint operator-consistency audit accepted at Outcome B.

Issue #56 accepted verdict:

`DLH_5VH_ACCEPTED__OUTCOME_B_CONFIRMED__UNBOUNDED_CONTROL_NUMERICAL_SCHEME_AND_STATE_CONSTRAINT_CONVERGENCE_APPLICATION_BLOCK_FROZEN`

One bounded unbounded-control/state-constraint convergence-application block remains explicit and unsolved.

---

## 3. Issue #57 / DLH-5V-I — boundary-HJB production-scheme design — OUTCOME A ACCEPTED

Accepted candidate / integration:

`3e450cf8ae177015e68ee7e05ecc5d6be7b2f8ec`

Reviewer acceptance: `5644767550`  
Acceptance integration: `5644769439`

Frozen authority includes unique Route-A F0–F11 ownership, explicit representability exclusions, algorithm-only numerical brackets, rates from local drift before scoring, ONE deterministic global selection, same selected rates in conservative backward Q, accepted `grid.switch_matrix`, pseudo-time HJB integration, separate iterate convergence/final Bellman residual, and named failures with no silent fallback.

---

## 4. Issue #58 / DLH-5V-J — boundary-HJB implementation + local validation — TERMINAL B ACCEPTED

Accepted candidate / integration:

`7b564d1b7d7aaf76b808135b192646e0ec1f5f08`

Reviewer acceptance: `5646205500`  
Acceptance integration: `5646215533`

Accepted result:

- F0 common-input regression PASS;
- Route-A family/sector/representability/first-moment checks PASS;
- first-iteration selected backward Q conservative and deterministic;
- frozen validation exits the `p_b>0` boundary effective domain at iteration 2;
- corrected implementation raises `DERIVATIVE_EFFECTIVE_DOMAIN_FAILURE` before candidate/bracket search.

This is not accepted as a household-equation, geometry, or sector-algebra contradiction.

---

## 5. Issue #59 / DLH-5V-K — fixed-household external-price envelope — TERMINAL B / H2 ACCEPTED

Accepted candidate / integration:

`08f0135de5a60d05eda7184c367e1705da69757d`

Reviewer acceptance:

`5649245347`

Acceptance integration:

`5649248162`

Accepted verdict:

`DLH_5VK_ACCEPTED__TERMINAL_B_H2_CONFIRMED__LEGACY_EXTERNAL_PRICE_SENSITIVITY_REAL__SELECTED_Q_EFFECTIVE_DOMAIN_GAP_REMAINS__STABILIZATION_DIAGNOSTIC_NEXT`

Accepted scientific interpretation:

- external prices materially affect the frozen legacy HJB solver;
- sampled convergent `r_a` points include `0.07,0.09,0.11,0.12`, while `0.065` and `0.125` fail; this is an observed sampled span / transition bracket, not a theorem that every `r_a` in `[0.07,0.12]` converges;
- legacy numerical convergence does not by itself validate economic quality or the exact unbounded-control HJB because the accepted source `v_b` floor is active at nontrivial shares and non-positive finite-difference `V_b` occurs at converged points;
- the current selected-Q solver still exits its accepted boundary effective domain at the central tested sentinel `r_a=0.07`;
- cross-solver convergence differences do not establish a geometry cause or a globally price-independent selected-Q failure.

Therefore future GE work should preserve external-price search discipline, but price envelopes are not accepted as a cure for the selected-Q invariant-domain gap.

---

## 6. Issue #60 / DLH-5V-L — ACTIVE invariant-domain safeguard diagnostic

Title:

`DLH-5V-L: Test invariant-domain safeguarded value-update line search on the central selected-Q HJB case`

Task type:

`SCIENTIFIC_NUMERICAL_DIAGNOSTIC__EFFECTIVE_DOMAIN_PRESERVING_VALUE_UPDATE`

Owner / Reviewer route decision:

`APPROVE_CONTROLLED_INVARIANT_DOMAIN_SAFEGUARDED_VALUE_UPDATE_DIAGNOSTIC`

Authority marker:

`DLH_5VL_INVARIANT_DOMAIN_SAFEGUARD_DIAGNOSTIC_AUTHORIZED`

Dedicated Builder branch:

`dsh/issue-60-dlh-5vl-invariant-domain-safeguard-2026-09-13`

Initial activation comment:

`PENDING_INITIAL_ACTIVATION_COMMENT`

### 6.1 Frozen central selected-Q case

```text
m=1
W_max=10
r_a=0.07
r_b=0.02
w=1.00
borrowing_rate_gap=0
delta=1000
tolerance_iter=1e-7
tolerance_Bellman=1e-3
max_iterations=1000
n_c=n_d=9
```

All household parameters, grid/domain, initialization, Q/candidate rules and search-bracket semantics remain frozen.

### 6.2 Authorized safeguard only

The raw accepted selected-Q update remains the only operator update:

```text
V_raw=T(V_old)
```

The new diagnostic may only replace immediate acceptance of `V_raw` by:

```text
V_trial(lambda)=V_old+lambda*(V_raw-V_old)
lambda in {1,1/2,...,2^-20}
choose the largest lambda with all required boundary p_b > 1e-12
```

The margin is an iterate-acceptance numerical tolerance only; no derivative is clipped/floored and no economics is changed.

Exactly one central-case run and one deterministic repeat are authorized.

### 6.3 PASS standard

Outcome A requires:

- accepted iterates stay inside the boundary effective domain;
- convergence within 1000 accepted iterations;
- final re-selection on final V;
- final `||R_Bellman||_inf <= 1e-3`;
- conservative selected Q;
- no accepted artificial bracket binding;
- deterministic repeat.

A tiny damped step without Bellman residual PASS is stagnation, not convergence.

---

## 7. Current roadmap position

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
fixed-household external-price envelope                       TERMINAL B/H2 ACCEPTED — ISSUE #59
invariant-domain safeguarded HJB update                       ACTIVE — ISSUE #60
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

## 8. Same-process safeguards — frozen

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

## 9. Current governance position

**ACTIVE BUILDER ISSUE: #60**, but execution begins only after initial activation comment + CURRENT activation-ID synchronization + final activation-refresh comment.

Current governance pointers:

- `tasks/TASK_INDEX_CURRENT.md`
- `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
- Issue #60 body/comments.

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.
