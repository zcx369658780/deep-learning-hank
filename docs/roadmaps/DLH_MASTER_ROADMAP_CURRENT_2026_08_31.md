# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.2  
**Date:** 2026-08-31  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** CURRENT SCIENTIFIC ROUTE / OWNER-REVIEWED REBASE  

---

## 0. Project objective

The long-run objective is not to reproduce the historical MATLAB multi-province model and not to replace HJB/KFE with a black-box neural solver.

The target is a **data-to-structural-model calibration engine**:

> Given a country (or monetary/fiscal union), a regional panel, bilateral flow data, household/micro moments where available, and institutional rules, construct and calibrate a multi-region HANK model whose local economic blocks remain structural while interregional connections and selected calibration mappings are learned from data under general-equilibrium discipline.

Conceptually:

\[
\text{regional data + bilateral flows + institutions}
\rightarrow
\text{learned regional networks / parameter mappings}
\rightarrow
\text{regional HANK equilibrium}
\rightarrow
\text{fit + equilibrium diagnostics}
\rightarrow
\text{parameter/network update}
\rightarrow
\text{validated multi-region HANK}.
\]

For year \(t\):

\[
X_t^*(\theta)=T\!\left(X_t^*(\theta);\theta,Z_t\right),
\]

where \(X_t^*\) contains regional household distributions, aggregates, prices, production, fiscal/monetary objects and flow allocations; \(Z_t\) contains observed regional/pair features; and \(\theta\) contains learned structural mappings shared across years where scientifically appropriate.

---

## 1. Scientific rebase after Issues #19–#23

### 1.1 Accepted household foundation

The current accepted two-asset household foundation is:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Accepted repair commit:

`b038db800da3760cebee484b1c7a76bf7c1529d0`

Post-repair identity recorded by Issue #23:

- Git blob: `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`
- SHA-256: `1795718C469FC3B427CAB8E3D5957C133BEAD6EACC9EF0A25A3EDB7211D1A024`

Accepted meaning:

- state space remains two-asset HA `(b,a,z)`;
- HJB/KFE/aggregates are the structural household engine;
- the MATLAB transfer-FOC raw-liquid-derivative mismatch is repaired;
- positive-derivative predecessor behavior is preserved;
- old fixed-bond GE evidence is not a validation of the intended project equilibrium.

### 1.2 Superseded route

The following is **retired as current scientific route**:

- arbitrary `B_hh = B_gov = 1` as the project steady-state target;
- nested cold-start Brent over `(r_a,r_b,L)` as the intended HANK steady-state architecture;
- interpreting a temporary HA stationary solution as an analytic/static DSGE steady-state block.

Issues #19–#22 remain historical evidence about an exploratory closure and numerical diagnostics, but their fixed-bond Option-A closure is not the forward model authority.

### 1.3 Correct steady-state concept

For this project, a regional HANK steady state is a **nested/outer fixed point across blocks**:

\[
\Gamma^{(n)}
\rightarrow
\text{conditional regional HA stationary solves}
\rightarrow
\text{aggregates/flows}
\rightarrow
\text{firm/fiscal/monetary/network updates}
\rightarrow
\Gamma^{(n+1)},
\]

iterated until project-defined convergence and validity gates are satisfied.

The historical MATLAB outer iteration is useful as provenance for this computational architecture, but its hand-designed interregional formulas are not the new model target.

---

## 2. What is hard structure and what is learned

### 2.1 Hard structural economics

Baseline DeepLearning-HANK does **not** let a neural network freely replace:

- household optimization;
- asset laws of motion and constraints;
- HJB equation;
- KFE / distribution law;
- aggregation identities;
- firm technology / factor FOCs;
- accounting identities;
- equilibrium conservation / market consistency;
- genuine HANK nominal equations once that gate is entered;
- fiscal and monetary institutional identities.

These objects may later receive separately reviewed numerical surrogates, but their economic definitions remain authoritative.

### 2.2 First learned object: labor-flow network

The first learned structural object is the interregional labor-service network:

\[
W^L_{ij,t}=f_L(x_{ij,t};\theta_L).
\]

A preferred baseline remains two-stage:

\[
m^L_{i,t}=\sigma(g_L(Z_{i,t};\phi_L)),
\]

\[
W^L_{ij,t}=\frac{\exp s^L_{ij,t}}{\sum_{k\neq i}\exp s^L_{ik,t}},
\]

with actual flow

\[
F^L_{ij,t}=L^{home}_{i,t}\,m^L_{i,t}\,W^L_{ij,t}.
\]

The network is identified first from real origin-destination flow data, not inferred only from GDP fit.

### 2.3 Second learned object: capital-flow network

After the labor network is stable, introduce

\[
W^K_{ij,t}=f_K(x^K_{ij,t};\theta_K).
\]

Before learning `W^K`, use a transparent, interpretable capital-flow baseline and verify accounting/conservation.

### 2.4 Fiscal network is later

Fiscal transfers should initially be observed/exogenous or governed by a transparent central-government rule. A learned `W^G` is a later extension, not a first-generation requirement.

---

## 3. Parameter automation — staged, identified, not all-at-once

The long-run system may automatically calibrate a large share of parameters, but the baseline must separate four parameter classes.

### Tier 0 — theory/definition parameters

Examples:

- asset meanings and constraints;
- utility/technology functional forms;
- HJB/KFE equations;
- accounting definitions;
- nominal-equation structure.

These are specification authority, not free neural outputs.

### Tier 1 — directly observed/institutional inputs

Examples:

- geography and adjacency;
- population;
- statutory tax rates where appropriate;
- observed transfers;
- monetary-regime descriptors;
- regional data definitions.

These should be read from data/config rather than estimated when reliable observations exist.

### Tier 2 — low-dimensional local calibrated parameters

Examples may include regional productivity scales, preference/technology heterogeneity, adjustment-cost or shock-process parameters when data identify them.

These are calibrated against explicit moments with bounds/priors and identification diagnostics.

### Tier 3 — learned mapping parameters

Examples:

- `theta_L` for labor flows;
- later `theta_K` for capital flows;
- later a regional parameter mapping `theta_P`, e.g.

\[
p_{i,t}=g_P(Z_{i,t};\theta_P),
\]

so that a country/region dataset can generate structured local parameter values rather than one unrelated free parameter vector per region-year.

### Joint fine-tuning ceiling

Only after separate identification stages may the project use an equilibrium-constrained objective such as

\[
\mathcal L=
\lambda_F\mathcal L_{flow}
+\lambda_M\mathcal L_{macro}
+\lambda_D\mathcal L_{distribution}
+\lambda_E\mathcal L_{equilibrium}
+\lambda_R\mathcal R(\theta).
\]

Do not jointly free every local/network parameter from random initialization and then call the resulting GDP fit structural identification.

---

## 4. Country-agnostic data contract — target architecture

The eventual model-generator interface should distinguish:

### Node-year data

- output / GDP;
- labor/employment;
- wages/income;
- capital/investment;
- population;
- industrial structure;
- fiscal variables;
- inflation / monetary variables where applicable;
- household distribution moments where available.

### Pair-year data

- origin-destination labor/migration flows;
- bilateral investment/capital exposures when available;
- later trade/fiscal links;
- changing transport/accessibility or policy links.

### Static pair features

- distance;
- adjacency;
- geography/topography;
- stable institutional or border relations.

### System-level institutional configuration

- monetary authority structure;
- fiscal authority structure;
- common currency vs multiple currencies;
- national/union accounting identities;
- policy-rule specification.

This separation is what makes China-31-province, EU-region, or future multi-country applications a common framework rather than separate hand-built models.

---

## 5. Revised implementation route

The project now proceeds through two parallel scientific tracks that later integrate.

# Track A — Regional structural/network learning

## A0 — Two-asset household engine [ACCEPTED FOUNDATION]

Status after Issue #23:

- two-asset household kernel available;
- MATLAB raw-`V_b` transfer-FOC fidelity repaired;
- household numerical caveats remain explicit research objects, not silently erased.

## A1 — Network-ready two-region structural contract [NEXT]

**Design first; no training yet.**

Goal:

- define two regional household modules;
- keep home-region household identity fixed;
- define a hand-specified `W^L` interface;
- define regional firm/fiscal/price interfaces;
- define an outer fixed-point state/update contract;
- define conservation and convergence diagnostics;
- explicitly mark which historical MATLAB spatial formulas are provenance only and which are replaced by network interfaces.

This is **not** a two-province MATLAB reproduction.

## A2 — Two-region hand-specified-flow fixed-point prototype

Implement the A1 contract with deterministic `W^L`.

Pass conditions include:

- both household blocks solve conditionally;
- labor-flow conservation;
- no hidden order dependence between regions;
- regional price feedback works through the outer fixed point;
- deterministic convergence/failure trace;
- no invented `B=1` target;
- all boundary/nonconvergence outcomes are preserved.

## A3 — Labor-flow data schema + transparent baseline

Before neural training:

- freeze OD-year schema;
- freeze feature schema and leakage rules;
- build gravity / transparent benchmark;
- define hold-out years and hold-out region pairs.

## A4 — Learned labor-flow network pretraining

Train `theta_L` only against flow evidence first.

Required diagnostics:

- OD flow error;
- origin-share error;
- destination-share error;
- hold-out-year performance;
- hold-out-pair performance;
- partial effects / feature sensitivity;
- benchmark comparison.

## A5 — 3–5 region equilibrium embedding with learned `W^L`

Embed frozen/pretrained `W^L` into the structural regional fixed point.

First ask whether the learned network survives equilibrium feedback; do not fine-tune jointly before this gate passes.

## A6 — Learned capital network `W^K`

Sequence:

1. transparent capital-flow baseline;
2. data inventory / identification;
3. supervised `W^K`;
4. joint regional equilibrium;
5. identification/ablation diagnostics.

# Track B — Genuine HANK nominal structure

## B1 — Minimal nominal HANK specification

Before claiming the regional system is a genuine HANK model, freeze and validate a minimal nominal block with appropriate source/literature authority, including as required:

- nominal rigidity / Phillips-curve object;
- monetary-policy rule;
- Fisher relation;
- fiscal/transfer/debt treatment;
- consistency with household liquid and illiquid returns.

Do not reuse the superseded arbitrary fixed-bond closure as a shortcut.

## B2 — Nominal-block integration on a small regional system

Integrate the minimal nominal block first on the smallest network-ready system that allows clean diagnostics (two or a few regions).

Only after B1/B2 pass may the project describe subsequent regional experiments as genuine regional HANK policy experiments.

# Integration and scale

## I1 — Equilibrium-constrained fine-tuning

After A4/A5 and B1/B2:

- allow bounded fine-tuning of learned network parameters inside equilibrium;
- preserve direct flow supervision;
- add macro/distribution/equilibrium losses only with explicit weights and ablations;
- use deterministic equilibrium traces and no-overwrite experiment records.

## I2 — Learned regional parameter mapping `theta_P`

Introduce automatic local-parameter generation only after network identification is stable.

Target:

\[
p_{i,t}=g_P(Z_{i,t};\theta_P)
\]

with economic bounds, priors/regularization, and moment-specific identification checks.

This is the first major step toward “input a regional dataset and automatically calibrate the regional HANK.”

## I3 — Full 31-region year-specific equilibrium panel

For each year:

\[
X_t^*=T(X_t^*;\theta,Z_t),
\]

while `theta_L`, later `theta_K/theta_P`, are shared across years as scientifically specified.

Do not model 2010→2011→... as one transition system in the first panel version; each year has its own conditional equilibrium.

## I4 — Automated calibration/model-generator pipeline

Target interface:

`data schema + institutional config -> validated regional model configuration + learned networks + calibrated parameters + equilibrium panel + diagnostics`

The pipeline must report uncertainty/identification warnings and may refuse to generate claims when required data are absent.

## I5 — Policy transmission and welfare

Only after identification, OOS, equilibrium and nominal-HANK gates pass:

- monetary/fiscal shocks;
- regional productivity shocks;
- labor-friction / transport changes;
- regional development policies;
- distributional and welfare effects.

## I6 — EU / multi-country extension

This is a later architecture test, not a near-term implementation target.

EU/common-currency use requires explicit treatment of:

- ECB-level monetary authority;
- country/region fiscal authorities;
- cross-border fiscal/trade/capital structure;
- institutional heterogeneity.

Non-common-currency systems additionally require exchange-rate and multiple monetary-authority modules.

---

## 6. Deep Learning role — explicit boundary

Baseline neural learning is for **hard-to-specify cross-regional mappings and later parameter mappings**.

Baseline does not start with:

- neural HJB replacement;
- GNN/message-passing over the whole economy;
- simultaneous `W^L + W^K + W^G + all local parameters` training;
- GPU-first 31-region experiments;
- black-box imitation of old MATLAB outputs.

Neural operators / HJB surrogates / message passing are later computational extensions once a validated structural baseline exists.

---

## 7. Validation hierarchy

Every major model stage must separately pass:

### Numerical validity

- deterministic/reproducible execution;
- HJB convergence/residual diagnostics;
- KFE mass/non-negativity/stationarity diagnostics;
- explicit boundary diagnostics;
- fixed-point trace and stopping reason.

### Economic validity

- accounting identities;
- labor/capital/flow conservation;
- equilibrium consistency;
- no invented clearing condition;
- nominal/fiscal consistency once HANK gate is active.

### Empirical validity

- flow fit;
- macro moments;
- household/distribution moments where available;
- parameter plausibility.

### Generalization

- hold-out years;
- hold-out pairs/regions;
- perturbation stability;
- policy OOD diagnostics.

A successful code run is not a scientific PASS unless the relevant layer's diagnostics pass.

---

## 8. Immediate next task candidate

No Builder task is activated by this roadmap alone.

The recommended next Issue is a **design/specification task**, tentatively:

`DLH-5A — Freeze Network-Ready Two-Region Structural and Outer-Fixed-Point Contract`

It should:

- consume the accepted two-asset household kernel;
- consume the MATLAB outer-iteration handoff only for computational architecture/provenance;
- explicitly reject replication of the old hand-coded spatial formulas as the new target;
- define the `W^L` interface that later becomes learned;
- define outer state, one-turn order, convergence/failure trace, and conservation gates;
- make no neural-training or empirical-fit claims yet.

---

## 9. Current scientific label

Working label remains:

**Network-Structured Regional HANK (NSR-HANK)**

Long-run methodological description:

> **A data-to-structural-model framework in which regional heterogeneous-agent/New-Keynesian blocks are connected by learned, interpretable interregional networks and calibrated under general-equilibrium, empirical-flow, distributional and institutional constraints.**

This is a research program description, not a novelty claim or final paper title.
