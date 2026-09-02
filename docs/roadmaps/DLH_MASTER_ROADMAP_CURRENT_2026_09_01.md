# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.12  
**Date:** 2026-09-02  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** CURRENT OWNER-APPROVED SCIENTIFIC ROUTE

---

## 0. Long-run objective

Build a data-to-structural-model calibration and regional-network HANK platform in which household HJB/KFE, aggregation, firm/accounting blocks and later nominal-HANK equations remain explicit structural economics, while difficult cross-regional mappings become interpretable learned modules only after household and equilibrium foundations pass scientific and numerical validation.

The first learned object remains the regional labor/spatial rule. Capital-network learning and nominal-HANK integration remain later stages.

---

## 1. Accepted household foundation through DLH-5N

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

Any eventual stationary density must satisfy the ORIGINAL `Q^T g=0`, mass/non-negativity, conservative-generator/recurrent-class/nullspace evidence, pin admissibility and valid-pin invariance before aggregates are accepted.

### Boundary/domain diagnostics — Issues #28–#36

Accepted findings:

- artificial upper asset bounds initially receive outward requests;
- liquid-extent expansion attenuates upper-b influence, but cross-a robustness fails through the hard b160 ceiling;
- refining the fixed physical `a` domain resolves upper-a but can reactivate upper-b, establishing coupled domain/resolution behavior;
- widening `a_max` is confounded by the accepted `a_max`-normalized illiquid-return taper;
- pure larger-grid PASS seeking is CLOSED.

### High-wealth mechanism — Issues #37–#38

Accepted evidence establishes, narrowly:

- positive high-wealth `mu_b` is largely a transfer/rebalancing phenomenon;
- the pre-frozen accepted high-wealth evidence set contains 105 states;
- all 44 material positive-`mu_b` states satisfy `mu_W=mu_a+mu_b<=0`;
- all 17 top-layer upper-b offenders satisfy `mu_a<=0` and `mu_W<=0` while violating rectangular `mu_b<=0`;
- the linear transfer term cancels one-for-one in `mu_W`, while adjustment cost remains;
- cross-a total-drift sensitivity remains material on 16/24 aligned pairs;
- this is finite-state/source-accounting evidence, not an infinite-domain theorem or stationary-tail proof.

### State-domain/KKT design review — Issue #39 / DLH-5M

Accepted candidate:

`80cdb7ab2c14bcb7606fc66a0737c28bd3fbb4bb`

Acceptance integration commit:

`69bde2115cdf038e40640ec41d23e0b620167539`

Owner scientific decision:

`ACCEPT_RECOMMENDATION_U__DO_NOT_FREEZE_R_OR_W_YET`

Controlling interpretation:

1. **Design R remains unfrozen.** A finite rectangular tangent-cone/KKT closure is mathematically coherent, but no accepted truncation-vanishing argument shows that the upper-b numerical closure has negligible interior influence as the truncation recedes.
2. **Design W remains unfrozen.** `W=a+b` is an accepted source-accounting coordinate and an economically plausible truncation hypothesis, but finite-state inwardness, undefined `W_max`, cross-a sensitivity, representation choice and HJB↔KFE process matching are insufficient for a model freeze.
3. Maximization upper-constraint KKT convention is `L=H-lambda*g`; effective gradients are `V-lambda`.
4. At a W face, `lambda_W` cancels from the linear transfer contribution but survives through adjustment cost.
5. W-face activity is conditional on symbolic `W_max`; no accepted state is classified W-interior or W-boundary without a chosen cap.
6. The geometry-inconsistent shortcut “rectangle but use `mu_W<=0` instead of `mu_b<=0` at the corner” is rejected.
7. Stationary KFE remains NOT AUTHORIZED.

### Fixed-a liquid-tail total-drift asymptotics — Issue #40 / DLH-5N

Accepted candidate:

`bded30a8b8cb579c3f359a62f5b530d7c34b7526`

Acceptance integration commit:

`e23b1ada5f5ab1b11c1291d8141d8286884553d4`

Accepted reviewer verdict:

`DLH_5N_REV2_ACCEPTED__OUTCOME_B_SUPPORTED__FIXED_A_LIQUID_TAIL_SIGN_REMAINS_CONDITIONAL__HJB_VALUE_FUNCTION_TAIL_ASYMPTOTICS_NEXT_GATE_REQUIRED`

Accepted terminal:

`DLH_5N_FIXED_A_LIQUID_TAIL_TOTAL_WEALTH_SIGN_CONDITIONAL__MISSING_CONTROL_ASYMPTOTICS_IDENTIFIED`

Controlling interpretation:

1. With `a in [0,10]` fixed, current accepted authority does **not** establish `mu_W<0` for all sufficiently large positive `b`.
2. `r_b*b` is the only explicit positive linearly growing term whose source order/sign is fixed; the asymptotic order of the control-dependent remainder is not identified by current authority.
3. Conditional inwardness and outwardness can be stated only under explicit assumptions on the tail of `V_b`, `V_a/V_b`, labor and adjustment cost.
4. The formula-level outward family is not HJB-verified and therefore is not a model-level counterexample.
5. The result is a **fixed-a liquid-tail** statement only; it is not a full two-asset infinite-domain theorem.
6. Reviewer acceptance comment `5503274333` supersedes local over-strong biconditional shorthand in the Phase A/C audit; downstream tasks must use only the sufficient transfer-ratio implications required by accepted M2/M3.
7. R/W remain unfrozen; no `W_max`; stationary KFE remains NOT AUTHORIZED.

---

## 2. Immediate theory gate — DLH-5O / Issue #41

### Name

**Fixed-a Liquid-Tail HJB Value-Function Asymptotics**

Task type:

`SCIENTIFIC_THEORY_ANALYSIS__HJB_VALUE_FUNCTION_LIQUID_TAIL_SCALING`

### Purpose

DLH-5N identified the exact missing object: the HJB-implied liquid-tail scaling of the value function and value derivatives.

DLH-5O therefore asks:

> Does the accepted MATLAB-faithful HJB authority itself determine the asymptotic scaling of `V_b`, `V_a/V_b`, and cross-productivity value differences strongly enough to identify `c/b` and the sign of total-wealth drift as `b->+infinity` with `a in [0,10]` fixed?

The candidate CRRA-2 balance

```text
V_b ~ K(a,z)/b^2
V ~ V_inf(a,z) - K(a,z)/b
c ~ b/sqrt(K)
```

is a hypothesis to be derived, rejected or left conditional — not an accepted premise.

### Required logic

DLH-5O must:

1. audit the exact converged HJB fixed-point authority in the accepted source;
2. distinguish finite-grid MATLAB numerical semantics from any derivable continuous interior HJB identity;
3. determine whether the accepted authority actually specifies an unbounded-`b` analytical HJB problem or asymptotic boundary/transversality condition;
4. compare `p<2`, `p=2`, `p>2` candidate balances jointly with transfer, adjustment cost, labor and productivity switching;
5. if authorized, derive the full `p=2` coefficient system for `V_inf(a,z)` and `K(a,z)`, retaining every same-order term;
6. test whether bounded/sub-root `V_a/V_b` and productivity-switch behavior are consequences of the candidate expansion or merely assumptions;
7. classify theorem / conditional theorem / HJB-consistent alternative / accepted-authority insufficiency;
8. translate the result narrowly back to DLH-5N without choosing a domain.

A simple tail consumption ratio, including any expression resembling `(rho+r_b)/2`, may be reported only if derived from the accepted HJB balance after all same-order terms are accounted for. No textbook representative-agent shortcut may be imported as authority.

### Exact terminals

Use exactly one:

- `DLH_5O_HJB_FIXED_A_LIQUID_TAIL_SCALING_DERIVED__CONSUMPTION_RATIO_AND_TOTAL_DRIFT_SIGN_RESOLVED`
- `DLH_5O_HJB_LIQUID_TAIL_DOMINANT_BALANCE_CONDITIONAL__MISSING_ANALYTIC_ASSUMPTIONS_IDENTIFIED`
- `DLH_5O_ACCEPTED_HJB_AUTHORITY_INSUFFICIENT_FOR_UNBOUNDED_LIQUID_TAIL_THEOREM__ANALYTIC_MODEL_SPECIFICATION_REQUIRED`
- `DLH_5O_HJB_CONSISTENT_NONINWARD_LIQUID_TAIL_REGIME_ESTABLISHED__W_DIRECTION_WEAKENED`
- `BLOCKED_DLH_5O_ACCEPTED_HJB_SOURCE_OR_EQUATION_AUTHORITY_INCONSISTENCY`

No terminal freezes R/W or authorizes implementation.

---

## 3. Decision tree after DLH-5O

### Route O-A — HJB scaling/sign resolved

Return to the domain-design question with a genuine fixed-a liquid-tail theorem as new evidence. Still do not immediately implement W: the finite `a_max=10` support/taper, truncation geometry, representation and HJB↔KFE same-process requirements remain separate gates.

### Route O-B — dominant balance conditional

Do not patch code or choose a domain. Freeze the exact missing analytic assumptions and decide whether they can be proved from a strengthened analytic HJB specification.

### Route O-C — accepted HJB authority insufficient

Publish an analytic-model specification gate that cleanly states the continuous/unbounded-tail HJB problem and its admissibility/transversality conditions before further theorem work.

### Route O-D — HJB-consistent non-inward regime

Treat W-tail mean reversion as weakened and reassess the household high-wealth economics before any W-domain design.

### Blocked

Resolve genuine source/equation-authority inconsistency before further progression.

No route bypasses later HJB/KFE same-controlled-process validation.

---

## 4. Stationary household revalidation remains blocked

Stationary KFE remains NOT AUTHORIZED throughout DLH-5O.

Only after a state-domain/boundary-law process is scientifically selected, implemented and numerically validated may the project re-enter Issue #27:

- conservative generator;
- recurrent-class/nullspace evidence;
- pin admissibility and valid-pin invariance;
- ORIGINAL `Q^T g` residual;
- mass/non-negativity;
- stationary-tail diagnostics;
- recompute `C,L,A,B` and the two-region anchor from scratch.

No historical aggregate is grandfathered.

---

## 5. Regional / Deep Learning sequence remains deferred

Permanent hierarchy:

```text
2-region unit fixture
-> 3–5 province integration fixture
-> 31-province empirical/source benchmark
```

`31_PROVINCE_HOUSEHOLD_UPPER_DOMAIN_AUDIT` remains deferred. No neural training is authorized until household boundary/stationary validation is usable.

---

## 6. Scientific ceiling

During DLH-5O do not:

- mutate accepted HJB/KFE/regional source;
- mutate taper, transfer FOC, adjustment cost, economics, prices or calibration;
- choose/implement R, W, W1, W2, `W_max`, a new `b_max` or a new `a_max`;
- extrapolate the accepted taper beyond `a_max=10` as authority;
- run/extend HJB grids or previous numerical fixtures;
- run stationary KFE/density/tail/aggregates;
- implement any boundary KKT law;
- import a textbook transversality condition or representative-agent tail solution as accepted authority;
- run regional GE, multi-province audit, network training, nominal HANK, policy/welfare or Results.

---

## 7. Governance status

Issue #41 is the current intended Builder theory-analysis task. Builder authority requires synchronized Task Index / Startup Snapshot plus authoritative activation comment.

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.
