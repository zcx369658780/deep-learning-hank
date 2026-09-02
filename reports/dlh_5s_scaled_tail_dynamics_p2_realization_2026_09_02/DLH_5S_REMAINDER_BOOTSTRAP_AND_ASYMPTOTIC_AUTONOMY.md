# DLH-5S — Scaled HJB, Remainder, and Bootstrap / Asymptotic Autonomy (Phases C & F)

**Issue #45, Phases C & F.** Derives the exact scaled HJB and normalized
remainder, then tests whether a non-circular asymptotic-autonomy theorem closes
the p=2 realization from S1+S2+S3.

## 1. Exact scaled HJB (Phase C)

Multiply the exact decomposition (Phase A)
`rho*V = -2*sqrt(V_b) + r_b*b*V_b + S*V + REM_FULL` by `-b`, using
`H=-bV`, `Q=b^2 V_b`, `b*sqrt(V_b)=sqrt(Q)` (b>0), `S` z-only
(`-b*S*V = S*H`):

```text
rho*H = 2*sqrt(Q) - r_b*Q + S*H - b*REM_FULL

(rho*I - S) H = F(Q) + E,
F(Q) = 2*sqrt(Q) - r_b*Q,
E(b,a,z) = -b * REM_FULL(b,a,z)
```

**S-sign convention verified:** the `S*V` term of the accepted HJB becomes
`+S*H` in scaled form and appears as `-S*H` on the left, i.e. the operator is
`(rho - S)`. On the mean (eigenvalue 0) it is `rho`; on the z-difference
(eigenvalue -2/3) it is `rho + 2/3` (used in Phase E).

## 2. Exact remainder components (every term derived and sign-audited)

From `REM_FULL = L(V_b,z) + r_a_eff(a)*a*V_a + V_b*[d*(R-1) - chi]`
(Phase A), with `V_a = R*V_b = R*Q/b^2` and `H_a = -b*V_a`:

```text
E = E_labor + E_illiquid + E_transfer_adj

E_labor(b,a,z)      = -b * L(V_b,z)
                    = -(5/6) * (0.85*z)^(6/5) * Q^(6/5) * b^(-7/5)        < 0
E_illiquid(b,a,z)   = -b * r_a_eff(a)*a*V_a
                    = r_a_eff(a) * a * H_a
                    = -r_a_eff(a) * a * R * Q / b                        (S3: V_a=R V_b)
E_transfer_adj(b,a,z) = -b * V_b * [d*(R-1) - chi]
                    = (Q/b) * [chi - d*(R-1)]
```

Sign audit: `E_labor < 0` (labor net surplus is a positive addition to
`rho*V`, hence enters `E = -b*REM` negatively); `E_illiquid < 0` under S3
(`R>0`, `H_a<0`, `r_a_eff>0`); `E_transfer_adj` has the sign of
`chi - d*(R-1)`, which is `-0.5*chi_1*d^2/max(a,a_bar) <= 0` on the active
branch (`a>=a_bar`), and `0` on the inaction branch (`d=0`).

**z-symmetric vs z-dependent:** `E_labor` carries `z` explicitly (through
`(0.85 z)^(6/5)`); `E_illiquid` and `E_transfer_adj` carry `z` only through
`H_a`, `R`, `Q`, `d`. In mean/difference decomposition (Phase E) `Delta E`
drives the z-difference mode; `E_bar` drives the mean mode.

## 3. Remainder decay — the weakest sufficient conditions

Do **not** assume p=2. The following are sufficient (with `a` on a fixed compact
interior set):

- **(R1) S3:** `R = O(1)` uniformly.
- **(R2) Scaled-tail tightness (upper):** `Q = b^2*V_b` bounded above uniformly
  on the tail.
- **(R3) compact interior a** (given by the gate scope).

Then:

```text
E_labor      = O(Q^(6/5) * b^(-7/5)) = O(b^(-7/5))      -> 0
E_illiquid   = -r_a_eff(a)*a*R*Q/b   = O(1/b)           -> 0
E_transfer_adj = (Q/b)[chi - d(R-1)] = O(1/b)           -> 0   (d, chi bounded under R1+R3)
```

**Statement:** under S3 + Q-bounded + compact a, `E -> 0` uniformly in s. This
uses only R1 (S3), R2 (new tightness), R3 (scope). It does **not** assume p=2
and is **non-circular**. **S3 alone does NOT imply `E->0`**: without R2, `Q`
could grow (e.g. `V_b` decaying slower than `1/b^2`), in which case the decay
rates above fail.

**Derivative-remainder:** for asymptotic autonomy the flow also needs
`dE/ds -> 0` (uniformly). Each component gains factors of `Q_s/Q` and constant
rates; given R1–R3 plus uniform boundedness of `Q_s/Q` (i.e. bounded
`d log Q/ds`) and of `H_a`, `R`, `d`, `chi` along the flow, `dE/ds -> 0`. This
bounded-`Q_s` control is a **separate derivative-remainder assumption (class B)**
— it is NOT implied by R1–R3 alone.

## 4. Exact vector Q-flow (asymptotic-autonomy limit system)

Differentiate the scaled HJB `(rho - S)H = F(Q) + E` in `s` (commuting with the
z-only `S`) and substitute the exact kinematic identity `dH/ds = H - Q`
(Phase B):

```text
(rho - S) dH/ds = F'(Q) dQ/ds + dE/ds
(rho - S)(H - Q) = F'(Q) dQ/ds + dE/ds
[F(Q) + E] - (rho - S) Q = F'(Q) dQ/ds + dE/ds

F'(Q) dQ/ds = F(Q) - rho*Q + S*Q + E - dE/ds,
F'(Q) = 1/sqrt(Q) - r_b
```

This is the **exact vector scaled-tail flow** (a system across z), valid away
from `F'(Q)=0` (`Q != 1/r_b^2`) wherever the s-differentiation is legitimate.

- **Reduced limit (E=0, S=0, z-symmetric):** reduces exactly to the Phase D
  candidate formula
  `dQ/ds = Q[2 - (rho+r_b) sqrt(Q)]/[1 - r_b sqrt(Q)]` — cross-check PASS.
- **Mean mode at K\*:** `dQ_bar/ds = -7 (Q_bar - K*) + 400 (E_bar - dE_bar/ds)`
  (Phase E) — the reduced eigenvalue with remainder forcing.
- **Asymptotic autonomy:** if `E -> 0` and `dE/ds -> 0` uniformly (R1–R3 +
  derivative control), the system is asymptotically autonomous with limit system
  the reduced scalar (mean) dynamics; the solution tracks the reduced lower-branch
  attractor, and `Q -> K*` follows **provided** the trajectory actually selects
  the regular lower branch and stays non-degenerate.

## 5. Bootstrap theorem attempt — condition classification (Phase F)

Attempt a full compact-interior-a p=2 realization theorem from S1+S2+S3+HJB.
For each candidate condition, classify: **A** derivable from S1+S2+S3+HJB;
**B** genuinely new but non-circular sufficient assumption; **C** circular
(effectively assumes p=2); **D** false / contradicted by a construction.

| # | Candidate condition | Needed for | Classification |
|---|---|---|---|
| 1 | Exact scaled identities (`dH/ds=H-Q`, `p_eff=2-dlogQ/dlogb`, `c/b=Q^(-1/2)`) | bookkeeping | **A** (mechanical) |
| 2 | Exact scaled HJB `(rho-S)H = F(Q)+E` and exact Q-flow | limit system | **A** (given regularity to differentiate) |
| 3 | p=2 fixed point `K* = 4/(rho+r_b)^2`, lower-branch stability (eigenvalue -7), basin `(0,1/r_b^2)` | attractor identification | **A** (reduced-system algebra) |
| 4 | z-difference damping (eigenvalue -273.67) and coefficient synchronization | z-constant leading coefficient | **A at linear order**; global/nonlinear version needs 5-7 |
| 5 | `Q = b^2 V_b` bounded above (scaled-tail tightness, upper) | E_labor->0, E_illiquid->0, E_transfer->0 | **B** (NOT implied by S1+S2+S3) |
| 6 | `Q` bounded away from 0 (non-degeneracy) | F'(Q) regular, c/b bounded, exclude Q->0 branch | **B** (NOT implied by S1+S2+S3) |
| 7 | `Q` away from the reduced-branch singularity `1/r_b^2` + eventual **lower-branch selection** | exclude upper-branch runaway | **B** (NOT implied by S1+S2+S3) |
| 8 | `R=O(1)` uniform | S3 (given); used for E_illiquid, E_transfer | **A** (S3, given) |
| 9 | `E -> 0` uniformly | asymptotic autonomy | **A given 5+8+compact-a** (derived); NOT from S3 alone |
| 10 | `dE/ds -> 0` uniformly (derivative-remainder control) | asymptotically autonomous limit | **B** (needs bounded `dlogQ/ds`, `H_a`, `R` along flow) |
| 11 | z-difference decay / coefficient synchronization (nonlinear) | z-constant limit | **B** (linear part A; nonlinear needs 5-7, 10) |
| 12 | absence of persistent exotic / oscillatory forcing (no `NO-EXOTIC-REGIME` counterexample) | exclude competing asymptotic regimes | **B** (open gate; no counterexample constructed — consistent with DLH-5Q) |
| 13 | `Q -> K*`, `H -> K*`, `V_b ~ K*/b^2`, `c/b -> 0.0175` | conclusion | **C** (circular — must NOT be assumed) |
| 14 | any in-class S3 counterexample to the attractor picture | falsification | **D** (none constructed; consistent with DLH-5Q) |

**Sharpest non-circular missing assumption.** The theorem does **not** close
from S1+S2+S3 alone. The single sharpest non-circular blocker is

```text
Scaled-tail tightness:  Q = b^2*V_b bounded above (and, jointly, non-degenerate:
bounded away from 0 and away from the reduced-branch turning point 1/r_b^2) on
the compact-interior-a tail, plus eventual lower-branch selection.
```

`Q`-boundedness is the lynchpin: it converts S3 into `E -> 0` (item 9), which
is the input that makes the system asymptotically autonomous, which lets the
reduced lower-branch attractor (item 3) govern; the non-degeneracy and
lower-branch selection then exclude the degenerate `Q->0` branch and the
upper-branch runaway. None of these follow from S1+S2+S3 (they are **B**),
none is circular (they do not assume p=2), and no counterexample (**D**) was
found among the correctly analyzed families. The derivative-remainder control
(item 10) and the no-exotic-forcing assumption (item 12) are the secondary
**B** inputs.

## 6. What S3 alone does and does not give

- **Does give:** `R=O(1)` (by definition); with `Q` bounded, `E_illiquid =
  O(1/b)` and `E_transfer_adj = O(1/b)` (R-dependent decay rates); the
  transfer/adjustment net term is subleading; the exact scaled structure.
- **Does NOT give:** `Q`-boundedness (tightness), `Q` away from 0 / from the
  singularity, lower-branch selection, `dE/ds -> 0`, or exclusion of exotic
  forcing. Hence S3 alone does NOT imply `E->0` as a theorem, and does NOT imply
  p=2 realization.
