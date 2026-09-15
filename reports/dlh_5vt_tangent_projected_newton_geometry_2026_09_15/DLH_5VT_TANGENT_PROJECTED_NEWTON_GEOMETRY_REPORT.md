# DLH-5V-T — Single-wall tangent-projected frozen-policy Newton geometry after the accepted final-validation repair

**Issue:** #68 / DLH-5V-T
**Task type:** `SCIENTIFIC_NUMERICAL_DIAGNOSTIC__BOUNDARY_TANGENT_PROJECTED_NEWTON_GEOMETRY_AFTER_VALIDATION_REPAIR`
**Route decision:** `APPROVE_SINGLE_WALL_TANGENT_PROJECTED_NEWTON_GEOMETRY_AFTER_5VS_TERMINAL_A`
**Authority marker:** `DLH_5VT_TANGENT_PROJECTED_NEWTON_GEOMETRY_AUTHORIZED`
**Initial authoritative activation:** `5674754187`
**Final authoritative activation-refresh:** `5675003122`
**Post-sync live `main`:** `e569271904eacbd3b2721b0b0f1ebb8e9a559e3f`
**Dedicated Builder branch:** `dsh/issue-68-dlh-5vt-tangent-projected-newton-2026-09-15`
**Date:** 2026-09-15

## TERMINAL (exactly one)

```
DLH_5VT_TANGENT_PROJECTED_NEWTON__TANGENT_DIRECTION_FINITE_AND_DOMAIN_SAFE_BUT_GEOMETRY_OR_RESIDUAL_IMPROVEMENT_INSUFFICIENT__FURTHER_DIRECTION_DESIGN_REQUIRED
```

**Outcome B.** The single-wall tangent projection is mathematically exact,
finite and domain-safe, and it **does** dramatically expand the safe geometry
(α_near / min(1, α_cross_N) = **50.55**, criterion `>= 10` satisfied). But
neither trial satisfies the dual material residual-reduction criterion
(ratios `0.9953` and `0.9906`, both far above the required `<= 0.50`), so the
combined Outcome A criterion does not hold.

## 0. Scope ceiling — what this Issue does NOT claim

- This is a local **direction-geometry diagnostic**. **No HJB convergence is
  claimed**, no convergence criterion is changed, the Bellman tolerance remains
  the unchanged `1e-3`, and the accepted residual `10.435094313164921` is still
  ~`10435`× that tolerance.
- **No trial state is an accepted HJB iterate.** Both trial states are marked
  `accepted_as_hjb_iterate = False`.
- No multi-step Newton, no policy iteration, no semismooth / trust-region /
  continuation, no adaptive line search or alpha tuning, no multiple active
  constraints, no projection-metric optimization, no `p_b` clip/floor, no
  price / Wmax / resolution sweep, no KFE / stationary KFE / steady state, no
  downstream work.
- The selected-Q source was **not** modified; its blob is asserted read-only at
  `556ccc214f03a1a22306cc4f5c7e9f7691bbf897`.

## 1. Frozen reconstruction (reproduced exactly)

| Required baseline | Required | Reproduced |
|---|---|---|
| iterations | 8 | **8** |
| final statistic | `3.6614352438846254e-08` | **`3.6614352438846254e-08`** |
| min boundary `p_b` | `4.8089461301970005e-09` | **`4.8089461301970005e-09`** |
| limiting wall | F3 (13,13), z=1 | **F3 (j=13, i=13, z=1), node 332** |
| genuine corrected residual `\|\|R\|\|inf` | `10.435094313164921` | **`10.435094313164921`** |

`R` argmax = F0, node 97, (j=3, i=2), z=0. Grid: `n = 391`, `nz = 2`,
`state_size = 782`, F0 rows = 596, required boundary states = 186.

## 2. Base operator and the ONE frozen-policy Newton solve

Exactly ONE current `final=False` operator build at `V_*`, giving `Q, u`:

```
R = rho V_* - (u + Q V_*)
J = rho I - Q
```

Exactly ONE solve `J d_N = -R`:

| Quantity | Value |
|---|---|
| `\|\|d_N\|\|inf` | `19.725548329099023` |
| Newton linear residual `\|\|J d_N + R\|\|inf` | `6.957900922088811e-11` |
| `newton_lin_res_ok` | `True` (`<= 1e-9`) |
| explicit solves / operator builds in the module | exactly `1` linalg solve, exactly `3` operator builds |

The accepted Issue #64 plain-Newton safe-fraction baseline is **reproduced
exactly** from the accepted Issue #62 semantics:

| Quantity | Accepted Issue #64 | Reproduced here |
|---|---|---|
| `alpha_cross_N` | `≈ 1.8667384893e-4` | **`1.8667388489296687e-4`** |
| limiting state | F3 (13,13), z=1 | **F3 (13,13), z=1, node 332** |

All-boundary directional accounting for `d_N`: 186 required states,
**40** zero-derivative `i == 0` states, **86** negative-derivative states.

## 3. Limiting-wall gradient

The wall state's `p_b` is the accepted regular backward finite-difference
coordinate `(V[node] - V[down]) / db`; its derivative with respect to the value
**at that state** is exactly `1/db`. The gradient is the single-entry vector

```
g[z*n + 332] = 1/db = 1/0.35 = 2.7142857142857144
```

| Requirement | Result |
|---|---|
| `g` finite | **True** |
| `\|\|g\|\|_2 > 0` | **True**, `2.7142857142857144` |
| `g @ d_N < 0` | **True**, `-50.84485675074963` |
| gradient reproduces the accepted Issue #62 derivative semantics | **exact**: basis-direction measurement of the accepted derivative map gives exactly `1/db` at the wall state |
| `i == 0` boundary derivative exactly `0` | **verified** for every `i == 0` boundary state (40 states) |

### 3.1 Recorded convention finding (transparency)

The accepted `boundary_direction_matrix` is a **coordinate map over all
required boundary states**, not a sparse linear operator on a sparse direction.
Measured basis-direction structure at the wall coordinate:

```
d = e[332, z=1] -> dp_b(332,z=1) = +1/db
d = e[331, z=1] -> dp_b(332,z=1) = -1/db        (331 is 332's backward neighbour, F0)
```

i.e. the wall's `p_b` coordinate *is* `(V[332,1] - V[331,1])/db`, and the
`-1/db` term is the **other state's own `p_b` coordinate**, not a second
derivative of the wall's `p_b`. Issue #68 section 4 specifies the gradient of
*the limiting wall's* `p_b`, whose own-state derivative is `1/db`; that literal
construction is what is implemented and reported.

For completeness, the alternative chain-rule assembly over both states
(`g[332] = 1/db`, `g[331] = -1/db`) was also measured: it changes α_cross_T to
`0.16170699931086815` (geometry ratio `866.25`) but leaves the residual plateau
essentially unchanged (`0.9193` / `0.8390`, still far above `0.50`). **The
Outcome B conclusion is therefore robust to this convention choice**; the
frozen Issue #68 convention is the one reported.

## 4. Single-wall tangent projection

Exactly ONE Euclidean orthogonal projection:

```
d_T = d_N - g * (g @ d_N) / (g @ g)
```

| Quantity | Value |
|---|---|
| `g @ d_T` | **`0.0`** (tangent identity holds exactly, tol `1e-9`) |
| `\|\|d_N\|\|inf` | `19.725548329099023` |
| `\|\|d_T\|\|inf` | `19.725548329099023` |
| `\|\|d_T - d_N\|\|inf` | `18.73231564501302` |
| `\|\|J d_N + R\|\|inf` | `6.957900922088811e-11` |
| `\|\|J d_T + R\|\|inf` | `733319.8338264916` |
| normalized normal fraction removed | `g@d_N / \|\|g\|\|_2 = -18.7323` |
| `projection_count` | exactly `1` |

Because the wall gradient is supported on a single state, the projection is an
exact one-dimensional normal subtraction: the entire wall-normal component of
`d_N` is removed precisely. This is expected to enlarge the frozen linear
residual of the projected direction, and it does (`7.33e5` vs `6.96e-11`).

## 5. All-boundary crossing geometry for `d_T`

ONE all-boundary crossing computation over the 186 required non-F0 boundary
states, with `PB_MARGIN = 1e-12`:

| Quantity | Value |
|---|---|
| required boundary states | `186` |
| zero-derivative (`i == 0`) states | `40` |
| negative-derivative states | `85` |
| `alpha_cross_T` | **`0.009436421907523617`** |
| limiting state after projection | **F3, node 333, (j=13, i=14), z=1** |
| `alpha_near = min(1, (1-EPS_ALPHA)*alpha_cross_T)` | **`0.00943641247110171`** |
| `alpha_half = 0.5*alpha_near` | **`0.004718206235550855`** |
| positive finite safe fraction exists | **`True`** |

Frozen constants honoured unchanged: `PB_MARGIN = 1e-12`, `EPS_ALPHA = 1e-6`,
`HALF_ALPHA = 0.5`, `MATERIAL_REDUCTION_RATIO = 0.50`.

**Geometry-improving criterion:** `alpha_near / min(1, alpha_cross_N)`
= `0.00943641247110171 / 1.8667388489296687e-4` = **`50.55026467396071`**
≥ `10` → **geometry-improving = True**.

No adaptive line search, no alpha tuning, no additional trial fraction: the two
fractions are exactly the frozen formulas, asserted in the test suite.

## 6. Exactly TWO diagnostic trials

For each of `alpha_half` and `alpha_near`: `V_trial = V_* + alpha*d_T`; strict
boundary safety over all 186 required states; ONE `final=False` policy
re-selection; ONE corrected `final=True` validation build under the SAME
freshly reselected current F0 controls; corrected-final vs iteration
equivalence check.

### 6.1 Trial `alpha_half` (α = `0.004718206235550855`)

| Quantity | Value |
|---|---|
| min boundary `p_b` | `0.01922419201827909` (state F3, node 345, (j=14, i=11), z=1) |
| domain safe (`> PB_MARGIN`) | **True** |
| `\|\|R_frozen_trial\|\|inf` | `3467.7103868581585` |
| `\|\|R_reselect\|\|inf` | `10.385865643798926` |
| `\|\|R_final_trial\|\|inf` | `10.385865643798926` |
| reselect ratio | **`0.9952823934419176`** |
| final ratio | **`0.9952823934419176`** |
| final-vs-iter rowwise operator gap (F0) | `7.105427357601002e-15` (`<= 1e-9`, equivalent **True**) |
| `max\|Q 1\|` reselect / final | `5.9396931817445875e-15` / `5.9396931817445875e-15` |
| sector/transfer label changes | `0` |
| max \|Δ consumption\| | `0.010180876655074833` |
| max \|Δ labor\| | `0.002983858893736313` |
| max \|Δ transfer\| | `1.208455764227867` |
| max \|Δ mu_a\| | `1.2084557642278666` |
| max \|Δ mu_b\| | `2.9581300532765393` |
| max \|Δ utility\| | `0.008400165694795958` |
| **material residual reducing** | **False** |

### 6.2 Trial `alpha_near` (α = `0.00943641247110171`)

| Quantity | Value |
|---|---|
| min boundary `p_b` | `4.831526173429016e-07` (state F3, node 333, (j=13, i=14), z=1) |
| domain safe (`> PB_MARGIN`) | **True** |
| `\|\|R_frozen_trial\|\|inf` | `6927.627830759692` |
| `\|\|R_reselect\|\|inf` | `10.336649537872423` |
| `\|\|R_final_trial\|\|inf` | `10.336649537872423` |
| reselect ratio | **`0.9905659908441556`** |
| final ratio | **`0.9905659908441556`** |
| final-vs-iter rowwise operator gap (F0) | `7.105427357601002e-15` (equivalent **True**) |
| `max\|Q 1\|` reselect / final | `1.5160095401256513e-13` / `1.5160095401256513e-13` |
| sector/transfer label changes | `0` |
| max \|Δ consumption\| | `0.020121105209693457` |
| max \|Δ labor\| | `0.005929892301609674` |
| max \|Δ transfer\| | `2.422214267550673` |
| max \|Δ mu_a\| | `2.4222142675506726` |
| max \|Δ mu_b\| | `6.394734882586073` |
| max \|Δ utility\| | `0.01675650349893676` |
| **material residual reducing** | **False** |

Both trials are strictly domain-safe, both preserve `Q` conservativity, both
show **zero** sector/transfer-label switches while continuous controls do move
(so the zero-switch count must **not** be read as unchanged controls).
`R_frozen_trial` is large (~`3.5e3` / `~6.9e3`) because the frozen `Q, u` are
being evaluated far along a direction they no longer describe — the meaningful
reduction evidence is the re-selected and corrected-final residuals.

## 7. Frozen interpretation rule and terminal derivation

- finite/consistent evidence: **yes** (`failure_detail = None`);
- tangent condition `g @ d_T ≈ 0`: **yes** (exactly `0.0`);
- both trial states boundary-safe: **yes**;
- geometry-improving (`ratio >= 10`): **yes** (`50.55`);
- at least one trial satisfying the dual material-reduction criterion
  (`reselect ratio <= 0.50` **and** `final ratio <= 0.50`): **NO**
  (best is `0.9906`);
- deterministic repeat identical: **yes**.

→ Outcome A criterion fails on residual reduction only → **Outcome B**, exactly
one terminal.

### 7.1 Scientific reading (local, trajectory-bounded)

The tangent projection achieves exactly what it was designed to achieve
geometrically: it removes the wall-normal component of the Newton direction
exactly, and the resulting safe fraction is **~50.55×** the plain-Newton safe
fraction, with the limiting state moving from the wall itself (332) to the
adjacent boundary state (333). **The geometry bottleneck identified by Issue #64
is therefore genuinely relaxed by a single-wall tangent projection.**

However, the geometry expansion does **not** translate into nonlinear residual
reduction: the policy re-selection at both trial states leaves
`\|\|R_reselect\|\|inf` at `99.06%`–`99.53%` of the accepted `\|\|R\|\|inf`. The
nonlinear residual is therefore **insensitive to stepping along the
tangent-projected direction at these admissible fractions**, and the residue is
now shown to be a property of the re-selected fixed-point map rather than of the
wall geometry alone.

This does **not** prove that no constrained direction can reduce the residual,
does not prove the HJB fixed point fails to exist, and does not authorize any
convergence-rule change or new iterate. It bounds the single-wall
Euclidean-projection hypothesis specifically.

## 8. Deterministic repeat

The full diagnostic was executed twice; every compared field is identical
(`deterministic_repeat_identical = True`), including the Newton direction, the
gradient, the projection, the crossing data, both trial states, all residual
ratios, all control-switch diagnostics and the terminal.

## 9. Tests

Focused suite `tests/test_dlh_5vt_tangent_projected_newton_geometry.py`:
**33 passed**.

Coverage: exact post-repair `V_*` reconstruction; selected-Q repaired blob
exactness (via `git rev-parse HEAD:<path>`); exact `R` reproduction; exactly ONE
Newton solve and ONE base operator build (runtime spy: 3 `final=False` and 2
`final=True` builds); Newton equation residual; accepted Issue #62 boundary
derivative semantics with exact basis-direction measurement; `i == 0` derivative
exactly zero; `g` finite/nonzero; `g @ d_N < 0`; plain-Newton historical
baseline reproduction; implicit `g @ d_T ≈ 0` (exactly zero); exact projection
closed form; all-boundary crossing determinism; exact alpha formulas with no
adaptive search; exactly two trial states with frozen labels; strict boundary
safety; ONE re-selection and ONE final validation build per trial (runtime spy);
corrected-final vs iteration equivalence per trial; residual ratios and
control-switch diagnostics; conservativity; material-reduction flag matching the
frozen rule; no accepted iterate and no convergence claim; fail-closed on
non-finite direction, degenerate gradient and boundary-safety violation; static
AST scan for forbidden machinery (exactly one `spsolve`, exactly three operator
builds); exactly one terminal.

Full repository suite `python -m pytest tests/ -q`: **567 passed, 0 failed,
6 warnings in 3418.10 s (0:56:58)**. The 6 warnings are the pre-existing
`MatrixRankWarning` entries from the accepted oracle tests (`test_dlh_5b`,
`test_dlh_5c`), not failures.

## 10. Authorized files (exact four-path allowlist)

1. `src/deep_learning_hank/two_asset/tangent_projected_newton_geometry.py`
2. `tests/test_dlh_5vt_tangent_projected_newton_geometry.py`
3. `reports/dlh_5vt_tangent_projected_newton_geometry_2026_09_15/DLH_5VT_TANGENT_PROJECTED_NEWTON_GEOMETRY_REPORT.md`
4. `reports/dlh_5vt_tangent_projected_newton_geometry_2026_09_15/DLH_5VT_TANGENT_PROJECTED_NEWTON_GEOMETRY_SUMMARY.csv`

No fifth tracked Builder path. All accepted sources/tests/reports/governance
remain byte-identical to their accepted blobs; the selected-Q repaired blob
`556ccc214f03a1a22306cc4f5c7e9f7691bbf897` is unchanged.

## 11. Next gate (for the Owner / reviewer — NOT decided here)

The single-wall Euclidean tangent projection relaxes the wall geometry by ~50×
but leaves the nonlinear residual at ~99% of its accepted value. Any further
work — a different projection metric, multiple active constraints, a
residual-driven constrained direction, or a reassessment of the residual's
origin now that the wall geometry is ruled out as the sole cause — requires
fresh explicit authorization. No convergence-rule change and no new HJB iterate
follows from this diagnostic.

Stationary KFE remains **NOT AUTHORIZED**.
