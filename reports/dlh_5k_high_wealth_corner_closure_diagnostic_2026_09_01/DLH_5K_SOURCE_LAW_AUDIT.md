# DLH-5K Phase A — accepted MATLAB-faithful source-law audit

Source (read-only): `src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py (accepted blob, read-only)`; blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`; SHA-256 `1795718C469FC3B427CAB8E3D5957C133BEAD6EACC9EF0A25A3EDB7211D1A024`.

## Accepted drift decomposition (derived from the implemented equations only)

```text
mu_b = base_liquid_surplus + transfer_injection
base_liquid_surplus = r_b*b + labor_income - (consumption - transfer_income)
transfer_injection = -transfer - adjustment_cost
```

- Special case (When the liquid zero-drift ('0') branch holds, consumption equals total liquid resources so base_liquid_surplus = 0 and mu_b = -transfer - adjustment_cost. This is an implemented-source identity under the stated branch conditions, NOT an economic theorem.)

## Exact accepted implementation ordering (8 audited objects)

### Upper-b derivative closure (`upper_b_derivative_closure`)

- Source fact: At the top liquid node i=n-1, the forward liquid derivative V_b^+ is closed from a resource-based marginal utility, not from the value function: vb_f[n-1,j,z] = resources^(-gamma_c) with resources = (1-tau)*w*z*labor0 + transfer_income + r_b_eff*b_top (solve loop, lines 536-541). The interior forward/backward derivatives are vb_f[:-1]=(V[1:]-V[:-1])/db and vb_b[1:]=vb_f[:-1] (line 533).
- Implied identity: At the top node, V_b^+(closure) is the marginal utility of the notional resource branch at baseline labor0; this is what consumption/labor FOCs see through the 1e-6 derivative floor.

### Liquid resource / consumption branch construction (`liquid_resource_branch`)

- Source fact: vb_b=max(v_b_backward,1e-6), vb_f=max(v_b_forward,1e-6) for controls (lines 270-271). consumption_b=vb_b^(-1/gamma_c), consumption_f=vb_f^(-1/gamma_c); liquid_resources = net_wage*labor + transfer_income + effective_r_b*b; sc_b=liquid_resources_b-consumption_b, sc_f=liquid_resources_f-consumption_f. If sc_b<-tol -> liquid_label 'B'; elif sc_f>tol -> 'F'; else liquid_label '0' with labor=baseline_labor and consumption=net_wage*baseline_labor + transfer_income + effective_r_b*b (lines 281-298).
- Implied identity: In the '0' branch, consumption equals total liquid resources, so base_liquid_surplus = r_b*b + labor_income - (consumption - transfer_income) = 0 exactly by construction.

### Transfer candidate d construction (`transfer_candidate`)

- Source fact: transfer_candidate(v_a,v_b,a,params) computes q=V_a/V_b-1 and returns a*threshold/chi_1 with threshold=min(q+chi_0,0)+max(q-chi_0,0) using the RAW liquid derivative (bare-a FOC, no 1e-6 floor; Issue #23 narrow repair, lines 85-99). Four candidates d_bb(v_a_b,v_b_b), d_bf(v_a_f,v_b_b), d_fb(v_a_b,v_b_f), d_ff(v_a_f,v_b_f) are assembled by logical masks d_b=d_bf*(d_bf>0)+d_bb*(d_bb<0), d_f=d_ff*(d_ff>0)+d_fb*(d_fb<0) (lines 302-312).
- Implied identity: The transfer FOC uses bare a (not max(a,a_bar)); the direction masks implement the chi kink: positive d only if q>chi_0, negative d only if q<-chi_0.

### Upper-a transfer-direction restriction (`upper_a_transfer_restriction`)

- Source fact: At the upper illiquid boundary a=a_max: d_b=d_bb*(d_bb<-tol) and d_f=d_fb*(d_fb<-tol), i.e. only NEGATIVE (withdrawal, inward-a) transfer candidates survive (lines 318-320). At the lower boundary only positive candidates survive (lines 313-317).
- Implied identity: At a=a_max, mu_a = r_a_eff*a + d <= 0 is enforced by admitting only d<0 with |d| large enough; the chosen d is the transfer-FOC candidate d_bb/d_fb.

### Upper-b transfer-direction override (`upper_b_transfer_override`)

- Source fact: sdh_b=-d_b-adjustment_cost(d_b), sdh_f=-d_f-adjustment_cost(d_f); use_transfer_f=sdh_f>tol, use_transfer_b=sdh_b<-tol and not use_transfer_f. At the upper liquid boundary: use_transfer_f=False and use_transfer_b=True (forced backward-transfer branch); at the lower liquid boundary use_transfer_b=False (lines 322-355).
- Implied identity: At b=b_max the forward transfer selection is disabled and the backward transfer branch (d_b) is forced, so transfer = d_b.

### Adjustment cost (`adjustment_cost`)

- Source fact: adjustment_cost(d,a,params)=chi_0*|d|+0.5*chi_1*d^2/max(a,a_bar) (lines 80-83). The denominator uses max(a,a_bar) (a_bar=1e-6 floor), unlike the transfer FOC which uses bare a.
- Implied identity: cost is convex in d with the a_bar floor; at d=-x<0, cost=chi_0*x+0.5*chi_1*x^2/max(a,a_bar).

### Final mu_a / mu_b evaluation (`final_mu_a_mu_b`)

- Source fact: asset_drifts_matlab_faithful computes cost=adjustment_cost(transfer,a,params), labor_income=sum(wages*(1-tau-migration_costs)*z*labor), mu_b=r_b*b+labor_income-transfer-cost-consumption_net where the wrapper passes consumption_net = consumption - transfer_income (lines 379-389, 138-157). mu_a=r_a_eff(a)*a+transfer with the MATLAB taper r_a*(1-0.1*(a/a_max)^9) (lines 155-156).
- Implied identity: mu_b = [r_b*b + labor_income - (consumption - transfer_income)] + [-transfer - adjustment_cost] = base_liquid_surplus + transfer_injection, exactly by construction.

### Requested generator-rate conversion (`requested_rate_conversion`)

- Source fact: b_forward_rate=max(mu_b,0)/db, b_backward_rate=max(-mu_b,0)/db; a_forward_rate=mh_f/da, a_backward_rate=-mh_b/da with mh_b=min(shadow_transfer_b,0) and mh_f=max(shadow_transfer_f,0)+effective_return*a (lines 404-415); the post-convergence operator uses max(mu_b,0)/db, max(-mu_b,0)/db, max(mu_a,0)/da, max(-mu_a,0)/da (line 562).
- Implied identity: The requested generator rate is raw outward drift divided by spacing (max(mu,0)/spacing), the HJB/KFE boundary-compatibility quantity.

## Frozen objects in every DLH-5K rerun

- `wbar=1.0`, `r_a=0.03`; a in [0.0,10.0], `a_max=10.0`, taper `r_a*(1-0.1*(a/a_max)^9)_MATLAB_FAITHFUL_UNCHANGED`; `b_lo=-2.0`, `db=0.368421052632`; a resolutions ['a77', 'a153']; b extents ['b120', 'b140', 'b160']; b160_IS_THE_HARD_ROUTE_CEILING__NO_B180_B200__NO_NEW_GRID.

This is an adjudication diagnostic, not a redesign. No source/model equation may change in DLH-5K; no terminal authorizes a source change.