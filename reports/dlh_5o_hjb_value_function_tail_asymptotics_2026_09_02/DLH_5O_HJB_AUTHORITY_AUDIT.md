# DLH-5O Phase A — Exact HJB Authority Audit

**Issue #41 Phase A.** Audits exactly what the accepted MATLAB-faithful finite-grid HJB
source authorizes, distinguishing finite-grid numerical semantics from any derivable
continuous interior economics, and states what is not specified by accepted authority.

Source (read-only, immutable):
`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`
(blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`,
SHA-256 `1795718C469FC3B427CAB8E3D5957C133BEAD6EACC9EF0A25A3EDB7211D1A024`).

---

## 1. What the accepted solver actually computes

`solve_matlab_faithful_hjb` iterates on a finite grid `(b,a,z)` with
`b in [b_lo,b_max]`, `a in [0,a_max]`, `z in {0.8,1.3}`. Each iteration:

1. Computes one-sided (upwind) finite differences:
   - `V_b` at interior cell `i` is the forward difference `(V_{i+1}-V_i)/db`
     (the same value is reused as the backward derivative: `vb_b[1:] = vb_f[:-1]`);
   - `V_a` is the forward difference `(V_{j+1}-V_j)/da`;
   - at `b_lo` and `b_max` the boundary cells set
     `V_b = resources^(-gamma_c)` with
     `resources = (1-tau)*wages*z*labor0 + transfer_income + r_eff*b` (the
     **marginal-utility-of-resources finite-grid closure**).
2. Selects local policy (consumption, labor, transfer, drifts) via
   `select_matlab_faithful_local_policy` using the accepted FOC objects.
3. Assembles the source operator `A = bb + aah + bswitch` with
   - `bb` = b-axis upwind drift generator (`b_backward_rate`, `b_forward_rate`);
   - `aah` = a-axis upwind drift generator;
   - `bswitch = kron(switch_matrix, eye)` = productivity-switch generator.
4. Solves `((1/delta + rho)I - A)V_new = u + V_old/delta` until
   `max|V_new - V_old| < convergence_tolerance`.

**Converged fixed point:** at convergence `V_new = V_old = V`, so

```text
(rho + 1/delta)V - A V = u + V/delta   =>   rho*V = u + A*V.
```

**Post-convergence operator:** `post = bb(mu) + aah(mu) + bswitch` assembled from the
actual drifts `max(-mu_b,0)/db`, `max(mu_b,0)/db`, `max(-mu_a,0)/da`,
`max(mu_a,0)/da`. This is the drift operator used only by the (NOT AUTHORIZED) KFE
solve. It is not needed for the tail asymptotics of the value function itself.

---

## 2. Continuum interior HJB identity (derivable)

In the interior of the finite grid, in the continuum limit (upwind finite differences
converging to derivatives), the fixed point becomes the **interior HJB identity**:

```text
rho*V(b,a,z) = u(c,l) + mu_b(b,a,z)*V_b + mu_a(b,a,z)*V_a
             + sum_z' lambda_{z,z'}(V(b,a,z') - V(b,a,z))
```

with the accepted objects (`gamma_c = 2`, `phi = 5`, `chi_0 = 0.1`, `chi_1 = 2`,
`a_bar = 1e-6`, `r_b = 0.015`, `r_a = 0.03`, `a_max = 10`, `tau = 0.15`, `z in
{0.8,1.3}`, switch rate `1/3`):

```text
c  = V_b^(-1/2)
l  = (V_b * 0.85 z)^(1/5)
u  = -1/c - l^6/6
d  = a * T(V_a/V_b - 1)/chi_1,   T(q) = min(q+chi_0,0)+max(q-chi_0,0)
chi(d,a) = chi_0|d| + 0.5 chi_1 d^2/max(a,a_bar)
r_a_eff(a) = r_a*(1 - 0.1*(a/a_max)^9)
mu_a = r_a_eff(a)*a + d
mu_b = r_b*b + labor_income - d - chi(d,a) - (c - transfer_income),   transfer_income = 0
labor_income = 0.85 z * l
```

**Combined transfer Hamiltonian (rev 2).** Grouping the transfer-dependent parts of
`mu_b V_b + mu_a V_a`, with `R = V_a/V_b`, `q = R - 1`:

```text
d*V_a + (-d - chi)*V_b = V_b * [ d*(V_a/V_b - 1) - chi(d,a) ] = V_b * [ d*q - chi(d,a) ].
```

The accepted transfer FOC `d = a*T(q)/chi_1` is precisely the maximizer of this object
over `d` (up to the bare-`a` and `a_bar` cost-floor caveat). This combined object is
the correct same-order accounting for transfer and adjustment cost: `d*V_a` is
generally the **same order** as `-d*V_b - chi*V_b` and must never be diagnosed from
`chi` alone.

This identity is **DERIVABLE_INTERIOR_IDENTITY** — it is the algebraic form the
accepted converged fixed point approaches on the interior, subject to the upwind
finite-difference semantics and the smooth-continuum regularity assumption (where
forward/backward one-sided derivatives coincide and the selected liquid/transfer
shadow components recombine to the actual drift).

---

## 3. Authority table

| # | Object / statement | Source basis | Classification |
|---|---|---|---|
| A1 | `u(c,l) = -1/c - l^6/6`, FOCs `c=V_b^(-1/2)`, `l=(0.85z V_b)^(1/5)` | `flow_utility`, `consumption_from_vb`, `labor_from_vb` | `DIRECTLY_ACCEPTED_SOURCE_AUTHORITY` |
| A2 | `d = a*T(V_a/V_b-1)/chi_1` (bare `a`), `chi = chi_0|d|+0.5 chi_1 d^2/max(a,a_bar)` | `transfer_candidate`, `adjustment_cost` | `DIRECTLY_ACCEPTED_SOURCE_AUTHORITY` |
| A3 | `mu_a = r_a_eff(a)*a + d`; `mu_b = r_b*b + labor_income - d - chi - (c - transfer_income)`; `mu_W = mu_a+mu_b` | `asset_drifts_matlab_faithful` | `DIRECTLY_ACCEPTED_SOURCE_AUTHORITY` (verified to machine precision in accepted DLH-5L Phase A) |
| A3b | combined transfer Hamiltonian `d*V_a + (-d-chi)*V_b = V_b*[d*(V_a/V_b-1) - chi]`; transfer FOC `d = a*T(V_a/V_b-1)/chi_1` is its maximizer (up to bare-`a`/`a_bar` caveat) | A1-A3 algebra; `transfer_candidate`, `select_matlab_faithful_local_policy` | `DERIVABLE_INTERIOR_IDENTITY` (same-order grouping; must not be split into `chi` alone) |
| A4 | `r_a_eff(a) = r_a*(1-0.1*(a/a_max)^9)`, `0<=a<=a_max=10` | `matlab_faithful_illiquid_return` | `DIRECTLY_ACCEPTED_SOURCE_AUTHORITY` |
| A5 | converged fixed point `rho*V = u + A*V`; interior continuum identity `rho*V = u + mu_b V_b + mu_a V_a + S*V` | `solve_matlab_faithful_hjb` iteration, `assemble_source_operator` | `DERIVABLE_INTERIOR_IDENTITY` (subject to upwind semantics and regularity) |
| A6 | productivity switch `S*V = sum_z' lambda(V(z')-V(z))`, `lambda = 1/3` | `bswitch`, `switch_matrix` | `DIRECTLY_ACCEPTED_SOURCE_AUTHORITY` (finite Markov generator; rows sum to zero) |
| A7 | upwind finite-difference derivative `V_b = (V_{i+1}-V_i)/db` | iteration loop | `FINITE_GRID_NUMERICAL_SEMANTICS_ONLY`; convergence to the true derivative `REQUIRES_ADDITIONAL_ANALYTIC_ASSUMPTION` (regularity, tail grid resolution) |
| A8 | `b_lo`/`b_max` boundary `V_b = resources^(-gamma_c)` | iteration loop boundary cells | `FINITE_GRID_NUMERICAL_SEMANTICS_ONLY`; **must NOT be promoted to an infinite-domain boundary / transversality condition** |
| A9 | unbounded-`b` asymptotic boundary condition / transversality condition | none | `NOT_SPECIFIED_BY_ACCEPTED_AUTHORITY` |
| A9b | transfer ratio `R = V_a/V_b` and the a-derivative of the `o(1/b)` remainder of `V` | none | `NOT_SPECIFIED_BY_ACCEPTED_AUTHORITY`; must be imposed as an explicit derivative-control / transfer-ratio premise for any `p=2` coefficient statement |
| A10 | tail scaling of the actual HJB solution (`V_b ~ b^{-p}`, `V_inf`, `K(a,z)`, ...) | none | `NOT_SPECIFIED_BY_ACCEPTED_AUTHORITY` (candidate only) |
| A11 | asymptotic orders of `labor_income`, `d`, `chi`, `V_a/V_b`, cross-`z` value differences absent tail assumptions | none | `NOT_SPECIFIED_BY_ACCEPTED_AUTHORITY` (consistent with accepted DLH-5N Outcome B) |
| A12 | finite `z` support implies bounded cross-`z` value differences | none | NOT implied: finite support alone does not bound `V(b,a,z')-V(b,a,z)` as `b` grows (accepted DLH-5N finding, preserved) |

---

## 4. Iteration operator vs post-convergence drift operator

- The **iteration operator** `A` is assembled from the MATLAB-faithful shadow rates
  `iteration_b_backward_rate`/`iteration_b_forward_rate` (built from `sc` = liquid
  savings and `sdh` = transfer shadow surplus) plus the `a`-rates. It is the numerical
  policy-iteration vehicle.
- The **post-convergence operator** `post` is assembled from the actual drifts
  `mu_a`, `mu_b` (the `asset_drifts_matlab_faithful` outputs).
- These two operators represent the **same continuum drift** `mu_b V_b + mu_a V_a`
  **only under the smooth-continuum assumption**: that the one-sided (forward/backward)
  finite differences coincide with the true derivative on the tail and that the
  selected liquid/transfer shadow components recombine to the actual drift. This is an
  **analytic assumption (R1)**, not an unconditional finite-grid identity.
- For the **tail asymptotics of the value function** only the converged fixed point
  (A5) matters; the KFE/post-convergence operator is NOT AUTHORIZED to run and is not
  used here.

---

## 5. Conclusion of Phase A

The accepted source authorizes the exact economics (A1-A4, A6), the algebraic
converged fixed point and hence the continuum interior HJB identity including the
combined transfer Hamiltonian `V_b*[d*(R-1)-chi]` (A5/A3b, conditional on
upwind-semantics and smooth-continuum regularity), and the finite-grid closures
(A7-A8, numerical semantics only). It does **not** specify an unbounded-`b` HJB
problem: there is **no asymptotic boundary/transversality condition**, **no
tail-scaling statement**, and **no derivative-control / transfer-ratio statement** for
the `o(1/b)` remainder (A9-A11). Therefore any tail asymptotics derived below is a
**conditional dominant balance**, not an unconditional theorem from accepted
authority.
