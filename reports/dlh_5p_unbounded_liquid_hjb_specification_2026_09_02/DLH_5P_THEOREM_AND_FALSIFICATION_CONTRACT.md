# DLH-5P Phase F — Theorem and Falsification Contract (Rev 4)

**Issue #42 Phase F (Rev 4).** States exactly what a future theorem would need to
establish before the DLH-5O `p=2` result could be promoted from conditional evidence to
a theorem, for each candidate S1/S2/S3. Rev 2 established that the `m=1/2` branch must
be **resolved** (not assumed away). Rev 3 added: corrected S1 (admissible V is
globally bounded and monotone in `b`; `V_inf` exists), corrected S2 (discounted-value
condition is vacuous under S1; replaced by the explicit tail-value selection
`V_inf = 0`, whose necessity is unproved), and the statement that S3's P-TR primitive
does **not** by itself prove the realized tail is `p=2`. **Rev 4 corrects the sign** of
the critical-branch `O(1/b)` equation (the optimized transfer Hamiltonian enters the
HJB positively), so the alternative family gives `c/b = (rho+r_b + 0.5 C/chi_1)/2` and
`mu_W/b = -0.0025 - 3C/(4 chi_1) < 0` (inward; no mean-reversion reversal claim). No
theorem is claimed in this task.

## F0. Target theorem (conditional, from DLH-5O, under an adopted P-TR primitive)

Under an analytic candidate with the interior balance, the adopted P-TR (preferably
`R=O(1)`) primitive, the `p=2` ansatz, and uniformity:

```text
V_inf = 0,  K = 4/(rho+r_b)^2 = 3265.3 (z-constant),
c/b -> (rho+r_b)/2 = 0.0175,   mu_W/b -> r_b - 0.0175 = -0.0025 < 0   (fixed-a liquid-tail inward).
```

The alternative `m=1/2` family (compact interior-`a`, `a >= a_bar`, `C = aL^2 >= 0`)
would give `c/b = (rho+r_b + 0.5 C/chi_1)/2` (sign corrected in Rev 4), `chi/b =
0.5 C/chi_1`, and `mu_W/b = -0.0025 - 3C/(4 chi_1) < 0` (inward) — so any theorem must
either resolve that family or rest on the adopted primitive.

## F1. Required theorem gates (per candidate)

| Gate | S1 | S2 | S3 |
|---|---|---|---|
| **Existence** of an admissible value solution on `(b_lo,+inf) x (0,a_max) x {z}` satisfying the HJB + endpoint laws | required | required | required |
| **Uniqueness / comparison** (or an equivalent selection argument) | NOT provided by S1 (family; `V_inf` free in `[-C,0]`) | via the `V_inf = 0` tail-value selection (which must be PROVED as necessity, not asserted; necessity currently unproved) | via S2 (if proved) + the adopted primitive |
| **Tail regularity** with an explicit **derivative-remainder expansion** (leading equivalences NOT differentiated term-by-term) | required | required | required |
| **Uniformity** over the claimed `(a,z)` support — full `[0,10]` vs compact interior-`a` stated separately | required | required | required (class is uniform by definition) |
| **P-TR** (`R=o(sqrt(b))` uniformly, or `R=O(1)`) — derivation OR justified adoption | not derivable; would need to be added | not derivable; would need to be added | adopted as an Owner primitive (no derivation claimed) |
| **Resolution (not assumption) of the critical `m=1/2` branch** | must resolve (admissible/unresolved now) | must resolve (the `V_inf=0` family passes S2) | must resolve OR show the adopted primitive is the correct selection (and justify its exclusionary cost) |
| **Asymptotic realization / no exotic competing regime** (the actual HJB solution realizes the `p=2` ansatz; no non-power/non-smooth tail) | required | required | required — P-TR alone does NOT establish this |
| **`V_b ~ K/b^2` coefficient convergence** (rate of `V_b b^2 -> K`) | required | required | required |
| **`c/b -> 0.0175`** and **`mu_W/b -> -0.0025`** (with `a`-independence and endpoint conventions) | required | required | required |
| **Critical-family drift sign** (`mu_W/b = -0.0025 - 3C/(4 chi_1) < 0` for the `m=1/2` family, `a>=a_bar`) | report as falsifiable sign statement | report as falsifiable sign statement | report as falsifiable sign statement (no mean-reversion reversal claim) |

## F2. Falsification conditions (would reject the candidate analytic specification)

1. **A constructed counterexample:** an S1- or S2-admissible smooth solution satisfying
   the interior HJB with a tail different from `p=2` (e.g., the `m=1/2` remainder
   family of Phase E, `p=1/2`, `p<2`, `p>2`, logarithmic, or non-power) that is
   balance-consistent would falsify the uniqueness of the `p=2` tail. Phase E shows the
   `m=1/2`/`p=2` family IS balance-consistent on the compact interior, so this is a
   live falsification class.
2. **A constructed `R` violation:** a smooth, uniform, balance-consistent expansion
   with `R` not `o(sqrt(b))` (e.g. the `m=1/2` family) falsifies the P-TR exclusion as
   a claim about S1/S2. Under S3 it is excluded by the primitive by construction, so it
   falsifies instead the claim that the primitive is "independently justified" or that
   it "proves the realized tail is `p=2`" (it does neither).
3. **Endpoint sensitivity:** if the tail coefficient `c/b` or the sign of `mu_W`
   depended on the `b_lo` lower-bound law, or on the `a_max` upper-`a` law, that would
   falsify the claim of asymptotic separation / `a`-independence of the tail result
   (Phase C robustness gate).
4. **Empirical (future) falsification:** a measurement under the accepted finite-grid
   source (in an authorized future experiment) showing `R = V_a/V_b` not `o(sqrt(b))`
   near `b_max`, or `V_b b^2` not converging to `K`, or `c/b` not near `0.0175`, would
   falsify the candidate's prediction of the realized tail — and would indicate the
   `m=1/2` family (or another branch) is realized. (No such experiment is run in
   DLH-5P.)
5. **Switch-spectrum inconsistency:** any tail whose `O(1/b)`-level balance forces a
   non-trivial coefficient to sit in the switch spectrum `{0,-2/3}` with a coefficient
   value not equal to the `rho`-perturbations that DLH-5O rules out would be a red
   flag. NOTE: the `m=1/2` family does NOT trigger this at its leading order (its
   altered system has positive interior solutions), so it is not excluded by this test.
6. **Drift-sign falsification (Rev 3; formula corrected in Rev 4):** any demonstrated
   smooth, balance-consistent branch with `mu_W/b >= 0` would falsify the claim that
   all admissible smooth dominant balances are inward; the `m=1/2` family has
   `mu_W/b = -0.0025 - 3C/(4 chi_1) < 0` for `C >= 0`, so it does not provide such a
   branch. A claim that the critical branch "reverses mean reversion" is falsified by
   the explicit drift accounting (Phase E E4).

## F3. What counts as "promoted to a theorem"

The `p=2` result is promoted from conditional evidence to a theorem only when, under an
Owner-endorsed candidate:

- an existence + comparison result selects the admissible value solution, with S2's
  `V_inf = 0` tail-value selection PROVED as a necessity (F1), not asserted;
- the `m=1/2` branch is **resolved** — either proved not realized as an actual HJB
  solution (Phase F research), or its realized coefficient is derived, or the adopted
  S3/P-TR primitive is established as the correct selection with its exclusionary cost
  accepted by the Owner;
- **asymptotic realization** is proved: the actual HJB solution realizes the `p=2`
  ansatz with no exotic competing regime (P-TR alone does not establish this);
- `V_b b^2 -> K`, `c/b -> 0.0175`, `mu_W/b -> -0.0025` are proved with explicit rates
  and an explicit derivative-remainder expansion;
- P-TR (or `R=O(1)`) is either derived or adopted as the Owner-endorsed admissibility
  primitive;
- the theorem is stated on the claimed `(a,z)` support with the Phase C endpoint
  conventions.

Until then, the DLH-5O statement `(rho+r_b)K - 2 sqrt(K) = S*K` and its consequences
remain a **conditional dominant balance** (valid only within the adopted P-TR class and
the full DLH-5O premise set), not a theorem.

## F4. Summary (Rev 4)

The contract now requires resolving the `m=1/2` branch rather than relying on its
exclusion. Under S1/S2 the branch is admissible/unresolved (its `V_inf=0` family passes
S2), so uniqueness of the `p=2` tail is NOT available; under S3 it is excluded only by
the Owner-adopted primitive, whose exclusionary cost must be made explicit and whose
realized-tail claim remains to be proved. The critical family's total-wealth drift is a
falsifiable sign statement (`mu_W/b = -0.0025 - 3C/(4 chi_1) < 0`, inward; Rev 4
corrects the `3/4` coefficient from the Rev 3 `1/4`). Falsification conditions
F2.1-F2.6 are concrete and testable by future analytic or (authorized) numerical work.
