# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.20  
**Date:** 2026-09-02  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** CURRENT OWNER-APPROVED SCIENTIFIC ROUTE — DLH-5S ANALYTIC ASYMPTOTIC-REALIZATION ACTIVE

---

## 0. Long-run objective

Build a data-to-structural-model calibration and regional-network HANK platform in which household HJB/KFE, aggregation, firm/accounting blocks and later nominal-HANK equations remain explicit structural economics, while difficult cross-regional mappings become interpretable learned modules only after household and equilibrium foundations pass scientific and numerical validation.

The first learned object remains the regional labor/spatial rule. Capital-network learning and nominal-HANK integration remain later stages.

---

## 1. Accepted household foundation through DLH-5R

Accepted MATLAB-faithful household source:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb337f1b02b3fe33c51e`

Binding Issue #27 law:

```text
HJB boundary policy <=> KFE boundary transition law
```

Stationary KFE remains NOT AUTHORIZED until a controlled household domain/boundary process is separately selected, implemented and validated.

R/W domain designs remain unfrozen. `W=a+b` remains an accounting coordinate, not production-domain authority. No `W_max` is authorized.

### Accepted analytic tail sequence

DLH-5O conditional p=2 candidate:

```text
(rho+r_b)K - 2*sqrt(K) = S*K
K = 4/(rho+r_b)^2
c/b = 0.0175
mu_W/b -> -0.0025
```

DLH-5P preserved an out-of-S3 critical benchmark `R~Theta(sqrt(b))` on compact interior-a sets and showed tail specification was not unique without an additional analytic class.

Owner then selected provisional S3 + parallel falsification:

`PROVISIONAL_S3_ANALYTIC_CLASS__PARALLEL_FALSIFICATION_ROUTE_APPROVED`

Working class:

- S1 fixed-a-support continuous unbounded-positive-b analytic base;
- S2 `V_inf=0` provisional tail/boundary selection;
- primary S3 `R=V_a/V_b=O(1)` uniformly;
- P-TR `R=o(sqrt(b))` sensitivity only;
- critical `R~Theta(sqrt(b))` retained outside S3 as an exclusion-cost/falsification benchmark.

### Accepted DLH-5Q / Issue #43

Accepted terminal:

`DLH_5Q_PROVISIONAL_S3_THEOREM_NOT_CLOSED__MISSING_EXISTENCE_COMPARISON_OR_ASYMPTOTIC_REALIZATION_IDENTIFIED__FALSIFICATION_PROTOCOL_READY`

Controlling interpretation:

1. continuous unbounded-b existence/comparison remains unproved;
2. among correctly analyzed power and explicit slow families inside S3, p=2 is the unique self-consistent formal balance;
3. broader non-power/exotic and monotone-preserving oscillatory regimes remain open;
4. p=2 coefficient/drift results are conditional on actual realization and derivative-remainder control;
5. full `[0,10]` endpoint authority remains absent.

### Accepted DLH-5R / Issue #44

Accepted candidate:

`6b79b7b1ff388174b5460a32de547a25ecb8a097`

Reviewer acceptance:

`5510368753`

Acceptance integration:

`96f0adb855233da06e96b71c6d8b6fe6aa540fc7`

Accepted verdict:

`DLH_5R_REV2_ACCEPTED__OUTCOME_C_CONFIRMED__S3_DERIVATIVE_CONTROL_NUMERICALLY_COMPATIBLE_ON_ACCESSIBLE_RANGE__P2_ASYMPTOTIC_REALIZATION_NOT_REACHED__FINITE_TRUNCATION_ASYMPTOTIC_REACH_REMAINS`

Accepted terminal:

`DLH_5R_HJB_TAIL_NUMERICAL_FALSIFICATION_INCONCLUSIVE__BOUNDARY_RESOLUTION_OR_SEMANTIC_SENSITIVITY_REMAINS`

Accepted numerical pattern:

```text
                 W1       W2       W3       W4 descriptive
slope          -0.559   -0.681   -0.758   -0.832
b^2 V_b         315      485      610      736
c/b            0.0564   0.0454   0.0405   0.0369
|R|/sqrt(b)    0.212    0.182    0.166    0.154
chi/b          0.00079  0.00058  0.00049  0.00040
mu_W/b        -0.0100  -0.0083  -0.0074  -0.0067
```

Accepted interpretation:

- accessible-range S3 derivative control is numerically compatible (`R=O(1)`, `R/sqrt(b)` and `chi/b` decline);
- the critical `R~sqrt(b)` / positive-`chi/b` benchmark is not observed;
- p=2 scaling is not reached at `b<=b160`;
- stable non-p2 asymptotic falsification is also not established;
- principal p2-facing observables move toward their conditional targets;
- the remaining numerical limitation is asymptotic reach at the pre-existing b160 hard ceiling, not cross-extent/resolution instability.

No larger numerical domain, production-domain choice, endpoint law or stationary KFE was authorized.

---

## 2. Owner route decision after DLH-5R — R-C1

Owner selected:

`APPROVE_R_C1_BOUNDED_ANALYTIC_ASYMPTOTIC_REALIZATION_CLOSURE__NO_NUMERICAL_DOMAIN_EXPANSION`

Owner-decision comment on Issue #44:

`5510675566`

Scientific rationale:

The numerical evidence has already ruled against the previously feared critical `R~sqrt(b)` signature on the accessible range and shown excellent local cross-grid stability. The unresolved object is not another finite-grid consistency check; it is whether the accepted HJB admits a long pre-asymptotic transition that eventually enters the p=2 attractor, and which non-circular assumptions are required to prove that statement.

This route deliberately does not reopen the b160 ceiling.

---

## 3. Immediate active gate — DLH-5S / Issue #45

### Name

**Provisional-S3 Pre-Asymptotic Dynamics and p=2 Realization**

Task type:

`SCIENTIFIC_THEORY_ANALYSIS__PROVISIONAL_S3_PREASYMPTOTIC_DYNAMICS_AND_P2_REALIZATION`

Dedicated branch:

`dsh/issue-45-dlh-5s-scaled-tail-p2-realization-2026-09-02`

### Core transformed variables

DLH-5S analyzes the continuous interior HJB using, at minimum,

```text
H(b,a,z) = -b V(b,a,z)
Q(b,a,z) = b^2 V_b(b,a,z)
s = log b
```

with exact kinematic identities to be audited:

```text
dH/ds = H-Q
c/b = Q^(-1/2)
p_eff = 2 - dlog(Q)/dlog(b)
```

and an exact scaled HJB decomposition of the form

```text
(rho I - S)H = 2 sqrt(Q) - r_b Q + E(b,a,z),
```

where every remainder component/sign must be derived from the accepted HJB rather than assumed.

### Scalar reduced comparison system

DLH-5S must fully analyze

```text
rho H = 2 sqrt(Q) - r_b Q,
dH/ds = H-Q,
```

including both algebraic branches, turning points, the p=2 fixed point

```text
H*=Q*=K*=4/(rho+r_b)^2 = 3265.3061224489797,
```

its local stability and basin/trapping restrictions, and the candidate reduced Q-flow

```text
dQ/ds = Q [2-(rho+r_b)sqrt(Q)]/[1-r_b sqrt(Q)]
```

which must be verified rather than presumed.

### Coupled and theorem-quality analysis

DLH-5S then restores the two-state Markov switching structure and analyzes mean/difference modes around the p=2 candidate. It must determine whether z-differences are damped and whether a coefficient-synchronization/nonresonance assumption is needed.

The main theorem attempt asks whether S1+S2+S3 can themselves establish:

- bounded/precompact scaled H,Q;
- eventual lower-branch selection;
- normalized remainder smallness/asymptotic autonomy;
- exclusion of persistent exotic forcing;
- convergence to the p=2 fixed point.

If not, the task must identify the sharpest non-circular missing condition rather than importing `Q->K` or `V_b~K/b^2` as an assumption.

### Relation to DLH-5R evidence

DLH-5R medians are read-only scalar evidence. DLH-5S may use them only to interpret why an increasing `Q` corresponds to decreasing `c/b` and an effective exponent below 2, and whether the observed direction is qualitatively compatible with the reduced lower-branch attractor picture. Finite-window compatibility is not theorem proof.

---

## 4. DLH-5S possible outcomes

### S-A — reduced/coupled attractor picture materially sharpens analytic closure

`DLH_5S_SCALED_TAIL_DYNAMICS_SUPPORT_P2_ATTRACTOR__MINIMAL_NONCIRCULAR_REALIZATION_ASSUMPTIONS_IDENTIFIED__NO_NUMERICAL_EXPANSION_NEEDED`

### S-B — transformed dynamics help but scaled-tail tightness/branch selection remains unproved

`DLH_5S_P2_REALIZATION_NOT_CLOSED__SCALED_TAIL_TIGHTNESS_OR_BRANCH_SELECTION_REMAINS_UNPROVED__OWNER_ROUTE_DECISION_REQUIRED`

### S-C — genuine analytic obstruction

`DLH_5S_SCALED_TAIL_DYNAMICS_REVEAL_P2_OR_PROVISIONAL_S3_OBSTRUCTION__OWNER_MODEL_REDEFINITION_REQUIRED`

### S-D — compact-interior closure achieved; only endpoints remain

`DLH_5S_INTERIOR_P2_REALIZATION_SUPPORTED__FULL_SUPPORT_ENDPOINT_AUTHORITY_REMAINS_OWNER_DECISION`

No outcome authorizes production-domain implementation or stationary KFE.

---

## 5. Household route after adequate analytic tail authority

The downstream sequence remains:

```text
accepted analytic authority / adequate falsification evidence
-> return to R/W domain-design decision
-> separate boundary-law implementation authority
-> HJB boundary validation
-> truncation/resolution robustness
-> conservative same-process generator
-> Issue #27 stationary KFE validation
-> recurrent-class / nullspace / pin / original Q^T g residual
-> mass / non-negativity / stationary-tail diagnostics
-> recompute C,L,A,B
-> rebuild two-region anchor
```

No historical aggregate is grandfathered.

---

## 6. Regional / Deep Learning sequence remains deferred

Permanent hierarchy:

```text
2-region unit fixture
-> 3–5 province integration fixture
-> 31-province empirical/source benchmark
```

Regional GE, learned regional labor/spatial rules, capital-network learning, nominal HANK, calibration, policy and welfare remain deferred until the household controlled process and stationary foundation are accepted.

---

## 7. Scientific ceiling during DLH-5S

Do not:

- mutate accepted HJB/KFE/regional source or household economics;
- run new HJB/grid/resolution experiments or rerun J0-J5 as new evidence;
- reopen b160 or create b180/b200;
- change b_lo, db, a_max, a-resolution or taper;
- choose/implement R/W/W1/W2 or `W_max`;
- invent/implement endpoint KKT/state-domain law;
- run stationary KFE/nullspace/pin/density/tail mass/aggregates;
- run regional GE, multi-province audit, network training, nominal HANK, calibration, policy/welfare or Results.

DLH-5S is analytic theory work only.

---

## 8. Governance status

Issue #45 / DLH-5S is the current intended Builder theory task. Builder authority requires synchronized Task Index / Startup Snapshot plus authoritative activation comment.

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.
