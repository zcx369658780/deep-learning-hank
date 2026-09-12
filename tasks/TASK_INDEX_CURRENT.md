# Deep Learning + HANK Task Index

Status: `ACTIVE_BUILDER_ISSUE_60__DLH_5VL_INVARIANT_DOMAIN_SAFEGUARD_DIAGNOSTIC`

Last synchronized: 2026-09-13

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

**ACTIVE — Issue #60 / DLH-5V-L**, subject to activation-comment synchronization and final refresh.

Title:

`DLH-5V-L: Test invariant-domain safeguarded value-update line search on the central selected-Q HJB case`

Task type:

`SCIENTIFIC_NUMERICAL_DIAGNOSTIC__EFFECTIVE_DOMAIN_PRESERVING_VALUE_UPDATE`

Owner / Reviewer route decision:

`APPROVE_CONTROLLED_INVARIANT_DOMAIN_SAFEGUARDED_VALUE_UPDATE_DIAGNOSTIC`

Authority marker:

`DLH_5VL_INVARIANT_DOMAIN_SAFEGUARD_DIAGNOSTIC_AUTHORIZED`

Dedicated Builder branch:

`dsh/issue-60-dlh-5vl-invariant-domain-safeguard-2026-09-13`

Authoritative activation comment:

`PENDING_INITIAL_ACTIVATION_COMMENT`

Builder authority becomes operative only after the initial activation comment, CURRENT activation-ID synchronization, and final activation-refresh comment confirm the post-sync live main.

## Latest accepted task — Issue #59 / DLH-5V-K

Issue #59 is CLOSED completed at Terminal B / H2.

Accepted candidate / integration:

`08f0135de5a60d05eda7184c367e1705da69757d`

Reviewer acceptance:

`5649245347`

Acceptance integration:

`5649248162`

Accepted verdict:

`DLH_5VK_ACCEPTED__TERMINAL_B_H2_CONFIRMED__LEGACY_EXTERNAL_PRICE_SENSITIVITY_REAL__SELECTED_Q_EFFECTIVE_DOMAIN_GAP_REMAINS__STABILIZATION_DIAGNOSTIC_NEXT`

Accepted scientific interpretation:

- external prices materially affect the frozen legacy solver;
- the sampled legacy `r_a` evidence is an observed convergent span / transition bracket, not a proof that every point in `[0.07,0.12]` converges;
- legacy convergence is not economic-quality or exact-unbounded-HJB validation because the accepted legacy derivative floor is active at nontrivial state shares and non-positive finite-difference `V_b` occurs even at converged points;
- the accepted selected-Q solver still exits its `p_b>0` boundary effective domain at the central tested sentinel `r_a=0.07`;
- cross-solver differences do not identify a geometry cause or a globally price-independent failure.

## Active scientific object — value-update invariant safeguard

Issue #60 tests exactly one controlled numerical mechanism on the single frozen central selected-Q case:

```text
V_raw = accepted implicit selected-Q update
V_trial(lambda) = V_old + lambda*(V_raw - V_old)
lambda in {1,1/2,...,2^-20}
choose largest lambda with all required boundary p_b > 1e-12
```

This changes the iteration path only. It does not change household economics, external prices, candidate scoring, controls, rates, Q construction, grid/domain, or the fixed-point equation.

Frozen central case includes `m=1`, `W_max=10`, `r_a=0.07`, `r_b=0.02`, `w=1`, `gap=0`, `delta=1000`, accepted Issue #58 tolerances/search settings.

Exactly one safeguarded run + one deterministic repeat are authorized. No price sweep or alternative damping/margin experiment is authorized.

## Frozen household / same-process authority

Accepted household oracle remains immutable/read-only:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb337f1b02b3fe33c51e`

Accepted selected-Q implementation remains immutable/read-only:

`src/deep_learning_hank/two_asset/boundary_hjb_selected_q.py`

Git blob:

`7ea342ccbe15d852b90743b14bb4b02977c2d78b`

Binding law remains:

```text
HJB boundary policy <=> KFE boundary transition law
Q backward
future KFE exactly Q^T
Q_ij>=0 for i!=j
Q_ii=-sum of ACTUAL represented outgoing rates
Q1=0 by construction
same selected candidate/rates for HJB and future KFE
```

Stationary KFE remains **NOT AUTHORIZED**.

## Hard ceiling

Issue #60 does not authorize mutation of accepted solvers, price sweeps, alternative damping factors/margins, pseudo-time adaptation, continuation, hard control bounds, KFE/stationary KFE, SCC/global-Q, production Wmax/resolution, GE, multi-region, neural, nominal, calibration, policy, welfare, or Results work.

## Current governance files

- `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
- `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
- Issue #60 body/comments.
