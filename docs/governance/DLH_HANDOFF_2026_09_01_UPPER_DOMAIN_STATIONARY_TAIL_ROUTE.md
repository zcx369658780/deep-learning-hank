# DeepLearning-HANK Scientific Handoff — Upper-Domain / Stationary-Tail Route

**Date:** 2026-09-01  
**Repository:** `zcx369658780/deep-learning-hank`  
**Purpose:** preserve the current scientific state across chat/project-source handoff before the next Builder Issue is published.

---

## 1. Governance state at this handoff

GitHub `main` is the repository/governance authority.

At the start of this handoff the post-DLH-5E synchronized baseline was:

`f1345b9dd866136e19281799e3aa1156768ed29e`

Issue #28 / DLH-5E is ACCEPTED / COMPLETED.

There is currently **NO ACTIVE BUILDER ISSUE**. DSH must remain stopped until a new Issue is explicitly published, Task Index / Startup Snapshot are synchronized, and an authoritative activation comment is present.

Owner has now approved the next scientific route described below. This approval authorizes roadmap/governance synchronization, but it does **not** by itself authorize Builder source mutation.

---

## 2. Latest accepted scientific gate — DLH-5E

Accepted candidate:

`a49c19bbc3257f62bebecc26fe7d88ddcc143d9c`

Accepted reviewer classification:

`DLH_5E_IMPLEMENTATION_VALIDATION_ACCEPTED__D0_BOUNDARY_POLICY_VIOLATION_CONFIRMED__OWNER_HJB_BOUNDARY_DECISION_REQUIRED`

Acceptance level:

`L3_COMMIT_OR_PR_VERIFIED`

Scientific evidence level:

`D2_MACHINE_NUMERICAL_DIAGNOSTIC__HUMAN_REVIEWED_BOUNDARY_POLICY_BLOCKER`

Accepted evidence roots:

- `reports/dlh_5e_conservative_stationary_kfe_validation_2026_09_01/`
- `reports/dlh_5e_conservative_stationary_kfe_validation_r1_2026_09_01/`

---

## 3. Frozen D0 evidence

Canonical D0:

```text
wbar = 1.0
r_a  = 0.03
```

Accepted MATLAB-faithful HJB:

- converged: `True`;
- iterations: `11`;
- final statistic: about `1.67e-08`.

Requested outward rates were reconstructed from post-convergence `mu_b/mu_a` without clipping.

### Upper-b

Three states above `1e-10`:

```text
(19,17,1) ~ 0.115760699
(19,18,1) ~ 0.271868724
(19,19,1) ~ 0.353747704
```

### Upper-a

28 states above `1e-10`, all on `a_index=19`.

Corrected maximum:

```text
(b,a,z) = (14,19,1)
rate ~= 0.264071883
```

Lower-b and lower-a have no material outward request on D0.

A mechanically conservative candidate generator constructed from admitted in-grid transitions satisfies:

```text
row-sum max abs           = 6.106227e-16
negative offdiag magnitude = 0.0
nnz                        = 3114
```

This proves that row-sum conservation can be restored mechanically, but it does not validate the HJB policy because HJB still requests materially outward movement at the upper numerical domain.

Accordingly, stationary/nullspace/pin/aggregate/anchor gates were not reached and no clipped density was accepted.

---

## 4. What remains accepted about KFE contamination

Issue #27 remains controlling scientific authority:

```text
Q^T g = 0
sum_s g_s * (db*da) = 1 per discrete z state
g_s >= 0 up to tolerance
```

Singularity of `Q/Q^T` is expected.

MATLAB-style contamination / component pinning remains allowed in principle, but acceptance requires:

- conservative generator;
- stationary recurrent-class/nullspace evidence;
- one-dimensional stationary nullspace on the canonical unique-stationary fixture;
- pin admissibility (`g_star[n] != 0` for component pin `g_n=c>0`);
- ORIGINAL `Q^T g` residual pass;
- mass and non-negativity pass;
- agreement across at least two valid deterministic pins;
- default MATLAB parity pin valid before future production use.

Contamination is a component-pinning scale device followed by separate mass normalization; it is not itself the total-mass normalization equation.

---

## 5. External multi-province review incorporated

A neighboring GPT adviser reviewed the DeepLearning-HANK route using a separate multi-province HANK Python reconstruction project.

The following corrections are now incorporated:

1. The neighboring project should be described as a **highly mature source-faithful multi-province reconstruction under active MATLAB–Python stationary parity adjudication**, not as fully parity accepted.
2. An artificial upper asset limit is not necessarily an economic state constraint, but any finite numerical domain still needs a coherent HJB boundary closure.
3. Persistent outward drift on wider grids does not automatically prove the HJB equation is wrong; stationary-tail existence / high-wealth mean reversion must also be considered.
4. Enlarging the grid does not mathematically repair a non-conservative generator construction. Generator conservativity must be guaranteed by construction.
5. A mechanically clipped conservative KFE cannot be accepted if it no longer corresponds to the HJB controlled process.
6. Grid adequacy should be judged by convergence of boundary influence, not by requiring maximum outward drift to become exactly zero.
7. Probability-weighted outward flux and near-boundary mass are required alongside max-drift diagnostics.
8. Cross-project 31-province work should first use frozen household input/price snapshots rather than repeated full-GE grid sweeps.
9. Reuse should be contract/module/oracle reuse, not blind repository merge.
10. The validation hierarchy should permanently retain `2-region -> 3–5 province -> 31 province` levels.
11. Future regional parity must separately inspect continuous-state parity and discrete-controller branch parity.
12. The first learned network should initially be a source spatial-rule surrogate before empirical flow replacement, to reduce endogeneity/double-counting risk.

---

## 6. Owner-approved next route

Owner explicitly approves:

> **Bounded Upper-Domain Adequacy + Stationary-Tail Diagnostic before any HJB boundary-law rewrite.**

The next experiment must:

- preserve accepted HJB equations;
- never clip outward drift to obtain PASS;
- never tune domain adaptively to obtain PASS;
- separate domain extent from resolution;
- test whether truncation influence converges to a negligible/stable level;
- consider stationary-tail existence / asymptotic behavior if it does not.

The new master roadmap is:

`docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`

---

## 7. Candidate next Builder gate — DLH-5F (NOT YET PUBLISHED)

Tentative task class:

`SCIENTIFIC_DIAGNOSTIC__UPPER_DOMAIN_ADEQUACY_AND_STATIONARY_TAIL`

No Issue exists yet at this handoff.

### Core experimental design

Use a small pre-frozen set of upper-domain extents and a separate resolution check.

When upper extent is increased, increase grid-point counts so that `db/da` stay approximately comparable. Do not confound extent with coarse resolution.

No adaptive refinement.

### Required diagnostics

#### Policy

- upper `a` / `b` outward max;
- quantiles where meaningful;
- violation counts/shares;
- complete offending states;
- lower-boundary regression diagnostics.

#### Distribution/tail

Only when a scientifically admissible stationary process is available under the same HJB/KFE closure:

- boundary mass;
- near-boundary mass (definition frozen in task);
- probability-weighted upper outward flux;
- recurrent-class/nullspace structure;
- original stationary residual.

#### Interior stability

Compare policies on a common interior domain across wider asset domains.

#### Aggregates

Only after stationary validation:

`C,L,A,B`

and convergence across domain/resolution.

### Required decision outcomes

Possible scientific outcomes include:

- `GRID_UPPER_DOMAIN_INADEQUATE__TRUNCATION_INFLUENCE_CONVERGES_WITH_EXPANSION`;
- `STATIONARY_TAIL_NOT_ESTABLISHED__HIGH_WEALTH_MEAN_REVERSION_REVIEW_REQUIRED`;
- `FINITE_DOMAIN_HJB_KFE_CLOSURE_REDESIGN_REQUIRED`;
- different outcomes for liquid vs illiquid dimensions.

The exact terminal vocabulary must be frozen in the eventual Issue before execution.

---

## 8. HJB/KFE consistency law for all future work

Binding principle:

```text
HJB boundary policy <=> KFE boundary transition law
```

The accepted economic/numerical process must be the same in backward and forward equations.

Do not:

- retain an outward HJB policy;
- independently impose a no-outflow KFE process;
- and call the resulting density the stationary distribution of the original HJB problem.

If a new upper-boundary closure is eventually required, the HJB derivative/policy law and KFE transition law must be designed and reviewed together.

---

## 9. Planned cross-project benchmark

A later/separate cross-project diagnostic should be:

`31_PROVINCE_HOUSEHOLD_UPPER_DOMAIN_AUDIT`

Preferred workflow:

```text
frozen steady-state household price/input snapshots
-> 31 independent household boundary/tail diagnostics
```

rather than repeated full 31-province outer-equilibrium grid sweeps.

The neighboring multi-province project is a reference/source benchmark under active parity adjudication, not yet an unquestioned production oracle.

---

## 10. Regional scale hierarchy

Retain permanently:

```text
2-region unit fixture
-> 3–5 province integration fixture
-> 31-province empirical/source benchmark
```

The two-region fixture remains the primary human-auditable accounting/orientation test bed.

For future outer-loop comparisons, separately evaluate:

- continuous numerical state differences;
- discrete controller branch/reset/threshold differences.

---

## 11. Revised Deep Learning route

No neural training is authorized yet.

When household/regional equilibrium is trusted:

### L0 — source spatial-rule surrogate

Learn the validated source spatial mapping first under explicit source inputs and preserve orientation/conservation/accounting.

### L1 — structural learned spatial rule

Only then replace hand-coded structure with an interpretable learned mapping.

### L2 — empirical OD-flow learning

Only later introduce real flow targets with explicit endogeneity/double-counting safeguards.

The two-stage origin-outflow + conditional-destination decomposition remains a DeepLearning-HANK redesign candidate, not a claim of unique MATLAB fidelity.

---

## 12. Scientific ceiling at handoff

Until DLH-5F and subsequent household/KFE revalidation are complete, do not:

- modify the accepted HJB equations merely to remove D0 violations;
- accept clipped `Q_c` density;
- restore old row-295 aggregates;
- run two-region economic Results as validated equilibrium;
- start learned `W^L` training;
- run policy/welfare claims;
- claim full 31-province MATLAB–Python parity is already accepted;
- move directly to nominal HANK integration.

---

## 13. Immediate continuation instruction for a future chat

A new ChatGPT session should:

1. fresh-fetch GitHub `main`;
2. read all CURRENT project rules;
3. read `tasks/TASK_INDEX_CURRENT.md`;
4. read `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`;
5. read `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`;
6. read this handoff;
7. confirm there is no active Builder Issue;
8. only then design/publish the exact DLH-5F diagnostic Issue if Owner/project-source synchronization is complete.

Do not infer authority from chat text alone.
