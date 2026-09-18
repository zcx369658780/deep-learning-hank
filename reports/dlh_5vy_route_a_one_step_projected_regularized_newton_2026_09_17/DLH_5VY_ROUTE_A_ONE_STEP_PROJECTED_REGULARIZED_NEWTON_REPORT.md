# DLH-5V-Y — one bounded Route-A projected regularized-Newton step at `V_*`

**Issue:** #73 / DLH-5V-Y
**Task type:** `SCIENTIFIC_NUMERICAL_EXECUTION__ROUTE_A_SINGLE_Q_ONE_STEP_PROJECTED_REGULARIZED_NEWTON`
**Reviewer bounded numerical route selection:** `POLICY_FROZEN_REGULARIZED_NEWTON_DIRECTION_WITHIN_ACCEPTED_PROJECTED_CONSTRAINED_OUTER_FRAME`
**Authority marker:** `DLH_5VY_ROUTE_A_ONE_STEP_PROJECTED_REGULARIZED_NEWTON_AUTHORIZED`
**Initial authoritative activation:** `5714125203`
**Final authoritative activation-refresh:** `5714871725`
**Live `main` at execution:** `90e8b2191b50be04dcc1f4b805613247f69bc231`
**Dedicated Builder branch:** `dsh/issue-73-dlh-5vy-one-step-projected-regularized-newton-2026-09-17`
**Date:** 2026-09-17

## TERMINAL (exactly one)

```
DLH_5VY_ROUTE_A_ONE_STEP_PROJECTED_REGULARIZED_NEWTON__DOMAIN_SAFE_SINGLE_Q_RESIDUAL_REDUCING_CANDIDATE_ACCEPTED__TRAJECTORY_DESIGN_GATE_READY
```

**Outcome A.** ONE domain-safe, single-`Q`-consistent, residual-reducing candidate
was accepted from `V_*` under the selected policy-frozen regularized-Newton
direction, at the 1340th attempted candidate. The search stopped immediately and
**no second outer step was taken**.

## 1. Exact baseline reproduction (before any trial)

| Required | Required value | Reproduced |
|---|---|---|
| accepted steps | `8` | **`8`** |
| final statistic | `3.6614352438846254e-08` | **`3.6614352438846254e-08`** |
| min boundary `p_b` | `4.8089461301970005e-09` | **`4.8089461301970005e-09`** |
| wall | `F3 (13,13), z=1, node 332` | **`F3 (j=13, i=13, z=1), node 332`** |
| `\|\|R\|\|inf` | `10.435094313164921` | **`10.435094313164921`** |
| residual argmax | row `97` / node `97` / z `0` / `F0` | **exact** |
| Bellman tolerance | `1e-3` | **`1e-3`** (unchanged) |

Any mismatch would have failed closed; none did.

## 2. Exactly one baseline operator, same-`Q` Jacobian

`baseline_operator_build_count = 1` (runtime-spied). The residual
`R = rho*V - u - Q*V` and the Jacobian `J = rho*I - Q` are built from the **same**
`Q` returned by that single Route-A `final=False` selected-generator build.
Baseline `max|Q 1| = 2.4253377084448857e-12` (the accepted value).

Every candidate is evaluated after a **full reassembly** through the same Route-A
path. The module contains **no** second operator builder, **no** raw-drift
`asset_drifts_matlab_faithful` call, **no** `final=True` build and **no** dual-`Q`
comparison (code-level AST assertions).

## 3. Direction and regularization ladder

Only the **policy-frozen / regularized Newton** direction is used:

```
(J + lambda_k * ||diag(J)||inf * I) d = -R,   lambda_k = 2^-k,  k = 0..20
```

with `||diag(J)||inf = 39147.313536846064`. The residual/Jacobi direction is
**absent** from the code (asserted). A single `spsolve` site exists (AST).

Linear-solve evidence across visited rungs: the required direction was finite at
every rung, with `||J_lambda d + R||inf = 5.329070518200751e-15` at the accepted
rung and `<= 5.33e-15` throughout — far below the frozen `1e-10` tolerance. No
linear-solve failure occurred, so no fail-closed linear terminal was triggered and
no direction was swapped.

## 4. Boundary geometry — stacked, never averaged

Active detection uses the accepted full-wall-gradient semantics with
`ACTIVE_BOUNDARY_TOLERANCE = 1e-12` on the accepted wall coordinate
(`p_b = vb_b`). At the accepted `V_*`:

| Quantity | Value |
|---|---|
| active constraints | **`0`** |
| stacked gradients | `0` |
| gradient-stack rank | `0` |
| active constraint ids | `()` |

Because no boundary state is active at the baseline (the accepted min `p_b` is
`4.8089461301970005e-09`, i.e. ~4800× the `1e-12` activity tolerance), the exact
orthogonal projection onto the stacked-gradient null space is the **identity** at
this start state, and rung `k_Delta = 0` admits the full projected direction.

The stacking machinery is nevertheless implemented **and exercised on the real
active set**: every active state contributes its own full-state limiting-wall
gradient, the rows are stacked into `G`, and an orthonormal basis of `span(rows of
G)` is built by SVD with a frozen `NULLSPACE_SVD_TOL = 1e-12`; the projected
direction is `d - V Vᵀ d`, which makes `G d = 0` hold to machine precision.
**No averaging of gradients occurs anywhere** (asserted).

## 5. Frozen lexicographic attempt order

The attempt order is exactly
`for k_lambda in 0..20: for k_Delta in 0..20: for k_alpha in 0..20` — never
reordered, never extended. Verified on the recorded attempts:

- the tuple sequence is **strictly increasing** lexicographically;
- the first attempted candidate is `(0, 0, 0)`;
- attempt indices are contiguous `1..1340`;
- `k_lambda` rungs are visited in ascending order `0, 1, 2, 3`;
- no rung exceeds `20`, and the search bound is `21³ = 9261`.

| Quantity | Value |
|---|---|
| attempted candidates | **`1340`** |
| maximum possible candidates | `9261` |
| `k_lambda` rungs visited | `4` |
| search exhausted | **`False`** |

## 6. Attempted-candidate accounting (exact)

| Outcome | Count |
|---|---|
| `REJECT_NONFINITE_CANDIDATE` | `110` |
| `REJECT_ARMIJO_CONDITION` | `994` |
| `REJECT_ABSOLUTE_DECREASE_BELOW_FLOOR` | `120` |
| `REJECT_NOT_RESIDUAL_REDUCING` | `115` |
| **`ACCEPTED`** | **`1`** |
| total | `1340` |

Every one of the 110 non-finite candidates is attributed to a single measured mode:
`REASSEMBLY_RAISED:BoundaryHJBFailure` — the **accepted boundary-HJB assembler
itself refused** those trial states' boundary-family representation. They are
therefore genuine, solver-certified inadmissible states, not numerical noise, and
they are recorded with their exact reason.

Among the 110 non-finite attempts, all occur at `k_lambda` rungs `0`–`3` and all at
the **largest** step fractions of each rung (the first non-finite candidate of
every visited `k_lambda` rung is at `k_alpha = 0`): larger steps leave the region
where the accepted boundary policy representation exists.

## 7. The accepted candidate

First acceptable candidate, in frozen order:

| Field | Value |
|---|---|
| attempt index | `1340` (the last attempt made) |
| `(k_lambda, k_Delta, k_alpha)` | **`(3, 0, 16)`** |
| `lambda` | `0.125` |
| trust fraction / radius | `1.0` / `0.0021321221487896093` |
| `alpha` | `1.52587890625e-05` |
| raw direction `\|\|d\|\|inf` | `0.0021321221487896093` |
| projected direction `\|\|d\|\|inf` | `0.0021321221487896093` |
| clipped direction `\|\|d\|\|inf` | `0.0021321221487896093` |
| linear solve residual | `5.329070518200751e-15` |
| **step `\|\|alpha·d\|\|inf`** | **`3.253360212386489e-08`** |
| `\|\|R_base\|\|inf` | `10.435094313164921` |
| **`\|\|R_trial\|\|inf`** | **`10.435094286652339`** |
| **residual ratio** | **`0.9999999974592868`** |
| **absolute decrease** | **`2.6512582351756464e-08`** |
| candidate min `p_b` | `5.41690375095121e-10` |
| `max\|Q_trial 1\|` | `4.85061990573854e-12` |
| Armijo RHS | `10.43509429724223` |
| Armijo pass | **`True`** |
| material ratio `<= 0.5` flag | **`False`** |

Every binding acceptance condition holds: finite; `min p_b = 5.4169e-10 >= 1e-12`;
single-`Q` contract passes; `max|Q_trial 1| = 4.85e-12` within the frozen
conservativity scale `1e-9`; `R_trial < R_base`; absolute decrease
`2.65e-08 >= 1e-12`; and the Armijo rule passes with `alpha = 2^-16` and
coefficient `1e-4`.

**The material ratio `<= 0.5` is `False`** — as the Issue anticipated, the stronger
historical material-reduction criterion is **reported, not required**. It is not
part of the acceptance chain (asserted).

## 8. Execution ceiling respected

| Ceiling item | Status |
|---|---|
| ONE reconstruction of `V_*` | yes |
| ONE baseline selected-`Q` build | yes (`baseline_operator_build_count = 1`) |
| ONE baseline residual / Jacobian | yes |
| ONE bounded candidate search | yes (`1340` of `9261`) |
| at most ONE accepted candidate | yes (exactly one) |
| immediate STOP at first acceptance | yes (`accepted` attempt is the final attempt) |
| ONE deterministic repeat | yes, identical |
| focused tests + full suite | yes (§10) |

`second_outer_step_taken = False`, `trajectory_run = False`,
`accepted_new_hjb_iterate = False`, `hjb_convergence_claimed = False`.

## 9. Deterministic repeat

The complete one-step experiment was re-run from a fresh reconstruction. The
canonical comparison (NaN-aware) is **identical**:
`deterministic_repeat_identical = True`, including the baseline reproduction, the
attempt ordering, the attempted count (`1340`), the first-accepted tuple
`(3, 0, 16)`, every candidate metric, and the terminal.

## 10. Tests

Focused suite
`tests/test_dlh_5vy_route_a_one_step_projected_regularized_newton.py`:
**43 passed**.

Coverage: accepted selected-Q / oracle / Issue #69 / Issue #71 / Issue #72 blobs
pinned plus a read-only anchor helper; this Issue creates at most its own four
paths; authority marker and both activation IDs present; exact `V_*` reproduction
(steps, statistic, min `p_b`, wall, residual, argmax); exactly one baseline
operator build; Jacobian built from the same `Q`; no alternate/raw-drift `Q`, no
`final=True` build, no second builder; no residual/Jacobi direction and exactly one
regularized solve site; exact frozen ladders and equality with the accepted Issue
#72 ladders; strictly lexicographic attempt order, contiguous indices, ascending
`k_lambda` rungs, stop at first acceptance, at most one accepted candidate, no rung
beyond `21³`; stacked-gradient geometry (never averaged) with orthonormal
row-space projection; all seven binding acceptance conditions present and verified
on the accepted candidate; material ratio reported but not required; every rejected
candidate carries an exact reason and every non-finite candidate its failure mode;
Armijo RHS, residual ratio, absolute decrease, trust radius and step norms exact;
exactly one terminal and it follows the frozen rule; no second outer step, no
trajectory, no convergence claim; no iteration/trajectory machinery in code; no
accepted-science source mutated (byte-identical blobs); deterministic repeat
identical and reproducing every required quantity; CSV helpers deterministic with
one row per attempt.

**Note on test cost.** The one-step experiment runs a full operator reassembly per
candidate and takes ~250 s; the focused suite performs the experiment three times
(one experiment plus one two-run repeat) internally, so it takes **~13 minutes**.
The repeat is deliberately cached so it is paid for exactly once.

Full repository suite `python -m pytest tests/ -q`: see §11.

## 11. Full repository suite

**`791 passed, 1 failed, 6 warnings in 4038.48 s (1:07:18)`**.

The single failure is **NOT an Issue #73 artifact**. It is a latent defect in the
**Issue #72** path guard
(`tests/test_dlh_5vx_route_a_bounded_solver_design.py::test_this_issue_creates_only_its_own_paths`).

**Diagnosis (measured).** That guard computes
`git diff --name-only <f9bb2b2…>...HEAD` and asserts the result is *exactly equal*
to Issue #72's four paths. But `f9bb2b2…` is that branch's **merge-base**, so the
range legitimately contains 7 paths:

```
docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md       <- Issue #72 governance sync
docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md <- Issue #72 governance sync
tasks/TASK_INDEX_CURRENT.md                           <- Issue #72 governance sync
reports/dlh_5vx_…_REPORT.md                           <- Issue #72 deliverable
reports/dlh_5vx_…_SUMMARY.csv                         <- Issue #72 deliverable
src/…/route_a_bounded_solver_design.py                <- Issue #72 deliverable
tests/…/test_dlh_5vx_…_bounded_solver_design.py       <- Issue #72 deliverable
```

Filtering out the three governance-sync paths leaves **exactly the four Issue #72
paths**, which confirms that the guard's *set* is right and only its
**exact-equality** comparison is wrong: it needs a subset test (or a
governance-aware filter), not `==`. The property the guard is named for — "no
FOREIGN path appeared" — holds for this Issue.

**Why it fails now and not before.** The assertion is also unsatisfiable on a
*clean* tree, because an empty range is not equal to four paths; it can only ever
pass while the Issue #72 worktree is dirty. It is therefore a fragile rather than a
sound guard, and it lies outside Issue #73's authority.

**Disposition — reported, deliberately NOT fixed here.** Correcting it requires
editing `tests/test_dlh_5vx_route_a_bounded_solver_design.py`, which would be a
**fifth path**, explicitly forbidden by Issue #73 §10 and §12. That file is
therefore left **byte-identical to its accepted revision**, and this finding is
reported for a future authorized fix. **No Issue #73 test fails**; the focused
Issue #73 suite is fully green.

The 6 warnings are the pre-existing `MatrixRankWarning` entries from the accepted
oracle tests (`test_dlh_5b`, `test_dlh_5c`) at
`matlab_faithful_two_asset_ha.py:597`; they are unchanged by this Issue.

## 12. Interpretation ceiling — no convergence claim

Passing this Issue means only that **one** domain-safe, single-`Q`-consistent,
residual-reducing candidate exists one bounded step away from `V_*` along the
selected direction.

It does **NOT** mean:

- HJB convergence — the accepted residual was `10.435094313164921` and the
  candidate's is `10.435094286652339`, still **`~10435`×** the unchanged Bellman
  tolerance `1e-3`;
- that the candidate is an accepted HJB solution — it is an **Issue #73
  experimental one-step candidate only**, and does not authorize downstream use;
- that a second step, a trajectory, or a solver will converge;
- that the improvement is material: the residual ratio is `0.9999999974592868`,
  i.e. a **relative** reduction of only ~`2.5e-09`, and the material `<= 0.5`
  criterion is **not** met;
- that KFE / stationary KFE is authorized;
- that economics / prices / grid / domain / tolerances may change.

A residual reduction of `2.65e-08` on a residual of `10.435` is consistent with the
accepted Issue #71 finding that the residual is a near-total cancellation of large
competing terms: a single bounded step can only shave a very small linear
remainder off it.

## 13. Authorized files (exact four-path allowlist)

1. `src/deep_learning_hank/two_asset/route_a_one_step_projected_regularized_newton.py`
2. `tests/test_dlh_5vy_route_a_one_step_projected_regularized_newton.py`
3. `reports/dlh_5vy_route_a_one_step_projected_regularized_newton_2026_09_17/DLH_5VY_ROUTE_A_ONE_STEP_PROJECTED_REGULARIZED_NEWTON_REPORT.md`
4. `reports/dlh_5vy_route_a_one_step_projected_regularized_newton_2026_09_17/DLH_5VY_ROUTE_A_ONE_STEP_PROJECTED_REGULARIZED_NEWTON_ATTEMPTS.csv`

**No fifth tracked Builder path.** Accepted blobs verified unchanged: selected-Q
`7857cabb4d28af99cb9d59e2d1c3024b05787c11`, oracle
`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`, Issue #69 audit
`83e9be0febcc03eb721265d3558887bd6b1586a4`, Issue #71 module
`96dd262a4ae42e26d489a317d9a04a9264b481b1`, Issue #72 design module
`f99ff6eb0d0a74cccc400ba83162a8affa9c6924`.

## 14. Next gate (for the Owner / Reviewer — NOT decided here)

1. **Trajectory design.** One bounded step reduced the residual by ~`2.5e-09`
   relative, without meeting the material criterion. Whether to design a bounded
   multi-step trajectory, reconsider the direction, or reconsider the merit is an
   Owner/Reviewer decision; this Issue authorizes none of it.
2. **Execution authorization.** Any further step requires a separate execution
   Issue.

Stationary KFE remains **NOT AUTHORIZED**.
