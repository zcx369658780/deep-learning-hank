# DLH-5U Rev 1 — W1 Face-Adapted Finite-Volume Same-Process Discretization Contract

**Gate:** DLH-5U / Issue #47 — `SCIENTIFIC_DESIGN__W1_FACE_ADAPTED_FINITE_VOLUME_SAME_PROCESS_DISCRETIZATION`
**Rev:** 1 (bounded revision inside the same Issue, same branch, same allowlist)
**Date:** 2026-09-03
**Dedicated branch:** `dsh/issue-47-dlh-5u-w1-face-adapted-fv-design-2026-09-03`
**Fresh baseline:** `origin/main = 9ba4a530ba5e880d45433cec74d618e9461357b7`
**Rev-0 candidate (parent):** `69e9b33de27a74fad2d334f32c492e3abde6d9c6`
**Controlling reviewer authority:** `5521119160`
**Status:** DESIGN-ONLY — DOCUMENTATION / ANALYTIC CORRECTION ONLY. No implementation,
no execution, no `W_max` selection.

This umbrella contract of the DLH-5U Rev-1 design package freezes the corrected
Route-F construction, records the honest scientific outcome after the four blocker
repairs, and defines the frozen contract for a successor boundary-HJB implementation
gate.

---

## 1. Authority

- Issue #47 (OPEN), activation comment `5520198694`, Owner decision
  `APPROVE_ROUTE_F_W1_FACE_ADAPTED_FINITE_VOLUME_OBLIQUE_FLUX_DESIGN`.
- Rev-0 candidate `69e9b33…`; controlling fresh reviewer comment `5521119160`
  (BLOCKED, Outcome-B direction plausible, four repairs required).
- Accepted upstream: DLH-5T (Issue #46, Outcome B); Issue #27 KFE contract
  (MATLAB-style component pin, `BOUNDARY_POLICY_VIOLATION` fail-closed); DLH-5M KKT
  laws; accepted household source blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`.
- Provenance and Rev-1 authority: `DLH_5U_AUTHORITY_AND_EVIDENCE_FREEZE.md`.

## 2. Frozen Route-F construction (Rev 1)

1. **Geometry (Phase 6, BLOCKER 1 repaired).** Control volumes are the **restricted
   Voronoi dual cells** induced ONLY by the represented W1 node set:
   `C_s = { x in D_W : ||x-s|| <= ||x-r|| for all represented r }`, which
   **partitions** `D_W = ⊔_s C_s` (up to measure-zero boundaries) — proven, not
   assumed. The Rev-0 claim that masked nodes have zero-measure clipped cells is
   withdrawn. Interior cells = base dual rectangles; frontier cells = convex Voronoi
   polygons with a physical W segment `F_s^W = ∂C_s ∩ {a+b=W_max}`. `omega_s`,
   shared faces, adjacency, W segments and sliver logic are recomputed from this
   tessellation.
2. **Boundary control object (Phase 7, BLOCKER 3 repaired).** Node value + cell-level
   constrained control: `V_s` at the node; the control is a cell object whose drift
   enters the cell's face-flux rates; the W KKT (`mu_W <= 0`) is imposed iff
   `|F_s^W| > 0` (cell-boundary condition, never a bare node-point condition), with
   the cell-shrinkage convergence argument (`diam(C_s) -> 0`, node within `O(h)` of
   the face).
3. **Discrete Hamiltonian + face-flux (Phase 8, BLOCKER 3 repaired).**
   `H_h(c,l,d) = u(c) - v(l) + sum_r q_{s->r}(c,l,d)[V_r - V_s] + switch`; boundary
   controls maximize `H_h` subject to the cell tangent cone. Continuous DLH-5T
   effective-gradient FOCs are **consistency targets / refinement limits only**, not
   exact discrete FOCs. Rates: `q_{s->r} = |F_{s,r}| max(mu_s(c,l,d).n_{s,r},0)/omega_s`;
   monotone, conservative (row sums 0), no masked-destination retention, W segment
   zero flux by KKT.
4. **One discrete process + adjoint (Phase 10).** Single `Q`: `(Q V)_s` backward and
   `p_dot = Q^T p` forward use the same rates; total mass conserved; interior junction
   is the same formula. The tangential representation is a **candidate** (not frozen
   as a viable same-process resolution).
5. **Tangential reallocation (Phase 9+14, BLOCKER 2 repaired).** The Rev-0
   first-order consistency claims are **withdrawn**. Exact-tangent benchmark
   (`mu_a=-u, mu_b=+u, mu_W=0`, `da/db=10/7`): the two-step cascade
   `s->(i,j-1)->(i+1,j-1)` has mean cycle time `tau = 1/r_a + 1/r_b` and effective
   drift `(-da/tau, +db/tau)`; consistency requires `da=db`, which fails on the
   accepted grid — the effective W-drift is O(1) and does NOT vanish as `h -> 0` at
   fixed aspect ratio (concrete: half-cell `-(1/4)u`, full-cell `-(3/17)u`). The
   oblique one-step is not monotone on the accepted grid. The cascade is downgraded
   to a diagnostic/candidate construction; **the bounded unresolved object is
   tangential same-process consistency** (a conservative, monotone, same-process
   discrete boundary process reproducing the admissible tangential cone including
   `mu_W = 0` sliding on the accepted `da != db` W1 grid).
6. **Mass vs density (Phase 11).** `omega_s = area(C_s)`, `M = diag(omega_s)`,
   `p = M g`; stationary `Q^T p = 0` (mass) and `M^{-1}Q^T M g = 0` (density; NOT
   `Q^T g = 0` with unequal `omega_s`); Issue #27 bounded notational clarification.
7. **Contamination / pin (Phase 12, BLOCKER 4 repaired).** Issue #27 MATLAB-style
   component pin on the mass variable `p`: `T = Q^T`; `T_tilde[n,:] = e_n`;
   `rhs[n] = c > 0`; solve raw `p`; normalize; validate the ORIGINAL `Q^T p`
   residual. NOT a `sum p = 1` row. No pin-location optimization, no sensitivity,
   `0.37*N` parity preserved.
8. **Sliver / small-cell (Phase 13).** Symbolic minimum cut-fraction admissibility for
   future `W_max` candidates (`omega_s >= delta*da*db`) + deterministic agglomeration,
   applied to the Voronoi cells; no `W_max` chosen to avoid cut cells.
9. **Consistency audit (Phase 14).** OK: monotonicity, conservation, adjoint mass,
   W-normal no-flux, interior junction, z-switch, negative-b gap. **UNRESOLVED:**
   14.4/14.6/14.7 tangential consistency (the bounded object).
10. **`W_max` authority (Phase 16).** Preserved: `W_max` is a numerical truncation
    parameter selected by the DLH-5T adequacy protocol; Route F adds only the
    geometric cut-fraction admissibility requirement; not selected here.
11. **Immutable economics (Phase 20).** All accepted accounting, controls, grid,
    taper, z-switch, `b_min/a_max` economics untouched.

## 3. Outcome and terminal (frozen, honest)

Route F remains **scientifically viable in the framework sense** (conservative,
monotone, same-`Q`, no outward W-normal flux, genuine tessellation, discrete HJB
control, MATLAB-style pin), with one **precisely bounded unresolved object**:
tangential same-process consistency at W-adjacent cells on the accepted `da != db`
grid. No impossibility is proven (the cascade and oblique candidates fail, but Route F
is not ruled out), so Outcome C is NOT triggered; the gate does NOT force Outcome A
(which requires the tangential object resolved).

```text
Terminal: DLH_5U_ROUTE_F_SCIENTIFICALLY_VIABLE__ONE_BOUNDED_DISCRETE_GEOMETRY_OR_WEIGHTED_ADJOINT_OBJECT_REMAINS_UNRESOLVED
```

## 4. Allowlist (nine files, the only task changes — same paths as Rev 0)

1. `docs/design/DLH_5U_W1_FACE_ADAPTED_FINITE_VOLUME_SAME_PROCESS_DISCRETIZATION.md` (this file)
2. `reports/dlh_5u_w1_face_adapted_fv_same_process_2026_09_03/DLH_5U_AUTHORITY_AND_EVIDENCE_FREEZE.md`
3. `reports/dlh_5u_w1_face_adapted_fv_same_process_2026_09_03/DLH_5U_CONTROL_VOLUME_GEOMETRY_AND_BOUNDARY_LOCATION.md`
4. `reports/dlh_5u_w1_face_adapted_fv_same_process_2026_09_03/DLH_5U_BOUNDARY_HAMILTONIAN_AND_FACE_FLUX_CONTRACT.md`
5. `reports/dlh_5u_w1_face_adapted_fv_same_process_2026_09_03/DLH_5U_CTMC_GENERATOR_AND_DISCRETE_ADJOINT.md`
6. `reports/dlh_5u_w1_face_adapted_fv_same_process_2026_09_03/DLH_5U_TANGENTIAL_REALLOCATION_AND_CONSISTENCY.md`
7. `reports/dlh_5u_w1_face_adapted_fv_same_process_2026_09_03/DLH_5U_MASS_DENSITY_CONTAMINATION_COMPATIBILITY.md`
8. `reports/dlh_5u_w1_face_adapted_fv_same_process_2026_09_03/DLH_5U_IMPLEMENTATION_READINESS_AND_TERMINAL.md`
9. `reports/dlh_5u_w1_face_adapted_fv_same_process_2026_09_03/DLH_5U_FORBIDDEN_OPERATION_CHECK.md`

## 5. Forbidden operations (Phase 18)

See `DLH_5U_FORBIDDEN_OPERATION_CHECK.md`. No source mutation; no Route-F
implementation; no HJB/KFE/stationary/grid execution; no generator numerical
assembly; no grid/domain experiments; no numerical `W_max`; no b160/b180/b200; no
grid/taper/economic change; no contamination sensitivity; no `C,L,A,B`; no two-region
GE; no multi-province / neural / nominal / calibration / policy / welfare / Results;
no PR/merge/close/successor/self-accept. Handoff / `_decision_inputs.json` stay
untracked.

## 6. Stop

The Builder stops for fresh ChatGPT review after committing and pushing ONLY the nine
allowlist paths (Rev 1) on the same dedicated branch, verifying the remote SHA, and
reporting.
