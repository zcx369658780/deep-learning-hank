# DLH-0 — Research Question and Contribution Options

- Date: 2026-08-19
- Author: DSH (bounded Builder)
- Status: CANDIDATE for Owner/ChatGPT decision — planning/specification only.

## A.1 Primary working research question (draft)

> For a minimal continuous-time heterogeneous-agent model with a small number of regions, can a neural **surrogate/accelerator** trained on a transparent small-grid reference solver approximate the household value/policy block (and later equilibrium objects) such that the neural model passes **economic-residual diagnostics** (HJB/KFE residual, market clearing, mass, boundary) with a measurable, auditable speedup on repeated experiments — i.e., a neural method that is scientifically auditable rather than a black box?

Narrowness check: it fixes (i) the neural role (surrogate/accelerator), (ii) the ground truth (project-owned transparent solver, not legacy Matlab), (iii) the acceptance criterion (economic residuals, not training loss), and (iv) the object (household value/policy block first). It supports a first paper/model path.

## A.2 Alternative questions (up to two)

**Alternative 1 (route A framing):**
> Can a neural value/policy function approximator, trained with explicit economic constraints (monotonicity, concavity, borrowing-boundary feasibility), achieve smaller HJB-equation residual error than unconstrained training in a minimal continuous-time HANK household block, and remain stable inside the equilibrium fixed point?

**Alternative 2 (route C/regional framing):**
> Can a learned latent representation faithfully compress the household × region distribution state of a small multi-region HANK such that equilibrium aggregates and transition responses are preserved within economic-residual tolerance?

## A.3 Candidate contribution for each

| Question | Candidate contribution | Type |
|---|---|---|
| Primary (surrogate/accelerator) | An **auditable neural-accelerator validation contract** for HANK: definition of neural-vs-solver error separation, economic-residual gates, and a benchmarkable speedup measure. | Methodology (primary), with the economic object being the household block of a minimal HANK. |
| Alternative 1 (constrained approximator) | Evidence on whether economic constraints materially reduce HJB residual error vs unconstrained neural fitting — a concrete, testable claim about neural methods in HJB-based models. | Methodology + numerical evidence. |
| Alternative 2 (distribution compression) | A distribution-compression scheme for regional HANK with moment/mass-preserving guarantees; relevant for scaling to province dimension. | Methodology + computational scaling (later stage). |

## A.4 What would make each question scientifically useful (not merely an engineering speed-up)

- Primary: scientifically useful **iff** the project produces (a) a reproducible, solver-anchored benchmark; (b) a formal separation between prediction error and economic residual; (c) OOD/sensitivity characterization; (d) a public, reusable diagnostic suite. Speed alone is not a scientific contribution; the validation methodology is.
- Alternative 1: useful **iff** constrained neural fitting is shown to change *economic* error (HJB residual / equilibrium objects), not just interpolation error, in a minimal but nontrivial HANK household block.
- Alternative 2: useful **iff** the latent representation is shown to preserve economically relevant objects (mass, moments, clearing) rather than only reproducing aggregate time series.

## A.5 Evidence still missing before claiming novelty (E-level per project rule)

No novelty claim is made in DLH-0. Missing evidence (all currently `E0`/absent; must reach `E1`–`E3` through a DLH-1 literature gate before any novelty statement):

1. Systematic literature inventory on neural methods for heterogeneous-agent models: DeepHAM / deep HJB solvers / neural operators for macro-equilibrium (method families, benchmark setups, reported residual/error metrics). — E0 today.
2. Evidence on whether neural HJB/value approximators are standard practice and what failure modes are documented (boundary handling, OOD, equilibrium fixed-point interaction). — E0 today.
3. Multi-region / spatial HANK computational-scaling literature (sequence-space, heterogeneous-agent spatial models) to position the regional extension. — E0 today.
4. Verified citation-level notes (E2/E3) from the local Zotero-workflow root: **none found** in bounded DLH-0 reconnaissance (see evidence source map).
5. Baseline HANK benchmark results (analytic limiting cases, small-grid solver) — to be produced in DLH-2, not DLH-0.

Caveat statement (required): *Any unverified literature claim in this packet is E0/E1 and explicitly caveated; no literature gap is manufactured.*
