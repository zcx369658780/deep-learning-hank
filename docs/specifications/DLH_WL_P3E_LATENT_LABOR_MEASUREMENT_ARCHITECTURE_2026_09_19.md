# DLH-WL-P3E — latent labor measurement architecture freeze

Issue: **#84 / `DLH-WL-P3E`** — latent labor measurement architecture freeze (docs/config only).
Owner route: `DLH-WL-V1-20260918`, plus the additive dated amendment
`docs/decisions/DLH_OWNER_ROUTE_AMENDMENT_LATENT_LABOR_MEASUREMENT_2026_09_19.md`.
Authority marker: `DLH_WL_P3E_LATENT_LABOR_MEASUREMENT_ARCHITECTURE_AUTHORIZED`.
Reviewer final activation comment: **`5742332586`**.
Operative baseline: `2f4bd66343ed8ae8a95e36316d2730084bd24e52`.
Publication baseline of the amendment: `7012bb5eb7ed05b0c85fb4835a350773e9ac9c6f`.
Dedicated branch: `dsh/issue-84-dlh-wl-p3e-latent-labor-measurement-2026-09-19`.

Status: **architecture freeze only — docs/config only.** No real source, dataset, table, codebook or
licence text was read. No transition matrix, OD matrix or official statistic was inspected. No
measurement equation was evaluated. Scientific / model / training / empirical-bridge calls = **0**.

Parallel human gate: Issue **#83 / `DLH-WL-P3D`** remains OPEN and **OWNER/HUMAN REVIEW ONLY**. It is
the **only** authority that may resolve or promote H1–H7. This Issue resolves, promotes, weakens or
reinterprets **none** of them.

Companion artifacts:

1. this architecture freeze;
2. `docs/data/DLH_WL_P3E_MEASUREMENT_AND_IDENTIFICATION_MATRIX_2026_09_19.md` — measurement-equation
   matrix, wedge identification matrix, moment-assignment matrix and dimension accounting;
3. `configs/dlh_wl_p3e_latent_labor_measurement.toml` — the machine-readable mirror;
4. `reports/dlh_wl_p3e_2026_09_19/DLH_WL_P3E_REPORT.md` — Issue report and terminal.

---

## 0. What this Issue freezes, and the one thing it changes

The locked V1 route learns the **conditional foreign destination share** `W^L` given an outflow
share, with `m` and `ell` as **given accounting inputs** (AGENTS.md; P1B §3.3; P3B §2, §3). The
dated Owner amendment adds an interpretation that the first revision of the route left implicit:

> Real population / employment data are **measurement anchors**, not truth values of `W` or `ell`.
> The distance + economic-gap structural flow equation is preserved as the **latent-flow backbone**.

This Issue freezes the architecture that operationalizes that amendment. It freezes:

1. the **latent-state vocabulary** and its units (§2, §3);
2. the **structural latent-flow backbone** `s_ij,t` with masked conditional normalization (§4);
3. the **symbolic measurement-equation families** `M1`–`M6`, which relate observations to latent
   objects without ever equating them (§5);
4. the **measurement-wedge identification and regularization discipline** (§6) and the
   **residual budget** / no-double-residual rule (§7);
5. the **three-model comparison contract** `S0` / `S1` / `S2` (§8);
6. the **first-wave Owner choices** (§9) and the **future diagnostics** that must accompany any
   later execution (§10).

**What it changes: nothing that was already frozen.** All accepted P3A/P3B/P3C semantics are
inherited unchanged, including the whole P3C threshold/search/threshold-claim surface: `C1`–`C21`
remain binding (§12.1). **No new numeric threshold, tolerance, seed or search constant is introduced
by this Issue**, and no inherited value is restated with a different number.

Two things this Issue deliberately does **not** do:

- it does **not** specify a production function, a government block, a market-clearing structure or a
  HANK coupling — the TFP/productivity and government-investment objects appear here only as
  **registered residual blocks with declared locations and budget rules** (§6.4, §7);
- it does **not** decide whether `ell_star` is estimated jointly with `W_star` — that is a later
  design decision, bounded by §7 and by H5/H6.

## 1. Scope, inheritance and non-authorization

### 1.1 Inherited authority (read-only, unchanged)

| Source | What is inherited |
|---|---|
| `AGENTS.md`, `tasks/TASK_INDEX_CURRENT.md` | Owner-locked route, frozen household dependency, no re-planning |
| Owner route freeze `DLH_OWNER_ROUTE_FREEZE_WL_V1_2026_09_18.md` | the V1 object and its orientation |
| Owner amendment `..._LATENT_LABOR_MEASUREMENT_2026_09_19.md` | latent objects, backbone preservation, measurement layer, identification discipline, the three-model requirement, first-wave choices |
| Issue #83 body + Owner comment `5742312556` | H1–H7 remain human-resolved; Owner A–E choices |
| P1B label and sample schema | label semantics, `m`/`ell` as given inputs, `STRUCTURAL_ZERO` rules, `feature_available_at_prediction_time` |
| P3A Branch B | real-data label evidence gate outcome |
| P3B preregistration + region/`m`/`ell` provenance contract | `(A1)`–`(A4)`, `(P-L)`, `lambda_ij = rho_ij·phi_ij`, `(C-LINK)`, `ell_unit` tokens, region universe rules U1–U6, weights/harmonization/leakage contract |
| P3C execution-readiness freeze | the 16 Reviewer numeric thresholds, `F_all_exact`/`F_search_tol`, R1–R4, claim ceiling, invariants `C1`–`C21`, H1–H7 packet |

Nothing in this Issue may be read as revising any row of that table.

### 1.2 What this Issue does not authorize

No data ingestion, no download, scrape, purchase or opening of a source; no source adapter; no
crosswalk; no bridge execution; no real transition-matrix inspection; no empirical estimation,
fitting, training or calibration; no social-insurance undercoverage calibration; no labor-law
non-compliance calibration; no fixed informal-employment share; no new government-investment
residual; no HJB/KFE/GE/MATLAB/household call; no `pytest`/full-suite run; no E3 promotion; no
successor Issue; no PR, merge, close or self-acceptance. Section §13 restates these as binding
flags, and the TOML mirrors them.

### 1.3 The single most important architecture statement

A measurement equation in this architecture relates an **observation** to a **latent object through
declared error and coverage structure**. It is never an identity:

```
W_model  =  W_census        FORBIDDEN as an assumption
ell_model =  ell_official   FORBIDDEN as an assumption
```

Such an equality may hold only if a **separately accepted source-specific measurement contract**
proves it for that source, wave and region universe. Until then, the observation enters as an
**anchor / moment / likelihood component** with explicit source-specific uncertainty, exactly as the
amendment §5 requires.

## 2. Latent-state vocabulary

### 2.1 The six latent objects

| Symbol | Name | Interpretation | Unit | Kind |
|---|---|---|---|---|
| `W_star_ij,t` | latent conditional destination share of labor services | share of the labor-service outflow of origin `i` realized in period `t` that goes to `j`; conditional on the outflow having occurred | dimensionless share | **the V1 learning object** |
| `m_star_i,t` | latent outflow share / transition intensity | within-period outflow share of origin `i`'s labor, required by the accounting closure | dimensionless share in `(0, 1]` | given accounting input |
| `ell_star_i,t` | latent effective origin labor amount | total effective labor of origin `i` in period `t` entering the flow identity | efficiency-labor units | given accounting input |
| `N_workers_star_i,t` | latent worker quantity | number of employed workers of origin `i` in `t` | persons | latent component |
| `h_star_i,t` | latent hours / intensity | effective hours per worker in the period | hours / person | latent component |
| `e_star_i,t` | latent efficiency | efficiency-labor units per hour | efficiency-labor units per hour | latent component |

```
DEFINITION (frozen):   ell_star_i,t  =  N_workers_star_i,t * h_star_i,t * e_star_i,t
```

This is a **modeling decomposition**, exactly as the amendment §2 states. It is **not** a claim that
the three factors are separately identified in any current or future data set; §2.3 records their
identification status, and §6 records what would be required to discipline them.

### 2.2 Accounting objects and the frozen identities

```
W_star_ii,t = 0 ;  W_star_ij,t >= 0 ;  sum_{j != i} W_star_ij,t = 1        (conditional normalization)
P_ii,t      = 1 - m_star_i,t                                               (home retention)
P_ij,t      = m_star_i,t * W_star_ij,t          (j != i)                   (flow construction)
F_ij,t      = ell_star_i,t * P_ij,t = ell_star_i,t * m_star_i,t * W_star_ij,t
```

These four lines are the **accounting tier**. They are imposed, never fitted, and no residual may
enter them as a free parameter (§7, rule RB3). They are inherited from the V1 route and from
P3A §1 and are unchanged here; in particular the pair target
`F_ij = ell_i · m_i · W_ij` is not re-derived and `m`/`ell` keep their P1B/P3B status as given
accounting inputs.

### 2.3 Block membership — which object enters which block

| Block | Objects entering | Status of the block in this Issue |
|---|---|---|
| **household block** | `m_star`, `ell_star` and the conditional shares `W_star` enter only through the already-accepted accounting, as **given inputs**; the household dependency is frozen and is **not re-specified here** | inherited unchanged (P1B/P3A/P3B); nothing new is frozen |
| **firm / production block** | `ell_star` as effective labor input, together with capital and a productivity object `A_i,t`; the functional form is **not specified here** | registered only (§6.4) |
| **flow-accounting block** | `F_ij,t = ell_star_i,t · m_star_i,t · W_star_ij,t`; row-conditional normalization; `W` diagonal false | the accounting tier of §2.2 |
| **measurement block** | every observation `T_obs`, `L_obs`, `H_obs`, `ELL_obs`, `COV_obs`, `Y_obs`, `K_obs`, `w_obs`, `G_obs` and its relation to the latent objects | frozen here (§5) |
| **government block** | `G` object, registered at its accounting location only | registered only (§6.4) |

**Consequences that must not be blurred:**

1. **The learning object is the conditional share, not the totals.** The V1/P2 learning exercise maps
   features to `W^L` for a **given** outflow share; `m_star` and `ell_star` are never the label of
   that learner and never features of it (P1B §3.3, P3B §4.7 L2, restated as `C19`-adjacent rule
   `E15` in §12.2).
2. **A latent measurement layer is added around the given inputs, not inside the learner.** Whether
   `m_star`/`ell_star` are jointly disciplined by anchors in the measurement model is a later design
   question (§7 budget, H5/H6); even then they remain neither label nor feature of the conditional
   share learner.
3. **`e_star` and `h_star` are structural factors, not observations.** Any later design that reports
   them separately must declare the measurement equation (M3/M4) that disciplines each, or declare
   them as prior-regularized structural objects with a sensitivity replicate.

### 2.4 Identification status vocabulary (closed, exactly one per latent object per design)

| Status | Meaning |
|---|---|
| `STRUCTURALLY_DEFINED_NOT_OBSERVED` | the object is defined by the architecture and is not directly observed by any source |
| `LATENT__MEASUREMENT_DISCIPLINED` | at least one declared measurement equation with a verified source disciplines it (requires H-resolution) |
| `LATENT__PRIOR_REGULARIZED` | no verified source disciplines it; it is carried by a declared low-dimensional prior/regularizer with a sensitivity replicate |
| `LATENT__NOT_SEPARATELY_IDENTIFIED` | the object is a component of a decomposition that the declared measurement set cannot separate from its partner, e.g. the `h_star` / `e_star` split under a worker-count-only source |
| `LATENT__BLOCKED_BY_H` | the object needs a source whose semantic item is unresolved in H1–H7, so no measurement claim is available |

No status above may be upgraded inside this Issue or by the Builder at any time; `LATENT__MEASUREMENT_
DISCIPLINED` additionally requires a human-resolved H item (§12.2 rule `E11`).

## 3. Units and dimension algebra

The Issue requires dimension/unit checks. The following algebra is frozen and every measurement
equation in §5 is dimensionally consistent with it.

| Quantity | Unit | Notes |
|---|---|---|
| `W_star_ij,t` | dimensionless | conditional share; `sum_{j != i} W_star_ij,t = 1` |
| `m_star_i,t` | dimensionless | share in `(0, 1]` |
| `P_ij,t` | dimensionless | transition share |
| `N_workers_star_i,t` | persons | |
| `h_star_i,t` | hours / person | hours worked per person within period `t`; the period is a label (`U-5`), not a unit factor |
| `e_star_i,t` | efficiency-labor units / hour | if a per-worker efficiency basis is declared instead, `e` is units/person and the declaration must say so; the two encodings may not be mixed inside one evaluation set |
| `ell_star_i,t` | efficiency-labor units | `= persons · (hours/person) · (units/hour)` |
| `F_ij,t` | efficiency-labor units | `= ell_star_i,t · P_ij,t` |
| `L_obs_i,t` | persons | employment-count observation |
| `H_obs_i,t` | hours | hours/intensity observation, if any |
| `ELL_obs_i,t` | efficiency-labor units | efficiency-labor observation, if any |
| `q_cov`, `q_hours`, `q_eff`, `q_si`, `κ_res` | dimensionless | source-frame/coverage factors, each in a declared admissible range; **no numeric value is chosen in this Issue** |
| `ω_i,t := h_star_i,t · e_star_i,t` | efficiency-labor units / person | intensity-efficiency content per worker; the only route by which a worker count can anchor `ell_star` |
| `distance_ij` | km (or a declared monotone transform) | static bilateral friction |
| `beta_d` | per distance unit | score contribution is dimensionless, so `beta_d` carries `1/distance` |
| `economic_gap_ij,t` | dimensionless (declared log-ratio or normalized difference form) | must be declared as one form per design |
| `Z_ij,t` | declared per term | optional registered terms only |
| `s_ij,t` | dimensionless score | |

**Unit rules (binding).**

```
U-1  ell_star is NOT a person count. Equating a person count to ell_star requires q_cov = 1 AND omega = 1,
     which is never assumed; it is only the declared variant ELL_PROXY_UNIT_INTENSITY_VARIANT (§5, M4b).
U-2  m_unit_basis (P3B section 2) and ell_unit must be reconcilable so that F = ell * m * W is
     dimensionally coherent (P3B E8). A PERSONS-based m with an EFFICIENCY_LABOR ell is incoherent
     unless a declared conversion is carried as an explicit measurement equation.
U-3  a score term whose unit is not dimensionless after multiplication by its coefficient may not
     enter s_ij,t.
U-4  no measurement equation may contain a quantity of undeclared unit; every symbol must appear in
     the table above or be declared in the matrix document.
U-5  the accounting period is a LABEL, not a dimension: every quantity in this architecture is
     stamped by (i, t), and the period is therefore never carried as a unit factor. This is why
     h_star is hours/person and ell_star is efficiency-labor units, and it is what makes
     omega = h_star * e_star a per-person quantity and N_workers_star * omega = ell_star exact.
```

## 4. Structural latent-flow backbone (preserved, not replaced)

The amendment requires the distance + economic-gap structural mobility equation to be **preserved as
the latent-flow backbone**. It is frozen here in the form the Issue specifies:

```
s_ij,t          =  beta_d * distance_ij  +  beta_gap' * economic_gap_ij,t  +  beta_z' * Z_ij,t
W_star_ij,t     =  exp(s_ij,t) / sum_{l != i, l in S_i,t} exp(s_il,t)     for j != i, j in S_i,t
W_star_ij,t     =  0                                                      for j = i or j not in S_i,t
```

where `S_i,t` is the declared allowed destination support for origin `i`.

### 4.1 Required terms

| Term | Symbol | Interpretation | Note |
|---|---|---|---|
| static geographic friction | `beta_d * distance_ij` | bilateral distance / adjacency / accessibility friction | time-invariant; a time-varying friction may enter only as a registered `Z` term |
| wage / income opportunity gap | `beta_gap,w * gap_wage_ij,t` | destination-origin wage or income opportunity differential | must be declared window-start available |
| output / productivity opportunity gap | `beta_gap,y * gap_output_ij,t` | destination-origin output or productivity opportunity differential | same timing requirement |
| optional registered terms | `beta_z' Z_ij,t` | e.g. accessibility or policy/friction terms | admissible **only** if later verified; unverified terms are not active |

### 4.2 Frozen properties of the backbone

| # | Property | Statement |
|---|---|---|
| B1 | conditional normalization | masked row-softmax over `S_i,t`; the diagonal is excluded by construction; `W_star_ii,t = 0` exactly |
| B2 | support is a design object | `S_i,t` is declared before execution, may never be widened to fit an observation or a candidate, and may not change after outcomes are seen (P1B §3.4, P3B §1.7 U6, P3C `C10`) |
| B3 | interpretability preserved | the backbone is retained *because* the accepted P2 result found the correctly specified parametric baseline was not outperformed by the small neural mapping; a neural component does not automatically replace it |
| B4 | ML is additive only | any future ML residual component must be **additive/augmenting** to `s_ij,t`, must be **separately identified** by declared moments, and must carry its own dimensionality and regularization declaration; an ML component may not absorb the structural terms |
| B5 | no numeric values | `beta_d`, `beta_gap`, `beta_z` are **symbolic** here; no value, sign estimate or prior magnitude is frozen |
| B6 | declared expected signs are design priors, not findings | a design declares the expected sign of each coefficient *before* execution; a sign reversal is reported as a finding, never absorbed by redefining the gap variable |
| B7 | timing | every `Z_ij,t` and every gap term must satisfy `feature_available_at_prediction_time = true` under the canonical window-start design (§9, choice E) |
| B8 | no leakage | `m_star`, `ell_star` and any same-period realized flow may not be features (P3B §4.7 L1–L2) |
| B9 | gap-form homogeneity | one declared gap form (log-ratio or normalized difference) per design, applied to every origin–destination cell; the form may not differ across regions |

### 4.3 What the backbone is not allowed to do

The backbone produces `W_star` from **structural** terms. It may not:

- contain `T_obs`, `L_obs`, `ELL_obs` or any observation as an argument (that would make the
  backbone a re-encoding of the data and destroy the `S0`/`S2` comparison);
- contain a per-origin–destination free intercept that is not declared as a registered `Z` term with
  its own moment assignment;
- be re-tuned per wave or per region after outcomes are seen (`C17`).

## 5. Measurement-equation families (symbolic; no empirical values)

Every equation below is a **declaration of structure**. No coefficient, coverage factor, error
variance or share is chosen, and no observation was consulted. Each family carries: the observed
object, the latent target, the equation, the wedge it activates, the declarations it requires, its
current status, and its claim ceiling. `OBS_*` and `LAT_*` symbols are as defined in §2 and §3.

### 5.1 M1 — residence / migration observation

```
OBSERVED     : T_obs^(k)_ij,t   observed k-year residence-transition share, person-based,
                                on the source's declared frame and universe
LATENT LINK  : Pp^(k)_ij,t      latent k-step PERSON-based residence transition share
               (NOT a labor-service object, NOT W_star)

EQUATION
  T_obs^(k)_ij,t  =  ( 1 - kappa_res,t ) * Pp^(k)_ij,t * 1{ j in frame }
                     + zeta_res_ij,t
                     + eps_res_ij,t
  with
    kappa_res,t     residence classification/coverage wedge (declared per source and wave)
    zeta_res_ij,t   frame/timing discrepancy term, declared; includes the source's
                    unclassified / non-mainland / other bucket a_res_i,t, which is carried as an
                    explicitly REPORTED category and never distributed across units
                    (P3B contract section 1.6, U-rules)
    eps_res_ij,t    observation error with declared treatment (moment condition or likelihood)
REQUIRED DECLARATIONS
  frame; universe; reference window (t-k, t]; orientation; diagonal treatment; weights;
  missing/unknown categories; reference date; publication vintage  (all H1/H3 items)
PROHIBITED
  no identity W_obs = W_star ; no labor-service reading of M1 ;
  no distribution of an unclassified bucket ;
  no use of a post-reference-moment vintage unless declared (H7)
SEMANTIC BRIDGE (not part of M1)
  the labor-service conditional share W_star is connected to person-based objects only through
  the accepted T-family bridge and the lambda / H5 route (P3B section 4). M1 alone does not
  identify W_star.
STATUS        NO_SOURCE_VERIFIED__BLOCKED_BY_H1_H3
CLAIM CEILING the observed object measures people-based multi-year RESIDENCE transitions
```

### 5.2 M2 — employment-count observation

```
OBSERVED     : L_obs_i,t        employed persons / labor-force / unit-employment count
LATENT TARGET: N_workers_star_i,t

EQUATION
  L_obs_i,t  =  q_cov_i,t * N_workers_star_i,t  +  eps_L_i,t
  with  q_cov_i,t  a source-specific coverage factor, declared for every source and region,
                   dimensionless, carrying the source's institutional frame (registration,
                   establishment, payroll, survey frame) relative to the latent worker universe
REQUIRED DECLARATIONS
  source frame; institutional coverage basis; whether the unit is persons, jobs or posts;
  region universe; reference period; whether published figures are already weighted
PROHIBITED
  no numeric q_cov ; q_cov may not be treated as one for all sources ;
  a count of jobs may not be equated to a count of workers without a declared equation
STATUS        NO_SOURCE_VERIFIED__BLOCKED_BY_H2_H4
CLAIM CEILING a partial observation of latent worker quantity, never of ell_star
```

### 5.3 M3 — hours / intensity observation

```
OBSERVED     : H_obs_i,t        hours / intensity measure, if any
LATENT TARGET: h_star_i,t  (via the product N_workers_star * h_star)

EQUATION (when a source exists)
  H_obs_i,t  =  q_hours_i,t * ( N_workers_star_i,t * h_star_i,t )  +  eps_H_i,t
ABSENT CASE (frozen disposition)
  if no hours source exists, h_star may NOT be set to a hidden constant and may NOT be left free
  per region; it must be carried by a declared low-dimensional prior/regularizer
  ( L_hours form, section 6.3 ) with a sensitivity replicate
PROHIBITED
  long hours may never be inferred from worker counts alone ;
  a worker count may not stand in for hours
STATUS        NO_SOURCE_VERIFIED__BLOCKED_BY_H2_H4  (or LATENT__PRIOR_REGULARIZED if absent)
CLAIM CEILING a partial observation of the hours margin, never a proof that h_star is identified
```

### 5.4 M4 — efficiency-labor observation

Two admissible encodings, and the declared basis decides which is active. They may not be mixed.

```
M4a DIRECT BASIS ( ell_unit = EFFICIENCY_LABOR )
  ELL_obs_i,t  =  q_eff_i,t * ell_star_i,t  +  eps_eff_i,t
  requires a source that actually measures efficiency labor, with its unit stated

M4b DECLARED PROXY BASIS ( ell_unit = EMPLOYED_PERSONS_DECLARED_AS_PROXY )

  the proxy observation measures WORKER QUANTITY, not ell_star:
      N_obs_i,t      =  q_cov_i,t * N_workers_star_i,t + eps_L_i,t        ( = M2 )
      ell_star_i,t   =  omega_i,t * N_workers_star_i,t
      omega_i,t      :=  h_star_i,t * e_star_i,t                          ( units: eff-labor / person )

  therefore   ELL_obs^proxy_i,t := N_obs_i,t   anchors  ell_star_i,t
              ONLY JOINTLY WITH  omega_i,t  and  q_cov_i,t .

  IDENTITY PROHIBITED (frozen):  ell_star_i,t  !=  N_obs_i,t  unless q_cov = 1 and omega = 1,
              which is NEVER ASSUMED. The equality is only the declared sensitivity variant
              ELL_PROXY_UNIT_INTENSITY_VARIANT, which must be reported with its own row and claim.
REQUIRED DECLARATIONS
  ell_unit token; unit of the observation; timing relative to the destination decision
  (must precede or coincide, P3B E4); coverage versus the label universe; C-LINK status
PROHIBITED
  no substitution of total population, urbanization or an unrelated total for ell (P3B E5/E6) ;
  no equating of person counts with efficiency labor
STATUS        NO_SOURCE_VERIFIED__BLOCKED_BY_H6
CLAIM CEILING a noisy anchor for ell_star under the declared proxy basis, never ell_star itself
```

### 5.5 M5 — formal / informal and covered / uncovered employment (registered channel)

```
OBSERVED     : COV_obs_i,t      covered-employment observation: social-insurance enrollment,
                                unit-employment count, or an equivalent institutional channel
DECOMPOSITION (registered)
  N_workers_star_i,t  =  N_cov_star_i,t  +  N_unc_star_i,t
EQUATION (only if a source later supports it)
  COV_obs_i,t  =  q_si_i,t * N_cov_star_i,t  +  eps_cov_i,t
  with q_si_i,t the institutional coverage factor of that channel
FROZEN PROHIBITIONS
  social-insurance enrollment may NOT be equated with total employment ;
  an informal / uncovered share may NOT be assumed numerically ;
  no undercoverage rate may be invented, borrowed or defaulted ;
  the channel is active only if a source supports it AND H2/H4 resolve its frame
STATUS        MEASUREMENT_CHANNEL_DECLARED_NOT_CALIBRATED
CLAIM CEILING a declared measurement channel for a coverage split; it may not be read as a
              measured undercoverage rate
```

### 5.6 M6 — macro / production anchor family (registered, not specified)

This family is **registered so that the residual budget of §7 has a well-defined moment side**. It
is **not** specified in this Issue; the functional forms, the capital accumulation, the market
structure and the government block are later-Issue objects.

```
REGISTERED LOCATIONS (symbolic only)
  output        Y_obs_i,t   relates to  A_i,t , K_star_i,t , ell_star_i,t  through an
                            unspecified production mapping  F(.,.)
  capital       K_obs_i,t   relates to  K_star_i,t
  wage          w_obs_i,t   relates to a marginal-product expression of the same mapping
  government    G_obs_i,t   relates to  G_i,t , the registered government-investment block
STATUS        REGISTERED_NOT_SPECIFIED_IN_THIS_ISSUE
PROHIBITED
  no production function, no elasticity, no share parameter and no government rule is chosen here ;
  these symbols may not be used in this Issue to claim any quantitative result
```

## 6. Measurement-wedge identification and regularization discipline

### 6.1 The mandatory wedge record (the eight-field tuple)

Every measurement wedge or residual used in any later empirical design must carry **all eight**
fields before it may appear in an equation. A wedge with an incomplete record is
`WEDGE_RECORD_INCOMPLETE__NOT_ADMISSIBLE`.

```
1 symbol                    the wedge's own symbol and unit
2 equation location         the exact measurement equation or block it enters
3 economic interpretation   what real-world discrepancy it represents
4 disciplining source/moment the declared source, moment or identity that can discipline it
5 allowed dimensionality    the declared parametric form and its free-parameter count structure
6 prior / regularization    what holds it when its disciplining moment is weak or absent
7 sensitivity requirement   the replicate(s) that must be reported for it
8 claim ceiling             what may and may not be claimed when it is active
```

### 6.2 The registered wedges

| Wedge | Symbol | Equation | Interpretation | Disciplined by | Allowed dimensionality | Prior / regularization | Sensitivity replicate | Claim ceiling |
|---|---|---|---|---|---|---|---|---|
| migration / residence wedge | `kappa_res_t` | M1 | residence classification, timing and multi-year aggregation discrepancy between the observed residence object and the latent person-based k-step transition | H1/H3 source semantics (documentation, not fit) | wave-level and source-level scalar(s); a declared semantic variant, never per-pair | set to the resolved mapping's value when H1 resolves semantics; otherwise a declared low-dimensional form with a prior | residence-semantics variant replicate | a measurement discrepancy, never an economic migration cost |
| employment-coverage wedge | `q_cov_i,t` | M2 | institutional frame of an employment count relative to the latent worker universe | M5 channel if supported; macro employment identity otherwise | declared low-dimensional form over `(i, t)`; a per-region-per-period free vector is forbidden without an anchor | declared prior with a reported sensitivity | anchored vs prior-only replicate | coverage of a source, never a labor-supply distortion |
| hours wedge | `q_hours_i,t` | M3 | reporting basis of an hours/intensity measure | M3 source if it exists; prior otherwise | declared low-dimensional form | declared prior; `h_star` may not be free per region | prior-scaled replicate | a measurement basis, never a preference for leisure |
| efficiency wedge | `q_eff_i,t` | M4 | efficiency-labor content discrepancy of a source | M4a source if it exists; prior otherwise | declared low-dimensional form | declared prior; jointly with the `h_star`/`e_star` split status | split-sensitivity replicate | a measurement basis, never a technology claim |
| intensity-efficiency content | `omega_i,t = h_star_i,t * e_star_i,t` | M4b | efficiency labor per worker, the only route by which a worker count anchors `ell_star` | M3 + M4a if available; else prior | declared low-dimensional form; not free per region | required prior with declared functional form | unit-intensity variant `ELL_PROXY_UNIT_INTENSITY_VARIANT` | a decomposition, never an identified productivity level |
| labour coverage / TFP split — productivity | `A_i,t` | M6 (tier 4) | total-factor-productivity / productivity object of the registered production mapping | declared macro moments (output, capital, wage) | declared low-dimensional form; sector or aggregate | required | productivity-prior replicate | a registered productivity object, never an identified causal effect |
| government-investment / output residual | `G_i,t` | M6 (tier 5) | explicit government-investment / government-output block | its **own** declared anchor `G_obs` or a declared prior, **plus** a moment set disjoint from the labour wedges | bounded by its declared low-dimensional form | required anchor or prior; **unbounded free form forbidden** | anchor-relaxation replicate | an economic block with its own moments, never a provincial balancing residual |

`WEDGE_RES` (migration), `WEDGE_COV`, `WEDGE_HOURS`, `WEDGE_EFF`, `WEDGE_OMEGA`, `WEDGE_TFP`,
`WEDGE_GOV` are the registered identifiers; the TOML mirrors them field by field.

### 6.3 Regularization forms (declared shape, no numeric values)

When a wedge has no verified disciplining source, it may not be free. It must take one of the
declared low-dimensional forms below, with its free directions declared and counted:

```
L_constant   : wedge_i,t      = wedge_bar
L_time       : wedge_i,t      = wedge_bar_t
L_factor     : log wedge_i,t  = log wedge_bar_t  + gamma' X_i        (X declared, low-dimensional)
L_anchored   : the wedge is pinned by a declared anchor observation or identity for the
               regions/periods the anchor covers and takes a declared form elsewhere
L_grouped    : wedge_i,t      = wedge_g(i) with a declared group partition g(i)
```

Frozen properties: the form is declared **before** execution; the free-parameter count of the chosen
form is reported in the dimension-accounting table (diagnostic `D9`); expanding a form after seeing
outcomes is forbidden (`C17`); `X_i` may not contain the label, a same-period realized flow or any
post-decision measurement (`B7`, `B8`).

### 6.4 Identification discipline rules

| # | Rule |
|---|---|
| I1 | every wedge carries the complete eight-field record of §6.1 before it appears in any equation |
| I2 | every wedge declares its allowed dimensionality and its resulting free-parameter count; an undeclared or unbounded dimensionality is `UNRESTRICTED_WEDGE_FORBIDDEN` |
| I3 | a wedge whose free directions span regions × periods without an anchor, prior or grouping is forbidden |
| I4 | a wedge and its partner in an unidentified split (e.g. `h_star` vs `e_star` under a worker-count-only source) may not both be free: exactly one is free, the other is fixed, grouped or prior-carried, and the split status is reported as `LATENT__NOT_SEPARATELY_IDENTIFIED` |
| I5 | the six-element set {labour coverage, hours, efficiency, migration, TFP, government} may **not** be simultaneously unrestricted (Issue §6; amendment §6) |
| I6 | when the source that would discipline a wedge is unresolved in H1–H7, the wedge is **not** freed to compensate: it is fixed by prior or the affected dimension set is excluded (`H_BLOCKED_WEDGE_FAIL_CLOSED`) |
| I7 | no wedge may be introduced solely to close provincial output or GDP without an explicit moment or prior (Issue §6) |
| I8 | no wedge value may be reported as data-identified unless a source-specific measurement contract proves it |
| I9 | every active wedge reports its sensitivity replicate; a missing replicate is a reporting defect |
| I10 | a wedge that fails any identification rule makes the design `RESIDUAL_BUDGET_EXCEEDED__NOT_ADMISSIBLE` (§7) — the design is reported as inadmissible, never silently relaxed |

## 7. Residual budget and the no-double-residual rule

### 7.1 Identification hierarchy (tiers)

```
TIER 1  observed / accounting identities          imposed exactly, never fitted
TIER 2  low-dimensional structural mobility       the section 4 backbone
TIER 3  source-specific measurement wedges        section 6, disciplined per the matrix
TIER 4  production / productivity residuals       A_i,t, registered at M6
TIER 5  government residual                       G_i,t, only if separately anchored and bounded
```

A later design must assign every residual to exactly one tier and must report the assignment.

### 7.2 The residual budget (frozen rule set)

Let `R` be the set of free residual/wedge parameter blocks in a design, `d_r` the declared
free-parameter count of block `r`, and `M_r` the set of moments assigned to `r` (declared per block).

```
RB1  every r in R has M_r non-empty                                  (no unanchored free residual)
RB2  d_r <= |M_r| for every r                                        (no block with more free
                                                                      directions than moments)
RB3  the tier-1 accounting identities are imposed exactly: no residual parameter may enter
     F_ij = ell_star_i * m_star_i * W_star_ij, the row normalization, or the support mask
RB4  moment disjointness: M_r intersect M_s = empty for r != s        (no moment serves two residuals)
RB5  no two residual blocks may be algebraic complements inside one identity, and no block may be
     defined as the difference of two others in a way no moment can separate
RB6  government block condition: G_i,t is active only if it has its own declared anchor or prior,
     its moment set satisfies RB4 against every labour wedge, and its dimension is bounded by its
     declared low-dimensional form
RB7  the six-element forbidden set of I5 is not simultaneously unrestricted: at least the tier-3
     wedges satisfy RB1-RB2 and at least one of the tier-4 / tier-5 blocks is anchored or inactive
RB8  reporting: the design reports the wedge dimension-accounting table (D9), the moment-assignment
     matrix and the absorption shares (D7); a missing report is a reporting defect and blocks any
     interpretation claim
```

Failure of any of `RB1`–`RB7` yields

```
RESIDUAL_BUDGET_EXCEEDED__NOT_ADMISSIBLE
```

which is **fail-closed**: no estimate, no `W_star` target, no comparison ranking and no claim may be
reported from that design. The correct responses are (a) resolve the missing source or anchor under
Issue #83, (b) reduce dimensionality by a declared prior/grouping, or (c) drop the affected
regions/periods by the declared exclusion rule — never to free the wedge.

### 7.3 The no-double-residual statement

Machine-readable identifier: **`NO_DOUBLE_RESIDUAL_RULE`** (mirrored in the TOML).

```
NO-DOUBLE-RESIDUAL (frozen):
  The same unexplained variation may not be absorbed by two different residual blocks.
  Concretely: (i) a moment assigned to a labour-measurement wedge may not also be assigned to the
  TFP block or the government block; (ii) the government block may not be the unbounded
  province-by-province balancing residual that closes output while labour wedges absorb the same
  moments; (iii) a residual introduced only because an identity fails to close is not a measurement
  wedge and is forbidden.
```

## 8. Three-model comparison contract (S0 / S1 / S2)

### 8.1 The three models

| ID | Name | Latent-flow source | Observation role | Active tiers | Minimum claim ceiling |
|---|---|---|---|---|---|
| `S0` | `STRUCTURAL_ONLY` | the §4 backbone alone: `s_ij,t` → masked softmax → `W_star` | OD observations are **not truth**; they may appear only as reported diagnostics, never as the target the model is fitted to | tier 2 (+ tier 1 identities) | may not claim to match observed OD; may claim only a structural latent allocation disciplined by macro moments |
| `S1` | `NAIVE_DATA_PROXY` | the observed proxy used as directly as its source semantics allow | the observation **is** the working object: `W_used = W_obs`, `ell_used` on the declared proxy basis | tier 1 (no measurement wedges active) | **benchmark only** — `NOT_PREFERRED_TRUTH`; may not claim structural interpretation, may not claim that the proxy equals the latent object |
| `S2` | `LATENT_MEASUREMENT_ADJUSTED` | the §4 backbone jointly disciplined by the §5 measurement equations, with the §6 wedges and the §7 budget | every observation is a noisy anchor with a declared measurement equation and source-specific uncertainty | tiers 2–5 as declared, subject to RB1–RB8 | may claim joint latent discipline; may **not** claim that any latent object is observed, nor global identification |

### 8.2 Frozen comparability requirements

All three models must use the **same**:

1. region universe (`U1`–`U6`, P3B contract §1.7) and the same per-wave mappable intersection;
2. information timing: the canonical **window-start** design (choice E);
3. macro-accounting definitions: the tier-1 identities of §2.2, the same `W`-support convention
   (diagonal false), the same row-conditional normalization, the same units (§3);
4. the same downstream HANK blocks when later coupled — the household dependency is frozen and is not
   re-specified per model;
5. the same diagnostics set (§10) and the same reporting structure;
6. the same wedge registry and the same `RB1`–`RB8` budget rules for whatever is active.

### 8.3 Comparison rules

| # | Rule |
|---|---|
| CMP1 | a comparison must report all **admissible** models; an inadmissible model is reported as inadmissible with its failing rule, never replaced silently |
| CMP2 | no model may be selected, preferred, tuned or dropped **after** inspecting outcomes: `NO_OUTCOME_BASED_MODEL_SELECTION` |
| CMP3 | `S1` is a benchmark: agreement between `S1` and `S2` may not be presented as validation of the proxy, and disagreement may not be presented as proof that the latent model is correct |
| CMP4 | `S0` may not be compared on observed-OD fit alone, because it is defined not to target the OD object |
| CMP5 | the comparison must declare, per model, which moments each model consumes, so that the comparison itself cannot create a double residual |
| CMP6 | no numeric acceptance threshold, tolerance or ranking criterion beyond the already frozen P3C values may be introduced; the comparison reports profiles and differences, not pass/fail gates, unless a later Reviewer authorization freezes a threshold before execution |
| CMP7 | the share-equivalence route (choice C) is a **labelled variant inside `S1`**: `S1_VARIANT_SHARE_EQUIVALENCE__DECLARED_BENCHMARK`, reported with its own row and never merged with the `S1` base row or with `S2` |

`E6` in §12.2 makes these rules binding invariants.

## 9. First-wave Owner choices (frozen)

| # | Owner choice (from comment `5742312556`, amendment §8) | Frozen token in this architecture |
|---|---|---|
| A | first bounded empirical wave = **2010 Census only** | `FIRST_WAVE_2010_CENSUS_ONLY` |
| B | the **2000 wave is excluded** initially | `WAVE_2000_EXCLUDED` (consistent with the P3B §1.5 (b) `WAVE_EXCLUDED` handling) |
| C | H5 share-equivalence only as a **declared benchmark/sensitivity variant** | `SHARE_EQUIVALENCE__DECLARED_BENCHMARK_VARIANT` (inside `S1` only, per `CMP7`) |
| D | employed persons = noisy proxy anchor for latent `ell_star` | `EMPLOYED_PERSONS_DECLARED_AS_PROXY` (P3B `ell_unit` token; M4b; `ELL_PROXY_IDENTITY_NOT_ASSUMED`) |
| E | canonical information set = **window-start** | `WINDOW_START_CANONICAL`; the window-end nowcast is **excluded from the first pass** |

```
FROZEN CONSEQUENCES
  W1  these five choices were fixed before any outcome was observed and may not be revised after
      an outcome is seen (C17).
  W2  none of them resolves, promotes, weakens or pre-empts any H1-H7 item. H1-H4 still require
      primary-source human verification; H5/H6 remain measurement/provenance questions and are not
      identity proofs for W_star or ell_star; H7's source publication/reference timing still
      requires verification even though the design choice is window-start.
  W3  the 2010-only first wave fixes the wave axis of the first comparison; it does not authorize
      any 2010 source to be opened.
  W4  excluding the 2000 wave removes the section 1.5/1.6 origin-coding ambiguity from the first
      wave design; it does not resolve it for any later wave.
```

## 10. Future diagnostics (defined now, not run)

Every later execution must report these. They are **diagnostics**, and none of them is a numeric
acceptance threshold.

| # | Diagnostic | Definition (symbolic) | Required granularity | Reads on |
|---|---|---|---|---|
| D1 | measurement residual by source and region | `r_Mk_i,t` = observed minus equation-implied value for each measurement family `Mk` | source × region × period | M1–M5 |
| D2 | coverage wedge magnitude | the reported profile of `q_cov_i,t` (and `q_si_i,t` if M5 is active) | region × period, by source | M2, M5 |
| D3 | hours / efficiency decomposition sensitivity | behaviour of the `N_workers_star`/`h_star`/`e_star` split across declared variants | variant × region | M3, M4, `WEDGE_OMEGA` |
| D4 | latent-versus-naive `W` difference | `ΔW_ij,t = W_star_ij,t − W_naive_ij,t` | pair × period, and by origin | S1 vs S2 |
| D5 | latent-versus-official `ell` difference | `Δell_i,t = ell_star_i,t − ELL_obs_i,t` on the declared basis | region × period | S1 vs S2, M4 |
| D6 | output / capital / wage fit | residuals of the registered M6 locations | region × period | M6 |
| D7 | residual absorption shares | the share of provincial output residual absorbed by each wedge/block | region × block | §7, `WEDGE_TFP`, `WEDGE_GOV` |
| D8 | government-residual crowding-out check | whether the government block's assigned moments overlap the labour wedges' moments, and how labour-wedge sensitivity changes with the block active versus inactive | block × region | §7 `RB6` |
| D9 | wedge dimension-accounting table | declared free-parameter count per wedge, its assigned moment count, and the `RB2` comparison | design level | §6, §7 |
| D10 | three-model comparison table | the `S0`/`S1`/`S2` comparison on the common universe, timing and accounting | design level | §8 |

`D1`–`D10` are **mandatory** in any later execution report. A missing diagnostic is a reporting
defect and blocks interpretation claims (`RB8`). No numeric acceptance threshold is attached to any
of them here; adding one requires a dated pre-execution Reviewer authorization.

## 11. Machine-readable mirror

`configs/dlh_wl_p3e_latent_labor_measurement.toml` mirrors this architecture: the latent-object
vocabulary with units and block membership; the accounting identities; the backbone specification;
the measurement families `M1`–`M6`; the wedge registry with the eight required fields; the residual
budget rules; the three model IDs and their comparison rules; the Owner first-wave choices; the
prohibition flags; the diagnostics list; and the inherited-P3C threshold mirror.

**Consistency rule.** Where this document and the TOML could disagree, the value is checked
mechanically and the two must be identical; the TOML contains **no** empirical value and **no** new
numeric threshold, and its inherited P3C threshold block must be byte-identical in value to
`configs/dlh_wl_p3c_bridge_readiness.toml`.

## 12. Invariants

### 12.1 Inherited, unchanged

`C1`–`C21` of the P3C freeze specification remain binding on every later Issue without exception,
together with the P3B conditions `(A1)`–`(A4)`, `(P-L)`, `(C-LINK)`, the region rules `U1`–`U6`, the
weights/harmonization/leakage contract, and the P1B label and support semantics. In particular: the
16 Reviewer numeric thresholds are inherited **unchanged**; `F_all_exact` / `F_search_tol` remain
separated; a finite search still proves neither global uniqueness nor non-existence; exactly 64
executed optimizer starts per window remains frozen; `lambda_ij` and `ell_i` remain two separate
provenance fields tied only by `(C-LINK)`.

### 12.2 New P3E invariants

| # | Statement |
|---|---|
| E1 | real population / employment observations are **measurement anchors**, never truth values of `W_star` or `ell_star`; the identities `W_model = W_census` and `ell_model = ell_official` are forbidden as assumptions |
| E2 | the distance + economic-gap structural backbone of §4 is preserved as the latent-flow backbone and may not be replaced by a data-re-encoding or an ML component |
| E3 | an ML residual component, if ever used, is additive/augmenting, separately identified by declared moments, dimensionality-declared and regularized; it never absorbs a structural term |
| E4 | no numeric undercoverage rate, informal-employment share, labor-law non-compliance share or coverage factor is assumed, borrowed or defaulted anywhere in this architecture |
| E5 | every wedge carries the complete eight-field record of §6.1 before appearing in any equation |
| E6 | `RB1`–`RB8` bind every later design; a design violating them is `RESIDUAL_BUDGET_EXCEEDED__NOT_ADMISSIBLE` and is fail-closed |
| E7 | the labour coverage, hours, efficiency, migration, TFP and government residual blocks may not be simultaneously unrestricted |
| E8 | the government-investment / output block is an explicit economic block with its own anchor or prior and a moment set disjoint from the labour wedges; it may not be an unbounded provincial balancing residual |
| E9 | `S0`, `S1` and `S2` use the same region universe, information timing, macro-accounting definitions and downstream HANK blocks, and the same diagnostics set |
| E10 | no model is selected, preferred, tuned or dropped after outcomes are inspected |
| E11 | H1–H7 remain unresolved here; Issue #83 is the only authority that may resolve or promote them; the Builder never self-promotes an evidence level or a latent-status upgrade |
| E12 | no new numeric threshold, tolerance, seed, weight or acceptance criterion is introduced by this Issue, and no inherited value is changed |
| E13 | the canonical information set is window-start; the window-end nowcast is excluded from the first pass and, if ever used, is a separately labelled design never mixed with the canonical one |
| E14 | the first bounded wave is 2010 Census only, with the 2000 wave excluded initially |
| E15 | `m_star` and `ell_star` are never the label and never a feature of the conditional-share learner, even when a measurement layer disciplines them |
| E16 | `ell_star` may not be equated with any person count; the proxy route requires the explicit `omega` and `q_cov` objects (`U-1`, M4b) |
| E17 | `h_star` and `e_star` may not both be free where their split is unidentified; the split status is reported honestly (`I4`) |
| E18 | a measurement equation is never an identity, and no source-specific equality may be assumed without a separately accepted measurement contract |
| E19 | the architecture may not be used to claim any empirical, causal, welfare, policy, GE, HJB/KFE or household result; it authorizes no execution |
| E20 | the two provenance fields `lambda_ij` and `ell_i` remain separate; nothing in the measurement layer may be used to infer one from the other outside `(C-LINK)` |

## 13. Non-authorization (binding flags)

```
real_data_or_source_read                       = false
dataset_download_scrape_purchase_ingestion      = false
source_adapter_or_crosswalk_created             = false
real_transition_matrix_inspected_or_executed    = false
bridge_executed                                 = false
empirical_estimation_fit_training_calibration   = false
social_insurance_undercoverage_calibrated       = false
labor_law_noncompliance_calibrated              = false
informal_share_assumed                          = false
new_government_investment_residual              = false
hjb_kfe_ge_matlab_household_calls               = 0
pytest_or_full_suite_runs                       = 0
evidence_levels_promoted                        = 0
h_items_resolved_or_promoted                    = 0
successor_issue_created                         = false
pr_merge_close_or_self_acceptance               = false
```

## 14. Decision terminal

PASS:

```
DLH_WL_P3E_LATENT_LABOR_MEASUREMENT_ARCHITECTURE__PASS__READY_FOR_POST_E3_IMPLEMENTATION
```

REVIEW:

```
DLH_WL_P3E_LATENT_LABOR_MEASUREMENT_ARCHITECTURE__REVIEW_REQUIRED
```

PASS **does not authorize real-data implementation**. It means only that the architecture is frozen
and may be used **after** the required H items of Issue #83 are resolved by the human/Owner gate. The
H1–H7 packet remains 7/7 unresolved with 0 promotions.
