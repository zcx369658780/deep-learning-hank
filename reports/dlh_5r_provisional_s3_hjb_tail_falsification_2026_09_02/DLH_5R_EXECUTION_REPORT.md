# DLH-5R — HJB-Only Provisional-S3 Liquid-Tail Numerical Falsification — Execution Report

**Issue #44.** Executes the accepted DLH-5Q falsification protocol against the
provisional S3 / p=2 tail candidate using the accepted immutable finite-grid
household HJB solver only. **HJB-ONLY.** No stationary KFE, no density, no
R/W/domain/endpoint law, no price/calibration change, no source mutation.

- Fresh `origin/main`: `d9d0d1c0b9af062968450200465d3caf50f068ff`
- Dedicated branch: `dsh/issue-44-dlh-5r-hjb-tail-falsification-2026-09-02`
- Accepted source blob (verified at runtime): `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`
- Terminal: `DLH_5R_HJB_TAIL_NUMERICAL_FALSIFICATION_INCONCLUSIVE__BOUNDARY_RESOLUTION_OR_SEMANTIC_SENSITIVITY_REMAINS` (see `DLH_5R_FALSIFICATION_DECISION.md`)

---

## 1. Execution

Fresh HJB-only runs of exactly the six mature DLH-5J variants J0-J5, frozen
economics (D0: `rho=0.02, gamma_c=2, phi=5, chi_0=0.1, chi_1=2, a_bar=1e-6`),
`a in [0,10]`, `a_max=10`, `b_lo=-2`, `db=7/19`, three b extents
b120/b140/b160 (b160 = HARD ROUTE CEILING). Deterministic cold initialization
(accepted fixture: scalar Brent labor root + `V0 = u(c_full)/rho`), fresh for
each variant, no warm-start. Accepted numerics: `delta=1000`,
`convergence_tolerance=1e-7`, `max_iterations=1000`, `drift_tolerance=1e-12`.

| Variant | grid (a×b×z) | converged | iterations | convergence_statistic | runtime (s) | floor_frac |
|---|---|---|---|---|---|---|
| J0_A77_B120 | 77×120×2 | True | 10 | 6.566175159e-08 | 25.5 | 0.0 |
| J1_A77_B140 | 77×140×2 | True | 10 | 6.566185817e-08 | 30.2 | 0.0 |
| J2_A77_B160 | 77×160×2 | True | 10 | 6.566180133e-08 | 34.4 | 0.0 |
| J3_A153_B120 | 153×120×2 | True | 10 | 2.057089432e-08 | 51.5 | 0.0 |
| J4_A153_B140 | 153×140×2 | True | 10 | 2.059847759e-08 | 60.5 | 0.0 |
| J5_A153_B160 | 153×160×2 | True | 10 | 2.059856286e-08 | 71.3 | 0.0 |

**Reproducibility against the accepted DLH-5J authority:** every run reproduces
the accepted DLH-5J variant status exactly — same iteration count (10) and same
convergence statistic to all printed digits
(`reports/dlh_5j_final_coupled_b_extent_diagnostic_2026_09_01/DLH_5J_VARIANT_STATUS.csv`),
and the J0 upper-b raw boundary maximum `4.291614197e-02` matches the accepted
DLH-5J boundary diagnostics verbatim. The fresh DLH-5R HJB solutions are
faithful reproductions of the accepted numerical solutions.

**Derivative-floor activation:** `MATLAB_DERIVATIVE_FLOOR = 1e-6` never
activated (floor count 0 / fraction 0.0 in every variant, on the full grid and
on primary evidence states). No non-finite values appear in `value`, any raw
gradient, consumption, transfer, or drifts.

**Raw-gradient provenance:** raw `V_a`/`V_b` are NOT exposed by the accepted
solver; they are reconstructed from the converged `value` with the exact
accepted forward/backward-difference semantics and b-boundary marginal-utility
closures (see `DLH_5R_RAW_GRADIENT_PROVENANCE.md`). The reconstruction is
verified two ways: (a) it reproduces the accepted DLH-5J runs bit-for-bit at the
solver level; (b) `c = V_b_raw^(-1/gamma_c)` on the dissaving branch to
~6e-10 relative error, confirming the reconstructed backward gradient is exactly
the economically-active `V_b` used by the accepted consumption FOC.

**Evidence masks applied (Issue #44 §6):** primary a-mask = aligned a77 nodes
`j=1..74` and a153 every-second nodes `j=2,4,..,148` (excludes `a=0`, top two
coarse a-layers near `a=10`); both z states included; top two b nodes excluded in
every variant; W1 `20<=b<=35`, W2 `35<b<=40`, W3 `42<=b<=48` (b140/b160),
W4 `50<=b<=55` (b160, **descriptive only**). W3/W4 on b120 and W4 on b140 are
`INSUFFICIENT_WINDOW_NODES` by construction (no nodes in those extents) and are
not used. All evidence windows carry ≥13 b nodes and 148 primary (a,z) pairs.

---

## 2. Pre-registered aligned tail observables (median over primary states)

Raw upwind pair (V_a = forward raw if mu_a≥0 else backward raw; V_b likewise).
On the tail the accepted solution is dissaving (`r_b < rho`), so `V_b` is the
backward raw gradient; `R_hat = V_a_raw/V_b_raw`, `Q_hat = b^2*V_b_raw`.

| Window | slope(log vb vs log b) | Q_hat | c/b | \|R\| | R/√b | chi/b | mu_W/b |
|---|---|---|---|---|---|---|---|
| W1 (20–35) | −0.559 | 314.5–314.9 | 0.05635–0.05639 | 1.109–1.114 | 0.211–0.212 | 0.00076–0.00079 | −0.00997…−0.01004 |
| W2 (35–40) | −0.681 | 484.8–485.4 | 0.04539–0.04542 | 1.110–1.115 | 0.181–0.182 | 0.00056–0.00058 | −0.00828…−0.00833 |
| W3 (42–48) | −0.758 | 609.7–610.4 | 0.04048–0.04050 | 1.111–1.115 | 0.166–0.167 | 0.00047–0.00049 | −0.00742…−0.00746 |
| W4 (50–55, descriptive) | −0.832 | 735.1–735.9 | 0.03686–0.03688 | 1.112–1.116 | 0.153–0.154 | 0.00041–0.00042 | −0.00674…−0.00677 |

Ranges span a77 and a153 at the same extent; within each variant the six values
are identical to 4+ decimals. Provisional S3/p=2 predictions: `slope = -2`,
`Q_hat -> K* = 3265.3061224489797`, `c/b -> 0.0175`, `mu_W/b -> -0.0025`,
`chi/b -> 0`, `R = O(1)`.

**Verdict on the p=2 signature:** the numerical tail does **not** realize the
p=2 scaling at any authorized window:
- raw-`V_b` log-log slope ≈ **−0.56 → −0.83** (W1→W4), far outside the support
  band `[-2.15,-1.85]` and the falsification band `[-2.25,-1.75]`;
- `Q_hat` is **growing** ≈ 315 → 736, not plateauing at `K* = 3265.3`
  (5–10× below `K*` at the accessible extents);
- `c/b` ≈ 0.0369–0.0564 (2–3× above `0.0175`), decreasing but not converging
  to `0.0175` within the ceiling;
- `mu_W/b` ≈ −0.0067…−0.010 (negative, currently 2.7–4× more negative than −0.0025, **trending toward** −0.0025).

All of these are **accessible finite-window effective values**; every
p=2-facing observable moves **monotonically in the p=2 target direction** over
W1 → W4 (see the trend table in `DLH_5R_FALSIFICATION_DECISION.md` §2): slope
−0.559 → −0.832 (toward −2), `Q_hat` 315 → 736 (toward `K*`), `c/b`
0.0564 → 0.0369 (toward 0.0175), `|R|/√b` 0.212 → 0.154 (toward 0), `chi/b`
0.00079 → 0.00040 (toward 0), `mu_W/b` −0.0100 → −0.0067 (**toward** −0.0025).
The eventual asymptotic class is **unresolved** at the authorized b160 hard
ceiling.

**S3 derivative-control consistency (R/chi) holds:** `|R| ≈ 1.11` is bounded
`O(1)` (pinned near `1 + chi_0 = 1.1`, the transfer-FOC inaction boundary),
`R/√b` decreases 0.212 → 0.154, `chi/b` decreases 0.00079 → 0.00041 toward 0.
**No critical `R ~ sqrt(b)` / positive-`chi/b` plateau signature is observed.**

**Cross-extent stability (b120 vs b140 vs b160, aligned common nodes):**
relative differences are `0.000000` for Q_hat, c/b, slope, R/√b, mu_W/b and
`~1e-5` for chi/b — i.e. the interior tail observables are b-extent independent
to <0.001%.

**Cross-resolution stability (a77 vs every-second a153, aligned nodes):**
relative differences Q_hat `0.0014`, c/b `0.0007`, slope `0.0012`, R/√b
`0.0043`, mu_W/b `0.007`, chi/b `0.032` (chi/b is O(1e-4), so the relative
difference of a near-zero quantity) — all < 4% and < 0.5% for the material
observables.

**z-dependence (b160, primary):** `Q_hat` z=1.3 vs z=0.8 differs by ~1.3%
(315.3 vs 319.5 in W1; 609.4 vs 615.3 in W3), `c/b` by ~0.6%, `|R|` by ~0.02%.
Mild z-variation; both z states are far below `K*`.

**a=0 (descriptive, excluded from primary):** `Q_hat ≈ 381–872`, `c/b ≈
0.034–0.051` — same non-p2 pattern, reported separately per Issue #44 §6.

---

## 3. Falsification screening (Issue #44 §10)

Evidence is stable across b140 **and** b160 **and** a77 **and** a153, with zero
floor activation, all variants converged, windows valid, and provenance
verified. However, no pre-registered falsification direction is satisfied: a
**stable non-p2 asymptotic plateau/exponent is required**, and none is observed.

- **A (critical `R~√b` + positive-`chi/b` plateau) — NOT SATISFIED.** `|R|` is
  flat ≈1.11; `R/√b` decreases with b; `chi/b -> 0`. The out-of-S3 m=1/2
  exclusion-cost scenario is not the numerical outcome.
- **B (Q_hat stable plateau >20% from K\*) — NOT SATISFIED.** `Q_hat` is
  `315 -> 485 -> 610 -> 736`, **growing, not a plateau** (>80% below `K*`).
  Cross-b equality at the same physical nodes shows truncation independence, not
  an asymptotic plateau.
- **C (c/b stable value >20% from 0.0175) — NOT SATISFIED.** `c/b` is
  `0.0564 -> 0.0454 -> 0.0405 -> 0.0369`, **decreasing, not a plateau**
  (2–3× above 0.0175).
- **D (raw V_b exponent stabilized outside [−2.25,−1.75]) — NOT SATISFIED /
  PRE-ASYMPTOTIC.** Slope `-0.559 -> -0.681 -> -0.758 -> -0.832` is far outside
  the band but **still materially b-dependent**, monotonically becoming more
  negative as b rises. Cross-extent equality of W1/W2/W3 across b120/b140/b160
  shows the common windows are not contaminated by the farther artificial upper
  boundary; it does **not** establish that the local effective exponent has
  converged as b → ∞.
- **E (bounded R but stable non-p2 coefficient/scaling) — NOT SATISFIED.**
  Bounded `R = O(1)` is supported; a **stable non-p2 asymptotic
  coefficient/scaling is not** — the scaling observables continue moving with b.

**Inconclusive screen (Issue #44 §11):** the material remaining limitation is
**finite truncation / asymptotic reach at the authorized b160 hard ceiling**.
It is **not** a claim of cross-extent instability: common-window values are
highly stable (cross-b < 0.001%, cross-a < 0.5% material), floor (0),
convergence (all converged), raw-gradient provenance (verified exactly), and
window-node sufficiency (all evidence windows valid) are all clean.

**Conclusion:** the accepted numerical HJB solution does **not** support the
p=2 coefficient/scaling at the accessible range (support screen fails:
effective raw-`V_b` slope ≈ −0.56…−0.83, `Q_hat` ≈ 315…736 growing below `K*`,
`c/b` ≈ 0.037…0.056 above 0.0175, `mu_W/b` more negative than −0.0025), while
the S3 derivative-control signature is numerically compatible
(`R = O(1)`, `R/√b` falls, `chi/b` falls) and no critical `R~√b` signature is
observed. Because every p=2-facing observable is still **trending toward its
conditional target** over W1 → W4 and the b160 hard ceiling prevents testing
farther, the eventual asymptotic class is unresolved: neither Outcome A nor
Outcome B is supported by the pre-registered screens. **Terminal C
(INCONCLUSIVE).** See `DLH_5R_FALSIFICATION_DECISION.md` for the full decision
and limitations.

---

## 4. Deliverables produced

- `configs/dlh_5r_provisional_s3_hjb_tail_falsification.toml`
- `scripts/run_dlh_5r_provisional_s3_hjb_tail_falsification.py`
- `reports/dlh_5r_provisional_s3_hjb_tail_falsification_2026_09_02/`:
  - `DLH_5R_EXECUTION_REPORT.md` (this file)
  - `DLH_5R_EXECUTION_MANIFEST.md`
  - `DLH_5R_RAW_GRADIENT_PROVENANCE.md`
  - `DLH_5R_VARIANT_RUN_SUMMARY.csv`
  - `DLH_5R_ALIGNED_TAIL_OBSERVABLES.csv`
  - `DLH_5R_SCALING_AND_PLATEAU_DIAGNOSTICS.csv`
  - `DLH_5R_FALSIFICATION_DECISION.md`
  - `DLH_5R_FORBIDDEN_OPERATION_CHECK.md`

Temporary execution arrays (`_decision_inputs.json`) remain outside Git staging.
