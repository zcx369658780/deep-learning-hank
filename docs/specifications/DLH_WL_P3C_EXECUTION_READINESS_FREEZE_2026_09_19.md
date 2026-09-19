# DLH-WL-P3C — bridge execution-readiness freeze: thresholds, search semantics, claim ceiling

Issue: **#82 / `DLH-WL-P3C`** — bridge execution-readiness freeze and human verification packet.
Owner route: `DLH-WL-V1-20260918`.
Authority marker: `DLH_WL_P3C_EXECUTION_READINESS_FREEZE_AUTHORIZED`.
Reviewer final activation comment: **`5741497930`**.
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
3. the **`F_all` / `F_search` claim boundary** and the closed uniqueness-status vocabulary (§3);
4. the **deterministic search protocol** R1–R4, including the parameterization, the start
   construction and the reproducibility contract (§4);
5. the **identification and selection claim ceiling** (§5);
6. the **human/source verification packet** H1–H7 in a separate document (§6 pointer).

None of this executes anything. The freeze exists so that the first real execution is
**decided in advance rather than after the fact**.

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
| definition | `max` over admissible `(i,j)`, `j ≠ i`, and over pairs `P,Q ∈ F_search`, of `|W_ij(P) - W_ij(Q)|` |
| requirement | `<= 0.02` before a discovered multi-root search set may be treated as numerically stable |
| evaluated per | window |
| `W_ij(P)` defined only when | `m_i(P) > 0` |
| vacuous value | `0.0` when `|F_search| <= 1` |
| on violation | window = `NOT_IDENTIFIED_BY_ANNUALIZATION` |

### 1.3 Outflow-share spread — `tau_m_abs = 0.02`

| | |
|---|---|
| definition | `max` over origins `i` and over pairs `P,Q ∈ F_search`, of `|m_i(P) - m_i(Q)|` |
| requirement | `<= 0.02` |
| vacuous value | `0.0` when `|F_search| <= 1` |
| on violation | window = `NOT_IDENTIFIED_BY_ANNUALIZATION` |

**Degenerate-root rule (fail-closed addition).** If any retained root has `min_i m_i(P) <= 0`,
the conditional share `W_ij(P) = P_ij/m_i(P)` is undefined for that origin and the window fails
closed to `NOT_IDENTIFIED_BY_ANNUALIZATION` **regardless of the measured spreads**. Enforcing
only the spread statistic would let a `0/0` cell pass unnoticed; P1B §2.2 item 5 already
forbids fabricating a label for a block with `m_i = 0`, and this rule makes the same
prohibition operational.

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
| root deduplication threshold | `max_abs(P_a − P_b) ≤ 1e-7` | reporting identity for `F_search` |
| imaginary-part tolerance | `max_abs(Im(·)) ≤ 1e-10` | reality of a candidate matrix / root / logarithm |

**No tolerance may be relaxed after observing a real bridge outcome.**

### 2.1 The negativity band is two-tier, and the middle tier is recorded

The two frozen negativity numbers imply three regions, and the middle one must not be
silently collapsed into either neighbour:

```
entry  <  -1e-10                 HARD FAILURE      -> candidate root REJECTED, not in F_search
entry in [-1e-10, -1e-12)        SOFT NEGATIVITY   -> retained, RECORDED, NOT zeroed
entry in [-1e-12, 0)             COSMETIC ZERO     -> may be set to exactly 0
entry  =  0 or > 0               admissible        -> no action
```

**Interpretive note, flagged for the Reviewer.** The Issue freezes a hard-failure bound
(`-1e-10`) and a *narrower* cosmetic-zeroing bound (`-1e-12`), which leaves the band
`[-1e-10, -1e-12)` in neither category. P3C resolves it as **retain-and-record, never zero**:
such an entry is treated as acceptable floating-point noise of a mathematically non-negative
entry (so the root is admissible), but it is **not** canonicalized, and its count, minimum and
location are reported (`soft_negativity_entries`). This is the reading that neither discards a
valid root nor hides a non-zero negative entry. If the Reviewer intended the cosmetic band to
apply to the whole `[-1e-10, 0)` range, that is a dated pre-execution amendment; P3C does not
assume it.

**Ordering constraint.** Cosmetic zeroing may happen **only after all other validity checks have
been established** on the candidate matrix, and the **retained** matrix must then pass every
check again. So zeroing can never be used to pass a check that the un-zeroed matrix would have
failed, and the reported root is always the retained (post-zeroing) matrix, with the
zeroing delta recorded.

### 2.2 Two distinct support checks, because two distinct masks are involved

P3B's `(A3)` and P3B §2.3's T2 support finding refer to **two different objects**, and P3C
freezes both checks separately:

| Check | Object | Rule | On failure |
|---|---|---|---|
| **T^(k)-side pre-check** | the observed window | no positive off-diagonal of `T^(k)` on a pair forbidden by the declared **annual transition support**; "positive" means `> 1e-12` | the block **fails closed**: the observation already contradicts the declared support |
| **P-side check** | each candidate root | `max` over forbidden `(i,j)` of `abs(P_ij) <= 1e-12`, with the forbidden mass sum also recorded | the candidate root is **rejected** |

**And two distinct supports must be declared, not conflated:**

- the **transition support** — which `i → j` transitions are structurally possible in the annual
  matrix `P`. It **includes the diagonal**: `P_ii` is the home-retention probability and is a
  real, allowed transition.
- the **`W` support** — the conditional foreign-destination support, where the diagonal is
  **always false** (P1B §3.4: `support_mask_ii = false` always; home retention is carried only
  by `P_ii = 1 − m_i`).

Conflating them would wrongly forbid self-transitions (making every root inadmissible) or
wrongly allow the diagonal into the conditional target. The support mask is a **design object**
and may never be widened to accommodate an observation.

## 3. Root-set semantics — the critical claim boundary

### 3.1 Two sets, never interchangeable

```
F_all     = the MATHEMATICAL set of all admissible annual stochastic roots P of P^k = T^(k)
            under the declared transition support. Not computable by a finite search.

F_search  = the FINITE set of admissible roots discovered by the preregistered numerical
            search and retained after deduplication by max_abs_separation.
```

Binding rules:

- `F_search ⊆ F_all`;
- **`F_search` must never be described as `F_all`** unless a separate mathematical
  uniqueness/completeness certificate exists;
- **finding exactly one root numerically means `ONE_ROOT_FOUND__GLOBAL_NONUNIQUENESS_NOT_EXCLUDED`**
  — it does **not** mean `UNIQUE_ROOT`;
- **a failed finite search cannot prove non-existence.** The status is
  `NO_ADMISSIBLE_ROOT_FOUND__EXISTENCE_NOT_PROVEN`. Proving non-existence requires a
  certificate, not a search.

### 3.2 P3B alias map (declared so the two documents cannot drift apart)

| P3C name | P3B name | Meaning |
|---|---|---|
| `F_all` | `𝓕(T^(k))` (P3B §2.2) | the mathematical admissible-root set |
| `F_search` | `𝓕_enum` (P3B §2.6 rule S1) | the finite set the search enumerates |

P3B's rule S5 ("if `|F_enum| > 1` and the induced spread of any `W_ij` exceeds the tolerance
`tau_W` … declare `NOT_IDENTIFIED` and withhold the target") is therefore the same rule as
§5.1 below, with `tau_W → tau_W_abs = 0.02` and with `tau_m_abs` added on the same footing.

### 3.3 Closed uniqueness-status vocabulary (exactly one per window)

| # | Status | When it is the correct status |
|---|---|---|
| 1 | `GLOBAL_UNIQUENESS_CERTIFIED` | **only** with an analytical, interval, verified-continuation or equivalent mathematical certificate covering the admissible domain |
| 2 | `MULTIPLE_ADMISSIBLE_ROOTS_FOUND` | `>= 2` distinct admissible roots in `F_search` |
| 3 | `ONE_ROOT_FOUND__GLOBAL_NONUNIQUENESS_NOT_EXCLUDED` | exactly one admissible root in `F_search`, no certificate |
| 4 | `NO_ADMISSIBLE_ROOT_FOUND__EXISTENCE_NOT_PROVEN` | zero admissible roots in `F_search`, no certificate |

**Forbidden terms.** `UNIQUE_ROOT`, `GLOBALLY_UNIQUE`, `NO_ROOT_EXISTS`,
`NON_EXISTENCE_PROVEN`, `F_search_IS_F_all`, `COMPLETE_ROOT_SET`, `ALL_ROOTS_FOUND`. Such a
term may appear only inside a statement that it is forbidden.

**Coverage limit that must travel with every `F_search` report.** The search is a numerical
search over the allowed-support row simplex. Whatever it finds, it cannot certify that it found
everything: a root could lie in a basin that none of the 64 preregistered starts enters. This is
precisely why status 1 requires a certificate and why statuses 3 and 4 are phrased as
non-exclusions and non-proofs.

## 4. Deterministic search protocol

Every applicable route runs, in fixed order, with no outcome-driven stopping. The route order is
an **execution** order; the **bridge-convention preference** is a separate, inherited object
(§4.5).

### R1 — principal real k-th root

Attempt the principal matrix k-th root. Retain only if it is real within
`imaginary_part_abs_tol = 1e-10`, fully stochastic (row-sum within `1e-10`, no entry below
`-1e-10`), support-valid (forbidden mass within `1e-12`), and the root residual
`max_abs(P^k − T^(k)) <= 1e-8` passes.

### R2 — generator / embedding candidate

Attempt the principal matrix logarithm `Q = (1/k) log(T^(k))`. Retain `P = exp(Q)` only if `Q`
satisfies the generator conditions (row sums within `1e-10`, no off-diagonal below `-1e-10`) and
`P` satisfies every stochastic, support and root-residual condition. **Do not claim the
generator is unique.**

### R3 — T2 initialization candidate

Use the frozen low-mobility matrix as an initialization **only when `C1` passes**
(`pi^(k) <= 0.15`). T2 itself remains an approximate candidate: it may **not** be called an exact
T1 root unless it independently passes the root residual. When `C1` passes and it is reported, its
status is `LOW_MOBILITY_APPROXIMATION__PREREGISTERED`.

### R4 — constrained multistart root search

| Parameter | Frozen value |
|---|---|
| RNG family | `numpy.random.Generator` (PCG64), constructed by `numpy.random.default_rng` |
| RNG seed | `20260919` |
| deterministic start count | **64** |
| max iterations per start | **5000** |
| objective | `\|\|P^k − T^(k)\|\|_F²` (Frobenius squared) |
| validity metric | `max_abs(P^k − T^(k))`, bound `1e-8` |
| convergence and validity decided only by | the frozen tolerances in §2 |
| non-converged start | recorded as `NOT_CONVERGED`, **no restart** |
| extra starts after observing results | **not allowed** |
| restarts or search-family changes after observing results | **not allowed** |
| search scope | **joint over all origins** — `P^k` couples rows, so the rows cannot be solved independently |

**Parameterization (frozen).** The allowed-support **row simplex, bound-constrained**:

```
free variables : P_ij for every allowed transition (i,j) under the declared transition support
                 (structural zeros are removed from the variable set and held at exactly 0)
bounds         : 0 <= P_ij <= 1  per entry            -> enforces (A1)
equalities     : sum_j P_ij = 1  for every origin row -> enforces (A2)
support        : enforced structurally by the variable set -> enforces (A3)
```

A **softmax / logit row parameterization is explicitly NOT the frozen choice**, because a softmax
cannot attain an exact interior zero: an admissible root with a genuine interior zero would be
unreachable, which would silently shrink `F_search` and weaken exactly the completeness question
this Issue is about. Recording that rejection here is part of the contract.

**Start construction (frozen, so that "64 deterministic starts" is reproducible).**

```
positions 1..4  : the four SPECIAL starts, constructed exactly in P-space, using NO random
                  draws, so the RNG stream is unaffected:
                    (1) identity
                    (2) T2 candidate
                    (3) principal-root candidate
                    (4) embedding candidate
                  A special start that is not valid for a window is recorded as OMITTED with a
                  reason; its position is NOT re-drawn.
positions 5..64 : 60 random starts drawn from ONE continuous RNG stream:
                  start_distribution = Dirichlet(alpha = 1 on the allowed-support row simplex)
                  draw order         = origin rows in ascending canonical index order; within a
                                       row, the allowed-support entries in ascending canonical
                                       index order; start indices in ascending order.
                  free numeric parameters = NONE (alpha = 1 is parameter-free, so no Builder
                  number enters a Reviewer-frozen contract)
```

**Reproducibility caveat, and the control for it.** The RNG *stream* is a property of the NumPy
version; a future release may change it even for the same seed. The contract therefore requires
the implementation to record (a) the NumPy version, and (b) a **start-manifest hash** over the 64
generated start matrices, so that the actual starts used are auditable independently of the
stream. The seed, the count, the draw order and the distribution are frozen; the stream's
version-dependence is disclosed rather than hidden.

**Retention and reporting.** Every valid root — from R1, R2, R3 and R4 alike — is deduplicated by
`max_abs_separation = 1e-7` and retained in `F_search`. The report must contain, per window:
the number of starts attempted, the per-start outcome (`CONVERGED_AND_VALID`,
`CONVERGED_BUT_INVALID`, `NOT_CONVERGED`, `OMITTED`), the objective and residual of every retained
root, the deduplication groups, and the soft-negativity record.

### 4.5 Route execution order versus bridge-convention preference

P3B §2.6 froze a **preference order** for choosing which annualization to *use*:
generator-embedding → principal real non-negative stochastic root → T2 (if `C1` passes) → fail
closed. P3C freezes R1→R2→R3→R4 as the **execution** order of the search.

These are not in conflict, and the difference is frozen explicitly so that it cannot be read as
one: **R1–R4 is the search execution order (which candidate generators are run, and in what
order, to build `F_search`); the P3B §2.6 order remains the bridge-convention preference (which
discovered root, if several, becomes the selected bridge).** The preference selects a
**convention**, not an identification theorem, and alternative discovered roots and their spreads
remain reportable (§5.3).

### 4.6 Deterministic-search pseudocode (review aid)

```
build_F_search(window, T_k, declared_transition_support):
    require T_k is row-stochastic within row_sum_abs_tol
    require no positive off-diagonal of T_k on a forbidden annual pair   # Tk-side pre-check
    F_search <- {}
    for route in [R1, R2, R3, R4]:                      # fixed order, all applicable routes run
        for candidate in route_candidates(route):
            if not real_within(candidate, 1e-10):            continue
            if not stochastic_within(candidate, 1e-10, -1e-10): continue
            if not support_within(candidate, 1e-12):          continue
            if max_abs(candidate^k - T_k) > 1e-8:             continue
            record objective and residual
            atomic cosmetic zeroing of entries in [-1e-12, 0)   # validity already established
            re-run every check on the retained matrix
            F_search <- dedup_add(F_search, candidate, 1e-7)
    status <- classify(F_search)                        # one of the four frozen statuses
    if any P in F_search has min_i m_i(P) <= 0: window <- NOT_IDENTIFIED_BY_ANNUALIZATION
    elif |F_search| >= 2 and (spread_W > 0.02 or spread_m > 0.02):
                                              window <- NOT_IDENTIFIED_BY_ANNUALIZATION
    elif |F_search| >= 2:                     window <- SEARCH_SET_STABLE_WITHIN_PREREGISTERED_TOLERANCE
    # no branch anywhere sets GLOBAL_UNIQUENESS_CERTIFIED without a certificate
```

## 5. Identification and selection claim ceiling

### 5.1 Two or more admissible roots found

Report **all** discovered roots. Then:

- if `tau_W_abs` **or** `tau_m_abs` is violated → window = `NOT_IDENTIFIED_BY_ANNUALIZATION`,
  and **no empirical `W` target is emitted**;
- if both spreads remain within tolerance → the window **may** be labelled
  `SEARCH_SET_STABLE_WITHIN_PREREGISTERED_TOLERANCE`;
- in **both** cases global uniqueness **may not** be claimed.

### 5.2 Exactly one root found

Without a global certificate:

- status = `ONE_ROOT_FOUND__GLOBAL_NONUNIQUENESS_NOT_EXCLUDED`;
- the selected bridge is **assumption-defined and search-defined**;
- it is **not data-identified**.

### 5.3 Generator / principal-root preference

The P3B preference order chooses a **bridge convention**, not an identification theorem. Even when
generator or principal root is selected, the alternative discovered roots and their spreads remain
**reportable** and must appear in the report.

### 5.4 T2

If `C1` passes, T2 may be reported as `LOW_MOBILITY_APPROXIMATION__PREREGISTERED`. It may not be
relabelled an exact annual root unless it independently passes the exact root residual.

### 5.5 Zero roots found

Status `NO_ADMISSIBLE_ROOT_FOUND__EXISTENCE_NOT_PROVEN`. Neither existence nor non-existence is
established; the window simply yields no root under the preregistered search.

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
contract — same tolerances, same route set and order, same parameterization, same 64-start
construction, same claim ceiling.

## 8. Execution-readiness invariants

These are binding on any later Issue until a dated pre-execution amendment replaces them.

| Invariant | Statement |
|---|---|
| C1 | `F_search` is a subset of `F_all`; `F_search` is never reported as complete or global |
| C2 | one numerical root ⇒ `ONE_ROOT_FOUND__GLOBAL_NONUNIQUENESS_NOT_EXCLUDED`, never `UNIQUE_ROOT` |
| C3 | zero numerical roots ⇒ `NO_ADMISSIBLE_ROOT_FOUND__EXISTENCE_NOT_PROVEN`, never a proof of non-existence |
| C4 | `GLOBAL_UNIQUENESS_CERTIFIED` requires a mathematical certificate over the admissible domain |
| C5 | exactly one uniqueness status per window, drawn from the closed four-term vocabulary |
| C6 | a root is retained only if it passes **every** frozen check: reality, row-sum, negativity, support, root residual |
| C7 | cosmetic zeroing is post-validity, bounded by `[-1e-12, 0)`, re-verified on the retained matrix, and its delta is recorded |
| C8 | the negativity band `[-1e-10, -1e-12)` is retained and recorded, never zeroed |
| C9 | both the `T^(k)`-side and the `P`-side support checks run, against the declared masks |
| C10 | the transition support and the `W` support are declared separately; the `W` diagonal is always false |
| C11 | 64 starts exactly, seed `20260919`, parameter-free start distribution, fixed draw order, no extra starts after results |
| C12 | max 5000 iterations per start; a non-converged start is recorded, never restarted |
| C13 | every applicable route runs; no outcome-driven stopping |
| C14 | the route execution order (R1–R4) is not the bridge-convention preference order (P3B §2.6) |
| C15 | a spread violation or a degenerate `m_i(P) <= 0` ⇒ `NOT_IDENTIFIED_BY_ANNUALIZATION` and no empirical `W` target |
| C16 | T2 is an approximation unless it independently passes the root residual |
| C17 | no tolerance, threshold, seed, start count, route set or claim rule is changed after an outcome is observed |
| C18 | E3 promotion is a human act; DSH never self-promotes |
| C19 | `lambda_ij` and `ell_i` remain two separate provenance fields, tied only by `(C-LINK)` |
| C20 | the frozen values in this document and in `configs/dlh_wl_p3c_bridge_readiness.toml` are identical |
