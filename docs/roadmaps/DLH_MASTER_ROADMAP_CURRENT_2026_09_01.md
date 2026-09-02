# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.13  
**Date:** 2026-09-02  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** CURRENT OWNER-DECISION CHECKPOINT — NO ACTIVE BUILDER ISSUE

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

- Git blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`
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
- Design R and Design W remain unfrozen under Owner decision
  `ACCEPT_RECOMMENDATION_U__DO_NOT_FREEZE_R_OR_W_YET`;
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

Accepted verdict:

`DLH_5O_REV2_ACCEPTED__OUTCOME_B_SUPPORTED__P2_COEFFICIENT_AND_INWARD_SIGN_VALID_ONLY_UNDER_EXPLICIT_DERIVATIVE_CONTROL__ANALYTIC_MODEL_SPECIFICATION_OWNER_DECISION_REQUIRED`

Accepted terminal:

`DLH_5O_HJB_LIQUID_TAIL_DOMINANT_BALANCE_CONDITIONAL__MISSING_ANALYTIC_ASSUMPTIONS_IDENTIFIED`

Controlling interpretation:

1. The accepted MATLAB-faithful source is finite-grid HJB authority; it does not itself define an unbounded-positive-`b` HJB/transversality problem.
2. Conditional asymptotic analysis must use the combined transfer Hamiltonian

   ```text
   V_b * [d*(V_a/V_b - 1) - chi(d,a)]
   ```

   rather than adjustment cost alone.
3. Under a source-faithful smooth-continuum interior HJB, the p=2 candidate may be analyzed only with explicit derivative control

   `P-TR: V_a/V_b = o(sqrt(b))` uniformly.

4. Under the complete conditional premise set, the leading coefficient equation is

   ```text
   (rho+r_b)K - 2*sqrt(K) = S*K.
   ```

   For the frozen symmetric productivity-switch block:

   ```text
   K = 4/(rho+r_b)^2,
   c/b = (rho+r_b)/2 = 0.0175.
   ```

5. Since `r_b=0.015`, the conditional candidate implies

   ```text
   mu_W/b -> -0.0025 < 0,
   ```

   i.e. fixed-a liquid-tail inwardness **conditional on the analytic assumptions and P-TR**.
6. This is not an unconditional theorem, not a full two-asset infinite-domain theorem, and not a domain choice.
7. The critical regime

   `V_a/V_b ~ Theta(sqrt(b))`

   remains unresolved because its transfer Hamiltonian is the same `O(1/b)` order and changes the coefficient system.
8. Reviewer comment `5504453148` supersedes two local shorthand statements:
   - P-TR alone yields sub-root/sublinear transfer-cost orders; `O(1)` transfer orders require the stronger `V_a/V_b=O(1)` subcase.
   - local p<1 exponent shorthand is not controlling; the corrected reviewer order comparison governs downstream use.

---

## 2. Current checkpoint — Owner decision before analytic-model specification

There is **no active Builder Issue**.

DLH-5O identifies the next scientific obstacle as model-defining rather than numerical:

> What continuous/unbounded-positive-`b` HJB problem, admissibility/transversality condition, regularity class and derivative-control regime should become analytic authority for proving or falsifying the conditional p=2 tail candidate?

This cannot be silently inferred from the finite-grid MATLAB boundary closure and cannot be supplied by Builder or ChatGPT without Owner scientific approval.

### Proposed next route — analytic-model specification gate

If Owner approves continuation on this route, the next Issue should be a design/specification gate, not implementation and not numerical execution. It should define or adjudicate at minimum:

1. **Analytic state-space authority** — fixed `a in [0,10]`, unbounded positive `b`, accepted productivity Markov states; explicit statement that this remains a fixed-a liquid-tail analytical extension, not a full two-asset infinite-domain model.
2. **Interior HJB authority** — exact continuous HJB equation corresponding to accepted household economics, with transfer/adjustment-cost coupling represented jointly.
3. **Admissibility / asymptotic boundary / transversality conditions** — what selects the economically relevant value solution without importing the finite-grid `b_max` closure.
4. **Regularity and uniformity** — differentiability, asymptotic expansion legitimacy, cross-z uniformity and any required domination/equicontinuity conditions.
5. **Derivative-control class** — whether P-TR (`V_a/V_b=o(sqrt(b))`) is assumed as an admissibility condition, derived from a stronger property, or rejected as too restrictive.
6. **Critical-transfer branch** — explicit analysis of `V_a/V_b~Theta(sqrt(b))`, whose transfer Hamiltonian changes the O(1/b) coefficient system.
7. **Theorem/falsification contract** — precise conditions under which the p=2 coefficient `c/b=0.0175` is accepted, rejected or remains conditional.
8. **Return path to domain design** — only after analytic tail authority is accepted may R/W domain design be reconsidered; no automatic W selection.

### Owner decision options

- **Approve analytic-model specification route:** publish a separate theory/design Issue after exact task drafting and activation.
- **Do not approve yet:** keep the project at this checkpoint and seek additional theory/economic review before any new authority.
- **Redirect:** Owner may choose a different scientific route; any such route must be published explicitly before Builder work.

No successor Issue is active until Owner decision.

---

## 3. Stationary household revalidation remains blocked

Stationary KFE remains NOT AUTHORIZED.

Only after a state-domain/boundary controlled process is selected, implemented, boundary-validated and shown to generate a conservative same-process KFE may the project re-enter Issue #27:

- recurrent-class/nullspace evidence;
- pin admissibility and valid-pin invariance;
- ORIGINAL `Q^T g` residual;
- mass/non-negativity;
- stationary-tail diagnostics;
- recompute `C,L,A,B` and the two-region anchor from scratch.

No historical aggregate is grandfathered.

---

## 4. Regional / Deep Learning sequence remains deferred

Permanent hierarchy:

```text
2-region unit fixture
-> 3–5 province integration fixture
-> 31-province empirical/source benchmark
```

`31_PROVINCE_HOUSEHOLD_UPPER_DOMAIN_AUDIT` remains deferred. No neural training is authorized until household boundary/stationary validation is usable.

---

## 5. Scientific ceiling at the current checkpoint

Until Owner decision and successor activation, do not:

- mutate accepted HJB/KFE/regional source;
- mutate taper, transfer FOC, adjustment cost, economics, prices or calibration;
- choose/implement R, W, W1, W2 or `W_max`;
- create new `b_max`/`a_max` or extrapolate the accepted taper beyond `a_max=10`;
- run/extend HJB grids or previous numerical fixtures;
- run stationary KFE/density/tail/aggregates;
- implement any boundary KKT law;
- run regional GE, multi-province audit, network training, nominal HANK, policy/welfare or Results.

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.
