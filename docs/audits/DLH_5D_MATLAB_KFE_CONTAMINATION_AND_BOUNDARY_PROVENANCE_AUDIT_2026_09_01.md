# DLH-5D — MATLAB KFE Contamination and Boundary Provenance Audit

- **Issue:** #27 (DLH-5D)
- **Task type:** `SCIENTIFIC_DESIGN__STATIONARY_KFE_BOUNDARY_AND_CONTAMINATION_CONTRACT`
- **Status:** PROVENANCE / DESIGN ONLY (read-only analysis; no mutation of legacy sources)
- **Branch:** `dsh/issue-27-dlh-5d-kfe-boundary-contamination-contract-2026-09-01`
- **Baseline `origin/main`:** `b0ab6857f82434f89416b784c312682645163c10`
- **Revision:** R1 (2026-09-01) — per GPT review of candidate `d5cb5dd…`, corrects the
  orientation wording in Section 3.2 (`A(row,col)>0` means `row -> col`, not "into state row from
  col"), tightens the normalization-weight wording in Section 3.5 (`cell_weight = db*dah` per
  discrete z state, no `dz` quadrature factor), and adds pin-admissibility / pin-classification
  rows to the provenance mapping (owner-frozen contract items). All other provenance content is
  preserved.

This audit locates, in the authorized read-only MATLAB source root
`D:\MatlabProgram\2023年12月2日 多省份神经网络HANK`, the stationary-KFE contamination and
finite-grid boundary construction, and maps every provenance statement to one of:

- `MATLAB_PROVENANCE` — directly located in the MATLAB source (with file/line citations);
- `OWNER_FROZEN_NEW_SCIENTIFIC_CONTRACT` — frozen by Issue #27 / Owner clarification, not present
  in the legacy source;
- `PYTHON_CURRENT_BEHAVIOR_TO_BE_SUPERSEDED` — current accepted Python faithful port behavior
  that the successor conservative KFE must supersede;
- `NOT LOCATED` — searched but not found in the legacy source; not inferred.

Companion document: `docs/specifications/DLH_5D_CONSERVATIVE_STATIONARY_KFE_BOUNDARY_AND_CONTAMINATION_CONTRACT_2026_09_01.md`
(the frozen scientific contract).

---

## 1. Provenance evidence base (read-only)

Files inspected read-only (no copy-out, no mutation, no execution):

| File | Role | KFE-relevant location |
|---|---|---|
| `HANK_2ASSETS_HJB.m` | two-asset HJB + stationary KFE | generator assembly lines 155-232 / 262-333; KFE/contamination lines 334-346 |
| `multi_prov_HANK_12sts.m` | multi-province driver (grid + numerics config) | `homecrit` line 17-18; grid `I/J/Nz` lines 34-46 |
| `HJB程序.txt` | saved text copy of `HANK_2ASSETS_HJB.m` | identical KFE/contamination lines 433-445 |
| `main.m`, `main2.m`, `HANK_mp_1eq.m`, `HANK_mp_1turn.m`, `HANK_firm.m`, `wage_caculate.m`, `Lt_seperate.m`, `lab_solve2.m`, `HANK3_FOC.m`, `HANK3_cost.m`, `HANK_gini.m`, `HANK_quantile5_multiprov.m`, `multi_prov_HANK.m`, `mpHANK_equilibrium_2000.m`, `mpHANK_shock_2000.m`, `adjust_weight_matrix.m`, `init_weight_matrix.m`, `load_*.m`, `It_to_Kt.m`, misc. | surrounding model/provenance context | searched for KFE/contamination/residual patterns; no other stationary-KFE or contamination implementation located |

Python faithful port inspected read-only for the `PYTHON_CURRENT_BEHAVIOR_TO_BE_SUPERSEDED`
classification:
`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`
(`assemble_source_axis` lines 425-451, `assemble_source_operator` 453-464,
`matlab_contaminated_row_index` 581-584, `solve_matlab_faithful_stationary_kfe` 586-603,
`aggregate_stationary_household` 620-630).

Repository provenance committed under Issues #23-#26 (accepted) was consulted, in particular the
DLH-5C accepted report on `origin/main` (issue-26 root, R2) and the prior
`docs/audits/DLH_5A_HISTORICAL_MATLAB_PROVENANCE_AND_REPLACEMENT_BOUNDARY_2026_08_31.md`
(replacement-boundary scope; its Section 2 noted the referenced handoff document was NOT LOCATED).

---

## 2. Provenance mapping (summary table)

| # | Requirement (Issue §8) | Finding | Classification |
|---|---|---|---|
| 1 | MATLAB HJB transition/generator matrix `A` | `A = BB + AAH + Bswitch` in `HANK_2ASSETS_HJB.m:232` (iterated) and `:333` (final); BB = b-axis upwind, AAH = a-axis upwind, Bswitch = z-switch `kron(la_mat, eye)` | `MATLAB_PROVENANCE` |
| 2 | KFE use of `A'` / transpose | `AT = A';` at `HANK_2ASSETS_HJB.m:335`; KFE solves the transposed system | `MATLAB_PROVENANCE` |
| 3 | Contaminated-row / pinned-equation construction | `AT(iFix,:) = [zeros(1,iFix-1),1,zeros(1,M-iFix)]` at `:339` (replace the iFix-th ROW of `AT`, i.e. the iFix-th KFE equation, with unit row); `g_stacked = AT\vec` at `:340` | `MATLAB_PROVENANCE` |
| 4 | Chosen row / RHS constant conventions | `iFix = floor(0.37*M)` at `:337` (1-based; M=I*J*Nz=800 → 296 1-based = 295 0-based); `vec(iFix) = 0.007` at `:338` | `MATLAB_PROVENANCE` |
| 5 | Normalization formula | `g_sum = g_stacked'*ones(M,1)*db*dah; g_stacked = g_stacked./g_sum` at `:341-342`; cell weight `db*dah` (no `dz` factor for the 2-point z process); reshape at `:343-344` | `MATLAB_PROVENANCE` |
| 6 | Finite-grid boundary treatment in operator assembly | uniform upwind `X/Y/Z` (b) and `chih/yyh/zetah` (a); outward destination omitted at grid edge while diagonal retains the rate; boundary rows can be materially negative | `MATLAB_PROVENANCE` |
| 7 | Whether `A*ones ≈ 0` is structurally guaranteed | interior rows yes (by `X+Y+Z=0` construction); boundary rows NO (outward destination omitted, diagonal rate retained); only HJB-iteration check `max(abs(sum(A,2))) <= homecrit=1e-2` (`:233-239`, `multi_prov_HANK_12sts.m:18`); the final KFE `A` is not re-checked | `MATLAB_PROVENANCE` |
| 8 | Whether original `A'*g` residual is checked | NOT LOCATED — no original-equation residual check anywhere in the MATLAB source | `NOT LOCATED` |
| 9 | Any MATLAB structure missing in Python | none missing: the Python faithful port reproduces generator structure, boundary truncation, contamination, row index, RHS constant, normalization, and stores only the contaminated residual | `PYTHON_CURRENT_BEHAVIOR_TO_BE_SUPERSEDED` (superseded by the new contract) |
| 10 | Singular-`Q` expected; singularity not failure | not present in MATLAB (MATLAB never treats singularity as a gate); frozen as new contract | `OWNER_FROZEN_NEW_SCIENTIFIC_CONTRACT` |
| 11 | Original-equation acceptance rule `||Q^T g|| <= tol` | not present in MATLAB | `OWNER_FROZEN_NEW_SCIENTIFIC_CONTRACT` |
| 12 | Pin admissibility (component pin `g_n=c>0` valid only if `g_star[n]!=0`) distinguished from stationary uniqueness | not present in MATLAB (MATLAB pins `iFix` unconditionally and never checks original validity) | `OWNER_FROZEN_NEW_SCIENTIFIC_CONTRACT` |
| 13 | Successor pin classification `PIN_VALID_STATIONARY_NORMALIZATION` / `PIN_INADMISSIBLE_ZERO_STATIONARY_SUPPORT` / `PIN_NUMERICAL_FAILURE_UNRESOLVED`; only valid pins compared; >= 2 valid pins for contamination acceptance | not present in MATLAB | `OWNER_FROZEN_NEW_SCIENTIFIC_CONTRACT` |
| 14 | Conservative generator `sum_j Q[i,j]=0`, no-outflow law | not satisfied by the MATLAB assembly (boundary leak) and absent as a requirement | `OWNER_FROZEN_NEW_SCIENTIFIC_CONTRACT` |
| 15 | `BOUNDARY_POLICY_VIOLATION` fail-closed semantics | not present in MATLAB (outward requested flow is silently clipped) | `OWNER_FROZEN_NEW_SCIENTIFIC_CONTRACT` |

---

## 3. Detailed findings

### 3.1 MATLAB generator matrix `A` (HJB transition/generator)

`MATLAB_PROVENANCE` — `HANK_2ASSETS_HJB.m`:

- `A = BB + AAH + Bswitch` at `:232` (during HJB iteration) and at `:333` (final post-convergence
  operator used for the KFE). `M = I*J*Nz` at `:334`.
- **b-axis `BB`**: one-step upwind on the b index. Coefficients (post-loop form, `:365-367`):
  `X = -min(s,0)/db`, `Y = min(s,0)/db - max(s,0)/db`, `Z = max(s,0)/db`, where `s` is the liquid
  savings flow (`:263`). Assembled as `spdiags(centdiag,0)+spdiags(updiag,1)+spdiags(lowdiag,-1)`
  (`:296`), block-diagonal over the two z states (`:298`).
- **a-axis `AAH`**: one-step upwind on the a index. Coefficients (post-loop form, `:299-301`):
  `chih = -min(mh,0)/dah`, `yyh = min(mh,0)/dah - max(mh,0)/dah`, `zetah = max(mh,0)/dah`, where
  `mh = dh + Rah.*aaah` (`:264`). Assembled as `spdiags(centdiagh,0)+spdiags(updiagh,I)+spdiags(lowdiagh,-I)`
  (`:330`), block-diagonal over the two z states (`:332`).
- **z-switch `Bswitch`**: `kron(la_mat, speye(I*J))` at `:164-166`, with
  `la_mat = ones(Nz,Nz)*(1/3/(Nz-1)) + eye(Nz,Nz)*(-1/3-1/3/(Nz-1))`
  (`multi_prov_HANK_12sts.m:47`); rows sum to zero (conservative by construction).
- Grid / numerics: `I=20` (b), `J=20` (a), `Nz=2` (z), `bmax=5`, `amax=10`, `zmin=0.8`,
  `zmax=1.3` (`multi_prov_HANK_12sts.m:34-46`) → `M = 800`.

### 3.2 KFE uses the transpose `A'`

`MATLAB_PROVENANCE` — `HANK_2ASSETS_HJB.m:335` `AT = A';`. The stationary distribution solves
the forward/adjoint system built from the transpose of the HJB generator, i.e. the MATLAB analog
of the frozen `Q^T g = 0` (with `Q` = MATLAB `A`). Orientation is exactly the frozen contract:
in the backward/source generator, `A(row,col) > 0` means `row -> col` (row = current/source
state, col = destination state). In the forward equation `A' g`, that same rate transports mass
from the source `row` into the destination `col`, and the stationary KFE is the adjoint balance
`A' g = 0`. This is consistent with the accepted DLH-5C orientation finding.

### 3.3 Contaminated-row / pinned-equation construction

`MATLAB_PROVENANCE` — `HANK_2ASSETS_HJB.m:336-340`:

```matlab
vec = zeros(M,1);
iFix = floor(0.37*M);
vec(iFix) = 0.007;
AT(iFix,:) = [zeros(1,iFix-1),1,zeros(1,M-iFix)];
g_stacked = AT\vec;
```

- The pin replaces the **iFix-th row of `AT`** (equivalently the iFix-th equation of the KFE
  system) with the unit row `e_iFix` and sets the RHS entry to `0.007`. The column `n` of `Q`
  corresponding to state `iFix` is thereby removed from the equation set and replaced by the pin
  `g_{iFix} = 0.007` before normalization.
- The solve is the MATLAB sparse `\` (UMFPACK direct), i.e. the MATLAB analog of the accepted
  Python `spsolve`.
- MATLAB never verifies the contaminated solution against the original `AT*g = 0` system.

### 3.4 Row selection and RHS constant conventions

`MATLAB_PROVENANCE`:

- `iFix = floor(0.37*M)` (`:337`) is a **1-based** index. For `M = 800`: `floor(0.37*800) = 296`
  (1-based), i.e. state **295 in 0-based indexing**. The accepted Python port
  `matlab_contaminated_row_index(state_count) = floor(0.37*state_count) - 1` (`matlab_faithful_two_asset_ha.py:581-584`)
  yields exactly 295 for `N=800` — a faithful parity with the MATLAB convention.
- RHS pin constant `c = 0.007` (`:338`). The contract permits retaining `c = 0.007` for parity
  while requiring normalized-density invariance in the magnitude of positive `c`.

### 3.5 Normalization formula

`MATLAB_PROVENANCE` — `HANK_2ASSETS_HJB.m:341-342`:

```matlab
g_sum = g_stacked'*ones(M,1)*db*dah;
g_stacked = g_stacked./g_sum;
```

- The cell weight used in normalization is exactly `cell_weight = db * dah` **per discrete z
  state**: there is **no `dz` quadrature factor** — the two z values are a finite-state Markov
  process (transition block `Bswitch`), not a continuum quadrature direction, so there is no
  "z-state quadrature weight" multiplier. Aggregates likewise use `*g*dah*db` everywhere
  (`:345-372`), and `results.g = g*db*dah` (`:387`).
- The frozen contract (Section 1 of the specification) freezes this weight convention exactly as
  `cell_weight = db * dah` per discrete z state and requires the normalization identity
  `sum_s g_s * cell_weight(s) = 1` to hold to the frozen tolerance, consistent with the
  MATLAB-faithful `db*dah` weight.

### 3.6 Finite-grid boundary treatment in the MATLAB operator assembly

`MATLAB_PROVENANCE` — uniform upwind with **outward-destination omission while the diagonal rate
is retained**:

- b-axis off-diagonal placement (`:275-294`): `lowdiag(i)=X(i+1)` for `i=1..I-1` and
  `lowdiag(I)=0`; `updiag(1)=0` and `updiag(i)=Z(i-1)` for `i=2..I`. Consequently, at the upper
  b-edge (`i=I`) with `s(I) > 0` (outward saving), the diagonal retains `Y(I) = -max(s,0)/db`
  (`:366`) but no destination entry exists for the outward rate `Z(I)`; the row sum is negative
  (probability leakage). The lower b-edge (`i=1`) behaves analogously when `s(1) < 0`.
- a-axis off-diagonal placement (`:402-428`): `lowdiagh(j)=chih(j+1)` for `j=1..J-1` and
  `lowdiagh(J)=0`; `updiagh(1)=0` and `updiagh(j)=zetah(j-1)` for `j=2..J`. At the upper a-edge
  (`j=J`) with `mh(J) > 0` (outward illiquid saving), the diagonal retains
  `yyh(J) = -max(mh,0)/dah` (`:400`) but the outward rate `zetah(J)` has no destination; the row
  sum is negative. (The iteration-time a-edge clip `MhF(:,J,:) = 0` at `:195` influences the
  drift-direction selection but does not enter the final upwind assembly at `:299-332`.)
- This is exactly the construction DLH-5C diagnosed (leaky upper-boundary rows; the accepted R2
  report measured 29-30 leaky states with row sums ≈ -0.39 on the frozen fixture). **MATLAB does
  not enforce `sum_j A[i,j] = 0` at these boundary states.**

### 3.7 Is `A*ones ≈ 0` structurally guaranteed?

`MATLAB_PROVENANCE` (partial) — not structurally guaranteed at boundaries:

- Interior states: yes, by construction the upwind triple sums to zero
  (`X + Y + Z = 0` on the b-axis; `chih + yyh + zetah = 0` on the a-axis) and `Bswitch` rows sum
  to zero.
- Boundary states: **no** — the outward destination is omitted while the diagonal keeps the rate
  (Section 3.6), so row sums can be materially negative at outward boundaries.
- The only generator-conservation check in the MATLAB codebase is
  `A2max = max(abs(sum(A,2))); if A2max > num.homecrit ... break` during **HJB iteration**
  (`HANK_2ASSETS_HJB.m:233-239`), with `num.homecrit = 10^(-2)`
  (`multi_prov_HANK_12sts.m:18`, active). This is a loose (1e-2) check applied to the iteration
  operator only; the **final post-convergence KFE operator** (`:333`) is assembled identically but
  is **not re-checked** for row sums, and no boundary-row-sum verification is applied to the KFE
  solve.

### 3.8 Is the original `A'*g` residual checked?

`NOT LOCATED` — no original-equation residual check exists in the MATLAB source:

- A read-only search across all `.m` files for `resid`, `norm(`, `sum(AT`, `sum(A`, `ones(...)*A`
  found no original `A'*g` residual verification. The only row-sum computation is the HJB-iteration
  `max(abs(sum(A,2)))` of Section 3.7.
- The KFE block (`:334-346`) outputs only the contaminated solve, its normalization, and the
  aggregates; no `AT*g` residual is computed or stored.
- `Bdotres` (`:352`) is the household **budget**-residual aggregate, not a KFE residual.
- Therefore MATLAB accepts the contaminated density without any original-equation validation; the
  accepted Python port likewise stores only the contaminated residual
  (`matlab_faithful_two_asset_ha.py:602`). This is the gap the new contract closes.

### 3.9 Any MATLAB structure currently missing in Python?

`PYTHON_CURRENT_BEHAVIOR_TO_BE_SUPERSEDED` — no structural gap in the faithful port; the reverse
gaps (new contract) are the missing items:

- `assemble_source_axis` (`matlab_faithful_two_asset_ha.py:425-451`) reproduces the MATLAB
  truncation exactly ("truncating outward entries but not their diagonal"): off-diagonals are
  dropped at the grid edge while the diagonal keeps `-(rb + rf)`, so boundary row sums are
  negative — the same leak as MATLAB (Section 3.6). The a-axis and b-axis both use this path, and
  `Bswitch` is `kron(switch_matrix, eye)` (`:463`), matching MATLAB.
- `matlab_contaminated_row_index` (`:581-584`) = `floor(0.37*N)-1` (0-based) — parity with the
  MATLAB 1-based `floor(0.37*M)` (Section 3.4).
- `solve_matlab_faithful_stationary_kfe` (`:586-603`) mirrors the MATLAB contamination
  (transpose → replace row → `rhs[row]=0.007` → `spsolve` → normalize by `sum(raw)*db*da`), with
  an added fail-closed non-finite check and the contaminated residual only.
- `aggregate_stationary_household` (`:620-630`) uses weight `db*da` and z-weighted labor — parity
  with MATLAB `*g*dah*db` and `zzz.*l.*g*dah*db`.
- No MATLAB structure was identified that the Python port omits. The gap is the reverse: neither
  MATLAB nor the current Python enforces boundary conservation, original-residual validation,
  pin-row invariance, or `BOUNDARY_POLICY_VIOLATION` surfacing — all new-contract requirements
  (`OWNER_FROZEN_NEW_SCIENTIFIC_CONTRACT`).

### 3.10 Owner-frozen new-contract items (not in MATLAB)

`OWNER_FROZEN_NEW_SCIENTIFIC_CONTRACT` — the frozen specification items that are **additions** the
legacy source does not contain:

- singularity of `Q` is expected (1-dimensional nullspace) and not a failure;
- contaminated residual vs ORIGINAL `Q^T g` residual distinction, with original-equation
  acceptance rule `||Q^T g||_inf <= 1e-10`;
- bounded pin-row invariance on `{0, floor(N/4), floor(0.37N)-1, floor(N/2), floor(3N/4), N-1}`;
- conservative generator `sum_j Q[i,j]=0`, `Q[i,j]>=0 (i≠j)`, `Q[i,i] = -sum_{j≠i} Q[i,j]`, no
  boundary rate in the diagonal if its destination is omitted (no-outward-flux law);
- `BOUNDARY_POLICY_VIOLATION` fail-closed semantics for economically requested outward flow
  above `1e-10`;
- unique-stationary-distribution gate (nullspace dimension 1) for the canonical fixture;
- exact successor tolerances (row-sum 1e-12, neg-offdiag 1e-12, original residual 1e-10, mass
  norm 1e-12, min density ≥ -1e-12, multi-pin max diff 1e-10, repeat diff 1e-12, boundary
  outward rate 1e-10);
- household aggregate recomputation (C, L, A, B) and `K=M*A` / `Z*, delta*` revalidation order,
  with STOP-for-Owner on invalid closure.

---

## 4. Explicitly NOT LOCATED (not inferred)

| Item | Result |
|---|---|
| Any MATLAB code that checks the ORIGINAL `A'*g` residual of the contaminated solution | `NOT LOCATED` |
| Any MATLAB enforcement of `sum_j A[i,j] = 0` on the final KFE operator (beyond the HJB-iteration `homecrit=1e-2` check) | `NOT LOCATED` |
| Any MATLAB comment/documentation in the source explaining the contamination rationale, the `0.37` row rule, or the `0.007` constant | `NOT LOCATED` |
| Any MATLAB statement of the z-state cell weight in normalization (empirically `db*dah` only, no `dz`) | `NOT LOCATED` (convention observed from code) |
| The `DeepLearning_HANK_MATLAB_NATIVE_STEADY_STATE_OUTER_ITERATION_SCIENTIFIC_HANDOFF_2026_08_31.md` document referenced by Issue #24 (KFE-specific content if any) | `NOT LOCATED` (consistent with the DLH-5A audit) |

None of the above is inferred; each remains open to a future, separately authorized provenance
pass if the relevant material becomes available.

---

## 5. Read-only / forbidden-operation compliance

- No mutation, copy-out, or execution in
  `D:\MatlabProgram\2023年12月2日 多省份神经网络HANK` (list/stat/read/search only).
- No `src/**`, tests, configs, roadmap, governance, or other existing repository file is modified
  by this audit; only the two Issue #27 allowlisted documents are added.
- No HJB/KFE/GE execution, no conservative assembly, no solver, no alternative pin, no
  regularization/jitter/pseudoinverse, no D0-D3 or two-region rerun.
- No self-acceptance, merge, close, PR, or successor Issue.

---

*This audit records MATLAB provenance to the extent the authorized source permits. It does not by
itself constitute a scientific PASS; the companion specification freezes the scientific contract,
and acceptance is an independent-review decision per project acceptance levels.*
