# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.21  
**Date:** 2026-09-03  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** CURRENT OWNER-DECISION CHECKPOINT — DLH-5S ACCEPTED / NO ACTIVE BUILDER ISSUE

---

## 0. Long-run objective

Build a data-to-structural-model calibration and regional-network HANK platform in which household HJB/KFE, aggregation, firm/accounting blocks and later nominal-HANK equations remain explicit structural economics, while difficult cross-regional mappings become interpretable learned modules only after household and equilibrium foundations pass scientific and numerical validation.

The first learned object remains the regional labor/spatial rule. Capital-network learning and nominal-HANK integration remain later stages.

---

## 1. Accepted household foundation through DLH-5S

Accepted MATLAB-faithful household source:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Binding Issue #27 law:

```text
HJB boundary policy <=> KFE boundary transition law
```

Stationary KFE remains **NOT AUTHORIZED** until a controlled household domain/boundary process is separately selected, implemented and validated.

R/W domain designs remain unfrozen. `W=a+b` remains an accounting coordinate, not production-domain authority. No `W_max` is authorized.

### Accepted analytic sequence before DLH-5S

DLH-5O produced the conditional p=2 candidate:

```text
K = 4/(rho+r_b)^2
c/b -> 0.0175
mu_W/b -> -0.0025
```

DLH-5P preserved a critical out-of-S3 benchmark `R~Theta(sqrt(b))` and showed the tail specification was not unique without an additional analytic class.

Owner selected provisional S3 + parallel falsification:

`PROVISIONAL_S3_ANALYTIC_CLASS__PARALLEL_FALSIFICATION_ROUTE_APPROVED`

Working class remains:

- S1: continuous unbounded-positive-b analytic base on fixed finite a-support, `V<0`, `V_b>0`;
- S2: `V_inf=0` provisional tail-selection assumption;
- primary S3: `R=V_a/V_b=O(1)` uniformly on claimed compact interior-a support, with no sign restriction;
- P-TR `R=o(sqrt(b))` sensitivity only;
- critical `R~Theta(sqrt(b))` retained outside S3 as a benchmark.

DLH-5Q established p=2 as the unique self-consistent formal balance among the correctly analyzed power/explicit-slow families inside S3, while existence/comparison, actual realization, broader exotic regimes, derivative-remainder control and endpoints remained open.

DLH-5R then found accessible-range numerical compatibility with S3 derivative control: `|R|=O(1)`, `|R|/sqrt(b)` and `chi/b` declined, no critical `R~sqrt(b)` signature appeared, but p=2 scaling was not reached before the pre-existing b160 ceiling. No larger numerical domain was authorized.

---

## 2. Accepted DLH-5S / Issue #45

Issue #45 is CLOSED completed.

Accepted candidate:

`160781a89c6e22b5f17b4259500893140fcb9c01`

Reviewer acceptance comment:

`5519142363`

Acceptance integration:

`75bedf6e3bb97d024dc8af3afa30f7398f205846`

Acceptance level:

`L3_COMMIT_VERIFIED__SCIENTIFIC_THEORY_ANALYSIS_ACCEPTED`

Accepted verdict:

`DLH_5S_REV3_ACCEPTED__OUTCOME_B_CONFIRMED__SCALED_TAIL_STRUCTURE_ACCEPTED__P2_REALIZATION_REMAINS_OPEN`

Accepted terminal:

`DLH_5S_P2_REALIZATION_NOT_CLOSED__SCALED_TAIL_TIGHTNESS_OR_BRANCH_SELECTION_REMAINS_UNPROVED__OWNER_ROUTE_DECISION_REQUIRED`

### 2.1 Exact scaled structure accepted

```text
H=-bV
Q=b^2 V_b
s=log b
H_s=H-Q
c/b=Q^(-1/2)
p_eff=2-dlog(Q)/dlog(b)
```

Exact scaled HJB:

```text
(rho I-S)H=F(Q)+E
F(Q)=2sqrt(Q)-r_b Q
```

Exact vector Q-flow:

```text
F'(Q)Q_s=F(Q)-rho Q+S Q+E-E_s
```

The remainder decomposition is accepted with the Rev-2/Rev-3 caveats: S3 does not sign `R` or `V_a`; `E_illiquid` is controlled in magnitude only under S3 + bounded Q + compact-a; the simplified transfer sign is restricted to the stated compact-interior branch.

### 2.2 Reduced p=2 attractor structure accepted

For the deliberately reduced `E=0`, z-symmetric scalar system:

```text
rho H = 2sqrt(Q)-r_b Q
H_s = H-Q
```

there is a positive fixed point

```text
K*=H*=Q*=4/(rho+r_b)^2=3265.3061224489797
```

on the regular lower sector. The exact nonlinear reduced flow has:

```text
0<Q<K*              => Q_s>0
K*<Q<1/r_b^2        => Q_s<0
Q>1/r_b^2           => upper-sector runaway
```

The mean eigenvalue `-7` is accepted only as the **local homogeneous** eigenvalue near `K*`; it is not a global trajectory estimate and is not a generic full-HJB rate.

### 2.3 z-coupled authority accepted

The local homogeneous z-difference eigenvalue near the candidate is about `-273.67`. This is also a local/unforced eigenvalue only.

If `E->0` and `E_s->0`, the asymptotically autonomous limit is the **E=0 z-coupled vector system**:

```text
F'(Q)Q_s=F(Q)-rho Q+S Q
```

The scalar z-symmetric reduced dynamics are an invariant/reduced subsystem and become an asymptotic reduction only conditional on z-difference synchronization. Nonlinear/global synchronization is not established.

### 2.4 Effective-exponent authority accepted

The identity

```text
p_eff=2-dlog(Q)/dlog(b)
```

is exact where regular. `Q->K*>0` by itself does not imply `p_eff->2`; derivative-regular convergence such as `dlog(Q)/dlog(b)->0` is additionally required. Oscillatory/derivative-irregular regimes therefore remain part of the open realization problem.

### 2.5 What DLH-5S does not prove

S1+S2+S3 do **not** establish:

1. Q upper tightness / precompactness;
2. Q non-degeneracy away from zero;
3. eventual regular-lower-sector branch selection / distance from `F'(Q)=0`;
4. derivative remainder `E_s->0`;
5. coupled-global z synchronization;
6. omega-limit / basin entry into the positive p=2 attractor.

No analytic obstruction or counterexample was demonstrated. S3 therefore remains provisional/falsifiable rather than rejected or promoted.

DLH-5R finite-window movements remain qualitatively compatible with the reduced-attractor direction but do not prove full-HJB p=2 realization.

---

## 3. Owner decision checkpoint after DLH-5S

There is currently **NO ACTIVE BUILDER ISSUE**.

DLH-5S converted the earlier vague “no exotic tail” gap into a concrete set of missing dynamical objects. The next step is model/science defining and therefore requires an Owner choice.

### Route T — bounded analytic tightness / basin theorem

Goal: try to derive, or materially reduce, the remaining class-B assumptions without new numerical-domain expansion.

Targets may include:

- upper/lower bounds for Q;
- exclusion of approach to the reduced singular sector;
- derivative regularity sufficient for `E_s->0`;
- nonlinear z synchronization;
- coupled omega-limit / basin entry.

This route preserves the existing b160 ceiling and remains theory-first.

### Route N — bounded numerical diagnosis of the remaining conditions

Goal: test empirical/numerical signatures of tightness, regular-sector selection, derivative behavior and synchronization under an exact pre-frozen scope.

This requires a new Owner authorization and Issue. It must not silently enlarge b160, convert finite-window evidence into theorem proof, or authorize stationary KFE.

### Route D — return to R/W domain and joint boundary-law design

Goal: accept that p=2 realization remains unresolved, and use the accepted tail information only as conditional guidance while making the model-defining production-domain / HJB-KFE boundary choice.

Any R/W/W1/W2/`W_max` or endpoint law is an Owner-level scientific choice. HJB and KFE boundary laws must be frozen together; stationary KFE remains blocked until that controlled process is implemented and validated.

### Route H — hold/defer

Preserve the current provisional scientific boundary and do not advance household production/KFE work until a later decision or stronger theory/evidence becomes available.

No route is selected automatically by this roadmap.

---

## 4. Downstream household sequence after adequate Owner authority

The downstream architecture remains:

```text
accepted analytic/diagnostic authority
-> Owner R/W/domain/boundary decision
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

Regional GE, learned regional labor/spatial rules, capital-network learning, nominal HANK, calibration, policy and welfare remain deferred until the household controlled process and stationary foundation are accepted.

When neural work eventually resumes, the intended sequence remains source spatial-rule surrogate first, then constrained structural learned rule, then empirical OD-flow learning with explicit endogeneity/double-counting safeguards.

---

## 6. Scientific ceiling at the current checkpoint

Until the Owner selects and authorizes a next route, do not:

- mutate accepted household HJB/economics;
- reopen b160 / create b180 or b200 / alter grid or taper;
- choose or implement R/W/W1/W2/`W_max`;
- invent/implement endpoint/state-domain laws;
- run stationary KFE/nullspace/pin/density/tail mass/aggregates;
- run regional GE / multi-province execution;
- train learned regional networks;
- enter nominal HANK, calibration, policy, welfare, or Results;
- create a successor Builder Issue automatically.

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.
