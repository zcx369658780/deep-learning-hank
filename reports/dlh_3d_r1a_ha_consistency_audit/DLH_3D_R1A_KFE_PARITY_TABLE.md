# DLH-3D-R1A — KFE / Generator Parity Table (Python vs Matlab)

- Date: 2026-08-20
- Authority: GitHub Issue #14 (OPEN), activation comment `5355380189`; canonical spec `tasks/DLH_3B_R1_HA_ALGORITHM_PARITY_AUDIT_2026_08_20.md`
- Type: `SCIENTIFIC_AUDIT_ONLY`; no modification; no numerical execution.

## 1. Transition operator / generator comparison

| Aspect | Python (current) | Matlab (legacy `HANK_2ASSETS_HJB.m`) | Match |
|---|---|---|---|
| Generator construction | `_build_generator(drift, state_generator, spacing)` — upwind asset-drift rates (right/left) + CTMC `z` rates; COO with duplicate summing (`solvers/hank_household_steady_state.py` ~L255-302) | `A = BB + AAH + Bswitch` — liquid-drift block + illiquid-drift block + `z` transition block (HJB ~L160-245) | SAME family |
| Generator convention | **infinitesimal generator / intensity matrix**: rows sum 0, off-diagonals ≥ 0, diagonal = negative total outflow (checked `≤1e-12` at load; `economics/grids.py`) | rows-sum-0 convention: `A2max = max(abs(sum(A,2)))` checked `< num.homecrit = 1e-2` (HJB ~L245-250) | SAME |
| HJB↔KFE same operator | YES: the same `generator` object is used in the HJB matrix `(ρ+1/Δ)I − G` and in the KFE solve `G^T g = 0` / transition `[I − dt G_k^T] g_{k+1} = g_k` | YES: the same `A` is used in HJB `B = (1/Delta+rho)*speye − A` and in KFE `AT = A'`, `g = AT\vec` | SAME (both share one operator) |
| Transpose relationship | stationary: solve `G^T g = 0` with a pinned row (`solvers/distribution_kfe.py` — last row set to 1, rhs last = 1); transition: `[I − dt G_k^T]` (implicit, `solvers/hank_kfe_transition.py`) | stationary: `AT = A'`, pin row `iFix = floor(0.37*M)` to `0.007`, `vec(iFix)=0.007` (HJB ~L334-341) | SAME logic |
| Stationary solve | `raw_mass = solve(G^T with pinned row)`; renormalize `mass = raw/sum(raw)`; tiny-negative cleanup rule reported | `g_stacked = AT\vec`; `g_sum = g'*ones*db*dah`; `g = g/g_sum` (density normalized by grid measure) | SAME logic; **convention difference**: Python mass sums to 1 over grid points; Matlab density integrates to 1 with measure `db*dah` |
| Mass conservation | `1^T G^T = 0` exact-arithmetic; diagnostics: mass error, min mass, negative count, NaN count; gate `mass_error ≤ 1e-10` (`diagnostics/hank_ge_transition.py` `_check_kfe_gates`) | row-sum check `< homecrit`; `sumg = sum(g*dah*db,'all')` reported | SAME intent; Python gate stricter |
| Dynamic transition | forward implicit `[I − dt G_k^T] g_{k+1} = g_k`; no mass renormalization (mass conservation emerges from the generator) | (no dynamic KFE in the audited Matlab steady-state file; transition version in `mpHANK_shock_2000.m`) | Python-only (3C/3D); not part of the Matlab steady-state reference |

## 2. Does Python use the same HJB → transition matrix → KFE → stationary distribution logic as Matlab?

**Yes at the level of the algorithm family:**

1. Solve the household HJB → obtain policies (consumption / labor / drift).
2. Build one continuous-time infinitesimal generator from the drift and the idiosyncratic CTMC.
3. Solve the stationary distribution from the **transposed** generator with a pinned row + renormalization.
4. Aggregate moments (assets, labor, consumption) from the distribution.

Both codebases follow exactly this chain, with the same generator shared between HJB and KFE. The differences are:
- the **state dimension** (Python 1 asset + 2 z-states ⇒ 802 nodes; Matlab 2 assets + 2 z-states ⇒ 800 nodes) and the grid sizes (401 vs 20×20);
- the **normalization measure** convention (Python: point mass summing to 1; Matlab: density with `db*dah` measure) — internally consistent in each codebase;
- Matlab additionally builds the illiquid-drift block `AAH` and the adjustment-cost-driven transfer rates; Python has no second asset.

## 3. Internal-consistency evidence for the Python KFE (from accepted evidence, no new runs)

- Accepted DLH-3B: `A_hh* = 10.000000002223675` against `B = 10` (asset clearing to ~2e-9), full suite 77/0.
- Accepted DLH-3C: forward KFE without mass renormalization; mass gates pass; repeat differences 0.0.
- DLH-3D: KFE-consistent discrete wealth-flow residual `R_wealth ≈ 7e-14 ≤ 1e-5` (authoritative `g_{k+1}` timing implemented at `solvers/hank_ge_transition.py` L225-233); zero-innovation invariance passes.

## 4. Conclusion

KFE/generator methodology parity: **MATCH** (same HJB→generator→transposed-KFE→stationary-distribution logic, same infinitesimal-generator convention, same shared operator). Differences are the expected consequences of the different state spaces (one-asset vs two-asset) — already documented as the structural parity mismatch in `DLH_3D_R1A_MAIN_REPORT.md`.
