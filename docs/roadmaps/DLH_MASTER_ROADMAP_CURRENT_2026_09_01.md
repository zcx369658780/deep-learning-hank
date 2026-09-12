# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.43  
**Date:** 2026-09-12  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** DLH-5V-I / ISSUE #57 ACTIVE — BOUNDARY-HJB PRODUCTION-SCHEME DESIGN

---

## 0. Long-run objective

Build a hybrid structural–learned regional HANK platform in which household HJB/KFE, aggregation, firm/accounting and later nominal-HANK equations remain explicit structural economics, while hard-to-specify cross-regional mappings become learned modules only after household and equilibrium foundations pass scientific and numerical validation.

The first learned object remains regional labor/spatial mapping `W^L`. Neural training remains downstream.

---

## 1. Accepted household / finite-domain foundation

Accepted household source:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Accepted finite production-domain family:

```text
D_W(W_max)={0<=a<=a_max,b>=b_min,a+b<=W_max}
a_max=10
b_min=-2
```

No numerical production `W_max` is selected.

Binding law:

```text
HJB boundary policy <=> KFE boundary transition law
```

Restricted-Voronoi cells remain the accepted state partition / mass-volume geometry unless a later Owner-authorized route changes them. The same selected backward generator `Q` must define future forward mass dynamics `p_dot=Q^T p`.

Stationary KFE remains **NOT AUTHORIZED**.

---

## 2. Accepted regular finite-process block — DLH-5V-A through DLH-5V-E

Base native grid:

```text
da=10/19
db=7/19
10j+7i<=N
```

Accepted common regular W-active region at m=1:

```text
7<=j<=12
i>=10
```

Accepted sector coverage:

```text
T_W={mu_W<=0}=T_realloc union R_reverse union R_deplete
```

with exact tangent moves

```text
w_T=(-70/19,+70/19)
w_RT=(+70/19,-70/19)
```

and local inward moves

```text
w_left=(-10/19,0)
w_down=(0,-7/19).
```

Candidate semantics remain frozen:

```text
continuous admissibility
 -> candidate-specific represented nonnegative rates
 -> discrete H_h score BEFORE selection
 -> ONE global statewise argmax
 -> selected rates
 -> ONE conservative backward Q
 -> future KFE consumes exactly Q^T
```

---

## 3. Issue #54 / DLH-5V-F — exact endpoint finite-process obstruction — ACCEPTED

Accepted candidate: `b9dab7b6cf5d724074765ddb88d6f300175f6c6f`

Reviewer acceptance: `5633995486`

Acceptance integration: `4e77d9c753f81eb2517a8b90a0827db6af8faed4`

Accepted verdict:

`DLH_5VF_ACCEPTED__OUTCOME_C_CONFIRMED__EXACT_ENDPOINT_FINITE_PROCESS_REPRESENTABILITY_OBSTRUCTION_FROZEN__OWNER_APPROXIMATION_ROUTE_DECISION_REQUIRED`

The finite-m native-lattice obstruction remains a true discretization fact. It is not a household-source or KFE repair issue.

---

## 4. Issue #55 / DLH-5V-G — Route A strong raw graph target — OUTCOME C ACCEPTED

Accepted candidate: `15f2f81653a847344d2cd647705487cc893af1d7`

Reviewer acceptance: `5635802416`

Acceptance integration: `8dd5e9c444d7356736f28a29b9ffe492bbe81caa`

Accepted verdict:

`DLH_5VG_ACCEPTED__OUTCOME_C_CONFIRMED__ROUTE_A_TANGENT_CONE_GRAPH_CONSISTENCY_OBSTRUCTION_FROZEN__OWNER_ROUTE_REDECISION_REQUIRED`

Accepted terminal:

`DLH_5VG_ROUTE_A_ASYMPTOTIC_ENDPOINT_APPROXIMATION_OBSTRUCTION__OWNER_ROUTE_REDECISION_REQUIRED`

Issue #55 proved failure of its strong raw admitted-drift-set graph target. That mathematical fact remains accepted provenance.

---

## 5. Issue #56 / DLH-5V-H — state-constraint consistency-target audit — OUTCOME B ACCEPTED

Accepted candidate / integration:

`55e29523e6f1bfefab270c05113984af003ea44b`

Reviewer acceptance:

`5644186157`

Acceptance-integration / Owner route-decision comment:

`5644340159`

Accepted verdict:

`DLH_5VH_ACCEPTED__OUTCOME_B_CONFIRMED__UNBOUNDED_CONTROL_NUMERICAL_SCHEME_AND_STATE_CONSTRAINT_CONVERGENCE_APPLICATION_BLOCK_FROZEN`

Accepted terminal:

`DLH_5VH_THEORY_AUDIT_PARTIAL__ONE_BOUNDED_BOUNDARY_CONSISTENCY_OR_COMPARISON_GAP_REMAINS`

Accepted scientific result:

- the legitimate boundary-consistency route is operator/test-function based, with the transformed Soner one-sided state-constraint orientation;
- Issue #55's raw graph target is stronger than the local operator-consistency machinery itself requires;
- on effective-domain smooth tests (`p_b>0`) the frozen process is not refuted at design level;
- discrete smooth-test optimizer localization, max-level Taylor consistency and boundary restriction/recovery are established locally;
- one bounded **UNBOUNDED-CONTROL NUMERICAL-SCHEME / STATE-CONSTRAINT CONVERGENCE-APPLICATION BLOCK** remains: global finite-m solution stability/existence, production fixed-point theory, global Bellman finiteness/effective-gradient restriction, and exact Soner/CDL comparison mapping.

This block is explicit and frozen. It is not silently solved.

---

## 6. Owner Route B decision — proceed without making a complete analytic convergence theorem a prerequisite

Owner approved:

`APPROVE_ROUTE_B_FREEZE_OUTCOME_B_THEORY_LIMIT_AND_PROCEED_TO_BOUNDARY_HJB_SCHEME_DESIGN`

Scientific interpretation:

- Kaplan-style / two-asset HA HJBs are numerical nonlinear fixed-point/PDE objects; no closed-form value function is required;
- future implementation acceptance is numerical: iterative convergence to declared tolerance + residual + policy/drift + regression + robustness evidence;
- Owner empirical experience that convergence is often available around `r_b=0.02` and roughly `0.05<r_a<0.12` is non-binding diagnostic guidance only, not calibration authority or an acceptance interval;
- the Issue #56 theory limitation remains visible in all downstream interpretation.

---

## 7. DLH-5V-I / Issue #57 — ACTIVE DESIGN GATE

Title:

`DLH-5V-I: Freeze boundary-HJB production scheme contract under accepted Outcome-B theory ceiling`

Task type:

`SCIENTIFIC_DESIGN__BOUNDARY_HJB_SCHEME_CONTRACT_AND_IMPLEMENTATION_READINESS`

Owner decision:

`APPROVE_ROUTE_B_FREEZE_OUTCOME_B_THEORY_LIMIT_AND_PROCEED_TO_BOUNDARY_HJB_SCHEME_DESIGN`

Authority marker:

`DLH_5VI_BOUNDARY_HJB_SCHEME_DESIGN_AUTHORIZED`

Dedicated Builder branch:

`dsh/issue-57-dlh-5vi-boundary-hjb-scheme-design-2026-09-12`

Authoritative activation comment:

`5644365170`

Builder authority becomes operative only after the final activation-refresh comment confirms the post-ID-sync live main.

### 7.1 Design objective

Freeze an implementation-ready chain:

```text
represented state
 -> exhaustive state-family classifier
 -> true continuously admissible controls
 -> numerical search/bracket semantics
 -> represented destinations
 -> candidate-specific rates from LOCAL drift
 -> candidate H_h score
 -> ONE statewise selection
 -> selected control + selected rates
 -> conservative backward Q row
 -> implicit/pseudo-time HJB integration contract
 -> numerical convergence/residual/failure diagnostics
```

The design must preserve the true unbounded household control domain and distinguish economic admissibility from finite numerical optimizer brackets.

### 7.2 Key safeguards

- no optimize-then-clip;
- no artificial hard control bounds promoted into economics;
- no unavailable destination retained as diagonal escape;
- no KFE-only process;
- no normalization/pinning leakage repair;
- deterministic tie handling may choose among score-equal candidates but must not change represented drift/rates;
- accepted interior household source remains read-only in this gate;
- no analytic `V` is required; the next implementation gate will use numerical convergence evidence.

### 7.3 Design-only ceiling

Issue #57 may specify future smoke/regression/robustness tests, including diagnostic rate cases informed by Owner experience, but may not implement or execute production HJB/Q/KFE/stationary solves and may not select numerical production `W_max`.

---

## 8. Current roadmap position

```text
MATLAB-faithful two-asset household economics                 ACCEPTED
finite W-domain + continuous tangent/KKT law                 ACCEPTED
same-process HJB <=> KFE principle                           ACCEPTED
restricted-Voronoi state partition                           ACCEPTED
regular W-frontier phase / adjacency                         ACCEPTED
shared-face-only local process                               OBSTRUCTION ACCEPTED
regular exact-tangent wide-stencil process                   ACCEPTED
regular control-dependent rates / global scoring             ACCEPTED
endpoint exact finite-process closure                         OBSTRUCTION ACCEPTED — ISSUE #54
Route A strong raw graph target                               OBSTRUCTION ACCEPTED — ISSUE #55
state-constraint operator-consistency audit                   OUTCOME B ACCEPTED — ISSUE #56
boundary-HJB production-scheme design                         ACTIVE — ISSUE #57
boundary-HJB implementation + local HJB validation            PENDING
same-process Q validation + SCC diagnostics                  PENDING
nested Wmax / resolution robustness                          PENDING
conservative stationary-generator validation                 PENDING
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
same selected Q for HJB and future KFE
p=M g
p_dot=Q^T p
```

No route may use pinning/normalization to repair leakage or create a KFE-only process.

Stationary KFE remains explicitly blocked.

---

## 10. Interpretation ceiling

DLH-5V-I is design-only. It does not authorize solver/source mutation, production generator assembly/run, HJB/KFE/stationary computation, numerical production `W_max`, state augmentation, grid/aspect/domain redesign, coordinate transformation, aggregates, GE, multi-region, neural, nominal, calibration, policy, welfare or Results prose.

---

## 11. Current governance pointers

- `tasks/TASK_INDEX_CURRENT.md`
- `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
- Issue #57 body/comments.

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.
