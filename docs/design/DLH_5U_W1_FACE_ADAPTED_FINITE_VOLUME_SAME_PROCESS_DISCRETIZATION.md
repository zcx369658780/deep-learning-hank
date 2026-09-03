# DLH-5U — W1 Face-Adapted Finite-Volume Same-Process Discretization Contract

**Gate:** DLH-5U / Issue #47 — `SCIENTIFIC_DESIGN__W1_FACE_ADAPTED_FINITE_VOLUME_SAME_PROCESS_DISCRETIZATION`
**Date:** 2026-09-03
**Dedicated branch:** `dsh/issue-47-dlh-5u-w1-face-adapted-fv-design-2026-09-03`
**Fresh baseline:** `origin/main = 9ba4a530ba5e880d45433cec74d618e9461357b7`
**Status:** DESIGN-ONLY — no implementation, no execution, no `W_max` selection.

This is the umbrella contract of the DLH-5U design package. It freezes the Route-F
face-adapted finite-volume construction, records the honest scientific outcome, and
defines the frozen contract for a successor boundary-HJB implementation gate.

---

## 1. Authority

- Issue #47 (OPEN), activation comment `5520198694`, Owner decision
  `APPROVE_ROUTE_F_W1_FACE_ADAPTED_FINITE_VOLUME_OBLIQUE_FLUX_DESIGN`.
- Accepted upstream: DLH-5T (Issue #46, Outcome B, terminal
  `DLH_5T_W_DOMAIN_SCIENTIFICALLY_SUPPORTED__W1_DISCRETE_PROCESS_MATCHING_REQUIRES_BOUNDED_FOLLOWUP_DESIGN`);
  Issue #27 KFE contract (uniform-weight form, `BOUNDARY_POLICY_VIOLATION`
  fail-closed); DLH-5M KKT laws; accepted household source blob
  `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`.
- Full provenance, identity freeze and read-only evidence inventory:
  `reports/dlh_5u_w1_face_adapted_fv_same_process_2026_09_03/DLH_5U_AUTHORITY_AND_EVIDENCE_FREEZE.md`.

## 2. Frozen route-F construction (summary)

1. **Geometry (Phase 6).** Clipped control volumes `C_s = C_s^base ∩ D_W(W_max)`;
   `C_s^base` is the native Cartesian dual cell of the represented state
   `s=(a_j,b_i,z_n)`; the physical W face is the straight line `a+b=W_max`
   partitioned into the physical W segments `F_s^W` of cut cells — the staircase of
   masked nodes is not the physical boundary. Details:
   `DLH_5U_CONTROL_VOLUME_GEOMETRY_AND_BOUNDARY_LOCATION.md`.
2. **Boundary control location (Phase 7).** Node/cell-based constrained Hamiltonian
   (Option A/B): the control lives at the represented cell; boundary cells (positive
   `|F_s^W|`, or touching `a=0`/`b=b_min`/`a=a_max`) use the KKT-constrained policy;
   strictly interior cells use the interior FOC; W-face KKT only on cells with a
   physical W segment; explicit `h->0` interpretation.
3. **Face-flux / CTMC rates (Phase 8).** `q_{s->r} = |F_{s,r}| max(mu_s.n_{s,r},0)/omega_s`;
   source-state (upwind) drift; `max(.,0)` monotonicity; diagonal `= -sum(assembled
   off-diagonal rates)`; masked destinations not assembled and not retained in the
   diagonal; physical W/axial faces carry no flux (`max(mu_W,0)=0` by KKT).
   Details: `DLH_5U_BOUNDARY_HAMILTONIAN_AND_FACE_FLUX_CONTRACT.md`.
4. **One discrete process + adjoint (Phase 10).** Single `Q`: backward HJB action
   `(Q V)_s` and forward mass dynamics `p_dot = Q^T p` use the same rates; total mass
   exactly conserved; junction with the interior operator is the same formula.
   Details: `DLH_5U_CTMC_GENERATOR_AND_DISCRETE_ADJOINT.md`.
5. **Tangential reallocation (Phase 9+14).** Frozen primary = the conservative
   monotone face-flux cascade (`s -> (i,j-1) -> (i+1,j-1) -> ...`, net displacement
   `(-da,+db)`, first-order sequence-consistent); oblique one-step exact-moment
   variant frozen for the a-dominant sub-cone (`|mu_a| db >= mu_b da`); the b-dominant
   sub-cone (`mu_b <= |mu_a| < (10/7)mu_b`) has NO one-step monotone
   pointwise-consistent representation on the W1 lattice with `da=10/19 != db=7/19`
   (impossibility argument) — the cascade is its only (sequence-level) monotone
   representation. Details:
   `DLH_5U_TANGENTIAL_REALLOCATION_AND_CONSISTENCY.md`.
6. **Mass vs density (Phase 11).** `omega_s = area(C_s)`, `M = diag(omega_s)`,
   `p = M g`; forward stationary `Q^T p = 0`; density stationary
   `M^{-1} Q^T M g = 0` (NOT `Q^T g = 0` with unequal `omega_s`); bounded notational
   clarification of Issue #27 (uniform case recovered when `omega_s` constant);
   aggregates weighted by mass; normalized density `g_s = p_s/omega_s`.
   Details: `DLH_5U_MASS_DENSITY_CONTAMINATION_COMPATIBILITY.md`.
7. **Contamination/pin (Phase 12).** Future pin acts on the mass variable `p`
   (component-pin normalization, downstream only); density reconstructed as
   `g = M^{-1} p`; original residual on the unmodified `Q^T M g`.
8. **Sliver / small-cell (Phase 13).** Frozen remedy: (a) a symbolic minimum
   cut-fraction admissibility condition for future `W_max` candidates
   (`omega_s >= delta*da*db` for all `s`, `delta` a frozen pre-registered threshold
   in the W_max adequacy protocol); (b) deterministic agglomeration of any
   sub-threshold sliver into the adjacent cell sharing the largest shared face,
   transferring measure/faces/flux identically on HJB and KFE sides; (c) no remedy
   loosened to obtain a PASS; no `W_max` selected to avoid cut cells.
9. **Consistency audit (Phase 14).** Ten-item audit: monotonicity OK, conservation OK,
   adjoint mass OK, local first-moment toward `(mu_a,mu_b)` OK at sequence level
   (pointwise exact on the a-dominant sub-cone only), W-normal boundary OK, tangential
   composition OK in the limit, refinement OK first-order, interior junction OK,
   z-switch OK, negative-b borrowing-rate-gap OK.
10. **`W_max` authority (Phase 16).** Preserved: `W_max` is a numerical truncation
    parameter selected by the nested DLH-5T adequacy protocol; Route F may add the
    geometric cut-fraction admissibility requirement of item 8 only; `W_max` is NOT
    selected here.
11. **Immutable economics (Phase 20).** All accepted accounting, controls, grid,
    taper, `z`-switch and `b_min/a_max` economics are untouched.

## 3. Outcome and terminal (frozen, honest)

Route F is **scientifically viable**: it resolves the DLH-5T discrete-process
non-uniqueness with a specific conservative monotone same-process face-flux CTMC,
preserving conservation, no outward W-normal flux, the z-switch and the negative-b
borrowing-rate-gap, with first-order refinement consistency. It does NOT overclaim
Outcome A: one bounded discrete-geometry object remains unresolved — the
unconditionally monotone, conservative, *pointwise*-generator-consistent tangential
boundary transition for the full admissible tangential cone on the accepted
`da != db` grid (the b-dominant sub-cone is representable only at sequence/first-order
level by the cascade; the exact one-step construction is not unconditionally
monotone). Route F is NOT Outcome C (no conservation / same-process / no-flux /
tangential-in-the-limit violation).

```text
Terminal: DLH_5U_ROUTE_F_SCIENTIFICALLY_VIABLE__ONE_BOUNDED_DISCRETE_GEOMETRY_OR_WEIGHTED_ADJOINT_OBJECT_REMAINS_UNRESOLVED
```

## 4. Allowlist (nine files, the only task changes)

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
implementation; no HJB/KFE/stationary/grid execution; no numerical `W_max`; no
b160/b180/b200; no grid/taper/economic change; no contamination sensitivity; no
`C,L,A,B`; no two-region rebuild; no PR/merge/close/successor/self-accept. Handoff /
`_decision_inputs.json` stay untracked.

## 6. Stop

The Builder stops for fresh ChatGPT review after committing and pushing only the nine
allowlist paths on the dedicated branch, verifying the remote SHA, and reporting.
