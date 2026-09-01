# Deep Learning + HANK Startup Snapshot — CURRENT

Date: 2026-09-01

Repository: `zcx369658780/deep-learning-hank`

Local Owner-designated workspace: `D:\deep-learning-hank`

## Governance state

- live GitHub `main` = synchronized repository/governance authority;
- GitHub Issue = sole DSH Builder authority only after publication + Task Index / Startup synchronization + authoritative activation comment;
- DSH = bounded Builder/executor;
- ChatGPT = independent fresh-GitHub reviewer / scientific-route advisor / task issuer / governance operator;
- Owner = final scientific-direction authority;
- Builder completion is not acceptance.

Priority:

`Scientific correctness > Experiment reproducibility > Research iteration speed > Git auditability > Documentation completeness`

## Current Builder state

`NO_ACTIVE_BUILDER_ISSUE__DLH_5E_ACCEPTED__DLH_5F_ROUTE_OWNER_APPROVED_PENDING_PUBLICATION`

There is currently **no active Builder Issue**. DSH must remain stopped until a new Issue is published, Task Index / Startup Snapshot are synchronized to that Issue, and an authoritative activation comment is present.

Owner has approved the next scientific route, but no Builder mutation authority has yet been published.

Current master roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`

Current scientific handoff:

`docs/governance/DLH_HANDOFF_2026_09_01_UPPER_DOMAIN_STATIONARY_TAIL_ROUTE.md`

---

## Latest accepted gate — Issue #28 / DLH-5E

Accepted candidate integrated to `main`:

`a49c19bbc3257f62bebecc26fe7d88ddcc143d9c`

Accepted classification:

`DLH_5E_IMPLEMENTATION_VALIDATION_ACCEPTED__D0_BOUNDARY_POLICY_VIOLATION_CONFIRMED__OWNER_HJB_BOUNDARY_DECISION_REQUIRED`

Acceptance level:

`L3_COMMIT_OR_PR_VERIFIED`

Scientific evidence level:

`D2_MACHINE_NUMERICAL_DIAGNOSTIC__HUMAN_REVIEWED_BOUNDARY_POLICY_BLOCKER`

Accepted evidence roots:

- `reports/dlh_5e_conservative_stationary_kfe_validation_2026_09_01/`
- `reports/dlh_5e_conservative_stationary_kfe_validation_r1_2026_09_01/`

## Accepted D0 boundary evidence

Frozen D0:

```text
wbar = 1.0
r_a  = 0.03
```

Accepted MATLAB-faithful HJB:

- converged in 11 iterations;
- final statistic about `1.67e-08`.

Upper requested outward rates:

### Upper-b

Three states above `1e-10`:

```text
(19,17,1) ~ 0.115760699
(19,18,1) ~ 0.271868724
(19,19,1) ~ 0.353747704
```

### Upper-a

28 states above `1e-10`, all on `a_index=19`.

Corrected maximum:

```text
(b,a,z) = (14,19,1)
rate ~= 0.264071883
```

Lower-b and lower-a have no material outward request.

Mechanical conservative candidate generator:

```text
row-sum max abs            = 6.106227e-16
negative offdiag magnitude = 0.0
nnz                         = 3114
```

This proves that row-sum conservation can be restored mechanically, but it does not validate the underlying HJB boundary policy. No clipped stationary density / new household aggregates / anchor is accepted.

---

## Stationary-KFE contract remains binding

The accepted Issue #27 contract remains controlling:

```text
Q^T g = 0
sum_s g_s * (db*da) = 1 per discrete z state
g_s >= 0 up to tolerance
```

Singular `Q/Q^T` is expected.

MATLAB-style contamination remains allowed in principle only with:

- conservative generator;
- recurrent-class/nullspace evidence;
- pin admissibility;
- ORIGINAL stationary residual pass;
- mass/non-negativity pass;
- valid-pin invariance;
- default MATLAB parity pin valid before future production use.

Contamination is component pinning to fix a scale direction followed by separate mass normalization; it is not itself the total-mass normalization equation.

---

## External multi-province review incorporated

The neighboring multi-province Python project is now described as:

> **a highly mature source-faithful multi-province reconstruction under active MATLAB–Python stationary parity adjudication**

It is a reference implementation / source-contract provider / benchmark, not yet a fully parity-accepted production oracle.

The following scientific corrections are now binding for the route:

1. An artificial upper asset limit is not necessarily an economic state constraint, but a finite numerical domain still needs a coherent HJB boundary closure.
2. Persistent outward drift on wider grids does not automatically prove the HJB equation is wrong; stationary-tail existence and high-wealth mean reversion must also be checked.
3. Grid expansion cannot mathematically repair a non-conservative generator rule; conservativity is guaranteed by generator construction.
4. A mechanically clipped KFE cannot be accepted if it represents a different controlled process from the HJB.
5. Grid adequacy is judged by convergence of boundary influence, not exact disappearance of every positive max drift.
6. Near-boundary mass and probability-weighted outward flux are required diagnostics alongside maximum drift.
7. Multi-province cross-project work should first use frozen household price/input snapshots rather than repeated full-GE grid sweeps.
8. Contract/module/oracle reuse is preferred over blind repository merge.
9. `2-region -> 3–5 province -> 31 province` is a permanent validation hierarchy.
10. Future regional parity separates continuous-state parity from discrete-controller branch parity.
11. First learned-network work should begin as a source spatial-rule surrogate before empirical-flow replacement.

---

## Owner-approved next scientific route — DLH-5F candidate

Tentative task class:

`SCIENTIFIC_DIAGNOSTIC__UPPER_DOMAIN_ADEQUACY_AND_STATIONARY_TAIL`

No Issue has yet been published.

### Purpose

Determine whether current upper-boundary evidence is primarily:

- finite upper-domain truncation;
- stationary-tail / high-wealth mean-reversion failure;
- inadequate finite-domain HJB/KFE boundary closure;
- or different liquid/illiquid-asset behavior.

### Prohibited interpretation

The next task must **not** define success as `max upper drift == 0` and must not alter the HJB equations or clip policy to achieve PASS.

### Experimental design

Separate:

- domain extent;
- grid resolution.

Use a small pre-frozen extent set. Increase grid-point counts with extent so `db/da` remain approximately comparable. Add separate fixed-domain resolution checks. No adaptive expansion.

### Required diagnostic families

#### Policy

- upper/lower outward maxima;
- quantiles where meaningful;
- counts/shares;
- complete offending states.

#### Tail / distribution

Only when the corresponding stationary process is scientifically admissible under the same HJB/KFE closure:

- boundary mass;
- near-boundary mass;
- probability-weighted upper outward flux;
- recurrent-class/nullspace structure;
- original stationary residual.

#### Interior stability

Compare policy on the common interior domain across wider asset domains.

#### Aggregates

Only after stationary validity:

`C,L,A,B`

and their convergence across extent/resolution.

### Decision routes

- truncation influence converges away -> freeze adequate numerical domain and revalidate KFE/aggregates;
- tail fails to stabilize -> investigate stationary-distribution existence / high-wealth asymptotics before boundary-law redesign;
- finite-domain closure remains inconsistent -> publish a separate joint HJB/KFE boundary-design gate;
- liquid and illiquid dimensions may follow different routes.

---

## Binding HJB/KFE consistency principle

```text
HJB boundary policy <=> KFE boundary transition law
```

Backward HJB and forward KFE must describe the same controlled process.

It is forbidden to solve an HJB with materially outward upper policy, independently clip the KFE to no-outflow, and then treat that density as the stationary distribution of the original HJB problem.

---

## Planned cross-project benchmark

A separate later diagnostic should be:

`31_PROVINCE_HOUSEHOLD_UPPER_DOMAIN_AUDIT`

Preferred workflow:

```text
frozen steady-state household price/input snapshots
-> 31 independent household upper-domain/tail diagnostics
```

before any repeated full 31-province GE grid sweep.

---

## Permanent regional validation hierarchy

```text
2-region unit fixture
-> 3–5 province integration fixture
-> 31-province empirical/source benchmark
```

The two-region fixture remains the primary human-auditable accounting/orientation test bed.

Future regional parity requires both:

- continuous-state parity;
- discrete-controller branch/threshold parity.

---

## Revised Deep Learning route

No neural training is currently authorized.

When the household/regional foundation is trusted:

1. `L0` — source spatial-rule surrogate;
2. `L1` — constrained structural learned spatial rule;
3. `L2` — empirical OD-flow learning with endogeneity/double-counting safeguards;
4. later capital-network learning;
5. nominal-HANK integration remains later and separately specified.

The two-stage origin-outflow + conditional-destination architecture remains a DeepLearning-HANK redesign candidate, not a claim of unique MATLAB fidelity.

---

## Immediate continuation instruction

Before publishing the next Issue, a new ChatGPT session must:

1. fresh-fetch GitHub `main`;
2. read all CURRENT rules;
3. read `tasks/TASK_INDEX_CURRENT.md`;
4. read this Startup Snapshot;
5. read `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`;
6. read `docs/governance/DLH_HANDOFF_2026_09_01_UPPER_DOMAIN_STATIONARY_TAIL_ROUTE.md`;
7. confirm there is no active Builder Issue;
8. only then publish/synchronize/activate the exact DLH-5F Issue after Owner/project-source synchronization.

Chat text is not Builder authority.

---

## Scientific ceiling

Until the upper-domain/stationary-tail route is resolved, do not:

- modify accepted HJB equations merely to remove the D0 violations;
- accept clipped `Q_c` as the original economic stationary process;
- restore old row-295 KFE aggregates;
- run validated policy/welfare Results;
- start learned `W^L` training;
- scale directly to a production learned 31-region equilibrium;
- claim the neighboring multi-province project is already fully stationary-parity accepted;
- enter nominal-HANK integration.

## Earlier accepted foundation

- Issue #27 / DLH-5D: conservative stationary-KFE / MATLAB contamination scientific contract accepted.
- Issue #26 / DLH-5C: fixed-row contamination artifact diagnosis accepted; historical row-295 aggregates not validated.
- Issue #25 / DLH-5B: two-region synchronous/Jacobi architecture accepted for wiring/accounting/trace semantics.
- Issue #24 / DLH-5A: network-ready two-region real structural contract accepted.
- Issue #23: MATLAB-faithful two-asset HJB / transfer-FOC parity repair accepted.
