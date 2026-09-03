# DLH-5U Rev 1 — Implementation Readiness and Terminal (Issue #47, Phase 15 + 17)

**Rev 1 status:** DOCUMENTATION / ANALYTIC CORRECTION ONLY. Updates the readiness
matrix and the honest terminal after the four blocker repairs (reviewer comment
`5521119160`). No execution.

---

## 1. Readiness matrix (Rev 1)

| Phase | Route-F deliverable | Rev-1 status | Reference |
|---|---|---|---|
| 6 | Physical W-face vs staircase; **Rev-1 tessellation** = restricted Voronoi dual cells over the represented set, `D_W = ⊔ C_s` (a.e.) | FROZEN (BLOCKER 1 repaired) | `DLH_5U_CONTROL_VOLUME_GEOMETRY_AND_BOUNDARY_LOCATION.md` |
| 7 | Boundary-control object = node value + cell-level constrained control; W KKT iff `|F_s^W|>0`; cell-shrinkage convergence | FROZEN (BLOCKER 3 repaired) | same |
| 8 | Face-flux/CTMC rates (source-state upwind, monotone, conservative, no masked retention); **discrete Hamiltonian** `H_h`; continuous FOCs = consistency targets only | FROZEN (BLOCKER 3 repaired) | `DLH_5U_BOUNDARY_HAMILTONIAN_AND_FACE_FLUX_CONTRACT.md` |
| 9 | **Tangential reallocation** | **UNRESOLVED (candidate only)** — two-step cascade has O(1) spurious normal drift at fixed aspect ratio (tangent benchmark); oblique one-step not monotone on accepted grid | `DLH_5U_TANGENTIAL_REALLOCATION_AND_CONSISTENCY.md` |
| 10 | Same-process adjoint (one `Q`) | FROZEN | `DLH_5U_CTMC_GENERATOR_AND_DISCRETE_ADJOINT.md` |
| 11 | Mass/density with nonuniform `omega_s`; `M=diag(omega_s)`, `p=Mg`, `M^{-1}Q^T M g = 0`; Issue #27 bounded notational clarification | FROZEN | `DLH_5U_MASS_DENSITY_CONTAMINATION_COMPATIBILITY.md` |
| 12 | Contamination/pin: MATLAB-style component pin on mass `p` (`T_tilde[n,:]=e_n`, `rhs[n]=c>0`, solve raw, normalize, validate original residual) | FROZEN (BLOCKER 4 repaired) | same |
| 13 | Sliver: min cut-fraction admissibility for future `W_max` candidates + deterministic agglomeration; applied to the Voronoi cells | FROZEN | geometry report §2.6 |
| 14 | Consistency audit (10 items) | OK except 14.4/14.6/14.7 tangential consistency UNRESOLVED (the bounded object) | tangential report §7 |
| 16 | `W_max` authority preserved; geometric admissibility additions only | FROZEN | umbrella contract §9 |

## 2. Honest terminal decision (Rev 1)

Route F remains **scientifically viable in the framework sense**: after the repairs,
the frozen face-flux construction is conservative, monotone, same-`Q`, with no outward
W-normal flux and preserved z-switch / negative-b borrowing-rate-gap; the tessellation
is a genuine partition; the discrete HJB control and the MATLAB-style pin are frozen
correctly.

**The single precisely-bounded unresolved object** (unchanged in kind, now exactly
identified after the benchmark) is the tangential same-process consistency: a
conservative, monotone, same-process discrete boundary process whose effective
generator reproduces the full admissible tangential cone (including `mu_W = 0`
sliding) on the accepted `da/db = 10/7` W1 grid. The two-step cascade is NOT such a
resolution (O(1) spurious normal drift at fixed aspect ratio — derived, not assumed);
the oblique one-step is not monotone on the accepted grid. No impossibility is proven,
so Route F is not ruled out and Outcome C is not triggered.

**Frozen terminal (Outcome B):**

```text
DLH_5U_ROUTE_F_SCIENTIFICALLY_VIABLE__ONE_BOUNDED_DISCRETE_GEOMETRY_OR_WEIGHTED_ADJOINT_OBJECT_REMAINS_UNRESOLVED
```

The unresolved object is the discrete-geometry/tangential one; the weighted-adjoint
(mass/density/pin) object is fully resolved.

## 3. What a successor implementation gate receives

A complete frozen contract for: restricted-Voronoi control volumes; node value +
cell-level constrained control; source-state upwind face-flux rates; the discrete
Hamiltonian maximization; the single `Q` adjoint; the mass/density weighted stationary
law; the MATLAB-style component pin on `p`; the sliver admissibility + agglomeration;
and the ten-item consistency audit with the tangential object explicitly flagged as
unresolved. The boundary-HJB implementation is authorized only by a successor Issue.

## 4. Compliance

No source mutation; no implementation; no execution; no `W_max` selection; no
numerical objects. Design-only.
