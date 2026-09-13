# DLH-5V-N — Local Continuous Resolvent / Domain-Margin Geometry Diagnostic — Report

Issue #62 / DLH-5V-N — `SCIENTIFIC_NUMERICAL_DIAGNOSTIC__LOCAL_CONTINUOUS_RESOLVENT_DOMAIN_GEOMETRY`

Branch: `dsh/issue-62-dlh-5vn-local-resolvent-geometry-2026-09-13`

Authority: initial activation `5651730413`; final authoritative activation-refresh `5651801939`; live `main` at activation `68ddc2b08132c7b95ecd15168be824d91738b938`.

## 1. Terminal (exactly ONE)

> **A — `DLH_5VN_LOCAL_RESOLVENT_GEOMETRY__POSITIVE_SUBFLOOR_SAFE_STEP_AND_REPRODUCIBLE_MARGIN_CROSSING__CONTINUATION_DESIGN_GATE_READY`**

**Issue #61 exhausted its authorized discrete ladder floor, not its operator:**
below the Issue #61 floor `1000·2^-20 ≈ 9.54e-4`, the frozen selected-Q resolvent
possesses a strictly positive local effective-domain-safe continuous delta
(verified directly feasible at `delta_below ≈ 7.8246e-4`), and the global boundary
margin crossing is reproduced deterministically inside the fixed bracket
`[0, 1000·2^-20]` at `delta_cross ≈ 7.8246e-4` (82.0% of the old floor), with the
first-order prediction within 3.0% of the nonlinear root.

Interpretation (trajectory-bounded and local only):

- the frozen terminal state/operator (Issue #61 last accepted state `V_*`,
  `Q_*`, `u_*`) is reproduced exactly (2 accepted updates; min boundary
  `p_b(V_*) = 0.009853744163134845` at F3 (13,13), z=1);
- local direction evidence is finite and non-trivial
  (`dV/delta|_0` max abs 10.45; most negative `dp_b/delta|_0 = −22.50` at
  node 332 z=0; 105 of 186 required boundary states have negative direction);
- the minimum positive finite first-order prediction is
  `delta_margin_linear = 7.5943e-4` at F3 (13,13), z=1 — the SAME wall state;
- the deterministic bracketed root `delta_cross = 7.8246e-4` lies strictly
  inside `(0, 1000·2^-20)`; the worst boundary state at the root and at the
  `(1±1e-6)·delta_cross` verification points is the SAME wall state
  F3 (13,13), z=1 (no state switching near the crossing);
- `delta_below` is directly verified feasible (`g = +9.56e-9 > 0`, min p_b =
  9.56e-9 > 1e-12) and `delta_above` infeasible (`g = −9.56e-9 < 0`);
- `delta_cross/(1000·2^-20) = 0.8205`; `delta_cross/delta_margin_linear = 1.0303`;
- the deterministic repeat is bit-identical.

Outcome A means the Issue #61 terminal event was **ladder-floor exhaustion**:
the authorized discrete ladder simply stopped above the local crossing. It does
NOT validate arbitrary continuation: the crossing is a reproducible
sign-changing crossing of the global boundary margin on the frozen local
operator — NOT a claim of global uniqueness, of the first positive crossing
over all positive delta, or of a viable next HJB iterate. A next-iterate /
continuation design remains a separate, NOT YET AUTHORIZED question.

> **R1 repair record (Reviewer `5652072976`):** bounded implementation/
> evidence repair on the same branch, no change to the frozen experiment or
> the Terminal-A crossing result.
>
> 1. **Real b=b_min face directional derivative.** The accepted
>    `compute_derivatives` map is NOT globally linear in V: at `i == 0` it
>    overwrites `vb_b` with the V-independent resource marginal
>    `resources**(-gamma_c)`. The directional diagnostic previously read
>    `compute_derivatives(dV, ...).vb_b` directly, which returned that positive
>    constant instead of the true directional derivative (exactly 0). Now
>    `boundary_direction_matrix` constructs `dp_b/delta|_0` per the accepted
>    semantics: backward finite-difference of `dV` for regular states
>    (identical to the accepted `vb_b` linear difference), and **exactly 0** on
>    the accepted V-independent boundary rule (`i == 0`). The accepted
>    selected-Q source is NOT modified. Focused regression tests prove on a
>    real `i == 0` required state that `p_b` is V-independent (exact under a
>    perturbation) and its directional derivative is exactly 0, while the
>    regular finite-difference path is unchanged.
> 2. **Non-finite crossing evidence fails closed.** `g_delta` previously
>    returned `+inf` for non-finite required boundary evidence, which would be
>    misread as `g > 0` (feasible) if it reached the feasibility path. Now
>    non-finite required boundary evidence in `g_delta` / the crossing path
>    RAISES `LocalGeometryFailure` (surfaced explicitly); the root, below-root
>    and above-root state recordings also guard on finiteness. Regression test:
>    a non-finite trial raises and can never be classified as below-root
>    feasible / Outcome A.
>
> Corrected directional evidence (all headline numbers unchanged): 105/186
> negative/required boundary states; most negative `dp_b/delta|_0 = −22.5000582300`
> at node 332, F3 (13,13), z=0; `dpb_zero_count = 40` (20 required `i == 0`
> nodes × 2 z, V-independent, exactly 0); min first-order prediction
> `delta_margin_linear = 7.5943e-4` at F3 (13,13), z=1. Crossing/root/
> below-above evidence and Terminal A are unchanged and bit-identical on the
> deterministic repeat. Tests now 24/24.

## 2. Authority and scope record

- Fresh live `main` at execution: `68ddc2b08132c7b95ecd15168be824d91738b938` (unchanged during execution).
- Issue #62 OPEN; initial activation `5651730413`; final authoritative activation-refresh `5651801939`; CURRENT governance synchronized to Issue #62.
- Household oracle blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e` — read-only, unchanged.
- Selected-Q blob `7ea342ccbe15d852b90743b14bb4b02977c2d78b` — read-only, unchanged.
- Accepted Issue #61 implementation blob `043e146ef499e985a49d256c4cec2f397f93e4e1` — read-only evidence (imported, never modified).
- Stationary KFE remains **NOT AUTHORIZED**.

## 3. Frozen central case and terminal-state provenance

Exactly the accepted Issue #61 frozen central configuration and initialization:
`m=1, W_max=10, b_min=-2, a_max=10; r_a=0.07, r_b=0.02, w=1.00, gap=0;
rho=0.02, gamma_c=2, phi=5, chi_0=0.1, chi_1=2, a_bar=1e-6; tau=0.15,
migration cost 0, labor weight 1; z=[0.8,1.3] + accepted switch; n_c=n_d=9,
bracket expansion x4 max 3; PB_MARGIN=1e-12`.

Reconstruction: the accepted Issue #61 trajectory is reconstructed
deterministically (same solver path, same operator-build-once-per-iterate rule,
same largest-feasible-delta selection) and STOPPED at the last accepted state
after exactly 2 accepted updates — the third update request is NOT executed as
an iterate (it is measured here only through the frozen operator diagnostics).

| iter | k | selected delta | accepted max\|ΔV\| | ref1000 max\|ΔV\| | ref1000 min p_b | min p_b old | min p_b new | delta1000 viol. | max\|Q·1\| | exp | ab | sector chg |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 15 | 0.0305176 | 0.319784 | 19.5763 | −0.68200 | 0.480766 | 0.060255 | true | 5.94e-15 | 0 | 0 | 0 |
| 2 | 18 | 0.00381470 | 0.039856 | 19.1616 | −0.73119 | 0.060255 | 0.009854 | true | 5.94e-15 | 0 | 0 | 7 |

Reproduced exactly: `V0` min boundary p_b = +0.48076562156308306; accepted
iterates k=15 then k=18; min accepted boundary p_b = **0.009853744163134845**;
ref1000 statistics 19.5763/19.1616 with ref1000 min p_b −0.6820/−0.7312;
Q conservative (max\|Q·1\| = 5.94e-15); 0/0 optimizer expansions/artificial
bindings; sector changes 0/7. Terminal state: **node 332, F3 (13,13), z=1**
with min boundary p_b = 0.009853744163134845 (identical to the accepted
Issue #61 terminal evidence).

## 4. Frozen operator (built EXACTLY ONCE)

At the frozen `V_*` the accepted selected policy / utility / conservative
backward `Q_*` and `u_*` are built exactly once
(`build_operator_and_u(V_*, labor0, 0, 0, final=False)`) and reused for every
local delta evaluation — no policy re-selection as delta varies (pinned by
test: exactly 2 reconstruction builds + exactly 1 frozen build; zero builds
during the whole root evaluation phase).

- `max|Q_* · 1| = 5.9396931817445875e-15` (conservative within accepted tolerance);
- optimizer expansions 0; artificial bindings 0;
- `rho = 0.02`; `V_*` (782-vector) frozen.

Equivalent continuous resolvent (well-defined at delta = 0):

```text
[I + delta*(rho I - Q_*)] V(delta) = V_* + delta*u_*       V(0) = V_*
```

Algebraically identical for every positive delta to the Issue #61 form
`[(1/delta + rho)I - Q_*] V(delta) = u_* + V_*/delta` (agreement pinned by
test at representative positive deltas; `V(0) = V_*` within 1e-12).

## 5. Local infinitesimal-direction diagnostic

```text
dV/delta|_0 = u_* + Q_* V_* - rho V_*
```

- max abs direction = 10.4479344678 (finite; residual direction is material);
- pinned by test against the closed form and against a small finite-difference
  check (h = 1e-6, relative agreement 1e-4).

## 6. Boundary dp_b/delta|_0 diagnostic and first-order margin prediction

Directional derivatives are constructed per the ACCEPTED derivative semantics
(selected-Q source not modified): regular backward finite-difference states use
the linear difference of `dV` (identical to the accepted `vb_b` difference of
`dV`); the accepted V-independent boundary rule at the b_min face (`i == 0`,
`vb_b = resources**(-gamma_c)`) has directional derivative **exactly 0**
(corrected in R1).

- required (non-F0) boundary states: **186**;
- V-independent (`i == 0`) required states: **40** (20 nodes × 2 z), all with
  `dp_b/delta|_0 = 0` exactly (pinned by test: `p_b` unchanged under a V
  perturbation);
- states with negative directional derivative: **105** (all finite);
- most negative finite `dp_b/delta|_0 = −22.5000582300` at **node 332,
  F3 (13,13), z=0** (distinct quantity from the crossing state, recorded
  separately);
- minimum positive finite first-order prediction:
  **`delta_margin_linear = 7.5943e-4` at node 332, F3 (13,13), z=1** — the
  SAME wall state as the terminal minimum p_b (its p_b is small, 0.00985, so it
  crosses first even though the steepest slope is at z=0);
- 105 finite positive predictions (one per negative-direction state);
- non-finite required boundary p_b or non-finite directional evidence fails
  closed (raised as `LocalGeometryFailure` and surfaced; pinned by test).

The linear prediction is a local diagnostic only, not a theorem of the
nonlinear continuous-delta path.

## 7. Continuous crossing diagnostic (fixed bracket [0, 1000·2^-20])

```text
g(delta) = min_required_boundary p_b(V(delta)) - PB_MARGIN
```

| quantity | value |
|---|---|
| g(0) | **+0.009853744162134845** (> 0; reproduces accepted terminal evidence) |
| g(1000·2^-20) | **−0.002078969754188379** (< 0; reproduces the accepted smallest-authorized-delta failure min p_b −0.002078969753188379) |
| bracket | [0, 0.00095367431640625] |
| delta_cross (brentq) | **0.0007824635781511621** (strictly inside bracket) |
| g(delta_cross) | −1.6406e-14 (≈ 0) |
| worst state at root | node 332, F3 (13,13), z=1 (wall state) |
| delta_below = (1−1e-6)·delta_cross | 0.0007824627956875839 → g = **+9.5629e-9 > 0** (min p_b = 9.5639e-9 > 1e-12) → **directly verified feasible** |
| delta_above = (1+1e-6)·delta_cross | 0.0007824643606147402 → g = **−9.5628e-9 < 0** → infeasible |
| worst state below / above | F3 (13,13), z=1 at both (no state switching) |
| ratio delta_cross / (1000·2^-20) | **0.8204725289** |
| ratio delta_cross / delta_margin_linear | **1.0303335349** (first-order prediction qualitatively reliable) |

The root solve is measurement of local geometry — NOT an extension of the
Issue #61 delta ladder and NOT a new HJB iteration.

## 8. Scientific interpretation (trajectory-bounded, local)

- The frozen terminal state/operator of Issue #61 is reproduced; the local
  operator geometry is finite and consistent (Q conservative 5.94e-15;
  0/0 expansions/bindings).
- A **strictly positive sub-floor safe delta exists** (`delta_below = 7.8246e-4
  < 1000·2^-20`, directly verified feasible) and the **global boundary margin
  crossing is deterministic and reproducible** at `delta_cross = 7.8246e-4`
  inside the fixed bracket, at the same wall state F3 (13,13), z=1 with no
  state switching near the crossing.
- **Conclusion: Issue #61's terminal event was ladder-floor exhaustion** — the
  authorized discrete ladder {1000·2^-k, k=0..20} simply stopped above the
  local crossing (its floor is 1.22× the crossing). This is NOT a local
  operator/domain pathology: the frozen resolvent direction is finite and a
  smaller continuous delta is locally feasible.
- Does NOT establish: global uniqueness or the first positive crossing over
  all delta > 0; viability of any next HJB iterate (a next-iterate or
  continuation design is a separate question, NOT YET AUTHORIZED); anything
  beyond the single frozen state/operator.

## 9. Tests (all pass — 24/24, incl. R1 regression tests)

`tests/test_dlh_5vn_local_resolvent_geometry.py`:
- frozen central configuration exact (params/inputs/z/switch/m/W/b_min/a_max/
  delta/tolerances/max_iterations/n_c=n_d=9/PB_MARGIN/ladder floor);
- reconstruction reproduces the accepted Issue #61 2-iterate trace exactly
  (k=15/k=18, statistics, ref1000 statistics, ref1000 min p_b, min p_b old/new,
  delta1000 violations, max\|Q·1\|, expansions/bindings, sector changes,
  V0 min p_b, min accepted p_b);
- full diagnostic reproduces the terminal state (node 332, F3 (13,13), z=1)
  and the accepted g(0) / g(floor) evidence;
- `(Q_*, u_*)` built exactly once and reused for every local delta evaluation
  (runtime pin: 2 reconstruction builds + 1 frozen build; ZERO builds during
  the crossing phase);
- scaled resolvent at delta=0 returns `V_*` within 1e-12;
- scaled and original positive-delta resolvent forms agree (< 1e-10) at
  representative deltas;
- infinitesimal direction equals `u_* + Q_*V_* − rho V_*` and matches a
  small finite-difference check within 1e-4 relative;
- R1: real `i == 0` required boundary state is V-independent (p_b exact under
  a perturbation) and its directional derivative is exactly 0;
  `dpb_zero_count` matches the V-independent states; the regular
  finite-difference directional path is unchanged;
- R1: non-finite required boundary p_b / directional evidence fails closed —
  `g_delta` RAISES `LocalGeometryFailure` (never returns `+inf` misread as
  feasible) and a non-finite trial in the crossing path is explicitly rejected
  (never below-root feasible / Outcome A);
- g(0) > 0 and g(1000·2^-20) < 0 reproduce accepted evidence;
- bracketed root deterministic, strictly inside the fixed bracket, below-root
  feasible / above-root infeasible (real and synthetic; synthetic crossing at
  a non-`i == 0` state);
- worst state at root / below / above = the same wall state F3 (13,13), z=1
  (no policy re-selection, no state switching near the crossing);
- static integrity: no unbounded loop / continuation / next-iterate logic;
  no KFE / stationary KFE / steady state / `solve_household_steady_state`;
  no derivative clipping/flooring; margin acceptance-only;
- outcome decision: exactly one terminal — A on the real evidence, B on
  synthetic state switching, C on unreproducible reconstruction / unreliable
  first-order prediction;
- deterministic full repeat (bit-identical outcome/trace/root);
- summary CSV well-formed and deterministic.

## 10. Reproducibility / run counts

- Commands:
  - `$env:PYTHONPATH = "D:\deep-learning-hank\src"`
  - `python -m pytest tests/test_dlh_5vn_local_resolvent_geometry.py -q`
    (24/24 pass, ~12 s)
  - diagnostic driver: `run_local_geometry_diagnostic_twice()` executed once
    (ONE run + ONE deterministic repeat, bit-identical;
    `deterministic_repeat_identical: true`; ~1 s);
    `DLH_5VN_LOCAL_GEOMETRY_SUMMARY.csv` written from the first run.
  - After the R1 repair the same diagnostic was re-executed: crossing/root/
    below-above evidence and the terminal are unchanged (bit-identical);
    the only new quantity is `direction.dpb_zero_count = 40` (the
    V-independent `i == 0` states).
- Run counts: exactly ONE deterministic reconstruction of the accepted Issue #61
  trajectory (2 accepted updates); ONE local infinitesimal-direction
  diagnostic; ONE bracketed continuous crossing solve on `[0, 1000·2^-20]`;
  ONE deterministic repeat. No other scientific configuration.

## 11. Forbidden-operation check (all respected)

No mutation of the household oracle, selected-Q source, or accepted Issue #61
implementation (all read-only; blobs unchanged); no economics/prices/grid/
domain/initialization/control-search/tolerances/PB_MARGIN change; no extension
of the Issue #61 discrete ladder as the experiment; no accepted third HJB
iterate; no multi-step continuation/homotopy; no value damping; no p_b
clip/floor; no price or Wmax/resolution sweeps; no KFE/stationary KFE / steady
state / `solve_household_steady_state`; no SCC/global-Q/GE/multi-region/neural/
nominal/calibration/policy/welfare/Results; no PR/merge/close/successor/
self-accept.

## 12. Deliverables (exactly four NEW paths)

1. `src/deep_learning_hank/two_asset/local_resolvent_domain_geometry.py`
2. `tests/test_dlh_5vn_local_resolvent_geometry.py`
3. `reports/dlh_5vn_local_resolvent_geometry_2026_09_13/DLH_5VN_LOCAL_RESOLVENT_GEOMETRY_REPORT.md` (this file)
4. `reports/dlh_5vn_local_resolvent_geometry_2026_09_13/DLH_5VN_LOCAL_GEOMETRY_SUMMARY.csv`
