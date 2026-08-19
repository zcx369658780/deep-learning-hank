# DLH-3A Review Packet — R1 Equation-Consistency Correction (Minimal Genuine Single-Region HANK Architecture / Equation Freeze)

- Date: 2026-08-19 (R1 revision 2026-08-20)
- Author: DSH (bounded Builder)
- Authority: GitHub Issue #10 — `DLH-3A: Minimal genuine single-region HANK architecture and equation freeze` (state: OPEN); authoritative R1 correction comment id `5348615886` (2026-08-19 22:10:46) read fresh.
- Status: **R1 CANDIDATE (specification only)**. Acceptance requires fresh-GitHub independent review (ChatGPT) + Owner scientific-direction awareness.
- Evidence class: **SPECIFICATION ONLY — no model code, no numerical result, no D2 HANK evidence.**

## 1. Terminal classification

`DLH_3A_R1_EQUATION_CONSISTENCY_CORRECTED_READY_FOR_GPT_OWNER_REVIEW`

## 2. Baseline / Issue / branch / commit

- Fresh baseline `origin/main` SHA: `d5e20f895ccec7ef116f777039aa1680025d0bcf`
- Issue #10 title/status: `DLH-3A: Minimal genuine single-region HANK architecture and equation freeze` — OPEN
- R1 dedicated branch (per review comment): `dsh/issue-10-dlh-3a-r1-equation-consistency-2026-08-20`, created from fresh `origin/main` `d5e20f8` (NOT from the unaccepted R0 candidate)
- R1 candidate commit: single coherent commit at branch HEAD (2026-08-20, DSH); hash reported in completion response. Expected delta: exactly the six allowlisted paths, 0 behind / 1 ahead.
- R0 provenance: candidate `4b17acbb1ca22ce04fce9eca012c72fc514cd80f` on branch `dsh/issue-10-dlh-3a-minimal-hank-architecture-2026-08-19` — reviewed, **NOT accepted / NOT merged**; read by R1 as provenance only, not cherry-picked.

## 3. Exact changed paths (six allowlisted outputs)

1. `docs/specifications/DLH_3_MINIMAL_GENUINE_HANK_ARCHITECTURE_2026_08_19.md`
2. `docs/specifications/DLH_3_ASSET_FISCAL_AND_NOMINAL_SEMANTICS_CONTRACT_2026_08_19.md`
3. `docs/specifications/DLH_3_STEADY_STATE_AND_DYNAMIC_EQUATION_CONTRACT_2026_08_19.md`
4. `docs/specifications/DLH_3_VALIDATION_LIMITING_CASE_AND_GRID_CONTRACT_2026_08_19.md`
5. `reports/dlh_3a_minimal_hank_architecture_2026_08_19/DLH_3A_REVIEW_PACKET.md`
6. `reports/dlh_3a_minimal_hank_architecture_2026_08_19/DLH_3A_FORBIDDEN_OPERATION_CHECK.md`

**No other tracked path modified** — `src/**`, `configs/**`, `tests/**`, `project_rules/**`, `tasks/**`, Startup Snapshot, README, roadmap, handoff, and all accepted DLH-0/1/2 reports/evidence untouched. The R0 branch and its candidate commit are preserved untouched.

## 4. Exact files read (GitHub / repository)

- `docs/governance/DLH_SESSION_HANDOFF_AFTER_TIER0_NUMERICAL_ROBUSTNESS_COMPLETE_2026_08_19.md` (fresh `origin/main`)
- `project_rules/PROJECT_RULE_INDEX_CURRENT.md` + all CURRENT rules required by the index (Overview; DSH GitHub Workflow; DSH Local Readonly Reference Access; Model Development Diagnostic Gates incl. stage-numbering disambiguation; Research Evidence and Citation; Acceptance Levels)
- `tasks/TASK_INDEX_CURRENT.md` (Status `ACTIVE_GITHUB_ISSUE_10__DLH_3A_MINIMAL_HANK_ARCHITECTURE`)
- `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`
- `docs/roadmaps/DLH_MASTER_ROADMAP_INITIAL_2026_08_19.md`
- Accepted DLH-0 constitution materials (`DLH_0_SCIENTIFIC_CONSTITUTION_CANDIDATE_2026_08_19.md`, `DLH_0_MINIMUM_ECONOMIC_MODEL_CONTRACT_2026_08_19.md`)
- Accepted DLH-2A code (interface semantics): `src/deep_learning_hank/economics/preferences.py`, `solvers/household_hjb.py`, `solvers/distribution_kfe.py`, `economics/grids.py`
- Accepted DLH-2B code (interface semantics): `src/deep_learning_hank/economics/firm.py`, `economics/fiscal.py`, `solvers/steady_state.py`
- Issue #9 accepted robustness reports (`reports/dlh_2c_b2_fixed_domain_grid_2026_08_19/DLH_2C_B2_EXECUTION_REPORT.md`) as numerical-reference provenance
- GitHub Issue #10 body + all authoritative comments (2 comments: synchronization id `5342742348`; R1 correction review id `5348615886`) via authenticated `gh api`
- R0 six-file candidate `4b17acbb…` (read as provenance/reference; copied to local temp reference only, not into the R1 tree)

## 5. Architecture summary (one paragraph)

The DLH-3A minimal genuine single-region HANK validation economy is a continuous-time economy with (i) a heterogeneous household block on a single liquid risk-free financial asset `a` with a two-state idiosyncratic productivity CTMC, CRRA consumption utility, and **endogenous static labor supply** (control, not state); (ii) labor-based production `Y = Z N` with aggregate productivity `Z_t`, monopolistic competition markup `μ`, **Rotemberg** price adjustment, and a continuous-time NKPC **derived** from the stated convention and frozen as an explicitly labeled local linearization `π̇ = ρπ − κ(mc − 1/μ)`, `κ = ε/φ_p`; (iii) a monetary block (nominal rate `i_t`, inflation `π_t`, real return `r_t`, Fisher, Taylor rule `i_t = r̄ + π̄ + φ_π(π_t − π̄) + ε^i_t` with `π̄ = 0`, `φ_π > 1`, `ε^i_t = 0` in 3B/3C); (iv) a fiscal/bond block with **constant** bond supply `B` through 3B–3D (`Ḃ ≡ 0`), labor tax, lump-sum transfer, lump-sum dividend incidence, and asset-market clearing `A^hh_t = B`; and (v) exact computed residual objects for HJB, KFE, asset/labor/goods markets (incl. Rotemberg cost), fiscal, profits, NKPC, Fisher, Taylor, and the aggregate wealth-flow identity. The liquid asset is explicitly **not** Tier-0 productive capital; steady-state reduction preserves the accepted stationary HJB/KFE family with a documented re-interpretation of income terms; dynamic household/KFE response and full NK GE are separate successor subgates (DLH-3B/3C/3D/3E), and Tier-0 `[0,200]` domain adequacy is **not** inherited by HANK.

## 6. R0 → R1 correction table (review comment id `5348615886`)

| # | Review finding | R1 resolution | Where |
|---|---|---|---|
| 1 | Symbol collision: `A_t` used for both aggregate productivity and aggregate household assets | Distinct notation frozen: `Z_t` = aggregate productivity; `A^hh_t = ∫ a dg_t` = aggregate household liquid assets; collision removed everywhere | architecture §3/§4; semantics §1/§6; equation contract §2.1/§5; all four specs + packet |
| 2 | Forward KFE expanded form double-counts CTMC outflow | KFE written in compact `∂_t g = −∂_a(ȧ g) + Qᵀ g` and expanded off-diagonal-only form `+ Σ_{z′≠z} Q[z′,z] g(z′) − (Σ_{z′≠z} Q[z,z′]) g(z)`; algebraic equivalence proven; R0 form removed | equation contract §1.5 |
| 3 | Rotemberg/NKPC sign contradiction + unjustified slope | Full derivation from stated convention (demand `y_j = Y(p_j/P)^{−ε}`, technology `y_j = Z n_j`, cost `(φ_p/2)π_j²Y`, Hamiltonian, FOC, costate, symmetric equilibrium) → exact nonlinear FOC `π̇ = ρπ − (ε/φ_p)(mc − 1/μ) − π(Ẏ/Y)`; frozen operational equation is the explicitly labeled local linearization `π̇ = ρπ − κ(mc − 1/μ)`, `κ = ε/φ_p`; sign interpretation made algebraically consistent (mc > 1/μ ⇒ π̇ < 0 at π = 0; forward solution π = κ∫e^{−ρ(s−t)}(mc − 1/μ)ds ⇒ positive π level); log-deviation coefficient `(ε−1)/φ_p` documented and mixing prohibited | equation contract §2.4; architecture §5.2; packet §9 |
| 4 | Taylor-rule coefficient convention ambiguous | Frozen: `i_t = r̄ + π̄ + φ_π(π_t − π̄) + ε^i_t`, `π̄ = 0`, `φ_π > 1` (total nominal-rate response to inflation deviation is exactly `φ_π`), `ε^i_t = 0` in 3B/3C, 3D innovation through `ε^i_t` | semantics §5; equation contract §3/§5; architecture §5.3 |
| 5 | Dynamic fiscal/debt closure incomplete if `B_t` varies | `B_t ≡ B` constant through 3B–3D with `Ḃ ≡ 0`; transfers adjust to service `r_t B`; varying-debt path/`Ḃ` law deferred to a separately authorized fiscal extension | semantics §2/§3; equation contract §4; architecture §5.4 |
| 6 | Wrong subtraction in aggregate cash-flow/resource identity | Aggregate wealth-flow identity written explicitly: `Ȧ^hh_t = (1−τ_l)w_t N_t + r_t A^hh_t + tr_t + Π_t − C_t`; full consistency chain (constant-B clearing ⇒ wealth-flow ⇒ fiscal ⇒ `C = wN + Π`; profits + goods ⇒ `C = Y − (φ_p/2)π²Y`); false R0 identity removed; wealth-flow residual `R_wealth` added | semantics §6; equation contract §5/§6; validation §3.1 |
| 7 | Labor-market residual lacks firm-demand definition | Firm labor demand defined by technology: `N^d_t = Y_t/Z_t`; `R_labor = N^s_t − N^d_t = ∫ z n dg − Y_t/Z_t`; markup `w_t = Z_t mc_t` confined to pricing, not labor demand | semantics §6.3; equation contract §2.2/§5; architecture §5.2 |

## 7. State / control / price / aggregate / residual table

| Category | Objects |
|---|---|
| Household state | `a` (liquid financial asset), `z ∈ {z_l, z_h}` (2-state CTMC) |
| Controls | consumption `c ≥ 0`; **endogenous static labor `n ∈ [0, n̄]`** |
| Prices | real wage `w_t`; real liquid return `r_t`; nominal rate `i_t`; inflation `π_t`; real marginal cost `mc_t` |
| Aggregates | `Y_t, N_t, A^hh_t, C_t, Π_t, B, tr_t, μ, Z_t` |
| Residuals | HJB, KFE/mass, asset, labor, goods (incl. Rotemberg cost), fiscal, profits, wealth flow, NKPC, Fisher, Taylor |

## 8. Liquid-asset semantic and why it is not Tier-0 productive capital

- `a` is a liquid, risk-free real financial claim (government-bond counterpart) paying `r_t`; it appears only in the household budget and asset-market clearing; aggregate demand `A^hh_t = ∫ a dg_t` clears against constant bond supply `B`.
- Tier-0's asset was productive capital entering the Cobb-Douglas production function (`alpha_k`, `delta`); accepted Tier-0 code (`economics/firm.py`, `solvers/steady_state.py`) is **not** silently reinterpreted — the DLH-3 cash flow replaces Tier-0's `(1−τ_l)w z + r a + transfer` with `(1−τ_l) w z n + r a + tr + Π` and the asset is financial, not productive. Consequently Tier-0 domain adequacy is not inherited (re-established in DLH-3E).

## 9. Endogenous-labor FOC semantics

`v′(n) = (1−τ_l) w_t z V_a` with `v(n) = χ n^(1+1/φ)/(1+1/φ)`; labor is a **static control** — no additional state dimension; aggregate effective labor supplied `N^s_t = ∫ z n dg`; labor-market residual `R_labor = N^s_t − Y_t/Z_t` (firm demand by technology, finding 7).

## 10. Rotemberg / NKPC timing convention (frozen in R1)

Derived exact nonlinear symmetric-equilibrium FOC: `π̇ = ρπ − (ε/φ_p)(mc − 1/μ) − π(Ẏ/Y)` (firms discount at the household rate `ρ`, representative-firm valuation convention). Frozen operational equation (explicitly labeled local linearization around the zero-inflation steady state): `π̇_t = ρ π_t − κ (mc_t − 1/μ)`, `κ = ε/φ_p > 0`. Sign convention: `π_t = Ṗ_t/P_t`; at `π_t = 0`, `mc_t > 1/μ` ⇒ `π̇_t < 0`; the bounded forward solution gives positive inflation for marginal cost above `1/μ`, matching the discrete-time NKPC `π_t = βπ_{t+1} + κ(mc_t − 1/μ)`. Steady state `π = 0`, `mc = 1/μ`. Log-deviation coefficient `(ε−1)/φ_p` documented; mixing level/log conventions prohibited. `P_t` continuous (no jump).

## 11. Fisher / Taylor timing convention (frozen in R1)

`i_t = r_t + π_t` (exact continuous-time Fisher; residual `i − r − π`); Taylor `i_t = r̄ + π̄ + φ_π(π_t − π̄) + ε^i_t`, `π̄ = 0`, `φ_π > 1`, `ε^i_t = 0` in 3B/3C (3D innovation through `ε^i_t`); residual `R_taylor = i_t − [r̄ + π̄ + φ_π(π_t − π̄) + ε^i_t]`; steady state `π* = 0`, `i* = r* = r̄`; zero-shock consistency at `π = π̄ = 0`, `ε^i = 0`.

## 12. Fiscal / bond / dividend accounting convention (frozen in R1)

Bonds: exogenous **constant** `B` through 3B–3D (`B_t ≡ B`, `Ḃ ≡ 0`); asset-market clearing `A^hh_t = B`; tax revenue `T_t = τ_l w_t N_t`; government budget `r_t B + tr_t = T_t` (no seigniorage, no issuance); transfer closure `tr_t = T_t − r_t B`; profits `Π_t = Y_t − w_t N_t − (φ_p/2)π_t²Y_t` distributed lump-sum per capita; every residual computed (never zeroed by labeling); varying-debt path deferred to a separately authorized fiscal extension.

## 13. Steady-state reduction

`∂_t V = 0`, `∂_t g = 0` ⇒ stationary HJB `ρ V = max{U + V_a ȧ + Q V}` and stationary KFE `Gᵀ g = 0` — the accepted Tier-0 stationary HJB/KFE family with the documented HANK cash-flow re-interpretation. Steady state: `π* = 0`, `mc* = 1/μ`, `w* = Z/μ`, `A^hh* = B`, `tr* = τ_l w* N* − r̄ B`, `C* = w* N* + Π* = Y*`.

## 14. Future gate boundaries (3B/3C/3D/3E)

- **DLH-3B** steady-state structural kernel (zero-inflation/zero-shock; a 3B PASS is not full dynamic HANK validation);
- **DLH-3C** time-dependent household/KFE response under externally prescribed small real paths `(w_t, r_t, tr_t, Π_t)` with `ε^i_t = 0` (zero-path ⇒ SS; amplitude→0 ⇒ response→0; mass/non-negativity; boundary; horizon; reproducibility);
- **DLH-3D** full NK GE + first deterministic monetary innovation through `ε^i_t` (only independent 3D review may first qualify for `MINIMAL_GENUINE_SINGLE_REGION_HANK_DYNAMIC_VALIDATED`);
- **DLH-3E** HANK numerical robustness freeze (asset domain, asset-grid refinement, **separate** time discretization, horizon/terminal, reproducibility).
- None authorized here; listed as non-binding design boundaries only.

## 15. Tier-0 Q200 relationship and non-inheritance

Q200 `[0,200]`/1265-pt remains the accepted Tier-0 real HA reference; C200/F200/Q200 hierarchy usable as regression provenance; changing asset semantics ⇒ HANK domain adequacy must be re-established (DLH-3E); a development grid is allowed in future only under an explicit regression contract; all fixtures `VALIDATION_FIXTURE_NOT_CALIBRATION`.

## 16. Owner deferral

Final regional steady-state asset/production architecture remains an Owner scientific-direction decision and is **not** irreversibly frozen by this single-region validation architecture (Issue #10 §2). Preserved in all R1 outputs.

## 17. Unresolved numerical parameters (for later validation fixture)

`γ, χ, φ, ε, φ_p, φ_π, r̄, τ_l, ā, B, z_l, z_h, λ_lh, λ_hl, Z_t` (Taylor target `π̄ = 0`), asset-domain `[ā, a_max]` and the HANK development/reference grids — all fixture-level, to be assigned only in a later implementation Issue, always `VALIDATION_FIXTURE_NOT_CALIBRATION`.

## 18. Evidence classification

**Specification only.** R1 is an equation-consistency correction of a specification candidate; it creates no numerical result. No D2 HANK result, no calibration, no genuine-HANK validity claim, no transition dynamics, no policy/Results/novelty claim.

## 19. Forbidden-operation counters (all zero)

See `DLH_3A_FORBIDDEN_OPERATION_CHECK.md`. Summary: model source/config/test creation or modification 0 · numerical execution 0 · pytest for scientific purposes 0 · shock/transition/IRF 0 · calibration/regression 0 · empirical data 0 · neural/RL/GPU 0 · legacy Matlab / old Python reference / private Zotero access 0 · regional/W code 0 · Results claims 0 · governance mutation 0 · PR / merge / Issue close / successor / self-accept 0 · R0-branch mutation or cherry-pick 0.

## 20. Recommendation (non-binding)

After independent review of this R1 specification, a separate successor Issue may authorize DLH-3B (steady-state structural kernel implementation) with the frozen R1 equations and residual gates; DSH does not create or propose 3B authority beyond this non-binding recommendation.
