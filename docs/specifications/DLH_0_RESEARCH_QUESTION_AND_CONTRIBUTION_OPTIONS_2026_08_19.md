# DLH-0R1 — Research Question and Contribution Options (NSR-HANK corrected)

- Date: 2026-08-19 (R1 revision)
- Author: DSH (bounded Builder)
- Status: CANDIDATE for Owner/ChatGPT decision — planning/specification only.

> R1 correction basis: Issue #2 authoritative revision comment (2026-08-19 07:27:53) + `DLH_MASTER_ROADMAP_INITIAL_2026_08_19.md`. The prior R0 candidate `b79b0310…` is provenance only. No novelty claim is made; all literature references are E0/E1 unless stated.

## A.1 Primary working research question (draft, R1)

> Can the interregional **labor-flow network** of a multi-province economy be identified and represented as an interpretable, trainable network `W^L` — parameterized by time-invariant geography, time-varying regional development, and time-varying pair linkages with parameters shared across years — such that, embedded in structural province-local HA/HANK modules and disciplined by national general equilibrium, it reproduces observed bilateral labor flows and regional equilibrium objects while passing economic-consistency diagnostics (labor conservation, clearing, residuals) and out-of-sample (hold-out year, hold-out pair) validation?

Narrowness check: the question fixes (i) the neural target (`W^L`, interpretable flow weights, not abstract message passing), (ii) the discipline (real origin-destination-year flow data + national GE, not macro aggregates alone), (iii) the structure (province-local modules stay hard), and (iv) the validation (economic residuals + hold-out year/pair). It supports a first paper/model path.

## A.2 Alternative questions (up to two)

**Alternative 1 (economics-constrained household approximation, Route A framing):**
> Can an economics-constrained neural household value/policy approximator achieve smaller HJB-residual error than unconstrained fitting in a minimal HA/HANK household block, and remain stable inside the equilibrium fixed point?

**Alternative 2 (regional equilibrium/distribution, Route B/C framing):**
> Can a learned representation of interregional flows plus distribution state compress the high-dimensional multi-region equilibrium in a way that preserves regional aggregates, market clearing, and transition responses within economic-residual tolerance?

## A.3 Candidate contribution for each

| Question | Candidate contribution | Type |
|---|---|---|
| Primary (`W^L` flow network) | An **identified, interpretable interregional labor-flow network** for a structural regional HA/HANK: flow-supervised identification (O-D-year data), cross-year shared parameters, year-specific equilibria, and a validation contract (hold-out year/pair, economic residuals). Three layers: structural / empirical-identification / computational. | Structural + empirical identification (primary). |
| Alternative 1 (constrained approximator) | Evidence on whether economic constraints materially reduce HJB residual error vs unconstrained neural fitting in a minimal HA/HANK household block. | Methodology + numerical evidence (fallback). |
| Alternative 2 (regional compression) | A compression/representation scheme for multi-region HA/HANK equilibrium that preserves clearing and moments; relevant for 31-province scaling later. | Methodology + computational scaling (deferred). |

## A.4 What would make each question scientifically useful (not merely an engineering speed-up)

- Primary: useful **iff** the flow network is identified from real bilateral flow data (not reverse-engineered from macro aggregates), is interpretable (feature partial effects, gravity-style baseline), generalizes to hold-out years and province pairs, and — when embedded in GE — passes economic-consistency diagnostics. A better GDP fit that destroys the observed migration network is explicitly a failure (identification discipline).
- Alternative 1: useful **iff** economic constraints change *economic* error (HJB residual / equilibrium objects), not only interpolation error, in a minimal but nontrivial household block.
- Alternative 2: useful **iff** compression preserves economically relevant objects (mass, moments, clearing) rather than only reproducing aggregate time series.

## A.5 Evidence still missing before claiming novelty (E-level per project rule)

No novelty claim is made in DLH-0R1. Missing evidence (all `E0` today; must reach `E1`–`E3` through DLH-1A before any novelty statement):

1. Systematic literature inventory: learned interregional/economic flow networks, gravity neural models, flow identification in structural models; structural RL; DeepHAM / neural HJB solvers; neural operators; differentiable equilibrium / implicit layers; spatial/multi-region HA-HANK; distribution compression. — E0 today.
2. Data feasibility evidence: availability and O-D-year structure of Chinese interprovincial labor-flow/migration data (census/intercensal, survey-based bilateral flows). — E0 today (no data access in DLH-0R1).
3. Kernel audit evidence: what the existing single-province Python HJB/firm code actually contains (equations, closures, legacy global state) — DLH-1B deliverable, not available now.
4. Baseline HA benchmark results (analytic limiting cases, small-grid solver) — DLH-2 deliverable.
5. Verified citation-level notes from the local Zotero-workflow root: **none found** in bounded DLH-0 reconnaissance (see evidence source map).

Caveat statement (required): *Any unverified literature claim in this packet is E0/E1 and explicitly caveated; no literature gap is manufactured.*
