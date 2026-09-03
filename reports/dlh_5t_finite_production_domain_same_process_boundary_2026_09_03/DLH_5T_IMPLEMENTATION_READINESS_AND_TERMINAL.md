# DLH-5T — Implementation Readiness Matrix and Terminal (Issue #46, Phase G + H)

**Design only.** Identifies which existing source objects a successor implementation
would extend/supersede (without mutating them) and returns exactly one terminal.

---

## 1. Readiness / impact matrix (Phase G)

Frozen classification of the accepted household source
`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py` (blob
`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`) relative to the Route-D design:

| Object | Status for successor | Notes |
|---|---|---|
| Economic params, utility, labor FOC, consumption FOC, transfer technology (`chi(d,a)`, `transfer_candidate`), taper `r_a_eff(a)`, drifts `mu_a, mu_b` | **Immutable accepted economics** | Not to be changed by any successor implementation |
| `select_matlab_faithful_local_policy` boundary masks (e.g., lower-a `d>=0`, upper-a `d<=0`, lower-b/upper-b handling) | **Boundary logic requiring new implementation (KKT)** | The MATLAB-faithful ordering is NOT KKT-equivalent (DLH-5M §2.4; this report §3.4/3.4): a successor must replace the boundary branch/relabeling with the constrained Hamiltonian/KKT policy of the HJB/KKT report, using the effective gradients per active face/intersection |
| `assemble_source_axis` / `assemble_source_operator` (upwind assembly, boundary truncation with diagonal retention) | **Generator logic requiring later same-process implementation** | The leaky boundary construction is superseded by the DLH-5D contract: diagonal = -sum(admitted rates), no outward-rate retention; on `D_W` the W-face stencil must follow the same-process rule (KFE report) |
| Interior upwind logic (uniform grid, b/a axial rates, z-switch `kron(switch, eye)`) | **Reusable source-faithful interior logic** | Retained in the interior; the successor adds the mask `a_j + b_i <= W_max` and the boundary/face handling |
| Stationary KFE solve / contamination (`matlab_contaminated_row_index`, `solve_matlab_faithful_stationary_kfe`) | **Later stationary-stage device** | Contamination remains a downstream numerical normalization device, applied only after an accepted same-process conservative generator exists (KFE report §5) |
| `aggregate_stationary_household`, two-region block | **Later aggregate/GE stage** | Not touched by this design |

Diagnostics/tests required of a successor (design list): per-state
active-face classification; KKT multiplier feasibility and complementarity;
primal tangent-cone residuals; boundary policy diagnostics (`c,l,d,mu_a,mu_b,mu_W`);
conservative generator row-sum / nonneg-offdiag / original-residual gates (DLH-5D
tolerances); W1 mask and W-face stencil consistency between HJB and KFE.

## 2. What DLH-5T freezes (summary of the package)

- `D_W(W_max)` geometry and economic/numerical classification (W-domain report §1).
- All continuous tangent-cone/KKT laws for every active face and feasible
  intersection (HJB/KKT report), including the lower-face `V + lambda` / upper-W-face
  `V - lambda` convention and the `lambda_W` linear-transfer cancellation.
- The same-process HJB-KFE law, diagonal rule, no-clipping / no-outward-rate-retention
  rules, and contamination-downstream placement (KFE report).
- The `W_max` adequacy protocol (method, not number; stages A-E) (Wmax report).
- W1 masked representation semantics up to the tangential-drift ambiguity
  (W-domain report §3.3 resolved, §3.4 open).

## 3. The specific unresolved item (Phase H evidence for the terminal)

The W1 masked-tensor discrete process near the slanted `W` face has a genuine,
specific **process-matching ambiguity**: the tangential component of an
HJB-admitted boundary drift (`mu_b > 0, mu_a < 0, mu_W <= 0` at a W-frontier state)
cannot be represented by the coordinate-aligned split upwind on the accepted axial
lattice (`da = 10/19 != db = 7/19`, so the face tangent is off-axis). Any axial-only
treatment either suppresses the tangential control (changing the process) or leaks;
a faithful representation requires an off-axis flux construction whose exact form is
not determined by the accepted science and cannot be validated in a design-only gate
(no execution authorized). This is exactly the Issue #46 §8 condition under which W1
is not implementation-ready at the design level.

## 4. Terminal

Return exactly one terminal, per Issue #46 §14:

```text
DLH_5T_W_DOMAIN_SCIENTIFICALLY_SUPPORTED__W1_DISCRETE_PROCESS_MATCHING_REQUIRES_BOUNDED_FOLLOWUP_DESIGN
```

Rationale:

- **Outcome B** (not A): the W-domain `D_W` economic/numerical logic and all
  continuous KKT laws are scientifically supported and frozen, but the W1 discrete
  masked-grid process-matching ambiguity of Section 3 prevents an
  implementation-ready contract.
- **Not Outcome C**: no scientific inconsistency of `D_W` or the same-process
  principle is demonstrated; the difficulty is a specific discrete representation
  ambiguity, not an inconsistency.
- **Not Blocked**: the accepted source/evidence is internally consistent and fully
  reconcilable; no upstream accepted authority needs changing.
- No terminal authorizes HJB/KFE execution or production integration.

Bounded follow-up design content (recommendation only, not created by Builder):
resolve the W1 W-face tangential-drift representation by choosing and freezing one of
(i) a face-adapted finite-volume scheme with explicit control volumes and normal
flux `mu_W` plus tangential face routing, (ii) tangent/corner-transport diagonal
transitions (with a grid-spacing analysis), or (iii) a W2 transformed representation
evaluated under separate authority — followed by a separate implementation-validation
gate for the frozen choice.

## 5. Stop

The Builder stops here for fresh ChatGPT review and, on acceptance, an Owner route
decision on the bounded follow-up design. No PR, merge, Issue close, successor Issue
or self-acceptance is performed.
