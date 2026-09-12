# DLH-5V-I — Bellman Selection and One-Q-Row Contract (Issue #57)

**Report 4 of 6** — `DLH_5VI_BELLMAN_SELECTION_AND_ONE_Q_ROW_CONTRACT.md`

This report freezes the statewise Bellman score, the numerical optimizer/search semantics
(algorithmic brackets), the derivative / effective-domain diagnostics, the ONE global
selection rule, and the conservative ONE backward Q-row construction with its structural
checks. Issue §6, §7, §8, §9. Design only — no execution.

---

## 1. Statewise Bellman score (Issue §8)

For every represented state `s = (j, i, z)` and every admissible, representable candidate
`alpha = (c, l, d)` (state-family and candidate contract), the discrete score is:

```text
H_h(s; alpha) = u(c) - v(l)
              + sum_r q_r(s, alpha) * [ V(dest_r) - V(s) ]          (controlled part)
              + sum_{z'} kappa(z -> z') * [ V(z', x_s) - V(z, x_s) ]  (z-switch part)
```

with:

- `u(c) - v(l)` the frozen flow payoff (authority report §3), evaluated at the candidate.
- **Controlled part:** `q_r(s, alpha) >= 0` are the candidate-specific rates of the family's
  sector contract (state-family report §2–§9), generated from `mu(s, alpha)` — the local
  drift at the CURRENT state — **before** maximization. `dest_r` are the exact represented
  destinations of the sector; `V(dest_r) - V(s)` the current iterate value differences.
- **z-switch part:** `kappa(z -> z') >= 0` are the accepted exogenous switching rates of the
  two-state `z` process (derived from the accepted `mu_z, sigma_z` Markov structure as
  instantiated in the oracle's `switch_matrix`); the switching transitions move only in `z`,
  with no `(a,b)` displacement and no dependence on `alpha`.
- **No double counting:** controlled transitions and switching transitions are disjoint
  transition types; a transition `(z, x) -> (z', x')` with `z' != z` is EXACTLY the switching
  transition (controlled rates carry `z` unchanged), and `(z, x) -> (z, x_r)` is EXACTLY the
  controlled transition (switching carries `(j,i)` unchanged). Each is counted once; both
  enter the score and both enter the Q row (Bellman report §5). The switching part has zero
  `(a,b)` first moment by construction, so the drift moment identity is checked on the
  controlled part and the switching part separately.

**Mandatory semantic rules (Issue §8):**

1. **Rates before maximization:** all `q_r` are computed from `mu(s, alpha)` BEFORE scoring;
   no rate is derived from any other candidate or from the maximizer.
2. **No optimize-then-clip:** the selected policy is never an unconstrained optimizer that is
   later projected onto a face; the candidate search is over the family's admissible cone.
3. **Sector decomposition is representation only:** a candidate maps to exactly one sector
   (state-family report §10.2); sectors are candidate-construction devices, never independent
   per-sector optima with an undocumented secondary choice.
4. **ONE global statewise selection:** the selected candidate is the argmax of `H_h(s; .)`
   over the full admissible + representable candidate set at `s` (see §3 for the search) —
   not per-sector selections.
5. **Selected rates = scored rates:** the selected candidate's already-computed rates are
   carried unchanged into the selected Q row; no recomputation with other controls.

## 2. Economic admissibility vs numerical search brackets (Issue §6)

- **True economic control set:** `c > 0`, `l >= 0`, `d in R`, subject only to the active-face
  tangent laws (state-family report §10.1). **No fixed `c_max`, `l_max`, `d_min`, `d_max` are
  installed as economic constraints.**
- **Algorithmic brackets (ALGORITHM ONLY, not economics):** the future numerical optimizer may
  search over finite brackets `[c_lo, c_hi] x [0, l_hi] x [d_lo, d_hi]` with these mandatory
  semantics:
  1. Brackets are **not** household feasibility; they never enter the admissibility test and
     never replace a tangent law.
  2. **Derivation/localization rule:** initial brackets are derived per state from the local
     effective-gradient evidence — the accepted FOC anchors when `V_b^eff > 0`:
     `c* = (V_b^eff)^(-1/gamma_c)` (with the accepted interior floor semantics only where the
     source applies them), `l_j* = (V_b^eff * w_j(1-tau-mig_j) z / omega_j)^(1/phi)`,
     `d*` from the transfer FOC with the effective gradients of the active face (5T KKT §3),
     each with a fixed multiplicative safety factor; and/or the 5V-H discrete
     coercivity/localization guidance (§D.5: on a localized gradient region `p_b >= eta > 0`
     the effective optimizer set is bounded — **used as design guidance for bracket sizing
     only, never as a global fixed-point theorem**).
  3. **Expansion rule:** if the optimizer reports an optimum on an artificial bracket, the
     algorithm must expand that bracket (documented expansion rule, e.g. doubling with a
     cap) and retry; brackets are not static.
  4. **Bound contact:** a bracket-binding optimum is NEVER accepted as the economic solution;
     after expansion/retry, persistent bound contact raises `OPTIMIZER_SEARCH_FAILURE`
     (failure taxonomy §7).
  5. **Non-binding diagnostic:** every accepted selection records bracket non-binding status
     (each coordinate strictly inside its bracket, or an explicitly documented equality that
     is a genuine economic tangent, e.g. `d = 0` transfer kink, `c -> 0` exclusion, `l = 0`);
     the implementation gate must verify no accepted selection is bracket-binding.
  6. **No tuning:** brackets are never tuned to force convergence or a desired policy; bracket
     parameters are fixed a priori in the implementation gate's configuration and any change
     requires a re-validation gate.
- **Localization failure:** if the candidate search cannot localize (e.g., no finite bracket
  region contains a score improvement within tolerance) → `OPTIMIZER_SEARCH_FAILURE`.

## 3. Numerical optimizer / search semantics

Freeze for the implementation gate (design contract, not code):

1. **Candidate generation:** (a) FOC-seeded candidates from the effective gradients of the
   active face(s) (5T KKT forms — the constrained optimum seeds); (b) a declared grid/refinement
   of `c`, `l`, `d` inside the brackets; (c) deterministic order. Generation must be dense
   enough that the discrete score's selection is stable under refinement within the declared
   tolerance (validation plan Gate 3 checks selection stability).
2. **Scoring:** every generated admissible + representable candidate is scored with §1; the
   score is finite (non-finite score → `DERIVATIVE_EFFECTIVE_DOMAIN_FAILURE` or
   `OPTIMIZER_SEARCH_FAILURE` per §4/§6 — never clipped).
3. **ONE selection:** `alpha* = argmax H_h(s; alpha)` over all scored candidates; the
   maximizer set may be a continuum; selection uses the deterministic tie rule (§4).
4. **Determinism:** the whole pipeline (family classification → generation → scoring →
   selection) is deterministic for fixed inputs; Gate-2/3 checks include a deterministic
   repeat (same inputs ⟹ same selected candidate, same Q row, bitwise or exact-to-tolerance).

## 4. Deterministic tie handling and ONE selection (Issue §8)

- **Tie rule:** among candidates whose scores equal the maximum within the declared score
  tolerance, select by a fixed precedence order: (1) sector id (fixed order: T_realloc,
  R_reverse, R_deplete, REV, TDEP, Case B, interior); (2) lexicographic `(c, l_1, ..., l_J, d)`
  with a fixed comparison order. The rule is a pure selection among exact maximizers: it does
  NOT perturb the chosen candidate, does NOT re-score, does NOT mix candidates.
- **First-moment / score invariance:** the tie rule changes neither the score nor the first
  moment of the SELECTED candidate (it selects, it does not modify). If two exact maximizers
  have different first moments, the rule still selects one deterministically (economic
  uniqueness is NOT required); the tie and the selected identity are recorded as diagnostics.
- **Represented first moment:** the Q row is built from the selected candidate's own rates
  (exact first moment `sum q (x_r - x_s) = mu(s, alpha*)`), so the represented first moment
  equals the selected candidate's drift exactly — no averaging over ties.
- **Attainment note (theory ceiling):** for smooth-test/effective-domain analysis the finite-m
  discrete argmax existence is the 5V-H §D.5 result (attainment on the localized set for
  `m >= m0`); for the production scheme, attainment of the numerical argmax within bracket
  resolution is a Gate-3/4 implementation check, NOT claimed as a theorem here (the
  unbounded-control convergence-application block stays frozen).

## 5. Derivative / effective-domain diagnostics (Issue §7)

Distinguish (A) accepted interior-source behavior from (B) the new boundary scientific
contract:

- **(A) Accepted interior behavior (unchanged authority):** the accepted source applies
  `V_b > 0` guards and the `1e-6` derivative floor to the consumption/labor FOCs, evaluates the
  bare-`a` transfer candidate on the raw `v_a/v_b` (finite negative `v_b` accepted literally;
  exact-zero/non-finite yields the IEEE result handed to the accepted masks), and uses
  `MATLAB_DRIFT_TOLERANCE = 1e-12` for zero-drift classification. These semantics remain where
  the source applies them (interior path, Gate-1 regression set).
- **(B) New boundary contract — future diagnostics (each a named failure, never clipped):**
  1. `DERIVATIVE_EFFECTIVE_DOMAIN_FAILURE` — the local optimizer of a boundary family requires
     positive liquid marginal-value evidence (`V_b^eff > 0`, i.e. `p_b > 0` effective-domain
     condition of 5V-H §D.4/§D.5) but the numerical derivative evidence is non-finite,
     non-positive, or invalid at the required tolerance;
  2. **Non-finite derivative** of `V` along any used direction at a boundary state;
  3. **Non-finite candidate score** (`H_h` non-finite at a candidate with finite drift/payoff
     — indicates an operator or value-array pathology);
  4. **Failed optimizer localization** (no bounded bracket region contains the improvement —
     §2.6);
  5. **No admissible represented candidate** at a state (the admissible cone is non-empty but
     every admissible candidate is unrepresentable — the 5V-F obstruction cells can exhibit
     this for exact-tangent sub-classes; recorded per family by Gate 2);
  6. **Inability to build a conservative Q row** (cannot satisfy §6 checks — a
     `GENERATOR_CONSERVATION_FAILURE`).
- **No arbitrary clipping / normalization / KFE-side repair** of any of these; each maps to
  the failure taxonomy (§7) and halts the run with an explicit failure object. The accepted
  source is NOT mutated to "fix" boundary pathologies.

## 6. Conservative ONE backward Q-row construction (Issue §9)

For the selected candidate `alpha*` at state `s = (j, i, z)`:

```text
Q[row, col] > 0  (row != col)  <=>  col is an ACTUAL represented destination of the selected
                                    candidate: controlled dest_r (with rate q_r(s, alpha*) >= 0)
                                    or switching dest (z', x_s) (with rate kappa(z -> z') >= 0)
Q[row, row] = -sum_{row != col} Q[row, col]        (exact, by construction)
```

- **Off-diagonal nonnegativity:** every controlled rate from the sector contract is
  nonnegative on its sector (frozen formulas); every switching rate nonnegative (accepted
  Markov structure).
- **Destination represented:** every off-diagonal target is a represented node of the frozen
  grid (state-family report availability conditions) — enforced by the representability
  contract (§10 of state-family report) BEFORE row construction; no unavailable outward
  destination contributes to the diagonal (no lost-diagonal exit).
- **Row sum zero by construction:** `Q 1 = 0` exactly; no normalization, no pinning, no
  leakage repair.
- **Same candidate / same rates:** the HJB score and the Q row consume the SAME selected
  candidate and its already-computed rates (report §1.5).
- **Switching orientation:** `kappa(z -> z')` is placed in `Q[row, col(z')]` with the accepted
  forward orientation (backward generator convention of the oracle); orientation verified by
  the structural checks.
- **No KFE-only process:** there is exactly one selected backward generator; the future KFE
  consumes exactly `Q^T` (same-process law). Stationary KFE remains NOT AUTHORIZED here.

**Future implementation structural checks (mandatory, Gate 2/3):**

1. Row sums: `Q 1 = 0` for every row within exact arithmetic (or the declared machine
   tolerance with exactness verified on rational re-evaluation of the selected rates).
2. Off-diagonal signs: `Q[row, col] >= 0` for `row != col` (no signed off-diagonals in the
   new boundary rows — this is the boundary contract's divergence from the accepted source's
   documented axis-truncation behavior, which is retained only on the interior path rows).
3. Represented-destination membership: every `col` with `Q[row, col] > 0` is a represented
   node (recompute from the grid mask).
4. First moments: `sum_col Q[row, col] * (x_col - x_row) = mu(s, alpha*)` (controlled part)
   and `0` in `(a,b)` for the switching part — within the frozen drift tolerance.
5. Selected-score recomputation: recompute `H_h(s; alpha*)` from the row's own rates and the
   current `V`; it must equal the recorded maximizer score within the score tolerance.
6. Deterministic repeat: re-running the pipeline on the same inputs reproduces the same
   selected candidate identity and the same row.
7. Candidate identity: the recorded `(c, l, d)` matches the rates' drift (first-moment
   consistency), and the HJB-iteration and post-convergence recomputation use the same
   selected candidates.

## 7. Failure taxonomy (Issue §12 — frozen names, no silent fallback)

| Failure | Meaning / trigger |
|---|---|
| `SCIENTIFIC_ADMISSIBILITY_FAILURE` | candidate violates an actual tangent/economic law (state-family report §10.1); no clip into the cone |
| `REPRESENTATION_FAILURE` | legal candidate drift cannot be represented by the authorized finite-process contract at that state (destination unavailable / outside `C_rep(s)`) |
| `OPTIMIZER_SEARCH_FAILURE` | bracket expansion/localization fails, or an artificial bound remains binding at an accepted selection |
| `DERIVATIVE_EFFECTIVE_DOMAIN_FAILURE` | numerical derivative evidence required by the selected local optimizer is invalid / non-finite / non-positive (`V_b^eff <= 0` where `p_b > 0` is required) |
| `GENERATOR_CONSERVATION_FAILURE` | off-diagonal sign / row-sum / destination-identity / first-moment check fails (§6) |
| `HJB_LINEAR_SOLVE_FAILURE` | the implicit sparse solve is non-finite or singular |
| `HJB_NONCONVERGENCE` | max iterations reached without the declared tolerance |
| `REGRESSION_FAILURE` | unaffected-interior states no longer match the accepted oracle (Gate 1) |

Every failure halts with an explicit failure object naming the state family, the candidate
(where applicable) and the check that failed. No automatic clipping, no silent fallback, no
KFE-side repair.
