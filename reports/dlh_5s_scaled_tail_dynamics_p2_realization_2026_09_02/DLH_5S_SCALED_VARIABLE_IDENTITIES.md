# DLH-5S — Scaled-Tail Variables and Exact Kinematic Identities (Phase B)

**Issue #45, Phase B.** Introduces and audits the scaled variables and derives
the exact kinematic identities. All statements here are mechanical consequences
of the definitions (given the accepted S1 regularity `V_b>0`, `V<0` and the
accepted analytic consumption FOC).

## 1. Definitions

```text
H(b,a,z) = -b * V(b,a,z)         > 0   (since V < 0)
Q(b,a,z) = b^2 * V_b(b,a,z)      > 0   (since V_b > 0)
s        = log(b)                (b > 0 tail)
m(b,a,z) = Q/H = b*V_b/(-V)
```

`H` is the scaled value (positive), `Q` is the scaled marginal value of liquid
wealth (the "b²·V_b" observable of DLH-5R), `s = log b` is the tail coordinate.

## 2. Exact kinematic identity — dH/ds = H − Q

For fixed `(a,z)` wherever differentiability permits:

```text
dH/ds = b * dH/db
      = b * d(-b*V)/db
      = b * (-V - b*V_b)
      = -b*V - b^2*V_b
      = H - Q
```

**Exact.** No asymptotic assumption. This is the driving identity of the whole
reduced-system analysis: `H` grows in `s` when `Q < H`, decays when `Q > H`,
and is stationary exactly when `H = Q`.

Equivalent growth form via `m = Q/H`:

```text
dH/ds = H * (1 - m),     i.e.   d log(H)/ds = 1 - m = 1 - Q/H.
```

So `m = Q/H` measures how much of the H-growth is "eaten" by the marginal
scaling `Q`. At the p=2 candidate `m -> 1`, `dH/ds -> 0`.

## 3. Consumption ratio under the accepted analytic FOC

`c = V_b^(-1/gamma_c) = V_b^(-1/2)` (gamma_c=2), and `V_b = Q/b^2`:

```text
c = (Q/b^2)^(-1/2) = b / sqrt(Q)
c/b = Q^(-1/2)
```

**Exact.** This is the DLH-5R observable `c/b`; it is a decreasing function of
`Q` (monotone decreasing, convex). It explains mechanically why an increasing
`Q` corresponds to a decreasing `c/b` (Phase G).

## 4. Local effective exponent — p_eff

```text
p_eff = - d log(V_b) / d log(b)
      = - d[log(Q) - 2 log(b)]/d log(b)
      = 2 - d log(Q)/d log(b)
```

**Exact** (where regular). Consequences:

- `Q` increasing with `d log Q/d log b in (0,2)`  ⟺  `p_eff in (0,2)`;
- `Q -> K*` constant  ⟹  `p_eff -> 2`;
- `Q ~ b^alpha` (power)  ⟹  `p_eff = 2 - alpha`.

This identity is how "increasing Q" and "p_eff < 2" coexist: a growing `Q`
means `d log Q/d log b > 0`, which *lowers* `p_eff` below 2 as long as the
growth is slower than quadratic in `b`.

## 5. Auxiliary identities used later

- `H_a = -b*V_a` (from `H = -bV`); under S3 (`V_a = R V_b`):
  `H_a = -b*R*V_b = -R*Q/b`.
- `c/b = Q^(-1/2)`, so `sqrt(Q) = b/c = 1/(c/b)`.
- The p=2 candidate values: `H* = Q* = K* = 4/(rho+r_b)^2 = 3265.3061224489797`,
  `c/b* = 1/sqrt(K*) = (rho+r_b)/2 = 0.0175`, `mu_W/b* = -0.0025` (Phase D
  verifies the fixed-point identity; Phase G uses the observed trends).

## 6. What these identities do NOT imply

- They do **not** imply `V_inf = 0` (S2 remains provisional input). They do
  not control `H/b` either: since `V = -H/b`, `H` may diverge sublinearly in
  `b` while `V -> 0` (e.g. `H = sqrt(b)` gives `V = -1/sqrt(b) -> 0`). The
  identities themselves do not select among `H = O(1)` (→ `V = O(1/b)`),
  sublinear growth (→ `V -> 0`), or linear/superlinear growth (→ `V`
  bounded-away-from-zero or diverging); hence they do not imply S2.
- They do not imply `Q -> K*`; they only give the exact bookkeeping
  (`dH/ds = H - Q`, `p_eff = 2 - d log Q/d log b`) used to *test* candidates.
- They do not imply `V_b ~ K*/b^2`; that is a realization claim, not an
  identity.

All arithmetic here is exact; no numerical execution was performed.
