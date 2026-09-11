# DLH-5V-A — Regular Voronoi Frontier Phase and Adjacency (Umbrella Design)

**Issue:** deep-learning-hank #49 (DLH-5V-A) · **Task type:** `SCIENTIFIC_DESIGN__REGULAR_VORONOI_FRONTIER_PHASE_AND_ADJACENCY_CLASSIFICATION`
**Branch:** `dsh/issue-49-dlh-5va-voronoi-frontier-phase-adjacency-2026-09-10`
**Status:** umbrella design document for Checkpoints B (phase classification) and C (adjacency); current commits are explicit-stage — `CHECKPOINT_ONLY__NOT_SCIENTIFIC_ACCEPTANCE`. Final acceptance pending the Issue #49 terminal (companion file `DLH_5VA_TERMINAL_AND_FORBIDDEN_CHECK.md`).
**Authority:** GitHub Issue #49 = sole DSH Builder authority; live `main` = authority branch; ChatGPT = independent reviewer. Owner split-gate decision: `APPROVE_DLH_5VA_SPLIT_GATE__REGULAR_FRONTIER_PHASE_ADJACENCY_ONLY`.

## 1. Governing contract (frozen, DLH-5U Rev 1 / Route F — accepted; not re-derived here)

* Domain `D_W = {0 ≤ a ≤ a_max, b ≥ b_min, a+b ≤ W_max}`; represented nodes `S = {s=(a_j,b_i) : a_j+b_i ≤ W_max}`;
  restricted-Voronoi cells `C_s = {x ∈ D_W : ‖x−s‖ ≤ ‖x−r‖ ∀ r ∈ S}` partition `D_W` a.e. (DLH-5U Rev 1 partition
  theorem). Physical W-activity: `F^W_s = ∂C_s ∩ {a+b = W_max}`, counts iff `|F^W_s| > 0`.
* Frozen grid: `a_j = j·10/19`, `b_i = b_min + i·7/19`; no numerical `W_max`; symbolic
  `kappa = 19·(W_max − b_min) = N + θ`, `N = floor(kappa)`, `θ ∈ [0,1)`.
* Retained: W1/native coordinates (a, b, z); single flux matrix `q_{s→r} = |F_{s,r}|·max(μ_s·n_{s,r}, 0)/ω_s`
  (DLH-5U Rev 1 contract) — referenced as the eventual consumer of the adjacency classification, **not** extended
  here (rates/moments are out of scope, §4).
* Housekeeping: household source blob VERIFIED `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`; no source mutation.

## 2. Scope of this gate (owner-approved)

Classify only the **regular, nondegenerate W-frontier phase structure** (Checkpoint B) and the **actual
restricted-Voronoi shared-face adjacency** of regular cells with exact displacement vectors (Checkpoint C).
Endpoint/corner cells, moment cones, (−1,+1) feasibility, transition rates, face-flux moment maps, endpoint
transitions, HJB/KFE, and stationary objects are explicitly deferred or forbidden (§4).

## 3. Accepted results of this gate (Checkpoints B + C, exact and spot-check-verified)

Let `i_t(j) = floor((N−10j)/7)`, `r_j = (N − 10j) mod 7 = (N − 3j) mod 7 ∈ {0,…,6}`, staircase drop `= 2` iff
`r_j ∈ {0,1,2}`, else 1; `r_{j+7} = r_j` (period 7), discrete phase = `N mod 7`.

**B. Phase classification** (details: `reports/dlh_5va_regular_voronoi_frontier_2026_09_10/DLH_5VA_PHASE_CLASSIFICATION.md`):
* Represented nodes: `10j + 7i ≤ N` (θ-independent, integer reduction). Node set fixed by N; θ moves only the
  frontier line `10x + 7y = N + θ`.
* Regular W-active cells: **top cell (A) always**; **sub-top cell (B) iff `r_j ∈ {0,1,2}`** (drop-2 columns;
  additionally `i_t(j) ≥ 2` for regularity); cells with `i ≤ i_t − 2` never W-active (max cell weight
  `≤ N − 5.5`).
* Exact W-face endpoints (j-units): A: `L = j + (14r+14θ−149)/340`; `R = j + (r+θ+7/2)/10` if `r ∈ {0,1,2}`,
  else `j + (14r+149+14θ)/340`; B: `[R_A, j + (14r+14θ+247)/340]`. Segments tile the regular frontier arc
  continuously (tiling identities exact). Per period: 7 A + 3 B = 10 W-segments.
* Invariant/sufficiency: `(N mod 7, θ)` complete; `N mod 7` alone fixes the discrete phase; no structural phase
  break in `θ ∈ [0,1)`; sole metric degeneracy = A₁/A₃₋₆ length tie at exactly θ = 1/2.

**C. Adjacency** (details: `reports/dlh_5va_regular_voronoi_frontier_2026_09_10/DLH_5VA_VORONOI_ADJACENCY_AND_DISPLACEMENTS.md`):
* Neighbor displacement census (θ-independent; `Δx_{sr} = ((10/19)Δj, (7/19)Δi)`):

| type | N_V | displacements (Δj,Δi) |
|---|---|---|
| INT (`i ≤ i_t−2`) | 4 | (−1,0), (0,−1), (0,1), (1,0) |
| A^F (`r ∈ {3,4,5,6}`) | 4 | (−1,0), (0,−1), (−1,1), (1,−1) |
| A^L (`r ∈ {0,1,2}`) | 3 | (−1,0), (0,−1), (−1,1) |
| B (`r ∈ {0,1,2}`) | 4 | (−1,0), (0,−1), (0,1), (1,−1) |
| B (`r ∈ {3,4,5,6}`) | 4 | (−1,0), (0,−1), (0,1), (1,0) |

* Only axial and diagonal displacement families occur; **no oblique or longer neighbors** (full candidate census).
* Masked-node-created adjacencies: diagonal NW (−1,1) on A-cells, diagonal SE (1,−1) on A^F- and B-cells;
  top cells lose their right/above axial neighbors (masked); A^L is the unique N_V = 3 cell.

## 4. Deferred / forbidden (explicit)

* **Deferred (later DLH-5V stages or successor issues, not this gate):** endpoint/corner cell phase & adjacency;
  moment-cone/rate design; use of the adjacency data in flux assembly (the `q_{s→r}` contract remains frozen as
  the consumer).
* **Forbidden in this task:** moment cones; (−1,+1) feasibility; transition rates; face-flux moment maps;
  endpoint/corner transitions; HJB/KFE; stationary objects; numerical `W_max`; mutation of the accepted
  household source; merging/self-accepting/closing Issue #49.
* **No existing tracked file modified;** only the five allowlist files of Issue #49 are written by the Builder.

## 5. File map

1. This umbrella design document.
2. `reports/dlh_5va_regular_voronoi_frontier_2026_09_10/DLH_5VA_AUTHORITY_CAPSULE.md` — authority digest.
3. `reports/dlh_5va_regular_voronoi_frontier_2026_09_10/DLH_5VA_PHASE_CLASSIFICATION.md` — Checkpoint B report.
4. `reports/dlh_5va_regular_voronoi_frontier_2026_09_10/DLH_5VA_VORONOI_ADJACENCY_AND_DISPLACEMENTS.md` — Checkpoint C report.
5. `reports/dlh_5va_regular_voronoi_frontier_2026_09_10/DLH_5VA_TERMINAL_AND_FORBIDDEN_CHECK.md` — finalize file (one Issue #49 terminal; forbidden-operation check).
