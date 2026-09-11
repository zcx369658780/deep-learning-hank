# DLH-5V-D — Control-Dependent W1 Wide-Stencil Rates and Conservative Same-Process Generator Contract (Umbrella Design)

**Issue:** deep-learning-hank #52 (DLH-5V-D) · **Task type:** `SCIENTIFIC_DESIGN__W1_WIDE_STENCIL_CONTROL_DEPENDENT_RATE_AND_CONSERVATIVE_GENERATOR_CONTRACT`
**Branch:** `dsh/issue-52-dlh-5vd-wide-stencil-rate-contract-2026-09-11` · **Activation:** comment `5630640873`
(`DLH_5VD_CONTROL_DEPENDENT_WIDE_STENCIL_RATE_AND_CONSERVATIVE_GENERATOR_AUTHORIZED`), activation `origin/main` = `aa1a0193757c062f488d492bc075411f96576a45`
**Status:** rate/generator contract frozen for the accepted `T_realloc` sector, submitted for fresh ChatGPT review —
**NOT scientific acceptance**. Owner continuation decision: `APPROVE_DLH_5VD_CONTROL_DEPENDENT_WIDE_STENCIL_RATE_AND_CONSERVATIVE_GENERATOR_GATE`.

## 1. Frozen inputs (accepted DLH-5V-C — not reopened)

`w_in = (-10/19, 0)`, `w_T = (-70/19, +70/19)`, wide transition `(j,i) -> (j-7,i+10)` on regular W-active states
with `j >= 7`; endpoint band `j in {0..6}` deferred; `T_realloc = {mu_a<=0, mu_b>=0, mu_W=mu_a+mu_b<=0}`;
`cone{w_in, w_T} = T_realloc`.

## 2. Frozen contract (this gate) — regular `T_realloc` reallocation sector only

**Rate map (base grid), for each candidate control `(c,l,d)` inside the discrete HJB maximization with
`mu in T_realloc`:**

```
q_T(c,l,d)  = 19 * mu_b / 70
q_in(c,l,d) = 19 * (-mu_W) / 10
```

with `mu = (-a-b, +a)`, `a = mu_b >= 0`, `b = -mu_W >= 0`; refinement scaling `q_T^h = 19 mu_b/(70h)`,
`q_in^h = 19(-mu_W)/(10h)`. Exact first moment `q_in w_in + q_T w_T = mu`; nonnegativity on `T_realloc` (proved).

**Contract items (all frozen exactly):**
- **Activation predicate**: accepted regular W-active source; `j >= 7`; candidate admissible under the accepted
  W-boundary KKT/tangent law; `mu_a <= 0, mu_b >= 0, mu_W <= 0`. Equality cases (`mu_b=0`, `mu_W=0`, `mu=(0,0)`)
  audited; rates vanish continuously (linear in drift). Candidates outside the sector are marked outside the
  contract — no invented transition rule.
- **Uniqueness**: `det[w_in w_T] = -700/361 != 0`; the nonnegative decomposition is unique for every
  `mu in T_realloc`; **no rate tie-breaking needed** inside the sector (only trivial zero-rate boundary cases).
- **Discrete Hamiltonian**: `H_h(c,l,d) = u(c)-v(l) + q_in[V_{s_in}-V_s] + q_T[V_{s_T}-V_s] + switch_z` with rates
  computed **before** maximization; selected control = argmax over admissible `H_h`; no continuous-max->clip->remap.
- **No double counting**: canonical asset generator uses exactly `{q_in, q_T}`; any alternative shared-face
  decomposition is rejected (not equivalent/unique by the uniqueness theorem); productivity switching separate.
- **Conservative rows**: off-diagonal asset rates `>= 0`; `Q_ss(asset) = -(q_in+q_T)`; with switching,
  `Q_ss = -sum(all actual outgoing)`; **`Q 1 = 0` by construction**; forbidden: omitted outside destination with
  retained negative diagonal escape; no later row-sum repair.
- **Same-Q handoff**: candidate controls -> in-`H_h` rates -> selected control/rates -> ONE backward `Q` ->
  future KFE uses exactly `Q^T` (never rebuilds boundary rates from drift).
- **Mass/density downstream**: `p = M g`, `p_dot = Q^T p`, future `Q^T p = 0`; pin/normalization = scale fixing
  only, never leakage repair; Issue #27 pin authority unchanged.
- **Future validation gates (record only)**: finite Q, off-diagonal >= 0, `||Q1||_inf`, orientation/flattening,
  same Q HJB->KFE, SCC/closed recurrent classes, original source-free residual, mass normalization/nonnegativity,
  density via cell weights — not executed now.

## 3. Remaining regular sector (explicitly identified, not designed)

This contract covers only `T_realloc`. The tangent-admissible complement
`{mu_W <= 0} \ T_realloc = {mu_b < 0, mu_W <= 0} = {mu_b < 0, mu_a <= -mu_b}` remains outside this contract:
(i) **reverse reallocation** `mu_a > 0, mu_b < 0, mu_a + mu_b <= 0` (mirror wide stencil `(+7,-10)` would be the
natural object — **not designed here**); (ii) **both-inward depletion** `mu_a <= 0, mu_b < 0, mu_W <= 0`. This is
the **next bounded scientific object**; no full regular-boundary closure is claimed (prior authority proves only
the `T_realloc` sector).

## 4. Interpretation ceiling (Issue §7)

Outcome A establishes only that the regular `T_realloc` obstruction-repair sector has a unique control-dependent
wide-stencil rate map and a conservative same-process generator contract suitable for later implementation. It
does **not** establish complete coverage of every admissible regular W-boundary drift sector, endpoint/corner
closure, implemented HJB/KFE correctness, stationary existence/uniqueness, or numerical `W_max` adequacy.

## 5. Deferred / forbidden in this gate

Deferred: remaining-sector/reverse-tangent design; endpoint/corner closure; code implementation; numerical
generator assembly; HJB/KFE/stationary solving; `W_max`; Issue #27 pin redesign; production rates beyond the
frozen in-`H_h` candidate map. Forbidden: source/economics mutation; grid/aspect change; import of
MATLAB-faithful contaminated-row KFE; aggregates/GE/neural/nominal/calibration/policy/welfare;
PR/merge/close/successor/self-accept.

## 6. File map (exact five-file allowlist)

1. This umbrella design document.
2. `reports/dlh_5vd_wide_stencil_rate_contract_2026_09_11/DLH_5VD_AUTHORITY_CAPSULE.md` — authority digest.
3. `reports/dlh_5vd_wide_stencil_rate_contract_2026_09_11/DLH_5VD_CONTROL_DEPENDENT_RATE_DECOMPOSITION.md` — rate map (§5), activation/equality (§6.1), uniqueness (§6.2), discrete `H_h` (§6.3), no double counting (§6.4).
4. `reports/dlh_5vd_wide_stencil_rate_contract_2026_09_11/DLH_5VD_CONSERVATIVE_GENERATOR_AND_KFE_HANDOFF_CONTRACT.md` — conservative rows (§6.5), same-Q handoff (§6.6), mass/density (§6.7), validation gates (§6.8), remaining sector (§6.9).
5. `reports/dlh_5vd_wide_stencil_rate_contract_2026_09_11/DLH_5VD_TERMINAL_AND_FORBIDDEN_CHECK.md` — single terminal (Outcome A) + forbidden-operation check + fresh state report.
