# DLH-5V-P — FTB Stagnation Residual Decomposition + Frozen-Policy Newton Boundary Geometry — Report

Issue #64 / DLH-5V-P — `SCIENTIFIC_NUMERICAL_DIAGNOSTIC__FTB_STAGNATION_RESIDUAL_DECOMPOSITION_AND_FROZEN_POLICY_NEWTON_GEOMETRY`

Branch: `dsh/issue-64-dlh-5vp-stagnation-newton-geometry-2026-09-13`

Authority: Issue #64 OPEN; initial activation `5652648524`; final authoritative
activation-refresh `5652783829` (post-sync live `main`
`7e82d606874d7b2347ba331678456b46529538c9`). Route decision
`APPROVE_FTB_STAGNATION_RESIDUAL_DECOMPOSITION_AND_FROZEN_POLICY_NEWTON_GEOMETRY_AFTER_5VO_TERMINAL_B`;
authority marker `DLH_5VP_STAGNATION_NEWTON_GEOMETRY_DIAGNOSTIC_AUTHORIZED`.

## 1. Terminal (exactly ONE)

> **B — `DLH_5VP_STAGNATION_NEWTON_GEOMETRY__POSITIVE_BOUNDARY_SAFE_NEWTON_STEP_BUT_NONLINEAR_RESIDUAL_REDUCTION_INSUFFICIENT__FURTHER_DIRECTION_DESIGN_REQUIRED`**

The frozen-policy Newton direction on the accepted Issue #63 stagnation state
is a genuine, boundary-safe direction (positive finite `alpha_cross ≈
1.8667e-4` with the SAME limiting wall state F3 (13,13), z=1 = node 332; exact
linear solve `||J_iter d_N + R_iter||_inf ≈ 6.96e-11`; both authorized trial
states strictly inside `PB_MARGIN`), but at the two authorized diagnostic
fractions the nonlinear re-selected residuals barely move: `ratio_iter ≈
0.9998-0.9999` and `ratio_final ≈ 0.9998-0.9999`, both far above the frozen
`MATERIAL_REDUCTION_RATIO = 0.50` dual criterion. → **Terminal B** (further
direction design required). Deterministic repeat bit-identical.

## 2. Answers to the two scientific questions

**Q1 (residual decomposition — why 490.756 vs 10.435?):** the gap is
**entirely driven by the F0 rows under the accepted final-validation
semantics**; boundary rows contribute zero. Boundary rows are built by the
same `_boundary_row` code in both semantics, so
`R_final - R_iter` is **exactly 0.0 on every boundary row**
(`||R_final - R_iter||_inf` = 488.0988429898615 with argmax F0 node 272
(10,5) z=1; F0-only max = 488.0988429898615; **boundary-only max = 0.0**).
`||R_final||_inf = 490.7560425919994` (reproduced exactly from the preserved
pre-step-8 F0 records) versus `||R_iter||_inf = 10.435094313164921`. The
final=True F0 rows (upwind `max(mu,0)/step` rates computed from the preserved
pre-step-8 records) evaluated at `V_*` produce a residual ~47× the iteration
scale at the same state. This is a semantics artifact of the final-validation
operator, not a boundary re-selection effect: the boundary-only contribution
is identical (`9.742068328671465`) in both operators.

**Q2 (is the Newton direction usable?):** the frozen-policy Newton direction
solves cleanly and is **boundary-safe but geometrically capped at a tiny
fraction**: `alpha_cross ≈ 1.8667e-4` (≈ 0.019% of a full Newton step), forced
by the wall state F3 (13,13), z=1 whose `p_b(V_*) ≈ 4.81e-9` sits only ≈ 4.8×
above the `PB_MARGIN = 1e-12` floor (86 of 186 required boundary states have
negative directional evidence; 40 are exactly-zero `i==0` V-independent
states). At the authorized `alpha_half` / `alpha_near` fractions the frozen
linear relation `R_iter(V_trial; frozen) = (1-alpha) R_iter(V_*)` holds to
`≤ 8.2e-11`, but one nonlinear re-selection at the trial changes the
iteration residual by only `≤ 0.02%` (`ratio_iter = 0.99981-0.99991`) and the
final-validation-style residual by `≤ 0.03%` (`ratio_final =
0.99976-0.99988`), with **0 sector switches**. The direction is therefore not
residual-reducing at any positive boundary-safe fraction: the obstruction is
neither pure boundary-normal unusability (Terminal C would require no positive
safe fraction) nor a material pseudo-time reduction (Terminal A) — it is a
boundary-capped Newton direction whose residual-reduction potential is
negligible at every domain-safe fraction → **Terminal B**.

## 3. Frozen central case and constants (unchanged, Issue #63 / #64)

Exactly the accepted Issue #61/#62/#63 central configuration and
initialization (`m=1, W_max=10, b_min=-2, a_max=10; r_a=0.07, r_b=0.02, w=1.00,
gap=0; rho=0.02, gamma_c=2, phi=5, chi_0=0.1, chi_1=2, a_bar=1e-6; tau=0.15;
z=[0.8,1.3]`). Frozen diagnostic constants (Issue #64 section 6):

```text
PB_MARGIN = 1e-12
EPS_ALPHA = 1e-6
HALF_ALPHA = 0.5
MATERIAL_REDUCTION_RATIO = 0.50
```

Deterministic fractions: `alpha_cross_i = (p_b(V_*) - PB_MARGIN)/(-dp_b(d_N))`
over required states with `dp_b(d_N) < 0`; `alpha_cross = min` positive finite;
`alpha_near = min(1, (1-EPS_ALPHA)*alpha_cross)`; `alpha_half = 0.5*alpha_near`.
No line search, no alpha tuning, no material-threshold tuning. Diagnostic trial
states are NOT accepted HJB iterates. Stationary KFE remains **NOT
AUTHORIZED**.

Read-only frozen blobs (verified unchanged at execution time):
household oracle `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`; selected-Q
`7ea342ccbe15d852b90743b14bb4b02977c2d78b`; Issue #61 implementation
`043e146ef499e985a49d256c4cec2f397f93e4e1`; Issue #62 local-geometry
implementation `cb6533475d0ba115e6f52bd73e61aeb85c9b6ea7`; Issue #63
implementation `746799509c517746ba6a321e5526c57a8f4698e4`.

## 4. Frozen state reconstruction (Issue #63 terminal, reproduced exactly)

Deterministic replay of the accepted Issue #63 trajectory, STOP immediately
after accepted FTB step 8, before any new HJB iterate is accepted. The
reconstructed trace is bit-identical to the accepted
`DLH_5VO_CONTINUATION_TRACE.csv` (8 root-controlled steps; full CSV in
`DLH_5VP_NEWTON_GEOMETRY_SUMMARY.csv`):

| iter | path | halv | delta_ftb | delta_selected | accepted stat | min p_b new | worst after | sector Δ | dir norm |
|---|---|---|---|---|---|---|---|---|---|
| 1 | root | 15 | 0.0317893 | 0.0317893 | 0.332664 | 0.0480769 | F3 (13,13) z1 | 0 | 10.8817 |
| 2 | root | 19 | 0.00331683 | 0.00331683 | 0.0346221 | 0.00480773 | F3 (13,13) z1 | 8 | 10.4664 |
| 3 | root | 22 | 0.000344912 | 0.000344911 | 0.00359930 | 0.000480777 | F3 (13,13) z1 | 0 | 10.4383 |
| 4 | root | 25 | 3.49012e-5 | 3.49012e-5 | 0.000364199 | 4.80781e-5 | F3 (13,13) z1 | 1 | 10.4354 |
| 5 | root | 29 | 3.50296e-6 | 3.50296e-6 | 3.65537e-5 | 4.80786e-6 | F3 (13,13) z1 | 0 | 10.4351 |
| 6 | root | 32 | 3.50703e-7 | 3.50703e-7 | 3.65962e-6 | 4.80791e-7 | F3 (13,13) z1 | 0 | 10.4351 |
| 7 | root | 35 | 3.50834e-8 | 3.50833e-8 | 3.66098e-7 | 4.80804e-8 | F3 (13,13) z1 | 0 | 10.4351 |
| 8 | root | 39 | 3.50877e-9 | 3.50877e-9 | **3.66144e-8** | 4.80895e-9 | F3 (13,13) z1 | 0 | 10.4351 |

Reproduced accepted terminal evidence:
- final step statistic = `3.6614352438846254e-08` (< `1e-7` step trigger);
- final min boundary `p_b(V_*) = 4.8089461301970005e-09` (> `1e-12`);
- wall state `V_*` = node 332, **F3 (13,13), z=1** (same as every accepted
  step, same as Issues #61/#62/#63);
- final accepted validation residual (accepted Issue #63 final-validation
  semantics, `final=True` with the preserved pre-step-8 F0 records) =
  `490.7560425919994` — reproduced exactly;
- `max|Q·1| = 2.4253377084448857e-12` (conservative) in both operators, 0
  optimizer expansions, 0 artificial bindings;
- `V_0` min boundary p_b = `0.48076562156308306` (reproduced).

## 5. Residual / operator decomposition at `V_*`

Built exactly once per semantics (Issue #64 section 4):

```text
Q_iter, u_iter : accepted final=False semantics, built EXACTLY ONCE
R_iter  = rho*V_* - [u_iter  + Q_iter  V_*]
Q_final,u_final: accepted Issue #63 final-validation semantics
                 (final=True with preserved pre-step-8 F0 records)
R_final = rho*V_* - [u_final + Q_final V_*]
```

| measure | R_iter | R_final | R_final − R_iter |
|---|---|---|---|
| total ‖·‖∞ | 10.435094313164921 | 490.7560425919994 | 488.0988429898615 |
| argmax state | F0 node 97 (3,2) z=0 | F0 node 272 (10,5) z=1 | F0 node 272 (10,5) z=1 |
| F0-only max | 10.435094313164921 | 490.7560425919994 | 488.0988429898615 |
| F0 argmax | node 97 (3,2) z=0 | node 272 (10,5) z=1 | node 272 (10,5) z=1 |
| boundary-only max | 9.742068328671465 | 9.742068328671465 | **0.0** |
| boundary argmax | F10 node 0 (0,0) z=0 | F10 node 0 (0,0) z=0 | — |

Operator diagnostics: `max|Q_iter·1| = 2.4253377084448857e-12`,
`max|Q_final·1| = 2.4253377084448857e-12` (both conservative, ≤ `1e-9`);
expansions / artificial bindings = 0 / 0 for both builds.

**Decomposition verdict:** the `490.756` final-validation residual is
dominated by the **F0 final semantics** (upwind F0 rows from the preserved
pre-step-8 records); the **boundary contribution is identical in both
operators** (`R_final - R_iter` is exactly 0 on every non-F0 row). Neither
residual is ever reinterpreted as the other.

## 6. Exactly ONE frozen-policy Newton direction

```text
J_iter = rho I - Q_iter          (frozen iteration operator)
J_iter d_N = -R_iter             (exact Newton step, frozen linear operator)
```

- `||d_N||_inf = 19.725548329099023`;
- linear solve residual `||J_iter d_N + R_iter||_inf = 6.957900922088811e-11`
  ≤ declared `NEWTON_SOLVE_TOL = 1e-8` → PASS (finite, deterministic);
- this is a single linear solve on the frozen operator — NOT a nonlinear
  Newton theorem, no iteration, no multi-step Newton / policy-iteration /
  semismooth / trust-region solver.

## 7. ONE boundary-crossing calculation (accepted Issue #62 semantics)

- required boundary states = 186 (non-F0 × z), finite required `p_b` verified;
- negative-direction states with `dp_b(d_N) < 0` = **86**;
- exactly-zero `i==0` V-independent states = **40** (directional derivative
  exactly 0 by the accepted rule);
- `alpha_cross = 1.866738489296687e-4` at limiting state **node 332, F3
  (13,13), z=1** — the SAME wall state as the trajectory limiting state;
- `alpha_near = min(1, (1-1e-6)·alpha_cross) = 1.8667366225581976e-4`;
- `alpha_half = 0.5·alpha_near = 9.333683112790988e-5`;
- 86 positive finite crossings (all negative-direction states are
  finite-positive).

## 8. Exactly TWO diagnostic trial fractions (one evaluation each)

For `alpha ∈ {alpha_half, alpha_near}`: `V_trial = V_* + alpha·d_N`; all
required boundary `p_b` finite and `> PB_MARGIN` (fail-closed); frozen
residual verified `R_iter(V_trial; frozen) = (1-alpha)·R_iter(V_*)`; exactly
ONE `final=False` nonlinear re-selection (`R_reselect`); final-validation-style
residual at the same trial with the TRIAL re-selected records as the F0 input
(`R_final_trial`).

| quantity | alpha_half | alpha_near |
|---|---|---|
| alpha | 9.333683112790988e-05 | 1.8667366225581976e-04 |
| trial min boundary p_b | 2.4049648621777516e-09 | 1.002880318472827e-12 |
| trial limiting state | F3 (13,13) z=1 (node 332) | F3 (13,13) z=1 (node 332) |
| domain-safe (all p_b > PB_MARGIN) | true | true |
| frozen |dev| max | 8.169642740085692e-11 | 6.943778885215579e-11 |
| frozen rel |dev| max | 1.0484364359930044e-11 | 8.912005882894363e-12 |
| ‖R_reselect‖∞ | 10.434120336973693 | 10.433146365670952 |
| **ratio_iter** = ‖R_reselect‖∞/‖R_iter‖∞ | 0.9999066634031282 | 0.9998133272747223 |
| ‖R_final_trial‖∞ | 490.69670132317856 | 490.6373628129756 |
| **ratio_final** = ‖R_final_trial‖∞/‖R_final‖∞ | 0.9998790819395571 | 0.9997581695002735 |
| sector switches vs `V_*` iteration records | 0 | 0 |
| artificial bindings / expansions | 0 / 0 | 0 / 0 |
| max\|Q·1\| (trial re-selection) | 2.4253377084448857e-12 | 1.5522044760629683e-10 |
| **material reduction** (BOTH ≤ 0.50) | **false** | **false** |

Material reduction requires BOTH `ratio_iter ≤ 0.50` AND
`ratio_final ≤ 0.50` (frozen ex ante diagnostic threshold). Both trials fail
by ~0.50 (ratios ≈ 0.9998-0.9999) → `material_reduction_any = false`.

## 9. Execution design, determinism, and forbidden-operation check

- exactly ONE deterministic reconstruction + ONE decomposition + ONE Newton
  direction + ONE boundary-crossing calculation + exactly TWO trial fractions
  + ONE deterministic repeat of the full diagnostic;
- deterministic repeat **bit-identical** (`deterministic_repeat_identical =
  true`: trace, all residuals, Newton solve, crossing, both trials);
- trial states were diagnostic only — no trial was accepted as a new HJB
  iterate;
- no multi-step Newton / policy-iteration / semismooth / trust-region solver,
  no adaptive line search, no alpha / material-threshold tuning (verified
  statically and by construction);
- no economics / prices / grid / domain / `PB_MARGIN` change; no Issue #63
  controller change; no clip/floor of `p_b`; no price / Wmax / resolution
  sweep; no KFE / stationary KFE / steady-state invocation;
- the household oracle, selected-Q source and the Issue #61 / #62 / #63
  implementations were imported read-only and are unchanged (five frozen
  blobs verified);
- builder allowlist respected: exactly the four Issue #64 paths
  (`stagnation_newton_geometry.py`, its test, this report, and the summary
  CSV); no fifth tracked path;
- non-finite / inconsistent evidence fails closed (`NewtonGeometryFailure`
  → Terminal C); no such failure occurred.

## 10. Boundary-limited interpretation (trajectory-bounded)

This is local evidence at the single accepted Issue #63 stagnation state with
the frozen central selected-Q case. It does NOT prove that every
frozen-policy Newton-like direction fails globally, does NOT prove the
absence of a better direction/operator (e.g., a direction less boundary-capped
or a trust-region design that stays inside the effective domain), does NOT
prove the HJB fixed point does not exist, and does NOT authorize KFE /
stationary KFE. Terminal B records that a boundary-safe frozen-policy Newton
step exists but its authorized nonlinear residual reduction is insufficient —
further direction design is required.
