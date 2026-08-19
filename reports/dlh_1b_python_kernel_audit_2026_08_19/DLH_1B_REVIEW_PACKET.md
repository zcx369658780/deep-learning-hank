# DLH-1B-R1 Review Packet — Existing Python Kernel Read-only Audit (Corrected)

- Date: 2026-08-19 (R1 correction)
- Author: DSH (bounded Builder)
- Authority: GitHub Issue #4 — `DLH-1B`; authoritative R1 correction comment (2026-08-19 09:11:31).
- Prior candidate: `1d2f3b20fb44680afd93e19ff0aba231a7b47467` — process-clean provenance only; NOT merged, NOT accepted.
- Target repository: `zcx369658780/deep-learning-hank`
- Source repository (READ-ONLY): `zcx369658780/dissertation-ch5-r5-python-model`
- Status: CANDIDATE audit. Acceptance requires fresh-GitHub independent review (ChatGPT).

## 1. Terminal classification

`DLH_1B_R1_AUDIT_TERMINOLOGY_AND_EVIDENCE_CORRECTION_READY_FOR_GPT_REVIEW`

## 2. Baselines and branch

- Fresh **target** `origin/main` SHA: `93a2a3da0fead97f788cbab2e504de81bd863650`
- Fresh **source-repo** `main` SHA: `3039a145f43d419a08999c476cd0d97fd5f8341f` (read-only; canonical remote verified)
- Dedicated R1 branch: `dsh/issue-4-dlh-1b-r1-audit-terminology-evidence-correction-2026-08-19`
- Candidate commit: single evidence commit at branch HEAD (2026-08-19, DSH); hash reported in completion response. Expected delta: exactly the seven paths below, 0 behind / 1 ahead of target baseline.

## 3. Exact changed paths (same seven DLH-1B outputs, corrected)

1. `docs/audits/DLH_1B_EXISTING_PYTHON_KERNEL_PROVENANCE_AND_SCOPE_AUDIT_2026_08_19.md`
2. `docs/audits/DLH_1B_KERNEL_EQUATION_AND_DEPENDENCY_MAP_2026_08_19.md`
3. `docs/audits/DLH_1B_REUSE_REDESIGN_DROP_MATRIX_2026_08_19.csv`
4. `docs/audits/DLH_1B_KERNEL_IO_AND_DIAGNOSTIC_CONTRACT_2026_08_19.md`
5. `reports/dlh_1b_python_kernel_audit_2026_08_19/DLH_1B_SOURCE_FILE_MANIFEST.csv`
6. `reports/dlh_1b_python_kernel_audit_2026_08_19/DLH_1B_REVIEW_PACKET.md`
7. `reports/dlh_1b_python_kernel_audit_2026_08_19/DLH_1B_FORBIDDEN_OPERATION_CHECK.md`

No roadmap, accepted spec, DLH-1A evidence, rule, Task Index, Startup Snapshot, README, or code modified.

## 4. R1 terminology/evidence corrections applied

- **Generator:** all "row-stochastic generator" wording replaced with **continuous-time infinitesimal generator / intensity matrix** (off-diagonal rates >= 0; diagonal = negative total outflow; row sums = 0). The `state_generator` input contract is now defined as a CTMC generator / intensity matrix (NOT a row-stochastic transition matrix).
- **Boundary:** "reflecting boundary" replaced with **state-constraint / no-outward-drift boundary treatment** (boundary derivative from constrained-consumption marginal utility; lower-boundary drift >= 0; upper-boundary drift <= 0). No reflected-process claim is made.
- **Evidence strength:** no "correct for Tier-0"/"exactly the Tier-0 kernel"/"validated" wording remains. Reuse rationale now reads as candidate/reference-only, execution-gated: e.g. "algorithmic structure is compatible with the Tier-0 target", "candidate reference implementation pending DLH-2 execution", "numerical convergence and scientific validity remain unverified".

## 5. Actual household asset / state / control structure found

- **One liquid asset** `a` (uniform grid [0,50], 40 pts); **two productivity states** {0.5,1.5} (symmetric intensities 0.25); controls consumption + drift; **inelastic labor**; **no portfolio choice**; CRRA γ=2; income `(1-τ_l)·wage·z + r_portfolio·a + transfer`.

## 6. HJB / KFE / firm / steady-state implementation summary

- **HJB:** continuous-time, implicit policy iteration w/ pseudo-time-step; upwind FD; Hamiltonian argmax {constrained, forward, backward}; **state-constraint/no-outward-drift boundary** (drift clamped lower>=0 / upper<=0; boundary derivative from constrained-consumption marginal utility); sparse **continuous-time infinitesimal generator** (2-state jumps + upwind asset drift; off-diagonals>=0; diagonal=-outflow; rows sum=0); `true_residual = max|ρV-(u(c)+GV)|`.
- **KFE:** stationary `A'g=0` (row-pin + solve, mass=1, tiny-negative clip, diagnostics); forward implicit one-step KFE for transition.
- **Firm:** **3-factor Cobb-Douglas** with state-owned-services factor `S` (`αg=0.10`) — legacy SOE.
- **Steady-state:** 2-region **symmetric** capital clearing via `brentq` on `capital_residual[0]`, with `W` capital exposure, aggregate goods/NFI/symmetry/W-row residuals, identity-only Fisher nominal.

## 7. Hidden / global-state and legacy-coupling findings

1. `region_count=2` hard-coded (2-region, not single-province); 2. frozen calibration in `validate()`; 3. legacy SOE `αg`/`S`; 4. open-economy accounting (NFI/current account); 5. `W` = capital-exposure (not `W^L`); 6. `diagnostics` subprocess `git` + run-package writes; 7. determinism otherwise good (PCG64, brentq).

## 8. Reuse classification counts (candidate/reference-only, execution-gated)

- `REUSE_AS_REFERENCE_IMPLEMENTATION`: 2 · `REUSE_WITH_ADAPTER`: 4 · `REDESIGN_FOR_NSR_HANK`: 3 · `DROP_FROM_TIER0`: 3 · `UNRESOLVED_NEEDS_EXECUTION_OR_SCIENTIFIC_DECISION`: 3.
- Most important REDESIGN: `steady_state` (→ single-region), `parameters` (→ bounds-validated). Most important DROP for Tier-0: `spatial_links`/`W`, `RegionalAccounts`.

## 9. Proposed Tier-0 migration allowlist candidate (NOT migration authority)

- **Candidate inputs for Tier-0 HA benchmark (pending DLH-2 execution and scientific validation):** `grids.py`, `io_contracts.py`, `household_hjb.py` + `distribution_kfe.py` (with clean adapters), 2-factor `production_block`, lump-sum `fiscal_closure`.
- **Excluded/redesigned for Tier-0:** `region_count=2`, `W`, `αg`/`S`, nominal, regional accounts, AR(1)/transition, frozen calibration.
- Target single-region Tier-0 = one asset, 2-state productivity, CRRA, inelastic labor, 2-factor firm, lump-sum fiscal, capital clearing, deterministic diagnostics — aligning with the accepted DLH-2 spec. **Numerical convergence and scientific validity are not accepted by this audit.**

## 10. Proposed clean I/O contracts (design only)

Household (explicit params, CTMC `state_generator`) → `HouseholdSolution`; KFE (generator/consumption/tolerances) → `DistributionSolution`; firm (2-factor) → `ProductionResult`; steady-state (single-region `R(K)=K-mean_assets(K)`) → `Tier0SteadyState + diagnostics`; diagnostics = residual dataclass + pure reproducibility payload (no subprocess git); config = TOML→dataclass with bounds validation + sha256 + no-overwrite.

## 11. Existing tests mapped to claimed properties (NOT executed)

- `test_household_hjb` → CRRA identity; fixed-price HJB convergence, residual ≤ tol, consumption>0, boundary drift signs, **generator row-sums = 0**.
- `test_distribution_kfe` → mass=1, non-negativity, state marginals [0.5,0.5], moment bounds.
- `test_steady_state_small_grid` → 2-region convergence + full diagnostic PASS + 12-file run package.
- `test_steady_state_reproducibility` → determinism (two solves → identical vectors/arrays).
- `test_aggregate_and_fiscal_block` → factor prices, balanced fiscal, W orientation, zero nominal/current-account residual.
- `test_grids` → grid bounds/dimension; generator row-sums; stationary probs.
- `test_no_model_implementation` / `test_imports` / `test_contracts` → status labels / version / config + no-overwrite rejection.
- **None executed in DLH-1B/R1.** Test presence is D0/D1 source evidence only; it does not prove current passing or scientific validity.

## 12. Unresolved items

1. Numerical convergence of kernels at frozen values — requires later-authorized execution.
2. Genuine-HANK nominal layer (DLH-3) — placeholder today.
3. Transition + AR(1) freeze — defer to DLH-3/DLH-6/7.
4. Interregional links — NSR-HANK `W^L` is a different object, later.

## 13. Forbidden-operation counters (all zero)

- source-repo writes = 0 · code copy/migration = 0 · Python/model/test executions = 0 · package installs = 0 · legacy Matlab reads = 0 · neural training = 0 · Results claims = 0 · governance changes = 0.

## 14. Recommended next gate (suggestion only — no successor creation)

`DLH-2` — single-region Tier-0 HA/Aiyagari computational benchmark, built on the candidate REUSE_WITH_ADAPTER kernels and clean interfaces above, subject to independent review and a separate GitHub Issue.
