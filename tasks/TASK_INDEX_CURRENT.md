# Deep Learning + HANK Task Index

Status: `DLH_4C_OPTION_A_GE_CLOSURE_CONTRACT_ACCEPTED__SUCCESSOR_PENDING`

Last synchronized: 2026-08-30

Repository: `zcx369658780/deep-learning-hank`

## Accepted scientific state

Issue #19 / DLH-4C is accepted at commit:

`7fcfd6412c580f888d2ef8175335c3909f146e59`

Accepted classification:

`DLH_4C_OPTION_A_GE_CLOSURE_CONTRACT_ACCEPTED`

Owner-frozen Option A:

- `K = A_hh`;
- `B_hh = B_gov` with constant exogenous real government bond supply;
- competitive firms, `mu = 1`;
- `Y = Z*K^alpha*L^(1-alpha)`;
- `w = F_L`;
- `r_a = F_K - delta`;
- balanced transfer `T = tau*w*L - r_b*B_gov`;
- GE unknowns `x = (r_a, r_b, L)`;
- root residuals `(A_hh-K, B_hh-B_gov, L_hh-L)`.

Faithful resource accounting must report separately:

- `R_resource_structural = Y - C - delta*K - AC`;
- `W_taper = integral[(r_a-r_a_eff(a))*a*g]`;
- `R_resource_faithful = R_resource_structural - W_taper`.

Only `R_resource_faithful` is a near-zero faithful numerical gate while the accepted taper remains active.

## Immutable household foundation

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`57e32076f0e11c9a047e1f90f8c2446d4148e457`

SHA-256:

`276D2244B389D6EDE140DAF8B1F9B0BE1F4AA859368941CED1A12BA8A5831AB8`

No future task may modify this accepted household oracle without a new explicit Owner scientific decision.

## Builder authority

No successor Builder authority is active until a separately published and activated GitHub Issue is created.
