# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.55  
**Date:** 2026-09-17  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** OWNER ROUTE A SELECTED — MATLAB-FAITHFUL SINGLE-Q OPERATOR CONTRACT AUTHORITATIVE AND CONSOLIDATED — ISSUE #73 / DLH-5V-Y NEXT ACTIVE (BUILDER NOT YET OPERATIVE) — ISSUE #72 / DLH-5V-X ACCEPTED / CLOSED AT TERMINAL B

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

## 8.9 Issue #66 / DLH-5V-R — F0 final=True rate/provenance and operator-consistency audit — TERMINAL A ACCEPTED / CLOSED (SUPERSEDED BY ISSUE #67)

Title:

`DLH-5V-R: Audit F0 final=True rate construction against the accepted MATLAB-faithful iteration operator`

Task type:

`SCIENTIFIC_NUMERICAL_DIAGNOSTIC__F0_FINAL_RATE_DISCRETIZATION_PROVENANCE_AND_OPERATOR_CONSISTENCY`

Owner / Reviewer route decision:

`APPROVE_F0_FINAL_RATE_DISCRETIZATION_PROVENANCE_AND_OPERATOR_CONSISTENCY_AUDIT_AFTER_5VQ_TERMINAL_B`

Authority marker:

`DLH_5VR_F0_FINAL_RATE_PROVENANCE_AUDIT_AUTHORIZED`

Initial authoritative activation comment:

`5656814064` (final authoritative activation-refresh `5657247407`)

Dedicated Builder branch (integrated into `main`):

`dsh/issue-66-dlh-5vr-f0-final-rate-provenance-2026-09-14`

Builder execution is **complete**: the Issue #66 audit was executed on its
dedicated branch after the activation comments (initial `5656814064` and the
final authoritative activation-refresh `5657247407` confirming the post-sync
live `main`), and the candidate is **ACCEPTED / CLOSED** as recorded below.

Issue #66 is **ACCEPTED / CLOSED** at Terminal A. Accepted candidate /
integration: `a31f17e6d965ddfe8214cd1b83d4074833310625`; reviewer acceptance
`5666168154`; acceptance integration `5666172248`. Accepted verdict:
`DLH_5VR_ACCEPTED__TERMINAL_A_CONFIRMED__ITERATION_OPERATOR_IS_MATLAB_FAITHFUL__FINAL_TRUE_F0_ROW_ASSEMBLY_DROPS_Z_BLOCK_OFFSET_FOR_Z1__VALIDATION_OPERATOR_SCIENTIFIC_REPAIR_OWNER_GATE_REQUIRED`;
accepted terminal:
`DLH_5VR_F0_FINAL_RATE_PROVENANCE__ITERATION_OPERATOR_MATCHES_ACCEPTED_MATLAB_FAITHFUL_HJB__FINAL_RAW_RATE_OPERATOR_NON_EQUIVALENT__VALIDATION_OPERATOR_REDESIGN_REVIEW_GATE_READY`.
Accepted facts / interpretation (local attribution at the fixed `V_*` only):
`ITER_EQ_MATLAB = true`, `FINAL_EQ_MATLAB = false`, `BOTH_EQUIVALENT = false`,
`MIXED_OR_UNRESOLVED = false`; F0 directional rate formulas coincide within
machine tolerance; utility/source terms identical; non-F0 boundary rows
identical; **destination assembly is the material discrepancy** — 298 z=1 F0
rows affected; rowwise max operator gap = `24.601971766296664`; the accepted
`final=True` F0 off-diagonal path uses bare `dn` while the accepted iteration
and boundary paths use `nz*n + dn`, therefore z=1 `final=True` F0 destinations
are incorrectly placed in the z=0 block; no conclusion yet that the
convergence criterion itself should change; correction of accepted `final=True`
source semantics requires explicit Owner authorization; `R_iter` is NOT
declared an accepted final convergence residual; does NOT prove HJB
fixed-point nonexistence; the next route is `OWNER SCIENTIFIC DECISION
REQUIRED — MINIMAL FINAL-VALIDATION OPERATOR REPAIR` — the Owner granted that
decision on 2026-09-15 through Issue #67 / DLH-5V-S. Stationary KFE remains
**NOT AUTHORIZED**.

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
sweep; no source mutation. Executed exactly as designed (deterministic repeat
bit-identical; full-repository suite 512 passed). Exactly ONE terminal was
reported:

- A `DLH_5VR_F0_FINAL_RATE_PROVENANCE__ITERATION_OPERATOR_MATCHES_ACCEPTED_MATLAB_FAITHFUL_HJB__FINAL_RAW_RATE_OPERATOR_NON_EQUIVALENT__VALIDATION_OPERATOR_REDESIGN_REVIEW_GATE_READY` — **ACCEPTED**
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

## 8.10 Issue #67 / DLH-5V-S — minimal `final=True` F0 z-block destination repair and corrected validation re-check — TERMINAL A ACCEPTED / CLOSED (SUPERSEDED BY ISSUE #68)

Title:

`DLH-5V-S: Minimal repair of final=True F0 z-block destination assembly and corrected validation re-check`

Task type:

`SCIENTIFIC_CHANGE__MINIMAL_FINAL_VALIDATION_OPERATOR_REPAIR_AND_REVALIDATION`

Owner / Reviewer route decision:

`APPROVE_MINIMAL_FINAL_VALIDATION_ZBLOCK_DESTINATION_REPAIR_AFTER_5VR_TERMINAL_A`

Authority marker:

`DLH_5VS_MINIMAL_FINAL_VALIDATION_ZBLOCK_REPAIR_AUTHORIZED`

Owner explicit authorization (2026-09-15, recorded in Issue #67):

> `同意 Issue #67 按最小 validation-operator repair 路线执行。`

Initial authoritative activation comment:

`5672573849` (final authoritative activation-refresh `5672691735`)

Builder execution is **complete and ACCEPTED / CLOSED**: the scientific
candidate `281cfe01b2925364a92308ca172a84a724c6ea58` was followed by the
Reviewer-authorized bounded post-repair test-contract remediation commit
`a5753bb9fa329a3d85a5652b03d101fa0be6cd32`, which is the accepted final
candidate / integration. Reviewer acceptance `5674741491`; acceptance
integration `5674743972` (fast-forward, not a merge commit). Accepted verdict
`DLH_5VS_ACCEPTED__TERMINAL_A_CONFIRMED__MINIMAL_ZBLOCK_DESTINATION_REPAIR_EXACT__CORRECTED_FINAL_OPERATOR_MATCHES_MATLAB_FAITHFUL_LAYOUT__FULL_SUITE_GREEN__HJB_RESIDUAL_REASSESSMENT_REQUIRED`;
accepted terminal
`DLH_5VS_FINAL_VALIDATION_ZBLOCK_REPAIR__CORRECTED_FINAL_OPERATOR_MATCHES_MATLAB_FAITHFUL_LAYOUT__SPURIOUS_CROSS_Z_VALIDATION_GAP_REMOVED__HJB_RESIDUAL_REASSESSMENT_GATE_READY`.

Accepted facts: selected-Q repaired blob
`556ccc214f03a1a22306cc4f5c7e9f7691bbf897`; the exact scientific source repair
remains only `cols.append(dn)` → `cols.append(nz * self.n + dn)`; corrected
final residual `10.435094313164921` matching accepted `R_iter`; corrected-final
vs ITER rowwise operator gap `1.4210854715202004e-14` versus historical
pre-repair `24.601971766296664` and pre-repair current final residual
`490.7560414005864` (~`480.32` excess attributed to the cross-z
destination-index defect); z=0 unchanged; non-F0 boundary `Q`/`u` diff `0`;
utility/source diff `0`; conservativity preserved; expansions/bindings `0`;
historical Issue #64/#65/#66 test constants preserved and post-repair runtime
contracts migrated; full suite **534 passed / 0 failed / 6 pre-existing
warnings**. **HJB convergence remains FALSE**: the corrected residual is
~`10435`× the unchanged Bellman tolerance `1e-3`, and `R_iter` is NOT declared
the accepted final convergence residual.

Dedicated Builder branch (integrated into `main`):

`dsh/issue-67-dlh-5vs-final-validation-zblock-repair-2026-09-15`

Controlling accepted authority: Issue #66 / DLH-5V-R ACCEPTED / CLOSED at
Terminal A (accepted candidate / integration
`a31f17e6d965ddfe8214cd1b83d4074833310625`; reviewer acceptance `5666168154`;
acceptance integration `5666172248`; accepted verdict
`DLH_5VR_ACCEPTED__TERMINAL_A_CONFIRMED__ITERATION_OPERATOR_IS_MATLAB_FAITHFUL__FINAL_TRUE_F0_ROW_ASSEMBLY_DROPS_Z_BLOCK_OFFSET_FOR_Z1__VALIDATION_OPERATOR_SCIENTIFIC_REPAIR_OWNER_GATE_REQUIRED`).
Issue #66 established that the accepted `final=True` F0 off-diagonal
destination assembly drops the z-block offset for z=1 rows while the
directional rate formulas themselves are MATLAB-faithful.

### 8.10.1 Authorized scientific change — exactly one location

Within the `final=True` F0 off-diagonal destination assembly of

`src/deep_learning_hank/two_asset/boundary_hjb_selected_q.py`

replace the bare destination-column placement

`cols.append(dn)`

with same-z-block placement

`cols.append(nz * self.n + dn)`

consistent with the accepted iteration path / boundary path / MATLAB-faithful
state layout. Scientific intent: repair **only** the z-block destination index,
so that z=1 F0 off-diagonal destinations remain inside the z=1 block.

Do NOT change: raw drift calculation; `max(±mu)/step` final rate formulas;
continuous controls; policy selection; diagonal construction; switch-matrix
assembly; economics, prices, grid/domain, initialization, tolerances,
`PB_MARGIN`; convergence thresholds; accepted iteration operator semantics.

### 8.10.2 Post-repair validation boundary

At the exact accepted Issue #63 stagnation state `V_*`, using current selected
F0 controls: build the iteration operator/residual under accepted `final=False`
semantics; build the corrected `final=True` operator/residual with the repaired
same-z-block F0 destination assembly; compare the corrected `final=True`
operator to the accepted MATLAB-faithful / iteration operator at the same
controls; verify non-F0 boundary rows remain unchanged; verify utility/source
terms remain identical where expected; record the corrected Bellman residual
and its argmax; and compare the corrected residual against the accepted
pre-repair current-record final residual `490.7560414005864` and the accepted
`||R_iter||_inf = 10.435094313164921`.

A materially lower corrected residual does **NOT** by itself establish HJB
convergence: the existing Bellman tolerance remains the unchanged acceptance
threshold unless a later Owner-authorized task changes it.

### 8.10.3 Exact repair-equivalence checks

Require at the same current controls and `V_*`: F0 corrected-final off-diagonal
destinations stay within the same z block; corrected-final F0 directional rates
reproduce the accepted rate formulas; corrected-final F0 row assembly
reproduces the source-backed MATLAB-faithful post-convergence row layout within
numerical tolerance; the corrected-final versus ITER rowwise operator
difference is decomposed and reported; non-F0 boundary operator/u differences
are 0 or fail closed; `Q 1` conservativity remains within accepted tolerance;
and no new artificial binding / optimizer expansion is introduced by the
repair.

### 8.10.4 Exact execution design and terminals

Execute exactly: ONE minimal source repair at the authorized location; ONE
focused static/source test of the destination index; ONE deterministic
reconstruction of accepted `V_*`; ONE `final=False` current-policy build; ONE
corrected `final=True` current-policy build using the same controls; ONE
corrected-equivalence/residual diagnostic; ONE deterministic repeat; focused
tests plus the full repository suite. No new HJB iterate is accepted in this
task — repair + revalidation only.

Exactly ONE terminal must be reported:

- A `DLH_5VS_FINAL_VALIDATION_ZBLOCK_REPAIR__CORRECTED_FINAL_OPERATOR_MATCHES_MATLAB_FAITHFUL_LAYOUT__SPURIOUS_CROSS_Z_VALIDATION_GAP_REMOVED__HJB_RESIDUAL_REASSESSMENT_GATE_READY` — **ACCEPTED**
- B `DLH_5VS_FINAL_VALIDATION_ZBLOCK_REPAIR__ZBLOCK_ASSEMBLY_REPAIRED_BUT_MATERIAL_HJB_VALIDATION_DISCREPANCY_REMAINS__FURTHER_VALIDATION_REVIEW_REQUIRED`
- C `DLH_5VS_FINAL_VALIDATION_ZBLOCK_REPAIR__NONFINITE_INCONSISTENT_OR_REGRESSION_FAILURE__SCIENTIFIC_REPAIR_REVIEW_REQUIRED`
- Blocked `BLOCKED_DLH_5VS_AUTHORITY_OR_DEPENDENCY_CONFLICT`

Executed exactly as designed (deterministic repeat identical; focused Issue #67
module 20 passed). The three accepted Issue #64/#65/#66 test modules were
subsequently migrated under Reviewer authorization so that historical
pre-repair constants remain preserved as evidence while runtime contracts assert
the repaired semantics; the full repository suite is **534 passed / 0 failed /
6 pre-existing warnings**.

### 8.10.5 Builder allowlist (four paths only)

1. `src/deep_learning_hank/two_asset/boundary_hjb_selected_q.py`
2. `tests/test_dlh_5vs_final_validation_zblock_repair.py`
3. `reports/dlh_5vs_final_validation_zblock_repair_2026_09_15/DLH_5VS_FINAL_VALIDATION_ZBLOCK_REPAIR_REPORT.md`
4. `reports/dlh_5vs_final_validation_zblock_repair_2026_09_15/DLH_5VS_FINAL_VALIDATION_ZBLOCK_REPAIR_SUMMARY.csv`

No fifth tracked Builder path. All other accepted sources/tests/reports/
governance remain read-only.

### 8.10.6 Forbidden

No change to any convergence criterion; `R_iter` must NOT be declared the
accepted final convergence residual by fiat; no final-rate-formula change
beyond the authorized destination-index repair; no policy-selection / control
change; no economics/prices/grid/domain/initialization/tolerances/`PB_MARGIN`
change; no new HJB iterate; no Newton / policy iteration / semismooth /
trust-region / continuation / line search; no price/Wmax/resolution sweep; no
KFE / stationary KFE / `solve_household_steady_state`; no SCC/global-Q / GE /
multi-region / neural / nominal / calibration / policy / welfare / Results; no
PR; no merge; no Issue close; no successor; no self-accept.

Stationary KFE remains **NOT AUTHORIZED**.

---

## 8.11 Issue #68 / DLH-5V-T — single-wall tangent-projected frozen-policy Newton geometry after accepted final-validation repair — TERMINAL C ACCEPTED / CLOSED (SUPERSEDED BY ISSUE #69)

Title:

`DLH-5V-T: Diagnose single-wall tangent-projected Newton geometry after final-validation repair`

Task type:

`SCIENTIFIC_NUMERICAL_DIAGNOSTIC__BOUNDARY_TANGENT_PROJECTED_NEWTON_GEOMETRY_AFTER_VALIDATION_REPAIR`

Owner / Reviewer route decision:

`APPROVE_SINGLE_WALL_TANGENT_PROJECTED_NEWTON_GEOMETRY_AFTER_5VS_TERMINAL_A`

Authority marker:

`DLH_5VT_TANGENT_PROJECTED_NEWTON_GEOMETRY_AUTHORIZED`

Initial authoritative activation comment:

`5674754187` (final authoritative activation-refresh `5675003122`)

Builder execution is **complete and ACCEPTED / CLOSED** at Terminal C. Scientific
candidate `b194eb3886af7a5e3d5abe85dad114fdc6ed98eb` was followed by the
Reviewer-authorized gradient-semantics remediation commit
`15083e5c9f089406aa69326bc84dbe2db0e42be8`, which is the accepted final
candidate / integration. Reviewer acceptance `5676811925`; acceptance
integration `5676816068` (fast-forward, not a merge commit). Accepted verdict
`DLH_5VT_ACCEPTED__TERMINAL_C_CONFIRMED__FULL_CHAIN_RULE_TANGENT_GEOMETRY_EXPANDS_SAFE_FRACTION_MATERIALLY__TRIAL_LEVEL_FINAL_VS_ITERATION_RATE_PATH_DIVERGENCE_INVALIDATES_CLEAN_RESIDUAL_CONTRACT__RATE_PATH_PROVENANCE_REVIEW_REQUIRED`;
accepted terminal
`DLH_5VT_TANGENT_PROJECTED_NEWTON__NONFINITE_INCONSISTENT_OR_NO_POSITIVE_SAFE_TANGENT_GEOMETRY__BOUNDARY_HJB_ROUTE_REVIEW_REQUIRED`.

Accepted facts: the controlling limiting-wall gradient is the full two-entry
chain rule (`g[wall] = +1/db`, `g[down] = -1/db`, basis identity error `0`);
the official tangent identity holds exactly (`g@d_T = 0`); the safe geometry
expands materially — `alpha_cross_T = 0.16170699931086815`,
`alpha_near = 0.16170683760386884`, `alpha_half = 0.08085341880193442`,
geometry ratio `866.2532997045214`; both trials are strictly domain-safe. But
under the SAME freshly reselected controls the corrected `final=True` and
`final=False` trial operators are **not** equivalent: F0 rowwise gaps
`0.6718037653783657` (rows `{452, 453}`) and `1.3379411925537439` (rows
`{452, 453, 482, 483}`), with bit-identical controls and utility at the affected
rows. That triggers the frozen Outcome C inconsistency clause regardless of the
indicative residual ratios (`0.9193283517706523`, `0.8390465254310803`). At the
accepted `V_*` the two rate paths agree to machine precision, so the divergence
is latent and appears only away from `V_*` near an upwind sign boundary.
**No HJB convergence**; **no accepted iterate**; the divergence does not
establish which rate path is scientifically correct away from `V_*`.

Dedicated Builder branch (integrated into `main`):

`dsh/issue-68-dlh-5vt-tangent-projected-newton-2026-09-15`

Controlling accepted authority: Issue #67 / DLH-5V-S ACCEPTED / CLOSED at
Terminal A (accepted candidate / integration
`a5753bb9fa329a3d85a5652b03d101fa0be6cd32`; reviewer acceptance `5674741491`;
acceptance integration `5674743972`), which established that the genuine
post-repair Bellman residual at `V_*` is ~`10.435`, not ~`490.756`.

### 8.11.1 Scientific question

Issue #64 showed the unconstrained frozen-policy Newton direction is
geometrically capped by the F3 `(13,13), z=1` wall. Issue #68 tests one precise
numerical hypothesis: does removing the first-order normal component of the
plain frozen-policy Newton direction with respect to the single limiting
boundary constraint produce a materially larger boundary-safe step and
meaningful nonlinear residual reduction at the same frozen economics/state?
Local direction-geometry diagnostic only; it does not authorize accepting a new
HJB iterate or a multi-step solver.

### 8.11.2 Frozen state / operator

Reconstruct the exact accepted Issue #63 stagnation state `V_*` using accepted
post-repair sources, reproducing final statistic `3.6614352438846254e-08`, min
boundary `p_b = 4.8089461301970005e-09`, limiting wall F3 `(13,13), z=1`, and
`||R||inf = 10.435094313164921`. Selected-Q repaired blob
`556ccc214f03a1a22306cc4f5c7e9f7691bbf897` remains read-only. Build exactly ONE
current `final=False` operator `Q,u`; define `R = rho V_* - (u + Q V_*)` and
`J = rho I - Q`; solve exactly once `J d_N = -R`.

### 8.11.3 Boundary gradient and exact tangent projection

Use the accepted Issue #62 boundary derivative semantics exactly (regular
backward finite differences on non-`i==0` boundary states; `i==0`
V-independent derivative exactly zero; no `p_b` clipping/flooring). Compute the
limiting-wall `p_b` gradient `g`; require `g` finite, `||g||_2 > 0`, and
`g @ d_N < 0`. Construct exactly ONE projection
`d_T = d_N - g*(g@d_N)/(g@g)`, verify `g @ d_T ≈ 0`, and report `||d_N||inf`,
`||d_T||inf`, `||d_T-d_N||inf` and the frozen linear residual effect `J d_T`
against `J d_N = -R`. No projection-metric optimization and no additional
active constraints.

### 8.11.4 Boundary-safe fraction and exactly two trials

Using all required non-F0 boundary states and `PB_MARGIN = 1e-12`, compute
`alpha_cross_T` as the minimum positive finite
`(p_b_i - PB_MARGIN)/(-dp_i)` over `dp_i < 0` (`+inf` if none), then
`alpha_near = min(1, (1-EPS_ALPHA)*alpha_cross_T)` with `EPS_ALPHA = 1e-6`
(and `alpha_near = 1` when `alpha_cross_T = +inf`), and
`alpha_half = 0.5 * alpha_near`. For exactly these two fractions: form
`V_trial = V_* + alpha*d_T`; verify all required boundary `p_b` finite and
strictly `> PB_MARGIN`; compute the frozen-policy residual with the one frozen
`Q,u`; perform exactly ONE nonlinear policy re-selection with `final=False` and
compute `R_reselect`; then with the same freshly reselected current F0 records
build exactly ONE corrected `final=True` validation operator and compute
`R_final_trial`; verify corrected `final=True` and `final=False` trial operators
remain equivalent to numerical tolerance under the same controls; record
policy/sector/transfer-label switching counts and continuous-control max
changes. Trial states are diagnostic only and MUST NOT become accepted HJB
iterates. No adaptive line search, no alpha tuning, no alternative fractions.

### 8.11.5 Deterministic interpretation rule and terminals

Historical plain-Newton safe-fraction baseline `alpha_cross_N ≈ 1.8667384893e-4`.
A tangent projection is **geometry-improving** iff
`alpha_near / min(1, alpha_cross_N) >= 10`. A trial is **materially
residual-reducing** only if BOTH `||R_reselect||inf / ||R||inf <= 0.50` and
`||R_final_trial||inf / ||R||inf <= 0.50`, with
`MATERIAL_REDUCTION_RATIO = 0.50` and `HALF_ALPHA = 0.5`. Outcome A requires
finite/consistent evidence, the tangent condition, both trial states
domain-safe, the geometry-improving criterion, at least one trial meeting the
dual material-reduction criterion, and an identical deterministic repeat.
Outcome B requires a finite/consistent tangent direction and a domain-safe
positive step but failure of Outcome A's combined criterion. Outcome C covers
nonfinite/inconsistent projection, no positive safe fraction, failed boundary
safety, or corrected-final/iteration inconsistency.

Exactly ONE terminal must be reported:

- A `DLH_5VT_TANGENT_PROJECTED_NEWTON__SINGLE_WALL_TANGENT_PROJECTION_EXPANDS_SAFE_GEOMETRY_AND_MATERIALLY_REDUCES_NONLINEAR_RESIDUAL__CONSTRAINED_DIRECTION_DESIGN_GATE_READY`
- B `DLH_5VT_TANGENT_PROJECTED_NEWTON__TANGENT_DIRECTION_FINITE_AND_DOMAIN_SAFE_BUT_GEOMETRY_OR_RESIDUAL_IMPROVEMENT_INSUFFICIENT__FURTHER_DIRECTION_DESIGN_REQUIRED`
- C `DLH_5VT_TANGENT_PROJECTED_NEWTON__NONFINITE_INCONSISTENT_OR_NO_POSITIVE_SAFE_TANGENT_GEOMETRY__BOUNDARY_HJB_ROUTE_REVIEW_REQUIRED`
- Blocked `BLOCKED_DLH_5VT_AUTHORITY_OR_DEPENDENCY_CONFLICT`

### 8.11.6 Builder allowlist (four new paths only)

1. `src/deep_learning_hank/two_asset/tangent_projected_newton_geometry.py`
2. `tests/test_dlh_5vt_tangent_projected_newton_geometry.py`
3. `reports/dlh_5vt_tangent_projected_newton_geometry_2026_09_15/DLH_5VT_TANGENT_PROJECTED_NEWTON_GEOMETRY_REPORT.md`
4. `reports/dlh_5vt_tangent_projected_newton_geometry_2026_09_15/DLH_5VT_TANGENT_PROJECTED_NEWTON_GEOMETRY_SUMMARY.csv`

No fifth tracked Builder path. All accepted source/test/report/governance files
remain read-only.

### 8.11.7 Forbidden

No mutation of selected-Q or any accepted source from Issues #61–#67; no
economics/prices/grid/domain/initialization/controls/tolerances/`PB_MARGIN`/
Bellman-tolerance change; no convergence-criterion change; no accepted trial as
an HJB iterate; no multi-step Newton / policy iteration / semismooth /
trust-region / continuation; no adaptive line search or alpha tuning; no
multiple active constraints or projection-metric optimization; no `p_b`
clip/floor; no price/Wmax/resolution sweep; no KFE / stationary KFE /
`solve_household_steady_state`; no SCC/global-Q / GE / multi-region / neural /
nominal / calibration / policy / welfare / Results; no PR; no merge; no Issue
close; no successor; no self-accept.

Stationary KFE remains **NOT AUTHORIZED**.

---

## 8.12 Issue #69 / DLH-5V-U — latent F0 iteration-rate vs raw-drift sign divergence away from `V_*` — TERMINAL A ACCEPTED / CLOSED (OWNER RATE-SEMANTICS DECISION NEXT)

Title:

`DLH-5V-U: Audit latent F0 iteration-rate vs raw-drift sign divergence away from V*`

Task type:

`SCIENTIFIC_NUMERICAL_DIAGNOSTIC__F0_ITERATION_RATE_VS_RAW_DRIFT_SIGN_PROVENANCE_AWAY_FROM_VSTAR`

Owner / Reviewer route decision:

`APPROVE_F0_ITERATION_RATE_VS_RAW_DRIFT_SIGN_PROVENANCE_AUDIT_AFTER_5VT_TERMINAL_C`

Authority marker:

`DLH_5VU_F0_RATE_PATH_DIVERGENCE_AUDIT_AUTHORIZED`

Initial authoritative activation comment:

`5676828795` (final authoritative activation-refresh `5677087565`)

Builder execution is **complete and ACCEPTED / CLOSED** at Terminal A. Accepted
candidate / integration:
`a08ad35c1dfea212fdc34c276e332b985af1a59f` (reviewer acceptance `5678488562`;
acceptance integration `5678493024`, fast-forward, not a merge commit). Accepted
verdict
`DLH_5VU_ACCEPTED__TERMINAL_A_CONFIRMED__UNIQUE_SOURCE_BACKED_F0_B_RATE_SIGN_BRANCH_DIVERGENCE_FULLY_ACCOUNTS_FOR_ISSUE68_TRIAL_OPERATOR_GAPS__OWNER_RATE_SEMANTICS_DECISION_REQUIRED`;
accepted terminal
`DLH_5VU_F0_RATE_PATH_DIVERGENCE__UNIQUE_SIGN_OR_BRANCH_MECHANISM_ESTABLISHED_AND_FULLY_ACCOUNTS_FOR_TRIAL_OPERATOR_GAPS__RATE_SEMANTICS_SCIENTIFIC_REVIEW_GATE_READY`.

Accepted facts: both frozen Issue #68 trial disparities reproduce exactly
(`alpha_half` gap `0.6718037653783657` on rows `{452, 453}`; `alpha_near` gap
`1.3379411925537439` on rows `{452, 453, 482, 483}`); across all `596` F0 rows
the b-rate divergent counts are `2` / `4`, the a-rate divergent counts are
`0` / `0`, the destination-layout and omitted-rate divergent counts are `0` / `0`,
and the max decomposition residual is `3.552713678800501e-15`; stored and
recomputed realized `mu_a` / `mu_b` are bit-identical on the affected rows; every
affected row has realized `mu_b < 0`, so the corrected raw-drift path has
`b_forward = 0` while the iteration path carries a positive
`iteration_b_forward_rate`; source provenance confirms iteration b-rates come
from branch-gated `sc_b`/`sc_f` + `sdh_b`/`sdh_f` FOC/shadow objects while the
corrected final raw rates come from `max(±mu_b)/db`; the unique observed
mechanism is `liquid_label == "F"` / branch-gated positive forward iteration
component while realized `mu_b < 0`, which fully accounts for the Issue #68 gaps.

Reviewer qualification (binding): the acceptance is **limited to attribution of
the observed Issue #68 trial discrepancies** and does **NOT** adopt the broader
claim that the two rate constructions coincide *only* whenever
`liquid_label == "0"` as a global theorem over the entire state/control space.
**No authoritative rate path has been selected.** No HJB convergence and no
accepted new HJB iterate. Stationary KFE remains **NOT AUTHORIZED**.

Dedicated Builder branch (integrated into `main`):

`dsh/issue-69-dlh-5vu-f0-rate-path-divergence-2026-09-15`

Controlling accepted authority: Issue #68 / DLH-5V-T ACCEPTED / CLOSED at
Terminal C (accepted candidate / integration
`15083e5c9f089406aa69326bc84dbe2db0e42be8`; reviewer acceptance `5676811925`;
acceptance integration `5676816068`), which exposed the latent trial-level
divergence between the accepted `final=False` iteration-rate path and the
corrected `final=True` raw-drift rate path under identical controls.

### 8.12.0 Owner scientific decision gate — RESOLVED: ROUTE A SELECTED

The Owner explicitly selected **Route A** on 2026-09-15:

> MATLAB-faithful iteration-rate semantics remain authoritative for the HJB
> operator.

Binding single-`Q` operator contract from that decision:

- Route A selected by the Owner; **Route B and Route C are not selected**;
- MATLAB-faithful selected iteration-rate semantics ARE authoritative for the HJB
  operator;
- the solve, final validation and any future authorized `Q^T` mass dynamics must
  share **one coherent selected generator**;
- raw-drift `max(±mu)/step` is **NOT** an independent final-validation `Q`
  authority;
- **dual-`Q` semantics are NOT AUTHORIZED**.

The gate is closed and Issue #70 / DLH-5V-V is the authorized successor that
implements the Route-A F0 `final=True` consolidation.

### 8.12.1 Scientific question

Before any further constrained-direction solver design, determine the exact
source/provenance mechanism of the latent F0 operator divergence: does it come
from (1) the stored iteration-rate construction of the accepted
MATLAB-faithful local-policy path, (2) the corrected `final=True` raw-drift
`max(±mu)/step` rates, (3) sign/tie-breaking or truncation differences around
`mu ≈ 0` / finite-difference branch boundaries, (4) destination availability /
diagonal accounting, or (5) another source-backed mechanism? Diagnostic only —
it does NOT authorize changing either rate path.

### 8.12.2 Frozen states and decomposition

Only the two accepted Issue #68 frozen trial states may be used:
`alpha_half = 0.08085341880193442`; `alpha_near = 0.16170683760386884`. No third
trial state. Must reproduce the accepted Issue #68 operator inconsistencies:
`alpha_half` F0 rowwise gap `0.6718037653783657` on rows `{452, 453}`;
`alpha_near` F0 rowwise gap `1.3379411925537439` on rows
`{452, 453, 482, 483}`.

At each frozen trial, exactly: ONE `final=False` nonlinear policy re-selection;
ONE corrected `final=True` same-control build; ONE all-F0 compact rate/row
decomposition. Per inconsistent F0 row persist: state `(node, j, i, z)`;
sector / transfer label; consumption / labor / transfer / utility; stored
`mu_a`, `mu_b`; recomputed raw `mu_a`, `mu_b`; iteration `b_backward`,
`b_forward`, `a_backward`, `a_forward` rates; raw-drift `b_backward`,
`b_forward`, `a_backward`, `a_forward` rates; rate sign / active direction per
axis; diagonal; represented destination columns and rates; omitted destination
rate; rowwise `Q_final - Q_iter` non-zero columns and magnitudes — plus
counts/maxima over ALL F0 rows. No full sparse matrices persisted.

### 8.12.3 Source-backed provenance audit

Read-only trace the accepted oracle/selected-Q implementation (not inferred from
names or docstrings): how iteration b-rates and a-rates are built from the
selected local policy and finite-difference branches; any clipping, sign /
tie-breaking, branch selection, shadow-rate, transfer or truncation convention
entering those rates; how corrected `final=True` recomputes raw drifts from the
SAME controls and maps them through `max(±mu)/step`; whether the two
constructions are mathematically guaranteed equivalent or only coincide on a
subset of states; and the exact local condition that flips the upwind direction
in the Issue #68 affected rows.

### 8.12.4 Deterministic classification

Frozen diagnostic flags: `ITER_RATE_PATH_SOURCE_BACKED`,
`FINAL_RAW_PATH_SOURCE_BACKED`, `RATE_FORMULAS_GLOBALLY_EQUIVALENT`,
`SIGN_OR_BRANCH_DIVERGENCE_ESTABLISHED`,
`TRUNCATION_OR_DESTINATION_DIVERGENCE_ESTABLISHED`,
`OTHER_MECHANISM_ESTABLISHED`, `MIXED_OR_UNRESOLVED`. The classification must
not choose which operator is scientifically authoritative away from `V_*`
unless the source provenance proves it uniquely.

### 8.12.5 Exact execution design and terminals

Execute exactly: ONE deterministic reconstruction of `V_*` plus the accepted
Issue #68 full-gradient tangent geometry; exactly TWO frozen trial states; at
each trial ONE `final=False` re-selection and ONE corrected `final=True`
same-control build; ONE all-F0 compact rate/row decomposition per trial; ONE
read-only source provenance mapping; ONE deterministic repeat. No accepted new
HJB iterate, no new direction solve, no line search, no additional trial.

Exactly ONE terminal must be reported:

- A `DLH_5VU_F0_RATE_PATH_DIVERGENCE__UNIQUE_SIGN_OR_BRANCH_MECHANISM_ESTABLISHED_AND_FULLY_ACCOUNTS_FOR_TRIAL_OPERATOR_GAPS__RATE_SEMANTICS_SCIENTIFIC_REVIEW_GATE_READY`
- B `DLH_5VU_F0_RATE_PATH_DIVERGENCE__UNIQUE_TRUNCATION_OR_DESTINATION_MECHANISM_ESTABLISHED_AND_FULLY_ACCOUNTS_FOR_TRIAL_OPERATOR_GAPS__RATE_SEMANTICS_SCIENTIFIC_REVIEW_GATE_READY`
- C `DLH_5VU_F0_RATE_PATH_DIVERGENCE__MIXED_OR_UNRESOLVED_SOURCE_PROVENANCE__OWNER_SCIENTIFIC_REVIEW_REQUIRED`
- Blocked `BLOCKED_DLH_5VU_AUTHORITY_OR_DEPENDENCY_CONFLICT`

### 8.12.6 Builder allowlist (four new paths only)

1. `src/deep_learning_hank/two_asset/f0_rate_path_divergence_audit.py`
2. `tests/test_dlh_5vu_f0_rate_path_divergence.py`
3. `reports/dlh_5vu_f0_rate_path_divergence_2026_09_15/DLH_5VU_F0_RATE_PATH_DIVERGENCE_REPORT.md`
4. `reports/dlh_5vu_f0_rate_path_divergence_2026_09_15/DLH_5VU_F0_RATE_PATH_DIVERGENCE_SUMMARY.csv`

No fifth tracked Builder path. All accepted source/test/report/governance files
remain read-only.

### 8.12.7 Forbidden

No mutation of selected-Q, the oracle, or any accepted Issue #61–#69 scientific
source; no choosing or replacing the authoritative rate path; no
convergence-criterion change; no economics/prices/grid/domain/initialization/
controls/tolerances/`PB_MARGIN`/Bellman-tolerance change; no accepted trial as
an HJB iterate; no new Newton / tangent / constrained direction; no multi-step
Newton / policy iteration / semismooth / trust-region / continuation / line
search; no additional trial state or alpha tuning; no price/Wmax/resolution
sweep; no KFE / stationary KFE / `solve_household_steady_state`; no
SCC/global-Q / GE / multi-region / neural / nominal / calibration / policy /
welfare / Results; no PR; no merge; no Issue close; no successor; no
self-accept.

While the Owner gate was open this also forbade starting any new Builder Issue or
branch and any further constrained-direction or convergence-rule work. The gate
is now resolved (Route A) and Issue #70 / DLH-5V-V is the authorized successor;
all other constraints above continue to apply unchanged.

Stationary KFE remains **NOT AUTHORIZED**.

---

## 8.13 Issue #70 / DLH-5V-V — Route-A single-`Q` F0 operator-contract consolidation and final Bellman revalidation — TERMINAL A ACCEPTED / CLOSED

Title:

`DLH-5V-V: Consolidate Route-A single-Q F0 operator contract and revalidate final Bellman operator`

Task type:

`OWNER_AUTHORIZED_SCIENTIFIC_CHANGE__MATLAB_FAITHFUL_SINGLE_Q_F0_OPERATOR_CONTRACT_CONSOLIDATION_AND_REVALIDATION`

Owner / Reviewer route decision:

`APPROVE_ROUTE_A_MATLAB_FAITHFUL_SINGLE_Q_F0_OPERATOR_CONTRACT`

Authority marker:

`DLH_5VV_ROUTE_A_SINGLE_Q_OPERATOR_CONTRACT_AUTHORIZED`

Initial authoritative activation comment:

`5681294485`

Final authoritative activation-refresh:

`5682174361`

Reviewer hold (bounded post-Route-A contract migration):

`5690304999`

Reviewer final hold (policy-label identity):

`5691015137`

Accepted candidate / integration:

`fb5523d55d01d4b64995d94efb786994b5f8326d`

Reviewer acceptance:

`5691693472`

Acceptance integration:

`5691696204`

Accepted verdict:

`DLH_5VV_ACCEPTED__TERMINAL_A_CONFIRMED__OWNER_ROUTE_A_SINGLE_Q_F0_CONTRACT_CONSOLIDATED__FINAL_VALIDATION_BIT_IDENTICAL_TO_SELECTED_ITERATION_GENERATOR_AT_S0_S1_S2__POLICY_LABEL_IDENTITY_RESTORED__FULL_SUITE_GREEN__HJB_RESIDUAL_REASSESSMENT_REQUIRED`

Accepted terminal:

`DLH_5VV_ROUTE_A_SINGLE_Q_OPERATOR_CONTRACT__FINAL_VALIDATION_REUSES_MATLAB_FAITHFUL_SELECTED_ITERATION_GENERATOR_AT_ALL_FROZEN_STATES__DUAL_RATE_GAP_REMOVED__HJB_RESIDUAL_REASSESSMENT_READY`

Accepted selected-Q blob:

`7857cabb4d28af99cb9d59e2d1c3024b05787c11`

Dedicated Builder branch (integrated into `main`):

`dsh/issue-70-dlh-5vv-route-a-single-q-operator-contract-2026-09-15`

Preserved ancestry (no rebase): original scientific commit
`825e241804c7fb260c807602fc0f1487caf84e56`; contract-migration commit
`0e3a9597cd5550a237452aeaa57ed0a145aa6c83`; final remediation / accepted
candidate `fb5523d55d01d4b64995d94efb786994b5f8326d`.

Controlling accepted authority: Issue #69 / DLH-5V-U ACCEPTED / CLOSED at
Terminal A (accepted candidate / integration
`a08ad35c1dfea212fdc34c276e332b985af1a59f`; reviewer acceptance `5678488562`;
acceptance integration `5678493024`), which uniquely attributed every observed
Issue #68 trial discrepancy to the F0 b-rate sign/branch difference without
choosing an authoritative path. The Owner chose Route A.

### 8.13.1 Exact accepted scientific change

Mutated only the F0 `final=True` validation assembly in
`src/deep_learning_hank/two_asset/boundary_hjb_selected_q.py`:

- the supplied selected F0 record's stored `row_entries` / iteration rates /
  `diagonal` / `utility` **directly define** the final-validation row;
- the supplied selected record's policy/sector label is preserved VERBATIM
  (`sector=rec.sector` and `sector_arr[node, nz] = rec.sector`), so selected
  controls AND selected policy labels are unchanged by final validation; no
  `INTERIOR_FINAL` retag remains anywhere in the module;
- same-z-block destination indexing preserved;
- **no** second F0 `Q` from `asset_drifts_matlab_faithful` + `max(±mu)/step`;
- `final=True` uses the SAME selected-generator semantics as `final=False`.

Three commits realize this: the original Route-A consolidation (`825e241…`), a
bounded post-Route-A contract migration of ten authorized paths (`0e3a959…`,
Reviewer hold `5690304999`), and a bounded policy-label remediation
(`fb5523d…`, Reviewer final hold `5691015137`).

### 8.13.2 Frozen non-change boundary

No alteration to `select_matlab_faithful_local_policy`; iteration `final=False`
F0 semantics; the accepted oracle; boundary families F1–F11; the switch matrix;
grid/domain/state variables; economics/prices/calibration; controls/policy
selection; initialization; tolerances, `PB_MARGIN`, Bellman tolerance; or the
convergence criterion.

### 8.13.3 Exact validation states and accepted result

Exactly THREE frozen states, with no search and no alpha tuning:

- **S0** — accepted Issue #63 stagnation state `V_*` (final statistic
  `3.6614352438846254e-08`; min boundary `p_b = 4.8089461301970005e-09`; wall F3
  `(13,13), z=1`; iteration residual `10.435094313164921`);
- **S1** — accepted Issue #68 `alpha_half = 0.08085341880193442`;
- **S2** — accepted Issue #68 `alpha_near = 0.16170683760386884`.

At each state: exactly ONE `final=False` build producing `Q_iter, u_iter,
records`, then exactly ONE Route-A `final=True` build using those SAME records.
Verified: F0 rowwise `|Q_final - Q_iter|`; non-F0 rowwise difference; global max
difference; `u_final - u_iter` max difference; diagonal difference; represented
destination/rate difference; `max|Q1|` for both; Bellman residuals
`R_iter = rho V - (u_iter + Q_iter V)` and
`R_final = rho V - (u_final + Q_final V)` with norms and argmax states; and that
selected controls AND policy labels are unchanged by final validation.

Measured and ACCEPTED result:

- `Q_final == Q_iter` and `u_final == u_iter` were **exactly `0.0`** at all three
  states, i.e. bit-identical rather than merely within tolerance;
- controls / `mu` / diagonal / destinations / represented rates / residual vector
  all identical;
- policy/sector label mismatch rows = `0` / `0` / `0`;
- the historical Issue #68 S1/S2 gaps (`0.6718037653783657`,
  `1.3379411925537439`) **collapsed to exactly `0.0`** while remaining preserved
  as historical evidence;
- S0 residual remained `10.435094313164921`;
- full repository suite: `641 passed`, `0 failed`, `0 errors`, `6` pre-existing
  oracle warnings.

**No HJB convergence claim**: Bellman tolerance remains the unchanged `1e-3`, so
S0 remains not converged (`~10435`× tolerance).

### 8.13.4 Accepted execution design

ONE minimal source mutation implementing Route A in the F0 `final=True`
assembly; ONE deterministic reconstruction of `V_*` and the accepted Issue #68
tangent direction; exactly the THREE frozen-state checks S0/S1/S2; at each state
ONE `final=False` build and ONE Route-A `final=True` build; ONE deterministic
repeat of the full three-state validation; focused tests plus the full repository
suite. No new HJB iteration trajectory. A bounded post-Route-A contract migration
of ten Reviewer-authorized paths followed, then a bounded policy-label
remediation.

### 8.13.5 Builder allowlist (four paths only, historical)

1. `src/deep_learning_hank/two_asset/boundary_hjb_selected_q.py`
2. `tests/test_dlh_5vv_route_a_single_q_operator_contract.py`
3. `reports/dlh_5vv_route_a_single_q_operator_contract_2026_09_15/DLH_5VV_ROUTE_A_SINGLE_Q_OPERATOR_CONTRACT_REPORT.md`
4. `reports/dlh_5vv_route_a_single_q_operator_contract_2026_09_15/DLH_5VV_ROUTE_A_SINGLE_Q_OPERATOR_CONTRACT_SUMMARY.csv`

No fifth tracked Builder path. All other accepted source/test/report/governance
files remain read-only.

Exactly ONE terminal was to be reported; **Terminal A** was reported and
accepted:

- A `DLH_5VV_ROUTE_A_SINGLE_Q_OPERATOR_CONTRACT__FINAL_VALIDATION_REUSES_MATLAB_FAITHFUL_SELECTED_ITERATION_GENERATOR_AT_ALL_FROZEN_STATES__DUAL_RATE_GAP_REMOVED__HJB_RESIDUAL_REASSESSMENT_READY`
- B `DLH_5VV_ROUTE_A_SINGLE_Q_OPERATOR_CONTRACT__ROUTE_A_IMPLEMENTED_BUT_MATERIAL_FINAL_VS_ITERATION_OPERATOR_DISCREPANCY_REMAINS__SCIENTIFIC_REPAIR_REVIEW_REQUIRED`
- C `DLH_5VV_ROUTE_A_SINGLE_Q_OPERATOR_CONTRACT__NONFINITE_REGRESSION_OR_CONTRACT_FAILURE__SCIENTIFIC_REPAIR_REVIEW_REQUIRED`
- Blocked `BLOCKED_DLH_5VV_AUTHORITY_OR_DEPENDENCY_CONFLICT`

### 8.13.6 Forbidden

No mutation of the accepted oracle; no modification of iteration `final=False`
rate semantics; no policy-selection / control change; no F1–F11 boundary-semantics
change; no economics/prices/grid/domain/initialization/tolerances/`PB_MARGIN`/
Bellman-tolerance change; no convergence-criterion change; no accepted state as a
new HJB iterate; no multi-step Newton / policy iteration / semismooth /
trust-region / continuation / line search; no alpha tuning or extra trial states;
no price/Wmax/resolution sweep; no KFE / stationary KFE /
`solve_household_steady_state`; no SCC/global-Q / GE / multi-region / neural /
nominal / calibration / policy / welfare / Results; no PR; no merge; no Issue
close; no successor; no self-accept.

Stationary KFE remains **NOT AUTHORIZED**.

## 8.14 Issue #71 / DLH-5V-W — decompose the remaining Route-A single-`Q` HJB residual at `V*` — TERMINAL B ACCEPTED / CLOSED

Title:

`DLH-5V-W: Decompose the remaining Route-A single-Q HJB residual at V*`

Task type:

`SCIENTIFIC_NUMERICAL_DIAGNOSTIC__ROUTE_A_SINGLE_Q_HJB_RESIDUAL_SOURCE_DECOMPOSITION`

Owner / Reviewer route decision:

`APPROVE_ROUTE_A_SINGLE_Q_HJB_RESIDUAL_SOURCE_DECOMPOSITION_AFTER_5VV_TERMINAL_A`

Authority marker:

`DLH_5VW_ROUTE_A_HJB_RESIDUAL_DECOMPOSITION_AUTHORIZED`

Initial authoritative activation comment:

`5691703381`

Final authoritative activation-refresh:

`5691863227`

Reviewer hold / bounded allowlist expansion (fifth path authorized):

`5695153100`

Accepted candidate / integration:

`e1d79d6aa6677ca262df1699e21007eaf9690c4d`

Reviewer acceptance:

`5696620837`

Acceptance integration:

`5696624495`

Accepted verdict:

`DLH_5VW_ACCEPTED__TERMINAL_B_CONFIRMED__ROUTE_A_SINGLE_Q_RESIDUAL_DECOMPOSITION_CLOSES__TOP20_POLICY_RECORDS_REPRODUCE_EXACTLY__NO_UNIQUE_DOMINANT_COMPONENT__MIXED_FIXED_POINT_IMBALANCE_REQUIRES_BOUNDED_SOLVER_DESIGN`

Accepted terminal:

`DLH_5VW_ROUTE_A_HJB_RESIDUAL_DECOMPOSITION__DECOMPOSITION_AND_POLICY_REPRODUCTION_PASS_BUT_RESIDUAL_IS_MIXED_FIXED_POINT_IMBALANCE__BOUNDED_SOLVER_DESIGN_REQUIRED`

Accepted selected-Q blob (unchanged):

`7857cabb4d28af99cb9d59e2d1c3024b05787c11`

Dedicated Builder branch (integrated into `main`):

`dsh/issue-71-dlh-5vw-route-a-hjb-residual-decomposition-2026-09-16`

Preserved ancestry (no rebase): original candidate
`8eeb2949d51ff17c631dd664e6d94ee136d0c0d9`; remediation / accepted candidate
`e1d79d6aa6677ca262df1699e21007eaf9690c4d`.

Controlling accepted authority: Issue #70 / DLH-5V-V ACCEPTED / CLOSED at
Terminal A (accepted candidate / integration
`fb5523d55d01d4b64995d94efb786994b5f8326d`; reviewer acceptance `5691693472`;
acceptance integration `5691696204`; accepted selected-Q blob
`7857cabb4d28af99cb9d59e2d1c3024b05787c11`). Owner Route A remains binding: one
coherent MATLAB-faithful selected generator governs F0 solve and final
validation, and dual-`Q` semantics are NOT AUTHORIZED.

### 8.14.1 Exact accepted scientific scope

Read-only diagnostic / source decomposition at exactly ONE frozen state: the
accepted Issue #63 stagnation state `V_*`. It did not choose or replace any rate
path, did not construct a second scientific `Q`, did not accept an HJB iterate,
and did not mutate any accepted source.

The accepted `V_*` was reproduced exactly: `8` steps; final statistic
`3.6614352438846254e-08`; min boundary `p_b = 4.8089461301970005e-09`; wall
`F3 (13,13), z=1, node 332`; `||R||inf = 10.435094313164921`; residual argmax =
row `97` / node `97` / z `0` / family `F0`.

Exactly ONE operator build was used: **ONE Route-A `final=False` `Q`**. No second
scientific `Q` path, no `final=True` second generator, no dual-`Q` semantics.

### 8.14.2 Accepted residual decomposition

Additive decomposition over ALL states, `R = rho*V - u - Q*V`, recording
`rho*V`; utility / source; z-switch; b-backward; b-forward; a-backward;
a-forward; boundary; diagonal; reconstructed residual; and closure error. The
nine components sum to the residual, with:

- decomposition closure max = `4.036238010485249e-11`;
- independent row reconstruction max = `2.816165078911581e-10`;
- rate attribution mismatch rows = `0`;
- `max|Q1| = 2.4253377084448857e-12` (unchanged).

Deterministic top-20 by `|R|` with tie-break row id; accepted top-20 are all F0 /
z=0, with full per-row evidence (controls, drifts, stored rate slots,
neighbours, represented destinations, all nine components, sign/magnitude).

### 8.14.3 Accepted policy reproduction audit

Read-only re-invocation of the accepted local-policy selector on the top-20 F0
rows: **`20 / 20`** reproduced, with controls / utility / drifts / stored rates
differences exactly `0` and branch labels matching. No new policy optimization.

### 8.14.4 Accepted classification and terminal

Frozen flags: `DECOMPOSITION_CLOSED = YES`; `DOMINANT_RESIDUAL_F0 = YES`;
`POLICY_RECORDS_REPRODUCED = YES`; `DOMINANT_COMPONENT_IDENTIFIED = NO`;
`BRANCH_INCONSISTENCY_ESTABLISHED = NO`; `OTHER_MECHANISM_ESTABLISHED = NO`;
`MIXED_OR_UNRESOLVED = YES`.

Mean top-20 cancellation ratio = `0.006665998653866562`: the residual is ~`0.67%`
of the gross component mass, i.e. a near-total cancellation of `O(1e3)` terms
rather than one dominant runaway component.

**Terminal B** accepted. Full repository suite: `693 passed`, `0 failed`,
`0 errors`, `6` pre-existing oracle warnings. Deterministic repeat identical.

### 8.14.5 Builder allowlist (four new paths; the fifth authorized by hold `5695153100`)

1. `src/deep_learning_hank/two_asset/route_a_hjb_residual_decomposition.py`
2. `tests/test_dlh_5vw_route_a_hjb_residual_decomposition.py`
3. `reports/dlh_5vw_route_a_hjb_residual_decomposition_2026_09_16/DLH_5VW_ROUTE_A_HJB_RESIDUAL_DECOMPOSITION_REPORT.md`
4. `reports/dlh_5vw_route_a_hjb_residual_decomposition_2026_09_16/DLH_5VW_ROUTE_A_HJB_RESIDUAL_DECOMPOSITION_SUMMARY.csv`
5. `tests/test_dlh_5vv_route_a_single_q_operator_contract.py` (bounded
   repository-state assertion correction only, authorized by hold `5695153100`)

No sixth tracked Builder path. All other accepted source/test/report/governance
files remain read-only.

### 8.14.6 Forbidden

No mutation of selected-Q, the oracle, or any accepted Issue #60–#70 source; no
`final=False` / `final=True` semantics change; no policy-selection / control
change; no F1–F11 boundary-semantics change; no
economics/prices/grid/domain/initialization/calibration change; no
tolerances/`PB_MARGIN`/Bellman-tolerance change; no convergence-criterion change;
no accepted state as a new HJB iterate; no new trajectory; no Newton solve /
tangent direction / trial step / policy iteration / semismooth / trust-region /
continuation / line search; no alpha tuning; no price/Wmax/resolution sweep; no
KFE / stationary KFE / `solve_household_steady_state`; no SCC/global-Q / GE /
multi-region / neural / nominal / calibration / policy / welfare / Results; no PR;
no merge; no Issue close; no successor; no self-accept.

Stationary KFE remains **NOT AUTHORIZED**.

## 8.15 Issue #72 / DLH-5V-X — design a bounded residual-balanced single-`Q` HJB solver contract after the mixed-imbalance diagnosis — TERMINAL B ACCEPTED / CLOSED

Title:

`DLH-5V-X: Design a bounded residual-balanced single-Q HJB solver contract after mixed-imbalance diagnosis`

Task type:

`SCIENTIFIC_NUMERICAL_DESIGN__ROUTE_A_SINGLE_Q_BOUNDED_RESIDUAL_BALANCED_HJB_SOLVER_CONTRACT`

Owner / Reviewer route decision:

`APPROVE_ROUTE_A_BOUNDED_RESIDUAL_BALANCED_SOLVER_CONTRACT_DESIGN_AFTER_5VW_TERMINAL_B`

Authority marker:

`DLH_5VX_ROUTE_A_BOUNDED_SOLVER_DESIGN_AUTHORIZED`

Initial authoritative activation comment:

`5696637965`

Final authoritative activation-refresh:

`5697299096`

Reviewer hold / bounded artifact-consistency remediation:

`5699275937`

Accepted candidate / integration:

`5d2f489f8dfb3527c0e4bd7dc418e35139b9dbd9`

Reviewer acceptance:

`5714106614`

Acceptance integration:

`5714110964`

Accepted verdict:

`DLH_5VX_ACCEPTED__TERMINAL_B_CONFIRMED__BOUNDED_SINGLE_Q_OUTER_FRAME_FROZEN__THREE_DIRECTION_FAMILIES_REMAIN_ADMISSIBLE_AT_FAMILY_LEVEL__PSEUDO_TIME_RESOLVENT_REFUTED__DIRECTION_SELECTION_GATE_REQUIRED`

Accepted terminal:

`DLH_5VX_ROUTE_A_BOUNDED_SOLVER_DESIGN__MULTIPLE_PLAUSIBLE_ROUTES_REMAIN__OWNER_OR_REVIEWER_ROUTE_SELECTION_REQUIRED`

Accepted selected-Q blob (unchanged):

`7857cabb4d28af99cb9d59e2d1c3024b05787c11`

Dedicated Builder branch (integrated into `main`):

`dsh/issue-72-dlh-5vx-route-a-bounded-solver-design-2026-09-16`

Preserved ancestry (no rebase): original candidate
`d06f53e4fe55d8823f2d7cca3a9838cd79b1a107`; remediation / accepted candidate
`5d2f489f8dfb3527c0e4bd7dc418e35139b9dbd9`.

### 8.15.1 Accepted design outcome

A **DESIGN / SPECIFICATION ONLY** task that synthesized accepted Issues #60–#71
evidence (nine entries, five negative), compared four candidate numerical families
across eight frozen admissibility axes, and froze a complete executable bounded
solver contract — while honestly declining to select a single route because three
families remained admissible.

| Family | Admissible |
|---|---|
| policy-frozen / regularized Newton | **YES** (as a direction inside the frame) |
| residual / Jacobi preconditioned correction | **YES** |
| constrained / projected LSQ or trust-region | **YES** (the outer frame) |
| pseudo-time / resolvent | **NO — refuted by accepted #60 and #61 evidence** |

Because three families remained admissible, the frozen selection rule (which
requires exactly one admissible family AND at least one refuted alternative) could
not certify a unique route: **Terminal B**.

### 8.15.2 Accepted frozen contract and ladders

The direction-agnostic outer frame is frozen with 19 contract clauses (V-only state;
Route-A residual; full-reassembly-only `Q` refresh; `J = rho I - Q_frozen`;
regularization / trust-radius / step-fraction ladders; active-boundary detection
using the FULL wall gradient with MULTIPLE stacked gradients; candidate-state
positive-`p_b` domain safety; projection rule; residual-based merit; Armijo
acceptance; deterministic three-ladder backoff; finite attempt budgets; separated
iterate-change and Bellman-residual criteria; six named fail-closed terminals;
per-attempt logging with domain margin and decision reason).

Frozen ladders: `lambda`, trust-radius fraction and step-fraction each
`{2^-k, k = 0..20}` (floor `9.5367431640625e-07`). Frozen thresholds:
`ARMIJO_COEFFICIENT = 1e-4`; `REQUIRED_RESIDUAL_REDUCTION_RATIO = 0.5`;
`MIN_RESIDUAL_REDUCTION_ABSOLUTE = 1e-12`; `CONSTRAINT_TOLERANCE = 1e-9`;
`ACTIVE_BOUNDARY_TOLERANCE = 1e-12`; `CANDIDATE_PB_MARGIN = 1e-12`;
`LINEAR_SOLVE_RTOL = 1e-12`; `LINEAR_RESIDUAL_TOL = 1e-10`;
`ITERATE_CHANGE_TOL = 1e-7`; `BELLMAN_RESIDUAL_TOL = 1e-3`;
`RESIDUAL_REFERENCE = 10.435094313164921`. Max attempts `21/21/21`, total `63`,
outer `1000`, linear `4`. No adaptive hedge language anywhere.

Accepted evidence: deterministic repeat = **TRUE** (structurally guaranteed);
consistency checks **38/38**; focused suite **56 passed**; full clean-tree suite
**749 passed / 0 failed / 0 errors / 6** pre-existing oracle warnings; **no
`V_new`**; no executed solver step; no accepted iterate; **HJB convergence =
FALSE**; Stationary KFE **NOT AUTHORIZED**.

### 8.15.3 Reviewer route selection made after acceptance

`POLICY_FROZEN_REGULARIZED_NEWTON_DIRECTION_WITHIN_ACCEPTED_PROJECTED_CONSTRAINED_OUTER_FRAME`

Basis: Issue #64 contains direct measured Newton-direction evidence and Issue #68
contains accepted full-wall projected geometry plus residual-reduction evidence on
the iteration operator, while the residual / Jacobi direction remains entirely
unmeasured. A **bounded first-probe selection only** — NOT a claim of global
superiority or convergence. It is activated in Issue #73 below.

### 8.15.4 Builder allowlist (four new paths only)

1. `src/deep_learning_hank/two_asset/route_a_bounded_solver_design.py`
2. `tests/test_dlh_5vx_route_a_bounded_solver_design.py`
3. `reports/dlh_5vx_route_a_bounded_solver_design_2026_09_16/DLH_5VX_ROUTE_A_BOUNDED_SOLVER_DESIGN_REPORT.md`
4. `reports/dlh_5vx_route_a_bounded_solver_design_2026_09_16/DLH_5VX_ROUTE_A_BOUNDED_SOLVER_DESIGN_SUMMARY.csv`

No fifth tracked Builder path. All other accepted source/test/report/governance
files remain read-only.

### 8.15.5 Forbidden

No mutation of selected-Q, the oracle, or any accepted Issue #60–#71 source; no
`final=False` / `final=True` semantics change; no policy-selection / control
change; no F1–F11 boundary-semantics change; no
economics/prices/grid/domain/initialization/calibration change; no
tolerances/`PB_MARGIN`/Bellman-tolerance change; no convergence-criterion change;
no new nonlinear HJB state; no accepted iterate; no new trajectory; no execution
of Newton / tangent / trust-region / line-search / continuation / pseudo-time /
resolvent; no KFE / stationary KFE / steady state; no SCC/global-Q / GE /
multi-region / neural / nominal / calibration / policy / welfare / Results; no PR;
no merge; no Issue close; no successor; no self-accept.

Stationary KFE remains **NOT AUTHORIZED**.

## 8.16 Issue #73 / DLH-5V-Y — execute one bounded Route-A projected regularized-Newton step at `V*` — NEXT ACTIVE (BUILDER NOT YET OPERATIVE)

Title:

`DLH-5V-Y: Execute one bounded Route-A projected regularized-Newton step at V*`

Task type:

`SCIENTIFIC_NUMERICAL_EXECUTION__ROUTE_A_SINGLE_Q_ONE_STEP_PROJECTED_REGULARIZED_NEWTON`

Reviewer bounded numerical route selection:

`POLICY_FROZEN_REGULARIZED_NEWTON_DIRECTION_WITHIN_ACCEPTED_PROJECTED_CONSTRAINED_OUTER_FRAME`

Authority marker:

`DLH_5VY_ROUTE_A_ONE_STEP_PROJECTED_REGULARIZED_NEWTON_AUTHORIZED`

Initial authoritative activation comment:

`5714125203`

Final authoritative activation-refresh: **NOT YET PUBLISHED**. Until that
refresh confirms the post-sync live `main`, Builder execution on Issue #73 is
**NOT YET OPERATIVE** and no scientific source, test or report may be modified.

Dedicated future Builder branch:

`dsh/issue-73-dlh-5vy-one-step-projected-regularized-newton-2026-09-17`

Controlling accepted authority: Issue #72 / DLH-5V-X ACCEPTED / CLOSED at
Terminal B (accepted candidate / integration
`5d2f489f8dfb3527c0e4bd7dc418e35139b9dbd9`; reviewer acceptance `5714106614`;
acceptance integration `5714110964`; accepted selected-Q blob
`7857cabb4d28af99cb9d59e2d1c3024b05787c11`), whose frozen outer frame and ladders
Issue #73 now executes one step of.

### 8.16.1 Exact execution scope

This is a **bounded one-step scientific numerical execution** — the first Issue
authorized to take an actual numerical step since Issue #63. Exactly: ONE
deterministic reconstruction of the accepted `V_*` (reproducing steps `8`,
statistic `3.6614352438846254e-08`, min `p_b` `4.8089461301970005e-09`, wall
`F3 (13,13) z=1 node 332`, `||R||inf` `10.435094313164921`, argmax row `97` /
node `97` / z `0` / F0, Bellman tolerance `1e-3`); exactly ONE baseline Route-A
`final=False` selected-`Q` build; ONE baseline residual/Jacobian; ONE bounded
lexicographic candidate search; at most ONE accepted experimental candidate;
immediate STOP at the first acceptable candidate or fail-closed on
authorized-search exhaustion; ONE deterministic repeat; focused tests plus the
full repository suite.

**No second outer step. No trajectory. No HJB convergence claim.**

### 8.16.2 Selected direction and boundary handling

Policy-frozen Jacobian `J = rho I - Q` from the SAME frozen selected operator.
Regularized direction rungs
`(J + lambda_k*||diag(J)||inf I) d = -R` with `lambda_k = 2^-k`, `k = 0..20`; the
linear solve must be deterministic and finite and `||J_lambda d + R||inf` is
recorded. Boundary handling uses accepted full-wall-gradient semantics, detecting
every active positive-`p_b` constraint under the frozen Issue #72 tolerance and
**stacking multiple gradients, never averaging them**. Candidate-state domain
safety is authoritative: every trial must be finite with `min p_b >= 1e-12`.

### 8.16.3 Frozen attempt order and acceptance

Lexicographic: `k_lambda = 0..20`, then trust-radius fraction `2^-k_Delta` with
`k_Delta = 0..20`, then step fraction `alpha = 2^-k_alpha` with `k_alpha = 0..20`.
No outcome-driven tuning and no extra rung. The actual number of attempted
candidates is reported, and the search stops at the **first** candidate satisfying
every acceptance criterion.

Each candidate requires a **full reassembly** of the same Route-A selected
generator. Acceptance requires ALL of: finite; `min p_b(V_trial) >= 1e-12`;
`max|Q_trial 1|` within the accepted numerical conservativity scale; single-`Q`
contract passes; `||R_trial||inf < ||R||inf` by at least `1e-12` absolute; and the
frozen Armijo-style sufficient-decrease rule with coefficient `1e-4` and the
attempted `alpha`. The stronger historical `<= 0.5` material-reduction ratio must be
**reported** but is **not** required for one-step acceptance.

Any accepted state is an **Issue #73 experimental one-step candidate only** — not
an accepted HJB solution, and it does not authorize downstream use.

### 8.16.4 Builder allowlist (four new paths only)

1. `src/deep_learning_hank/two_asset/route_a_one_step_projected_regularized_newton.py`
2. `tests/test_dlh_5vy_route_a_one_step_projected_regularized_newton.py`
3. `reports/dlh_5vy_route_a_one_step_projected_regularized_newton_2026_09_17/DLH_5VY_ROUTE_A_ONE_STEP_PROJECTED_REGULARIZED_NEWTON_REPORT.md`
4. `reports/dlh_5vy_route_a_one_step_projected_regularized_newton_2026_09_17/DLH_5VY_ROUTE_A_ONE_STEP_PROJECTED_REGULARIZED_NEWTON_ATTEMPTS.csv`

**No fifth tracked Builder path.** All accepted Issue #60–#72
source/test/report/governance files remain read-only.

Exactly ONE terminal must be reported:

- A `DLH_5VY_ROUTE_A_ONE_STEP_PROJECTED_REGULARIZED_NEWTON__DOMAIN_SAFE_SINGLE_Q_RESIDUAL_REDUCING_CANDIDATE_ACCEPTED__TRAJECTORY_DESIGN_GATE_READY`
- B `DLH_5VY_ROUTE_A_ONE_STEP_PROJECTED_REGULARIZED_NEWTON__AUTHORIZED_SEARCH_EXHAUSTED_WITH_NO_ACCEPTABLE_STEP__DIRECTION_RECONSIDERATION_REQUIRED`
- C `DLH_5VY_ROUTE_A_ONE_STEP_PROJECTED_REGULARIZED_NEWTON__REPRODUCTION_LINEAR_SOLVE_DOMAIN_OR_SINGLE_Q_CONTRACT_FAILURE__SCIENTIFIC_REVIEW_REQUIRED`
- Blocked `BLOCKED_DLH_5VY_AUTHORITY_OR_DEPENDENCY_CONFLICT`

### 8.16.5 Forbidden

No mutation of selected-Q, the oracle, or any accepted Issue #60–#72 source; no
`final=False` / `final=True` semantics change; no policy-selection change; no
F1–F11 boundary-semantics change; no
economics/prices/grid/domain/initialization/calibration change; no
tolerances/`PB_MARGIN`/Bellman-tolerance change; no convergence-criterion change;
no use of the residual / Jacobi direction; no added or tuned ladder rungs; no
second outer step; no trajectory; no HJB convergence claim; no KFE / stationary
KFE / steady state; no SCC/global-Q / GE / multi-region / neural / nominal /
calibration / policy / welfare / Results; no PR; no merge; no Issue close; no
successor; no self-accept.

Stationary KFE remains **NOT AUTHORIZED**.

---

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
F0 final=True rate/provenance and operator-consistency audit          TERMINAL A ACCEPTED/CLOSED — ISSUE #66
minimal final-validation z-block operator repair                     TERMINAL A ACCEPTED/CLOSED — ISSUE #67 / DLH-5V-S
single-wall tangent-projected Newton geometry diagnostic             TERMINAL C ACCEPTED/CLOSED — ISSUE #68 / DLH-5V-T
latent F0 iteration-rate vs raw-drift sign-divergence provenance audit  TERMINAL A ACCEPTED/CLOSED — ISSUE #69 / DLH-5V-U
F0 rate semantics authority / operator contract                   RESOLVED — OWNER SELECTED ROUTE A (MATLAB-FAITHFUL SINGLE-Q AUTHORITATIVE)
Route-A single-Q F0 operator contract consolidation + revalidation   TERMINAL A ACCEPTED/CLOSED — ISSUE #70 / DLH-5V-V
Route-A single-Q residual source decomposition at V*               TERMINAL B ACCEPTED/CLOSED — ISSUE #71 / DLH-5V-W
Route-A bounded residual-balanced solver contract design           TERMINAL B ACCEPTED/CLOSED — ISSUE #72 / DLH-5V-X
Route-A one-step projected regularized-Newton execution at V*      NEXT ACTIVE (BUILDER NOT YET OPERATIVE) — ISSUE #73 / DLH-5V-Y
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

**ISSUE #73 / DLH-5V-Y IS NEXT ACTIVE — BUILDER NOT YET OPERATIVE.** Issue #72 /
DLH-5V-X is ACCEPTED / CLOSED at Terminal B and integrated to `main` at
`5d2f489f8dfb3527c0e4bd7dc418e35139b9dbd9` (reviewer acceptance `5714106614`;
acceptance integration `5714110964`; accepted selected-Q blob
`7857cabb4d28af99cb9d59e2d1c3024b05787c11`; accepted verdict
`DLH_5VX_ACCEPTED__TERMINAL_B_CONFIRMED__BOUNDED_SINGLE_Q_OUTER_FRAME_FROZEN__THREE_DIRECTION_FAMILIES_REMAIN_ADMISSIBLE_AT_FAMILY_LEVEL__PSEUDO_TIME_RESOLVENT_REFUTED__DIRECTION_SELECTION_GATE_REQUIRED`;
accepted terminal
`DLH_5VX_ROUTE_A_BOUNDED_SOLVER_DESIGN__MULTIPLE_PLAUSIBLE_ROUTES_REMAIN__OWNER_OR_REVIEWER_ROUTE_SELECTION_REQUIRED`).

Accepted Issue #72 facts: the constrained / projected residual-balanced outer frame
is frozen; pseudo-time / resolvent is refuted by accepted Issues #60 and #61;
admissible family-level directions include policy-frozen / regularized Newton,
residual / Jacobi preconditioned correction, and the constrained / projected outer
frame itself; every ladder and threshold is frozen exactly in-Issue with no
adaptive hedge language; deterministic repeat **TRUE**; consistency checks
**38/38**; focused suite **56 passed**; full clean-tree suite **749 passed**,
`0 failed`, `0 errors`, `6` pre-existing oracle warnings; no `V_new`; no executed
solver step; no accepted iterate. The accepted candidate is one remediation commit
atop original candidate `d06f53e4…` with cumulative diff exactly the four
Reviewer-authorized paths, no fifth, and no rebase.

Reviewer route selection made AFTER Issue #72 and activated in Issue #73:
`POLICY_FROZEN_REGULARIZED_NEWTON_DIRECTION_WITHIN_ACCEPTED_PROJECTED_CONSTRAINED_OUTER_FRAME`.
Basis: Issue #64 contains direct measured Newton-direction evidence and Issue #68
contains accepted full-wall projected geometry plus residual-reduction evidence on
the iteration operator, while the residual / Jacobi direction remains entirely
unmeasured. A bounded first-probe choice only — NOT a claim of global superiority
or convergence.

**OWNER SCIENTIFIC DECISION RESOLVED — ROUTE A SELECTED.** The Owner explicitly
selected Route A on 2026-09-15: MATLAB-faithful iteration-rate semantics remain
authoritative for the HJB operator. Binding single-`Q` contract: the solve, final
validation and any future authorized `Q^T` mass dynamics must share **one
coherent selected generator**; raw-drift `max(±mu)/step` is **not** an independent
final-validation `Q` authority; **dual-`Q` semantics are NOT AUTHORIZED**; Routes
B and C are not selected. Issue #70 realized this contract: the F0 `final=True`
assembly reuses the supplied selected record's `row_entries` / `diagonal` /
`utility` / controls / realized drifts / policy-sector label verbatim, with no
`INTERIOR_FINAL` retag and no second raw-drift F0 generator remaining.

Issue #69 evidence underlying the Owner gate remains the accepted attribution: both
Issue #68 trial disparities reproduce exactly (gaps `0.6718037653783657` on rows
`{452, 453}` and `1.3379411925537439` on rows `{452, 453, 482, 483}`); across all
`596` F0 rows the b-rate divergent counts are `2` / `4`, a-rate divergent
`0` / `0`, destination-layout and omitted-rate divergent `0` / `0`, max
decomposition residual `3.552713678800501e-15`; stored and recomputed realized
`mu_a` / `mu_b` bit-identical on affected rows; every affected row has realized
`mu_b < 0` so the raw-drift path has `b_forward = 0` while the iteration path
carries a positive `iteration_b_forward_rate`; iteration b-rates come from
branch-gated `sc_b`/`sc_f` + `sdh_b`/`sdh_f` FOC/shadow objects, corrected final
raw rates from `max(±mu_b)/db`; unique mechanism `liquid_label == "F"` /
branch-gated positive forward iteration component while realized `mu_b < 0`.
Reviewer qualification (binding): the acceptance is limited to attribution of the
observed Issue #68 trial discrepancies and does **not** adopt the broader claim
that the two rate constructions coincide *only* whenever `liquid_label == "0"` as
a global theorem.

**No HJB convergence** and **no accepted new HJB iterate**; the accepted residual
`10.435094313164921` remains ~`10435`× the unchanged Bellman tolerance `1e-3`.
Stationary KFE remains **NOT AUTHORIZED**.

Issue #73 / DLH-5V-Y is the **first execution Issue** since Issue #63: the frozen
Issue #72 outer frame is now executed for exactly **ONE** bounded step at `V_*`.

Route selection:
`POLICY_FROZEN_REGULARIZED_NEWTON_DIRECTION_WITHIN_ACCEPTED_PROJECTED_CONSTRAINED_OUTER_FRAME`.
Authority marker: `DLH_5VY_ROUTE_A_ONE_STEP_PROJECTED_REGULARIZED_NEWTON_AUTHORIZED`.
Initial authoritative activation comment: `5714125203`. Final authoritative
activation-refresh: **NOT YET PUBLISHED**, so Builder execution on Issue #73
remains **NOT YET OPERATIVE** until that refresh confirms the post-sync live
`main`, and no scientific source, test or report may be modified before then.

Dedicated future Builder branch:
`dsh/issue-73-dlh-5vy-one-step-projected-regularized-newton-2026-09-17`.

Task type:
`SCIENTIFIC_NUMERICAL_EXECUTION__ROUTE_A_SINGLE_Q_ONE_STEP_PROJECTED_REGULARIZED_NEWTON`.

Authorized work: ONE deterministic reconstruction of the accepted `V_*`
(reproducing steps `8`, statistic `3.6614352438846254e-08`, min `p_b`
`4.8089461301970005e-09`, wall `F3 (13,13) z=1 node 332`, `||R||inf`
`10.435094313164921`, argmax row `97` / node `97` / z `0` / F0, Bellman tolerance
`1e-3`); exactly ONE baseline Route-A `final=False` selected-`Q` build; ONE
baseline residual/Jacobian with `J = rho I - Q` from that SAME frozen operator;
ONE bounded lexicographic candidate search over `k_lambda`, `k_Delta`, `k_alpha`
each `0..20` using
`(J + lambda_k*||diag(J)||inf I) d = -R` with `lambda_k = 2^-k`; full-wall-gradient
boundary handling with multiple stacked active gradients (never averaged) and
candidate-state domain safety `min p_b >= 1e-12`; at most ONE accepted experimental
candidate; immediate STOP at the first acceptable candidate or fail-closed on
authorized-search exhaustion; ONE deterministic repeat; focused tests plus the full
repository suite.

Explicitly NOT authorized in Issue #73: mutating selected-Q, the oracle, or any
accepted Issue #60–#72 source; modifying `final=False` / `final=True` semantics;
modifying policy selection; modifying F1–F11 boundary semantics; economics /
prices / grid / domain / initialization / calibration / tolerances / `PB_MARGIN` /
Bellman-tolerance change; convergence-criterion change; using the residual /
Jacobi direction; adding or tuning ladder rungs; accepting a second outer step;
running a trajectory; claiming HJB convergence; KFE / stationary KFE / steady
state / `solve_household_steady_state`; SCC/global-Q;
GE/multi-region/neural/nominal/calibration/policy/welfare/Results; successor Issue
activation; any Builder scientific branch beyond the dedicated Issue #73 branch
(not yet created); PR / merge / Issue close / self-accept.

Issue #73 exact four-path Builder allowlist:
`src/deep_learning_hank/two_asset/route_a_one_step_projected_regularized_newton.py`;
`tests/test_dlh_5vy_route_a_one_step_projected_regularized_newton.py`;
`reports/dlh_5vy_route_a_one_step_projected_regularized_newton_2026_09_17/DLH_5VY_ROUTE_A_ONE_STEP_PROJECTED_REGULARIZED_NEWTON_REPORT.md`;
`reports/dlh_5vy_route_a_one_step_projected_regularized_newton_2026_09_17/DLH_5VY_ROUTE_A_ONE_STEP_PROJECTED_REGULARIZED_NEWTON_ATTEMPTS.csv`.
No fifth tracked Builder path.

Issue #73 terminal set (exactly ONE to be reported):
A `DLH_5VY_ROUTE_A_ONE_STEP_PROJECTED_REGULARIZED_NEWTON__DOMAIN_SAFE_SINGLE_Q_RESIDUAL_REDUCING_CANDIDATE_ACCEPTED__TRAJECTORY_DESIGN_GATE_READY`;
B `DLH_5VY_ROUTE_A_ONE_STEP_PROJECTED_REGULARIZED_NEWTON__AUTHORIZED_SEARCH_EXHAUSTED_WITH_NO_ACCEPTABLE_STEP__DIRECTION_RECONSIDERATION_REQUIRED`;
C `DLH_5VY_ROUTE_A_ONE_STEP_PROJECTED_REGULARIZED_NEWTON__REPRODUCTION_LINEAR_SOLVE_DOMAIN_OR_SINGLE_Q_CONTRACT_FAILURE__SCIENTIFIC_REVIEW_REQUIRED`;
Blocked `BLOCKED_DLH_5VY_AUTHORITY_OR_DEPENDENCY_CONFLICT`. Stationary KFE
remains **NOT AUTHORIZED**.

### 11.1 Superseded Issue #72 execution record

Dedicated Builder branch (integrated into `main`):
`dsh/issue-72-dlh-5vx-route-a-bounded-solver-design-2026-09-16`.

Task type:
`SCIENTIFIC_NUMERICAL_DESIGN__ROUTE_A_SINGLE_Q_BOUNDED_RESIDUAL_BALANCED_HJB_SOLVER_CONTRACT`.

Authorized work (**DESIGN ONLY**): ONE read-only synthesis of accepted Issues
#60–#71 evidence; ONE candidate-family comparison matrix over
policy-frozen/regularized Newton, residual/Jacobi preconditioned correction,
constrained/projected least-squares or trust-region correction, and
pseudo-time/resolvent continuation as historical baseline only; ONE selected
bounded solver contract or an explicit no-route conclusion; ONE deterministic
pseudocode/specification freezing every ladder and threshold in-Issue; ONE
deterministic internal consistency check; focused tests plus the full repository
suite. Measured and accepted: **Terminal B** — three families admissible, one
refuted, so no unique route could be certified; the direction-agnostic outer frame
is nevertheless fully frozen. No nonlinear trial state, no accepted iterate, no
trajectory. A bounded artifact-consistency remediation (Reviewer hold `5699275937`)
repaired a repeat-flag reporting-path defect structurally.

### 11.2 Superseded Issue #71 execution record

Dedicated Builder branch (integrated into `main`):
`dsh/issue-71-dlh-5vw-route-a-hjb-residual-decomposition-2026-09-16`.

Task type:
`SCIENTIFIC_NUMERICAL_DIAGNOSTIC__ROUTE_A_SINGLE_Q_HJB_RESIDUAL_SOURCE_DECOMPOSITION`.

Authorized work: read-only decomposition of the remaining Route-A single-`Q`
residual `R = rho*V - u - Q*V` at the ONE accepted `V_*` (reproduced exactly:
`8` steps, final statistic `3.6614352438846254e-08`, min boundary `p_b`
`4.8089461301970005e-09`, wall `F3 (13,13), z=1, node 332`, `||R||inf`
`10.435094313164921`, argmax row `97` / node `97` / z `0` / F0); exactly ONE
Route-A `final=False` operator build; additive per-state components (`rho*V`,
utility/source, z-switch, b-backward, b-forward, a-backward, a-forward,
diagonal, reconstructed residual, closure error); deterministic top-20 by `|R|`
with tie-break row id, each recording row/node/j/i/z/family, sector/liquid/transfer
labels where available, controls, realized drifts, stored iteration rates,
neighbours, additive components and residual sign/magnitude; read-only policy
reproduction audit on the top-20 F0 rows; ONE deterministic repeat; focused tests
plus the full repository suite. No new HJB iterate or trajectory. Measured and
accepted: Terminal B, with the residual a near-total cancellation
(mean top-20 ratio `0.006665998653866562`) and no unique dominant component.

### 11.3 Superseded Issue #70 execution record

Dedicated Builder branch (integrated into `main`):
`dsh/issue-70-dlh-5vv-route-a-single-q-operator-contract-2026-09-15`.

Task type:
`OWNER_AUTHORIZED_SCIENTIFIC_CHANGE__MATLAB_FAITHFUL_SINGLE_Q_F0_OPERATOR_CONTRACT_CONSOLIDATION_AND_REVALIDATION`.

Authorized work: ONE minimal source mutation implementing Route A in the F0
`final=True` validation assembly of
`src/deep_learning_hank/two_asset/boundary_hjb_selected_q.py` (the supplied
selected F0 record's stored `row_entries` / iteration rates / `diagonal` /
`utility` / policy-sector label directly define the final-validation row;
same-z-block destination indexing preserved; no second F0 `Q` from
`asset_drifts_matlab_faithful` + `max(±mu)/step`); ONE deterministic
reconstruction of `V_*` plus the accepted Issue #68 tangent direction; exactly
THREE frozen-state checks S0 = `V_*`, S1 = `alpha_half = 0.08085341880193442`,
S2 = `alpha_near = 0.16170683760386884` with no search and no alpha tuning; at
each state ONE `final=False` build and ONE Route-A `final=True` build under the
SAME records; ONE deterministic repeat; focused tests plus the full repository
suite. Measured and accepted: `Q_final == Q_iter` and `u_final == u_iter` exactly
`0.0` at all three states, the historical S1/S2 gaps collapsing to exactly `0.0`,
and the S0 residual remaining `10.435094313164921`. No new HJB iteration
trajectory. A bounded post-Route-A contract migration of ten authorized paths
(Reviewer hold `5690304999`) and a bounded policy-label remediation (Reviewer
final hold `5691015137`) followed.

### 11.4 Superseded Issue #69 execution record

Dedicated Builder branch (integrated into `main`):
`dsh/issue-69-dlh-5vu-f0-rate-path-divergence-2026-09-15`.

Task type:
`SCIENTIFIC_NUMERICAL_DIAGNOSTIC__F0_ITERATION_RATE_VS_RAW_DRIFT_SIGN_PROVENANCE_AWAY_FROM_VSTAR`.

Authorized work: ONE deterministic reconstruction of `V_*` plus the accepted
Issue #68 full-gradient tangent geometry; exactly TWO frozen trial states
(`alpha_half = 0.08085341880193442`, `alpha_near = 0.16170683760386884`) with no
third trial; at each trial exactly ONE `final=False` re-selection and ONE
corrected `final=True` same-control build; ONE all-F0 compact rate/row
decomposition per trial; ONE read-only source provenance mapping; ONE
deterministic repeat. Must reproduce the accepted Issue #68 gaps `0.6718037653783657`
(rows `{452, 453}`) and `1.3379411925537439` (rows `{452, 453, 482, 483}`), and
record the frozen flags `ITER_RATE_PATH_SOURCE_BACKED`,
`FINAL_RAW_PATH_SOURCE_BACKED`, `RATE_FORMULAS_GLOBALLY_EQUIVALENT`,
`SIGN_OR_BRANCH_DIVERGENCE_ESTABLISHED`,
`TRUNCATION_OR_DESTINATION_DIVERGENCE_ESTABLISHED`,
`OTHER_MECHANISM_ESTABLISHED`, `MIXED_OR_UNRESOLVED`.

Explicitly NOT authorized in Issue #69: mutating selected-Q, the oracle, or any
accepted Issue #61–#69 scientific source; choosing or replacing the
authoritative rate path; convergence-criterion change; economics / prices /
grid / domain / initialization / controls / tolerances / `PB_MARGIN` /
Bellman-tolerance change; accepting any trial as an HJB iterate; constructing a
new Newton / tangent / constrained direction; multi-step Newton / policy
iteration / semismooth / trust-region / continuation / line search; adding trial
states or alpha tuning; price / Wmax / resolution sweeps; KFE / stationary KFE /
`solve_household_steady_state`; SCC/global-Q;
GE/multi-region/neural/nominal/calibration/policy/welfare/Results; successor
Issue activation; any Builder scientific branch beyond the dedicated Issue #69
branch (not yet created); PR / merge / Issue close / self-accept. Pending the
Owner route decision it also forbids creating Issue #70 or any new Builder
branch.

Issue #69 exact four-path Builder allowlist:
`src/deep_learning_hank/two_asset/f0_rate_path_divergence_audit.py`;
`tests/test_dlh_5vu_f0_rate_path_divergence.py`;
`reports/dlh_5vu_f0_rate_path_divergence_2026_09_15/DLH_5VU_F0_RATE_PATH_DIVERGENCE_REPORT.md`;
`reports/dlh_5vu_f0_rate_path_divergence_2026_09_15/DLH_5VU_F0_RATE_PATH_DIVERGENCE_SUMMARY.csv`.
No fifth tracked Builder path.

Issue #69 terminal set (exactly ONE to be reported):
A `DLH_5VU_F0_RATE_PATH_DIVERGENCE__UNIQUE_SIGN_OR_BRANCH_MECHANISM_ESTABLISHED_AND_FULLY_ACCOUNTS_FOR_TRIAL_OPERATOR_GAPS__RATE_SEMANTICS_SCIENTIFIC_REVIEW_GATE_READY`;
B `DLH_5VU_F0_RATE_PATH_DIVERGENCE__UNIQUE_TRUNCATION_OR_DESTINATION_MECHANISM_ESTABLISHED_AND_FULLY_ACCOUNTS_FOR_TRIAL_OPERATOR_GAPS__RATE_SEMANTICS_SCIENTIFIC_REVIEW_GATE_READY`;
C `DLH_5VU_F0_RATE_PATH_DIVERGENCE__MIXED_OR_UNRESOLVED_SOURCE_PROVENANCE__OWNER_SCIENTIFIC_REVIEW_REQUIRED`;
Blocked `BLOCKED_DLH_5VU_AUTHORITY_OR_DEPENDENCY_CONFLICT`. Stationary KFE
remains **NOT AUTHORIZED**.

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

Issue #66 / DLH-5V-R execution is **complete and ACCEPTED / CLOSED at
Terminal A**: the audit deterministically reconstructed the accepted Issue #63
stagnation state `V_*` (final statistic ≈ `3.6614352438846254e-08`, min boundary
`p_b ≈ 4.8089461301970005e-09`, wall F3 (13,13), z=1), built the current-policy
`final=False` operator and the current-policy `final=True` operator exactly
once each at that same `V_*` with the SAME current selected F0 controls,
reproduced `||R_iter||_inf = 10.435094313164921`,
`||R_final_current||_inf = 490.7560414005864` and the F0 rowwise max
`|Q_final_current - Q_iter| = 24.601971766296664`, and performed the all-F0
compact row/rate/component comparison plus the read-only source-backed
MATLAB/oracle provenance mapping. Accepted facts: `ITER_EQ_MATLAB = true`,
`FINAL_EQ_MATLAB = false`, `BOTH_EQUIVALENT = false`,
`MIXED_OR_UNRESOLVED = false`; F0 directional rate formulas coincide within
machine tolerance; utility/source terms identical; non-F0 boundary rows
identical; **destination assembly is the material discrepancy** — 298 z=1 F0
rows affected; the accepted `final=True` F0 off-diagonal path uses bare `dn`
while the accepted iteration and boundary paths use `nz*n + dn`, therefore z=1
`final=True` F0 destinations are incorrectly placed in the z=0 block; no
conclusion yet that the convergence criterion itself should change; correction
of accepted `final=True` source semantics requires explicit Owner
authorization; `R_iter` is NOT declared an accepted final convergence residual.
The next route is `OWNER SCIENTIFIC DECISION REQUIRED — MINIMAL
FINAL-VALIDATION OPERATOR REPAIR`; the Owner granted that route decision on
2026-09-15 through Issue #67 / DLH-5V-S (initial authoritative activation
`5672573849`), which was the NEXT ACTIVE task at that time (Builder execution NOT
YET OPERATIVE pending the then-pending final authoritative activation-refresh;
Issue #67 is now ACCEPTED / CLOSED). Explicitly NOT
authorized in Issue #67: any second scientific source change,
`final=True` rate-formula change, convergence-criterion replacement, `R_iter`
becoming an accepted final convergence residual, any new HJB iterate, declaring
HJB convergence because the corrected residual drops, Newton / continuation /
line search, price / Wmax / resolution sweep, KFE / stationary KFE, and
successor Issue activation. Frozen accepted blob authority (oracle
`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`; selected-Q REPAIRED and accepted
`556ccc214f03a1a22306cc4f5c7e9f7691bbf897`, with the historical pre-repair blob
`7ea342ccbe15d852b90743b14bb4b02977c2d78b` retained as the accepted
Issue #64–#66 comparison authority; Issue #61
`043e146ef499e985a49d256c4cec2f397f93e4e1`; Issue #62
`cb6533475d0ba115e6f52bd73e61aeb85c9b6ea7`; Issue #63
`746799509c517746ba6a321e5526c57a8f4698e4`; Issue #64
`3ca2371c7da1939d1fed55df5728baefb27d8aa7`; Issue #65
`bb4045378bf19607f68d7d4a7628b3431afcd676`; Issue #66
`44d47c7545f279dfe9189736f5cdcdfa30c3b84b` — the latter seven remain strictly
read-only; selected-Q was the one accepted scientific source that Issue #70 /
DLH-5V-V was authorized to modify, and only within the F0 `final=True`
validation assembly; that change is now ACCEPTED / CLOSED with the accepted blob
`7857cabb4d28af99cb9d59e2d1c3024b05787c11` and the pre-Issue-70 blob
`556ccc214f03a1a22306cc4f5c7e9f7691bbf897` retained as the frozen comparison
authority; it is read-only for Issue #71 and every other Issue).
The accepted Issue #67 repair/migration paths, the accepted Issue #68
tangent-projected-Newton-geometry paths, the accepted Issue #69
rate-path-divergence-audit paths, the accepted Issue #70
operator-contract/migration paths, and the accepted Issue #71
residual-decomposition paths (the five Reviewer-authorized paths, hold
`5695153100`) are read-only evidence as well.
Stationary KFE remains **NOT
AUTHORIZED**; no successor; no PR / merge / Issue close / self-accept by the
Builder. Issue #71 / DLH-5V-W, Issue #70 / DLH-5V-V, Issue #69 / DLH-5V-U,
Issue #68 / DLH-5V-T,
Issue #67 / DLH-5V-S, Issue #66 / DLH-5V-R, Issue #65 / DLH-5V-Q, Issue #64 /
DLH-5V-P, Issue #63 / DLH-5V-O, Issue #62 / DLH-5V-N, Issue #61 / DLH-5V-M and
Issue #60 / DLH-5V-L
remain ACCEPTED / CLOSED; the seven tested stabilization/diagnostic route gates
plus the final-validation z-block validation-operator repair gate, the
single-wall tangent-projected Newton geometry gate, the F0 rate-path
divergence attribution gate, the Route-A single-`Q` F0 operator-contract
consolidation gate, the Route-A single-`Q` residual source-decomposition gate, and
the Route-A bounded residual-balanced solver-contract design gate are closed. The
Issue #69 Owner gate was **RESOLVED:
Route A selected** — MATLAB-faithful selected iteration-rate semantics are
authoritative for the HJB operator, the solve / final validation / future
authorized `Q^T` must share one coherent selected generator, raw-drift
`max(±mu)/step` is not an independent final-validation `Q` authority, and
dual-`Q` semantics are **NOT AUTHORIZED**. Issue #73 / DLH-5V-Y is NEXT ACTIVE
with Builder execution NOT YET OPERATIVE pending the final authoritative
activation-refresh.

Current governance pointers:

- `tasks/TASK_INDEX_CURRENT.md`
- `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
- Issue #73 body/comments (OPEN; initial authoritative activation `5714125203`;
  final authoritative activation-refresh not yet published).
- Issue #72 body/comments (accepted/closed; reviewer acceptance `5714106614`,
  acceptance integration `5714110964`).
- Issue #71 body/comments (accepted/closed; reviewer acceptance `5696620837`,
  acceptance integration `5696624495`).
- Issue #70 body/comments (accepted/closed; reviewer acceptance `5691693472`,
  acceptance integration `5691696204`).
- Issue #69 body/comments (accepted/closed; reviewer acceptance `5678488562`,
  acceptance integration `5678493024`).
- Issue #68 body/comments (accepted/closed; reviewer acceptance `5676811925`,
  acceptance integration `5676816068`).
- Issue #67 body/comments (accepted/closed; reviewer acceptance `5674741491`,
  acceptance integration `5674743972`).
- Issue #66 body/comments (accepted/closed; reviewer acceptance `5666168154`,
  acceptance integration `5666172248`).
- Issue #65 body/comments (accepted/closed).

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.