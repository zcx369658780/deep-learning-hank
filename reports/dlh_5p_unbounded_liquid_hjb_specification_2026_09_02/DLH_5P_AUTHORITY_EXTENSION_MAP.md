# DLH-5P Phase A — Authority-Extension Map

**Issue #42 Phase A.** Exact map of what is inherited from accepted authority versus
what is newly model-defining for the fixed-`a`, unbounded-positive-`b` analytic HJB
problem. Labels are exactly those required by Issue #42:

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
| A6 | `r_b = 0.015`; borrowing-rate gap `rb_gap=0.01` (effective rate `0.025` for `b<0`, used in boundary/shadow selection); `r_a = 0.03`; `tau=0.15`; wages `1`; migration costs; `rho=0.02` | frozen D0 config, policy selection | `INHERITED_ACCEPTED_ECONOMICS` |
| A7 | Illiquid return taper `r_a_eff(a) = r_a*(1 - 0.1*(a/a_max)^9)` on `[0,a_max=10]`; no extrapolation beyond `a_max` | `matlab_faithful_illiquid_return` | `INHERITED_ACCEPTED_ECONOMICS` (on `[0,10]` only) |
| A8 | Productivity switch `z in {0.8,1.3}`, rate `1/3`, `S = [[-1/3,1/3],[1/3,-1/3]]`; finite Markov generator | `switch_matrix`, `bswitch` | `INHERITED_ACCEPTED_ECONOMICS` |
| A9 | Lower liquid bound `b_lo = -2` (grid lower edge) and its finite-grid closure | solver grid dataclass, boundary cells | `INHERITED_FINITE_GRID_NUMERICAL_SEMANTICS_ONLY` |
| A10 | `a=0` corner: bare-`a` transfer `d = 0` for any `R`; `mu_a(0)=0` | `transfer_candidate` bare-`a`, `asset_drifts` | `INHERITED_FINITE_GRID_NUMERICAL_SEMANTICS_ONLY` (corner semantics) |
| A11 | `a=a_max=10` upper boundary: `at_upper_a` restricts `d<0`; `r_a_eff(10)=0.027` | `select_matlab_faithful_local_policy` boundary branch | `INHERITED_FINITE_GRID_NUMERICAL_SEMANTICS_ONLY` |
| A12 | Continuous interior HJB identity `rho*V = u + mu_b V_b + mu_a V_a + S*V`, equivalently `rho*V = u + (r_b b + labor - c)V_b + r_a_eff a V_a + V_b[d(R-1)-chi] + S*V` | converged fixed point of `solve_matlab_faithful_hjb` (continuum limit) | `DERIVABLE_CONTINUOUS_INTERIOR_IDENTITY` (conditional on smooth-continuum regularity) |
| A13 | Combined transfer Hamiltonian `V_b[d(R-1)-chi]`, `R=V_a/V_b`; transfer FOC is its maximizer (up to bare-`a`/`a_bar` caveat) | A3-A5 algebra; accepted DLH-5O A3b | `DERIVABLE_CONTINUOUS_INTERIOR_IDENTITY` |
| A14 | Unbounded positive-`b` state-space extension `(b_lo,+inf)` | none (solver is finite-grid) | `NEW_ANALYTIC_MODEL_DEFINITION_REQUIRES_OWNER` |
| A15 | Asymptotic boundary / transversality / no-Ponzi law at `b -> +inf` | none | `NEW_ANALYTIC_MODEL_DEFINITION_REQUIRES_OWNER` |
| A16 | Analytic lower-boundary law at `b_lo=-2` | finite-grid closure only (A9) | `NEW_ANALYTIC_MODEL_DEFINITION_REQUIRES_OWNER` (or `INHERITED_FINITE_GRID_NUMERICAL_SEMANTICS_ONLY` if left as data) |
| A17 | Analytic upper-`a` endpoint law at `a=a_max` | finite-grid branch only (A11) | `NEW_ANALYTIC_MODEL_DEFINITION_REQUIRES_OWNER` |
| A18 | Admissible value-function class (growth bound on `V`) | none | `NEW_ANALYTIC_MODEL_DEFINITION_REQUIRES_OWNER` |
| A19 | Regularity (smooth-continuum convergence of the upwind finite-difference solution; `C^1`/`C^2` tail) | none | `THEOREM_ASSUMPTION_ONLY__NOT_MODEL_PRIMITIVE` |
| A20 | Uniformity of rates over `(a,z)` | none | `THEOREM_ASSUMPTION_ONLY__NOT_MODEL_PRIMITIVE` |
| A21 | Derivative-control condition `P-TR: R = V_a/V_b = o(sqrt(b))` uniformly (or `R=O(1)`) | assumed in DLH-5O as a theorem premise | `THEOREM_ASSUMPTION_ONLY__NOT_MODEL_PRIMITIVE` unless Owner elevates; partially justified at the dominant-balance level (Phase D/E) |
| A22 | Uniqueness/comparison principle selecting the value solution | none | `NEW_ANALYTIC_MODEL_DEFINITION_REQUIRES_OWNER` / `UNRESOLVED` |
| A23 | Critical `m=1/2` branch (`R ~ Theta(sqrt(b))`) status | left unresolved in DLH-5O | `UNRESOLVED` at DLH-5O level; DLH-5P Phase E rules it out as a smooth dominant balance |

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
