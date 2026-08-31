# DeepLearning-HANK Scientific Handoff — Network-Calibrated Regional HANK Route

**Date:** 2026-08-31  
**Repository:** `zcx369658780/deep-learning-hank`  
**Purpose:** new-session recovery after Issue #23 acceptance and scientific-route rebase.  

---

## 1. Governance

- GitHub `main` = synchronized code/document authority.
- GitHub Issue = sole DSH Builder task authority after publication + activation.
- ChatGPT = independent reviewer / scientific route advisor / task issuer / governance operator.
- DSH = bounded executor.
- Owner = final scientific-direction authority.
- No active Builder Issue at handoff.

Priority:

`Scientific correctness > Experiment reproducibility > Research iteration speed > Git auditability > Documentation completeness`

Read first:

1. `tasks/TASK_INDEX_CURRENT.md`
2. `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
3. `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_08_31.md`
4. current project rules.

---

## 2. Latest accepted scientific state

Issue #23 is accepted/closed.

Accepted commit:

`b038db800da3760cebee484b1c7a76bf7c1529d0`

Accepted classification:

`DLH_4D_R3_MATLAB_TRANSFER_FOC_PARITY_REPAIR_ACCEPTED__OLD_FIXED_BOND_GE_CLOSURE_SUPERSEDED`

Accepted household identity after repair:

- blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`
- SHA-256 `1795718C469FC3B427CAB8E3D5957C133BEAD6EACC9EF0A25A3EDB7211D1A024`

Issue #23 establishes:

- MATLAB transfer FOC uses raw liquid derivative `V_b`; no Python-only positivity guard;
- `1e-6` floor remains for consumption/labor controls only;
- focused committed test evidence: 137 passed;
- frozen 729-point post-repair reclassification: FULL_FINITE 277→499, zero previously-finite regressions, exact repeat reproducibility;
- remaining HJB non-convergence and KFE singularity are preserved diagnostics.

The Issue #23 committed execution reports contain some pre-clarification prose suggesting a later rerun of old Phase E. This prose is historical/stale. Later authoritative Issue comments supersede it.

---

## 3. Critical scientific correction

The old exploratory single-region closure is no longer the project route.

Superseded:

- arbitrary `B_hh=B_gov=1` target;
- nested cold-start Brent over `(r_a,r_b,L)`;
- treating the HA conditional stationary problem as an analytic/static RANK-style steady-state block;
- resuming the 8.77h old Phase-E solve.

The 8.77h run is preserved only as:

`INCONCLUSIVE / SUPERSEDED_CLOSURE_EXECUTION_EVIDENCE`.

Correct project interpretation:

A HANK/HA regional steady state is approached by an outer iterative equilibrium map. Given current prices/policy inputs, each regional HA block solves a conditional stationary HJB/KFE distribution and returns aggregates; regional-flow/firm/fiscal/monetary blocks update prices and states; the updated state is fed back to HA until convergence/validity gates pass.

The historical MATLAB outer iteration is provenance for this **computational architecture**. Its hand-designed interregional spatial equations are not the new-model target.

---

## 4. Project target after route rebase

Working label:

`Network-Structured Regional HANK (NSR-HANK)`

Long-run target:

> Given a country/union regional dataset, bilateral flow data and institutional configuration, automatically generate/calibrate a structural multi-region HANK model with learned interregional networks, selected learned regional parameter mappings, year-specific equilibria and explicit uncertainty/diagnostic output.

Core equation for each year:

\[
X_t^*(\theta)=T(X_t^*(\theta);\theta,Z_t).
\]

Deep Learning does not initially replace HJB/KFE. It first learns hard-to-specify regional mappings.

---

## 5. Structural vs learned components

Hard structure:

- household optimization;
- asset laws/constraints;
- HJB;
- KFE/distribution law;
- firm technology/FOCs;
- accounting/conservation;
- genuine nominal HANK equations once specified;
- fiscal/monetary institutional identities.

First learned object:

\[
W^L_{ij,t}=f_L(x_{ij,t};\theta_L)
\]

for labor-service/migration allocation, supervised by real OD-year flow data.

Second learned object later:

\[
W^K_{ij,t}=f_K(x^K_{ij,t};\theta_K).
\]

Fiscal network `W^G` is later/optional.

Later automatic regional parameter mapping:

\[
p_{i,t}=g_P(Z_{i,t};\theta_P).
\]

Do not train `W^L + W^K + W^G + all local parameters` jointly from scratch.

---

## 6. Parameter identification tiers

- Tier 0: theory/specification definitions — not neural free parameters.
- Tier 1: directly observed/institutional inputs.
- Tier 2: low-dimensional local parameters calibrated to explicit moments with bounds/priors.
- Tier 3: learned network and regional-parameter mappings.

Only after separate identification gates may an equilibrium-constrained joint objective be used.

Potential later objective:

\[
\mathcal L=
\lambda_F\mathcal L_{flow}+
\lambda_M\mathcal L_{macro}+
\lambda_D\mathcal L_{distribution}+
\lambda_E\mathcal L_{equilibrium}+
\lambda_R\mathcal R(\theta).
\]

---

## 7. Current implementation route

### Track A — regional/network structure

A1. **NEXT:** network-ready two-region structural + outer-fixed-point design contract, hand-specified `W^L`, no training.

A2. implement deterministic two-region fixed-point prototype and conservation/failure trace.

A3. freeze OD-year data/feature schema and transparent gravity benchmark.

A4. flow-supervised learned `W^L` with hold-out years/pairs.

A5. embed frozen learned `W^L` into 3–5 region equilibrium.

A6. transparent capital-flow baseline → learned `W^K`.

### Track B — genuine HANK nominal structure

B1. separately freeze minimal nominal HANK specification: price rigidity / Phillips object, monetary rule, Fisher relation, fiscal/debt treatment, household-return consistency.

B2. integrate nominal block on the smallest network-ready regional system.

Only after B1/B2 may policy experiments be called genuine regional HANK experiments.

### Integration/scale

I1. bounded equilibrium-constrained fine-tuning.

I2. learned regional parameter mapping `theta_P`.

I3. 31-region year-specific equilibrium panel with shared learned parameters across years.

I4. automated data-to-model calibration pipeline.

I5. policy/welfare after identification/OOS/equilibrium/nominal gates.

I6. later EU/multi-country extension.

---

## 8. Immediate next Issue candidate

No Issue is active yet.

Recommended next Issue:

`DLH-5A — Freeze Network-Ready Two-Region Structural and Outer-Fixed-Point Contract`

Task type candidate:

`SCIENTIFIC_DESIGN__NETWORK_READY_TWO_REGION_FIXED_POINT_CONTRACT`

It should be design/specification-first and should define:

- two regional structural household interfaces;
- home-region identity;
- hand-specified `W^L` input/output/conservation contract;
- regional firm/fiscal/price interfaces;
- outer state snapshot and update order;
- deterministic convergence/nonconvergence trace;
- household/KFE/boundary validity gates;
- labor-flow conservation and accounting checks;
- explicit list of historical MATLAB spatial formulas that are provenance-only / replaced by network interfaces.

It must not:

- reproduce old multi-province MATLAB as the final target;
- reactivate `B=1` / nested Brent;
- start neural training;
- start 31-region scaling;
- change household equations without separate authority.

---

## 9. Project-source provenance handoff

Important project-source document:

`DeepLearning_HANK_MATLAB_NATIVE_STEADY_STATE_OUTER_ITERATION_SCIENTIFIC_HANDOFF_2026_08_31.md`

Use it for:

- native outer fixed-point architecture;
- household conditional-stationary role;
- batch/Jacobi-style regional HA turn semantics;
- historical convergence/controller provenance;
- identifying old hand-coded spatial objects that the new learned network should replace.

Do **not** treat it as authority to replicate historical spatial formulas.

---

## 10. Next-session startup prompt

```text
你好，请接续 DeepLearning-HANK / Network-Structured Regional HANK 项目。

Repository:
zcx369658780/deep-learning-hank

你的角色：
- ChatGPT independent scientific reviewer / route advisor / GitHub task issuer
- Owner 是最终 scientific authority
- DSH 是 bounded Builder
- GitHub main 是代码与文档事实来源
- GitHub Issue 只有在 publication + activation 后才是 Builder authority

首先 fresh fetch live origin/main，不要假设 handoff SHA 仍是最新。

依次读取：
1. project rules / CURRENT rule index
2. tasks/TASK_INDEX_CURRENT.md
3. docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md
4. docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_08_31.md
5. docs/governance/DLH_HANDOFF_2026_08_31_NETWORK_CALIBRATION_ROUTE.md
6. Issue #23 acceptance/supersession comments and accepted commit as needed
7. Project Source: DeepLearning_HANK_MATLAB_NATIVE_STEADY_STATE_OUTER_ITERATION_SCIENTIFIC_HANDOFF_2026_08_31.md

当前已确认科学路线：
- accepted two-asset HA kernel with Issue #23 MATLAB transfer-FOC repair;
- old arbitrary B_hh=B_gov=1 + nested-Brent single-region GE route is superseded and must not be resumed;
- HANK equilibrium uses outer fixed-point logic across conditional HA and macro/regional blocks;
- historical MATLAB outer loop is provenance for iterative architecture only, not a target for copying old spatial formulas;
- project core is learned interpretable interregional networks, first W^L, later W^K, while household/HJB/KFE/firm/equilibrium definitions remain hard structure;
- long-run target is regional data + bilateral flows + institutional config → automatically calibrated regional HANK model.

当前没有 active Builder Issue。

请先恢复 live state，并基于 CURRENT roadmap 独立判断下一步。若 live state 一致且不需要新的 Owner scientific decision，准备并发布下一张设计任务：
DLH-5A — Freeze Network-Ready Two-Region Structural and Outer-Fixed-Point Contract
但在发布前先向 Owner 简要说明该任务将冻结哪些科学接口；不要直接启动代码实现或 neural training。
```
