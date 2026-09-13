# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.47  
**Date:** 2026-09-13  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** NO_ACTIVE_BUILDER_ISSUE — DLH-5V-O / ISSUE #63 TERMINAL B ACCEPTED / CLOSED (continuous FTB continuation stagnates at boundary; next = scientific design required)

---

## 0. Long-run objective

Build a hybrid structural–learned regional HANK platform in which household HJB/KFE, aggregation, firm/accounting and later nominal-HANK equations remain explicit structural economics, while hard-to-specify cross-regional mappings become learned modules only after household and equilibrium foundations pass scientific and numerical validation.

The first learned object remains regional labor/spatial mapping `W^L`. Neural training remains downstream.

---

## 1. Accepted household / finite-domain foundation

Accepted household oracle:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb337f1b02b3fe33c51e`

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
next scientific route (fixed-point-preserving successor)        SCIENTIFIC DESIGN REQUIRED — OWNER/CHATGPT
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

**NO ACTIVE BUILDER ISSUE.** Issue #63 / DLH-5V-O is ACCEPTED / CLOSED at
Terminal B (accepted candidate / integration
`a552dc6ebb2c82ad19fe26cd747d362ceecdfdcc`; reviewer acceptance `5652576918`;
acceptance integration `5652579072`).

Accepted verdict:

`DLH_5VO_ACCEPTED__TERMINAL_B_CONFIRMED__CONTINUOUS_FTB_PRESERVES_EFFECTIVE_DOMAIN_BUT_STAGNATES_AT_BOUNDARY_WITH_MATERIAL_BELLMAN_RESIDUAL__ROUTE_RECONSIDERATION_REQUIRED`

Accepted terminal:

`DLH_5VO_CONTINUOUS_FTB_RESOLVENT__EFFECTIVE_DOMAIN_PRESERVED_BUT_VALIDATED_HJB_CONVERGENCE_NOT_REACHED`

The continuous FTB controller preserved the effective domain on the frozen
central selected-Q case (8 accepted root-controlled steps; cap-direct = 0;
limiting wall state F3 (13,13), z=1; selected delta and margin shrinking ≈
geometrically; final min p_b ≈ 4.81e-9 > 1e-12), but the accepted-step trigger
at iteration 8 (`max|V_{n+1}-V_n| ≈ 3.66e-8 < 1e-7`) is a tiny step caused by
boundary-following geometry: the final Bellman residual ≈ 490.756 >> 1e-3 with
the raw fixed-point direction norm ≈ 10.43-10.88 not approaching 0 →
**FTB_STAGNATION**, NOT validated HJB convergence. Q conservative, 0/0
bindings/expansions, deterministic repeat identical. The Issue #62 positive
local safe radius is real but does NOT suffice for validated convergence under
this frozen FTB controller. Trajectory-bounded evidence only: does NOT prove
all FTB controllers globally fail, does NOT prove the absence of another
fixed-point-preserving direction/operator, does NOT prove the HJB fixed point
does not exist.

Metadata note (wording): the candidate result field `converged=True` means
ONLY that the accepted-step statistic trigger was reached; scientific
validated convergence = FALSE. Recommended wording:
`step-size convergence trigger reached; validated HJB convergence failed (FTB_STAGNATION)`.

Next scientific route: **OWNER / ChatGPT SCIENTIFIC DESIGN REQUIRED**. The next
route must NOT be merely continuing to shrink delta or tuning `TAU_FTB`.
Residual-aware / policy-Newton / semismooth / boundary-tangent direction
successors are **NOT YET AUTHORIZED** — they await a ChatGPT scientific design
and a new authorized Issue (no successor Issue, no Builder scientific branch,
no accepted new HJB iterate, no continuous continuation variant, no extension
of any delta ladder as an experiment, no new price / grid / margin
experiments). Stationary KFE remains **NOT AUTHORIZED**. Issue #62 / DLH-5V-N,
Issue #61 / DLH-5V-M and Issue #60 / DLH-5V-L remain ACCEPTED / CLOSED; the
four tested stabilization-route gates are closed.

Current governance pointers:

- `tasks/TASK_INDEX_CURRENT.md`
- `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
- Issue #63 body/comments (accepted/closed).

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.
