# DLH-5P — Forbidden-Operation / Scope Check (Issue #42 §12) — Rev 3

DLH-5P is a **theory/design specification gate only** (bounded same-Issue revision:
rev 1 `3fde31a5…` reviewed at `5504929967`; rev 2 `4ec70095…` reviewed at
`5505175722`; rev 3 is the corrected package on the same dedicated branch). DSH
performed NONE of the following during DLH-5P (rev 1, rev 2, or rev 3); no source,
model, domain, or numerical object was touched.

| Forbidden operation | Status |
|---|---|
| Modify accepted HJB/KFE/regional source (`matlab_faithful_two_asset_ha.py`) | NOT PERFORMED (immutable; blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e` verified on fresh `origin/main`) |
| Modify utility / transfer FOC / adjustment cost / taper / prices / taxes / calibration | NOT PERFORMED (all inherited read-only) |
| Freeze or implement an analytic specification | NOT PERFORMED (S1/S2/S3 are candidate packages for Owner decision only) |
| Choose / implement R, W, W1, W2, `W_max` | NOT PERFORMED (all remain unfrozen) |
| Choose a new numerical `b_max` or new `a_max` | NOT PERFORMED |
| Extrapolate the accepted taper beyond `a_max = 10` | NOT PERFORMED |
| Run or extend HJB grids / domain / resolution | NOT PERFORMED |
| Rerun J0–J5 or previous numerical fixtures | NOT PERFORMED (no numerical run at all) |
| Run stationary KFE / nullspace / pin / density / tail / aggregates | NOT PERFORMED (stationary KFE remains NOT AUTHORIZED under Issue #27) |
| Implement a boundary KKT law | NOT PERFORMED |
| Enter regional GE / multi-province audit / network training / nominal HANK / calibration / policy / welfare / Results | NOT PERFORMED |
| Create PR / merge / close Issue / successor Issue / self-accept | NOT PERFORMED |
| Promote the finite-grid upper-`b` marginal-utility closure into an infinite-domain boundary/transversality condition | NOT PERFORMED (explicitly refused; Phase A A2, Issue #42 §5) |
| Label P-TR "proved" merely because it was assumed in DLH-5O | NOT PERFORMED (Phase D Rev 2: P-TR is an Owner-adopted admissibility primitive, not a theorem) |
| Claim the critical `m=1/2` branch is "ruled out" | NOT PERFORMED (withdrawn in Rev 2/3; the branch is UNRESOLVED/ADMISSIBLE — Phase E Rev 3) |
| Claim the critical branch reverses mean reversion (`mu_W/b >= 0`) | NOT PERFORMED (Phase E Rev 3: the demonstrated compact-interior family has `mu_W/b = -0.0025 - C/(4 chi_1) < 0`, inward) |
| `git add .` / `git add -A` | NOT PERFORMED (explicit staging of allowlist paths only) |

## Stationary marker

```text
NOT_AUTHORIZED__DLH_5P_THEORY_DESIGN_SPECIFICATION_ONLY__NO_HJB_KFE_GRID_RUN__NO_MODEL_FREEZE__NO_DOMAIN_CHOICE__STATIONARY_KFE_STILL_NOT_AUTHORIZED
```

## Scope confirmation

DLH-5P (rev 1, rev 2, and rev 3) created/modified only the Issue #42 allowlist paths:

1. `docs/design/DLH_5P_UNBOUNDED_LIQUID_HJB_ANALYTIC_SPECIFICATION_REVIEW.md`
2. `reports/dlh_5p_unbounded_liquid_hjb_specification_2026_09_02/` with exactly the
   eight frozen filenames listed in Issue #42 §11.

No existing tracked file was modified (each revision added/modified only these 9 paths).
No HJB/KFE/grid/stationary experiment was run. No analytic specification is frozen; the
Owner remains final authority for any model-defining analytic specification. The
completion is a bounded specification-review package that stops for fresh ChatGPT
review.
