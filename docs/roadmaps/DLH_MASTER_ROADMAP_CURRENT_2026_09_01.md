# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.18  
**Date:** 2026-09-02  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** CURRENT OWNER-APPROVED SCIENTIFIC ROUTE — DLH-5R HJB-ONLY NUMERICAL FALSIFICATION ACTIVE

---

## 0. Long-run objective

Build a data-to-structural-model calibration and regional-network HANK platform in which household HJB/KFE, aggregation, firm/accounting blocks and later nominal-HANK equations remain explicit structural economics, while difficult cross-regional mappings become interpretable learned modules only after household and equilibrium foundations pass scientific and numerical validation.

The first learned object remains the regional labor/spatial rule. Capital-network learning and nominal-HANK integration remain later stages.

---

## 1. Accepted household foundation through DLH-5Q

Accepted MATLAB-faithful source:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb337f1b02b3fe33c51e`

The source remains finite-grid numerical authority.

Binding Issue #27 law:

```text
HJB boundary policy <=> KFE boundary transition law
```

Stationary KFE remains NOT AUTHORIZED until a controlled household domain/boundary process is separately selected, implemented and validated.

R/W domain designs remain unfrozen. `W=a+b` remains an accounting coordinate, not production-domain authority. No `W_max` is authorized.

### Accepted tail-theory sequence

DLH-5O conditional p=2 / derivative-control candidate:

```text
(rho+r_b)K - 2*sqrt(K) = S*K
K = 4/(rho+r_b)^2
c/b = 0.0175
mu_W/b -> -0.0025
```

DLH-5P established that the critical out-of-S3 formal branch `R~Theta(sqrt(b))` can alter the tail coefficient on compact interior-a sets while the demonstrated family remains total-wealth inward.

Owner then selected provisional S3 + parallel falsification:

`PROVISIONAL_S3_ANALYTIC_CLASS__PARALLEL_FALSIFICATION_ROUTE_APPROVED`

Working class:

- S1 fixed-a-support continuous unbounded-positive-b analytic base;
- S2 `V_inf=0` provisional tail/boundary selection;
- primary S3 `R=V_a/V_b=O(1)` uniformly;
- P-TR `R=o(sqrt(b))` sensitivity only;
- critical `R~Theta(sqrt(b))` retained outside S3 as an exclusion-cost/falsification benchmark.

### Accepted DLH-5Q / Issue #43

Accepted candidate:

`dd39385b6cf4fcf8fed382d69683ab907747cfe3`

Reviewer acceptance:

`5507534903`

Acceptance integration:

`570d858aea3029e1a30c286b5c683a8efdb836bd`

Accepted terminal:

`DLH_5Q_PROVISIONAL_S3_THEOREM_NOT_CLOSED__MISSING_EXISTENCE_COMPARISON_OR_ASYMPTOTIC_REALIZATION_IDENTIFIED__FALSIFICATION_PROTOCOL_READY`

Controlling interpretation:

1. Existence/comparison for the continuous unbounded-b first-order regime-switching HJB is NOT ESTABLISHED.
2. Among correctly analyzed power/explicit slow families inside S3, p=2 is the unique self-consistent formal balance.
3. Broader exotic/non-power and monotone-preserving oscillatory tails remain open.
4. Conditional on actual p=2 realization plus the accepted derivative-remainder contract (E), the coefficient/drift targets above follow.
5. No in-class counterexample was found among the correctly analyzed families, but this is not an exhaustive theorem.
6. Full `[0,10]` endpoint authority remains absent.
7. The numerical falsification protocol is accepted as design only and was not executed under DLH-5Q.

Reviewer execution annotations:

- numerical `R_hat` must use raw accepted value gradients consistent with the transfer FOC;
- consumption/labor derivative floors must not silently redefine `R_hat`;
- floor activation is numerical-semantic evidence;
- any truncation-sensitivity variants require explicit Issue authority.

---

## 2. Owner route decision after DLH-5Q — Q-B2

Owner selected:

`APPROVE_Q_B2_HJB_ONLY_NUMERICAL_FALSIFICATION__NO_KFE`

Owner-decision comment on Issue #43:

`5507666206`

Scientific rationale:

Before investing further in difficult infinite-domain existence/comparison work, test whether the accepted finite-grid household HJB solution actually exhibits a stable interior signature compatible with provisional S3 / p=2. If the finite-grid evidence instead shows a robust critical-type or non-p=2 signature, return to Owner model-definition review rather than proving a class that the realized model does not approach.

This is a bounded falsification experiment, not production-domain selection.

---

## 3. Immediate active gate — DLH-5R / Issue #44

### Name

**HJB-Only Provisional-S3 Liquid-Tail Numerical Falsification**

Task type:

`SCIENTIFIC_NUMERICAL_FALSIFICATION__PROVISIONAL_S3_HJB_TAIL_DIAGNOSTIC`

Dedicated branch:

`dsh/issue-44-dlh-5r-hjb-tail-falsification-2026-09-02`

### Exact numerical authority

Reuse only the mature pre-existing DLH-5J grids from:

`configs/dlh_5j_final_coupled_b_extent_diagnostic.toml`

Fresh HJB-only runs authorized:

```text
J0_A77_B120
J1_A77_B140
J2_A77_B160
J3_A153_B120
J4_A153_B140
J5_A153_B160
```

Frozen:

```text
a in [0,10]
a_max = 10
b_lo = -2
db = 7/19
b_hi in {795/19, 935/19, 1075/19}
```

`b160` remains the hard route ceiling.

No b180/b200, no new b_lo, no new a extent, no b-resolution change, no adaptive seventh grid.

### Primary observables

- raw transfer-FOC-consistent `V_a`, `V_b`, and `R=V_a/V_b`;
- `R/sqrt(b)`;
- `b^2 V_b`;
- accepted `c/b`;
- transfer `d/sqrt(b)`;
- adjustment cost `chi/b`;
- `mu_W/b`;
- derivative-floor activation;
- log-log scaling slope;
- b-extent and a-resolution stability.

### Frozen primary windows

```text
W1_COMMON      = [20,35]
W2_COMMON_HIGH = (35,40]
W3_EXTENDED    = [42,48]   # b140/b160
W4_B160_ONLY   = [50,55]   # descriptive only
```

Primary interior-a evidence excludes `a=0` and top two a77 coarse layers; a77/a153 comparisons use aligned nodes. `a=0` is reported separately; `a=10` is not primary theorem evidence.

### Scientific outcomes

Possible terminals:

- numerical evidence supports provisional S3/p=2, while analytic theorem remains open;
- stable multi-grid evidence falsifies promotion of S3 as the realized model and returns to Owner redefinition;
- evidence is inconclusive because of boundary/resolution/semantic sensitivity;
- raw-gradient provenance or required HJB execution is blocked.

A numerical support result does NOT prove existence/comparison or promote the theorem automatically.

---

## 4. Route after DLH-5R

### Route R-A — numerical support for provisional S3 / p=2

Do not call the theorem proved. Owner chooses between:

- return to bounded analytic existence/comparison/asymptotic-realization closure with stronger empirical motivation;
- or, if evidence is sufficiently robust, consider a separate analytic-authority/domain-design decision gate.

No automatic R/W implementation.

### Route R-B — stable falsification of S3 promotion

Return immediately to Owner model-definition review. Re-open the critical/exotic tail route or revise the admissibility class. Do not continue domain design under S3.

### Route R-C — inconclusive

Resolve the identified numerical-semantic or truncation/resolution blocker in a separate bounded gate. Do not search for a PASS by uncontrolled grid expansion.

### Blocked

Resolve raw-gradient provenance or scientific execution validity before interpretation.

No route bypasses HJB/KFE same-controlled-process validation.

---

## 5. Household route after adequate analytic/numerical tail evidence

Downstream sequence remains:

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

## 7. Scientific ceiling during DLH-5R

Do not:

- mutate accepted HJB/KFE/regional source or household economics;
- create any new b extent beyond existing b160, new b_lo, new a_max, or new b resolution;
- choose/implement R/W/W1/W2 or `W_max`;
- implement endpoint KKT/state-domain law;
- run stationary KFE/nullspace/pin/density/tail mass/aggregates;
- run regional GE, multi-province audit, network training, nominal HANK, calibration, policy/welfare or Results.

DLH-5R is HJB-only numerical falsification.

---

## 8. Governance status

Issue #44 / DLH-5R is the current intended Builder numerical-diagnostic task. Builder authority requires synchronized Task Index / Startup Snapshot plus authoritative activation comment.

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.
