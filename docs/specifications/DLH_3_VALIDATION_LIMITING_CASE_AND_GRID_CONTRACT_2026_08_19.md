# DLH-3 — Validation Limiting-Case and Grid Contract (DLH-3A)

- Date: 2026-08-19
- Author: DSH (bounded Builder)
- Authority: GitHub Issue #10 — DLH-3A
- Status: **SPECIFICATION ONLY — CANDIDATE for GPT/Owner review.** No implementation, no execution.

> This contract fixes: (a) the relationship to the accepted Tier-0 Q200 numerical standard, (b) the practical future development/reference grid hierarchy (all `VALIDATION_FIXTURE_NOT_CALIBRATION`), and (c) the required limiting cases for the future DLH-3B/3C/3D/3E subgates. It creates no numerical result.

## 1. Relationship to the accepted Tier-0 Q200 standard (Issue #10 §6)

- Accepted Tier-0 reference: Q200 on `[0,200]` (1265 points, spacing `12.5/79`) with `K_Q = 28.010252116571742`; accepted hierarchy C200 (317)/F200 (633)/Q200 (1265) with `d_C_F = 0.00495219029457629`, `d_F_Q = 0.00248694289348661`; `54/54` regression suite; reproducibility diffs `0.0`.
- **Q200 `[0,200]` remains the accepted Tier-0 real HA/Aiyagari validation/reference numerical standard.** It may be used as regression/reference provenance.
- **Non-inheritance:** changing the economic meaning of the asset from productive capital to a liquid financial asset (DLH-3) means Tier-0 domain adequacy is **not automatically inherited**. Final HANK domain/grid adequacy must be re-established in DLH-3E.
- DLH-3A performs no grid run and creates no new numerical result.

## 2. Practical future development / reference hierarchy (recommendation, `VALIDATION_FIXTURE_NOT_CALIBRATION`)

Recommended hierarchy for the future DLH-3 implementation (to be authorized by a separate Issue):

1. **Development grid (lower cost):** a small liquid-asset grid (e.g., ~101–201 points on a HANK domain to be re-established) for rapid iteration, used **only** under an explicit regression contract to a HANK reference grid.
2. **HANK reference grid:** a high-accuracy HANK grid (to be defined and validated in DLH-3E, mirroring the Tier-0 C/F/Q methodology) that anchors the regression contract.
3. **Regression contract:** every development-grid equilibrium must reproduce the reference-grid equilibrium objects (e.g., K*, C, N, distribution moments, residuals) within a frozen tolerance before any claim of HANK adequacy.

Every grid/fixture label must be `VALIDATION_FIXTURE_NOT_CALIBRATION`. A starting numerical convention is **not** proven HANK domain adequacy.

## 3. Required limiting cases for future subgates

### 3.1 DLH-3B (steady-state structural kernel) — future limiting cases
- Zero-inflation, zero-shock steady state: `π* = 0`, `i* = r* = r̄`, `mc* = 1/μ`.
- Endogenous labor consistency: `N* = ∫ z n* dg` with labor FOC; no-labor-disutility limit (`χ → 0`) degeneracy documented.
- Bond-market clearing: `A* = B`.
- All §5 residuals of the equation contract at steady state within frozen tolerances.
- **A DLH-3B PASS alone must NOT be called full dynamic genuine-HANK validation.**

### 3.2 DLH-3C (time-dependent household/KFE response) — future required cases
Under externally prescribed small paths for household-relevant aggregate prices/incomes (w_t, r_t, tr_t, Π_t), without closing full NK GE and without a structural monetary shock:
- **zero path ⇒ steady state:** with a constant path equal to the steady-state values, backward HJB + forward KFE reproduce the steady state;
- **amplitude → 0 ⇒ response → 0:** perturbation amplitude scaling to zero drives the response to zero;
- **mass conservation / non-negativity:** `∫g = 1` and `g ≥ 0` along the path;
- **boundary feasibility:** no-outward-drift conditions and consumption positivity along the path;
- **terminal / horizon robustness:** results stable in the (long) horizon; terminal condition documented;
- **deterministic reproducibility:** repeat differences ≤ frozen tolerance.

### 3.3 DLH-3D (NK GE + first monetary innovation) — future required cases
- Close the full household-distribution-firm-inflation-policy loop with one small deterministic monetary-policy innovation.
- Report all §5 residuals; the Taylor rule, Fisher, NKPC and markets must be computed, not labeled.
- Only an independent 3D review may first qualify for `MINIMAL_GENUINE_SINGLE_REGION_HANK_DYNAMIC_VALIDATED` (validation fixture only — not calibration, Results, or policy evidence).

### 3.4 DLH-3E (HANK numerical robustness freeze) — future required assessments
- **Asset-domain adequacy under the new HANK economy** (re-establish, do not inherit);
- **asset-grid refinement** (HANK C/F/Q-style sequence);
- **aggregate-time discretization** (separate from asset-grid convergence — never conflate the two);
- **transition horizon / terminal condition**;
- **deterministic reproducibility.**

## 4. Explicit no-actions (DLH-3A)

- No grid run; no new numerical result; no implementation; no pytest for scientific purposes; no transition/shock/IRF; no calibration/regression; no empirical data; no neural/RL; no GPU; no regional/W^L/W^K/W^G; no multi-region code; no Results/policy/novelty claims; no legacy Matlab / old Python reference / private Zotero access; no governance mutation; no PR/merge/Issue close/successor/self-accept.
