# DLH-5P Phase F — Theorem and Falsification Contract

**Issue #42 Phase F.** States exactly what a future theorem would need to establish
before the DLH-5O `p=2` result could be promoted from conditional evidence to a
theorem, for each candidate S1/S2/S3. No theorem is claimed in this task; this is a
contract for a future gate.

## F0. Target theorem (conditional, from DLH-5O)

Under an analytic candidate with the interior balance, P-TR (preferably `R=O(1)`), the
`p=2` ansatz, and uniformity:

```text
V_inf = 0,  K = 4/(rho+r_b)^2 = 3265.3 (z-constant),
c/b -> (rho+r_b)/2 = 0.0175,   mu_W/b -> r_b - 0.0175 = -0.0025 < 0   (fixed-a liquid-tail inward).
```

## F1. Required theorem gates (per candidate)

| Gate | S1 | S2 | S3 |
|---|---|---|---|
| **Existence** of an admissible value solution on `(b_lo,+inf) x (0,a_max) x {z}` satisfying the HJB + endpoint laws | required | required | required |
| **Uniqueness / comparison** (or an equivalent selection argument) | NOT provided by S1 (family) | via the transversality/no-Ponzi law (selects the constant) | via S2 + the admissible class |
| **Tail regularity** sufficient for `V_b`, `V_a`, and the transfer FOC (`C^1`; `C^2` for the balance) | required | required | required |
| **Uniformity** over the claimed `(a,z)` support (full `[0,10]` or interior) | required | required | required (class is uniform by definition) |
| **P-TR** (`R=o(sqrt(b))` uniformly, or `R=O(1)`) — derivation OR justified admissibility | not derivable; would need to be added | not derivable; would need to be added | assumed (admissibility); partially justified at dominant-balance level (Phase E) |
| **Exclusion/characterization of the critical `m=1/2` branch** | Phase E argument (Clairaut + `O(b^{1/2})` balance) formalized as a lemma | same | same + class exclusion |
| **`V_b ~ K/b^2` coefficient convergence** (rate of `V_b b^2 -> K`) | required | required | required |
| **`c/b -> 0.0175`** and **`mu_W/b -> -0.0025`** (with `a`-independence and endpoint conventions) | required | required | required |

## F2. Falsification conditions (would reject the candidate analytic specification)

1. **A constructed counterexample:** an S1- or S2-admissible smooth solution satisfying
   the interior HJB with a tail different from `p=2` (e.g., `p=1/2`, `p<2`, `p>2`,
   logarithmic, or non-power) that is balance-consistent would falsify the uniqueness
   of the `p=2` tail. (Phase E already rules out the `m=1/2` power branch as a smooth
   dominant balance; a non-power consistent tail would be a genuine falsification.)
2. **A constructed `R` violation:** a smooth, uniform, balance-consistent expansion
   with `R` not `o(sqrt(b))` would falsify the P-TR exclusion (and the S3 class).
   Phase E shows the power branches `R ~ b^m`, `m >= 1/2` are not consistent; a
   logarithmic or other non-power violation would be a real counterexample.
3. **Endpoint sensitivity:** if the tail coefficient `c/b` or the sign of `mu_W`
   depended on the `b_lo` lower-bound law, or on the `a_max` upper-`a` law, that would
   falsify the claim of asymptotic separation / `a`-independence of the tail result
   (Phase C robustness gate).
4. **Empirical (future) falsification:** a measurement under the accepted finite-grid
   source (in an authorized future experiment) showing `R = V_a/V_b` not `o(sqrt(b))`
   near `b_max`, or `V_b b^2` not converging to `K`, or `c/b` not near `0.0175`, would
   falsify the candidate's prediction of the realized tail. (No such experiment is run
   in DLH-5P.)
5. **Switch-spectrum inconsistency:** any tail whose `O(b^{1-p})`-level balance forces a
   non-trivial coefficient to sit in the switch spectrum `{0,-2/3}` with a coefficient
   value not equal to `rho`-perturbations that DLH-5O rules out would be a red flag
   (e.g., the `p<2`/`R=o(sqrt(b))` families already shown inconsistent).

## F3. What counts as "promoted to a theorem"

The `p=2` result is promoted from conditional evidence to a theorem only when, under an
Owner-endorsed candidate (recommendation: S3 with S2 selection law and S1 base):

- an existence + comparison result selects the admissible value solution (F1);
- the Phase E lemma (exclusion of `m=1/2` and the power branches) is formalized;
- `V_b b^2 -> K`, `c/b -> 0.0175`, `mu_W/b -> -0.0025` are proved with explicit rates;
- P-TR (or `R=O(1)`) is either derived or adopted as the Owner-endorsed admissibility
  class;
- the theorem is stated on the claimed `(a,z)` support with the Phase C endpoint
  conventions.

Until then, the DLH-5O statement `(rho+r_b)K - 2 sqrt(K) = S*K` and its consequences
remain a **conditional dominant balance**, not a theorem.

## F4. Summary

The contract is identical in structure for all three candidates; S2 supplies the
selection (uniqueness) ingredient that S1 lacks, and S3 supplies the derivative-control
ingredient needed for the coefficient theorem. The Phase E ruling-out removes the
`m=1/2` obstruction, so the contract is satisfiable in principle under S3 (conditional
on the class being Owner-endorsed and the theorem gates being met). Falsification
conditions F2.1-F2.5 are concrete and testable by future analytic or (authorized)
numerical work.
