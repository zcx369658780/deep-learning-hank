# DLH-5V-T — Single-wall tangent-projected frozen-policy Newton geometry after the accepted final-validation repair

**Issue:** #68 / DLH-5V-T
**Task type:** `SCIENTIFIC_NUMERICAL_DIAGNOSTIC__BOUNDARY_TANGENT_PROJECTED_NEWTON_GEOMETRY_AFTER_VALIDATION_REPAIR`
**Route decision:** `APPROVE_SINGLE_WALL_TANGENT_PROJECTED_NEWTON_GEOMETRY_AFTER_5VS_TERMINAL_A`
**Authority marker:** `DLH_5VT_TANGENT_PROJECTED_NEWTON_GEOMETRY_AUTHORIZED`
**Initial authoritative activation:** `5674754187`
**Final authoritative activation-refresh:** `5675003122`
**Post-sync live `main`:** `e569271904eacbd3b2721b0b0f1ebb8e9a559e3f`
**Reviewer hold (gradient semantics):** `5676002613`
**Dedicated Builder branch:** `dsh/issue-68-dlh-5vt-tangent-projected-newton-2026-09-15`
**Date:** 2026-09-15

> **This revision supersedes the initial candidate `b194eb3886af7a5e3d5abe85dad114fdc6ed98eb`.**
> Per the Reviewer hold `5676002613`, the controlling diagnostic now uses the
> **exact two-entry full-state chain-rule gradient** of the limiting wall's
> `p_b`. The initial candidate's single-entry gradient is retained only as
> historical/debug evidence (§9) and does **not** feed the official projection,
> crossing or terminal.

## TERMINAL (exactly one)

```
DLH_5VT_TANGENT_PROJECTED_NEWTON__NONFINITE_INCONSISTENT_OR_NO_POSITIVE_SAFE_TANGENT_GEOMETRY__BOUNDARY_HJB_ROUTE_REVIEW_REQUIRED
```

**Outcome C.** With the corrected official gradient the geometry is
finite/consistent, the tangent identity holds exactly, both trials are strictly
domain-safe, and the geometry-improving criterion is satisfied **866.25×** (vs
the required `>= 10`). The disqualified condition is the frozen Outcome C
clause **"corrected-final vs iteration inconsistency"**: at both corrected trial
states the re-selected `final=False` operator and the corrected `final=True`
operator are **not** equivalent (`0.672` and `1.338` vs the `1e-9` tolerance),
on a small number of F0 rows in the z=1 block.

## 0. Scope ceiling — what this Issue does NOT claim

- Local **direction-geometry diagnostic only**. **No HJB convergence is
  claimed**; the Bellman tolerance remains the unchanged `1e-3` and the accepted
  residual `10.435094313164921` is still ~`10435`× that tolerance.
- **No trial state is an accepted HJB iterate** (`accepted_as_hjb_iterate =
  False`; `accepted_new_hjb_iterate = False`).
- No multi-step Newton, no policy iteration, no semismooth / trust-region /
  continuation, no adaptive line search or alpha tuning, no third trial
  fraction, no multiple active constraints, no projection-metric optimization,
  no `p_b` clip/floor, no price / Wmax / resolution sweep, no KFE / stationary
  KFE / steady state, no downstream work.
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

Exactly ONE current `final=False` operator build at `V_*`; `R = rho V_* - (u + Q V_*)`,
`J = rho I - Q`; exactly ONE solve `J d_N = -R`.

| Quantity | Value |
|---|---|
| `\|\|d_N\|\|inf` | `19.725548329099023` |
| Newton linear residual `\|\|J d_N + R\|\|inf` | `6.957900922088811e-11` |
| `newton_lin_res_ok` | `True` (`<= 1e-9`) |
| solves / operator builds in the module | exactly `1` linalg solve, exactly `3` builds |

Historical plain-Newton baseline reproduced exactly from the accepted Issue #62
semantics: `alpha_cross_N` = **`1.8667388489296687e-4`** (historical
`≈ 1.8667384893e-4`) at F3 (13,13), z=1, node 332. All-boundary accounting for
`d_N`: 186 required, **40** zero-derivative (`i == 0`), **86** negative-derivative.

## 3. OFFICIAL limiting-wall gradient — exact two-entry full chain rule

The wall's accepted `p_b` coordinate is `(V[wall] - V[down]) / db` with
`db = 0.3684210526315789`. Its gradient with respect to the **full** value
vector `V` is therefore:

| Entry | State index | Value |
|---|---|---|
| `g[wall]` | `723` (`1*391 + 332`) | **`+2.7142857142857144`** = `+1/db` |
| `g[down]` | `722` (`1*391 + 331`) | **`-2.7142857142857144`** = `-1/db` |
| all others | — | **`0`** |

| Requirement | Result |
|---|---|
| exactly two non-zero entries | **True** (`gradient_nonzero_count = 2`) |
| signs `+` / `-` | **True** |
| magnitudes `1/db` | **True** (exact) |
| `g` finite | **True** |
| `\|\|g\|\|_2 > 0` | **True**, `3.838579669298401` |
| basis / finite-difference identity reproduces the full chain rule | **True**, `gradient_basis_check_max_abs_err = 0.0` |
| `g @ d_N < 0` | **True**, `g @ d_N = -2.5755863276799573e-05` |

**Basis identity.** For every state index `j` and z block, mapping the basis
direction `e[j,z]` through the accepted
`local_resolvent_domain_geometry.boundary_direction_matrix` gives exactly
`g[j,z]` at the wall coordinate — the complete chain rule, verified
entry-by-entry with zero error. Directional finite differences confirm
`d p_b/d V[332,1] = +1/db` and `d p_b/d V[331,1] = -1/db`.

`i == 0` boundary states remain exactly zero-gradient per the accepted
V-independent rule (verified for all 40 such states).

## 4. OFFICIAL single-wall tangent projection

`d_T = d_N - g*(g@d_N)/(g@g)`, exactly ONE projection.

| Quantity | Value |
|---|---|
| `g @ d_N` | `-2.5755863276799573e-05` |
| **`g @ d_T`** | **`0.0`** — tangent identity holds exactly (tol `1e-9`) |
| `\|\|g\|\|_2` | `3.838579669298401` |
| `\|\|d_N\|\|inf` | `19.725548329099023` |
| `\|\|d_T\|\|inf` | `19.725548329099023` |
| `\|\|d_T - d_N\|\|inf` | **`4.7445011297497786e-06`** |
| `\|\|J d_N + R\|\|inf` | `6.957900922088811e-11` |
| `\|\|J d_T + R\|\|inf` | `0.3714265007988642` |
| `projection_count` | exactly `1` |

Because the two-entry gradient is aligned with the Newton direction to first
order, the projection removes only a very small normal component
(`g@d_N = -2.58e-05`): the official tangent direction is a **near-tangent step**
staying within `4.7e-06` of `d_N`, and its frozen linear residual
(`0.371`) is only ~`5.3e9`× the Newton linear residual — qualitatively different
from the superseded single-entry construction, which removed a large normal
component (§9).

## 5. OFFICIAL all-boundary crossing geometry

ONE all-boundary crossing computation over the 186 required non-F0 boundary
states, `PB_MARGIN = 1e-12`:

| Quantity | Value |
|---|---|
| required boundary states | `186` |
| exactly-zero-derivative states | `41` (includes all 40 `i == 0` states) |
| negative-derivative states | `85` |
| **`alpha_cross_T`** | **`0.16170699931086815`** |
| limiting state after projection | **F3, node 345, (j=14, i=11), z=1** |
| **`alpha_near`** = `min(1,(1-EPS_ALPHA)*alpha_cross_T)` | **`0.16170683760386884`** |
| **`alpha_half`** = `0.5*alpha_near` | **`0.08085341880193442`** |
| positive finite safe fraction exists | **`True`** |

Frozen constants honoured unchanged: `PB_MARGIN = 1e-12`, `EPS_ALPHA = 1e-6`,
`HALF_ALPHA = 0.5`, `MATERIAL_REDUCTION_RATIO = 0.50`. No adaptive search, no
tuning, no additional fraction.

**Geometry-improving criterion:** `alpha_near / min(1, alpha_cross_N)`
= `0.16170683760386884 / 1.8667388489296687e-4` = **`866.2532997045214`**
≥ `10` → **geometry-improving = True**.

## 6. OFFICIAL two diagnostic trials

Each trial: `V_trial = V_* + alpha*d_T`; strict boundary safety over all 186
required states; ONE `final=False` re-selection; ONE corrected `final=True`
validation build under the SAME freshly reselected current F0 controls;
corrected-final vs iteration equivalence check.

| Quantity | `alpha_half` | `alpha_near` |
|---|---|---|
| α | `0.08085341880193442` | `0.16170683760386884` |
| min boundary `p_b` | `4.8089461301970005e-09` (F3 node 332, (13,13), z=1) | `4.8089461301970005e-09` (same state) |
| domain safe (`> PB_MARGIN`) | **True** | **True** |
| `\|\|R_frozen_trial\|\|inf` | `9.591381262425049` | `8.747668211684884` |
| `\|\|R_reselect\|\|inf` | `9.593278055493213` | `8.755529626006652` |
| `\|\|R_final_trial\|\|inf` | `9.593278055493213` | `8.755529626006652` |
| reselect ratio | **`0.9193283517706523`** | **`0.8390465254310803`** |
| final ratio | **`0.9193283517706523`** | **`0.8390465254310803`** |
| final-vs-iter rowwise F0 gap | **`0.6718037653783657`** | **`1.3379411925537439`** |
| final-vs-iter equivalent | **False** | **False** |
| inconsistent F0 rows | **2** (`452`, `453`) | **4** (`452`, `453`, `482`, `483`) |
| `max\|Q 1\|` reselect / final | `2.4253377084448857e-12` / `2.4253377084448857e-12` | `2.4253377084448857e-12` / `2.4253377084448857e-12` |
| sector/transfer label changes | `0` | `2` |
| max \|Δ consumption\| | `0.11037704464076992` | `0.19758003449302874` |
| max \|Δ labor\| | `0.035978160412827975` | `0.06811077236428831` |
| max \|Δ transfer\| | `0.2879381893122205` | `0.5572061756483162` |
| max \|Δ mu_a\| | `0.2879381893122205` | `0.5572061756483162` |
| max \|Δ mu_b\| | `0.8364080749990155` | `1.2708541379074427` |
| max \|Δ utility\| | `0.1090224644177229` | `0.21516820213532295` |
| **material residual reducing** | **False** | **False** |

Both trials are strictly domain-safe, conserve `Q`, and their residual ratios
(`0.9193`, `0.8390`) remain far above the required `0.50`. The zero/2 label
switch counts must **not** be read as unchanged controls — the
continuous-control maxima are non-zero. No trial is an accepted iterate.

## 7. The disqualifying finding: trial-level operator inconsistency

At the corrected trial states the two construction paths disagree on F0 rows in
the z=1 block. Row-level evidence at `alpha_near` (node 61, (j=1, i=28), z=1):

| Column (in-block node) | corrected `final=True` | re-selected `final=False` |
|---|---|---|
| `451` (60) | `2.112988670733337` | `2.7819592670102096` |
| `452` (61, diagonal) | `-3.466279165757324` | `-4.804220358311068` |
| `453` (62) | `0.0` | `0.6689705962768723` |

Both rows report `utility` and the continuous controls as **bit-identical**
(`c`, `l`, `d`, `mu_a`, `mu_b` all equal), and both are conservative in total
(`max|Q 1| = 2.4253377084448857e-12` for both operators). The difference is in
the **rate construction**:

- the re-selection path uses the accepted policy's `iteration_b_*` rates with
  the source truncation convention (so it places an upwind entry at node 62 with
  rate `0.669` and carries it in the diagonal);
- the corrected `final=True` path recomputes raw drifts and applies
  `max(±mu)/step`, which puts the `b`-direction drift on the *other* side of the
  upwind sign boundary, so node 62 receives no entry and the diagonal is smaller.

This is a **latent semantic divergence between the two accepted rate paths**,
not a defect introduced by this Issue. It is invisible at the accepted `V_*`
(where the two operators agree exactly — measured: **0** inconsistent F0 rows)
and in the superseded single-entry trials, which sat `~4000×` closer to `V_*`.
The corrected two-entry projection opens a genuinely larger admissible step, and
in that region the divergence becomes measurable.

**Consequences** (stated as evidence, not as a convergence claim):

- the corrected `final=True` operator is **not** the MATLAB-faithful row at
  these trial states, so the trial-level "corrected final validation" identity
  that Issue #67 established at `V_*` **does not extend** to these states;
- the reported trial residual ratios are therefore *indicative* of residual
  behaviour along the tangent direction, but they are **not contractual**
  evidence under the frozen Issue #68 §7 rule, which requires the
  corrected-final/iteration equivalence as a precondition;
- any further direction design that relies on evaluating the corrected
  `final=True` operator away from `V_*` must first resolve this rate-path
  divergence.

## 8. Frozen interpretation rule → exactly ONE terminal

- finite/consistent evidence: **yes** (`failure_detail = None`)
- tangent condition `g @ d_T ≈ 0`: **yes** (exactly `0.0`)
- both trial states boundary-safe: **yes**
- geometry-improving (`>= 10`): **yes** (`866.25`)
- **corrected-final vs iteration consistency: NO** (`0.672` / `1.338`)
- at least one trial meeting the dual material-reduction criterion: **no**
  (best `0.8390`)
- deterministic repeat identical: **yes**

The frozen Outcome C condition *"corrected-final vs iteration inconsistency"* is
met → **Outcome C**, exactly one terminal.

### 8.1 Scientific reading (local, trajectory-bounded)

The corrected official gradient confirms that the single-wall tangent projection
**does** relax the wall geometry — and by a much larger factor than the
superseded construction suggested (`866.25×` vs `50.55×` the plain-Newton safe
fraction). The limiting state moves from the wall itself (node 332) to the
adjacent boundary state (node 345).

However the corrected projection is a *near-tangent* step
(`\|\|d_T - d_N\|\|inf = 4.7e-06`), and at its admissible fractions the residual
falls only to `83.9%`–`91.9%` of the accepted value — still far above the
required `50%`. Independently, the trial states expose the rate-path divergence
described in §7, which disqualifies the trials under the frozen rule.

This does **not** prove that no constrained direction can reduce the residual,
does **not** prove the HJB fixed point fails to exist, and does **not** authorize
any convergence-rule change or new iterate. It bounds the single-wall Euclidean
projection hypothesis and surfaces a separate operator-consistency question that
is now the binding blocker.

## 9. Historical / debug evidence — superseded single-entry gradient

Retained for the Reviewer-authorized remediation record only. It **must not**
feed the official projection, crossing or terminal classification.

| Quantity | Superseded single-entry value |
|---|---|
| gradient support | wall state only, `+1/db` |
| basis identity | **FAILS** at the backward neighbour (error `1/db`) |
| `\|\|g\|\|_2` | `2.7142857142857144` |
| `g @ d_N` | `-50.84485675074963` |
| `\|\|d_T - d_N\|\|inf` | `18.73231564501302` |
| `\|\|J d_T + R\|\|inf` | `733319.8338264916` |
| `alpha_cross_T` | `0.009436421907523617` |
| limiting state | F3, node 333, (j=13, i=14), z=1 |
| geometry ratio | `50.55026467396071` |
| trial ratios | `0.9952823934419176`, `0.9905659908441556` |
| operators equivalent at trials | **True** (`7.105427357601002e-15`) |
| historical terminal | `DLH_5VT_TANGENT_PROJECTED_NEWTON__TANGENT_DIRECTION_FINITE_AND_DOMAIN_SAFE_BUT_GEOMETRY_OR_RESIDUAL_IMPROVEMENT_INSUFFICIENT__FURTHER_DIRECTION_DESIGN_REQUIRED` |

The superseded construction satisfied its equivalence check only because its
trials were trivially close to `V_*`; the corrected construction reaches regions
where the rate paths genuinely differ.

## 10. Deterministic repeat

The full corrected diagnostic was executed twice; every compared field is
identical (`deterministic_repeat_identical = True`), including the gradient
support and basis error, the projection, the crossing data, both trials, the
operator-inconsistency rows and the terminal.

## 11. Tests

Focused suite `tests/test_dlh_5vt_tangent_projected_newton_geometry.py`:
**39 passed**.

Coverage: exact post-repair `V_*` reconstruction; selected-Q repaired blob
exactness; exact `R` reproduction; exactly ONE Newton solve and ONE base build
(runtime spies); Newton equation residual; **official gradient has exactly two
non-zero entries with `+1/db` at the wall and `-1/db` at the backward neighbour
and no other support**; **full-gradient basis identity with zero error**;
**directional finite-difference identity**; **single-entry gradient explicitly
rejected as the official construction (basis check fails, documented
debug-only)**; `i == 0` derivative exactly zero; gradient diagnostics recorded;
`g` finite/nonzero; `g @ d_N < 0`; historical baseline reproduction; tangent
identity exactly zero; official projection closed form; official `d_T` metrics;
official crossing determinism with the corrected `alpha_cross_T`; **stale
single-entry result does not feed classification**; exact alpha formulas with no
adaptive search; exactly two official trial fractions; official trial residuals
reproduced from the corrected projection; strict boundary safety; ONE
re-selection and ONE final build per trial; **trial operator inconsistency
recorded precisely (rows and gaps)**; residual ratios and control-switch
diagnostics; conservativity; material-reduction flag matching the frozen rule;
no accepted iterate and no convergence claim; fail-closed guards; static AST
scan for forbidden machinery; exactly one terminal.

Full repository suite `python -m pytest tests/ -q`: **573 passed, 0 failed,
6 warnings in 3539.12 s (0:58:59)**. The 6 warnings are the pre-existing
`MatrixRankWarning` entries from the accepted oracle tests (`test_dlh_5b`,
`test_dlh_5c`), not failures.

## 12. Authorized files (exact four-path allowlist)

1. `src/deep_learning_hank/two_asset/tangent_projected_newton_geometry.py`
2. `tests/test_dlh_5vt_tangent_projected_newton_geometry.py`
3. `reports/dlh_5vt_tangent_projected_newton_geometry_2026_09_15/DLH_5VT_TANGENT_PROJECTED_NEWTON_GEOMETRY_REPORT.md`
4. `reports/dlh_5vt_tangent_projected_newton_geometry_2026_09_15/DLH_5VT_TANGENT_PROJECTED_NEWTON_GEOMETRY_SUMMARY.csv`

No fifth tracked path. All accepted sources/tests/reports/governance remain
byte-identical to their accepted blobs; the selected-Q repaired blob
`556ccc214f03a1a22306cc4f5c7e9f7691bbf897` is unchanged.

## 13. Next gate (for the Owner / reviewer — NOT decided here)

Two distinct questions now stand:

1. **Rate-path divergence.** The re-selected `final=False` path and the
   corrected `final=True` path disagree on F0 rows in admissible regions away
   from `V_*`. This is a separate operator-consistency question that must be
   resolved before any direction design can rely on trial-level corrected-final
   validation.
2. **Residual behaviour.** Even where the operators are consistent, the
   near-tangent single-wall projection reduces the residual only to
   `83.9%`–`91.9%` of its accepted value.

Neither question authorizes a convergence-rule change, a new HJB iterate, or any
further direction by default. Stationary KFE remains **NOT AUTHORIZED**.
