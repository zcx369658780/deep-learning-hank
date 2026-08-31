# DLH-5D — Conservative Stationary-KFE Boundary Law and MATLAB-Style Contamination Contract

- **Issue:** #27 (DLH-5D)
- **Task type:** `SCIENTIFIC_DESIGN__STATIONARY_KFE_BOUNDARY_AND_CONTAMINATION_CONTRACT`
- **Status:** DESIGN / PROVENANCE ONLY (freezes the scientific contract; NO source implementation or experiment execution)
- **Branch:** `dsh/issue-27-dlh-5d-kfe-boundary-contamination-contract-2026-09-01`
- **Baseline `origin/main`:** `b0ab6857f82434f89416b784c312682645163c10`
- **Revision:** R1 (2026-09-01) — per GPT review of candidate `d5cb5dd…`:
  `DLH_5D_DESIGN_SCIENTIFICALLY_STRONG__ACCEPTANCE_BLOCKED_PENDING_PIN_ADMISSIBILITY_AND_PROVENANCE_ORIENTATION_WORDING_REPAIR`.
  Adds pin-admissibility vs stationary-uniqueness distinction (Section 3.3), successor pin
  classification (Section 3.4), default-parity-pin rule (Section 3.5), uniqueness-gate caveat
  (Section 5), admissible-pin-only invariance with >= 2 valid pins (Section 7), and fixes the
  normalization-weight and orientation wording. All other accepted content is preserved.
- **Prior accepted gate:** Issue #26 / DLH-5C accepted at `c6b773323fa4d7fe480f4ae8a1523bcb97d8113c` —
  `DLH_5C_KFE_SINGULARITY_DIAGNOSTIC_ACCEPTED__FIXED_ROW_SELECTION_ARTIFACT_PRIMARY__OWNER_KFE_REDESIGN_DECISION_REQUIRED`

This specification freezes the scientific contract for the stationary KFE that a successor
implementation-validation task must satisfy. It separates (1) the mathematical stationary KFE
object, (2) finite-grid boundary / generator conservation, (3) the MATLAB-style contamination
method as a numerical normalization device, and (4) acceptance tests proving the contamination
does not change the stationary solution. It authorizes **no** code change and **no** model run.

Owner scientific clarification (Issue #27 body and activation comment, binding):

- The KFE generator `Q` is **expected to be singular**; singularity of `Q` is not a failure.
- MATLAB-style contamination / row replacement remains an **authorized** numerical normalization
  method in principle.
- A contaminated solution is scientifically accepted **only if** the normalized `g` also satisfies
  the ORIGINAL unmodified equation `Q^T g = 0`.
- For a conservative unique-stationary generator, deterministic alternative pin rows should
  recover the same normalized density within tolerance (bounded pin-row invariance).
- The redesign target is finite-grid generator **conservation / boundary-state-constraint
  semantics**, not the existence of singularity.

---

## 1. Frozen mathematical stationary KFE definition

The scientific stationary distribution is defined by the ORIGINAL unmodified system:

```text
Q^T g = 0
```

with normalization:

```text
sum_s g_s * cell_weight(s) = 1
```

and admissibility:

```text
g_s >= 0   (up to frozen numerical tolerance; Section 6)
```

where `Q` is the finite-state source/generator operator with the frozen convention:

```text
Q[row,col] > 0, row != col   =>   row -> col
```

so that:

- `Q V` = backward/HJB action;
- `Q^T g` = forward/KFE action;
- the stationary KFE is the forward/adjoint equation `Q^T g = 0`.

`cell_weight(s)` is the measure weight of state `s` used for integrals over the grid. In the
MATLAB-faithful convention the weight is exactly `cell_weight = db * dah` **per discrete z
state**: the two z values form a finite-state Markov process (transition block `Bswitch`), not a
continuum quadrature direction, so there is **no `dz` quadrature factor** and no "z-state
quadrature weight" multiplier (see the provenance audit, Section 3.5). The successor
implementation must freeze the same weight convention it integrates with, and the normalization
identity must be exact to the tolerance in Section 6.

## 2. Singularity is expected, not a failure

For a conservative generator with a unique stationary distribution, `Q` is expected to be
singular with a **one-dimensional nullspace (up to scale)**:

```text
nullspace dimension of Q^T  =  1
```

- Singularity of the unmodified `Q^T` must **not** be classified by any KFE solver or diagnostic
  as a numerical failure.
- The unmodified `Q^T g = 0` system is under-determined up to one scaling direction; mass
  normalization resolves the scale.
- A singular `Q^T` becomes numerically solvable only through a normalization device (e.g. the
  MATLAB-style contamination of Section 3), whose result must then be re-validated against the
  ORIGINAL equation (Section 3.2).

## 3. MATLAB-style contamination / row-replacement contract (authorized numerical normalization)

### 3.1 Algorithm (frozen form)

For a deterministic pin index `n` and a positive pin constant `c`:

```text
T        = Q^T
T_tilde  = T
T_tilde[n,:] = 0
T_tilde[n,n] = 1
rhs      = 0
rhs[n]   = c
raw      = solve(T_tilde, rhs)
g        = raw / ( sum_s raw_s * cell_weight(s) )
```

- The current MATLAB-faithful constant `c = 0.007` may be retained for parity/provenance.
- After normalization, the economically relevant density must not depend on the magnitude of a
  positive `c` except for numerical roundoff. Any material dependence of the normalized `g` on
  `c > 0` is a blocker.
- The pinned index convention remains `n = floor(0.37*N) - 1` (0-based, `N` = number of states)
  as the default parity pin candidate (see Section 4.3 for its non-privileged status).

### 3.2 Critical distinction: contaminated residual vs ORIGINAL residual

The contamination equation is a **numerical normalization device**, not the scientific stationary
equation.

- The contaminated-system residual `|| T_tilde @ raw - rhs ||_inf` measures only how well the
  pin device was solved. It is **insufficient** for scientific acceptance.
- A contaminated solve is accepted **only if** the normalized `g` also satisfies the ORIGINAL
  unmodified equation:

```text
|| Q^T g ||_inf  <=  tolerance_original_residual   (Section 6)
```

- The successor implementation must report **both** residuals per pinned solve:
  1. contaminated residual `|| T_tilde @ raw - rhs ||_inf`;
  2. original residual `|| Q^T g ||_inf` (with `g` the normalized density),
  and acceptance is gated on the ORIGINAL residual, not the contaminated one.

### 3.3 Pin admissibility vs stationary uniqueness vs contamination-row invariance

The design separates three distinct objects that must not be conflated:

1. **Stationary uniqueness** — the ORIGINAL `Q^T g = 0` has a one-dimensional nullspace (up to
   scale) on the canonical fixture (Sections 2 and 5). This says nothing, by itself, about which
   states carry positive stationary mass.
2. **Pin admissibility** — a MATLAB-style component-value pin `g_n = c > 0` is a legal
   scaling/normalization device **only if** the true stationary vector satisfies `g_star[n] != 0`.
3. **Contamination-row invariance** — among admissible pins, the normalized density must be
   recovered within tolerance.

The conditional contract (replaces any unconditional "any row works" statement):

- If `Q^T` has a one-dimensional nullspace **and** the true stationary vector has a nonzero
  component at pin `n` (`g_star[n] != 0`), then a component-value contamination `g_n = c > 0` may
  fix the scale and must recover the same normalized density as any other admissible pin.
- If the stationary component at `n` is zero (`g_star[n] = 0`), then `g_n = c > 0` is
  **inadmissible**: the component-value constraint is inconsistent with the ORIGINAL stationary
  equation. Even if `Q` is conservative and the stationary distribution is unique, that pin may
  be singular or may manufacture a vector that fails the ORIGINAL equation. Failure or a
  non-solution at such a row is **not** evidence against the stationary KFE itself.

Therefore the contract does **not** assert that "nullspace dimension = 1 implies any component
pin must succeed". A claim that **arbitrary** component pins are valid requires separately
establishing **irreducibility / strictly positive stationary support** (Section 5). Otherwise the
successor requirement is only **admissible-pin invariance**: the deterministic pin set is
classified per Section 3.4, and only pins classified `PIN_VALID_STATIONARY_NORMALIZATION` are
compared (Section 7).

- The successor implementation must prove **bounded pin-row invariance** among admissible pins on
  a deterministic diagnostic row set (Section 7).
- A fixed production row may be retained for reproducibility **only after** admissible-pin
  invariance is established (Sections 3.4-3.5).
- The current `floor(0.37*N)-1` row may remain the default parity pin candidate; it does **not**
  receive scientific privilege if it is inadmissible (Section 3.5).

### 3.4 Successor pin classification (frozen)

For the deterministic pin set (Section 7), the successor implementation must classify each pin
after the solve as exactly one of:

- `PIN_VALID_STATIONARY_NORMALIZATION` — conditions (at least): finite solve; normalized density
  finite; ORIGINAL `Q^T g` residual PASS (`<= tolerance_original_residual`, Section 6); mass
  normalization PASS (`<= tolerance_mass_normalization`, Section 6); density minimum PASS
  (`>= tolerance_min_density`, Section 6).
- `PIN_INADMISSIBLE_ZERO_STATIONARY_SUPPORT` — evidence supports that the stationary component at
  that pin is zero, i.e. the component-value constraint is inconsistent with the stationary null
  vector (e.g. bounded sparse null-vector / communicating-class diagnostics show zero stationary
  support at the pin).
- `PIN_NUMERICAL_FAILURE_UNRESOLVED` — neither valid stationary normalization nor zero-support
  inadmissibility can be established.

Only pins classified `PIN_VALID_STATIONARY_NORMALIZATION` are compared for normalized-density
invariance.

### 3.5 Default MATLAB parity pin rule (frozen)

- `floor(0.37*N)-1` may continue as the default parity / production pin candidate.
- In the successor, it must itself pass `PIN_VALID_STATIONARY_NORMALIZATION` (Section 3.4) to
  remain the production pin.
- If, after conservative repair, it is classified
  `PIN_INADMISSIBLE_ZERO_STATIONARY_SUPPORT`, STOP for scientific review. Do **not** automatically
  switch to another pin.

## 4. Finite-grid boundary / generator conservation law

### 4.1 Generator conservation (frozen)

For every represented state:

```text
sum_j Q[i,j] = 0      (within tolerance_* , Section 6)
```

Off-diagonal transition rates must be nonnegative up to tolerance:

```text
Q[i,j] >= 0   for i != j   (up to tolerance_negative_offdiag)
```

The diagonal must equal minus the sum of the **actually represented / admitted** off-diagonal
rates:

```text
Q[i,i] = - sum_{j != i} Q[i,j]
```

**No boundary rate may be kept in the diagonal if its destination transition is omitted.** The
current source-axis assembler (both MATLAB and the Python faithful port) truncates an outward
off-diagonal destination at a finite grid edge while retaining the corresponding rate in the
diagonal; DLH-5C established this produces materially negative row sums and probability leakage.
This contract forbids that construction for the successor conservative generator.

### 4.2 Economic state-constraint / no-outflow interpretation

At finite asset boundaries the represented process must obey a **no-outward-flux state
constraint**: the generator may not leak probability mass outside the represented grid.

The design must distinguish two objects:

1. **requested / economic outward drift or rate** produced by policy selection;
2. **admitted generator rate** after finite-grid boundary admissibility.

The implementation must **not** silently hide a materially outward economic policy. It must
**report suppressed outward boundary rates**. If economically requested outward flow exceeds the
frozen tolerance (Section 6), this is a `BOUNDARY_POLICY_VIOLATION` scientific blocker rather
than an automatic PASS.

Thus the successor implementation must both:

- assemble a conservative no-outflow generator (Section 4.1); and
- expose whether the underlying HJB policy itself respects the state constraint
  (`BOUNDARY_POLICY_VIOLATION` semantics, Section 4.3).

### 4.3 `BOUNDARY_POLICY_VIOLATION` fail-closed rule (frozen)

- Let `r_out(i)` be the economically requested outward boundary rate at a finite boundary state
  `i` (e.g. `max(s_i,0)/db` on the b-axis or `max(m_i,0)/da` on the a-axis, in the MATLAB/faithful
  flow notation) before boundary admissibility.
- If `max_i r_out(i) > tolerance_boundary_requested_outward` (Section 6), the canonical fixture
  is **blocked**: `BOUNDARY_POLICY_VIOLATION`. This is a scientific blocker even if the assembled
  generator is mechanically conservative.
- The violation must be reported with the offending states, coordinates and requested rates; it
  must not be silenced by clipping.

## 5. Stationary-class / uniqueness gate for the canonical validation fixture

For the canonical DLH-4B / DLH-5B validation fixture, the repaired stationary KFE must establish
a **unique normalized stationary distribution** before household aggregates are accepted.

- Required evidence may use bounded sparse rank/nullspace, communicating-class diagnostics, and
  contamination-row invariance (Sections 6-7).
- Target acceptance condition for this fixture:

```text
stationary nullspace dimension = 1
```

- If the repaired conservative generator instead has **multiple economically valid closed
  recurrent classes / multiple stationary measures**, STOP for Owner scientific decision. Do not
  choose a mixture implicitly through a pin row.
- `nullspace dimension = 1` does **not** imply full support: a unique stationary distribution may
  still have transient states with `g_star[n] = 0` (this is exactly the DLH-5C exposure — a
  conservative `a=0` recurrent class plus transient/leaky mass). Claiming that **arbitrary**
  component pins are valid requires separately establishing **irreducibility / strictly positive
  stationary support**; otherwise the successor requirement is admissible-pin invariance only
  (Sections 3.3-3.4, 7).
- DLH-5C established the current (un-repaired) operator has a conservative `a=0` class and a leaky
  546-state sink containing row 295; the successor conservative generator must re-derive its
  communicating-class / nullspace structure from scratch under Section 4.

## 6. Future numerical acceptance tolerances (frozen)

The successor implementation task must use the following exact tolerances. A different tolerance
is permitted only with an explicit numerical scaling analysis documented in the design/evidence;
a tolerance may not be loosened merely to obtain PASS.

```text
generator row-sum max abs              <= 1e-12
negative off-diagonal magnitude        <= 1e-12
original stationary residual ||Q^T g|| <= 1e-10
mass normalization error               <= 1e-12
minimum density                        >= -1e-12
multi-pin normalized-density max diff  <= 1e-10
repeat numeric difference              <= 1e-12
```

Boundary-policy requested outward rate:

```text
boundary requested outward rate        <= 1e-10
```

for a fully accepted canonical fixture. A larger value is a scientific boundary-policy blocker
(`BOUNDARY_POLICY_VIOLATION`) even if the assembled generator is mechanically conservative.

## 7. Deterministic contamination invariance set (frozen)

For future validation, freeze the bounded diagnostic pin set:

```text
{0, floor(N/4), floor(0.37*N)-1, floor(N/2), floor(3N/4), N-1}
```

Deduplicate if needed. Each pin is first classified per Section 3.4
(`PIN_VALID_STATIONARY_NORMALIZATION` / `PIN_INADMISSIBLE_ZERO_STATIONARY_SUPPORT` /
`PIN_NUMERICAL_FAILURE_UNRESOLVED`). For every pin that yields a finite solve, future acceptance
must record, per pin:

- pin classification (Section 3.4);
- normalized density (against every other **valid** pin, pairwise `max |g_p1 - g_p2|` on the
  shared grid);
- ORIGINAL `Q^T g` residual (Section 3.2);
- mass normalization error;
- density minimum.

Only pins classified `PIN_VALID_STATIONARY_NORMALIZATION` are compared for normalized-density
invariance. The contamination method is accepted on the canonical fixture only if **at least two
distinct valid pins** are found and their normalized densities agree within tolerance (Section 6),
with original residual, mass normalization and non-negativity all PASS for every valid pin. A pin
classified `PIN_INADMISSIBLE_ZERO_STATIONARY_SUPPORT` or `PIN_NUMERICAL_FAILURE_UNRESOLVED` is
**not** evidence against the stationary KFE. This test validates the **contamination method**, not
any particular row.

## 8. Household aggregate and two-region anchor revalidation sequence (frozen)

After a successor KFE implementation passes the contract, in this fixed order:

1. Recompute from scratch the canonical household stationary aggregates:
   ```text
   C, L, A, B
   ```
   from the newly accepted stationary density. **No aggregate from the current row-295 density is
   grandfathered.**
2. Revalidate the two-region exploratory closure:
   ```text
   K_i = M_i * A_i
   ```
   and re-derive the firm-anchor quantities:
   ```text
   Z*, delta*
   ```
   from the newly accepted stationary household aggregates.
3. If the corrected stationary solution gives `A <= 0`, non-finite `A`, or otherwise makes the
   `K = M * A` firm block invalid, **STOP for Owner decision**. Do not change household
   parameters, grids, `alpha`, or anchor prices to rescue the closure.
4. Issue #25 remains accepted only for architecture/wiring/Jacobi/accounting/trace semantics
   until this revalidation succeeds.

## 9. Explicit implementation non-authority

This specification is **design/provenance only**. It does NOT authorize:

- any HJB/KFE/household source change;
- any regional fixed-point code/config change;
- changing the current contaminated-row solver;
- implementing a new row selection;
- implementing conservative assembly;
- running D0-D3 or the two-region model;
- changing grids/parameters/prices/tolerances in code;
- regularization / jitter / pseudoinverse;
- changing `K = M * A`;
- OD data, learned `W^L`, larger regions, nominal HANK, calibration, policy/welfare or Results.

A successor, separately issued and separately authorized implementation-validation task will be
required before any of the above. This contract only freezes what that successor must satisfy.

## 10. Acceptance criteria for this design (DLH-5D)

1. singular `Q` explicitly recognized as expected stationary-KFE structure, not an error;
2. MATLAB-style contamination remains authorized as a numerical method, conditional on
   original-equation validation;
3. contaminated residual vs original `Q^T g` residual distinction is binding;
4. pin admissibility distinguished from stationary uniqueness, and admissible-pin (bounded
   pin-row) invariance frozen as a successor acceptance test with per-pin classification
   (Sections 3.3-3.4, 7);
5. conservative generator / no-outflow boundary law frozen;
6. economically requested outward boundary flow has explicit fail-closed semantics
   (`BOUNDARY_POLICY_VIOLATION`);
7. unique-stationary-distribution gate for the canonical fixture frozen (nullspace dimension 1),
   with the explicit caveat that nullity 1 does not imply full support (Section 5);
8. exact successor tolerances frozen (Section 6);
9. household aggregates / `K=M*A` / firm anchor revalidation order frozen (Section 8);
10. MATLAB provenance audit complete to the extent the source permits (companion audit document);
11. only the two allowlisted documents are added.

Terminal classification for the Builder gate:

```text
DLH_5D_CONSERVATIVE_STATIONARY_KFE_AND_MATLAB_CONTAMINATION_CONTRACT_FROZEN__READY_FOR_GPT_REVIEW
```

(or, if provenance is incomplete but the design is still scientifically frozen,
`DLH_5D_CONTRACT_FROZEN__MATLAB_PROVENANCE_PARTIAL_READY_FOR_GPT_REVIEW`).
