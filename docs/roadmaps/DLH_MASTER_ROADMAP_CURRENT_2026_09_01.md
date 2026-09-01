# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.3  
**Date:** 2026-09-01  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** CURRENT OWNER-APPROVED SCIENTIFIC ROUTE  

---

## 0. Project objective

The long-run objective is a **data-to-structural-model calibration and regional-network HANK platform**. The project does not use deep learning to replace the economic definition of the household HJB/KFE. Instead:

- household optimization, HJB/KFE, aggregation, firm blocks, accounting identities and later nominal-HANK equations remain hard structural economics;
- hard-to-specify cross-regional mappings are the first objects eligible for learning;
- all learned mappings must remain embedded in a transparent equilibrium/accounting structure and must survive out-of-sample and perturbation tests.

The first learned object remains the regional labor-flow/spatial rule. Capital-network learning and nominal-HANK integration are later stages.

---

## 1. Accepted scientific foundation through DLH-5E

### 1.1 Household/HJB foundation — Issue #23

Accepted MATLAB-faithful two-asset household/HJB source:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Accepted source identity recorded through the parity work:

- Git blob: `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`
- SHA-256: `1795718C469FC3B427CAB8E3D5957C133BEAD6EACC9EF0A25A3EDB7211D1A024`

The old arbitrary fixed-bond closure (`B_hh=B_gov=1`) and nested cold-start Brent route are superseded as forward model authority.

### 1.2 Two-region structural contract — Issues #24–#25

The project has an accepted two-region synchronous/Jacobi architecture with:

- conditional household blocks;
- labor-flow accounting;
- home-region identity preserved;
- destination labor aggregation;
- composite wage interface;
- regional firm block;
- fixed-damping outer map;
- deterministic trace / fail-closed semantics;
- region-order invariance.

The two-region fixture is retained permanently as a human-auditable unit fixture. It is not intended to identify a real spatial network by itself.

### 1.3 KFE diagnosis and scientific contract — Issues #26–#27

Accepted conclusions:

- singular `Q` / `Q^T` is expected for a stationary generator and is not itself a failure;
- MATLAB-style row contamination remains an authorized numerical scale-pinning method in principle;
- contaminated-system residual alone is not scientific evidence;
- accepted stationary density must satisfy the ORIGINAL `Q^T g = 0`, mass normalization and non-negativity;
- stationary uniqueness, pin admissibility and pin invariance are distinct;
- a component pin `g_n=c>0` is admissible only when the stationary vector has non-zero support at `n`;
- conservative generator construction and recurrent-class/nullspace evidence are required;
- HJB boundary policy and KFE generator must ultimately represent the **same controlled process**.

### 1.4 DLH-5E accepted boundary-policy blocker — Issue #28

Accepted candidate:

`a49c19bbc3257f62bebecc26fe7d88ddcc143d9c`

Accepted classification:

`DLH_5E_IMPLEMENTATION_VALIDATION_ACCEPTED__D0_BOUNDARY_POLICY_VIOLATION_CONFIRMED__OWNER_HJB_BOUNDARY_DECISION_REQUIRED`

Frozen D0:

```text
wbar = 1.0
r_a  = 0.03
```

Accepted HJB converges in 11 iterations. Requested upper-boundary rates are materially outward:

- upper-b: 3 states above `1e-10`; max about `0.353747704` at `(19,19,1)`;
- upper-a: 28 states above `1e-10`; max about `0.264071883` at corrected coordinate `(14,19,1)`;
- lower-b / lower-a: no material outward requests.

A mechanically conservative candidate generator can satisfy row-sum zero to machine precision, but that does not repair the underlying HJB policy. Therefore stationary/nullspace/pin/aggregate/anchor acceptance is not reached on D0.

---

## 2. Scientific interpretation after external multi-province review

The current upper-boundary evidence must **not** be reduced to a binary choice between “grid too narrow” and “impose an economic upper state constraint”.

The theoretical asset domain is plausibly unbounded above, while current `b_max=5` and `a_max=10` are numerical truncations. A finite numerical domain still requires a mathematically coherent upper-boundary closure. Candidate explanations for persistent outward drift include:

1. the upper domain is simply too narrow;
2. the finite-domain HJB closure is inadequate (e.g. derivative/tail/asymptotic condition);
3. the parameter/price configuration does not generate sufficient high-wealth mean reversion, so a stable stationary wealth tail may not exist under the current structural specification;
4. liquid and illiquid assets may require different upper-domain treatment.

Therefore the next gate must diagnose **upper-domain adequacy and stationary-tail behavior**, not tune the grid until `max drift = 0`.

---

## 3. Controlling boundary consistency principle

Future household acceptance must satisfy:

```text
HJB boundary policy  <=>  KFE boundary transition law
```

The HJB and KFE must describe the same controlled process.

It is forbidden to:

- solve an HJB with materially outward upper-boundary policy;
- then silently clip the KFE generator to no-outflow;
- and treat the resulting conservative stationary density as the solution to the original household problem.

Mechanical generator conservativity is necessary but not sufficient.

---

## 4. Immediate next scientific gate — DLH-5F candidate

### 4.1 Name

**Upper-Domain Adequacy and Stationary-Tail Diagnostic**

This is the Owner-approved next scientific route. No Builder authority exists until a dedicated Issue is later published and activated.

### 4.2 Purpose

Determine whether the current upper-domain blocker is primarily a finite-domain truncation problem, a tail/stationarity problem, or evidence that a new finite-domain HJB closure must be designed.

This gate must not modify the accepted HJB equations or force outward drift to zero.

### 4.3 Experimental design

Separate **domain extent** from **resolution**.

#### Extent experiment

Use a small, pre-frozen set of upper-domain expansions such as baseline / moderately wider / substantially wider domains. Increase grid-point counts with domain extent so that `db` and `da` remain approximately comparable to baseline.

Do not enlarge the domain while keeping point counts fixed and then attribute all changes to extent; that confounds domain and resolution.

#### Resolution experiment

At one or more fixed domains, refine grid resolution to test discretization sensitivity independently of upper extent.

No adaptive expansion and no PASS-seeking search are allowed.

### 4.4 Required diagnostic families

The next gate must not rely only on maximum outward drift.

#### A. Policy diagnostics

For both liquid and illiquid assets:

- upper-boundary outward maximum;
- outward-rate quantiles where meaningful;
- count/share of outward states;
- complete offending-state coordinates/rates;
- lower-boundary diagnostics for regression safety.

#### B. Boundary and near-boundary mass

After a scientifically admissible stationary distribution is available for the relevant candidate process, report quantities such as:

```text
Pr(a at / near a_max)
Pr(b at / near b_max)
Pr(a >= 0.9*a_max)
```

with the exact definition frozen before execution.

#### C. Probability-weighted upper outward flux

For a scientifically admissible density `g`, define diagnostics such as:

```text
Phi_a_upper = sum_{s on upper-a} g_s * max(mu_a_s,0)
Phi_b_upper = sum_{s on upper-b} g_s * max(mu_b_s,0)
```

The purpose is to distinguish a large drift on negligible mass from economically material boundary influence.

#### D. Interior-policy stability

Compare policies on the **shared interior domain** across progressively wider grids. A valid truncation should not materially change interior policy simply because a farther numerical boundary is introduced.

#### E. Aggregate stability

Only after the stationary KFE is scientifically admissible under the same controlled process, compare:

`C, L, A, B`

across domains/resolutions.

No historical row-295 aggregate is grandfathered.

### 4.5 Decision logic

#### Route A — truncation influence converges away

If wider domains show:

- near-boundary mass declining;
- probability-weighted outward flux declining;
- shared-interior policy stabilizing;
- accepted aggregates stabilizing;
- stationary structure remaining well-defined;

then classify primarily as **GRID / UPPER-DOMAIN ADEQUACY**. Freeze an adequate numerical domain and continue KFE/aggregate revalidation without inventing an economic upper asset constraint.

#### Route B — tail does not stabilize

If the distribution/policy simply follows the boundary outward, boundary mass/flux does not decline, or aggregates do not converge, investigate **stationary-tail existence / high-wealth asymptotics / economic mean reversion** before designing a numerical boundary fix.

Do not automatically interpret persistent positive drift as proof that the HJB equation is wrong.

#### Route C — finite-domain closure required

If evidence supports existence of a stationary economic tail but the finite-domain numerical approximation remains inconsistent, publish a separate scientific-design gate for an upper-boundary HJB/KFE closure (e.g. one-sided/asymptotic/transversality-consistent treatment). HJB and KFE boundary laws must be frozen together.

#### Route D — liquid/illiquid assets differ

Treat `b` and `a` separately if one dimension stabilizes while the other does not.

---

## 5. Multi-province reference project — correct role

The neighboring multi-province Python project is currently treated as:

> **a highly mature source-faithful multi-province reconstruction under active MATLAB–Python stationary parity adjudication**

It is not yet treated as a fully parity-accepted binary oracle.

Its correct role for DeepLearning-HANK is:

- reference implementation;
- source/provenance provider;
- interface-contract provider;
- benchmark and test oracle where the relevant layer is already accepted;
- provider of frozen household input snapshots for bounded cross-project diagnostics.

Do not blindly merge repositories or make the entire neighboring codebase a production dependency.

---

## 6. Planned cross-project household benchmark

After or alongside the first upper-domain diagnostic, a separate cross-project gate should perform a:

**31_PROVINCE_HOUSEHOLD_UPPER_DOMAIN_AUDIT**

Preferred design:

```text
frozen steady-state price/input snapshot
-> 31 independent household solves / boundary diagnostics
```

rather than a full 31-province GE grid sweep.

Target outputs per province should include, when available under the accepted household process:

- household input provenance;
- HJB convergence;
- upper/lower requested drift diagnostics;
- near-boundary mass;
- probability-weighted boundary flux;
- stationary validity diagnostics;
- `A, B, C, L` grid sensitivity.

This benchmark helps distinguish whether the current D0 blocker is fixture-specific or systematic across economically relevant multi-province states.

---

## 7. Regional validation hierarchy — retained permanently

The project uses three complementary scales:

```text
2-region unit fixture
-> 3–5 province integration fixture
-> 31-province empirical/source benchmark
```

The two-region fixture is never “retired” by larger systems because it is the only level where regional flow accounting can remain directly human-auditable.

For future regional parity, separately test:

1. **continuous-state parity** — prices, aggregates, flows and residuals;
2. **discrete-controller branch parity** — threshold-triggered resets, clipping/controller decisions and branch sequences.

Tiny continuous numerical differences can cross discrete thresholds and create materially different equilibrium trajectories.

---

## 8. Revised Deep Learning route

### 8.1 Do not train yet

No learned network should be trained until the stationary household block and regional equilibrium foundation are scientifically trustworthy.

### 8.2 First learned object remains the spatial labor rule

However, the first learning stage is revised to avoid endogeneity/double counting.

#### Stage L0 — source-rule surrogate

First learn or emulate the validated source spatial rule under explicit structural inputs, e.g. wages, taxes, migration costs, pair features and other source-authorized state variables:

```text
f_theta(source inputs) ~= source spatial-module output
```

The purpose is to prove that a learned module can reproduce the source spatial mechanism while preserving orientation, conservation and equilibrium interfaces.

#### Stage L1 — structural learned rule

Only after L0 passes, replace hand-coded mapping structure with an interpretable learned mapping under explicit constraints and ablations.

#### Stage L2 — empirical flow learning

Only later add real OD flow targets, with explicit safeguards against double counting equilibrium wage/policy effects and against hidden leakage from endogenous outcomes into features.

The two-stage origin outflow + conditional destination architecture remains a candidate redesign contract, not a claim that it is uniquely MATLAB-faithful.

---

## 9. Capital-network and nominal-HANK tracks

Capital-network learning remains later than the labor-network route.

Nominal HANK remains a separate later track requiring an independently frozen minimal nominal block (nominal rigidity, inflation/Phillips object, monetary rule, Fisher relation, fiscal/debt consistency and household-return consistency). A Taylor-style rate object alone does not turn the current regional real-side scaffold into a complete nominal HANK.

---

## 10. Current sequencing

### Immediate

1. preserve accepted Issues #23–#28 evidence;
2. keep DSH stopped until new authority is published;
3. run/publish DLH-5F only after governance synchronization;
4. diagnose upper-domain adequacy + stationary-tail behavior without changing HJB equations.

### After DLH-5F

Depending on evidence:

- freeze adequate asset domain and revalidate KFE/aggregates; or
- investigate stationary-tail existence / asymptotics; or
- design a joint HJB/KFE upper-boundary closure.

### Then

1. revalidate household stationary `C,L,A,B`;
2. revalidate `K=M*A` and the two-region anchor;
3. rerun two-region S0/S1 and order-invariance gates;
4. build 3–5 province integration fixture;
5. perform 31-province frozen-price household audit / source benchmark;
6. only then resume spatial learned-module work.

---

## 11. Current governance status

There is currently **NO ACTIVE BUILDER ISSUE**.

Owner has approved the DLH-5F scientific route described above, but Builder work remains unauthorized until:

- a dedicated GitHub Issue is published;
- `tasks/TASK_INDEX_CURRENT.md` is synchronized;
- `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md` is synchronized;
- an authoritative activation comment is posted.

This roadmap is scientific route authority, not Builder mutation authority.

---

## 12. Current scientific ceiling

Until upper-domain/stationary-tail evidence is resolved, do not:

- modify the accepted HJB equations to force a PASS;
- silently clip HJB outward policy into a different KFE process;
- accept mechanically conservative `Q_c` as the original economic stationary process;
- restore old row-295 KFE aggregates;
- run policy/welfare Results;
- start OD / learned `W^L` training;
- scale directly to production 31-region learned equilibrium;
- claim the neighboring multi-province Python reconstruction is already complete MATLAB–Python stationary parity authority.

---

## 13. Working scientific label

Working label remains:

**Network-Structured Regional HANK (NSR-HANK)**

Long-run description:

> A structural heterogeneous-agent regional equilibrium framework in which economically defined household, firm, accounting and nominal-policy blocks are connected by interpretable learned spatial mappings only after the underlying stationary and equilibrium processes have passed explicit numerical, economic and empirical validation gates.
