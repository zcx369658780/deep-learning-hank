# DLH-WL-P3C — bridge execution-readiness freeze — report

Issue: **#82 / `DLH-WL-P3C`**. Owner route: `DLH-WL-V1-20260918`.
Authority marker: `DLH_WL_P3C_EXECUTION_READINESS_FREEZE_AUTHORIZED`.
Reviewer final activation comment: **`5741497930`**.
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
| `DLH_WL_P3C_EXECUTION_READINESS_FREEZE__PASS__HUMAN_SOURCE_VERIFICATION_PENDING` | **YES — selected** | every PASS condition of Issue #82 §8 holds: all sixteen Reviewer thresholds are represented consistently in the documents and the TOML; the finite-search versus global-root-set semantics are explicit and the alias map to P3B is declared; uniqueness and non-existence claims are fail-closed with a closed four-term vocabulary and a certificate requirement; the human verification packet is complete (H1–H7, each with question, required primary evidence, decision tokens and fail-closed consequence); and no data, bridge or model execution occurred. |
| `DLH_WL_P3C_EXECUTION_READINESS_FREEZE__REVIEW_REQUIRED` | no | not selected: no threshold, tolerance, search parameter or status term is internally inconsistent, and no P3B condition is left undecided by this freeze. The two interpretive decisions P3C did have to make are declared in place rather than left as silent choices — the negativity band `[-1e-10, -1e-12)` is handled as retain-and-record, and the degenerate-root rule is added fail-closed — and each is flagged for the Reviewer. Should the Reviewer disagree with either reading, the correct response is a dated pre-execution amendment, not a re-scoping of this Issue. |

`HUMAN_SOURCE_VERIFICATION_PENDING` is part of the selected terminal, not a caveat on it: the
packet it refers to is complete **and** entirely unresolved, which is exactly the intended state
before any real transition matrix is inspected.

## 1. Deliverables

| # | Path | Role |
|---|---|---|
| 1 | `docs/specifications/DLH_WL_P3C_EXECUTION_READINESS_FREEZE_2026_09_19.md` | the freeze: thresholds, the P3B condition each tolerance decides, `F_all`/`F_search` semantics, closed status vocabulary, deterministic search protocol, claim ceiling, invariants |
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
4. Issue #82 body and activation comment `5741497930`.

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
| cosmetic zeroing band | `[-1e-12, 0)` | canonicalization within (A1) |
| forbidden-support mass tolerance | `1e-12` | (A3) support admissibility |
| exact k-step root residual | `1e-8` | (A4) window consistency |
| generator row-sum tolerance | `1e-10` | generator condition `Q·1 = 0` |
| generator off-diagonal hard failure | below `-1e-10` | generator condition `Q_ij ≥ 0, i ≠ j` |
| discovered-root dedup threshold | `1e-7` | `F_search` reporting identity |
| imaginary-part tolerance | `1e-10` | reality of a candidate matrix / root / logarithm |
| multistart RNG seed | `20260919` | R4 |
| deterministic constrained starts | `64` | R4 |
| max iterations per start | `5000` | R4 |

This closes the four items P3B explicitly left open — `tau_W`, `pi_max`, the unmappable-mass
threshold and the search parameters — **before any source is opened**, which is exactly the
condition P3B attached to them.

**Two additions P3C made, both fail-closed, both flagged for the Reviewer:**

1. **Degenerate-root rule.** If any retained root has `min_i m_i(P) ≤ 0`, the window fails closed
   to `NOT_IDENTIFIED_BY_ANNUALIZATION` **regardless of the measured spreads**. Enforcing only
   the spread statistic would let a `0/0` conditional-share cell pass unnoticed; P1B §2.2 item 5
   already forbids fabricating a label for a block with `m_i = 0`.
2. **Negativity band `[-1e-10, -1e-12)` = retain-and-record, never zero.** The two frozen
   negativity numbers leave this band in neither the hard-failure nor the cosmetic-zeroing
   category. P3C treats such an entry as acceptable floating-point noise (root admissible) but
   **does not canonicalize it**, recording its count, minimum and location. If the Reviewer
   intended the cosmetic band to cover the whole `[-1e-10, 0)` range, that is a dated
   pre-execution amendment; P3C does not assume it.

## 4. Search semantics

### 4.1 `F_all` versus `F_search`

```
F_all     = the mathematical set of all admissible annual stochastic roots P of P^k = T^(k)
F_search  = the finite set of admissible roots discovered by the preregistered search,
            retained after deduplication at 1e-7
F_search subset of F_all ;  F_search is NEVER reported as complete or global
```

The aliases to P3B are declared so the two documents cannot drift: `F_all` ≡ P3B's `𝓕(T^(k))`;
`F_search` ≡ P3B's `𝓕_enum`.

**Fail-closed claim rules.** One numerical root ⇒
`ONE_ROOT_FOUND__GLOBAL_NONUNIQUENESS_NOT_EXCLUDED`, never `UNIQUE_ROOT`. Zero numerical roots ⇒
`NO_ADMISSIBLE_ROOT_FOUND__EXISTENCE_NOT_PROVEN`, never a proof of non-existence.
`GLOBAL_UNIQUENESS_CERTIFIED` requires an analytical, interval, verified-continuation or
equivalent certificate over the admissible domain — a finite search can never produce it.

Closed status vocabulary (**exactly one per window**), as frozen:

```
GLOBAL_UNIQUENESS_CERTIFIED
MULTIPLE_ADMISSIBLE_ROOTS_FOUND
ONE_ROOT_FOUND__GLOBAL_NONUNIQUENESS_NOT_EXCLUDED
NO_ADMISSIBLE_ROOT_FOUND__EXISTENCE_NOT_PROVEN
```

Forbidden terms, allowed only inside a statement that they are forbidden: `UNIQUE_ROOT`,
`GLOBALLY_UNIQUE`, `NO_ROOT_EXISTS`, `NON_EXISTENCE_PROVEN`, `F_search_IS_F_all`,
`COMPLETE_ROOT_SET`, `ALL_ROOTS_FOUND`.

**Coverage limit recorded with every `F_search` report.** A numerical search over the row simplex
cannot certify that it found everything: a root could lie in a basin none of the 64 starts
enters. That is precisely why status 1 needs a certificate and why statuses 3 and 4 are phrased
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
starts           : exactly 64 = 4 special (identity, T2, principal root, embedding) in P-space
                   with NO random draws + 60 from one continuous stream,
                   Dirichlet(alpha = 1) on the allowed-support row simplex,
                   draw order = ascending origin row, ascending allowed entry, ascending start
extra starts / restarts / family changes after seeing results : NOT ALLOWED
max iterations   : 5000 per start; a non-converged start is recorded, never restarted
scope            : joint over all origins (P^k couples rows)
```

Three design decisions are recorded with their reasons rather than left implicit:

- **softmax / logit row parameterization is explicitly rejected.** A softmax cannot attain an
  exact interior zero, so an admissible root with a genuine interior zero would be unreachable —
  silently shrinking `F_search` and weakening exactly the completeness question this Issue
  exists to protect. The bound-constrained simplex keeps such roots reachable.
- **the start distribution has no free numeric parameter.** `Dirichlet(alpha = 1)` is
  parameter-free, so no Builder-invented number enters a Reviewer-frozen contract.
- **the RNG stream is version-dependent, and that is disclosed rather than hidden.** The contract
  requires the implementation to record the NumPy version and a **start-manifest hash** over the
  64 generated start matrices, so the actual starts are auditable even if a future NumPy release
  changes the stream for the same seed.

### 4.3 Route execution order versus bridge-convention preference

P3B froze a preference order (generator embedding → principal real non-negative root → T2 if `C1`
passes → fail closed). P3C freezes R1→R2→R3→R4 as the **execution** order. These are different
objects and the difference is frozen explicitly so it cannot be read as a contradiction:
**R1–R4 decides which candidate generators are run and in what order to build `F_search`; the
P3B order decides which discovered root becomes the selected bridge convention.** The preference
selects a convention, not an identification theorem, and alternative discovered roots and their
spreads remain reportable.

### 4.4 Two support checks against two distinct masks

P3C freezes **both** the `T^(k)`-side pre-check (no positive off-diagonal of the observed window
on a pair forbidden by the declared annual transition support; positive means `> 1e-12`,
otherwise the block fails closed) **and** the `P`-side check (forbidden mass `<= 1e-12`, else the
root is rejected). It also freezes that two masks must be declared separately:

- the **transition support** includes the diagonal — `P_ii` is home retention and is a real
  allowed transition;
- the **`W` support** always excludes the diagonal (P1B §3.4).

Conflating them would either forbid self-transitions (making every root inadmissible) or allow the
diagonal into the conditional target.

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

- **TOML parses** with the Python standard-library `tomllib`; 13 top-level keys (11 of them
  tables) and 176 leaf values; LF SHA-256
  `D2F238EB035F5DE35572BCA33487369DB832F5AAF85E2956BA2D4AD4E07A688A`.
- **all sixteen frozen numbers are byte-identical** between the freeze document and the TOML.
- **every tolerance is bound** to the P3B condition it decides, with no tolerance left
  unassigned and no P3B condition left undecided.
- **`F_all`/`F_search` are distinguished everywhere**, the P3B alias map is declared, and every
  occurrence of a forbidden term sits inside a statement that it is forbidden.
- **the closed status vocabulary is stated once and reused**, with exactly one status required
  per window.
- **the pseudocode contains no branch that can reach `GLOBAL_UNIQUENESS_CERTIFIED` without a
  certificate.**
- **no numeric empirical value appears anywhere**: no transition matrix, no root, no `m`, no
  `ell`, no `W`, no region mass.

No real matrix was executed by any of these checks, and no source file was ingested.

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
| frozen values invented by the Builder | **0** (all sixteen come from the Reviewer; the only parameter-free design choices are declared as such) |
| numeric empirical values emitted | **0** |
| source code, tests, config outside the allowlist, CURRENT governance or P3B artifacts touched | **0** |
| PRs, merges, closes, successors or self-acceptances | **0** |

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
freeze specification   32D016C12065DE520F505A9F8AB53FAB0E0D2C3D36A01EB1558F9F1F297B1890
human packet            9AB077D9569BC5E6AC52985387932311F19611E7B493966A13866F7FD9D5FFDF
readiness TOML          D2F238EB035F5DE35572BCA33487369DB832F5AAF85E2956BA2D4AD4E07A688A
report                  FD4F7FF58BE1CF05C656BFF3415CE48773B7319B8EEE40AD194EE77E382C437E
```

## 9. Interpretation ceiling

Allowed by this Issue: the freeze itself; the statement that the packet is complete and
unresolved; the statement that no real bridge execution is authorized ; the declarations that
`F_search` is a subset of `F_all` and that no uniqueness or non-existence claim is available.

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
same route set and order, the same 64-start construction and the same claim ceiling.

## 11. Terminal

```
DLH_WL_P3C_EXECUTION_READINESS_FREEZE__PASS__HUMAN_SOURCE_VERIFICATION_PENDING
```
