# DLH-WL-P3A — empirical label gate for real Chinese interprovincial labor mobility

Issue: **#80 / `DLH-WL-P3A`** — real-data label / provenance evidence gate.
Owner route: `DLH-WL-V1-20260918`.
Authority marker: `DLH_WL_P3A_REAL_DATA_LABEL_PROVENANCE_GATE_AUTHORIZED`.
Reviewer final activation comment: **`5741079748`**.
Operative baseline: `e688a78907b69627800af65970f82d2fd94afae4`.
Status: **gate specification and frozen P3A decision. No empirical fitting is authorized.**

Companion documents:

- `docs/data/DLH_WL_P3A_REAL_DATA_SOURCE_EVIDENCE_2026_09_19.md` (per-source audit);
- `docs/data/DLH_WL_P3A_REGION_TIME_SUPPORT_MATRIX_2026_09_19.md` (support matrix);
- `reports/dlh_wl_p3a_2026_09_19/DLH_WL_P3A_REPORT.md` (Issue report and terminal).

---

## 1. What this gate governs

The V1 scientific object is the **conditional foreign destination share**

```
W^L_ii,t = 0 ;  W^L_ij,t >= 0 ;  sum_{j != i} W^L_ij,t = 1
P_ii,t = 1 - m_i,t ;  P_ij,t = m_i,t * W^L_ij,t (j != i) ;  F_ij,t = ell_i,t * P_ij,t
```

`W^L_ij,t` is a **share of a flow realized inside period `t`**, conditional on origin `i`
having already sent `m_i,t` of its labor abroad. It is not a stock, not a multi-year
transition probability and not a provincial aggregate ratio (P1B §1.1).

This gate answers exactly one question: **does a real, verifiable Chinese interprovincial
data object exist that can carry that target — directly, or only through a separately
authorized bridge?** It does not choose a preferred source, does not design a bridge, does
not fit anything, and does not create a successor issue.

## 2. Frozen vocabulary this gate uses without modification

**Label-semantic classes** (P1B §2, closed set of six):
`TRUE_ANNUAL_OD_FLOW`, `ANNUAL_OD_STOCK_OR_SAMPLE_CROSSTAB`,
`MULTIYEAR_TRANSITION_OR_DERIVED_PROXY`, `PROVINCIAL_AGGREGATE_PROXY`, `RULE_GENERATED`,
`SYNTHETIC`. `RULE_GENERATED` and `SYNTHETIC` are project-internal and are `N/A` for
real-data P3A.

**Bridge vocabulary** (Issue #80 §4): `NONE` / `STOCK_TO_FLOW` / `ANNUALIZATION` /
`SPATIAL_DECOMPOSITION` / `OTHER`.

**Evidence levels** (`project_rules/PROJECT_RULE_RESEARCH_EVIDENCE_AND_CITATION_CURRENT.md`):
`E0` metadata/search · `E1` abstract / official summary · `E2` machine-read substantive
sections · `E3` human-verified. **`E3 = 0` and the Builder may not promote any entry.** A
search result is `E0`/`E1`; a machine read is at most `E2`.

**Directness vs usability** (P1B §3.2) — the two flags are orthogonal and must never be
conflated:
`label_is_direct_target` asks *"is this an empirical annual bilateral flow?"*;
`target_available` asks *"can this row supervise the declared purpose?"*. A bridged empirical
class may become `target_available = true` **only** after an explicit dated bridge/assumption
record exists.

## 3. Gate G1 — direct-target gate (Branch D)

Branch D is available if and only if **all** of the following hold for at least one source:

| # | Condition |
|---|---|
| G1.1 | the source's own documentation verifies the raw object is **newly realized moves inside a single year**, not a presence snapshot and not a `k`-year residence transition |
| G1.2 | `time_semantics = CALENDAR_YEAR` for the object, with the reference period declared |
| G1.3 | origin **and** destination are observed **for the same move** |
| G1.4 | bilateral `(i,j,t)` coverage is documented well enough to construct the destination-share denominator and numerator at the same period |
| G1.5 | population / sample definition, weighting and coverage are declared and harmonization across periods is stated |
| G1.6 | provider, version/edition, licence and access condition are verified |
| G1.7 | feature timing and label-end availability permit a leakage-free same-period feature set under P1B §3.5 |

**Result: G1 is NOT satisfied.** No source in the P3A audit is a verified
`TRUE_ANNUAL_OD_FLOW` object. Branch D is **not available**. (See the source evidence
document §4 and §7.)

## 4. Gate G2 — bridged-pair gate (Branch B)

Branch B is available if and only if: G1 fails, **and** at least one source satisfies:

| # | Condition |
|---|---|
| G2.1 | the raw object is bilateral — origin **and** destination are observed for the same measured unit (transition or snapshot), i.e. the class is `ANNUAL_OD_STOCK_OR_SAMPLE_CROSSTAB` or `MULTIYEAR_TRANSITION_OR_DERIVED_PROXY` |
| G2.2 | the reference window / period definition is documented |
| G2.3 | the population / sample definition and the coverage are documented |
| G2.4 | a bridge **class** from the frozen bridge vocabulary can be named for the object |
| G2.5 | the object is documented well enough that a *separately authorized* bridge / sensitivity design could be specified against it |

**Result: G2 IS satisfied.** Two independent objects satisfy G2.1–G2.5:

- **S1 / S2** — census long-form and 1% sample survey: documented bilateral interprovincial
  **transition** matrices, declared five-year reference windows, declared coverage, with the
  bridge class `OTHER` (a pre-registered, sensitivity-tested `k`-year→annual timing model);
- **S3 / S5** — CMDS annual migrant cross-section and the *Journal of Maps* floating-population
  OD matrix: documented bilateral **stock/sample** objects with declared reference periods,
  with the bridge class `STOCK_TO_FLOW`.

Branch B is therefore **available**, subject to the qualification in §5.5.

## 5. Gate G3 — supportability floor (Branch P)

Branch P is selected if either clause holds:

| # | Clause | Result |
|---|---|---|
| G3.1 | only provincial aggregate / proxy objects are verified | **false** — bilateral pair objects are verified to exist at E1 (S1, S2, S5; S3 conditionally) |
| G3.2 | pair-level source semantics **and** access remain insufficient for every candidate | **partially true, not decisive** — the specific schema/access questions the DLH-1A E3 queue reserves are open, but the objects' bilateral character, reference windows and coverage are documented |

**Result: G3 is NOT decisive.** Branch P is **not selected**.

### 5.5 The qualification that must travel with Branch B

Branch B is a **data-evidence classification about whether a bridge could be specified**. It
is **not** a statement that a bridged label set exists or may be built now. In particular,
under Branch B the following all remain true:

1. no source is `TRUE_ANNUAL_OD_FLOW`, so no `direct_W_supervision` is available anywhere;
2. no source has `target_available_without_bridge = true`;
3. the bridge is a scientific decision requiring **its own dated authority** (P1B §5 item 5);
   none exists;
4. **no empirical `W^L` fit is authorized**, and no real-data adapter, label set, evaluation
   set or model run may be created;
5. stock/transition classes must never be relabelled, rescaled or normalized into
   `TRUE_ANNUAL_OD_FLOW` (P1B §2.2 items 1–2);
6. the concrete region dictionary does not exist, so no canonical row can be instantiated;
7. real `m` and real `ell` provenance does not exist, so even a bridged share would have no
   admissible conditional denominator;
8. the P/B boundary is close; the **substantive** consequence — no empirical `W` work now —
   is identical under Branch B and Branch P. This is recorded so a Reviewer can re-adjudicate
   the label without any change to the scientific prohibitions.

## 6. Terminal selection

Issue #80 §10 defines three terminals. Selection for this Issue:

| Terminal | Selected? | Reason |
|---|---|---|
| `DLH_WL_P3A_REAL_DATA_LABEL_EVIDENCE_GATE__PASS__BRANCH_B` | **YES — selected** | the gate ran to completion on the frozen evidence set; G1 fails, G2 is satisfied, G3 is not decisive; branch `B` |
| `DLH_WL_P3A_REAL_DATA_LABEL_EVIDENCE_GATE__REVIEW_REQUIRED` | no | no internal or source contradiction was found. The cross-reference checks in the source evidence document §6 are consistent: the DLH-1A tier list maps onto the P1B six-class taxonomy without conflict, the feasibility file and the review packet agree on every classification, and the P1B residual open items match the open questions this audit could not close. A taxonomy *refinement* (tier-3 splitting into two P1B classes) is a declared mapping, not a contradiction |
| `BLOCKED_DLH_WL_P3A_SOURCE_AUTHORITY_OR_METADATA` | no | the authorizing evidence was available and was read: the DLH-1A feasibility file, its companion review packet and E3 queue, the accepted P1B schema, the accepted P2D report and the Owner route freeze. External provider metadata could not be fully verified, but Issue #80 §3 explicitly provides the `NOT_VERIFIED_EXTERNAL` disposition for exactly that case, so unverifiable external metadata is a recorded per-source status rather than a block of the gate |

## 7. Frozen P3A decision

```
terminal:  DLH_WL_P3A_REAL_DATA_LABEL_EVIDENCE_GATE__PASS__BRANCH_B
branch:    B — bridged pair object only
```

`Branch D/B/P is a data-evidence classification, not a model-performance ranking.` No model
was run, so no performance statement of any kind is made.

## 8. Gate invariants that survive this Issue

These are **gate invariants**, not recommendations. They remain binding on any later Issue
until superseded by a dated Owner/Reviewer authority.

| Invariant | Statement |
|---|---|
| I1 | the V1 target `W^L_ij,t` is a **same-period conditional flow share**; no source may be described as providing it unless G1 is fully satisfied |
| I2 | `support_mask_ii = false` always; home retention is carried only by `P_ii = 1 - m_i`; the `W` support mask must never encode home retention |
| I3 | no class may be assigned from marginals; a marginal-only object is `PROVINCIAL_AGGREGATE_PROXY` or nothing |
| I4 | normalization never repairs semantic mismatch |
| I5 | evidence levels are per-row properties and are never silently promoted; `E3` requires human verification |
| I6 | `target_available = true` for a bridged empirical class requires an explicit **dated** bridge/assumption record |
| I7 | `m` and `ell` are given inputs, never learning targets and never features; real `m`/`ell` provenance is unresolved |
| I8 | the support set is part of the experiment design and may not change after outcomes are seen |
| I9 | a block with `m_i = 0` or `ell_i = 0` carries no identifiable conditional target; no uniform label may be fabricated for it |
| I10 | mixing `CALENDAR_YEAR` with transition or synthetic time inside one evaluation set is forbidden |
| I11 | synthetic / rule-generated method success is never evidence that a real source identifies `W` |

## 9. Preconditions for any future use of Branch B (recorded, not started)

This section records what a **separately authorized** later Issue would have to establish.
It is **not** a design, **not** a plan with dates, and **not** authorization. No successor
Issue is created by P3A.

A later Issue that wishes to act on Branch B would have to:

1. obtain a dated authority for the specific bridge class and its assumption set, naming the
   exact source, vintage and reference window;
2. resolve the DLH-1A E3 data-side queue items that bear on that source (S4 pair-level field
   existence; S3 codebook and cross-year harmonization; S1/S2 tabulation and transition
   semantics), with human verification rather than machine reading;
3. create the concrete region dictionary and prove the source geography maps onto it;
4. establish real `m` and `ell` provenance with an explicit efficiency-labor basis;
5. declare `calendar_lag_definition` and `outer_iteration_lag_definition` separately, and
   prove a leakage-free feature set under P1B §3.5;
6. declare weights and their harmonization status for every survey-derived row;
7. carry a pre-registered sensitivity analysis over the bridge assumption, so that the
   bridged object is reported as what it is rather than as an annual flow.

Until **all** of these exist, the following remain forbidden by the gate invariants in §8:
any real-data adapter, any real label set, any real evaluation set, any `W^L` estimation, any
`m`/`ell` derivation, and any wording that presents a stock, transition or aggregate object
as an annual bilateral flow.

## 10. Claim-ceiling ladder (applied, not proposed)

| Level | Claim | Available now? |
|---|---|---|
| L0 | "this project has a verified method for the conditional destination-share problem, validated on pre-registered synthetic controls" | **yes** — accepted P2D, `8ae4561ca3b0c78ba1d47045182fa5b4b023ed6d` |
| L1 | "a bilateral Chinese interprovincial stock / transition object is documented at E1 and could support a separately authorized bridge" | **yes** — this Issue, Branch B |
| L2 | "a bridged annual destination-share label set has been constructed and its assumptions pre-registered and sensitivity-tested" | **no** — no dated bridge authority exists |
| L3 | "a conditional destination-share relationship has been estimated on real Chinese provinces" | **no** — no direct target, no `m`/`ell` provenance, no region dictionary |
| L4 | causal, welfare, policy, GE, HJB/KFE or household claims | **no** — outside the route's current authorization |

The P2D ceiling already forbids an "annual bilateral OD data availability claim". This Issue
makes **no** such claim; it records the opposite.
