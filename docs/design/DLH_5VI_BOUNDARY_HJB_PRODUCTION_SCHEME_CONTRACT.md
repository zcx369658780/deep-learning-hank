# DLH-5V-I — Boundary-HJB Production-Scheme Contract (Issue #57)

**Issue #57 / DLH-5V-I — OPEN.** `SCIENTIFIC_DESIGN__BOUNDARY_HJB_SCHEME_CONTRACT_AND_IMPLEMENTATION_READINESS`
**Branch:** `dsh/issue-57-dlh-5vi-boundary-hjb-scheme-design-2026-09-12`
**Fresh live `main` at final activation:** `6df5bc9441b1db709b61eb0abc6e4e41debee636`
**Activation comments:** `5644365170` (authoritative activation) + `5644371668` (final CURRENT sync refresh)
**Authority marker:** `DLH_5VI_BOUNDARY_HJB_SCHEME_DESIGN_AUTHORIZED`
**Owner route decision:** `APPROVE_ROUTE_B_FREEZE_OUTCOME_B_THEORY_LIMIT_AND_PROCEED_TO_BOUNDARY_HJB_SCHEME_DESIGN`
**Micro-Rev (Rev 2, committed on top of candidate `816a817a04f0bb7fbcb0fdc4f8690fab41eddb61`):**
Reviewer `5644585238` verdict
`DLH_5VI_OUTCOME_A_NOT_YET_ACCEPTED__STATE_FAMILY_OWNERSHIP_AND_VALIDATION_SEMANTICS_FIX_REQUIRED` —
repaired in this revision: ONE state-family ownership convention (Route A, §5), scratch
classifier truth-table (report 3 §11), Gate 1A/1B split (report 5 §5), two-residual contract
(report 5 §3), exact-tie semantics (report 4 §4), z-switch authority wording (report 4 §1).
Initial candidate remains in the branch history (NOT reset/rebased/discarded).

**Status: DESIGN / PROVENANCE ONLY.** No source mutation, no implementation, no
HJB/Q/KFE/stationary execution, no numerical `W_max`, no PR/merge/close/successor/self-accept.

This is the umbrella contract for the boundary-HJB production-scheme design gate. It freezes
the exact design chain, the state-family classifier, the economic-vs-algorithmic control
semantics, the Bellman score / ONE-selection / conservative ONE-Q contract, the HJB-iteration
integration, the validation hierarchy, the failure taxonomy, and the terminal. Detailed
arguments live in the five companion reports (File map, §8).

---

## 1. Controlling authority

- Issue #57 is the sole active Builder authority; governance CURRENT files agree.
- Latest accepted gate: **Issue #56 / DLH-5V-H** — CLOSED at accepted **Outcome B**
  (candidate/integration `55e29523e6f1bfefab270c05113984af003ea44b`; acceptance `5644186157`;
  integration `5644340159`; verdict
  `DLH_5VH_ACCEPTED__OUTCOME_B_CONFIRMED__UNBOUNDED_CONTROL_NUMERICAL_SCHEME_AND_STATE_CONSTRAINT_CONVERGENCE_APPLICATION_BLOCK_FROZEN`).
- The Issue #56 unbounded-control / state-constraint convergence-application block is an
  explicit, frozen theory ceiling: this gate does not solve it and does not silently relabel
  it solved. The 5V-H discrete smooth-test coercivity / optimizer-localization lemma (§D.5) is
  **design guidance** for search localization only, never a global production fixed-point
  theorem.
- Accepted household source (immutable/read-only): blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e` (verified).
- Stationary KFE remains **NOT AUTHORIZED**.

## 2. Route-B scientific interpretation (binding)

- Kaplan-class / two-asset HA HJBs are numerical nonlinear fixed-point/PDE objects; **no
  analytic closed-form `V(a,b,z)` is required or sought** in this gate.
- Future acceptance is numerical: iterative convergence to declared tolerance, HJB residual,
  finite/economically admissible policies, drift diagnostics, regression against the accepted
  household oracle, later resolution / `W_max` robustness.
- Owner empirical rate experience (`r_b ≈ 0.02`, roughly `0.05 < r_a < 0.12`) is
  **NON-BINDING DIAGNOSTIC GUIDANCE ONLY** — not calibration/theorem/acceptance authority,
  not permission to tune until convergence.

## 3. Frozen science (consume, do not reopen)

- Domain `D_W(W_max) = {0 <= a <= a_max, b >= b_min, a+b <= W_max}`, `a_max = 10`,
  `b_min = -2`; grid `a_j = j*10/(19m)`, `b_i = b_min + i*7/(19m)`, `10j + 7i <= N_m`;
  no numerical production `W_max` selected.
- True control domain `c > 0`, `l >= 0`, `d in R`; **no** global `mu_b >= 0` budget, **no**
  static-budget inequality, **no** hard economic `c/l/d` bounds; `tau` is the wage wedge
  inside effective wages (never additive transfer income).
- Active-face tangent laws (jointly at feasible intersections):

```text
a = 0:       mu_a >= 0
b = b_min:   mu_b >= 0
a = a_max:   mu_a <= 0
a + b = W_max: mu_W = mu_a + mu_b <= 0
```

- Drift/payoff source-exact (blob verified): `mu_a = r_a_eff(a)*a + d`;
  `mu_b = r_b*b + labor_income - d - chi(d,a) - c`;
  `mu_W = mu_a + mu_b` (linear `d` cancels; `chi` remains); `g = u(c) - v(l)` with
  `u` the frozen CRRA/log form, `v` the (1+phi)-power disutility; `gamma_c > 0, phi > 0`
  parameter-generic (`gamma_c = 2, phi = 5` fixtures are `VALIDATION_FIXTURE_NOT_CALIBRATION`,
  not theory authority).
- Accepted finite-process chain consumed: DLH-5T KKT laws; DLH-5V-A..E sector contracts;
  DLH-5V-F representability obstruction (accepted provenance, consumed as candidate-level
  exclusion — never a silent clip, never a lost-diagonal exit); DLH-5V-G corner-semantics
  corrections; DLH-5V-H Outcome-B ceiling.

## 4. Frozen design chain (Issue §4)

```text
represented state (j, i, z)
 -> exhaustive state-family classifier (F0..F11; deterministic, mutually exclusive)
 -> true continuously admissible control family (c>0, l>=0, d in R + active tangent laws)
 -> numerical optimizer/search semantics (algorithmic brackets only; expansion rule)
 -> exact represented destinations (sector contract; availability conditions)
 -> candidate-specific nonnegative rates from LOCAL drift mu(s, alpha) BEFORE maximization
 -> candidate discrete H_h score (u - v + sum q [V(dest)-V(s)] + z-switch)
 -> ONE statewise global selection (deterministic tie rule; no score/moment perturbation)
 -> selected control + selected rates (exactly the scored rates)
 -> ONE conservative backward Q row (Q[row,col]>0 iff actual transition; Q[row,row]=-sum; Q 1 = 0)
 -> implicit/pseudo-time HJB linear step [(1/delta + rho)I - Q_selected] V_new = u_selected + V_old/delta
 -> convergence / residual / failure diagnostics
```

Economic admissibility is strictly separated from numerical search mechanics (report 4 §2).

## 5. State-family classifier — summary (full table in report 3)

**Micro-Rev (Reviewer `5644585238`):** ONE ownership convention — **Route A** — with explicit
precedence: **F9 (triple corner, `N_m = 190m` exactly) checked first and exclusive; F4
(`i = 0` W-contact) before F3; corner cells before face families.** F2/F3/F4 own their ENTIRE
endpoint bands; F8 is the genuinely residual disjoint set of W-active cells inside the regular
j-band below the `i ≥ 10` floor. The scratch classifier truth-table (TEMP, not committed)
verified `family_count == 1` for every represented state and
`dispatch_contract_count == 1` (or 0 with documented exclusion) per admissible drift-sign
class over 74 `(m, N_m)` cases / 120,272 states / 50,036 classes (report 3 §11).

| Family | Membership (Route A) | Active tangent laws | Sector contract(s) | Destination offsets |
|---|---|---|---|---|
| F0 interior / W-inactive | not W-active, no face, no corner | none (full plane) | accepted interior path (local rows UNCHANGED for same input; global iterate NOT claimed bit-identical — Gate 1A/1B) | 4-neighbor upwind |
| F1 regular W-active | W-active, 7 ≤ j ≤ 19m−7, i ≥ 10 | μ_W ≤ 0 | T_realloc ∪ R_reverse ∪ R_deplete (unique by μ_b/μ_a signs) | w_T, w_RT, w_left, w_down |
| F2 lower-a × W | W-active, j ∈ {0..6} (entire band) | j=0: {μ_a ≥ 0, μ_W ≤ 0}; j∈{1..6}: {μ_W ≤ 0} | j=0: REV (q_RT = 19m·μ_a/70, q_down = 19m·(−μ_W)/7); band: R_reverse / R_deplete by signs; μ_b ≥ 0 excluded (5V-F forward-sliding content) | w_RT, w_down; w_left, w_down |
| F3 upper-a × W | W-active, j ∈ {19m−6..19m}, i ≥ 1 (entire band; i=0 is F4/F9) | j=19m: {μ_a ≤ 0, μ_W ≤ 0}; band: {μ_W ≤ 0} | TDEP split: μ_b ≥ 0 → T_realloc; μ_b < 0 → R_deplete; R_reverse excluded (j+7 > 19m; 5V-F reverse-sliding content) | w_T, w_left, w_down |
| F4 b_min × W W-contact | W-active, i = 0 (Regime-I instance: (19m, 0), i_t(19m) = 0, N_m ∈ {191m..196m}; at N_m = 190m → F9) | {μ_b ≥ 0, μ_W ≤ 0} | Case B / T_realloc (q_T = 19m·μ_b/70, q_in = 19m·(−μ_W)/10) | w_T, w_left |
| F5 non-W lower-a face | j = 0, W-inactive, i ≥ 1 (corner (0,0) → F10) | {μ_a ≥ 0} | interior face (q_right = 19m·μ_a/10 + b-moves) | w_right, w_up, w_down |
| F6 non-W upper-a face | j = 19m, W-inactive, i ≥ 1 (corner (19m,0) → F11) | {μ_a ≤ 0} | interior face (q_left = 19m·(−μ_a)/10 + b-moves) | w_left, w_up, w_down |
| F7 non-W lower-b face | i = 0, W-inactive, 1 ≤ j ≤ 19m−1 (corners → F10/F11) | {μ_b ≥ 0} | interior face (q_up = 19m·μ_b/7 + a-moves) | w_up, w_right, w_left |
| F8 residual W-active | W-active, 7 ≤ j ≤ 19m−7, 1 ≤ i ≤ 9 (sub-tops with i_t(j) = 10; residual, disjoint) | {μ_W ≤ 0} | μ_b ≥ 0 → T_realloc; μ_b < 0, μ_a ≤ 0 → R_deplete; μ_b < 0, μ_a > 0 excluded (mirror needs i ≥ 10) | w_T, w_left, w_down |
| F9 triple corner (W_max=8) | N_m = 190m exactly, cells (19m−7, 9), (19m, 0) — EXCLUSIVE, checked first | {μ_a ≤ 0, μ_b ≥ 0, μ_W ≤ 0} | TREA: Case-B at (19m−7, 9) (no mirror); T_realloc at (19m, 0) | w_T, w_left |
| F10 corner (0, b_min) | non-W, always W-inactive (i_t(0) ≥ 10) | {μ_a ≥ 0, μ_b ≥ 0} | cone{w_right, w_up} | w_right, w_up |
| F11 corner (a_max, b_min) | non-W, N_m ≥ 197m (i_t(19m) ≥ 1); N_m ∈ {191m..196m} → F4; N_m = 190m → F9 | {μ_a ≤ 0, μ_b ≥ 0} | cone{w_left, w_up} | w_left, w_up |

Every family fixes destination-availability conditions, rate formulas, zero-rate ownership
(`μ_a = 0`, `μ_W = 0`, `μ_b = 0`, `μ = (0,0)` equality cases owned by exactly one sector),
and its accepted source authority (report 3 §2–§9). The 5V-F obstruction classes are explicit
candidate-level exclusions (report 3 §10.3): unrepresentable candidates are excluded whole,
never kept in the diagonal as a lost exit. Classifier completeness/determinism: report 3 §11.

## 6. Core contracts (summary)

- **Controls vs brackets (report 4 §2):** brackets are ALGORITHM ONLY; derived from
  effective-gradient FOC anchors and/or the 5V-H localization guidance; expand/retry on bound
  contact; persistent contact → `OPTIMIZER_SEARCH_FAILURE`; bracket-binding optima never
  accepted as economics; non-binding status a mandatory diagnostic; no tuning.
- **Derivative / effective-domain diagnostics (report 4 §5):** (A) accepted interior floors /
  masks (1e-6 floor, drift tolerance 1e-12, bare-a transfer evaluation) preserved on the
  interior path; (B) boundary contract diagnostics — non-finite derivative / non-positive
  `V_b^eff` where `p_b > 0` required / non-finite score / failed localization / no admissible
  represented candidate / no conservative row — each a named failure, never clipped.
- **Bellman + ONE selection (report 4 §1–§4):** `H_h = u − v + Σ q [V(dest)−V(s)] + Σ κ[V(z′)−V(z)]`;
  rates from local drift before maximization; no optimize-then-clip; sector = representation
  only; ONE global argmax; **tie semantics = exact/machine-identical maxima (Option A, no
  positive score tolerance; epsilon-optimal semantics explicitly not adopted)**, deterministic
  tie rule (sector precedence, then lexicographic controls) that does not perturb
  score/first moment; selected rates = scored rates; z-switch authority = the accepted
  `grid.switch_matrix` / exogenous switching generator supplied to the oracle (no claim of a
  `mu_z, sigma_z`-derived mapping); combined without double counting (controlled vs switching
  transition types disjoint).
- **Conservative ONE Q row (report 4 §6):** `Q[row,col] > 0` iff actual represented
  transition; `Q[row,row] = −Σ` actual outgoing; row sums zero by construction; no
  normalization/pinning; HJB score and Q row same candidate/rates; mandatory structural
  checks (row sums, offdiag signs, destination membership, first moments, score
  recomputation, deterministic repeat, candidate identity, switch orientation).
- **HJB iteration (report 5 §1–§4):** accepted `[(1/δ+ρ)I − Q_selected]V_new = u_selected +
  V_old/δ` structure preserved; F0 rows unchanged (interior path, local-row semantics); 
  boundary-family rows conservative; z-switch `kron(switch, I)` added to both; initial δ
  semantics preserved; **TWO separate residuals**: per-iteration fixed-policy/policy-evaluation
  residual `R_policy_iter = (ρI − Q_selected(V_old))V_new − u_selected(V_old)` (diagnostic
  only) and mandatory final Bellman residual `R_Bellman(V) = ρV − [u_selected(V) +
  Q_selected(V)V]` from the post-convergence re-selection, with predeclared
  `tolerance_Bellman` (iterate-change `tolerance_iter` kept separate); max-iteration →
  nonconvergence; non-finite/singular solve failure; policy/family switching diagnostics near
  convergence; post-convergence recomputation of policies + final Q from the final V.
- **Validation hierarchy (report 5 §5):** **Gate 1A exact local/common-input F0 regression**
  (same frozen V; local row/policy/rates match the accepted oracle path to declared
  semantics; failure → `REGRESSION_FAILURE`); **Gate 1B global boundary-influence diagnostic**
  (interior V/policies compared only as localization diagnostic with predeclared
  subset/tolerances; NOT automatic regression failure); Gate 2 local boundary algebra per
  family incl. exactly-one family/dispatch checks, obstruction cells and triple corner;
  Gate 3 deterministic finite-domain smoke (iterate convergence, final Bellman residual ≤
  predeclared `tolerance_Bellman`, finite V, c > 0, finite l/d/drifts, conservative Q, no
  bracket-binding artifact, deterministic repeat); Gate 4 diagnostic rate cases (Owner
  experience labelled DIAGNOSTIC/VALIDATION, not calibration; no sweep); Gate 5
  resolution/`W_max` downstream.
- **Failure taxonomy (report 4 §7 / report 5 §4):** `SCIENTIFIC_ADMISSIBILITY_FAILURE`,
  `REPRESENTATION_FAILURE`, `OPTIMIZER_SEARCH_FAILURE`,
  `DERIVATIVE_EFFECTIVE_DOMAIN_FAILURE`, `GENERATOR_CONSERVATION_FAILURE`,
  `HJB_LINEAR_SOLVE_FAILURE`, `HJB_NONCONVERGENCE`, `REGRESSION_FAILURE` — explicit, no
  silent fallback.

## 7. Terminal (exactly one)

```text
DLH_5VI_BOUNDARY_HJB_SCHEME_CONTRACT_FROZEN__IMPLEMENTATION_GATE_READY_UNDER_ACCEPTED_OUTCOME_B_THEORY_CEILING
```

**Rationale:** the state-family classifier, candidate-control/search semantics, Bellman score,
ONE selection, conservative Q-row contract, HJB-iteration integration, failure taxonomy and
validation hierarchy are unambiguous and no new scientific contradiction was found — Outcome A
(implementation-ready design contract under the accepted Outcome-B theory ceiling).

## 8. File map (exact six-file allowlist — all NEW, no existing tracked file modified)

1. `docs/design/DLH_5VI_BOUNDARY_HJB_PRODUCTION_SCHEME_CONTRACT.md` (this file)
2. `reports/dlh_5vi_boundary_hjb_scheme_design_2026_09_12/DLH_5VI_AUTHORITY_AND_ACCEPTED_INPUTS.md`
3. `reports/dlh_5vi_boundary_hjb_scheme_design_2026_09_12/DLH_5VI_STATE_FAMILY_AND_CANDIDATE_CONTRACT.md`
4. `reports/dlh_5vi_boundary_hjb_scheme_design_2026_09_12/DLH_5VI_BELLMAN_SELECTION_AND_ONE_Q_ROW_CONTRACT.md`
5. `reports/dlh_5vi_boundary_hjb_scheme_design_2026_09_12/DLH_5VI_HJB_ITERATION_AND_VALIDATION_PLAN.md`
6. `reports/dlh_5vi_boundary_hjb_scheme_design_2026_09_12/DLH_5VI_IMPLEMENTATION_READINESS_TERMINAL_AND_FORBIDDEN_CHECK.md`

## 9. Forbidden operations (summary)

Design-only: no source mutation; no implementation; no production HJB/Q/KFE/stationary
execution; no numerical `W_max`; no ghost states / grid / aspect / domain redesign; no hard
economic control bounds; no `gamma_c/phi/tau` authority change; no reopening of Issues
#54/#55/#56 verdicts; no claim the Outcome-B block is solved; no aggregates/GE/regional/
neural/nominal/calibration/policy/welfare/Results; no PR/merge/close/successor/self-accept.
Stationary KFE remains **NOT AUTHORIZED**. See the forbidden check (report 6).

## 10. Stop

The Builder completes the six-file package, commits and pushes the dedicated branch, verifies
remote SHA = local SHA, publishes exactly one completion comment, and **stops for fresh
ChatGPT review**. No merge, no close, no successor, no self-accept.
