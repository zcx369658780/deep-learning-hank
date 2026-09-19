# DLH-WL-P3C — human/source verification packet (E3 gate, items H1–H7)

Issue: **#82 / `DLH-WL-P3C`**. Owner route: `DLH-WL-V1-20260918`.
Authority marker: `DLH_WL_P3C_EXECUTION_READINESS_FREEZE_AUTHORIZED`.
Reviewer final activation comment: **`5741497930`**.
Operative baseline: `2b7b0b7d506907ecbf41509bc526ad2b5ea794a6`.

Status: **packet prepared, nothing resolved.** No dataset, microdata, tabulation, codebook,
questionnaire, licence text or full text was opened, downloaded, scraped or purchased. No source
was verified. No evidence level was promoted.

Companion artifacts:

- `docs/specifications/DLH_WL_P3C_EXECUTION_READINESS_FREEZE_2026_09_19.md` (the freeze);
- `configs/dlh_wl_p3c_bridge_readiness.toml` (machine-readable mirror);
- `reports/dlh_wl_p3c_2026_09_19/DLH_WL_P3C_REPORT.md` (report and terminal).

---

## 1. Rules governing this packet

| Rule | Statement |
|---|---|
| P-1 | **No self-promotion.** E3 promotion is a human/Owner act. DSH prepared this packet and resolved nothing. |
| P-2 | **Every item is `UNRESOLVED` at this Issue.** There is no partially-promoted item, and no item is marked "likely" or "probably". |
| P-3 | **No answer may be inferred** from a secondary paper, a dataset title, a mirror page, a reseller listing or a citation in another document. A secondary mention may motivate a question; it can never answer one. |
| P-4 | **A primary official source is required** for H1–H4: the provider's own definition, table/schema description, code standard, or survey documentation. |
| P-5 | **Fail-closed.** While an item that a source needs is unresolved, that source family is **blocked for that wave**. An unresolved item may never be treated as "assume the neutral reading". |
| P-6 | **The packet is not a licence to ingest.** Resolving an item authorises the *decision*, not a download. Any later ingestion needs its own authorization. |
| P-7 | **The packet may block execution without blocking the Issue.** A blocked wave is a legitimate outcome; it is recorded, not worked around. |
| P-8 | **Decision vocabulary is closed.** Each item ends in exactly one of the decision tokens listed for it. |

Common decision tokens:

```
RESOLVED_AS_DOCUMENTED     the primary source confirms the item; the finding is recorded verbatim
RESOLVED_WITH_DECLARED_VARIANT  the source requires a declared variant (merge / exclusion /
                           wave-drop); the variant is named and applied identically everywhere
UNRESOLVED_BLOCKING        no primary evidence; the affected source family is blocked for that wave
NOT_APPLICABLE             the item does not arise for that source (reason recorded)
```

## 2. Item index

| Item | Subject | Blocking scope if unresolved |
|---|---|---|
| H1 | NBS transition semantics | all T-family waves |
| H2 | census / 1% table availability and vintage | the affected wave only |
| H3 | region coding and crosswalks | all waves; every region-joined object |
| H4 | source weights and cross-wave comparability | survey-derived waves (1% sample, and any weighted tabulation) |
| H5 | pair labor-intensity `lambda_ij` | the population→labor-service bridge, for every family |
| H6 | origin labor amount `ell_i` | the conditional denominator, for every family |
| H7 | timing, publication and leakage | the predictive information set for every wave |

Items H5 and H6 are **separate provenance fields** and are handled separately (§4).

---

## 3. H1–H4 — transition object, tables, geography, weights

### H1 — NBS transition semantics

**Question.** Does the primary official documentation confirm, for the migration item used by the
T-family object, each of the following?

| # | Sub-question | Required primary evidence |
|---|---|---|
| H1.1 | the **current-residence** definition used as the destination concept | the official definition text |
| H1.2 | the **residence five years earlier** definition used as the origin concept | the official definition text |
| H1.3 | the **row/column orientation** of the published table (origin rows × destination columns, or the reverse) | the table's own header/notes |
| H1.4 | that the **local-stayer diagonal** is the "same province both dates" cell | the table's own notes |
| H1.5 | the **universe / coverage** (which population is enumerated; which is excluded) | the survey's coverage statement |
| H1.6 | the **weights / tabulation basis** (weighted counts vs sample counts vs percentages) | the tabulation's unit statement |
| H1.7 | the **missing / unknown** categories (undetermined place, "other", non-response) | the tabulation's category list |
| H1.8 | the **exact reference date and window** for each wave | the survey's reference-moment statement |

**Why blocking.** P3B's entire time bridge is a statement about a k-year residence **transition**
matrix with a self-transition diagonal. If the orientation, the diagonal convention or the
reference window is not confirmed from the provider, then `T^(k)` is not even identified as an
object, and every admissibility condition downstream is being applied to something unknown.

**Fail-closed consequence.** `UNRESOLVED_BLOCKING` ⇒ no T-family wave may be used, and the bridge
cannot be implemented at all.

**Decision token.** one of `RESOLVED_AS_DOCUMENTED` / `RESOLVED_WITH_DECLARED_VARIANT` /
`UNRESOLVED_BLOCKING`.

### H2 — census / 1% table availability and vintage

**Question.** For **each** wave, which **exact official table / schema / vintage** provides the
interprovincial transition matrix?

| # | Sub-question | Required primary evidence |
|---|---|---|
| H2.1 | the exact table identifier and title for the wave | the official table listing |
| H2.2 | the publication vintage and any revision history | the publication record |
| H2.3 | whether the published table is machine-readable or tabulation-only | the provider's own format statement |
| H2.4 | whether the table is the same object across waves, or was redefined | the provider's comparability note |

**Explicit prohibition.** **No secondary-paper substitution.** A journal article that reports
numbers *from* the table does not establish the table's identity, availability or semantics.

**Fail-closed consequence.** `UNRESOLVED_BLOCKING` ⇒ the affected wave is excluded from any pooled
or cross-wave design.

**Decision token.** one of `RESOLVED_AS_DOCUMENTED` / `RESOLVED_WITH_DECLARED_VARIANT` /
`UNRESOLVED_BLOCKING`.

### H3 — region coding and crosswalks

**Question.** Which region coding does the source use, and how does it join the pinned canonical
universe?

| # | Sub-question | Required primary evidence |
|---|---|---|
| H3.1 | the **pinned province-code standard and version** | the standard's own edition record |
| H3.2 | the **source's own coding convention** and whether it matches the pinned version | the source's code list |
| H3.3 | the **2000-wave Chongqing / 1995 residence treatment**: how respondents who lived in the Chongqing area in 1995 are coded in the 2000 tabulation | the survey's coding instruction |
| H3.4 | **HK / Macao / Taiwan / other** handling: are they reported separately, merged, or absent | the source's category list |
| H3.5 | **Xinjiang Production and Construction Corps** handling, if present | the source's category list |
| H3.6 | any **merged or absent** unit relative to the 31-unit canonical universe | the source's category list |

**Why H3.3 is load-bearing.** The 2000 wave's five-year window reaches back to 1995, and
Chongqing's status as a separately administered municipality dates from 1997. The geographic
identity of the early-window origin therefore depends on the tabulation's coding convention,
which has not been verified. P3B froze the handling as exactly one of `MERGED_VARIANT` (a
30-unit wave), `WAVE_EXCLUDED`, or `AS_REPORTED` with the coding risk carried into sensitivity —
and required that if `AS_REPORTED` is chosen, the merged variant is **still** evaluated.

**Fail-closed consequence.** `UNRESOLVED_BLOCKING` on H3.1/H3.2 ⇒ no region-joined object at all.
On H3.3 ⇒ the 2000 wave is blocked unless a declared variant is chosen. On H3.4/H3.5 ⇒ any
affected block drops, and the unmappable-mass rule applies: more than
`unmappable_mass_share_max = 0.01` of a block's mass unassigned ⇒ the **whole block fails
closed**, with **no redistribution or imputation**.

**Decision token.** one of `RESOLVED_AS_DOCUMENTED` / `RESOLVED_WITH_DECLARED_VARIANT` /
`UNRESOLVED_BLOCKING`.

### H4 — source weights and cross-wave comparability

**Question.** For every survey-derived wave, what are the weights, and are the waves comparable?

| # | Sub-question | Required primary evidence |
|---|---|---|
| H4.1 | the **weight definition** and the variable identity | the survey's weighting documentation |
| H4.2 | whether tabulated counts are weighted or unweighted | the tabulation's unit statement |
| H4.3 | **cross-wave weight comparability**, and the reconciliation method if not comparable | the provider's comparability note |
| H4.4 | **questionnaire changes** across waves (reference period, wording, category list) | the successive instruments |
| H4.5 | **sample-design changes** (frame, stratification, sampling units) | the successive design documents |

**Fail-closed consequence.** `UNRESOLVED_BLOCKING` on H4.1/H4.2 ⇒ the wave may not be used with
weights, and unweighted use must be declared as a degraded variant. On H4.3–H4.5 ⇒ **cross-wave
pooling is blocked** for the affected waves; each wave may still be analysed separately with the
non-comparability declared.

**Decision token.** one of `RESOLVED_AS_DOCUMENTED` / `RESOLVED_WITH_DECLARED_VARIANT` /
`UNRESOLVED_BLOCKING`.

---

## 4. H5 and H6 — two independent provenance fields

P3B (as remediated under HOLD `5741346648`) established that these are **logically distinct
moments**, not one object. This packet preserves that separation as a hard structural rule.

### H5 — pair labor-intensity `lambda_ij`

**Field.** `lambda_ij`

**Definition.** the **expected labor service per observed mover or person, conditional on
`i → j`**:

```
lambda_ij  =  rho_ij * phi_ij
```

where `rho_ij` is the participation/employment margin and `phi_ij` the efficiency-labor intensity
conditional on being employed.

| # | Sub-question | Required primary evidence |
|---|---|---|
| H5.1 | a source or frame that provides `lambda_ij` at **pair level** (destination-varying within origin), or an explicit decision to use the preregistered share-equivalence approximation instead | the source's variable documentation, or the declared approximation |
| H5.2 | if a source is claimed: whether the two margins `rho` and `phi` are available **separately**, or only as a product | the source's variable list |
| H5.3 | under a two-margin encoding, whether `phi` excludes non-workers (so `rho` is a separate factor); under a single-margin encoding, whether `phi` already includes zero service for non-workers (so `rho` is **redundant and must be dropped**) | the variable definition |
| H5.4 | the frame: which observed population `lambda_ij` is conditional on | the sampling frame statement |
| H5.5 | whether the frame covers the same origin–destination cells as the label object | coverage comparison |

**Explicit prohibitions.** `lambda_ij` may **not** be inferred from `ell_i`; the two encodings may
**not** be mixed inside one evaluation set; a destination-varying `rho` alone breaks share
equality, so `E[phi | i→j]` alone is not sufficient.

**Fail-closed consequence.** `UNRESOLVED_BLOCKING` ⇒ the population→labor-service bridge cannot be
applied, so the pair target stays blocked **even if a clean bilateral transition matrix exists**.

**Decision token.** one of `RESOLVED_AS_DOCUMENTED` / `RESOLVED_WITH_DECLARED_VARIANT` (the
declared approximation is a variant) / `UNRESOLVED_BLOCKING`.

### H6 — origin labor amount `ell_i`

**Field.** `ell_i`

**Definition.** the **total origin labor amount** entering `F_ij = ell_i · m_i · W_ij`, including
the origin population/labor basis and — depending on the accounting — home/stayer labor.

| # | Sub-question | Required primary evidence |
|---|---|---|
| H6.1 | a separate, coherent source for origin total labor, on one declared basis: employed-persons proxy, labor-force proxy, or an efficiency-labor quantity | the source's definition and unit |
| H6.2 | the declared `ell_unit` ∈ {`EFFICIENCY_LABOR`, `EMPLOYED_PERSONS_DECLARED_AS_PROXY`, `LABOR_FORCE_DECLARED_AS_PROXY`} | the declaration, with the proxy status explicit |
| H6.3 | time alignment with the label window, and `accounting_period_alignment` | the source's reference period |
| H6.4 | that the measurement **precedes or coincides with** the destination decision (a post-decision measurement is forbidden leakage) | the source's reference period versus the label window |
| H6.5 | coverage over the same region universe as the label object | coverage comparison |

**Explicit prohibitions.** Total population may **not** be silently substituted for `ell_i`; `ell_i`
may **not** be derived from an unrelated provincial aggregate; `ell_i` may **not** be inferred from
`lambda_ij`.

**Fail-closed consequence.** `UNRESOLVED_BLOCKING` ⇒ there is no admissible conditional
denominator, so no `W^L_ij,t` target can be formed, independently of the transition matrix.

**Decision token.** one of `RESOLVED_AS_DOCUMENTED` / `RESOLVED_WITH_DECLARED_VARIANT` /
`UNRESOLVED_BLOCKING`.

### 4.3 The consistency condition `(C-LINK)`, and the one-frame question

```
(C-LINK)   ell_i  =  ell_i^movers  +  ell_i^stay  +  ell_i^unobserved
```

| Term | Source |
|---|---|
| `ell_i^movers` | labor services of observed movers, from the pair-level data and `lambda_ij` |
| `ell_i^stay` | home/stayer labor, carried by `P_ii = 1 − m_i`; **not observable in a mover-only frame** |
| `ell_i^unobserved` | movers outside the observed frame; **not zero a priori** for a mover-only frame |

**Rules.**

1. `lambda_ij` and `ell_i` must remain **separately declared provenance fields** with separate
   `*_provenance_id` values;
2. neither may be inferred from the other, and neither may be used to validate the other;
3. a design must either (a) supply all three `(C-LINK)` components from **one coherent frame**, or
   (b) **declare which components are unobserved and report the residual**. It may never assume
   the identity by construction;
4. **one source may satisfy both H5 and H6 only if it is shown to be one coherent frame** — that
   is itself a finding that must be recorded, with the frame's definition, coverage and weights.
   Absent that finding, H5 and H6 stay separate and both must be satisfied independently.

**Current status.** `one_coherent_frame_proven = false`. Both items are `UNRESOLVED_BLOCKING`.

---

## 5. H7 — timing, publication and leakage

| # | Sub-question | Required primary evidence |
|---|---|---|
| H7.1 | the **feature reference period** versus the label window, for every declared feature group | the source reference periods |
| H7.2 | the **publication date** of each source, kept separate from its reference period | the publication record |
| H7.3 | that **no post-decision measurement** enters the predictive information set | the timing comparison |
| H7.4 | the **canonical information set**: window-start features at `t − k`, with the label over `(t−k, t]` | the declared design |
| H7.5 | that the window-end nowcast variant, if used at all, is a **separately labelled** design and not mixed with the canonical one | the declared design |
| H7.6 | that `m` and `ell` do **not** appear as features | the declared feature set |
| H7.7 | that no feature encodes the label, the same-period realized flow, future information or a test target | the declared feature set |
| H7.8 | the **split claim** actually supported: `HELD_OUT_TIME` and/or `HELD_OUT_ORIGIN_ROLE` only | the split design |

**Fail-closed consequence.** `UNRESOLVED_BLOCKING` ⇒ no predictive exercise may be run, because
the information set cannot be shown to be leakage-free.

**Decision token.** one of `RESOLVED_AS_DOCUMENTED` / `RESOLVED_WITH_DECLARED_VARIANT` /
`UNRESOLVED_BLOCKING`.

---

## 6. Packet status table

| Item | Subject | Status at this Issue | Promoted by DSH | Blocks |
|---|---|---|---|---|
| H1 | NBS transition semantics | `UNRESOLVED` | no | all T-family waves |
| H2 | census / 1% table availability and vintage | `UNRESOLVED` | no | affected wave |
| H3 | region coding and crosswalks | `UNRESOLVED` | no | all region-joined objects; the 2000 wave specifically |
| H4 | source weights and cross-wave comparability | `UNRESOLVED` | no | survey-derived waves; cross-wave pooling |
| H5 | pair labor-intensity `lambda_ij` | `UNRESOLVED` | no | population→labor bridge (all families) |
| H6 | origin labor amount `ell_i` | `UNRESOLVED` | no | conditional denominator (all families) |
| H7 | timing, publication and leakage | `UNRESOLVED` | no | predictive information set (all waves) |

Aggregate: **7 of 7 unresolved · 0 promoted by DSH · 0 source verified · 0 dataset opened.**

## 7. What resolving the packet would and would not authorise

**Would authorise.** A later, separately authorized Issue to implement the preregistered bridge
against the frozen P3C contract, for the waves whose items resolved as documented, using the
declared variants where a variant was chosen.

**Would not authorise.** Any ingestion by itself (P-6); any promotion beyond the item actually
resolved; any relaxation of the frozen P3C tolerances, seed, start count, route set or claim
ceiling; any empirical `W^L` fit by this packet; any successor Issue.

## 8. Non-actions performed while preparing this packet

| Action | Count |
|---|---|
| datasets, microdata, tabulations, codebooks, questionnaires or licence texts opened | **0** |
| datasets downloaded, scraped, purchased or ingested | **0** |
| external metadata queries issued | **0** |
| evidence levels promoted | **0** |
| source findings recorded as resolved | **0** |
| scientific / model / training / empirical-bridge calls | **0** |
| HJB / KFE / GE / MATLAB / household calls | **0** |
| `pytest` / full-suite runs | **0** |
| source code, tests, CURRENT governance or P3B artifacts touched | **0** |

The packet is a set of **questions with acceptance criteria**, prepared so that a human verifier
can work them in a bounded way. It deliberately contains no answer.
