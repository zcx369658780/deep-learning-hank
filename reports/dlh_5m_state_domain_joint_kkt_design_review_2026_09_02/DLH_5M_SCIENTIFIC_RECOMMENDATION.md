# DLH-5M — Required Scientific Recommendation

**Issue #39 §10.** The Builder must recommend exactly one of:

- `DLH_5M_RECTANGULAR_COMPONENTWISE_STATE_CONSTRAINT_KKT_RECOMMENDED__OWNER_SCIENTIFIC_DECISION_REQUIRED`
- `DLH_5M_HYBRID_JOINT_WEALTH_DOMAIN_AND_JOINT_KKT_RECOMMENDED__OWNER_SCIENTIFIC_DECISION_REQUIRED`
- `DLH_5M_DOMAIN_GEOMETRY_DESIGN_EVIDENCE_INSUFFICIENT__OWNER_SCIENTIFIC_DECISION_REQUIRED`
- `BLOCKED_DLH_5M_SOURCE_OR_ACCEPTED_EVIDENCE_INCONSISTENCY`

## Exact recommendation

```text
DLH_5M_DOMAIN_GEOMETRY_DESIGN_EVIDENCE_INSUFFICIENT__OWNER_SCIENTIFIC_DECISION_REQUIRED
```

(Recommendation U). No design is frozen; the Owner scientific decision is mandatory
before any implementation authority can exist. No recommendation freezes or changes
the model.

---

## Why not Design R

1. **The upper-b cap is a computational truncation, not an economic constraint.**
   The classification (`DLH_5M_CONSTRAINT_CLASSIFICATION.md`) labels `b <= b_max`
   a pure computational truncation: no economic reason bars liquid wealth above the
   route ceiling. A rectangular KKT law `mu_b <= 0` would convert this truncation
   into economic law.
2. **The accepted evidence does not justify R.** All 17 top-layer offenders violate
   rectangular `mu_b <= 0` while satisfying `mu_a <= 0` and `mu_W <= 0`. Under R
   these remain genuine KKT violations at a face whose economic status is unresolved —
   R would entrench the geometry whose basis is in question.
3. **The current solver is not R's KKT problem.** The accepted DLH-5K
   `joint_corner_feasibility` shows joint rectangular inwardness is infeasible at all
   17 offenders under the selected transfer candidate, and the current boundary
   closure is a finite-difference convention, not a KKT multiplier. R would require a
   large boundary-value reformulation whose economic premise is missing.
4. **Corner economics are inconsistent with rebalancing.** The R corner law taxes net
   `b` accumulation even when financed by `a` drawdown
   (`DLH_5M_JOINT_KKT_BOUNDARY_LAWS.md` §2.3), in tension with the accepted
   portfolio-reallocation interpretation.

## Why not Design W (yet)

1. **Finite-state evidence only.** `mu_W <= 0` holds on the pre-frozen 105-state set,
   not as an infinite-domain theorem. Freezing W would claim more than the evidence.
2. **`W_max` is undefined.** No principled selection criterion exists, and selecting
   one is explicitly forbidden in DLH-5M. A numerical `W_max` would be an artificial
   wealth cap with potential economic consequences (criterion C10).
3. **Cross-a total-drift sensitivity remains.** `rel_diff_mu_W` exceeds the
   pre-registered 1e-2 threshold on 16/24 aligned pairs; total-wealth robustness is
   improved but not established.
4. **Representation unresolved.** W1 (masked tensor) has slanted-face stencil /
   conservation problems; W2 (transformed `(a,W)`) moves the difficulty to a slanted
   borrowing floor. Neither is selected.
5. **Process matching / generator conservativity undeveloped.** Conservative
   generator with slanted-face flux and exact HJB↔KFE controlled-process matching are
   stated as design requirements, not established.

## Why not Blocked

The `BLOCKED_DLH_5M_SOURCE_OR_ACCEPTED_EVIDENCE_INCONSISTENCY` terminal does not
apply: the accepted source and evidence are internally consistent — J0–J5 reproduce
accepted HJB/boundary facts exactly, the `mu_W` identity and transfer cancellation
hold to machine precision, and the accepted evidence set is coherent.

## What the accepted evidence actually supports (tradeoffs, not PASS)

- It separates two facts: componentwise liquid outward drift under the rectangle, and
  total-wealth inward drift on the same states.
- It is consistent with W-inwardness on the inspected finite set and with the
  reallocation interpretation, which is why W is the more economically coherent
  *hypothesis* — but only a hypothesis on this evidence.
- It rules out the geometry-inconsistent shortcut (replace `mu_b<=0` by `mu_W<=0` at
  the corner) explicitly, because that is a PASS-seeking enlargement of the admissible
  cone, not a coherent boundary law.
- It cannot, by itself, choose between R and W; that choice requires the additional
  theoretical work itemized in the Owner decision packet and an Owner scientific
  decision.

## Recommended next gate (after Owner decision)

The Owner decision packet (`DLH_5M_OWNER_DECISION_PACKET.md`) itemizes the theory
gaps that must be closed before either design can be frozen. No implementation task
is recommended by DLH-5M; the next gate after the Owner decision is additional
theoretical work (infinite-domain/asymptotic total-wealth analysis, principled `W_max`
selection, formal KKT statements, generator/process-matching analysis), and only then
a separate implementation authority under fresh review.
