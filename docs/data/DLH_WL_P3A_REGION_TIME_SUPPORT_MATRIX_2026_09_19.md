# DLH-WL-P3A — canonical source × region / time / support matrix

Issue: **#80 / `DLH-WL-P3A`**. Owner route: `DLH-WL-V1-20260918`.
Authority marker: `DLH_WL_P3A_REAL_DATA_LABEL_PROVENANCE_GATE_AUTHORIZED`.
Reviewer final activation comment: **`5741079748`**.
Operative baseline: `e688a78907b69627800af65970f82d2fd94afae4`.
Status: evidence / schema validation only. **No fabricated `m`, `ell`, `W` numerator or
`W` denominator exists anywhere in this matrix, and no real-data fit is authorized.**

Companion documents:

- `docs/data/DLH_WL_P3A_REAL_DATA_SOURCE_EVIDENCE_2026_09_19.md` (per-source audit);
- `docs/specifications/DLH_WL_P3A_EMPIRICAL_LABEL_GATE_2026_09_19.md` (branch gate);
- `reports/dlh_wl_p3a_2026_09_19/DLH_WL_P3A_REPORT.md` (Issue report).

---

## 1. Cell vocabulary (closed set)

| Token | Meaning |
|---|---|
| `YES_TRANSITION` | present, as a multi-year residence transition (origin and destination both observed for the same transition) |
| `YES_STOCK` | present, as a stock / sample snapshot |
| `YES_AGGREGATE` | present only at origin-level or destination-level aggregate granularity |
| `NOT_ESTABLISHED` | the repository's E1 record explicitly says the dimension is unproven or absent |
| `NOT_VERIFIED_EXTERNAL` | the dimension could not be independently verified from this environment |
| `DOC_ONLY` | documentation of semantics, not a measured dimension |
| `ABSENT_BY_DESIGN` | structurally excluded by the source's own sampling/design frame |
| `N_A_NOT_A_DATA_OBJECT` | the candidate is not a data object |
| `NOT_PRODUCED_BY_P3A` | reserved marker: this Issue emits no such quantity for any source |

## 2. Source × dimension support matrix

Reference periods use the P1B `time_semantics` vocabulary
(`CALENDAR_YEAR`, `TRANSITION_WINDOW_K_YEARS`, `SNAPSHOT_YEAR`, `SYNTHETIC_STEP`).

| Dimension | S1 Census long-form | S2 1% sample survey | S3 CMDS | S4 geodoi Id=3621 | S5 *J. Maps* 2016 OD | S6 methods / standard |
|---|---|---|---|---|---|---|
| **origin observed?** | `YES_TRANSITION` (province of residence 5 years earlier) | `YES_TRANSITION` | `YES_STOCK` (hukou province) | `YES_AGGREGATE` (province outflow rate / component) | `YES_STOCK` | `DOC_ONLY` |
| **destination observed?** | `YES_TRANSITION` (province at reference moment) | `YES_TRANSITION` | `YES_STOCK` (current province) | `YES_AGGREGATE` (province inflow rate / component) | `YES_STOCK` | `DOC_ONLY` |
| **bilateral pair observed?** | `YES_TRANSITION` | `YES_TRANSITION` | `NOT_VERIFIED_EXTERNAL` (constructible only if the microdata carry both fields) | `NOT_ESTABLISHED` (no proven `(i,j,t)` field) | `YES_STOCK` | `N_A_NOT_A_DATA_OBJECT` |
| **time id / window** | `TRANSITION_WINDOW_K_YEARS`, `k = 5`; moments 2000, 2010, 2020 | `TRANSITION_WINDOW_K_YEARS`, `k = 5`; moments 2005, 2015 | `SNAPSHOT_YEAR`, annual 2009–2018 | window 2010–2020 (derived series) | `SNAPSHOT_YEAR`, single matrix 2010 | `DOC_ONLY` |
| **same-period move?** | no — a 5-year residence transition window is not a same-period move | no | no — a snapshot of who is currently there, not of who moved in the period | no — derived components, not moves | no — stock at the census moment | `DOC_ONLY` |
| **local stayer present?** | yes (same-province cell family) — but not the conditional `W^L` object; `support_mask_ii = false` always | yes (as S1) | `ABSENT_BY_DESIGN` (migrant-only frame) | `NOT_ESTABLISHED` at pair level | `ABSENT_BY_DESIGN` (floating population only) | `DOC_ONLY` |
| **province coverage** | all provincial-level units of the census year (31 mainland provincial-level units as documented); concrete join blocked on the region dictionary (§3) | as S1 | national cross-section, migrant-only; per-province cell counts `NOT_VERIFIED_EXTERNAL` | 31 provinces as documented | 31 provinces as documented | `DOC_ONLY` |
| **sample / design weight** | census long-form weights exist; cross-round harmonization `NOT_VERIFIED_EXTERNAL` | 1% sample design weights; cross-round harmonization `NOT_VERIFIED_EXTERNAL` | survey weights exist; cross-year weight harmonization, sample-design and questionnaire harmonization `NOT_VERIFIED_EXTERNAL` (P1B §5 item 4) | not a survey — no sample weights; estimator identity/vintage `NOT_VERIFIED_EXTERNAL` | census-derived; derivation weights `NOT_VERIFIED_EXTERNAL` | `DOC_ONLY` |
| **direct `m_i` candidate?** | `NOT_PRODUCED_BY_P3A` — no real `m` provenance exists in the repository (P1B §5 item 3) | `NOT_PRODUCED_BY_P3A` | `NOT_PRODUCED_BY_P3A` | `NOT_PRODUCED_BY_P3A` | `NOT_PRODUCED_BY_P3A` | `N_A_NOT_A_DATA_OBJECT` |
| **direct `ell_i` candidate?** | `NOT_PRODUCED_BY_P3A` — no real efficiency-labor conversion exists in the repository (P1B §5 item 3) | `NOT_PRODUCED_BY_P3A` | `NOT_PRODUCED_BY_P3A` | `NOT_PRODUCED_BY_P3A` | `NOT_PRODUCED_BY_P3A` | `N_A_NOT_A_DATA_OBJECT` |
| **potential `W` numerator?** | `NOT_PRODUCED_BY_P3A` — the transition matrix cells are a *transition* count, not an annual flow count | `NOT_PRODUCED_BY_P3A` | `NOT_PRODUCED_BY_P3A` — stock cells, not flow counts | `NOT_PRODUCED_BY_P3A` — no pair dimension | `NOT_PRODUCED_BY_P3A` | `N_A_NOT_A_DATA_OBJECT` |
| **potential `W` denominator?** | `NOT_PRODUCED_BY_P3A` — the conditional denominator must be an origin-level flow realized in one period | `NOT_PRODUCED_BY_P3A` | `NOT_PRODUCED_BY_P3A` | `NOT_PRODUCED_BY_P3A` | `NOT_PRODUCED_BY_P3A` | `N_A_NOT_A_DATA_OBJECT` |
| **support-mask evidence?** | partial: the source distinguishes "same province" from "other province", which supports a structural statement about the **diagonal** only. It does **not** evidence which foreign pairs are structurally unavailable | as S1 | not established | none | not established (the matrix's zero cells are not documented as structural) | `DOC_ONLY` |
| **feature timing / leakage compatibility** | label complete only at the end of the 5-year window → `calendar_lag_definition` must be declared; `REQUIRES_DECLARATION_AT_ADAPTER_TIME` | as S1, plus smaller sample base → per-pair density must be declared | contemporaneous with the survey year; migrant-only frame conflicts with an all-population conditional share → must be declared | inherits census/employment-statistics revision timing; estimator identity undeclared → `NOT_VERIFIED_EXTERNAL` | single snapshot → cannot support held-out **time**; `HELD_OUT_ORIGIN_ROLE` at best, and only with ≥2 years | `DOC_ONLY` |

### 2.1 P1B flag closure for every source

Per P1B §3.2, `target_available` requires a non-`MISSING` `zero_kind`, a `true`
`support_mask_ij`, `identifiable_conditional_target`, a non-null `target_W_ij_t`, **and**
either direct empiricalness or a dated bridge/assumption record. For every real-data source
in this matrix the third and fourth conditions are unmet and no dated bridge record exists,
so:

| Source | `label_is_direct_target` | `target_available` | `target_W_ij_t` | `share_numerator` / `share_denominator` | `zero_kind` at source level |
|---|---|---|---|---|---|
| S1 | `false` | `false` | `null` | `null` (`null` is required because no share is derived) | `NOT_APPLICABLE` at source level; per-`(i,j,t)` `zero_kind` is an adapter-time decision |
| S2 | `false` | `false` | `null` | `null` | as S1 |
| S3 | `false` | `false` | `null` | `null` | as S1 |
| S4 | `false` | `false` | `null` | `null` | as S1 |
| S5 | `false` | `false` | `null` | `null` | as S1 |
| S6 | `false` | `false` | `null` | `null` (no share at all) | `NOT_APPLICABLE` |

**No row anywhere in this matrix is marked `target_available = true`.** A source-level
`target_available` of `true` would require a dated bridge/assumption record, which Issue #80
does not authorize and which does not exist.

## 3. Region dimension

- The P1B region dictionary id is `DLH_WL_REGION_DICT_V1_2026_09_18`. P1B §5 declares it a
  **declaration placeholder**: "the concrete regional dictionary is a later deliverable and
  is not created here".
- Consequence for P3A: **no concrete region ids can be written into a canonical row yet.**
  Every coverage statement in this matrix is therefore at the granularity the sources
  themselves document ("31 mainland provincial-level units"; "all provincial-level units of
  the reference year") and is marked
  `BLOCKED_ON_REGION_DICTIONARY_NOT_CREATED` for any join purpose.
- Unresolved regional issues that the concrete dictionary must settle before any adapter can
  be written: provincial-level unit set and code version; treatment of the special
  administrative regions and of any province-level unit with a distinct statistical regime;
  the mapping from the sources' residence/hukou geography onto the dictionary; and whether
  the dictionary carries the destination-role exposure metadata that P1B §3.6 requires.
- No region id, no region code and no region count is asserted here beyond what the
  repository already documents.

## 4. Time dimension

| Source | Documented reference periods | P1B `time_semantics` | Consecutive-annual series? | Usable for `HELD_OUT_TIME`? |
|---|---|---|---|---|
| S1 | 2000, 2010, 2020 | `TRANSITION_WINDOW_K_YEARS` (`k = 5`) | no — decennial moments | no: only three non-adjacent windows, and each is a multi-year object |
| S2 | 2005, 2015 | `TRANSITION_WINDOW_K_YEARS` (`k = 5`) | no — two moments | no |
| S3 | 2009–2018 | `SNAPSHOT_YEAR` | yes, annual snapshots | not for annual **flow** labels; only for stock-share objects |
| S4 | 2010–2020 | derived series | yes, annual derived | not for pair labels — no pair dimension |
| S5 | 2010 (single matrix) | `SNAPSHOT_YEAR` | no | no |
| S6 | n/a | `DOC_ONLY` | no | n/a |

P1B forbids mixing `CALENDAR_YEAR` with transition or synthetic time inside one evaluation
set. Since **no** real-data source in this audit carries `CALENDAR_YEAR` semantics with
same-period moves, no real-data evaluation set can currently be assembled under that rule.

## 5. Support-mask dimension

`support_mask_ij` is the structural-availability statement P1B §3.4 requires, and the
conditional `W^L` object fixes `support_mask_ii = false` **always**, with home retention
carried only by `P_ii = 1 - m_i`.

| Question | Finding |
|---|---|
| does any source document a foreign-pair structural exclusion? | **no** — no source in this audit documents which foreign province pairs are structurally unavailable |
| does any source evidence the diagonal? | partially — a source that separates "same province" from "other province" supports the diagonal statement, but the diagonal is **fixed by the schema** rather than discovered from data |
| is a real `STRUCTURAL_ZERO` set available? | no. P1B requires `structural_zero_reason` for any `STRUCTURAL_ZERO`; no source provides such a reason |
| is a real `support_mask` available? | no. Consequently any real-data row would have to declare `zero_kind` per cell from the source's own observed zero/non-observation distinction — which under P1B makes it `OBSERVED_ZERO` or `MISSING`, **not** `STRUCTURAL_ZERO` |
| are the sources' zero cells structural? | `NOT_VERIFIED_EXTERNAL` for every source. Treating an undocumented zero as structural would be a design invention and is forbidden |

## 6. Weights dimension

| Source | Weights present? | Harmonization status | Effect on eligibility |
|---|---|---|---|
| S1 | long-form census weights | `NOT_VERIFIED_EXTERNAL` across rounds | a cross-round pooled design would need a declared harmonization record |
| S2 | 1% sample design weights | `NOT_VERIFIED_EXTERNAL` across rounds | as S1 |
| S3 | survey weights | `NOT_VERIFIED_EXTERNAL` across years **and** across sample-design / questionnaire changes (P1B §5 item 4) | a cross-year CMDS panel would need a declared harmonization record; this is a named P1B open item |
| S4 | no (not a survey) | n/a | not a weighted object |
| S5 | census-derived | derivation `NOT_VERIFIED_EXTERNAL` | single-year, so cross-year harmonization does not arise |
| S6 | n/a | n/a | not a data object |

P1B §3.6 requires `sample_weight` and `sample_weight_source` for survey-derived rows, with the
harmonization status declared. No source in this audit currently supports a **verified**
harmonization declaration.

## 7. Feature timing and leakage compatibility

P1B §3.5 requires, per feature group, an availability list, a transformation list, a
`feature_available_at_prediction_time` flag and `leakage_flags`, and forbids features that
encode the label, the same-period realized flow, future information or any test target.
`m` and `ell` are never features.

The DLH-1A feature feasibility map (unchanged) is the only repository evidence on feature
availability, and it is class-level, not province-level:

| Feature group | Class verdict (DLH-1A) | P3A consequence |
|---|---|---|
| `Z_static_ij` (distance / adjacency / terrain) | `AVAILABLE` (public GIS) | usable in principle; the concrete source and vintage still need declaration |
| `Z_node_i,t` (GDP pc, wage, population, urbanization, capital stock, fiscal) | `LIKELY_AVAILABLE_NEEDS_VERIFICATION` | not yet declareable |
| returns, industrial structure / upgrading | `DIFFICULT` | not yet declareable |
| `Z_pair_ij,t` (wage/GDP/return gaps) | `LIKELY_AVAILABLE_NEEDS_VERIFICATION` | not yet declareable |
| accessibility change | `DIFFICULT` | not yet declareable |
| bilateral migration history | `LIKELY_AVAILABLE_NEEDS_VERIFICATION` | depends on the §2 label blockers |
| policy links / institutional state | `UNRESOLVED` | not available |

Additional P3A-specific timing findings:

- **label-end availability.** Every transition-type candidate (S1, S2) yields a label that is
  only complete at the **end** of its window, so `calendar_lag_definition` is mandatory and
  must be kept separate from `outer_iteration_lag_definition` (P1B §3.3);
- **migrant-frame mismatch.** S3 and S5 cover only movers, while the conditional object
  `W^L` is defined on an origin's labor total with `m_i` given. Using a mover-only frame
  requires an explicit declaration of how the population basis maps onto `ell_i` — which is
  currently impossible because no real `ell` provenance exists (P1B §5 item 3);
- **destination-role exposure.** P1B §3.6 requires `test_regions_appear_as_train_destinations`
  to be recorded honestly. For a real province panel this will be `true` whenever an
  origin-role holdout shares provinces with the destination axis, so no unseen-region claim
  will ever be available from such a split; that is a property of the design, not of P3A.

## 8. Branch-availability decision table

| Branch | Required condition | Satisfied? | Evidence |
|---|---|---|---|
| **D** — direct target available | at least one source verified `TRUE_ANNUAL_OD_FLOW` with same-period bilateral origin/destination support sufficient to construct `W` without a bridge | **NO** | no source is `TRUE_ANNUAL_OD_FLOW`; S1/S2 are 5-year transitions; S3/S5 are snapshots; S4 has no pair dimension |
| **B** — bridged pair object only | no direct annual flow source verified, **but** at least one bilateral stock/sample/transition object is sufficiently documented to support a separately authorized explicit bridge/sensitivity design | **YES** | S1 and S2 are documented bilateral interprovincial transition matrices with declared reference windows and coverage; S3 and S5 are documented bilateral stock/sample objects. Any of these can support a *later, separately authorized* bridge/sensitivity design. See §9 for the qualification |
| **P** — pair target not supportable | only provincial aggregate/proxy objects verified, **or** pair-level source semantics/access insufficient | **NO** as stated | pair-level objects **are** verified to exist at E1 (S1, S2, S5; S3 conditionally), so the first clause fails. The second clause ("pair-level semantics/access insufficient") is **partially** true for the *specific* questions the E3 queue reserves — see §9 |

## 9. Branch decision, with the qualification stated explicitly

**Selected branch: `B`.**

Reasoning, and the boundary of the claim:

1. **Branch D is excluded.** No source is a verified `TRUE_ANNUAL_OD_FLOW` object. S1/S2 are
   five-year residence transitions; S3/S5 are snapshots of who is present, not of who moved
   in the period; S4 has no established pair dimension. The DLH-1A-R1 conclusion that a
   direct credible `(i,j,t)` destination-share label set is `UNRESOLVED` stands unchanged.
2. **Branch B is available.** At least one, and in fact several, bilateral stock / sample /
   transition objects are documented well enough to specify a bridge: the origin and
   destination axes, the reference window, the population basis and the coverage are all
   recorded, and the P1B taxonomy already names the required bridge classes
   (`STOCK_TO_FLOW`, and a pre-registered `k`-year→annual timing model). Being able to
   *specify* such a bridge is exactly what Branch B means.
3. **The Branch-B qualification is load-bearing and must not be read as availability.** Branch
   B does **not** say a bridged label set exists, and it does **not** authorize constructing
   one. Specifically:
   - the bridge itself is a scientific decision that "needs its own dated authority"
     (P1B §5 item 5); no such record exists;
   - `ANNUAL_OD_STOCK_OR_SAMPLE_CROSSTAB` and `MULTIYEAR_TRANSITION_OR_DERIVED_PROXY` rows
     must never be relabelled or rescaled into `TRUE_ANNUAL_OD_FLOW` (P1B §2.2 item 1), and
     normalization never repairs the semantic mismatch (P1B §2.2 item 2);
   - the concrete region dictionary does not exist (§3), so no canonical row can yet be
     instantiated;
   - no real `m` and no real `ell` provenance exists (§2), so even a bridged `W` would have
     no admissible conditional denominator;
   - the DLH-1A E3 queue still holds three unresolved data-side questions (S4 pair-level
     fields; S3 codebook and harmonization; S1/S2 tabulation and transition semantics), so
     the *access and schema* half of the Branch-B object documentation is `NOT_VERIFIED_EXTERNAL`.
4. **Branch P is not selected**, because Branch P's first clause requires that only provincial
   aggregate/proxy objects be verified, and that is factually not the case. Its second clause
   would be reached only if pair-level semantics **and** access were insufficient *for every*
   candidate; here the pair-level objects are documented at E1 even though the specific
   schema/access questions remain open. Because the P/B boundary is close, this is recorded
   as the single point a Reviewer may most reasonably wish to re-adjudicate — the substantive
   scientific consequence (no empirical `W` fit is authorized now) is identical under B and P.

## 10. What this matrix does not contain

- no numeric `m`, no numeric `ell`, no `W` numerator, no `W` denominator, no share value, for
  any source;
- no concrete region id, region code, region count beyond the sources' own documented
  coverage statements, and no region dictionary;
- no annual flow value, no annualization factor, no transition→annual conversion;
- no bilateral estimate derived from marginals;
- no label, no target, no training input, no evaluation set.

Every quantity in this matrix is either a classification token from the closed vocabularies
in §1 and P1B §2, or a documented coverage/reference-period statement carried over from the
accepted E1 repository record.
