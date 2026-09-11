# DLH-5V-C — W1 Wide-Stencil Exact-Tangent Regular-Frontier Feasibility Audit

**Issue:** deep-learning-hank #51 (DLH-5V-C) · **Task type:** `SCIENTIFIC_DESIGN__W1_WIDE_STENCIL_EXACT_TANGENT_REGULAR_FEASIBILITY`
**Branch:** `dsh/issue-51-dlh-5vc-w1-wide-stencil-tangent-2026-09-11` · **Activation:** comment `5629684453`
(`DLH_5VC_W1_WIDE_STENCIL_EXACT_TANGENT_REGULAR_FEASIBILITY_AUTHORIZED`), activation `origin/main` = `b7930358e54ac9d86c4e2e05d027cf921900c9c6`
**Status:** feasibility audit submitted for fresh ChatGPT review — **NOT scientific acceptance**. Owner route
decision: `APPROVE_ROUTE_F_WIDE__W1_NATIVE_EXACT_TANGENT_REGULAR_AUDIT`.

## 1. Frozen inputs (accepted DLH-5V-A/B — not reopened)

Grid `da = 10/19`, `db = 7/19`; displacement map `Delta x = ((10/19) Delta j, (7/19) Delta i)`. Accepted local
shared-face obstruction: `A^F: K={7 mu_a+10 mu_b<=0}`, `A^L: K={mu_a<=0, 7 mu_a+10 mu_b<=0}`, `B^W: K=R^2`.
Continuous target `T_realloc = {mu_a<=0, mu_b>=0, mu_a+mu_b<=0}`; exact sliding `(-u,+u)`.

## 2. Primary candidate (exact tangent, this gate)

Native tangent condition `10 Delta j + 7 Delta i = 0`. Since `gcd(10,7)=1`, the integer tangent lattice is
`(Delta j, Delta i) = k(7,-10)`, `k in Z`; the primitive reallocation solution is

```
v_T = (-7, +10),   Delta x_T = (-70/19, +70/19),   Delta a + Delta b = 0 (exact).
```

## 3. Submitted candidate results (exact; reports = files 3–4)

| audit item (Issue §5) | result |
|---|---|
| 5.1 represented destination `(j-7,i+10)` | **PROVED** for all represented sources with `j>=7`: `10(j-7)+7(i+10)=10j+7i<=N`; `a>=0` needs `j>=7`; `b>=b_min`, `a<=a_max`, W-membership, and the full straight segment inside `D_W` all hold exactly; the only excluded band is the finite 7-column endpoint strip `j in {0..6}` (deferred) |
| 5.2 phase/class preservation | **PROVED**: `r_{j-7} = r_j` (exact period-7 inverse shift), `A^F->A^F`, `A^L->A^L`, `B^W->B^W`, top/sub-top offset preserved (`i_t(j-7)=i_t(j)+10`) |
| 5.3 tangential-cone closure | **PROVED (equality)**: `cone{(-10/19,0), (-70/19,+70/19)} = T_realloc`; generic `mu=(-a-b,+a)`: coefficients `(19b/10)` on local inward, `(19a/70)` on wide tangent, nonnegative |
| 5.4 monotone CTMC certificate | **PROVED (symbolic only)**: `q_T = 19a/(70h)`, `q_in = 19b/(10h)` realize the exact first moment; no production rate function frozen |
| 5.5 refinement/locality | **PROVED**: physical jump `O(h)`; required rate `O(1/h)`; exact first-moment consistency for smooth test functions; second-order remainder `O(h)`; fixed 17-step index distance compatible (physical jump -> 0, `17/N_h = O(h)`) |
| 5.6 cell/face-control (same-process) | **PROVED coherent**: the identical wide edge enters `H_h` and `p_dot = Q^T p` with one `Q`, one controlled process — an explicit **boundary wide-stencil Markov transition**, NOT a shared-face finite-volume flux |
| 5.7 hidden path violation | **NONE in the regular region**: `a+b = const` along the segment; `a=0` crossing confined to the deferred band `j<7` |

**No recurring regular-class failure condition from Issue §7 is proven**; all remaining failures are confined to
the precisely identified finite endpoint band (`j in {0..6}`), deferred to endpoint/corner closure.

## 4. Bounded meaning (Issue §6)

Outcome A establishes only: on recurring regular W-frontier states sufficiently far from endpoint/joint-boundary
regions, a W1/native wide-stencil exact-tangent transition is **geometrically and asymptotically compatible**
with a monotone same-process CTMC design. It does **not** authorize production rates, endpoint/corner handling,
HJB policy implementation, KFE/stationary execution, or numerical `W_max`.

## 5. Deferred / forbidden in this gate

Deferred: production rate design/freeze; endpoint/corner closure; strict face-flux replacement semantics;
implementation; numerical `W_max`; stationary KFE; aggregates/GE; neural/nominal/calibration/policy/welfare.
Forbidden: source/economics mutation; production grid/aspect change; wide-stencil code; production generator
assembly; broad phase enumeration; HJB/KFE/stationary execution; PR/merge/close/successor/self-accept.

## 6. File map (exact five-file allowlist)

1. This umbrella design document.
2. `reports/dlh_5vc_w1_wide_stencil_tangent_2026_09_11/DLH_5VC_AUTHORITY_CAPSULE.md` — authority digest.
3. `reports/dlh_5vc_w1_wide_stencil_tangent_2026_09_11/DLH_5VC_DESTINATION_PHASE_AND_DOMAIN_AUDIT.md` — primitivity, destination/domain audit (§5.1, §5.7), phase/class preservation (§5.2).
4. `reports/dlh_5vc_w1_wide_stencil_tangent_2026_09_11/DLH_5VC_MOMENT_LOCALITY_AND_SAME_PROCESS_AUDIT.md` — cone closure (§5.3), CTMC certificate (§5.4), refinement/locality (§5.5), same-process (§5.6), failure-condition check.
5. `reports/dlh_5vc_w1_wide_stencil_tangent_2026_09_11/DLH_5VC_TERMINAL_AND_FORBIDDEN_CHECK.md` — single terminal (Outcome A) + forbidden-operation check + fresh state report.
