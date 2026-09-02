# DLH-5M — Owner Decision Packet

**Issue #39 §11.** A concise decision packet for the Owner. No recommendation freezes
or changes the model. The Builder stops after producing this packet.

**Revision (2026-09-02, reviewer comment `5501914968`):** KKT statements use the
maximization convention `L = H - lambda*g` (effective gradients `V - lambda`);
`lambda_W` cancellation from the linear transfer term is preserved with its effect
retained through the adjustment cost; W-face activity is recorded only as the
`W_max`-conditional; a finite rectangular state constraint is distinguished from an
economic asset cap. Recommendation U is unchanged.

---

## 1. Exact recommended design

```text
DLH_5M_DOMAIN_GEOMETRY_DESIGN_EVIDENCE_INSUFFICIENT__OWNER_SCIENTIFIC_DECISION_REQUIRED
```

Neither Design R (rectangular componentwise KKT) nor Design W (hybrid joint-wealth
truncation) can be scientifically frozen on the accepted evidence alone. The
domain/boundary choice is an Owner scientific decision; before it is made, the
additional theoretical work in §6 must be performed.

## 2. Strongest evidence in favor

- **Total-wealth inwardness:** every inspected state (105/105) has
  `mu_W = mu_a + mu_b <= 0`; no inspected state has positive `mu_W`; all 44 material
  positive-`mu_b` states are `B_OUTWARD__TOTAL_INWARD`; all 17 top-layer offenders
  satisfy `mu_a <= 0` and `mu_W <= 0`.
- **Accounting additivity:** the *linear* part of the transfer `d` cancels one-for-one
  from `mu_W`, so `W = a + b` is a genuine accounting coordinate in which the linear
  reallocation control does not appear (the adjustment cost `chi(d,a)` remains, so `d`
  is not fully absent from `mu_W`).
- **KKT structure:** at a W face the constraint multiplier enters both value
  gradients symmetrically and cancels from the linear transfer FOC (surviving only in
  the adjustment-cost resource term); at an R corner the componentwise tangent cone
  makes net `b` accumulation inadmissible even when `a`-financed. W is therefore more
  consistent with the accepted portfolio-reallocation interpretation.
- These facts support W as the more economically coherent *hypothesis*.

## 3. Strongest argument against (freezing anything now)

- **Finite-state evidence:** `mu_W <= 0` is established only on the pre-frozen
  105-state set; it is not an infinite-domain mean-reversion theorem or stationary
  evidence.
- **`W_max` undefined:** no principled numerical/economic selection criterion exists;
  an artificial wealth cap could have economic consequences if it binds.
- **Cross-a sensitivity remains:** `rel_diff_mu_W` exceeds the pre-registered 1e-2
  threshold on 16/24 aligned pairs.
- **Representation and process unresolved:** W1 masked tensor has slanted-face
  stencil/conservation problems; W2 transformed `(a,W)` moves them to a slanted
  borrowing floor; conservative generator and exact HJB↔KFE process matching on the
  slanted face are undeveloped.
- **Design R is unestablished at the truncation face:** a finite rectangular state
  constraint need not be an economic law if treated as a numerical closure whose
  influence vanishes with truncation, but no such vanishing argument exists and the
  offenders satisfy total-wealth inwardness instead.

## 4. Equations / state constraints that would become controlling if Owner accepts

### If Owner accepts Design R

```text
a in [0, a_max],  b in [b_min, b_max]
upper-a: mu_a <= 0 ;  upper-b: mu_b <= 0 ;  corner: mu_a <= 0 AND mu_b <= 0
constrained HJB: sup over controls admissible to the active tangent cone
  with KKT multipliers (lambda_a, lambda_b), complementarity, and the maximization
  convention L = H - lambda_a*mu_a - lambda_b*mu_b (effective gradients V - lambda)
```

### If Owner accepts Design W

```text
D_W = { a >= 0,  b >= b_min,  a <= a_max,  a + b <= W_max }
W face: mu_W = mu_a + mu_b <= 0 ;  upper-a: mu_a <= 0
intersection a=a_max, W=W_max: mu_a <= 0 AND mu_W <= 0 (exists only for W_max >= a_max+b_min)
constrained HJB: sup with KKT multipliers (lambda_W on mu_W, lambda_a on mu_a),
  maximization convention L = H - lambda_W*mu_W - lambda_a*mu_a
  - lambda_W cancels from the linear transfer FOC; survives through the adjustment-cost term
  - W-face activity conditional on symbolic W_max: inactive if W_max > W,
    active if W_max = W, state outside D_W if W_max < W
KFE generator on D_W conservative, normal flux = mu_W on the slanted W face,
  sharing the same controlled process as the HJB
```

Neither is implemented by DLH-5M; these are the equations an implementation Issue
would have to freeze.

## 5. What remains unchanged

- The current rectangular computational domain and the MATLAB-faithful HJB source
  (blob `76ae5b149993a7edeeb337f1b02b3fe33c51e`).
- Frozen D0 economics (`wbar=1.0`, `r_a=0.03`), `a_max=10`, the accepted
  `a_max`-normalized taper, the transfer technology and adjustment cost, `b_min=-2.0`,
  `db=7/19`.
- The accepted DLH-5K/5L evidence set (read-only).
- Stationary KFE remains NOT AUTHORIZED (Issue #27).

## 6. What implementation task would follow (only after Owner decision)

A separate scientific implementation Issue, under fresh review, for the chosen design:
- R: a genuine rectangular state-constraint HJB/KKT boundary-value formulation
  (multiplier structure at every face and the corner), mirrored in the KFE;
- W: freeze the full `D_W` specification and numerical representation (including a
  principled `W_max` selection), then implement the constrained HJB and its
  conservative KFE counterpart on the identical controlled process.

No implementation authority exists until then.

## 7. What falsification / numerical validation would be required after implementation

- Inward drift (`mu_a<=0`, `mu_b<=0` or `mu_W<=0` as appropriate) on every active
  face and at every intersection;
- resolution robustness across the mature a-lattices (a77/a153) and b extents;
- conservative generator (mass conservation / discrete Gauss theorem across slanted
  faces if W);
- exact HJB↔KFE controlled-process matching;
- then Issue #27 stationary re-entry: recurrent-class/nullspace evidence, pin
  admissibility and valid-pin invariance, ORIGINAL `Q^T g` residual, mass and
  non-negativity, stationary-tail diagnostics; recompute `C,L,A,B` and the two-region
  anchor from scratch (no grandfathered aggregates).

## 8. Why stationary KFE still cannot begin immediately

The HJB↔KFE contract of Issue #27 requires an accepted, implemented and validated
domain/boundary controlled process. No such process exists yet: the current rectangle
has an unresolved truncation response, and neither candidate design is implemented.
Stationary validation can begin only after (a) the Owner decides, (b) the design is
implemented under separate authority, and (c) the boundary behavior, resolution
robustness, conservativity and process matching are validated.

## 9. Required additional theory before a domain choice (the U-path)

Concrete theory gaps to close before R or W can be frozen:

1. **Infinite-domain / asymptotic total-wealth analysis:** establish conditions under
   which `mu_W <= 0` persists as `W -> infinity` along the accepted a-lattice (using
   the transfer FOC, taper structure, and boundary consumption/wealth relationship),
   or exhibit a counterexample family. A theorem task, not a grid task.
2. **Principled `W_max` selection as a computational truncation:** a dimensionless /
   economic criterion (e.g. the smallest `W` beyond which stationary mass is provably
   negligible, or where `mu_W` is inward with a required margin). Because stationary
   is blocked, this must be an a-priori argument; alternatively a
   `W_max -> infinity` convergence argument.
3. **Formal joint HJB/KKT statements:** full constrained Hamiltonian for W (W face +
   intersections) and for R (rectangular faces + corner), including the transfer FOC
   coupling and taper compatibility, and whether the MATLAB-faithful ordering can be
   made equivalent to either.
4. **Generator / process-matching analysis:** conservative generator on the chosen
   domain (flux through slanted faces) and the HJB↔KFE duality on that domain.
5. **(Owner-scoped economic modeling decision):** whether `W` is a legitimate
   *production* truncation variable or only a computational device.

## 10. Stop

The Builder has produced this packet and now **stops for fresh ChatGPT review and an
Owner scientific decision**. No PR, merge, close, successor Issue or self-acceptance
is performed.
