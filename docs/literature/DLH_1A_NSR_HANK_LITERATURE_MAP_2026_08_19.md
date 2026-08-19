# DLH-1A — NSR-HANK Literature Map (Evidence Boundary)

- Date: 2026-08-19
- Author: DSH (bounded Builder)
- Authority: GitHub Issue #3 — `DLH-1A: Literature evidence and interprovincial labor-flow data feasibility`
- Status: EVIDENCE ONLY — no novelty claim, no implementation authorization.

> Evidence discipline: E0 = metadata/search; E1 = abstract/official summary; E2 = machine-read full text/substantive sections; E3 = human-verified (stays 0). All findings here are E0/E1 from bounded public-web search; no full-text machine read (E2) and no human verification (E3) were performed. Every entry carries a caveat.

## 1. Scope and method

Bounded public-web search over the eight Issue #3 method families, prioritizing primary sources (arXiv, publishers, RePEc, official statistical/census documentation, dataset owners). Local `D:\Zotero-Analytical-Workflow` bounded text search performed for the same concepts (allowed text types only; see review packet). This is a **recall-oriented boundary map**, not a systematic review and not a novelty claim.

## 2. Method families and material papers

### 2.1 Structural RL for heterogeneous-agent macro

- **Structural Reinforcement Learning for Heterogeneous Agent Macroeconomics** — Y. Yang, C. Wang, A. Schaab, B. Moll (arXiv:2512.18892). E1 (abstract-level). Learns: perceived state / equilibrium policy via RL with state compression; positions RL as the global solution approach for HA macro. Related: "The Trouble with Rational Expectations in Heterogeneous Agent…" (arXiv:2508.20571). URLs: [Semantic Scholar](https://www.semanticscholar.org/paper/52e14aaceb14465d31e306432eeb5d42682fbf03), [RePEc](https://EconPapers.repec.org/paper/arxpapers/2512.18892.htm), [ar5iv HTML](https://ar5iv.labs.arxiv.org/html/2512.18892). Caveat: single-region HA models; does not learn interregional flow networks; local equations are NOT retained as hard modules in the same sense as NSR-HANK.

### 2.2 DeepHAM / global neural solution methods

- **DeepHAM: A Global Solution Method for Heterogeneous Agent Models with Aggregate Shocks** — J. Han, Y. Yang, W. E (Quantitative Economics, 2026; QE2190; arXiv:2112.14377). E1. Learns: global value/policy and distribution; single-region; full distribution state; multi-shock. URLs: [Wiley QE](https://onlinelibrary.wiley.com/doi/10.3982/QE2190), [arXiv](https://arxiv.org/pdf/2112.14377v1). Caveat: replaces the household solver with a global network (opposite of NSR-HANK's "hard local modules + learned links"); no multi-region, no flow data.

### 2.3 Neural HJB / value-policy / master-equation methods

- **Deep-MacroFin: Informed Equilibrium Neural Network for Continuous-Time Economic Models** — J. An et al. (arXiv:2408.10368). E1. Learns: equilibrium-informed value/policy/density. URL: [arXiv](https://arxiv.org/abs/2408.10368v4). Caveat: single-region continuous-time; no interregional network.
- **Deep Learning Solutions to Master Equations for Continuous Time Heterogeneous Agent Macroeconomic Models** — Zhou & Gu (working draft). E0. URL: [draft](https://zzhougu.github.io/drafts/GLMP_20230824.pdf). Caveat: master-equation approach; single-region.
- **Solving Heterogeneous Agent Models with Physics-informed Neural Networks** — (arXiv:2511.20283). E1. URL: [ar5iv](https://ar5iv.labs.arxiv.org/html/2511.20283). Caveat: PINN for HJB/KFE; single-region.
- **A deep learning-driven iterative scheme for high-dimensional [HJB]** (arXiv:2509.02267). E0. Caveat: HJB solver; not spatial.

### 2.4 Surrogate / hybrid finite-difference + deep-learning

- **Sequence-Space Jacobian meets Deep Learning: Exploiting the Random Walk for HANK** — H. Kase (work in progress). E0. URL: [hannokase.com](https://www.hannokase.com/research/deep-learning-mh/). Caveat: hybrid SSJ+DL; single-region; no learned interregional flow network.

### 2.5 Differentiable / implicit equilibrium / neural operators

- **Economics-Inspired Neural Networks with Stabilizing Homotopies** — (arXiv:2303.14802). E1. URL: [arXiv](http://arxiv.org/pdf/2303.14802). Caveat: homotopy stabilization for equilibrium networks; not spatial.
- **Deep Learning for Solving and Estimating Dynamic Models in Economics and Finance** — (arXiv:2605.14493, survey). E1. URL: [HuggingFace](https://huggingface.co/papers/2605.14493). Caveat: survey; scope check for prior learned-economic-network claims.

### 2.6 Spatial / multi-region HA/HANK

- **Balanced and Coordinated Regional Economic Development in China: Insights from Heterogeneous Agent New Keynesian Models** — (SSRN 6028234). E0 (title only). URL: [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6028234). Caveat: China regional HANK; needs E1/E2 read to determine whether links are learned or hand-specified; most directly relevant spatial precedent found.

### 2.7 Learned economic networks / neural gravity / migration-flow

- **Deep learning four decades of human migration** — Gaskin, Abel, et al. (Nature Communications). E1. URL: [Semantic Scholar](https://www.semanticscholar.org/paper/716888600f5e317bb4276f4571d9a0a7c125c591). Caveat: predicts migration flows with DL; NOT embedded in a structural HA/HANK; no market clearing.
- **Human mobility is well described by closed-form gravity-like models learned automatically from data** — Simini et al. (Nature Communications, 2025). E1. URL: [Nature Comms](https://link-hkg.springer.com/article/10.1038/s41467-025-56495-5). Caveat: gravity-like mobility models learned from data; not economic equilibrium.
- **人口怎样在城市间迁移？从引力模型到深度学习** (thepaper/swarma popular-science overview). E0. URL: [swarma](https://swarma.org/?p=35947). Caveat: survey of gravity→DL migration models; non-academic.
- **Agglomeration of knowledge intensive activities…: a gravity model with Spanish labor mobility data** — (ScienceDirect, 2026). E0. URL: [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S1056819026000151). Caveat: static gravity estimation; not learned/structural GE.

### 2.8 Distribution compression / latent-state (later extension only)

- No bounded-search paper yet establishes distribution compression **for multi-region HA/HANK**. Structural RL (2.1) uses state compression (perception), which is the closest mechanism; marked for E3 queue. Verdict: `UNRESOLVED` for the 31-province/message-passing extension.

## 3. What each material paper actually learns (cross-tab)

| Paper | Learned object | Local eqs hard? | Clearing | Region | Real flow data |
|---|---|---|---|---|---|
| Structural RL (2512.18892) | perceived state / policy | partially (perception) | equilibrium-constrained | single | no |
| DeepHAM (2112.14377) | global value/policy/distribution | no (replaces solver) | equilibrium | single | no |
| Deep-MacroFin (2408.10368) | value/policy/density | no | equilibrium | single | no |
| Master equation (Zhou-Gu) | value/distribution (master eq) | no | equilibrium | single | no |
| PINN HA (2511.20283) | HJB/KFE solution | no | equilibrium | single | no |
| Kase SSJ+DL | SSJ operator acceleration | partially | equilibrium | single | no |
| China regional HANK (SSRN 6028234) | (unknown — needs read) | unknown | equilibrium | multi-region | unknown |
| Gaskin et al. (migration DL) | migration flow | n/a (no econ model) | none | multi-region | **yes (bilateral flows)** |
| Simini et al. (gravity-like) | mobility flux model | n/a | none | multi-region | **yes (mobility flows)** |

**Key gap observed in bounded search:** papers that learn interregional/migration flows (2.7) are NOT embedded in structural HA/HANK; papers that do structural/global neural HA-HANK (2.1–2.5) are single-region and do not learn interregional networks from bilateral flow data. The NSR-HANK combination (hard local modules + learned `W^L` + flow data + national GE) is therefore `PARTIAL_PRECEDENT` across components, with no single direct match found in this bounded search.

## 4. Explicit non-claims

- This map does **not** assert a literature gap.
- `NO_PRECEDENT_FOUND_IN_BOUNDED_SEARCH` (used in the boundary matrix) means "not found in this bounded search", not "novel".
- E3 remains 0; the human-verification queue is recorded separately.
