# DLH-5R — Falsification Decision

**Issue #44, step 12 (bounded Rev 2 per fresh review `5509806834`).** Exact
single terminal (exactly one, used verbatim):

```
DLH_5R_HJB_TAIL_NUMERICAL_FALSIFICATION_INCONCLUSIVE__BOUNDARY_RESOLUTION_OR_SEMANTIC_SENSITIVITY_REMAINS
```

No terminal in this Issue proves the analytic theorem. The decision below is
numerical-falsification evidence about the **promotion** of the provisional S3 /
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
| mu_W/b negative, toward −0.0025 | yes | negative, and **trending toward** −0.0025 (−0.0100 → −0.0067), not yet reached at accessible b | PARTIAL/FAIL |
| b140/b160 & a77/a153 discrepancies ≤10% | ≤10% | <0.001% (b-extent), <0.5% (a-res, material) | PASS |

**Support screen: FAILS** on the three p=2 scaling observables (slope, Q_hat,
c/b) at the accessible range. Per Issue #44 §9, failure of the support screen is
**not** automatic falsification — the falsification screen decides.

## 2. Pre-registered falsification screen (Issue #44 §10)

Strong falsification-direction evidence must be stable across at least
b140 **and** b160 **and** a77 **and** a153 and not attributable to
boundary/floor/non-convergence artifacts. A stable non-p2 *asymptotic*
plateau/exponent is required; **no falsification direction is satisfied.**

| Direction | Criterion | Observed | Verdict |
|---|---|---|---|
| A | R grows with b **and** R/√b → nonzero plateau **and** chi/b → positive plateau | \|R\| flat ≈1.11; R/√b decreases 0.212→0.154; chi/b → 0 | **NOT SATISFIED** |
| B | Q_hat **stable plateau** >20% from K* and b140/b160 disc <10% | Q_hat 315 → 485 → 610 → 736 — **growing, not a plateau** (>80% below K*; b-extent disc 0.000000 only shows truncation independence, not an asymptotic plateau) | **NOT SATISFIED** |
| C | c/b **stable value** >20% from 0.0175 and b140/b160 disc <10% | c/b 0.0564 → 0.0454 → 0.0405 → 0.0369 — **decreasing, not a plateau** (2–3× above 0.0175; b-extent disc 0.000000 only shows truncation independence) | **NOT SATISFIED** |
| D | raw V_b exponent **stabilized** outside [−2.25,−1.75] as b increases | slope −0.559 → −0.681 → −0.758 → −0.832 — still materially b-dependent, monotonically more negative (pre-asymptotic); far outside the band, but not stabilized | **NOT SATISFIED / PRE-ASYMPTOTIC** |
| E | bounded R **and stable non-p2 asymptotic coefficient/scaling** | bounded R = YES (\|R\|≈1.11, R/√b falls, chi/b falls); **stable non-p2 coefficient/scaling = NO** (all scaling observables still moving with b) | **NOT SATISFIED** |

Artifact exclusions (all satisfied): derivative floor never activated; all six
variants converged per the accepted criterion (stat < 1e-7, reproducing accepted
DLH-5J exactly); all evidence windows are interior (W1/W2 far from b_max, top
two b nodes excluded, W4 descriptive only); raw-gradient provenance verified
exactly; cross-extent and cross-resolution stability < 1%. Cross-b equality at
the same physical b nodes establishes truncation independence of those interior
values — it does **not** establish that the local effective exponent/coefficient
has converged as b → ∞.

**No falsification direction holds.** In particular, every principal
p=2-facing observable moves **monotonically in the p=2 target direction** over
W1 → W4:

| Observable | W1 → W4 | p=2 target | Movement |
|---|---|---|---|
| slope | −0.559 → −0.681 → −0.758 → −0.832 | −2 | toward −2 |
| Q_hat | 315 → 485 → 610 → 736 | 3265.3 | toward K* |
| c/b | 0.0564 → 0.0454 → 0.0405 → 0.0369 | 0.0175 | toward 0.0175 |
| \|R\|/√b | 0.212 → 0.182 → 0.166 → 0.154 | 0 | toward 0 |
| chi/b | 0.00079 → 0.00058 → 0.00049 → 0.00040 | 0 | toward 0 |
| mu_W/b | −0.0100 → −0.0083 → −0.0074 → −0.0067 | −0.0025 | toward −0.0025 |

This pattern is compatible with a long pre-asymptotic transition toward p=2; it
is also compatible with some other eventual asymptotic regime. The authorized
b160 hard ceiling cannot discriminate those possibilities.

## 3. Inconclusive screen (Issue #44 §11)

The **remaining inconclusive limitation is finite truncation / asymptotic reach
at the authorized b160 hard ceiling** — the p=2-facing observables are still
trending toward their conditional targets and the experiment cannot go farther
beyond b160. This is **not** a claim that common-window values are materially
unstable across the existing b extents: cross-b stability is < 0.001% and
cross-a stability (material) is < 0.5%, and none of the following are material
causes of the inconclusiveness:

- b extent: cross-b relative diff 0.000000 (Q_hat, c/b, slope, R/√b, mu_W/b) — highly stable → not a material cause.
- a resolution: material cross-a diff < 0.5% — highly stable → not a material cause.
- top boundary: non-p2 effective slope present in interior W1, consistent through W3/W4; top two b nodes excluded → not a material cause.
- derivative-floor activation: 0 states → not a material cause.
- non-convergence: all converged → not a material cause.
- raw-gradient provenance ambiguity: none (verified) → not a material cause.
- insufficient window nodes: W1/W2/W3 valid everywhere applicable; W3/W4 on b120 and W4 on b140 structurally INSUFFICIENT by design and unused → not a material cause.

The material limitation is solely **asymptotic reach**: the effective exponent
and the coefficient/scaling observables are still evolving at b ≤ 56.6, and
b160 is the hard route ceiling.

## 4. Decision and meaning

**Terminal C — INCONCLUSIVE.** The evidence supports the following three
separate statements, which must not be conflated:

1. **S3 derivative-control signature — numerically compatible/supported over the
   accessible range.** `R = O(1)` (≈1.11, pinned near `1+chi_0 = 1.1`),
   `|R|/√b` falls, and `chi/b` falls toward 0. This is consistent with the
   S3 derivative-control family.
2. **p=2 coefficient/scaling — NOT yet supported at the accessible b.** At every
   authorized window, raw-`V_b` slope ≈ −0.56…−0.83 (far outside the p=2 band
   `[-2.25,-1.75]` and the support band `[-2.15,-1.85]`), `Q_hat` ≈ 315…736
   (well below `K*=3265.3`, no plateau), `c/b` ≈ 0.037…0.056 (2–3× above
   0.0175), `mu_W/b` ≈ −0.0067…−0.010 (more negative than −0.0025). The support
   screen **fails** at the accessible range.
3. **Eventual asymptotic p=2 — NOT falsified.** The failure of the p=2 support
   screen at accessible b is **not** an asymptotic falsification, because all
   p=2-facing observables are still trending monotonically toward their
   conditional targets over W1 → W4 and the authorized b160 hard ceiling
   prevents testing farther.

Therefore neither Outcome A (support) nor Outcome B (falsification of the
promotion) is supported by the pre-registered screens as written. The
scientifically defensible terminal is **C**,
`INCONCLUSIVE__BOUNDARY_RESOLUTION_OR_SEMANTIC_SENSITIVITY_REMAINS`, where the
suffix is interpreted as the **finite-truncation / asymptotic-reach limitation**
imposed by the authorized b160 hard ceiling — not as instability of common-window
values across the existing b extents (which are highly stable).

S3 **in full** is not claimed to be numerically verified: `V_inf = 0` is not
established by this finite experiment.

## 5. Explicit limitations (honest scope)

1. **Finite-extent statement only.** The effective raw-`V_b` exponent is still
   evolving within the authorized domain (−0.559 in W1 → −0.832 in W4); the
   asymptotic regime is not reached at b ≤ 56.6, and b160 is the hard route
   ceiling. Whether a longer extent would approach p=2 (or some other regime) is
   beyond the authorized experiment and is not resolved here. A larger-domain
   experiment would require a new Owner decision and successor authority.
2. **The accessible finite-window regime is non-p2 and pre-asymptotic; the
   eventual asymptotic class remains unresolved at the authorized b160 hard
   ceiling.** The accepted DLH-5Q `NO-EXOTIC-REGIME` / `ASYMPTOTIC_REALIZATION`
   gate remains open; this experiment does not select a specific exotic family.
3. **`R` is pinned near the transfer inaction boundary** (`R ≈ 1+chi_0 = 1.1`),
   which is an S3-consistent O(1) result, not evidence about the p=2 coefficient
   itself.
4. This decision reflects the accepted numerical solver's converged solutions on
   the frozen grids; it is not a theorem, not an Owner acceptance, and it does
   not freeze or redefine any model.
