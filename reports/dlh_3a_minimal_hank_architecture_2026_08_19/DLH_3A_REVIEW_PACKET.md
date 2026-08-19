# DLH-3A Review Packet — Minimal Genuine Single-Region HANK Architecture / Equation Freeze

- Date: 2026-08-19
- Author: DSH (bounded Builder)
- Authority: GitHub Issue #10 — `DLH-3A: Minimal genuine single-region HANK architecture and equation freeze` (state: OPEN; 1 authoritative synchronization comment read fresh)
- Status: **CANDIDATE (specification only)**. Acceptance requires fresh-GitHub independent review (ChatGPT) + Owner scientific-direction awareness.
- Evidence class: **SPECIFICATION ONLY — no model code, no numerical result, no D2 HANK evidence.**

## 1. Terminal classification

`DLH_3A_MINIMAL_HANK_ARCHITECTURE_READY_FOR_GPT_OWNER_REVIEW`

## 2. Baseline / Issue / branch / commit

- Fresh baseline `origin/main` SHA: `d5e20f895ccec7ef116f777039aa1680025d0bcf`
- Issue #10 title/status: `DLH-3A: Minimal genuine single-region HANK architecture and equation freeze` — OPEN
- Dedicated branch: `dsh/issue-10-dlh-3a-minimal-hank-architecture-2026-08-19`
- Candidate commit: single coherent commit at branch HEAD (2026-08-19, DSH); hash reported in completion response. Expected delta: exactly the six allowlisted paths, 0 behind / 1 ahead.

## 3. Exact changed paths (six allowlisted outputs)

1. `docs/specifications/DLH_3_MINIMAL_GENUINE_HANK_ARCHITECTURE_2026_08_19.md`
2. `docs/specifications/DLH_3_ASSET_FISCAL_AND_NOMINAL_SEMANTICS_CONTRACT_2026_08_19.md`
3. `docs/specifications/DLH_3_STEADY_STATE_AND_DYNAMIC_EQUATION_CONTRACT_2026_08_19.md`
4. `docs/specifications/DLH_3_VALIDATION_LIMITING_CASE_AND_GRID_CONTRACT_2026_08_19.md`
5. `reports/dlh_3a_minimal_hank_architecture_2026_08_19/DLH_3A_REVIEW_PACKET.md`
6. `reports/dlh_3a_minimal_hank_architecture_2026_08_19/DLH_3A_FORBIDDEN_OPERATION_CHECK.md`

**No other tracked path modified** — `src/**`, `configs/**`, `tests/**`, `project_rules/**`, `tasks/**`, Startup Snapshot, README, roadmap, handoff, and all accepted DLH-0/1/2 reports/evidence untouched.

## 4. Exact files read (GitHub / repository, fresh origin/main)

- `docs/governance/DLH_SESSION_HANDOFF_AFTER_TIER0_NUMERICAL_ROBUSTNESS_COMPLETE_2026_08_19.md`
- `project_rules/PROJECT_RULE_INDEX_CURRENT.md` + all CURRENT rules (incl. the updated `PROJECT_RULE_MODEL_DEVELOPMENT_DIAGNOSTIC_GATES_CURRENT.md` with stage-numbering disambiguation)
- `tasks/TASK_INDEX_CURRENT.md` (Status `ACTIVE_GITHUB_ISSUE_10__DLH_3A_MINIMAL_HANK_ARCHITECTURE`)
- `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
- `docs/roadmaps/DLH_MASTER_ROADMAP_INITIAL_2026_08_19.md`
- Accepted DLH-0 constitution materials (Issue #2 accepted R1 constitution)
- Accepted DLH-2A household/HJB/KFE contracts and code (interface semantics)
- Accepted DLH-2B firm/fiscal/steady-state contracts and code (interface semantics)
- Issue #9 accepted robustness reports/results (`reports/dlh_2c_b2_fixed_domain_grid_2026_08_19/…`) as numerical-reference provenance
- GitHub Issue #10 body + all authoritative comments (1 synchronization comment) via authenticated `gh api`

## 5. Architecture summary (one paragraph)

The DLH-3A minimal genuine single-region HANK validation economy is a continuous-time economy with (i) a heterogeneous household block on a single liquid risk-free financial asset `a` with a two-state idiosyncratic productivity CTMC, CRRA consumption utility, and **endogenous static labor supply** (control, not state); (ii) labor-based production `Y = A N` with monopolistic competition markup `μ` and **Rotemberg** price adjustment (NKPC with frozen continuous-time timing/sign convention); (iii) a monetary block (nominal rate `i_t`, inflation `π_t`, real return `r_t`, Fisher, Taylor rule with `π̄=0`); (iv) a fiscal/bond block (exogenous bond supply `B_t`, labor tax, lump-sum transfer, lump-sum dividend incidence, asset-market clearing `A_t = B_t`); and (v) exact computed residual objects for HJB, KFE, asset/labor/goods markets (incl. Rotemberg cost), fiscal, profits, NKPC, Fisher and Taylor. The liquid asset is explicitly **not** Tier-0 productive capital; steady-state reduction preserves the accepted stationary HJB/KFE family with a documented re-interpretation of income terms; dynamic household/KFE response and full NK GE are separate successor subgates (DLH-3B/3C/3D/3E), and Tier-0 `[0,200]` domain adequacy is **not** inherited by HANK.

## 6. State / control / price / aggregate / residual table

| Category | Objects |
|---|---|
| Household state | `a` (liquid financial asset), `z ∈ {z_l, z_h}` (2-state CTMC) |
| Controls | consumption `c ≥ 0`; **endogenous static labor `n ∈ [0, n̄]`** |
| Prices | real wage `w_t`; real liquid return `r_t`; nominal rate `i_t`; inflation `π_t`; real marginal cost `mc_t` |
| Aggregates | `Y_t, N_t, A_t, C_t, Π_t, B_t, tr_t, μ` |
| Residuals | HJB, KFE/mass, asset, labor, goods (incl. Rotemberg cost), fiscal, profits, NKPC, Fisher, Taylor |

## 7. Liquid-asset semantic and why it is not Tier-0 productive capital

- `a` is a liquid, risk-free real financial claim (government-bond counterpart) paying `r_t`; it appears only in the household budget and asset-market clearing.
- Tier-0's asset was productive capital entering the Cobb-Douglas production function (`alpha_k`, `delta`); accepted Tier-0 code (`economics/firm.py`, `solvers/steady_state.py`) is **not** silently reinterpreted — the DLH-3 cash flow replaces Tier-0's `(1−τ_l)w z + r a + transfer` with `(1−τ_l) w z n + r a + tr + Π` and the asset is financial, not productive. Consequently Tier-0 domain adequacy is not inherited (re-established in DLH-3E).

## 8. Endogenous-labor FOC semantics

`v′(n) = (1−τ_l) w_t z V_a` with `v(n) = χ n^(1+1/φ)/(1+1/φ)`; labor is a **static control** — no additional state dimension; aggregate effective labor `N_t = ∫ z n dg` enters production and the labor market.

## 9. Rotemberg / NKPC timing convention (frozen)

`π̇_t = ρ π_t − κ (mc_t − 1/μ)`, `κ = (ε−1)/φ_p > 0`; `π_t = Ṗ_t/P_t`; `π̇_t = dπ_t/dt`; sign: `mc > 1/μ` ⇒ `π̇ > 0` at `π=0`; steady state `π=0`, `mc=1/μ`; `P_t` continuous (no jump); exact `κ` convention frozen at DLH-3A.

## 10. Fisher / Taylor timing convention (frozen)

`i_t = r_t + π_t` (exact continuous-time Fisher; residual `i − r − π`); Taylor `i_t = r̄ + π_t + φ_π(π_t − π̄)`, `π̄ = 0`, `φ_π > 1`; steady state `π*=0`, `i*=r*=r̄`; zero-shock consistency at `π=π̄=0`.

## 11. Fiscal / bond / dividend accounting convention (frozen)

Bonds: exogenous `B_t`; asset-market clearing `A_t = B_t`; tax revenue `T_t = τ_l w_t N_t`; government budget `r_t B_t + tr_t = T_t`; transfer closure `tr_t = T_t − r_t B_t`; profits `Π_t = Y_t − w_t N_t − (φ_p/2)π_t²Y_t` distributed lump-sum per capita; every residual computed (never zeroed by labeling).

## 12. Steady-state reduction

`∂_t V = 0`, `∂_t g = 0` ⇒ stationary HJB `ρ V = max{U + V_a ȧ + Q V}` and stationary KFE `Gᵀ g = 0` — the accepted Tier-0 stationary HJB/KFE family with the documented HANK cash-flow re-interpretation.

## 13. Future gate boundaries (3B/3C/3D/3E)

- **DLH-3B** steady-state structural kernel (zero-inflation/zero-shock; a 3B PASS is not full dynamic HANK validation);
- **DLH-3C** time-dependent household/KFE response under externally prescribed small paths (zero-path ⇒ SS; amplitude→0 ⇒ response→0; mass/non-negativity; boundary; horizon; reproducibility);
- **DLH-3D** full NK GE + first deterministic monetary innovation (only independent 3D review may first qualify for `MINIMAL_GENUINE_SINGLE_REGION_HANK_DYNAMIC_VALIDATED`);
- **DLH-3E** HANK numerical robustness freeze (asset domain, asset-grid refinement, **separate** time discretization, horizon/terminal, reproducibility).
- None authorized here; listed as non-binding design boundaries only.

## 14. Tier-0 Q200 relationship and non-inheritance

Q200 `[0,200]`/1265-pt remains the accepted Tier-0 real HA reference; C200/F200/Q200 hierarchy usable as regression provenance; changing asset semantics ⇒ HANK domain adequacy must be re-established (DLH-3E); a development grid is allowed in future only under an explicit regression contract; all fixtures `VALIDATION_FIXTURE_NOT_CALIBRATION`.

## 15. Owner deferral

Final regional steady-state asset/production architecture remains an Owner scientific-direction decision and is **not** irreversibly frozen by this single-region validation architecture (Issue #10 §2).

## 16. Unresolved numerical parameters (for later validation fixture)

`γ, χ, φ, ε, φ_p, φ_π, r̄, τ_l, ā, B, z_l, z_h, λ_lh, λ_hl, A_t`, asset-domain `[ā, a_max]` and the HANK development/reference grids — all fixture-level, to be assigned only in a later implementation Issue, always `VALIDATION_FIXTURE_NOT_CALIBRATION`.

## 17. Evidence classification

**Specification only.** No D2 HANK result, no calibration, no genuine-HANK validity claim, no transition dynamics, no policy/Results/novelty claim.

## 18. Forbidden-operation counters (all zero)

See `DLH_3A_FORBIDDEN_OPERATION_CHECK.md`. Summary: model source/config/test creation or modification 0 · numerical execution 0 · pytest for scientific purposes 0 · shock/transition/IRF 0 · calibration/regression 0 · empirical data 0 · neural/RL/GPU 0 · legacy Matlab / old Python reference / private Zotero access 0 · regional/W code 0 · Results claims 0 · governance mutation 0 · PR / merge / Issue close / successor / self-accept 0.

## 19. Recommendation (non-binding)

After independent review of this specification, a separate successor Issue may authorize DLH-3B (steady-state structural kernel implementation) with frozen equations and residual gates; DSH does not create or propose 3B authority beyond this non-binding recommendation.
