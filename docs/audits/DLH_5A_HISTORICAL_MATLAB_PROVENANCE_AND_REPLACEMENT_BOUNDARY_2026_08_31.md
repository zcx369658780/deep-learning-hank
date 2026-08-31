# DLH-5A — Historical MATLAB Provenance and Replacement Boundary

- **Issue:** #24 (DLH-5A)
- **Task type:** `SCIENTIFIC_DESIGN__NETWORK_READY_TWO_REGION_FIXED_POINT_CONTRACT`
- **Status:** DESIGN / AUDIT ONLY (read-only provenance analysis; no mutation of legacy sources)
- **Branch:** `dsh/issue-24-dlh-5a-two-region-structural-contract-2026-08-31`
- **Baseline `origin/main`:** `08f291e765570bbaa6f7b343a3d4f3d627adcd4c`

This audit records the boundary between **historical MATLAB multi-province
provenance** (reference/reasoning source only) and the **new NSR-HANK A1/A2
authority** (the two-region real structural HA-GE outer-fixed-point contract frozen
by Issue #24). Historical material is read-only and is never automatically inherited
as new-model authority.

---

## 1. Purpose and boundary

Per project rules (`PROJECT_RULE_OVERVIEW_CURRENT.md`, `LEGACY_REFERENCE_BOUNDARY.md`):

- the new project is a **clean-slate model line**;
- historical MATLAB economic modules, variable semantics, candidate equations and
  failure modes may be **consulted**;
- historical calibration, numerical outputs, parser verdicts, code architecture and
  Results are **not automatically inherited**;
- any mechanism taken from legacy material must be redefined, re-tested and
  re-authorized inside the new project.

DLH-5A uses historical MATLAB **only** as provenance for the outer-iteration
architecture and as an explicit replacement-boundary inventory. Its hand-coded
spatial allocation rules are not the new-model target.

---

## 2. Source-availability note (provenance evidence base)

The Issue #24 controlling-sources list references a local provenance document
`DeepLearning_HANK_MATLAB_NATIVE_STEADY_STATE_OUTER_ITERATION_SCIENTIFIC_HANDOFF_2026_08_31.md`
"if available under Owner-designated references". A bounded, read-only search of the
two legacy roots
(`D:\MatlabProgram\2023年12月2日 多省份神经网络HANK`,
`D:\Zotero-Analytical-Workflow`) and the repository did **not** locate that exact
document. No legacy source was modified; no copy-out was needed for this Issue.

This audit therefore relies on the **authoritative provenance facts already
published in Issue #24 Section 8**, `DLH_STARTUP_SNAPSHOT_CURRENT.md`,
`DLH_HANDOFF_2026_08_31_NETWORK_CALIBRATION_ROUTE.md`, and
`DLH_MASTER_ROADMAP_CURRENT_2026_08_31.md` (all read from fresh `origin/main`).
If the referenced handoff document later becomes available, a future Issue may
deepen this table; nothing here depends on it.

---

## 3. Provenance vs new A1 authority table

| Historical MATLAB object / mechanism | Historical role (provenance) | A1/A2 new NSR-HANK authority | Status |
|---|---|---|---|
| Outer/nested fixed-point interpretation | steady state found by iterating a broader equilibrium map around conditional HA solves | same computational architecture (Section 6 of the contract) | **retained as architecture provenance** |
| Conditional regional HA stationary solves | HA solved given current prices inside the outer loop | same role; both regional HA blocks solve conditionally each turn | **retained** |
| Batch/synchronous old-state household semantics | household blocks read the same old state; no same-turn contamination | frozen as Owner Decision 4 (Jacobi/synchronous) | **retained** |
| `At` (illiquid assets) feeds productive private capital | historical route: illiquid assets, not liquid `Bt`, feed productive private capital | `K_i = M_i * A_i` with `A_i` = per-household illiquid-asset aggregate | **retained in spirit; new provisional closure** |
| `Bt` (liquid assets) role | historical liquid-asset aggregate; not the productive-capital input | `B_i` = per-household liquid-asset aggregate/**diagnostic**; explicitly NOT productive capital and NOT a clearing/root target | **retained as diagnostic only** |
| `GovInv` (government capital) | active government-capital / controller state (`K = K_supply + GovInv`) | **excluded** from A1/A2; may be reintroduced later only under a separate scientific Issue | **deferred** |
| `K = K_supply + GovInv` firm turn | historical firm turn: supply assets plus government capital, depreciation in firm investment/return accounting | replaced by `K_i = M_i * A_i` (deliberately simplified exploratory closure) | **replaced / simplified** |
| `Lt_seperate` hand-coded spatial allocation | hand-coded interregional labor allocation | replaced by the network interface `m^L / W^L / P^L`, flows `F^L`, destination `L^dest`, composite wage `wbar_i` (Owner Decision 3) | **replaced by network interface** |
| `wage_caculate` historical `phi/sigmau` formula | hand-coded wage formula | replaced by regional competitive firm block `w_i = (1-alpha_i) Y_i / L_i^dest` and composite gross wage `wbar_i = sum_j P^L_ij w_j` | **replaced** |
| `(Nprov-1)` cross-capital averaging | historical cross-province capital averaging | replaced by per-region `K_i = M_i * A_i`; no cross-capital averaging in A1/A2 | **replaced** |
| cross-province `rah` mapping | historical mapping across provinces | replaced by regional `r_i^a` from the local real firm block; interregional capital flows belong to a future `W^K` stage | **replaced / deferred (`W^K`)** |
| historical Taylor `rb` assignment | historical monetary `rb` rule | **not** used: `r_b` is exogenous/common in A1/A2; nominal HANK deferred to Track B | **replaced / deferred** |
| `GovInv` 0.9/1.1 GDP-target controller | historical government-capital controller | **excluded** from A1/A2 | **deferred** |
| `Zt` output-reset controller | historical controller | **excluded** from A1/A2 | **deferred** |
| `tKNratio` 0.6/0.4 controller | historical capital-ratio controller | **excluded** from A1/A2 | **deferred** |
| household nonconvergence / boundary failures | treated as diagnostic information | preserved as diagnostics; not reasons to invent a clearing equation (contract Sections 7, 8.5) | **retained** |

---

## 4. Precise `At` / `Bt` / `GovInv` distinction

Frozen semantics for A1/A2 (read from Issue #24 Section 8 and the handoff):

1. **`At` (illiquid assets)** — in the historical route, `At`/illiquid assets, not
   `Bt`, feed productive private capital. A1/A2 keep this intuition: `A_i` (the
   per-household illiquid-asset aggregate returned by the accepted HA kernel) feeds
   private productive capital via `K_i = M_i * A_i`.
2. **`Bt` (liquid assets)** — `B_i` is the per-household liquid-asset aggregate,
   an endogenous household object and a **diagnostic**. It is **not** productive
   capital, **not** a root target, and **must not** be forced to equal an arbitrary
   government bond supply. The superseded `B_hh = B_gov = 1` route is not authority.
3. **`GovInv` (government capital)** — historically an active government-capital /
   controller state (`K = K_supply + GovInv`, with depreciation entering firm
   investment/return accounting). A1/A2 **defer** `GovInv`; no government productive
   capital and no GDP-target controller enter the A1 contract.

The `K_i = M_i * A_i` closure is a **deliberately simplified exploratory NSR-HANK
prototype closure**, explicitly **not** a correction of, and **not** an exact
reproduction of, the historical firm turn.

---

## 5. Historical objects intentionally replaced or deferred

### 5.1 Replaced by A1/A2 network / structural interfaces

- `Lt_seperate` → `m^L / W^L / P^L / F^L / L^dest` labor-network interface;
- `wage_caculate` (phi/sigmau) → competitive regional firm block + composite gross
  wage `wbar_i = sum_j P^L_ij w_j`;
- `(Nprov-1)` cross-capital averaging → per-region `K_i = M_i * A_i`;
- cross-province `rah` mapping → regional `r_i^a` from the local firm block (capital
  flow network `W^K` is a later, separately authorized stage).

### 5.2 Deferred to later stages (not A1/A2)

- `W^K` / interregional capital flows (later Track A6);
- learned `W^L` (later Track A3/A4);
- genuine nominal HANK block incl. Taylor `rb` / Phillips / Fisher (Track B1/B2);
- `GovInv`, `Zt` output-reset, `tKNratio` 0.6/0.4 controllers (require a separate
  scientific Issue);
- 31-region scaling;
- policy/welfare/Results claims.

---

## 6. Unresolved items requiring future Owner authority

These are genuine open items that a later Issue (not DLH-5A) must decide:

1. **Genuine nominal HANK closure** (Track B1/B2): price-rigidity/Phillips object,
   monetary rule, Fisher relation, fiscal/debt treatment, consistency with
   household liquid and illiquid returns. Not resolved by A1/A2 (real prototype).
2. **Learned `W^L` identification** (Track A3/A4): OD-year data schema, feature
   schema, hold-out years/pairs, transparent gravity benchmark. A1/A2 use
   hand-specified `W^L` only.
3. **Capital-flow network `W^K`** (Track A6): transparent capital-flow baseline and
   supervision targets.
4. **`GovInv` / government productive capital** reintroduction: whether and how the
   historical `K = K_supply + GovInv` and its controllers return.
5. **Migration/commuting resource cost**: intentionally absent in A1/A2; whether to
   add later requires new authority.
6. **Two-region degeneracy**: with two regions the conditional off-diagonal `W^L` is
   degenerate (`W^L_12 = W^L_21 = 1` when outflow is positive); genuine
   destination-choice identification needs 3+ regions and a later Issue.
7. **Exact A2 numerical configuration**: `lambda`, `tol_w`, `tol_ra`, `max_iter`,
   retry policy, output root must be frozen by a separate A2 execution-specification
   Issue/config before any run.
8. **Learned regional parameter mapping `g_P`** (later `theta_P` tier-3 mapping):
   not part of A1/A2.

None of these is resolved by inventing a mechanism inside DLH-5A; each is
explicitly out of scope.

---

## 7. Read-only / forbidden-operation compliance

- No mutation of `D:\MatlabProgram\2023年12月2日 多省份神经网络HANK` or
  `D:\Zotero-Analytical-Workflow` (list/stat/search only);
- no copy-out was required for this Issue;
- no `src/**`, tests, configs, roadmap, governance, or other existing file is
  modified by DLH-5A;
- no implementation, HJB/KFE/GE execution, or neural training was performed;
- no historical spatial formula is adopted as new-model authority;
- no `B_hh = B_gov = 1`, no Brent/Newton/fsolve replacement of the ordered outer
  map, no invented closure.

---

*This audit establishes provenance/replacement boundaries only. It does not by
itself constitute a scientific PASS; acceptance is an independent-review decision
per project acceptance levels.*
