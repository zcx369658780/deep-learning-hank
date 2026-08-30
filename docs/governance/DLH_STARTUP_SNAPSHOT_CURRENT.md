# Deep Learning + HANK Startup Snapshot — CURRENT

Date: 2026-08-30

Repository: `zcx369658780/deep-learning-hank`

Local Owner-designated workspace: `D:\deep-learning-hank`

## Governance state

- live GitHub `main` = synchronized repository/governance authority;
- GitHub Issue = Builder task authority only when separately published and activated;
- DSH = bounded Builder/executor;
- ChatGPT = independent fresh-GitHub reviewer / scientific-route authority / task issuer / GitHub governance operator;
- Owner = final scientific-direction authority;
- Builder completion is not acceptance;
- no active Builder task currently exists.

Priority:

`Scientific correctness > Experiment reproducibility > Research iteration speed > Git auditability > Documentation completeness`

## Current scientific stage

`TWO_ASSET_HA_HOUSEHOLD_FOUNDATION_ACCEPTED`

Issue #18 has been independently reviewed and accepted at candidate commit:

`24dde6792f6800f1ae872001587c2a1a3503d919`

Canonical package:

`src/deep_learning_hank/two_asset/`

Canonical household implementation:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

## Accepted source authority

Source repository:

`zcx369658780/dissertation-ch5-two-asset-hank`

Accepted source export:

`exports/matlab_faithful_two_asset_ha.py`

Export-authority marker:

`6469e5a87a00366c1b2af38f27efaa3014206936`

Required transferred artifact SHA-256:

`276D2244B389D6EDE140DAF8B1F9B0BE1F4AA859368941CED1A12BA8A5831AB8`

Source and canonical Git blob identity:

`57e32076f0e11c9a047e1f90f8c2446d4148e457`

Designated MATLAB source:

`HANK_2ASSETS_HJB.m`

MATLAB SHA-256:

`049136B769560040BC678F828F5D3EC5338DDCAA2090D6BED4E40732F56C3EAE`

## Accepted household object

The canonical household foundation now contains:

- state `(b,a,z)`;
- liquid asset `b` and illiquid asset `a`;
- consumption/labor/transfer policy logic;
- adjustment cost;
- MATLAB-faithful HJB iteration operator;
- separate post-convergence operator;
- stationary KFE density solve;
- consumption, effective-labor, liquid-asset, and illiquid-asset aggregates.

Independent review reproduced the validation fixture with:

- HJB convergence: 11 iterations;
- convergence statistic approximately `1.6736e-8`;
- post-convergence `A^T` nullity = 1;
- KFE contaminated-system residual approximately `3.47e-18`;
- density normalization approximately 1;
- illiquid assets `A ≈ 8.9586992251`;
- liquid assets `B ≈ 0.7952878841`;
- consumption `C ≈ 1.0582828618`;
- effective labor `L ≈ 0.9924967366`.

These are validation-fixture results, not empirical calibration.

## Economic structure versus numerical implementation

Maintain an explicit distinction between:

### `ECONOMIC_STRUCTURE`

- two assets;
- household budget structure;
- consumption/labor choices;
- transfer/deposit choice;
- adjustment-cost mechanism;
- productivity heterogeneity and stationary distribution.

### `NUMERICAL_REGULARIZATION / MATLAB_FAITHFUL_IMPLEMENTATION`

- `max(a,a_bar)` denominator floor used in adjustment cost near `a=0`;
- production bare-`a` transfer-FOC pairing retained for faithful parity;
- illiquid-return taper used to stabilize finite-grid stationary distributions;
- exact MATLAB-spdiags-equivalent boundary truncation;
- contaminated-row stationary KFE solve and subsequent density normalization.

These devices are preserved in the canonical faithful baseline but must not all be described as primitive economic equations. Any future redesign of them requires a separate explicit scientific task and new validation.

## Historical route status

- one-asset DLH-3B/DLH-3C kernels remain useful numerical benchmarks only;
- Issue #17 failed two-asset reconstruction remains superseded provenance and is not scientific authority;
- Issue #18 imported the separately accepted Chapter-5 faithful implementation and is now the canonical household foundation.

## Current scientific ceiling

Accepted:

`TWO_ASSET_HA_HOUSEHOLD_HJB_KFE_AGGREGATE_FOUNDATION`

Not yet validated or authorized:

- GE closure;
- transition dynamics / IRFs;
- NK monetary closure;
- regional flow networks / NSR-HANK;
- Deep Learning training or learned flow matrices;
- empirical calibration;
- policy/welfare/paper Results claims.

## Builder state

`NO_ACTIVE_BUILDER_TASK`

Future work requires a separately published and activated GitHub Issue.
