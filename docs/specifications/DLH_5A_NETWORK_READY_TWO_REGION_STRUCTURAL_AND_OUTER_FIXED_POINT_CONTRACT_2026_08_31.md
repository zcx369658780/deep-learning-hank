# DLH-5A — Network-Ready Two-Region Structural and Outer-Fixed-Point Contract

- **Issue:** #24 (DLH-5A)
- **Task type:** `SCIENTIFIC_DESIGN__NETWORK_READY_TWO_REGION_FIXED_POINT_CONTRACT`
- **Status:** DESIGN / SPECIFICATION ONLY (no implementation, no execution, no training)
- **Branch:** `dsh/issue-24-dlh-5a-two-region-structural-contract-2026-08-31`
- **Baseline `origin/main`:** `08f291e765570bbaa6f7b343a3d4f3d627adcd4c`
- **Accepted household foundation:** `src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`
  (post-issue-23 identity: blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`, SHA-256 `1795718C469FC3B427CAB8E3D5957C133BEAD6EACC9EF0A25A3EDB7211D1A024`)

This document freezes the **scientific design contract** for the A1/A2 network-ready
**two-region real structural HA-GE outer-fixed-point prototype**. It is a reviewed
design artifact only; it does not authorize implementation, HJB/KFE/GE execution,
neural training, or any Results claim.

---

## 1. Owner-frozen scientific decisions (binding, preserved exactly)

### Decision 1 — A1/A2 scientific role

The first network-ready regional prototype is a **two-region real structural HA-GE
outer-fixed-point prototype**:

- household block = accepted two-asset HA/HJB/KFE foundation;
- regional production/price feedback = real structural block;
- common liquid return `r_b`, regional taxes `tau_i`, transfers `T_i` are
  exogenous/config inputs;
- genuine nominal HANK closure is deferred to Track B (B1/B2).

A1/A2 must **not** claim a validated genuine regional nominal HANK policy model.

### Decision 2 — provisional private-capital closure

For A1/A2 freeze a **new NSR-HANK provisional scientific specification**:

```
K_i = M_i * A_i
```

where:

- `A_i` = normalized/per-household illiquid-asset aggregate returned by regional
  household block `i`;
- `M_i` = regional household mass / population scaling;
- `K_i` = home-region private productive capital used by firm `i`.

Competitive real firm block:

```
Y_i        = Z_i * K_i^alpha_i * (L_i^dest)^(1 - alpha_i)
w_i        = (1 - alpha_i) * Y_i / L_i^dest
r_i^a      = alpha_i * Y_i / K_i - delta_i
```

This closure is **not** claimed to be the `N=1` limit of historical MATLAB and is
**not** source-faithful replication of the old multi-province capital allocation.

`B_i` remains an endogenous household liquid-asset aggregate/diagnostic. It is not
productive capital, not a root target, and must not be forced to equal an arbitrary
government bond supply.

Government productive capital / `GovInv` is **deferred** from A1/A2.

### Decision 3 — labor-network and composite-wage contract

Household home-region identity is fixed in A1/A2; the household distribution does
not migrate between HA blocks.

Regional household block `i` first returns home-origin effective labor supply
`L_i^home`.

Origin outflow share `0 <= m_i^L <= 1` and conditional destination weights
`W^L_ij >= 0` with `sum_{j != i} W^L_ij = 1`.

Complete labor-allocation matrix:

```
P^L_ii = 1 - m_i^L
P^L_ij = m_i^L * W^L_ij      (j != i)
sum_j P^L_ij = 1             (each origin row)
```

Labor-service flow:

```
F^L_ij = M_i * L_i^home * P^L_ij
```

Destination labor used by firm `j`:

```
L_j^dest = sum_i F^L_ij
```

No migration/commuting resource cost is introduced in A1/A2. Gross composite wage
seen by origin household `i`:

```
wbar_i = sum_j P^L_ij * w_j
```

Intended gross wage-bill identity:

```
sum_i M_i * L_i^home * wbar_i = sum_j w_j * L_j^dest
```

The accepted household kernel continues to receive a **scalar/one-element wage
interface**. A1/A2 do not broaden its destination-choice state and do not rewrite
the HJB labor choice.

Two-region note: with only two regions, conditional off-diagonal `W^L` is
mechanically degenerate (`W^L_12 = W^L_21 = 1` when outflow is positive). A1/A2
validate the `m^L / P^L / flow / accounting / fixed-point` interface; genuine
destination-choice identification begins at 3+ regions.

### Decision 4 — synchronous outer fixed-point semantics

The two regional HA blocks use **Jacobi / synchronous old-state semantics**:

- both household solves read the same `Gamma^(n)` snapshot;
- no region consumes another region's newly updated same-turn price/state;
- region iteration order must not change the mathematical one-turn mapping.

Historical MATLAB batch household semantics are provenance for this architecture
only.

---

## 2. Region index and two-region convention

Regions `i, j in {1, 2}`. All regional objects carry an explicit region index.

- A single common liquid return `r_b` is shared across regions (exogenous).
- Regional taxes `tau_i` and transfers `T_i` may differ across regions (exogenous).
- `rb_gap_i` is the regional borrowing-rate-gap input to the household kernel
  (may be region-specific config).
- `M_i` is regional household mass (number-of-households / population scaling),
  exogenous and strictly positive.
- `Z_i`, `alpha_i`, `delta_i` are regional real-firm technology parameters
  (exogenous, in the frozen A2 config).
- `m_i^L`, `W^L` (equivalently `P^L`) are **hand-specified** for A1/A2 (a
  deterministic network interface; learned `W^L` is a later, separately authorized
  stage).

---

## 3. Notation and normalization table (frozen)

Do **not** overload the same symbol for normalized (per-household) and region-total
quantities. This table is binding for A1/A2 code, diagnostics and reports.

| Symbol | Meaning | Domain | Type |
|---|---|---|---|
| `i, j` | region indices | `{1,2}` | index |
| `M_i` | regional household mass / population scaling | `(0, ∞)` | config/exogenous |
| `C_i` | normalized/per-household consumption aggregate | `(0, ∞)` | HA output |
| `L_i^home` | normalized/per-household home-origin effective labor supply (z-weighted) | `[0, ∞)` | HA output |
| `A_i` | normalized/per-household illiquid-asset aggregate | `[0, ∞)` | HA output |
| `B_i` | normalized/per-household liquid-asset aggregate (diagnostic) | `(-∞, ∞)` | HA output |
| `C_i^tot` | region-total consumption `= M_i * C_i` | `(0, ∞)` | derived |
| `A_i^tot` | region-total illiquid assets `= M_i * A_i` | `[0, ∞)` | derived |
| `B_i^tot` | region-total liquid assets `= M_i * B_i` (diagnostic) | `(-∞, ∞)` | derived |
| `L_i^tot` | region-total home-origin effective labor `= M_i * L_i^home` | `[0, ∞)` | derived |
| `m_i^L` | origin outflow share | `[0,1]` | hand-specified |
| `W^L_ij` | conditional destination weight (`sum_{j≠i}=1`) | `[0,1]` | hand-specified |
| `P^L_ij` | complete labor-allocation matrix (`sum_j=1`) | `[0,1]` | derived |
| `F^L_ij` | labor-service flow origin `i` → destination `j` | `[0, ∞)` | derived |
| `L_i^dest` | destination labor available to firm `i` | `[0, ∞)` | derived |
| `wbar_i` | gross composite wage seen by origin household `i` | `[0, ∞)` | derived |
| `w_i` | regional real wage (firm `i`) | `[0, ∞)` | outer state |
| `r_i^a` | regional real return on productive capital (firm `i`) | `(-∞, ∞)` | outer state |
| `r_b` | common liquid-asset return | exogenous | config |
| `tau_i` | regional labor-income tax rate | config | config |
| `T_i` | regional lump-sum transfer income | config | config |
| `rb_gap_i` | regional borrowing-rate gap | config | config |
| `Z_i` | regional TFP | config | config |
| `alpha_i` | regional capital share | `(0,1)` | config |
| `delta_i` | regional depreciation rate | config | config |
| `K_i` | home-region private productive capital `= M_i * A_i` | `(0, ∞)` | derived |
| `Y_i` | regional output (real firm block) | `(0, ∞)` | derived |
| `Gamma^(n)` | outer state snapshot `{w_1, w_2, r_1^a, r_2^a}` at turn `n` | — | outer state |
| `Gamma_hat^(n+1)` | candidate updated state from firm blocks | — | candidate |
| `lambda` | deterministic damping factor (if A2 authorizes) | `(0,1]` | frozen before run |
| `R_w, R_ra` | outer fixed-point residuals | `[0, ∞)` | trace |
| `tol_w, tol_ra` | convergence tolerances (A2 freeze) | `(0, ∞)` | A2 config |
| `max_iter` | outer-turn cap (A2 freeze) | `ℕ` | A2 config |

---

## 4. Household interface (frozen; kernel NOT redesigned)

For each region `i`, define the conceptual conditional interface:

```
HA_i(r_i^a, r_b, wbar_i, tau_i, T_i, rb_gap_i ; household/grid/numerical config)
    -> ( C_i, L_i^home, A_i, B_i, HJB_diag, KFE_diag, boundary_diag )
```

Mapping to the accepted kernel (all per-household, normalized):

- `r_a` in the kernel is the region's firm-return **candidate or old-state**
  `r_i^a` passed into the outer turn;
- `r_b` is the common liquid return;
- the kernel's scalar one-element `wages` vector is set to `[wbar_i]`;
- `migration_costs = [0.0]` and `labor_weights = [1.0]` (home-region identity
  fixed; no destination choice in A1/A2);
- `transfer_income = T_i`; `borrowing_rate_gap = rb_gap_i`;
- normalized aggregates map as:

```
C_i      = aggregates.c_ss
L_i^home = aggregates.l_ss          (z-weighted effective home-origin labor)
A_i      = aggregates.a_ss
B_i      = aggregates.b_ss
```

Required diagnostics (preserved and reported, never silently redesigned or tuned):

- HJB status: `hjb.converged`, `hjb.iterations`, `hjb.convergence_statistic`;
- KFE status: `kfe` density solve success/failure, mass error, `density_normalization`;
- boundary diagnostics: asset-grid boundary mass and any reported boundary warnings;
- non-finite/NaN diagnostics as exposed by the kernel/GE layer.

The existing accepted implementation uses one-element wage/labor vectors in the
source-faithful local policy path; A1 adapts regional information into that scalar
household price interface rather than expanding the HJB state/control problem.

---

## 5. Outer state and frozen/config inputs

### 5.1 Minimal endogenous outer price state

```
Gamma^(n) = { w_1^(n), w_2^(n), r_1^a(n), r_2^a(n) }
```

### 5.2 Frozen/config inputs (A1/A2)

At minimum:

- `r_b`;
- `tau_i`, `T_i`;
- `rb_gap_i`;
- `Z_i`, `alpha_i`, `delta_i`;
- `M_i`;
- hand-specified `m_i^L / W^L / P^L`;
- household/grid/numerical config;
- future A2 fixed-point numerical config (`lambda`, `tol_w`, `tol_ra`, `max_iter`,
  retry policy, output root) — **frozen separately before A2 execution**.

---

## 6. One-turn map (frozen order, synchronous/Jacobi)

Freeze the conceptual one-turn map:

1. Read immutable old snapshot `Gamma^(n)`.
2. Compute `P^L` from hand-specified `m^L, W^L`.
3. Compute `wbar_i^(n) = sum_j P^L_ij * w_j^(n)` for each origin.
4. Solve both conditional regional HA blocks against the **same** old snapshot.
5. Scale household aggregates using `M_i` (region-total objects).
6. Construct `F^L_ij` and destination labor `L_j^dest`.
7. Construct private productive capital `K_i = M_i * A_i`.
8. Evaluate both regional real firm blocks; obtain candidate prices
   `w_hat_i, r_hat_i^a`.
9. Construct candidate `Gamma_hat^(n+1)`.
10. Apply the separately frozen deterministic damping rule if A2 authorizes
    damping.
11. Record residuals, diagnostics and exact stopping reason.
12. Either accept, continue to the next synchronous turn, or fail closed.

No Taylor-rule update, `B` clearing root, `GovInv` GDP targeting, `W^K`, neural
network, or hidden adaptive controller belongs to this A1 contract.

### 6.1 Dataflow (conceptual pseudocode, non-implementation)

```
Gamma = init_gamma()                     # frozen A2 initial condition
for n in 0..max_iter-1:
    P_L    = build_PL(m_L, W_L)          # hand-specified
    wbar_i = P_L[i,j] * w_j  (per origin)
    hh_i   = HA_i(r_a=Gamma.r_a[i], r_b, wbar_i, tau_i, T_i, rb_gap_i)   # SAME snapshot
    (C_i, Lhome_i, A_i, B_i, hjb_diag_i, kfe_diag_i) = hh_i
    F_L[i,j]   = M_i * Lhome_i * P_L[i,j]
    Ldest_j    = sum_i F_L[i,j]
    K_i        = M_i * A_i
    (w_hat_i, r_hat_a_i) = firm_i(Z_i, alpha_i, delta_i, K_i, Ldest_i)
    Gamma_hat   = { w_hat, r_hat_a }
    if damping authorized: Gamma_next = (1-lambda)*Gamma + lambda*Gamma_hat
    else:                 Gamma_next = Gamma_hat
    R_w  = max_i |log(w_hat_i / w_i)|
    R_ra = max_i |r_hat_a_i - r_a_i|
    trace.append(n, Gamma, P_L_id, hh_diags, F_L, Ldest, K_i,
                 Gamma_hat, R_w, R_ra, damping_id, Gamma_next, stop_reason)
    if (R_w <= tol_w and R_ra <= tol_ra) and validity_gates_pass: stop(ACCEPTED)
    Gamma = Gamma_next
stop(MAX_ITER_REACHED)                    # nonconvergence = preserved evidence
```

Synchronous property: both `HA_1` and `HA_2` read `Gamma^(n)`; no `HA_i` sees
`Gamma_hat` values produced in the same turn. Reversing region order `(1,2) -> (2,1)`
must produce the identical one-turn map output (verified as a validity check, not
by silent reordering).

---

## 7. Fixed-point residual and trace contract

### 7.1 Residual definitions (frozen at design level)

```
R_w  = max_i | log(w_hat_i / w_i) |
R_ra = max_i | r_hat_i^a - r_i^a |
```

### 7.2 Damping (only if a later A2 issue/config freezes it)

```
Gamma^(n+1) = (1 - lambda) * Gamma^(n) + lambda * Gamma_hat^(n+1)
```

`lambda` is fixed before the run. No residual-dependent or PASS-seeking automatic
retuning is authorized by A1.

### 7.3 Trace contract (per iteration, frozen fields)

- iteration index `n`;
- input `Gamma^(n)`;
- `P^L` / labor-network config identity;
- both household statuses (`converged`, `iterations`, `convergence_statistic`);
- `C_i, L_i^home, A_i, B_i` and total-scaled counterparts;
- HJB/KFE/mass/boundary diagnostics;
- `F^L`, `L^dest`, `K_i`;
- candidate firm prices `w_hat_i, r_hat_i^a`;
- `R_w`, `R_ra`;
- damping identity/value;
- output state `Gamma^(n+1)`;
- explicit stop reason.

Failures/nonconvergence are **research evidence** and must not be silently
discarded or automatically tuned away.

### 7.4 Stop reasons (frozen vocabulary)

- `ACCEPTED` — residuals below frozen tolerances and all validity gates pass;
- `MAX_ITER_REACHED` — outer-turn cap reached without acceptance;
- `HOUSEHOLD_BLOCK_FAILED` — a regional HA solve fails closed (HJB/KFE/boundary);
- `INVALID_FIRM_STATE` — non-finite/non-positive factor state in the real firm
  block;
- `VALIDITY_GATE_FAILED` — a conservation/validity identity fails;
- `CONFIG_ERROR` — frozen config malformed.

---

## 8. Conservation and validity gates (frozen)

### 8.1 Labor origin conservation

For every origin `i`:

```
sum_j F^L_ij = M_i * L_i^home
```

### 8.2 Economy-wide labor conservation

```
sum_j L_j^dest = sum_i M_i * L_i^home
```

### 8.3 Gross wage-bill consistency

```
sum_i M_i * L_i^home * wbar_i = sum_j w_j * L_j^dest
```

### 8.4 Network validity

- finite entries;
- `0 <= m_i^L <= 1`;
- `P^L_ij >= 0`;
- origin rows sum to one;
- no hidden region-order dependence (synchronous one-turn property).

### 8.5 Household validity (preserve/report, not redesign)

- HJB convergence/nonconvergence status;
- KFE solve success/failure;
- finite density and normalization diagnostics;
- non-negativity diagnostics/tolerance interface;
- asset-grid boundary mass diagnostics;
- no automatic asset-grid expansion or PASS-seeking household tuning.

### 8.6 Firm validity

- finite positive `K_i` and `L_i^dest` required for interior Cobb-Douglas evaluation;
- finite `Y_i, w_i, r_i^a`;
- invalid zero/negative factor states **fail closed** rather than being clipped
  into a PASS.

A1 freezes diagnostic definitions/interfaces. Exact numerical tolerances not
already part of the accepted household kernel are **deferred** to the A2
execution-specification gate.

---

## 9. A2 implementation handoff checklist

The A2 issue/config must freeze (this list is a handoff, not authority):

- [ ] exact initial condition `Gamma^(0)`;
- [ ] exact hand-specified `m^L`, `W^L` (and derived `P^L`) for the two-region case;
- [ ] exact region configs: `Z_i, alpha_i, delta_i, M_i, tau_i, T_i, rb_gap_i, r_b`;
- [ ] exact household/grid/numerical config (reuse accepted kernel configs only);
- [ ] exact fixed-point numerics: `lambda`, `tol_w`, `tol_ra`, `max_iter`, retry
      policy, output root, no-overwrite rules;
- [ ] exact trace/output schema matching Section 7.3;
- [ ] exact validity-gate tolerance identities (Sections 8.1–8.6);
- [ ] explicit statement that `B_i` is a diagnostic only (no `B` clearing root);
- [ ] explicit statement that `K_i = M_i * A_i` is the provisional NSR-HANK closure;
- [ ] deterministic reproducibility and region-order-invariance checks;
- [ ] preservation of all nonconvergence/boundary failure evidence.

---

## 10. Scientific ceiling (frozen for DLH-5A)

Passing DLH-5A establishes only a reviewed **design contract** for a two-region
network-ready real structural HA-GE fixed-point prototype. It does **not**
establish:

- a working two-region equilibrium implementation;
- a converged regional steady state;
- a learned labor network;
- a learned capital network;
- genuine nominal regional HANK;
- calibration/data fit;
- 31-region results;
- policy/welfare/Results evidence.

Those require later separately published and activated Issues.

---

## 11. Non-authority list (explicit)

DLH-5A does not authorize:

- source/model implementation;
- HJB/KFE/GE numerical execution;
- household redesign;
- neural training or learned `W^L`;
- `W^K` or capital flows;
- government productive capital / `GovInv` integration;
- nominal rigidity / Phillips curve / Taylor/Fisher closure / new fiscal-debt closure;
- setting/solving `B_hh = B_gov = 1`;
- Brent/Newton/fsolve as a replacement for the ordered outer map;
- inventing `GovSurplus = 0` or any other unauthorized closure;
- copying old MATLAB spatial equations as the new target;
- 31-region scaling;
- policy/welfare/Results claims;
- tuning equations/parameters for PASS.

---

## 12. Acceptance summary (how this contract satisfies Issue #24 criteria)

1. preserves the four Owner decisions exactly (Section 1);
2. does not silently widen household economics (Sections 1.Decision-3, 4);
3. separates per-household from region-total aggregates (Section 3);
4. defines `m^L, W^L, P^L, F^L, L^dest`, composite wage unambiguously (Section 1.Decision-3);
5. shows labor and gross wage-bill conservation algebraically (Sections 8.1–8.3);
6. defines `K_i = M_i * A_i` explicitly as provisional new NSR-HANK authority (Section 1.Decision-2);
7. keeps `B_i` out of productive capital and arbitrary root clearing (Sections 1.Decision-2, 10);
8. defines synchronous/Jacobi one-turn semantics and no order dependence (Section 1.Decision-4, 6);
9. defines outer residual/trace/failure interfaces without PASS-seeking adaptive retuning (Section 7);
10. preserves HJB/KFE/boundary failures as diagnostics (Sections 4, 7.3, 8.5);
11. documents historical MATLAB provenance/replacement boundaries (see companion audit);
12. contains no implementation/training/Results claims (Sections 10–11).

---

*Terminal classification (set by the completion report):*
`DLH_5A_NETWORK_READY_TWO_REGION_STRUCTURAL_CONTRACT_COMPLETE__READY_FOR_GPT_REVIEW`
or an authorized `BLOCKED_*` class if a genuine ambiguity could not be resolved by
this Issue. This document itself claims no PASS.
