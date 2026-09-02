# DLH-5Q — Future Numerical Falsification Protocol (Design Only — NOT EXECUTED)

**Issue #43 (step 38).** Designs the future numerical falsification protocol against
the provisional S3 class. **Nothing here is executed in DLH-5Q.** Execution would
require separate Owner authorization and would still be subject to Issue #27 (stationary
KFE NOT AUTHORIZED; this protocol concerns the accepted finite-grid HJB solver only,
not KFE/density runs).

---

## P0. Purpose

Given the accepted finite-grid household HJB solver (immutable source, blob
`76ae5b14…`), obtain, on an interior liquid-wealth window well inside
`(b_lo, b_max)`, numerical proxies for the S3/p=2 tail observables and compare them
against the provisional-class predictions. The protocol's output is a **pass/fail
verdict for provisional S3 and for the p=2 promotion**, plus detection of the
out-of-class `m=1/2` signature.

---

## P1. Observables (proxies on the interior liquid window `[b1,b2]`, `b_max >> b2`)

| Observable | Proxy definition | Provisional S3 / p=2 prediction | Falsification signal |
|---|---|---|---|
| `V_a/V_b` | upwind finite-difference ratio `R_hat = va/vb` (respecting `MATLAB_DERIVATIVE_FLOOR`) | `R = O(1)` (bounded, flat or slowly varying, not growing) | `R` grows like `sqrt(b)` (m=1/2 signature) or diverges in the interior with no boundary artifact |
| `b^2 V_b` | `Q_hat = b^2 * vb` (upwind) on `[b1,b2]` | `Q_hat -> K = 3265.3` (z-constant) within tolerance | `Q_hat` does not plateau; plateaus at a z-varying value; or diverges/->0 |
| `c/b` | `consumption_from_vb(vb)/b` | `c/b -> 0.0175` | `c/b ->` a different constant, e.g. toward `(rho+r_b+0.5 C/chi_1)/2 > 0.0175` (m=1/2 family) |
| `d` order | `transfer_candidate(va,vb,a)/b` and raw `d` | `d = O(1)` (bounded) | `d ~ sqrt(b)` (m=1/2); `d` growing like `b` would violate `R=O(1)` economics |
| `chi` order | `adjustment_cost(d,a)/b` | `chi/b -> 0` (`chi = O(1)`) | `chi/b ->` positive constant `= 0.5 C/chi_1` (m=1/2 signature) |
| `mu_W/b` | `(mu_b + mu_a)/b` (transfer cancels) | `mu_W/b -> -0.0025 < 0` | any `mu_W/b >= 0` plateau would falsify the inward-drift statement |

---

## P2. Boundary influence and scaling logic

1. **Liquid-window selection:** choose `[b1,b2]` well inside `(b_lo, b_max)` so that
   upwind/scheme artifacts at `b_lo`/`b_max` are excluded (e.g. keep several grid
   points from both boundaries; use the converged-solution interior).
2. **`b_max` sensitivity:** repeat with two or more increasing `b_max` values; the
   observables must be stable across `b_max`. Strong `b_max` dependence of the tail
   observables flags an endpoint/scheme artifact (not an S3 falsification per se, but a
   protocol-quality failure).
3. **`b_lo` sensitivity (tail independence gate):** vary the `b_lo` treatment; the
   tail observables must be `b_lo`-independent. This tests the Phase F robustness gate.
4. **Log-log slope:** regress `ln(vb)` on `ln(b)` over `[b1,b2]`; the provisional
   `p=2` tail predicts slope `≈ -2` (`V_b ~ K/b^2`). Reject the p=2 promotion if the
   slope is outside tolerance (e.g. `|slope + 2| > tol`), after checking that the
   window is genuinely interior.
5. **Pass/fail thresholds:** set tolerances relative to the grid resolution (e.g.
   `Q_hat` within `5-10%` of `K` on the plateau; `R_hat` bounded by a constant with no
   systematic `sqrt(b)` growth over a decade of `b`; `c/b` within `5-10%` of `0.0175`;
   `chi/b -> 0` within `O(1/b)`).

---

## P3. Which result would falsify provisional S3 (or its p=2 promotion)

- **Falsifies provisional S3 (terminal C direction):** an S3-internal alternative with
  `R=O(1)` and `V_inf=0` (per the numerical proxies) whose tail is NOT p=2 — e.g.
  `Q_hat` converging to a z-dependent or non-`4/(rho+r_b)^2` value, or `c/b` not ->
  `0.0175`, or a non-power tail (log slope `!= -2`) while `R` stays bounded.
- **Falsifies the p=2 promotion (S3 not the realized model):** an interior `m=1/2`
  signature (`R ~ sqrt(b)`, `chi/b ->` positive constant, `c/b > 0.0175` toward the
  continuum) not explainable by a boundary artifact. This does NOT falsify S3 *as an
  admissibility class* — it falsifies the claim that the actual model lies in S3 and
  would trigger Owner redefinition (terminal C) or a route re-evaluation.
- **Pass:** all observables match the p=2/S3 predictions within tolerance over the
  interior window, stable across `b_max`/`b_lo` — then the S3/p=2 promotion is
  *numerically supported* (still not a theorem; existence/comparison remain analytic
  gates).

---

## P4. Execution constraints (binding for any future run)

- Only the accepted immutable finite-grid household HJB solver may be used.
- No stationary KFE, nullspace, density, tail-count, or aggregate run (Issue #27).
- No R/W/W1/W2/`W_max` selection, no new numerical `b_max`/`a_max`, no taper
  extrapolation.
- No grid/domain resolution experiments beyond what the protocol above specifies.
- Any execution requires separate Owner authorization and a new Issue.

---

## P5. Status

**DESIGN ONLY.** Not executed in DLH-5Q. Readiness: the protocol is complete and
concrete (observables, windows, thresholds, falsification logic) — hence the terminal
carries `FALSIFICATION_PROTOCOL_READY`.
