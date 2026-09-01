# Deep Learning + HANK Task Index

Status: `NO_ACTIVE_BUILDER_ISSUE__DLH_5E_ACCEPTED__OWNER_HJB_BOUNDARY_POLICY_DECISION_REQUIRED`

Last synchronized: 2026-09-01

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

There is currently **NO ACTIVE BUILDER ISSUE**.

DSH must not mutate the repository until a new GitHub Issue is explicitly published, this Task Index and the CURRENT Startup Snapshot are synchronized to that Issue, and an authoritative activation comment is present.

## Latest accepted task

**Issue #28 — DLH-5E — ACCEPTED / COMPLETED**

Title:

`DLH-5E: Implement conservative stationary-KFE validator and test canonical boundary-policy gate`

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

## Accepted DLH-5E findings

The exact frozen D0 household/HJB state remains:

```text
wbar = 1.0
r_a  = 0.03
```

The accepted MATLAB-faithful HJB converges in 11 iterations. From the post-convergence drifts, the requested finite-grid boundary rates are materially outward at the upper asset boundaries:

- upper-b: 3 states above `1e-10`; max `0.353747704...` at `(b,a,z)=(19,19,1)`;
- upper-a: 28 states above `1e-10`; max `0.264071883...` at corrected coordinate `(14,19,1)`;
- lower-b / lower-a: no material outward requests.

The full offending-state coordinate/rate sets are preserved in the accepted R1 boundary-policy evidence.

A mechanically conservative candidate generator `Q_c`, built only from admitted in-grid transitions, satisfies:

```text
row-sum max abs = 6.106227e-16
negative off-diagonal magnitude = 0.0
```

Therefore matrix conservation can be restored mechanically. However, this does **not** validate the underlying HJB boundary policy, because the requested economic drift remains materially outward.

The accepted terminal scientific blocker is:

`BLOCKED_DLH_5E_BOUNDARY_POLICY_VIOLATION__OWNER_BOUNDARY_POLICY_DECISION_REQUIRED`

The implementation correctly fail-closes before stationary/nullspace/pin/aggregate/anchor acceptance. Accordingly:

- no clipped `Q_c` stationary density is scientifically accepted;
- no new `C/L/A/B` aggregates are accepted;
- no `Z*/delta*` anchor is accepted;
- D1-D3 are not reached;
- no two-region outer iteration is reached.

Deterministic R1 reproduction includes exact per-boundary labels/counts/argmax coordinates/complete offending coordinate sets and requested rates; accepted repeat max numeric/rate difference is `0.0`.

## Current scientific interpretation

The project has moved the primary blocker upstream from the KFE contamination mechanism to the HJB finite-grid boundary policy on the frozen canonical fixture.

The accepted MATLAB-style contamination contract from Issue #27 remains valid in principle, but it cannot yet be revalidated on D0 because the HJB boundary-policy gate blocks first.

The accepted conservative KFE validator is a candidate/diagnostic tool only. It is not production household routing and must not be treated as a production solver.

## Owner scientific decision required before next Issue

The next Builder task is intentionally **not published**.

Owner must freeze the HJB upper-boundary state-constraint / boundary-policy semantics before implementation resumes. At minimum the decision must determine:

- how the HJB local policy is constrained at finite upper `b` and upper `a` boundaries;
- whether the correct economic law is inward/no-outflow state constraint, endogenous boundary derivative/one-sided policy selection, grid adequacy expansion, or another explicitly justified boundary treatment;
- how requested outward drift is distinguished from numerical truncation;
- what diagnostics establish that a repaired boundary policy is economically admissible rather than merely mechanically conservative;
- the order for re-running D0 boundary gate, conservative KFE/nullspace/contamination validation, household aggregates, and then the two-region anchor.

Until that Owner decision is frozen and a successor Issue is published/activated, DSH must remain stopped.

## Earlier accepted foundation

- Issue #27 / DLH-5D: conservative stationary-KFE / MATLAB contamination scientific contract accepted.
- Issue #26 / DLH-5C: fixed-row contamination artifact diagnosis accepted; prior row-295 KFE-dependent aggregates are not validated stationary-equilibrium quantities.
- Issue #25 / DLH-5B: two-region synchronous/Jacobi architecture accepted for wiring/accounting/trace semantics; KFE-dependent aggregates/anchor remain scientifically qualified.
- Issue #24 / DLH-5A: network-ready two-region real structural contract accepted.
- Issue #23: MATLAB-faithful two-asset HJB / transfer-FOC parity repair accepted; accepted HJB/local-policy source remains unchanged through DLH-5E.
