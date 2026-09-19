# Owner route amendment — latent labor measurement architecture

Date: 2026-09-19
Repository: zcx369658780/deep-learning-hank
Base route: DLH-WL-V1-20260918
Authority: Owner explicit approval in ChatGPT project session, 2026-09-19
Live main at publication: 9a81338454e6f006e54da2732342049778fa844d

## 1. Owner-approved amendment

The Owner explicitly approves:

> Real population / employment data are measurement anchors, not truth values of W or ell.
> Preserve the distance + economic-gap structural flow equation as the latent-flow backbone.

This amendment is additive. It does not revoke the locked V1 matrix orientation, household boundaries,
P2 method result, P3A/P3B/P3C evidence/search contracts, or the requirement for separate authorization
before empirical bridge execution or HANK coupling.

## 2. Latent economic objects

The structural model works with latent objects:
- W_star_ij,t : latent conditional destination shares of labor services;
- m_star_i,t  : latent outflow share / transition intensity when required by the accounting closure;
- ell_star_i,t: latent effective origin labor amount.

They are not mechanically equal to census migration shares, registered employment, social-insurance
counts, unit-employment counts, or total population.

A generic effective-labor decomposition may be written:

ell_star_i,t = N_workers_star_i,t * h_star_i,t * e_star_i,t

where N_workers_star is latent employed-worker quantity, h_star is effective hours/intensity, and
e_star is efficiency per hour/worker. This is a modeling decomposition, not a claim that all components
are separately identified in current data.

## 3. Structural latent-flow backbone

Retain a low-dimensional structural mobility backbone based on geographic frictions and economic
incentives. Candidate terms include:
- bilateral distance / adjacency / accessibility;
- destination-origin wage or income gaps;
- destination-origin output/productivity opportunity gaps;
- other pre-registered frictions.

The accepted P2 result that the small neural mapping did not outperform the correctly specified
parametric baseline supports retaining this interpretable backbone. ML may later augment residual
mappings but does not automatically replace the structural score.

## 4. Measurement layer

Observed data are noisy/incomplete measurements of the latent labor economy.

Examples:
- census residence-transition matrices measure people-based multi-year residence transitions;
- labor-force surveys observe employment under their survey frame;
- unit-employment / payroll / social-insurance sources observe only their institutional coverage;
- recorded employment does not automatically measure hours or efficiency labor.

Future measurement equations must distinguish at minimum:
- migration/residence measurement;
- employment-coverage measurement;
- hours/intensity measurement;
- labor-efficiency measurement;
- formal/informal or covered/uncovered employment measurement when supported.

No fixed numerical undercoverage rate is assumed without evidence.

## 5. Measurement anchors, not hard targets

Future empirical work must not impose identities such as:

W_model = W_census
ell_model = ell_official

unless a separately accepted source-specific measurement contract proves the equality.

Official observations may instead enter as anchors / moments / likelihood components with explicit
measurement equations and source-specific uncertainty.

## 6. Identification discipline

A future empirical specification must prevent unrestricted residual absorption.

It may not simultaneously allow all of the following to vary freely without identification or
regularization:
- labor-coverage wedge;
- hours wedge;
- efficiency wedge;
- migration wedge;
- TFP/productivity wedge;
- government-investment/output residual.

Government investment may remain an explicit economic block, but it must not serve as an unlimited
province-by-province balancing residual that can absorb the same moments assigned to labor measurement
wedges.

Every residual/wedge used later must have:
- economic interpretation;
- equation/location;
- data anchor or prior/regularization;
- dimensionality restriction;
- sensitivity/reporting requirement.

## 7. Required future comparison

Before policy interpretation, future real-data work should distinguish at least:

1. STRUCTURAL_ONLY
   distance + economic-gap mobility backbone; OD data are not truth.

2. NAIVE_DATA_PROXY
   observed census/transition/employment proxy used as directly as its semantics allow;
   benchmark only.

3. LATENT_MEASUREMENT_ADJUSTED
   structural latent-flow backbone jointly disciplined by noisy population/employment/macro anchors
   through explicit measurement equations.

## 8. Relationship to P3D / H1-H7

Issue #83 remains the human/source verification gate.

Owner choices approved for the first bounded empirical wave:
- A: first pass may focus on 2010 Census only;
- B: 2000 wave may remain excluded initially;
- C: share-equivalence is a declared benchmark/sensitivity variant, not truth;
- D: employed persons may be used as a declared noisy proxy for ell, not ell_star itself;
- E: canonical prediction design remains window-start.

H1-H4 still require primary-source verification.
H5/H6 are measurement/provenance questions, not identity proofs for latent W_star or ell_star.

## 9. Non-authorization

This amendment does NOT authorize:
- data ingestion;
- real transition-matrix bridge execution;
- empirical estimation;
- HANK policy/welfare results;
- social-insurance undercoverage calibration;
- labor-law noncompliance calibration;
- a fixed informal-employment share;
- a new government-investment residual.

A separate Builder issue may now specify the latent measurement architecture in docs/config only.
