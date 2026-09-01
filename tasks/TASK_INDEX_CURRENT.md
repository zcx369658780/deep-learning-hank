# Deep Learning + HANK Task Index

Status: `NO_ACTIVE_BUILDER_ISSUE__DLH_5E_ACCEPTED__DLH_5F_ROUTE_OWNER_APPROVED_PENDING_PUBLICATION`

Last synchronized: 2026-09-01

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

There is currently **NO ACTIVE BUILDER ISSUE**.

DSH must not mutate the repository until a new GitHub Issue is explicitly published, this Task Index and the CURRENT Startup Snapshot are synchronized to that Issue, and an authoritative activation comment is present.

Owner has approved the next scientific route, but **no Builder authority has yet been published**.

Current scientific roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`

Current handoff:

`docs/governance/DLH_HANDOFF_2026_09_01_UPPER_DOMAIN_STATIONARY_TAIL_ROUTE.md`

---

## Latest accepted task

**Issue #28 — DLH-5E — ACCEPTED / COMPLETED**

Accepted candidate integrated to `main`:

`a49c19bbc3257f62bebecc26fe7d88ddcc143d9c`

Accepted reviewer classification:

`DLH_5E_IMPLEMENTATION_VALIDATION_ACCEPTED__D0_BOUNDARY_POLICY_VIOLATION_CONFIRMED__OWNER_HJB_BOUNDARY_DECISION_REQUIRED`

Acceptance level:

`L3_COMMIT_OR_PR_VERIFIED`

Scientific evidence level:

`D2_MACHINE_NUMERICAL_DIAGNOSTIC__HUMAN_REVIEWED_BOUNDARY_POLICY_BLOCKER`

Accepted evidence roots:

- `reports/dlh_5e_conservative_stationary_kfe_validation_2026_09_01/`
- `reports/dlh_5e_conservative_stationary_kfe_validation_r1_2026_09_01/`

## Accepted DLH-5E evidence

Frozen D0:

```text
wbar = 1.0
r_a  = 0.03
```

Accepted HJB converges in 11 iterations.

Material upper-boundary requested outward rates:

- upper-b: 3 states above `1e-10`; max about `0.353747704` at `(19,19,1)`;
- upper-a: 28 states above `1e-10`; max about `0.264071883` at corrected coordinate `(14,19,1)`;
- lower-b / lower-a: no material outward request.

A mechanically conservative candidate generator satisfies:

```text
row-sum max abs            = 6.106227e-16
negative offdiag magnitude = 0.0
```

This establishes mechanical conservation only. It does not validate the HJB boundary policy, and no clipped stationary density / new `C,L,A,B` / `Z*,delta*` is accepted.

---

## Owner-approved next scientific route — DLH-5F candidate

Tentative task class:

`SCIENTIFIC_DIAGNOSTIC__UPPER_DOMAIN_ADEQUACY_AND_STATIONARY_TAIL`

No Issue has yet been published.

The next gate must diagnose whether the upper-boundary problem is primarily:

- finite upper-domain truncation;
- stationary-tail / high-wealth mean-reversion failure;
- inadequate finite-domain HJB/KFE boundary closure;
- or different behavior in liquid vs illiquid asset dimensions.

It must **not** modify the accepted HJB equations or tune the grid to force `max outward drift = 0`.

### Required experimental principles

1. Separate upper-domain extent from grid resolution.
2. Use a small, pre-frozen set of domain expansions; no adaptive PASS-seeking.
3. Increase point counts with extent so `db/da` remain approximately comparable.
4. Add separate fixed-domain resolution checks.
5. Diagnose convergence of boundary influence, not exact disappearance of every positive boundary drift.

### Required diagnostic families

- upper/lower policy drift maxima, quantiles, counts and complete states;
- boundary / near-boundary mass when a scientifically admissible stationary process is available;
- probability-weighted upper outward flux;
- shared-interior policy stability across domain extents;
- recurrent-class/nullspace/original-stationary-residual evidence;
- `C,L,A,B` stability only after stationary validity;
- liquid and illiquid assets separately where needed.

### Binding consistency law

```text
HJB boundary policy <=> KFE boundary transition law
```

HJB and KFE must represent the same controlled process. Mechanical clipping of KFE after an outward HJB solution is not an accepted scientific repair.

---

## Multi-province cross-project reference status

The neighboring multi-province Python project is treated as:

> a highly mature source-faithful multi-province reconstruction under active MATLAB–Python stationary parity adjudication

It is not yet treated as fully parity-accepted production authority.

Preferred future cross-project diagnostic:

`31_PROVINCE_HOUSEHOLD_UPPER_DOMAIN_AUDIT`

using frozen household price/input snapshots and independent household solves before any full 31-province GE grid sweep.

Reuse policy:

- reuse validated contracts/modules/oracles;
- do not blindly merge repositories or import the entire neighboring project as an unquestioned production dependency.

---

## Permanent validation hierarchy

```text
2-region unit fixture
-> 3–5 province integration fixture
-> 31-province empirical/source benchmark
```

The two-region fixture remains permanently because it is the human-auditable accounting/orientation test bed.

Future regional parity must distinguish:

- continuous-state parity;
- discrete-controller branch / threshold parity.

---

## Revised Deep Learning route

No learned-network training is currently authorized.

When the household/regional equilibrium foundation is trusted:

1. `L0`: source spatial-rule surrogate;
2. `L1`: constrained structural learned spatial rule;
3. `L2`: empirical OD-flow learning with endogeneity/double-counting safeguards;
4. later capital-network learning;
5. nominal-HANK track remains later and separately specified.

The two-stage origin-outflow + conditional-destination architecture is a DeepLearning-HANK redesign candidate, not a claim of unique MATLAB fidelity.

---

## Scientific ceiling before DLH-5F resolution

Do not:

- mutate the accepted HJB equations to force boundary PASS;
- accept mechanically clipped `Q_c` as the stationary process of the original HJB;
- restore historical row-295 KFE aggregates;
- run validated policy/welfare Results;
- start learned `W^L` training;
- scale directly to production learned 31-region equilibrium;
- claim neighboring multi-province MATLAB–Python stationary parity is already fully accepted;
- enter nominal-HANK integration.

## Earlier accepted foundation

- Issue #27 / DLH-5D: conservative stationary-KFE / MATLAB contamination scientific contract accepted.
- Issue #26 / DLH-5C: fixed-row contamination artifact diagnosis accepted; old row-295 KFE aggregates not validated.
- Issue #25 / DLH-5B: two-region synchronous/Jacobi architecture accepted for wiring/accounting/trace semantics.
- Issue #24 / DLH-5A: network-ready two-region real structural contract accepted.
- Issue #23: MATLAB-faithful two-asset HJB / transfer-FOC parity repair accepted.
