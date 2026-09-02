# DLH-5P Phase A — Authority-Extension Map (Rev 3)

**Issue #42 Phase A (Rev 3).** Exact map of what is inherited from accepted authority
versus what is newly model-defining for the fixed-`a`, unbounded-positive-`b` analytic
HJB problem. Labels are exactly those required by Issue #42. Rev 3: (i) the critical
`m=1/2` branch status is `UNRESOLVED/ADMISSIBLE` (the Rev 1 ruling-out is withdrawn —
see Phase E); (ii) adopting `b_lo=-2` as continuous analytic state-space authority is
separated from the inherited borrowing-gap economics (step 24); (iii) regularity
includes explicit derivative-remainder control (no term-by-term differentiation of
leading equivalences); (iv) the admissible value class is noted to imply global
boundedness (`V_b>0, V<0`, finite `b_lo`, compact `a,z`); (v) the S2 selection content
is the explicit tail-value condition `V_inf = 0` (the discounted-value condition is
vacuous under S1).

- `INHERITED_ACCEPTED_ECONOMICS`
- `INHERITED_FINITE_GRID_NUMERICAL_SEMANTICS_ONLY`
- `DERIVABLE_CONTINUOUS_INTERIOR_IDENTITY`
- `NEW_ANALYTIC_MODEL_DEFINITION_REQUIRES_OWNER`
- `THEOREM_ASSUMPTION_ONLY__NOT_MODEL_PRIMITIVE`
- `UNRESOLVED`

No new specification is accepted merely by appearing in this table.

## A0. Objects and their classification

| # | Object | Accepted source basis | Classification |
|---|---|---|---|
| A1 | Flow utility `u(c,l) = -1/c - l^6/6` (`gamma_c=2`, `phi=5`, `lw=1`) | `flow_utility` | `INHERITED_ACCEPTED_ECONOMICS` |
| A2 | Consumption FOC `c = V_b^(-1/2)`; labor FOC `l = (0.85 z V_b)^(1/5)` (`net_wage = 0.85 z`), `labor_income = 0.85 z l` | `consumption_from_vb`, `labor_from_vb`, `net_wage` | `INHERITED_ACCEPTED_ECONOMICS` |
| A3 | Transfer FOC `d = a*T(V_a/V_b-1)/chi_1`, `T(q)=min(q+chi_0,0)+max(q-chi_0,0)`, `chi_0=0.1`, `chi_1=2` (bare `a`) | `transfer_candidate` | `INHERITED_ACCEPTED_ECONOMICS` |
| A4 | Adjustment cost `chi(d,a) = chi_0|d| + 0.5 chi_1 d^2/max(a,a_bar)`, `a_bar=1e-6` | `adjustment_cost` | `INHERITED_ACCEPTED_ECONOMICS` |
| A5 | Drifts `mu_a = r_a_eff(a)*a + d`; `mu_b = r_b*b + labor_income - d - chi - (c - transfer_income)`, `transfer_income=0` | `asset_drifts_matlab_faithful` | `INHERITED_ACCEPTED_ECONOMICS` |
| A6 | `r_b = 0.015`; borrowing-rate gap `rb_gap=0.01` (effective rate `0.025` for `b<0`, used in boundary/shadow selection); `r_a = 0.03`; `tau=0.15`; wages `1`; migration costs; `rho=0.02` | frozen D0 config, policy selection | `INHERITED_ACCEPTED_ECONOMICS` (the borrowing-gap economics is inherited; it is DISTINCT from adopting `b_lo=-2` as continuous analytic state-space authority, step 24) |
| A7 | Illiquid return taper `r_a_eff(a) = r_a*(1 - 0.1*(a/a_max)^9)` on `[0,a_max=10]`; no extrapolation beyond `a_max` | `matlab_faithful_illiquid_return` | `INHERITED_ACCEPTED_ECONOMICS` (on `[0,10]` only) |
| A8 | Productivity switch `z in {0.8,1.3}`, rate `1/3`, `S = [[-1/3,1/3],[1/3,-1/3]]`; finite Markov generator | `switch_matrix`, `bswitch` | `INHERITED_ACCEPTED_ECONOMICS` |
| A9 | Lower liquid bound `b_lo = -2` (grid lower edge) and its finite-grid closure | solver grid dataclass, boundary cells | `INHERITED_FINITE_GRID_NUMERICAL_SEMANTICS_ONLY` (the grid value `-2` is inherited); **adopting `b_lo=-2` as the continuous analytic state-space lower bound is a separate `NEW_ANALYTIC_MODEL_DEFINITION_REQUIRES_OWNER` step (step 24)** |
| A10 | `a=0` corner: bare-`a` transfer `d = 0` for any `R`; `mu_a(0)=0` | `transfer_candidate` bare-`a`, `asset_drifts` | `INHERITED_FINITE_GRID_NUMERICAL_SEMANTICS_ONLY` (corner semantics) |
| A11 | `a=a_max=10` upper boundary: `at_upper_a` restricts `d<0`; `r_a_eff(10)=0.027` | `select_matlab_faithful_local_policy` boundary branch | `INHERITED_FINITE_GRID_NUMERICAL_SEMANTICS_ONLY` |
| A12 | Continuous interior HJB identity `rho*V = u + mu_b V_b + mu_a V_a + S*V`, equivalently `rho*V = u + (r_b b + labor - c)V_b + r_a_eff a V_a + V_b[d(R-1)-chi] + S*V` | converged fixed point of `solve_matlab_faithful_hjb` (continuum limit) | `DERIVABLE_CONTINUOUS_INTERIOR_IDENTITY` (conditional on smooth-continuum regularity) |
| A13 | Combined transfer Hamiltonian `V_b[d(R-1)-chi]`, `R=V_a/V_b`; transfer FOC is its maximizer (up to bare-`a`/`a_bar` caveat) | A3-A5 algebra; accepted DLH-5O A3b | `DERIVABLE_CONTINUOUS_INTERIOR_IDENTITY` |
| A14 | Unbounded positive-`b` state-space extension `(b_lo,+inf)` | none (solver is finite-grid) | `NEW_ANALYTIC_MODEL_DEFINITION_REQUIRES_OWNER` |
| A15 | Asymptotic boundary / transversality / no-Ponzi law at `b -> +inf` | none | `NEW_ANALYTIC_MODEL_DEFINITION_REQUIRES_OWNER` |
| A16 | Analytic lower-boundary law at `b_lo=-2` | finite-grid closure only (A9) | `NEW_ANALYTIC_MODEL_DEFINITION_REQUIRES_OWNER` — distinct from the inherited borrowing-rate-gap economics (A6); adopting `b_lo=-2` as the continuous analytic state-space edge is itself new model definition (step 24) |
| A17 | Analytic upper-`a` endpoint law at `a=a_max` | finite-grid branch only (A11) | `NEW_ANALYTIC_MODEL_DEFINITION_REQUIRES_OWNER` |
| A18 | Admissible value-function class (`V in C(D̄) cap C^1(D)`, `V_b>0`, `V<0`, continuity to finite `b_lo`, compact `a`, finite `z`) — **derives global boundedness** (V monotone in `b`, bounded above by 0, bounded below by `min V(b_lo,·,·)`) and existence of `V_inf(a,z) in [-C,0]` | none | `NEW_ANALYTIC_MODEL_DEFINITION_REQUIRES_OWNER` (the class); the derived boundedness is a mathematical consequence, not new authority |
| A19 | Regularity (smooth-continuum convergence of the upwind finite-difference solution; `C^1`/`C^2` tail) **with an explicit derivative-remainder expansion** (leading equivalences are NOT differentiated term-by-term; e.g. `V_b = K b^{-p} + M b^{-p-1/2} + ...` must be carried when differentiating) | none | `THEOREM_ASSUMPTION_ONLY__NOT_MODEL_PRIMITIVE` |
| A20 | Uniformity of rates over `(a,z)` (full `[0,10]` vs compact interior-`a` kept separate) | none | `THEOREM_ASSUMPTION_ONLY__NOT_MODEL_PRIMITIVE` |
| A21 | Derivative-control condition `P-TR: R = V_a/V_b = o(sqrt(b))` uniformly (or `R=O(1)`) | assumed in DLH-5O as a theorem premise | `THEOREM_ASSUMPTION_ONLY__NOT_MODEL_PRIMITIVE` unless the Owner elevates it; NOT independently justified by a ruling-out (withdrawn — Phase E Rev 3); excludes the `m=1/2` branch by class but does NOT by itself prove the realized tail is `p=2` (conditional on the full DLH-5O premise set) |
| A22 | Uniqueness/comparison principle selecting the value solution | none | `NEW_ANALYTIC_MODEL_DEFINITION_REQUIRES_OWNER` / `UNRESOLVED`; S2's discounted-value condition is VACUOUS under S1 (bounded V) and is replaced by the explicit tail-value selection `V_inf = 0` (new model definition; necessity unproved) |
| A23 | Critical `m=1/2` branch (`R ~ Theta(sqrt(b))`) status | left unresolved in DLH-5O | `UNRESOLVED/ADMISSIBLE` (compact interior-`a`) after Rev 2/3; Rev 1's "ruled out" claim withdrawn (Phase E). Full-`[0,10]` uniform smooth realization not established; `a=0` governed by the bare-`a` degeneracy; the compact-interior family has inward `mu_W/b = -0.0025 - C/(4 chi_1) < 0` (no mean-reversion reversal) |

## A1. Inheritance boundary (what is fixed)

Everything in rows A1-A8 (the economics) is `INHERITED_ACCEPTED_ECONOMICS` and is
fixed read-only. Rows A9-A11 are finite-grid semantics that must not be promoted to
analytic law. Row A12-A13 are derivable identities (conditional on smoothness). All
rows A14-A22 are `NEW_ANALYTIC_MODEL_DEFINITION_REQUIRES_OWNER` or theorem-level
assumptions; none becomes authority merely by appearing in this table.

## A2. Explicit refusal (Issue #42 §5 / activation rule 3)

The finite-grid upper-`b` marginal-utility closure at `b_max` (a numerical boundary
condition in `solve_matlab_faithful_hjb`) is **NOT** promoted into an infinite-domain
boundary/transversality condition. No row of this map derives an unbounded-`b` law
from it.

## A3. Consequence for the candidates

Any candidate S1/S2/S3 (Phase B) may reuse A1-A8 and A12-A13 freely (inherited/
derivable), must treat A9-A11 as finite-grid semantics, and must explicitly obtain
A14-A22 as new model definition (Owner) or theorem assumption — otherwise the
candidate is incomplete.
