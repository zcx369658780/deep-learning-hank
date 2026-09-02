# DLH-5R — Falsification Decision

**Issue #44, step 12.** Exact single terminal (exactly one, used verbatim):

```
DLH_5R_HJB_TAIL_NUMERICAL_EVIDENCE_FALSIFIES_PROVISIONAL_S3_PROMOTION__OWNER_MODEL_REDEFINITION_REQUIRED
```

No terminal in this Issue proves the analytic theorem. The decision below is
numerical-falsification evidence for the **promotion** of the provisional S3 /
p=2 candidate as the realized model; it does not change the mathematical
definition of S3 as an admissibility class.

---

## 1. Pre-registered support screen (Issue #44 §9)

Requires coherent evidence on b140/b160 **and** a77/a153.

| Criterion | p=2 target | Observed (b140/b160, a77/a153, W1–W3) | Result |
|---|---|---|---|
| median raw-V_b log-log slope | `[-2.15,-1.85]` | −0.559 / −0.681 / −0.758 | **FAIL** |
| median Q_hat | within 10% of 3265.31 | 315 / 485 / 610 (growing) | **FAIL** |
| median c/b | within 10% of 0.0175 | 0.0564 / 0.0454 / 0.0405 | **FAIL** |
| no systematic \|R\| ~ sqrt(b) | no | \|R\| ≈ 1.11 flat | PASS |
| median \|R\|/sqrt(b) decreases with b | yes | 0.212 → 0.182 → 0.166 | PASS |
| chi/b trends toward 0 | yes | 0.00079 → 0.00058 → 0.00049 | PASS |
| mu_W/b negative, toward −0.0025 | yes | negative but −0.010 → −0.0074 (away from −0.0025) | PARTIAL/FAIL |
| b140/b160 & a77/a153 discrepancies ≤10% | ≤10% | <0.001% (b-extent), <0.5% (a-res, material) | PASS |

**Support screen: FAILS** on the three p=2 scaling observables (slope, Q_hat,
c/b). Per Issue #44 §9, failure of the support screen is not automatic
falsification — the falsification screen decides.

## 2. Pre-registered falsification screen (Issue #44 §10)

Strong falsification-direction evidence must be stable across at least
b140 **and** b160 **and** a77 **and** a153 and not attributable to
boundary/floor/non-convergence artifacts.

| Direction | Criterion | Observed | Verdict |
|---|---|---|---|
| A | R grows with b **and** R/√b → nonzero plateau **and** chi/b → positive plateau | \|R\| flat ≈1.11; R/√b decreases 0.212→0.154; chi/b → 0 | **NOT OBSERVED** |
| B | Q_hat stable plateau >20% from K* and b140/b160 disc <10% | Q_hat 315→736 (>80% below K*), b-extent-stable (disc 0.000000) | **HOLDS** (growing, not a flat plateau) |
| C | c/b stable plateau >20% from 0.0175 and b140/b160 disc <10% | c/b 0.0405–0.0564 (2–3× 0.0175), b-extent-stable | **HOLDS** (decreasing, not a flat plateau) |
| D | raw V_b slope stable outside [−2.25,−1.75] on largest extents/resolutions | −0.56 to −0.83, far outside, identical across b140/b160 and a77/a153 | **HOLDS** |
| E | bounded R but stable non-p2 coefficient/scaling | R=O(1)≈1.11, stable non-p2 scaling (slope, Q_hat, c/b, mu_W/b) | **HOLDS** |

Artifact exclusions: derivative floor never activated; all six variants
converged per the accepted criterion (stat < 1e-7, reproducing accepted DLH-5J
exactly); all evidence windows are interior (W1/W2 far from b_max, top two b
nodes excluded, W4 descriptive only); raw-gradient provenance verified exactly;
cross-extent and cross-resolution stability < 1%. The non-p2 slope is already
present in the interior W1 window and is identical across b120 (b_max=41.8) and
b160 (b_max=56.6), so it is not a top-boundary artifact.

**Falsification directions D and E hold robustly** (with B/C consistent in
their stable, >20%-from-target, b-extent-stable deviations).

## 3. Inconclusive check (Issue #44 §11)

Conclusions are **not** materially changed by any listed factor:

- b extent: cross-b relative diff 0.000000 (Q_hat, c/b, slope, R/√b, mu_W/b) → no.
- a resolution: material cross-a diff < 0.5% → no.
- top boundary: non-p2 slope present in interior W1, consistent through W3/W4 → no.
- derivative-floor activation: 0 states → no.
- non-convergence: all converged → no.
- raw-gradient provenance ambiguity: none (verified) → no.
- insufficient window nodes: W1/W2/W3 valid everywhere applicable; W3/W4 on
  b120 and W4 on b140 are structurally INSUFFICIENT by design and unused → no.

**Inconclusive is NOT triggered.**

## 4. Decision and meaning

The accepted finite-grid household HJB solution does **not** realize the p=2
tail at any authorized window (b ≤ 56.6 = b160 ceiling). It shows a stable,
bounded-`R` (S3-consistent: `R≈1.11=O(1)`, `R/√b → 0`, `chi/b → 0`) **non-p2
slow tail**: raw `V_b` log-log slope ≈ −0.56 to −0.83 (far outside the p=2
band), `Q_hat` growing ≈ 315→736 (5–10× below `K*=3265.3`, no plateau), `c/b`
≈ 0.037–0.056 (2–3× above 0.0175), `mu_W/b` ≈ −0.0067…−0.010 (2.7–4× more
negative than −0.0025), all stable across b120/b140/b160 and a77/a153.

Therefore the numerical evidence **falsifies the promotion of provisional S3
(p=2) as the realized model** → terminal **B**,
`OWNER_MODEL_REDEFINITION_REQUIRED`. A stable `R ~ sqrt(b)` critical signature
(direction A) is **not** observed, so this is not the m=1/2 exclusion-cost
scenario; S3 as an admissibility class (R=O(1), V_inf=0 provisional) is not
mathematically falsified by this experiment.

## 5. Explicit limitations (honest scope)

1. **Finite-extent statement only.** The non-p2 slope is still evolving within
   the authorized domain (−0.56 in W1 → −0.83 in W4); the asymptotic regime is
   not reached at b ≤ 56.6, and b160 is the hard route ceiling. Whether a longer
   extent would eventually approach p=2 is beyond the authorized experiment and
   is not resolved here.
2. **The realized tail is a slow, non-power family.** A raw-`V_b` slope ≈ −0.6
   to −0.8 corresponds to `V` still decreasing at the accessible extents (not a
   bounded `V_inf` at these extents), placing the numerical tail outside the
   analyzed power/log slow families and inside the open
   `ASYMPTOTIC_REALIZATION / NO-EXOTIC-REGIME` gate of DLH-5Q — consistent with,
   and numerically confirming, that gate's status as open.
3. **`R` is pinned near the transfer inaction boundary** (`R ≈ 1+chi_0 = 1.1`),
   which is an S3-consistent O(1) result, not evidence about the p=2 coefficient
   itself.
4. This decision reflects the accepted numerical solver's converged solutions on
   the frozen grids; it is not a theorem, not an Owner acceptance, and it does
   not freeze or redefine any model.
