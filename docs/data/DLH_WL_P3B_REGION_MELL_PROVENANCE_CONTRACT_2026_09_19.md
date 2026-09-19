# DLH-WL-P3B — region dictionary, `m`/`ell` provenance, weights and leakage contract

Issue: **#81 / `DLH-WL-P3B`**. Owner route: `DLH-WL-V1-20260918`.
Authority marker: `DLH_WL_P3B_BRIDGE_SOURCE_PREREGISTRATION_AUTHORIZED`.
Reviewer final activation comment: **`5741234971`**.
Operative baseline: `1f4bee7290da7143fab9612157bd99f83e3216b4`.
Status: preregistration only. **No crosswalk is fabricated. No numeric `m` or `ell` value is
produced. No dataset was downloaded, scraped, purchased, ingested or opened. Scientific /
model / training calls = 0.**

Companion documents:

- `docs/specifications/DLH_WL_P3B_BRIDGE_PREREGISTRATION_2026_09_19.md` (the bridges);
- `docs/data/DLH_WL_P3B_SOURCE_BRIDGE_SENSITIVITY_MATRIX_2026_09_19.md` (source and sensitivity
  matrix);
- `reports/dlh_wl_p3b_2026_09_19/DLH_WL_P3B_REPORT.md` (report and terminal).

---

## 1. Region dictionary specification (candidate, not yet an adapter)

P1B declares the region dictionary id `DLH_WL_REGION_DICT_V1_2026_09_18` as a **declaration
placeholder** and states that the concrete dictionary is a later deliverable. This section
freezes the **specification** of that deliverable. It creates **no** dictionary file, **no**
code table and **no** source crosswalk, and it asserts **no** mapping between any source label
and any dictionary id.

### 1.1 Universe and composition

```
dictionary_id            : DLH_WL_REGION_DICT_V1_2026_09_18
canonical_universe       : 31 provincial-level units under mainland administration
composition              : 4 municipalities + 22 provinces + 5 autonomous regions = 31
region_level             : provincial level only (no prefecture or county level)
```

Unit names, grouped by their conventional code prefix band (prefixes are recorded as the
**candidate** code system; see §1.2):

| Band | Units | Count |
|---|---|---|
| 11–15 | Beijing (municipality), Tianjin (municipality), Hebei, Shanxi, Inner Mongolia (autonomous region) | 5 |
| 21–23 | Liaoning, Jilin, Heilongjiang | 3 |
| 31–37 | Shanghai (municipality), Jiangsu, Zhejiang, Anhui, Fujian, Jiangxi, Shandong | 7 |
| 41–46 | Henan, Hubei, Hunan, Guangdong, Guangxi (autonomous region), Hainan | 6 |
| 50–54 | Chongqing (municipality), Sichuan, Guizhou, Yunnan, Tibet (autonomous region) | 5 |
| 61–65 | Shaanxi, Gansu, Qinghai, Ningxia (autonomous region), Xinjiang (autonomous region) | 5 |
| | **total** | **31** |

The **unit set** above is not in dispute and is the basis of the canonical universe. The exact
numeric code values are **`NOT_VERIFIED_EXTERNAL`** in this Issue and must be verified against
the official national administrative-division code standard edition in force at adapter time.
No code value, and no source label, is asserted by P3B.

### 1.2 Code system

```
code_system              : national administrative-division codes (GB/T 2260 family), province level
code_width               : 2-digit province prefix (candidate)
version_pinning          : REQUIRED — the standard edition in force must be named, and the
                           dictionary must be version-pinned, because cross-year joins are
                           only valid within one pinned version
verification_status      : NOT_VERIFIED_EXTERNAL
```

Preregistered rule: a source may be joined only to a dictionary whose pinned version is either
identical to the source's own coding basis, or accompanied by a **declared, dated** transition
record. Version drift that is not covered by such a record fails closed.

### 1.3 Hong Kong, Macao and Taiwan

| Question | Preregistered answer |
|---|---|
| are they in the canonical universe? | **no** — the canonical universe is the 31 mainland provincial-level units |
| if a source reports them separately | they map to an explicit **`EXCLUDED_NON_MAINLAND`** category, recorded as a declared exclusion, and are **not** folded into any mainland unit |
| if a source reports an undifferentiated "other / abroad / not stated" bucket | maps to **`EXCLUDED_OTHER`** with its mass recorded; it is never distributed across units |
| may an excluded category be used as a denominator component? | **no** — the conditional denominator is built only over the canonical universe |
| fail-closed trigger | any source whose mainland mass cannot be separated from `EXCLUDED_NON_MAINLAND` / `EXCLUDED_OTHER` for a given `(origin, time)` block drops that block |

### 1.4 Municipalities

Beijing, Tianjin, Shanghai and Chongqing are **single provincial-level units**; the dictionary
does **not** decompose them into districts. Consequences that must be declared, not resolved by
convenience:

- their `hukou`-registration and residence geographies are administratively identical to any
  other unit at this level, so no special rule is introduced;
- however, their high in-migration and their large floating populations mean that the
  `S^h` vs `S^r` distinction (§3.3 of the source matrix) is materially more important for them
  than for other units, so the declaration is mandatory rather than optional;
- the municipality treatment must be **identical across all waves**; introducing a
  municipality-specific rule is a region-dictionary design change and requires a dated
  amendment.

### 1.5 Historical boundary and code changes relevant to the reference waves

| Event | Date | Effect on the waves used here |
|---|---|---|
| Hainan separated from Guangdong | 1988 | all waves (2000, 2005, 2010, 2015, 2020) post-date it: **no merging required** |
| Chongqing separated from Sichuan as a directly-administered municipality | 1997 | all reference **moments** post-date it, so all five waves report Chongqing separately |
| pre-1997 sources | — | would require a Sichuan+Chongqing **merged variant**; fail closed if any source covers pre-1997 |

**Chongqing consistency — the live issue, stated precisely.** The T-family migration item asks
for residence **five years before** the reference moment. For the 2000 wave (reference moment
2000-11-01) the window is therefore `[1995-11, 2000-11]`, and **1995 precedes Chongqing's 1997
separation**. The origin geography for the early part of that window is thus administratively
Sichuan, not Chongqing. Whether the published tabulation codes those respondents to Chongqing
(by applying the current dictionary to the reported place name) or leaves them in Sichuan is a
**tabulation/coding-convention question that is `NOT_VERIFIED_EXTERNAL`** in this Issue.

Preregistered handling (chosen before any outcome, applied identically):

```
for the 2000 wave only, exactly one of the following MUST be preregistered and applied:
  (a) MERGED_VARIANT : Sichuan and Chongqing are combined into one unit, giving a 30-unit
                       universe for that wave, with the merge recorded as a declared
                       source-specific category;
  (b) WAVE_EXCLUDED  : the 2000 wave is excluded from any pooled or cross-wave design;
  (c) AS_REPORTED    : the wave is used as published, WITH a declared unresolved-coding risk
                       and the resulting origin-role ambiguity carried into the sensitivity
                       design (axis A13).
Option (c) may not be chosen silently: it must be declared, and the merged variant must still
be evaluated as a sensitivity replicate. No third-way "guess" is permitted.
```

### 1.6 Source-specific missing and merged categories

The dictionary contract requires each source to declare, per wave:

```
- units reported              (the units the source actually tabulates)
- units absent                (in the universe but not reported)
- units merged                (two or more universe units reported as one)
- excluded categories         (EXCLUDED_NON_MAINLAND, EXCLUDED_OTHER, undetermined hukou)
- coding basis                (dictionary version used by the source)
- mass of each excluded/merged category
```

Recognised source-specific categories that must be declared rather than silently absorbed:
an undetermined/other hukou-origin bucket; a non-mainland bucket; units reported only in
aggregate; and any unit whose reporting changed between waves. The `Xinjiang Production and
Construction Corps` question (whether a source reports it inside Xinjiang or separately) is
`NOT_VERIFIED_EXTERNAL` and must be declared per source.

### 1.7 Rule for constructing the common region universe

```
U1. Start from the canonical 31-unit universe.
U2. For a given wave, compute the mappable set = units the source reports with a verified
    one-to-one correspondence to the pinned dictionary version.
U3. If a wave requires a merged variant (section 1.5) the variant is constructed by
    SUMMING the merged units' counts, never by splitting, distributing or imputing.
U4. The common universe for a multi-wave design is the INTERSECTION of the per-wave mappable
    sets; a wave that cannot reach the intersection under (1.5) is excluded, not patched.
U5. The intersection, the excluded units and the excluded mass are reported for every design.
U6. The support mask is NOT derived from the dictionary: the dictionary fixes the region
    universe, and the support mask is a separate, separately evidenced object (P1B section 3.4).
```

### 1.8 Fail-closed behaviour

| Condition | Required behaviour |
|---|---|
| a source label cannot be mapped to exactly one dictionary unit | **drop the entire `(origin, time)` block** containing it, with a recorded reason; never approximate |
| two source labels map to the same unit | treat as a declared merged category (sum), or fail closed if the merge basis is unverified |
| a source reports a unit not in the pinned dictionary | fail closed for the affected block |
| a wave's unmappable mass exceeds the preregistered threshold | reject that wave for that time id; the threshold is frozen before execution |
| coding version of the source is unnamed | fail closed |
| a source's total mass cannot be reconciled to the excluded categories | fail closed |

Every fail-closed event must be **reported, counted and attributed**, so that the surviving
support is auditable rather than silently reduced.

## 2. `m_i,t` derivation rules

`m` is a **given accounting input**, never a learning target and never a feature (P1B §3.3).
P3B states candidate derivations and computes none.

| Route | Derivation | Preconditions | Status |
|---|---|---|---|
| M-A (annual transition) | `m_i,t = 1 − P_ii,t` from an **authorized annual** transition matrix `P` | the time bridge T1/T2 has been selected under the preregistered rule, the induced spread over `𝓕` is within `tau_W`, and the annualization is admitted for that window | **candidate-derived given input only**; `NOT_PRODUCED_BY_P3B` |
| M-B (stock objects) | **not available** from stock shares alone | `m` is a within-period outflow probability; a stock snapshot conveys presence, not transitions. Even under the stock→flow bridge, recovering `F` requires pair-level duration `D_ij` (§3 of the preregistration), so `m` inherits the `NOT_IDENTIFIED` status | `NOT_IDENTIFIED` |
| M-C (repeated cross-sections) | **not available** | only the net stock change is identified from two cross-sections; inflow and outflow cannot be separated | `NOT_IDENTIFIED` |
| M-D (aggregate/proxy objects) | **prohibited** | marginals never identify the pair distribution, and `m` derived from unrelated totals is forbidden by Issue #81 §7 and P1B §2.2 item 4 | forbidden |

Mandatory declarations attached to any future `m`:

```
m_provenance_id            : REQUIRED (source/estimator identity)
m_unit_basis               : PERSONS or EFFICIENCY_LABOR, declared and consistent with ell_unit
m_time_alignment           : REQUIRED — must refer to the same window as the label
accounting_period_alignment: REQUIRED (P1B section 3.3)
m_is_never_a_feature       : REQUIRED declaration
m_not_learning_target      : REQUIRED declaration
```

**Identification warning that must travel with M-A.** Because the time bridge does not identify
`P` from `T^(k)` alone, `m` derived by M-A is **assumption-dependent**: in the exact 2-region
example of the preregistration §2.2, the same two-year observation yields `m = 3/4` or
`m = 1/4`. A future design must therefore report `m` **jointly with** the enumeration of `𝓕`
and the selection rule, and must not present `m` as data-identified.

## 3. `ell_i,t` external provenance requirements

`ell` is a **given accounting input**, never a learning target and never a feature. No real
efficiency-labor conversion exists in this repository (P1B §5 item 3). P3B requires the
following of any future source.

### 3.1 Required basis

```
ell_unit ∈ { EFFICIENCY_LABOR,
             EMPLOYED_PERSONS_DECLARED_AS_PROXY,
             LABOR_FORCE_DECLARED_AS_PROXY }
```

Population counts may **not** be silently treated as efficiency labor (P1B §3.3). If either
proxy basis is used it must be declared as a proxy with its own sensitivity replicate, and
the resulting claim ceiling must say so.

### 3.2 Required properties

| # | Requirement |
|---|---|
| E1 | **scope**: the origin labor amount for the same `(i, t)` as the label — employed persons, labor force, or an efficiency-labor equivalent |
| E2 | **unit**: explicit, with hours/efficiency content stated if `EFFICIENCY_LABOR` is claimed |
| E3 | **time alignment**: same `time_id` window as the label; `accounting_period_alignment` declared |
| E4 | **timing**: the `ell` measurement must **precede or coincide with** the destination decision; a post-decision `ell` measurement is same-period leakage and is forbidden as an input |
| E5 | **no automatic substitution**: total population, urbanization, GDP or any unrelated total may not stand in for `ell` |
| E6 | **no derivation from unrelated totals**: `ell` may not be inferred from a provincial aggregate that measures something else |
| E7 | **provenance**: `ell_provenance_id`, provider, version/vintage, licence/access |
| E8 | **consistency with `m`**: `m_unit_basis` and `ell_unit` must be reconcilable, so that `F_ij = ell_i · m_i · W_ij` is dimensionally coherent |
| E9 | **coverage**: the `ell` source must cover the same region universe as the label, or the intersection rule of §1.7 applies |

### 3.3 `ell_i` and the pair-level `lambda_ij` are two linked provenance requirements

The population→labor-service bridge requires the **pair-level** weight
`lambda_ij = rho_ij · phi_ij` — expected labor service per observed mover to destination `j`
(preregistration §4.2). Putting `ell_i` on an efficiency-labor basis requires an **origin-level**
labor amount. These are **logically distinct moments** and neither identifies the other:

| | pair-level `lambda_ij` | origin-level `ell_i` |
|---|---|---|
| what it measures | conditional labor service per **observed mover/person** to destination `j` | **total** origin labor amount entering `F_ij = ell_i · m_i · W_ij` |
| conditioning | destination `j` within origin `i` | origin `i` only; no destination dimension |
| does it include stayers? | no — movers only | yes, via `P_ii = 1 − m_i` (home retention) |
| role | reweighting destination shares | scaling the origin's total flow |

```
REQUIRED_EXTERNAL (two linked requirements, ideally supplied by ONE coherent
                   labor-intensity / employment data system):
   R-lambda : pair-level   lambda_ij = rho_ij * phi_ij   (destination-varying, on the observed
                                                          mover frame)
   R-ell    : origin-level ell_i                          (total origin labor, consistent with
                                                          m_i and with the home/stayer share
                                                          1 - m_i)
STATUS     : no such source is verified in this repository or in this Issue.
CONSEQUENCE: BOTH requirements remain unsatisfied and must stay separately declared, so the
             population->labor bridge AND the ell basis remain blocked, and the pair target
             remains UNRESOLVED, even if a clean bilateral matrix exists.
```

A sufficiently rich joint microdata or administrative data system **could** supply both
coherently, and pair-level labor-intensity information may aggregate into an origin-level basis
**if** the population frame is complete and weights and stayers are covered. That is a
possibility, not an identity. Until a source proves that both come from one coherent frame,
`R-lambda` and `R-ell` remain **separately required fields**, and neither may be inferred from,
substituted for, or used to validate the other. This is recorded so that a later Issue cannot
satisfy the `ell` requirement formally while leaving the labor-service bridge silently
unaddressed — or vice versa.

### 3.4 Frozen consistency condition between the pair-level and origin-level objects

Let `N_ij` be the observed i→j mover count and `𝓜_i = {j : N_ij > 0}`. Define the
mover-implied labor leaving `i` as

```
ell_i^movers  :=  Σ_{j ∈ M_i}  N_ij * lambda_ij
```

Any design using both `lambda_ij` and `ell_i` must satisfy, with every term declared from the
same `(i, t)`:

```
(C-LINK)   ell_i  =  ell_i^movers  +  ell_i^stay  +  ell_i^unobserved
```

| Term | Meaning |
|---|---|
| `ell_i^movers` | labor services of observed movers, from the pair-level data and `lambda_ij` |
| `ell_i^stay` | home/stayer labor, carried by `P_ii = 1 − m_i`; **not observable** in a mover-only frame |
| `ell_i^unobserved` | movers outside the observed frame; **not zero a priori** for a mover-only frame (families S and C) |

A design must either (a) supply all three components from one coherent frame, or (b) **declare
which components are unobserved and treat `(C-LINK)` as a consistency check with a reported
residual** — never as an equality assumed by construction. `(C-LINK)` is a consistency
condition, not an identification of either object; satisfying it does not make `lambda_ij` and
`ell_i` the same thing, and failing it does not by itself invalidate either.

## 4. Weights, harmonization and leakage contract

### 4.1 Survey / design weights

| Requirement | Statement |
|---|---|
| W1 | every survey-derived row carries `sample_weight` and `sample_weight_source`, or `null` with a declared reason |
| W2 | the weight variable identity is named; a re-derived weight is acceptable only with its derivation declared |
| W3 | weights reweight **sampled persons**; they cannot manufacture labor-force status that the instrument did not collect (so weights alone cannot supply the §3.3 labor basis) |
| W4 | unweighted and weighted variants must both be reported when weights exist, as separate sensitivity replicates |

### 4.2 Cross-year harmonization

| Requirement | Statement |
|---|---|
| H1 | questionnaire harmonization: any change in the migration question's reference period or wording between waves must be declared, and the affected waves may not be pooled silently |
| H2 | sample-design harmonization: frame, stratification and sampling-unit changes must be declared |
| H3 | weight harmonization: the harmonization method must be declared; without a declared record, cross-year pooling is **blocked** |
| H4 | census/sample comparability: a full-enumeration wave and a 1 % sample wave may be pooled only with a declared comparability record, because their sampling variance differs by orders of magnitude |
| H5 | the harmonization record is dated and versioned, and is part of the frozen design |

### 4.3 Missing-cell and structural-zero handling

| Requirement | Statement |
|---|---|
| Z1 | `STRUCTURAL_ZERO` requires a documented `structural_zero_reason`; an undocumented zero may not be declared structural |
| Z2 | an observed zero inside the support is `OBSERVED_ZERO` and must not be deleted after seeing evaluation results |
| Z3 | `MISSING` is neither a zero nor an impossibility; missing rows may be predicted but **never** supervised, and can never set `target_available = true` |
| Z4 | a source's undocumented zero cells are `MISSING` or `OBSERVED_ZERO` by default, never `STRUCTURAL_ZERO` |
| Z5 | pair-support stability: the support set is part of the experiment design and may not change after outcomes are seen; any wave-to-wave support change must be declared and handled by the §1.7 intersection rule |

### 4.4 Pair-support stability

A pair observed in one wave and not in another is not evidence that the pair became impossible.
Preregistered handling: retain the pair in the intersection only if it is observed or validly
missing in **every** wave of the design; otherwise report it as a support-change event and
evaluate the design both with and without it (sensitivity axis A15/A16).

### 4.5 Feature availability at prediction time

Canonical P3 design decision (preregistered, not left to adapter time):

```
CANONICAL  : window-start design — the feature set uses only information available at t-k,
             the start of the transition window. The label describes moves realized during
             (t-k, t]. This is the only design under which the exercise is a forecast rather
             than a same-window nowcast.
VARIANT    : window-end nowcast — features available at t, including information from inside
             the window. Admissible ONLY as a separately labelled design with its own row and
             its own claim, never mixed with the canonical design.
```

`feature_available_at_prediction_time` must be `true` for the canonical design; if any declared
input becomes known only after the reference moment, it is `false` and the design is rejected.
The four `*_availability_time` and four `*_transformation_log` lists of P1B §3.5 must each
match their feature-name list in length and order.

### 4.6 Publication and revision timing

| Requirement | Statement |
|---|---|
| R1 | the label's **reference period** and its **publication date** are recorded separately; a prediction exercise claiming information "at t" may not use data published after its own exercise date unless declared |
| R2 | revised vintages must be declared; a design may not switch vintage mid-evaluation |
| R3 | the dictionary's pinned coding version is part of the publication record |

### 4.7 Leakage rules

| Requirement | Statement |
|---|---|
| L1 | no feature may encode the label, the same-period realized flow, any future information or any test target |
| L2 | `m` and `ell` are never features, and the group metadata may not imply otherwise |
| L3 | normalization statistics are fitted on training data only |
| L4 | destination-role exposure is recorded honestly: when a test-origin region also appears among training destinations, its destination-side features are legitimately visible, this is **not** leakage, and it **caps** the generalization claim |
| L5 | the window-start canonical design (§4.5) is the primary leakage control; deviations must be declared |

### 4.8 Split claims

| Requirement | Statement |
|---|---|
| S1 | `split_assignment`, `split_block_id`, `split_policy_id` are mandatory per row |
| S2 | blocking is by **time** and by **origin role**, not by region identity |
| S3 | the strongest available claim is `HELD_OUT_TIME` or `HELD_OUT_ORIGIN_ROLE`; `UNSEEN_REGION` is **unavailable** to this design because test origins appear as training destinations |
| S4 | with five waves and each wave a 5-year object, a held-out **time** claim requires generalizing across 5-year periods — a strong requirement that must be stated, not assumed |
| S5 | `test_touches_train_origin` and `test_regions_appear_as_train_destinations` are recorded as measured, never asserted |

## 5. What this contract does not contain

- no dictionary file, no code table, no source crosswalk, no mapping of any source label;
- no numeric `m`, no numeric `ell`, no efficiency-labor conversion factor;
- no weight value, no harmonization factor, no region mass;
- no threshold numeric value (the unmappable-mass threshold, `tau_W`, `pi_max` and the search
  parameters are all frozen by Reviewer authority before execution, not by P3B);
- no executed bridge, no label, no target, no evaluation set.

Every entry is a requirement, a declared status token, or a carried-over P1B normative rule.
The region unit set is stated at the level at which it is not in dispute; every code value and
every source mapping is explicitly `NOT_VERIFIED_EXTERNAL`.
