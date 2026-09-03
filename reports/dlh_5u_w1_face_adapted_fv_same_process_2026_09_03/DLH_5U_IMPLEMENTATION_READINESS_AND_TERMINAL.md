# DLH-5U — Implementation Readiness and Terminal (Issue #47, Phase 15 + 17)

**Design only.** Records the implementation-readiness matrix, the honest outcome
decision, and the exact terminal.

---

## 1. Readiness matrix (frozen in this gate)

| Phase | Route-F deliverable | Status | Reference |
|---|---|---|---|
| 6 | Physical W-face vs staircase semantics (clipped control volumes) | FROZEN | `DLH_5U_CONTROL_VOLUME_GEOMETRY_AND_BOUNDARY_LOCATION.md` |
| 7 | Boundary-control location (node/cell-based constrained Hamiltonian with cut-cell FV correction; h->0 interpretation) | FROZEN | same |
| 8 | Monotone/conservative face-flux / CTMC rates (source-state upwind, `max(.,0)`, row sums 0, no masked-destination retention) | FROZEN | `DLH_5U_BOUNDARY_HAMILTONIAN_AND_FACE_FLUX_CONTRACT.md` |
| 9 | Tangential reallocation: cascade (conservative, monotone, sequence-consistent) + oblique exact-moment variant (a-dominant sub-cone) | FROZEN (viable scheme) | `DLH_5U_TANGENTIAL_REALLOCATION_AND_CONSISTENCY.md` |
| 9+14 | **Bounded unresolved discrete-geometry object**: unconditionally monotone *pointwise*-consistent tangential transition for the full admissible cone (`mu_b <= |mu_a|`) on the accepted `da != db` grid | **UNRESOLVED (impossibility argued)** | same |
| 10 | Same-process adjoint: one `Q` for `Q V` (backward) and `p_dot = Q^T p` (forward) | FROZEN | `DLH_5U_CTMC_GENERATOR_AND_DISCRETE_ADJOINT.md` |
| 11 | Mass vs density with nonuniform `omega_s`; `M = diag(omega_s)`, `p = M g`, `M^{-1} Q^T M g = 0`; Issue #27 bounded notational clarification | FROZEN | `DLH_5U_MASS_DENSITY_CONTAMINATION_COMPATIBILITY.md` |
| 12 | Contamination/pin placement (acts on mass `p`; downstream; density `g = M^{-1}p`; original residual on `Q^T M g`) | FROZEN | same |
| 13 | Sliver / small-cell: symbolic minimum cut-fraction admissibility for future `W_max` candidates + deterministic agglomeration fallback | FROZEN | umbrella contract §9 |
| 14 | Consistency audit (10 items) | OK except 14.4 pointwise exactness on b-dominant sub-cone (the unresolved object) | tangential report §6 |
| 16 | `W_max` authority preserved; geometric admissibility additions only | FROZEN | umbrella contract §10 |

## 2. Honest outcome decision

Route F is **scientifically viable**: it defines a specific, conservative, monotone,
same-process face-flux CTMC (the cascade) that resolves the DLH-5T non-uniqueness and
preserves conservation, no outward W-normal flux, the z-switch, and the negative-b
borrowing-rate-gap, with first-order refinement consistency.

Route F does **not** overclaim Outcome A: the pointwise-generator-consistent,
unconditionally monotone representation of the full admissible tangential cone on the
accepted `da != db` grid does not exist within one-step monotone schemes on the W1
lattice (the b-dominant sub-cone `mu_b <= |mu_a| < (10/7) mu_b` cannot be represented
pointwise; only the first-order cascade represents it in the sequence limit). This is
a genuine bounded discrete-geometry object that remains unresolved.

Route F is **not** Outcome C: no conservation / same-process / no-outward-W-flux /
tangential-reallocation-in-the-limit contract is violated.

**Frozen terminal (Outcome B):**

```text
DLH_5U_ROUTE_F_SCIENTIFICALLY_VIABLE__ONE_BOUNDED_DISCRETE_GEOMETRY_OR_WEIGHTED_ADJOINT_OBJECT_REMAINS_UNRESOLVED
```

The single bounded unresolved object is the discrete-geometry one (tangential
pointwise consistency on the b-dominant sub-cone); the weighted-adjoint (mass/density)
object is fully resolved.

## 3. What a successor implementation gate receives

A complete frozen contract for: clipped control volumes; node/cell-based constrained
Hamiltonian; source-state upwind face-flux rates; the cascade primary process; the
oblique variant restricted to the a-dominant sub-cone; the single `Q` adjoint; the
mass/density weighted stationary law; the downstream mass-pin; the sliver admissibility
+ agglomeration; and the ten-item consistency audit. The boundary-HJB implementation
is authorized only by a successor Issue.

## 4. Compliance

No source mutation; no implementation; no execution; no `W_max` selection; no
numerical objects. Design-only.
