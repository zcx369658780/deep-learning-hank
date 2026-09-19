# DLH-WL-P3E — latent labor measurement architecture freeze — report

Issue: **#84 / `DLH-WL-P3E`**. Owner route: `DLH-WL-V1-20260918` plus the dated amendment
`docs/decisions/DLH_OWNER_ROUTE_AMENDMENT_LATENT_LABOR_MEASUREMENT_2026_09_19.md`.
Authority marker: `DLH_WL_P3E_LATENT_LABOR_MEASUREMENT_ARCHITECTURE_AUTHORIZED`.
Reviewer final activation comment: **`5742332586`**.
Operative baseline: `2f4bd66343ed8ae8a95e36316d2730084bd24e52`.
Dedicated branch: `dsh/issue-84-dlh-wl-p3e-latent-labor-measurement-2026-09-19`.

---

## 0. Terminal

```
DLH_WL_P3E_LATENT_LABOR_MEASUREMENT_ARCHITECTURE__PASS__READY_FOR_POST_E3_IMPLEMENTATION
```

The latent labor measurement architecture is frozen and internally consistent: the latent objects,
their units, the preserved structural backbone, the symbolic measurement equations, the wedge
identification and regularization discipline, the residual budget and the three-model comparison
contract are all stated, mirrored in the TOML and dimension-checked. **PASS does not authorize
real-data implementation.** It means only that the architecture is frozen and may be used **after**
the required H items of Issue #83 are resolved by the human/Owner gate.

### 0.1 Terminal selection (Issue #84 §11)

| Terminal | Selected? | Reason |
|---|---|---|
| `DLH_WL_P3E_LATENT_LABOR_MEASUREMENT_ARCHITECTURE__PASS__READY_FOR_POST_E3_IMPLEMENTATION` | **YES — selected** | every architecture element the Issue requires is frozen and consistent: the latent-state/accounting vocabulary with units and block membership (§3); the structural distance + economic-gap backbone preserved with masked conditional normalization (§4); symbolic measurement equations `M1`–`M6` with declared error and coverage structure and **no identity** between any observation and any latent object (§5); the wedge identification and regularization matrix with all eight required fields per wedge and the ten identification rules (§6); the residual budget `RB1`–`RB8` with the no-double-residual statement and its fail-closed status (§7); the `S0`/`S1`/`S2` comparison contract with frozen common elements and rules (§8); the five first-wave Owner choices (§9); the future diagnostics `D1`–`D10` (§10); and a machine-readable mirror with no empirical value and no new numeric threshold (§11). No data, source, bridge or model execution occurred, and no H item was resolved or promoted. |
| `DLH_WL_P3E_LATENT_LABOR_MEASUREMENT_ARCHITECTURE__REVIEW_REQUIRED` | no | not selected: no requirement of Issue #84 §1–§10 is left unfrozen, no accepted P3A/P3B/P3C semantic is contradicted, the 16 inherited Reviewer numeric thresholds are unchanged, and the residual/wedge rules are closed and fail-closed rather than discretionary. The architecture makes two deliberate non-choices — it does **not** specify the production/government blocks (they are registered only) and it does **not** decide whether `ell_star` is estimated jointly — and both are declared in place as later-Issue objects rather than left silent. |

`READY_FOR_POST_E3_IMPLEMENTATION` is a statement about the **architecture**, not a licence: the H1–H7
packet remains 7 of 7 `UNRESOLVED` with 0 promotions, and Issue #83 remains the only authority that
can change that.

## 1. Deliverables

| # | Path | Role |
|---|---|---|
| 1 | `docs/specifications/DLH_WL_P3E_LATENT_LABOR_MEASUREMENT_ARCHITECTURE_2026_09_19.md` | the architecture: latent vocabulary and units, backbone, measurement families, wedge discipline, residual budget, `S0`/`S1`/`S2`, Owner choices, diagnostics, invariants `E1`–`E20` |
| 2 | `docs/data/DLH_WL_P3E_MEASUREMENT_AND_IDENTIFICATION_MATRIX_2026_09_19.md` | the matrix layer: latent↔observation matrix, measurement-equation matrix, the eight-field wedge records, moment-assignment matrix, dimension accounting, model comparison matrix, diagnostics × model matrix, H-dependency matrix |
| 3 | `configs/dlh_wl_p3e_latent_labor_measurement.toml` | machine-readable mirror: latent objects, units, backbone, `M1`–`M6`, wedges with the eight fields, budget rules, models, comparison rules, Owner choices, prohibitions, diagnostics, inherited P3C threshold mirror |
| 4 | this report | Issue report and terminal |

## 2. What was read (fresh, read-only)

1. `AGENTS.md`, `tasks/TASK_INDEX_CURRENT.md`;
2. Owner route freeze `docs/decisions/DLH_OWNER_ROUTE_FREEZE_WL_V1_2026_09_18.md`, and the dated
   amendment `docs/decisions/DLH_OWNER_ROUTE_AMENDMENT_LATENT_LABOR_MEASUREMENT_2026_09_19.md`;
3. Issue **#83 / `DLH-WL-P3D`** body and its Owner decision comment `5742312556` (choices A–E,
   H1–H4 still requiring primary-source verification, H5/H6/H7 design-level notes);
4. accepted P3A Branch B (`docs/specifications/DLH_WL_P3A_EMPIRICAL_LABEL_GATE_2026_09_19.md`);
5. accepted P3B preregistration and the region/`m`/`ell` provenance contract — in particular
   `(A1)`–`(A4)`, `(P-L)`, `lambda_ij = rho_ij·phi_ij`, `(C-LINK)`, the `ell_unit` token set, the
   region universe rules `U1`–`U6`, the weights/harmonization/leakage contract and the window-start
   canonical rule;
6. accepted P3C freeze `docs/specifications/DLH_WL_P3C_EXECUTION_READINESS_FREEZE_2026_09_19.md` and
   `configs/dlh_wl_p3c_bridge_readiness.toml` (thresholds, `F_all_exact`/`F_search_tol`, `R1`–`R4`,
   claim ceiling, invariants `C1`–`C21`) and the H1–H7 packet;
7. Issue **#84** body and its single reviewer comment `5742332586` (activation).

**No dataset, microdata, tabulation, codebook, licence text or published table was opened.** No
crosswalk, no source label and no statistic was inspected. No external metadata query was issued:
every element this Issue needed was a Reviewer-frozen value, an Owner decision or an accepted
requirement statement, not an external fact.

## 3. Latent state definitions and equations

### 3.1 The six latent objects (frozen notation and units)

| Symbol | Name | Unit | Kind |
|---|---|---|---|
| `W_star_ij,t` | latent conditional destination share of labor services | dimensionless share | **the V1 learning object** |
| `m_star_i,t` | latent outflow share / transition intensity | dimensionless, `(0, 1]` | given accounting input |
| `ell_star_i,t` | latent effective origin labor amount | efficiency-labor units | given accounting input |
| `N_workers_star_i,t` | latent worker quantity | persons | latent component |
| `h_star_i,t` | latent hours / intensity | hours / person | latent component |
| `e_star_i,t` | latent efficiency per hour | efficiency-labor units / hour | latent component |

```
ell_star_i,t  =  N_workers_star_i,t  *  h_star_i,t  *  e_star_i,t
```

This decomposition is a **modeling decomposition**, exactly as the amendment §2 states; it is not a
claim that the three factors are separately identified.

### 3.2 Accounting equations (tier 1, imposed, never fitted)

```
W_star_ii,t = 0 ;  W_star_ij,t >= 0 ;  sum_{j != i} W_star_ij,t = 1
P_ii,t      = 1 - m_star_i,t
P_ij,t      = m_star_i,t * W_star_ij,t                       (j != i)
F_ij,t      = ell_star_i,t * P_ij,t  =  ell_star_i,t * m_star_i,t * W_star_ij,t
```

No residual parameter may enter these lines (`RB3`). The pair target is not re-derived and `m`/`ell`
keep their inherited status as given accounting inputs.

### 3.3 Derived object used by the measurement layer

```
omega_i,t  :=  h_star_i,t * e_star_i,t        ( efficiency-labor units per person )
```

`omega` is the **only** route by which a worker count can anchor `ell_star`. It may not be free per
region and requires a declared regularization form (`WEDGE_OMEGA`).

### 3.4 Block membership

| Block | Objects entering | Status in this Issue |
|---|---|---|
| household | `m_star`, `ell_star`, `W_star` enter only through the accepted accounting, as **given inputs** | inherited unchanged; **not re-specified** |
| firm / production | `ell_star` as effective labor, with capital and the registered productivity object `A_i,t` | **registered only**, form not specified |
| flow-accounting | the tier-1 identities of §3.2 | the accounting tier |
| measurement | every observation and its relation to the latent objects (`M1`–`M6`) | **frozen here** |
| government | `G_i,t` at its accounting location | **registered only** |

### 3.5 Identification status (closed vocabulary, one per object per design)

| Object | Status now | Upgrade authority |
|---|---|---|
| `W_star` | `STRUCTURALLY_DEFINED_NOT_OBSERVED` | not upgradable by measurement; it stays the structural/search object |
| `m_star`, `ell_star`, `N_workers_star` | `LATENT__BLOCKED_BY_H` | Issue #83 human gate only |
| `h_star`, `e_star` | `LATENT__NOT_SEPARATELY_IDENTIFIED` | Issue #83 human gate only |
| `omega`, `A`, `G` | `LATENT__PRIOR_REGULARIZED` | later Reviewer authorization only |
| covered / uncovered split | `MEASUREMENT_CHANNEL_DECLARED_NOT_CALIBRATED` | Issue #83 human gate only |

The Builder may upgrade **no** status (`E11`).

## 4. Structural latent-flow backbone (preserved)

```
s_ij,t       =  beta_d * distance_ij  +  beta_gap' * economic_gap_ij,t  +  beta_z' * Z_ij,t
W_star_ij,t  =  exp(s_ij,t) / sum_{l != i, l in S_i,t} exp(s_il,t)     for j != i, j in S_i,t
W_star_ij,t  =  0                                                      for j = i or j not in S_i,t
```

| Property | Frozen statement |
|---|---|
| required terms | static geographic friction (`distance`); wage/income opportunity gap; output/productivity opportunity gap |
| optional terms | accessibility and policy/friction terms **only if later verified** |
| conditionality | masked row-softmax; diagonal false by construction |
| support | a design object; never widened to fit an observation; never changed after outcomes (`C10`, `B2`) |
| coefficients | symbolic only — **no value, sign estimate or prior magnitude is frozen** (`B5`) |
| expected signs | declared design priors, not findings; a sign reversal is reported, never absorbed by redefining the gap variable (`B6`) |
| ML | additive/augmenting, separately identified, dimensionality-declared, regularized; never absorbs a structural term (`B4`, `E3`) |
| timing / leakage | every gap and `Z` term must be window-start available; `m_star`, `ell_star` and same-period flows are never features (`B7`, `B8`, P3B `L1`–`L2`) |
| why preserved | the accepted P2 result found the correctly specified parametric baseline was not outperformed by the small neural mapping; the structural score is therefore retained rather than replaced (`B3`) |

Prohibited inside the backbone: any observation as an argument; an undeclared per-pair free
intercept; per-wave or per-region re-tuning after outcomes (`C17`).

## 5. Measurement equations (symbolic; no empirical values)

| ID | Observed object | Latent target | Equation | Wedge | Status | Blocked by |
|---|---|---|---|---|---|---|
| `M1` | `T_obs^(k)_ij,t` person-based k-year residence transition share | `Pp^(k)_ij,t` latent **person-based** k-step residence transition | `T_obs^(k)_ij,t = (1 − kappa_res_t)·Pp^(k)_ij,t·1{j∈frame} + zeta_res_ij,t + eps_res_ij,t` | `WEDGE_RES` | `NO_SOURCE_VERIFIED__BLOCKED_BY_H1_H3` | H1, H3 |
| `M2` | `L_obs_i,t` employed persons / labor force / unit employment | `N_workers_star_i,t` | `L_obs_i,t = q_cov_i,t·N_workers_star_i,t + eps_L_i,t` | `WEDGE_COV` | `NO_SOURCE_VERIFIED__BLOCKED_BY_H2_H4` | H2, H4 |
| `M3` | `H_obs_i,t` hours / intensity | `h_star_i,t` | `H_obs_i,t = q_hours_i,t·(N_workers_star_i,t·h_star_i,t) + eps_H_i,t` | `WEDGE_HOURS` | blocked by H2/H4, or `LATENT__PRIOR_REGULARIZED` if absent | H2, H4 |
| `M4a` | `ELL_obs_i,t` efficiency labor (direct basis) | `ell_star_i,t` | `ELL_obs_i,t = q_eff_i,t·ell_star_i,t + eps_eff_i,t` | `WEDGE_EFF` | `NO_SOURCE_VERIFIED__BLOCKED_BY_H6` | H6 |
| `M4b` | `N_obs_i,t` employed-persons proxy | `ell_star_i,t` **jointly** with `N_workers_star_i,t`, `omega_i,t` | `N_obs_i,t = q_cov_i,t·N_workers_star_i,t + eps_L_i,t`; `ell_star_i,t = omega_i,t·N_workers_star_i,t` | `WEDGE_COV` + `WEDGE_OMEGA` | `NO_SOURCE_VERIFIED__BLOCKED_BY_H6` | H6 |
| `M5` | `COV_obs_i,t` social-insurance / unit-employment channel | `N_cov_star_i,t` in `N_workers_star = N_cov_star + N_unc_star` | `COV_obs_i,t = q_si_i,t·N_cov_star_i,t + eps_cov_i,t` | channel registry entry | `MEASUREMENT_CHANNEL_DECLARED_NOT_CALIBRATED` | H2, H4 |
| `M6` | `Y_obs`, `K_obs`, `w_obs`, `G_obs` | `A_i,t`, `K_star_i,t`, `ell_star_i,t`, `G_i,t` | **registered only**; no functional form chosen | `WEDGE_TFP`, `WEDGE_GOV` | `REGISTERED_NOT_SPECIFIED_IN_THIS_ISSUE` | H2, H7 |

**Frozen reading of `M1`.** The observed residence object measures **people-based multi-year residence
transitions**, not labor-service shares. The labor-service conditional share `W_star` is reached only
through the accepted P3B T-family bridge and the `lambda` / H5 route. No identity `W_obs = W_star`
exists (`E1`, `E18`).

**Frozen reading of `M4b` (Owner choice D).** The proxy observation measures **worker quantity**, not
`ell_star`:

```
ell_star_i,t  !=  N_obs_i,t    unless  q_cov = 1  AND  omega = 1,   which is NEVER assumed
ELL_PROXY_IDENTITY_NOT_ASSUMED
```

The equality is admissible only as the declared sensitivity variant `ELL_PROXY_UNIT_INTENSITY_VARIANT`,
reported with its own row.

**Frozen readings that apply to every family.** No numeric `q` of any kind is chosen; no informal or
uncovered share is assumed; social-insurance enrollment is never total employment; a job count is
never a worker count without a declared equation; an unclassified bucket is reported, never
distributed; a post-decision measurement is never an input (P3B `E4`).

## 6. Measurement-wedge identification and regularization matrix

Every wedge carries the complete eight-field record — **symbol; equation location; economic
interpretation; disciplining source/moment; allowed dimensionality; prior/regularization;
sensitivity requirement; claim ceiling** — before it may appear in any equation; an incomplete
record is `WEDGE_RECORD_INCOMPLETE__NOT_ADMISSIBLE`.

| Wedge | Tier | Symbol | Equation | Disciplined by | Allowed dimensionality | Prior / regularization | Sensitivity | Claim ceiling |
|---|---|---|---|---|---|---|---|---|
| `WEDGE_RES` | 3 | `kappa_res_t` | `M1` | H1/H3 source semantics by documentation, not by fit | wave/source scalars; a declared semantic variant; **never** per-pair | resolved mapping value when H1 resolves semantics; else a declared `L_*` form with prior | residence-semantics replicate | a measurement discrepancy, never a migration cost |
| `WEDGE_COV` | 3 | `q_cov_i,t` | `M2`, `M4b` | `M5` channel if supported; else the macro employment identity | declared `L_*`; a per-region-per-period free vector is forbidden | declared prior with reported sensitivity | anchored vs prior-only | source coverage, never a labor-supply distortion |
| `WEDGE_HOURS` | 3 | `q_hours_i,t` | `M3` | the `M3` source if it exists; else a prior | declared `L_*` | required prior; `h_star` may not be free per region | prior-scaled | a measurement basis, never a leisure preference |
| `WEDGE_EFF` | 3 | `q_eff_i,t` | `M4a` | the `M4a` source if it exists; else a prior | declared `L_*` | required prior, with the `h`/`e` split status | split-sensitivity (with `WEDGE_OMEGA`) | a measurement basis, never a technology claim |
| `WEDGE_OMEGA` | 3 | `omega_i,t = h_star·e_star` | `M4b` | `M3` + `M4a` jointly; else a prior | declared `L_*`; free per region forbidden | required, form declared | `ELL_PROXY_UNIT_INTENSITY_VARIANT` | a decomposition, never an identified productivity level |
| `WEDGE_TFP` | 4 | `A_i,t` | `M6` | declared macro moments: output, capital, wage | declared low-dimensional form | required | productivity-prior replicate | a registered productivity object, never a causal effect |
| `WEDGE_GOV` | 5 | `G_i,t` | `M6` | its **own** anchor or prior **plus** a moment set disjoint from every labor wedge | bounded by its declared form; unbounded provincial free form forbidden | anchor or prior required | anchor-relaxation replicate | an economic block with its own moments, never a provincial balancing residual |

**Identification rules `I1`–`I10`** (frozen): complete record; declared dimensionality and free-count
(else `UNRESTRICTED_WEDGE_FORBIDDEN`); no anchor-free region × period wedge; at most one partner of an
unidentified split free (`h_star`/`e_star`); the six-element forbidden set not simultaneously
unrestricted; an H-blocked wedge is fixed by prior or its dimension set is excluded
(`H_BLOCKED_WEDGE_FAIL_CLOSED`) and is **never freed to compensate**; no wedge introduced solely to
close provincial output; no wedge reported as data-identified without a source-specific contract;
every active wedge reports its sensitivity replicate; any violation makes the design
`RESIDUAL_BUDGET_EXCEEDED__NOT_ADMISSIBLE`.

**Regularization forms** (`L_constant`, `L_time`, `L_factor`, `L_anchored`, `L_grouped`) are declared
before execution; their free-parameter counts are reported in the dimension-accounting table `D9`;
changing a form or partition after outcomes is a design violation.

## 7. Residual budget and the no-double-residual rule

```
TIER 1  observed / accounting identities      imposed exactly, never fitted
TIER 2  low-dimensional structural mobility   the section 4 backbone
TIER 3  source-specific measurement wedges    section 6, disciplined per the matrix
TIER 4  production / productivity residuals   A_i,t (registered)
TIER 5  government residual                   G_i,t, only if separately anchored and bounded
```

```
RB1  every free residual block has a non-empty declared moment set
RB2  a block's declared free-parameter count may not exceed its assigned moment count
RB3  tier-1 accounting identities are imposed exactly; no residual may enter them
RB4  moment sets are disjoint across residual blocks
RB5  no two blocks may be algebraic complements inside one identity
RB6  the government block needs its own anchor or prior, a moment set disjoint from every labor
     wedge, and a dimension bounded by its declared form
RB7  the six-element forbidden set is not simultaneously unrestricted
RB8  the dimension-accounting table, the moment-assignment matrix and the absorption shares
     are reported; a missing report blocks interpretation claims
```

Violating any of `RB1`–`RB7` yields **`RESIDUAL_BUDGET_EXCEEDED__NOT_ADMISSIBLE`**, and the design is
**fail-closed**: no estimate, no `W_star` target, no comparison ranking and no claim may be reported
from it. The permitted responses are to resolve the missing source under Issue #83, to reduce
dimensionality by a declared prior or grouping, or to drop the affected regions/periods by the
declared exclusion rule — **never** to free a wedge.

```
NO-DOUBLE-RESIDUAL (frozen):
  the same unexplained variation may not be absorbed by two residual blocks; a labor-wedge moment
  may not also be assigned to the TFP or government block; the government block may not be the
  unbounded province-by-province balancing residual that closes output while labor wedges absorb the
  same moments; a residual introduced only because an identity fails to close is not a measurement
  wedge and is forbidden.
```

This is the architecture-level answer to the amendment §6 requirement that the labor-coverage,
hours, efficiency, migration, TFP and government-investment residual may not **all** remain
unrestricted.

## 8. Three-model comparison contract

| Element | `S0` `STRUCTURAL_ONLY` | `S1` `NAIVE_DATA_PROXY` | `S2` `LATENT_MEASUREMENT_ADJUSTED` |
|---|---|---|---|
| `W` source | backbone → masked softmax | observed proxy used as directly as source semantics allow | backbone jointly disciplined through `M1` and `WEDGE_RES` |
| `ell` source | declared macro/labor anchor basis, no proxy identity | `EMPLOYED_PERSONS_DECLARED_AS_PROXY` as the working `ell_used` | `M4` family with `omega`/`q_cov`; the proxy is one noisy anchor |
| active tiers | 2 (+1 imposed) | 1 (identities only) | 2–5 as declared |
| wedges active | none | none (declared assumptions instead) | tier 3 (+4/5 if anchored) |
| disciplines the latent states | macro moments | nothing — the proxy is the working object | `M1`–`M6` plus macro moments |
| residual budget | on the tier-2 structural parameters | trivially satisfied | fully binding |
| claim ceiling | may not claim to match observed OD | **benchmark only**, `NOT_PREFERRED_TRUTH`; may not claim structural interpretation | may claim joint latent discipline; may not claim observation of any latent object, nor global identification |
| labelled variant | — | `S1_VARIANT_SHARE_EQUIVALENCE__DECLARED_BENCHMARK` (choice C) | `ELL_PROXY_UNIT_INTENSITY_VARIANT` |

**Shared, identical across all three:** region universe `U1`–`U6` and the per-wave mappable
intersection; window-start information timing; macro-accounting definitions and the tier-1
identities; the `W`-support convention (diagonal false); row-conditional normalization and units;
the downstream HANK blocks when later coupled; the diagnostics set `D1`–`D10`; the wedge registry and
the budget rules.

**Rules `CMP1`–`CMP7`:** all admissible models are reported and an inadmissible model is reported with
its failing rule rather than replaced; no model is selected, preferred, tuned or dropped after
inspecting outcomes (`NO_OUTCOME_BASED_MODEL_SELECTION`); `S1` agreement is not validation of the
proxy and disagreement is not proof of the latent model; `S0` is not compared on observed-OD fit
alone; per-model moment consumption is declared so the comparison itself cannot create a double
residual; **no numeric acceptance threshold or ranking criterion beyond the frozen P3C values**; the
share-equivalence route is a labelled variant inside `S1` with its own row.

## 9. First-wave Owner choices (frozen)

| # | Choice (comment `5742312556`, amendment §8) | Frozen token |
|---|---|---|
| A | 2010 Census only | `FIRST_WAVE_2010_CENSUS_ONLY` |
| B | 2000 wave excluded initially | `WAVE_2000_EXCLUDED` |
| C | share-equivalence only as a declared benchmark/sensitivity variant | `SHARE_EQUIVALENCE__DECLARED_BENCHMARK_VARIANT` (inside `S1` only) |
| D | employed persons as a noisy proxy anchor for latent `ell_star` | `EMPLOYED_PERSONS_DECLARED_AS_PROXY` (M4b; `ELL_PROXY_IDENTITY_NOT_ASSUMED`) |
| E | canonical information set = window-start | `WINDOW_START_CANONICAL`; window-end nowcast **excluded** from the first pass |

These five were fixed before any outcome was observed and may not be revised after one. **None of
them resolves, promotes, weakens or pre-empts any H1–H7 item**: H1–H4 still require primary-source
human verification; H5 and H6 remain measurement/provenance questions and are not identity proofs
for `W_star` or `ell_star`; H7's source publication and reference timing still require verification
even though the design choice is window-start. Excluding the 2000 wave removes the P3B §1.5/§1.6
origin-coding ambiguity from the first wave without resolving it for any later wave.

## 10. Future diagnostics (defined now, not run)

| # | Diagnostic | Required in |
|---|---|---|
| `D1` | measurement residual by source and region, per family | `S2` |
| `D2` | coverage wedge magnitude (`q_cov`, and `q_si` if `M5` is active) | `S2` |
| `D3` | hours / efficiency decomposition sensitivity across declared variants | `S2` |
| `D4` | latent-versus-naive `W` difference, by pair and by origin | `S0`, `S1`, `S2` |
| `D5` | latent-versus-official `ell` difference on the declared `ell_unit` basis | `S0`, `S1`, `S2` |
| `D6` | output / capital / wage fit at the registered `M6` locations | `S0`, `S2` |
| `D7` | share of provincial output residual absorbed by each wedge/block | `S0`, `S2` |
| `D8` | government-residual crowding-out check: moment overlap with labor wedges and labor-wedge sensitivity with the block active vs inactive | `S0`, `S2` |
| `D9` | wedge dimension-accounting table with the `RB2` comparison | `S2` |
| `D10` | three-model comparison table on the common universe, timing and accounting | `S0`, `S1`, `S2` |

All ten are **mandatory** in any later execution report; a missing one is a reporting defect that
blocks interpretation claims (`RB8`). **No numeric acceptance threshold is attached to any
diagnostic here**; adding one requires a dated pre-execution Reviewer authorization.

## 11. Config consistency

The TOML mirror `configs/dlh_wl_p3e_latent_labor_measurement.toml` parses with the Python
standard-library `tomllib`: **27 top-level keys, 522 leaf values**, and it
contains the latent-object vocabulary with units and block membership; the accounting identities;
the backbone specification with its nine frozen properties; the seven measurement families
(`M1`, `M2`, `M3`, `M4a`, `M4b`, `M5`, `M6`); the seven wedge records plus the required-field list;
the identification rules `I1`–`I10`; the regularization forms; the residual budget `RB1`–`RB8` with
its fail-closed status; the moment-assignment rules; the dimension-accounting contract; the three
model blocks; the comparison rules; the five Owner choices; the ten diagnostics; the human-gate
block; the provenance-separation block; the 20 new invariants; and the prohibition flags.

**Inherited-threshold mirror.** The `[inherited_p3c]` block mirrors all sixteen Reviewer numeric
thresholds (plus the cosmetic-band upper bound) of `configs/dlh_wl_p3c_bridge_readiness.toml` and
asserts `values_inherited_unchanged = true`, `any_inherited_value_changed = false` and
`thresholds_restated_with_new_numbers = 0`. Each mirrored value was compared mechanically against the
P3C TOML and is **identical** (see §12).

**No new numeric constant of any kind.** Every floating-point literal in the P3E TOML belongs to the
inherited P3C set; the only other numbers are structural counts, tier indices, the Issue and comment
identifiers and boolean flags. This is verified mechanically in §12.

## 12. Consistency checks performed

Only the Issue #84 §13 classes were used: symbolic/static reasoning, config parse, cross-document
consistency and dimension/unit checks. **282 checks, 282 PASS / 0 FAIL.**

- **config parse** — the TOML parses; leaf and key counts reported above; no `null`, no orphan table,
  no duplicated key.
- **inherited-threshold identity** — all sixteen P3C thresholds plus the band upper bound are
  byte-identical in value between the P3E mirror and the P3C TOML; `new_numeric_thresholds_introduced
  = 0` and the P3E float-literal set is exactly the inherited P3C float set.
- **cross-document token consistency** — the six latent objects, the derived `omega`, the seven
  measurement families, the seven wedges, the identification rules `I1`–`I10`, the budget rules
  `RB1`–`RB8`, the comparison rules `CMP1`–`CMP7`, the Owner tokens, the ten diagnostics, the
  invariants `E1`–`E20` and the prohibitions all appear, with identical names and statuses, in the
  architecture document, the matrix document and the TOML.
- **dimension/unit check** — the unit algebra was verified symbolically: `persons · (hours/person) ·
  (units/hour) = units`; `ell_star · P` is dimensionally equal to `F`; `omega = h·e` is units/person
  and `omega · N_workers_star = ell_star` exactly; each measurement-equation left- and right-hand side
  carries the same unit, including the proxy route and the coverage channel; `s_ij,t` is dimensionless
  term by term. The check also enforces the `U-5` period-label rule: the accounting period is a label,
  not a unit factor, so no quantity carries a spurious period dimension and no measurement equation
  needs an undeclared conversion factor.
- **no-identity check** — the strings asserting `W_model = W_census` and `ell_model = ell_official`
  appear only inside statements that they are forbidden; `ell_star ≠ N_obs` unless `q_cov = 1` and
  `omega = 1`, which is declared never assumed.
- **no-empirical-value check** — the numeric-token inventory of all four artifacts contains no
  coverage factor, undercoverage rate, informal share, hours, efficiency, wage, output, capital or
  government value; the only real-valued tokens are the inherited P3C thresholds and the declared
  band bound.
- **wedge-record completeness** — each of the seven registered wedges carries all eight required
  fields, and every wedge declares `may_be_free_without_anchor_or_prior = false` and
  `fail_closed_when_h_unresolved = true`.
- **residual-budget closure** — `RB1`–`RB8` are present with a named failure status and
  `failure_is_fail_closed = true`; the six-element forbidden set and the no-double-residual statement
  are present; the permitted responses list excludes freeing a wedge.
- **human-gate integrity** — H1–H7 are listed, all `UNRESOLVED`, `builder_may_resolve_or_promote =
  false`, `self_promotion_allowed = false`, and no artifact claims an H resolution or an evidence
  promotion.
- **allowlist discipline** — the changed/added path set is exactly the four allowlisted paths, and no
  pre-existing artifact is modified (all four are new files of this Issue).

No real matrix was executed by any of these checks, no measurement equation was evaluated, and no
source file was ingested.

## 13. Prohibited-action accounting (all zero)

| Item | Count |
|---|---|
| real population / employment / census / survey sources read or opened | **0** |
| datasets downloaded, scraped, purchased, ingested or opened | **0** |
| external metadata queries issued | **0** |
| real transition matrices inspected or executed | **0** |
| measurement equations evaluated on any data | **0** |
| bridges implemented or executed; empirical adapters | **0** |
| fits, estimates, trainings, calibrations | **0** |
| social-insurance undercoverage calibrations | **0** |
| labor-law non-compliance calibrations | **0** |
| informal-employment shares assumed | **0** |
| new government-investment residuals introduced | **0** |
| HJB / KFE / GE / MATLAB / household calls | **0** |
| `pytest` / full-suite runs | **0** |
| evidence levels promoted | **0** |
| H1–H7 items resolved or promoted by DSH | **0** |
| new numeric thresholds introduced | **0** |
| inherited numeric values changed | **0** |
| numeric empirical values emitted | **0** |
| source code, tests, CURRENT governance, P3C or P3D artifacts touched | **0** |
| PRs, merges, closes, successors or self-acceptances | **0** |

## 14. Exact changed paths (4 — exactly the Issue #84 allowlist)

```
docs/specifications/DLH_WL_P3E_LATENT_LABOR_MEASUREMENT_ARCHITECTURE_2026_09_19.md
docs/data/DLH_WL_P3E_MEASUREMENT_AND_IDENTIFICATION_MATRIX_2026_09_19.md
configs/dlh_wl_p3e_latent_labor_measurement.toml
reports/dlh_wl_p3e_2026_09_19/DLH_WL_P3E_REPORT.md
```

Nothing else was created or modified: no source code, no tests, no CURRENT governance document, no
P3C artifact, no P3D artifact, no issue pointer.

Artifact identity (LF-normalised SHA-256):

```
architecture specification  539FD83DB9DE0A7B4EF781BEFBA7AB142A28D23ED3C597C2B01CFD51985828E6
measurement matrix          3C863EDD052E18B3691A92A73F175888A66232695B818181D63AD69C93AFF6E8
readiness config (TOML)     AE32C2734EECE82244AE0DE711586A5C7686592DC46A7C4092E536EDF88F417C
report                      7E97D8EED0157B13B4C5D4942D5728B9CD30C89E794121BBCB6B81E57529E129
```

The `report` value is the LF SHA-256 of this report **with its own identity line removed**, so the
value is reproducible from the committed artifact instead of being self-referential; the other three
values are the plain LF SHA-256 of the named files as committed.

## 15. Interpretation ceiling

Allowed by this Issue: the frozen architecture; the statement that the latent objects, units,
backbone, measurement families, wedge records, residual budget and comparison contract are defined;
the statement that no measurement equation is an identity; the statement that the H1–H7 packet is
complete and entirely unresolved; and the statement that no execution is authorized.

Explicitly **not** claimed: that any source exists, is available, is licensed or is accessible; that
any source's semantics, schema, codes, weights or timings have been verified; that any latent object
is observed, measured, identified or estimated; that any coverage factor, undercoverage rate,
informal share or wedge magnitude has a value; that `ell_star` or `W_star` equals any observation;
that the `h_star`/`e_star` split is identified; that any model in the comparison is superior; that
any empirical, causal, welfare, policy, GE, HJB/KFE or household result is available; that any
production function, government rule or market structure is specified; and that any H item is
resolved.

## 16. What happens next, and what does not

This Issue authorizes **nothing executable**. The next authority in the route is the **human/Owner
gate of Issue #83**: only a human decision token per H item, with primary-source provenance, can
unblock a measurement family. After the items a given wave needs are resolved — and only under a
separately authorized Issue — the architecture frozen here can support a bounded source adapter and
a first `S0`/`S1`/`S2` comparison on the 2010 wave, under the same residual budget, the same wedge
records and the same claim ceilings. No successor Issue is created here.

## 17. Terminal

```
DLH_WL_P3E_LATENT_LABOR_MEASUREMENT_ARCHITECTURE__PASS__READY_FOR_POST_E3_IMPLEMENTATION
```
