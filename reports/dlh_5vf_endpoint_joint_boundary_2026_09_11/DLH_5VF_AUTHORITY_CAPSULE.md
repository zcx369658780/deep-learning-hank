# DLH-5V-F — Authority Capsule (Issue #54)

**Gate:** `SCIENTIFIC_DESIGN__ENDPOINT_BAND_AND_JOINT_BOUNDARY_FINITE_PROCESS_CLOSURE`
**Dedicated Builder branch:** `dsh/issue-54-dlh-5vf-endpoint-joint-boundary-2026-09-11`

## 1. Authority chain

- **Fresh live `main` at this gate (post-final-CURRENT-sync):**
  `cff55e7a75a7bb76d3186bc218233dff0c672d95` — verified by DSH fresh-fetch before any
  mutation; identical to the refresh-activation main `cff55e7…` in comment
  `5632615142`; HEAD message `Finalize active DLH-5V-F Issue #54 roadmap state`.
- **Issue #54 / DLH-5V-F:** OPEN, the sole active Builder authority (Task Index /
  Startup Snapshot / Master Roadmap CURRENT state at `cff55e7…`).
- **Activation comments:** `5632596303` (authoritative activation,
  `DLH_5VF_ENDPOINT_BAND_AND_JOINT_BOUNDARY_FINITE_PROCESS_CLOSURE_AUTHORIZED`,
  owner decision `APPROVE_DLH_5VF_ENDPOINT_BAND_AND_JOINT_BOUNDARY_FINITE_PROCESS_CLOSURE_GATE`)
  and `5632615142` (authoritative activation refresh, final CURRENT sync, fresh main
  `cff55e7a75a7bb76d3186bc218233dff0c672d95`).
- **Prior accepted gate:** Issue #53 / DLH-5V-E — **accepted candidate**
  `ff4607ff74ab1e0cea530ba04f17045698f43a62`, acceptance `5632150936`, integration
  `28e42e4c0f65d03aa403cf7aeedb60b83c7837e2`, terminal
  `DLH_5VE_FULL_REGULAR_W_BOUNDARY_SECTOR_CONTRACT_FROZEN__READY_FOR_ENDPOINT_JOINT_BOUNDARY_GATE`.
  The earlier candidate `98872fe16a355efb24264e5b9211f87cfe4a687b` was the
  **pre-Micro-Rev** candidate of that gate; reviewer `5631930098` was its
  pre-acceptance Micro-Rev request (not an acceptance).
- **Accepted household source (immutable):**
  `src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`, blob
  `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e` — re-verified at this gate.
- **Binding Issue #27 law:** `HJB boundary policy <=> KFE boundary transition law`.

## 2. Frozen inputs (unchanged this session)

- Domain `D_W(W_max) = { 0 <= a <= a_max, b >= b_min, a + b <= W_max }`, `b_min = -2`,
  `a_max = 10` (independent upper-a authority, `j_max = 19`).
- Grid `a_j = j*(10/19)`, `b_i = b_min + i*(7/19)`; nodes `10 j + 7 i <= N`,
  `N = floor(19 (W_max - b_min))`; symbolic `W_max`, no numerical selection.
- Economic boundary laws: `a=0: mu_a>=0`, `b=b_min: mu_b>=0`, `a=a_max: mu_a<=0`,
  `W: mu_a+mu_b<=0`, applied jointly on actually active faces.
- Wide stencils and availability: forward `(j,i)->(j-7,i+10)` iff `j>=7`; mirror
  `(j,i)->(j+7,i-10)` iff `j<=12` and `i>=10`; regular region `7<=j<=12, i>=10`;
  deferred complement `j in {0..6}`, `j in {13..19}`, `i <= 9`.
- Sector rate formulas (accepted DLH-5V-D/E, frozen): `T_realloc` (`q_in = 19*(-mu_W)/10`,
  `q_T = 19*mu_b/70`), `R_reverse` (`q_RT = 19*mu_a/70`, `q_down = 19*(-mu_W)/7`),
  `R_deplete` (`q_left = 19*(-mu_a)/10`, `q_down = 19*(-mu_b)/7`).
- Same-process law: candidate control -> continuous admissibility -> candidate-specific
  represented nonnegative rates -> discrete `H_h` score -> ONE global statewise argmax
  -> ONE conservative backward `Q`; future exact KFE consumes exactly `Q^T`.
- Stationary KFE: **NOT AUTHORIZED**.

## 3. Builder decision

**Outcome C — finite-process representability obstruction.** At least one
continuously admissible deferred-state drift class cannot be represented by any
nonnegative combination of actual allowed native-grid destinations under the frozen
exact same-process contract (exact W-tangent sliding rays at exact-frontier
(`r_j = 0`) a-interior top cells; universal across every `N >= 190` in the current
regular-Regime-I symbolic family — no claim is made for other `W_max` regimes, and no
numerical `W_max` is selected).

**Exact terminal (posted on Issue #54):**

```text
DLH_5VF_ENDPOINT_JOINT_BOUNDARY_FINITE_PROCESS_OBSTRUCTION__OWNER_ROUTE_DECISION_REQUIRED
```

## 4. Science evidence (exact, tiny)

- Exact closed-form certificates (audit report §4–§7): at `r_j = 0` cells no
  represented destination has `Delta W > 0`; `mu_W = 0` forces same-W mass only;
  available same-W rays have the wrong orientation in the endpoint bands.
- Exact enumeration over `N in [190, 260]` (all seven residues mod 7, both bands,
  all top/sub-top deferred cells): certificate property verified cell-by-cell
  (121/121 exact-frontier cells; exact separation test, no exceptions); universality
  verified for the current `N >= 190` family (every residue has at least one
  obstruction cell; exact per-residue obstruction-cell tables in the audit report §8).
- Exact constructive decompositions for representable band cells
  (e.g. forward-sliding at `r_j >= 4` via `q_1*(j-1,i+2) + q_2*(j,i-1)` with
  `q_1 = 19 u/10`, `q_2 = 38 u/35`, exact `(-u, +u)`).
- Closable classes: cone equality with accepted sector cones (reverse at `j=0`,
  T_realloc at the b-min face, T_realloc/deplete at `j=19`); rates identical to
  regular formulas (seam-consistent).
- Tiny exact spot-checks were run in `%TEMP%` only and are not committed.

## 5. Governance state

- Issue #54 remains OPEN; Builder STOPs after push; no merge, no close, no successor,
  no self-accept.
- Only the six allowlist paths were created; no tracked file modified; no source
  mutation; no implementation; no numerical run.
- Verification artifacts: `git status` (only the six new files staged/committed plus
  pre-existing unrelated untracked files), `git diff origin/main...HEAD` (allowlist
  only), remote SHA = local SHA (post-push verification).
