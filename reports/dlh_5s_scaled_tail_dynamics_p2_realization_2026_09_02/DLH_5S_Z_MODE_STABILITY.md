# DLH-5S — z-Switching Mean/Difference Modes (Phase E)

**Issue #45, Phase E.** Restores the frozen two-state symmetric Markov switch
generator and analyzes the scaled system in mean and z-difference modes around
the z-symmetric p=2 candidate.

## 1. Switch structure

`S` = symmetric two-state z-generator with rate `1/3`:

```text
S = [[-1/3, 1/3],
     [ 1/3,-1/3]],      spectrum {0, -2/3}
```

Decompose any z-dependent object `X(z)` into mean and difference modes:

```text
X_bar = (X(z1) + X(z2))/2        (z-constant mode; S X_bar = 0)
Delta_X = X(z2) - X(z1)          (z-difference mode; S Delta_X = -(2/3) Delta_X)
```

`S` acts only on the `z` index; it commutes with the `s = log b` derivative.

## 2. Exact mean/difference scaled HJB

From the exact scaled HJB `(rho I - S)H = F(Q) + E` (Phase C), with
`F(Q) = 2*sqrt(Q) - r_b*Q`:

```text
Mean:      rho * H_bar          = F(Q)_bar        + E_bar
Difference: (rho + 2/3) Delta_H = Delta_F(Q)      + Delta_E
```

The switch eigenvalue enters as `+2/3` on the difference mode (this is the
`S`-sign convention verified in the Phase C derivation: `(rho - S)H` has
eigenvalue `rho - 0 = rho` on the mean and `rho - (-2/3) = rho + 2/3` on the
difference).

## 3. The z-symmetric p=2 candidate is a fixed point of the E=0 coupled system

The candidate `(H_bar, Q_bar) = (K*, K*)`, `(Delta_H, Delta_Q) = (0, 0)` is a
fixed point of the `E=0` coupled system:

- Mean mode at `Q_bar = K*`: `rho*H_bar = F(K*) = 2*sqrt(K*) - r_b*K*`, and
  `F(K*) - rho*K* = 2*sqrt(K*) - (rho+r_b)*K* = 0` (fixed-point identity,
  Phase D). With `H_bar = K*` this is satisfied.
- Difference mode: `Delta_H = Delta_Q = 0` satisfies `(rho+2/3)Delta_H = 0`.

With `E != 0` the candidate is a "quasi-fixed point": the mean mode is driven
by `E_bar` and `d E_bar/ds`; the difference mode is driven by `Delta_E` and
`d Delta_E/ds` (section 5).

## 4. Linearization around the p=2 candidate

At `Q_bar = K*`:

```text
F'(K*) = 1/sqrt(K*) - r_b = (rho+r_b)/2 - r_b = (rho - r_b)/2 = 0.0025
F'(K*) - rho = (rho-r_b)/2 - rho = -(rho+r_b)/2 = -0.0175
```

**Difference mode (Delta_Q).** Using the exact vector Q-flow of Phase C
(`F'(Q) dQ/ds = F(Q) - rho Q + S Q + E - dE/ds`), the difference of the
linearized numerator around `Q_bar = K*` is:

```text
Delta[F(Q) - rho Q + S Q] ~ (F'(K*) - rho) Delta_Q + S Delta_Q
                          = -(rho+r_b)/2 * Delta_Q - (2/3) * Delta_Q
```

so

```text
d(Delta_Q)/ds = - [ (rho+r_b)/2 + 2/3 ] / [ (rho-r_b)/2 ] * Delta_Q
                    + [ Delta_E - d(Delta_E)/ds ] / [ (rho-r_b)/2 ]
```

```text
lambda_diff = - [0.0175 + 0.66667] / 0.0025 = -273.67   (in s)
```

**The z-difference mode is strongly damped:** `Delta_Q ~ exp(lambda_diff s) =
b^(-273.67)` at linear order. The two-state switch rate provides the strong
`2/3` damping, amplified by the small `(rho-r_b)/2 = 0.0025` divisor.

**Slaving of Delta_H.** From `(rho + 2/3) Delta_H = (rho-r_b)/2 Delta_Q + Delta_E`:

```text
Delta_H = [ (rho-r_b)/2 / (rho + 2/3) ] * Delta_Q + Delta_E/(rho + 2/3)
        = 0.00364 * Delta_Q + 1.456 * Delta_E
```

`Delta_H` is slaved to `Delta_Q` (coefficient ~0.4%) and to `Delta_E`.

**Mean mode (Q_bar).** The mean of the linearized Q-flow around `K*`:

```text
d(Q_bar)/ds = - (rho+r_b)/(rho-r_b) * (Q_bar - K*) + 2*(E_bar - d E_bar/ds)/(rho-r_b)
            = -7 * (Q_bar - K*) + 400*(E_bar - d E_bar/ds)
```

This reproduces the reduced-system eigenvalue `-7` (Phase D) and shows the mean
mode is **forced by the mean remainder** `E_bar` and its `s`-derivative. The
z-symmetric reduced dynamics of Phase D are therefore exactly the `E=0` mean
mode.

## 5. Stability summary and conditions

| Mode | Eigenvalue (in s) | b-rate | Character |
|---|---|---|---|
| Mean (Q_bar) | -7 | b^(-7) | stable node; forced by E_bar, dE_bar/ds |
| Difference (Delta_Q) | -273.67 | b^(-273.67) | strongly damped; forced by Delta_E, dDelta_E/ds |
| Difference (Delta_H) | slaved to Delta_Q | b^(-273.67) | damped via Delta_Q + Delta_E |

- **Isolated candidate:** the z-symmetric p=2 candidate is an isolated fixed
  point of the `E=0` coupled system; it is not an entire manifold.
- **Difference mode damping:** strong (rate 273.67 in s). No spectral
  **nonresonance** assumption is needed at linear order: the difference rate
  `-(rho+r_b)/2 - 2/3` divided by `(rho-r_b)/2` is far from 0 and from the mean
  rate -7; the frozen switch spectrum `{0,-2/3}` supplies the `2/3` gap that
  drives the damping. (The DLH-5Q O(1/b) coefficient equation's nonresonance
  requirement, `(rho+r_b)/2 = 0.0175 notin {0,-2/3}`, is a separate, mean-mode
  statement and is preserved here.)
- **Coefficient synchronization** (Delta_Q -> 0, Delta_H -> 0, so the leading
  tail coefficient becomes z-constant) holds **conditionally**: at linear order
  via the strong damping, provided (i) the linearization is valid (perturbations
  small), and (ii) the forcing `Delta_E` and `d Delta_E/ds` are small/integrable
  enough not to sustain the difference mode. Both conditions are part of the
  explicit non-circular assumption set of Phase F; they are NOT implied by
  S1+S2+S3 alone.
- **Do not replace the coupled system by the scalar formula if z-dependent
  coefficients survive at leading order:** here the p=2 candidate is z-constant,
  so the difference mode decays and the scalar (mean) formula is the valid
  asymptotic reduction. If a candidate had z-dependent leading coefficients, the
  scalar reduction would be invalid; no such candidate is generated by this
  analysis (consistent with DLH-5Q Phase D: the required spectral value
  `(rho+r_b)/2 = 0.0175 notin {0,-2/3}` excludes z-dependent O(1/b) amplitudes).

## 6. Exact / linearized / local / conditional labeling

- **Exact:** the mean/difference decomposition of the scaled HJB; the fixed
  point of the E=0 coupled system; the `+2/3` switch sign.
- **Linearized:** the eigenvalues -7 and -273.67; the slaving coefficient.
- **Local:** the linearization holds in a neighborhood of the candidate.
- **Conditional:** the actual convergence (Delta -> 0, coefficient
  synchronization) requires the Phase F remainder/tightness assumptions.

No numerical execution was performed.
