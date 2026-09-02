# DLH-5R — Raw-Gradient Provenance

**Issue #44 §4 gate — MUST precede scientific inference.**

## 1. Verdict

**PASS.** The raw transfer-FOC-consistent value gradients are recoverable from
the converged `value` by exact reconstruction with the accepted solver's own
finite-difference/upwind semantics, **without any source mutation**. The primary
S3 observable `R_hat = V_a_raw / V_b_raw` uses raw (unfloored) gradients; the
`MATLAB_DERIVATIVE_FLOOR` (1e-6) is never substituted into `R_hat` and in fact
never activated in any DLH-5R run.

The blocked terminal
`BLOCKED_DLH_5R_RAW_VALUE_GRADIENT_PROVENANCE_NOT_RECOVERABLE_WITHOUT_SOURCE_MUTATION`
is **NOT** triggered.

## 2. What the accepted solver exposes vs. what is reconstructed

The accepted solver (`solve_matlab_faithful_hjb`, source lines 511–563) computes
the raw gradients `vb_f`, `vb_b`, `va_f`, `va_b` inside every iteration but does
**not** expose them on `MatlabFaithfulHJBResult` (which carries `value`,
`consumption`, `labor`, `transfer`, `adjustment_cost`, `mu_a`, `mu_b`,
`liquid_label`, `transfer_label`, the operators, and convergence fields). They
are therefore **reconstructed** from the converged `value` using the exact
accepted formulas (source lines 528–542):

```text
vb_f[i-1] = (V[i]-V[i-1])/db,   vb_b[i]   = vb_f[i-1]           (b axis)
va_f[j-1] = (V[j]-V[j-1])/da,   va_b[j]   = va_f[j-1]           (a axis)
vb_b[0]   = resources(b_lo)^(-gamma_c)
vb_f[-1]  = resources(b_max)^(-gamma_c)
va_f[-1]  = 0  (a-upper interior zero),   va_b[0] = 0 (a-lower interior zero)
resources = (1-tau)*w*z*labor0 + transfer_income + r_b_eff*b,
            r_b_eff = r_b + rb_gap if b < 0 else r_b
```

This is algebraically identical to one more iteration of the accepted operator on
the converged value. `labor0` is the accepted baseline-labor array passed into
the solver (from the accepted deterministic fixture initialization), so the
b-boundary marginal-utility closures are reproduced exactly.

## 3. Which raw pair is economically active

- The transfer FOC (`transfer_candidate`) is evaluated on the **raw** gradients
  (Issue #23: the `1e-6` floor applies to consumption/labor only, never to the
  transfer FOC). Four raw pairs are evaluated (`d_bb, d_bf, d_fb, d_ff`); the
  active branch is selected from the shadow drifts.
- The accepted solution on the liquid tail is **dissaving** (`r_b < rho`, so
  `mu_b < 0`): 98.9–99.4% of primary evidence states have `mu_b < 0`, and 94.6–
  94.9% have the upwind pair a-forward/b-backward. Hence the economically-active
  raw `V_b` is the **backward** gradient `vb_b`, and the active `V_a` is the
  forward gradient `va_f` on ~95% of states.
- **Verification 1 (consumption FOC):** on dissaving primary states,
  `c = vb_b^(-1/gamma_c)` reproduces the accepted `consumption` array to a
  median relative error of **6.4e-10** (max 6.8e-10), confirming the
  reconstructed backward gradient is exactly the gradient the accepted
  consumption FOC uses (floor inactive).
- **Verification 2 (solver-level reproduction):** every run reproduces the
  accepted DLH-5J variant status exactly (iterations=10, identical convergence
  statistics, identical raw upper-b boundary maximum `4.291614197e-02`), so the
  underlying converged `value` is the accepted numerical solution.

## 4. Primary observable definition (as recorded)

```text
V_a_raw = va_f  if mu_a >= 0 else va_b          (raw, unfloored)
V_b_raw = vb_f  if mu_b >= 0 else vb_b          (raw, unfloored)
R_hat   = V_a_raw / V_b_raw
R_over_sqrt_b = R_hat / sqrt(b)
Q_hat   = b^2 * V_b_raw
```

Audit columns persisted per state: `V_a_raw_forward`, `V_b_raw_forward`,
`V_a_raw_backward`, `V_b_raw_backward`, `R_hat_ff = va_f/vb_f`,
`Q_hat_ff = b^2*vb_f`, so any alternative ratio is recomputable from
`DLH_5R_ALIGNED_TAIL_OBSERVABLES.csv`. Forward vs backward `V_b` differ by
~1% in the tail (e.g. vb_f=0.594, vb_b=0.599 at b=20.1); all scientific
conclusions are robust to this choice.

## 5. Floor and non-finite accounting

- `MATLAB_DERIVATIVE_FLOOR = 1e-6` activates on 0 states in every variant
  (full grid and primary evidence states). Floor activation is recorded
  separately (`floor_activated_bf`, `floor_activated_bb`) and would be
  classified as a numerical-semantic limitation if it had occurred; it did not.
- Non-finite counts are zero for `value`, all four raw gradients, consumption,
  transfer, and drifts in every variant.

## 6. Limits

The reconstruction is faithful to the accepted finite-grid operator and to the
accepted b-boundary marginal-utility closures. It inherits the finite-grid
semantics of the accepted solver (upwind differences, the `a=0`/`a_max` interior
zero-gradient convention for the non-active direction, and the b-boundary
closures); it does not claim anything about off-grid derivatives.
