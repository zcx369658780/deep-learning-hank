# DLH-WL-P3E — measurement and identification matrix

Issue: **#84 / `DLH-WL-P3E`**. Owner route: `DLH-WL-V1-20260918` plus the dated amendment
`docs/decisions/DLH_OWNER_ROUTE_AMENDMENT_LATENT_LABOR_MEASUREMENT_2026_09_19.md`.
Authority marker: `DLH_WL_P3E_LATENT_LABOR_MEASUREMENT_ARCHITECTURE_AUTHORIZED`.
Reviewer final activation comment: **`5742332586`**. Operative baseline:
`2f4bd66343ed8ae8a95e36316d2730084bd24e52`.

Status: **matrix/registry only — docs/config only.** No source, dataset, table, codebook or licence
text was opened; no statistic was inspected; no equation was evaluated. Scientific / model /
training / empirical-bridge calls = **0**. No numeric coverage, undercoverage, informal-share,
hours, efficiency or wedge value appears anywhere in this document; every row is a declaration, a
requirement or a status token.

Companion to `docs/specifications/DLH_WL_P3E_LATENT_LABOR_MEASUREMENT_ARCHITECTURE_2026_09_19.md`
(the architecture), `configs/dlh_wl_p3e_latent_labor_measurement.toml` (the machine-readable
mirror) and `reports/dlh_wl_p3e_2026_09_19/DLH_WL_P3E_REPORT.md` (report and terminal).

---

## 1. How to read this document

The architecture document states the objects, the backbone, the measurement families and the rules.
This document is the **matrix layer**: it records, in tabular form, which observation can discipline
which latent object, which wedge sits in which equation, which moment may be claimed by which
residual block, what dimension accounting a design must report, and what remains blocked by the
human gate of Issue #83.

Every table is a **declaration**, not a result. Columns named *status* carry the closed status
vocabulary of the architecture document §2.4 and §5; columns named *blocked by* name the H items
whose resolution is a precondition, and all seven H items are `UNRESOLVED` in this Issue.

## 2. Latent object ↔ observation matrix

| Latent object | Symbol | Directly observed? | Observation(s) that may enter a measurement equation | Which latent object the observation actually measures | Status now | Blocked by |
|---|---|---|---|---|---|---|
| destination share of labor services | `W_star_ij,t` | **no** | none directly; `T_obs^(k)` measures a *person-based residence* object, and the labor-service sharing is reached only through the P3B T-family bridge and the `lambda` / H5 route | `W_star` is the V1 learning object and the structural output of §4; no observation is a measurement of it | `STRUCTURALLY_DEFINED_NOT_OBSERVED` | H1, H3, H5 |
| outflow share / intensity | `m_star_i,t` | **no** | M-A/M-B/M-C derivations of the P3B contract §2 remain the only admissible routes; `m` is never a feature and never a label | `m_star` is a given accounting input; its derivation is assumption-dependent (P3B warning) | `LATENT__BLOCKED_BY_H` | H1, H3 |
| effective origin labor | `ell_star_i,t` | **no** | M4a direct efficiency-labor source; M4b declared proxy basis (`EMPLOYED_PERSONS_DECLARED_AS_PROXY`) jointly with `omega` and `q_cov` | M4b measures **worker quantity**, not `ell_star`; the anchor acts on `ell_star` only through `omega = h_star·e_star` | `LATENT__BLOCKED_BY_H` | H6, (H5 for `lambda`) |
| worker quantity | `N_workers_star_i,t` | **no** | M2 (`L_obs_i,t`) | employment counts with a source-specific coverage factor `q_cov_i,t` | `LATENT__BLOCKED_BY_H` | H2, H4 |
| hours / intensity | `h_star_i,t` | **no** | M3 (`H_obs_i,t`) if a source exists | hours measures the hours margin; worker counts cannot identify it | `LATENT__NOT_SEPARATELY_IDENTIFIED` absent an M3 source | H2, H4 |
| efficiency per hour | `e_star_i,t` | **no** | M4 (`ELL_obs` / `q_eff`) | the `h`/`e` split is unidentified under worker-count-only or hours-only sources | `LATENT__NOT_SEPARATELY_IDENTIFIED` absent an M4 source | H6 |
| intensity-efficiency content per worker | `omega_i,t = h_star_i,t · e_star_i,t` | **no** | product of M3 and M4 objects; otherwise prior-regularized | this is the only route by which a worker count anchors `ell_star` | `LATENT__PRIOR_REGULARIZED` | H2, H4, H6 |
| covered / uncovered worker split | `N_cov_star_i,t`, `N_unc_star_i,t` | **no** | M5 (`COV_obs_i,t`) **if** a source supports it | institutional coverage of a specific channel; never total employment, never an undercoverage rate | `MEASUREMENT_CHANNEL_DECLARED_NOT_CALIBRATED` | H2, H4 |
| productivity object | `A_i,t` | **no** | M6 registered locations (output, capital, wage) | registered tier-4 residual block; functional form not specified in this Issue | `LATENT__PRIOR_REGULARIZED` | H2, H7 |
| government block | `G_i,t` | **no** | M6 registered location (`G_obs_i,t`) | registered tier-5 block with its own anchor/prior and a moment set disjoint from the labour wedges | `LATENT__PRIOR_REGULARIZED` | H2, H7 |

**Frozen reading rule.** No row of this table permits an equality between the observation and the
latent object. `W_model = W_census` and `ell_model = ell_official` remain forbidden as assumptions
(invariant `E1`); an equality requires a separately accepted source-specific measurement contract.

## 3. Measurement-equation matrix

| ID | Observed object | Latent target | Equation (symbolic) | Active wedge | Error treatment | Required declarations | Status | Blocked by | Claim ceiling |
|---|---|---|---|---|---|---|---|---|---|
| `M1` | `T_obs^(k)_ij,t` (person-based k-year residence transition share) | `Pp^(k)_ij,t` (latent **person-based** k-step residence transition) | `T_obs^(k)_ij,t = (1 − kappa_res_t)·Pp^(k)_ij,t·1{j ∈ frame} + zeta_res_ij,t + eps_res_ij,t` | `WEDGE_RES` (`kappa_res`) | declared moment condition or likelihood; `zeta_res` carries frame/timing terms and the reported unclassified bucket `a_res_i,t` | frame, universe, reference window `(t−k, t]`, orientation, diagonal, weights, missing/unknown categories, reference date, vintage (H1/H3) | `NO_SOURCE_VERIFIED__BLOCKED_BY_H1_H3` | H1, H3 | the object measures people-based multi-year **residence** transitions; it does not measure `W_star` and never equals it |
| `M2` | `L_obs_i,t` (employed persons / labor force / unit employment) | `N_workers_star_i,t` | `L_obs_i,t = q_cov_i,t·N_workers_star_i,t + eps_L_i,t` | `WEDGE_COV` (`q_cov`) | declared moment condition or likelihood | source frame, institutional basis, unit (persons/jobs/posts), region universe, reference period, weighting status | `NO_SOURCE_VERIFIED__BLOCKED_BY_H2_H4` | H2, H4 | a partial observation of worker quantity, never of `ell_star`; `q_cov` is never set numerically here |
| `M3` | `H_obs_i,t` (hours / intensity) | `h_star_i,t` (through `N_workers_star·h_star`) | `H_obs_i,t = q_hours_i,t·(N_workers_star_i,t·h_star_i,t) + eps_H_i,t`; if absent, `h_star` is carried by a declared `L_*` form | `WEDGE_HOURS` (`q_hours`) | declared | source basis, whether the measure is per worker or per job, reference period | `NO_SOURCE_VERIFIED__BLOCKED_BY_H2_H4`, or `LATENT__PRIOR_REGULARIZED` if absent | H2, H4 | a partial hours-margin observation; cannot be obtained from worker counts |
| `M4a` | `ELL_obs_i,t` (efficiency labor, direct basis) | `ell_star_i,t` | `ELL_obs_i,t = q_eff_i,t·ell_star_i,t + eps_eff_i,t` | `WEDGE_EFF` (`q_eff`) | declared | `ell_unit = EFFICIENCY_LABOR`; unit with hours/efficiency content stated; timing preceding or coinciding with the decision (P3B E4); coverage versus the label universe; `C-LINK` status | `NO_SOURCE_VERIFIED__BLOCKED_BY_H6` | H6 | a partial efficiency-labor observation |
| `M4b` | `N_obs_i,t` (employed-persons proxy) | `ell_star_i,t` **jointly** with `N_workers_star_i,t` and `omega_i,t` | `N_obs_i,t = q_cov_i,t·N_workers_star_i,t + eps_L_i,t` and `ell_star_i,t = omega_i,t·N_workers_star_i,t`, `omega := h_star·e_star` | `WEDGE_COV` + `WEDGE_OMEGA` | declared | `ell_unit = EMPLOYED_PERSONS_DECLARED_AS_PROXY`; explicit proxy status; sensitivity replicate; `ELL_PROXY_IDENTITY_NOT_ASSUMED` | `NO_SOURCE_VERIFIED__BLOCKED_BY_H6` | H6 | a **noisy anchor** for `ell_star`; `ell_star ≠ N_obs` unless `q_cov = 1` **and** `omega = 1`, which is never assumed (only the declared variant `ELL_PROXY_UNIT_INTENSITY_VARIANT`) |
| `M5` | `COV_obs_i,t` (covered-employment channel: social insurance, unit employment, equivalent) | `N_cov_star_i,t` in `N_workers_star = N_cov_star + N_unc_star` | `COV_obs_i,t = q_si_i,t·N_cov_star_i,t + eps_cov_i,t` | registry entry `WEDGE_SI_COVERAGE` (channel, not a calibrated wedge) | declared | channel identity, institutional coverage basis, region universe, period; **no numeric `q_si`**; enrollment ≠ total employment; informal share not assumed | `MEASUREMENT_CHANNEL_DECLARED_NOT_CALIBRATED` | H2, H4 | a declared channel for a coverage split; it is not a measured undercoverage rate |
| `M6` | `Y_obs_i,t`, `K_obs_i,t`, `w_obs_i,t`, `G_obs_i,t` | `A_i,t`, `K_star_i,t`, `ell_star_i,t`, `G_i,t` (registered locations) | registered only; no functional form chosen in this Issue | `WEDGE_TFP`, `WEDGE_GOV` | declared later | functional form, capital accumulation, market structure and government rule are **later-Issue** objects | `REGISTERED_NOT_SPECIFIED_IN_THIS_ISSUE` | H2, H7 | registered locations for the moment side of the residual budget; no quantitative claim may be made from them here |

### 3.1 Timing and leakage column (frozen for every family)

| Family | Observation reference window | Permitted as a feature? | Permitted as a label/measurement target? |
|---|---|---|---|
| `M1` | `(t−k, t]`, must satisfy the H1/H7 declarations | **no** | it is a measurement object; it is never treated as truth for `W_star` |
| `M2` | must precede or coincide with the destination decision | **no** for `N_workers_star` as a same-period object; window-start values only if declared available | measurement only |
| `M3` | same rule as `M2` | window-start only if declared | measurement only |
| `M4a`/`M4b` | must precede or coincide (P3B E4) | window-start only if declared | measurement only |
| `M5` | same rule as `M2` | window-start only if declared | measurement channel only |
| `M6` | declared per location | window-start only if declared | measurement/anchor only |

`m_star` and `ell_star` are **never** features and **never** the label of the conditional-share
learner (`E15`, P3B `L2`); a measurement layer around them does not change that.

## 4. Wedge identification matrix (the eight-field records)

Every wedge below carries all eight fields required by the architecture §6.1. A wedge that reaches an
equation without them is `WEDGE_RECORD_INCOMPLETE__NOT_ADMISSIBLE`.

### 4.1 `WEDGE_RES` — migration / residence wedge

```
1 symbol                    kappa_res_t                      (dimensionless)
2 equation location         M1
3 economic interpretation   residence classification, timing and multi-year aggregation
                            discrepancy between the observed residence object and the latent
                            person-based k-step transition — a measurement discrepancy, NOT an
                            economic migration cost
4 disciplining source       H1/H3 source semantics, resolved by documentation; NOT by fitting
5 allowed dimensionality    wave-level and source-level scalars; a declared semantic variant;
                            NEVER a per-pair or per-origin free residual
6 prior / regularization    when H1 resolves the mapping, kappa_res_t takes the resolved value;
                            otherwise a declared L_* form with a stated prior
7 sensitivity requirement   residence-semantics variant replicate
8 claim ceiling             a measurement discrepancy; never a migration barrier, cost or friction
```

### 4.2 `WEDGE_COV` — employment-coverage wedge

```
1 symbol                    q_cov_i,t                        (dimensionless)
2 equation location         M2 (and M4b)
3 economic interpretation   the institutional frame of an employment count relative to the latent
                            worker universe (registration, establishment, payroll, survey frame)
4 disciplining source       M5 channel if a source supports it; otherwise the macro employment
                            accounting identity; never an assumption
5 allowed dimensionality    declared L_* form; a per-region-per-period free vector is FORBIDDEN
                            without an anchor, prior or grouping
6 prior / regularization    declared prior with a reported sensitivity
7 sensitivity requirement   anchored versus prior-only replicate
8 claim ceiling             coverage of a specific source; never a labour-supply distortion,
                            never an undercoverage rate for the economy
```

### 4.3 `WEDGE_HOURS` — hours wedge

```
1 symbol                    q_hours_i,t                      (dimensionless)
2 equation location         M3
3 economic interpretation   the reporting basis of an hours/intensity measure (per worker vs per
                            job, paid vs actual, reference period)
4 disciplining source       the M3 source if it exists; otherwise a declared prior
5 allowed dimensionality    declared L_* form
6 prior / regularization    required prior; h_star may not be free per region
7 sensitivity requirement   prior-scaled replicate
8 claim ceiling             a measurement basis; never a leisure or labour-supply preference
```

### 4.4 `WEDGE_EFF` — efficiency wedge

```
1 symbol                    q_eff_i,t                        (dimensionless)
2 equation location         M4a
3 economic interpretation   efficiency-labor content discrepancy of a source relative to the
                            latent effective labor object
4 disciplining source       the M4a source if it exists; otherwise a declared prior
5 allowed dimensionality    declared L_* form
6 prior / regularization    required prior, jointly with the h/e split status
7 sensitivity requirement   split-sensitivity replicate (with WEDGE_OMEGA)
8 claim ceiling             a measurement basis; never a technology or human-capital claim
```

### 4.5 `WEDGE_OMEGA` — intensity-efficiency content per worker

```
1 symbol                    omega_i,t = h_star_i,t * e_star_i,t      (eff-labor units / person)
2 equation location         M4b
3 economic interpretation   effective labor carried by one worker — the only route by which a
                            worker count can anchor ell_star
4 disciplining source       M3 and M4a jointly if both exist; else the declared prior
5 allowed dimensionality    declared L_* form; free per region is FORBIDDEN
6 prior / regularization    required, with the functional form declared
7 sensitivity requirement   ELL_PROXY_UNIT_INTENSITY_VARIANT (omega == 1) reported as its own row
8 claim ceiling             a decomposition; never an identified productivity level
```

### 4.6 `WEDGE_TFP` — productivity residual (tier 4)

```
1 symbol                    A_i,t                            (declared output-per-input unit)
2 equation location         M6 registered production location
3 economic interpretation   total-factor-productivity / productivity object of the registered
                            production mapping
4 disciplining source       declared macro moments: output, capital, wage
5 allowed dimensionality    declared low-dimensional form (aggregate or sector)
6 prior / regularization    required
7 sensitivity requirement   productivity-prior replicate
8 claim ceiling             a registered productivity object; never an identified causal effect
```

### 4.7 `WEDGE_GOV` — government-investment / output residual (tier 5)

```
1 symbol                    G_i,t                            (declared output unit)
2 equation location         M6 registered government location
3 economic interpretation   an explicit government-investment / government-output economic block
4 disciplining source       its OWN declared anchor G_obs_i,t or a declared prior, PLUS a moment
                            set disjoint from every labour wedge
5 allowed dimensionality    bounded by its declared low-dimensional form; an unbounded
                            province-by-province free form is FORBIDDEN
6 prior / regularization    anchor or prior required
7 sensitivity requirement   anchor-relaxation replicate
8 claim ceiling             an economic block with its own moments; NEVER a provincial balancing
                            residual that closes output
```

### 4.8 Wedge activation matrix

| Wedge | Tier | Active in `S0` | Active in `S1` | Active in `S2` | May be free without anchor/prior? | Fails closed when its H source is unresolved |
|---|---|---|---|---|---|---|
| `WEDGE_RES` | 3 | no | no (semantics are used as declared assumptions, not as a wedge) | yes | no | yes (`I6`) |
| `WEDGE_COV` | 3 | no | no (proxy used as-is, declared) | yes | no | yes |
| `WEDGE_HOURS` | 3 | no | no | yes | no | yes |
| `WEDGE_EFF` | 3 | no | no | yes | no | yes |
| `WEDGE_OMEGA` | 3 | no | no (unit intensity assumed only in the labelled variant) | yes | no | yes |
| `WEDGE_TFP` | 4 | no | no | only if registered and anchored | no | yes |
| `WEDGE_GOV` | 5 | no | no | only if anchored, bounded and moment-disjoint | no | yes |

`S0` activates tier 2 only; `S1` uses observations as declared proxies without measurement wedges,
which is precisely why it is a benchmark and not a measurement model; `S2` is the only model in which
the tier-3 wedges and the residual budget `RB1`–`RB8` become binding.

## 5. Moment-assignment matrix

### 5.1 Moment families

| Moment family | Examples of its members (symbolic) | Tier that may claim it |
|---|---|---|
| accounting identities | row normalization, `W` diagonal false, `F = ell·m·W` | tier 1 — **imposed, not fitted; no block may claim them** |
| mobility moments | residence-transition cells, aggregate outflow shares, support/zero patterns | tier 3 `WEDGE_RES` (via M1), or tier 2 structure |
| employment moments | employed persons, labor force, unit-employment counts | tier 3 `WEDGE_COV` (via M2) |
| hours moments | hours, intensity, working-time measures | tier 3 `WEDGE_HOURS` (via M3) |
| efficiency-labor moments | efficiency-labor quantities, wage-bill/labor-compensation equivalents | tier 3 `WEDGE_EFF` / `WEDGE_OMEGA` (via M4) |
| coverage-channel moments | social-insurance enrollment, unit-employment channel totals | M5 channel, which disciplines `q_cov` **once** per design (see §5.3) |
| output / capital / wage moments | output, capital stock, wage measures | tier 4 `WEDGE_TFP` (via M6) |
| government moments | government-investment / government-output measures | tier 5 `WEDGE_GOV` (via M6), disjoint from every labour moment |

### 5.2 Assignment rules

| # | Rule |
|---|---|
| MA1 | moment sets are declared before execution and are **disjoint** across residual blocks (`RB4`) |
| MA2 | a moment may not be claimed by two blocks; if a design wishes to use one observation in two places, the design must declare the restriction that makes the two uses non-redundant, or drop one use |
| MA3 | identity moments (tier 1) are never "claimed": the identities are imposed, so no block may be credited with them |
| MA4 | an M5 coverage moment may discipline `q_cov` **or** the coverage split, not both at full strength; the choice is declared and the other side is prior-carried |
| MA5 | the government block's moment set must be disjoint from every labour-moment family (`RB6`, `D8`) |
| MA6 | the moment inventory, the block inventory and the disjointness check are reported in the dimension-accounting table (`D9`) |

### 5.3 Empty / absent moment families (frozen dispositions)

| Situation | Required disposition |
|---|---|
| no verified M5 source | `q_cov` is not calibrated from a coverage channel; it must be prior-carried or grouped (`I6`) |
| no verified M3 source | `h_star` prior-carried; the `h`/`e` split is `LATENT__NOT_SEPARATELY_IDENTIFIED` |
| no verified M4 source | `omega` prior-carried; the proxy route anchors `ell_star` only weakly, and this must be stated in the claim ceiling |
| no verified M1 source | `S2` loses its mobility anchor; `WEDGE_RES` may not be freed to compensate; the design reports the difference against `S0` |
| no verified M6 anchor for the government block | the government block is **inactive**; it may not be activated as a free residual (`RB6`) |

### 5.4 Budget-rule cross-reference (`RB1`–`RB8`) and the `NO_DOUBLE_RESIDUAL_RULE`

| Rule | What it constrains in matrix terms | Where it bites in this document |
|---|---|---|
| `RB1` | every free residual block must appear in the moment-assignment table with a non-empty `M_r` | §5.1, §5.2 `MA1` |
| `RB2` | for every row of the dimension-accounting table, free directions `d_r` may not exceed the assigned moment count | §6 |
| `RB3` | no parameter of any tier-3/4/5 block may be listed as entering an accounting identity | §2.2-adjacent identity rows, §5.1 tier-1 row |
| `RB4` | the disjointness column of the moment-assignment and dimension tables must be clean for every pair of blocks | §5.2 `MA1`/`MA2`, §6 disjointness column |
| `RB5` | no two registered blocks may be defined as complements of one another inside one identity | §5.1, §5.2 `MA2` |
| `RB6` | the government block row must carry its own anchor or prior and a moment set disjoint from every labour-moment family | §5.2 `MA5`, §5.3 government row, §6 `WEDGE_GOV` row |
| `RB7` | the six-element forbidden set must not all be unrestricted: at least the tier-3 wedges satisfy `RB1`–`RB2` and at least one tier-4/5 block is anchored or inactive | §4.8 activation matrix, §5.3 absent-family dispositions, §6 |
| `RB8` | the design must publish `D9`, the moment-assignment matrix and the `D7` absorption shares | §6, §10 `D7`/`D9` |

`NO_DOUBLE_RESIDUAL_RULE` is the machine-readable identifier of the statement that the same
unexplained variation may not be absorbed by two residual blocks; it is recorded here, in the
architecture §7.3 and in the config, and its three limbs are: a labour-wedge moment may not also be
assigned to the TFP or government block; the government block may not be an unbounded
province-by-province balancing residual; a residual introduced only because an identity fails to close
is forbidden.

## 6. Dimension-accounting table (required report, diagnostic `D9`)

Every later design must publish this table. It contains **no numeric threshold**: it is a count of
declared free directions against declared assigned moments, and it is the mechanical form of `RB2`.

| Block | Tier | Declared form (`L_*`) | Free-parameter count `d_r` (declared structure) | Assigned moment count `|M_r|` | `RB2` satisfied? | Disjointness checked against |
|---|---|---|---|---|---|
| `WEDGE_RES` | 3 | declared | declared | declared | required | all other blocks |
| `WEDGE_COV` | 3 | declared | declared | declared | required | `WEDGE_SI_COVERAGE`, `WEDGE_OMEGA` |
| `WEDGE_HOURS` | 3 | declared | declared | declared | required | `WEDGE_EFF`, `WEDGE_OMEGA` |
| `WEDGE_EFF` | 3 | declared | declared | declared | required | `WEDGE_HOURS`, `WEDGE_OMEGA` |
| `WEDGE_OMEGA` | 3 | declared | declared | declared | required | `WEDGE_HOURS`, `WEDGE_EFF` |
| `WEDGE_TFP` | 4 | declared | declared | declared | required | `WEDGE_GOV` and all tier-3 blocks |
| `WEDGE_GOV` | 5 | declared | declared | declared | required | every labour block (`RB6`) |
| structural `beta` | 2 | §4 backbone | declared | mobility and macro moments | required | tier-3/4/5 blocks |

A design whose table violates `RB2` for any row, or whose disjointness check fails, is
`RESIDUAL_BUDGET_EXCEEDED__NOT_ADMISSIBLE`, and no estimate or comparison ranking may be reported
from it.

## 7. Regularization-form matrix

| Form | Expression | Free-parameter structure | Admissible for | Not admissible for |
|---|---|---|---|---|
| `L_constant` | `wedge_i,t = wedge_bar` | one direction | any wedge as a last-resort prior form | wedges whose claimed interpretation is source-specific per region |
| `L_time` | `wedge_i,t = wedge_bar_t` | one per period | source-frame changes over time | absorbing region heterogeneity |
| `L_factor` | `log wedge_i,t = log wedge_bar_t + gamma' X_i` | declared low-dimensional `gamma` | `q_cov`, `q_hours`, `q_eff`, `omega` | any form whose `X_i` includes a post-decision measurement |
| `L_anchored` | pinned by a declared anchor where covered, declared form elsewhere | anchor cells + declared remainder | `q_cov` with M5, `G` with `G_obs` | `WEDGE_RES`, which is disciplined by documentation, not by fit |
| `L_grouped` | `wedge_i,t = wedge_g(i)` with a declared partition | one per declared group | any tier-3 wedge | partitions chosen after seeing outcomes (`C17`) |

Frozen properties: the form is chosen before execution; the `X_i`/partition declarations are part of
the design; changing a form or a partition after outcomes is a design violation; a form's free count
enters the `D9` table and the `RB2` comparison.

### 7.1 Identification-rule cross-reference (`I1`–`I10`)

| Rule | What it constrains in matrix terms | Where it bites in this document |
|---|---|---|
| `I1` | each of the seven wedge records in §4 must be complete before the wedge is named by an equation row of §3 | §3 active-wedge column, §4.1–§4.7 |
| `I2` | every wedge row must name a form from §7 and a declared free-parameter structure | §4.1–§4.7, §7 |
| `I3` | no wedge row may declare an anchor-free region × period span | §4.8, §7 |
| `I4` | the `h`/`e` split rows may not both be free; `WEDGE_OMEGA` carries the product | §2 (`h_star`, `e_star` rows), §4.5 |
| `I5` | the six registered wedges of the forbidden set may not all be unrestricted | §4.8 activation matrix |
| `I6` | an H-blocked wedge row is prior-carried or its dimension set is excluded, never freed | §5.3, §11 |
| `I7` | no wedge row may be justified by provincial output closure alone | §4.6, §4.7, §5.1 output-moment row |
| `I8` | no wedge row may be reported as data-identified without a source-specific contract | §4.1–§4.7 claim-ceiling fields |
| `I9` | every active wedge row names its sensitivity replicate | §4.1–§4.7 sensitivity fields, §10 |
| `I10` | any violation makes the design `RESIDUAL_BUDGET_EXCEEDED__NOT_ADMISSIBLE` | §5.4, §6 |

### 7.2 Unit discipline in matrix terms

The dimension algebra of the architecture §3 is what makes the matrix rows comparable: `h_star` is
hours/person, `e_star` is efficiency-labor units/hour, `N_workers_star` is persons, `ell_star` and
`ELL_obs` and `F` are efficiency-labor units, `omega` is efficiency-labor units/person, and the
accounting period is a **label** rather than a dimension (`U-5`). Consequently
`N_workers_star · h_star · e_star = ell_star`, `omega · N_workers_star = ell_star` and
`ell_star · P = F` hold exactly as dimensions, so no row of §3 mixes incompatible scales and no
row of §5 needs an undeclared conversion factor.

## 8. Identification-status matrix per latent object

| Object | Status now | What would upgrade it to `LATENT__MEASUREMENT_DISCIPLINED` | Authority required | Builder may upgrade? |
|---|---|---|---|---|
| `W_star_ij,t` | `STRUCTURALLY_DEFINED_NOT_OBSERVED` | not upgradable by measurement: no source measures the labor-service conditional share; it stays a structural/search object | none | **no** |
| `m_star_i,t` | `LATENT__BLOCKED_BY_H` | a resolved M-A derivation with H1/H3 semantics and a declared `m_provenance_id`, `m_unit_basis`, alignment | Issue #83 human gate | **no** |
| `ell_star_i,t` | `LATENT__BLOCKED_BY_H` | H6 resolution plus M4a or the M4b proxy route with declared `omega`/`q_cov` | Issue #83 human gate | **no** |
| `N_workers_star_i,t` | `LATENT__BLOCKED_BY_H` | H2/H4 resolution and an M2 source with declared coverage basis | Issue #83 human gate | **no** |
| `h_star_i,t` | `LATENT__NOT_SEPARATELY_IDENTIFIED` | an M3 source whose basis separates hours from worker counts | Issue #83 human gate | **no** |
| `e_star_i,t` | `LATENT__NOT_SEPARATELY_IDENTIFIED` | an M4 source separating efficiency from hours | Issue #83 human gate | **no** |
| `omega_i,t` | `LATENT__PRIOR_REGULARIZED` | nothing directly; it may become measurement-informed via M3+M4 | Issue #83 human gate | **no** |
| `A_i,t`, `G_i,t` | `LATENT__PRIOR_REGULARIZED` | a registered and anchored M6 specification in a later Issue | later Reviewer authorization | **no** |

The `Builder may upgrade?` column is uniformly **no**: an evidence-level or status upgrade is a
human/Owner act (invariant `E11`).

## 9. Three-model comparison matrix

| Element | `S0` `STRUCTURAL_ONLY` | `S1` `NAIVE_DATA_PROXY` | `S2` `LATENT_MEASUREMENT_ADJUSTED` |
|---|---|---|---|
| region universe | `U1`–`U6` intersection | identical | identical |
| information timing | window-start canonical | identical | identical |
| macro-accounting definitions | tier-1 identities of the architecture §2.2 | identical | identical |
| downstream HANK blocks | frozen household dependency, unchanged | identical | identical |
| `W` source | §4 backbone → masked softmax | observed proxy used as directly as source semantics allow (`W_used = W_obs`) | backbone jointly disciplined by `M1` through `WEDGE_RES` |
| `ell` source | declared macro/labor anchor basis; no proxy identity | `EMPLOYED_PERSONS_DECLARED_AS_PROXY` used as the working `ell_used`, with explicit proxy status | `M4` family with `omega`/`q_cov`; the proxy is one noisy anchor among several |
| active tiers | 2 (+1 imposed) | 1 (identities) | 2–5 as declared |
| measurement wedges active | none | none (declared assumptions instead) | tier 3 (+4/5 if anchored) |
| what disciplines the latent states | macro moments | nothing — the proxy is taken as the working object | measurement equations `M1`–`M6` plus macro moments |
| residual budget `RB1`–`RB8` | applies to the few tier-2 structural parameters | applies trivially (no free residuals) | fully binding |
| admissibility condition | declared support and timing | declared source semantics and `NOT_PREFERRED_TRUTH` | `RB1`–`RB8` satisfied |
| comparison role | structural benchmark | naive benchmark | measurement-adjusted model |
| minimum claim ceiling | may not claim to match observed OD | may not claim structural interpretation, and may not claim the proxy equals the latent object | may claim joint latent discipline; may not claim observation of any latent object, nor global identification |
| labelled variant | — | `S1_VARIANT_SHARE_EQUIVALENCE__DECLARED_BENCHMARK` (Owner choice C) | `ELL_PROXY_UNIT_INTENSITY_VARIANT` (report as its own row) |

**Comparison rules.** `CMP1`–`CMP7` of the architecture §8.3 are binding: all admissible models are
reported; no outcome-based selection; `S1` agreement is not validation; `S0` is not compared on
observed-OD fit alone; per-model moment consumption is declared so the comparison cannot create a
double residual; no new numeric acceptance threshold; the share-equivalence and unit-intensity
variants carry their own rows.

### 9.1 Comparison-rule cross-reference (`CMP1`–`CMP7`)

| Rule | What it constrains in matrix terms | Where it bites in this document |
|---|---|---|
| `CMP1` | every model row that is admissible is reported; an inadmissible model is reported with its failing rule | §9 rows, §10 |
| `CMP2` | the model rows and the Owner choices may not be revised after outcomes are seen | §9, §11 |
| `CMP3` | agreement between the `S1` and `S2` rows is not validation of any proxy | §9 claim-ceiling row |
| `CMP4` | the `S0` row is compared on latent-versus-naive differences, not on observed-OD fit | §9, §10 `D4`/`D5` |
| `CMP5` | per-model moment consumption is declared so the comparison cannot create a double residual | §5, §6, §5.4 `NO_DOUBLE_RESIDUAL_RULE` |
| `CMP6` | no numeric acceptance threshold or ranking criterion beyond the frozen P3C values | §10 |
| `CMP7` | the share-equivalence and unit-intensity variants keep their own rows | §9 labelled-variant row |

## 10. Diagnostics × model matrix

| Diagnostic | `S0` | `S1` | `S2` | Notes |
|---|---|---|---|---|
| `D1` measurement residual by source/region | n/a (no measurement equations) | n/a | **required** | per family `M1`–`M5` |
| `D2` coverage wedge magnitude | no | no | **required** | reported profile only |
| `D3` hours/efficiency decomposition sensitivity | no | no | **required** | with `WEDGE_OMEGA` |
| `D4` latent-versus-naive `W` difference | **required** (against `S1`) | reported reference | **required** | the central comparison |
| `D5` latent-versus-official `ell` difference | **required** | reported reference | **required** | on the declared `ell_unit` basis |
| `D6` output/capital/wage fit | **required** if M6 is active | reported if active | **required** if M6 is active | registered locations |
| `D7` residual absorption shares | **required** if a tier-4/5 block is active | n/a | **required** | per region and block |
| `D8` government-residual crowding-out check | **required** if a government block is active | n/a | **required** | overlap with labour moments |
| `D9` wedge dimension-accounting table | structural parameters only | n/a | **required** | `RB2` comparison |
| `D10` three-model comparison table | **required** | **required** | **required** | common universe/timing/accounting |

A missing required diagnostic is a reporting defect and blocks interpretation claims (`RB8`). No
numeric acceptance threshold is attached to any diagnostic in this Issue.

## 11. H-dependency matrix (all items `UNRESOLVED`, 0 promotions)

| H item | Subject | Blocks which families / wedges / statuses | Owner-design-level note from comment `5742312556` |
|---|---|---|---|
| `H1` | NBS transition semantics (current and five-years-earlier residence, orientation, diagonal, universe, weights, missing categories, reference date) | `M1`, `WEDGE_RES`, `m_star` derivation (M-A) | still requires primary-source human verification |
| `H2` | census / 1% table availability and vintage | every family that needs a wave table (`M1`–`M6`) for the affected wave | still requires verification |
| `H3` | region coding, pinned code standard, 2000-wave Chongqing/Sichuan treatment, HK/Macao/Taiwan, XPCC, merged/absent units | `M1`, region universe `U1`–`U6` joins, all region-joined objects | still requires verification; the excluded 2000 wave keeps this out of the first pass without resolving it |
| `H4` | weights, cross-wave comparability, questionnaire/sample-design changes | `M2`, `M3`, `M5`, any weighted variant | still requires verification |
| `H5` | pair labor-intensity `lambda_ij = rho_ij·phi_ij`, or the declared share-equivalence route | the population→labour bridge; `M4b`'s coverage of the mover frame; `W_star`'s link to `M1` | **partially** resolved at the Owner-design level as `RESOLVED_WITH_DECLARED_VARIANT` for the share-equivalence **benchmark**; this does not prove that population shares equal labour-service shares |
| `H6` | origin labor amount `ell_i` on a declared basis | `ell_star` status, `M4`, the conditional denominator | basis Owner-selected as `EMPLOYED_PERSONS_DECLARED_AS_PROXY`, but the actual source, vintage and timing still require primary-source verification |
| `H7` | timing, publication, leakage, supported split claim | `M6`, feature availability, every timing declaration | the canonical design choice is window-start at the Owner-design level; source publication/reference timing still requires verification |

**Frozen properties of this matrix.**

1. The Builder resolves **none** of these; nothing in this Issue may be read as a resolution,
   promotion, weakening or reinterpretation of any H item (`E11`).
2. The two Owner-design-level notes (`H5`, `H7`) are **design choices**, not source verifications,
   and they do not unblock `M1`, `M2`, `M4` or any measurement wedge.
3. `H5` and `H6` remain two independent provenance fields tied only by `(C-LINK)` (`E20`, P3C `C19`);
   the share-equivalence route is a declared benchmark, never truth.
4. A wave whose H items are unresolved is blocked for that wave, and an unresolved item may never be
   read as "assume the neutral reading" (P3C packet rule P-1).

## 12. What this matrix does not contain

- no numeric coverage, undercoverage, informal-share, non-compliance, hours, efficiency, wage,
  output, capital or government value;
- no numeric measurement-error variance, prior magnitude or regularization strength;
- no numeric acceptance threshold, tolerance, weight, seed or pass/fail gate beyond the P3C-frozen
  values, which are inherited unchanged and are not restated here with any new number;
- no source label, table identifier, codebook item, crosswalk entry or region mass;
- no resolved H item, no promoted evidence level and no empirical estimate;
- no executed measurement equation, bridge, adapter or fit.

Every row is a declaration, a requirement, a status token or a blocked dependency.
