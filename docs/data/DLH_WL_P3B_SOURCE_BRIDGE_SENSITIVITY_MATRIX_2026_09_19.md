# DLH-WL-P3B — source × bridge × sensitivity matrix

Issue: **#81 / `DLH-WL-P3B`**. Owner route: `DLH-WL-V1-20260918`.
Authority marker: `DLH_WL_P3B_BRIDGE_SOURCE_PREREGISTRATION_AUTHORIZED`.
Reviewer final activation comment: **`5741234971`**.
Operative baseline: `1f4bee7290da7143fab9612157bd99f83e3216b4`.
Status: preregistration only. No dataset was downloaded, scraped, purchased, ingested or
opened. **No numeric empirical bridge was executed. Scientific / model / training calls = 0.**

Companion documents:

- `docs/specifications/DLH_WL_P3B_BRIDGE_PREREGISTRATION_2026_09_19.md` (the bridges);
- `docs/data/DLH_WL_P3B_REGION_MELL_PROVENANCE_CONTRACT_2026_09_19.md` (region, `m`, `ell`,
  weights, leakage);
- `reports/dlh_wl_p3b_2026_09_19/DLH_WL_P3B_REPORT.md` (report and terminal).

---

## 1. Cell vocabulary (closed set)

Inherited from the accepted P3A support matrix where applicable, plus bridge-specific tokens.

| Token | Meaning |
|---|---|
| `REQUIRED` | the bridge cannot proceed without this element |
| `REQUIRED_EXTERNAL` | required, and must come from a source outside the label object |
| `NOT_IDENTIFIED` | the element is not identified from the documented object (proved or demonstrated in the preregistration) |
| `NOT_VERIFIED_EXTERNAL` | the element could not be independently verified from this environment |
| `NOT_PRODUCED_BY_P3B` | reserved marker: P3B emits no such numeric quantity |
| `N_A` | not applicable to this family |
| `EXCLUDED_FROM_DESIGN` | the family is outside pair-label bridge design by Issue #81 §2 |
| `CONDITIONAL_DESIGN` | a bridge candidate exists, but execution is gated on stated prerequisites |
| `PROXY_ONLY` | usable only as a clearly-labelled proxy, never as the target |

## 2. Source family × bridge coverage

| | T — census / 1 % sample multi-year transition | S — single-year floating-population stock OD | C — CMDS repeated migrant cross-section | geodoi aggregate components |
|---|---|---|---|---|
| **P3A P1B class** | `MULTIYEAR_TRANSITION_OR_DERIVED_PROXY` | `ANNUAL_OD_STOCK_OR_SAMPLE_CROSSTAB` | `ANNUAL_OD_STOCK_OR_SAMPLE_CROSSTAB` | `PROVINCIAL_AGGREGATE_PROXY` |
| **bilateral pair dimension** | yes (transition) | yes (stock) | `NOT_VERIFIED_EXTERNAL` (constructible only if schema permits) | none established |
| **time bridge (§2 of preregistration)** | **applicable** — T1, T2, T3 | not applicable (single snapshot; no `k`) | not applicable (single-year snapshot) | not applicable |
| **stock→flow bridge (§3)** | not applicable (transition, not stock) | **applicable** — `NOT_IDENTIFIED` as documented | **applicable** — `NOT_IDENTIFIED` as documented | `EXCLUDED_FROM_DESIGN` |
| **population→labor bridge (§4)** | **applicable** | **applicable** | **applicable** | `EXCLUDED_FROM_DESIGN` |
| **bridge candidate status** | **`CANDIDATE`** (T1/T2); T3 `PROXY_ONLY` | **`CONDITIONAL_DESIGN`** | **`CONDITIONAL_DESIGN`** | `EXCLUDED_FROM_DESIGN` |
| **may supply `W^L` now?** | no | no | no | no |

No family may supply `W^L` at this Issue. The status tokens describe whether a bridge design
is *preregisterable*, not whether a target exists.

## 3. Per-family bridge matrix

### 3.1 T — census / 1 % sample multi-year transition

| Dimension | Finding |
|---|---|
| observed object | bilateral current residence × residence five years earlier, row-stochastic, diagonal = non-movers |
| `k` | 5 (all documented waves) |
| reference waves | 2000, 2005, 2010, 2015, 2020 |
| time bridge T1 | `𝓕(T^(k))` = admissible stochastic 5th roots; existence checkable per window via the preregistered search; multiplicity must be enumerated |
| T1 existence | **not guaranteed** — proved by the 2-region exchange counterexample (no real non-negative stochastic root); determinantal necessary condition for the embedding route |
| T1 uniqueness | **not guaranteed** — proved by the 2-region `T^(2) = [[5/8,3/8],[3/8,5/8]]` example with two admissible roots implying `m = 3/4` vs `m = 1/4` |
| T1 embedding route | available only when `det(T^(k)) > 0`; may select one root but does not generally eliminate multiplicity |
| T2 low mobility | `P̂ = I + (T^(k) − I)/k`; error `O(k‖A‖²)`; validity conditional on `C1: max_i(1 − T^(k)_ii) ≤ pi_max` |
| T3 proxy | `W^(k)_ij = T^(k)_ij / Σ_{l≠i}T^(k)_il`; exact but structurally biased (demonstrated: 10.05 % at `k = 2`, ≈16.5 % at `k = 5` on the exact `circ(1/2, 3/10, 1/5)` example), grows with `k`, ergodic limit `π_j/Σ_{l≠i}π_l`; **`PROXY_ONLY`** |
| implied `m_i` | `m_i = 1 − P_ii` **only** from an authorized annual `P`; `NOT_IDENTIFIED` until the time bridge is selected and the spread over `𝓕` is within tolerance |
| implied `W` | `W_ij = P_ij/h_i` from an authorized annual `P`; **`NOT_IDENTIFIED`** from `T^(k)` alone |
| observation at a second `k` | not documented for any wave → the strongest identification route is `UNAVAILABLE` |
| unit | `ALL_PERSONS` |
| population→labor | requires `(P-L)` or an observable worker subpopulation; blocked by the missing destination-varying labor-intensity source (§4 of the preregistration) |
| claim ceiling | an **annual** transition matrix and its conditional shares, conditional on the preregistered selection rule and reported spread; **never** a direct `TRUE_ANNUAL_OD_FLOW` label |
| `label_is_direct_target` | `false` |
| `target_available` | `false` (no dated bridge/assumption record exists) |

### 3.2 S — single-year floating-population stock OD

| Dimension | Finding |
|---|---|
| observed object | bilateral stock / sample matrix at one reference moment (2010 census floating population) |
| time bridge | `N_A` — a single snapshot carries no window and no `k` |
| accounting statement | `S_ij = F_ij · D_ij` (Little's law, per cell) |
| equality condition | row-normalized stock shares equal flow shares **iff** `D_ij` is constant across the origin's destinations (proved in §3.1 of the preregistration) |
| identification from the snapshot alone | `NOT_IDENTIFIED`: `D_ij` is not observable from one snapshot |
| identification from repeated cross-sections | `NOT_IDENTIFIED`: `S_ij(t+1) = S_ij(t) − Out_ij(t) + In_ij(t)` is one equation with two unknowns per cell, so only the net is identified |
| panel / duration requirement | `REQUIRED`: an individual panel (d1), a duration or arrival-time question (d2), or an explicitly preregistered constant-duration assumption (d4) with full sensitivity |
| hukou vs previous residence | `S^h ≠ S^r` in general (paths `i → k → j`); the declaration is `REQUIRED` |
| unit | `FLOATING_POPULATION_ALL_PERSONS` |
| population→labor | `(P-L)` `REQUIRED`; also a mover-only frame maps onto origin labor only under a declared rule |
| claim ceiling | stock shares of a snapshot; **must not** be reported as annual flows or as `W^L` (P1B §2.2 items 1–2) |
| `label_is_direct_target` | `false` |
| `target_available` | `false` |

### 3.3 C — CMDS repeated migrant cross-section

| Dimension | Finding |
|---|---|
| observed object | annual repeated migrant cross-section; bilateral only if the microdata carry both current destination and hukou origin province |
| pair constructibility | `NOT_VERIFIED_EXTERNAL` (DLH-1A E3 queue item 2) — **no bridge design may treat pair fields as available until schema verification** |
| time bridge | `N_A` for the annualization sense; the object is already annual but is a snapshot, not a flow |
| stock→flow | same structure as S and equally `NOT_IDENTIFIED`; additionally disqualified from route d3 because the design is a repeated cross-section, not a panel |
| weights | `REQUIRED`: cross-year weight harmonization, sample-design and questionnaire harmonization are all `NOT_VERIFIED_EXTERNAL` (P1B §5 item 4) |
| unit | `MIGRANTS__UNIT_NOT_VERIFIED_EXTERNAL` — whether the issued unit is workers, labor force or all migrants requires the codebook |
| local stayers | `ABSENT_BY_DESIGN` (mover-only frame) |
| population→labor | `(P-L)` `REQUIRED`; a mover-only frame also requires the declared mapping onto origin labor |
| claim ceiling | stock/sample shares of an annual snapshot, once schema is verified; **never** annual flows, **never** `W^L` |
| `label_is_direct_target` | `false` |
| `target_available` | `false` |

### 3.4 geodoi aggregate components

`EXCLUDED_FROM_DESIGN`. No pair dimension is established, so no pair-label bridge can be
preregistered against it. `S4` remains `PROVINCIAL_AGGREGATE_PROXY`; it may never be labelled
bilateral, and marginals alone never identify `W^L` (P1B §2.2 item 4).

## 4. Sensitivity matrix

Every axis below is **frozen before execution**. Values are selected and reported uniformly,
never chosen after seeing an outcome. "Grid" means a preregistered discrete set of levels
evaluated in full.

| # | Axis | Applies to | Levels / grid (preregistered structure) | Tolerance / decision impact |
|---|---|---|---|---|
| A1 | time-bridge family | T | `{T1-embedding, T1-principal-root, T2-low-mobility}` | changing family changes the class and the `m` implied; all three reported |
| A2 | admissible-root spread | T | full enumeration of `𝓕_enum` per window | if the induced `W` spread exceeds the preregistered `tau_W`, the window is declared `NOT_IDENTIFIED` and its target withheld |
| A3 | low-mobility applicability | T | `C1: max_i(1 − T^(k)_ii) ≤ pi_max`, evaluated per window | `C1` violated ⇒ T2 not usable for that window |
| A4 | window length `k` | T | the documented `k = 5`; any auxiliary `k` only if a source documents it (currently none) | the T3 bias is increasing in `k`; reported, never used to pick `k` |
| A5 | duration heterogeneity across destinations | S, C | `max_j D_ij / min_j D_ij` over a grid including the value `1` | the equal-`1` level is the idealization; deviation measures the stock-share distortion |
| A6 | duration heterogeneity across origins | S, C | same structure on the origin axis | as A5 |
| A7 | duration–flow correlation | S, C | `corr(D_ij, F_ij)` over a grid spanning negative → zero → positive | the sign of the correlation fixes the sign of the stock-share distortion |
| A8 | duration definition | S, C | `{time since last move, time in current province, time since hukou separation}` | treated as distinct objects, never mixed inside one evaluation set |
| A9 | origin-type definition | S, C | `{S^h hukou-origin, S^r previous-residence}` | the difference is `O(η²)` and systematically oriented; both reported |
| A10 | population→labor mapping | T, S, C | `{(P-L) share-equivalence, observable worker subpopulation, φ-insensitive approximation}` | the third is admissible only as an explicitly preregistered approximation with `φ` swept |
| A11 | labor-intensity gradient `ρφ` | T, S, C | grid over the destination gradient of `ρ_ij φ_ij` | if the gradient is positive and correlated with attractiveness, the person-based share systematically understates high-wage destinations; reported |
| A12 | efficiency-labor weighting | all | `{externally supplied, ignored with declared approximation, not available ⇒ blocked}` | "not available" blocks the pair target |
| A13 | region mapping | all | `{31-unit common universe, per-wave merged variant where a boundary change requires it, wave excluded}` | any un-mappable label fails the whole block closed (region contract §5) |
| A14 | survey-weight harmonization | S, C, and T where weights apply | `{harmonized with a declared record, not harmonized ⇒ blocked}` | no cross-year pooling without a declared harmonization record |
| A15 | support-mask treatment | all | `{no structural mask beyond the schema diagonal, source-derived observed-zero/missing distinction}` | `STRUCTURAL_ZERO` may never be assigned without a documented reason |
| A16 | missing-cell handling | all | `{drop block, retain as MISSING with `target_available = false`}` | `MISSING` rows can never be supervised (P1B §3.4) |
| A17 | prediction-time information set | all | `{window-start features at t−k, window-end nowcast at t}` | the window-start design is canonical; the window-end variant is a separate, clearly labelled design |
| A18 | publication / revision timing | all | declared per source vintage | no post-exercise publication may enter the feature set unless declared |
| A19 | split claim | all | `{HELD_OUT_TIME, HELD_OUT_ORIGIN_ROLE}` | `UNSEEN_REGION` is unavailable to this design (test origins appear as training destinations) |

**Outcome-driven selection is prohibited.** No axis level, tolerance, selection rule or bridge
family may be changed, added or dropped after any outcome is inspected. The preregistered
artifacts are the three companion documents plus this matrix; any later change requires a dated
amendment with Reviewer authority.

## 5. Bridge prerequisite ledger (what is missing, by bridge)

| Bridge | Prerequisite | Status | Blocking effect |
|---|---|---|---|
| T1 | admissible annualization exists for every used window | `TO_BE_CHECKED_AT_ADAPTER_TIME` | a window with `𝓕 = ∅` fails closed |
| T1 | multiplicity enumerated and the induced `(m, W)` spread within `tau_W` | `TO_BE_FROZEN` (`tau_W`) | spread above `tau_W` ⇒ window `NOT_IDENTIFIED` |
| T1 | preregistered selection rule | **frozen by this document (§2.6)** | — |
| T1/T2 | `m_i = 1 − P_ii` from an authorized annual `P` | `NOT_PRODUCED_BY_P3B` | no `m` value exists |
| T2 | `C1` verified with a frozen `pi_max` | `TO_BE_FROZEN` | `C1` violated ⇒ T2 unusable |
| T3 | — | `PROXY_ONLY` | never usable as the target |
| S/C | pair-level duration or an individual panel | `REQUIRED`, not documented | stock→flow `NOT_IDENTIFIED` |
| S/C | declared `S^h` vs `S^r` object | `REQUIRED` | silent conflation prohibited |
| S/C | declared duration definition | `REQUIRED` | definitions are not interchangeable |
| C | pair-field schema verification | `NOT_VERIFIED_EXTERNAL` (E3 item 2) | no pair bridge until verified |
| C | weight / sample-design / questionnaire harmonization | `NOT_VERIFIED_EXTERNAL` (P1B §5 item 4) | no cross-year pooling |
| S/C/T | destination-varying labor-intensity `ρφ` | `REQUIRED_EXTERNAL`, no source verified | blocks the population→labor bridge **and** the `ell` basis |
| all | 31-unit region dictionary instantiated | `NOT_CREATED` | no canonical row can be instantiated |
| all | `ell_i` efficiency-labor provenance | `REQUIRED_EXTERNAL`, none verified | no admissible conditional denominator |
| all | survey-weight harmonization records | `REQUIRED` where weights apply | blocks pooling |

## 6. What this matrix does not contain

- no numeric `m`, `ell`, `W` numerator or `W` denominator for any family;
- no annualized transition matrix, no root, no generator, no duration value;
- no region crosswalk and no source-specific label mapping;
- no label, target, training input or evaluation set;
- no executed bridge and no empirical result.

Every entry is either a token from the §1 closed vocabulary, a mathematical statement proved or
demonstrated in the companion preregistration, or a carried-over classification from the
accepted P3A/P1B record. The illustrative matrices used in the preregistration
(`[[0,1],[1,0]]`, `[[5/8,3/8],[3/8,5/8]]`, `circ(1/2,3/10,1/5)`) are **mathematical objects
constructed for demonstration**, clearly labelled as such, and are **not** data.
