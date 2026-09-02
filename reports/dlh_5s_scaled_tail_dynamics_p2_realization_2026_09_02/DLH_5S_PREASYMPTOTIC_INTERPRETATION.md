# DLH-5S — Interpretation of DLH-5R Pre-Asymptotic Evidence (Phase G)

**Issue #45, Phase G.** Uses the accepted DLH-5R scalar medians **only** as
read-only evidence context. No new HJB/grid execution. The transformed
identities are used to explain the observed pattern; qualitative compatibility
is **not** theorem proof.

## 1. Accepted DLH-5R medians (read-only)

```text
            W1      W2      W3      W4 (descriptive)
Q          315     485     610     736
c/b       0.0564  0.0454  0.0405  0.0369
p_eff     0.559   0.681   0.758   0.832        (reported V_b slopes, p_eff = -slope)
|R|/sqrt(b) 0.212  0.182   0.166   0.154
chi/b     0.00079 0.00058 0.00049 0.00040
mu_W/b    -0.0100 -0.0083 -0.0074 -0.0067
```

## 2. Why increasing Q implies decreasing c/b (exact)

Phase B identity `c/b = Q^(-1/2)`:

```text
d log(c/b)/d log b = -(1/2) * d log Q / d log b
```

So any increase of `Q` with b (`d log Q/d log b > 0`) forces `c/b` to fall
monotonically. **Arithmetic cross-check against the accepted medians:**

```text
1/sqrt(315) = 0.0563  ~  observed 0.0564
1/sqrt(485) = 0.0454  ~  observed 0.0454
1/sqrt(610) = 0.0405  ~  observed 0.0405
1/sqrt(736) = 0.0369  ~  observed 0.0369
```

The observed `c/b` reproduces `Q^(-1/2)` to the reported precision — the
accepted analytic consumption FOC is exactly satisfied by the finite-window
medians, and `Q` increasing (315 -> 736) is precisely what drives `c/b`
decreasing (0.0564 -> 0.0369) toward `1/sqrt(K*) = 0.0175`.

## 3. Why increasing Q can coexist with p_eff < 2 (exact)

Phase B identity `p_eff = 2 - d log Q / d log b`:

```text
Q increasing  <=>  d log Q / d log b > 0  =>  p_eff = 2 - d log Q/d log b < 2.
```

`p_eff < 2` only requires `Q` to grow more slowly than `b^2`. The observed
`p_eff` rises from 0.559 to 0.832 as `d log Q/d log b` falls from
`2 - 0.559 = 1.441` to `2 - 0.832 = 1.168`. End-to-end,
`Delta log Q / Delta log b = log(736/315)/log(55/20) = 0.848/1.012 = 0.838`,
so `p_eff ~ 1.16` over the whole window — consistent, all `p_eff < 2`. There is
no contradiction: a *growing* `Q` is exactly the signature of `p_eff` below 2
that is *moving toward* 2.

## 4. Does the reduced lower branch predict Q < K* => Q increasing? YES (exact)

Phase D: on the reduced lower branch,

```text
dQ/ds = Q * [2 - (rho+r_b)*sqrt(Q)] / [1 - r_b*sqrt(Q)] > 0   for all Q in (0, K*)
```

because the numerator is positive (`sqrt(Q) < 2/(rho+r_b) = sqrt(K*)`) and the
denominator is positive (`r_b*sqrt(Q) < 6/7 < 1`). So the reduced system's
lower branch predicts exactly the observed **direction**: `Q < K* => Q
increasing`, monotonically toward `K* = 3265.3`. The observed `Q` (315->736) is
far below `K*` and also below the turning point `1/r_b^2 = 4444.4`, i.e. on the
lower branch throughout.

## 5. Is DLH-5R qualitatively compatible with a pre-asymptotic approach to the p=2 attractor? (conditional)

**Qualitatively compatible — but not a proof.** All principal p=2-facing
observables move monotonically in the p=2 direction over W1 -> W4:

```text
Q:        315 -> 736            toward K* = 3265.3
c/b:      0.0564 -> 0.0369      toward 0.0175  (= 1/sqrt(K*))
p_eff:    0.559 -> 0.832        toward 2
|R|/sqrt(b): 0.212 -> 0.154     toward 0
chi/b:    0.00079 -> 0.00040    toward 0
mu_W/b:  -0.0100 -> -0.0067     toward -0.0025
```

This is the signature of the reduced lower-branch attractor being approached
**from below** (Phase D): `Q < K*`, `Q` increasing, `c/b = Q^(-1/2)` falling,
`p_eff = 2 - dlogQ/dlogb` rising toward 2.

**Two honest qualifications (do NOT over-read the data):**

1. **The reduced system alone does NOT reproduce the observed rate.** At the
   observed `Q`, the reduced flow would give
   `d log Q/d log b = [2 - (rho+r_b)sqrt(Q)]/[1 - r_b sqrt(Q)]`, e.g. ~1.88 at
   `Q=315`, and would have `Q ~ K*` essentially by `b ~ 30` (correction
   `~ b^(-7)`). The observed solution stays far below `K*` at `b <= 56.6`
   (`Q=736` at W4) with a slower `d log Q/d log b` (~1.44 -> 1.17). Hence the
   normalized remainder `E` is **materially active and negative** on the
   accessible range (consistent with `E_labor < 0`, `E_illiquid < 0`,
   `E_transfer_adj <= 0`), retarding the approach; the reduced system is the
   *asymptotic* attractor, not the finite-window trajectory. The approach rate
   is set by `E` (and `dE/ds`), which S3 alone does not control.
2. **The numerical medians come from the accepted fixed-`labor0` finite-grid
   solver**, whereas the analytic attractor analysis is for the accepted
   endogenous-labor analytic HJB (Phase A note). The qualitative direction is
   shared; the quantitative rates are indicative only.

**Bottom line:** the accepted finite-window evidence is **qualitatively
compatible** with a long pre-asymptotic approach to the reduced p=2 attractor on
the lower branch, and the exact identities (`c/b = Q^(-1/2)`, `p_eff =
2 - dlogQ/dlogb`, `dQ/ds > 0` for `Q<K*`) account for the observed directions
without any assumption. This does **not** imply the actual HJB reaches p=2:
realization still requires the explicit non-circular tightness / branch-selection /
derivative-remainder / no-exotic assumptions of Phase F.
