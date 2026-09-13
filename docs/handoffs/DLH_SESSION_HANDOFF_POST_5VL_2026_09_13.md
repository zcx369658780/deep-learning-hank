# DeepLearning-HANK Scientific Handoff — Post DLH-5V-L

Date: 2026-09-13
Repository: `zcx369658780/deep-learning-hank`

## Current authority

Live `main` at handoff creation: `9b1538feabe2cc4634653721e725ee3e46d449bb`.

Latest accepted gate: Issue #60 / DLH-5V-L, CLOSED completed at Terminal C.

Accepted candidate / integration:
`9b1538feabe2cc4634653721e725ee3e46d449bb`

Reviewer acceptance:
`5650057012`

Acceptance integration:
`5650059195`

Accepted verdict:
`DLH_5VL_ACCEPTED__TERMINAL_C_CONFIRMED__VALUE_UPDATE_ONLY_INVARIANT_SAFEGUARD_FAILS_ON_FROZEN_CENTRAL_TRAJECTORY__RAW_OPERATOR_ROUTE_RECONSIDERATION_REQUIRED`

Accepted Terminal C:
`DLH_5VL_INVARIANT_DOMAIN_SAFEGUARD__NO_VIABLE_POSITIVE_EFFECTIVE_DOMAIN_UPDATE__ROUTE_RECONSIDERATION_REQUIRED`

## Frozen household / same-process authority

Household oracle remains read-only:
`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`
blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`.

Selected-Q implementation remains read-only:
`src/deep_learning_hank/two_asset/boundary_hjb_selected_q.py`
blob `7ea342ccbe15d852b90743b14bb4b02977c2d78b`.

Binding law:
- HJB boundary policy <=> KFE boundary transition law;
- backward `Q`, future forward process exactly `Q^T`;
- off-diagonal rates nonnegative;
- diagonal equals minus actual represented outgoing rates;
- `Q 1 = 0` by construction;
- same selected candidate/rates in HJB score and Q.

Stationary KFE remains NOT AUTHORIZED.

## Accepted scientific results through Issue #60

### Issue #58
Boundary selected-Q implementation materially accepted. Classifier/sector/representability/first-moment checks pass. Frozen central HJB exits accepted positive-liquid-marginal effective domain at iteration 2.

### Issue #59
Fixed-household price-envelope diagnostic accepted at H2: external prices materially affect the legacy rectangular solver, but price discipline alone does not cure selected-Q effective-domain exit. Legacy convergence evidence is a sampled numerical envelope, not a theorem or full economic-validity certificate.

### Issue #60
A value-update-only invariant-domain safeguard was tested on the frozen central selected-Q case. It preserved the domain for 17 accepted iterations but was not a viable convergence route. The minimum accepted lambda reached `2^-20`; the 18th request had no authorized dyadic step preserving `p_b > 1e-12`. The late-path raw update remained materially nonzero. This evidence is trajectory-bounded and does NOT prove that no positive-domain fixed point exists.

Terminal metadata is now cleanly separated:
- global raw minimum `p_b ≈ -0.3369237` at F2 `(j,i)=(6,24)`, `z=1`;
- margin-binding state F3 `(16,8)`, `z=1` with same-state `p_old≈1.8129e-12`, `p_raw≈-1.0825e-6`;
- same-state `lambda_margin≈7.5094e-7 < 2^-20≈9.5367e-7`;
- zero crossing is separately named and not used as the acceptance criterion.

## New active scientific route

Issue #61 / DLH-5V-M has been published:
`DLH-5V-M: Test adaptive pseudo-time resolvent safeguard on the frozen central selected-Q HJB case`.

Task type:
`SCIENTIFIC_NUMERICAL_DIAGNOSTIC__ADAPTIVE_PSEUDO_TIME_RESOLVENT_EFFECTIVE_DOMAIN`.

Scientific idea:
for each accepted `V_old`, build the accepted `Q(V_old),u(V_old)` once and solve the pseudo-time resolvent for
`delta_k = 1000*2^-k`, `k=0..20`, choosing the largest delta whose direct resolvent output keeps all required boundary `p_b > 1e-12`.

This differs from Issue #60: Issue #60 damped an already-computed fixed-`delta=1000` update; Issue #61 changes the implicit resolvent step itself while preserving the same fixed-point equation. No additional value damping is allowed.

## Hard ceilings for Issue #61

No household/source mutation; no price sweep; no alternative delta ladder/margin; no Wmax/resolution work; no continuation/homotopy; no KFE/stationary KFE; no SCC/global-Q; no GE/multi-region/neural/nominal/calibration/policy/welfare/Results.

Exact Builder allowlist for Issue #61:
1. `src/deep_learning_hank/two_asset/adaptive_resolvent_hjb.py`
2. `tests/test_dlh_5vm_adaptive_resolvent.py`
3. `reports/dlh_5vm_adaptive_resolvent_2026_09_13/DLH_5VM_ADAPTIVE_RESOLVENT_REPORT.md`
4. `reports/dlh_5vm_adaptive_resolvent_2026_09_13/DLH_5VM_RESOLVENT_TRACE.csv`

Issue #61 must not begin until CURRENT governance is synchronized and final activation refresh is published.
