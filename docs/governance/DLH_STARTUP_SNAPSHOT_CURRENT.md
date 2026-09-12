# Deep Learning + HANK Startup Snapshot — CURRENT

Date: 2026-09-13

Repository: `zcx369658780/deep-learning-hank`

Local Owner-designated workspace: `D:\deep-learning-hank`

## Governance state

- live GitHub `main` = synchronized repository/code/governance authority;
- open GitHub Issue = sole DSH Builder task authority only after publication + CURRENT synchronization + authoritative activation comments;
- DSH = bounded Builder/scientific analyst only under an active Issue;
- ChatGPT = independent reviewer / scientific-route advisor / task issuer / governance operator;
- Owner = final scientific authority;
- Builder completion is not acceptance.

Priority:

`Scientific correctness > Experiment reproducibility > Research iteration speed > Git auditability > Documentation completeness`

## Current Builder state

**ACTIVE — Issue #60 / DLH-5V-L**, pending final activation refresh.

Title:

`DLH-5V-L: Test invariant-domain safeguarded value-update line search on the central selected-Q HJB case`

Task type:

`SCIENTIFIC_NUMERICAL_DIAGNOSTIC__EFFECTIVE_DOMAIN_PRESERVING_VALUE_UPDATE`

Owner / Reviewer route decision:

`APPROVE_CONTROLLED_INVARIANT_DOMAIN_SAFEGUARDED_VALUE_UPDATE_DIAGNOSTIC`

Authority marker:

`DLH_5VL_INVARIANT_DOMAIN_SAFEGUARD_DIAGNOSTIC_AUTHORIZED`

Dedicated branch:

`dsh/issue-60-dlh-5vl-invariant-domain-safeguard-2026-09-13`

Initial activation comment:

`5649259224`

Builder must not begin until CURRENT records this activation ID and a final activation-refresh comment confirms the post-sync live main.

## Latest accepted gate — Issue #59 / DLH-5V-K

Accepted candidate / integration:

`08f0135de5a60d05eda7184c367e1705da69757d`

Reviewer acceptance:

`5649245347`

Acceptance integration:

`5649248162`

Accepted verdict:

`DLH_5VK_ACCEPTED__TERMINAL_B_H2_CONFIRMED__LEGACY_EXTERNAL_PRICE_SENSITIVITY_REAL__SELECTED_Q_EFFECTIVE_DOMAIN_GAP_REMAINS__STABILIZATION_DIAGNOSTIC_NEXT`

Accepted interpretation:

- the frozen legacy solver has reproducible external-price sensitivity;
- tested convergent `r_a` points include `0.07,0.09,0.11,0.12`, with sampled failures immediately outside at `0.065` and `0.125`; this is a sampled span/bracket, not a continuous-interval theorem;
- legacy convergence alone is not economic-quality or exact-unbounded-HJB validation: the accepted legacy `v_b` floor is materially active and non-positive finite-difference `V_b` occurs at converged points;
- the selected-Q solver exits its boundary effective domain at iteration 2 even at the central historical sentinel `r_a=0.07`;
- therefore external-price discipline and a selected-Q invariant-domain numerical issue both remain relevant.

## Active diagnostic route

Issue #60 tests whether a deterministic safeguarded value update can keep every accepted selected-Q iterate inside the required boundary `p_b>0` effective domain without changing the target fixed-point equation.

Frozen central case:

```text
m=1
W_max=10
r_a=0.07
r_b=0.02
w=1.00
borrowing_rate_gap=0
rho=0.02
gamma_c=2
phi=5
chi_0=0.1
chi_1=2
a_bar=1e-6
tau=0.15
z=[0.8,1.3]
delta=1000
tolerance_iter=1e-7
tolerance_Bellman=1e-3
max_iterations=1000
n_c=n_d=9
```

Authorized safeguard only:

```text
V_trial(lambda)=V_old+lambda*(V_raw-V_old)
lambda in {1,1/2,...,2^-20}
accept largest lambda with all required boundary p_b > 1e-12
```

The `1e-12` margin is an iterate-acceptance tolerance only; no derivative clipping/flooring is allowed.

Exactly one safeguarded run and one deterministic repeat are authorized. Final PASS requires the accepted final Bellman residual criterion, not merely a tiny damped step.

## Frozen household / same-process authority

Accepted household oracle remains immutable/read-only:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb337f1b02b3fe33c51e`

Accepted selected-Q source remains immutable/read-only:

`src/deep_learning_hank/two_asset/boundary_hjb_selected_q.py`

Git blob:

`7ea342ccbe15d852b90743b14bb4b02977c2d78b`

```text
HJB boundary policy <=> KFE boundary transition law
Q backward
future KFE exactly Q^T
Q_ij>=0 for i!=j
Q_ii=-sum of ACTUAL represented outgoing rates
Q1=0 by construction
same selected candidate/rates for HJB and future KFE
```

Pinning/normalization may never repair leakage.

Stationary KFE remains **NOT AUTHORIZED**.

## Interpretation ceiling

No price sweep, no alternative lambda grid/margin, no pseudo-time adaptation, no continuation, no hard economic bounds, no KFE/stationary KFE, no SCC/global-Q, no production Wmax/resolution, no GE/multi-region/neural/nominal/calibration/policy/welfare/Results.

## Current authoritative files

- `tasks/TASK_INDEX_CURRENT.md`
- `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
- Issue #60 body/comments.
