# DLH-WL-P3C — bridge execution-readiness freeze: thresholds, search semantics, claim ceiling

Issue: **#82 / `DLH-WL-P3C`** — bridge execution-readiness freeze and human verification packet.
Owner route: `DLH-WL-V1-20260918`.
Authority marker: `DLH_WL_P3C_EXECUTION_READINESS_FREEZE_AUTHORIZED`.
Reviewer final activation comment: **`5741497930`**.
Reviewer HOLD remediated by this revision: **`5741651898`**.
Operative baseline: `2b7b0b7d506907ecbf41509bc526ad2b5ea794a6`.
Dedicated branch: `dsh/issue-82-dlh-wl-p3c-execution-readiness-freeze-2026-09-19`.

Status: **docs/config only.** No real transition matrix was inspected. No bridge was executed.
No dataset was downloaded, scraped, purchased or ingested. Scientific / model / training /
empirical-bridge calls = **0**.

Companion artifacts:

1. this freeze specification;
2. `docs/data/DLH_WL_P3C_HUMAN_SOURCE_VERIFICATION_PACKET_2026_09_19.md` — the E3 packet (H1–H7);
3. `configs/dlh_wl_p3c_bridge_readiness.toml` — the machine-readable freeze;
4. `reports/dlh_wl_p3c_2026_09_19/DLH_WL_P3C_REPORT.md` — Issue report and terminal.

---

## 0. What this Issue freezes and why it matters now

P3B (Issue #81) preregistered the T-family bridge and deliberately **left every numeric value
open**, recording that `pi_max`, `tau_W` and the search parameters are "frozen by Reviewer
authority **before** any outcome is computed", because choosing them with no data would be
arbitrary and choosing them after seeing results would be outcome-driven selection.

This Issue closes that gap. It freezes:

1. the **applicability and identification thresholds** (§1);
2. the **numerical validity tolerances** that operationalize the P3B admissibility conditions
   (A1)–(A4) and the generator conditions (§2);
3. the **`F_all_exact` / `F_search_tol` claim boundary** and the closed uniqueness-status vocabulary (§3);
4. the **deterministic search protocol** R1–R4, including the parameterization, the start
   construction and the reproducibility contract (§4);
5. the **identification and selection claim ceiling** (§5);
6. the **human/source verification packet** H1–H7 in a separate document (§6 pointer).

None of this executes anything. The freeze exists so that the first real execution is
**decided in advance rather than after the fact**.

### 0.1 Bounded remediation under Reviewer HOLD `5741651898`

Five numerical/claim semantics in the first revision of this freeze were wrong or too strong and
have been corrected consistently across this document, the TOML and the report. **All sixteen
Reviewer numeric thresholds are unchanged**, and no route, terminal or gate direction changed.

| HOLD item | Correction applied |
|---|---|
| **A** support semantics | the `T^(k)`-side global block failure was **mathematically wrong and is removed**. `T^(k)` is a k-step matrix, so `T^(k)_ij > 0` on a non-annual pair is expected behaviour and is now a `MULTISTEP_MASS_ON_NON_ANNUAL_PAIR` **diagnostic**, never a failure. R1/R2/R4 check **only the candidate annual matrix `P`** against the annual transition support. For T2 alone, a positive `T^(k)_ij` on a forbidden annual direct pair makes `P̂` support-invalid, recorded as `T2_SUPPORT_ELIGIBILITY_FAIL` and scoped to T2 |
| **B** exact vs numerical candidates | `F_all` → **`F_all_exact`** (exact mathematical roots) and `F_search` → **`F_search_tol`** (numerically admissible ε-root candidates). The unconditional `F_search ⊆ F_all` claim is **withdrawn**; only the `exact_root_certified` subset is asserted to lie in `F_all_exact`. Every candidate carries `root_residual` and `exact_root_certified`. Spread diagnostics are search-defined sensitivity evidence. The uniqueness vocabulary is replaced by the four `NUMERICALLY_ADMISSIBLE_ROOT_CANDIDATE` forms |
| **C** negativity middle band | `[-1e-10, -1e-12)` is now **`NUMERIC_SIGN_AMBIGUOUS__NOT_BRIDGE_USABLE`**: recordable as a raw solver candidate for diagnostics only, and it may **not** enter `F_search_tol`, spreads, bridge selection, `m`/`W` or admissibility counts. Only candidates whose retained matrix is entrywise `>= 0` after permitted cosmetic zeroing may enter the search set, with the row-sum/support/residual checks re-run |
| **D** exactly 64 starts | the contract freezes **64 executed optimizer starts for every window**: `n_special_valid + (64 − n_special_valid) = 64`. Invalid special candidates go to a separate `special_start_unavailable` ledger and are not optimizer starts. `default_rng`/PCG64 and `Dirichlet(alpha = 1)` are now labelled **Reviewer-ratified pre-execution search-design constants**, and `alpha = 1` is no longer described as "parameter-free" |
| **E** degenerate `m` | the whole-window degenerate-root failure is **removed**. `m_i(P) = 0` marks only that origin row `TARGET_UNAVAILABLE_DEGENERATE_OUTFLOW`; the window status is unaffected, other origins are evaluated normally, the row leaves the `W` spread and the supervised rows, and no uniform `W` is fabricated. `m_i < 0` remains invalid through the negativity rules. Whole-panel completeness is a **separate design gate** |

## 1. Reviewer-frozen thresholds

All values are copied verbatim from the Issue #82 body and the activation comment. The TOML
mirror is the normative machine-readable copy; this section states each value, the P3B
condition it belongs to, and what happens when it is exceeded.

### 1.1 Low-mobility applicability — `pi_max = 0.15`

| | |
|---|---|
| P3B condition | `C1` in P3B §2.3, the T2 applicability check |
| definition | `pi^(k) = max_i ( 1 - T^(k)_ii )` — the largest k-year one-way outflow probability |
| eligibility rule | T2 is eligible for a window **only if** `pi^(k) <= 0.15` |
| evaluated per | window |
| on violation | T2 is **not usable** for that window; the route is recorded as `C1_FAILED`; T1 and R4 are unaffected |
| rationale (Reviewer) | at `k = 5` the leading matrix-error scale `(pi^(k))²/k` is about `0.0045` at the boundary, keeping the low-mobility route deliberately conservative |
| status | **methodological tolerance, not a claim that real China data satisfy it** |

### 1.2 Annualization non-identification spread — `tau_W_abs = 0.02`

| | |
|---|---|
| P3B condition | the `tau_W` tolerance used by P3B §2.6 rule S5 |
| definition | `max` over non-degenerate origins, over admissible `(i,j)`, `j ≠ i`, and over pairs `P,Q ∈ F_search_tol`, of `|W_ij(P) - W_ij(Q)|` |
| origin scope | **only origins with `m_i(P) > 0` in every retained candidate**; a degenerate origin is excluded from the `W` spread and reported (see §1.5) |
| requirement | `<= 0.02` before a discovered multi-candidate search set may be treated as numerically stable |
| evaluated per | window |
| `W_ij(P)` defined only when | `m_i(P) > 0` |
| vacuous value | `0.0` when `|F_search_tol| <= 1`, or when no non-degenerate origin remains |
| on violation | window = `NOT_IDENTIFIED_BY_ANNUALIZATION` |

### 1.3 Outflow-share spread — `tau_m_abs = 0.02`

| | |
|---|---|
| definition | `max` over **all** origins `i` and over pairs `P,Q ∈ F_search_tol`, of `|m_i(P) - m_i(Q)|` |
| origin scope | **all origins** — `m_i = 1 - P_ii` is defined even when `m_i = 0`, so no origin is excluded from the `m` spread |
| requirement | `<= 0.02` |
| vacuous value | `0.0` when `|F_search_tol| <= 1` |
| on violation | window = `NOT_IDENTIFIED_BY_ANNUALIZATION` |

### 1.4 Region mapping loss — `unmappable_mass_share_max = 0.01`

| | |
|---|---|
| P3B condition | the unmappable-mass threshold that P3B left `TO_BE_FROZEN` |
| definition | the share of a source origin–time block's mass that cannot be assigned to the pinned canonical universe after declared exclusions and merges |
| requirement | `<= 0.01` |
| on violation | the **whole block fails closed** |
| redistribution or imputation | **not allowed** |

This is the numeric value P3B's region/`m`/`ell` contract said it deliberately did not choose
("no threshold numeric value … frozen by Reviewer authority before execution, not by P3B"). It
is now frozen here, before any source is opened.

### 1.5 Degenerate outflow is a **row-level** target-availability condition, not a window failure

P1B's accepted semantics are row-specific: a block with `m_i = 0` (or `ell_i = 0`) carries no
identifiable conditional target, while other origins are unaffected.

| | |
|---|---|
| trigger | `m_i(P) = 0` for origin `i` in a retained candidate |
| scope | **the affected origin row only** |
| row status | `TARGET_UNAVAILABLE_DEGENERATE_OUTFLOW` |
| window identification status | **unaffected** — the candidate remains a valid annual matrix and the window keeps its root status |
| other origins | evaluated normally |
| excluded from | the `W` spread (§1.2) and the supervised/evaluation rows |
| reported per candidate | the count and the list of degenerate origins |
| fabricating a uniform `W` | **not allowed** |
| all origins degenerate | `supervised_origin_count = 0` ⇒ no empirical `W` target is emitted for that window; the root status is still unaffected |
| whole-panel completeness | if a future empirical design separately requires a complete all-origin panel, that completeness rule may fail the window — but that is a **separate design gate**, not annualization non-identification |
| `m_i < 0` | cannot occur in a valid candidate: `m_i < 0` requires `P_ii > 1`, which the negativity and row-sum checks already reject; a negative `m` remains `INVALID_STOCHASTIC_CANDIDATE` through the negativity rules, never through this row rule |

## 2. Numerical validity tolerances, and the P3B condition each one operationalizes

P3B stated the admissibility conditions `(A1)`–`(A4)` symbolically. The frozen tolerances make
them decidable. The mapping is the substance of this section.

| Frozen tolerance | Value | P3B condition it decides |
|---|---|---|
| row-sum absolute tolerance | `1e-10` | **(A2)** row-stochasticity: `abs(Σ_j P_ij − 1) ≤ 1e-10` per origin row |
| stochastic non-negativity hard failure | any entry `< -1e-10` | **(A1)** non-negativity: such an entry **rejects** the candidate root |
| cosmetic zeroing band | `[-1e-12, 0)` | canonicalization of floating-point noise in **(A1)** |
| forbidden-support mass tolerance | `1e-12` | **(A3)** support admissibility |
| k-step root equation residual | `max_abs(P^k − T^(k)) ≤ 1e-8` | **(A4)** window consistency |
| generator row-sum tolerance | `1e-10` | generator condition `Q·1 = 0` (P3B §2.2 embedding route) |
| generator off-diagonal hard failure | any off-diagonal `< -1e-10` | generator condition `Q_ij ≥ 0` for `i ≠ j` |
| root deduplication threshold | `max_abs(P_a − P_b) ≤ 1e-7` | reporting identity for `F_search_tol` |
| imaginary-part tolerance | `max_abs(Im(·)) ≤ 1e-10` | reality of a candidate matrix / root / logarithm |

**No tolerance may be relaxed after observing a real bridge outcome.**

### 2.1 The negativity band is two-tier, and the middle tier is recorded

The two frozen negativity numbers imply three regions, and the middle one must not be
silently collapsed into either neighbour:

```
entry  <  -1e-10                 HARD FAILURE      -> candidate REJECTED, not in F_search_tol
entry in [-1e-10, -1e-12)        NUMERIC_SIGN_AMBIGUOUS__NOT_BRIDGE_USABLE
entry in [-1e-12, 0)             COSMETIC ZERO     -> may be set to exactly 0
entry  =  0 or > 0               non-negative      -> no action
```

**The middle band is not admissible.** The Issue's two frozen negativity numbers leave the band
`[-1e-10, -1e-12)` classified by neither bound. It is **not** correct to call a matrix that still
retains a negative entry "admissible": such a matrix is not entrywise non-negative, so it is not a
probability matrix and must not be used as a `W` or `m` source. The frozen thresholds are
unchanged; the *disposition* of the band is:

| | |
|---|---|
| band | `[-1e-10, -1e-12)` |
| status | `NUMERIC_SIGN_AMBIGUOUS__NOT_BRIDGE_USABLE` |
| permitted use | recorded as a **raw solver candidate for diagnostics only** |
| forbidden use | it may **not** enter `F_search_tol`, any root-spread calculation, bridge selection, `m`/`W` construction, or any "stochastic/admissible" count |
| reason | a retained negative entry means the matrix is not entrywise non-negative |

**Admission to the search set.** Only a candidate whose **retained/canonical** matrix is
entrywise `>= 0` after any permitted cosmetic zeroing may enter `F_search_tol`.

**Ordering constraint.** Cosmetic zeroing may happen **only after all other validity checks have
been established** on the candidate matrix. After zeroing, the **row-sum, annual-support and
root-residual checks are re-run on the retained matrix**, and the zeroing delta is recorded. So
zeroing can never be used to pass a check that the un-zeroed matrix would have failed, and the
reported candidate is always the retained (post-zeroing) matrix.

### 2.2 Support semantics: only the **annual candidate** is checked against the annual support

The previous revision of this document froze a `T^(k)`-side check that failed the **whole block**
whenever `T^(k)_ij > 0` on a pair forbidden by the annual transition support. **That rule was
mathematically wrong and is removed** (Reviewer HOLD `5741651898` item A).

**Why it was wrong.** `T^(k)` is a **k-step** transition matrix. If the annual direct edge `i → j`
is forbidden but an allowed indirect path `i → l → … → j` exists, then `T^(k)_ij > 0` is the
*expected* behaviour of a multi-step matrix, not a contradiction of the observed window. Applying
the annual support to `T^(k)` would fail essentially every non-trivial window closed — the exact
mechanism used in the P3B support counterexample.

**Corrected rules.**

| Check | Object | Rule | On failure |
|---|---|---|---|
| **annual-candidate check** | each candidate **annual** matrix `P` | `max` over forbidden annual direct `(i,j)` of `abs(P_ij) <= 1e-12`, with the forbidden mass sum recorded | the candidate is **rejected** and excluded from `F_search_tol` — this is the only support test that can reject a candidate |
| **multistep-mass diagnostic** | the observed window `T^(k)` | positive `T^(k)_ij` on a non-annual pair is recorded as a `MULTISTEP_MASS_ON_NON_ANNUAL_PAIR` diagnostic | **no failure** — informational only; there is no `T^(k)`-side global block failure |
| **T2 support eligibility** | the T2 candidate only | T2 is ineligible if any `T^(k)_ij > 1e-12` on a pair forbidden by the annual transition support, because `P̂_ij = T^(k)_ij/k` would then violate the annual support mask | status `T2_SUPPORT_ELIGIBILITY_FAIL`; **T2 only** — routes R1, R2 and R4 are unaffected and are validated on the candidate annual matrix alone |

`P^k` is therefore **allowed** to carry positive mass on pairs that are not annual direct edges.
Routes **R1, R2 and R4 check only the candidate annual matrix `P`** against the annual transition
support; they never inspect `T^(k)` against it.

**And two distinct supports must be declared, not conflated:**

- the **transition support** — which `i → j` transitions are structurally possible in the annual
  matrix `P`. It **includes the diagonal**: `P_ii` is the home-retention probability and is a
  real, allowed transition.
- the **`W` support** — the conditional foreign-destination support, where the diagonal is
  **always false** (P1B §3.4: `support_mask_ii = false` always; home retention is carried only
  by `P_ii = 1 − m_i`).

Conflating them would wrongly forbid self-transitions (making every candidate rejection-bound) or
wrongly allow the diagonal into the conditional target. The support mask is a **design object**
and may never be widened to accommodate an observation or a candidate.

## 3. Root-set semantics — the critical claim boundary

### 3.1 Exact mathematical roots versus numerical ε-root candidates

```
F_all_exact   = the MATHEMATICAL set of annual stochastic matrices P satisfying P^k = T^(k)
                EXACTLY, under the declared annual transition support.
                Not computable by a finite search.

F_search_tol  = the FINITE set of NUMERICALLY ADMISSIBLE EPSILON-ROOT CANDIDATES retained by
                the preregistered numerical search under the frozen tolerances, after
                deduplication by max_abs_separation = 1e-7.
```

**The unconditional subset claim is withdrawn.** The previous revision asserted
`F_search_tol ⊆ F_all_exact`. That implication is **not literally valid**: a matrix with residual `7e-9`
satisfies the frozen tolerance but is a numerical ε-root candidate, **not** necessarily an exact
mathematical root. The binding rules are now:

- **`F_search_tol ⊆ F_all_exact` is NOT asserted.** Every member of `F_search_tol` is a
  `NUMERICALLY_ADMISSIBLE_EPSILON_ROOT_CANDIDATE`;
- the only asserted inclusion is the **certified subset**:
  `{ P ∈ F_search_tol : exact_root_certified(P) = true } ⊆ F_all_exact`;
- each retained candidate carries both `root_residual` (its measured `max_abs(P^k − T^(k))`) and
  **`exact_root_certified = true/false`**, which may be `true` only if an analytical, interval,
  verified-continuation or equivalent computation proves `P^k = T^(k)` exactly;
- **the residual bound is a backward-error statement.** `residual ≤ 1e-8` bounds `P^k − T^(k)`;
  it does **not** by itself establish that an exact root exists nearby. That would require a
  separate perturbation or conditioning argument, which this contract does not supply;
- the finite-search **spread diagnostics are computed over `F_search_tol` only** and remain
  search-defined sensitivity evidence. They are **never** a proof about the complete exact-root
  set;
- **finding exactly one numerical candidate means
  `ONE_NUMERICALLY_ADMISSIBLE_ROOT_CANDIDATE_FOUND__GLOBAL_NONUNIQUENESS_NOT_EXCLUDED`** — it does
  **not** mean `UNIQUE_ROOT`;
- **a failed finite search cannot prove non-existence.** The status is
  `NO_NUMERICALLY_ADMISSIBLE_ROOT_CANDIDATE_FOUND__EXISTENCE_NOT_PROVEN`. Proving non-existence
  requires a certificate, not a search;
- **`F_search_tol` must never be described as `F_all_exact`**, and never as complete or global,
  unless a separate mathematical uniqueness/completeness certificate exists.

### 3.2 P3B alias map (declared so the two documents cannot drift apart)

| P3C name | P3B name | Meaning |
|---|---|---|
| `F_all_exact` | `𝓕(T^(k))` (P3B §2.2) | the exact mathematical admissible-root set |
| `F_search_tol` | `𝓕_enum` (P3B §2.6 rule S1) | the finite set of numerically admissible ε-root candidates the search enumerates |

P3B's rule S5 ("if `|F_enum| > 1` and the induced spread of any `W_ij` exceeds the tolerance
`tau_W` … declare `NOT_IDENTIFIED` and withhold the target") is therefore the same rule as
§5.1 below, with `tau_W → tau_W_abs = 0.02` and with `tau_m_abs` added on the same footing, and
with `𝓕_enum` read as the **tolerance-level** search set `F_search_tol` throughout.

### 3.3 Closed uniqueness-status vocabulary (exactly one per window)

| # | Status | When it is the correct status |
|---|---|---|
| 1 | `GLOBAL_UNIQUENESS_CERTIFIED` | **only** with an analytical, interval, verified-continuation or equivalent mathematical certificate covering the admissible domain |
| 2 | `MULTIPLE_NUMERICALLY_ADMISSIBLE_ROOT_CANDIDATES_FOUND` | `>= 2` distinct numerically admissible ε-root candidates in `F_search_tol` |
| 3 | `ONE_NUMERICALLY_ADMISSIBLE_ROOT_CANDIDATE_FOUND__GLOBAL_NONUNIQUENESS_NOT_EXCLUDED` | exactly one numerically admissible ε-root candidate in `F_search_tol`, no certificate |
| 4 | `NO_NUMERICALLY_ADMISSIBLE_ROOT_CANDIDATE_FOUND__EXISTENCE_NOT_PROVEN` | zero numerically admissible ε-root candidates in `F_search_tol`, no certificate |

**Vocabulary note.** Statuses 2–4 describe **tolerance-level candidates**, not proven exact roots.
The shorter pre-remediation wordings are therefore **forbidden**, and a candidate may carry the
additional per-candidate mark `EXACT_ROOT_CERTIFIED` **only** if an analytical/interval/verified
computation proves `P^k = T^(k)` exactly.

**Forbidden terms.** `UNIQUE_ROOT`, `GLOBALLY_UNIQUE`, `NO_ROOT_EXISTS`,
`NON_EXISTENCE_PROVEN`, `F_search_IS_F_all`, `COMPLETE_ROOT_SET`, `ALL_ROOTS_FOUND`, and the
superseded tolerance-level wordings `MULTIPLE_ADMISSIBLE_ROOTS_FOUND`,
`ONE_ROOT_FOUND__GLOBAL_NONUNIQUENESS_NOT_EXCLUDED`,
`NO_ADMISSIBLE_ROOT_FOUND__EXISTENCE_NOT_PROVEN`, `ADMISSIBLE_ROOTS_FOUND`. Such a term may appear
only inside a statement that it is forbidden or superseded.

**Coverage limit that must travel with every `F_search_tol` report.** The search is a numerical
search over the allowed-support row simplex. Whatever it finds, it cannot certify that it found
everything: a candidate could lie in a basin that none of the 64 executed starts enters, and even
a candidate it does find is only a tolerance-level ε-root candidate. This is precisely why status 1
requires a certificate, why statuses 3 and 4 are phrased as non-exclusions and non-proofs, and why
the spread diagnostics are search-defined sensitivity evidence rather than a statement about
`F_all_exact`.

## 4. Deterministic search protocol

Every applicable route runs, in fixed order, with no outcome-driven stopping. The route order is
an **execution** order; the **bridge-convention preference** is a separate, inherited object
(§4.5).

### 4.1 R1 — principal real k-th root

Attempt the principal matrix k-th root. Retain only if it is real within
`imaginary_part_abs_tol = 1e-10`, entrywise non-negative after any permitted cosmetic zeroing,
row-stochastic (row-sum within `1e-10`), **annual-support valid** (forbidden *annual* mass within
`1e-12`), and the root residual `max_abs(P^k − T^(k)) <= 1e-8` passes. **The support check applies
to the candidate annual matrix `P` only**; `P^k` may carry multistep mass on non-annual pairs.

### 4.2 R2 — generator / embedding candidate

Attempt the principal matrix logarithm `Q = (1/k) log(T^(k))`. Retain `P = exp(Q)` only if `Q`
satisfies the generator conditions (row sums within `1e-10`, no off-diagonal below `-1e-10`) and
`P` satisfies every stochastic, **annual-support** and root-residual condition. **Do not claim the
generator is unique.** As for R1, the support check applies to `P`, not to `P^k`.

### 4.3 R3 — T2 initialization candidate

Use the frozen low-mobility matrix as an initialization **only when `C1` passes**
(`pi^(k) <= 0.15`) **and the T2 support eligibility check passes** — because
`P̂_ij = T^(k)_ij/k`, a positive `T^(k)_ij` on a pair forbidden by the annual transition support
would make `P̂` violate the annual support mask. Failure is recorded as
`T2_SUPPORT_ELIGIBILITY_FAIL` and is **scoped to T2 only**; R1, R2 and R4 are unaffected. T2
itself remains an approximate candidate: it may **not** be called an exact root unless it
independently passes the root residual. When it is eligible and reported, its status is
`LOW_MOBILITY_APPROXIMATION__PREREGISTERED`.

### 4.4 R4 — constrained multistart root search

| Parameter | Frozen value |
|---|---|
| RNG family | `numpy.random.Generator` (PCG64), constructed by `numpy.random.default_rng` — **Reviewer-ratified pre-execution search-design constant** |
| RNG seed | `20260919` |
| **total executed optimizer starts** | **exactly 64, for every window** |
| max iterations per start | **5000** |
| objective | `\|\|P^k − T^(k)\|\|_F²` (Frobenius squared) |
| validity metric | `max_abs(P^k − T^(k))`, bound `1e-8` |
| convergence and validity decided only by | the frozen tolerances in §2 |
| non-converged start | recorded as `NOT_CONVERGED`, **no restart** |
| extra starts after observing results | **not allowed** |
| restarts or search-family changes after observing results | **not allowed** |
| search scope | **joint over all origins** — `P^k` couples rows, so the rows cannot be solved independently |
| candidate support checked | the candidate annual matrix `P` only |

**Parameterization (frozen).** The allowed-support **row simplex, bound-constrained**:

```
free variables : P_ij for every allowed transition (i,j) under the declared transition support
                 (structural zeros are removed from the variable set and held at exactly 0)
bounds         : 0 <= P_ij <= 1  per entry            -> enforces (A1)
equalities     : sum_j P_ij = 1  for every origin row -> enforces (A2)
support        : enforced structurally by the variable set -> enforces (A3)
```

A **softmax / logit row parameterization is explicitly NOT the frozen choice**, because a softmax
cannot attain an exact interior zero: a candidate with a genuine interior zero would be
unreachable, which would silently shrink `F_search_tol` and weaken exactly the completeness
question this Issue is about. Recording that rejection here is part of the contract.

**Start construction (frozen): 64 EXECUTED optimizer starts, always exactly 64.**

```
n_special_valid  := the number of valid starts among the four special start candidates
                    { identity, T2_candidate, principal_root_candidate, embedding_candidate }
                    for this window
random starts    := 64 - n_special_valid          drawn from ONE continuous fixed-seed stream
executed starts  := n_special_valid + (64 - n_special_valid) = 64      for EVERY window
```

| Element | Rule |
|---|---|
| special candidates | constructed exactly in P-space; **they consume NO RNG draws**, so the stream is unaffected by how many of them are valid |
| special-start validity | a special candidate is a valid **optimizer start** only if it satisfies every eligibility condition it is subject to (identity: always representable; T2: `C1` **and** T2 support eligibility; principal root and embedding: real, non-negative, row-stochastic, annual-support valid, residual-valid) |
| invalid special candidates | recorded in a separate `special_start_unavailable` ledger with the reason; **not counted as optimizer starts** and **not** re-drawn as a slot |
| random starts | `64 - n_special_valid`, drawn as `Dirichlet(alpha = 1)` on the allowed-support row simplex |
| draw order | origin rows in ascending canonical index order; within a row, the allowed-support entries in ascending canonical index order; start indices in ascending order |
| invariant | **total executed optimizer starts = 64 for every window**, whatever `n_special_valid` is |

The start distribution `Dirichlet(alpha = 1)` and the `default_rng` / PCG64 generator are
**Reviewer-ratified pre-execution search-design constants** (HOLD `5741651898` item D). They are
**not** empirical thresholds, and this document does **not** describe `alpha = 1` as
"parameter-free" or as "no numeric choice": it is a ratified pre-execution design constant, kept
distinct from the sixteen Reviewer numeric thresholds.

**Reproducibility caveat, and the control for it.** The RNG *stream* is a property of the NumPy
version; a future release may change it even for the same seed. The contract therefore requires
the implementation to record (a) the NumPy version, and (b) a **start-manifest hash** over all
**64 executed optimizer starts**, so that the actual starts used are auditable independently of the
stream. The seed, the count rule, the draw order and the distribution are frozen; the stream's
version-dependence is disclosed rather than hidden.

**Retention and reporting.** Every valid candidate — from R1, R2, R3 and R4 alike — whose retained
matrix is entrywise non-negative is deduplicated by `max_abs_separation = 1e-7` and retained in
`F_search_tol`. Candidates in the `NUMERIC_SIGN_AMBIGUOUS__NOT_BRIDGE_USABLE` band are recorded
**separately** and do not enter `F_search_tol`. The report must contain, per window: the number of
executed starts (always 64), the `special_start_unavailable` ledger, the per-start outcome
(`CONVERGED_AND_VALID`, `CONVERGED_BUT_INVALID`, `NOT_CONVERGED`), the objective and residual of
every retained candidate, its `exact_root_certified` flag, the deduplication groups, the
sign-ambiguous record, and the degenerate-origin list per candidate.

### 4.5 Route execution order versus bridge-convention preference

P3B §2.6 froze a **preference order** for choosing which annualization to *use*:
generator-embedding → principal real non-negative stochastic root → T2 (if `C1` passes) → fail
closed. P3C freezes R1→R2→R3→R4 as the **execution** order of the search.

These are not in conflict, and the difference is frozen explicitly so that it cannot be read as
one: **R1–R4 is the search execution order (which candidate generators are run, and in what
order, to build `F_search_tol`); the P3B §2.6 order remains the bridge-convention preference (which
discovered root, if several, becomes the selected bridge).** The preference selects a
**convention**, not an identification theorem, and alternative discovered roots and their spreads
remain reportable (§5.3).

### 4.6 Deterministic-search pseudocode (review aid)

```
search(window, T_k, declared_annual_support):
    require T_k is row-stochastic within row_sum_abs_tol
    record MULTISTEP_MASS_ON_NON_ANNUAL_PAIR diagnostic for positive T_k mass on
           non-annual pairs                 # informational; NEVER a window failure
    t2_eligible <- C1_passes(T_k) and no T_k_ij > 1e-12 on a forbidden annual direct pair
    if not t2_eligible: record T2_SUPPORT_ELIGIBILITY_FAIL   # scoped to T2 only

    F_search_tol <- {}
    sign_ambiguous <- []
    for route in [R1, R2, R3, R4]:                      # fixed order, all applicable routes run
        for candidate in route_candidates(route):
            if not real_within(candidate, 1e-10):              continue
            if min_entry(candidate) < -1e-10:                  continue   # hard rejection
            if min_entry(candidate) < -1e-12:                  # band [-1e-10, -1e-12)
                sign_ambiguous.append(candidate)               # diagnostics only
                continue                                       # NOT in F_search_tol
            record objective and residual
            cosmetic_zero_entries_in_minus_1e_12_to_0(candidate)
            re-run row-sum, annual-support and root-residual checks on the retained matrix
            if not row_stochastic_within(candidate, 1e-10):   continue
            if not annual_support_within(candidate, 1e-12):   continue
            if max_abs(candidate^k - T_k) > 1e-8:             continue
            candidate.exact_root_certified <- false            # true only with a proof
            F_search_tol <- dedup_add(F_search_tol, candidate, 1e-7)

    n_special_valid <- count of valid special candidates for this window
    executed_starts <- n_special_valid + (64 - n_special_valid)   # ALWAYS 64
    record special_start_unavailable ledger for invalid special candidates

    status <- classify(F_search_tol)                    # one of the four frozen statuses
    degenerate_origins <- { i : m_i(P) = 0 for some P in F_search_tol }
    for i in degenerate_origins: row_status[i] <- TARGET_UNAVAILABLE_DEGENERATE_OUTFLOW
    supervised_origins <- origins not in degenerate_origins
    spread_W <- over supervised_origins only ; spread_m <- over ALL origins
    if len(F_search_tol) >= 2 and (spread_W > 0.02 or spread_m > 0.02):
                          window <- NOT_IDENTIFIED_BY_ANNUALIZATION
    elif len(F_search_tol) >= 2:
                          window <- SEARCH_SET_STABLE_WITHIN_PREREGISTERED_TOLERANCE
    # no branch anywhere sets GLOBAL_UNIQUENESS_CERTIFIED without a certificate
    # no branch turns a degenerate origin into a window failure
    # no branch puts a sign-ambiguous candidate into F_search_tol, a spread, m/W or counting
```

## 5. Identification and selection claim ceiling

### 5.1 Two or more numerically admissible candidates found

Report **all** candidates retained in `F_search_tol` (and separately the sign-ambiguous ones).
Then:

- if `tau_W_abs` **or** `tau_m_abs` is violated → window = `NOT_IDENTIFIED_BY_ANNUALIZATION`,
  and **no empirical `W` target is emitted**;
- if both spreads remain within tolerance → the window **may** be labelled
  `SEARCH_SET_STABLE_WITHIN_PREREGISTERED_TOLERANCE`;
- in **both** cases global uniqueness **may not** be claimed.

### 5.2 Exactly one numerically admissible candidate found

Without a global certificate:

- status = `ONE_NUMERICALLY_ADMISSIBLE_ROOT_CANDIDATE_FOUND__GLOBAL_NONUNIQUENESS_NOT_EXCLUDED`;
- the selected bridge is **assumption-defined and search-defined**;
- the candidate is a **tolerance-level ε-root candidate**, not a proven exact root unless
  `exact_root_certified = true`;
- it is **not data-identified**.

### 5.3 Generator / principal-root preference

The P3B preference order chooses a **bridge convention**, not an identification theorem. Even when
generator or principal root is selected, the alternative discovered candidates and their spreads
remain **reportable** and must appear in the report.

### 5.4 T2

If `C1` passes **and** the T2 support eligibility check passes, T2 may be reported as
`LOW_MOBILITY_APPROXIMATION__PREREGISTERED`. It may not be relabelled an exact annual matrix
unless it independently passes the exact root residual.

### 5.5 Zero numerically admissible candidates found

Status `NO_NUMERICALLY_ADMISSIBLE_ROOT_CANDIDATE_FOUND__EXISTENCE_NOT_PROVEN`. Neither existence
nor non-existence is established; the window simply yields no admissible candidate under the
preregistered search.

### 5.6 Degenerate origins are a row-level matter

A retained candidate with `m_i(P) = 0` for some origin `i` is **not** a window failure: `P` is
still a valid annual matrix, the window keeps its status, and the other origins are evaluated
normally. The affected row is reported as `TARGET_UNAVAILABLE_DEGENERATE_OUTFLOW` and is excluded
from the `W` spread and from supervised/evaluation rows. No uniform `W` is fabricated for it. If a
future empirical design separately requires a complete all-origin panel, that completeness rule is
a **separate design gate** and must be added by its own dated authority.

## 6. Human/source verification packet

The packet is `docs/data/DLH_WL_P3C_HUMAN_SOURCE_VERIFICATION_PACKET_2026_09_19.md`. It freezes
seven items **H1–H7** — NBS transition semantics; census/1% table availability; region coding;
source weights and comparability; pair labor intensity `lambda_ij`; origin labor amount `ell_i`;
timing and leakage — each with the exact question, the required evidence, the decision options,
the E3 promotion criterion and the fail-closed consequence of remaining unresolved.

Two properties of the packet are binding and stated here as well:

1. **No self-promotion.** E3 promotion is a human/Owner act. DSH may prepare the packet and may
   not promote any source or evidence level. Every item is recorded as unresolved at this Issue.
2. **`lambda_ij` and `ell_i` remain two independent provenance fields.** They may not be
   inferred from one another, and the `(C-LINK)` consistency condition
   `ell_i = ell_i^movers + ell_i^stay + ell_i^unobserved` must either be supplied from one
   coherent frame or declared with a reported residual. H5 and H6 are therefore separate fields
   with separate evidence requirements, and a single source may satisfy both only if it is
   shown to be one coherent frame.

## 7. What this freeze does and does not authorize

**Does not authorize:** any real transition matrix execution or inspection; any bridge
implementation or adapter; any dataset download, scrape, purchase or ingestion; any fit, training
or estimation; any HJB/KFE/GE/MATLAB/household call; any full-suite run; any E3 promotion; any
relaxation of a frozen value after an outcome is observed; any successor Issue.

**Does authorize (only):** a later, **separately authorized** Issue to (a) work the H1–H7 packet
to human verification, and (b) implement the preregistered bridge **exactly** against this frozen
contract — same tolerances, same route set and order, same parameterization, same
64-executed-start construction, same claim ceiling.

## 8. Execution-readiness invariants

These are binding on any later Issue until a dated pre-execution amendment replaces them.

| Invariant | Statement |
|---|---|
| C1 | `F_search_tol ⊆ F_all_exact` is **not asserted**; members of `F_search_tol` are numerically admissible ε-root candidates, and only the `exact_root_certified` subset is asserted to lie in `F_all_exact`. `F_search_tol` is never reported as complete or global |
| C2 | one numerical candidate ⇒ `ONE_NUMERICALLY_ADMISSIBLE_ROOT_CANDIDATE_FOUND__GLOBAL_NONUNIQUENESS_NOT_EXCLUDED`, never `UNIQUE_ROOT` |
| C3 | zero numerical candidates ⇒ `NO_NUMERICALLY_ADMISSIBLE_ROOT_CANDIDATE_FOUND__EXISTENCE_NOT_PROVEN`, never a proof of non-existence |
| C4 | `GLOBAL_UNIQUENESS_CERTIFIED` requires a mathematical certificate over the admissible domain |
| C5 | exactly one uniqueness status per window, drawn from the closed four-term vocabulary; the superseded tolerance-as-admissible wordings are forbidden |
| C6 | a candidate is retained only if it passes **every** frozen check on the retained matrix: reality, entrywise non-negativity, row-sum, annual support, root residual |
| C7 | cosmetic zeroing is post-validity, bounded by `[-1e-12, 0)`, followed by a re-run of the row-sum, annual-support and root-residual checks, with the delta recorded |
| C8 | the band `[-1e-10, -1e-12)` is `NUMERIC_SIGN_AMBIGUOUS__NOT_BRIDGE_USABLE`: recorded for diagnostics only, never in `F_search_tol`, spreads, bridge selection, `m`/`W` or admissibility counts |
| C9 | **only the candidate annual matrix `P`** is checked against the annual transition support; positive `T^(k)` mass on a non-annual pair is an expected `MULTISTEP_MASS_ON_NON_ANNUAL_PAIR` diagnostic and never a window failure |
| C10 | the transition support and the `W` support are declared separately; the `W` diagonal is always false |
| C11 | **exactly 64 executed optimizer starts for every window**: `n_special_valid` valid special starts plus `64 − n_special_valid` Dirichlet(α=1) starts; invalid specials go to a separate ledger and are not optimizer starts; special starts consume no RNG draws |
| C12 | max 5000 iterations per start; a non-converged start is recorded, never restarted |
| C13 | every applicable route runs; no outcome-driven stopping |
| C14 | the route execution order (R1–R4) is not the bridge-convention preference order (P3B §2.6) |
| C15 | a spread violation ⇒ `NOT_IDENTIFIED_BY_ANNUALIZATION` and no empirical `W` target. A degenerate origin (`m_i(P) = 0`) is **not** a window failure: it is `TARGET_UNAVAILABLE_DEGENERATE_OUTFLOW` for that row only, excluded from the `W` spread and from supervised rows, with no fabricated `W` |
| C16 | T2 is an approximation unless it independently passes the root residual, and it is ineligible when the T2 support eligibility check fails (`T2_SUPPORT_ELIGIBILITY_FAIL`), which is scoped to T2 alone |
| C17 | no tolerance, threshold, seed, start-count rule, route set or claim rule is changed after an outcome is observed |
| C18 | E3 promotion is a human act; DSH never self-promotes |
| C19 | `lambda_ij` and `ell_i` remain two separate provenance fields, tied only by `(C-LINK)` |
| C20 | the frozen values in this document and in `configs/dlh_wl_p3c_bridge_readiness.toml` are identical, and all sixteen Reviewer numeric thresholds are unchanged by this remediation |
| C21 | `Dirichlet(alpha = 1)` and `default_rng`/PCG64 are Reviewer-ratified **pre-execution search-design constants**, not empirical thresholds, and are not described as "parameter-free" |
