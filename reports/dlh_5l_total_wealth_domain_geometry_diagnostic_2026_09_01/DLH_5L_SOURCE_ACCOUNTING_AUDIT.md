# DLH-5L Phase A — accepted total-wealth drift accounting audit

Source (read-only): `src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py (accepted, read-only)`.

## Accepted accounting identities (implemented-source, verified numerically)

```text
mu_a = r_a_eff(a)*a + d
mu_b = r_b*b + labor_income - d - adjustment_cost - (consumption - transfer_income)
mu_W = mu_a + mu_b
     = r_a_eff(a)*a + r_b*b + labor_income - adjustment_cost - (consumption - transfer_income)
linear transfer cancellation: (+d in mu_a) + (-d in mu_b) = 0  (adjustment cost separate)
base_liquid_surplus = r_b*b + labor_income - (consumption - transfer_income)
transfer_injection = -transfer - adjustment_cost ;  mu_b = base_liquid_surplus + transfer_injection
```

- Implemented-source accounting identity, not an external economic theorem.

## Audited objects

### Total-wealth drift identity mu_W = mu_a + mu_b (`mu_W_identity`)

- Source fact: Accepted source: mu_a = r_a_eff(a)*a + d and mu_b = r_b*b + labor_income - d - adjustment_cost - (consumption - transfer_income), with d = transfer. Therefore mu_W = mu_a + mu_b = r_a_eff(a)*a + r_b*b + labor_income - adjustment_cost - (consumption - transfer_income); the linear transfer term d cancels one-for-one between mu_a and mu_b.
- Verified: numerically at every inherited state (see state-drift decomposition)

### Linear transfer cancellation (`transfer_cancellation`)

- Source fact: mu_a linear d contribution = +d; mu_b linear -d contribution = -d; (mu_a - r_a_eff(a)*a) + (mu_b - base_liquid_surplus + adjustment_cost) = d + (-d) = 0 exactly (adjustment cost is NOT part of the linear cancellation and is kept separate).
- Verified: numerically at every inherited state

### Reused accepted DLH-5K decomposition (`base_decomposition_reuse`)

- Source fact: base_liquid_surplus = r_b*b + labor_income - (consumption - transfer_income); transfer_injection = -transfer - adjustment_cost; mu_b = base_liquid_surplus + transfer_injection (accepted DLH-5K Phase A identity, verified to machine precision).
- Verified: recomputed at every inherited state

### Frozen objects in every DLH-5L rerun (`frozen_objects`)

- Source fact: wbar=1.0, r_a=0.03; a in [0,10], a_max=10, accepted taper; a in {a77,a153}; db=7/19; b extent in {b120,b140,b160}; b160 hard ceiling; no new grid/extent/resolution/warm start; no b100 rerun; no clipping.
- Verified: grid_plan_identity asserts the exact J0-J5 plan

## Frozen objects / inspected state set

- `wbar=1.0`, `r_a=0.03`; a in [0.0,10.0], `a_max=10.0`, taper `r_a*(1-0.1*(a/a_max)^9)_MATLAB_FAITHFUL_UNCHANGED`; `b_lo=-2.0`, `db=0.368421052632`; a resolutions ['a77', 'a153']; b extents ['b120', 'b140', 'b160']; b160_IS_THE_HARD_ROUTE_CEILING__NO_B180_B200__NO_NEW_GRID.
- Inspected state set: exact union of `reports/dlh_5k_high_wealth_corner_closure_diagnostic_2026_09_01/DLH_5K_BOUNDARY_INTERIOR_LOCALIZATION.csv` and `reports/dlh_5k_high_wealth_corner_closure_diagnostic_2026_09_01/DLH_5K_CROSS_A_MECHANISM.csv`, deduplicated only by exact (variant,b_index,a_index,z_index) identity; no post-hoc states.

This is an adjudication diagnostic, not a redesign. No source/model/domain equation may change in DLH-5L; no terminal authorizes a domain or HJB change.