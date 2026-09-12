# DLH-5V-I — HJB Iteration Integration and Validation Plan (Issue #57)

**Report 5 of 6** — `DLH_5VI_HJB_ITERATION_AND_VALIDATION_PLAN.md`

This report freezes the integration of the boundary candidate/scoring/Q-row contract into the
accepted implicit/pseudo-time HJB iteration structure, the convergence/residual/failure
semantics, and the staged validation hierarchy for the future implementation gate.
Issue §10, §11, §12. Design only — no implementation, no production execution.

---

## 1. Accepted iteration pattern (consumed, read-only)

The accepted oracle (`solve_matlab_faithful_hjb`) iterates:

```text
for iteration = 1..max_iterations:
    policy / rates from current value iterate (accepted interior local-policy path)
    operator = assemble(axis rates) + switch_matrix (z-switch via kron)
    matrix = (1/delta + rho)*I - operator.full
    rhs    = utility + V_old/delta
    V_new  = spsolve(matrix, rhs)
    statistic = max|V_new - V_old|            (iterate change)
    converged = statistic < convergence_tolerance
post-convergence: recompute policy/rates from final V (upwind max(mu,0)/step)
```

The boundary production scheme **preserves this outer structure** (same pseudo-time implicit
step, same `delta` semantics initially, same iterate-change statistic) and replaces the
**operator rows of the boundary families** with the conservative candidate/Q rows, leaving the
accepted interior-path rows unchanged.

## 2. State-path ownership (Issue §10; Micro-Rev — local vs global semantics fixed)

- **States retaining the accepted interior path (unchanged local rows):** family F0
  (interior / W-inactive) — the accepted MATLAB-faithful local-policy selection with its
  accepted floors/masks and upwind axis rates. **Local semantics:** for the SAME input value
  array `V`, the F0 family classification, local derivative inputs where directly comparable,
  local policy computation, `(c, l, d)`, utility, drifts, controlled rates and controlled
  sparse row are **unchanged by construction** from the accepted interior/oracle path
  (Gate 1A common-input regression). **Global semantics (NOT claimed):** the F0 full value
  iterates or converged policies are NOT asserted bit-identical to the old full-domain oracle,
  because changing boundary rows changes the global sparse system and can propagate into
  interior `V`; any interior difference is a Gate-1B boundary-influence/localization
  diagnostic, not an automatic regression failure.
- **States using the new boundary path (new candidate/scoring/Q rows):** families
  F1 (regular W-active), F2/F3 (lower/upper-a × W endpoint bands + faces), F4 (b_min × W
  W-contact), F5/F6/F7 (non-W faces), F8 (residual W-active regular-band cells),
  F9/F10/F11 (corners incl. symbolic triple corner). For these rows the selected candidate
  determines the represented destinations and rates via the state-family + Bellman contracts;
  **no axis truncation and no lost-diagonal exit** (conservative rows).
- **Mixed-row states:** none — the partition is by family; every state is exactly one of
  (interior path, boundary path).
- **Z-switch assembly:** the accepted `grid.switch_matrix` (`kron(switch_matrix,
  eye(state_size))` — the exogenous switching generator supplied to the oracle) is added to
  BOTH path types identically; switching transitions are exogenous and do not depend on the
  selected candidate (Bellman report §1). No double counting (Bellman report §1).
- **Sparse operator composition:** `Q_selected = Q_controlled_rows(boundary ∪ interior) +
  B_switch`, where the boundary rows use the selected-candidate conservative construction and
  the interior rows use the accepted interior rates; the composition is a single sparse
  matrix in the oracle's `(b, a, z)` layout.

## 3. Iteration contract (Issue §10 — frozen)

```text
[(1/delta + rho)*I - Q_selected(V_old)] V_new = u_selected(V_old) + V_old/delta
```

1. **Initial `delta` semantics:** preserve the accepted source's `delta` semantics initially
   (same parameter meaning, same role as the pseudo-time step); the implementation gate may
   only change `delta` under a documented schedule with re-validation (no silent tuning to
   force convergence).
2. **Candidate selection per iteration:** each iteration recomputes the family classification
   (static by geometry — computed once), the effective-gradient evidence, the candidate
   search, ONE selection, and the selected Q rows from the CURRENT iterate `V_old`
   (policy iteration pattern, matching the accepted oracle's per-iteration policy update).
3. **Convergence statistic (iterate change):** `max|V_new - V_old| < tolerance_iter`
   (accepted semantics; kept separate from the Bellman residual — the two metrics are NOT
   collapsed into one).
4. **Policy-evaluation (fixed-policy) residual — per-iteration diagnostic:** because
   `Q_selected` and `u_selected` are chosen from `V_old`, the quantity
   ```text
   R_policy_iter = (rho*I - Q_selected(V_old)) V_new - u_selected(V_old)
   ```
   is a **fixed-policy / policy-evaluation residual** of `V_new` under the OLD selection — it
   is NOT the Bellman residual of `V_new`. This name and interpretation are frozen; the
   quantity may be reported each iteration as a diagnostic only.
5. **Final Bellman residual (mandatory, after convergence):** take the final `V`; recompute
   derivative / effective-gradient evidence; regenerate candidates; redo ONE global selection;
   rebuild `u_selected(V)` and `Q_selected(V)` from the final `V` (same selected candidate,
   same rates); then compute
   ```text
   R_Bellman(V) = rho*V - [ u_selected(V) + Q_selected(V) V ]
   ```
   The future implementation gate MUST predeclare `tolerance_Bellman`, and acceptance requires
   the declared Bellman residual criterion (e.g. `||R_Bellman(V)||_inf <= tolerance_Bellman`)
   — "finite residual" alone is NOT an acceptance criterion. Iterate-change convergence and the
   final Bellman residual are separate, both required.
6. **Max-iteration failure:** reaching `max_iterations` without the tolerance →
   `HJB_NONCONVERGENCE` (failure taxonomy).
7. **Linear-solve failure:** non-finite or singular `(1/delta + rho)I - Q_selected` →
   `HJB_LINEAR_SOLVE_FAILURE`.
8. **Policy / family switching diagnostics near convergence:** record the per-state sequence
   of selected candidates and family memberships over the last K iterations; a state whose
   selection oscillates between candidates (or families) above a declared threshold while the
   value iterate change is below tolerance is reported as a convergence-quality diagnostic
   (policy instability) — NOT silently resolved by averaging.
9. **Post-convergence recomputation (mandatory):** after convergence, recompute from the final
   `V`: family classification, effective-gradient evidence, candidate search, ONE selection,
   selected rates, and the final conservative Q rows. Reported policies/controls/rates/drifts
   and the final Q are those of the final `V` (generalizing the accepted post-convergence
   operator recomputation); the FINAL BELLMAN RESIDUAL (§5 above) is evaluated with the final
   Q and checked against `tolerance_Bellman`.
10. **No analytic value function required** — the acceptance evidence is numerical
    (convergence, final Bellman residual, policy/drift diagnostics, regression, robustness).

## 4. Failure taxonomy wiring (Issue §12)

Every failure name of the Bellman report §7 is wired to a stage of the iteration: candidate
generation (`SCIENTIFIC_ADMISSIBILITY_FAILURE`, `REPRESENTATION_FAILURE`), search
(`OPTIMIZER_SEARCH_FAILURE`), derivative evidence
(`DERIVATIVE_EFFECTIVE_DOMAIN_FAILURE`), row assembly (`GENERATOR_CONSERVATION_FAILURE`),
linear step (`HJB_LINEAR_SOLVE_FAILURE`), iteration cap (`HJB_NONCONVERGENCE`), validation
(`REGRESSION_FAILURE`). A failure halts the run with an explicit object; no automatic
clipping, normalization, or fallback.

## 5. Validation hierarchy for the future implementation gate (Issue §11; Micro-Rev — Gate 1 split)

### Gate 1A — exact local / common-input regression (the genuine regression gate)

- **Scope:** the F0 state set (interior / W-inactive), evaluated on a **common frozen value-array
  input `V`** (same input array for the boundary scheme and the accepted oracle path).
- **Requirement (per state, on the common input):** family classification; local derivative
  inputs where directly comparable; local policy computation; `c, l, d`; utility;
  `mu_a, mu_b`; controlled rates; controlled sparse row; z-switch row contribution where
  applicable — must match the accepted interior/oracle path to the declared semantics:
  exact equality where the computation is purely mechanical (e.g., family classification,
  rate formulas), otherwise predeclared numerical tolerances. Failure here:
  `REGRESSION_FAILURE`.
- **Also:** sparse-operator identity check that the boundary-path rows do not alter any F0
  row.

### Gate 1B — global solution / boundary-influence diagnostic (NOT a regression gate)

- **Context:** after a future full boundary-HJB run, interior values/policies MAY differ from
  the old full-domain oracle because the boundary rows changed (the global sparse solve
  couples states).
- **Requirement:** compare interior `V`/policies ONLY as a boundary-influence / localization
  diagnostic: predeclare the interior comparison subset (distance-from-boundary rule) and the
  tolerances; report spatial decay / localization where appropriate.
- **Explicitly NOT:** any interior difference is NOT automatically `REGRESSION_FAILURE`
  merely because boundary rows changed. No wording asserts that F0 full value iterates or
  converged policies must be bit-identical by construction.

### Gate 2 — local boundary algebra + exactly-one family/dispatch checks

- **Scope:** representative states of every family F1–F11 (including the 5V-F obstruction
  classes and the symbolic `W_max = 8` triple-corner cells, at the declared production `m`).
- **Checks (per family):** candidate admissibility against the active tangent laws; **exactly
  one family per represented state and exactly one candidate-contract dispatch per admissible
  drift-sign class** (re-run of the classifier truth-table logic at the production `N_m`);
  sector membership uniqueness; destinations represented; rates nonnegative; exact first
  moment `sum q (x_r - x_s) = mu(s, alpha)` (controlled part) within the drift tolerance;
  selected-score recomputation equals the maximizer score; conservative row checks (Bellman
  report §6); deterministic repeat; obstruction-cell behavior verified against the recorded
  5V-F certificate (excluded candidates are exactly the certified unrepresentable rays; no
  diagonal-escape retention).

### Gate 3 — deterministic finite-domain HJB smoke

- **Configuration:** ONE predeclared small/validation configuration (declared in the
  implementation gate; `m` and `W_max`-family fixed as a validation instance, NOT a
  production `W_max` selection).
- **Required outcomes:** numerical HJB **iterate convergence** (`tolerance_iter` met within
  `max_iterations`); **final Bellman residual `R_Bellman(V) = rho V - [u_selected(V) +
  Q_selected(V) V] <= tolerance_Bellman` with the predeclared tolerance** (post-convergence
  re-selection from final `V`); finite `V` everywhere; `c > 0`; finite `l, d`, drifts;
  conservative selected `Q` (all structural checks pass); **no bracket-binding artifact** (all
  accepted selections strictly inside brackets, or declared genuine economic equalities);
  **deterministic repeat** of the whole run (same inputs ⟹ same selected candidates, same
  final `Q`, same residual within declared semantics).

### Gate 4 — rate diagnostic / robustness cases

- Owner empirical guidance may be used to choose **diagnostic** cases near `r_b = 0.02` and
  selected `r_a` inside approximately `(0.05, 0.12)`; every such case is labelled
  `DIAGNOSTIC / VALIDATION`, NOT calibration.
- Requirements: (a) the cases exercise representative families and the diagnostics of the
  Bellman report §5 (finite derivatives, `V_b^eff > 0` where required, no localization
  failure, conservative rows); (b) no parameter sweep in this design gate; (c) robustness
  evidence at other rates is neither claimed nor required by these cases; (d) passing only in
  the Owner-experience interval is NOT proof of global stability (explicitly recorded).

### Gate 5 — resolution / `W_max` work remains downstream

- Numerical production `W_max` selection, nested `W_max` adequacy (DLH-5T protocol), and
  resolution robustness are **downstream roadmap gates** after implementation and
  same-process `Q` validation. This design gate selects no `W_max` and runs no nested study.

## 6. Design-readiness statement

The architecture is unambiguous at the design level: exhaustive family classifier; candidate
admissibility/representability; search-bracket semantics; derivative/effective-domain
diagnostics; Bellman score + ONE selection; conservative ONE backward Q row with structural
checks; iteration integration with the accepted implicit/pseudo-time pattern; validation
hierarchy Gates 1–5; failure taxonomy with no silent fallback. The frozen unbounded-control
theory ceiling (Issue #56 Outcome B) remains explicit and is not claimed solved. No new
scientific contradiction with the accepted process was discovered in this gate.
