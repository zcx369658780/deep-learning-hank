# DLH-5V-I — Authority and Accepted Inputs (Issue #57)

**Report 2 of 6** — `DLH_5VI_AUTHORITY_AND_ACCEPTED_INPUTS.md`

This report freezes the controlling authority, the accepted scientific inputs that the
boundary-HJB production-scheme design consumes, and the binding Route-B interpretation
ceiling. Everything here is consumed, not reopened.

**Micro-Rev (Rev 2, Reviewer `5644585238`):** this revision adds the z-switch authority
wording fix (§5 — the controlling switching object is the accepted `grid.switch_matrix`,
with no claim of a `mu_z, sigma_z`-derived mapping) and records the single ownership
convention consumed by the classifier (Route A, report 3 §1). Committed on top of initial
candidate `816a817a04f0bb7fbcb0fdc4f8690fab41eddb61` (NOT reset/rebased/discarded).

---

## 1. Controlling authority

- **Issue #57 / DLH-5V-I — OPEN (sole active Builder authority).**
  - Title: `DLH-5V-I: Freeze boundary-HJB production scheme contract under accepted Outcome-B theory ceiling`
  - Task type: `SCIENTIFIC_DESIGN__BOUNDARY_HJB_SCHEME_CONTRACT_AND_IMPLEMENTATION_READINESS`
  - Owner decision: `APPROVE_ROUTE_B_FREEZE_OUTCOME_B_THEORY_LIMIT_AND_PROCEED_TO_BOUNDARY_HJB_SCHEME_DESIGN`
  - Authority marker: `DLH_5VI_BOUNDARY_HJB_SCHEME_DESIGN_AUTHORIZED`
  - Activation comments: `5644365170` (authoritative activation) + `5644371668` (final CURRENT synchronization refresh; live `main` = `6df5bc9441b1db709b61eb0abc6e4e41debee636`).
  - Dedicated branch: `dsh/issue-57-dlh-5vi-boundary-hjb-scheme-design-2026-09-12` (created from fresh `origin/main` `6df5bc9…`; verified equal to local HEAD).
- **Latest accepted gate — Issue #56 / DLH-5V-H — CLOSED at accepted Outcome B.**
  - Accepted candidate / integration: `55e29523e6f1bfefab270c05113984af003ea44b`
  - Reviewer acceptance: `5644186157`
  - Acceptance integration / Owner route decision: `5644340159`
  - Accepted verdict: `DLH_5VH_ACCEPTED__OUTCOME_B_CONFIRMED__UNBOUNDED_CONTROL_NUMERICAL_SCHEME_AND_STATE_CONSTRAINT_CONVERGENCE_APPLICATION_BLOCK_FROZEN`
  - Accepted terminal: `DLH_5VH_THEORY_AUDIT_PARTIAL__ONE_BOUNDED_BOUNDARY_CONSISTENCY_OR_COMPARISON_GAP_REMAINS`
  - The Outcome-B block (UNBOUNDED-CONTROL NUMERICAL-SCHEME / STATE-CONSTRAINT CONVERGENCE-APPLICATION BLOCK) is an explicit, frozen theory limitation. **This gate does not attempt to solve it and does not silently relabel it solved.**
- **Fresh live `main` at final activation (re-verified by fresh fetch at this gate):** `6df5bc9441b1db709b61eb0abc6e4e41debee636` — no conflict; the three CURRENT governance files (`tasks/TASK_INDEX_CURRENT.md`, `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`, `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`) name Issue #57 / DLH-5V-I as ACTIVE with this exact task type, branch and authority marker.
- **Accepted household source (immutable / read-only):** `src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`, blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e` (verified at this gate). No source mutation in this gate.

## 2. Binding Route-B scientific interpretation

1. Kaplan-class / two-asset heterogeneous-agent HJBs are **numerical nonlinear fixed-point/PDE objects**. An analytic closed-form value function `V(a,b,z)` is **not** an acceptance requirement and no effort is spent searching for one in this gate.
2. The future production acceptance standard is **numerical**: iterative convergence to a declared tolerance; HJB residual statistics; finite/economically admissible policy controls; drift diagnostics; regression against the accepted household oracle on unaffected states; later resolution / `W_max` robustness.
3. Issue #56's unbounded-control / state-constraint convergence-application block remains an explicit theory limitation of this design. The discrete smooth-test coercivity / optimizer-localization lemma of the 5V-H audit (monotone-scheme report §D.5) is available as **design guidance** for the numerical search/localization semantics — it is **NOT** a global production fixed-point theorem and must not be presented as one.
4. **Owner empirical experience** (HJB convergence often observed near `r_b = 0.02` and roughly `0.05 < r_a < 0.12`) is **NON-BINDING DIAGNOSTIC GUIDANCE ONLY**. It is not calibration authority, not a theorem assumption, not a frozen acceptance interval, not evidence that values outside the range fail, and not permission to tune parameters until the solver converges. It may inform future smoke-test / diagnostic case selection (validation plan Gate 4) with explicit `DIAGNOSTIC / VALIDATION` labelling.

## 3. Frozen domain, grid and economic laws (consume, do not reopen)

```text
D_W(W_max) = { (a,b,z) : 0 <= a <= a_max, b >= b_min, a + b <= W_max, z in {z0, z1} }
a_max = 10,  b_min = -2
grid: a_j = j*10/19 (j = 0..19), b_i = b_min + i*7/19 (i >= 0)
nodes: 10*j + 7*i <= N,  N = floor(19*(W_max - b_min)) = floor(kappa)
fixed-aspect refinement family (accepted provenance): da_m = 10/(19m), db_m = 7/(19m),
  a_j = j*10/(19m), b_i = b_min + i*7/(19m), N_m = floor(19m*(W_max - b_min)),
  represented nodes 10*j + 7*i <= N_m,   j_max = 19m
```

- **No numerical production `W_max` is selected in this gate.** The contracts are written at the frozen symbolic finite-`m` level (`m >= 1`; the production implementation gate fixes `m`). Selection of `W_max` remains downstream (validation plan Gate 5).
- **True economic control domain:** `c > 0`, `l >= 0`, `d in R`. No false global `mu_b >= 0` budget; no static-budget inequality replacing the liquid drift; no hard economic `c/l/d` bounds; `tau` is the wage wedge inside effective wages `w_j*(1 - tau - mig_j)*z`, never additive transfer income. (The accepted source's exogenous per-period `transfer_income` object, where present, is a named exogenous resource netted against consumption in `mu_b`; it is preserved as-is and is not reintroduced as a τ-like additive term anywhere in this design.)
- **Active-face tangent laws (applied jointly at feasible intersections):**

```text
a = 0:          mu_a >= 0
b = b_min:      mu_b >= 0
a = a_max:      mu_a <= 0
a + b = W_max:  mu_W = mu_a + mu_b <= 0
```

- **Drift / payoff (source lines 80–157):**

```text
r_a_eff(a) = r_a*(1 - 0.1*(a/a_max)^9)  (accepted taper, >= 0.9*r_a >= 0)
mu_a = r_a_eff(a)*a + d
chi(d,a) = chi_0*|d| + 0.5*chi_1*d^2/max(a, a_bar)
labor_income = sum_j w_j*(1 - tau - mig_j)*z*l_j
mu_b = r_b*b + labor_income - d - chi(d,a) - c        (d enters -1, chi enters -1)
mu_W = mu_a + mu_b = r_a_eff(a)*a + r_b*b + labor_income - chi(d,a) - c   (linear d cancels; chi remains)
g(c,l) = u(c) - v(l),  u(c) = log(c) if gamma_c = 1 else c^(1-gamma_c)/(1-gamma_c),  gamma_c > 0
v(l) = sum_j omega_j*l_j^(1+phi)/(1+phi),  phi > 0
```

- **Parameter authority:** the source freezes only `rho > 0, gamma_c > 0, phi > 0, chi_0 >= 0, chi_1 > 0, a_bar > 0, mu_z >= 0, sigma_z >= 0`. Repository instances with `gamma_c = 2, phi = 5` are `VALIDATION_FIXTURE_NOT_CALIBRATION` and are **not** theory authority. This design is parameter-generic; no numeric `gamma_c / phi` value is promoted.

## 4. Accepted finite-process authority chain (consumed, not reopened)

| Authority | Content consumed by this gate |
|---|---|
| DLH-5T (Issue #46) | Finite domain `D_W`; unified KKT convention `L = H - sum lambda_j g_j`, `g_j = mu·n_j <= 0`; per-face effective gradients (`V + lambda` lower faces, `V - lambda` upper/W faces); W-face transfer FOC with `lambda_W` cancelling one-for-one from the linear part; `a = a_max` face tightening (`mu_a <= 0` with `d <= -r_a_eff(a_max)*a_max` at the anchor, materially stricter than the old `d <= 0` mask); same-process law `HJB boundary policy <=> KFE boundary transition law`; `Q_ij >= 0 (i != j)`, `Q_ii = -sum ACTUAL represented outgoing rates`, `Q 1 = 0`; no KFE-only repair; W1 tangential-drift representation caveat consumed as provenance (superseded by the accepted sector contracts of DLH-5V-A..E at the frozen taxonomy level) |
| DLH-5V-A..D | Accepted W-frontier phase / class formulas (`i_t(j) = floor((N_m - 10j)/7)`, `r_j = (N_m - 10j) mod 7`); wide stencils `w_T = (-70/(19m), +70/(19m))`, `w_RT = (+70/(19m), -70/(19m))`, `w_left = (-10/(19m), 0)`, `w_down = (0, -7/(19m))`, `w_right`, `w_up`; `T_realloc = {mu_a <= 0, mu_b >= 0, mu_W <= 0}` with `q_T = 19m*mu_b/70`, `q_in = 19m*(-mu_W)/10`; rate/scoring semantics "rates from the LOCAL drift before maximization" |
| DLH-5V-E (Issue #53) | Regular W-band closure on the common regular region `7 <= j <= 19m-7`, `i >= 10`: `R_reverse` (`q_RT = 19m*mu_a/70` on `w_RT`, `q_down = 19m*(-mu_W)/7` on `w_down`), `R_deplete` (`q_left = 19m*(-mu_a)/10`, `q_down = 19m*(-mu_b)/7`); full coverage `T_W = T_realloc union R_reverse union R_deplete` with boundary ownership `B1 (mu_b = 0 -> T_realloc limit)`, `B2 (mu_a = 0 -> R_deplete limit)`, `B3 (mu_W = 0 sliding ray, rate `19m|mu_b|/70`)`, `mu = (0,0)` trivial; one sector per candidate (no double counting); future global composition = score each sector candidate, ONE global argmax, selected rates into ONE backward Q |
| DLH-5V-F (Issue #54) | Endpoint-band / joint-boundary closure: closable classes with exact seam-consistent contracts (`j = 0` lower-a × W reverse sector; `j = 19m` upper-a × W T_realloc/deplete split; `b_min × W` Case-B cells); **representability obstruction certificate**: at exact-frontier `r_j = 0` W-active top cells in the a-interior endpoint bands (`j in {1..6}` forward-sliding, `j in {13..18}` reverse-sliding) the continuously admissible W-tangent sliding ray of the missing orientation is NOT representable by any nonnegative combination of actual represented native-grid destinations (universal for every `N >= 190` in the Regime-I symbolic family; exact enumeration `N in [190, 260]` 121/121). This is **accepted provenance**; the production candidate contract consumes it (state-family and candidate contract, §5) |
| DLH-5V-G (Issue #55) | Route-A shrinking-layer approximation **Outcome C** under the exact raw graph target; corner-semantics corrections frozen (true cones at the Regime-I corners; `W_max = 8` triple corner; for fixed `W_max > 8` the W-active lower-b layer cells disappear for large `m`). Consumed; not reopened |
| DLH-5V-H (Issue #56) | **Outcome B accepted.** The strong raw graph target is over-strong for operator/test-function consistency; the legitimate target is monotone-scheme consistency with one-sided boundary subsolution on the closure; discrete smooth-test coercivity / optimizer-localization lemma (§D.5 of the monotone-scheme report) and the corrected logical order (raw controls -> discrete localization -> compact maximizing controls -> uniform rates/drift -> O(1/m) second moment -> max-level Taylor) are **design guidance** for the numerical search semantics; scheme-level stability / strict contraction / constant-test operator-finiteness / relevant-gradient effective-domain restriction / Soner-CD(L) comparison mapping remain the frozen unbounded-control convergence-application block. Consumed as the theory ceiling |

## 5. Accepted source integration mapping (read-only facts)

Read-only facts from `src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py` used for the iteration-integration contract (validation plan):

- `solve_matlab_faithful_hjb` (lines 511–563): pseudo-time implicit step
  `matrix = (1/delta + rho)*I - operator.full`, `rhs = utility + old/delta`,
  `value = spsolve(matrix, rhs)`, iterate-change statistic `max|value - old|` vs
  `convergence_tolerance`, `max_iterations` cap, `converged` flag.
- Operator assembly (lines 425–464): per-axis signed source placement with outward
  **truncation of entries but NOT of the diagonal** (documented
  `MATLAB_FAITHFUL_HJB_ITERATION_BB_MAY_HAVE_SIGNED_OFFDIAGONALS_AND_NONZERO_BOUNDARY_ROW_SUMS`),
  plus exogenous z-switch via `kron(switch_matrix, eye(state_size))`.
- **Z-switch authority (Micro-Rev provenance fix, Reviewer `5644585238`):** the controlling
  switching object is the accepted `grid.switch_matrix` — the exogenous switching generator
  **supplied to the household oracle**. Production switching rates ARE the switch-matrix
  entries; the design makes **no claim** that they are derived from `mu_z, sigma_z` (that
  mapping is not an accepted repository contract and is not asserted anywhere in this gate).
  (`mu_z, sigma_z >= 0` remain frozen parameter-positivity facts only, §3.)
- Local policy selection: MATLAB-faithful FOC candidates (consumption FOC `c = v_b^(-1/gamma_c)`
  with the accepted `1e-6` derivative floor; labor FOC; bare-`a` transfer candidate evaluated on
  the RAW `v_a/v_b` with no positivity guard — exact-zero/non-finite denominators yield IEEE
  results handed to the accepted masks downstream), upwind `max(mu,0)/step` rates, face masks.
- `MATLAB_DERIVATIVE_FLOOR = 1e-6` and `MATLAB_DRIFT_TOLERANCE = 1e-12` are accepted source
  constants: the floor is accepted interior authority where the source applies it
  (consumption/labor FOCs); the drift tolerance is the accepted zero-drift threshold.
- Post-convergence operator: upwind rates recomputed from the final `mu_a, mu_b` arrays
  (`max(-mu_b,0)/db`, `max(mu_b,0)/db`, `max(-mu_a,0)/da`, `max(mu_a,0)/da`) — the
  post-convergence policy/Q recomputation pattern this design generalizes.
- Stationary KFE (`solve_matlab_faithful_stationary_kfe`, lines 586+) exists in the oracle but
  remains **NOT AUTHORIZED** in this gate and in the boundary-scheme design.

**Derivative-behavior distinction (Issue §7, consumed into the Bellman/selection report):**
(A) accepted interior-source behavior — FOC-based policy with the accepted floors/masks;
(B) new boundary scientific contract — candidate-based discrete scoring with the effective
gradients of the active face(s) as seeding/localization evidence only; pathological
derivative evidence is a diagnostic failure (taxonomy), never silently clipped.

## 6. Same-process binding law (unchanged)

```text
controlled process selected by boundary HJB == controlled process represented by future KFE generator
Q backward (HJB),  Q^T forward (future KFE)
Q_ij >= 0 for i != j
Q_ii = -sum of ACTUAL represented outgoing rates
Q 1 = 0 by construction
HJB and future KFE consume the SAME selected Q
```

Pinning/normalization may never repair leakage. Stationary KFE remains **NOT AUTHORIZED**.

## 7. What this gate freezes and what it does not

**Freezes (design-level, implementation-ready):** exhaustive state-family classifier; candidate
admissibility/representability contract; algorithmic search-bracket semantics; derivative /
effective-domain diagnostics; Bellman score + ONE global selection + deterministic ties;
conservative Q-row construction and structural checks; implicit/pseudo-time HJB iteration
integration; validation hierarchy Gates 1–5; failure taxonomy.

**Does not freeze / does not do:** no solver/source mutation; no production HJB/Q/KFE/stationary
execution; no numerical production `W_max`; no grid/aspect/domain redesign; no state augmentation;
no ghost states; no aggregates/GE/regional/neural/nominal/calibration/policy/welfare/Results;
no PR/merge/close/successor/self-accept.
