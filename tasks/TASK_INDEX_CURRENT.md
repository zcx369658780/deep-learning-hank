# Deep Learning + HANK Task Index

Status: `NO_ACTIVE_BUILDER_ISSUE__DLH_5O_ACCEPTED__OWNER_DECISION_PENDING_ANALYTIC_MODEL_SPECIFICATION`

Last synchronized: 2026-09-02

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

**No active Builder Issue.**

Issue #41 / DLH-5O is accepted, integrated to `main`, and CLOSED completed. DSH must fail closed until a new GitHub Issue is published, Task Index / Startup Snapshot are synchronized to it, and an authoritative activation comment is posted.

No chat instruction alone creates Builder authority.

## Latest accepted task — Issue #41 / DLH-5O

Title:

`DLH-5O: Derive fixed-a liquid-tail HJB value-function asymptotics`

Accepted candidate:

`25645d2dd1963e8fc17176a7fadc16d914811221`

Reviewer acceptance comment:

`5504453148`

Acceptance integration commit:

`540b16ebd3a577a55ccd92a8d74ced373798557e`

Accepted reviewer verdict:

`DLH_5O_REV2_ACCEPTED__OUTCOME_B_SUPPORTED__P2_COEFFICIENT_AND_INWARD_SIGN_VALID_ONLY_UNDER_EXPLICIT_DERIVATIVE_CONTROL__ANALYTIC_MODEL_SPECIFICATION_OWNER_DECISION_REQUIRED`

Acceptance level:

`L3_COMMIT_VERIFIED__SCIENTIFIC_THEORY_ANALYSIS_ACCEPTED`

Accepted terminal:

`DLH_5O_HJB_LIQUID_TAIL_DOMINANT_BALANCE_CONDITIONAL__MISSING_ANALYTIC_ASSUMPTIONS_IDENTIFIED`

## Controlling accepted interpretation

1. The accepted MATLAB-faithful household source is finite-grid numerical authority. It does not itself specify an unbounded-positive-`b` HJB boundary/transversality condition or tail theorem.
2. Under an explicit smooth-continuum interior-HJB assumption and the p=2 candidate `V_b ~ K/b^2`, the transfer-dependent HJB object must be treated jointly as
   `V_b*[d*(V_a/V_b-1)-chi(d,a)]`.
3. The conditional p=2 coefficient result requires explicit derivative control P-TR:
   `V_a/V_b = o(sqrt(b))` uniformly over the fixed `a in [0,10]` support and accepted z states. Under P-TR the transfer Hamiltonian is subleading at `O(1/b)`.
4. Under the full conditional premise set, the leading coefficient system is
   `(rho+r_b)K - 2*sqrt(K) = S*K`.
   For the frozen symmetric z-switch system this gives
   `K = 4/(rho+r_b)^2` and `c/b = (rho+r_b)/2 = 0.0175`.
5. Because `0.0175 > r_b=0.015`, the candidate implies conditional fixed-a liquid-tail total-wealth inwardness: `mu_W/b -> -0.0025`.
6. This is not an unconditional theorem, not a full two-asset infinite-domain result, and not domain authority.
7. The critical transfer regime `V_a/V_b ~ Theta(sqrt(b))` remains unresolved; its transfer Hamiltonian is same-order and changes the coefficient equation.
8. Reviewer comment `5504453148` controls two non-blocking clarifications over local report shorthand:
   - P-TR alone implies `d=o(sqrt(b))`, `chi=o(b)`, `mu_a=o(sqrt(b))`; `O(1)` transfer/cost orders require the stronger `V_a/V_b=O(1)` subcase.
   - the local p<1 utility exponent comparison is not controlling; the switch-spectrum conclusion in the sub-root-transfer class survives with the corrected order comparison.
9. R and W remain unfrozen. No `W_max` is authorized.
10. Stationary KFE remains NOT AUTHORIZED under Issue #27.

## Owner decision checkpoint

The next proposed route is an **analytic-model specification gate** for the unbounded-positive-`b` HJB problem. That gate would be model-defining because it must specify or adjudicate:

- the continuous/unbounded-`b` HJB problem being claimed as analytic authority;
- admissibility / asymptotic boundary / transversality conditions;
- regularity and uniformity requirements;
- derivative-control / transfer-ratio class, including whether P-TR is assumed or proved;
- treatment of the unresolved critical `V_a/V_b ~ Theta(sqrt(b))` regime.

**Owner scientific decision is required before any successor Issue is activated.**

No implementation, domain selection, stationary KFE, regional GE, neural training, nominal HANK, calibration, policy/welfare or Results work is authorized at this checkpoint.

## Current route authority

- Latest accepted theory package: Issue #41 / DLH-5O.
- Reviewer acceptance authority: Issue #41 comment `5504453148`.
- Startup Snapshot: `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`.
- Roadmap: `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`.
- There is currently **no active Builder branch/task authority**.
