# DLH-3D-R1A — HA State-Space, Algorithm, and Asset-Accounting Consistency Audit — Main Report

- Date: 2026-08-20
- Author: DSH (bounded Builder)
- Authority: GitHub Issue #14 — `DLH-3D-R1A: HA state-space, algorithm, and asset-accounting consistency audit` (state: OPEN), authoritative activation comment id `5355380189`; canonical execution specification `tasks/DLH_3B_R1_HA_ALGORITHM_PARITY_AUDIT_2026_08_20.md`
- Task type: `SCIENTIFIC_AUDIT_ONLY`
- Status: **AUDIT COMPLETE — structural parity mismatch documented (fail-closed blocker evidence).** No model/code/parameter modification; no numerical execution.
- Evidence class: `D2_MACHINE_DIAGNOSTIC`-style static audit evidence — audit conclusions are derived from source/evidence inspection, not from new numerical runs.

> Read together with the companion documents in this directory:
> `DLH_3D_R1A_STATE_SPACE_AUDIT.md`, `DLH_3D_R1A_HJB_PARITY_TABLE.md`,
> `DLH_3D_R1A_KFE_PARITY_TABLE.md`, `DLH_3D_R1A_ASSET_ACCOUNTING_AUDIT.md`,
> `DLH_3D_R1A_FAILURE_INTERPRETATION.md`, `DLH_3D_R1A_EVIDENCE_MANIFEST.md`,
> `DLH_3D_R1A_FORBIDDEN_OPERATION_CHECK.md`.

## 0. Headline findings

1. **The current Python HA/HANK module implements a ONE-asset economy** with household state `(a, z)`: one liquid, risk-free real financial asset `a` plus a two-state idiosyncratic CTMC productivity `z`. There is **no** second (illiquid) asset, **no** adjustment cost `chi(d,a)`, **no** borrowing premium, and **no** portfolio choice in the current Python route.
2. **The legacy Matlab reference `HANK_2ASSETS_HJB.m` implements a TWO-asset HANK** with household state `(b, ah, z)`: liquid asset `b` (with borrowing premium `rb_gap`) and illiquid asset `ah` (productive capital), coupled by the adjustment-cost mechanism `chi(d,a)` (`HANK3_FOC.m` / `HANK3_cost.m`), inside a 31-province data-calibrated model.
3. Therefore the current Python implementation and the legacy Matlab reference **do not solve the same economic problem**: asset structure, production, and regional scope all differ. Under Issue #14's completion rule ("If structural mismatch: `BLOCKED_DLH_3D_R1A_HA_ALGORITHM_PARITY_MISMATCH`"), the terminal classification is:
   **`BLOCKED_DLH_3D_R1A_HA_ALGORITHM_PARITY_MISMATCH`** (correct fail-closed blocker evidence, not a PASS).
4. **The Python implementation is internally self-consistent**: HJB drift, KFE generator, asset accounting, and labor accounting match its own declared one-asset structure and the accepted DLH-3A/DLH-3B/DLH-3C contracts (verified from code and accepted evidence, incl. zero-innovation invariance, KFE-consistent wealth-flow residual `~7e-14`, accepted `A_hh* = 10.000000002223675 ≈ B = 10`). No internal implementation bug was found by this audit.
5. **DLH-3D fail-closed goods-gate failure** is classified as a **finite-horizon terminal-boundary artifact** (with frozen-fixture interaction), not an HA implementation / asset-accounting / HJB-KFE mismatch. Evidence-based analysis in `DLH_3D_R1A_FAILURE_INTERPRETATION.md`.

The distinction between findings 3 and 4 is the central message of this audit: *parity mismatch with the legacy two-asset reference* (a documented, contract-level architectural difference) ≠ *internal inconsistency of the Python implementation* (none found).

## 1. MATLAB specification map (read-only reference)

Files inspected (SHA-256 in `DLH_3D_R1A_EVIDENCE_MANIFEST.md`):

- `HANK_2ASSETS_HJB.m` — household two-asset HJB + transition-matrix + stationary distribution + aggregates.
- `HANK3_FOC.m`, `HANK3_cost.m` — adjustment-cost transfer choice `d` and cost `chi(d,a)`.
- `lab_solve2.m` — static labor FOC root.
- `HANK_firm.m` — firm block: `Y = Z*K^alpha*L^(1-alpha)`, Rotemberg NKPC (`theta`), capital rental `rk`, wage `wjt`, illiquid-asset return `ra0 = rk - delta + divrate`.
- `multi_prov_HANK_12sts.m` — driver: grids/parameters/CHI; 31 provinces.
- `mpHANK_equilibrium_2000.m`, `HANK_mp_1eq.m`, `HANK_mp_1turn.m` — steady-state equilibrium loop.
- `12年稳态值.xlsx` — exported steady-state GDP table (province × years, actual vs model).

Economic problem (Matlab): two-asset HANK, continuous time, per-province; productive capital `ah`; liquid bonds `b` with borrowing premium; adjustment cost between assets; labor-only? No — Cobb-Douglas `Y = Z K^α L^(1-α)`; Rotemberg price adjustment; Taylor rule (`param.rho_pi`, `istar`); 31 provinces with inter-province capital spillovers and labor-flow matrices.

## 2. Python implementation map (current)

Files inspected (paths relative to repo root; all at audited commits):

- `src/deep_learning_hank/solvers/hank_household_steady_state.py` — one-asset HJB with endogenous static labor.
- `src/deep_learning_hank/solvers/hank_steady_state.py` — nested `brentq` equilibrium (`r`, `N`).
- `src/deep_learning_hank/solvers/hank_household_transition.py` — backward implicit HJB (DLH-3C).
- `src/deep_learning_hank/solvers/hank_kfe_transition.py` — forward implicit KFE.
- `src/deep_learning_hank/solvers/hank_nkpc_transition.py`, `solvers/hank_ge_transition.py` — DLH-3D aggregate closure + krylov path root.
- `src/deep_learning_hank/economics/{preferences,grids,hank_firm,hank_fiscal,hank_nominal}.py`.
- `src/deep_learning_hank/{hank_config,hank_transition_config,hank_ge_config}.py`.
- `configs/dlh_3b_hank_steady_state_validation.toml`, `dlh_3c_hank_transition_validation.toml`, `dlh_3d_hank_monetary_ge_validation.toml`.

Economic problem (Python, current): one-asset HANK validation route per accepted DLH-3A contracts — liquid risk-free real bond `a`, labor-only production `Y = Z*N`, constant bond supply `B`, Fisher/Taylor/NKPC nominal block, single region, no capital, no adjustment cost, no borrowing (`a_min = 0.0`).

## 3. State-space comparison

| Dimension | Python (current) | Matlab (legacy `HANK_2ASSETS_HJB.m`) |
|---|---|---|
| Household state | `(a, z)` — one asset + productivity | `(b, ah, z)` — two assets + productivity |
| Liquid asset | `a`, return `r` (single real return) | `b ∈ [-2, 5]` (I=20), return `rb` (borrowing premium `rb_gap` for `b<0`) |
| Illiquid asset | — (none) | `ah ∈ [0, 10]` (J=20), return `raah = rah*(1 - 0.1*(ahmax/ah)^(-9))`; `rah` from firm block |
| Productivity | `z ∈ {0.5, 1.5}` CTMC (rates 0.25/0.25) | `z ∈ [0.8, 1.3]` (Nz=2), generator `la_mat` (rate 1/3) |
| Asset grid | uniform 401 pts on `[0, 100]` (3B fixture; `a_min=0`, no borrowing) | `b`: 20 pts, `ah`: 20 pts |
| Aggregate states | none (transition solved pathwise) | none (steady state per year/province) |
| Regional dimension | none (single region) | 31 provinces, spillover matrices, labor-flow matrices |

Source: Python `configs/dlh_3b_hank_steady_state_validation.toml` (`asset_grid_count=401`, `a_min=0.0`, `a_max=100.0`, `idiosyncratic_states=[0.5,1.5]`, `q_*=0.25`); Matlab `multi_prov_HANK_12sts.m` (`grid.I=20`, `bmin=-2`, `bmax=5`, `grid.J=20`, `amin=0`, `amax=10`, `Nz=2`, `zmin=0.8`, `zmax=1.3`, `la_mat`), `HANK_2ASSETS_HJB.m` state arrays `bbb/aaah/zzz`.

## 4. Asset-accounting comparison

| Object | Python (current) | Matlab (legacy) |
|---|---|---|
| `A` | `A_hh = ∫ a dg` — aggregate household liquid-asset demand (`distribution.mean_assets`) | `Aht = ∫ ah dg` — aggregate illiquid (capital) holdings |
| `B` | constant bond **supply** `B = 10` (`config.fiscal.B`); clearing `A_hh = B` | `Bt = ∫ b dg` — aggregate liquid **holdings** (demand); also `B` used as HJB iteration matrix `(1/Δ+ρ)I − A` |
| `L` / `N` | `N_hh = ∫ z n dg` — aggregate effective labor; cleared vs `N` (`R_labor = N_hh − N`); production `Y = Z*N` | `Lt = ∫ z l dg`; production `Y = Z K^α L^(1−α)` |
| `Z` | productivity `Z = 1.0` (`config.production.Z`) | province productivity `Zt` (data-calibrated) |
| Clearing | one market: `A_hh = B` (+ labor `N_hh = N`) | two asset aggregates `Bt`, `Aht` (capital market via firm block; liquid market via monetary block) |

**Symbol-collision warnings (documentation/semantic):**
- Python `B` = bond **supply**; Matlab `Bt` = liquid asset **demand**. Never equate them without the codebase qualifier.
- Python `chi` = labor-disutility scale `χ` (`v(n)=χ n^(1+1/φ)/(1+1/φ)`); Matlab `CHI` = asset **adjustment cost** parameters (`chi0=0.1`, `chi1=2`, `a_bar=1e-6`). The names collide across codebases; they are different objects.

Details: `DLH_3D_R1A_ASSET_ACCOUNTING_AUDIT.md`.

## 5. HJB comparison

| Aspect | Python (current) | Matlab (legacy) |
|---|---|---|
| Value-function state | `V(a,z)` | `V(b,ah,z)` |
| Controls | `c`, `n` (static labor) | `c`, `l` (static labor), plus illiquid-asset transfer `d` (adjustment cost) |
| Utility | `u(c)=c^(1-γ)/(1-γ)`, `γ=2` | `alphac*c^(1-ga)/(1-ga)`, `ga=2`, `alphac=1` |
| Labor disutility | `v(n)=χ n^(1+1/φ)/(1+1/φ)`, `χ=0.7`, `φ=1.0` | `alphal*l^(1+1/frisch_l)/(1+1/frisch_l)`, `frisch_l=0.2` |
| Labor FOC | `v'(n)=(1-τ_l) w z V_a` (static, KKT-clipped) | `lab_solve2.m`: same FOC family `l = (…w z)^frisch_l (c)^(-ga*frisch_l)` |
| Asset adjustment | none | `chi(d,a)`: inaction band `[1−chi0, 1+chi0]` on `V_ah/V_b`, transfer `d = (…)*a/chi1`, cost `chi0|d| + chi1 d²/2 * max(a,a_bar)^(-1)` |
| Upwind | 3-candidate (zero-drift / forward / backward) on `a` | `VbF/VbB` on `b`, `VahF/VahB` on `ah` |
| Boundaries | state-constraint / no-outward-drift (`drift≥0` at `a_min`; `drift≤0` at `a_max`) | lower/upper `b` via constrained marginal utility; `VahF(:,J)=0`, `VahB(:,1)=0`; forced switching at `b` upper |
| Iteration | `(ρ+1/Δ)I − G` pseudo-time, `Δ=1000` | `(1/Delta+rho)I − A`, `Delta=1000`, `crit=1e-7` |

**Verdict:** the HJB numerical methodology is the same HACT family (continuous-time upwind HJB with pseudo-time value iteration), but the **economic problem differs** (one asset vs two assets; no vs yes adjustment cost). This is the core structural parity mismatch.

Details: `DLH_3D_R1A_HJB_PARITY_TABLE.md`.

## 6. Generator / transition-matrix comparison

| Aspect | Python (current) | Matlab (legacy) |
|---|---|---|
| Generator | `_build_generator` (COO): upwind asset-drift rates + CTMC `z` rates; rows sum 0 (checked `≤1e-12`) | `A = BB + AAH + Bswitch`: liquid drift + illiquid drift + `z` transitions; row sums checked `< homecrit=1e-2` |
| HJB↔KFE sharing | same generator object used in HJB matrix and KFE | same `A` used in HJB (`(1/Δ+ρ)I−A`) and KFE (`AT\vec`) |
| Orientation | KFE solves `G^T g = 0`; transition `[I − dt G_k^T] g_{k+1} = g_k` | `AT = A'`; stationary solve `AT\vec` with pinned row |
| Stationary solve | pin last row to 1, rhs=1, then renormalize to `Σg=1` | pin row `iFix=floor(0.37M)` to 0.007, then normalize `g_sum = g'·ones·db·dah` (density measure) |
| Mass conservation | `1^T G^T = 0` in exact arithmetic; mass error `≤1e-10` gate | row sums ≈ 0 checked; `sumg = sum(g·db·dah)=1` |

**Verdict:** same HJB→KFE coupling logic (same infinitesimal generator for both, transpose solve, pinned-row normalization). Convention difference only: Python mass vector sums to 1 on grid points (mean `Σ g·a`); Matlab `g` is a density normalized by grid measure `db·dah`. Both are internally consistent.

Details: `DLH_3D_R1A_KFE_PARITY_TABLE.md`.

## 7. Steady-state solver workflow comparison

| Stage | Matlab (legacy) | Python (current) |
|---|---|---|
| Guess prices | per-province `Zt`, `alpha` from data; `ra`, `wjt`; `KNratio` | Tier-0: guess `K`; 3B: guess `(r, N)`; 3D: path guess `x=(log w/w*, log N/N*)` |
| Household HJB | `HANK_2ASSETS_HJB` (two-asset) | `solve_hank_household` / `solve_dynamic_household` (one-asset) |
| Transition matrix | `A = BB + AAH + Bswitch` | generator `G` |
| Stationary distribution | `AT\vec` (+normalization) | `G^T g = 0` (+normalization) |
| Aggregate moments | `Lt, Bt, Aht, Ct, ...` | `N_hh, A_hh, C` |
| Update equilibrium | adjust `Zt`, `GovInv`, `KNratio`; check `KNratio` gap, `Yt` gap, HJB convergence, boundary counts | brentq on `K` (Tier-0) / nested brentq `(N, r)` (3B) / krylov path root (3D) |

**Verdict:** same overall loop family (prices → HJB → generator → stationary distribution → aggregates → update prices → convergence), different specific closure (one-asset vs two-asset; single-region vs 31-province data-calibrated; scalar roots vs path root).

## 8. Confirmed matches

1. Continuous-time HJB/KFE methodology (HACT family): upwind scheme, pseudo-time value iteration, generator-transpose KFE.
2. HJB↔KFE share the same transition/generator operator in both codebases.
3. Stationary distribution solved as null-space of the transposed generator with a pinned row and renormalization.
4. Endogenous static labor FOC family `v'(n) = (1-τ) w z V_a` (identical structure; different fixture parameters).
5. CRRA consumption utility family (identical structure).
6. Deterministic, reproducible execution discipline in the current Python route (repeat diffs 0.0), consistent with the accepted evidence.

## 9. Scientific mismatches (structural)

1. **State space**: `(a,z)` one-asset vs `(b,ah,z)` two-asset. *(highest priority finding)*
2. **Asset accounting**: single liquid bond cleared against constant supply `B=10` vs two asset aggregates (`Bt` liquid demand, `Aht` capital) with adjustment-cost coupling.
3. **Adjustment cost `chi(d,a)`**: present in Matlab (inaction band + quadratic cost), absent in Python.
4. **Borrowing**: Python `a_min=0.0` (no borrowing); Matlab `bmin=-2` with borrowing premium `rb_gap`.
5. **Production**: Python labor-only `Y=Z*N`; Matlab Cobb-Douglas `Y=Z K^α L^(1-α)` with productive capital.
6. **Regional scope**: Python single-region validation fixture; Matlab 31-province data-calibrated model with spillovers.
7. **Symbol semantics**: `B` (supply vs demand), `chi` (labor vs adjustment cost), `A` (liquid vs illiquid) collide across codebases.

## 10. Risk classification

| Risk | Level | Notes |
|---|---|---|
| Confusing Python's one-asset route with the legacy two-asset model (A/B/L/Z misreading) | HIGH | explicit symbol-collision documentation required; see §4 |
| Python internally inconsistent (HJB↔KFE↔accounting) | NOT FOUND | audited code + accepted evidence consistent |
| DLH-3D goods-gate failure caused by an implementation/accounting bug | NOT SUPPORTED | evidence points to terminal-boundary artifact (see `DLH_3D_R1A_FAILURE_INTERPRETATION.md`) |
| Two-asset HACT features (adjustment cost, borrowing spread, illiquid return curvature) silently assumed in Python | NOT PRESENT | Python has none; any such assumption would be unfounded |

## 11. Recommendation for the next scientific step (non-binding; no authority)

- Keep the Python one-asset route labeled exactly as its accepted contracts label it: minimal single-region HANK validation route with one liquid bond; do not describe it as a two-asset/HACT model.
- Any future two-asset HANK/HACT work (adjustment cost `chi(d,a)`, borrowing spread, illiquid capital) requires a separate, explicit open Issue and would be a **new model**, not a migration of the current route.
- Any claim that the current Python route is "the Python port of `HANK_2ASSETS_HJB.m`" is not supported and must be avoided.
- DLH-3D fail-closed interpretation and next-gate options are discussed in `DLH_3D_R1A_FAILURE_INTERPRETATION.md`.

## 12. Terminal classification

**`BLOCKED_DLH_3D_R1A_HA_ALGORITHM_PARITY_MISMATCH`**

Per Issue #14 completion rule ("If structural mismatch: `BLOCKED_DLH_3D_R1A_HA_ALGORITHM_PARITY_MISMATCH`"): the audit found that the current Python implementation (one-asset `(a,z)`) and the legacy Matlab reference (`(b,ah,z)` two-asset with adjustment cost) have **different algorithm/economic structure**. This is a correct fail-closed blocker classification; per project rules it may be accepted as blocker evidence but is not a PASS and does not relabel the accepted one-asset DLH-3 route.

- Branch: `dsh/issue-14-dlh-3d-r1a-ha-consistency-audit-2026-08-20` (created from fresh `origin/main` `d727dda28738bbdad126c784f0366f0e21be3e1d`).
- Commit: reported in the completion response.
- Changed paths: only `reports/dlh_3d_r1a_ha_consistency_audit/**` (Issue #14 output allowlist).
- Files reviewed / limitations / unresolved questions: see `DLH_3D_R1A_EVIDENCE_MANIFEST.md` and `DLH_3D_R1A_FORBIDDEN_OPERATION_CHECK.md`.
