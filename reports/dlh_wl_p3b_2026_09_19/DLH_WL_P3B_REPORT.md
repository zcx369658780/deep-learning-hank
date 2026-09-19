# DLH-WL-P3B — bridge / source preregistration gate — report

Issue: **#81 / `DLH-WL-P3B`**. Owner route: `DLH-WL-V1-20260918`.
Authority marker: `DLH_WL_P3B_BRIDGE_SOURCE_PREREGISTRATION_AUTHORIZED`.
Reviewer final activation comment: **`5741234971`**.
Operative baseline: `1f4bee7290da7143fab9612157bd99f83e3216b4`.
Dedicated branch: `dsh/issue-81-dlh-wl-p3b-bridge-preregistration-2026-09-19`.

---

## 0. Terminal

```
DLH_WL_P3B_BRIDGE_PREREGISTRATION__PASS__CANDIDATE_AVAILABLE
```

At least one source family (T — the NBS census / 1 % sample bilateral multi-year transition
object) carries a mathematically explicit bridge candidate with named assumptions, named
failure conditions and named sensitivity axes. **This does not authorize empirical fitting.**

## 1. Deliverables

| # | Path | Role |
|---|---|---|
| 1 | `docs/specifications/DLH_WL_P3B_BRIDGE_PREREGISTRATION_2026_09_19.md` | the three bridges, their equations, assumptions, failure conditions, selection rule, decision |
| 2 | `docs/data/DLH_WL_P3B_SOURCE_BRIDGE_SENSITIVITY_MATRIX_2026_09_19.md` | source × bridge coverage, per-family matrices, 19-axis sensitivity matrix, prerequisite ledger |
| 3 | `docs/data/DLH_WL_P3B_REGION_MELL_PROVENANCE_CONTRACT_2026_09_19.md` | region dictionary specification, `m` and `ell` provenance rules, weights / harmonization / leakage contract |
| 4 | this report | Issue completion report and terminal |

## 2. What was read (fresh, read-only)

1. `AGENTS.md`, `tasks/TASK_INDEX_CURRENT.md`;
2. Owner route freeze `docs/decisions/DLH_OWNER_ROUTE_FREEZE_WL_V1_2026_09_18.md`;
3. accepted P1B label/schema taxonomy `docs/data/DLH_WL_P1B_LABEL_AND_SAMPLE_SCHEMA_2026_09_18.md`
   (revision 4) — the six-class taxonomy, the derived flags, the support/zero rules, the
   feature-timing rules and the residual open items;
4. accepted P3A Branch-B package:
   `docs/data/DLH_WL_P3A_REAL_DATA_SOURCE_EVIDENCE_2026_09_19.md`,
   `docs/data/DLH_WL_P3A_REGION_TIME_SUPPORT_MATRIX_2026_09_19.md`,
   `docs/specifications/DLH_WL_P3A_EMPIRICAL_LABEL_GATE_2026_09_19.md`,
   `reports/dlh_wl_p3a_2026_09_19/DLH_WL_P3A_REPORT.md`;
5. the DLH-1A-R1 feasibility evidence and its E3 verification queue (carried through P3A);
6. Issue #81 body and activation comment `5741234971`.

No dataset, microdata, full text or external file was opened. No external metadata query was
required by this Issue because every prerequisite it needs is a **requirement statement**, not
an external fact; where an external fact would be needed to execute a bridge, it is recorded as
`NOT_VERIFIED_EXTERNAL` or `REQUIRED_EXTERNAL` rather than looked up or guessed.

## 3. Bridge results

### 3.1 Time bridge `T^(k) → P → (m, W)`

The inverse problem is: find an admissible annual `P` (non-negative, row-stochastic,
support-admissible) with `P^k = T^(k)`.

| Result | Statement |
|---|---|
| **T1 existence is not guaranteed** | the 2-region exchange object `T = [[0,1],[1,0]]` admits **no** real non-negative stochastic square root. Proved twice: directly from `x² + (1−x)(1−y) = 0`, and from the eigenvalue argument (eigenvalues `±i` force `bc = −1 − a² < 0`). A window in which regions effectively exchange their populations cannot be annualized at all. |
| **T1 uniqueness is not guaranteed** | the 2-region object `T^(2) = [[5/8,3/8],[3/8,5/8]]` has **two** admissible roots, `[[1/4,3/4],[3/4,1/4]]` and `[[3/4,1/4],[1/4,3/4]]`. The implied annual outflow share is `m = 3/4` or `m = 1/4` — **a factor of three, from identical data**. |
| **the naive rule is invalid** | "divide the k-year off-diagonal by k" gives `3/16` for that example — neither root. It is not a valid annualization. |
| **general multiplicity** | for `n = 2, k = 2` the solution set reduces to `s² − 2s + (A+B) = 0`, which has **two** roots whenever `A + B < 1`. Multiplicity is generic, not a corner case. |
| **the generator route restricts but does not rescue** | embeddability requires `det(T^(k)) > 0` (necessary); the exchange object has `det = −1` and is excluded. For the `T^(2)` example the embedding exists and selects **one** of the two roots (the low-mobility one, off-diagonal `1/4`). Embeddability is not implied by row-stochasticity, and the embedding is not unique in general. |
| **a second window length is unavailable** | all documented waves are `k = 5`, and consecutive non-overlapping windows give one equation each with no nested structure, so the strongest identification route is unavailable. |
| **T2 (low mobility)** | `P̂ = I + (T^(k) − I)/k` is always admissible in (A1)–(A3), with error `P̂ − P = ((k−1)/2)A² + O(‖A‖³)`, i.e. **second order** in the annual hazard scale, or `O((π^(k))²/k)`. Applicability is conditional on the preregistered check `C1: max_i(1 − T^(k)_ii) ≤ pi_max`. |
| **T3 (multi-year proxy)** | exact and error-free as a computation, but **structurally biased**: on the exact annual matrix `circ(1/2, 3/10, 1/5)` with `W = (0.600, 0.400)`, the 2-year proxy is `(0.53968, 0.46032)` — a **10.05 %** understatement with **no annualization error at all**; at `k = 5` it is `≈ 0.50112`, a **16.5 %** understatement. The bias grows with `k` and converges to `π_j/Σ_{l≠i}π_l`, the ergodic composition, **deleting the origin-conditional variation the model exists to learn**. First-order decomposition: `W^(k)_ij ∝ W_ij[1 + ((k−1)/2)(ρ_i^ret − h_j)] + ((k−1)/2)R_ij/h_i`, exposing three channels — return migration, destination turnover, multi-step routing. The bias is **first order** in the mobility scale, one order worse than T1/T2, and **not repairable by better annualization**. |

**Preregistered selection rule (§2.6 of the preregistration):** enumerate `𝓕_enum`; fail closed
if empty; then prefer generator-embedding, else the principal real non-negative stochastic root,
else T2 subject to `C1`, else fail closed; **always report every member of `𝓕_enum` and the
induced spread of `(m, W)`**; declare the window `NOT_IDENTIFIED` if the spread exceeds the
preregistered `tau_W`. `tau_W`, `pi_max` and the search parameters are frozen by Reviewer
authority **before execution** — P3B deliberately does not choose their numeric values, because
choosing them now with no data would be arbitrary and choosing them later would be
outcome-driven selection.

### 3.2 Stock → flow bridge

| Result | Statement |
|---|---|
| accounting | `S_ij = F_ij · D_ij` per cell (Little's law) |
| **exact equality condition** | row-normalized stock shares equal flow shares **iff** expected duration `D_ij` is constant across the origin's destinations. Proved: the stock share equals the **duration-weighted** flow share, so a destination with above-average duration is over-represented by exactly its duration ratio. |
| **turnover is not identified from cross-sections** | `S_ij(t+1) = S_ij(t) − Out_ij(t) + In_ij(t)` is one equation with two unknowns per cell; only the net is identified. The CMDS and the floating-population OD are documented as cross-sections, not panels, so the repeated-snapshot route is **unavailable**. |
| **hukou-origin ≠ previous-residence** | a path `i → k → j` contributes to `S^h_ij` but not to `S^r_ij`; the difference is `O(η²)` and **systematically oriented**, over-counting origins that supply long chains of onward moves. |
| consequence | `stock → flow` is `NOT_IDENTIFIED` for families S and C under currently documented evidence. A constant-duration assumption is admissible **only** as an explicitly preregistered assumption with full sensitivity, never as a convenience. |

### 3.3 Population → labor-service bridge

| Result | Statement |
|---|---|
| observed units | T: all persons. S: floating population, all persons. C: migrants-only frame, unit `NOT_VERIFIED_EXTERNAL`. geodoi: excluded from pair-label design. |
| required assumption | `(P-L)`: `E[φ | i→j] = E[φ | i→any]` for every `j`, i.e. destination choice independent of per-migrant labor-service intensity. |
| exact correction if it fails | `W^L_ij = W^persons_ij (ρ_ij φ_ij) / Σ_l W^persons_il (ρ_il φ_il)` |
| **key unification** | the correction needs a **destination-varying labor-intensity weight `ρφ`** — which is *the same object* required to put `ell_i` on an efficiency-labor basis. There is therefore **one** missing external input, not two: without it, neither the population→labor bridge nor the `ell` basis can be supplied, and the pair target stays blocked even if a clean bilateral matrix exists. |
| failure direction is not innocuous | if `φ` rises with destination attractiveness, the person-based share **systematically understates** high-wage destinations' labor-service share, i.e. the bias is correlated with the model's own explanatory variables and will not average out. |
| mandatory statements | who is excluded; whether a mover-only frame distorts destination shares relative to origin labor; whether weights can recover the intended labor population (they cannot invent labor-force status not collected); whether efficiency-labor weighting is ignored, approximated or externally supplied — one of the three must be declared. |

## 4. Region / `m` / `ell` provenance contract (summary)

Full contract: `docs/data/DLH_WL_P3B_REGION_MELL_PROVENANCE_CONTRACT_2026_09_19.md`.

- **Region dictionary specification (candidate, no adapter, no crosswalk):** canonical universe
  = 31 provincial-level units under mainland administration, composed of 4 municipalities + 22
  provinces + 5 autonomous regions; provincial level only; code system = the national
  administrative-division code standard, **unit set not in dispute, every code value
  `NOT_VERIFIED_EXTERNAL`** and requiring version pinning.
- **HK / Macao / Taiwan:** outside the canonical universe; a source reporting them maps to an
  explicit `EXCLUDED_NON_MAINLAND` category that is never folded into a mainland unit and never
  used in the conditional denominator.
- **Municipalities:** single units, no district decomposition, identical treatment across all
  waves; a municipality-specific rule would be a dictionary design change requiring a dated
  amendment.
- **Historical changes:** Hainan (1988) and Chongqing (1997) both pre-date every reference
  *moment*, so no merging is required for the waves as such. **Live issue:** the 2000 wave's
  five-year window is `[1995-11, 2000-11]`, and 1995 **precedes Chongqing's separation**, so the
  early-window origin geography is administratively Sichuan. The tabulation convention is
  `NOT_VERIFIED_EXTERNAL`; the preregistered handling is exactly one of `MERGED_VARIANT`
  (30-unit wave), `WAVE_EXCLUDED`, or `AS_REPORTED` with the unresolved-coding risk carried into
  sensitivity — and if `AS_REPORTED` is chosen, the merged variant must still be evaluated.
- **Common-universe rule:** per-wave mappable set → intersection across waves; merges are built
  by **summing**, never by splitting or imputing; the intersection, excluded units and excluded
  mass are reported; the support mask is **not** derived from the dictionary.
- **Fail-closed:** an unmappable label drops the whole `(origin, time)` block with a recorded
  reason; ambiguous or duplicated mappings, unlisted units, an unnamed coding version, an
  exceeded unmappable-mass threshold, or an unreconcilable excluded mass all fail closed. Every
  fail-closed event is reported, counted and attributed.
- **`m`:** `m_i = 1 − P_ii` is a candidate-derived given input **only** from an authorized annual
  `P`; not available from stock shares; not available from repeated cross-sections; derivation
  from unrelated totals is forbidden. Because the time bridge does not identify `P`, `m` must be
  reported jointly with the enumeration of `𝓕` and the selection rule and must **not** be
  presented as data-identified.
- **`ell`:** `ell_unit ∈ {EFFICIENCY_LABOR, EMPLOYED_PERSONS_DECLARED_AS_PROXY,
  LABOR_FORCE_DECLARED_AS_PROXY}`; population counts may not be silently treated as efficiency
  labor; nine requirements E1–E9 cover scope, unit, time alignment, timing (must precede or
  coincide with the decision — a post-decision measurement is forbidden), no substitution of
  total population, no derivation from unrelated totals, provenance, dimensional consistency
  with `m`, and coverage.
- **Weights / harmonization / leakage:** weight identity and re-derivation rules, unweighted and
  weighted variants both reported; questionnaire, sample-design, weight and census/sample
  comparability harmonization records all required, with cross-year pooling **blocked** absent a
  declared record; structural-zero requires a documented reason and undocumented zeros default
  to `MISSING`/`OBSERVED_ZERO`; pair-support stability handled by the intersection rule with
  both-variants reporting; the **canonical design is window-start** (features at `t−k`, label
  over `(t−k, t]`), with the window-end nowcast admissible only as a separately labelled variant;
  publication/revision timing recorded separately from the reference period; leakage rules L1–L5
  including the honest destination-role-exposure record; split claims limited to
  `HELD_OUT_TIME` / `HELD_OUT_ORIGIN_ROLE`, with `UNSEEN_REGION` unavailable.

## 5. Sensitivity matrix (summary)

Full 19-axis matrix: companion document §4. Axes, all frozen before execution:

```
A1  time-bridge family            A2  admissible-root spread        A3  low-mobility applicability (C1)
A4  window length k               A5  duration heterogeneity (dest) A6  duration heterogeneity (origin)
A7  duration-flow correlation     A8  duration definition           A9  origin-type (hukou vs residence)
A10 population->labor mapping     A11 labor-intensity gradient      A12 efficiency-labor weighting
A13 region mapping                A14 survey-weight harmonization   A15 support-mask treatment
A16 missing-cell handling         A17 prediction-time information set
A18 publication/revision timing   A19 split claim
```

**Outcome-driven selection is prohibited:** no axis level, tolerance, selection rule or bridge
family may be changed, added or dropped after any outcome is inspected.

## 6. Decision rationale

| Terminal | Selected? | Reason |
|---|---|---|
| `DLH_WL_P3B_BRIDGE_PREREGISTRATION__PASS__CANDIDATE_AVAILABLE` | **YES** | the T-family bridges T1 and T2 are mathematically explicit: T1 admits a fully specified admissible solution set with proved existence and uniqueness failure modes plus a deterministic preregistered selection rule, and T2 has a proved second-order error term with an explicit applicability condition `C1`. Issue #81 §10 requires exactly "a mathematically explicit bridge candidate with named assumptions, failure conditions and sensitivity axes", which is met. |
| `DLH_WL_P3B_BRIDGE_PREREGISTRATION__PASS__NO_DEFENSIBLE_BRIDGE_YET` | no | not selected, for the reason above. Note that the *execution* prerequisites for every family remain unsatisfied (region dictionary not instantiated, `m` not identified, `ell` provenance absent, labor-intensity gradient absent, C-family schema unverified), so this is a statement about preregisterability, not about availability. |
| `DLH_WL_P3B_BRIDGE_PREREGISTRATION__REVIEW_REQUIRED` | no | no internal contradiction was found. P3A's Branch-B qualification — that Branch B means a bridge could be *specified*, not that one exists — is exactly what this document formalizes. The P3A-flagged closeness of the B/P boundary is unaffected, and the identification results here make the "no empirical `W^L` fit now" conclusion strictly **stronger**, not weaker. |

## 7. Prohibited-action accounting (all zero)

| Item | Count |
|---|---|
| scientific / model / training calls | **0** |
| fits, estimates, optimizations, calibrations | **0** |
| empirical adapters written | **0** |
| real label sets constructed | **0** |
| datasets downloaded, scraped, purchased, ingested or opened | **0** |
| external metadata queries required | **0** |
| `pytest` / full-suite runs | **0** |
| HJB / KFE / GE / MATLAB / household calls | **0** |
| numeric `m`, `ell`, `W` numerator or denominator values produced | **0** |
| region crosswalk values or source label mappings produced | **0** |
| stock→flow equality silently assumed | **0** |
| stochastic-root existence or uniqueness assumed | **0** |
| multi-year proxy relabelled annual | **0** |
| population share relabelled labor-service share | **0** |
| total population substituted for `ell` | **0** |
| numeric tolerances or thresholds chosen | **0** (`tau_W`, `pi_max`, search parameters and the unmappable-mass threshold are all left for Reviewer authority before execution) |
| outcome-driven selections | **0** |
| successor Issues / P3C artifacts created | **0** |
| source code / tests / config / CURRENT governance / P2 artifacts touched | **0** |
| PRs, merges, closes, self-acceptances | **0** |

The illustrative matrices used in the preregistration (`[[0,1],[1,0]]`,
`[[5/8,3/8],[3/8,5/8]]`, `circ(1/2,3/10,1/5)`) are **mathematical objects constructed for
demonstration**, labelled as such in place, and are not data.

### 7.1 Static mathematical verification performed (disclosed for completeness)

The only computation performed by this Issue was **exact/symbolic and floating-point
verification of the algebra in §3.1**, on the constructed matrices above, with **zero data**:
no dataset was opened, nothing was fitted, estimated, optimized or sampled, and no empirical
bridge was executed. 25 of 25 checks passed. The verified numbers reported in this document
are:

```
root A and root B both square exactly to T^(2) = [[5/8,3/8],[3/8,5/8]]   (exact rational arithmetic)
implied m:  m_A = 3/4  vs  m_B = 1/4                    (factor 3)
naive divide-by-k rule: 3/16                            (neither root)
det(T^(2)) = 1/4 ;   det([[0,1],[1,0]]) = -1            (embedding necessary condition)
grid search over the admissible 2-region roots of [[0,1],[1,0]]: none found
exp(Q) = [[3/4,1/4],[1/4,3/4]] = root B, and exp(2Q) = T^(2)
W  = (0.600, 0.400) ;  P^2 = circ(0.37, 0.34, 0.29) ;  W^(2)_12 = 34/63 = 0.53968254
two-year proxy bias = 10.053 % ;  W^(5)_12 = 0.5011174 ;  five-year bias = 16.480 %
W^(50)_12 = 0.5000000                                  (ergodic limit reached)
low-mobility operator: 200 random small-hazard matrices, always non-negative and row-stochastic;
  max ||P_hat - P|| / ||A||^2 = 3.75    (confirms second-order error)
first-order bias formula vs truth in the small-mobility regime:
  predicted -0.00480000  vs  actual -0.00481384        (0.3 % agreement)
```

The last line is the substantive one: the three-channel first-order decomposition is not merely
asserted, it reproduces the exact bias to within 0.3 % where its small-mobility premise holds.

## 8. Exact changed paths (4 — exactly the Issue #81 allowlist)

```
docs/specifications/DLH_WL_P3B_BRIDGE_PREREGISTRATION_2026_09_19.md
docs/data/DLH_WL_P3B_SOURCE_BRIDGE_SENSITIVITY_MATRIX_2026_09_19.md
docs/data/DLH_WL_P3B_REGION_MELL_PROVENANCE_CONTRACT_2026_09_19.md
reports/dlh_wl_p3b_2026_09_19/DLH_WL_P3B_REPORT.md
```

Nothing else was created or modified: no source code, no tests, no config, no CURRENT
governance document, no P2/P2D artifact, no P3A artifact.

## 9. Interpretation ceiling

Allowed by this Issue:

- the bridge preregistration itself: equations, assumptions, failure conditions and the
  selection rule;
- the mathematical propositions and counterexamples, which are presented as mathematics and
  labelled as such;
- statements about which prerequisites remain unsatisfied and why;
- the region / `m` / `ell` / weights / leakage contract as **requirements**.

Explicitly **not** claimed by this Issue:

- any empirical China estimate, and no empirical `W^L` fitting of any kind;
- any claim that a bridge has been executed, or that a real label set exists;
- any claim that any source's pair fields, schema, licence or access have been verified;
- any claim that a stochastic root exists, is unique, or that an embedding exists, for any real
  matrix;
- any claim that a multi-year proxy approximates an annual share;
- any claim that a stock share equals a flow share;
- any claim that a population share equals a labor-service share;
- any annual bilateral OD data **availability** claim — the P3A non-availability record stands;
- any unseen-region, causal, welfare, policy, GE, HJB/KFE or household claim;
- any model-performance statement: no model was run.

## 10. Terminal

```
DLH_WL_P3B_BRIDGE_PREREGISTRATION__PASS__CANDIDATE_AVAILABLE
```

**This does not authorize empirical fitting.** No successor Issue, no adapter and no label set
is created by this report. A later, **separately authorized** Issue could verify the source
schema at E3, instantiate the region dictionary, establish `m`/`ell` provenance, freeze `tau_W`,
`pi_max` and the search parameters, and implement the preregistered bridge — with the selection
rule, the enumeration of `𝓕` and the sensitivity design of these documents applied unchanged.
Until every one of those preconditions holds, the pair target remains `UNRESOLVED` and empirical
`W^L` work remains forbidden.
