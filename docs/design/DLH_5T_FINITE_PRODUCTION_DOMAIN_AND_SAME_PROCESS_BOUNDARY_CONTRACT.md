# DLH-5T — Finite Production-Domain and Same-Process HJB–KFE Boundary Contract

**Issue #46 — OPEN.** `SCIENTIFIC_DESIGN__FINITE_PRODUCTION_DOMAIN_AND_SAME_PROCESS_HJB_KFE_BOUNDARY_CONTRACT`
**Branch:** `dsh/issue-46-dlh-5t-finite-domain-same-process-boundary-2026-09-03`
**Fresh `origin/main`:** `01865f2a6d6099f47031f5f3a79653dcbdbf2374`
**Activation comment:** `5519463570`
**Owner route decision:** `APPROVE_ROUTE_D_FINITE_PRODUCTION_DOMAIN_AND_JOINT_HJB_KFE_BOUNDARY_DESIGN`

This is the umbrella design contract for the DLH-5T design-only gate. It freezes the
finite production domain, the boundary HJB/KKT law, the same-process HJB-KFE law, and
the `W_max` adequacy method, and it states the exact terminal. Companion reports
contain the detailed derivations and evidence.

**Status: DESIGN / PROVENANCE ONLY.** No source mutation, no HJB/KFE/grid/stationary
execution, no numerical `W_max` selection.

---

## 1. Controlling accepted authority

- Fresh live `main` at this gate: `01865f2a6d6099f47031f5f3a79653dcbdbf2374`.
- Latest accepted gate: Issue #45 / DLH-5S (candidate `160781a…`, acceptance
  `5519142363`, integration `75bedf6…`, terminal Outcome B — infinite-domain p=2
  caveat preserved through Route D).
- Accepted household source (immutable/read-only):
  `src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`, blob
  `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`.
- Binding Issue #27 law: `HJB boundary policy <=> KFE boundary transition law`.
- Stationary KFE remains **NOT AUTHORIZED** in this Issue.

## 2. Frozen finite production domain `D_W`

```text
D_W(W_max) = { (a,b,z) : 0 <= a <= a_max, b >= b_min, a + b <= W_max, z in {z0,z1} }
```

- `a >= 0` (floor `a_bar`): economic non-negativity — face `mu_a >= 0`.
- `b >= b_min = -2`: economic borrowing floor — face `mu_b >= 0`.
- `a <= a_max = 10`: computational truncation + taper anchor — face `mu_a <= 0`.
- `a + b <= W_max`: **numerical production-domain truncation** (not a household
  primitive / calibrated parameter / wealth ceiling) — face `mu_W = mu_a + mu_b <= 0`.
- `W_max` is **not selected** in DLH-5T; the selection METHOD is frozen (Section 6).

## 3. Frozen boundary tangent-cone / KKT law

At a boundary state the HJB maximizes over controls admissible to the active tangent
cone (never unconstrained-policy-then-clip):

```text
rho*V = sup_{c,l,d : mu·n <= 0 on active faces} { u(c) - v_l*l + V_a*mu_a + V_b*mu_b }
```

Unified KKT convention (maximization, upper constraints): `L = H - sum lambda_j g_j`,
`g_j = mu·n_j <= 0`, `lambda_j >= 0`, `lambda_j*g_j = 0`. Effective gradients:
lower faces `V + lambda`, upper/W faces `V - lambda`.

Tangent cones (jointly at every feasible intersection):

```text
a = 0:           mu_a >= 0
b = b_min:       mu_b >= 0
a = a_max:       mu_a <= 0
a + b = W_max:   mu_W <= 0
```

Distinguishing facts (derived in the HJB/KKT report):

- at the `W` face `lambda_W` cancels one-for-one from the linear transfer FOC and
  survives only through the adjustment-cost term; the reallocation is not fully free;
- at `a=0`, `mu_a = d`, so `mu_a >= 0` is exactly the accepted `d >= 0` transfer
  mask;
- at `a=a_max`, `mu_a = 0.27 + d` under the accepted anchors, so `mu_a <= 0`
  requires `d <= -0.27` — materially stricter than the accepted MATLAB `d <= 0`
  mask, confirming the accepted source ordering is not KKT-equivalent and must be
  superseded by the constrained policy.

All face/intersection laws (lower-a, lower-b, upper-a, W, lower-a×lower-b,
upper-a×lower-b, upper-a×W, lower-a×W, lower-b×W with exact `W_max`-existence
conditions) are frozen in the HJB/KKT report.

## 4. Frozen same-process HJB-KFE law

```text
controlled process selected by boundary HJB
        ==
controlled process represented by KFE generator
```

- `Q[row,col] > 0 (row != col)` means `row -> col`; `Q V` backward/HJB, `Q^T g`
  forward/KFE.
- No KFE-only clipping; a boundary-HJB inadmissible outward request is a
  **boundary-HJB scientific failure**, not a KFE repair.
- Every off-diagonal transition corresponds to an HJB-admitted controlled transition
  (including admitted tangential flow on the `W` face).
- Diagonal = minus the sum of ACTUALLY admitted represented off-diagonal rates; no
  outward destination omitted by the mask retains a diagonal exit rate; row sums 0,
  nonnegative off-diagonals within frozen tolerances.
- Contamination/pin-row normalization stays **downstream**, after an accepted
  same-process conservative generator exists; it plays no role in boundary-policy
  repair (Issue #27 interpretation preserved, `0.37*N` parity unchanged).

## 5. W1 representation — frozen semantics and the one open point

W1 = native `(a,b)` tensor coordinates + mask `a_j + b_i <= W_max`. Frozen: the
represented-state mask; frontier sets; one-sided/tangent behavior (outward-normal
drift non-positive by the KKT law); transition orientation; boundary-admitted rates;
diagonal construction; same-stencil HJB/KFE consistency; conservation implications.

**Open point (drives the terminal):** on the accepted axial lattice
(`da = 10/19 != db = 7/19`) the `W`-face tangent `(1,-1)` is off-axis, so the
tangential component of an HJB-admitted boundary drift (`mu_b > 0, mu_a < 0,
mu_W <= 0`) cannot be represented by axial moves; a faithful representation requires
an off-axis flux construction whose exact form is not determined by the accepted
science and cannot be validated in a design-only gate. W1 is therefore **not
implementation-ready at the design level** (Issue #46 §8). No silent switch to W2.

## 6. Frozen `W_max` adequacy protocol (method, not number)

Nested candidates `W_max^(1) < W_max^(2) < W_max^(3)`; the accepted production cap is
the smallest passing all applicable accepted gates in order:

- A. HJB-stage shared-interior policy stability (`c,l,d,mu_a,mu_b,mu_W` + value/
  derivative diagnostics on aligned shared-interior states);
- B. HJB-stage boundary-influence localization (decay on a pre-registered common
  interior);
- C. future KFE-stage stationary-tail influence (design only now);
- D. future aggregate-stage stability (`C,L,A,B`);
- E. future GE-stage stability (wages, illiquid returns, two-region fixed point).

Pre-registered comparison quantities and tolerance families; tolerances must not be
loosened to obtain PASS.

## 7. Exact Builder allowlist (only files created by this gate)

1. `docs/design/DLH_5T_FINITE_PRODUCTION_DOMAIN_AND_SAME_PROCESS_BOUNDARY_CONTRACT.md` (this file)
2. `reports/dlh_5t_finite_production_domain_same_process_boundary_2026_09_03/DLH_5T_AUTHORITY_AND_EVIDENCE_FREEZE.md`
3. `reports/dlh_5t_finite_production_domain_same_process_boundary_2026_09_03/DLH_5T_W_DOMAIN_AND_W1_REPRESENTATION.md`
4. `reports/dlh_5t_finite_production_domain_same_process_boundary_2026_09_03/DLH_5T_HJB_KKT_BOUNDARY_LAWS.md`
5. `reports/dlh_5t_finite_production_domain_same_process_boundary_2026_09_03/DLH_5T_SAME_PROCESS_KFE_GENERATOR_CONTRACT.md`
6. `reports/dlh_5t_finite_production_domain_same_process_boundary_2026_09_03/DLH_5T_WMAX_ADEQUACY_PROTOCOL.md`
7. `reports/dlh_5t_finite_production_domain_same_process_boundary_2026_09_03/DLH_5T_IMPLEMENTATION_READINESS_AND_TERMINAL.md`
8. `reports/dlh_5t_finite_production_domain_same_process_boundary_2026_09_03/DLH_5T_FORBIDDEN_OPERATION_CHECK.md`

No existing tracked file is modified by the Builder.

## 8. Terminal

```text
DLH_5T_W_DOMAIN_SCIENTIFICALLY_SUPPORTED__W1_DISCRETE_PROCESS_MATCHING_REQUIRES_BOUNDED_FOLLOWUP_DESIGN
```

Rationale (Issue #46 §14, Outcome B): the W-domain `D_W` economic/numerical logic and
all continuous tangent-cone/KKT laws are scientifically supported and frozen, but a
specific discrete masked-grid (W1) process-matching ambiguity — the tangential-drift
representation on the slanted `W` face on the accepted axial lattice — prevents an
implementation-ready contract. Not Outcome C (no scientific inconsistency
demonstrated); not Blocked (accepted source/evidence is internally consistent). No
terminal authorizes HJB/KFE execution or production integration.

## 9. Forbidden operations (summary)

Design-only: no source mutation, no HJB/KFE/stationary/grid execution, no numerical
`W_max`, no b160 reopen, no grid/taper/FOC/transfer change, no W1/KKT/generator
implementation, no contamination sensitivity, no aggregates/GE/neural/nominal/
calibration/policy/welfare/Results, no PR/merge/close/successor/self-accept. See the
forbidden-operation check.

## 10. Stop

The Builder completes the design package, commits and pushes the dedicated branch,
and **stops for fresh ChatGPT review**. No merge, close, successor Issue or
self-acceptance from the Builder.
