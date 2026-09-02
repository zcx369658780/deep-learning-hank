# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.17  
**Date:** 2026-09-02  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** CURRENT OWNER-DECISION CHECKPOINT — DLH-5Q ACCEPTED / NO ACTIVE BUILDER ISSUE

---

## 0. Long-run objective

Build a data-to-structural-model calibration and regional-network HANK platform in which household HJB/KFE, aggregation, firm/accounting blocks and later nominal-HANK equations remain explicit structural economics, while difficult cross-regional mappings become interpretable learned modules only after household and equilibrium foundations pass scientific and numerical validation.

The first learned object remains the regional labor/spatial rule. Capital-network learning and nominal-HANK integration remain later stages.

---

## 1. Accepted household foundation through DLH-5Q

### Household source

Accepted MATLAB-faithful source:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb337f1b02b3fe33c51e`

The source remains finite-grid numerical authority. It does not itself create unbounded-liquid endpoint/transversality authority.

### HJB/KFE same-process contract

Binding law from Issue #27:

```text
HJB boundary policy <=> KFE boundary transition law
```

Stationary KFE remains NOT AUTHORIZED until the household controlled process, domain and boundary law are separately selected, implemented and validated.

### Accepted domain/tail theory before DLH-5Q

- R/W domain designs remain unfrozen.
- `W=a+b` is an accounting coordinate, not production-domain authority.
- No `W_max` is authorized.
- DLH-5N: source accounting alone does not determine the high-liquid-tail sign; value-gradient asymptotics are the missing object.
- DLH-5O: under the complete conditional p=2 / derivative-control premise set,

```text
(rho+r_b)K - 2*sqrt(K) = S*K
K = 4/(rho+r_b)^2
c/b = 0.0175
mu_W/b -> -0.0025
```

but this is a conditional dominant balance, not an unconditional theorem.
- DLH-5P: the critical out-of-S3 branch `R~Theta(sqrt(b))` remains a formal admissible benchmark on compact interior-a sets and can alter the consumption coefficient; the demonstrated family remains total-wealth inward.

### Owner provisional analytic choice after DLH-5P

Owner selected:

`PROVISIONAL_S3_ANALYTIC_CLASS__PARALLEL_FALSIFICATION_ROUTE_APPROVED`

Working class:

- S1 fixed-a-support continuous unbounded-positive-b analytic base;
- S2 `V_inf=0` provisional tail/boundary selection;
- primary S3 `R=V_a/V_b=O(1)` uniformly;
- P-TR `R=o(sqrt(b))` sensitivity only;
- critical `R~Theta(sqrt(b))` kept outside S3 as an exclusion-cost/falsification benchmark.

---

## 2. Accepted DLH-5Q / Issue #43

Accepted candidate:

`dd39385b6cf4fcf8fed382d69683ab907747cfe3`

Reviewer acceptance comment:

`5507534903`

Acceptance integration:

`570d858aea3029e1a30c286b5c683a8efdb836bd`

Accepted verdict:

`DLH_5Q_REV3_ACCEPTED__OUTCOME_B_CONFIRMED__PROVISIONAL_S3_SURVIVES_ANALYZED_FAMILIES__THEOREM_NOT_CLOSED__FALSIFICATION_PROTOCOL_READY`

Accepted terminal:

`DLH_5Q_PROVISIONAL_S3_THEOREM_NOT_CLOSED__MISSING_EXISTENCE_COMPARISON_OR_ASYMPTOTIC_REALIZATION_IDENTIFIED__FALSIFICATION_PROTOCOL_READY`

### Controlling scientific interpretation

1. **Existence / comparison:** NOT ESTABLISHED for the continuous unbounded-b first-order regime-switching HJB. `V_inf=0` is tail/boundary selection content, not gauge normalization or uniqueness theorem.
2. **Power-tail realization:** among correctly analyzed power families inside S3, p=2 is the unique self-consistent formal balance.
   - `1<p<2`: rho/r_b/S block dominates and `[rho+(p-1)r_b]K=S K`; the required positive eigenvalue is absent from `{0,-2/3}`.
   - `p>2`: consumption block dominates and is unbalanced.
   - `p<=1`/log violates S1 boundedness.
3. **Explicit slow families:** `b^-alpha` and `1/log b` examples are formally excluded by corrected order/switch-spectrum arguments, including the z-dependent `1/log b` equation `S A=rho A`.
4. **Non-exhaustive scope:** broader exotic/non-power and monotone-preserving oscillatory tails remain open under `ASYMPTOTIC_REALIZATION / NO-EXOTIC-REGIME`.
5. **Derivative-remainder contract:** the accepted conditional S3-compatible expansion is

```text
V   = -K(z)/b + H(a,z)/b^2 + r0
V_b =  K(z)/b^2 - 2H(a,z)/b^3 + r_b
V_a =  H_a(a,z)/b^2 + r_a
```

with uniform small-o controls. A nonzero a-derivative in a b^-3/2 coefficient would generate `R~sqrt(b)` and leave S3.
6. **Coefficient/drift:** conditional on actual p=2 realization, the derivative-remainder contract, no exotic regime and uniformity:

```text
(rho+r_b)K - 2*sqrt(K) = S*K
K = 4/(rho+r_b)^2       (z-constant candidate)
c/b -> 0.0175
mu_W/b -> -0.0025
```

These remain conditional, not theorem-level.
7. **Falsification search:** no S3-internal counterexample was found among the correctly analyzed families. This is not an exhaustive exclusion theorem.
8. **Endpoint scope:** full `[0,10]` theorem authority remains absent; `a=10` analytic law and continuous `b_lo` adoption remain model-defining decisions.
9. **Numerical falsification protocol:** accepted as design only; NOT executed.

### Reviewer execution annotations

Future numerical falsification must obey:

- measure analytic `R=V_a/V_b` with the raw accepted value gradients consistent with the transfer FOC; do not silently substitute the consumption/labor derivative floor into `R_hat`;
- treat activation of derivative floors in the tail as a numerical-semantic limitation / possible boundary artifact;
- any `b_max` / `b_lo` sensitivity variants require explicit future Owner/Issue authorization;
- “no in-class counterexample found” remains limited to the correctly analyzed families.

---

## 3. Current checkpoint after DLH-5Q

There is **no active Builder Issue**.

DLH-5Q returned Outcome B: provisional S3 has not been analytically falsified by the tested families, but the theorem is not closed because existence/comparison and actual asymptotic realization remain unresolved.

The current scientifically defensible next routes are:

### Q-B1 — continue analytic closure

Open a bounded theory gate targeting the first-order regime-switching HJB existence/comparison framework and/or a more rigorous asymptotic-realization argument. Do not import endpoint laws silently.

### Q-B2 — execute the parallel numerical falsification protocol

Open a separate Owner-authorized HJB-only diagnostic Issue. It may test raw `V_a/V_b`, `b^2V_b`, `c/b`, transfer/cost orders and boundary influence. Any bounded `b_max`/`b_lo` comparison variants must be explicitly authorized. No stationary KFE.

### Q-B3 — endpoint model-definition review

Resolve analytic `a=10` and continuous `b_lo` authority before any full-support theorem or domain implementation. This is model-defining and requires Owner choice.

No successor is automatically active at this checkpoint.

---

## 4. Household route after analytic closure

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

## 5. Regional / Deep Learning sequence remains deferred

Permanent hierarchy:

```text
2-region unit fixture
-> 3–5 province integration fixture
-> 31-province empirical/source benchmark
```

Only after the household controlled process and stationary foundation are accepted does the project resume regional GE, learned regional labor/spatial rules, later capital-network learning, nominal HANK, calibration, policy and welfare.

---

## 6. Scientific ceiling at the current checkpoint

Until the next Owner/route decision and successor activation, do not:

- mutate accepted HJB/KFE/regional source or household economics;
- choose/implement R/W/W1/W2 or `W_max`;
- choose new numerical `b_max`/`a_max`;
- run HJB/KFE/grid/stationary experiments;
- implement endpoint KKT/state-domain law;
- run regional GE, multi-province audit, network training, nominal HANK, calibration, policy/welfare or Results.

---

## 7. Governance status

Issue #43 / DLH-5Q is accepted and CLOSED completed.

Current governance status:

`NO_ACTIVE_BUILDER_ISSUE__DLH_5Q_ACCEPTED__NEXT_ROUTE_OWNER_DECISION_PENDING`

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.
