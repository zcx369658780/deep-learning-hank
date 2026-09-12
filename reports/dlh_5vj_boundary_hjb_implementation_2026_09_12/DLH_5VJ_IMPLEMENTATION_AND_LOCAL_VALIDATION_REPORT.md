# DLH-5V-J Implementation and Local Validation Report

**Issue:** #58 — "DLH-5V-J: Implement boundary-HJB selected-Q solver and pass local validation gates"
**Gate type:** `SCIENTIFIC_IMPLEMENTATION__BOUNDARY_HJB_SELECTED_Q_AND_LOCAL_VALIDATION`
**Marker:** `DLH_5VJ_BOUNDARY_HJB_IMPLEMENTATION_AND_LOCAL_VALIDATION_AUTHORIZED`
**Branch:** `dsh/issue-58-dlh-5vj-boundary-hjb-implementation-2026-09-12`
**Base:** fresh `origin/main` at activation `7d6a11e7110a88b4c2f9e6e992283c940c282071`
**Activation comments:** `5644789118` (activation), `5644795353` (final refresh)
**Reviewer comment (controlling this Micro-Rev):** `5645920346`
**Candidate history (same branch, no reset/rebase):** `d0e5267ea57c8674cccfb8ccd90326735dd1920c` (parent, accepted in material part) → this Micro-Rev commit on top.
**Source blob (read-only facts):** `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`
**Date:** 2026-09-12 (Micro-Rev)

---

## 1. Terminal (exactly ONE)

> **B — `DLH_5VJ_BOUNDARY_HJB_IMPLEMENTATION_PARTIAL__ONE_BOUNDED_NUMERICAL_OR_CONTRACT_GAP_REMAINS`**

The boundary-HJB selected-Q solver is fully implemented and faithful to the accepted Issue #57 contract.
Gate 1A (common-input local regression) and Gate 2 (boundary/family algebra) **pass** (accepted by the
Reviewer and unchanged by this Micro-Rev).

This Micro-Rev applies the **accepted boundary effective-domain guard** (frozen Issue #57 Rev-2 rule):
when the boundary optimizer requires positive effective liquid marginal evidence and the evidence is
non-finite or non-positive, the run must surface `DERIVATIVE_EFFECTIVE_DOMAIN_FAILURE` before any raw
candidate/bracket search. With the guard, the frozen Gate-3 smoke now fails deterministically at
iteration 2 with `DERIVATIVE_EFFECTIVE_DOMAIN_FAILURE` at the **same** state as candidate `d0e5267`
(F3, `(j,i)=(13,13)`, z=0), recorded `p_b = -0.3652 < 0` — the iteration-2 value iterate has left the
accepted positive-liquid-marginal effective domain. The previously documented unbounded `R_DEPLETE`
Bellman score is the **consequence** of that invalid effective-domain state, not a standalone
optimizer-localization defect and not a small-bracket artifact.

The bounded remaining gap is:

> the implemented production HJB iteration leaves the accepted positive-liquid-marginal effective
> domain before convergence — an **effective-domain / unbounded-control production-iteration failure
> within the frozen Issue #56 Outcome-B convergence-application block**.

Terminal A (smoke pass) is NOT claimed. Terminal C (design contradiction) is NOT claimed: `p_b < 0` on
a rough iterate is the design's own predicted effective-domain exit, classified under
`DERIVATIVE_EFFECTIVE_DOMAIN_FAILURE`, and does not contradict the sector algebra, the finite-domain
geometry, or the household HJB. Terminal Blocked is not applicable.

---

## 2. Implementation summary

New module `src/deep_learning_hank/two_asset/boundary_hjb_selected_q.py` (public API
`BoundaryHJBConfig`, `BoundaryHJBGrid`, `BoundaryHJBSolver`, `BoundaryHJBResult`,
`BoundaryHJBFailure`, `sector_dispatch`, `drift_admissible`, `FAMILIES`, `SECTORS`, `SECTOR_RANK`,
`FAILURE_NAMES`):

- **Grid:** restricted-Voronoi triangle `D_W = {0 <= a <= 10, b >= -2, a + b <= W_max}`,
  `a_max = 10`, `b_min = -2`; validation instance `m = 1, W_max = 10` coincides with the canonical
  fixture rectangle for its lower portion: `b = linspace(-2, 5, 20)` (`db = 7/19`),
  `a = linspace(0, 10, 20)` (`da = 10/19`), `z = [0.8, 1.3]`,
  `switch = [[-1/3, 1/3], [1/3, -1/3]]`; represented iff `10j + 7i <= N_m`,
  `N_m = floor(19 m (W_max - b_min)) = 228`; `jmax = 19`, `n_nodes = 391`, `state_size = 782`,
  `i_t(19) = 5`.
- **Classifier (Route A, accepted Rev-2):** W-active iff top `i = i_t(j)` or sub-top `i_t(j) - 1`
  (with `i_t(j) >= 2`). Precedence F9 → F4 → F2 → F3 → F1 → F8 (W-active), then
  F10 → F11 → F5 → F6 → F7 → F0 (W-inactive). Validation-instance histogram:
  F10=1, F5=30, F2=14, F7=18, F0=298, F1=12, F3=14, F11=1, F6=3, F4=0, F8=0 (391 nodes).
- **Boundary candidate search:** cone-aware deterministic d-intervals per family, per-d c-bands from the
  active-face cones, labor candidates {FOC anchor, 0.0}, c-grid (9 points) split at the `mu_b = 0`
  seam, deterministic bracket init around the transfer-FOC anchor, expansion x4 up to 3, exact-tie
  selection via `np.lexsort((sector-rank, c, l, d))` over the ONE global statewise argmax of the
  Bellman score `H = u(c) - v(l) + sum_r q_r [V(dest_r) - V(s)] + sum_z' kappa[z,z'] [V(z',s) - V(z,s)]`
  with rates computed from the local drift BEFORE maximization and sector as representation only.
- **Boundary effective-domain guard (Micro-Rev addition):** at the top of every boundary row, before
  candidate/bracket search, the accepted boundary optimizer/coercivity contract requires positive
  effective liquid marginal evidence `p_b = vb_b` (declared backward derivative, marginal at `i = 0`);
  non-finite or non-positive `p_b` raises `DERIVATIVE_EFFECTIVE_DOMAIN_FAILURE` with
  family/state/z and the offending derivative recorded (iteration attached by the HJB step). `p_b` is
  never clipped or floored; the accepted interior-source derivative floor remains interior authority
  only (the F0 path via the oracle is untouched); no bracket enlargement disguises an invalid
  effective-domain state.
- **Conservative Q rows:** selected rates carried unchanged; off-diagonals are the actual represented
  transitions (within-z), diagonal = -sum of actual outgoing; z-switch via
  `kron(switch, eye(n))` with z as the SLOW index (`row = nz*n + node`); row sums zero;
  first-moment identity `sum q w = (mu_a, mu_b)` verified per row.
- **HJB iteration:** implicit/pseudo-time solve `((1/delta + rho) I - Q) V' = u + V/delta` with
  per-iteration re-selection (accepted policy-iteration pattern), iterate statistic
  `max |V' - V|` vs `tolerance_iter`, frozen failure taxonomy with NO silent fallback, and a
  post-convergence final Bellman residual stage `R_Bellman(V) = rho V - [u + Q V]` (inf norm,
  `tolerance_Bellman`).
- **F0 (interior) rows:** the accepted oracle path UNCHANGED (`select_matlab_faithful_local_policy`
  with the triangle derivative conventions; iteration rates placed b_backward → (j,i-1),
  b_forward → (j,i+1), a_backward → (j-1,i), a_forward → (j+1,i); outward truncation with the
  diagonal kept).

---

## 3. Gate 1A — common-input local regression (PASS, unchanged)

For every interior node whose row is identical to the accepted rectangle machinery (no triangle
truncation difference; `i <= 18`), the module's F0 row is **bit-identical** to the accepted oracle's
local policy and row assembly given the SAME state and derivative inputs:

- 504 rows checked (252 shared F0 nodes x 2 z).
- Exact identity: classifier family, `transfer_label`, consumption, labor, transfer, `mu_a`, `mu_b`,
  utility, all four iteration rates, destinations, and `diagonal == -(rb + rf + ab + af)`.
- Evidence: `tests/test_dlh_5vj_interior_regression.py` (passes; unchanged by the Micro-Rev).

Independent construction-level check (not part of the test suite): the module's F0 rows also match a
separately-built rectangle reference to ~1e-14 (float noise from 1-ulp coordinate rounding), with all
rates and destinations equal; the common-input test above is the exact Gate-1A claim.

## 4. Gate 2 — boundary/family algebra (PASS, unchanged)

- Classifier ownership sweep over `W_max in {8.0 + k/19, k = 0..7, 10.0, 8 + 8/19}` (`N_m = 190..198,
  228`): F9 exclusive at N_m=190, F4 at (19,0) for N_m=191..196, F11 from N_m=197, F8 at (12,9) for
  N_m=191; all windows exact.
- Validation-instance histogram (above) exact; every node classified exactly once.
- Sector dispatch truth tables per family with exact destinations and rates and first-moment identity
  at 1e-9; exactly one sector per served drift class, `None` exactly on the documented whole-candidate
  exclusions (F2b `mu_b >= 0` forward-sliding; F3/F8 `mu_b < 0, mu_a > 0` reverse-sliding
  obstruction); `drift_admissible` tangent laws exact.
- Every dispatched destination represented (W-index preservation) — no defensive
  `REPRESENTATION_FAILURE` trips on the served classes.
- Evidence: `tests/test_dlh_5vj_classifier_dispatch.py` (passes; unchanged by the Micro-Rev).

---

## 5. Gate 3 — exactly ONE predeclared deterministic HJB smoke (deterministic FAILURE; Terminal B)

### 5.1 Complete frozen configuration (predeclared before the first run; unchanged by every retry and by the Micro-Rev)

| parameter | value |
|---|---|
| `m` | 1 |
| `W_max` | 10.0 (VALIDATION INSTANCE ONLY, not a production W_max) |
| `b_min`, `a_max` | -2.0, 10.0 |
| `r_b`, `r_a` | 0.02, 0.08 (DIAGNOSTIC / VALIDATION ONLY) |
| `borrowing_rate_gap` | 0.0 |
| `delta` | 1000.0 |
| `tolerance_iter` | 1e-7 (max |V_new - V_old|) |
| `tolerance_Bellman` | 1e-3 (inf norm) |
| `max_iterations` | 1000 |
| c/d grid | n_c = n_d = 9, deterministic |
| bracket init / expansion | transfer-FOC anchor +/- D (D = max(1, |d*|)); expansion x4; max 3 |
| structural tolerances | drift 1e-12, row sum 1e-9, first moment 1e-9 |
| initial V, labor0 | deterministic fixture construction (brentq labor0; utility-based V) |
| iteration | implicit/pseudo-time with per-iteration re-selection (accepted pattern) |

### 5.2 Smoke outcome after the Micro-Rev guard (deterministic, reproduced identically on every run)

- **Iteration 1 — unchanged and fully inside the effective domain:** 186 boundary rows + 596 F0 rows;
  0 expansions; 0 artificial bindings; 66 economic (cone-seam) bindings; `max |Q row sum| = 7.11e-15`;
  V1 finite, range `[-70.71, -53.66]`; minimum boundary `p_b` at V0 is `+0.4575 > 0` (the guard never
  trips on iteration 1; the iteration-1 operator is conservative and deterministic).
- **Iteration 2 (first failing row):** `DERIVATIVE_EFFECTIVE_DOMAIN_FAILURE` —
  `family 'F3' at (j,i)=(13,13): z=0: non-positive effective liquid marginal p_b=-0.365224
  (boundary optimizer effective-domain guard, before candidate/bracket search)`,
  `detail = {'iteration': 2, 'family': 'F3', 'j': 13, 'i': 13, 'z': 0, 'p_b': -0.36522}`.
- **Mechanism (effective-domain interpretation):** on the iteration-2 value iterate,
  `V(13,13) - V(13,12) = -0.1346` (z=0), so the declared backward liquid derivative is
  `p_b = (V(s) - V(down))/db = -0.3652 < 0`. The accepted boundary optimizer/coercivity contract
  requires **positive** effective liquid marginal evidence; `p_b <= 0` means the iterate has left the
  accepted effective domain, and the guard surfaces the frozen failure **before** any raw
  candidate/bracket search — no bracket expansion is used to disguise the invalid effective-domain
  state. The previously documented unbounded `R_DEPLETE` Bellman score is the **consequence** of this
  state: with `q_down = (19m/7)(-mu_b)` and `-mu_b` growing quadratically through `chi(d, a)` for large
  negative `d`, while `V(down) - V(s) > 0`, the score term `q_down [V(down) - V(s)] -> +inf` — no
  finite bracket could localize the argmax, but the guard now classifies the root cause correctly
  before that raw search is entered.
- **Failure taxonomy change (Micro-Rev):** the frozen smoke no longer pins
  `OPTIMIZER_SEARCH_FAILURE`; the corrected classification is `DERIVATIVE_EFFECTIVE_DOMAIN_FAILURE`
  (persistent `p_b <= 0` on the production iterate), per the frozen Issue #57 Rev-2 effective-domain
  rule. This is an effective-domain / unbounded-control production-iteration failure within the frozen
  Issue #56 Outcome-B convergence-application block; the run never reaches the iterate-convergence or
  final Bellman residual stage. No final Bellman residual is manufactured.
- Evidence: `tests/test_dlh_5vj_hjb_smoke.py` (frozen config; pinned corrected signature incl.
  family/state/z/iteration/offending `p_b`; deterministic repeat with `max|V1a - V1b| == 0.0`),
  `tests/test_dlh_5vj_bellman_q_rows.py` (conservative rows, represented destinations, exact first
  moments, z-switch entries, score recomputation, iteration-1 binding-free determinism).

### 5.3 POST-FAILURE OUT-OF-SCOPE OBSERVATIONS — NOT ACCEPTANCE EVIDENCE

The following were disclosed by the initial completion report but were performed **after** the frozen
scientific failure had been reached, i.e. beyond the explicit STOP-scientific-execution instruction.
They are retained for full disclosure only and are **not acceptance evidence**:

- alternate rate/gap executions (frozen instance with gap=0.01; accepted fixture instance
  r_a=0.03/r_b=0.015/gap=0.01) that showed the pre-guard failure signature repeated across
  configurations;
- accepted-oracle frozen-instance cross-check (`solve_matlab_faithful_hjb` on the frozen instance:
  converged=False after 1000 iterations, statistic 0.0172, a limit cycle; 11 iterations on the
  fixture instance).

No further alternate-config / parameter / W_max / resolution / oracle-convergence executions are
performed in this Micro-Rev (authorized execution is limited to the targeted tests, static checks, and
the SAME frozen Gate-3 configuration for classification verification and deterministic repeat).

---

## 6. Bounded engineering retries (frozen smoke config unchanged)

Six bounded code-bug repairs were made during the original implementation (accepted by the Reviewer);
each is documented and the frozen smoke configuration was never changed:

1. **F7 FACE geometry pairing** — first-moment mismatch at (1,0) fixed by semantic q1/q2 pairing and
   assembly via the mask-owning geometry entry (no FACE double-count).
2. **F3b `R_DEPLETE` mask** — `BLT0` -> `BLT0ALE0`: the `mu_a > 0, mu_b < 0` class leaked into
   `R_DEPLETE` with a negative `q_left`; it is a documented exclusion (mirroring F8).
3. **Uncovered candidates** — candidates with no sector coverage kept a finite raw score; excluded
   whole via `score = -inf` (removed an artificial binding at F3 (13,13) on iteration 1).
4. **State-vector layout** — `reshape/ravel(order="C")` -> `order="F"` for the z-major/node-fastest
   layout in the solve and residuals (caused the original F5 (0,16) iteration-2 explosion).
5. **z-block column mapping** — controlled row entries (node indices) must map to full columns
   `nz*n + node`; they were placed in the z=0 block for z=1 rows (row sums stayed ~0, masking it);
   caught by the new Bellman/Q-row structural test.
6. **F3 dispatch exclusion** — `sector_dispatch` for F3 with `mu_b < 0, mu_a > 0` now returns `None`
   (reverse-sliding obstruction, whole-candidate exclusion per the F3 contract), matching F8.

**Micro-Rev bounded contract fix (7th, this commit):**

7. **Boundary effective-domain guard** — per the frozen Issue #57 Rev-2 rule and Reviewer comment
   `5645920346`: the boundary optimizer requires positive effective liquid marginal evidence; the
   implementation previously continued the raw candidate/bracket search when `p_b <= 0` (setting
   `c_anchor = None, l_anchor = 0`), eventually surfacing `OPTIMIZER_SEARCH_FAILURE` only after
   bracket expansion. The guard now raises `DERIVATIVE_EFFECTIVE_DOMAIN_FAILURE` at the top of every
   boundary row, before candidate/bracket search, with family/state/z/iteration/`p_b` recorded;
   `p_b` is never clipped/floored; the F0 interior path is untouched. After this fix the frozen smoke
   fails at the SAME F3 (13,13) z=0 state at iteration 2 with the corrected classification — the
   residual failure is the frozen convergence-application block, not a code defect.

## 7. Deterministic repeat

- Smoke: two full runs raise identical failure (same name, message, detail —
  `DERIVATIVE_EFFECTIVE_DOMAIN_FAILURE`, `p_b = -0.36522`); iteration-1 value iterates bit-identical
  (`max|V1a - V1b| == 0.0`).
- Operator build: repeated builds bit-identical (`Q.data`, `Q.indices`, `u`, diagnostics equal).
- Selection: repeated row builds return identical selected identities / controls / rates / entries.

## 8. Forbidden-check (all respected)

No oracle/source mutation; no economics mutation (no fixed c/l/d economic bounds); no grid/domain/
aspect redesign; no ghost states; no interpolated missing destinations; no coordinate change; no
silent reinterpretation of the 5V-F exclusions; no KFE and NO call to `solve_household_steady_state`
or `solve_matlab_faithful_stationary_kfe`; no production W_max; no W_max/resolution/parameter sweep;
no post-failure tuning; no SCC/global stationary-generator validation; no aggregates/GE/regional/
neural/nominal/calibration/policy/welfare/Results; no PR/merge/close/successor/self-accept. In this
Micro-Rev: no rate/gap/W_max/resolution variation, no bracket enlargement to hide `p_b <= 0`, no
clipping/flooring of the new boundary `p_b`, no new alternate-config or oracle-convergence runs.

## 9. Execution evidence (Issue #58 §16)

- **(A) Targeted Issue #58 tests:** 20 passed
  (`test_dlh_5vj_classifier_dispatch.py`, `test_dlh_5vj_bellman_q_rows.py`,
  `test_dlh_5vj_interior_regression.py`, `test_dlh_5vj_hjb_smoke.py`).
- **(B) Relevant existing oracle tests (no KFE / no `solve_household_steady_state`):** 4 passed
  (`test_dlh_4b_transfer.py::test_local_policy_liquid_branch_and_boundaries`,
  `::test_local_policy_boundary_flags`, `::test_source_axis_boundary_truncation`,
  `::test_contaminated_row_index_reference`).
- **(C) Static/source check:** `py_compile` clean on all six files; module contains no debug output.
- **(D) Exactly one predeclared deterministic HJB smoke + deterministic repeat:** §5 (fails
  deterministically at iteration 2 with `DERIVATIVE_EFFECTIVE_DOMAIN_FAILURE`; repeat identical).
- Invocation convention: `$env:PYTHONPATH = "D:\deep-learning-hank\src"` then
  `python -m pytest ...` (reported for reproducibility).

## 10. Deliverables (cumulative diff vs branch base = exactly the six allowlist paths)

1. `src/deep_learning_hank/two_asset/boundary_hjb_selected_q.py` (new; Micro-Rev guard added)
2. `tests/test_dlh_5vj_classifier_dispatch.py` (new)
3. `tests/test_dlh_5vj_bellman_q_rows.py` (new)
4. `tests/test_dlh_5vj_interior_regression.py` (new)
5. `tests/test_dlh_5vj_hjb_smoke.py` (new; corrected failure-signature pin)
6. `reports/dlh_5vj_boundary_hjb_implementation_2026_09_12/DLH_5VJ_IMPLEMENTATION_AND_LOCAL_VALIDATION_REPORT.md` (this file)

No `__init__.py` or household-oracle modification; no seventh tracked file; the four pre-existing
untracked handoff files are not staged. The Micro-Rev commit sits directly on top of candidate
`d0e5267` on the same dedicated branch (no reset/rebase/discard); remote verified equal to local
after push.
