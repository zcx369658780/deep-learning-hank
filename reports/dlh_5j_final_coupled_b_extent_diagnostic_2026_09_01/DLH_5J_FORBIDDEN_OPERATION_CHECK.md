# DLH-5J — Forbidden-Operation / Scope Check (Issue #36)

DSH did NOT perform any of the following during DLH-5J execution:

| Forbidden operation | Status |
|---|---|
| Modify `matlab_faithful_two_asset_ha.py` | NOT performed (immutable) |
| Modify `coupled_boundary_frontier_diagnostic.py` | NOT performed (read-only reference) |
| Modify any existing HJB/local-policy/KFE/regional source | NOT performed |
| Modify accepted Issues #23-#35 evidence | NOT performed |
| Change physical a domain, `a_max=10` or accepted taper | NOT performed (frozen) |
| Widen a domain | NOT performed |
| Change a resolution outside a77/a153 | NOT performed (only a77/a153) |
| Change `db` from 7/19 | NOT performed (db=7/19 frozen) |
| Use a b extent beyond b160 | NOT performed (b160 is the hard route ceiling) |
| Rerun b100 as an extra variant | NOT performed (read-only scalar anchors only) |
| Modify economics/prices/parameters/tolerances/initialization | NOT performed (frozen D0) |
| Warm-start one grid from another | NOT performed (fresh initialization per variant) |
| Add adaptive/seventh grid, grid search or root-seeking extent | NOT performed (exact J0-J5) |
| Clip policy | NOT performed |
| Run stationary KFE / nullspace / pin / density / tail / aggregates | NOT performed (policy-only) |
| Run D1-D3 | NOT performed |
| Run two-region or multi-province GE | NOT performed |
| Run `31_PROVINCE_HOUSEHOLD_UPPER_DOMAIN_AUDIT` | NOT performed |
| Train any network | NOT performed |
| Enter nominal HANK / calibration / policy / welfare / Results | NOT performed |
| Mutate governance files from the Builder branch | NOT performed |
| `git add .` / `git add -A` | NOT performed (explicit staging only) |
| Create PR / merge / close Issue / successor / self-accept | NOT performed |

Terminal classification: `DLH_5J_JOINT_BOUNDARY_COMPATIBILITY_NOT_ROBUST_ACROSS_A_RESOLUTION__SCIENTIFIC_REVIEW_REQUIRED`

Secondary annotations: `DLH_5J_CROSS_A_POLICY_RESOLUTION_SENSITIVITY_REMAINS_MATERIAL__NUMERICAL_REVIEW_REQUIRED`

Stationary fields marker: `NOT_AUTHORIZED__DLH_5J_POLICY_ONLY_FINAL_BOUNDED_EXTENT_DIAGNOSTIC`
