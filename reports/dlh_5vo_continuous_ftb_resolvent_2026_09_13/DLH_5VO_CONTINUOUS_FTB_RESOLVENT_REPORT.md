# DLH-5V-O — Continuous Fraction-to-Boundary Pseudo-Transient Continuation — Report

Issue #63 / DLH-5V-O — `SCIENTIFIC_NUMERICAL_DIAGNOSTIC__CONTINUOUS_FRACTION_TO_BOUNDARY_RESOLVENT_CONTINUATION`

Branch: `dsh/issue-63-dlh-5vo-continuous-ftb-resolvent-2026-09-13`

Authority: Issue #63 OPEN; initial activation `5652277509`; final
authoritative activation-refresh `5652449297` (post-sync live `main`
`9029e66dafa76f02cb2690c7e3152a2691350f61`). Route decision
`APPROVE_CONTINUOUS_FRACTION_TO_BOUNDARY_RESOLVENT_CONTINUATION_AFTER_5VN_OUTCOME_A`;
authority marker `DLH_5VO_CONTINUOUS_FTB_RESOLVENT_CONTINUATION_AUTHORIZED`.

## 1. Terminal (exactly ONE)

> **B — `DLH_5VO_CONTINUOUS_FTB_RESOLVENT__EFFECTIVE_DOMAIN_PRESERVED_BUT_VALIDATED_HJB_CONVERGENCE_NOT_REACHED`**

The continuous fraction-to-boundary pseudo-transient controller preserved the
effective domain at every accepted step and produced a deterministic,
reproducible trajectory of 8 accepted FTB-controlled steps on the frozen
central selected-Q case, but validated HJB convergence was NOT reached: the
accepted-step trigger (`max|V_{n+1}-V_n| < 1e-7`) fired on an asymptotically
shrinking step at iteration 8, and the final re-selection / Bellman validation
FAILED (final Bellman residual inf-norm = 490.76 >> 1e-3). Per Issue #63
section 7, a tiny step with a material residual is `FTB_STAGNATION`, not
convergence → Terminal B. No `FTB_STEP_CONSTRUCTION_FAILURE`, no non-finite
evidence, no domain breach (final min boundary p_b = 4.81e-9 > 1e-12), Q
conservative (max|Q·1| = 2.43e-12), 0 optimizer expansions / 0 artificial
bindings, deterministic repeat bit-identical.

## 2. Scientific interpretation (trajectory-bounded)

- The FTB controller is a well-defined fixed-point-preserving step rule:
  every accepted step solved `[I + delta(rho I - Q_n)] V(delta) = V_n +
  delta*u_n` with the frozen `(Q_n,u_n)` built exactly once per iterate, chose
  `delta_selected = (1 - EPS_FTB)*delta_ftb` at the root of
  `h_n(delta) = min_required_boundary p_b(V_n(delta)) - PB_MARGIN - RETAIN*m0`,
  and directly verified finite `p_b`, `min p_b > PB_MARGIN`, and retained
  margin `>= m_target`.
- The trajectory tracks the Issue #61/#62 local geometry exactly: the first
  step root `delta_ftb = 0.03179` (halving 15) sits in the Issue #61 feasible
  regime (accepted iter-1 delta k=15 = 0.03052), the second step root
  `0.00332` near Issue #61 iter-2 (k=18 = 0.00381), and subsequent steps decay
  by ≈ ×0.1 per iterate (`0.000345 → 3.49e-5 → 3.50e-6 → 3.51e-7 → 3.51e-8 →
  3.51e-9`) with the boundary margin decaying in lock-step
  (`4.81e-2 → 4.81e-3 → ... → 4.81e-9`), i.e. the trajectory crawls
  geometrically toward the boundary of the effective domain.
- The limiting state is F3 (13,13), z=1 (node 332) on every accepted step —
  the SAME wall state identified in Issues #61 and #62. The worst state at V0
  (node 377, F3 (17,8), z=1) is replaced after the first step.
- The raw fixed-point direction
  `max|u_n + Q_n V_n - rho V_n|` never decays (≈ 10.43-10.88 across all
  iterates; consistent with Issue #62 `dV/delta|_0` max abs 10.45): the step
  trigger fires on an asymptotically shrinking step that is NOT near the HJB
  fixed point (final Bellman residual 490.8). This is stagnation at the
  domain boundary, exactly the classification prescribed by Issue #63 section 7.
- Conclusion: the positive local safe radius established in Issue #62 does NOT
  extend to validated HJB convergence under this frozen controller on this
  frozen central case. This is trajectory-bounded evidence only: it does NOT
  prove global non-convergence of the FTB controller, does NOT prove the
  absence of another fixed-point-preserving route, and does NOT authorize KFE /
  stationary KFE.

## 3. Frozen central case and controller (unchanged, Issue #63 sections 3-5)

Exactly the accepted Issue #61/#62 central configuration and initialization
(`m=1, W_max=10, b_min=-2, a_max=10; r_a=0.07, r_b=0.02, w=1.00, gap=0;
rho=0.02, gamma_c=2, phi=5, chi_0=0.1, chi_1=2, a_bar=1e-6; tau=0.15;
z=[0.8,1.3]; tolerance_iter=1e-7, tolerance_Bellman=1e-3, max_iterations=1000;
n_c=n_d=9, bracket expansion x4 max 3; PB_MARGIN=1e-12`).

Controller constants frozen: `DELTA_CAP=1000`, `TAU_FTB=0.90`,
`RETAIN=1-TAU_FTB=0.10`, `EPS_FTB=1e-6`, `MAX_BRACKET_HALVINGS=60`.
Halving (`1000, 500, 250, ...`) was used ONLY to construct the first
sign-changing bracket for the continuous root solve — never accepted as a
ladder and never accepted merely because a probe was feasible
(0 cap-direct steps; every accepted step is a `(1-EPS_FTB)`-scaled continuous
root). Bellman residual was never used for step selection.

## 4. Per-iteration trace (authoritative run; full CSV in
`DLH_5VO_CONTINUATION_TRACE.csv`)

| iter | path | halv | delta_ftb | delta_selected | accepted stat | min p_b new | retained ratio | worst after | max\|Q·1\| | exp/ab | sector | dir norm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | root | 15 | 0.0317893 | 0.0317893 | 0.332664 | 0.0480769 | 1.000006 | F3 (13,13) z1 | 5.94e-15 | 0/0 | 0 | 10.8817 |
| 2 | root | 19 | 0.00331683 | 0.00331683 | 0.0346221 | 0.00480773 | 1.000008 | F3 (13,13) z1 | 5.94e-15 | 0/0 | 8 | 10.4664 |
| 3 | root | 22 | 0.000344912 | 0.000344911 | 0.00359930 | 0.000480777 | 1.000009 | F3 (13,13) z1 | 5.94e-15 | 0/0 | 0 | 10.4383 |
| 4 | root | 25 | 3.49012e-5 | 3.49012e-5 | 0.000364199 | 4.80781e-5 | 1.000009 | F3 (13,13) z1 | 9.49e-15 | 0/0 | 1 | 10.4354 |
| 5 | root | 29 | 3.50296e-6 | 3.50296e-6 | 3.65537e-5 | 4.80786e-6 | 1.000009 | F3 (13,13) z1 | 1.89e-14 | 0/0 | 0 | 10.4351 |
| 6 | root | 32 | 3.50703e-7 | 3.50703e-7 | 3.65962e-6 | 4.80791e-7 | 1.000009 | F3 (13,13) z1 | 7.58e-14 | 0/0 | 0 | 10.4351 |
| 7 | root | 35 | 3.50834e-8 | 3.50833e-8 | 3.66098e-7 | 4.80804e-8 | 1.000009 | F3 (13,13) z1 | 1.52e-13 | 0/0 | 0 | 10.4351 |
| 8 | root | 39 | 3.50877e-9 | 3.50877e-9 | **3.66144e-8** | 4.80895e-9 | 1.000001 | F3 (13,13) z1 | 6.06e-13 | 0/0 | 0 | 10.4351 |

Every row: `h(1000) ≈ -0.71` (cap never feasible), `cap_direct = false`,
retained margin `>= m_target` with ratio `≈ 1.000009` (root-interior factor
`1 - 1e-6`), bracket `[delta_lo, delta_hi]` genuine sign change (`h(lo) > 0`,
`h(hi) < 0`), accepted statistic decreasing ×0.1 per step.

## 5. Convergence trigger and final validation (iteration 8)

- accepted statistic at iter 8: `3.66144e-8 < 1e-7` → trigger fired;
- final re-selection / validation on final V:
  - final Bellman residual inf-norm `||rho V - [u_selected(V) +
    Q_selected(V) V]||_inf = 490.756 > 1e-3` → **FAIL**;
  - final min required boundary p_b = `4.80895e-9 > 1e-12` → PASS (domain
    preserved);
  - final max|Q·1| = `2.42534e-12 <= 1e-9` → PASS (conservative);
  - final artificial bindings = 0 → PASS;
- verdict: `FTB_STAGNATION` — the tiny accepted step is NOT validated
  convergence → **Terminal B**.

## 6. Execution design and reproducibility

Exactly ONE continuous FTB continuation run on the frozen central case + ONE
deterministic repeat of the same run (Issue #63 section 8). Both runs: 8
accepted iterations, identical outcome, identical trace, identical final
validation evidence (`deterministic_repeat_identical: true`). No second
controller parameter, no alternative `TAU_FTB`, no alternative cap, no price
case, no Wmax/resolution case.

Controller usage summary: 0 cap-direct steps, 8 root steps, min/median/max
selected delta `3.51e-9 / 1.92e-5 / 0.0318`, total halving probes 216.

## 7. Tests (all pass — 20/20)

`tests/test_dlh_5vo_continuous_ftb_resolvent.py`:
- frozen central configuration exact (economics / grid-domain / tolerances /
  control-search / PB_MARGIN / ladder floor);
- frozen controller constants exact (`TAU_FTB=0.90`, `RETAIN=0.10`,
  `DELTA_CAP=1000`, `EPS_FTB=1e-6`, `MAX_BRACKET_HALVINGS=60`);
- `(Q_n,u_n)` built exactly once per iterate and reused across all controller
  evaluations (runtime pin on a real iterate: exactly 1 build; full synthetic
  run: builds == accepted_iterations + 1 final);
- cap accepted directly when the target retained margin passes;
- halving is bracket construction only, not an accepted ladder (selected delta
  is the `(1-EPS_FTB)`-scaled continuous root, never a halving probe; genuine
  sign-changing bracket; bounded by `MAX_BRACKET_HALVINGS`; no bracket within
  the limit fails closed);
- bracketed root deterministic; selected delta equals `(1-EPS_FTB)*delta_ftb`
  on the root path;
- selected trial directly satisfies finite `p_b`, `p_b > PB_MARGIN`, retained
  margin `>= m_target`;
- synthetic sub-floor case consistent with Issue #62 geometry: the continuous
  root-derived step lies BELOW the old Issue #61 ladder floor `1000*2^-20`;
- non-finite boundary evidence fails closed (raises
  `FTBStepConstructionFailure`; a full run with non-finite evidence terminates
  at Terminal C, never feasible);
- step trigger cannot PASS without the final Bellman criterion (monkeypatched
  failing final validation → `FTB_STAGNATION` / Terminal B, not A);
- deterministic full repeat; max-iteration bounded non-convergence → Terminal B
  with domain preserved;
- scaled resolvent equals the accepted Issue #61 form for delta > 0 and
  `V(0) = V_n` at delta = 0;
- static integrity: no value damping, no `p_b` clip/floor, no Bellman-residual
  step selection, no delta ladder / `select_largest_feasible_delta`, no KFE /
  stationary KFE / steady state / `solve_household_steady_state`;
- real frozen central cross-checks: V0 min boundary p_b matches the accepted
  value `0.48076562156308306`; a real single FTB iterate constructs and
  verifies one step with Q conservative and 0/0 expansions/bindings.

## 8. Forbidden-operation check (all respected)

No mutation of the household oracle, selected-Q source, or Issue #61 / Issue #62
accepted implementations (all read-only imports; blobs unchanged); no
economics/prices/grid/domain/initialization/control-search/tolerances/
`PB_MARGIN`/controller-constant change; no value damping; no clip/floor/replace
of `p_b`; no Bellman-residual-based step selection; no price or Wmax/resolution
sweeps; no controller-parameter tuning after results; no KFE / stationary KFE /
`solve_household_steady_state`; no SCC/global-Q/GE/multi-region/neural/nominal/
calibration/policy/welfare/Results; no PR / merge / Issue close / successor /
self-accept.

## 9. Deliverables (exactly four new paths)

1. `src/deep_learning_hank/two_asset/continuous_ftb_resolvent_hjb.py`
2. `tests/test_dlh_5vo_continuous_ftb_resolvent.py`
3. `reports/dlh_5vo_continuous_ftb_resolvent_2026_09_13/DLH_5VO_CONTINUOUS_FTB_RESOLVENT_REPORT.md` (this file)
4. `reports/dlh_5vo_continuous_ftb_resolvent_2026_09_13/DLH_5VO_CONTINUATION_TRACE.csv`
