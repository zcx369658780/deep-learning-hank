# DLH-1A-R1 — NSR-HANK Literature Map (Evidence Boundary, Corrected)

- Date: 2026-08-19 (R1 correction)
- Author: DSH (bounded Builder)
- Authority: GitHub Issue #3 — `DLH-1A`; authoritative R1 correction comment (2026-08-19 08:12:28).
- Prior candidate: `2a04a737bd6aa62b00e8c39a9e2a2d7e3b22b021` — process-clean provenance only; NOT merged, NOT accepted.
- Status: EVIDENCE ONLY — no novelty claim, no implementation authorization.

> Evidence discipline: E0 = metadata/search; E1 = abstract/official summary; E2 = machine-read substantive sections; E3 = human-verified (stays 0). R1 corrections reflect primary-source descriptions provided/confirmed in the authoritative review; no E2 full-text machine read was newly performed by the Builder (E2 = 0 remains).

## 1. Scope and method

Bounded public-web search over the eight Issue #3 method families, prioritizing primary sources. R1 applies the authoritative corrections: Owner prior work is excluded from external-precedent reasoning; geodoi/CMDS data classifications corrected; DeepHAM/master-equation/Structural-RL descriptions aligned to primary sources. This is a **recall-oriented boundary map**, not a systematic review and not a novelty claim.

## 2. Method families and material papers

### 2.1 Structural RL for heterogeneous-agent macro (E1, primary abstract)

- **Structural Reinforcement Learning for Heterogeneous Agent Macroeconomics** — Y. Yang, C. Wang, A. Schaab, B. Moll (arXiv:2512.18892). E1. Mechanism (abstract-level, corrected): **replaces the cross-sectional distribution with a low-dimensional set of prices as state variables, and learns equilibrium price dynamics from simulated paths**; includes a HANK application with a forward-looking Phillips curve. URLs: [Semantic Scholar](https://www.semanticscholar.org/paper/52e14aaceb14465d31e306432eeb5d42682fbf03), [RePEc](https://EconPapers.repec.org/paper/arxpapers/2512.18892.htm), [ar5iv HTML](https://ar5iv.labs.arxiv.org/html/2512.18892). Caveat: single-region HA models; does not learn interregional flow networks; local equations are NOT retained as hard modules in the NSR-HANK sense. Related: "The Trouble with Rational Expectations in Heterogeneous Agent…" (arXiv:2508.20571, E0).

### 2.2 DeepHAM / global neural solution methods (E1, primary abstract corrected)

- **DeepHAM: A Global Solution Method for Heterogeneous Agent Models with Aggregate Shocks** — J. Han, Y. Yang, W. E (Quantitative Economics, 2026; QE2190; arXiv:2112.14377). E1. Corrected description: **the distribution is approximately represented by a set of optimal generalized moments (not the full distribution state); neural networks approximate value/policy functions.** Single-region; multi-shock. URLs: [Wiley QE](https://onlinelibrary.wiley.com/doi/10.3982/QE2190), [arXiv](https://arxiv.org/pdf/2112.14377v1). Caveat: replaces the household solver with global networks (opposite of NSR-HANK "hard local modules + learned links"); no multi-region, no flow data.

### 2.3 Neural HJB / value-policy / master-equation methods

- **Global Solutions to Master Equations for Continuous Time Heterogeneous Agent Macroeconomic Models** — J. Gu, M. Laurière, S. Merkel, J. Payne (arXiv:2406.13726). E1 (PRIMARY master-equation source). Corrected description: **represents the value function with a neural network after finite-dimensional distribution approximations; demonstrates macro and spatial examples.** URLs: [arXiv HTML](https://ar5iv.labs.arxiv.org/html/2406.13726), [RePEc](https://ideas.repec.org/p/arx/papers/2406.13726.html). Caveat: neural value-function solving; distribution finite-dimensionally approximated; not the NSR-HANK learned-flow design. Note: the older Zhou–Gu "Deep Learning Solutions to Master Equations…" draft (GLMP_20230824) remains provenance only, superseded as the primary anchor by arXiv:2406.13726.
- **Deep-MacroFin: Informed Equilibrium Neural Network for Continuous-Time Economic Models** — J. An et al. (arXiv:2408.10368). E1. URL: [arXiv](https://arxiv.org/abs/2408.10368v4). Caveat: single-region continuous-time; no interregional network.
- **Solving Heterogeneous Agent Models with Physics-informed Neural Networks** — (arXiv:2511.20283). E1. URL: [ar5iv](https://ar5iv.labs.arxiv.org/html/2511.20283). Caveat: PINN for HJB/KFE; single-region.

### 2.4 Surrogate / hybrid finite-difference + deep-learning

- **Sequence-Space Jacobian meets Deep Learning: Exploiting the Random Walk for HANK** — H. Kase (work in progress). E0. URL: [hannokase.com](https://www.hannokase.com/research/deep-learning-mh/). Caveat: hybrid SSJ+DL; single-region; no learned interregional flow network.

### 2.5 Differentiable / implicit equilibrium / neural operators

- **Economics-Inspired Neural Networks with Stabilizing Homotopies** — (arXiv:2303.14802). E1. URL: [arXiv](http://arxiv.org/pdf/2303.14802). Caveat: homotopy stabilization; not spatial.
- **Deep Learning for Solving and Estimating Dynamic Models in Economics and Finance** — (arXiv:2605.14493, survey). E1. URL: [HuggingFace](https://huggingface.co/papers/2605.14493). Caveat: survey.

### 2.6 Spatial / multi-region HA/HANK — external precedent (R1 corrected)

- **Owner prior work (NOT external precedent):** `Balanced and Coordinated Regional Economic Development in China: Insights from Heterogeneous Agent New Keynesian Models` (SSRN 6028234) = **Chenxin Zhang's own prior dissertation / multi-provincial HANK work (Jinhe Center, Xi'an Jiaotong University).** Reclassified `OWNER_PRIOR_WORK / PROJECT_PROVENANCE`. Used only to document the project's historical baseline/prior mechanisms, NOT as independent external multi-region HANK precedent.
- **External spatial/multi-region HA/HANK literature boundary: `UNRESOLVED`.** No independent external precedent has been verified in bounded search after removing Owner prior work.

### 2.7 Learned economic networks / neural gravity / migration-flow

- **Deep learning four decades of human migration** — Gaskin, Abel, et al. (Nature Communications). E1. URL: [Semantic Scholar](https://www.semanticscholar.org/paper/716888600f5e317bb4276f4571d9a0a7c125c591). Caveat: predicts migration flows with DL; NOT embedded in a structural HA/HANK; no market clearing.
- **Human mobility is well described by closed-form gravity-like models learned automatically from data** — Simini et al. (Nature Communications, 2025). E1. URL: [Nature Comms](https://link-hkg.springer.com/article/10.1038/s41467-025-56495-5). Caveat: gravity-like mobility models learned from data; not economic equilibrium.
- **人口怎样在城市间迁移？从引力模型到深度学习** (thepaper/swarma popular-science overview). E0. URL: [swarma](https://swarma.org/?p=35947). Caveat: survey of gravity→DL migration models; non-academic.

### 2.8 Distribution compression / latent-state (later extension only)

- No bounded-search paper yet establishes distribution compression **for multi-region HA/HANK**. Structural RL (2.1) uses low-dimensional price state (perception), the closest mechanism. Verdict: `UNRESOLVED` for the 31-province/message-passing extension.

## 3. What each material paper actually learns (cross-tab, R1 corrected)

| Paper | Learned object | Local eqs hard? | Clearing | Region | Real flow data |
|---|---|---|---|---|---|
| Structural RL (2512.18892) | low-dimensional price state + price dynamics | no (prices as state) | equilibrium-constrained | single (+ HANK app) | no |
| DeepHAM (2112.14377) | value/policy (distribution ≈ optimal generalized moments) | no (replaces solver) | equilibrium | single | no |
| Master equation (Gu et al. 2406.13726) | value function (finite-dim distribution approx) | no | equilibrium | single + spatial examples | no |
| Deep-MacroFin (2408.10368) | value/policy/density | no | equilibrium | single | no |
| Kase SSJ+DL | SSJ operator acceleration | partially | equilibrium | single | no |
| Gaskin et al. (migration DL) | migration flow | n/a | none | multi-region | **yes (bilateral flows)** |
| Simini et al. (gravity-like) | mobility flux model | n/a | none | multi-region | **yes (mobility flows)** |

**Key gap (R1 recomputed):** papers that learn interregional/migration flows (2.7) are NOT embedded in structural HA/HANK; papers that do structural/global neural HA-HANK (2.1–2.5) are single-region and do not learn interregional networks from bilateral flow data; and the only multi-region China HANK candidate found is **Owner prior work**, excluded from external precedent. The NSR-HANK combination therefore has **partial precedent across components and no verified external direct match** in bounded search.

## 4. Explicit non-claims

- This map does **not** assert a literature gap.
- `NO_PRECEDENT_FOUND_IN_BOUNDED_SEARCH` means "not found in this bounded search", not "novel".
- E3 remains 0; the human-verification queue is recorded separately.
