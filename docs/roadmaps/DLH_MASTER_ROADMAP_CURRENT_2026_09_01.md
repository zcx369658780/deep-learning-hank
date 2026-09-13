# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.47  
**Date:** 2026-09-14  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** DLH-5V-R / ISSUE #66 NEXT ACTIVE — F0 FINAL-RATE PROVENANCE AND OPERATOR-CONSISTENCY AUDIT (BUILDER NOT YET OPERATIVE)

---

## 0. Long-run objective

Build a hybrid structural–learned regional HANK platform in which household HJB/KFE, aggregation, firm/accounting and later nominal-HANK equations remain explicit structural economics, while hard-to-specify cross-regional mappings become learned modules only after household and equilibrium foundations pass scientific and numerical validation.

The first learned object remains regional labor/spatial mapping `W^L`. Neural training remains downstream.

---

## 1. Accepted household / finite-domain foundation

Accepted household oracle:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Accepted finite production-domain family:

```text
D_W(W_max)={0<=a<=10,b>=-2,a+b<=W_max}
```

No numerical production `W_max` is selected.

Binding law:

```text
HJB boundary policy <=> KFE boundary transition law
```

Restricted-Voronoi cells remain the accepted state partition / mass-volume geometry unless a later Owner-authorized route changes them. The same selected backward generator `Q` must define future forward mass dynamics `p_dot=Q^T p`.

Stationary KFE remains **NOT AUTHORIZED**.

---

## 2. Accepted finite-process provenance — Issues #54–#56

- Issue #54 / DLH-5V-F: endpoint exact finite-process representability obstruction ACCEPTED.
- Issue #55 / DLH-5V-G: strong raw admitted-drift-set graph target obstruction ACCEPTED.
- Issue #56 / DLH-5V-H: state-constraint operator-consistency audit accepted at Outcome B.

Issue #56 accepted verdict:

`DLH_5VH_ACCEPTED__OUTCOME_B_CONFIRMED__UNBOUNDED_CONTROL_NUMERICAL_SCHEME_AND_STATE_CONSTRAINT_CONVERGENCE_APPLICATION_BLOCK_FROZEN`

One bounded unbounded-control/state-constraint convergence-application block remains explicit and unsolved.

---

## 3. Issue #57 / DLH-5V-I — boundary-HJB production-scheme design — OUTCOME A ACCEPTED

Accepted candidate / integration:

`3e450cf8ae177015e68ee7e05ecc5d6be7b2f8ec`

Reviewer acceptance: `5644767550`  
Acceptance integration: `5644769439`

Frozen authority includes unique Route-A F0–F11 ownership, explicit representability exclusions, algorithm-only numerical brackets, rates from local drift before scoring, ONE deterministic global selection, same selected rates in conservative backward Q, accepted `grid.switch_matrix`, pseudo-time HJB integration, separate iterate convergence/final Bellman residual, and named failures with no silent fallback.

---

## 4. Issue #58 / DLH-5V-J — boundary-HJB implementation + local validation — TERMINAL B ACCEPTED

Accepted candidate / integration:

`7b564d1b7d7aaf76b808135b192646e0ec1f5f08`

Reviewer acceptance: `5646205500`  
Acceptance integration: `5646215533`

Accepted result:

- F0 common-input regression PASS;
- Route-A family/sector/representability/first-moment checks PASS;
- first-iteration selected backward Q conservative and deterministic;
- frozen validation exits the `p_b>0` boundary effective domain at iteration 2;
- corrected implementation raises `DERIVATIVE_EFFECTIVE_DOMAIN_FAILURE` before candidate/bracket search.

This is not accepted as a household-equation, geometry, or sector-algebra contradiction.

---

## 5. Issue #59 / DLH-5V-K — fixed-household external-price envelope — TERMINAL B / H2 ACCEPTED

Accepted candidate / integration:

`08f0135de5a60d05eda7184c367e1705da69757d`

Reviewer acceptance:

`5649245347`

Acceptance integration:

`5649248162`

Accepted verdict:

`DLH_5VK_ACCEPTED__TERMINAL_B_H2_CONFIRMED__LEGACY_EXTERNAL_PRICE_SENSITIVITY_REAL__SELECTED_Q_EFFECTIVE_DOMAIN_GAP_REMAINS__STABILIZATION_DIAGNOSTIC_NEXT`

Accepted scientific interpretation:

- external prices materially affect the frozen legacy HJB solver;
- sampled convergent `r_a` points include `0.07,0.09,0.11,0.12`, while `0.065` and `0.125` fail; this is an observed sampled span / transition bracket, not a theorem that every `r_a` in `[0.07,0.12]` converges;
- legacy numerical convergence does not by itself validate economic quality or the exact unbounded-control HJB because the accepted source `v_b` floor is active at nontrivial shares and non-positive finite-difference `V_b` occurs at converged points;
- the current selected-Q solver still exits its accepted boundary effective domain at the central tested sentinel `r_a=0.07`;
- cross-solver convergence differences do not establish a geometry cause or a globally price-independent selected-Q failure.

Therefore future GE work should preserve external-price search discipline, but price envelopes are not accepted as a cure for the selected-Q invariant-domain gap.

---

## 6. Issue #60 / DLH-5V-L — invariant-domain safeguard diagnostic — TERMINAL C ACCEPTED / CLOSED

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

Accepted scientific interpretation:

- pure value-update damping preserves the positive-`p_b` domain for a short path but is not a viable convergence route on the frozen central trajectory;
- 17 accepted iterations remain in-domain, then no authorized dyadic value-damping step exists;
- this is trajectory-bounded evidence only and does NOT prove global nonexistence of a positive-domain HJB fixed point;
- external-price sensitivity from Issue #59 remains real but does not resolve the selected-Q invariant-domain problem.

---

## 7. Issue #61 / DLH-5V-M — adaptive pseudo-time / resolvent diagnostic — TERMINAL C ACCEPTED / CLOSED

Title:

`DLH-5V-M: Adaptive pseudo-time / resolvent safeguard diagnostic on the central selected-Q HJB case`

Task type:

`SCIENTIFIC_NUMERICAL_DIAGNOSTIC__ADAPTIVE_PSEUDO_TIME_RESOLVENT_EFFECTIVE_DOMAIN`

Authority marker:

`DLH_5VM_ADAPTIVE_RESOLVENT_DIAGNOSTIC_AUTHORIZED`

Accepted candidate / integration:

`2721dadbfd0ad49813f12c8424f6be77fcaf3f85`

Reviewer acceptance:

`5651495744`

Acceptance integration:

`5651496951`

Accepted verdict:

`DLH_5VM_ACCEPTED__TERMINAL_C_CONFIRMED__ADAPTIVE_RESOLVENT_LADDER_EXHAUSTED_ON_FROZEN_CENTRAL_TRAJECTORY__ROUTE_RECONSIDERATION_REQUIRED`

Accepted Terminal C:

`DLH_5VM_ADAPTIVE_RESOLVENT__NO_VIABLE_EFFECTIVE_DOMAIN_RESOLVENT_STEP__ROUTE_RECONSIDERATION_REQUIRED`

Accepted scientific interpretation (trajectory-bounded):

- the adaptive pseudo-time/resolvent route accepted 2 positive-domain iterations on the frozen central trajectory;
- at the third update request every authorized delta on the ladder {1000·2^-k, k=0..20} is infeasible (the smallest-delta limiting failure is at F3 (13,13), z=1);
- this does NOT prove global nonexistence or uniqueness of a positive-domain HJB fixed point;
- it does NOT exclude another basin, a continuation/homotopy path, or another fixed-point-preserving operator;
- the R1 fail-closed non-finite-boundary handling is part of the accepted implementation;
- together with Issue #60 value damping, the two tested stabilization routes are BOTH negative evidence on the frozen central selected-Q case.

Reference handoff: `docs/handoffs/DLH_SESSION_HANDOFF_POST_5VL_2026_09_13.md`.

### 7.1 Frozen central selected-Q case (executed design, unchanged)

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

All household parameters, grid/domain, initialization, Q/candidate rules and search-bracket semantics remain frozen.

### 7.2 Authorized adaptive resolvent only

At each accepted `V_old`, build the accepted selected policy, utility and conservative backward `Q` from `V_old` exactly once, then:

```text
[(1/delta + rho)I - Q(V_old)] V_delta = u(V_old) + V_old/delta
delta_k = 1000*2^-k, k = 0..20, descending
choose the largest delta whose V_trial satisfies all required boundary p_b > 1e-12
accept V_trial directly — NO additional value damping
```

The `1e-12` margin is an iterate-acceptance tolerance only; no derivative is clipped/floored and the margin never enters FOCs or Bellman scoring. No value-update line search from Issue #60 may be layered on top.

Exactly one central-case run and one deterministic repeat are authorized.

### 7.3 PASS standard

Outcome A requires:

- accepted iterates stay inside the boundary effective domain;
- convergence `max|V_new-V_old| < 1e-7` within 1000 accepted iterations;
- final re-selection on final V;
- final `||rho V - [u_selected(V)+Q_selected(V)V]||_inf <= 1e-3`;
- conservative selected Q within accepted row-sum tolerance;
- no accepted artificial bracket binding;
- deterministic repeat.

A tiny delta-induced update without final Bellman residual PASS is stagnation (`RESOLVENT_STAGNATION`), not convergence.

---

## 8. Issue #62 / DLH-5V-N — local continuous resolvent / domain-margin geometry — OUTCOME A ACCEPTED / CLOSED

Title:

`DLH-5V-N: Diagnose local continuous resolvent/domain-margin geometry at the Issue #61 terminal accepted state`

Task type:

`SCIENTIFIC_NUMERICAL_DIAGNOSTIC__LOCAL_CONTINUOUS_RESOLVENT_DOMAIN_GEOMETRY`

Owner / Reviewer route decision:

`APPROVE_LOCAL_CONTINUOUS_RESOLVENT_DOMAIN_GEOMETRY_DIAGNOSTIC_AFTER_5VM_TERMINAL_C`

Authority marker:

`DLH_5VN_LOCAL_RESOLVENT_DOMAIN_GEOMETRY_DIAGNOSTIC_AUTHORIZED`

Builder branch (integrated into `main`):

`dsh/issue-62-dlh-5vn-local-resolvent-geometry-2026-09-13`

Initial authoritative activation comment:

`5651730413` (final authoritative activation-refresh `5651801939`)

Accepted candidate / integration:

`7ba2d75978033064c588230b15d760b60bec9e00`

Reviewer acceptance:

`5652208157`

Acceptance integration:

`5652209372`

Accepted verdict:

`DLH_5VN_ACCEPTED__OUTCOME_A_CONFIRMED__POSITIVE_SUBFLOOR_LOCAL_SAFE_STEP_AND_REPRODUCIBLE_MARGIN_CROSSING__CONTINUATION_DESIGN_GATE_READY`

Accepted terminal:

`DLH_5VN_LOCAL_RESOLVENT_GEOMETRY__POSITIVE_SUBFLOOR_SAFE_STEP_AND_REPRODUCIBLE_MARGIN_CROSSING__CONTINUATION_DESIGN_GATE_READY`

### 8.0 Accepted scientific interpretation (trajectory-bounded / local evidence)

- the Issue #61 terminal event is identified as authorized **ladder-floor
  exhaustion**;
- the frozen Issue #61 terminal operator possesses a strictly positive
  sub-floor local safe delta;
- the continuous margin crossing is reproducible inside the fixed bracket
  `[0, 1000·2^-20]`;
- `delta_cross ≈ 7.8246e-4`; `delta_cross / old ladder floor ≈ 0.8205`;
- first-order prediction `delta_margin_linear ≈ 7.5943e-4`;
  `delta_cross / delta_margin_linear ≈ 1.0303`;
- the limiting state near root / below / above is F3 (13,13), z=1;
- corrected directional accounting: 186 required boundary states, 105
  negative-direction, and 40 `i == 0` V-independent states with
  `dp_b/delta|_0` exactly 0;
- the R1 true fail-closed non-finite handling is part of the accepted
  implementation;
- this is trajectory-bounded / local evidence only: it does NOT prove global
  uniqueness, does NOT prove the mathematically first positive crossing, does
  NOT prove any actual next HJB iterate is acceptable, does NOT prove
  continuation convergence, and does NOT authorize KFE / stationary KFE.

### 8.1 Executed design — scientific question

At the last accepted Issue #61 state immediately before its terminal third
update request, does the frozen selected-Q resolvent possess a strictly
positive local effective-domain-safe step below the Issue #61 ladder floor, and
what is the local domain-margin geometry? The Issue distinguishes ladder-floor
exhaustion (sufficiently small positive continuous delta remains locally
feasible) from a deeper local operator/domain pathology (non-finite,
inconsistent, or no reproducible positive local step). Executed and accepted:
the terminal event was ladder-floor exhaustion, not a local operator/domain
pathology.

### 8.2 Executed design — frozen terminal-state provenance and object

Exactly the accepted Issue #61 frozen central configuration and initialization
(`m=1, W_max=10, b_min=-2, a_max=10; r_a=0.07, r_b=0.02, w=1.00, gap=0;
rho=0.02, gamma_c=2, phi=5, chi_0=0.1, chi_1=2, a_bar=1e-6; tau=0.15;
z=[0.8,1.3]; n_c=n_d=9, bracket expansion x4 max 3; PB_MARGIN=1e-12`). The
accepted Issue #61 trajectory was reconstructed deterministically and STOPPED
at its last accepted state after exactly 2 accepted updates; the reconstruction
reproduces the accepted Issue #61 trace and terminal-state boundary minimum
(min accepted boundary p_b = 0.009853744163134845 at F3 (13,13), z=1 node 332).
At this frozen `V_*`, selected policy / utility / conservative backward `Q_*`
was built exactly once; the same frozen `(V_*, Q_*, u_*)` was used for every
local delta evaluation; no policy re-selection as delta varies.

Equivalent continuous resolvent representation (well-defined at delta=0):

```text
[I + delta*(rho I - Q_*)] V(delta) = V_* + delta*u_*
V(0) = V_*
```

### 8.3 Executed design — authorized local diagnostics only

- exact infinitesimal direction `dV/delta|_0 = u_* + Q_* V_* - rho V_*`
  (finite; max abs 10.45);
- directional derivatives `dp_b/delta|_0` for every required non-F0 boundary
  state, per the accepted derivative semantics: backward finite-difference of
  `dV` for regular states and EXACTLY 0 on the accepted V-independent b_min
  face (`i == 0`; R1-corrected, 40 states);
- first-order margin-crossing predictions
  `delta_margin_linear = (p_b(V_*) - PB_MARGIN)/(-dp_b/delta|_0)` for every
  negative-direction state; minimum positive finite
  `delta_margin_linear = 7.5943e-4` at F3 (13,13), z=1 (the wall state);
- ONE deterministic bracketed continuous root solve of
  `g(delta) = min_required_boundary p_b(V(delta)) - PB_MARGIN` on the fixed
  bracket `[0, 1000*2^-20]`, after verifying `g(0) > 0`
  (+0.009853744162134845) and `g(1000*2^-20) < 0`
  (−0.002078969754188379); reproducible root `delta_cross = 7.8246e-4`
  strictly inside the bracket; `g(delta_cross) ≈ -1.64e-14`; worst state at
  root / below / above = F3 (13,13), z=1; direct verification at
  `(1-1e-6)*delta_cross` (`g = +9.56e-9 > 0`, feasible) and
  `(1+1e-6)*delta_cross` (`g = -9.56e-9 < 0`, infeasible);
  `delta_cross/(1000*2^-20) = 0.8205`; ratio to the minimum finite first-order
  `delta_margin_linear = 1.0303`.

Non-finite required boundary or directional evidence fails closed (RAISES
`LocalGeometryFailure` — R1; never misread as feasible). The linear prediction
is a local diagnostic only. The bracketed root is a reproducible
sign-changing crossing of the global boundary margin on the frozen local
operator — not a claim of global uniqueness or of the first positive crossing.

Executed exactly: ONE deterministic reconstruction of the accepted Issue #61
trajectory; ONE local infinitesimal-direction diagnostic; ONE bracketed
continuous crossing solve on `[0, 1000*2^-20]`; ONE deterministic repeat of
the full local diagnostic (bit-identical).

### 8.4 Executed design — terminal set (exactly ONE reported)

- A `DLH_5VN_LOCAL_RESOLVENT_GEOMETRY__POSITIVE_SUBFLOOR_SAFE_STEP_AND_REPRODUCIBLE_MARGIN_CROSSING__CONTINUATION_DESIGN_GATE_READY` — **ACCEPTED**
- B `DLH_5VN_LOCAL_RESOLVENT_GEOMETRY__POSITIVE_LOCAL_FEASIBILITY_WITH_STIFF_OR_NONUNIQUE_MARGIN_GEOMETRY__FURTHER_DESIGN_REQUIRED`
- C `DLH_5VN_LOCAL_RESOLVENT_GEOMETRY__NONFINITE_OR_INCONSISTENT_LOCAL_DIRECTION_OR_MARGIN_EVIDENCE__BOUNDARY_HJB_ROUTE_REVIEW_REQUIRED`
- Blocked `BLOCKED_DLH_5VN_AUTHORITY_OR_DEPENDENCY_CONFLICT`

### 8.5 Executed design — forbidden (respected)

No accepted third HJB iterate; no multi-step continuation/homotopy; no
extension of the Issue #61 discrete ladder as the experiment; no
economics/prices/grid/domain/`PB_MARGIN` change; no mutation of the household
oracle, selected-Q source, or accepted Issue #61 implementation (all
read-only); no KFE/stationary KFE; no successor; no PR/merge/close/self-accept
by the Builder.

---

## 8.6 Issue #63 / DLH-5V-O — continuous fraction-to-boundary pseudo-transient continuation — TERMINAL B ACCEPTED / CLOSED

Title:

`DLH-5V-O: Test continuous fraction-to-boundary pseudo-transient continuation on the frozen central selected-Q HJB case`

Task type:

`SCIENTIFIC_NUMERICAL_DIAGNOSTIC__CONTINUOUS_FRACTION_TO_BOUNDARY_RESOLVENT_CONTINUATION`

Owner / Reviewer route decision:

`APPROVE_CONTINUOUS_FRACTION_TO_BOUNDARY_RESOLVENT_CONTINUATION_AFTER_5VN_OUTCOME_A`

Authority marker:

`DLH_5VO_CONTINUOUS_FTB_RESOLVENT_CONTINUATION_AUTHORIZED`

Initial authoritative activation comment:

`5652277509` (final authoritative activation-refresh `5652449297`)

Builder branch (integrated into `main`):

`dsh/issue-63-dlh-5vo-continuous-ftb-resolvent-2026-09-13`

Accepted candidate / integration:

`a552dc6ebb2c82ad19fe26cd747d362ceecdfdcc`

Reviewer acceptance:

`5652576918`

Acceptance integration:

`5652579072`

Accepted verdict:

`DLH_5VO_ACCEPTED__TERMINAL_B_CONFIRMED__CONTINUOUS_FTB_PRESERVES_EFFECTIVE_DOMAIN_BUT_STAGNATES_AT_BOUNDARY_WITH_MATERIAL_BELLMAN_RESIDUAL__ROUTE_RECONSIDERATION_REQUIRED`

Accepted terminal:

`DLH_5VO_CONTINUOUS_FTB_RESOLVENT__EFFECTIVE_DOMAIN_PRESERVED_BUT_VALIDATED_HJB_CONVERGENCE_NOT_REACHED`

### 8.6.0 Accepted scientific interpretation (trajectory-bounded)

- the continuous FTB controller successfully preserves the effective domain on
  the frozen central selected-Q case;
- 8 accepted root-controlled FTB steps; cap-direct = 0, root-controlled = 8;
- the limiting wall state is locked to F3 (13,13), z=1 on the accepted path;
- selected delta and the boundary margin shrink approximately geometrically;
- final min boundary p_b ≈ 4.81e-9, still > `PB_MARGIN=1e-12`;
- the accepted-step trigger fired at iteration 8:
  `max|V_{n+1}-V_n| ≈ 3.66e-8 < 1e-7`;
- but the final re-selection / validation shows Bellman residual
  ≈ 490.756 >> 1e-3;
- the raw fixed-point direction norm stays ≈ 10.43-10.88 on the trajectory and
  does NOT approach 0;
- accepted interpretation = **FTB_STAGNATION**: a tiny step caused by
  boundary-following geometry, NOT validated HJB convergence;
- Q conservative, 0 artificial bindings, 0 optimizer expansions;
- deterministic repeat identical;
- the Issue #62 positive local safe radius is real but does NOT suffice for
  validated convergence under this frozen FTB controller;
- trajectory-bounded evidence only: does NOT prove all FTB controllers
  globally fail to converge; does NOT prove the absence of another
  fixed-point-preserving direction/operator; does NOT prove the HJB fixed
  point does not exist; does NOT authorize KFE / stationary KFE.

Non-blocking metadata observation (CURRENT / roadmap wording): the candidate
result field `converged=True` means ONLY that the accepted-step statistic
trigger was reached; scientific validated convergence = FALSE (final Bellman
validation failed). Recommended wording:
`step-size convergence trigger reached; validated HJB convergence failed (FTB_STAGNATION)`.

### 8.6.1 Executed design — scientific question

Can a fixed-point-preserving pseudo-transient resolvent iteration converge on
the single frozen central selected-Q HJB case when each accepted step is chosen
by a continuous fraction-to-boundary rule, rather than by a pre-truncated
discrete delta ladder? This is the first authorized multi-step continuation
test after Issue #62 established a positive local safe radius.

### 8.6.2 Executed design — frozen central case and fixed-point-preserving resolvent

Exactly the accepted Issue #61/#62 central configuration and initialization
(`m=1, W_max=10, b_min=-2, a_max=10; r_a=0.07, r_b=0.02, w=1.00, gap=0;
rho=0.02, gamma_c=2, phi=5, chi_0=0.1, chi_1=2, a_bar=1e-6; tau=0.15;
z=[0.8,1.3]; tolerance_iter=1e-7, tolerance_Bellman=1e-3, max_iterations=1000;
n_c=n_d=9, bracket expansion x4 max 3; PB_MARGIN=1e-12`). At every accepted
iterate `V_n`, selected policy / utility / conservative backward `Q_n,u_n` are
built **exactly once** and reused for ALL delta/controller evaluations within
that iterate (no policy re-selection as delta varies). For trial `delta >= 0`
solve only:

```text
[I + delta*(rho I - Q_n)] V_n(delta) = V_n + delta*u_n
```

For positive delta this is algebraically equivalent to the accepted Issue #61
resolvent and preserves the same HJB fixed-point equation.

### 8.6.3 Executed design — authorized continuous fraction-to-boundary controller (frozen)

Controller constants frozen: `DELTA_CAP=1000`, `TAU_FTB=0.90`,
`RETAIN=1-TAU_FTB=0.10`, `EPS_FTB=1e-6`, `MAX_BRACKET_HALVINGS=60`.

- `m0 = min_required_boundary p_b(V_n) - PB_MARGIN`; require finite `m0 > 0`;
- `m_target = RETAIN*m0 = 0.10*m0`;
- `h_n(delta) = min_required_boundary p_b(V_n(delta)) - PB_MARGIN - m_target`
  (accepted step must retain at least 10% of the current margin above
  `PB_MARGIN`);
- if finite `h_n(DELTA_CAP) >= 0`: `delta_selected = DELTA_CAP`;
- else construct a bracket ONLY for the continuous root solve by deterministic
  halving from `DELTA_CAP` (`1000, 500, 250, ...`) until the first finite
  positive `h_n(delta_lo) > 0` with the immediately previous point
  `h_n(delta_hi) < 0`; the halving probes are **bracket construction only**,
  NOT an accepted ladder, and no probe is accepted merely because it is
  feasible;
- on the first sign-changing bracket, deterministic `brentq` on `h_n = 0` with
  root `delta_ftb`; `delta_selected = (1 - EPS_FTB)*delta_ftb`;
- directly verify at `delta_selected`: all required boundary `p_b` finite,
  `min p_b > PB_MARGIN`, retained margin `>= m_target` (declared numerical root
  tolerance);
- accept `V_{n+1} = V_n(delta_selected)` directly — NO value damping;
- Bellman residual never used for step selection;
- no finite feasible bracket within 60 halvings, or non-finite required
  evidence: surface `FTB_STEP_CONSTRUCTION_FAILURE` and STOP (fail closed);
- no controller-parameter tuning after seeing trajectory results.

### 8.6.4 Executed design — convergence, stagnation, final validation, execution design

Accepted-iterate convergence trigger: `max|V_{n+1}-V_n| < 1e-7` (a tiny step is
not sufficient). On trigger, recompute the complete selected policy/rates/Q
from final V and require all of: all required boundary `p_b > 1e-12`;
`||rho V - [u_selected(V)+Q_selected(V)V]||_inf <= 1e-3`; conservative Q within
accepted row-sum tolerance; no accepted artificial bracket binding;
deterministic repeat. Step criterion reached but final Bellman residual fails =
`FTB_STAGNATION` (not convergence). 1000 accepted iterations without validated
convergence = bounded non-convergence.

Execute exactly: ONE continuous fraction-to-boundary continuation run on the
frozen central case + ONE deterministic repeat of the same run. No second
controller parameter, no alternative `TAU_FTB`, no alternative cap, no price
case, no Wmax/resolution case.

### 8.6.5 Builder allowlist — four new paths only

1. `src/deep_learning_hank/two_asset/continuous_ftb_resolvent_hjb.py`
2. `tests/test_dlh_5vo_continuous_ftb_resolvent.py`
3. `reports/dlh_5vo_continuous_ftb_resolvent_2026_09_13/DLH_5VO_CONTINUOUS_FTB_RESOLVENT_REPORT.md`
4. `reports/dlh_5vo_continuous_ftb_resolvent_2026_09_13/DLH_5VO_CONTINUATION_TRACE.csv`

### 8.6.6 Executed design — terminal set (exactly ONE reported)

- A `DLH_5VO_CONTINUOUS_FTB_RESOLVENT__CENTRAL_HJB_CONVERGES_WITH_FINAL_BELLMAN_PASS__ROBUSTNESS_GATE_READY`
- B `DLH_5VO_CONTINUOUS_FTB_RESOLVENT__EFFECTIVE_DOMAIN_PRESERVED_BUT_VALIDATED_HJB_CONVERGENCE_NOT_REACHED` — **ACCEPTED**
- C `DLH_5VO_CONTINUOUS_FTB_RESOLVENT__NO_VIABLE_FRACTION_TO_BOUNDARY_STEP__BOUNDARY_HJB_ROUTE_REVIEW_REQUIRED`
- Blocked `BLOCKED_DLH_5VO_AUTHORITY_OR_DEPENDENCY_CONFLICT`

### 8.6.7 Executed design — forbidden (respected)

No mutation of the household oracle, selected-Q source, or Issue #61 / Issue #62
accepted implementations (all read-only); no economics/prices/grid/domain/
initialization/control-search/tolerances/`PB_MARGIN`/controller-constant change;
no value damping; no clip/floor/replace of `p_b`; no Bellman-residual-based step
selection; no price or Wmax/resolution sweeps; no parameter tuning after
results; no KFE/stationary KFE; no `solve_household_steady_state`; no SCC/
global-Q/GE/multi-region/neural/nominal/calibration/policy/welfare/Results; no
PR; no merge; no Issue close; no successor; no self-accept.

---

## 8.7 Issue #64 / DLH-5V-P — frozen-policy Newton geometry diagnostic — TERMINAL B ACCEPTED / CLOSED

Title:

`DLH-5V-P: Diagnose Issue #63 stagnation residual decomposition and frozen-policy Newton boundary geometry`

Task type:

`SCIENTIFIC_NUMERICAL_DIAGNOSTIC__FTB_STAGNATION_RESIDUAL_DECOMPOSITION_AND_FROZEN_POLICY_NEWTON_GEOMETRY`

Owner / Reviewer route decision:

`APPROVE_FTB_STAGNATION_RESIDUAL_DECOMPOSITION_AND_FROZEN_POLICY_NEWTON_GEOMETRY_AFTER_5VO_TERMINAL_B`

Authority marker:

`DLH_5VP_STAGNATION_NEWTON_GEOMETRY_DIAGNOSTIC_AUTHORIZED`

Initial authoritative activation comment:

`5652648524`

Dedicated future Builder branch:

`dsh/issue-64-dlh-5vp-stagnation-newton-geometry-2026-09-13`

Builder execution is **complete**: the Issue #64 diagnostic was executed on its
dedicated branch (`dsh/issue-64-dlh-5vp-stagnation-newton-geometry-2026-09-13`)
after the activation comments (initial `5652648524` and the final
authoritative activation-refresh confirming the post-sync live `main`), and
the candidate was ACCEPTED / CLOSED as recorded below.

Issue #64 is **ACCEPTED / CLOSED** at Terminal B. Accepted candidate /
integration: `5db144a65796ff6a7e0f59d2d2a75a0446c13b83`; reviewer acceptance
`5653190792`; acceptance integration `5653192646`. Accepted verdict:
`DLH_5VP_ACCEPTED__TERMINAL_B_CONFIRMED__F0_FINAL_SEMANTICS_DOMINATE_VALIDATION_GAP__FROZEN_POLICY_NEWTON_IS_BOUNDARY_SAFE_BUT_GEOMETRICALLY_CAPPED_AND_NONLINEAR_RESIDUAL_REDUCTION_INSUFFICIENT__FURTHER_DIRECTION_DESIGN_REQUIRED`;
accepted terminal:
`DLH_5VP_STAGNATION_NEWTON_GEOMETRY__POSITIVE_BOUNDARY_SAFE_NEWTON_STEP_BUT_NONLINEAR_RESIDUAL_REDUCTION_INSUFFICIENT__FURTHER_DIRECTION_DESIGN_REQUIRED`.
Accepted interpretation (trajectory-bounded / local evidence only): the
accepted Issue #63 stagnation state was reconstructed exactly (8 root-
controlled FTB steps; final statistic ≈ 3.66e-8; final min p_b ≈ 4.81e-9; wall
state F3 (13,13), z=1; accepted final-validation residual ≈ 490.756
reproduced); `||R_iter||_inf = 10.435094313164921`,
`||R_final_stale||_inf = 490.7560425919994`,
`||R_final_stale - R_iter||_inf = 488.0988429898615` with the difference
entirely on F0 rows and non-F0 boundary difference exactly 0; the frozen-
policy Newton solve is finite/correct (`||J_iter d_N + R_iter||_inf ≈ 6.96e-11`)
but the same F3 (13,13), z=1 wall caps the safe fraction at
`alpha_cross ≈ 1.87e-4`, and both authorized trials leave the nonlinear
residuals essentially unchanged (ratios ≈ 0.9998-0.9999 >> 0.50) → plain
frozen-policy Newton is not a viable local residual-reducing route under this
wall geometry; this does NOT prove HJB fixed-point nonexistence or failure of
future constrained/tangent directions; sector-switch count 0 must not be
overinterpreted as proof that continuous controls are unchanged. The F0
final-validation semantic gap is audited next by Issue #65. Stationary KFE
remains **NOT AUTHORIZED**.

### 8.7.1 Scientific question

At the accepted Issue #63 FTB-stagnation state, is the obstruction mainly a
boundary-normal geometry problem that also makes a frozen-policy Newton
direction essentially unusable, or a pseudo-time direction problem, where a
Newton-like frozen-policy direction has a meaningful positive domain-safe step
and materially reduces the re-selected HJB residual? A second required
question is why the accepted final-validation residual (~490.756) is much
larger than the iteration-operator residual scale (~10.43): decompose the
difference by F0 versus boundary rows and by iteration versus final-validation
operator semantics. This is a local diagnostic only; it does NOT authorize a
multi-step Newton / policy-iteration / semismooth solver.

### 8.7.2 Frozen state reconstruction

Use exactly the accepted Issue #63 frozen central configuration and controller.
Deterministically reconstruct the accepted Issue #63 trajectory and STOP at
the state immediately after accepted FTB step 8, before any new HJB iterate is
accepted. Reproduce at minimum: 8 accepted root-controlled steps; final step
statistic ≈ `3.6614352438846254e-08`; final min boundary
`p_b ≈ 4.8089461301970005e-09`; final wall state F3 (13,13), z=1; final
accepted Bellman validation residual ≈ `490.7560425919994`; deterministic
repeat / accepted trace consistency. Preserve the pre-step-8 policy records
required to reproduce the accepted Issue #63 final-validation semantics
exactly.

### 8.7.3 Residual/operator decomposition at the frozen stagnation state

At `V_*`: build `Q_iter,u_iter` exactly once with accepted `final=False`
semantics; `R_iter = rho*V_* - [u_iter + Q_iter V_*]`. Build `Q_final,u_final`
using exactly the accepted Issue #63 final-validation semantics and preserved
pre-step-8 F0 policy records; `R_final = rho*V_* - [u_final + Q_final V_*]`
(must reproduce ≈ 490.756). Record both `||R||_inf` and argmax state/family/z,
max absolute residual separately over F0 rows and non-F0 boundary rows,
`||R_final - R_iter||_inf` and argmax, and rowwise/operator differences
sufficient to identify whether the large gap is dominated by F0 final
semantics, boundary reselection, or both. Never reinterpret one residual as
the other; no large matrices persisted.

### 8.7.4 Frozen-policy Newton direction and exact boundary-safe geometry

Use only the frozen iteration operator `(Q_iter,u_iter)` at `V_*`:
`J_iter = rho I - Q_iter`, solve `J_iter d_N = -R_iter` (exact Newton step
for the frozen linear policy/operator, not a nonlinear Newton theorem).
Verify numerically `R_iter(V_* + alpha*d_N; frozen) = (1-alpha) R_iter(V_*)`
at the authorized trial points. Any non-finite solve/evidence fails closed.
Boundary derivative semantics from accepted Issue #62: regular backward
finite-difference boundary states use the linear difference of `d_N`; `i==0`
V-independent `p_b` states have directional derivative exactly 0. For each
required boundary state with `dp_b(d_N) < 0`,
`alpha_cross_i = (p_b(V_*) - PB_MARGIN)/(-dp_b(d_N))`;
`alpha_cross = min` positive finite `alpha_cross_i`.

Frozen diagnostic constants:

```text
PB_MARGIN = 1e-12
EPS_ALPHA = 1e-6
HALF_ALPHA = 0.5
MATERIAL_REDUCTION_RATIO = 0.50
```

Deterministic trial fractions:
`alpha_near = min(1, (1-EPS_ALPHA)*alpha_cross)` if a finite positive crossing
exists, otherwise `1`; `alpha_half = 0.5*alpha_near`. No line search or tuning
is authorized. For both trial fractions: form `V_trial = V_* + alpha*d_N`;
directly verify all required boundary `p_b` finite and `> PB_MARGIN`; verify
the frozen residual relation `(1-alpha)R_iter`; perform exactly ONE nonlinear
policy re-selection at that trial using accepted `final=False` semantics
(`R_reselect`); compute the accepted final-validation-style residual at the
same trial using the trial re-selected records as the F0 policy input for
`final=True` semantics; record residual ratios versus baseline residuals and
policy/sector switching counts. Diagnostic trial states only — neither trial
may be accepted as a new HJB iterate.

### 8.7.5 Interpretation thresholds

A trial counts as a material nonlinear residual reduction only if BOTH
`||R_reselect||_inf / ||R_iter||_inf <= 0.50` and
`||R_final_trial||_inf / ||R_final||_inf <= 0.50`. This 0.50 threshold is
diagnostic and frozen ex ante for this Issue; it is not a convergence
criterion. Record whether the limiting boundary state for the Newton direction
is the same F3 (13,13), z=1 wall state or another state.

Execute exactly: ONE deterministic reconstruction; ONE residual/operator
decomposition at `V_*`; ONE frozen-policy Newton direction solve; ONE
boundary-crossing calculation; exactly TWO diagnostic trial fractions; ONE
deterministic repeat of the full diagnostic. No multi-step Newton iteration,
no adaptive alpha search, no alternative material-reduction threshold.

### 8.7.6 Builder allowlist — four new paths only

1. `src/deep_learning_hank/two_asset/stagnation_newton_geometry.py`
2. `tests/test_dlh_5vp_stagnation_newton_geometry.py`
3. `reports/dlh_5vp_stagnation_newton_geometry_2026_09_13/DLH_5VP_STAGNATION_NEWTON_GEOMETRY_REPORT.md`
4. `reports/dlh_5vp_stagnation_newton_geometry_2026_09_13/DLH_5VP_NEWTON_GEOMETRY_SUMMARY.csv`

No fifth tracked Builder path. Do not modify existing accepted source, tests,
reports, governance files, or `__init__.py` on the Builder branch.

### 8.7.7 Terminal set (exactly ONE reported)

- A `DLH_5VP_STAGNATION_NEWTON_GEOMETRY__BOUNDARY_SAFE_NEWTON_DIRECTION_MATERIALLY_REDUCES_RESELECTED_RESIDUALS__NEWTON_TRUST_REGION_DESIGN_GATE_READY`
- B `DLH_5VP_STAGNATION_NEWTON_GEOMETRY__POSITIVE_BOUNDARY_SAFE_NEWTON_STEP_BUT_NONLINEAR_RESIDUAL_REDUCTION_INSUFFICIENT__FURTHER_DIRECTION_DESIGN_REQUIRED`
- C `DLH_5VP_STAGNATION_NEWTON_GEOMETRY__NONFINITE_INCONSISTENT_OR_NO_POSITIVE_BOUNDARY_SAFE_NEWTON_GEOMETRY__BOUNDARY_HJB_ROUTE_REVIEW_REQUIRED`
- Blocked `BLOCKED_DLH_5VP_AUTHORITY_OR_DEPENDENCY_CONFLICT`

### 8.7.8 Forbidden

No mutation of the household oracle, selected-Q source, or Issue #61 / Issue
#62 / Issue #63 accepted implementations (all read-only); no economics/prices/
grid/domain/initialization/control-search/tolerances/`PB_MARGIN` change; no
Issue #63 controller change; no clip/floor/replace of `p_b`; no accepted new
HJB iterate; no multi-step Newton/policy-iteration/semismooth/trust-region
solver; no adaptive line search; no price or Wmax/resolution sweeps; no KFE/
stationary KFE; no `solve_household_steady_state`; no SCC/global-Q/GE/
multi-region/neural/nominal/calibration/policy/welfare/Results; no PR; no
merge; no Issue close; no successor; no self-accept.

---

## 8.8 Issue #65 / DLH-5V-Q — F0 final-validation operator consistency audit — TERMINAL B ACCEPTED / CLOSED

Title:

`DLH-5V-Q: Audit F0 final-validation operator semantics at the accepted Issue #63 stagnation state`

Task type:

`SCIENTIFIC_NUMERICAL_DIAGNOSTIC__F0_FINAL_VALIDATION_OPERATOR_CONSISTENCY_AUDIT`

Owner / Reviewer route decision:

`APPROVE_F0_FINAL_VALIDATION_OPERATOR_CONSISTENCY_AUDIT_AFTER_5VP_TERMINAL_B`

Authority marker:

`DLH_5VQ_F0_FINAL_VALIDATION_SEMANTICS_AUDIT_AUTHORIZED`

Initial authoritative activation comment:

`5653199929`

Dedicated Builder branch:

`dsh/issue-65-dlh-5vq-f0-final-validation-audit-2026-09-13`

Builder execution is **complete**: the Issue #65 audit was executed on its
dedicated branch after the activation comments (initial `5653199929` and the
final authoritative activation-refresh `5653443917` confirming the post-sync
live `main`), and the candidate is **ACCEPTED / CLOSED** as recorded below.

Issue #65 is **ACCEPTED / CLOSED** at Terminal B. Accepted candidate /
integration: `44cb7bda1a040cacfc94fa45cda689755daa5a4e`; reviewer acceptance
`5656806015`; acceptance integration `5656807180`. Accepted verdict:
`DLH_5VQ_ACCEPTED__TERMINAL_B_CONFIRMED__FINAL_TRUE_F0_RATE_SEMANTICS_DOMINATE_ACCEPTED_VALIDATION_GAP__STALE_RECORD_EFFECT_NEGLIGIBLE__F0_FINAL_OPERATOR_PROVENANCE_REVIEW_REQUIRED`;
accepted terminal:
`DLH_5VQ_F0_FINAL_VALIDATION_SEMANTICS__FINAL_RATE_SEMANTICS_DOMINATE_OR_TIE_ACCEPTED_VALIDATION_GAP__F0_FINAL_OPERATOR_REVIEW_REQUIRED`.
Accepted facts / interpretation (local attribution at the fixed `V_*` only):
`||R_iter||_inf = 10.435094313164921`, `||R_final_stale||_inf =
490.7560425919994`, `||R_final_current||_inf = 490.7560414005864`; `D_total =
D_stale + D_rate` with additive error `0.0` (`||D_total||_inf =
488.0988429898615`, `||D_stale||_inf = 1.8406872158038823e-05`,
`||D_rate||_inf = 488.0988417984485`) and non-F0 boundary contribution exactly
0 for all three differences; 596 F0 rows with changed sector/transfer label =
0 but non-identical continuous controls (max |Δ c/l/t/mu_a/mu_b/u| =
1.26e-8 / 3.53e-9 / 2.06e-7 / 2.06e-7 / 4.03e-7 / 1.09e-8); rowwise max
|`Q_final_stale` - `Q_final_current`| ≈ 1.48e-6; rowwise max |`Q_final_current`
- `Q_iter`| ≈ 24.60. Accepted interpretation: stale F0 records contribute
negligibly to the ~490.756 gap; a record refresh cannot eliminate the gap; the
accepted `final=True` F0 rate/discretization semantics dominate locally; no
counterfactual is declared the correct convergence criterion; does NOT prove
HJB fixed-point nonexistence; the provenance/equivalence of the `final=True`
F0 rate construction against the MATLAB-faithful iteration / discrete HJB
operator is audited next by Issue #66. Stationary KFE remains **NOT
AUTHORIZED**.

### 8.8.1 Scientific question

The accepted Issue #64 decomposition established that the ~490.756
final-validation residual gap is entirely an F0 phenomenon. Before any further
nonlinear-direction design, determine which F0 semantic change is responsible:
(1) **stale-record effect** — `final=True` uses F0 policy records preserved
from the pre-step-8 accepted iterate rather than policies re-selected at the
stagnation state `V_*`; (2) **final-rate/discretization effect** — even using
current `V_*`-selected F0 controls, the accepted `final=True` F0 upwind-rate
construction defines a materially different residual/operator from
`final=False` iteration semantics; (3) both. This is a scientific consistency
audit of the accepted validation operator; it does NOT authorize changing the
accepted source or convergence criterion.

### 8.8.2 Frozen stagnation state

Deterministically reconstruct the exact accepted Issue #63 stagnation state
`V_*` using the accepted Issue #64 reconstruction path and STOP before any new
HJB iterate is accepted. Reproduce: 8 accepted FTB steps; final statistic ≈
`3.6614352438846254e-08`; min boundary `p_b ≈ 4.8089461301970005e-09`; wall
state F3 (13,13), z=1; accepted stale-record final residual ≈
`490.7560425919994`. Preserve `records_pre_step8` (accepted pre-step-8 records
used by Issue #63 final validation) and `records_current` (the `final=False`
policies re-selected exactly once at `V_*`).

### 8.8.3 Exact three residual/operator objects at the same `V_*`

- A. iteration operator: build once with `final=False` at `V_*` →
  `Q_iter, u_iter, records_current`; `R_iter = rho V_* - [u_iter + Q_iter
  V_*]` (reproduce `||R_iter||_inf ≈ 10.435094313164921`);
- B. accepted stale-record final operator: `final=True` with
  `f0_policies = records_pre_step8` → `Q_final_stale, u_final_stale`;
  `R_final_stale = rho V_* - [u_final_stale + Q_final_stale V_*]`
  (reproduce `||R_final_stale||_inf = 490.7560425919994`);
- C. diagnostic current-record final operator: `final=True` with
  `f0_policies = records_current` → `Q_final_current, u_final_current`;
  `R_final_current = rho V_* - [u_final_current + Q_final_current V_*]`
  (diagnostic counterfactual operator at the same state, NOT an accepted
  replacement validation rule).

### 8.8.4 Exact required decomposition

`D_total = R_final_stale - R_iter`; `D_stale = R_final_stale -
R_final_current`; `D_rate = R_final_current - R_iter`; verify numerically
`D_total = D_stale + D_rate` within declared tolerance. For each residual /
difference record total / F0-only / non-F0 boundary-only infinity norms with
argmax state/family/z, conservative-Q row-sum diagnostic, optimizer
expansions / artificial bindings. Persist no large matrices.

### 8.8.5 F0 policy/control provenance audit

On F0 rows only, compare `records_pre_step8` vs `records_current`: count of
rows with changed sector/transfer label and max |Δ consumption|, |Δ labor|, |Δ
transfer|, |Δ mu_a|, |Δ mu_b|, |Δ utility|. Do NOT treat "same sector label" as
"same continuous control". Also compare `Q_final_stale - Q_final_current` and
`Q_final_current - Q_iter` rowwise max absolute operator differences and
`u_final_stale - u_final_current` / `u_final_current - u_iter` max absolute
differences.

### 8.8.6 Deterministic attribution rule (frozen ex ante)

`STALE_RECORD_DOMINANT` iff `||D_stale||_inf > ||D_rate||_inf`;
`FINAL_RATE_SEMANTICS_DOMINANT_OR_TIED` iff `||D_rate||_inf >=
||D_stale||_inf`; separately record whether `||R_final_current||_inf <
||R_final_stale||_inf`. Local attribution only — dominance does NOT imply
either diagnostic counterfactual is already the correct convergence criterion.

### 8.8.7 Exact execution design and terminals

Execute exactly: ONE deterministic reconstruction; ONE iteration-operator
build; ONE stale-record `final=True` build; ONE current-record `final=True`
build; ONE compact F0 policy/control provenance audit; ONE deterministic
repeat. No trial value states; no Newton step; no continuation; no source
modification. Exactly ONE terminal:

- A `DLH_5VQ_F0_FINAL_VALIDATION_SEMANTICS__STALE_F0_RECORDS_DOMINATE_ACCEPTED_VALIDATION_GAP__FINAL_VALIDATION_RECORD_REFRESH_REVIEW_GATE_READY`
- B `DLH_5VQ_F0_FINAL_VALIDATION_SEMANTICS__FINAL_RATE_SEMANTICS_DOMINATE_OR_TIE_ACCEPTED_VALIDATION_GAP__F0_FINAL_OPERATOR_REVIEW_REQUIRED`
- C `DLH_5VQ_F0_FINAL_VALIDATION_SEMANTICS__NONFINITE_OR_INCONSISTENT_DECOMPOSITION__BOUNDARY_HJB_VALIDATION_ROUTE_REVIEW_REQUIRED`
- Blocked `BLOCKED_DLH_5VQ_AUTHORITY_OR_DEPENDENCY_CONFLICT`

### 8.8.8 Builder allowlist (four new paths only)

1. `src/deep_learning_hank/two_asset/f0_final_validation_semantics_audit.py`
2. `tests/test_dlh_5vq_f0_final_validation_semantics_audit.py`
3. `reports/dlh_5vq_f0_final_validation_semantics_2026_09_13/DLH_5VQ_F0_FINAL_VALIDATION_SEMANTICS_REPORT.md`
4. `reports/dlh_5vq_f0_final_validation_semantics_2026_09_13/DLH_5VQ_F0_FINAL_VALIDATION_SUMMARY.csv`

---

## 8.9 Issue #66 / DLH-5V-R — NEXT ACTIVE F0 final=True rate/provenance and operator-consistency audit

Title:

`DLH-5V-R: Audit F0 final=True rate construction against the accepted MATLAB-faithful iteration operator`

Task type:

`SCIENTIFIC_NUMERICAL_DIAGNOSTIC__F0_FINAL_RATE_DISCRETIZATION_PROVENANCE_AND_OPERATOR_CONSISTENCY`

Owner / Reviewer route decision:

`APPROVE_F0_FINAL_RATE_DISCRETIZATION_PROVENANCE_AND_OPERATOR_CONSISTENCY_AUDIT_AFTER_5VQ_TERMINAL_B`

Authority marker:

`DLH_5VR_F0_FINAL_RATE_PROVENANCE_AUDIT_AUTHORIZED`

Initial authoritative activation comment:

`5656814064`

Dedicated future Builder branch:

`dsh/issue-66-dlh-5vr-f0-final-rate-provenance-2026-09-14`

Builder execution is **NOT YET OPERATIVE**: it becomes operative only after all
three CURRENT governance files are synchronized to Issue #66 (this roadmap
included), this activation ID is recorded, and a final authoritative
activation-refresh comment confirms the post-sync live `main`.

### 8.9.1 Scientific question

Issue #65 established that the large accepted final-validation gap is caused
by the F0 `final=True` operator semantics rather than stale F0 records.
Before changing any accepted source or convergence rule, determine the
provenance and discrete-HJB consistency of that `final=True` construction at
the same frozen `V_*` and the same current selected F0 controls: (A) ITER /
MATLAB-faithful iteration semantics — the accepted F0 `local_interior_row`
path with stored iteration rates (`iteration_b_backward_rate`,
`iteration_b_forward_rate`, `a_backward_rate`, `a_forward_rate`) and
source-faithful truncation / represented-destination convention; (B)
FINAL-RAW semantics — the accepted `final=True` F0 row construction from raw
drifts with direct `max(±mu)/step` upwind rates; (C) accepted oracle /
MATLAB-faithful source provenance, source-backed only. Read-only
diagnostic/provenance work; does NOT authorize replacing `final=True`,
changing the convergence criterion, or modifying the selected-Q source.

### 8.9.2 Frozen state and controls

Deterministically reconstruct the exact accepted Issue #63 stagnation state
`V_*` using accepted Issue #65/#64 helpers and STOP before any new HJB
iterate. Reproduce final statistic ≈ `3.6614352438846254e-08`; min boundary
`p_b ≈ 4.8089461301970005e-09`; wall F3 (13,13), z=1. At `V_*`, build current
`final=False` policies exactly once and use those SAME selected F0 controls
for all row/rate comparisons (no stale-record comparison needed except as
accepted baseline fact from Issue #65). Reproduce `||R_iter||_inf =
10.435094313164921`, `||R_final_current||_inf = 490.7560414005864`, and F0
rowwise max `|Q_final_current - Q_iter| ≈ 24.6019717663`.

### 8.9.3 Exact F0 row-rate decomposition

For every F0 state row, using the same current selected policy/control
record, extract and persist compact rowwise diagnostics (no full sparse
matrices) for at least: liquid/b direction backward and forward; illiquid/a
direction backward and forward; diagonal; represented outgoing-rate sum; any
requested raw drift/rate whose destination is not represented because of a
grid/domain edge; utility/source term (must distinguish operator-rate
differences from utility differences). Define rate/operator difference classes
sufficient to attribute the max ~24.60 difference; record counts/maxima/argmax
state for each component/class.

### 8.9.4 MATLAB-faithful provenance audit

Read-only inspect the accepted oracle / helper path used by the ITER F0 row
and record explicit provenance for: how selected continuous controls are
converted into iteration b backward/forward rates; how a backward/forward
rates are obtained; whether source-faithful clipping/truncation or
finite-difference sign logic is embedded before the row is assembled; how the
diagonal is constructed; what happens when an outward/requested rate has no
represented destination. Separately document the `final=True` F0 path: raw
`mu_a`, `mu_b` source; direct `max(±mu)/step` conversion; represented
off-diagonal destinations; diagonal construction. Source-backed mapping, not
an inferred rewrite of accepted code.

### 8.9.5 Exact equivalence checks and classifications

Freeze ex ante on F0 rows with the same current controls: `ITER_EQ_MATLAB`
(ITER row/rates source-backed as the MATLAB-faithful discrete HJB
construction and reproduced within tolerance); `FINAL_EQ_MATLAB` (FINAL-RAW
row/rates source-backed as the MATLAB-faithful discrete HJB construction and
reproduced within tolerance); `BOTH_EQUIVALENT` (ITER and FINAL-RAW rowwise
operator-equivalent within tolerance); `MIXED_OR_UNRESOLVED` (mixed
provenance, neither established, or insufficient source evidence). Also
record `||R_iter||_inf`, `||R_final_current||_inf`, rowwise max
`|Q_final_current - Q_iter|` and its component decomposition, whether
utility/source terms are identical under same current controls, and whether
all non-F0 boundary rows remain identical (expected from Issue #65; any
discrepancy fails closed). Do NOT convert these classifications into a source
mutation or new convergence rule in this Issue.

### 8.9.6 Exact execution design and terminals

Execute exactly: ONE deterministic reconstruction; ONE current-policy
`final=False` build at `V_*`; ONE current-policy `final=True` build at `V_*`;
ONE all-F0 compact row/rate/component comparison; ONE read-only
MATLAB/oracle provenance mapping; ONE deterministic repeat. No new HJB
iterate; no Newton / continuation / line search; no parameter/grid/price
sweep; no source mutation. Exactly ONE terminal:

- A `DLH_5VR_F0_FINAL_RATE_PROVENANCE__ITERATION_OPERATOR_MATCHES_ACCEPTED_MATLAB_FAITHFUL_HJB__FINAL_RAW_RATE_OPERATOR_NON_EQUIVALENT__VALIDATION_OPERATOR_REDESIGN_REVIEW_GATE_READY`
- B `DLH_5VR_F0_FINAL_RATE_PROVENANCE__FINAL_RAW_RATE_OPERATOR_MATCHES_ACCEPTED_MATLAB_FAITHFUL_HJB__ITERATION_OPERATOR_NON_EQUIVALENT__ITERATION_OPERATOR_REVIEW_REQUIRED`
- C `DLH_5VR_F0_FINAL_RATE_PROVENANCE__MIXED_EQUIVALENT_OR_UNRESOLVED_DISCRETE_OPERATOR_PROVENANCE__OWNER_SCIENTIFIC_REVIEW_REQUIRED`
- Blocked `BLOCKED_DLH_5VR_AUTHORITY_OR_DEPENDENCY_CONFLICT`

Classification is local to the accepted finite-grid operator/provenance and
does not by itself authorize changing source code.

### 8.9.7 Builder allowlist (four new paths only)

1. `src/deep_learning_hank/two_asset/f0_final_rate_provenance_audit.py`
2. `tests/test_dlh_5vr_f0_final_rate_provenance.py`
3. `reports/dlh_5vr_f0_final_rate_provenance_2026_09_14/DLH_5VR_F0_FINAL_RATE_PROVENANCE_REPORT.md`
4. `reports/dlh_5vr_f0_final_rate_provenance_2026_09_14/DLH_5VR_F0_FINAL_RATE_PROVENANCE_SUMMARY.csv`

### 8.9.8 Forbidden

No source mutation (household oracle, selected-Q, Issues #61-#65 accepted
implementations, `final=True` semantics); no convergence-criterion change;
`R_iter` must NOT be declared the accepted final convergence residual; no
economics/prices/grid/domain/initialization/controls/tolerances/`PB_MARGIN`
change; no Newton / policy-iteration / semismooth / trust-region /
continuation; no line search; no new HJB iterate; no price/Wmax/resolution
sweep; no KFE / stationary KFE / `solve_household_steady_state`; no
SCC/global-Q / GE / multi-region / neural / nominal / calibration / policy /
welfare / Results; no successor; no PR / merge / Issue close / self-accept.

---

## 9. Current roadmap position

```text
MATLAB-faithful two-asset household economics                 ACCEPTED
finite W-domain + continuous tangent/KKT law                 ACCEPTED
same-process HJB <=> KFE principle                           ACCEPTED
restricted-Voronoi state partition                           ACCEPTED
regular W-frontier finite-process block                      ACCEPTED
endpoint exact finite-process closure                         OBSTRUCTION ACCEPTED — ISSUE #54
Route A strong raw graph target                               OBSTRUCTION ACCEPTED — ISSUE #55
state-constraint operator-consistency audit                   OUTCOME B ACCEPTED — ISSUE #56
boundary-HJB production-scheme design                         OUTCOME A ACCEPTED — ISSUE #57
boundary-HJB implementation + local HJB validation            TERMINAL B ACCEPTED — ISSUE #58
fixed-household external-price envelope                       TERMINAL B/H2 ACCEPTED — ISSUE #59
invariant-domain safeguarded HJB update                       TERMINAL C ACCEPTED/CLOSED — ISSUE #60
adaptive pseudo-time / resolvent diagnostic                   TERMINAL C ACCEPTED/CLOSED — ISSUE #61
local continuous resolvent / domain-margin geometry          OUTCOME A ACCEPTED/CLOSED — ISSUE #62
continuous fraction-to-boundary pseudo-transient continuation  TERMINAL B ACCEPTED/CLOSED — ISSUE #63
frozen-policy Newton geometry diagnostic (stagnation residual decomposition)  TERMINAL B ACCEPTED/CLOSED — ISSUE #64
F0 final-validation operator consistency audit                      TERMINAL B ACCEPTED/CLOSED — ISSUE #65
F0 final=True rate/provenance and operator-consistency audit          NEXT ACTIVE — ISSUE #66 (BUILDER NOT YET OPERATIVE)
next scientific route (multi-step Newton / trust-region successor)  SCIENTIFIC DESIGN REQUIRED — OWNER/CHATGPT
same-process Q global validation + SCC diagnostics            BLOCKED UNTIL HJB ROUTE RESOLVED
nested Wmax / resolution robustness                          BLOCKED UNTIL HJB ROUTE RESOLVED
conservative stationary-generator validation                 BLOCKED UNTIL HJB ROUTE RESOLVED
Issue #27 stationary KFE                                     NOT AUTHORIZED
stationary C,L,A,B                                           PENDING
two-region structural anchor rebuild                         PENDING
3–5 province integration                                     PENDING
learned regional W^L                                         PENDING
```

---

## 10. Same-process safeguards — frozen

```text
Q backward
Q^T forward
Q_ij>=0 for i!=j
Q_ii=-sum of ACTUAL represented outgoing rates
Q1=0 by construction
same selected candidate/rates for HJB and future KFE
p=M g
p_dot=Q^T p
```

No route may use pinning/normalization to repair leakage or create a KFE-only process.

Stationary KFE remains explicitly blocked.

---

## 11. Current governance position

**NEXT ACTIVE BUILDER ISSUE: #66 / DLH-5V-R** (initial activation comment
`5656814064` recorded). Route decision:
`APPROVE_F0_FINAL_RATE_DISCRETIZATION_PROVENANCE_AND_OPERATOR_CONSISTENCY_AUDIT_AFTER_5VQ_TERMINAL_B`;
authority marker:
`DLH_5VR_F0_FINAL_RATE_PROVENANCE_AUDIT_AUTHORIZED`; dedicated future
Builder branch
`dsh/issue-66-dlh-5vr-f0-final-rate-provenance-2026-09-14`. Builder
execution becomes operative only after all three CURRENT governance files are
synchronized to Issue #66 and a final authoritative activation-refresh comment
confirms the post-sync live `main`. Until then Builder execution remains
**NOT YET OPERATIVE**.

Issue #64 / DLH-5V-P is ACCEPTED / CLOSED at Terminal B (accepted candidate /
integration `5db144a65796ff6a7e0f59d2d2a75a0446c13b83`; reviewer acceptance
`5653190792`; acceptance integration `5653192646`; accepted verdict
`DLH_5VP_ACCEPTED__TERMINAL_B_CONFIRMED__F0_FINAL_SEMANTICS_DOMINATE_VALIDATION_GAP__FROZEN_POLICY_NEWTON_IS_BOUNDARY_SAFE_BUT_GEOMETRICALLY_CAPPED_AND_NONLINEAR_RESIDUAL_REDUCTION_INSUFFICIENT__FURTHER_DIRECTION_DESIGN_REQUIRED`)
and remains the controlling accepted evidence for the F0 final-validation
semantic gap audited by Issue #65: the accepted Issue #63 stagnation state was
reconstructed exactly (8 root-controlled FTB steps; final statistic ≈
3.66e-8; final min p_b ≈ 4.81e-9; wall state F3 (13,13), z=1; accepted
final-validation residual ≈ 490.756 reproduced); `||R_iter||_inf =
10.435094313164921`, `||R_final_stale||_inf = 490.7560425919994`,
`||R_final_stale - R_iter||_inf = 488.0988429898615` with the difference
entirely on F0 rows and non-F0 boundary-row difference exactly 0; the
frozen-policy Newton solve is well-defined (`||J_iter d_N + R_iter||_inf ≈
6.96e-11`) but the same F3 (13,13), z=1 wall caps the safe fraction at
`alpha_cross ≈ 1.87e-4`, and both authorized trials leave the nonlinear
residuals essentially unchanged (ratios ≈ 0.9998-0.9999 >> 0.50) → plain
frozen-policy Newton is not a viable local residual-reducing route under this
wall geometry; this does NOT prove HJB fixed-point nonexistence or failure of
future constrained/tangent directions; sector-switch count 0 must not be
overinterpreted as proof that continuous controls are unchanged. Stationary
KFE remains **NOT AUTHORIZED**.

Issue #65 / DLH-5V-Q is ACCEPTED / CLOSED at Terminal B (accepted candidate /
integration `44cb7bda1a040cacfc94fa45cda689755daa5a4e`; reviewer acceptance
`5656806015`; acceptance integration `5656807180`; accepted verdict
`DLH_5VQ_ACCEPTED__TERMINAL_B_CONFIRMED__FINAL_TRUE_F0_RATE_SEMANTICS_DOMINATE_ACCEPTED_VALIDATION_GAP__STALE_RECORD_EFFECT_NEGLIGIBLE__F0_FINAL_OPERATOR_PROVENANCE_REVIEW_REQUIRED`)
and remains the controlling accepted evidence for the F0 `final=True`
rate/discretization operator dominance audited by Issue #66: at the same
frozen stagnation state `V_*`, `||R_iter||_inf = 10.435094313164921`,
`||R_final_stale||_inf = 490.7560425919994`,
`||R_final_current||_inf = 490.7560414005864`; `D_total = D_stale + D_rate`
with additive error `0.0` (`||D_total||_inf = 488.0988429898615`,
`||D_stale||_inf = 1.8406872158038823e-05`,
`||D_rate||_inf = 488.0988417984485`); non-F0 boundary contribution exactly 0
for all three differences; 596 F0 rows with changed sector/transfer label = 0
but non-identical continuous controls (max |Δ c/l/t/mu_a/mu_b/u| =
1.26e-8 / 3.53e-9 / 2.06e-7 / 2.06e-7 / 4.03e-7 / 1.09e-8); rowwise max
|`Q_final_stale` - `Q_final_current`| ≈ 1.48e-6; rowwise max |`Q_final_current`
- `Q_iter`| ≈ 24.60. Accepted interpretation: stale F0 records contribute
negligibly to the ~490.756 gap; a record refresh cannot eliminate the gap; the
accepted `final=True` F0 rate/discretization semantics dominate locally; no
counterfactual is declared the correct convergence criterion; does NOT prove
HJB fixed-point nonexistence. Stationary KFE remains **NOT AUTHORIZED**.

Scientific boundary of Issue #66 (binding): deterministically reconstruct
the exact accepted Issue #63 stagnation state `V_*` using accepted Issue #65/
#64 helpers (deterministic reconstruction, STOP before any new HJB iterate is
accepted; reproduce final statistic ≈ `3.6614352438846254e-08`, min boundary
`p_b ≈ 4.8089461301970005e-09`, wall F3 (13,13), z=1) and build current
`final=False` policies exactly once at `V_*`, using those SAME selected F0
controls for all row/rate comparisons; reproduce `||R_iter||_inf =
10.435094313164921`, `||R_final_current||_inf = 490.7560414005864`, and F0
rowwise max `|Q_final_current - Q_iter| ≈ 24.6019717663`. For every F0 state
row extract and persist compact rowwise diagnostics (no full sparse matrices):
b backward / b forward / a backward / a forward rates, diagonal, represented
outgoing-rate sum, omitted / unavailable destination rate at a grid/domain
edge, and utility/source term (separating operator-rate differences from
utility differences); attribute the max ~24.60 difference into defined
rate/operator difference classes with counts/maxima/argmax state. Read-only
MATLAB-faithful provenance mapping (source-backed, no re-interpretation or
rewrite): how selected continuous controls become iteration b backward/forward
and a backward/forward rates; source-faithful clipping/truncation or
finite-difference sign logic; diagonal construction; handling of an
outward/requested rate with no represented destination; separately the
`final=True` F0 path (raw `mu_a`/`mu_b` source; direct `max(±mu)/step`
conversion; represented off-diagonal destinations; diagonal construction).
Frozen ex ante equivalence classifications on F0 rows with the same current
controls: `ITER_EQ_MATLAB`, `FINAL_EQ_MATLAB`, `BOTH_EQUIVALENT`,
`MIXED_OR_UNRESOLVED`; also record whether utility/source terms are identical
under same current controls and whether all non-F0 boundary rows remain
identical (any discrepancy fails closed); classifications must NOT be
converted into a source mutation or new convergence rule. Execute exactly: ONE
deterministic reconstruction, ONE current-policy `final=False` build at
`V_*`, ONE current-policy `final=True` build at `V_*`, ONE all-F0 compact
row/rate/component comparison, ONE read-only MATLAB/oracle provenance
mapping, ONE deterministic repeat; no new HJB iterate; no Newton /
continuation / line search; no parameter/grid/price sweep; no source mutation;
non-finite / provenance ambiguity fails closed. Terminal set per Issue #66
body (A/B/C + Blocked, exactly one). Seven read-only blobs (oracle
`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`; selected-Q
`7ea342ccbe15d852b90743b14bb4b02977c2d78b`; Issue #61
`043e146ef499e985a49d256c4cec2f397f93e4e1`; Issue #62
`cb6533475d0ba115e6f52bd73e61aeb85c9b6ea7`; Issue #63
`746799509c517746ba6a321e5526c57a8f4698e4`; Issue #64
`3ca2371c7da1939d1fed55df5728baefb27d8aa7`; Issue #65
`bb4045378bf19607f68d7d4a7628b3431afcd676`). Stationary KFE remains **NOT
AUTHORIZED**; no successor; no PR / merge / Issue close / self-accept. Issue
#65 / DLH-5V-Q, Issue #64 / DLH-5V-P, Issue #63 / DLH-5V-O, Issue #62 /
DLH-5V-N, Issue #61 / DLH-5V-M and Issue #60 / DLH-5V-L remain ACCEPTED /
CLOSED; the six tested stabilization-route gates are closed.

Current governance pointers:

- `tasks/TASK_INDEX_CURRENT.md`
- `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
- Issue #66 body/comments (next active; initial activation `5656814064`).
- Issue #65 body/comments (accepted/closed).

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.
