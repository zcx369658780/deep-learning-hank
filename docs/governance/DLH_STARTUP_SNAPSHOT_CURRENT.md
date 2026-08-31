# Deep Learning + HANK Startup Snapshot — CURRENT

Date: 2026-08-31

Repository: `zcx369658780/deep-learning-hank`

Local Owner-designated workspace: `D:\deep-learning-hank`

## Governance state

- live GitHub `main` = synchronized repository/governance authority;
- GitHub Issue = sole DSH Builder authority after publication + activation;
- DSH = bounded Builder/executor;
- ChatGPT = independent fresh-GitHub reviewer / scientific-route authority / task issuer / governance operator;
- Owner = final scientific-direction authority;
- Builder completion is not acceptance.

Priority:

`Scientific correctness > Experiment reproducibility > Research iteration speed > Git auditability > Documentation completeness`

## Current Builder state

Current published task:

**Issue #25 — DLH-5B: Implement and validate deterministic two-region hand-specified-flow outer fixed point**

Task type:

`SCIENTIFIC_IMPLEMENTATION__TWO_REGION_HAND_SPECIFIED_FIXED_POINT_PROTOTYPE`

Builder authority is active only when Issue #25 remains open, Task Index/Startup identity is synchronized, and the authoritative activation comment is present.

Dedicated branch after activation:

`dsh/issue-25-dlh-5b-two-region-fixed-point-prototype-2026-08-31`

## Latest accepted scientific-design gate

Issue #24 — DLH-5A

Accepted commit merged to `main`:

`820f23375377b21561d261c0850917056dec15c2`

Accepted classification:

`DLH_5A_NETWORK_READY_TWO_REGION_STRUCTURAL_CONTRACT_ACCEPTED`

Acceptance level:

`L3_COMMIT_VERIFIED__SCIENTIFIC_DESIGN_CONTRACT_ACCEPTED`

Accepted artifacts:

- `docs/specifications/DLH_5A_NETWORK_READY_TWO_REGION_STRUCTURAL_AND_OUTER_FIXED_POINT_CONTRACT_2026_08_31.md`
- `docs/audits/DLH_5A_HISTORICAL_MATLAB_PROVENANCE_AND_REPLACEMENT_BOUNDARY_2026_08_31.md`

## Accepted A1/A2 structural contract

A1/A2 is a two-region **real structural HA-GE outer-fixed-point prototype**.

Binding economics:

- household block = accepted two-asset HA/HJB/KFE foundation;
- `K_i = M_i * A_i` is the provisional exploratory private-capital closure;
- `B_i` is household liquid-asset aggregate/diagnostic only;
- hand-specified labor network uses `m_i^L / W^L / P^L`, `F^L_ij=M_i L_i^home P^L_ij`, `L_j^dest=sum_i F^L_ij`;
- composite wage `wbar_i=sum_j P^L_ij w_j`;
- firm block `Y_i=Z_i K_i^alpha_i (L_i^dest)^(1-alpha_i)`, `w_i=(1-alpha_i)Y_i/L_i^dest`, `r_i^a=alpha_i Y_i/K_i-delta_i`;
- outer state `Gamma={w_1,w_2,r_1^a,r_2^a}`;
- both regional HA solves use the same immutable old `Gamma^(n)` snapshot (Jacobi/synchronous);
- common `r_b`, regional taxes/transfers remain exogenous for A1/A2;
- genuine nominal HANK remains deferred to Track B.

The accepted current `solve_household_steady_state` fail-closes if HJB does not converge. Historical MATLAB KFE-after-false behavior is provenance only and must not be silently reintroduced.

## Accepted household foundation

Canonical source:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Accepted Issue #23 commit:

`b038db800da3760cebee484b1c7a76bf7c1529d0`

Post-repair identity:

- blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`
- SHA-256 `1795718C469FC3B427CAB8E3D5957C133BEAD6EACC9EF0A25A3EDB7211D1A024`

Old `B_hh=B_gov=1` / nested-Brent GE closure is superseded and must not be resumed.

## DLH-5B exact exploratory fixture

The exact task authority is Issue #25. Summary only:

### Household fixture — both regions

Reuse the accepted `VALIDATION_FIXTURE_NOT_CALIBRATION` from `tests/test_dlh_4b_transfer.py`:

```text
rho=0.02, gamma_c=2.0, phi=5.0, chi_0=0.1, chi_1=2.0,
a_bar=1e-6, mu_z=0, sigma_z=0
b-grid: [-2,5], 20 points
a-grid: [0,10], 20 points
z=[0.8,1.3]
switch=[[-1/3,1/3],[1/3,-1/3]]
r_b=0.015, tau_i=0.15, T_i=0, rb_gap_i=0.01
HJB Delta=1000, tol=1e-7, maxit=1000, drift tol=1e-12
```

Baseline labor/value initialization must reuse the exact accepted household fixture logic. Its local scalar Brent solve is allowed only for household initialization; it is not outer GE authority.

### Symmetric network

```text
M_1=M_2=1
m_1^L=m_2^L=0.10
W_12=W_21=1
P^L=[[0.9,0.1],[0.1,0.9]]
```

No migration resource cost.

### Deterministic firm anchor

Anchor:

```text
w_1*=w_2*=1.0
r_1^a*=r_2^a*=0.03
alpha_1=alpha_2=1/3
```

Run the accepted household solve once at anchor and record `A*,L*,C*,B*`. With symmetry and `M=1`, set `K*=A*`, `Ldest*=L*` and derive once:

```text
Z* = [1/(1-alpha)] * (L*/K*)^alpha
delta* = [alpha/(1-alpha)] * (L*/K*) - 0.03
```

Require finite positive anchor objects and `0<delta*<1`; otherwise fail closed. Then freeze the same `Z*,delta*` for both regions and all DLH-5B cases. This is a validation-fixture anchor, not empirical calibration.

## DLH-5B experiments

### S0 — anchor smoke

`Gamma0={1.0,1.0,0.03,0.03}`.

Full one-turn map must satisfy `R_w<=1e-10`, `R_ra<=1e-10` plus all validity gates. If S0 fails, stop before S1.

### S1 — asymmetric perturbation

```text
w_1=0.99, w_2=1.01
r_1^a=0.0295, r_2^a=0.0305
lambda=0.5
tol_w=tol_ra=1e-6
max_iter=25
```

No retry or adaptive retuning. Convergence is positive evidence; deterministic nonconvergence/household fail-closed is preserved negative research evidence.

### S2 — region-order invariance

Evaluate same S1 snapshot in explicit orders `[1,2]` and `[2,1]`; complete one-turn numeric difference must be `<=1e-12`.

## DLH-5B validity/reproducibility

- labor/accounting/network identities: abs+rel tolerance `1e-12`;
- order invariance: `1e-12`;
- KFE integrated mass error `<=1e-10`;
- KFE min density `>=-1e-10` and finite;
- firm factors `K,L>0`, output/wage positive finite, return finite;
- boundary masses on four asset edges must be reported; threshold `0.10` is non-blocking warning only;
- no grid expansion;
- S0/S1 deterministic repeats required; numeric trace differences `<=1e-12` with identical stop reason/iteration count as applicable;
- randomness `NOT_APPLICABLE`;
- retry policy `NO_AUTOMATIC_RETRY`;
- output root `reports/dlh_5b_two_region_fixed_point_2026_08_31/`, no-overwrite mandatory.

## Issue #25 allowed paths

Only the explicit allowlist in Issue #25 is Builder authority. It includes new regional implementation/config/test paths and required new evidence under the DLH-5B report root.

The accepted household source, existing GE code, historical outputs, roadmaps and governance files are not Builder-mutable under Issue #25.

## DLH-5B explicit non-authority

No:

- household redesign;
- fixed-bond `B=1` closure;
- outer Brent/Newton/fsolve;
- PASS-seeking fixture changes;
- adaptive damping/retry/grid expansion;
- `GovInv`;
- learned `W^L` or `W^K`;
- neural training;
- nominal rigidity/Taylor/Fisher/new debt closure;
- 31-region scaling;
- policy/welfare/Results claims.

## Current scientific route

Working label: `Network-Structured Regional HANK (NSR-HANK)`.

Current sequence:

1. accepted two-asset HA foundation;
2. accepted two-region design contract;
3. **DLH-5B current: deterministic hand-specified-flow implementation/validation**;
4. OD-year data schema + transparent baseline;
5. learned labor-flow network `W^L`;
6. 3–5 region equilibrium embedding;
7. separately frozen/validated minimal genuine nominal HANK;
8. learned `W^K` later;
9. equilibrium-constrained calibration / parameter mapping;
10. 31-region panel / automated pipeline;
11. policy/welfare only after all gates.

## Scientific ceiling during Issue #25

Issue #25 may establish only the deterministic two-region real structural prototype, including convergence or preserved nonconvergence evidence, conservation/accounting validity, reproducibility and order invariance.

It does not establish learned networks, empirical calibration, genuine nominal HANK, 31-region results, policy/welfare or paper Results authority.

## DSH startup sequence

1. `Set-Location D:\deep-learning-hank`;
2. verify repo/remote/worktree;
3. `git fetch origin` and record fresh `origin/main`;
4. read all CURRENT rules;
5. read fresh Task Index and this Startup Snapshot;
6. read accepted DLH-5A contract/audit;
7. read Issue #25 latest body/comments and verify activation;
8. verify accepted household identity/read its API and canonical fixture source;
9. create the exact Issue #25 dedicated branch from fresh `origin/main`;
10. implement/test/run only the exact Issue allowlist;
11. commit/push and STOP for fresh ChatGPT independent review.
