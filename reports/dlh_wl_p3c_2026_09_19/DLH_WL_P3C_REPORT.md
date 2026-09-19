# DLH-WL-P3C — bridge execution-readiness freeze — report

Issue: **#82 / `DLH-WL-P3C`**. Owner route: `DLH-WL-V1-20260918`.
Authority marker: `DLH_WL_P3C_EXECUTION_READINESS_FREEZE_AUTHORIZED`.
Reviewer activation comment: **`5741497930`**.
Reviewer HOLD remediated by this revision: **`5741651898`** (items A–E, §6.1).
Operative baseline: `2b7b0b7d506907ecbf41509bc526ad2b5ea794a6`.
Dedicated branch: `dsh/issue-82-dlh-wl-p3c-execution-readiness-freeze-2026-09-19`.

---

## 0. Terminal

```
DLH_WL_P3C_EXECUTION_READINESS_FREEZE__PASS__HUMAN_SOURCE_VERIFICATION_PENDING
```

The execution-readiness contract is frozen and internally consistent; the human/source
verification packet is complete and **entirely unresolved**, so no real bridge execution is
authorized or possible yet.

### 0.1 Terminal selection (Issue #82 §8)

| Terminal | Selected? | Reason |
|---|---|---|
| `DLH_WL_P3C_EXECUTION_READINESS_FREEZE__PASS__HUMAN_SOURCE_VERIFICATION_PENDING` | **YES — selected** | every PASS condition of Issue #82 §8 holds: all sixteen Reviewer thresholds are represented consistently in the documents and the TOML; the tolerance-level candidate-set versus exact-root-set semantics are explicit, the alias map to P3B is declared and the `F_search_tol ⊆ F_all_exact` implication is withdrawn rather than asserted; uniqueness and non-existence claims are fail-closed with a closed four-term vocabulary and a certificate requirement; the human verification packet is complete (H1–H7, each with question, required primary evidence, decision tokens and fail-closed consequence); and no data, bridge or model execution occurred. |
| `DLH_WL_P3C_EXECUTION_READINESS_FREEZE__REVIEW_REQUIRED` | no | not selected: after this bounded remediation no threshold, tolerance, search parameter or status term is internally inconsistent, and no P3B condition is left undecided by this freeze. The five HOLD `5741651898` items A–E were closed by content correction with all sixteen Reviewer numeric thresholds unchanged (§6.1): the support check now applies to the candidate annual `P` only, the candidate set is named `F_search_tol` with the `⊆ F_all_exact` implication withdrawn, `[-1e-10, -1e-12)` is `NUMERIC_SIGN_AMBIGUOUS__NOT_BRIDGE_USABLE`, exactly 64 optimizer starts are executed for every window, and a degenerate origin is a row-level condition instead of a whole-window failure. |

`HUMAN_SOURCE_VERIFICATION_PENDING` is part of the selected terminal, not a caveat on it: the
packet it refers to is complete **and** entirely unresolved, which is exactly the intended state
before any real transition matrix is inspected.

## 1. Deliverables

| # | Path | Role |
|---|---|---|
| 1 | `docs/specifications/DLH_WL_P3C_EXECUTION_READINESS_FREEZE_2026_09_19.md` | the freeze: thresholds, the P3B condition each tolerance decides, `F_all_exact`/`F_search_tol` semantics, closed status vocabulary, deterministic search protocol, claim ceiling, invariants |
| 2 | `docs/data/DLH_WL_P3C_HUMAN_SOURCE_VERIFICATION_PACKET_2026_09_19.md` | the E3 packet H1–H7, each with question, required primary evidence, decision tokens, fail-closed consequence |
| 3 | `configs/dlh_wl_p3c_bridge_readiness.toml` | machine-readable mirror of every threshold, search parameter and status vocabulary |
| 4 | this report | Issue report and terminal |

## 2. What was read (fresh, read-only)

1. `AGENTS.md`, `tasks/TASK_INDEX_CURRENT.md`;
2. Owner route freeze `docs/decisions/DLH_OWNER_ROUTE_FREEZE_WL_V1_2026_09_18.md`;
3. accepted P3B preregistration at integration `1819b0a5a36b2a8ffde3641c711892df2cdcede7` —
   `docs/specifications/DLH_WL_P3B_BRIDGE_PREREGISTRATION_2026_09_19.md`,
   `docs/data/DLH_WL_P3B_SOURCE_BRIDGE_SENSITIVITY_MATRIX_2026_09_19.md`,
   `docs/data/DLH_WL_P3B_REGION_MELL_PROVENANCE_CONTRACT_2026_09_19.md` — read in particular for
   the `(A1)`–`(A4)` admissibility conditions, the generator conditions, the `C1` applicability
   check, the §2.6 selection rule S1–S5, the sensitivity axes, the region fail-closed rules and
   the `lambda`/`ell` separation;
4. Issue #82 body, activation comment `5741497930` and Reviewer HOLD `5741651898` (items A–E).

No dataset, microdata, tabulation, codebook, licence text or full text was opened. No external
metadata query was issued: every item this Issue needed was either a Reviewer-frozen number or a
requirement statement, not an external fact.

## 3. Threshold / config consistency

All sixteen Reviewer-frozen values are represented identically in the freeze document and in the
TOML, and each is bound to the P3B condition it decides.

| Frozen value | Number | Where it is bound in P3B |
|---|---|---|
| `pi_max` | `0.15` | `C1`, the T2 applicability check (P3B §2.3) |
| `tau_W_abs` | `0.02` | the `tau_W` tolerance of P3B §2.6 rule S5, now named and finite |
| `tau_m_abs` | `0.02` | same rule, extended to the outflow-share spread |
| `unmappable_mass_share_max` | `0.01` | the region-mapping threshold P3B left `TO_BE_FROZEN` |
| row-sum absolute tolerance | `1e-10` | (A2) row-stochasticity |
| stochastic non-negativity hard failure | below `-1e-10` | (A1) non-negativity |
| negativity middle band — **derived from the two frozen values, not a new threshold** | `[-1e-10, -1e-12)` | `NUMERIC_SIGN_AMBIGUOUS__NOT_BRIDGE_USABLE`, diagnostic only (item C) |
| cosmetic zeroing band | `[-1e-12, 0)` | canonicalization within (A1) |
| forbidden-support mass tolerance | `1e-12` | (A3) support admissibility |
| exact k-step root residual | `1e-8` | (A4) window consistency |
| generator row-sum tolerance | `1e-10` | generator condition `Q·1 = 0` |
| generator off-diagonal hard failure | below `-1e-10` | generator condition `Q_ij ≥ 0, i ≠ j` |
| discovered-root dedup threshold | `1e-7` | `F_search_tol` candidate identity |
| imaginary-part tolerance | `1e-10` | reality of a candidate matrix / root / logarithm |
| multistart RNG seed | `20260919` | R4 |
| deterministic constrained starts | `64` | R4 — **exactly 64 executed optimizer starts per window** (item D) |
| max iterations per start | `5000` | R4 |

This closes the four items P3B explicitly left open — `tau_W`, `pi_max`, the unmappable-mass
threshold and the search parameters — **before any source is opened**, which is exactly the
condition P3B attached to them.

**Bounded remediation under HOLD `5741651898`.** The first revision of this report and of the freeze
contained five semantics the Reviewer correctly rejected (items A–E). All five were corrected by
content change, with **all sixteen Reviewer numeric thresholds unchanged**. In summary:

1. **A — support semantics.** The `T^(k)`-side global block failure was **removed**: a k-step matrix
   legitimately carries mass on pairs that are not annual direct edges, via indirect paths. Only the
   candidate annual `P` is tested against the annual transition support; positive `T^(k)` mass on a
   non-annual pair is the non-failing diagnostic `MULTISTEP_MASS_ON_NON_ANNUAL_PAIR`; for the T2 route
   alone, ineligibility is recorded as `T2_SUPPORT_ELIGIBILITY_FAIL`.
2. **B — exact roots versus numerical candidates.** `F_all`/`F_search` are renamed
   `F_all_exact`/`F_search_tol`, and the unconditional subset claim is **withdrawn**
   (`F_search_tol_is_subset_of_F_all_exact = NOT_ASSERTED`). Only the certified subset
   `{ P ∈ F_search_tol : exact_root_certified(P) = true } ⊆ F_all_exact` is asserted.
3. **C — negativity middle band.** `[-1e-10, -1e-12)` is
   `NUMERIC_SIGN_AMBIGUOUS__NOT_BRIDGE_USABLE`: raw-solver diagnostic only, never entering
   `F_search_tol`, any spread, bridge selection, `m`/`W` construction or any admissibility count.
4. **D — exactly 64 starts.** Every window executes exactly 64 optimizer starts,
   `n_special_valid + (64 − n_special_valid) = 64`; unavailable special starts go to a separate ledger and
   are not optimizer starts; special starts consume no RNG draws.
5. **E — degenerate `m` is row-level.** `m_i(P) = 0` marks only that origin
   `TARGET_UNAVAILABLE_DEGENERATE_OUTFLOW`; the window status is unaffected, the row is excluded from the
   `W` spread and from supervised rows, and no uniform `W` is fabricated for it.

§6.1 records the per-item closure with the corrected statement, its frozen location and the toy-check
evidence. The remaining `W` semantics are unchanged: the **`W` support excludes the diagonal** while the
**transition support includes it** (P1B §3.4).

## 4. Search semantics

### 4.1 `F_all_exact` versus `F_search_tol` (corrected: HOLD `5741651898` item B)

```
F_all_exact  = the mathematical set of all annual stochastic matrices P satisfying P^k = T^(k) EXACTLY
F_search_tol = the finite set of numerically admissible eps-root candidates retained by the
               preregistered search under the frozen tolerances, after deduplication at 1e-7

{ P in F_search_tol : exact_root_certified(P) = true }  subset of  F_all_exact
F_search_tol_is_subset_of_F_all_exact = NOT_ASSERTED
F_search_tol is NEVER reported as complete, global or exhaustive
```

The pre-remediation names `F_all`/`F_search` survive only in the forbidden/superseded list below. The
aliases to P3B are declared so the two documents cannot drift: `F_all_exact` ≡ P3B's `𝓕(T^(k))`;
`F_search_tol` ≡ P3B's `𝓕_enum`, read as a tolerance-level candidate set.

**Why the old subset claim is withdrawn.** A candidate with residual `7e-9` satisfies the frozen
`1e-8` tolerance but is a numerical ε-root candidate, not necessarily an exact mathematical root, so
`F_search ⊆ F_all` was not literally valid and is superseded. Only the certified subset above is
asserted. Every retained candidate therefore carries its `root_residual` and an `exact_root_certified`
flag, the latter `true` only with an analytical/interval/verified-continuation proof. The residual bound
is a **backward-error** statement: it does **not** establish that an exact root exists nearby, which
would require a separate perturbation/conditioning argument. All spread diagnostics are computed over
`F_search_tol` and are **search-defined sensitivity evidence**, never a statement about the complete
exact-root set.

**Fail-closed claim rules.** One numerically admissible candidate ⇒
`ONE_NUMERICALLY_ADMISSIBLE_ROOT_CANDIDATE_FOUND__GLOBAL_NONUNIQUENESS_NOT_EXCLUDED`, never
`UNIQUE_ROOT`. Zero numerically admissible candidates ⇒
`NO_NUMERICALLY_ADMISSIBLE_ROOT_CANDIDATE_FOUND__EXISTENCE_NOT_PROVEN`, never a proof of
non-existence. `GLOBAL_UNIQUENESS_CERTIFIED` requires an analytical, interval, verified-continuation or
equivalent certificate over the admissible domain — a finite search can never produce it.

Closed status vocabulary (**exactly one per window**), as frozen and replaced under HOLD `5741651898`:

```
GLOBAL_UNIQUENESS_CERTIFIED
MULTIPLE_NUMERICALLY_ADMISSIBLE_ROOT_CANDIDATES_FOUND
ONE_NUMERICALLY_ADMISSIBLE_ROOT_CANDIDATE_FOUND__GLOBAL_NONUNIQUENESS_NOT_EXCLUDED
NO_NUMERICALLY_ADMISSIBLE_ROOT_CANDIDATE_FOUND__EXISTENCE_NOT_PROVEN
```

Forbidden terms, allowed only inside a statement that they are forbidden or superseded: `UNIQUE_ROOT`,
`GLOBALLY_UNIQUE`, `NO_ROOT_EXISTS`, `NON_EXISTENCE_PROVEN`, `F_search_IS_F_all`,
`COMPLETE_ROOT_SET`, `ALL_ROOTS_FOUND`, and the superseded pre-remediation wordings
`MULTIPLE_ADMISSIBLE_ROOTS_FOUND`, `ONE_ROOT_FOUND__GLOBAL_NONUNIQUENESS_NOT_EXCLUDED`,
`NO_ADMISSIBLE_ROOT_FOUND__EXISTENCE_NOT_PROVEN`, `ADMISSIBLE_ROOTS_FOUND`.

**Coverage limit recorded with every `F_search_tol` report.** A numerical search over the row simplex
cannot certify that it found everything: a candidate could lie in a basin none of the 64 executed
starts enters. That is precisely why status 1 needs a certificate and why statuses 3 and 4 are phrased
as non-exclusions and non-proofs.

### 4.2 Deterministic search protocol

Routes run in fixed order with no outcome-driven stopping: **R1** principal real k-th root →
**R2** generator/embedding (`Q = (1/k)log(T^(k))`, generator conditions, no uniqueness claim) →
**R3** T2 initialization (only when `C1` passes; stays an approximation unless it independently
passes the root residual) → **R4** constrained multistart.

R4 is frozen in full:

```
parameterization : allowed-support row simplex, bound-constrained
                   variables = allowed transition entries; structural zeros held at exactly 0
                   bounds    = 0 <= P_ij <= 1          -> (A1)
                   equality  = sum_j P_ij = 1 per row  -> (A2)
                   support   = enforced by the variable set -> (A3)
objective        : ||P^k - T^(k)||_F^2
validity metric  : max_abs(P^k - T^(k)) <= 1e-8
rng              : numpy.random.Generator (PCG64) via default_rng, seed 20260919
starts           : EXACTLY 64 EXECUTED OPTIMIZER STARTS FOR EVERY WINDOW
                   executed_starts = n_special_valid + (64 - n_special_valid) = 64
                   n_special_valid = valid special starts among {identity, T2, principal root,
                   embedding}; specials are built in P-space and consume NO RNG draws
                   invalid specials -> separate special_start_unavailable ledger, and they are
                   NOT optimizer starts, so they never reduce the 64 executed starts
                   random starts   = 64 - n_special_valid from one continuous stream,
                   Dirichlet(alpha = 1) on the allowed-support row simplex,
                   draw order = ascending origin row, ascending allowed entry, ascending start
extra starts / restarts / family changes after seeing results : NOT ALLOWED
max iterations   : 5000 per start; a non-converged start is recorded, never restarted
scope            : joint over all origins (P^k couples rows)
```

Three design decisions are recorded with their reasons rather than left implicit:

- **softmax / logit row parameterization is explicitly rejected.** A softmax cannot attain an
  exact interior zero, so a candidate with a genuine interior zero would be unreachable — silently
  shrinking `F_search_tol` and weakening exactly the completeness question this Issue exists to
  protect. The bound-constrained simplex keeps such candidates reachable.
- **the start-distribution constants are Reviewer-ratified design constants.** `default_rng`/PCG64 and
  `Dirichlet(alpha = 1)` are pre-execution search-design constants ratified by the Reviewer (HOLD
  `5741651898` item D). They are **no longer described as "parameter-free"**, which would misdescribe
  them as threshold-free rather than as Builder-chosen-but-ratified design constants; no
  Builder-invented number enters a Reviewer-frozen contract.
- **the RNG stream is version-dependent, and that is disclosed rather than hidden.** The contract
  requires the implementation to record the NumPy version and a **start-manifest hash** over all 64
  executed start matrices, so the actual starts are auditable even if a future NumPy release changes
  the stream for the same seed.

### 4.3 Route execution order versus bridge-convention preference

P3B froze a preference order (generator embedding → principal real non-negative root → T2 if `C1`
passes → fail closed). P3C freezes R1→R2→R3→R4 as the **execution** order. These are different
objects and the difference is frozen explicitly so it cannot be read as a contradiction:
**R1–R4 decides which candidate generators are run and in what order to build `F_search_tol`; the
P3B order decides which discovered root becomes the selected bridge convention.** The preference
selects a convention, not an identification theorem, and alternative discovered roots and their
spreads remain reportable.

### 4.4 Support semantics (corrected: HOLD `5741651898` item A)

**The `T^(k)`-side global block failure of the first revision is removed.** `T^(k)` is a **k-step**
matrix: where the annual direct edge `i → j` is forbidden but an allowed indirect path
`i → l → … → j` exists, `T^(k)_ij > 0` is the expected behaviour, not a contradiction. Applying the
annual transition support to `T^(k)` would fail essentially every non-trivial window closed; a
synthetic counterexample is recorded in §6.1 (toy check A1: a 3-origin allowed support with
`(0,2)` forbidden annually still gives `T^(2)_02 = 1/4` through the allowed path `0 → 1 → 2`).

The corrected rules are frozen as:

1. **Annual support is tested on the candidate annual `P` only.** Forbidden *annual* mass `≤ 1e-12`,
   else the candidate is rejected. R1, R2 and R4 check only candidate annual `P`.
2. **Positive `T^(k)` mass on a non-annual pair is a diagnostic, not a failure**:
   `MULTISTEP_MASS_ON_NON_ANNUAL_PAIR`, recorded with count, location and magnitude.
3. **T2 alone is affected by the `T^(k)`-side test.** Because T2 sets `P̂_ij = T^(k)_ij / k`, a
   positive `T^(k)_ij` on a pair forbidden by the **annual** transition support makes T2 ineligible;
   that is recorded as `T2_SUPPORT_ELIGIBILITY_FAIL` and scoped to T2 only. `P^k` is therefore
   **allowed** to carry positive mass on non-annual pairs.

Two masks are still declared separately:

- the **transition support** includes the diagonal — `P_ii` is home retention and is a real allowed
  transition;
- the **`W` support** always excludes the diagonal (P1B §3.4).

Conflating them would either forbid self-transitions or leak the diagonal into the conditional target.

## 5. Human/source verification packet

Seven items, all `UNRESOLVED`, none promoted:

| Item | Subject | Blocking scope if unresolved |
|---|---|---|
| H1 | NBS transition semantics (current residence, 5-years-earlier residence, orientation, diagonal, universe, weights, missing categories, reference date) | all T-family waves |
| H2 | census / 1% table availability and vintage, with **no secondary-paper substitution** | affected wave |
| H3 | region coding: pinned code standard/version, source convention, the **2000-wave Chongqing / 1995-residence treatment**, HK/Macao/Taiwan, XPCC, merged/absent units | all region-joined objects; the 2000 wave specifically |
| H4 | source weights, cross-wave weight comparability, questionnaire and sample-design changes | survey-derived waves; cross-wave pooling |
| H5 | pair labor-intensity `lambda_ij = rho_ij·phi_ij`, or an explicit decision to use the preregistered share-equivalence approximation | population→labor bridge (all families) |
| H6 | origin labor amount `ell_i` on a declared basis, time-aligned and not post-decision | conditional denominator (all families) |
| H7 | feature/label/publication timing and leakage; the split claim actually supported | predictive information set (all waves) |

**Packet rules.** No self-promotion: E3 promotion is a human/Owner act, the Builder prepared the
packet and resolved nothing. No answer may be inferred from a secondary paper, dataset title,
mirror page, reseller listing or another document's citation. A primary official source is
required for H1–H4. Resolving an item authorises a **decision**, not a download. While an item a
source needs is unresolved, that source family is **blocked for that wave** — an unresolved item
may never be read as "assume the neutral reading". A blocked wave is a legitimate outcome.

**`lambda_ij` and `ell_i` remain two independent provenance fields.** Separate field names,
separate `*_provenance_id` values, neither inferable from or usable to validate the other, tied
only by `(C-LINK)` `ell_i = ell_i^movers + ell_i^stay + ell_i^unobserved`, to be supplied from one
coherent frame or declared with a reported residual. `one_coherent_frame_proven = false`, so both
items must currently be satisfied independently.

Aggregate packet status: **7 of 7 unresolved · 0 promoted by DSH · 0 datasets opened.**

## 6. Consistency checks performed

Only the checks Issue #82 §10 allows: TOML parse, cross-document threshold consistency,
static/symbolic reasoning and deterministic-search pseudocode review.

- **TOML parses** with the Python standard-library `tomllib`; 14 top-level keys (12 of them
  tables) and 246 leaf values; LF SHA-256
  `C232D43FE1D1923A6C2DC380D596E1AF1B33612D4654E3D5DC813CAC2FA8E3B1`.
- **all sixteen frozen numbers are byte-identical** between the freeze document and the TOML.
- **every tolerance is bound** to the P3B condition it decides, with no tolerance left
  unassigned and no P3B condition left undecided.
- **`F_all_exact`/`F_search_tol` are distinguished everywhere**, the P3B alias map is declared, the
  `F_search_tol ⊆ F_all_exact` implication is withdrawn rather than asserted, and every occurrence of
  a forbidden or superseded term sits inside a statement that it is forbidden or superseded.
- **the closed status vocabulary is stated once and reused**, with exactly one status required
  per window.
- **the pseudocode contains no branch that can reach `GLOBAL_UNIQUENESS_CERTIFIED` without a
  certificate.**
- **no numeric empirical value appears anywhere**: no transition matrix, no root, no `m`, no
  `ell`, no `W`, no region mass.

No real matrix was executed by any of these checks, and no source file was ingested.

### 6.1 Bounded remediation closure — HOLD `5741651898` items A–E

| Item | Reviewer finding | Corrected statement now frozen | Frozen location | Toy-check evidence |
|---|---|---|---|---|
| **A** | the `T^(k)`-side global support check was mathematically wrong | only the **candidate annual `P`** is tested against the annual transition support (forbidden annual mass `≤ 1e-12` else the candidate is rejected, R1/R2/R4); positive `T^(k)` mass on a non-annual pair is the **non-failing** diagnostic `MULTISTEP_MASS_ON_NON_ANNUAL_PAIR`; T2-only ineligibility is `T2_SUPPORT_ELIGIBILITY_FAIL`; `P^k` may carry positive mass on non-annual pairs | freeze §2.2, §4.2, §4.4; TOML `[numerical.support]`, `[status_vocabulary.route]` | A1–A5 |
| **B** | `F_search ⊆ F_all` was not literally valid and the two objects were conflated | `F_all_exact` (exact roots of `P^k = T^(k)`) separated from `F_search_tol` (numerically admissible ε-root candidates under the frozen tolerances); unconditional subset claim **withdrawn**; per-candidate `root_residual` + `exact_root_certified`; the residual bound is backward-error only; spreads are search-defined sensitivity evidence; closed four-term vocabulary | freeze §3.1–§3.3, §4; TOML `[root_sets]`, `[status_vocabulary.uniqueness]` | static/symbolic |
| **C** | `[-1e-10, -1e-12)` cannot be "admissible" while retaining a negative entry | `NUMERIC_SIGN_AMBIGUOUS__NOT_BRIDGE_USABLE`: raw-solver diagnostic only, excluded from `F_search_tol`, spreads, bridge selection, `m`/`W` and admissibility counts; admission requires a retained matrix entrywise `≥ 0`, after which row-sum, annual-support and residual checks are re-run | freeze §2.1; TOML `[numerical]` | C1–C9 |
| **D** | the slot-based rule could execute fewer than 64 starts | `executed_starts = n_special_valid + (64 − n_special_valid) = 64` for **every** window; invalid specials go to a separate `special_start_unavailable` ledger and are not optimizer starts; specials consume no RNG draws; `default_rng`/PCG64 and `Dirichlet(alpha = 1)` declared as Reviewer-ratified design constants; NumPy version + start-manifest hash over all 64 executed starts retained | freeze §4.2; TOML `[search]`, `[search.R4_constrained_multistart]` | D1–D6 |
| **E** | the whole-window degenerate failure was wrong; P1B's rule is row-specific | `m_i(P) = 0` marks **only that origin** `TARGET_UNAVAILABLE_DEGENERATE_OUTFLOW`, excluded from the `W` spread and from supervised/evaluation rows, with **no** fabricated uniform `W`; window root status unaffected; `m_i < 0` invalid through the negativity rules; `m` spread over **all** origins, `W` spread over non-degenerate origins only; whole-panel completeness is a separate design gate | freeze §1.5, §5.6; TOML `[row_availability]` | E1–E5 |

**Vocabulary mirror completed (no numeric change).** The route-status vocabulary in the TOML now mirrors
both route-status terms the freeze document uses — `C1_FAILED` for a `pi_max` applicability failure (P3B
`C1`) and `T2_SUPPORT_ELIGIBILITY_FAIL` for the T2-only support rule — and the row vocabulary mirrors
`TARGET_UNAVAILABLE_DEGENERATE_OUTFLOW`. No threshold, tolerance or search parameter was touched by this
completion; it removes a vocabulary-mirror gap only.

**Reviewer numeric thresholds: sixteen, all unchanged by this remediation.** Every value was re-parsed
from the TOML and compared against the §3 table: `pi_max = 0.15`, `tau_W_abs = 0.02`,
`tau_m_abs = 0.02`, `unmappable_mass_share_max = 0.01`, row-sum tolerance `1e-10`, negativity hard
failure `< -1e-10`, cosmetic-zeroing band `[-1e-12, 0)`, forbidden-support tolerance `1e-12`, exact
k-step root residual `1e-8`, generator row-sum tolerance `1e-10`, generator off-diagonal hard failure
`< -1e-10`, root dedup `1e-7`, imaginary-part tolerance `1e-10`, RNG seed `20260919`, 64 deterministic
start slots, 5000 max iterations per start.

**Toy/synthetic checks (25, exact rational arithmetic, zero empirical values).** Only the checks Issue
#82 §10 allows were used: TOML parse, cross-document static consistency, symbolic reading and
toy-matrix reasoning. The toy checks were performed outside the repository with a synthetic 3×3
allowed-support matrix, a synthetic negativity sweep over the two frozen thresholds and their interior,
a synthetic start-count enumeration and a synthetic `m` vector; no artifact was added to the allowlist
and no empirical number was produced. Results: **A1–A5, C1–C9, D1–D6, E1–E5 all PASS (25/25)**,
including the A1 counterexample that invalidated the old `T^(k)`-side failure and the C7/C9 cases
showing that a candidate retaining a sign-ambiguous or hard-failing entry is rejected before any spread
is computed. A separate 115-check static/TOML pass over all four artifacts reports **115 PASS / 0 FAIL**,
including the 16/16 unchanged Reviewer thresholds.

**Unchanged by this remediation:** the four-path allowlist, the ancestry and authority chain
(→ P3B preregistration → Issue #82 → activation `5741497930` → HOLD `5741651898`), the H1–H7
human/source packet (7 of 7 `UNRESOLVED`, 0 self-promoted, 0 promoted by DSH), the selected terminal and
its direction, and the zero-execution accounting of §7.

## 7. Prohibited-action accounting (all zero)

| Item | Count |
|---|---|
| real transition matrix inspected or executed | **0** |
| bridge implementations or empirical adapters | **0** |
| datasets downloaded, scraped, purchased, ingested or opened | **0** |
| external metadata queries issued | **0** |
| scientific / model / training / empirical-bridge calls | **0** |
| fits, estimates, optimizations, calibrations | **0** |
| HJB / KFE / GE / MATLAB / household calls | **0** |
| `pytest` / full-suite runs | **0** |
| evidence levels promoted | **0** |
| frozen values invented by the Builder | **0** (all sixteen come from the Reviewer; the start-distribution constants are declared as Reviewer-ratified design constants, not Builder-invented values) |
| numeric empirical values emitted | **0** |
| source code, tests, config outside the allowlist, CURRENT governance or P3B artifacts touched | **0** |
| PRs, merges, closes, successors or self-acceptances | **0** |

Only the Issue #82 §10 check classes were used in this revision: TOML parse, cross-document static
consistency, symbolic reading and deterministic-search pseudocode review, plus toy-matrix checks on
synthetic inputs (25 toy checks, 115 static checks, both fully passing). Every toy input is synthetic or
exact rational arithmetic; **no empirical value** was read, produced or emitted by any of them.

## 8. Exact changed paths (4 — exactly the Issue #82 allowlist)

```
docs/specifications/DLH_WL_P3C_EXECUTION_READINESS_FREEZE_2026_09_19.md
docs/data/DLH_WL_P3C_HUMAN_SOURCE_VERIFICATION_PACKET_2026_09_19.md
configs/dlh_wl_p3c_bridge_readiness.toml
reports/dlh_wl_p3c_2026_09_19/DLH_WL_P3C_REPORT.md
```

Nothing else was created or modified: no source code, no tests, no CURRENT governance document,
no P3B artifact, no P2/P2D artifact.

Artifact identity (LF-normalised SHA-256):

```
freeze specification   CF3224210396BBA004C392F03814EDC1B8282F13221490544F8295990EC4D349
human packet           9AB077D9569BC5E6AC52985387932311F19611E7B493966A13866F7FD9D5FFDF
readiness TOML         C232D43FE1D1923A6C2DC380D596E1AF1B33612D4654E3D5DC813CAC2FA8E3B1
report                 319C5287C7A3E31B5C0411D227D5C42F15DD0B9AC08E73D74F28F3CD6FD95C40
```

The `report` value is the LF SHA-256 of this report **with its own identity line removed**, so the
value is reproducible from the committed artifact instead of being self-referential; the other three
values are the plain LF SHA-256 of the named files as committed.

The `report` value is the LF SHA-256 of this report **with its own identity line removed**, so the
value is reproducible from the committed artifact instead of being self-referential; the other three
values are the plain LF SHA-256 of the named files as committed.

The `report` value is the LF SHA-256 of this report **with its own identity line removed**, so the
value is reproducible from the committed artifact instead of being self-referential; the other three
values are the plain LF SHA-256 of the named files as committed.

The `report` value is the LF SHA-256 of this report **with its own identity line removed**, so the
value is reproducible from the committed artifact instead of being self-referential; the other three
values are the plain LF SHA-256 of the named files as committed.

This bounded remediation changed three of the four allowlisted paths — the freeze specification, the
readiness TOML and this report. The human/source verification packet was re-read against items A–E and
required **no change** (its terminology was unaffected), so its identity is unchanged at
`9AB077D9569BC5E6AC52985387932311F19611E7B493966A13866F7FD9D5FFDF`.

## 9. Interpretation ceiling

Allowed by this Issue: the freeze itself; the statement that the packet is complete and
unresolved; the statement that no real bridge execution is authorized ; the declaration that only the
certified subset `{ P ∈ F_search_tol : exact_root_certified(P) = true }` is contained in `F_all_exact`, with the
unconditional subset claim withdrawn, and that no uniqueness or non-existence claim is available.

Explicitly **not** claimed: that any source exists, is available, is licensed or is accessible;
that any source's semantics, schema, codes, weights or timings have been verified; that any
transition matrix exists in a usable form; that any admissible root exists for any real window;
that any root is unique or non-unique; that any `lambda_ij` or `ell_i` source exists; that any
coherent single frame supplies both; any empirical China estimate of any kind; any annual
bilateral OD availability claim; any unseen-region, causal, welfare, policy, GE, HJB/KFE or
household claim; any model-performance statement.

## 10. What happens next, and what does not

This Issue authorizes **nothing executable**. The next step is a **human** pass over the H1–H7
packet; DSH cannot perform it and cannot promote anything. Only after the items a given wave
needs are resolved as documented — and after a separately authorized Issue — could the
preregistered bridge be implemented against this frozen contract, with the same tolerances, the
same route set and order, the same exactly-64-executed-start construction and the same claim ceiling.

## 11. Terminal

```
DLH_WL_P3C_EXECUTION_READINESS_FREEZE__PASS__HUMAN_SOURCE_VERIFICATION_PENDING
```
