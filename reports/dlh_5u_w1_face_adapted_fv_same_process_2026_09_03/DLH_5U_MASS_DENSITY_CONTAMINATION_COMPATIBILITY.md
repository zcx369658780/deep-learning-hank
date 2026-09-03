# DLH-5U — Mass / Density / Contamination Compatibility (Issue #47, Phase 11 + 12)

**Design only.** Freezes the mass-vs-density variable-weight contract under Route F
cut cells, the normalized-density reconstruction, aggregate weighting, the original
residual, and the placement of the future downstream contamination/pin. No execution.

---

## 1. Mass vs density with nonuniform cut-cell weights (frozen)

For each represented cell `s` (each `(a_j, b_i, z_n)` state):

```text
omega_s = area(C_s)      (cell measure; cut cells have omega_s < da*db)
M       = diag(omega_s)  (mass matrix)
g_s     = density of households at state s
p_s     = omega_s * g_s  (probability mass in cell C_s)
p       = M g
```

Forward dynamics (the generator's natural forward variable is the MASS):

```text
p_dot = Q^T p,   stationary:  Q^T p = 0,  sum_s p_s = 1
```

Density dynamics derived from the mass form:

```text
g_dot = M^{-1} Q^T M g,   stationary density:  M^{-1} Q^T M g = 0  <=>  Q^T M g = 0
```

**Critical notation rule (frozen).** With nonuniform `omega_s` (cut cells), the
shorthand `Q^T g = 0` is NOT the correct stationary density equation: it omits the
weight matrix. The correct form is `M^{-1} Q^T M g = 0` (equivalently `Q^T M g = 0`
for the mass-residual). Any future text writing `Q^T g = 0` with unequal `omega_s`
must first prove the weight absorption or use the mass variable `p`.

## 2. Relationship to Issue #27 (bounded notational clarification, no mutation)

Issue #27 (DLH-5D contract) states the stationary KFE in the uniform-weight form
(`cell_weight = db*da` per `z`-state; density and mass coincide up to a constant). Under
Route F the cut cells make `omega_s` nonuniform, which is a bounded notational
extension, NOT a contradiction:

- `p_s = omega_s g_s` is the mass variable;
- the uniform case is recovered with `omega_s = da*db` for every `s`;
- the forward stationary law `Q^T p = 0` (mass) is the generator's intrinsic form in
  both cases; the density form `M^{-1}Q^T M g = 0` specializes to `Q^T g = 0` only
  when `M = const`.

This clarification is recorded here; Issue #27 is not mutated. The `BOUNDARY_POLICY_VIOLATION`
fail-closed semantics and the contamination-as-downstream-normalization semantics are
preserved unchanged.

## 3. Aggregates and density reconstruction (frozen)

Economic aggregates weight by MASS (consistent with `p`):

```text
C = sum_s p_s c_s,   L = sum_s p_s l_s,   A = sum_s p_s a_s,   B = sum_s p_s b_s
```

Normalized density reconstruction:

```text
g_s = p_s / omega_s,   sum_s omega_s g_s = sum_s p_s = 1
```

## 4. Original residual (frozen)

For any candidate solution, the original-equation residual is the ORIGINAL unmodified
mass residual

```text
residual = || Q^T p ||_inf = || Q^T M g ||_inf
```

evaluated on the UNMODIFIED generator (never on a pinned/modified operator). This
preserves the Issue #27 rule that the pin is a downstream normalization device
validated against the original residual.

## 5. Future contamination / pin placement (frozen)

- The future pin acts on the **mass variable `p`** (the generator's natural forward
  variable): the component-pin normalization replaces one row of `Q^T p = 0` with
  `sum_s p_s = 1`, then `g = M^{-1} p` reconstructs the density.
- The pin is downstream-only: it never changes `Q` or the HJB controls; it selects the
  stationary mass distribution consistent with `Q^T p = 0` and unit total mass.
- The stationary contamination transfer target, once specified by a successor, is
  expressed in mass terms `p_s` and converted to density `g_s = p_s/omega_s` for
  any density comparison.
- Route F does NOT select, compute or validate the pin; this report only freezes
  the variable convention.

## 6. Compliance

No mass matrix is built, no generator assembled, no residual computed, no pin applied.
This is the frozen contract for the successor implementation gate.
