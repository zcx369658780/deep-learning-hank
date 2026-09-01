# DLH-5G — Forbidden-Operation / Scope Check (Issue #31)

DSH did NOT perform any of the following during DLH-5G execution:

| Forbidden operation | Status |
|---|---|
| Modify `matlab_faithful_two_asset_ha.py` | NOT performed (immutable) |
| Modify `upper_domain_stationary_tail_diagnostic.py` | NOT performed (read-only reference) |
| Modify any existing HJB/local-policy/KFE/regional source | NOT performed |
| Modify accepted Issues #23-#29 evidence | NOT performed |
| Modify `a_max`, a-grid, `da` or accepted illiquid-return taper | NOT performed (frozen) |
| Modify economics/prices/parameters/tolerances/initialization | NOT performed (frozen D0) |
| Warm-start one grid from another | NOT performed (fresh initialization per variant) |
| Add adaptive/seventh grid or grid search | NOT performed (exact G0-G5) |
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

Terminal classification: `DLH_5G_LIQUID_B_PREFROZEN_EXTENT_REACHES_BOUNDARY_THRESHOLD__GPT_REVIEW_REQUIRED`

Secondary annotations: `DLH_5G_B_RESOLUTION_SENSITIVITY_REMAINS_MATERIAL__SEPARATE_NUMERICAL_REVIEW_REQUIRED`

Stationary fields marker: `NOT_AUTHORIZED__DLH_5G_POLICY_ONLY_LIQUID_DOMAIN_DIAGNOSTIC`
