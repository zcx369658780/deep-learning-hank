# DLH-5S — Scalar z-Symmetric Reduced Dynamics (Phase D)

**Issue #45, Phase D.** A deliberately reduced comparison system: z-difference
mode set to zero, normalized remainder set to zero. This is **not** a theorem
for the full HJB; it is the reduced attractor system whose properties are used
to organize the full analysis.

## 1. Reduced system

```text
rho*H = 2*sqrt(Q) - r_b*Q        (algebraic relation)
dH/ds = H - Q                    (exact kinematic identity, Phase B)
```

The reduced system is the `(E=0, z-symmetric)` projection of the exact scaled
HJB `(rho I - S)H = F(Q) + E` (Phase C file) with `F(Q) = 2*sqrt(Q) - r_b*Q`.

## 2. Algebraic branches Q_±(H)

Set `x = sqrt(Q) >= 0`. The algebraic relation is
`r_b*x^2 - 2x + rho*H = 0`, so

```text
x_±(H) = [1 ± sqrt(1 - r_b*rho*H)] / r_b
Q_±(H) = x_±(H)^2
```

- Real iff `H <= H_max := 1/(rho*r_b) = 1/(0.0003) = 3333.333...`.
- **Turning point** (both branches meet): `H = H_max`, `x = 1/r_b`,
  `Q = 1/r_b^2 = (1/0.015)^2 = 4444.444...`.
- **Lower branch** `Q_-(H)` (minus sign): `x_- = (1 - sqrt(1-r_b rho H))/r_b`;
  `Q_-(0) = 0`, increasing in H, `Q_-(H_max) = 1/r_b^2 = 4444.4`.
- **Upper branch** `Q_+(H)` (plus sign): `x_+ = (1 + sqrt(1-r_b rho H))/r_b`;
  `Q_+(0) = 4/r_b^2 = 17777.8`, decreasing in H, `Q_+(H_max) = 4444.4`.
  On the upper branch `Q >= 4444.4`; `H = 0` is reached at `Q = 4/r_b^2`.

Admissible region: `H in [0, H_max]`, `Q in [0, 4/r_b^2]` with `H>0` requiring
`Q in (0, 4/r_b^2)`.

## 3. Fixed points (H = Q)

From `rho*H = 2*sqrt(Q) - r_b*Q` with `H = Q`:

```text
(rho + r_b)*Q = 2*sqrt(Q)
sqrt(Q) * [ (rho+r_b)*sqrt(Q) - 2 ] = 0
```

- `Q = H = 0` (degenerate fixed point);
- `Q = H = K* := 4/(rho+r_b)^2`.

**Verification of K\*:**

```text
K* = 4/(rho + r_b)^2 = 4/(0.02 + 0.015)^2 = 4/(0.035)^2
   = 4/0.001225 = 3265.3061224489797        (matches the frozen anchor exactly)
```

Which branch carries K*? At `H = K*`, `1 - r_b rho H = 1 - 0.0003*3265.306 = 0.020408`,
`sqrt = 0.142857`. `x_- = (1-0.142857)/0.015 = 57.1429`,
`Q_- = x_-^2 = 3265.306 = K*`. So **K* lies on the lower branch** (the upper
branch at this H has `Q_+ = 5805`). The p=2 candidate is a lower-branch fixed
point.

## 4. Exact reduced Q-flow (candidate identity verified, not assumed)

On the algebraic surface, `H = (2*sqrt(Q) - r_b*Q)/rho`, and

```text
dH/ds = H - Q = [2*sqrt(Q) - (rho+r_b)*Q]/rho
dH/dQ = (1/rho)*(1/sqrt(Q) - r_b)
```

so (away from `F'(Q) = 0`, i.e. `Q != 1/r_b^2`):

```text
dQ/ds = (dH/ds)/(dH/dQ)
      = Q * [2 - (rho+r_b)*sqrt(Q)] / [1 - r_b*sqrt(Q)]
```

**The candidate identity in the Issue is EXACT under the exact derivation**
(sign, denominator, and numerator all verified above). The same formula falls
out of the general exact vector Q-flow of Phase C with `E=0, S=0`. The singular
denominator at `Q = 1/r_b^2 = 4444.4` is exactly the branch turning point.

## 5. Sign of dQ/ds and basin/trapping region

Let `a_sum := rho + r_b = 0.035`. Recall `sqrt(K*) = 2/a_sum = 57.1429`,
`1/r_b = 66.667`.

- **Q in (0, K\*):** numerator `2 - a_sum*sqrt(Q) > 0`; denominator
  `1 - r_b*sqrt(Q) > 0` (since `r_b*sqrt(K*) = 2r_b/a_sum = 0.030/0.035 = 6/7 < 1`).
  ⟹ `dQ/ds > 0`: **Q < K\* moves monotonically toward K\***.
- **Q in (K\*, 1/r_b^2):** numerator < 0, denominator > 0 ⟹ `dQ/ds < 0`:
  Q decreases toward K*.
- **Q = 1/r_b^2 = 4444.4 (turning point / singularity):** denominator = 0;
  `dQ/ds` diverges; this is the boundary of the trapping region.
- **Q > 1/r_b^2 (upper branch):** numerator < 0, denominator < 0 ⟹
  `dQ/ds > 0`: **runaway** (Q increases without bound; H crosses 0 at
  `Q = 4/r_b^2` and the H>0 admissible region is exited).

**Basin of K\* (within the reduced scalar system, H>0):**
`Q in (0, 1/r_b^2)`, i.e. the entire lower branch except the two endpoints
(`Q=0` is a repelling fixed point, `Q=1/r_b^2` is the singular turning point).
The upper branch `Q > 1/r_b^2` is run-away.

## 6. Local stability of the p=2 fixed point

Linearize `dQ/ds = f(Q)` around `K*`, `f(Q) = Q[2 - a_sum sqrt(Q)]/[1 - r_b sqrt(Q)]`.
`f'(K*) = N'(K*)/D(K*)` with `N' = 2 - a_sum sqrt(Q) - (a_sum/2) sqrt(Q)` and
`D = 1 - r_b sqrt(Q)`:

```text
N'(K*)  = 2 - (3/2)*a_sum*(2/a_sum) = -1
D(K*)   = 1 - 2*r_b/a_sum = (rho - r_b)/(rho + r_b) = 0.005/0.035 = 1/7
lambda  = f'(K*) = -1/(1/7) = -7   (in s)
```

So `dQ/ds ~ -7 (Q - K*)` in any sufficiently small neighborhood of K* where
the linearization is valid: a **stable node with local homogeneous eigenvalue
-7 in s**, i.e. for the **unforced** reduced system in that neighborhood
`Q - K* ~ C*exp(-7s) = C*b^(-7)`. This is a *local* (linearized) relaxation
rate near K* only; it is not promoted to a global trajectory approximation, and
it is not a full-HJB convergence rate (Phase C/F treats the forcing).

**Rev 3 (review `5518243412`):** the `b^(-7)` estimate is **local** — it is the
eigenvalue of the linearization about K* and holds only where `Q - K*` is
small. It must **not** be extrapolated to trajectories starting far from K*
(e.g. `Q=315`). Away from the local neighborhood of K*, the authority is the
**exact nonlinear reduced flow** `dQ/ds = f(Q)`, whose rigorously established
content here is sign/qualitative: `Q in (0,K*) => Q_s > 0` (monotone increase),
`Q in (K*,1/r_b^2) => Q_s < 0`, `Q > 1/r_b^2 => Q_s > 0` (run-away). No
controlled nonlinear trajectory timing ("by which b is Q essentially K*") is
derived in this package, and no numerical trajectory calculation is performed.

## 7. Reduced-system predictions to carry forward

1. **p=2 candidate is a lower-branch fixed point of the exact nonlinear
   reduced flow** with a **local** homogeneous eigenvalue `-7` in s (near K*).
   The exact nonlinear flow on `(0, 1/r_b^2)` moves monotonically toward it
   (sign results of section 5); this is the reduced basin statement.
2. **Q < K\* ⟹ Q increasing** (exact nonlinear sign result) — the exact
   mechanism behind the DLH-5R direction `Q: 315 -> 485 -> 610 -> 736`.
3. **c/b = Q^(-1/2)** decreases monotonically as Q grows toward K*
   (`0.0175 = 1/sqrt(K*)` is the target).
4. **The upper branch is run-away**: without an additional lower-branch
   selection / `Q < 1/r_b^2` bound, the reduced system alone does not guarantee
   the attractor is reached.
5. **Local vs global (Rev 3):** the homogeneous rate `-7` in s is **local** to
   a small neighborhood of K*; no controlled trajectory timing ("essentially at
   K* by some b") is derived away from K*, and none is computed numerically.
   The observed DLH-5R solution stays far below K* at `b<=56.6`, so on the
   accessible range the **full-system remainder/coupling** (the net forcing
   `S Q + E - E_s` of the exact flow) materially modifies/retards the motion
   toward the reduced attractor; its **net sign is not identified** from the
   accepted medians alone. The scalar z-symmetric reduced system is an
   **invariant reduced subsystem** of the `E=0` coupled vector limit (Rev 3);
   it is not by itself a description of the finite-window trajectory (Phase G),
   and a slowly-decaying forcing can dominate any realized rate (Phase C/F).

## 8. Scope caveat

This is a **reduced comparison system**; its local stability and basin are NOT
promoted to a theorem for the full HJB. The full system (with remainder E,
z-coupling, and a-dependence) is addressed in Phases C/E/F.
