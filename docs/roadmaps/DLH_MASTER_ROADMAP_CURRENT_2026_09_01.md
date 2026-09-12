# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.45  
**Date:** 2026-09-12  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** DLH-5V-J / ISSUE #58 TERMINAL B ACCEPTED — EFFECTIVE-DOMAIN STABILIZATION ROUTE DECISION PENDING

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

## 3. Issue #54 / DLH-5V-F — endpoint finite-m representability obstruction — ACCEPTED

Accepted candidate: `b9dab7b6cf5d724074765ddb88d6f300175f6c6f`  
Reviewer acceptance: `5633995486`  
Acceptance integration: `4e77d9c753f81eb2517a8b90a0827db6af8faed4`

The exact finite-m native-lattice obstruction remains a true discretization fact. Certified unrepresentable candidate rays may not be silently clipped or converted into diagonal leakage.

---

## 4. Issue #55 / DLH-5V-G — strong raw graph target obstruction — ACCEPTED

Accepted candidate: `15f2f81653a847344d2cd647705487cc893af1d7`  
Reviewer acceptance: `5635802416`  
Acceptance integration: `8dd5e9c444d7356736f28a29b9ffe492bbe81caa`

Issue #55 remains accepted under the strong raw admitted-drift-set graph target it was assigned.

---

## 5. Issue #56 / DLH-5V-H — state-constraint operator-consistency audit — OUTCOME B ACCEPTED

Accepted candidate / integration:

`55e29523e6f1bfefab270c05113984af003ea44b`

Reviewer acceptance: `5644186157`  
Acceptance integration / Owner route decision: `5644340159`

Accepted verdict:

`DLH_5VH_ACCEPTED__OUTCOME_B_CONFIRMED__UNBOUNDED_CONTROL_NUMERICAL_SCHEME_AND_STATE_CONSTRAINT_CONVERGENCE_APPLICATION_BLOCK_FROZEN`

Accepted result:

- Issue #55 raw graph target is stronger than the legitimate local operator/test-function consistency machinery;
- frozen process is not refuted on effective-domain smooth tests;
- discrete optimizer localization / max-level Taylor consistency / boundary restriction-recovery are established locally;
- one bounded unbounded-control/state-constraint convergence-application block remains unresolved.

Owner selected Route B: preserve that theory ceiling and proceed numerically rather than require a global analytic convergence theorem before implementation.

---

## 6. Issue #57 / DLH-5V-I — boundary-HJB production-scheme design — OUTCOME A ACCEPTED

Accepted candidate / integration:

`3e450cf8ae177015e68ee7e05ecc5d6be7b2f8ec`

Reviewer acceptance:

`5644767550`

Acceptance integration:

`5644769439`

Accepted verdict:

`DLH_5VI_ACCEPTED__OUTCOME_A_CONFIRMED__BOUNDARY_HJB_SCHEME_CONTRACT_FROZEN__IMPLEMENTATION_GATE_READY_UNDER_ACCEPTED_OUTCOME_B_THEORY_CEILING`

Frozen implementation authority includes unique Route-A F0–F11 ownership, explicit representability exclusions, algorithm-only numerical brackets, rates from local drift before scoring, ONE deterministic global selection, same selected rates in conservative backward Q, accepted `grid.switch_matrix`, pseudo-time HJB integration, separate iterate convergence / final Bellman residual, and named failures with no silent fallback.

---

## 7. Issue #58 / DLH-5V-J — boundary-HJB implementation + local validation — TERMINAL B ACCEPTED

Accepted candidate / integration:

`7b564d1b7d7aaf76b808135b192646e0ec1f5f08`

Reviewer acceptance:

`5646205500`

Accepted verdict:

`DLH_5VJ_ACCEPTED__TERMINAL_B_CONFIRMED__BOUNDARY_HJB_IMPLEMENTATION_PARTIAL__EFFECTIVE_DOMAIN_EXIT_FROZEN__OWNER_STABILIZATION_ROUTE_DECISION_REQUIRED`

Accepted terminal:

`DLH_5VJ_BOUNDARY_HJB_IMPLEMENTATION_PARTIAL__ONE_BOUNDED_NUMERICAL_OR_CONTRACT_GAP_REMAINS`

### 7.1 Accepted implementation evidence

- new boundary-HJB selected-Q implementation is materially accepted;
- Gate 1A common-input F0 local regression passes;
- Gate 2 classifier / sector / representability / first-moment algebra passes;
- first-iteration selected backward Q is conservative and deterministic;
- on the frozen Gate-3 validation instance, iteration 1 remains inside the positive-liquid-marginal effective domain and has `max|Q1|≈7.11e-15`;
- iteration 2 deterministically reaches F3 `(13,13)`, `z=0`, with `p_b≈-0.365224`;
- the corrected implementation raises `DERIVATIVE_EFFECTIVE_DOMAIN_FAILURE` before raw candidate/bracket search;
- no final Bellman residual is available because convergence is not reached.

### 7.2 Scientific interpretation

The failure is not a household-HJB equation error, finite-domain geometry contradiction, or F3 sector-algebra contradiction. It is a concrete production-iteration manifestation of the Issue #56 Outcome-B convergence-application block:

> the pseudo-time / policy-update iteration leaves the accepted `p_b>0` effective domain before HJB convergence.

The previously observed unbounded R_DEPLETE Bellman score is the consequence of the invalid effective-domain iterate, not a small search-bracket root cause.

### 7.3 Next route decision — PENDING, no successor yet

The next scientific gate should investigate an **effective-domain-preserving / invariant-region HJB numerical stabilization route** before SCC/global-Q/KFE work.

Potential method classes include damping, pseudo-time-step control, continuation/safeguarded policy iteration, or another monotonicity/effective-domain-preserving construction. These are research candidates only; none is yet authorized, and no method may be selected by silent tuning-to-pass.

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
effective-domain-preserving HJB stabilization route          OWNER / REVIEWER DECISION PENDING
same-process Q global validation + SCC diagnostics            BLOCKED UNTIL HJB STABILIZATION
nested Wmax / resolution robustness                          BLOCKED UNTIL HJB STABILIZATION
conservative stationary-generator validation                 BLOCKED UNTIL HJB STABILIZATION
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

**NO ACTIVE BUILDER ISSUE.** Builder STOP remains binding until Owner / ChatGPT authorizes a successor route.

Current governance pointers:

- `tasks/TASK_INDEX_CURRENT.md`
- `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
- Issue #58 body/comments.

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.
