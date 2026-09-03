# DLH-5U Rev 1 — Mass / Density / Contamination Compatibility (Issue #47, Phase 11 + 12)

**Rev 1 status:** DOCUMENTATION / ANALYTIC CORRECTION ONLY. Repairs BLOCKER 4
(Issue #27 MATLAB-style component pin) per reviewer comment `5521119160`. No
execution, no pin sensitivity, no pin-location optimization.

---

## 1. Mass vs density with nonuniform cut-cell weights (frozen)

For each represented cell `s` (state `(a_j,b_i,z_n)`), with `omega_s = area(C_s)`
from the Rev-1 restricted-Voronoi tessellation:

```text
M      = diag(omega_s)
g_s    = density of households at state s
p_s    = omega_s * g_s   (probability mass in cell C_s)
p      = M g
```

Forward dynamics (the generator's natural forward variable is the MASS):

```text
p_dot = Q^T p,   stationary:  Q^T p = 0,  sum_s p_s = 1
```

Density dynamics derived from the mass form:

```text
g_dot = M^{-1} Q^T M g,   stationary density:  M^{-1} Q^T M g = 0  <=>  Q^T M g = 0
```

**Notation rule (frozen):** with nonuniform `omega_s`, `Q^T g = 0` is NOT the correct
stationary density equation; the correct form is `M^{-1} Q^T M g = 0` (or the mass
residual `Q^T M g = 0`). The uniform special case (`omega_s = da*db` for all `s`) is a
bounded notational recovery of the Issue #27 statement; Issue #27 is not mutated.

## 2. Aggregates and density reconstruction (frozen)

```text
C = sum_s p_s c_s,   L = sum_s p_s l_s,   A = sum_s p_s a_s,   B = sum_s p_s b_s
g_s = p_s / omega_s,   sum_s omega_s g_s = sum_s p_s = 1
```

## 3. Original residual (frozen)

```text
residual = || Q^T p ||_inf = || Q^T M g ||_inf
```

evaluated on the UNMODIFIED generator `Q^T` at any candidate solution (never on a
pinned/modified operator).

## 4. Future contamination / pin placement (BLOCKER 4 repair — frozen)

The accepted Issue #27 contamination is the **MATLAB-style component-value pin**, not
a global normalization-row replacement. Rev-1 freezes the MASS pin as follows:

```text
T          = Q^T                       (full forward generator, z-switch included)
T_tilde    = T with row n replaced by e_n   (component pin at state n)
rhs[n]     = c > 0                     (positive contamination mass source at state n)
rhs[k]     = 0   for k != n
solve      T_tilde * p = rhs           -> raw p  (unnormalized)
normalize  p <- p / (sum_s p_s)        (post-normalization)
validate   original residual  || Q^T p ||_inf   at the pinned, normalized p
           plus sum_s p_s = 1 and p_s >= 0 (within tolerance)
```

Rules (frozen):

- The pin acts on the **mass variable `p`** (the generator's natural forward
  variable, consistent with Issue #27 which pins the value at a native component
  state). Density is reconstructed afterwards as `g = M^{-1} p`.
- The row replacement is `T_tilde[n,:] = e_n` and the RHS entry is `c > 0` — this is
  the component pin; it is NOT a `sum p = 1` row.
- If a future authority prefers a DENSITY pin instead (`g_n = c`), it must state and
  justify that choice explicitly and map it consistently through `p = M g` (i.e. the
  corresponding row becomes `e_n M^{-1}` with RHS `c`); Rev 1 does not select it.
- No pin-location optimization. No pin sensitivity. No change to the `0.37*N` parity
  convention.
- Post-normalization and original-residual validation are mandatory.

## 5. Compliance

No mass matrix built, no generator assembled, no residual computed, no pin applied.
Frozen contract for the successor implementation gate.
