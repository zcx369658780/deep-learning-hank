# DLH-5Q — Forbidden-Operation / Scope Check (Issue #43 §11) — Rev 3

DLH-5Q is a **theorem-verification + falsification-design gate only**. DSH performed
NONE of the following during DLH-5Q (Rev 1 `9f5774d`, Rev 2 `593f569`, Rev 3 on the
same dedicated branch); no source, model, domain, numerical, or endpoint object was
touched.

| Forbidden operation | Status |
|---|---|
| Modify accepted HJB/KFE/regional source (`matlab_faithful_two_asset_ha.py`) | NOT PERFORMED (immutable; blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e` verified on fresh `origin/main`) |
| Modify utility / transfer FOC / adjustment cost / taper / prices / taxes / calibration | NOT PERFORMED (all inherited read-only) |
| Freeze or implement an analytic specification | NOT PERFORMED (S1/S2/S3 are provisional working authority for this task only; no freeze) |
| Choose / implement R, W, W1, W2, `W_max` | NOT PERFORMED (all remain unfrozen) |
| Choose a new numerical `b_max` or new `a_max` | NOT PERFORMED |
| Extrapolate the accepted taper beyond `a_max = 10` | NOT PERFORMED |
| Run or extend HJB grids / domain / resolution | NOT PERFORMED |
| Rerun J0–J5 or previous numerical fixtures | NOT PERFORMED (no numerical run at all) |
| Run stationary KFE / nullspace / pin / density / tail / aggregates | NOT PERFORMED (stationary KFE remains NOT AUTHORIZED under Issue #27) |
| Implement an endpoint KKT or state-domain law | NOT PERFORMED (no `a=10` analytic law invented; `b_lo` adoption not made) |
| Invent an analytic `a=10` boundary law | NOT PERFORMED (explicitly refused; Phase F / A4 — Owner decision item) |
| Enter regional GE / multi-province audit / network training / nominal HANK / calibration / policy / welfare / Results | NOT PERFORMED |
| Create PR / merge / close Issue / successor Issue / self-accept | NOT PERFORMED |
| Promote the finite-grid upper-`b` / lower-`b` marginal-utility closures into infinite-domain boundary/transversality conditions | NOT PERFORMED (explicitly refused; numerical semantics only) |
| Claim `V_inf=0` is a proved necessity or a uniqueness/comparison theorem | NOT PERFORMED (Issue #42 acceptance item 6 controls; it is a provisional selection) |
| Claim the actual HJB solution realizes `p=2` merely because S3 excludes `m=1/2` | NOT PERFORMED (explicitly refused; step 27) |
| Claim the critical `m=1/2` branch is ruled out or economically impossible | NOT PERFORMED (preserved outside S3 as benchmark; step 37) |
| Execute the future numerical falsification protocol | NOT PERFORMED (design only; step 38) |
| Claim consumption dominates for `1<p<2` (reversed-inequality error) | NOT RETAINED — withdrawn in Rev 2; `1<p<2` is excluded by the switch-spectrum argument on the dominant rho/r_b/S block (reviewer `5506978886`) |
| Claim all non-power/exotic S3 tails are formally excluded | NOT PERFORMED — Rev 2 excludes only power families and explicitly tested log/slow families; broader classes remain open (step 18) |
| Use a degenerate derivative-remainder term `|b^2(V_a - R V_b)|` or `M_a = O(K b^(-1/2))` | NOT RETAINED — removed in Rev 2; replaced by the explicit derivative-remainder contract (E) (Phase C C4) |
| Reproduce the S3-incompatible `a`-dependent `M(a,z) b^(-3/2)` value remainder in Phase D alongside `R=O(1)` | NOT RETAINED — removed in Rev 3; Phase D D1 uses the exact contract (E) with all `a`-dependence at `H/b^2` order or smaller; `M_a` forced to 0 at that order (reviewer `5507222546`) |
| Claim the `1/log b` slow tail is excluded merely as "unmatched" for all amplitudes | NOT RETAINED — Rev 3 gives the z-dependent case via the switch-spectrum equation `S A = rho A` (no nonzero `A` since `rho=0.02 notin {0,-2/3}`); z-constant reduces to the unmatched rho term |
| Claim every oscillatory-envelope tail makes `V_b` change sign (categorical) | NOT RETAINED — Rev 3 excludes only sign-changing-derivative constructions; monotone-preserving oscillatory remainders remain in the open `ASYMPTOTIC_REALIZATION / NO-EXOTIC-REGIME` gate |
| State that second derivatives "enter the HJB" | NOT RETAINED — Rev 3: second/mixed partials, if used, are auxiliary regularity for differentiating (E), not HJB terms (first-order HJB in `(a,b)`) |
| Call the frozen analytic problem a second-order HJB | NOT RETAINED — corrected to the first-order regime-switching HJB (Phase B B1) |
| `git add .` / `git add -A` | NOT PERFORMED (explicit staging of allowlist paths only) |

---

## Stationary marker

```text
NOT_AUTHORIZED__DLH_5Q_THEOREM_VERIFICATION_AND_FALSIFICATION_DESIGN_ONLY__NO_HJB_KFE_GRID_RUN__NO_DOMAIN_ENDPOINT_CHOICE__NO_MODEL_FREEZE__STATIONARY_KFE_STILL_NOT_AUTHORIZED
```

---

## Scope confirmation

DLH-5Q created only the Issue #43 allowlist paths:

1. `docs/theory/DLH_5Q_PROVISIONAL_S3_TAIL_THEOREM_AND_FALSIFICATION.md`
2. `reports/dlh_5q_provisional_s3_theorem_falsification_2026_09_02/` with exactly the
   nine frozen filenames listed in Issue #43 §10.

No existing tracked file was modified. No HJB/KFE/grid/stationary experiment was run.
No analytic specification is frozen; provisional S3 is falsifiable working authority
for this task only; the Owner remains final scientific authority. The completion is a
bounded theorem-verification + falsification-design package that stops for fresh
ChatGPT review.
